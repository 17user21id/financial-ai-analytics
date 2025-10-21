"""
Chat Message Model
Represents a message in the chat_messages table
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
import json


@dataclass
class ChatMessage:
    """Represents a message in the chat_messages table"""

    id: Optional[int] = None
    chat_id: Optional[str] = None
    message_type: Optional[str] = None  # 'user' or 'assistant'
    content: Optional[str] = None
    query_intent: Optional[str] = None
    data_points: Optional[str] = None  # JSON string
    prompt: Optional[str] = None  # Original prompt sent to LLM
    llm_response: Optional[str] = None  # Raw LLM response
    summary: Optional[str] = None  # Structured summary of the interaction
    token_count: Optional[int] = None  # Token count for this interaction
    timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "message_type": self.message_type,
            "content": self.content,
            "query_intent": self.query_intent,
            "data_points": self.data_points,
            "prompt": self.prompt,
            "llm_response": self.llm_response,
            "summary": self.summary,
            "token_count": self.token_count,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    def get_data_points_as_list(self) -> Optional[List[Dict]]:
        """Parse data_points JSON string to list"""
        if self.data_points:
            try:
                return json.loads(self.data_points)
            except json.JSONDecodeError:
                return None
        return None

    def set_data_points_from_list(self, data_points: List[Dict]):
        """Set data_points from list"""
        self.data_points = json.dumps(data_points) if data_points else None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChatMessage":
        """Create from dictionary"""
        return ChatMessage(
            id=data.get("id"),
            chat_id=data.get("chat_id"),
            message_type=data.get("message_type"),
            content=data.get("content"),
            query_intent=data.get("query_intent"),
            data_points=data.get("data_points"),
            prompt=data.get("prompt"),
            llm_response=data.get("llm_response"),
            summary=data.get("summary"),
            token_count=data.get("token_count"),
            timestamp=(
                datetime.fromisoformat(data["timestamp"])
                if data.get("timestamp")
                else None
            ),
        )

    @staticmethod
    def from_row(row: tuple) -> "ChatMessage":
        """Create from database row"""
        return ChatMessage(
            id=row[0] if len(row) > 0 else None,
            chat_id=row[1] if len(row) > 1 else None,
            message_type=row[2] if len(row) > 2 else None,
            content=row[3] if len(row) > 3 else None,
            query_intent=row[4] if len(row) > 4 else None,
            data_points=row[5] if len(row) > 5 else None,
            prompt=row[6] if len(row) > 6 else None,
            llm_response=row[7] if len(row) > 7 else None,
            summary=row[8] if len(row) > 8 else None,
            token_count=row[9] if len(row) > 9 else None,
            timestamp=(
                datetime.fromisoformat(row[10]) if len(row) > 10 and row[10] else None
            ),
        )
