"""Pure analysis functions for the Superstore dataset.

Each function is small, side-effect free, and parameterized by column name so
the same logic works for any numeric column. :func:`analyze` composes them into
a single immutable :class:`AnalysisResult` that the reporting and deck layers
consume.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import Columns


@dataclass(frozen=True)
class AnalysisResult:
    """Immutable bundle of the metrics produced from the dataset."""

    row_count: int
    column_count: int
    total_sales: float
    average_profit: float
    sales_by_region: pd.Series
    missing_values: dict[str, int]

    @property
    def top_region(self) -> str:
        """Name of the region with the highest total sales."""
        return str(self.sales_by_region.index[0])

    @property
    def top_region_sales(self) -> float:
        """Total sales for the highest-selling region."""
        return float(self.sales_by_region.iloc[0])


def column_total(frame: pd.DataFrame, column: str) -> float:
    """Return the sum of a numeric column."""
    return float(frame[column].sum())


def column_average(frame: pd.DataFrame, column: str) -> float:
    """Return the mean of a numeric column."""
    return float(frame[column].mean())


def aggregate_sum(frame: pd.DataFrame, group_column: str, value_column: str) -> pd.Series:
    """Sum ``value_column`` per ``group_column``, sorted high to low."""
    grouped = frame.groupby(group_column)[value_column].sum()
    return grouped.sort_values(ascending=False)


def missing_value_counts(frame: pd.DataFrame) -> dict[str, int]:
    """Return the number of missing values per column."""
    counts = frame.isna().sum()
    return {str(column): int(total) for column, total in counts.items()}


def summary_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for the numeric columns."""
    return frame.describe()


def analyze(frame: pd.DataFrame, columns: Columns) -> AnalysisResult:
    """Compute every headline metric for the dataset.

    Args:
        frame: The loaded Superstore dataset.
        columns: Configured column names to analyze.

    Returns:
        An :class:`AnalysisResult` holding the computed metrics.
    """
    rows, cols = frame.shape
    return AnalysisResult(
        row_count=int(rows),
        column_count=int(cols),
        total_sales=column_total(frame, columns.sales),
        average_profit=column_average(frame, columns.profit),
        sales_by_region=aggregate_sum(frame, columns.region, columns.sales),
        missing_values=missing_value_counts(frame),
    )
