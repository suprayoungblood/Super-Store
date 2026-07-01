"""Command-line entry point for the Superstore analytics pipeline.

Run ``python main.py`` for the analysis and chart, add ``--deck`` to also build
the PowerPoint report, and ``--show`` to display the chart interactively.
Presenter details for the title slide can be overridden with ``--name``,
``--course``, and ``--instructor``.
"""

from __future__ import annotations

import argparse
from dataclasses import replace

from superstore.config import AppConfig, default_config
from superstore.visualization import configure_backend


def main() -> None:
    """Parse arguments, build the configuration, and run the pipeline."""
    args = _parse_args()
    # Select the Matplotlib backend before any plotting module imports pyplot.
    configure_backend(interactive=args.show)
    config = _build_config(args)

    from superstore.pipeline import run_pipeline

    run_pipeline(config, show=args.show, make_deck=args.deck)


def _parse_args() -> argparse.Namespace:
    """Define and parse the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Analyze the Superstore dataset and report the results."
    )
    parser.add_argument(
        "--deck", action="store_true", help="also generate the PowerPoint report"
    )
    parser.add_argument(
        "--show", action="store_true", help="display the chart interactively"
    )
    parser.add_argument("--name", help="presenter name for the title slide")
    parser.add_argument("--course", help="course name for the title slide")
    parser.add_argument("--instructor", help="instructor name for the title slide")
    return parser.parse_args()


def _build_config(args: argparse.Namespace) -> AppConfig:
    """Apply any command-line presenter overrides to the default config."""
    config = default_config()
    presenter = replace(
        config.presenter,
        name=args.name or config.presenter.name,
        course=args.course or config.presenter.course,
        instructor=args.instructor or config.presenter.instructor,
    )
    return replace(config, presenter=presenter)


if __name__ == "__main__":
    main()
