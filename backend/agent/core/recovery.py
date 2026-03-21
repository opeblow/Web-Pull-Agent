"""Recovery module - handles errors and provides fallback mechanisms."""
from typing import Any, Callable, Optional
from datetime import datetime


class Recovery:
    """Handles errors and provides fallback mechanism with retry logic."""

    def __init__(self, max_retries: int = 3):
        """Initialize recovery handler.
        
        Args:
            max_retries: Maximum retry attempts before giving up.
        """
        self.max_retries = max_retries
        self.error_log: list[dict] = []

    def execute_with_retry(
        self,
        func: Callable,
        *args: Any,
        fallback: Optional[Callable] = None,
        **kwargs: Any,
    ) -> Any:
        """Execute function with retry logic.
        
        Args:
            func: Function to execute.
            *args: Positional arguments for function.
            fallback: Optional fallback function.
            **kwargs: Keyword arguments for function.
            
        Returns:
            Function result or fallback result.
            
        Raises:
            Exception: Last exception if all retries fail.
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                last_error = e
                self.error_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "function": getattr(func, "__name__", str(func)),
                    "attempt": attempt + 1,
                    "error": str(e),
                })

        if fallback:
            try:
                return fallback(*args, **kwargs)
            except Exception as e:
                raise e

        raise last_error

    def graceful_failure(self, error: Exception, context: str = "") -> dict[str, Any]:
        """Return a graceful failure response.
        
        Args:
            error: Exception that occurred.
            context: Context description.
            
        Returns:
            Formatted error response dictionary.
        """
        return {
            "status": "error",
            "message": "I ran into an issue and could not finish the task.",
            "error_type": type(error).__name__,
            "context": context,
            "suggestion": "Please try rephrasing your request or try again later.",
        }

    def get_error_summary(self) -> dict[str, Any]:
        """Get summary of errors encountered.
        
        Returns:
            Dictionary with error statistics.
        """
        return {
            "total_errors": len(self.error_log),
            "recent_errors": self.error_log[-5:],
        }
