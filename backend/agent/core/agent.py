"""Main Agent class that orchestrates all building blocks."""
from typing import Any, Optional
import json

from agent.core.intelligence import Intelligence
from agent.core.memory import Memory
from agent.core.tools import Tool, ToolRegistry
from agent.core.validation import ValidationSchema
from agent.core.recovery import Recovery
from agent.core.feedback import FeedbackControl


class Agent:
    """Universal AI Agent with all 6 building blocks."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        api_key: str,
        model: str = "gpt-4o",
        require_approval: bool = False,
        max_retries: int = 3,
        max_history: int = 100,
    ):
        """Initialize Agent with all components.
        
        Args:
            name: Agent identifier.
            system_prompt: System instructions.
            api_key: OpenAI API key.
            model: Model to use.
            require_approval: Whether to require human approval.
            max_retries: Maximum retry attempts.
            max_history: Maximum conversation history size.
        """
        self.name = name
        self.system_prompt = system_prompt
        self.require_approval = require_approval

        self.intelligence = Intelligence(api_key=api_key, model=model)
        self.memory = Memory(max_history=max_history)
        self.tools = ToolRegistry()
        self.validation = ValidationSchema()
        self.recovery = Recovery(max_retries=max_retries)
        self.feedback = FeedbackControl()

    def run(
        self,
        user_input: str,
        use_memory: bool = True,
        require_approval: Optional[bool] = None,
    ) -> str:
        """Process user input through all building blocks.
        
        Args:
            user_input: User's message.
            use_memory: Whether to use conversation memory.
            require_approval: Override for approval requirement.
            
        Returns:
            Agent's response string.
        """
        try:
            context = ""
            if use_memory and self.memory.conversation_history:
                context = self.memory.get_context(last_n=3)

            full_prompt = user_input
            if context:
                full_prompt = f"Previous conversation:\n{context}\n\nCurrent request: {user_input}"

            if self.tools.list_tools():
                tools_info = self.tools.get_tool_description()
                full_prompt += f"\n\nAvailable tools:\n{tools_info}"
                full_prompt += """
To use a tool, respond with EXACTLY this format:
USE_TOOL: tool_name
PARAMS: param1=value1, param2=value2

Example:
USE_TOOL: get_weather
PARAMS: city=London

After using a tool, provide a natural response to the user."""

            response = self.recovery.execute_with_retry(
                self.intelligence.generate_decision,
                prompt=full_prompt,
                system_prompt=self.system_prompt,
                temperature=0.7,
            )

            if "USE_TOOL:" in response:
                lines = response.split("\n")
                tool_name = None
                params = {}

                for line in lines:
                    if line.startswith("USE_TOOL:"):
                        tool_name = line.replace("USE_TOOL:", "").strip()
                    elif line.startswith("PARAMS:"):
                        params_str = line.replace("PARAMS:", "").strip()
                        for param in params_str.split(","):
                            if "=" in param:
                                key, value = param.split("=", 1)
                                params[key.strip()] = value.strip()

                if tool_name:
                    try:
                        tool_result = self.execute_tool(tool_name, **params)
                        final_prompt = f"""Original user request: {user_input}

Tool used: {tool_name}
Tool result: {json.dumps(tool_result, indent=2)}

Based on this data, provide a clear, natural language response to the user."""

                        response = self.recovery.execute_with_retry(
                            self.intelligence.generate_decision,
                            prompt=final_prompt,
                            system_prompt=self.system_prompt,
                            temperature=0.7,
                        )
                    except Exception:
                        response = "I encountered an issue while processing your request."

            needs_approval = (
                require_approval if require_approval is not None else self.require_approval
            )

            if needs_approval:
                self.feedback.request_approval(
                    action="Generate response",
                    details={"user_input": user_input},
                    confidence=0.85,
                )

            if use_memory:
                self.memory.add_interaction(
                    user_input=user_input,
                    agent_response=response,
                )

            return response

        except Exception as e:
            error_response = self.recovery.graceful_failure(e, context="run method")
            return json.dumps(error_response, indent=2)

    def register_tool(self, tool: Tool) -> None:
        """Register a new tool for the agent.
        
        Args:
            tool: Tool instance to register.
        """
        self.tools.register(tool)

    def execute_tool(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:
        """Execute a registered tool.
        
        Args:
            tool_name: Name of tool to execute.
            **kwargs: Tool parameters.
            
        Returns:
            Tool execution result.
        """
        return self.tools.execute(tool_name, **kwargs)

    def get_status(self) -> dict[str, Any]:
        """Get agent status and statistics.
        
        Returns:
            Dictionary with agent status.
        """
        return {
            "name": self.name,
            "memory": self.memory.get_summary(),
            "tools": self.tools.list_tools(),
            "errors": self.recovery.get_error_summary(),
            "approvals": len(self.feedback.approval_log),
        }
