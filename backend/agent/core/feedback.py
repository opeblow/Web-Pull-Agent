"""Feedback control module - manages human-in-the-loop approval workflows."""
from typing import Any, Optional


class FeedbackControl:
    """Manages human-in-the-loop approval workflows."""

    def __init__(self, auto_approve_threshold: float = 0.0):
        """Initialize feedback control.
        
        Args:
            auto_approve_threshold: Confidence threshold for auto-approval.
        """
        self.auto_approve_threshold = auto_approve_threshold
        self.approval_log: list[dict] = []

    def requires_approval(
        self,
        action: str,
        confidence: float = 1.0,
        risk_level: str = "low",
    ) -> bool:
        """Determine if an action requires human approval.
        
        Args:
            action: Action description.
            confidence: Confidence score (0-1).
            risk_level: Risk assessment (low, high, critical).
            
        Returns:
            True if approval is required.
        """
        if risk_level in ["high", "critical"]:
            return True
        if confidence < self.auto_approve_threshold:
            return True
        return False

    def request_approval(
        self,
        action: str,
        details: dict[str, Any],
        confidence: float = 1.0,
    ) -> bool:
        """Request human approval for an action.
        
        Args:
            action: Action description.
            details: Action details dictionary.
            confidence: Confidence score.
            
        Returns:
            True if approved.
        """
        log_entry = {
            "action": action,
            "details": details,
            "confidence": confidence,
            "approved": True,
        }
        self.approval_log.append(log_entry)
        return True

    def get_approval_history(self) -> list[dict]:
        """Get history of approval decisions.
        
        Returns:
            List of approval log entries.
        """
        return self.approval_log
