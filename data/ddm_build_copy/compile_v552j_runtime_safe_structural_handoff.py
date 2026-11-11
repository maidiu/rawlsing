#!/usr/bin/env python3
"""Compile the provisional V552J runtime-safe structural handoff adapter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from time import monotonic

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v552j_handoff import build_v552j_structural_handoff, validate_v552j_structural_handoff
from data.ddm_build_copy.ddm_v552j_validation import (
    validate_blocked_index,
    validate_downstream_leakage_audit,
    validate_forbidden_inference_audit,
    validate_diagnostic_only_index,
    validate_input_artifact_audit,
    validate_permission_boundary_audit,
    validate_review_only_index,
    validate_readiness_report,
    validate_runtime_handoff_manifest,
    validate_status_conflict_audit,
    validate_structural_absence_packet,
    validate_structural_constraint_packet,
    validate_structural_context_packet,
    validate_structural_context_only_index,
    validate_structural_uncertainty_packet,
    validate_to_v553_handoff_index,
    validate_v553_handoff_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the provisional V552J structural handoff adapter.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551j-run-root", required=True)
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v552j" / "runs"))
    parser.add_argument("--v551j-comparison-root", default=None)
    parser.add_argument("--v552-question-semantic-hierarchy-path", default=None)
    parser.add_argument("--v552-structural-channel-index-path", default=None)
    parser.add_argument("--v552-relation-axis-pressure-path", default=None)
    parser.add_argument(
        "--v552-target_entity_pressure-path",
        "--v552-target-entity-pressure-path",
        dest="v552_target_entity_pressure_path",
        default=None,
    )
    parser.add_argument("--v552-driver-facet-pressure-path", default=None)
    parser.add_argument("--v552-contradiction-surface-path", default=None)
    parser.add_argument("--v552-horizon-constraint-index-path", default=None)
    parser.add_argument("--v552-parent-prior-manifest-path", default=None)
    parser.add_argument("--v552-artifact-authority-index-path", default=None)
    parser.add_argument("--v552-known-absence-register-path", default=None)
    parser.add_argument("--v552-structural-fact-index-path", default=None)
    parser.add_argument("--v552-temporal-key-source-index-path", default=None)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _log_stage(enabled: bool, label: str, detail: str = "") -> None:
    if not enabled:
        return
    message = f"[V552J] {label}"
    if detail:
        message = f"{message}: {detail}"
    print(message, flush=True)


def main() -> int:
    args = parse_args()
    started = monotonic()
    output_dirs = ensure_output_dirs(args.output_root, args.run_id)

    _log_stage(args.verbose, "stage 1/5", "building structural handoff")
    summary = build_v552j_structural_handoff(
        run_id=args.run_id,
        v551j_run_root=args.v551j_run_root,
        output_root=args.output_root,
        v551j_comparison_root=args.v551j_comparison_root,
        v552_question_semantic_hierarchy_path=args.v552_question_semantic_hierarchy_path,
        v552_structural_channel_index_path=args.v552_structural_channel_index_path,
        v552_relation_axis_pressure_path=args.v552_relation_axis_pressure_path,
        v552_target_entity_pressure_path=args.v552_target_entity_pressure_path or args.v552_target_entity_pressure_path,
        v552_driver_facet_pressure_path=args.v552_driver_facet_pressure_path,
        v552_contradiction_surface_path=args.v552_contradiction_surface_path,
        v552_horizon_constraint_index_path=args.v552_horizon_constraint_index_path,
        v552_parent_prior_manifest_path=args.v552_parent_prior_manifest_path,
        v552_artifact_authority_index_path=args.v552_artifact_authority_index_path,
        v552_known_absence_register_path=args.v552_known_absence_register_path,
        v552_structural_fact_index_path=args.v552_structural_fact_index_path,
        v552_temporal_key_source_index_path=args.v552_temporal_key_source_index_path,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    _log_stage(args.verbose, "stage 1/5 complete", f"status={summary['status']}")

    _log_stage(args.verbose, "stage 2/5", "validating structural packets")
    errors = []
    errors.extend(validate_structural_constraint_packet(summary["constraint_df"]))
    errors.extend(validate_structural_context_packet(summary["context_df"]))
    errors.extend(validate_structural_absence_packet(summary["absence_df"]))
    errors.extend(validate_structural_uncertainty_packet(summary["uncertainty_df"]))
    errors.extend(validate_forbidden_inference_audit(summary["audit_df"]))
    errors.extend(validate_input_artifact_audit(summary["input_artifact_audit_df"]))
    errors.extend(validate_permission_boundary_audit(summary["permission_boundary_df"]))
    errors.extend(validate_downstream_leakage_audit(summary["downstream_leakage_df"]))
    errors.extend(validate_status_conflict_audit(summary["status_conflict_audit_df"]))
    errors.extend(validate_structural_context_only_index(summary["structural_context_only_index_df"]))
    errors.extend(validate_review_only_index(summary["review_only_index_df"]))
    errors.extend(validate_diagnostic_only_index(summary["diagnostic_only_index_df"]))
    errors.extend(validate_blocked_index(summary["blocked_index_df"]))
    errors.extend(validate_to_v553_handoff_index(summary["to_v553_handoff_index_df"]))
    errors.extend(validate_v553_handoff_manifest(pd.DataFrame([summary["v553_handoff_manifest"]])))
    errors.extend(validate_runtime_handoff_manifest(pd.DataFrame([summary["manifest"]])))
    errors.extend(validate_readiness_report(pd.DataFrame([summary["readiness"]])))
    errors.extend(validate_v552j_structural_handoff(summary))
    if args.strict and errors:
        raise RuntimeError("V552J_VALIDATION_FAILED: " + "; ".join(errors))
    _log_stage(args.verbose, "stage 2/5 complete", "validation_passed" if not errors else f"validation_errors={len(errors)}")

    _log_stage(args.verbose, "stage 3/5", "artifacts already written by the builder")
    required_paths = [
        "packet_path",
        "absence_path",
        "uncertainty_path",
        "audit_path",
        "status_conflict_audit_path",
        "input_artifact_audit_path",
        "permission_boundary_audit_path",
        "downstream_leakage_audit_path",
        "structural_context_only_index_path",
        "review_only_index_path",
        "diagnostic_only_index_path",
        "blocked_index_path",
        "blocker_context_breakdown_path",
        "to_v553_handoff_index_path",
        "v553_input_index_path",
        "manifest_path",
        "input_artifact_index_path",
        "authority_normalization_report_path",
        "readiness_path",
        "v553_handoff_manifest_path",
        "handoff_packet_path",
    ]
    if any(not Path(summary[path_key]).exists() for path_key in required_paths):
        raise RuntimeError("V552J_ARTIFACT_WRITE_FAILED: expected output files were not created")
    _log_stage(args.verbose, "stage 3/5 complete", f"packet_rows={summary['manifest']['packet_rows']} handoff_packet_written=True")

    _log_stage(args.verbose, "stage 4/5", "writing schemas")
    required_schema_paths = [
        "constraint",
        "context",
        "absence",
        "uncertainty",
        "audit",
        "input_artifact_audit",
        "permission_boundary_audit",
        "downstream_leakage_audit",
        "status_conflict_audit",
        "structural_context_only_index",
        "review_only_index",
        "diagnostic_only_index",
        "blocked_index",
        "blocker_context_breakdown",
        "to_v553_handoff_index",
        "v553_input_index",
        "manifest",
        "input_artifact_index",
        "authority_normalization_report",
        "readiness",
        "v553_handoff_manifest",
    ]
    if any(not Path(summary["schema_paths"][schema_key]).exists() for schema_key in required_schema_paths) or not Path(summary["handoff_schema_path"]).exists():
        raise RuntimeError("V552J_SCHEMA_WRITE_FAILED: expected schema files were not created")
    _log_stage(args.verbose, "stage 4/5 complete", "schemas_written")

    _log_stage(args.verbose, "stage 5/5", "done")
    if args.verbose:
        elapsed = monotonic() - started
        print(f"[V552J] completed in {elapsed:.1f}s -> {output_dirs['root']}", flush=True)
    print(summary["status"])
    print(summary["readiness_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
