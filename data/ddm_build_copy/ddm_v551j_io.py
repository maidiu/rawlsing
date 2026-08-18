#!/usr/bin/env python3
"""I/O helpers for V551J artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy import ddm_v551j_schema as _v551j_schema
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    validate_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v550_shards import shard_id_for
from data.ddm_build_copy.ddm_v550_storage import atomic_write_json, read_table_any


# PG8-013/014: the authoritative v2.2.3 schema aliases are declared after the
# earlier W04-B UID-aware transitional schemas. Bind the additive machine and
# physical scope fields into those active lists in place before packet builders
# import their schema dictionaries. Labels and frozen packet/component identity
# and contract-hash namespaces remain unchanged.
_V551J_PACKET_UID_FIELDS = (
    "shard_id",
    "source_family_uid",
    "wave_uid",
    "uid_key",
    "uid_native_packet_id_v1",
    "cross_wave_homology_key_v1",
)
_V551J_COMPONENT_UID_FIELDS = (
    "shard_id",
    "source_family_uid",
    "wave_uid",
    "uid_key",
    "uid_native_component_id_v1",
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _insert_identity_fields(columns: list[str], fields: tuple[str, ...]) -> None:
    missing = [field for field in fields if field not in columns]
    if not missing:
        return
    anchor = columns.index("country_code") + 1 if "country_code" in columns else len(columns)
    columns[anchor:anchor] = missing


def bind_v551j_active_uid_transport_schema() -> None:
    """Restore additive scope transport to the active v2.2.3 output schemas."""
    _insert_identity_fields(
        _v551j_schema.V551J_V22_PACKET_COLUMNS,
        _V551J_PACKET_UID_FIELDS,
    )
    _insert_identity_fields(
        _v551j_schema.V551J_V22_COMPONENT_INDEX_COLUMNS,
        _V551J_COMPONENT_UID_FIELDS,
    )
    _insert_identity_fields(
        _v551j_schema.V551J_V22_REVIEW_SURFACE_SCHEMA["required_columns"],
        _V551J_PACKET_UID_FIELDS,
    )


bind_v551j_active_uid_transport_schema()


def _bind_frozen_shard_transport(df: pd.DataFrame) -> pd.DataFrame:
    """Populate the frozen V550 shard spelling from an exact UID-coherent row.

    V550 shard ids are historical physical compatibility identifiers. They are
    deterministically spelled from the governed canonical display source/wave
    pair and are not part of source-wave machine identity. Existing populated
    shard ids must agree with that frozen spelling or publication fails closed.
    """
    out = df.copy()
    if out.empty or "shard_id" not in out.columns:
        return out
    for index, row in out.iterrows():
        source_family_uid = _clean(row.get("source_family_uid"))
        wave_uid = _clean(row.get("wave_uid"))
        if not source_family_uid or not wave_uid:
            raise BoundaryContractError(
                "V551J_SHARD_TRANSPORT_REQUIRES_UID_PAIR:"
                f"row={index}:source_family_uid={source_family_uid or '<missing>'}:"
                f"wave_uid={wave_uid or '<missing>'}"
            )
        coherence = validate_source_wave_identity_coherence(
            row.to_dict(),
            expected_source_family_uid=source_family_uid,
            expected_wave_uid=wave_uid,
            require_complete=True,
        )
        frozen_shard_id = shard_id_for(
            coherence.canonical_display_source,
            coherence.canonical_display_wave,
        )
        existing = _clean(row.get("shard_id"))
        if existing and existing != frozen_shard_id:
            raise BoundaryContractError(
                "V551J_SHARD_ID_TRANSPORT_CONFLICT:"
                f"expected={frozen_shard_id}:observed={existing}"
            )
        out.at[index, "shard_id"] = frozen_shard_id
    return out


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
    serializable = _bind_frozen_shard_transport(df)
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
        "rows": int(len(serializable)),
        "columns": int(len(serializable.columns)),
    }


def write_json_artifact(path: Path, payload: dict[str, Any]) -> Path:
    atomic_write_json(path, payload)
    return path
