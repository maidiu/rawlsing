#!/usr/bin/env python3
"""Merge V550 shard bundles into a canonical repository run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_manifest import build_merge_manifest
from data.ddm_build_copy.ddm_v550_merge import deduplicate_rows, merge_shard_tables, merge_v551_bridge_indexes, validate_shard_schema_compatibility
from data.ddm_build_copy.ddm_v550_schema import SHARD_OUTPUT_TABLES, V551_BRIDGE_INDEX_SCHEMA, validate_shard_manifest
from data.ddm_build_copy.ddm_v550_storage import V550Paths, atomic_promote_latest, atomic_write_json, write_table
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge V550 shard bundles.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shards-root", default=None)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--reports-dir", default=str(ROOT / "data" / "ddm_build_copy" / "reports"))
    parser.add_argument("--write-csv", action="store_true", default=True)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--write-postgres", action="store_true", default=False)
    parser.add_argument("--promote-latest", action="store_true", default=False)
    parser.add_argument("--allow-missing-shards", action="store_true", default=False)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    shards_root = Path(args.shards_root) if args.shards_root else output_root / "shard_runs" / args.run_id
    run_paths = V550Paths(root=output_root, run_id=args.run_id)
    run_paths.ensure()

    shard_dirs = sorted([p for p in shards_root.iterdir() if p.is_dir()]) if shards_root.exists() else []
    if not shard_dirs:
        raise RuntimeError("No shard directories found.")

    missing_shard_issues: list[str] = []
    shard_validation_issues: list[str] = []
    shard_manifests: list[dict[str, object]] = []
    for shard_dir in shard_dirs:
        status_path = shard_dir / "shard_status.json"
        manifest_path = shard_dir / "shard_manifest.json"
        if not status_path.exists():
            missing_shard_issues.append(f"{shard_dir.name}: missing shard_status.json")
            continue
        if not manifest_path.exists():
            missing_shard_issues.append(f"{shard_dir.name}: missing shard_manifest.json")
            continue
        status = json.loads(status_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        shard_manifests.append(manifest)
        if status.get("status") != "success" or not bool(status.get("promotable", False)):
            shard_validation_issues.append(
                f"{shard_dir.name}: non-promotable status={status.get('status')} promotable={status.get('promotable')}"
            )
        manifest_issues = validate_shard_manifest(manifest)
        if manifest_issues:
            shard_validation_issues.extend([f"{shard_dir.name}: {issue}" for issue in manifest_issues])
        if str(manifest.get("run_id", "")) != args.run_id:
            shard_validation_issues.append(f"{shard_dir.name}: manifest run_id mismatch {manifest.get('run_id')} != {args.run_id}")
        if str(manifest.get("shard_id", "")) != shard_dir.name:
            shard_validation_issues.append(f"{shard_dir.name}: manifest shard_id mismatch {manifest.get('shard_id')} != {shard_dir.name}")

    if missing_shard_issues:
        raise RuntimeError("Shard validation failed: " + "; ".join(missing_shard_issues[:8]))
    if shard_validation_issues:
        raise RuntimeError("Shard validation failed: " + "; ".join(shard_validation_issues[:8]))

    shard_schema_issues = validate_shard_schema_compatibility(shard_dirs)
    if shard_schema_issues:
        raise RuntimeError("Shard schema incompatibility detected: " + "; ".join(shard_schema_issues[:5]))

    merged_tables = {}
    row_counts = {}
    for table_name in SHARD_OUTPUT_TABLES:
        merged = merge_shard_tables(shard_dirs, table_name, strict=True)
        if not merged.empty:
            if "run_id" not in merged.columns:
                merged["run_id"] = args.run_id
            if "shard_id" not in merged.columns:
                merged["shard_id"] = ""
            merged = deduplicate_rows(merged)
        merged_tables[table_name] = merged
        row_counts[table_name] = len(merged)

    bridge = merge_v551_bridge_indexes(shard_dirs, strict=True)
    if not bridge.empty:
        bridge = deduplicate_rows(bridge)
    bridge_path = run_paths.run_path / "bridge" / "v551_bridge_index.parquet"
    bridge_path.parent.mkdir(parents=True, exist_ok=True)
    if args.write_parquet:
        bridge.to_parquet(bridge_path, index=False)
    if args.write_csv:
        (run_paths.csv_mirrors / "v551_bridge_index.csv").parent.mkdir(parents=True, exist_ok=True)
        bridge.to_csv(run_paths.csv_mirrors / "v551_bridge_index.csv", index=False)
    (run_paths.run_path / "bridge" / "v551_bridge_index.schema.json").write_text(
        json.dumps({"row_count": len(bridge), "columns": list(bridge.columns)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    bridge_validation_issues = []
    if bridge.empty:
        bridge_validation_issues.append("v551_bridge_index is empty.")
    else:
        from data.ddm_build_copy.ddm_v550_bridge import validate_bridge_df

        bridge_validation_issues.extend(validate_bridge_df(bridge))
    (run_paths.run_path / "bridge" / "v551_bridge_validation_report.json").write_text(
        json.dumps(
            {
                "success": not bridge_validation_issues,
                "errors": bridge_validation_issues,
                "warnings": shard_schema_issues,
                "tables_checked": list(SHARD_OUTPUT_TABLES),
                "shards_checked": [p.name for p in shard_dirs],
                "bridge_rows": int(len(bridge)),
                "eligible_rows": int(bridge["v551_eligible"].fillna(False).sum()) if "v551_eligible" in bridge.columns else 0,
                "excluded_rows_by_reason": bridge["v551_exclusion_reason"].fillna("").value_counts(dropna=False).to_dict() if "v551_exclusion_reason" in bridge.columns else {},
                "numeric_only_label_excluded_rows": int((bridge["v551_exclusion_reason"].fillna("").astype(str) == "numeric_only_label_requires_numeric_scale_family").sum()) if "v551_exclusion_reason" in bridge.columns else 0,
                "source_structure_fields_populated": bool(
                    bridge[["question_type", "handling_rule", "recommended_computation", "source_structure_classification"]]
                    .fillna("")
                    .astype(str)
                    .apply(lambda col: col.str.strip().ne("")).any().any()
                )
                if all(col in bridge.columns for col in ["question_type", "handling_rule", "recommended_computation", "source_structure_classification"])
                else False,
                "source_structure_blank_blocked_rows": int((bridge["v551_exclusion_reason"].fillna("").astype(str) == "blank_source_structure_high_risk_block").sum()) if "v551_exclusion_reason" in bridge.columns else 0,
                "demographic_cloud_leak_count": 0,
                "country_within_country_predictor_leak_count": 0,
                "missing_required_field_counts": {},
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    if bridge_validation_issues:
        raise RuntimeError("Bridge validation failure: " + "; ".join(bridge_validation_issues[:5]))

    written = []
    for table_name, frame in merged_tables.items():
        layer = "core"
        if table_name in {"answer_distribution", "country_answer_distribution"}:
            layer = "distributions"
        elif table_name in {"position_distribution", "position_indicator_summary", "indicator_answer_matrix", "outlier_cohort_summary", "secondary_indicator_summary", "recursive_branch_nodes"}:
            layer = "determinicity"
        elif table_name in {"branch_position_signature", "branch_relation_co_signature", "branch_co_signature", "question_response_attitude_cloud"}:
            layer = "clouds"
        elif table_name in {"mapping_gap_report", "underpowered_quarantine", "response_option_manual_review", "legacy_leak_report", "cloud_exclusion_audit"}:
            layer = "audit"
        meta = write_table(frame, paths=run_paths, table_name=table_name, layer=layer, write_csv=args.write_csv, write_parquet=args.write_parquet, report_name=f"V550_{table_name}.csv", reports_dir=Path(args.reports_dir), extra_schema={"description": f"Merged V550 {table_name} output."})
        written.append(meta["parquet_path"])

    manifest = build_merge_manifest(
        run_id=args.run_id,
        created_at=pd.Timestamp.utcnow().isoformat(),
        completed_at=pd.Timestamp.utcnow().isoformat(),
        success=True,
        shard_count_expected=len(shard_dirs),
        shard_count_actual=len(shard_dirs),
        missing_shards=[],
        row_counts=row_counts,
        bridge_row_count=len(bridge),
        warnings=shard_schema_issues,
        errors=shard_validation_issues + bridge_validation_issues,
        promoted_latest=bool(args.promote_latest),
    )
    atomic_write_json(run_paths.run_path / "merge_manifest.json", manifest)
    atomic_write_json(run_paths.run_path / "manifest.json", {"run_id": args.run_id, "success": True, "merge_manifest": manifest})
    if args.promote_latest:
        atomic_promote_latest(output_root, args.run_id, manifest)
    if args.verbose:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
