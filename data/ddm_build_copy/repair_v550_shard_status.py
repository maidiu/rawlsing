#!/usr/bin/env python3
"""Repair stale V550 shard status metadata from existing artifacts.

This script does not recompute any question outputs, bridge tables, or readiness
coverage. It only rewrites the shard status file with a current assessment based
on the artifacts already on disk.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_READINESS_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks" / "shard_runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair the stale metadata for an existing V550 shard.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--readiness-artifact", default=None)
    parser.add_argument("--apply", action="store_true", help="Overwrite shard_status.json with the repaired metadata.")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    shard_path = output_root / "shard_runs" / args.run_id / args.shard_id
    readiness_root = Path(args.readiness_artifact) if args.readiness_artifact else (DEFAULT_READINESS_ROOT / args.run_id / args.shard_id)

    shard_manifest = _read_json(shard_path / "shard_manifest.json") or {}
    shard_status = _read_json(shard_path / "shard_status.json") or {}
    readiness_manifest = _read_json(readiness_root / "readiness_manifest.json") or {}
    readiness_status = _read_json(readiness_root / "readiness_status.json") or {}
    readiness_table_path = readiness_root / "core" / "substrate_readiness.parquet"

    question_universe_dir = shard_path / "checkpoints" / "question_tables" / "question_universe"
    parquet_count = sum(1 for p in question_universe_dir.glob("*.parquet")) if question_universe_dir.exists() else 0
    complete_count = sum(1 for p in question_universe_dir.glob("*.complete")) if question_universe_dir.exists() else 0

    readiness_success = readiness_status.get("status") == "success"
    readiness_rows = readiness_manifest.get("readiness_rows")
    readiness_class_counts = readiness_manifest.get("readiness_class_counts") or {}
    mapping_rows = readiness_manifest.get("mapping_rows")
    if not readiness_class_counts and readiness_table_path.exists():
        readiness_table = pd.read_parquet(readiness_table_path)
        if not readiness_table.empty and "readiness_status" in readiness_table.columns:
            readiness_class_counts = readiness_table["readiness_status"].value_counts(dropna=False).to_dict()
    mapping_insufficient = int(readiness_class_counts.get("mapping_insufficient", 0) or 0)
    ready_count = int(readiness_class_counts.get("ready", 0) or 0)

    if readiness_success and (mapping_rows == 0 or mapping_insufficient > 0):
        repaired_error = (
            f"[V550_READINESS_MAPPING_INSUFFICIENT] Readiness artifact exists and is successful, "
            f"but mapping_rows={mapping_rows} and readiness_rows={readiness_rows}; "
            f"ready={ready_count}, mapping_insufficient={mapping_insufficient}. "
            "Existing substantive outputs are intact, but the recorded run remains not promotable."
        )
    elif not readiness_success:
        repaired_error = (
            "[V550_READINESS_UNAVAILABLE] The readiness artifact is missing or not successful, "
            "so the shard cannot be promoted from the existing outputs alone."
        )
    else:
        repaired_error = (
            "[V550_SHARD_NEEDS_REVIEW] Existing outputs are present, but the run metadata still needs review "
            "before it can be treated as promotable."
        )

    repaired_status = {
        **shard_status,
        "run_id": args.run_id,
        "shard_id": args.shard_id,
        "status": shard_status.get("status", "failed"),
        "success": bool(shard_manifest.get("success", False)),
        "promotable": bool(shard_manifest.get("promotable", False)),
        "error": repaired_error,
        "updated_at": pd.Timestamp.utcnow().isoformat(),
        "repaired_at": pd.Timestamp.utcnow().isoformat(),
        "repair_summary": {
            "question_universe_parquets": parquet_count,
            "question_universe_completes": complete_count,
            "readiness_success": readiness_success,
            "readiness_rows": readiness_rows,
            "readiness_mapping_rows": mapping_rows,
            "readiness_ready": ready_count,
            "readiness_mapping_insufficient": mapping_insufficient,
        },
    }

    if args.apply:
        status_path = shard_path / "shard_status.json"
        backup_path = shard_path / "shard_status.original.json"
        if status_path.exists() and not backup_path.exists():
            backup_path.write_text(status_path.read_text(), encoding="utf-8")
        _write_json(status_path, repaired_status)

    print(json.dumps(
        {
            "shard_path": str(shard_path),
            "readiness_path": str(readiness_root),
            "apply": args.apply,
            "repaired_status": repaired_status,
            "shard_manifest_success": shard_manifest.get("success"),
            "shard_manifest_promotable": shard_manifest.get("promotable"),
            "readiness_success": readiness_success,
            "readiness_rows": readiness_rows,
            "readiness_class_counts": readiness_class_counts,
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
