"""
Localization system for enum fields
Provides language-specific translations for enum values
"""

from typing import Dict, Any
from enum import IntEnum
from .enums import (
    AccountType,
    DataSource,
    Currency,
    RevenueSubType,
    ExpenseSubType,
    DerivedSubType,
)


class Language(IntEnum):
    """Supported languages"""

    ENGLISH = 1
    ARABIC = 2


class LocalizationManager:
    """Manages localization for enum fields"""

    def __init__(self):
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Dict[int, Dict[int, str]]]:
        """Load all translations"""
        return {
            "account_type": {
                Language.ENGLISH: {
                    AccountType.REVENUE: "Revenue",
                    AccountType.COGS: "Cost of Goods Sold",
                    AccountType.EXPENSE: "Expense",
                    AccountType.TAX: "Tax",
                    AccountType.DERIVED: "Derived",
                },
                Language.ARABIC: {
                    AccountType.REVENUE: "إيرادات",
                    AccountType.COGS: "تكلفة البضائع المباعة",
                    AccountType.EXPENSE: "مصروفات",
                    AccountType.TAX: "ضريبة",
                    AccountType.DERIVED: "مشتق",
                },
            },
            "data_source": {
                Language.ENGLISH: {
                    DataSource.PL_REPORT: "P&L Report",
                    DataSource.ROOTFI_REPORT: "Rootfi Report",
                },
                Language.ARABIC: {
                    DataSource.PL_REPORT: "تقرير الأرباح والخسائر",
                    DataSource.ROOTFI_REPORT: "تقرير Rootfi",
                },
            },
            "currency": {
                Language.ENGLISH: {
                    Currency.USD: "US Dollar",
                    Currency.EUR: "Euro",
                    Currency.GBP: "British Pound",
                    Currency.CAD: "Canadian Dollar",
                    Currency.AUD: "Australian Dollar",
                    Currency.JPY: "Japanese Yen",
                    Currency.INR: "Indian Rupee",
                    Currency.AED: "UAE Dirham",
                },
                Language.ARABIC: {
                    Currency.USD: "الدولار الأمريكي",
                    Currency.EUR: "اليورو",
                    Currency.GBP: "الجنيه الإسترليني",
                    Currency.CAD: "الدولار الكندي",
                    Currency.AUD: "الدولار الأسترالي",
                    Currency.JPY: "الين الياباني",
                    Currency.INR: "الروبية الهندية",
                    Currency.AED: "درهم إماراتي",
                },
            },
            "revenue_sub_type": {
                Language.ENGLISH: {
                    RevenueSubType.OPERATING: "Operating",
                    RevenueSubType.NON_OPERATING: "Non-Operating",
                },
                Language.ARABIC: {
                    RevenueSubType.OPERATING: "تشغيلي",
                    RevenueSubType.NON_OPERATING: "غير تشغيلي",
                },
            },
            "expense_sub_type": {
                Language.ENGLISH: {
                    ExpenseSubType.OPERATING: "Operating",
                    ExpenseSubType.NON_OPERATING: "Non-Operating",
                },
                Language.ARABIC: {
                    ExpenseSubType.OPERATING: "تشغيلي",
                    ExpenseSubType.NON_OPERATING: "غير تشغيلي",
                },
            },
            "derived_sub_type": {
                Language.ENGLISH: {
                    DerivedSubType.GROSS_PROFIT: "Gross Profit",
                    DerivedSubType.OPERATING_PROFIT: "Operating Profit",
                    DerivedSubType.EBITDA: "EBITDA",
                    DerivedSubType.NON_OPERATING_INCOME: "Non-Operating Income",
                    DerivedSubType.PROFIT_BEFORE_TAX: "Profit Before Tax",
                    DerivedSubType.NET_PROFIT: "Net Profit",
                    DerivedSubType.OTHER: "Other",
                },
                Language.ARABIC: {
                    DerivedSubType.GROSS_PROFIT: "الربح الإجمالي",
                    DerivedSubType.OPERATING_PROFIT: "الربح التشغيلي",
                    DerivedSubType.EBITDA: "الأرباح قبل الفوائد والضرائب والإهلاك والاستهلاك",
                    DerivedSubType.NON_OPERATING_INCOME: "الدخل غير التشغيلي",
                    DerivedSubType.PROFIT_BEFORE_TAX: "الربح قبل الضريبة",
                    DerivedSubType.NET_PROFIT: "صافي الربح",
                    DerivedSubType.OTHER: "أخرى",
                },
            },
        }

    def localize_enum(
        self, enum_type: str, enum_value: int, language: Language = Language.ENGLISH
    ) -> str:
        """Get localized string for enum value"""
        if enum_type not in self.translations:
            return str(enum_value)

        if language not in self.translations[enum_type]:
            language = Language.ENGLISH  # Fallback to English

        return self.translations[enum_type][language].get(enum_value, str(enum_value))

    def localize_field(
        self, field_name: str, value: Any, language: Language = Language.ENGLISH
    ) -> Any:
        """Localize a field value if it's an enum"""
        if field_name == "account_type" and isinstance(value, int):
            return self.localize_enum("account_type", value, language)
        elif field_name == "data_source" and isinstance(value, int):
            return self.localize_enum("data_source", value, language)
        elif field_name == "currency" and isinstance(value, int):
            return self.localize_enum("currency", value, language)
        elif field_name == "revenue_sub_type" and isinstance(value, int):
            return self.localize_enum("revenue_sub_type", value, language)
        elif field_name == "expense_sub_type" and isinstance(value, int):
            return self.localize_enum("expense_sub_type", value, language)
        elif field_name == "derived_sub_type" and isinstance(value, int):
            return self.localize_enum("derived_sub_type", value, language)

        return value

    def get_supported_languages(self) -> Dict[int, str]:
        """Get list of supported languages"""
        return {Language.ENGLISH: "English", Language.ARABIC: "العربية"}


# Global localization manager instance
localization_manager = LocalizationManager()
