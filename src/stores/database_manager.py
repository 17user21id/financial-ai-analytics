"""
Consolidated Database Manager
Provides singleton access to all database stores and consolidates database operations
"""

import sqlite3
import threading
import logging
import os
from typing import List, Dict, Any, Tuple
from enum import Enum

from ..config.settings import config_manager
from .database_schema import DatabaseSchema
from .account_store import (
    AccountStoreInterface,
    SQLiteAccountStore,
    InMemoryAccountStore,
)
from .transaction_store import (
    TransactionStoreInterface,
    SQLiteTransactionStore,
    InMemoryTransactionStore,
)
from .chat_store import ChatStore

logger = logging.getLogger(__name__)


class FilterOperator(Enum):
    """Filter operators for advanced queries"""

    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    BETWEEN = "BETWEEN"
    LIKE = "LIKE"
    IN = "IN"
    NOT_IN = "NOT IN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"


class FilterCondition:
    """Represents a filter condition for queries"""

    def __init__(self, field: str, operator: FilterOperator, value: Any = None):
        self.field = field
        self.operator = operator
        self.value = value

    def to_sql(self) -> Tuple[str, List[Any]]:
        """Convert filter condition to SQL WHERE clause"""
        if self.operator == FilterOperator.BETWEEN:
            if not isinstance(self.value, (list, tuple)) or len(self.value) != 2:
                raise ValueError("BETWEEN operator requires a list/tuple with 2 values")
            return f"{self.field} BETWEEN ? AND ?", list(self.value)
        elif self.operator == FilterOperator.IN:
            if not isinstance(self.value, (list, tuple)):
                raise ValueError("IN operator requires a list/tuple")
            placeholders = ",".join(["?" for _ in self.value])
            return f"{self.field} IN ({placeholders})", list(self.value)
        elif self.operator == FilterOperator.NOT_IN:
            if not isinstance(self.value, (list, tuple)):
                raise ValueError("NOT IN operator requires a list/tuple")
            placeholders = ",".join(["?" for _ in self.value])
            return f"{self.field} NOT IN ({placeholders})", list(self.value)
        elif self.operator in [FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL]:
            return f"{self.field} {self.operator.value}", []
        else:
            return f"{self.field} {self.operator.value} ?", [self.value]


class DatabaseManager:
    """
    Singleton database manager that consolidates all database operations
    Uses existing stores as singletons and provides unified interface
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.config = config_manager.config
        self._local = threading.local()

        # Check if we're in test mode
        self._is_test_mode = (
            os.getenv("ENVIRONMENT") == "TEST" or self.config.database.type == "memory"
        )

        # Initialize stores
        self._account_store = None
        self._transaction_store = None
        self._chat_store = None

        # Initialize database
        self._init_database()
        self._initialized = True

        logger.info(
            f"DatabaseManager singleton initialized (test_mode={self._is_test_mode})"
        )

    def _init_database(self):
        """Initialize database connection and schema"""
        if self._is_test_mode or self.config.database.type == "memory":
            logger.info("Initializing in-memory database for testing")
            self._db_path = ":memory:"
            self._is_memory = True
        else:
            logger.info(f"Initializing file database: {self.config.database.path}")
            self._db_path = self.config.database.path
            self._is_memory = False

        # Initialize schema
        connection = self._get_connection()
        cursor = connection.cursor()
        DatabaseSchema.initialize_schema(cursor, connection.commit)
        logger.info("Database schema initialized")

    def _get_connection(self):
        """Get thread-safe database connection"""
        if self._is_memory:
            # For in-memory, use a shared connection
            if not hasattr(self, "_shared_connection"):
                self._shared_connection = sqlite3.connect(":memory:")
                self._shared_connection.row_factory = sqlite3.Row
            return self._shared_connection
        else:
            # For file-based, use thread-local connections
            if not hasattr(self._local, "connection"):
                self._local.connection = sqlite3.connect(self._db_path)
                self._local.connection.row_factory = sqlite3.Row
            return self._local.connection

    @property
    def account_store(self) -> AccountStoreInterface:
        """Get account store singleton"""
        if self._account_store is None:
            connection_factory = self._get_connection
            if self._is_memory:
                self._account_store = InMemoryAccountStore(connection_factory)
            else:
                self._account_store = SQLiteAccountStore(connection_factory)
        return self._account_store

    @property
    def transaction_store(self) -> TransactionStoreInterface:
        """Get transaction store singleton"""
        if self._transaction_store is None:
            connection_factory = self._get_connection
            if self._is_memory:
                self._transaction_store = InMemoryTransactionStore(connection_factory)
            else:
                self._transaction_store = SQLiteTransactionStore(connection_factory)
        return self._transaction_store

    @property
    def chat_store(self) -> ChatStore:
        """Get chat store singleton"""
        if self._chat_store is None:
            self._chat_store = ChatStore(self._db_path)
        return self._chat_store

    # Legacy compatibility methods for existing code
    def query_metrics(
        self,
        filters: List[FilterCondition] = None,
        order_by: str = None,
        limit: int = None,
        offset: int = None,
    ) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        # Convert FilterCondition to dict format
        dict_filters = []
        if filters:
            for filter_condition in filters:
                dict_filters.append(
                    {
                        "field": filter_condition.field,
                        "operator": filter_condition.operator.value,
                        "value": filter_condition.value,
                    }
                )

        result = self.transaction_store.query_transactions(
            filters=dict_filters, order_by=order_by, limit=limit, offset=offset
        )
        return result.get("data", [])

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
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.query_transactions_aggregate(
            filters=filters,
            group_by=group_by,
            aggregates=aggregates,
            order_by=order_by,
            limit=limit,
            offset=offset,
            language=language,
        )

    def get_metrics_by_type(self, account_type: str, limit: int = 100) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.get_transactions_by_account_type(
            account_type, limit
        )

    def get_metrics_by_period(self, start_date: str, end_date: str) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.get_transactions_by_period(start_date, end_date)

    def get_financial_summary(
        self, period_start: str, period_end: str
    ) -> Dict[str, Any]:
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.get_financial_summary(period_start, period_end)

    def get_metrics_summary(
        self, group_by: str, filters: List[FilterCondition] = None
    ) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        # Convert FilterCondition to dict format
        dict_filters = []
        if filters:
            for filter_condition in filters:
                dict_filters.append(
                    {
                        "field": filter_condition.field,
                        "operator": filter_condition.operator.value,
                        "value": filter_condition.value,
                    }
                )

        return self.transaction_store.get_metrics_summary(group_by, dict_filters)

    def store_metrics(self, metrics: List[Dict[str, Any]]) -> None:
        """Legacy method - delegates to transaction store"""
        for metric in metrics:
            self.transaction_store.create_transaction(metric)

    def search_metrics(self, search_term: str) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.search_transactions(search_term)

    def get_available_periods(self) -> List[Dict]:
        """Legacy method - delegates to transaction store"""
        return self.transaction_store.get_available_periods()

    def clear_data(self) -> None:
        """Legacy method - clears all data"""
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM finance_transactions")
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM chat_sessions")
        cursor.execute("DELETE FROM chat_messages")
        connection.commit()
        logger.info("Cleared all data from database")

    def get_accounts_count(self) -> int:
        """Get total number of accounts"""
        return self.account_store.get_accounts_count()

    def get_transactions_count(self) -> int:
        """Get total number of transactions"""
        return self.transaction_store.get_transactions_count()

    def reset_for_testing(self):
        """Reset the database manager for testing (clears all data)"""
        if not self._is_test_mode:
            logger.warning("reset_for_testing called in non-test mode")

        # Clear all data
        self.clear_data()

        # Reset store instances to force re-initialization
        self._account_store = None
        self._transaction_store = None
        self._chat_store = None

        logger.info("Database manager reset for testing")


# Global singleton instance
_database_manager = None
_manager_lock = threading.Lock()


def get_database_manager() -> DatabaseManager:
    """Get the global database manager singleton"""
    global _database_manager
    if _database_manager is None:
        with _manager_lock:
            if _database_manager is None:
                _database_manager = DatabaseManager()
    return _database_manager


# Convenience functions for backward compatibility
def get_database():
    """Legacy function - returns database manager"""
    return get_database_manager()


def get_account_store() -> AccountStoreInterface:
    """Get account store instance"""
    return get_database_manager().account_store


def get_transaction_store() -> TransactionStoreInterface:
    """Get transaction store instance"""
    return get_database_manager().transaction_store


def get_chat_store() -> ChatStore:
    """Get chat store instance"""
    return get_database_manager().chat_store


def reset_database_manager():
    """Reset the global database manager singleton (for testing)"""
    global _database_manager
    with _manager_lock:
        if _database_manager is not None:
            _database_manager.reset_for_testing()
        _database_manager = None
