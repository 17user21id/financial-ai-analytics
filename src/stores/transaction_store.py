"""
Transaction Store
Handles all transaction-related database operations
"""

import sqlite3
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class TransactionStoreInterface(ABC):
    """Abstract interface for transaction store operations"""

    @abstractmethod
    def create_transaction(self, transaction_data: Dict[str, Any]) -> int:
        """Create a new transaction and return tx_id"""
        pass

    @abstractmethod
    def get_transaction_by_id(self, tx_id: int) -> Optional[Dict[str, Any]]:
        """Get transaction by ID"""
        pass

    @abstractmethod
    def query_transactions(
        self,
        filters: List[Dict[str, Any]] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Query transactions with advanced filtering"""
        pass

    @abstractmethod
    def query_transactions_aggregate(
        self,
        filters: List[Dict[str, Any]] = None,
        group_by: List[str] = None,
        aggregates: List[Dict[str, Any]] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Query transactions with aggregation and grouping"""
        pass

    @abstractmethod
    def get_transactions_by_account(
        self, account_id: int, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get transactions for a specific account"""
        pass

    @abstractmethod
    def get_transactions_by_period(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """Get transactions for a specific period"""
        pass

    @abstractmethod
    def update_transaction(self, tx_id: int, transaction_data: Dict[str, Any]) -> bool:
        """Update transaction"""
        pass

    @abstractmethod
    def delete_transaction(self, tx_id: int) -> bool:
        """Delete transaction"""
        pass

    @abstractmethod
    def get_transactions_count(self) -> int:
        """Get total count of transactions"""
        pass

    @abstractmethod
    def get_transactions_sum(
        self, filters: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get sum of transaction values with optional filters"""
        pass

    @abstractmethod
    def clear_all_transactions(self) -> int:
        """Clear all transactions from the database"""
        pass


class SQLiteTransactionStore(TransactionStoreInterface):
    """SQLite implementation of transaction store"""

    def __init__(self, connection_factory):
        """
        Initialize with a connection factory function

        Args:
            connection_factory: Function that returns a database connection
        """
        self.get_connection = connection_factory
        logger.info("Initialized SQLiteTransactionStore")

    def create_transaction(self, transaction_data: Dict[str, Any]) -> int:
        """Create a new transaction and return tx_id"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO finance_transactions 
                (account_id, period_start, period_end, value, currency, 
                 derived_sub_type, created_by, notes, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    transaction_data.get("account_id"),
                    transaction_data.get("period_start"),
                    transaction_data.get("period_end"),
                    transaction_data.get("value"),
                    transaction_data.get("currency", 1),
                    transaction_data.get("derived_sub_type"),
                    transaction_data.get("created_by"),
                    transaction_data.get("notes"),
                    transaction_data.get("source_id", 1),
                ),
            )

            tx_id = cursor.lastrowid
            connection.commit()
            logger.info(f"Created transaction with ID: {tx_id}")
            return tx_id

        except Exception as e:
            connection.rollback()
            logger.error(f"Error creating transaction: {e}")
            raise

    def get_transaction_by_id(self, tx_id: int) -> Optional[Dict[str, Any]]:
        """Get transaction by ID"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 
                ft.tx_id, ft.account_id, ft.period_start, ft.period_end,
                ft.value, ft.currency, ft.derived_sub_type, ft.posted_date,
                ft.created_by, ft.notes, ft.source_id,
                a.name as account_name, a.type as account_type,
                a.sub_type, a.is_derived, a.description
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
            WHERE ft.tx_id = ?
        """,
            (tx_id,),
        )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def query_transactions(
        self,
        filters: List[Dict[str, Any]] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Query transactions with advanced filtering"""
        connection = self.get_connection()
        cursor = connection.cursor()

        # Build base query
        query = """
            SELECT 
                ft.tx_id, ft.account_id,
                a.name as account_name, a.type as account_type,
                a.sub_type, a.is_derived, a.description,
                ft.period_start, ft.period_end, ft.value, ft.currency,
                ft.derived_sub_type, ft.posted_date, ft.created_by,
                ft.notes, ft.source_id
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
        """

        # Add WHERE conditions
        params = []
        if filters:
            where_conditions = []
            for filter_item in filters:
                field = filter_item.get("field")
                operator = filter_item.get("operator", "=")
                value = filter_item.get("value")

                if field and value is not None:
                    condition_sql, condition_params = self._build_filter_condition(
                        field, operator, value
                    )
                    where_conditions.append(condition_sql)
                    params.extend(condition_params)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

        # Add ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"
        else:
            query += " ORDER BY ft.posted_date DESC, ft.value DESC"

        # Add LIMIT and OFFSET
        if limit:
            query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"

        cursor.execute(query, params)

        # Process results
        results = []
        for row in cursor.fetchall():
            result_dict = {
                "tx_id": row["tx_id"],
                "account_id": row["account_id"],
                "account_name": row["account_name"],
                "account_type": row["account_type"],
                "sub_type": row["sub_type"],
                "is_derived": bool(row["is_derived"]),
                "description": row["description"],
                "period_start": row["period_start"],
                "period_end": row["period_end"],
                "value": float(row["value"]),
                "currency": row["currency"],
                "derived_sub_type": row["derived_sub_type"],
                "posted_date": row["posted_date"],
                "created_by": row["created_by"],
                "notes": row["notes"],
                "source_id": row["source_id"],
            }

            # Apply localization if requested
            if language != "en":
                result_dict = self._localize_result(result_dict, language)

            results.append(result_dict)

        # Get total count for pagination
        count_query = """
            SELECT COUNT(*)
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
        """

        if filters:
            where_conditions = []
            count_params = []
            for filter_item in filters:
                field = filter_item.get("field")
                operator = filter_item.get("operator", "=")
                value = filter_item.get("value")

                if field and value is not None:
                    condition_sql, condition_params = self._build_filter_condition(
                        field, operator, value
                    )
                    where_conditions.append(condition_sql)
                    count_params.extend(condition_params)

            if where_conditions:
                count_query += " WHERE " + " AND ".join(where_conditions)

        cursor.execute(count_query, count_params if filters else [])
        total_count = cursor.fetchone()[0]

        return {
            "data": results,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": (offset or 0) + len(results) < total_count,
        }

    def _build_filter_condition(
        self, field: str, operator: str, value: Any
    ) -> Tuple[str, List[Any]]:
        """Build SQL condition for filter"""
        # Map field names to actual database columns
        field_mapping = {
            "account_id": "ft.account_id",
            "account_name": "a.name",
            "account_type": "a.type",
            "sub_type": "a.sub_type",
            "is_derived": "a.is_derived",
            "period_start": "ft.period_start",
            "period_end": "ft.period_end",
            "value": "ft.value",
            "currency": "ft.currency",
            "derived_sub_type": "ft.derived_sub_type",
            "source_id": "ft.source_id",
            "posted_date": "ft.posted_date",
            "created_by": "ft.created_by",
        }

        db_field = field_mapping.get(field, field)

        if operator == "=":
            return f"{db_field} = ?", [value]
        elif operator == "!=":
            return f"{db_field} != ?", [value]
        elif operator == ">":
            return f"{db_field} > ?", [value]
        elif operator == ">=":
            return f"{db_field} >= ?", [value]
        elif operator == "<":
            return f"{db_field} < ?", [value]
        elif operator == "<=":
            return f"{db_field} <= ?", [value]
        elif operator == "BETWEEN":
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return f"{db_field} BETWEEN ? AND ?", list(value)
            else:
                raise ValueError("BETWEEN operator requires a list/tuple with 2 values")
        elif operator == "LIKE" or operator == "ILIKE":
            return f"{db_field} LIKE ?", [f"%{value}%"]
        elif operator == "IN":
            if isinstance(value, (list, tuple)):
                placeholders = ",".join(["?" for _ in value])
                return f"{db_field} IN ({placeholders})", list(value)
            else:
                raise ValueError("IN operator requires a list/tuple")
        elif operator == "NOT IN":
            if isinstance(value, (list, tuple)):
                placeholders = ",".join(["?" for _ in value])
                return f"{db_field} NOT IN ({placeholders})", list(value)
            else:
                raise ValueError("NOT IN operator requires a list/tuple")
        elif operator == "IS NULL":
            return f"{db_field} IS NULL", []
        elif operator == "IS NOT NULL":
            return f"{db_field} IS NOT NULL", []
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _localize_result(
        self, result_dict: Dict[str, Any], language: str
    ) -> Dict[str, Any]:
        """Apply localization to result dictionary"""
        from ..common.localization import localization_manager, Language

        # Map language string to enum
        lang_mapping = {"en": Language.ENGLISH, "ar": Language.ARABIC}

        lang_enum = lang_mapping.get(language.lower(), Language.ENGLISH)

        # Localize enum fields
        if "account_type" in result_dict:
            result_dict["account_type_localized"] = localization_manager.localize_enum(
                "account_type", result_dict["account_type"], lang_enum
            )

        if "currency" in result_dict:
            result_dict["currency_localized"] = localization_manager.localize_enum(
                "currency", result_dict["currency"], lang_enum
            )

        if "source_id" in result_dict:
            result_dict["source_id_localized"] = localization_manager.localize_enum(
                "data_source", result_dict["source_id"], lang_enum
            )

        return result_dict

    def query_transactions_aggregate(
        self,
        filters: List[Dict[str, Any]] = None,
        group_by: List[str] = None,
        aggregates: List[Dict[str, Any]] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Query transactions with aggregation and grouping"""
        connection = self.get_connection()
        cursor = connection.cursor()

        # Default aggregates if none specified
        if not aggregates:
            aggregates = [{"function": "SUM", "field": "value", "alias": "total_sum"}]

        # Build SELECT clause with GROUP BY fields and aggregates
        select_fields = []

        # Add GROUP BY fields to SELECT
        if group_by:
            for field in group_by:
                field_mapping = {
                    "account_type": "a.type",
                    "account_name": "a.name",
                    "currency": "ft.currency",
                    "source_id": "ft.source_id",
                    "sub_type": "a.sub_type",
                    "is_derived": "a.is_derived",
                    "period_start": "ft.period_start",
                    "period_end": "ft.period_end",
                    "posted_date": "ft.posted_date",
                    "created_by": "ft.created_by",
                }
                db_field = field_mapping.get(field, field)
                select_fields.append(f"{db_field} as {field}")

        # Add aggregate functions to SELECT
        for agg in aggregates:
            function = agg.get("function", "SUM").upper()
            field = agg.get("field", "value")
            alias = agg.get("alias", f"{function.lower()}_{field}")

            field_mapping = {
                "value": "ft.value",
                "tx_id": "ft.tx_id",
                "account_id": "ft.account_id",
            }
            db_field = field_mapping.get(field, field)

            select_fields.append(f"{function}({db_field}) as {alias}")

        # Build base query
        query = f"""
            SELECT {', '.join(select_fields)}
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
        """

        # Add WHERE conditions
        params = []
        if filters:
            where_conditions = []
            for filter_item in filters:
                field = filter_item.get("field")
                operator = filter_item.get("operator", "=")
                value = filter_item.get("value")

                if field and value is not None:
                    condition_sql, condition_params = self._build_filter_condition(
                        field, operator, value
                    )
                    where_conditions.append(condition_sql)
                    params.extend(condition_params)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

        # Add GROUP BY clause
        if group_by:
            group_fields = []
            for field in group_by:
                field_mapping = {
                    "account_type": "a.type",
                    "account_name": "a.name",
                    "currency": "ft.currency",
                    "source_id": "ft.source_id",
                    "sub_type": "a.sub_type",
                    "is_derived": "a.is_derived",
                    "period_start": "ft.period_start",
                    "period_end": "ft.period_end",
                    "posted_date": "ft.posted_date",
                    "created_by": "ft.created_by",
                }
                db_field = field_mapping.get(field, field)
                group_fields.append(db_field)
            query += " GROUP BY " + ", ".join(group_fields)

        # Add ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"

        # Add LIMIT and OFFSET
        if limit:
            query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"

        # Execute query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Convert results to list of dictionaries
        groups = []
        for row in results:
            group_dict = dict(row)
            groups.append(group_dict)

        # Get total count for pagination
        count_query = (
            query.split("ORDER BY")[0]
            if "ORDER BY" in query
            else query.split("LIMIT")[0] if "LIMIT" in query else query
        )
        count_query = f"SELECT COUNT(*) FROM ({count_query}) as count_subquery"
        cursor.execute(count_query, params)
        total_groups = cursor.fetchone()[0]

        return {
            "groups": groups,
            "total_groups": total_groups,
            "limit": limit,
            "offset": offset,
            "has_more": (offset or 0) + len(groups) < total_groups,
            "group_by_fields": group_by or [],
            "aggregate_functions": [agg.get("function", "SUM") for agg in aggregates],
            "query_executed": query,
            "params_used": params,
        }

    def get_transactions_by_account(
        self, account_id: int, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get transactions for a specific account"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 
                ft.tx_id, ft.account_id,
                a.name as account_name, a.type as account_type,
                ft.period_start, ft.period_end, ft.value, ft.currency,
                ft.posted_date, ft.source_id
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
            WHERE ft.account_id = ?
            ORDER BY ft.posted_date DESC
            LIMIT ?
        """,
            (account_id, limit),
        )

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def get_transactions_by_period(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """Get transactions for a specific period"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 
                ft.tx_id, ft.account_id,
                a.name as account_name, a.type as account_type,
                ft.period_start, ft.period_end, ft.value, ft.currency,
                ft.posted_date, ft.source_id
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
            WHERE ft.period_start >= ? AND ft.period_end <= ?
            ORDER BY ft.period_start DESC, ft.value DESC
        """,
            (start_date, end_date),
        )

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def update_transaction(self, tx_id: int, transaction_data: Dict[str, Any]) -> bool:
        """Update transaction"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # Build dynamic update query
            update_fields = []
            params = []

            for field in [
                "account_id",
                "period_start",
                "period_end",
                "value",
                "currency",
                "derived_sub_type",
                "created_by",
                "notes",
                "source_id",
            ]:
                if field in transaction_data:
                    update_fields.append(f"{field} = ?")
                    params.append(transaction_data[field])

            if not update_fields:
                logger.warning("No fields to update")
                return False

            params.append(tx_id)

            query = f"UPDATE finance_transactions SET {', '.join(update_fields)} WHERE tx_id = ?"
            cursor.execute(query, params)

            connection.commit()
            updated = cursor.rowcount > 0

            if updated:
                logger.info(f"Updated transaction with ID: {tx_id}")
            else:
                logger.warning(f"No transaction found with ID: {tx_id}")

            return updated

        except Exception as e:
            connection.rollback()
            logger.error(f"Error updating transaction: {e}")
            raise

    def delete_transaction(self, tx_id: int) -> bool:
        """Delete transaction"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM finance_transactions WHERE tx_id = ?", (tx_id,))
            connection.commit()
            deleted = cursor.rowcount > 0

            if deleted:
                logger.info(f"Deleted transaction with ID: {tx_id}")
            else:
                logger.warning(f"No transaction found with ID: {tx_id}")

            return deleted

        except Exception as e:
            connection.rollback()
            logger.error(f"Error deleting transaction: {e}")
            raise

    def get_transactions_count(self) -> int:
        """Get total count of transactions"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM finance_transactions")
        count = cursor.fetchone()[0]

        return count

    def get_transactions_sum(
        self, filters: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get sum of transaction values with optional filters"""
        connection = self.get_connection()
        cursor = connection.cursor()

        # Build base query for sum
        query = """
            SELECT SUM(ft.value) as total_sum, COUNT(*) as count
            FROM finance_transactions ft
            JOIN accounts a ON ft.account_id = a.account_id
        """

        # Add WHERE conditions
        params = []
        if filters:
            where_conditions = []
            for filter_item in filters:
                field = filter_item.get("field")
                operator = filter_item.get("operator", "=")
                value = filter_item.get("value")

                if field and value is not None:
                    condition_sql, condition_params = self._build_filter_condition(
                        field, operator, value
                    )
                    where_conditions.append(condition_sql)
                    params.extend(condition_params)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

        cursor.execute(query, params)
        result = cursor.fetchone()

        total_sum = float(result[0]) if result[0] is not None else 0.0
        count = result[1] if result[1] is not None else 0

        return {
            "total_sum": total_sum,
            "count": count,
            "filters_applied": filters or [],
            "query_executed": query,
            "params_used": params,
        }

    def clear_all_transactions(self) -> int:
        """Clear all transactions from the database"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM finance_transactions")
            deleted_count = cursor.rowcount
            connection.commit()
            logger.info(f"Cleared {deleted_count} transactions from database")
            return deleted_count

        except Exception as e:
            connection.rollback()
            logger.error(f"Error clearing transactions: {e}")
            raise


class InMemoryTransactionStore(SQLiteTransactionStore):
    """In-memory implementation of transaction store (inherits from SQLiteTransactionStore)"""

    def __init__(self, connection_factory):
        super().__init__(connection_factory)
        logger.info("Initialized InMemoryTransactionStore")
