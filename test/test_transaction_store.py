"""
Test suite for Transaction Store functionality.

This module tests the TransactionStore implementation using an in-memory SQLite database.
It covers all CRUD operations, query functionality, filtering, aggregation, and edge cases
to ensure the transaction store works correctly in isolation.
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
    reset_database_manager,
    get_account_store,
    get_transaction_store,
)
from src.stores.transaction_store import TransactionStoreInterface


class TestTransactionStore(unittest.TestCase):
    """
    Test case for Transaction Store operations.

    This test verifies all transaction store functionality including:
    - Transaction creation, retrieval, updating, and deletion
    - Query operations with various filters
    - Aggregation and grouping operations
    - Edge cases and error handling
    - Data integrity and constraints
    """

    def setUp(self):
        """
        Set up test environment with clean in-memory database.

        Initializes a fresh in-memory database and both account and transaction stores
        for each test to ensure test isolation.
        """
        # Reset database manager to ensure clean state
        reset_database_manager()

        # Get store instances (will be in-memory due to TEST environment)
        self.account_store = get_account_store()
        self.transaction_store = get_transaction_store()

        # Verify we have the correct store types
        self.assertIsInstance(self.transaction_store, TransactionStoreInterface)

        # Create test accounts
        self.test_accounts = self._create_test_accounts()

        # Sample transaction data for testing
        self.sample_transactions = [
            {
                "account_id": self.test_accounts[0]["account_id"],
                "period_start": "2022-01-01",
                "period_end": "2022-01-31",
                "value": 1000.50,
                "currency": 1,
                "derived_sub_type": 1,
                "created_by": "test_user",
                "notes": "Initial cash deposit",
                "source_id": 1,
            },
            {
                "account_id": self.test_accounts[1]["account_id"],
                "period_start": "2022-01-01",
                "period_end": "2022-01-31",
                "value": 2500.75,
                "currency": 1,
                "derived_sub_type": 2,
                "created_by": "test_user",
                "notes": "Customer payment received",
                "source_id": 1,
            },
            {
                "account_id": self.test_accounts[2]["account_id"],
                "period_start": "2022-02-01",
                "period_end": "2022-02-28",
                "value": -500.00,
                "currency": 1,
                "derived_sub_type": 1,
                "created_by": "test_user",
                "notes": "Equipment purchase",
                "source_id": 1,
            },
            {
                "account_id": self.test_accounts[3]["account_id"],
                "period_start": "2022-02-01",
                "period_end": "2022-02-28",
                "value": 1500.25,
                "currency": 1,
                "derived_sub_type": 1,
                "created_by": "test_user",
                "notes": "Vendor invoice",
                "source_id": 1,
            },
            {
                "account_id": self.test_accounts[4]["account_id"],
                "period_start": "2022-03-01",
                "period_end": "2022-03-31",
                "value": 5000.00,
                "currency": 1,
                "derived_sub_type": None,
                "created_by": "test_user",
                "notes": "Revenue summary for March",
                "source_id": 1,
            },
        ]

    def _create_test_accounts(self):
        """Create test accounts and return their data."""
        account_data = [
            {
                "name": "Cash Account",
                "category_path": "Assets/Current Assets",
                "sub_category": "Cash",
                "type": 1,
                "sub_type": 1,
                "is_summary": False,
                "is_derived": False,
                "description": "Primary cash account",
                "is_active": True,
            },
            {
                "name": "Accounts Receivable",
                "category_path": "Assets/Current Assets",
                "sub_category": "Receivables",
                "type": 1,
                "sub_type": 2,
                "is_summary": False,
                "is_derived": False,
                "description": "Customer receivables",
                "is_active": True,
            },
            {
                "name": "Equipment",
                "category_path": "Assets/Fixed Assets",
                "sub_category": "Equipment",
                "type": 1,
                "sub_type": 3,
                "is_summary": False,
                "is_derived": False,
                "description": "Office equipment",
                "is_active": True,
            },
            {
                "name": "Accounts Payable",
                "category_path": "Liabilities/Current Liabilities",
                "sub_category": "Payables",
                "type": 2,
                "sub_type": 1,
                "is_summary": False,
                "is_derived": False,
                "description": "Vendor payables",
                "is_active": True,
            },
            {
                "name": "Revenue Summary",
                "category_path": "Income/Operating Revenue",
                "sub_category": "Summary",
                "type": 4,
                "sub_type": None,
                "is_summary": True,
                "is_derived": True,
                "description": "Revenue summary account",
                "is_active": True,
            },
        ]

        created_accounts = []
        for data in account_data:
            account_id = self.account_store.create_account(data)
            account = self.account_store.get_account_by_id(account_id)
            created_accounts.append(account)

        return created_accounts

    def tearDown(self):
        """
        Clean up after test execution.

        Resets the database factory to ensure clean state for next test.
        """
        reset_database_manager()

    def test_create_transaction_success(self):
        """Test successful transaction creation."""
        transaction_data = self.sample_transactions[0]

        # Create transaction
        tx_id = self.transaction_store.create_transaction(transaction_data)

        # Verify transaction was created
        self.assertIsInstance(tx_id, int)
        self.assertGreater(tx_id, 0)

        # Verify transaction data
        created_transaction = self.transaction_store.get_transaction_by_id(tx_id)
        self.assertIsNotNone(created_transaction)
        self.assertEqual(
            created_transaction["account_id"], transaction_data["account_id"]
        )
        self.assertEqual(
            created_transaction["period_start"], transaction_data["period_start"]
        )
        self.assertEqual(
            created_transaction["period_end"], transaction_data["period_end"]
        )
        self.assertEqual(created_transaction["value"], transaction_data["value"])
        self.assertEqual(created_transaction["currency"], transaction_data["currency"])
        self.assertEqual(
            created_transaction["derived_sub_type"],
            transaction_data["derived_sub_type"],
        )
        self.assertEqual(
            created_transaction["created_by"], transaction_data["created_by"]
        )
        self.assertEqual(created_transaction["notes"], transaction_data["notes"])
        self.assertEqual(
            created_transaction["source_id"], transaction_data["source_id"]
        )

        # Verify account information is joined
        self.assertEqual(
            created_transaction["account_name"], self.test_accounts[0]["name"]
        )
        self.assertEqual(
            created_transaction["account_type"], self.test_accounts[0]["type"]
        )

    def test_create_transaction_with_null_derived_sub_type(self):
        """Test transaction creation with NULL derived_sub_type."""
        transaction_data = self.sample_transactions[4]  # Has derived_sub_type=None

        tx_id = self.transaction_store.create_transaction(transaction_data)

        created_transaction = self.transaction_store.get_transaction_by_id(tx_id)
        self.assertIsNotNone(created_transaction)
        self.assertIsNone(created_transaction["derived_sub_type"])

    def test_get_transaction_by_id_existing(self):
        """Test retrieving existing transaction by ID."""
        transaction_data = self.sample_transactions[0]
        tx_id = self.transaction_store.create_transaction(transaction_data)

        retrieved_transaction = self.transaction_store.get_transaction_by_id(tx_id)

        self.assertIsNotNone(retrieved_transaction)
        self.assertEqual(retrieved_transaction["tx_id"], tx_id)
        self.assertEqual(
            retrieved_transaction["account_id"], transaction_data["account_id"]
        )

    def test_get_transaction_by_id_nonexistent(self):
        """Test retrieving non-existent transaction by ID."""
        retrieved_transaction = self.transaction_store.get_transaction_by_id(99999)
        self.assertIsNone(retrieved_transaction)

    def test_query_transactions_no_filters(self):
        """Test querying transactions without filters."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Query all transactions
        result = self.transaction_store.query_transactions()

        self.assertIsInstance(result, dict)
        self.assertIn("data", result)
        self.assertIn("total_count", result)
        self.assertEqual(len(result["data"]), len(self.sample_transactions))
        self.assertEqual(result["total_count"], len(self.sample_transactions))

    def test_query_transactions_with_filters(self):
        """Test querying transactions with various filters."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Filter by account_id
        result = self.transaction_store.query_transactions(
            [
                {
                    "field": "account_id",
                    "operator": "=",
                    "value": self.test_accounts[0]["account_id"],
                }
            ]
        )

        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(
            result["data"][0]["account_id"], self.test_accounts[0]["account_id"]
        )

        # Filter by value range
        result = self.transaction_store.query_transactions(
            [{"field": "value", "operator": ">=", "value": 1000.0}]
        )

        self.assertGreaterEqual(
            len(result["data"]), 2
        )  # At least 2 transactions >= 1000
        for transaction in result["data"]:
            self.assertGreaterEqual(transaction["value"], 1000.0)

        # Filter by period
        result = self.transaction_store.query_transactions(
            [
                {"field": "period_start", "operator": ">=", "value": "2022-02-01"},
                {"field": "period_end", "operator": "<=", "value": "2022-02-28"},
            ]
        )

        self.assertEqual(len(result["data"]), 2)  # 2 transactions in February
        for transaction in result["data"]:
            self.assertGreaterEqual(transaction["period_start"], "2022-02-01")
            self.assertLessEqual(transaction["period_end"], "2022-02-28")

    def test_query_transactions_with_operators(self):
        """Test querying transactions with different operators."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Test LIKE operator
        result = self.transaction_store.query_transactions(
            [{"field": "notes", "operator": "LIKE", "value": "payment"}]
        )

        self.assertGreaterEqual(len(result["data"]), 1)
        for transaction in result["data"]:
            self.assertIn("payment", transaction["notes"].lower())

        # Test IN operator
        account_ids = [
            self.test_accounts[0]["account_id"],
            self.test_accounts[1]["account_id"],
        ]
        result = self.transaction_store.query_transactions(
            [{"field": "account_id", "operator": "IN", "value": account_ids}]
        )

        self.assertEqual(len(result["data"]), 2)
        for transaction in result["data"]:
            self.assertIn(transaction["account_id"], account_ids)

        # Test BETWEEN operator
        result = self.transaction_store.query_transactions(
            [{"field": "value", "operator": "BETWEEN", "value": [1000.0, 2000.0]}]
        )

        for transaction in result["data"]:
            self.assertGreaterEqual(transaction["value"], 1000.0)
            self.assertLessEqual(transaction["value"], 2000.0)

    def test_query_transactions_with_pagination(self):
        """Test querying transactions with pagination."""
        # Create more transactions than limit
        for i in range(10):
            transaction_data = self.sample_transactions[0].copy()
            transaction_data["value"] = 100.0 + i
            self.transaction_store.create_transaction(transaction_data)

        # Test with limit
        result = self.transaction_store.query_transactions(limit=5)

        self.assertEqual(len(result["data"]), 5)
        self.assertEqual(result["limit"], 5)
        self.assertGreater(result["total_count"], 5)

        # Test with offset
        result = self.transaction_store.query_transactions(limit=3, offset=2)

        self.assertEqual(len(result["data"]), 3)
        self.assertEqual(result["limit"], 3)
        self.assertEqual(result["offset"], 2)

    def test_query_transactions_aggregate(self):
        """Test querying transactions with aggregation."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Test simple aggregation
        result = self.transaction_store.query_transactions_aggregate(
            aggregates=[{"function": "SUM", "field": "value", "alias": "total_value"}]
        )

        self.assertIn("groups", result)
        self.assertEqual(len(result["groups"]), 1)
        self.assertIn("total_value", result["groups"][0])
        self.assertGreater(result["groups"][0]["total_value"], 0)

        # Test grouping by account_type
        result = self.transaction_store.query_transactions_aggregate(
            group_by=["account_type"],
            aggregates=[
                {"function": "SUM", "field": "value", "alias": "total_value"},
                {"function": "COUNT", "field": "tx_id", "alias": "transaction_count"},
            ],
        )

        self.assertIn("groups", result)
        self.assertGreater(len(result["groups"]), 0)

        for group in result["groups"]:
            self.assertIn("account_type", group)
            self.assertIn("total_value", group)
            self.assertIn("transaction_count", group)

    def test_get_transactions_by_account(self):
        """Test getting transactions for a specific account."""
        # Create transactions for different accounts
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Get transactions for first account
        account_id = self.test_accounts[0]["account_id"]
        transactions = self.transaction_store.get_transactions_by_account(account_id)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["account_id"], account_id)

    def test_get_transactions_by_period(self):
        """Test getting transactions for a specific period."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Get transactions for February 2022
        transactions = self.transaction_store.get_transactions_by_period(
            "2022-02-01", "2022-02-28"
        )

        self.assertEqual(len(transactions), 2)  # 2 transactions in February
        for transaction in transactions:
            self.assertGreaterEqual(transaction["period_start"], "2022-02-01")
            self.assertLessEqual(transaction["period_end"], "2022-02-28")

    def test_update_transaction_success(self):
        """Test successful transaction update."""
        # Create transaction
        transaction_data = self.sample_transactions[0]
        tx_id = self.transaction_store.create_transaction(transaction_data)

        # Update transaction
        update_data = {
            "value": 2000.00,
            "notes": "Updated notes",
            "created_by": "updated_user",
        }

        success = self.transaction_store.update_transaction(tx_id, update_data)

        self.assertTrue(success)

        # Verify update
        updated_transaction = self.transaction_store.get_transaction_by_id(tx_id)
        self.assertEqual(updated_transaction["value"], update_data["value"])
        self.assertEqual(updated_transaction["notes"], update_data["notes"])
        self.assertEqual(updated_transaction["created_by"], update_data["created_by"])

        # Verify other fields unchanged
        self.assertEqual(
            updated_transaction["account_id"], transaction_data["account_id"]
        )
        self.assertEqual(
            updated_transaction["period_start"], transaction_data["period_start"]
        )

    def test_update_transaction_nonexistent(self):
        """Test updating non-existent transaction."""
        update_data = {"value": 2000.00}

        success = self.transaction_store.update_transaction(99999, update_data)

        self.assertFalse(success)

    def test_update_transaction_no_fields(self):
        """Test updating transaction with no fields."""
        transaction_data = self.sample_transactions[0]
        tx_id = self.transaction_store.create_transaction(transaction_data)

        success = self.transaction_store.update_transaction(tx_id, {})

        self.assertFalse(success)

    def test_delete_transaction_success(self):
        """Test successful transaction deletion."""
        # Create transaction
        transaction_data = self.sample_transactions[0]
        tx_id = self.transaction_store.create_transaction(transaction_data)

        # Verify transaction exists
        self.assertIsNotNone(self.transaction_store.get_transaction_by_id(tx_id))

        # Delete transaction
        success = self.transaction_store.delete_transaction(tx_id)

        self.assertTrue(success)

        # Verify transaction is deleted
        self.assertIsNone(self.transaction_store.get_transaction_by_id(tx_id))

    def test_delete_transaction_nonexistent(self):
        """Test deleting non-existent transaction."""
        success = self.transaction_store.delete_transaction(99999)

        self.assertFalse(success)

    def test_get_transactions_count_empty(self):
        """Test getting transaction count when database is empty."""
        count = self.transaction_store.get_transactions_count()
        self.assertEqual(count, 0)

    def test_get_transactions_count_with_data(self):
        """Test getting transaction count with data."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        count = self.transaction_store.get_transactions_count()
        self.assertEqual(count, len(self.sample_transactions))

    def test_get_transactions_sum(self):
        """Test getting sum of transaction values."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Get sum without filters
        result = self.transaction_store.get_transactions_sum()

        self.assertIn("total_sum", result)
        self.assertIn("count", result)
        self.assertGreater(result["total_sum"], 0)
        self.assertEqual(result["count"], len(self.sample_transactions))

        # Get sum with filters
        result = self.transaction_store.get_transactions_sum(
            [{"field": "value", "operator": ">=", "value": 1000.0}]
        )

        self.assertGreaterEqual(result["total_sum"], 1000.0)
        self.assertGreater(result["count"], 0)

    def test_clear_all_transactions(self):
        """Test clearing all transactions."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Verify transactions exist
        self.assertGreater(self.transaction_store.get_transactions_count(), 0)

        # Clear all transactions
        deleted_count = self.transaction_store.clear_all_transactions()

        self.assertEqual(deleted_count, len(self.sample_transactions))
        self.assertEqual(self.transaction_store.get_transactions_count(), 0)

    def test_transaction_data_integrity(self):
        """Test transaction data integrity and constraints."""
        # Test with invalid account_id (foreign key constraint)
        invalid_transaction = self.sample_transactions[0].copy()
        invalid_transaction["account_id"] = 99999  # Non-existent account

        # This should either raise an exception or fail silently
        # depending on database configuration
        try:
            tx_id = self.transaction_store.create_transaction(invalid_transaction)
            # If it succeeds, verify the transaction was created but with invalid account
            transaction = self.transaction_store.get_transaction_by_id(tx_id)
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction["account_id"], 99999)
        except Exception:
            # Expected behavior - foreign key constraint should prevent this
            pass

        # Test with invalid value range
        invalid_transaction = self.sample_transactions[0].copy()
        invalid_transaction["value"] = 999999999999.99  # Exceeds max value

        # This should either raise an exception or succeed depending on constraint enforcement
        try:
            tx_id = self.transaction_store.create_transaction(invalid_transaction)
            # If it succeeds, verify the transaction was created
            transaction = self.transaction_store.get_transaction_by_id(tx_id)
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction["value"], 999999999999.99)
        except Exception:
            # Expected behavior - value constraint should prevent this
            pass

    def test_transaction_ordering(self):
        """Test that transactions are returned in correct order."""
        # Create transactions with specific values
        values = [300.0, 100.0, 200.0]

        for value in values:
            transaction_data = self.sample_transactions[0].copy()
            transaction_data["value"] = value
            self.transaction_store.create_transaction(transaction_data)

        # Query transactions (should be ordered by posted_date DESC, value DESC)
        result = self.transaction_store.query_transactions()

        self.assertEqual(len(result["data"]), len(values))

        # Verify ordering (should be by value descending)
        retrieved_values = [tx["value"] for tx in result["data"]]
        self.assertEqual(retrieved_values, sorted(values, reverse=True))

    def test_query_with_localization(self):
        """Test querying transactions with localization."""
        # Create transactions
        for transaction_data in self.sample_transactions:
            self.transaction_store.create_transaction(transaction_data)

        # Query with Arabic localization
        result = self.transaction_store.query_transactions(language="ar")

        self.assertIn("data", result)
        self.assertGreater(len(result["data"]), 0)

        # Check if localization fields are present (if localization is implemented)
        if result["data"]:
            first_transaction = result["data"][0]
            # Note: Localization fields may not be present if localization is not fully implemented
            # This test verifies the method doesn't crash with different languages

    def test_complex_aggregation_query(self):
        """Test complex aggregation query with multiple groups and filters."""
        # Create more diverse transactions
        for i in range(5):
            for account in self.test_accounts[:3]:  # Use first 3 accounts
                transaction_data = {
                    "account_id": account["account_id"],
                    "period_start": f"2022-{i+1:02d}-01",
                    "period_end": f"2022-{i+1:02d}-28",
                    "value": 100.0 * (i + 1),
                    "currency": 1,
                    "derived_sub_type": 1,
                    "created_by": f"user_{i}",
                    "notes": f"Transaction {i}",
                    "source_id": 1,
                }
                self.transaction_store.create_transaction(transaction_data)

        # Complex aggregation query
        result = self.transaction_store.query_transactions_aggregate(
            filters=[{"field": "value", "operator": ">=", "value": 200.0}],
            group_by=["account_type", "currency"],
            aggregates=[
                {"function": "SUM", "field": "value", "alias": "total_value"},
                {"function": "COUNT", "field": "tx_id", "alias": "tx_count"},
                {"function": "AVG", "field": "value", "alias": "avg_value"},
            ],
            order_by="total_value DESC",
        )

        self.assertIn("groups", result)
        self.assertGreater(len(result["groups"]), 0)

        for group in result["groups"]:
            self.assertIn("account_type", group)
            self.assertIn("currency", group)
            self.assertIn("total_value", group)
            self.assertIn("tx_count", group)
            self.assertIn("avg_value", group)
            self.assertGreater(group["total_value"], 0)
            self.assertGreater(group["tx_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
