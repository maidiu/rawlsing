#!/usr/bin/env python3
"""Validation helpers for V550 shard and merge execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import re

import pandas as pd

from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, support_threshold_series

from data.ddm_build_copy.ddm_v550_schema import (
    SHARD_MANIFEST_SCHEMA,
    SHARD_PLAN_SCHEMA,
    V551_BRIDGE_INDEX_SCHEMA,
    QUESTION_USE_CONTRACT_SCHEMA,
    SOURCE_STRUCTURE_POPULATION_AUDIT_SCHEMA,
    V551_ATOM_EXCLUSION_AUDIT_SCHEMA,
    CONDITIONAL_DETERMINICITY_INDEX_SCHEMA,
    V551_RELATION_EVIDENCE_ATOMS_SCHEMA,
    V552_CONTRADICTION_TENSOR_SCHEMA,
    V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA,
    V552_DRIVER_FACET_PRESSURE_SCHEMA,
    V552_HORIZON_CONSTRAINT_INDEX_SCHEMA,
    V552_RELATION_AXIS_PRESSURE_SCHEMA,
    V552_CONDITIONAL_DETERMINICITY_STATUS_AUDIT_SCHEMA,
    V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA,
    V552_TARGET_ENTITY_PRESSURE_SCHEMA,
    validate_bridge_index,
    validate_columns,
    validate_no_forbidden_cloud_features,
    validate_shard_manifest,
)
from data.ddm_build_copy.ddm_v550_clouds import QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS


def _to_bool(value: object, default: bool = False) -> bool:
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


def _bool_series(df: pd.DataFrame, column: str, default: bool = False) -> pd.Series:
    if column not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    return df[column].map(lambda value: _to_bool(value, default))


def _normalized_tokens(value: object) -> set[str]:
    text = str(value or "").strip().lower()
    if not text:
        return set()
    return {token for token in re.split(r"[^a-z0-9]+", text) if token}


def _contains_forbidden_token(value: object, forbidden_tokens: set[str]) -> bool:
    tokens = _normalized_tokens(value)
    return any(token in tokens for token in forbidden_tokens)


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


def _is_numeric_only_label(value: object) -> bool:
    text = str(value or "").strip()
    return bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", text))


def _response_family_allows_numeric_only_label(value: object) -> bool:
    family = str(value or "").strip().lower()
    if not family:
        return False
    if family in NUMERIC_ONLY_LABEL_ALLOWED_FAMILIES:
        return True
    return family.endswith("_scale") or any(token in family for token in {"numeric", "quantity", "count"})


def validate_shard_plan(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, SHARD_PLAN_SCHEMA["required_columns"], "shard_plan")


def validate_bridge_index_df(df: pd.DataFrame) -> list[str]:
    return validate_bridge_index(df)


def validate_shard_manifest_df(manifest: dict[str, Any]) -> list[str]:
    return validate_shard_manifest(manifest)


def validate_response_distribution_rows(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty:
        return issues
    if "response_value_normalized" not in df.columns:
        issues.append("response_distribution: missing response_value_normalized")
    if "pct_unweighted" in df.columns and ((df["pct_unweighted"].fillna(0) < 0) | (df["pct_unweighted"].fillna(0) > 1)).any():
        issues.append("response_distribution: pct_unweighted out of range")
    if "pct_weighted" in df.columns and ((df["pct_weighted"].fillna(0) < 0) | (df["pct_weighted"].fillna(0) > 1)).any():
        issues.append("response_distribution: pct_weighted out of range")
    return issues


def validate_weight_fields(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty or "weight_status" not in df.columns:
        return issues
    if "n_weighted" in df.columns and df["weight_status"].fillna("").isin(["missing", "invalid", "unweighted_only"]).any():
        bad = df.loc[df["weight_status"].fillna("").isin(["missing", "invalid", "unweighted_only"]), "n_weighted"].fillna("")
        if any(str(v).strip() not in {"", "nan", "None"} for v in bad.tolist()):
            issues.append("weight_fields: weighted counts must be null when weights are unavailable")
    return issues


def validate_question_use_contract(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, QUESTION_USE_CONTRACT_SCHEMA["required_columns"], "question_use_contract")


def validate_source_structure_population_audit(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, SOURCE_STRUCTURE_POPULATION_AUDIT_SCHEMA["required_columns"], "source_structure_population_audit")


def validate_v551_relation_evidence_atoms_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_RELATION_EVIDENCE_ATOMS_SCHEMA["required_columns"], "v551_relation_evidence_atoms")


def validate_v551_atom_exclusion_audit_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"], "v551_atom_exclusion_audit")


def validate_conditional_determinicity_index_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"], "conditional_determinicity_index")


def validate_position_signature_rows(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty:
        return issues
    if "feature_kind" in df.columns:
        forbidden = df["feature_kind"].fillna("").str.lower().isin({"admin", "metadata", "relation_evidence"})
        if forbidden.any():
            issues.append("position_signature: forbidden feature kinds present")
    if "demographic_feature_excluded_flag" in df.columns and _bool_series(df, "demographic_feature_excluded_flag", False).any():
        issues.append("position_signature: demographic_feature_excluded_flag must remain false")
    return issues


def validate_relation_signature_rows(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty:
        return issues
    if "feature_kind" in df.columns:
        forbidden = df["feature_kind"].fillna("").str.lower().isin({"demographic", "admin", "metadata", "position_coordinate"})
        if forbidden.any():
            issues.append("relation_signature: forbidden feature kinds present")
    if "feature_name" in df.columns and "feature_value" in df.columns:
        if (df["feature_name"].fillna("").astype(str).str.strip().eq("") | df["feature_value"].fillna("").astype(str).str.strip().eq("")).any():
            issues.append("relation_signature: missing feature_name or feature_value")
    return issues


def validate_attitude_cloud_rows(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    issues = validate_columns(df, QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS, "attitude_cloud")
    issues.extend(validate_no_forbidden_cloud_features(df))
    required_nonempty = [
        "run_id",
        "shard_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "anchor_question_id",
        "anchor_var_code",
        "cotravelling_question_id",
        "cotravelling_var_code",
        "anchor_response_semantics_status",
        "anchor_response_semantics_source",
        "anchor_response_semantics_contract_hash",
        "anchor_source_structure_source",
        "anchor_source_structure_basis",
        "anchor_source_structure_confidence",
        "anchor_question_use_contract_hash",
        "cotravelling_response_semantics_status",
        "cotravelling_response_semantics_source",
        "cotravelling_response_semantics_contract_hash",
        "cotravelling_source_structure_source",
        "cotravelling_source_structure_basis",
        "cotravelling_source_structure_confidence",
        "cotravelling_question_use_contract_hash",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "source_structure_source",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_contract_hash",
        "question_use_contract_hash",
        "artifact_status",
        "cloud_engine_version",
        "cloud_feature",
        "cloud_value",
    ]
    for column in required_nonempty:
        if column in df.columns and df[column].fillna("").astype(str).str.strip().eq("").any():
            issues.append(f"attitude_cloud: missing required provenance field {column}")
    if "artifact_status" in df.columns:
        allowed_artifact_status = {"prototype_diagnostic"}
        if not df["artifact_status"].fillna("").astype(str).str.strip().isin(allowed_artifact_status).all():
            issues.append("attitude_cloud: artifact_status must remain prototype_diagnostic")
    if "cloud_lane_artifact" in df.columns and _bool_series(df, "cloud_lane_artifact", False).eq(False).any():
        issues.append("attitude_cloud: cloud_lane_artifact must remain true")
    if "diagnostic_artifact" in df.columns and _bool_series(df, "diagnostic_artifact", False).eq(False).any():
        issues.append("attitude_cloud: diagnostic_artifact must remain true")
    if "not_direct_evidence" in df.columns and _bool_series(df, "not_direct_evidence", False).eq(False).any():
        issues.append("attitude_cloud: not_direct_evidence must remain true")
    if "same_question_flag" in df.columns and _bool_series(df, "same_question_flag", False).any():
        issues.append("attitude_cloud: same_question_flag must remain false")
    if "anchor_question_id" in df.columns and "cotravelling_question_id" in df.columns:
        if (df["anchor_question_id"].fillna("").astype(str) == df["cotravelling_question_id"].fillna("").astype(str)).any():
            issues.append("attitude_cloud: self-question distribution detected")
    elif "anchor_question_id" in df.columns and "cloud_feature" in df.columns:
        if (df["anchor_question_id"].fillna("").astype(str) == df["cloud_feature"].fillna("").astype(str)).any():
            issues.append("attitude_cloud: self-question distribution detected")
    return issues


def validate_v551_bridge_rows(df: pd.DataFrame) -> list[str]:
    issues = validate_bridge_index(df)
    issues.extend(validate_semantic_authority_alignment(df))
    if df.empty:
        return issues
    required_role_cols = [
        "bridge_evidence_lane",
        "support_status",
        "v551_conditional_determinicity_eligible",
        "usable_for_evidence",
        "semantic_role",
        "v551_visible",
        "v551_evidence_role",
        "v551_context_eligible",
        "v551_position_coordinate_eligible",
        "v551_relation_evidence_eligible",
        "v551_cloud_eligible",
        "v551_persona_packet_eligible",
        "question_use_contract_joined",
    ]
    issues.extend(validate_columns(df, required_role_cols, "v551_bridge_index"))
    if "bridge_evidence_lane" in df.columns:
        allowed_lanes = {
            "direct_relation_response",
            "derived_determinicity",
            "position_context",
            "structural_context",
            "audit_quarantine",
            "disabled_artifact",
            "unknown",
        }
        lane_values = df["bridge_evidence_lane"].fillna("").astype(str).str.strip()
        if (~lane_values.isin(allowed_lanes)).any():
            issues.append("v551_bridge_index: invalid bridge_evidence_lane values present")
    if "support_status" in df.columns:
        allowed_support = {"sufficient_support", "underpowered", "zero_support", "missing_support", "not_applicable"}
        support_values = df["support_status"].fillna("").astype(str).str.strip()
        if (~support_values.isin(allowed_support)).any():
            issues.append("v551_bridge_index: invalid support_status values present")
    if "v551_relation_evidence_eligible" in df.columns and "semantic_role" in df.columns:
        bad = df.loc[
            _bool_series(df, "v551_relation_evidence_eligible", False)
            & df["semantic_role"].fillna("").astype(str).ne("RELATION_EVIDENCE")
        ]
        if not bad.empty:
            issues.append("v551_bridge_index: non-relation rows marked relation-evidence eligible")
    if "v551_relation_evidence_eligible" in df.columns and "bridge_evidence_lane" in df.columns:
        bad = df.loc[
            _bool_series(df, "v551_relation_evidence_eligible", False)
            & df["bridge_evidence_lane"].fillna("").astype(str).ne("direct_relation_response")
        ]
        if not bad.empty:
            issues.append("v551_bridge_index: non-direct relation rows marked relation-evidence eligible")
    if "v551_conditional_determinicity_eligible" in df.columns and "bridge_evidence_lane" in df.columns:
        bad = df.loc[
            _bool_series(df, "v551_conditional_determinicity_eligible", False)
            & df["bridge_evidence_lane"].fillna("").astype(str).ne("derived_determinicity")
        ]
        if not bad.empty:
            issues.append("v551_bridge_index: non-derived rows marked conditional determinicity eligible")
    if "v551_relation_evidence_eligible" in df.columns:
        relation_rows = _bool_series(df, "v551_relation_evidence_eligible", False)
        if relation_rows.any():
            relation = df.loc[relation_rows]
            forbidden_ids = {
                "context",
                "context_not_applicable",
                "survey_admin_context",
                "administrative_context",
                "technical_metadata",
                "sample_design_context",
                "weighting_context",
            }
            forbidden_tokens = {"admin", "metadata", "technical", "survey_admin", "sample_design", "weight"}
            if "relation_axis_id" in relation.columns:
                axis = relation["relation_axis_id"].fillna("").astype(str)
                if axis.map(lambda value: value.strip().lower() in forbidden_ids or _contains_forbidden_token(value, forbidden_tokens)).any():
                    issues.append("v551_bridge_index: relation-evidence eligible rows must not use admin/context relation_axis_id")
            if "target_entity_id" in relation.columns:
                target = relation["target_entity_id"].fillna("").astype(str)
                if target.map(lambda value: value.strip().lower() in forbidden_ids or _contains_forbidden_token(value, forbidden_tokens)).any():
                    issues.append("v551_bridge_index: relation-evidence eligible rows must not use admin/context target_entity_id")
            if "driver_id" in relation.columns and relation["driver_id"].fillna("").astype(str).map(lambda value: value.startswith("metadata::") or _contains_forbidden_token(value, forbidden_tokens)).any():
                issues.append("v551_bridge_index: relation-evidence eligible rows must not use metadata-like drivers")
            if "is_substantive" in relation.columns and ~_bool_series(relation, "is_substantive", False).all():
                issues.append("v551_bridge_index: relation-evidence eligible rows must be substantive")
            if "is_special" in relation.columns and _bool_series(relation, "is_special", False).any():
                issues.append("v551_bridge_index: relation-evidence eligible rows must not be special")
            if "allowed_as_v551_relation_evidence" in relation.columns and ~_bool_series(relation, "allowed_as_v551_relation_evidence", False).all():
                issues.append("v551_bridge_index: relation-evidence eligible rows must be contract-allowed")
            if "question_use_contract_joined" in relation.columns and ~_bool_series(relation, "question_use_contract_joined", False).all():
                issues.append("v551_bridge_index: relation-evidence eligible rows must be joined to question_use_contract")
            if "review_required" in relation.columns and _bool_series(relation, "review_required", False).any():
                issues.append("v551_bridge_index: relation-evidence eligible rows must not require review")
            if "normalized_response_label" in relation.columns and relation["normalized_response_label"].fillna("").astype(str).str.strip().eq("").any():
                issues.append("v551_bridge_index: relation-evidence eligible rows must have normalized_response_label")
            if "response_option_map_matched" in relation.columns and ~_bool_series(relation, "response_option_map_matched", True).all():
                issues.append("v551_bridge_index: relation-evidence eligible rows must match response option map")
            if "normalization_confidence" in relation.columns:
                low_conf = relation["normalization_confidence"].fillna("").astype(str).str.lower().isin({"", "observed_only", "low"})
                if low_conf.any():
                    issues.append("v551_bridge_index: relation-evidence eligible rows must have sufficient normalization_confidence")
            if "n_unweighted" in relation.columns:
                support = pd.to_numeric(relation["n_unweighted"], errors="coerce")
                thresholds = support_threshold_series(relation.get("n_respondents", pd.Series([None] * len(relation), index=relation.index)))
                if support.isna().any() or (support.fillna(0).astype(float) < thresholds.fillna(DEFAULT_SUPPORT_CAP).astype(float)).any():
                    issues.append("v551_bridge_index: relation-evidence eligible rows must meet minimum support")
            if "support_status" in relation.columns and ~relation["support_status"].fillna("").astype(str).str.strip().eq("sufficient_support").all():
                issues.append("v551_bridge_index: relation-evidence eligible rows must have sufficient_support")
            if "response_label" in relation.columns:
                numeric_only = relation["response_label"].fillna("").astype(str).map(_is_numeric_only_label)
                if numeric_only.any():
                    family = relation["response_family"].fillna("").astype(str)
                    confidence = relation["normalization_confidence"].fillna("").astype(str).str.lower() if "normalization_confidence" in relation.columns else pd.Series([""] * len(relation), index=relation.index)
                    allowed = family.map(_response_family_allows_numeric_only_label) & confidence.eq("high")
                    bad = numeric_only & ~allowed
                    if bad.any():
                        issues.append("v551_bridge_index: relation-evidence eligible rows must use numeric-only labels only for numeric/scale families with high normalization confidence")
            if "response_family" in relation.columns and relation["response_family"].fillna("").astype(str).str.lower().eq("country_code").any():
                issues.append("v551_bridge_index: relation-evidence eligible rows must not use country_code response_family by default")
            if "source_structure_fields_joined" in relation.columns:
                joined = _bool_series(relation, "source_structure_fields_joined", False)
                if joined.any():
                    blank_fields = pd.Series([True] * len(relation), index=relation.index)
                    for field in ["question_type", "handling_rule", "recommended_computation", "source_structure_classification"]:
                        if field in relation.columns:
                            blank_fields &= relation[field].fillna("").astype(str).str.strip().eq("")
                    if (joined & blank_fields).any():
                        issues.append("v551_bridge_index: relation-evidence eligible rows must not have blank source structure fields when joined")
    if "source_table" in df.columns:
        position_rows = df["source_table"].fillna("").astype(str).eq("position_distribution")
        if position_rows.any():
            pos = df.loc[position_rows]
            if "semantic_role" in pos.columns and ~pos["semantic_role"].fillna("").astype(str).eq("POSITION_COORDINATE").all():
                issues.append("v551_bridge_index: position_distribution rows must bridge as POSITION_COORDINATE")
            if "bridge_evidence_lane" in pos.columns and ~pos["bridge_evidence_lane"].fillna("").astype(str).eq("position_context").all():
                issues.append("v551_bridge_index: position_distribution rows must bridge as position_context")
            if "position_field" in pos.columns and pos["position_field"].fillna("").astype(str).str.strip().eq("").any():
                issues.append("v551_bridge_index: position_distribution rows must carry position_field")
            if "position_value" in pos.columns and pos["position_value"].fillna("").astype(str).str.strip().eq("").any():
                issues.append("v551_bridge_index: position_distribution rows must carry position_value")
            if "v551_relation_evidence_eligible" in pos.columns and _bool_series(pos, "v551_relation_evidence_eligible", False).any():
                issues.append("v551_bridge_index: position_distribution rows must not be relation-evidence eligible")
    return issues


def validate_semantic_authority_alignment(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty:
        return issues
    if "bridge_evidence_lane" not in df.columns:
        issues.append("semantic_authority: missing bridge_evidence_lane")
        return issues

    lane = df["bridge_evidence_lane"].fillna("").astype(str).str.strip()
    evidentiary = lane.isin({"direct_relation_response", "derived_determinicity"})

    if evidentiary.any():
        if "response_semantics_status" not in df.columns:
            issues.append("semantic_authority: missing response_semantics_status on evidentiary rows")
        else:
            status = df["response_semantics_status"].fillna("").astype(str).str.strip().str.lower()
            if (evidentiary & status.eq("")).any():
                issues.append("semantic_authority: missing response_semantics_status on evidentiary rows")
            if (evidentiary & status.isin({"stale_contract", "missing_contract", "ambiguous"})).any():
                issues.append("semantic_authority: stale or ambiguous response semantics present on evidentiary rows")
            direct = lane.eq("direct_relation_response")
            curated_statuses = {
                "curated", "curated_packet", "certified",
                "manual_authority_all_eight", "curated_unsigned",
                "authority_curated", "family_curated",
            }
            # A direct-relation lane is itself an evidentiary claim.  It may not
            # carry observed-only or inferred response semantics even when a
            # downstream eligibility column is absent or currently false.
            if (direct & ~status.isin(curated_statuses)).any():
                issues.append("semantic_authority: direct relation rows must carry curated response semantics")
        if "response_semantics_source" not in df.columns:
            issues.append("semantic_authority: missing response_semantics_source on evidentiary rows")
        else:
            source = df["response_semantics_source"].fillna("").astype(str).str.strip()
            if (evidentiary & source.eq("")).any():
                issues.append("semantic_authority: missing response_semantics_source on evidentiary rows")
        if "response_semantics_contract_hash" not in df.columns:
            issues.append("semantic_authority: missing response_semantics_contract_hash on evidentiary rows")
        else:
            contract_hash = df["response_semantics_contract_hash"].fillna("").astype(str).str.strip()
            if (evidentiary & contract_hash.eq("")).any():
                issues.append("semantic_authority: missing response_semantics_contract_hash on evidentiary rows")

        if "source_structure_fields_joined" not in df.columns:
            issues.append("semantic_authority: missing source_structure_fields_joined on evidentiary rows")
        elif _bool_series(df, "source_structure_fields_joined", False).any():
            joined = _bool_series(df, "source_structure_fields_joined", False)
            if "source_structure_source" in df.columns and (joined & df["source_structure_source"].fillna("").astype(str).str.strip().eq("")).any():
                issues.append("semantic_authority: missing source_structure_source on joined rows")
            if "source_structure_basis" in df.columns and (joined & df["source_structure_basis"].fillna("").astype(str).str.strip().eq("")).any():
                issues.append("semantic_authority: missing source_structure_basis on joined rows")
            if "source_structure_confidence" in df.columns and (joined & df["source_structure_confidence"].fillna("").astype(str).str.strip().eq("")).any():
                issues.append("semantic_authority: missing source_structure_confidence on joined rows")
    return issues


def validate_shard_promotability(shard_dir: Path) -> list[str]:
    issues: list[str] = []
    status_path = shard_dir / "shard_status.json"
    manifest_path = shard_dir / "shard_manifest.json"
    if not status_path.exists():
        issues.append("missing shard_status.json")
    if not manifest_path.exists():
        issues.append("missing shard_manifest.json")
    return issues


def validate_merge_outputs(run_dir: Path) -> list[str]:
    issues: list[str] = []
    if not run_dir.exists():
        issues.append("run_dir missing")
    return issues


def validate_no_cloud_leakage(df: pd.DataFrame) -> list[str]:
    return validate_attitude_cloud_rows(df)


def validate_v552_relation_axis_pressure_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_RELATION_AXIS_PRESSURE_SCHEMA["required_columns"], "v552_relation_axis_pressure")


def validate_v552_target_entity_pressure_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_TARGET_ENTITY_PRESSURE_SCHEMA["required_columns"], "v552_target_entity_pressure")


def validate_v552_driver_facet_pressure_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_DRIVER_FACET_PRESSURE_SCHEMA["required_columns"], "v552_driver_facet_pressure")


def validate_v552_contradiction_tensor_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"], "v552_contradiction_tensor")


def validate_v552_structural_channel_index_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"], "v552_structural_channel_index")


def validate_v552_country_wave_pressure_profile_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA["required_columns"], "v552_country_wave_pressure_profile")


def validate_v552_horizon_constraint_index_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_HORIZON_CONSTRAINT_INDEX_SCHEMA["required_columns"], "v552_horizon_constraint_index")


def validate_v552_conditional_determinicity_status_audit_df(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_CONDITIONAL_DETERMINICITY_STATUS_AUDIT_SCHEMA["required_columns"], "v552_conditional_determinicity_status_audit")


def write_validation_report(path: Path, *, issues: list[str], warnings: list[str] | None = None) -> None:
    payload = {"issues": issues, "warnings": warnings or []}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pd.Series(payload).to_json(indent=2), encoding="utf-8")
