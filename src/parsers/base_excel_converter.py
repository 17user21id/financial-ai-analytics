"""
Base Excel Converter
Shared functionality for JSON to Excel converters
"""

import json
from typing import Dict, List, Any, Set
from abc import ABC, abstractmethod

# openpyxl is required at runtime for Excel output. We import it lazily-friendly,
# but fail fast with a clear error the moment Excel creation is attempted.
try:
    from openpyxl import Workbook  # type: ignore
except ImportError:  # pragma: no cover - environment specific
    Workbook = None  # type: ignore[assignment]


def _require_openpyxl():
    """Ensure openpyxl is available before attempting Excel operations."""
    if Workbook is None:
        raise ImportError(
            "openpyxl is required to export Excel files. Please install openpyxl."
        )


def _create_workbook():
    """Create and return a new openpyxl Workbook instance."""
    _require_openpyxl()
    return Workbook()


def _write_headers(sheet, headers: List[str]) -> None:
    """Write a header row (row=1) with the provided column names."""
    for i, header in enumerate(headers, start=1):
        sheet.cell(row=1, column=i, value=header)


class BaseJsonToExcelConverter(ABC):
    """
    Base class for JSON to Excel converters
    Provides shared functionality for both dataset converters
    """

    def __init__(self):
        self.category_paths: Set[str] = set()

    @abstractmethod
    def convert_to_excel(self, input_json_path: str, output_excel_path: str) -> str:
        """Convert JSON file to Excel format"""
        pass

    def _get_sub_type(self, group: str, sub_category: str = None) -> str:
        """
        Determine sub_type based on group and subCategory
        Override in subclasses for specific logic
        """
        key = group.lower()
        type_str = self.account_type_map.get(key, "derived")

        if type_str == "revenue":
            if key == "other_income" or (
                sub_category and "non" in sub_category.lower()
            ):
                return "non_operating"
            return "operating"
        elif type_str == "expense":
            if key == "other_expenses" or (
                sub_category
                and (
                    "non" in sub_category.lower()
                    or sub_category
                    in ["revenue_stream_51", "revenue_stream_52", "tax_expense_53"]
                )
            ):
                return "non_operating"
            return "operating"
        elif type_str == "derived":
            return self.derived_subtype_map.get(key)

        return None

    def _validate_is_derived(self, group: str, type_str: str) -> bool:
        """Validate if is_derived is correct based on group and type"""
        should_be_derived = (
            type_str == "derived" or group.lower() in self.derived_subtype_map
        )
        is_derived = type_str == "derived" or group.lower() in self.derived_subtype_map
        return should_be_derived == is_derived

    def _has_child_paths(self, category_path: str) -> bool:
        """Check if the category_path has child paths"""
        for path in self.category_paths:
            if path.startswith(category_path + " > ") and path != category_path:
                return True
        return False

    def _create_metadata(self, path: List[str]) -> str:
        """Create metadata as a JSON object with category1, category2, etc., and hierarchy_level"""
        metadata = {}
        hierarchy = []
        for i, category in enumerate(path):
            if category:
                metadata[f"category{i+1}"] = category
                hierarchy.append(category)
        metadata["hierarchy"] = hierarchy
        metadata["hierarchy_level"] = len(path)
        return json.dumps(metadata)

    @property
    @abstractmethod
    def account_type_map(self) -> Dict[str, str]:
        """Account type mapping - must be implemented by subclasses"""
        pass

    @property
    @abstractmethod
    def derived_subtype_map(self) -> Dict[str, str]:
        """Derived subtype mapping - must be implemented by subclasses"""
        pass
