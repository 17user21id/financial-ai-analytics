"""
Enum Mappings for Database Schema
Provides human-readable mappings for all database enums
"""

from src.common.enums import (
    AccountType,
    DataSource,
    Currency,
    RevenueSubType,
    ExpenseSubType,
    DerivedSubType,
)


class EnumMappings:
    """Central repository for all enum definitions and mappings"""

    @staticmethod
    def get_all_enum_definitions() -> dict:
        """
        Get all enum definitions with values, descriptions, and usage examples

        Returns:
            Dictionary containing all enum definitions for LLM context
        """
        return {
            "AccountType": {
                "description": "Types of financial accounts - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "REVENUE",
                        "value": int(AccountType.REVENUE),
                        "description": "Revenue/Income accounts",
                    },
                    {
                        "name": "COGS",
                        "value": int(AccountType.COGS),
                        "description": "Cost of Goods Sold",
                    },
                    {
                        "name": "EXPENSE",
                        "value": int(AccountType.EXPENSE),
                        "description": "Expense accounts",
                    },
                    {
                        "name": "TAX",
                        "value": int(AccountType.TAX),
                        "description": "Tax-related accounts",
                    },
                    {
                        "name": "DERIVED",
                        "value": int(AccountType.DERIVED),
                        "description": "Calculated/derived metrics",
                    },
                ],
                "usage": "CRITICAL: Use integer values in WHERE clauses",
                "examples": [
                    "WHERE a.type = 1  -- REVENUE",
                    "WHERE a.type = 2  -- COGS",
                    "WHERE a.type = 3  -- EXPENSE",
                    "WHERE a.type = 4  -- TAX",
                    "WHERE a.type = 5  -- DERIVED",
                ],
            },
            "DataSource": {
                "description": "Source system for financial data - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "PL_REPORT",
                        "value": int(DataSource.PL_REPORT),
                        "description": "P&L Report (data_set_1.json)",
                    },
                    {
                        "name": "ROOTFI_REPORT",
                        "value": int(DataSource.ROOTFI_REPORT),
                        "description": "Rootfi Report (data_set_2.json)",
                    },
                ],
                "usage": "CRITICAL: Use integer values in WHERE clauses",
                "examples": [
                    "WHERE ft.source_id = 1  -- PL_REPORT",
                    "WHERE ft.source_id = 2  -- ROOTFI_REPORT",
                ],
            },
            "Currency": {
                "description": "Currency types for transactions - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "USD",
                        "value": int(Currency.USD),
                        "description": "US Dollar",
                    },
                    {"name": "EUR", "value": int(Currency.EUR), "description": "Euro"},
                    {
                        "name": "GBP",
                        "value": int(Currency.GBP),
                        "description": "British Pound",
                    },
                    {
                        "name": "CAD",
                        "value": int(Currency.CAD),
                        "description": "Canadian Dollar",
                    },
                    {
                        "name": "AUD",
                        "value": int(Currency.AUD),
                        "description": "Australian Dollar",
                    },
                    {
                        "name": "JPY",
                        "value": int(Currency.JPY),
                        "description": "Japanese Yen",
                    },
                    {
                        "name": "INR",
                        "value": int(Currency.INR),
                        "description": "Indian Rupee",
                    },
                    {
                        "name": "AED",
                        "value": int(Currency.AED),
                        "description": "UAE Dirham",
                    },
                ],
                "usage": "CRITICAL: Use integer values in WHERE clauses",
                "examples": [
                    "WHERE ft.currency = 1  -- USD",
                    "WHERE ft.currency = 7  -- INR",
                ],
            },
            "RevenueSubType": {
                "description": "Revenue account classification - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "OPERATING",
                        "value": int(RevenueSubType.OPERATING),
                        "description": "Operating revenue",
                    },
                    {
                        "name": "NON_OPERATING",
                        "value": int(RevenueSubType.NON_OPERATING),
                        "description": "Non-operating revenue",
                    },
                ],
                "usage": "CRITICAL: Use integer values with revenue accounts (type = 1)",
                "examples": [
                    "WHERE a.type = 1 AND a.sub_type = 1  -- Operating Revenue",
                    "WHERE a.type = 1 AND a.sub_type = 2  -- Non-operating Revenue",
                ],
            },
            "ExpenseSubType": {
                "description": "Expense account classification - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "OPERATING",
                        "value": int(ExpenseSubType.OPERATING),
                        "description": "Operating expenses",
                    },
                    {
                        "name": "NON_OPERATING",
                        "value": int(ExpenseSubType.NON_OPERATING),
                        "description": "Non-operating expenses",
                    },
                ],
                "usage": "CRITICAL: Use integer values with expense accounts (type = 3)",
                "examples": [
                    "WHERE a.type = 3 AND a.sub_type = 1  -- Operating Expense",
                    "WHERE a.type = 3 AND a.sub_type = 2  -- Non-operating Expense",
                ],
            },
            "DerivedSubType": {
                "description": "Types of derived/calculated metrics - ALWAYS use integer values in SQL",
                "values": [
                    {
                        "name": "GROSS_PROFIT",
                        "value": int(DerivedSubType.GROSS_PROFIT),
                        "description": "Gross Profit (Revenue - COGS)",
                    },
                    {
                        "name": "OPERATING_PROFIT",
                        "value": int(DerivedSubType.OPERATING_PROFIT),
                        "description": "Operating Profit",
                    },
                    {
                        "name": "EBITDA",
                        "value": int(DerivedSubType.EBITDA),
                        "description": "Earnings Before Interest, Taxes, Depreciation & Amortization",
                    },
                    {
                        "name": "NON_OPERATING_INCOME",
                        "value": int(DerivedSubType.NON_OPERATING_INCOME),
                        "description": "Non-operating income",
                    },
                    {
                        "name": "PROFIT_BEFORE_TAX",
                        "value": int(DerivedSubType.PROFIT_BEFORE_TAX),
                        "description": "Profit before tax",
                    },
                    {
                        "name": "NET_PROFIT",
                        "value": int(DerivedSubType.NET_PROFIT),
                        "description": "Net Profit after all deductions",
                    },
                    {
                        "name": "OTHER",
                        "value": int(DerivedSubType.OTHER),
                        "description": "Other derived metrics",
                    },
                ],
                "usage": "CRITICAL: Use integer values with derived accounts (type = 5)",
                "examples": [
                    "WHERE a.type = 5 AND a.sub_type = 1  -- GROSS_PROFIT",
                    "WHERE a.type = 5 AND a.sub_type = 2  -- OPERATING_PROFIT",
                    "WHERE a.type = 5 AND a.sub_type = 6  -- NET_PROFIT",
                ],
            },
        }

    @staticmethod
    def get_human_readable_mappings() -> dict:
        """
        Get mappings from enum integer values to human-readable names

        Returns:
            Dictionary mapping enum types to their human-readable values
        """
        return {
            "account_type": {
                int(AccountType.REVENUE): "Revenue",
                int(AccountType.COGS): "Cost of Goods Sold",
                int(AccountType.EXPENSE): "Expense",
                int(AccountType.TAX): "Tax",
                int(AccountType.DERIVED): "Derived/Calculated",
            },
            "data_source": {
                int(DataSource.PL_REPORT): "P&L Report",
                int(DataSource.ROOTFI_REPORT): "Rootfi Report",
            },
            "currency": {
                int(Currency.USD): "USD (US Dollar)",
                int(Currency.EUR): "EUR (Euro)",
                int(Currency.GBP): "GBP (British Pound)",
                int(Currency.CAD): "CAD (Canadian Dollar)",
                int(Currency.AUD): "AUD (Australian Dollar)",
                int(Currency.JPY): "JPY (Japanese Yen)",
                int(Currency.INR): "INR (Indian Rupee)",
                int(Currency.AED): "AED (UAE Dirham)",
            },
            "revenue_sub_type": {
                int(RevenueSubType.OPERATING): "Operating Revenue",
                int(RevenueSubType.NON_OPERATING): "Non-Operating Revenue",
            },
            "expense_sub_type": {
                int(ExpenseSubType.OPERATING): "Operating Expense",
                int(ExpenseSubType.NON_OPERATING): "Non-Operating Expense",
            },
            "derived_sub_type": {
                int(DerivedSubType.GROSS_PROFIT): "Gross Profit",
                int(DerivedSubType.OPERATING_PROFIT): "Operating Profit",
                int(DerivedSubType.EBITDA): "EBITDA",
                int(DerivedSubType.NON_OPERATING_INCOME): "Non-Operating Income",
                int(DerivedSubType.PROFIT_BEFORE_TAX): "Profit Before Tax",
                int(DerivedSubType.NET_PROFIT): "Net Profit",
                int(DerivedSubType.OTHER): "Other Derived Metric",
            },
        }

    @staticmethod
    def format_enum_reference_for_llm() -> str:
        """
        Format enum mappings as a readable reference for LLM prompts

        Returns:
            Formatted string explaining enum value to name mappings
        """
        mappings = EnumMappings.get_human_readable_mappings()

        reference = ["ENUM VALUE MAPPINGS (for human-readable responses):", ""]

        reference.append("Account Types:")
        for value, name in mappings["account_type"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append("Data Sources:")
        for value, name in mappings["data_source"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append("Currencies:")
        for value, name in mappings["currency"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append("Revenue Sub-Types:")
        for value, name in mappings["revenue_sub_type"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append("Expense Sub-Types:")
        for value, name in mappings["expense_sub_type"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append("Derived Metric Types:")
        for value, name in mappings["derived_sub_type"].items():
            reference.append(f"  {value} = {name}")
        reference.append("")

        reference.append(
            "IMPORTANT: Always use these human-readable names in your response,"
        )
        reference.append("NOT the integer values. For example, say 'Revenue' not '1',")
        reference.append("and 'USD (US Dollar)' not '1'.")

        return "\n".join(reference)
