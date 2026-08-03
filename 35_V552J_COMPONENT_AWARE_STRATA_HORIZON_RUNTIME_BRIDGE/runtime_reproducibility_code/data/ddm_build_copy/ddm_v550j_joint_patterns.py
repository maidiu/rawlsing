#!/usr/bin/env python3
"""V550J joint-response pattern compiler helpers."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_readiness import POSITION_FIELDS
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, DEFAULT_SUPPORT_FLOOR, support_status_from_count, support_threshold_from_total
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550j_registry_classifier import AssociationLaneRegistry
from data.ddm_build_copy.ddm_survey_identity import canonical_family_key
from data.ddm_build_copy.numeric_formulas import (
    COMPLETION_RATE_FORMULA_ID,
    COMPLETION_RATE_FORMULA_VERSION,
    COMPLETION_RATE_IMPLEMENTATION_FUNCTION,
    COMPLETION_RATE_SCORE_FAMILY,
    COMPLETION_RATE_HIGHEST_BETTER,
    COMPLETION_RATE_DECISION_ROLE,
    CONFIDENCE_FORMULA_ID,
    CONFIDENCE_FORMULA_VERSION,
    CONFIDENCE_IMPLEMENTATION_FUNCTION,
    CONFIDENCE_SCORE_FAMILY,
    CONFIDENCE_HIGHEST_BETTER,
    CONFIDENCE_DECISION_ROLE,
    EFFECTIVE_N_FORMULA_ID,
    EFFECTIVE_N_FORMULA_VERSION,
    EFFECTIVE_N_IMPLEMENTATION_FUNCTION,
    EFFECTIVE_N_SCORE_FAMILY,
    EFFECTIVE_N_HIGHEST_BETTER,
    EFFECTIVE_N_DECISION_ROLE,
    EFFECTIVE_N_RATIO_FORMULA_ID,
    EFFECTIVE_N_RATIO_FORMULA_VERSION,
    EFFECTIVE_N_RATIO_IMPLEMENTATION_FUNCTION,
    EFFECTIVE_N_RATIO_SCORE_FAMILY,
    EFFECTIVE_N_RATIO_HIGHEST_BETTER,
    EFFECTIVE_N_RATIO_DECISION_ROLE,
    MISSINGNESS_RATE_FORMULA_ID,
    MISSINGNESS_RATE_FORMULA_VERSION,
    MISSINGNESS_RATE_IMPLEMENTATION_FUNCTION,
    MISSINGNESS_RATE_SCORE_FAMILY,
    MISSINGNESS_RATE_HIGHEST_BETTER,
    MISSINGNESS_RATE_DECISION_ROLE,
    PATTERN_PROBABILITY_FORMULA_ID,
    PATTERN_PROBABILITY_FORMULA_VERSION,
    PATTERN_PROBABILITY_IMPLEMENTATION_FUNCTION,
    PATTERN_PROBABILITY_SCORE_FAMILY,
    PATTERN_PROBABILITY_HIGHEST_BETTER,
    PATTERN_PROBABILITY_DECISION_ROLE,
    WEIGHT_VALIDITY_FORMULA_ID,
    WEIGHT_VALIDITY_FORMULA_VERSION,
    WEIGHT_VALIDITY_IMPLEMENTATION_FUNCTION,
    WEIGHT_VALIDITY_SCORE_FAMILY,
    WEIGHT_VALIDITY_HIGHEST_BETTER,
    WEIGHT_VALIDITY_DECISION_ROLE,
    confidence_score_v1,
    completion_rate_v1,
    effective_n_ratio_v1,
    effective_n_v1,
    missingness_rate_v1,
    pattern_probability_v1,
    prevalence_score_v1,
    support_prevalence_companions,
    support_score_v1,
    weight_validity_score_v1,
)


ROOT = Path(__file__).resolve().parents[2]

V550J_SCHEMA_VERSION = "v1"
DEFAULT_ASSOCIATION_SUPPORT_THRESHOLD = 5

_POSITION_ASSOCIATION_CODES = {
    "AGE",
    "SEX",
    "RACE",
    "REG16",
    "REG16_7222",
    "REGION",
    "STATE",
    "MARITAL",
    "SIZE",
    "SEX12",
    "CHILDS",
    "EDUC",
    "RACEWHT",
}
_LIFE_COURSE_ASSOCIATION_CODES = {
    "AGEWED",
    "AGEKDBRN",
    "CHILDS",
    "MARCOHRT",
}
_INSTITUTIONAL_ASSOCIATION_CODES = {
    "UNION",
    "VOTE",
    "CHURCH",
    "ATTEND",
    "SCHOOL",
    "WORKPLACE",
}
_STATUS_ASSOCIATION_CODES = {
    "OCCSTAT",
    "SOCIOECON",
    "SOCIOECO",
    "CLASS",
    "STATUS",
}
_OCCUPATIONAL_ASSOCIATION_CODES = {
    "OCC",
    "OCC10",
    "ISCO08",
    "ISCO88",
    "INDUS10",
    "PAOCC",
    "PAISCO88",
    "WRKSTAT",
    "WORKHR",
    "WKSUP",
    "WKSUPS",
    "WKSUB",
    "WKSUBS",
    "WORKDY",
    "HRS1",
    "HRS2",
    "SPWRKSTA",
    "SPHOUR",
    "SPWRKSLF",
    "PAWRKSLF",
    "SPDAYS",
    "INDSTATUS",
    "MAINDSTATUS",
    "SPINDSTATUS",
    "PAINDSTATUS",
    "INDTAG",
    "MAINDTAG",
    "SPINDTAG",
    "PAINDTAG",
    "OCCSTATUS",
    "MAOCCSTATUS",
    "SPOCCSTATUS",
    "PAOCCSTATUS",
    "OCCTAG",
    "MAOCCTAG",
    "SPOCCTAG",
    "PAOCCTAG",
    "WRKSLF",
    "PAWRKSLF",
    "SPWRKSLF",
}
_FAMILY_BACKGROUND_ASSOCIATION_CODES = {
    "PAEDUC",
    "MAEDUC",
    "SPEDUC",
    "PADEG",
    "MADEG",
    "SPDEG",
    "FAMLIVE",
    "FAMILY",
    "FAMILY16",
    "SIBS",
    "CHILDS",
    "HOMEPOP",
    "BORN",
    "PARBORN",
    "MOBORN",
    "FOBORN",
}
_IDENTITY_ASSOCIATION_CODES = {
    "SEX",
    "GENDER",
    "RACE",
    "RACER",
    "RACEWHT",
    "ETHNICITY",
    "RELIG",
    "RELITEN",
    "NATIVITY",
    "BIRTHPLACE",
}
_ADMINISTRATIVE_ASSOCIATION_CODES = {
    "WEIGHT",
    "WT",
    "SAMPSTAT",
    "SAMPLE",
    "ADMIN",
    "ADMINCODE",
}
_SUBSTANTIVE_ATTITUDE_ASSOCIATION_CODES = {
    "PARTYID",
    "POLVIEWS",
    "GUNLAW",
    "COURTS",
    "HAPPY",
    "FEWORK",
    "RACSEG",
    "TRUST",
    "NATSPAC",
    "NATENVIR",
    "HELPPOOR",
    "HELPFUL",
    "SPKATH",
    "SPKCOM",
    "SPKHOMO",
    "SPKMIL",
    "SPKRAC",
    "SPKSOC",
    "LIBATH",
    "LIBCOM",
    "LIBHOMO",
    "LIBMIL",
    "LIBRAC",
    "LIBSOC",
}
_POLITICAL_BEHAVIOR_ASSOCIATION_CODES = {
    "VOTE68",
    "PRES68",
    "IF68WHO",
}
_MEDIA_EXPOSURE_ASSOCIATION_CODES = {
    "NEWS",
}
_HEALTH_STATUS_CONTEXT_ASSOCIATION_CODES = {
    "HEALTH",
}
_RESIDENCE_ORIGIN_CONTEXT_ASSOCIATION_CODES = {
    "MOBILE16",
    "RES16",
    "XNORCSIZ",
    "SRCBELT",
}
_FAMILY_DEMOGRAPHIC_CONTEXT_ASSOCIATION_CODES = {
    "CHLDNUM",
}
_SATISFACTION_CONTEXT_ASSOCIATION_CODES = {
    "SATJOB",
    "SATFIN",
}
_POLITICAL_ORIENTATION_ASSOCIATION_CODES = {
    "PARTYID",
}
_RELIGIOUS_ORIENTATION_ASSOCIATION_CODES = {
    "FOUND",
    "FUND",
}
_LANGUAGE_CULTURAL_CONTEXT_ASSOCIATION_CODES = {
    "SPANENG",
}
_ECONOMIC_POLICY_ATTITUDE_ASSOCIATION_CODES = {
    "POVLINE",
    "INCDEF",
}

_RAW_OCCUPATIONAL_STATUS_CODE_SUFFIXES = (
    "DOTPRES", "DOTSVP", "DOTGED", "DOTDATA", "DOTTHNG", "DOTPEOP",
    "SEI10INC", "SEI10EDUC", "SEI10", "PRESTG10", "PRESTG80",
    "OCC10", "OCC80", "OCC",
    "ISCO68", "ISCO08", "ISCO88",
    "INDUSTRY", "INDUS10",
    "SPOCC10", "SPOCC80", "SPOCC",
    "SPISCO08", "SPISCO68", "SPISCO88",
    "SPDOTSVP", "SPDOTPRES", "SPDOTGED", "SPDOTDATA", "SPDOTTHNG", "SPDOTPEOP",
    "PAOCC16", "PAOCC10", "PAOCC80", "PAOCC",
    "PAISCO08", "PAISCO68", "PAISCO88",
    "PADOTSVP", "PADOTPRES", "PADOTGED", "PADOTDATA", "PADOTTHNG", "PADOTPEOP",
    "MAOCC16", "MAOCC10", "MAOCC80", "MAOCC",
    "MAISCO08", "MAISCO68", "MAISCO88",
    "MADOTSVP", "MADOTPRES", "MADOTGED", "MADOTDATA", "MADOTTHNG", "MADOTPEOP",
    "SEI", "PRESTIGE", "PRES",
    "INDUS",
)

_RAW_OCCUPATIONAL_STATUS_CODE_PREFIXES = (
    "DOT",
    "OCC",
    "ISCO",
    "SEI",
    "SPOCC",
    "SPISCO",
    "SPDOT",
    "PAOCC",
    "PAISCO",
    "PADOT",
    "MAOCC",
    "MAISCO",
    "MADOT",
    "INDUS",
    "INDUSTRY",
)

_LANE_PUBLISHABILITY_MAP: dict[str, str] = {
    "substantive_attitude_association": "publishable_lane",
    "identity_coordinate_association": "review_only_lane",
    "position_context_association": "review_only_lane",
    "political_behavior_association": "review_only_lane",
    "media_exposure_association": "review_only_lane",
    "health_status_context_association": "review_only_lane",
    "residence_origin_context_association": "review_only_lane",
    "family_demographic_context_association": "review_only_lane",
    "satisfaction_context_association": "review_only_lane",
    "political_orientation_association": "review_only_lane",
    "religious_orientation_association": "review_only_lane",
    "language_cultural_context_association": "review_only_lane",
    "economic_policy_attitude_association": "review_only_lane",
    "occupational_status_association": "diagnostic_only_lane",
    "family_background_association": "review_only_lane",
    "life_course_context_association": "review_only_lane",
    "institutional_context_association": "review_only_lane",
    "status_code_association": "diagnostic_only_lane",
    "administrative_context": "blocked_lane",
    "diagnostic_numeric_context": "diagnostic_only_lane",
    "blocked_metadata_context": "blocked_lane",
    "unknown_association_lane": "unknown_lane",
}


def _is_raw_occupational_status_code(var_code: str) -> bool:
    code = str(var_code).upper().strip()
    if not code:
        return False
    if code in _RAW_OCCUPATIONAL_STATUS_CODE_SUFFIXES:
        return True
    for prefix in _RAW_OCCUPATIONAL_STATUS_CODE_PREFIXES:
        if code.startswith(prefix):
            return True
    return False


def _association_lane_publishability(lane: str) -> str:
    return _LANE_PUBLISHABILITY_MAP.get(str(lane).strip(), "unknown_lane")


def _compute_associated_var_cardinality(
    context_frame: pd.DataFrame | None,
    associated_var_code: str,
    *,
    wave: str = "",
    country_code: str = "",
) -> tuple[int, int, str, bool]:
    distinct_count = 0
    effective_cardinality = 0
    band = "unknown_cardinality"
    is_high = False
    if context_frame is not None and not context_frame.empty and "var_code" in context_frame.columns and "response_value_normalized" in context_frame.columns:
        var_frame = context_frame[context_frame["var_code"].astype(str).str.upper() == str(associated_var_code).upper()]
        if not var_frame.empty:
            distinct_values = var_frame["response_value_normalized"].dropna().unique()
            distinct_count = len(distinct_values)
            if distinct_count > 0:
                total = len(var_frame)
                if total > 0:
                    value_counts = var_frame["response_value_normalized"].value_counts(normalize=True)
                    effective_cardinality = int(1.0 / max(1e-12, (value_counts ** 2).sum()))
    if distinct_count <= 10:
        band = "low_cardinality"
    elif distinct_count <= 25:
        band = "moderate_cardinality"
    elif distinct_count <= 75:
        band = "high_cardinality"
    else:
        band = "very_high_cardinality"
        is_high = True
    is_high = is_high or distinct_count > 25
    return distinct_count, effective_cardinality, band, is_high


def _compute_associated_response_total_support(
    context_frame: pd.DataFrame | None,
    associated_var_code: str,
    associated_response_value: str,
) -> tuple[int, float, int]:
    total_n = 0
    total_weighted_n = 0.0
    baseline_share = 0.0
    if context_frame is not None and not context_frame.empty and "var_code" in context_frame.columns and "response_value_normalized" in context_frame.columns:
        var_frame = context_frame[context_frame["var_code"].astype(str).str.upper() == str(associated_var_code).upper()]
        if not var_frame.empty:
            total_n = len(var_frame)
            response_frame = var_frame[var_frame["response_value_normalized"].astype(str).str.strip() == str(associated_response_value).strip()]
            response_total_n = len(response_frame)
            if total_n > 0:
                baseline_share = response_total_n / total_n
            weight_col = "weight_value" if "weight_value" in context_frame.columns else "context_weight_value" if "context_weight_value" in context_frame.columns else None
            if weight_col is not None and not response_frame.empty:
                total_weighted_n = int(pd.to_numeric(response_frame[weight_col], errors="coerce").fillna(0.0).sum())
            return response_total_n, baseline_share, int(total_weighted_n)
    return 0, 0.0, 0


def _is_sparse_associated_response(associated_response_total_n: int, ultra: bool = False) -> bool:
    return associated_response_total_n < (5 if ultra else 10)


def _check_same_family_association(associated_var_code: str, family_var_codes: set[str]) -> bool:
    return str(associated_var_code).upper().strip() in {str(c).upper().strip() for c in (family_var_codes or set())}


def _check_same_variable_association(associated_var_code: str, pattern_var_codes: set[str]) -> bool:
    return str(associated_var_code).upper().strip() in {str(c).upper().strip() for c in (pattern_var_codes or set())}


V550J_ASSOCIATION_INDEX_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "pattern_id",
    "family_id",
    "var_code",
    "question_id",
    "item_role",
    "condition_label",
    "associated_var_code",
    "associated_question_id",
    "associated_response_value",
    "associated_response_value_normalized",
    "associated_response_label",
    "associated_response_direction",
    "p_response_given_pattern",
    "p_response_baseline",
    "denominator_basis",
    "baseline_denominator_basis",
    "difference_from_baseline",
    "lift",
    "mutual_information",
    "pattern_member_n_unweighted",
    "pattern_member_n_weighted",
    "pattern_var_answered_n_unweighted",
    "pattern_var_answered_n_weighted",
    "pattern_answered_var_n_unweighted",
    "pattern_answered_var_n_weighted",
    "response_overlap_n_unweighted",
    "response_overlap_n_weighted",
    "n_overlap_unweighted",
    "n_overlap_weighted",
    "association_support_n_unweighted",
    "association_support_n_weighted",
    "association_support_threshold",
    "association_support_ratio",
    "association_support_margin",
    "association_support_gate_status",
    "association_publication_status",
    "association_publication_reason",
    "support_status",
    "confidence_tier",
    "would_emit_as_publishable",
    "association_eligibility_status",
    "direct_evidence_status",
    "association_lane",
    "association_lane_status",
    "association_lane_authority_source",
    "association_lane_basis",
    "association_lane_resolution_type",
    "association_lane_authority_status",
    "association_lane_publishability",
    "associated_response_total_n",
    "associated_response_total_weighted_n",
    "associated_response_baseline_share",
    "associated_var_distinct_response_count",
    "associated_var_effective_cardinality",
    "associated_var_cardinality_band",
    "is_high_cardinality_associated_var",
    "is_sparse_associated_response",
    "is_raw_occupational_status_code",
    "is_same_family_association",
    "is_same_variable_association",
    "association_context_status",
    "association_status",
    "association_gate_status",
    "association_strength_status",
    "support_gate_status",
    "formula_id",
    "formula_version",
    "created_at",
    "schema_version",
]

V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "family_id",
    "pattern_id",
    "var_code",
    "question_id",
    "item_role",
    "condition_label",
    "associated_var_code",
    "associated_question_id",
    "associated_response_value",
    "associated_response_value_normalized",
    "associated_response_label",
    "associated_response_direction",
    "candidate_stage",
    "pattern_member_n_unweighted",
    "pattern_member_n_weighted",
    "eligible_rows_for_var",
    "eligible_rows_with_response_value",
    "pattern_member_rows_for_var",
    "response_overlap_n_unweighted",
    "response_overlap_n_weighted",
    "baseline_answered_n_unweighted",
    "baseline_answered_n_weighted",
    "pattern_var_answered_n_unweighted",
    "pattern_var_answered_n_weighted",
    "pattern_answered_var_n_unweighted",
    "pattern_answered_var_n_weighted",
    "n_overlap_unweighted",
    "n_overlap_weighted",
    "association_support_n_unweighted",
    "association_support_n_weighted",
    "association_support_threshold",
    "association_support_ratio",
    "association_support_margin",
    "association_support_gate_status",
    "association_publication_status",
    "association_publication_reason",
    "p_response_given_pattern",
    "p_response_baseline",
    "difference_from_baseline",
    "lift",
    "mutual_information",
    "support_threshold",
    "support_ratio",
    "support_gate_status",
    "suppression_reason",
    "would_emit_as_diagnostic",
    "would_emit_as_publishable",
    "association_eligibility_status",
    "direct_evidence_status",
    "association_lane",
    "association_lane_status",
    "association_lane_authority_source",
    "association_lane_basis",
    "association_lane_resolution_type",
    "association_lane_authority_status",
    "association_lane_publishability",
    "associated_response_total_n",
    "associated_response_total_weighted_n",
    "associated_response_baseline_share",
    "associated_var_distinct_response_count",
    "associated_var_effective_cardinality",
    "associated_var_cardinality_band",
    "is_high_cardinality_associated_var",
    "is_sparse_associated_response",
    "is_raw_occupational_status_code",
    "is_same_family_association",
    "is_same_variable_association",
    "association_context_status",
    "association_status",
    "association_gate_status",
    "association_strength_status",
    "support_status",
    "confidence_tier",
    "denominator_basis",
    "baseline_denominator_basis",
    "formula_id",
    "formula_version",
    "created_at",
    "schema_version",
]

V550J_ASSOCIATION_REVIEW_SURFACE_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "family_id",
    "pattern_id",
    "associated_var_code",
    "associated_response_value",
    "associated_response_label",
    "association_lane",
    "association_lane_status",
    "association_lane_authority_source",
    "association_lane_basis",
    "association_lane_resolution_type",
    "association_lane_authority_status",
    "association_lane_publishability",
    "associated_response_total_n",
    "associated_response_total_weighted_n",
    "associated_response_baseline_share",
    "associated_var_distinct_response_count",
    "associated_var_effective_cardinality",
    "associated_var_cardinality_band",
    "is_high_cardinality_associated_var",
    "is_sparse_associated_response",
    "is_raw_occupational_status_code",
    "association_support_n_unweighted",
    "association_support_threshold",
    "p_response_given_pattern",
    "p_response_baseline",
    "difference_from_baseline",
    "lift",
    "mutual_information",
    "association_publication_status",
    "review_surface_reason",
    "review_surface_priority",
    "created_at",
    "schema_version",
]

V550J_MEANING_SUMMARY_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "family_id",
    "pattern_id",
    "boundary_pattern_type",
    "pattern_support_n_unweighted",
    "pattern_support_status",
    "semantic_role_resolved_share",
    "target_structure_status",
    "target_selectivity_profile",
    "top_publishable_attitude_associations_json",
    "top_reviewable_attitude_signals_json",
    "top_identity_context_signals_json",
    "top_position_context_signals_json",
    "top_occupational_status_signals_json",
    "top_family_background_signals_json",
    "top_life_course_context_signals_json",
    "top_political_behavior_signals_json",
    "top_media_exposure_signals_json",
    "top_health_status_context_signals_json",
    "top_residence_origin_context_signals_json",
    "top_family_demographic_context_signals_json",
    "top_satisfaction_context_signals_json",
    "top_political_orientation_signals_json",
    "top_religious_orientation_signals_json",
    "top_language_cultural_context_signals_json",
    "top_economic_policy_attitude_signals_json",
    "top_unknown_or_diagnostic_signals_json",
    "publishable_attitude_signal_count",
    "true_reviewable_attitude_signal_count",
    "context_review_signal_count",
    "diagnostic_candidate_count",
    "displayed_diagnostic_signal_count",
    "unknown_signal_count",
    "meaning_summary_status",
    "meaning_summary_confidence",
    "meaning_summary_warning_flags_json",
    "created_at",
    "schema_version",
]

V550J_ASSOCIATION_FUNNEL_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "family_id",
    "outside_family_rows_total",
    "outside_family_rows_with_respondent_overlap",
    "outside_family_rows_with_positive_authority",
    "outside_family_rows_blocked_metadata_context",
    "outside_family_rows_blocked_not_direct_evidence",
    "outside_family_rows_blocked_missing_authority",
    "eligible_association_rows",
    "eligible_association_var_count",
    "eligible_association_var_codes",
    "association_lane_summary",
    "candidate_pairs_formed",
    "candidate_pairs_published",
    "candidate_pairs_suppressed_missing_response_value",
    "candidate_pairs_suppressed_no_candidate_pairs_formed",
    "candidate_pairs_suppressed_no_pattern_member_overlap",
    "candidate_pairs_suppressed_low_response_overlap",
    "candidate_pairs_suppressed_low_baseline",
    "candidate_pairs_suppressed_low_pattern_support",
    "candidate_pairs_suppressed_effect_size_zero_or_trivial",
    "pattern_var_answered_n_unweighted",
    "pattern_var_answered_n_weighted",
    "pattern_answered_var_n_unweighted",
    "pattern_answered_var_n_weighted",
    "n_overlap_unweighted",
    "n_overlap_weighted",
    "eligible_rows_with_response_value",
    "eligible_rows_missing_response_value",
    "emitted_association_rows",
    "association_context_status",
    "association_empty_reason",
    "created_at",
    "schema_version",
]

V550J_PATTERN_MEMBERSHIP_COLUMNS = [
    "run_id",
    "source_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "family_id",
    "pattern_id",
    "respondent_id",
    "respondent_id_norm",
    "weight_value",
    "pattern_signature",
    "answered_item_count",
    "pattern_count_unweighted",
    "pattern_count_weighted",
    "pattern_probability",
    "pattern_support_status",
    "pattern_support_gate_status",
    "created_at",
    "schema_version",
]


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


def _confidence_tier_from_score(score: Any) -> str:
    try:
        value = float(score)
    except Exception:
        return "unknown"
    if pd.isna(value):
        return "unknown"
    if value >= 75:
        return "high"
    if value >= 50:
        return "medium"
    return "low"


def _association_confidence_tier(
    *,
    pattern_confidence_score: Any,
    association_support_gate_status: Any,
    association_publication_status: Any,
    association_lane_publishability: Any,
    association_context_status: Any,
) -> str:
    tier = _confidence_tier_from_score(pattern_confidence_score)
    if tier != "low":
        return tier
    if (
        _clean(association_support_gate_status) == "sufficient_support"
        and _clean(association_publication_status) == "publishable"
        and _clean(association_lane_publishability) == "publishable_lane"
        and _clean(association_context_status) == "outside_family_context_authorized"
    ):
        return "medium"
    return tier


def _fallback_response_value(row: Any) -> str:
    for field in ("response_value_normalized", "normalized_response_label", "response_label", "value_text", "value_raw"):
        value = _clean(getattr(row, field, ""))
        if value:
            return value
    return ""


def _ensure_association_response_value_columns(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    out = frame.copy()
    if "response_value_normalized" not in out.columns:
        out["response_value_normalized"] = ""
    out["response_value_normalized"] = out["response_value_normalized"].fillna("").astype(str).str.strip()
    if "response_label" not in out.columns:
        out["response_label"] = ""
    out["response_label"] = out["response_label"].fillna("").astype(str).str.strip()
    if "normalized_response_label" not in out.columns:
        out["normalized_response_label"] = ""
    out["normalized_response_label"] = out["normalized_response_label"].fillna("").astype(str).str.strip()

    fallback_source = None
    for field in ("normalized_response_label", "response_label", "value_text", "value_raw"):
        if field in out.columns:
            series = out[field].fillna("").astype(str).str.strip()
            if series.ne("").any():
                fallback_source = series
                break
    if fallback_source is not None:
        missing_mask = out["response_value_normalized"].eq("")
        if missing_mask.any():
            out.loc[missing_mask, "response_value_normalized"] = fallback_source[missing_mask]

    missing_label_mask = out["response_label"].eq("")
    if missing_label_mask.any():
        out.loc[missing_label_mask, "response_label"] = out.loc[missing_label_mask, "response_value_normalized"]
    missing_normalized_label_mask = out["normalized_response_label"].eq("")
    if missing_normalized_label_mask.any():
        out.loc[missing_normalized_label_mask, "normalized_response_label"] = out.loc[missing_normalized_label_mask, "response_value_normalized"]
    return out


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


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        parsed = float(value)
        if math.isnan(parsed) or math.isinf(parsed):
            return None
        return parsed
    except Exception:
        return None


def _stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _first_nonempty(values: Iterable[Any], default: Any = "") -> Any:
    for value in values:
        if isinstance(value, float) and pd.isna(value):
            continue
        if value is None:
            continue
        text = str(value).strip()
        if text and text.lower() not in {"nan", "none"}:
            return value
    return default


_APPROVED_DIRECTIONALITY_AUTHORITIES = {
    "inferred_from_directionality_overlay",
    "inferred_from_response_family",
    "manually_authorized_directionality",
    "registry_resolved_directionality",
    "response_option_map_directionality",
    "v551_directionality_joined",
    "v552_pressure_directionality",
}


def _has_directionality_authority(value: Any) -> bool:
    text = _clean(value).lower()
    return bool(text and text in _APPROVED_DIRECTIONALITY_AUTHORITIES)


def _classify_target_resolution(target_entity_id: Any) -> str:
    text = _clean(target_entity_id).lower()
    if not text or text in {"unknown", "missing", "unresolved", "none"}:
        return "unresolved"
    if text.startswith("infer_"):
        return "inferred_placeholder"
    return "registry_resolved"


def _classify_target_grain(value: Any) -> str:
    text = _clean(value).lower()
    if text in {"canonical_target_entity", "target_entity", "canonical"}:
        return "canonical_target_entity"
    if text in {"condition_label", "condition"}:
        return "condition_label"
    if text in {"target_group", "group_label", "target_group_label"}:
        return "target_group"
    if text in {"permission_domain", "permission"}:
        return "permission_domain"
    if text in {"mixed", "mixed_resolution"}:
        return "mixed"
    return "unresolved"


def _looks_like_condition_label(text: str) -> bool:
    text = _clean(text).lower()
    return bool(text and text not in {"unknown", "missing", "unresolved", "none"} and not text.startswith("infer_"))


def _response_label_matches_guard(rule: dict[str, Any], response_label: str) -> bool:
    label_text = _clean(response_label).lower()
    if not label_text:
        return False
    contains_any = [_clean(value).lower() for value in (rule.get("expected_response_label_contains_any") or []) if _clean(value)]
    if contains_any and not any(token in label_text for token in contains_any):
        return False
    regex = _clean(rule.get("expected_response_label_regex"))
    if regex and re.search(regex, label_text) is None:
        return False
    return True


def _is_numeric_like_response_label(response_label: Any, response_value_normalized: Any = "") -> bool:
    label_text = _clean(response_label).lower()
    value_text = _clean(response_value_normalized).lower()
    if not label_text:
        return True
    if label_text == value_text and value_text:
        return True
    try:
        float(label_text)
        return True
    except Exception:
        return False


def _response_role_rule_guard_status(
    rule: dict[str, Any], *, wave: str, response_label: str, response_value_normalized: str
) -> tuple[bool, str]:
    validated_waves = {_clean(value) for value in (rule.get("validated_waves") or []) if _clean(value)}
    if validated_waves and wave and wave not in validated_waves:
        return False, "family_registry_rule_wave_not_validated"
    if response_label and not _is_numeric_like_response_label(response_label, response_value_normalized):
        if not _response_label_matches_guard(rule, response_label):
            return False, "family_registry_rule_label_mismatch"
        return True, "family_registry_fallback_authorized"
    if not _to_bool(rule.get("allow_unlabeled_numeric_fallback"), False):
        return False, "family_registry_rule_missing_label_guard"
    return True, "family_registry_fallback_authorized"


def _summarize_target_resolution(item_rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter()
    grain_counts = Counter()
    target_entities: set[str] = set()
    target_domains: set[str] = set()
    target_condition_labels: set[str] = set()
    target_group_labels: set[str] = set()
    permission_domains: set[str] = set()
    permission_domain_count = 0
    target_bearing_count = 0
    for item in item_rows:
        has_target = any(
            field in item
            for field in (
                "target_entity_id",
                "target_domain",
                "target_condition_label",
                "target_group_label",
                "permission_domain",
                "target_resolution_status",
                "target_resolution_grain",
            )
        )
        if not has_target:
            continue
        target_bearing_count += 1
        status = _clean(item.get("target_resolution_status"))
        grain = _classify_target_grain(item.get("target_resolution_grain"))
        if not status:
            if grain == "condition_label":
                status = "family_registry_resolved_condition"
            elif grain == "target_group":
                status = "family_registry_resolved_group"
            elif grain == "canonical_target_entity":
                status = _classify_target_resolution(item.get("target_entity_id"))
            elif _clean(item.get("target_entity_id")):
                status = _classify_target_resolution(item.get("target_entity_id"))
            else:
                status = "unresolved"
        status_counts[status] += 1
        grain_counts[grain] += 1
        target_entity = _clean(item.get("target_entity_id"))
        if target_entity:
            target_entities.add(target_entity)
        target_domain = _clean(item.get("target_domain"))
        if target_domain:
            target_domains.add(target_domain)
        target_condition_label = _clean(item.get("target_condition_label"))
        if target_condition_label:
            target_condition_labels.add(target_condition_label)
        target_group_label = _clean(item.get("target_group_label"))
        if target_group_label:
            target_group_labels.add(target_group_label)
        permission_domain = _clean(item.get("permission_domain"))
        if permission_domain:
            permission_domains.add(permission_domain)
            permission_domain_count += 1
    if target_bearing_count <= 0:
        return {
            "target_resolution_status": "no_target_items",
            "target_resolution_status_summary": {"no_target_items": 1},
            "target_resolution_grain_summary": {"no_target_items": 1},
            "target_entity_id_set": [],
            "target_domain_set": [],
            "target_condition_label_set": [],
            "target_group_label_set": [],
            "permission_domain_set": [],
            "infer_placeholder_share": 0.0,
            "registry_resolved_share": 0.0,
            "unresolved_target_share": 1.0,
            "condition_label_share": 0.0,
            "target_group_share": 0.0,
            "permission_domain_share": 0.0,
        }
    unresolved_count = status_counts.get("unresolved", 0)
    infer_count = status_counts.get("inferred_placeholder", 0)
    registry_count = status_counts.get("registry_resolved", 0)
    condition_count = grain_counts.get("condition_label", 0)
    group_count = grain_counts.get("target_group", 0)
    canonical_count = grain_counts.get("canonical_target_entity", 0)
    if unresolved_count == target_bearing_count:
        compact_status = "unresolved"
    elif condition_count == target_bearing_count:
        compact_status = "family_registry_resolved_condition"
    elif group_count == target_bearing_count:
        compact_status = "family_registry_resolved_group"
    elif canonical_count == target_bearing_count or registry_count == target_bearing_count:
        compact_status = "registry_resolved"
    else:
        compact_status = "mixed_resolution"
    return {
        "target_resolution_status": compact_status,
        "target_resolution_status_summary": {
            "registry_resolved": registry_count,
            "family_registry_resolved_condition": status_counts.get("family_registry_resolved_condition", 0),
            "family_registry_resolved_group": status_counts.get("family_registry_resolved_group", 0),
            "inferred_placeholder": infer_count,
            "unresolved": unresolved_count,
            "mixed_resolution": status_counts.get("mixed_resolution", 0),
        },
        "target_resolution_grain_summary": {
            "canonical_target_entity": canonical_count,
            "condition_label": condition_count,
            "target_group": group_count,
            "permission_domain": grain_counts.get("permission_domain", 0),
            "mixed": grain_counts.get("mixed", 0),
            "unresolved": grain_counts.get("unresolved", 0),
        },
        "target_entity_id_set": sorted(target_entities),
        "target_domain_set": sorted(target_domains),
        "target_condition_label_set": sorted(target_condition_labels),
        "target_group_label_set": sorted(target_group_labels),
        "permission_domain_set": sorted(permission_domains),
        "infer_placeholder_share": infer_count / target_bearing_count,
        "registry_resolved_share": registry_count / target_bearing_count,
        "unresolved_target_share": unresolved_count / target_bearing_count,
        "condition_label_share": condition_count / target_bearing_count,
        "target_group_share": group_count / target_bearing_count,
        "permission_domain_share": permission_domain_count / target_bearing_count,
    }


def _summarize_item_authority(item_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not item_rows:
        return {
            "directionality_status": "unknown",
            "directionality_status_summary": {"unknown": 0},
            "semantic_response_role_status": "unknown",
            "semantic_response_role_status_summary": {"unknown": 0},
            "response_semantics_authority_source": "none",
            "response_semantics_authority_source_summary": {"none": 0},
            "directionality_authority_source": "none",
            "directionality_authority_source_summary": {"none": 0},
            "directionality_basis_source": "observed_response_row",
            "directionality_basis_source_summary": {"observed_response_row": 0},
            "semantic_response_role_authority": "none",
            "semantic_role_resolved_share": 0.0,
            "semantic_role_unknown_share": 0.0,
            "directionality_authority_coverage": 0.0,
        }
    status_counts = Counter()
    directionality_status_counts = Counter()
    response_semantics_sources = Counter()
    directionality_sources = Counter()
    directionality_bases = Counter()
    resolved_count = 0
    unknown_count = 0
    authority_count = 0
    for item in item_rows:
        status = _clean(item.get("semantic_response_role_status")) or "unknown"
        directionality_status = _clean(item.get("directionality_status")) or "unknown"
        response_source = _clean(item.get("response_semantics_authority_source")) or "none"
        directionality_source = _clean(item.get("directionality_authority_source")) or "none"
        directionality_basis = _clean(item.get("directionality_basis_source")) or "observed_response_row"
        status_counts[status] += 1
        directionality_status_counts[directionality_status] += 1
        response_semantics_sources[response_source] += 1
        directionality_sources[directionality_source] += 1
        directionality_bases[directionality_basis] += 1
        if _clean(item.get("semantic_response_role")) and _clean(item.get("semantic_response_role")).lower() != "unknown":
            resolved_count += 1
        else:
            unknown_count += 1
        if directionality_source != "none" or response_source != "none":
            authority_count += 1
    total = max(1, len(item_rows))
    unique_statuses = [status for status, count in status_counts.items() if count > 0]
    if len(unique_statuses) == 1:
        compact_status = unique_statuses[0]
    elif "unknown" in status_counts and status_counts.get("unknown", 0) == total:
        compact_status = "unknown"
    else:
        compact_status = "mixed_authority"
    def _compact_source(counter: Counter) -> str:
        values = [key for key, count in counter.items() if count > 0 and key != "none"]
        if len(values) == 1:
            return values[0]
        if not values:
            return "none"
        return "mixed_authority"
    return {
        "directionality_status": _compact_source(directionality_status_counts),
        "directionality_status_summary": dict(directionality_status_counts),
        "semantic_response_role_status": compact_status,
        "semantic_response_role_status_summary": dict(status_counts),
        "response_semantics_authority_source": _compact_source(response_semantics_sources),
        "response_semantics_authority_source_summary": dict(response_semantics_sources),
        "directionality_authority_source": _compact_source(directionality_sources),
        "directionality_authority_source_summary": dict(directionality_sources),
        "directionality_basis_source": _compact_source(directionality_bases),
        "directionality_basis_source_summary": dict(directionality_bases),
        "semantic_response_role_authority": _compact_source(response_semantics_sources),
        "semantic_role_resolved_share": resolved_count / total,
        "semantic_role_unknown_share": unknown_count / total,
        "directionality_authority_coverage": authority_count / total,
    }


def _normalize_semantic_response(direction: Any, polarity: Any = "", label: Any = "", directionality_authority: Any = False) -> str:
    if not _has_directionality_authority(directionality_authority):
        label_text = _clean(label).lower()
        if any(token in label_text for token in {"neutral", "ambivalent", "dk", "don't know", "na", "iap"}):
            return "neutral"
        return "unknown"
    direction_text = " ".join([_clean(direction).lower(), _clean(polarity).lower()])
    label_text = _clean(label).lower()
    if direction_text and any(token in direction_text for token in {"more approving", "more endorsing", "allow_directionality", "positive", "support"}):
        return "support"
    if direction_text and any(token in direction_text for token in {"more disapproving", "more rejecting", "negative", "oppose", "disallow_directionality"}):
        return "oppose"
    if any(token in label_text for token in {"neutral", "ambivalent", "dk", "don't know", "na", "iap"}) or any(
        token in direction_text for token in {"neutral", "ambivalent", "dk", "don't know", "na", "iap"}
    ):
        return "neutral"
    return "unknown"


def _resolve_family_item_semantics(
    row: pd.Series,
    *,
    family_cfg: dict[str, Any],
    item_meta: dict[str, Any],
) -> dict[str, Any]:
    var_code = _clean(row.get("var_code")).upper()
    item_role = _clean(item_meta.get("item_role") or row.get("item_role") or "target_case")
    condition_label = _clean(item_meta.get("condition_label") or row.get("condition_label"))
    response_value_normalized = _clean(row.get("response_value_normalized"))
    response_label = _clean(row.get("response_label") or row.get("normalized_response_label") or row.get("value_label_clean"))
    response_direction = _clean(row.get("response_direction"))
    polarity = _clean(row.get("polarity"))
    upstream_directionality_status = _clean(row.get("directionality_status")) or "unknown"
    upstream_semantics_source = _clean(row.get("response_semantics_source")) or "observed_response_row"
    response_semantics_status = _clean(row.get("response_semantics_status")) or "observed_only"
    response_semantics_source = upstream_semantics_source
    response_semantics_contract_hash = _clean(row.get("response_semantics_contract_hash"))
    upstream_response_authority = _to_bool(row.get("response_option_map_matched"), False) and upstream_semantics_source == "response_option_map"
    directionality_authority_source = "none"
    response_semantics_authority_source = "none"
    directionality_basis_source = "observed_response_row"
    semantic_response_role = "unknown"
    semantic_response_role_status = "missing_or_unsigned_directionality_authority"

    if upstream_response_authority and _has_directionality_authority(upstream_directionality_status):
        semantic_response_role = _normalize_semantic_response(response_direction, polarity, response_label, upstream_directionality_status)
        directionality_authority_source = "response_option_map"
        response_semantics_authority_source = "response_option_map"
        directionality_basis_source = "response_option_map"
        response_semantics_source = "response_option_map"
        response_semantics_status = "curated"
        if semantic_response_role in {"support", "oppose"}:
            semantic_response_role_status = "directionality_authorized"
        elif semantic_response_role == "neutral":
            semantic_response_role_status = "neutral_directionality_status"
        else:
            semantic_response_role_status = "missing_or_unsigned_directionality_authority"
    else:
        fallback_rule, fallback_guard_status = _matching_response_role_rule(
            family_cfg,
            item_role=item_role,
            var_code=var_code,
            condition_label=condition_label,
            wave=_clean(row.get("wave")) or _clean(row.get("canonical_wave")),
            response_label=response_label,
            response_value_normalized=response_value_normalized,
        )
        if fallback_rule:
            semantic_response_role = _clean(fallback_rule.get("semantic_response_role")) or semantic_response_role
            response_direction = _clean(fallback_rule.get("response_direction")) or (
                "positive" if semantic_response_role == "support" else "negative" if semantic_response_role == "oppose" else "neutral"
            )
            polarity = _clean(fallback_rule.get("polarity")) or (
                "positive" if semantic_response_role == "support" else "negative" if semantic_response_role == "oppose" else "neutral"
            )
            upstream_directionality_status = _clean(fallback_rule.get("directionality_status")) or "manually_authorized_directionality"
            directionality_authority_source = "question_family_registry.response_role_rules"
            response_semantics_authority_source = "question_family_registry.response_role_rules"
            fallback_basis_source = _clean(fallback_rule.get("directionality_authority_source"))
            if fallback_basis_source in {
                "response_option_map",
                "response_option_map_directionality",
                "v551_directionality_joined",
                "v552_pressure_directionality",
                "registry_resolved_directionality",
                "inferred_from_directionality_overlay",
                "inferred_from_response_family",
                "manually_authorized_directionality",
            }:
                directionality_basis_source = fallback_basis_source
            else:
                directionality_basis_source = _clean(fallback_rule.get("numeric_fallback_authority")) or _clean(fallback_rule.get("codebook_contract_id"))
            response_semantics_source = "question_family_registry.response_role_rules"
            response_semantics_status = "registry_resolved"
            semantic_response_role_status = fallback_guard_status if fallback_guard_status and fallback_guard_status != "family_registry_fallback_authorized" else "family_registry_fallback_authorized"
        else:
            directionality_authority_source = "none"
            response_semantics_authority_source = "none"
            directionality_basis_source = "observed_response_row"
            semantic_response_role = "unknown"
            semantic_response_role_status = fallback_guard_status or "missing_or_unsigned_directionality_authority"

    target_entity_id = _clean(row.get("target_entity_id"))
    target_domain = _clean(row.get("target_domain"))
    target_condition_label = _clean(row.get("target_condition_label")) or condition_label
    target_group_label = _clean(row.get("target_group_label"))
    permission_domain = _clean(row.get("permission_domain"))
    target_resolution_grain = _classify_target_grain(row.get("target_resolution_grain"))
    target_resolution_status = _clean(row.get("target_resolution_status")) or _classify_target_resolution(target_entity_id)
    target_resolution_authority_source = _clean(row.get("target_resolution_authority_source")) or _clean(row.get("source_structure_source")) or _clean(row.get("response_semantics_source")) or "upstream_mapping"
    target_resolution_basis_source = _clean(row.get("target_resolution_basis_source")) or _clean(row.get("source_structure_source")) or _clean(row.get("response_semantics_source")) or "upstream_mapping"
    target_rule = _matching_target_resolution_rule(
        family_cfg,
        item_role=item_role,
        var_code=var_code,
        condition_label=condition_label,
    )
    if target_rule:
        authority_source = _clean(target_rule.get("target_resolution_authority_source")) or "question_family_registry.target_resolution_rules"
        basis_source = _clean(target_rule.get("target_resolution_basis_source")) or "question_family_registry.item_role_groups"
        target_resolution_authority_source = authority_source
        target_resolution_basis_source = basis_source
        target_entity_from = _clean(target_rule.get("target_entity_from"))
        target_condition_from = _clean(target_rule.get("target_condition_label_from")) or ("condition_label" if target_entity_from in {"condition_label", "fixed"} else "")
        target_group_from = _clean(target_rule.get("target_group_label_from"))
        target_entity_template = _clean(target_rule.get("target_entity_template"))
        fixed_target_entity = _clean(target_rule.get("target_entity_id"))
        if fixed_target_entity:
            target_entity_id = fixed_target_entity
        elif target_entity_template and condition_label:
            target_entity_id = target_entity_template.format(condition_label=condition_label)
        elif target_entity_from == "condition_label" and condition_label:
            target_entity_id = condition_label
        if target_condition_from == "condition_label":
            target_condition_label = condition_label
        if target_group_from == "condition_label":
            target_group_label = condition_label
        target_domain = _clean(target_rule.get("target_domain")) or target_domain
        permission_domain = _clean(target_rule.get("permission_domain")) or permission_domain
        target_resolution_grain = _classify_target_grain(target_rule.get("target_resolution_grain")) or target_resolution_grain
        target_resolution_status = _clean(target_rule.get("target_resolution_status")) or (
            "family_registry_resolved_condition" if target_resolution_grain == "condition_label" else "family_registry_resolved_group" if target_resolution_grain == "target_group" else "registry_resolved"
        )
    elif target_entity_id:
        target_resolution_grain = "canonical_target_entity"
        target_resolution_status = _classify_target_resolution(target_entity_id)
        target_resolution_authority_source = _clean(row.get("source_structure_source")) or _clean(row.get("response_semantics_source")) or "upstream_mapping"
        target_resolution_basis_source = _clean(row.get("source_structure_source")) or _clean(row.get("response_semantics_source")) or "upstream_mapping"

    return {
        "response_direction": response_direction,
        "polarity": polarity,
        "directionality_status": upstream_directionality_status,
        "directionality_authority_source": directionality_authority_source,
        "directionality_basis_source": directionality_basis_source,
        "response_semantics_authority_source": response_semantics_authority_source,
        "semantic_response_role": semantic_response_role,
        "semantic_response_role_authority": response_semantics_authority_source,
        "semantic_response_role_status": semantic_response_role_status,
        "response_semantics_status": response_semantics_status,
        "response_semantics_source": response_semantics_source,
        "response_semantics_contract_hash": response_semantics_contract_hash,
        "target_entity_id": target_entity_id,
        "target_domain": target_domain,
        "target_condition_label": target_condition_label,
        "target_group_label": target_group_label,
        "permission_domain": permission_domain,
        "target_resolution_grain": target_resolution_grain,
        "target_resolution_status": target_resolution_status,
        "target_resolution_authority_source": target_resolution_authority_source,
        "target_resolution_basis_source": target_resolution_basis_source,
    }


def _weighted_mean(values: list[float], weights: list[float] | None = None) -> float | None:
    if not values:
        return None
    if weights is None:
        return sum(values) / len(values)
    if len(values) != len(weights) or not weights:
        return None
    total_weight = sum(weights)
    if total_weight <= 0:
        return None
    return sum(value * weight for value, weight in zip(values, weights)) / total_weight


def _weight_metrics(weights: list[float | None]) -> dict[str, Any]:
    total = len(weights)
    observed_nonnull = [w for w in weights if w is not None]
    observed_positive = [w for w in observed_nonnull if w > 0]
    nonnull_ratio = (len([w for w in weights if w is not None]) / total) if total else 0.0
    positive_ratio = (len(observed_positive) / len(observed_nonnull)) if observed_nonnull else 0.0
    if not observed_nonnull:
        variability_score = 0.0
        concentration_risk = 1.0
        effective_n = 0.0
        effective_n_ratio = 0.0
        weighted_count_validation_passed = False
        weight_status = "weights_missing"
        weighted_count_basis = "unweighted_fallback"
        n_weighted = float(total)
    elif any(w <= 0 for w in observed_nonnull if w is not None):
        variability_score = 0.0
        concentration_risk = 1.0
        effective_n = 0.0
        effective_n_ratio = 0.0
        weighted_count_validation_passed = False
        weight_status = "weights_invalid"
        weighted_count_basis = "unweighted_fallback"
        n_weighted = float(total)
    elif len(observed_nonnull) < total:
        mean = sum(observed_positive) / len(observed_positive)
        variance = sum((w - mean) ** 2 for w in observed_positive) / len(observed_positive)
        cv = math.sqrt(variance) / mean if mean > 0 else 0.0
        variability_score = 1.0 / (1.0 + cv)
        sum_w = sum(observed_positive)
        sum_w_sq = sum(w * w for w in observed_positive)
        concentration_risk = min(1.0, max(0.0, sum_w_sq / (sum_w * sum_w))) if sum_w > 0 else 1.0
        effective_n = effective_n_v1(sum_w, sum_w_sq) or 0.0
        effective_n_ratio = effective_n_ratio_v1(effective_n, total) or 0.0
        weighted_count_validation_passed = False
        weight_status = "weighted_partial"
        weighted_count_basis = "weighted_partial"
        n_weighted = float(sum(observed_positive)) if observed_positive else float(total)
    else:
        mean = sum(observed_positive) / len(observed_positive)
        variance = sum((w - mean) ** 2 for w in observed_positive) / len(observed_positive)
        cv = math.sqrt(variance) / mean if mean > 0 else 0.0
        variability_score = 1.0 / (1.0 + cv)
        sum_w = sum(observed_positive)
        sum_w_sq = sum(w * w for w in observed_positive)
        concentration_risk = min(1.0, max(0.0, sum_w_sq / (sum_w * sum_w))) if sum_w > 0 else 1.0
        effective_n = effective_n_v1(sum_w, sum_w_sq) or 0.0
        effective_n_ratio = effective_n_ratio_v1(effective_n, total) or 0.0
        weighted_count_validation_passed = bool(observed_nonnull and len(observed_nonnull) == total and all(w > 0 for w in observed_nonnull))
        weight_status = "weighted_valid" if weighted_count_validation_passed else "weighted_partial"
        weighted_count_basis = weight_status
        n_weighted = float(sum(observed_positive)) if observed_positive else float(len(weights))
    validity_score = weight_validity_score_v1(
        nonnull_ratio,
        positive_ratio,
        variability_score,
        concentration_risk,
        effective_n_ratio,
    )
    return {
        "weight_status": weight_status,
        "weight_nonnull_ratio": nonnull_ratio,
        "weight_positive_ratio": positive_ratio,
        "weight_variability_score": variability_score,
        "weight_concentration_risk_score": concentration_risk,
        "effective_n": effective_n,
        "effective_n_ratio": effective_n_ratio,
        "weight_validity_score": validity_score if validity_score is not None else 0.0,
        "weighted_count_validation_passed": weighted_count_validation_passed,
        "weighted_count_basis": weighted_count_basis,
        "n_weighted": n_weighted,
    }


def _combine_weight_statuses(statuses: Iterable[Any]) -> str:
    cleaned = [_clean(status).lower() for status in statuses if _clean(status)]
    if not cleaned:
        return "unweighted_only"
    if any(status == "weights_invalid" for status in cleaned):
        return "weights_invalid"
    if any(status == "weights_missing" for status in cleaned):
        return "weights_missing"
    if any(status == "weighted_partial" for status in cleaned):
        return "weighted_partial"
    if any(status == "weighted_valid" for status in cleaned) and any(status == "unweighted_only" for status in cleaned):
        return "weighted_partial"
    if any(status == "weighted_valid" for status in cleaned):
        return "weighted_valid"
    return "unweighted_only"


def _formula_provenance(prefix: str, formula_id: str, formula_version: str, implementation_function: str, score_family: str, higher_is_better: bool, decision_role: str) -> dict[str, Any]:
    return {
        f"{prefix}_formula_id": formula_id,
        f"{prefix}_formula_version": formula_version,
        f"{prefix}_implementation_function": implementation_function,
        f"{prefix}_score_family": score_family,
        f"{prefix}_higher_is_better": higher_is_better,
        f"{prefix}_decision_role": decision_role,
    }


def _family_item_map(family_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    role_groups = family_cfg.get("item_role_groups", {}) or {}
    for item_role, item_rows in role_groups.items():
        for item in item_rows or []:
            item_code = _clean(item.get("var_code"))
            if not item_code:
                continue
            normalized_item = dict(item)
            normalized_item.update(
                {
                    "var_code": item_code,
                    "item_role": _clean(item_role) or "target_case",
                    "condition_label": _clean(item.get("condition_label")),
                }
            )
            items.append(normalized_item)
    return items


def _family_item_lookup(family_cfg: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["var_code"].upper(): item for item in _family_item_map(family_cfg)}


def _family_item_order(family_cfg: dict[str, Any]) -> list[str]:
    return [item["var_code"].upper() for item in _family_item_map(family_cfg)]


def _pattern_membership_lookup(
    pattern_df: pd.DataFrame,
    *,
    pattern_membership_frame: pd.DataFrame | None = None,
) -> dict[str, set[str]]:
    lookup: dict[str, set[str]] = {}
    if pattern_membership_frame is not None and not pattern_membership_frame.empty and "pattern_id" in pattern_membership_frame.columns:
        respondent_column = "respondent_id"
        if respondent_column not in pattern_membership_frame.columns and "respondent_id_norm" in pattern_membership_frame.columns:
            respondent_column = "respondent_id_norm"
        if respondent_column in pattern_membership_frame.columns:
            grouped = pattern_membership_frame.groupby("pattern_id", observed=True, sort=False)
            for pattern_id, group in grouped:
                lookup[str(pattern_id)] = { _clean(value) for value in group[respondent_column].dropna().astype(str).tolist() if _clean(value) }
            return lookup
    if pattern_df.empty or "pattern_id" not in pattern_df.columns or "respondent_ids" not in pattern_df.columns:
        return lookup
    for pattern in pattern_df.itertuples(index=False):
        lookup[str(getattr(pattern, "pattern_id", ""))] = {str(rid) for rid in getattr(pattern, "respondent_ids", []) if _clean(rid)}
    return lookup


def _pattern_membership_rows(
    respondent_df: pd.DataFrame,
    pattern_df: pd.DataFrame,
    *,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
) -> pd.DataFrame:
    if respondent_df.empty or pattern_df.empty:
        return pd.DataFrame(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)
    respondent_cols = [column for column in ["respondent_id", "respondent_id_norm", "pattern_signature_raw", "pattern_signature_semantic", "weight_value", "n_items_answered", "source", "source_id", "wave", "canonical_wave", "country_code"] if column in respondent_df.columns]
    pattern_cols = [column for column in ["pattern_id", "family_id", "pattern_signature_raw", "pattern_signature_semantic", "pattern_count_unweighted", "pattern_count_weighted", "pattern_probability", "support_status", "support_gate_status", "source", "source_id", "wave", "canonical_wave", "country_code"] if column in pattern_df.columns]
    merge_keys = [column for column in ["pattern_signature_raw", "pattern_signature_semantic"] if column in respondent_cols and column in pattern_cols]
    if not merge_keys:
        merge_keys = []
    if merge_keys:
        merged = respondent_df[respondent_cols].merge(
            pattern_df[pattern_cols],
            on=merge_keys,
            how="inner",
            suffixes=("", "_pattern"),
        )
    else:
        merged = pd.DataFrame()
    if merged.empty and "respondent_id" in respondent_df.columns and "respondent_ids" in pattern_df.columns:
        rows: list[dict[str, Any]] = []
        respondent_lookup: dict[str, pd.Series] = {}
        for responder_id, responder_group in respondent_df.groupby("respondent_id", sort=False):
            if responder_group.empty:
                continue
            respondent_lookup[str(responder_id)] = responder_group.iloc[0]
        for pattern in pattern_df.itertuples(index=False):
            for member_id in getattr(pattern, "respondent_ids", []) or []:
                respondent_row = respondent_lookup.get(str(member_id))
                if respondent_row is None:
                    continue
                rows.append(
                    {
                        "run_id": _clean(getattr(pattern, "run_id", "")) or _clean(run_id),
                        "source_id": _clean(getattr(pattern, "source_id", "")) or _clean(source_id) or _clean(source),
                        "source": _clean(getattr(pattern, "source", "")) or _clean(source),
                        "wave": _clean(getattr(pattern, "wave", "")) or _clean(wave),
                        "canonical_wave": _clean(getattr(pattern, "canonical_wave", "")) or _clean(canonical_wave) or _clean(wave),
                        "country_code": _clean(getattr(pattern, "country_code", "")) or _clean(country_code),
                        "family_id": _clean(getattr(pattern, "family_id", "")),
                        "pattern_id": _clean(getattr(pattern, "pattern_id", "")),
                        "respondent_id": _clean(member_id),
                        "respondent_id_norm": _clean(getattr(respondent_row, "respondent_id_norm", "")) or _clean(member_id),
                        "weight_value": _safe_float(getattr(respondent_row, "weight_value", None)) or 0.0,
                        "pattern_signature": _clean(getattr(pattern, "pattern_signature_raw", "")) or _clean(getattr(pattern, "pattern_signature_semantic", "")) or _clean(getattr(pattern, "pattern_id", "")),
                        "answered_item_count": int(_safe_float(getattr(respondent_row, "n_items_answered", None)) or 0),
                        "pattern_count_unweighted": int(_safe_float(getattr(pattern, "pattern_count_unweighted", None)) or 0),
                        "pattern_count_weighted": _safe_float(getattr(pattern, "pattern_count_weighted", None)) or 0.0,
                        "pattern_probability": _safe_float(getattr(pattern, "pattern_probability", None)) or 0.0,
                        "pattern_support_status": _clean(getattr(pattern, "support_status", "")),
                        "pattern_support_gate_status": _clean(getattr(pattern, "support_gate_status", "")),
                        "created_at": utc_now(),
                        "schema_version": V550J_SCHEMA_VERSION,
                    }
                )
        membership_df = pd.DataFrame(rows)
        if membership_df.empty:
            return pd.DataFrame(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)
        return membership_df.reindex(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)
    if merged.empty:
        return pd.DataFrame(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)
    rows: list[dict[str, Any]] = []
    for row in merged.itertuples(index=False):
        rows.append(
            {
                "run_id": _clean(getattr(row, "run_id", "")) or _clean(getattr(row, "run_id_pattern", "")) or _clean(run_id),
                "source_id": _clean(getattr(row, "source_id", "")) or _clean(getattr(row, "source_id_pattern", "")) or _clean(source_id) or _clean(source),
                "source": _clean(getattr(row, "source", "")) or _clean(getattr(row, "source_pattern", "")) or _clean(source),
                "wave": _clean(getattr(row, "wave", "")) or _clean(getattr(row, "wave_pattern", "")) or _clean(wave),
                "canonical_wave": _clean(getattr(row, "canonical_wave", "")) or _clean(getattr(row, "canonical_wave_pattern", "")) or _clean(canonical_wave) or _clean(wave),
                "country_code": _clean(getattr(row, "country_code", "")) or _clean(getattr(row, "country_code_pattern", "")) or _clean(country_code),
                "family_id": _clean(getattr(row, "family_id", "")),
                "pattern_id": _clean(getattr(row, "pattern_id", "")),
                "respondent_id": _clean(getattr(row, "respondent_id", "")),
                "respondent_id_norm": _clean(getattr(row, "respondent_id_norm", "")) or _clean(getattr(row, "respondent_id", "")),
                "weight_value": _safe_float(getattr(row, "weight_value", None)) or 0.0,
                "pattern_signature": _clean(getattr(row, "pattern_signature_raw", "")) or _clean(getattr(row, "pattern_signature_semantic", "")),
                "answered_item_count": int(_safe_float(getattr(row, "n_items_answered", None)) or 0),
                "pattern_count_unweighted": int(_safe_float(getattr(row, "pattern_count_unweighted", None)) or 0),
                "pattern_count_weighted": _safe_float(getattr(row, "pattern_count_weighted", None)) or 0.0,
                "pattern_probability": _safe_float(getattr(row, "pattern_probability", None)) or 0.0,
                "pattern_support_status": _clean(getattr(row, "support_status", "")),
                "pattern_support_gate_status": _clean(getattr(row, "support_gate_status", "")),
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    membership_df = pd.DataFrame(rows)
    if membership_df.empty:
        return pd.DataFrame(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)
    return membership_df.reindex(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS)


def _family_response_role_rules(family_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    rules = family_cfg.get("response_role_rules", []) or []
    return [rule for rule in rules if isinstance(rule, dict)]


def _family_target_resolution_rules(family_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    rules = family_cfg.get("target_resolution_rules", []) or []
    return [rule for rule in rules if isinstance(rule, dict)]


def _rule_applies_to_item(rule: dict[str, Any], *, item_role: str, var_code: str, condition_label: str) -> bool:
    allowed_roles = {_clean(value).lower() for value in (rule.get("applies_to_roles") or []) if _clean(value)}
    if allowed_roles and item_role.lower() not in allowed_roles:
        return False
    rule_item_role = _clean(rule.get("item_role")).lower()
    if rule_item_role and rule_item_role != item_role.lower():
        return False
    rule_var_code = _clean(rule.get("var_code")).upper()
    if rule_var_code and rule_var_code != var_code.upper():
        return False
    rule_condition_label = _clean(rule.get("condition_label")).lower()
    if rule_condition_label and rule_condition_label != condition_label.lower():
        return False
    return True


def _matching_response_role_rule(
    family_cfg: dict[str, Any],
    *,
    item_role: str,
    var_code: str,
    condition_label: str,
    wave: str,
    response_label: str,
    response_value_normalized: str,
) -> tuple[dict[str, Any] | None, str]:
    response_value = _clean(response_value_normalized)
    if not response_value:
        return None, "family_registry_rule_missing_label_guard"
    first_guard_status = "missing_or_unsigned_directionality_authority"
    for rule in _family_response_role_rules(family_cfg):
        rule_value = _clean(rule.get("response_value_normalized") or rule.get("response_value") or rule.get("value"))
        if rule_value and rule_value != response_value:
            continue
        if _rule_applies_to_item(rule, item_role=item_role, var_code=var_code, condition_label=condition_label):
            allowed, guard_status = _response_role_rule_guard_status(
                rule,
                wave=wave,
                response_label=response_label,
                response_value_normalized=response_value,
            )
            if allowed:
                return rule, guard_status
            first_guard_status = guard_status
    return None, first_guard_status


def _matching_target_resolution_rule(
    family_cfg: dict[str, Any],
    *,
    item_role: str,
    var_code: str,
    condition_label: str,
) -> dict[str, Any] | None:
    for rule in _family_target_resolution_rules(family_cfg):
        if _rule_applies_to_item(rule, item_role=item_role, var_code=var_code, condition_label=condition_label):
            return rule
    return None


def _family_boundary_rules(family_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    rules = family_cfg.get("boundary_rules", []) or []
    return [rule for rule in rules if isinstance(rule, dict)]


def _evaluate_boundary_rules(
    family_cfg: dict[str, Any],
    semantic_counts: Counter[str],
    item_rows: list[dict[str, Any]],
) -> tuple[str, dict[str, Any]]:
    support_count = semantic_counts.get("support", 0)
    oppose_count = semantic_counts.get("oppose", 0)
    neutral_count = semantic_counts.get("neutral", 0)
    unknown_count = semantic_counts.get("unknown", 0)
    total = support_count + oppose_count + neutral_count + unknown_count
    diagnostics: dict[str, Any] = {}
    if total <= 0:
        return "mixed_unclassified", {
            "rules_evaluated": [],
            "rules_matched": [],
            "rules_failed": [],
            "boundary_rule_failure_reasons": {},
            "boundary_rule_evaluation_summary": {},
            "boundary_rule_authority_source": "question_family_registry.boundary_rules",
            "boundary_rule_status": "mixed_unclassified",
        }
    support_share = support_count / total
    oppose_share = oppose_count / total
    role_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in item_rows:
        role_counts[_clean(item.get("item_role", ""))][_clean(item.get("semantic_response_role", ""))] += 1
    evaluated_rules: list[str] = []
    matched_rules: list[str] = []
    failed_rules: list[str] = []
    failure_reasons: dict[str, str] = {}
    for idx, rule in enumerate(_family_boundary_rules(family_cfg), start=1):
        boundary_type = _clean(rule.get("boundary_pattern_type"))
        if not boundary_type:
            continue
        rule_name = _clean(rule.get("rule_id")) or _clean(rule.get("boundary_rule_id")) or f"{boundary_type}_{idx}"
        evaluated_rules.append(rule_name)
        diagnostics_entry = {
            "boundary_pattern_type": boundary_type,
            "matched": False,
            "required_conditions_met": [],
            "required_conditions_missing": [],
            "failure_reason": "",
        }
        require_all = rule.get("require_all", []) or []
        require_any = rule.get("require_any", []) or []
        support_roles = [_clean(value) for value in (rule.get("support_roles") or []) if _clean(value)]
        oppose_roles = [_clean(value) for value in (rule.get("oppose_roles") or []) if _clean(value)]
        support_share_min = _safe_float(rule.get("support_share_min"))
        support_share_max = _safe_float(rule.get("support_share_max"))
        oppose_share_min = _safe_float(rule.get("oppose_share_min"))
        oppose_share_max = _safe_float(rule.get("oppose_share_max"))
        require_distinct_condition_labels = _to_bool(rule.get("require_distinct_condition_labels"), False)
        failure_reason = ""
        if support_share_min is not None and support_share < support_share_min:
            failure_reason = "support_share_below_min"
        elif support_share_max is not None and support_share > support_share_max:
            failure_reason = "support_share_above_max"
        elif oppose_share_min is not None and oppose_share < oppose_share_min:
            failure_reason = "oppose_share_below_min"
        elif oppose_share_max is not None and oppose_share > oppose_share_max:
            failure_reason = "oppose_share_above_max"
        if not support_roles:
            support_roles = [
                _clean(requirement.get("role") or requirement.get("item_role"))
                for requirement in require_all
                if isinstance(requirement, dict) and _clean(requirement.get("semantic_response_role") or requirement.get("response_role") or requirement.get("value")) == "support"
            ]
            support_roles = [role for role in support_roles if role]
        if not oppose_roles:
            oppose_roles = [
                _clean(requirement.get("role") or requirement.get("item_role"))
                for requirement in require_all
                if isinstance(requirement, dict) and _clean(requirement.get("semantic_response_role") or requirement.get("response_role") or requirement.get("value")) == "oppose"
            ]
            oppose_roles = [role for role in oppose_roles if role]
        if not failure_reason:
            for requirement in require_all:
                if not isinstance(requirement, dict):
                    continue
                role = _clean(requirement.get("role") or requirement.get("item_role") or requirement.get("support_role") or requirement.get("oppose_role"))
                required_role = _clean(requirement.get("semantic_response_role") or requirement.get("response_role") or requirement.get("value"))
                min_share = _safe_float(requirement.get("min_share"))
                min_count = _safe_float(requirement.get("min_count"))
                role_counts_for_role = role_counts.get(role, Counter()) if role else Counter()
                role_total = sum(role_counts_for_role.values()) if role_counts_for_role else 0
                if required_role and role_counts_for_role.get(required_role, 0) <= 0:
                    failure_reason = f"missing_{role}_{required_role}"
                    diagnostics_entry["required_conditions_missing"].append(f"{role}:{required_role}")
                    break
                if min_count is not None and role_counts_for_role.get(required_role or "support", 0) < min_count:
                    failure_reason = f"below_min_count_{role}"
                    diagnostics_entry["required_conditions_missing"].append(f"{role}:min_count")
                    break
                if min_share is not None and role_total > 0 and role_counts_for_role.get(required_role or "support", 0) / role_total < min_share:
                    failure_reason = f"below_min_share_{role}"
                    diagnostics_entry["required_conditions_missing"].append(f"{role}:min_share")
                    break
                diagnostics_entry["required_conditions_met"].append(f"{role}:{required_role or 'any'}")
        if not failure_reason and require_distinct_condition_labels:
            support_labels = {
                _clean(item.get("condition_label"))
                for item in item_rows
                if _clean(item.get("semantic_response_role")) == "support"
                and (not support_roles or _clean(item.get("item_role")) in support_roles)
                and _clean(item.get("condition_label"))
            }
            oppose_labels = {
                _clean(item.get("condition_label"))
                for item in item_rows
                if _clean(item.get("semantic_response_role")) == "oppose"
                and (not oppose_roles or _clean(item.get("item_role")) in oppose_roles)
                and _clean(item.get("condition_label"))
            }
            if not support_labels or not oppose_labels or support_labels & oppose_labels:
                failure_reason = "not_distinct_condition_labels"
        if not failure_reason and require_any:
            any_satisfied = False
            for requirement in require_any:
                if not isinstance(requirement, dict):
                    continue
                role = _clean(requirement.get("role") or requirement.get("item_role"))
                required_role = _clean(requirement.get("semantic_response_role") or requirement.get("response_role") or requirement.get("value"))
                if not role:
                    continue
                if required_role and role_counts.get(role, Counter()).get(required_role, 0) > 0:
                    any_satisfied = True
                    diagnostics_entry["required_conditions_met"].append(f"{role}:{required_role}")
                    break
            if not any_satisfied:
                failure_reason = "require_any_not_satisfied"
        if not failure_reason and support_roles and not any(role_counts[role].get("support", 0) > 0 for role in support_roles):
            failure_reason = "missing_support_role"
        if not failure_reason and oppose_roles and not any(role_counts[role].get("oppose", 0) > 0 for role in oppose_roles):
            failure_reason = "missing_oppose_role"
        if failure_reason:
            diagnostics_entry["failure_reason"] = failure_reason
            diagnostics_entry["required_conditions_missing"] = diagnostics_entry["required_conditions_missing"] or [failure_reason]
            failed_rules.append(rule_name)
            failure_reasons[rule_name] = failure_reason
        else:
            diagnostics_entry["matched"] = True
            diagnostics_entry["failure_reason"] = ""
            matched_rules.append(rule_name)
            diagnostics[rule_name] = diagnostics_entry
            return boundary_type, {
                "rules_evaluated": evaluated_rules,
                "rules_matched": matched_rules,
                "rules_failed": failed_rules,
                "boundary_rule_failure_reasons": failure_reasons,
                "boundary_rule_evaluation_summary": {**diagnostics, rule_name: diagnostics_entry},
                "boundary_rule_authority_source": "question_family_registry.boundary_rules",
                "boundary_rule_status": boundary_type,
            }
        diagnostics[rule_name] = diagnostics_entry
    return "mixed_unclassified", {
        "rules_evaluated": evaluated_rules,
        "rules_matched": matched_rules,
        "rules_failed": failed_rules,
        "boundary_rule_failure_reasons": failure_reasons,
        "boundary_rule_evaluation_summary": diagnostics,
        "boundary_rule_authority_source": "question_family_registry.boundary_rules",
        "boundary_rule_status": "mixed_unclassified",
    }


def _association_authority_status(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "missing_context_frame"
    authority_columns = [
        "is_substantive",
        "allowed_as_association_feature",
        "allowed_as_attitude_cloud_feature",
    ]
    if not any(column in frame.columns for column in authority_columns):
        return "missing_association_authority"
    if "is_substantive" in frame.columns and frame["is_substantive"].map(lambda value: _to_bool(value, False)).any():
        return "has_association_authority"
    if "allowed_as_association_feature" in frame.columns and frame["allowed_as_association_feature"].map(lambda value: _to_bool(value, False)).any():
        return "has_association_authority"
    if "allowed_as_attitude_cloud_feature" in frame.columns and frame["allowed_as_attitude_cloud_feature"].map(lambda value: _to_bool(value, False)).any():
        return "has_association_authority"
    return "missing_association_authority"


def _association_authority_mask(frame: pd.DataFrame) -> pd.Series:
    if frame.empty:
        return pd.Series(dtype="bool")
    mask = pd.Series(False, index=frame.index)
    for column in ("is_substantive", "allowed_as_association_feature", "allowed_as_attitude_cloud_feature"):
        if column in frame.columns:
            mask = mask | frame[column].map(lambda value: _to_bool(value, False))
    return mask


def _boundary_pattern_type(
    family_cfg: dict[str, Any],
    semantic_counts: Counter[str],
    item_rows: list[dict[str, Any]],
) -> str:
    boundary_type, _ = _evaluate_boundary_rules(family_cfg, semantic_counts, item_rows)
    return boundary_type


_BLOCKED_ASSOCIATION_SEMANTIC_ROLES = {
    "metadata",
    "context",
    "context_only",
    "accepted_context_only",
    "demographic",
    "administrative",
    "admin",
    "design",
    "position",
    "position_context",
    "position_coordinate",
    "respondent_metadata",
    "non_substantive",
}

_BLOCKED_ASSOCIATION_CLASSIFICATIONS = {
    "metadata",
    "context",
    "context_only",
    "position",
    "position_context",
    "administrative",
    "admin",
    "design",
    "forbidden",
    "non_substantive",
}


def _association_row_status(row: Any) -> tuple[str, str]:
    semantic_role = _clean(getattr(row, "semantic_role", "")).lower()
    source_classification = _clean(getattr(row, "source_structure_classification", "")).lower()
    not_direct_evidence = _to_bool(getattr(row, "not_direct_evidence", False), False)
    allowed_association = _to_bool(getattr(row, "allowed_as_association_feature", False), False)
    allowed_cloud = _to_bool(getattr(row, "allowed_as_attitude_cloud_feature", False), False)
    is_substantive = _to_bool(getattr(row, "is_substantive", False), False)
    if semantic_role in _BLOCKED_ASSOCIATION_SEMANTIC_ROLES or source_classification in _BLOCKED_ASSOCIATION_CLASSIFICATIONS:
        return "blocked_metadata_context", "blocked_metadata_context"
    if not_direct_evidence:
        if allowed_association:
            return "eligible_diagnostic_association", "not_direct_evidence"
        return "blocked_not_direct_evidence", "not_direct_evidence"
    if is_substantive or allowed_association or allowed_cloud:
        return "eligible", "direct_or_not_flagged"
    return "blocked_missing_authority", "direct_or_not_flagged"


def get_associated_var_code(record: Any) -> str:
    for key in (
        "associated_var_code",
        "associated_variable_code",
        "var_code_norm",
        "var_code",
        "variable_code",
        "question_id",
    ):
        try:
            value = record.get(key) if hasattr(record, "get") else getattr(record, key, None)
        except Exception:
            value = None
        if value is not None and str(value).strip():
            return str(value).strip().upper()
    return ""


def classify_association_lane(
    *,
    associated_var_code: str,
    source_structure_classification: str | None = None,
    semantic_role: str | None = None,
    direct_evidence_status: str | None = None,
    question_type: str | None = None,
    response_semantics_status: str | None = None,
    registry_override: str | None = None,
    associated_var_distinct_response_count: int = 0,
    registry: Any = None,
    source: str = "",
    wave: str = "",
    country_code: str = "",
) -> tuple[str, str, str]:
    """Return (lane, lane_status, rule_id). rule_id is empty when not from registry."""
    if registry_override and str(registry_override).strip():
        lane = str(registry_override).strip()
        return lane, "registry_override", ""
    var_code = _clean(associated_var_code).upper()
    source_classification = _clean(source_structure_classification).lower()
    semantic_role_text = _clean(semantic_role).lower()
    question_type_text = _clean(question_type).lower()
    response_semantics_text = _clean(response_semantics_status).lower()
    gss_legacy_adapter = canonical_family_key(source) == "gss"

    if not var_code:
        return "unknown_association_lane", "missing_associated_var_code", ""

    # YAML registry check (before hardcoded sets)
    if isinstance(registry, AssociationLaneRegistry):
        reg_result = registry.classify(var_code, source, wave, country_code)
        if reg_result is not None:
            lane = reg_result.lane
            if reg_result.match_type == "exact":
                status = "exact_registry"
            elif reg_result.match_type == "prefix":
                status = "prefix_registry"
            else:
                status = "exact_registry"
            return lane, status, reg_result.rule_id
    if source_classification in {"administrative", "admin", "sample", "metadata", "blocked_metadata", "survey_admin"} or (gss_legacy_adapter and var_code in _ADMINISTRATIVE_ASSOCIATION_CODES):
        return "blocked_metadata_context", "blocked_metadata_rule", ""
    if direct_evidence_status == "not_direct_evidence":
        return "diagnostic_numeric_context", "diagnostic", ""
    if (gss_legacy_adapter and var_code in _IDENTITY_ASSOCIATION_CODES) or source_classification in {"identity", "identity_coordinate", "demographic", "respondent_metadata"} or semantic_role_text in {"identity", "identity_coordinate"}:
        return "identity_coordinate_association", "var_code_rule", ""
    if _is_raw_occupational_status_code(var_code) or source_classification in {"occupational", "occupation", "occupation_status"} or semantic_role_text in {"occupational_status", "occupation", "occupation_status"}:
        return "occupational_status_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _OCCUPATIONAL_ASSOCIATION_CODES:
        return "occupational_status_association", "var_code_rule", ""
    if (gss_legacy_adapter and var_code in _FAMILY_BACKGROUND_ASSOCIATION_CODES) or source_classification in {"family_background", "parental_background", "education_background"} or semantic_role_text in {"family_background", "parental_background"}:
        return "family_background_association", "var_code_rule", ""
    if (gss_legacy_adapter and var_code in _LIFE_COURSE_ASSOCIATION_CODES) or source_classification in {"life_course", "life_course_context"} or semantic_role_text in {"life_course", "life_course_context"}:
        return "life_course_context_association", "var_code_rule", ""
    if (gss_legacy_adapter and var_code in _INSTITUTIONAL_ASSOCIATION_CODES) or source_classification in {"institutional", "institutional_context"} or semantic_role_text in {"institutional", "institutional_context"}:
        return "institutional_context_association", "var_code_rule", ""
    if (gss_legacy_adapter and var_code in _POSITION_ASSOCIATION_CODES) or source_classification in {"position", "position_context", "position_coordinate"} or semantic_role_text in {"position", "position_coordinate", "position_context"}:
        return "position_context_association", "var_code_rule", ""
    if (gss_legacy_adapter and var_code in _STATUS_ASSOCIATION_CODES) or source_classification in {"status", "status_code", "class", "socioeconomic_status"} or semantic_role_text in {"status", "status_code"}:
        return "status_code_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _POLITICAL_BEHAVIOR_ASSOCIATION_CODES:
        return "political_behavior_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _MEDIA_EXPOSURE_ASSOCIATION_CODES:
        return "media_exposure_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _HEALTH_STATUS_CONTEXT_ASSOCIATION_CODES:
        return "health_status_context_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _RESIDENCE_ORIGIN_CONTEXT_ASSOCIATION_CODES:
        return "residence_origin_context_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _FAMILY_DEMOGRAPHIC_CONTEXT_ASSOCIATION_CODES:
        return "family_demographic_context_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _SATISFACTION_CONTEXT_ASSOCIATION_CODES:
        return "satisfaction_context_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _LANGUAGE_CULTURAL_CONTEXT_ASSOCIATION_CODES:
        return "language_cultural_context_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _POLITICAL_ORIENTATION_ASSOCIATION_CODES:
        return "political_orientation_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _RELIGIOUS_ORIENTATION_ASSOCIATION_CODES:
        return "religious_orientation_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _ECONOMIC_POLICY_ATTITUDE_ASSOCIATION_CODES:
        return "economic_policy_attitude_association", "var_code_rule", ""
    if gss_legacy_adapter and var_code in _SUBSTANTIVE_ATTITUDE_ASSOCIATION_CODES:
        return "substantive_attitude_association", "var_code_rule", ""
    if associated_var_distinct_response_count > 25:
        return "diagnostic_numeric_context", "high_cardinality_safety_rule", ""
    if response_semantics_text in {"observed_only", "family_registry_authorized", "family_registry_fallback_authorized"}:
        if question_type_text in {"attitude", "opinion", "belief", "preference", "issue"}:
            return "substantive_attitude_association", "response_semantics_question_type_rule", ""
        if semantic_role_text in {"attitude", "opinion", "belief", "preference", "relation_evidence"}:
            return "substantive_attitude_association", "response_semantics_semantic_role_rule", ""
        if question_type_text in {"single_choice", "multiple_choice", "open_text"} and semantic_role_text not in {"identity", "occupational_status", "position_coordinate"}:
            return "unknown_association_lane", "observed_response_semantics_insufficient_for_lane", ""
        return "unknown_association_lane", "observed_response_semantics_insufficient_for_lane", ""
    _context_suffixes = ("STAT", "HOUR", "HRS", "SUP", "SUPS", "SUB", "SUBS", "SLF", "DAY", "DAYS", "TAG", "TAGS")
    _context_prefixes = ("MA", "PA", "SP")
    if var_code and (var_code.endswith(_context_suffixes) or (len(var_code) >= 4 and var_code[:2] in _context_prefixes and var_code[2:].endswith(_context_suffixes))):
        return "unknown_association_lane", "context_suffix_rule", ""
    if question_type_text in {"attitude", "opinion", "belief", "preference", "issue"}:
        return "substantive_attitude_association", "question_type_rule", ""
    if semantic_role_text in {"attitude", "opinion", "belief", "preference", "relation_evidence"} and source_classification not in {"administrative", "metadata"}:
        return "substantive_attitude_association", "semantic_role_rule", ""
    if var_code and any(ch.isdigit() for ch in var_code) and not semantic_role_text in {"attitude", "opinion", "belief", "preference", "issue"}:
        return "unknown_association_lane", "source_structure_rule", ""
    if var_code and any(ch.isdigit() for ch in var_code):
        return "diagnostic_numeric_context", "source_structure_rule", ""
    return "unknown_association_lane", "unknown_no_rule", ""


_RESOLUTION_TYPE_MAP: dict[str, str] = {
    "registry_override": "manual_override_review_only",
    "exact_registry": "exact_registry",
    "prefix_registry": "prefix_registry",
    "var_code_rule": "legacy_family_adapter",
    "blocked_metadata_rule": "blocked",
    "diagnostic": "blocked",
    "blocked": "blocked",
    "high_cardinality_safety_rule": "cardinality_gate",
    "context_suffix_rule": "source_structure",
    "question_type_rule": "semantic_role",
    "semantic_role_rule": "semantic_role",
    "response_semantics_question_type_rule": "semantic_role",
    "response_semantics_semantic_role_rule": "semantic_role",
    "source_structure_rule": "source_structure",
    "observed_response_semantics_insufficient_for_lane": "semantic_role_insufficient",
    "missing_associated_var_code": "fallback",
    "unknown_no_rule": "fallback",
}


def _association_lane_resolution_type(association_lane_status: str) -> str:
    status = str(association_lane_status).strip().lower()
    return _RESOLUTION_TYPE_MAP.get(status, "fallback")


_AUTHORITY_STATUS_MAP: dict[str, str] = {
    "exact_registry": "registry_authoritative",
    "prefix_registry": "registry_authoritative",
    "manual_override_review_only": "manual_review_required",
    "legacy_family_adapter": "legacy_adapter_review_only",
    "blocked": "blocked",
    "cardinality_gate": "policy_gate",
    "semantic_role": "response_semantics_computed",
    "source_structure": "heuristic_computed",
    "semantic_role_insufficient": "heuristic_insufficient",
    "fallback": "heuristic_insufficient",
}


def _association_lane_authority_status(association_lane_status: str) -> str:
    res_type = _association_lane_resolution_type(association_lane_status)
    return _AUTHORITY_STATUS_MAP.get(res_type, "unknown_authority")


def _association_lane_override(
    association_lane_overrides: dict[str, Any] | None,
    associated_var_code: str,
) -> tuple[str, str]:
    if not association_lane_overrides:
        return "", ""
    var_code = _clean(associated_var_code).upper()
    if not var_code:
        return "", ""
    override = association_lane_overrides.get(var_code) or association_lane_overrides.get(var_code.lower())
    if override is None:
        return "", ""
    if isinstance(override, dict):
        lane = _clean(override.get("association_lane"))
        basis = _clean(override.get("basis")) or _clean(override.get("association_lane_basis"))
        return lane, basis
    return _clean(override), ""


def _association_lane(
    row: Any,
    row_status: str,
    direct_evidence_status: str,
    *,
    registry: Any = None,
    source: str = "",
    wave: str = "",
    country_code: str = "",
) -> tuple[str, str, str]:
    if row_status == "blocked_metadata_context":
        return "blocked_metadata_context", "blocked", ""
    if row_status == "blocked_not_direct_evidence":
        return "blocked_metadata_context", "blocked", ""
    if row_status == "blocked_missing_authority":
        return "blocked_metadata_context", "blocked", ""
    if row_status == "eligible_diagnostic_association" or direct_evidence_status == "not_direct_evidence":
        return "diagnostic_numeric_context", "diagnostic", ""
    associated_var_code = get_associated_var_code(row)
    lane, lane_status, rule_id = classify_association_lane(
        associated_var_code=associated_var_code,
        source_structure_classification=getattr(row, "source_structure_classification", ""),
        semantic_role=getattr(row, "semantic_role", ""),
        direct_evidence_status=direct_evidence_status,
        question_type=getattr(row, "question_type", ""),
        response_semantics_status=getattr(row, "response_semantics_status", ""),
        registry_override=getattr(row, "association_lane_override", ""),
        registry=registry,
        source=source,
        wave=wave,
        country_code=country_code,
    )
    if lane == "unknown_association_lane" and any(ch.isdigit() for ch in associated_var_code):
        return "diagnostic_numeric_context", "diagnostic", ""
    return lane, lane_status, rule_id


def _association_support_threshold(override: Any = None) -> int:
    parsed = pd.to_numeric(pd.Series([override]), errors="coerce").iloc[0]
    if pd.isna(parsed):
        return int(DEFAULT_SUPPORT_FLOOR)
    return max(int(DEFAULT_SUPPORT_FLOOR), int(parsed))


def _association_publication_status(
    *,
    support_gate_status: str,
    association_lane: str,
    association_lane_status: str = "",
    row_status: str,
    direct_evidence_status: str,
    is_same_variable: bool = False,
    is_same_family: bool = False,
    is_raw_occupational: bool = False,
    is_high_cardinality: bool = False,
    is_sparse_response: bool = False,
    n_overlap_unweighted: int = 0,
    association_support_threshold: int = 5,
    associated_var_distinct_response_count: int = 0,
    associated_response_total_n: int = 0,
    association_support_n_unweighted: int = 0,
    pattern_member_n_unweighted: int = 0,
    association_support_ratio: float = 0.0,
    difference_from_baseline: float = 0.0,
    publishable_lanes: set[str] | None = None,
) -> tuple[str, str, bool]:
    publishable_lanes = {str(value).strip() for value in (publishable_lanes or {"substantive_attitude_association"}) if str(value).strip()}
    resolution_type = _association_lane_resolution_type(association_lane_status)

    # Precedence order: earlier checks override later ones
    if row_status == "blocked_metadata_context":
        return "blocked_metadata_context", "metadata/context/admin-only rows are not publishable", False
    if row_status == "blocked_missing_authority":
        return "blocked_missing_authority", "missing association authority", False
    if row_status == "blocked_not_direct_evidence":
        return "blocked_not_direct_evidence", "not_direct_evidence rows are not publishable", False
    if is_same_variable:
        return "blocked_same_variable_leakage", "same-variable association is not publishable", False
    if is_same_family:
        return "blocked_same_family_leakage", "same-family association is not publishable", False
    if is_raw_occupational:
        return "diagnostic_only_raw_occupational_code", "raw occupational/status/code is diagnostic-only", False

    # The governed lane defines the publication class. Sparse/high-cardinality
    # modifiers remain available as diagnostic fields, but they must not erase
    # the fact that a row belongs to a diagnostic-only lane.
    if association_lane not in publishable_lanes:
        if association_lane in {"unknown_association_lane", "diagnostic_numeric_context", "administrative_context"}:
            return "diagnostic_only_raw_component", f"lane={association_lane} is diagnostic-only", False
        return "diagnostic_only_raw_component", f"lane={association_lane} is not enabled for publication", False

    # For a publication-capable lane, support is the first material gate.
    # Cardinality/sparsity remain explicit fields and only become the primary
    # status after the row has enough overlap to be evaluated for publication.
    if support_gate_status == "zero_overlap":
        return "blocked_low_support", "zero overlap", False
    if support_gate_status in {"below_threshold", "missing_denominator"}:
        return "diagnostic_only_low_overlap", "below publishable support threshold", False

    if is_high_cardinality:
        return "diagnostic_only_high_cardinality", f"high-cardinality associated var ({associated_var_distinct_response_count} distinct values) is diagnostic-only", False
    if is_sparse_response:
        return "diagnostic_only_sparse_response", f"sparse associated response (total_n={associated_response_total_n}) is diagnostic-only", False

    if direct_evidence_status == "not_direct_evidence":
        return "blocked_not_direct_evidence", "not_direct_evidence rows are not publishable", False

    # Registry authority governs publication-capable lanes. Diagnostic lanes have
    # already exited above and retain their diagnostic status even when no lane
    # registry rule exists.
    if resolution_type not in {"exact_registry", "prefix_registry"}:
        return (
            "reviewable_missing_registry_authority",
            f"association lane resolution {resolution_type or 'missing'} is not registry authority",
            False,
        )

    # Multi-condition publication gate
    if n_overlap_unweighted < association_support_threshold:
        return "reviewable_low_support", f"n_overlap={n_overlap_unweighted} below publishable threshold={association_support_threshold}", False
    if association_support_n_unweighted < 5:
        return "reviewable_low_support", f"support_n={association_support_n_unweighted} below minimum 5", False
    if pattern_member_n_unweighted < 20:
        return "reviewable_low_support", f"pattern_n={pattern_member_n_unweighted} below minimum 20", False
    if associated_response_total_n < 20:
        return "reviewable_low_support", f"response_total_n={associated_response_total_n} below minimum 20", False
    if association_support_ratio < 0.03:
        return "reviewable_low_support", f"support_ratio={association_support_ratio:.3f} below minimum 0.03", False
    if abs(difference_from_baseline) < 0.10:
        return "reviewable_low_support", f"|diff|={abs(difference_from_baseline):.3f} below minimum 0.10", False

    return "publishable", "cleared all publication gates", True


def _bool_series(frame: pd.DataFrame, column: str, default: bool = False) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index)
    return frame[column].map(lambda value: _to_bool(value, default))


def _association_publication_mask(
    frame: pd.DataFrame,
    *,
    publishable_lanes: set[str] | None = None,
) -> pd.Series:
    if frame.empty:
        return pd.Series(False, index=frame.index)
    support_gate_column = "association_support_gate_status" if "association_support_gate_status" in frame.columns else "support_gate_status" if "support_gate_status" in frame.columns else None
    required_columns = {
        "association_publication_status",
        "association_lane_publishability",
        "association_lane",
        "association_lane_resolution_type",
        "association_lane_rule_id",
        "association_support_n_unweighted",
        "association_support_threshold",
        "associated_response_total_n",
        "associated_var_distinct_response_count",
        "is_high_cardinality_associated_var",
        "is_sparse_associated_response",
        "is_raw_occupational_status_code",
        "is_same_family_association",
        "is_same_variable_association",
        "pattern_member_n_unweighted",
    }
    if support_gate_column is None or not required_columns.issubset(set(frame.columns)):
        return pd.Series(False, index=frame.index)
    publishable_lanes = {str(value).strip() for value in (publishable_lanes or {"substantive_attitude_association"}) if str(value).strip()}
    support_n = pd.to_numeric(frame["association_support_n_unweighted"], errors="coerce").fillna(-1)
    support_threshold = pd.to_numeric(frame["association_support_threshold"], errors="coerce").fillna(0)
    pattern_n = pd.to_numeric(frame["pattern_member_n_unweighted"], errors="coerce").fillna(0)
    response_total_n = pd.to_numeric(frame["associated_response_total_n"], errors="coerce").fillna(0)
    distinct_count = pd.to_numeric(frame["associated_var_distinct_response_count"], errors="coerce").fillna(0)
    support_ratio = pd.to_numeric(frame.get("association_support_ratio", pd.Series(0.0, index=frame.index)), errors="coerce").fillna(0.0)
    diff = pd.to_numeric(frame.get("difference_from_baseline", pd.Series(0.0, index=frame.index)), errors="coerce").fillna(0.0)
    return (
        frame["association_publication_status"].astype(str).eq("publishable")
        & _bool_series(frame, "would_emit_as_publishable", False)
        & frame[support_gate_column].astype(str).eq("sufficient_support")
        & frame["association_lane_publishability"].astype(str).eq("publishable_lane")
        & frame["association_lane"].astype(str).isin(publishable_lanes)
        & frame["association_lane_resolution_type"].astype(str).isin({"exact_registry", "prefix_registry"})
        & frame["association_lane_rule_id"].fillna("").astype(str).str.strip().ne("")
        & ~_bool_series(frame, "is_same_variable_association", False)
        & ~_bool_series(frame, "is_same_family_association", False)
        & ~_bool_series(frame, "is_raw_occupational_status_code", False)
        & ~_bool_series(frame, "is_high_cardinality_associated_var", False)
        & ~_bool_series(frame, "is_sparse_associated_response", False)
        & support_n.ge(support_threshold)
        & support_n.ge(5)
        & pattern_n.ge(20)
        & response_total_n.ge(20)
        & distinct_count.le(10)
        & support_ratio.ge(0.03)
        & diff.abs().ge(0.10)
    )


def _validate_association_index_publication_constraints(
    frame: pd.DataFrame,
    *,
    publishable_lanes: set[str] | None = None,
) -> None:
    if frame.empty:
        return
    required_columns = {
        "run_id",
        "source_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "family_id",
        "pattern_id",
        "association_publication_status",
        "association_support_gate_status",
        "association_lane_publishability",
        "association_lane",
        "association_support_n_unweighted",
        "association_support_threshold",
    }
    missing_columns = sorted(required_columns.difference(set(frame.columns)))
    if missing_columns:
        raise RuntimeError(f"joint_pattern_association_index missing required columns: {', '.join(missing_columns)}")
    publication_mask = _association_publication_mask(frame, publishable_lanes=publishable_lanes)
    invalid = frame[~publication_mask].copy()
    if invalid.empty:
        blank_identity_columns = [column for column in ["source", "wave", "canonical_wave", "country_code", "family_id", "pattern_id"] if column in frame.columns]
        if blank_identity_columns:
            blank_identity_mask = frame[blank_identity_columns].fillna("").astype(str).eq("").any(axis=1)
            if bool(blank_identity_mask.any()):
                raise RuntimeError(f"joint_pattern_association_index contains blank identity fields ({int(blank_identity_mask.sum())})")
        _known_context_codes = {
            "PADEG", "MADEG", "SPDEG", "PAEDUC", "MAEDUC", "SPEDUC",
            "WRKSTAT", "WORKHR", "SPHOUR", "SPWRKSTA", "SPWRKSLF", "PAWRKSLF",
            "WKSUP", "WKSUPS", "WKSUB", "WKSUBS", "WORKDY", "SPDAYS",
            "INDSTATUS", "MAINDSTATUS", "SPINDSTATUS", "PAINDSTATUS",
            "INDTAG", "MAINDTAG", "SPINDTAG", "PAINDTAG",
            "OCCSTATUS", "MAOCCSTATUS", "SPOCCSTATUS", "PAOCCSTATUS",
            "OCCTAG", "MAOCCTAG", "SPOCCTAG", "PAOCCTAG",
        }
        if "associated_var_code" in frame.columns:
            attitude = frame[frame["association_lane"].astype(str).eq("substantive_attitude_association")] if "association_lane" in frame.columns else frame
            known_context_in_index = attitude[attitude["associated_var_code"].astype(str).str.upper().str.strip().isin(_known_context_codes)]
            if not known_context_in_index.empty:
                context_vars = sorted(known_context_in_index["associated_var_code"].astype(str).str.upper().str.strip().unique())
                raise RuntimeError(f"joint_pattern_association_index contains known context variables classified as substantive_attitude_association: {context_vars}")
        return
    problems = {
        "non_publishable_status": int((invalid["association_publication_status"].astype(str) != "publishable").sum()),
        "bad_support_gate": int((invalid["association_support_gate_status"].astype(str) != "sufficient_support").sum()),
        "bad_lane_publishability": int((invalid["association_lane_publishability"].astype(str) != "publishable_lane").sum()),
        "lane_not_enabled": int((~invalid["association_lane"].astype(str).isin({str(value).strip() for value in (publishable_lanes or {"substantive_attitude_association"}) if str(value).strip()})).sum()),
        "support_below_threshold": int((pd.to_numeric(invalid["association_support_n_unweighted"], errors="coerce").fillna(-1) < pd.to_numeric(invalid["association_support_threshold"], errors="coerce").fillna(0)).sum()),
    }
    detail = ", ".join(f"{key}={value}" for key, value in problems.items() if value)
    raise RuntimeError(f"joint_pattern_association_index violates publication constraints ({len(invalid)} rows){(': ' + detail) if detail else ''}")


def _association_eligibility_funnel(
    *,
    family_cfg: dict[str, Any],
    respondent_df: pd.DataFrame,
    context_frame: pd.DataFrame | None,
    family_var_codes: set[str],
    association_index: pd.DataFrame,
    candidate_trace: pd.DataFrame | None = None,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
) -> pd.DataFrame:
    if context_frame is None or context_frame.empty or "var_code" not in context_frame.columns:
        return pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "source_id": source_id,
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "family_id": family_cfg["family_id"],
                    "outside_family_rows_total": 0,
                    "outside_family_rows_with_respondent_overlap": 0,
                    "outside_family_rows_with_positive_authority": 0,
                    "outside_family_rows_blocked_metadata_context": 0,
                    "outside_family_rows_blocked_not_direct_evidence": 0,
                    "outside_family_rows_blocked_missing_authority": 0,
                    "eligible_association_rows": 0,
                    "eligible_association_var_count": 0,
                    "eligible_association_var_codes": [],
                    "association_lane_summary": {},
                    "emitted_association_rows": int(len(association_index)),
                    "association_context_status": "association_context_unavailable",
                    "association_empty_reason": "association_context_unavailable",
                    "created_at": utc_now(),
                    "schema_version": V550J_SCHEMA_VERSION,
                }
            ]
        )
    outside_family_context = context_frame.copy()
    if "var_code" in outside_family_context.columns:
        outside_family_context = outside_family_context[~outside_family_context["var_code"].astype(str).str.upper().isin({str(code).upper() for code in family_var_codes})].copy()
    if outside_family_context.empty:
        return pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "source_id": source_id,
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "family_id": family_cfg["family_id"],
                    "outside_family_rows_total": 0,
                    "outside_family_rows_with_respondent_overlap": 0,
                    "outside_family_rows_with_positive_authority": 0,
                    "outside_family_rows_blocked_metadata_context": 0,
                    "outside_family_rows_blocked_not_direct_evidence": 0,
                    "outside_family_rows_blocked_missing_authority": 0,
                    "eligible_association_rows": 0,
                    "eligible_association_var_count": 0,
                    "eligible_association_var_codes": [],
                    "association_lane_summary": {},
                    "emitted_association_rows": int(len(association_index)),
                    "association_context_status": "association_context_unavailable",
                    "association_empty_reason": "no_outside_family_rows",
                    "created_at": utc_now(),
                    "schema_version": V550J_SCHEMA_VERSION,
                }
            ]
        )
    respondent_ids = {str(value) for value in respondent_df.get("respondent_id", pd.Series(dtype="object")).dropna().astype(str).tolist()} if not respondent_df.empty and "respondent_id" in respondent_df.columns else set()
    overlap_mask = outside_family_context["respondent_id"].astype(str).isin(respondent_ids) if respondent_ids and "respondent_id" in outside_family_context.columns else pd.Series(False, index=outside_family_context.index)
    positive_authority_mask = _association_authority_mask(outside_family_context)
    blocked_metadata_mask = pd.Series(False, index=outside_family_context.index)
    if "semantic_role" in outside_family_context.columns:
        blocked_metadata_mask = blocked_metadata_mask | outside_family_context["semantic_role"].astype(str).str.lower().isin(_BLOCKED_ASSOCIATION_SEMANTIC_ROLES)
    if "source_structure_classification" in outside_family_context.columns:
        blocked_metadata_mask = blocked_metadata_mask | outside_family_context["source_structure_classification"].astype(str).str.lower().isin(_BLOCKED_ASSOCIATION_CLASSIFICATIONS)
    blocked_not_direct_mask = pd.Series(False, index=outside_family_context.index)
    if "not_direct_evidence" in outside_family_context.columns:
        not_direct_mask = outside_family_context["not_direct_evidence"].map(lambda value: _to_bool(value, False))
        assoc_mask = (
            outside_family_context["allowed_as_association_feature"].map(lambda value: _to_bool(value, False))
            if "allowed_as_association_feature" in outside_family_context.columns
            else pd.Series(False, index=outside_family_context.index)
        )
        blocked_not_direct_mask = not_direct_mask & ~assoc_mask
    blocked_missing_authority_mask = ~(blocked_metadata_mask | blocked_not_direct_mask | positive_authority_mask)
    eligible_mask = positive_authority_mask & ~blocked_metadata_mask & ~blocked_not_direct_mask
    eligible_rows_count = int(eligible_mask.sum()) if hasattr(eligible_mask, "sum") else 0
    emitted_rows = int(len(association_index))
    candidate_pairs_formed = int(candidate_trace.attrs.get("candidate_pairs_formed", 0) if candidate_trace is not None else 0)
    candidate_pairs_published = int(candidate_trace.attrs.get("candidate_pairs_published", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_missing_response_value = int(candidate_trace.attrs.get("candidate_pairs_suppressed_missing_response_value", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_no_candidate_pairs_formed = int(candidate_trace.attrs.get("candidate_pairs_suppressed_no_candidate_pairs_formed", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_no_pattern_member_overlap = int(candidate_trace.attrs.get("candidate_pairs_suppressed_no_pattern_member_overlap", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_low_response_overlap = int(candidate_trace.attrs.get("candidate_pairs_suppressed_low_response_overlap", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_low_baseline = int(candidate_trace.attrs.get("candidate_pairs_suppressed_low_baseline", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_low_pattern_support = int(candidate_trace.attrs.get("candidate_pairs_suppressed_low_pattern_support", 0) if candidate_trace is not None else 0)
    candidate_pairs_suppressed_effect_size_zero_or_trivial = int(candidate_trace.attrs.get("candidate_pairs_suppressed_effect_size_zero_or_trivial", 0) if candidate_trace is not None else 0)
    eligible_rows_with_response_value = int(candidate_trace.attrs.get("eligible_rows_with_response_value", eligible_rows_count) if candidate_trace is not None else eligible_rows_count)
    eligible_rows_missing_response_value = int(candidate_trace.attrs.get("eligible_rows_missing_response_value", 0) if candidate_trace is not None else 0)
    association_mode = _clean(candidate_trace.attrs.get("association_mode", "") if candidate_trace is not None else "")
    if association_mode in {"off", "funnel_only"} and emitted_rows == 0:
        empty_reason = "association_mode_disabled" if association_mode == "off" else "association_mode_funnel_only"
        association_context_status = "outside_family_context_authorized" if not blocked_missing_authority_mask.all() else "association_context_authority_missing"
        eligible_var_codes = sorted({_clean(value).upper() for value in outside_family_context.loc[eligible_mask, "var_code"].tolist() if _clean(value)})
        return pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "source_id": source_id,
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "family_id": family_cfg["family_id"],
                    "outside_family_rows_total": int(len(outside_family_context)),
                    "outside_family_rows_with_respondent_overlap": int(overlap_mask.sum()) if hasattr(overlap_mask, "sum") else 0,
                    "outside_family_rows_with_positive_authority": int(positive_authority_mask.sum()) if hasattr(positive_authority_mask, "sum") else 0,
                    "outside_family_rows_blocked_metadata_context": int(blocked_metadata_mask.sum()) if hasattr(blocked_metadata_mask, "sum") else 0,
                    "outside_family_rows_blocked_not_direct_evidence": int(blocked_not_direct_mask.sum()) if hasattr(blocked_not_direct_mask, "sum") else 0,
                    "outside_family_rows_blocked_missing_authority": int(blocked_missing_authority_mask.sum()) if hasattr(blocked_missing_authority_mask, "sum") else 0,
                    "eligible_association_rows": eligible_rows_count,
                    "eligible_association_var_count": int(len(eligible_var_codes)),
                    "eligible_association_var_codes": eligible_var_codes,
                    "association_lane_summary": {},
                    "candidate_pairs_formed": candidate_pairs_formed,
                    "candidate_pairs_published": candidate_pairs_published,
                    "candidate_pairs_suppressed_missing_response_value": candidate_pairs_suppressed_missing_response_value,
                    "candidate_pairs_suppressed_no_candidate_pairs_formed": candidate_pairs_suppressed_no_candidate_pairs_formed,
                    "candidate_pairs_suppressed_no_pattern_member_overlap": candidate_pairs_suppressed_no_pattern_member_overlap,
                    "candidate_pairs_suppressed_low_response_overlap": candidate_pairs_suppressed_low_response_overlap,
                    "candidate_pairs_suppressed_low_baseline": candidate_pairs_suppressed_low_baseline,
                    "candidate_pairs_suppressed_low_pattern_support": candidate_pairs_suppressed_low_pattern_support,
                    "candidate_pairs_suppressed_effect_size_zero_or_trivial": candidate_pairs_suppressed_effect_size_zero_or_trivial,
                    "pattern_var_answered_n_unweighted": candidate_pairs_formed,
                    "pattern_var_answered_n_weighted": candidate_pairs_formed,
                    "pattern_answered_var_n_unweighted": candidate_pairs_formed,
                    "pattern_answered_var_n_weighted": candidate_pairs_formed,
                    "n_overlap_unweighted": int(candidate_trace["n_overlap_unweighted"].sum()) if candidate_trace is not None and not candidate_trace.empty and "n_overlap_unweighted" in candidate_trace.columns else 0,
                    "n_overlap_weighted": float(candidate_trace["n_overlap_weighted"].sum()) if candidate_trace is not None and not candidate_trace.empty and "n_overlap_weighted" in candidate_trace.columns else 0.0,
                    "eligible_rows_with_response_value": eligible_rows_with_response_value,
                    "eligible_rows_missing_response_value": eligible_rows_missing_response_value,
                    "emitted_association_rows": int(len(association_index)),
                    "association_context_status": association_context_status,
                    "association_empty_reason": empty_reason,
                    "created_at": utc_now(),
                    "schema_version": V550J_SCHEMA_VERSION,
                }
            ]
        )
    if emitted_rows > 0:
        empty_reason = "not_empty"
        association_context_status = "outside_family_context_authorized"
    elif blocked_metadata_mask.all():
        empty_reason = "all_rows_blocked_metadata_context"
        association_context_status = "association_context_unavailable"
    elif blocked_not_direct_mask.all():
        empty_reason = "all_rows_blocked_not_direct_evidence"
        association_context_status = "association_context_unavailable"
    elif blocked_missing_authority_mask.all():
        empty_reason = "association_context_authority_missing"
        association_context_status = "association_context_authority_missing"
    elif candidate_pairs_formed > 0 and candidate_pairs_published == 0:
        if candidate_pairs_suppressed_low_response_overlap > 0 or candidate_pairs_suppressed_low_pattern_support > 0 or candidate_pairs_suppressed_low_baseline > 0 or candidate_pairs_suppressed_effect_size_zero_or_trivial > 0:
            empty_reason = "eligible_rows_below_support_threshold"
        elif candidate_pairs_suppressed_missing_response_value > 0 or eligible_rows_with_response_value <= 0:
            empty_reason = "no_response_overlap"
        elif candidate_pairs_suppressed_no_pattern_member_overlap > 0:
            empty_reason = "no_respondent_overlap"
        else:
            empty_reason = "eligible_rows_below_support_threshold"
        association_context_status = "outside_family_context_authorized"
    elif candidate_pairs_formed <= 0 and eligible_rows_with_response_value <= 0:
        empty_reason = "no_response_overlap"
        association_context_status = "outside_family_context_authorized"
    elif candidate_pairs_formed <= 0:
        empty_reason = "no_candidate_pairs_formed"
        association_context_status = "outside_family_context_authorized"
    elif overlap_mask.any() and emitted_rows == 0:
        empty_reason = "no_response_overlap"
        association_context_status = "outside_family_context_authorized"
    else:
        empty_reason = "no_respondent_overlap"
        association_context_status = "outside_family_context_authorized"
    eligible_var_codes = sorted({_clean(value).upper() for value in outside_family_context.loc[eligible_mask, "var_code"].tolist() if _clean(value)})
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "source_id": source_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "family_id": family_cfg["family_id"],
                "outside_family_rows_total": int(len(outside_family_context)),
                "outside_family_rows_with_respondent_overlap": int(overlap_mask.sum()) if hasattr(overlap_mask, "sum") else 0,
                "outside_family_rows_with_positive_authority": int(positive_authority_mask.sum()) if hasattr(positive_authority_mask, "sum") else 0,
                "outside_family_rows_blocked_metadata_context": int(blocked_metadata_mask.sum()) if hasattr(blocked_metadata_mask, "sum") else 0,
                "outside_family_rows_blocked_not_direct_evidence": int(blocked_not_direct_mask.sum()) if hasattr(blocked_not_direct_mask, "sum") else 0,
                "outside_family_rows_blocked_missing_authority": int(blocked_missing_authority_mask.sum()) if hasattr(blocked_missing_authority_mask, "sum") else 0,
                "eligible_association_rows": eligible_rows_count,
                "eligible_association_var_count": int(len(eligible_var_codes)),
                "eligible_association_var_codes": eligible_var_codes,
                "association_lane_summary": dict(Counter(candidate_trace["association_lane"].astype(str))) if candidate_trace is not None and not candidate_trace.empty and "association_lane" in candidate_trace.columns else {},
                "candidate_pairs_formed": candidate_pairs_formed,
                "candidate_pairs_published": candidate_pairs_published,
                "candidate_pairs_suppressed_missing_response_value": candidate_pairs_suppressed_missing_response_value,
                "candidate_pairs_suppressed_no_candidate_pairs_formed": candidate_pairs_suppressed_no_candidate_pairs_formed,
                "candidate_pairs_suppressed_no_pattern_member_overlap": candidate_pairs_suppressed_no_pattern_member_overlap,
                "candidate_pairs_suppressed_low_response_overlap": candidate_pairs_suppressed_low_response_overlap,
                "candidate_pairs_suppressed_low_baseline": candidate_pairs_suppressed_low_baseline,
                "candidate_pairs_suppressed_low_pattern_support": candidate_pairs_suppressed_low_pattern_support,
                "candidate_pairs_suppressed_effect_size_zero_or_trivial": candidate_pairs_suppressed_effect_size_zero_or_trivial,
                "pattern_var_answered_n_unweighted": candidate_pairs_formed,
                "pattern_var_answered_n_weighted": candidate_pairs_formed,
                "pattern_answered_var_n_unweighted": candidate_pairs_formed,
                "pattern_answered_var_n_weighted": candidate_pairs_formed,
                "n_overlap_unweighted": int(candidate_trace["n_overlap_unweighted"].sum()) if candidate_trace is not None and not candidate_trace.empty and "n_overlap_unweighted" in candidate_trace.columns else 0,
                "n_overlap_weighted": float(candidate_trace["n_overlap_weighted"].sum()) if candidate_trace is not None and not candidate_trace.empty and "n_overlap_weighted" in candidate_trace.columns else 0.0,
                "eligible_rows_with_response_value": eligible_rows_with_response_value,
                "eligible_rows_missing_response_value": eligible_rows_missing_response_value,
                "emitted_association_rows": int(len(association_index)),
                "association_context_status": association_context_status,
                "association_empty_reason": empty_reason,
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        ]
    )


def _empty_association_index() -> pd.DataFrame:
    return pd.DataFrame(columns=V550J_ASSOCIATION_INDEX_COLUMNS)


def _empty_association_review_surface() -> pd.DataFrame:
    return pd.DataFrame(columns=V550J_ASSOCIATION_REVIEW_SURFACE_COLUMNS)


def _empty_meaning_summary() -> pd.DataFrame:
    return pd.DataFrame(columns=V550J_MEANING_SUMMARY_COLUMNS)


def _association_lane_publishability(association_lane: str) -> str:
    lane = _clean(association_lane)
    if lane == "substantive_attitude_association":
        return "publishable_lane"
    if lane == "exclude_from_lane":
        return "never_publishable"
    if lane in {
        "identity_coordinate_association",
        "position_context_association",
        "political_behavior_association",
        "media_exposure_association",
        "health_status_context_association",
        "residence_origin_context_association",
        "family_demographic_context_association",
        "satisfaction_context_association",
        "political_orientation_association",
        "religious_orientation_association",
        "language_cultural_context_association",
        "economic_policy_attitude_association",
        "status_code_association",
        "occupational_status_association",
        "family_background_association",
        "life_course_context_association",
        "institutional_context_association",
        "cognitive_ability_association",
        "diagnostic_numeric_context",
    }:
        return "diagnostic_only_lane"
    if lane == "blocked_metadata_context":
        return "blocked_lane"
    return "unknown_lane"


def _signal_payload_records(frame: pd.DataFrame, *, limit: int = 3) -> list[dict[str, Any]]:
    if frame.empty:
        return []

    def _support(v: Any) -> int | None:
        if v is None:
            return None
        try:
            val = int(float(str(v)))
            return val if val > 0 else None
        except (ValueError, TypeError):
            return None

    sort_cols = [col for col in ["association_support_n_unweighted", "n_overlap_unweighted", "response_overlap_n_unweighted", "lift", "difference_from_baseline"] if col in frame.columns]
    if sort_cols:
        ascending = [False] * len(sort_cols)
        frame = frame.sort_values(sort_cols, ascending=ascending, kind="mergesort")
    payloads: list[dict[str, Any]] = []
    for row in frame.head(limit).itertuples(index=False):
        row_series = pd.Series(row._asdict())
        payloads.append(
            {
                "associated_var_code": _clean(row_series.get("associated_var_code", "")),
                "associated_response_value": _clean(row_series.get("associated_response_value", "")),
                "associated_response_label": _clean(row_series.get("associated_response_label", "")),
                "association_lane": _clean(row_series.get("association_lane", "")),
                "n_overlap": _support(row_series.get("association_support_n_unweighted", row_series.get("n_overlap_unweighted", row_series.get("response_overlap_n_unweighted")))),
                "p_response_given_pattern": float(row_series.get("p_response_given_pattern", 0.0) or 0.0),
                "p_response_baseline": float(row_series.get("p_response_baseline", 0.0) or 0.0),
                "difference_from_baseline": float(row_series.get("difference_from_baseline", 0.0) or 0.0),
                "lift": float(row_series.get("lift", 0.0) or 0.0),
                "publication_status": _clean(row_series.get("association_publication_status", "")),
                "review_surface_reason": _clean(row_series.get("review_surface_reason", "")),
            }
        )
    return payloads


def _association_review_surface_rows(candidate_trace: pd.DataFrame) -> pd.DataFrame:
    if candidate_trace.empty:
        return _empty_association_review_surface()
    frame = candidate_trace.copy()
    if "association_publication_status" not in frame.columns:
        return _empty_association_review_surface()
    if "association_lane_publishability" not in frame.columns:
        frame["association_lane_publishability"] = frame["association_lane"].map(_association_lane_publishability)
    support_source = frame["association_support_n_unweighted"] if "association_support_n_unweighted" in frame.columns else frame.get("response_overlap_n_unweighted", pd.Series(0, index=frame.index))
    diff_source = frame["difference_from_baseline"] if "difference_from_baseline" in frame.columns else pd.Series(0.0, index=frame.index)
    lift_source = frame["lift"] if "lift" in frame.columns else pd.Series(0.0, index=frame.index)
    support = pd.to_numeric(support_source, errors="coerce").fillna(0).astype(int)
    diff = pd.to_numeric(diff_source, errors="coerce").fillna(0.0).astype(float)
    lift = pd.to_numeric(lift_source, errors="coerce").fillna(0.0).astype(float)
    publication_status = frame["association_publication_status"].astype(str)
    lane_publishability = frame["association_lane_publishability"].astype(str)
    lane = frame["association_lane"].astype(str)
    is_occ = _bool_series(frame, "is_raw_occupational_status_code", False)
    is_high_card = _bool_series(frame, "is_high_cardinality_associated_var", False)
    is_sparse = _bool_series(frame, "is_sparse_associated_response", False)
    is_same_fam = _bool_series(frame, "is_same_family_association", False)
    is_same_var = _bool_series(frame, "is_same_variable_association", False)
    distinct_count = pd.to_numeric(frame.get("associated_var_distinct_response_count", pd.Series(0, index=frame.index)), errors="coerce").fillna(0).astype(int)
    response_total_n = pd.to_numeric(frame.get("associated_response_total_n", pd.Series(0, index=frame.index)), errors="coerce").fillna(0).astype(int)
    context_lanes = {"identity_coordinate_association", "position_context_association", "family_background_association", "life_course_context_association"}
    review_mask = (
        ~is_same_fam
        & ~is_same_var
        & ~publication_status.isin({"publishable", "blocked_metadata_context", "blocked_missing_authority", "blocked_not_direct_evidence"})
        & (
            # Attitude lane review
            (lane.eq("substantive_attitude_association")
             & (support >= 3)
             & (distinct_count <= 15)
             & (response_total_n >= 10)
             & (diff.abs() >= 0.15))
            |
            # Context lane review
            (lane.isin(context_lanes)
             & (support >= 5)
             & (response_total_n >= 20)
             & (~is_occ))
            |
            # Occupational/status review
            (is_occ
             & (support >= 10)
             & (response_total_n >= 20))
            |
            # High-lift low-n review
            ((lift >= 3) & (support >= 3) & ~is_high_card & ~is_sparse)
        )
    )
    rows = frame.loc[review_mask].copy()
    if rows.empty:
        return _empty_association_review_surface()
    rows["review_surface_reason"] = "reviewable_not_publishable"
    rows.loc[(support >= 10) & (diff.abs() >= 0.15), "review_surface_reason"] = "moderate_support_below_publish_threshold"
    rows.loc[(lift >= 2.0) & (support >= 5), "review_surface_reason"] = "high_lift_with_minimum_support"
    rows.loc[lane_publishability.eq("diagnostic_only_lane") & (support >= 5), "review_surface_reason"] = "lane_not_publishable_but_supported"
    rows.loc[is_occ & (support >= 10), "review_surface_reason"] = "occupational_code_with_support"
    rows["review_surface_priority"] = "low"
    rows.loc[(support >= 10) & (diff.abs() >= 0.25), "review_surface_priority"] = "high"
    rows.loc[(support >= 10) & (diff.abs() >= 0.15) & (rows["review_surface_priority"] != "high"), "review_surface_priority"] = "medium"
    rows.loc[(lift >= 2.0) & (support >= 10), "review_surface_priority"] = "medium"
    rows = rows[[column for column in V550J_ASSOCIATION_REVIEW_SURFACE_COLUMNS if column in rows.columns]].copy()
    if rows.empty:
        return _empty_association_review_surface()
    return rows.reset_index(drop=True)


def _pattern_meaning_summary_rows(
    pattern_df: pd.DataFrame,
    candidate_trace: pd.DataFrame,
    association_review_surface: pd.DataFrame,
    association_index: pd.DataFrame,
) -> pd.DataFrame:
    if pattern_df.empty:
        return _empty_meaning_summary()
    candidate_frame = candidate_trace if candidate_trace is not None else pd.DataFrame()
    association_frame = association_index if association_index is not None else pd.DataFrame()
    review_frame = association_review_surface if association_review_surface is not None else pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for pattern in pattern_df.itertuples(index=False):
        pattern_id = _clean(getattr(pattern, "pattern_id", ""))
        family_id = _clean(getattr(pattern, "family_id", ""))
        pattern_candidates = candidate_frame[candidate_frame["pattern_id"].astype(str).eq(pattern_id)] if not candidate_frame.empty and "pattern_id" in candidate_frame.columns else pd.DataFrame()
        pattern_associations = association_frame[association_frame["pattern_id"].astype(str).eq(pattern_id)] if not association_frame.empty and "pattern_id" in association_frame.columns else pd.DataFrame()
        pattern_review = review_frame[review_frame["pattern_id"].astype(str).eq(pattern_id)] if not review_frame.empty and "pattern_id" in review_frame.columns else pd.DataFrame()
        publishable_attitude = pd.DataFrame()
        if not pattern_associations.empty and "association_lane" in pattern_associations.columns:
            pa = pattern_associations[pattern_associations["association_lane"].astype(str).eq("substantive_attitude_association")]
            if not pa.empty:
                if "is_raw_occupational_status_code" in pa.columns:
                    pa = pa[~pa["is_raw_occupational_status_code"].map(lambda v: _to_bool(v, False))]
                if "is_high_cardinality_associated_var" in pa.columns:
                    pa = pa[~pa["is_high_cardinality_associated_var"].map(lambda v: _to_bool(v, False))]
                if "is_sparse_associated_response" in pa.columns:
                    pa = pa[~pa["is_sparse_associated_response"].map(lambda v: _to_bool(v, False))]
                publishable_attitude = pa
        reviewable = pd.DataFrame()
        if not pattern_review.empty and "association_lane" in pattern_review.columns:
            _allowed_review_lanes = {
                "substantive_attitude_association",
                "economic_policy_attitude_association",
                "religious_orientation_association",
                "political_orientation_association",
            }
            reviewable = pattern_review[pattern_review["association_lane"].astype(str).isin(_allowed_review_lanes)]
            if not reviewable.empty and "association_publication_status" in reviewable.columns:
                reviewable = reviewable[~reviewable["association_publication_status"].astype(str).str.startswith(("diagnostic_only_", "blocked_"))]
            if not reviewable.empty:
                if "is_raw_occupational_status_code" in reviewable.columns:
                    reviewable = reviewable[~reviewable["is_raw_occupational_status_code"].map(lambda v: _to_bool(v, False))]
                if "is_high_cardinality_associated_var" in reviewable.columns:
                    reviewable = reviewable[~reviewable["is_high_cardinality_associated_var"].map(lambda v: _to_bool(v, False))]
                if "is_sparse_associated_response" in reviewable.columns:
                    reviewable = reviewable[~reviewable["is_sparse_associated_response"].map(lambda v: _to_bool(v, False))]

        def _lane_subset(frame: pd.DataFrame, lane_name: str) -> pd.DataFrame:
            if frame.empty or "association_lane" not in frame.columns:
                return pd.DataFrame()
            return frame[frame["association_lane"].astype(str).eq(lane_name)]

        # ── Context/review buckets from review_surface ──
        _review_context = pattern_review if not pattern_review.empty else pd.DataFrame()
        _context_lanes = [
            "identity_coordinate_association", "position_context_association",
            "political_behavior_association", "media_exposure_association",
            "health_status_context_association", "residence_origin_context_association",
            "family_demographic_context_association", "satisfaction_context_association",
            "family_background_association", "life_course_context_association",
            "institutional_context_association", "occupational_status_association",
            "political_orientation_association", "religious_orientation_association",
            "language_cultural_context_association", "economic_policy_attitude_association",
        ]

        # ── Signal counts ──
        publishable_count = len(publishable_attitude) if not publishable_attitude.empty else 0
        reviewable_count = len(reviewable) if not reviewable.empty else 0
        context_count = sum(len(_lane_subset(_review_context, lane)) for lane in _context_lanes) if not _review_context.empty else 0
        _diagnostic_frame = pattern_candidates if not pattern_candidates.empty else pd.DataFrame()
        diagnostic_lane_names = ["diagnostic_numeric_context", "unknown_association_lane", "occupational_status_association"]
        diagnostic_count = 0
        unknown_count = 0
        if not _diagnostic_frame.empty:
            for dl in diagnostic_lane_names:
                dl_rows = len(_lane_subset(_diagnostic_frame, dl))
                diagnostic_count += dl_rows
                if dl == "unknown_association_lane":
                    unknown_count += dl_rows

        boundary_pattern_type = _clean(getattr(pattern, "boundary_pattern_type", ""))
        semantic_resolved_share = float(_safe_float(getattr(pattern, "semantic_role_resolved_share", 0.0)) or 0.0)
        support_count = int(_safe_float(getattr(pattern, "pattern_count_unweighted", 0)) or 0)
        status = "insufficient_association_evidence"
        confidence = "diagnostic_only"
        warning_flags: list[str] = []

        # ── Warning flags ──
        if publishable_attitude.empty and reviewable.empty and _review_context.empty and _diagnostic_frame.empty:
            warning_flags.append("no_association_data")
        if publishable_attitude.empty and reviewable.empty and not _diagnostic_frame.empty:
            warning_flags.append("diagnostic_only_candidates_present")
        if reviewable.empty and not _review_context.empty:
            warning_flags.append("review_bucket_contains_no_true_review_rows")
        if publishable_attitude.empty and not reviewable.empty and _review_context.empty and _diagnostic_frame.empty:
            warning_flags.append("review_surface_empty")
        if unknown_count > 0:
            warning_flags.append(f"unknown_lane_present:{unknown_count}")
        if _diagnostic_frame.empty and not pattern_candidates.empty:
            warning_flags.append("candidate_trace_only_summary")

        # Check association index for pollution
        _known_context_codes = {
            "PADEG", "MADEG", "SPDEG", "PAEDUC", "MAEDUC", "SPEDUC",
            "WRKSTAT", "WORKHR", "SPHOUR", "SPWRKSTA", "SPWRKSLF", "PAWRKSLF",
            "WKSUP", "WKSUPS", "WKSUB", "WKSUBS", "WORKDY", "SPDAYS",
            "INDSTATUS", "MAINDSTATUS", "SPINDSTATUS", "PAINDSTATUS",
            "INDTAG", "MAINDTAG", "SPINDTAG", "PAINDTAG",
            "OCCSTATUS", "MAOCCSTATUS", "SPOCCSTATUS", "PAOCCSTATUS",
            "OCCTAG", "MAOCCTAG", "SPOCCTAG", "PAOCCTAG",
        }
        if not pattern_associations.empty:
            _pollution_flags = []
            if "is_raw_occupational_status_code" in pattern_associations.columns:
                _occ_rows = pattern_associations[pattern_associations["is_raw_occupational_status_code"].map(lambda v: _to_bool(v, False))]
                if not _occ_rows.empty:
                    _pollution_flags.append(f"occupational_code_in_index: {len(_occ_rows)}")
            if "is_high_cardinality_associated_var" in pattern_associations.columns:
                _high_card_rows = pattern_associations[pattern_associations["is_high_cardinality_associated_var"].map(lambda v: _to_bool(v, False))]
                if not _high_card_rows.empty:
                    _pollution_flags.append(f"high_cardinality_in_index: {len(_high_card_rows)}")
            if "is_sparse_associated_response" in pattern_associations.columns:
                _sparse_rows = pattern_associations[pattern_associations["is_sparse_associated_response"].map(lambda v: _to_bool(v, False))]
                if not _sparse_rows.empty:
                    _pollution_flags.append(f"sparse_response_in_index: {len(_sparse_rows)}")
            if "associated_var_code" in pattern_associations.columns:
                _attitude_rows = pattern_associations[pattern_associations["association_lane"].astype(str).eq("substantive_attitude_association")]
                _known_context_in_index = _attitude_rows[_attitude_rows["associated_var_code"].astype(str).str.upper().str.strip().isin(_known_context_codes)]
                if not _known_context_in_index.empty:
                    _pollution_flags.append(f"known_context_var_in_index: {len(_known_context_in_index)}")
            if _pollution_flags:
                warning_flags.extend(_pollution_flags)
                confidence = "diagnostic_only"
                status = "diagnostic_only_polluted_association_index"

        _has_pollution = bool(
            [f for f in warning_flags
             if f.startswith(("occupational_code_in_index", "high_cardinality_in_index", "sparse_response_in_index", "known_context_var_in_index"))]
        )

        # ── Status / Confidence logic ──
        if not _has_pollution:
            if publishable_count > 0:
                if publishable_count >= 10:
                    status = "summary_available_publishable"
                    confidence = "high"
                elif publishable_count >= 3:
                    status = "summary_available_publishable"
                    confidence = "medium"
                else:
                    status = "summary_available_publishable_only"
                    confidence = "low"
            elif reviewable_count > 0:
                status = "summary_available_review_only"
                confidence = "low"
            elif context_count > 0:
                status = "summary_available_context_only"
                confidence = "low"
            elif diagnostic_count > 0 or unknown_count > 0:
                status = "summary_available_diagnostic_only"
                confidence = "diagnostic_only"
        if not pattern_candidates.empty and pattern_candidates["association_lane"].astype(str).nunique(dropna=True) == 1 and pattern_candidates["association_lane"].astype(str).eq("substantive_attitude_association").all():
            warning_flags.append("lane_collapse_warning")
        if publishable_attitude.empty and not reviewable.empty and candidate_frame.empty:
            warning_flags.append("association_index_empty")
        _top_unknown_diag_payload = _signal_payload_records(pd.concat([
            _lane_subset(_diagnostic_frame, dl)
            for dl in diagnostic_lane_names
        ], ignore_index=True)) if not _diagnostic_frame.empty else []
        _top_unknown_diag_json = json.dumps(_top_unknown_diag_payload, ensure_ascii=False)
        _top_unknown_diag_len = len(_top_unknown_diag_payload)
        rows.append(
            {
                "run_id": _clean(getattr(pattern, "run_id", "")),
                "source_id": _clean(getattr(pattern, "source_id", "")),
                "source": _clean(getattr(pattern, "source", "")),
                "wave": _clean(getattr(pattern, "wave", "")),
                "canonical_wave": _clean(getattr(pattern, "canonical_wave", "")),
                "country_code": _clean(getattr(pattern, "country_code", "")),
                "family_id": family_id,
                "pattern_id": pattern_id,
                "boundary_pattern_type": boundary_pattern_type,
                "pattern_support_n_unweighted": support_count,
                "pattern_support_status": _clean(getattr(pattern, "support_status", "")),
                "semantic_role_resolved_share": semantic_resolved_share,
                "target_structure_status": _clean(getattr(pattern, "target_structure_status", "")),
                "target_selectivity_profile": _clean(getattr(pattern, "target_selectivity_profile", "")),
                "top_publishable_attitude_associations_json": json.dumps(_signal_payload_records(publishable_attitude), ensure_ascii=False),
                "top_reviewable_attitude_signals_json": json.dumps(_signal_payload_records(reviewable), ensure_ascii=False),
                "top_identity_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "identity_coordinate_association")), ensure_ascii=False),
                "top_position_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "position_context_association")), ensure_ascii=False),
                "top_occupational_status_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "occupational_status_association")), ensure_ascii=False),
                "top_family_background_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "family_background_association")), ensure_ascii=False),
                "top_life_course_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "life_course_context_association")), ensure_ascii=False),
                "top_political_behavior_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "political_behavior_association")), ensure_ascii=False),
                "top_media_exposure_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "media_exposure_association")), ensure_ascii=False),
                "top_health_status_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "health_status_context_association")), ensure_ascii=False),
                "top_residence_origin_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "residence_origin_context_association")), ensure_ascii=False),
                "top_family_demographic_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "family_demographic_context_association")), ensure_ascii=False),
                "top_satisfaction_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "satisfaction_context_association")), ensure_ascii=False),
                "top_political_orientation_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "political_orientation_association")), ensure_ascii=False),
                "top_religious_orientation_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "religious_orientation_association")), ensure_ascii=False),
                "top_language_cultural_context_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "language_cultural_context_association")), ensure_ascii=False),
                "top_economic_policy_attitude_signals_json": json.dumps(_signal_payload_records(_lane_subset(_review_context, "economic_policy_attitude_association")), ensure_ascii=False),
                "top_unknown_or_diagnostic_signals_json": _top_unknown_diag_json,
                "publishable_attitude_signal_count": publishable_count,
                "true_reviewable_attitude_signal_count": reviewable_count,
                "context_review_signal_count": context_count,
                "diagnostic_candidate_count": diagnostic_count,
                "displayed_diagnostic_signal_count": _top_unknown_diag_len,
                "unknown_signal_count": unknown_count,
                "meaning_summary_status": status,
                "meaning_summary_confidence": confidence,
                "meaning_summary_warning_flags_json": json.dumps(warning_flags, ensure_ascii=False),
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    frame = pd.DataFrame(rows)
    if frame.empty:
        return _empty_meaning_summary()
    return frame


def _pattern_id(family_id: str, source: str, wave: str, country_code: str, signature_raw: str) -> str:
    payload = {
        "family_id": family_id,
        "source": source,
        "wave": wave,
        "country_code": country_code,
        "signature_raw": signature_raw,
    }
    return _stable_hash(payload)


def _family_question_meta(family_questions: pd.DataFrame, family_lookup: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for row in family_questions.itertuples(index=False):
        var_code = _clean(getattr(row, "var_code", "")).upper()
        if not var_code:
            continue
        item_meta = family_lookup.get(var_code, {})
        lookup[var_code] = {
            "var_code": var_code,
            "question_id": _clean(getattr(row, "question_id", "")),
            "question_text": _clean(getattr(row, "question_text", "")),
            "semantic_role": _clean(getattr(row, "semantic_role", "")),
            "v551_evidence_role": _clean(getattr(row, "v551_evidence_role", "")),
            "driver_id": _clean(getattr(row, "driver_id", "")),
            "driver_facet_id": _clean(getattr(row, "driver_facet_id", "")),
            "relation_axis_id": _clean(getattr(row, "relation_axis_id", "")),
            "target_entity_id": _clean(getattr(row, "target_entity_id", "")),
            "mapping_status": _clean(getattr(row, "mapping_status", "")),
            "question_type": _clean(getattr(row, "question_type", "")),
            "handling_rule": _clean(getattr(row, "handling_rule", "")),
            "recommended_computation": _clean(getattr(row, "recommended_computation", "")),
            "source_structure_classification": _clean(getattr(row, "source_structure_classification", "")),
            "source_structure_basis": _clean(getattr(row, "source_structure_basis", "")),
            "source_structure_confidence": _clean(getattr(row, "source_structure_confidence", "")),
            "source_structure_source": _clean(getattr(row, "source_structure_source", "")),
            "source_structure_fields_joined": _to_bool(getattr(row, "source_structure_fields_joined", False)),
            "item_role": item_meta.get("item_role", "target_case"),
            "condition_label": item_meta.get("condition_label", ""),
        }
    return lookup


def _summarize_respondents(
    family_frame: pd.DataFrame,
    *,
    family_cfg: dict[str, Any],
    family_questions: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    item_lookup = _family_question_meta(family_questions, _family_item_lookup(family_cfg))
    item_order = _family_item_order(family_cfg)
    family_item_count = len(item_order)
    minimum_items_answered = int(_safe_float(family_cfg.get("minimum_items_answered", 1)) or 1)
    if family_frame.empty:
        return (
            pd.DataFrame(columns=["respondent_id"]),
            pd.DataFrame(columns=["pattern_id"]),
        )
    substantive_available = bool("is_substantive" in family_frame.columns and family_frame["is_substantive"].fillna(False).any())
    respondents_below_minimum_items_answered = 0

    respondent_rows: list[dict[str, Any]] = []
    for respondent_id, respondent_df in family_frame.groupby("respondent_id", sort=False):
        respondent_df = respondent_df.copy()
        respondent_df = respondent_df.sort_values(["var_code", "question_id"], kind="mergesort")
        respondent_weight_values = [_safe_float(value) for value in respondent_df.get("weight_value", []).tolist()]
        respondent_weight_metrics = _weight_metrics(respondent_weight_values)
        respondent_weight = _first_nonempty(respondent_df.get("weight_value", []), default=None)
        weight_float = _safe_float(respondent_weight)
        position_values = {field: _first_nonempty(respondent_df[field], default="") if field in respondent_df.columns else "" for field in POSITION_FIELDS}
        item_rows: list[dict[str, Any]] = []
        for var_code in item_order:
            item_df = respondent_df[respondent_df["var_code"].astype(str).str.upper().eq(var_code)]
            if item_df.empty:
                continue
            row = item_df.iloc[0]
            if substantive_available and not _to_bool(row.get("is_substantive", False), False):
                continue
            normalized_value = _clean(row.get("response_value_normalized"))
            if not normalized_value:
                continue
            item_meta = item_lookup.get(var_code, {})
            resolved_authority = _resolve_family_item_semantics(row, family_cfg=family_cfg, item_meta=item_meta)
            directionality_status_value = _clean(resolved_authority["directionality_status"]) or "unknown"
            directionality_authority_source = _clean(resolved_authority["directionality_authority_source"]) or "none"
            directionality_basis_source = _clean(resolved_authority.get("directionality_basis_source")) or "observed_response_row"
            response_semantics_authority_source = _clean(resolved_authority.get("response_semantics_authority_source")) or "none"
            semantic_response_role = _clean(resolved_authority["semantic_response_role"]) or "unknown"
            semantic_response_role_status = _clean(resolved_authority["semantic_response_role_status"]) or "missing_or_unsigned_directionality_authority"
            response_direction_value = _clean(resolved_authority["response_direction"])
            polarity_value = _clean(resolved_authority["polarity"])
            response_semantics_status = _clean(resolved_authority["response_semantics_status"]) or "observed_only"
            response_semantics_source = _clean(resolved_authority["response_semantics_source"]) or "observed_response_row"
            response_semantics_contract_hash = _clean(resolved_authority["response_semantics_contract_hash"])
            target_entity_id = _clean(resolved_authority["target_entity_id"])
            target_domain = _clean(resolved_authority.get("target_domain"))
            target_condition_label = _clean(resolved_authority.get("target_condition_label"))
            target_group_label = _clean(resolved_authority.get("target_group_label"))
            permission_domain = _clean(resolved_authority.get("permission_domain"))
            target_resolution_grain = _clean(resolved_authority.get("target_resolution_grain")) or "unresolved"
            target_resolution_status = _clean(resolved_authority["target_resolution_status"]) or _classify_target_resolution(target_entity_id)
            target_resolution_authority_source = _clean(resolved_authority.get("target_resolution_authority_source")) or "upstream_mapping"
            target_resolution_basis_source = _clean(resolved_authority.get("target_resolution_basis_source")) or "upstream_mapping"
            item_rows.append(
                {
                    "var_code": var_code,
                    "question_id": _clean(row.get("question_id")),
                    "response_value_normalized": normalized_value,
                    "response_label": _clean(row.get("response_label")),
                    "normalized_response_label": _clean(row.get("normalized_response_label")),
                    "response_direction": response_direction_value,
                    "response_intensity": _safe_float(row.get("response_intensity")),
                    "polarity": polarity_value,
                    "semantic_response_role": semantic_response_role,
                    "item_role": item_meta.get("item_role", "target_case"),
                    "condition_label": item_meta.get("condition_label", ""),
                    "driver_id": _clean(row.get("driver_id")),
                    "driver_facet_id": _clean(row.get("driver_facet_id")),
                    "relation_axis_id": _clean(row.get("relation_axis_id")),
                    "target_entity_id": target_entity_id,
                    "target_domain": target_domain,
                    "target_condition_label": target_condition_label,
                    "target_group_label": target_group_label,
                    "permission_domain": permission_domain,
                    "target_resolution_grain": target_resolution_grain,
                    "target_resolution_status": target_resolution_status,
                    "target_resolution_authority_source": target_resolution_authority_source,
                    "target_resolution_basis_source": target_resolution_basis_source,
                    "target_resolution_source": target_resolution_authority_source,
                    "mapping_status": _clean(row.get("mapping_status")),
                    "semantic_role": _clean(row.get("semantic_role")),
                    "v551_evidence_role": _clean(row.get("v551_evidence_role")),
                    "question_type": _clean(row.get("question_type")),
                    "handling_rule": _clean(row.get("handling_rule")),
                    "recommended_computation": _clean(row.get("recommended_computation")),
                    "source_structure_classification": _clean(row.get("source_structure_classification")),
                    "source_structure_basis": _clean(row.get("source_structure_basis")),
                    "source_structure_confidence": _clean(row.get("source_structure_confidence")),
                    "source_structure_source": _clean(row.get("source_structure_source")),
                    "source_structure_fields_joined": _to_bool(row.get("source_structure_fields_joined"), False),
                    "directionality_status": directionality_status_value,
                    "directionality_authority_source": directionality_authority_source,
                    "directionality_basis_source": directionality_basis_source,
                    "response_semantics_authority_source": response_semantics_authority_source,
                    "semantic_response_role_authority": response_semantics_authority_source,
                    "semantic_response_role_status": semantic_response_role_status,
                    "response_semantics_status": response_semantics_status,
                    "response_semantics_source": response_semantics_source,
                    "response_semantics_contract_hash": response_semantics_contract_hash,
                }
            )
        answered_var_codes = [row["var_code"] for row in item_rows]
        answered_item_count = len(answered_var_codes)
        if answered_item_count <= 0:
            continue
        if answered_item_count < minimum_items_answered:
            respondents_below_minimum_items_answered += 1
            continue
        raw_signature = "|".join(f"{row['var_code']}={row['response_value_normalized']}" for row in item_rows)
        semantic_signature = "|".join(f"{row['item_role']}={row['semantic_response_role']}" for row in item_rows)
        semantic_counts = Counter(row["semantic_response_role"] for row in item_rows)
        respondent_rows.append(
            {
                "respondent_id": _clean(respondent_id),
                "source": _clean(_first_nonempty(respondent_df.get("source", []), default="")),
                "wave": _clean(_first_nonempty(respondent_df.get("wave", []), default="")),
                "canonical_wave": _clean(_first_nonempty(respondent_df.get("canonical_wave", []), default="")),
                "country_code": _clean(_first_nonempty(respondent_df.get("country_code", []), default="")),
                "survey_year": _safe_float(_first_nonempty(respondent_df.get("survey_year", []), default=None)),
                "weight_value": weight_float,
                "weight_status": respondent_weight_metrics["weight_status"],
                "pattern_signature_raw": raw_signature,
                "pattern_signature_semantic": semantic_signature,
                "answered_var_codes": answered_var_codes,
                "n_items_answered": answered_item_count,
                "n_family_items": family_item_count,
                "completion_rate": completion_rate_v1(answered_item_count, family_item_count),
                "missingness_rate": missingness_rate_v1(completion_rate_v1(answered_item_count, family_item_count)),
                "directional_consistency": (sum(1 for row in item_rows if row["semantic_response_role"] in {"support", "oppose"}) / answered_item_count) if answered_item_count else 0.0,
                "support_direction_count": sum(1 for row in item_rows if row["semantic_response_role"] == "support"),
                "oppose_direction_count": sum(1 for row in item_rows if row["semantic_response_role"] == "oppose"),
                "neutral_direction_count": sum(1 for row in item_rows if row["semantic_response_role"] == "neutral"),
                "unknown_direction_count": sum(1 for row in item_rows if row["semantic_response_role"] == "unknown"),
                "semantic_counts": dict(semantic_counts),
                "position_values": position_values,
                **position_values,
                "item_rows": item_rows,
            }
        )

    respondent_df = pd.DataFrame(respondent_rows)
    respondent_df.attrs["respondents_below_minimum_items_answered"] = respondents_below_minimum_items_answered
    respondent_df.attrs["minimum_items_answered"] = minimum_items_answered
    if respondent_df.empty:
        return respondent_df, pd.DataFrame(columns=["pattern_id"])

    family_respondent_count = int(len(respondent_df))
    pattern_rows: list[dict[str, Any]] = []
    for signature_key, group in respondent_df.groupby(["pattern_signature_raw", "pattern_signature_semantic"], sort=False):
        raw_signature, semantic_signature = signature_key
        pattern_count_unweighted = int(len(group))
        weight_values = [_safe_float(row) for row in group["weight_value"].tolist()]
        pattern_weight_status = _combine_weight_statuses(group["weight_status"].tolist()) if "weight_status" in group.columns else "unweighted_only"
        weight_sum = float(sum(value for value in weight_values if value is not None and value > 0)) if weight_values else float(pattern_count_unweighted)
        family_weighted_respondent_total = float(sum(value for value in respondent_df["weight_value"].tolist() if value is not None and value > 0)) if "weight_value" in respondent_df.columns else float(family_respondent_count)
        pattern_probability_unweighted = (pattern_count_unweighted / family_respondent_count) if family_respondent_count else 0.0
        pattern_probability_weighted = (weight_sum / family_weighted_respondent_total) if family_weighted_respondent_total > 0 else pattern_probability_unweighted
        family_weight_metrics = _weight_metrics(weight_values)
        support_payload = support_prevalence_companions(
            pattern_count_unweighted,
            total_respondents=family_respondent_count,
            lane="relation",
            support_cap=DEFAULT_SUPPORT_CAP,
        )
        use_weighted_probability = pattern_weight_status in {"weighted_valid", "weighted_partial"}
        pattern_probability_basis = pattern_weight_status if use_weighted_probability else "unweighted_fallback"
        pattern_count_weighted_value = weight_sum if use_weighted_probability else float(pattern_count_unweighted)
        pattern_probability_weighted_value = pattern_probability_weighted if use_weighted_probability else pattern_probability_unweighted
        pattern_probability = pattern_probability_v1(pattern_probability_weighted_value)
        mean_completion = float(group["completion_rate"].dropna().mean()) if group["completion_rate"].notna().any() else 0.0
        mean_missingness = float(group["missingness_rate"].dropna().mean()) if group["missingness_rate"].notna().any() else 1.0
        confidence_score = confidence_score_v1(
            support_payload["support_score"],
            mean_completion * 100.0,
            family_weight_metrics["effective_n_ratio"] * 100.0,
            (pattern_probability or 0.0) * 100.0,
            (1.0 - mean_missingness) * 100.0,
        )
        support_ratio = support_payload["support_ratio"] if support_payload["support_ratio"] is not None else 0.0
        pattern_id = _pattern_id(family_cfg["family_id"], _clean(group.iloc[0].get("source", "")), _clean(group.iloc[0].get("wave", "")), _clean(group.iloc[0].get("country_code", "")), raw_signature)
        semantic_counts = Counter()
        for item_rows in group["item_rows"].tolist():
            semantic_counts.update(row["semantic_response_role"] for row in item_rows)
        item_rows_flat = [row for item_rows in group["item_rows"].tolist() for row in item_rows]
        boundary_pattern_type, boundary_diagnostics = _evaluate_boundary_rules(family_cfg, semantic_counts, item_rows_flat)
        target_resolution = _summarize_target_resolution(item_rows_flat)
        item_authority = _summarize_item_authority(item_rows_flat)
        pattern_rows.append(
            {
                "pattern_id": pattern_id,
                "family_id": family_cfg["family_id"],
                "family_label": family_cfg.get("family_label", ""),
                "family_type": family_cfg.get("family_type", ""),
                "family_structure_type": _clean(family_cfg.get("family_structure_type", "")) or _clean(family_cfg.get("family_type", "")),
                "expected_multi_target": bool(_to_bool(family_cfg.get("expected_multi_target", False), False)),
                "family_respondent_count": family_respondent_count,
                "family_item_count": family_item_count,
                "minimum_items_answered": minimum_items_answered,
                "completion_gate_status": "meets_minimum",
                "respondents_below_minimum_items_answered": respondents_below_minimum_items_answered,
                "pattern_signature_raw": raw_signature,
                "pattern_signature_semantic": semantic_signature,
                "semantic_counts": dict(semantic_counts),
                "boundary_pattern_type": boundary_pattern_type,
                "boundary_rule_evaluation_summary": boundary_diagnostics.get("boundary_rule_evaluation_summary", {}),
                "rules_evaluated": boundary_diagnostics.get("rules_evaluated", []),
                "rules_matched": boundary_diagnostics.get("rules_matched", []),
                "rules_failed": boundary_diagnostics.get("rules_failed", []),
                "boundary_rule_failure_reasons": boundary_diagnostics.get("boundary_rule_failure_reasons", {}),
                "boundary_rule_authority_source": boundary_diagnostics.get("boundary_rule_authority_source", "question_family_registry.boundary_rules"),
                "boundary_rule_status": boundary_diagnostics.get("boundary_rule_status", boundary_pattern_type),
                "pattern_count_unweighted": pattern_count_unweighted,
                "pattern_count_weighted": pattern_count_weighted_value,
                "pattern_probability_unweighted": pattern_probability_unweighted,
                "pattern_probability_weighted": pattern_probability_weighted_value,
                "pattern_probability_basis": pattern_probability_basis,
                "pattern_probability": pattern_probability if pattern_probability is not None else 0.0,
                "pattern_probability_formula_id": PATTERN_PROBABILITY_FORMULA_ID,
                "pattern_probability_formula_version": PATTERN_PROBABILITY_FORMULA_VERSION,
                "pattern_probability_implementation_function": PATTERN_PROBABILITY_IMPLEMENTATION_FUNCTION,
                "pattern_probability_score_family": PATTERN_PROBABILITY_SCORE_FAMILY,
                "pattern_probability_higher_is_better": PATTERN_PROBABILITY_HIGHEST_BETTER,
                "pattern_probability_decision_role": PATTERN_PROBABILITY_DECISION_ROLE,
                "n_unweighted": pattern_count_unweighted,
                "n_weighted": pattern_count_weighted_value,
                "weighted_count_basis": pattern_probability_basis if use_weighted_probability else "unweighted_fallback",
                "support_threshold": support_payload["support_threshold"],
                "support_ratio": support_ratio,
                "support_ratio_margin": support_payload["support_ratio_margin"],
                "support_score": support_payload["support_score"],
                **_formula_provenance("support", "support_score_v1", "v1", "data.ddm_build_copy.numeric_formulas.support_score_v1", "support_adequacy", True, "eligibility"),
                "support_status": support_payload["support_status"],
                "support_gate_status": support_payload["support_gate_status"],
                "prevalence_score": support_payload["prevalence_score"],
                **_formula_provenance("prevalence", "prevalence_score_v1", "v1", "data.ddm_build_copy.numeric_formulas.prevalence_score_v1", "prevalence", True, "context"),
                "completion_rate": mean_completion,
                **_formula_provenance("completion_rate", COMPLETION_RATE_FORMULA_ID, COMPLETION_RATE_FORMULA_VERSION, COMPLETION_RATE_IMPLEMENTATION_FUNCTION, COMPLETION_RATE_SCORE_FAMILY, COMPLETION_RATE_HIGHEST_BETTER, COMPLETION_RATE_DECISION_ROLE),
                "missingness_rate": mean_missingness,
                **_formula_provenance("missingness_rate", MISSINGNESS_RATE_FORMULA_ID, MISSINGNESS_RATE_FORMULA_VERSION, MISSINGNESS_RATE_IMPLEMENTATION_FUNCTION, MISSINGNESS_RATE_SCORE_FAMILY, MISSINGNESS_RATE_HIGHEST_BETTER, MISSINGNESS_RATE_DECISION_ROLE),
                "effective_n": family_weight_metrics["effective_n"],
                **_formula_provenance("effective_n", EFFECTIVE_N_FORMULA_ID, EFFECTIVE_N_FORMULA_VERSION, EFFECTIVE_N_IMPLEMENTATION_FUNCTION, EFFECTIVE_N_SCORE_FAMILY, EFFECTIVE_N_HIGHEST_BETTER, EFFECTIVE_N_DECISION_ROLE),
                "effective_n_ratio": family_weight_metrics["effective_n_ratio"],
                **_formula_provenance("effective_n_ratio", EFFECTIVE_N_RATIO_FORMULA_ID, EFFECTIVE_N_RATIO_FORMULA_VERSION, EFFECTIVE_N_RATIO_IMPLEMENTATION_FUNCTION, EFFECTIVE_N_RATIO_SCORE_FAMILY, EFFECTIVE_N_RATIO_HIGHEST_BETTER, EFFECTIVE_N_RATIO_DECISION_ROLE),
                "weight_nonnull_ratio": family_weight_metrics["weight_nonnull_ratio"],
                "weight_positive_ratio": family_weight_metrics["weight_positive_ratio"],
                "weight_variability_score": family_weight_metrics["weight_variability_score"],
                "weight_concentration_risk_score": family_weight_metrics["weight_concentration_risk_score"],
                "weight_validity_score": family_weight_metrics["weight_validity_score"],
                **_formula_provenance("weight_validity", WEIGHT_VALIDITY_FORMULA_ID, WEIGHT_VALIDITY_FORMULA_VERSION, WEIGHT_VALIDITY_IMPLEMENTATION_FUNCTION, WEIGHT_VALIDITY_SCORE_FAMILY, WEIGHT_VALIDITY_HIGHEST_BETTER, WEIGHT_VALIDITY_DECISION_ROLE),
                "weighted_count_validation_passed": pattern_weight_status == "weighted_valid",
                "weight_status": pattern_weight_status,
                "confidence_component_support": support_payload["support_score"],
                "confidence_component_mapping": mean_completion * 100.0,
                "confidence_component_directionality": ((group["directional_consistency"].dropna().mean() or 0.0) * 100.0) if group["directional_consistency"].notna().any() else 0.0,
                "confidence_component_weight": family_weight_metrics["weight_validity_score"],
                "confidence_component_missingness": (1.0 - mean_missingness) * 100.0,
                "confidence_score": confidence_score if confidence_score is not None else 0.0,
                **_formula_provenance("confidence", CONFIDENCE_FORMULA_ID, CONFIDENCE_FORMULA_VERSION, CONFIDENCE_IMPLEMENTATION_FUNCTION, CONFIDENCE_SCORE_FAMILY, CONFIDENCE_HIGHEST_BETTER, CONFIDENCE_DECISION_ROLE),
                "source": _clean(group.iloc[0].get("source", "")),
                "source_family": (
                    _clean(group.iloc[0].get("source_family", ""))
                    or _clean(group.iloc[0].get("source", ""))
                ),
                "wave": _clean(group.iloc[0].get("wave", "")),
                "canonical_wave": _clean(group.iloc[0].get("canonical_wave", "")),
                "country_code": _clean(group.iloc[0].get("country_code", "")),
                "survey_year": _safe_float(group.iloc[0].get("survey_year")),
                "directionality_status": item_authority["directionality_status"],
                "directionality_status_summary": item_authority["directionality_status_summary"],
                "directionality_authority_source": item_authority["directionality_authority_source"],
                "directionality_authority_source_summary": item_authority["directionality_authority_source_summary"],
                "directionality_basis_source": item_authority["directionality_basis_source"],
                "directionality_basis_source_summary": item_authority["directionality_basis_source_summary"],
                "response_semantics_authority_source": item_authority["response_semantics_authority_source"],
                "response_semantics_authority_source_summary": item_authority["response_semantics_authority_source_summary"],
                "semantic_response_role_authority": item_authority["semantic_response_role_authority"],
                "semantic_response_role_status": item_authority["semantic_response_role_status"],
                "semantic_response_role_status_summary": item_authority["semantic_response_role_status_summary"],
                "semantic_role_resolved_share": item_authority["semantic_role_resolved_share"],
                "semantic_role_unknown_share": item_authority["semantic_role_unknown_share"],
                "directionality_authority_coverage": item_authority["directionality_authority_coverage"],
                "target_resolution_status": target_resolution["target_resolution_status"],
                "target_resolution_status_summary": target_resolution["target_resolution_status_summary"],
                "target_resolution_grain_summary": target_resolution["target_resolution_grain_summary"],
                "target_entity_id_set": target_resolution["target_entity_id_set"],
                "target_domain_set": target_resolution["target_domain_set"],
                "target_condition_label_set": target_resolution["target_condition_label_set"],
                "target_group_label_set": target_resolution["target_group_label_set"],
                "permission_domain_set": target_resolution["permission_domain_set"],
                "infer_placeholder_share": target_resolution["infer_placeholder_share"],
                "registry_resolved_share": target_resolution["registry_resolved_share"],
                "unresolved_target_share": target_resolution["unresolved_target_share"],
                "condition_label_share": target_resolution["condition_label_share"],
                "target_group_share": target_resolution["target_group_share"],
                "permission_domain_share": target_resolution["permission_domain_share"],
                "mapping_coverage_score": (
                    100.0
                    * (
                        sum(1 for item in group.iloc[0]["item_rows"] if _clean(item.get("mapping_status", "")).lower() not in {"", "unknown", "missing"})
                        / max(1, len(group.iloc[0]["item_rows"]))
                    )
                ),
                "included_var_codes": item_order,
                "answered_var_codes": sorted({code for code in group["answered_var_codes"].explode().tolist() if code}),
                "n_items_answered": int(group["n_items_answered"].max()),
                "respondent_ids": group["respondent_id"].tolist(),
                "item_rows": group.iloc[0]["item_rows"],
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )

    pattern_df = pd.DataFrame(pattern_rows)
    if pattern_df.empty:
        return respondent_df, pattern_df
    pattern_df = pattern_df.sort_values(["family_id", "country_code", "support_score", "pattern_count_unweighted"], ascending=[True, True, False, False], kind="mergesort").reset_index(drop=True)
    return respondent_df, pattern_df


def _item_index_rows(pattern_df: pd.DataFrame, family_questions: pd.DataFrame) -> pd.DataFrame:
    if pattern_df.empty:
        return pd.DataFrame()
    question_lookup = {str(row.var_code).upper(): row._asdict() for row in family_questions.itertuples(index=False)}
    rows: list[dict[str, Any]] = []
    for pattern in pattern_df.itertuples(index=False):
        item_rows = pattern.item_rows if isinstance(pattern.item_rows, list) else []
        for item_order, item in enumerate(item_rows, start=1):
            question_meta = question_lookup.get(str(item["var_code"]).upper(), {})
            rows.append(
                {
                    "pattern_id": pattern.pattern_id,
                    "family_id": pattern.family_id,
                    "family_label": pattern.family_label,
                    "family_type": pattern.family_type,
                    "pattern_count_unweighted": pattern.pattern_count_unweighted,
                    "pattern_count_weighted": pattern.pattern_count_weighted,
                    "pattern_probability": pattern.pattern_probability,
                    "support_status": pattern.support_status,
                    "confidence_tier": _confidence_tier_from_score(getattr(pattern, "confidence_score", 0.0)),
                    "item_order": item_order,
                    "var_code": item["var_code"],
                    "question_id": question_meta.get("question_id", item.get("question_id", "")),
                    "item_role": item["item_role"],
                    "condition_label": item["condition_label"],
                    "response_value_normalized": item["response_value_normalized"],
                    "response_label": item["response_label"],
                    "normalized_response_label": item["normalized_response_label"],
                    "response_direction": item["response_direction"],
                    "response_intensity": item["response_intensity"],
                    "polarity": item.get("polarity", ""),
                    "directionality_status": item.get("directionality_status", ""),
                    "directionality_authority_source": item.get("directionality_authority_source", "none"),
                    "directionality_basis_source": item.get("directionality_basis_source", ""),
                    "response_semantics_authority_source": item.get("response_semantics_authority_source", "none"),
                    "semantic_response_role": item["semantic_response_role"],
                    "semantic_response_role_authority": item.get("semantic_response_role_authority", "none"),
                    "semantic_response_role_status": item.get("semantic_response_role_status", ""),
                    "response_semantics_status": item.get("response_semantics_status", ""),
                    "response_semantics_source": item.get("response_semantics_source", ""),
                    "response_semantics_contract_hash": item.get("response_semantics_contract_hash", ""),
                    "driver_id": item.get("driver_id", ""),
                    "driver_facet_id": item.get("driver_facet_id", ""),
                    "relation_axis_id": item.get("relation_axis_id", ""),
                    "target_entity_id": item.get("target_entity_id", ""),
                    "target_domain": item.get("target_domain", ""),
                    "target_condition_label": item.get("target_condition_label", ""),
                    "target_group_label": item.get("target_group_label", ""),
                    "permission_domain": item.get("permission_domain", ""),
                    "target_resolution_grain": item.get("target_resolution_grain", ""),
                    "target_resolution_status": item.get("target_resolution_status", ""),
                    "target_resolution_authority_source": item.get("target_resolution_authority_source", ""),
                    "target_resolution_basis_source": item.get("target_resolution_basis_source", ""),
                    "target_resolution_source": item.get("target_resolution_source", ""),
                    "mapping_status": item.get("mapping_status", ""),
                    "semantic_role": item.get("semantic_role", ""),
                    "v551_evidence_role": item.get("v551_evidence_role", ""),
                    "question_type": item.get("question_type", ""),
                    "handling_rule": item.get("handling_rule", ""),
                    "recommended_computation": item.get("recommended_computation", ""),
                    "source_structure_classification": item.get("source_structure_classification", ""),
                    "source_structure_basis": item.get("source_structure_basis", ""),
                    "source_structure_confidence": item.get("source_structure_confidence", ""),
                    "source_structure_source": item.get("source_structure_source", ""),
                    "source_structure_fields_joined": item.get("source_structure_fields_joined", False),
                    "created_at": utc_now(),
                    "schema_version": V550J_SCHEMA_VERSION,
                }
            )
    return pd.DataFrame(rows)


def _association_candidate_trace_rows_fast(
    pattern_df: pd.DataFrame,
    respondent_df: pd.DataFrame,
    *,
    context_frame: pd.DataFrame | None = None,
    family_var_codes: set[str] | None = None,
    pattern_membership_frame: pd.DataFrame | None = None,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
    association_support_threshold: int | None = None,
    publish_association_lanes: set[str] | None = None,
    association_lane_overrides: dict[str, Any] | None = None,
    emit_diagnostics: bool = True,
    registry: Any = None,
) -> pd.DataFrame | None:
    if pattern_df.empty or pattern_membership_frame is None or pattern_membership_frame.empty:
        return None
    baseline_frame = context_frame if context_frame is not None and not context_frame.empty else respondent_df
    if baseline_frame.empty or "var_code" not in baseline_frame.columns or "respondent_id" not in baseline_frame.columns:
        return None
    baseline_frame = _ensure_association_response_value_columns(baseline_frame).copy()
    family_var_codes = {str(code).upper() for code in (family_var_codes or set()) if str(code).strip()}
    baseline_frame["respondent_id_norm"] = baseline_frame["respondent_id"].astype(str).str.strip()
    baseline_frame["var_code_norm"] = baseline_frame["var_code"].astype(str).str.upper()
    baseline_frame["response_value_normalized"] = baseline_frame["response_value_normalized"].fillna("").astype(str).str.strip()
    baseline_frame["response_label"] = baseline_frame["response_label"].fillna("").astype(str).str.strip()
    baseline_frame["normalized_response_label"] = baseline_frame["normalized_response_label"].fillna("").astype(str).str.strip()
    association_support_threshold_value = _association_support_threshold(association_support_threshold)
    publish_association_lanes = {str(value).strip() for value in (publish_association_lanes or {"substantive_attitude_association"}) if str(value).strip()}
    eligible_rows: list[dict[str, Any]] = []
    blocked_not_direct_pairs: set[tuple[str, str]] = set()
    blocked_metadata_pairs: set[tuple[str, str]] = set()
    blocked_missing_authority_pairs: set[tuple[str, str]] = set()
    eligible_rows_missing_response_value = 0
    for row in baseline_frame.itertuples(index=False):
        var_code = str(getattr(row, "var_code_norm", "")).upper()
        if not var_code or var_code in family_var_codes:
            continue
        response_value = _fallback_response_value(row)
        if not response_value:
            eligible_rows_missing_response_value += 1
            continue
        row_status, direct_evidence_status = _association_row_status(row)
        pair_key = (var_code, response_value)
        if row_status == "blocked_not_direct_evidence":
            blocked_not_direct_pairs.add(pair_key)
            continue
        if row_status == "blocked_metadata_context":
            blocked_metadata_pairs.add(pair_key)
            continue
        if row_status == "blocked_missing_authority":
            blocked_missing_authority_pairs.add(pair_key)
            continue
        record = row._asdict()
        record["var_code_norm"] = var_code
        record["_association_eligibility_status"] = row_status
        record["_direct_evidence_status"] = direct_evidence_status
        eligible_rows.append(record)
    if not eligible_rows:
        return None
    eligible_df = pd.DataFrame(eligible_rows)
    if eligible_df.empty:
        return None
    for column, default in {
        "semantic_role": "",
        "source_structure_classification": "",
        "not_direct_evidence": False,
        "allowed_as_association_feature": False,
        "allowed_as_attitude_cloud_feature": False,
        "response_direction": "",
        "response_label": "",
        "normalized_response_label": "",
    }.items():
        if column not in eligible_df.columns:
            eligible_df[column] = default
    eligible_df["respondent_id_norm"] = eligible_df["respondent_id_norm"].fillna("").astype(str).str.strip()
    eligible_df["var_code_norm"] = eligible_df["var_code_norm"].fillna("").astype(str).str.upper()
    eligible_df["response_value_normalized"] = eligible_df["response_value_normalized"].fillna("").astype(str).str.strip()
    eligible_df = eligible_df.rename(columns={"weight_value": "context_weight_value"})
    eligible_df["context_weight_value"] = eligible_df["context_weight_value"].map(lambda value: _safe_float(value) or 1.0)
    eligible_df.loc[eligible_df["context_weight_value"] <= 0, "context_weight_value"] = 1.0
    eligible_df = eligible_df[eligible_df["respondent_id_norm"].ne("") & eligible_df["var_code_norm"].ne("") & eligible_df["response_value_normalized"].ne("")].copy()
    if eligible_df.empty:
        return None
    membership_frame = pattern_membership_frame.copy()
    if "respondent_id_norm" not in membership_frame.columns:
        if "respondent_id" in membership_frame.columns:
            membership_frame["respondent_id_norm"] = membership_frame["respondent_id"].astype(str).str.strip()
        else:
            membership_frame["respondent_id_norm"] = ""
    membership_frame["respondent_id_norm"] = membership_frame["respondent_id_norm"].fillna("").astype(str).str.strip()
    membership_frame["pattern_id"] = membership_frame["pattern_id"].astype(str)
    if "weight_value" in membership_frame.columns:
        membership_frame = membership_frame.rename(columns={"weight_value": "pattern_weight_value"})
    else:
        membership_frame["pattern_weight_value"] = 1.0
    membership_frame = membership_frame[membership_frame["respondent_id_norm"].ne("") & membership_frame["pattern_id"].ne("")].copy()
    if membership_frame.empty:
        return None
    join_cols = [column for column in [
        "run_id",
        "source_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "family_id",
        "pattern_id",
        "respondent_id",
        "respondent_id_norm",
        "pattern_weight_value",
        "pattern_signature",
        "answered_item_count",
        "pattern_count_unweighted",
        "pattern_count_weighted",
        "pattern_probability",
        "pattern_support_status",
        "pattern_support_gate_status",
        "support_status",
        "confidence_score",
    ] if column in membership_frame.columns]
    joined = membership_frame[join_cols].merge(
        eligible_df[
            [
                "respondent_id_norm",
                "var_code",
                "var_code_norm",
                "response_value_normalized",
                "response_label",
                "normalized_response_label",
                "response_direction",
                "context_weight_value",
                "_association_eligibility_status",
                "_direct_evidence_status",
                "semantic_role",
                "source_structure_classification",
                "not_direct_evidence",
                "allowed_as_association_feature",
                "allowed_as_attitude_cloud_feature",
            ]
        ],
        on="respondent_id_norm",
        how="inner",
    )
    if joined.empty:
        return None
    pattern_totals = (
        joined.groupby(["pattern_id"], observed=True)
        .agg(
            run_id=("run_id", "first") if "run_id" in joined.columns else ("pattern_id", "first"),
            source_id=("source_id", "first") if "source_id" in joined.columns else ("pattern_id", "first"),
            source=("source", "first") if "source" in joined.columns else ("pattern_id", "first"),
            wave=("wave", "first") if "wave" in joined.columns else ("pattern_id", "first"),
            canonical_wave=("canonical_wave", "first") if "canonical_wave" in joined.columns else ("pattern_id", "first"),
            country_code=("country_code", "first") if "country_code" in joined.columns else ("pattern_id", "first"),
            family_id=("family_id", "first") if "family_id" in joined.columns else ("pattern_id", "first"),
            pattern_member_n_unweighted=("respondent_id_norm", "nunique"),
            pattern_member_n_weighted=("pattern_weight_value", "sum"),
            pattern_count_unweighted=("pattern_count_unweighted", "first"),
            pattern_count_weighted=("pattern_count_weighted", "first"),
            support_status=("support_status", "first") if "support_status" in joined.columns else ("pattern_support_status", "first"),
            confidence_score=("confidence_score", "first") if "confidence_score" in joined.columns else ("pattern_count_weighted", "first"),
        )
        .reset_index()
    )
    pattern_var_totals = (
        joined.groupby(["pattern_id", "var_code_norm"], observed=True)
        .agg(
            pattern_var_answered_n_unweighted=("respondent_id_norm", "nunique"),
            pattern_var_answered_n_weighted=("context_weight_value", "sum"),
        )
        .reset_index()
    )
    candidate_counts = (
        joined.groupby(["pattern_id", "var_code_norm", "response_value_normalized"], observed=True)
        .agg(
            response_overlap_n_unweighted=("respondent_id_norm", "nunique"),
            response_overlap_n_weighted=("context_weight_value", "sum"),
            association_eligibility_status=("_association_eligibility_status", "first"),
            direct_evidence_status=("_direct_evidence_status", "first"),
            semantic_role=("semantic_role", "first"),
            source_structure_classification=("source_structure_classification", "first"),
            not_direct_evidence=("not_direct_evidence", "first"),
            allowed_as_association_feature=("allowed_as_association_feature", "first"),
            allowed_as_attitude_cloud_feature=("allowed_as_attitude_cloud_feature", "first"),
            response_label=("response_label", "first"),
            normalized_response_label=("normalized_response_label", "first"),
            response_direction=("response_direction", "first"),
        )
        .reset_index()
    )
    baseline_counts = (
        eligible_df.groupby(["var_code_norm", "response_value_normalized"], observed=True)
        .agg(
            baseline_response_n_unweighted=("respondent_id_norm", "nunique"),
            baseline_response_n_weighted=("context_weight_value", "sum"),
        )
        .reset_index()
    )
    baseline_totals = (
        eligible_df.groupby(["var_code_norm"], observed=True)
        .agg(
            baseline_answered_n_unweighted=("respondent_id_norm", "nunique"),
            baseline_answered_n_weighted=("context_weight_value", "sum"),
        )
        .reset_index()
    )
    candidate_counts = candidate_counts.merge(pattern_totals, on="pattern_id", how="left")
    candidate_counts = candidate_counts.merge(pattern_var_totals, on=["pattern_id", "var_code_norm"], how="left")
    candidate_counts = candidate_counts.merge(baseline_counts, on=["var_code_norm", "response_value_normalized"], how="left")
    candidate_counts = candidate_counts.merge(baseline_totals, on=["var_code_norm"], how="left")
    candidate_counts["pattern_member_n_unweighted"] = candidate_counts["pattern_count_unweighted"].fillna(0).astype(int)
    candidate_counts["pattern_member_n_weighted"] = candidate_counts["pattern_count_weighted"].fillna(0.0).astype(float)
    candidate_counts["eligible_rows_for_var"] = candidate_counts["baseline_answered_n_unweighted"].fillna(0).astype(int)
    candidate_counts["eligible_rows_with_response_value"] = candidate_counts["baseline_answered_n_unweighted"].fillna(0).astype(int)
    candidate_counts["pattern_member_rows_for_var"] = candidate_counts["pattern_var_answered_n_unweighted"].fillna(0).astype(int)
    candidate_counts["pattern_answered_var_n_unweighted"] = candidate_counts["pattern_var_answered_n_unweighted"].fillna(0).astype(int)
    candidate_counts["pattern_answered_var_n_weighted"] = candidate_counts["pattern_var_answered_n_weighted"].fillna(0.0).astype(float)
    candidate_counts["n_overlap_unweighted"] = candidate_counts["response_overlap_n_unweighted"].fillna(0).astype(int)
    candidate_counts["n_overlap_weighted"] = candidate_counts["response_overlap_n_weighted"].fillna(0.0).astype(float)
    candidate_counts["support_threshold"] = int(association_support_threshold_value)
    candidate_counts["support_gate_status"] = candidate_counts["n_overlap_unweighted"].map(
        lambda value: "zero_overlap"
        if int(value or 0) <= 0
        else "below_threshold"
        if int(value or 0) < association_support_threshold_value
        else "sufficient_support"
    )
    candidate_counts["baseline_share"] = candidate_counts["baseline_response_n_unweighted"].fillna(0).astype(float) / candidate_counts["baseline_answered_n_unweighted"].replace(0, pd.NA)
    candidate_counts["p_response_given_pattern"] = candidate_counts["response_overlap_n_weighted"].fillna(0.0).astype(float) / candidate_counts["pattern_var_answered_n_weighted"].replace(0, pd.NA)
    candidate_counts["p_response_baseline"] = candidate_counts["baseline_share"].fillna(0.0)
    candidate_counts["difference_from_baseline"] = candidate_counts["p_response_given_pattern"].fillna(0.0) - candidate_counts["p_response_baseline"].fillna(0.0)
    candidate_counts["lift"] = candidate_counts.apply(lambda row: 0.0 if float(row["p_response_baseline"] or 0.0) <= 0 else float(row["p_response_given_pattern"] or 0.0) / float(row["p_response_baseline"] or 1.0), axis=1)
    candidate_counts["mutual_information"] = candidate_counts.apply(
        lambda row: 0.0
        if float(row["p_response_baseline"] or 0.0) <= 0 or float(row["p_response_given_pattern"] or 0.0) <= 0
        else float(math.log2(max(1e-12, float(row["p_response_given_pattern"])) / max(1e-12, float(row["p_response_baseline"]))))
        * (float(row["pattern_member_n_unweighted"]) / max(1, int(len(respondent_df)) if not respondent_df.empty else 1)),
        axis=1,
    )

    # Compute cardinality and response total support from baseline_frame
    _baseline_var_cardinality: dict[str, tuple[int, str, bool]] = {}
    _baseline_response_total: dict[tuple[str, str], tuple[int, float, int]] = {}
    if baseline_frame is not None and not baseline_frame.empty:
        _bf = baseline_frame.copy()
        _bf["_vcn"] = _bf["var_code_norm"].fillna("").astype(str).str.upper().str.strip()
        _bf["_rvn"] = _bf["response_value_normalized"].fillna("").astype(str).str.strip()
        _weight_col = "context_weight_value" if "context_weight_value" in _bf.columns else "weight_value" if "weight_value" in _bf.columns else None
        for vc in candidate_counts["var_code_norm"].unique():
            vc_str = str(vc).upper().strip() if vc else ""
            if not vc_str:
                continue
            vf = _bf[_bf["_vcn"] == vc_str]
            if vf.empty:
                continue
            distinct_vals = vf["_rvn"].unique()
            dc = len(distinct_vals)
            band = "low_cardinality"
            if dc > 75:
                band = "very_high_cardinality"
            elif dc > 25:
                band = "high_cardinality"
            elif dc > 10:
                band = "moderate_cardinality"
            is_high = dc > 25
            _baseline_var_cardinality[vc_str] = (dc, band, is_high)
            for rv in distinct_vals:
                rv_str = str(rv).strip() if rv else ""
                if not rv_str:
                    continue
                rf = vf[vf["_rvn"] == rv_str]
                rn = len(rf)
                rw = int(pd.to_numeric(rf[_weight_col], errors="coerce").fillna(0.0).sum()) if _weight_col and not rf.empty else 0
                bs = rn / max(1, len(vf))
                _baseline_response_total[(vc_str, rv_str)] = (rn, bs, rw)

    _occ_cache: dict[str, bool] = {}
    def _cached_is_raw_occ(vc: str) -> bool:
        if vc not in _occ_cache:
            _occ_cache[vc] = _is_raw_occupational_status_code(vc)
        return _occ_cache[vc]

    candidate_counts["associated_var_distinct_response_count"] = candidate_counts["var_code_norm"].map(
        lambda v: _baseline_var_cardinality.get(str(v).upper().strip(), (0, "unknown_cardinality", False))[0]
    ).fillna(0).astype(int)
    candidate_counts["associated_var_cardinality_band"] = candidate_counts["var_code_norm"].map(
        lambda v: _baseline_var_cardinality.get(str(v).upper().strip(), (0, "unknown_cardinality", False))[1]
    ).fillna("unknown_cardinality")
    candidate_counts["associated_var_effective_cardinality"] = candidate_counts["associated_var_distinct_response_count"]
    candidate_counts["is_high_cardinality_associated_var"] = candidate_counts["var_code_norm"].map(
        lambda v: _baseline_var_cardinality.get(str(v).upper().strip(), (0, "unknown_cardinality", False))[2]
    ).fillna(False)
    def _lookup_response_total(row: Any) -> tuple[int, float, int]:
        vc = str(getattr(row, "var_code_norm", "")).upper().strip()
        rv = str(getattr(row, "response_value_normalized", "")).strip()
        return _baseline_response_total.get((vc, rv), (0, 0.0, 0))
    candidate_counts["associated_response_total_n"] = candidate_counts.apply(
        lambda r: _lookup_response_total(r)[0], axis=1
    ).fillna(0).astype(int)
    candidate_counts["associated_response_total_weighted_n"] = candidate_counts.apply(
        lambda r: _lookup_response_total(r)[2], axis=1
    ).fillna(0).astype(int)
    candidate_counts["associated_response_baseline_share"] = candidate_counts.apply(
        lambda r: _lookup_response_total(r)[1], axis=1
    ).fillna(0.0).astype(float)
    candidate_counts["is_sparse_associated_response"] = candidate_counts["associated_response_total_n"].map(
        lambda n: _is_sparse_associated_response(int(n or 0))
    ).fillna(False)

    rows: list[dict[str, Any]] = []
    candidate_pairs_formed = 0
    candidate_pairs_published = 0
    suppressed_no_candidate_pairs_formed = 0
    suppressed_no_pattern_member_overlap = 0
    suppressed_low_response_overlap = 0
    suppressed_low_baseline = 0
    suppressed_effect_size_zero_or_trivial = 0
    for row in candidate_counts.itertuples(index=False):
        row_series = pd.Series(row._asdict())
        row_status = _clean(row_series.get("association_eligibility_status", "eligible"))
        direct_evidence_status = _clean(row_series.get("direct_evidence_status", "direct_or_not_flagged"))
        associated_var_code = _clean(row_series.get("associated_var_code", "")) or _clean(row_series.get("var_code_norm", ""))
        lane_override, lane_override_basis = _association_lane_override(association_lane_overrides, associated_var_code)
        _card_data = _baseline_var_cardinality.get(str(associated_var_code).upper().strip(), (0, "unknown_cardinality", False))
        _rvn_str = str(row_series.get("response_value_normalized", "")).strip()
        _response_total_data = _baseline_response_total.get((str(associated_var_code).upper().strip(), _rvn_str), (0, 0.0, 0))
        _is_occ = _cached_is_raw_occ(str(associated_var_code).upper().strip())
        _is_high_card = _card_data[2]
        _is_sparse = _is_sparse_associated_response(_response_total_data[0])
        _is_same_fam = _check_same_family_association(associated_var_code, family_var_codes)
        _is_same_var = _check_same_variable_association(associated_var_code, family_var_codes)
        association_lane, association_lane_status, association_lane_rule_id = classify_association_lane(
            associated_var_code=associated_var_code,
            source_structure_classification=row_series.get("source_structure_classification", ""),
            semantic_role=row_series.get("semantic_role", ""),
            direct_evidence_status=direct_evidence_status,
            question_type=row_series.get("question_type", ""),
            response_semantics_status=row_series.get("response_semantics_status", ""),
            registry_override=lane_override,
            associated_var_distinct_response_count=_card_data[0],
            registry=registry,
            source=source,
            wave=wave,
            country_code=country_code,
        )
        support_gate_status = _clean(row_series.get("support_gate_status", "missing_denominator"))
        association_support_gate_status = support_gate_status
        support_threshold_value = int(row_series.get("support_threshold", association_support_threshold_value) or association_support_threshold_value)
        support_ratio = float(row_series.get("support_ratio", 0.0) or 0.0)
        support_margin = int(row_series.get("n_overlap_unweighted", 0) or 0) - support_threshold_value
        _n_overlap = int(row_series.get("n_overlap_unweighted", 0) or 0)
        _pattern_n = int(row_series.get("pattern_member_n_unweighted", 0) or 0)
        _support_n = _n_overlap
        _support_ratio_val = _support_n / max(1, _pattern_n)
        _diff = float(row_series.get("difference_from_baseline", 0.0) or 0.0)
        association_publication_status, association_publication_reason, would_emit_as_publishable = _association_publication_status(
            support_gate_status=association_support_gate_status,
            association_lane=association_lane,
            association_lane_status=association_lane_status,
            row_status=row_status,
            direct_evidence_status=direct_evidence_status,
            is_same_variable=_is_same_var,
            is_same_family=_is_same_fam,
            is_raw_occupational=_is_occ,
            is_high_cardinality=_is_high_card,
            is_sparse_response=_is_sparse,
            n_overlap_unweighted=_n_overlap,
            association_support_threshold=association_support_threshold_value,
            associated_var_distinct_response_count=_card_data[0],
            associated_response_total_n=_response_total_data[0],
            association_support_n_unweighted=_support_n,
            pattern_member_n_unweighted=_pattern_n,
            association_support_ratio=_support_ratio_val,
            difference_from_baseline=_diff,
            publishable_lanes=publish_association_lanes,
        )
    candidate_counts["baseline_share"] = candidate_counts["baseline_response_n_unweighted"].fillna(0).astype(float) / candidate_counts["baseline_answered_n_unweighted"].replace(0, pd.NA)
    candidate_counts["p_response_given_pattern"] = candidate_counts["response_overlap_n_weighted"].fillna(0.0).astype(float) / candidate_counts["pattern_var_answered_n_weighted"].replace(0, pd.NA)
    candidate_counts["p_response_baseline"] = candidate_counts["baseline_share"].fillna(0.0)
    candidate_counts["difference_from_baseline"] = candidate_counts["p_response_given_pattern"].fillna(0.0) - candidate_counts["p_response_baseline"].fillna(0.0)
    candidate_counts["lift"] = candidate_counts.apply(lambda row: 0.0 if float(row["p_response_baseline"] or 0.0) <= 0 else float(row["p_response_given_pattern"] or 0.0) / float(row["p_response_baseline"] or 1.0), axis=1)
    candidate_counts["mutual_information"] = candidate_counts.apply(
        lambda row: 0.0
        if float(row["p_response_baseline"] or 0.0) <= 0 or float(row["p_response_given_pattern"] or 0.0) <= 0
        else float(math.log2(max(1e-12, float(row["p_response_given_pattern"])) / max(1e-12, float(row["p_response_baseline"]))))
        * (float(row["pattern_member_n_unweighted"]) / max(1, int(len(respondent_df)) if not respondent_df.empty else 1)),
        axis=1,
    )
    rows: list[dict[str, Any]] = []
    candidate_pairs_formed = 0
    candidate_pairs_published = 0
    suppressed_no_candidate_pairs_formed = 0
    suppressed_no_pattern_member_overlap = 0
    suppressed_low_response_overlap = 0
    suppressed_low_baseline = 0
    suppressed_low_pattern_support = 0
    suppressed_effect_size_zero_or_trivial = 0
    for row in candidate_counts.itertuples(index=False):
        row_series = pd.Series(row._asdict())
        row_status = _clean(row_series.get("association_eligibility_status", "eligible"))
        direct_evidence_status = _clean(row_series.get("direct_evidence_status", "direct_or_not_flagged"))
        associated_var_code = _clean(row_series.get("associated_var_code", "")) or _clean(row_series.get("var_code_norm", ""))
        lane_override, lane_override_basis = _association_lane_override(association_lane_overrides, associated_var_code)
        association_lane, association_lane_status, association_lane_rule_id = classify_association_lane(
            associated_var_code=associated_var_code,
            source_structure_classification=row_series.get("source_structure_classification", ""),
            semantic_role=row_series.get("semantic_role", ""),
            direct_evidence_status=direct_evidence_status,
            question_type=row_series.get("question_type", ""),
            response_semantics_status=row_series.get("response_semantics_status", ""),
            registry_override=lane_override,
            registry=registry,
            source=source,
            wave=wave,
            country_code=country_code,
        )
        support_gate_status = _clean(row_series.get("support_gate_status", "missing_denominator"))
        association_support_gate_status = support_gate_status
        support_threshold_value = int(row_series.get("support_threshold", association_support_threshold_value) or association_support_threshold_value)
        support_ratio = float(row_series.get("support_ratio", 0.0) or 0.0)
        support_margin = int(row_series.get("n_overlap_unweighted", 0) or 0) - support_threshold_value
        _n_overlap = int(row_series.get("n_overlap_unweighted", 0) or 0)
        _pattern_n = int(row_series.get("pattern_member_n_unweighted", 0) or 0)
        _support_n = _n_overlap
        _support_ratio_val = _support_n / max(1, _pattern_n)
        _diff = float(row_series.get("difference_from_baseline", 0.0) or 0.0)
        _is_occ = _cached_is_raw_occ(str(associated_var_code).upper().strip())
        _is_high_card = bool(row_series.get("is_high_cardinality_associated_var", False))
        _is_sparse = bool(row_series.get("is_sparse_associated_response", False))
        _is_same_fam = _check_same_family_association(associated_var_code, family_var_codes)
        _is_same_var = _check_same_variable_association(associated_var_code, family_var_codes)
        _card_data_count = int(row_series.get("associated_var_distinct_response_count", 0) or 0)
        _resp_total_n = int(row_series.get("associated_response_total_n", 0) or 0)
        _auth_source = association_lane_rule_id if association_lane_rule_id else "lane_classifier"
        _auth_basis = "registry" if association_lane_rule_id else "computed"
        association_publication_status, association_publication_reason, would_emit_as_publishable = _association_publication_status(
            support_gate_status=association_support_gate_status,
            association_lane=association_lane,
            association_lane_status=association_lane_status,
            row_status=row_status,
            direct_evidence_status=direct_evidence_status,
            is_same_variable=_is_same_var,
            is_same_family=_is_same_fam,
            is_raw_occupational=_is_occ,
            is_high_cardinality=_is_high_card,
            is_sparse_response=_is_sparse,
            n_overlap_unweighted=_n_overlap,
            association_support_threshold=association_support_threshold_value,
            associated_var_distinct_response_count=_card_data_count,
            associated_response_total_n=_resp_total_n,
            association_support_n_unweighted=_support_n,
            pattern_member_n_unweighted=_pattern_n,
            association_support_ratio=_support_ratio_val,
            difference_from_baseline=_diff,
            publishable_lanes=publish_association_lanes,
        )
        if association_support_gate_status == "below_threshold":
            suppressed_low_response_overlap += 1
        elif association_support_gate_status == "zero_overlap":
            suppressed_no_pattern_member_overlap += 1
        elif association_support_gate_status == "missing_denominator":
            suppressed_low_baseline += 1
        suppression_reason = association_publication_reason
        candidate_pairs_formed += 1
        if would_emit_as_publishable:
            candidate_pairs_published += 1
        effective_run_id = _clean(row_series.get("run_id", "")) or _clean(run_id)
        effective_source_id = _clean(row_series.get("source_id", "")) or _clean(source_id) or _clean(source)
        effective_source = _clean(row_series.get("source", "")) or _clean(source)
        effective_wave = _clean(row_series.get("wave", "")) or _clean(wave)
        effective_canonical_wave = _clean(row_series.get("canonical_wave", "")) or _clean(canonical_wave) or effective_wave
        effective_country_code = _clean(row_series.get("country_code", "")) or _clean(country_code)
        effective_family_id = _clean(row_series.get("family_id", ""))
        payload = {
            "run_id": effective_run_id,
            "source_id": effective_source_id,
            "source": effective_source,
            "wave": effective_wave,
            "canonical_wave": effective_canonical_wave,
            "country_code": effective_country_code,
            "pattern_id": _clean(row_series.get("pattern_id", "")),
            "family_id": effective_family_id,
            "var_code": _clean(row_series.get("var_code_norm", "")),
            "question_id": "",
            "item_role": "outside_family",
            "condition_label": "",
            "associated_var_code": associated_var_code,
            "associated_question_id": "",
            "associated_response_value": _clean(row_series.get("response_value_normalized", "")),
            "associated_response_value_normalized": _clean(row_series.get("response_value_normalized", "")),
            "associated_response_label": _clean(row_series.get("response_label", "")),
            "associated_response_direction": _clean(row_series.get("response_direction", "")),
            "candidate_stage": "candidate_pair_publishable" if would_emit_as_publishable else "candidate_pair_suppressed",
            "pattern_member_n_unweighted": int(row_series.get("pattern_member_n_unweighted", 0) or 0),
            "pattern_member_n_weighted": float(row_series.get("pattern_member_n_weighted", 0.0) or 0.0),
            "eligible_rows_for_var": int(row_series.get("eligible_rows_for_var", 0) or 0),
            "eligible_rows_with_response_value": int(row_series.get("eligible_rows_with_response_value", 0) or 0),
            "pattern_member_rows_for_var": int(row_series.get("pattern_member_rows_for_var", 0) or 0),
            "response_overlap_n_unweighted": int(row_series.get("response_overlap_n_unweighted", 0) or 0),
            "response_overlap_n_weighted": float(row_series.get("response_overlap_n_weighted", 0.0) or 0.0),
            "baseline_answered_n_unweighted": int(row_series.get("baseline_answered_n_unweighted", 0) or 0),
            "baseline_answered_n_weighted": float(row_series.get("baseline_answered_n_weighted", 0.0) or 0.0),
            "pattern_var_answered_n_unweighted": int(row_series.get("pattern_var_answered_n_unweighted", 0) or 0),
            "pattern_var_answered_n_weighted": float(row_series.get("pattern_var_answered_n_weighted", 0.0) or 0.0),
            "pattern_answered_var_n_unweighted": int(row_series.get("pattern_answered_var_n_unweighted", 0) or 0),
            "pattern_answered_var_n_weighted": float(row_series.get("pattern_answered_var_n_weighted", 0.0) or 0.0),
            "n_overlap_unweighted": int(row_series.get("n_overlap_unweighted", 0) or 0),
            "n_overlap_weighted": float(row_series.get("n_overlap_weighted", 0.0) or 0.0),
            "association_support_n_unweighted": int(row_series.get("n_overlap_unweighted", 0) or 0),
            "association_support_n_weighted": float(row_series.get("n_overlap_weighted", 0.0) or 0.0),
            "association_support_threshold": support_threshold_value,
            "association_support_ratio": round(_support_ratio_val, 6),
            "association_support_margin": support_margin,
            "association_support_gate_status": association_support_gate_status,
            "association_publication_status": association_publication_status,
            "association_publication_reason": association_publication_reason,
            "p_response_given_pattern": float(row_series.get("p_response_given_pattern", 0.0) or 0.0),
            "p_response_baseline": float(row_series.get("p_response_baseline", 0.0) or 0.0),
            "denominator_basis": "answered_var_within_pattern",
            "baseline_denominator_basis": "eligible_context",
            "difference_from_baseline": float(row_series.get("difference_from_baseline", 0.0) or 0.0),
            "lift": float(row_series.get("lift", 0.0) or 0.0),
            "mutual_information": float(row_series.get("mutual_information", 0.0) or 0.0),
            "support_threshold": support_threshold_value,
            "support_ratio": support_ratio,
            "support_gate_status": association_support_gate_status,
            "suppression_reason": suppression_reason,
            "would_emit_as_diagnostic": True,
            "would_emit_as_publishable": would_emit_as_publishable,
            "association_eligibility_status": row_status,
            "direct_evidence_status": direct_evidence_status,
            "association_lane": association_lane,
            "association_lane_status": association_lane_status,
            "association_lane_authority_source": association_lane_rule_id if association_lane_rule_id else "lane_classifier",
            "association_lane_basis": "registry" if association_lane_rule_id else "computed",
            "association_lane_resolution_type": _association_lane_resolution_type(association_lane_status),
            "association_lane_authority_status": _association_lane_authority_status(association_lane_status),
            "association_lane_publishability": _association_lane_publishability(association_lane),
            "associated_response_total_n": int(row_series.get("associated_response_total_n", 0) or 0),
            "associated_response_total_weighted_n": int(row_series.get("associated_response_total_weighted_n", 0) or 0),
            "associated_response_baseline_share": round(float(row_series.get("associated_response_baseline_share", 0.0) or 0.0), 6),
            "associated_var_distinct_response_count": int(row_series.get("associated_var_distinct_response_count", 0) or 0),
            "associated_var_effective_cardinality": int(row_series.get("associated_var_effective_cardinality", 0) or 0),
            "associated_var_cardinality_band": _clean(row_series.get("associated_var_cardinality_band", "unknown_cardinality")),
            "is_high_cardinality_associated_var": _is_high_card,
            "is_sparse_associated_response": _is_sparse,
            "is_raw_occupational_status_code": _is_occ,
            "is_same_family_association": _is_same_fam,
            "is_same_variable_association": _is_same_var,
            "association_publication_status": association_publication_status,
            "association_publication_reason": association_publication_reason,
            "association_support_gate_status": support_gate_status,
            "association_support_n_unweighted": int(row_series.get("n_overlap_unweighted", 0) or 0),
            "association_support_n_weighted": float(row_series.get("n_overlap_weighted", 0.0) or 0.0),
            "association_support_threshold": 5,
            "association_context_status": "outside_family_context_authorized",
            "association_status": "outside_family_association" if would_emit_as_publishable else "diagnostic_association",
            "association_gate_status": "publishable" if would_emit_as_publishable else "diagnostic_only",
            "association_strength_status": "not_computed_phase4_pending",
            "support_status": _clean(row_series.get("pattern_support_status", "")),
            "confidence_tier": _association_confidence_tier(
                pattern_confidence_score=row_series.get("confidence_score", 0.0),
                association_support_gate_status=association_support_gate_status,
                association_publication_status=association_publication_status,
                association_lane_publishability=_association_lane_publishability(association_lane),
                association_context_status="outside_family_context_authorized",
            ),
            "formula_id": "joint_pattern_association_raw_components_v1",
            "formula_version": "v1",
            "created_at": utc_now(),
            "schema_version": V550J_SCHEMA_VERSION,
        }
        if emit_diagnostics or would_emit_as_publishable:
            rows.append(payload)
    trace_df = pd.DataFrame(rows)
    if trace_df.empty:
        trace_df = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
    trace_df.attrs["blocked_not_direct_pairs"] = len(blocked_not_direct_pairs)
    trace_df.attrs["blocked_metadata_pairs"] = len(blocked_metadata_pairs)
    trace_df.attrs["blocked_missing_authority_pairs"] = len(blocked_missing_authority_pairs)
    trace_df.attrs["candidate_pairs_formed"] = candidate_pairs_formed
    trace_df.attrs["candidate_pairs_published"] = candidate_pairs_published
    trace_df.attrs["candidate_pairs_suppressed_missing_response_value"] = eligible_rows_missing_response_value
    trace_df.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = suppressed_no_candidate_pairs_formed
    trace_df.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = suppressed_no_pattern_member_overlap
    trace_df.attrs["candidate_pairs_suppressed_low_response_overlap"] = suppressed_low_response_overlap
    trace_df.attrs["candidate_pairs_suppressed_low_baseline"] = suppressed_low_baseline
    trace_df.attrs["candidate_pairs_suppressed_low_pattern_support"] = suppressed_low_pattern_support
    trace_df.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = suppressed_effect_size_zero_or_trivial
    trace_df.attrs["eligible_rows_with_response_value"] = len(eligible_df)
    trace_df.attrs["eligible_rows_missing_response_value"] = eligible_rows_missing_response_value
    return trace_df


def _association_candidate_trace_rows(
    pattern_df: pd.DataFrame,
    respondent_df: pd.DataFrame,
    *,
    context_frame: pd.DataFrame | None = None,
    family_var_codes: set[str] | None = None,
    pattern_membership_lookup: dict[str, set[str]] | None = None,
    pattern_membership_frame: pd.DataFrame | None = None,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
    association_support_threshold: int | None = None,
    publish_association_lanes: set[str] | None = None,
    association_lane_overrides: dict[str, Any] | None = None,
    progress: Any | None = None,
    emit_diagnostics: bool = True,
    registry: Any = None,
) -> pd.DataFrame:
    association_support_threshold_value = _association_support_threshold(
        association_support_threshold
    )
    if pattern_df.empty:
        return pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
    if pattern_membership_frame is None and not pattern_df.empty and not respondent_df.empty:
        synthetic_membership = _pattern_membership_rows(
            respondent_df,
            pattern_df,
            run_id=run_id,
            source_id=source_id,
            source=source,
            wave=wave,
            canonical_wave=canonical_wave,
            country_code=country_code,
        )
        if not synthetic_membership.empty:
            pattern_membership_frame = synthetic_membership
    if pattern_membership_frame is not None and not pattern_membership_frame.empty:
        fast_trace = _association_candidate_trace_rows_fast(
            pattern_df,
            respondent_df,
            context_frame=context_frame,
            family_var_codes=family_var_codes,
            pattern_membership_frame=pattern_membership_frame,
            run_id=run_id,
            source_id=source_id,
            source=source,
            wave=wave,
            canonical_wave=canonical_wave,
            country_code=country_code,
            association_support_threshold=association_support_threshold,
            publish_association_lanes=publish_association_lanes,
            association_lane_overrides=association_lane_overrides,
            emit_diagnostics=emit_diagnostics,
            registry=registry,
        )
        if fast_trace is not None:
            return fast_trace
    baseline_frame = context_frame if context_frame is not None and not context_frame.empty else respondent_df
    if baseline_frame.empty or "var_code" not in baseline_frame.columns or "respondent_id" not in baseline_frame.columns:
        empty = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
        empty.attrs["blocked_not_direct_pairs"] = 0
        empty.attrs["blocked_metadata_pairs"] = 0
        empty.attrs["blocked_missing_authority_pairs"] = 0
        empty.attrs["candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_published"] = 0
        empty.attrs["candidate_pairs_suppressed_missing_response_value"] = 0
        empty.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_response_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_baseline"] = 0
        empty.attrs["candidate_pairs_suppressed_low_pattern_support"] = 0
        empty.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = 0
        empty.attrs["eligible_rows_with_response_value"] = 0
        empty.attrs["eligible_rows_missing_response_value"] = 0
        return empty
    outside_family_frame = _ensure_association_response_value_columns(baseline_frame)
    if family_var_codes is None:
        family_var_codes = set()
    family_var_codes = {str(code).upper() for code in family_var_codes if str(code).strip()}
    if family_var_codes and "var_code" in outside_family_frame.columns:
        outside_family_frame = outside_family_frame[~outside_family_frame["var_code"].astype(str).str.upper().isin(family_var_codes)].copy()
    if outside_family_frame.empty:
        empty = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
        empty.attrs["blocked_not_direct_pairs"] = 0
        empty.attrs["blocked_metadata_pairs"] = 0
        empty.attrs["blocked_missing_authority_pairs"] = 0
        empty.attrs["candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_published"] = 0
        empty.attrs["candidate_pairs_suppressed_missing_response_value"] = 0
        empty.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_response_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_baseline"] = 0
        empty.attrs["candidate_pairs_suppressed_low_pattern_support"] = 0
        empty.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = 0
        empty.attrs["eligible_rows_with_response_value"] = 0
        empty.attrs["eligible_rows_missing_response_value"] = 0
        return empty
    if _association_authority_status(outside_family_frame) != "has_association_authority":
        empty = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
        empty.attrs["blocked_not_direct_pairs"] = 0
        empty.attrs["blocked_metadata_pairs"] = 0
        empty.attrs["blocked_missing_authority_pairs"] = 0
        empty.attrs["candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_published"] = 0
        empty.attrs["candidate_pairs_suppressed_missing_response_value"] = 0
        empty.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_response_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_baseline"] = 0
        empty.attrs["candidate_pairs_suppressed_low_pattern_support"] = 0
        empty.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = 0
        empty.attrs["eligible_rows_with_response_value"] = 0
        empty.attrs["eligible_rows_missing_response_value"] = 0
        return empty
    outside_family_frame = _ensure_association_response_value_columns(outside_family_frame)

    eligible_rows: list[dict[str, Any]] = []
    blocked_not_direct_pairs: set[tuple[str, str]] = set()
    blocked_metadata_pairs: set[tuple[str, str]] = set()
    blocked_missing_authority_pairs: set[tuple[str, str]] = set()
    eligible_rows_missing_response_value = 0
    for row in outside_family_frame.itertuples(index=False):
        var_code = str(getattr(row, "var_code", "")).upper()
        response_value = _fallback_response_value(row)
        if not var_code or var_code in family_var_codes:
            continue
        if not response_value:
            eligible_rows_missing_response_value += 1
            continue
        row_status, direct_evidence_status = _association_row_status(row)
        pair_key = (var_code, response_value)
        if row_status == "blocked_not_direct_evidence":
            blocked_not_direct_pairs.add(pair_key)
            continue
        if row_status == "blocked_metadata_context":
            blocked_metadata_pairs.add(pair_key)
            continue
        if row_status == "blocked_missing_authority":
            blocked_missing_authority_pairs.add(pair_key)
            continue
        record = row._asdict()
        record["_association_eligibility_status"] = row_status
        record["_direct_evidence_status"] = direct_evidence_status
        eligible_rows.append(record)

    if not eligible_rows:
        empty = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
        empty.attrs["blocked_not_direct_pairs"] = len(blocked_not_direct_pairs)
        empty.attrs["blocked_metadata_pairs"] = len(blocked_metadata_pairs)
        empty.attrs["blocked_missing_authority_pairs"] = len(blocked_missing_authority_pairs)
        empty.attrs["candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_published"] = 0
        empty.attrs["candidate_pairs_suppressed_missing_response_value"] = eligible_rows_missing_response_value
        empty.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_response_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_baseline"] = 0
        empty.attrs["candidate_pairs_suppressed_low_pattern_support"] = 0
        empty.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = 0
        empty.attrs["eligible_rows_with_response_value"] = 0
        empty.attrs["eligible_rows_missing_response_value"] = eligible_rows_missing_response_value
        return empty

    baseline_frame = pd.DataFrame(eligible_rows)
    if baseline_frame.empty or "respondent_id" not in baseline_frame.columns or "var_code" not in baseline_frame.columns:
        empty = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
        empty.attrs["blocked_not_direct_pairs"] = len(blocked_not_direct_pairs)
        empty.attrs["blocked_metadata_pairs"] = len(blocked_metadata_pairs)
        empty.attrs["blocked_missing_authority_pairs"] = len(blocked_missing_authority_pairs)
        empty.attrs["candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_published"] = 0
        empty.attrs["candidate_pairs_suppressed_missing_response_value"] = eligible_rows_missing_response_value
        empty.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = 0
        empty.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_response_overlap"] = 0
        empty.attrs["candidate_pairs_suppressed_low_baseline"] = 0
        empty.attrs["candidate_pairs_suppressed_low_pattern_support"] = 0
        empty.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = 0
        empty.attrs["eligible_rows_with_response_value"] = len(eligible_rows)
        empty.attrs["eligible_rows_missing_response_value"] = eligible_rows_missing_response_value
        return empty
    rows: list[dict[str, Any]] = []
    candidate_pairs_formed = 0
    candidate_pairs_published = 0
    suppressed_missing_response_value = eligible_rows_missing_response_value
    suppressed_no_candidate_pairs_formed = 0
    suppressed_no_pattern_member_overlap = 0
    suppressed_low_response_overlap = 0
    suppressed_low_baseline = 0
    suppressed_low_pattern_support = 0
    suppressed_effect_size_zero_or_trivial = 0
    family_count = int(len(respondent_df)) if not respondent_df.empty else 0
    total_patterns = int(len(pattern_df))
    progress_stride = max(1, total_patterns // 10) if total_patterns else 1
    item_baselines: dict[str, Counter[str]] = defaultdict(Counter)
    item_totals: dict[str, float] = defaultdict(float)
    for row in baseline_frame.itertuples(index=False):
        var_code = str(getattr(row, "var_code", "")).upper()
        if not var_code or var_code in family_var_codes:
            continue
        response_value = _fallback_response_value(row)
        if not response_value:
            continue
        weight = _safe_float(getattr(row, "weight_value", None))
        weight = weight if weight is not None and weight > 0 else 1.0
        item_baselines[var_code][response_value] += weight
        item_totals[var_code] += weight
    for pattern_index, pattern in enumerate(pattern_df.itertuples(index=False), start=1):
        if progress is not None and (pattern_index == 1 or pattern_index == total_patterns or pattern_index % progress_stride == 0):
            progress.stage(7, 8, f"{_clean(getattr(pattern, 'family_id', 'family'))}: association candidate trace", f"pattern {pattern_index}/{total_patterns}")
        member_ids = set()
        if pattern_membership_lookup is not None:
            member_ids = {str(rid) for rid in pattern_membership_lookup.get(str(pattern.pattern_id), set()) if _clean(rid)}
        if not member_ids:
            member_ids = {str(rid) for rid in pattern.respondent_ids}
        group = baseline_frame[baseline_frame["respondent_id"].astype(str).isin(member_ids)]
        if group.empty:
            continue
        outside_group = group[~group["var_code"].astype(str).str.upper().isin(family_var_codes)] if family_var_codes else group.copy()
        if outside_group.empty:
            continue
        pattern_var_counts: dict[str, Counter[str]] = defaultdict(Counter)
        pattern_var_weights: dict[str, float] = defaultdict(float)
        pattern_var_respondents: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
        pattern_var_totals: dict[str, set[str]] = defaultdict(set)
        for row in outside_group.itertuples(index=False):
            var_code = str(getattr(row, "var_code", "")).upper()
            response_value = _fallback_response_value(row)
            respondent_id = _clean(getattr(row, "respondent_id", ""))
            if not var_code or not response_value:
                continue
            weight = _safe_float(getattr(row, "weight_value", None))
            weight = weight if weight is not None and weight > 0 else 1.0
            pattern_var_counts[var_code][response_value] += weight
            pattern_var_weights[var_code] += weight
            if respondent_id:
                pattern_var_respondents[var_code][response_value].add(respondent_id)
                pattern_var_totals[var_code].add(respondent_id)
        pattern_candidate_count = 0
        for var_code, response_counts in pattern_var_counts.items():
            baseline_total = item_totals.get(var_code, 0.0)
            if baseline_total <= 0:
                suppressed_low_baseline += len(response_counts)
                continue
            for observed_value, observed_weight in response_counts.items():
                pair_key = (var_code, observed_value)
                if pair_key in blocked_not_direct_pairs or pair_key in blocked_metadata_pairs:
                    continue
                candidate_pairs_formed += 1
                baseline_count = item_baselines.get(var_code, Counter()).get(observed_value, 0.0)
                baseline_share = baseline_count / baseline_total if baseline_total else 0.0
                p_given_pattern = observed_weight / max(1e-12, pattern_var_weights.get(var_code, 0.0))
                lift = None if baseline_share <= 0 else p_given_pattern / baseline_share
                difference = p_given_pattern - baseline_share
                mutual_information = None
                if baseline_share > 0 and p_given_pattern > 0:
                    mutual_information = math.log2(max(1e-12, p_given_pattern / baseline_share)) * (pattern.pattern_count_unweighted / max(1, family_count))
                overlap_n_unweighted = len(pattern_var_respondents[var_code].get(observed_value, set()))
                overlap_n_weighted = observed_weight
                answered_var_n_unweighted = len(pattern_var_totals.get(var_code, set()))
                answered_var_n_weighted = float(pattern_var_weights.get(var_code, 0.0))
                support_threshold = association_support_threshold_value
                support_ratio = None
                support_gate_status = (
                    "zero_overlap"
                    if overlap_n_unweighted <= 0
                    else "below_threshold"
                    if overlap_n_unweighted < support_threshold
                    else "sufficient_support"
                )
                if support_threshold > 0:
                    support_ratio = float(overlap_n_unweighted / float(support_threshold))
                suppression_reason = "not_suppressed"
                would_emit_as_publishable = True
                would_emit_as_diagnostic = True
                association_strength_status = "not_computed_phase4_pending"
                if answered_var_n_unweighted <= 0 or answered_var_n_weighted <= 0:
                    suppression_reason = "eligible_rows_missing_response_value"
                    would_emit_as_publishable = False
                elif overlap_n_unweighted <= 0:
                    suppression_reason = "no_pattern_member_overlap"
                    would_emit_as_publishable = False
                elif support_gate_status != "sufficient_support":
                    suppression_reason = "low_response_overlap"
                    would_emit_as_publishable = False
                    suppressed_low_response_overlap += 1
                elif baseline_share <= 0:
                    suppression_reason = "low_baseline_support"
                    would_emit_as_publishable = False
                    suppressed_low_baseline += 1
                elif difference <= 0 and (lift is None or lift <= 1.0):
                    suppression_reason = "not_suppressed"
                    would_emit_as_publishable = True
                    association_strength_status = "low_effect_size_but_publishable"
                if would_emit_as_publishable:
                    candidate_pairs_published += 1
                row_lookup = baseline_frame[
                    (baseline_frame["var_code"].astype(str).str.upper() == var_code)
                    & (baseline_frame["response_value_normalized"].astype(str) == observed_value)
                ]
                row_status = _clean(row_lookup.iloc[0].get("_association_eligibility_status", "eligible")) if not row_lookup.empty else "eligible"
                direct_evidence_status = _clean(row_lookup.iloc[0].get("_direct_evidence_status", "direct_or_not_flagged")) if not row_lookup.empty else "direct_or_not_flagged"
                association_lane, association_lane_status, association_lane_rule_id = _association_lane(
                    row, row_status, direct_evidence_status,
                    registry=registry, source=source, wave=wave, country_code=country_code,
                )
                _dc_rel, _effective_dc_rel, _dc_band_rel, _dc_is_high_rel = _compute_associated_var_cardinality(baseline_frame, var_code)
                _rtn_rel, _rbs_rel, _rtwn_rel = _compute_associated_response_total_support(baseline_frame, var_code, observed_value)
                _is_occ_rel = _is_raw_occupational_status_code(var_code)
                _is_high_card_rel = _dc_is_high_rel
                _is_sparse_rel = _is_sparse_associated_response(_rtn_rel)
                _auth_source = association_lane_rule_id if association_lane_rule_id else "lane_classifier"
                _auth_basis = "registry" if association_lane_rule_id else "computed"
                association_publication_status, association_publication_reason, would_emit_as_publishable = _association_publication_status(
                    support_gate_status=support_gate_status,
                    association_lane=association_lane,
                    association_lane_status=association_lane_status,
                    row_status=row_status,
                    direct_evidence_status=direct_evidence_status,
                    is_same_variable=_check_same_variable_association(var_code, family_var_codes),
                    is_same_family=_check_same_family_association(var_code, family_var_codes),
                    is_raw_occupational=_is_occ_rel,
                    is_high_cardinality=_is_high_card_rel,
                    is_sparse_response=_is_sparse_rel,
                    n_overlap_unweighted=overlap_n_unweighted,
                    association_support_threshold=association_support_threshold_value,
                    associated_var_distinct_response_count=_dc_rel,
                    associated_response_total_n=_rtn_rel,
                    association_support_n_unweighted=overlap_n_unweighted,
                    pattern_member_n_unweighted=pattern.pattern_count_unweighted,
                    association_support_ratio=overlap_n_unweighted / max(1, pattern.pattern_count_unweighted),
                    difference_from_baseline=difference,
                    publishable_lanes=publish_association_lanes,
                )
                candidate_stage = "candidate_pair_publishable" if would_emit_as_publishable else "candidate_pair_suppressed"
                row_payload = {
                        "run_id": _clean(getattr(pattern, "run_id", "")),
                        "source_id": _clean(getattr(pattern, "source", "")),
                        "source": _clean(getattr(pattern, "source", "")),
                        "wave": _clean(getattr(pattern, "wave", "")),
                        "canonical_wave": _clean(getattr(pattern, "canonical_wave", "")),
                        "country_code": _clean(getattr(pattern, "country_code", "")),
                        "pattern_id": pattern.pattern_id,
                        "family_id": pattern.family_id,
                        "var_code": var_code,
                        "question_id": "",
                        "item_role": "outside_family",
                        "condition_label": "",
                        "associated_var_code": var_code,
                        "associated_question_id": "",
                        "associated_response_value": observed_value,
                        "associated_response_value_normalized": observed_value,
                        "associated_response_label": observed_value,
                        "associated_response_direction": "",
                        "candidate_stage": candidate_stage,
                        "pattern_member_n_unweighted": pattern.pattern_count_unweighted,
                        "pattern_member_n_weighted": pattern.pattern_count_weighted,
                        "eligible_rows_for_var": int(len(baseline_frame[baseline_frame["var_code"].astype(str).str.upper() == var_code])),
                        "eligible_rows_with_response_value": int(len(baseline_frame[(baseline_frame["var_code"].astype(str).str.upper() == var_code) & (baseline_frame["response_value_normalized"].astype(str).str.len() > 0)])),
                        "pattern_member_rows_for_var": answered_var_n_unweighted,
                        "response_overlap_n_unweighted": overlap_n_unweighted,
                        "response_overlap_n_weighted": overlap_n_weighted,
                        "baseline_answered_n_unweighted": answered_var_n_unweighted,
                        "baseline_answered_n_weighted": answered_var_n_weighted,
                        "pattern_var_answered_n_unweighted": answered_var_n_unweighted,
                        "pattern_var_answered_n_weighted": answered_var_n_weighted,
                        "pattern_answered_var_n_unweighted": answered_var_n_unweighted,
                        "pattern_answered_var_n_weighted": answered_var_n_weighted,
                        "n_overlap_unweighted": overlap_n_unweighted,
                        "n_overlap_weighted": overlap_n_weighted,
                        "p_response_given_pattern": p_given_pattern,
                        "p_response_baseline": baseline_share,
                        "denominator_basis": "answered_var_within_pattern",
                        "baseline_denominator_basis": "eligible_context",
                        "difference_from_baseline": difference,
                        "lift": lift if lift is not None else 0.0,
                        "mutual_information": mutual_information if mutual_information is not None else 0.0,
                        "support_threshold": support_threshold,
                        "support_ratio": support_ratio if support_ratio is not None else 0.0,
                        "support_gate_status": support_gate_status,
                        "suppression_reason": suppression_reason,
                        "would_emit_as_diagnostic": would_emit_as_diagnostic,
                        "would_emit_as_publishable": would_emit_as_publishable,
                        "association_eligibility_status": row_status,
                        "direct_evidence_status": direct_evidence_status,
                        "association_lane": association_lane,
                        "association_lane_status": association_lane_status,
                        "association_lane_authority_source": _auth_source,
                        "association_lane_basis": _auth_basis,
                        "association_lane_resolution_type": _association_lane_resolution_type(association_lane_status),
                        "association_lane_authority_status": _association_lane_authority_status(association_lane_status),
                        "association_context_status": "outside_family_context_authorized",
                        "association_publication_status": association_publication_status,
                        "association_publication_reason": association_publication_reason,
                        "association_support_gate_status": support_gate_status,
                        "association_lane_publishability": _association_lane_publishability(association_lane),
                        "associated_response_total_n": _rtn_rel,
                        "associated_response_total_weighted_n": _rtwn_rel,
                        "associated_response_baseline_share": round(_rbs_rel, 6),
                        "associated_var_distinct_response_count": _dc_rel,
                        "associated_var_effective_cardinality": _dc_rel,
                        "associated_var_cardinality_band": _dc_band_rel,
                        "is_high_cardinality_associated_var": _is_high_card_rel,
                        "is_sparse_associated_response": _is_sparse_rel,
                        "is_raw_occupational_status_code": _is_occ_rel,
                        "is_same_family_association": False,
                        "is_same_variable_association": False,
                        "association_support_n_unweighted": overlap_n_unweighted,
                        "association_support_n_weighted": overlap_n_weighted,
                        "association_support_threshold": support_threshold,
                        "association_status": "outside_family_association" if would_emit_as_publishable else "diagnostic_association",
                        "association_gate_status": "raw_components_only" if would_emit_as_publishable else "diagnostic_only",
                        "association_strength_status": association_strength_status if would_emit_as_publishable else "not_computed_phase4_pending",
                        "support_status": pattern.support_status,
                        "confidence_tier": _association_confidence_tier(
                            pattern_confidence_score=getattr(pattern, "confidence_score", 0.0),
                            association_support_gate_status=support_gate_status,
                            association_publication_status=association_publication_status,
                            association_lane_publishability=_association_lane_publishability(association_lane),
                            association_context_status="outside_family_context_authorized",
                        ),
                        "formula_id": "joint_pattern_association_raw_components_v1",
                        "formula_version": "v1",
                        "created_at": utc_now(),
                        "schema_version": V550J_SCHEMA_VERSION,
                    }
                if emit_diagnostics or would_emit_as_publishable:
                    rows.append(row_payload)
                pattern_candidate_count += 1
        if pattern_candidate_count <= 0:
            row_payload = {
                "run_id": _clean(run_id),
                "source_id": _clean(source_id) or _clean(source),
                "source": _clean(source),
                "wave": _clean(wave),
                "canonical_wave": _clean(canonical_wave) or _clean(wave),
                "country_code": _clean(country_code),
                "pattern_id": pattern.pattern_id,
                "family_id": pattern.family_id,
                "var_code": "",
                "question_id": "",
                "item_role": "outside_family",
                "condition_label": "",
                "associated_var_code": "",
                "associated_question_id": "",
                "associated_response_value": "",
                "associated_response_value_normalized": "",
                "associated_response_label": "",
                "associated_response_direction": "",
                "candidate_stage": "no_candidate_pairs_formed",
                "pattern_member_n_unweighted": pattern.pattern_count_unweighted,
                "pattern_member_n_weighted": pattern.pattern_count_weighted,
                "eligible_rows_for_var": 0,
                "eligible_rows_with_response_value": eligible_rows_missing_response_value,
                "pattern_member_rows_for_var": 0,
                "response_overlap_n_unweighted": 0,
                "response_overlap_n_weighted": 0.0,
                "baseline_answered_n_unweighted": 0,
                "baseline_answered_n_weighted": 0.0,
                "pattern_var_answered_n_unweighted": 0,
                "pattern_var_answered_n_weighted": 0.0,
                "pattern_answered_var_n_unweighted": 0,
                "pattern_answered_var_n_weighted": 0.0,
                "n_overlap_unweighted": 0,
                "n_overlap_weighted": 0.0,
                "association_support_n_unweighted": 0,
                "association_support_n_weighted": 0.0,
                "association_support_threshold": association_support_threshold_value,
                "association_support_ratio": 0.0,
                "association_support_margin": -association_support_threshold_value,
                "association_support_gate_status": "missing_denominator",
                "association_publication_status": "not_computable",
                "association_publication_reason": "no_candidate_pairs_formed",
                "p_response_given_pattern": 0.0,
                "p_response_baseline": 0.0,
                "denominator_basis": "answered_var_within_pattern",
                "baseline_denominator_basis": "eligible_context",
                "difference_from_baseline": 0.0,
                "lift": 0.0,
                "mutual_information": 0.0,
                "support_threshold": association_support_threshold_value,
                "support_ratio": 0.0,
                "support_gate_status": "missing_denominator",
                "suppression_reason": "no_candidate_pairs_formed",
                "would_emit_as_diagnostic": True,
                "would_emit_as_publishable": False,
                "association_eligibility_status": "eligible",
                "direct_evidence_status": "direct_or_not_flagged",
                "association_lane": "unknown_association_lane",
                "association_lane_status": "diagnostic",
                "association_context_status": "outside_family_context_authorized",
                "association_status": "diagnostic_association",
                "association_gate_status": "diagnostic_only",
                "association_strength_status": "not_computed_phase4_pending",
                "support_status": pattern.support_status,
                "confidence_tier": _association_confidence_tier(
                    pattern_confidence_score=getattr(pattern, "confidence_score", 0.0),
                    association_support_gate_status=support_gate_status,
                    association_publication_status="not_computable",
                    association_lane_publishability=_association_lane_publishability(association_lane),
                    association_context_status="outside_family_context_authorized",
                ),
                "formula_id": "joint_pattern_association_raw_components_v1",
                "formula_version": "v1",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
            if emit_diagnostics:
                rows.append(row_payload)
            suppressed_no_candidate_pairs_formed += 1
    trace_df = pd.DataFrame(rows)
    if trace_df.empty:
        trace_df = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
    trace_df.attrs["blocked_not_direct_pairs"] = len(blocked_not_direct_pairs)
    trace_df.attrs["blocked_metadata_pairs"] = len(blocked_metadata_pairs)
    trace_df.attrs["blocked_missing_authority_pairs"] = len(blocked_missing_authority_pairs)
    trace_df.attrs["candidate_pairs_formed"] = candidate_pairs_formed
    trace_df.attrs["candidate_pairs_published"] = candidate_pairs_published
    trace_df.attrs["candidate_pairs_suppressed_missing_response_value"] = suppressed_missing_response_value
    trace_df.attrs["candidate_pairs_suppressed_no_candidate_pairs_formed"] = suppressed_no_candidate_pairs_formed
    trace_df.attrs["candidate_pairs_suppressed_no_pattern_member_overlap"] = suppressed_no_pattern_member_overlap
    trace_df.attrs["candidate_pairs_suppressed_low_response_overlap"] = suppressed_low_response_overlap
    trace_df.attrs["candidate_pairs_suppressed_low_baseline"] = suppressed_low_baseline
    trace_df.attrs["candidate_pairs_suppressed_low_pattern_support"] = suppressed_low_pattern_support
    trace_df.attrs["candidate_pairs_suppressed_effect_size_zero_or_trivial"] = suppressed_effect_size_zero_or_trivial
    trace_df.attrs["eligible_rows_with_response_value"] = len(eligible_rows)
    trace_df.attrs["eligible_rows_missing_response_value"] = eligible_rows_missing_response_value
    return trace_df


def _association_rows(
    pattern_df: pd.DataFrame,
    respondent_df: pd.DataFrame,
    *,
    context_frame: pd.DataFrame | None = None,
    family_var_codes: set[str] | None = None,
    pattern_membership_lookup: dict[str, set[str]] | None = None,
    pattern_membership_frame: pd.DataFrame | None = None,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
    association_support_threshold: int | None = None,
    publish_association_lanes: set[str] | None = None,
    association_lane_overrides: dict[str, Any] | None = None,
    emit_diagnostics: bool = True,
    registry: Any = None,
) -> pd.DataFrame:
    trace_df = _association_candidate_trace_rows(
        pattern_df,
        respondent_df,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
        pattern_membership_lookup=pattern_membership_lookup,
        pattern_membership_frame=pattern_membership_frame,
        run_id=run_id,
        source_id=source_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
        association_support_threshold=association_support_threshold,
        registry=registry,
        publish_association_lanes=publish_association_lanes,
        association_lane_overrides=association_lane_overrides,
        emit_diagnostics=emit_diagnostics,
    )
    if trace_df.empty:
        empty = _empty_association_index()
        empty.attrs.update(trace_df.attrs)
        return empty
    publication_mask = _association_publication_mask(trace_df, publishable_lanes=publish_association_lanes)
    rows = trace_df[publication_mask].copy()
    if not rows.empty:
        rows = rows[[column for column in V550J_ASSOCIATION_INDEX_COLUMNS if column in rows.columns]].copy()
    if rows.empty:
        rows = _empty_association_index()
    else:
        _validate_association_index_publication_constraints(rows, publishable_lanes=publish_association_lanes)
    rows.attrs.update(trace_df.attrs)
    return rows


def _position_signature_rows(
    pattern_df: pd.DataFrame,
    respondent_df: pd.DataFrame,
    *,
    pattern_membership_lookup: dict[str, set[str]] | None = None,
) -> pd.DataFrame:
    if pattern_df.empty or respondent_df.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    baseline_total = len(respondent_df)
    for pattern in pattern_df.itertuples(index=False):
        member_ids = set()
        if pattern_membership_lookup is not None:
            member_ids = {str(rid) for rid in pattern_membership_lookup.get(str(pattern.pattern_id), set()) if _clean(rid)}
        if not member_ids:
            member_ids = {str(rid) for rid in pattern.respondent_ids}
        group = respondent_df[respondent_df["respondent_id"].isin(member_ids)]
        if group.empty:
            continue
        weight_status = _clean(getattr(pattern, "weight_status", "unweighted_only"))
        use_weighted = weight_status == "weighted_valid" and "weight_value" in group.columns and group["weight_value"].notna().all()
        for field in POSITION_FIELDS:
            if field not in group.columns or field not in respondent_df.columns:
                continue
            if use_weighted:
                pattern_counts = group.groupby(field, dropna=False)["weight_value"].sum()
                baseline_counts = respondent_df.groupby(field, dropna=False)["weight_value"].sum()
                pattern_total = float(group["weight_value"].fillna(0.0).clip(lower=0).sum())
                baseline_total_weighted = float(respondent_df["weight_value"].fillna(0.0).clip(lower=0).sum())
                weight_basis = "weighted_valid"
            else:
                pattern_counts = group[field].fillna("").astype(str).value_counts()
                baseline_counts = respondent_df[field].fillna("").astype(str).value_counts()
                pattern_total = float(len(group))
                baseline_total_weighted = float(len(respondent_df))
                weight_basis = "unweighted_fallback"
            for value, count in pattern_counts.items():
                if not value or value.lower() in {"nan", "none"}:
                    continue
                baseline_count = float(baseline_counts.get(value, 0))
                pattern_share = float(count) / pattern_total if pattern_total else 0.0
                baseline_share = baseline_count / baseline_total_weighted if baseline_total_weighted else 0.0
                lift = None if baseline_share <= 0 else pattern_share / baseline_share
                pattern_support_status = _clean(getattr(pattern, "support_status", ""))
                pattern_support_n_unweighted = int(getattr(pattern, "pattern_count_unweighted", 0) or 0)
                pattern_support_n_weighted = float(getattr(pattern, "pattern_count_weighted", 0.0) or 0.0)
                pattern_support_gate_status = _clean(getattr(pattern, "support_gate_status", ""))
                cell_n_unweighted = int(group[field].fillna("").astype(str).eq(str(value)).sum())
                cell_n_weighted = float(count)
                cell_support_status = support_status_from_count(
                    cell_n_unweighted,
                    total_respondents=baseline_total,
                    lane="relation",
                )
                cell_support_gate_status = cell_support_status
                rows.append(
                    {
                        "pattern_id": pattern.pattern_id,
                        "family_id": pattern.family_id,
                        "indicator_name": field,
                        "indicator_value": value,
                        "pattern_pct_with_indicator": pattern_share,
                        "baseline_pct_with_indicator": baseline_share,
                        "lift": lift if lift is not None else 0.0,
                        "risk_difference": pattern_share - baseline_share,
                        "n_unweighted": cell_n_unweighted,
                        "n_weighted": cell_n_weighted,
                        "pattern_pct_weighted": pattern_share,
                        "baseline_pct_weighted": baseline_share,
                        "position_signature_weight_basis": weight_basis,
                        "weight_status": weight_status,
                        "pattern_support_status": pattern_support_status,
                        "pattern_support_n_unweighted": pattern_support_n_unweighted,
                        "pattern_support_n_weighted": pattern_support_n_weighted,
                        "pattern_support_gate_status": pattern_support_gate_status,
                        "position_cell_support_status": cell_support_status,
                        "position_cell_n_unweighted": cell_n_unweighted,
                        "position_cell_n_weighted": cell_n_weighted,
                        "position_cell_support_ratio": pattern_share,
                        "position_cell_support_gate_status": cell_support_gate_status,
                        "support_status": pattern_support_status,
                        "confidence_tier": _confidence_tier_from_score(getattr(pattern, "confidence_score", 0.0)),
                        "created_at": utc_now(),
                        "schema_version": V550J_SCHEMA_VERSION,
                    }
                )
    return pd.DataFrame(rows)


def _relation_signature_rows(pattern_df: pd.DataFrame) -> pd.DataFrame:
    if pattern_df.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for pattern in pattern_df.itertuples(index=False):
        driver_ids = sorted({str(item.get("driver_id", "")).strip() for item in pattern.item_rows if _clean(item.get("driver_id", ""))})
        driver_facet_ids = sorted({str(item.get("driver_facet_id", "")).strip() for item in pattern.item_rows if _clean(item.get("driver_facet_id", ""))})
        relation_axis_ids = sorted({str(item.get("relation_axis_id", "")).strip() for item in pattern.item_rows if _clean(item.get("relation_axis_id", ""))})
        target_entity_ids = sorted({str(item.get("target_entity_id", "")).strip() for item in pattern.item_rows if _clean(item.get("target_entity_id", ""))})
        mapping_statuses = Counter(_clean(item.get("mapping_status", "")) or "unknown" for item in pattern.item_rows)
        semantic_roles = Counter(_clean(item.get("semantic_role", "")) or "unknown" for item in pattern.item_rows)
        support_roles = Counter(_clean(item.get("v551_evidence_role", "")) or "unknown" for item in pattern.item_rows)
        n_questions_mapped = sum(1 for item in pattern.item_rows if _clean(item.get("mapping_status", "")) and _clean(item.get("mapping_status", "")).lower() not in {"unknown", "missing"})
        n_questions_unmapped = sum(1 for item in pattern.item_rows if not _clean(item.get("mapping_status", "")) or _clean(item.get("mapping_status", "")).lower() in {"unknown", "missing"})
        family_structure_type = _clean(getattr(pattern, "family_structure_type", "")) or _clean(getattr(pattern, "family_type", ""))
        expected_multi_target = _to_bool(getattr(pattern, "expected_multi_target", False), False)
        target_structure_status = "single_target_battery"
        target_selectivity_profile = "not_applicable"
        if expected_multi_target or family_structure_type in {"target_selective_tolerance_battery", "target_selective_battery"}:
            target_structure_status = "target_selective_battery"
            target_selectivity_profile = "target_selective_tolerance"
        elif "conditional_attitude" in family_structure_type:
            target_structure_status = "conditional_attitude_battery"
        relation_conflict = "clean"
        if expected_multi_target and len(target_entity_ids) > 1:
            relation_conflict = "expected_multi_target_battery"
        elif len(driver_ids) > 1 or len(driver_facet_ids) > 1 or len(relation_axis_ids) > 1 or (len(target_entity_ids) > 1 and not expected_multi_target):
            relation_conflict = "mixed_mapping_requires_review"
        if n_questions_unmapped > 0 and relation_conflict == "clean":
            relation_conflict = "partial_mapping"
        target_resolution = _summarize_target_resolution(pattern.item_rows)
        rows.append(
            {
                "pattern_id": pattern.pattern_id,
                "family_id": pattern.family_id,
                "family_label": pattern.family_label,
                "family_type": pattern.family_type,
                "family_structure_type": family_structure_type,
                "expected_multi_target": expected_multi_target,
                "driver_id_set": driver_ids,
                "driver_facet_id_set": driver_facet_ids,
                "relation_axis_id_set": relation_axis_ids,
                "target_entity_id_set": target_entity_ids,
                "target_domain_set": target_resolution["target_domain_set"],
                "target_condition_label_set": target_resolution["target_condition_label_set"],
                "target_group_label_set": target_resolution["target_group_label_set"],
                "permission_domain_set": target_resolution["permission_domain_set"],
                "mapping_status_summary": dict(mapping_statuses),
                "semantic_role_summary": dict(semantic_roles),
                "v551_evidence_role_summary": dict(support_roles),
                "n_questions_mapped": n_questions_mapped,
                "n_questions_unmapped": n_questions_unmapped,
                "semantic_conflict_status": relation_conflict,
                "relation_signature_status": "aggregated_pattern_relation_signature",
                "target_structure_status": target_structure_status,
                "target_count": len(target_entity_ids),
                "target_group_count": len(target_resolution["target_group_label_set"]),
                "target_selectivity_profile": target_selectivity_profile,
                "target_resolution_status": target_resolution["target_resolution_status"],
                "target_resolution_status_summary": target_resolution["target_resolution_status_summary"],
                "target_resolution_grain_summary": target_resolution["target_resolution_grain_summary"],
                "infer_placeholder_share": target_resolution["infer_placeholder_share"],
                "registry_resolved_share": target_resolution["registry_resolved_share"],
                "unresolved_target_share": target_resolution["unresolved_target_share"],
                "condition_label_share": target_resolution["condition_label_share"],
                "target_group_share": target_resolution["target_group_share"],
                "permission_domain_share": target_resolution["permission_domain_share"],
                "mapping_coverage_score": (
                    100.0
                    * (
                        sum(1 for item in pattern.item_rows if _clean(item.get("mapping_status", "")).lower() not in {"", "unknown", "missing"})
                        / max(1, len(pattern.item_rows))
                    )
                ),
                "support_status": pattern.support_status,
                "confidence_tier": _confidence_tier_from_score(getattr(pattern, "confidence_score", 0.0)),
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _boundary_pattern_rows(pattern_df: pd.DataFrame) -> pd.DataFrame:
    if pattern_df.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for pattern in pattern_df.itertuples(index=False):
        boundary_pattern_id = _stable_hash({"pattern_id": pattern.pattern_id, "boundary_pattern_type": pattern.boundary_pattern_type})
        target_resolution = _summarize_target_resolution(pattern.item_rows if isinstance(pattern.item_rows, list) else [])
        rows.append(
            {
                "boundary_pattern_id": boundary_pattern_id,
                "pattern_id": pattern.pattern_id,
                "family_id": pattern.family_id,
                "family_label": pattern.family_label,
                "family_type": pattern.family_type,
                "boundary_pattern_type": pattern.boundary_pattern_type,
                "pattern_signature_raw": pattern.pattern_signature_raw,
                "pattern_signature_semantic": pattern.pattern_signature_semantic,
                "pattern_ids_included": [pattern.pattern_id],
                "semantic_rule_id": f"{pattern.family_id}_{pattern.boundary_pattern_type}",
                "boundary_rule_evaluation_summary": getattr(pattern, "boundary_rule_evaluation_summary", {}),
                "rules_evaluated": getattr(pattern, "rules_evaluated", []),
                "rules_matched": getattr(pattern, "rules_matched", []),
                "rules_failed": getattr(pattern, "rules_failed", []),
                "boundary_rule_failure_reasons": getattr(pattern, "boundary_rule_failure_reasons", {}),
                "boundary_rule_authority_source": getattr(pattern, "boundary_rule_authority_source", "question_family_registry.boundary_rules"),
                "boundary_rule_status": getattr(pattern, "boundary_rule_status", "mixed_unclassified"),
                "n_unweighted": pattern.pattern_count_unweighted,
                "n_weighted": pattern.pattern_count_weighted,
                "pct_unweighted": pattern.pattern_probability_unweighted,
                "pct_weighted": pattern.pattern_probability_weighted,
                "pct_basis": pattern.pattern_probability_basis,
                "target_resolution_status": target_resolution["target_resolution_status"],
                "target_resolution_status_summary": target_resolution["target_resolution_status_summary"],
                "target_resolution_grain_summary": target_resolution["target_resolution_grain_summary"],
                "target_entity_id_set": target_resolution["target_entity_id_set"],
                "target_domain_set": target_resolution["target_domain_set"],
                "target_condition_label_set": target_resolution["target_condition_label_set"],
                "target_group_label_set": target_resolution["target_group_label_set"],
                "permission_domain_set": target_resolution["permission_domain_set"],
                "infer_placeholder_share": target_resolution["infer_placeholder_share"],
                "registry_resolved_share": target_resolution["registry_resolved_share"],
                "unresolved_target_share": target_resolution["unresolved_target_share"],
                "condition_label_share": target_resolution["condition_label_share"],
                "target_group_share": target_resolution["target_group_share"],
                "permission_domain_share": target_resolution["permission_domain_share"],
                "support_status": pattern.support_status,
                "confidence_tier": _confidence_tier_from_score(getattr(pattern, "confidence_score", 0.0)),
                "label_source": "registry_rule",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _audit_rows(family_cfg: dict[str, Any], family_questions: pd.DataFrame, respondent_df: pd.DataFrame, pattern_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    minimum_items_answered = int(_safe_float(family_cfg.get("minimum_items_answered", 1)) or 1)
    expected_vars = {str(item["var_code"]).upper() for item in _family_item_map(family_cfg)}
    present_vars = set()
    if not family_questions.empty and "var_code" in family_questions.columns:
        present_vars = {str(v).upper() for v in family_questions["var_code"].fillna("").astype(str).tolist() if str(v).strip()}
    missing_vars = sorted(expected_vars - present_vars)
    if missing_vars:
        rows.append(
            {
                "family_id": family_cfg["family_id"],
                "issue_type": "family_vars_missing_in_wave",
                "severity": "medium",
                "item_count": len(missing_vars),
                "respondent_count": 0,
                "detail": f"Missing approved vars: {', '.join(missing_vars)}",
                "action": "pattern family was compiled from the vars available in this wave",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    if not family_questions.empty and len(family_questions) < minimum_items_answered:
        rows.append(
            {
                "family_id": family_cfg["family_id"],
                "issue_type": "family_available_items_below_minimum",
                "severity": "high",
                "item_count": int(len(family_questions)),
                "respondent_count": 0,
                "detail": f"Only {len(family_questions)} approved vars were available; minimum_items_answered is {minimum_items_answered}.",
                "action": "family skipped",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    skipped_rows = int(respondent_df.attrs.get("respondents_below_minimum_items_answered", 0) or 0)
    if skipped_rows > 0:
        rows.append(
            {
                "family_id": family_cfg["family_id"],
                "issue_type": "respondents_below_minimum_items_answered",
                "severity": "medium",
                "item_count": int(len(pattern_df)),
                "respondent_count": skipped_rows,
                "detail": f"{skipped_rows} respondents fell below minimum_items_answered={minimum_items_answered} and were excluded.",
                "action": "retain the compiled patterns, but note the respondent gate",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    if respondent_df.empty:
        rows.append(
            {
                "family_id": family_cfg["family_id"],
                "issue_type": "family_no_respondents",
                "severity": "high",
                "item_count": 0,
                "respondent_count": 0,
                "detail": "No respondent rows were available for this family.",
                "action": "family skipped",
                "created_at": utc_now(),
                "schema_version": V550J_SCHEMA_VERSION,
            }
        )
    if not pattern_df.empty:
        low_support = pattern_df[pattern_df["support_status"].astype(str).isin(["underpowered", "missing_support", "not_applicable"])]
        if not low_support.empty:
            rows.append(
                {
                    "family_id": family_cfg["family_id"],
                    "issue_type": "low_support_pattern",
                    "severity": "low",
                    "item_count": int(len(low_support)),
                    "respondent_count": int(low_support["pattern_count_unweighted"].sum()),
                    "detail": "One or more patterns did not clear the support gate.",
                    "action": "retain as diagnostic only",
                    "created_at": utc_now(),
                    "schema_version": V550J_SCHEMA_VERSION,
                }
            )
    return pd.DataFrame(rows)


def compile_v550j_family_tables(
    family_cfg: dict[str, Any],
    family_questions: pd.DataFrame,
    family_frame: pd.DataFrame,
    *,
    context_frame: pd.DataFrame | None = None,
    pattern_membership_frame: pd.DataFrame | None = None,
    association_mode: str = "publishable",
    association_support_threshold: int | None = None,
    publish_association_lanes: set[str] | None = None,
    association_lane_overrides: dict[str, Any] | None = None,
    run_id: str = "",
    source_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
    progress: Any | None = None,
    emit_diagnostics: bool = True,
    registry: Any = None,
) -> dict[str, pd.DataFrame]:
    family_id = _clean(family_cfg.get("family_id", "family"))
    effective_lane_overrides = association_lane_overrides or family_cfg.get("association_lane_overrides") or {}
    if progress is not None:
        progress.stage(1, 8, f"{family_id}: summarize respondents", "starting")
    respondent_df, pattern_df = _summarize_respondents(family_frame, family_cfg=family_cfg, family_questions=family_questions)
    if progress is not None:
        progress.stage(1, 8, f"{family_id}: summarize respondents", f"respondents={len(respondent_df)} patterns={len(pattern_df)}")
        progress.stage(2, 8, f"{family_id}: build item index", "starting")
    item_index = _item_index_rows(pattern_df, family_questions)
    if progress is not None:
        progress.stage(2, 8, f"{family_id}: build item index", f"rows={len(item_index)}")
        progress.stage(3, 8, f"{family_id}: build boundary patterns", "starting")
    boundary_index = _boundary_pattern_rows(pattern_df)
    if progress is not None:
        progress.stage(3, 8, f"{family_id}: build boundary patterns", f"rows={len(boundary_index)}")
        progress.stage(4, 8, f"{family_id}: build relation signatures", "starting")
    relation_index = _relation_signature_rows(pattern_df)
    if progress is not None:
        progress.stage(4, 8, f"{family_id}: build relation signatures", f"rows={len(relation_index)}")
        progress.stage(5, 8, f"{family_id}: build position signatures", "starting")
    membership_frame = pattern_membership_frame if pattern_membership_frame is not None else _pattern_membership_rows(
        respondent_df,
        pattern_df,
        run_id=run_id,
        source_id=source_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
    )
    membership_lookup = _pattern_membership_lookup(pattern_df, pattern_membership_frame=membership_frame)
    position_index = _position_signature_rows(pattern_df, respondent_df, pattern_membership_lookup=membership_lookup)
    if progress is not None:
        progress.stage(5, 8, f"{family_id}: build position signatures", f"rows={len(position_index)}")
    family_var_codes = {str(item["var_code"]).upper() for item in _family_item_map(family_cfg)}
    association_mode = _clean(association_mode).lower() or "publishable"
    audit_frames = [_audit_rows(family_cfg, family_questions, respondent_df, pattern_df)] if emit_diagnostics else []
    association_context_frame = context_frame
    outside_family_context = pd.DataFrame()
    candidate_trace = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
    candidate_trace.attrs["association_mode"] = association_mode
    empty_audit_frame = pd.DataFrame(columns=[
        "family_id",
        "issue_type",
        "association_context_status",
        "severity",
        "item_count",
        "respondent_count",
        "detail",
        "action",
        "created_at",
        "schema_version",
    ])
    if context_frame is None or context_frame.empty or "var_code" not in context_frame.columns:
        audit_frames.append(
            pd.DataFrame(
                [
                    {
                        "family_id": family_cfg["family_id"],
                        "issue_type": "association_context_unavailable",
                        "association_context_status": "association_context_unavailable",
                        "severity": "low",
                        "item_count": int(len(family_var_codes)),
                        "respondent_count": int(respondent_df["respondent_id"].nunique() if not respondent_df.empty and "respondent_id" in respondent_df.columns else 0),
                        "detail": "No outside-family context was available for association generation.",
                        "action": "association index suppressed for this family call",
                        "created_at": utc_now(),
                        "schema_version": V550J_SCHEMA_VERSION,
                    }
                ]
            )
        )
        association_context_frame = None
    else:
        outside_family_context = context_frame[~context_frame["var_code"].astype(str).str.upper().isin(family_var_codes)].copy()
        if outside_family_context.empty:
            audit_frames.append(
                pd.DataFrame(
                    [
                        {
                            "family_id": family_cfg["family_id"],
                            "issue_type": "association_context_unavailable",
                            "association_context_status": "association_context_unavailable",
                            "severity": "low",
                            "item_count": int(len(family_var_codes)),
                            "respondent_count": int(context_frame["respondent_id"].nunique() if "respondent_id" in context_frame.columns else 0),
                            "detail": "No outside-family context rows were available for association generation.",
                            "action": "association index suppressed for this family call",
                            "created_at": utc_now(),
                            "schema_version": V550J_SCHEMA_VERSION,
                        }
                    ]
                )
            )
            association_context_frame = None
        elif _association_authority_status(outside_family_context) != "has_association_authority":
            audit_frames.append(
                pd.DataFrame(
                    [
                        {
                            "family_id": family_cfg["family_id"],
                            "issue_type": "association_context_authority_missing",
                            "association_context_status": "association_context_authority_missing",
                            "severity": "medium",
                            "item_count": int(len(family_var_codes)),
                            "respondent_count": int(context_frame["respondent_id"].nunique() if "respondent_id" in context_frame.columns else 0),
                            "detail": "Outside-family context was present but lacked association authority columns.",
                            "action": "association index suppressed for this family call",
                            "created_at": utc_now(),
                            "schema_version": V550J_SCHEMA_VERSION,
                        }
                    ]
                )
            )
            association_context_frame = None
    if progress is not None:
        progress.stage(6, 8, f"{family_id}: association context", "starting")
    if association_mode in {"off", "funnel_only"}:
        association_index = _empty_association_index()
        if emit_diagnostics:
            audit_frames.append(
                pd.DataFrame(
                    [
                        {
                            "family_id": family_cfg["family_id"],
                            "issue_type": f"association_mode_{association_mode}",
                            "association_context_status": f"association_mode_{association_mode}",
                            "severity": "low" if association_mode == "funnel_only" else "medium",
                            "item_count": int(len(family_var_codes)),
                            "respondent_count": int(outside_family_context["respondent_id"].nunique() if "respondent_id" in outside_family_context.columns else 0),
                            "detail": "Association candidate generation was intentionally skipped for this family call.",
                            "action": "retain prepared raw components only; no association rows emitted",
                            "created_at": utc_now(),
                            "schema_version": V550J_SCHEMA_VERSION,
                        }
                    ]
                )
            )
        audit = pd.concat(audit_frames, ignore_index=True, sort=False) if emit_diagnostics else empty_audit_frame
    elif association_context_frame is None:
        association_index = _empty_association_index()
        audit = pd.concat(audit_frames, ignore_index=True, sort=False) if emit_diagnostics else empty_audit_frame
    elif emit_diagnostics:
        candidate_trace = _association_candidate_trace_rows(
            pattern_df,
            respondent_df,
            context_frame=association_context_frame,
            family_var_codes=family_var_codes,
            pattern_membership_lookup=membership_lookup,
            pattern_membership_frame=membership_frame,
            run_id=run_id,
            source_id=source_id,
            source=source,
            wave=wave,
            canonical_wave=canonical_wave,
            country_code=country_code,
                association_support_threshold=association_support_threshold,
                publish_association_lanes=publish_association_lanes,
                association_lane_overrides=effective_lane_overrides,
                progress=progress,
                emit_diagnostics=True,
                registry=registry,
            )
        publication_mask = _association_publication_mask(candidate_trace, publishable_lanes=publish_association_lanes)
        association_index = candidate_trace[publication_mask].copy()
        if not association_index.empty:
            association_index = association_index[[column for column in V550J_ASSOCIATION_INDEX_COLUMNS if column in association_index.columns]].copy()
        else:
            association_index = _empty_association_index()
        if association_index.empty and not outside_family_context.empty:
            blocked_not_direct = False
            if "not_direct_evidence" in outside_family_context.columns:
                not_direct_mask = outside_family_context["not_direct_evidence"].map(lambda value: _to_bool(value, False))
                allowed_assoc_mask = (
                    outside_family_context["allowed_as_association_feature"].map(lambda value: _to_bool(value, False))
                    if "allowed_as_association_feature" in outside_family_context.columns
                    else pd.Series(False, index=outside_family_context.index)
                )
                blocked_not_direct = bool((not_direct_mask & ~allowed_assoc_mask).any())
            blocked_semantic = False
            if "semantic_role" in outside_family_context.columns:
                blocked_semantic_roles = {
                    "metadata",
                    "position_coordinate",
                    "context",
                    "context_only",
                    "accepted_context_only",
                    "demographic",
                    "administrative",
                    "design",
                    "non_substantive",
                }
                blocked_semantic = outside_family_context["semantic_role"].astype(str).str.lower().isin(blocked_semantic_roles).any()
            blocked_classification = False
            if "source_structure_classification" in outside_family_context.columns:
                blocked_classifications = {
                    "metadata",
                    "context",
                    "context_only",
                    "position",
                    "administrative",
                    "design",
                    "forbidden",
                    "non_substantive",
                }
                blocked_classification = outside_family_context["source_structure_classification"].astype(str).str.lower().isin(blocked_classifications).any()
            if blocked_semantic or blocked_classification:
                audit_frames.append(
                    pd.DataFrame(
                        [
                            {
                                "family_id": family_cfg["family_id"],
                                "issue_type": "association_rows_suppressed_metadata_context",
                                "association_context_status": "association_rows_suppressed_metadata_context",
                                "severity": "low",
                                "item_count": int(len(family_var_codes)),
                                "respondent_count": int(outside_family_context["respondent_id"].nunique() if "respondent_id" in outside_family_context.columns else 0),
                                "detail": "Association-authorized context was filtered because rows were metadata/context/admin-only.",
                                "action": "retain raw components only; no association rows emitted",
                                "created_at": utc_now(),
                                "schema_version": V550J_SCHEMA_VERSION,
                            }
                        ]
                    )
                )
            if blocked_not_direct:
                audit_frames.append(
                    pd.DataFrame(
                        [
                            {
                                "family_id": family_cfg["family_id"],
                                "issue_type": "blocked_not_direct_evidence",
                                "association_context_status": "blocked_not_direct_evidence",
                                "severity": "medium",
                                "item_count": int(len(family_var_codes)),
                                "respondent_count": int(outside_family_context["respondent_id"].nunique() if "respondent_id" in outside_family_context.columns else 0),
                                "detail": "Outside-family context was present but not_direct_evidence rows lacked explicit association permission.",
                                "action": "retain raw components only; no association rows emitted",
                                "created_at": utc_now(),
                                "schema_version": V550J_SCHEMA_VERSION,
                            }
                        ]
                    )
                )
            audit = pd.concat(audit_frames, ignore_index=True, sort=False)
        else:
            association_index = _association_rows(
                pattern_df,
                respondent_df,
                context_frame=association_context_frame,
                family_var_codes=family_var_codes,
                pattern_membership_lookup=membership_lookup,
                pattern_membership_frame=membership_frame,
                run_id=run_id,
                source_id=source_id,
                source=source,
                wave=wave,
                canonical_wave=canonical_wave,
                country_code=country_code,
                association_support_threshold=association_support_threshold,
                publish_association_lanes=publish_association_lanes,
                association_lane_overrides=effective_lane_overrides,
                emit_diagnostics=False,
                registry=registry,
            )
            if not association_index.empty:
                association_index = association_index[[column for column in V550J_ASSOCIATION_INDEX_COLUMNS if column in association_index.columns]].copy()
            else:
                association_index = _empty_association_index()
            audit = empty_audit_frame
    else:
        association_index = _association_rows(
            pattern_df,
            respondent_df,
            context_frame=association_context_frame,
            family_var_codes=family_var_codes,
            pattern_membership_lookup=membership_lookup,
            pattern_membership_frame=membership_frame,
            run_id=run_id,
            source_id=source_id,
            source=source,
            wave=wave,
            canonical_wave=canonical_wave,
            country_code=country_code,
            registry=registry,
            association_support_threshold=association_support_threshold,
            publish_association_lanes=publish_association_lanes,
            association_lane_overrides=effective_lane_overrides,
            emit_diagnostics=False,
        )
        if not association_index.empty:
            association_index = association_index[[column for column in V550J_ASSOCIATION_INDEX_COLUMNS if column in association_index.columns]].copy()
        else:
            association_index = _empty_association_index()
        audit = empty_audit_frame
    if progress is not None:
        progress.stage(
            6,
            8,
            f"{family_id}: association context",
            f"context_rows={0 if association_context_frame is None else len(association_context_frame)} candidate_rows={len(candidate_trace)} association_rows={len(association_index)}",
        )
    if emit_diagnostics:
        audit = pd.concat(audit_frames, ignore_index=True, sort=False) if audit.empty and audit_frames else audit
    review_surface = _association_review_surface_rows(candidate_trace)
    meaning_summary = _pattern_meaning_summary_rows(pattern_df, candidate_trace, review_surface, association_index)
    if not meaning_summary.empty:
        _invalid_status = meaning_summary[
            meaning_summary["top_publishable_attitude_associations_json"].astype(str).str.strip().isin({"[]", "", "null"}) == False
        ]
        _bad_status = _invalid_status[_invalid_status["meaning_summary_status"].astype(str).isin({"insufficient_association_evidence", "summary_available_review_only"})]
        if not _bad_status.empty:
            _bad_ids = _bad_status["pattern_id"].astype(str).tolist()
            raise RuntimeError(f"meaning_summary has publishable content but status={_bad_status['meaning_summary_status'].unique()} (patterns={_bad_ids[:10]})")
        _bad_confidence = _invalid_status[_invalid_status["meaning_summary_confidence"].astype(str).eq("diagnostic_only")]
        if not _bad_confidence.empty:
            _bad_ids = _bad_confidence["pattern_id"].astype(str).tolist()
            raise RuntimeError(f"meaning_summary has publishable content but confidence=diagnostic_only (patterns={_bad_ids[:10]})")
        # Validate reviewable bucket contains no diagnostic_only rows
        _review_check = meaning_summary[
            meaning_summary["top_reviewable_attitude_signals_json"].astype(str).str.contains('"publication_status":\\s*"diagnostic_only_', na=False, regex=True)
        ]
        if not _review_check.empty:
            _bad_ids = _review_check["pattern_id"].astype(str).tolist()
            raise RuntimeError(f"meaning_summary reviewable bucket contains diagnostic_only publication_status (patterns={_bad_ids[:10]})")
    if progress is not None:
        progress.stage(7, 8, f"{family_id}: assemble outputs", f"audit_rows={len(audit)}")
        progress.stage(8, 8, f"{family_id}: complete", f"association_rows={len(association_index)} candidate_rows={len(candidate_trace)}")
    return {
        "joint_response_pattern_index": pattern_df,
        "joint_response_pattern_item_index": item_index,
        "question_family_boundary_pattern_index": boundary_index,
        "joint_pattern_position_signature": position_index,
        "joint_pattern_relation_signature": relation_index,
        "joint_pattern_respondent_membership": membership_frame if membership_frame is not None else pd.DataFrame(columns=V550J_PATTERN_MEMBERSHIP_COLUMNS),
        "joint_pattern_association_index": association_index,
        "joint_pattern_association_candidate_trace": candidate_trace,
        "joint_pattern_association_review_surface": review_surface,
        "joint_pattern_meaning_summary": meaning_summary,
        "joint_pattern_audit": audit,
    }
