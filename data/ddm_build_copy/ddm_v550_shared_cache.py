#!/usr/bin/env python3
"""Shared on-disk cache helpers for V550 readiness/build queries."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from data.ddm_build_copy.ddm_v550_storage import atomic_write_json, utc_now

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SHARED_CACHE_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "shared_cache"
CACHE_FORMAT_VERSION = "v2"


@dataclass(frozen=True)
class CacheEntry:
    cache_root: Path
    cache_kind: str
    cache_key: str

    @property
    def entry_dir(self) -> Path:
        return self.cache_root / self.cache_kind / self.cache_key

    @property
    def data_path(self) -> Path:
        return self.entry_dir / "data.parquet"

    @property
    def meta_path(self) -> Path:
        return self.entry_dir / "meta.json"


def shared_cache_root(cache_root: Path | None = None) -> Path:
    return Path(cache_root or DEFAULT_SHARED_CACHE_ROOT)


def _normalize_for_signature(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _normalize_for_signature(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple, set)):
        return [_normalize_for_signature(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float) and pd.isna(value):
        return None
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


def cache_signature(payload: Any) -> str:
    normalized = _normalize_for_signature(payload)
    blob = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def cache_entry(cache_kind: str, cache_key: str, cache_root: Path | None = None) -> CacheEntry:
    return CacheEntry(cache_root=shared_cache_root(cache_root), cache_kind=str(cache_kind), cache_key=str(cache_key))


def load_cached_frame(entry: CacheEntry, expected_signature: str | None = None) -> pd.DataFrame | None:
    if not entry.data_path.exists() or not entry.meta_path.exists():
        return None
    try:
        metadata = json.loads(entry.meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if expected_signature and metadata.get("query_signature") not in {expected_signature, f"sha256:{expected_signature}"}:
        return None
    try:
        return pd.read_parquet(entry.data_path)
    except Exception:
        return None


def write_cached_frame(frame: pd.DataFrame, entry: CacheEntry, metadata: dict[str, Any]) -> None:
    entry.entry_dir.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(entry.data_path, index=False)
    payload = dict(metadata)
    payload.setdefault("created_at", utc_now())
    payload.setdefault("row_count", int(len(frame)))
    payload.setdefault("schema_version", "v1")
    atomic_write_json(entry.meta_path, payload)


def cached_query_frame(
    cache_kind: str,
    payload: dict[str, Any],
    query_fn: Callable[[], pd.DataFrame],
    *,
    cache_root: Path | None = None,
    metadata: dict[str, Any] | None = None,
) -> pd.DataFrame:
    signature = cache_signature({"cache_format_version": CACHE_FORMAT_VERSION, "payload": payload})
    entry = cache_entry(cache_kind, signature, cache_root=cache_root)
    cached = load_cached_frame(entry, expected_signature=signature)
    if cached is not None:
        return cached.reset_index(drop=True)
    frame = query_fn().reset_index(drop=True)
    write_cached_frame(
        frame,
        entry,
        {
            "cache_kind": cache_kind,
            "query_signature": signature,
            "query_payload": _normalize_for_signature(payload),
            "cache_format_version": CACHE_FORMAT_VERSION,
            **(metadata or {}),
        },
    )
    return frame


def question_structural_mapping_select_columns(conn) -> list[str]:
    base_columns = [
        "source",
        "wave",
        "question_id",
        "var_code",
        "display_text",
        "legacy_final_driver_id",
        "final_driver_label",
        "final_driver_scope",
        "final_driver_origin",
        "driver_id",
        "driver_facet_id",
        "question_block_id",
        "structural_domain_id",
        "relation_axis_id",
        "target_entity_id",
        "mapping_status",
        "evidence_kind",
        "strata_relevance",
        "channel_affordances",
        "forbidden_inference",
        "does_not_measure",
        "review_notes",
    ]
    optional_columns = [
        "question_type",
        "handling_rule",
        "recommended_computation",
        "final_driver_scope",
        "source_structure_classification",
        "authority_semantic_role",
        "authority_disposition",
        "semantic_role",
        "semantic_lane",
        "evidence_lane",
        "source_structure_fields_joined",
        # R1 authority identity/disposition fields are optional for older
        # installations, but must be selected whenever the table exposes them.
        "canonical_wave",
        "country_code_scope",
        "authority_status",
        "authority_rule_id",
    ]
    import os
    qsm_rel = os.getenv("DDM_QSM_RELATION", "public.question_structural_mapping")
    if "." in qsm_rel:
        parts = qsm_rel.split(".", 1)
        qsm_schema = parts[0]
        qsm_table = parts[1]
    else:
        qsm_schema = "public"
        qsm_table = qsm_rel
    sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %(schema)s
          AND table_name = %(table)s
    """
    available = {str(value) for value in pd.read_sql_query(sql, conn, params={"schema": qsm_schema, "table": qsm_table})["column_name"].tolist()}
    return [column for column in base_columns + [col for col in optional_columns if col not in base_columns] if column in available or column in base_columns]
