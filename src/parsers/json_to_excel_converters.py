"""
JSON to Excel Converters
Convenience functions for converting JSON files to Excel format
"""

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


def _write_headers(sheet, headers: list) -> None:
    """Write a header row (row=1) with the provided column names."""
    for i, header in enumerate(headers, start=1):
        sheet.cell(row=1, column=i, value=header)


# Convenience functions
def convert_rootfi_to_excel(input_json_path: str, output_excel_path: str) -> str:
    """Convert data_set_1.json to Excel format"""
    from .rootfi_excel_converter import JsonToExcelConverterRootfi

    converter = JsonToExcelConverterRootfi()
    return converter.convert_to_excel(input_json_path, output_excel_path)


def convert_pl_to_excel(input_json_path: str, output_excel_path: str) -> str:
    """Convert data_set_2.json to Excel format"""
    from .pl_excel_converter import JsonToExcelConverterPL

    converter = JsonToExcelConverterPL()
    return converter.convert_to_excel(input_json_path, output_excel_path)
