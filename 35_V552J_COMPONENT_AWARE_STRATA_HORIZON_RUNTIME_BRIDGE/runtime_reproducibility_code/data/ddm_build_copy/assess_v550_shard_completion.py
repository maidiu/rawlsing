#!/usr/bin/env python3
"""Assess an existing V550 shard without recomputing any outputs.

This script is intentionally read-only. It inspects the shard run folder and an
optional readiness artifact bundle, then reports whether the existing outputs
look complete and promotable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_READINESS_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks" / "shard_runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assess an existing V550 shard without rebuilding it.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--readiness-artifact", default=None)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def _count_files(path: Path, suffix: str) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.glob(f"*{suffix}") if p.is_file())


def _print_block(title: str, payload: Any) -> None:
    print(f"\n== {title} ==")
    if payload is None:
        print("missing")
    elif isinstance(payload, (dict, list)):
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload)


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    shard_path = output_root / "shard_runs" / args.run_id / args.shard_id
    readiness_root = Path(args.readiness_artifact) if args.readiness_artifact else (DEFAULT_READINESS_ROOT / args.run_id / args.shard_id)

    shard_manifest = _read_json(shard_path / "shard_manifest.json")
    shard_status = _read_json(shard_path / "shard_status.json")
    shard_warnings = _read_json(shard_path / "shard_warnings.json")
    readiness_manifest = _read_json(readiness_root / "readiness_manifest.json")
    readiness_status = _read_json(readiness_root / "readiness_status.json")

    question_universe_dir = shard_path / "checkpoints" / "question_tables" / "question_universe"
    complete_count = _count_files(question_universe_dir, ".complete")
    parquet_count = _count_files(question_universe_dir, ".parquet")
    checkpoint_missing = parquet_count - complete_count

    summary = {
        "shard_path": str(shard_path),
        "readiness_path": str(readiness_root),
        "question_universe_parquets": parquet_count,
        "question_universe_completes": complete_count,
        "question_universe_missing_completes": max(checkpoint_missing, 0),
        "shard_status": None if shard_status is None else shard_status.get("status"),
        "shard_success": None if shard_status is None else shard_status.get("status") == "success",
        "shard_promotable": None if shard_status is None else shard_status.get("promotable"),
        "manifest_success": None if shard_manifest is None else shard_manifest.get("success"),
        "manifest_promotable": None if shard_manifest is None else shard_manifest.get("promotable"),
        "readiness_success": None if readiness_status is None else readiness_status.get("status") == "success",
        "readiness_status": None if readiness_status is None else readiness_status.get("status"),
        "readiness_rows": None if readiness_manifest is None else readiness_manifest.get("readiness_rows"),
        "readiness_class_counts": None if readiness_manifest is None else readiness_manifest.get("readiness_class_counts"),
        "warnings": [] if shard_warnings is None else shard_warnings.get("warnings", shard_warnings if isinstance(shard_warnings, list) else [shard_warnings]),
    }

    _print_block("Summary", summary)
    _print_block("Shard Manifest", shard_manifest)
    _print_block("Shard Status", shard_status)
    _print_block("Shard Warnings", shard_warnings)
    _print_block("Readiness Status", readiness_status)
    _print_block("Readiness Manifest", readiness_manifest)

    if args.verbose:
        print("\nVerdict:")
        if shard_manifest and shard_manifest.get("success") and shard_manifest.get("promotable"):
            print("existing substance looks complete and promotable")
        elif shard_manifest and shard_manifest.get("success"):
            print("existing substance is present, but the shard is not yet promotable")
        elif shard_status and shard_status.get("status") == "failed":
            print("existing substance is present, but the recorded run is failed/incomplete")
        else:
            print("insufficient information to declare the shard complete")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
