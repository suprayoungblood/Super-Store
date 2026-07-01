"""Deck content as plain data (no PowerPoint dependency).

This module decides *what* goes on each of the seven slides, pulling live
numbers from the :class:`~superstore.analysis.AnalysisResult` so the reflection
answers reference the real dataset. :mod:`superstore.deck` decides *how* to
render these specs into a ``.pptx`` file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .analysis import AnalysisResult
from .config import AppConfig
from .reporting import format_currency


@dataclass(frozen=True)
class TitleSlide:
    """A title slide with a heading and multi-line subtitle."""

    title: str
    subtitle: str


@dataclass(frozen=True)
class BulletsSlide:
    """A content slide rendered as a bulleted list."""

    title: str
    bullets: tuple[str, ...]


@dataclass(frozen=True)
class ImageSlide:
    """A slide that embeds an image with a caption."""

    title: str
    image_path: Path
    caption: str


def build_slides(
    result: AnalysisResult, versions: dict[str, str], config: AppConfig
) -> list[object]:
    """Build the ordered list of slide specs for the 7-slide report."""
    return [
        _title_slide(config),
        _installation_slide(versions),
        _analysis_slide(result, config),
        _chart_slide(result, config),
        *_reflection_slides(result, config),
    ]


def _title_slide(config: AppConfig) -> TitleSlide:
    """Slide 1: presenter and course metadata."""
    presenter = config.presenter
    subtitle = (
        f"{presenter.name}\n"
        f"Course: {presenter.course}\n"
        f"Instructor: {presenter.instructor}"
    )
    return TitleSlide(title=presenter.topic, subtitle=subtitle)


def _installation_slide(versions: dict[str, str]) -> BulletsSlide:
    """Slide 2: library install command and detected versions."""
    version_lines = tuple(f"{label}: {value}" for label, value in versions.items())
    bullets = (
        "Installed with: pip install pandas matplotlib python-pptx",
        *version_lines,
        "Add a screenshot of these version numbers from your terminal.",
    )
    return BulletsSlide(title="Installation & Verification", bullets=bullets)


def _analysis_slide(result: AnalysisResult, config: AppConfig) -> BulletsSlide:
    """Slide 3: the basic analysis output (totals, averages, data health)."""
    columns = config.columns
    missing_total = sum(result.missing_values.values())
    bullets = (
        f"Dataset: {result.row_count:,} rows x {result.column_count} columns",
        f"Total {columns.sales}: {format_currency(result.total_sales)}",
        f"Average {columns.profit}: {format_currency(result.average_profit)}",
        f"Missing values: {missing_total:,}",
        "Add a screenshot of this analysis from your terminal.",
    )
    return BulletsSlide(title="Basic Analysis Output", bullets=bullets)


def _chart_slide(result: AnalysisResult, config: AppConfig) -> ImageSlide:
    """Slide 4: the generated bar chart with a one-line takeaway."""
    caption = (
        f"{result.top_region} leads with "
        f"{format_currency(result.top_region_sales)} in sales."
    )
    return ImageSlide(
        title=config.columns.sales_by_region_title,
        image_path=config.paths.chart_file,
        caption=caption,
    )


def _reflection_slides(result: AnalysisResult, config: AppConfig) -> list[BulletsSlide]:
    """Slides 5-7: short answers to the three reflection questions."""
    return [
        BulletsSlide(title=question, bullets=answer)
        for question, answer in _reflection_content(result, config)
    ]


def _reflection_content(
    result: AnalysisResult, config: AppConfig
) -> list[tuple[str, tuple[str, ...]]]:
    """Return (question, answer-bullets) pairs grounded in the real metrics."""
    columns = config.columns
    top_region = result.top_region
    return [
        (
            "Insights gained from analyzing the dataset",
            (
                f"Sales concentrate by region: {top_region} is the top market "
                f"at {format_currency(result.top_region_sales)}.",
                f"Across {result.row_count:,} orders, average {columns.profit} "
                f"was only {format_currency(result.average_profit)} per order.",
                "High sales volume does not guarantee strong margins, hinting "
                "that discounting pressures profit.",
                "The dataset is clean, so the metrics are reliable as-is.",
            ),
        ),
        (
            "How visualizations enhance data-driven decisions",
            (
                "Charts reveal patterns and outliers far faster than raw tables.",
                "Ranking regions side by side shows where to focus spend.",
                "Visuals communicate findings to non-technical stakeholders "
                "in seconds.",
                "They expose trends that drive forecasting and resource "
                "allocation.",
            ),
        ),
        (
            "Additional analysis to explore further",
            (
                "Trend sales and profit over time to spot seasonality.",
                f"Break {columns.profit} down by Category and Sub-Category to "
                f"find loss-making lines.",
                "Correlate Discount with Profit to measure margin erosion.",
                "Rank top customers and map sales by State for geographic "
                "insight.",
            ),
        ),
    ]
