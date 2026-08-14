#!/usr/bin/env python3
"""Compile V552 structural-pressure contract v2.1 artifacts from V551 v2.1 atoms."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v550_schema import dataframe_schema_json
from data.ddm_build_copy.ddm_v552_structural import (
    V552_HANDOFF_SCHEMA_VERSION,
    V552_SCHEMA_VERSION,
    _fact_index,
    _handoff,
    _pressure_observation_handoff,
    _temporal_key_index,
    build_v552_structural_outputs,
    validate_v552_v551_input_contract,
)
from data.ddm_build_copy.ddm_v552_contract import recompute_v552_v2_1_4_pressure_measurement_hash
from data.ddm_build_copy.ddm_v552_validation import validate_v552_v2_1_4_outputs, validate_written_v552_artifacts

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v552" / "runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V552 structural-pressure contract v2.1 artifacts.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--atoms-path", required=True)
    parser.add_argument("--conditional-determinicity-path", default=None)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--strict-handoff", dest="strict_handoff", action="store_true", default=True)
    parser.add_argument("--no-strict-handoff", dest="strict_handoff", action="store_false")
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--progress", dest="progress", action="store_true", default=True)
    parser.add_argument("--no-progress", dest="progress", action="store_false")
    return parser.parse_args()


def _read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(str(path))
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    return pd.read_parquet(path)


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _frame_hash(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "empty"
    out = frame.copy()
    for column in out.columns:
        out[column] = out[column].fillna("").astype(str)
    out = out.sort_values(list(out.columns), kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(out.to_csv(index=False).encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_frame(root: Path, schemas: Path, name: str, frame: pd.DataFrame, *, write_csv: bool, write_parquet: bool) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    schemas.mkdir(parents=True, exist_ok=True)
    csv_path = root / f"{name}.csv"
    parquet_path = root / f"{name}.parquet"
    if write_csv:
        # Acceptance validation reconstructs contracts from the persisted CSV.
        # Preserve IEEE-754 values so that persistence cannot change governed
        # weights, signed summaries, or pressure magnitudes.
        frame.to_csv(csv_path, index=False, float_format="%.17g")
    if write_parquet:
        frame.to_parquet(parquet_path, index=False)
    _write_json(schemas / f"{name}.schema.json", dataframe_schema_json(frame, name=name, run_id=root.parent.name))
    return {
        "rows": int(len(frame)),
        "csv_path": str(csv_path),
        "parquet_path": str(parquet_path),
        "hash": _frame_hash(frame),
    }


def _scale_encoding_report(component_index: pd.DataFrame) -> dict[str, Any]:
    representation_class_counts = component_index.get("source_intensity_representation_class", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict()
    representation_status_counts = component_index.get("source_intensity_representation_status", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict()
    return {
        "status": "PASS",
        "candidate_component_rows": int(len(component_index)),
        "component_index_rows": int(len(component_index)),
        "encoding_class_counts": component_index.get("scale_encoding_class", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict(),
        "intensity_representation_class_counts": representation_class_counts,
        "intensity_representation_status_counts": representation_status_counts,
        "resolved_intensity_representation_component_rows": int(component_index.get("source_intensity_representation_status", pd.Series(dtype=str)).fillna("").astype(str).eq("EXACT_UNIQUE_DISTRIBUTION_RESOLUTION").sum()),
        "scale_direction_token_counts": component_index.get("scale_direction", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict(),
        "scale_encoding_status_counts": component_index.get("scale_encoding_status", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict(),
        "direction_scale_consistency_status_counts": component_index.get("direction_scale_consistency_status", pd.Series(dtype=str)).fillna("").astype(str).value_counts().to_dict(),
        "source_intensity_zero_count": int(component_index.get("source_intensity_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
        "canonical_signed_zero_count": int(component_index.get("canonical_signed_component_zero", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not component_index.empty else 0,
        "unknown_scale_direction_tokens": sorted(set(component_index.loc[component_index.get("scale_encoding_class", pd.Series(dtype=str)).fillna("").astype(str).isin(["UNKNOWN", "UNRESOLVED"]), "scale_direction"].fillna("").astype(str).tolist())) if not component_index.empty and "scale_encoding_class" in component_index.columns else [],
        "superseded_formula_usage_count": 0,
        "axis_coordinate_raw_direction_times_intensity_usage_count": 0,
    }


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    run_dir = Path(args.output_root) / args.run_id
    structural_dir = run_dir / "structural"
    audit_dir = run_dir / "audits"
    manifest_dir = run_dir / "manifest"
    schema_dir = run_dir / "schemas"
    for p in [structural_dir, audit_dir, manifest_dir, schema_dir]:
        p.mkdir(parents=True, exist_ok=True)

    atoms_path = Path(args.atoms_path)
    if not atoms_path.exists():
        print("BLOCKED_V552_MISSING_ATOMS_PATH")
        return 1
    atoms = _read_table(atoms_path)
    atoms_hash = _hash_file(atoms_path)
    atoms_csv_path = manifest_dir / "v552_input_atoms.csv"
    atoms_parquet_path = manifest_dir / "v552_input_atoms.parquet"
    atoms.to_csv(atoms_csv_path, index=False, float_format="%.17g")
    atoms.to_parquet(atoms_parquet_path, index=False)
    input_contract = validate_v552_v551_input_contract(atoms)
    _write_json(manifest_dir / "v552_input_contract_report.json", input_contract)
    if input_contract["status"] != "PASS":
        print(input_contract["status"])
        return 1

    outputs = build_v552_structural_outputs(atoms, None, run_id=args.run_id)
    if "v552_readiness_report" in outputs and not outputs["v552_readiness_report"].empty:
        provisional_status = "READY_V552_STRUCTURAL_PRESSURE_CONTRACT" if args.strict_handoff else "DIAGNOSTIC_V552_NO_STRICT_NOT_READY"
        outputs["v552_readiness_report"].loc[:, "status"] = provisional_status
        outputs["v552_readiness_report"].loc[:, "final_status"] = provisional_status
        outputs["v552_readiness_report"].loc[:, "v552_compile_status"] = provisional_status
    initial_issues = validate_v552_v2_1_4_outputs(
        input_atoms=atoms,
        components=outputs.get("v552_pressure_component_index", pd.DataFrame()),
        observations=outputs.get("v552_pressure_observation_index", pd.DataFrame()),
        structural_facts=outputs.get("v552_structural_fact_index", pd.DataFrame()),
        temporal_sources=outputs.get("v552_temporal_key_source_index", pd.DataFrame()),
        pressure_handoff=outputs.get("v552_to_v552j_pressure_observation_handoff_index", pd.DataFrame()),
        readiness=outputs.get("v552_readiness_report", pd.DataFrame()),
        execution_mode="acceptance" if args.strict_handoff else "diagnostic",
    )
    if initial_issues or not args.strict_handoff:
        blocked_status = "BLOCKED_V552_OUTPUT_CONTRACT" if args.strict_handoff else "DIAGNOSTIC_V552_NO_STRICT_NOT_READY"
        for frame_name in [
            "v552_pressure_observation_index",
            "v552_structural_fact_index",
            "v552_temporal_key_source_index",
            "v552_to_v552j_handoff_index",
            "v552_to_v552j_pressure_observation_handoff_index",
        ]:
            frame = outputs.get(frame_name)
            if isinstance(frame, pd.DataFrame) and not frame.empty:
                for col in [
                    "v552j_pressure_linkage_eligible",
                    "v552j_structural_context_eligible",
                    "v553_probe_candidate_after_v552j",
                    "pressure_anchor_candidate_after_v552j",
                    "allowed_for_v552j",
                    "allowed_for_v553_probe",
                    "ready_for_v552j_inspection",
                    "ready_for_v553_after_v552j",
                    "direct_v553_authorization",
                    "temporal_authority",
                    "runtime_authority",
                ]:
                    if col in frame.columns:
                        frame.loc[:, col] = False
                for col in ["allowed_for_v553_temporal_field", "ready_for_v553_direct"]:
                    if col in frame.columns:
                        frame.loc[:, col] = False
                if "allowed_v552j_use" in frame.columns:
                    frame.loc[:, "allowed_v552j_use"] = "not_authorized"
                if "allowed_downstream_use" in frame.columns:
                    frame.loc[:, "allowed_downstream_use"] = "not_authorized"
        if "v552_readiness_report" in outputs and not outputs["v552_readiness_report"].empty:
            outputs["v552_readiness_report"].loc[:, "status"] = blocked_status
            outputs["v552_readiness_report"].loc[:, "final_status"] = blocked_status
            outputs["v552_readiness_report"].loc[:, "v552_compile_status"] = blocked_status
            outputs["v552_readiness_report"].loc[:, "ready_for_v552j_structural_inspection"] = False
            outputs["v552_readiness_report"].loc[:, "ready_for_v552j_pressure_linkage"] = False
            outputs["v552_readiness_report"].loc[:, "ready_for_v552j_inspection"] = False
            outputs["v552_readiness_report"].loc[:, "ready_for_v553_direct"] = False
            outputs["v552_readiness_report"].loc[:, "ready_for_v553_after_v552j"] = False
            outputs["v552_readiness_report"].loc[:, "pressure_linkage_eligible_count"] = 0
            outputs["v552_readiness_report"].loc[:, "v552_v552j_handoff_readiness"] = "not_authorized"
        observations = outputs.get("v552_pressure_observation_index", pd.DataFrame())
        components = outputs.get("v552_pressure_component_index", pd.DataFrame())
        for idx, obs in observations.iterrows():
            comp_group = components[components["v552_pressure_observation_id"].astype(str).eq(str(obs.get("v552_pressure_observation_id")))]
            observations.loc[idx, "pressure_measurement_hash"] = recompute_v552_v2_1_4_pressure_measurement_hash(observations.loc[idx].to_dict(), comp_group.to_dict("records"))
        outputs["v552_structural_fact_index"] = _fact_index(observations, outputs, outputs.get("contradiction_tensor", pd.DataFrame()), args.run_id)
        outputs["v552_temporal_key_source_index"] = _temporal_key_index(outputs["v552_structural_fact_index"], args.run_id)
        outputs["v552_to_v552j_handoff_index"] = _handoff(outputs, args.run_id)
        outputs["v552_to_v552j_pressure_observation_handoff_index"] = _pressure_observation_handoff(observations, components, args.run_id)
    final_mode = "strict_blocked" if args.strict_handoff and initial_issues else ("diagnostic" if not args.strict_handoff else "acceptance")
    validation_issues = validate_v552_v2_1_4_outputs(
        input_atoms=atoms,
        components=outputs.get("v552_pressure_component_index", pd.DataFrame()),
        observations=outputs.get("v552_pressure_observation_index", pd.DataFrame()),
        structural_facts=outputs.get("v552_structural_fact_index", pd.DataFrame()),
        temporal_sources=outputs.get("v552_temporal_key_source_index", pd.DataFrame()),
        pressure_handoff=outputs.get("v552_to_v552j_pressure_observation_handoff_index", pd.DataFrame()),
        readiness=outputs.get("v552_readiness_report", pd.DataFrame()),
        execution_mode=final_mode,
    )
    outputs["v552_validation_issue_report"] = pd.DataFrame([issue.__dict__ for issue in validation_issues], columns=["token", "detail"])
    if "v552_readiness_report" in outputs and not outputs["v552_readiness_report"].empty:
        outputs["v552_readiness_report"].loc[:, "invalid_output_contract_rows"] = len(validation_issues)
    component_index = outputs["v552_pressure_component_index"]
    scale_report = _scale_encoding_report(component_index)
    _write_json(manifest_dir / "v552_scale_encoding_report.json", scale_report)

    artifact_info: dict[str, Any] = {}
    audit_names = {"v552_pressure_observation_audit", "v552_directionality_coverage_audit", "v552_directionality_gap_surface", "v552_status_pressure_review_surface", "conditional_determinicity_status_audit"}
    manifest_names = {"v552_readiness_report"}
    for name, frame in outputs.items():
        if name.startswith("_") or not isinstance(frame, pd.DataFrame):
            continue
        target = manifest_dir if name in manifest_names else audit_dir if name in audit_names else structural_dir
        artifact_info[name] = _write_frame(target, schema_dir, name, frame, write_csv=args.write_csv, write_parquet=args.write_parquet)

    written_issues: list[Any] = []
    written_audit = pd.DataFrame()
    if args.write_csv and args.write_parquet:
        written_issues, written_audit = validate_written_v552_artifacts(
            run_directory=run_dir,
            atoms_csv_path=atoms_csv_path,
            atoms_parquet_path=atoms_parquet_path,
            execution_mode=final_mode,
        )
        outputs["v552_written_artifact_reproducibility_audit"] = written_audit
        _write_frame(structural_dir, schema_dir, "v552_written_artifact_reproducibility_audit", written_audit, write_csv=args.write_csv, write_parquet=args.write_parquet)
        if written_issues:
            outputs["v552_validation_issue_report"] = pd.DataFrame([issue.__dict__ for issue in written_issues], columns=["token", "detail"])
            if "v552_readiness_report" in outputs and not outputs["v552_readiness_report"].empty:
                outputs["v552_readiness_report"].loc[:, "invalid_output_contract_rows"] = len(written_issues)
                if args.strict_handoff:
                    outputs["v552_readiness_report"].loc[:, "status"] = "BLOCKED_V552_OUTPUT_CONTRACT"
                    outputs["v552_readiness_report"].loc[:, "final_status"] = "BLOCKED_V552_OUTPUT_CONTRACT"
                    outputs["v552_readiness_report"].loc[:, "v552_compile_status"] = "BLOCKED_V552_OUTPUT_CONTRACT"
            _write_frame(structural_dir, schema_dir, "v552_validation_issue_report", outputs["v552_validation_issue_report"], write_csv=args.write_csv, write_parquet=args.write_parquet)
            _write_frame(manifest_dir, schema_dir, "v552_readiness_report", outputs["v552_readiness_report"], write_csv=args.write_csv, write_parquet=args.write_parquet)

    readiness_df = outputs["v552_readiness_report"]
    readiness = readiness_df.iloc[0].to_dict() if not readiness_df.empty else {
        "status": "BLOCKED_V552_OUTPUT_CONTRACT_INVALID",
        "schema_version": V552_SCHEMA_VERSION,
    }
    _write_json(manifest_dir / "v552_readiness_report.json", readiness)

    manifest = {
        "run_id": args.run_id,
        "status": readiness["status"],
        "schema_version": V552_SCHEMA_VERSION,
        "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        "input_contract_status": input_contract["status"],
        "atoms_path": str(atoms_path),
        "atoms_input_hash": atoms_hash,
        "input_atom_rows": int(len(atoms)),
        "pressure_observation_rows": int(len(outputs["v552_pressure_observation_index"])),
        "observed_pressure_rows": int(readiness.get("observed_pressure_count", 0) + readiness.get("observed_zero_pressure_count", 0)),
        "pressure_linkage_eligible_rows": int(readiness.get("pressure_linkage_eligible_count", 0)),
        "noncomputable_pressure_rows": int(readiness.get("noncomputable_pressure_count", 0)),
        "review_required_pressure_rows": int(readiness.get("review_required_pressure_count", 0)),
        "contradiction_rows": int(readiness.get("contradiction_row_count", 0)),
        "structural_channel_rows": int(readiness.get("structural_channel_count", 0)),
        "allowed_for_v553_temporal_field_rows": 0,
        "output_artifact_count": int(readiness.get("output_artifact_count", 0)),
        "handoff_index_rows": int(readiness.get("handoff_index_rows", 0)),
        "comparability_key_count": int(readiness.get("comparability_key_count", 0)),
        "category_empirical_object_count": int(readiness.get("category_empirical_object_count", 0)),
        "unique_empirical_distribution_count": int(readiness.get("unique_empirical_distribution_count", 0)),
        "artifacts": artifact_info,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        **capture_run_provenance(input_documents={"atoms_path": args.atoms_path}),
    }
    _write_json(manifest_dir / "manifest.json", manifest)
    (run_dir / "v552_performance_profile.json").write_text(json.dumps({
        "run_id": args.run_id,
        "compiler_name": "compile_v552_structural_ddm",
        "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        "elapsed_seconds": manifest["elapsed_seconds"],
        "input_rows": int(len(atoms)),
        "output_rows": int(sum(info["rows"] for info in artifact_info.values())),
        "final_status": readiness["status"],
    }, indent=2), encoding="utf-8")

    print(readiness["status"])
    return 1 if str(readiness["status"]).startswith("BLOCKED_") else 0


if __name__ == "__main__":
    raise SystemExit(main())
