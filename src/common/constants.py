"""
Constants for the Financial Data Processing System
Minimal set of actually used constants
"""

from .enums import DataSource, AccountType


# File Names (actually used)
class FileNames:
    QUICKBOOKS_DATA = "data_set_1.json"
    ROOTFI_DATA = "data_set_2.json"
    FINANCIAL_DB = "financial_data.db"
    FINANCIAL_DB_PROD = "financial_data_prod.db"


# Default Values (actually used)
class Defaults:
    CURRENCY = "USD"
    LOG_LEVEL = "INFO"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_PORT_TEST = 8001
    LIMIT_DEFAULT = 100
    LIMIT_MAX = 1000
