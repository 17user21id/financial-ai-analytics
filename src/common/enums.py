"""
System and Financial Data Enums
Defines all enum types for the system
"""

from enum import IntEnum, Enum


# System Logging Enums
class LogComponent(Enum):
    """Log component types"""

    APP = "app"
    AI = "ai"
    DATABASE = "database"
    API = "api"
    PARSER = "parser"
    ERROR = "error"
    PERFORMANCE = "performance"


# Financial Data Enums
class DataSource(IntEnum):
    """Data source types"""

    PL_REPORT = 1  # P&L Report (data_set_1.json)
    ROOTFI_REPORT = 2  # Rootfi Report (data_set_2.json)


class AccountType(IntEnum):
    """Main account types"""

    REVENUE = 1
    COGS = 2
    EXPENSE = 3
    TAX = 4
    DERIVED = 5


class RevenueSubType(IntEnum):
    """Revenue sub-types"""

    OPERATING = 1
    NON_OPERATING = 2


class ExpenseSubType(IntEnum):
    """Expense sub-types"""

    OPERATING = 1
    NON_OPERATING = 2


class DerivedSubType(IntEnum):
    """Derived metric sub-types"""

    GROSS_PROFIT = 1
    OPERATING_PROFIT = 2
    EBITDA = 3
    NON_OPERATING_INCOME = 4
    PROFIT_BEFORE_TAX = 5
    NET_PROFIT = 6
    OTHER = 7


class Currency(IntEnum):
    """Currency types"""

    USD = 1
    EUR = 2
    GBP = 3
    CAD = 4
    AUD = 5
    JPY = 6
    INR = 7
    AED = 8  # UAE Dirham
