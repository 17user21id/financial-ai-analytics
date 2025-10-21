"""
Chat Session Model
Represents a chat session in the chat_sessions table
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class ChatSession:
    """Represents a chat session in the chat_sessions table"""

    chat_id: str
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    context_summary: Optional[str] = None
    metadata: Optional[str] = None  # JSON string

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_activity": (
                self.last_activity.isoformat() if self.last_activity else None
            ),
            "context_summary": self.context_summary,
            "metadata": self.metadata,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChatSession":
        """Create from dictionary"""
        return ChatSession(
            chat_id=data["chat_id"],
            user_id=data.get("user_id"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            last_activity=(
                datetime.fromisoformat(data["last_activity"])
                if data.get("last_activity")
                else None
            ),
            context_summary=data.get("context_summary"),
            metadata=data.get("metadata"),
        )

    @staticmethod
    def from_row(row: tuple) -> "ChatSession":
        """Create from database row"""
        return ChatSession(
            chat_id=row[0],
            user_id=row[1] if len(row) > 1 else None,
            created_at=(
                datetime.fromisoformat(row[2]) if len(row) > 2 and row[2] else None
            ),
            last_activity=(
                datetime.fromisoformat(row[3]) if len(row) > 3 and row[3] else None
            ),
            context_summary=row[4] if len(row) > 4 else None,
            metadata=row[5] if len(row) > 5 else None,
        )
