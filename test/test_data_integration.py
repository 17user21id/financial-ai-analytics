"""
Test suite for data integration functionality.

This module tests the import of financial data for a specific period
(2022-08-01 to 2022-08-31) using an in-memory SQLite database implementation.
It verifies that the correct number of accounts and transactions are created
and that period-specific data can be queried accurately.
"""

import os
import sys
import unittest

# Add project root directory to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

# Set environment to TEST for in-memory SQLite database
os.environ["ENVIRONMENT"] = "TEST"

from src.parsers.excel_to_database_importers import import_excel_to_database
from src.stores.database_manager import (
    reset_database_manager,
    get_account_store,
    get_transaction_store,
)


class TestDataIntegration(unittest.TestCase):
    """
    Test case for data integration and import.

    This test verifies the complete data import pipeline for financial
    data, including account creation, transaction processing, and period-specific
    data retrieval using an in-memory SQLite database.
    """

    def setUp(self):
        """
        Set up test environment and prepare test data.

        Initializes the test with the existing financial data Excel file
        and clears any existing data from the in-memory database to ensure
        a clean test state.
        """
        # Path to the existing financial data Excel file
        self.test_excel_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "dataset2_output_20251019_120912.xlsx",
        )

        # Verify test file exists
        if not os.path.exists(self.test_excel_file):
            raise FileNotFoundError(
                f"Test Excel file not found: {self.test_excel_file}"
            )

        # Reset database manager to ensure clean state
        reset_database_manager()

        # Get store instances (will be in-memory due to TEST environment)
        self.account_store = get_account_store()
        self.transaction_store = get_transaction_store()

        # Clear existing data to ensure clean test state
        self.transaction_store.clear_all_transactions()

    def tearDown(self):
        """
        Clean up after test execution.

        Clear all data from both accounts and transactions tables to ensure
        clean state for subsequent test runs.
        """
        # Clear all data from both tables to prevent test interference
        reset_database_manager()

    def test_data_integration_import(self):
        """
        Test the complete data import process.

        This test verifies:
        1. Successful import of Excel data to database
        2. Correct total count of accounts created
        3. Correct total count of transactions created
        4. Accurate retrieval of period-specific transactions

        Expected results:
        - 70 total accounts
        - 2520 total transactions
        - 70 transactions for period 2022-08-01 to 2022-08-31
        """
        # Import Excel data to database
        accounts_created, transactions_created = import_excel_to_database(
            self.test_excel_file
        )

        # Verify total counts in database
        total_accounts = self.account_store.get_accounts_count()
        total_transactions = self.transaction_store.get_transactions_count()

        # Query transactions for specific period
        period_transactions = self.transaction_store.query_transactions(
            filters=[
                {"field": "period_start", "operator": ">=", "value": "2022-08-01"},
                {"field": "period_end", "operator": "<=", "value": "2022-08-31"},
            ]
        )

        # Extract transaction count from query result
        period_count = (
            len(period_transactions.get("data", [])) if period_transactions else 0
        )

        # Assert expected account count
        self.assertEqual(
            total_accounts, 70, f"Expected 70 accounts, got {total_accounts}"
        )

        # Assert expected total transaction count
        self.assertEqual(
            total_transactions,
            2520,
            f"Expected 2520 transactions, got {total_transactions}",
        )

        # Assert expected period-specific transaction count
        self.assertEqual(
            period_count,
            70,
            f"Expected 70 transactions for period 2022-08-01 to 2022-08-31, got {period_count}",
        )

    def test_list_transactions_with_date_and_source_filter(self):
        """
        Test listing transactions with date range and data source filters.

        This test verifies:
        1. Filtering transactions by date range (2022-08-01 to 2022-08-31)
        2. Filtering transactions by data source (Rootfi Report)
        3. Correct count of filtered transactions

        Expected results:
        - 70 transactions matching the date range and Rootfi data source
        """
        # Import Excel data to database
        import_excel_to_database(self.test_excel_file)

        # Query transactions with date range and data source filters
        # DataSource.ROOTFI_REPORT = 2
        filtered_transactions = self.transaction_store.query_transactions(
            filters=[
                {"field": "period_start", "operator": ">=", "value": "2022-08-01"},
                {"field": "period_end", "operator": "<=", "value": "2022-08-31"},
                {"field": "source_id", "operator": "=", "value": 2},  # ROOTFI_REPORT
            ]
        )

        # Extract transaction count from query result
        transaction_count = (
            len(filtered_transactions.get("data", [])) if filtered_transactions else 0
        )

        # Assert expected transaction count for Rootfi report in the specified period
        self.assertEqual(
            transaction_count,
            70,
            f"Expected 70 transactions for Rootfi report in period 2022-08-01 to 2022-08-31, got {transaction_count}",
        )

        # Verify all transactions are from Rootfi report
        if filtered_transactions and filtered_transactions.get("data"):
            for transaction in filtered_transactions["data"]:
                self.assertEqual(
                    transaction.get("source_id"),
                    2,
                    f"Expected source_id to be 2 (ROOTFI_REPORT), got {transaction.get('source_id')}",
                )

    def test_revenue_aggregation_for_period(self):
        """
        Test revenue aggregation for a specific period.

        This test verifies:
        1. Aggregation of revenue transactions for period 2022-08-01 to 2022-08-31
        2. Correct total revenue value (around 3369378.43)

        Expected results:
        - Total revenue for period 2022-08-01 to 2022-08-31: ~3369378.43
        """
        # Import Excel data to database
        import_excel_to_database(self.test_excel_file)

        # Query revenue aggregation for specific period
        # AccountType.REVENUE = 1
        aggregated_result = self.transaction_store.query_transactions_aggregate(
            filters=[
                {"field": "account_type", "operator": "=", "value": 1},  # REVENUE
                {"field": "period_start", "operator": ">=", "value": "2022-08-01"},
                {"field": "period_end", "operator": "<=", "value": "2022-08-31"},
            ],
            aggregates=[
                {"function": "SUM", "field": "value", "alias": "total_revenue"}
            ],
        )

        # Extract total revenue from result
        total_revenue = None
        if aggregated_result and aggregated_result.get("groups"):
            # If there's grouping, sum all groups
            total_revenue = sum(
                group.get("total_revenue", 0) for group in aggregated_result["groups"]
            )
        elif (
            aggregated_result
            and "total_revenue" in aggregated_result.get("groups", [{}])[0]
            if aggregated_result.get("groups")
            else {}
        ):
            total_revenue = aggregated_result["groups"][0]["total_revenue"]

        # Since query_transactions_aggregate returns groups, we need to handle the response properly
        # The aggregation without group_by should return a single row with the total
        if (
            aggregated_result
            and aggregated_result.get("groups")
            and len(aggregated_result["groups"]) > 0
        ):
            total_revenue = aggregated_result["groups"][0].get("total_revenue", 0)
        else:
            total_revenue = 0

        # Assert expected revenue value (using assertAlmostEqual for floating point comparison)
        # Allow for small differences due to floating point precision (2 decimal places)
        expected_revenue = 3369378.43
        self.assertAlmostEqual(
            total_revenue,
            expected_revenue,
            places=2,
            msg=f"Expected total revenue around {expected_revenue}, got {total_revenue}",
        )

    def test_pl_report_revenue_aggregation(self):
        """
        Test P&L Report revenue aggregation for specific periods.

        This test verifies:
        1. Import of test_pl.xlsx file
        2. Revenue aggregation for April 2021 (expected: 84,790)
        3. Revenue aggregation for May 2022 (expected: 324,013.23)

        Expected results:
        - April 2021 revenue: 84,790
        - May 2022 revenue: 324,013.23 (20,263.23 + 3,750 + 300,000)
        """
        # Path to the P&L test file
        pl_test_file = os.path.join(
            os.path.dirname(__file__), "..", "resources", "test_pl.xlsx"
        )

        # Verify test file exists
        if not os.path.exists(pl_test_file):
            raise FileNotFoundError(f"P&L test Excel file not found: {pl_test_file}")

        # Import P&L Excel data to database
        accounts_created, transactions_created = import_excel_to_database(pl_test_file)

        # Test April 2021 revenue aggregation (using date range operators)
        # AccountType.REVENUE = 1
        april_2021_result = self.transaction_store.query_transactions_aggregate(
            filters=[
                {"field": "account_type", "operator": "=", "value": 1},  # REVENUE
                {"field": "period_start", "operator": ">=", "value": "2021-04-01"},
                {"field": "period_end", "operator": "<=", "value": "2021-04-30"},
            ],
            aggregates=[
                {"function": "SUM", "field": "value", "alias": "total_revenue"}
            ],
        )

        # Extract April 2021 revenue
        april_2021_revenue = 0
        if (
            april_2021_result
            and april_2021_result.get("groups")
            and len(april_2021_result["groups"]) > 0
        ):
            revenue_value = april_2021_result["groups"][0].get("total_revenue")
            april_2021_revenue = revenue_value if revenue_value is not None else 0

        # Test May 2022 revenue aggregation (using date range operators)
        may_2022_result = self.transaction_store.query_transactions_aggregate(
            filters=[
                {"field": "account_type", "operator": "=", "value": 1},  # REVENUE
                {"field": "period_start", "operator": ">=", "value": "2022-05-01"},
                {"field": "period_end", "operator": "<=", "value": "2022-05-31"},
            ],
            aggregates=[
                {"function": "SUM", "field": "value", "alias": "total_revenue"}
            ],
        )

        # Extract May 2022 revenue
        may_2022_revenue = 0
        if (
            may_2022_result
            and may_2022_result.get("groups")
            and len(may_2022_result["groups"]) > 0
        ):
            revenue_value = may_2022_result["groups"][0].get("total_revenue")
            may_2022_revenue = revenue_value if revenue_value is not None else 0

        # Debug: Print the aggregation results
        print(f"April 2021 revenue: {april_2021_revenue}")
        print(f"May 2022 revenue: {may_2022_revenue}")

        # Assert April 2021 revenue (expected: 84,790)
        expected_april_2021 = 84790
        self.assertAlmostEqual(
            april_2021_revenue,
            expected_april_2021,
            places=2,
            msg=f"Expected April 2021 revenue {expected_april_2021}, got {april_2021_revenue}",
        )

        # Assert May 2022 revenue (expected: 324,013.23 = 300,000 + 20,263.23 + 3,750)
        expected_may_2022 = 324013.23
        self.assertAlmostEqual(
            may_2022_revenue,
            expected_may_2022,
            places=2,
            msg=f"Expected May 2022 revenue {expected_may_2022}, got {may_2022_revenue}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
