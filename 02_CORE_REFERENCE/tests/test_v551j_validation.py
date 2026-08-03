from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v551j_schema import V551J_PACKET_CANDIDATE_TRACE_SCHEMA, V551J_REVIEW_SURFACE_SCHEMA
from data.ddm_build_copy.ddm_v551j_validation import (
    validate_authority_statuses,
    validate_candidate_trace_schema,
    validate_directionality_statuses,
    validate_forbidden_claim_ids,
    validate_no_actor_orientation_fields,
    validate_no_carrier_mediation_fields,
    validate_no_enneagram_fields,
    validate_no_runtime_safe_packets_in_phase_a,
    validate_packet_lifecycle_statuses,
    validate_review_surface_schema,
    validate_runtime_use_classes,
)


def _base_frame() -> pd.DataFrame:
    row = {column: "" for column in V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"]}
    row.update(
        {
            "packet_status": "candidate",
            "runtime_use_class": "not_runtime_consumable",
            "authority_status": "unknown",
            "directionality_status": "unknown",
            "forbidden_claim_ids_json": '["do_not_render_as_actor_orientation"]',
            "future_target_affordances_json": '["structural_context_support"]',
            "person_level_allowed": False,
            "household_level_allowed": False,
            "carrier_level_allowed": False,
            "structural_level_only": True,
            "temporal_level_allowed": False,
            "requires_temporalization": True,
            "requires_household_mediation": False,
            "requires_carrier_mediation": False,
            "requires_orientation_resolution": True,
            "requires_pressureflow_mediation": True,
            "requires_enneagram_runtime": False,
            "v552_context_status": "not_supplied",
        }
    )
    return pd.DataFrame([row])


def test_validation_rejects_runtime_safe_packets():
    df = _base_frame()
    df.loc[0, "runtime_use_class"] = "runtime_safe_after_v553"
    assert validate_no_runtime_safe_packets_in_phase_a(df)


def test_validation_rejects_downstream_leakage_fields():
    df = _base_frame().copy()
    df["parent_orientation"] = "x"
    assert validate_no_actor_orientation_fields(df)
    df = _base_frame().copy()
    df["carrier_language"] = "x"
    assert validate_no_carrier_mediation_fields(df)
    df = _base_frame().copy()
    df["enneagram_type"] = "x"
    assert validate_no_enneagram_fields(df)


def test_validation_rejects_bad_enums_and_claims():
    df = _base_frame().copy()
    df.loc[0, "packet_status"] = "certified"
    df.loc[0, "runtime_use_class"] = "runtime_safe_after_v552j"
    df.loc[0, "authority_status"] = "bogus"
    df.loc[0, "directionality_status"] = "bogus"
    df.loc[0, "forbidden_claim_ids_json"] = "[]"
    errors = validate_candidate_trace_schema(df)
    assert any("packet_status" in error for error in errors)
    assert any("runtime_use_class" in error for error in errors)
    assert any("authority_status" in error for error in errors)
    assert any("directionality_status" in error for error in errors)
    assert any("forbidden_claim_ids_json" in error for error in errors)


def test_validation_helpers_individual():
    df = _base_frame()
    assert not validate_packet_lifecycle_statuses(df)
    assert not validate_runtime_use_classes(df)
    assert not validate_authority_statuses(df)
    assert not validate_directionality_statuses(df)
    assert not validate_forbidden_claim_ids(df)


def test_review_surface_validation_requires_review_columns():
    row = {column: "" for column in V551J_REVIEW_SURFACE_SCHEMA["required_columns"]}
    row.update(_base_frame().iloc[0].to_dict())
    row.update(
        {
            "review_surface_status": "reviewable",
            "review_priority": "high",
            "certification_candidate": False,
            "review_reason_codes_json": "[]",
            "review_blockers_json": "[]",
            "review_notes_json": "[]",
            "v552_join_strength": "not_supplied",
            "v552_structural_channel_refs_json": "[]",
            "v552_relation_axis_pressure_refs_json": "[]",
            "v552_target_entity_pressure_refs_json": "[]",
            "v552_driver_facet_pressure_refs_json": "[]",
            "v552_contradiction_refs_json": "[]",
            "v552_horizon_constraint_refs_json": "[]",
            "v552_parent_prior_refs_json": "[]",
            "v551j_evidence_certification_status": "candidate",
            "v552_handoff_readiness": "not_ready_v552_context_missing",
            "v552_handoff_blockers_json": '["v552_context_missing"]',
            "certification_blockers_json": "[]",
            "required_for_certification_json": "[]",
            "evidence_quality_status": "reviewable_evidence",
            "use_permission_class": "review_only",
        }
    )
    for column in (
        "support_score_numeric",
        "confidence_score_numeric",
        "authority_score_numeric",
        "directionality_score_numeric",
        "join_strength_score_numeric",
        "semantic_specificity_score_numeric",
        "evidence_completeness_score_numeric",
        "certifiability_score_numeric",
        "review_priority_score_numeric",
    ):
        row[column] = 0.0
    df = pd.DataFrame([row])
    errors = validate_review_surface_schema(df)
    assert not errors

