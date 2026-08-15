#!/usr/bin/env python3
"""Compile deterministic V551 relation-evidence atoms from V550 bridge outputs."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v551_atoms import (
    build_v551_blocked_signal_audit,
    build_v551_certification_candidate_bridge,
    build_v551_eligible_bridge_atom_coverage_audit,
    build_v551_exclusion_samples,
    build_v551_exclusion_summary,
    build_v551_lineage_basis_audit,
    build_v551_numeric_wrapper_audit,
    build_v551_pressure_component_audit,
    build_v551_relation_evidence_atoms,
    build_v551_relation_review_surface,
    summarize_v551_denominator_contract,
    validate_v551_atom_contract,
    validate_v551_bridge_input_contract,
)
from data.ddm_build_copy.ddm_v551_directionality_expectation import (
    build_v551_directionality_stamp_audit,
    summarize_v551_directionality_stamp_coverage,
)
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v550_schema import V551_ATOM_EXCLUSION_AUDIT_SCHEMA, V551_BLOCKED_SIGNAL_AUDIT_SCHEMA, V551_LINEAGE_BASIS_AUDIT_SCHEMA, V551_NUMERIC_WRAPPER_AUDIT_SCHEMA, V551_PRESSURE_COMPONENT_AUDIT_SCHEMA, V551_RELATION_EVIDENCE_ATOMS_SCHEMA, V551_RELATION_REVIEW_SURFACE_SCHEMA, dataframe_schema_json, write_schema_json

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v551" / "runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile deterministic V551 relation-evidence atoms.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--bridge-path", required=True)
    parser.add_argument("--question-use-contract-path", default=None)
    parser.add_argument("--source-structure-audit-path", default=None)
    parser.add_argument("--response-option-map-path", default=None)
    parser.add_argument("--source-structure-population-hash", default="")
    parser.add_argument("--question-use-contract-hash", default="")
    parser.add_argument("--response-option-map-hash", default="")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument(
        "--v551-compile-mode",
        default="legacy_full_bridge",
        choices=("legacy_full_bridge", "optimized_candidate_bridge", "compare"),
        help="Control whether V551 builds from the full bridge, a candidate bridge prefilter, or both for comparison.",
    )
    parser.add_argument(
        "--v551-audit-mode",
        default="full",
        choices=("summary", "samples", "full"),
        help="Control V551 audit depth: summary counts, sampled rows, or full row-level audits.",
    )
    parser.add_argument("--verbose", action="store_true")
    progress_group = parser.add_mutually_exclusive_group()
    progress_group.add_argument("--progress", dest="progress", action="store_true", default=True, help="Emit numbered progress updates to stderr.")
    progress_group.add_argument("--no-progress", dest="progress", action="store_false", help="Disable numbered progress updates.")
    return parser.parse_args()


def _read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    return pd.read_parquet(path)


def _frame_hash(df: pd.DataFrame) -> str:
    if df.empty:
        return "empty"
    out = df.copy()
    sort_cols = sorted(out.columns)
    for column in sort_cols:
        out[column] = out[column].fillna("").astype(str)
    out = out.sort_values(sort_cols, kind="mergesort").reset_index(drop=True)
    payload = out.to_csv(index=False).encode("utf-8")
    import hashlib

    return hashlib.sha256(payload).hexdigest()


def _write_frame(path_root: Path, name: str, frame: pd.DataFrame, *, write_csv: bool, write_parquet: bool) -> None:
    csv_path = path_root / f"{name}.csv"
    parquet_path = path_root / f"{name}.parquet"
    if write_csv:
        frame.to_csv(csv_path, index=False)
    if write_parquet:
        frame.to_parquet(parquet_path, index=False)
    write_schema_json(path_root / "schemas" / f"{name}.schema.json", frame, name=name, run_id=path_root.parent.name)


def _compare_atom_frames(legacy_atoms: pd.DataFrame, optimized_atoms: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if len(legacy_atoms) != len(optimized_atoms):
        issues.append(f"atom_row_count mismatch legacy={len(legacy_atoms)} optimized={len(optimized_atoms)}")
    legacy_keys = set(legacy_atoms.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist())
    optimized_keys = set(optimized_atoms.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist())
    if legacy_keys != optimized_keys:
        issues.append(f"atom_key_set mismatch missing_from_optimized={len(legacy_keys - optimized_keys)} extra_in_optimized={len(optimized_keys - legacy_keys)}")
    if "atom_id" in legacy_atoms.columns and "atom_id" in optimized_atoms.columns:
        legacy_atoms = legacy_atoms.sort_values(["atom_id"], kind="mergesort").reset_index(drop=True)
        optimized_atoms = optimized_atoms.sort_values(["atom_id"], kind="mergesort").reset_index(drop=True)
    compare_columns = [
        "target_entity_id",
        "relation_axis_id",
        "driver_id",
        "driver_facet_id",
        "support_status",
        "n_unweighted",
        "support_threshold",
        "directionality_status",
        "atom_contract_hash",
        "empirical_object_type",
        "empirical_object_id",
        "response_scale_signature",
        "semantic_identity_signature",
        "structural_identity_signature",
        "measurement_contract_hash",
        "pressure_evidence_class",
        "v552_pressure_component_eligible",
        "v552_pressure_component_status",
        "v552_pressure_component_ineligibility_reason",
        "allowed_as_temporal_pressure_indicator",
        "forbidden_inference",
        "known_absences",
        "evidence_basis_origin",
        "provenance_basis_origin",
        "temporal_authority_status",
    ]
    for column in compare_columns:
        if column not in legacy_atoms.columns or column not in optimized_atoms.columns:
            issues.append(f"missing_compare_column={column}")
            continue
        legacy_values = legacy_atoms[column].fillna("").astype(str).tolist()
        optimized_values = optimized_atoms[column].fillna("").astype(str).tolist()
        if legacy_values != optimized_values:
            issues.append(f"column_mismatch={column}")
    return issues


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _bridge_row_fingerprints(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    ordered = frame.copy().reset_index(drop=True)
    for column in sorted(ordered.columns):
        ordered[column] = ordered[column].fillna("").astype(str)
    ordered = ordered.loc[:, sorted(ordered.columns)]
    return sorted(pd.util.hash_pandas_object(ordered, index=False).astype(str).tolist())


def _compare_candidate_bridge_coverage(full_bridge: pd.DataFrame, candidate_bridge: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    expected_candidate = build_v551_certification_candidate_bridge(full_bridge)
    expected_fingerprints = _bridge_row_fingerprints(expected_candidate)
    actual_fingerprints = _bridge_row_fingerprints(candidate_bridge)
    if expected_fingerprints != actual_fingerprints:
        issues.append(
            "candidate_bridge coverage mismatch "
            f"expected_rows={len(expected_candidate)} actual_rows={len(candidate_bridge)}"
        )
    if len(expected_candidate) != len(candidate_bridge):
        issues.append(
            "candidate_bridge row_count mismatch "
            f"expected={len(expected_candidate)} actual={len(candidate_bridge)}"
        )
    return issues


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    run_dir = output_root / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    schemas_dir = run_dir / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)

    _total_stages = 8
    _progress_step = 0

    def log(message: str) -> None:
        if args.verbose:
            print(f"[V551] {message}", flush=True)

    def progress(message: str) -> None:
        nonlocal _progress_step
        nonlocal _current_stage
        _progress_step += 1
        _current_stage = message
        if args.progress:
            elapsed = time.monotonic() - profile_started
            print(f"[{_progress_step}/{_total_stages}] {message} ({elapsed:.0f}s)", flush=True, file=sys.stderr)

    profile_started = time.monotonic()

    _current_stage = "starting"

    def _heartbeat() -> None:
        while args.progress:
            time.sleep(30)
            elapsed = time.monotonic() - profile_started
            print(f"  ... still working on \"{_current_stage}\" ({elapsed:.0f}s elapsed)", flush=True, file=sys.stderr)

    import threading as _threading
    _heartbeat_thread = _threading.Thread(target=_heartbeat, daemon=True)
    if args.progress:
        _heartbeat_thread.start()

    progress("loading bridge input")
    log(f"loading bridge input: {args.bridge_path}")
    bridge = _read_table(Path(args.bridge_path))
    if bridge.empty:
        raise RuntimeError(f"Bridge input is empty or missing: {args.bridge_path}")
    log(f"bridge loaded: rows={len(bridge)} columns={len(bridge.columns)}")
    input_contract = validate_v551_bridge_input_contract(bridge)
    input_contract_report = {
        "run_id": args.run_id,
        **input_contract,
        "schema_version": "v2.1",
    }
    _write_json(run_dir / "v551_input_contract_report.json", input_contract_report)
    if input_contract["status"] != "PASS":
        raise RuntimeError("BLOCKED_V551_MISSING_BRIDGE_CONTRACT: " + ", ".join(input_contract["missing_columns"]))

    # Directionality completeness has its own authority-defined denominator.
    # Only substantive response rows whose variable/question contract says a
    # current directional atom is applicable are audited here.  Row-level
    # success fields are deliberately excluded from denominator selection.
    directionality_stamp_audit = build_v551_directionality_stamp_audit(bridge)
    directionality_stamp_summary = summarize_v551_directionality_stamp_coverage(
        directionality_stamp_audit
    )
    _write_json(
        run_dir / "v551_directionality_stamp_coverage_report.json",
        {"run_id": args.run_id, **directionality_stamp_summary, "schema_version": "v2.1"},
    )
    directionality_missing_stamp_rows = int(
        directionality_stamp_summary["directionality_missing_stamp_rows"]
    )

    progress("loading auxiliary inputs")
    question_use_contract = _read_table(Path(args.question_use_contract_path)) if args.question_use_contract_path else pd.DataFrame()
    source_structure_audit = _read_table(Path(args.source_structure_audit_path)) if args.source_structure_audit_path else pd.DataFrame()
    response_option_map = _read_table(Path(args.response_option_map_path)) if args.response_option_map_path else pd.DataFrame()

    log("hashing auxiliary inputs")
    question_use_contract_hash = args.question_use_contract_hash or _frame_hash(question_use_contract)
    source_structure_population_hash = args.source_structure_population_hash or _frame_hash(source_structure_audit)
    response_option_map_hash = args.response_option_map_hash or _frame_hash(response_option_map)

    progress("building atoms")
    coverage_candidate_bridge = build_v551_certification_candidate_bridge(bridge)
    candidate_bridge = bridge if args.v551_compile_mode == "legacy_full_bridge" else build_v551_certification_candidate_bridge(bridge)
    candidate_atoms, candidate_exclusion_audit = build_v551_relation_evidence_atoms(
        candidate_bridge,
        question_use_contract=question_use_contract,
        source_structure_population_audit=source_structure_audit,
        question_use_contract_hash=question_use_contract_hash,
        source_structure_population_hash=source_structure_population_hash,
        response_option_map_hash=response_option_map_hash,
    )
    if args.v551_compile_mode == "compare":
        atoms, exclusion_audit = build_v551_relation_evidence_atoms(
            bridge,
            question_use_contract=question_use_contract,
            source_structure_population_audit=source_structure_audit,
            question_use_contract_hash=question_use_contract_hash,
            source_structure_population_hash=source_structure_population_hash,
            response_option_map_hash=response_option_map_hash,
        )
        compare_issues = _compare_atom_frames(atoms, candidate_atoms)
        compare_issues.extend(_compare_candidate_bridge_coverage(bridge, candidate_bridge))
        if compare_issues:
            raise RuntimeError("V551 compare mode mismatch: " + "; ".join(compare_issues))
        bridge_for_audit = bridge
    else:
        atoms, exclusion_audit = candidate_atoms, candidate_exclusion_audit
        bridge_for_audit = candidate_bridge
    progress("building audit frames")
    numeric_wrapper_audit = build_v551_numeric_wrapper_audit(bridge_for_audit, run_id=args.run_id)
    relation_review_surface = build_v551_relation_review_surface(bridge_for_audit, run_id=args.run_id)
    blocked_signal_audit = build_v551_blocked_signal_audit(bridge_for_audit, run_id=args.run_id)
    exclusion_summary = build_v551_exclusion_summary(exclusion_audit)
    exclusion_samples = build_v551_exclusion_samples(exclusion_audit)
    pressure_component_audit = build_v551_pressure_component_audit(atoms)
    lineage_basis_audit = build_v551_lineage_basis_audit(candidate_bridge, atoms, candidate_exclusion_audit)
    eligible_bridge_atom_coverage_audit = build_v551_eligible_bridge_atom_coverage_audit(
        coverage_candidate_bridge,
        atoms,
        candidate_exclusion_audit,
    )
    atom_contract_issues = validate_v551_atom_contract(atoms)
    denominator_contract_summary = summarize_v551_denominator_contract(atoms)
    atom_contract_invalid_rows = int(len(atoms)) if atom_contract_issues else 0
    eligible_bridge_missing_atom_rows = (
        int(eligible_bridge_atom_coverage_audit["coverage_blocker"].map(lambda value: bool(value)).sum())
        if not eligible_bridge_atom_coverage_audit.empty and "coverage_blocker" in eligible_bridge_atom_coverage_audit.columns
        else 0
    )
    log(
        "frames built: "
        f"atoms={len(atoms)} exclusion={len(exclusion_audit)} numeric_wrapper={len(numeric_wrapper_audit)} "
        f"review_surface={len(relation_review_surface)} blocked_signal={len(blocked_signal_audit)}"
    )
    if args.v551_audit_mode == "summary":
        exclusion_audit = exclusion_summary
    elif args.v551_audit_mode == "samples":
        exclusion_audit = exclusion_samples

    progress("writing outputs")
    if args.write_csv:
        log("writing csv outputs")
        atoms.to_csv(run_dir / "relation_evidence_atoms.csv", index=False)
        pressure_component_audit.to_csv(run_dir / "pressure_component_audit.csv", index=False)
        lineage_basis_audit.to_csv(run_dir / "v551_lineage_basis_audit.csv", index=False)
        exclusion_audit.to_csv(run_dir / "atom_exclusion_audit.csv", index=False)
        numeric_wrapper_audit.to_csv(run_dir / "numeric_wrapper_audit.csv", index=False)
        relation_review_surface.to_csv(run_dir / "relation_review_surface.csv", index=False)
        blocked_signal_audit.to_csv(run_dir / "blocked_signal_audit.csv", index=False)
        eligible_bridge_atom_coverage_audit.to_csv(run_dir / "eligible_bridge_atom_coverage_audit.csv", index=False)
        directionality_stamp_audit.to_csv(run_dir / "directionality_stamp_audit.csv", index=False)
        candidate_bridge.to_csv(run_dir / "certification_candidate_bridge.csv", index=False)
        exclusion_summary.to_csv(run_dir / "exclusion_summary.csv", index=False)
        exclusion_samples.to_csv(run_dir / "exclusion_samples.csv", index=False)
    if args.write_parquet:
        log("writing parquet outputs")
        atoms.to_parquet(run_dir / "relation_evidence_atoms.parquet", index=False)
        pressure_component_audit.to_parquet(run_dir / "pressure_component_audit.parquet", index=False)
        lineage_basis_audit.to_parquet(run_dir / "v551_lineage_basis_audit.parquet", index=False)
        exclusion_audit.to_parquet(run_dir / "atom_exclusion_audit.parquet", index=False)
        numeric_wrapper_audit.to_parquet(run_dir / "numeric_wrapper_audit.parquet", index=False)
        relation_review_surface.to_parquet(run_dir / "relation_review_surface.parquet", index=False)
        blocked_signal_audit.to_parquet(run_dir / "blocked_signal_audit.parquet", index=False)
        eligible_bridge_atom_coverage_audit.to_parquet(run_dir / "eligible_bridge_atom_coverage_audit.parquet", index=False)
        directionality_stamp_audit.to_parquet(run_dir / "directionality_stamp_audit.parquet", index=False)
        candidate_bridge.to_parquet(run_dir / "certification_candidate_bridge.parquet", index=False)
        exclusion_summary.to_parquet(run_dir / "exclusion_summary.parquet", index=False)
        exclusion_samples.to_parquet(run_dir / "exclusion_samples.parquet", index=False)

    progress("writing schemas")
    write_schema_json(run_dir / "schemas" / "relation_evidence_atoms.schema.json", atoms, name="relation_evidence_atoms", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "pressure_component_audit.schema.json", pressure_component_audit, name="pressure_component_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "v551_lineage_basis_audit.schema.json", lineage_basis_audit, name="v551_lineage_basis_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "atom_exclusion_audit.schema.json", exclusion_audit, name="atom_exclusion_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "numeric_wrapper_audit.schema.json", numeric_wrapper_audit, name="numeric_wrapper_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "relation_review_surface.schema.json", relation_review_surface, name="relation_review_surface", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "blocked_signal_audit.schema.json", blocked_signal_audit, name="blocked_signal_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "eligible_bridge_atom_coverage_audit.schema.json", eligible_bridge_atom_coverage_audit, name="eligible_bridge_atom_coverage_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "directionality_stamp_audit.schema.json", directionality_stamp_audit, name="directionality_stamp_audit", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "certification_candidate_bridge.schema.json", candidate_bridge, name="certification_candidate_bridge", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "exclusion_summary.schema.json", exclusion_summary, name="exclusion_summary", run_id=args.run_id)
    write_schema_json(run_dir / "schemas" / "exclusion_samples.schema.json", exclusion_samples, name="exclusion_samples", run_id=args.run_id)

    provenance = capture_run_provenance(
        input_documents={
            "bridge_path": args.bridge_path,
            "question_use_contract_path": args.question_use_contract_path or "",
            "source_structure_audit_path": args.source_structure_audit_path or "",
            "response_option_map_path": args.response_option_map_path or "",
        }
    )
    pressure_eligible_rows = int(atoms.get("v552_pressure_component_status", pd.Series(dtype=str)).astype(str).eq("ELIGIBLE").sum()) if not atoms.empty else 0
    pressure_review_rows = int(atoms.get("v552_pressure_component_status", pd.Series(dtype=str)).astype(str).eq("REVIEW_REQUIRED").sum()) if not atoms.empty else 0
    pressure_ineligible_rows = int(atoms.get("v552_pressure_component_status", pd.Series(dtype=str)).astype(str).eq("INELIGIBLE").sum()) if not atoms.empty else 0
    observed_zero_rows = int(atoms.get("observed_response_zero", pd.Series(dtype=bool)).map(lambda value: bool(value)).sum()) if not atoms.empty else 0
    missing_intensity_rows = int(atoms.get("response_intensity_status", pd.Series(dtype=str)).astype(str).eq("MISSING").sum()) if not atoms.empty else 0
    source_provided_evidence_basis_rows = int(atoms.get("evidence_basis_origin", pd.Series(dtype=str)).astype(str).eq("SOURCE_PROVIDED").sum()) if not atoms.empty else 0
    derived_evidence_basis_rows = int(atoms.get("evidence_basis_origin", pd.Series(dtype=str)).astype(str).eq("DERIVED_FROM_ACCEPTED_V550_BRIDGE").sum()) if not atoms.empty else 0
    source_provided_provenance_basis_rows = int(atoms.get("provenance_basis_origin", pd.Series(dtype=str)).astype(str).eq("SOURCE_PROVIDED").sum()) if not atoms.empty else 0
    derived_provenance_basis_rows = int(atoms.get("provenance_basis_origin", pd.Series(dtype=str)).astype(str).eq("DERIVED_FROM_ACCEPTED_V550_BRIDGE").sum()) if not atoms.empty else 0
    evidence_basis_derivation_failure_rows = int(lineage_basis_audit.get("evidence_basis_derivation_status", pd.Series(dtype=str)).astype(str).eq("FAILED").sum()) if not lineage_basis_audit.empty else 0
    provenance_basis_derivation_failure_rows = int(lineage_basis_audit.get("provenance_basis_derivation_status", pd.Series(dtype=str)).astype(str).eq("FAILED").sum()) if not lineage_basis_audit.empty else 0
    upstream_temporal_true_rows = int(atoms.get("allowed_as_temporal_pressure_indicator", pd.Series(dtype=bool)).map(lambda value: bool(value)).sum()) if not atoms.empty else 0
    upstream_temporal_false_rows = int(len(atoms) - upstream_temporal_true_rows) if not atoms.empty else 0
    temporal_authority_status_counts = atoms.get("temporal_authority_status", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict() if not atoms.empty else {}
    unresolved_signed_projection_rows = 0
    if {"authority_intensity_semantics", "v551_signed_side", "v551_signed_intensity"}.issubset(atoms.columns):
        signed_side = atoms["v551_signed_side"].fillna("").astype(str).str.strip()
        signed_intensity = pd.to_numeric(atoms["v551_signed_intensity"], errors="coerce")
        unresolved_signed_projection_rows = int(
            (
                atoms["authority_intensity_semantics"].fillna("").astype(str).str.strip().str.upper().eq("BLOCKED_UNRESOLVED_INTENSITY_SEMANTICS")
                | signed_side.eq("")
                | signed_intensity.isna()
            ).sum()
        )
    if input_contract["status"] != "PASS":
        readiness_status = "BLOCKED_V551_MISSING_BRIDGE_CONTRACT"
    elif directionality_missing_stamp_rows:
        readiness_status = "BLOCKED_V551_DIRECTIONAL_STAMP_COVERAGE"
    elif unresolved_signed_projection_rows:
        readiness_status = "NOT_READY_V551_UNRESOLVED_SIGNED_PROJECTION"
    elif atom_contract_issues:
        readiness_status = "BLOCKED_V551_ATOM_CONTRACT_INVALID"
    elif eligible_bridge_missing_atom_rows:
        readiness_status = "BLOCKED_V551_ELIGIBLE_BRIDGE_ATOM_COVERAGE"
    elif atoms.empty:
        readiness_status = "BLOCKED_V551_NO_RELATION_EVIDENCE_ATOMS"
    else:
        readiness_status = "READY_V551_RELATION_EVIDENCE_CONTRACT"
    readiness = {
        "run_id": args.run_id,
        "status": readiness_status,
        "ready_for_v552_relation_structure": bool(len(atoms) > 0 and directionality_missing_stamp_rows == 0 and atom_contract_invalid_rows == 0 and eligible_bridge_missing_atom_rows == 0 and unresolved_signed_projection_rows == 0),
        "ready_for_v552_pressure_compilation": bool(pressure_eligible_rows > 0 and directionality_missing_stamp_rows == 0 and atom_contract_invalid_rows == 0 and eligible_bridge_missing_atom_rows == 0 and unresolved_signed_projection_rows == 0),
        "bridge_rows": int(len(bridge)),
        "candidate_bridge_rows": int(len(candidate_bridge)),
        "relation_evidence_atom_rows": int(len(atoms)),
        **directionality_stamp_summary,
        "eligible_bridge_missing_atom_rows": eligible_bridge_missing_atom_rows,
        "pressure_component_eligible_rows": pressure_eligible_rows,
        "pressure_component_ineligible_rows": pressure_ineligible_rows,
        "pressure_component_review_required_rows": pressure_review_rows,
        "observed_zero_intensity_rows": observed_zero_rows,
        "missing_intensity_rows": missing_intensity_rows,
        "unresolved_signed_projection_rows": unresolved_signed_projection_rows,
        "source_provided_evidence_basis_rows": source_provided_evidence_basis_rows,
        "derived_evidence_basis_rows": derived_evidence_basis_rows,
        "source_provided_provenance_basis_rows": source_provided_provenance_basis_rows,
        "derived_provenance_basis_rows": derived_provenance_basis_rows,
        "evidence_basis_derivation_failure_rows": evidence_basis_derivation_failure_rows,
        "provenance_basis_derivation_failure_rows": provenance_basis_derivation_failure_rows,
        "upstream_temporal_indicator_true_rows": upstream_temporal_true_rows,
        "upstream_temporal_indicator_false_rows": upstream_temporal_false_rows,
        "temporal_authority_status_counts": temporal_authority_status_counts,
        **denominator_contract_summary,
        "unique_empirical_object_count": int(atoms.get("empirical_object_id", pd.Series(dtype=str)).fillna("").astype(str).nunique()) if not atoms.empty else 0,
        "unique_empirical_distribution_count": int(atoms.get("empirical_distribution_id", pd.Series(dtype=str)).fillna("").astype(str).nunique()) if not atoms.empty else 0,
        "unique_semantic_identity_count": int(atoms.get("semantic_identity_signature", pd.Series(dtype=str)).fillna("").astype(str).nunique()) if not atoms.empty else 0,
        "unique_structural_identity_count": int(atoms.get("structural_identity_signature", pd.Series(dtype=str)).fillna("").astype(str).nunique()) if not atoms.empty else 0,
        "atom_contract_invalid_rows": atom_contract_invalid_rows,
        "atom_contract_issues": atom_contract_issues,
        "input_contract_status": input_contract["status"],
        "schema_version": "v2.1",
    }
    _write_json(run_dir / "v551_readiness_report.json", readiness)
    manifest = {
        "run_id": args.run_id,
        "bridge_rows": int(len(bridge)),
        "candidate_bridge_rows": int(len(candidate_bridge)),
        "atom_rows": int(len(atoms)),
        "exclusion_rows": int(len(exclusion_audit)),
        "exclusion_summary_rows": int(len(exclusion_summary)),
        "exclusion_sample_rows": int(len(exclusion_samples)),
        "numeric_wrapper_audit_rows": int(len(numeric_wrapper_audit)),
        "relation_review_surface_rows": int(len(relation_review_surface)),
        "blocked_signal_audit_rows": int(len(blocked_signal_audit)),
        **directionality_stamp_summary,
        "pressure_component_eligible_rows": pressure_eligible_rows,
        "pressure_component_ineligible_rows": pressure_ineligible_rows,
        "pressure_component_review_required_rows": pressure_review_rows,
        "lineage_basis_audit_rows": int(len(lineage_basis_audit)),
        "unique_empirical_distribution_count": int(atoms.get("empirical_distribution_id", pd.Series(dtype=str)).fillna("").astype(str).nunique()) if not atoms.empty else 0,
        "input_contract_status": input_contract["status"],
        "atom_contract_invalid_rows": atom_contract_invalid_rows,
        "unresolved_signed_projection_rows": unresolved_signed_projection_rows,
        **denominator_contract_summary,
        "ready_for_v552_relation_structure": readiness["ready_for_v552_relation_structure"],
        "ready_for_v552_pressure_compilation": readiness["ready_for_v552_pressure_compilation"],
        "source_run_id": str(bridge["run_id"].dropna().astype(str).iloc[0]) if "run_id" in bridge.columns and not bridge["run_id"].dropna().empty else "",
        "question_use_contract_hash": question_use_contract_hash,
        "source_structure_population_hash": source_structure_population_hash,
        "response_option_map_hash": response_option_map_hash,
        "status": readiness_status,
        "compile_mode": args.v551_compile_mode,
        "audit_mode": args.v551_audit_mode,
        "relation_evidence_atoms_hash": _frame_hash(atoms),
        "pressure_component_audit_hash": _frame_hash(pressure_component_audit),
        "lineage_basis_audit_hash": _frame_hash(lineage_basis_audit),
        "directionality_stamp_audit_hash": _frame_hash(directionality_stamp_audit),
        "schema_version": "v2.1",
        "created_at": pd.Timestamp.utcnow().isoformat(),
        **provenance,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    performance_profile = {
        "run_id": args.run_id,
        "compiler_name": "compile_v551_relation_evidence_atoms",
        "compiler_version": "v2.1",
        "source": str(bridge.get("source", pd.Series(dtype=str)).dropna().astype(str).iloc[0]) if "source" in bridge.columns and not bridge["source"].dropna().empty else "",
        "wave": str(bridge.get("wave", pd.Series(dtype=str)).dropna().astype(str).iloc[0]) if "wave" in bridge.columns and not bridge["wave"].dropna().empty else "",
        "country_code": str(bridge.get("country_code", pd.Series(dtype=str)).dropna().astype(str).iloc[0]) if "country_code" in bridge.columns and not bridge["country_code"].dropna().empty else "",
        "compile_mode": args.v551_compile_mode,
        "audit_mode": args.v551_audit_mode,
        "bridge_rows": int(len(bridge)),
        "candidate_bridge_rows": int(len(candidate_bridge)),
        "atom_rows": int(len(atoms)),
        "exclusion_rows": int(len(exclusion_audit)),
        "numeric_wrapper_audit_rows": int(len(numeric_wrapper_audit)),
        "relation_review_surface_rows": int(len(relation_review_surface)),
        "blocked_signal_audit_rows": int(len(blocked_signal_audit)),
        **directionality_stamp_summary,
        "elapsed_seconds": round(time.monotonic() - profile_started, 3),
        "write_csv": bool(args.write_csv),
        "write_parquet": bool(args.write_parquet),
        **provenance,
    }
    (run_dir / "v551_performance_profile.json").write_text(json.dumps(performance_profile, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.verbose:
        log("writing manifest and printing summary")
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        print(json.dumps(performance_profile, indent=2, ensure_ascii=False))
    progress("done")
    if directionality_missing_stamp_rows:
        raise RuntimeError("BLOCKED_V551_DIRECTIONAL_STAMP_COVERAGE")
    if unresolved_signed_projection_rows:
        raise RuntimeError("NOT_READY_V551_UNRESOLVED_SIGNED_PROJECTION")
    if atom_contract_issues:
        raise RuntimeError("BLOCKED_V551_ATOM_CONTRACT_INVALID: " + "; ".join(atom_contract_issues))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
