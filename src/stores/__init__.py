"""
Database Stores Package
Provides access to all database stores and consolidated database operations
"""

# Main consolidated database manager
from .database_manager import (
    DatabaseManager,
    FilterOperator,
    FilterCondition,
    get_database_manager,
    get_database,
    get_account_store,
    get_transaction_store,
    get_chat_store,
    reset_database_manager,
)

# Individual store interfaces (for direct access if needed)
from .account_store import AccountStoreInterface
from .transaction_store import TransactionStoreInterface
from .chat_store import ChatStore

# Database schema
from .database_schema import DatabaseSchema

__all__ = [
    # Main consolidated manager
    "DatabaseManager",
    "FilterOperator",
    "FilterCondition",
    "get_database_manager",
    "get_database",
    "get_account_store",
    "get_transaction_store",
    "get_chat_store",
    "reset_database_manager",
    # Individual stores
    "AccountStoreInterface",
    "TransactionStoreInterface",
    "ChatStore",
    # Schema
    "DatabaseSchema",
]
