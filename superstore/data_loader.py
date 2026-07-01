"""Robust loading of the Superstore CSV.

The published Superstore file ships in a Windows-1252 encoding, so a naive
UTF-8 read can fail. :func:`load_dataset` tries each configured encoding in
order and validates that the columns the pipeline needs are present, raising
clear, actionable errors when something is wrong.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import AppConfig


def load_dataset(config: AppConfig) -> pd.DataFrame:
    """Load and validate the Superstore dataset.

    Args:
        config: Application configuration providing the data path, the
            encodings to attempt, and the required columns.

    Returns:
        The dataset as a :class:`pandas.DataFrame`.

    Raises:
        FileNotFoundError: If the CSV does not exist.
        UnicodeDecodeError: If none of the configured encodings can decode it.
        ValueError: If the file is empty or malformed, required columns are
            missing, the dataset has no rows, or a numeric column is not numeric.
    """
    path = config.paths.data_file
    columns = config.columns
    _require_file(path)
    frame = _read_first_compatible(path, config.encodings)
    _require_columns(frame, columns.required)
    _require_rows(frame, path)
    _require_numeric(frame, columns.numeric)
    return frame


def _require_file(path: Path) -> None:
    """Raise a helpful error if the dataset file is absent."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Download the Kaggle Superstore "
            f"dataset, rename it 'superstore.csv', and place it in the 'data' "
            f"folder."
        )


def _read_first_compatible(path: Path, encodings: tuple[str, ...]) -> pd.DataFrame:
    """Return the frame from the first encoding that decodes the file."""
    last_error: UnicodeDecodeError | None = None
    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error
        except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
            raise ValueError(
                f"Dataset at '{path}' is empty or malformed and could not be "
                f"parsed as CSV."
            ) from error
    raise _decode_failure(path, encodings, last_error)


def _decode_failure(
    path: Path, encodings: tuple[str, ...], cause: UnicodeDecodeError | None
) -> UnicodeDecodeError:
    """Build a descriptive decode error covering every attempted encoding."""
    attempted = ", ".join(encodings)
    message = f"Could not decode '{path}' using any of: {attempted}."
    if cause is None:
        return UnicodeDecodeError("ascii", b"", 0, 1, message)
    return UnicodeDecodeError(
        cause.encoding, cause.object, cause.start, cause.end, message
    )


def _require_columns(frame: pd.DataFrame, required: tuple[str, ...]) -> None:
    """Raise if any required column is missing from the frame."""
    present = set(frame.columns)
    missing = [column for column in required if column not in present]
    if missing:
        raise ValueError(
            f"Dataset is missing required column(s): {', '.join(missing)}. "
            f"Found columns: {', '.join(map(str, frame.columns))}."
        )


def _require_rows(frame: pd.DataFrame, path: Path) -> None:
    """Raise if the dataset has headers but no data rows."""
    if frame.empty:
        raise ValueError(
            f"Dataset at '{path}' contains no data rows. Check that the CSV "
            f"holds records beneath its header."
        )


def _require_numeric(frame: pd.DataFrame, numeric_columns: tuple[str, ...]) -> None:
    """Raise if any column that must be numeric holds non-numeric values."""
    offenders = [
        column
        for column in numeric_columns
        if not pd.api.types.is_numeric_dtype(frame[column])
    ]
    if offenders:
        raise ValueError(
            f"Column(s) {', '.join(offenders)} must be numeric. Remove stray "
            f"characters (for example '$' or ',') from the CSV and try again."
        )
