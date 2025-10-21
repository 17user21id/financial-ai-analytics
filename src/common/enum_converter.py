"""
Enum conversion utilities for API filters
Converts string values to enum values for filtering
"""

from typing import Any, Dict, List, Optional, Union
from .enums import (
    AccountType,
    DataSource,
    Currency,
    RevenueSubType,
    ExpenseSubType,
    DerivedSubType,
)


class EnumConverter:
    """Converts string values to enum values for API filtering"""

    def __init__(self):
        self.converters = {
            "account_type": self._convert_account_type,
            "type": self._convert_account_type,  # Alias
            "data_source": self._convert_data_source,
            "source_id": self._convert_data_source,  # Alias
            "currency": self._convert_currency,
            "revenue_sub_type": self._convert_revenue_sub_type,
            "expense_sub_type": self._convert_expense_sub_type,
            "derived_sub_type": self._convert_derived_sub_type,
            "sub_type": self._convert_sub_type,  # Generic sub_type converter
        }

    def convert_filter_value(self, field_name: str, value: Any) -> Any:
        """Convert filter value to appropriate enum if needed"""
        if field_name in self.converters:
            return self.converters[field_name](value)
        return value

    def convert_filter_condition(
        self, field_name: str, operator: str, value: Any
    ) -> tuple:
        """Convert filter condition with enum conversion"""
        converted_value = self.convert_filter_value(field_name, value)
        return field_name, operator, converted_value

    def _convert_account_type(
        self, value: Union[str, int, List]
    ) -> Union[int, List[int]]:
        """Convert account type string to enum value"""
        if isinstance(value, list):
            return [self._convert_account_type_single(v) for v in value]
        return self._convert_account_type_single(value)

    def _convert_account_type_single(self, value: Union[str, int]) -> int:
        """Convert single account type value"""
        if isinstance(value, int):
            return value

        mapping = {
            "revenue": AccountType.REVENUE,
            "income": AccountType.REVENUE,
            "sales": AccountType.REVENUE,
            "cogs": AccountType.COGS,
            "cost_of_goods_sold": AccountType.COGS,
            "cost": AccountType.COGS,
            "expense": AccountType.EXPENSE,
            "expenses": AccountType.EXPENSE,
            "operating_expense": AccountType.EXPENSE,
            "tax": AccountType.TAX,
            "taxes": AccountType.TAX,
            "derived": AccountType.DERIVED,
            "calculated": AccountType.DERIVED,
            "profit": AccountType.DERIVED,
        }

        return mapping.get(value.lower(), AccountType.REVENUE)

    def _convert_data_source(
        self, value: Union[str, int, List]
    ) -> Union[int, List[int]]:
        """Convert data source string to enum value"""
        if isinstance(value, list):
            return [self._convert_data_source_single(v) for v in value]
        return self._convert_data_source_single(value)

    def _convert_data_source_single(self, value: Union[str, int]) -> int:
        """Convert single data source value"""
        if isinstance(value, int):
            return value

        mapping = {
            "pl_report": DataSource.PL_REPORT,
            "p&l_report": DataSource.PL_REPORT,
            "profit_and_loss": DataSource.PL_REPORT,
            "quickbooks": DataSource.PL_REPORT,
            "rootfi_report": DataSource.ROOTFI_REPORT,
            "rootfi": DataSource.ROOTFI_REPORT,
        }

        return mapping.get(value.lower(), DataSource.PL_REPORT)

    def _convert_currency(self, value: Union[str, int, List]) -> Union[int, List[int]]:
        """Convert currency string to enum value"""
        if isinstance(value, list):
            return [self._convert_currency_single(v) for v in value]
        return self._convert_currency_single(value)

    def _convert_currency_single(self, value: Union[str, int]) -> int:
        """Convert single currency value"""
        if isinstance(value, int):
            return value

        mapping = {
            "usd": Currency.USD,
            "dollar": Currency.USD,
            "us_dollar": Currency.USD,
            "eur": Currency.EUR,
            "euro": Currency.EUR,
            "gbp": Currency.GBP,
            "pound": Currency.GBP,
            "british_pound": Currency.GBP,
            "cad": Currency.CAD,
            "canadian_dollar": Currency.CAD,
            "aud": Currency.AUD,
            "australian_dollar": Currency.AUD,
            "jpy": Currency.JPY,
            "yen": Currency.JPY,
            "japanese_yen": Currency.JPY,
            "inr": Currency.INR,
            "rupee": Currency.INR,
            "indian_rupee": Currency.INR,
            "aed": Currency.AED,
            "dirham": Currency.AED,
            "dirhams": Currency.AED,
            "dhirham": Currency.AED,
            "uae_dirham": Currency.AED,
            "emirati_dirham": Currency.AED,
        }

        return mapping.get(value.lower(), Currency.USD)

    def _convert_revenue_sub_type(
        self, value: Union[str, int, List]
    ) -> Union[int, List[int]]:
        """Convert revenue sub-type string to enum value"""
        if isinstance(value, list):
            return [self._convert_revenue_sub_type_single(v) for v in value]
        return self._convert_revenue_sub_type_single(value)

    def _convert_revenue_sub_type_single(self, value: Union[str, int]) -> int:
        """Convert single revenue sub-type value"""
        if isinstance(value, int):
            return value

        mapping = {
            "operating": RevenueSubType.OPERATING,
            "operational": RevenueSubType.OPERATING,
            "non_operating": RevenueSubType.NON_OPERATING,
            "non_operational": RevenueSubType.NON_OPERATING,
        }

        return mapping.get(value.lower(), RevenueSubType.OPERATING)

    def _convert_expense_sub_type(
        self, value: Union[str, int, List]
    ) -> Union[int, List[int]]:
        """Convert expense sub-type string to enum value"""
        if isinstance(value, list):
            return [self._convert_expense_sub_type_single(v) for v in value]
        return self._convert_expense_sub_type_single(value)

    def _convert_expense_sub_type_single(self, value: Union[str, int]) -> int:
        """Convert single expense sub-type value"""
        if isinstance(value, int):
            return value

        mapping = {
            "operating": ExpenseSubType.OPERATING,
            "operational": ExpenseSubType.OPERATING,
            "non_operating": ExpenseSubType.NON_OPERATING,
            "non_operational": ExpenseSubType.NON_OPERATING,
        }

        return mapping.get(value.lower(), ExpenseSubType.OPERATING)

    def _convert_derived_sub_type(
        self, value: Union[str, int, List]
    ) -> Union[int, List[int]]:
        """Convert derived sub-type string to enum value"""
        if isinstance(value, list):
            return [self._convert_derived_sub_type_single(v) for v in value]
        return self._convert_derived_sub_type_single(value)

    def _convert_derived_sub_type_single(self, value: Union[str, int]) -> int:
        """Convert single derived sub-type value"""
        if isinstance(value, int):
            return value

        mapping = {
            "gross_profit": DerivedSubType.GROSS_PROFIT,
            "gross": DerivedSubType.GROSS_PROFIT,
            "operating_profit": DerivedSubType.OPERATING_PROFIT,
            "operating": DerivedSubType.OPERATING_PROFIT,
            "ebitda": DerivedSubType.EBITDA,
            "non_operating_income": DerivedSubType.NON_OPERATING_INCOME,
            "non_operating": DerivedSubType.NON_OPERATING_INCOME,
            "profit_before_tax": DerivedSubType.PROFIT_BEFORE_TAX,
            "pretax": DerivedSubType.PROFIT_BEFORE_TAX,
            "net_profit": DerivedSubType.NET_PROFIT,
            "net": DerivedSubType.NET_PROFIT,
            "other": DerivedSubType.OTHER,
        }

        return mapping.get(value.lower(), DerivedSubType.OTHER)

    def _convert_sub_type(self, value: Union[str, int, List]) -> Union[int, List[int]]:
        """Generic sub-type converter - tries all sub-type converters"""
        if isinstance(value, list):
            return [self._convert_sub_type_single(v) for v in value]
        return self._convert_sub_type_single(value)

    def _convert_sub_type_single(self, value: Union[str, int]) -> int:
        """Convert single sub-type value using all converters"""
        if isinstance(value, int):
            return value

        # Try revenue sub-type first
        try:
            return self._convert_revenue_sub_type_single(value)
        except:
            pass

        # Try expense sub-type
        try:
            return self._convert_expense_sub_type_single(value)
        except:
            pass

        # Try derived sub-type
        try:
            return self._convert_derived_sub_type_single(value)
        except:
            pass

        # Default to 1 (operating)
        return 1

    def get_enum_values(self, enum_type: str) -> Dict[str, int]:
        """Get all possible values for an enum type"""
        if enum_type == "account_type":
            return {
                "revenue": AccountType.REVENUE,
                "cogs": AccountType.COGS,
                "expense": AccountType.EXPENSE,
                "tax": AccountType.TAX,
                "derived": AccountType.DERIVED,
            }
        elif enum_type == "data_source":
            return {
                "pl_report": DataSource.PL_REPORT,
                "rootfi_report": DataSource.ROOTFI_REPORT,
            }
        elif enum_type == "currency":
            return {
                "usd": Currency.USD,
                "eur": Currency.EUR,
                "gbp": Currency.GBP,
                "cad": Currency.CAD,
                "aud": Currency.AUD,
                "jpy": Currency.JPY,
                "inr": Currency.INR,
                "aed": Currency.AED,
            }
        elif enum_type == "revenue_sub_type":
            return {
                "operating": RevenueSubType.OPERATING,
                "non_operating": RevenueSubType.NON_OPERATING,
            }
        elif enum_type == "expense_sub_type":
            return {
                "operating": ExpenseSubType.OPERATING,
                "non_operating": ExpenseSubType.NON_OPERATING,
            }
        elif enum_type == "derived_sub_type":
            return {
                "gross_profit": DerivedSubType.GROSS_PROFIT,
                "operating_profit": DerivedSubType.OPERATING_PROFIT,
                "ebitda": DerivedSubType.EBITDA,
                "non_operating_income": DerivedSubType.NON_OPERATING_INCOME,
                "profit_before_tax": DerivedSubType.PROFIT_BEFORE_TAX,
                "net_profit": DerivedSubType.NET_PROFIT,
                "other": DerivedSubType.OTHER,
            }

        return {}


# Global enum converter instance
enum_converter = EnumConverter()
