#!/usr/bin/env python3
"""V551J packet assembly helpers."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd

from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_AUTHORITY_STATUSES,
    V551J_COMPILER_VERSION,
    V551J_DIRECTIONALITY_STATUSES,
    V551J_FORBIDDEN_CLAIM_IDS,
    V551J_FUTURE_TARGET_AFFORDANCES,
    V551J_PACKET_CANDIDATE_TRACE_SCHEMA,
    V551J_PACKET_EXCLUSION_AUDIT_SCHEMA,
    V551J_PACKET_READINESS_REPORT_SCHEMA,
    V551J_JOIN_KEY_DIAGNOSTICS_SCHEMA,
    V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
)
from data.ddm_build_copy.ddm_v551j_contract import (
    recompute_joint_component_measurement_signature,
    recompute_joint_empirical_distribution_signature,
    recompute_joint_measurement_contract_hash,
    recompute_joint_orientation_signature,
    recompute_joint_response_identity_signature,
    recompute_joint_semantic_signature,
    recompute_joint_structural_signature,
    recompute_joint_target_signature,
    recompute_joint_topology_signature,
    recompute_v551j_component_contract_hash,
    recompute_v551j_component_id,
    recompute_v551j_packet_id,
    recompute_v551j_v2_2_3_packet_contract_hash,
)
from data.ddm_build_copy.ddm_v551j_validation import (
    validate_candidate_trace_schema,
)
from data.ddm_build_copy.ddm_v550_manifest import utc_now


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


def _stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _json_array(values: Iterable[Any] | None) -> str:
    if values is None:
        return "[]"
    seen: list[str] = []
    for value in values:
        cleaned = _clean(value)
        if cleaned and cleaned not in seen:
            seen.append(cleaned)
    return json.dumps(seen, ensure_ascii=False)


def _json_object(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, ensure_ascii=False, sort_keys=True, default=str)


def _first_nonempty(*values: Any) -> str:
    for value in values:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
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


def _confidence_tier_rank(value: Any) -> int:
    cleaned = _clean(value).lower()
    if cleaned == "high":
        return 3
    if cleaned == "medium":
        return 2
    if cleaned == "low":
        return 1
    return 0


def _best_confidence_tier(*values: Any) -> str:
    best_tier = "unknown"
    best_rank = 0
    for value in values:
        cleaned = _clean(value).lower()
        rank = _confidence_tier_rank(cleaned)
        if rank > best_rank:
            best_rank = rank
            best_tier = cleaned
    return best_tier if best_rank > 0 else "unknown"


def _series_first(frame: pd.DataFrame, column: str, default: Any = "") -> Any:
    if column not in frame.columns or frame.empty:
        return default
    value = frame.iloc[0].get(column, default)
    return default if pd.isna(value) else value


def _pick_join_row(frame: pd.DataFrame, keys: list[tuple[str, Any]]) -> pd.Series | None:
    if frame.empty:
        return None
    candidate = frame.copy()
    matched = False
    for column, value in keys:
        if column not in candidate.columns:
            continue
        variants = _join_token_variants(value)
        if not variants:
            continue
        candidate = candidate[candidate[column].astype(str).str.strip().isin(variants)]
        matched = True
        if candidate.empty:
            return None
    if not matched or candidate.empty:
        return None
    return candidate.iloc[0]


def _classify_authority(row: pd.Series, join_strategy: str) -> tuple[str, str]:
    if join_strategy == "priority_a":
        return "exact_registry", "source_wave_country_family_pattern"
    if join_strategy == "priority_b":
        return "prefix_registry", "question_variable_overlap"
    if join_strategy == "priority_c":
        return "semantic_role", "semantic_axis_overlap"
    if join_strategy == "priority_d":
        return "computed_context", "context_only_fallback"
    if _clean(row.get("association_publication_status")) == "publishable":
        return "computed_context", "association_context"
    return "unknown", "unknown_join_authority"


def _directionality_status(row: pd.Series) -> str:
    value = _clean(row.get("directionality_status"))
    if value in V551J_DIRECTIONALITY_STATUSES:
        return value
    if value in {"inferred_from_directionality_overlay", "directionality_overlay", "overlay_directionality"}:
        return "known_directional"
    if value in {"inferred_from_response_family", "response_family_directionality", "family_directionality"}:
        return "partial_directionality"
    if value:
        return "unknown"
    return "not_applicable"


def _v552_context_bundle(
    qsh_row: pd.Series | None,
    contradiction_row: pd.Series | None,
    parent_row: pd.Series | None,
) -> pd.Series:
    qsh_row = qsh_row if qsh_row is not None else pd.Series(dtype=object)
    contradiction_row = contradiction_row if contradiction_row is not None else pd.Series(dtype=object)
    parent_row = parent_row if parent_row is not None else pd.Series(dtype=object)

    qsh_joined = not qsh_row.empty
    contradiction_joined = not contradiction_row.empty
    parent_joined = not parent_row.empty

    bundle = {
        "v552_context_status": "joined" if (qsh_joined or contradiction_joined or parent_joined) else "not_supplied",
        "v552_question_semantic_hierarchy_join_status": "joined" if qsh_joined else "not_supplied",
        "v552_contradiction_context_status": "joined" if contradiction_joined else "not_supplied",
        "v552_parent_prior_context_status": "joined" if parent_joined else "not_supplied",
        "v552_structural_refs_json": _json_array([
            qsh_row.get("question_semantic_hierarchy_id"),
            qsh_row.get("question_id"),
            qsh_row.get("var_code"),
            qsh_row.get("relation_axis_id"),
            qsh_row.get("target_entity_id"),
            qsh_row.get("driver_facet_id"),
        ]) if qsh_joined else "[]",
        "v552_contradiction_refs_json": _json_array([
            contradiction_row.get("question_id"),
            contradiction_row.get("var_code"),
            contradiction_row.get("relation_axis_id"),
            contradiction_row.get("target_entity_id"),
            contradiction_row.get("driver_facet_id"),
        ]) if contradiction_joined else "[]",
        "v552_horizon_constraint_refs_json": _json_array([
            qsh_row.get("question_semantic_hierarchy_id"),
            qsh_row.get("question_id"),
            qsh_row.get("var_code"),
            qsh_row.get("horizon_affordance"),
            qsh_row.get("horizon_type"),
            qsh_row.get("horizon_scope"),
            qsh_row.get("horizon_reach"),
        ]) if qsh_joined else "[]",
        "v552_parent_prior_refs_json": _json_array([
            parent_row.get("parent_prior_manifest_id"),
            parent_row.get("question_id"),
            parent_row.get("var_code"),
        ]) if parent_joined else "[]",
    }
    return pd.Series(bundle, dtype=object)


def _packet_type_for_join(*, atom_joined: bool, pattern_joined: bool, association_joined: bool, v552_joined: bool) -> str:
    if atom_joined and pattern_joined:
        return "joint_relation_evidence_packet"
    if pattern_joined and not atom_joined:
        return "joint_pattern_context_packet"
    if association_joined and not atom_joined:
        return "conditional_support_packet"
    if v552_joined and not atom_joined and not pattern_joined:
        return "contradiction_candidate_packet"
    return "known_absence_packet"


def _future_affordances(row: pd.Series) -> list[str]:
    affordances: list[str] = ["structural_context_support"]
    if _clean(row.get("boundary_pattern_type")) or _clean(row.get("pattern_id")):
        affordances.append("joint_morphology_support")
    tags = " ".join([
        _clean(row.get("semantic_tags_json")),
        _clean(row.get("strata_path_json")),
        _clean(row.get("top_identity_context_signals_json")),
        _clean(row.get("top_position_context_signals_json")),
        _clean(row.get("top_family_background_signals_json")),
        _clean(row.get("top_unknown_or_diagnostic_signals_json")),
        _clean(row.get("horizon_affordance")),
    ]).lower()
    if any(token in tags for token in ["family", "household", "parent", "coparent", "child", "children", "marriage", "spouse", "home", "domestic", "kin", "intergenerational"]):
        affordances.append("household_mediation_possible")
    if any(token in tags for token in ["relig", "school", "work", "media", "institution", "community"]):
        affordances.append("carrier_mediation_possible")
    horizon_tags = " ".join([
        _clean(row.get("semantic_tags_json")),
        _clean(row.get("strata_path_json")),
        _clean(row.get("v552_horizon_constraint_refs_json")),
        _clean(row.get("horizon_affordance")),
    ]).lower()
    if any(token in horizon_tags for token in ["horizon", "absolute", "transcendent", "metaphysical", "sacred", "ultimate", "meaning"]):
        affordances.append("horizon_relation_possible")
    if _clean(row.get("v552_context_status")) not in {"", "not_supplied"}:
        if _clean(row.get("v552_horizon_constraint_refs_json")) not in {"", "[]"} or _clean(row.get("horizon_affordance")):
            affordances.append("horizon_relation_possible")
    if _clean(row.get("v552_context_status")) not in {"", "not_supplied"}:
        affordances.append("contradiction_rupture_support")
    if _clean(row.get("directionality_status")) in {"known_directional", "partial_directionality"}:
        affordances.append("temporal_pressure_support")
        affordances.append("pressureflow_mediation_required")
    if _clean(row.get("packet_type")) in {"known_absence_packet", "contradiction_candidate_packet"}:
        affordances.append("review_only")
    return [item for item in dict.fromkeys(affordances).keys() if item in V551J_FUTURE_TARGET_AFFORDANCES]


def _known_absence_claims() -> list[str]:
    return list(V551J_FORBIDDEN_CLAIM_IDS)


def _packet_row(
    *,
    run_id: str,
    packet_type: str,
    source_layer: str,
    source: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    atom_row: pd.Series | None,
    pattern_row: pd.Series | None,
    meaning_row: pd.Series | None,
    association_row: pd.Series | None,
    v552_row: pd.Series | None,
    join_strategy: str,
    join_status: str,
    join_warning: str,
    required_downstream_layer: str,
) -> dict[str, Any]:
    atom_row = atom_row if atom_row is not None else pd.Series(dtype=object)
    pattern_row = pattern_row if pattern_row is not None else pd.Series(dtype=object)
    meaning_row = meaning_row if meaning_row is not None else pd.Series(dtype=object)
    association_row = association_row if association_row is not None else pd.Series(dtype=object)
    v552_row = v552_row if v552_row is not None else pd.Series(dtype=object)
    authority_status, authority_basis = _classify_authority(atom_row if not atom_row.empty else association_row, join_strategy)
    directionality_status = _directionality_status(atom_row if not atom_row.empty else association_row)
    packet_status = "candidate"
    runtime_use_class = "not_runtime_consumable"
    input_atom_ids = [atom_row.get("atom_id")] if _clean(atom_row.get("atom_id")) else []
    input_pattern_ids = [_clean(pattern_row.get("pattern_id"))] if _clean(pattern_row.get("pattern_id")) else []
    input_meaning_summary_ids = [_clean(meaning_row.get("pattern_id"))] if _clean(meaning_row.get("pattern_id")) else []
    input_association_ids = [_clean(association_row.get("association_id"))] if _clean(association_row.get("association_id")) else []
    source_artifact_ids = [item for item in [f"{source_layer}:{source}:{wave}:{country_code}", _clean(pattern_row.get("source_row_hash")), _clean(atom_row.get("source_row_hash"))] if item]
    source_run_ids = [item for item in [_clean(atom_row.get("source_run_id")), _clean(pattern_row.get("source_run_id")), _clean(association_row.get("run_id"))] if item]
    family_ids = [item for item in [_clean(pattern_row.get("family_id")), _clean(association_row.get("family_id"))] if item]
    question_ids = [item for item in [_clean(atom_row.get("question_id")), _clean(pattern_row.get("question_id")), _clean(association_row.get("question_id"))] if item]
    variable_codes = [item for item in [_clean(atom_row.get("var_code")), _clean(pattern_row.get("var_code")), _clean(association_row.get("associated_var_code"))] if item]
    response_family = [item for item in [_clean(atom_row.get("response_family"))] if item]
    relation_axis_ids = [item for item in [_clean(atom_row.get("relation_axis_id")), _clean(pattern_row.get("relation_axis_id"))] if item]
    target_entity_ids = [item for item in [_clean(atom_row.get("target_entity_id")), _clean(pattern_row.get("target_entity_id"))] if item]
    driver_facet_ids = [item for item in [_clean(atom_row.get("driver_facet_id")), _clean(pattern_row.get("driver_facet_id"))] if item]
    strata_relevance = [item for item in [_clean(atom_row.get("strata_relevance")), _clean(pattern_row.get("strata_relevance"))] if item]
    strata_path = [item for item in [_clean(atom_row.get("strata_path")), _clean(pattern_row.get("strata_path"))] if item]
    semantic_roles = [item for item in [_clean(atom_row.get("semantic_role")), _clean(pattern_row.get("semantic_role"))] if item]
    semantic_tags = [item for item in [_clean(atom_row.get("semantic_tags")), _clean(pattern_row.get("semantic_tags"))] if item]
    support_n_unweighted = int(float(_first_nonempty(atom_row.get("n_unweighted"), pattern_row.get("pattern_support_n_unweighted"), association_row.get("association_support_n_unweighted"), 0) or 0))
    support_n_weighted = float(_first_nonempty(atom_row.get("n_weighted"), pattern_row.get("pattern_support_n_weighted"), association_row.get("association_support_n_weighted"), support_n_unweighted) or 0)
    support_score = _first_nonempty(atom_row.get("support_score"), pattern_row.get("support_score"), association_row.get("mutual_information"), 0)
    prevalence_score = _first_nonempty(atom_row.get("prevalence_score"), pattern_row.get("pattern_probability"), association_row.get("associated_response_baseline_share"), 0)
    support_status = _first_nonempty(
        atom_row.get("support_status"),
        pattern_row.get("pattern_support_status"),
        association_row.get("support_status"),
        association_row.get("association_support_gate_status"),
        association_row.get("association_publication_status"),
        "unknown",
    )
    support_gate_status = _first_nonempty(atom_row.get("support_gate_status"), pattern_row.get("pattern_support_gate_status"), association_row.get("association_support_gate_status"), "unknown")
    evidence_stratum = _first_nonempty(atom_row.get("evidence_stratum"), "reviewable")
    evidence_stratum_v2 = _first_nonempty(atom_row.get("evidence_stratum_v2"), "reviewable")
    pattern_support_n_unweighted = int(float(_first_nonempty(pattern_row.get("pattern_support_n_unweighted"), association_row.get("pattern_member_n_unweighted"), 0) or 0))
    pattern_support_status = _first_nonempty(pattern_row.get("pattern_support_status"), association_row.get("pattern_support_status"), "unknown")
    boundary_pattern_type = _first_nonempty(pattern_row.get("boundary_pattern_type"), meaning_row.get("boundary_pattern_type"), "")
    target_structure_status = _first_nonempty(pattern_row.get("target_structure_status"), meaning_row.get("target_structure_status"), "")
    target_selectivity_profile = _first_nonempty(pattern_row.get("target_selectivity_profile"), meaning_row.get("target_selectivity_profile"), "")
    meaning_summary_status = _first_nonempty(meaning_row.get("meaning_summary_status"), "not_supplied")
    meaning_summary_confidence = _first_nonempty(meaning_row.get("meaning_summary_confidence"), "unknown")
    meaning_summary_warning_flags_json = _json_array(json.loads(_clean(meaning_row.get("meaning_summary_warning_flags_json")) or "[]") if _clean(meaning_row.get("meaning_summary_warning_flags_json")) else [])
    association_context_status = _first_nonempty(association_row.get("association_context_status"), "not_supplied")
    association_publication_status = _first_nonempty(association_row.get("association_publication_status"), "not_supplied")
    association_lane = _first_nonempty(association_row.get("association_lane"), "unknown_association_lane")
    association_lane_status = _first_nonempty(association_row.get("association_lane_status"), "unknown")
    association_lane_authority_source = _first_nonempty(association_row.get("association_lane_authority_source"), "unknown")
    association_lane_publishability = _first_nonempty(association_row.get("association_lane_publishability"), "diagnostic_only_lane")
    top_publishable_attitude_associations_json = _clean(association_row.get("top_publishable_attitude_associations_json")) or "[]"
    top_reviewable_attitude_signals_json = _clean(association_row.get("top_reviewable_attitude_signals_json")) or "[]"
    top_identity_context_signals_json = _clean(association_row.get("top_identity_context_signals_json")) or "[]"
    top_position_context_signals_json = _clean(association_row.get("top_position_context_signals_json")) or "[]"
    top_family_background_signals_json = _clean(association_row.get("top_family_background_signals_json")) or "[]"
    top_unknown_or_diagnostic_signals_json = _clean(association_row.get("top_unknown_or_diagnostic_signals_json")) or "[]"
    v552_context_status = _first_nonempty(v552_row.get("v552_context_status"), "not_supplied")
    v552_question_semantic_hierarchy_join_status = _first_nonempty(v552_row.get("v552_question_semantic_hierarchy_join_status"), "not_supplied")
    v552_contradiction_context_status = _first_nonempty(v552_row.get("v552_contradiction_context_status"), "not_supplied")
    v552_parent_prior_context_status = _first_nonempty(v552_row.get("v552_parent_prior_context_status"), "not_supplied")
    v552_structural_refs_json = _clean(v552_row.get("v552_structural_refs_json")) or "[]"
    future_target_affordances = _future_affordances(pd.Series({
        "packet_type": packet_type,
        "boundary_pattern_type": boundary_pattern_type,
        "pattern_id": _clean(pattern_row.get("pattern_id")),
        "horizon_affordance": _first_nonempty(atom_row.get("horizon_affordance"), pattern_row.get("horizon_affordance"), meaning_row.get("horizon_affordance")),
        "family_ids_json": _json_array(family_ids),
        "semantic_tags_json": _json_array(semantic_tags),
        "top_identity_context_signals_json": top_identity_context_signals_json,
        "top_position_context_signals_json": top_position_context_signals_json,
        "top_family_background_signals_json": top_family_background_signals_json,
        "top_unknown_or_diagnostic_signals_json": top_unknown_or_diagnostic_signals_json,
        "v552_context_status": v552_context_status,
        "v552_horizon_constraint_refs_json": _clean(v552_row.get("v552_horizon_constraint_refs_json")),
        "strata_path_json": _json_array(strata_path),
        "directionality_status": directionality_status,
    }))
    forbidden_claim_ids = list(V551J_FORBIDDEN_CLAIM_IDS)
    review_required = not (packet_type == "joint_relation_evidence_packet" and join_strategy == "priority_a")
    diagnostic_only_reason = "context_only" if packet_type in {"joint_pattern_context_packet", "known_absence_packet", "contradiction_candidate_packet"} else ""
    blocked_reason = "" if packet_status == "candidate" else "blocked_by_validation"
    evidence_certification_status = "blocked" if packet_type in {"known_absence_packet", "contradiction_candidate_packet"} else "candidate"
    v552_handoff_readiness = "ready" if v552_context_status not in {"", "not_supplied"} else "not_ready_v552_context_missing"
    v552_handoff_blockers = [] if v552_handoff_readiness == "ready" else ["v552_context_missing"]
    return {
        "run_id": run_id,
        "packet_id": _stable_hash({
            "run_id": run_id,
            "packet_type": packet_type,
            "source": source,
            "wave": wave,
            "country_code": country_code,
            "atom_id": _clean(atom_row.get("atom_id")),
            "pattern_id": _clean(pattern_row.get("pattern_id")),
            "association_id": _clean(association_row.get("association_id")),
            "v552_key": _clean(v552_row.get("question_id")) or _clean(v552_row.get("relation_axis_id")),
            "family_ids_json": _json_array(family_ids),
            "question_ids_json": _json_array(question_ids),
            "variable_codes_json": _json_array(variable_codes),
            "source_artifact_ids_json": _json_array(source_artifact_ids),
            "source_run_ids_json": _json_array(source_run_ids),
            "packet_status": packet_status,
            "runtime_use_class": runtime_use_class,
        }),
        "packet_type": packet_type,
        "packet_status": packet_status,
        "source_layer": source_layer,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "created_at": utc_now(),
        "schema_version": "v0.1",
        "compiler_version": V551J_COMPILER_VERSION,
        "input_atom_ids_json": _json_array(input_atom_ids),
        "input_pattern_ids_json": _json_array(input_pattern_ids),
        "input_meaning_summary_ids_json": _json_array(input_meaning_summary_ids),
        "input_association_ids_json": _json_array(input_association_ids),
        "source_artifact_ids_json": _json_array(source_artifact_ids),
        "source_run_ids_json": _json_array(source_run_ids),
        "family_ids_json": _json_array(family_ids),
        "question_ids_json": _json_array(question_ids),
        "variable_codes_json": _json_array(variable_codes),
        "response_family_json": _json_array(response_family),
        "relation_axis_ids_json": _json_array(relation_axis_ids),
        "target_entity_ids_json": _json_array(target_entity_ids),
        "driver_facet_ids_json": _json_array(driver_facet_ids),
        "strata_relevance_json": _json_array(strata_relevance),
        "strata_path_json": _json_array(strata_path),
        "semantic_roles_json": _json_array(semantic_roles),
        "semantic_tags_json": _json_array(semantic_tags),
        "support_n_unweighted": support_n_unweighted,
        "support_n_weighted": support_n_weighted,
        "support_score": support_score,
        "prevalence_score": prevalence_score,
        "confidence_tier": _best_confidence_tier(
            atom_row.get("confidence_tier"),
            pattern_row.get("confidence_tier"),
            association_row.get("confidence_tier"),
        ),
        "support_status": support_status,
        "support_gate_status": support_gate_status,
        "evidence_stratum": evidence_stratum,
        "evidence_stratum_v2": evidence_stratum_v2,
        "authority_status": authority_status,
        "authority_basis": authority_basis,
        "authority_source_fields_json": _json_array([c for c in ["source", "wave", "canonical_wave", "country_code", "question_id", "var_code", "pattern_id"] if _clean(atom_row.get(c))]),
        "directionality_status": directionality_status,
        "directionality_basis": _first_nonempty(atom_row.get("directionality_policy"), atom_row.get("directionality_status"), "unknown"),
        "directionality_coverage_status": "covered" if directionality_status in {"known_directional", "partial_directionality"} else "not_applicable" if directionality_status == "not_applicable" else "unknown",
        "pattern_count": 1 if pattern_row is not None and not pattern_row.empty else 0,
        "pattern_support_n_unweighted": pattern_support_n_unweighted,
        "pattern_support_status": pattern_support_status,
        "boundary_pattern_type": boundary_pattern_type,
        "target_structure_status": target_structure_status,
        "target_selectivity_profile": target_selectivity_profile,
        "meaning_summary_status": meaning_summary_status,
        "meaning_summary_confidence": meaning_summary_confidence,
        "meaning_summary_warning_flags_json": meaning_summary_warning_flags_json,
        "association_context_status": association_context_status,
        "association_publication_status": association_publication_status,
        "association_lane": association_lane,
        "association_lane_status": association_lane_status,
        "association_lane_authority_source": association_lane_authority_source,
        "association_lane_publishability": association_lane_publishability,
        "top_publishable_attitude_associations_json": top_publishable_attitude_associations_json,
        "top_reviewable_attitude_signals_json": top_reviewable_attitude_signals_json,
        "top_identity_context_signals_json": top_identity_context_signals_json,
        "top_position_context_signals_json": top_position_context_signals_json,
        "top_family_background_signals_json": top_family_background_signals_json,
        "top_unknown_or_diagnostic_signals_json": top_unknown_or_diagnostic_signals_json,
        "runtime_use_class": "not_runtime_consumable",
        "future_target_affordances_json": _json_array(future_target_affordances),
        "allowed_future_targets_json": _json_array(["v552j", "v553", "v554", "v556"]),
        "forbidden_future_targets_json": _json_array(["person_runtime", "household_biography", "carrier_membership", "actor_orientation", "enneagram"]),
        "person_level_allowed": False,
        "household_level_allowed": False,
        "carrier_level_allowed": False,
        "structural_level_only": True,
        "temporal_level_allowed": False,
        "requires_temporalization": True,
        "requires_household_mediation": _to_bool("household_mediation_possible" in future_target_affordances, False),
        "requires_carrier_mediation": _to_bool("carrier_mediation_possible" in future_target_affordances, False),
        "requires_orientation_resolution": True,
        "requires_pressureflow_mediation": True,
        "requires_enneagram_runtime": False,
        "known_absences_json": _json_array([] if packet_type == "joint_relation_evidence_packet" else ["join_limitation", "runtime_boundary"]),
        "forbidden_claim_ids_json": _json_array(forbidden_claim_ids),
        "review_required": review_required,
        "diagnostic_only_reason": diagnostic_only_reason,
        "blocked_reason": blocked_reason,
        "v552_context_status": v552_context_status,
        "v552_question_semantic_hierarchy_join_status": v552_question_semantic_hierarchy_join_status,
        "v552_contradiction_context_status": v552_contradiction_context_status,
        "v552_parent_prior_context_status": v552_parent_prior_context_status,
        "v552_structural_refs_json": v552_structural_refs_json,
        "v551j_evidence_certification_status": evidence_certification_status,
        "v552_handoff_readiness": v552_handoff_readiness,
        "v552_handoff_blockers_json": _json_array(v552_handoff_blockers),
        "required_downstream_layer": required_downstream_layer,
        "join_strategy": join_strategy,
        "join_status": join_status,
        "join_warning": join_warning,
    }


def _join_diagnostics_row(
    *,
    run_id: str,
    table_name: str,
    path: str,
    frame: pd.DataFrame,
    required_columns: list[str],
    join_strategy: str,
    join_warning: str,
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
        "join_status": "ok" if not missing else "degraded",
        "join_warning": join_warning,
        "created_at": utc_now(),
        "schema_version": "v0.1",
    }


def build_v551j_join_key_diagnostics(
    *,
    run_id: str,
    inputs: dict[str, tuple[str, pd.DataFrame, list[str]]],
) -> pd.DataFrame:
    rows = [
        _join_diagnostics_row(run_id=run_id, table_name=name, path=path, frame=frame, required_columns=required_columns, join_strategy=_heuristic_join_strategy(frame), join_warning="" if frame.empty else "")
        for name, (path, frame, required_columns) in inputs.items()
    ]
    return pd.DataFrame(rows, columns=V551J_JOIN_KEY_DIAGNOSTICS_SCHEMA["required_columns"])


def _heuristic_join_strategy(frame: pd.DataFrame) -> str:
    cols = {column.lower() for column in frame.columns}
    if {"source", "wave", "canonical_wave", "country_code", "family_id", "pattern_id"}.issubset(cols):
        return "priority_a"
    if {"question_id", "var_code"}.intersection(cols):
        return "priority_b"
    if {"relation_axis_id", "target_entity_id", "driver_facet_id", "semantic_role", "semantic_tags"}.intersection(cols):
        return "priority_c"
    return "priority_d"


def build_v551j_candidate_trace(
    *,
    run_id: str,
    atoms: pd.DataFrame,
    pattern_index: pd.DataFrame,
    meaning_summary: pd.DataFrame,
    association_index: pd.DataFrame | None = None,
    review_surface: pd.DataFrame | None = None,
    v552_question_semantic_hierarchy: pd.DataFrame | None = None,
    v552_contradiction_surface: pd.DataFrame | None = None,
    v552_parent_prior_manifest: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if atoms.empty:
        packet_df = pd.DataFrame(columns=V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"])
        exclusion_df = pd.DataFrame(columns=V551J_PACKET_EXCLUSION_AUDIT_SCHEMA["required_columns"])
        forbidden_df = pd.DataFrame(columns=V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA["required_columns"])
        readiness_df = pd.DataFrame(columns=V551J_PACKET_READINESS_REPORT_SCHEMA["required_columns"])
        return packet_df, exclusion_df, forbidden_df, readiness_df

    matched_pattern_ids: set[str] = set()
    packet_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    forbidden_rows: list[dict[str, Any]] = []

    pattern_index = pattern_index.copy() if not pattern_index.empty else pd.DataFrame()
    meaning_summary = meaning_summary.copy() if not meaning_summary.empty else pd.DataFrame()
    association_index = association_index.copy() if association_index is not None and not association_index.empty else pd.DataFrame()
    review_surface = review_surface.copy() if review_surface is not None and not review_surface.empty else pd.DataFrame()
    v552_question_semantic_hierarchy = v552_question_semantic_hierarchy.copy() if v552_question_semantic_hierarchy is not None and not v552_question_semantic_hierarchy.empty else pd.DataFrame()
    v552_contradiction_surface = v552_contradiction_surface.copy() if v552_contradiction_surface is not None and not v552_contradiction_surface.empty else pd.DataFrame()
    v552_parent_prior_manifest = v552_parent_prior_manifest.copy() if v552_parent_prior_manifest is not None and not v552_parent_prior_manifest.empty else pd.DataFrame()

    for atom in atoms.itertuples(index=False):
        atom_row = pd.Series(atom._asdict())
        keys = [
            ("source", atom_row.get("source")),
            ("wave", atom_row.get("wave")),
            ("canonical_wave", atom_row.get("canonical_wave")),
            ("country_code", atom_row.get("country_code")),
        ]
        exact_pattern = _pick_join_row(pattern_index, keys + [("question_id", atom_row.get("question_id")), ("var_code", atom_row.get("var_code"))])
        join_strategy = "priority_a" if exact_pattern is not None else "priority_b" if not pattern_index.empty else "priority_d"
        if exact_pattern is None and not pattern_index.empty:
            exact_pattern = _pick_join_row(pattern_index, keys + [("var_code", atom_row.get("var_code"))])
        meaning_row = _pick_join_row(meaning_summary, keys + [("pattern_id", exact_pattern.get("pattern_id") if exact_pattern is not None else "")]) if not meaning_summary.empty else None
        association_row = _pick_join_row(association_index, keys + [("question_id", atom_row.get("question_id")), ("associated_var_code", atom_row.get("var_code"))]) if not association_index.empty else None
        v552_question_semantic_hierarchy_row = _pick_join_row(v552_question_semantic_hierarchy, keys + [("question_id", atom_row.get("question_id")), ("var_code", atom_row.get("var_code"))]) if not v552_question_semantic_hierarchy.empty else None
        contradiction_row = _pick_join_row(v552_contradiction_surface, keys + [("question_id", atom_row.get("question_id")), ("var_code", atom_row.get("var_code"))]) if not v552_contradiction_surface.empty else None
        parent_row = _pick_join_row(v552_parent_prior_manifest, keys + [("question_id", atom_row.get("question_id")), ("var_code", atom_row.get("var_code"))]) if not v552_parent_prior_manifest.empty else None
        v552_row = _v552_context_bundle(v552_question_semantic_hierarchy_row, contradiction_row, parent_row)
        packet_type = _packet_type_for_join(
            atom_joined=True,
            pattern_joined=exact_pattern is not None,
            association_joined=association_row is not None and _clean(association_row.get("association_publication_status")) == "publishable",
            v552_joined=not v552_row.empty and _clean(v552_row.get("v552_context_status")) == "joined",
        )
        join_status = "strict" if exact_pattern is not None else "context_only"
        join_warning = "" if exact_pattern is not None else "atom_pattern_strict_join_missing"
        if exact_pattern is not None and _clean(exact_pattern.get("pattern_id")):
            matched_pattern_ids.add(_clean(exact_pattern.get("pattern_id")))
        if exact_pattern is None and pattern_index.empty:
            packet_type = "known_absence_packet"
            exclusion_rows.append({
                "run_id": run_id,
                "candidate_source": "atom",
                "source": _clean(atom_row.get("source")),
                "wave": _clean(atom_row.get("wave")),
                "canonical_wave": _clean(atom_row.get("canonical_wave")),
                "country_code": _clean(atom_row.get("country_code")),
                "family_id": "",
                "pattern_id": "",
                "atom_id": _clean(atom_row.get("atom_id")),
                "question_id": _clean(atom_row.get("question_id")),
                "var_code": _clean(atom_row.get("var_code")),
                "exclusion_reason": "missing_required_input",
                "exclusion_stage": "pattern_index",
                "severity": "high",
                "would_have_packet_type": "joint_relation_evidence_packet",
                "required_downstream_layer": "v550j",
                "created_at": utc_now(),
                "schema_version": "v0.1",
            })
        elif exact_pattern is None:
            exclusion_rows.append({
                "run_id": run_id,
                "candidate_source": "atom",
                "source": _clean(atom_row.get("source")),
                "wave": _clean(atom_row.get("wave")),
                "canonical_wave": _clean(atom_row.get("canonical_wave")),
                "country_code": _clean(atom_row.get("country_code")),
                "family_id": "",
                "pattern_id": "",
                "atom_id": _clean(atom_row.get("atom_id")),
                "question_id": _clean(atom_row.get("question_id")),
                "var_code": _clean(atom_row.get("var_code")),
                "exclusion_reason": "weak_join_only",
                "exclusion_stage": "pattern_join",
                "severity": "medium",
                "would_have_packet_type": "joint_relation_evidence_packet",
                "required_downstream_layer": "v552j",
                "created_at": utc_now(),
                "schema_version": "v0.1",
            })
        packet_rows.append(
            _packet_row(
                run_id=run_id,
                packet_type=packet_type if exact_pattern is not None else ("joint_pattern_context_packet" if not pattern_index.empty else "known_absence_packet"),
                source_layer="v551j_candidate",
                source=_clean(atom_row.get("source")),
                wave=_clean(atom_row.get("wave")),
                canonical_wave=_clean(atom_row.get("canonical_wave")),
                country_code=_clean(atom_row.get("country_code")),
                atom_row=atom_row,
                pattern_row=exact_pattern,
                meaning_row=meaning_row,
                association_row=association_row,
                v552_row=v552_row,
                join_strategy=join_strategy,
                join_status=join_status,
                join_warning=join_warning,
                required_downstream_layer="v551j",
            )
        )

    if not pattern_index.empty and "pattern_id" in pattern_index.columns:
        for pattern in pattern_index.itertuples(index=False):
            pattern_row = pd.Series(pattern._asdict())
            pattern_id = _clean(pattern_row.get("pattern_id"))
            if pattern_id and pattern_id in matched_pattern_ids:
                continue
            meaning_row = _pick_join_row(meaning_summary, [("pattern_id", pattern_id)]) if not meaning_summary.empty else None
            association_row = _pick_join_row(association_index, [("pattern_id", pattern_id)]) if not association_index.empty else None
            packet_rows.append(
                _packet_row(
                    run_id=run_id,
                    packet_type="joint_pattern_context_packet" if association_row is None else "conditional_support_packet",
                    source_layer="v551j_pattern_context",
                    source=_clean(pattern_row.get("source")),
                    wave=_clean(pattern_row.get("wave")),
                    canonical_wave=_clean(pattern_row.get("canonical_wave")),
                    country_code=_clean(pattern_row.get("country_code")),
                    atom_row=None,
                    pattern_row=pattern_row,
                    meaning_row=meaning_row,
                    association_row=association_row,
                    v552_row=None,
                    join_strategy="priority_a",
                    join_status="pattern_context",
                    join_warning="pattern_not_joined_to_atom",
                    required_downstream_layer="v551j",
                )
            )
            exclusion_rows.append({
                "run_id": run_id,
                "candidate_source": "pattern",
                "source": _clean(pattern_row.get("source")),
                "wave": _clean(pattern_row.get("wave")),
                "canonical_wave": _clean(pattern_row.get("canonical_wave")),
                "country_code": _clean(pattern_row.get("country_code")),
                "family_id": _clean(pattern_row.get("family_id")),
                "pattern_id": pattern_id,
                "atom_id": "",
                "question_id": _clean(pattern_row.get("question_id")),
                "var_code": _clean(pattern_row.get("var_code")),
                "exclusion_reason": "review_surface_not_certified" if association_row is not None else "missing_join_key",
                "exclusion_stage": "pattern_context",
                "severity": "low" if association_row is not None else "medium",
                "would_have_packet_type": "joint_pattern_context_packet",
                "required_downstream_layer": "v552j",
                "created_at": utc_now(),
                "schema_version": "v0.1",
            })

    if not association_index.empty:
        for assoc in association_index.itertuples(index=False):
            assoc_row = pd.Series(assoc._asdict())
            pattern_anchor_row = None
            assoc_pattern_id = _clean(assoc_row.get("pattern_id"))
            if assoc_pattern_id and not pattern_index.empty and "pattern_id" in pattern_index.columns:
                pattern_anchor_row = _pick_join_row(pattern_index, [("pattern_id", assoc_pattern_id)])
            if pattern_anchor_row is None and assoc_pattern_id:
                pattern_anchor_row = assoc_row
            if _clean(assoc_row.get("association_publication_status")) != "publishable":
                exclusion_rows.append({
                    "run_id": run_id,
                    "candidate_source": "association",
                    "source": _clean(assoc_row.get("source")),
                    "wave": _clean(assoc_row.get("wave")),
                    "canonical_wave": _clean(assoc_row.get("canonical_wave")),
                    "country_code": _clean(assoc_row.get("country_code")),
                    "family_id": _clean(assoc_row.get("family_id")),
                    "pattern_id": _clean(assoc_row.get("pattern_id")),
                    "atom_id": "",
                    "question_id": _clean(assoc_row.get("question_id")),
                    "var_code": _clean(assoc_row.get("associated_var_code")) or _clean(assoc_row.get("var_code")),
                    "exclusion_reason": "association_not_publishable",
                    "exclusion_stage": "association_context",
                    "severity": "medium",
                    "would_have_packet_type": "conditional_support_packet",
                    "required_downstream_layer": "v551j",
                    "created_at": utc_now(),
                    "schema_version": "v0.1",
                })
                continue
            packet_rows.append(
                _packet_row(
                    run_id=run_id,
                    packet_type="conditional_support_packet",
                    source_layer="v551j_association_context",
                    source=_clean(assoc_row.get("source")),
                    wave=_clean(assoc_row.get("wave")),
                    canonical_wave=_clean(assoc_row.get("canonical_wave")),
                    country_code=_clean(assoc_row.get("country_code")),
                    atom_row=None,
                    pattern_row=pattern_anchor_row,
                    meaning_row=None,
                    association_row=assoc_row,
                    v552_row=None,
                    join_strategy="priority_a" if pattern_anchor_row is not None else "priority_b",
                    join_status="association_context_anchored" if pattern_anchor_row is not None else "association_context",
                    join_warning="" if pattern_anchor_row is not None else "association_context_only",
                    required_downstream_layer="v551j",
                )
            )

    if not v552_contradiction_surface.empty:
        for row in v552_contradiction_surface.itertuples(index=False):
            v552_row = pd.Series(row._asdict())
            packet_rows.append(
                _packet_row(
                    run_id=run_id,
                    packet_type="contradiction_candidate_packet",
                    source_layer="v551j_v552_context",
                    source=_clean(v552_row.get("source")),
                    wave=_clean(v552_row.get("wave")),
                    canonical_wave=_clean(v552_row.get("canonical_wave")),
                    country_code=_clean(v552_row.get("country_code")),
                    atom_row=None,
                    pattern_row=None,
                    meaning_row=None,
                    association_row=None,
                    v552_row=v552_row,
                    join_strategy="priority_c",
                    join_status="v552_context",
                    join_warning="contradiction_context_only",
                    required_downstream_layer="v551j",
                )
            )

    packet_df = pd.DataFrame(packet_rows, columns=V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"] + ["join_strategy", "join_status", "join_warning", "required_downstream_layer"])
    if not packet_df.empty:
        packet_df = packet_df.drop(columns=[column for column in ["join_strategy", "join_status", "join_warning", "required_downstream_layer"] if column in packet_df.columns])
        packet_df = packet_df.reindex(columns=V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"])
        packet_df = packet_df.fillna("")
        packet_df = packet_df.reset_index(drop=True)
        packet_df["packet_id"] = [f"{run_id}__packet_{index + 1:07d}" for index in range(len(packet_df))]
    exclusion_df = pd.DataFrame(exclusion_rows, columns=V551J_PACKET_EXCLUSION_AUDIT_SCHEMA["required_columns"])
    forbidden_rows.extend(_forbidden_inference_rows(packet_df))
    forbidden_df = pd.DataFrame(forbidden_rows, columns=V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA["required_columns"])
    readiness_df = build_v551j_readiness_report(run_id=run_id, packet_df=packet_df, exclusion_df=exclusion_df, forbidden_df=forbidden_df)
    return packet_df, exclusion_df, forbidden_df, readiness_df


def _forbidden_inference_rows(packet_df: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if packet_df.empty:
        return rows
    risk_map = {
        "do_not_render_as_person_belief": ("Packet evidence is not a person belief.", "Carry forward as candidate context only."),
        "do_not_render_as_parent_trait": ("Packet evidence is not a parent trait.", "Keep parent modeling for later layers."),
        "do_not_render_as_child_memory": ("Packet evidence is not a child memory.", "Do not convert into persona memory."),
        "do_not_render_as_causal_relation": ("Packet evidence is not causality.", "Keep relation evidence structural."),
        "do_not_render_as_enneagram_type": ("Packet evidence is not an Enneagram type.", "Leave Enneagram for downstream work."),
        "do_not_render_as_household_biography": ("Packet evidence is not a household biography.", "Keep household mediation separate."),
        "do_not_render_as_countrywide_personality": ("Packet evidence is not a country-level personality.", "Keep evidence at the joint layer."),
        "do_not_render_as_carrier_membership": ("Packet evidence is not carrier membership.", "Do not infer carrier identity."),
        "do_not_render_as_actor_orientation": ("Packet evidence is not actor orientation.", "Do not infer runtime actor orientation."),
        "do_not_render_as_temporal_field": ("Packet evidence is not a temporal field.", "Temporalization is reserved for later layers."),
        "do_not_render_as_runtime_psyche": ("Packet evidence is not runtime psyche.", "Keep runtime psyche out of V551J."),
    }
    for row in packet_df.itertuples(index=False):
        first = pd.Series(row._asdict())
        for claim_id in V551J_FORBIDDEN_CLAIM_IDS:
            risk_description, safe_alternative = risk_map[claim_id]
            rows.append(
                {
                    "run_id": _clean(first.get("run_id")),
                    "packet_id": _clean(first.get("packet_id")),
                    "packet_type": _clean(first.get("packet_type")),
                    "forbidden_claim_id": claim_id,
                    "risk_description": risk_description,
                    "upstream_basis": _clean(first.get("source_artifact_ids_json")) or _clean(first.get("input_atom_ids_json")),
                    "safe_alternative": safe_alternative,
                    "applies_to_future_layer": True,
                    "severity": "medium" if claim_id in {"do_not_render_as_actor_orientation", "do_not_render_as_runtime_psyche", "do_not_render_as_enneagram_type"} else "low",
                    "created_at": utc_now(),
                    "schema_version": "v0.1",
                }
            )
    return rows


def build_v551j_readiness_report(
    *,
    run_id: str,
    packet_df: pd.DataFrame,
    exclusion_df: pd.DataFrame,
    forbidden_df: pd.DataFrame,
    join_diag_rows: int = 0,
) -> pd.DataFrame:
    packet_type_counts = dict(Counter(packet_df["packet_type"].astype(str))) if not packet_df.empty and "packet_type" in packet_df.columns else {}
    packet_status_counts = dict(Counter(packet_df["packet_status"].astype(str))) if not packet_df.empty and "packet_status" in packet_df.columns else {}
    runtime_use_class_counts = dict(Counter(packet_df["runtime_use_class"].astype(str))) if not packet_df.empty and "runtime_use_class" in packet_df.columns else {}
    authority_status_counts = dict(Counter(packet_df["authority_status"].astype(str))) if not packet_df.empty and "authority_status" in packet_df.columns else {}
    directionality_status_counts = dict(Counter(packet_df["directionality_status"].astype(str))) if not packet_df.empty and "directionality_status" in packet_df.columns else {}
    future_target_affordance_counts = dict(Counter(val for cell in packet_df.get("future_target_affordances_json", pd.Series(dtype=str)).astype(str).tolist() for val in json.loads(cell) if cell)) if not packet_df.empty and "future_target_affordances_json" in packet_df.columns else {}
    known_absence_counts = dict(Counter(val for cell in packet_df.get("known_absences_json", pd.Series(dtype=str)).astype(str).tolist() for val in json.loads(cell) if cell)) if not packet_df.empty and "known_absences_json" in packet_df.columns else {}
    row = {
        "run_id": run_id,
        "candidate_packet_rows": int(len(packet_df)),
        "exclusion_audit_rows": int(len(exclusion_df)),
        "forbidden_inference_audit_rows": int(len(forbidden_df)),
        "join_diagnostic_rows": int(join_diag_rows),
        "packet_type_counts": json.dumps(packet_type_counts, sort_keys=True),
        "packet_status_counts": json.dumps(packet_status_counts, sort_keys=True),
        "runtime_use_class_counts": json.dumps(runtime_use_class_counts, sort_keys=True),
        "authority_status_counts": json.dumps(authority_status_counts, sort_keys=True),
        "directionality_status_counts": json.dumps(directionality_status_counts, sort_keys=True),
        "future_target_affordance_counts": json.dumps(future_target_affordance_counts, sort_keys=True),
        "person_level_allowed_count": int(packet_df["person_level_allowed"].astype(bool).sum()) if not packet_df.empty and "person_level_allowed" in packet_df.columns else 0,
        "household_level_allowed_count": int(packet_df["household_level_allowed"].astype(bool).sum()) if not packet_df.empty and "household_level_allowed" in packet_df.columns else 0,
        "carrier_level_allowed_count": int(packet_df["carrier_level_allowed"].astype(bool).sum()) if not packet_df.empty and "carrier_level_allowed" in packet_df.columns else 0,
        "structural_level_only_count": int(packet_df["structural_level_only"].astype(bool).sum()) if not packet_df.empty and "structural_level_only" in packet_df.columns else 0,
        "requires_temporalization_count": int(packet_df["requires_temporalization"].astype(bool).sum()) if not packet_df.empty and "requires_temporalization" in packet_df.columns else 0,
        "requires_household_mediation_count": int(packet_df["requires_household_mediation"].astype(bool).sum()) if not packet_df.empty and "requires_household_mediation" in packet_df.columns else 0,
        "requires_carrier_mediation_count": int(packet_df["requires_carrier_mediation"].astype(bool).sum()) if not packet_df.empty and "requires_carrier_mediation" in packet_df.columns else 0,
        "requires_orientation_resolution_count": int(packet_df["requires_orientation_resolution"].astype(bool).sum()) if not packet_df.empty and "requires_orientation_resolution" in packet_df.columns else 0,
        "requires_pressureflow_mediation_count": int(packet_df["requires_pressureflow_mediation"].astype(bool).sum()) if not packet_df.empty and "requires_pressureflow_mediation" in packet_df.columns else 0,
        "requires_enneagram_runtime_count": int(packet_df["requires_enneagram_runtime"].astype(bool).sum()) if not packet_df.empty and "requires_enneagram_runtime" in packet_df.columns else 0,
        "v552_context_status": (
            _first_nonempty(*packet_df["v552_context_status"].astype(str).tolist())
            if not packet_df.empty and "v552_context_status" in packet_df.columns
            else "not_supplied"
        ),
        "known_absence_counts": json.dumps(known_absence_counts, sort_keys=True),
        "readiness_warnings": json.dumps([]),
        "certified_packet_index_written": False,
        "runtime_safe_packets_written": False,
        "final_status": "READY_CANDIDATE_TRACE_ONLY" if len(packet_df) > 0 else "NOT_READY_NO_CANDIDATE_ROWS",
        "created_at": utc_now(),
        "schema_version": "v0.1",
    }
    return pd.DataFrame([row], columns=V551J_PACKET_READINESS_REPORT_SCHEMA["required_columns"])


def validate_v551j_candidate_trace(df: pd.DataFrame) -> list[str]:
    return validate_candidate_trace_schema(df)


# ---- V551J joint evidence contract v2 -------------------------------------------------

V2_CERTIFIED_AUTHORITY_TOKENS = {
    "certified", "CERTIFIED", "high", "very high", "validated", "authorized", "resolved",
    "allowed", "true", "True", "PASS", "pass", "family_registry_fallback_authorized",
    "family_registry_resolved_condition", "family_registry_resolved_group", "registry_resolved",
    "present", "sufficient_support", "manually_authorized_directionality",
    "manual_authorized_directionality", "authorized_directionality",
}

V2_CONTEXT_ITEM_ROLES = {
    "context", "position_context", "condition", "conditioning", "metadata", "administrative",
    "nonrelation", "non_relation", "context_component",
}

V551J_STANCE_TO_DIRECTION = {
    "support": "positive",
    "oppose": "negative",
    "neutral": "neutral",
}


def _stance_alignment_status(stance: Any, direction: Any) -> str:
    s = _clean(stance).lower()
    d = _clean(direction).lower()
    if not s or not d:
        return "ONE_SIDE_MISSING"
    expected = V551J_STANCE_TO_DIRECTION.get(s)
    if expected is None:
        return "UNKNOWN_STANCE_TOKEN"
    return "EXACT_GOVERNED_ALIGNMENT" if expected == d else "CONFLICT"


def _evidence_role_status(role: Any) -> str:
    r = _clean(role).upper()
    if not r:
        return "MISSING_EVIDENCE_ROLE"
    if r in {"RELATION_EVIDENCE", "RELATION_EVIDENCE_ATOM"}:
        return "VALID_RELATION_EVIDENCE_ROLE"
    if "CONTEXT" in r:
        return "VALID_CONTEXT_EVIDENCE_ROLE"
    return "UNKNOWN_EVIDENCE_ROLE"


def _v2_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def _v2_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, float) and pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("[") or text.startswith("{"):
            try:
                parsed = json.loads(text)
                return parsed if isinstance(parsed, list) else [parsed]
            except Exception:
                pass
        return [part.strip() for part in text.replace(",", "|").split("|") if part.strip()]
    return [value]


def _v2_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float):
        if pd.isna(value):
            return None
        return float(f"{value:.12g}")
    if isinstance(value, (int, bool)):
        return value
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text if text != "" else None


def _v2_hash(namespace: str, payload: dict[str, Any]) -> str:
    normalized = {"namespace": namespace, **payload}
    return hashlib.sha256(_v2_json(normalized).encode("utf-8")).hexdigest()


def _v2_hash_file(path: str | Path | None) -> str:
    if not path:
        return "not_supplied"
    p = Path(path)
    if not p.exists():
        return "missing"
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _v2_packet_id(pattern: Mapping[str, Any]) -> str:
    return recompute_v551j_packet_id(pattern)


def _v2_component_id(packet: Mapping[str, Any], item: Mapping[str, Any]) -> str:
    return recompute_v551j_component_id({**dict(packet), **dict(item)})


def _v2_bool_certified(value: Any) -> bool:
    text = _clean(value)
    return text in V2_CERTIFIED_AUTHORITY_TOKENS or text.lower() in V2_CERTIFIED_AUTHORITY_TOKENS


def _v2_pattern_measurements(pattern: Mapping[str, Any]) -> dict[str, Any]:
    mapping = {
        "joint_pattern_count_unweighted": "pattern_count_unweighted",
        "joint_pattern_count_weighted": "pattern_count_weighted",
        "joint_probability_unweighted": "pattern_probability_unweighted",
        "joint_probability_weighted": "pattern_probability_weighted",
        "joint_probability_basis": "pattern_probability_basis",
        "joint_probability": "pattern_probability",
        "joint_n_unweighted": "n_unweighted",
        "joint_n_weighted": "n_weighted",
        "joint_weighted_count_basis": "weighted_count_basis",
        "joint_support_threshold": "support_threshold",
        "joint_support_ratio": "support_ratio",
        "joint_support_ratio_margin": "support_ratio_margin",
        "joint_support_score": "support_score",
        "joint_support_status": "support_status",
        "joint_support_gate_status": "support_gate_status",
        "joint_prevalence_score": "prevalence_score",
        "joint_completion_rate": "completion_rate",
        "joint_missingness_rate": "missingness_rate",
        "joint_effective_n": "effective_n",
        "joint_effective_n_ratio": "effective_n_ratio",
        "joint_confidence_score": "confidence_score",
        "joint_weight_status": "weight_status",
    }
    out = {left: pattern.get(right) for left, right in mapping.items()}
    missing_required = [field for field in ["joint_pattern_count_unweighted", "joint_support_score", "joint_support_status", "joint_support_gate_status"] if _v2_scalar(out.get(field)) is None]
    out["joint_measurement_status"] = "COMPLETE_PATTERN_MEASUREMENT_CONTRACT" if not missing_required else "REVIEW_REQUIRED_PATTERN_MEASUREMENT_GAP"
    return out


def _v2_equal(a: Any, b: Any) -> str:
    av, bv = _v2_scalar(a), _v2_scalar(b)
    if av is None and bv is None:
        return "gap"
    if av is None or bv is None:
        return "gap"
    return "consistent" if str(av).casefold() == str(bv).casefold() else "conflict"


def _v221_status(a: Any, b: Any) -> str:
    av, bv = _v2_scalar(a), _v2_scalar(b)
    if av is None and bv is None:
        return "BOTH_MISSING"
    if av is None or bv is None:
        return "ONE_SIDE_MISSING"
    return "EXACT_MATCH" if str(av).casefold() == str(bv).casefold() else "CONFLICT"


def _v221_old_status(status: str) -> str:
    return {"consistent": "EXACT_MATCH", "conflict": "CONFLICT", "gap": "ONE_SIDE_MISSING"}.get(status, "ONE_SIDE_MISSING")


def _v2_identity(value: Any) -> str:
    return _clean(value).casefold()


def _v2_match_atoms_for_item(item: Mapping[str, Any], atoms: pd.DataFrame, pattern: Mapping[str, Any]) -> tuple[str, str, pd.DataFrame, list[str]]:
    scope = atoms[
        atoms.get("source_family", pd.Series(dtype=str)).fillna("").astype(str).eq(_clean(pattern.get("source_family")) or _clean(pattern.get("source")))
        & atoms.get("canonical_wave", pd.Series(dtype=str)).fillna("").astype(str).eq(_clean(pattern.get("canonical_wave")) or _clean(pattern.get("wave")))
        & atoms.get("country_code", pd.Series(dtype=str)).fillna("").astype(str).eq(_clean(pattern.get("country_code")))
    ].copy()
    q = _v2_identity(item.get("question_id"))
    v = _v2_identity(item.get("var_code"))
    reasons: list[str] = []
    if q and v:
        candidates = scope[
            scope.get("question_id", pd.Series(dtype=str)).fillna("").astype(str).str.casefold().eq(q)
            & scope.get("var_code", pd.Series(dtype=str)).fillna("").astype(str).str.casefold().eq(v)
        ]
        basis = "exact_question_id_and_var_code"
    elif q:
        candidates = scope[scope.get("question_id", pd.Series(dtype=str)).fillna("").astype(str).str.casefold().eq(q)]
        basis = "exact_question_id"
    elif v:
        candidates = scope[scope.get("var_code", pd.Series(dtype=str)).fillna("").astype(str).str.casefold().eq(v)]
        basis = "exact_var_code"
    else:
        candidates = scope.iloc[0:0].copy()
        basis = "missing_question_and_var_identity"
    response = _v2_scalar(item.get("response_value_normalized"))
    if response is not None and not candidates.empty and "response_value_normalized" in candidates.columns:
        candidates = candidates[candidates["response_value_normalized"].map(_v2_scalar).astype(str).eq(str(response))]
        basis += "+exact_response_value_normalized"
    elif not candidates.empty and _clean(item.get("normalized_response_label")) and "normalized_response_label" in candidates.columns:
        label_matches = candidates[candidates["normalized_response_label"].fillna("").astype(str).eq(_clean(item.get("normalized_response_label")))]
        if not label_matches.empty and label_matches.get("response_semantics_contract_hash", pd.Series(dtype=str)).fillna("").astype(str).nunique() == 1 and label_matches.get("semantic_response_role", pd.Series(dtype=str)).fillna("").astype(str).nunique() == 1:
            candidates = label_matches
            basis += "+unique_normalized_response_label"
    if candidates.empty:
        role = (_clean(item.get("v551_evidence_role")) or _clean(item.get("item_role")) or _clean(item.get("semantic_role"))).lower()
        if _clean(item.get("response_value_normalized")).lower() in {"", "nan", "none", "missing"} or _clean(item.get("semantic_response_role")).lower() in {"missing", "special", "nonresponse"}:
            return "UNMATCHED_SPECIAL_OR_MISSING_RESPONSE", basis, candidates, ["special_or_missing_response"]
        if role in V2_CONTEXT_ITEM_ROLES or "context" in role or "nonrelation" in role:
            return "UNMATCHED_V551_RELATION_INELIGIBLE", basis, candidates, ["governed_context_or_nonrelation_item"]
        return "MISSING_V551_ATOM_UNEXPLAINED", basis, candidates, ["no_exact_v551_atom"]
    if "atom_contract_hash" in candidates.columns:
        unique_hashes = sorted(set(candidates["atom_contract_hash"].fillna("").astype(str)))
        unique_hashes = [h for h in unique_hashes if h]
        if len(unique_hashes) > 1:
            return "AMBIGUOUS_V551_ATOM_MATCH", basis, candidates, ["multiple_distinct_atom_contract_hashes"]
        if len(candidates) > 1:
            return "MATCHED_EQUIVALENT_DUPLICATE_V551_ATOM", basis + "+deduplicated_atom_contract_hash", candidates.iloc[[0]].copy(), ["equivalent_duplicate_atoms"]
    return "MATCHED_EXACT_V551_ATOM", basis, candidates.iloc[[0]].copy(), reasons


def _v2_component_row(run_id: str, pattern: Mapping[str, Any], item: Mapping[str, Any], atom_match: pd.DataFrame, match_status: str, match_basis: str, reasons: list[str]) -> dict[str, Any]:
    packet_id = _v2_packet_id(pattern)
    component_id = _v2_component_id(pattern, item)
    atom = atom_match.iloc[0].to_dict() if not atom_match.empty else {}
    comparisons = {
        "question_id_consistent": _v2_equal(item.get("question_id"), atom.get("question_id")),
        "var_code_consistent": _v2_equal(item.get("var_code"), atom.get("var_code")),
        "response_identity_consistent": _v2_equal(item.get("response_value_normalized"), atom.get("response_value_normalized")),
        "normalized_response_label_consistent": _v2_equal(item.get("normalized_response_label"), atom.get("normalized_response_label")),
        "semantic_role_consistent": "parallel",
        "directionality_consistent": _v2_equal(item.get("response_direction"), atom.get("response_direction")),
        "intensity_consistent": _v2_equal(item.get("response_intensity"), atom.get("response_intensity")),
        "semantic_polarity_consistent": _v2_equal(item.get("polarity"), atom.get("response_direction")),
        "driver_id_consistent": _v2_equal(item.get("driver_id"), atom.get("driver_id")),
        "relation_axis_consistent": _v2_equal(item.get("relation_axis_id"), atom.get("relation_axis_id")),
        "target_entity_consistent": "parallel",
        "driver_facet_consistent": _v2_equal(item.get("driver_facet_id"), atom.get("driver_facet_id")),
    }
    structural_consistent = "consistent" if _v2_scalar(atom.get("structural_identity_signature")) is not None else "gap"
    authority_hash_consistent = _v2_equal(item.get("response_semantics_contract_hash"), atom.get("response_semantics_contract_hash"))
    stance_alignment = _stance_alignment_status(item.get("semantic_response_role"), atom.get("response_direction"))
    evidence_role_status = _evidence_role_status(atom.get("semantic_role") or atom.get("v551_evidence_role"))
    reason_codes = list(reasons)
    conflict_status = "CROSS_CONTRACT_CONSISTENT"
    if authority_hash_consistent == "conflict":
        conflict_status = "CROSS_CONTRACT_AUTHORITY_HASH_CONFLICT"
    elif comparisons["response_identity_consistent"] == "conflict":
        conflict_status = "CROSS_CONTRACT_RESPONSE_CONFLICT"
    elif comparisons["directionality_consistent"] == "conflict":
        conflict_status = "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT"
    elif comparisons["intensity_consistent"] == "conflict":
        conflict_status = "CROSS_CONTRACT_SOURCE_INTENSITY_CONFLICT"
    elif comparisons["semantic_polarity_consistent"] == "conflict":
        conflict_status = "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT"
    elif any(comparisons[k] == "conflict" for k in ["relation_axis_consistent", "driver_facet_consistent"]):
        conflict_status = "CROSS_CONTRACT_SHARED_STRUCTURAL_CONFLICT"
    elif structural_consistent == "gap" or authority_hash_consistent == "gap":
        conflict_status = "CROSS_CONTRACT_GAP"
    if conflict_status != "CROSS_CONTRACT_CONSISTENT":
        reason_codes.append(conflict_status.lower())
    item_role = (_clean(item.get("v551_evidence_role")) or _clean(item.get("item_role")) or _clean(item.get("semantic_role"))).lower()
    matched = match_status.startswith("MATCHED")
    relation_like = matched and item_role not in V2_CONTEXT_ITEM_ROLES and "context" not in item_role and "nonrelation" not in item_role and _clean(atom.get("allowed_as_v551_relation_evidence")).lower() not in {"false", "0", "no"}
    if relation_like:
        contribution = "relation_component"
    elif match_status in {"UNMATCHED_SPECIAL_OR_MISSING_RESPONSE"}:
        contribution = "special_or_missing_component"
    elif match_status in {"UNMATCHED_V551_RELATION_INELIGIBLE"}:
        contribution = "explained_nonrelation_component"
    elif matched:
        contribution = "context_component"
    elif match_status == "AMBIGUOUS_V551_ATOM_MATCH":
        contribution = "blocked_component"
    else:
        contribution = "unresolved_component"
    row = {
        "run_id": run_id, "packet_id": packet_id, "pattern_id": _clean(pattern.get("pattern_id")), "family_id": _clean(pattern.get("family_id")),
        "item_order": item.get("item_order"), "component_id": component_id, "component_contract_hash": "",
        "source": _clean(pattern.get("source")), "source_family": _clean(pattern.get("source_family")) or _clean(pattern.get("source")),
        "canonical_wave": _clean(pattern.get("canonical_wave")) or _clean(pattern.get("wave")), "country_code": _clean(pattern.get("country_code")),
        "v550j_item_var_code": _clean(item.get("var_code")), "v550j_item_question_id": _clean(item.get("question_id")),
        "v551_var_code": _clean(atom.get("var_code")), "v551_question_id": _clean(atom.get("question_id")), "v550j_item_role": _clean(item.get("item_role")),
        "v550j_item_condition_label": _clean(item.get("condition_label")), "v550j_item_response_value_normalized": item.get("response_value_normalized"),
        "v550j_item_response_label": _clean(item.get("response_label")), "v550j_item_normalized_response_label": _clean(item.get("normalized_response_label")),
        "v550j_item_response_direction": _clean(item.get("response_direction")), "v550j_item_response_intensity": item.get("response_intensity"),
        "v550j_item_polarity": _clean(item.get("polarity")), "v550j_semantic_polarity_label": _clean(item.get("polarity")),
        "v551_source_polarity_coordinate": _clean(atom.get("polarity")), "v550j_item_directionality_authority_status": _clean(item.get("directionality_status")),
        "v550j_item_directionality_authority_source": _clean(item.get("directionality_authority_source")),
        "v550j_item_response_semantics_authority_status": _clean(item.get("response_semantics_status")),
        "v550j_item_response_semantics_contract_hash": _clean(item.get("response_semantics_contract_hash")),
        "v550j_item_semantic_response_role": _clean(item.get("semantic_response_role")),
        "v550j_joint_response_stance": _clean(item.get("semantic_response_role")),
        "v551_evidence_role": _clean(atom.get("semantic_role") or atom.get("v551_evidence_role")),
        "v551_evidence_role_status": evidence_role_status,
        "joint_response_stance_alignment_status": stance_alignment,
        "v550j_item_semantic_role_authority_status": _clean(item.get("semantic_response_role_status")),
        "v550j_driver_id": _clean(item.get("driver_id")), "v550j_driver_facet_id": _clean(item.get("driver_facet_id")),
        "v550j_relation_axis_id": _clean(item.get("relation_axis_id")), "v550j_family_target_entity_id": _clean(item.get("target_entity_id")),
        "v550j_target_domain": _clean(item.get("target_domain")), "v550j_target_condition_label": _clean(item.get("target_condition_label")),
        "v550j_target_group_label": _clean(item.get("target_group_label")), "v550j_permission_domain": _clean(item.get("permission_domain")),
        "v550j_target_resolution_grain": _clean(item.get("target_resolution_grain")), "v550j_target_resolution_status": _clean(item.get("target_resolution_status")),
        "v550j_target_resolution_authority_source": _clean(item.get("target_resolution_authority_source")),
        "v550j_item_mapping_status": _clean(item.get("mapping_status")), "v550j_item_semantic_role": _clean(item.get("semantic_role")),
        "v550j_item_v551_evidence_role": _clean(item.get("v551_evidence_role")), "v551_atom_match_status": match_status, "v551_atom_match_basis": match_basis,
        "v551_atom_id": _clean(atom.get("atom_id")), "v551_atom_contract_hash": _clean(atom.get("atom_contract_hash")),
        "v551_empirical_object_type": _clean(atom.get("empirical_object_type")), "v551_empirical_object_id": _clean(atom.get("empirical_object_id")),
        "v551_empirical_distribution_id": _clean(atom.get("empirical_distribution_id")),
        "v551_response_value_normalized": atom.get("response_value_normalized"), "v551_normalized_response_label": _clean(atom.get("normalized_response_label")),
        "v551_semantic_response_role": _clean(atom.get("semantic_response_role") or atom.get("semantic_role")),
        "v551_response_semantics_contract_hash": _clean(atom.get("response_semantics_contract_hash")),
        "v551_response_direction": _clean(atom.get("response_direction")), "v551_response_direction_status": _clean(atom.get("response_direction_status")),
        "v551_response_intensity": atom.get("response_intensity"), "v551_response_intensity_status": _clean(atom.get("response_intensity_status")),
        "v551_polarity": _clean(atom.get("polarity")), "v551_response_scale_signature": _clean(atom.get("response_scale_signature")),
        "v551_semantic_identity_signature": _clean(atom.get("semantic_identity_signature")), "v551_structural_identity_signature": _clean(atom.get("structural_identity_signature")),
        "v551_measurement_contract_hash": _clean(atom.get("measurement_contract_hash")),
        "v551_response_value_raw": atom.get("response_value_raw"), "v551_response_label": _clean(atom.get("response_label")), "v551_response_family": _clean(atom.get("response_family")),
        "v551_observed_response_zero": bool(atom.get("observed_response_zero", False)) if atom else False, "v551_ordinal_rank": atom.get("ordinal_rank"), "v551_scale_min": atom.get("scale_min"), "v551_scale_max": atom.get("scale_max"), "v551_scale_direction": _clean(atom.get("scale_direction")), "v551_directionality_policy": _clean(atom.get("directionality_policy")), "v551_response_topology": _clean(atom.get("response_topology")),
        "v551_n_unweighted": atom.get("n_unweighted"), "v551_n_respondents": atom.get("n_respondents"), "v551_n_weighted": atom.get("n_weighted"), "v551_pct_unweighted": atom.get("pct_unweighted"), "v551_pct_weighted": atom.get("pct_weighted"), "v551_population_share": atom.get("population_share"), "v551_weight_status": _clean(atom.get("weight_status")), "v551_support_score": atom.get("support_score"), "v551_prevalence_score": atom.get("prevalence_score"),
        "v551_driver_id": _clean(atom.get("driver_id")), "v551_driver_facet_id": _clean(atom.get("driver_facet_id")), "v551_relation_axis_id": _clean(atom.get("relation_axis_id")), "v551_structural_target_entity_id": _clean(atom.get("target_entity_id")), "v551_strata_path": _clean(atom.get("strata_path")), "v551_subject_position_signature": _clean(atom.get("subject_position_signature")),
        "v551_structural_mapping_status": _clean(atom.get("structural_mapping_status")), "v551_semantic_role_authority_status": _clean(atom.get("semantic_role_authority_status")), "v551_response_semantics_authority_status": _clean(atom.get("response_semantics_authority_status")), "v551_directionality_authority_status": _clean(atom.get("directionality_authority_status")), "v551_directional_certification_status": _clean(atom.get("directional_certification_status")),
        "v551_allowed_as_v551_relation_evidence": bool(atom.get("allowed_as_v551_relation_evidence", False)) if atom else False, "v551_allowed_as_temporal_pressure_indicator": bool(atom.get("allowed_as_temporal_pressure_indicator", False)) if atom else False, "v551_temporal_authority_status": _clean(atom.get("temporal_authority_status")),
        "v551_v552_pressure_component_eligible": bool(atom.get("v552_pressure_component_eligible", False)) if atom else False, "v551_v552_pressure_component_status": _clean(atom.get("v552_pressure_component_status")), "v551_v552_pressure_component_ineligibility_reason": _clean(atom.get("v552_pressure_component_ineligibility_reason")),
        "v551_evidence_basis_origin": _clean(atom.get("evidence_basis_origin")), "v551_provenance_basis_origin": _clean(atom.get("provenance_basis_origin")),
        "v551_v552_pressure_component_status": _clean(atom.get("v552_pressure_component_status")), "v551_temporal_pressure_indicator_authorized": bool(atom.get("temporal_pressure_indicator_authorized", False)) if atom else False,
        "v551_evidence_basis": _clean(atom.get("evidence_basis")), "v551_provenance_basis": _clean(atom.get("provenance_basis")),
        "v551_forbidden_inference": _clean(atom.get("forbidden_inference")), "v551_known_absences": _clean(atom.get("known_absences")),
        "question_identity_status": _v221_old_status(comparisons["question_id_consistent"]), "var_code_status": _v221_old_status(comparisons["var_code_consistent"]),
        "response_identity_status": _v221_old_status(comparisons["response_identity_consistent"]),
        "normalized_response_label_status": _v221_old_status(comparisons["normalized_response_label_consistent"]),
        "semantic_response_role_status": "NOT_COMPARABLE_PARALLEL_CONTRACT", "response_direction_status": _v221_old_status(comparisons["directionality_consistent"]),
        "response_intensity_status": _v221_old_status(comparisons["intensity_consistent"]),
        "semantic_polarity_status": _v221_old_status(comparisons["semantic_polarity_consistent"]),
        "source_polarity_representation_status": "PARALLEL_SOURCE_COORDINATE_PRESERVED" if _v2_scalar(atom.get("polarity")) is not None else "SOURCE_COORDINATE_MISSING",
        "polarity_status": _v221_old_status(comparisons["semantic_polarity_consistent"]),
        "response_semantics_hash_status": _v221_old_status(authority_hash_consistent), "driver_id_status": _v221_old_status(comparisons["driver_id_consistent"]),
        "driver_facet_id_status": _v221_old_status(comparisons["driver_facet_consistent"]), "relation_axis_id_status": _v221_old_status(comparisons["relation_axis_consistent"]),
        "family_target_contract_status": "EXACT_MATCH" if _clean(item.get("target_resolution_status")) else "ONE_SIDE_MISSING", "structural_target_contract_status": "EXACT_MATCH" if _clean(atom.get("structural_mapping_status")) or _clean(atom.get("structural_identity_signature")) else "ONE_SIDE_MISSING", "target_layer_relation_status": "PARALLEL_GOVERNED_TARGET_LAYERS" if _clean(item.get("target_entity_id")) and _clean(atom.get("target_entity_id")) else "FAMILY_TARGET_CONTRACT_GAP" if _clean(atom.get("target_entity_id")) else "STRUCTURAL_TARGET_CONTRACT_GAP",
        "cross_contract_status": conflict_status,
        "cross_contract_reason_codes_json": _v2_json(reason_codes), "comparison_value_audit_json": _v2_json({"response_value": {"v550j": _v2_scalar(item.get("response_value_normalized")), "v551": _v2_scalar(atom.get("response_value_normalized")), "status": "EXACT_MATCH" if comparisons["response_identity_consistent"] == "consistent" else "CONFLICT" if comparisons["response_identity_consistent"] == "conflict" else "ONE_SIDE_MISSING"}, "driver_facet_id": {"v550j": _clean(item.get("driver_facet_id")), "v551": _clean(atom.get("driver_facet_id")), "status": "EXACT_MATCH" if comparisons["driver_facet_consistent"] == "consistent" else "CONFLICT" if comparisons["driver_facet_consistent"] == "conflict" else "ONE_SIDE_MISSING"}, "relation_axis_id": {"v550j": _clean(item.get("relation_axis_id")), "v551": _clean(atom.get("relation_axis_id")), "status": "EXACT_MATCH" if comparisons["relation_axis_consistent"] == "consistent" else "CONFLICT" if comparisons["relation_axis_consistent"] == "conflict" else "ONE_SIDE_MISSING"}, "target_layers": {"v550j_family_target_entity_id": _clean(item.get("target_entity_id")), "v551_structural_target_entity_id": _clean(atom.get("target_entity_id")), "status": "PARALLEL_GOVERNED_TARGET_LAYERS"}}), "component_evidence_role": contribution,
        "component_certification_contribution": contribution, "component_v552_linkage_class": "v552_linkable" if bool(atom.get("v552_pressure_component_eligible", False)) else "v552_ineligible", "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
    }
    row["component_contract_hash"] = recompute_v551j_component_contract_hash(row)
    return row


def build_v551j_joint_component_index(*, pattern_index: pd.DataFrame, pattern_item_index: pd.DataFrame, v551_atoms: pd.DataFrame, run_id: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    component_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    patterns = {str(row.get("pattern_id")): row for row in pattern_index.to_dict("records")}
    item_work = pattern_item_index.copy()
    if "_source_row_index" not in item_work.columns:
        item_work["_source_row_index"] = range(len(item_work))
    item_work = item_work.sort_values(["pattern_id", "item_order", "_source_row_index"], kind="mergesort")
    for item in item_work.to_dict("records"):
        pattern = patterns.get(str(item.get("pattern_id")), {})
        if not pattern:
            continue
        match_status, match_basis, candidates, reasons = _v2_match_atoms_for_item(item, v551_atoms, pattern)
        component = _v2_component_row(run_id, pattern, item, candidates, match_status, match_basis, reasons)
        component_rows.append(component)
        audit_rows.append({
            "run_id": run_id, "packet_id": component["packet_id"], "pattern_id": component["pattern_id"], "component_id": component["component_id"],
            "item_order": component["item_order"], "v551_atom_match_status": match_status, "v551_atom_match_basis": match_basis,
            "candidate_atom_count": int(len(candidates)), "effective_atom_count": 1 if match_status.startswith("MATCHED") else 0,
            "audit_reason_codes_json": _v2_json(reasons), "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        })
    from data.ddm_build_copy.ddm_v551j_schema import V551J_COMPONENT_MATCH_AUDIT_SCHEMA, V551J_JOINT_COMPONENT_INDEX_SCHEMA
    return (
        pd.DataFrame(component_rows).reindex(columns=V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"]),
        pd.DataFrame(audit_rows).reindex(columns=V551J_COMPONENT_MATCH_AUDIT_SCHEMA["required_columns"]),
    )


def _v2_signature(namespace: str, rows: list[dict[str, Any]], fields: list[str]) -> str:
    payload = [{field: _v2_scalar(row.get(field)) for field in fields} for row in rows]
    return _v2_hash(namespace, {"ordered_components": payload})


def validate_governed_input_scope(
    *,
    run_id: str,
    atoms: pd.DataFrame,
    pattern_index: pd.DataFrame,
    pattern_items: pd.DataFrame,
    relation_signatures: pd.DataFrame,
    expected_source: str,
    expected_wave: str,
    expected_country: str,
) -> tuple[pd.DataFrame, list[str]]:
    from data.ddm_build_copy.ddm_v551j_schema import V551J_INPUT_SCOPE_AUDIT_SCHEMA

    issues: list[str] = []

    def _values(frame: pd.DataFrame, *columns: str) -> list[str]:
        for column in columns:
            if column in frame.columns:
                return sorted({str(value).strip() for value in frame[column].fillna("").astype(str) if str(value).strip()})
        return []

    def _status(source_values: list[str], wave_values: list[str], country_values: list[str]) -> tuple[str, list[str]]:
        row_issues: list[str] = []
        if not source_values or not wave_values or not country_values:
            row_issues.append("scope_contract_unresolved")
        if source_values and source_values != [expected_source]:
            row_issues.append("scope_contract_mismatch")
        if wave_values and wave_values != [expected_wave]:
            row_issues.append("scope_contract_mismatch")
        if country_values and country_values != [expected_country]:
            row_issues.append("scope_contract_mismatch")
        if "scope_contract_unresolved" in row_issues:
            return "FAIL_SCOPE_UNRESOLVED", row_issues
        if "scope_contract_mismatch" in row_issues:
            return "FAIL_SCOPE_MISMATCH", row_issues
        return "PASS", []

    rows: list[dict[str, Any]] = []

    def _append(name: str, frame: pd.DataFrame, source_values: list[str], wave_values: list[str], country_values: list[str], extra_issues: list[str] | None = None) -> None:
        status, row_issues = _status(source_values, wave_values, country_values)
        row_issues.extend(extra_issues or [])
        if extra_issues and status == "PASS":
            status = "FAIL_PARENT_COVERAGE"
        issues.extend(row_issues)
        rows.append({
            "run_id": run_id,
            "artifact_name": name,
            "source_family_values_json": _v2_json(source_values),
            "canonical_wave_values_json": _v2_json(wave_values),
            "country_code_values_json": _v2_json(country_values),
            "scope_contract_status": status,
            "row_count": int(len(frame)),
            "issue_codes_json": _v2_json(sorted(set(row_issues))),
            "created_at": utc_now(),
            "schema_version": "v2.2.3",
            "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        })

    _append("v551_atoms", atoms, _values(atoms, "source_family", "source"), _values(atoms, "canonical_wave", "wave"), _values(atoms, "country_code"))
    _append("v550j_pattern_index", pattern_index, _values(pattern_index, "source_family", "source"), _values(pattern_index, "canonical_wave", "wave"), _values(pattern_index, "country_code"))
    parent_scope = pattern_index[["pattern_id"]].copy() if "pattern_id" in pattern_index.columns else pd.DataFrame(columns=["pattern_id"])
    parent_scope["source_family"] = pattern_index.get("source_family", pattern_index.get("source", pd.Series(dtype=str)))
    parent_scope["canonical_wave"] = pattern_index.get("canonical_wave", pattern_index.get("wave", pd.Series(dtype=str)))
    parent_scope["country_code"] = pattern_index.get("country_code", pd.Series(dtype=str))
    item_joined = pattern_items.merge(parent_scope, on="pattern_id", how="left", indicator=True) if "pattern_id" in pattern_items.columns else pattern_items.copy()
    item_issues = ["item_to_pattern_coverage_mismatch"] if not item_joined.empty and (("_merge" not in item_joined.columns) or item_joined["_merge"].astype(str).ne("both").any()) else []
    _append("v550j_pattern_item_index", item_joined, _values(item_joined, "source_family"), _values(item_joined, "canonical_wave"), _values(item_joined, "country_code"), item_issues)
    if "pattern_id" not in relation_signatures.columns:
        relation_joined = relation_signatures.copy()
        relation_issues = ["scope_contract_unresolved"]
    else:
        relation_joined = relation_signatures.merge(parent_scope, on="pattern_id", how="left", indicator=True)
        relation_issues = ["item_to_pattern_coverage_mismatch"] if not relation_joined.empty and relation_joined["_merge"].astype(str).ne("both").any() else []
    _append("v550j_relation_signature", relation_joined, _values(relation_joined, "source_family"), _values(relation_joined, "canonical_wave"), _values(relation_joined, "country_code"), relation_issues)
    return pd.DataFrame(rows).reindex(columns=V551J_INPUT_SCOPE_AUDIT_SCHEMA["required_columns"]), list(dict.fromkeys(issues))


def _v2_packet_status(pattern: Mapping[str, Any], comps: pd.DataFrame, relation_signature: Mapping[str, Any]) -> tuple[str, str, list[str], list[str], dict[str, str]]:
    blockers: list[str] = []
    reviews: list[str] = []
    relation_count = int(comps["component_certification_contribution"].astype(str).eq("relation_component").sum()) if not comps.empty else 0
    context_count = int(comps["component_certification_contribution"].astype(str).isin({"context_component", "special_or_missing_component", "explained_nonrelation_component"}).sum()) if not comps.empty else 0
    if comps.empty:
        blockers.append("pattern_item_count_gate")
    if comps["v551_atom_match_status"].astype(str).eq("AMBIGUOUS_V551_ATOM_MATCH").any():
        blockers.append("ambiguous_component")
    if comps["cross_contract_status"].astype(str).str.endswith("_CONFLICT").any():
        blockers.append("cross_contract_conflict")
    if comps["component_certification_contribution"].astype(str).eq("unresolved_component").any():
        blockers.append("unexplained_component")
    if relation_count < 2:
        blockers.append("insufficient_joint_relation_components")
    measurement = _v2_pattern_measurements(pattern)
    if measurement["joint_measurement_status"] != "COMPLETE_PATTERN_MEASUREMENT_CONTRACT" or _clean(pattern.get("support_gate_status")).lower() in {"blocked", "unsupported", "fail", "failed"}:
        reviews.append("measurement_gap")
    semantic_authority_col = (
        "v550j_item_response_semantics_authority_status"
        if "v550j_item_response_semantics_authority_status" in comps.columns
        else "v551_response_semantics_authority_status"
        if "v551_response_semantics_authority_status" in comps.columns
        else "v551_semantic_role_authority_status"
    )
    semantic_status = "CERTIFIED" if not comps.empty and semantic_authority_col in comps.columns and comps[semantic_authority_col].map(_v2_bool_certified).all() else "REVIEW_REQUIRED"
    direction_status = "CERTIFIED" if not comps.empty and comps["v550j_item_directionality_authority_status"].map(_v2_bool_certified).all() else "REVIEW_REQUIRED"
    component_target_resolved = (
        not comps.empty
        and "v550j_target_resolution_status" in comps.columns
        and comps["v550j_target_resolution_status"].fillna("").astype(str).str.lower().isin(
            {"family_registry_resolved_condition", "family_registry_resolved_group", "registry_resolved", "resolved", "certified"}
        ).all()
    )
    target_status = "CERTIFIED" if component_target_resolved or _clean(relation_signature.get("target_structure_status")).lower() in {"single_target", "multi_target_allowed", "resolved", "target_resolved", "coherent"} or float(pattern.get("registry_resolved_share", 0) or 0) > 0 else "REVIEW_REQUIRED"
    structural_status = "CERTIFIED" if not comps.empty and comps["v551_structural_mapping_status"].fillna("").astype(str).str.lower().isin({"mapped", "resolved", "certified", "pass", "ok", "complete", "structural_mapping_certified"}).all() else "REVIEW_REQUIRED"
    measurement_status = "CERTIFIED" if not reviews else "REVIEW_REQUIRED"
    if semantic_status != "CERTIFIED":
        reviews.append("semantic_authority_gap")
    if direction_status != "CERTIFIED":
        reviews.append("directionality_authority_gap")
    if target_status != "CERTIFIED":
        reviews.append("target_authority_gap")
    if structural_status != "CERTIFIED":
        reviews.append("structural_authority_gap")
    if blockers:
        if "ambiguous_component" in blockers:
            status = "BLOCKED_AMBIGUOUS_COMPONENT_MATCH"
        elif "cross_contract_conflict" in blockers:
            status = "BLOCKED_CROSS_CONTRACT_CONFLICT"
        elif "insufficient_joint_relation_components" in blockers:
            status = "CONTEXT_ONLY_PATTERN"
        else:
            status = "BLOCKED_PACKET_CONTRACT"
    elif reviews:
        status = "REVIEW_REQUIRED_AUTHORITY_GAP" if any(x in reviews for x in ["semantic_authority_gap", "directionality_authority_gap", "target_authority_gap", "structural_authority_gap"]) else "REVIEW_REQUIRED_COMPONENT_GAP"
    elif context_count:
        status = "CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT"
    else:
        status = "CERTIFIED_JOINT_RELATION_EVIDENCE"
    if status.startswith("CERTIFIED") and comps["v550j_item_response_direction"].fillna("").astype(str).nunique() > 1:
        evidence_class = "joint_mixed_directional_relation_observation"
    elif status.startswith("CERTIFIED") and context_count:
        evidence_class = "joint_relation_observation_with_context_components"
    elif status.startswith("CERTIFIED"):
        evidence_class = "joint_directional_relation_observation"
    elif relation_count < 2:
        evidence_class = "joint_pattern_context_only"
    else:
        evidence_class = "blocked_joint_pattern"
    authority = {
        "joint_semantic_authority_status": semantic_status,
        "joint_directionality_authority_status": direction_status,
        "joint_family_target_authority_status": target_status,
        "joint_structural_authority_status": structural_status,
        "joint_measurement_authority_status": measurement_status,
        "joint_evidence_authority_status": "CERTIFIED" if status.startswith("CERTIFIED") else "REVIEW_REQUIRED" if status.startswith("REVIEW") else "BLOCKED",
    }
    return status, evidence_class, sorted(set(reviews)), sorted(set(blockers)), authority


def build_v551j_joint_outputs_v2(
    *,
    run_id: str,
    atoms: pd.DataFrame,
    pattern_index: pd.DataFrame,
    pattern_item_index: pd.DataFrame,
    relation_signature: pd.DataFrame,
    registry_path: str,
    v550j_manifest_path: str,
    v550j_readiness_report_path: str,
    association_index: pd.DataFrame | None = None,
    position_signature: pd.DataFrame | None = None,
    meaning_summary: pd.DataFrame | None = None,
    deprecated_v552_inputs_supplied: int = 0,
    input_hashes: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    from data.ddm_build_copy.ddm_v551j_schema import (
        V551J_ASSOCIATION_CONTEXT_SIDECAR_SCHEMA, V551J_CERTIFICATION_AUDIT_SCHEMA, V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA,
        V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA, V551J_COMPONENT_MATCH_AUDIT_SCHEMA, V551J_JOINT_COMPONENT_INDEX_SCHEMA,
        V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA, V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA, V551J_JOINT_READINESS_REPORT_SCHEMA,
        V551J_MEANING_SUMMARY_SIDECAR_SCHEMA, V551J_MEASUREMENT_SEPARATION_AUDIT_SCHEMA, V551J_PATTERN_CONTEXT_SIDECAR_SCHEMA,
        V551J_POSITION_CONTEXT_SIDECAR_SCHEMA, V551J_REGISTRY_CONTRACT_AUDIT_SCHEMA, V551J_INPUT_SCOPE_AUDIT_SCHEMA,
        V551J_PACKET_CONTRACT_VALIDATION_REPORT_SCHEMA, V551J_V2_FORBIDDEN_CLAIM_IDS, V551J_V2_FORBIDDEN_FUTURE_TARGETS,
        V551J_CROSS_CONTRACT_COMPARISON_AUDIT_SCHEMA, V551J_TARGET_LAYER_AUDIT_SCHEMA,
        V551J_DENOMINATOR_SEPARATION_AUDIT_SCHEMA,
    )
    registry_hash = _v2_hash_file(registry_path)
    manifest_hash = _v2_hash_file(v550j_manifest_path)
    readiness_hash = _v2_hash_file(v550j_readiness_report_path)
    input_hashes = dict(input_hashes or {})
    v551_hash = input_hashes.get("v551_atoms_artifact_hash", "")
    manifest = {}
    readiness = {}
    try:
        manifest = json.loads(Path(v550j_manifest_path).read_text(encoding="utf-8"))
    except Exception:
        pass
    try:
        readiness = json.loads(Path(v550j_readiness_report_path).read_text(encoding="utf-8"))
    except Exception:
        pass
    manifest_registry_path = manifest.get("registry_path") or manifest.get("input_documents", {}).get("registry_path", "")
    manifest_registry_hash = manifest.get("question_family_registry_hash") or _v2_hash_file(manifest_registry_path)
    if registry_hash in {"missing", "not_supplied"}:
        registry_contract_status = "BLOCKED_MISSING_CURRENT_REGISTRY"
    elif not manifest_registry_hash or manifest_registry_hash in {"missing", "not_supplied"}:
        registry_contract_status = "BLOCKED_MISSING_V550J_MANIFEST_REGISTRY_HASH"
    elif registry_hash != manifest_registry_hash:
        registry_contract_status = "BLOCKED_REGISTRY_HASH_MISMATCH"
    else:
        registry_contract_status = "MATCHED_GOVERNED_REGISTRY_HASH"
    component_df, match_audit = build_v551j_joint_component_index(pattern_index=pattern_index, pattern_item_index=pattern_item_index, v551_atoms=atoms, run_id=run_id)
    relation_map = {str(row.get("pattern_id")): row for row in relation_signature.to_dict("records")}
    candidate_rows: list[dict[str, Any]] = []
    measurement_rows: list[dict[str, Any]] = []
    cert_audit_rows: list[dict[str, Any]] = []
    rejection_rows: list[dict[str, Any]] = []
    for pattern in pattern_index.to_dict("records"):
        pid = _clean(pattern.get("pattern_id"))
        comps = component_df[component_df["pattern_id"].astype(str).eq(pid)].sort_values("item_order", kind="mergesort")
        comp_records = comps.to_dict("records")
        relation_row = relation_map.get(pid, {})
        packet_id = _v2_packet_id(pattern)
        status, evidence_class, reviews, blockers, authority = _v2_packet_status(pattern, comps, relation_row)
        measurements = _v2_pattern_measurements(pattern)
        empirical_object_ids = [r.get("v551_empirical_object_id") or None for r in comp_records]
        empirical_distribution_ids = [r.get("v551_empirical_distribution_id") or None for r in comp_records]
        measurement_hashes = [r.get("v551_measurement_contract_hash") or None for r in comp_records]
        denominator_values = [r.get("v551_n_respondents") if _v2_scalar(r.get("v551_n_respondents")) is not None else None for r in comp_records]
        pressure_linkage_values = [r.get("component_v552_linkage_class") or None for r in comp_records]
        distinct_distributions = sorted({str(x) for x in empirical_distribution_ids if x})
        denominator_nonnull = [x for x in denominator_values if x is not None]
        pressure_counts = Counter(str(x) for x in pressure_linkage_values if x)
        denominator_by_distribution: dict[str, Any] = {}
        denominator_violations: list[str] = []
        for r in comp_records:
            dist = _clean(r.get("v551_empirical_distribution_id"))
            denom = r.get("v551_n_respondents")
            if not dist:
                continue
            prior = denominator_by_distribution.get(dist)
            if prior is None:
                denominator_by_distribution[dist] = denom
            elif _v2_scalar(prior) != _v2_scalar(denom):
                denominator_violations.append(dist)
        denominator_separation_status = "PASS" if not denominator_violations else "BLOCKED_DISTRIBUTION_DENOMINATOR_CONFLICT"
        response_sig = recompute_joint_response_identity_signature(comp_records)
        empirical_distribution_sig = recompute_joint_empirical_distribution_signature(comp_records)
        semantic_sig = recompute_joint_semantic_signature(comp_records)
        orientation_sig = recompute_joint_orientation_signature(comp_records)
        topology_sig = recompute_joint_topology_signature(pattern, comp_records)
        target_sig = recompute_joint_target_signature(comp_records)
        structural_sig = recompute_joint_structural_signature({**dict(pattern), "pattern_id": pid, "target_structure_status": relation_row.get("target_structure_status")}, comp_records)
        component_measurement_sig = recompute_joint_component_measurement_signature(comp_records)
        measurement_hash = recompute_joint_measurement_contract_hash(measurements)
        component_hashes = comps["component_contract_hash"].dropna().astype(str).tolist() if not comps.empty else []
        ready = status.startswith("CERTIFIED")
        permissions = {
            "ready_for_v552j_joint_evidence": ready,
            "ready_for_v553": False,
            "pressure_anchor_eligible": False,
            "temporal_pressure_authorized": False,
            "runtime_use_class": "not_runtime_consumable",
            "allowed_future_targets_json": _v2_json(["v552j"] if ready else []),
            "forbidden_future_targets_json": _v2_json(V551J_V2_FORBIDDEN_FUTURE_TARGETS),
            "forbidden_claim_ids_json": _v2_json(V551J_V2_FORBIDDEN_CLAIM_IDS),
        }
        contract_hash = ""
        row = {
            "run_id": run_id, "packet_id": packet_id, "packet_contract_hash": contract_hash, "pattern_id": pid, "family_id": _clean(pattern.get("family_id")),
            "family_label": _clean(pattern.get("family_label")), "family_type": _clean(pattern.get("family_type")), "family_structure_type": _clean(pattern.get("family_structure_type")),
            "source": _clean(pattern.get("source")), "source_family": _clean(pattern.get("source_family")) or _clean(pattern.get("source")), "wave": _clean(pattern.get("wave")),
            "canonical_wave": _clean(pattern.get("canonical_wave")) or _clean(pattern.get("wave")), "country_code": _clean(pattern.get("country_code")), "survey_year": pattern.get("survey_year"),
            "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
            "boundary_pattern_type": _clean(pattern.get("boundary_pattern_type")),
            "target_structure_status": _clean(relation_row.get("target_structure_status")) or _clean(pattern.get("target_structure_status")),
            "v551_schema_version": _clean(atoms.get("schema_version", pd.Series([""])).iloc[0]) if not atoms.empty and "schema_version" in atoms.columns else "",
            "v551_input_artifact_hash": v551_hash,
            "v550j_pattern_index_artifact_hash": input_hashes.get("v550j_pattern_index_artifact_hash", ""),
            "v550j_pattern_item_index_artifact_hash": input_hashes.get("v550j_pattern_item_index_artifact_hash", ""),
            "v550j_relation_signature_artifact_hash": input_hashes.get("v550j_relation_signature_artifact_hash", ""),
            "v550j_schema_version": _clean(pattern.get("schema_version")), "v550j_manifest_hash": manifest_hash,
            "v550j_readiness_report_hash": readiness_hash, "question_family_registry_path": str(registry_path), "question_family_registry_hash": registry_hash,
            "question_family_registry_status": registry_contract_status,
            "v550j_input_contract_status": "VALIDATED_V550J_PATTERN_CONTRACT" if len(pattern_index) and len(pattern_item_index) and len(relation_signature) else "BLOCKED_V550J_PATTERN_CONTRACT",
            "pattern_item_count": int(len(comps)), "matched_relation_component_count": int(comps["component_certification_contribution"].astype(str).eq("relation_component").sum()) if not comps.empty else 0,
            "matched_context_component_count": int(comps["component_certification_contribution"].astype(str).eq("context_component").sum()) if not comps.empty else 0,
            "special_or_missing_component_count": int(comps["component_certification_contribution"].astype(str).eq("special_or_missing_component").sum()) if not comps.empty else 0,
            "unmatched_explained_component_count": int(comps["component_certification_contribution"].astype(str).eq("explained_nonrelation_component").sum()) if not comps.empty else 0,
            "unmatched_unexplained_component_count": int(comps["component_certification_contribution"].astype(str).eq("unresolved_component").sum()) if not comps.empty else 0,
            "ambiguous_component_count": int(comps["v551_atom_match_status"].astype(str).eq("AMBIGUOUS_V551_ATOM_MATCH").sum()) if not comps.empty else 0,
            "cross_contract_conflict_count": int(comps["cross_contract_status"].astype(str).str.endswith("_CONFLICT").sum()) if not comps.empty else 0,
            "component_contract_complete": bool(not blockers), "component_order_integrity_status": "PASS" if not comps.empty and comps["item_order"].is_unique else "BLOCKED_DUPLICATE_ITEM_ORDER",
            "component_match_status_summary_json": _v2_json(comps["v551_atom_match_status"].astype(str).value_counts().to_dict() if not comps.empty else {}),
            "matched_atom_ids_json": _v2_json([x for x in comps["v551_atom_id"].dropna().astype(str).tolist() if x]), "matched_atom_contract_hashes_json": _v2_json([x for x in comps["v551_atom_contract_hash"].dropna().astype(str).tolist() if x]),
            "matched_empirical_object_ids_json": _v2_json([x for x in empirical_object_ids if x]),
            "matched_empirical_distribution_ids_json": _v2_json([x for x in empirical_distribution_ids if x]),
            "distinct_matched_empirical_distribution_count": len(distinct_distributions),
            "component_question_denominator_nonnull_count": len(denominator_nonnull),
            "component_question_denominator_null_count": len(denominator_values) - len(denominator_nonnull),
            "component_question_denominator_min": min(denominator_nonnull) if denominator_nonnull else None,
            "component_question_denominator_max": max(denominator_nonnull) if denominator_nonnull else None,
            "component_question_denominators_ordered_json": _v2_json(denominator_values),
            "denominator_separation_status": denominator_separation_status,
            "v552_pressure_linkable_component_count": int(pressure_counts.get("v552_linkable", 0)),
            "v552_pressure_ineligible_component_count": int(pressure_counts.get("v552_ineligible", 0)),
            "v552_pressure_review_required_component_count": int(pressure_counts.get("v552_review_required", 0)),
            "v552_pressure_linkage_status_summary_json": _v2_json(dict(pressure_counts)),
            "joint_response_identity_signature": response_sig, "joint_empirical_distribution_signature": empirical_distribution_sig,
            "joint_semantic_signature": semantic_sig, "joint_orientation_signature": orientation_sig, "joint_topology_signature": topology_sig,
            "joint_target_signature": target_sig, "joint_structural_signature": structural_sig, "joint_measurement_contract_hash": measurement_hash,
            "joint_component_measurement_signature": component_measurement_sig,
            "component_contract_hashes_ordered_json": _v2_json(component_hashes),
            "component_measurement_contract_hashes_ordered_json": _v2_json(measurement_hashes),
            "component_empirical_object_ids_ordered_json": _v2_json(empirical_object_ids),
            "component_empirical_distribution_ids_ordered_json": _v2_json(empirical_distribution_ids),
            "component_response_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v550j_item_question_id", "v550j_item_var_code", "v551_question_id", "v551_var_code", "v550j_item_response_value_normalized"]} for r in comp_records]),
            "component_semantic_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v550j_item_semantic_response_role", "v551_semantic_identity_signature"]} for r in comp_records]),
            "component_orientation_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v550j_item_response_direction", "v550j_item_response_intensity", "v550j_item_polarity"]} for r in comp_records]),
            "component_topology_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v551_response_scale_signature"]} for r in comp_records]),
            "component_target_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v550j_relation_axis_id", "v550j_family_target_entity_id", "v551_structural_target_entity_id"]} for r in comp_records]),
            "component_structural_vector_json": _v2_json([{k: r.get(k) for k in ["item_order", "v551_structural_identity_signature"]} for r in comp_records]),
            "component_denominator_vector_json": _v2_json([{"item_order": r.get("item_order"), "empirical_distribution_id": r.get("v551_empirical_distribution_id"), "n_respondents": r.get("v551_n_respondents")} for r in comp_records]),
            "component_pressure_linkage_vector_json": _v2_json([{"item_order": r.get("item_order"), "component_v552_linkage_class": r.get("component_v552_linkage_class")} for r in comp_records]),
            **measurements, "joint_evidence_class": evidence_class, **authority,
            "semantic_conflict_status": _clean(relation_row.get("semantic_conflict_status")), "shared_structural_status": authority["joint_structural_authority_status"], "family_target_status": authority["joint_family_target_authority_status"],
            "expected_multi_target": bool(pattern.get("expected_multi_target")), "target_resolution_coverage": pattern.get("registry_resolved_share"), "mapping_coverage": pattern.get("mapping_coverage_score"),
            "certification_status": status, "review_required": bool(status.startswith("REVIEW") or status.startswith("BLOCKED") or status.startswith("DIAGNOSTIC")),
            "review_reason_codes_json": _v2_json(reviews), "blocking_reason_codes_json": _v2_json(blockers), **permissions,
            "ready_for_v552j_component_linkage": bool(ready and not denominator_violations and len(comp_records) == int(len(comps))),
            "known_absences_json": _v2_json([x for x in comps["v551_known_absences"].dropna().astype(str).tolist() if x]),
            "compatibility_projection_only": False, "not_authoritative_v2_artifact": False,
        }
        row["joint_measurement_contract_hash"] = recompute_joint_measurement_contract_hash(row)
        measurement_hash = row["joint_measurement_contract_hash"]
        candidate_rows.append(row)
        measurement_rows.append({"run_id": run_id, "pattern_id": pid, "packet_id": packet_id, "pattern_measurement_source": "v550j_joint_response_pattern_index", "association_measurements_present": bool(association_index is not None and not association_index.empty), "association_measurements_used_in_core_packet": False, "atom_measurements_used_as_pattern_measurements": False, "measurement_contract_hash": measurement_hash, "measurement_separation_status": "PASS", "violations_json": _v2_json([]), "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3"})
        cert_audit_rows.append({"run_id": run_id, "packet_id": packet_id, "packet_type": evidence_class, "source": row["source"], "wave": row["wave"], "canonical_wave": row["canonical_wave"], "country_code": row["country_code"], "gate_identity_pass": True, "gate_lifecycle_pass": True, "gate_authority_pass": authority["joint_evidence_authority_status"] == "CERTIFIED", "gate_support_pass": measurements["joint_measurement_status"] == "COMPLETE_PATTERN_MEASUREMENT_CONTRACT", "gate_directionality_pass": authority["joint_directionality_authority_status"] == "CERTIFIED", "gate_forbidden_claims_pass": True, "gate_mediation_flags_pass": True, "gate_no_downstream_leakage_pass": True, "certified": ready, "certification_blockers_json": _v2_json(blockers), "certification_notes_json": _v2_json(reviews), "created_at": utc_now(), "schema_version": "v2.2.3"})
        if not ready:
            rejection_rows.append({"run_id": run_id, "packet_id": packet_id, "packet_type": evidence_class, "source": row["source"], "wave": row["wave"], "canonical_wave": row["canonical_wave"], "country_code": row["country_code"], "certification_blocker_code": status, "certification_blocker_detail": _v2_json(blockers or reviews), "gate_identity_pass": True, "gate_lifecycle_pass": True, "gate_authority_pass": False, "gate_support_pass": measurements["joint_measurement_status"] == "COMPLETE_PATTERN_MEASUREMENT_CONTRACT", "gate_directionality_pass": authority["joint_directionality_authority_status"] == "CERTIFIED", "gate_forbidden_claims_pass": True, "gate_mediation_flags_pass": True, "gate_no_downstream_leakage_pass": True, "created_at": utc_now(), "schema_version": "v2.2.3"})
    candidate = pd.DataFrame(candidate_rows).reindex(columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"])
    certified = candidate[candidate["certification_status"].astype(str).str.startswith("CERTIFIED")].copy().reindex(columns=V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA["required_columns"])
    review = candidate[candidate["review_required"].fillna(False).astype(bool)].copy()
    if review.empty:
        review_surface = pd.DataFrame(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
    else:
        review_surface = pd.DataFrame([{"run_id": run_id, "packet_id": r["packet_id"], "pattern_id": r["pattern_id"], "family_id": r["family_id"], "certification_status": r["certification_status"], "review_required": r["review_required"], "review_priority": "high" if str(r["certification_status"]).startswith("BLOCKED") else "medium" if str(r["certification_status"]).startswith("REVIEW") else "diagnostic", "review_reason_codes_json": r["review_reason_codes_json"], "blocking_reason_codes_json": r["blocking_reason_codes_json"], "joint_evidence_class": r["joint_evidence_class"], "ready_for_v552j_joint_evidence": r["ready_for_v552j_joint_evidence"], "review_triage_priority_score": 1.0 if str(r["certification_status"]).startswith("BLOCKED") else 0.5, "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3"} for r in review.to_dict("records")]).reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
    context_sidecar = candidate[candidate["joint_evidence_class"].astype(str).eq("joint_pattern_context_only")][["run_id", "packet_id", "pattern_id", "family_id", "joint_evidence_class"]].copy()
    if context_sidecar.empty:
        context_sidecar = pd.DataFrame(columns=V551J_PATTERN_CONTEXT_SIDECAR_SCHEMA["required_columns"])
    else:
        context_sidecar["context_reason"] = "fewer_than_two_matched_relation_components"; context_sidecar["created_at"] = utc_now(); context_sidecar["schema_version"] = "v2.2.3"; context_sidecar["compiler_version"] = "v551j_joint_evidence_contract_v2_2_3"; context_sidecar = context_sidecar.reindex(columns=V551J_PATTERN_CONTEXT_SIDECAR_SCHEMA["required_columns"])
    assoc_sidecar = pd.DataFrame(columns=V551J_ASSOCIATION_CONTEXT_SIDECAR_SCHEMA["required_columns"])
    pos_sidecar = pd.DataFrame(columns=V551J_POSITION_CONTEXT_SIDECAR_SCHEMA["required_columns"])
    meaning_sidecar = pd.DataFrame(columns=V551J_MEANING_SUMMARY_SIDECAR_SCHEMA["required_columns"])
    comparison_fields = {
        "question_id": ("v550j_item_question_id", "v551_question_id", "question_identity_status"),
        "var_code": ("v550j_item_var_code", "v551_var_code", "var_code_status"),
        "response_value_normalized": ("v550j_item_response_value_normalized", "v551_response_value_normalized", "response_identity_status"),
        "normalized_response_label": ("v550j_item_normalized_response_label", "v551_normalized_response_label", "normalized_response_label_status"),
        "joint_response_stance_alignment": ("v550j_joint_response_stance", "v551_response_direction", "joint_response_stance_alignment_status"),
        "v551_evidence_role": ("v551_evidence_role", "v551_evidence_role", "v551_evidence_role_status"),
        "semantic_response_role": ("v550j_item_semantic_response_role", "v551_semantic_response_role", "semantic_response_role_status"),
        "response_direction": ("v550j_item_response_direction", "v551_response_direction", "response_direction_status"),
        "response_intensity": ("v550j_item_response_intensity", "v551_response_intensity", "response_intensity_status"),
        "semantic_polarity": ("v550j_semantic_polarity_label", "v551_response_direction", "semantic_polarity_status"),
        "source_polarity_coordinate": ("v551_source_polarity_coordinate", "v551_source_polarity_coordinate", "source_polarity_representation_status"),
        "response_semantics_contract_hash": ("v550j_item_response_semantics_contract_hash", "v551_response_semantics_contract_hash", "response_semantics_hash_status"),
        "driver_id": ("v550j_driver_id", "v551_driver_id", "driver_id_status"),
        "driver_facet_id": ("v550j_driver_facet_id", "v551_driver_facet_id", "driver_facet_id_status"),
        "relation_axis_id": ("v550j_relation_axis_id", "v551_relation_axis_id", "relation_axis_id_status"),
    }
    comparison_audit_rows: list[dict[str, Any]] = []
    target_audit_rows: list[dict[str, Any]] = []
    denominator_rows: list[dict[str, Any]] = []
    for record in component_df.to_dict("records"):
        for field, (v550j_col, v551_col, status_col) in comparison_fields.items():
            status = _clean(record.get(status_col)) or "NOT_EVALUATED"
            issue = ""
            left = _v2_scalar(record.get(v550j_col))
            right = _v2_scalar(record.get(v551_col))
            if field in {"source_polarity_coordinate", "joint_response_stance_alignment", "v551_evidence_role"}:
                issue = "" if status in {"PARALLEL_SOURCE_COORDINATE_PRESERVED", "SOURCE_COORDINATE_MISSING", "INVALID_SOURCE_COORDINATE"} else "INVALID_SOURCE_POLARITY_STATUS"
                if field == "joint_response_stance_alignment":
                    issue = "" if status in {"EXACT_GOVERNED_ALIGNMENT", "ONE_SIDE_MISSING", "UNKNOWN_STANCE_TOKEN", "CONFLICT"} else "INVALID_STANCE_ALIGNMENT_STATUS"
                if field == "v551_evidence_role":
                    issue = "" if status in {"VALID_RELATION_EVIDENCE_ROLE", "VALID_CONTEXT_EVIDENCE_ROLE", "UNKNOWN_EVIDENCE_ROLE", "MISSING_EVIDENCE_ROLE"} else "INVALID_EVIDENCE_ROLE_STATUS"
            elif left is not None and right is not None and str(left) == str(right) and status == "CONFLICT":
                issue = "EQUAL_VALUES_MARKED_CONFLICT"
            elif left is not None and right is not None and str(left).casefold() != str(right).casefold() and status == "EXACT_MATCH":
                issue = "DIFFERENT_VALUES_MARKED_EXACT_MATCH"
            comparison_audit_rows.append({
                "run_id": run_id, "packet_id": record.get("packet_id"), "pattern_id": record.get("pattern_id"),
                "component_id": record.get("component_id"), "item_order": record.get("item_order"), "field_name": field,
                "v550j_value": left, "v551_value": right, "comparison_status": status, "issue_code": issue,
                "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
            })
        target_audit_rows.append({
            "run_id": run_id, "packet_id": record.get("packet_id"), "pattern_id": record.get("pattern_id"),
            "component_id": record.get("component_id"), "v550j_family_target_entity_id": record.get("v550j_family_target_entity_id"),
            "v551_structural_target_entity_id": record.get("v551_structural_target_entity_id"),
            "family_target_contract_status": record.get("family_target_contract_status"),
            "structural_target_contract_status": record.get("structural_target_contract_status"),
            "target_layer_relation_status": record.get("target_layer_relation_status"),
            "issue_code": "" if record.get("target_layer_relation_status") != "EXPLICIT_SAME_NAMESPACE_CONFLICT" else "explicit_target_conflict",
            "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        })
        denominator_rows.append({
            "run_id": run_id, "packet_id": record.get("packet_id"), "pattern_id": record.get("pattern_id"),
            "v551_empirical_distribution_id": record.get("v551_empirical_distribution_id"),
            "v551_n_respondents": record.get("v551_n_respondents"),
            "component_denominator_sum_used_as_joint_n": False,
            "component_denominator_substitution_detected": False,
            "component_denominator_equality_required_across_questions": False,
            "denominator_status": "PASS" if _v2_scalar(record.get("v551_n_respondents")) is not None else "DENOMINATOR_GAP",
            "issue_code": "" if _v2_scalar(record.get("v551_n_respondents")) is not None else "missing_v551_n_respondents",
            "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        })
    measurement_audit = pd.DataFrame(measurement_rows).reindex(columns=V551J_MEASUREMENT_SEPARATION_AUDIT_SCHEMA["required_columns"])
    comparison_audit = pd.DataFrame(comparison_audit_rows).reindex(columns=V551J_CROSS_CONTRACT_COMPARISON_AUDIT_SCHEMA["required_columns"])
    target_layer_audit = pd.DataFrame(target_audit_rows).reindex(columns=V551J_TARGET_LAYER_AUDIT_SCHEMA["required_columns"])
    denominator_audit = pd.DataFrame(denominator_rows).reindex(columns=V551J_DENOMINATOR_SEPARATION_AUDIT_SCHEMA["required_columns"])
    cert_audit = pd.DataFrame(cert_audit_rows).reindex(columns=V551J_CERTIFICATION_AUDIT_SCHEMA["required_columns"])
    rejection_audit = pd.DataFrame(rejection_rows).reindex(columns=V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA["required_columns"])
    expected_source = _clean(candidate["source_family"].iloc[0]) if not candidate.empty else ""
    expected_wave = _clean(candidate["canonical_wave"].iloc[0]) if not candidate.empty else ""
    expected_country = _clean(candidate["country_code"].iloc[0]) if not candidate.empty else ""
    scope_audit, scope_issues = validate_governed_input_scope(
        run_id=run_id,
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_items=pattern_item_index,
        relation_signatures=relation_signature,
        expected_source=expected_source,
        expected_wave=expected_wave,
        expected_country=expected_country,
    )
    registry_audit = pd.DataFrame([{"run_id": run_id, "registry_path": str(registry_path), "registry_hash": registry_hash, "v550j_manifest_registry_path": manifest_registry_path, "v550j_manifest_registry_hash": manifest_registry_hash, "registry_contract_status": registry_contract_status, "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3"}], columns=V551J_REGISTRY_CONTRACT_AUDIT_SCHEMA["required_columns"])
    validation_issues: list[str] = []
    if registry_contract_status != "MATCHED_GOVERNED_REGISTRY_HASH":
        validation_issues.append("registry_hash_mismatch")
    validation_issues.extend(scope_issues)
    packet_required_columns = V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    for column in packet_required_columns:
        if column not in candidate.columns:
            validation_issues.append(f"missing_packet_column:{column}")
            continue
        if column.endswith("_json"):
            null_mask = candidate[column].isna() | candidate[column].astype(str).eq("")
        else:
            null_mask = candidate[column].isna()
        if null_mask.any() and column not in {"packet_contract_hash", "review_reason_codes_json", "blocking_reason_codes_json"}:
            validation_issues.append(f"null_packet_column:{column}:{int(null_mask.sum())}")
    comparison_issue_count = int(comparison_audit["issue_code"].fillna("").astype(str).ne("").sum()) if not comparison_audit.empty else 0
    if comparison_issue_count:
        validation_issues.append(f"comparison_status_inconsistencies:{comparison_issue_count}")
    denominator_issue_count = int(denominator_audit["issue_code"].fillna("").astype(str).ne("").sum()) if not denominator_audit.empty else 0
    if denominator_issue_count:
        validation_issues.append(f"denominator_issues:{denominator_issue_count}")
    measurement_issue_count = int((measurement_audit["measurement_separation_status"].astype(str) != "PASS").sum()) if not measurement_audit.empty else 0
    if measurement_issue_count:
        validation_issues.append(f"measurement_separation_issues:{measurement_issue_count}")
    unknown_cross = sorted(set(component_df["cross_contract_status"].fillna("").astype(str)) - {
        "CROSS_CONTRACT_CONSISTENT", "CROSS_CONTRACT_GAP", "CROSS_CONTRACT_RESPONSE_CONFLICT",
        "CROSS_CONTRACT_SEMANTIC_CONFLICT", "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT",
        "CROSS_CONTRACT_SOURCE_INTENSITY_CONFLICT", "CROSS_CONTRACT_SHARED_STRUCTURAL_CONFLICT",
        "CROSS_CONTRACT_EXPLICIT_TARGET_CONFLICT",
    }) if "cross_contract_status" in component_df.columns else []
    if unknown_cross:
        validation_issues.append(f"unknown_cross_contract_status:{unknown_cross}")
    if "ready_for_v553" in candidate.columns and candidate["ready_for_v553"].fillna(False).astype(bool).any():
        validation_issues.append("direct_v553_authorization")
    if "pressure_anchor_eligible" in candidate.columns and candidate["pressure_anchor_eligible"].fillna(False).astype(bool).any():
        validation_issues.append("pressure_anchor_authorization")
    if "temporal_pressure_authorized" in candidate.columns and candidate["temporal_pressure_authorized"].fillna(False).astype(bool).any():
        validation_issues.append("temporal_authorization")
    if "runtime_use_class" in candidate.columns and not candidate["runtime_use_class"].fillna("").astype(str).eq("not_runtime_consumable").all():
        validation_issues.append("runtime_authorization")
    validation_report = pd.DataFrame([{"run_id": run_id, "candidate_contract_valid": not validation_issues, "component_contract_valid": not validation_issues, "issue_count": len(validation_issues), "issues_json": _v2_json(validation_issues), "created_at": utc_now(), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3"}], columns=V551J_PACKET_CONTRACT_VALIDATION_REPORT_SCHEMA["required_columns"])
    certified_count = int(len(certified)); review_count = int(candidate["certification_status"].astype(str).str.startswith("REVIEW").sum()); blocked_count = int(candidate["certification_status"].astype(str).str.startswith("BLOCKED").sum()); context_count = int(candidate["joint_evidence_class"].astype(str).eq("joint_pattern_context_only").sum())
    candidate_contract_valid = bool(validation_report.iloc[0]["candidate_contract_valid"])
    component_contract_valid = bool(validation_report.iloc[0]["component_contract_valid"])
    final_status = "READY_V551J_JOINT_EVIDENCE_CONTRACT" if certified_count and candidate_contract_valid and component_contract_valid else "BLOCKED_PACKET_CONTRACT" if validation_issues else "PARTIAL_READY_V551J_REVIEW_ONLY" if review_count or blocked_count else "PARTIAL_READY_V551J_CONTEXT_ONLY" if context_count else "BLOCKED_V551J_NO_CANDIDATE_PATTERNS"
    readiness_report = {"run_id": run_id, "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3", "source_family": _clean(candidate["source_family"].iloc[0]) if not candidate.empty else "", "canonical_wave": _clean(candidate["canonical_wave"].iloc[0]) if not candidate.empty else "", "country_code": _clean(candidate["country_code"].iloc[0]) if not candidate.empty else "", "input_pattern_count": int(len(pattern_index)), "input_pattern_item_count": int(len(pattern_item_index)), "candidate_packet_count": int(len(candidate)), "component_row_count": int(len(component_df)), "certified_packet_count": certified_count if candidate_contract_valid and component_contract_valid else 0, "certified_with_context_count": int(candidate["certification_status"].astype(str).eq("CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT").sum()) if not candidate.empty and candidate_contract_valid else 0, "review_required_packet_count": review_count, "context_only_packet_count": context_count, "blocked_packet_count": blocked_count, "ambiguous_component_count": int(candidate["ambiguous_component_count"].sum()) if not candidate.empty else 0, "cross_contract_conflict_count": int(candidate["cross_contract_conflict_count"].sum()) if not candidate.empty else 0, "measurement_separation_violation_count": int((measurement_audit["measurement_separation_status"].astype(str) != "PASS").sum()) if not measurement_audit.empty else 0, "registry_contract_status": registry_audit.iloc[0]["registry_contract_status"], "scope_contract_status": "PASS" if not scope_issues else "FAIL_SCOPE_MISMATCH", "candidate_contract_valid": candidate_contract_valid, "component_contract_valid": component_contract_valid, "ready_for_review": bool(len(review_surface)), "ready_for_v552j_joint_evidence": bool(certified_count and candidate_contract_valid and component_contract_valid), "ready_for_v553": False, "final_status": final_status, "blockers_json": _v2_json(validation_issues), "warnings_json": _v2_json([f"deprecated_v552_inputs_supplied={deprecated_v552_inputs_supplied}", f"v550j_original_readiness={readiness.get('readiness_status', '')}"]), "created_at": utc_now()}
    return {
        "candidate": candidate, "component": component_df, "certified": certified, "review_surface": review_surface,
        "pattern_context_sidecar": context_sidecar, "association_context_sidecar": assoc_sidecar, "position_context_sidecar": pos_sidecar,
        "meaning_summary_sidecar": meaning_sidecar, "component_match_audit": match_audit,
        "cross_contract_comparison_audit": comparison_audit, "target_layer_audit": target_layer_audit,
        "denominator_separation_audit": denominator_audit, "measurement_separation_audit": measurement_audit,
        "packet_exclusion_audit": pd.DataFrame(), "certification_audit": cert_audit, "certification_rejection_audit": rejection_audit,
        "forbidden_inference_audit": pd.DataFrame(), "input_scope_audit": scope_audit, "registry_contract_audit": registry_audit,
        "input_contract_report": {"run_id": run_id, "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3", "required_inputs_status": "PASS", "v550j_input_contract_status": "VALIDATED_V550J_PATTERN_CONTRACT", "registry_contract_status": registry_audit.iloc[0]["registry_contract_status"], "v551_field_mapping": {}, "deprecated_v552_inputs_supplied": deprecated_v552_inputs_supplied},
        "packet_contract_validation_report": validation_report.iloc[0].to_dict(), "readiness_report": readiness_report,
        "input_provenance_manifest": {"run_id": run_id, "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3", "registry_path": str(registry_path), "registry_hash": registry_hash, "input_hashes": input_hashes, "v550j_manifest_hash": manifest_hash, "v550j_readiness_report_hash": readiness_hash, "row_counts": {"v551_atoms": int(len(atoms)), "v550j_pattern_index": int(len(pattern_index)), "v550j_pattern_item_index": int(len(pattern_item_index)), "v550j_relation_signature": int(len(relation_signature)), "candidate": int(len(candidate)), "component": int(len(component_df)), "certified": certified_count}, "final_status": final_status},
    }
