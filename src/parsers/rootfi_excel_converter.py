"""
Rootfi JSON to Excel Converter
Convert data_set_1.json (Rootfi Report format) to Excel
Based on Java JsonToExcelConverterRootfi implementation
"""

import json
from typing import Dict, List, Any
from .base_excel_converter import (
    BaseJsonToExcelConverter,
    _create_workbook,
    _write_headers,
)


class JsonToExcelConverterRootfi(BaseJsonToExcelConverter):
    """
    Converter for data_set_1.json (Rootfi Report format) to Excel
    Based on Java JsonToExcelConverterRootfi implementation
    """

    def __init__(self):
        super().__init__()

        # Map JSON keys to AccountType (string values)
        self._account_type_map = {
            # Income -> revenue
            "income": "revenue",
            "revenue_stream_5": "revenue",
            "operations_expense_6": "revenue",
            "revenue_stream_7": "revenue",
            "product_revenue_4": "revenue",
            "service_division_3": "revenue",
            "revenue_stream_1": "revenue",
            # COGS -> cogs
            "cogs": "cogs",
            "expense_category_8": "cogs",
            "labor_expense_9": "cogs",
            "labor_expense_55": "cogs",
            "labor_expense_56": "cogs",
            "material_cost_10": "cogs",
            "material_cost_11": "cogs",
            "material_cost_12": "cogs",
            "shipping_expense_13": "cogs",
            "technology_expense_14": "cogs",
            "expense_category_54": "cogs",
            # Expenses -> expense
            "expenses": "expense",
            "revenue_stream_15": "expense",
            "revenue_stream_16": "expense",
            "marketing_expense_17": "expense",
            "marketing_expense_18": "expense",
            "marketing_expense_19": "expense",
            "labor_expense_20": "expense",
            "labor_expense_21": "expense",
            "labor_expense_22": "expense",
            "labor_expense_23": "expense",
            "labor_expense_24": "expense",
            "labor_expense_25": "expense",
            "labor_expense_26": "expense",
            "labor_expense_27": "expense",
            "labor_expense_64": "expense",
            "technology_expense_28": "expense",
            "professional_fee_29": "expense",
            "professional_fee_30": "expense",
            "professional_fee_31": "expense",
            "professional_fee_32": "expense",
            "professional_fee_33": "expense",
            "travel_expense_34": "expense",
            "meal_expense_35": "expense",
            "entertainment_expense_36": "expense",
            "insurance_expense_37": "expense",
            "equipment_expense_38": "expense",
            "office_expense_39": "expense",
            "communication_expense_40": "expense",
            "utility_expense_41": "expense",
            "banking_expense_42": "expense",
            "facility_cost_43": "expense",
            "shipping_expense_60": "expense",
            "facility_cost_63": "expense",
            "facility_cost_65": "expense",
            "facility_cost_66": "expense",
            "facility_cost_67": "expense",
            "rd_expense_44": "expense",
            "rd_labor_expense_45": "expense",
            "rd_labor_expense_57": "expense",
            "rd_labor_expense_58": "expense",
            "rd_contractor_fee_62": "expense",
            "rd_equipment_46": "expense",
            "rd_supplies_47": "expense",
            "rd_expense_48": "expense",
            "operating_expense_49": "expense",
            "depreciation_expense_50": "expense",
            "material_cost_59": "expense",
            "expense_category_2": "expense",
            # OtherIncome -> revenue
            "other_income": "revenue",
            "revenue_stream_61": "revenue",
            # OtherExpenses -> expense
            "other_expenses": "expense",
            "revenue_stream_51": "expense",
            "revenue_stream_52": "expense",
            "tax_expense_53": "expense",
            # Derived types
            "gross_profit": "derived",
            "operating_profit": "derived",
            "ebitda": "derived",
            "non_operating_income": "derived",
            "profit_before_tax": "derived",
            "net_profit": "derived",
            "other": "derived",
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

    @property
    def account_type_map(self) -> Dict[str, str]:
        return self._account_type_map

    @property
    def derived_subtype_map(self) -> Dict[str, str]:
        return self._derived_subtype_map

    def convert_to_excel(self, input_json_path: str, output_excel_path: str) -> str:
        """
        Convert data_set_1.json to Excel format

        Args:
            input_json_path: Path to input JSON file
            output_excel_path: Path to output Excel file

        Returns:
            Path to created Excel file
        """
        try:
            with open(input_json_path, "r") as f:
                data = json.load(f)

            data_section = data["data"]
            columns = data_section["Columns"]["Column"]
            rows = data_section["Rows"]["Row"]

            original_num_cols = len(columns)

            # Create workbook and sheet
            workbook = _create_workbook()
            sheet = workbook.active
            sheet.title = "Rootfi Report"

            # Create header row
            fixed_headers = [
                "name",
                "category_path",
                "sub_category",
                "type",
                "sub_type",
                "is_summary",
                "is_derived",
                "is_derived_correct",
                "metadata",
            ]
            _write_headers(sheet, fixed_headers)
            col_index = len(fixed_headers)

            # Add monthly columns
            for i, col in enumerate(columns):
                title = col["ColTitle"]
                sheet.cell(row=1, column=col_index + 1, value=title)
                col_index += 1

            # Add computed columns
            sheet.cell(row=1, column=col_index + 1, value="Computed Total")
            col_index += 1
            sheet.cell(row=1, column=col_index + 1, value="Difference")

            # First pass: collect all category paths
            self.category_paths.clear()
            self._collect_category_paths(rows, [])

            # Second pass: flatten rows and populate data
            row_index = 2
            row_index = self._flatten_rows(
                rows, sheet, row_index, original_num_cols, []
            )

            # Save workbook
            workbook.save(output_excel_path)

            return output_excel_path

        except Exception as e:
            raise

    def _collect_category_paths(self, rows_node: List[Dict], path: List[str]):
        """Collect all category paths for determining is_summary"""
        for row_node in rows_node:
            group = row_node.get("group", "")
            type_str = self.account_type_map.get(group.lower(), "derived")
            new_path = path + [group]
            category_path = type_str + (" > " + " > ".join(new_path) if group else "")
            if group:
                self.category_paths.add(category_path)

            if "Rows" in row_node:
                self._collect_category_paths(row_node["Rows"]["Row"], new_path)

    def _flatten_rows(
        self,
        rows_node: List[Dict],
        sheet,
        current_row_index: int,
        original_num_cols: int,
        path: List[str],
    ) -> int:
        """Recursively flatten the nested Rows, including Header, Summary, and ColData rows"""
        for row_node in rows_node:
            group = row_node.get("group", "")
            new_path = path + [group]
            type_str = self.account_type_map.get(group.lower(), "derived")
            category_path = type_str + (" > " + " > ".join(new_path) if group else "")

            if "Header" in row_node or "Summary" in row_node:
                # Handle Header or Summary row
                col_data = (
                    row_node.get("Header", {}).get("ColData", [])
                    if "Header" in row_node
                    else row_node.get("Summary", {}).get("ColData", [])
                )
                if col_data:
                    group = col_data[0]["value"]
                    new_path[-1] = group
                    type_str = self.account_type_map.get(group.lower(), "derived")
                    category_path = type_str + (
                        " > " + " > ".join(new_path) if group else ""
                    )
                    current_row_index = self._add_row(
                        sheet,
                        current_row_index,
                        original_num_cols,
                        group,
                        new_path,
                        category_path,
                        col_data,
                        True,
                    )
            elif "ColData" in row_node:
                # Handle ColData (detail) row
                col_data = row_node["ColData"]
                if col_data:
                    group = col_data[0]["value"]
                    new_path[-1] = group
                    type_str = self.account_type_map.get(group.lower(), "derived")
                    category_path = type_str + (
                        " > " + " > ".join(new_path) if group else ""
                    )
                    current_row_index = self._add_row(
                        sheet,
                        current_row_index,
                        original_num_cols,
                        group,
                        new_path,
                        category_path,
                        col_data,
                        False,
                    )

            # Recurse into sub-rows if present
            if "Rows" in row_node:
                current_row_index = self._flatten_rows(
                    row_node["Rows"]["Row"],
                    sheet,
                    current_row_index,
                    original_num_cols,
                    new_path,
                )

        return current_row_index

    def _add_row(
        self,
        sheet,
        row_index: int,
        original_num_cols: int,
        group: str,
        path: List[str],
        category_path: str,
        col_data: List[Dict],
        is_header_or_summary: bool,
    ) -> int:
        """Add a row to the sheet with all columns"""
        name = group
        sub_category = "" if is_header_or_summary else group
        type_str = self.account_type_map.get(group.lower(), "derived")
        sub_type = self._get_sub_type(group, sub_category)
        is_summary = is_header_or_summary or self._has_child_paths(category_path)
        is_derived = type_str == "derived" or group.lower() in self.derived_subtype_map
        is_derived_correct = self._validate_is_derived(group, type_str)
        metadata = self._create_metadata(path)

        # Fixed columns
        sheet.cell(row=row_index, column=1, value=name)
        sheet.cell(row=row_index, column=2, value=category_path)
        sheet.cell(row=row_index, column=3, value=sub_category)
        sheet.cell(row=row_index, column=4, value=type_str)
        sheet.cell(row=row_index, column=5, value=sub_type)
        sheet.cell(row=row_index, column=6, value=is_summary)
        sheet.cell(row=row_index, column=7, value=is_derived)
        sheet.cell(row=row_index, column=8, value=is_derived_correct)
        sheet.cell(row=row_index, column=9, value=metadata)

        # Monthly columns, Computed Total, Difference
        sum_val = 0.0
        for i in range(min(original_num_cols, len(col_data))):
            cell_node = col_data[i]
            val = cell_node["value"]
            try:
                num_val = float(val)
                sheet.cell(row=row_index, column=10 + i, value=num_val)
                if 1 <= i < original_num_cols - 1:
                    sum_val += num_val
            except ValueError:
                sheet.cell(row=row_index, column=10 + i, value=val)

        # Computed Total
        sheet.cell(row=row_index, column=10 + original_num_cols, value=sum_val)

        # Difference
        total_cell = sheet.cell(row=row_index, column=10 + original_num_cols - 1)
        existing_total = 0.0
        if total_cell.value is not None and isinstance(total_cell.value, (int, float)):
            existing_total = total_cell.value
        sheet.cell(
            row=row_index,
            column=10 + original_num_cols + 1,
            value=existing_total - sum_val,
        )

        return row_index + 1
