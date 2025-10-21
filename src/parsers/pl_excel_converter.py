"""
P&L JSON to Excel Converter
Convert data_set_2.json (P&L Report format) to Excel
Based on Java JsonToExcelConverterPL implementation
"""

import json
from typing import Dict, List, Any
from .base_excel_converter import (
    BaseJsonToExcelConverter,
    _create_workbook,
    _write_headers,
)


class JsonToExcelConverterPL(BaseJsonToExcelConverter):
    """
    Converter for data_set_2.json (P&L Report format) to Excel
    Based on Java JsonToExcelConverterPL implementation
    """

    def __init__(self):
        super().__init__()

        # Map JSON keys to AccountType (string values)
        self._account_type_map = {
            "revenue": "revenue",
            "cost_of_goods_sold": "cogs",
            "operating_expenses": "expense",
            "non_operating_expenses": "expense",
            "tax": "tax",
            "derived": "derived",
            "gross_profit": "derived",
            "operating_profit": "derived",
            "ebitda": "derived",
            "non_operating_income": "derived",
            "profit_before_tax": "derived",
            "net_profit": "derived",
            "other": "derived",
            "non_operating_revenue": "revenue",
        }

        # Map JSON keys to DerivedSubType for type="derived" (string values)
        self._derived_subtype_map = {
            "gross_profit": "gross_profit",
            "operating_profit": "operating_profit",
            "ebitda": "ebitda",
            "non_operating_income": "non_operating_income",
            "profit_before_tax": "profit_before_tax",
            "net_profit": "net_profit",
            "other": "other",
        }

        # Store all category paths for the current period
        self.period_category_paths: set = set()

    @property
    def account_type_map(self) -> Dict[str, str]:
        return self._account_type_map

    @property
    def derived_subtype_map(self) -> Dict[str, str]:
        return self._derived_subtype_map

    def convert_to_excel(self, input_json_path: str, output_excel_path: str) -> str:
        """
        Convert data_set_2.json to Excel format

        Args:
            input_json_path: Path to input JSON file
            output_excel_path: Path to output Excel file

        Returns:
            Path to created Excel file
        """
        try:
            with open(input_json_path, "r") as f:
                data = json.load(f)

            data_array = data["data"]

            # Create workbook
            workbook = _create_workbook()

            for period_data in data_array:
                period_start = period_data["period_start"]
                period_end = period_data["period_end"]
                period_name = f"{period_start} to {period_end}"

                # Create sheet for this period
                sheet = workbook.create_sheet(period_name)

                # Header row
                headers = [
                    "account_id",
                    "name",
                    "category_path",
                    "sub_category",
                    "type",
                    "sub_type",
                    "is_summary",
                    "is_derived",
                    "is_derived_correct",
                    "metadata",
                    "value",
                ]
                _write_headers(sheet, headers)

                # Clear category paths for the current period
                self.period_category_paths.clear()

                # First pass: collect all category paths
                self._collect_category_paths(period_data)

                # Second pass: process fields for Excel output
                current_row = 2
                for key, value in period_data.items():
                    if key in [
                        "period_start",
                        "period_end",
                        "rootfi_id",
                        "rootfi_company_id",
                    ]:
                        continue

                    if isinstance(value, list):
                        current_row = self._flatten_section(
                            value, sheet, current_row, key, [key]
                        )
                    elif isinstance(value, (int, float)):
                        current_row = self._add_summary_row(
                            sheet, current_row, key, value, [key]
                        )

            # Remove default sheet
            if "Sheet" in workbook.sheetnames:
                workbook.remove(workbook["Sheet"])

            # Save workbook
            workbook.save(output_excel_path)

            return output_excel_path

        except Exception as e:
            raise

    def _collect_category_paths(self, period_data: Dict):
        """Collect all category paths for the current period"""
        for key, value in period_data.items():
            if key in ["period_start", "period_end", "rootfi_id", "rootfi_company_id"]:
                continue

            if isinstance(value, list):
                self._collect_section_paths(value, key, [key])
            elif isinstance(value, (int, float)):
                self.period_category_paths.add(key)

    def _collect_section_paths(
        self, section: List[Dict], main_category: str, path: List[str]
    ):
        """Collect category paths from a section"""
        for category in section:
            cat_name = category["name"]
            new_path = path + [cat_name]
            category_path = " > ".join(new_path)
            self.period_category_paths.add(category_path)

            if "line_items" in category and category["line_items"]:
                self._collect_line_item_paths(
                    category["line_items"], main_category, new_path
                )

    def _collect_line_item_paths(
        self, line_items: List[Dict], main_category: str, path: List[str]
    ):
        """Collect category paths from line_items"""
        for item in line_items:
            sub_name = item["name"]
            new_path = path + [sub_name]
            category_path = " > ".join(new_path)
            self.period_category_paths.add(category_path)

            if "line_items" in item and item["line_items"]:
                self._collect_line_item_paths(
                    item["line_items"], main_category, new_path
                )

    def _flatten_section(
        self,
        section: List[Dict],
        sheet,
        start_row: int,
        main_category: str,
        path: List[str],
    ) -> int:
        """Process a section (array of categories with line_items)"""
        for category in section:
            cat_name = category["name"]
            new_path = path + [cat_name]

            if "line_items" not in category or not category["line_items"]:
                # No line_items: treat as summary if it has child paths
                start_row = self._add_summary_row(
                    sheet, start_row, main_category, category["value"], new_path
                )
            else:
                # Has line_items: process children only
                start_row = self._flatten_line_items(
                    category["line_items"], sheet, start_row, main_category, new_path
                )

        return start_row

    def _flatten_line_items(
        self,
        line_items: List[Dict],
        sheet,
        start_row: int,
        main_category: str,
        path: List[str],
    ) -> int:
        """Flatten line_items recursively, adding rows for child items"""
        for item in line_items:
            sub_name = item["name"]
            sub_value = item["value"]
            account_id = item.get("account_id", "")
            new_path = path + [sub_name]

            # Add row for this line_item
            category_path = " > ".join(new_path)
            name = path[1] if len(path) >= 1 else sub_name
            type_str = self.account_type_map.get(main_category.lower(), "derived")
            sub_type = self._get_sub_type(main_category, sub_name)
            is_summary = self._has_child_paths(category_path)
            is_derived = (
                type_str == "derived"
                or main_category.lower() in self.derived_subtype_map
            )
            is_derived_correct = self._validate_is_derived(main_category, type_str)
            metadata = self._create_metadata(new_path)

            # Add row data
            sheet.cell(row=start_row, column=1, value=account_id)
            sheet.cell(row=start_row, column=2, value=name)
            sheet.cell(row=start_row, column=3, value=category_path)
            sheet.cell(row=start_row, column=4, value=sub_name)
            sheet.cell(row=start_row, column=5, value=type_str)
            sheet.cell(row=start_row, column=6, value=sub_type)
            sheet.cell(row=start_row, column=7, value=is_summary)
            sheet.cell(row=start_row, column=8, value=is_derived)
            sheet.cell(row=start_row, column=9, value=is_derived_correct)
            sheet.cell(row=start_row, column=10, value=metadata)
            sheet.cell(row=start_row, column=11, value=sub_value)

            start_row += 1

            # Recurse deeper if needed
            if "line_items" in item and item["line_items"]:
                start_row = self._flatten_line_items(
                    item["line_items"], sheet, start_row, main_category, new_path
                )

        return start_row

    def _add_summary_row(
        self, sheet, row_index: int, main_category: str, value: float, path: List[str]
    ) -> int:
        """Add a summary row for top-level numeric fields or categories without line_items"""
        category_path = " > ".join(path)
        name = path[1] if len(path) >= 2 else path[0]
        type_str = self.account_type_map.get(main_category.lower(), "derived")
        sub_type = self._get_sub_type(main_category, None)
        is_summary = self._has_child_paths(category_path)
        is_derived = (
            type_str == "derived" or main_category.lower() in self.derived_subtype_map
        )
        is_derived_correct = self._validate_is_derived(main_category, type_str)
        metadata = self._create_metadata(path)

        # Add row data
        sheet.cell(row=row_index, column=1, value="")  # No account_id
        sheet.cell(row=row_index, column=2, value=name)
        sheet.cell(row=row_index, column=3, value=category_path)
        sheet.cell(row=row_index, column=4, value="")  # No sub_category
        sheet.cell(row=row_index, column=5, value=type_str)
        sheet.cell(row=row_index, column=6, value=sub_type)
        sheet.cell(row=row_index, column=7, value=is_summary)
        sheet.cell(row=row_index, column=8, value=is_derived)
        sheet.cell(row=row_index, column=9, value=is_derived_correct)
        sheet.cell(row=row_index, column=10, value=metadata)
        sheet.cell(row=row_index, column=11, value=value)

        return row_index + 1

    def _has_child_paths(self, category_path: str) -> bool:
        """Check if the category_path has child paths in the period"""
        for path in self.period_category_paths:
            if path.startswith(category_path + " > ") and path != category_path:
                return True
        return False
