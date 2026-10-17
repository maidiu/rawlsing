#!/usr/bin/env python3
"""V551J review-surface helpers for phase B."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_AUTHORITY_STATUSES,
    V551J_DIRECTIONALITY_STATUSES,
    V551J_PACKET_TYPES,
    V551J_REVIEW_PRIORITIES,
    V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA,
    V551J_REVIEW_READINESS_REPORT_SCHEMA,
    V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA,
    V551J_REVIEW_SURFACE_SCHEMA,
    V551J_REVIEW_SURFACE_STATUSES,
    V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA,
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


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = _clean(value).lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _json_array(values: list[Any] | tuple[Any, ...] | set[Any] | None) -> str:
    if not values:
        return "[]"
    cleaned: list[str] = []
    for value in values:
        token = _clean(value)
        if token and token not in cleaned:
            cleaned.append(token)
    return json.dumps(cleaned, ensure_ascii=False)


def _json_object(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, ensure_ascii=False, default=str)


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


def _parse_json_object(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    text = _clean(value)
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _first_nonempty(*values: Any) -> str:
    for value in values:
        token = _clean(value)
        if token:
            return token
    return ""


def _join_token_variants(value: Any) -> set[str]:
    token = _clean(value)
    if not token:
        return set()
    variants = {
        token,
        token.replace(":", "_"),
        token.replace("_", ":"),
        token.replace(" ", "_"),
        token.replace(" ", ":"),
    }
    return {variant for variant in variants if variant}


def _series_first(frame: pd.DataFrame, column: str, default: Any = "") -> Any:
    if frame.empty or column not in frame.columns:
        return default
    value = frame.iloc[0].get(column, default)
    return default if pd.isna(value) else value


def _join_series(frame: pd.DataFrame, keys: list[tuple[str, Any]]) -> pd.Series | None:
    if frame.empty:
        return None
    subset = frame.copy()
    matched = False
    for column, value in keys:
        if column not in subset.columns:
            continue
        tokens = _join_token_variants(value)
        if not tokens:
            continue
        subset = subset[subset[column].astype(str).str.strip().isin(tokens)]
        matched = True
        if subset.empty:
            return None
    if not matched or subset.empty:
        return None
    return subset.iloc[0]


def _join_audit_row(
    *,
    run_id: str,
    table_name: str,
    path: str,
    frame: pd.DataFrame,
    required_columns: list[str],
    join_strategy: str,
    join_warning: str = "",
) -> dict[str, Any]:
    present = [column for column in required_columns if column in frame.columns]
    missing = [column for column in required_columns if column not in frame.columns]
    return {
        "run_id": run_id,
        "table_name": table_name,
        "path": path,
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "columns_json": _json_array(list(frame.columns)),
        "required_columns_present_json": _json_array(present),
        "required_columns_missing_json": _json_array(missing),
        "candidate_join_keys_json": _json_array(required_columns[:5]),
        "join_strategy": join_strategy,
        "join_status": "not_supplied" if not path and frame.empty else ("ok" if not missing else "degraded"),
        "join_warning": join_warning,
        "created_at": utc_now(),
        "schema_version": "v0.1",
    }


def build_v551j_v552_context_join_audit(
    *,
    run_id: str,
    inputs: dict[str, tuple[str, pd.DataFrame, list[str]]],
) -> pd.DataFrame:
    rows = []
    for table_name, (path, frame, required_columns) in inputs.items():
        rows.append(
            _join_audit_row(
                run_id=run_id,
                table_name=table_name,
                path=path,
                frame=frame,
                required_columns=required_columns,
                join_strategy="source_wave_country" if "source" in required_columns else "context_key",
                join_warning="",
            )
        )
    return pd.DataFrame(rows, columns=V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA["required_columns"])


def _review_blockers(row: pd.Series) -> list[str]:
    blockers: list[str] = []
    if not _clean(row.get("packet_id")):
        blockers.append("missing_packet_id")
    if not _clean(row.get("source")):
        blockers.append("missing_source")
    if not _clean(row.get("wave")):
        blockers.append("missing_wave")
    if not _clean(row.get("country_code")):
        blockers.append("missing_country_code")
    if not _clean(row.get("source_artifact_ids_json")):
        blockers.append("missing_source_artifact_ids")
    if not _parse_json_array(row.get("forbidden_claim_ids_json")):
        blockers.append("missing_forbidden_claim_ids")
    if _clean(row.get("runtime_use_class")) in {"runtime_safe_after_v552j", "runtime_safe_after_v553"}:
        blockers.append("runtime_safe_packet")
    leakage_fields = [
        column
        for column in [
            "identity_with",
            "alienation_from",
            "lens_capture",
            "object_visibility",
            "carrier_language",
            "implicit_legitimated_strata",
            "actor_absorption",
            "parent_orientation",
            "coparent_orientation",
            "expectation_baseline",
            "striving_affordance",
            "pressureflow_route",
            "enneagram_type",
            "enneagram_attractor",
        ]
        if _clean(row.get(column))
    ]
    blockers.extend(f"downstream_leakage:{field}" for field in leakage_fields)
    authority_status = _clean(row.get("authority_status"))
    if authority_status == "fallback" and not _to_bool(row.get("review_required"), False):
        blockers.append("fallback_authority_without_review_flag")
    if authority_status == "unknown" and not _to_bool(row.get("review_required"), False):
        blockers.append("unknown_authority_without_review_flag")
    if _clean(row.get("packet_type")) not in V551J_PACKET_TYPES:
        blockers.append("invalid_packet_type")
    return blockers


def _review_reason_codes(row: pd.Series, v552_joined: bool) -> list[str]:
    reasons: list[str] = []
    if _clean(row.get("packet_type")) == "known_absence_packet":
        reasons.append("diagnostic_only_upstream_source")
    if not v552_joined:
        reasons.append("v552_context_gap")
    if _clean(row.get("directionality_status")) in {"unknown", "not_applicable", "undirected_association"}:
        reasons.append("directionality_gap")
    if _clean(row.get("authority_status")) in {"fallback", "unknown"}:
        reasons.append("authority_gap")
    if _clean(row.get("support_status")) in {"insufficient", "failed", "unknown", "missing_support"}:
        reasons.append("weak_support")
    if _clean(row.get("packet_status")) == "diagnostic":
        reasons.append("diagnostic_upstream_source")
    if _clean(row.get("association_context_status")) == "association_context_only":
        reasons.append("association_context_only")
    if not reasons:
        reasons.append("reviewable")
    return list(dict.fromkeys(reasons))


def _review_priority(row: pd.Series, reason_codes: list[str], v552_joined: bool) -> str:
    support = _clean(row.get("support_status"))
    confidence = _clean(row.get("confidence_tier"))
    authority = _clean(row.get("authority_status"))
    if "diagnostic_only_upstream_source" in reason_codes or "diagnostic_upstream_source" in reason_codes:
        return "diagnostic"
    if "v552_context_gap" in reason_codes and "authority_gap" in reason_codes:
        return "low"
    if not v552_joined:
        return "low"
    if authority in {"exact_registry", "regex_registry", "prefix_registry"} and confidence in {"high", "medium"} and support not in {"insufficient", "failed", "unknown", "missing_support"}:
        return "high" if v552_joined else "medium"
    if authority == "manual_review":
        return "medium"
    if "directionality_gap" in reason_codes or "authority_gap" in reason_codes:
        return "low"
    return "medium"



def _numeric(value: Any, default: float = 0.0) -> float:
    token = _clean(value)
    if token == "":
        return default
    try:
        score = float(token)
    except Exception:
        return default
    if pd.isna(score):
        return default
    return max(0.0, min(1.0, score))


def _confidence_score(value: Any) -> float:
    return {
        "high": 1.0,
        "medium": 0.66,
        "low": 0.33,
        "unknown": 0.0,
        "": 0.0,
    }.get(_clean(value).lower(), 0.0)


def _authority_score(value: Any) -> float:
    return {
        "exact_registry": 1.0,
        "regex_registry": 0.9,
        "prefix_registry": 0.85,
        "manual_review": 0.8,
        "semantic_role": 0.55,
        "computed_context": 0.5,
        "fallback": 0.2,
        "unknown": 0.0,
        "not_applicable": 0.0,
        "": 0.0,
    }.get(_clean(value), 0.0)


def _directionality_score(value: Any, packet_type: Any = "") -> float:
    status = _clean(value)
    if status == "known_directional":
        return 1.0
    if status == "partial_directionality":
        return 0.65
    if status in {"undirected_association", "not_applicable"}:
        return 0.4 if _clean(packet_type) != "joint_relation_evidence_packet" else 0.15
    if status == "conflicting_directionality":
        return 0.2
    return 0.0


def _join_strength_score(value: Any) -> float:
    return {"strong": 1.0, "weak": 0.35, "not_supplied": 0.0, "": 0.0}.get(_clean(value), 0.0)


def _semantic_specificity_score(row: pd.Series) -> float:
    tokens: list[str] = []
    for column in [
        "relation_axis_ids_json",
        "target_entity_ids_json",
        "driver_facet_ids_json",
        "semantic_roles_json",
        "semantic_tags_json",
        "strata_relevance_json",
        "future_target_affordances_json",
    ]:
        tokens.extend(_parse_json_array(row.get(column)))
    if not tokens:
        return 0.0
    return max(0.1, min(1.0, len(set(tokens)) / 8.0))


def _support_score(row: pd.Series) -> float:
    explicit = _numeric(row.get("support_score"), default=-1.0)
    if explicit >= 0:
        return explicit
    support_n = _numeric(row.get("support_n_unweighted"), default=0.0)
    if support_n <= 0:
        return 0.0
    if support_n >= 30:
        return 1.0
    return support_n / 30.0


def _review_priority_score(value: Any) -> float:
    return {"high": 1.0, "medium": 0.66, "low": 0.33, "diagnostic": 0.0}.get(_clean(value), 0.0)


def _reliability_vector(row: pd.Series, *, review_priority: str, v552_join_strength: str) -> dict[str, Any]:
    support = _support_score(row)
    confidence = _confidence_score(row.get("confidence_tier"))
    authority = _authority_score(row.get("authority_status"))
    directionality = _directionality_score(row.get("directionality_status"), row.get("packet_type"))
    join_strength = _join_strength_score(v552_join_strength)
    semantic_specificity = _semantic_specificity_score(row)
    completeness_parts = [support, confidence, authority, directionality, semantic_specificity]
    if join_strength > 0:
        completeness_parts.append(join_strength)
    evidence_completeness = round(sum(completeness_parts) / len(completeness_parts), 6)
    certifiability_parts = [support, confidence, authority, directionality]
    certifiability = round(sum(certifiability_parts) / len(certifiability_parts), 6)
    priority = _review_priority_score(review_priority)
    status = "certifiable" if certifiability >= 0.7 and support > 0 and authority >= 0.8 else "reviewable_evidence"
    if _clean(row.get("packet_type")) == "known_absence_packet" or _clean(row.get("packet_status")) == "diagnostic":
        status = "diagnostic_only"
    if support <= 0 and _clean(row.get("support_status")) in {"insufficient", "failed", "unknown", "missing_support"}:
        status = "blocked_unsupported"
    use_permission = "structural_context_only" if status == "certifiable" else "review_only"
    if status == "diagnostic_only":
        use_permission = "diagnostic_only"
    if status == "blocked_unsupported":
        use_permission = "blocked"
    provenance = {
        "support_score_numeric": "support_score if present else support_n_unweighted/30 capped at 1",
        "confidence_score_numeric": "confidence_tier mapping high=1 medium=0.66 low=0.33 unknown=0",
        "authority_score_numeric": "authority_status conservative ordinal mapping",
        "directionality_score_numeric": "directionality_status conservative ordinal mapping",
        "join_strength_score_numeric": "V552 join strength; zero when context not supplied",
        "semantic_specificity_score_numeric": "count of distinct semantic affordance/id tokens capped at 8",
        "certifiability_score_numeric": "mean of support/confidence/authority/directionality scores",
    }
    return {
        "support_score_numeric": round(support, 6),
        "confidence_score_numeric": round(confidence, 6),
        "authority_score_numeric": round(authority, 6),
        "directionality_score_numeric": round(directionality, 6),
        "join_strength_score_numeric": round(join_strength, 6),
        "semantic_specificity_score_numeric": round(semantic_specificity, 6),
        "evidence_completeness_score_numeric": evidence_completeness,
        "certifiability_score_numeric": certifiability,
        "review_priority_score_numeric": round(priority, 6),
        "score_provenance_json": _json_object(provenance),
        "evidence_quality_status": status,
        "use_permission_class": use_permission,
    }


def _evidence_backed_for_sidecar(row: pd.Series) -> bool:
    if _clean(row.get("certification_status")) == "certified" or _clean(row.get("packet_status")) == "certified":
        return False
    if _clean(row.get("review_surface_status")) in {"blocked", "diagnostic_only"}:
        return False
    if _clean(row.get("evidence_quality_status")) in {"blocked_unsupported", "diagnostic_only"}:
        return False
    support_status = _clean(row.get("support_status"))
    support_n = _numeric(row.get("support_n_unweighted"), default=0.0)
    support_score = _numeric(row.get("support_score_numeric"), default=0.0)
    if support_n <= 0 and support_score <= 0 and support_status in {"insufficient", "failed", "unknown", "missing_support"}:
        return False
    if _clean(row.get("runtime_use_class")) in {"runtime_safe_after_v552j", "runtime_safe_after_v553"}:
        return False
    return bool(_clean(row.get("packet_id")) and _parse_json_array(row.get("forbidden_claim_ids_json")))


def _sidecar_reasons(row: pd.Series) -> list[str]:
    reasons = ["preserve_non_certified_evidence"]
    if _clean(row.get("confidence_tier")) in {"low", "unknown"}:
        reasons.append("confidence_gap")
    if _clean(row.get("authority_status")) in {"semantic_role", "computed_context", "fallback", "unknown"}:
        reasons.append("authority_gap")
    if _clean(row.get("directionality_status")) in {"partial_directionality", "undirected_association", "not_applicable", "unknown"}:
        reasons.append("directionality_limited")
    if _clean(row.get("v552_context_status")) != "joined":
        reasons.append("v552_context_gap")
    blockers = _parse_json_array(row.get("certification_blockers_json"))
    reasons.extend(f"certification_blocker:{blocker}" for blocker in blockers)
    return list(dict.fromkeys(reasons))


def build_v551j_reviewable_evidence_sidecar(
    review_surface: pd.DataFrame,
    *,
    run_id: str = "",
) -> pd.DataFrame:
    """Preserve weak-but-real V551J evidence separately from certified packets.

    The sidecar is deliberately not a runtime surface. It keeps nonzero-support
    or otherwise evidence-backed packets that fail certification because of
    confidence, authority, directionality, or V552-context gaps. Zero-support
    raw joint pattern context remains blocked/diagnostic and is not preserved
    here.
    """
    if review_surface.empty:
        return pd.DataFrame(columns=V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA["required_columns"])

    rows: list[dict[str, Any]] = []
    for row in review_surface.itertuples(index=False):
        series = pd.Series(row._asdict())
        if not _evidence_backed_for_sidecar(series):
            continue
        sidecar_row = {column: series.get(column, "") for column in V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA["required_columns"]}
        normalized_lane = _clean(series.get("normalized_v551j_lane")) or _clean(series.get("association_lane")) or "reviewable_context"
        sidecar_row.update(
            {
                "run_id": run_id or _clean(series.get("run_id")),
                "sidecar_reason_codes_json": _json_array(_sidecar_reasons(series)),
                "use_permission_class": "review_only" if _clean(series.get("use_permission_class")) != "blocked" else "blocked",
                "sidecar_lane": normalized_lane,
                "sidecar_role": "reviewable_evidence_shadow" if normalized_lane != "blocked" else "blocked_evidence_shadow",
                "created_at": utc_now(),
                "schema_version": "v0.2",
            }
        )
        rows.append(sidecar_row)
    sidecar = pd.DataFrame(rows, columns=V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA["required_columns"])
    if not sidecar.empty:
        sidecar = sidecar.fillna("").reset_index(drop=True)
    return sidecar


def _v552_join_strength(row: pd.Series, v552_row: pd.Series | None) -> str:
    if v552_row is None or v552_row.empty:
        return "not_supplied"
    return "strong"


def _v552_refs(row: pd.Series, v552_row: pd.Series | None, field_name: str) -> str:
    if v552_row is None or v552_row.empty:
        return "[]"
    value = v552_row.get(field_name, [])
    refs = _parse_json_array(value)
    if refs:
        return _json_array(refs)
    token = _first_nonempty(v552_row.get("question_id"), v552_row.get("relation_axis_id"), v552_row.get("target_entity_id"), v552_row.get("driver_facet_id"))
    return _json_array([token] if token else [])


def _required_for_certification(row: pd.Series, reason_codes: list[str]) -> str:
    required: list[str] = []
    if "directionality_gap" in reason_codes:
        required.append("directionality")
    if "authority_gap" in reason_codes:
        required.append("strict_authority")
    if _clean(row.get("support_status")) in {"insufficient", "failed", "unknown", "missing_support"}:
        required.append("support")
    if not _parse_json_array(row.get("forbidden_claim_ids_json")):
        required.append("forbidden_claims")
    if _clean(row.get("packet_id")) == "":
        required.append("packet_identity")
    return _json_array(required)


def _normalized_authority_status(row: pd.Series) -> str:
    authority = _clean(row.get("authority_status"))
    return authority if authority in V551J_AUTHORITY_STATUSES else "unknown"


def _normalized_directionality_status(row: pd.Series) -> str:
    directionality = _clean(row.get("directionality_status"))
    return directionality if directionality in V551J_DIRECTIONALITY_STATUSES else "unknown"


def _normalized_support_status(row: pd.Series) -> str:
    support = _clean(row.get("support_status"))
    if support in {"sufficient_support", "supported"}:
        return "sufficient_support"
    if support in {"insufficient", "failed", "missing_support"}:
        return "insufficient_support"
    if support in {"unknown", ""}:
        return "unknown"
    return support


def _normalized_v552_context_status(row: pd.Series) -> str:
    context = _clean(row.get("v552_context_status"))
    return context if context in {"joined", "not_supplied", "blocked"} else ("not_supplied" if not context else context)


def _normalized_comparability_status(row: pd.Series) -> str:
    comparability = _clean(row.get("comparability_status"))
    return comparability if comparability else "not_supplied"


def _normalized_v551j_review_status(review_surface_status: str) -> str:
    status = _clean(review_surface_status)
    if status in {"reviewable", "reviewable_with_context_gap", "reviewable_with_directionality_gap", "reviewable_with_authority_gap"}:
        return status
    if status in {"diagnostic_only", "blocked"}:
        return status
    return "unknown"


def _normalized_v551j_certification_status(row: pd.Series, review_surface_status: str, evidence_certification_blockers: list[str]) -> str:
    packet_status = _clean(row.get("packet_status"))
    if packet_status == "certified" or _clean(row.get("certification_status")) == "certified":
        return "certified"
    if review_surface_status == "blocked" or "review_surface_blocked" in evidence_certification_blockers:
        return "blocked"
    if review_surface_status == "diagnostic_only" or packet_status == "diagnostic":
        return "diagnostic"
    if review_surface_status.startswith("reviewable"):
        return "reviewable"
    if _clean(row.get("v551j_evidence_certification_status")) in {"candidate", "reviewable"}:
        return "reviewable"
    return "unknown"


def _normalized_v551j_lane(normalized_certification_status: str) -> str:
    if normalized_certification_status == "certified":
        return "certified_spine"
    if normalized_certification_status == "reviewable":
        return "reviewable_context"
    if normalized_certification_status == "diagnostic":
        return "diagnostic_forensic"
    if normalized_certification_status == "blocked":
        return "blocked"
    if normalized_certification_status == "conflict":
        return "conflict"
    return "blocked"


def _normalization_bundle(
    row: pd.Series,
    *,
    review_surface_status: str,
    evidence_certification_blockers: list[str],
    v552_joined: bool,
) -> dict[str, Any]:
    normalized_certification_status = _normalized_v551j_certification_status(row, review_surface_status, evidence_certification_blockers)
    normalized_review_status = _normalized_v551j_review_status(review_surface_status)
    normalized_lane = _normalized_v551j_lane(normalized_certification_status)
    normalized_authority = _normalized_authority_status(row)
    normalized_directionality = _normalized_directionality_status(row)
    normalized_support = _normalized_support_status(row)
    normalized_v552_context = _normalized_v552_context_status(row)
    normalized_comparability = _normalized_comparability_status(row)
    permission_class = (
        "v553_constraint_candidate"
        if normalized_lane == "certified_spine"
        else "v553_context_only"
        if normalized_lane == "reviewable_context"
        else "forensic_only"
        if normalized_lane == "diagnostic_forensic"
        else "blocked"
    )
    if normalized_lane == "certified_spine" and not v552_joined:
        permission_class = "v553_context_only"
    constraint_eligibility = normalized_lane == "certified_spine"
    context_eligibility = normalized_lane in {"certified_spine", "reviewable_context"}
    forensic_eligibility = normalized_lane in {"diagnostic_forensic", "blocked", "conflict"}
    blocked_from_downstream = normalized_lane in {"blocked", "conflict"}
    status_conflict_flag = False
    status_conflict_reason = ""
    if review_surface_status == "blocked" and normalized_certification_status in {"certified", "reviewable"}:
        status_conflict_flag = True
        status_conflict_reason = "blocked_review_status_incompatible_with_positive_certification"
    elif review_surface_status == "diagnostic_only" and normalized_certification_status == "certified":
        status_conflict_flag = True
        status_conflict_reason = "diagnostic_review_status_incompatible_with_certified_spine"
    return {
        "normalized_v551j_lane": normalized_lane,
        "normalized_v551j_certification_status": normalized_certification_status,
        "normalized_v551j_review_status": normalized_review_status,
        "normalized_authority_status": normalized_authority,
        "normalized_directionality_status": normalized_directionality,
        "normalized_support_status": normalized_support,
        "normalized_v552_context_status": normalized_v552_context,
        "normalized_comparability_status": normalized_comparability,
        "permission_class": permission_class,
        "constraint_eligibility": constraint_eligibility,
        "context_eligibility": context_eligibility,
        "forensic_eligibility": forensic_eligibility,
        "blocked_from_downstream": blocked_from_downstream,
        "status_conflict_flag": status_conflict_flag,
        "status_conflict_reason": status_conflict_reason,
    }


def build_v551j_review_surface(
    candidate_trace: pd.DataFrame,
    *,
    run_id: str = "",
    v552_input_paths: dict[str, str] | None = None,
    v552_question_semantic_hierarchy: pd.DataFrame | None = None,
    v552_structural_channel_index: pd.DataFrame | None = None,
    v552_relation_axis_pressure: pd.DataFrame | None = None,
    v552_target_entity_pressure: pd.DataFrame | None = None,
    v552_driver_facet_pressure: pd.DataFrame | None = None,
    v552_contradiction_surface: pd.DataFrame | None = None,
    v552_horizon_constraint_index: pd.DataFrame | None = None,
    v552_parent_prior_manifest: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if candidate_trace.empty:
        empty_review = pd.DataFrame(columns=V551J_REVIEW_SURFACE_SCHEMA["required_columns"])
        empty_exclusion = pd.DataFrame(columns=V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA["required_columns"])
        empty_join = pd.DataFrame(columns=V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA["required_columns"])
        return empty_review, empty_exclusion, empty_join

    v552_input_paths = v552_input_paths or {}
    v552_inputs = {
        "v552_question_semantic_hierarchy": (v552_input_paths.get("v552_question_semantic_hierarchy", ""), v552_question_semantic_hierarchy if v552_question_semantic_hierarchy is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code"]),
        "v552_structural_channel_index": (v552_input_paths.get("v552_structural_channel_index", ""), v552_structural_channel_index if v552_structural_channel_index is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code"]),
        "v552_relation_axis_pressure": (v552_input_paths.get("v552_relation_axis_pressure", ""), v552_relation_axis_pressure if v552_relation_axis_pressure is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "relation_axis_id"]),
        "v552_target_entity_pressure": (v552_input_paths.get("v552_target_entity_pressure", ""), v552_target_entity_pressure if v552_target_entity_pressure is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "target_entity_id"]),
        "v552_driver_facet_pressure": (v552_input_paths.get("v552_driver_facet_pressure", ""), v552_driver_facet_pressure if v552_driver_facet_pressure is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "driver_facet_id"]),
        "v552_contradiction_surface": (v552_input_paths.get("v552_contradiction_surface", ""), v552_contradiction_surface if v552_contradiction_surface is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code"]),
        "v552_horizon_constraint_index": (v552_input_paths.get("v552_horizon_constraint_index", ""), v552_horizon_constraint_index if v552_horizon_constraint_index is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code"]),
        "v552_parent_prior_manifest": (v552_input_paths.get("v552_parent_prior_manifest", ""), v552_parent_prior_manifest if v552_parent_prior_manifest is not None else pd.DataFrame(), ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code"]),
    }
    join_audit = build_v551j_v552_context_join_audit(run_id=run_id, inputs=v552_inputs)
    join_map = {name: frame for name, (_, frame, _) in v552_inputs.items()}
    rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []

    for row in candidate_trace.itertuples(index=False):
        series = pd.Series(row._asdict())
        blockers = _review_blockers(series)
        v552_row = None
        for frame in join_map.values():
            if frame is None or frame.empty:
                continue
            keys = [
                ("source", series.get("source")),
                ("wave", series.get("wave")),
                ("canonical_wave", series.get("canonical_wave")),
                ("country_code", series.get("country_code")),
                ("question_id", series.get("question_id")),
                ("var_code", series.get("var_code")),
            ]
            if "relation_axis_id" in frame.columns:
                keys.append(("relation_axis_id", _first_nonempty(*_parse_json_array(series.get("relation_axis_ids_json")))))
            if "target_entity_id" in frame.columns:
                keys.append(("target_entity_id", _first_nonempty(*_parse_json_array(series.get("target_entity_ids_json")))))
            if "driver_facet_id" in frame.columns:
                keys.append(("driver_facet_id", _first_nonempty(*_parse_json_array(series.get("driver_facet_ids_json")))))
            v552_row = _join_series(frame, keys)
            if v552_row is not None:
                break
        v552_joined = v552_row is not None
        reason_codes = _review_reason_codes(series, v552_joined)
        if blockers:
            for blocker in blockers:
                exclusion_rows.append(
                    {
                        "run_id": run_id,
                        "candidate_source": "candidate_trace",
                        "source": _clean(series.get("source")),
                        "wave": _clean(series.get("wave")),
                        "canonical_wave": _clean(series.get("canonical_wave")),
                        "country_code": _clean(series.get("country_code")),
                        "packet_id": _clean(series.get("packet_id")),
                        "packet_type": _clean(series.get("packet_type")),
                        "review_surface_status": "blocked",
                        "review_priority": "diagnostic" if blocker.startswith("downstream_leakage") else "low",
                        "review_reason_code": reason_codes[0] if reason_codes else "blocked",
                        "review_blocker_code": blocker,
                        "required_downstream_layer": "v551j",
                        "created_at": utc_now(),
                        "schema_version": "v0.1",
                    }
                )
            continue

        review_surface_status = "reviewable"
        if "v552_context_gap" in reason_codes:
            review_surface_status = "reviewable_with_context_gap"
        if "directionality_gap" in reason_codes:
            review_surface_status = "reviewable_with_directionality_gap"
        if "authority_gap" in reason_codes:
            review_surface_status = "reviewable_with_authority_gap"
        if "diagnostic_only_upstream_source" in reason_codes or "diagnostic_upstream_source" in reason_codes:
            review_surface_status = "diagnostic_only"

        if review_surface_status not in V551J_REVIEW_SURFACE_STATUSES:
            review_surface_status = "blocked"

        review_priority = _review_priority(series, reason_codes, v552_joined)
        if review_priority not in V551J_REVIEW_PRIORITIES:
            review_priority = "diagnostic"

        evidence_certification_blockers = []
        if review_surface_status == "blocked":
            evidence_certification_blockers.append("review_surface_blocked")
        if _clean(series.get("authority_status")) not in {"exact_registry", "regex_registry", "prefix_registry", "manual_review"}:
            evidence_certification_blockers.append("authority_not_certifiable")
        if _clean(series.get("directionality_status")) in {"unknown", "undirected_association"}:
            evidence_certification_blockers.append("directionality_not_certifiable")
        if _clean(series.get("support_status")) in {"insufficient", "failed", "unknown", "missing_support"}:
            evidence_certification_blockers.append("support_not_certifiable")
        if not _parse_json_array(series.get("forbidden_claim_ids_json")):
            evidence_certification_blockers.append("forbidden_claims_missing")
        certification_candidate = False
        v552_handoff_readiness = "ready" if v552_joined else "not_ready_v552_context_missing"
        v552_handoff_blockers = [] if v552_joined else ["v552_context_missing"]
        v552_join_strength = _v552_join_strength(series, v552_row)
        reliability = _reliability_vector(series, review_priority=review_priority, v552_join_strength=v552_join_strength)
        normalization = _normalization_bundle(
            series,
            review_surface_status=review_surface_status,
            evidence_certification_blockers=evidence_certification_blockers,
            v552_joined=v552_joined,
        )

        rows.append(
            {
                **series.to_dict(),
                "review_surface_status": review_surface_status,
                "review_priority": review_priority,
                "review_reason_codes_json": _json_array(reason_codes),
                "review_blockers_json": _json_array(blockers),
                "review_notes_json": _json_array(
                    [
                        f"v552_joined={str(v552_joined).lower()}",
                        f"authority={_clean(series.get('authority_status'))}",
                        f"directionality={_clean(series.get('directionality_status'))}",
                    ]
                ),
                "v552_context_status": "joined" if v552_joined else "not_supplied",
                "v552_join_strength": v552_join_strength,
                "v552_structural_channel_refs_json": _v552_refs(series, v552_row, "v552_structural_channel_refs_json"),
                "v552_relation_axis_pressure_refs_json": _v552_refs(series, v552_row, "v552_relation_axis_pressure_refs_json"),
                "v552_target_entity_pressure_refs_json": _v552_refs(series, v552_row, "v552_target_entity_pressure_refs_json"),
                "v552_driver_facet_pressure_refs_json": _v552_refs(series, v552_row, "v552_driver_facet_pressure_refs_json"),
                "v552_contradiction_refs_json": _v552_refs(series, v552_row, "v552_contradiction_refs_json"),
                "v552_horizon_constraint_refs_json": _v552_refs(series, v552_row, "v552_horizon_constraint_refs_json"),
                "v552_parent_prior_refs_json": _v552_refs(series, v552_row, "v552_parent_prior_refs_json"),
                **reliability,
                **normalization,
                "certification_candidate": certification_candidate,
                "v551j_evidence_certification_status": "candidate" if not evidence_certification_blockers else "blocked",
                "v552_handoff_readiness": v552_handoff_readiness,
                "v552_handoff_blockers_json": _json_array(v552_handoff_blockers),
                "certification_blockers_json": _json_array(evidence_certification_blockers),
                "required_for_certification_json": _required_for_certification(series, reason_codes),
            }
        )

    review_surface = pd.DataFrame(rows, columns=V551J_REVIEW_SURFACE_SCHEMA["required_columns"])
    if not review_surface.empty:
        review_surface = review_surface.fillna("")
        review_surface = review_surface.reset_index(drop=True)
    exclusion_audit = pd.DataFrame(exclusion_rows, columns=V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA["required_columns"])
    return review_surface, exclusion_audit, join_audit


def build_v551j_review_readiness_report(
    *,
    run_id: str,
    candidate_trace: pd.DataFrame,
    review_surface: pd.DataFrame,
    exclusion_audit: pd.DataFrame,
    join_audit: pd.DataFrame,
) -> pd.DataFrame:
    surface_status_counts = dict(Counter(review_surface["review_surface_status"].astype(str))) if not review_surface.empty and "review_surface_status" in review_surface.columns else {}
    priority_counts = dict(Counter(review_surface["review_priority"].astype(str))) if not review_surface.empty and "review_priority" in review_surface.columns else {}
    context_status_counts = dict(Counter(review_surface["v552_context_status"].astype(str))) if not review_surface.empty and "v552_context_status" in review_surface.columns else {}
    evidence_certification_status_counts = dict(Counter(review_surface["v551j_evidence_certification_status"].astype(str))) if not review_surface.empty and "v551j_evidence_certification_status" in review_surface.columns else {}
    handoff_readiness_counts = dict(Counter(review_surface["v552_handoff_readiness"].astype(str))) if not review_surface.empty and "v552_handoff_readiness" in review_surface.columns else {}
    certification_blocker_counts: dict[str, int] = {}
    if not review_surface.empty and "certification_blockers_json" in review_surface.columns:
        for cell in review_surface["certification_blockers_json"].astype(str).tolist():
            for token in _parse_json_array(cell):
                certification_blocker_counts[token] = certification_blocker_counts.get(token, 0) + 1
    handoff_blocker_counts: dict[str, int] = {}
    if not review_surface.empty and "v552_handoff_blockers_json" in review_surface.columns:
        for cell in review_surface["v552_handoff_blockers_json"].astype(str).tolist():
            for token in _parse_json_array(cell):
                handoff_blocker_counts[token] = handoff_blocker_counts.get(token, 0) + 1
    row = {
        "run_id": run_id,
        "review_candidate_rows": int(len(candidate_trace)),
        "review_surface_rows": int(len(review_surface)),
        "review_exclusion_rows": int(len(exclusion_audit)),
        "v552_context_join_rows": int(len(join_audit)),
        "review_surface_status_counts": json.dumps(surface_status_counts, sort_keys=True),
        "review_priority_counts": json.dumps(priority_counts, sort_keys=True),
        "v552_context_status_counts": json.dumps(context_status_counts, sort_keys=True),
        "authority_gap_rows": int(review_surface["review_surface_status"].astype(str).eq("reviewable_with_authority_gap").sum()) if not review_surface.empty and "review_surface_status" in review_surface.columns else 0,
        "directionality_gap_rows": int(review_surface["review_surface_status"].astype(str).eq("reviewable_with_directionality_gap").sum()) if not review_surface.empty and "review_surface_status" in review_surface.columns else 0,
        "context_gap_rows": int(review_surface["review_surface_status"].astype(str).eq("reviewable_with_context_gap").sum()) if not review_surface.empty and "review_surface_status" in review_surface.columns else 0,
        "blocked_rows": int(review_surface["review_surface_status"].astype(str).eq("blocked").sum()) if not review_surface.empty and "review_surface_status" in review_surface.columns else 0,
        "diagnostic_only_rows": int(review_surface["review_surface_status"].astype(str).eq("diagnostic_only").sum()) if not review_surface.empty and "review_surface_status" in review_surface.columns else 0,
        "certification_candidate_rows": int(review_surface["certification_candidate"].astype(bool).sum()) if not review_surface.empty and "certification_candidate" in review_surface.columns else 0,
        "v551j_evidence_certification_candidate_rows": int(review_surface["certification_candidate"].astype(bool).sum()) if not review_surface.empty and "certification_candidate" in review_surface.columns else 0,
        "v551j_evidence_certification_status_counts": json.dumps(evidence_certification_status_counts, sort_keys=True),
        "v552_handoff_readiness_counts": json.dumps(handoff_readiness_counts, sort_keys=True),
        "v552_handoff_blocker_counts": json.dumps(handoff_blocker_counts, sort_keys=True),
        "certification_blocker_counts": json.dumps(certification_blocker_counts, sort_keys=True),
        "final_status": "READY_REVIEW_SURFACE_ONLY" if len(review_surface) > 0 else "NOT_READY_NO_REVIEW_SURFACE_ROWS",
        "created_at": utc_now(),
        "schema_version": "v0.1",
    }
    return pd.DataFrame([row], columns=V551J_REVIEW_READINESS_REPORT_SCHEMA["required_columns"])
