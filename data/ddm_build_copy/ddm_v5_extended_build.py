#!/usr/bin/env python3
"""Extended V5 build that binds multi-wave harmonization to the thin forward path."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v5_thin_end_to_end import build_v5_thin_end_to_end, validate_thin_end_to_end
from data.ddm_build_copy.ddm_v553_harmonization import build_v553_wave_harmonization, validate_v553_wave_harmonization_report
from data.ddm_build_copy.ddm_v553_repo_discovery import build_wave_descriptors_from_repo
from data.ddm_build_copy.ddm_v553_temporal_pressure import build_v553_temporal_pressure_field, validate_v553_temporal_pressure_readiness
from data.ddm_build_copy.ddm_v553_schema import V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def build_v5_extended_build(
    *,
    run_id: str,
    repo_root: str | Path,
    v551j_run_root: str | Path,
    output_root: str | Path,
    survey_family: str = "",
    country_code: str = "",
) -> dict[str, Any]:
    root = Path(output_root) / run_id
    root.mkdir(parents=True, exist_ok=True)

    descriptors, discovery_report = build_wave_descriptors_from_repo(
        repo_root=repo_root,
        survey_family=survey_family,
        country_code=country_code,
    )
    wave_table, wave_report = build_v553_wave_harmonization(descriptors)
    wave_errors = validate_v553_wave_harmonization_report(wave_report)
    wave_dir = root / "v553_wave_harmonization"
    wave_dir.mkdir(parents=True, exist_ok=True)
    _write_json(wave_dir / "v553_repo_discovery_report.json", discovery_report)
    wave_table.to_csv(wave_dir / "v553_wave_harmonization_table.csv", index=False)
    wave_evidence_df = pd.DataFrame(wave_report.get("wave_pair_evidence", []), columns=V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA["required_columns"])
    wave_evidence_df.to_csv(wave_dir / "v553_wave_harmonization_evidence.csv", index=False)
    wave_evidence_df.to_parquet(wave_dir / "v553_wave_harmonization_evidence.parquet", index=False)
    wave_report["wave_pair_evidence_path"] = str(wave_dir / "v553_wave_harmonization_evidence.parquet")
    wave_report["wave_pair_evidence_row_count"] = int(len(wave_evidence_df))
    _write_json(wave_dir / "v553_wave_harmonization_report.json", wave_report)
    _write_json(wave_dir / "v553_wave_harmonization_validation_report.json", {"errors": wave_errors, "error_count": len(wave_errors)})

    temporal_root = root / "v553_temporal_pressure"
    temporal_summary = build_v553_temporal_pressure_field(
        run_id=run_id,
        wave_harmonization_report_path=wave_dir / "v553_wave_harmonization_report.json",
        output_root=temporal_root,
        country_code=country_code,
    )
    temporal_errors = validate_v553_temporal_pressure_readiness(temporal_summary)

    thin_root = root / "v5_thin_end_to_end"
    thin_summary = build_v5_thin_end_to_end(
        run_id=run_id,
        v551j_run_root=v551j_run_root,
        output_root=thin_root,
        survey_family=survey_family,
        country_code=country_code,
        v553_temporal_context_root=temporal_root / run_id,
        v553_wave_harmonization_root=wave_dir,
    )
    thin_errors = validate_thin_end_to_end(thin_summary)
    latest_v552j_readiness = {}
    latest_v552j_root = ""
    latest_v558_readiness = {}
    latest_v558_root = ""
    for layer_report in thin_summary.get("layer_reports", []):
        if str(layer_report.get("layer", "")) != "v552j":
            if str(layer_report.get("layer", "")) == "v558":
                latest_v558_root = str(layer_report.get("layer_output_root", ""))
                readiness_path = Path(latest_v558_root) / "manifest" / "v558_readiness_report.json" if latest_v558_root else None
                if readiness_path and readiness_path.exists():
                    try:
                        latest_v558_readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
                    except Exception:
                        latest_v558_readiness = {}
            continue
        latest_v552j_root = str(layer_report.get("layer_output_root", ""))
        readiness_path = Path(latest_v552j_root) / "manifest" / "v552j_readiness_report.json" if latest_v552j_root else None
        if readiness_path and readiness_path.exists():
            try:
                latest_v552j_readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
            except Exception:
                latest_v552j_readiness = {}

    final_status = "READY_V5_EXTENDED_BUILD"
    if wave_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_WAVE_GAPS"
    if temporal_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_TEMPORAL_GAPS"
    if thin_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_THIN_GAPS"
    if wave_errors and temporal_errors and thin_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_WAVE_TEMPORAL_AND_THIN_GAPS"
    elif wave_errors and temporal_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_WAVE_AND_TEMPORAL_GAPS"
    elif wave_errors and thin_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_WAVE_AND_THIN_GAPS"
    elif temporal_errors and thin_errors:
        final_status = "READY_V5_EXTENDED_BUILD_WITH_TEMPORAL_AND_THIN_GAPS"

    ledger = {
        "run_id": run_id,
        "build_kind": "v5_extended_build",
        "implementation_kind": "thin_scaffold" if wave_errors or thin_errors else "reviewable",
        "provisionality": "thin_scaffold" if wave_errors or thin_errors else "provisional",
        "scaffold_level": "cross_wave_plus_thin_end_to_end",
        "final_status": final_status,
        "counts": {
            "subbuild_count": 3,
            "layer_count": int(thin_summary.get("layer_count", 0) or 0),
            "wave_count": int(wave_report.get("wave_count", 0) or 0),
        },
        "layer_records": [
            {
                "layer": "v553_wave_harmonization",
                "implementation_kind": "reviewable" if wave_report.get("ready_for_v553") else "thin_scaffold",
                "provisionality": "provisional" if wave_report.get("ready_for_v553") else "thin_scaffold",
                "status": wave_report.get("overall_status", ""),
                "continuity_checked_full": False,
                "upstream_continuity_result": "pass" if wave_report.get("multiple_waves_present") else "partial",
                "downstream_continuity_result": "not_checked",
                "validation_errors": wave_errors,
                "artifact_paths": {
                    "report_path": str(wave_dir / "v553_wave_harmonization_report.json"),
                    "table_path": str(wave_dir / "v553_wave_harmonization_table.csv"),
                    "evidence_path": str(wave_dir / "v553_wave_harmonization_evidence.parquet"),
                    "discovery_path": str(wave_dir / "v553_repo_discovery_report.json"),
                },
                "evidence_row_count": int(wave_report.get("wave_pair_evidence_row_count", 0) or 0),
            },
            {
                "layer": "v553_temporal_pressure",
                "implementation_kind": "reviewable" if temporal_summary.get("ready_for_v554") else "thin_scaffold",
                "provisionality": "provisional" if temporal_summary.get("ready_for_v554") else "thin_scaffold",
                "status": temporal_summary.get("status", ""),
                "continuity_checked_full": False,
                "upstream_continuity_result": "pass" if not temporal_errors else "partial",
                "downstream_continuity_result": "not_checked",
                "validation_errors": temporal_errors,
                "artifact_paths": {
                    "readiness_report": temporal_summary.get("packet_path", ""),
                    "pressure_field_path": temporal_summary.get("pressure_field_path", ""),
                    "year_indexed_pressure_path": temporal_summary.get("year_indexed_pressure_path", ""),
                    "interpolated_pressure_path": temporal_summary.get("interpolated_pressure_path", ""),
                },
            },
            {
                "layer": "v5_thin_end_to_end",
                "implementation_kind": "thin_scaffold" if thin_errors else "reviewable",
                "provisionality": "thin_scaffold" if thin_errors else "provisional",
                "status": thin_summary.get("final_status", ""),
                "continuity_checked_full": False,
                "upstream_continuity_result": "pass" if not thin_errors else "partial",
                "downstream_continuity_result": "not_checked",
                "validation_errors": thin_errors,
                "artifact_paths": {
                    "readiness_report": str(thin_root / run_id / "manifest" / "v5_thin_end_to_end_readiness_report.json"),
                },
            },
        ],
        "repo_root": str(Path(repo_root)),
        "v551j_run_root": str(Path(v551j_run_root)),
        "latest_v552j_root": latest_v552j_root,
        "latest_v552j_readiness": latest_v552j_readiness,
        "latest_v558_root": latest_v558_root,
        "latest_v558_readiness": latest_v558_readiness,
        "wave_harmonization": {
            **wave_report,
            "report_path": str(wave_dir / "v553_wave_harmonization_report.json"),
            "evidence_path": str(wave_dir / "v553_wave_harmonization_evidence.parquet"),
            "evidence_row_count": int(wave_report.get("wave_pair_evidence_row_count", 0) or 0),
            "validation_errors": wave_errors,
        },
        "v553_temporal_pressure": {
            "status": temporal_summary.get("status", ""),
            "ready_for_v554": bool(temporal_summary.get("ready_for_v554", False)),
            "packet_path": temporal_summary.get("packet_path", ""),
            "pressure_field_path": temporal_summary.get("pressure_field_path", ""),
            "validation_errors": temporal_errors,
        },
        "thin_end_to_end": {
            "status": thin_summary.get("final_status", ""),
            "layer_count": int(thin_summary.get("layer_count", 0) or 0),
            "summary_path": str(thin_root / run_id / "manifest" / "v5_thin_end_to_end_readiness_report.json"),
            "validation_errors": thin_errors,
        },
        "latest_v552j_root": latest_v552j_root,
        "latest_v552j_readiness_status": latest_v552j_readiness.get("status", ""),
        "latest_v552j_blocker_context_count": int(latest_v552j_readiness.get("blocker_context_count", 0) or 0),
        "latest_v558_root": latest_v558_root,
        "latest_v558_readiness_status": latest_v558_readiness.get("status", ""),
        "latest_v558_blocker_context_count": int(latest_v558_readiness.get("blocker_context_count", 0) or 0),
    }
    wave_harmonization_summary = {
        **wave_report,
        "report_path": str(wave_dir / "v553_wave_harmonization_report.json"),
        "evidence_path": str(wave_dir / "v553_wave_harmonization_evidence.parquet"),
        "evidence_row_count": int(wave_report.get("wave_pair_evidence_row_count", 0) or 0),
        "validation_errors": wave_errors,
    }
    _write_json(root / "manifest" / "v5_extended_build_ledger.json", ledger)
    _write_json(
        root / "manifest" / "v5_extended_build_readiness_report.json",
        {
            "run_id": run_id,
            "final_status": final_status,
            "wave_harmonization_status": wave_report.get("overall_status", ""),
            "v553_temporal_pressure_status": temporal_summary.get("status", ""),
            "thin_end_to_end_status": thin_summary.get("final_status", ""),
            "thin_end_to_end_layer_count": int(thin_summary.get("layer_count", 0) or 0),
            "latest_v552j_root": latest_v552j_root,
            "latest_v552j_readiness_status": latest_v552j_readiness.get("status", ""),
            "latest_v552j_blocker_context_count": int(latest_v552j_readiness.get("blocker_context_count", 0) or 0),
            "latest_v558_root": latest_v558_root,
            "latest_v558_readiness_status": latest_v558_readiness.get("status", ""),
            "latest_v558_blocker_context_count": int(latest_v558_readiness.get("blocker_context_count", 0) or 0),
            "wave_validation_errors": wave_errors,
            "temporal_validation_errors": temporal_errors,
            "thin_validation_errors": thin_errors,
            "created_at": thin_summary.get("created_at", ""),
        },
    )
    return {
        "run_id": run_id,
        "final_status": final_status,
        "wave_harmonization": wave_harmonization_summary,
        "v553_temporal_pressure": temporal_summary,
        "thin_end_to_end": thin_summary,
        "ledger": ledger,
    }


__all__ = ["build_v5_extended_build"]
