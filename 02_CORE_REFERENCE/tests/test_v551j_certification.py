from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v551j_certification import build_v551j_certified_packet_index
from data.ddm_build_copy.ddm_v551j_schema import V551J_REVIEW_SURFACE_SCHEMA


def _review_row() -> dict[str, object]:
    row = {column: "" for column in V551J_REVIEW_SURFACE_SCHEMA["required_columns"]}
    row.update(
        {
            "run_id": "run-1",
            "packet_id": "run-1__packet_0000001",
            "packet_type": "joint_relation_evidence_packet",
            "packet_status": "candidate",
            "source_layer": "v551j_candidate",
            "source": "GSS",
            "wave": "2002",
            "canonical_wave": "2002",
            "country_code": "US",
            "created_at": "2026-06-19T00:00:00Z",
            "schema_version": "v0.1",
            "compiler_version": "v551j_a_0.1",
            "input_atom_ids_json": '["atom-1"]',
            "input_pattern_ids_json": '["pattern-1"]',
            "input_meaning_summary_ids_json": '["pattern-1"]',
            "input_association_ids_json": '["assoc-1"]',
            "source_artifact_ids_json": '["source:GSS:2002:US"]',
            "source_run_ids_json": '["run-1"]',
            "family_ids_json": '["family-1"]',
            "question_ids_json": '["Q1"]',
            "variable_codes_json": '["VAR1"]',
            "response_family_json": '["yes_no"]',
            "relation_axis_ids_json": '["axis-1"]',
            "target_entity_ids_json": '["target-1"]',
            "driver_facet_ids_json": '["facet-1"]',
            "strata_relevance_json": '["high"]',
            "strata_path_json": '["path-1"]',
            "semantic_roles_json": '["RELATION_EVIDENCE"]',
            "semantic_tags_json": '["family"]',
            "support_n_unweighted": 10,
            "support_n_weighted": 10.0,
            "support_score": 0.9,
            "prevalence_score": 0.2,
            "confidence_tier": "high",
            "support_status": "sufficient_support",
            "support_gate_status": "sufficient",
            "evidence_stratum": "certified",
            "evidence_stratum_v2": "certified",
            "authority_status": "exact_registry",
            "authority_basis": "source_wave_country_family_pattern",
            "authority_source_fields_json": '["source","wave"]',
            "directionality_status": "known_directional",
            "directionality_basis": "known",
            "directionality_coverage_status": "covered",
            "pattern_count": 1,
            "pattern_support_n_unweighted": 10,
            "pattern_support_status": "supported",
            "boundary_pattern_type": "boundary",
            "target_structure_status": "structured",
            "target_selectivity_profile": "selective",
            "meaning_summary_status": "ready",
            "meaning_summary_confidence": "high",
            "meaning_summary_warning_flags_json": "[]",
            "association_context_status": "has_context",
            "association_publication_status": "publishable",
            "association_lane": "substantive_attitude_association",
            "association_lane_status": "registry_resolved",
            "association_lane_authority_source": "registry",
            "association_lane_publishability": "publishable_lane",
            "top_publishable_attitude_associations_json": "[]",
            "top_reviewable_attitude_signals_json": "[]",
            "top_identity_context_signals_json": "[]",
            "top_position_context_signals_json": "[]",
            "top_family_background_signals_json": "[]",
            "top_unknown_or_diagnostic_signals_json": "[]",
            "runtime_use_class": "not_runtime_consumable",
            "future_target_affordances_json": '["structural_context_support"]',
            "allowed_future_targets_json": '["v552j"]',
            "forbidden_future_targets_json": '["runtime_psyche"]',
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
            "known_absences_json": "[]",
            "forbidden_claim_ids_json": '["do_not_render_as_person_belief","do_not_render_as_causal_relation","do_not_render_as_runtime_psyche"]',
            "review_required": True,
            "diagnostic_only_reason": "",
            "blocked_reason": "",
            "v552_context_status": "reviewable_with_context_gap",
            "v552_question_semantic_hierarchy_join_status": "not_supplied",
            "v552_contradiction_context_status": "not_supplied",
            "v552_parent_prior_context_status": "not_supplied",
            "v552_structural_refs_json": "[]",
            "v551j_evidence_certification_status": "candidate",
            "v552_handoff_readiness": "not_ready_v552_context_missing",
            "v552_handoff_blockers_json": '["v552_context_missing"]',
            "review_surface_status": "reviewable_with_context_gap",
            "review_priority": "high",
            "review_reason_codes_json": '["v552_context_gap"]',
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
            "certification_candidate": False,
            "certification_blockers_json": "[]",
            "required_for_certification_json": "[]",
        }
    )
    return row


def test_certification_creates_index_for_valid_review_row():
    certified, audit, rejection, readiness = build_v551j_certified_packet_index(
        pd.DataFrame([_review_row()]),
        pd.DataFrame([_review_row()]),
        run_id="run-1",
    )
    assert len(certified) == 1
    assert len(audit) == 1
    assert rejection.empty
    assert certified.iloc[0]["certification_status"] == "certified"
    assert certified.iloc[0]["v551j_evidence_certification_status"] == "certified"
    assert certified.iloc[0]["v551j_evidence_certification_status_input"] == "candidate"
    assert "strict_certification_gates" in certified.iloc[0]["status_resolution_provenance_json"]
    assert certified.iloc[0]["status_conflict_flag"] is False or certified.iloc[0]["status_conflict_flag"] == False
    assert certified.iloc[0]["directionality_limited"] is False or certified.iloc[0]["directionality_limited"] == False
    assert readiness.iloc[0]["certified_packet_rows"] == 1
    assert readiness.iloc[0]["final_status"] == "READY_V551J_EVIDENCE_CERTIFIED_WITH_CONTEXT_GAPS"


def test_certification_rejects_invalid_authority():
    row = _review_row()
    row["authority_status"] = "unknown"
    certified, audit, rejection, readiness = build_v551j_certified_packet_index(
        pd.DataFrame([row]),
        pd.DataFrame([row]),
        run_id="run-1",
    )
    assert certified.empty
    assert len(audit) == 1
    assert len(rejection) == 1
    assert "authority" in rejection.iloc[0]["certification_blocker_code"]
    assert readiness.iloc[0]["certified_packet_rows"] == 0
