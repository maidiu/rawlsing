#!/usr/bin/env python3
"""V550 -> V551 bridge index compiler helpers."""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Mapping
from collections import Counter
from itertools import combinations
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_io import EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES, infer_response_family
from data.ddm_build_copy.ddm_v550_source_structure import _is_ses_relation_evidence, _normalized_join_key
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_question_use import allowed_uses_for_role, evidence_role_for_semantic_role, infer_semantic_role
from data.ddm_build_copy.ddm_v550_authority_contract import (
    CERTIFIED_RESPONSE_SEMANTICS_STATUSES,
)
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity
from data.ddm_build_copy.ddm_v550_response_options import normalize_response_code
from data.ddm_build_copy.ddm_v550_schema import V551_BRIDGE_INDEX_SCHEMA, validate_bridge_index
from data.ddm_build_copy.ddm_v550_validation import validate_v551_bridge_rows
from data.ddm_build_copy.numeric_formulas import support_prevalence_companions
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, confidence_tier_from_support, support_status_from_count, support_threshold_series, support_threshold_from_total
from data.ddm_build_copy.ddm_v550_question_relation_authority import apply_question_relation_authority
from data.ddm_build_copy.ddm_v550_family_overlay import (
    OverlayLoadResult,
    canonical_family_key,
    canonical_wave_key,
    load_family_overlay,
    wave_aliases,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR = ROOT / "data" / "ddm_build_copy" / "directionality_authority"
DEFAULT_GSS_DIRECTIONALITY_OVERLAY_PATH = DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR / "gss1972_directionality_authority.csv"

MIN_V551_RELATION_EVIDENCE_N = DEFAULT_SUPPORT_CAP
GSS_DIRECTIONALITY_OVERLAY_COLUMNS = [
    "var_name",
    "question_text",
    "semantic_role",
    "semantic_subrole",
    "directionality_policy",
    "signed_polarity_status",
    "response_family_expectation",
    "positive_anchor_label",
    "negative_anchor_label",
    "neutral_anchor_label",
    "bridge_directionality_action",
    "directionality_confidence",
    "directionality_note",
    "manual_review_required",
]
NUMERIC_ONLY_LABEL_ALLOWED_FAMILIES = {
    "yes_no",
    "agreement_scale",
    "trust_scale",
    "satisfaction_scale",
    "importance_scale",
    "frequency_scale",
    "ordinal_scale",
    "left_right_scale",
    "nominal_single_choice",
    "numeric_quantity",
    "numeric_scale",
    "count",
    "count_scale",
}
FORBIDDEN_RELATION_IDS = {
    "context",
    "context_not_applicable",
    "survey_admin_context",
    "administrative_context",
    "technical_metadata",
    "sample_design_context",
    "weighting_context",
}
FORBIDDEN_RELATION_TOKENS = {
    "admin",
    "metadata",
    "technical",
    "survey_admin",
    "sample_design",
    "weight",
}


BRIDGE_TABLE_MAP = {
    "answer_distribution": "answer_distribution",
    "country_answer_distribution": "country_answer_distribution",
    "position_distribution": "position_distribution",
    "position_indicator_summary": "position_indicator",
    "indicator_answer_matrix": "indicator_answer_matrix",
    "outlier_cohort_summary": "outlier_cohort",
    "secondary_indicator_summary": "secondary_indicator",
    "recursive_branch_nodes": "recursive_branch",
    "branch_position_signature": "branch_position_signature",
    "branch_relation_co_signature": "branch_relation_co_signature",
    "branch_co_signature": "branch_co_signature",
    "question_response_attitude_cloud": "attitude_cloud",
    "mapping_gap_report": "mapping_gap_report",
    "underpowered_quarantine": "underpowered_quarantine",
}

BRIDGE_EVIDENCE_LANE_MAP = {
    "answer_distribution": "direct_relation_response",
    "country_answer_distribution": "direct_relation_response",
    "indicator_answer_matrix": "derived_determinicity",
    "outlier_cohort_summary": "derived_determinicity",
    "recursive_branch_nodes": "derived_determinicity",
    "secondary_indicator_summary": "derived_determinicity",
    "position_distribution": "position_context",
    "position_indicator_summary": "position_context",
    "branch_position_signature": "position_context",
    "mapping_gap_report": "audit_quarantine",
    "underpowered_quarantine": "audit_quarantine",
    "question_response_attitude_cloud": "disabled_artifact",
    "branch_relation_co_signature": "disabled_artifact",
    "branch_co_signature": "disabled_artifact",
}

PIPELINE_PROCESS_TOTAL = 51
PIPELINE_PROCESS_LABELS = {
    "answer_distribution": 23,
    "country_answer_distribution": 24,
    "position_indicator_summary": 25,
    "indicator_answer_matrix": 26,
    "outlier_cohort_summary": 27,
    "secondary_indicator_summary": 28,
    "recursive_branch_nodes": 29,
    "branch_co_signature": 30,
    "question_response_attitude_cloud": 31,
    "mapping_gap_report": 44,
    "underpowered_quarantine": 53,
}


def _process_label(table_name: str) -> str:
    idx = PIPELINE_PROCESS_LABELS.get(table_name)
    return f" ({idx}/{PIPELINE_PROCESS_TOTAL})" if idx else ""


def _stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def _row_value(row: Any, *names: str, default: Any = "") -> Any:
    for name in names:
        if isinstance(row, Mapping):
            value = row.get(name, default)
            if pd.notna(value):
                text = str(value).strip()
                if text and text.lower() not in {"nan", "none"}:
                    return value
        if hasattr(row, name):
            value = getattr(row, name)
            if pd.notna(value):
                text = str(value).strip()
                if text and text.lower() not in {"nan", "none"}:
                    return value
    return default


def _question_respondent_lookup(question_universe: pd.DataFrame | None) -> dict[str, Any]:
    if question_universe is None or question_universe.empty:
        return {}
    lookup: dict[tuple[str, str, str], Any] = {}
    for row in question_universe.itertuples(index=False):
        row_dict = row._asdict()
        source = canonical_family_key(_row_value(row_dict, "source", "source_family"))
        wave = _row_value(row_dict, "wave", "canonical_wave")
        question_id = _normalized_join_key(_row_value(row_dict, "question_id"))
        var_code = _normalized_join_key(_row_value(row_dict, "var_code", "var_name"))
        n_respondents = _row_value(row_dict, "n_respondents", default="")
        n_respondents = pd.to_numeric(n_respondents, errors="coerce")
        if pd.isna(n_respondents):
            n_respondents = None
        else:
            n_respondents = int(n_respondents)
        for wave_variant in _wave_lookup_variants(source, wave):
            for key in {question_id, var_code}:
                if key:
                    lookup[(source, wave_variant, key)] = n_respondents
    return lookup


def _wave_lookup_variants(source: Any, wave: Any) -> list[str]:
    family = canonical_family_key(source)
    tokens: list[str] = []
    for token in [wave, canonical_wave_key(family, wave), *wave_aliases(family, wave)]:
        cleaned = str(token or "").strip()
        if cleaned:
            tokens.append(cleaned)
            normalized = _normalized_join_key(cleaned)
            if normalized:
                tokens.append(normalized)
    out: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        marker = token.strip().lower()
        if marker and marker not in seen:
            seen.add(marker)
            out.append(token.strip())
    return out


def _question_contract_lookup(question_use_contract: pd.DataFrame | None) -> dict[tuple[str, str, str], dict[str, Any]]:
    if question_use_contract is None or question_use_contract.empty:
        return {}
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in question_use_contract.itertuples(index=False):
        row_dict = row._asdict()
        source = canonical_family_key(_row_value(row_dict, "source", "source_family"))
        wave = _row_value(row_dict, "wave", "canonical_wave")
        question_id = _normalized_join_key(_row_value(row_dict, "question_id"))
        var_code = _normalized_join_key(_row_value(row_dict, "var_code", "var_name"))
        for wave_variant in _wave_lookup_variants(source, wave):
            for key in {question_id, var_code}:
                if key:
                    lookup[(source, wave_variant, key)] = row_dict
    return lookup


def _bridge_additional_fields(
    *,
    row: Any,
    question_contract_row: dict[str, Any] | None,
    wave: Any,
    row_hash: str,
    response_raw: Any,
    response_normalized: Any,
    support_status: str,
    support_companions: dict[str, Any],
    direct_relation_table: bool,
    empirical_object_type: str,
    semantic_role: str,
    bridge_evidence_lane: str,
    n_respondents: Any,
) -> dict[str, Any]:
    quc_owned_fields = {"semantic_role", "semantic_subrole", "semantic_role_authority_status", "current_directional_atom_eligible", "directional_applicability_status", "directional_certification_status", "directionality_authority_status", "structural_mapping_status", "driver_id", "driver_facet_id", "question_block_id", "structural_domain_id", "relation_axis_id", "target_entity_id", "allowed_as_v551_relation_evidence", "v551_evidence_role", "mapping_status", "source_structure_source", "source_structure_basis", "source_structure_confidence", "source_structure_fields_joined", "source_structure_review_required", "review_required", "manual_review_required", "manual_review_flag"}
    authority_conflicts: list[dict[str, Any]] = []

    def contract_or_row(*names: str, default: Any = "") -> Any:
        if question_contract_row is not None:
            contract_value = _row_value(question_contract_row, *names, default="")
            if str(contract_value).strip() not in {"", "nan", "none"}:
                candidate_value = _row_value(row, *names, default="")
                if names[0] in quc_owned_fields and str(candidate_value).strip() not in {"", "nan", "none"} and str(candidate_value) != str(contract_value):
                    authority_conflicts.append({"field": names[0], "candidate_value": candidate_value, "quc_value": contract_value, "conflict_class": "STALE_CANDIDATE_AUTHORITY_OVERRIDDEN_BY_CURRENT_QUC"})
                return contract_value
        value = _row_value(row, *names, default="")
        if str(value).strip() not in {"", "nan", "none"}:
            return value
        return default

    role_uses = allowed_uses_for_role(semantic_role)
    survey_year = contract_or_row("survey_year", default=wave)
    is_substantive_default = direct_relation_table or str(semantic_role).strip().upper() == "RELATION_EVIDENCE"
    is_substantive = _to_bool(contract_or_row("is_substantive", default=is_substantive_default))
    is_missing = _to_bool(contract_or_row("is_missing", default=False))
    is_dk = _to_bool(contract_or_row("is_dk", default=False))
    is_refusal = _to_bool(contract_or_row("is_refusal", default=False))
    is_iap = _to_bool(contract_or_row("is_iap", default=False))
    is_not_asked = _to_bool(contract_or_row("is_not_asked", default=False))
    is_inapplicable = _to_bool(contract_or_row("is_inapplicable", default=False))
    explicit_special = _to_bool(contract_or_row("is_special", default=False))
    is_special = explicit_special or is_missing or is_dk or is_refusal or is_iap or is_not_asked or is_inapplicable
    result = {
        "survey_year": survey_year,
        "analysis_scope": contract_or_row("analysis_scope", default="country"),
        "source_row_hash": row_hash,
        "response_value_raw": response_raw,
        "response_value_normalized": response_normalized,
        "response_topology": contract_or_row("response_topology", default=""),
        "future_evidence_eligible": _to_bool(contract_or_row("future_evidence_eligible", default=False)),
        "future_topology_evidence_eligible": _to_bool(contract_or_row("future_topology_evidence_eligible", default=contract_or_row("future_evidence_eligible", default=False))),
        "current_directional_atom_eligible": _to_bool(contract_or_row("current_directional_atom_eligible", default=False)),
        "directional_applicability_status": contract_or_row("directional_applicability_status", default="APPLICABILITY_UNRESOLVED"),
        "directional_certification_status": (
            str(contract_or_row("directional_certification_status", default="")).strip()
            or ("NOT_CERTIFIED_SPECIAL" if _to_bool(_row_value(row, "is_special", default=False)) else "NOT_CERTIFIED")
        ),
        "semantic_role_authority_status": contract_or_row(
            "semantic_role_authority_status", default=""
        ),
        "response_semantics_authority_status": contract_or_row(
            "response_semantics_authority_status", default=""
        ),
        "directionality_authority_status": contract_or_row(
            "directionality_authority_status", default=""
        ),
        "structural_mapping_status": contract_or_row(
            "structural_mapping_status", default=""
        ),
        "eligibility_gate_status": contract_or_row(
            "eligibility_gate_status", default=""
        ),
        "eligibility_failed_gates": contract_or_row(
            "eligibility_failed_gates", default=""
        ),
        "response_semantics_status": contract_or_row(
            "response_semantics_status", default=""
        ),
        "response_semantics_source": contract_or_row(
            "response_semantics_source", default=""
        ),
        "response_semantics_contract_hash": contract_or_row(
            "response_semantics_contract_hash", default=""
        ),
        "source_structure_fields_joined": _to_bool(contract_or_row("source_structure_fields_joined", default=False)),
        "source_structure_source": contract_or_row("source_structure_source", default=""),
        "source_structure_basis": contract_or_row("source_structure_basis", default=""),
        "source_structure_confidence": contract_or_row("source_structure_confidence", default=""),
        "source_structure_review_required": _to_bool(contract_or_row("source_structure_review_required", default=False)),
        "source_structure_join_key": contract_or_row("source_structure_join_key", default=""),
        "source_structure_join_confidence": contract_or_row("source_structure_join_confidence", default=""),
        "ordinal_rank": contract_or_row("ordinal_rank", default=None),
        "scale_min": contract_or_row("scale_min", default=None),
        "scale_max": contract_or_row("scale_max", default=None),
        "support_gate_status": support_companions.get("support_gate_status", support_status),
        "support_threshold": support_companions.get("support_threshold", None),
        "support_ratio": support_companions.get("support_ratio"),
        "support_ratio_margin": support_companions.get("support_ratio_margin"),
        "support_score": support_companions.get("support_score"),
        "support_formula_id": support_companions.get("support_formula_id", ""),
        "support_formula_version": support_companions.get("support_formula_version", ""),
        "support_implementation_function": support_companions.get("support_implementation_function", ""),
        "support_score_family": support_companions.get("support_score_family", ""),
        "support_higher_is_better": support_companions.get("support_higher_is_better", False),
        "support_decision_role": support_companions.get("support_decision_role", ""),
        "population_share": support_companions.get("population_share"),
        "prevalence_score": support_companions.get("prevalence_score"),
        "prevalence_formula_id": support_companions.get("prevalence_formula_id", ""),
        "prevalence_formula_version": support_companions.get("prevalence_formula_version", ""),
        "prevalence_implementation_function": support_companions.get("prevalence_implementation_function", ""),
        "prevalence_score_family": support_companions.get("prevalence_score_family", ""),
        "prevalence_higher_is_better": support_companions.get("prevalence_higher_is_better", False),
        "prevalence_decision_role": support_companions.get("prevalence_decision_role", ""),
        "is_substantive": is_substantive,
        "is_missing": is_missing,
        "is_special": is_special,
        "is_dk": is_dk,
        "is_refusal": is_refusal,
        "is_iap": is_iap,
        "is_not_asked": is_not_asked,
        "is_inapplicable": is_inapplicable,
        "normalization_confidence": contract_or_row(
            "normalization_confidence",
            default="",
        ),
        "v551_visible": _to_bool(contract_or_row("v551_visible", default=True)),
        "v551_evidence_role": contract_or_row("v551_evidence_role", default=evidence_role_for_semantic_role(semantic_role)),
        "driver_id": contract_or_row("driver_id", default=""),
        "driver_facet_id": contract_or_row("driver_facet_id", default=""),
        "relation_axis_id": contract_or_row("relation_axis_id", default=""),
        "target_entity_id": contract_or_row("target_entity_id", default=""),
        "strata_relevance": contract_or_row("strata_relevance", default=""),
        "strata_path": _conditional_strata_path(contract_or_row("conditional_strata_weights", default="")),
        "subject_position_signature": _subject_position_signature(
            {
                "position_conditioning": contract_or_row("position_conditioning", default=""),
                "position_modifiers": contract_or_row("position_modifiers", default=""),
                "strata_path": _conditional_strata_path(contract_or_row("conditional_strata_weights", default="")),
                "horizon_affordance": contract_or_row("horizon_affordance", default=""),
            }
        ),
        "mapping_status": contract_or_row("mapping_status", default=""),
        "allowed_as_response_distribution": _to_bool(
            contract_or_row("allowed_as_response_distribution", default=role_uses["allowed_as_response_distribution"])
        ),
        "allowed_as_position_distribution": _to_bool(
            contract_or_row("allowed_as_position_distribution", default=role_uses["allowed_as_position_distribution"])
        ),
        "allowed_as_context_distribution": _to_bool(
            contract_or_row("allowed_as_context_distribution", default=role_uses["allowed_as_context_distribution"])
        ),
        "allowed_as_demographic_predictor": _to_bool(
            contract_or_row("allowed_as_demographic_predictor", default=role_uses["allowed_as_demographic_predictor"])
        ),
        "allowed_as_branch_splitter": _to_bool(
            contract_or_row("allowed_as_branch_splitter", default=role_uses["allowed_as_branch_splitter"])
        ),
        "allowed_as_branch_position_signature": _to_bool(
            contract_or_row("allowed_as_branch_position_signature", default=role_uses["allowed_as_branch_position_signature"])
        ),
        "allowed_as_branch_relation_cosignature": _to_bool(
            contract_or_row("allowed_as_branch_relation_cosignature", default=role_uses["allowed_as_branch_relation_cosignature"])
        ),
        "allowed_as_attitude_cloud_anchor": _to_bool(
            contract_or_row("allowed_as_attitude_cloud_anchor", default=role_uses["allowed_as_attitude_cloud_anchor"])
        ),
        "allowed_as_attitude_cloud_feature": _to_bool(
            contract_or_row("allowed_as_attitude_cloud_feature", default=role_uses["allowed_as_attitude_cloud_feature"])
        ),
        "allowed_as_v551_relation_evidence": _to_bool(
            contract_or_row("allowed_as_v551_relation_evidence", default=role_uses["allowed_as_v551_relation_evidence"])
        ),
        "allowed_as_parent_prior_coordinate": _to_bool(
            contract_or_row("allowed_as_parent_prior_coordinate", default=role_uses["allowed_as_parent_prior_coordinate"])
        ),
        "allowed_as_temporal_pressure_indicator": _to_bool(
            contract_or_row("allowed_as_temporal_pressure_indicator", default=role_uses["allowed_as_temporal_pressure_indicator"])
        ),
        "allowed_as_runtime_persona_evidence": _to_bool(
            contract_or_row("allowed_as_runtime_persona_evidence", default=role_uses["allowed_as_runtime_persona_evidence"])
        ),
        "legacy_final_driver_id": contract_or_row("legacy_final_driver_id", default=""),
        "legacy_driver_leak_flag": _to_bool(contract_or_row("legacy_driver_leak_flag", default=False)),
        "forbidden_inference": contract_or_row("forbidden_inference", default=""),
        "known_absences": contract_or_row("known_absences", default=""),
        "manual_review_flag": _to_bool(contract_or_row("manual_review_flag", "review_required", "manual_designation_required", default=False)),
        "manual_review_reason": contract_or_row("manual_review_reason", default=""),
        "question_type": contract_or_row("question_type", default=""),
        "handling_rule": contract_or_row("handling_rule", default=""),
        "recommended_computation": contract_or_row("recommended_computation", default=""),
        "semantic_subrole": contract_or_row("semantic_subrole", default=""),
        "semantic_tags": contract_or_row("semantic_tags", default=""),
        "directionality_policy": contract_or_row("directionality_policy", default=""),
        "semantic_confidence": contract_or_row("semantic_confidence", default=""),
        "semantic_note": contract_or_row("semantic_note", default=""),
        "position_conditioning": contract_or_row("position_conditioning", default=""),
        "position_modifiers": contract_or_row("position_modifiers", default=""),
        "conditional_strata_weights": contract_or_row("conditional_strata_weights", default=""),
        "horizon_affordance": contract_or_row("horizon_affordance", default=""),
        "position_conditioning_note": contract_or_row("position_conditioning_note", default=""),
        "position_conditioning_confidence": contract_or_row("position_conditioning_confidence", default=""),
        "question_use_contract_joined": _to_bool(contract_or_row("question_use_contract_joined", default=False)),
        "evidence_basis": contract_or_row("evidence_basis", default=""),
        "provenance_basis": contract_or_row("provenance_basis", default=""),
        "created_at": contract_or_row("created_at", default=utc_now()),
    }
    result["authority_merge_conflicts"] = json.dumps(authority_conflicts, sort_keys=True)
    return result


def _bridge_evidence_lane_for_source_table(source_table: str) -> str:
    return BRIDGE_EVIDENCE_LANE_MAP.get(str(source_table or "").strip(), "unknown")


def _support_status_from_support(value: Any, *, lane: str, total_respondents: Any = None) -> str:
    return support_status_from_count(
        value,
        total_respondents=total_respondents,
        lane=lane,
        support_cap=MIN_V551_RELATION_EVIDENCE_N,
    )


def _bridge_lane_usability(lane: str, support_status: str) -> tuple[bool, bool]:
    usable_for_evidence = (
        lane == "direct_relation_response"
        and support_status in {"sufficient_support", "supported", "underpowered"}
    ) or (
        lane == "derived_determinicity"
        and support_status == "sufficient_support"
    )
    conditional_determinicity = lane == "derived_determinicity" and support_status == "sufficient_support"
    return usable_for_evidence, conditional_determinicity


def _is_numeric_only_label(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", text):
        return False
    return True


def _response_family_allows_numeric_only_label(value: Any) -> bool:
    family = str(value or "").strip().lower()
    if not family:
        return False
    if family in NUMERIC_ONLY_LABEL_ALLOWED_FAMILIES:
        return True
    return family.endswith("_scale") or any(token in family for token in {"numeric", "quantity", "count"})


def _numeric_only_label_allowed(bridge: pd.DataFrame) -> pd.Series:
    if bridge.empty:
        return pd.Series(dtype=bool, index=bridge.index)
    numeric_only = bridge.get("response_label", pd.Series([""] * len(bridge), index=bridge.index)).apply(_is_numeric_only_label)
    family_allowed = bridge.get("response_family", pd.Series([""] * len(bridge), index=bridge.index)).apply(_response_family_allows_numeric_only_label)
    high_confidence = bridge.get("normalization_confidence", pd.Series([""] * len(bridge), index=bridge.index)).fillna("").astype(str).str.strip().str.lower().eq("high")
    return numeric_only & family_allowed & high_confidence


def _apply_v551_eligibility(bridge: pd.DataFrame) -> pd.DataFrame:
    """Apply fail-closed V551 eligibility gates and preserve every failed cause.

    ``v551_eligible`` is the direct-relation atom gate.  Context, position, and
    derived-determinicity lanes retain their dedicated eligibility fields but do
    not masquerade as direct relation evidence.
    """
    if bridge.empty:
        return bridge
    bridge = bridge.copy()
    if "semantic_role" not in bridge.columns:
        bridge["semantic_role"] = bridge.apply(lambda row: infer_semantic_role(row.to_dict()), axis=1)
    if "v551_evidence_role" not in bridge.columns:
        bridge["v551_evidence_role"] = bridge["semantic_role"].map(evidence_role_for_semantic_role)
    if "v551_visible" not in bridge.columns:
        bridge["v551_visible"] = True
    else:
        bridge["v551_visible"] = bridge["v551_visible"].map(lambda value: True if pd.isna(value) else _to_bool(value, True))
    if "question_use_contract_joined" not in bridge.columns:
        bridge["question_use_contract_joined"] = False
    if "bridge_evidence_lane" not in bridge.columns:
        bridge["bridge_evidence_lane"] = "unknown"
    if "support_status" not in bridge.columns:
        bridge["support_status"] = "missing_support"
    if "usable_for_evidence" not in bridge.columns:
        bridge["usable_for_evidence"] = False

    lane = bridge["bridge_evidence_lane"].fillna("").astype(str)
    semantic_role = bridge["semantic_role"].fillna("").astype(str)
    driver = bridge.get("driver_id", pd.Series([""] * len(bridge), index=bridge.index)).fillna("").astype(str).str.strip().str.lower()
    relation_axis = bridge.get("relation_axis_id", pd.Series([""] * len(bridge), index=bridge.index)).fillna("").astype(str).str.strip().str.lower()
    target_entity = bridge.get("target_entity_id", pd.Series([""] * len(bridge), index=bridge.index)).fillna("").astype(str).str.strip().str.lower()
    mapping_status = bridge.get("mapping_status", pd.Series([""] * len(bridge), index=bridge.index)).fillna("").astype(str).str.strip().str.lower()

    direct_lane = lane.eq("direct_relation_response")
    derived_lane = lane.eq("derived_determinicity")
    audit_lane = lane.eq("audit_quarantine")
    relation_role = semantic_role.eq("RELATION_EVIDENCE")
    context_role = semantic_role.isin(["STRUCTURAL_CONTEXT", "POSITION_COORDINATE", "MISSINGNESS_SIGNAL"])
    substantive = _bool_series(bridge, "is_substantive", False)
    special = _bool_series(bridge, "is_special", False) | _bool_series(bridge, "is_missing", False)
    response_map_matched = _bool_series(bridge, "response_option_map_matched", False)
    source_structure_joined = _bool_series(bridge, "source_structure_fields_joined", False)
    contract_joined = _bool_series(bridge, "question_use_contract_joined", False)
    allowed_relation = _bool_series(bridge, "allowed_as_v551_relation_evidence", False)
    allowed_cloud = _bool_series(bridge, "allowed_as_attitude_cloud_feature", False)
    allowed_persona = _bool_series(bridge, "allowed_as_runtime_persona_evidence", False)
    review_required = (
        _bool_series(bridge, "review_required", False)
        | _bool_series(bridge, "manual_review_flag", False)
        | _bool_series(bridge, "manual_review_required", False)
        | _bool_series(bridge, "manual_designation_required", False)
        | _bool_series(bridge, "source_structure_review_required", False)
    )
    visible = _bool_series(bridge, "v551_visible", True)

    metadata_driver = driver.str.startswith("metadata::")
    context_axis = relation_axis.eq("context")
    context_target = target_entity.isin({"context", "context_not_applicable", "not_applicable", "none"})
    context_mapping = mapping_status.str.contains("context_only", regex=False)
    semantic_authority_certified = (
        bridge.get(
            "semantic_role_authority_status",
            pd.Series([""] * len(bridge), index=bridge.index),
        )
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .eq("CERTIFIED")
    )
    response_semantics_certified = (
        bridge.get(
            "response_semantics_status",
            pd.Series([""] * len(bridge), index=bridge.index),
        )
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(CERTIFIED_RESPONSE_SEMANTICS_STATUSES)
        & bridge.get(
            "response_semantics_source",
            pd.Series([""] * len(bridge), index=bridge.index),
        ).fillna("").astype(str).str.strip().ne("")
        & bridge.get(
            "response_semantics_contract_hash",
            pd.Series([""] * len(bridge), index=bridge.index),
        ).fillna("").astype(str).str.strip().ne("")
    )
    directionality_certified = (
        _bool_series(bridge, "current_directional_atom_eligible", False)
        & bridge.get(
            "directionality_authority_status",
            pd.Series([""] * len(bridge), index=bridge.index),
        ).fillna("").astype(str).str.strip().str.upper().eq("CERTIFIED")
    )
    structural_mapping_complete = (
        bridge.get(
            "structural_mapping_status",
            pd.Series([""] * len(bridge), index=bridge.index),
        )
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .eq("COMPLETE")
    )
    relation_structure_certified = (
        relation_role
        & allowed_relation
        & structural_mapping_complete
        & ~context_axis
        & ~context_target
    )
    context_mapping_blocks_relation = context_mapping & ~relation_structure_certified

    numeric_only_allowed = _numeric_only_label_allowed(bridge)
    numeric_only_blocked = (
        bridge.get("response_label", pd.Series([""] * len(bridge), index=bridge.index)).apply(_is_numeric_only_label)
        & ~numeric_only_allowed
    )

    common_relation_gates = (
        relation_role
        & semantic_authority_certified
        & response_semantics_certified
        & directionality_certified
        & structural_mapping_complete
        & allowed_relation
        & ~review_required
        & contract_joined
        & source_structure_joined
        & visible
        & substantive
        & ~special
        & response_map_matched
        & ~metadata_driver
        & ~context_axis
        & ~context_target
        & ~context_mapping_blocks_relation
        & ~numeric_only_blocked
        & ~audit_lane
    )

    bridge["v551_context_eligible"] = context_role
    bridge["v551_position_coordinate_eligible"] = semantic_role.eq("POSITION_COORDINATE") & _bool_series(
        bridge, "allowed_as_position_distribution", True
    )
    bridge["v551_relation_evidence_eligible"] = direct_lane & common_relation_gates
    bridge["v551_conditional_determinicity_eligible"] = derived_lane & common_relation_gates
    bridge["v551_cloud_eligible"] = semantic_role.isin(["RELATION_EVIDENCE", "STRUCTURAL_CONTEXT"]) & allowed_cloud & contract_joined
    bridge["v551_persona_packet_eligible"] = semantic_role.isin(
        ["RELATION_EVIDENCE", "STRUCTURAL_CONTEXT", "POSITION_COORDINATE"]
    ) & allowed_persona & contract_joined
    bridge["v551_eligible"] = bridge["v551_relation_evidence_eligible"]

    failed_by_index: dict[Any, list[str]] = {}
    primary_by_index: dict[Any, str] = {}
    for idx in bridge.index:
        failures: list[str] = []
        if audit_lane.loc[idx]:
            failures.append("audit_quarantine_not_relation_evidence")
        if derived_lane.loc[idx]:
            failures.append("derived_determinicity_not_direct_relation_evidence")
        if not substantive.loc[idx] or special.loc[idx]:
            failures.append("non_substantive_or_missing_response")
        if not response_map_matched.loc[idx] and direct_lane.loc[idx]:
            failures.append("response_option_map_unmatched_not_relation_evidence")
        if metadata_driver.loc[idx]:
            failures.append("metadata_driver_prefix_not_relation_evidence")
        if context_axis.loc[idx]:
            failures.append("context_relation_axis_not_relation_evidence")
        if context_target.loc[idx]:
            failures.append("context_target_entity_not_relation_evidence")
        if context_mapping_blocks_relation.loc[idx] or (context_role.loc[idx] and direct_lane.loc[idx]):
            failures.append("structural_context_not_relation_evidence")
        if not source_structure_joined.loc[idx] and direct_lane.loc[idx]:
            failures.append("source_structure_fields_not_joined")
        if not semantic_authority_certified.loc[idx] and direct_lane.loc[idx]:
            failures.append("semantic_role_authority_not_certified")
        if not response_semantics_certified.loc[idx] and direct_lane.loc[idx]:
            failures.append("response_semantics_authority_not_certified")
        if not directionality_certified.loc[idx] and direct_lane.loc[idx]:
            failures.append("directionality_authority_not_certified")
        if not structural_mapping_complete.loc[idx] and direct_lane.loc[idx]:
            failures.append("structural_mapping_not_complete")
        if not contract_joined.loc[idx] and direct_lane.loc[idx]:
            failures.append("question_use_contract_not_joined")
        if review_required.loc[idx]:
            failures.append("review_required_not_relation_evidence")
        if contract_joined.loc[idx] and not allowed_relation.loc[idx] and direct_lane.loc[idx]:
            failures.append("question_use_contract_blocks_relation_evidence")
        if numeric_only_blocked.loc[idx]:
            failures.append("numeric_only_label_requires_numeric_scale_family")
        if not relation_role.loc[idx] and direct_lane.loc[idx] and not context_role.loc[idx]:
            failures.append("semantic_role_not_relation_evidence")
        if not visible.loc[idx]:
            failures.append("v551_not_visible")
        failures = list(dict.fromkeys(failures))
        failed_by_index[idx] = failures

        if bridge.at[idx, "v551_relation_evidence_eligible"]:
            primary = ""
        else:
            priority = [
                "audit_quarantine_not_relation_evidence",
                "derived_determinicity_not_direct_relation_evidence",
                "non_substantive_or_missing_response",
                "metadata_driver_prefix_not_relation_evidence",
                "context_relation_axis_not_relation_evidence",
                "context_target_entity_not_relation_evidence",
                "structural_context_not_relation_evidence",
                "question_use_contract_not_joined",
                "semantic_role_authority_not_certified",
                "response_semantics_authority_not_certified",
                "directionality_authority_not_certified",
                "structural_mapping_not_complete",
                "review_required_not_relation_evidence",
                "question_use_contract_blocks_relation_evidence",
                "response_option_map_unmatched_not_relation_evidence",
                "source_structure_fields_not_joined",
                "numeric_only_label_requires_numeric_scale_family",
                "semantic_role_not_relation_evidence",
                "v551_not_visible",
            ]
            primary = next((reason for reason in priority if reason in failures), "missing_mapping_or_non_substantive")
        primary_by_index[idx] = primary

    bridge["v551_failed_gates"] = pd.Series(
        {idx: "|".join(failed_by_index[idx]) for idx in bridge.index}, dtype="object"
    )
    bridge["v551_failed_gate_count"] = bridge["v551_failed_gates"].map(
        lambda text: 0 if not text else len([piece for piece in str(text).split("|") if piece.strip()])
    )
    bridge["v551_exclusion_reason"] = pd.Series(primary_by_index, dtype="object")
    return bridge


def _base_bridge_row(
    row: Any,
    *,
    run_id: str,
    shard_id: str,
    empirical_object_type: str,
    source_table: str,
    question_respondent_lookup: dict[str, Any] | None = None,
    question_contract_lookup: dict[str, dict[str, Any]] | None = None,
    directionality_overlay_lookup: dict[tuple[str, str, str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    response_raw = _row_value(row, "response_value_raw", "response_value", "value_raw")
    response_normalized = _row_value(row, "response_value_normalized", "response_label", "value_text", default=response_raw)
    if not str(response_normalized).strip() or str(response_normalized).strip().lower() == "nan":
        response_normalized = normalize_response_code(_row_value(row, "value_raw", "response_value", "value_text")) or response_normalized
    response_label = _row_value(row, "response_label", "normalized_response_label", "value_text", "value_raw", default=response_normalized)
    normalized_response_label = str(response_label).strip() or str(response_normalized).strip()
    question_id = _row_value(row, "question_id")
    var_code = _row_value(row, "var_code")
    source_raw = _row_value(row, "source", "source_family")
    source_key = canonical_family_key(source_raw)
    wave_key = _row_value(row, "wave")
    question_contract_row = None
    if question_contract_lookup:
        for wave_variant in _wave_lookup_variants(source_raw, wave_key):
            for key in (_normalized_join_key(question_id), _normalized_join_key(var_code)):
                lookup_key = (source_key, wave_variant, key)
                if key and lookup_key in question_contract_lookup:
                    question_contract_row = question_contract_lookup[lookup_key]
                    break
            if question_contract_row is not None:
                break
    position_field = _row_value(row, "position_field")
    position_value = _row_value(row, "position_value")
    country_code = _row_value(row, "country_code")
    source = _row_value(row, "source")
    source_family = _row_value(row, "source_family", "source")
    wave = _row_value(row, "wave")
    canonical_wave = _row_value(row, "canonical_wave", "wave")
    n_respondents = _row_value(row, "n_respondents", default="")
    if not str(n_respondents).strip() and question_respondent_lookup:
        for wave_variant in _wave_lookup_variants(source_raw, wave):
            for key in (_normalized_join_key(question_id), _normalized_join_key(var_code)):
                lookup_key = (source_key, wave_variant, key)
                if key and lookup_key in question_respondent_lookup:
                    n_respondents = question_respondent_lookup[lookup_key]
                    break
            if str(n_respondents).strip():
                break
    n_respondents = pd.to_numeric(n_respondents, errors="coerce")
    n_respondents = None if pd.isna(n_respondents) else int(n_respondents)
    direct_relation_table = source_table in {"answer_distribution", "country_answer_distribution"}
    response_option_map_matched = _to_bool(_row_value(row, "response_option_map_matched", default=False))
    response_family = _row_value(row, "response_family", default="")
    if direct_relation_table and not str(response_family).strip():
        if _is_ses_relation_evidence(row):
            response_family = "numeric_scale"
        else:
            inferred_family = infer_response_family(
                _row_value(row, "question_text", default=""),
                var_code or question_id,
                [normalized_response_label],
                storage_type=_row_value(row, "storage_type", default=""),
                measure=_row_value(row, "recommended_computation", default=""),
            )
            if inferred_family and inferred_family != "unknown":
                response_family = inferred_family
    payload = {
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source,
        "wave": wave,
        "country_code": country_code,
        "n_respondents": n_respondents,
        "question_id": question_id,
        "var_code": var_code,
        "position_field": position_field,
        "position_value": position_value,
        "response_raw": response_raw,
        "response_normalized": response_normalized,
        "empirical_object_type": empirical_object_type,
        "source_table": source_table,
    }
    row_hash = _stable_hash(payload)
    existing_semantic_role = _row_value(row, "semantic_role", default="")
    if question_contract_row and _row_value(question_contract_row, "semantic_role", default=""):
        semantic_role = _row_value(question_contract_row, "semantic_role", default="UNKNOWN")
    elif existing_semantic_role:
        semantic_role = existing_semantic_role
    elif _is_ses_relation_evidence(row):
        semantic_role = "RELATION_EVIDENCE"
    else:
        semantic_role = "UNKNOWN"
    if source_table == "position_distribution":
        semantic_role = "POSITION_COORDINATE"
    bridge_evidence_lane = _bridge_evidence_lane_for_source_table(source_table)
    support_status = _support_status_from_support(
        _row_value(row, "n_unweighted", default=None),
        lane=bridge_evidence_lane,
        total_respondents=n_respondents,
    )
    support_companions = support_prevalence_companions(
        _row_value(row, "n_unweighted", default=None),
        total_respondents=n_respondents,
        lane=bridge_evidence_lane,
        support_cap=MIN_V551_RELATION_EVIDENCE_N,
    )
    usable_for_evidence, conditional_determinicity = _bridge_lane_usability(bridge_evidence_lane, support_status)
    evidence_role = evidence_role_for_semantic_role(semantic_role)
    uses = allowed_uses_for_role(semantic_role)
    substantive_default = direct_relation_table or source_table == "indicator_answer_matrix"
    empirical_object_id = "|".join(
        [
            str(empirical_object_type),
            str(source),
            str(wave),
            str(country_code),
            str(question_id),
            str(position_field),
            str(position_value),
            str(response_raw),
            row_hash[:16],
        ]
    )

    # V550 owns only the source/neutral coordinate. It must not project a
    # canonical signed side, polarity, or signed intensity. V551 performs that
    # exact-response adjudication using the response-scale authority.
    response_intensity = _row_value(row, "response_intensity", default=None)
    special_flags = [
        _to_bool(_row_value(row, "is_special", default=False)),
        _to_bool(_row_value(row, "is_missing", default=False)),
        _to_bool(_row_value(row, "is_dk", default=False)),
        _to_bool(_row_value(row, "is_refusal", default=False)),
        _to_bool(_row_value(row, "is_iap", default=False)),
        _to_bool(_row_value(row, "is_not_asked", default=False)),
        _to_bool(_row_value(row, "is_inapplicable", default=False)),
    ]
    is_special_row = any(special_flags)
    if direct_relation_table and not is_special_row and _safe_float(response_intensity) is None:
        numeric_normalized = _safe_float(response_normalized)
        numeric_label = _safe_float(response_label)
        if numeric_normalized is not None and (
            numeric_label is not None
            or str(response_family).strip().lower() in {"numeric_scale", "numeric_quantity", "count", "count_scale"}
        ):
            response_intensity = numeric_normalized
    # Transport only the authoritative raw response-category direction already
    # present on a matched V550 response-option row. This is not a signed
    # projection: V551 still owns side, magnitude, rule application, and final
    # adjudication. Question-level polarity/certification cannot manufacture a
    # category direction here.
    raw_response_direction = str(_row_value(row, "response_direction", default="") or "").strip().lower()
    response_direction = (
        raw_response_direction
        if direct_relation_table and response_option_map_matched and not is_special_row
        else ""
    )
    polarity = ""
    scale_direction = ""
    directionality_status = "NOT_PROJECTED_V550"
    ordinal_rank = _row_value(row, "ordinal_rank", default=None)
    scale_min = _row_value(row, "scale_min", default=None)
    scale_max = _row_value(row, "scale_max", default=None)
    if is_special_row:
        response_intensity = None
        directionality_status = "NOT_CERTIFIED_SPECIAL"
        ordinal_rank = None
        scale_min = None
        scale_max = None

    bridge_row = {
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source,
        "source_family": source_family,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "question_id": question_id,
        "var_code": var_code,
        "position_field": position_field,
        "position_value": position_value,
        "response_raw": response_raw,
        "response_normalized": response_normalized,
        "response_label": response_label,
        "normalized_response_label": normalized_response_label,
        "response_family": response_family,
        "response_direction": response_direction,
        "response_intensity": response_intensity,
        "polarity": polarity,
        "scale_direction": scale_direction,
        "directionality_status": directionality_status,
        "bridge_evidence_lane": bridge_evidence_lane,
        "support_status": support_status,
        "support_status_label": support_companions.get("support_status_label", support_status),
        "support_tier": support_companions.get("support_tier", confidence_tier_from_support(support_status)),
        "support_n_unweighted": _row_value(row, "n_unweighted", default=None),
        "support_n_weighted": _row_value(row, "n_weighted", default=None),
        "support_n_total": _row_value(row, "n_total", default=None),
        "n_unweighted": _row_value(row, "n_unweighted", default=None),
        "n_weighted": _row_value(row, "n_weighted", default=None),
        "pct_unweighted": _row_value(row, "pct_unweighted", default=None),
        "pct_weighted": _row_value(row, "pct_weighted", default=None),
        "weight_status": _row_value(row, "weight_status", default=""),
        "confidence_tier": _row_value(
            row,
            "confidence_tier",
            default=support_companions.get("support_tier", confidence_tier_from_support(support_status)),
        ),
        "support_fraction": support_companions.get("support_fraction"),
        "support_prevalence_status": support_companions.get("support_prevalence_status"),
        "support_prevalence_ratio": support_companions.get("support_prevalence_ratio"),
        "support_prevalence_gap": support_companions.get("support_prevalence_gap"),
        "evidence_role": evidence_role,
        "allowed_uses": uses,
        "empirical_object_type": empirical_object_type,
        "empirical_object_id": empirical_object_id,
        "semantic_role": semantic_role,
        "v551_visible": True,
        "response_option_map_matched": response_option_map_matched,
        "substantive_default": substantive_default,
        "usable_for_evidence": usable_for_evidence,
        "conditional_determinicity": conditional_determinicity,
        "question_respondent_lookup": question_respondent_lookup,
        "directionality_overlay_lookup": directionality_overlay_lookup,
        "n_respondents": n_respondents,
        "source_table": source_table,
        "row_hash": row_hash,
        "response_semantics_status": _row_value(row, "response_semantics_status", default=""),
        "response_semantics_source": _row_value(row, "response_semantics_source", default=""),
        "response_semantics_contract_hash": _row_value(row, "response_semantics_contract_hash", default=""),
        "source_structure_classification": _row_value(row, "source_structure_classification", default=""),
        "source_structure_basis": _row_value(row, "source_structure_basis", default=""),
        "source_structure_confidence": _row_value(row, "source_structure_confidence", default=""),
        "source_structure_review_required": _to_bool(_row_value(row, "source_structure_review_required", default=False)),
        "source_structure_source": _row_value(row, "source_structure_source", default=""),
        "source_structure_fields_joined": _to_bool(_row_value(row, "source_structure_fields_joined", default=False)),
        "source_structure_join_key": _row_value(row, "source_structure_join_key", default=""),
        "source_structure_join_confidence": _row_value(row, "source_structure_join_confidence", default=""),
        "allowed_as_response_distribution": _to_bool(_row_value(row, "allowed_as_response_distribution", default=uses["allowed_as_response_distribution"])),
        "allowed_as_position_distribution": _to_bool(_row_value(row, "allowed_as_position_distribution", default=uses["allowed_as_position_distribution"])),
        "allowed_as_context_distribution": _to_bool(_row_value(row, "allowed_as_context_distribution", default=uses["allowed_as_context_distribution"])),
        "allowed_as_demographic_predictor": _to_bool(_row_value(row, "allowed_as_demographic_predictor", default=uses["allowed_as_demographic_predictor"])),
        "allowed_as_branch_splitter": _to_bool(_row_value(row, "allowed_as_branch_splitter", default=uses["allowed_as_branch_splitter"])),
        "allowed_as_branch_position_signature": _to_bool(_row_value(row, "allowed_as_branch_position_signature", default=uses["allowed_as_branch_position_signature"])),
        "allowed_as_branch_relation_cosignature": _to_bool(_row_value(row, "allowed_as_branch_relation_cosignature", default=uses["allowed_as_branch_relation_cosignature"])),
        "allowed_as_attitude_cloud_anchor": _to_bool(_row_value(row, "allowed_as_attitude_cloud_anchor", default=uses["allowed_as_attitude_cloud_anchor"])),
        "allowed_as_attitude_cloud_feature": _to_bool(_row_value(row, "allowed_as_attitude_cloud_feature", default=uses["allowed_as_attitude_cloud_feature"])),
        "allowed_as_v551_relation_evidence": _to_bool(_row_value(row, "allowed_as_v551_relation_evidence", default=uses["allowed_as_v551_relation_evidence"])),
        "allowed_as_parent_prior_coordinate": _to_bool(_row_value(row, "allowed_as_parent_prior_coordinate", default=uses["allowed_as_parent_prior_coordinate"])),
        "allowed_as_temporal_pressure_indicator": _to_bool(_row_value(row, "allowed_as_temporal_pressure_indicator", default=uses["allowed_as_temporal_pressure_indicator"])),
        "allowed_as_runtime_persona_evidence": _to_bool(_row_value(row, "allowed_as_runtime_persona_evidence", default=uses["allowed_as_runtime_persona_evidence"])),
        "question_use_contract_hash": _row_value(row, "question_use_contract_hash", default=""),
        "question_use_contract_joined": _to_bool(_row_value(row, "question_use_contract_joined", default=False)),
        **_bridge_additional_fields(
            row=row,
            question_contract_row=question_contract_row,
            wave=wave,
            row_hash=row_hash,
            response_raw=response_raw,
            response_normalized=response_normalized,
            support_status=support_status,
            support_companions=support_companions,
            direct_relation_table=direct_relation_table,
            empirical_object_type=empirical_object_type,
            semantic_role=semantic_role,
            bridge_evidence_lane=bridge_evidence_lane,
            n_respondents=n_respondents,
        ),
    }
    return apply_question_relation_authority(bridge_row)


# The active 35-wave question-relation authority is resolved generically by
# ddm_v550_question_relation_authority. Family/question dictionaries are forbidden.
# No embedded question-specific relation authority.


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _log_progress(progress_started: float | None, message: str) -> None:
    if progress_started is None:
        return
    elapsed = time.monotonic() - progress_started
    print(f"[v550bridge +{elapsed:0.0f}s] {message}", flush=True)


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        parsed = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        if pd.isna(parsed):
            return None
        return float(parsed)
    except Exception:
        return None


def _normalize_gss_directionality_overlay_frame(frame: pd.DataFrame, *, source: str, wave: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, "source", "wave", "canonical_wave"])
    out = frame.copy()
    for column in GSS_DIRECTIONALITY_OVERLAY_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    if "manual_review_required" not in out.columns:
        out["manual_review_required"] = False
    out["source"] = source
    out["wave"] = wave
    out["canonical_wave"] = wave
    for column in [
        "var_name",
        "question_text",
        "semantic_role",
        "semantic_subrole",
        "directionality_policy",
        "signed_polarity_status",
        "response_family_expectation",
        "positive_anchor_label",
        "negative_anchor_label",
        "neutral_anchor_label",
        "bridge_directionality_action",
        "directionality_confidence",
        "directionality_note",
    ]:
        out[column] = out[column].fillna("").astype(str).str.strip()
    out["manual_review_required"] = out["manual_review_required"].map(_to_bool)
    return out


def _parse_weighted_strata(weighted: Any) -> list[str]:
    entries: list[tuple[str, float, int]] = []
    text = str(weighted or "").strip()
    if text.lower() in {"", "nan", "none"}:
        return []
    for idx, part in enumerate(text.split("|")):
        token = part.strip()
        if not token:
            continue
        if ":" in token:
            label, weight_text = token.split(":", 1)
        else:
            label, weight_text = token, ""
        label = label.strip()
        if not label:
            continue
        weight = _safe_float(weight_text)
        entries.append((label, float(weight) if weight is not None else 0.0, idx))
    entries.sort(key=lambda item: (-item[1], item[2], item[0]))
    ordered: list[str] = []
    for label, _, _ in entries:
        if label and label not in ordered:
            ordered.append(label)
    return ordered


def _conditional_strata_path(weighted: Any) -> str:
    path: list[str] = []
    text = str(weighted or "").strip()
    if text.lower() in {"nan", "none"}:
        return ""
    for label in _parse_weighted_strata(weighted):
        if label and label not in path:
            path.append(label)
    return "|".join(path)


def _subject_position_signature(record: dict[str, Any]) -> str:
    parts: list[str] = []
    conditioning = _row_value(record, "position_conditioning", default="") if isinstance(record, dict) else ""
    modifiers = _row_value(record, "position_modifiers", default="") if isinstance(record, dict) else ""
    strata_path = _row_value(record, "strata_path", default="") if isinstance(record, dict) else ""
    horizon = _row_value(record, "horizon_affordance", default="") if isinstance(record, dict) else ""
    if conditioning:
        parts.append(f"conditioning={conditioning}")
    if modifiers:
        parts.append(f"modifiers={modifiers}")
    if strata_path:
        parts.append(f"strata={strata_path}")
    if horizon:
        parts.append(f"horizon={horizon}")
    return "|".join(parts)


@lru_cache(maxsize=4)
def _cached_directionality_overlay_frame(path_text: str) -> pd.DataFrame:
    resolved = Path(path_text)
    if resolved.is_file():
        try:
            frame = pd.read_csv(resolved, low_memory=False)
        except Exception:
            return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *GSS_DIRECTIONALITY_OVERLAY_COLUMNS])
        match = re.search(r"^gss(?P<wave>[0-9]{4})_(?:directionality_authority|directionality_overlay)\.csv$", resolved.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        return _normalize_gss_directionality_overlay_frame(frame, source="GSS", wave=wave)
    if not resolved.exists():
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *GSS_DIRECTIONALITY_OVERLAY_COLUMNS])
    frames: list[pd.DataFrame] = []
    authority_paths = sorted(resolved.glob("gss*_directionality_authority.csv"))
    overlay_paths = sorted(resolved.glob("gss*_directionality_overlay.csv")) if not authority_paths else []
    for path in authority_paths or overlay_paths:
        match = re.match(r"^gss(?P<wave>[0-9]{4})_(?:directionality_authority|directionality_overlay)\.csv$", path.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        if not wave:
            continue
        try:
            frame = pd.read_csv(path, low_memory=False)
        except Exception:
            continue
        frames.append(_normalize_gss_directionality_overlay_frame(frame, source="GSS", wave=wave))
    if not frames:
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *GSS_DIRECTIONALITY_OVERLAY_COLUMNS])
    return pd.concat(frames, ignore_index=True, sort=False)


def _resolved_gss_directionality_directory(directory: Path | None = None) -> Path:
    return DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR if directory is None else Path(directory)


def load_gss_directionality_overlay(directory: Path | None = None, canonical_wave: str | None = None) -> pd.DataFrame:
    resolved = _resolved_gss_directionality_directory(directory)
    if not canonical_wave:
        return _cached_directionality_overlay_frame(str(resolved)).copy()
    result = load_family_overlay("GSS", canonical_wave, "directionality", search_roots=[resolved])
    if result.status == "FOUND" and result.data_frame is not None:
        return result.data_frame.copy()
    return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *GSS_DIRECTIONALITY_OVERLAY_COLUMNS])


def _exact_directionality_identifier_key(value: Any) -> str:
    return str(value or "").strip()


def _directionality_overlay_index(overlay: pd.DataFrame | None) -> dict[str, Any]:
    empty = {"exact": {}, "normalized": {}, "normalized_collisions": {}}
    if overlay is None or overlay.empty:
        return empty
    exact_lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    normalized_candidates: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = {}
    for row in overlay.itertuples(index=False):
        row_dict = row._asdict()
        source_raw = _row_value(row_dict, "source")
        source = canonical_family_key(source_raw)
        wave = canonical_wave_key(source_raw, _row_value(row_dict, "wave"))
        canonical_wave = canonical_wave_key(source_raw, _row_value(row_dict, "canonical_wave"))
        raw_var_name = str(_row_value(row_dict, "var_name", default="")).strip()
        exact_var_name = _exact_directionality_identifier_key(raw_var_name)
        normalized_var_name = _normalized_join_key(raw_var_name)
        for wave_key in {wave, canonical_wave}:
            if not source or not wave_key or not exact_var_name:
                continue
            exact_key = (source, wave_key, exact_var_name)
            existing_exact = exact_lookup.get(exact_key)
            if existing_exact is not None and existing_exact != row_dict:
                raise RuntimeError(
                    "duplicate exact directionality overlay row for "
                    f"source={source} wave={wave_key} var_name={raw_var_name}"
                )
            exact_lookup[exact_key] = row_dict
            if normalized_var_name:
                normalized_key = (source, wave_key, normalized_var_name)
                normalized_candidates.setdefault(normalized_key, {})[exact_var_name] = row_dict
    normalized_lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    normalized_collisions: dict[tuple[str, str, str], tuple[str, ...]] = {}
    for key, candidates in normalized_candidates.items():
        if len(candidates) == 1:
            normalized_lookup[key] = next(iter(candidates.values()))
        else:
            normalized_collisions[key] = tuple(sorted(candidates))
    return {
        "exact": exact_lookup,
        "normalized": normalized_lookup,
        "normalized_collisions": normalized_collisions,
    }


def _directionality_overlay_match(record: Any, overlay_lookup: dict[str, Any]) -> dict[str, Any] | None:
    if not overlay_lookup:
        return None
    source_raw = _row_value(record, "source", "source_family")
    source = canonical_family_key(source_raw)
    wave = canonical_wave_key(source_raw, _row_value(record, "wave"))
    canonical_wave = canonical_wave_key(source_raw, _row_value(record, "canonical_wave"))
    wave_keys = [key for key in (wave, canonical_wave) if key]
    raw_identifiers: list[str] = []
    for field_name in ("var_code", "var_name", "question_id", "source_var_name"):
        raw_value = _row_value(record, field_name, default="")
        cleaned = str(raw_value or "").strip()
        if cleaned and cleaned not in raw_identifiers:
            raw_identifiers.append(cleaned)
    exact_lookup = overlay_lookup.get("exact", {})
    normalized_lookup = overlay_lookup.get("normalized", {})
    normalized_collisions = overlay_lookup.get("normalized_collisions", {})
    for raw_identifier in raw_identifiers:
        exact_identifier = _exact_directionality_identifier_key(raw_identifier)
        for wave_key in wave_keys:
            key = (source, wave_key, exact_identifier)
            if all(key) and key in exact_lookup:
                return exact_lookup[key]
    for raw_identifier in raw_identifiers:
        normalized_identifier = _normalized_join_key(raw_identifier)
        for wave_key in wave_keys:
            key = (source, wave_key, normalized_identifier)
            if not all(key):
                continue
            if key in normalized_collisions:
                candidates = ", ".join(normalized_collisions[key])
                raise RuntimeError(
                    "ambiguous normalized directionality overlay match for "
                    f"source={source} wave={wave_key} var_name={raw_identifier}; "
                    f"exact candidates=[{candidates}]"
                )
            if key in normalized_lookup:
                return normalized_lookup[key]
    return None


def _directionality_family_hint(overlay_row: dict[str, Any]) -> str:
    family = str(_row_value(overlay_row, "response_family_expectation", default="")).strip().lower()
    if family in EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES:
        return family
    status = str(_row_value(overlay_row, "signed_polarity_status", "directionality_policy", default="")).strip().lower()
    if status == "signed_frequency":
        return "frequency_scale"
    if status in {"signed_evaluation", "signed_coordinate", "conditionally_signed_coordinate"}:
        return "ordinal_scale"
    if status in {"signed_attitude", "signed_policy"}:
        return "yes_no"
    return family or "ordinal_scale"


def _apply_directionality_overlay(
    *,
    response_family: str,
    response_label: str,
    response_direction: str,
    response_intensity: Any,
    polarity: str,
    scale_direction: str,
    directionality_status: str,
    ordinal_rank: Any,
    scale_min: Any,
    scale_max: Any,
    overlay_row: dict[str, Any] | None,
) -> tuple[str, Any, str, str, str]:
    """Compatibility helper only: V550 must never create canonical projection.

    The historical helper name remains import-compatible, but signed inputs are
    stripped and neutral/source intensity is returned unchanged. Exact signed
    adjudication belongs to V551.
    """
    if overlay_row is not None and _to_bool(_row_value(overlay_row, "manual_review_required", default=False)):
        return "", response_intensity, "", "", "manual_review_required_by_directionality_overlay"
    return "", response_intensity, "", "", "NOT_PROJECTED_V550"


def _normalize_bridge_frame(frame: pd.DataFrame, *, survey_year_is_numeric: bool) -> pd.DataFrame:
    if frame.empty:
        return frame
    out = frame.copy()
    if "survey_year" in out.columns:
        survey_year_series = out["survey_year"]
        if survey_year_is_numeric:
            out["survey_year"] = pd.to_numeric(survey_year_series, errors="coerce").astype("Int64")
        else:
            out["survey_year"] = survey_year_series.map(
                lambda value: None
                if value is None or pd.isna(value) or str(value).strip() == ""
                else str(value).strip()
            )
    for column in [
        "n_respondents", "ordinal_rank", "scale_min", "scale_max", "n_unweighted",
        "support_threshold", "n_atoms", "n_unweighted_total", "branch_depth",
    ]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").astype("Int64")
    for column in [
        "n_weighted", "n_weighted_total", "pct_unweighted", "pct_weighted",
        "pressure_score", "directionality_coverage", "response_intensity",
        "response_option_confidence_min", "response_option_confidence_max",
        "support_ratio", "support_ratio_margin", "support_score", "population_share",
        "prevalence_score",
    ]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").astype("float64")
    return out


def _bool_series(df: pd.DataFrame, column: str, default: bool) -> pd.Series:
    if column not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    series = df[column]
    if isinstance(series, pd.Series):
        text = series.fillna("").astype(str).str.strip().str.lower()
        return text.isin({"1", "true", "t", "yes", "y", "on"})
    return pd.Series([bool(series)] * len(df), index=df.index)


def _directionality_overlay_lookup_for_family(
    *,
    survey_family: str,
    canonical_wave: str,
    directionality_authority_dir: Path | None,
) -> dict[tuple[str, str, str], dict[str, Any]]:
    identity = require_survey_identity(survey_family, canonical_wave)
    result = load_family_overlay(
        identity.source,
        identity.canonical_wave,
        "directionality",
        required=False,
        search_roots=[directionality_authority_dir] if directionality_authority_dir else None,
    )
    if result.status == "FOUND" and result.data_frame is not None:
        return _directionality_overlay_index(result.data_frame)
    return _directionality_overlay_index(None)


def _directionality_overlay_lookup_for_frame(
    frame: pd.DataFrame,
    *,
    directionality_authority_dir: Path | None,
) -> dict[str, Any]:
    if frame is None or frame.empty:
        return _directionality_overlay_index(None)
    overlays: list[pd.DataFrame] = []
    seen: set[tuple[str, str]] = set()
    for record in frame.to_dict(orient="records"):
        source = _row_value(record, "source", "source_family")
        wave = _row_value(record, "canonical_wave", "wave")
        source_key = canonical_family_key(source)
        canonical = canonical_wave_key(source_key, wave)
        scope = (source_key, canonical)
        if not source_key or not canonical or scope in seen:
            continue
        seen.add(scope)
        authority_root = directionality_authority_dir or DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR
        result = load_family_overlay(
            source,
            canonical,
            "directionality",
            required=False,
            search_roots=[authority_root],
        )
        if result.status == "FOUND" and result.data_frame is not None and not result.data_frame.empty:
            overlays.append(result.data_frame)
    if not overlays:
        return _directionality_overlay_index(None)
    return _directionality_overlay_index(pd.concat(overlays, ignore_index=True, sort=False))


def build_v551_bridge_index_for_table(
    df: pd.DataFrame,
    *,
    run_id: str,
    shard_id: str,
    table_name: str,
    progress_started: float | None = None,
    directionality_overlay_lookup: dict[tuple[str, str, str], dict[str, Any]] | None = None,
    directionality_authority_dir: Path | None = None,
    question_contract_lookup: dict[str, dict[str, Any]] | None = None,
) -> pd.DataFrame:
    if df.empty:
        _log_progress(progress_started, f"bridge table {table_name}{_process_label(table_name)}: empty, skipping")
        return pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
    if directionality_overlay_lookup is None:
        directionality_overlay_lookup = _directionality_overlay_lookup_for_frame(
            df,
            directionality_authority_dir=directionality_authority_dir,
        )
    empirical_object_type = BRIDGE_TABLE_MAP.get(table_name, table_name)
    _log_progress(progress_started, f"bridge table {table_name}{_process_label(table_name)}: building {len(df)} rows")
    rows = []
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        rows.append(
            _base_bridge_row(
                row,
                run_id=run_id,
                shard_id=shard_id,
                empirical_object_type=empirical_object_type,
                source_table=table_name,
                directionality_overlay_lookup=directionality_overlay_lookup,
                question_contract_lookup=question_contract_lookup,
            )
        )
        if progress_started is not None and (idx == 1 or idx % 100000 == 0 or idx == len(df)):
            _log_progress(progress_started, f"bridge table {table_name}{_process_label(table_name)}: built {idx}/{len(df)} rows")
    bridge = pd.DataFrame(rows)
    return _apply_v551_eligibility(bridge)


def build_v551_bridge_index_for_shard(
    tables: dict[str, pd.DataFrame],
    *,
    run_id: str,
    shard_id: str,
    progress_started: float | None = None,
    directionality_overlay_lookup: dict[tuple[str, str, str], dict[str, Any]] | None = None,
    directionality_authority_dir: Path | None = None,
    survey_family: str = "",
    canonical_wave: str = "",
) -> pd.DataFrame:
    identity = require_survey_identity(survey_family, canonical_wave)
    survey_family = identity.source
    canonical_wave = identity.canonical_wave
    if directionality_overlay_lookup is None:
        directionality_overlay_lookup = _directionality_overlay_lookup_for_family(
            survey_family=survey_family,
            canonical_wave=canonical_wave,
            directionality_authority_dir=directionality_authority_dir,
        )
    frames = []
    observed_columns: list[str] = []
    survey_year_is_numeric = bool(re.fullmatch(r"\d{4}", shard_id.split("__")[-1].strip()))
    for table_name, df in tables.items():
        if table_name not in BRIDGE_TABLE_MAP:
            continue
        if df is None or df.empty:
            _log_progress(progress_started, f"bridge shard {shard_id}: {table_name}{_process_label(table_name)} is empty")
            continue
        _log_progress(progress_started, f"bridge shard {shard_id}: starting {table_name}{_process_label(table_name)}")
        frame = build_v551_bridge_index_for_table(
            df,
            run_id=run_id,
            shard_id=shard_id,
            table_name=table_name,
            progress_started=progress_started,
            directionality_overlay_lookup=directionality_overlay_lookup,
            directionality_authority_dir=directionality_authority_dir,
        )
        if frame is not None and not frame.empty:
            observed_columns.extend([col for col in frame.columns if col not in observed_columns])
            frames.append(frame.dropna(axis=1, how="all"))
        _log_progress(progress_started, f"bridge shard {shard_id}: finished {table_name}{_process_label(table_name)}")
    if not frames:
        return pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
    bridge = pd.concat(frames, ignore_index=True, sort=False)
    for column in observed_columns:
        if column not in bridge.columns:
            bridge[column] = pd.NA
    bridge = _normalize_bridge_frame(bridge, survey_year_is_numeric=survey_year_is_numeric)
    if "v551_exclusion_reason" not in bridge.columns:
        bridge["v551_exclusion_reason"] = ""
    if "v551_eligible" not in bridge.columns:
        bridge["v551_eligible"] = False
    bridge["v551_exclusion_reason"] = bridge["v551_exclusion_reason"].fillna("")
    return bridge


def build_bridge_lane_audits(bridge: pd.DataFrame) -> dict[str, pd.DataFrame]:
    empirical_columns = [
        "source", "wave", "canonical_wave", "source_table", "bridge_evidence_lane",
        "question_id", "var_code", "source_row_hash", "support_status",
        "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash",
        "source_structure_source", "source_structure_basis", "source_structure_confidence",
        "v551_eligible", "v551_exclusion_reason", "v551_failed_gates", "v551_failed_gate_count",
    ]
    support_quarantine_columns = [
        "source", "wave", "canonical_wave", "source_table", "bridge_evidence_lane",
        "question_id", "var_code", "support_status", "n_unweighted",
        "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash",
        "source_structure_source", "source_structure_basis", "source_structure_confidence",
        "v551_relation_evidence_eligible", "v551_exclusion_reason", "v551_failed_gates", "v551_failed_gate_count",
    ]
    if bridge.empty:
        empty_lane_counts = pd.DataFrame(columns=["source", "wave", "canonical_wave", "source_table", "bridge_evidence_lane", "row_count", "v551_relation_evidence_eligible_count", "v551_conditional_determinicity_eligible_count"])
        empty_exclusion_by_lane = pd.DataFrame(columns=["source", "wave", "canonical_wave", "bridge_evidence_lane", "v551_exclusion_reason", "row_count"])
        empty_direct = pd.DataFrame(columns=["source", "wave", "question_id", "var_code", "response_value_normalized", "normalized_response_label", "response_family", "n_unweighted", "support_status", "response_option_map_matched", "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash", "normalization_confidence", "is_substantive", "is_special", "source_structure_source", "source_structure_basis", "source_structure_confidence", "source_structure_fields_joined", "question_use_contract_joined", "response_topology", "future_evidence_eligible", "future_topology_evidence_eligible", "current_directional_atom_eligible", "directional_applicability_status", "directional_certification_status", "v551_relation_evidence_eligible", "v551_exclusion_reason", "v551_failed_gates", "v551_failed_gate_count"])
        empty_derived = pd.DataFrame(columns=["source", "wave", "source_table", "question_id", "var_code", "predictor_field", "predictor_value", "response_value_normalized", "n_unweighted", "support_status", "bridge_evidence_lane", "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash", "source_structure_source", "source_structure_basis", "source_structure_confidence", "future_topology_evidence_eligible", "current_directional_atom_eligible", "directional_applicability_status", "directional_certification_status", "v551_relation_evidence_eligible", "v551_conditional_determinicity_eligible", "reason_not_direct_relation_evidence", "v551_failed_gates", "v551_failed_gate_count"])
        empty_underpowered = pd.DataFrame(columns=["source", "wave", "source_table", "question_id", "var_code", "bridge_evidence_lane", "support_status", "n_unweighted", "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash", "source_structure_source", "source_structure_basis", "source_structure_confidence", "v551_relation_evidence_eligible", "v551_exclusion_reason", "v551_failed_gates", "v551_failed_gate_count"])
        empty_zero_support = pd.DataFrame(columns=["source", "wave", "source_table", "question_id", "var_code", "bridge_evidence_lane", "support_status", "n_unweighted", "response_family", "response_label", "normalized_response_label"])
        empty_empirical = pd.DataFrame(columns=empirical_columns)
        empty_candidate = pd.DataFrame(columns=empty_direct.columns)
        empty_derived_index = pd.DataFrame(columns=empty_derived.columns)
        empty_support_quarantine = pd.DataFrame(columns=support_quarantine_columns)
        empty_response_semantics = pd.DataFrame(columns=["source", "wave", "canonical_wave", "country_code", "source_table", "question_id", "var_code", "response_value_normalized", "response_label", "normalized_response_label", "response_family", "response_direction", "response_intensity", "polarity", "ordinal_rank", "scale_min", "scale_max", "scale_direction", "directionality_status", "response_topology", "future_evidence_eligible", "future_topology_evidence_eligible", "current_directional_atom_eligible", "directional_applicability_status", "directional_certification_status", "bridge_evidence_lane", "support_status", "is_substantive", "is_special", "response_option_map_matched", "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash", "source_structure_source", "source_structure_basis", "source_structure_confidence", "normalization_confidence", "v551_failed_gates", "v551_failed_gate_count"])
        return {
            "bridge_lane_counts": empty_lane_counts,
            "bridge_exclusion_reason_by_lane": empty_exclusion_by_lane,
            "empirical_object_index": empty_empirical,
            "v551_relation_candidate_index": empty_candidate,
            "derived_determinicity_index": empty_derived_index,
            "support_quarantine_index": empty_support_quarantine,
            "direct_relation_response_eligibility_audit": empty_direct,
            "derived_determinicity_support_audit": empty_derived,
            "underpowered_quarantine_audit": empty_underpowered,
            "zero_support_matrix_audit": empty_zero_support,
            "response_semantics_audit": empty_response_semantics,
        }

    frame = bridge.copy()
    frame["bridge_evidence_lane"] = frame.get("bridge_evidence_lane", pd.Series(["unknown"] * len(frame), index=frame.index)).fillna("unknown").astype(str).str.strip().replace("", "unknown")
    frame["v551_exclusion_reason"] = frame.get("v551_exclusion_reason", pd.Series([""] * len(frame), index=frame.index)).fillna("").astype(str)
    frame["support_status"] = frame.get("support_status", pd.Series(["missing_support"] * len(frame), index=frame.index)).fillna("").astype(str).str.strip().replace("", "missing_support")

    lane_counts = (
        frame.groupby(["source", "wave", "canonical_wave", "source_table", "bridge_evidence_lane"], dropna=False, sort=True)
        .agg(
            row_count=("bridge_evidence_lane", "size"),
            v551_relation_evidence_eligible_count=("v551_relation_evidence_eligible", lambda s: int(_bool_series(pd.DataFrame({"x": s}), "x", False).sum())),
            v551_conditional_determinicity_eligible_count=("v551_conditional_determinicity_eligible", lambda s: int(_bool_series(pd.DataFrame({"x": s}), "x", False).sum())),
        )
        .reset_index()
    )
    exclusion_by_lane = (
        frame.loc[~_bool_series(frame, "v551_eligible", False)]
        .groupby(["source", "wave", "canonical_wave", "bridge_evidence_lane", "v551_exclusion_reason"], dropna=False, sort=True)
        .size()
        .reset_index(name="row_count")
    )

    direct = frame.loc[frame["bridge_evidence_lane"].eq("direct_relation_response")].copy()
    if not direct.empty:
        direct = direct[[col for col in [
            "source", "wave", "question_id", "var_code", "response_value_normalized",
            "normalized_response_label", "response_family", "n_unweighted", "support_status",
            "response_option_map_matched", "response_semantics_status", "response_semantics_source",
            "response_semantics_contract_hash", "normalization_confidence", "is_substantive", "is_special",
            "source_structure_source", "source_structure_basis", "source_structure_confidence",
            "source_structure_fields_joined", "question_use_contract_joined", "response_topology",
            "future_evidence_eligible", "future_topology_evidence_eligible", "current_directional_atom_eligible",
            "directional_applicability_status", "directional_certification_status", "v551_relation_evidence_eligible",
            "v551_exclusion_reason", "v551_failed_gates", "v551_failed_gate_count",
        ] if col in direct.columns]].copy()

    derived = frame.loc[frame["bridge_evidence_lane"].eq("derived_determinicity")].copy()
    if not derived.empty:
        derived = derived.assign(
            predictor_field=derived.get("driver_id", pd.Series([""] * len(derived), index=derived.index)).fillna("").astype(str),
            predictor_value=derived.get("driver_facet_id", pd.Series([""] * len(derived), index=derived.index)).fillna("").astype(str),
            reason_not_direct_relation_evidence=derived.get("v551_exclusion_reason", pd.Series([""] * len(derived), index=derived.index)).fillna("").astype(str),
        )
        derived = derived[[col for col in [
            "source", "wave", "source_table", "question_id", "var_code", "predictor_field", "predictor_value",
            "response_value_normalized", "n_unweighted", "support_status", "bridge_evidence_lane",
            "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash",
            "source_structure_source", "source_structure_basis", "source_structure_confidence",
            "v551_relation_evidence_eligible", "v551_conditional_determinicity_eligible",
            "reason_not_direct_relation_evidence", "v551_failed_gates", "v551_failed_gate_count",
        ] if col in derived.columns]].copy()

    underpowered = frame.loc[frame["support_status"].isin(["underpowered", "zero_support", "missing_support"]) | frame["bridge_evidence_lane"].eq("audit_quarantine")].copy()
    if not underpowered.empty:
        underpowered = underpowered[[col for col in [
            "source", "wave", "source_table", "question_id", "var_code", "bridge_evidence_lane",
            "support_status", "n_unweighted", "response_semantics_status", "response_semantics_source",
            "response_semantics_contract_hash", "source_structure_source", "source_structure_basis",
            "source_structure_confidence", "v551_relation_evidence_eligible", "v551_exclusion_reason",
            "v551_failed_gates", "v551_failed_gate_count",
        ] if col in underpowered.columns]].copy()

    zero_support = frame.loc[(frame["source_table"].eq("indicator_answer_matrix")) & (frame["support_status"].eq("zero_support"))].copy()
    if not zero_support.empty:
        zero_support = zero_support[[col for col in [
            "source", "wave", "source_table", "question_id", "var_code", "bridge_evidence_lane", "support_status",
            "n_unweighted", "response_family", "response_label", "normalized_response_label",
            "response_semantics_status", "response_semantics_source", "response_semantics_contract_hash",
            "source_structure_source", "source_structure_basis", "source_structure_confidence",
        ] if col in zero_support.columns]].copy()

    response_semantics = frame.loc[frame["bridge_evidence_lane"].eq("direct_relation_response") | frame["bridge_evidence_lane"].eq("derived_determinicity")].copy()
    if not response_semantics.empty:
        response_semantics = response_semantics[[col for col in [
            "source", "wave", "canonical_wave", "country_code", "source_table", "question_id", "var_code",
            "response_value_normalized", "response_label", "normalized_response_label", "response_family",
            "response_direction", "response_intensity", "polarity", "ordinal_rank", "scale_min", "scale_max",
            "scale_direction", "directionality_status", "bridge_evidence_lane", "support_status", "is_substantive",
            "is_special", "response_option_map_matched", "response_semantics_status", "response_semantics_source",
            "response_semantics_contract_hash", "source_structure_source", "source_structure_basis",
            "source_structure_confidence", "response_topology", "future_evidence_eligible",
            "future_topology_evidence_eligible", "current_directional_atom_eligible", "directional_applicability_status",
            "directional_certification_status", "normalization_confidence", "v551_failed_gates", "v551_failed_gate_count",
        ] if col in response_semantics.columns]].copy()

    empirical_object_index = frame[[col for col in empirical_columns if col in frame.columns]].copy()
    v551_relation_candidate_index = direct.copy()
    derived_determinicity_index = derived.copy()
    support_quarantine_index = pd.concat(
        [
            underpowered[[col for col in support_quarantine_columns if col in underpowered.columns]].copy(),
            zero_support[[col for col in support_quarantine_columns if col in zero_support.columns]].copy(),
        ],
        ignore_index=True,
        sort=False,
    )
    return {
        "bridge_lane_counts": lane_counts,
        "bridge_exclusion_reason_by_lane": exclusion_by_lane,
        "empirical_object_index": empirical_object_index,
        "v551_relation_candidate_index": v551_relation_candidate_index,
        "derived_determinicity_index": derived_determinicity_index,
        "support_quarantine_index": support_quarantine_index,
        "direct_relation_response_eligibility_audit": direct,
        "derived_determinicity_support_audit": derived,
        "underpowered_quarantine_audit": underpowered,
        "zero_support_matrix_audit": zero_support,
        "response_semantics_audit": response_semantics,
    }


def _failed_gate_list(row: Any) -> list[str]:
    raw = _row_value(row, "v551_failed_gates", default="")
    if not str(raw).strip():
        raw = _row_value(row, "v551_exclusion_reason", default="")
    return [gate.strip() for gate in str(raw).split(";") if gate.strip()]


def _json_int(value: Any, default: int = 0) -> int:
    numeric = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric):
        return default
    return int(numeric)


def build_bridge_causal_summary(
    bridge: pd.DataFrame,
    *,
    max_pairs: int = 25,
    examples_per_reason: int = 5,
) -> dict[str, Any]:
    if bridge.empty:
        return {
            "bridge_rows": 0,
            "eligible_rows": 0,
            "excluded_rows": 0,
            "direct_relation_response": {
                "row_count": 0, "eligible_rows": 0, "excluded_rows": 0,
                "failed_gate_counts": {}, "failed_gate_count_histogram": {},
                "rows_with_multiple_failed_gates": 0, "top_gate_pairs": [],
                "exclusion_reason_counts": {}, "reason_examples": {},
            },
        }
    bridge_frame = bridge.copy()
    bridge_frame["bridge_evidence_lane"] = bridge_frame.get(
        "bridge_evidence_lane", pd.Series(["unknown"] * len(bridge_frame), index=bridge_frame.index)
    ).fillna("unknown").astype(str).str.strip().replace("", "unknown")
    bridge_frame["v551_exclusion_reason"] = bridge_frame.get(
        "v551_exclusion_reason", pd.Series([""] * len(bridge_frame), index=bridge_frame.index)
    ).fillna("").astype(str)
    bridge_frame["v551_failed_gates"] = bridge_frame.get(
        "v551_failed_gates", pd.Series([""] * len(bridge_frame), index=bridge_frame.index)
    ).fillna("").astype(str)
    bridge_frame["v551_failed_gate_count"] = pd.to_numeric(
        bridge_frame.get("v551_failed_gate_count", pd.Series([0] * len(bridge_frame), index=bridge_frame.index)),
        errors="coerce",
    ).fillna(0).astype(int)
    direct = bridge_frame.loc[bridge_frame["bridge_evidence_lane"].eq("direct_relation_response")].copy()
    if direct.empty:
        direct_payload = {
            "row_count": 0, "eligible_rows": 0, "excluded_rows": 0,
            "failed_gate_counts": {}, "failed_gate_count_histogram": {},
            "rows_with_multiple_failed_gates": 0, "top_gate_pairs": [],
            "exclusion_reason_counts": {}, "reason_examples": {},
        }
    else:
        failed_gate_counts: Counter[str] = Counter()
        pair_counts: Counter[tuple[str, str]] = Counter()
        reason_examples: dict[str, list[dict[str, Any]]] = {}
        for row in direct.itertuples(index=False):
            gates = sorted(set(_failed_gate_list(row)))
            for gate in gates:
                failed_gate_counts[gate] += 1
            if len(gates) > 1:
                for pair in combinations(gates, 2):
                    pair_counts[pair] += 1
            reason = _row_value(row, "v551_exclusion_reason", default="")
            reason = str(reason).strip() or ("eligible" if _to_bool(_row_value(row, "v551_eligible", default=False)) else "missing_mapping_or_non_substantive")
            samples = reason_examples.setdefault(reason, [])
            if len(samples) < examples_per_reason:
                samples.append({
                    "question_id": _row_value(row, "question_id", default=""),
                    "var_code": _row_value(row, "var_code", default=""),
                    "support_status": _row_value(row, "support_status", default=""),
                    "n_unweighted": _json_int(_row_value(row, "n_unweighted", default=None), default=0),
                    "failed_gates": gates,
                })
        top_pairs = [
            {"gate_a": pair[0], "gate_b": pair[1], "row_count": int(count)}
            for pair, count in pair_counts.most_common(max_pairs)
        ]
        direct_payload = {
            "row_count": int(len(direct)),
            "eligible_rows": int(_bool_series(direct, "v551_eligible", False).sum()),
            "excluded_rows": int(len(direct) - _bool_series(direct, "v551_eligible", False).sum()),
            "failed_gate_counts": {gate: int(count) for gate, count in failed_gate_counts.most_common()},
            "failed_gate_count_histogram": {str(int(k)): int(v) for k, v in direct["v551_failed_gate_count"].value_counts().sort_index().items()},
            "rows_with_multiple_failed_gates": int((direct["v551_failed_gate_count"] > 1).sum()),
            "top_gate_pairs": top_pairs,
            "exclusion_reason_counts": {reason: int(count) for reason, count in direct["v551_exclusion_reason"].fillna("").replace("", "<eligible>").value_counts().items()},
            "reason_examples": reason_examples,
        }
    lane_counts = (
        bridge_frame.groupby("bridge_evidence_lane", dropna=False, sort=True)
        .agg(
            row_count=("bridge_evidence_lane", "size"),
            eligible_rows=("v551_eligible", lambda s: int(_bool_series(pd.DataFrame({"x": s}), "x", False).sum())),
            excluded_rows=("v551_eligible", lambda s: int((~_bool_series(pd.DataFrame({"x": s}), "x", False)).sum())),
        )
        .reset_index()
    )
    excluded_reason_counts = {
        reason: int(count)
        for reason, count in bridge_frame["v551_exclusion_reason"].fillna("").replace("", "<eligible>").value_counts().items()
    }
    return {
        "bridge_rows": int(len(bridge_frame)),
        "eligible_rows": int(_bool_series(bridge_frame, "v551_eligible", False).sum()),
        "excluded_rows": int(len(bridge_frame) - _bool_series(bridge_frame, "v551_eligible", False).sum()),
        "eligible_by_lane": lane_counts.to_dict(orient="records"),
        "exclusion_reason_counts": excluded_reason_counts,
        "direct_relation_response": direct_payload,
    }


def iter_v551_bridge_index_batches_for_table(
    df: pd.DataFrame,
    *,
    run_id: str,
    shard_id: str,
    table_name: str,
    question_respondent_lookup: dict[str, Any] | None = None,
    question_contract_lookup: dict[str, dict[str, Any]] | None = None,
    directionality_overlay_lookup: dict[tuple[str, str, str], dict[str, Any]] | None = None,
    directionality_authority_dir: Path | None = None,
    progress_started: float | None = None,
    batch_size: int = 10_000,
    survey_year_is_numeric: bool = True,
):
    if df.empty:
        _log_progress(progress_started, f"bridge table {table_name}: empty, skipping")
        return
    if directionality_overlay_lookup is None:
        directionality_overlay_lookup = _directionality_overlay_lookup_for_frame(
            df,
            directionality_authority_dir=directionality_authority_dir,
        )
    empirical_object_type = BRIDGE_TABLE_MAP.get(table_name, table_name)
    _log_progress(progress_started, f"bridge table {table_name}: building {len(df)} rows")
    rows: list[dict[str, Any]] = []
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        rows.append(
            _base_bridge_row(
                row,
                run_id=run_id,
                shard_id=shard_id,
                empirical_object_type=empirical_object_type,
                source_table=table_name,
                question_respondent_lookup=question_respondent_lookup,
                question_contract_lookup=question_contract_lookup,
                directionality_overlay_lookup=directionality_overlay_lookup,
            )
        )
        if progress_started is not None and (idx == 1 or idx % 100000 == 0 or idx == len(df)):
            _log_progress(progress_started, f"bridge table {table_name}: built {idx}/{len(df)} rows")
        if len(rows) >= batch_size:
            yield _apply_v551_eligibility(
                _normalize_bridge_frame(
                    pd.DataFrame.from_records(rows, columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"]),
                    survey_year_is_numeric=survey_year_is_numeric,
                )
            )
            rows = []
    if rows:
        yield _apply_v551_eligibility(
            _normalize_bridge_frame(
                pd.DataFrame.from_records(rows, columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"]),
                survey_year_is_numeric=survey_year_is_numeric,
            )
        )


def write_v551_bridge_index_for_shard(
    tables: dict[str, pd.DataFrame],
    *,
    run_id: str,
    shard_id: str,
    bridge_path: Path,
    csv_path: Path | None = None,
    write_csv: bool = False,
    progress_started: float | None = None,
    batch_size: int = 10_000,
    directionality_overlay_lookup: dict[tuple[str, str, str], dict[str, Any]] | None = None,
    directionality_authority_dir: Path | None = None,
    survey_family: str = "",
    canonical_wave: str = "",
) -> dict[str, int]:
    import pyarrow as pa
    import pyarrow.parquet as pq

    identity = require_survey_identity(survey_family, canonical_wave)
    survey_family = identity.source
    canonical_wave = identity.canonical_wave
    if directionality_overlay_lookup is None:
        directionality_overlay_lookup = _directionality_overlay_lookup_for_family(
            survey_family=survey_family,
            canonical_wave=canonical_wave,
            directionality_authority_dir=directionality_authority_dir,
        )
    bridge_path.parent.mkdir(parents=True, exist_ok=True)
    if bridge_path.exists():
        bridge_path.unlink()
    if csv_path is not None and write_csv:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        if csv_path.exists():
            csv_path.unlink()

    writer: pq.ParquetWriter | None = None
    csv_header_written = False
    total_rows = 0
    eligible_rows = 0
    excluded_rows = 0
    numeric_only_label_excluded_rows = 0
    survey_year_is_numeric = bool(re.fullmatch(r"\d{4}", shard_id.split("__")[-1].strip()))
    question_respondent_lookup = _question_respondent_lookup(tables.get("question_universe"))
    question_contract_lookup = _question_contract_lookup(tables.get("question_use_contract"))

    try:
        for table_name, df in tables.items():
            if table_name not in BRIDGE_TABLE_MAP:
                continue
            if df is None or df.empty:
                _log_progress(progress_started, f"bridge shard {shard_id}: {table_name} is empty")
                continue
            _log_progress(progress_started, f"bridge shard {shard_id}: starting {table_name}")
            for chunk in iter_v551_bridge_index_batches_for_table(
                df,
                run_id=run_id,
                shard_id=shard_id,
                table_name=table_name,
                question_respondent_lookup=question_respondent_lookup,
                question_contract_lookup=question_contract_lookup,
                directionality_overlay_lookup=directionality_overlay_lookup,
                directionality_authority_dir=directionality_authority_dir,
                progress_started=progress_started,
                batch_size=batch_size,
                survey_year_is_numeric=survey_year_is_numeric,
            ):
                if chunk.empty:
                    continue
                table = pa.Table.from_pandas(
                    _normalize_bridge_frame(chunk, survey_year_is_numeric=survey_year_is_numeric),
                    preserve_index=False,
                )
                if writer is None:
                    writer = pq.ParquetWriter(str(bridge_path), table.schema, compression="snappy")
                else:
                    table = table.cast(writer.schema, safe=False)
                writer.write_table(table)
                if write_csv and csv_path is not None:
                    chunk.to_csv(csv_path, index=False, mode="a", header=not csv_header_written)
                    csv_header_written = True
                total_rows += len(chunk)
                if "v551_eligible" in chunk.columns:
                    chunk_eligible = int(chunk["v551_eligible"].fillna(False).sum())
                else:
                    chunk_eligible = 0
                eligible_rows += chunk_eligible
                excluded_rows += len(chunk) - chunk_eligible
                if "v551_exclusion_reason" in chunk.columns:
                    numeric_only_label_excluded_rows += int((chunk["v551_exclusion_reason"].fillna("").astype(str) == "numeric_only_label_requires_numeric_scale_family").sum())
            _log_progress(progress_started, f"bridge shard {shard_id}: finished {table_name}")
    finally:
        if writer is not None:
            writer.close()

    if writer is None:
        empty = pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
        empty.to_parquet(bridge_path, index=False)
        if write_csv and csv_path is not None:
            empty.to_csv(csv_path, index=False)

    return {
        "bridge_rows": total_rows,
        "eligible_rows": eligible_rows,
        "excluded_rows": excluded_rows,
        "numeric_only_label_excluded_rows": numeric_only_label_excluded_rows,
    }


def _validation_semantics_compatibility_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "response_semantics_status" not in df.columns:
        return df
    validation_df = df.copy()
    status = validation_df["response_semantics_status"].fillna("").astype(str).str.strip().str.lower()
    source = validation_df.get(
        "response_semantics_source", pd.Series([""] * len(validation_df), index=validation_df.index)
    ).fillna("").astype(str).str.strip().str.lower()
    contract_hash = validation_df.get(
        "response_semantics_contract_hash", pd.Series([""] * len(validation_df), index=validation_df.index)
    ).fillna("").astype(str).str.strip()
    matched = _bool_series(validation_df, "response_option_map_matched", False)
    packet_certified = (
        status.isin({"certified", "certified_manual_packet"})
        & source.str.endswith("_manual_authority_packet")
        & contract_hash.ne("")
        & matched
    )
    validation_df.loc[packet_certified, "response_semantics_status"] = "curated"
    return validation_df


def validate_bridge_df(df: pd.DataFrame) -> list[str]:
    return validate_v551_bridge_rows(_validation_semantics_compatibility_frame(df))


def _load_all_wave_directionality(directory):
    import pandas as pd, re
    from pathlib import Path
    from .ddm_v550_family_overlay import load_family_overlay
    if not directory:
        return None
    unique_waves = set()
    for fp in sorted(Path(directory).glob("gss*_directionality*.csv")):
        m = re.search(r'gss(\d{4})_', fp.name)
        if m:
            unique_waves.add(m.group(1))
    waves_found = []
    for wave in sorted(unique_waves):
        result = load_family_overlay("GSS", wave, "directionality", search_roots=[Path(directory)])
        if result.status == "FOUND" and result.data_frame is not None and not result.data_frame.empty:
            waves_found.append(result.data_frame)
    if not waves_found:
        return None
    combined = pd.concat(waves_found, ignore_index=True, sort=False)
    dedup_cols = [c for c in ['source', 'wave', 'canonical_wave', 'var_name'] if c in combined.columns]
    if dedup_cols:
        combined = combined.drop_duplicates(subset=dedup_cols)
    return combined
