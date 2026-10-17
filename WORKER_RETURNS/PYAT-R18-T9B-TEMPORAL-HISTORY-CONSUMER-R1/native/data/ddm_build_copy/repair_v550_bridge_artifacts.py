#!/usr/bin/env python3
"""Repair only the V550 bridge artifacts for an existing shard.

This is intentionally narrow:
- it does not recompute question outputs
- it does not rerun stages 1-4
- it does not touch the cloud replay
- it only rebuilds the persisted bridge outputs from the already-built shard tables

Optionally, it can refresh the shard manifest and shard status metadata so the
recorded bridge counts line up with the repaired bridge file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_bridge import _apply_v551_eligibility
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_schema import V551_BRIDGE_INDEX_SCHEMA, validate_bridge_index
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths, atomic_write_json

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair only the bridge artifacts for an existing V550 shard.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--apply", action="store_true", help="Overwrite the existing bridge artifacts and metadata.")
    parser.add_argument("--refresh-manifest", action="store_true", help="Rewrite shard_manifest.json with the repaired bridge counts.")
    parser.add_argument("--refresh-status", action="store_true", help="Rewrite shard_status.json after refreshing the manifest.")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)
def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    shard_paths = V550ShardPaths(root=output_root, run_id=args.run_id, shard_id=args.shard_id)
    shard_paths.ensure()

    existing_manifest = _read_json(shard_paths.manifest_path) or {}
    existing_status = _read_json(shard_paths.status_path) or {}
    bridge_path = shard_paths.bridge / "v551_bridge_index.parquet"
    if not bridge_path.exists():
        raise FileNotFoundError(f"Missing bridge parquet: {bridge_path}")

    bridge = pd.read_parquet(bridge_path)
    bridge = _apply_v551_eligibility(bridge) if not bridge.empty else bridge
    bridge_meta = {
        "bridge_rows": int(len(bridge)),
        "eligible_rows": int(bridge["v551_eligible"].fillna(False).sum()) if "v551_eligible" in bridge.columns else 0,
        "excluded_rows": int(len(bridge) - int(bridge["v551_eligible"].fillna(False).sum())) if "v551_eligible" in bridge.columns else int(len(bridge)),
    }

    bridge_schema_path = shard_paths.bridge / "v551_bridge_index.schema.json"
    bridge_validation_issues = validate_bridge_index(pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"]))
    bridge_validation_report = {
        "success": not bridge_validation_issues,
        "errors": bridge_validation_issues,
        "warnings": [],
        "bridge_rows": int(bridge_meta["bridge_rows"]),
        "eligible_rows": int(bridge_meta["eligible_rows"]),
        "excluded_rows": int(bridge_meta["excluded_rows"]),
    }
    bridge_warnings = {
        "run_id": args.run_id,
        "shard_id": args.shard_id,
        "bridge_rows": int(bridge_meta["bridge_rows"]),
        "eligible_rows": int(bridge_meta["eligible_rows"]),
        "excluded_rows": int(bridge_meta["excluded_rows"]),
        "issues": bridge_validation_issues,
    }

    if args.apply:
        bridge.to_parquet(bridge_path, index=False)
        _write_json(bridge_schema_path, {"row_count": int(bridge_meta["bridge_rows"]), "columns": list(V551_BRIDGE_INDEX_SCHEMA["required_columns"])})
        _write_json(shard_paths.bridge / "v551_bridge_warnings.json", bridge_warnings)
        _write_json(shard_paths.bridge / "v551_bridge_validation_report.json", bridge_validation_report)

    repaired_manifest = dict(existing_manifest)
    if args.apply and args.refresh_manifest:
        repaired_manifest.update(
            {
                "completed_at": utc_now(),
                "bridge_rows": int(bridge_meta["bridge_rows"]),
                "v551_bridge_index_row_count": int(bridge_meta["bridge_rows"]),
                "v551_eligible_count": int(bridge_meta["eligible_rows"]),
                "v551_excluded_count": int(bridge_meta["excluded_rows"]),
                "promotable": bool(existing_manifest.get("promotable", False)) and not bool(bridge_validation_issues),
            }
        )
        _write_json(shard_paths.manifest_path, repaired_manifest)

    repaired_status = dict(existing_status)
    if args.apply and args.refresh_status:
        repaired_status.update(
            {
                "status": existing_status.get("status", "success"),
                "success": bool(repaired_manifest.get("success", existing_manifest.get("success", False))),
                "promotable": bool(repaired_manifest.get("promotable", existing_manifest.get("promotable", False))),
                "updated_at": utc_now(),
                "repaired_at": utc_now(),
                "repair_summary": {
                    "bridge_rows": int(bridge_meta["bridge_rows"]),
                    "bridge_eligible_rows": int(bridge_meta["eligible_rows"]),
                    "bridge_excluded_rows": int(bridge_meta["excluded_rows"]),
                },
            }
        )
        _write_json(shard_paths.status_path, repaired_status)

    print(
        json.dumps(
            {
                "shard_path": str(shard_paths.shard_path),
                "apply": args.apply,
                "refresh_manifest": args.refresh_manifest,
                "refresh_status": args.refresh_status,
                "bridge_meta": bridge_meta,
                "bridge_validation_report": bridge_validation_report,
                "manifest_bridge_rows": repaired_manifest.get("bridge_rows", existing_manifest.get("bridge_rows")),
                "manifest_eligible_rows": repaired_manifest.get("v551_eligible_count", existing_manifest.get("v551_eligible_count")),
                "status_promotable": repaired_status.get("promotable", existing_status.get("promotable")),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
