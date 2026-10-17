#!/usr/bin/env python3
"""Co-signature and attitude cloud helpers for V550."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_branching import INDICATOR_FIELDS
from data.ddm_build_copy.ddm_v550_metrics import cramers_v, dominant_response, normalized_mutual_information
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, confidence_tier_from_support, support_status_from_count, support_threshold_from_total

CLOUD_ENGINE_VERSION = "v550_clouds_v1"
DEFAULT_HIGH_CARDINALITY_THRESHOLD = 12
DEFAULT_RARE_CATEGORY_SUPPORT_THRESHOLD = 5

BRANCH_POSITION_SIGNATURE_COLUMNS = [
    "run_id",
    "branch_id",
    "branch_key",
    "anchor_question_id",
    "feature_rank",
    "predictor_family",
    "feature_name",
    "feature_role",
    "feature_value",
    "association_score",
    "association_metric",
    "normalized_mutual_information",
    "cramers_v",
    "n_unweighted",
    "n_unique_feature_values",
    "n_unique_response_values",
    "target_dominant_response",
    "target_dominant_response_share",
    "support_status",
    "confidence_tier",
    "high_cardinality_flag",
    "rare_category_flag",
    "rare_category_handling",
    "cloud_lane_artifact",
    "diagnostic_artifact",
    "not_direct_evidence",
    "evidence_role",
    "artifact_status",
    "feature_kind",
    "demographic_feature_excluded_flag",
]

BRANCH_RELATION_CO_SIGNATURE_COLUMNS = [
    "run_id",
    "branch_id",
    "branch_key",
    "anchor_question_id",
    "feature_rank",
    "predictor_family",
    "feature_name",
    "feature_role",
    "feature_value",
    "association_score",
    "association_metric",
    "normalized_mutual_information",
    "cramers_v",
    "n_unweighted",
    "n_unique_feature_values",
    "n_unique_response_values",
    "target_dominant_response",
    "target_dominant_response_share",
    "support_status",
    "confidence_tier",
    "cloud_lane_artifact",
    "diagnostic_artifact",
    "not_direct_evidence",
    "evidence_role",
    "artifact_status",
    "feature_kind",
    "demographic_feature_excluded_flag",
]

QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS = [
    "run_id",
    "shard_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "anchor_question_id",
    "anchor_var_code",
    "anchor_response_value_normalized",
    "anchor_response_label",
    "anchor_response_direction",
    "anchor_response_intensity",
    "anchor_polarity",
    "anchor_relation_axis_id",
    "anchor_target_entity_id",
    "anchor_response_semantics_status",
    "anchor_response_semantics_source",
    "anchor_response_semantics_contract_hash",
    "anchor_source_structure_source",
    "anchor_source_structure_basis",
    "anchor_source_structure_confidence",
    "anchor_question_use_contract_hash",
    "cotravelling_question_id",
    "cotravelling_var_code",
    "cotravelling_response_value_normalized",
    "cotravelling_response_label",
    "cotravelling_response_direction",
    "cotravelling_response_intensity",
    "cotravelling_polarity",
    "cotravelling_relation_axis_id",
    "cotravelling_target_entity_id",
    "cotravelling_response_semantics_status",
    "cotravelling_response_semantics_source",
    "cotravelling_response_semantics_contract_hash",
    "cotravelling_source_structure_source",
    "cotravelling_source_structure_basis",
    "cotravelling_source_structure_confidence",
    "cotravelling_question_use_contract_hash",
    "n_anchor",
    "n_candidate_baseline",
    "n_overlap",
    "p_cotravelling_given_anchor",
    "p_cotravelling_baseline",
    "difference_from_baseline",
    "lift",
    "mutual_information",
    "association_strength",
    "support_status",
    "confidence_tier",
    "directional_alignment",
    "cloud_lane_artifact",
    "diagnostic_artifact",
    "not_direct_evidence",
    "same_question_flag",
    "question_use_contract_hash",
    "response_semantics_status",
    "response_semantics_source",
    "response_semantics_contract_hash",
    "source_structure_source",
    "source_structure_basis",
    "source_structure_confidence",
    "source_structure_contract_hash",
    "evidence_role",
    "artifact_status",
    "cloud_engine_version",
    "cloud_feature",
    "cloud_value",
    "n_unweighted",
    "demographic_feature_excluded_flag",
    "created_at",
]


EXCLUDED_FEATURES = {
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
    "country_code",
    "survey_year",
    "weight",
    "weight_value",
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
    "respondent_id",
    "dataset_id",
    "source_file",
}

TECHNICAL_FEATURES = {
    "response_value_normalized",
    "response_label",
    "normalized_response_label",
    "response_direction",
    "response_intensity",
    "polarity",
    "ordinal_rank",
    "scale_min",
    "scale_max",
    "scale_direction",
    "directionality_status",
    "question_id",
    "var_code",
    "var_name",
    "response_value_raw",
    "value_raw",
    "value_text",
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
    "survey_year",
    "dataset_id",
    "source_file",
    "respondent_id",
    "weight",
    "weight_value",
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
    "question_use_contract_joined",
    "question_use_contract_hash",
    "response_semantics_status",
    "response_semantics_source",
    "response_semantics_contract_hash",
    "source_structure_source",
    "source_structure_basis",
    "source_structure_confidence",
    "source_structure_fields_joined",
    "source_structure_contract_hash",
    "relation_axis_id",
    "target_entity_id",
    "driver_id",
    "driver_facet_id",
}

DEMOGRAPHIC_FEATURES = {
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

POSITION_FEATURES = set(INDICATOR_FIELDS) | DEMOGRAPHIC_FEATURES

_ATTITUDE_CLOUD_STATE: dict[tuple[str, str, str, str, str], dict[str, dict[str, Any]]] = {}


def _contract_allows(question_meta: dict[str, Any], field_name: str, default: bool = True) -> bool:
    if field_name not in question_meta:
        return default
    value = question_meta.get(field_name)
    if value is None:
        return default
    text = str(value).strip().lower()
    if text == "":
        return default
    return text in {"1", "true", "t", "yes", "y", "on"}


def _feature_role(feature_name: str) -> str:
    lowered = feature_name.lower()
    if lowered in DEMOGRAPHIC_FEATURES:
        return "POSITION_COORDINATE"
    if lowered in EXCLUDED_FEATURES or lowered in TECHNICAL_FEATURES:
        return "ADMINISTRATIVE_METADATA"
    if lowered in {"question_id", "var_code", "var_name", "response_value_normalized", "response_label"}:
        return "GENERATION_FORBIDDEN"
    if lowered in POSITION_FEATURES:
        return "POSITION_COORDINATE"
    return "UNKNOWN"


def _csv_allowlist(question_meta: dict[str, Any], *field_names: str) -> set[str]:
    for field_name in field_names:
        raw = question_meta.get(field_name, "")
        if raw is None:
            continue
        text = str(raw).strip()
        if not text:
            continue
        values = [token.strip() for token in text.replace(";", ",").replace("|", ",").split(",")]
        return {value for value in values if value}
    return set()


def valid_cloud_feature(question_meta: dict[str, Any]) -> bool:
    scope = str(question_meta.get("final_driver_scope", "")).lower()
    qtype = str(question_meta.get("question_type", "")).lower()
    if scope == "metadata":
        return False
    if qtype in {"metadata", "derived_reference"}:
        return False
    if str(question_meta.get("var_name", "")).lower() in EXCLUDED_FEATURES:
        return False
    return True


def _candidate_feature_kind(feature_name: str) -> str:
    role = _feature_role(feature_name)
    if role == "POSITION_COORDINATE":
        return "demographic"
    if role == "ADMINISTRATIVE_METADATA":
        return "admin"
    if role == "GENERATION_FORBIDDEN":
        return "excluded"
    return "relation_evidence"


def _candidate_association_stats(feature_values: pd.Series, target_values: pd.Series) -> dict[str, Any] | None:
    feature_series = feature_values.fillna("").astype(str).str.strip()
    target_series = target_values.fillna("").astype(str).str.strip()
    mask = feature_series.ne("") & feature_series.ne("nan") & target_series.ne("") & target_series.ne("nan")
    if mask.sum() < 2:
        return None
    x = feature_series[mask]
    y = target_series[mask]
    if x.nunique(dropna=False) < 2 or y.nunique(dropna=False) < 2:
        return None
    nmi = float(normalized_mutual_information(x, y))
    c_v = float(cramers_v(x, y))
    score = max(nmi, c_v)
    feature_value, _ = dominant_response(x)
    target_value, target_share = dominant_response(y)
    return {
        "feature_value": feature_value,
        "association_score": float(score),
        "association_metric": "max(normalized_mutual_information, cramers_v)",
        "normalized_mutual_information": nmi,
        "cramers_v": c_v,
        "n_unweighted": int(mask.sum()),
        "n_unique_feature_values": int(x.nunique(dropna=False)),
        "n_unique_response_values": int(y.nunique(dropna=False)),
        "target_dominant_response": target_value,
        "target_dominant_response_share": float(target_share),
    }


def _support_status_from_count(n_unweighted: Any, total_respondents: Any = None) -> str:
    parsed = pd.to_numeric(pd.Series([n_unweighted]), errors="coerce").iloc[0]
    if pd.isna(parsed):
        return "missing_support"
    support = int(parsed)
    if support <= 0:
        return "zero_support"
    threshold = support_threshold_from_total(total_respondents)
    if support < threshold:
        return "underpowered"
    return "minimum_supported" if support < DEFAULT_SUPPORT_CAP else "strong_supported"


def _confidence_tier_from_stats(stats: dict[str, Any], *, support_status: str, total_respondents: Any = None) -> str:
    support = int(stats.get("n_unweighted", 0) or 0)
    feature_cardinality = int(stats.get("n_unique_feature_values", 0) or 0)
    response_cardinality = int(stats.get("n_unique_response_values", 0) or 0)
    score = float(stats.get("association_score", 0.0) or 0.0)
    if support_status in {"missing_support", "zero_support"}:
        return "low"
    if support_status == "underpowered":
        return "low" if score < 0.2 else "medium"
    if feature_cardinality > DEFAULT_HIGH_CARDINALITY_THRESHOLD or response_cardinality > DEFAULT_HIGH_CARDINALITY_THRESHOLD:
        return "medium"
    if support >= max(DEFAULT_SUPPORT_CAP, support_threshold_from_total(total_respondents)) and score >= 0.5:
        return "high"
    return "medium"


def _high_cardinality_flag(stats: dict[str, Any]) -> bool:
    return int(stats.get("n_unique_feature_values", 0) or 0) > DEFAULT_HIGH_CARDINALITY_THRESHOLD


def _rare_category_flag(stats: dict[str, Any]) -> bool:
    support = int(stats.get("n_unweighted", 0) or 0)
    unique_values = int(stats.get("n_unique_feature_values", 0) or 0)
    return unique_values > 0 and support > 0 and (support / max(unique_values, 1)) < 3


def _rare_category_handling(stats: dict[str, Any]) -> str:
    if _high_cardinality_flag(stats):
        return "collapse_to_other"
    if _rare_category_flag(stats):
        return "retain_with_caution"
    return "retain"


def reset_attitude_cloud_state() -> None:
    _ATTITUDE_CLOUD_STATE.clear()


def _stable_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def _cloud_state_key(question_meta: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        str(question_meta.get("run_id", "") or ""),
        str(question_meta.get("source", "") or ""),
        str(question_meta.get("wave", "") or ""),
        str(question_meta.get("canonical_wave", question_meta.get("wave", "")) or ""),
        str(question_meta.get("country_code", "") or ""),
    )


def _question_use_contract_hash(question_meta: dict[str, Any]) -> str:
    payload = {
        "source": question_meta.get("source", ""),
        "wave": question_meta.get("wave", ""),
        "canonical_wave": question_meta.get("canonical_wave", question_meta.get("wave", "")),
        "country_code": question_meta.get("country_code", ""),
        "question_id": question_meta.get("question_id", ""),
        "var_code": question_meta.get("var_code", ""),
        "semantic_role": question_meta.get("semantic_role", ""),
        "relation_axis_id": question_meta.get("relation_axis_id", ""),
        "target_entity_id": question_meta.get("target_entity_id", ""),
        "driver_id": question_meta.get("driver_id", ""),
        "driver_facet_id": question_meta.get("driver_facet_id", ""),
        "allowed_as_attitude_cloud_anchor": bool(question_meta.get("allowed_as_attitude_cloud_anchor", False)),
        "allowed_as_attitude_cloud_feature": bool(question_meta.get("allowed_as_attitude_cloud_feature", False)),
        "allowed_as_v551_relation_evidence": bool(question_meta.get("allowed_as_v551_relation_evidence", False)),
        "source_structure_classification": question_meta.get("source_structure_classification", ""),
        "source_structure_basis": question_meta.get("source_structure_basis", ""),
        "source_structure_confidence": question_meta.get("source_structure_confidence", ""),
        "source_structure_source": question_meta.get("source_structure_source", ""),
        "source_structure_fields_joined": bool(question_meta.get("source_structure_fields_joined", False)),
    }
    return _stable_hash(payload)


def _cloud_row_support_status(n_overlap: int, total_respondents: Any = None) -> str:
    if n_overlap <= 0:
        return "zero_support"
    if n_overlap < support_threshold_from_total(total_respondents):
        return "underpowered"
    return "minimum_supported" if n_overlap < DEFAULT_SUPPORT_CAP else "strong_supported"


def _cloud_confidence_tier(n_overlap: int, association_strength: float, total_respondents: Any = None) -> str:
    if n_overlap <= 0:
        return "low"
    if n_overlap < support_threshold_from_total(total_respondents):
        return "low" if association_strength < 0.2 else "medium"
    if n_overlap >= max(DEFAULT_SUPPORT_CAP, support_threshold_from_total(total_respondents)) and association_strength >= 0.5:
        return "high"
    return "medium"


def _direction_alignment(anchor_dir: str, candidate_dir: str, anchor_pol: str, candidate_pol: str) -> str:
    anchor_dir = str(anchor_dir or "").strip().lower()
    candidate_dir = str(candidate_dir or "").strip().lower()
    anchor_pol = str(anchor_pol or "").strip().lower()
    candidate_pol = str(candidate_pol or "").strip().lower()
    if not anchor_dir and not candidate_dir and not anchor_pol and not candidate_pol:
        return "unknown"
    if anchor_dir and candidate_dir and anchor_dir == candidate_dir:
        return "aligned"
    if anchor_pol and candidate_pol and anchor_pol == candidate_pol:
        return "aligned"
    if anchor_dir and candidate_dir and anchor_dir != candidate_dir:
        return "opposed"
    if anchor_pol and candidate_pol and anchor_pol != candidate_pol:
        return "opposed"
    return "unknown"


def _attitude_cloud_semantics_allowed(status: str) -> bool:
    normalized = str(status or "").strip().lower()
    if not normalized:
        normalized = "observed_only"
    return normalized in {"curated", "observed_only", "matched", "observed"}


def _attitude_cloud_semantics_blocked(question_meta: dict[str, Any]) -> bool:
    source_structure_classification = str(question_meta.get("source_structure_classification", "") or "").strip().lower()
    final_driver_scope = str(question_meta.get("final_driver_scope", "") or "").strip().lower()
    mapping_status = str(question_meta.get("mapping_status", "") or "").strip().lower()
    relation_axis_id = str(question_meta.get("relation_axis_id", "") or "").strip().lower()
    target_entity_id = str(question_meta.get("target_entity_id", "") or "").strip().lower()
    semantic_subrole = str(question_meta.get("semantic_subrole", "") or "").strip().lower()
    semantic_role = str(question_meta.get("semantic_role", "") or "").strip().lower()
    if source_structure_classification in {"respondent_position_coordinate", "continuous_position_coordinate", "position_coordinate", "structural_context"}:
        return True
    if final_driver_scope in {"metadata"}:
        return True
    if mapping_status in {"accepted_context_only", "context_only", "context"}:
        return True
    if relation_axis_id in {"", "context"}:
        return True
    if target_entity_id in {"", "context_not_applicable"}:
        return True
    if semantic_role in {"position_coordinate", "structural_context", "administrative_metadata", "missingness_signal"}:
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


def _prepare_attitude_cloud_frame(question_df: pd.DataFrame, question_meta: dict[str, Any]) -> pd.DataFrame:
    if question_df.empty or "respondent_id" not in question_df.columns:
        return pd.DataFrame()
    out = question_df.copy()
    if "response_value_normalized" not in out.columns:
        if "response_label" in out.columns:
            out["response_value_normalized"] = out["response_label"]
        elif "value_text" in out.columns:
            out["response_value_normalized"] = out["value_text"]
        elif "value_raw" in out.columns:
            out["response_value_normalized"] = out["value_raw"]
        else:
            out["response_value_normalized"] = ""
    if "response_label" not in out.columns:
        out["response_label"] = out["response_value_normalized"]
    if "normalized_response_label" not in out.columns:
        out["normalized_response_label"] = out["response_label"]
    out["respondent_id"] = out["respondent_id"].fillna("").astype(str).str.strip()
    out["response_value_normalized"] = out["response_value_normalized"].fillna("").astype(str).str.strip()
    out["response_label"] = out["response_label"].fillna("").astype(str).str.strip()
    out["normalized_response_label"] = out["normalized_response_label"].fillna("").astype(str).str.strip()
    if "response_direction" not in out.columns:
        out["response_direction"] = question_meta.get("response_direction", "")
    if "response_intensity" not in out.columns:
        out["response_intensity"] = question_meta.get("response_intensity", "")
    if "polarity" not in out.columns:
        out["polarity"] = question_meta.get("polarity", "")
    if "question_id" not in out.columns:
        out["question_id"] = question_meta.get("question_id", "")
    if "var_code" not in out.columns:
        out["var_code"] = question_meta.get("var_code", "")
    for field in [
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "semantic_role",
        "question_use_contract_joined",
        "allowed_as_attitude_cloud_anchor",
        "allowed_as_attitude_cloud_feature",
        "allowed_as_v551_relation_evidence",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "source_structure_source",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_fields_joined",
        "relation_axis_id",
        "target_entity_id",
        "driver_id",
        "driver_facet_id",
    ]:
        if field not in out.columns:
            out[field] = question_meta.get(field, "")
    if "question_use_contract_hash" not in out.columns:
        out["question_use_contract_hash"] = _question_use_contract_hash(question_meta)
    if "source_structure_contract_hash" not in out.columns:
        out["source_structure_contract_hash"] = _stable_hash(
            {
                "source_structure_source": question_meta.get("source_structure_source", ""),
                "source_structure_basis": question_meta.get("source_structure_basis", ""),
                "source_structure_confidence": question_meta.get("source_structure_confidence", ""),
                "source_structure_fields_joined": bool(question_meta.get("source_structure_fields_joined", False)),
                "question_id": question_meta.get("question_id", ""),
                "var_code": question_meta.get("var_code", ""),
            }
        )
    out = out[out["respondent_id"].ne("") & out["response_value_normalized"].ne("")]
    if out.empty:
        return out
    out = out.drop_duplicates(subset=["respondent_id"], keep="first").reset_index(drop=True)
    return out


def _series_first_nonempty(frame: pd.DataFrame, column: str, default: Any = "") -> Any:
    if column not in frame.columns:
        return default
    series = frame[column].fillna("").astype(str).str.strip()
    series = series[series.ne("")]
    if series.empty:
        return default
    return series.iloc[0]


def _question_cloud_meta(question_meta: dict[str, Any], question_df: pd.DataFrame | None = None) -> dict[str, Any]:
    meta = dict(question_meta)
    meta["run_id"] = str(meta.get("run_id", "") or "")
    meta["shard_id"] = str(meta.get("shard_id", "") or "")
    meta["source"] = str(meta.get("source", "") or "")
    meta["wave"] = str(meta.get("wave", "") or "")
    meta["canonical_wave"] = str(meta.get("canonical_wave", meta.get("wave", "")) or "")
    meta["country_code"] = str(meta.get("country_code", "") or "")
    meta["question_id"] = str(meta.get("question_id", "") or "")
    meta["var_code"] = str(meta.get("var_code", "") or "")
    meta["semantic_role"] = str(meta.get("semantic_role", "") or "")
    meta["question_use_contract_joined"] = bool(meta.get("question_use_contract_joined", False))
    meta["allowed_as_attitude_cloud_anchor"] = bool(meta.get("allowed_as_attitude_cloud_anchor", False))
    meta["allowed_as_attitude_cloud_feature"] = bool(meta.get("allowed_as_attitude_cloud_feature", False))
    meta["allowed_as_v551_relation_evidence"] = bool(meta.get("allowed_as_v551_relation_evidence", False))
    meta["response_semantics_status"] = str(meta.get("response_semantics_status", "") or "")
    meta["response_semantics_source"] = str(meta.get("response_semantics_source", "") or "")
    meta["response_semantics_contract_hash"] = str(meta.get("response_semantics_contract_hash", "") or "")
    if question_df is not None and not question_df.empty:
        if not meta["response_semantics_status"]:
            meta["response_semantics_status"] = str(_series_first_nonempty(question_df, "response_semantics_status", "observed_only") or "observed_only")
        if not meta["response_semantics_source"]:
            meta["response_semantics_source"] = str(_series_first_nonempty(question_df, "response_semantics_source", "observed_response_row") or "observed_response_row")
        if not meta["response_semantics_contract_hash"]:
            meta["response_semantics_contract_hash"] = str(_series_first_nonempty(question_df, "response_semantics_contract_hash", "") or "")
    meta["source_structure_source"] = str(meta.get("source_structure_source", "") or "")
    meta["source_structure_basis"] = str(meta.get("source_structure_basis", "") or "")
    meta["source_structure_confidence"] = str(meta.get("source_structure_confidence", "") or "")
    meta["source_structure_fields_joined"] = bool(meta.get("source_structure_fields_joined", False))
    if question_df is not None and not question_df.empty:
        if not meta["source_structure_source"]:
            meta["source_structure_source"] = str(_series_first_nonempty(question_df, "source_structure_source", "") or "")
        if not meta["source_structure_basis"]:
            meta["source_structure_basis"] = str(_series_first_nonempty(question_df, "source_structure_basis", "") or "")
        if not meta["source_structure_confidence"]:
            meta["source_structure_confidence"] = str(_series_first_nonempty(question_df, "source_structure_confidence", "") or "")
        if not meta["source_structure_fields_joined"]:
            meta["source_structure_fields_joined"] = bool(_series_first_nonempty(question_df, "source_structure_fields_joined", False))
    meta["relation_axis_id"] = str(meta.get("relation_axis_id", "") or "")
    meta["target_entity_id"] = str(meta.get("target_entity_id", "") or "")
    meta["driver_id"] = str(meta.get("driver_id", "") or "")
    meta["driver_facet_id"] = str(meta.get("driver_facet_id", "") or "")
    meta["question_use_contract_hash"] = str(meta.get("question_use_contract_hash", "") or _question_use_contract_hash(meta))
    meta["source_structure_contract_hash"] = str(meta.get("source_structure_contract_hash", "") or _stable_hash(
        {
            "source_structure_source": meta["source_structure_source"],
            "source_structure_basis": meta["source_structure_basis"],
            "source_structure_confidence": meta["source_structure_confidence"],
            "source_structure_fields_joined": meta["source_structure_fields_joined"],
            "question_id": meta["question_id"],
            "var_code": meta["var_code"],
        }
    ))
    return meta


def _emit_attitude_cloud_pair(anchor_df: pd.DataFrame, anchor_meta: dict[str, Any], candidate_df: pd.DataFrame, candidate_meta: dict[str, Any]) -> list[dict[str, Any]]:
    joined = anchor_df.merge(candidate_df, on="respondent_id", how="inner", suffixes=("_anchor", "_candidate"))
    if joined.empty:
        return []
    joined = joined[
        joined["response_value_normalized_anchor"].fillna("").astype(str).str.strip().ne("")
        & joined["response_value_normalized_candidate"].fillna("").astype(str).str.strip().ne("")
    ].copy()
    if joined.empty:
        return []
    crosstab = pd.crosstab(joined["response_value_normalized_anchor"], joined["response_value_normalized_candidate"], dropna=False)
    if crosstab.empty:
        return []
    stacked = crosstab.stack().sort_values(ascending=False, kind="mergesort")
    if stacked.empty:
        return []
    anchor_value = str(stacked.index[0][0])
    candidate_value = str(stacked.index[0][1])
    n_overlap = int(stacked.iloc[0])
    anchor_mask = anchor_df["response_value_normalized"].astype(str).eq(anchor_value)
    candidate_mask = candidate_df["response_value_normalized"].astype(str).eq(candidate_value)
    n_anchor = int(anchor_mask.sum())
    n_candidate_baseline = int(candidate_mask.sum())
    if n_anchor <= 0 or n_candidate_baseline <= 0 or n_overlap <= 0:
        return []
    p_given_anchor = float(n_overlap / n_anchor)
    p_baseline = float(n_candidate_baseline / max(len(candidate_df), 1))
    nmi = 0.0
    c_v = 0.0
    try:
        if joined["response_value_normalized_anchor"].nunique(dropna=False) >= 2 and joined["response_value_normalized_candidate"].nunique(dropna=False) >= 2:
            nmi = float(normalized_mutual_information(joined["response_value_normalized_anchor"], joined["response_value_normalized_candidate"]))
            c_v = float(cramers_v(joined["response_value_normalized_anchor"], joined["response_value_normalized_candidate"]))
    except Exception:
        nmi = 0.0
        c_v = 0.0
    association_strength = max(nmi, c_v)
    anchor_total = anchor_meta.get("n_respondents")
    candidate_total = candidate_meta.get("n_respondents")
    paired_total = None
    try:
        anchor_total_value = float(anchor_total)
        candidate_total_value = float(candidate_total)
        if anchor_total_value > 0 and candidate_total_value > 0:
            paired_total = min(anchor_total_value, candidate_total_value)
    except Exception:
        paired_total = None
    support_status = _cloud_row_support_status(n_overlap, total_respondents=paired_total)
    confidence_tier = _cloud_confidence_tier(n_overlap, association_strength, total_respondents=paired_total)
    direction_alignment = _direction_alignment(
        anchor_meta.get("response_direction", ""),
        candidate_meta.get("response_direction", ""),
        anchor_meta.get("polarity", ""),
        candidate_meta.get("polarity", ""),
    )
    if not anchor_meta.get("response_semantics_contract_hash") or not candidate_meta.get("response_semantics_contract_hash"):
        return []
    if not _attitude_cloud_semantics_allowed(anchor_meta.get("response_semantics_status", "")) or not _attitude_cloud_semantics_allowed(candidate_meta.get("response_semantics_status", "")):
        return []
    if not anchor_meta.get("question_use_contract_joined") or not candidate_meta.get("question_use_contract_joined"):
        return []
    if not anchor_meta.get("source_structure_fields_joined") or not candidate_meta.get("source_structure_fields_joined"):
        return []
    if not anchor_meta.get("allowed_as_attitude_cloud_anchor") or not candidate_meta.get("allowed_as_attitude_cloud_feature"):
        return []
    if anchor_meta.get("semantic_role") != "RELATION_EVIDENCE" or candidate_meta.get("semantic_role") != "RELATION_EVIDENCE":
        return []
    return [
        {
            "run_id": anchor_meta.get("run_id", ""),
            "shard_id": anchor_meta.get("shard_id", ""),
            "source": anchor_meta.get("source", ""),
            "wave": anchor_meta.get("wave", ""),
            "canonical_wave": anchor_meta.get("canonical_wave", anchor_meta.get("wave", "")),
            "country_code": anchor_meta.get("country_code", ""),
            "anchor_question_id": anchor_meta.get("question_id", ""),
            "anchor_var_code": anchor_meta.get("var_code", ""),
            "anchor_response_value_normalized": anchor_value,
            "anchor_response_label": anchor_df.loc[anchor_mask, "response_label"].astype(str).iloc[0] if anchor_mask.any() and "response_label" in anchor_df.columns else anchor_value,
            "anchor_response_direction": str(anchor_meta.get("response_direction", "") or ""),
            "anchor_response_intensity": anchor_meta.get("response_intensity", ""),
            "anchor_polarity": str(anchor_meta.get("polarity", "") or ""),
            "anchor_relation_axis_id": anchor_meta.get("relation_axis_id", ""),
            "anchor_target_entity_id": anchor_meta.get("target_entity_id", ""),
            "anchor_response_semantics_status": anchor_meta.get("response_semantics_status", ""),
            "anchor_response_semantics_source": anchor_meta.get("response_semantics_source", ""),
            "anchor_response_semantics_contract_hash": anchor_meta.get("response_semantics_contract_hash", ""),
            "anchor_source_structure_source": anchor_meta.get("source_structure_source", ""),
            "anchor_source_structure_basis": anchor_meta.get("source_structure_basis", ""),
            "anchor_source_structure_confidence": anchor_meta.get("source_structure_confidence", ""),
            "anchor_question_use_contract_hash": anchor_meta.get("question_use_contract_hash", ""),
            "cotravelling_question_id": candidate_meta.get("question_id", ""),
            "cotravelling_var_code": candidate_meta.get("var_code", ""),
            "cotravelling_response_value_normalized": candidate_value,
            "cotravelling_response_label": candidate_df.loc[candidate_mask, "response_label"].astype(str).iloc[0] if candidate_mask.any() and "response_label" in candidate_df.columns else candidate_value,
            "cotravelling_response_direction": str(candidate_meta.get("response_direction", "") or ""),
            "cotravelling_response_intensity": candidate_meta.get("response_intensity", ""),
            "cotravelling_polarity": str(candidate_meta.get("polarity", "") or ""),
            "cotravelling_relation_axis_id": candidate_meta.get("relation_axis_id", ""),
            "cotravelling_target_entity_id": candidate_meta.get("target_entity_id", ""),
            "cotravelling_response_semantics_status": candidate_meta.get("response_semantics_status", ""),
            "cotravelling_response_semantics_source": candidate_meta.get("response_semantics_source", ""),
            "cotravelling_response_semantics_contract_hash": candidate_meta.get("response_semantics_contract_hash", ""),
            "cotravelling_source_structure_source": candidate_meta.get("source_structure_source", ""),
            "cotravelling_source_structure_basis": candidate_meta.get("source_structure_basis", ""),
            "cotravelling_source_structure_confidence": candidate_meta.get("source_structure_confidence", ""),
            "cotravelling_question_use_contract_hash": candidate_meta.get("question_use_contract_hash", ""),
            "n_anchor": n_anchor,
            "n_candidate_baseline": n_candidate_baseline,
            "n_overlap": n_overlap,
            "p_cotravelling_given_anchor": p_given_anchor,
            "p_cotravelling_baseline": p_baseline,
            "difference_from_baseline": float(p_given_anchor - p_baseline),
            "lift": float(p_given_anchor / p_baseline) if p_baseline else 0.0,
            "mutual_information": float(nmi),
            "association_strength": float(association_strength),
            "support_status": support_status,
            "confidence_tier": confidence_tier,
            "directional_alignment": direction_alignment,
            "cloud_lane_artifact": True,
            "diagnostic_artifact": True,
            "not_direct_evidence": True,
            "same_question_flag": False,
            "question_use_contract_hash": anchor_meta.get("question_use_contract_hash", ""),
            "source_structure_contract_hash": anchor_meta.get("source_structure_contract_hash", ""),
            "evidence_role": "diagnostic_attitude_cloud",
            "artifact_status": "prototype_diagnostic",
            "cloud_engine_version": CLOUD_ENGINE_VERSION,
            "cloud_feature": candidate_meta.get("question_id", ""),
            "cloud_value": candidate_value,
            "n_unweighted": n_overlap,
            "demographic_feature_excluded_flag": False,
            "created_at": pd.Timestamp.utcnow().isoformat(),
            "response_semantics_status": anchor_meta.get("response_semantics_status", ""),
            "response_semantics_source": anchor_meta.get("response_semantics_source", ""),
            "response_semantics_contract_hash": anchor_meta.get("response_semantics_contract_hash", ""),
            "source_structure_source": anchor_meta.get("source_structure_source", ""),
            "source_structure_basis": anchor_meta.get("source_structure_basis", ""),
            "source_structure_confidence": anchor_meta.get("source_structure_confidence", ""),
        }
    ]


def should_emit_cloud_tables(
    branch_rows: int,
    *,
    cloud_mode: str = "auto",
    cloud_max_branch_rows: int = 1000,
    cloud_max_branch_share: float | None = None,
    wave_respondents: int | None = None,
) -> bool:
    mode = str(cloud_mode or "auto").strip().lower()
    if mode == "full":
        return True
    if mode == "off":
        return False
    if mode not in {"auto", "share"}:
        raise ValueError(f"Unsupported cloud_mode: {cloud_mode}")
    threshold = int(cloud_max_branch_rows)
    if mode == "share" and cloud_max_branch_share is not None and wave_respondents is not None and wave_respondents > 0:
        share_threshold = int(round(float(wave_respondents) * float(cloud_max_branch_share)))
        threshold = max(threshold, share_threshold)
    return int(branch_rows) <= max(0, threshold)


def build_position_signature_rows(question_df: pd.DataFrame, question_meta: dict[str, Any], max_features: int = 5) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if question_df.empty:
        return rows
    anchor = question_meta.get("question_id", "")
    branch_key = "::".join(
        str(part or "")
        for part in [
            question_meta.get("source", ""),
            question_meta.get("canonical_wave", question_meta.get("wave", "")),
            question_meta.get("country_code", ""),
            anchor,
        ]
    ).strip(":")
    if "response_value_normalized" in question_df.columns:
        target = question_df["response_value_normalized"]
    else:
        target = pd.Series([""] * len(question_df), index=question_df.index, dtype="object")
    feature_candidates = []
    for col in question_df.columns:
        role = _feature_role(col)
        if role != "POSITION_COORDINATE":
            continue
        feature_series = question_df[col].fillna("").astype(str).str.strip()
        if feature_series.eq("").all():
            continue
        if not _contract_allows(question_meta, "allowed_as_branch_position_signature") and not bool(question_meta.get("allowed_as_branch_position_signature", False)):
            continue
        stats = _candidate_association_stats(question_df[col], target)
        if stats is None:
            target_series = target.fillna("").astype(str).str.strip()
            target_value, target_share = dominant_response(target_series)
            stats = {
                "association_score": 0.0,
                "association_metric": "presence_only",
                "normalized_mutual_information": 0.0,
                "cramers_v": 0.0,
                "n_unweighted": int(feature_series.ne("").sum()),
                "n_unique_feature_values": int(feature_series[feature_series.ne("")].nunique(dropna=False)),
                "n_unique_response_values": int(target_series[target_series.ne("")].nunique(dropna=False)),
                "target_dominant_response": target_value,
                "target_dominant_response_share": float(target_share),
            }
        feature_candidates.append(
            {
                "feature_name": col,
                "feature_kind": "demographic",
                "demographic_feature_excluded_flag": False,
                **stats,
            }
        )
    feature_candidates.sort(
        key=lambda row: (
            -float(row.get("association_score", 0.0)),
            -int(row.get("n_unweighted", 0)),
            str(row.get("feature_name", "")),
        )
    )
    for rank, candidate in enumerate(feature_candidates[:max_features], start=1):
        rows.append(
            {
                **question_meta,
                "branch_id": anchor,
                "branch_key": branch_key,
                "anchor_question_id": anchor,
                "feature_rank": rank,
                "predictor_family": candidate["feature_kind"],
                "feature_role": _feature_role(candidate["feature_name"]),
                "support_status": _support_status_from_count(candidate.get("n_unweighted"), question_meta.get("n_respondents")),
                "confidence_tier": _confidence_tier_from_stats(
                    candidate,
                    support_status=_support_status_from_count(candidate.get("n_unweighted"), question_meta.get("n_respondents")),
                    total_respondents=question_meta.get("n_respondents"),
                ),
                "high_cardinality_flag": _high_cardinality_flag(candidate),
                "rare_category_flag": _rare_category_flag(candidate),
                "rare_category_handling": _rare_category_handling(candidate),
                "cloud_lane_artifact": True,
                "diagnostic_artifact": True,
                "not_direct_evidence": True,
                "evidence_role": "diagnostic_position_signature",
                "artifact_status": "enabled_diagnostic",
                **candidate,
            }
        )
    return rows


def build_co_signature_rows(question_df: pd.DataFrame, question_meta: dict[str, Any], max_features: int = 5) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if question_df.empty:
        return rows
    if not valid_cloud_feature(question_meta):
        return rows
    if not _contract_allows(question_meta, "allowed_as_branch_relation_cosignature"):
        return rows
    allowlist = _csv_allowlist(question_meta, "branch_relation_feature_allowlist", "relation_feature_allowlist")
    if allowlist:
        candidate_columns = [col for col in question_df.columns if col in allowlist]
    else:
        candidate_columns = [
            col
            for col in question_df.columns
            if col not in EXCLUDED_FEATURES
            and col not in TECHNICAL_FEATURES
            and col not in DEMOGRAPHIC_FEATURES
            and col not in POSITION_FEATURES
            and col not in {"response_value_normalized", "response_label", "normalized_response_label", "question_id", "var_code", "var_name"}
        ]
    if not candidate_columns:
        return rows
    anchor = question_meta.get("question_id", "")
    branch_key = "::".join(
        str(part or "")
        for part in [
            question_meta.get("source", ""),
            question_meta.get("canonical_wave", question_meta.get("wave", "")),
            question_meta.get("country_code", ""),
            anchor,
        ]
    ).strip(":")
    if "response_value_normalized" in question_df.columns:
        target = question_df["response_value_normalized"]
    else:
        target = pd.Series([""] * len(question_df), index=question_df.index, dtype="object")
    feature_candidates = []
    for col in candidate_columns:
        role = _feature_role(col)
        if role in {"ADMINISTRATIVE_METADATA", "POSITION_COORDINATE", "GENERATION_FORBIDDEN"}:
            continue
        if col not in question_df.columns:
            continue
        stats = _candidate_association_stats(question_df[col], target)
        if stats is None:
            continue
        feature_candidates.append(
            {
                "feature_name": col,
                "feature_kind": "relation_evidence",
                "demographic_feature_excluded_flag": False,
                "feature_role": "RELATION_EVIDENCE",
                **stats,
            }
        )
    feature_candidates.sort(
        key=lambda row: (
            -float(row.get("association_score", 0.0)),
            -int(row.get("n_unweighted", 0)),
            str(row.get("feature_name", "")),
        )
    )
    for rank, candidate in enumerate(feature_candidates[:max_features], start=1):
        rows.append(
            {
                **question_meta,
                "branch_id": anchor,
                "branch_key": branch_key,
                "anchor_question_id": anchor,
                "feature_rank": rank,
                "predictor_family": candidate["feature_kind"],
                "feature_role": _feature_role(candidate["feature_name"]),
                "support_status": _support_status_from_count(candidate.get("n_unweighted"), question_meta.get("n_respondents")),
                "confidence_tier": _confidence_tier_from_stats(
                    candidate,
                    support_status=_support_status_from_count(candidate.get("n_unweighted"), question_meta.get("n_respondents")),
                    total_respondents=question_meta.get("n_respondents"),
                ),
                "cloud_lane_artifact": True,
                "diagnostic_artifact": True,
                "not_direct_evidence": True,
                "evidence_role": "diagnostic_relation_cosignature",
                "artifact_status": "enabled_contract_gated" if _contract_allows(question_meta, "allowed_as_branch_relation_cosignature") else "disabled_no_contract_allowlist",
                **candidate,
            }
        )
    return rows


def build_attitude_cloud_rows(question_df: pd.DataFrame, question_meta: dict[str, Any]) -> list[dict[str, Any]]:
    current_meta = _question_cloud_meta(question_meta, question_df)
    if not valid_cloud_feature(current_meta):
        return []
    if _attitude_cloud_semantics_blocked(current_meta):
        return []
    current_frame = _prepare_attitude_cloud_frame(question_df, current_meta)
    if current_frame.empty:
        return []
    key = _cloud_state_key(current_meta)
    state = _ATTITUDE_CLOUD_STATE.setdefault(key, {})
    current_qid = current_meta.get("question_id", "")
    current_anchor_allowed = bool(current_meta.get("allowed_as_attitude_cloud_anchor", False))
    current_feature_allowed = bool(current_meta.get("allowed_as_attitude_cloud_feature", False))
    if current_anchor_allowed:
        rows: list[dict[str, Any]] = []
        for candidate_qid, candidate in state.items():
            if candidate_qid == current_qid:
                continue
            candidate_meta = candidate["meta"]
            if candidate_meta.get("question_id", "") == current_qid:
                continue
            rows.extend(_emit_attitude_cloud_pair(current_frame, current_meta, candidate["frame"], candidate_meta))
    else:
        rows = []
    if current_feature_allowed or current_anchor_allowed:
        state[current_qid] = {"frame": current_frame, "meta": current_meta}
    return rows
