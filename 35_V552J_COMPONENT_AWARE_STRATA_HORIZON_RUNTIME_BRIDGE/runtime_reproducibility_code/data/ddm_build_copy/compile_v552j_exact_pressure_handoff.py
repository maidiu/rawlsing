#!/usr/bin/env python3
"""Compile the exact pressure-primary V552J handoff contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v552j_exact_integration import (
    V552J_EXACT_COMPILER_VERSION,
    V552J_EXACT_SCHEMA_VERSION,
    build_exact_v552j_integration,
    validate_exact_v552j_integration,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile exact V551J-component to V552-pressure V552J outputs.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551j-run-root", required=True)
    parser.add_argument("--v552-pressure-observation-handoff-path", required=True)
    parser.add_argument("--v552-structural-fact-index-path", required=True)
    parser.add_argument("--v552-temporal-key-source-index-path", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    return parser.parse_args()


def _read_first(paths: list[Path]) -> pd.DataFrame:
    for path in paths:
        if path.exists():
            frame = read_table(path)
            if not frame.empty or path.exists():
                return frame
    return pd.DataFrame()


def _artifact_paths(v551j_root: Path) -> dict[str, list[Path]]:
    return {
        "components": [
            v551j_root / "packets/v551j_joint_component_index.parquet",
            v551j_root / "packets/v551j_joint_component_index.csv",
        ],
        "certified": [
            v551j_root / "packets/v551j_certified_joint_packet_index.parquet",
            v551j_root / "packets/v551j_certified_packet_index.parquet",
            v551j_root / "packets/v551j_certified_joint_packet_index.csv",
            v551j_root / "packets/v551j_certified_packet_index.csv",
        ],
        "review": [
            v551j_root / "packets/v551j_review_surface.parquet",
            v551j_root / "packets/v551j_review_surface.csv",
        ],
        "candidate": [
            v551j_root / "packets/v551j_joint_packet_candidate_index.parquet",
            v551j_root / "packets/v551j_joint_packet_candidate_index.csv",
        ],
    }


def main() -> int:
    args = parse_args()
    dirs = ensure_output_dirs(args.output_root, args.run_id)
    v551j_root = Path(args.v551j_run_root)
    path_sets = _artifact_paths(v551j_root)
    inputs = {
        "pressure_handoff": read_table(args.v552_pressure_observation_handoff_path),
        "structural_facts": read_table(args.v552_structural_fact_index_path),
        "temporal_sources": read_table(args.v552_temporal_key_source_index_path),
        **{name: _read_first(paths) for name, paths in path_sets.items()},
    }
    outputs = build_exact_v552j_integration(
        run_id=args.run_id,
        pressure_handoff=inputs["pressure_handoff"],
        components=inputs["components"],
        certified_packets=inputs["certified"],
        review_packets=inputs["review"],
        candidate_packets=inputs["candidate"],
        structural_facts=inputs["structural_facts"],
        temporal_sources=inputs["temporal_sources"],
    )
    issues = validate_exact_v552j_integration(outputs)
    if issues:
        outputs["readiness"]["status"] = "BLOCKED_V552J_EXACT_INTEGRATION_CONTRACT"
        outputs["readiness"]["adapter_preflight_ready"] = False
        outputs["readiness"]["ready_for_v553_probe"] = False
        outputs["readiness"]["ready_for_v553"] = False
        outputs["readiness"]["validation_issues_json"] = json.dumps(issues)
    else:
        outputs["readiness"]["validation_issues_json"] = "[]"

    specs = [
        ("pressure_observation_index", "packets", "v552j_pressure_observation_index"),
        ("joint_context_link_index", "packets", "v552j_joint_context_link_index"),
        ("component_linkage_audit", "audits", "v552j_component_linkage_audit"),
        ("certified_link_index", "packets", "v552j_certified_joint_context_link_index"),
        ("review_link_index", "packets", "v552j_review_joint_context_link_index"),
        ("unlinked_pressure_index", "packets", "v552j_unlinked_pressure_observation_index"),
        ("v553_input_index", "packets", "v552j_v553_input_index"),
        ("v553_input_index", "packets", "v552j_to_v553_handoff_index"),
        ("pressure_conservation_audit", "audits", "v552j_pressure_conservation_audit"),
    ]
    artifact_manifest: dict[str, dict[str, object]] = {}
    for key, directory, name in specs:
        frame = outputs[key]
        info = write_frame_artifact(
            frame,
            path=dirs[directory] / f"{name}.parquet",
            schema_path=dirs["schemas"] / f"{name}.schema.json",
            name=name,
            run_id=args.run_id,
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
            extra_schema={"layer": "v552j", "contract": "exact_pressure_primary"},
        )
        artifact_manifest[name] = info

    readiness = outputs["readiness"]
    readiness.update({
        "constraint_rows": int(len(outputs["pressure_observation_index"])),
        "context_rows": int(len(outputs["joint_context_link_index"])),
        "absence_rows": 0,
        "uncertainty_rows": int(readiness.get("structural_fact_gap_count", 0)),
        "forensic_rows": int(len(outputs["pressure_conservation_audit"])),
        "forbidden_rows": 0,
        "status_conflict_rows": 0,
        "forbidden_leakage_rows": 0,
        "input_status": "exact_current_contract",
        "blocker_context_breakdown_json": json.dumps({"validation_issues": issues}),
        "blocker_classes_json": json.dumps(issues),
        "warning_count": int(readiness.get("unlinked_pressure_rows", 0)),
        "warning_classes_json": json.dumps(["unlinked_pressure_observation"] if readiness.get("unlinked_pressure_rows") else []),
        "packet_ready_for_v553": bool(readiness.get("ready_for_v553_probe")),
        "structural_dimensions_resolved_for_v553": int(readiness.get("structural_fact_gap_count", 0)) == 0,
        "input_artifact_index_path": "",
        "authority_normalization_report_path": "",
        "v553_input_index_path": str(
            dirs["packets"] / ("v552j_v553_input_index.parquet" if args.write_parquet else "v552j_v553_input_index.csv")
        ),
    })
    write_json_artifact(dirs["manifest"] / "v552j_readiness_report.json", readiness)
    manifest = {
        "run_id": args.run_id,
        "status": readiness["status"],
        "contract": "exact_pressure_primary",
        "schema_version": V552J_EXACT_SCHEMA_VERSION,
        "compiler_version": V552J_EXACT_COMPILER_VERSION,
        "input_paths": {
            "v551j_run_root": str(v551j_root),
            "v552_pressure_observation_handoff": args.v552_pressure_observation_handoff_path,
            "v552_structural_fact_index": args.v552_structural_fact_index_path,
            "v552_temporal_key_source_index": args.v552_temporal_key_source_index_path,
        },
        "input_rows": {name: int(len(frame)) for name, frame in inputs.items()},
        "artifacts": artifact_manifest,
        "validation_issues": issues,
        "created_at": readiness["created_at"],
    }
    write_json_artifact(dirs["manifest"] / "v552j_exact_integration_manifest.json", manifest)
    write_json_artifact(dirs["manifest"] / "v552j_runtime_handoff_manifest.json", {
        **readiness,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
    })
    write_schema_json(
        dirs["schemas"] / "v552j_readiness_report.schema.json",
        pd.DataFrame([readiness]),
        name="v552j_readiness_report",
        run_id=args.run_id,
        extra={"layer": "v552j", "contract": "exact_pressure_primary"},
    )
    print(readiness["status"])
    print(dirs["manifest"] / "v552j_readiness_report.json")
    return 1 if args.strict and issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
