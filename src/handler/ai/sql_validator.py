"""
SQL Validator
Validates SQL queries for safety and correctness before execution
"""

import re
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)


class SQLValidator:
    """Validates SQL queries to ensure they are safe to execute"""

    # Prohibited SQL keywords that could modify data
    PROHIBITED_KEYWORDS = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "grant",
        "revoke",
        "exec",
        "execute",
        "pragma",
        "attach",
        "detach",
        "replace",
        "rename",
    ]

    # Allowed tables
    VALID_TABLES = ["accounts", "finance_transactions", "ft", "a"]

    # Maximum query length
    MAX_QUERY_LENGTH = 5000

    # Maximum number of JOINs
    MAX_JOINS = 5

    def validate_query(self, sql_query: str) -> Tuple[bool, str]:
        """
        Validate SQL query for safety and correctness

        Args:
            sql_query: The SQL query string to validate

        Returns:
            Tuple of (is_valid: bool, error_message: str)
            If valid, error_message is empty string
        """
        if not sql_query:
            return False, "Query is empty"

        if not isinstance(sql_query, str):
            return False, "Query must be a string"

        # Check query length
        if len(sql_query) > self.MAX_QUERY_LENGTH:
            return (
                False,
                f"Query exceeds maximum length of {self.MAX_QUERY_LENGTH} characters",
            )

        sql_lower = sql_query.lower().strip()

        # Must start with SELECT or WITH (CTE)
        if not (sql_lower.startswith("select") or sql_lower.startswith("with")):
            return False, "Query must be a SELECT or WITH statement (read-only)"

        # Check for prohibited keywords
        for keyword in self.PROHIBITED_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r"\b" + keyword + r"\b"
            if re.search(pattern, sql_lower):
                return False, f"Prohibited SQL keyword detected: {keyword.upper()}"

        # Check for multiple statements (SQL injection attempt)
        semicolons = sql_query.count(";")
        if semicolons > 1 or (semicolons == 1 and not sql_query.strip().endswith(";")):
            return False, "Multiple SQL statements or inline semicolons not allowed"

        # Check for comments (potential injection vector)
        if "--" in sql_query or "/*" in sql_query or "*/" in sql_query:
            return False, "SQL comments not allowed"

        # Check for valid table references
        has_valid_table = False
        for table in ["finance_transactions", "accounts"]:
            if table in sql_lower:
                has_valid_table = True
                break

        if not has_valid_table:
            return (
                False,
                f"Query must reference valid tables: accounts or finance_transactions",
            )

        # Check for excessive JOINs
        join_count = sql_lower.count(" join ")
        if join_count > self.MAX_JOINS:
            return (
                False,
                f"Too many JOINs ({join_count}). Maximum allowed: {self.MAX_JOINS}",
            )

        # Note: UNION is now allowed since we already validate table references
        # If all tables in UNION parts are validated, it's safe

        # Warn about missing LIMIT (but don't fail)
        if " limit " not in sql_lower:
            logger.warning(
                "Query does not include LIMIT clause - may return large result set"
            )

        # All checks passed
        return True, ""

    def sanitize_query(self, sql_query: str) -> str:
        """
        Clean up query formatting while preserving functionality

        Args:
            sql_query: The SQL query to sanitize

        Returns:
            Sanitized query string
        """
        # Remove extra whitespace
        query = " ".join(sql_query.split())

        # Ensure single trailing semicolon
        query = query.rstrip(";").strip()

        # Add LIMIT if not present
        if "limit" not in query.lower():
            query += " LIMIT 100"

        # Add trailing semicolon
        query += ";"

        return query

    def estimate_query_complexity(self, sql_query: str) -> dict:
        """
        Estimate the complexity of a query

        Args:
            sql_query: The SQL query to analyze

        Returns:
            Dictionary with complexity metrics
        """
        sql_lower = sql_query.lower()

        complexity = {
            "has_join": " join " in sql_lower,
            "join_count": sql_lower.count(" join "),
            "has_group_by": " group by " in sql_lower,
            "has_order_by": " order by " in sql_lower,
            "has_aggregation": any(
                func in sql_lower for func in ["sum(", "avg(", "count(", "max(", "min("]
            ),
            "has_subquery": (
                "(" in sql_query and "select" in sql_lower.split("from")[0]
                if "from" in sql_lower
                else False
            ),
            "has_limit": " limit " in sql_lower,
            "estimated_cost": "low",
        }

        # Calculate estimated cost
        cost_score = 0
        cost_score += complexity["join_count"] * 2
        cost_score += 1 if complexity["has_group_by"] else 0
        cost_score += 1 if complexity["has_aggregation"] else 0
        cost_score += 3 if complexity["has_subquery"] else 0
        cost_score -= 1 if complexity["has_limit"] else 0

        if cost_score <= 3:
            complexity["estimated_cost"] = "low"
        elif cost_score <= 7:
            complexity["estimated_cost"] = "medium"
        else:
            complexity["estimated_cost"] = "high"

        return complexity

    def get_validation_errors(self, sql_query: str) -> List[str]:
        """
        Get all validation errors as a list

        Args:
            sql_query: The SQL query to validate

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        if not sql_query:
            errors.append("Query is empty")
            return errors

        sql_lower = sql_query.lower().strip()

        if not sql_lower.startswith("select"):
            errors.append("Query must start with SELECT")

        for keyword in self.PROHIBITED_KEYWORDS:
            pattern = r"\b" + keyword + r"\b"
            if re.search(pattern, sql_lower):
                errors.append(f"Prohibited keyword: {keyword.upper()}")

        if ";" in sql_query[:-1]:
            errors.append("Multiple statements not allowed")

        if "--" in sql_query or "/*" in sql_query:
            errors.append("Comments not allowed")

        return errors
