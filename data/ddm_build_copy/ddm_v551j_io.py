#!/usr/bin/env python3
"""I/O helpers for V551J artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v550_storage import atomic_write_json, read_table_any


def _json_safe(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple, set)):
        if isinstance(value, set):
            value = sorted(value)
        elif isinstance(value, tuple):
            value = list(value)
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return value


def read_table(path: str | Path | None) -> pd.DataFrame:
    if path is None:
        return pd.DataFrame()
    path_obj = Path(path)
    if not path_obj.exists():
        return pd.DataFrame()
    return read_table_any(path_obj)


def file_hash(path: str | Path | None) -> str:
    if path is None:
        return "not_supplied"
    path_obj = Path(path)
    if not path_obj.exists():
        return "missing"
    try:
        return hashlib.sha256(path_obj.read_bytes()).hexdigest()
    except Exception:
        return "unreadable"


def ensure_output_dirs(output_root: str | Path, run_id: str) -> dict[str, Path]:
    root = Path(output_root) / run_id
    packets = root / "packets"
    audits = root / "audits"
    schemas = root / "schemas"
    manifest = root / "manifest"
    for path in (root, packets, audits, schemas, manifest):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "packets": packets,
        "audits": audits,
        "schemas": schemas,
        "manifest": manifest,
    }


def write_frame_artifact(
    df: pd.DataFrame,
    *,
    path: Path,
    schema_path: Path,
    name: str,
    run_id: str,
    write_csv: bool,
    write_parquet: bool,
    extra_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = df.copy()
    for column in serializable.columns:
        serializable[column] = serializable[column].map(_json_safe)
        if serializable[column].dtype == "object":
            serializable[column] = serializable[column].map(lambda value: "" if pd.isna(value) else str(value))
    if write_parquet:
        serializable.to_parquet(path, index=False)
    if write_csv:
        serializable.to_csv(path.with_suffix(".csv"), index=False, float_format="%.13f")
    write_schema_json(schema_path, serializable, name=name, run_id=run_id, extra=extra_schema)
    return {
        "path": str(path) if write_parquet else "",
        "csv_path": str(path.with_suffix(".csv")) if write_csv else "",
        "schema_path": str(schema_path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
    }


def write_json_artifact(path: Path, payload: dict[str, Any]) -> Path:
    atomic_write_json(path, payload)
    return path
