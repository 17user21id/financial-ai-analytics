"""
Test suite for Database Manager functionality.

This module tests the DatabaseManager implementation to ensure proper
initialization, store creation, and environment-specific behavior using
in-memory SQLite database for testing.
"""

import os
import sys
import unittest

# Add project root directory to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

# Set environment to TEST for in-memory SQLite database
os.environ["ENVIRONMENT"] = "TEST"

from src.stores.database_manager import (
    DatabaseManager,
    get_database_manager,
    get_account_store,
    get_transaction_store,
    get_chat_store,
    reset_database_manager,
)
from src.stores.account_store import AccountStoreInterface
from src.stores.transaction_store import TransactionStoreInterface
from src.stores.chat_store import ChatStore


class TestDatabaseManager(unittest.TestCase):
    """
    Test case for Database Manager operations.

    This test verifies the manager functionality including:
    - Proper initialization for different environments
    - Correct store instance creation
    - Environment-specific database type selection
    - Manager reset and cleanup
    - Connection management
    """

    def setUp(self):
        """
        Set up test environment.

        Ensures clean state before each test by resetting the manager.
        """
        # Reset manager to ensure clean state
        reset_database_manager()

    def tearDown(self):
        """
        Clean up after test execution.

        Resets the database manager to ensure clean state for next test.
        """
        reset_database_manager()

    def test_manager_reset(self):
        """Test manager reset functionality."""
        # Get manager instance
        manager = get_database_manager()
        self.assertIsInstance(manager, DatabaseManager)

        # Reset manager
        reset_database_manager()

        # Get new instance (should be fresh)
        new_manager = get_database_manager()
        self.assertIsInstance(new_manager, DatabaseManager)

    def test_singleton_behavior(self):
        """Test that manager is a singleton."""
        manager1 = get_database_manager()
        manager2 = get_database_manager()

        # Should be the same instance
        self.assertIs(manager1, manager2)

    def test_store_creation(self):
        """Test store instance creation."""
        # Get store instances
        account_store = get_account_store()
        transaction_store = get_transaction_store()
        chat_store = get_chat_store()

        # Verify store types
        self.assertIsInstance(account_store, AccountStoreInterface)
        self.assertIsInstance(transaction_store, TransactionStoreInterface)
        self.assertIsInstance(chat_store, ChatStore)

    def test_in_memory_database(self):
        """Test that TEST environment uses in-memory database."""
        manager = get_database_manager()

        # In TEST environment, should use in-memory database
        self.assertTrue(manager._is_memory)
        self.assertEqual(manager._db_path, ":memory:")

    def test_store_singleton_behavior(self):
        """Test that stores are singletons within manager."""
        manager = get_database_manager()

        # Get stores multiple times
        account_store1 = manager.account_store
        account_store2 = manager.account_store

        transaction_store1 = manager.transaction_store
        transaction_store2 = manager.transaction_store

        # Should be the same instances
        self.assertIs(account_store1, account_store2)
        self.assertIs(transaction_store1, transaction_store2)

    def test_legacy_compatibility_methods(self):
        """Test legacy compatibility methods."""
        manager = get_database_manager()

        # Test legacy methods exist and work
        self.assertIsNotNone(manager.query_metrics)
        self.assertIsNotNone(manager.query_transactions_aggregate)
        self.assertIsNotNone(manager.get_metrics_by_type)
        self.assertIsNotNone(manager.get_metrics_by_period)
        self.assertIsNotNone(manager.get_financial_summary)
        self.assertIsNotNone(manager.store_metrics)
        self.assertIsNotNone(manager.search_metrics)
        self.assertIsNotNone(manager.get_available_periods)
        self.assertIsNotNone(manager.clear_data)

    def test_connection_management(self):
        """Test database connection management."""
        manager = get_database_manager()

        # Get connection
        connection = manager._get_connection()

        # Should be a valid SQLite connection
        self.assertIsNotNone(connection)
        self.assertEqual(connection.__class__.__name__, "Connection")

    def test_accounts_count(self):
        """Test getting accounts count."""
        manager = get_database_manager()

        # Should return 0 for empty database
        count = manager.get_accounts_count()
        self.assertEqual(count, 0)

    def test_transactions_count(self):
        """Test getting transactions count."""
        manager = get_database_manager()

        # Should return 0 for empty database
        count = manager.get_transactions_count()
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
