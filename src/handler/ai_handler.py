"""
AI Service Handler
Handles AI query service initialization and processing logic
"""

import logging
import os
from typing import Optional
from datetime import datetime

from .financial_handler import FinancialDataHandler
from .ai.ai_query_service import AIQueryService as ContextAwareAIQueryService
from ..models.financial_models import QueryResponse

logger = logging.getLogger(__name__)


class AIServiceHandler:
    """Handler class for AI service operations"""

    def __init__(
        self, llm_model: Optional[str] = None, llm_temperature: Optional[float] = None
    ):
        """
        Initialize AI Service Handler with Azure OpenAI

        Args:
            llm_model: Azure OpenAI model deployment name
            llm_temperature: LLM temperature setting
        """
        # Get configuration from environment variables or use defaults (Azure OpenAI only)
        self.llm_provider = "azure"  # Always use Azure OpenAI
        self.llm_model = llm_model or os.getenv("LLM_MODEL")
        self.llm_temperature = llm_temperature or float(
            os.getenv("LLM_TEMPERATURE", "0.4")
        )

        # Initialize financial service
        self.financial_service = FinancialDataHandler()

        # Lazy initialization of AI query service
        self._ai_query_service = None

    @property
    def ai_query_service(self) -> ContextAwareAIQueryService:
        """
        Get AI query service with lazy initialization

        Returns:
            Initialized AI query service

        Raises:
            Exception: If AI service initialization fails
        """
        if self._ai_query_service is None:
            try:
                logger.info(f"Initializing AI service with Azure OpenAI")
                self._ai_query_service = ContextAwareAIQueryService(
                    self.financial_service,
                    llm_model=self.llm_model,
                    llm_temperature=self.llm_temperature,
                )
                logger.info("AI service initialized successfully with Azure OpenAI")
            except Exception as e:
                logger.error(f"Failed to initialize AI service: {e}")
                raise Exception(
                    f"AI service unavailable: {str(e)}. Please check LLM configuration."
                )

        return self._ai_query_service

    def process_query(
        self,
        query: str,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None,
        use_v2: bool = False,
    ) -> QueryResponse:
        """
        Process a natural language query using AI

        Args:
            query: Natural language query string
            chat_id: Optional chat session ID for context-aware conversations
            user_id: Optional user ID for personalization
            use_v2: If True, use Two-API architecture (SQL generation + formatting)
                   If False, use standard single-API approach

        Returns:
            QueryResponse with answer, confidence, data points, and insights

        Raises:
            Exception: If query processing fails
        """
        try:
            logger.info(f"Processing query (v2={use_v2}): {query[:100]}...")
            start_time = datetime.now()

            # Route to appropriate processing method
            if use_v2:
                logger.info("Using Two-API architecture (v2)")
                response = self.ai_query_service.process_natural_language_query_v2(
                    query, chat_id=chat_id, user_id=user_id
                )
            else:
                logger.info("Using standard single-API architecture (v1)")
                response = self.ai_query_service.process_natural_language_query(
                    query, chat_id=chat_id, user_id=user_id
                )

            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Query processed successfully in {processing_time:.2f}s")

            return response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    def get_conversation_history(self, chat_id: str):
        """
        Get conversation history for a specific chat

        Args:
            chat_id: Chat session ID

        Returns:
            List of conversation history items
        """
        try:
            return self.ai_query_service.get_conversation_history(chat_id)
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise

    def clear_conversation_context(self, chat_id: Optional[str] = None):
        """
        Clear conversation context

        Args:
            chat_id: Optional chat session ID. If None, clears all contexts
        """
        try:
            self.ai_query_service.clear_conversation_context(chat_id)
            if chat_id:
                logger.info(f"Cleared conversation context for chat {chat_id}")
            else:
                logger.info("Cleared all conversation contexts")
        except Exception as e:
            logger.error(f"Error clearing conversation context: {e}")
            raise

    def get_llm_service_info(self):
        """
        Get LLM service information

        Returns:
            Dictionary with LLM service details
        """
        try:
            llm_service = self.ai_query_service.llm_service
            return {
                "llm_provider": self.llm_provider,
                "llm_model": self.llm_model,
                "llm_temperature": self.llm_temperature,
                "service_type": type(llm_service).__name__,
                "is_mock_service": hasattr(llm_service, "provider")
                and llm_service.provider == "mock",
                "service_provider": getattr(llm_service, "provider", "unknown"),
            }
        except Exception as e:
            logger.error(f"Error getting LLM service info: {e}")
            raise


# Global singleton instance
_ai_handler_instance = None


def get_ai_handler() -> AIServiceHandler:
    """
    Get global AI service handler instance (singleton pattern)

    Returns:
        AIServiceHandler instance
    """
    global _ai_handler_instance
    if _ai_handler_instance is None:
        _ai_handler_instance = AIServiceHandler()
    return _ai_handler_instance
