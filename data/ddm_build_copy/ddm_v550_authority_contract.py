#!/usr/bin/env python3
"""Fail-closed authority and eligibility contract for V550/V551.

Semantic classification is not permission.  Each downstream use is derived
from independent, visible gates so that missing authority cannot be converted
to a positive decision by a role label, confidence adjective, or fallback.
"""
from __future__ import annotations

from typing import Any, Mapping


CERTIFIED = "CERTIFIED"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
NOT_CERTIFIED = "NOT_CERTIFIED"
MISSING = "MISSING"
CONFLICT = "CONFLICT"
NOT_APPLICABLE = "NOT_APPLICABLE"

APPLICABLE_BY_AUTHORITY = "APPLICABLE_BY_AUTHORITY"
NOT_APPLICABLE_BY_AUTHORITY = "NOT_APPLICABLE_BY_AUTHORITY"
APPLICABILITY_UNRESOLVED = "APPLICABILITY_UNRESOLVED"
DIRECTIONAL_APPLICABILITY_STATUSES = {
    APPLICABLE_BY_AUTHORITY,
    NOT_APPLICABLE_BY_AUTHORITY,
    APPLICABILITY_UNRESOLVED,
}
CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES = {"scalar", "binary_contrast"}

AUTHORITY_STATUSES = {
    CERTIFIED,
    REVIEW_REQUIRED,
    NOT_CERTIFIED,
    MISSING,
    CONFLICT,
    NOT_APPLICABLE,
}

CERTIFIED_RESPONSE_SEMANTICS_STATUSES = {
    "authority_curated",
    "certified",
    "curated",
    "curated_packet",
    "curated_unsigned",
    "family_curated",
    "manual_authority_all_eight",
}

USE_FIELDS = (
    "allowed_as_response_distribution",
    "allowed_as_position_distribution",
    "allowed_as_context_distribution",
    "allowed_as_demographic_predictor",
    "allowed_as_branch_splitter",
    "allowed_as_branch_position_signature",
    "allowed_as_branch_relation_cosignature",
    "allowed_as_attitude_cloud_anchor",
    "allowed_as_attitude_cloud_feature",
    "allowed_as_v551_relation_evidence",
    "allowed_as_parent_prior_coordinate",
    "allowed_as_temporal_pressure_indicator",
    "allowed_as_runtime_persona_evidence",
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    text = _clean(value).lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", ""}:
        return False
    return default


def normalize_authority_status(value: Any, *, missing: str = MISSING) -> str:
    text = _clean(value).upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "APPROVED": CERTIFIED,
        "AUTHORITATIVE": CERTIFIED,
        "CURATED": CERTIFIED,
        "MANUAL_CERTIFIED": CERTIFIED,
        "FOUND": REVIEW_REQUIRED,
        "PASS": REVIEW_REQUIRED,
        "PENDING": REVIEW_REQUIRED,
        "REVIEW": REVIEW_REQUIRED,
        "HEURISTIC": REVIEW_REQUIRED,
        "HEURISTIC_REVIEW_ONLY": REVIEW_REQUIRED,
        "REVIEW_ONLY": REVIEW_REQUIRED,
        "UNKNOWN": MISSING,
        "UNRESOLVED": MISSING,
        "BLOCKED": NOT_CERTIFIED,
        "FAIL": NOT_CERTIFIED,
        "FALSE": NOT_CERTIFIED,
    }
    normalized = aliases.get(text, text)
    return normalized if normalized in AUTHORITY_STATUSES else missing


def semantic_role_authority_status(row: Mapping[str, Any]) -> str:
    explicit = normalize_authority_status(
        row.get("semantic_role_authority_status")
        or row.get("semantic_authority_status"),
    )
    if explicit != MISSING:
        return explicit
    if _bool(row.get("authority_table_used")):
        confidence = _clean(row.get("authority_designation_confidence")).lower()
        manual_required = _bool(row.get("manual_designation_required")) or _bool(
            row.get("itinerary_manual_designation_required")
        )
        if confidence in {"high", "very high"} and not manual_required:
            return CERTIFIED
        return REVIEW_REQUIRED
    if _bool(row.get("manual_override_used")):
        return REVIEW_REQUIRED
    return MISSING


def response_semantics_authority_status(row: Mapping[str, Any]) -> str:
    explicit = normalize_authority_status(row.get("response_semantics_authority_status"))
    if explicit != MISSING:
        return explicit
    status = _clean(row.get("response_semantics_status")).lower()
    source = _clean(row.get("response_semantics_source"))
    contract_hash = _clean(row.get("response_semantics_contract_hash"))
    if status in CERTIFIED_RESPONSE_SEMANTICS_STATUSES and source and contract_hash:
        return CERTIFIED
    if status or source or contract_hash:
        return REVIEW_REQUIRED
    return MISSING


def directionality_authority_status(row: Mapping[str, Any]) -> str:
    """Return only governing directionality authority, never row-level certification.

    ``directional_certification_status`` is a promotability/evidence state.  It
    may be inferred from a response row and therefore cannot be promoted into
    the immutable applicability denominator.
    """
    return normalize_authority_status(row.get("directionality_authority_status"))


def derive_directional_applicability_status(row: Mapping[str, Any]) -> str:
    """Derive the immutable current-directional applicability denominator.

    Applicability is defined only by governing question/directionality
    authority plus the question's semantic role/topology.  Response-map
    success, response intensity, row-level directional certification,
    structural completeness, support, and review/promotability gates are
    deliberately excluded.
    """
    explicit = _clean(row.get("directional_applicability_status")).upper()
    if explicit in DIRECTIONAL_APPLICABILITY_STATUSES:
        return explicit

    role = _clean(row.get("semantic_role")).upper()
    topology = _clean(row.get("response_topology")).lower()
    authority_status = directionality_authority_status(row)

    if authority_status == NOT_APPLICABLE:
        return NOT_APPLICABLE_BY_AUTHORITY
    if role and role != "RELATION_EVIDENCE":
        return NOT_APPLICABLE_BY_AUTHORITY
    if topology and topology not in CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES:
        return NOT_APPLICABLE_BY_AUTHORITY

    if not role or not topology:
        return APPLICABILITY_UNRESOLVED
    if authority_status == CERTIFIED:
        return APPLICABLE_BY_AUTHORITY
    return APPLICABILITY_UNRESOLVED


def structural_mapping_status(row: Mapping[str, Any]) -> str:
    explicit = _clean(row.get("structural_mapping_status")).upper()
    if explicit in {
        "COMPLETE",
        "PARTIAL",
        "PENDING",
        "INTENTIONALLY_AXISLESS",
        "NOT_APPLICABLE",
        "CONFLICT",
        "BLOCKED",
    }:
        return explicit
    role = _clean(row.get("semantic_role")).upper()
    if role in {
        "ADMINISTRATIVE_METADATA",
        "GENERATION_FORBIDDEN",
        "MISSINGNESS_SIGNAL",
    }:
        return "NOT_APPLICABLE"
    if not _bool(row.get("source_structure_fields_joined")):
        return "PENDING"
    if _bool(row.get("source_structure_review_required")):
        return "PARTIAL"
    mapping = _clean(row.get("mapping_status")).lower()
    axis = _clean(row.get("relation_axis_id")).lower()
    target = _clean(row.get("target_entity_id")).lower()
    if role == "RELATION_EVIDENCE":
        if mapping in {"", "pending", "unknown", "unresolved"}:
            return "PENDING"
        if axis in {"", "context", "unknown", "unresolved"}:
            return "PARTIAL"
        if target in {"", "context", "context_not_applicable", "unknown", "unresolved"}:
            return "PARTIAL"
    return "COMPLETE"


def conservative_uses_for_role(role: Any) -> dict[str, bool]:
    """Return role-shape hints only; no high-risk permission is granted."""
    normalized = _clean(role).upper() or "UNKNOWN"
    uses = {field: False for field in USE_FIELDS}
    uses["allowed_as_response_distribution"] = normalized == "RELATION_EVIDENCE"
    uses["allowed_as_position_distribution"] = normalized == "POSITION_COORDINATE"
    uses["allowed_as_context_distribution"] = normalized == "STRUCTURAL_CONTEXT"
    return uses


def derive_question_use_eligibility(row: Mapping[str, Any]) -> dict[str, Any]:
    role = _clean(row.get("semantic_role")).upper() or "UNKNOWN"
    semantic_status = semantic_role_authority_status(row)
    response_status = response_semantics_authority_status(row)
    direction_status = directionality_authority_status(row)
    applicability_status = derive_directional_applicability_status(row)
    mapping_status = structural_mapping_status(row)
    review_required = any(
        _bool(row.get(field))
        for field in (
            "review_required",
            "manual_review_required",
            "manual_designation_required",
            "source_structure_review_required",
            "authority_review_required",
        )
    )
    forbidden = role in {
        "ADMINISTRATIVE_METADATA",
        "GENERATION_FORBIDDEN",
        "MISSINGNESS_SIGNAL",
        "UNKNOWN",
    }
    relation = role == "RELATION_EVIDENCE"
    position = role == "POSITION_COORDINATE"
    context = role == "STRUCTURAL_CONTEXT"
    semantic_certified = semantic_status == CERTIFIED
    response_certified = response_status == CERTIFIED
    direction_applicable = applicability_status == APPLICABLE_BY_AUTHORITY
    structure_complete = mapping_status == "COMPLETE"

    failed: list[str] = []
    for condition, reason in (
        (relation, "semantic_role_not_relation_evidence"),
        (semantic_certified, f"semantic_role_authority_{semantic_status.lower()}"),
        (response_certified, f"response_semantics_authority_{response_status.lower()}"),
        (direction_applicable, f"directional_applicability_{applicability_status.lower()}"),
        (structure_complete, f"structural_mapping_{mapping_status.lower()}"),
        (not review_required, "review_required"),
        (not forbidden, "forbidden_semantic_role"),
    ):
        if not condition:
            failed.append(reason)

    v551 = not failed
    runtime_authority = normalize_authority_status(row.get("runtime_authority_status"))
    runtime = v551 and runtime_authority == CERTIFIED

    uses = {field: False for field in USE_FIELDS}
    uses["allowed_as_response_distribution"] = (
        relation and semantic_certified and response_certified and not review_required
    )
    uses["allowed_as_position_distribution"] = (
        position and semantic_certified and mapping_status in {"COMPLETE", "INTENTIONALLY_AXISLESS"}
        and not review_required
    )
    uses["allowed_as_context_distribution"] = (
        context and semantic_certified and not review_required
    )
    uses["allowed_as_demographic_predictor"] = (
        position and semantic_certified and structure_complete and not review_required
    )
    uses["allowed_as_branch_splitter"] = (
        (relation or position or context) and semantic_certified and structure_complete
        and not review_required
    )
    uses["allowed_as_branch_position_signature"] = uses["allowed_as_demographic_predictor"]
    uses["allowed_as_branch_relation_cosignature"] = v551
    uses["allowed_as_attitude_cloud_anchor"] = v551
    uses["allowed_as_attitude_cloud_feature"] = v551
    uses["allowed_as_v551_relation_evidence"] = v551
    uses["allowed_as_parent_prior_coordinate"] = uses["allowed_as_demographic_predictor"]
    uses["allowed_as_temporal_pressure_indicator"] = (
        (v551 or uses["allowed_as_demographic_predictor"])
        and normalize_authority_status(row.get("temporal_authority_status")) == CERTIFIED
    )
    uses["allowed_as_runtime_persona_evidence"] = runtime

    return {
        **uses,
        "semantic_role_authority_status": semantic_status,
        "response_semantics_authority_status": response_status,
        "directionality_authority_status": direction_status,
        "directional_applicability_status": applicability_status,
        "structural_mapping_status": mapping_status,
        "runtime_authority_status": runtime_authority,
        "eligibility_gate_status": CERTIFIED if v551 else NOT_CERTIFIED,
        "eligibility_failed_gates": "|".join(dict.fromkeys(failed)),
        "current_directional_atom_eligible": bool(direction_applicable),
    }
