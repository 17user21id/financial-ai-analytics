"""
Database Schema Definition
Single source of truth for all database table schemas

This module centralizes all CREATE TABLE statements to ensure consistency
across different database implementations (InMemoryDatabase, FileDatabase, DatabaseConnection).
"""

import logging

logger = logging.getLogger(__name__)


class DatabaseSchema:
    """Centralized database schema management"""

    # Table creation order matters due to foreign key constraints
    # Order: 1) accounts, 2) finance_transactions, 3) chat_sessions, 4) chat_messages

    @staticmethod
    def get_accounts_table_sql() -> str:
        """Get CREATE TABLE SQL for accounts table"""
        return """
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                category_path VARCHAR(500),
                sub_category VARCHAR(255),
                type INTEGER NOT NULL CHECK (type BETWEEN 1 AND 5),
                sub_type INTEGER CHECK (sub_type BETWEEN 1 AND 7 OR sub_type IS NULL),
                is_summary BOOLEAN DEFAULT FALSE,
                is_derived BOOLEAN DEFAULT FALSE,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

    @staticmethod
    def get_finance_transactions_table_sql() -> str:
        """Get CREATE TABLE SQL for finance_transactions table"""
        return """
            CREATE TABLE IF NOT EXISTS finance_transactions (
                tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                period_start DATE NOT NULL,
                period_end DATE NOT NULL,
                value DECIMAL(15,2) NOT NULL,
                currency INTEGER DEFAULT 1,
                derived_sub_type INTEGER CHECK (derived_sub_type BETWEEN 1 AND 7 OR derived_sub_type IS NULL),
                posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(100),
                notes TEXT,
                source_id INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
                CHECK (value >= -99999999999.99 AND value <= 99999999999.99)
            )
        """

    @staticmethod
    def get_chat_sessions_table_sql() -> str:
        """Get CREATE TABLE SQL for chat_sessions table"""
        return """
            CREATE TABLE IF NOT EXISTS chat_sessions (
                chat_id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context_summary TEXT,
                metadata TEXT
            )
        """

    @staticmethod
    def get_chat_messages_table_sql() -> str:
        """Get CREATE TABLE SQL for chat_messages table"""
        return """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                message_type TEXT NOT NULL CHECK (message_type IN ('user', 'assistant')),
                content TEXT NOT NULL,
                query_intent TEXT,
                data_points TEXT,
                prompt TEXT,
                llm_response TEXT,
                summary TEXT,
                token_count INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chat_sessions(chat_id) ON DELETE CASCADE
            )
        """

    @staticmethod
    def get_financial_indexes_sql() -> list:
        """Get CREATE INDEX SQL statements for financial data tables"""
        return [
            "CREATE INDEX IF NOT EXISTS idx_account_type ON accounts (type)",
            "CREATE INDEX IF NOT EXISTS idx_account_sub_type ON accounts (sub_type)",
            "CREATE INDEX IF NOT EXISTS idx_account_name ON accounts (name)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_period ON finance_transactions (period_start, period_end)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_account ON finance_transactions (account_id)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_source ON finance_transactions (source_id)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_value ON finance_transactions (value)",
        ]

    @staticmethod
    def get_chat_indexes_sql() -> list:
        """Get CREATE INDEX SQL statements for chat/conversation tables"""
        return [
            "CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_sessions (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_chat_last_activity ON chat_sessions (last_activity)",
            "CREATE INDEX IF NOT EXISTS idx_message_chat ON chat_messages (chat_id)",
            "CREATE INDEX IF NOT EXISTS idx_message_timestamp ON chat_messages (timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_message_type ON chat_messages (message_type)",
        ]

    @classmethod
    def initialize_schema(cls, cursor, commit_func=None):
        """
        Initialize complete database schema

        Args:
            cursor: Database cursor object
            commit_func: Optional function to commit changes (e.g., connection.commit)

        Returns:
            int: Number of tables created
        """
        tables_created = 0

        # Create tables in order (respecting foreign key dependencies)
        table_sqls = [
            ("accounts", cls.get_accounts_table_sql()),
            ("finance_transactions", cls.get_finance_transactions_table_sql()),
            ("chat_sessions", cls.get_chat_sessions_table_sql()),
            ("chat_messages", cls.get_chat_messages_table_sql()),
        ]

        for table_name, sql in table_sqls:
            try:
                cursor.execute(sql)
                tables_created += 1
                logger.debug(f"Created/verified table: {table_name}")
            except Exception as e:
                logger.error(f"Error creating table {table_name}: {e}")
                raise

        # Create financial data indexes
        for index_sql in cls.get_financial_indexes_sql():
            try:
                cursor.execute(index_sql)
            except Exception as e:
                logger.warning(f"Error creating financial index: {e}")

        # Create chat/conversation indexes
        for index_sql in cls.get_chat_indexes_sql():
            try:
                cursor.execute(index_sql)
            except Exception as e:
                logger.warning(f"Error creating chat index: {e}")

        # Commit if commit function provided
        if commit_func:
            commit_func()

        logger.info(
            f"Database schema initialized with {tables_created} tables: accounts, finance_transactions, chat_sessions, chat_messages"
        )

        return tables_created

    @classmethod
    def get_table_names(cls) -> list:
        """Get list of all table names in schema"""
        return ["accounts", "finance_transactions", "chat_sessions", "chat_messages"]

    @classmethod
    def get_table_count(cls) -> int:
        """Get total number of tables in schema"""
        return len(cls.get_table_names())

    @classmethod
    def verify_schema(cls, cursor) -> dict:
        """
        Verify that all tables and indexes exist in the database

        Args:
            cursor: Database cursor object

        Returns:
            dict: Verification results with table and index status
        """
        results = {"tables": {}, "indexes": {}, "all_valid": True}

        # Check tables
        for table_name in cls.get_table_names():
            cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            exists = cursor.fetchone() is not None
            results["tables"][table_name] = exists
            if not exists:
                results["all_valid"] = False
                logger.warning(f"Table missing: {table_name}")

        # Check indexes (just count them)
        total_expected_indexes = len(cls.get_financial_indexes_sql()) + len(
            cls.get_chat_indexes_sql()
        )
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
        actual_indexes = cursor.fetchone()[0]
        results["indexes"]["expected"] = total_expected_indexes
        results["indexes"]["actual"] = actual_indexes
        results["indexes"]["all_created"] = actual_indexes >= total_expected_indexes

        return results


# Convenience function for backward compatibility
def initialize_database_schema(cursor, commit_func=None):
    """
    Initialize database schema (convenience function)

    Args:
        cursor: Database cursor object
        commit_func: Optional function to commit changes

    Returns:
        int: Number of tables created
    """
    return DatabaseSchema.initialize_schema(cursor, commit_func)
