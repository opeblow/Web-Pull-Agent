"""Memory module - stores and retrieves conversation history."""
from typing import Optional, Any
from datetime import datetime


class Memory:
    """Stores and retrieves conversation history for context."""

    def __init__(self, max_history: int = 100):
        """Initialize memory storage.
        
        Args:
            max_history: Maximum number of interactions to keep.
        """
        self.conversation_history: list[dict[str, Any]] = []
        self.long_term_storage: dict[str, Any] = {}
        self.max_history = max_history

    def add_interaction(
        self,
        user_input: str,
        agent_response: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Store an interaction in memory.
        
        Args:
            user_input: User's input text.
            agent_response: Agent's response text.
            metadata: Optional metadata dictionary.
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata or {},
        }
        self.conversation_history.append(interaction)

        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def get_context(self, last_n: Optional[int] = None) -> str:
        """Get conversation context as a formatted string.
        
        Args:
            last_n: Number of recent interactions to retrieve.
            
        Returns:
            Formatted context string.
        """
        history = self.conversation_history[-last_n:] if last_n else self.conversation_history

        context_parts = []
        for interaction in history:
            context_parts.append(f"User: {interaction['user_input']}")
            context_parts.append(f"Agent: {interaction['agent_response']}")

        return "\n".join(context_parts)

    def store_fact(self, key: str, value: Any) -> None:
        """Store long-term information.
        
        Args:
            key: Storage key.
            value: Value to store.
        """
        self.long_term_storage[key] = value

    def retrieve_fact(self, key: str) -> Optional[Any]:
        """Retrieve stored information.
        
        Args:
            key: Storage key.
            
        Returns:
            Stored value or None.
        """
        return self.long_term_storage.get(key)

    def clear_short_term(self) -> None:
        """Clear conversation history (short-term memory)."""
        self.conversation_history.clear()

    def get_summary(self) -> dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dictionary with memory stats.
        """
        return {
            "conversation_count": len(self.conversation_history),
            "stored_facts": len(self.long_term_storage),
            "memory_keys": list(self.long_term_storage.keys()),
        }
