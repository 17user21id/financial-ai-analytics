"""
Data Sync Handler
Handles all data synchronization business logic
"""

import logging
from typing import Dict, Any, List, Tuple
from pathlib import Path

from ..parsers import import_excel_to_database
from .financial_handler import FinancialDataHandler
from ..models.query_models import SyncResponse

logger = logging.getLogger(__name__)


class DataSyncHandler:
    """
    Handler for data synchronization operations

    This class contains all the business logic for syncing Excel data
    and should be used by API endpoints to keep them thin.
    """

    def __init__(self):
        self.financial_handler = FinancialDataHandler()

    def _process_excel_file(
        self, resources_folder: Path, file_pattern: str, source_name: str
    ) -> Dict[str, Any]:
        """
        Helper function to process a single Excel file pattern

        Args:
            resources_folder: Path to resources directory
            file_pattern: Glob pattern for file matching (e.g., "dataset1_output_*.xlsx")
            source_name: Human-readable source name (e.g., "P&L Report")

        Returns:
            Dictionary with processing results
        """
        try:
            files = list(resources_folder.glob(file_pattern))
            if files:
                file_path = files[0]  # Take the first one found
                logger.info(f"Processing {source_name} Excel: {file_path.name}")

                accounts_created, transactions_created = import_excel_to_database(
                    str(file_path)
                )

                result = {
                    "file": file_path.name,
                    "source": source_name,
                    "accounts": accounts_created,
                    "transactions": transactions_created,
                    "success": True,
                }
                logger.info(
                    f"Processed {file_path.name}: {accounts_created} accounts, {transactions_created} transactions"
                )
                return result
            else:
                logger.warning(f"No {file_pattern} files found in resources folder")
                return {
                    "file": file_pattern,
                    "source": source_name,
                    "accounts": 0,
                    "transactions": 0,
                    "success": False,
                    "error": "File not found",
                }

        except Exception as e:
            logger.error(f"Error processing {source_name} Excel: {e}")
            return {
                "file": file_pattern,
                "source": source_name,
                "accounts": 0,
                "transactions": 0,
                "success": False,
                "error": str(e),
            }

    def _get_resources_folder(self) -> Path:
        """
        Get the resources folder path

        Returns:
            Path to the resources directory
        """
        # Get resources directory path relative to this file
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        return project_root / "resources"

    def _get_dataset_configurations(self) -> List[Tuple[str, str]]:
        """
        Get the list of dataset configurations to process

        Returns:
            List of tuples (file_pattern, source_name)
        """
        return [
            ("dataset1_output_*.xlsx", "P&L Report"),
            ("dataset2_output_*.xlsx", "Rootfi Report"),
        ]

    def sync_excel_data(self) -> SyncResponse:
        """
        Synchronously sync data from Excel files to accounts and transactions tables

        Automatically finds and processes:
        - dataset1_output_*.xlsx (P&L Report)
        - dataset2_output_*.xlsx (Rootfi Report)

        Returns:
            SyncResponse with sync results
        """
        try:
            logger.info("Starting Excel data sync")

            # Clear existing data first
            self.financial_handler.db.clear_data()
            logger.info("Cleared existing data")

            total_accounts = 0
            total_transactions = 0
            files_processed = []

            # Get resources directory path
            resources_folder = self._get_resources_folder()

            # Get dataset configurations
            datasets = self._get_dataset_configurations()

            # Process each dataset
            for file_pattern, source_name in datasets:
                result = self._process_excel_file(
                    resources_folder, file_pattern, source_name
                )
                files_processed.append(result)

                if result["success"]:
                    total_accounts += result["accounts"]
                    total_transactions += result["transactions"]

            # Determine success
            successful_files = [f for f in files_processed if f.get("success", False)]
            overall_success = len(successful_files) > 0

            message = f"Excel sync completed: {len(successful_files)}/{len(files_processed)} files processed, {total_accounts} accounts, {total_transactions} transactions"

            logger.info(f"Excel data sync completed: {message}")

            return SyncResponse(
                success=overall_success,
                message=message,
                accounts_created=total_accounts,
                transactions_created=total_transactions,
                total_metrics=total_transactions,  # Using transactions as metrics count
            )

        except Exception as e:
            logger.error(f"Error in Excel data sync: {e}")
            raise
