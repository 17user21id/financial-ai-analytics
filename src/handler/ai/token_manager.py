"""
Token Manager Utility
Handles token estimation and conversation history formatting with token limits
"""

import logging
from typing import List

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages token limits and conversation history formatting"""

    def __init__(self, max_context_tokens: int = 4000):
        """
        Initialize token manager

        Args:
            max_context_tokens: Maximum tokens for context window (default 4000)
        """
        self.max_context_tokens = max_context_tokens

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Uses rough approximation: 1 token ≈ 4 characters

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count
        """
        if not text:
            return 0
        return len(text) // 4

    def format_history_with_limit(
        self,
        history: List[str],
        reserved_tokens: int,
        empty_message: str = "No previous conversation",
    ) -> str:
        """
        Format conversation history within token limits

        Args:
            history: List of conversation summaries (most recent first - ORDER BY timestamp DESC)
            reserved_tokens: Tokens to reserve for query/schema/prompt
            empty_message: Message to return if no history available

        Returns:
            Formatted conversation history string that fits within token limit
            Maintains MOST RECENT FIRST ordering with explicit labels
        """
        if not history:
            return empty_message

        # Calculate available tokens for history
        available_tokens = self.max_context_tokens - reserved_tokens

        if available_tokens <= 0:
            logger.warning(
                f"No tokens available for history (max: {self.max_context_tokens}, "
                f"reserved: {reserved_tokens})"
            )
            return "No previous conversation (insufficient token budget)"

        # Select history items that fit within token limit
        # Start from most recent (index 0) and add items until token limit
        selected_history = []
        current_tokens = 0

        for item in history:
            item_tokens = self.estimate_tokens(item)
            if current_tokens + item_tokens <= available_tokens:
                selected_history.append(item)
                current_tokens += item_tokens
            else:
                break

        if not selected_history:
            return f"No previous conversation (history too large for token limit of {available_tokens})"

        # Format with explicit labels: [MOST RECENT], [2 queries ago], etc.
        formatted_items = []
        for idx, item in enumerate(selected_history):
            if idx == 0:
                label = "[MOST RECENT]"
            elif idx == 1:
                label = "[2 queries ago]"
            elif idx == 2:
                label = "[3 queries ago]"
            else:
                label = f"[{idx + 1} queries ago]"

            formatted_items.append(f"{label} {item}")

        formatted = "\n".join(formatted_items)

        logger.info(
            f"Formatted {len(selected_history)}/{len(history)} history items "
            f"(~{current_tokens} tokens, limit: {available_tokens})"
        )

        return formatted

    def get_token_budget(self, reserved_tokens: int) -> dict:
        """
        Get token budget breakdown

        Args:
            reserved_tokens: Tokens reserved for other purposes

        Returns:
            Dictionary with token budget information
        """
        available = max(0, self.max_context_tokens - reserved_tokens)

        return {
            "total_tokens": self.max_context_tokens,
            "reserved_tokens": reserved_tokens,
            "available_tokens": available,
            "percentage_available": (
                (available / self.max_context_tokens * 100)
                if self.max_context_tokens > 0
                else 0
            ),
        }
