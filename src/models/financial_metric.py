from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal
from ..common.enums import AccountType, DataSource, Currency
from .account import Account
from .finance_transaction import FinanceTransaction


@dataclass
class FinancialMetric:
    """Legacy class for backward compatibility - maps to new schema"""

    account_id: str
    account_name: str
    account_type: str
    parent_account_id: Optional[str]
    is_derived: bool
    calculation_rule: Optional[str]
    description: str
    period_start: str
    period_end: str
    value: float
    currency: str = "USD"
    source_id: str = "pl_report"  # New field

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "parent_account_id": self.parent_account_id,
            "is_derived": self.is_derived,
            "calculation_rule": self.calculation_rule,
            "description": self.description,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "value": self.value,
            "currency": self.currency,
            "source_id": self.source_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FinancialMetric":
        """Create from dictionary"""
        return cls(
            account_id=data["account_id"],
            account_name=data["account_name"],
            account_type=data["account_type"],
            parent_account_id=data.get("parent_account_id"),
            is_derived=data.get("is_derived", False),
            calculation_rule=data.get("calculation_rule"),
            description=data.get("description", ""),
            period_start=data["period_start"],
            period_end=data["period_end"],
            value=data["value"],
            currency=data.get("currency", "USD"),
            source_id=data.get("source_id", "pl_report"),
        )

    def to_account(self) -> Account:
        """Convert to new Account model"""
        # Map account type string to enum
        type_mapping = {
            "revenue": AccountType.REVENUE,
            "cogs": AccountType.COGS,
            "expense": AccountType.EXPENSE,
            "tax": AccountType.TAX,
            "derived": AccountType.DERIVED,
        }

        account_type = type_mapping.get(self.account_type.lower(), AccountType.REVENUE)

        return Account(
            name=self.account_name,
            type=account_type,
            is_derived=self.is_derived,
            description=self.description,
            is_active=True,
        )

    def to_transaction(self, account_id: int) -> FinanceTransaction:
        """Convert to new FinanceTransaction model"""
        # Map currency string to enum
        currency_mapping = {
            "USD": Currency.USD,
            "EUR": Currency.EUR,
            "GBP": Currency.GBP,
            "CAD": Currency.CAD,
            "AUD": Currency.AUD,
            "JPY": Currency.JPY,
            "INR": Currency.INR,
        }

        currency = currency_mapping.get(self.currency.upper(), Currency.USD)

        # Map source string to enum
        source_mapping = {
            "pl_report": DataSource.PL_REPORT,
            "rootfi_report": DataSource.ROOTFI_REPORT,
        }

        source_id = source_mapping.get(self.source_id.lower(), DataSource.PL_REPORT)

        return FinanceTransaction(
            account_id=account_id,
            period_start=self.period_start,
            period_end=self.period_end,
            value=Decimal(str(self.value)),
            currency=currency,
            source_id=source_id,
            notes=self.description,
        )
