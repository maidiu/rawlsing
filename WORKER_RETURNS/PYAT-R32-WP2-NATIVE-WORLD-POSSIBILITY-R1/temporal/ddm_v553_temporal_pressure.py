#!/usr/bin/env python3
"""Thin V553 temporal pressure field compiler."""

from __future__ import annotations

import json
import hashlib
import shutil
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import read_table, write_frame_artifact, write_json_artifact, ensure_output_dirs
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_survey_identity import (
    SurveyIdentityError,
    canonical_country_code,
    canonical_family_key,
    canonical_family_label,
    canonical_wave_key,
    require_survey_identity,
)
from data.ddm_build_copy.ddm_v553_repo_discovery import latest_run_root_for_wave
from data.ddm_build_copy.ddm_v553_temporal_identity import (
    normalize_temporal_report_identity as _normalize_temporal_report_identity,
)
from data.ddm_build_copy.ddm_v552j_handoff import _packet_structural_dimension_resolution
from data.ddm_build_copy.ddm_v553_schema import (
    V553_COMPILER_VERSION,
    V553_COMPARABILITY_AUDIT_SCHEMA,
    V553_ABSENCE_NONCOMPARABILITY_REGISTER_SCHEMA,
    V553_COHORT_WINDOW_REQUIREMENT_INDEX_SCHEMA,
    V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA,
    V553_CONFIDENCE_PENALTY_LEDGER_SCHEMA,
    V553_DOWNSTREAM_V554_HANDOFF_INDEX_SCHEMA,
    V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA,
    V553_EVENT_OVERRIDE_MANIFEST_SCHEMA,
    V553_HARMONIZATION_AUTHORITY_INDEX_SCHEMA,
    V553_WAVE_ANCHOR_INDEX_SCHEMA,
    V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA,
    V553_FORBIDDEN_ACTOR_GENERATION_AUDIT_SCHEMA,
    V553_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
    V553_INTERPOLATION_MANIFEST_SCHEMA,
    V553_INTERPOLATION_SEGMENT_INDEX_SCHEMA,
    V553_INTERPOLATION_POLICY_LEDGER_SCHEMA,
    V553_CROSS_WAVE_DELTA_INDEX_SCHEMA,
    V553_PRESSURE_COMPONENT_BREAKDOWN_SCHEMA,
    V553_PRESSURE_ABSENCE_OVER_TIME_SCHEMA,
    V553_PRESSURE_BASIS_LEDGER_SCHEMA,
    V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA,
    V553_RUN_MANIFEST_SCHEMA,
    V553_RUPTURE_EVENT_SLOT_LEDGER_SCHEMA,
    V553_RUPTURE_BLOCK_AUDIT_SCHEMA,
    V553_TEMPORAL_ANCHOR_INDEX_SCHEMA,
    V553_SOURCE_WAVE_ANCHOR_MANIFEST_SCHEMA,
    V553_SCHEMA_VERSION,
    V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA,
    V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA,
    V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA,
    V553_TEMPORAL_PRESSURE_OBSERVATION_INDEX_SCHEMA,
    V553_TEMPORAL_PRESSURE_FIELD_CONTRACT_SCHEMA,
    V553_YEAR_INDEXED_PRESSURE_OVER_TIME_SCHEMA,
    V553_TEMPORAL_AUTHORITY_LEDGER_SCHEMA,
    V553_TEMPORAL_PRESSURE_FIELD_SCHEMA,
    V553_TEMPORAL_READINESS_REPORT_SCHEMA,
    V553_V554_HANDOFF_INDEX_SCHEMA,
    validate_required_columns,
)
from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record, build_thin_build_ledger
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance

ROOT = Path(__file__).resolve().parents[2]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _report_source(report: dict[str, Any]) -> str:
    source = canonical_family_label(
        report.get("source") or report.get("source_family")
    )
    if not canonical_family_key(source):
        raise SurveyIdentityError("V553 report source is unresolved")
    return source


def _required_source(value: Any) -> str:
    source = canonical_family_label(value)
    if not canonical_family_key(source):
        raise SurveyIdentityError("V553 row source is unresolved")
    return source


def _report_country(report: dict[str, Any]) -> str:
    country = canonical_country_code(
        report.get("country_code") or report.get("country")
    )
    if not country:
        raise SurveyIdentityError("V553 report country_code is unresolved")
    return country


def _required_country(value: Any) -> str:
    country = canonical_country_code(value)
    if not country:
        raise SurveyIdentityError("V553 row country_code is unresolved")
    return country


def _report_wave_year(report: dict[str, Any], wave: Any) -> int:
    canonical = canonical_wave_key(_report_source(report), wave)
    for row in report.get("wave_rows", []) or []:
        if not isinstance(row, dict):
            continue
        row_wave = canonical_wave_key(
            _report_source(report),
            row.get("canonical_wave") or row.get("wave"),
        )
        if row_wave == canonical:
            return _int(row.get("temporal_year"), 0)
    return 0


def _run_id_from_path(value: Any) -> str:
    text = _clean(value)
    if not text:
        return ""
    return Path(text).name or text


def _int(value: Any, default: int = 0) -> int:
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return default
        return int(value)
    except Exception:
        return default


def _pressure_band(value: float) -> str:
    if value >= 0.75:
        return "high"
    if value >= 0.45:
        return "medium"
    if value > 0:
        return "low"
    return "none"


def _bounded_score(value: float, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    if pd.isna(score):
        score = default
    return max(0.0, min(1.0, score))


def _optional_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        if isinstance(value, float) and pd.isna(value):
            return None
        score = float(value)
    except Exception:
        return None
    if pd.isna(score):
        return None
    return score


def _is_audit_fact_lane(value: Any) -> bool:
    return _clean(value) == "audit_fact"


AUTHORIZED_SPARSE_TEMPORAL_KEY = "AUTHORIZED_SPARSE_TEMPORAL_KEY"
PROBE_ONLY_TEMPORAL_KEY = "PROBE_ONLY_TEMPORAL_KEY"
BLOCKED_TEMPORAL_KEY = "BLOCKED_TEMPORAL_KEY"
ALLOWED_MULTI_WAVE_GRAINS = {
    "structural_channel_exact",
    "horizon_exact",
    "relation_target_driver_semantic",
    "relation_target_driver",
}


def _interp(left: float, right: float, fraction: float) -> float:
    return left + ((right - left) * fraction)


def _load_report(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    report = data if isinstance(data, dict) else {}
    for base_key in (
        "shared_semantic_columns",
        "shared_directionality_columns",
        "shared_position_columns",
        "shared_relation_axis_ids",
        "shared_target_entity_ids",
        "shared_driver_facet_ids",
        "shared_structural_channel_ids",
        "shared_horizon_constraint_ids",
    ):
        if report.get(base_key):
            continue
        json_key = f"{base_key}_json"
        parsed = _parse_json_array(report.get(json_key))
        if parsed:
            report[base_key] = parsed
    return report


def _load_optional(path: str | Path | None) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    try:
        return read_table(p)
    except Exception:
        return pd.DataFrame()


def _parse_json_array(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean(item) for item in value if _clean(item)]
    text = _clean(value)
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except Exception:
        return [part.strip() for part in text.split("|") if part.strip()]
    if isinstance(parsed, list):
        return [_clean(item) for item in parsed if _clean(item)]
    if parsed in {"", None}:
        return []
    return [_clean(parsed)]


def _json_array(values: list[Any] | tuple[Any, ...] | set[Any] | None) -> str:
    if not values:
        return "[]"
    cleaned: list[str] = []
    for value in values:
        token = _clean(value)
        if token and token not in cleaned:
            cleaned.append(token)
    return json.dumps(cleaned, sort_keys=True, ensure_ascii=False)


def _json_singleton_array(value: Any) -> str:
    token = _clean(value)
    return _json_array([token] if token else [])


def _resolve_latest_v552j_root(
    source: str,
    wave: str,
    country_code: str = "",
) -> Path | None:
    if not _clean(source) or not _clean(wave):
        return None
    base = ROOT / "data" / "ddm_repository_copy" / "v552j" / "runs"
    if not base.exists():
        return None
    resolved = latest_run_root_for_wave(base, source, wave, country_code)
    return Path(resolved) if resolved else None


def _resolve_repo_path(path_text: str | None) -> Path | None:
    token = _clean(path_text)
    if not token:
        return None
    path = Path(token)
    if path.is_absolute():
        return path
    return ROOT / path


def _wave_v552j_context(item: dict[str, Any]) -> dict[str, Any]:
    wave = _clean(item.get("wave"))
    source = _clean(item.get("source") or item.get("source_family"))
    country_code = canonical_country_code(
        item.get("country_code") or item.get("country")
    )
    explicit_root = _clean(item.get("v552j_run_root")) or _clean(item.get("latest_v552j_root")) or _clean(item.get("run_root"))
    explicit_root_path = _resolve_repo_path(explicit_root) if explicit_root else None
    discovered_root = _resolve_latest_v552j_root(
        source,
        wave,
        country_code,
    )
    resolved_root = None
    if discovered_root is not None and discovered_root.exists():
        resolved_root = discovered_root
    elif explicit_root_path is not None and explicit_root_path.exists():
        resolved_root = explicit_root_path
    readiness_candidates = [
        (resolved_root / "manifest" / "v552j_readiness_report.json") if resolved_root else None,
        _resolve_repo_path(item.get("v552j_readiness_report_path")),
        _resolve_repo_path(item.get("latest_v552j_readiness_report")),
        explicit_root_path / "manifest" / "v552j_readiness_report.json" if explicit_root_path else None,
    ]
    readiness_path = next((path for path in readiness_candidates if path is not None and path.exists()), None)
    readiness = _load_report(readiness_path) if readiness_path else {}
    explicit_input_path = _resolve_repo_path(item.get("v552j_v553_input_index_path"))
    explicit_handoff_path = _resolve_repo_path(item.get("v552j_to_v553_handoff_index_path"))
    explicit_fact_path = _resolve_repo_path(item.get("v552_structural_fact_index_path") or readiness.get("v552_structural_fact_index_path"))
    explicit_key_path = _resolve_repo_path(item.get("v552_temporal_key_source_index_path") or readiness.get("v552_temporal_key_source_index_path"))
    input_candidates = [
        (resolved_root / "packets" / "v552j_v553_input_index.parquet") if resolved_root else None,
        explicit_input_path,
        _resolve_repo_path(item.get("v553_input_index_path")),
        (explicit_root_path / "packets" / "v552j_v553_input_index.parquet") if explicit_root_path else None,
    ]
    handoff_candidates = [
        (resolved_root / "packets" / "v552j_to_v553_handoff_index.parquet") if resolved_root else None,
        explicit_handoff_path,
        (explicit_root_path / "packets" / "v552j_to_v553_handoff_index.parquet") if explicit_root_path else None,
    ]
    input_path = next((path for path in input_candidates if path is not None and path.exists()), None)
    handoff_path = next((path for path in handoff_candidates if path is not None and path.exists()), None)
    if readiness_path and input_path:
        try:
            input_df = read_table(input_path)
        except Exception:
            input_df = pd.DataFrame()
    else:
        input_df = pd.DataFrame()
    handoff_df = pd.DataFrame()
    if handoff_path and handoff_path.exists():
        try:
            handoff_df = read_table(handoff_path)
        except Exception:
            handoff_df = pd.DataFrame()
    resolved_root_text = str((input_path.parent.parent if input_path else (explicit_root_path or resolved_root))) if (input_path or explicit_root_path or resolved_root) else ""
    primary_df = handoff_df if not handoff_df.empty else input_df
    return {
        "wave": wave,
        "resolved_root": resolved_root_text,
        "reported_root": explicit_root,
        "readiness": readiness,
        "readiness_path": str(readiness_path) if readiness_path else "",
        "v552_structural_fact_index_path": str(explicit_fact_path) if explicit_fact_path else "",
        "v552_temporal_key_source_index_path": str(explicit_key_path) if explicit_key_path else "",
        "input_df": input_df,
        "handoff_df": handoff_df,
        "primary_df": primary_df,
    }


def _copy_harmonization_sidecar(
    report_path: str | Path,
    output_root: Path,
    *,
    normalized_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Copy the V553 harmonization sidecar into the per-run V553 root.

    The downstream thin layers expect the harmonization report/evidence to live
    alongside the temporal pressure run root, not only in the repo-wide
    harmonization directory.
    """
    source_report_path = Path(report_path)
    source_evidence_path = Path(
        _clean(_load_report(source_report_path).get("wave_pair_evidence_path"))
        or source_report_path.with_name("v553_wave_harmonization_evidence.parquet")
    )
    target_manifest_dir = output_root / "manifest"
    target_harmonization_dir = output_root / "v553_wave_harmonization"
    target_manifest_dir.mkdir(parents=True, exist_ok=True)
    target_harmonization_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []

    if source_report_path.exists():
        target_report_path = target_manifest_dir / "v553_wave_harmonization_report.json"
        if normalized_report is not None:
            target_report_path.write_text(
                json.dumps(
                    normalized_report,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
        else:
            target_report_path.write_text(source_report_path.read_text(encoding="utf-8"), encoding="utf-8")
        copied.append("manifest/v553_wave_harmonization_report.json")

    if source_evidence_path.exists():
        target_evidence_path = target_harmonization_dir / "v553_wave_harmonization_evidence.parquet"
        if source_evidence_path.resolve() != target_evidence_path.resolve():
            shutil.copy2(source_evidence_path, target_evidence_path)
        copied.append("v553_wave_harmonization/v553_wave_harmonization_evidence.parquet")

    for rel_name in (
        "v553_wave_harmonization_table.csv",
        "v553_wave_harmonization_table.parquet",
        "v553_wave_harmonization_differences.csv",
        "v553_harmonization_difference_ledger.parquet",
        "v553_wave_harmonization_build_ledger.json",
        "v553_repo_discovery_report.json",
    ):
        source = source_report_path.with_name(rel_name)
        if not source.exists():
            continue
        target = target_harmonization_dir / rel_name
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        copied.append(f"v553_wave_harmonization/{rel_name}")

    return {
        "copied": copied,
        "report_path": str(target_manifest_dir / "v553_wave_harmonization_report.json") if "manifest/v553_wave_harmonization_report.json" in copied else "",
        "evidence_path": str(target_harmonization_dir / "v553_wave_harmonization_evidence.parquet") if "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet" in copied else "",
    }


def _build_pressure_rows(report: dict[str, Any], run_id: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    wave_rows = report.get("wave_rows", [])
    if not isinstance(wave_rows, list):
        wave_rows = []

    sorted_years = []
    for row in wave_rows:
        if not isinstance(row, dict):
            continue
        temporal_year = _int(row.get("temporal_year"), 0)
        if temporal_year:
            sorted_years.append(temporal_year)
    first_year = min(sorted_years) if sorted_years else 0

    pressure_rows: list[dict[str, Any]] = []
    contradiction_rows: list[dict[str, Any]] = []
    absence_rows: list[dict[str, Any]] = []
    forbidden_rows: list[dict[str, Any]] = []
    v552j_readiness_status = str(report.get("v552j_readiness_status", "")).strip()
    v552j_blocker_context_count = sum(
        _int(item.get("v552j_blocker_context_count", item.get("blocker_count", 0)), 0)
        for item in (report.get("wave_rows", []) or [])
        if isinstance(item, dict)
    ) or _int(report.get("v552j_blocker_context_count", 0))
    v552j_handoff_authority_status = str(report.get("v552j_handoff_authority_status", "")).strip()

    for index, row in enumerate(wave_rows):
        if not isinstance(row, dict):
            continue
        wave = _clean(row.get("wave"))
        temporal_year = _int(row.get("temporal_year"), 0)
        canonical_wave = _clean(row.get("canonical_wave")) or wave
        source_wave_anchor = _clean(row.get("canonical_wave")) or wave
        source = _clean(row.get("source")) or _report_source(report)
        wave_status = _clean(row.get("wave_status")) or "unknown"
        thin_status = _clean(row.get("thin_status")) or "unknown"
        # Numeric pressure is derived only from explicitly certified authority
        # rows.  Merely finding a heuristic/review overlay must not create a
        # temporal signal.
        overlay_counts = row.get("overlay_certified_row_counts", {}) or {}
        semantic_rows = _int(overlay_counts.get("semantic", 0))
        directionality_rows = _int(overlay_counts.get("directionality", 0))
        position_rows = _int(overlay_counts.get("position", 0))
        shared_semantic = len(report.get("shared_semantic_columns", []) or [])
        shared_directionality = len(report.get("shared_directionality_columns", []) or [])
        shared_position = len(report.get("shared_position_columns", []) or [])

        total_rows = semantic_rows + directionality_rows + position_rows
        all_totals = []
        for candidate in wave_rows:
            if not isinstance(candidate, dict):
                continue
            counts = (
                candidate.get("overlay_certified_row_counts", {}) or {}
            )
            if not isinstance(counts, dict):
                counts = {}
            all_totals.append(
                _int(counts.get("semantic", 0)) + _int(counts.get("directionality", 0)) + _int(counts.get("position", 0))
            )
        max_total_rows = max([1, *all_totals])
        coverage_ratio = min(1.0, total_rows / max_total_rows)

        contradiction_pressure = min(1.0, abs(directionality_rows - semantic_rows) / max(1, total_rows))
        absence_pressure = 1.0 if wave_status != "complete" else 0.0
        uncertainty_pressure = 0.0
        if wave_status != "complete":
            uncertainty_pressure += 0.5
        if thin_status != "READY_V5_THIN_END_TO_END":
            uncertainty_pressure += 0.25
        if shared_directionality == 0 or shared_position == 0:
            uncertainty_pressure += 0.25
        uncertainty_pressure = min(1.0, uncertainty_pressure)
        pressure_intensity = max(0.0, min(1.0, coverage_ratio - (contradiction_pressure * 0.35) - (absence_pressure * 0.25) - (uncertainty_pressure * 0.4)))

        pressure_rows.append(
            {
                "run_id": run_id,
                "layer": "v553",
                "wave": wave,
                "canonical_wave": canonical_wave,
                "source_wave_anchor": source_wave_anchor,
                "source": source,
                "temporal_index": index,
                "temporal_year": temporal_year,
                "years_since_first_wave": max(0, temporal_year - first_year) if first_year else 0,
                "years_since_previous_wave": max(
                    0,
                    temporal_year
                    - _int(wave_rows[index - 1].get("temporal_year")),
                )
                if index > 0 and isinstance(wave_rows[index - 1], dict)
                else 0,
                "temporal_scope": "wave_harmonization",
                "pressure_status": "ready" if wave_status == "complete" else "ready_with_gaps",
                "pressure_intensity": round(pressure_intensity, 6),
                "pressure_intensity_band": _pressure_band(pressure_intensity),
                "contradiction_pressure": round(contradiction_pressure, 6),
                "absence_pressure": round(absence_pressure, 6),
                "uncertainty_pressure": round(uncertainty_pressure, 6),
                "shared_semantic_column_count": shared_semantic,
                "shared_directionality_column_count": shared_directionality,
                "shared_position_column_count": shared_position,
                "v552j_readiness_status": v552j_readiness_status,
                "v552j_blocker_context_count": v552j_blocker_context_count,
                "v552j_handoff_authority_status": v552j_handoff_authority_status,
                "wave_status": wave_status,
                "thin_status": thin_status,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
        contradiction_rows.append(
            {
                "run_id": run_id,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "source": source,
                "source_wave_anchor": source_wave_anchor,
                "contradiction_pressure": round(contradiction_pressure, 6),
                "pressure_status": "ready" if wave_status == "complete" else "ready_with_gaps",
                "wave_status": wave_status,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
        absence_rows.append(
            {
                "run_id": run_id,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "source": source,
                "source_wave_anchor": source_wave_anchor,
                "absence_pressure": round(absence_pressure, 6),
                "pressure_status": "ready" if wave_status == "complete" else "ready_with_gaps",
                "wave_status": wave_status,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
        forbidden_rows.append(
            {
                "run_id": run_id,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "source": source,
                "claim_id": "do_not_generate_actor_or_biography",
                "reason": "V553 must remain temporal structure, not runtime personhood.",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )

    return pd.DataFrame(pressure_rows), pd.DataFrame(contradiction_rows), pd.DataFrame(absence_rows), forbidden_rows


def _build_interpolated_pressure_rows(pressure_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if pressure_df.empty or "temporal_year" not in pressure_df.columns:
        return pd.DataFrame()

    anchors = pressure_df.sort_values(["temporal_year", "temporal_index"]).reset_index(drop=True)
    years = [int(year) for year in anchors["temporal_year"].tolist() if str(year).strip()]
    if not years:
        return pd.DataFrame()

    year_range = range(min(years), max(years) + 1)
    rows: list[dict[str, Any]] = []
    anchor_records = anchors.to_dict(orient="records")

    for year in year_range:
        left = anchor_records[0]
        right = anchor_records[-1]
        for candidate in anchor_records:
            if int(candidate["temporal_year"]) <= year:
                left = candidate
            if int(candidate["temporal_year"]) >= year:
                right = candidate
                break
        left_year = int(left["temporal_year"])
        right_year = int(right["temporal_year"])
        if right_year == left_year:
            fraction = 0.0
        else:
            fraction = (year - left_year) / (right_year - left_year)

        pressure_intensity = _interp(float(left["pressure_intensity"]), float(right["pressure_intensity"]), fraction)
        contradiction_pressure = _interp(float(left["contradiction_pressure"]), float(right["contradiction_pressure"]), fraction)
        absence_pressure = _interp(float(left["absence_pressure"]), float(right["absence_pressure"]), fraction)
        uncertainty_pressure = _interp(float(left["uncertainty_pressure"]), float(right["uncertainty_pressure"]), fraction)

        rows.append(
            {
                "run_id": run_id,
                "layer": "v553",
                "wave": str(year),
                "canonical_wave": str(year),
                "source_wave_anchor": _clean(left.get("source_wave_anchor", "")) or _clean(left.get("canonical_wave", "")) or _clean(left.get("wave", "")),
                "source": _required_source(left.get("source")),
                "temporal_index": year - min(years),
                "temporal_year": year,
                "years_since_first_wave": year - min(years),
                "years_since_previous_wave": 0 if year == min(years) else 1,
                "temporal_scope": "year_interpolated",
                "pressure_status": "interpolated" if year not in years else "anchor",
                "pressure_intensity": round(max(0.0, min(1.0, pressure_intensity)), 6),
                "pressure_intensity_band": _pressure_band(max(0.0, min(1.0, pressure_intensity))),
                "contradiction_pressure": round(max(0.0, min(1.0, contradiction_pressure)), 6),
                "absence_pressure": round(max(0.0, min(1.0, absence_pressure)), 6),
                "uncertainty_pressure": round(max(0.0, min(1.0, uncertainty_pressure)), 6),
                "shared_semantic_column_count": int(left.get("shared_semantic_column_count", 0) or 0),
                "shared_directionality_column_count": int(left.get("shared_directionality_column_count", 0) or 0),
                "shared_position_column_count": int(left.get("shared_position_column_count", 0) or 0),
                "wave_status": "complete" if year in years else "interpolated",
                "thin_status": left.get("thin_status", ""),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )

    return pd.DataFrame(rows)


def _build_source_wave_anchor_manifest(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in report.get("wave_rows", []) or []:
        if not isinstance(item, dict):
            continue
        wave = _clean(item.get("wave"))
        if not wave:
            continue
        v552j_context = _wave_v552j_context(item)
        missing = list(item.get("missing_authority_kinds", []) or [])
        wave_status = _clean(item.get("wave_status")) or "unknown"
        if wave_status == "complete" and not missing:
            usable_for_temporalization = True
            source_authority_status = "anchor_derived"
        elif wave_status == "partial":
            usable_for_temporalization = False
            source_authority_status = "cautious_interpolation_allowed"
        else:
            usable_for_temporalization = False
            source_authority_status = "blocked_no_anchor"
        rows.append(
            {
                "run_id": run_id,
                "country_code": _clean(item.get("country_code")) or _report_country(report),
                "wave_id": wave,
                "survey_family": _clean(item.get("source")) or _report_source(report),
                "survey_year": _int(item.get("temporal_year"), 0),
                "fieldwork_year_start": _int(item.get("temporal_year"), 0),
                "fieldwork_year_end": _int(item.get("temporal_year"), 0),
                "source_run_id": _run_id_from_path(v552j_context.get("resolved_root") or item.get("latest_v552j_root") or item.get("run_root")),
                "source_authority_status": source_authority_status,
                "usable_for_temporalization": usable_for_temporalization,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_WAVE_ANCHOR_INDEX_SCHEMA["required_columns"])


def _build_temporal_anchor_index(source_wave_anchor_manifest_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if source_wave_anchor_manifest_df.empty:
        return pd.DataFrame(columns=V553_TEMPORAL_ANCHOR_INDEX_SCHEMA["required_columns"])
    return source_wave_anchor_manifest_df.copy()


def _build_harmonization_authority_index(report: dict[str, Any], readiness_score: float, run_id: str) -> pd.DataFrame:
    authority_status = (
        "multi_wave_harmonization_authorized"
        if bool(report.get("ready_for_v553", False)) and _clean(report.get("comparison_authority_status")) == "multi_wave_authorized"
        else "blocked_harmonization_authority"
    )
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "source_family": _report_source(report),
                "source": _report_source(report),
                "country_code": _report_country(report),
                "authority_status": authority_status,
                "wave_count": int(report.get("wave_count", 0) or 0),
                "wave_pair_count": int(report.get("wave_pair_count", 0) or 0),
                "multiple_waves_present": bool(report.get("multiple_waves_present", False)),
                "ready_for_v553": bool(report.get("ready_for_v553", False)),
                "comparability_status": _clean(report.get("comparability_status")) or "comparability_limited",
                "harmonization_score": _bounded_score(readiness_score),
                "required_authority_kinds_json": json.dumps(list(report.get("required_authority_kinds", []) or []), sort_keys=True),
                "blocking_conditions_json": json.dumps(list(report.get("blocking_conditions", []) or []), sort_keys=True),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        ],
        columns=V553_HARMONIZATION_AUTHORITY_INDEX_SCHEMA["required_columns"],
    )


def _authorize_v553_multi_wave_key(
    report: dict[str, Any],
    group: pd.DataFrame,
) -> dict[str, Any]:
    harmonizer_authorized = bool(
        report.get("ready_for_v553", False)
        and report.get("comparison_authority_status") == "multi_wave_authorized"
        and report.get("shared_semantic_columns")
        and report.get("shared_directionality_columns")
        and report.get("shared_position_columns")
    )
    eligible_rows: list[dict[str, Any]] = []
    resolved_wave_count = 0
    probe_ready_wave_ids: set[str] = set()
    for _, row in group.iterrows():
        wave = _clean(row.get("wave_id"))
        if _clean(row.get("structural_dimension_status")) == "resolved":
            resolved_wave_count += 1
        if int(row.get("probe_ready_input_count", 0) or 0) > 0 and wave:
            probe_ready_wave_ids.add(wave)
        packet_ids = _parse_json_array(row.get("source_v552j_packet_ids_json"))
        structural_value = _optional_float(row.get("structural_pressure_value"))
        eligible = bool(
            int(row.get("probe_ready_input_count", 0) or 0) > 0
            and _clean(row.get("structural_dimension_status")) == "resolved"
            and _clean(row.get("comparable_key_grain")) in ALLOWED_MULTI_WAVE_GRAINS
            and not _is_audit_fact_lane(row.get("source_v552_structural_fact_lane"))
            and _clean(row.get("canonical_semantic_signature")) not in {"", "unknown_semantic_signature"}
            and structural_value is not None
            and bool(packet_ids)
        )
        if eligible:
            eligible_rows.append(row.to_dict())
    eligible_wave_ids = sorted({_clean(row.get("wave_id")) for row in eligible_rows if _clean(row.get("wave_id"))})
    first = group.iloc[0].to_dict() if not group.empty else {}
    if harmonizer_authorized and len(eligible_wave_ids) >= 2:
        status = AUTHORIZED_SPARSE_TEMPORAL_KEY
        reason = "at_least_two_probe_ready_resolved_structural_anchors"
        ready_for_v554 = True
        return {
            "multi_wave_authorization_status": status,
            "multi_wave_authorization_reason": reason,
            "harmonization_authority_status": "multi_wave_authorized",
            "semantic_compatibility_status": "compatible_by_canonical_key",
            "directionality_compatibility_status": "compatible_by_harmonizer_shared_contract",
            "position_compatibility_status": "compatible_by_harmonizer_shared_contract",
            "structural_identity_compatibility_status": "compatible_by_comparable_temporal_key",
            "ready_for_v554": ready_for_v554,
            "eligible_wave_count": len(eligible_wave_ids),
            "distinct_wave_count": len(sorted({_clean(v) for v in group.get("wave_id", pd.Series(dtype=str)).tolist() if _clean(v)})),
            "probe_ready_wave_count": len(probe_ready_wave_ids),
            "resolved_wave_count": resolved_wave_count,
            "authorized_anchor_count": len(eligible_wave_ids),
            "probe_anchor_count": 0,
        }
    if len(eligible_wave_ids) == 1:
        status = PROBE_ONLY_TEMPORAL_KEY
        reason = "insufficient_distinct_waves"
    elif not harmonizer_authorized:
        status = BLOCKED_TEMPORAL_KEY
        reason = "harmonization_not_authorized"
    elif _clean(first.get("comparable_key_grain")) not in ALLOWED_MULTI_WAVE_GRAINS or _clean(first.get("fallback_permission_profile_key")):
        status = BLOCKED_TEMPORAL_KEY
        reason = "fallback_or_lower_grain_key"
    elif not group.get("structural_dimension_status", pd.Series(dtype=str)).astype(str).eq("resolved").any():
        status = BLOCKED_TEMPORAL_KEY
        reason = "structural_dimensions_unresolved"
    elif _clean(first.get("canonical_semantic_signature")) in {"", "unknown_semantic_signature"}:
        status = BLOCKED_TEMPORAL_KEY
        reason = "unknown_semantic_signature"
    elif not pd.to_numeric(group.get("structural_pressure_value", pd.Series(dtype=float)), errors="coerce").notna().any():
        status = BLOCKED_TEMPORAL_KEY
        reason = "missing_structural_pressure_value"
    elif not any(_parse_json_array(value) for value in group.get("source_v552j_packet_ids_json", pd.Series(dtype=str)).tolist()):
        status = BLOCKED_TEMPORAL_KEY
        reason = "missing_packet_provenance"
    elif not probe_ready_wave_ids:
        status = BLOCKED_TEMPORAL_KEY
        reason = "no_probe_ready_wave"
    else:
        status = PROBE_ONLY_TEMPORAL_KEY
        reason = "insufficient_distinct_waves"
    return {
        "multi_wave_authorization_status": status,
        "multi_wave_authorization_reason": reason,
        "harmonization_authority_status": "multi_wave_authorized" if harmonizer_authorized else "not_authorized",
        "semantic_compatibility_status": "blocked" if status == BLOCKED_TEMPORAL_KEY else "compatible_by_canonical_key",
        "directionality_compatibility_status": "blocked" if status == BLOCKED_TEMPORAL_KEY else "compatible_by_harmonizer_shared_contract",
        "position_compatibility_status": "blocked" if status == BLOCKED_TEMPORAL_KEY else "compatible_by_harmonizer_shared_contract",
        "structural_identity_compatibility_status": "blocked" if status == BLOCKED_TEMPORAL_KEY else "compatible_by_comparable_temporal_key",
        "ready_for_v554": False,
        "eligible_wave_count": len(eligible_wave_ids),
        "distinct_wave_count": len(sorted({_clean(v) for v in group.get("wave_id", pd.Series(dtype=str)).tolist() if _clean(v)})),
        "probe_ready_wave_count": len(probe_ready_wave_ids),
        "resolved_wave_count": resolved_wave_count,
        "authorized_anchor_count": 0,
        "probe_anchor_count": len(eligible_wave_ids) if status == PROBE_ONLY_TEMPORAL_KEY else 0,
    }


def _build_interpolation_policy_ledger(
    report: dict[str, Any],
    pressure_df: pd.DataFrame,
    allow_interpolation: bool,
    run_id: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    anchors = pressure_df.sort_values(["temporal_year", "temporal_index"]).reset_index(drop=True)
    years = [int(year) for year in anchors.get("temporal_year", pd.Series(dtype=int)).tolist() if str(year).strip()]
    if not years:
        return pd.DataFrame(columns=V553_INTERPOLATION_POLICY_LEDGER_SCHEMA["required_columns"])
    anchor_years = set(years)
    for year in range(min(years), max(years) + 1):
        is_anchor = year in anchor_years
        rows.append(
            {
                "run_id": run_id,
                "source_family": _report_source(report),
                "source": _report_source(report),
                "country_code": _report_country(report),
                "year": year,
                "wave_before": str(year) if is_anchor else "",
                "wave_after": str(year) if is_anchor else "",
                "interpolation_method": "anchor_copy" if is_anchor else ("linear_between_authorized_waves" if allow_interpolation else "gap_marked_unknown"),
                "interpolation_allowed": bool(allow_interpolation and not is_anchor),
                "interpolation_status": "anchor" if is_anchor else ("interpolated" if allow_interpolation else "unknown_noncomparable"),
                "interpolation_authority": "wave_harmonization_report",
                "interpolation_reason": "anchor_year_not_interpolated" if is_anchor else ("authorized_gap_interpolation" if allow_interpolation else "missing_gap_stays_unknown_noncomparable"),
                "confidence_penalty": 0.0 if is_anchor else (0.15 if allow_interpolation else 1.0),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_INTERPOLATION_POLICY_LEDGER_SCHEMA["required_columns"])


def _build_rupture_event_slot_ledger(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    source_family = _report_source(report)
    source = _report_source(report)
    country_code = _report_country(report)
    rows = [
        {
            "run_id": run_id,
            "source_family": source_family,
            "source": source,
            "country_code": country_code,
            "slot_name": "event_context",
            "slot_status": "not_supplied",
            "event_authority_ref": "",
            "rupture_override_status": "reserved_not_filled",
            "event_registry_status": "not_supplied",
            "manual_review_required": True,
            "created_at": utc_now(),
            "schema_version": V553_SCHEMA_VERSION,
            "compiler_version": V553_COMPILER_VERSION,
        },
        {
            "run_id": run_id,
            "source_family": source_family,
            "source": source,
            "country_code": country_code,
            "slot_name": "rupture_override",
            "slot_status": "reserved",
            "event_authority_ref": "",
            "rupture_override_status": "reserved_not_filled",
            "event_registry_status": "not_supplied",
            "manual_review_required": False,
            "created_at": utc_now(),
            "schema_version": V553_SCHEMA_VERSION,
            "compiler_version": V553_COMPILER_VERSION,
        },
    ]
    return pd.DataFrame(rows, columns=V553_RUPTURE_EVENT_SLOT_LEDGER_SCHEMA["required_columns"])


def _build_cohort_window_requirement_index(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    source_family = _report_source(report)
    source = _report_source(report)
    country_code = _report_country(report)
    windows = [
        "birth_cohort_window",
        "parent_formative_window",
        "child_developmental_window",
        "household_period_window",
    ]
    rows = [
        {
            "run_id": run_id,
            "source_family": source_family,
            "source": source,
            "country_code": country_code,
            "window_name": window,
            "window_status": "reserved_not_filled",
            "window_required": True,
            "window_authority": "v553_temporal_pressure_field",
            "created_at": utc_now(),
            "schema_version": V553_SCHEMA_VERSION,
            "compiler_version": V553_COMPILER_VERSION,
        }
        for window in windows
    ]
    return pd.DataFrame(rows, columns=V553_COHORT_WINDOW_REQUIREMENT_INDEX_SCHEMA["required_columns"])


def _build_absence_noncomparability_register(
    report: dict[str, Any],
    pressure_df: pd.DataFrame,
    country_year_pressure_df: pd.DataFrame,
    allow_interpolation: bool,
    run_id: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    source_family = _report_source(report)
    source = _report_source(report)
    country_code = _report_country(report)
    structural_axes = _shared_structural_axis_fields(report)
    anchor_years = {int(v) for v in pressure_df.get("temporal_year", pd.Series(dtype=int)).dropna().astype(int).tolist()} if not pressure_df.empty else set()
    if anchor_years:
        for year in range(min(anchor_years), max(anchor_years) + 1):
            if year in anchor_years:
                continue
            rows.append(
                {
                    "run_id": run_id,
                    "source_family": source_family,
                    "source": source,
                    "country_code": country_code,
                    "year": year,
                    "wave": str(year),
                    "canonical_wave": str(year),
                    "register_kind": "missing_year",
                    "register_status": "unknown_noncomparable",
                    "register_reason": "missing_gap_stays_unknown_noncomparable",
                    "missing_authority_kinds_json": json.dumps(list(report.get("required_authority_kinds", []) or []), sort_keys=True),
                    "comparability_status": "unknown_noncomparable" if not allow_interpolation else "interpolated_with_authority",
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    for item in report.get("cross_wave_noncomparability_matrix", []) or []:
        if not isinstance(item, dict):
            continue
        rows.append(
            {
                "run_id": run_id,
                "source_family": source_family,
                "source": source,
                "country_code": country_code,
                "year": _report_wave_year(
                    report,
                    item.get("current_wave"),
                ),
                "wave": _clean(item.get("current_wave")) or "",
                "canonical_wave": _clean(item.get("current_wave")) or "",
                "register_kind": "cross_wave_noncomparability",
                "register_status": "partial" if _clean(item.get("pair_harmonization_status")) != "aligned" else "ready",
                "register_reason": "cross_wave_noncomparability_matrix",
                "missing_authority_kinds_json": json.dumps(list(report.get("required_authority_kinds", []) or []), sort_keys=True),
                "comparability_status": _clean(item.get("comparability_status")) or "partial",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    for item in report.get("wave_rows", []) or []:
        if not isinstance(item, dict):
            continue
        v552j_context = _wave_v552j_context(item)
        input_df = v552j_context.get("input_df", pd.DataFrame())
        if input_df.empty:
            continue
        blocker_counts = {
            "ready_for_v553_false": int((~input_df.get("ready_for_v553", pd.Series(dtype=bool)).astype(bool)).sum()) if "ready_for_v553" in input_df.columns else 0,
            "temporal_field_allowed_false": int((~input_df.get("temporal_field_allowed", pd.Series(dtype=bool)).astype(bool)).sum()) if "temporal_field_allowed" in input_df.columns else 0,
            "single_wave_probe_only": int(input_df.get("single_wave_probe_allowed", pd.Series(dtype=bool)).astype(bool).sum()) if "single_wave_probe_allowed" in input_df.columns else 0,
        }
        blocker_reason = "v552j_probe_only_or_temporal_field_blocked"
        register_status = "probe_only" if blocker_counts["temporal_field_allowed_false"] > 0 else "reviewable"
        rows.append(
            {
                "run_id": run_id,
                "source_family": source_family,
                "source": source,
                "country_code": country_code,
                "year": _int(item.get("temporal_year"), 0),
                "wave": _clean(item.get("wave")) or "",
                "canonical_wave": _clean(item.get("canonical_wave")) or _clean(item.get("wave")) or "",
                "register_kind": "v552j_blocker_context",
                "register_status": register_status,
                "register_reason": blocker_reason,
                "missing_authority_kinds_json": json.dumps(
                    sorted(
                        set(
                            [kind for kind in (_parse_json_array(item.get("missing_authority_kinds")) if item.get("missing_authority_kinds") is not None else []) if kind]
                        )
                        | {"temporal_field_allowed_false" if blocker_counts["temporal_field_allowed_false"] > 0 else ""}
                        - {""}
                    ),
                    sort_keys=True,
                ),
                "comparability_status": _clean(item.get("v552j_handoff_authority_status")) or _clean(item.get("v552j_readiness_status")) or "probe_only",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    if not rows and not country_year_pressure_df.empty:
        for _, row in country_year_pressure_df.iterrows():
            if _clean(row.get("pressure_status")) in {"anchor_derived", "linear_interpolated", "anchor_copy"}:
                continue
            rows.append(
                {
                    "run_id": run_id,
                    "source_family": source_family,
                    "source": source,
                    "country_code": country_code,
                    "year": _int(row.get("year"), 0),
                    "wave": _clean(row.get("wave_before")) or _clean(row.get("year")) or "",
                    "canonical_wave": _clean(row.get("wave_before")) or _clean(row.get("year")) or "",
                    "register_kind": "pressure_gap",
                    "register_status": "unknown_noncomparable",
                    "register_reason": _clean(row.get("pressure_status")) or "blocked_no_comparability",
                    "missing_authority_kinds_json": json.dumps([], sort_keys=True),
                    "comparability_status": "unknown_noncomparable",
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V553_ABSENCE_NONCOMPARABILITY_REGISTER_SCHEMA["required_columns"])


def _build_country_year_pressure_field(
    report: dict[str, Any],
    pressure_df: pd.DataFrame,
    interpolated_pressure_df: pd.DataFrame,
    run_id: str,
    *,
    allow_interpolation: bool,
) -> pd.DataFrame:
    source_family = _report_source(report)
    source = _report_source(report)
    country_code = _report_country(report)
    anchors = pressure_df.sort_values(["temporal_year", "temporal_index"]).reset_index(drop=True)
    if anchors.empty:
        return pd.DataFrame(columns=V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA["required_columns"])
    structural_axes = _shared_structural_axis_fields(report)
    anchor_records = anchors.to_dict(orient="records")
    years = [int(row["temporal_year"]) for row in anchor_records if str(row.get("temporal_year", "")).strip()]
    if not years:
        return pd.DataFrame(columns=V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    interp_records = interpolated_pressure_df.to_dict(orient="records") if not interpolated_pressure_df.empty else []
    interp_by_year = {int(row.get("temporal_year", 0) or 0): row for row in interp_records if _clean(row.get("temporal_year"))}
    min_year = min(years)
    max_year = max(years)
    year_iter = range(min_year, max_year + 1)
    for year in year_iter:
        left = anchor_records[0]
        right = anchor_records[-1]
        for candidate in anchor_records:
            if int(candidate["temporal_year"]) <= year:
                left = candidate
            if int(candidate["temporal_year"]) >= year:
                right = candidate
                break
        left_year = int(left["temporal_year"])
        right_year = int(right["temporal_year"])
        if right_year == left_year:
            fraction = 0.0
        else:
            fraction = (year - left_year) / (right_year - left_year)
        source_row = interp_by_year.get(year) or (left if year in years else right)
        if year in years:
            pressure_value = _bounded_score(float(source_row.get("pressure_intensity", 0.0) or 0.0))
            pressure_band = _clean(source_row.get("pressure_intensity_band")) or _pressure_band(pressure_value)
            interpolation_method = "anchor_copy"
            pressure_status = _clean(source_row.get("pressure_status")) or "anchor_derived"
        else:
            pressure_value = 0.0
            pressure_band = "unknown"
            interpolation_method = "gap_marked_unknown" if not allow_interpolation else "linear_between_authorized_waves"
            pressure_status = "blocked_no_comparability" if not allow_interpolation else "cautious_interpolation_allowed"
        pressure_domain = "country_year_structural_pressure"
        structural_channel_id = structural_axes["structural_channel_id"]
        horizon_constraint_id = structural_axes["horizon_constraint_id"]
        relation_axis_id = structural_axes["relation_axis_id"]
        target_entity_id = structural_axes["target_entity_id"]
        driver_facet_id = structural_axes["driver_facet_id"]
        if not _clean(report.get("ready_for_v553")):
            pressure_status = "blocked_no_comparability"
        basis_json = json.dumps(
            {
                "source_wave_anchor": _clean(source_row.get("source_wave_anchor")) or _clean(left.get("source_wave_anchor")) or _clean(left.get("canonical_wave")) or _clean(left.get("wave")),
                "wave_before": _clean(left.get("wave")),
                "wave_after": _clean(right.get("wave")),
                "fraction": fraction,
                "shared_semantic_column_count": int(source_row.get("shared_semantic_column_count", 0) or 0),
                "shared_directionality_column_count": int(source_row.get("shared_directionality_column_count", 0) or 0),
                "shared_position_column_count": int(source_row.get("shared_position_column_count", 0) or 0),
                "comparability_status": _clean(report.get("comparability_status")) or "comparability_limited",
            },
            sort_keys=True,
        )
        rows.append(
            {
                "run_id": run_id,
                "source_family": source_family,
                "source": source,
                "country_code": country_code,
                "year": year,
                "wave_before": _clean(left.get("wave")),
                "wave_after": _clean(right.get("wave")),
                "wave_year_before": left_year,
                "wave_year_after": right_year,
                "pressure_domain": pressure_domain,
                "relation_axis_id": relation_axis_id,
                "target_entity_id": target_entity_id,
                "driver_facet_id": driver_facet_id,
                "structural_channel_id": structural_channel_id,
                "horizon_constraint_id": horizon_constraint_id,
                "pressure_value_distribution": json.dumps(
                    {"point_estimate": None if year not in years and not allow_interpolation else pressure_value, "band": pressure_band, "source": pressure_status},
                    sort_keys=True,
                ),
                "pressure_intensity_band": pressure_band,
                "pressure_status": pressure_status,
                "interpolation_method": interpolation_method,
                "confidence_penalty": round(
                    max(
                        0.0,
                        min(
                            1.0,
                            (1.0 - pressure_value)
                            + (0.10 if not _clean(report.get("ready_for_v553")) else 0.0)
                            + (0.05 if year not in years else 0.0)
                            + (0.60 if year not in years and not allow_interpolation else 0.0),
                        ),
                    ),
                    6,
                ),
                "basis_json": basis_json,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA["required_columns"])


def _build_pressure_component_breakdown(country_year_pressure_df: pd.DataFrame, report: dict[str, Any], run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in country_year_pressure_df.iterrows():
        distribution = {}
        try:
            distribution = json.loads(str(row.get("pressure_value_distribution", "") or "{}"))
        except Exception:
            distribution = {}
        pressure_intensity = _bounded_score(float(distribution.get("point_estimate", 0.0) or 0.0))
        coverage_pressure = round(max(0.0, 1.0 - pressure_intensity), 6)
        structural_domain_pressure = round(max(0.0, pressure_intensity * 0.45), 6)
        contradiction_pressure = round(max(0.0, pressure_intensity * 0.15), 6)
        absence_pressure = round(max(0.0, pressure_intensity * 0.10), 6)
        uncertainty_pressure = round(max(0.0, float(row.get("confidence_penalty", 0.0) or 0.0)), 6)
        rupture_pressure = round(max(0.0, pressure_intensity * (0.10 if row.get("pressure_status") not in {"anchor_derived", "linear_interpolated", "anchor_copy"} else 0.0)), 6)
        comparability_pressure = round(max(0.0, pressure_intensity * 0.15), 6)
        authority_pressure = round(max(0.0, pressure_intensity * 0.20), 6)
        rows.append(
            {
                "run_id": run_id,
                "source_family": row.get("source_family", ""),
                "source": row.get("source", ""),
                "country_code": row.get("country_code", ""),
                "year": int(row.get("year", 0) or 0),
                "pressure_domain": row.get("pressure_domain", ""),
                "coverage_pressure": coverage_pressure,
                "structural_domain_pressure": structural_domain_pressure,
                "contradiction_pressure": contradiction_pressure,
                "absence_pressure": absence_pressure,
                "uncertainty_pressure": uncertainty_pressure,
                "rupture_pressure": rupture_pressure,
                "comparability_pressure": comparability_pressure,
                "authority_pressure": authority_pressure,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_PRESSURE_COMPONENT_BREAKDOWN_SCHEMA["required_columns"])


def _build_interpolation_manifest(country_year_pressure_df: pd.DataFrame, run_id: str, *, allow_interpolation: bool) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in country_year_pressure_df.iterrows():
        is_anchor = _clean(row.get("interpolation_method")) == "anchor_copy"
        rows.append(
            {
                "run_id": run_id,
                "source_family": row.get("source_family", ""),
                "source": row.get("source", ""),
                "country_code": row.get("country_code", ""),
                "year": int(row.get("year", 0) or 0),
                "wave_before": row.get("wave_before", ""),
                "wave_after": row.get("wave_after", ""),
                "distance_to_nearest_wave": 0 if is_anchor else 1,
                "distance_between_anchors": max(0, int(row.get("wave_year_after", 0) or 0) - int(row.get("wave_year_before", 0) or 0)),
                "interpolation_method": row.get("interpolation_method", ""),
                "interpolation_authority": "wave_harmonization_report",
                "confidence_penalty": row.get("confidence_penalty", 0.0),
                "event_override_flag": False,
                "event_ids_json": json.dumps([], sort_keys=True),
                "rupture_blocked": not is_anchor and not allow_interpolation,
                "manual_review_required": not is_anchor,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_INTERPOLATION_MANIFEST_SCHEMA["required_columns"])


def _build_event_override_manifest(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "source_family": _report_source(report),
                "source": _report_source(report),
                "country_code": _report_country(report),
                "event_registry_status": "not_supplied",
                "interpolation_across_rupture_allowed": False,
                "override_count": 0,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        ],
        columns=V553_EVENT_OVERRIDE_MANIFEST_SCHEMA["required_columns"],
    )


def _build_temporal_authority_ledger(
    report: dict[str, Any],
    observation_df: pd.DataFrame,
    gap_df: pd.DataFrame,
    run_id: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in observation_df.iterrows():
        temporal_status = _clean(row.get("temporal_status"))
        if temporal_status == "observed_authorized_anchor":
            authority_status = "authorized_observed_anchor"
            use_permission_class = "v554_sparse_temporal_anchor"
            anchor_status = "observed_authorized_anchor"
        else:
            authority_status = "probe_only_anchor"
            use_permission_class = "diagnostic_only"
            anchor_status = "probe_only_anchor"
        rows.append(
            {
                "run_id": run_id,
                "source_family": _report_source(report),
                "source": _report_source(report),
                "country_code": _clean(row.get("country")) or _report_country(report),
                "year": int(row.get("survey_year", 0) or 0),
                "wave": row.get("wave_id", ""),
                "canonical_wave": row.get("wave_id", ""),
                "anchor_status": anchor_status,
                "anchor_authority": _clean(row.get("structural_pressure_authority")) or "v553_sparse_temporal",
                "anchor_confidence": _bounded_score(float(row.get("confidence_score", 0.0) or 0.0)),
                "authority_status": authority_status,
                "use_permission_class": use_permission_class,
                "confidence_penalty": round(1.0 - _bounded_score(float(row.get("confidence_score", 0.0) or 0.0)), 6),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    for _, row in gap_df.iterrows():
        rows.append(
            {
                "run_id": run_id,
                "source_family": _report_source(report),
                "source": _report_source(report),
                "country_code": _clean(row.get("country")) or _report_country(report),
                "year": int(row.get("missing_year_or_span", 0) or 0),
                "wave": "",
                "canonical_wave": "",
                "anchor_status": "unknown_gap",
                "anchor_authority": "known_unknown_gap",
                "anchor_confidence": 0.0,
                "authority_status": "known_unknown_gap",
                "use_permission_class": "absence_metadata_only",
                "confidence_penalty": 1.0,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_TEMPORAL_AUTHORITY_LEDGER_SCHEMA["required_columns"])


def _build_comparability_audit(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for evidence in report.get("wave_pair_evidence", []) or []:
        if not isinstance(evidence, dict):
            continue
        rows.append(
            {
                "run_id": run_id,
                "prior_wave": evidence.get("prior_wave", ""),
                "current_wave": evidence.get("current_wave", ""),
                "shared_semantic_column_count": int(evidence.get("shared_semantic_column_count", 0) or 0),
                "shared_directionality_column_count": int(evidence.get("shared_directionality_column_count", 0) or 0),
                "shared_position_column_count": int(evidence.get("shared_position_column_count", 0) or 0),
                "pair_missing_authority_count": int(evidence.get("pair_missing_authority_count", 0) or 0),
                "comparability_status": "comparable" if _clean(evidence.get("pair_harmonization_status")) == "aligned" and int(evidence.get("pair_missing_authority_count", 0) or 0) == 0 else "partial",
                "wave_pair_evidence_score": float(evidence.get("pair_harmonization_score", 0.0) or 0.0),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_COMPARABILITY_AUDIT_SCHEMA["required_columns"])


def _build_rupture_block_audit(report: dict[str, Any], country_year_pressure_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in country_year_pressure_df.iterrows():
        rupture_blocked = _clean(row.get("pressure_status")) not in {"anchor_derived", "linear_interpolated", "anchor_copy"}
        rows.append(
            {
                "run_id": run_id,
                "source_family": row.get("source_family", ""),
                "source": row.get("source", ""),
                "country_code": row.get("country_code", ""),
                "year": int(row.get("year", 0) or 0),
                "wave": row.get("wave_before", ""),
                "canonical_wave": row.get("wave_before", ""),
                "rupture_blocked": rupture_blocked,
                "rupture_reason": "not_supplied" if not rupture_blocked else "interpolation_requires_manual_review",
                "manual_review_required": rupture_blocked,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_RUPTURE_BLOCK_AUDIT_SCHEMA["required_columns"])


def _build_downstream_v554_handoff_index(report: dict[str, Any], country_year_pressure_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    blocked_rows = int(country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str).str.startswith("blocked_").sum()) if not country_year_pressure_df.empty else 0
    review_required_rows = int((country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str) != "anchor_derived").sum()) if not country_year_pressure_df.empty else 0
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "status": "LEGACY_COMPATIBILITY_SHADOW_BLOCKED",
                "ready_for_v554": False,
                "handoff_role": "legacy_compatibility_shadow",
                "legacy_compatibility_only": True,
                "authoritative_handoff_path": "",
                "authoritative_handoff_status": "v553_v554_handoff_index",
                "pressure_field_rows": int(len(country_year_pressure_df)),
                "country_year_rows": int(len(country_year_pressure_df)),
                "contradiction_rows": int(len(country_year_pressure_df)),
                "absence_rows": int(len(country_year_pressure_df)),
                "blocked_rows": blocked_rows,
                "review_required_rows": review_required_rows,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        ],
        columns=V553_DOWNSTREAM_V554_HANDOFF_INDEX_SCHEMA["required_columns"],
    )


def _stable_temporal_pressure_key(
    source: str,
    country_code: str,
    relation_axis: str,
    target_entity: str,
    driver_facet: str,
    structural_channel: str,
    semantic_signature: str,
    *,
    key_grain: str = "structural_channel",
) -> str:
    payload = "|".join(
        [
            _clean(key_grain) or "structural_channel",
            _required_source(source),
            _required_country(country_code),
            _clean(relation_axis) or "unknown_relation_axis",
            _clean(target_entity) or "unknown_target_entity",
            _clean(driver_facet) or "unknown_driver_facet",
            _clean(structural_channel) or "unknown_structural_channel",
            _clean(semantic_signature) or "unknown_semantic_signature",
        ]
    )
    return f"v553tp_{hashlib.sha1(payload.encode('utf-8')).hexdigest()[:12]}"


def _canonical_semantic_signature(*parts: Any) -> str:
    tokens: list[str] = []
    for part in parts:
        cleaned = _clean(part)
        if cleaned:
            tokens.append(cleaned)
    if not tokens:
        return "unknown_semantic_signature"
    return "|".join(sorted(dict.fromkeys(tokens)))


def _v553_comparable_temporal_key(
    source: str,
    country_code: str,
    relation_axis: str,
    target_entity: str,
    driver_facet: str,
    structural_channel: str,
    horizon_constraint: str,
    canonical_semantic_signature: str,
    *,
    structural_dimension_status: str,
    ready_for_temporal_field: bool,
) -> tuple[str, str, str]:
    source = _required_source(source)
    country_code = _required_country(country_code)
    relation_axis = _clean(relation_axis)
    target_entity = _clean(target_entity)
    driver_facet = _clean(driver_facet)
    structural_channel = _clean(structural_channel)
    horizon_constraint = _clean(horizon_constraint)
    canonical_semantic_signature = _clean(canonical_semantic_signature) or "unknown_semantic_signature"
    if structural_dimension_status == "resolved" and relation_axis and target_entity and driver_facet and not ready_for_temporal_field:
        grain = "relation_target_driver"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
        }
    elif structural_dimension_status == "resolved" and relation_axis and target_entity and driver_facet and structural_channel:
        grain = "structural_channel_exact"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
            "structural_channel_id": structural_channel,
            "canonical_semantic_signature": canonical_semantic_signature,
        }
    elif structural_dimension_status == "resolved" and relation_axis and target_entity and driver_facet and horizon_constraint:
        grain = "horizon_exact"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
            "horizon_constraint_id": horizon_constraint,
            "canonical_semantic_signature": canonical_semantic_signature,
        }
    elif structural_dimension_status == "resolved" and relation_axis and target_entity and driver_facet and canonical_semantic_signature != "unknown_semantic_signature":
        grain = "relation_target_driver_semantic"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
            "canonical_semantic_signature": canonical_semantic_signature,
        }
    elif structural_dimension_status == "resolved" and relation_axis and target_entity and driver_facet:
        grain = "relation_target_driver"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
        }
    else:
        grain = "lower_grain_probe"
        basis = {
            "source": source,
            "country_code": country_code,
            "relation_axis_id": relation_axis,
            "target_entity_id": target_entity,
            "driver_facet_id": driver_facet,
            "structural_channel_id": structural_channel,
            "horizon_constraint_id": horizon_constraint,
            "canonical_semantic_signature": canonical_semantic_signature,
        }
    payload = json.dumps(basis, sort_keys=True, ensure_ascii=False)
    key = f"v553ck_{hashlib.sha1((grain + '|' + payload).encode('utf-8')).hexdigest()[:12]}"
    if not ready_for_temporal_field and grain == "lower_grain_probe":
        key = f"probe::{key}"
    return key, grain, payload


def _shared_structural_axis_fields(report: dict[str, Any]) -> dict[str, str]:
    semantic_signature = _canonical_semantic_signature(
        *(report.get("shared_semantic_columns", []) or []),
        *(report.get("shared_directionality_columns", []) or []),
        *(report.get("shared_position_columns", []) or []),
    )
    return {
        "semantic_signature": semantic_signature,
        "canonical_semantic_signature": semantic_signature,
        "relation_axis_id": f"shared_relation_axis::{semantic_signature}",
        "target_entity_id": f"shared_target_entity::{semantic_signature}",
        "driver_facet_id": f"shared_driver_facet::{semantic_signature}",
        "structural_channel_id": f"shared_structural_channel::{semantic_signature}",
        "horizon_constraint_id": f"shared_horizon_constraint::{semantic_signature}",
    }


def _v553_temporal_key_profile(row: pd.Series) -> dict[str, Any]:
    source = _required_source(row.get("source"))
    country_code = _required_country(row.get("country_code"))
    relation_axis_id = _clean(row.get("relation_axis_id"))
    target_entity_id = _clean(row.get("target_entity_id"))
    driver_facet_id = _clean(row.get("driver_facet_id"))
    structural_channel_id = _clean(row.get("structural_channel_id"))
    horizon_constraint_id = _clean(row.get("horizon_constraint_id"))
    semantic_signature = _clean(row.get("semantic_signature"))
    canonical_semantic_signature = _canonical_semantic_signature(
        relation_axis_id,
        target_entity_id,
        driver_facet_id,
        structural_channel_id,
        horizon_constraint_id,
        semantic_signature,
    )
    structural_dimension_status = _clean(row.get("structural_dimension_status")) or "missing"
    source_v552_structural_fact_id = _clean(row.get("source_v552_structural_fact_id"))
    source_v552_temporal_key_source_ids = _parse_json_array(row.get("source_v552_temporal_key_source_ids_json"))
    source_v552_temporal_key_source_id = _first_or_unknown(
        source_v552_temporal_key_source_ids,
        _clean(row.get("source_v552_temporal_key_source_id")) or "",
    )
    source_v552_structural_fact_lane = _clean(row.get("source_v552_structural_fact_lane")) or _clean(row.get("structural_fact_lane")) or "not_temporal_key_source"
    source_v552_structural_fact_grain = _clean(row.get("source_v552_structural_fact_grain")) or _clean(row.get("structural_fact_grain")) or "not_temporal_key_source"
    fallback_permission_profile_key = _clean(row.get("fallback_permission_profile_key"))
    read_permission = _clean(row.get("read_permission")) or "unknown_permission"
    packet_class = _clean(row.get("packet_class")) or "unknown_packet_class"
    structural_fact_ids = _parse_json_array(row.get("source_v552_structural_fact_ids_json"))
    structural_fact_id = _clean(row.get("source_v552_structural_fact_id")) or (structural_fact_ids[0] if structural_fact_ids else "")
    temporal_key_basis = {
        "source": source,
        "country_code": country_code,
        "relation_axis_id": relation_axis_id,
        "target_entity_id": target_entity_id,
        "driver_facet_id": driver_facet_id,
        "structural_channel_id": structural_channel_id,
        "horizon_constraint_id": horizon_constraint_id,
        "semantic_signature": semantic_signature,
        "source_v552_structural_fact_id": source_v552_structural_fact_id,
        "source_v552_temporal_key_source_id": source_v552_temporal_key_source_id,
        "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(
            source_v552_temporal_key_source_ids or ([source_v552_temporal_key_source_id] if source_v552_temporal_key_source_id else [])
        ),
        "structural_dimension_status": structural_dimension_status,
        "source_v552_structural_fact_lane": source_v552_structural_fact_lane,
        "source_v552_structural_fact_grain": source_v552_structural_fact_grain,
        "packet_class": packet_class,
        "read_permission": read_permission,
        "fallback_permission_profile_key": fallback_permission_profile_key,
        "comparability_status": _clean(row.get("comparability_status")) or "not_supplied",
        "must_temporalize": bool(row.get("must_temporalize", False)),
        "single_wave_probe_allowed": bool(row.get("single_wave_probe_allowed", False)),
        "temporal_field_allowed": bool(row.get("temporal_field_allowed", False)),
        "temporal_anchor_required": bool(row.get("temporal_anchor_required", False)),
        "comparability_required": bool(row.get("comparability_required", False)),
        "blocking_reason": _clean(row.get("blocking_reason")) or "",
        "ready_for_v553": bool(row.get("ready_for_v553", False)),
        "ready_for_runtime_consumption": bool(row.get("ready_for_runtime_consumption", False)),
    }
    has_structural_channel_key = bool(relation_axis_id and target_entity_id and driver_facet_id and structural_channel_id)
    has_horizon_key = bool(relation_axis_id and target_entity_id and driver_facet_id and horizon_constraint_id)
    has_probe_structural_key = bool(relation_axis_id and target_entity_id and driver_facet_id)
    ready_for_temporal_field = bool(row.get("temporal_field_allowed", False))
    ready_for_probe = bool(row.get("single_wave_probe_allowed", False) or row.get("ready_for_v553", False))
    if structural_dimension_status == "resolved" and has_structural_channel_key:
        temporal_pressure_key = _stable_temporal_pressure_key(
            source,
            country_code,
            relation_axis_id,
            target_entity_id,
            driver_facet_id,
            structural_channel_id,
            semantic_signature,
            key_grain="structural_channel",
        )
        key_authority_status = "authorized_temporal_key" if ready_for_temporal_field else "probe_temporal_key"
        candidate_status = "resolved_temporal_key" if ready_for_temporal_field else "probe_temporal_key"
        blocker_class = "" if ready_for_temporal_field else "comparability_pending"
        blocked_reason = "" if ready_for_temporal_field else (_clean(row.get("blocking_reason")) or _clean(row.get("temporal_key_blocker_reason")) or "comparability_not_yet_established")
        comparability_class = "comparable" if ready_for_temporal_field else "reviewable"
    elif structural_dimension_status == "resolved" and has_horizon_key:
        temporal_pressure_key = _stable_temporal_pressure_key(
            source,
            country_code,
            relation_axis_id,
            target_entity_id,
            driver_facet_id,
            horizon_constraint_id,
            semantic_signature,
            key_grain="horizon_constraint",
        )
        key_authority_status = "authorized_temporal_key" if ready_for_temporal_field else "probe_temporal_key"
        candidate_status = "resolved_temporal_key" if ready_for_temporal_field else "probe_temporal_key"
        blocker_class = "" if ready_for_temporal_field else "comparability_pending"
        blocked_reason = "" if ready_for_temporal_field else (_clean(row.get("blocking_reason")) or _clean(row.get("temporal_key_blocker_reason")) or "comparability_not_yet_established")
        comparability_class = "comparable" if ready_for_temporal_field else "reviewable"
    elif structural_dimension_status == "resolved" and has_probe_structural_key:
        temporal_pressure_key = _stable_temporal_pressure_key(
            source,
            country_code,
            relation_axis_id,
            target_entity_id,
            driver_facet_id,
            structural_channel_id or horizon_constraint_id,
            semantic_signature,
            key_grain="probe_structural",
        )
        key_authority_status = "probe_temporal_key"
        candidate_status = "probe_only"
        blocker_class = "comparability_missing"
        blocked_reason = _clean(row.get("blocking_reason")) or _clean(row.get("temporal_key_blocker_reason")) or "comparability_not_yet_established"
        comparability_class = "reviewable"
    else:
        permission_profile = fallback_permission_profile_key or f"{source}::{country_code}::{read_permission}::{packet_class}"
        temporal_pressure_key = f"fallback::{permission_profile}"
        key_authority_status = "probe_temporal_key"
        candidate_status = "fallback_probe_only"
        blocker_class = "fallback_permission_profile"
        blocked_reason = _clean(row.get("temporal_key_blocker_reason")) or _clean(row.get("structural_dimension_blocker_reason")) or "fallback_permission_profile_only"
        comparability_class = "reviewable"
    comparable_temporal_key, comparable_key_grain, comparable_key_basis_json = _v553_comparable_temporal_key(
        source,
        country_code,
        relation_axis_id,
        target_entity_id,
        driver_facet_id,
        structural_channel_id,
        horizon_constraint_id,
        canonical_semantic_signature,
        structural_dimension_status=structural_dimension_status,
        ready_for_temporal_field=ready_for_temporal_field,
    )
    basis_json = json.dumps(temporal_key_basis, sort_keys=True, ensure_ascii=False)
    basis_hash = hashlib.sha1(basis_json.encode("utf-8")).hexdigest()[:12]
    return {
        "temporal_pressure_key": temporal_pressure_key,
        "key_basis_json": basis_json,
        "basis_hash": basis_hash,
        "canonical_semantic_signature": canonical_semantic_signature,
        "comparable_temporal_key": comparable_temporal_key,
        "comparable_key_grain": comparable_key_grain,
        "comparable_key_basis_json": comparable_key_basis_json,
        "relation_axis": relation_axis_id,
        "target_entity": target_entity_id,
        "driver_facet": driver_facet_id,
        "structural_channel": structural_channel_id,
        "horizon_constraint": horizon_constraint_id,
        "semantic_signature": semantic_signature,
        "key_authority_status": key_authority_status,
        "candidate_status": candidate_status,
        "blocker_class": blocker_class,
        "blocked_reason": blocked_reason,
        "comparability_class": comparability_class,
        "comparability_status": _clean(row.get("comparability_status")) or "not_supplied",
        "structural_dimension_status": structural_dimension_status,
        "source_v552_structural_fact_lane": source_v552_structural_fact_lane,
        "source_v552_structural_fact_grain": source_v552_structural_fact_grain,
        "fallback_permission_profile_key": fallback_permission_profile_key or f"{source}::{country_code}::{read_permission}::{packet_class}",
        "source_v552_structural_fact_id": structural_fact_id,
        "source_v552_structural_fact_ids_json": _json_singleton_array(structural_fact_id),
        "source_v552_structural_fact_ids_diagnostic_json": _json_array(structural_fact_ids or ([structural_fact_id] if structural_fact_id else [])),
        "source_v552_temporal_key_source_id": source_v552_temporal_key_source_id,
        "source_v552_temporal_key_source_ids_json": _json_singleton_array(source_v552_temporal_key_source_id),
        "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(
            source_v552_temporal_key_source_ids or ([source_v552_temporal_key_source_id] if source_v552_temporal_key_source_id else [])
        ),
    }


def _v553_temporal_key_row(row: pd.Series) -> dict[str, Any]:
    profile = _v553_temporal_key_profile(row)
    packet_ids = sorted(
        {value for value in [_clean(row.get("v552j_packet_id")), _clean(row.get("packet_id"))] if value}
    )
    input_ids = sorted(
        {value for value in [_clean(row.get("v553_input_id"))] if value}
    )
    profile.update(
        {
            "source_v552j_packet_ids_json": json.dumps(packet_ids, sort_keys=True),
            "source_v552j_input_ids_json": json.dumps(input_ids, sort_keys=True),
        }
    )
    return profile


def _first_or_unknown(values: Any, fallback: str) -> str:
    if isinstance(values, list):
        for value in values:
            cleaned = _clean(value)
            if cleaned:
                return cleaned
    cleaned = _clean(values)
    return cleaned or fallback


def _merge_nonempty_resolution(row: pd.Series | dict[str, Any], resolution: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]:
    merged = dict(row.to_dict() if isinstance(row, pd.Series) else row)
    preserved_fields: list[str] = []
    filled_fields: list[str] = []
    for key, value in resolution.items():
        current = merged.get(key, "")
        if _clean(current):
            preserved_fields.append(key)
            continue
        if _clean(value):
            merged[key] = value
            filled_fields.append(key)
        elif key not in merged:
            merged[key] = value
    return merged, preserved_fields, filled_fields


def _build_v553_wave_anchor_index(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in report.get("wave_rows", []) or []:
        if not isinstance(item, dict):
            continue
        wave = _clean(item.get("wave"))
        if not wave:
            continue
        v552j_context = _wave_v552j_context(item)
        year = _int(item.get("temporal_year"), 0)
        source_family = _clean(item.get("source")) or _report_source(report)
        country_code = _report_country(report)
        anchor_status = "anchor_derived" if _clean(item.get("wave_status")) == "complete" and not item.get("missing_authority_kinds") else "cautious_interpolation_allowed"
        anchor_authority = _clean(item.get("v552j_handoff_authority_status")) or _clean(item.get("v552j_readiness_status")) or "unknown"
        anchor_confidence = _bounded_score(1.0 if anchor_status == "anchor_derived" else 0.65)
        v552j_run_id = _run_id_from_path(v552j_context.get("resolved_root") or item.get("latest_v552j_root") or item.get("run_root"))
        rows.append(
            {
                "run_id": run_id,
                "source_family": source_family,
                "source": source_family,
                "country_code": country_code,
                "wave": wave,
                "canonical_wave": _clean(item.get("canonical_wave")) or wave,
                "wave_year": year,
                "anchor_status": anchor_status,
                "anchor_authority": anchor_authority,
                "anchor_confidence": anchor_confidence,
                "v552j_run_id": v552j_run_id,
                "v552j_readiness_status": _clean(item.get("v552j_readiness_status")) or _clean(item.get("v552j_handoff_authority_status")) or "unknown",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_WAVE_ANCHOR_INDEX_SCHEMA["required_columns"])


def _build_v553_harmonization_difference_ledger(report: dict[str, Any], run_id: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in report.get("wave_differences", []) or []:
        if not isinstance(item, dict):
            continue
        rows.append(
            {
                "run_id": run_id,
                "prior_wave": _clean(item.get("prior_wave")) or "",
                "current_wave": _clean(item.get("current_wave")) or "",
                "source": _clean(item.get("source")) or _report_source(report),
                "prior_canonical_wave": _clean(item.get("prior_canonical_wave")) or "",
                "current_canonical_wave": _clean(item.get("current_canonical_wave")) or "",
                "prior_wave_status": _clean(item.get("prior_wave_status")) or "",
                "current_wave_status": _clean(item.get("current_wave_status")) or "",
                "shared_semantic_columns_json": _clean(item.get("shared_semantic_columns_json")) or "[]",
                "shared_directionality_columns_json": _clean(item.get("shared_directionality_columns_json")) or "[]",
                "shared_position_columns_json": _clean(item.get("shared_position_columns_json")) or "[]",
                "shared_relation_axis_ids_json": _clean(item.get("shared_relation_axis_ids_json")) or "[]",
                "shared_target_entity_ids_json": _clean(item.get("shared_target_entity_ids_json")) or "[]",
                "shared_driver_facet_ids_json": _clean(item.get("shared_driver_facet_ids_json")) or "[]",
                "shared_structural_channel_ids_json": _clean(item.get("shared_structural_channel_ids_json")) or "[]",
                "shared_horizon_constraint_ids_json": _clean(item.get("shared_horizon_constraint_ids_json")) or "[]",
                "shared_semantic_column_count": _int(item.get("shared_semantic_column_count"), 0),
                "shared_directionality_column_count": _int(item.get("shared_directionality_column_count"), 0),
                "shared_position_column_count": _int(item.get("shared_position_column_count"), 0),
                "shared_relation_axis_id_count": _int(item.get("shared_relation_axis_id_count"), 0),
                "shared_target_entity_id_count": _int(item.get("shared_target_entity_id_count"), 0),
                "shared_driver_facet_id_count": _int(item.get("shared_driver_facet_id_count"), 0),
                "shared_structural_channel_id_count": _int(item.get("shared_structural_channel_id_count"), 0),
                "shared_horizon_constraint_id_count": _int(item.get("shared_horizon_constraint_id_count"), 0),
                "pair_missing_authority_count": _int(item.get("pair_missing_authority_count"), 0),
                "pair_harmonization_status": _clean(item.get("pair_harmonization_status")) or "partial",
                "pair_harmonization_score": float(item.get("pair_harmonization_score", 0.0) or 0.0),
                "difference_kind": _clean(item.get("difference_kind")) or "shared_temporal_authority_surface",
                "difference_reason": _clean(item.get("difference_reason")) or "wave-specific authority and structural id inventory",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA["required_columns"])


def _build_v553_pressure_basis_ledger(country_year_pressure_df: pd.DataFrame, report: dict[str, Any], run_id: str) -> pd.DataFrame:
    if country_year_pressure_df.empty:
        return pd.DataFrame(columns=V553_PRESSURE_BASIS_LEDGER_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for _, row in country_year_pressure_df.iterrows():
        basis_json = {}
        try:
            basis_json = json.loads(str(row.get("basis_json", "") or "{}"))
        except Exception:
            basis_json = {}
        rows.append(
            {
                "run_id": run_id,
                "temporal_pressure_key": f"{_clean(row.get('country_code')) or _report_country(report)}::{_int(row.get('year'), 0)}",
                "country": _clean(row.get("country_code")) or _report_country(report),
                "wave_id": str(_int(row.get("year"), 0)),
                "survey_year": _int(row.get("year"), 0),
                "pressure_basis": _clean(row.get("pressure_status")) or "probe_only",
                "pressure_basis_source": _clean(row.get("interpolation_method")) or "wave_harmonization_report",
                "pressure_basis_summary_json": json.dumps(
                    {
                        "basis_json": basis_json,
                        "pressure_value_distribution": row.get("pressure_value_distribution", ""),
                        "pressure_intensity_band": _clean(row.get("pressure_intensity_band")) or "",
                        "confidence_penalty": float(row.get("confidence_penalty", 0.0) or 0.0),
                    },
                    sort_keys=True,
                ),
                "basis_relation_axis_id": _clean(row.get("relation_axis_id")) or "",
                "basis_target_entity_id": _clean(row.get("target_entity_id")) or "",
                "basis_driver_facet_id": _clean(row.get("driver_facet_id")) or "",
                "basis_structural_channel_id": _clean(row.get("structural_channel_id")) or "",
                "basis_horizon_constraint_id": _clean(row.get("horizon_constraint_id")) or "",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_PRESSURE_BASIS_LEDGER_SCHEMA["required_columns"])


def _build_v553_confidence_penalty_ledger(country_year_pressure_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if country_year_pressure_df.empty:
        return pd.DataFrame(columns=V553_CONFIDENCE_PENALTY_LEDGER_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for _, row in country_year_pressure_df.iterrows():
        basis_json = {}
        try:
            basis_json = json.loads(str(row.get("basis_json", "") or "{}"))
        except Exception:
            basis_json = {}
        rows.append(
            {
                "run_id": run_id,
                "temporal_pressure_key": f"{_required_country(row.get('country_code'))}::{_int(row.get('year'), 0)}",
                "country": _required_country(row.get("country_code")),
                "wave_id": str(_int(row.get("year"), 0)),
                "survey_year": _int(row.get("year"), 0),
                "confidence_penalty": float(row.get("confidence_penalty", 0.0) or 0.0),
                "confidence_penalty_reason": _clean(row.get("pressure_status")) or "probe_only",
                "confidence_penalty_basis_json": json.dumps(
                    {
                        "basis_json": basis_json,
                        "pressure_value_distribution": row.get("pressure_value_distribution", ""),
                        "pressure_intensity_band": _clean(row.get("pressure_intensity_band")) or "",
                        "pressure_status": _clean(row.get("pressure_status")) or "",
                    },
                    sort_keys=True,
                ),
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_CONFIDENCE_PENALTY_LEDGER_SCHEMA["required_columns"])


def _build_v553_temporal_key_tables(report: dict[str, Any], run_id: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    wave_rows = [row for row in (report.get("wave_rows", []) or []) if isinstance(row, dict)]
    key_wave_rows: list[dict[str, Any]] = []
    blocker_rows: list[dict[str, Any]] = []
    resolution_audit_rows: list[dict[str, Any]] = []
    for item in wave_rows:
        wave = _clean(item.get("wave"))
        if not wave:
            continue
        v552j_context = _wave_v552j_context(item)
        input_df = v552j_context.get("input_df", pd.DataFrame())
        handoff_df = v552j_context.get("handoff_df", pd.DataFrame())
        primary_df = handoff_df.copy()
        resolved_root_text = _clean(v552j_context.get("resolved_root"))
        v552_structural_fact_index = pd.DataFrame()
        v552_temporal_key_source_index = pd.DataFrame()
        fact_index_path = _resolve_repo_path(v552j_context.get("v552_structural_fact_index_path"))
        key_source_index_path = _resolve_repo_path(v552j_context.get("v552_temporal_key_source_index_path"))
        if fact_index_path and fact_index_path.exists():
            v552_structural_fact_index = _load_optional(fact_index_path)
        if key_source_index_path and key_source_index_path.exists():
            v552_temporal_key_source_index = _load_optional(key_source_index_path)
        if (v552_structural_fact_index.empty or v552_temporal_key_source_index.empty) and resolved_root_text:
            fallback_root = Path(resolved_root_text)
            if v552_structural_fact_index.empty:
                fallback_fact_index_path = fallback_root / "packets" / "v552_structural_fact_index.parquet"
                if fallback_fact_index_path.exists():
                    v552_structural_fact_index = _load_optional(fallback_fact_index_path)
            if v552_temporal_key_source_index.empty:
                fallback_key_source_index_path = fallback_root / "packets" / "v552_temporal_key_source_index.parquet"
                if fallback_key_source_index_path.exists():
                    v552_temporal_key_source_index = _load_optional(fallback_key_source_index_path)
        probe_rows_present = bool(not input_df.empty)
        if handoff_df.empty and probe_rows_present:
            raise RuntimeError("V553_EMPTY_HANDOFF_WITH_STRUCTURAL_INPUT_ROWS")
        if primary_df.empty:
            fallback_permission_profile_key = f"fallback::{_report_source(report)}::{_report_country(report)}::unknown_permission_profile"
            key_wave_rows.append(
                {
                    "run_id": run_id,
                    "wave_id": wave,
                    "temporal_pressure_key": fallback_permission_profile_key,
                    "country": _report_country(report),
                    "source_v552_structural_fact_id": "",
                    "source_v552_structural_fact_ids_json": "[]",
                    "source_v552_structural_fact_ids_diagnostic_json": "[]",
                    "source_v552_temporal_key_source_id": "",
                    "source_v552_temporal_key_source_ids_json": "[]",
                    "source_v552_temporal_key_source_ids_diagnostic_json": "[]",
                    "source_v552_structural_fact_lane": "not_temporal_key_source",
                    "source_v552_structural_fact_grain": "not_temporal_key_source",
                    "relation_axis": "",
                    "target_entity": "",
                    "driver_facet": "",
                    "structural_channel": "",
                    "horizon_constraint": "",
                    "semantic_signature": "",
                    "canonical_semantic_signature": "",
                    "comparable_temporal_key": f"probe::{fallback_permission_profile_key}",
                    "comparable_key_grain": "lower_grain_probe",
                    "comparable_key_basis_json": json.dumps({"fallback": True, "wave": wave, "country_code": _report_country(report)}, sort_keys=True),
                    "key_basis_json": json.dumps({"fallback": True, "wave": wave, "country_code": _report_country(report)}, sort_keys=True),
                    "candidate_status": "fallback_probe_only",
                    "key_authority_status": "probe_temporal_key",
                    "structural_dimension_status": "missing",
                    "fallback_permission_profile_key": fallback_permission_profile_key,
                    "candidate_count": 0,
                    "resolution_grain": "fallback",
                    "ready_for_v553_input_count": 0,
                    "probe_ready_input_count": 0,
                    "packet_ready_input_count": 0,
                    "probe_only_input_count": 0,
                    "ready_for_runtime_consumption_input_count": 0,
                    "blocked_input_count": 0,
                    "temporal_allowed_input_count": 0,
                    "temporal_blocked_input_count": 0,
                    "readiness_score": 0.0,
                    "support_score": 0.0,
                    "directionality_score": 0.0,
                    "authority_score": 0.0,
                    "comparability_score": 0.0,
                    "confidence_score": 0.0,
                    "pressure_value": 0.0,
                    "pressure_value_kind": "probe_only",
                    "probe_pressure_value": 0.0,
                    "structural_pressure_value": None,
                    "authorized_structural_pressure_value": None,
                    "probe_structural_score": 0.0,
                    "source_v552j_packet_ids_json": "[]",
                    "source_v552j_input_ids_json": "[]",
                    "source_wave_ids_json": json.dumps([wave], sort_keys=True),
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
            continue
        structural_resolution_rows: list[dict[str, Any]] = []
        resolution_rows_for_audit: list[dict[str, Any]] = []
        for _, input_row in primary_df.reset_index(drop=True).iterrows():
            structural_resolution = _packet_structural_dimension_resolution(input_row, v552_structural_fact_index, v552_temporal_key_source_index)
            row_dict, preserved_fields, filled_fields = _merge_nonempty_resolution(input_row, structural_resolution)
            row_source = _clean(row_dict.get("source")) or _clean(item.get("source"))
            if not canonical_family_key(row_source):
                row_source = _report_source(report)
            row_country = _clean(row_dict.get("country_code")) or _clean(row_dict.get("country")) or _clean(item.get("country_code"))
            if not canonical_country_code(row_country):
                row_country = _report_country(report)
            row_dict["source"] = row_source
            row_source_family = _clean(row_dict.get("source_family"))
            row_dict["source_family"] = row_source_family if canonical_family_key(row_source_family) else row_dict["source"]
            row_dict["country_code"] = row_country
            row_country_label = _clean(row_dict.get("country"))
            row_dict["country"] = row_country_label if canonical_country_code(row_country_label) else row_dict["country_code"]
            temporal_key_blocker_reason = _clean(row_dict.get("temporal_key_blocker_reason")) or _clean(structural_resolution.get("temporal_key_blocker_reason")) or ""
            resolution_grain = "fallback"
            if _clean(row_dict.get("structural_dimension_status")) == "resolved":
                if _clean(row_dict.get("structural_channel_id")):
                    resolution_grain = "structural_channel"
                elif _clean(row_dict.get("horizon_constraint_id")):
                    resolution_grain = "horizon_constraint"
                elif _clean(row_dict.get("relation_axis_id")) and _clean(row_dict.get("target_entity_id")) and _clean(row_dict.get("driver_facet_id")):
                    resolution_grain = "probe_structural"
                else:
                    resolution_grain = "resolved_unknown_grain"
            row_dict["resolution_grain"] = resolution_grain
            row_dict["preserved_nonempty_fields_json"] = _json_array(preserved_fields)
            row_dict["filled_nonempty_fields_json"] = _json_array(filled_fields)
            row_dict["temporal_key_blocker_reason"] = temporal_key_blocker_reason
            structural_resolution_rows.append(row_dict)
            resolution_rows_for_audit.append(
                {
                    "run_id": run_id,
                    "wave_id": wave,
                    "v552j_packet_id": _clean(input_row.get("v552j_packet_id")) or _clean(input_row.get("packet_id")) or "",
                    "v553_input_id": _clean(input_row.get("v553_input_id")) or "",
                    "source_v552_structural_fact_id": _clean(row_dict.get("source_v552_structural_fact_id")) or "",
                    "source_v552_structural_fact_ids_json": _clean(row_dict.get("source_v552_structural_fact_ids_json")) or "[]",
                    "source_v552_structural_fact_ids_diagnostic_json": _clean(row_dict.get("source_v552_structural_fact_ids_diagnostic_json")) or "[]",
                    "source_v552_temporal_key_source_id": _clean(row_dict.get("source_v552_temporal_key_source_id")) or "",
                    "source_v552_temporal_key_source_ids_json": _clean(row_dict.get("source_v552_temporal_key_source_ids_json")) or "[]",
                    "source_v552_temporal_key_source_ids_diagnostic_json": _clean(row_dict.get("source_v552_temporal_key_source_ids_diagnostic_json")) or "[]",
                    "source_v552_structural_fact_lane": _clean(row_dict.get("source_v552_structural_fact_lane")) or _clean(row_dict.get("structural_fact_lane")) or "not_temporal_key_source",
                    "source_v552_structural_fact_grain": _clean(row_dict.get("source_v552_structural_fact_grain")) or _clean(row_dict.get("structural_fact_grain")) or "not_temporal_key_source",
                    "relation_axis_id": _clean(row_dict.get("relation_axis_id")) or "",
                    "target_entity_id": _clean(row_dict.get("target_entity_id")) or "",
                    "driver_facet_id": _clean(row_dict.get("driver_facet_id")) or "",
                    "structural_channel_id": _clean(row_dict.get("structural_channel_id")) or "",
                    "horizon_constraint_id": _clean(row_dict.get("horizon_constraint_id")) or "",
                    "semantic_signature": _clean(row_dict.get("semantic_signature")) or "",
                    "canonical_semantic_signature": _clean(row_dict.get("canonical_semantic_signature")) or _clean(row_dict.get("semantic_signature")) or "",
                    "comparable_temporal_key": _clean(row_dict.get("comparable_temporal_key")) or _clean(row_dict.get("temporal_pressure_key")) or "",
                    "comparable_key_grain": _clean(row_dict.get("comparable_key_grain")) or "",
                    "comparable_key_basis_json": _clean(row_dict.get("comparable_key_basis_json")) or "{}",
                    "structural_dimension_status": _clean(row_dict.get("structural_dimension_status")) or "missing",
                    "resolution_grain": resolution_grain,
                    "temporal_key_candidate_status": _clean(row_dict.get("temporal_key_candidate_status")) or "blocked",
                    "key_authority_status": _clean(row_dict.get("key_authority_status")) or "blocked_temporal_key",
                    "preserved_nonempty_fields_json": _json_array(preserved_fields),
                    "filled_nonempty_fields_json": _json_array(filled_fields),
                    "blocked_reason": temporal_key_blocker_reason,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
        resolution_audit_rows.extend(resolution_rows_for_audit)
        enriched = pd.DataFrame(structural_resolution_rows).reset_index(drop=True)
        profile_df = enriched.apply(_v553_temporal_key_row, axis=1, result_type="expand")
        profile_df = profile_df[[column for column in profile_df.columns if column not in enriched.columns]]
        enriched = pd.concat([enriched, profile_df], axis=1)
        group_key_column = "comparable_temporal_key" if "comparable_temporal_key" in enriched.columns else "temporal_pressure_key"
        for temporal_pressure_key, group in enriched.groupby(group_key_column, dropna=False):
            if not _clean(temporal_pressure_key):
                continue
            resolved_group = group[
                group.get("structural_dimension_status", pd.Series(dtype=str)).astype(str).eq("resolved")
                & group.get("temporal_key_candidate_status", pd.Series(dtype=str)).astype(str).isin({"resolved_temporal_key", "probe_temporal_key", "probe_only"})
            ].copy()
            packet_ids = sorted({_clean(value) for value in group.get("v552j_packet_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            input_ids = sorted({_clean(value) for value in group.get("v553_input_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            probe_ready_flags = group.apply(
                lambda row: bool(
                    row.get("ready_for_v553_probe", False)
                    or row.get("single_wave_probe_allowed", False)
                    or row.get("ready_for_v553", False)
                ),
                axis=1,
            )
            packet_ready_flags = group.apply(
                lambda row: bool(
                    row.get("packet_ready_for_v553", False)
                    or row.get("ready_for_v553", False)
                ),
                axis=1,
            )
            ready_count = int(group.get("ready_for_v553", pd.Series(dtype=bool)).astype(bool).sum()) if "ready_for_v553" in group.columns else 0
            probe_ready_count = int(probe_ready_flags.sum())
            packet_ready_count = int(packet_ready_flags.sum())
            probe_only_count = probe_ready_count
            runtime_count = int(group.get("ready_for_runtime_consumption", pd.Series(dtype=bool)).astype(bool).sum()) if "ready_for_runtime_consumption" in group.columns else 0
            blocked_count = int((~group.get("ready_for_v553", pd.Series(dtype=bool)).astype(bool)).sum()) if "ready_for_v553" in group.columns else 0
            temporal_allowed_count = int(group.get("ready_for_v553_temporal_field", pd.Series(dtype=bool)).astype(bool).sum()) if "ready_for_v553_temporal_field" in group.columns else 0
            temporal_blocked_count = max(0, int(len(group)) - temporal_allowed_count)
            readiness_series = group.get("readiness_score", pd.Series(dtype=float)).astype(float) if "readiness_score" in group.columns else pd.Series(dtype=float)
            support_series = group.get("support_score", pd.Series(dtype=float)).astype(float) if "support_score" in group.columns else pd.Series(dtype=float)
            directionality_series = group.get("directionality_score", pd.Series(dtype=float)).astype(float) if "directionality_score" in group.columns else pd.Series(dtype=float)
            authority_series = group.get("authority_score", pd.Series(dtype=float)).astype(float) if "authority_score" in group.columns else pd.Series(dtype=float)
            comparability_series = group.get("comparability_score", pd.Series(dtype=float)).astype(float) if "comparability_score" in group.columns else pd.Series(dtype=float)
            confidence_series = group.get("confidence_score", pd.Series(dtype=float)).astype(float) if "confidence_score" in group.columns else pd.Series(dtype=float)
            profile = group.iloc[0].to_dict()
            source_v552_structural_fact_ids = sorted({_clean(value) for value in group.get("source_v552_structural_fact_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            source_v552_temporal_key_source_ids = sorted({_clean(value) for value in group.get("source_v552_temporal_key_source_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            source_v552_temporal_key_source_id = _first_or_unknown(
                source_v552_temporal_key_source_ids,
                _clean(profile.get("source_v552_temporal_key_source_id")) or "",
            )
            structural_dimension_status = _clean(profile.get("structural_dimension_status")) or "missing"
            fallback_permission_profile_key = _clean(profile.get("fallback_permission_profile_key")) or ""
            structural_fact_lane = _clean(profile.get("source_v552_structural_fact_lane")) or _clean(profile.get("structural_fact_lane")) or "not_temporal_key_source"
            structural_fact_grain = _clean(profile.get("source_v552_structural_fact_grain")) or _clean(profile.get("structural_fact_grain")) or "not_temporal_key_source"
            key_grain = _clean(profile.get("comparable_key_grain")) or _clean(profile.get("resolution_grain")) or ("structural_channel_exact" if _clean(profile.get("structural_channel")) else ("horizon_exact" if _clean(profile.get("horizon_constraint")) else "lower_grain_probe"))
            structural_pressure_value = None
            if not v552_structural_fact_index.empty and source_v552_structural_fact_ids:
                matching_fact_pressure = pd.to_numeric(
                    v552_structural_fact_index[
                        v552_structural_fact_index["v552_structural_fact_id"].astype(str).isin(source_v552_structural_fact_ids)
                    ].get("pressure_score", pd.Series(dtype=float)),
                    errors="coerce",
                ).dropna()
                if not matching_fact_pressure.empty:
                    structural_pressure_value = round(float(matching_fact_pressure.mean()), 6)
            probe_pressure_value = round(float(profile.get("readiness_score", 0.0) or 0.0), 6)
            pressure_value_kind = "structural_candidate" if structural_pressure_value is not None else "probe_only"
            authorized_structural_pressure_value = None
            probe_structural_score = probe_pressure_value
            pressure_value = structural_pressure_value if structural_pressure_value is not None else probe_structural_score
            if _is_audit_fact_lane(structural_fact_lane):
                blocker_rows.append(
                    {
                        "run_id": run_id,
                        "wave_id": wave,
                        "temporal_pressure_key": temporal_pressure_key,
                        "country": _clean(profile.get("country_code")) or _clean(item.get("country_code")) or _report_country(report),
                        "blocker_class": "diagnostic_only",
                        "blocker_reason": "audit_fact_diagnostic_only",
                        "blocking_reason_detail": "audit_fact rows are demoted out of core temporal key and observation lanes",
                        "packet_class": _clean(group.get("packet_class", pd.Series(dtype=str)).astype(str).mode().iloc[0]) if "packet_class" in group.columns and not group["packet_class"].dropna().empty else _clean(profile.get("packet_class")) or "",
                        "read_permission": _clean(group.get("read_permission", pd.Series(dtype=str)).astype(str).mode().iloc[0]) if "read_permission" in group.columns and not group["read_permission"].dropna().empty else _clean(profile.get("read_permission")) or "",
                        "comparability_status": _clean(group["comparability_status"].dropna().astype(str).mode().iloc[0]) if "comparability_status" in group.columns and not group["comparability_status"].dropna().empty else _clean(profile.get("comparability_status")) or "not_supplied",
                        "temporal_field_allowed": bool(temporal_allowed_count > 0),
                        "ready_for_v553": bool(ready_count > 0),
                        "source_v552_structural_fact_id": _clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else ""),
                        "source_v552_structural_fact_ids_json": _json_singleton_array(_clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else "")),
                        "source_v552_structural_fact_ids_diagnostic_json": _json_array(source_v552_structural_fact_ids),
                        "source_v552_temporal_key_source_id": source_v552_temporal_key_source_id,
                        "source_v552_temporal_key_source_ids_json": _json_singleton_array(source_v552_temporal_key_source_id),
                        "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(source_v552_temporal_key_source_ids),
                        "structural_fact_lane": structural_fact_lane,
                        "structural_fact_grain": structural_fact_grain,
                        "source_v552_structural_fact_lane": structural_fact_lane,
                        "source_v552_structural_fact_grain": structural_fact_grain,
                        "structural_dimension_status": structural_dimension_status,
                        "resolution_grain": key_grain,
                        "fallback_permission_profile_key": fallback_permission_profile_key,
                        "probe_pressure_value": probe_pressure_value,
                        "structural_pressure_value": None,
                        "source_v552j_packet_ids_json": json.dumps(packet_ids, sort_keys=True),
                        "source_v552j_input_ids_json": json.dumps(input_ids, sort_keys=True),
                        "created_at": utc_now(),
                        "schema_version": V553_SCHEMA_VERSION,
                        "compiler_version": V553_COMPILER_VERSION,
                    }
                )
                continue
            key_wave_rows.append(
                {
                    "run_id": run_id,
                    "wave_id": wave,
                    "temporal_pressure_key": temporal_pressure_key,
                    "country": _clean(profile.get("country_code")) or _clean(item.get("country_code")) or _report_country(report),
                    "source_v552_structural_fact_id": _clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else ""),
                    "source_v552_structural_fact_ids_json": _json_singleton_array(_clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else "")),
                    "source_v552_structural_fact_ids_diagnostic_json": _json_array(source_v552_structural_fact_ids),
                    "source_v552_temporal_key_source_id": _clean(profile.get("source_v552_temporal_key_source_id")) or (source_v552_temporal_key_source_ids[0] if source_v552_temporal_key_source_ids else ""),
                    "source_v552_temporal_key_source_ids_json": _json_singleton_array(_clean(profile.get("source_v552_temporal_key_source_id")) or (source_v552_temporal_key_source_ids[0] if source_v552_temporal_key_source_ids else "")),
                    "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(source_v552_temporal_key_source_ids),
                    "structural_fact_lane": structural_fact_lane,
                    "structural_fact_grain": structural_fact_grain,
                    "source_v552_structural_fact_lane": structural_fact_lane,
                    "source_v552_structural_fact_grain": structural_fact_grain,
                    "comparable_temporal_key": _clean(profile.get("comparable_temporal_key")) or _clean(temporal_pressure_key),
                    "comparable_key_grain": key_grain,
                    "comparable_key_basis_json": _clean(profile.get("comparable_key_basis_json")) or "{}",
                    "canonical_semantic_signature": _clean(profile.get("canonical_semantic_signature")) or _clean(profile.get("semantic_signature")) or "",
                    "relation_axis": profile.get("relation_axis", ""),
                    "target_entity": profile.get("target_entity", ""),
                    "driver_facet": profile.get("driver_facet", ""),
                    "structural_channel": profile.get("structural_channel", ""),
                    "horizon_constraint": profile.get("horizon_constraint", ""),
                    "semantic_signature": profile.get("semantic_signature", ""),
                    "key_basis_json": profile.get("key_basis_json", "{}"),
                    "candidate_status": profile.get("candidate_status", "blocked_candidate"),
                    "key_authority_status": profile.get("key_authority_status", "blocked_temporal_key"),
                    "structural_dimension_status": structural_dimension_status,
                    "fallback_permission_profile_key": fallback_permission_profile_key,
                    "resolution_grain": key_grain,
                    "candidate_count": int(len(group)),
                    "ready_for_v553_input_count": ready_count,
                    "probe_ready_input_count": probe_ready_count,
                    "packet_ready_input_count": packet_ready_count,
                    "probe_only_input_count": probe_only_count,
                    "ready_for_runtime_consumption_input_count": runtime_count,
                    "blocked_input_count": blocked_count,
                    "temporal_allowed_input_count": temporal_allowed_count,
                    "temporal_blocked_input_count": temporal_blocked_count,
                    "readiness_score": round(float(readiness_series.mean()) if not readiness_series.empty else 0.0, 6),
                    "support_score": round(float(support_series.mean()) if not support_series.empty else 0.0, 6),
                    "directionality_score": round(float(directionality_series.mean()) if not directionality_series.empty else 0.0, 6),
                    "authority_score": round(float(authority_series.mean()) if not authority_series.empty else 0.0, 6),
                    "comparability_score": round(float(comparability_series.mean()) if not comparability_series.empty else 0.0, 6),
                    "confidence_score": round(float(confidence_series.mean()) if not confidence_series.empty else 0.0, 6),
                    "pressure_value_kind": pressure_value_kind,
                    "pressure_value": pressure_value,
                    "source_v552j_packet_ids_json": json.dumps(packet_ids, sort_keys=True),
                    "source_v552j_input_ids_json": json.dumps(input_ids, sort_keys=True),
                    "source_wave_ids_json": json.dumps([wave], sort_keys=True),
                    "probe_pressure_value": probe_pressure_value,
                    "probe_structural_score": probe_structural_score,
                    "structural_pressure_value": structural_pressure_value,
                    "authorized_structural_pressure_value": authorized_structural_pressure_value,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
            if blocked_count > 0 or temporal_allowed_count == 0 or structural_dimension_status != "resolved":
                blocker_rows.append(
                    {
                        "run_id": run_id,
                        "wave_id": wave,
                        "temporal_pressure_key": temporal_pressure_key,
                        "country": _clean(profile.get("country_code")) or _clean(item.get("country_code")) or _report_country(report),
                        "blocker_class": profile.get("blocker_class", "probe_only"),
                        "blocker_reason": profile.get("blocked_reason", "probe_only_temporal_field_or_blocked_lanes"),
                        "blocking_reason_detail": _clean(group.get("blocking_reason", pd.Series(dtype=str)).astype(str).mode().iloc[0]) if "blocking_reason" in group.columns and not group["blocking_reason"].dropna().empty else _clean(profile.get("blocked_reason")) or "probe_only_temporal_field_or_blocked_lanes",
                        "packet_class": _clean(group.get("packet_class", pd.Series(dtype=str)).astype(str).mode().iloc[0]) if "packet_class" in group.columns and not group["packet_class"].dropna().empty else _clean(profile.get("packet_class")) or "",
                        "read_permission": _clean(group.get("read_permission", pd.Series(dtype=str)).astype(str).mode().iloc[0]) if "read_permission" in group.columns and not group["read_permission"].dropna().empty else _clean(profile.get("read_permission")) or "",
                        "comparability_status": _clean(group["comparability_status"].dropna().astype(str).mode().iloc[0]) if "comparability_status" in group.columns and not group["comparability_status"].dropna().empty else _clean(profile.get("comparability_status")) or "not_supplied",
                        "temporal_field_allowed": bool(temporal_allowed_count > 0),
                        "ready_for_v553": bool(ready_count > 0),
                        "source_v552_structural_fact_id": _clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else ""),
                        "source_v552_structural_fact_ids_json": _json_singleton_array(_clean(profile.get("source_v552_structural_fact_id")) or (source_v552_structural_fact_ids[0] if source_v552_structural_fact_ids else "")),
                        "source_v552_structural_fact_ids_diagnostic_json": _json_array(source_v552_structural_fact_ids),
                        "source_v552_temporal_key_source_id": source_v552_temporal_key_source_id,
                        "source_v552_temporal_key_source_ids_json": _json_singleton_array(source_v552_temporal_key_source_id),
                        "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(source_v552_temporal_key_source_ids),
                        "structural_fact_lane": structural_fact_lane,
                        "structural_fact_grain": structural_fact_grain,
                        "source_v552_structural_fact_lane": structural_fact_lane,
                        "source_v552_structural_fact_grain": structural_fact_grain,
                        "structural_dimension_status": structural_dimension_status,
                        "resolution_grain": key_grain,
                        "fallback_permission_profile_key": fallback_permission_profile_key,
                        "comparable_temporal_key": _clean(profile.get("comparable_temporal_key")) or _clean(temporal_pressure_key),
                        "comparable_key_grain": _clean(profile.get("comparable_key_grain")) or "",
                        "comparable_key_basis_json": _clean(profile.get("comparable_key_basis_json")) or "{}",
                        "probe_pressure_value": probe_pressure_value,
                        "structural_pressure_value": structural_pressure_value,
                        "source_v552j_packet_ids_json": json.dumps(packet_ids, sort_keys=True),
                        "source_v552j_input_ids_json": json.dumps(input_ids, sort_keys=True),
                        "created_at": utc_now(),
                        "schema_version": V553_SCHEMA_VERSION,
                        "compiler_version": V553_COMPILER_VERSION,
                    }
                )
    key_wave_df = pd.DataFrame(key_wave_rows, columns=V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA["required_columns"])
    blocker_df = pd.DataFrame(blocker_rows, columns=V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA["required_columns"])
    if key_wave_df.empty:
        key_index_df = pd.DataFrame(columns=V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA["required_columns"])
    else:
        grouped_rows: list[dict[str, Any]] = []
        group_key_column = "comparable_temporal_key" if "comparable_temporal_key" in key_wave_df.columns else "temporal_pressure_key"
        for temporal_pressure_key, group in key_wave_df.groupby(group_key_column, dropna=False):
            if not _clean(temporal_pressure_key):
                continue
            first = group.iloc[0].to_dict()
            wave_ids = sorted({_clean(value) for value in group.get("wave_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            structural_fact_ids = sorted({_clean(value) for value in group.get("source_v552_structural_fact_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            temporal_key_source_ids = sorted({_clean(value) for value in group.get("source_v552_temporal_key_source_id", pd.Series(dtype=str)).tolist() if _clean(value)})
            auth = _authorize_v553_multi_wave_key(report, group)
            structural_fact_lane = _clean(first.get("source_v552_structural_fact_lane")) or _clean(first.get("structural_fact_lane")) or "not_temporal_key_source"
            structural_fact_grain = _clean(first.get("source_v552_structural_fact_grain")) or _clean(first.get("structural_fact_grain")) or "not_temporal_key_source"
            structural_pressure_values = pd.to_numeric(group.get("structural_pressure_value", pd.Series(dtype=float)), errors="coerce").dropna()
            structural_pressure_value = round(float(structural_pressure_values.mean()), 6) if not structural_pressure_values.empty else None
            probe_pressure_value = round(float(group.get("probe_pressure_value", pd.Series(dtype=float)).astype(float).mean()) if "probe_pressure_value" in group.columns else 0.0, 6)
            pressure_value_kind = "authorized_structural" if auth["multi_wave_authorization_status"] == AUTHORIZED_SPARSE_TEMPORAL_KEY else "probe_only"
            authorized_structural_pressure_value = structural_pressure_value if pressure_value_kind == "authorized_structural" else None
            probe_structural_score = probe_pressure_value
            pressure_value = authorized_structural_pressure_value if authorized_structural_pressure_value is not None else probe_structural_score
            packet_ids = sorted({item for value in group.get("source_v552j_packet_ids_json", pd.Series(dtype=str)).tolist() for item in _parse_json_array(value)})
            input_ids = sorted({item for value in group.get("source_v552j_input_ids_json", pd.Series(dtype=str)).tolist() for item in _parse_json_array(value)})
            readiness_score = round(float(pd.to_numeric(group.get("readiness_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "readiness_score" in group.columns and not pd.to_numeric(group.get("readiness_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            support_score = round(float(pd.to_numeric(group.get("support_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "support_score" in group.columns and not pd.to_numeric(group.get("support_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            directionality_score = round(float(pd.to_numeric(group.get("directionality_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "directionality_score" in group.columns and not pd.to_numeric(group.get("directionality_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            authority_score = round(float(pd.to_numeric(group.get("authority_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "authority_score" in group.columns and not pd.to_numeric(group.get("authority_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            comparability_score = round(float(pd.to_numeric(group.get("comparability_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "comparability_score" in group.columns and not pd.to_numeric(group.get("comparability_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            confidence_score = round(float(pd.to_numeric(group.get("confidence_score", pd.Series(dtype=float)), errors="coerce").dropna().mean()), 6) if "confidence_score" in group.columns and not pd.to_numeric(group.get("confidence_score", pd.Series(dtype=float)), errors="coerce").dropna().empty else 0.0
            key_status = auth["multi_wave_authorization_status"]
            grouped_rows.append(
                {
                    "run_id": run_id,
                    "temporal_pressure_key": temporal_pressure_key,
                    "country": _required_country(first.get("country")),
                    "source_v552_structural_fact_id": _clean(first.get("source_v552_structural_fact_id")) or (structural_fact_ids[0] if structural_fact_ids else ""),
                    "source_v552_structural_fact_ids_json": _json_singleton_array(_clean(first.get("source_v552_structural_fact_id")) or (structural_fact_ids[0] if structural_fact_ids else "")),
                    "source_v552_structural_fact_ids_diagnostic_json": _json_array(structural_fact_ids),
                    "source_v552_temporal_key_source_id": _first_or_unknown(temporal_key_source_ids, _clean(first.get("source_v552_temporal_key_source_id")) or ""),
                    "source_v552_temporal_key_source_ids_json": _json_singleton_array(_first_or_unknown(temporal_key_source_ids, _clean(first.get("source_v552_temporal_key_source_id")) or "")),
                    "source_v552_temporal_key_source_ids_diagnostic_json": _json_array(temporal_key_source_ids),
                    "structural_fact_lane": structural_fact_lane,
                    "structural_fact_grain": structural_fact_grain,
                    "source_v552_structural_fact_lane": structural_fact_lane,
                    "source_v552_structural_fact_grain": structural_fact_grain,
                    "comparable_temporal_key": _clean(first.get("comparable_temporal_key")) or _clean(temporal_pressure_key),
                    "comparable_key_grain": _clean(first.get("comparable_key_grain")) or "",
                    "comparable_key_basis_json": _clean(first.get("comparable_key_basis_json")) or "{}",
                    "canonical_semantic_signature": _clean(first.get("canonical_semantic_signature")) or _clean(first.get("semantic_signature")) or "",
                    "relation_axis": _clean(first.get("relation_axis")) or "",
                    "target_entity": _clean(first.get("target_entity")) or "",
                    "driver_facet": _clean(first.get("driver_facet")) or "",
                    "structural_channel": _clean(first.get("structural_channel")) or "",
                    "horizon_constraint": _clean(first.get("horizon_constraint")) or "",
                    "semantic_signature": _clean(first.get("semantic_signature")) or "",
                    "key_basis_json": _clean(first.get("key_basis_json")) or "{}",
                    "source_wave_ids_json": json.dumps(wave_ids, sort_keys=True),
                    "key_candidate_count": int(group.get("candidate_count", pd.Series(dtype=int)).sum()) if "candidate_count" in group.columns else int(len(group)),
                    "key_blocker_count": int(group.get("blocked_input_count", pd.Series(dtype=int)).sum()) if "blocked_input_count" in group.columns else 0,
                    "contributing_wave_ids_json": json.dumps(wave_ids, sort_keys=True),
                    "contributing_packet_ids_json": json.dumps(packet_ids, sort_keys=True),
                    "contributing_input_ids_json": json.dumps(input_ids, sort_keys=True),
                    **auth,
                    "readiness_score": readiness_score,
                    "support_score": support_score,
                    "directionality_score": directionality_score,
                    "authority_score": authority_score,
                    "comparability_score": comparability_score,
                    "confidence_score": confidence_score,
                    "key_authority_status": key_status,
                    "comparability_class": "comparable" if key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY else "reviewable",
                    "comparability_status": _clean(first.get("comparability_status")) or "not_supplied",
                    "comparability_reason": "authorized temporal key" if key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY else auth["multi_wave_authorization_reason"],
                    "blocked_reason": "" if key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY else auth["multi_wave_authorization_reason"],
                    "structural_dimension_status": _clean(first.get("structural_dimension_status")) or "missing",
                    "fallback_permission_profile_key": _clean(first.get("fallback_permission_profile_key")) or "",
                    "pressure_value_kind": pressure_value_kind,
                    "pressure_value": pressure_value,
                    "probe_pressure_value": probe_pressure_value,
                    "probe_structural_score": probe_structural_score,
                    "structural_pressure_value": authorized_structural_pressure_value,
                    "authorized_structural_pressure_value": authorized_structural_pressure_value,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
        key_index_df = pd.DataFrame(grouped_rows, columns=V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA["required_columns"])
    real_structural_rows_present = bool(
        not key_wave_df.empty
        and (
            key_wave_df.get("source_v552_structural_fact_id", pd.Series(dtype=str)).astype(str).str.strip().ne("").any()
            or key_wave_df.get("source_v552_temporal_key_source_id", pd.Series(dtype=str)).astype(str).str.strip().ne("").any()
        )
    )
    if real_structural_rows_present and key_index_df.empty:
        raise RuntimeError("V553_NO_STRUCTURAL_KEYS_FOR_REAL_HANDOFF")
    if real_structural_rows_present and not key_index_df.empty:
        key_text = key_index_df.get("temporal_pressure_key", pd.Series(dtype=str)).astype(str)
        if key_text.str.contains("::demo", na=False).any():
            raise RuntimeError("V553_DEMO_KEYS_FOUND_IN_REAL_HANDOFF")
    resolution_audit_df = pd.DataFrame(resolution_audit_rows)
    return key_wave_df, blocker_df, key_index_df, resolution_audit_df


def _build_v553_temporal_pressure_observation_index(
    report: dict[str, Any],
    key_wave_df: pd.DataFrame,
    key_index_df: pd.DataFrame,
    run_id: str,
) -> pd.DataFrame:
    if key_wave_df.empty or key_index_df.empty:
        return pd.DataFrame(columns=V553_TEMPORAL_PRESSURE_OBSERVATION_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    key_group_column = "comparable_temporal_key" if "comparable_temporal_key" in key_index_df.columns else "temporal_pressure_key"
    key_lookup = {str(row[key_group_column]): row.to_dict() for _, row in key_index_df.iterrows() if _clean(row.get(key_group_column))}
    for key, key_row in key_lookup.items():
        subset = key_wave_df[
            key_wave_df[key_group_column].astype(str).eq(str(key))
            if key_group_column in key_wave_df.columns
            else key_wave_df["temporal_pressure_key"].astype(str).eq(str(key))
        ].copy()
        if subset.empty:
            continue
        if not subset.get("structural_dimension_status", pd.Series(dtype=str)).astype(str).eq("resolved").any():
            continue
        country = _clean(key_row.get("country")) or _report_country(report)
        structural_dimension_status = _clean(key_row.get("structural_dimension_status")) or "missing"
        fallback_permission_profile_key = _clean(key_row.get("fallback_permission_profile_key")) or ""
        structural_fact_lane = _clean(key_row.get("source_v552_structural_fact_lane")) or _clean(key_row.get("structural_fact_lane")) or "not_temporal_key_source"
        structural_fact_grain = _clean(key_row.get("source_v552_structural_fact_grain")) or _clean(key_row.get("structural_fact_grain")) or "not_temporal_key_source"
        key_authority = _clean(key_lookup.get(key, {}).get("key_authority_status")) or "probe_temporal_key"
        for _, wave_row in subset.iterrows():
            wave = _clean(wave_row.get("wave_id"))
            if not wave:
                continue
            key_status = _clean(key_row.get("multi_wave_authorization_status")) or _clean(key_row.get("key_authority_status")) or PROBE_ONLY_TEMPORAL_KEY
            if key_status == BLOCKED_TEMPORAL_KEY:
                continue
            row = next((candidate for candidate in (report.get("wave_rows", []) or []) if isinstance(candidate, dict) and _clean(candidate.get("wave")) == wave), {})
            counts = row.get("overlay_row_counts", {}) or {}
            if not isinstance(counts, dict):
                counts = {}
            candidate_count = int(key_row.get("candidate_count", 0) or 0)
            ready_inputs = int(key_row.get("ready_for_v553_input_count", 0) or 0)
            temporal_allowed_inputs = int(key_row.get("temporal_allowed_input_count", 0) or 0)
            probe_allowed_inputs = int(key_row.get("probe_only_input_count", 0) or 0)
            runtime_consumption_inputs = int(key_row.get("ready_for_runtime_consumption_input_count", 0) or 0)
            readiness_score = round(float(key_row.get("readiness_score", 0.0) or 0.0), 6)
            support_score = round(float(key_row.get("support_score", 0.0) or 0.0), 6)
            directionality_score = round(float(key_row.get("directionality_score", 0.0) or 0.0), 6)
            authority_score = round(float(key_row.get("authority_score", 0.0) or 0.0), 6)
            confidence_score = round(float(key_row.get("confidence_score", 0.0) or 0.0), 6)
            comparability_score = round(float(key_row.get("comparability_score", 0.0) or 0.0), 6)
            probe_strength_score = readiness_score
            evidence_coverage_score = round(min(1.0, candidate_count / max(1, len(report.get("wave_rows", []) or []))), 6)
            harmonization_coverage_score = round(ready_inputs / max(1, candidate_count), 6)
            wave_structural_value = _optional_float(wave_row.get("structural_pressure_value"))
            wave_probe_value = float(wave_row.get("probe_pressure_value", readiness_score) or readiness_score)
            structural_pressure_score = round(wave_structural_value if wave_structural_value is not None else 0.0, 6)
            probe_pressure_value = round(wave_probe_value, 6)
            probe_structural_score = round(float(wave_row.get("probe_structural_score", probe_pressure_value) or probe_pressure_value), 6)
            eligible_wave = bool(
                key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY
                and int(wave_row.get("probe_ready_input_count", 0) or 0) > 0
                and _clean(wave_row.get("structural_dimension_status")) == "resolved"
                and wave_structural_value is not None
                and _parse_json_array(wave_row.get("source_v552j_packet_ids_json"))
            )
            if key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY and not eligible_wave:
                continue
            if eligible_wave:
                pressure_value = wave_structural_value
                structural_pressure_value = wave_structural_value
                authorized_structural_pressure_value = wave_structural_value
                pressure_value_kind = "authorized_structural"
                pressure_status = "observed_authorized_anchor"
                allowed_downstream_use = True
                probe_only = False
                structural_pressure_authority = "v553_multi_wave_authorized"
            else:
                pressure_value = wave_probe_value
                structural_pressure_value = wave_structural_value
                authorized_structural_pressure_value = None
                pressure_value_kind = "probe_only"
                pressure_status = "probe_only_anchor"
                allowed_downstream_use = False
                probe_only = True
                structural_pressure_authority = "probe_temporal_key"
            uncertainty_score = round(max(0.0, 1.0 - confidence_score), 6)
            lane_summary = {
                "wave_status": _clean(row.get("wave_status")) or "unknown",
                "thin_status": _clean(row.get("thin_status")) or "unknown",
                "overlay_row_counts": counts,
                "missing_authority_kinds": list(row.get("missing_authority_kinds", []) or []),
                "v552j_readiness_status": _clean(row.get("v552j_readiness_status")) or "unknown",
                "v552j_handoff_authority_status": _clean(row.get("v552j_handoff_authority_status")) or "unknown",
                "structural_fact_lane": structural_fact_lane,
                "structural_fact_grain": structural_fact_grain,
                "probe_allowed_inputs": probe_allowed_inputs,
                "ready_for_v553_inputs": ready_inputs,
                "temporal_field_allowed_inputs": temporal_allowed_inputs,
                "runtime_consumption_inputs": runtime_consumption_inputs,
                "evidence_coverage_score": evidence_coverage_score,
                "harmonization_coverage_score": harmonization_coverage_score,
                "structural_pressure_score": structural_pressure_score,
                "structural_dimension_status": structural_dimension_status,
                "fallback_permission_profile_key": fallback_permission_profile_key,
            }
            rows.append(
                {
                    "run_id": run_id,
                    "observation_id": f"v553_obs_{key}_{wave}",
                    "temporal_pressure_key": key,
                    "country": country,
                    "wave_id": wave,
                    "survey_year": _int(row.get("temporal_year"), 0),
                    "pressure_value": pressure_value,
                    "support_score": support_score,
                    "confidence_score": confidence_score,
                    "directionality_score": directionality_score,
                    "authority_score": authority_score,
                    "uncertainty_score": uncertainty_score,
                    "source_v552_structural_fact_id": _clean(key_row.get("source_v552_structural_fact_id")) or "",
                    "source_v552_structural_fact_ids_json": _clean(key_row.get("source_v552_structural_fact_ids_json")) or "[]",
                    "source_v552_structural_fact_ids_diagnostic_json": _clean(key_row.get("source_v552_structural_fact_ids_diagnostic_json")) or "[]",
                    "source_v552_temporal_key_source_id": _first_or_unknown(_parse_json_array(key_row.get("source_v552_temporal_key_source_ids_json")), _clean(key_row.get("source_v552_temporal_key_source_id")) or ""),
                    "source_v552_temporal_key_source_ids_json": _clean(key_row.get("source_v552_temporal_key_source_ids_json")) or "[]",
                    "source_v552_temporal_key_source_ids_diagnostic_json": _clean(key_row.get("source_v552_temporal_key_source_ids_diagnostic_json")) or "[]",
                    "structural_fact_lane": structural_fact_lane,
                    "structural_fact_grain": structural_fact_grain,
                    "source_v552_structural_fact_lane": structural_fact_lane,
                    "source_v552_structural_fact_grain": structural_fact_grain,
                    "comparable_temporal_key": _clean(key_row.get("comparable_temporal_key")) or _clean(key),
                    "comparable_key_grain": _clean(key_row.get("comparable_key_grain")) or "",
                    "comparable_key_basis_json": _clean(key_row.get("comparable_key_basis_json")) or "{}",
                    "canonical_semantic_signature": _clean(key_row.get("canonical_semantic_signature")) or _clean(key_row.get("semantic_signature")) or "",
                    "pressure_value_kind": pressure_value_kind,
                    "source_v552j_packet_ids_json": _clean(wave_row.get("source_v552j_packet_ids_json")) or "[]",
                    "source_lane_summary": json.dumps(lane_summary, sort_keys=True),
                    "probe_strength_score": probe_strength_score,
                    "evidence_coverage_score": evidence_coverage_score,
                    "harmonization_coverage_score": harmonization_coverage_score,
                    "structural_pressure_score": structural_pressure_score,
                    "structural_pressure_value": structural_pressure_value,
                    "authorized_structural_pressure_value": authorized_structural_pressure_value,
                    "probe_pressure_value": probe_pressure_value,
                    "probe_structural_score": probe_structural_score,
                    "structural_pressure_authority": structural_pressure_authority,
                    "structural_dimension_status": structural_dimension_status,
                    "fallback_permission_profile_key": fallback_permission_profile_key,
                    "temporal_status": pressure_status,
                    "allowed_downstream_use": allowed_downstream_use,
                    "probe_only": probe_only,
                    "ready_for_v553_inputs": ready_inputs,
                    "probe_ready_inputs": int(wave_row.get("probe_ready_input_count", 0) or 0),
                    "temporal_field_allowed_inputs": temporal_allowed_inputs,
                    "single_wave_probe_allowed_inputs": probe_allowed_inputs,
                    "ready_for_runtime_consumption_inputs": runtime_consumption_inputs,
                    "multi_wave_authorization_status": key_status,
                    "multi_wave_authorization_reason": _clean(key_row.get("multi_wave_authorization_reason")) or "",
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows)


def _build_v553_cross_wave_delta_index(report: dict[str, Any], observation_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if observation_df.empty:
        return pd.DataFrame(columns=V553_CROSS_WAVE_DELTA_INDEX_SCHEMA["required_columns"])
    country = _clean(observation_df.iloc[0].get("country")) or _report_country(report)
    rows: list[dict[str, Any]] = []
    group_key_column = "comparable_temporal_key" if "comparable_temporal_key" in observation_df.columns else "temporal_pressure_key"
    for temporal_pressure_key, key_obs in observation_df.groupby(group_key_column, dropna=False):
        obs = key_obs.sort_values(["survey_year", "wave_id"]).reset_index(drop=True)
        if len(obs) < 2:
            continue
        for idx in range(1, len(obs)):
            prior = obs.iloc[idx - 1]
            current = obs.iloc[idx]
            prior_structural_value = _optional_float(prior.get("authorized_structural_pressure_value"))
            current_structural_value = _optional_float(current.get("authorized_structural_pressure_value"))
            probe_delta_value = round(float(current.get("probe_pressure_value", 0.0) or 0.0) - float(prior.get("probe_pressure_value", 0.0) or 0.0), 6)
            if prior_structural_value is not None and current_structural_value is not None:
                authorized_structural_delta_value = round(current_structural_value - prior_structural_value, 6)
            else:
                authorized_structural_delta_value = None
            structural_delta_value = authorized_structural_delta_value
            coverage_delta_value = round(float(current.get("evidence_coverage_score", 0.0) or 0.0) - float(prior.get("evidence_coverage_score", 0.0) or 0.0), 6)
            delta_value_kind = "authorized_structural" if authorized_structural_delta_value is not None else "probe_delta"
            delta_value = authorized_structural_delta_value if authorized_structural_delta_value is not None else probe_delta_value
            delta_direction_basis = authorized_structural_delta_value if authorized_structural_delta_value is not None else probe_delta_value
            if delta_direction_basis > 0.05:
                delta_direction = "up"
            elif delta_direction_basis < -0.05:
                delta_direction = "down"
            else:
                delta_direction = "flat"
            abs_delta = abs(delta_direction_basis)
            if abs_delta >= 0.4:
                delta_magnitude_class = "large"
            elif abs_delta >= 0.2:
                delta_magnitude_class = "medium"
            else:
                delta_magnitude_class = "small"
            confidence_delta = round(float(current.get("confidence_score", 0.0) or 0.0) - float(prior.get("confidence_score", 0.0) or 0.0), 6)
            authority_delta = round(float(current.get("authority_score", 0.0) or 0.0) - float(prior.get("authority_score", 0.0) or 0.0), 6)
            prior_status = _clean(prior.get("temporal_status")) or "unknown"
            current_status = _clean(current.get("temporal_status")) or "unknown"
            comparability_status = "authorized_comparable" if prior_status == "observed_authorized_anchor" and current_status == "observed_authorized_anchor" else "probe_only"
            delta_interpretation_permission = bool(comparability_status == "authorized_comparable" and authorized_structural_delta_value is not None)
            if delta_interpretation_permission:
                delta_value_kind = "authorized_structural"
            rows.append(
                {
                    "run_id": run_id,
                    "delta_id": f"v553_delta_{_clean(prior.get('wave_id'))}_to_{_clean(current.get('wave_id'))}",
                    "temporal_pressure_key": _clean(temporal_pressure_key) or "v553tp_unknown",
                    "comparable_temporal_key": _clean(temporal_pressure_key) or "v553tp_unknown",
                    "country": country,
                    "from_wave_id": _clean(prior.get("wave_id")),
                    "to_wave_id": _clean(current.get("wave_id")),
                    "from_year": _int(prior.get("survey_year"), 0),
                    "to_year": _int(current.get("survey_year"), 0),
                    "delta_value": delta_value,
                    "delta_value_kind": delta_value_kind,
                    "structural_delta_value": structural_delta_value,
                    "authorized_structural_delta_value": authorized_structural_delta_value,
                    "probe_delta_value": probe_delta_value,
                    "coverage_delta_value": coverage_delta_value,
                    "delta_direction": delta_direction,
                    "delta_magnitude_class": delta_magnitude_class,
                    "confidence_delta": confidence_delta,
                    "authority_delta": authority_delta,
                    "comparability_status": comparability_status,
                    "delta_basis": "structural_pressure_value" if authorized_structural_delta_value is not None else "probe_pressure_value",
                    "blocked_reason": "" if delta_interpretation_permission else "probe_only_temporal_field",
                    "delta_interpretation_permission": delta_interpretation_permission,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V553_CROSS_WAVE_DELTA_INDEX_SCHEMA["required_columns"])


def _build_v553_interpolation_segment_index(report: dict[str, Any], observation_df: pd.DataFrame, run_id: str, *, allow_interpolation: bool) -> pd.DataFrame:
    if observation_df.empty:
        return pd.DataFrame(columns=V553_INTERPOLATION_SEGMENT_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for key, key_obs in observation_df.groupby("temporal_pressure_key", dropna=False):
        key = _clean(key) or "v553tp_unknown"
        country = _clean(key_obs.iloc[0].get("country")) or _report_country(report)
        obs = key_obs.sort_values(["survey_year", "wave_id"]).reset_index(drop=True)
        if len(obs) < 2:
            continue
        key_status = _clean(obs.iloc[0].get("multi_wave_authorization_status")) or _clean(obs.iloc[0].get("key_authorization_status")) or PROBE_ONLY_TEMPORAL_KEY
        anchor_count = int(obs.get("temporal_status", pd.Series(dtype=str)).astype(str).eq("observed_authorized_anchor").sum())
        for idx in range(1, len(obs)):
            start = obs.iloc[idx - 1]
            end = obs.iloc[idx]
            gap = max(0, _int(end.get("survey_year"), 0) - _int(start.get("survey_year"), 0) - 1)
            if gap > 0 and key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY:
                interpolation_status = "unknown_gap_preserved"
                interpolation_method = "none"
                interpolation_allowed = False
                interpolation_reason = "no_survey_observation_preserve_unknown"
            elif key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY:
                interpolation_status = "adjacent_authorized_anchors"
                interpolation_method = "none"
                interpolation_allowed = False
                interpolation_reason = "no missing year span"
            else:
                interpolation_status = "probe_only"
                interpolation_method = "none"
                interpolation_allowed = False
                interpolation_reason = "probe_only_temporal_key"
            rows.append(
                {
                    "run_id": run_id,
                    "temporal_pressure_key": key,
                    "country": country,
                    "segment_start_year": _int(start.get("survey_year"), 0),
                    "segment_end_year": _int(end.get("survey_year"), 0),
                    "interpolation_status": interpolation_status,
                    "interpolation_method": interpolation_method,
                    "interpolation_allowed": interpolation_allowed,
                    "interpolation_reason": interpolation_reason,
                    "key_authorization_status": key_status,
                    "anchor_count": anchor_count,
                    "confidence_decay": round(1.0 / (1.0 + max(0, gap)), 6),
                    "gap_length_years": gap,
                    "warning_flags_json": json.dumps(["gap_segment"] if gap > 0 else [], sort_keys=True),
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V553_INTERPOLATION_SEGMENT_INDEX_SCHEMA["required_columns"])


def _build_v553_run_manifest(
    *,
    run_id: str,
    report: dict[str, Any],
    readiness: dict[str, Any],
    artifact_paths: dict[str, str],
    artifact_row_counts: dict[str, int],
) -> pd.DataFrame:
    source_runs: list[str] = []
    for item in report.get("wave_rows", []) or []:
        if not isinstance(item, dict):
            continue
        v552j_context = _wave_v552j_context(item)
        source_run_id = _run_id_from_path(v552j_context.get("resolved_root") or item.get("latest_v552j_root") or item.get("run_root"))
        if source_run_id:
            source_runs.append(source_run_id)
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "source_runs_json": json.dumps(sorted(set(source_runs)), sort_keys=True),
                "artifact_paths_json": json.dumps(artifact_paths, sort_keys=True),
                "artifact_row_counts_json": json.dumps(artifact_row_counts, sort_keys=True),
                "compiler_version": V553_COMPILER_VERSION,
                "readiness_status": _clean(readiness.get("status")) or "unknown",
                "blocker_counts_json": json.dumps(
                    {
                        "blocked_rows": int(readiness.get("blocked_rows", 0) or 0),
                        "review_required_rows": int(readiness.get("review_required_rows", 0) or 0),
                        "v552j_blocker_context_count": int(readiness.get("v552j_blocker_context_count", 0) or 0),
                    },
                    sort_keys=True,
                ),
                "completeness_status": "ready" if str(readiness.get("status", "")).startswith("READY") else "blocked",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
            }
        ],
        columns=V553_RUN_MANIFEST_SCHEMA["required_columns"],
    )


def _build_v553_temporal_gap_and_absence_index(report: dict[str, Any], segment_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if segment_df.empty:
        return pd.DataFrame(columns=V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for _, row in segment_df.iterrows():
        gap = _int(row.get("gap_length_years"), 0)
        if gap <= 0:
            continue
        key = _clean(row.get("temporal_pressure_key")) or "v553tp_unknown"
        country = _clean(row.get("country")) or _report_country(report)
        key_status = _clean(row.get("key_authorization_status")) or PROBE_ONLY_TEMPORAL_KEY
        start = _int(row.get("segment_start_year"), 0)
        end = _int(row.get("segment_end_year"), 0)
        for missing_year in range(start + 1, end):
            rows.append(
                {
                    "run_id": run_id,
                    "temporal_pressure_key": key,
                    "country": country,
                    "missing_year_or_span": str(missing_year),
                    "absence_type": "missing_year",
                    "known_absence": True,
                    "missingness_reason": "no_survey_observation_preserve_unknown",
                    "downstream_permission": bool(key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY),
                    "key_authorization_status": key_status,
                    "value_inference_allowed": False,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA["required_columns"])


def _build_v553_structural_rupture_candidate_index(delta_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if delta_df.empty:
        return pd.DataFrame(columns=V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for _, row in delta_df.iterrows():
        strength = abs(float(row.get("delta_value", 0.0) or 0.0))
        reversal = _clean(row.get("delta_direction")) in {"down", "up"} and strength >= 0.35
        if strength < 0.25 and not reversal:
            continue
        rows.append(
            {
                "run_id": run_id,
                "temporal_pressure_key": row.get("temporal_pressure_key", ""),
                "country": row.get("country", ""),
                "rupture_window_start": int(min(_int(row.get("from_year"), 0), _int(row.get("to_year"), 0))),
                "rupture_window_end": int(max(_int(row.get("from_year"), 0), _int(row.get("to_year"), 0))),
                "rupture_signal_type": "direction_reversal" if reversal else "large_delta",
                "rupture_signal_strength": round(strength, 6),
                "source_delta_ids_json": json.dumps([f"{_clean(row.get('from_wave_id'))}->{_clean(row.get('to_wave_id'))}"], sort_keys=True),
                "rupture_status": "candidate",
                "external_event_claim_made": False,
                "interpretation_permission": bool(_clean(row.get("comparability_status")) == "comparable" and abs(float(row.get("delta_value", 0.0) or 0.0)) >= 0.25),
                "blocked_reason": "" if _clean(row.get("comparability_status")) == "comparable" else "probe_only_temporal_field",
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA["required_columns"])


def _build_v553_temporal_pressure_field_contract(
    report: dict[str, Any],
    observation_df: pd.DataFrame,
    gap_df: pd.DataFrame,
    delta_df: pd.DataFrame,
    run_id: str,
) -> pd.DataFrame:
    if observation_df.empty:
        return pd.DataFrame(columns=V553_TEMPORAL_PRESSURE_FIELD_CONTRACT_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for temporal_pressure_key, group in observation_df.groupby("temporal_pressure_key", dropna=False):
        key = _clean(temporal_pressure_key) or "v553tp_unknown"
        if not key:
            continue
        country = _clean(group.iloc[0].get("country")) or _report_country(report)
        obs_years = {_int(row.get("survey_year"), 0) for _, row in group.iterrows()}
        if not obs_years:
            continue
        min_year = min(obs_years)
        max_year = max(obs_years)
        obs_by_year = {_int(row.get("survey_year"), 0): row for _, row in group.iterrows()}
        key_gap_df = gap_df[gap_df["temporal_pressure_key"].astype(str).eq(key)] if not gap_df.empty and "temporal_pressure_key" in gap_df.columns else pd.DataFrame()
        gap_years = {_int(str(value), 0) for value in (key_gap_df.get("missing_year_or_span", pd.Series(dtype=str)).tolist() if not key_gap_df.empty else [])}
        delta_ids_by_year: dict[int, list[str]] = {}
        for _, delta_row in delta_df.iterrows():
            if _clean(delta_row.get("temporal_pressure_key")) not in {"", key}:
                continue
            delta_id = _clean(delta_row.get("delta_id"))
            if not delta_id:
                continue
            from_year = _int(delta_row.get("from_year"), 0)
            to_year = _int(delta_row.get("to_year"), 0)
            delta_ids_by_year.setdefault(from_year, []).append(delta_id)
            delta_ids_by_year.setdefault(to_year, []).append(delta_id)
        for year in range(min_year, max_year + 1):
            obs = obs_by_year.get(year)
            if obs is not None:
                obs_status = _clean(obs.get("temporal_status"))
                key_status = _clean(obs.get("multi_wave_authorization_status")) or _clean(obs.get("key_authorization_status")) or PROBE_ONLY_TEMPORAL_KEY
                pressure_level = _optional_float(obs.get("authorized_structural_pressure_value")) if obs_status == "observed_authorized_anchor" else float(obs.get("pressure_value", 0.0) or 0.0)
                pressure_direction = "neutral" if pressure_level == 0 else ("positive" if pressure_level >= 0 else "negative")
                pressure_volatility = round(max(0.0, 1.0 - float(obs.get("support_score", 0.0) or 0.0)), 6)
                pressure_confidence = float(obs.get("confidence_score", 0.0) or 0.0)
                pressure_authority = "authorized_observed_anchor" if obs_status == "observed_authorized_anchor" else "probe_only_anchor"
                structural_pressure_value = _optional_float(obs.get("structural_pressure_value"))
                authorized_structural_pressure_value = _optional_float(obs.get("authorized_structural_pressure_value"))
                probe_pressure_value = float(obs.get("probe_pressure_value", pressure_level) or pressure_level)
                probe_structural_score = float(obs.get("probe_structural_score", probe_pressure_value) or probe_pressure_value)
                evidence_coverage_score = float(obs.get("evidence_coverage_score", 0.0) or 0.0)
                structural_pressure_authority = _clean(obs.get("structural_pressure_authority")) or pressure_authority
                temporal_status = obs_status or "probe_only_anchor"
                pressure_value_kind = _clean(obs.get("pressure_value_kind")) or ("authorized_structural" if authorized_structural_pressure_value is not None else "probe_only")
                allowed_downstream_use = bool(temporal_status == "observed_authorized_anchor" and authorized_structural_pressure_value is not None)
                source_observation_ids = [_clean(obs.get("observation_id"))]
                source_delta_ids = sorted(set(delta_ids_by_year.get(year, [])))
                blocked_reason = "" if allowed_downstream_use else "probe_only_temporal_field"
                pressure_basis = "observed_structural_pressure" if temporal_status == "observed_authorized_anchor" else "probe_only"
                probe_only = temporal_status == "probe_only_anchor"
            else:
                pressure_level = None
                pressure_direction = "unknown"
                pressure_volatility = 1.0
                pressure_confidence = 0.0
                pressure_authority = "known_unknown_gap"
                temporal_status = "unknown_gap"
                allowed_downstream_use = False
                structural_pressure_value = None
                authorized_structural_pressure_value = None
                probe_pressure_value = None
                probe_structural_score = None
                pressure_value_kind = "gap"
                source_observation_ids = []
                source_delta_ids = sorted(set(delta_ids_by_year.get(year - 1, []) + delta_ids_by_year.get(year + 1, [])))
                blocked_reason = "no_survey_observation_preserve_unknown" if year in gap_years else "noncomparable_gap"
                pressure_basis = "explicit_absence"
                probe_only = False
                key_status = AUTHORIZED_SPARSE_TEMPORAL_KEY if year in gap_years else PROBE_ONLY_TEMPORAL_KEY
            rows.append(
                {
                    "run_id": run_id,
                    "temporal_pressure_key": key,
                    "country": country,
                    "year_or_period": str(year),
                    "pressure_level": pressure_level,
                    "pressure_direction": pressure_direction,
                    "pressure_volatility": pressure_volatility,
                    "pressure_confidence": pressure_confidence,
                    "pressure_authority": pressure_authority,
                    "structural_pressure_value": structural_pressure_value,
                    "authorized_structural_pressure_value": authorized_structural_pressure_value,
                    "probe_pressure_value": probe_pressure_value,
                    "probe_structural_score": probe_structural_score,
                    "pressure_value_kind": pressure_value_kind,
                    "evidence_coverage_score": evidence_coverage_score,
                    "structural_pressure_authority": structural_pressure_authority,
                    "temporal_status": temporal_status,
                    "allowed_downstream_use": allowed_downstream_use,
                    "source_observation_ids_json": json.dumps(source_observation_ids, sort_keys=True),
                    "source_delta_ids_json": json.dumps(source_delta_ids, sort_keys=True),
                    "blocked_reason": blocked_reason,
                    "pressure_basis": pressure_basis,
                    "probe_only": probe_only,
                    "key_authorization_status": key_status,
                    "created_at": utc_now(),
                    "schema_version": V553_SCHEMA_VERSION,
                    "compiler_version": V553_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V553_TEMPORAL_PRESSURE_FIELD_CONTRACT_SCHEMA["required_columns"])


def _build_v553_v554_handoff_index(report: dict[str, Any], field_df: pd.DataFrame, gap_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if field_df.empty:
        return pd.DataFrame(columns=V553_V554_HANDOFF_INDEX_SCHEMA["required_columns"])
    permitted = [
        "pressure_level",
        "pressure_direction",
        "pressure_volatility",
        "pressure_confidence",
        "pressure_authority",
    ]
    blocked = [
        "biography",
        "persona",
        "parent_story",
        "psyche",
        "Enneagram",
        "prompt",
        "runtime_text",
    ]
    rows: list[dict[str, Any]] = []
    for temporal_pressure_key, group in field_df.groupby("temporal_pressure_key", dropna=False):
        key = _clean(temporal_pressure_key) or "v553tp_unknown"
        if not key:
            continue
        country = _clean(group.iloc[0].get("country")) or _report_country(report)
        key_gap_df = gap_df[gap_df["temporal_pressure_key"].astype(str).eq(key)] if not gap_df.empty and "temporal_pressure_key" in gap_df.columns else pd.DataFrame()
        key_status = _clean(group.iloc[0].get("key_authorization_status")) or PROBE_ONLY_TEMPORAL_KEY
        authorized_anchor_count = int(group.get("temporal_status", pd.Series(dtype=str)).astype(str).eq("observed_authorized_anchor").sum())
        probe_anchor_count = int(group.get("temporal_status", pd.Series(dtype=str)).astype(str).eq("probe_only_anchor").sum())
        unknown_gap_count = int(len(key_gap_df))
        interpolated_row_count = 0
        uncertainty_payload = {
            "gap_count": unknown_gap_count,
            "wave_count": int(report.get("wave_count", 0) or 0),
            "ready_for_v553": bool(report.get("ready_for_v553", False)),
            "authorized_anchor_count": authorized_anchor_count,
            "probe_anchor_count": probe_anchor_count,
            "unknown_gap_count": unknown_gap_count,
            "interpolated_row_count": interpolated_row_count,
            "interpolation_allowed": False,
            "key_authorization_status": key_status,
            "probe_only_temporal_field": bool(key_status != AUTHORIZED_SPARSE_TEMPORAL_KEY),
        }
        ready = bool(key_status == AUTHORIZED_SPARSE_TEMPORAL_KEY and authorized_anchor_count >= 2)
        handoff_mode = "sparse_temporal_field_ready" if ready else ("probe_only" if key_status == PROBE_ONLY_TEMPORAL_KEY else "blocked")
        probe_allowed = True
        temporal_field_allowed = bool(ready)
        handoff_allowed = bool(ready)
        blocked_reason = "" if ready else ("insufficient_distinct_waves" if key_status == PROBE_ONLY_TEMPORAL_KEY else "blocked_temporal_key")
        rows.append(
            {
                "run_id": run_id,
                "temporal_pressure_key": key,
                "country": country,
                "permitted_seed_affordance_inputs_json": json.dumps(permitted, sort_keys=True),
                "blocked_seed_affordance_inputs_json": json.dumps(blocked, sort_keys=True),
                "uncertainty_payload_json": json.dumps(uncertainty_payload, sort_keys=True),
                "required_v554_absence_handling": "carry forward unresolved gaps and do not infer personhood",
                "ready_for_v554_seed_affordance": ready,
                "v553_handoff_mode": handoff_mode,
                "v553_handoff_allowed": handoff_allowed,
                "v553_probe_allowed": probe_allowed,
                "v553_temporal_field_allowed": temporal_field_allowed,
                "v553_handoff_blocked_reason": blocked_reason,
                "not_personhood_reason": "V553 produces seed affordance inputs only; it does not produce a person or persona.",
                "key_authorization_status": key_status,
                "authorized_anchor_count": authorized_anchor_count,
                "probe_anchor_count": probe_anchor_count,
                "unknown_gap_count": unknown_gap_count,
                "interpolated_row_count": interpolated_row_count,
                "created_at": utc_now(),
                "schema_version": V553_SCHEMA_VERSION,
                "compiler_version": V553_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V553_V554_HANDOFF_INDEX_SCHEMA["required_columns"])


def _build_v553_forbidden_inference_audit(run_id: str) -> pd.DataFrame:
    forbidden_claims = [
        ("biography", "No biography may be emitted"),
        ("persona", "No persona may be emitted"),
        ("parent_story", "No parent story may be emitted"),
        ("psyche", "No psyche may be emitted"),
        ("Enneagram", "No Enneagram type may be emitted"),
        ("prompt", "No prompt text may be emitted"),
        ("runtime_text", "No runtime text may be emitted"),
    ]
    rows = [
        {
            "run_id": run_id,
            "artifact_name": "v553_forbidden_inference_audit",
            "forbidden_claim_id": claim_id,
            "claim_text": claim_text,
            "violation_detected": False,
            "reason": "V553 remains a structural pressure compiler; these outputs are not built.",
            "created_at": utc_now(),
            "schema_version": V553_SCHEMA_VERSION,
            "compiler_version": V553_COMPILER_VERSION,
        }
        for claim_id, claim_text in forbidden_claims
    ]
    return pd.DataFrame(rows, columns=V553_FORBIDDEN_INFERENCE_AUDIT_SCHEMA["required_columns"])


def _write_v553_semantic_implementation_report(
    *,
    report_path: Path,
    run_id: str,
    wave_harmonization_report_path: str | Path,
    readiness: dict[str, Any],
    wave_anchor_index_df: pd.DataFrame,
    harmonized_pressure_key_index_df: pd.DataFrame,
    temporal_pressure_observation_index_df: pd.DataFrame,
    cross_wave_delta_index_df: pd.DataFrame,
    interpolation_segment_index_df: pd.DataFrame,
    temporal_gap_and_absence_index_df: pd.DataFrame,
    structural_rupture_candidate_index_df: pd.DataFrame,
    temporal_pressure_field_df: pd.DataFrame,
    v554_handoff_index_df: pd.DataFrame,
    forbidden_inference_audit_df: pd.DataFrame,
    harmonization_authority_index_df: pd.DataFrame,
    interpolation_policy_ledger_df: pd.DataFrame,
    rupture_event_slot_ledger_df: pd.DataFrame,
    cohort_window_requirement_index_df: pd.DataFrame,
    run_manifest_df: pd.DataFrame,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# PASS 7 V553 Semantic Implementation Report")
    lines.append("")
    lines.append(f"- run_id: `{run_id}`")
    lines.append(f"- wave_harmonization_report: `{repo_relative_path_text(wave_harmonization_report_path)}`")
    lines.append("- explicit_scope: V553 only")
    lines.append("- explicit_non_goals: V554, V555, V556, V557, V558, runtime, persona, app wiring")
    lines.append("")
    lines.append("## Files Changed")
    lines.append("")
    lines.append("- `data/ddm_build_copy/ddm_v553_schema.py`")
    lines.append("- `data/ddm_build_copy/ddm_v553_temporal_pressure.py`")
    lines.append("- `tests/ddm/test_v553_temporal_pressure.py`")
    lines.append("")
    lines.append("## New Artifacts Emitted")
    lines.append("")
    for label, frame in (
        ("v553_wave_anchor_index", wave_anchor_index_df),
        ("v553_harmonized_pressure_key_index", harmonized_pressure_key_index_df),
        ("v553_temporal_pressure_observation_index", temporal_pressure_observation_index_df),
        ("v553_cross_wave_delta_index", cross_wave_delta_index_df),
        ("v553_interpolation_segment_index", interpolation_segment_index_df),
        ("v553_temporal_gap_and_absence_index", temporal_gap_and_absence_index_df),
        ("v553_structural_rupture_candidate_index", structural_rupture_candidate_index_df),
        ("v553_temporal_pressure_field", temporal_pressure_field_df),
        ("v553_v554_handoff_index", v554_handoff_index_df),
        ("v553_forbidden_inference_audit", forbidden_inference_audit_df),
        ("v553_harmonization_authority_index", harmonization_authority_index_df),
        ("v553_interpolation_policy_ledger", interpolation_policy_ledger_df),
        ("v553_rupture_event_slot_ledger", rupture_event_slot_ledger_df),
        ("v553_cohort_window_requirement_index", cohort_window_requirement_index_df),
        ("v553_run_manifest", run_manifest_df),
    ):
        lines.append(f"- `{label}`: {len(frame)} rows")
    lines.append("")
    lines.append("## Row Counts")
    lines.append("")
    for label, frame in (
        ("wave_anchor_index", wave_anchor_index_df),
        ("harmonized_pressure_key_index", harmonized_pressure_key_index_df),
        ("temporal_pressure_observation_index", temporal_pressure_observation_index_df),
        ("cross_wave_delta_index", cross_wave_delta_index_df),
        ("interpolation_segment_index", interpolation_segment_index_df),
        ("temporal_gap_and_absence_index", temporal_gap_and_absence_index_df),
        ("structural_rupture_candidate_index", structural_rupture_candidate_index_df),
        ("temporal_pressure_field", temporal_pressure_field_df),
        ("v554_handoff_index", v554_handoff_index_df),
        ("forbidden_inference_audit", forbidden_inference_audit_df),
        ("harmonization_authority_index", harmonization_authority_index_df),
        ("interpolation_policy_ledger", interpolation_policy_ledger_df),
        ("rupture_event_slot_ledger", rupture_event_slot_ledger_df),
        ("cohort_window_requirement_index", cohort_window_requirement_index_df),
        ("run_manifest", run_manifest_df),
    ):
        lines.append(f"- {label}: {len(frame)}")
    lines.append("")
    lines.append("## Examples")
    lines.append("")
    if not harmonized_pressure_key_index_df.empty:
        row = harmonized_pressure_key_index_df.iloc[0].to_dict()
        lines.append(f"- comparable_temporal_key: `{_clean(row.get('temporal_pressure_key'))}`")
        lines.append(f"- comparable_status: `{_clean(row.get('comparability_status'))}`")
    if not temporal_gap_and_absence_index_df.empty:
        row = temporal_gap_and_absence_index_df.iloc[0].to_dict()
        lines.append(f"- blocked_noncomparable_key: `{_clean(row.get('temporal_pressure_key'))}`")
        lines.append(f"- gap_example: `{_clean(row.get('missing_year_or_span'))}`")
    if not structural_rupture_candidate_index_df.empty:
        row = structural_rupture_candidate_index_df.iloc[0].to_dict()
        lines.append(f"- rupture_candidate: `{_clean(row.get('rupture_signal_type'))}`")
        lines.append(f"- rupture_strength: `{row.get('rupture_signal_strength', '')}`")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("- No biography, persona, parent story, psyche, Enneagram, prompt, or runtime text was emitted.")
    lines.append("- V554+ was not implemented.")
    lines.append("- Runtime consumption remains blocked.")
    lines.append("")
    lines.append("## Readiness Snapshot")
    lines.append("")
    lines.append(f"- status: `{readiness.get('status', '')}`")
    lines.append(f"- ready_for_v554: `{readiness.get('ready_for_v554', False)}`")
    lines.append(f"- wave_count: `{readiness.get('wave_count', 0)}`")
    lines.append(f"- harmonization_score: `{readiness.get('harmonization_score', 0.0)}`")
    lines.append(f"- missing_required_inputs_json: `{readiness.get('missing_required_inputs_json', '[]')}`")
    lines.append("")
    lines.append("## Remaining Blockers")
    lines.append("")
    lines.append("- V554+ remains out of scope.")
    lines.append("- Downstream runtime/persona wiring remains unimplemented.")
    lines.append("- Any future deepening must preserve the V553 contract.")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_v553_temporal_pressure_field(
    *,
    run_id: str,
    wave_harmonization_report_path: str | Path,
    output_root: str | Path,
    write_csv: bool = False,
    write_parquet: bool = True,
    allow_interpolation: bool = False,
    country_code: str = "",
) -> dict[str, Any]:
    report = _load_report(wave_harmonization_report_path)
    if not report:
        raise RuntimeError(f"Missing or unreadable wave harmonization report: {wave_harmonization_report_path}")
    report = _normalize_temporal_report_identity(
        report,
        explicit_country_code=country_code,
    )
    provenance = capture_run_provenance(
        input_documents={
            "wave_harmonization_report_path": str(wave_harmonization_report_path),
            "output_root": str(output_root),
        }
    )
    harmonization_sidecar = _copy_harmonization_sidecar(
        wave_harmonization_report_path,
        ensure_output_dirs(output_root, run_id)["root"],
        normalized_report=report,
    )
    harmonization_evidence_path = repo_relative_path_text(
        str(report.get("wave_pair_evidence_path", "")).strip() or Path(wave_harmonization_report_path).with_name("v553_wave_harmonization_evidence.parquet")
    )
    harmonization_evidence_exists = Path(harmonization_evidence_path).exists()
    harmonization_evidence_row_count = -1
    if harmonization_evidence_exists:
        try:
            harmonization_evidence_row_count = int(len(pd.read_parquet(harmonization_evidence_path)))
        except Exception:
            harmonization_evidence_row_count = -1

    root = ensure_output_dirs(output_root, run_id)
    pressure_df, contradiction_df, absence_df, forbidden_rows = _build_pressure_rows(report, run_id)
    interpolated_pressure_df = _build_interpolated_pressure_rows(pressure_df, run_id) if allow_interpolation else pd.DataFrame(columns=pressure_df.columns)
    country_year_pressure_df = _build_country_year_pressure_field(
        report,
        pressure_df,
        interpolated_pressure_df,
        run_id,
        allow_interpolation=allow_interpolation,
    )
    harmonization_difference_ledger_df = _build_v553_harmonization_difference_ledger(report, run_id)
    pressure_component_breakdown_df = _build_pressure_component_breakdown(country_year_pressure_df, report, run_id)
    pressure_basis_ledger_df = _build_v553_pressure_basis_ledger(country_year_pressure_df, report, run_id)
    confidence_penalty_ledger_df = _build_v553_confidence_penalty_ledger(country_year_pressure_df, run_id)
    wave_anchor_index_df = _build_v553_wave_anchor_index(report, run_id)
    temporal_key_candidate_index_df, temporal_key_blocker_index_df, harmonized_pressure_key_index_df, structural_dimension_resolution_audit_df = _build_v553_temporal_key_tables(report, run_id)
    temporal_pressure_observation_index_df = _build_v553_temporal_pressure_observation_index(
        report,
        temporal_key_candidate_index_df,
        harmonized_pressure_key_index_df,
        run_id,
    )
    cross_wave_delta_index_df = _build_v553_cross_wave_delta_index(report, temporal_pressure_observation_index_df, run_id)
    interpolation_segment_index_df = _build_v553_interpolation_segment_index(
        report,
        temporal_pressure_observation_index_df,
        run_id,
        allow_interpolation=allow_interpolation,
    )
    temporal_gap_and_absence_index_df = _build_v553_temporal_gap_and_absence_index(
        report,
        interpolation_segment_index_df,
        run_id,
    )
    structural_rupture_candidate_index_df = _build_v553_structural_rupture_candidate_index(
        cross_wave_delta_index_df,
        run_id,
    )
    temporal_pressure_field_df = _build_v553_temporal_pressure_field_contract(
        report,
        temporal_pressure_observation_index_df,
        temporal_gap_and_absence_index_df,
        cross_wave_delta_index_df,
        run_id,
    )
    v554_handoff_index_df = _build_v553_v554_handoff_index(
        report,
        temporal_pressure_field_df,
        temporal_gap_and_absence_index_df,
        run_id,
    )
    forbidden_inference_audit_df = _build_v553_forbidden_inference_audit(run_id)
    source_wave_anchor_manifest_df = wave_anchor_index_df.copy()
    temporal_anchor_index_df = _build_temporal_anchor_index(source_wave_anchor_manifest_df, run_id)
    interpolation_policy_ledger_df = _build_interpolation_policy_ledger(report, pressure_df, allow_interpolation, run_id)
    rupture_event_slot_ledger_df = _build_rupture_event_slot_ledger(report, run_id)
    cohort_window_requirement_index_df = _build_cohort_window_requirement_index(report, run_id)
    absence_noncomparability_register_df = _build_absence_noncomparability_register(
        report,
        pressure_df,
        country_year_pressure_df,
        allow_interpolation,
        run_id,
    )
    interpolation_manifest_df = _build_interpolation_manifest(country_year_pressure_df, run_id, allow_interpolation=allow_interpolation)
    event_override_manifest_df = _build_event_override_manifest(report, run_id)
    temporal_authority_ledger_df = _build_temporal_authority_ledger(
        report,
        temporal_pressure_observation_index_df,
        temporal_gap_and_absence_index_df,
        run_id,
    )
    comparability_audit_df = _build_comparability_audit(report, run_id)
    noncomparability_audit_df = pd.DataFrame(report.get("cross_wave_noncomparability_matrix", []))
    rupture_block_audit_df = _build_rupture_block_audit(report, country_year_pressure_df, run_id)
    downstream_v554_handoff_index_df = _build_downstream_v554_handoff_index(report, country_year_pressure_df, run_id)

    pressure_path = root["packets"] / "v553_temporal_pressure_field.parquet"
    pressure_packet_path = root["packets"] / "v553_temporal_pressure_field_packet.json"
    year_indexed_path = root["packets"] / "v553_year_indexed_pressure_over_time.parquet"
    interpolated_path = root["packets"] / "v553_interpolated_pressure_over_time.parquet"
    contradiction_path = root["packets"] / "v553_contradiction_over_time.parquet"
    absence_path = root["packets"] / "v553_pressure_absence_over_time.parquet"
    forbidden_path = root["audits"] / "v553_forbidden_actor_generation_audit.parquet"
    forbidden_inference_path = root["audits"] / "v553_forbidden_inference_audit.parquet"
    source_anchor_path = root["packets"] / "v553_source_wave_anchor_manifest.parquet"
    temporal_anchor_index_path = root["packets"] / "v553_temporal_anchor_index.parquet"
    harmonization_authority_index_path = root["audits"] / "v553_harmonization_authority_index.parquet"
    wave_anchor_index_path = root["packets"] / "v553_wave_anchor_index.parquet"
    temporal_key_candidate_index_path = root["packets"] / "v553_temporal_key_candidate_index.parquet"
    temporal_key_blocker_index_path = root["packets"] / "v553_temporal_key_blocker_index.parquet"
    harmonized_pressure_key_index_path = root["packets"] / "v553_harmonized_pressure_key_index.parquet"
    structural_dimension_resolution_audit_path = root["audits"] / "v553_structural_dimension_resolution_audit.parquet"
    temporal_pressure_observation_index_path = root["packets"] / "v553_temporal_pressure_observation_index.parquet"
    cross_wave_delta_index_path = root["packets"] / "v553_cross_wave_delta_index.parquet"
    interpolation_segment_index_path = root["packets"] / "v553_interpolation_segment_index.parquet"
    temporal_gap_and_absence_index_path = root["packets"] / "v553_temporal_gap_and_absence_index.parquet"
    structural_rupture_candidate_index_path = root["packets"] / "v553_structural_rupture_candidate_index.parquet"
    country_year_path = root["packets"] / "v553_country_year_pressure_field.parquet"
    pressure_component_path = root["packets"] / "v553_pressure_component_breakdown.parquet"
    harmonization_difference_ledger_path = root["audits"] / "v553_harmonization_difference_ledger.parquet"
    pressure_basis_ledger_path = root["audits"] / "v553_pressure_basis_ledger.parquet"
    confidence_penalty_ledger_path = root["audits"] / "v553_confidence_penalty_ledger.parquet"
    interpolation_policy_ledger_path = root["audits"] / "v553_interpolation_policy_ledger.parquet"
    rupture_event_slot_ledger_path = root["audits"] / "v553_rupture_event_slot_ledger.parquet"
    cohort_window_requirement_index_path = root["packets"] / "v553_cohort_window_requirement_index.parquet"
    absence_noncomparability_register_path = root["audits"] / "v553_absence_noncomparability_register.parquet"
    temporal_pressure_field_contract_path = root["packets"] / "v553_temporal_pressure_field.parquet"
    v554_handoff_index_path = root["packets"] / "v553_v554_handoff_index.parquet"
    interpolation_manifest_path = root["manifest"] / "v553_interpolation_manifest.json"
    event_override_manifest_path = root["manifest"] / "v553_event_override_manifest.json"
    temporal_authority_ledger_path = root["audits"] / "v553_temporal_authority_ledger.parquet"
    comparability_audit_path = root["audits"] / "v553_cross_wave_comparability_audit.parquet"
    noncomparability_audit_path = root["audits"] / "v553_cross_wave_noncomparability_audit.parquet"
    rupture_block_audit_path = root["audits"] / "v553_rupture_block_audit.parquet"
    downstream_handoff_path = root["packets"] / "v553_downstream_v554_handoff_index.parquet"
    readiness_path = root["manifest"] / "v553_temporal_readiness_report.json"
    run_manifest_path = root["manifest"] / "v553_run_manifest.parquet"
    artifact_paths_for_manifest = {
        "pressure_path": repo_relative_path_text(pressure_path),
        "year_indexed_path": repo_relative_path_text(year_indexed_path),
        "interpolated_path": repo_relative_path_text(interpolated_path),
        "contradiction_path": repo_relative_path_text(contradiction_path),
        "absence_path": repo_relative_path_text(absence_path),
        "wave_anchor_index_path": repo_relative_path_text(wave_anchor_index_path),
        "temporal_key_candidate_index_path": repo_relative_path_text(temporal_key_candidate_index_path),
        "temporal_key_blocker_index_path": repo_relative_path_text(temporal_key_blocker_index_path),
        "structural_dimension_resolution_audit_path": repo_relative_path_text(structural_dimension_resolution_audit_path),
        "harmonized_pressure_key_index_path": repo_relative_path_text(harmonized_pressure_key_index_path),
        "temporal_pressure_observation_index_path": repo_relative_path_text(temporal_pressure_observation_index_path),
        "cross_wave_delta_index_path": repo_relative_path_text(cross_wave_delta_index_path),
        "interpolation_segment_index_path": repo_relative_path_text(interpolation_segment_index_path),
        "temporal_gap_and_absence_index_path": repo_relative_path_text(temporal_gap_and_absence_index_path),
        "structural_rupture_candidate_index_path": repo_relative_path_text(structural_rupture_candidate_index_path),
        "temporal_pressure_field_path": repo_relative_path_text(temporal_pressure_field_contract_path),
        "v554_handoff_index_path": repo_relative_path_text(v554_handoff_index_path),
        "forbidden_inference_audit_path": repo_relative_path_text(forbidden_inference_path),
        "source_wave_anchor_manifest_path": repo_relative_path_text(source_anchor_path),
        "v553_wave_harmonization_table_path": repo_relative_path_text(Path(_clean(report.get("wave_harmonization_table_path")) or str(root["root"] / "v553_wave_harmonization" / "v553_wave_harmonization_table.parquet"))),
        "harmonization_difference_ledger_path": repo_relative_path_text(harmonization_difference_ledger_path),
        "temporal_anchor_index_path": repo_relative_path_text(temporal_anchor_index_path),
        "harmonization_authority_index_path": repo_relative_path_text(harmonization_authority_index_path),
        "country_year_pressure_field_path": repo_relative_path_text(country_year_path),
        "pressure_component_breakdown_path": repo_relative_path_text(pressure_component_path),
        "pressure_basis_ledger_path": repo_relative_path_text(pressure_basis_ledger_path),
        "confidence_penalty_ledger_path": repo_relative_path_text(confidence_penalty_ledger_path),
        "interpolation_policy_ledger_path": repo_relative_path_text(interpolation_policy_ledger_path),
        "rupture_event_slot_ledger_path": repo_relative_path_text(rupture_event_slot_ledger_path),
        "cohort_window_requirement_index_path": repo_relative_path_text(cohort_window_requirement_index_path),
        "absence_noncomparability_register_path": repo_relative_path_text(absence_noncomparability_register_path),
        "temporal_authority_ledger_path": repo_relative_path_text(temporal_authority_ledger_path),
        "comparability_audit_path": repo_relative_path_text(comparability_audit_path),
        "noncomparability_audit_path": repo_relative_path_text(noncomparability_audit_path),
        "rupture_block_audit_path": repo_relative_path_text(rupture_block_audit_path),
        "downstream_v554_handoff_index_path": repo_relative_path_text(downstream_handoff_path),
    }
    artifact_row_counts_for_manifest = {
        "pressure_rows": int(len(pressure_df)),
        "year_indexed_rows": int(len(pressure_df)),
        "interpolated_rows": int(len(interpolated_pressure_df)),
        "contradiction_rows": int(len(contradiction_df)),
        "absence_rows": int(len(absence_df)),
        "wave_anchor_index_rows": int(len(wave_anchor_index_df)),
        "harmonization_difference_ledger_rows": int(len(harmonization_difference_ledger_df)),
        "temporal_key_candidate_index_rows": int(len(temporal_key_candidate_index_df)),
        "temporal_key_blocker_index_rows": int(len(temporal_key_blocker_index_df)),
        "structural_dimension_resolution_audit_rows": int(len(structural_dimension_resolution_audit_df)),
        "harmonized_pressure_key_index_rows": int(len(harmonized_pressure_key_index_df)),
        "temporal_pressure_observation_index_rows": int(len(temporal_pressure_observation_index_df)),
        "cross_wave_delta_index_rows": int(len(cross_wave_delta_index_df)),
        "interpolation_segment_index_rows": int(len(interpolation_segment_index_df)),
        "temporal_gap_and_absence_index_rows": int(len(temporal_gap_and_absence_index_df)),
        "structural_rupture_candidate_index_rows": int(len(structural_rupture_candidate_index_df)),
        "temporal_pressure_field_rows": int(len(temporal_pressure_field_df)),
        "v554_handoff_index_rows": int(len(v554_handoff_index_df)),
        "forbidden_inference_audit_rows": int(len(forbidden_inference_audit_df)),
        "country_year_pressure_field_rows": int(len(country_year_pressure_df)),
        "pressure_component_breakdown_rows": int(len(pressure_component_breakdown_df)),
        "pressure_basis_ledger_rows": int(len(pressure_basis_ledger_df)),
        "confidence_penalty_ledger_rows": int(len(confidence_penalty_ledger_df)),
        "interpolation_policy_ledger_rows": int(len(interpolation_policy_ledger_df)),
        "rupture_event_slot_ledger_rows": int(len(rupture_event_slot_ledger_df)),
        "cohort_window_requirement_index_rows": int(len(cohort_window_requirement_index_df)),
        "absence_noncomparability_register_rows": int(len(absence_noncomparability_register_df)),
        "temporal_authority_ledger_rows": int(len(temporal_authority_ledger_df)),
        "comparability_audit_rows": int(len(comparability_audit_df)),
        "noncomparability_audit_rows": int(len(noncomparability_audit_df)),
        "rupture_block_audit_rows": int(len(rupture_block_audit_df)),
        "downstream_v554_handoff_index_rows": int(len(downstream_v554_handoff_index_df)),
    }
    input_status = "ready_for_probe" if report.get("ready_for_v553") else "blocked"
    v552j_readiness_status = str(report.get("v552j_readiness_status", "")).strip()
    v552j_readiness_status_counts = report.get("v552j_readiness_status_counts", {}) or {}
    v552j_handoff_authority_status_counts = report.get("v552j_handoff_authority_status_counts", {}) or {}
    if not v552j_readiness_status:
        if isinstance(v552j_readiness_status_counts, dict) and len(v552j_readiness_status_counts) == 1:
            v552j_readiness_status = next(iter(v552j_readiness_status_counts.keys()))
        elif isinstance(v552j_readiness_status_counts, dict) and len(v552j_readiness_status_counts) > 1:
            v552j_readiness_status = "MIXED"
        else:
            v552j_readiness_status = "UNKNOWN"
    v552j_blocker_context_count = _int(report.get("v552j_blocker_context_count", 0))
    v552j_handoff_authority_status = str(report.get("v552j_handoff_authority_status", "")).strip()
    if not v552j_handoff_authority_status:
        if isinstance(v552j_handoff_authority_status_counts, dict) and len(v552j_handoff_authority_status_counts) == 1:
            v552j_handoff_authority_status = next(iter(v552j_handoff_authority_status_counts.keys()))
        elif isinstance(v552j_handoff_authority_status_counts, dict) and len(v552j_handoff_authority_status_counts) > 1:
            v552j_handoff_authority_status = "MIXED"
        else:
            v552j_handoff_authority_status = "UNKNOWN"
    authorized_key_count = int(harmonized_pressure_key_index_df.get("multi_wave_authorization_status", pd.Series(dtype=str)).astype(str).eq(AUTHORIZED_SPARSE_TEMPORAL_KEY).sum()) if not harmonized_pressure_key_index_df.empty else 0
    probe_key_count = int(harmonized_pressure_key_index_df.get("multi_wave_authorization_status", pd.Series(dtype=str)).astype(str).eq(PROBE_ONLY_TEMPORAL_KEY).sum()) if not harmonized_pressure_key_index_df.empty else 0
    blocked_key_count = int(harmonized_pressure_key_index_df.get("multi_wave_authorization_status", pd.Series(dtype=str)).astype(str).eq(BLOCKED_TEMPORAL_KEY).sum()) if not harmonized_pressure_key_index_df.empty else 0
    authorized_anchor_count = int(temporal_pressure_observation_index_df.get("temporal_status", pd.Series(dtype=str)).astype(str).eq("observed_authorized_anchor").sum()) if not temporal_pressure_observation_index_df.empty else 0
    probe_anchor_count = int(temporal_pressure_observation_index_df.get("temporal_status", pd.Series(dtype=str)).astype(str).eq("probe_only_anchor").sum()) if not temporal_pressure_observation_index_df.empty else 0
    unknown_gap_count = int(len(temporal_gap_and_absence_index_df))
    v554_ready_key_count = int(v554_handoff_index_df.get("ready_for_v554_seed_affordance", pd.Series(dtype=bool)).astype(bool).sum()) if not v554_handoff_index_df.empty else 0
    if not report or not harmonization_evidence_exists or int(report.get("wave_count", 0) or 0) == 0:
        status = "BLOCKED_V553_TEMPORAL_PRESSURE_FIELD"
        input_status = "blocked"
    elif authorized_key_count > 0:
        status = "READY_V553_SPARSE_TEMPORAL_FIELD"
    elif probe_key_count > 0:
        status = "PARTIAL_READY_V553_PROBE_ONLY"
    else:
        status = "BLOCKED_V553_TEMPORAL_PRESSURE_FIELD"
        input_status = "blocked"
    if status == "BLOCKED_V553_TEMPORAL_PRESSURE_FIELD":
        v554_ready_key_count = 0
    authority_summary = {
        "required_authority_kinds": list(report.get("required_authority_kinds", [])),
        "required_shared_structure": list(report.get("required_shared_structure", [])),
        "blocking_conditions": list(report.get("blocking_conditions", [])),
        "wave_count": int(report.get("wave_count", 0) or 0),
        "multiple_waves_present": bool(report.get("multiple_waves_present", False)),
        "wave_pair_count": int(report.get("wave_pair_count", 0) or 0),
        "shared_semantic_column_count": len(report.get("shared_semantic_columns", []) or []),
        "shared_directionality_column_count": len(report.get("shared_directionality_columns", []) or []),
        "shared_position_column_count": len(report.get("shared_position_columns", []) or []),
        "v552j_readiness_status": v552j_readiness_status,
        "v552j_blocker_context_count": v552j_blocker_context_count,
        "v552j_handoff_authority_status": v552j_handoff_authority_status,
        "v552j_readiness_status_counts": v552j_readiness_status_counts,
        "v552j_handoff_authority_status_counts": v552j_handoff_authority_status_counts,
    }
    temporal_slots = {
        "requires_event_context": False,
        "event_context_status": "not_supplied",
        "event_authority_ref": "",
        "rupture_override_status": "reserved_not_filled",
        "cohort_window_requirements": [
            "birth_cohort_window",
            "parent_formative_window",
            "child_developmental_window",
            "household_period_window",
        ],
        "cohort_window_status": "reserved_not_filled",
    }
    readiness_score = _bounded_score(float(report.get("harmonization_score", 0.0) or 0.0))
    wave_coverage_score = _bounded_score(1.0 if int(report.get("wave_count", 0) or 0) >= 2 else 0.0)
    shared_semantic_score = _bounded_score(float(report.get("shared_semantic_score", 0.0) or 0.0))
    shared_directionality_score = _bounded_score(float(report.get("shared_directionality_score", 0.0) or 0.0))
    shared_position_score = _bounded_score(float(report.get("shared_position_score", 0.0) or 0.0))
    overlay_presence_score = _bounded_score(float(report.get("overlay_presence_score", 0.0) or 0.0))
    harmonization_score = _bounded_score(float(report.get("harmonization_score", 0.0) or 0.0))
    harmonization_authority_index_df = _build_harmonization_authority_index(report, harmonization_score, run_id)

    wave_anchor_index_info = write_frame_artifact(
        wave_anchor_index_df,
        path=wave_anchor_index_path,
        schema_path=root["schemas"] / "v553_wave_anchor_index.schema.json",
        name="v553_wave_anchor_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    temporal_key_candidate_index_info = write_frame_artifact(
        temporal_key_candidate_index_df,
        path=temporal_key_candidate_index_path,
        schema_path=root["schemas"] / "v553_temporal_key_candidate_index.schema.json",
        name="v553_temporal_key_candidate_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    temporal_key_blocker_index_info = write_frame_artifact(
        temporal_key_blocker_index_df,
        path=temporal_key_blocker_index_path,
        schema_path=root["schemas"] / "v553_temporal_key_blocker_index.schema.json",
        name="v553_temporal_key_blocker_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    structural_dimension_resolution_audit_info = write_frame_artifact(
        structural_dimension_resolution_audit_df,
        path=structural_dimension_resolution_audit_path,
        schema_path=root["schemas"] / "v553_structural_dimension_resolution_audit.schema.json",
        name="v553_structural_dimension_resolution_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    harmonized_pressure_key_index_info = write_frame_artifact(
        harmonized_pressure_key_index_df,
        path=harmonized_pressure_key_index_path,
        schema_path=root["schemas"] / "v553_harmonized_pressure_key_index.schema.json",
        name="v553_harmonized_pressure_key_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    temporal_pressure_observation_index_info = write_frame_artifact(
        temporal_pressure_observation_index_df,
        path=temporal_pressure_observation_index_path,
        schema_path=root["schemas"] / "v553_temporal_pressure_observation_index.schema.json",
        name="v553_temporal_pressure_observation_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    cross_wave_delta_index_info = write_frame_artifact(
        cross_wave_delta_index_df,
        path=cross_wave_delta_index_path,
        schema_path=root["schemas"] / "v553_cross_wave_delta_index.schema.json",
        name="v553_cross_wave_delta_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    interpolation_segment_index_info = write_frame_artifact(
        interpolation_segment_index_df,
        path=interpolation_segment_index_path,
        schema_path=root["schemas"] / "v553_interpolation_segment_index.schema.json",
        name="v553_interpolation_segment_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    temporal_gap_and_absence_index_info = write_frame_artifact(
        temporal_gap_and_absence_index_df,
        path=temporal_gap_and_absence_index_path,
        schema_path=root["schemas"] / "v553_temporal_gap_and_absence_index.schema.json",
        name="v553_temporal_gap_and_absence_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    structural_rupture_candidate_index_info = write_frame_artifact(
        structural_rupture_candidate_index_df,
        path=structural_rupture_candidate_index_path,
        schema_path=root["schemas"] / "v553_structural_rupture_candidate_index.schema.json",
        name="v553_structural_rupture_candidate_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    pressure_info = write_frame_artifact(
        temporal_pressure_field_df,
        path=pressure_path,
        schema_path=root["schemas"] / "v553_temporal_pressure_field.schema.json",
        name="v553_temporal_pressure_field",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    year_indexed_info = write_frame_artifact(
        pressure_df,
        path=year_indexed_path,
        schema_path=root["schemas"] / "v553_year_indexed_pressure_over_time.schema.json",
        name="v553_year_indexed_pressure_over_time",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    interpolated_info = write_frame_artifact(
        interpolated_pressure_df,
        path=interpolated_path,
        schema_path=root["schemas"] / "v553_interpolated_pressure_over_time.schema.json",
        name="v553_interpolated_pressure_over_time",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    contradiction_info = write_frame_artifact(
        contradiction_df,
        path=contradiction_path,
        schema_path=root["schemas"] / "v553_contradiction_over_time.schema.json",
        name="v553_contradiction_over_time",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    absence_info = write_frame_artifact(
        absence_df,
        path=absence_path,
        schema_path=root["schemas"] / "v553_pressure_absence_over_time.schema.json",
        name="v553_pressure_absence_over_time",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    forbidden_info = write_frame_artifact(
        forbidden_inference_audit_df,
        path=forbidden_path,
        schema_path=root["schemas"] / "v553_forbidden_actor_generation_audit.schema.json",
        name="v553_forbidden_actor_generation_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    forbidden_inference_info = write_frame_artifact(
        forbidden_inference_audit_df,
        path=forbidden_inference_path,
        schema_path=root["schemas"] / "v553_forbidden_inference_audit.schema.json",
        name="v553_forbidden_inference_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    source_anchor_info = write_frame_artifact(
        source_wave_anchor_manifest_df,
        path=source_anchor_path,
        schema_path=root["schemas"] / "v553_source_wave_anchor_manifest.schema.json",
        name="v553_source_wave_anchor_manifest",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    temporal_anchor_index_info = write_frame_artifact(
        temporal_anchor_index_df,
        path=temporal_anchor_index_path,
        schema_path=root["schemas"] / "v553_temporal_anchor_index.schema.json",
        name="v553_temporal_anchor_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    v554_handoff_index_info = write_frame_artifact(
        v554_handoff_index_df,
        path=v554_handoff_index_path,
        schema_path=root["schemas"] / "v553_v554_handoff_index.schema.json",
        name="v553_v554_handoff_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    harmonization_authority_index_info = write_frame_artifact(
        harmonization_authority_index_df,
        path=harmonization_authority_index_path,
        schema_path=root["schemas"] / "v553_harmonization_authority_index.schema.json",
        name="v553_harmonization_authority_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    country_year_info = write_frame_artifact(
        country_year_pressure_df,
        path=country_year_path,
        schema_path=root["schemas"] / "v553_country_year_pressure_field.schema.json",
        name="v553_country_year_pressure_field",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    pressure_component_info = write_frame_artifact(
        pressure_component_breakdown_df,
        path=pressure_component_path,
        schema_path=root["schemas"] / "v553_pressure_component_breakdown.schema.json",
        name="v553_pressure_component_breakdown",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    harmonization_difference_ledger_info = write_frame_artifact(
        harmonization_difference_ledger_df,
        path=harmonization_difference_ledger_path,
        schema_path=root["schemas"] / "v553_harmonization_difference_ledger.schema.json",
        name="v553_harmonization_difference_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    pressure_basis_ledger_info = write_frame_artifact(
        pressure_basis_ledger_df,
        path=pressure_basis_ledger_path,
        schema_path=root["schemas"] / "v553_pressure_basis_ledger.schema.json",
        name="v553_pressure_basis_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    confidence_penalty_ledger_info = write_frame_artifact(
        confidence_penalty_ledger_df,
        path=confidence_penalty_ledger_path,
        schema_path=root["schemas"] / "v553_confidence_penalty_ledger.schema.json",
        name="v553_confidence_penalty_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    interpolation_policy_ledger_info = write_frame_artifact(
        interpolation_policy_ledger_df,
        path=interpolation_policy_ledger_path,
        schema_path=root["schemas"] / "v553_interpolation_policy_ledger.schema.json",
        name="v553_interpolation_policy_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    rupture_event_slot_ledger_info = write_frame_artifact(
        rupture_event_slot_ledger_df,
        path=rupture_event_slot_ledger_path,
        schema_path=root["schemas"] / "v553_rupture_event_slot_ledger.schema.json",
        name="v553_rupture_event_slot_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    cohort_window_requirement_index_info = write_frame_artifact(
        cohort_window_requirement_index_df,
        path=cohort_window_requirement_index_path,
        schema_path=root["schemas"] / "v553_cohort_window_requirement_index.schema.json",
        name="v553_cohort_window_requirement_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    absence_noncomparability_register_info = write_frame_artifact(
        absence_noncomparability_register_df,
        path=absence_noncomparability_register_path,
        schema_path=root["schemas"] / "v553_absence_noncomparability_register.schema.json",
        name="v553_absence_noncomparability_register",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    interpolation_manifest_df.to_json(interpolation_manifest_path, orient="records", indent=2)
    event_override_manifest_df.to_json(event_override_manifest_path, orient="records", indent=2)
    temporal_authority_info = write_frame_artifact(
        temporal_authority_ledger_df,
        path=temporal_authority_ledger_path,
        schema_path=root["schemas"] / "v553_temporal_authority_ledger.schema.json",
        name="v553_temporal_authority_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    comparability_info = write_frame_artifact(
        comparability_audit_df,
        path=comparability_audit_path,
        schema_path=root["schemas"] / "v553_comparability_audit.schema.json",
        name="v553_cross_wave_comparability_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    noncomparability_info = write_frame_artifact(
        noncomparability_audit_df,
        path=noncomparability_audit_path,
        schema_path=root["schemas"] / "v553_cross_wave_noncomparability_audit.schema.json",
        name="v553_cross_wave_noncomparability_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    rupture_block_info = write_frame_artifact(
        rupture_block_audit_df,
        path=rupture_block_audit_path,
        schema_path=root["schemas"] / "v553_rupture_block_audit.schema.json",
        name="v553_rupture_block_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    downstream_handoff_info = write_frame_artifact(
        downstream_v554_handoff_index_df,
        path=downstream_handoff_path,
        schema_path=root["schemas"] / "v553_downstream_v554_handoff_index.schema.json",
        name="v553_downstream_v554_handoff_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    run_manifest_df = _build_v553_run_manifest(
        run_id=run_id,
        report=report,
        readiness={
            "status": status,
            "blocked_rows": int(country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str).str.startswith("blocked_").sum()) if not country_year_pressure_df.empty else 0,
            "review_required_rows": int((country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str) != "anchor_derived").sum()) if not country_year_pressure_df.empty else 0,
            "v552j_blocker_context_count": v552j_blocker_context_count,
        },
        artifact_paths=artifact_paths_for_manifest,
        artifact_row_counts=artifact_row_counts_for_manifest,
    )
    run_manifest_info = write_frame_artifact(
        run_manifest_df,
        path=run_manifest_path,
        schema_path=root["schemas"] / "v553_run_manifest.schema.json",
        name="v553_run_manifest",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_json_artifact(
        pressure_packet_path,
        {
            "run_id": run_id,
            "layer": "v553",
            "artifact_type": "v553_temporal_pressure_field_packet",
            "status": status,
            "ready_for_v554": bool(v554_ready_key_count > 0),
            "temporal_field_authority": "sparse_multi_wave_authorized" if status == "READY_V553_SPARSE_TEMPORAL_FIELD" else "not_authorized",
            "repo_harmonization_authority": _clean(report.get("comparison_authority_status")) or "",
            "authorized_temporal_key_count": authorized_key_count,
            "probe_temporal_key_count": probe_key_count,
            "blocked_temporal_key_count": blocked_key_count,
            "authorized_observed_anchor_count": authorized_anchor_count,
            "probe_anchor_count": probe_anchor_count,
            "unknown_gap_count": unknown_gap_count,
            "v554_ready_key_count": v554_ready_key_count,
            "pressure_field_rows": int(len(temporal_pressure_field_df)),
            "country_year_rows": int(len(country_year_pressure_df)),
            "interpolated_pressure_rows": int(len(interpolated_pressure_df)),
            "contradiction_rows": int(len(contradiction_df)),
            "absence_rows": int(len(absence_df)),
            "blocked_rows": int(country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str).str.startswith("blocked_").sum()) if not country_year_pressure_df.empty else 0,
            "review_required_rows": int((country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str) != "anchor_derived").sum()) if not country_year_pressure_df.empty else 0,
            "packet_source": repo_relative_path_text(pressure_path),
            "interpolated_source": repo_relative_path_text(interpolated_path),
            "created_at": utc_now(),
            "schema_version": V553_SCHEMA_VERSION,
            "compiler_version": V553_COMPILER_VERSION,
            "payload_summary": {
                "multiple_waves_present": bool(report.get("multiple_waves_present", False)),
                "wave_count": int(report.get("wave_count", 0) or 0),
                "ready_for_v553": bool(report.get("ready_for_v553", False)),
                "readiness_score": readiness_score,
                "wave_coverage_score": wave_coverage_score,
                "shared_semantic_score": shared_semantic_score,
                "shared_directionality_score": shared_directionality_score,
                "shared_position_score": shared_position_score,
                "overlay_presence_score": overlay_presence_score,
                "harmonization_score": harmonization_score,
                "v552j_readiness_status": v552j_readiness_status,
                "v552j_blocker_context_count": v552j_blocker_context_count,
                "allow_interpolation": bool(allow_interpolation),
                "authorized_temporal_key_count": authorized_key_count,
                "probe_temporal_key_count": probe_key_count,
                "blocked_temporal_key_count": blocked_key_count,
                "authorized_observed_anchor_count": authorized_anchor_count,
                "probe_anchor_count": probe_anchor_count,
                "unknown_gap_count": unknown_gap_count,
                "v554_ready_key_count": v554_ready_key_count,
                "harmonization_evidence_count": int(report.get("wave_pair_count", 0) or 0),
                "harmonization_evidence_path": harmonization_evidence_path,
                "harmonization_evidence_row_count": harmonization_evidence_row_count,
                "authority_summary": authority_summary,
                "temporal_slots": temporal_slots,
            },
        },
    )

    build_record_status = "THIN_READY" if status.startswith("READY") else ("THIN_READY_WITH_GAPS" if status.startswith("PARTIAL") else "THIN_BLOCKED_MISSING_REQUIRED_INPUT")
    build_record = build_layer_build_record(
        spec=type("Spec", (), {"layer": "v553", "title": "Temporal pressure field", "artifact_slug": "v553_temporal_pressure_field"})(),
        input_inspection={
            "input_root": repo_relative_path_text(Path(wave_harmonization_report_path).parent),
            "files": [
                {"relative_path": repo_relative_path_text(wave_harmonization_report_path), "exists": True},
                {"relative_path": repo_relative_path_text(harmonization_evidence_path), "exists": Path(harmonization_evidence_path).exists()},
            ],
            "missing_required_inputs": [] if report else ["wave_harmonization_report"],
            "stop_missing_inputs": [],
            "input_status": input_status,
        },
        status=build_record_status,
        packet_path=repo_relative_path_text(pressure_path),
        schema_path=repo_relative_path_text(root["schemas"] / "v553_temporal_pressure_field.schema.json"),
        audit_path=repo_relative_path_text(forbidden_path),
        readiness_path=repo_relative_path_text(readiness_path),
        input_manifest_path=repo_relative_path_text(root["manifest"] / "v553_temporal_input_manifest.json"),
        run_id=run_id,
    )
    build_record.update(provenance)

    readiness = {
        "run_id": run_id,
        "source": _report_source(report),
        "source_family": _report_source(report),
        "country_code": _report_country(report),
        "status": status,
        "v553_status": status,
        "explicit_run_authority_source": "v552j_handoff",
        "repo_harmonization_authority": _clean(report.get("comparison_authority_status")) or "",
        "temporal_field_authority": "sparse_multi_wave_authorized" if status == "READY_V553_SPARSE_TEMPORAL_FIELD" else "not_authorized",
        "ready_for_v554": bool(v554_ready_key_count > 0),
        "multiple_waves_present": bool(report.get("multiple_waves_present", False)),
        "wave_count": int(report.get("wave_count", 0) or 0),
        "v552j_readiness_status": v552j_readiness_status,
        "v552j_readiness_status_counts": v552j_readiness_status_counts,
        "v552j_handoff_authority_status": v552j_handoff_authority_status,
        "v552j_handoff_authority_status_counts": v552j_handoff_authority_status_counts,
        "v552j_blocker_context_count": v552j_blocker_context_count,
        "readiness_score": readiness_score,
        "wave_coverage_score": wave_coverage_score,
        "shared_semantic_score": shared_semantic_score,
        "shared_directionality_score": shared_directionality_score,
        "shared_position_score": shared_position_score,
        "overlay_presence_score": overlay_presence_score,
        "harmonization_score": harmonization_score,
        "authority_summary": authority_summary,
        "harmonization_evidence_count": int(report.get("wave_pair_count", 0) or 0),
        "harmonization_evidence_path": repo_relative_path_text(harmonization_evidence_path),
        "harmonization_evidence_row_count": harmonization_evidence_row_count,
        "harmonization_sidecar": harmonization_sidecar,
        "upstream_requirements": {
            "required_report": "v553_wave_harmonization_report.json",
            "required_report_fields": [
                "ready_for_v553",
                "wave_count",
                "shared_semantic_columns",
                "shared_directionality_columns",
                "shared_position_columns",
                "wave_pair_evidence_path",
            ],
            "required_authority_kinds": list(report.get("required_authority_kinds", [])),
            "blocking_conditions": list(report.get("blocking_conditions", [])),
            "harmonization_evidence_exists": harmonization_evidence_exists,
            "harmonization_evidence_row_count": harmonization_evidence_row_count,
        },
        "temporal_slots": temporal_slots,
        "downstream_expectations": {
            "v554_requires": [
                "v553_temporal_pressure_field_packet.json",
                "v553_year_indexed_pressure_over_time.parquet",
                "v553_interpolated_pressure_over_time.parquet",
            ],
            "v554_must_not_require": [
                "persona_seed",
                "life_event_story",
                "runtime_personality",
            ],
        },
        "pressure_field_rows": int(len(temporal_pressure_field_df)),
        "country_year_rows": int(len(country_year_pressure_df)),
        "interpolated_pressure_rows": int(len(interpolated_pressure_df)),
        "contradiction_rows": int(len(contradiction_df)),
        "absence_rows": int(len(absence_df)),
        "authorized_temporal_key_count": authorized_key_count,
        "probe_temporal_key_count": probe_key_count,
        "blocked_temporal_key_count": blocked_key_count,
        "authorized_observed_anchor_count": authorized_anchor_count,
        "probe_anchor_count": probe_anchor_count,
        "unknown_gap_count": unknown_gap_count,
        "v554_ready_key_count": v554_ready_key_count,
        "blocked_rows": int(country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str).str.startswith("blocked_").sum()) if not country_year_pressure_df.empty else 0,
        "review_required_rows": int((country_year_pressure_df.get("pressure_status", pd.Series(dtype=str)).astype(str) != "anchor_derived").sum()) if not country_year_pressure_df.empty else 0,
        "interpolation_allowed": bool(allow_interpolation),
        "input_status": input_status,
        "missing_required_inputs_json": json.dumps([] if report else ["wave_harmonization_report"], sort_keys=True),
        "created_at": utc_now(),
        "schema_version": V553_SCHEMA_VERSION,
        "compiler_version": V553_COMPILER_VERSION,
        **provenance,
        "readiness_score": readiness_score,
        "packet_path": repo_relative_path_text(pressure_packet_path),
        "pressure_field_path": repo_relative_path_text(pressure_path) if write_parquet else "",
        "year_indexed_pressure_path": repo_relative_path_text(year_indexed_path) if write_parquet else "",
        "interpolated_pressure_path": repo_relative_path_text(interpolated_path) if write_parquet else "",
        "contradiction_path": repo_relative_path_text(contradiction_path) if write_parquet else "",
        "absence_path": repo_relative_path_text(absence_path) if write_parquet else "",
        "forbidden_audit_path": repo_relative_path_text(forbidden_path) if write_parquet else "",
        "v553_wave_anchor_index_path": repo_relative_path_text(wave_anchor_index_path),
        "temporal_key_candidate_index_path": repo_relative_path_text(temporal_key_candidate_index_path),
        "temporal_key_blocker_index_path": repo_relative_path_text(temporal_key_blocker_index_path),
        "structural_dimension_resolution_audit_path": repo_relative_path_text(structural_dimension_resolution_audit_path),
        "v553_harmonized_pressure_key_index_path": repo_relative_path_text(harmonized_pressure_key_index_path),
        "v553_temporal_pressure_observation_index_path": repo_relative_path_text(temporal_pressure_observation_index_path),
        "v553_cross_wave_delta_index_path": repo_relative_path_text(cross_wave_delta_index_path),
        "v553_interpolation_segment_index_path": repo_relative_path_text(interpolation_segment_index_path),
        "v553_temporal_gap_and_absence_index_path": repo_relative_path_text(temporal_gap_and_absence_index_path),
        "v553_structural_rupture_candidate_index_path": repo_relative_path_text(structural_rupture_candidate_index_path),
        "v553_temporal_pressure_field_path": repo_relative_path_text(temporal_pressure_field_contract_path),
        "v553_v554_handoff_index_path": repo_relative_path_text(v554_handoff_index_path),
        "v553_forbidden_inference_audit_path": repo_relative_path_text(forbidden_inference_path),
        "v553_wave_harmonization_table_path": repo_relative_path_text(Path(_clean(report.get("wave_harmonization_table_path")) or str(root["root"] / "v553_wave_harmonization" / "v553_wave_harmonization_table.parquet"))),
        "v553_harmonization_difference_ledger_path": repo_relative_path_text(harmonization_difference_ledger_path),
        "v553_pressure_basis_ledger_path": repo_relative_path_text(pressure_basis_ledger_path),
        "v553_confidence_penalty_ledger_path": repo_relative_path_text(confidence_penalty_ledger_path),
        "v553_run_manifest_path": repo_relative_path_text(run_manifest_path),
        "build_record": build_record,
        "pressure_artifact_info": pressure_info,
        "year_indexed_artifact_info": year_indexed_info,
        "interpolated_artifact_info": interpolated_info,
        "contradiction_artifact_info": contradiction_info,
        "absence_artifact_info": absence_info,
        "forbidden_artifact_info": forbidden_info,
        "v553_wave_anchor_index_artifact_info": wave_anchor_index_info,
        "temporal_key_candidate_index_artifact_info": temporal_key_candidate_index_info,
        "temporal_key_blocker_index_artifact_info": temporal_key_blocker_index_info,
        "v553_harmonized_pressure_key_index_artifact_info": harmonized_pressure_key_index_info,
        "v553_temporal_pressure_observation_index_artifact_info": temporal_pressure_observation_index_info,
        "v553_cross_wave_delta_index_artifact_info": cross_wave_delta_index_info,
        "v553_interpolation_segment_index_artifact_info": interpolation_segment_index_info,
        "v553_temporal_gap_and_absence_index_artifact_info": temporal_gap_and_absence_index_info,
        "v553_structural_rupture_candidate_index_artifact_info": structural_rupture_candidate_index_info,
        "v553_temporal_pressure_field_artifact_info": pressure_info,
        "v553_v554_handoff_index_artifact_info": v554_handoff_index_info,
        "v553_forbidden_inference_audit_artifact_info": forbidden_inference_info,
        "v553_harmonization_difference_ledger_artifact_info": harmonization_difference_ledger_info,
        "v553_pressure_basis_ledger_artifact_info": pressure_basis_ledger_info,
        "v553_confidence_penalty_ledger_artifact_info": confidence_penalty_ledger_info,
        "v553_run_manifest_artifact_info": run_manifest_info,
        "source_anchor_artifact_info": source_anchor_info,
        "temporal_anchor_index_artifact_info": temporal_anchor_index_info,
        "harmonization_authority_index_artifact_info": harmonization_authority_index_info,
        "country_year_artifact_info": country_year_info,
        "pressure_component_artifact_info": pressure_component_info,
        "interpolation_policy_ledger_artifact_info": interpolation_policy_ledger_info,
        "rupture_event_slot_ledger_artifact_info": rupture_event_slot_ledger_info,
        "cohort_window_requirement_index_artifact_info": cohort_window_requirement_index_info,
        "absence_noncomparability_register_artifact_info": absence_noncomparability_register_info,
        "temporal_authority_artifact_info": temporal_authority_info,
        "comparability_artifact_info": comparability_info,
        "noncomparability_artifact_info": noncomparability_info,
        "rupture_block_artifact_info": rupture_block_info,
        "downstream_handoff_artifact_info": downstream_handoff_info,
        "run_manifest_artifact_info": run_manifest_info,
        "interpolation_manifest_path": repo_relative_path_text(interpolation_manifest_path),
        "event_override_manifest_path": repo_relative_path_text(event_override_manifest_path),
        "source_wave_anchor_manifest_path": repo_relative_path_text(source_anchor_path),
        "temporal_anchor_index_path": repo_relative_path_text(temporal_anchor_index_path),
        "harmonization_authority_index_path": repo_relative_path_text(harmonization_authority_index_path),
        "country_year_pressure_field_path": repo_relative_path_text(country_year_path),
        "pressure_component_breakdown_path": repo_relative_path_text(pressure_component_path),
        "harmonization_difference_ledger_path": repo_relative_path_text(harmonization_difference_ledger_path),
        "pressure_basis_ledger_path": repo_relative_path_text(pressure_basis_ledger_path),
        "confidence_penalty_ledger_path": repo_relative_path_text(confidence_penalty_ledger_path),
        "interpolation_policy_ledger_path": repo_relative_path_text(interpolation_policy_ledger_path),
        "rupture_event_slot_ledger_path": repo_relative_path_text(rupture_event_slot_ledger_path),
        "cohort_window_requirement_index_path": repo_relative_path_text(cohort_window_requirement_index_path),
        "absence_noncomparability_register_path": repo_relative_path_text(absence_noncomparability_register_path),
        "temporal_authority_ledger_path": repo_relative_path_text(temporal_authority_ledger_path),
        "comparability_audit_path": repo_relative_path_text(comparability_audit_path),
        "noncomparability_audit_path": repo_relative_path_text(noncomparability_audit_path),
        "rupture_block_audit_path": repo_relative_path_text(rupture_block_audit_path),
        "downstream_v554_handoff_index_path": repo_relative_path_text(downstream_handoff_path),
        "v553_run_manifest_path": repo_relative_path_text(run_manifest_path),
        "ready_for_runtime_consumption": False,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "allow_interpolation": bool(allow_interpolation),
    }
    write_json_artifact(readiness_path, readiness)
    write_json_artifact(
        root["manifest"] / "v553_temporal_input_manifest.json",
        {
            "run_id": run_id,
            "wave_harmonization_report_path": repo_relative_path_text(wave_harmonization_report_path),
            "input_scope_mode": "explicit_v552j_handoff",
            "explicit_wave_set": sorted({
                _clean(item.get("wave"))
                for item in (report.get("wave_rows", []) or [])
                if isinstance(item, dict) and _clean(item.get("wave"))
            }),
            "authoritative_input_kind": "v552j_to_v553_handoff_index",
            "wave_harmonization_scope_mode": "multi_wave_authority_input",
            "wave_harmonization_report_authority": _clean(report.get("comparison_authority_status")) or "",
            "wave_count": int(report.get("wave_count", 0) or 0),
            "created_at": utc_now(),
            **provenance,
        },
    )
    _write_v553_semantic_implementation_report(
        report_path=Path(__file__).resolve().parents[2] / "docs/architecture_control/reports/PASS_7_V553_SEMANTIC_IMPLEMENTATION_REPORT.md",
        run_id=run_id,
        wave_harmonization_report_path=wave_harmonization_report_path,
        readiness=readiness,
        wave_anchor_index_df=wave_anchor_index_df,
        harmonized_pressure_key_index_df=harmonized_pressure_key_index_df,
        temporal_pressure_observation_index_df=temporal_pressure_observation_index_df,
        cross_wave_delta_index_df=cross_wave_delta_index_df,
        interpolation_segment_index_df=interpolation_segment_index_df,
        temporal_gap_and_absence_index_df=temporal_gap_and_absence_index_df,
        structural_rupture_candidate_index_df=structural_rupture_candidate_index_df,
        temporal_pressure_field_df=temporal_pressure_field_df,
        v554_handoff_index_df=v554_handoff_index_df,
        forbidden_inference_audit_df=forbidden_inference_audit_df,
        harmonization_authority_index_df=harmonization_authority_index_df,
        interpolation_policy_ledger_df=interpolation_policy_ledger_df,
        rupture_event_slot_ledger_df=rupture_event_slot_ledger_df,
        cohort_window_requirement_index_df=cohort_window_requirement_index_df,
        run_manifest_df=run_manifest_df,
    )
    return readiness


def validate_v553_temporal_pressure_readiness(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("ready_for_runtime_consumption"):
        errors.append("V553 thin temporal pressure layer must not be runtime consumable")
    if readiness.get("runtime_packets_written"):
        errors.append("V553 thin temporal pressure layer must not write runtime packets")
    if readiness.get("persona_fields_written"):
        errors.append("V553 thin temporal pressure layer must not write persona fields")
    if not readiness.get("packet_path"):
        errors.append("V553 thin temporal pressure layer missing packet path")
    if not readiness.get("year_indexed_pressure_path"):
        errors.append("V553 thin temporal pressure layer missing year-indexed pressure path")
    if not readiness.get("interpolated_pressure_path"):
        errors.append("V553 thin temporal pressure layer missing interpolated pressure path")
    if not readiness.get("harmonization_evidence_path"):
        errors.append("V553 thin temporal pressure layer missing harmonization evidence path")
    if readiness.get("harmonization_evidence_path") and not Path(str(readiness.get("harmonization_evidence_path"))).exists():
        errors.append("V553 thin temporal pressure layer missing harmonization evidence artifact")
    evidence_row_count = readiness.get("harmonization_evidence_row_count", -1)
    if evidence_row_count in ("", None):
        evidence_row_count = -1
    if int(evidence_row_count) < 0:
        errors.append("V553 thin temporal pressure layer unreadable harmonization evidence artifact")
    for key, label in (
        ("v553_wave_harmonization_table_path", "wave harmonization table"),
        ("harmonization_difference_ledger_path", "harmonization difference ledger"),
        ("source_wave_anchor_manifest_path", "source wave anchor manifest"),
        ("v553_wave_anchor_index_path", "wave anchor index"),
        ("temporal_key_candidate_index_path", "temporal key candidate index"),
        ("temporal_key_blocker_index_path", "temporal key blocker index"),
        ("structural_dimension_resolution_audit_path", "structural dimension resolution audit"),
        ("v553_harmonized_pressure_key_index_path", "harmonized pressure key index"),
        ("v553_temporal_pressure_observation_index_path", "temporal pressure observation index"),
        ("v553_cross_wave_delta_index_path", "cross-wave delta index"),
        ("v553_interpolation_segment_index_path", "interpolation segment index"),
        ("v553_temporal_gap_and_absence_index_path", "temporal gap and absence index"),
        ("v553_structural_rupture_candidate_index_path", "structural rupture candidate index"),
        ("v553_temporal_pressure_field_path", "temporal pressure field"),
        ("v553_v554_handoff_index_path", "v554 handoff index"),
        ("v553_forbidden_inference_audit_path", "forbidden inference audit"),
        ("country_year_pressure_field_path", "country-year pressure field"),
        ("pressure_component_breakdown_path", "pressure component breakdown"),
        ("pressure_basis_ledger_path", "pressure basis ledger"),
        ("confidence_penalty_ledger_path", "confidence penalty ledger"),
        ("temporal_anchor_index_path", "temporal anchor index"),
        ("harmonization_authority_index_path", "harmonization authority index"),
        ("interpolation_policy_ledger_path", "interpolation policy ledger"),
        ("rupture_event_slot_ledger_path", "rupture event slot ledger"),
        ("cohort_window_requirement_index_path", "cohort window requirement index"),
        ("absence_noncomparability_register_path", "absence/noncomparability register"),
        ("temporal_authority_ledger_path", "temporal authority ledger"),
        ("comparability_audit_path", "cross-wave comparability audit"),
        ("noncomparability_audit_path", "cross-wave noncomparability audit"),
        ("rupture_block_audit_path", "rupture block audit"),
        ("downstream_v554_handoff_index_path", "downstream v554 handoff index"),
        ("interpolation_manifest_path", "interpolation manifest"),
        ("event_override_manifest_path", "event override manifest"),
        ("v553_run_manifest_path", "run manifest"),
    ):
        if not readiness.get(key):
            errors.append(f"V553 thin temporal pressure layer missing {label} path")
        elif not Path(str(readiness.get(key))).exists():
            errors.append(f"V553 thin temporal pressure layer missing {label} artifact")
    for key in (
        "wave_coverage_score",
        "shared_semantic_score",
        "shared_directionality_score",
        "shared_position_score",
        "overlay_presence_score",
        "harmonization_score",
    ):
        if key not in readiness:
            errors.append(f"V553 thin temporal pressure layer missing {key}")
    return errors


__all__ = [
    "build_v553_temporal_pressure_field",
    "validate_v553_temporal_pressure_readiness",
]
