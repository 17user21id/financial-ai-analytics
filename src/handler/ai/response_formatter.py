"""
Response Formatter - Second API Call
Formats query results into human-readable responses
"""

import json
import logging
from typing import Dict, List, Any
from .token_manager import TokenManager
from .enum_mappings import EnumMappings
from .llm_templates import RESPONSE_FORMATTING_PROMPT

logger = logging.getLogger(__name__)


class ResponseFormatter:
    """Second LLM call: Format query results into professional response"""

    def __init__(self, llm_service, max_context_tokens: int = 4000):
        """
        Initialize formatter

        Args:
            llm_service: LLM service instance for response formatting
            max_context_tokens: Maximum tokens for context window (default 4000)
        """
        self.llm_service = llm_service
        self.token_manager = TokenManager(max_context_tokens)

    def format_response(
        self,
        user_query: str,
        sql_query: str,
        query_results: List[Dict[str, Any]],
        intent: str,
        conversation_history: List[str] = None,
    ) -> tuple:
        """
        Second API call to LLM: Format data into human-readable response

        Args:
            user_query: Original user question
            sql_query: SQL query that was executed
            query_results: Actual data from database
            intent: Detected intent (revenue, profit, etc.)
            conversation_history: Recent conversation context

        Returns:
            Tuple of (formatted_response, context_summary)
        """
        try:
            logger.info(
                f"[SECOND API CALL] Formatting response for {len(query_results)} results..."
            )

            # Format conversation history
            history_context = self._format_history(conversation_history or [])

            # Format query results for prompt
            results_json = self._format_results_for_prompt(query_results)

            # Create formatting prompt
            prompt = self._create_formatting_prompt(
                user_query, sql_query, results_json, intent, history_context
            )

            # Call LLM
            logger.info("Calling LLM for response formatting...")
            llm_response = self.llm_service.get_response(
                prompt=prompt,
                context="You are a senior financial analyst presenting data insights to stakeholders.",
            )

            full_response = llm_response.answer.strip()

            # Extract context summary from response
            formatted_response, context_summary = self._extract_context_summary(
                full_response, user_query, intent
            )

            logger.info(
                f"OK Response formatted successfully ({len(formatted_response)} chars)"
            )
            logger.info(f"OK Context summary extracted: {context_summary[:80]}...")

            return formatted_response, context_summary

        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            # Return fallback response
            fallback = self._create_fallback_response(user_query, query_results, intent)
            fallback_summary = f'User asked: "{user_query[:60]}..." | Intent: {intent}'
            return fallback, fallback_summary

    def _create_formatting_prompt(
        self,
        user_query: str,
        sql_query: str,
        results_json: str,
        intent: str,
        history_context: str,
    ) -> str:
        """Create prompt for response formatting using the template"""
        # Get enum mappings for human-readable conversion
        enum_reference = EnumMappings.format_enum_reference_for_llm()

        return RESPONSE_FORMATTING_PROMPT.format(
            user_query=user_query,
            sql_query=sql_query,
            results_json=results_json,
            intent=intent,
            history_context=history_context,
            enum_reference=enum_reference,
        )

    def _format_results_for_prompt(self, query_results: List[Dict[str, Any]]) -> str:
        """
        Format query results for inclusion in prompt

        Args:
            query_results: Raw query results

        Returns:
            Formatted JSON string
        """
        if not query_results:
            return "No results found (empty result set)"

        # Limit results in prompt to prevent token overflow
        max_results = 50
        limited_results = query_results[:max_results]

        # Add truncation note if needed
        result_note = ""
        if len(query_results) > max_results:
            result_note = f"\n\nNote: Showing first {max_results} of {len(query_results)} total results"

        try:
            json_str = json.dumps(limited_results, indent=2, default=str)
            return json_str + result_note
        except Exception as e:
            logger.error(f"Error formatting results as JSON: {e}")
            return f"Error formatting results: {str(e)}"

    def _create_fallback_response(
        self, user_query: str, query_results: List[Dict[str, Any]], intent: str
    ) -> str:
        """
        Create fallback response when LLM formatting fails

        Args:
            user_query: Original user query
            query_results: Query results
            intent: Detected intent

        Returns:
            Basic formatted response
        """
        if not query_results:
            return f"I couldn't find any data matching your query about {intent}. The database query returned no results. Please try rephrasing your question or specifying a different time period."

        # Build basic response
        response_parts = []

        # Add header
        response_parts.append(
            f"Based on the available financial data, here are the results for your query about {intent}:"
        )
        response_parts.append("")

        # Add result summary
        if len(query_results) == 1:
            # Single result - likely an aggregation
            result = query_results[0]
            for key, value in result.items():
                if isinstance(value, (int, float)):
                    response_parts.append(
                        f"**{key.replace('_', ' ').title()}**: ${value:,.2f}"
                    )
                else:
                    response_parts.append(
                        f"**{key.replace('_', ' ').title()}**: {value}"
                    )
        else:
            # Multiple results
            response_parts.append(f"Found {len(query_results)} records:")
            response_parts.append("")

            # Show first few results
            for i, result in enumerate(query_results[:5], 1):
                response_parts.append(
                    f"{i}. "
                    + ", ".join(
                        [
                            (
                                f"{k}: {v:,.2f}"
                                if isinstance(v, (int, float))
                                else f"{k}: {v}"
                            )
                            for k, v in result.items()
                        ]
                    )
                )

            if len(query_results) > 5:
                response_parts.append(f"... and {len(query_results) - 5} more results")

        response_parts.append("")
        response_parts.append(
            "For more detailed analysis or to explore specific aspects of this data, please let me know!"
        )

        return "\n".join(response_parts)

    def _extract_context_summary(
        self, full_response: str, user_query: str, intent: str
    ) -> tuple:
        """
        Extract context summary from LLM response

        Args:
            full_response: Full LLM response with summary marker
            user_query: Original user query (for fallback)
            intent: Query intent (for fallback)

        Returns:
            Tuple of (formatted_response, context_summary)
        """
        # Look for the summary marker
        marker = "---CONTEXT_SUMMARY---"

        if marker in full_response:
            # Split response and summary
            parts = full_response.split(marker, 1)
            formatted_response = parts[0].strip()
            context_summary = parts[1].strip() if len(parts) > 1 else ""

            # If summary is empty or too short, create fallback
            if not context_summary or len(context_summary) < 20:
                context_summary = (
                    f'User asked: "{user_query[:60]}..." | Intent: {intent}'
                )

            return formatted_response, context_summary
        else:
            # No marker found - LLM didn't follow instructions
            # Use full response and create basic summary
            logger.warning("Context summary marker not found in LLM response")
            context_summary = f'User asked: "{user_query[:60]}..." | Intent: {intent}'
            return full_response, context_summary

    def _format_history(self, history: List[str]) -> str:
        """Format conversation history for prompt with token management"""
        # Reserve tokens for query, results, and prompt template
        reserved_tokens = 2500
        return self.token_manager.format_history_with_limit(
            history=history,
            reserved_tokens=reserved_tokens,
            empty_message="No previous conversation",
        )

    def format_error_response(self, error_message: str, user_query: str) -> str:
        """
        Format error message in user-friendly way

        Args:
            error_message: Technical error message
            user_query: Original user query

        Returns:
            User-friendly error response
        """
        response = (
            f'I encountered an issue while processing your question: "{user_query}"\n\n'
        )

        if "timeout" in error_message.lower():
            response += "The query took too long to execute. Please try:\n"
            response += "- Narrowing down the time period\n"
            response += "- Focusing on specific accounts or categories\n"
            response += "- Breaking down your question into smaller parts"

        elif "no such column" in error_message.lower():
            response += "The query referenced a column that doesn't exist in the database. Please rephrase your question using standard financial terms like 'revenue', 'expenses', 'profit', or 'account'."

        elif "syntax error" in error_message.lower():
            response += "There was a problem generating the database query. Please try rephrasing your question in simpler terms."

        else:
            response += f"Technical details: {error_message}\n\n"
            response += "Please try rephrasing your question or ask about a different aspect of the financial data."

        return response
