"""
Query Generator - First API Call
Analyzes user intent and generates SQL query using database schema
"""

import json
import logging
from typing import Dict, Any, List, Optional
from .database_schema_provider import DatabaseSchemaProvider
from .token_manager import TokenManager
from .llm_templates import SQL_GENERATION_PROMPT

logger = logging.getLogger(__name__)


class IntentAndQueryGenerator:
    """First LLM call: Analyze intent and generate SQL query from schema"""

    def __init__(self, llm_service, max_context_tokens: int = 4000):
        """
        Initialize generator

        Args:
            llm_service: LLM service instance for query generation
            max_context_tokens: Maximum tokens for context window (default 4000)
        """
        self.llm_service = llm_service
        self.schema_provider = DatabaseSchemaProvider()
        self.token_manager = TokenManager(max_context_tokens)

    def analyze_and_generate_query(
        self, user_query: str, conversation_history: List[str] = None
    ) -> Dict[str, Any]:
        """
        First API call to LLM: Analyze intent and generate SQL

        Args:
            user_query: The natural language query from user
            conversation_history: List of recent conversation summaries

        Returns:
            Dictionary with:
            - intent: str (revenue, profit, expense, trend, comparison, summary)
            - is_data_retrieval: bool
            - is_modification: bool
            - sql_query: str or None
            - reasoning: str
            - confidence: float
        """
        try:
            logger.info(
                f"[FIRST API CALL] Generating SQL for query: {user_query[:50]}..."
            )

            # Get database schema
            schema = self.schema_provider.get_schema_json()

            # Format conversation history
            history_context = self._format_history(conversation_history or [])

            # Create prompt for SQL generation
            prompt = self._create_sql_generation_prompt(
                user_query, schema, history_context
            )

            # Call LLM
            logger.info("Calling LLM for SQL generation...")
            llm_response = self.llm_service.get_response(
                prompt=prompt,
                context="You are an expert SQL query generator for financial databases.",
            )

            logger.info(f"OK LLM Response received: {llm_response.answer[:200]}...")

            # Parse LLM response
            result = self._parse_llm_response(llm_response.answer, user_query)

            logger.info(f"OK Intent detected: {result.get('intent')}")
            logger.info(f"OK SQL generated: {result.get('sql_query', 'None')[:100]}...")

            return result

        except Exception as e:
            logger.error(f"Error in query generation: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Full error: {str(e)}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "intent": "general",
                "is_data_retrieval": False,
                "is_modification": False,
                "sql_query": None,
                "reasoning": f"Failed to generate query: {str(e)}",
                "confidence": 0.0,
            }

    def _create_sql_generation_prompt(
        self, user_query: str, schema: str, history_context: str
    ) -> str:
        """Create the prompt for SQL generation using the template"""
        return SQL_GENERATION_PROMPT.format(
            schema=schema, history_context=history_context, user_query=user_query
        )

    def _parse_llm_response(self, llm_answer: str, user_query: str) -> Dict[str, Any]:
        """
        Parse LLM response and extract structured data

        Args:
            llm_answer: Raw LLM response
            user_query: Original user query

        Returns:
            Parsed result dictionary
        """
        try:
            # Try to extract JSON from response
            # Remove markdown code blocks if present
            answer = llm_answer.strip()
            if answer.startswith("```"):
                # Extract content between code blocks
                lines = answer.split("\n")
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block or (not line.startswith("```") and json_lines):
                        json_lines.append(line)
                answer = "\n".join(json_lines)

            # Parse JSON
            result = json.loads(answer)

            # Validate required fields
            required_fields = [
                "intent",
                "is_data_retrieval",
                "is_modification",
                "sql_query",
                "reasoning",
                "confidence",
            ]
            for field in required_fields:
                if field not in result:
                    result[field] = self._get_default_value(field)

            # Clean up SQL query
            if result.get("sql_query"):
                result["sql_query"] = result["sql_query"].strip()
                # Ensure it ends with semicolon
                if not result["sql_query"].endswith(";"):
                    result["sql_query"] += ";"

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"LLM Response: {llm_answer}")

            # Attempt fallback parsing
            return self._fallback_parse(llm_answer, user_query)

    def _fallback_parse(self, llm_answer: str, user_query: str) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails"""

        # Simple heuristic-based intent detection
        query_lower = user_query.lower()

        if any(word in query_lower for word in ["revenue", "income", "sales"]):
            intent = "revenue"
        elif any(word in query_lower for word in ["profit", "margin", "profitability"]):
            intent = "profit"
        elif any(word in query_lower for word in ["expense", "cost", "spending"]):
            intent = "expense"
        elif any(
            word in query_lower for word in ["trend", "growth", "over time", "pattern"]
        ):
            intent = "trend"
        elif any(
            word in query_lower for word in ["compare", "comparison", "versus", "vs"]
        ):
            intent = "comparison"
        else:
            intent = "summary"

        return {
            "intent": intent,
            "is_data_retrieval": True,
            "is_modification": False,
            "sql_query": None,
            "reasoning": "Fallback parsing due to LLM response format error",
            "confidence": 0.5,
        }

    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing fields"""
        defaults = {
            "intent": "general",
            "is_data_retrieval": False,
            "is_modification": False,
            "sql_query": None,
            "reasoning": "No reasoning provided",
            "confidence": 0.5,
        }
        return defaults.get(field)

    def _format_history(self, history: List[str]) -> str:
        """Format conversation history for prompt with token management"""
        # Reserve tokens for query, schema, and prompt template
        reserved_tokens = 2000
        return self.token_manager.format_history_with_limit(
            history=history,
            reserved_tokens=reserved_tokens,
            empty_message="No previous conversation",
        )
