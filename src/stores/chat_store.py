"""
Chat Store for managing conversation data and chat sessions
Handles all database operations for chat-related functionality
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChatSession:
    """Chat session data model"""

    chat_id: str
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    context_summary: str = ""
    metadata: Optional[str] = None


@dataclass
class ChatMessage:
    """Chat message data model"""

    id: Optional[int] = None
    chat_id: str = ""
    message_type: str = ""
    content: str = ""
    query_intent: Optional[str] = None
    data_points: Optional[List[Dict]] = None
    prompt: Optional[str] = None
    llm_response: Optional[str] = None
    summary: Optional[str] = None
    token_count: Optional[int] = None
    timestamp: Optional[datetime] = None


class ChatStore:
    """Store for managing chat sessions and messages"""

    def __init__(self, db_path: str = "financial_data.db"):
        self.db_path = db_path
        self.init_tables()

    def init_tables(self):
        """Initialize chat-related tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Chat sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    chat_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_summary TEXT,
                    metadata TEXT
                )
            """
            )

            # Chat messages table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT,
                    message_type TEXT, -- 'user' or 'assistant'
                    content TEXT,
                    query_intent TEXT,
                    data_points TEXT, -- JSON
                    prompt TEXT, -- Original prompt sent to LLM
                    llm_response TEXT, -- Raw LLM response
                    summary TEXT, -- Structured summary of the interaction
                    token_count INTEGER, -- Token count for this interaction
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES chat_sessions (chat_id)
                )
            """
            )

            conn.commit()

    def create_chat_session(self, chat_id: str, user_id: str = None) -> ChatSession:
        """Create a new chat session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO chat_sessions 
                (chat_id, user_id, created_at, last_activity, context_summary)
                VALUES (?, ?, ?, ?, ?)
            """,
                (chat_id, user_id, datetime.now(), datetime.now(), ""),
            )
            conn.commit()

        return ChatSession(
            chat_id=chat_id,
            user_id=user_id,
            created_at=datetime.now(),
            last_activity=datetime.now(),
        )

    def get_chat_session(self, chat_id: str) -> Optional[ChatSession]:
        """Get existing chat session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT chat_id, user_id, created_at, last_activity, context_summary
                FROM chat_sessions WHERE chat_id = ?
            """,
                (chat_id,),
            )

            row = cursor.fetchone()
            if row:
                return ChatSession(
                    chat_id=row[0],
                    user_id=row[1],
                    created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                    last_activity=datetime.fromisoformat(row[3]) if row[3] else None,
                    context_summary=row[4] or "",
                )
        return None

    def add_message(self, message: ChatMessage) -> int:
        """Add a message to chat history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_messages 
                (chat_id, message_type, content, query_intent, data_points, 
                 prompt, llm_response, summary, token_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    message.chat_id,
                    message.message_type,
                    message.content,
                    message.query_intent,
                    json.dumps(message.data_points) if message.data_points else None,
                    message.prompt,
                    message.llm_response,
                    message.summary,
                    message.token_count,
                ),
            )

            message_id = cursor.lastrowid

            # Update last activity
            cursor.execute(
                """
                UPDATE chat_sessions 
                SET last_activity = CURRENT_TIMESTAMP 
                WHERE chat_id = ?
            """,
                (message.chat_id,),
            )

            conn.commit()
            return message_id

    def get_messages(
        self, chat_id: str, limit: int = 10, order_desc: bool = True
    ) -> List[ChatMessage]:
        """Get messages for a chat session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            order_clause = "DESC" if order_desc else "ASC"
            cursor.execute(
                f"""
                SELECT id, chat_id, message_type, content, query_intent, data_points, 
                       prompt, llm_response, summary, token_count, timestamp
                FROM chat_messages 
                WHERE chat_id = ? 
                ORDER BY timestamp {order_clause}
                LIMIT ?
            """,
                (chat_id, limit),
            )

            messages = []
            for row in cursor.fetchall():
                messages.append(
                    ChatMessage(
                        id=row[0],
                        chat_id=row[1],
                        message_type=row[2],
                        content=row[3],
                        query_intent=row[4],
                        data_points=json.loads(row[5]) if row[5] else [],
                        prompt=row[6],
                        llm_response=row[7],
                        summary=row[8],
                        token_count=row[9],
                        timestamp=datetime.fromisoformat(row[10]) if row[10] else None,
                    )
                )

            return messages

    def get_conversation_summaries(self, chat_id: str, limit: int = 5) -> List[str]:
        """Get recent conversation summaries for context"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT summary FROM chat_messages 
                WHERE chat_id = ? AND summary IS NOT NULL AND summary != ''
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (chat_id, limit),
            )

            summaries = [str(row[0]) for row in cursor.fetchall() if row[0] is not None]
            return summaries

    def get_messages_with_token_limit(
        self, chat_id: str, max_tokens: int = 2000, limit: int = 20
    ) -> List[ChatMessage]:
        """Get recent conversation history respecting token limits"""
        messages = self.get_messages(chat_id, limit, order_desc=True)
        selected_messages = []
        total_tokens = 0

        # Start from most recent and work backwards
        for message in reversed(messages):
            message_tokens = self._estimate_token_count(message.content)
            if total_tokens + message_tokens <= max_tokens:
                selected_messages.insert(
                    0, message
                )  # Insert at beginning to maintain order
                total_tokens += message_tokens
            else:
                break

        return selected_messages

    def update_context_summary(self, chat_id: str, summary: str):
        """Update context summary for the chat"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE chat_sessions 
                SET context_summary = ? 
                WHERE chat_id = ?
            """,
                (summary, chat_id),
            )
            conn.commit()

    def clear_chat_messages(self, chat_id: str = None):
        """Clear chat messages for a specific chat or all chats"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if chat_id:
                cursor.execute(
                    "DELETE FROM chat_messages WHERE chat_id = ?", (chat_id,)
                )
                cursor.execute(
                    "UPDATE chat_sessions SET context_summary = '' WHERE chat_id = ?",
                    (chat_id,),
                )
            else:
                cursor.execute("DELETE FROM chat_messages")
                cursor.execute("UPDATE chat_sessions SET context_summary = ''")
            conn.commit()

    def _estimate_token_count(self, text: str) -> int:
        """Estimate token count for text (rough approximation: 1 token ≈ 4 characters)"""
        if not text:
            return 0
        return len(text) // 4

    def get_chat_statistics(self, chat_id: str) -> Dict[str, Any]:
        """Get statistics for a chat session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get message count
            cursor.execute(
                "SELECT COUNT(*) FROM chat_messages WHERE chat_id = ?", (chat_id,)
            )
            message_count = cursor.fetchone()[0]

            # Get total tokens
            cursor.execute(
                "SELECT SUM(token_count) FROM chat_messages WHERE chat_id = ?",
                (chat_id,),
            )
            total_tokens = cursor.fetchone()[0] or 0

            # Get session info
            cursor.execute(
                """
                SELECT created_at, last_activity FROM chat_sessions WHERE chat_id = ?
            """,
                (chat_id,),
            )
            session_info = cursor.fetchone()

            return {
                "message_count": message_count,
                "total_tokens": total_tokens,
                "created_at": session_info[0] if session_info else None,
                "last_activity": session_info[1] if session_info else None,
            }
