"""Unit tests for dataset loading and validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from superstore.config import AppConfig, Paths
from superstore.data_loader import load_dataset


def _config_for(root: Path) -> AppConfig:
    """Build a config whose data file lives under ``root/data``."""
    return AppConfig(paths=Paths(root=root))


def _write_csv(root: Path, raw: bytes) -> None:
    """Write raw CSV bytes to the conventional data location."""
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "superstore.csv").write_bytes(raw)


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_dataset(_config_for(tmp_path))


def test_missing_required_columns_raises(tmp_path: Path):
    _write_csv(tmp_path, b"Alpha,Beta\n1,2\n")
    with pytest.raises(ValueError):
        load_dataset(_config_for(tmp_path))


def test_falls_back_to_cp1252_encoding(tmp_path: Path):
    # 0xe9 ('é' in cp1252) is invalid UTF-8, forcing the encoding fallback.
    _write_csv(tmp_path, "Sales,Profit,Region\n100,10,Wést\n".encode("cp1252"))
    frame = load_dataset(_config_for(tmp_path))
    assert list(frame.columns) == ["Sales", "Profit", "Region"]
    assert len(frame) == 1
    assert frame.loc[0, "Region"] == "Wést"


def test_header_only_dataset_raises(tmp_path: Path):
    _write_csv(tmp_path, b"Sales,Profit,Region\n")
    with pytest.raises(ValueError, match="no data rows"):
        load_dataset(_config_for(tmp_path))


def test_non_numeric_column_raises(tmp_path: Path):
    _write_csv(tmp_path, b"Sales,Profit,Region\n$100,10,West\n")
    with pytest.raises(ValueError, match="must be numeric"):
        load_dataset(_config_for(tmp_path))


def test_empty_file_raises(tmp_path: Path):
    _write_csv(tmp_path, b"")
    with pytest.raises(ValueError, match="empty or malformed"):
        load_dataset(_config_for(tmp_path))
