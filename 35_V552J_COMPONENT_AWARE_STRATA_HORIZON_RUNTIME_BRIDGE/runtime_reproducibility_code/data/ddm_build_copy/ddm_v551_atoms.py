#!/usr/bin/env python3
"""Helpers for compiling deterministic V551 relation-evidence atoms."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from data.ddm_build_copy.ddm_v550_metrics import evidence_stratum_from_row, evidence_stratum_v2_from_row, numeric_wrapper_audit_from_row
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.numeric_formulas import support_prevalence_companions
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, confidence_tier_from_support, support_status_from_count, support_threshold_from_total
from data.ddm_build_copy.ddm_v550_authority_contract import (
    CERTIFIED_RESPONSE_SEMANTICS_STATUSES,
)
from data.ddm_build_copy.ddm_v550_schema import V551_ATOM_EXCLUSION_AUDIT_SCHEMA, V551_BLOCKED_SIGNAL_AUDIT_SCHEMA, V551_LINEAGE_BASIS_AUDIT_SCHEMA, V551_NUMERIC_WRAPPER_AUDIT_SCHEMA, V551_PRESSURE_COMPONENT_AUDIT_SCHEMA, V551_RELATION_EVIDENCE_ATOMS_SCHEMA, V551_RELATION_REVIEW_SURFACE_SCHEMA, validate_columns

ATOM_SCHEMA_VERSION = "v2.1"
MIN_ATOM_SUPPORT = DEFAULT_SUPPORT_CAP
V551_EMPIRICAL_DISTRIBUTION_GROUP_COLUMNS = [
    "source",
    "source_family",
    "canonical_wave",
    "country_code",
    "survey_year",
    "analysis_scope",
    "empirical_distribution_id",
    "question_id",
    "var_code",
    "position_field",
    "position_value",
    "response_scale_signature",
    "semantic_identity_signature",
    "structural_identity_signature",
]
V551_REQUIRED_BRIDGE_CONTRACT_COLUMNS = [
    "run_id", "shard_id", "source", "source_family", "wave", "canonical_wave", "country_code", "survey_year", "analysis_scope",
    "empirical_object_type", "empirical_object_id", "source_table", "source_row_hash", "question_id", "var_code", "position_field", "position_value",
    "response_value_raw", "response_value_normalized", "response_label", "normalized_response_label", "response_family", "response_direction", "response_intensity", "polarity", "ordinal_rank", "scale_min", "scale_max", "scale_direction", "directionality_status", "response_topology",
    "n_unweighted", "n_respondents", "n_weighted", "pct_unweighted", "pct_weighted", "weight_status", "support_status", "support_score", "prevalence_score",
    "is_substantive", "is_missing", "is_special", "usable_for_evidence",
    "bridge_evidence_lane", "v551_relation_evidence_eligible", "allowed_as_v551_relation_evidence", "allowed_as_temporal_pressure_indicator", "allowed_as_runtime_persona_evidence",
    "semantic_role", "semantic_subrole", "semantic_tags", "directionality_policy", "driver_id", "driver_facet_id", "relation_axis_id", "target_entity_id", "strata_relevance", "strata_path", "subject_position_signature", "position_conditioning", "position_modifiers", "conditional_strata_weights", "horizon_affordance", "mapping_status",
    "response_option_map_matched", "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash", "semantic_role_authority_status", "response_semantics_authority_status", "directionality_authority_status", "directional_certification_status", "current_directional_atom_eligible", "structural_mapping_status", "eligibility_gate_status", "eligibility_failed_gates",
    "question_use_contract_joined", "source_structure_fields_joined", "source_structure_basis", "source_structure_confidence", "source_structure_source", "source_structure_review_required",
    "manual_review_flag", "manual_review_reason", "forbidden_inference", "known_absences", "evidence_basis", "provenance_basis",
]
APPROVED_EMPIRICAL_OBJECT_TYPES = {"answer_distribution", "country_answer_distribution"}
APPROVED_DIRECT_RELATION_SOURCE_TABLES = {"answer_distribution", "country_answer_distribution"}
PRESSURE_COMPONENT_REASON_ORDER = [
    "v551_relation_evidence_not_authorized",
    "not_usable_for_evidence",
    "manual_review_required",
    "source_structure_review_required",
    "response_semantics_authority_not_certified",
    "directionality_authority_not_certified",
    "structural_mapping_not_complete",
    "missing_observed_distribution_measure",
    "missing_directional_measure",
    "special_or_missing_response",
    "unsupported_empirical_object",
]
SOURCE_TABLE_PRIORITY = {
    "answer_distribution": 0,
    "country_answer_distribution": 1,
    "outlier_cohort_summary": 2,
    "recursive_branch_nodes": 3,
    "indicator_answer_matrix": 4,
}
NUMERIC_ONLY_LABEL_ALLOWED_FAMILIES = {
    "yes_no",
    "agreement_scale",
    "trust_scale",
    "satisfaction_scale",
    "importance_scale",
    "frequency_scale",
    "ordinal_scale",
    "left_right_scale",
    "numeric_quantity",
    "numeric_scale",
    "count",
    "count_scale",
}

APPROVED_DIRECTIONAL_INTENSITY_RESPONSE_FAMILIES = {
    "agreement_scale",
    "count",
    "count_scale",
    "frequency_scale",
    "importance_scale",
    "left_right_scale",
    "numeric_quantity",
    "numeric_scale",
    "ordinal_scale",
    "satisfaction_scale",
    "signed_direction",
    "signed_evaluation",
    "signed_frequency",
    "signed_policy",
    "signed_position",
    "signed_scale",
    "signed_attitude",
    "trust_scale",
    "yes_no",
}

DIRECTION_PLACEHOLDER_VALUES = {
    "",
    "na",
    "nan",
    "missing",
    "not_applicable",
    "not applicable",
    "not_certified",
    "not_inferred",
    "none",
    "signed",
    "unknown",
    "unsigned",
    "unresolved",
    "review_required",
}

DIRECTION_CERTIFIED_VALUES = {
    "agree",
    "disagree",
    "graded",
    "intermediate",
    "negative",
    "neutral",
    "oppose",
    "positive",
    "support",
}


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


def _stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _canonical_scalar(value: Any) -> Any:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return format(value, ".12g")
    return str(value).strip()


def _hash_fields(row: dict[str, Any], fields: list[str]) -> str:
    return _stable_hash({field: _canonical_scalar(row.get(field)) for field in fields})


def _series_hash(series: pd.Series) -> str:
    values = [str(value) for value in series.fillna("").astype(str).tolist()]
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def _support_status(n_unweighted: float | int | None) -> str:
    return support_status_from_count(n_unweighted, support_cap=MIN_ATOM_SUPPORT)


def _support_status_for_row(row: Mapping[str, Any]) -> str:
    return support_status_from_count(
        row.get("n_unweighted"),
        total_respondents=row.get("n_respondents"),
        lane=row.get("bridge_evidence_lane", "relation"),
        support_cap=MIN_ATOM_SUPPORT,
    )


def _confidence_tier(row: dict[str, Any]) -> str:
    if _to_bool(row.get("source_structure_fields_joined"), False) and _to_bool(row.get("question_use_contract_joined"), False) and _clean(row.get("normalization_confidence")).lower() == "high":
        return "high"
    support = float(row.get("n_unweighted") or 0)
    threshold = support_threshold_from_total(row.get("n_respondents"), support_cap=MIN_ATOM_SUPPORT)
    if support >= 100:
        return "high"
    if support >= threshold:
        return "medium"
    return "low"


def _safe_float(value: Any) -> float | None:
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        parsed = float(value)
        if pd.isna(parsed):
            return None
        return parsed
    except Exception:
        return None


def _optional_positive_integer(value: Any) -> int | None:
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return None
    numeric_float = float(numeric)
    if not math.isfinite(numeric_float):
        return None
    if numeric_float <= 0:
        return None
    if not numeric_float.is_integer():
        return None
    return int(numeric_float)


def _response_intensity(row: pd.Series) -> float | None:
    if _certified_response_direction(row) == "neutral":
        return 0.0
    if "response_intensity" in row.index:
        parsed = _safe_float(row.get("response_intensity"))
        if parsed is not None:
            return parsed
    return None


def _source_measure_status(row: pd.Series) -> str:
    support = _safe_float(row.get("n_unweighted"))
    if support is None or support < 0:
        return "INVALID"
    return "OBSERVED"


def _directional_measure_kind(row: pd.Series) -> str:
    has_direction = bool(_certified_response_direction(row))
    has_intensity = _safe_float(row.get("response_intensity")) is not None
    if has_direction and has_intensity:
        return "direction_and_intensity"
    if has_direction:
        return "direction_only"
    if has_intensity:
        return "intensity_only"
    return "none"


def _response_direction_status(row: pd.Series) -> str:
    if _certified_response_direction(row):
        return "CERTIFIED_EXPLICIT"
    response_family = _clean(row.get("response_family")).lower()
    if response_family in APPROVED_DIRECTIONAL_INTENSITY_RESPONSE_FAMILIES and _safe_float(row.get("response_intensity")) is not None:
        return "CERTIFIED_INTENSITY_ONLY"
    return "MISSING_OR_PLACEHOLDER"


def _response_intensity_status(row: pd.Series) -> str:
    return "OBSERVED_NUMERIC" if _safe_float(row.get("response_intensity")) is not None else "MISSING"


def _v551_signed_projection(row: pd.Series) -> dict[str, Any]:
    authority_direction = _certified_response_direction(row)
    authority_intensity = _safe_float(row.get("response_intensity"))
    authority_scale_direction = _clean(row.get("scale_direction"))
    if not authority_direction:
        return {
            "authority_response_direction": _clean(row.get("response_direction")),
            "authority_response_intensity": authority_intensity,
            "authority_scale_direction": authority_scale_direction,
            "v551_signed_side": "",
            "v551_signed_intensity": None,
            "v551_projection_rule_id": "BLOCKED_UNRESOLVED_AUTHORITY_TOKEN",
            "v551_projection_authority_hash": "",
        }
    if authority_direction in {"positive", "support", "agree"}:
        signed_side = "positive"
        signed_intensity = authority_intensity if authority_intensity is not None else 1.0
        rule_id = "v551_signed_projection_direct_positive_v1"
    elif authority_direction in {"negative", "oppose", "disagree"}:
        signed_side = "negative"
        signed_intensity = authority_intensity if authority_intensity is not None else 1.0
        rule_id = "v551_signed_projection_direct_negative_v1"
    elif authority_direction == "neutral":
        signed_side = "neutral"
        signed_intensity = 0.0
        rule_id = "v551_signed_projection_explicit_neutral_v1"
    elif authority_direction in {"graded", "intermediate"} and authority_intensity is not None:
        if authority_intensity > 0.5:
            signed_side = "positive"
        elif authority_intensity < 0.5:
            signed_side = "negative"
        else:
            signed_side = "neutral"
        signed_intensity = round(abs(authority_intensity - 0.5) * 2.0, 6)
        rule_id = f"v551_signed_projection_{authority_direction}_coordinate_v1"
    else:
        signed_side = ""
        signed_intensity = None
        rule_id = "BLOCKED_UNRESOLVED_AUTHORITY_TOKEN"
    payload = {
        "authority_response_direction": authority_direction,
        "authority_response_intensity": authority_intensity,
        "authority_scale_direction": authority_scale_direction,
        "v551_signed_side": signed_side,
        "v551_signed_intensity": signed_intensity,
        "v551_projection_rule_id": rule_id,
        "directionality_authority_status": _clean(row.get("directionality_authority_status")).upper(),
        "response_semantics_contract_hash": _clean(row.get("response_semantics_contract_hash")),
    }
    return {
        **payload,
        "v551_projection_authority_hash": _stable_hash(payload) if signed_side else "",
    }


def _pressure_component_decision(base: dict[str, Any], *, source_measure_status: str, directional_measure_kind: str) -> tuple[bool, str, str, str]:
    reasons: list[str] = []
    if _clean(base.get("response_direction")).lower() == "neutral":
        reasons.append("coverage_only_neutral")
    if not _to_bool(base.get("allowed_as_v551_relation_evidence"), False):
        reasons.append("v551_relation_evidence_not_authorized")
    if not _to_bool(base.get("usable_for_evidence"), False):
        reasons.append("not_usable_for_evidence")
    if _to_bool(base.get("manual_review_flag"), False):
        reasons.append("manual_review_required")
    if _to_bool(base.get("source_structure_review_required"), False):
        reasons.append("source_structure_review_required")
    if _clean(base.get("response_semantics_authority_status")).upper() != "CERTIFIED":
        reasons.append("response_semantics_authority_not_certified")
    if _clean(base.get("directionality_authority_status")).upper() != "CERTIFIED":
        reasons.append("directionality_authority_not_certified")
    if _clean(base.get("structural_mapping_status")).upper() != "COMPLETE":
        reasons.append("structural_mapping_not_complete")
    if source_measure_status != "OBSERVED":
        reasons.append("missing_observed_distribution_measure")
    if directional_measure_kind == "none":
        reasons.append("missing_directional_measure")
    if _to_bool(base.get("is_missing"), False) or _to_bool(base.get("is_special"), False):
        reasons.append("special_or_missing_response")
    if _clean(base.get("empirical_object_type")) not in APPROVED_EMPIRICAL_OBJECT_TYPES:
        reasons.append("unsupported_empirical_object")
    support_status = _clean(base.get("support_status"))
    if support_status and support_status not in {"sufficient_support", "supported"}:
        reasons.append("low_support_review_required")
    ordered = [reason for reason in PRESSURE_COMPONENT_REASON_ORDER if reason in set(reasons)]
    if "coverage_only_neutral" in reasons:
        ordered.append("coverage_only_neutral")
    if "low_support_review_required" in reasons:
        ordered.append("low_support_review_required")
    reason_text = "|".join(ordered)
    if "coverage_only_neutral" in ordered:
        status = "COVERAGE_ONLY_NEUTRAL"
    elif "manual_review_required" in ordered or "source_structure_review_required" in ordered or "low_support_review_required" in ordered:
        status = "REVIEW_REQUIRED"
    elif ordered:
        status = "INELIGIBLE"
    else:
        status = "ELIGIBLE"
    eligible = status == "ELIGIBLE"
    if status == "COVERAGE_ONLY_NEUTRAL":
        pressure_class = "coverage_only_neutral_relation_evidence"
    elif status == "REVIEW_REQUIRED":
        pressure_class = "directional_response_review_required"
    elif eligible:
        pressure_class = "directional_response_pressure_component_candidate"
    else:
        pressure_class = "directional_response_relation_evidence_only"
    return eligible, status, reason_text, pressure_class


def _response_scale_signature(row: dict[str, Any]) -> str:
    return _hash_fields(row, ["response_family", "response_topology", "scale_min", "scale_max", "scale_direction", "directionality_policy", "response_semantics_contract_hash"])


def _semantic_identity_signature(row: dict[str, Any]) -> str:
    return _hash_fields(row, ["semantic_role", "semantic_subrole", "semantic_tags", "relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id", "response_family", "directionality_policy"])


def _structural_identity_signature(row: dict[str, Any]) -> str:
    return _hash_fields(row, ["relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id", "strata_path", "subject_position_signature", "position_conditioning", "position_modifiers", "conditional_strata_weights", "horizon_affordance"])


def _empirical_distribution_identity_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract": "V551_EMPIRICAL_DISTRIBUTION_ID_V1",
        "source": _clean(row.get("source")),
        "source_family": _clean(row.get("source_family")),
        "canonical_wave": _clean(row.get("canonical_wave")),
        "country_code": _clean(row.get("country_code")),
        "survey_year": _canonical_scalar(row.get("survey_year")) or None,
        "analysis_scope": _clean(row.get("analysis_scope")),
        "empirical_object_type": _clean(row.get("empirical_object_type")),
        "source_table": _clean(row.get("source_table")),
        "question_id": _clean(row.get("question_id")),
        "var_code": _clean(row.get("var_code")),
        "position_field": _clean(row.get("position_field")),
        "position_value": _clean(row.get("position_value")),
        "response_scale_signature": _clean(row.get("response_scale_signature")),
        "semantic_identity_signature": _clean(row.get("semantic_identity_signature")),
        "structural_identity_signature": _clean(row.get("structural_identity_signature")),
    }


def _empirical_distribution_id(row: Mapping[str, Any]) -> str:
    payload = _empirical_distribution_identity_payload(row)
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()[:24]
    return f"v551dist__{digest}"


def _measurement_contract_hash(row: dict[str, Any]) -> str:
    return _hash_fields(row, ["empirical_object_type", "empirical_object_id", "source_table", "source_row_hash", "source_measure_kind", "source_measure_status", "response_value_raw", "response_value_normalized", "authority_response_direction", "authority_response_intensity", "authority_scale_direction", "response_direction", "response_direction_status", "response_intensity", "response_intensity_status", "observed_response_zero", "v551_projection_rule_id", "v551_projection_authority_hash", "n_unweighted", "n_respondents", "n_weighted", "pct_unweighted", "pct_weighted", "support_formula_id", "support_formula_version", "prevalence_formula_id", "prevalence_formula_version", "pressure_evidence_class", "v552_pressure_component_status"])


def _atom_contract_hash(row: dict[str, Any]) -> str:
    return _hash_fields(row, ["atom_id", "empirical_distribution_id", "response_scale_signature", "semantic_identity_signature", "structural_identity_signature", "measurement_contract_hash", "v551_projection_authority_hash", "semantic_role_authority_status", "response_semantics_authority_status", "directionality_authority_status", "structural_mapping_status", "allowed_as_v551_relation_evidence", "allowed_as_temporal_pressure_indicator", "v552_pressure_component_eligible", "manual_review_flag", "source_structure_review_required", "forbidden_inference", "known_absences", "evidence_basis", "evidence_basis_origin", "provenance_basis", "provenance_basis_origin", "temporal_authority_status"])


def _require_clean(base: dict[str, Any], fields: list[str]) -> None:
    if any(not _clean(base.get(field)) for field in fields):
        raise ValueError("missing_derivation_input")


def _derive_evidence_basis(base: dict[str, Any]) -> tuple[str, str]:
    source_value = _clean(base.get("evidence_basis"))
    if source_value:
        return source_value, "SOURCE_PROVIDED"
    required = [
        "empirical_object_type",
        "source_table",
        "bridge_evidence_lane",
        "semantic_role",
        "response_semantics_authority_status",
        "directionality_authority_status",
        "structural_mapping_status",
    ]
    _require_clean(base, required)
    empirical_object_type = _clean(base.get("empirical_object_type"))
    source_table = _clean(base.get("source_table"))
    bridge_evidence_lane = _clean(base.get("bridge_evidence_lane"))
    semantic_role = _clean(base.get("semantic_role"))
    if empirical_object_type not in APPROVED_EMPIRICAL_OBJECT_TYPES:
        raise ValueError("missing_derivation_input")
    if source_table not in APPROVED_DIRECT_RELATION_SOURCE_TABLES:
        raise ValueError("missing_derivation_input")
    if bridge_evidence_lane != "direct_relation_response":
        raise ValueError("missing_derivation_input")
    if semantic_role != "RELATION_EVIDENCE":
        raise ValueError("missing_derivation_input")
    payload = {
        "bridge_evidence_lane": bridge_evidence_lane,
        "contract": "V551_EVIDENCE_BASIS_V1",
        "directionality_authority_status": _clean(base.get("directionality_authority_status")).upper(),
        "empirical_object_type": empirical_object_type,
        "empirical_observation_class": "single_question_response_category_observation",
        "response_semantics_authority_status": _clean(base.get("response_semantics_authority_status")).upper(),
        "semantic_role": semantic_role,
        "source_measure_kind": "response_category_distribution",
        "source_table": source_table,
        "structural_mapping_status": _clean(base.get("structural_mapping_status")).upper(),
    }
    return _canonical_json(payload), "DERIVED_FROM_ACCEPTED_V550_BRIDGE"


def _derive_provenance_basis(base: dict[str, Any]) -> tuple[str, str]:
    source_value = _clean(base.get("provenance_basis"))
    if source_value:
        return source_value, "SOURCE_PROVIDED"
    required = [
        "run_id",
        "shard_id",
        "source",
        "canonical_wave",
        "country_code",
        "empirical_object_id",
        "source_table",
        "source_row_hash",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
    ]
    _require_clean(base, required)
    payload = {
        "canonical_wave": _clean(base.get("canonical_wave")),
        "contract": "V551_PROVENANCE_BASIS_V1",
        "country_code": _clean(base.get("country_code")),
        "empirical_object_id": _clean(base.get("empirical_object_id")),
        "response_semantics_contract_hash": _clean(base.get("response_semantics_contract_hash")),
        "response_semantics_source": _clean(base.get("response_semantics_source")),
        "source": _clean(base.get("source")),
        "source_row_hash": _clean(base.get("source_row_hash")),
        "source_structure_basis": _clean(base.get("source_structure_basis")),
        "source_structure_confidence": _clean(base.get("source_structure_confidence")),
        "source_structure_source": _clean(base.get("source_structure_source")),
        "source_table": _clean(base.get("source_table")),
        "source_v550_run_id": _clean(base.get("run_id")),
        "source_v550_shard_id": _clean(base.get("shard_id")),
    }
    return _canonical_json(payload), "DERIVED_FROM_ACCEPTED_V550_BRIDGE"


def validate_v551_bridge_input_contract(bridge: pd.DataFrame) -> dict[str, Any]:
    missing = [column for column in V551_REQUIRED_BRIDGE_CONTRACT_COLUMNS if column not in bridge.columns]
    return {
        "status": "BLOCKED_V551_MISSING_BRIDGE_CONTRACT" if missing else "PASS",
        "bridge_rows": int(len(bridge)),
        "missing_columns": missing,
        "required_column_count": int(len(V551_REQUIRED_BRIDGE_CONTRACT_COLUMNS)),
        "present_required_column_count": int(len(V551_REQUIRED_BRIDGE_CONTRACT_COLUMNS) - len(missing)),
    }


def _response_direction(row: pd.Series) -> str:
    for field in ["response_direction", "directionality", "orientation", "polarity"]:
        value = _clean(row.get(field))
        if value:
            return value
    return ""


def _certified_response_direction(row: pd.Series) -> str:
    for field in ["response_direction", "directionality", "orientation", "polarity"]:
        value = _clean(row.get(field)).lower()
        if not value or value in DIRECTION_PLACEHOLDER_VALUES:
            continue
        if value in DIRECTION_CERTIFIED_VALUES:
            return value
    return ""


def _has_any_directionality_value(row: pd.Series) -> bool:
    return any(_clean(row.get(field)) for field in ("response_direction", "directionality", "orientation", "polarity"))


def _has_certified_directional_response(row: pd.Series) -> bool:
    certified_direction = _certified_response_direction(row)
    if certified_direction:
        return True
    if _has_any_directionality_value(row):
        return False
    response_family = _clean(row.get("response_family")).lower()
    if response_family not in APPROVED_DIRECTIONAL_INTENSITY_RESPONSE_FAMILIES:
        return False
    return _safe_float(row.get("response_intensity")) is not None


def _allowed_source_table(value: Any) -> bool:
    return _clean(value) in SOURCE_TABLE_PRIORITY


def _directional_certification_status(value: Any) -> str:
    status = _clean(value).upper()
    return status if status == "CERTIFIED" else "NOT_CERTIFIED"


def _support_count_from_row(row: pd.Series) -> float | None:
    for field in ("n_unweighted", "support_n_unweighted", "support_count", "support_n_total"):
        parsed = _safe_float(row.get(field))
        if parsed is not None:
            return parsed
    return None


def _is_numeric_only_label(value: Any) -> bool:
    text = _clean(value)
    return bool(text) and bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", text))


def _response_family_allows_numeric_only_label(value: Any) -> bool:
    family = _clean(value).lower()
    if not family:
        return False
    if family in NUMERIC_ONLY_LABEL_ALLOWED_FAMILIES:
        return True
    return family.endswith("_scale") or any(token in family for token in {"numeric", "quantity", "count"})


def _atom_id(row: dict[str, Any]) -> str:
    payload = {
        "source": row.get("source", ""),
        "canonical_wave": row.get("canonical_wave", ""),
        "country_code": row.get("country_code", ""),
        "question_id": row.get("question_id", ""),
        "var_code": row.get("var_code", ""),
        "response_value_normalized": row.get("response_value_normalized", ""),
        "relation_axis_id": row.get("relation_axis_id", ""),
        "target_entity_id": row.get("target_entity_id", ""),
        "driver_id": row.get("driver_id", ""),
        "source_table": row.get("source_table", ""),
        "source_row_hash": row.get("source_row_hash", ""),
        "source_run_id": row.get("source_run_id", ""),
    }
    return _stable_hash(payload)


def _canonical_empirical_key(row: pd.Series) -> str:
    payload = {
        "source": _clean(row.get("source")),
        "wave": _clean(row.get("wave")),
        "canonical_wave": _clean(row.get("canonical_wave")),
        "country_code": _clean(row.get("country_code")),
        "question_id": _clean(row.get("question_id")),
        "var_code": _clean(row.get("var_code")),
        "response_value_normalized": _clean(row.get("response_value_normalized")),
        "relation_axis_id": _clean(row.get("relation_axis_id")),
        "target_entity_id": _clean(row.get("target_entity_id")),
        "driver_id": _clean(row.get("driver_id")),
        "source_run_id": _clean(row.get("run_id") or row.get("source_run_id")),
    }
    return _stable_hash(payload)


def _atom_row(row: pd.Series, *, question_use_contract_hash: str, source_structure_population_hash: str, response_option_map_hash: str) -> dict[str, Any]:
    base = row.to_dict()
    evidence_basis, evidence_basis_origin = _derive_evidence_basis(base)
    provenance_basis, provenance_basis_origin = _derive_provenance_basis(base)
    response_intensity = _response_intensity(row)
    signed_projection = _v551_signed_projection(row)
    source_measure_status = _source_measure_status(row)
    directional_measure_kind = _directional_measure_kind(row)
    response_direction_status = _response_direction_status(row)
    response_intensity_status = _response_intensity_status(row)
    observed_response_zero = bool(response_intensity_status == "OBSERVED_NUMERIC" and response_intensity == 0.0)
    support_status = _support_status_for_row(base)
    base["support_status"] = support_status
    low_support_review_required = support_status not in {"sufficient_support", "supported"}
    pressure_eligible, pressure_status, pressure_reason, pressure_class = _pressure_component_decision(
        base,
        source_measure_status=source_measure_status,
        directional_measure_kind=directional_measure_kind,
    )
    if low_support_review_required:
        pressure_eligible = False
        if pressure_status != "COVERAGE_ONLY_NEUTRAL":
            pressure_status = "REVIEW_REQUIRED"
        pressure_reason = "|".join(
            reason for reason in [pressure_reason, "low_support_review_required"] if reason
        )
        if pressure_class != "coverage_only_neutral_relation_evidence":
            pressure_class = "directional_response_review_required"
    support_companions = support_prevalence_companions(
        base.get("n_unweighted"),
        total_respondents=base.get("n_respondents"),
        lane=base.get("bridge_evidence_lane", "relation"),
        support_cap=MIN_ATOM_SUPPORT,
    )
    result = {
        "shard_id": _clean(base.get("shard_id")),
        "source": _clean(base.get("source")),
        "source_family": _clean(base.get("source_family")),
        "wave": _clean(base.get("wave")),
        "canonical_wave": _clean(base.get("canonical_wave")),
        "country_code": _clean(base.get("country_code")),
        "survey_year": base.get("survey_year"),
        "analysis_scope": _clean(base.get("analysis_scope")),
        "empirical_object_type": _clean(base.get("empirical_object_type")),
        "empirical_object_id": _clean(base.get("empirical_object_id")),
        "question_id": _clean(base.get("question_id")),
        "var_code": _clean(base.get("var_code")),
        "question_text": _clean(base.get("question_text")),
        "position_field": _clean(base.get("position_field")),
        "position_value": _clean(base.get("position_value")),
        "response_value_raw": _clean(base.get("response_value_raw")),
        "response_value_normalized": _clean(base.get("response_value_normalized")),
        "response_label": _clean(base.get("response_label")),
        "normalized_response_label": _clean(base.get("normalized_response_label")),
        "response_family": _clean(base.get("response_family")),
        "bridge_evidence_lane": _clean(base.get("bridge_evidence_lane")),
        **signed_projection,
        "response_direction": _response_direction(row),
        "response_intensity": response_intensity,
        "polarity": _clean(base.get("polarity")),
        "ordinal_rank": base.get("ordinal_rank"),
        "scale_min": base.get("scale_min"),
        "scale_max": base.get("scale_max"),
        "scale_direction": _clean(base.get("scale_direction")),
        "directionality_status": _clean(base.get("directionality_status")) or "unknown",
        "response_topology": _clean(base.get("response_topology")),
        "future_evidence_eligible": _to_bool(base.get("future_evidence_eligible"), False),
        "future_topology_evidence_eligible": _to_bool(base.get("future_topology_evidence_eligible"), _to_bool(base.get("future_evidence_eligible"), False)),
        "current_directional_atom_eligible": _to_bool(base.get("current_directional_atom_eligible"), False),
        "directional_certification_status": _directional_certification_status(base.get("directional_certification_status")),
        "semantic_role_authority_status": _clean(base.get("semantic_role_authority_status")).upper(),
        "response_semantics_authority_status": _clean(base.get("response_semantics_authority_status")).upper(),
        "directionality_authority_status": _clean(base.get("directionality_authority_status")).upper(),
        "structural_mapping_status": _clean(base.get("structural_mapping_status")).upper(),
        "eligibility_gate_status": _clean(base.get("eligibility_gate_status")),
        "eligibility_failed_gates": _clean(base.get("eligibility_failed_gates")),
        "semantic_role": _clean(base.get("semantic_role")),
        "v551_evidence_role": "relation_evidence",
        "evidence_stratum": evidence_stratum_from_row(
            bridge_evidence_lane=base.get("bridge_evidence_lane", ""),
            semantic_role="RELATION_EVIDENCE",
            v551_relation_evidence_eligible=base.get("v551_relation_evidence_eligible"),
        ),
        "evidence_stratum_v2": evidence_stratum_v2_from_row(
            bridge_evidence_lane=base.get("bridge_evidence_lane", ""),
            semantic_role="RELATION_EVIDENCE",
            v551_relation_evidence_eligible=base.get("v551_relation_evidence_eligible"),
        ),
        "driver_id": _clean(base.get("driver_id")),
        "driver_facet_id": _clean(base.get("driver_facet_id")),
        "relation_axis_id": _clean(base.get("relation_axis_id")),
        "target_entity_id": _clean(base.get("target_entity_id")),
        "strata_relevance": _clean(base.get("strata_relevance")),
        "strata_path": _clean(base.get("strata_path")),
        "subject_position_signature": _clean(base.get("subject_position_signature")),
        "is_substantive": _to_bool(base.get("is_substantive"), False),
        "is_missing": _to_bool(base.get("is_missing"), False),
        "is_special": _to_bool(base.get("is_special"), False),
        "usable_for_evidence": _to_bool(base.get("usable_for_evidence"), False),
        "response_option_map_matched": _to_bool(base.get("response_option_map_matched"), False),
        "response_semantics_status": _clean(base.get("response_semantics_status")),
        "response_semantics_source": _clean(base.get("response_semantics_source")),
        "response_semantics_contract_hash": _clean(base.get("response_semantics_contract_hash")),
        "normalization_confidence": _clean(base.get("normalization_confidence")),
        "n_unweighted": int(float(base.get("n_unweighted"))),
        "n_weighted": _safe_float(base.get("n_weighted")),
        "pct_unweighted": _safe_float(base.get("pct_unweighted")),
        "pct_weighted": _safe_float(base.get("pct_weighted")),
        "weight_status": _clean(base.get("weight_status")),
        "confidence_tier": _confidence_tier(base),
        "support_status": support_status,
        **support_companions,
        "question_type": _clean(base.get("question_type")),
        "handling_rule": _clean(base.get("handling_rule")),
        "recommended_computation": _clean(base.get("recommended_computation")),
        "mapping_status": _clean(base.get("mapping_status")),
        "source_structure_classification": _clean(base.get("source_structure_classification")),
        "source_structure_basis": _clean(base.get("source_structure_basis")),
        "source_structure_confidence": _clean(base.get("source_structure_confidence")),
        "source_structure_source": _clean(base.get("source_structure_source")),
        "source_structure_review_required": _to_bool(base.get("source_structure_review_required"), False),
        "source_structure_fields_joined": _to_bool(base.get("source_structure_fields_joined"), False),
        "semantic_subrole": _clean(base.get("semantic_subrole")),
        "semantic_tags": _clean(base.get("semantic_tags")),
        "directionality_policy": _clean(base.get("directionality_policy")),
        "semantic_confidence": _clean(base.get("semantic_confidence")),
        "semantic_note": _clean(base.get("semantic_note")),
        "position_conditioning": _clean(base.get("position_conditioning")),
        "position_modifiers": _clean(base.get("position_modifiers")),
        "conditional_strata_weights": _clean(base.get("conditional_strata_weights")),
        "horizon_affordance": _clean(base.get("horizon_affordance")),
        "position_conditioning_note": _clean(base.get("position_conditioning_note")),
        "position_conditioning_confidence": _clean(base.get("position_conditioning_confidence")),
        "question_use_contract_joined": _to_bool(base.get("question_use_contract_joined"), False),
        "manual_review_flag": _to_bool(base.get("manual_review_flag"), False) or low_support_review_required,
        "manual_review_reason": "|".join(
            reason
            for reason in [_clean(base.get("manual_review_reason")), "REVIEW_REQUIRED_LOW_SUPPORT" if low_support_review_required else ""]
            if reason
        ),
        "forbidden_inference": _clean(base.get("forbidden_inference")),
        "known_absences": _clean(base.get("known_absences")),
        "allowed_as_v551_relation_evidence": _to_bool(base.get("allowed_as_v551_relation_evidence"), False),
        "allowed_as_temporal_pressure_indicator": _to_bool(base.get("allowed_as_temporal_pressure_indicator"), False),
        "allowed_as_runtime_persona_evidence": _to_bool(base.get("allowed_as_runtime_persona_evidence"), False),
        "evidence_basis": evidence_basis,
        "evidence_basis_origin": evidence_basis_origin,
        "provenance_basis": provenance_basis,
        "provenance_basis_origin": provenance_basis_origin,
        "temporal_authority_status": "NOT_EVALUATED_AT_V551",
        "empirical_observation_class": "single_question_response_category_observation",
        "source_measure_kind": "response_category_distribution",
        "source_measure_status": source_measure_status,
        "directional_measure_kind": directional_measure_kind,
        "response_direction_status": response_direction_status,
        "response_intensity_status": response_intensity_status,
        "observed_response_zero": observed_response_zero,
        "support_measure_role": "evidence_sufficiency_and_sample_support",
        "prevalence_measure_role": "observed_population_distribution_share",
        "support_may_be_used_as_pressure": False,
        "prevalence_may_be_used_as_pressure": False,
        "pressure_evidence_class": pressure_class,
        "v552_pressure_component_eligible": pressure_eligible,
        "v552_pressure_component_status": pressure_status,
        "v552_pressure_component_ineligibility_reason": pressure_reason,
        "n_respondents": _optional_positive_integer(base.get("n_respondents")),
        "source_table": _clean(base.get("source_table")),
        "source_row_hash": _clean(base.get("source_row_hash")),
        "source_run_id": _clean(base.get("run_id") or base.get("source_run_id")),
        "question_use_contract_hash": question_use_contract_hash,
        "source_structure_population_hash": source_structure_population_hash,
        "response_option_map_hash": response_option_map_hash,
        "compiled_at": utc_now(),
        "schema_version": ATOM_SCHEMA_VERSION,
    }
    result["atom_id"] = _atom_id(result)
    result["response_scale_signature"] = _response_scale_signature(result)
    result["semantic_identity_signature"] = _semantic_identity_signature(result)
    result["structural_identity_signature"] = _structural_identity_signature(result)
    result["empirical_distribution_id"] = _empirical_distribution_id(result)
    result["measurement_contract_hash"] = _measurement_contract_hash(result)
    result["atom_contract_hash"] = _atom_contract_hash(result)
    return result


def _numeric_wrapper_audit_row(row: pd.Series, *, run_id: str = "") -> dict[str, Any]:
    audit = numeric_wrapper_audit_from_row(row)
    first = row.to_dict()
    return {
        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
        "source": _clean(first.get("source")),
        "wave": _clean(first.get("wave")),
        "canonical_wave": _clean(first.get("canonical_wave")),
        "country_code": _clean(first.get("country_code")),
        "question_id": _clean(first.get("question_id")),
        "var_code": _clean(first.get("var_code")),
        "source_table": _clean(first.get("source_table")),
        "bridge_evidence_lane": _clean(first.get("bridge_evidence_lane")),
        "semantic_role": _clean(first.get("semantic_role")),
        "evidence_stratum": evidence_stratum_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "evidence_stratum_v2": evidence_stratum_v2_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "response_label": _clean(first.get("response_label")),
        "response_family": _clean(first.get("response_family")),
        "response_value_normalized": _clean(audit.get("response_value_normalized")),
        "numeric_like_label": bool(audit.get("numeric_like_label")),
        "numeric_family_compatible": bool(audit.get("numeric_family_compatible")),
        "numeric_wrapper_status": _clean(audit.get("numeric_wrapper_status")),
        "numeric_wrapper_reason": _clean(audit.get("numeric_wrapper_reason")),
        "numeric_wrapper_confidence": _clean(audit.get("numeric_wrapper_confidence")),
        "support_status": _clean(first.get("support_status")),
        "confidence_tier": _clean(first.get("confidence_tier")),
        "v551_relation_evidence_eligible": _to_bool(first.get("v551_relation_evidence_eligible"), False),
        "v551_exclusion_reason": _clean(first.get("v551_exclusion_reason")),
        "source_row_hash": _clean(first.get("source_row_hash")),
        "n_rows": 1,
        "created_at": utc_now(),
    }


def _review_surface_row(row: pd.Series, *, reason: str, priority: str, run_id: str = "") -> dict[str, Any]:
    first = row.to_dict()
    audit = numeric_wrapper_audit_from_row(row)
    return {
        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
        "source": _clean(first.get("source")),
        "wave": _clean(first.get("wave")),
        "canonical_wave": _clean(first.get("canonical_wave")),
        "country_code": _clean(first.get("country_code")),
        "question_id": _clean(first.get("question_id")),
        "var_code": _clean(first.get("var_code")),
        "source_table": _clean(first.get("source_table")),
        "bridge_evidence_lane": _clean(first.get("bridge_evidence_lane")),
        "semantic_role": _clean(first.get("semantic_role")),
        "evidence_stratum": evidence_stratum_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "evidence_stratum_v2": evidence_stratum_v2_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "review_surface_reason": reason,
        "review_surface_priority": priority,
        "support_status": _clean(first.get("support_status")),
        "confidence_tier": _clean(first.get("confidence_tier")),
        "numeric_wrapper_status": _clean(audit.get("numeric_wrapper_status")),
        "numeric_wrapper_reason": _clean(audit.get("numeric_wrapper_reason")),
        "numeric_wrapper_confidence": _clean(audit.get("numeric_wrapper_confidence")),
        "v551_relation_evidence_eligible": _to_bool(first.get("v551_relation_evidence_eligible"), False),
        "v551_exclusion_reason": _clean(first.get("v551_exclusion_reason")),
        "source_row_hash": _clean(first.get("source_row_hash")),
        "n_rows": 1,
        "created_at": utc_now(),
    }


def _blocked_signal_row(row: pd.Series, *, run_id: str = "") -> dict[str, Any]:
    first = row.to_dict()
    audit = numeric_wrapper_audit_from_row(row)
    reason = _clean(first.get("v551_exclusion_reason")) or _clean(first.get("exclusion_reason"))
    if not reason:
        reason = _clean(audit.get("numeric_wrapper_reason")) or "blocked_for_review"
    priority = "high" if reason in {"missing_bridge_evidence_lane", "missing_bridge_relation_eligibility_field", "numeric_only_label_requires_numeric_scale_family"} else "medium"
    return {
        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
        "source": _clean(first.get("source")),
        "wave": _clean(first.get("wave")),
        "canonical_wave": _clean(first.get("canonical_wave")),
        "country_code": _clean(first.get("country_code")),
        "question_id": _clean(first.get("question_id")),
        "var_code": _clean(first.get("var_code")),
        "source_table": _clean(first.get("source_table")),
        "bridge_evidence_lane": _clean(first.get("bridge_evidence_lane")),
        "semantic_role": _clean(first.get("semantic_role")),
        "evidence_stratum": evidence_stratum_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "evidence_stratum_v2": evidence_stratum_v2_from_row(
            bridge_evidence_lane=first.get("bridge_evidence_lane", ""),
            semantic_role=first.get("semantic_role", ""),
            v551_relation_evidence_eligible=first.get("v551_relation_evidence_eligible"),
        ),
        "gate_name": _clean(first.get("gate_name")) or _clean(first.get("exclusion_reason")) or "v551_blocked",
        "blocked_signal_reason": reason,
        "blocked_signal_priority": priority,
        "support_status": _clean(first.get("support_status")) or _clean(audit.get("numeric_wrapper_status")),
        "confidence_tier": _clean(first.get("confidence_tier")),
        "blocked_row_count": int(float(first.get("n_rows") or 1)),
        "sample_source_row_hash": _clean(first.get("sample_source_row_hash") or first.get("source_row_hash")),
        "created_at": utc_now(),
    }


def _exclusion_row(row: pd.Series, gate_name: str, exclusion_reason: str) -> dict[str, Any]:
    return {
        "source": _clean(row.get("source")),
        "canonical_wave": _clean(row.get("canonical_wave")),
        "country_code": _clean(row.get("country_code")),
        "question_id": _clean(row.get("question_id")),
        "var_code": _clean(row.get("var_code")),
        "source_table": _clean(row.get("source_table")),
        "gate_name": gate_name,
        "exclusion_reason": exclusion_reason,
        "n_rows": 1,
        "sample_source_row_hash": _clean(row.get("source_row_hash")),
    }


def _row_contract_missing_reason(row: pd.Series) -> tuple[str, str] | None:
    required_values = [
        ("run_id", "missing_run_id"),
        ("shard_id", "missing_shard_id"),
        ("source", "missing_source"),
        ("canonical_wave", "missing_canonical_wave"),
        ("country_code", "missing_country_code"),
        ("empirical_object_type", "missing_empirical_object_type"),
        ("empirical_object_id", "missing_empirical_object_id"),
        ("source_table", "missing_source_table"),
        ("response_value_normalized", "missing_response_value_normalized"),
        ("response_family", "missing_response_family"),
        ("bridge_evidence_lane", "missing_bridge_evidence_lane"),
        ("semantic_role", "missing_semantic_role"),
        ("relation_axis_id", "missing_relation_axis_id"),
        ("target_entity_id", "missing_target_entity_id"),
        ("driver_id", "missing_driver_id"),
        ("driver_facet_id", "missing_driver_facet_id"),
        ("response_semantics_source", "missing_response_semantics_source"),
        ("response_semantics_contract_hash", "missing_response_semantics_contract_hash"),
        ("source_structure_basis", "missing_source_structure_basis"),
        ("source_structure_confidence", "missing_source_structure_confidence"),
        ("source_structure_source", "missing_source_structure_source"),
    ]
    if not _clean(row.get("question_id")) and not _clean(row.get("var_code")):
        return "v551_contract_completeness", "missing_question_id_or_var_code"
    for field, reason in required_values:
        if not _clean(row.get(field)):
            return "v551_contract_completeness", reason
    return None


def build_v551_relation_evidence_atoms(
    bridge: pd.DataFrame,
    *,
    question_use_contract: pd.DataFrame | None = None,
    source_structure_population_audit: pd.DataFrame | None = None,
    response_option_map_hash: str = "",
    question_use_contract_hash: str = "",
    source_structure_population_hash: str = "",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if bridge.empty:
        return (
            pd.DataFrame(columns=V551_RELATION_EVIDENCE_ATOMS_SCHEMA["required_columns"]),
            pd.DataFrame(columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"]),
        )
    contract = validate_v551_bridge_input_contract(bridge)
    if contract["status"] != "PASS":
        raise ValueError("BLOCKED_V551_MISSING_BRIDGE_CONTRACT: " + ", ".join(contract["missing_columns"]))

    bridge = bridge.copy()
    if "future_topology_evidence_eligible" not in bridge.columns:
        bridge["future_topology_evidence_eligible"] = bridge.get(
            "future_evidence_eligible",
            pd.Series([False] * len(bridge), index=bridge.index),
        ).map(lambda value: _to_bool(value, False))
    if "current_directional_atom_eligible" not in bridge.columns:
        bridge["current_directional_atom_eligible"] = pd.Series([False] * len(bridge), index=bridge.index)
    if "directional_certification_status" not in bridge.columns:
        bridge["directional_certification_status"] = pd.Series(["NOT_CERTIFIED"] * len(bridge), index=bridge.index)

    if "v551_eligible" not in bridge.columns:
        bridge["v551_eligible"] = bridge.get(
            "v551_relation_evidence_eligible",
            pd.Series([False] * len(bridge), index=bridge.index),
        ).map(lambda value: _to_bool(value, False))

    atoms: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    seen_atom_keys: set[str] = set()

    prioritized = bridge.copy()
    prioritized["_source_table_priority"] = prioritized.get("source_table", pd.Series([""] * len(prioritized), index=prioritized.index)).map(lambda value: SOURCE_TABLE_PRIORITY.get(_clean(value), 99))
    prioritized = prioritized.sort_values(["_source_table_priority", "source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"], kind="mergesort").reset_index(drop=True)

    for row in prioritized.itertuples(index=False):
        series = pd.Series(row._asdict())
        if "support_status" not in series.index:
            exclusions.append(_exclusion_row(series, "support_status", "missing_support_status"))
            continue
        support_status = _clean(series.get("support_status"))
        if support_status in {"missing_support", "not_applicable"}:
            exclusions.append(_exclusion_row(series, "support_status", f"{support_status or 'missing_support'}_not_sufficient"))
            continue
        current_directional_atom_eligible = _to_bool(series.get("current_directional_atom_eligible"), False)
        directional_certification_status = _directional_certification_status(series.get("directional_certification_status"))
        if not current_directional_atom_eligible or directional_certification_status != "CERTIFIED":
            exclusions.append(_exclusion_row(series, "directional_certification_status", directional_certification_status.lower() or "not_certified"))
            continue
        if not _has_certified_directional_response(series):
            reason = "BLOCKED_UNRESOLVED_AUTHORITY_TOKEN" if _has_any_directionality_value(series) else "missing_certified_directional_response"
            exclusions.append(_exclusion_row(series, "directional_response", reason))
            continue
        if _clean(series.get("semantic_role_authority_status")).upper() != "CERTIFIED":
            exclusions.append(_exclusion_row(series, "semantic_role_authority", "semantic_role_authority_not_certified"))
            continue
        directionality_authority_status = _clean(
            series.get("directionality_authority_status")
        ).upper()
        if directionality_authority_status != "CERTIFIED":
            exclusions.append(_exclusion_row(series, "directionality_authority", "directionality_authority_not_certified"))
            continue
        if _clean(series.get("structural_mapping_status")).upper() != "COMPLETE":
            exclusions.append(_exclusion_row(series, "structural_mapping", "structural_mapping_not_complete"))
            continue
        bridge_eligible = _to_bool(series.get("v551_relation_evidence_eligible"), False)
        if not bridge_eligible:
            exclusions.append(_exclusion_row(series, "v551_eligibility", _clean(series.get("v551_exclusion_reason")) or "not_v551_eligible"))
            continue
        if _clean(series.get("bridge_evidence_lane")) != "direct_relation_response":
            exclusions.append(_exclusion_row(series, "bridge_evidence_lane", "not_direct_relation_response_lane"))
            continue
        if "question_use_contract_joined" not in series.index:
            exclusions.append(_exclusion_row(series, "question_use_contract", "missing_question_use_contract_joined"))
            continue
        if not _allowed_source_table(series.get("source_table")):
            exclusions.append(_exclusion_row(series, "source_table_priority", "unsupported_source_table"))
            continue
        if not _to_bool(series.get("question_use_contract_joined"), False):
            exclusions.append(_exclusion_row(series, "question_use_contract", "question_use_contract_not_joined"))
            continue
        if "response_semantics_status" not in series.index:
            exclusions.append(_exclusion_row(series, "response_semantics", "missing_response_semantics_status"))
            continue
        response_semantics_status = _clean(series.get("response_semantics_status")).lower()
        if response_semantics_status not in CERTIFIED_RESPONSE_SEMANTICS_STATUSES:
            exclusions.append(_exclusion_row(series, "response_semantics", "non_curated_response_semantics"))
            continue
        if "response_semantics_source" not in series.index:
            exclusions.append(_exclusion_row(series, "response_semantics", "missing_response_semantics_source"))
            continue
        if not _clean(series.get("response_semantics_source")):
            exclusions.append(_exclusion_row(series, "response_semantics", "missing_response_semantics_source"))
            continue
        if "response_semantics_contract_hash" not in series.index:
            exclusions.append(_exclusion_row(series, "response_semantics", "missing_response_semantics_contract_hash"))
            continue
        if not _clean(series.get("response_semantics_contract_hash")):
            exclusions.append(_exclusion_row(series, "response_semantics", "missing_response_semantics_contract_hash"))
            continue
        if "source_structure_fields_joined" not in series.index:
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_fields_joined"))
            continue
        if not _to_bool(series.get("source_structure_fields_joined"), False):
            exclusions.append(_exclusion_row(series, "source_structure_fields", "source_structure_fields_not_joined"))
            continue
        if "source_structure_source" not in series.index:
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_source"))
            continue
        if not _clean(series.get("source_structure_source")):
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_source"))
            continue
        if "source_structure_basis" not in series.index:
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_basis"))
            continue
        if not _clean(series.get("source_structure_basis")):
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_basis"))
            continue
        if "source_structure_confidence" not in series.index:
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_confidence"))
            continue
        if not _clean(series.get("source_structure_confidence")):
            exclusions.append(_exclusion_row(series, "source_structure_fields", "missing_source_structure_confidence"))
            continue
        if "response_option_map_matched" not in series.index:
            exclusions.append(_exclusion_row(series, "response_option_map", "missing_response_option_map_matched"))
            continue
        if not _to_bool(series.get("response_option_map_matched"), False):
            exclusions.append(_exclusion_row(series, "response_option_map", "response_option_map_unmatched_not_relation_evidence"))
            continue
        if _clean(series.get("semantic_role")) != "RELATION_EVIDENCE":
            exclusions.append(_exclusion_row(series, "semantic_role", "non_relation_semantic_role"))
            continue
        if not _to_bool(series.get("is_substantive"), False):
            exclusions.append(_exclusion_row(series, "response_state", "non_substantive_response"))
            continue
        if _to_bool(series.get("is_missing"), False):
            exclusions.append(_exclusion_row(series, "response_state", "missing_response_not_relation_evidence"))
            continue
        if _to_bool(series.get("is_special"), False):
            exclusions.append(_exclusion_row(series, "response_state", "special_response_not_relation_evidence"))
            continue
        if not _to_bool(series.get("allowed_as_v551_relation_evidence"), False):
            exclusions.append(_exclusion_row(series, "allowed_as_v551_relation_evidence", "question_use_contract_disallows_v551_relation_evidence"))
            continue
        if not _to_bool(series.get("usable_for_evidence"), False):
            exclusions.append(_exclusion_row(series, "usable_for_evidence", "not_usable_for_evidence"))
            continue
        if _clean(series.get("empirical_object_type")) not in APPROVED_EMPIRICAL_OBJECT_TYPES:
            exclusions.append(_exclusion_row(series, "empirical_object_type", "unsupported_empirical_object_type"))
            continue
        if _clean(series.get("source_table")) not in APPROVED_DIRECT_RELATION_SOURCE_TABLES:
            exclusions.append(_exclusion_row(series, "source_table", "unsupported_direct_relation_source_table"))
            continue
        row_contract_issue = _row_contract_missing_reason(series)
        if row_contract_issue is not None:
            exclusions.append(_exclusion_row(series, row_contract_issue[0], row_contract_issue[1]))
            continue
        try:
            _derive_evidence_basis(series.to_dict())
        except ValueError:
            exclusions.append(_exclusion_row(series, "v551_contract_completeness", "missing_evidence_basis_derivation_input"))
            continue
        try:
            _derive_provenance_basis(series.to_dict())
        except ValueError:
            exclusions.append(_exclusion_row(series, "v551_contract_completeness", "missing_provenance_basis_derivation_input"))
            continue
        if _is_numeric_only_label(series.get("response_label")):
            if not _response_family_allows_numeric_only_label(series.get("response_family")):
                exclusions.append(_exclusion_row(series, "numeric_label", "numeric_only_label_requires_numeric_scale_family"))
                continue
            if not _has_certified_directional_response(series):
                exclusions.append(_exclusion_row(series, "numeric_label", "numeric_only_label_requires_directionality"))
                continue
        if "normalization_confidence" not in series.index or not _clean(series.get("normalization_confidence")):
            exclusions.append(_exclusion_row(series, "normalization_confidence", "missing_normalization_confidence"))
            continue
        support_status = _clean(series.get("support_status"))
        support_value: float
        if "n_unweighted" not in series.index or _safe_float(series.get("n_unweighted")) is None:
            exclusions.append(_exclusion_row(series, "support", "missing_support_count"))
            continue
        else:
            try:
                support_value = float(series.get("n_unweighted") or 0)
            except Exception:
                support_value = 0.0
        support_threshold = support_threshold_from_total(series.get("n_respondents"), support_cap=MIN_ATOM_SUPPORT)
        canonical_key = _canonical_empirical_key(series)
        if canonical_key in seen_atom_keys:
            exclusions.append(_exclusion_row(series, "atom_dedupe", "duplicate_empirical_answer"))
            continue
        seen_atom_keys.add(canonical_key)
        atom = _atom_row(
            series,
            question_use_contract_hash=question_use_contract_hash,
            source_structure_population_hash=source_structure_population_hash,
            response_option_map_hash=response_option_map_hash,
        )
        atom_id = atom["atom_id"]
        atoms.append(atom)

    atom_df = pd.DataFrame(atoms, columns=V551_RELATION_EVIDENCE_ATOMS_SCHEMA["required_columns"])
    exclusion_df = pd.DataFrame(exclusions, columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"])
    if not atom_df.empty:
        atom_df = atom_df.sort_values(["source", "canonical_wave", "country_code", "question_id", "var_code", "atom_id"], kind="mergesort").reset_index(drop=True)
    return atom_df, exclusion_df


def build_v551_numeric_wrapper_audit(bridge: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    if bridge.empty:
        return pd.DataFrame(columns=V551_NUMERIC_WRAPPER_AUDIT_SCHEMA["required_columns"])
    rows = [_numeric_wrapper_audit_row(row if isinstance(row, pd.Series) else pd.Series(row._asdict()), run_id=run_id) for row in bridge.itertuples(index=False)]
    frame = pd.DataFrame(rows, columns=V551_NUMERIC_WRAPPER_AUDIT_SCHEMA["required_columns"])
    if not frame.empty:
        frame = frame.sort_values(["source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"], kind="mergesort").reset_index(drop=True)
    return frame


def build_v551_relation_review_surface(bridge: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    if bridge.empty:
        return pd.DataFrame(columns=V551_RELATION_REVIEW_SURFACE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for row in bridge.itertuples(index=False):
        series = row if isinstance(row, pd.Series) else pd.Series(row._asdict())
        audit = numeric_wrapper_audit_from_row(series)
        eligible = _to_bool(series.get("v551_relation_evidence_eligible"), False)
        lane = _clean(series.get("bridge_evidence_lane"))
        wrapper_status = _clean(audit.get("numeric_wrapper_status"))
        support_status = _clean(series.get("support_status"))
        exclusion_reason = _clean(series.get("v551_exclusion_reason"))
        reason = ""
        priority = "low"
        if wrapper_status == "blocked_numeric_wrapper":
            reason = _clean(audit.get("numeric_wrapper_reason")) or "numeric_only_label_requires_numeric_scale_family"
            priority = "high"
        elif lane != "direct_relation_response":
            reason = exclusion_reason or "lane_not_certifiable_as_relation_evidence"
            priority = "high" if lane in {"derived_determinicity", "position_context", "structural_context"} else "medium"
        elif not eligible:
            reason = exclusion_reason or "not_v551_eligible"
            priority = "medium"
        elif support_status != "sufficient_support":
            reason = exclusion_reason or "support_status_not_sufficient"
            priority = "medium"
        if not reason:
            continue
        rows.append(_review_surface_row(series, reason=reason, priority=priority, run_id=run_id))
    frame = pd.DataFrame(rows, columns=V551_RELATION_REVIEW_SURFACE_SCHEMA["required_columns"])
    if not frame.empty:
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        frame["_review_surface_priority_rank"] = frame["review_surface_priority"].map(priority_rank).fillna(99)
        frame = frame.sort_values(["_review_surface_priority_rank", "source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"], ascending=[True, True, True, True, True, True, True], kind="mergesort").drop(columns=["_review_surface_priority_rank"]).reset_index(drop=True)
    return frame


def build_v551_blocked_signal_audit(bridge: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    if bridge.empty:
        return pd.DataFrame(columns=V551_BLOCKED_SIGNAL_AUDIT_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for row in bridge.itertuples(index=False):
        series = row if isinstance(row, pd.Series) else pd.Series(row._asdict())
        audit = numeric_wrapper_audit_from_row(series)
        if _clean(series.get("bridge_evidence_lane")) == "direct_relation_response" and _to_bool(series.get("v551_relation_evidence_eligible"), False) and _clean(series.get("v551_exclusion_reason")) in {"", "none", "nan"} and _clean(audit.get("numeric_wrapper_status")) != "blocked_numeric_wrapper":
            continue
        rows.append(_blocked_signal_row(series, run_id=run_id))
    frame = pd.DataFrame(rows, columns=V551_BLOCKED_SIGNAL_AUDIT_SCHEMA["required_columns"])
    if frame.empty:
        return frame
    group_cols = [column for column in ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code", "source_table", "bridge_evidence_lane", "semantic_role", "evidence_stratum", "evidence_stratum_v2", "gate_name", "blocked_signal_reason", "blocked_signal_priority", "support_status", "confidence_tier"] if column in frame.columns]
    agg = (
        frame.groupby(group_cols, dropna=False, sort=True)
        .agg(blocked_row_count=("blocked_row_count", "sum"), sample_source_row_hash=("sample_source_row_hash", "first"), run_id=("run_id", "first"), created_at=("created_at", "first"))
        .reset_index()
    )
    return agg.loc[:, V551_BLOCKED_SIGNAL_AUDIT_SCHEMA["required_columns"]]


def build_v551_certification_candidate_bridge(bridge: pd.DataFrame) -> pd.DataFrame:
    if bridge.empty:
        return bridge.copy()
    frame = bridge.copy()
    required = [
        "v551_relation_evidence_eligible",
        "bridge_evidence_lane",
        "source_table",
        "question_use_contract_joined",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "source_structure_fields_joined",
        "source_structure_source",
        "source_structure_basis",
        "source_structure_confidence",
        "response_option_map_matched",
        "semantic_role",
        "semantic_role_authority_status",
        "directionality_authority_status",
        "structural_mapping_status",
        "support_status",
        "n_unweighted",
        "n_respondents",
    ]
    missing = [column for column in required + V551_REQUIRED_BRIDGE_CONTRACT_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError("BLOCKED_V551_MISSING_BRIDGE_CONTRACT: " + ", ".join(sorted(set(missing))))
    support_n = pd.to_numeric(frame.get("n_unweighted", pd.Series(-1, index=frame.index)), errors="coerce").fillna(-1)
    mask = (
        frame["v551_relation_evidence_eligible"].map(lambda value: _to_bool(value, False))
        & frame["bridge_evidence_lane"].astype(str).eq("direct_relation_response")
        & frame["source_table"].map(_allowed_source_table)
        & frame["question_use_contract_joined"].map(lambda value: _to_bool(value, False))
        & frame["response_semantics_status"].astype(str).str.lower().isin(CERTIFIED_RESPONSE_SEMANTICS_STATUSES)
        & frame["response_semantics_source"].astype(str).str.strip().ne("")
        & frame["response_semantics_contract_hash"].astype(str).str.strip().ne("")
        & frame["source_structure_fields_joined"].map(lambda value: _to_bool(value, False))
        & frame["source_structure_source"].astype(str).str.strip().ne("")
        & frame["source_structure_basis"].astype(str).str.strip().ne("")
        & frame["source_structure_confidence"].astype(str).str.strip().ne("")
        & frame["response_option_map_matched"].map(lambda value: _to_bool(value, False))
        & frame["semantic_role"].astype(str).eq("RELATION_EVIDENCE")
        & frame.get("is_substantive", pd.Series(False, index=frame.index)).map(lambda value: _to_bool(value, False))
        & ~frame.get("is_missing", pd.Series(False, index=frame.index)).map(lambda value: _to_bool(value, False))
        & ~frame.get("is_special", pd.Series(False, index=frame.index)).map(lambda value: _to_bool(value, False))
        & frame.get("usable_for_evidence", pd.Series(False, index=frame.index)).map(lambda value: _to_bool(value, False))
        & frame["semantic_role_authority_status"].astype(str).str.upper().eq("CERTIFIED")
        & frame["directionality_authority_status"].astype(str).str.upper().eq("CERTIFIED")
        & frame["structural_mapping_status"].astype(str).str.upper().eq("COMPLETE")
        & frame["support_status"].astype(str).ne("missing_support")
        & frame["support_status"].astype(str).ne("not_applicable")
        & support_n.ge(0)
    )
    candidate = frame.loc[mask].copy()
    if not candidate.empty:
        candidate = candidate.reset_index(drop=True)
    return candidate


def build_v551_exclusion_summary(exclusion_audit: pd.DataFrame) -> pd.DataFrame:
    if exclusion_audit.empty:
        return exclusion_audit.copy()
    group_cols = [
        column
        for column in [
            "source",
            "wave",
            "canonical_wave",
            "country_code",
            "question_id",
            "var_code",
            "source_table",
            "bridge_evidence_lane",
            "semantic_role",
            "gate_name",
            "exclusion_reason",
            "support_status",
            "confidence_tier",
        ]
        if column in exclusion_audit.columns
    ]
    if not group_cols:
        return exclusion_audit.copy()
    summary = exclusion_audit.groupby(group_cols, dropna=False, sort=True).size().reset_index(name="excluded_row_count")
    return summary


def build_v551_exclusion_samples(exclusion_audit: pd.DataFrame, *, sample_size: int = 3) -> pd.DataFrame:
    if exclusion_audit.empty:
        return exclusion_audit.copy()
    group_cols = [column for column in ["exclusion_reason", "source_table", "bridge_evidence_lane"] if column in exclusion_audit.columns]
    if not group_cols:
        return exclusion_audit.head(sample_size).copy()
    sampled = exclusion_audit.sort_values(group_cols + [column for column in ["source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"] if column in exclusion_audit.columns], kind="mergesort")
    sampled = sampled.groupby(group_cols, dropna=False, sort=True).head(sample_size).reset_index(drop=True)
    return sampled


def build_v551_pressure_component_audit(atoms: pd.DataFrame) -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V551_PRESSURE_COMPONENT_AUDIT_SCHEMA["required_columns"])
    frame = atoms.loc[:, [column for column in V551_PRESSURE_COMPONENT_AUDIT_SCHEMA["required_columns"] if column in atoms.columns]].copy()
    return frame.reindex(columns=V551_PRESSURE_COMPONENT_AUDIT_SCHEMA["required_columns"])


def _clean_unique_count(series: pd.Series) -> int:
    return int(series.map(_clean).nunique(dropna=False))


def _ambiguous_response_category_group(group: pd.DataFrame) -> bool:
    if "response_value_normalized" not in group.columns:
        return False
    exact_duplicate_fields = [
        "atom_contract_hash",
        "measurement_contract_hash",
        "empirical_object_id",
        "n_unweighted",
        "n_respondents",
        "n_weighted",
        "pct_unweighted",
        "pct_weighted",
        "response_direction",
        "response_intensity",
        "response_label",
        "normalized_response_label",
        "response_semantics_contract_hash",
    ]
    for _, response_group in group.groupby(group["response_value_normalized"].map(_clean), dropna=False, sort=True):
        if len(response_group) <= 1:
            continue
        for column in exact_duplicate_fields:
            if column in response_group.columns and _clean_unique_count(response_group[column]) > 1:
                return True
    return False


def summarize_v551_denominator_contract(atoms: pd.DataFrame) -> dict[str, Any]:
    base = {
        "empirical_distribution_id_column_present": "empirical_distribution_id" in atoms.columns,
        "atom_count": int(len(atoms)),
        "empirical_distribution_count": 0,
        "distribution_count_by_wave": {},
        "distribution_atom_count_min": 0,
        "distribution_atom_count_max": 0,
        "distribution_atom_count_mean": 0.0,
        "complete_selected_category_coverage_count": 0,
        "partial_selected_category_coverage_count": 0,
        "missing_denominator_distribution_count": 0,
        "inconsistent_denominator_distribution_count": 0,
        "category_count_exceeds_denominator_distribution_count": 0,
        "ambiguous_response_category_distribution_count": 0,
        "n_respondents_column_present": "n_respondents" in atoms.columns,
        "n_respondents_nonnull_atom_count": 0,
        "n_respondents_null_atom_count": int(len(atoms)),
        "empirical_object_groups_with_denominator": 0,
        "empirical_object_groups_without_denominator": 0,
        "inconsistent_denominator_group_count": 0,
        "category_count_exceeds_denominator_group_count": 0,
    }
    if atoms.empty or "n_respondents" not in atoms.columns:
        return base
    denom = pd.to_numeric(atoms["n_respondents"], errors="coerce")
    base["n_respondents_nonnull_atom_count"] = int(denom.notna().sum())
    base["n_respondents_null_atom_count"] = int(denom.isna().sum())
    group_cols = V551_EMPIRICAL_DISTRIBUTION_GROUP_COLUMNS
    if not all(column in atoms.columns for column in group_cols):
        return base
    group_sizes = atoms.groupby(group_cols, dropna=False, sort=True).size()
    base["empirical_distribution_count"] = int(len(group_sizes))
    if len(group_sizes):
        base["distribution_atom_count_min"] = int(group_sizes.min())
        base["distribution_atom_count_max"] = int(group_sizes.max())
        base["distribution_atom_count_mean"] = float(group_sizes.mean())
    if {"canonical_wave", "empirical_distribution_id"}.issubset(atoms.columns):
        base["distribution_count_by_wave"] = {
            str(wave): int(group["empirical_distribution_id"].fillna("").astype(str).nunique())
            for wave, group in atoms.groupby("canonical_wave", dropna=False, sort=True)
        }
    with_denom = without_denom = inconsistent = exceeds = ambiguous = complete = partial = 0
    for _, group in atoms.groupby(group_cols, dropna=False, sort=True):
        group_denom = pd.to_numeric(group["n_respondents"], errors="coerce").dropna()
        distinct = sorted(set(float(value) for value in group_denom.tolist()))
        if _ambiguous_response_category_group(group):
            ambiguous += 1
        if distinct:
            with_denom += 1
        else:
            without_denom += 1
            continue
        if len(distinct) > 1:
            inconsistent += 1
            continue
        n_resp = distinct[0]
        sum_n = pd.to_numeric(group.get("n_unweighted", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()
        if sum_n > n_resp:
            exceeds += 1
        elif sum_n == n_resp:
            complete += 1
        elif sum_n < n_resp:
            partial += 1
    base["missing_denominator_distribution_count"] = int(without_denom)
    base["inconsistent_denominator_distribution_count"] = int(inconsistent)
    base["category_count_exceeds_denominator_distribution_count"] = int(exceeds)
    base["ambiguous_response_category_distribution_count"] = int(ambiguous)
    base["complete_selected_category_coverage_count"] = int(complete)
    base["partial_selected_category_coverage_count"] = int(partial)
    base["empirical_object_groups_with_denominator"] = int(with_denom)
    base["empirical_object_groups_without_denominator"] = int(without_denom)
    base["inconsistent_denominator_group_count"] = int(inconsistent)
    base["category_count_exceeds_denominator_group_count"] = int(exceeds)
    return base


def build_v551_lineage_basis_audit(candidate_bridge: pd.DataFrame, atoms: pd.DataFrame, exclusion_audit: pd.DataFrame) -> pd.DataFrame:
    if candidate_bridge.empty:
        return pd.DataFrame(columns=V551_LINEAGE_BASIS_AUDIT_SCHEMA["required_columns"])
    emitted_hashes = set(atoms.get("source_row_hash", pd.Series(dtype=str)).fillna("").astype(str).tolist())
    distribution_by_hash = {}
    if {"source_row_hash", "empirical_distribution_id"}.issubset(atoms.columns):
        distribution_by_hash = {
            _clean(row.get("source_row_hash")): _clean(row.get("empirical_distribution_id"))
            for row in atoms.to_dict("records")
        }
    failure_by_hash = {}
    if not exclusion_audit.empty and {"sample_source_row_hash", "exclusion_reason"}.issubset(exclusion_audit.columns):
        for row in exclusion_audit.itertuples(index=False):
            reason = _clean(getattr(row, "exclusion_reason", ""))
            if reason in {"missing_evidence_basis_derivation_input", "missing_provenance_basis_derivation_input"}:
                failure_by_hash[_clean(getattr(row, "sample_source_row_hash", ""))] = reason
    rows: list[dict[str, Any]] = []
    for row in candidate_bridge.itertuples(index=False):
        series = pd.Series(row._asdict())
        base = series.to_dict()
        source_row_hash = _clean(base.get("source_row_hash"))
        source_evidence = bool(_clean(base.get("evidence_basis")))
        source_provenance = bool(_clean(base.get("provenance_basis")))
        evidence_origin = ""
        provenance_origin = ""
        evidence_status = "NOT_EMITTED_OTHER_GATE"
        provenance_status = "NOT_EMITTED_OTHER_GATE"
        failure_reason = failure_by_hash.get(source_row_hash, "")
        if source_row_hash in emitted_hashes:
            try:
                _, evidence_origin = _derive_evidence_basis(base)
                evidence_status = "SOURCE_PROVIDED" if evidence_origin == "SOURCE_PROVIDED" else "DERIVED"
            except ValueError:
                evidence_status = "FAILED"
                failure_reason = "missing_evidence_basis_derivation_input"
            try:
                _, provenance_origin = _derive_provenance_basis(base)
                provenance_status = "SOURCE_PROVIDED" if provenance_origin == "SOURCE_PROVIDED" else "DERIVED"
            except ValueError:
                provenance_status = "FAILED"
                failure_reason = "missing_provenance_basis_derivation_input"
        elif failure_reason == "missing_evidence_basis_derivation_input":
            evidence_status = "FAILED"
        elif failure_reason == "missing_provenance_basis_derivation_input":
            provenance_status = "FAILED"
        rows.append({
            "run_id": _clean(base.get("run_id")),
            "source": _clean(base.get("source")),
            "canonical_wave": _clean(base.get("canonical_wave")),
            "country_code": _clean(base.get("country_code")),
            "question_id": _clean(base.get("question_id")),
            "var_code": _clean(base.get("var_code")),
            "empirical_object_id": _clean(base.get("empirical_object_id")),
            "empirical_distribution_id": distribution_by_hash.get(source_row_hash, ""),
            "source_row_hash": source_row_hash,
            "source_evidence_basis_nonblank": source_evidence,
            "source_provenance_basis_nonblank": source_provenance,
            "evidence_basis_origin": evidence_origin,
            "provenance_basis_origin": provenance_origin,
            "evidence_basis_derivation_status": evidence_status,
            "provenance_basis_derivation_status": provenance_status,
            "derivation_failure_reason": failure_reason,
        })
    return pd.DataFrame(rows).reindex(columns=V551_LINEAGE_BASIS_AUDIT_SCHEMA["required_columns"])


ELIGIBLE_BRIDGE_ATOM_COVERAGE_AUDIT_COLUMNS = [
    "source",
    "canonical_wave",
    "country_code",
    "question_id",
    "var_code",
    "response_value_normalized",
    "response_label",
    "response_direction",
    "response_intensity",
    "source_row_hash",
    "coverage_status",
    "emitted_atom_id",
    "exclusion_reason",
    "coverage_blocker",
]


def build_v551_eligible_bridge_atom_coverage_audit(
    candidate_bridge: pd.DataFrame,
    atoms: pd.DataFrame,
    exclusion_audit: pd.DataFrame,
) -> pd.DataFrame:
    if candidate_bridge.empty:
        return pd.DataFrame(columns=ELIGIBLE_BRIDGE_ATOM_COVERAGE_AUDIT_COLUMNS)
    def category_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return (
            _clean(row.get("source")),
            _clean(row.get("canonical_wave")),
            _clean(row.get("country_code")),
            _clean(row.get("question_id")),
            _clean(row.get("var_code")),
            _clean(row.get("response_value_normalized")),
            _clean(row.get("relation_axis_id")),
            _clean(row.get("target_entity_id")),
            _clean(row.get("driver_id")),
            _clean(row.get("driver_facet_id")),
        )

    atom_by_key: dict[tuple[str, ...], str] = {}
    if {"atom_id", "source", "canonical_wave", "country_code", "question_id", "var_code", "response_value_normalized"}.issubset(atoms.columns):
        atom_by_key = {
            category_key(row): _clean(row.get("atom_id"))
            for row in atoms.to_dict("records")
            if _clean(row.get("atom_id"))
        }
    exclusion_by_hash: dict[str, str] = {}
    if {"sample_source_row_hash", "exclusion_reason"}.issubset(exclusion_audit.columns):
        for row in exclusion_audit.to_dict("records"):
            source_row_hash = _clean(row.get("sample_source_row_hash"))
            if source_row_hash and source_row_hash not in exclusion_by_hash:
                exclusion_by_hash[source_row_hash] = _clean(row.get("exclusion_reason"))
    rows: list[dict[str, Any]] = []
    for row in candidate_bridge.to_dict("records"):
        source_row_hash = _clean(row.get("source_row_hash"))
        atom_id = atom_by_key.get(category_key(row), "")
        emitted = bool(atom_id)
        rows.append(
            {
                "source": _clean(row.get("source")),
                "canonical_wave": _clean(row.get("canonical_wave")),
                "country_code": _clean(row.get("country_code")),
                "question_id": _clean(row.get("question_id")),
                "var_code": _clean(row.get("var_code")),
                "response_value_normalized": _clean(row.get("response_value_normalized")),
                "response_label": _clean(row.get("response_label")),
                "response_direction": _clean(row.get("response_direction")),
                "response_intensity": row.get("response_intensity"),
                "source_row_hash": source_row_hash,
                "coverage_status": "EMITTED_V551_ATOM" if emitted else "MISSING_V551_ATOM",
                "emitted_atom_id": atom_id,
                "exclusion_reason": "" if emitted else exclusion_by_hash.get(source_row_hash, ""),
                "coverage_blocker": not emitted,
            }
        )
    frame = pd.DataFrame(rows, columns=ELIGIBLE_BRIDGE_ATOM_COVERAGE_AUDIT_COLUMNS)
    return frame.sort_values(
        ["coverage_blocker", "source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"],
        ascending=[False, True, True, True, True, True, True],
        kind="mergesort",
    ).reset_index(drop=True)


def validate_v551_atom_contract(df: pd.DataFrame) -> list[str]:
    issues = validate_columns(df, V551_RELATION_EVIDENCE_ATOMS_SCHEMA["required_columns"], "v551_relation_evidence_atoms")
    if df.empty:
        return issues
    pressure_columns = {"pressure_score", "pressure_value", "field_pressure_score", "projection_score", "constraint_signal_score", "structural_pressure_value"}
    present_pressure_columns = sorted(pressure_columns.intersection(df.columns))
    if present_pressure_columns:
        issues.append("forbidden_pressure_value_columns_present=" + ",".join(present_pressure_columns))
    required_nonblank = [
        "atom_id",
        "empirical_distribution_id",
        "atom_contract_hash",
        "response_scale_signature",
        "semantic_identity_signature",
        "structural_identity_signature",
        "measurement_contract_hash",
        "semantic_role_authority_status",
        "response_semantics_authority_status",
        "directionality_authority_status",
        "structural_mapping_status",
        "evidence_basis",
        "evidence_basis_origin",
        "provenance_basis",
        "provenance_basis_origin",
        "temporal_authority_status",
    ]
    for column in required_nonblank:
        if column in df.columns and df[column].fillna("").astype(str).str.strip().eq("").any():
            issues.append(f"blank_required_contract_column={column}")
    if "empirical_object_type" in df.columns and ~df["empirical_object_type"].isin(APPROVED_EMPIRICAL_OBJECT_TYPES).all():
        issues.append("invalid_empirical_object_type")
    if "empirical_observation_class" in df.columns and ~df["empirical_observation_class"].eq("single_question_response_category_observation").all():
        issues.append("invalid_empirical_observation_class")
    if "evidence_basis_origin" in df.columns and ~df["evidence_basis_origin"].isin({"SOURCE_PROVIDED", "DERIVED_FROM_ACCEPTED_V550_BRIDGE"}).all():
        issues.append("invalid_evidence_basis_origin")
    if "provenance_basis_origin" in df.columns and ~df["provenance_basis_origin"].isin({"SOURCE_PROVIDED", "DERIVED_FROM_ACCEPTED_V550_BRIDGE"}).all():
        issues.append("invalid_provenance_basis_origin")
    if "temporal_authority_status" in df.columns and ~df["temporal_authority_status"].eq("NOT_EVALUATED_AT_V551").all():
        issues.append("invalid_temporal_authority_status")
    if {"evidence_basis", "evidence_basis_origin"}.issubset(df.columns):
        derived = df["evidence_basis_origin"].eq("DERIVED_FROM_ACCEPTED_V550_BRIDGE")
        for value in df.loc[derived, "evidence_basis"].fillna("").astype(str):
            try:
                if json.loads(value).get("contract") != "V551_EVIDENCE_BASIS_V1":
                    issues.append("invalid_derived_evidence_basis_contract")
                    break
            except Exception:
                issues.append("invalid_derived_evidence_basis_json")
                break
    if {"provenance_basis", "provenance_basis_origin"}.issubset(df.columns):
        derived = df["provenance_basis_origin"].eq("DERIVED_FROM_ACCEPTED_V550_BRIDGE")
        for value in df.loc[derived, "provenance_basis"].fillna("").astype(str):
            try:
                if json.loads(value).get("contract") != "V551_PROVENANCE_BASIS_V1":
                    issues.append("invalid_derived_provenance_basis_contract")
                    break
            except Exception:
                issues.append("invalid_derived_provenance_basis_json")
                break
    if "source_measure_kind" in df.columns and ~df["source_measure_kind"].eq("response_category_distribution").all():
        issues.append("invalid_source_measure_kind")
    if "source_measure_status" in df.columns and ~df["source_measure_status"].eq("OBSERVED").all():
        issues.append("invalid_source_measure_status")
    if "support_may_be_used_as_pressure" in df.columns and df["support_may_be_used_as_pressure"].map(lambda value: _to_bool(value, False)).any():
        issues.append("support_may_be_used_as_pressure_true")
    if "prevalence_may_be_used_as_pressure" in df.columns and df["prevalence_may_be_used_as_pressure"].map(lambda value: _to_bool(value, False)).any():
        issues.append("prevalence_may_be_used_as_pressure_true")
    if "n_respondents" in df.columns:
        denom = pd.to_numeric(df["n_respondents"], errors="coerce")
        nonblank = df["n_respondents"].notna() & df["n_respondents"].astype(str).str.strip().ne("")
        if (nonblank & denom.isna()).any():
            issues.append("invalid_n_respondents_nonintegral")
        if (nonblank & denom.notna() & (denom <= 0)).any():
            issues.append("invalid_n_respondents_nonpositive")
        if (nonblank & denom.notna() & denom.map(lambda value: not float(value).is_integer())).any():
            issues.append("invalid_n_respondents_nonintegral")
        if "empirical_distribution_id" in df.columns:
            valid_dist = df["empirical_distribution_id"].fillna("").astype(str).str.match(r"^v551dist__[0-9a-f]{24}$")
            if (~valid_dist).any():
                issues.append("invalid_empirical_distribution_id")
        group_cols = V551_EMPIRICAL_DISTRIBUTION_GROUP_COLUMNS
        if all(column in df.columns for column in group_cols):
            for _, group in df.groupby(group_cols, dropna=False, sort=True):
                single_value_fields = [
                    "empirical_object_type",
                    "source_table",
                    "question_id",
                    "var_code",
                    "position_field",
                    "position_value",
                    "response_scale_signature",
                    "semantic_identity_signature",
                    "structural_identity_signature",
                ]
                for field in single_value_fields:
                    if field in group.columns and _clean_unique_count(group[field]) > 1:
                        issues.append(f"inconsistent_distribution_identity_field={field}")
                        break
                if _ambiguous_response_category_group(group):
                    issues.append("ambiguous_response_category_within_distribution")
                    break
                group_denom = pd.to_numeric(group["n_respondents"], errors="coerce").dropna()
                distinct = sorted(set(float(value) for value in group_denom.tolist()))
                if len(distinct) > 1:
                    issues.append("inconsistent_n_respondents_within_empirical_distribution")
                    break
                if len(distinct) == 1:
                    sum_n = pd.to_numeric(group.get("n_unweighted", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()
                    if sum_n > distinct[0]:
                        issues.append("category_count_exceeds_respondent_denominator")
                        break
    if {"observed_response_zero", "response_intensity_status", "response_intensity"}.issubset(df.columns):
        observed_zero = df["observed_response_zero"].map(lambda value: _to_bool(value, False))
        intensity = pd.to_numeric(df["response_intensity"], errors="coerce")
        bad_zero = observed_zero & ~(df["response_intensity_status"].eq("OBSERVED_NUMERIC") & intensity.eq(0.0))
        if bad_zero.any():
            issues.append("observed_response_zero_without_numeric_zero")
        missing_as_zero = df["response_intensity_status"].eq("MISSING") & intensity.eq(0.0)
        if missing_as_zero.any():
            issues.append("missing_intensity_coerced_to_zero")
    if {"v552_pressure_component_eligible", "v552_pressure_component_status", "v552_pressure_component_ineligibility_reason"}.issubset(df.columns):
        eligible = df["v552_pressure_component_eligible"].map(lambda value: _to_bool(value, False))
        status_eligible = df["v552_pressure_component_status"].eq("ELIGIBLE") & df["v552_pressure_component_ineligibility_reason"].fillna("").astype(str).eq("")
        if not eligible.equals(status_eligible):
            issues.append("pressure_component_eligible_status_mismatch")
        review_without_reason = df["v552_pressure_component_status"].eq("REVIEW_REQUIRED") & df["v552_pressure_component_ineligibility_reason"].fillna("").astype(str).eq("")
        if review_without_reason.any():
            issues.append("review_required_without_reason")
        temporal_reason = df["v552_pressure_component_ineligibility_reason"].fillna("").astype(str).str.contains("temporal", case=False, regex=False)
        if temporal_reason.any():
            issues.append("temporal_authority_used_as_pressure_gate")
    if "atom_id" in df.columns and df["atom_id"].duplicated().any():
        issues.append("duplicate_atom_id")
    if {"atom_id", "atom_contract_hash"}.issubset(df.columns) and df[["atom_id", "atom_contract_hash"]].duplicated().any():
        issues.append("duplicate_atom_contract_identity")
    for column, expected in [("is_substantive", True), ("is_missing", False), ("is_special", False)]:
        if column in df.columns:
            values = df[column].map(lambda value: _to_bool(value, not expected))
            if not values.eq(expected).all():
                issues.append(f"invalid_{column}_state")
    if "schema_version" in df.columns and ~df["schema_version"].eq(ATOM_SCHEMA_VERSION).all():
        issues.append("invalid_atom_schema_version")
    return issues


def validate_v551_relation_evidence_atoms(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_RELATION_EVIDENCE_ATOMS_SCHEMA["required_columns"], "v551_relation_evidence_atoms")


def validate_v551_atom_exclusion_audit(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"], "v551_atom_exclusion_audit")
