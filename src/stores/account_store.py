"""
Account Store
Handles all account-related database operations
"""

import sqlite3
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AccountStoreInterface(ABC):
    """Abstract interface for account store operations"""

    @abstractmethod
    def create_account(self, account_data: Dict[str, Any]) -> int:
        """Create a new account and return account_id"""
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        pass

    @abstractmethod
    def get_account_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get account by name"""
        pass

    @abstractmethod
    def get_account_by_composite_key(
        self, name: str, category_path: str, account_type: int, sub_type: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Get account by composite key (name, category_path, type, sub_type)"""
        pass

    @abstractmethod
    def get_accounts_by_type(
        self, account_type: int, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get accounts filtered by type"""
        pass

    @abstractmethod
    def search_accounts(self, search_term: str) -> List[Dict[str, Any]]:
        """Search accounts by name or description"""
        pass

    @abstractmethod
    def get_all_accounts(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get all accounts"""
        pass

    @abstractmethod
    def update_account(self, account_id: int, account_data: Dict[str, Any]) -> bool:
        """Update account"""
        pass

    @abstractmethod
    def delete_account(self, account_id: int) -> bool:
        """Delete account"""
        pass

    @abstractmethod
    def get_accounts_count(self) -> int:
        """Get total count of accounts"""
        pass


class SQLiteAccountStore(AccountStoreInterface):
    """SQLite implementation of account store"""

    def __init__(self, connection_factory):
        """
        Initialize with a connection factory function

        Args:
            connection_factory: Function that returns a database connection
        """
        self.get_connection = connection_factory
        logger.info("Initialized SQLiteAccountStore")

    def create_account(self, account_data: Dict[str, Any]) -> int:
        """Create a new account and return account_id"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO accounts 
                (name, category_path, sub_category, type, sub_type, is_summary, 
                 is_derived, description, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    account_data.get("name"),
                    account_data.get("category_path"),
                    account_data.get("sub_category"),
                    account_data.get("type"),
                    account_data.get("sub_type"),
                    account_data.get("is_summary", False),
                    account_data.get("is_derived", False),
                    account_data.get("description", ""),
                    account_data.get("is_active", True),
                ),
            )

            account_id = cursor.lastrowid
            connection.commit()
            logger.info(f"Created account with ID: {account_id}")
            return account_id

        except sqlite3.IntegrityError as e:
            connection.rollback()
            logger.error(f"Account already exists: {e}")
            raise
        except Exception as e:
            connection.rollback()
            logger.error(f"Error creating account: {e}")
            raise

    def get_account_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_id, name, category_path, sub_category, type, sub_type,
                   is_summary, is_derived, description, is_active, 
                   created_at, updated_at
            FROM accounts
            WHERE account_id = ?
        """,
            (account_id,),
        )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_account_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get account by name"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_id, name, category_path, sub_category, type, sub_type,
                   is_summary, is_derived, description, is_active,
                   created_at, updated_at
            FROM accounts
            WHERE name = ?
        """,
            (name,),
        )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_account_by_composite_key(
        self, name: str, category_path: str, account_type: int, sub_type: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Get account by composite key (name, category_path, type, sub_type)"""
        connection = self.get_connection()
        cursor = connection.cursor()

        # Handle NULL sub_type properly
        if sub_type is None:
            cursor.execute(
                """
                SELECT account_id, name, category_path, sub_category, type, sub_type,
                       is_summary, is_derived, description, is_active,
                       created_at, updated_at
                FROM accounts
                WHERE name = ? AND category_path = ? AND type = ? AND sub_type IS NULL
            """,
                (name, category_path, account_type),
            )
        else:
            cursor.execute(
                """
                SELECT account_id, name, category_path, sub_category, type, sub_type,
                       is_summary, is_derived, description, is_active,
                       created_at, updated_at
                FROM accounts
                WHERE name = ? AND category_path = ? AND type = ? AND sub_type = ?
            """,
                (name, category_path, account_type, sub_type),
            )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_accounts_by_type(
        self, account_type: int, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get accounts filtered by type"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_id, name, category_path, sub_category, type, sub_type,
                   is_summary, is_derived, description, is_active,
                   created_at, updated_at
            FROM accounts
            WHERE type = ?
            ORDER BY name
            LIMIT ?
        """,
            (account_type, limit),
        )

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def search_accounts(self, search_term: str) -> List[Dict[str, Any]]:
        """Search accounts by name or description"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_id, name, category_path, sub_category, type, sub_type,
                   is_summary, is_derived, description, is_active,
                   created_at, updated_at
            FROM accounts
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY name
            LIMIT 50
        """,
            (f"%{search_term}%", f"%{search_term}%"),
        )

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def get_all_accounts(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get all accounts"""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT account_id, name, category_path, sub_category, type, sub_type,
                   is_summary, is_derived, description, is_active,
                   created_at, updated_at
            FROM accounts
            ORDER BY name
        """

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query)

        results = []
        for row in cursor.fetchall():
            results.append(dict(row))

        return results

    def update_account(self, account_id: int, account_data: Dict[str, Any]) -> bool:
        """Update account"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            params = []

            for field in [
                "name",
                "category_path",
                "sub_category",
                "type",
                "sub_type",
                "is_summary",
                "is_derived",
                "description",
                "is_active",
            ]:
                if field in account_data:
                    update_fields.append(f"{field} = ?")
                    params.append(account_data[field])

            if not update_fields:
                logger.warning("No fields to update")
                return False

            # Add updated_at timestamp
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            params.append(account_id)

            query = (
                f"UPDATE accounts SET {', '.join(update_fields)} WHERE account_id = ?"
            )
            cursor.execute(query, params)

            connection.commit()
            updated = cursor.rowcount > 0

            if updated:
                logger.info(f"Updated account with ID: {account_id}")
            else:
                logger.warning(f"No account found with ID: {account_id}")

            return updated

        except Exception as e:
            connection.rollback()
            logger.error(f"Error updating account: {e}")
            raise

    def delete_account(self, account_id: int) -> bool:
        """Delete account"""
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
            connection.commit()
            deleted = cursor.rowcount > 0

            if deleted:
                logger.info(f"Deleted account with ID: {account_id}")
            else:
                logger.warning(f"No account found with ID: {account_id}")

            return deleted

        except sqlite3.IntegrityError as e:
            connection.rollback()
            logger.error(f"Cannot delete account (foreign key constraint): {e}")
            raise
        except Exception as e:
            connection.rollback()
            logger.error(f"Error deleting account: {e}")
            raise

    def get_accounts_count(self) -> int:
        """Get total count of accounts"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM accounts")
        count = cursor.fetchone()[0]

        return count


class InMemoryAccountStore(SQLiteAccountStore):
    """In-memory implementation of account store (inherits from SQLiteAccountStore)"""

    def __init__(self, connection_factory):
        super().__init__(connection_factory)
        logger.info("Initialized InMemoryAccountStore")
