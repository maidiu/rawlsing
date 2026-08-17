#!/usr/bin/env python3
"""Compile V553 harmonization from the latest wave runs discovered in the repo."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_build_standard import build_thin_build_ledger
from data.ddm_build_copy.ddm_v553_canonical_harmonization import build_v553_wave_harmonization
from data.ddm_build_copy.ddm_v553_harmonization import WaveDescriptor, validate_v553_wave_harmonization_report
from data.ddm_build_copy.ddm_v553_repo_discovery import build_wave_descriptors_from_repo
from data.ddm_build_copy.ddm_v553_schema import V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA, V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V553 wave harmonization from repository-discovered wave runs.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--wave-spec-json", default="")
    parser.add_argument(
        "--source",
        required=True,
        help="Explicit survey family for repository discovery.",
    )
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    return parser.parse_args()


def _load_explicit_descriptors(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise RuntimeError(f"Explicit wave spec not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        items = payload.get("waves") or payload.get("wave_rows") or payload.get("descriptors") or []
    elif isinstance(payload, list):
        items = payload
    else:
        items = []
    descriptors: list[dict[str, object]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        descriptors.append(
            {
                "wave": item.get("wave", ""),
                "source": item.get("source", ""),
                "canonical_wave": item.get("canonical_wave", item.get("wave", "")),
                "country_code": item.get("country_code", ""),
                "temporal_year": item.get(
                    "temporal_year",
                    item.get("fieldwork_year", item.get("survey_year", "")),
                ),
                "authority_dir": item.get("authority_dir", ""),
                "run_root": item.get("run_root", ""),
                "v552j_run_root": item.get("v552j_run_root", item.get("run_root", "")),
                "latest_v552j_root": item.get("latest_v552j_root", item.get("v552j_run_root", item.get("run_root", ""))),
                "latest_v552j_readiness_report": item.get("latest_v552j_readiness_report", item.get("v552j_readiness_report_path", "")),
                "v552j_readiness_report_path": item.get("v552j_readiness_report_path", item.get("latest_v552j_readiness_report", "")),
                "v552j_v553_input_index_path": item.get("v552j_v553_input_index_path", ""),
                "v552j_to_v553_handoff_index_path": item.get("v552j_to_v553_handoff_index_path", ""),
                "v552_structural_fact_index_path": item.get("v552_structural_fact_index_path", ""),
                "v552_temporal_key_source_index_path": item.get("v552_temporal_key_source_index_path", ""),
                "v552j_handoff_manifest_path": item.get("v552j_handoff_manifest_path", ""),
            }
        )
    if not descriptors:
        raise RuntimeError(f"Explicit wave spec did not contain any usable wave descriptors: {path}")
    return descriptors


def _write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _parquet_safe_frame(frame: pd.DataFrame) -> pd.DataFrame:
    safe = frame.copy()
    for column in safe.columns:
        if safe[column].dtype != "object":
            continue
        safe[column] = safe[column].map(
            lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False)
            if isinstance(value, (dict, list, tuple, set))
            else value
        )
    return safe


def main() -> int:
    args = parse_args()
    if args.wave_spec_json:
        spec_path = Path(args.wave_spec_json)
        explicit_items = _load_explicit_descriptors(spec_path)
        for item in explicit_items:
            item["source"] = item.get("source") or args.source
            item["country_code"] = item.get("country_code") or args.country_code
        descriptors = [
            WaveDescriptor.from_mapping(item).normalized().__dict__
            for item in explicit_items
        ]
        discovery_report = {
            "repo_root": str(Path(args.repo_root)),
            "scope_mode": "explicit",
            "wave_count": len(descriptors),
            "waves": [str(item.get("wave", "")) for item in descriptors],
            "source": "explicit_wave_spec",
            "wave_spec_json": str(spec_path),
        }
    else:
        descriptors, discovery_report = build_wave_descriptors_from_repo(
            repo_root=args.repo_root,
            survey_family=args.source,
            country_code=args.country_code,
        )
    table, report = build_v553_wave_harmonization(descriptors)
    provenance = capture_run_provenance(
        input_documents={
            "repo_root": args.repo_root,
            "wave_spec_json": args.wave_spec_json or "",
        }
    )
    discovery_report.update(provenance)

    output_root = Path(args.output_root)
    harmonization_dir = output_root / "v553_wave_harmonization"
    harmonization_dir.mkdir(parents=True, exist_ok=True)

    _write_json(harmonization_dir / "v553_repo_discovery_report.json", discovery_report)
    _write_text(harmonization_dir / "v553_wave_harmonization_table.csv", table.to_csv(index=False))
    table_parquet_path = harmonization_dir / "v553_wave_harmonization_table.parquet"
    _parquet_safe_frame(table).to_parquet(table_parquet_path, index=False)
    evidence_df = _parquet_safe_frame(pd.DataFrame(report.get("wave_pair_evidence", []), columns=V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA["required_columns"]))
    _write_text(harmonization_dir / "v553_wave_harmonization_evidence.csv", evidence_df.to_csv(index=False))
    evidence_df.to_parquet(harmonization_dir / "v553_wave_harmonization_evidence.parquet", index=False)
    report["wave_pair_evidence_path"] = str(harmonization_dir / "v553_wave_harmonization_evidence.parquet")
    report["wave_pair_evidence_row_count"] = int(len(evidence_df))
    differences_df = _parquet_safe_frame(pd.DataFrame(report.get("wave_differences", []), columns=V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA["required_columns"]))
    differences_parquet_path = harmonization_dir / "v553_harmonization_difference_ledger.parquet"
    differences_df.to_parquet(differences_parquet_path, index=False)
    report["wave_harmonization_table_path"] = str(table_parquet_path)
    report["harmonization_difference_ledger_path"] = str(differences_parquet_path)
    report.update(provenance)
    errors = validate_v553_wave_harmonization_report(report)
    _write_json(harmonization_dir / "v553_wave_harmonization_report.json", report)
    if not (harmonization_dir / "v553_wave_harmonization_report.json").exists() or not (harmonization_dir / "v553_wave_harmonization_evidence.parquet").exists():
        raise RuntimeError("V553_WAVE_HARMONIZATION_ARTIFACT_WRITE_FAILED: expected report/evidence artifacts were not created")
    differences_path = harmonization_dir / "v553_wave_harmonization_differences.csv"
    with differences_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "wave",
                "source",
                "canonical_wave",
                "wave_status",
                "missing_authority_kinds_json",
                "semantic_overlay_rows",
                "directionality_overlay_rows",
                "position_overlay_rows",
                "thin_status",
                "thin_ready",
                "thin_layer_count",
            ]
        )
        for row in report.get("wave_differences", []):
            writer.writerow(
                [
                    row.get("wave", ""),
                    row.get("source", ""),
                    row.get("canonical_wave", ""),
                    row.get("wave_status", ""),
                    row.get("missing_authority_kinds_json", ""),
                    row.get("semantic_overlay_rows", 0),
                    row.get("directionality_overlay_rows", 0),
                    row.get("position_overlay_rows", 0),
                    row.get("thin_status", ""),
                    row.get("thin_ready", False),
                    row.get("thin_layer_count", 0),
                ]
            )

    final_status = report.get("overall_status", "STATUS: UNKNOWN")
    provisionality = "thin_scaffold"
    if report.get("ready_for_v553"):
        provisionality = "provisional"
    if int(report.get("wave_count", 0) or 0) <= 1:
        provisionality = "blocked"

    build_ledger = build_thin_build_ledger(
        run_id="v553_wave_harmonization",
        records=[],
        final_status=final_status,
    )
    build_ledger.update(
        {
            "build_kind": "v553_repo_discovered_wave_harmonization",
            "provisionality": provisionality,
            "scaffold_level": "cross_wave_comparison",
            "implementation_kind": "reviewable" if report.get("ready_for_v553") else "thin_scaffold",
            "discovery_report_path": str(harmonization_dir / "v553_repo_discovery_report.json"),
            "table_path": str(harmonization_dir / "v553_wave_harmonization_table.csv"),
            "table_parquet_path": str(table_parquet_path),
            "report_path": str(harmonization_dir / "v553_wave_harmonization_report.json"),
            "wave_pair_evidence_path": str(harmonization_dir / "v553_wave_harmonization_evidence.parquet"),
            "wave_pair_evidence_row_count": int(len(evidence_df)),
            "evidence_csv_path": str(harmonization_dir / "v553_wave_harmonization_evidence.csv"),
            "evidence_parquet_path": str(harmonization_dir / "v553_wave_harmonization_evidence.parquet"),
            "differences_path": str(differences_path),
            "differences_parquet_path": str(differences_parquet_path),
            "wave_count": int(report.get("wave_count", 0) or 0),
            "multiple_waves_present": bool(report.get("multiple_waves_present", False)),
            **provenance,
        }
    )
    _write_json(harmonization_dir / "v553_wave_harmonization_build_ledger.json", build_ledger)

    if args.strict and errors:
        raise RuntimeError("V553_WAVE_HARMONIZATION_VALIDATION_FAILED: " + "; ".join(errors))

    print(final_status)
    print(str(harmonization_dir / "v553_wave_harmonization_report.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())