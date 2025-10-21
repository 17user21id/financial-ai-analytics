"""
AI Query Service with Context-Aware Conversations and Advanced Analytics
Implements intelligent query processing with database-backed conversation management
"""

import json
import logging
import traceback
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from ...models.financial_models import QueryResponse
from ...stores.chat_store import ChatStore, ChatMessage
from ...common.system_logger import system_logger
from .real_llm_service import FinancialLLMService

logger = logging.getLogger(__name__)


@dataclass
class ConversationContext:
    """Conversation context for maintaining chat history"""

    chat_id: str
    user_id: Optional[str] = None
    created_at: datetime = None
    last_activity: datetime = None
    context_summary: str = ""
    relevant_data_points: List[Dict] = None


class ConversationDatabase:
    """Database management for conversation context using ChatStore"""

    def __init__(self, db_path: str = "financial_data.db"):
        self.chat_store = ChatStore(db_path)

    def create_chat_session(
        self, chat_id: str, user_id: str = None
    ) -> ConversationContext:
        """Create a new chat session"""
        chat_session = self.chat_store.create_chat_session(chat_id, user_id)
        return ConversationContext(
            chat_id=chat_session.chat_id,
            user_id=chat_session.user_id,
            created_at=chat_session.created_at,
            last_activity=chat_session.last_activity,
        )

    def get_chat_session(self, chat_id: str) -> Optional[ConversationContext]:
        """Get existing chat session"""
        chat_session = self.chat_store.get_chat_session(chat_id)
        if chat_session:
            return ConversationContext(
                chat_id=chat_session.chat_id,
                user_id=chat_session.user_id,
                created_at=chat_session.created_at,
                last_activity=chat_session.last_activity,
                context_summary=chat_session.context_summary,
            )
        return None

    def add_message(
        self,
        chat_id: str,
        message_type: str,
        content: str,
        query_intent: str = None,
        data_points: List[Dict] = None,
        prompt: str = None,
        llm_response: str = None,
        summary: str = None,
        token_count: int = None,
    ):
        """Add a message to chat history with enhanced conversation tracking"""
        message = ChatMessage(
            chat_id=chat_id,
            message_type=message_type,
            content=content,
            query_intent=query_intent,
            data_points=data_points,
            prompt=prompt,
            llm_response=llm_response,
            summary=summary,
            token_count=token_count,
        )
        self.chat_store.add_message(message)

    def get_recent_messages(self, chat_id: str, limit: int = 10) -> List[Dict]:
        """Get recent messages for context with enhanced conversation data"""
        messages = self.chat_store.get_messages(chat_id, limit)
        return [
            {
                "type": msg.message_type,
                "content": msg.content,
                "query_intent": msg.query_intent,
                "data_points": msg.data_points or [],
                "prompt": msg.prompt,
                "llm_response": msg.llm_response,
                "summary": msg.summary,
                "token_count": msg.token_count,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
            }
            for msg in messages
        ]

    def update_context_summary(self, chat_id: str, summary: str):
        """Update context summary for the chat"""
        self.chat_store.update_context_summary(chat_id, summary)

    def estimate_token_count(self, text: str) -> int:
        """Estimate token count for text (rough approximation: 1 token ≈ 4 characters)"""
        return self.chat_store._estimate_token_count(text)

    def get_conversation_summaries(self, chat_id: str, limit: int = 5) -> List[str]:
        """Get recent conversation summaries for context"""
        return self.chat_store.get_conversation_summaries(chat_id, limit)

    def get_recent_history_with_token_limit(
        self, chat_id: str, max_tokens: int = 2000
    ) -> List[Dict]:
        """Get recent conversation history respecting token limits"""
        messages = self.chat_store.get_messages_with_token_limit(chat_id, max_tokens)
        return [
            {
                "type": msg.message_type,
                "content": msg.content,
                "query_intent": msg.query_intent,
                "data_points": msg.data_points or [],
                "prompt": msg.prompt,
                "llm_response": msg.llm_response,
                "summary": msg.summary,
                "token_count": msg.token_count,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
            }
            for msg in messages
        ]


class AIQueryService:
    """AI Query Service with context-aware conversations and advanced analytics"""

    def __init__(
        self,
        financial_service,
        llm_provider: str = "azure",
        llm_model: str = None,
        llm_temperature: float = 0.4,
        max_context_tokens: int = 4000,
    ):
        self.financial_service = financial_service
        self.max_context_tokens = max_context_tokens

        # Initialize conversation database
        self.conversation_db = ConversationDatabase()

        # Get singleton instance of LLM service (Azure OpenAI)
        try:
            self.llm_service = FinancialLLMService.get_instance(
                provider="azure", model_name=llm_model, temperature=llm_temperature
            )
            logger.info(f"Using Azure OpenAI LLM service (singleton)")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI service: {e}")
            logger.error(f"   Model: {llm_model or 'Default'}")
            logger.error("   No fallback available - AI queries will fail.")
            raise RuntimeError(f"Failed to initialize LLM service: {e}")

        # Initialize Two-API components
        from .database_schema_provider import DatabaseSchemaProvider
        from .sql_validator import SQLValidator
        from .safe_query_executor import SafeQueryExecutor
        from .query_generator import IntentAndQueryGenerator
        from .response_formatter import ResponseFormatter

        self.schema_provider = DatabaseSchemaProvider()
        self.sql_validator = SQLValidator()
        # Pass the database connection method
        self.query_executor = SafeQueryExecutor(financial_service.db._get_connection)
        self.query_generator = IntentAndQueryGenerator(
            self.llm_service, self.max_context_tokens
        )
        self.response_formatter = ResponseFormatter(
            self.llm_service, self.max_context_tokens
        )

        logger.info("AI Query Service initialized (with Two-API architecture support)")

    def get_conversation_history(self, chat_id: str) -> List[Dict]:
        """Get conversation history for a specific chat"""
        return self.conversation_db.get_recent_messages(chat_id, limit=20)

    def clear_conversation_context(self, chat_id: str = None):
        """Clear conversation context"""
        self.conversation_db.chat_store.clear_chat_messages(chat_id)
        logger.info(f"Conversation context cleared for chat_id: {chat_id or 'all'}")

    def process_natural_language_query(
        self, query: str, chat_id: str = None, user_id: str = None
    ) -> QueryResponse:
        """Process natural language query (v1 - legacy method)"""
        # For backward compatibility, redirect to v2
        return self.process_natural_language_query_v2(query, chat_id, user_id)

    def process_natural_language_query_v2(
        self, query: str, chat_id: str = None, user_id: str = None
    ) -> QueryResponse:
        """
        Process query using Two-API architecture

        Flow:
        1. First API Call: Generate SQL query from schema
        2. Validate SQL
        3. Execute query to get real data
        4. Second API Call: Format data into response
        5. Save to conversation history

        Args:
            query: Natural language query from user
            chat_id: Optional chat session ID
            user_id: Optional user ID

        Returns:
            QueryResponse with formatted answer and data
        """
        start_time = datetime.now()

        try:
            logger.info(f"Processing query with Two-API architecture: {query[:50]}...")

            # 1. Setup chat session
            chat_id = self._setup_chat_session(chat_id, user_id)

            # Get conversation history (get more, let query_generator manage token limits)
            conversation_history = self.conversation_db.get_conversation_summaries(
                chat_id, limit=20
            )

            # 2. FIRST API CALL: Generate SQL query
            separator = "=" * 70
            logger.info(f"{separator}\nFIRST API CALL: Query Generation\n{separator}")

            intent_result = self.query_generator.analyze_and_generate_query(
                user_query=query, conversation_history=conversation_history
            )

            logger.info(
                f"Intent: {intent_result.get('intent')}\n"
                f"Confidence: {intent_result.get('confidence')}\n"
                f"SQL: {intent_result.get('sql_query', 'None')}"
            )

            # 3. Check if modification attempt
            if intent_result.get("is_modification"):
                return QueryResponse(
                    query=query,
                    answer="I can only retrieve and analyze data, not modify it. Please rephrase your query as a question about the financial data.",
                    confidence=1.0,
                    data_points=[],
                    insights=["Data modification operations are not permitted"],
                    timestamp=datetime.now().isoformat(),
                    chat_id=chat_id,
                )

            # Get SQL query
            sql_query = intent_result.get("sql_query")

            if not sql_query or not intent_result.get("is_data_retrieval"):
                return QueryResponse(
                    query=query,
                    answer="I couldn't generate a database query for your request. Could you please rephrase your question or provide more details?",
                    confidence=0.5,
                    data_points=[],
                    insights=[],
                    timestamp=datetime.now().isoformat(),
                    chat_id=chat_id,
                )

            # 4. Validate SQL
            logger.info("Validating SQL query...")
            is_valid, error_msg = self.sql_validator.validate_query(sql_query)

            if not is_valid:
                logger.error(f"SQL validation failed: {error_msg}")
                return QueryResponse(
                    query=query,
                    answer=f"The generated query failed safety validation: {error_msg}. Please try rephrasing your question.",
                    confidence=0.5,
                    data_points=[],
                    insights=[],
                    timestamp=datetime.now().isoformat(),
                    chat_id=chat_id,
                )

            # Sanitize query (add LIMIT if missing)
            sql_query = self.sql_validator.sanitize_query(sql_query)
            logger.info(f"SQL validated and sanitized: {sql_query[:100]}...")

            # 5. Execute query
            logger.info("Executing SQL query...")
            try:
                query_results = self.query_executor.execute_read_query(sql_query)
                logger.info(
                    f"Query executed successfully: {len(query_results)} results"
                )
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                return QueryResponse(
                    query=query,
                    answer=self.response_formatter.format_error_response(str(e), query),
                    confidence=0.3,
                    data_points=[],
                    insights=[],
                    timestamp=datetime.now().isoformat(),
                    chat_id=chat_id,
                )

            # 6. SECOND API CALL: Format response (returns response + context summary)
            logger.info(
                f"{separator}\nSECOND API CALL: Response Formatting\n{separator}"
            )

            formatted_response, context_summary = (
                self.response_formatter.format_response(
                    user_query=query,
                    sql_query=sql_query,
                    query_results=query_results,
                    intent=intent_result.get("intent", "general"),
                    conversation_history=conversation_history,
                )
            )

            logger.info(f"Response formatted ({len(formatted_response)} chars)")
            logger.info(f"Context summary: {context_summary[:100]}...")

            # 7. Extract insights
            insights = self._extract_insights_from_results(
                query_results, intent_result.get("intent")
            )

            # 8. Save to conversation history with LLM-generated context summary
            token_count = self._estimate_and_store_tokens(query, formatted_response)
            self._store_conversation_messages(
                chat_id,
                query,
                formatted_response,
                intent_result,
                query_results[:5],
                token_count,
                formatted_response,
                context_summary,
            )

            # Update context summary
            self._update_context_summary(chat_id, intent_result, query)

            # 9. Create and return response
            response_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Two-API query completed in {response_time:.2f} seconds")

            response = self._create_query_response(
                query,
                formatted_response,
                intent_result,
                query_results[:10],
                insights,
                chat_id,
            )

            system_logger.log_api_request(
                method="TWO_API",
                endpoint="/api/ai/query/v2",
                status_code=200,
                response_time=response_time,
                extra={
                    "intent": intent_result.get("intent"),
                    "sql_query": sql_query[:100],
                    "result_count": len(query_results),
                    "confidence": intent_result.get("confidence"),
                },
            )

            return response

        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Error in Two-API query processing: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            system_logger.api_error(
                f"Two-API query error: {e}",
                {"query": query, "response_time": response_time, "error": str(e)},
            )

            return self._handle_query_error(query, e, chat_id, "two_api")

    def _setup_chat_session(self, chat_id: str = None, user_id: str = None) -> str:
        """Setup chat session and return chat_id"""
        if not chat_id:
            chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id or 'anonymous'}"

        chat_session = self.conversation_db.get_chat_session(chat_id)
        if not chat_session:
            chat_session = self.conversation_db.create_chat_session(chat_id, user_id)

        return chat_id

    def _store_conversation_messages(
        self,
        chat_id: str,
        query: str,
        response_text: str,
        intent_data: Dict,
        financial_data: List[Dict],
        token_count: int,
        llm_response: str = None,
        summary: str = None,
    ):
        """Store user and assistant messages in conversation history"""
        # Add user message to conversation history
        self.conversation_db.add_message(
            chat_id,
            "user",
            query,
            intent_data.get("intent", "general"),
            financial_data[:5],
            token_count=token_count,
        )

        # Add assistant message with final response data
        self.conversation_db.add_message(
            chat_id,
            "assistant",
            response_text,
            intent_data.get("intent", "general"),
            financial_data[:5],
            prompt=query,
            llm_response=llm_response,
            summary=summary,
            token_count=token_count,
        )

    def _update_context_summary(self, chat_id: str, intent_data: Dict, query: str):
        """Update context summary for the chat"""
        context_summary = (
            f"Last query: {intent_data.get('intent', 'general')} - {query[:50]}..."
        )
        self.conversation_db.update_context_summary(chat_id, context_summary)

    def _create_query_response(
        self,
        query: str,
        response_text: str,
        intent_data: Dict,
        financial_data: List[Dict],
        insights: List[str],
        chat_id: str,
    ) -> QueryResponse:
        """Create QueryResponse object"""
        return QueryResponse(
            query=query,
            answer=response_text,
            confidence=intent_data.get("confidence", 0.7),
            data_points=financial_data[:5],
            insights=insights,
            timestamp=datetime.now().isoformat(),
            chat_id=chat_id,
        )

    def _handle_query_error(
        self,
        query: str,
        error: Exception,
        chat_id: str = None,
        error_type: str = "general",
    ) -> QueryResponse:
        """Handle query processing errors"""
        logger.error(f"Error processing query: {error}")

        if error_type == "two_api":
            error_message = f"I encountered an error processing your query: {str(error)}. Please try rephrasing your question or contact support if the issue persists."
        else:
            error_message = (
                f"I encountered an error processing your query: {str(error)}"
            )

        return QueryResponse(
            query=query,
            answer=error_message,
            confidence=0.0,
            data_points=[],
            insights=[],
            timestamp=datetime.now().isoformat(),
            chat_id=chat_id,
        )

    def _estimate_and_store_tokens(self, query: str, response_text: str) -> int:
        """Estimate token count for query and response"""
        return self.conversation_db.estimate_token_count(query + response_text)

    def _extract_insights_from_results(
        self, results: List[Dict], intent: str
    ) -> List[str]:
        """Extract basic insights from query results"""
        insights = []

        if not results:
            insights.append("No data found for this query")
            return insights

        insights.append(f"Analyzed {len(results)} data records")

        # Check for numeric columns and calculate basic stats
        if results:
            numeric_cols = []
            for key, value in results[0].items():
                if isinstance(value, (int, float)) and key != "account_id":
                    numeric_cols.append(key)

            if numeric_cols:
                for col in numeric_cols:
                    values = [
                        r.get(col)
                        for r in results
                        if isinstance(r.get(col), (int, float))
                    ]
                    if values:
                        total = sum(values)
                        insights.append(f"Total {col.replace('_', ' ')}: ${total:,.2f}")

        return insights[:5]  # Limit to 5 insights
