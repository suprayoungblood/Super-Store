"""Terminal reporting (the presentation layer for the console).

These functions turn an :class:`~superstore.analysis.AnalysisResult` and the
raw frame into the human-readable output a student screenshots for the report.
Formatting helpers are shared so currency and section headers stay consistent.
"""

from __future__ import annotations

import pandas as pd

from .analysis import AnalysisResult, summary_statistics
from .config import Columns

_RULE_WIDTH = 60


def format_currency(value: float) -> str:
    """Format a number as a USD currency string with thousands separators."""
    return f"${value:,.2f}"


def print_section(title: str) -> None:
    """Print a titled section divider."""
    print(f"\n{'=' * _RULE_WIDTH}\n{title}\n{'=' * _RULE_WIDTH}")


def report_environment(versions: dict[str, str]) -> None:
    """Print the installed library versions (the verification step)."""
    print_section("Installed Library Versions")
    for label, version in versions.items():
        print(f"{label} version: {version}")


def report_overview(frame: pd.DataFrame, result: AnalysisResult) -> None:
    """Print dataset shape, a preview, structure, and statistics."""
    print_section("Dataset Overview")
    print(f"Rows: {result.row_count:,}   Columns: {result.column_count}")
    print("\nFirst 5 rows:")
    print(frame.head())
    print("\nStructure (info):")
    frame.info()
    print("\nSummary statistics:")
    print(summary_statistics(frame))


def report_missing_values(result: AnalysisResult) -> None:
    """Print missing-value counts, highlighting only affected columns."""
    print_section("Missing Values")
    affected = {name: count for name, count in result.missing_values.items() if count}
    if not affected:
        print("No missing values found.")
        return
    for name, count in affected.items():
        print(f"{name}: {count:,}")


def report_metrics(result: AnalysisResult, columns: Columns) -> None:
    """Print the headline totals and averages."""
    print_section("Basic Analysis")
    print(f"Total {columns.sales}: {format_currency(result.total_sales)}")
    print(f"Average {columns.profit}: {format_currency(result.average_profit)}")


def report_sales_by_region(result: AnalysisResult, columns: Columns) -> None:
    """Print total sales per region, ranked high to low."""
    print_section(columns.sales_by_region_title)
    for region, sales in result.sales_by_region.items():
        print(f"{region:<12} {format_currency(float(sales))}")


def print_full_report(
    frame: pd.DataFrame,
    result: AnalysisResult,
    versions: dict[str, str],
    columns: Columns,
) -> None:
    """Print the complete terminal report in activity-guide order."""
    report_environment(versions)
    report_overview(frame, result)
    report_missing_values(result)
    report_metrics(result, columns)
    report_sales_by_region(result, columns)
