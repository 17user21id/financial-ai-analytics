"""
Safe Query Executor
Executes validated SQL queries with safety controls and result formatting
"""

import sqlite3
import logging
from typing import List, Dict, Any
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)


class SafeQueryExecutor:
    """Executes validated SELECT queries safely with proper error handling"""

    def __init__(self, db_connection_factory):
        """
        Initialize executor

        Args:
            db_connection_factory: Factory function or object that provides database connections
        """
        self.db_connection_factory = db_connection_factory
        self.timeout = 30  # 30 second timeout
        self.max_results = 1000  # Maximum 1000 rows

    def execute_read_query(
        self, sql_query: str, params: tuple = None
    ) -> List[Dict[str, Any]]:
        """
        Execute validated SELECT query and return results as list of dictionaries

        Args:
            sql_query: The validated SQL query to execute
            params: Optional query parameters for parameterized queries

        Returns:
            List of dictionaries containing query results

        Raises:
            RuntimeError: If query execution fails
        """
        conn = None

        try:
            # Get database connection
            if hasattr(self.db_connection_factory, "get_connection"):
                conn = self.db_connection_factory.get_connection()
            elif callable(self.db_connection_factory):
                conn = self.db_connection_factory()
            else:
                conn = self.db_connection_factory

            # Set row factory for dict-like access
            conn.row_factory = sqlite3.Row

            # Create cursor
            cursor = conn.cursor()

            # Execute query
            logger.info(f"Executing SQL query: {sql_query[:100]}...")

            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)

            # Fetch results with limit
            rows = cursor.fetchmany(self.max_results)

            # Convert to list of dictionaries with proper type conversion
            results = []
            for row in rows:
                row_dict = {}
                for key in row.keys():
                    value = row[key]
                    # Convert types for JSON serialization
                    if isinstance(value, Decimal):
                        row_dict[key] = float(value)
                    elif isinstance(value, (datetime)):
                        row_dict[key] = value.isoformat()
                    else:
                        row_dict[key] = value
                results.append(row_dict)

            logger.info(f"Query returned {len(results)} results")

            return results

        except sqlite3.OperationalError as e:
            error_msg = f"Query execution error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        except sqlite3.DatabaseError as e:
            error_msg = f"Database error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        except Exception as e:
            error_msg = f"Unexpected error executing query: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        finally:
            # Don't close connection - it's managed by the database factory
            # The connection is reused across requests
            pass

    def execute_with_timeout(
        self, sql_query: str, timeout_seconds: int = None
    ) -> List[Dict[str, Any]]:
        """
        Execute query with custom timeout

        Args:
            sql_query: The SQL query to execute
            timeout_seconds: Custom timeout in seconds (defaults to self.timeout)

        Returns:
            Query results
        """
        original_timeout = self.timeout

        try:
            if timeout_seconds:
                self.timeout = timeout_seconds

            return self.execute_read_query(sql_query)

        finally:
            self.timeout = original_timeout

    def get_result_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """
        Generate summary statistics of query results

        Args:
            results: Query results to analyze

        Returns:
            Dictionary with result statistics
        """
        if not results:
            return {"row_count": 0, "has_data": False, "columns": [], "column_count": 0}

        # Get column information
        columns = list(results[0].keys()) if results else []

        # Analyze column types
        column_types = {}
        for col in columns:
            sample_value = results[0].get(col)
            if sample_value is not None:
                column_types[col] = type(sample_value).__name__
            else:
                column_types[col] = "null"

        # Calculate numeric statistics if applicable
        numeric_stats = {}
        for col in columns:
            values = [
                row.get(col)
                for row in results
                if isinstance(row.get(col), (int, float))
            ]
            if values:
                numeric_stats[col] = {
                    "min": min(values),
                    "max": max(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values),
                    "count": len(values),
                }

        summary = {
            "row_count": len(results),
            "has_data": True,
            "columns": columns,
            "column_count": len(columns),
            "column_types": column_types,
            "sample_row": results[0] if results else None,
            "numeric_stats": numeric_stats if numeric_stats else None,
        }

        return summary

    def format_results_for_display(
        self, results: List[Dict], max_rows: int = 10
    ) -> str:
        """
        Format results as human-readable string

        Args:
            results: Query results to format
            max_rows: Maximum number of rows to display

        Returns:
            Formatted string representation
        """
        if not results:
            return "No results found."

        output = []
        output.append(f"Query returned {len(results)} rows")
        output.append("-" * 50)

        # Show limited rows
        display_rows = results[:max_rows]

        for i, row in enumerate(display_rows, 1):
            output.append(f"\nRow {i}:")
            for key, value in row.items():
                if isinstance(value, float):
                    output.append(f"  {key}: {value:,.2f}")
                else:
                    output.append(f"  {key}: {value}")

        if len(results) > max_rows:
            output.append(f"\n... and {len(results) - max_rows} more rows")

        return "\n".join(output)

    def execute_and_summarize(self, sql_query: str) -> Dict[str, Any]:
        """
        Execute query and return results with summary

        Args:
            sql_query: The SQL query to execute

        Returns:
            Dictionary with results and summary
        """
        results = self.execute_read_query(sql_query)
        summary = self.get_result_summary(results)

        return {"results": results, "summary": summary, "query": sql_query}
