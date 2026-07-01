"""Runtime detection of the installed analytics libraries.

The version numbers are surfaced in two places: the terminal report (the
"verify the installation" step) and the deck's installation slide. Detecting
them at runtime keeps the report accurate instead of hard-coding versions.
"""

from __future__ import annotations

import platform


def library_versions() -> dict[str, str]:
    """Return the installed versions of the libraries used by the pipeline.

    Returns:
        Mapping of library label to its version string, including the active
        Python runtime.
    """
    import matplotlib
    import pandas as pd

    return {
        "Python": platform.python_version(),
        "pandas": pd.__version__,
        "Matplotlib": matplotlib.__version__,
    }
