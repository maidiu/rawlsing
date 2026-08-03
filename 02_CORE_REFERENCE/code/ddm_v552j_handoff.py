#!/usr/bin/env python3
"""Structural handoff builder for the provisional V552J adapter."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_v551j_io import file_hash, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v552j_schema import (
    V552J_COMPILER_VERSION,
    V552J_FORBIDDEN_CLAIM_IDS,
    V552J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
    V552J_HANDOFF_STATUSES,
    V552J_LIFECYCLE_STATUSES,
    V552J_READINESS_REPORT_SCHEMA,
    V552J_RUNTIME_HANDOFF_MANIFEST_SCHEMA,
    V552J_RUNTIME_USE_CLASSES,
    V552J_SCHEMA_VERSION,
    V552J_BLOCKED_INDEX_SCHEMA,
    V552J_STRUCTURAL_ABSENCE_PACKET_SCHEMA,
    V552J_STRUCTURAL_CONSTRAINT_PACKET_SCHEMA,
    V552J_STRUCTURAL_CONTEXT_PACKET_SCHEMA,
    V552J_STRUCTURAL_CONTEXT_ONLY_INDEX_SCHEMA,
    V552J_STRUCTURAL_UNCERTAINTY_PACKET_SCHEMA,
    V552J_REVIEW_ONLY_INDEX_SCHEMA,
    V552J_DIAGNOSTIC_ONLY_INDEX_SCHEMA,
    V552J_TO_V553_HANDOFF_INDEX_SCHEMA,
    V552J_INPUT_ARTIFACT_AUDIT_SCHEMA,
    V552J_PERMISSION_BOUNDARY_AUDIT_SCHEMA,
    V552J_DOWNSTREAM_LEAKAGE_AUDIT_SCHEMA,
    V552J_V553_HANDOFF_MANIFEST_SCHEMA,
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _resolve_repo_path(path_text: str | None) -> Path | None:
    token = _clean(path_text)
    if not token:
        return None
    path = Path(token)
    if path.is_absolute():
        return path
    return ROOT / path


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
    return json.dumps(cleaned, ensure_ascii=False)


def _json_singleton_array(value: Any) -> str:
    token = _clean(value)
    return _json_array([token] if token else [])


def _first_nonempty(values: Any, fallback: str = "") -> str:
    if isinstance(values, (list, tuple, set)):
        for value in values:
            token = _clean(value)
            if token:
                return token
    token = _clean(values)
    return token or fallback


def _json_object(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, ensure_ascii=False, default=str)


def _ledger_json(payload: dict[str, Any] | None) -> str:
    return _json_object(payload or {})


def _artifact_mode_from_inputs(*, supplied_v552_context: bool, comparability_status: str, required_inputs_present: bool) -> str:
    if not required_inputs_present:
        return "blocked"
    if supplied_v552_context and comparability_status != "not_supplied":
        return "v553_temporal_input_candidate"
    if supplied_v552_context:
        return "single_wave_structural_handoff"
    return "adapter_preflight"


def _v552_context_profile_from_inputs(v552_inputs: dict[str, Any], comparability_present: bool) -> str:
    core_keys = {
        "v552_question_semantic_hierarchy_path",
        "v552_structural_channel_index_path",
        "v552_relation_axis_pressure_path",
        "v552_target_entity_pressure_path",
        "v552_driver_facet_pressure_path",
        "v552_contradiction_surface_path",
        "v552_horizon_constraint_index_path",
        "v552_parent_prior_manifest_path",
    }
    supplied_core = sum(1 for key in core_keys if _clean(v552_inputs.get(key)))
    if supplied_core == 0:
        return "none"
    if supplied_core < len(core_keys):
        return "partial"
    return "full_supplied" if comparability_present else "core_supplied"


def _resolve_v552_structural_artifact_paths(
    *,
    v552_artifact_authority_index_path: str | None,
    v552_structural_fact_index_path: str | None,
    v552_temporal_key_source_index_path: str | None,
) -> dict[str, Path | None]:
    explicit_fact_path = _resolve_repo_path(v552_structural_fact_index_path)
    explicit_key_path = _resolve_repo_path(v552_temporal_key_source_index_path)
    authority_index = _load_optional(v552_artifact_authority_index_path)
    if authority_index.empty:
        return {
            "v552_structural_fact_index_path": explicit_fact_path,
            "v552_temporal_key_source_index_path": explicit_key_path,
        }

    def _authority_path(artifact_name: str) -> Path | None:
        matches = authority_index[authority_index["artifact_name"].astype(str).eq(artifact_name)].copy()
        if matches.empty:
            return None
        for column in ("artifact_path_parquet", "artifact_path_csv"):
            candidate = _clean(matches.iloc[0].get(column))
            resolved = _resolve_repo_path(candidate)
            if resolved is not None:
                return resolved
        return None

    return {
        "v552_structural_fact_index_path": explicit_fact_path or _authority_path("v552_structural_fact_index"),
        "v552_temporal_key_source_index_path": explicit_key_path or _authority_path("v552_temporal_key_source_index"),
    }


def _input_artifact_record(
    *,
    run_id: str,
    artifact_name: str,
    path: Path | None,
    required_for_mode: str,
    authority_class: str,
    read_permission: str,
    failure_if_missing: str,
    artifact_mode: str,
) -> dict[str, Any]:
    path_text = str(path) if path else ""
    present = bool(path and path.exists())
    row_count = 0
    if present:
        try:
            table = read_table(path)
            row_count = int(len(table))
        except Exception:
            row_count = 0
    return {
        "run_id": run_id,
        "artifact_name": artifact_name,
        "path": repo_relative_path_text(path_text),
        "present": present,
        "row_count": row_count,
        "hash": file_hash(path_text) if path_text else "not_supplied",
        "required_for_mode": required_for_mode,
        "authority_class": authority_class,
        "read_permission": read_permission,
        "failure_if_missing": failure_if_missing,
        "artifact_mode": artifact_mode,
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
    }


def _load_optional(path: str | None) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    return read_table(path)


def _first_nonempty(*values: Any) -> str:
    for value in values:
        token = _clean(value)
        if token:
            return token
    return ""


def _normalize_v553_handoff_modes(v553_input_index_df: pd.DataFrame) -> pd.DataFrame:
    if v553_input_index_df.empty:
        return v553_input_index_df
    frame = v553_input_index_df.copy()
    if "v553_handoff_mode" not in frame.columns:
        frame["v553_handoff_mode"] = "blocked_context"
    if "v553_handoff_allowed" not in frame.columns:
        frame["v553_handoff_allowed"] = False
    if "v553_probe_allowed" not in frame.columns:
        frame["v553_probe_allowed"] = False
    if "v553_temporal_field_allowed" not in frame.columns:
        frame["v553_temporal_field_allowed"] = False
    if "v553_handoff_blocked_reason" not in frame.columns:
        frame["v553_handoff_blocked_reason"] = "no_authorized_temporal_field_yet"
    probe_mask = frame["ready_for_v553_probe"].astype(bool) if "ready_for_v553_probe" in frame.columns else pd.Series(False, index=frame.index)
    temporal_mask = frame["ready_for_v553_temporal_field"].astype(bool) if "ready_for_v553_temporal_field" in frame.columns else pd.Series(False, index=frame.index)
    resolved_mask = frame["structural_dimensions_resolved_for_v553"].astype(bool) if "structural_dimensions_resolved_for_v553" in frame.columns else pd.Series(False, index=frame.index)
    audit_mask = frame["source_v552_structural_fact_lane"].astype(str).eq("audit_fact") if "source_v552_structural_fact_lane" in frame.columns else pd.Series(False, index=frame.index)
    normalized_mode = pd.Series("diagnostic_only", index=frame.index, dtype=object)
    normalized_mode.loc[resolved_mask] = "blocked_context"
    normalized_mode.loc[probe_mask] = "probe_only"
    normalized_mode.loc[temporal_mask] = "temporal_field_ready"
    normalized_mode.loc[audit_mask] = "diagnostic_only"
    frame["v553_handoff_mode"] = normalized_mode
    frame["v553_handoff_allowed"] = (probe_mask | temporal_mask | resolved_mask) & ~audit_mask
    frame["v553_probe_allowed"] = probe_mask & ~audit_mask
    frame["v553_temporal_field_allowed"] = temporal_mask & ~audit_mask
    frame.loc[audit_mask, "v553_handoff_blocked_reason"] = "audit_fact_diagnostic_only"
    return frame


def _standardize_review_status(value: str) -> str:
    if not value:
        return "not_supplied"
    if value.startswith("reviewable"):
        return "reviewable_context"
    if value in {"diagnostic_only", "blocked"}:
        return value
    return value


def _standardize_certification_status(value: str, review_status: str) -> str:
    if value == "certified":
        return "certified"
    if review_status.startswith("reviewable"):
        return "reviewable"
    if review_status == "diagnostic_only":
        return "diagnostic"
    if value:
        return value
    return "unknown"


def _standardize_lane(certification_status: str, review_status: str) -> str:
    if certification_status == "certified":
        return "certified_spine"
    if review_status.startswith("reviewable"):
        return "reviewable_context"
    if review_status == "diagnostic_only":
        return "diagnostic_forensic"
    if review_status == "blocked" or certification_status == "blocked":
        return "blocked"
    return "blocked"


def _standardize_permission_class(normalized_lane: str) -> str:
    if normalized_lane == "certified_spine":
        return "v553_constraint_candidate"
    if normalized_lane == "reviewable_context":
        return "v553_context_only"
    if normalized_lane == "diagnostic_forensic":
        return "forensic_only"
    return "blocked"


def _bounded_score(value: Any, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        return float(default)
    if score != score:
        return float(default)
    return max(0.0, min(1.0, score))


def _score_from_map(value: str, mapping: dict[str, float], default: float = 0.0) -> float:
    token = _clean(value)
    if not token:
        return float(default)
    return float(mapping.get(token, default))


def _packet_score_bundle(packet_row: pd.Series, comparability_context: dict[str, Any], ready_for_v553: bool) -> dict[str, float]:
    certification_score = _score_from_map(
        packet_row.get("normalized_v551j_certification_status"),
        {
            "certified": 1.0,
            "reviewable": 0.65,
            "diagnostic": 0.25,
            "blocked": 0.0,
            "unknown": 0.0,
        },
    )
    support_score = _score_from_map(
        packet_row.get("normalized_support_status"),
        {
            "sufficient_support": 1.0,
            "underpowered": 0.45,
            "zero_support": 0.0,
            "missing_support": 0.0,
            "not_applicable": 0.6,
            "unknown": 0.1,
        },
    )
    directionality_score = _score_from_map(
        packet_row.get("normalized_directionality_status"),
        {
            "known_directional": 1.0,
            "partial_directionality": 0.6,
            "not_applicable": 0.45,
            "unknown": 0.0,
        },
    )
    authority_score = _score_from_map(
        packet_row.get("normalized_authority_status"),
        {
            "exact_registry": 1.0,
            "manual_review": 0.75,
            "computed_context": 0.5,
            "unknown": 0.0,
        },
    )
    comparability_score = _score_from_map(
        comparability_context.get("status"),
        {
            "READY_V551J_CROSS_WAVE_DIFF": 1.0,
            "READY_V551J_CROSS_WAVE_DIFF_WITH_GAPS": 0.75,
            "READY_V551J_SINGLE_WAVE_ONLY": 0.5,
            "not_supplied": 0.0,
        },
    )
    confidence_score = _bounded_score((certification_score + support_score + directionality_score + authority_score) / 4.0)
    readiness_score = _bounded_score(
        (0.28 * certification_score)
        + (0.24 * support_score)
        + (0.24 * directionality_score)
        + (0.14 * authority_score)
        + (0.10 * comparability_score)
        - (0.20 if bool(packet_row.get("status_conflict_flag", False)) else 0.0)
    )
    return {
        "certification_score": certification_score,
        "support_score": support_score,
        "directionality_score": directionality_score,
        "authority_score": authority_score,
        "comparability_score": comparability_score,
        "confidence_score": confidence_score,
        "readiness_score": readiness_score if ready_for_v553 else max(0.0, readiness_score * 0.85),
    }


def _normalization_bundle(row: pd.Series, comparability_context: dict[str, Any], v552_context_supplied: bool) -> dict[str, Any]:
    raw_review = _clean(row.get("v551j_review_surface_status")) or _clean(row.get("review_surface_status"))
    raw_cert = _clean(row.get("v551j_evidence_certification_status")) or _clean(row.get("certification_status"))
    raw_authority = _clean(row.get("authority_status"))
    raw_directionality = _clean(row.get("directionality_status"))
    raw_support = _clean(row.get("support_status"))
    raw_v552_context = _clean(row.get("v552_context_status"))
    raw_comparability = _clean(row.get("comparability_status"))

    normalized_review_status = _clean(row.get("normalized_v551j_review_status")) or _standardize_review_status(raw_review)
    normalized_certification_status = _clean(row.get("normalized_v551j_certification_status")) or _standardize_certification_status(raw_cert, normalized_review_status)
    normalized_lane = _clean(row.get("normalized_v551j_lane")) or _standardize_lane(normalized_certification_status, normalized_review_status)
    normalized_authority_status = _clean(row.get("normalized_authority_status")) or raw_authority or "unknown"
    normalized_directionality_status = _clean(row.get("normalized_directionality_status")) or raw_directionality or "unknown"
    normalized_support_status = _clean(row.get("normalized_support_status")) or raw_support or "unknown"
    normalized_v552_context_status = _clean(row.get("normalized_v552_context_status")) or raw_v552_context or ("supplied" if v552_context_supplied else "not_supplied")
    normalized_comparability_status = _clean(row.get("normalized_comparability_status")) or raw_comparability or _clean(comparability_context.get("status")) or "not_supplied"
    permission_class = _clean(row.get("permission_class")) or _standardize_permission_class(normalized_lane)
    constraint_eligibility = normalized_lane == "certified_spine"
    context_eligibility = normalized_lane in {"certified_spine", "reviewable_context"}
    forensic_eligibility = normalized_lane in {"diagnostic_forensic", "blocked", "conflict"}
    blocked_from_downstream = normalized_lane in {"blocked", "conflict"}

    raw_review_standard = _standardize_review_status(raw_review)
    raw_cert_standard = _standardize_certification_status(raw_cert, raw_review_standard)
    raw_lane_standard = _standardize_lane(raw_cert_standard, raw_review_standard)

    def _status_family(label: str, value: str) -> str:
        if not value:
            return ""
        if label in {"review_status", "certification_status"}:
            if value.startswith("reviewable"):
                return "reviewable"
            if value in {"certified", "review"}:
                return "certified"
            if value in {"blocked", "diagnostic_only"}:
                return value
            return value
        if label == "lane":
            if value in {"certified_spine", "reviewable_context"}:
                return "contextual_or_certified"
            if value in {"diagnostic_forensic", "blocked", "conflict"}:
                return value
            return value
        if label == "authority_status":
            if value in {"exact_registry", "manual_review", "unknown"}:
                return value
            return value
        if label == "directionality_status":
            if value in {"known_directional", "partial_directionality", "not_applicable", "unknown", "directionality_gap"}:
                return value if value != "directionality_gap" else "unknown"
            return value
        if label == "support_status":
            if value in {"sufficient_support", "unknown"}:
                return value
            return value
        if label in {"v552_context_status", "comparability_status"}:
            if value in {"supplied", "not_supplied", "ready"}:
                return value
            return value
        return value

    conflicts: list[str] = []
    for label, raw_value, normalized_value in (
        ("review_status", raw_review_standard, normalized_review_status),
        ("certification_status", raw_cert_standard, normalized_certification_status),
        ("lane", raw_lane_standard, normalized_lane),
        ("authority_status", raw_authority, normalized_authority_status),
        ("directionality_status", raw_directionality, normalized_directionality_status),
        ("support_status", raw_support, normalized_support_status),
        ("v552_context_status", raw_v552_context, normalized_v552_context_status),
        ("comparability_status", raw_comparability, normalized_comparability_status),
    ):
        if label == "v552_context_status" and v552_context_supplied and _clean(raw_value) in {"", "not_supplied"} and normalized_value == "supplied":
            continue
        if raw_value and normalized_value and _status_family(label, raw_value) != _status_family(label, normalized_value):
            conflicts.append(label)

    status_conflict_flag = bool(conflicts)
    status_conflict_reason = ", ".join(conflicts)

    return {
        "normalized_v551j_lane": normalized_lane,
        "normalized_v551j_certification_status": normalized_certification_status,
        "normalized_v551j_review_status": normalized_review_status,
        "normalized_authority_status": normalized_authority_status,
        "normalized_directionality_status": normalized_directionality_status,
        "normalized_support_status": normalized_support_status,
        "normalized_v552_context_status": normalized_v552_context_status,
        "normalized_comparability_status": normalized_comparability_status,
        "permission_class": permission_class,
        "constraint_eligibility": constraint_eligibility,
        "context_eligibility": context_eligibility,
        "forensic_eligibility": forensic_eligibility,
        "blocked_from_downstream": blocked_from_downstream,
        "status_conflict_flag": status_conflict_flag,
        "status_conflict_reason": status_conflict_reason,
    }


def _temporal_normalization_bundle(row: pd.Series, comparability_context: dict[str, Any], v552_context_supplied: bool) -> dict[str, Any]:
    allowed_probe = bool(row.get("allowed_for_v553_probe", False))
    allowed_temporal = bool(row.get("allowed_for_v553_temporal_field", False))
    resolution_status = _clean(row.get("resolution_status"))
    directionality_coverage = _bounded_score(row.get("directionality_coverage"), 0.0)
    normalized_review_status = "reviewable_context" if allowed_probe else "diagnostic_only"
    normalized_certification_status = "certified" if allowed_probe else "reviewable"
    normalized_lane = "certified_spine" if allowed_probe else "reviewable_context"
    normalized_authority_status = "exact_registry" if resolution_status == "resolved_structural_match" else ("computed_context" if allowed_probe else "unknown")
    if directionality_coverage >= 0.999:
        normalized_directionality_status = "known_directional"
    elif directionality_coverage > 0:
        normalized_directionality_status = "partial_directionality"
    else:
        normalized_directionality_status = "unknown"
    normalized_support_status = _clean(row.get("support_status")) or "unknown"
    normalized_v552_context_status = "supplied" if v552_context_supplied else "not_supplied"
    normalized_comparability_status = _clean(comparability_context.get("status")) or "not_supplied"
    permission_class = "v553_constraint_candidate" if allowed_temporal else ("v553_context_only" if allowed_probe else "blocked")
    return {
        "normalized_v551j_lane": normalized_lane,
        "normalized_v551j_certification_status": normalized_certification_status,
        "normalized_v551j_review_status": normalized_review_status,
        "normalized_authority_status": normalized_authority_status,
        "normalized_directionality_status": normalized_directionality_status,
        "normalized_support_status": normalized_support_status,
        "normalized_v552_context_status": normalized_v552_context_status,
        "normalized_comparability_status": normalized_comparability_status,
        "permission_class": permission_class,
        "constraint_eligibility": allowed_temporal,
        "context_eligibility": allowed_probe,
        "forensic_eligibility": not allowed_probe,
        "blocked_from_downstream": not allowed_probe,
        "status_conflict_flag": False,
        "status_conflict_reason": "",
    }


def _bundle_bundle_rows(certified: pd.DataFrame, sidecar: pd.DataFrame) -> pd.DataFrame:
    if certified.empty and sidecar.empty:
        return pd.DataFrame()
    rows: dict[str, dict[str, Any]] = {}
    for frame, source_label in ((sidecar, "sidecar"), (certified, "certified")):
        if frame.empty:
            continue
        for row in frame.to_dict(orient="records"):
            packet_id = _first_nonempty(row.get("packet_id"), row.get("v551j_packet_id"), f"v552j__{source_label}")
            current = rows.get(packet_id, {})
            current.update(row)
            current["packet_id"] = packet_id
            rows[packet_id] = current
    return pd.DataFrame(list(rows.values()))


def _build_comparability_context(diff_summary: pd.DataFrame, run_id: str) -> dict[str, Any]:
    if diff_summary.empty:
        return {
            "comparison_id": "",
            "status": "not_supplied",
            "packet_change_count": 0,
            "packet_presence_counts": {},
            "top_changed_fields": {},
            "left_run_id": "",
            "right_run_id": "",
            "created_at": utc_now(),
        }
    row = diff_summary.iloc[0].to_dict()
    return {
        "comparison_id": _clean(row.get("comparison_id")),
        "status": _clean(row.get("status")) or "not_supplied",
        "packet_change_count": int(row.get("packet_change_count", 0) or 0),
        "packet_presence_counts": _json_object(row.get("packet_presence_counts")),
        "top_changed_fields": _json_object(row.get("top_changed_fields")),
        "left_run_id": _clean(row.get("left_run_id")),
        "right_run_id": _clean(row.get("right_run_id")),
        "created_at": utc_now(),
    }


def _determine_required_mediation(row: pd.Series) -> list[str]:
    requirements: list[str] = []
    if bool(row.get("requires_temporalization", False)):
        requirements.append("temporalization_required")
    if bool(row.get("requires_household_mediation", False)):
        requirements.append("household_mediation_required")
    if bool(row.get("requires_carrier_mediation", False)):
        requirements.append("carrier_mediation_required")
    if bool(row.get("requires_orientation_resolution", False)):
        requirements.append("orientation_resolution_required")
    if bool(row.get("requires_pressureflow_mediation", False)):
        requirements.append("pressureflow_mediation_required")
    if bool(row.get("requires_enneagram_runtime", False)):
        requirements.append("enneagram_runtime_required")
    return requirements


def _blocker_contexts(packet_row: pd.Series, comparability_context: dict[str, Any], v552_context_supplied: bool) -> list[str]:
    missing_contexts: list[str] = []
    if _clean(packet_row.get("normalized_v551j_review_status")) in {"", "unknown", "not_supplied"}:
        missing_contexts.append("review_surface_status")
    if _clean(packet_row.get("normalized_v551j_certification_status")) != "certified":
        missing_contexts.append("certified_spine")
    if not v552_context_supplied:
        missing_contexts.append("v552_context")
    if _clean(packet_row.get("normalized_authority_status")) in {"unknown", ""}:
        missing_contexts.append("authority")
    if _clean(packet_row.get("normalized_directionality_status")) in {"unknown", ""}:
        missing_contexts.append("directionality")
    return missing_contexts


def _derived_status(packet_row: pd.Series, comparability_context: dict[str, Any], v552_context_supplied: bool) -> tuple[str, str, str]:
    missing_contexts = _blocker_contexts(packet_row, comparability_context, v552_context_supplied)
    if missing_contexts:
        return "ready_with_gaps", "constraint_recorded_with_gaps", ", ".join(missing_contexts)
    return "ready", "constraint_recorded", ""


def _context_breakdown(packet_row: pd.Series, comparability_context: dict[str, Any], v552_context_supplied: bool) -> dict[str, Any]:
    required_blockers = _blocker_contexts(packet_row, comparability_context, v552_context_supplied)
    optional_contexts: list[str] = []
    if comparability_context.get("status") == "not_supplied":
        optional_contexts.append("comparability")
    return {
        "required_blockers_json": _json_array(required_blockers),
        "required_blocker_count": len(required_blockers),
        "optional_contexts_json": _json_array(optional_contexts),
        "optional_context_count": len(optional_contexts),
        "comparability_status": _clean(comparability_context.get("status")) or "not_supplied",
        "v552_context_supplied": bool(v552_context_supplied),
    }


def _provenance_summary(row: pd.Series, provenance_manifest: pd.DataFrame, comparability_context: dict[str, Any], v552_inputs: dict[str, Any]) -> dict[str, Any]:
    source = _clean(row.get("source")) or _clean(provenance_manifest.iloc[0].get("source") if not provenance_manifest.empty and "source" in provenance_manifest.columns else "")
    wave = _clean(row.get("wave")) or _clean(provenance_manifest.iloc[0].get("wave") if not provenance_manifest.empty and "wave" in provenance_manifest.columns else "")
    canonical_wave = _clean(row.get("canonical_wave")) or wave
    country_code = _clean(row.get("country_code")) or _clean(provenance_manifest.iloc[0].get("country_code") if not provenance_manifest.empty and "country_code" in provenance_manifest.columns else "")
    return {
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "v551j_sources": {
            "certification_readiness": "manifest/v551j_certification_readiness_report.json",
            "review_readiness": "manifest/v551j_review_readiness_report.json",
            "input_provenance": "manifest/v551j_input_provenance_manifest.json",
        },
        "comparability_status": comparability_context.get("status", "not_supplied"),
        "v552_optional_inputs_supplied": [name for name, value in v552_inputs.items() if value],
    }


def _upstream_provenance_links(
    v551j_root: Path,
    v551j_comparison_root: str | Path | None,
    v552_inputs: dict[str, Any],
) -> dict[str, Any]:
    comparison_root = Path(v551j_comparison_root) if v551j_comparison_root else None
    comparison_report = comparison_root / "manifest" / "v551j_cross_wave_comparability_report.json" if comparison_root else None
    links = {
        "v551j_run_root": repo_relative_path_text(v551j_root),
        "v551j_certified_packet_index": repo_relative_path_text(v551j_root / "packets" / "v551j_certified_packet_index.parquet"),
        "v551j_reviewable_evidence_sidecar": repo_relative_path_text(v551j_root / "packets" / "v551j_reviewable_evidence_sidecar.parquet"),
        "v551j_certification_readiness_report": repo_relative_path_text(v551j_root / "manifest" / "v551j_certification_readiness_report.json"),
        "v551j_review_readiness_report": repo_relative_path_text(v551j_root / "manifest" / "v551j_review_readiness_report.json"),
        "v551j_packet_readiness_report": repo_relative_path_text(v551j_root / "manifest" / "v551j_packet_readiness_report.json"),
        "v551j_input_provenance_manifest": repo_relative_path_text(v551j_root / "manifest" / "v551j_input_provenance_manifest.json"),
        "v551j_cross_wave_comparability_report": repo_relative_path_text(comparison_report) if comparison_report and comparison_report.exists() else "",
        "v552_optional_inputs": {name: repo_relative_path_text(value) if value else "" for name, value in v552_inputs.items()},
    }
    links["upstream_link_count"] = int(
        sum(1 for value in links.values() if isinstance(value, str) and value) + sum(1 for value in links.get("v552_optional_inputs", {}).values() if value)
    )
    return links


def _structural_fact_match_score(packet_row: pd.Series, fact_row: pd.Series) -> int:
    score = 0
    packet_relation_axes = set(_parse_json_array(packet_row.get("relation_axis_ids_json"))) | { _clean(packet_row.get("relation_axis_id")) }
    packet_target_entities = set(_parse_json_array(packet_row.get("target_entity_ids_json"))) | { _clean(packet_row.get("target_entity_id")) }
    packet_driver_facets = set(_parse_json_array(packet_row.get("driver_facet_ids_json"))) | { _clean(packet_row.get("driver_facet_id")) }
    packet_questions = set(_parse_json_array(packet_row.get("question_ids_json"))) | { _clean(packet_row.get("question_id")) }
    packet_wave = _clean(packet_row.get("wave"))
    packet_country = _clean(packet_row.get("country_code"))
    if _clean(fact_row.get("relation_axis_id")) and _clean(fact_row.get("relation_axis_id")) in packet_relation_axes:
        score += 4
    if _clean(fact_row.get("target_entity_id")) and _clean(fact_row.get("target_entity_id")) in packet_target_entities:
        score += 3
    if _clean(fact_row.get("driver_facet_id")) and _clean(fact_row.get("driver_facet_id")) in packet_driver_facets:
        score += 3
    if _clean(fact_row.get("question_id")) and _clean(fact_row.get("question_id")) in packet_questions:
        score += 2
    if packet_wave and _clean(fact_row.get("wave")) == packet_wave:
        score += 1
    if packet_country and _clean(fact_row.get("country_code")) == packet_country:
        score += 1
    return score


def _structural_fact_match_policy(match_score: int) -> str:
    if match_score >= 8:
        return "exact_structural_match"
    if match_score >= 5:
        return "partial_structural_match"
    if match_score >= 2:
        return "question_match_only"
    if match_score >= 1:
        return "broad_context_match"
    return "no_match"


def _packet_structural_dimension_resolution(
    packet_row: pd.Series,
    v552_structural_fact_index: pd.DataFrame,
    v552_temporal_key_source_index: pd.DataFrame,
) -> dict[str, Any]:
    packet_relation_axes = [value for value in _parse_json_array(packet_row.get("relation_axis_ids_json")) if value] or [_clean(packet_row.get("relation_axis_id"))]
    packet_target_entities = [value for value in _parse_json_array(packet_row.get("target_entity_ids_json")) if value] or [_clean(packet_row.get("target_entity_id"))]
    packet_driver_facets = [value for value in _parse_json_array(packet_row.get("driver_facet_ids_json")) if value] or [_clean(packet_row.get("driver_facet_id"))]
    packet_questions = [value for value in _parse_json_array(packet_row.get("question_ids_json")) if value] or [_clean(packet_row.get("question_id"))]
    packet_country = _clean(packet_row.get("country_code"))
    packet_wave = _clean(packet_row.get("wave"))
    packet_source = _clean(packet_row.get("source"))
    packet_structural_fact_id = _clean(packet_row.get("source_v552_structural_fact_id")) or _clean(packet_row.get("v552_structural_fact_id"))
    packet_structural_fact_ids = [value for value in _parse_json_array(packet_row.get("source_v552_structural_fact_ids_json")) if value]
    if packet_structural_fact_id and packet_structural_fact_id not in packet_structural_fact_ids:
        packet_structural_fact_ids.insert(0, packet_structural_fact_id)
    packet_temporal_key_source_id = _clean(packet_row.get("source_v552_temporal_key_source_id")) or _clean(packet_row.get("v552_temporal_key_source_id"))
    packet_temporal_key_source_ids = [packet_temporal_key_source_id] if packet_temporal_key_source_id else []
    packet_relation_axis_id = _clean(packet_row.get("relation_axis_id"))
    packet_target_entity_id = _clean(packet_row.get("target_entity_id"))
    packet_driver_facet_id = _clean(packet_row.get("driver_facet_id"))
    packet_structural_channel_id = _clean(packet_row.get("structural_channel_id"))
    packet_horizon_constraint_id = _clean(packet_row.get("horizon_constraint_id"))
    packet_semantic_signature = _clean(packet_row.get("semantic_signature"))
    packet_structural_fact_lane = _clean(packet_row.get("source_v552_structural_fact_lane")) or _clean(packet_row.get("structural_fact_lane")) or "not_temporal_key_source"
    packet_structural_fact_grain = _clean(packet_row.get("source_v552_structural_fact_grain")) or _clean(packet_row.get("structural_fact_grain")) or "not_temporal_key_source"
    packet_has_structural_fields = bool(
        packet_structural_fact_id
        or packet_relation_axis_id
        or packet_target_entity_id
        or packet_driver_facet_id
        or packet_structural_channel_id
        or packet_horizon_constraint_id
        or packet_semantic_signature
    )
    packet_base_resolution = {
        "source_v552_artifact": _clean(packet_row.get("source_artifact")) or "",
        "source_v552_structural_fact_id": packet_structural_fact_id,
        "source_v552_structural_fact_ids_json": _json_singleton_array(packet_structural_fact_id or (packet_structural_fact_ids[0] if packet_structural_fact_ids else "")),
        "source_v552_structural_fact_ids_diagnostic_json": _json_array(packet_structural_fact_ids),
        "source_v552_temporal_key_source_id": packet_temporal_key_source_id,
        "source_v552_temporal_key_source_ids_json": _json_array(packet_temporal_key_source_ids),
        "source_v552_structural_fact_status": _clean(packet_row.get("source_v552_structural_fact_status")) or _clean(packet_row.get("structural_fact_status")) or "",
        "source_v552_structural_fact_lane": packet_structural_fact_lane,
        "source_v552_structural_fact_grain": packet_structural_fact_grain,
        "structural_dimension_status": "resolved" if packet_has_structural_fields else "missing",
        "structural_dimension_blocker_reason": "" if packet_has_structural_fields else "missing_v552_structural_fact_index",
        "relation_axis_id": packet_relation_axis_id,
        "target_entity_id": packet_target_entity_id,
        "driver_facet_id": packet_driver_facet_id,
        "structural_channel_id": packet_structural_channel_id,
        "horizon_constraint_id": packet_horizon_constraint_id,
        "semantic_signature": packet_semantic_signature,
        "v552_structural_match_status": "preserved_handoff_structural_fields" if packet_has_structural_fields else "no_match",
        "v552_structural_match_score": 0,
        "v552_structural_match_reason": "preserved_handoff_structural_fields" if packet_has_structural_fields else "missing_v552_structural_fact_index",
        "matched_fact_count": 0,
        "broad_match_count": 0,
        "temporal_key_basis": json.dumps(
            {
                "fallback": not packet_has_structural_fields,
                "source": packet_source,
                "wave": packet_wave,
                "country_code": packet_country,
                "preserved_handoff_structural_fields": packet_has_structural_fields,
            },
            sort_keys=True,
            ensure_ascii=False,
        ),
        "temporal_key_candidate_status": "resolved" if packet_has_structural_fields else "blocked",
        "temporal_key_blocker_reason": "" if packet_has_structural_fields else "missing_v552_structural_fact_index",
        "fallback_permission_profile_key": f"{_clean(packet_row.get('permission_class')) or _clean(packet_row.get('read_permission')) or 'unknown_permission_profile'}::probe_only",
        "fallback_used": not packet_has_structural_fields,
        "resolution_status": "preserved_handoff_structural_fields" if packet_has_structural_fields else "fallback_shared_column_profile",
        "allowed_downstream_use": bool(packet_has_structural_fields),
        "source_v552_fact_matches": [],
    }

    if v552_structural_fact_index.empty:
        return packet_base_resolution

    fact_df = v552_structural_fact_index.copy()
    fact_df["_match_score"] = fact_df.apply(lambda fact_row: _structural_fact_match_score(packet_row, fact_row), axis=1)
    fact_df["_match_policy"] = fact_df["_match_score"].map(_structural_fact_match_policy)
    fact_df = fact_df.sort_values(["_match_score", "source_artifact", "source_row_index", "v552_structural_fact_id"], ascending=[False, True, True, True]).reset_index(drop=True)
    matched_df = fact_df[fact_df["_match_score"].astype(int) > 0].copy()
    if matched_df.empty:
        return packet_base_resolution

    primary = matched_df.iloc[0].to_dict()
    fact_ids = [str(value) for value in matched_df["v552_structural_fact_id"].astype(str).tolist() if _clean(value)]
    temporal_rows = v552_temporal_key_source_index[
        v552_temporal_key_source_index["v552_structural_fact_id"].astype(str).isin(fact_ids)
    ].copy()
    temporal_ids = [str(value) for value in temporal_rows.get("v552_temporal_key_source_id", pd.Series(dtype=str)).astype(str).tolist() if _clean(value)]
    temporal_source_row_ids = [str(value) for value in temporal_rows.get("source_row_id", pd.Series(dtype=str)).astype(str).tolist() if _clean(value)]
    relation_axis_id = _clean(primary.get("relation_axis_id")) or packet_relation_axis_id
    target_entity_id = _clean(primary.get("target_entity_id")) or packet_target_entity_id
    driver_facet_id = _clean(primary.get("driver_facet_id")) or packet_driver_facet_id
    structural_channel_id = _clean(primary.get("structural_channel_id")) or packet_structural_channel_id
    horizon_constraint_id = _clean(primary.get("horizon_constraint_id")) or packet_horizon_constraint_id
    semantic_signature = _clean(primary.get("semantic_signature")) or packet_semantic_signature
    structural_fact_lane = _clean(primary.get("structural_fact_lane")) or packet_structural_fact_lane
    structural_fact_grain = _clean(primary.get("structural_fact_grain")) or packet_structural_fact_grain
    source_v552_temporal_key_source_id = _first_nonempty(
        packet_temporal_key_source_id,
        _clean(primary.get("v552_temporal_key_source_id")),
        *temporal_ids,
    )
    temporal_basis = {
        "source_source": packet_source,
        "source_wave": packet_wave,
        "source_country_code": packet_country,
        "source_v552_structural_fact_id": _clean(primary.get("v552_structural_fact_id")),
        "relation_axis_id": relation_axis_id,
        "target_entity_id": target_entity_id,
        "driver_facet_id": driver_facet_id,
        "structural_channel_id": structural_channel_id,
        "horizon_constraint_id": horizon_constraint_id,
        "semantic_signature": semantic_signature,
        "structural_fact_lane": structural_fact_lane,
        "structural_fact_grain": structural_fact_grain,
    }
    temporal_key_basis = json.dumps(temporal_basis, sort_keys=True, ensure_ascii=False)
    match_score = int(primary.get("_match_score", 0) or 0)
    match_policy = _structural_fact_match_policy(match_score)
    structural_dimension_status = "resolved" if match_policy in {"exact_structural_match", "partial_structural_match"} or packet_has_structural_fields else "probe_only"
    blocker_reason = "" if structural_dimension_status == "resolved" else ("broad_structural_context_only" if match_policy in {"question_match_only", "broad_context_match"} else "partial_structural_dimensions")
    fallback_used = structural_dimension_status != "resolved" and not packet_has_structural_fields
    resolved_structural = structural_dimension_status == "resolved"
    return {
        "source_v552_artifact": _clean(primary.get("source_artifact")) if resolved_structural else packet_base_resolution["source_v552_artifact"],
        "source_v552_structural_fact_id": _clean(primary.get("v552_structural_fact_id")) if resolved_structural else packet_structural_fact_id,
        "source_v552_structural_fact_ids_json": _json_singleton_array(
            _clean(primary.get("v552_structural_fact_id")) if resolved_structural else (packet_structural_fact_id or (packet_structural_fact_ids[0] if packet_structural_fact_ids else ""))
        ),
        "source_v552_structural_fact_ids_diagnostic_json": _json_array(fact_ids or packet_structural_fact_ids),
        "source_v552_temporal_key_source_id": source_v552_temporal_key_source_id,
        "source_v552_temporal_key_source_ids_json": _json_array(
            [source_v552_temporal_key_source_id] if source_v552_temporal_key_source_id else packet_temporal_key_source_ids
        ),
        "source_v552_temporal_key_source_row_ids_json": _json_array(temporal_source_row_ids),
        "source_v552_structural_fact_status": _clean(primary.get("structural_fact_status")) if resolved_structural else _clean(packet_row.get("source_v552_structural_fact_status")) or "probe_only",
        "source_v552_structural_fact_lane": structural_fact_lane if resolved_structural else packet_structural_fact_lane,
        "source_v552_structural_fact_grain": structural_fact_grain if resolved_structural else packet_structural_fact_grain,
        "structural_dimension_status": structural_dimension_status,
        "structural_dimension_blocker_reason": blocker_reason,
        "relation_axis_id": relation_axis_id if resolved_structural else "",
        "target_entity_id": target_entity_id if resolved_structural else "",
        "driver_facet_id": driver_facet_id if resolved_structural else "",
        "structural_channel_id": structural_channel_id if resolved_structural else "",
        "horizon_constraint_id": horizon_constraint_id if resolved_structural else "",
        "semantic_signature": semantic_signature if resolved_structural else "",
        "v552_structural_match_status": match_policy,
        "v552_structural_match_score": match_score,
        "v552_structural_match_reason": blocker_reason or "matched_v552_structural_fact",
        "matched_fact_count": int(len(matched_df)),
        "broad_match_count": int((matched_df["_match_score"].astype(int) < 5).sum()),
        "temporal_key_basis": temporal_key_basis,
        "temporal_key_candidate_status": "resolved" if structural_dimension_status == "resolved" else "probe_only",
        "temporal_key_blocker_reason": blocker_reason,
        "fallback_permission_profile_key": "" if structural_dimension_status == "resolved" else f"{_clean(packet_row.get('permission_class')) or _clean(packet_row.get('read_permission')) or 'unknown_permission_profile'}::probe_only",
        "fallback_used": fallback_used,
        "resolution_status": "resolved_structural_match" if match_policy in {"exact_structural_match", "partial_structural_match"} else ("preserved_handoff_structural_fields" if packet_has_structural_fields else "fallback_shared_column_profile"),
        "allowed_downstream_use": bool(structural_dimension_status == "resolved"),
        "source_v552_fact_matches": matched_df.to_dict(orient="records"),
    }


def _forbidden_claim_validation_summary(forbidden_claims: list[str]) -> dict[str, Any]:
    expected = [str(value).strip() for value in V552J_FORBIDDEN_CLAIM_IDS if str(value).strip()]
    observed = [str(value).strip() for value in forbidden_claims if str(value).strip()]
    expected_set = set(expected)
    observed_set = set(observed)
    missing = [value for value in expected if value not in observed_set]
    extra = [value for value in observed if value not in expected_set]
    duplicates = sorted({value for value in observed if observed.count(value) > 1})
    status = "complete"
    if not observed:
        status = "missing"
    elif missing or extra or duplicates:
        status = "partial"
    return {
        "forbidden_claim_ids_expected_count": len(expected),
        "forbidden_claim_ids_observed_count": len(observed),
        "forbidden_claim_ids_unique_observed_count": len(observed_set),
        "forbidden_claim_ids_missing_count": len(missing),
        "forbidden_claim_ids_extra_count": len(extra),
        "forbidden_claim_ids_duplicate_count": len(duplicates),
        "forbidden_claim_ids_validation_status": status,
        "forbidden_claim_ids_missing_json": _json_array(missing),
        "forbidden_claim_ids_extra_json": _json_array(extra),
        "forbidden_claim_ids_duplicates_json": _json_array(duplicates),
    }


def build_v552j_structural_handoff(
    *,
    run_id: str,
    v551j_run_root: str | Path,
    output_root: str | Path,
    v551j_comparison_root: str | Path | None = None,
    v552_question_semantic_hierarchy_path: str | None = None,
    v552_structural_channel_index_path: str | None = None,
    v552_relation_axis_pressure_path: str | None = None,
    v552_target_entity_pressure_path: str | None = None,
    v552_driver_facet_pressure_path: str | None = None,
    v552_contradiction_surface_path: str | None = None,
    v552_horizon_constraint_index_path: str | None = None,
    v552_parent_prior_manifest_path: str | None = None,
    v552_artifact_authority_index_path: str | None = None,
    v552_known_absence_register_path: str | None = None,
    v552_structural_fact_index_path: str | None = None,
    v552_temporal_key_source_index_path: str | None = None,
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    root = Path(output_root) / run_id
    root.mkdir(parents=True, exist_ok=True)
    packets_dir = root / "packets"
    audits_dir = root / "audits"
    schemas_dir = root / "schemas"
    manifest_dir = root / "manifest"
    for path in (packets_dir, audits_dir, schemas_dir, manifest_dir):
        path.mkdir(parents=True, exist_ok=True)

    v551j_root = Path(v551j_run_root)
    certified = read_table(v551j_root / "packets" / "v551j_certified_packet_index.parquet")
    if certified.empty:
        certified = read_table(v551j_root / "packets" / "v551j_certified_packet_index.csv")
    sidecar = read_table(v551j_root / "packets" / "v551j_reviewable_evidence_sidecar.parquet")
    if sidecar.empty:
        sidecar = read_table(v551j_root / "packets" / "v551j_reviewable_evidence_sidecar.csv")
    review_readiness = _load_optional(v551j_root / "manifest" / "v551j_review_readiness_report.json")
    certification_readiness = _load_optional(v551j_root / "manifest" / "v551j_certification_readiness_report.json")
    provenance_manifest = _load_optional(v551j_root / "manifest" / "v551j_input_provenance_manifest.json")
    comparability_context = _build_comparability_context(
        _load_optional(Path(v551j_comparison_root) / "manifest" / "v551j_cross_wave_comparability_report.json") if v551j_comparison_root else pd.DataFrame(),
        run_id,
    )
    resolved_v552_paths = _resolve_v552_structural_artifact_paths(
        v552_artifact_authority_index_path=v552_artifact_authority_index_path,
        v552_structural_fact_index_path=v552_structural_fact_index_path,
        v552_temporal_key_source_index_path=v552_temporal_key_source_index_path,
    )
    v552_artifact_authority_index_path = str(v552_artifact_authority_index_path) if v552_artifact_authority_index_path else None
    v552_structural_fact_index_path = str(resolved_v552_paths["v552_structural_fact_index_path"]) if resolved_v552_paths["v552_structural_fact_index_path"] else None
    v552_temporal_key_source_index_path = str(resolved_v552_paths["v552_temporal_key_source_index_path"]) if resolved_v552_paths["v552_temporal_key_source_index_path"] else None

    v552_inputs = {
        "v552_question_semantic_hierarchy_path": v552_question_semantic_hierarchy_path,
        "v552_structural_channel_index_path": v552_structural_channel_index_path,
        "v552_relation_axis_pressure_path": v552_relation_axis_pressure_path,
        "v552_target_entity_pressure_path": v552_target_entity_pressure_path,
        "v552_driver_facet_pressure_path": v552_driver_facet_pressure_path,
        "v552_contradiction_surface_path": v552_contradiction_surface_path,
        "v552_horizon_constraint_index_path": v552_horizon_constraint_index_path,
        "v552_parent_prior_manifest_path": v552_parent_prior_manifest_path,
        "v552_artifact_authority_index_path": v552_artifact_authority_index_path,
        "v552_known_absence_register_path": v552_known_absence_register_path,
        "v552_structural_fact_index_path": v552_structural_fact_index_path,
        "v552_temporal_key_source_index_path": v552_temporal_key_source_index_path,
    }
    supplied_optional = [name for name, value in v552_inputs.items() if value]
    missing_optional = [name for name, value in v552_inputs.items() if not value]
    supplied_v552_context = any(bool(value) for value in v552_inputs.values())

    input_artifact_records: list[dict[str, Any]] = []
    v551j_required_paths = {
        "v551j_certified_packet_index": v551j_root / "packets" / "v551j_certified_packet_index.parquet",
        "v551j_reviewable_evidence_sidecar": v551j_root / "packets" / "v551j_reviewable_evidence_sidecar.parquet",
        "v551j_certification_readiness_report": v551j_root / "manifest" / "v551j_certification_readiness_report.json",
        "v551j_review_readiness_report": v551j_root / "manifest" / "v551j_review_readiness_report.json",
        "v551j_packet_readiness_report": v551j_root / "manifest" / "v551j_packet_readiness_report.json",
        "v551j_input_provenance_manifest": v551j_root / "manifest" / "v551j_input_provenance_manifest.json",
    }
    v551j_optional_paths = {
        "v551j_packet_review_surface": v551j_root / "packets" / "v551j_packet_review_surface.parquet",
        "v551j_certification_audit": v551j_root / "audits" / "v551j_certification_audit.parquet",
        "v551j_certification_rejection_audit": v551j_root / "audits" / "v551j_certification_rejection_audit.parquet",
        "v551j_forbidden_inference_audit": v551j_root / "audits" / "v551j_forbidden_inference_audit.parquet",
        "v551j_v552_context_join_audit": v551j_root / "audits" / "v551j_v552_context_join_audit.parquet",
    }
    artifact_mode = _artifact_mode_from_inputs(
        supplied_v552_context=supplied_v552_context,
        comparability_status=_clean(comparability_context.get("status")) or "not_supplied",
        required_inputs_present=all(path.exists() for path in v551j_required_paths.values()),
    )
    for artifact_name, path in v551j_required_paths.items():
        input_artifact_records.append(
            _input_artifact_record(
                run_id=run_id,
                artifact_name=artifact_name,
                path=path,
                required_for_mode="adapter_preflight",
                authority_class="v551j_authority",
                read_permission="required",
                failure_if_missing="BLOCKED_V552J_MISSING_REQUIRED_INPUTS",
                artifact_mode=artifact_mode,
            )
        )
    for artifact_name, path in v551j_optional_paths.items():
        input_artifact_records.append(
            _input_artifact_record(
                run_id=run_id,
                artifact_name=artifact_name,
                path=path,
                required_for_mode="adapter_preflight",
                authority_class="v551j_audit_authority",
                read_permission="optional",
                failure_if_missing="gap_only",
                artifact_mode=artifact_mode,
            )
        )
    for artifact_name, value in v552_inputs.items():
        path = Path(value) if value else None
        input_artifact_records.append(
            _input_artifact_record(
                run_id=run_id,
                artifact_name=artifact_name,
                path=path,
                required_for_mode="v553_temporal_input_candidate" if comparability_context.get("status") != "not_supplied" else "single_wave_structural_handoff",
                authority_class="v552_structural_authority",
                read_permission="optional",
                failure_if_missing="gap_only",
                artifact_mode=artifact_mode,
            )
        )
    if v551j_comparison_root:
        comparison_path = Path(v551j_comparison_root) / "manifest" / "v551j_cross_wave_comparability_report.json"
        input_artifact_records.append(
            _input_artifact_record(
                run_id=run_id,
                artifact_name="v551j_cross_wave_comparability_report",
                path=comparison_path,
                required_for_mode="v553_temporal_input_candidate",
                authority_class="comparability_authority",
                read_permission="optional",
                failure_if_missing="comparison_missing",
                artifact_mode=artifact_mode,
            )
        )
    input_artifact_index_df = pd.DataFrame(input_artifact_records, columns=V552J_INPUT_ARTIFACT_AUDIT_SCHEMA["required_columns"])
    required_input_mask = (
        input_artifact_index_df["required_for_mode"].astype(str).eq("adapter_preflight")
        & input_artifact_index_df["read_permission"].astype(str).eq("required")
    )
    required_input_records = input_artifact_index_df[required_input_mask].copy()
    required_inputs_present = bool(
        not required_input_records.empty
        and required_input_records["present"].astype(bool).all()
    )
    missing_required_inputs = (
        required_input_records.loc[~required_input_records["present"].astype(bool), "artifact_name"]
        .astype(str)
        .tolist()
    )
    comparability_present = bool(
        v551j_comparison_root
        and (Path(v551j_comparison_root) / "manifest" / "v551j_cross_wave_comparability_report.json").exists()
    )
    v552_context_profile = _v552_context_profile_from_inputs(v552_inputs, comparability_present)
    upstream_provenance_links = _upstream_provenance_links(v551j_root, v551j_comparison_root, v552_inputs)
    upstream_provenance_links_json = _json_object(upstream_provenance_links)
    command_provenance = capture_run_provenance(
        input_documents={
            "v551j_run_root": str(v551j_root),
            "v551j_comparison_root": str(v551j_comparison_root or ""),
            "v552_question_semantic_hierarchy_path": v552_question_semantic_hierarchy_path or "",
            "v552_structural_channel_index_path": v552_structural_channel_index_path or "",
            "v552_relation_axis_pressure_path": v552_relation_axis_pressure_path or "",
            "v552_target_entity_pressure_path": v552_target_entity_pressure_path or "",
            "v552_driver_facet_pressure_path": v552_driver_facet_pressure_path or "",
            "v552_contradiction_surface_path": v552_contradiction_surface_path or "",
            "v552_horizon_constraint_index_path": v552_horizon_constraint_index_path or "",
            "v552_parent_prior_manifest_path": v552_parent_prior_manifest_path or "",
            "v552_artifact_authority_index_path": v552_artifact_authority_index_path or "",
            "v552_known_absence_register_path": v552_known_absence_register_path or "",
            "v552_structural_fact_index_path": v552_structural_fact_index_path or "",
            "v552_temporal_key_source_index_path": v552_temporal_key_source_index_path or "",
        }
    )
    v552_structural_fact_index = _load_optional(v552_structural_fact_index_path)
    v552_temporal_key_source_index = _load_optional(v552_temporal_key_source_index_path)

    packet_bundle_rows = _bundle_bundle_rows(certified, sidecar)
    packet_bundle_summary = {
        "certified_packet_rows": int(len(certified)),
        "reviewable_sidecar_rows": int(len(sidecar)),
        "bundle_rows": int(len(packet_bundle_rows)),
        "certified_present": bool(len(certified)),
        "reviewable_present": bool(len(sidecar)),
        "bundle_packet_ids_json": _json_array(packet_bundle_rows.get("packet_id", pd.Series(dtype=str)).astype(str).tolist() if not packet_bundle_rows.empty and "packet_id" in packet_bundle_rows.columns else []),
        "bundle_statuses_json": _json_array(packet_bundle_rows.get("packet_status", pd.Series(dtype=str)).astype(str).tolist() if not packet_bundle_rows.empty and "packet_status" in packet_bundle_rows.columns else []),
        "bundle_context_mode": "temporal_primary" if not v552_temporal_key_source_index.empty else "packet_bundle_fallback",
    }
    if not v552_temporal_key_source_index.empty:
        primary_rows = v552_temporal_key_source_index.copy()
        primary_mode = "temporal"
    elif not packet_bundle_rows.empty:
        primary_rows = packet_bundle_rows.copy()
        primary_mode = "packet_bundle"
    else:
        primary_rows = pd.DataFrame(
            [
                {
                    "packet_id": f"v552j__{run_id}",
                    "source": "unknown",
                    "wave": _clean(provenance_manifest.iloc[0].get("wave") if not provenance_manifest.empty else ""),
                    "canonical_wave": _clean(provenance_manifest.iloc[0].get("canonical_wave") if not provenance_manifest.empty else ""),
                    "country_code": _clean(provenance_manifest.iloc[0].get("country_code") if not provenance_manifest.empty else ""),
                }
            ]
        )
        primary_mode = "packet_bundle"

    constraint_rows: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []
    absence_rows: list[dict[str, Any]] = []
    uncertainty_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    leakage_rows: list[dict[str, Any]] = []
    permission_boundary_rows: list[dict[str, Any]] = []
    status_conflict_rows: list[dict[str, Any]] = []
    blocker_context_breakdown_rows: list[dict[str, Any]] = []
    blocker_contexts_seen: list[str] = []
    v553_input_index_rows: list[dict[str, Any]] = []

    for _, row in primary_rows.iterrows():
        if primary_mode == "temporal":
            normalized = _temporal_normalization_bundle(row, comparability_context, supplied_v552_context)
            packet_row = pd.Series({**row.to_dict(), **normalized})
            packet_id = _clean(packet_row.get("v552_temporal_key_source_id")) or _clean(packet_row.get("v552_structural_fact_id")) or _clean(packet_row.get("source_row_id")) or f"v552j__{run_id}"
            packet_row["packet_id"] = packet_id
            packet_row["v552j_packet_id"] = packet_id
            packet_type = "structural_constraint_packet" if bool(packet_row.get("constraint_eligibility", False)) else "structural_context_packet"
            packet_status = "candidate" if bool(packet_row.get("constraint_eligibility", False)) else "context"
            source = _clean(packet_row.get("source")) or "unknown"
            wave = _clean(packet_row.get("wave")) or _clean(provenance_manifest.iloc[0].get("wave") if not provenance_manifest.empty and "wave" in provenance_manifest.columns else "")
            canonical_wave = _clean(packet_row.get("canonical_wave")) or wave
            country_code = _clean(packet_row.get("country_code"))
        else:
            normalized = _normalization_bundle(row, comparability_context, supplied_v552_context)
            packet_row = pd.Series({**row.to_dict(), **normalized})
            packet_id = _clean(packet_row.get("packet_id")) or f"v552j__{run_id}"
            packet_type = _clean(packet_row.get("packet_type")) or "structural_handoff_packet"
            packet_status = _clean(packet_row.get("packet_status")) or "candidate"
            source = _clean(packet_row.get("source")) or "unknown"
            wave = _clean(packet_row.get("wave")) or _clean(provenance_manifest.iloc[0].get("wave") if not provenance_manifest.empty and "wave" in provenance_manifest.columns else "")
            canonical_wave = _clean(packet_row.get("canonical_wave")) or wave
            country_code = _clean(packet_row.get("country_code"))
        structural_resolution = _packet_structural_dimension_resolution(packet_row, v552_structural_fact_index, v552_temporal_key_source_index)
        downstream_mediation = _determine_required_mediation(packet_row)
        if primary_mode == "temporal":
            packet_ready_for_v553 = bool(packet_row.get("constraint_eligibility", False))
            ready_for_v553_probe = bool(packet_row.get("context_eligibility", False))
            ready_for_v553_temporal_field = bool(packet_row.get("constraint_eligibility", False) and comparability_context.get("status") != "not_supplied")
            handoff_status = "ready" if packet_ready_for_v553 else "ready_with_gaps"
            constraint_status = "constraint_recorded" if packet_ready_for_v553 else "constraint_recorded_with_gaps"
            missing_context_text = "" if packet_ready_for_v553 else "temporal_probe_only"
        else:
            handoff_status, constraint_status, missing_context_text = _derived_status(packet_row, comparability_context, supplied_v552_context)
        context_breakdown = _context_breakdown(packet_row, comparability_context, supplied_v552_context)
        known_absences = _parse_json_array(packet_row.get("known_absences_json"))
        forbidden_claims = _parse_json_array(packet_row.get("forbidden_claim_ids_json"))
        review_status = _clean(packet_row.get("normalized_v551j_review_status")) or "not_supplied"
        certification_status = _clean(packet_row.get("normalized_v551j_certification_status")) or "unknown"
        runtime_use_class = "structural_handoff_only"
        if primary_mode != "temporal":
            packet_ready_for_v553 = (
                certification_status == "certified"
                and _clean(packet_row.get("normalized_v551j_lane")) == "certified_spine"
                and bool(packet_row.get("constraint_eligibility", False))
                and _clean(packet_row.get("permission_class")) == "v553_constraint_candidate"
                and not bool(packet_row.get("blocked_from_downstream", False))
                and not bool(packet_row.get("status_conflict_flag", False))
                and handoff_status == "ready"
                and constraint_status == "constraint_recorded"
                and bool(packet_id)
            )
            structural_dimensions_resolved_for_v553 = _clean(structural_resolution.get("structural_dimension_status")) == "resolved"
            ready_for_v553_probe = bool(
                packet_ready_for_v553
                or supplied_v552_context
                or structural_dimensions_resolved_for_v553
                or _clean(structural_resolution.get("v552_structural_match_status")) in {"question_match_only", "broad_context_match"}
            )
            ready_for_v553_temporal_field = bool(
                packet_ready_for_v553
                and comparability_context.get("status") != "not_supplied"
                and structural_dimensions_resolved_for_v553
                and _clean(structural_resolution.get("v552_structural_match_status")) in {"exact_structural_match", "partial_structural_match"}
                and not bool(packet_row.get("blocked_from_downstream", False))
                and not bool(packet_row.get("status_conflict_flag", False))
            )
        else:
            structural_dimensions_resolved_for_v553 = bool(packet_row.get("allowed_for_v553_probe", False))
            ready_for_v553_probe = bool(packet_row.get("allowed_for_v553_probe", False))
            ready_for_v553_temporal_field = bool(packet_row.get("allowed_for_v553_temporal_field", False) and comparability_context.get("status") != "not_supplied")
        score_bundle = _packet_score_bundle(packet_row, comparability_context, packet_ready_for_v553)
        runtime_safe_for_app = False
        blocker_contexts = _blocker_contexts(packet_row, comparability_context, supplied_v552_context)
        for context in blocker_contexts:
            if context not in blocker_contexts_seen:
                blocker_contexts_seen.append(context)
        blocker_context_breakdown_rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "required_blockers_json": context_breakdown["required_blockers_json"],
                "required_blocker_count": context_breakdown["required_blocker_count"],
                "optional_contexts_json": context_breakdown["optional_contexts_json"],
                "optional_context_count": context_breakdown["optional_context_count"],
                "comparability_status": context_breakdown["comparability_status"],
                "v552_context_supplied": context_breakdown["v552_context_supplied"],
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )
        structural_resolution = _packet_structural_dimension_resolution(packet_row, v552_structural_fact_index, v552_temporal_key_source_index)
        structural_absence_status = "recorded" if known_absences or missing_context_text else "clear"
        structural_uncertainty_status = "recorded" if missing_context_text or review_status in {"blocked", "diagnostic_only", "not_supplied"} else "minimal"
        uncertainty_score = 1.0 if structural_uncertainty_status == "recorded" else 0.2
        certainty_score = 0.0 if structural_uncertainty_status == "recorded" else 0.8
        source_packet_id = packet_id
        evidence_ledger = {
            "v551j_review_surface_status": review_status,
            "v551j_evidence_certification_status": certification_status,
            "support_status": _clean(packet_row.get("normalized_support_status")),
        }
        authority_ledger = {
            "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
            "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
            "permission_class": _clean(packet_row.get("permission_class")),
        }
        absence_uncertainty_ledger = {
            "known_absences": known_absences,
            "missing_context_text": missing_context_text,
            "structural_absence_status": structural_absence_status,
            "structural_uncertainty_status": structural_uncertainty_status,
        }
        generation_ledger = {
            "generated_personhood": False,
            "generated_psyche": False,
            "generated_runtime_content": False,
        }
        constraint_payload = {
            "packet_id": packet_id,
            "packet_type": packet_type,
            "packet_status": packet_status,
            "source": source,
            "wave": wave,
            "canonical_wave": canonical_wave,
            "country_code": country_code,
            "packet_ready_for_v553": packet_ready_for_v553,
            "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
            "ready_for_v553_probe": ready_for_v553_probe,
            "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
            "ready_for_v553": packet_ready_for_v553,
            "missing_context_text": missing_context_text,
            "blocker_contexts": blocker_contexts,
        }

        constraint_rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "source_packet_id": source_packet_id,
                "packet_type": packet_type,
                "packet_status": packet_status,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "v551j_evidence_certification_status": _clean(packet_row.get("v551j_evidence_certification_status")) or _clean(packet_row.get("certification_status")) or certification_status,
                "v551j_review_surface_status": _clean(packet_row.get("v551j_review_surface_status")) or _clean(packet_row.get("review_surface_status")) or review_status,
                "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                "normalized_v551j_certification_status": certification_status,
                "normalized_v551j_review_status": review_status,
                "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                "normalized_v552_context_status": _clean(packet_row.get("normalized_v552_context_status")),
                "normalized_comparability_status": _clean(packet_row.get("normalized_comparability_status")),
                "permission_class": _clean(packet_row.get("permission_class")),
                "constraint_eligibility": bool(packet_row.get("constraint_eligibility", False)),
                "context_eligibility": bool(packet_row.get("context_eligibility", False)),
                "forensic_eligibility": bool(packet_row.get("forensic_eligibility", False)),
                "blocked_from_downstream": bool(packet_row.get("blocked_from_downstream", False)),
                "status_conflict_flag": bool(packet_row.get("status_conflict_flag", False)),
                "status_conflict_reason": _clean(packet_row.get("status_conflict_reason")),
                "structural_handoff_status": handoff_status,
                "structural_constraint_status": constraint_status,
                "structural_constraint_reason": missing_context_text,
                "structural_constraint_type": "single_wave_structural_constraint" if packet_ready_for_v553 else "contextual_structural_constraint",
                "structural_constraint_scope": "single_wave",
                "structural_constraint_payload_json": _json_object(constraint_payload),
                "runtime_use_class": runtime_use_class,
                "runtime_safe_for_app": runtime_safe_for_app,
                **score_bundle,
                "packet_ready_for_v553": packet_ready_for_v553,
                "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                "ready_for_v553_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                "ready_for_v553": packet_ready_for_v553,
                "ready_for_v553_single_wave_probe": ready_for_v553_probe,
                "required_downstream_mediation_json": _json_array(downstream_mediation),
                "required_downstream_layers_json": _json_array(["v553"] if packet_ready_for_v553 else ["v553", "v554"]),
                "known_absences_json": _json_array(known_absences),
                "forbidden_claim_ids_json": _json_array(forbidden_claims or V552J_FORBIDDEN_CLAIM_IDS),
                "evidence_ledger_json": _ledger_json(evidence_ledger),
                "authority_ledger_json": _ledger_json(authority_ledger),
                "absence_uncertainty_ledger_json": _ledger_json(absence_uncertainty_ledger),
                "generation_ledger_json": _ledger_json(generation_ledger),
                "comparability_status": comparability_context.get("status", "not_supplied"),
                "comparability_summary_json": json.dumps(comparability_context, sort_keys=True, ensure_ascii=False),
                "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
                "v552_context_source_json": _json_array([name for name, value in v552_inputs.items() if value]),
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )

        if not packet_ready_for_v553 or review_status in {"reviewable", "diagnostic_only", "blocked", "not_supplied"}:
            context_rows.append(
                {
                    "run_id": run_id,
                    "v552j_packet_id": packet_id,
                    "packet_id": packet_id,
                    "source_packet_id": source_packet_id,
                    "packet_type": "structural_context_packet",
                    "packet_status": "context",
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                    "normalized_v551j_certification_status": certification_status,
                    "normalized_v551j_review_status": review_status,
                    "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                    "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                    "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                    "normalized_v552_context_status": _clean(packet_row.get("normalized_v552_context_status")),
                    "normalized_comparability_status": _clean(packet_row.get("normalized_comparability_status")),
                    "permission_class": _clean(packet_row.get("permission_class")),
                    "context_only": True,
                    "assertion_allowed": False,
                    "structural_context_type": "reviewable_context" if review_status.startswith("reviewable") else ("diagnostic_forensic" if review_status == "diagnostic_only" else "blocked_context"),
                    "structural_context_scope": "single_wave",
                    "structural_context_payload_json": _json_object({
                        "packet_id": packet_id,
                        "source": source,
                        "wave": wave,
                        "canonical_wave": canonical_wave,
                        "country_code": country_code,
                        "review_status": review_status,
                        "blocked_from_downstream": bool(packet_row.get("blocked_from_downstream", False)),
                        "status_conflict_flag": bool(packet_row.get("status_conflict_flag", False)),
                        "blocker_contexts": blocker_contexts,
                    }),
                    "runtime_use_class": "review_only" if review_status.startswith("reviewable") else "not_runtime_consumable",
                    "packet_ready_for_v553": packet_ready_for_v553,
                    "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                    "ready_for_v553_probe": ready_for_v553_probe,
                    "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                    "ready_for_v553": packet_ready_for_v553,
                    "ready_for_v553_single_wave_probe": ready_for_v553_probe,
                    **score_bundle,
                    "required_downstream_mediation_json": _json_array(downstream_mediation),
                    "known_absences_json": _json_array(known_absences),
                    "forbidden_claim_ids_json": _json_array(forbidden_claims or V552J_FORBIDDEN_CLAIM_IDS),
                    "evidence_ledger_json": _ledger_json(evidence_ledger),
                    "authority_ledger_json": _ledger_json(authority_ledger),
                    "absence_uncertainty_ledger_json": _ledger_json(absence_uncertainty_ledger),
                    "generation_ledger_json": _ledger_json(generation_ledger),
                    "comparability_status": comparability_context.get("status", "not_supplied"),
                    "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
                    "created_at": utc_now(),
                    "schema_version": V552J_SCHEMA_VERSION,
                    "compiler_version": V552J_COMPILER_VERSION,
                }
            )

        absence_rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                "normalized_v551j_certification_status": certification_status,
                "normalized_v551j_review_status": review_status,
                "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                "normalized_v552_context_status": _clean(packet_row.get("normalized_v552_context_status")),
                "normalized_comparability_status": _clean(packet_row.get("normalized_comparability_status")),
                "permission_class": _clean(packet_row.get("permission_class")),
                "constraint_eligibility": bool(packet_row.get("constraint_eligibility", False)),
                "context_eligibility": bool(packet_row.get("context_eligibility", False)),
                "forensic_eligibility": bool(packet_row.get("forensic_eligibility", False)),
                "blocked_from_downstream": bool(packet_row.get("blocked_from_downstream", False)),
                "status_conflict_flag": bool(packet_row.get("status_conflict_flag", False)),
                "status_conflict_reason": _clean(packet_row.get("status_conflict_reason")),
                "packet_ready_for_v553": packet_ready_for_v553,
                "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                "ready_for_v553_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                **score_bundle,
                "structural_absence_status": structural_absence_status,
                "absence_reason": missing_context_text or "known absences preserved",
                "known_absences_json": _json_array(known_absences),
                "missing_input_fields_json": _json_array(missing_optional + (["v551j_comparability"] if comparability_context.get("status") == "not_supplied" else [])),
                "forbidden_claim_ids_json": _json_array(forbidden_claims or V552J_FORBIDDEN_CLAIM_IDS),
                "comparability_status": comparability_context.get("status", "not_supplied"),
                "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )

        permission_boundary_rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                "normalized_v551j_certification_status": certification_status,
                "normalized_v551j_review_status": review_status,
                "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                "permission_class": _clean(packet_row.get("permission_class")),
                "context_only": not packet_ready_for_v553,
                "assertion_allowed": packet_ready_for_v553,
                "read_permission": "assertion" if packet_ready_for_v553 else "context",
                "packet_ready_for_v553": packet_ready_for_v553,
                "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                "ready_for_v553_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                "blocked_from_downstream": bool(packet_row.get("blocked_from_downstream", False)),
                "ready_for_v553": packet_ready_for_v553,
                "ready_for_v553_single_wave_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                **score_bundle,
                "blocking_reason": missing_context_text or ("status_conflict" if bool(packet_row.get("status_conflict_flag", False)) else ""),
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )

        if not packet_ready_for_v553 or bool(packet_row.get("blocked_from_downstream", False)) or bool(packet_row.get("status_conflict_flag", False)):
            leakage_rows.append(
                {
                    "run_id": run_id,
                    "v552j_packet_id": packet_id,
                    "packet_id": packet_id,
                    "claim_id": "blocked_from_v553",
                    "claim_group": "permission_boundary",
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "leakage_type": "blocked_boundary",
                    "leakage_reason": missing_context_text or "permission boundary preserved",
                    "source_field": "ready_for_v553" if packet_ready_for_v553 else "blocked_from_downstream",
                    "blocked": True,
                    "created_at": utc_now(),
                    "schema_version": V552J_SCHEMA_VERSION,
                    "compiler_version": V552J_COMPILER_VERSION,
                }
            )

        if ready_for_v553_temporal_field:
            v553_handoff_mode = "temporal_field_ready"
            v553_handoff_allowed = True
            v553_probe_allowed = True
            v553_temporal_field_allowed = True
            v553_handoff_blocked_reason = ""
        elif ready_for_v553_probe:
            v553_handoff_mode = "probe_only"
            v553_handoff_allowed = True
            v553_probe_allowed = True
            v553_temporal_field_allowed = False
            v553_handoff_blocked_reason = "comparability_not_yet_established"
        elif structural_dimensions_resolved_for_v553:
            v553_handoff_mode = "blocked_context"
            v553_handoff_allowed = True
            v553_probe_allowed = False
            v553_temporal_field_allowed = False
            v553_handoff_blocked_reason = (
                structural_resolution["structural_dimension_blocker_reason"]
                or missing_context_text
                or ("comparability_missing" if comparability_context.get("status") == "not_supplied" else "blocked_from_downstream")
            )
        else:
            v553_handoff_mode = "diagnostic_only"
            v553_handoff_allowed = False
            v553_probe_allowed = False
            v553_temporal_field_allowed = False
            v553_handoff_blocked_reason = (
                structural_resolution["structural_dimension_blocker_reason"]
                or missing_context_text
                or ("comparability_missing" if comparability_context.get("status") == "not_supplied" else "blocked_from_downstream")
            )

        if _clean(structural_resolution.get("source_v552_structural_fact_lane")) == "audit_fact":
            v553_handoff_mode = "diagnostic_only"
            v553_handoff_allowed = False
            v553_probe_allowed = False
            v553_temporal_field_allowed = False
            v553_handoff_blocked_reason = "audit_fact_diagnostic_only"
            packet_ready_for_v553 = False
            ready_for_v553_probe = False
            ready_for_v553_temporal_field = False

        v553_input_index_rows.append(
            {
                "run_id": run_id,
                "v553_input_id": f"{run_id}__v553_input_{len(v553_input_index_rows)+1:07d}",
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "packet_class": "structural_constraint_packet" if packet_ready_for_v553 else "structural_context_packet",
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "source_v552_artifact": structural_resolution["source_v552_artifact"],
                "source_v552_structural_fact_id": structural_resolution["source_v552_structural_fact_id"],
                "source_v552_structural_fact_ids_json": structural_resolution["source_v552_structural_fact_ids_json"],
                "source_v552_structural_fact_ids_diagnostic_json": structural_resolution["source_v552_structural_fact_ids_diagnostic_json"],
                "source_v552_temporal_key_source_id": structural_resolution["source_v552_temporal_key_source_id"],
                "source_v552_temporal_key_source_ids_json": structural_resolution["source_v552_temporal_key_source_ids_json"],
                "source_v552_structural_fact_status": structural_resolution["source_v552_structural_fact_status"],
                "source_v552_structural_fact_lane": structural_resolution["source_v552_structural_fact_lane"],
                "source_v552_structural_fact_grain": structural_resolution["source_v552_structural_fact_grain"],
                "structural_dimension_status": structural_resolution["structural_dimension_status"],
                "structural_dimension_blocker_reason": structural_resolution["structural_dimension_blocker_reason"],
                "relation_axis_id": structural_resolution["relation_axis_id"],
                "target_entity_id": structural_resolution["target_entity_id"],
                "driver_facet_id": structural_resolution["driver_facet_id"],
                "structural_channel_id": structural_resolution["structural_channel_id"],
                "horizon_constraint_id": structural_resolution["horizon_constraint_id"],
                "semantic_signature": structural_resolution["semantic_signature"],
                "v552_structural_match_status": structural_resolution["v552_structural_match_status"],
                "v552_structural_match_score": structural_resolution["v552_structural_match_score"],
                "v552_structural_match_reason": structural_resolution["v552_structural_match_reason"],
                "matched_fact_count": structural_resolution["matched_fact_count"],
                "broad_match_count": structural_resolution["broad_match_count"],
                "temporal_key_basis": structural_resolution["temporal_key_basis"],
                "temporal_key_candidate_status": structural_resolution["temporal_key_candidate_status"],
                "temporal_key_blocker_reason": structural_resolution["temporal_key_blocker_reason"],
                "fallback_permission_profile_key": structural_resolution["fallback_permission_profile_key"],
                "read_permission": "assertion" if packet_ready_for_v553 else "context",
                "must_temporalize": bool(packet_ready_for_v553 and comparability_context.get("status") != "not_supplied"),
                "single_wave_probe_allowed": bool(supplied_v552_context),
                "temporal_field_allowed": bool(ready_for_v553_temporal_field),
                "temporal_anchor_required": bool(ready_for_v553_temporal_field),
                "comparability_required": bool(ready_for_v553_temporal_field),
                "comparability_status": comparability_context.get("status", "not_supplied"),
                "packet_ready_for_v553": packet_ready_for_v553,
                "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                "ready_for_v553_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                "v553_handoff_mode": v553_handoff_mode,
                "v553_handoff_allowed": v553_handoff_allowed,
                "v553_probe_allowed": v553_probe_allowed,
                "v553_temporal_field_allowed": v553_temporal_field_allowed,
                "v553_handoff_blocked_reason": v553_handoff_blocked_reason,
                **score_bundle,
                "constraint_payload_ref": f"packets/v552j_structural_constraint_packet.parquet#{packet_id}" if packet_ready_for_v553 else "",
                "uncertainty_payload_ref": f"packets/v552j_structural_uncertainty_packet.parquet#{packet_id}",
                "absence_payload_ref": f"packets/v552j_structural_absence_packet.parquet#{packet_id}",
                "blocking_reason": structural_resolution["structural_dimension_blocker_reason"] or missing_context_text or ("comparability_missing" if comparability_context.get("status") == "not_supplied" else ""),
                "required_temporal_context_json": _json_object(
                    {
                        "comparability_status": comparability_context.get("status", "not_supplied"),
                        "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
                        "blocker_contexts": blocker_contexts,
                        "structural_dimension_status": structural_resolution["structural_dimension_status"],
                        "source_v552_structural_fact_ids_json": structural_resolution["source_v552_structural_fact_ids_json"],
                        "source_v552_structural_fact_ids_diagnostic_json": structural_resolution["source_v552_structural_fact_ids_diagnostic_json"],
                        "packet_bundle_context": packet_bundle_summary,
                    }
                ),
                "packet_ready_for_v553": packet_ready_for_v553,
                "structural_dimensions_resolved_for_v553": structural_dimensions_resolved_for_v553,
                "ready_for_v553_probe": ready_for_v553_probe,
                "ready_for_v553_temporal_field": ready_for_v553_temporal_field,
                "ready_for_v553": packet_ready_for_v553,
                "ready_for_runtime_consumption": False,
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )

        uncertainty_rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": packet_id,
                "packet_id": packet_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                "normalized_v551j_certification_status": certification_status,
                "normalized_v551j_review_status": review_status,
                "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                "normalized_v552_context_status": _clean(packet_row.get("normalized_v552_context_status")),
                "normalized_comparability_status": _clean(packet_row.get("normalized_comparability_status")),
                "permission_class": _clean(packet_row.get("permission_class")),
                "constraint_eligibility": bool(packet_row.get("constraint_eligibility", False)),
                "context_eligibility": bool(packet_row.get("context_eligibility", False)),
                "forensic_eligibility": bool(packet_row.get("forensic_eligibility", False)),
                "blocked_from_downstream": bool(packet_row.get("blocked_from_downstream", False)),
                "status_conflict_flag": bool(packet_row.get("status_conflict_flag", False)),
                "status_conflict_reason": _clean(packet_row.get("status_conflict_reason")),
                "structural_uncertainty_status": structural_uncertainty_status,
                "uncertainty_reason": missing_context_text or "structural handoff constrained by provisional adapter",
                "uncertainty_score": uncertainty_score,
                "certainty_score": certainty_score,
                "runtime_use_class": runtime_use_class,
                "known_absences_json": _json_array(known_absences),
                "forbidden_claim_ids_json": _json_array(forbidden_claims or V552J_FORBIDDEN_CLAIM_IDS),
                "comparability_status": comparability_context.get("status", "not_supplied"),
                "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
                "created_at": utc_now(),
                "schema_version": V552J_SCHEMA_VERSION,
                "compiler_version": V552J_COMPILER_VERSION,
            }
        )

        for claim_id in forbidden_claims or V552J_FORBIDDEN_CLAIM_IDS:
            audit_rows.append(
                {
                    "run_id": run_id,
                    "v552j_packet_id": packet_id,
                    "packet_id": packet_id,
                    "claim_id": claim_id,
                    "claim_group": "runtime_forbidden",
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "reason": "provisional V552J must not emit runtime/person-level claims",
                    "created_at": utc_now(),
                    "schema_version": V552J_SCHEMA_VERSION,
                }
            )

        if packet_row.get("status_conflict_flag"):
            status_conflict_rows.append(
                {
                    "run_id": run_id,
                    "v552j_packet_id": packet_id,
                    "packet_id": packet_id,
                    "source_fields_json": _json_array(
                        [
                            "v551j_evidence_certification_status",
                            "v551j_review_surface_status",
                            "normalized_v551j_lane",
                            "normalized_v551j_certification_status",
                            "normalized_v551j_review_status",
                            "normalized_authority_status",
                            "normalized_directionality_status",
                            "normalized_support_status",
                            "normalized_v552_context_status",
                            "normalized_comparability_status",
                            "permission_class",
                        ]
                    ),
                    "observed_values_json": _json_object(
                        {
                            "v551j_evidence_certification_status": _clean(packet_row.get("v551j_evidence_certification_status")) or _clean(packet_row.get("certification_status")),
                            "v551j_review_surface_status": _clean(packet_row.get("v551j_review_surface_status")) or _clean(packet_row.get("review_surface_status")),
                            "normalized_v551j_lane": _clean(packet_row.get("normalized_v551j_lane")),
                            "normalized_v551j_certification_status": _clean(packet_row.get("normalized_v551j_certification_status")),
                            "normalized_v551j_review_status": _clean(packet_row.get("normalized_v551j_review_status")),
                            "normalized_authority_status": _clean(packet_row.get("normalized_authority_status")),
                            "normalized_directionality_status": _clean(packet_row.get("normalized_directionality_status")),
                            "normalized_support_status": _clean(packet_row.get("normalized_support_status")),
                            "normalized_v552_context_status": _clean(packet_row.get("normalized_v552_context_status")),
                            "normalized_comparability_status": _clean(packet_row.get("normalized_comparability_status")),
                            "permission_class": _clean(packet_row.get("permission_class")),
                        }
                    ),
                    "normalized_status": _clean(packet_row.get("normalized_v551j_lane")) or "conflict",
                    "normalization_rule_id": "V551J_STATUS_NORMALIZATION_V1",
                    "conflict_severity": "high",
                    "blocking_effect": "blocks_v552j_adapter",
                    "resolution_required": True,
                    "created_at": utc_now(),
                    "schema_version": V552J_SCHEMA_VERSION,
                    "compiler_version": V552J_COMPILER_VERSION,
                }
            )

    constraint_df = pd.DataFrame(constraint_rows, columns=V552J_STRUCTURAL_CONSTRAINT_PACKET_SCHEMA["required_columns"])
    context_df = pd.DataFrame(context_rows, columns=V552J_STRUCTURAL_CONTEXT_PACKET_SCHEMA["required_columns"])
    absence_df = pd.DataFrame(absence_rows, columns=V552J_STRUCTURAL_ABSENCE_PACKET_SCHEMA["required_columns"])
    uncertainty_df = pd.DataFrame(uncertainty_rows, columns=V552J_STRUCTURAL_UNCERTAINTY_PACKET_SCHEMA["required_columns"])
    audit_df = pd.DataFrame(audit_rows, columns=V552J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA["required_columns"])
    leakage_df = pd.DataFrame(leakage_rows, columns=V552J_DOWNSTREAM_LEAKAGE_AUDIT_SCHEMA["required_columns"])
    permission_boundary_df = pd.DataFrame(permission_boundary_rows, columns=V552J_PERMISSION_BOUNDARY_AUDIT_SCHEMA["required_columns"])
    status_conflict_df = pd.DataFrame(
        status_conflict_rows,
        columns=[
            "run_id",
            "v552j_packet_id",
            "packet_id",
            "source_fields_json",
            "observed_values_json",
            "normalized_status",
            "normalization_rule_id",
            "conflict_severity",
            "blocking_effect",
            "resolution_required",
            "created_at",
            "schema_version",
            "compiler_version",
        ],
    )
    input_artifact_audit_df = input_artifact_index_df.copy()
    v553_input_index_df = pd.DataFrame(v553_input_index_rows, columns=V552J_TO_V553_HANDOFF_INDEX_SCHEMA["required_columns"])
    if not v553_input_index_df.empty:
        v553_input_index_df = _normalize_v553_handoff_modes(v553_input_index_df)
    v553_input_row_count = int(len(v553_input_index_df))
    structural_dimensions_resolved_row_count = int(v553_input_index_df["structural_dimensions_resolved_for_v553"].astype(bool).sum()) if not v553_input_index_df.empty and "structural_dimensions_resolved_for_v553" in v553_input_index_df.columns else 0
    structural_dimensions_resolved_any = bool(structural_dimensions_resolved_row_count)
    structural_dimensions_resolved_all = bool(v553_input_row_count and structural_dimensions_resolved_row_count == v553_input_row_count)
    v553_probe_handoff_df = v553_input_index_df[v553_input_index_df["v553_probe_allowed"].astype(bool)].copy() if not v553_input_index_df.empty and "v553_probe_allowed" in v553_input_index_df.columns else pd.DataFrame(columns=v553_input_index_df.columns)
    v553_temporal_field_handoff_df = v553_input_index_df[v553_input_index_df["v553_temporal_field_allowed"].astype(bool)].copy() if not v553_input_index_df.empty and "v553_temporal_field_allowed" in v553_input_index_df.columns else pd.DataFrame(columns=v553_input_index_df.columns)
    to_v553_handoff_df = v553_input_index_df[v553_input_index_df["v553_handoff_allowed"].astype(bool)].copy() if not v553_input_index_df.empty and "v553_handoff_allowed" in v553_input_index_df.columns else pd.DataFrame(columns=v553_input_index_df.columns)
    probe_ready_row_count = int(v553_input_index_df["v553_probe_allowed"].astype(bool).sum()) if not v553_input_index_df.empty and "v553_probe_allowed" in v553_input_index_df.columns else 0
    if probe_ready_row_count > 0 and to_v553_handoff_df.empty:
        raise RuntimeError("V552J_PROBE_ROWS_DROPPED_FROM_V553_HANDOFF")
    def _index_frame(frame: pd.DataFrame, index_name: str, schema_columns: list[str]) -> pd.DataFrame:
        if frame.empty:
            return pd.DataFrame(columns=schema_columns)
        indexed = frame.copy()
        indexed.insert(1, "index_name", index_name)
        missing = [column for column in schema_columns if column not in indexed.columns]
        for column in missing:
            indexed[column] = ""
        return indexed.loc[:, schema_columns]

    structural_context_only_df = _index_frame(
        constraint_df[
            constraint_df["context_eligibility"].astype(bool)
            & ~constraint_df["constraint_eligibility"].astype(bool)
            & ~constraint_df["blocked_from_downstream"].astype(bool)
        ],
        "v552j_structural_context_only_index",
        V552J_STRUCTURAL_CONTEXT_ONLY_INDEX_SCHEMA["required_columns"],
    )
    review_only_df = _index_frame(
        constraint_df[
            constraint_df["normalized_v551j_review_status"].astype(str).str.startswith("reviewable")
            & ~constraint_df["blocked_from_downstream"].astype(bool)
        ],
        "v552j_review_only_index",
        V552J_REVIEW_ONLY_INDEX_SCHEMA["required_columns"],
    )
    diagnostic_only_df = _index_frame(
        constraint_df[
            constraint_df["normalized_v551j_lane"].astype(str).eq("diagnostic_forensic")
            | constraint_df["permission_class"].astype(str).eq("forensic_only")
        ],
        "v552j_diagnostic_only_index",
        V552J_DIAGNOSTIC_ONLY_INDEX_SCHEMA["required_columns"],
    )
    blocked_index_df = _index_frame(
        constraint_df[
            constraint_df["blocked_from_downstream"].astype(bool)
            | constraint_df["status_conflict_flag"].astype(bool)
            | constraint_df["normalized_v551j_lane"].astype(str).eq("blocked")
        ],
        "v552j_blocked_index",
        V552J_BLOCKED_INDEX_SCHEMA["required_columns"],
    )
    blocker_context_breakdown_df = pd.DataFrame(blocker_context_breakdown_rows)

    packet_rows = int(len(constraint_df))
    absence_rows_n = int(len(absence_df))
    uncertainty_rows_n = int(len(uncertainty_df))
    forbidden_rows = int(len(audit_df))
    status_conflict_rows_n = int(len(status_conflict_df))
    structural_context_only_rows_n = int(len(structural_context_only_df))
    review_only_rows_n = int(len(review_only_df))
    diagnostic_only_rows_n = int(len(diagnostic_only_df))
    blocked_index_rows_n = int(len(blocked_index_df))
    probe_handoff_rows_n = int(len(v553_probe_handoff_df))
    temporal_field_handoff_rows_n = int(len(v553_temporal_field_handoff_df))
    to_v553_handoff_rows_n = int(len(to_v553_handoff_df))
    constraint_rows_n = packet_rows
    forensic_rows_n = int(len(diagnostic_only_df) + len(audit_df) + len(status_conflict_df))
    forbidden_leakage_rows_n = int(len(leakage_df))
    ready_for_v553 = bool(packet_rows and (constraint_df["ready_for_v553"].astype(bool).any() if "ready_for_v553" in constraint_df.columns else False))
    forbidden_claim_validation_status = "complete"
    forbidden_claim_validation_counts: dict[str, int] = {}
    if not constraint_df.empty and "forbidden_claim_ids_json" in constraint_df.columns:
        observed_forbidden = constraint_df["forbidden_claim_ids_json"].astype(str).tolist()
        statuses: list[str] = []
        for item in observed_forbidden:
            try:
                claims = json.loads(item)
            except Exception:
                claims = []
            if not isinstance(claims, list) or not claims:
                statuses.append("missing")
                continue
            normalized = [str(value).strip() for value in claims if str(value).strip()]
            expected = [str(value).strip() for value in V552J_FORBIDDEN_CLAIM_IDS if str(value).strip()]
            if set(normalized) == set(expected) and len(normalized) == len(expected):
                statuses.append("complete")
            else:
                statuses.append("partial")
        forbidden_claim_validation_counts = {str(key): int(value) for key, value in pd.Series(statuses).value_counts().sort_index().items()}
        if statuses and all(status == "missing" for status in statuses):
            forbidden_claim_validation_status = "missing"
        elif statuses and not all(status == "complete" for status in statuses):
            forbidden_claim_validation_status = "partial"
    aggregate_score_summary = {
        "mean_certification_score": float(pd.to_numeric(constraint_df.get("certification_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_support_score": float(pd.to_numeric(constraint_df.get("support_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_directionality_score": float(pd.to_numeric(constraint_df.get("directionality_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_authority_score": float(pd.to_numeric(constraint_df.get("authority_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_comparability_score": float(pd.to_numeric(constraint_df.get("comparability_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_confidence_score": float(pd.to_numeric(constraint_df.get("confidence_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
        "mean_readiness_score": float(pd.to_numeric(constraint_df.get("readiness_score", pd.Series(dtype=float)), errors="coerce").fillna(0).mean()) if not constraint_df.empty else 0.0,
    }
    probe_ready = bool(len(v553_input_index_df))
    temporal_field_ready = bool(
        packet_rows
        and ready_for_v553
        and comparability_context.get("status") != "not_supplied"
        and bool(v553_input_index_df["ready_for_v553_temporal_field"].astype(bool).any() if not v553_input_index_df.empty and "ready_for_v553_temporal_field" in v553_input_index_df.columns else False)
    )

    blocked_lanes_present = bool(
        status_conflict_rows_n
        or (
            not constraint_df.empty
            and "blocked_from_downstream" in constraint_df.columns
            and constraint_df["blocked_from_downstream"].astype(bool).any()
        )
    )
    structural_handoff_status = "ready" if ready_for_v553 and not blocked_lanes_present else "ready_with_gaps"
    if primary_rows.empty or not required_inputs_present:
        structural_handoff_status = "blocked"
    if not required_inputs_present:
        status = "BLOCKED_V552J_MISSING_REQUIRED_INPUTS"
    elif status_conflict_rows_n:
        status = "BLOCKED_CONFLICTING_AUTHORITY"
    elif blocked_lanes_present and ready_for_v553:
        status = "READY_WITH_BLOCKED_LANES"
    elif ready_for_v553 and comparability_context.get("status") != "not_supplied":
        status = "PARTIAL_READY_FOR_V553_PROBE"
    elif ready_for_v553:
        status = "PARTIAL_READY_FOR_V553_PROBE"
    elif probe_ready:
        status = "PARTIAL_READY_FOR_V553_PROBE"
    elif supplied_v552_context:
        status = "READY_WITH_BLOCKED_LANES"
    else:
        status = "READY_WITH_BLOCKED_LANES"
    downstream_context_ready = bool(supplied_v552_context or probe_ready)
    runtime_ready = False

    manifest = {
        "run_id": run_id,
        "status": status,
        "structural_handoff_status": structural_handoff_status,
        "input_status": "ready" if not primary_rows.empty else "blocked",
        "adapter_preflight_ready": required_inputs_present,
        "single_wave_structural_ready": bool(supplied_v552_context),
        "v553_probe_ready": probe_ready,
        "v553_temporal_field_ready": temporal_field_ready,
        "v553_downstream_context_ready": downstream_context_ready,
        "runtime_ready": runtime_ready,
        "v552_context_profile": v552_context_profile,
        "runtime_app_ready": False,
        "constraint_rows": constraint_rows_n,
        "packet_rows": packet_rows,
        "v553_input_row_count": v553_input_row_count,
        "structural_dimensions_resolved_row_count": structural_dimensions_resolved_row_count,
        "structural_dimensions_resolved_any": structural_dimensions_resolved_any,
        "structural_dimensions_resolved_all": structural_dimensions_resolved_all,
        "v553_probe_handoff_row_count": probe_handoff_rows_n,
        "v553_temporal_field_handoff_row_count": temporal_field_handoff_rows_n,
        "v553_blocked_context_handoff_row_count": int(max(0, v553_input_row_count - probe_handoff_rows_n)),
        "v553_handoff_row_count": to_v553_handoff_rows_n,
        "context_rows": int(len(context_df)),
        "absence_rows": absence_rows_n,
        "uncertainty_rows": uncertainty_rows_n,
        "packet_ready_for_v553": bool(packet_rows and ready_for_v553),
        "structural_dimensions_resolved_for_v553": bool(packet_rows and structural_dimensions_resolved_for_v553),
        "ready_for_v553_probe": bool(probe_ready),
        "ready_for_v553_temporal_field": bool(temporal_field_ready),
        **aggregate_score_summary,
        "forensic_rows": forensic_rows_n,
        "forbidden_rows": forbidden_rows,
        "status_conflict_rows": status_conflict_rows_n,
        "forbidden_leakage_rows": forbidden_leakage_rows_n,
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "ready_for_v553": ready_for_v553 and not status_conflict_rows_n,
        "ready_for_runtime_consumption": False,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "missing_required_inputs_json": _json_array(missing_required_inputs),
        "optional_inputs_supplied_json": _json_array(supplied_optional),
        "optional_inputs_missing_json": _json_array(missing_optional),
        "blocker_context_breakdown_json": _json_object(Counter(blocker_contexts_seen)),
        "blocker_count": len(blocker_contexts_seen),
        "blocker_classes_json": _json_array(blocker_contexts_seen),
        "warning_count": int((len(context_df) if not context_df.empty else 0) + (len(leakage_df) if not leakage_df.empty else 0)),
        "warning_classes_json": _json_array((["context_only"] if not context_df.empty else []) + (["downstream_leakage"] if not leakage_df.empty else [])),
        "input_artifact_index_path": repo_relative_path_text(manifest_dir / "v552j_input_artifact_index.json"),
        "authority_normalization_report_path": repo_relative_path_text(manifest_dir / "v552j_authority_normalization_report.json"),
        "v553_input_index_path": repo_relative_path_text(packets_dir / "v552j_v553_input_index.parquet"),
        "v553_handoff_manifest_path": repo_relative_path_text(manifest_dir / "v552j_v553_handoff_manifest.json"),
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
        **command_provenance,
    }

    input_artifact_index_payload = {
        "run_id": run_id,
        "status": "ready" if required_inputs_present else "blocked",
        "artifact_mode": artifact_mode,
        "required_inputs_present": required_inputs_present,
        "comparability_present": comparability_present,
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "required_artifact_count": int(len(required_input_records)),
        "artifact_count": int(len(input_artifact_index_df)),
        "records": input_artifact_index_df.to_dict(orient="records"),
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
        **command_provenance,
    }
    v553_handoff_manifest = {
        "run_id": run_id,
        "status": status,
        "structural_handoff_status": structural_handoff_status,
        "adapter_preflight_ready": required_inputs_present,
        "single_wave_structural_ready": bool(supplied_v552_context),
        "v553_probe_ready": probe_ready,
        "v553_temporal_field_ready": temporal_field_ready,
        "v553_downstream_context_ready": downstream_context_ready,
        "runtime_ready": runtime_ready,
        "v552_context_profile": v552_context_profile,
        "runtime_app_ready": False,
        "packet_rows": packet_rows,
        "v553_input_row_count": v553_input_row_count,
        "structural_dimensions_resolved_row_count": structural_dimensions_resolved_row_count,
        "structural_dimensions_resolved_any": structural_dimensions_resolved_any,
        "structural_dimensions_resolved_all": structural_dimensions_resolved_all,
        "v553_probe_handoff_row_count": probe_handoff_rows_n,
        "v553_temporal_field_handoff_row_count": temporal_field_handoff_rows_n,
        "v553_blocked_context_handoff_row_count": int(max(0, v553_input_row_count - probe_handoff_rows_n)),
        "v553_handoff_row_count": to_v553_handoff_rows_n,
        "constraint_rows": constraint_rows_n,
        "context_rows": int(len(context_df)),
        "absence_rows": absence_rows_n,
        "uncertainty_rows": uncertainty_rows_n,
        "packet_ready_for_v553": bool(packet_rows and ready_for_v553),
        "structural_dimensions_resolved_for_v553": bool(packet_rows and structural_dimensions_resolved_for_v553),
        "ready_for_v553_probe": bool(probe_ready),
        "ready_for_v553_temporal_field": bool(temporal_field_ready),
        **aggregate_score_summary,
        "forensic_rows": forensic_rows_n,
        "forbidden_rows": forbidden_rows,
        "status_conflict_rows": status_conflict_rows_n,
        "forbidden_leakage_rows": forbidden_leakage_rows_n,
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "input_artifact_index_path": repo_relative_path_text(manifest_dir / "v552j_input_artifact_index.json"),
        "authority_normalization_report_path": repo_relative_path_text(manifest_dir / "v552j_authority_normalization_report.json"),
        "v553_input_index_path": repo_relative_path_text(packets_dir / "v552j_v553_input_index.parquet"),
        "blocker_count": len(blocker_contexts_seen),
        "blocker_classes_json": _json_array(blocker_contexts_seen),
        "warning_count": int((len(context_df) if not context_df.empty else 0) + (len(leakage_df) if not leakage_df.empty else 0)),
        "warning_classes_json": _json_array((["context_only"] if not context_df.empty else []) + (["downstream_leakage"] if not leakage_df.empty else [])),
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
        **command_provenance,
    }

    authority_normalization_report = {
        "run_id": run_id,
        "status": status,
        "status_conflict_rows": status_conflict_rows_n,
        "blocker_contexts_json": _json_array(blocker_contexts_seen),
        "comparability_status": comparability_context.get("status", "not_supplied"),
        "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "normalized_lane_counts": json.dumps(
            {
                str(key): int(value)
                for key, value in (constraint_df["normalized_v551j_lane"].astype(str).value_counts().sort_index().items() if not constraint_df.empty and "normalized_v551j_lane" in constraint_df.columns else [])
            },
            sort_keys=True,
            ensure_ascii=False,
        ),
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
        **command_provenance,
    }

    readiness = {
        "run_id": run_id,
        "status": status,
        "structural_handoff_status": structural_handoff_status,
        "adapter_preflight_ready": required_inputs_present,
        "single_wave_structural_ready": bool(supplied_v552_context),
        "v553_probe_ready": probe_ready,
        "v553_temporal_field_ready": temporal_field_ready,
        "v553_downstream_context_ready": downstream_context_ready,
        "runtime_ready": runtime_ready,
        "v552_context_profile": v552_context_profile,
        "runtime_app_ready": False,
        "ready_for_v553": ready_for_v553,
        "ready_for_runtime_consumption": False,
        "runtime_safe_for_app": False,
        "packet_ready_for_v553": bool(packet_rows and ready_for_v553),
        "structural_dimensions_resolved_for_v553": bool(packet_rows and structural_dimensions_resolved_for_v553),
        "ready_for_v553_probe": bool(probe_ready),
        "ready_for_v553_temporal_field": bool(temporal_field_ready),
        **aggregate_score_summary,
        "constraint_rows": constraint_rows_n,
        "blocker_contexts_json": _json_array(blocker_contexts_seen),
        "blocker_context_count": len(blocker_contexts_seen),
        "blocker_classes_json": _json_array(blocker_contexts_seen),
        "warning_count": int((len(context_df) if not context_df.empty else 0) + (len(leakage_df) if not leakage_df.empty else 0)),
        "warning_classes_json": _json_array((["context_only"] if not context_df.empty else []) + (["downstream_leakage"] if not leakage_df.empty else [])),
        "packet_rows": packet_rows,
        "v553_input_row_count": v553_input_row_count,
        "structural_dimensions_resolved_row_count": structural_dimensions_resolved_row_count,
        "structural_dimensions_resolved_any": structural_dimensions_resolved_any,
        "structural_dimensions_resolved_all": structural_dimensions_resolved_all,
        "v553_probe_handoff_row_count": probe_handoff_rows_n,
        "v553_temporal_field_handoff_row_count": temporal_field_handoff_rows_n,
        "v553_blocked_context_handoff_row_count": int(max(0, v553_input_row_count - probe_handoff_rows_n)),
        "v553_handoff_row_count": to_v553_handoff_rows_n,
        "context_rows": int(len(context_df)),
        "absence_rows": absence_rows_n,
        "uncertainty_rows": uncertainty_rows_n,
        "forensic_rows": forensic_rows_n,
        "forbidden_rows": forbidden_rows,
        "status_conflict_rows": status_conflict_rows_n,
        "forbidden_leakage_rows": forbidden_leakage_rows_n,
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "input_status": manifest["input_status"],
        "missing_required_inputs_json": manifest["missing_required_inputs_json"],
        "optional_inputs_supplied_json": manifest["optional_inputs_supplied_json"],
        "optional_inputs_missing_json": manifest["optional_inputs_missing_json"],
        "blocker_context_breakdown_json": manifest["blocker_context_breakdown_json"],
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "input_artifact_index_path": manifest["input_artifact_index_path"],
        "authority_normalization_report_path": manifest["authority_normalization_report_path"],
        "v553_input_index_path": manifest["v553_input_index_path"],
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
    }

    handoff_packet = {
        "run_id": run_id,
        "layer": "v552j",
        "artifact_type": "v552j_structural_handoff_packet",
        "status": status,
        "structural_handoff_status": structural_handoff_status,
        "ready_for_v553": ready_for_v553,
        "ready_for_runtime_consumption": False,
        "runtime_safe_for_app": False,
        "runtime_use_class": "structural_handoff_only",
        "blocker_contexts_json": _json_array(blocker_contexts_seen),
        "blocker_context_count": len(blocker_contexts_seen),
        "blocker_context_summary": "; ".join(blocker_contexts_seen) if blocker_contexts_seen else "none",
        "packet_rows": packet_rows,
        "absence_rows": absence_rows_n,
        "uncertainty_rows": uncertainty_rows_n,
        **aggregate_score_summary,
        "forbidden_rows": forbidden_rows,
        "status_conflict_rows": status_conflict_rows_n,
        "missing_required_inputs_json": manifest["missing_required_inputs_json"],
        "optional_inputs_supplied_json": manifest["optional_inputs_supplied_json"],
        "optional_inputs_missing_json": manifest["optional_inputs_missing_json"],
        "blocker_context_breakdown_json": manifest["blocker_context_breakdown_json"],
        "blocker_count": len(blocker_contexts_seen),
        "blocker_classes_json": _json_array(blocker_contexts_seen),
        "required_downstream_layers_json": _json_array(["v553"] if ready_for_v553 else ["v553", "v554"]),
        "required_downstream_mediation_json": _json_array([] if ready_for_v553 else ["temporalization_required", "seed_contract_required"]),
        "known_absences_json": _json_array([] if not primary_rows.empty else ["v551j_certified_spine"]),
        "forbidden_claim_ids_json": _json_array(V552J_FORBIDDEN_CLAIM_IDS),
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "provenance_summary_json": _json_object(
            {
                "source": _clean(primary_rows.iloc[0].get("source")) if not primary_rows.empty else "unknown",
                "wave": _clean(primary_rows.iloc[0].get("wave")) if not primary_rows.empty else "",
                "canonical_wave": _clean(primary_rows.iloc[0].get("canonical_wave")) if not primary_rows.empty else "",
                "country_code": _clean(primary_rows.iloc[0].get("country_code")) if not primary_rows.empty else "",
                "v551j_artifacts": {
                    "certified": "packets/v551j_certified_packet_index.parquet",
                    "reviewable": "packets/v551j_reviewable_evidence_sidecar.parquet",
                    "certification_readiness": "manifest/v551j_certification_readiness_report.json",
                    "review_readiness": "manifest/v551j_review_readiness_report.json",
                    "input_provenance": "manifest/v551j_input_provenance_manifest.json",
                },
                "upstream_provenance_links": upstream_provenance_links,
                "forbidden_claim_validation_status": forbidden_claim_validation_status,
                "forbidden_claim_validation_counts": forbidden_claim_validation_counts,
                "comparability_status": comparability_context.get("status", "not_supplied"),
                "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
            }
        ),
        "v552_context_status": "supplied" if supplied_v552_context else "not_supplied",
        "v552_context_profile": v552_context_profile,
        "comparability_status": comparability_context.get("status", "not_supplied"),
        "upstream_provenance_links_json": upstream_provenance_links_json,
        "upstream_provenance_link_count": upstream_provenance_links["upstream_link_count"],
        "forbidden_claim_validation_status": forbidden_claim_validation_status,
        "forbidden_claim_validation_counts_json": _json_object(forbidden_claim_validation_counts),
        "input_artifact_index_path": manifest["input_artifact_index_path"],
        "authority_normalization_report_path": manifest["authority_normalization_report_path"],
        "v553_input_index_path": manifest["v553_input_index_path"],
        "v553_handoff_manifest_path": manifest["v553_handoff_manifest_path"],
        "created_at": utc_now(),
        "schema_version": V552J_SCHEMA_VERSION,
        "compiler_version": V552J_COMPILER_VERSION,
        **command_provenance,
    }

    if write_parquet or write_csv:
        write_frame_artifact(
            constraint_df,
            path=packets_dir / "v552j_structural_constraint_packet.parquet",
            schema_path=schemas_dir / "v552j_structural_constraint_packet.schema.json",
            name="v552j_structural_constraint_packet",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            context_df,
            path=packets_dir / "v552j_structural_context_packet.parquet",
            schema_path=schemas_dir / "v552j_structural_context_packet.schema.json",
            name="v552j_structural_context_packet",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            absence_df,
            path=packets_dir / "v552j_structural_absence_packet.parquet",
            schema_path=schemas_dir / "v552j_structural_absence_packet.schema.json",
            name="v552j_structural_absence_packet",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            uncertainty_df,
            path=packets_dir / "v552j_structural_uncertainty_packet.parquet",
            schema_path=schemas_dir / "v552j_structural_uncertainty_packet.schema.json",
            name="v552j_structural_uncertainty_packet",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            audit_df,
            path=audits_dir / "v552j_forbidden_inference_audit.parquet",
            schema_path=schemas_dir / "v552j_forbidden_inference_audit.schema.json",
            name="v552j_forbidden_inference_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            input_artifact_audit_df,
            path=audits_dir / "v552j_input_artifact_audit.parquet",
            schema_path=schemas_dir / "v552j_input_artifact_audit.schema.json",
            name="v552j_input_artifact_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            permission_boundary_df,
            path=audits_dir / "v552j_permission_boundary_audit.parquet",
            schema_path=schemas_dir / "v552j_permission_boundary_audit.schema.json",
            name="v552j_permission_boundary_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            leakage_df,
            path=audits_dir / "v552j_downstream_leakage_audit.parquet",
            schema_path=schemas_dir / "v552j_downstream_leakage_audit.schema.json",
            name="v552j_downstream_leakage_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            status_conflict_df,
            path=audits_dir / "v552j_status_conflict_audit.parquet",
            schema_path=schemas_dir / "v552j_status_conflict_audit.schema.json",
            name="v552j_status_conflict_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            structural_context_only_df,
            path=packets_dir / "v552j_structural_context_only_index.parquet",
            schema_path=schemas_dir / "v552j_structural_context_only_index.schema.json",
            name="v552j_structural_context_only_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            review_only_df,
            path=packets_dir / "v552j_review_only_index.parquet",
            schema_path=schemas_dir / "v552j_review_only_index.schema.json",
            name="v552j_review_only_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            diagnostic_only_df,
            path=packets_dir / "v552j_diagnostic_only_index.parquet",
            schema_path=schemas_dir / "v552j_diagnostic_only_index.schema.json",
            name="v552j_diagnostic_only_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            blocked_index_df,
            path=packets_dir / "v552j_blocked_index.parquet",
            schema_path=schemas_dir / "v552j_blocked_index.schema.json",
            name="v552j_blocked_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            blocker_context_breakdown_df,
            path=audits_dir / "v552j_blocker_context_breakdown.parquet",
            schema_path=schemas_dir / "v552j_blocker_context_breakdown.schema.json",
            name="v552j_blocker_context_breakdown",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            to_v553_handoff_df,
            path=packets_dir / "v552j_to_v553_handoff_index.parquet",
            schema_path=schemas_dir / "v552j_to_v553_handoff_index.schema.json",
            name="v552j_to_v553_handoff_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
        write_frame_artifact(
            v553_input_index_df,
            path=packets_dir / "v552j_v553_input_index.parquet",
            schema_path=schemas_dir / "v552j_v553_input_index.schema.json",
            name="v552j_v553_input_index",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
            extra_schema={"layer": "v552j"},
        )
    write_json_artifact(packets_dir / "v552j_structural_handoff_packet.json", handoff_packet)
    write_schema_json(
        schemas_dir / "v552j_structural_handoff_packet.schema.json",
        pd.DataFrame([handoff_packet]),
        name="v552j_structural_handoff_packet",
        run_id=run_id,
        extra={"layer": "v552j"},
    )
    write_json_artifact(manifest_dir / "v552j_input_artifact_index.json", input_artifact_index_payload)
    write_json_artifact(manifest_dir / "v552j_runtime_handoff_manifest.json", manifest)
    write_json_artifact(manifest_dir / "v552j_v553_handoff_manifest.json", v553_handoff_manifest)
    write_json_artifact(manifest_dir / "v552j_authority_normalization_report.json", authority_normalization_report)
    write_json_artifact(manifest_dir / "v552j_readiness_report.json", readiness)
    write_schema_json(schemas_dir / "v552j_structural_context_packet.schema.json", context_df, name="v552j_structural_context_packet", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_input_artifact_index.schema.json", input_artifact_index_df, name="v552j_input_artifact_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_runtime_handoff_manifest.schema.json", pd.DataFrame([manifest]), name="v552j_runtime_handoff_manifest", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_input_artifact_audit.schema.json", input_artifact_audit_df, name="v552j_input_artifact_audit", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_permission_boundary_audit.schema.json", permission_boundary_df, name="v552j_permission_boundary_audit", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_downstream_leakage_audit.schema.json", leakage_df, name="v552j_downstream_leakage_audit", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_status_conflict_audit.schema.json", status_conflict_df, name="v552j_status_conflict_audit", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_authority_normalization_report.schema.json", pd.DataFrame([authority_normalization_report]), name="v552j_authority_normalization_report", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_readiness_report.schema.json", pd.DataFrame([readiness]), name="v552j_readiness_report", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_structural_context_only_index.schema.json", structural_context_only_df, name="v552j_structural_context_only_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_review_only_index.schema.json", review_only_df, name="v552j_review_only_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_diagnostic_only_index.schema.json", diagnostic_only_df, name="v552j_diagnostic_only_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_blocked_index.schema.json", blocked_index_df, name="v552j_blocked_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_blocker_context_breakdown.schema.json", pd.DataFrame(blocker_context_breakdown_rows), name="v552j_blocker_context_breakdown", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_to_v553_handoff_index.schema.json", to_v553_handoff_df, name="v552j_to_v553_handoff_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_v553_input_index.schema.json", v553_input_index_df, name="v552j_v553_input_index", run_id=run_id, extra={"layer": "v552j"})
    write_schema_json(schemas_dir / "v552j_v553_handoff_manifest.schema.json", pd.DataFrame([v553_handoff_manifest]), name="v552j_v553_handoff_manifest", run_id=run_id, extra={"layer": "v552j"})

    return {
        "run_id": run_id,
        "status": status,
        "constraint_df": constraint_df,
        "absence_df": absence_df,
        "uncertainty_df": uncertainty_df,
        "audit_df": audit_df,
        "handoff_packet": handoff_packet,
        "manifest": manifest,
        "status_conflict_audit_df": status_conflict_df,
        "structural_context_only_index_df": structural_context_only_df,
        "review_only_index_df": review_only_df,
        "diagnostic_only_index_df": diagnostic_only_df,
        "blocked_index_df": blocked_index_df,
        "blocker_context_breakdown_df": pd.DataFrame(blocker_context_breakdown_rows),
        "to_v553_handoff_index_df": to_v553_handoff_df,
        "v553_input_index_df": v553_input_index_df,
        "context_df": context_df,
        "input_artifact_audit_df": input_artifact_audit_df,
        "permission_boundary_df": permission_boundary_df,
        "downstream_leakage_df": leakage_df,
        "authority_normalization_report": authority_normalization_report,
        "v553_handoff_manifest": v553_handoff_manifest,
        "readiness": readiness,
        "output_root": repo_relative_path_text(root),
        "handoff_packet_path": repo_relative_path_text(packets_dir / "v552j_structural_handoff_packet.json"),
        "handoff_schema_path": repo_relative_path_text(schemas_dir / "v552j_structural_handoff_packet.schema.json"),
        "packet_path": repo_relative_path_text(packets_dir / "v552j_structural_constraint_packet.parquet"),
        "context_path": repo_relative_path_text(packets_dir / "v552j_structural_context_packet.parquet"),
        "absence_path": repo_relative_path_text(packets_dir / "v552j_structural_absence_packet.parquet"),
        "uncertainty_path": repo_relative_path_text(packets_dir / "v552j_structural_uncertainty_packet.parquet"),
        "audit_path": repo_relative_path_text(audits_dir / "v552j_forbidden_inference_audit.parquet"),
        "input_artifact_audit_path": repo_relative_path_text(audits_dir / "v552j_input_artifact_audit.parquet"),
        "permission_boundary_audit_path": repo_relative_path_text(audits_dir / "v552j_permission_boundary_audit.parquet"),
        "downstream_leakage_audit_path": repo_relative_path_text(audits_dir / "v552j_downstream_leakage_audit.parquet"),
        "status_conflict_audit_path": repo_relative_path_text(audits_dir / "v552j_status_conflict_audit.parquet"),
        "structural_context_only_index_path": repo_relative_path_text(packets_dir / "v552j_structural_context_only_index.parquet"),
        "review_only_index_path": repo_relative_path_text(packets_dir / "v552j_review_only_index.parquet"),
        "diagnostic_only_index_path": repo_relative_path_text(packets_dir / "v552j_diagnostic_only_index.parquet"),
        "blocked_index_path": repo_relative_path_text(packets_dir / "v552j_blocked_index.parquet"),
        "blocker_context_breakdown_path": repo_relative_path_text(audits_dir / "v552j_blocker_context_breakdown.parquet"),
        "to_v553_handoff_index_path": repo_relative_path_text(packets_dir / "v552j_to_v553_handoff_index.parquet"),
        "v553_input_index_path": repo_relative_path_text(packets_dir / "v552j_v553_input_index.parquet"),
        "manifest_path": repo_relative_path_text(manifest_dir / "v552j_runtime_handoff_manifest.json"),
        "input_artifact_index_path": repo_relative_path_text(manifest_dir / "v552j_input_artifact_index.json"),
        "authority_normalization_report_path": repo_relative_path_text(manifest_dir / "v552j_authority_normalization_report.json"),
        "readiness_path": repo_relative_path_text(manifest_dir / "v552j_readiness_report.json"),
        "v553_handoff_manifest_path": repo_relative_path_text(manifest_dir / "v552j_v553_handoff_manifest.json"),
        "schema_paths": {
            "constraint": repo_relative_path_text(schemas_dir / "v552j_structural_constraint_packet.schema.json"),
            "context": repo_relative_path_text(schemas_dir / "v552j_structural_context_packet.schema.json"),
            "absence": repo_relative_path_text(schemas_dir / "v552j_structural_absence_packet.schema.json"),
            "uncertainty": repo_relative_path_text(schemas_dir / "v552j_structural_uncertainty_packet.schema.json"),
            "audit": repo_relative_path_text(schemas_dir / "v552j_forbidden_inference_audit.schema.json"),
            "input_artifact_audit": repo_relative_path_text(schemas_dir / "v552j_input_artifact_audit.schema.json"),
            "permission_boundary_audit": repo_relative_path_text(schemas_dir / "v552j_permission_boundary_audit.schema.json"),
            "downstream_leakage_audit": repo_relative_path_text(schemas_dir / "v552j_downstream_leakage_audit.schema.json"),
            "status_conflict_audit": repo_relative_path_text(schemas_dir / "v552j_status_conflict_audit.schema.json"),
            "structural_context_only_index": repo_relative_path_text(schemas_dir / "v552j_structural_context_only_index.schema.json"),
            "review_only_index": repo_relative_path_text(schemas_dir / "v552j_review_only_index.schema.json"),
            "diagnostic_only_index": repo_relative_path_text(schemas_dir / "v552j_diagnostic_only_index.schema.json"),
            "blocked_index": repo_relative_path_text(schemas_dir / "v552j_blocked_index.schema.json"),
            "blocker_context_breakdown": repo_relative_path_text(schemas_dir / "v552j_blocker_context_breakdown.schema.json"),
            "to_v553_handoff_index": repo_relative_path_text(schemas_dir / "v552j_to_v553_handoff_index.schema.json"),
            "v553_input_index": repo_relative_path_text(schemas_dir / "v552j_v553_input_index.schema.json"),
            "manifest": repo_relative_path_text(schemas_dir / "v552j_runtime_handoff_manifest.schema.json"),
            "input_artifact_index": repo_relative_path_text(schemas_dir / "v552j_input_artifact_index.schema.json"),
            "authority_normalization_report": repo_relative_path_text(schemas_dir / "v552j_authority_normalization_report.schema.json"),
            "readiness": repo_relative_path_text(schemas_dir / "v552j_readiness_report.schema.json"),
            "v553_handoff_manifest": repo_relative_path_text(schemas_dir / "v552j_v553_handoff_manifest.schema.json"),
        },
    }


def validate_v552j_structural_handoff(summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if summary.get("ready_for_runtime_consumption"):
        errors.append("V552J may not be marked runtime consumable for app runtime")
    if summary.get("manifest", {}).get("runtime_packets_written"):
        errors.append("runtime_packets_written must remain false")
    profile = summary.get("manifest", {}).get("v552_context_profile")
    if profile not in {"none", "partial", "core_supplied", "full_supplied"}:
        errors.append("invalid v552_context_profile")
    for key in ("constraint_df", "absence_df", "uncertainty_df", "audit_df", "status_conflict_audit_df"):
        if key not in summary:
            errors.append(f"missing {key}")
    if summary.get("status") not in V552J_HANDOFF_STATUSES:
        errors.append("unexpected V552J status")
    return errors


__all__ = ["build_v552j_structural_handoff", "validate_v552j_structural_handoff"]
