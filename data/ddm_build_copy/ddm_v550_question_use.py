#!/usr/bin/env python3
"""Question-use contract helpers for V550 (universal authority repair).

This module centralizes the semantic-role classification that downstream
builders must obey. It is intentionally conservative: when a row cannot be
proven to be relation evidence, it is treated as context, position, admin, or
unknown rather than promoted.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re

import pandas as pd

from data.ddm_build_copy.ddm_v550_source_structure import _is_ses_relation_evidence
from data.ddm_build_copy.ddm_v550_family_overlay import (
    canonical_family_key,
    family_keys_equal,
    load_family_overlay,
    waves_equivalent,
)
from data.ddm_build_copy.ddm_survey_identity import (
    SurveyIdentityError,
    canonical_wave_key,
    require_survey_identity,
)
from data.ddm_build_copy.ddm_v550_authority_contract import (
    CERTIFIED,
    MISSING,
    REVIEW_REQUIRED,
    conservative_uses_for_role,
    derive_question_use_eligibility,
    normalize_authority_status,
    structural_mapping_status,
)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = ROOT / "data" / "ddm_build_copy" / "manifests"
DEFAULT_QUESTION_USE_OVERRIDES_PATH = MANIFEST_DIR / "question_use_overrides.csv"
DEFAULT_QUESTION_WAVE_ITINERARY_PATH = MANIFEST_DIR / "question_wave_itinerary.csv"
DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
DEFAULT_GSS2010_FIRST_PASS_AUTHORITY_PATH = DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR / "gss2010_first_pass_authority_table.csv"
DEFAULT_GSS2010_STRUCTURAL_OVERLAY_PATH = ROOT / "data" / "final_codebooks" / "structural_registries" / "gss2010_structural_overlay.csv"

POSITION_COORDINATE_FIELDS = {
    "sex",
    "sex_gender",
    "gender",
    "age",
    "age_group",
    "education",
    "education_level",
    "income",
    "income_level",
    "religion",
    "religion_label",
    "urban_rural",
    "region",
    "ethnicity",
    "language",
    "employment",
    "marital",
    "household_size",
}

ADMINISTRATIVE_FIELDS = {
    "weight",
    "weight_value",
    "weight_status",
    "wtss",
    "wtssall",
    "wtssnr",
    "wtssnrps",
    "wtssps",
    "wtssps_as",
    "wtssps_next",
    "sampling_weight",
    "poststrat_weight",
    "design_weight",
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
    "respondent_id",
    "case_id",
    "dataset_id",
    "source_file",
    "upload_date",
    "year",
    "survey_year",
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
}

HARD_ADMIN_DESIGN_FIELDS = {
    "respondent_id",
    "case_id",
    "source_file",
    "dataset_id",
    "upload_date",
    "year",
    "survey_year",
    "wave",
    "canonical_wave",
    "country_code",
    "weight",
    "weight_value",
    "weight_status",
    "wtss",
    "wtssall",
    "wtssnr",
    "wtssps",
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
    "sampling_weight",
    "poststrat_weight",
    "design_weight",
}

MISSINGNESS_FIELDS = {
    "missing",
    "dk",
    "dont_know",
    "don't_know",
    "refused",
    "no_answer",
    "not_asked",
    "inapplicable",
    "iap",
}

ALLOWED_ROLES = [
    "RELATION_EVIDENCE",
    "POSITION_COORDINATE",
    "STRUCTURAL_CONTEXT",
    "ADMINISTRATIVE_METADATA",
    "MISSINGNESS_SIGNAL",
    "GENERATION_FORBIDDEN",
    "UNKNOWN",
]

CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES = {
    "scalar",
    "binary_contrast",
}

FUTURE_TOPOLOGY_EVIDENCE_TOPOLOGIES = {
    "scalar",
    "binary_contrast",
    "ranked_choice",
    "multiselect",
    "nominal_choice",
    "routed_followup",
    "factual_context",
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
    "negative",
    "oppose",
    "positive",
    "support",
}


def _has_any_directionality_value(row: dict[str, Any] | pd.Series) -> bool:
    return any(
        _normalized_key(row.get(field))
        for field in ("response_direction", "directionality", "orientation", "polarity")
    )

NON_FUTURE_TOPOLOGIES = {
    "administrative_context",
    "missingness_control",
    "unresolved",
}

SIGNED_DIRECTIONAL_POLICIES = {
    "signed_attitude",
    "signed_evaluation",
    "signed_policy",
    "signed_frequency",
    "signed_scale",
    "signed_direction",
    "signed_position",
}

SEMANTIC_DETAIL_COLUMNS = [
    "semantic_subrole",
    "semantic_tags",
    "directionality_policy",
    "semantic_confidence",
    "semantic_note",
]

POSITION_CONDITIONING_COLUMNS = [
    "position_conditioning",
    "position_modifiers",
    "conditional_strata_weights",
    "horizon_affordance",
    "position_conditioning_note",
    "position_conditioning_confidence",
]

QUESTION_USE_CONTRACT_HASH_COLUMNS = [
    "source",
    "wave",
    "canonical_wave",
    "question_id",
    "var_code",
    "response_topology",
    "future_evidence_eligible",
    "future_topology_evidence_eligible",
    "current_directional_atom_eligible",
    "directional_certification_status",
    "semantic_role_authority_status",
    "response_semantics_authority_status",
    "directionality_authority_status",
    "directional_applicability_status",
    "structural_mapping_status",
    "runtime_authority_status",
    "eligibility_gate_status",
    "eligibility_failed_gates",
    "semantic_role",
    "v551_evidence_role",
    "review_required",
    "disallowed_reason",
    "manual_override_used",
    "manual_override_basis",
    "manual_override_reason",
    "itinerary_review_priority",
    "itinerary_manual_designation_required",
    "itinerary_primary_docs",
    "itinerary_secondary_docs",
    "itinerary_review_notes",
    "authority_table_used",
    "authority_table_basis",
    "authority_semantic_lane",
    "authority_semantic_role",
    "authority_evidence_lane",
    "authority_designation_confidence",
    "authority_review_required",
    "question_directionality_authority_used",
    "question_directionality_authority_status",
    "gss2010_structural_overlay_used",
    "gss2010_structural_overlay_basis",
    "gss2010_structural_overlay_review_required",
    "source_structure_fields_joined",
    "source_structure_source",
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
    "question_type",
    "handling_rule",
    "recommended_computation",
    "mapping_status",
    "question_block_id",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
    "driver_id",
    "driver_facet_id",
    "target_entity_rule",
    "final_driver_scope",
    "source_structure_classification",
    "source_structure_basis",
    "source_structure_confidence",
    "source_structure_source",
    "source_structure_review_required",
    *SEMANTIC_DETAIL_COLUMNS,
    *POSITION_CONDITIONING_COLUMNS,
]


def _question_use_contract_hash(row: dict[str, Any]) -> str:
    payload = {column: row.get(column, "") for column in QUESTION_USE_CONTRACT_HASH_COLUMNS}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()

HOUSEHOLD_CONTEXT_VARS = {
    "adults",
    "babies",
    "babies_7222",
    "childs",
    "chldidel",
    "chldmore",
    "chldnum",
    "chldsoon",
    "earnrs",
    "earnrs_7222",
    "family16",
    "hompop",
    "preteen",
    "preteen_7222",
    "sibs",
    "sibs_7222",
    "teens",
    "teens_7222",
    "unrelat",
    "unrelat_7222",
}

LIFE_COURSE_VARS = {
    "age",
    "agewed",
    "cohort",
    "family16",
    "finalter",
    "incom16",
    "marcohrt",
    "mobile16",
    "reg16",
    "reg16_7222",
    "res16",
    "vote68",
    "if68who",
}

SOCIAL_POSITION_VARS = {
    "class",
    "degree",
    "denom",
    "denom_7222",
    "educ",
    "ethnic",
    "ethnum",
    "income72",
    "coninc",
    "realinc",
    "finrela",
    "marital",
    "race",
    "region",
    "region_7222",
    "relig",
    "reltrad",
    "sex",
    "family16",
    "attend",
}

LABOR_MARKET_VARS = {
    "indus10",
    "industry",
    "indstatus",
    "indtag",
    "occ",
    "occ10",
    "occindv",
    "occstatus",
    "occtag",
    "wrkstat",
    "wrkslf",
    "workdy",
    "workhr",
    "wksub",
    "wksubs",
    "wksup",
    "wksups",
    "spind",
    "spind10",
    "spindstatus",
    "spindtag",
    "spocc",
    "spocc10",
    "spoccindv",
    "spoccstatus",
    "spocctag",
    "spwrkslf",
    "spwrksta",
}

OCCUPATIONAL_CODING_VARS = {
    "dotdata",
    "dotged",
    "dotpeop",
    "dotpres",
    "dotsvp",
    "dotthng",
    "spdotdat",
    "spdotged",
    "spdotpeo",
    "spdotpre",
    "spdotsvp",
    "spdotthn",
    "pasei10",
    "masei10",
    "cosei10",
    "sei10",
    "sei10educ",
    "sei10inc",
    "spsei10",
    "spsei10educ",
    "spsei10inc",
    "prestige",
    "sppres",
    "sppres10",
    "sppres105plus",
    "spres",
    "spres10",
    "spres105plus",
    "isco68",
    "isco88",
    "isco08",
    "spisco68",
    "spisco88",
    "spisco08",
}

IDENTITY_VARS = {
    "race",
    "sex",
    "ethnic",
    "ethnum",
    "relig",
    "reltrad",
}

MATERIAL_SECURITY_VARS = {
    "coninc",
    "finrela",
    "incdef",
    "income",
    "income72",
    "realinc",
}

STATUS_CODING_VARS = {
    "indstatus",
    "indtag",
    "maindstatus",
    "maindtag",
    "maoccstatus",
    "maocctag",
    "occstatus",
    "occtag",
    "spindstatus",
    "spindtag",
    "spoccstatus",
    "spocctag",
    "occindv",
    "maoccindv",
    "spoccindv",
    "found",
}

ATTITUDE_POLICY_PATTERNS = (
    "attitude toward",
    "favor",
    "favour",
    "oppose",
    "support",
    "should",
    "allow",
    "permit",
    "trust",
    "helpful",
    "fair",
    "disagree",
    "agree",
    "can people be trusted",
    "satisfaction",
    "happy",
)

POLICY_PATTERNS = (
    "should",
    "allow",
    "permit",
    "ban",
    "favor",
    "favour",
    "oppose",
    "vote for",
    "government should",
)

EVALUATIVE_PATTERNS = (
    "fair",
    "helpful",
    "happy",
    "satisfaction",
    "trust",
    "better",
    "good",
    "bad",
)

STATUS_CODING_PATTERNS = (
    "status",
    "coding",
    "code",
    "tag",
    "verbatim",
    "retrieved",
    "not found",
    "found",
)

NUMERIC_COORDINATE_PATTERNS = (
    "how many",
    "number of",
    "hours",
    "days",
    "years",
    "year of",
    "age when",
    "since age",
    "constant dollars",
    "income",
)

QUESTION_USE_OVERRIDE_COLUMNS = [
    "source",
    "wave",
    "canonical_wave",
    "question_id",
    "var_code",
    "semantic_role",
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
    "override_reason",
    "reviewer",
    "date",
]

QUESTION_WAVE_ITINERARY_COLUMNS = [
    "source",
    "wave",
    "canonical_wave",
    "review_priority",
    "manual_designation_required",
    "primary_docs",
    "secondary_docs",
    "review_notes",
]

GSS2010_FIRST_PASS_AUTHORITY_COLUMNS = [
    "var_name",
    "question_text",
    "module_guess",
    "semantic_lane",
    "semantic_role",
    "evidence_lane",
    "allowed_as_branch_position_signature",
    "allowed_as_branch_relation_cosignature",
    "allowed_as_attitude_cloud_anchor",
    "allowed_as_attitude_cloud_feature",
    "manual_designation_required",
    "designation_confidence",
    "rationale",
]

GSS2010_STRUCTURAL_OVERLAY_COLUMNS = [
    "source",
    "wave",
    "var_name",
    "question_block_id",
    "structural_domain_id",
    "driver_id",
    "driver_facet_id",
    "relation_axis_id",
    "target_entity_rule",
    "mapping_status",
    "evidence_kind",
    "channel_affordances",
    "new_driver_needed",
    "notes",
]

_GSS_FIRST_PASS_AUTHORITY_RE = re.compile(r"^gss(?P<wave>[0-9]{4})_first_pass_authority_table\.csv$", re.IGNORECASE)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _normalized_key(value: Any) -> str:
    return _clean(value).lower()


def _to_bool(value: Any) -> bool:
    text = _normalized_key(value)
    return text in {"1", "true", "t", "yes", "y", "on"}


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


def _normalize_source(value: Any) -> str:
    text = _clean(value)
    return text or ""


def _normalize_wave(value: Any) -> str:
    text = _clean(value)
    return text or ""


def _overlay_candidate_frame(record: dict[str, Any], overlay: pd.DataFrame) -> pd.DataFrame:
    """Return an exact identifier match before a unique case-folded fallback.

    Family and wave aliases may be normalized, but physical variable identity
    is case-preserving. If no exact variable match exists, case-folded fallback
    is permitted only when it identifies one row; callers fail closed on an
    ambiguous fallback such as ``Duration1`` versus ``DURATION1``.
    """
    if overlay is None or overlay.empty:
        return pd.DataFrame()
    source = _clean(record.get("source") or record.get("source_family"))
    wave = _clean(record.get("canonical_wave") or record.get("wave"))
    var_exact = _clean(record.get("var_code") or record.get("var_name"))
    if not source or not wave or not var_exact or "var_name" not in overlay.columns:
        return pd.DataFrame()

    scope_mask = pd.Series(True, index=overlay.index)
    if "source" in overlay.columns:
        scope_mask &= overlay["source"].map(lambda value: family_keys_equal(value, source))
    wave_columns = [column for column in ("canonical_wave", "wave") if column in overlay.columns]
    if wave_columns:
        wave_mask = pd.Series(False, index=overlay.index)
        for column in wave_columns:
            wave_mask |= overlay[column].map(lambda value: waves_equivalent(source, value, wave))
        scope_mask &= wave_mask
    scoped = overlay.loc[scope_mask]
    if scoped.empty:
        return scoped

    exact = scoped.loc[scoped["var_name"].fillna("").astype(str).str.strip().eq(var_exact)]
    if not exact.empty:
        return exact
    var_folded = var_exact.lower()
    return scoped.loc[scoped["var_name"].fillna("").astype(str).str.strip().str.lower().eq(var_folded)]


def _overlay_candidate_names(candidate: pd.DataFrame) -> list[str]:
    if candidate is None or candidate.empty or "var_name" not in candidate.columns:
        return []
    return list(dict.fromkeys(candidate["var_name"].fillna("").astype(str).str.strip().tolist()))


def _override_match_frame(record: dict[str, Any], overrides: pd.DataFrame, *, source_field: str, wave_field: str, key_field: str) -> pd.DataFrame:
    if overrides.empty:
        return pd.DataFrame()
    source = _normalize_source(record.get("source") or record.get("source_family"))
    wave = _normalize_wave(record.get(wave_field))
    key_value = _clean(record.get(key_field))
    if not source or not wave or not key_value:
        return pd.DataFrame()
    return overrides.loc[
        overrides["source"].fillna("").astype(str).eq(source)
        & overrides[wave_field].fillna("").astype(str).eq(wave)
        & overrides[key_field].fillna("").astype(str).eq(key_value)
    ]


def _role_from_doc_fields(row: dict[str, Any]) -> str:
    for field in [
        "semantic_role",
        "structural_role",
        "question_type_structural_role",
        "classification_kind",
        "semantic_scope",
        "final_driver_scope",
        "record_kind",
        "handling_rule",
    ]:
        value = _normalized_key(row.get(field))
        if not value:
            continue
        if value in {"administrative_metadata", "metadata", "sample", "routing", "prompt_shell_cleanup"}:
            return "ADMINISTRATIVE_METADATA"
        if value in {"structural_context", "context", "context_only"}:
            return "STRUCTURAL_CONTEXT"
        if value in {"missingness_signal", "missing", "missing_value"}:
            return "MISSINGNESS_SIGNAL"
        if value in {"generation_forbidden", "forbidden", "excluded"}:
            return "GENERATION_FORBIDDEN"
        if value in {"position_coordinate", "predictor", "demographic", "demographic_predictor"}:
            return "POSITION_COORDINATE"
        if value in {"relation_evidence", "evidence", "answer", "response"}:
            return "RELATION_EVIDENCE"
    return ""


def _merge_role_hint(base_role: str, doc_role: str) -> str:
    if doc_role and doc_role != "UNKNOWN":
        if base_role in {"", "UNKNOWN"}:
            return doc_role
        if base_role == "RELATION_EVIDENCE" and doc_role != "RELATION_EVIDENCE":
            return doc_role
        if base_role == "UNKNOWN":
            return doc_role
    return base_role or "UNKNOWN"


def _load_csv_frame(path: Path | None, *, columns: list[str]) -> pd.DataFrame:
    if path is None:
        return pd.DataFrame(columns=columns)
    resolved = Path(path)
    if not resolved.exists():
        return pd.DataFrame(columns=columns)
    try:
        frame = pd.read_csv(resolved, low_memory=False)
    except Exception:
        return pd.DataFrame(columns=columns)
    if frame.empty:
        return pd.DataFrame(columns=columns)
    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    return frame


@lru_cache(maxsize=4)
def _cached_override_frame(path_text: str) -> pd.DataFrame:
    return _load_csv_frame(Path(path_text), columns=QUESTION_USE_OVERRIDE_COLUMNS)


@lru_cache(maxsize=4)
def _cached_itinerary_frame(path_text: str) -> pd.DataFrame:
    return _load_csv_frame(Path(path_text), columns=QUESTION_WAVE_ITINERARY_COLUMNS)


def _normalize_gss_first_pass_authority_frame(frame: pd.DataFrame, *, source: str, wave: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, "source", "wave", "canonical_wave"])
    out = frame.copy()
    for column in GSS2010_FIRST_PASS_AUTHORITY_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    out["source"] = source
    out["wave"] = wave
    out["canonical_wave"] = wave
    out["var_name"] = out["var_name"].fillna("").astype(str).str.strip()
    out["semantic_lane"] = out["semantic_lane"].fillna("").astype(str).str.strip()
    out["semantic_role"] = out["semantic_role"].fillna("").astype(str).str.strip()
    out["evidence_lane"] = out["evidence_lane"].fillna("").astype(str).str.strip()
    return out


def _normalize_gss2010_structural_overlay_frame(frame: pd.DataFrame, *, source: str, wave: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, "source", "wave", "canonical_wave"])
    out = frame.copy()
    for column in GSS2010_STRUCTURAL_OVERLAY_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    out["source"] = source
    out["wave"] = wave
    out["canonical_wave"] = wave
    for column in [
        "var_name",
        "question_block_id",
        "structural_domain_id",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_rule",
        "mapping_status",
        "evidence_kind",
        "channel_affordances",
        "new_driver_needed",
        "notes",
    ]:
        out[column] = out[column].fillna("").astype(str).str.strip()
    if "var_name" in out.columns:
        out["_specificity_score"] = 0
        if "question_block_id" in out.columns:
            out["_specificity_score"] += (~out["question_block_id"].eq("GSS_STRATA_CORE")).astype(int)
        if "driver_id" in out.columns:
            out["_specificity_score"] += (~out["driver_id"].eq("strataSubstrate")).astype(int)
        if "relation_axis_id" in out.columns:
            out["_specificity_score"] += (~out["relation_axis_id"].eq("respondent_position")).astype(int)
        out = out.sort_values(
            by=["var_name", "_specificity_score", "question_block_id", "driver_id", "relation_axis_id"],
            ascending=[True, False, True, True, True],
            kind="mergesort",
        ).drop_duplicates(subset=["var_name"], keep="first")
        out = out.drop(columns=["_specificity_score"], errors="ignore")
    return out


def load_question_use_overrides(path: Path | None = None) -> pd.DataFrame:
    resolved = Path(path) if path is not None else DEFAULT_QUESTION_USE_OVERRIDES_PATH
    return _cached_override_frame(str(resolved)).copy()


def load_question_wave_itinerary(path: Path | None = None) -> pd.DataFrame:
    resolved = Path(path) if path is not None else DEFAULT_QUESTION_WAVE_ITINERARY_PATH
    return _cached_itinerary_frame(str(resolved)).copy()


def load_gss2010_first_pass_authority(path: Path | None = None) -> pd.DataFrame:
    resolved = Path(path) if path is not None else DEFAULT_GSS2010_FIRST_PASS_AUTHORITY_PATH
    try:
        frame = pd.read_csv(resolved, low_memory=False)
    except Exception:
        return pd.DataFrame(columns=[*GSS2010_FIRST_PASS_AUTHORITY_COLUMNS, "source", "wave", "canonical_wave"])
    return _normalize_gss_first_pass_authority_frame(frame, source="GSS", wave="2010")


def load_gss_first_pass_authority(directory: Path | None = None) -> pd.DataFrame:
    resolved = Path(directory) if directory is not None else DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR
    if resolved.is_file():
        match = _GSS_FIRST_PASS_AUTHORITY_RE.match(resolved.name)
        wave = match.group("wave") if match else ""
        try:
            frame = pd.read_csv(resolved, low_memory=False)
        except Exception:
            return pd.DataFrame(columns=[*GSS2010_FIRST_PASS_AUTHORITY_COLUMNS, "source", "wave", "canonical_wave"])
        return _normalize_gss_first_pass_authority_frame(frame, source="GSS", wave=wave)
    if not resolved.exists():
        return pd.DataFrame(columns=[*GSS2010_FIRST_PASS_AUTHORITY_COLUMNS, "source", "wave", "canonical_wave"])
    frames: list[pd.DataFrame] = []
    for path in sorted(resolved.glob("gss*_first_pass_authority_table.csv")):
        match = _GSS_FIRST_PASS_AUTHORITY_RE.match(path.name)
        wave = match.group("wave") if match else ""
        if not wave:
            continue
        try:
            frame = pd.read_csv(path, low_memory=False)
        except Exception:
            continue
        frames.append(_normalize_gss_first_pass_authority_frame(frame, source="GSS", wave=wave))
    if not frames:
        return pd.DataFrame(columns=[*GSS2010_FIRST_PASS_AUTHORITY_COLUMNS, "source", "wave", "canonical_wave"])
    return pd.concat(frames, ignore_index=True, sort=False)


def _normalize_gss_semantic_authority_frame(frame: pd.DataFrame, *, source: str, wave: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, "source", "wave", "canonical_wave"])
    out = frame.copy()
    for column in [
        "var_name",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
    ]:
        if column not in out.columns:
            out[column] = ""
    out["source"] = source
    out["wave"] = wave
    out["canonical_wave"] = wave
    for column in [
        "var_name",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
    ]:
        out[column] = out[column].fillna("").astype(str).str.strip()
    return out


def _normalize_gss_position_conditioning_overlay_frame(frame: pd.DataFrame, *, source: str, wave: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, "source", "wave", "canonical_wave"])
    out = frame.copy()
    for column in [
        "var_name",
        "position_conditioning",
        "position_modifiers",
        "conditional_strata_weights",
        "horizon_affordance",
        "position_conditioning_note",
        "position_conditioning_confidence",
    ]:
        if column not in out.columns:
            out[column] = ""
    out["source"] = source
    out["wave"] = wave
    out["canonical_wave"] = wave
    for column in [
        "var_name",
        "position_conditioning",
        "position_modifiers",
        "conditional_strata_weights",
        "horizon_affordance",
        "position_conditioning_note",
        "position_conditioning_confidence",
    ]:
        out[column] = out[column].fillna("").astype(str).str.strip()
    return out


@lru_cache(maxsize=4)
def _cached_semantic_authority_frame(path_text: str) -> pd.DataFrame:
    resolved = Path(path_text)
    if resolved.is_file():
        try:
            frame = pd.read_csv(resolved, low_memory=False)
        except Exception:
            return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *SEMANTIC_DETAIL_COLUMNS])
        match = re.search(r"^gss(?P<wave>[0-9]{4})_semantic_authority_overlay\.csv$", resolved.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        return _normalize_gss_semantic_authority_frame(frame, source="GSS", wave=wave)
    if not resolved.exists():
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *SEMANTIC_DETAIL_COLUMNS])
    frames: list[pd.DataFrame] = []
    for path in sorted(resolved.glob("gss*_semantic_authority_overlay.csv")):
        match = re.match(r"^gss(?P<wave>[0-9]{4})_semantic_authority_overlay\.csv$", path.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        if not wave:
            continue
        try:
            frame = pd.read_csv(path, low_memory=False)
        except Exception:
            continue
        frames.append(_normalize_gss_semantic_authority_frame(frame, source="GSS", wave=wave))
    if not frames:
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *SEMANTIC_DETAIL_COLUMNS])
    return pd.concat(frames, ignore_index=True, sort=False)


@lru_cache(maxsize=4)
def _cached_position_conditioning_overlay_frame(path_text: str) -> pd.DataFrame:
    resolved = Path(path_text)
    if resolved.is_file():
        try:
            frame = pd.read_csv(resolved, low_memory=False)
        except Exception:
            return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *POSITION_CONDITIONING_COLUMNS])
        match = re.search(r"^gss(?P<wave>[0-9]{4})_position_conditioning_overlay\.csv$", resolved.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        return _normalize_gss_position_conditioning_overlay_frame(frame, source="GSS", wave=wave)
    if not resolved.exists():
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *POSITION_CONDITIONING_COLUMNS])
    frames: list[pd.DataFrame] = []
    for path in sorted(resolved.glob("gss*_position_conditioning_overlay.csv")):
        match = re.match(r"^gss(?P<wave>[0-9]{4})_position_conditioning_overlay\.csv$", path.name, re.IGNORECASE)
        wave = match.group("wave") if match else ""
        if not wave:
            continue
        try:
            frame = pd.read_csv(path, low_memory=False)
        except Exception:
            continue
        frames.append(_normalize_gss_position_conditioning_overlay_frame(frame, source="GSS", wave=wave))
    if not frames:
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *POSITION_CONDITIONING_COLUMNS])
    return pd.concat(frames, ignore_index=True, sort=False)


def _combine_gss_overlay_frames(loader, directories: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    seen_files: set[tuple[str, str]] = set()
    for directory in directories:
        if directory is None:
            continue
        resolved = Path(directory)
        if not resolved.exists():
            continue
        for path in sorted(resolved.glob("gss*_*.csv")):
            key = (resolved.as_posix(), path.name)
            if key in seen_files:
                continue
            seen_files.add(key)
        frame = loader(str(resolved))
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True, sort=False)
    if "source" in combined.columns and "wave" in combined.columns and "canonical_wave" in combined.columns and "var_name" in combined.columns:
        combined = combined.drop_duplicates(subset=["source", "wave", "canonical_wave", "var_name"], keep="first").reset_index(drop=True)
    return combined


def load_gss_semantic_authority_overlay(directory: Path | None = None) -> pd.DataFrame:
    resolved = Path(directory) if directory is not None else DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR
    frames = []
    for candidate in [resolved]:
        if candidate is None:
            continue
        if candidate.exists():
            frame = _cached_semantic_authority_frame(str(candidate))
            if not frame.empty:
                frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *SEMANTIC_DETAIL_COLUMNS])
    out = pd.concat(frames, ignore_index=True, sort=False)
    out = out.drop_duplicates(subset=["source", "wave", "canonical_wave", "var_name"], keep="first").reset_index(drop=True)
    return out.copy()


def load_gss_position_conditioning_overlay(directory: Path | None = None) -> pd.DataFrame:
    resolved = Path(directory) if directory is not None else DEFAULT_GSS_FIRST_PASS_AUTHORITY_DIR
    frames = []
    for candidate in [resolved]:
        if candidate is None:
            continue
        if candidate.exists():
            frame = _cached_position_conditioning_overlay_frame(str(candidate))
            if not frame.empty:
                frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["source", "wave", "canonical_wave", "var_name", *POSITION_CONDITIONING_COLUMNS])
    out = pd.concat(frames, ignore_index=True, sort=False)
    out = out.drop_duplicates(subset=["source", "wave", "canonical_wave", "var_name"], keep="first").reset_index(drop=True)
    return out.copy()


def load_gss2010_structural_overlay(path: Path | None = None) -> pd.DataFrame:
    resolved = Path(path) if path is not None else DEFAULT_GSS2010_STRUCTURAL_OVERLAY_PATH
    try:
        frame = pd.read_csv(resolved, low_memory=False)
    except Exception:
        return pd.DataFrame(columns=[*GSS2010_STRUCTURAL_OVERLAY_COLUMNS, "source", "wave", "canonical_wave"])
    return _normalize_gss2010_structural_overlay_frame(frame, source="GSS", wave="2010")


def _select_override(record: dict[str, Any], overrides: pd.DataFrame) -> tuple[dict[str, Any] | None, str, bool]:
    if overrides.empty:
        return None, "", False
    question_id = _clean(record.get("question_id"))
    var_code = _clean(record.get("var_code") or record.get("var_name"))
    source = _normalize_source(record.get("source") or record.get("source_family"))
    wave = _normalize_wave(record.get("wave"))
    canonical_wave = _normalize_wave(record.get("canonical_wave"))

    candidate_frames: list[tuple[str, pd.DataFrame]] = []
    if source and wave and var_code:
        candidate_frames.append(
            (
                "source_wave_var_code",
                overrides.loc[
                    overrides["source"].fillna("").astype(str).eq(source)
                    & overrides["wave"].fillna("").astype(str).eq(wave)
                    & overrides["var_code"].fillna("").astype(str).eq(var_code)
                ],
            )
        )
    if source and canonical_wave and var_code:
        candidate_frames.append(
            (
                "source_canonical_wave_var_code",
                overrides.loc[
                    overrides["source"].fillna("").astype(str).eq(source)
                    & overrides["canonical_wave"].fillna("").astype(str).eq(canonical_wave)
                    & overrides["var_code"].fillna("").astype(str).eq(var_code)
                ],
            )
        )
    if source and wave and question_id:
        candidate_frames.append(
            (
                "source_wave_question_id",
                overrides.loc[
                    overrides["source"].fillna("").astype(str).eq(source)
                    & overrides["wave"].fillna("").astype(str).eq(wave)
                    & overrides["question_id"].fillna("").astype(str).eq(question_id)
                ],
            )
        )
    if source and canonical_wave and question_id:
        candidate_frames.append(
            (
                "source_canonical_wave_question_id",
                overrides.loc[
                    overrides["source"].fillna("").astype(str).eq(source)
                    & overrides["canonical_wave"].fillna("").astype(str).eq(canonical_wave)
                    & overrides["question_id"].fillna("").astype(str).eq(question_id)
                ],
            )
        )

    matched_row: dict[str, Any] | None = None
    matched_basis = ""
    matched_key: tuple[tuple[str, str], ...] | None = None
    for basis, frame in candidate_frames:
        if len(frame) > 1:
            raise RuntimeError(
                f"ambiguous manual override match for source={source} wave={wave or canonical_wave} question_id={question_id} var_code={var_code} via {basis}: {len(frame)} rows"
            )
        if len(frame) == 1:
            row = frame.iloc[0].to_dict()
            row_key = tuple(sorted((key, _clean(value)) for key, value in row.items()))
            if matched_row is None:
                matched_row = row
                matched_basis = basis
                matched_key = row_key
                continue
            if matched_key is not None and row_key != matched_key:
                raise RuntimeError(
                    f"ambiguous manual override match for source={source} wave={wave or canonical_wave} question_id={question_id} var_code={var_code}: matched multiple distinct override rows"
                )

    if matched_row is None:
        return None, "", False
    return matched_row, matched_basis, False


def _normalize_authority_role(authority_row: dict[str, Any]) -> str:
    """Resolve packet role with explicit row-level fields taking precedence.

    `semantic_lane=substantive` is not enough to make a row relation evidence:
    rankings and other preserved topologies are substantive but explicitly
    structural-context rows.  The old ordering silently promoted them.
    """
    semantic_lane = _normalized_key(authority_row.get("semantic_lane"))
    semantic_role = _normalized_key(authority_row.get("semantic_role"))
    evidence_lane = _normalized_key(authority_row.get("evidence_lane"))

    if semantic_role in {"admin", "administrative", "administrative_metadata"}:
        return "ADMINISTRATIVE_METADATA"
    if semantic_role in {"demographic", "position_context", "position_coordinate"}:
        return "POSITION_COORDINATE"
    if semantic_role in {
        "structural_context",
        "context",
        "context_only",
        "behavior_exposure_context",
        "behavioral_or_demographic_context",
        "demographic_material_or_behavioral_context",
        "preference_target_or_ranking",
        "preference_target_or_relation",
        "multi_response_preference_or_classification",
        "list_experiment_count",
        "uncertified_substantive_choice",
    }:
        return "STRUCTURAL_CONTEXT"
    if semantic_role.startswith("substantive") or semantic_role in {
        "relation_evidence",
        "attitude_perception_evaluation_or_intention",
    }:
        return "RELATION_EVIDENCE"

    if not semantic_role:
        auth_semantic_role = _normalized_key(authority_row.get("authority_semantic_role"))
        if auth_semantic_role:
            if auth_semantic_role in {"admin", "administrative", "administrative_metadata"}:
                return "ADMINISTRATIVE_METADATA"
            if auth_semantic_role in {"demographic", "position_context", "position_coordinate",
                    "demographic_material_or_behavioral_context", "demographic_material_or_identity_context"}:
                return "POSITION_COORDINATE"
            if auth_semantic_role in {"structural_context", "behavior_exposure_context",
                    "behavior_participation_exposure_context", "behavioral_or_demographic_context",
                    "interview_and_fieldwork_context", "open_or_continuous_context",
                    "reported_fact_or_status_context", "uncertified_substantive_choice",
                    "preference_target_or_ranking", "preference_target_or_relation",
                    "preference_target_tradeoff_or_ranking", "multi_response_preference_or_classification",
                    "substantive_nominal_choice", "list_experiment_count",
                    "structural_or_derived_context", "harmonized_cross_country_tradeoff",
                    "blocked_review", "blocked_unknown"}:
                return "STRUCTURAL_CONTEXT"
            if auth_semantic_role in {"relation_evidence", "attitude_perception_evaluation_or_intention",
                    "derived_forced_choice_strength_recode"}:
                return "RELATION_EVIDENCE"

    if evidence_lane == "administrative":
        return "ADMINISTRATIVE_METADATA"
    if evidence_lane == "position_context":
        return "POSITION_COORDINATE"
    if evidence_lane in {"context", "context_only", "future_topology", "preserved"}:
        return "STRUCTURAL_CONTEXT"
    if evidence_lane in {"direct_relation", "direct_subjective"}:
        return "RELATION_EVIDENCE"

    if semantic_lane == "administrative":
        return "ADMINISTRATIVE_METADATA"
    if semantic_lane == "demographic":
        return "POSITION_COORDINATE"
    if semantic_lane in {"context", "non_scalar_evidence"}:
        return "STRUCTURAL_CONTEXT"
    if semantic_lane in {"substantive", "subjective_evidence"}:
        return "RELATION_EVIDENCE"
    return "UNKNOWN"


def _apply_authority_designation(
    record: dict[str, Any],
    authority: pd.DataFrame | None,
) -> tuple[str, dict[str, bool], bool, str, str, str, str, str, bool, str]:
    """
    Apply a family-scoped first-pass authority table when it matches.

    Returns:
        role, uses, authority_used, authority_basis, authority_lane, authority_role,
        authority_evidence_lane, authority_confidence,
        authority_review_required, semantic_role_authority_status
    """
    if authority is None or authority.empty:
        return "UNKNOWN", allowed_uses_for_role("UNKNOWN"), False, "", "", "", "", "", False, MISSING
    source = _normalized_key(record.get("source") or record.get("source_family"))
    wave = _normalized_key(record.get("wave") or record.get("canonical_wave"))
    var_code = _normalized_key(record.get("var_code") or record.get("var_name"))
    if not var_code:
        return "UNKNOWN", allowed_uses_for_role("UNKNOWN"), False, "", "", "", "", "", False, MISSING
    candidate = _overlay_candidate_frame(record, authority)
    if candidate.empty:
        return "UNKNOWN", allowed_uses_for_role("UNKNOWN"), False, "", "", "", "", "", False, MISSING
    if len(candidate) > 1:
        raise RuntimeError(f"ambiguous authority overlay match for var_name={var_code}: candidates={_overlay_candidate_names(candidate)}")
    authority_row = candidate.iloc[0].to_dict()
    role = _normalize_authority_role(authority_row)
    authority_confidence = _clean(authority_row.get("designation_confidence"))
    authority_manual_required = _to_bool(authority_row.get("manual_designation_required"))
    authority_semantic_status = normalize_authority_status(
        authority_row.get("semantic_role_authority_status")
        or authority_row.get("semantic_authority_status"),
    )
    if authority_semantic_status == MISSING:
        conf = _clean(authority_row.get("designation_confidence")).lower()
        manual = _normalized_key(authority_row.get("manual_designation_required")) in {"1", "true", "yes", "y", "on"}
        if conf in {"high", "very high"} and not manual:
            authority_semantic_status = CERTIFIED
        else:
            authority_semantic_status = REVIEW_REQUIRED
    # Semantic role and structural mapping are independent authorities.
    # Missing structural coordinates may block a use, but may not relabel a
    # certified semantic role.
    if role == "UNKNOWN":
        return (
            role,
            allowed_uses_for_role(role),
            False,
            "",
            _clean(authority_row.get("semantic_lane")),
            _clean(authority_row.get("semantic_role")),
            _clean(authority_row.get("evidence_lane")),
            _clean(authority_row.get("designation_confidence")),
            _to_bool(authority_row.get("manual_designation_required")),
            authority_semantic_status,
        )
    uses = allowed_uses_for_role(role)
    for field, value in {
        "allowed_as_branch_position_signature": authority_row.get("allowed_as_branch_position_signature", ""),
        "allowed_as_branch_relation_cosignature": authority_row.get("allowed_as_branch_relation_cosignature", ""),
        "allowed_as_attitude_cloud_anchor": authority_row.get("allowed_as_attitude_cloud_anchor", ""),
        "allowed_as_attitude_cloud_feature": authority_row.get("allowed_as_attitude_cloud_feature", ""),
    }.items():
        if _clean(value) != "":
            uses[field] = _to_bool(value)
    if role == "ADMINISTRATIVE_METADATA":
        uses["allowed_as_branch_position_signature"] = False
        uses["allowed_as_branch_relation_cosignature"] = False
        uses["allowed_as_attitude_cloud_anchor"] = False
        uses["allowed_as_attitude_cloud_feature"] = False
        uses["allowed_as_v551_relation_evidence"] = False
    elif role == "POSITION_COORDINATE":
        uses["allowed_as_branch_relation_cosignature"] = False
        uses["allowed_as_attitude_cloud_anchor"] = False
        uses["allowed_as_attitude_cloud_feature"] = False
        uses["allowed_as_v551_relation_evidence"] = False
    elif role == "RELATION_EVIDENCE":
        uses["allowed_as_branch_position_signature"] = False
    return (
        role,
        uses,
        True,
        "gss2010_first_pass_authority_table" if canonical_family_key(source) == "gss" else "family_first_pass_authority_table",
        _clean(authority_row.get("semantic_lane")),
        _clean(authority_row.get("semantic_role")),
        _clean(authority_row.get("evidence_lane")),
        authority_confidence,
        _normalized_key(authority_row.get("manual_designation_required")) in {"1", "true", "yes", "y", "on"}
        or authority_confidence.lower() not in {"high", "very high"}
        or authority_semantic_status != CERTIFIED,
        authority_semantic_status,
    )


def _select_itinerary(record: dict[str, Any], itinerary: pd.DataFrame) -> dict[str, Any]:
    default = {
        "review_priority": "normal",
        "manual_designation_required": False,
        "primary_docs": "data/ddm_build_copy/reports/respondent_wave_source_registry.md|data/ddm_build_copy/reports/respondent_wave_semantics_registry.md|data/ddm_build_copy/manifests/question_structure_register.csv",
        "secondary_docs": "data/ddm_build_copy/manifests/question_use_overrides.csv",
        "review_notes": "Use the repo's existing structural and semantic registers before any manual designation.",
    }
    if itinerary.empty:
        return default
    source = _normalize_source(record.get("source") or record.get("source_family"))
    wave = _normalize_wave(record.get("wave") or record.get("canonical_wave"))
    if not source or not wave:
        return default
    candidate = itinerary.loc[
        itinerary["source"].fillna("").astype(str).eq(source)
        & itinerary["wave"].fillna("").astype(str).eq(wave)
    ]
    if candidate.empty:
        return default
    row = candidate.iloc[0].to_dict()
    out = {
        "review_priority": _clean(row.get("review_priority")) or default["review_priority"],
        "manual_designation_required": _to_bool(row.get("manual_designation_required")),
        "primary_docs": _clean(row.get("primary_docs")) or default["primary_docs"],
        "secondary_docs": _clean(row.get("secondary_docs")) or default["secondary_docs"],
        "review_notes": _clean(row.get("review_notes")) or default["review_notes"],
    }
    return out


def _apply_manual_override(
    role: str,
    uses: dict[str, bool],
    record: dict[str, Any],
    overrides: pd.DataFrame,
) -> tuple[str, dict[str, bool], bool, str, bool, str, str, dict[str, bool]]:
    override_row, override_basis, ambiguous = _select_override(record, overrides)
    if ambiguous:
        raise RuntimeError("ambiguous_manual_override_match")
    if not override_row:
        return role, uses, False, "", False, "", "", {}

    manual_override_used = True
    override_reason = _clean(override_row.get("override_reason"))
    override_role = _clean(override_row.get("semantic_role"))
    var_code = _normalized_key(record.get("var_code") or record.get("var_name"))
    hard_admin_design = var_code in HARD_ADMIN_DESIGN_FIELDS or _normalized_key(record.get("final_driver_scope")) == "metadata" or _normalized_key(record.get("handling_rule")) == "administrative_metadata"
    if override_role:
        role = _merge_role_hint(role, override_role)
    if hard_admin_design and role == "RELATION_EVIDENCE":
        role = "ADMINISTRATIVE_METADATA"

    updated = allowed_uses_for_role(role)
    high_risk_fields = {
        "allowed_as_branch_relation_cosignature",
        "allowed_as_attitude_cloud_anchor",
        "allowed_as_attitude_cloud_feature",
        "allowed_as_v551_relation_evidence",
        "allowed_as_runtime_persona_evidence",
    }
    explicit_high_risk_allow = {field: False for field in high_risk_fields}
    for field in list(updated.keys()):
        if not field.startswith("allowed_as_"):
            continue
        override_value = override_row.get(field, "")
        if _clean(override_value) == "":
            continue
        requested = _to_bool(override_value)
        if field in high_risk_fields:
            explicit_high_risk_allow[field] = requested
            if requested and (role != "RELATION_EVIDENCE" or hard_admin_design):
                updated[field] = False
                continue
        updated[field] = requested

    if role != "RELATION_EVIDENCE" or hard_admin_design:
        for field in high_risk_fields:
            updated[field] = False

    disallowed_reason = ""
    if role == "UNKNOWN":
        disallowed_reason = "semantic_role_unknown"
    elif hard_admin_design and override_role == "RELATION_EVIDENCE":
        disallowed_reason = "override_admin_design_blocked"
    elif override_reason and role != "RELATION_EVIDENCE" and any(
        updated[field] for field in [
            "allowed_as_branch_relation_cosignature",
            "allowed_as_attitude_cloud_anchor",
            "allowed_as_attitude_cloud_feature",
            "allowed_as_v551_relation_evidence",
            "allowed_as_runtime_persona_evidence",
        ]
    ):
        disallowed_reason = "override_high_risk_use_blocked"
    return role, updated, True, disallowed_reason, False, override_basis, override_reason, explicit_high_risk_allow


def _apply_manual_designation_gate(
    uses: dict[str, bool],
    *,
    manual_designation_required: bool,
    manual_override_used: bool,
    manual_override_high_risk_allow: dict[str, bool] | None = None,
) -> tuple[dict[str, bool], str]:
    if not manual_designation_required:
        return uses, ""
    gated = dict(uses)
    allow = manual_override_high_risk_allow or {}
    high_risk_fields = [
        "allowed_as_branch_relation_cosignature",
        "allowed_as_attitude_cloud_anchor",
        "allowed_as_attitude_cloud_feature",
        "allowed_as_v551_relation_evidence",
        "allowed_as_runtime_persona_evidence",
    ]
    for field in [
        *high_risk_fields,
    ]:
        gated[field] = bool(uses.get(field, False) and allow.get(field, False))
    if any(gated.get(field, False) for field in high_risk_fields):
        return gated, ""
    return gated, "wave_itinerary_manual_designation_required"


def _apply_gss2010_structural_overlay(
    record: dict[str, Any],
    overlay: pd.DataFrame | None,
) -> tuple[dict[str, str], bool, str, bool]:
    if overlay is None or overlay.empty:
        return {}, False, "", False
    source = _normalized_key(record.get("source") or record.get("source_family"))
    wave = _normalized_key(record.get("wave") or record.get("canonical_wave"))
    if source != "gss" or wave != "2010":
        return {}, False, "", False
    var_code = _normalized_key(record.get("var_code") or record.get("var_name"))
    if not var_code:
        return {}, False, "", False
    candidate = _overlay_candidate_frame(record, overlay)
    if candidate.empty:
        return {}, False, "", False
    if len(candidate) > 1:
        raise RuntimeError(f"ambiguous structural overlay match for var_name={var_code}: candidates={_overlay_candidate_names(candidate)}")
    row = candidate.iloc[0].to_dict()
    fields = {
        "question_block_id": _clean(row.get("question_block_id")),
        "structural_domain_id": _clean(row.get("structural_domain_id")),
        "driver_id": _clean(row.get("driver_id")),
        "driver_facet_id": _clean(row.get("driver_facet_id")),
        "relation_axis_id": _clean(row.get("relation_axis_id")),
        "target_entity_rule": _clean(row.get("target_entity_rule")),
    }
    basis = _clean(row.get("mapping_status")) or "gss_v5_candidate_variable_details"
    review_required = _clean(row.get("new_driver_needed")).strip().lower() not in {"", "no", "false", "none", "no; strata substrate."}
    return fields, True, basis, review_required


def _apply_semantic_detail_overlay(record: dict[str, Any], overlay: pd.DataFrame | None) -> tuple[dict[str, str], bool]:
    if overlay is None or overlay.empty:
        return {}, False
    source = _normalized_key(record.get("source") or record.get("source_family"))
    wave = _normalized_key(record.get("wave") or record.get("canonical_wave"))
    var_code = _normalized_key(record.get("var_code") or record.get("var_name"))
    if not source or not wave or not var_code:
        return {}, False
    candidate = _overlay_candidate_frame(record, overlay)
    if candidate.empty:
        return {}, False
    if len(candidate) > 1:
        raise RuntimeError(f"ambiguous semantic authority overlay match for var_name={var_code}: candidates={_overlay_candidate_names(candidate)}")
    row = candidate.iloc[0].to_dict()
    return {
        "semantic_subrole": _clean(row.get("semantic_subrole")),
        "semantic_tags": _clean(row.get("semantic_tags")),
        "directionality_policy": _clean(row.get("directionality_policy")),
        "semantic_confidence": _clean(row.get("semantic_confidence")),
        "semantic_note": _clean(row.get("semantic_note")),
        "semantic_detail_authority_status": _clean(
            row.get("semantic_detail_authority_status")
            or row.get("semantic_authority_status")
        ).upper(),
    }, True


def _apply_position_conditioning_overlay(record: dict[str, Any], overlay: pd.DataFrame | None) -> tuple[dict[str, str], bool]:
    default = {
        "position_conditioning": "no",
        "position_modifiers": "",
        "conditional_strata_weights": "",
        "horizon_affordance": "none",
        "position_conditioning_note": "",
        "position_conditioning_confidence": "low",
    }
    if overlay is None or overlay.empty:
        return default, False
    source = _normalized_key(record.get("source") or record.get("source_family"))
    wave = _normalized_key(record.get("wave") or record.get("canonical_wave"))
    var_code = _normalized_key(record.get("var_code") or record.get("var_name"))
    if not source or not wave or not var_code:
        return default, False
    candidate = _overlay_candidate_frame(record, overlay)
    if candidate.empty:
        return default, False
    if len(candidate) > 1:
        raise RuntimeError(f"ambiguous position conditioning overlay match for var_name={var_code}: candidates={_overlay_candidate_names(candidate)}")
    row = candidate.iloc[0].to_dict()
    return {
        "position_conditioning": _clean(row.get("position_conditioning")) or default["position_conditioning"],
        "position_modifiers": _clean(row.get("position_modifiers")) or default["position_modifiers"],
        "conditional_strata_weights": _clean(row.get("conditional_strata_weights")) or default["conditional_strata_weights"],
        "horizon_affordance": _clean(row.get("horizon_affordance")) or default["horizon_affordance"],
        "position_conditioning_note": _clean(row.get("position_conditioning_note")) or default["position_conditioning_note"],
        "position_conditioning_confidence": _clean(row.get("position_conditioning_confidence")) or default["position_conditioning_confidence"],
        "position_conditioning_authority_status": _clean(
            row.get("position_conditioning_authority_status")
            or row.get("structural_mapping_authority_status")
        ).upper(),
    }, True


def _apply_question_directionality_overlay(record: dict[str, Any], overlay: pd.DataFrame) -> tuple[dict[str, Any], bool]:
    if overlay is None or overlay.empty:
        return {}, False
    candidate = _overlay_candidate_frame(record, overlay)
    if candidate.empty:
        return {}, False
    if len(candidate) > 1:
        var_code = _clean(record.get("var_code") or record.get("var_name"))
        raise RuntimeError(f"ambiguous question directionality overlay match for var_name={var_code}: candidates={_overlay_candidate_names(candidate)}")
    row = candidate.iloc[0].to_dict()
    directional_certification_status = _clean(row.get("directional_certification_status")).upper()
    current_directional_atom_eligible = _to_bool(row.get("current_directional_atom_eligible"))
    directionality_authority_status = _clean(row.get("directionality_authority_status")).upper()
    if not directionality_authority_status and (
        directional_certification_status == "CERTIFIED" or current_directional_atom_eligible
    ):
        directionality_authority_status = CERTIFIED
    return {
        "response_topology": _clean(row.get("response_topology")),
        "future_topology_evidence_eligible": _to_bool(row.get("future_topology_evidence_eligible")),
        "current_directional_atom_eligible": current_directional_atom_eligible,
        "directional_certification_status": directional_certification_status,
        "directionality_authority_status": directionality_authority_status,
    }, True


def _attitude_cloud_semantics_blocked(record: dict[str, Any], semantic_role: str, semantic_detail: dict[str, str]) -> bool:
    source_structure_classification = _normalized_key(record.get("source_structure_classification"))
    final_driver_scope = _normalized_key(record.get("final_driver_scope"))
    mapping_status = _normalized_key(record.get("mapping_status"))
    relation_axis_id = _normalized_key(record.get("relation_axis_id"))
    target_entity_id = _normalized_key(record.get("target_entity_id"))
    semantic_subrole = _normalized_key(semantic_detail.get("semantic_subrole"))
    if source_structure_classification in {"respondent_position_coordinate", "continuous_position_coordinate", "position_coordinate", "structural_context"}:
        return True
    if final_driver_scope in {"metadata"}:
        return True
    if mapping_status in {"accepted_context_only", "context_only", "context"}:
        if semantic_role not in {"RELATION_EVIDENCE"}:
            return True
    if relation_axis_id in {"", "context"}:
        if semantic_role not in {"RELATION_EVIDENCE"}:
            return True
    if target_entity_id in {"", "context_not_applicable"}:
        if semantic_role not in {"RELATION_EVIDENCE"}:
            return True
    if semantic_role in {"POSITION_COORDINATE", "STRUCTURAL_CONTEXT", "ADMINISTRATIVE_METADATA", "MISSINGNESS_SIGNAL"}:
        return True
    if semantic_subrole in {
        "geographic_region_coordinate",
        "geographic_place_size_coordinate",
        "household_context",
        "life_course_coordinate",
        "social_position_coordinate",
        "identity_coordinate",
        "labor_market_coordinate",
        "labor_market_status",
        "status_coding",
        "occupational_coding",
        "survey_process_language",
        "survey_process_quality",
        "religious_practice_coordinate",
        "material_security_coordinate",
        "political_identity_coordinate",
    }:
        return True
    return False


def _source_structure_blank(row: dict[str, Any]) -> bool:
    fields = [
        _clean(row.get("question_type")),
        _clean(row.get("handling_rule")),
        _clean(row.get("recommended_computation")),
        _clean(row.get("source_structure_classification")),
    ]
    classification = _normalized_key(row.get("source_structure_classification"))
    return not any(fields) or classification in {"unknown", "open_text_excluded"}


def infer_semantic_role(record: dict[str, Any] | pd.Series) -> str:
    """Infer the semantic role for a row or question meta record."""
    row = record if isinstance(record, dict) else record.to_dict()
    var_code = _normalized_key(row.get("var_code") or row.get("var_name"))
    driver_id = _normalized_key(row.get("driver_id"))
    mapping_status = _normalized_key(row.get("mapping_status"))
    relation_axis_id = _normalized_key(row.get("relation_axis_id"))
    target_entity_id = _normalized_key(row.get("target_entity_id"))
    question_type = _normalized_key(row.get("question_type"))
    handling_rule = _normalized_key(row.get("handling_rule"))
    final_driver_scope = _normalized_key(row.get("final_driver_scope"))
    response_family = _normalized_key(row.get("response_family"))
    source_structure_classification = _normalized_key(row.get("source_structure_classification"))
    doc_role = _role_from_doc_fields(row)

    if source_structure_classification in {"administrative_metadata", "weight_design_variable", "survey_weight_or_design_metadata", "survey_design_metadata"}:
        return _merge_role_hint("ADMINISTRATIVE_METADATA", doc_role)
    if source_structure_classification in {"structural_context"}:
        return _merge_role_hint("STRUCTURAL_CONTEXT", doc_role)
    if source_structure_classification in {"continuous_position_coordinate", "respondent_position_field", "respondent_position_coordinate"}:
        return _merge_role_hint("POSITION_COORDINATE", doc_role)
    if source_structure_classification in {"multi_select_child", "matrix_child"}:
        return _merge_role_hint("STRUCTURAL_CONTEXT", doc_role)
    if source_structure_classification in {"substantive_single_choice", "substantive_scale"}:
        return _merge_role_hint("RELATION_EVIDENCE", doc_role)
    if source_structure_classification in {"open_text_excluded"}:
        return _merge_role_hint("GENERATION_FORBIDDEN", doc_role)
    if source_structure_classification in {"unknown"}:
        return _merge_role_hint("UNKNOWN", doc_role)
    if source_structure_classification in {"continuous_position_coordinate", "respondent_position_field"}:
        return _merge_role_hint("POSITION_COORDINATE", doc_role)

    if var_code in ADMINISTRATIVE_FIELDS:
        return _merge_role_hint("ADMINISTRATIVE_METADATA", doc_role)
    if var_code in MISSINGNESS_FIELDS or question_type in {"missing", "missingness_signal"}:
        return _merge_role_hint("MISSINGNESS_SIGNAL", doc_role)
    if var_code in POSITION_COORDINATE_FIELDS:
        return _merge_role_hint("POSITION_COORDINATE", doc_role)
    if driver_id.startswith("metadata::") and relation_axis_id in {"", "context"}:
        return _merge_role_hint("STRUCTURAL_CONTEXT", doc_role)
    if mapping_status == "accepted_context_only" or relation_axis_id == "context" or target_entity_id == "context_not_applicable":
        return _merge_role_hint("STRUCTURAL_CONTEXT", doc_role)
    if any(token in question_type for token in ["open_text", "open text", "free_text"]):
        return _merge_role_hint("GENERATION_FORBIDDEN", doc_role)
    if final_driver_scope == "metadata":
        return _merge_role_hint("ADMINISTRATIVE_METADATA", doc_role)
    if handling_rule in {"administrative_metadata", "structural_context"}:
        return _merge_role_hint("STRUCTURAL_CONTEXT", doc_role)
    if response_family or question_type in {"single_choice", "multi_select", "matrix", "scale"}:
        relation_bound = (
            mapping_status not in {"", "accepted_context_only", "context_only", "context"}
            and relation_axis_id not in {"", "context"}
            and target_entity_id not in {"", "context_not_applicable"}
            and final_driver_scope not in {"metadata"}
        )
        if relation_bound:
            return _merge_role_hint("RELATION_EVIDENCE", doc_role)
        return _merge_role_hint("UNKNOWN", doc_role)
    return _merge_role_hint("UNKNOWN", doc_role)


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def infer_semantic_detail(record: dict[str, Any] | pd.Series) -> dict[str, str]:
    row = record if isinstance(record, dict) else record.to_dict()
    var_code = _normalized_key(row.get("var_code") or row.get("var_name"))
    question_text = _normalized_key(row.get("question_text"))
    semantic_role_value = _normalized_key(row.get("semantic_role"))
    role_lookup = {
        "relation_evidence": "RELATION_EVIDENCE",
        "position_context": "POSITION_COORDINATE",
        "position_coordinate": "POSITION_COORDINATE",
        "demographic": "POSITION_COORDINATE",
        "admin": "ADMINISTRATIVE_METADATA",
        "administrative": "ADMINISTRATIVE_METADATA",
        "administrative_metadata": "ADMINISTRATIVE_METADATA",
        "missingness_signal": "MISSINGNESS_SIGNAL",
        "generation_forbidden": "GENERATION_FORBIDDEN",
        "unknown": "UNKNOWN",
    }
    role = role_lookup.get(semantic_role_value, infer_semantic_role(row))
    subrole = "other_substantive"
    directionality_policy = "unsigned_context"
    confidence = "medium"
    tags: list[str] = []
    note = ""

    def set_detail(new_subrole: str, new_policy: str, new_confidence: str = "medium", *new_tags: str, new_note: str = "") -> None:
        nonlocal subrole, directionality_policy, confidence, note, tags
        subrole = new_subrole
        directionality_policy = new_policy
        confidence = new_confidence
        note = new_note
        tags = list(dict.fromkeys([*tags, *new_tags]))

    explicit_detail_overrides: dict[str, tuple[str, str, str, tuple[str, ...], str]] = {
        "comprend": (
            "survey_process_quality",
            "unsigned_context",
            "high",
            ("survey_process", "quality", "context"),
            "respondent comprehension / interview-process quality coordinate",
        ),
        "courts": (
            "justice_policy_orientation",
            "signed_policy",
            "high",
            ("justice", "policy", "signed"),
            "criminal-justice policy orientation with explicit evaluative direction",
        ),
        "fair": (
            "subjective_evaluation",
            "signed_evaluation",
            "high",
            ("attitude", "evaluation", "signed"),
            "social fairness / trust evaluation item with explicit valence",
        ),
        "fepres": (
            "gender_equality_policy",
            "signed_policy",
            "high",
            ("gender", "policy", "signed"),
            "gender-equality policy orientation",
        ),
        "fund": (
            "religious_orientation_coordinate",
            "unsigned_identity",
            "high",
            ("religion", "identity", "coordinate"),
            "religious orientation / self-placement coordinate",
        ),
        "happy": (
            "subjective_wellbeing_coordinate",
            "signed_evaluation",
            "high",
            ("wellbeing", "evaluation", "signed"),
            "subjective well-being scale with evaluative direction",
        ),
        "health": (
            "health_state_coordinate",
            "signed_evaluation",
            "high",
            ("health", "evaluation", "signed"),
            "self-rated health state coordinate",
        ),
        "other": (
            "religious_affiliation_coordinate",
            "unsigned_identity",
            "high",
            ("religion", "affiliation", "coordinate"),
            "detailed Protestant affiliation coordinate",
        ),
        "partyid": (
            "political_identity_coordinate",
            "unsigned_identity",
            "high",
            ("politics", "identity", "coordinate"),
            "political party identity / partisan self-placement coordinate",
        ),
        "pres68": (
            "political_choice_coordinate",
            "unsigned_context",
            "high",
            ("politics", "choice", "coordinate"),
            "retrospective vote-choice coordinate",
        ),
        "racinteg": (
            "racial_projection_coordinate",
            "unsigned_context",
            "high",
            ("race", "projection", "context"),
            "racial neighborhood-projection coordinate",
        ),
        "racobjct": (
            "racial_integration_preference",
            "signed_policy",
            "high",
            ("race", "integration", "policy", "signed"),
            "racial integration preference with explicit valence",
        ),
        "racpres": (
            "racial_representational_policy",
            "signed_policy",
            "high",
            ("race", "representation", "policy", "signed"),
            "racial political representation policy item",
        ),
        "racseg": (
            "racial_segregation_policy",
            "signed_policy",
            "high",
            ("race", "segregation", "policy", "signed"),
            "racial segregation policy item with explicit valence",
        ),
        "region_7222": (
            "geographic_region_coordinate",
            "unsigned_context",
            "high",
            ("geography", "region", "coordinate"),
            "region-of-interview geographic coordinate",
        ),
        "size": (
            "geographic_place_size_coordinate",
            "unsigned_numeric",
            "high",
            ("geography", "place_size", "numeric"),
            "place-size coordinate",
        ),
        "spaneng": (
            "survey_process_language",
            "unsigned_context",
            "high",
            ("survey_process", "language", "context"),
            "interview language / survey-process coordinate",
        ),
        "spdeg": (
            "spouse_social_position_coordinate",
            "unsigned_context",
            "high",
            ("spouse", "education", "position"),
            "spouse educational-attainment coordinate",
        ),
        "speduc": (
            "spouse_social_position_coordinate",
            "unsigned_context",
            "high",
            ("spouse", "education", "position"),
            "spouse educational-attainment coordinate",
        ),
    }

    if var_code in explicit_detail_overrides:
        new_subrole, new_policy, new_confidence, new_tags, new_note = explicit_detail_overrides[var_code]
        set_detail(new_subrole, new_policy, new_confidence, *new_tags, new_note=new_note)
        semantic_tags = "|".join(sorted(dict.fromkeys(tags))) if tags else "semantic"
        return {
            "semantic_subrole": subrole,
            "semantic_tags": semantic_tags,
            "directionality_policy": directionality_policy,
            "semantic_confidence": confidence,
            "semantic_note": note,
        }

    if role == "ADMINISTRATIVE_METADATA":
        set_detail("administrative_metadata", "unsigned_metadata", "high", "administrative", "metadata", new_note="survey-control or release metadata")
    elif role == "MISSINGNESS_SIGNAL":
        set_detail("missingness_signal", "unsigned_missingness", "high", "missingness", "control", new_note="missingness / response control signal")
    elif role in {"STRUCTURAL_CONTEXT", "POSITION_COORDINATE"}:
        if var_code in MATERIAL_SECURITY_VARS or _contains_any(question_text, ("family income", "income in constant dollars", "financial situation", "poverty line", "money", "financial")):
            set_detail("material_security_coordinate", "unsigned_numeric", "high", "material_security", "numeric", new_note="material security / economic position coordinate")
        elif var_code in HOUSEHOLD_CONTEXT_VARS or _contains_any(question_text, ("household", "family", "children", "siblings", "respondent number", "number of persons", "members")):
            set_detail("household_context", "unsigned_context", "high", "household", "roster", "context", new_note="household roster / family context coordinate")
        elif var_code in LIFE_COURSE_VARS or _contains_any(question_text, ("age when", "year of birth", "when 16", "first marriage", "ever been divorced", "birth", "since age", "lived with parents when 16")):
            set_detail("life_course_coordinate", "unsigned_life_course", "high", "life_course", "coordinate", new_note="life-course coordinate rather than attitude polarity")
        elif var_code == "attend" or _contains_any(question_text, ("attends religious services", "religious services", "prayer", "church attendance")):
            set_detail("religious_practice_coordinate", "unsigned_context", "high", "religion", "practice", "context", new_note="religious-practice coordinate")
        elif var_code in IDENTITY_VARS or _contains_any(question_text, ("race", "religious preference", "religious tradition", "sex", "gender", "ethnic")):
            set_detail("identity_coordinate", "unsigned_identity", "high", "identity", "position", new_note="identity / position coordinate")
        elif var_code in SOCIAL_POSITION_VARS or _contains_any(question_text, ("class", "income", "education", "marital status", "region", "employment", "work", "attends religious services")):
            set_detail("social_position_coordinate", "unsigned_context", "high", "position", "context", new_note="social position / respondent-context coordinate")
        elif var_code in LABOR_MARKET_VARS or _contains_any(question_text, ("labor force", "occupation", "industry", "work", "supervisor", "self-emp", "hours r usually works", "days r normally works")):
            if var_code in {"wrkstat", "spwrksta"} or _contains_any(question_text, ("labor force status", "status")):
                set_detail("labor_market_status", "unsigned_status", "high", "labor_market", "status", "position", new_note="labor-market status rather than attitude polarity")
            else:
                set_detail("labor_market_coordinate", "unsigned_context", "high", "labor_market", "position", new_note="labor-market coordinate or status")
        else:
            set_detail("position_coordinate", "unsigned_context", "medium", "position", "context", new_note="generic position/context coordinate")
    elif role == "RELATION_EVIDENCE":
        if var_code in {"abdefect", "abhlth", "abnomore", "abpoor", "abrape", "absingle"}:
            set_detail("attitude_polarity", "signed_attitude", "high", "attitude", "policy", "abortion", "signed", new_note="abortion attitude item with explicit polarity")
        elif var_code in STATUS_CODING_VARS or _contains_any(question_text, STATUS_CODING_PATTERNS):
            set_detail("status_coding", "unsigned_status", "high", "coding", "status", new_note="status/coding semantics rather than attitude polarity")
        elif var_code in OCCUPATIONAL_CODING_VARS or _contains_any(question_text, ("prestige", "socioeconomic index", "occupation code", "industry code", "d.o.t.", "dot", "isco", "sei")):
            set_detail("occupational_coding", "unsigned_coding", "high", "coding", "occupation", "index", new_note="occupational or socioeconomic coding / index semantics")
        elif var_code in LABOR_MARKET_VARS or _contains_any(question_text, ("hours r usually works", "days r normally works", "labor force", "occupation", "industry", "self-emp", "supervisor", "work")):
            if var_code in {"wrkstat", "spwrksta"} or _contains_any(question_text, ("labor force status", "status")):
                set_detail("labor_market_status", "unsigned_status", "high", "labor_market", "status", "position", new_note="labor-market status rather than attitude polarity")
            else:
                set_detail("labor_market_coordinate", "unsigned_context", "high", "labor_market", "position", new_note="labor-market coordinate or status")
        elif var_code in {"trust"} or _contains_any(question_text, ATTITUDE_POLICY_PATTERNS):
            if _contains_any(question_text, POLICY_PATTERNS) or var_code in {"busing", "cappun2", "fepres", "fework", "libath", "libcom", "libsoc", "spkath", "spkcom", "spksoc", "racmar", "racjob", "racschol", "racseg", "racpres"}:
                set_detail("policy_orientation", "signed_policy", "high", "attitude", "policy", "signed", new_note="policy orientation / evaluative stance")
            elif _contains_any(question_text, EVALUATIVE_PATTERNS):
                set_detail("subjective_evaluation", "signed_evaluation", "high", "attitude", "evaluation", "signed", new_note="subjective evaluation / attitude polarity")
            else:
                set_detail("attitude_polarity", "signed_attitude", "high", "attitude", "polarity", "signed", new_note="explicitly directional attitude item")
        elif var_code in LIFE_COURSE_VARS or _contains_any(question_text, ("age when", "year of", "ever been", "since age", "number of", "hours", "days", "married", "divorced", "birth")):
            set_detail("life_course_coordinate", "unsigned_life_course", "medium", "life_course", "coordinate", new_note="life-course / event-history coordinate")
        elif var_code in HOUSEHOLD_CONTEXT_VARS or _contains_any(question_text, ("household", "family", "children", "siblings", "number of", "living with parents", "home language")):
            set_detail("household_context", "unsigned_context", "medium", "household", "context", new_note="household or family context")
        elif var_code in IDENTITY_VARS or _contains_any(question_text, ("race", "religious preference", "sex", "gender", "ethnic")):
            set_detail("identity_coordinate", "unsigned_identity", "medium", "identity", "position", new_note="identity-bearing but not necessarily polarity-bearing")
        elif _contains_any(question_text, ("how often", "frequency", "usually", "normally")):
            set_detail("behavioral_frequency", "signed_frequency", "medium", "frequency", "behavior", new_note="frequency or habitual practice item")
        elif _contains_any(question_text, ("income", "financial", "money", "poor", "poverty", "employ", "work", "job")):
            set_detail("material_security_coordinate", "unsigned_numeric", "medium", "material_security", "numeric", new_note="material-security or labor-market coordinate")
        else:
            set_detail("substantive_relation", "unsigned_context", "low", "substantive", "relation", new_note="substantive relation evidence without a clear polarity contract")
    else:
        if role == "POSITION_COORDINATE":
            set_detail("position_coordinate", "unsigned_context", "medium", "position", "context", new_note="position / context coordinate")
        elif role == "UNKNOWN":
            set_detail("unknown", "unsigned_context", "low", "unknown", new_note="semantic role unresolved")
        else:
            set_detail(role.lower() or "other", "unsigned_context", "low", "other", new_note="fallback semantic classification")

    if not tags:
        tags = ["semantic"]
    semantic_tags = "|".join(sorted(dict.fromkeys(tags)))
    return {
        "semantic_subrole": subrole,
        "semantic_tags": semantic_tags,
        "directionality_policy": directionality_policy,
        "semantic_confidence": confidence,
        "semantic_note": note,
    }


def allowed_uses_for_role(role: str) -> dict[str, bool]:
    """Return role-shape hints without manufacturing downstream authority."""
    return conservative_uses_for_role(role)


def evidence_role_for_semantic_role(role: str) -> str:
    mapping = {
        "RELATION_EVIDENCE": "relation_evidence",
        "POSITION_COORDINATE": "position_coordinate",
        "STRUCTURAL_CONTEXT": "structural_context",
        "ADMINISTRATIVE_METADATA": "administrative_metadata",
        "MISSINGNESS_SIGNAL": "missingness_signal",
        "GENERATION_FORBIDDEN": "excluded",
        "UNKNOWN": "unknown",
    }
    return mapping.get(role or "UNKNOWN", "unknown")


def _response_topology_for_row(
    record: dict[str, Any] | pd.Series,
    *,
    semantic_role: str = "",
    semantic_detail: dict[str, str] | None = None,
) -> str:
    row = record if isinstance(record, dict) else record.to_dict()
    semantic_detail = semantic_detail or {}
    question_text = _normalized_key(row.get("question_text"))
    question_type = _normalized_key(row.get("question_type"))
    handling_rule = _normalized_key(row.get("handling_rule"))
    source_structure_classification = _normalized_key(row.get("source_structure_classification"))
    semantic_role_value = _normalized_key(semantic_role or row.get("semantic_role"))
    semantic_subrole = _normalized_key(semantic_detail.get("semantic_subrole") or row.get("semantic_subrole"))
    directionality_policy = _normalized_key(semantic_detail.get("directionality_policy") or row.get("directionality_policy"))

    if source_structure_classification in {
        "administrative_metadata",
        "weight_design_variable",
        "survey_weight_or_design_metadata",
        "survey_design_metadata",
    } or semantic_role_value in {"admin", "administrative", "administrative_metadata"}:
        return "administrative_context"
    if semantic_role_value == "missingness_signal" or source_structure_classification in {"missingness_signal", "missingness_control"}:
        return "missingness_control"
    if any(token in question_type for token in {"multi_select", "multiselect", "check_all", "battery"}) or _contains_any(
        handling_rule,
        (
            "check all that apply",
            "select all",
            "multiple response",
            "check-all-that-apply",
        ),
    ) or "check all that apply" in question_text:
        return "multiselect"
    if any(token in question_type for token in {"rank", "ranking", "ordered_choice", "priority"}) or _contains_any(
        handling_rule,
        (
            "rank",
            "ranking",
            "priority order",
            "order the",
            "most important",
            "least important",
        ),
    ) or _contains_any(question_text, ("rank these", "rank the following", "most important", "least important", "priority order")):
        return "ranked_choice"
    if any(token in question_type for token in {"binary", "yes_no", "yes/no", "forced_binary", "dichotomous"}) or _contains_any(
        handling_rule,
        (
            "yes/no",
            "yes or no",
            "forced binary",
            "dichotomous",
        ),
    ) or _contains_any(question_text, ("yes or no", "either/or", "true or false")):
        return "binary_contrast"
    if any(token in question_type for token in {"open_text", "open_answer", "free_text", "write_in"}) or _contains_any(
        handling_rule,
        (
            "open answer",
            "write exactly",
            "write-in",
            "write in",
            "free text",
        ),
    ) or _contains_any(question_text, ("open answer", "write exactly", "write-in", "write in")):
        return "nominal_choice"
    if any(token in question_type for token in {"follow_up", "conditional", "routed_followup"}) or _contains_any(
        handling_rule,
        (
            "follow-up",
            "skip logic",
            "conditional",
            "if respondent",
            "if yes",
            "if no",
        ),
    ) or _contains_any(question_text, ("follow-up", "if respondent", "if yes", "if no", "when applicable")):
        return "routed_followup"
    if source_structure_classification in {"structural_context"} or semantic_role_value == "structural_context":
        return "factual_context"
    if semantic_role_value == "relation_evidence" or source_structure_classification in {
        "substantive_single_choice",
        "substantive_scale",
    }:
        if directionality_policy.startswith("signed_") or semantic_subrole in {
            "attitude_polarity",
            "policy_orientation",
            "subjective_evaluation",
            "behavioral_frequency",
            "signed_attitude",
            "signed_evaluation",
            "signed_policy",
            "signed_frequency",
        }:
            return "scalar"
        return "scalar"
    if semantic_role_value in {"position_coordinate", "structural_context", "administrative_metadata", "missingness_signal"}:
        return "factual_context"
    if source_structure_classification in {"continuous_position_coordinate", "respondent_position_coordinate", "respondent_position_field", "multi_select_child", "matrix_child"}:
        return "factual_context"
    if handling_rule in {"administrative_metadata", "structural_context"}:
        return "factual_context"
    if question_type in {"single_choice", "scale", "matrix", "ordinal"}:
        return "scalar"
    return "unresolved"


def _future_topology_evidence_eligible(response_topology: str) -> bool:
    return response_topology in FUTURE_TOPOLOGY_EVIDENCE_TOPOLOGIES


def _directional_certification_status_for_row(
    record: dict[str, Any] | pd.Series,
    *,
    semantic_role: str = "",
    semantic_detail: dict[str, str] | None = None,
    response_topology: str = "",
) -> str:
    row = record if isinstance(record, dict) else record.to_dict()
    semantic_detail = semantic_detail or {}
    semantic_role_value = _normalized_key(semantic_role or row.get("semantic_role"))
    if response_topology in NON_FUTURE_TOPOLOGIES:
        return "NOT_APPLICABLE"
    if semantic_role_value != "relation_evidence":
        return "NOT_CERTIFIED"
    if response_topology not in CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES:
        return "NOT_CERTIFIED"
    directionality_policy = _normalized_key(semantic_detail.get("directionality_policy") or row.get("directionality_policy"))
    if directionality_policy in SIGNED_DIRECTIONAL_POLICIES or directionality_policy.startswith("signed_"):
        response_direction = ""
        for field in ("response_direction", "directionality", "orientation", "polarity"):
            candidate = _normalized_key(row.get(field))
            if not candidate or candidate in DIRECTION_PLACEHOLDER_VALUES:
                continue
            response_direction = candidate
            break
        if response_direction in DIRECTION_CERTIFIED_VALUES:
            return "CERTIFIED"
        if _has_any_directionality_value(row):
            return "REVIEW_REQUIRED"
        response_family = _normalized_key(row.get("response_family"))
        if response_family in APPROVED_DIRECTIONAL_INTENSITY_RESPONSE_FAMILIES:
            if _safe_float(row.get("response_intensity")) is not None:
                return "CERTIFIED"
        return "REVIEW_REQUIRED"
    return "REVIEW_REQUIRED"


def _current_directional_atom_eligible_for_row(
    record: dict[str, Any] | pd.Series,
    *,
    semantic_role: str = "",
    semantic_detail: dict[str, str] | None = None,
    response_topology: str = "",
) -> bool:
    return _directional_certification_status_for_row(
        record,
        semantic_role=semantic_role,
        semantic_detail=semantic_detail,
        response_topology=response_topology,
    ) == "CERTIFIED"


def build_question_use_contract(
    question_frame: pd.DataFrame,
    question_use_overrides_path: Path | None = None,
    wave_itinerary_path: Path | None = None,
    gss_first_pass_authority_path: Path | None = None,
    gss2010_structural_overlay_path: Path | None = None,
    gss_semantic_authority_path: Path | None = None,
    gss_position_conditioning_path: Path | None = None,
    directionality_authority_path: Path | None = None,
    *,
    survey_family: str = "",
    canonical_wave: str = "",
) -> pd.DataFrame:
    """Return a conservative question-use contract for one explicit wave."""
    if question_frame.empty:
        columns = [
            "source",
            "wave",
            "canonical_wave",
            "question_id",
            "var_code",
            "response_topology",
            "future_evidence_eligible",
            "semantic_role",
            "v551_evidence_role",
            "review_required",
            "disallowed_reason",
            "manual_override_used",
            "manual_override_basis",
            "manual_override_reason",
            "itinerary_review_priority",
            "itinerary_manual_designation_required",
            "itinerary_primary_docs",
            "itinerary_secondary_docs",
            "itinerary_review_notes",
            "authority_table_used",
            "authority_table_basis",
            "authority_semantic_lane",
            "authority_semantic_role",
            "authority_evidence_lane",
            "authority_designation_confidence",
            "authority_review_required",
    "question_directionality_authority_used",
    "question_directionality_authority_status",
            "gss2010_structural_overlay_used",
            "gss2010_structural_overlay_basis",
            "gss2010_structural_overlay_review_required",
            "source_structure_fields_joined",
            "source_structure_source",
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
            "future_topology_evidence_eligible",
            "current_directional_atom_eligible",
            "directional_certification_status",
            "semantic_role_authority_status",
            "response_semantics_authority_status",
            "directionality_authority_status",
            "directional_applicability_status",
            "structural_mapping_status",
            "runtime_authority_status",
            "eligibility_gate_status",
            "eligibility_failed_gates",
            "question_type",
            "handling_rule",
            "recommended_computation",
            "mapping_status",
            "question_block_id",
            "structural_domain_id",
            "relation_axis_id",
            "target_entity_id",
            "driver_id",
            "driver_facet_id",
            "target_entity_rule",
            "final_driver_scope",
            "source_structure_classification",
            "source_structure_basis",
            "source_structure_confidence",
            "source_structure_source",
            "source_structure_review_required",
            *SEMANTIC_DETAIL_COLUMNS,
            *POSITION_CONDITIONING_COLUMNS,
        ]
        return pd.DataFrame(columns=columns)

    def unique_value(columns: tuple[str, ...]) -> str:
        values: list[str] = []
        for column in columns:
            if column not in question_frame.columns:
                continue
            for value in question_frame[column].dropna().astype(str):
                value = value.strip()
                if value and value.lower() not in {"nan", "none", "null"}:
                    values.append(value)
        unique = list(dict.fromkeys(values))
        if len(unique) > 1:
            raise SurveyIdentityError(
                f"question-use contract must contain one {columns[0]} scope; found {unique[:8]}"
            )
        return unique[0] if unique else ""

    frame_source = unique_value(("source", "source_family"))
    frame_wave = unique_value(("canonical_wave", "wave"))
    identity = require_survey_identity(
        survey_family or frame_source,
        canonical_wave or frame_wave,
    )
    if frame_source and canonical_family_key(frame_source) != identity.source_key:
        raise SurveyIdentityError(
            f"caller source {survey_family!r} conflicts with frame source {frame_source!r}"
        )
    if frame_wave and canonical_wave_key(identity.source_key, frame_wave) != identity.canonical_wave:
        raise SurveyIdentityError(
            f"caller wave {canonical_wave!r} conflicts with frame wave {frame_wave!r}"
        )
    survey_family = identity.source
    canonical_wave = identity.canonical_wave

    overrides = load_question_use_overrides(question_use_overrides_path)
    itinerary = load_question_wave_itinerary(wave_itinerary_path)

    def overlay_root(value: Path | None) -> list[Path] | None:
        if value is None:
            return None
        path = Path(value)
        return [path if path.is_dir() else path.parent]

    auth_r = load_family_overlay(
        survey_family,
        canonical_wave,
        "first_pass_authority",
        required=False,
        search_roots=overlay_root(gss_first_pass_authority_path),
    )
    sem_r = load_family_overlay(
        survey_family,
        canonical_wave,
        "semantic_authority",
        required=False,
        search_roots=overlay_root(gss_semantic_authority_path),
    )
    pos_r = load_family_overlay(
        survey_family,
        canonical_wave,
        "position_conditioning",
        required=False,
        search_roots=overlay_root(gss_position_conditioning_path),
    )
    dir_r = load_family_overlay(
        survey_family,
        canonical_wave,
        "directionality",
        required=False,
        search_roots=overlay_root(directionality_authority_path),
    )
    authority = auth_r.data_frame if auth_r.status == "FOUND" else None
    semantic_authority = sem_r.data_frame if sem_r.status == "FOUND" else None
    position_conditioning_overlay = pos_r.data_frame if pos_r.status == "FOUND" else None
    directionality_overlay = dir_r.data_frame if dir_r.status == "FOUND" else None
    structural_overlay = None
    if identity.source_key == "gss" and identity.canonical_wave == "2010":
        structural_overlay = load_gss2010_structural_overlay(gss2010_structural_overlay_path)
    rows: list[dict[str, Any]] = []
    for record in question_frame.to_dict(orient="records"):
        row = build_question_use_contract_row(
            record,
            overrides=overrides,
            itinerary=itinerary,
            authority=authority,
            structural_overlay=structural_overlay,
            semantic_authority=semantic_authority,
            position_conditioning_overlay=position_conditioning_overlay,
            directionality_overlay=directionality_overlay,
            survey_family=survey_family,
            canonical_wave=canonical_wave,
        )
        rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        dedupe_wave = out["canonical_wave"].fillna("").astype(str)
        dedupe_wave = dedupe_wave.where(dedupe_wave.str.strip().ne(""), out["wave"].fillna("").astype(str))
        out = out.assign(_dedupe_wave=dedupe_wave)
        out = out.drop_duplicates(subset=["source", "_dedupe_wave", "question_id", "var_code"], keep="first").reset_index(drop=True)
        out = out.drop(columns=["_dedupe_wave"], errors="ignore")
    return out


def build_question_use_contract_row(
    record: dict[str, Any] | pd.Series,
    *,
    question_use_overrides_path: Path | None = None,
    wave_itinerary_path: Path | None = None,
    gss_first_pass_authority_path: Path | None = None,
    gss2010_structural_overlay_path: Path | None = None,
    gss_semantic_authority_path: Path | None = None,
    gss_position_conditioning_path: Path | None = None,
    directionality_authority_path: Path | None = None,
    overrides: pd.DataFrame | None = None,
    itinerary: pd.DataFrame | None = None,
    authority: pd.DataFrame | None = None,
    structural_overlay: pd.DataFrame | None = None,
    semantic_authority: pd.DataFrame | None = None,
    position_conditioning_overlay: pd.DataFrame | None = None,
    directionality_overlay: pd.DataFrame | None = None,
    survey_family: str = "",
    canonical_wave: str = "",
) -> dict[str, Any]:
    row = dict(record) if isinstance(record, dict) else record.to_dict()
    record_source = _clean(row.get("source") or row.get("source_family"))
    record_wave = _clean(row.get("canonical_wave") or row.get("wave"))
    identity = require_survey_identity(
        survey_family or record_source,
        canonical_wave or record_wave,
    )
    if record_source and canonical_family_key(record_source) != identity.source_key:
        raise SurveyIdentityError(
            f"caller source {survey_family!r} conflicts with row source {record_source!r}"
        )
    if record_wave and canonical_wave_key(identity.source_key, record_wave) != identity.canonical_wave:
        raise SurveyIdentityError(
            f"caller wave {canonical_wave!r} conflicts with row wave {record_wave!r}"
        )
    survey_family = identity.source
    canonical_wave = identity.canonical_wave
    row["source"] = record_source or identity.source
    row["source_family"] = _clean(row.get("source_family")) or identity.source
    row["canonical_wave"] = identity.canonical_wave
    row["wave"] = _clean(row.get("wave")) or identity.canonical_wave

    ses_relation_evidence = _is_ses_relation_evidence(row)
    overrides = overrides if overrides is not None else load_question_use_overrides(question_use_overrides_path)
    itinerary = itinerary if itinerary is not None else load_question_wave_itinerary(wave_itinerary_path)

    def overlay_root(value: Path | None) -> list[Path] | None:
        if value is None:
            return None
        path = Path(value)
        return [path if path.is_dir() else path.parent]

    if authority is None:
        result = load_family_overlay(
            survey_family,
            canonical_wave,
            "first_pass_authority",
            required=False,
            search_roots=overlay_root(gss_first_pass_authority_path),
        )
        authority = result.data_frame if result.status == "FOUND" else None
    if structural_overlay is None and identity.source_key == "gss" and identity.canonical_wave == "2010":
        structural_overlay = load_gss2010_structural_overlay(gss2010_structural_overlay_path)
    if semantic_authority is None:
        result = load_family_overlay(
            survey_family,
            canonical_wave,
            "semantic_authority",
            required=False,
            search_roots=overlay_root(gss_semantic_authority_path),
        )
        semantic_authority = result.data_frame if result.status == "FOUND" else None
    if position_conditioning_overlay is None:
        result = load_family_overlay(
            survey_family,
            canonical_wave,
            "position_conditioning",
            required=False,
            search_roots=overlay_root(gss_position_conditioning_path),
        )
        position_conditioning_overlay = result.data_frame if result.status == "FOUND" else None
    if directionality_overlay is None and canonical_wave:
        dir_r = load_family_overlay(
            survey_family,
            canonical_wave,
            "directionality",
            required=False,
            search_roots=overlay_root(directionality_authority_path),
        )
        directionality_overlay = dir_r.data_frame if dir_r and dir_r.status == "FOUND" else None
    if ses_relation_evidence:
        # Derived SES / spouse-structure families are substantive relation evidence,
        # not open-text or blank source-structure rows.
        row["source_structure_classification"] = "substantive_scale"
    role = infer_semantic_role(row)
    (
        authority_role,
        authority_uses,
        authority_used,
        authority_basis,
        authority_lane,
        authority_semantic_role,
        authority_evidence_lane,
        authority_confidence,
        authority_review_required,
        authority_semantic_status,
    ) = _apply_authority_designation(row, authority)
    uses = allowed_uses_for_role(role)
    if authority_used:
        role = authority_role
        uses = authority_uses
    if _is_ses_relation_evidence(row):
        role = "RELATION_EVIDENCE"
        uses = allowed_uses_for_role(role)
    source_structure_fields_joined = _to_bool(row.get("source_structure_fields_joined"))
    source_structure_blank = _source_structure_blank(row)
    role, uses, manual_override_used, disallowed_reason, review_required_from_override, override_basis, override_reason, explicit_high_risk_allow = _apply_manual_override(role, uses, row, overrides)
    itinerary_row = _select_itinerary(row, itinerary)
    uses, manual_designation_reason = _apply_manual_designation_gate(
        uses,
        manual_designation_required=bool(itinerary_row["manual_designation_required"]),
        manual_override_used=manual_override_used,
        manual_override_high_risk_allow=explicit_high_risk_allow,
    )
    manual_designation_still_unresolved = bool(itinerary_row["manual_designation_required"] and not any(explicit_high_risk_allow.values()))
    source_structure_high_risk_block = bool(source_structure_fields_joined and source_structure_blank and role == "RELATION_EVIDENCE" and not manual_override_used)
    if source_structure_high_risk_block:
        uses["allowed_as_v551_relation_evidence"] = False
        uses["allowed_as_branch_relation_cosignature"] = False
        uses["allowed_as_attitude_cloud_anchor"] = False
        uses["allowed_as_attitude_cloud_feature"] = False
        uses["allowed_as_runtime_persona_evidence"] = False
    if manual_designation_still_unresolved and not disallowed_reason:
        disallowed_reason = manual_designation_reason or "wave_itinerary_manual_designation_required"
    review_required = bool(role == "UNKNOWN" or disallowed_reason or manual_designation_still_unresolved or review_required_from_override or source_structure_high_risk_block)
    if manual_designation_reason and not disallowed_reason:
        disallowed_reason = manual_designation_reason
    if source_structure_high_risk_block and not disallowed_reason:
        disallowed_reason = "blank_source_structure_high_risk_block"
    source_structure_classification = _clean(row.get("source_structure_classification"))
    structural_overlay_fields, structural_overlay_used, structural_overlay_basis, structural_overlay_review_required = _apply_gss2010_structural_overlay(row, structural_overlay)
    question_block_id = _clean(row.get("question_block_id")) or structural_overlay_fields.get("question_block_id", "")
    structural_domain_id = _clean(row.get("structural_domain_id")) or structural_overlay_fields.get("structural_domain_id", "")
    driver_id = _clean(row.get("driver_id")) or structural_overlay_fields.get("driver_id", "")
    driver_facet_id = _clean(row.get("driver_facet_id")) or structural_overlay_fields.get("driver_facet_id", "")
    target_entity_rule = _clean(row.get("target_entity_rule")) or structural_overlay_fields.get("target_entity_rule", "")
    mapping_status_value = _clean(row.get("mapping_status")) or structural_overlay_fields.get("mapping_status", "")
    relation_axis_value = _clean(row.get("relation_axis_id")) or structural_overlay_fields.get("relation_axis_id", "")
    # Structural overlays populate coordinates only.  They cannot create a
    # semantic role or downstream permission.
    semantic_detail = infer_semantic_detail({**row, "semantic_role": role})
    semantic_overlay_fields, semantic_overlay_used = _apply_semantic_detail_overlay({**row, "semantic_role": role}, semantic_authority)
    semantic_detail_authority_status = (
        normalize_authority_status(
            semantic_overlay_fields.pop(
                "semantic_detail_authority_status",
                "",
            )
        )
        if semantic_overlay_used
        else REVIEW_REQUIRED
    )
    if semantic_overlay_used:
        for key, value in semantic_overlay_fields.items():
            if _clean(value):
                semantic_detail[key] = value
    position_conditioning_detail = {
        "position_conditioning": "no",
        "position_modifiers": "",
        "conditional_strata_weights": "",
        "horizon_affordance": "none",
        "position_conditioning_note": "",
        "position_conditioning_confidence": "low",
    }
    position_conditioning_overlay_fields, position_conditioning_overlay_used = _apply_position_conditioning_overlay(
        {**row, "semantic_role": role},
        position_conditioning_overlay,
    )
    position_conditioning_authority_status = (
        normalize_authority_status(
            position_conditioning_overlay_fields.pop(
                "position_conditioning_authority_status",
                "",
            )
        )
        if position_conditioning_overlay_used
        else MISSING
    )
    if position_conditioning_overlay_used:
        for key, value in position_conditioning_overlay_fields.items():
            if _clean(value):
                position_conditioning_detail[key] = value
    final_semantic_role = "RELATION_EVIDENCE" if _is_ses_relation_evidence(row) else role
    response_topology = _response_topology_for_row({**row, "semantic_role": final_semantic_role}, semantic_role=final_semantic_role, semantic_detail=semantic_detail)
    future_topology_evidence_eligible = _future_topology_evidence_eligible(response_topology)
    directional_certification_status = _directional_certification_status_for_row(
        {**row, "semantic_role": final_semantic_role},
        semantic_role=final_semantic_role,
        semantic_detail=semantic_detail,
        response_topology=response_topology,
    )
    directionality_authority_status = normalize_authority_status(
        row.get("directionality_authority_status")
    )
    current_directional_atom_eligible = bool(
        directional_certification_status == "CERTIFIED"
        and directionality_authority_status == CERTIFIED
    )
    question_directionality_fields, question_directionality_authority_used = _apply_question_directionality_overlay(
        {**row, "semantic_role": final_semantic_role},
        directionality_overlay,
    )
    if question_directionality_authority_used:
        overlay_topology = _clean(question_directionality_fields.get("response_topology"))
        if overlay_topology:
            response_topology = overlay_topology
        future_topology_evidence_eligible = bool(question_directionality_fields.get("future_topology_evidence_eligible", False))
        overlay_status = _clean(question_directionality_fields.get("directional_certification_status")).upper()
        directional_certification_status = overlay_status or "NOT_CERTIFIED"
        directionality_authority_status = normalize_authority_status(
            question_directionality_fields.get(
                "directionality_authority_status"
            )
        )
        current_directional_atom_eligible = bool(
            question_directionality_fields.get("current_directional_atom_eligible", False)
            and directional_certification_status == "CERTIFIED"
            and directionality_authority_status == CERTIFIED
            and final_semantic_role == "RELATION_EVIDENCE"
            and response_topology in CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES
        )
    relation_axis_resolved = _normalized_key(relation_axis_value) not in {
        "",
        "context",
        "unknown",
        "unresolved",
    }
    target_entity_resolved = _normalized_key(row.get("target_entity_id")) not in {
        "",
        "context",
        "context_not_applicable",
        "unknown",
        "unresolved",
    }
    certified_relation_structure_resolved = bool(
        final_semantic_role == "RELATION_EVIDENCE"
        and authority_used
        and _clean(authority_confidence).lower() in {"high", "very high"}
        and not authority_review_required
        and directional_certification_status == "CERTIFIED"
        and directionality_authority_status == CERTIFIED
        and response_topology in CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES
        and relation_axis_resolved
        and target_entity_resolved
    )
    manual_designation_resolved_by_authority = bool(
        disallowed_reason == "wave_itinerary_manual_designation_required"
        and final_semantic_role == "RELATION_EVIDENCE"
        and authority_used
        and _clean(authority_confidence).lower() in {"high", "very high"}
        and not authority_review_required
        and directional_certification_status == "CERTIFIED"
        and directionality_authority_status == CERTIFIED
        and structural_mapping_status(
            {
                **row,
                "mapping_status": mapping_status_value,
                "question_block_id": question_block_id,
                "structural_domain_id": structural_domain_id,
                "relation_axis_id": relation_axis_value,
                "target_entity_id": _clean(row.get("target_entity_id")),
                "driver_id": driver_id,
                "driver_facet_id": driver_facet_id,
                "target_entity_rule": target_entity_rule,
            }
        )
        == "COMPLETE"
    )
    if manual_designation_resolved_by_authority:
        disallowed_reason = ""
        review_required = bool(
            role == "UNKNOWN"
            or review_required_from_override
            or source_structure_high_risk_block
        )
        uses = allowed_uses_for_role(final_semantic_role)
    if not current_directional_atom_eligible:
        uses["allowed_as_v551_relation_evidence"] = False
        uses["allowed_as_branch_relation_cosignature"] = False
        uses["allowed_as_attitude_cloud_anchor"] = False
        uses["allowed_as_attitude_cloud_feature"] = False
        uses["allowed_as_runtime_persona_evidence"] = False
        uses["allowed_as_temporal_pressure_indicator"] = False
    if _attitude_cloud_semantics_blocked(row, role, semantic_detail):
        uses["allowed_as_attitude_cloud_anchor"] = False
        uses["allowed_as_attitude_cloud_feature"] = False
        uses["allowed_as_branch_relation_cosignature"] = False
        uses["allowed_as_v551_relation_evidence"] = False
        uses["allowed_as_runtime_persona_evidence"] = False
    out = {
        "source": identity.source,
        "source_key": identity.source_key,
        "wave": _clean(row.get("wave")),
        "canonical_wave": identity.canonical_wave,
        "canonical_var_name": _clean(row.get("canonical_var_name") or row.get("var_code") or row.get("var_name")),
        "source_var_name": _clean(row.get("source_var_name") or row.get("var_code") or row.get("var_name")),
        "source_var_names": _clean(row.get("source_var_names")),
        "source_mapping_type": _clean(row.get("source_mapping_type")),
        "source_mapping_authority": _clean(row.get("source_mapping_authority")),
        "question_id": _clean(row.get("question_id")),
        "var_code": _clean(row.get("var_code") or row.get("var_name")),
        "response_topology": response_topology,
        "future_evidence_eligible": future_topology_evidence_eligible,
        "future_topology_evidence_eligible": future_topology_evidence_eligible,
        "current_directional_atom_eligible": current_directional_atom_eligible,
        "directional_certification_status": directional_certification_status,
        "semantic_role": role,
        "v551_evidence_role": evidence_role_for_semantic_role(role),
        "review_required": review_required,
        "disallowed_reason": disallowed_reason,
        "manual_override_used": manual_override_used,
        "manual_override_basis": override_basis,
        "manual_override_reason": override_reason,
        "itinerary_review_priority": itinerary_row["review_priority"],
        "itinerary_manual_designation_required": itinerary_row["manual_designation_required"],
        "itinerary_primary_docs": itinerary_row["primary_docs"],
        "itinerary_secondary_docs": itinerary_row["secondary_docs"],
        "itinerary_review_notes": itinerary_row["review_notes"],
        "authority_table_used": authority_used,
        "authority_table_basis": authority_basis,
        "authority_semantic_lane": authority_lane,
        "authority_semantic_role": authority_semantic_role,
        "authority_evidence_lane": authority_evidence_lane,
        "authority_designation_confidence": authority_confidence,
        "authority_review_required": authority_review_required,
        "question_directionality_authority_used": question_directionality_authority_used,
        "question_directionality_authority_status": "FOUND" if question_directionality_authority_used else "MISSING",
        "semantic_detail_authority_status": semantic_detail_authority_status,
        "semantic_detail_basis": (
            "explicit_family_semantic_authority_overlay"
            if semantic_detail_authority_status == CERTIFIED
            else "non_authoritative_heuristic_or_uncertified_overlay"
        ),
        "position_conditioning_authority_status": position_conditioning_authority_status,
        "response_semantics_authority_status": normalize_authority_status(
            row.get("response_semantics_authority_status")
        ),
        "response_semantics_status": _clean(row.get("response_semantics_status")),
        "response_semantics_source": _clean(row.get("response_semantics_source")),
        "response_semantics_contract_hash": _clean(row.get("response_semantics_contract_hash")),
        "runtime_authority_status": _clean(row.get("runtime_authority_status")) or MISSING,
        "temporal_authority_status": _clean(row.get("temporal_authority_status")) or MISSING,
        "gss2010_structural_overlay_used": structural_overlay_used,
        "gss2010_structural_overlay_basis": structural_overlay_basis,
        "gss2010_structural_overlay_review_required": structural_overlay_review_required,
        "structural_overlay_used": structural_overlay_used,
        "structural_overlay_basis": structural_overlay_basis,
        "structural_overlay_review_required": structural_overlay_review_required,
        "source_structure_fields_joined": source_structure_fields_joined,
        "source_structure_source": _clean(row.get("source_structure_source")),
        **uses,
        "question_type": _clean(row.get("question_type")),
        "handling_rule": _clean(row.get("handling_rule")),
        "recommended_computation": _clean(row.get("recommended_computation")),
        "mapping_status": mapping_status_value,
        "question_block_id": question_block_id,
        "structural_domain_id": structural_domain_id,
        "relation_axis_id": relation_axis_value,
        "target_entity_id": _clean(row.get("target_entity_id")),
        "driver_id": driver_id,
        "driver_facet_id": driver_facet_id,
        "target_entity_rule": target_entity_rule,
        "final_driver_scope": _clean(row.get("final_driver_scope")),
        "source_structure_classification": source_structure_classification,
        "source_structure_basis": _clean(row.get("source_structure_basis")),
        "source_structure_confidence": _clean(row.get("source_structure_confidence")),
        "source_structure_source": _clean(row.get("source_structure_source")),
        "source_structure_review_required": bool(
            not certified_relation_structure_resolved
            and (
                _to_bool(row.get("source_structure_review_required"))
                or source_structure_blank
                or source_structure_classification == "unknown"
            )
        ),
        **semantic_detail,
        **position_conditioning_detail,
    }
    explicit_semantic_status = _clean(
        row.get("semantic_role_authority_status")
        or row.get("semantic_authority_status")
    ).upper()
    if explicit_semantic_status:
        out["semantic_role_authority_status"] = normalize_authority_status(
            explicit_semantic_status
        )
    elif authority_used:
        out["semantic_role_authority_status"] = authority_semantic_status
    elif manual_override_used:
        out["semantic_role_authority_status"] = REVIEW_REQUIRED
    elif role == "UNKNOWN":
        out["semantic_role_authority_status"] = MISSING
    else:
        out["semantic_role_authority_status"] = REVIEW_REQUIRED
    out["directionality_authority_status"] = directionality_authority_status
    eligibility = derive_question_use_eligibility(out)
    out.update(eligibility)
    if out["eligibility_failed_gates"] and not out["disallowed_reason"]:
        out["disallowed_reason"] = out["eligibility_failed_gates"]
    out["review_required"] = bool(
        out["review_required"]
        or out["eligibility_gate_status"] != CERTIFIED
    )
    out["question_use_contract_hash"] = _question_use_contract_hash(out)
    return out
