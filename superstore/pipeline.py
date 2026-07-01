"""Orchestration: wire the modules into the end-to-end analytics workflow.

:func:`run_pipeline` performs the activity in order (load, analyze, report,
visualize, and optionally build the PowerPoint deck), delegating each step to a
focused module so this file stays a thin coordinator.
"""

from __future__ import annotations

from pathlib import Path

from .analysis import AnalysisResult, analyze
from .config import AppConfig
from .data_loader import load_dataset
from .deck import build_deck
from .environment import library_versions
from .reporting import print_full_report
from .visualization import render_bar_chart


def run_pipeline(
    config: AppConfig, *, show: bool = False, make_deck: bool = False
) -> AnalysisResult:
    """Run the full analytics workflow.

    Args:
        config: Application configuration.
        show: When ``True``, display the chart interactively.
        make_deck: When ``True``, also generate the PowerPoint report.

    Returns:
        The computed :class:`~superstore.analysis.AnalysisResult`.
    """
    versions = library_versions()
    frame = load_dataset(config)
    result = analyze(frame, config.columns)

    print_full_report(frame, result, versions, config.columns)

    chart_path = _render_chart(result, config, show=show)
    print(f"\nChart saved to: {chart_path}")

    if make_deck:
        deck_path = build_deck(result, versions, config)
        print(f"Deck saved to: {deck_path}")

    return result


def _render_chart(result: AnalysisResult, config: AppConfig, *, show: bool) -> Path:
    """Render the 'Total Sales by Region' bar chart."""
    columns = config.columns
    return render_bar_chart(
        result.sales_by_region,
        title=columns.sales_by_region_title,
        xlabel=columns.region,
        ylabel=f"Total {columns.sales}",
        output_path=config.paths.chart_file,
        style=config.chart,
        show=show,
    )
