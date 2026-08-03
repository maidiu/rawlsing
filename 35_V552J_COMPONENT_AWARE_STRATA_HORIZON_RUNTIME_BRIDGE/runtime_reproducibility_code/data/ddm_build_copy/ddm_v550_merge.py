#!/usr/bin/env python3
"""Merge compiler helpers for V550 shard bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_bridge import validate_bridge_df
from data.ddm_build_copy.ddm_v550_schema import SHARD_OUTPUT_TABLES
from data.ddm_build_copy.ddm_v550_storage import read_table_any


TABLE_LAYER_MAP = {
    "question_universe": "core",
    "question_use_contract": "core",
    "position_distribution": "determinicity",
    "answer_distribution": "distributions",
    "country_answer_distribution": "distributions",
    "position_indicator_summary": "determinicity",
    "indicator_answer_matrix": "determinicity",
    "outlier_cohort_summary": "determinicity",
    "secondary_indicator_summary": "determinicity",
    "recursive_branch_nodes": "determinicity",
    "branch_position_signature": "clouds",
    "branch_relation_co_signature": "clouds",
    "branch_co_signature": "clouds",
    "question_response_attitude_cloud": "clouds",
    "mapping_gap_report": "audit",
    "underpowered_quarantine": "audit",
    "response_option_manual_review": "audit",
    "scope_manifest": "core",
    "substrate_readiness": "core",
    "position_field_coverage": "core",
    "weight_coverage": "core",
    "mapping_status_coverage": "core",
    "legacy_leak_report": "audit",
    "cloud_exclusion_audit": "audit",
}


def _table_path_for_shard(shard_dir: Path, table_name: str) -> Path:
    layer = TABLE_LAYER_MAP.get(table_name, "core")
    return shard_dir / layer / f"{table_name}.parquet"


def load_shard_manifests(shards_root: Path) -> list[dict[str, Any]]:
    manifests: list[dict[str, Any]] = []
    for manifest_path in sorted(shards_root.glob("*/*/shard_manifest.json")):
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            manifests.append(payload)
    return manifests


def merge_shard_tables(shard_dirs: list[Path], table_name: str, *, strict: bool = True) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    missing: list[str] = []
    expected_columns: tuple[str, ...] | None = None
    for shard_dir in shard_dirs:
        table_path = _table_path_for_shard(shard_dir, table_name)
        if not table_path.exists():
            missing.append(str(table_path))
            continue
        frame = pd.read_parquet(table_path)
        columns = tuple(frame.columns)
        if expected_columns is None:
            expected_columns = columns
        elif columns != expected_columns:
            raise ValueError(
                f"schema drift detected for {table_name}: {shard_dir.name} has {list(columns)} but expected {list(expected_columns)}"
            )
        frames.append(frame)
    if missing and strict:
        raise FileNotFoundError(f"missing required shard table files for {table_name}: {missing[:8]}")
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def merge_v551_bridge_indexes(shard_dirs: list[Path], *, strict: bool = True) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    missing: list[str] = []
    expected_columns: tuple[str, ...] | None = None
    for shard_dir in shard_dirs:
        bridge_path = shard_dir / "bridge" / "v551_bridge_index.parquet"
        if not bridge_path.exists():
            missing.append(str(bridge_path))
            continue
        frame = pd.read_parquet(bridge_path)
        columns = tuple(frame.columns)
        if expected_columns is None:
            expected_columns = columns
        elif columns != expected_columns:
            raise ValueError(
                f"schema drift detected for v551_bridge_index: {shard_dir.name} has {list(columns)} but expected {list(expected_columns)}"
            )
        frames.append(frame)
    if missing and strict:
        raise FileNotFoundError(f"missing required bridge index files: {missing[:8]}")
    if not frames:
        return pd.DataFrame()
    bridge = pd.concat(frames, ignore_index=True, sort=False)
    validate_bridge_df(bridge)
    return bridge


def validate_shard_schema_compatibility(shard_dirs: list[Path]) -> list[str]:
    issues: list[str] = []
    seen_signatures: dict[str, tuple[str, ...]] = {}
    for shard_dir in shard_dirs:
        for table_name in SHARD_OUTPUT_TABLES:
            path = _table_path_for_shard(shard_dir, table_name)
            if not path.exists():
                issues.append(f"{shard_dir.name}:{table_name}:missing_required_file")
                continue
            try:
                frame = pd.read_parquet(path)
            except Exception as exc:  # pragma: no cover - filesystem/runtime failure
                issues.append(f"{shard_dir.name}:{table_name}:{exc}")
                continue
            signature = tuple(frame.columns)
            previous = seen_signatures.get(table_name)
            if previous is None:
                seen_signatures[table_name] = signature
            elif previous != signature:
                issues.append(f"{shard_dir.name}:{table_name}:schema_drift")
    return issues


def deduplicate_rows(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    if df.empty:
        return df
    if subset:
        return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)
    return df.drop_duplicates().reset_index(drop=True)
