"""Tools module - base classes for agent tools."""
from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """Abstract base class for agent tools."""

    def __init__(self, name: str, description: str):
        """Initialize tool with name and description.
        
        Args:
            name: Tool identifier.
            description: Human-readable description.
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters.
        
        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Tool must implement execute method.")


class ToolRegistry:
    """Registry for managing and executing available tools."""

    def __init__(self):
        """Initialize empty tool registry."""
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a new tool.
        
        Args:
            tool: Tool instance to register.
        """
        self.tools[tool.name] = tool

    def execute(self, tool_name: str, **kwargs) -> dict[str, Any]:
        """Execute tool by name.
        
        Args:
            tool_name: Name of tool to execute.
            **kwargs: Tool parameters.
            
        Returns:
            Dictionary with success status and result/error.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")

        tool = self.tools[tool_name]
        try:
            result = tool.execute(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_tool_description(self) -> str:
        """Get description of all available tools.
        
        Returns:
            Formatted string of tool descriptions.
        """
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)

    def list_tools(self) -> list[str]:
        """List all available tool names.
        
        Returns:
            List of tool name strings.
        """
        return list(self.tools.keys())
