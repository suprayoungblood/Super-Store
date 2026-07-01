"""Centralized configuration for the Superstore analytics pipeline.

Every tunable value (file locations, dataset column names, chart styling,
presenter details, and the encodings to try when reading the CSV) lives here so
that the rest of the package contains no hard-coded literals. Paths are derived
dynamically from the project root, so the project works regardless of where it
is checked out.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# Project root = two levels up from this file (``<root>/superstore/config.py``).
_PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Paths:
    """Filesystem locations derived from a single project ``root``."""

    root: Path

    @property
    def data_file(self) -> Path:
        """Path to the UTF-8 Superstore CSV."""
        return self.root / "data" / "superstore.csv"

    @property
    def reports_dir(self) -> Path:
        """Directory that holds generated artifacts (chart, deck)."""
        return self.root / "reports"

    @property
    def chart_file(self) -> Path:
        """Output path for the 'Total Sales by Region' bar chart."""
        return self.reports_dir / "sales_by_region.png"

    @property
    def deck_file(self) -> Path:
        """Output path for the generated PowerPoint report."""
        return self.reports_dir / "topic9_report.pptx"


@dataclass(frozen=True)
class Columns:
    """Names of the dataset columns the pipeline depends on."""

    sales: str = "Sales"
    profit: str = "Profit"
    region: str = "Region"

    @property
    def required(self) -> tuple[str, ...]:
        """Columns that must exist for the pipeline to run."""
        return (self.sales, self.profit, self.region)

    @property
    def numeric(self) -> tuple[str, ...]:
        """Columns that must hold numeric values for analysis."""
        return (self.sales, self.profit)

    @property
    def sales_by_region_title(self) -> str:
        """Shared title for the sales-by-region chart and report section."""
        return f"Total {self.sales} by {self.region}"


@dataclass(frozen=True)
class ChartStyle:
    """Styling applied to generated Matplotlib charts."""

    color: str = "skyblue"
    figsize: tuple[float, float] = (8.0, 6.0)
    dpi: int = 120


@dataclass(frozen=True)
class Presenter:
    """Metadata used to populate the report's title slide.

    Defaults are placeholders that can be overridden from the command line.
    """

    name: str = "Pariss Youngblood"
    course: str = "[Course Name]"
    topic: str = "Topic 9: Data Analytics Using Python"
    instructor: str = "[Instructor Name]"


@dataclass(frozen=True)
class AppConfig:
    """Top-level configuration aggregating every settings group."""

    paths: Paths
    columns: Columns = field(default_factory=Columns)
    chart: ChartStyle = field(default_factory=ChartStyle)
    presenter: Presenter = field(default_factory=Presenter)
    # Encodings are attempted in order; the first that decodes the file wins.
    encodings: tuple[str, ...] = ("utf-8", "cp1252", "latin-1")


def default_config() -> AppConfig:
    """Build the default configuration rooted at the project directory."""
    return AppConfig(paths=Paths(root=_PROJECT_ROOT))
