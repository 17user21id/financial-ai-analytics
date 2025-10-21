"""
Database Schema Provider
Provides database schema information with enum mappings for LLM query generation
"""

import json
from typing import Dict, Any
from .enum_mappings import EnumMappings


class DatabaseSchemaProvider:
    """Provides complete database schema with enum mappings for LLM"""

    def get_schema_for_llm(self) -> Dict[str, Any]:
        """
        Returns schema in LLM-friendly format with all enums and relationships

        Returns:
            Dictionary containing tables, columns, enums, relationships, and common patterns
        """
        return {
            "tables": {
                "accounts": {
                    "description": "Master table of all financial accounts",
                    "columns": {
                        "account_id": {
                            "type": "INTEGER",
                            "description": "Primary key, unique identifier",
                        },
                        "name": {
                            "type": "TEXT",
                            "description": "Account name (e.g., 'Business Revenue', 'Operating Expenses')",
                        },
                        "type": {
                            "type": "INTEGER",
                            "description": "Account type - MUST use AccountType enum values",
                        },
                        "sub_type": {
                            "type": "INTEGER",
                            "description": "Account sub-type (nullable) - use RevenueSubType or ExpenseSubType",
                        },
                        "is_derived": {
                            "type": "BOOLEAN",
                            "description": "Whether account is calculated (0=false, 1=true)",
                        },
                        "description": {
                            "type": "TEXT",
                            "description": "Detailed account description",
                        },
                        "platform_id": {
                            "type": "TEXT",
                            "description": "External platform identifier",
                        },
                        "created_at": {
                            "type": "TIMESTAMP",
                            "description": "Creation timestamp",
                        },
                    },
                    "indexes": ["name", "type", "sub_type", "is_derived"],
                    "primary_key": "account_id",
                },
                "finance_transactions": {
                    "description": "All financial transactions across time periods",
                    "columns": {
                        "tx_id": {
                            "type": "INTEGER",
                            "description": "Primary key, unique transaction identifier",
                        },
                        "account_id": {
                            "type": "INTEGER",
                            "description": "Foreign key to accounts table",
                        },
                        "period_start": {
                            "type": "DATE",
                            "description": "Period start date in YYYY-MM-DD format",
                        },
                        "period_end": {
                            "type": "DATE",
                            "description": "Period end date in YYYY-MM-DD format",
                        },
                        "value": {
                            "type": "DECIMAL(15,2)",
                            "description": "Transaction amount (positive or negative)",
                        },
                        "currency": {
                            "type": "INTEGER",
                            "description": "Currency code - MUST use Currency enum",
                        },
                        "derived_sub_type": {
                            "type": "INTEGER",
                            "description": "For derived accounts only (nullable) - use DerivedSubType enum",
                        },
                        "posted_date": {
                            "type": "TIMESTAMP",
                            "description": "Transaction posting date",
                        },
                        "created_by": {
                            "type": "TEXT",
                            "description": "User or system that created the transaction",
                        },
                        "notes": {
                            "type": "TEXT",
                            "description": "Additional transaction notes",
                        },
                        "source_id": {
                            "type": "INTEGER",
                            "description": "Data source - MUST use DataSource enum",
                        },
                    },
                    "indexes": [
                        "account_id",
                        "period_start",
                        "period_end",
                        "source_id",
                        "posted_date",
                    ],
                    "primary_key": "tx_id",
                    "foreign_keys": ["account_id → accounts.account_id"],
                },
            },
            "enums": EnumMappings.get_all_enum_definitions(),
            "relationships": [
                "finance_transactions.account_id → accounts.account_id (INNER JOIN)",
                "finance_transactions.source_id references DataSource enum",
                "accounts.type references AccountType enum",
                "accounts.sub_type references RevenueSubType or ExpenseSubType enum",
                "finance_transactions.derived_sub_type references DerivedSubType enum",
            ],
            "common_patterns": {
                "total_revenue": {
                    "description": "Calculate total revenue across all periods",
                    "sql": "SELECT SUM(ft.value) as total_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1",
                },
                "total_expenses": {
                    "description": "Calculate total expenses across all periods",
                    "sql": "SELECT SUM(ft.value) as total_expenses FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 3",
                },
                "revenue_by_period": {
                    "description": "Group revenue by time period",
                    "sql": "SELECT ft.period_start, ft.period_end, SUM(ft.value) as total_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 GROUP BY ft.period_start, ft.period_end ORDER BY ft.period_start",
                },
                "revenue_by_account": {
                    "description": "Break down revenue by individual accounts",
                    "sql": "SELECT a.name as account_name, SUM(ft.value) as total_value FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 GROUP BY a.name ORDER BY total_value DESC",
                },
                "transactions_by_source": {
                    "description": "Analyze transactions by data source",
                    "sql": "SELECT ft.source_id, COUNT(*) as transaction_count, SUM(ft.value) as total_value FROM finance_transactions ft GROUP BY ft.source_id",
                },
                "monthly_revenue": {
                    "description": "Revenue aggregated by month",
                    "sql": "SELECT strftime('%Y-%m', ft.period_start) as month, SUM(ft.value) as monthly_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 GROUP BY month ORDER BY month DESC",
                },
            },
            "query_rules": [
                "ALWAYS use JOIN between finance_transactions and accounts tables",
                "Use alias 'ft' for finance_transactions and 'a' for accounts",
                "ALWAYS use enum INTEGER values in WHERE clauses, never string names",
                "Date filters: period_start >= 'YYYY-MM-DD' AND period_end <= 'YYYY-MM-DD'",
                "For aggregations, use SUM, AVG, COUNT, MIN, MAX",
                "Always include LIMIT to prevent excessive results (default: 100)",
                "Use ORDER BY for better result presentation",
                "Use GROUP BY when aggregating data",
            ],
        }

    def get_schema_json(self) -> str:
        """
        Returns schema as formatted JSON string for LLM prompts

        Returns:
            JSON string with proper indentation
        """
        return json.dumps(self.get_schema_for_llm(), indent=2)

    def get_enum_explanation(self) -> str:
        """
        Returns human-readable explanation of all enums

        Returns:
            Formatted string explaining all enum values
        """
        schema = self.get_schema_for_llm()
        explanation = []

        explanation.append("ENUM VALUE REFERENCE:")
        explanation.append("=" * 50)

        for enum_name, enum_data in schema["enums"].items():
            explanation.append(f"\n{enum_name}:")
            explanation.append(f"  {enum_data['description']}")
            explanation.append("  Values:")
            for name, value in enum_data["values"].items():
                explanation.append(f"    {name} = {value}")
            explanation.append(f"  {enum_data['usage']}")

        return "\n".join(explanation)

    def get_table_summary(self) -> str:
        """
        Returns concise summary of tables for quick reference

        Returns:
            Formatted string with table information
        """
        schema = self.get_schema_for_llm()
        summary = []

        summary.append("TABLE SUMMARY:")
        summary.append("=" * 50)

        for table_name, table_data in schema["tables"].items():
            summary.append(f"\n{table_name}:")
            summary.append(f"  {table_data['description']}")
            summary.append(f"  Primary Key: {table_data['primary_key']}")
            summary.append(f"  Columns: {len(table_data['columns'])}")
            summary.append(
                f"  Key columns: {', '.join(list(table_data['columns'].keys())[:5])}..."
            )

        return "\n".join(summary)
