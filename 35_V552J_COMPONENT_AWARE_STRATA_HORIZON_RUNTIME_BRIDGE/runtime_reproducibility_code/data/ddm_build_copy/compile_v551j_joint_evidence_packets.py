#!/usr/bin/env python3
"""Compile V551J candidate evidence packets."""

from __future__ import annotations

import argparse
from io import StringIO
import sys
from pathlib import Path
from time import monotonic

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def _contract_csv_text(frame: pd.DataFrame) -> str:
    return frame.to_csv(index=False, float_format="%.13f")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, file_hash, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v551j_review import (
    build_v551j_review_readiness_report,
    build_v551j_review_surface,
    build_v551j_reviewable_evidence_sidecar,
)
from data.ddm_build_copy.ddm_v551j_certification import build_v551j_certified_packet_index, build_v551j_status_conflict_audit, certify_v551j_v2_2_3
from data.ddm_build_copy.ddm_v551j_packets import (
    build_v551j_candidate_trace,
    build_v551j_join_key_diagnostics,
    build_v551j_joint_outputs_v2,
    build_v551j_readiness_report,
)
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_COMPILER_VERSION,
    V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
    V551J_INPUT_PROVENANCE_AUDIT_SCHEMA,
    V551J_INPUT_PROVENANCE_MANIFEST_SCHEMA,
    V551J_JOIN_KEY_DIAGNOSTICS_SCHEMA,
    V551J_PACKET_CANDIDATE_TRACE_SCHEMA,
    V551J_PACKET_EXCLUSION_AUDIT_SCHEMA,
    V551J_PACKET_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_AUDIT_SCHEMA,
    V551J_CERTIFICATION_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA,
    V551J_CERTIFIED_PACKET_INDEX_SCHEMA,
    V551J_REVIEW_READINESS_REPORT_SCHEMA,
    V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA,
    V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA,
    V551J_REVIEW_SURFACE_SCHEMA,
    V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA,
)
from data.ddm_build_copy.ddm_v551j_validation import validate_candidate_trace_schema, validate_review_surface_schema, validate_reviewable_evidence_sidecar_schema, validate_certification_audit_schema, validate_certification_readiness_report_schema, validate_certification_rejection_audit_schema, validate_certified_packet_index_schema, validate_v551j_v2_2_3_outputs, validate_written_v551j_artifacts
from data.ddm_build_copy.ddm_v551j_contract import recompute_joint_measurement_contract_hash, recompute_v551j_component_contract_hash, recompute_v551j_v2_2_3_packet_contract_hash
from data.ddm_build_copy.ddm_v550_schema import write_schema_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V551J candidate evidence packets.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551-atoms-path", required=True)
    parser.add_argument("--v550j-pattern-index-path", required=True)
    parser.add_argument("--v550j-pattern-item-index-path", required=True)
    parser.add_argument("--v550j-relation-signature-path", required=True)
    parser.add_argument("--v550j-manifest-path", required=True)
    parser.add_argument("--v550j-readiness-report-path", required=True)
    parser.add_argument("--registry-path", required=True)
    parser.add_argument("--v550j-meaning-summary-path", default=None)
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v551j" / "runs"))
    parser.add_argument("--v550j-position-signature-path", default=None)
    parser.add_argument("--v550j-association-index-path", default=None)
    parser.add_argument("--v550j-review-surface-path", default=None)
    parser.add_argument("--v552-question-semantic-hierarchy-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-structural-channel-index-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-relation-axis-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-target-entity-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-driver-facet-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-contradiction-surface-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-horizon-constraint-index-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-parent-prior-manifest-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--emit-review-surface", action="store_true", default=False)
    parser.add_argument("--emit-certified-index", action="store_true", default=False)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _load(path: str | None) -> pd.DataFrame:
    return read_table(path) if path else pd.DataFrame()


def _row_count(frame: pd.DataFrame) -> int:
    return int(len(frame)) if frame is not None else 0


def _log_stage(enabled: bool, label: str, detail: str = "") -> None:
    if not enabled:
        return
    message = f"[V551J] {label}"
    if detail:
        message = f"{message}: {detail}"
    print(message, flush=True)


def main() -> int:
    args = parse_args()
    if args.emit_certified_index and not args.emit_review_surface:
        raise RuntimeError("V551J_C_CERTIFICATION_REQUIRES_REVIEW_SURFACE: pass --emit-review-surface with --emit-certified-index")
    output_dirs = ensure_output_dirs(args.output_root, args.run_id)
    sidecar_dir = output_dirs["root"] / "sidecars"
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    required_paths = {
        "v551_atoms_path": args.v551_atoms_path,
        "v550j_pattern_index_path": args.v550j_pattern_index_path,
        "v550j_pattern_item_index_path": args.v550j_pattern_item_index_path,
        "v550j_relation_signature_path": args.v550j_relation_signature_path,
        "v550j_manifest_path": args.v550j_manifest_path,
        "v550j_readiness_report_path": args.v550j_readiness_report_path,
        "registry_path": args.registry_path,
    }
    missing_required = [name for name, path in required_paths.items() if not path or not Path(path).exists()]
    if missing_required:
        write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", {
            "run_id": args.run_id,
            "schema_version": "v2.2.3",
            "compiler_version": V551J_COMPILER_VERSION,
            "final_status": "BLOCKED_V551J_MISSING_REQUIRED_INPUTS",
            "blockers_json": missing_required,
            "ready_for_v552j_joint_evidence": False,
            "ready_for_v553": False,
            "created_at": utc_now(),
        })
        print("BLOCKED_V551J_MISSING_REQUIRED_INPUTS")
        return 1
    started = monotonic()
    atoms = _load(args.v551_atoms_path)
    pattern_index = _load(args.v550j_pattern_index_path)
    pattern_item_index = _load(args.v550j_pattern_item_index_path)
    relation_signature = _load(args.v550j_relation_signature_path)
    association_index = _load(args.v550j_association_index_path)
    position_signature = _load(args.v550j_position_signature_path)
    meaning_summary = _load(args.v550j_meaning_summary_path)
    deprecated_v552_inputs = {
        "v552_question_semantic_hierarchy_path": args.v552_question_semantic_hierarchy_path,
        "v552_structural_channel_index_path": args.v552_structural_channel_index_path,
        "v552_relation_axis_pressure_path": args.v552_relation_axis_pressure_path,
        "v552_target_entity_pressure_path": args.v552_target_entity_pressure_path,
        "v552_driver_facet_pressure_path": args.v552_driver_facet_pressure_path,
        "v552_contradiction_surface_path": args.v552_contradiction_surface_path,
        "v552_horizon_constraint_index_path": args.v552_horizon_constraint_index_path,
        "v552_parent_prior_manifest_path": args.v552_parent_prior_manifest_path,
    }
    required_input_hashes = {
        "v551_atoms_artifact_hash": file_hash(args.v551_atoms_path),
        "v550j_pattern_index_artifact_hash": file_hash(args.v550j_pattern_index_path),
        "v550j_pattern_item_index_artifact_hash": file_hash(args.v550j_pattern_item_index_path),
        "v550j_relation_signature_artifact_hash": file_hash(args.v550j_relation_signature_path),
        "v550j_manifest_hash": file_hash(args.v550j_manifest_path),
        "v550j_readiness_report_hash": file_hash(args.v550j_readiness_report_path),
        "question_family_registry_hash": file_hash(args.registry_path),
    }

    def _input_provenance_audit(scope_audit: pd.DataFrame) -> pd.DataFrame:
        import re
        scope_status = dict(zip(scope_audit.get("artifact_name", pd.Series(dtype=str)).astype(str), scope_audit.get("scope_contract_status", pd.Series(dtype=str)).astype(str))) if not scope_audit.empty else {}
        rows = []
        specs = [
            ("v551_atoms", args.v551_atoms_path, required_input_hashes["v551_atoms_artifact_hash"]),
            ("v550j_pattern_index", args.v550j_pattern_index_path, required_input_hashes["v550j_pattern_index_artifact_hash"]),
            ("v550j_pattern_item_index", args.v550j_pattern_item_index_path, required_input_hashes["v550j_pattern_item_index_artifact_hash"]),
            ("v550j_relation_signature", args.v550j_relation_signature_path, required_input_hashes["v550j_relation_signature_artifact_hash"]),
            ("v550j_manifest", args.v550j_manifest_path, required_input_hashes["v550j_manifest_hash"]),
            ("v550j_readiness_report", args.v550j_readiness_report_path, required_input_hashes["v550j_readiness_report_hash"]),
            ("question_family_registry", args.registry_path, required_input_hashes["question_family_registry_hash"]),
        ]
        for artifact_name, input_path, expected_hash in specs:
            path = Path(input_path)
            exists = path.exists()
            actual_hash = file_hash(path)
            rows.append({
                "run_id": args.run_id,
                "artifact_name": artifact_name,
                "input_path": str(path),
                "size_bytes": path.stat().st_size if exists else "",
                "sha256": actual_hash,
                "exists": exists,
                "hash_format_valid": bool(re.fullmatch(r"[0-9a-f]{64}", actual_hash)),
                "hash_matches_file": exists and actual_hash == file_hash(path),
                "expected_governed_hash": expected_hash,
                "governed_hash_matches": actual_hash == expected_hash,
                "scope_status": scope_status.get(artifact_name, "PASS"),
                "created_at": utc_now(),
                "schema_version": "v2.2.3",
                "compiler_version": V551J_COMPILER_VERSION,
            })
        return pd.DataFrame(rows).reindex(columns=V551J_INPUT_PROVENANCE_AUDIT_SCHEMA["required_columns"])

    outputs = build_v551j_joint_outputs_v2(
        run_id=args.run_id,
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_item_index=pattern_item_index,
        relation_signature=relation_signature,
        registry_path=args.registry_path,
        v550j_manifest_path=args.v550j_manifest_path,
        v550j_readiness_report_path=args.v550j_readiness_report_path,
        association_index=association_index,
        position_signature=position_signature,
        meaning_summary=meaning_summary,
        deprecated_v552_inputs_supplied=sum(1 for value in deprecated_v552_inputs.values() if value),
        input_hashes=required_input_hashes,
    )
    outputs["input_provenance_audit"] = _input_provenance_audit(outputs["input_scope_audit"])
    finalized_candidate, certified, certification_audit, certification_rejection = certify_v551j_v2_2_3(
        outputs["candidate"],
        outputs["component"],
        outputs["packet_contract_validation_report"],
    )
    outputs["candidate"] = finalized_candidate
    outputs["certified"] = certified
    outputs["certification_audit"] = certification_audit
    outputs["certification_rejection_audit"] = certification_rejection
    def _refresh_packet_hashes() -> None:
        csv_component = pd.read_csv(StringIO(_contract_csv_text(outputs["component"])), dtype=str, keep_default_na=False) if not outputs["component"].empty else outputs["component"].copy()
        if not csv_component.empty:
            component_hashes = [recompute_v551j_component_contract_hash(row) for _, row in csv_component.iterrows()]
            outputs["component"]["component_contract_hash"] = component_hashes
            csv_component["component_contract_hash"] = component_hashes
        csv_candidate = pd.read_csv(StringIO(_contract_csv_text(outputs["candidate"])), dtype=str, keep_default_na=False) if not outputs["candidate"].empty else outputs["candidate"].copy()
        if not csv_candidate.empty:
            measurement_hashes = [recompute_joint_measurement_contract_hash(row) for _, row in csv_candidate.iterrows()]
            outputs["candidate"]["joint_measurement_contract_hash"] = measurement_hashes
        csv_candidate = pd.read_csv(StringIO(_contract_csv_text(outputs["candidate"])), dtype=str, keep_default_na=False) if not outputs["candidate"].empty else outputs["candidate"].copy()
        if not csv_candidate.empty:
            packet_hashes = []
            for _, packet_row in csv_candidate.iterrows():
                component_rows = csv_component[csv_component["packet_id"].astype(str).eq(str(packet_row.get("packet_id")))].sort_values("item_order", kind="mergesort").to_dict("records")
                packet_hashes.append(recompute_v551j_v2_2_3_packet_contract_hash(packet_row, component_rows))
            outputs["candidate"]["packet_contract_hash"] = packet_hashes
        if not outputs["certified"].empty:
            hash_map = dict(zip(outputs["candidate"]["packet_id"].astype(str), outputs["candidate"]["packet_contract_hash"].astype(str)))
            measure_map = dict(zip(outputs["candidate"]["packet_id"].astype(str), outputs["candidate"]["joint_measurement_contract_hash"].astype(str)))
            outputs["certified"]["packet_contract_hash"] = outputs["certified"]["packet_id"].astype(str).map(hash_map)
            outputs["certified"]["joint_measurement_contract_hash"] = outputs["certified"]["packet_id"].astype(str).map(measure_map)

    def _rebuild_review_surface() -> None:
        from data.ddm_build_copy.ddm_v551j_schema import V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA
        review_rows = outputs["candidate"][outputs["candidate"]["review_required"].fillna(False).astype(bool)].copy()
        if review_rows.empty:
            outputs["review_surface"] = pd.DataFrame(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
            return
        review_rows["review_priority"] = "medium"
        review_rows["review_triage_priority_score"] = 0.5
        outputs["review_surface"] = review_rows.reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])

    for frame_name in ("candidate", "certified"):
        frame = outputs[frame_name].copy()
        if not frame.empty:
            hashes = []
            for _, packet_row in frame.iterrows():
                component_rows = outputs["component"][outputs["component"]["packet_id"].astype(str).eq(str(packet_row.get("packet_id")))].sort_values("item_order", kind="mergesort").to_dict("records")
                hashes.append(recompute_v551j_v2_2_3_packet_contract_hash(packet_row, component_rows))
            frame["packet_contract_hash"] = hashes
            outputs[frame_name] = frame
    _refresh_packet_hashes()
    _rebuild_review_surface()
    outputs["readiness_report"]["candidate_packet_count"] = int(len(finalized_candidate))
    outputs["readiness_report"]["certified_packet_count"] = int(len(certified))
    outputs["readiness_report"]["review_required_packet_count"] = int(finalized_candidate["review_required"].fillna(False).astype(bool).sum())
    outputs["readiness_report"]["blocked_packet_count"] = int(finalized_candidate["certification_status"].astype(str).str.startswith("BLOCKED").sum())
    outputs["readiness_report"]["ready_for_review"] = bool(outputs["readiness_report"]["review_required_packet_count"])
    outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = bool(len(certified)) and bool(outputs["packet_contract_validation_report"].get("candidate_contract_valid"))
    outputs["readiness_report"]["final_status"] = (
        "READY_V551J_JOINT_EVIDENCE_CONTRACT"
        if outputs["readiness_report"]["ready_for_v552j_joint_evidence"]
        else "EMPTY_VALID_V551J_NO_RELATIONAL_EVIDENCE"
        if not atoms.shape[0] and not pattern_index.shape[0]
        else "BLOCKED_PACKET_CONTRACT"
    )
    validation_issues = []
    if str(outputs["readiness_report"].get("registry_contract_status")) != "MATCHED_GOVERNED_REGISTRY_HASH":
        validation_issues.append("registry_hash_mismatch")
    if str(outputs["readiness_report"].get("scope_contract_status")) != "PASS":
        validation_issues.append("scope_contract_mismatch")
    provenance_failures = outputs["input_provenance_audit"]
    if not provenance_failures.empty:
        bad_provenance = provenance_failures[
            ~provenance_failures["exists"].astype(bool)
            | ~provenance_failures["hash_format_valid"].astype(bool)
            | ~provenance_failures["hash_matches_file"].astype(bool)
            | ~provenance_failures["governed_hash_matches"].astype(bool)
            | provenance_failures["scope_status"].astype(str).ne("PASS")
        ]
        if not bad_provenance.empty:
            validation_issues.append("input_provenance_failure")
    strict_failed = False
    if validation_issues:
        outputs["packet_contract_validation_report"]["candidate_contract_valid"] = False
        outputs["packet_contract_validation_report"]["component_contract_valid"] = False
        outputs["packet_contract_validation_report"]["issue_count"] = len(validation_issues)
        outputs["packet_contract_validation_report"]["issues_json"] = __import__("json").dumps(validation_issues, sort_keys=True)
        outputs["readiness_report"]["candidate_contract_valid"] = False
        outputs["readiness_report"]["component_contract_valid"] = False
        outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = False
        outputs["readiness_report"]["final_status"] = "BLOCKED_V551J_OUTPUT_CONTRACT"
        outputs["readiness_report"]["blockers_json"] = __import__("json").dumps(validation_issues, sort_keys=True)
        if args.strict:
            strict_failed = True
            frame = outputs.get("candidate")
            if frame is not None and not frame.empty:
                for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                    if column in frame.columns:
                        frame[column] = False
                frame["certification_status"] = "BLOCKED_PACKET_CONTRACT"
                frame["review_required"] = False
                frame["review_reason_codes_json"] = "[]"
                if "blocking_reason_codes_json" in frame.columns:
                    frame["blocking_reason_codes_json"] = __import__("json").dumps(validation_issues, sort_keys=True)
                if "allowed_future_targets_json" in frame.columns:
                    frame["allowed_future_targets_json"] = "[]"
                if "runtime_use_class" in frame.columns:
                    frame["runtime_use_class"] = "not_runtime_consumable"
            outputs["candidate"] = frame
            if not outputs["certification_audit"].empty:
                outputs["certification_audit"]["certified"] = False
                outputs["certification_audit"]["certification_blockers_json"] = __import__("json").dumps(validation_issues, sort_keys=True)
            outputs["certified"] = outputs["certified"].iloc[0:0].copy()
            outputs["review_surface"] = outputs["review_surface"].iloc[0:0].copy()
            _refresh_packet_hashes()
            _rebuild_review_surface()
            for frame_name in ("candidate", "certified", "review_surface"):
                frame = outputs.get(frame_name)
                if frame is None or frame.empty:
                    continue
                for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                    if column in frame.columns:
                        frame[column] = False
                if "allowed_future_targets_json" in frame.columns:
                    frame["allowed_future_targets_json"] = "[]"
                if "runtime_use_class" in frame.columns:
                    frame["runtime_use_class"] = "not_runtime_consumable"
            outputs[frame_name] = frame
    if not args.strict:
        outputs["readiness_report"]["final_status"] = "DIAGNOSTIC_V551J_NO_STRICT_NOT_READY"
        outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = False
        for frame_name in ("candidate", "certified", "review_surface"):
            frame = outputs.get(frame_name)
            if frame is None or frame.empty:
                continue
            for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage"):
                if column in frame.columns:
                    frame[column] = False
            if "allowed_future_targets_json" in frame.columns:
                frame["allowed_future_targets_json"] = "[]"
            for column in ("ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                if column in frame.columns:
                    frame[column] = False
            if "runtime_use_class" in frame.columns:
                frame["runtime_use_class"] = "not_runtime_consumable"
            outputs[frame_name] = frame
        if not outputs["candidate"].empty:
            pass
        if not outputs["certification_audit"].empty:
            outputs["certification_audit"]["certified"] = False
            outputs["certification_audit"]["certification_notes_json"] = "[\"diagnostic_no_strict\"]"
        outputs["certified"] = outputs["certified"].iloc[0:0].copy()
        _refresh_packet_hashes()
        _rebuild_review_surface()
        outputs["readiness_report"]["certified_packet_count"] = 0
        outputs["readiness_report"]["review_required_packet_count"] = int(len(outputs["review_surface"]))
        outputs["readiness_report"]["ready_for_review"] = bool(len(outputs["review_surface"]))
    outputs["readiness_report"]["candidate_packet_count"] = int(len(outputs["candidate"]))
    outputs["readiness_report"]["certified_packet_count"] = int(len(outputs["certified"]))
    outputs["readiness_report"]["review_required_packet_count"] = int(outputs["candidate"].get("review_required", pd.Series(dtype=str)).astype(str).str.lower().eq("true").sum()) if not outputs["candidate"].empty else 0
    outputs["readiness_report"]["blocked_packet_count"] = int(outputs["candidate"].get("certification_status", pd.Series(dtype=str)).astype(str).str.startswith("BLOCKED").sum()) if not outputs["candidate"].empty else 0
    outputs["readiness_report"]["ready_for_review"] = bool(len(outputs["review_surface"]))
    outputs["input_provenance_manifest"]["row_counts"]["candidate"] = int(len(outputs["candidate"]))
    outputs["input_provenance_manifest"]["row_counts"]["component"] = int(len(outputs["component"]))
    outputs["input_provenance_manifest"]["row_counts"]["certified"] = int(len(outputs["certified"]))
    outputs["input_provenance_manifest"]["row_counts"]["review_surface"] = int(len(outputs["review_surface"]))
    outputs["input_provenance_manifest"]["final_status"] = outputs["readiness_report"]["final_status"]
    frame_targets = {
        "candidate": (output_dirs["packets"] / "v551j_joint_packet_candidate_index.parquet", "v551j_joint_packet_candidate_index"),
        "component": (output_dirs["packets"] / "v551j_joint_component_index.parquet", "v551j_joint_component_index"),
        "certified": (output_dirs["packets"] / "v551j_certified_joint_packet_index.parquet", "v551j_certified_joint_packet_index"),
        "review_surface": (output_dirs["packets"] / "v551j_review_surface.parquet", "v551j_review_surface"),
        "pattern_context_sidecar": (sidecar_dir / "v551j_pattern_context_sidecar.parquet", "v551j_pattern_context_sidecar"),
        "association_context_sidecar": (sidecar_dir / "v551j_association_context_sidecar.parquet", "v551j_association_context_sidecar"),
        "position_context_sidecar": (sidecar_dir / "v551j_position_context_sidecar.parquet", "v551j_position_context_sidecar"),
        "meaning_summary_sidecar": (sidecar_dir / "v551j_meaning_summary_sidecar.parquet", "v551j_meaning_summary_sidecar"),
        "component_match_audit": (output_dirs["audits"] / "v551j_component_match_audit.parquet", "v551j_component_match_audit"),
        "cross_contract_comparison_audit": (output_dirs["audits"] / "v551j_cross_contract_comparison_audit.parquet", "v551j_cross_contract_comparison_audit"),
        "target_layer_audit": (output_dirs["audits"] / "v551j_target_layer_audit.parquet", "v551j_target_layer_audit"),
        "denominator_separation_audit": (output_dirs["audits"] / "v551j_denominator_separation_audit.parquet", "v551j_denominator_separation_audit"),
        "measurement_separation_audit": (output_dirs["audits"] / "v551j_measurement_separation_audit.parquet", "v551j_measurement_separation_audit"),
        "certification_audit": (output_dirs["audits"] / "v551j_certification_audit.parquet", "v551j_certification_audit"),
        "certification_rejection_audit": (output_dirs["audits"] / "v551j_certification_rejection_audit.parquet", "v551j_certification_rejection_audit"),
        "input_scope_audit": (output_dirs["audits"] / "v551j_input_scope_audit.parquet", "v551j_input_scope_audit"),
        "input_provenance_audit": (output_dirs["audits"] / "v551j_input_provenance_audit.parquet", "v551j_input_provenance_audit"),
        "registry_contract_audit": (output_dirs["audits"] / "v551j_registry_contract_audit.parquet", "v551j_registry_contract_audit"),
    }
    artifact_info: dict[str, dict[str, object]] = {}
    for key, (path, name) in frame_targets.items():
        frame = outputs[key]
        artifact_info[key] = write_frame_artifact(
            frame,
            path=path,
            schema_path=output_dirs["schemas"] / f"{name}.schema.json",
            name=name,
            run_id=args.run_id,
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
        )
    compatibility = outputs["candidate"].copy()
    compatibility["compatibility_projection_only"] = True
    compatibility["not_authoritative_v2_artifact"] = True
    artifact_info["compatibility_candidate_trace"] = write_frame_artifact(
        compatibility,
        path=output_dirs["packets"] / "v551j_packet_candidate_trace.parquet",
        schema_path=output_dirs["schemas"] / "v551j_packet_candidate_trace.schema.json",
        name="v551j_packet_candidate_trace",
        run_id=args.run_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    artifact_info["compatibility_certified_packet_index"] = write_frame_artifact(
        outputs["certified"],
        path=output_dirs["packets"] / "v551j_certified_packet_index.parquet",
        schema_path=output_dirs["schemas"] / "v551j_certified_packet_index.schema.json",
        name="v551j_certified_packet_index",
        run_id=args.run_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    if args.write_csv:
        execution_mode = "strict_blocked" if strict_failed else "diagnostic" if not args.strict else "acceptance"
        written_issues = validate_written_v551j_artifacts(
            candidate_path=output_dirs["packets"] / "v551j_joint_packet_candidate_index.csv",
            component_path=output_dirs["packets"] / "v551j_joint_component_index.csv",
            certified_path=output_dirs["packets"] / "v551j_certified_joint_packet_index.csv",
            review_path=output_dirs["packets"] / "v551j_review_surface.csv",
            certification_audit_path=output_dirs["audits"] / "v551j_certification_audit.csv",
            expected_registry_hash=required_input_hashes["question_family_registry_hash"],
            execution_mode=execution_mode,
        )
        if written_issues:
            outputs["packet_contract_validation_report"]["candidate_contract_valid"] = False
            outputs["packet_contract_validation_report"]["component_contract_valid"] = False
            outputs["packet_contract_validation_report"]["issue_count"] = len(written_issues)
            outputs["packet_contract_validation_report"]["issues_json"] = __import__("json").dumps(written_issues, sort_keys=True)
            outputs["readiness_report"]["candidate_contract_valid"] = False
            outputs["readiness_report"]["component_contract_valid"] = False
            if args.strict:
                outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = False
                outputs["readiness_report"]["final_status"] = "BLOCKED_V551J_OUTPUT_CONTRACT"
            outputs["readiness_report"]["blockers_json"] = __import__("json").dumps(written_issues, sort_keys=True)
            strict_failed = bool(args.strict)
        else:
            if not strict_failed:
                outputs["packet_contract_validation_report"]["candidate_contract_valid"] = True
                outputs["packet_contract_validation_report"]["component_contract_valid"] = True
                outputs["packet_contract_validation_report"]["issue_count"] = 0
                outputs["packet_contract_validation_report"]["issues_json"] = "[]"
            if not args.strict:
                outputs["readiness_report"]["final_status"] = "DIAGNOSTIC_V551J_NO_STRICT_NOT_READY"
                outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = False
            if strict_failed:
                outputs["packet_contract_validation_report"]["candidate_contract_valid"] = False
                outputs["packet_contract_validation_report"]["component_contract_valid"] = False
    provenance = outputs["input_provenance_manifest"]
    provenance.update({
        **capture_run_provenance(input_documents={**required_paths, **{k: v or "" for k, v in deprecated_v552_inputs.items()}}),
        "output_artifacts": artifact_info,
        "elapsed_seconds": round(monotonic() - started, 3),
    })
    write_json_artifact(output_dirs["manifest"] / "v551j_input_contract_report.json", outputs["input_contract_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_packet_contract_validation_report.json", outputs["packet_contract_validation_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", outputs["readiness_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_input_provenance_manifest.json", provenance)
    write_json_artifact(output_dirs["manifest"] / "manifest.json", {
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": outputs["readiness_report"].get("final_status"),
        "ready_for_v552j_joint_evidence": outputs["readiness_report"].get("ready_for_v552j_joint_evidence"),
        "ready_for_v553": False,
        "row_counts": outputs["input_provenance_manifest"].get("row_counts", {}),
        "output_artifacts": artifact_info,
        "created_at": utc_now(),
    })
    print(outputs["readiness_report"]["final_status"])
    return 1 if strict_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
