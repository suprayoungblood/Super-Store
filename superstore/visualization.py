"""Matplotlib chart rendering.

Charts are built with the modern object-oriented Matplotlib API (``Figure`` /
``Axes``), saved as PNG files for the report, and optionally shown
interactively. The backend is selected by :func:`configure_backend` before any
plotting so the pipeline runs headless by default.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

from .config import ChartStyle


def configure_backend(interactive: bool) -> None:
    """Select the Matplotlib backend before the first plot is created.

    Args:
        interactive: When ``False``, force the non-interactive 'Agg' backend so
            charts render to files without opening a window.
    """
    if not interactive:
        matplotlib.use("Agg")


def render_bar_chart(
    series,
    *,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: Path,
    style: ChartStyle,
    show: bool = False,
) -> Path:
    """Render a bar chart from a pandas Series and save it as a PNG.

    Args:
        series: Indexed values to plot (index becomes the x-axis categories).
        title: Chart title.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        output_path: File to write the PNG to (parent dirs are created).
        style: Color, figure size, and DPI settings.
        show: When ``True``, also display the chart interactively.

    Returns:
        The path the chart was written to.
    """
    # Imported lazily so :func:`configure_backend` can run first.
    import matplotlib.pyplot as plt

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(figsize=style.figsize)
    series.plot(kind="bar", color=style.color, ax=axes)
    _style_axes(axes, title=title, xlabel=xlabel, ylabel=ylabel)
    figure.tight_layout()
    figure.savefig(output_path, dpi=style.dpi, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(figure)
    return output_path


def _style_axes(axes, *, title: str, xlabel: str, ylabel: str) -> None:
    """Apply titles and axis labels to a set of axes."""
    axes.set_title(title)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
