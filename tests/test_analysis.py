"""Unit tests for the pure analysis functions."""

from __future__ import annotations

import pandas as pd

from superstore.analysis import (
    aggregate_sum,
    analyze,
    column_average,
    column_total,
    missing_value_counts,
)
from superstore.config import Columns


def _sample_frame() -> pd.DataFrame:
    """A tiny dataset with distinct regional totals (no ties)."""
    return pd.DataFrame(
        {
            "Sales": [100.0, 200.0, 300.0, 50.0],
            "Profit": [10.0, -5.0, 20.0, 15.0],
            "Region": ["West", "East", "West", "South"],
        }
    )


def test_column_total_sums_column():
    assert column_total(_sample_frame(), "Sales") == 650.0


def test_column_average_returns_mean():
    assert column_average(_sample_frame(), "Profit") == 10.0


def test_aggregate_sum_is_sorted_descending():
    result = aggregate_sum(_sample_frame(), "Region", "Sales")
    assert list(result.index) == ["West", "East", "South"]
    assert result.iloc[0] == 400.0


def test_missing_value_counts_detects_gaps():
    frame = _sample_frame()
    frame.loc[0, "Profit"] = None
    assert missing_value_counts(frame)["Profit"] == 1
    assert missing_value_counts(frame)["Sales"] == 0


def test_analyze_bundles_all_metrics():
    result = analyze(_sample_frame(), Columns())
    assert result.row_count == 4
    assert result.column_count == 3
    assert result.total_sales == 650.0
    assert result.average_profit == 10.0
    assert result.top_region == "West"
    assert result.top_region_sales == 400.0
