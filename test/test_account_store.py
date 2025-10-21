"""
Test suite for Account Store functionality.

This module tests the AccountStore implementation using an in-memory SQLite database.
It covers all CRUD operations, search functionality, filtering, and edge cases
to ensure the account store works correctly in isolation.
"""

import os
import sys
import unittest

# Add project root directory to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

# Set environment to TEST for in-memory SQLite database
os.environ["ENVIRONMENT"] = "TEST"

from src.stores.database_manager import reset_database_manager, get_account_store
from src.stores.account_store import AccountStoreInterface


class TestAccountStore(unittest.TestCase):
    """
    Test case for Account Store operations.

    This test verifies all account store functionality including:
    - Account creation, retrieval, updating, and deletion
    - Search and filtering operations
    - Edge cases and error handling
    - Data integrity and constraints
    """

    def setUp(self):
        """
        Set up test environment with clean in-memory database.

        Initializes a fresh in-memory database and account store
        for each test to ensure test isolation.
        """
        # Reset database manager to ensure clean state
        reset_database_manager()

        # Get account store instance (will be in-memory due to TEST environment)
        self.account_store = get_account_store()

        # Verify we have the correct store type
        self.assertIsInstance(self.account_store, AccountStoreInterface)

        # Sample account data for testing
        self.sample_accounts = [
            {
                "name": "Cash Account",
                "category_path": "Assets/Current Assets",
                "sub_category": "Cash",
                "type": 1,  # Asset
                "sub_type": 1,  # Current Asset
                "is_summary": False,
                "is_derived": False,
                "description": "Primary cash account for daily operations",
                "is_active": True,
            },
            {
                "name": "Accounts Receivable",
                "category_path": "Assets/Current Assets",
                "sub_category": "Receivables",
                "type": 1,  # Asset
                "sub_type": 2,  # Accounts Receivable
                "is_summary": False,
                "is_derived": False,
                "description": "Outstanding customer invoices",
                "is_active": True,
            },
            {
                "name": "Equipment",
                "category_path": "Assets/Fixed Assets",
                "sub_category": "Equipment",
                "type": 1,  # Asset
                "sub_type": 3,  # Fixed Asset
                "is_summary": False,
                "is_derived": False,
                "description": "Office equipment and machinery",
                "is_active": True,
            },
            {
                "name": "Accounts Payable",
                "category_path": "Liabilities/Current Liabilities",
                "sub_category": "Payables",
                "type": 2,  # Liability
                "sub_type": 1,  # Current Liability
                "is_summary": False,
                "is_derived": False,
                "description": "Outstanding vendor invoices",
                "is_active": True,
            },
            {
                "name": "Revenue Summary",
                "category_path": "Income/Operating Revenue",
                "sub_category": "Summary",
                "type": 4,  # Income
                "sub_type": None,  # No sub-type for summary accounts
                "is_summary": True,
                "is_derived": True,
                "description": "Summary of all revenue accounts",
                "is_active": True,
            },
        ]

    def tearDown(self):
        """
        Clean up after test execution.

        Resets the database factory to ensure clean state for next test.
        """
        reset_database_manager()

    def test_create_account_success(self):
        """Test successful account creation."""
        account_data = self.sample_accounts[0]

        # Create account
        account_id = self.account_store.create_account(account_data)

        # Verify account was created
        self.assertIsInstance(account_id, int)
        self.assertGreater(account_id, 0)

        # Verify account data
        created_account = self.account_store.get_account_by_id(account_id)
        self.assertIsNotNone(created_account)
        self.assertEqual(created_account["name"], account_data["name"])
        self.assertEqual(
            created_account["category_path"], account_data["category_path"]
        )
        self.assertEqual(created_account["type"], account_data["type"])
        self.assertEqual(created_account["sub_type"], account_data["sub_type"])
        self.assertEqual(created_account["is_summary"], account_data["is_summary"])
        self.assertEqual(created_account["is_derived"], account_data["is_derived"])
        self.assertEqual(created_account["description"], account_data["description"])
        self.assertEqual(created_account["is_active"], account_data["is_active"])

        # Verify timestamps were set
        self.assertIsNotNone(created_account["created_at"])
        self.assertIsNotNone(created_account["updated_at"])

    def test_create_account_with_null_sub_type(self):
        """Test account creation with NULL sub_type."""
        account_data = self.sample_accounts[4]  # Revenue Summary with sub_type=None

        account_id = self.account_store.create_account(account_data)

        created_account = self.account_store.get_account_by_id(account_id)
        self.assertIsNotNone(created_account)
        self.assertIsNone(created_account["sub_type"])

    def test_create_account_duplicate_name(self):
        """Test account creation with duplicate name (should succeed)."""
        account_data = self.sample_accounts[0]

        # Create first account
        account_id1 = self.account_store.create_account(account_data)

        # Create second account with same name (should succeed)
        account_id2 = self.account_store.create_account(account_data)

        # Both should be created successfully
        self.assertNotEqual(account_id1, account_id2)
        self.assertEqual(2, self.account_store.get_accounts_count())

    def test_get_account_by_id_existing(self):
        """Test retrieving existing account by ID."""
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        retrieved_account = self.account_store.get_account_by_id(account_id)

        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account["account_id"], account_id)
        self.assertEqual(retrieved_account["name"], account_data["name"])

    def test_get_account_by_id_nonexistent(self):
        """Test retrieving non-existent account by ID."""
        retrieved_account = self.account_store.get_account_by_id(99999)
        self.assertIsNone(retrieved_account)

    def test_get_account_by_name_existing(self):
        """Test retrieving existing account by name."""
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        retrieved_account = self.account_store.get_account_by_name(account_data["name"])

        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account["account_id"], account_id)
        self.assertEqual(retrieved_account["name"], account_data["name"])

    def test_get_account_by_name_nonexistent(self):
        """Test retrieving non-existent account by name."""
        retrieved_account = self.account_store.get_account_by_name("NonExistentAccount")
        self.assertIsNone(retrieved_account)

    def test_get_account_by_composite_key_existing(self):
        """Test retrieving account by composite key."""
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        retrieved_account = self.account_store.get_account_by_composite_key(
            account_data["name"],
            account_data["category_path"],
            account_data["type"],
            account_data["sub_type"],
        )

        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account["account_id"], account_id)

    def test_get_account_by_composite_key_with_null_sub_type(self):
        """Test retrieving account by composite key with NULL sub_type."""
        account_data = self.sample_accounts[4]  # Has sub_type=None
        account_id = self.account_store.create_account(account_data)

        retrieved_account = self.account_store.get_account_by_composite_key(
            account_data["name"],
            account_data["category_path"],
            account_data["type"],
            None,  # sub_type is None
        )

        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account["account_id"], account_id)

    def test_get_account_by_composite_key_nonexistent(self):
        """Test retrieving non-existent account by composite key."""
        retrieved_account = self.account_store.get_account_by_composite_key(
            "NonExistent", "NonExistent/Path", 1, 1
        )
        self.assertIsNone(retrieved_account)

    def test_get_accounts_by_type(self):
        """Test retrieving accounts filtered by type."""
        # Create accounts of different types
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Get all asset accounts (type 1)
        asset_accounts = self.account_store.get_accounts_by_type(1)

        self.assertEqual(len(asset_accounts), 3)  # 3 asset accounts in sample data
        for account in asset_accounts:
            self.assertEqual(account["type"], 1)

        # Get liability accounts (type 2)
        liability_accounts = self.account_store.get_accounts_by_type(2)

        self.assertEqual(
            len(liability_accounts), 1
        )  # 1 liability account in sample data
        for account in liability_accounts:
            self.assertEqual(account["type"], 2)

    def test_get_accounts_by_type_with_limit(self):
        """Test retrieving accounts by type with limit."""
        # Create multiple accounts of same type
        for i in range(5):
            account_data = self.sample_accounts[0].copy()
            account_data["name"] = f"Account {i+1}"
            self.account_store.create_account(account_data)

        # Get first 3 accounts
        accounts = self.account_store.get_accounts_by_type(1, limit=3)

        self.assertEqual(len(accounts), 3)
        for account in accounts:
            self.assertEqual(account["type"], 1)

    def test_search_accounts_by_name(self):
        """Test searching accounts by name."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Search for "Cash"
        results = self.account_store.search_accounts("Cash")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Cash Account")

    def test_search_accounts_by_description(self):
        """Test searching accounts by description."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Search for "equipment"
        results = self.account_store.search_accounts("equipment")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Equipment")

    def test_search_accounts_partial_match(self):
        """Test searching accounts with partial matches."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Search for "Cash" (should match Cash Account)
        results = self.account_store.search_accounts("Cash")

        self.assertGreaterEqual(len(results), 1)  # At least Cash Account
        for result in results:
            # Check if "Cash" is in name or description
            self.assertTrue(
                "Cash" in result["name"] or "Cash" in result["description"],
                f"Expected 'Cash' in name or description of {result['name']}",
            )

    def test_search_accounts_no_matches(self):
        """Test searching accounts with no matches."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Search for non-existent term
        results = self.account_store.search_accounts("NonExistentTerm")

        self.assertEqual(len(results), 0)

    def test_get_all_accounts(self):
        """Test retrieving all accounts."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        # Get all accounts
        all_accounts = self.account_store.get_all_accounts()

        self.assertEqual(len(all_accounts), len(self.sample_accounts))

        # Verify all accounts are present
        account_names = [acc["name"] for acc in all_accounts]
        for sample_account in self.sample_accounts:
            self.assertIn(sample_account["name"], account_names)

    def test_get_all_accounts_with_limit(self):
        """Test retrieving all accounts with limit."""
        # Create more accounts than limit
        for i in range(10):
            account_data = self.sample_accounts[0].copy()
            account_data["name"] = f"Account {i+1}"
            self.account_store.create_account(account_data)

        # Get first 5 accounts
        accounts = self.account_store.get_all_accounts(limit=5)

        self.assertEqual(len(accounts), 5)

    def test_update_account_success(self):
        """Test successful account update."""
        # Create account
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        # Update account
        update_data = {
            "name": "Updated Cash Account",
            "description": "Updated description",
            "is_active": False,
        }

        success = self.account_store.update_account(account_id, update_data)

        self.assertTrue(success)

        # Verify update
        updated_account = self.account_store.get_account_by_id(account_id)
        self.assertEqual(updated_account["name"], update_data["name"])
        self.assertEqual(updated_account["description"], update_data["description"])
        self.assertEqual(updated_account["is_active"], update_data["is_active"])

        # Verify other fields unchanged
        self.assertEqual(updated_account["type"], account_data["type"])
        self.assertEqual(updated_account["sub_type"], account_data["sub_type"])

    def test_update_account_nonexistent(self):
        """Test updating non-existent account."""
        update_data = {"name": "Updated Name"}

        success = self.account_store.update_account(99999, update_data)

        self.assertFalse(success)

    def test_update_account_no_fields(self):
        """Test updating account with no fields."""
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        success = self.account_store.update_account(account_id, {})

        self.assertFalse(success)

    def test_delete_account_success(self):
        """Test successful account deletion."""
        # Create account
        account_data = self.sample_accounts[0]
        account_id = self.account_store.create_account(account_data)

        # Verify account exists
        self.assertIsNotNone(self.account_store.get_account_by_id(account_id))

        # Delete account
        success = self.account_store.delete_account(account_id)

        self.assertTrue(success)

        # Verify account is deleted
        self.assertIsNone(self.account_store.get_account_by_id(account_id))

    def test_delete_account_nonexistent(self):
        """Test deleting non-existent account."""
        success = self.account_store.delete_account(99999)

        self.assertFalse(success)

    def test_get_accounts_count_empty(self):
        """Test getting account count when database is empty."""
        count = self.account_store.get_accounts_count()
        self.assertEqual(count, 0)

    def test_get_accounts_count_with_data(self):
        """Test getting account count with data."""
        # Create accounts
        for account_data in self.sample_accounts:
            self.account_store.create_account(account_data)

        count = self.account_store.get_accounts_count()
        self.assertEqual(count, len(self.sample_accounts))

    def test_account_data_integrity(self):
        """Test account data integrity and constraints."""
        # Test with invalid account type
        invalid_account = self.sample_accounts[0].copy()
        invalid_account["type"] = 99  # Invalid type

        with self.assertRaises(Exception):
            self.account_store.create_account(invalid_account)

        # Test with invalid sub_type
        invalid_account = self.sample_accounts[0].copy()
        invalid_account["sub_type"] = 99  # Invalid sub_type

        with self.assertRaises(Exception):
            self.account_store.create_account(invalid_account)

    def test_account_ordering(self):
        """Test that accounts are returned in correct order."""
        # Create accounts with specific names
        account_names = ["Zebra Account", "Alpha Account", "Beta Account"]

        for name in account_names:
            account_data = self.sample_accounts[0].copy()
            account_data["name"] = name
            self.account_store.create_account(account_data)

        # Get all accounts (should be ordered by name)
        all_accounts = self.account_store.get_all_accounts()

        self.assertEqual(len(all_accounts), len(account_names))

        # Verify alphabetical ordering
        retrieved_names = [acc["name"] for acc in all_accounts]
        self.assertEqual(retrieved_names, sorted(account_names))


if __name__ == "__main__":
    unittest.main(verbosity=2)
