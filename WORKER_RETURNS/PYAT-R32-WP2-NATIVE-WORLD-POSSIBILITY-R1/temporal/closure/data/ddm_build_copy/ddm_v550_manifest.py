#!/usr/bin/env python3
"""Manifest assembly for V550 runs."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_manifest(
    *,
    run_id: str,
    version: str,
    stage: str,
    repo_root: Path,
    run_path: Path,
    input_db_used: bool,
    source_filters: list[str],
    wave_filters: list[str],
    country_filters: list[str],
    thresholds: dict[str, Any],
    script_versions: dict[str, str],
    input_row_counts: dict[str, Any],
    output_row_counts: dict[str, Any],
    readiness_class_counts: dict[str, Any],
    warnings: list[str],
    errors: list[str],
    files_written: list[str],
    csv_mirrors_written: list[str],
    postgres_tables_written: list[str],
    postgres_views_written: list[str],
    success: bool,
    storage_layout_version: str = "v550-storage-1",
) -> dict[str, Any]:
    now = utc_now()
    return {
        "run_id": run_id,
        "version": version,
        "stage": stage,
        "created_at": now,
        "completed_at": now,
        "success": success,
        "repo_root": str(repo_root),
        "run_path": str(run_path),
        "latest_pointer_updated": success,
        "script_versions": script_versions,
        "python_version": "",
        "input_db_used": input_db_used,
        "source_filters": source_filters,
        "wave_filters": wave_filters,
        "country_filters": country_filters,
        "thresholds": thresholds,
        "storage_layout_version": storage_layout_version,
        "canonical_tables_written": files_written,
        "csv_mirrors_written": csv_mirrors_written,
        "postgres_tables_written": postgres_tables_written,
        "postgres_latest_views_written": postgres_views_written,
        "schema_files_written": [f.replace(".parquet", ".schema.json") for f in files_written],
        "input_row_counts": input_row_counts,
        "output_row_counts": output_row_counts,
        "readiness_class_counts": readiness_class_counts,
        "quarantine_counts": {},
        "manual_review_counts": {},
        "warnings": warnings,
        "errors": errors,
    }


def build_shard_manifest(
    *,
    run_id: str,
    shard_id: str,
    source: str,
    source_family: str,
    wave: str,
    canonical_wave: str,
    created_at: str,
    completed_at: str,
    success: bool,
    output_root: Path,
    inputs: dict[str, Any],
    rows_by_table: dict[str, int],
    warnings: list[str],
    errors: list[str],
    outputs: list[str],
    bridge_rows: int,
    v551_eligible_count: int,
    v551_excluded_count: int,
    promotable: bool,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source,
        "source_family": source_family,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "created_at": created_at,
        "completed_at": completed_at,
        "success": success,
        "promotable": promotable,
        "output_root": str(output_root),
        "inputs": inputs,
        "rows_by_table": rows_by_table,
        "warnings": warnings,
        "errors": errors,
        "outputs": outputs,
        "bridge_rows": bridge_rows,
        "v551_bridge_index_row_count": bridge_rows,
        "v551_eligible_count": v551_eligible_count,
        "v551_excluded_count": v551_excluded_count,
    }


def build_merge_manifest(
    *,
    run_id: str,
    created_at: str,
    completed_at: str,
    success: bool,
    shard_count_expected: int,
    shard_count_actual: int,
    missing_shards: list[str],
    row_counts: dict[str, Any],
    bridge_row_count: int,
    warnings: list[str],
    errors: list[str],
    promoted_latest: bool,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "created_at": created_at,
        "completed_at": completed_at,
        "success": success,
        "shard_count_expected": shard_count_expected,
        "shard_count_actual": shard_count_actual,
        "missing_shards": missing_shards,
        "row_counts": row_counts,
        "bridge_row_count": bridge_row_count,
        "warnings": warnings,
        "errors": errors,
        "promoted_latest": promoted_latest,
    }


def write_success_manifest(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        __import__("json").dumps({**payload, "success": True}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def write_failure_manifest(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        __import__("json").dumps({**payload, "success": False}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path
