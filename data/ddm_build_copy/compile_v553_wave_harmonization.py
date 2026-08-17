#!/usr/bin/env python3
"""Compile the V553 wave harmonization readiness package."""

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

from data.ddm_build_copy.ddm_v553_canonical_harmonization import build_v553_wave_harmonization  # noqa: E402
from data.ddm_build_copy.ddm_v553_harmonization import validate_v553_wave_harmonization_report  # noqa: E402
from data.ddm_build_copy.ddm_v553_schema import V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA, V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V553 wave harmonization reports from a wave spec JSON file.")
    parser.add_argument("--wave-spec-json", required=True, help="Path to a JSON list of wave descriptors.")
    parser.add_argument("--output-root", required=True, help="Directory for the harmonization package.")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    return parser.parse_args()


def _load_wave_specs(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("wave-spec-json must contain a JSON list")
    specs: list[dict[str, object]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("wave-spec-json list items must be objects")
        specs.append(item)
    return specs


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
    wave_specs = _load_wave_specs(Path(args.wave_spec_json))
    table, report = build_v553_wave_harmonization(wave_specs)
    output_root = Path(args.output_root)
    harmonization_dir = output_root / "v553_wave_harmonization"
    harmonization_dir.mkdir(parents=True, exist_ok=True)

    table_path = harmonization_dir / "v553_wave_harmonization_table.csv"
    table_parquet_path = harmonization_dir / "v553_wave_harmonization_table.parquet"
    report_path = harmonization_dir / "v553_wave_harmonization_report.json"
    differences_path = harmonization_dir / "v553_wave_harmonization_differences.csv"
    differences_parquet_path = harmonization_dir / "v553_harmonization_difference_ledger.parquet"
    evidence_path = harmonization_dir / "v553_wave_harmonization_evidence.csv"
    evidence_parquet_path = harmonization_dir / "v553_wave_harmonization_evidence.parquet"
    _write_text(table_path, table.to_csv(index=False))
    _parquet_safe_frame(table).to_parquet(table_parquet_path, index=False)
    differences_path.parent.mkdir(parents=True, exist_ok=True)
    with differences_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
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
        ])
        for row in report.get("wave_differences", []):
            writer.writerow([
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
            ])
    differences_df = _parquet_safe_frame(pd.DataFrame(report.get("wave_differences", []), columns=V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA["required_columns"]))
    differences_df.to_parquet(differences_parquet_path, index=False)

    evidence_df = _parquet_safe_frame(pd.DataFrame(report.get("wave_pair_evidence", []), columns=V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA["required_columns"]))
    _write_text(evidence_path, evidence_df.to_csv(index=False))
    evidence_df.to_parquet(evidence_parquet_path, index=False)
    report["wave_pair_evidence_path"] = str(evidence_parquet_path)
    report["wave_pair_evidence_row_count"] = int(len(evidence_df))
    report["wave_harmonization_table_path"] = str(table_parquet_path)
    report["harmonization_difference_ledger_path"] = str(differences_parquet_path)
    errors = validate_v553_wave_harmonization_report(report)
    _write_json(report_path, report)
    if not evidence_parquet_path.exists() or not report_path.exists():
        raise RuntimeError("V553_WAVE_HARMONIZATION_ARTIFACT_WRITE_FAILED: expected report/evidence artifacts were not created")

    if args.strict and errors:
        raise RuntimeError("V553_WAVE_HARMONIZATION_VALIDATION_FAILED: " + "; ".join(errors))

    print(report["overall_status"])
    print(str(report_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())