#!/usr/bin/env python3
"""Schema and enum definitions for V551J candidate evidence packets."""

from __future__ import annotations

from typing import Any

import pandas as pd

V551J_SCHEMA_VERSION = "v2.2.3"
V551J_COMPILER_VERSION = "v551j_joint_evidence_contract_v2_2_3"

V551J_PACKET_STATUSES = {
    "candidate",
    "review",
    "certified",
    "diagnostic",
    "blocked",
    "unknown",
}

V551J_RUNTIME_USE_CLASSES = {
    "not_runtime_consumable",
    "structural_context_only",
    "temporalization_required",
    "household_mediation_required",
    "carrier_mediation_required",
    "orientation_resolution_required",
    "pressureflow_mediation_required",
    "runtime_safe_after_v552j",
    "runtime_safe_after_v553",
    "debug_only",
}

V551J_AUTHORITY_STATUSES = {
    "exact_registry",
    "regex_registry",
    "prefix_registry",
    "semantic_role",
    "computed_context",
    "fallback",
    "manual_review",
    "unknown",
    "not_applicable",
}

V551J_DIRECTIONALITY_STATUSES = {
    "known_directional",
    "partial_directionality",
    "undirected_association",
    "conflicting_directionality",
    "not_applicable",
    "unknown",
}

V551J_PACKET_TYPES = {
    "joint_relation_evidence_packet",
    "joint_pattern_context_packet",
    "conditional_support_packet",
    "contradiction_candidate_packet",
    "known_absence_packet",
}

V551J_FUTURE_TARGET_AFFORDANCES = {
    "temporal_pressure_support",
    "stratum_relation_support",
    "structural_context_support",
    "joint_morphology_support",
    "contradiction_rupture_support",
    "carrier_mediation_possible",
    "household_mediation_possible",
    "orientation_resolution_required",
    "expectation_seed_possible",
    "striving_affordance_possible",
    "pressureflow_mediation_required",
    "horizon_relation_possible",
    "runtime_forbidden",
    "diagnostic_only",
    "review_only",
}

V551J_FORBIDDEN_CLAIM_IDS = [
    "do_not_render_as_person_belief",
    "do_not_render_as_parent_trait",
    "do_not_render_as_child_memory",
    "do_not_render_as_causal_relation",
    "do_not_render_as_enneagram_type",
    "do_not_render_as_household_biography",
    "do_not_render_as_countrywide_personality",
    "do_not_render_as_carrier_membership",
    "do_not_render_as_actor_orientation",
    "do_not_render_as_temporal_field",
    "do_not_render_as_runtime_psyche",
]

V551J_REQUIRED_FUTURE_LAYER_TARGETS = [
    "v552j",
]

V551J_REVIEW_SURFACE_STATUSES = {
    "reviewable",
    "reviewable_with_context_gap",
    "reviewable_with_directionality_gap",
    "reviewable_with_authority_gap",
    "diagnostic_only",
    "blocked",
}

V551J_REVIEW_PRIORITIES = {
    "high",
    "medium",
    "low",
    "diagnostic",
}

V551J_EVIDENCE_QUALITY_STATUSES = {
    "certifiable",
    "reviewable_evidence",
    "diagnostic_only",
    "blocked_unsupported",
}

V551J_USE_PERMISSION_CLASSES = {
    "structural_context_only",
    "review_only",
    "diagnostic_only",
    "blocked",
    "not_runtime_consumable",
}

V551J_PACKET_CANDIDATE_TRACE_SCHEMA = {
    "required_columns": [
        "run_id",
        "packet_id",
        "packet_type",
        "packet_status",
        "source_layer",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "created_at",
        "schema_version",
        "compiler_version",
        "input_atom_ids_json",
        "input_pattern_ids_json",
        "input_meaning_summary_ids_json",
        "input_association_ids_json",
        "source_artifact_ids_json",
        "source_run_ids_json",
        "family_ids_json",
        "question_ids_json",
        "variable_codes_json",
        "response_family_json",
        "relation_axis_ids_json",
        "target_entity_ids_json",
        "driver_facet_ids_json",
        "strata_relevance_json",
        "strata_path_json",
        "semantic_roles_json",
        "semantic_tags_json",
        "support_n_unweighted",
        "support_n_weighted",
        "support_score",
        "prevalence_score",
        "confidence_tier",
        "support_status",
        "support_gate_status",
        "evidence_stratum",
        "evidence_stratum_v2",
        "authority_status",
        "authority_basis",
        "authority_source_fields_json",
        "directionality_status",
        "directionality_basis",
        "directionality_coverage_status",
        "pattern_count",
        "pattern_support_n_unweighted",
        "pattern_support_status",
        "boundary_pattern_type",
        "target_structure_status",
        "target_selectivity_profile",
        "meaning_summary_status",
        "meaning_summary_confidence",
        "meaning_summary_warning_flags_json",
        "association_context_status",
        "association_publication_status",
        "association_lane",
        "association_lane_status",
        "association_lane_authority_source",
        "association_lane_publishability",
        "top_publishable_attitude_associations_json",
        "top_reviewable_attitude_signals_json",
        "top_identity_context_signals_json",
        "top_position_context_signals_json",
        "top_family_background_signals_json",
        "top_unknown_or_diagnostic_signals_json",
        "runtime_use_class",
        "future_target_affordances_json",
        "allowed_future_targets_json",
        "forbidden_future_targets_json",
        "person_level_allowed",
        "household_level_allowed",
        "carrier_level_allowed",
        "structural_level_only",
        "temporal_level_allowed",
        "requires_temporalization",
        "requires_household_mediation",
        "requires_carrier_mediation",
        "requires_orientation_resolution",
        "requires_pressureflow_mediation",
        "requires_enneagram_runtime",
        "known_absences_json",
        "forbidden_claim_ids_json",
        "review_required",
        "diagnostic_only_reason",
        "blocked_reason",
        "v552_context_status",
        "v552_question_semantic_hierarchy_join_status",
        "v552_contradiction_context_status",
        "v552_parent_prior_context_status",
        "v552_structural_refs_json",
    ]
}

V551J_PACKET_EXCLUSION_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "candidate_source",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "family_id",
        "pattern_id",
        "atom_id",
        "question_id",
        "var_code",
        "exclusion_reason",
        "exclusion_stage",
        "severity",
        "would_have_packet_type",
        "required_downstream_layer",
        "created_at",
        "schema_version",
    ]
}

V551J_JOIN_KEY_DIAGNOSTICS_SCHEMA = {
    "required_columns": [
        "run_id",
        "table_name",
        "path",
        "row_count",
        "column_count",
        "columns_json",
        "required_columns_present_json",
        "required_columns_missing_json",
        "candidate_join_keys_json",
        "join_strategy",
        "join_status",
        "join_warning",
        "created_at",
        "schema_version",
    ]
}

V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "packet_id",
        "packet_type",
        "forbidden_claim_id",
        "risk_description",
        "upstream_basis",
        "safe_alternative",
        "applies_to_future_layer",
        "severity",
        "created_at",
        "schema_version",
    ]
}

V551J_INPUT_PROVENANCE_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "compiler",
        "compiler_version",
        "created_at",
        "input_paths",
        "input_hashes",
        "input_row_counts",
        "input_column_counts",
        "optional_inputs_supplied",
        "optional_inputs_missing",
        "output_paths",
        "schema_version",
        "final_status",
    ]
}

V551J_PACKET_READINESS_REPORT_SCHEMA = {
    "required_columns": [
        "run_id",
        "candidate_packet_rows",
        "exclusion_audit_rows",
        "forbidden_inference_audit_rows",
        "join_diagnostic_rows",
        "packet_type_counts",
        "packet_status_counts",
        "runtime_use_class_counts",
        "authority_status_counts",
        "directionality_status_counts",
        "future_target_affordance_counts",
        "person_level_allowed_count",
        "household_level_allowed_count",
        "carrier_level_allowed_count",
        "structural_level_only_count",
        "requires_temporalization_count",
        "requires_household_mediation_count",
        "requires_carrier_mediation_count",
        "requires_orientation_resolution_count",
        "requires_pressureflow_mediation_count",
        "requires_enneagram_runtime_count",
        "v552_context_status",
        "known_absence_counts",
        "readiness_warnings",
        "certified_packet_index_written",
        "runtime_safe_packets_written",
        "final_status",
        "created_at",
        "schema_version",
    ]
}

V551J_REVIEW_SURFACE_SCHEMA = {
    "required_columns": list(dict.fromkeys([
        *V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"],
        "review_surface_status",
        "review_priority",
        "review_reason_codes_json",
        "review_blockers_json",
        "review_notes_json",
        "v552_join_strength",
        "v552_structural_channel_refs_json",
        "v552_relation_axis_pressure_refs_json",
        "v552_target_entity_pressure_refs_json",
        "v552_driver_facet_pressure_refs_json",
        "v552_contradiction_refs_json",
        "v552_horizon_constraint_refs_json",
        "v552_parent_prior_refs_json",
        "support_score_numeric",
        "confidence_score_numeric",
        "authority_score_numeric",
        "directionality_score_numeric",
        "join_strength_score_numeric",
        "semantic_specificity_score_numeric",
        "evidence_completeness_score_numeric",
        "certifiability_score_numeric",
        "review_priority_score_numeric",
        "score_provenance_json",
        "evidence_quality_status",
        "use_permission_class",
        "sidecar_lane",
        "sidecar_role",
        "certification_candidate",
        "v551j_evidence_certification_status",
        "v551j_evidence_certification_status_input",
        "normalized_v551j_lane",
        "normalized_v551j_certification_status",
        "normalized_v551j_review_status",
        "normalized_authority_status",
        "normalized_directionality_status",
        "normalized_support_status",
        "normalized_v552_context_status",
        "normalized_comparability_status",
        "permission_class",
        "constraint_eligibility",
        "context_eligibility",
        "forensic_eligibility",
        "blocked_from_downstream",
        "status_conflict_flag",
        "status_conflict_reason",
        "v552_handoff_readiness",
        "v552_handoff_blockers_json",
        "certification_blockers_json",
        "required_for_certification_json",
    ])),
}

V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA = {
    "required_columns": list(dict.fromkeys([
        "run_id",
        "packet_id",
        "packet_type",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "input_atom_ids_json",
        "input_pattern_ids_json",
        "input_meaning_summary_ids_json",
        "input_association_ids_json",
        "source_artifact_ids_json",
        "source_run_ids_json",
        "family_ids_json",
        "question_ids_json",
        "variable_codes_json",
        "relation_axis_ids_json",
        "target_entity_ids_json",
        "driver_facet_ids_json",
        "semantic_roles_json",
        "semantic_tags_json",
        "support_n_unweighted",
        "support_n_weighted",
        "support_status",
        "support_gate_status",
        "confidence_tier",
        "authority_status",
        "directionality_status",
        "review_surface_status",
        "review_priority",
        "review_reason_codes_json",
        "certification_blockers_json",
        "v551j_evidence_certification_status",
        "normalized_v551j_lane",
        "normalized_v551j_certification_status",
        "normalized_v551j_review_status",
        "normalized_authority_status",
        "normalized_directionality_status",
        "normalized_support_status",
        "normalized_v552_context_status",
        "normalized_comparability_status",
        "permission_class",
        "constraint_eligibility",
        "context_eligibility",
        "forensic_eligibility",
        "blocked_from_downstream",
        "status_conflict_flag",
        "status_conflict_reason",
        "v552_context_status",
        "v552_handoff_readiness",
        "support_score_numeric",
        "confidence_score_numeric",
        "authority_score_numeric",
        "directionality_score_numeric",
        "join_strength_score_numeric",
        "semantic_specificity_score_numeric",
        "evidence_completeness_score_numeric",
        "certifiability_score_numeric",
        "review_priority_score_numeric",
        "score_provenance_json",
        "evidence_quality_status",
        "use_permission_class",
        "sidecar_lane",
        "sidecar_role",
        "sidecar_reason_codes_json",
        "forbidden_claim_ids_json",
        "runtime_use_class",
        "future_target_affordances_json",
        "known_absences_json",
        "normalized_v551j_lane",
        "normalized_v551j_certification_status",
        "normalized_v551j_review_status",
        "normalized_authority_status",
        "normalized_directionality_status",
        "normalized_support_status",
        "normalized_v552_context_status",
        "normalized_comparability_status",
        "permission_class",
        "constraint_eligibility",
        "context_eligibility",
        "forensic_eligibility",
        "blocked_from_downstream",
        "status_conflict_flag",
        "status_conflict_reason",
        "created_at",
        "schema_version",
    ])),
}

V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "candidate_source",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "packet_id",
        "packet_type",
        "review_surface_status",
        "review_priority",
        "review_reason_code",
        "review_blocker_code",
        "required_downstream_layer",
        "created_at",
        "schema_version",
    ]
}

V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "table_name",
        "path",
        "row_count",
        "column_count",
        "columns_json",
        "required_columns_present_json",
        "required_columns_missing_json",
        "candidate_join_keys_json",
        "join_strategy",
        "join_status",
        "join_warning",
        "created_at",
        "schema_version",
    ]
}

V551J_REVIEW_READINESS_REPORT_SCHEMA = {
    "required_columns": [
        "run_id",
        "review_candidate_rows",
        "review_surface_rows",
        "review_exclusion_rows",
        "v552_context_join_rows",
        "review_surface_status_counts",
        "review_priority_counts",
        "v552_context_status_counts",
        "authority_gap_rows",
        "directionality_gap_rows",
        "context_gap_rows",
        "blocked_rows",
        "diagnostic_only_rows",
        "certification_candidate_rows",
        "v551j_evidence_certification_candidate_rows",
        "v551j_evidence_certification_status_counts",
        "v552_handoff_readiness_counts",
        "v552_handoff_blocker_counts",
        "certification_blocker_counts",
        "final_status",
        "created_at",
        "schema_version",
    ]
}

V551J_CERTIFIED_PACKET_INDEX_SCHEMA = {
    "required_columns": [
        *V551J_REVIEW_SURFACE_SCHEMA["required_columns"],
        "certification_status",
        "certification_basis_json",
        "certification_gate_results_json",
        "status_resolution_provenance_json",
        "certified_at",
        "certification_schema_version",
        "directionality_limited",
    ]
}

V551J_CERTIFICATION_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "packet_id",
        "packet_type",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "gate_identity_pass",
        "gate_lifecycle_pass",
        "gate_authority_pass",
        "gate_support_pass",
        "gate_directionality_pass",
        "gate_forbidden_claims_pass",
        "gate_mediation_flags_pass",
        "gate_no_downstream_leakage_pass",
        "certified",
        "certification_blockers_json",
        "certification_notes_json",
        "created_at",
        "schema_version",
    ]
}

V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "packet_id",
        "packet_type",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "certification_blocker_code",
        "certification_blocker_detail",
        "gate_identity_pass",
        "gate_lifecycle_pass",
        "gate_authority_pass",
        "gate_support_pass",
        "gate_directionality_pass",
        "gate_forbidden_claims_pass",
        "gate_mediation_flags_pass",
        "gate_no_downstream_leakage_pass",
        "created_at",
        "schema_version",
    ]
}

V551J_CERTIFICATION_READINESS_REPORT_SCHEMA = {
    "required_columns": [
        "run_id",
        "review_surface_rows",
        "certified_packet_rows",
        "rejection_rows",
        "gate_identity_pass_rows",
        "gate_lifecycle_pass_rows",
        "gate_authority_pass_rows",
        "gate_support_pass_rows",
        "gate_directionality_pass_rows",
        "gate_forbidden_claims_pass_rows",
        "gate_mediation_flags_pass_rows",
        "gate_no_downstream_leakage_pass_rows",
        "certification_status_counts",
        "v552_context_status_counts",
        "evidence_certification_status_counts",
        "authority_status_counts",
        "directionality_status_counts",
        "review_surface_status_counts",
        "final_status",
        "created_at",
        "schema_version",
    ]
}


def _normalize_tokens(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("[") and text.endswith("]"):
            try:
                parsed = pd.read_json(text, typ="series")
                return [str(item) for item in parsed.tolist()]
            except Exception:
                pass
        return [part.strip() for part in text.split("|") if part.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


V551J_V2_HASH_NAMESPACES = {
    "packet_identity": "v551j_packet_identity_v2",
    "joint_response_identity": "v551j_joint_response_identity_v2",
    "joint_semantic_signature": "v551j_joint_semantic_signature_v2",
    "joint_orientation_signature": "v551j_joint_orientation_signature_v2",
    "joint_topology_signature": "v551j_joint_topology_signature_v2",
    "joint_target_signature": "v551j_joint_target_signature_v2",
    "joint_structural_signature": "v551j_joint_structural_signature_v2",
    "joint_measurement_contract": "v551j_joint_measurement_contract_v2",
    "packet_contract": "v551j_packet_contract_v2",
    "component_match": "v551j_component_match_v2",
}

V551J_V2_COMPONENT_MATCH_STATUSES = {
    "MATCHED_EXACT_V551_ATOM",
    "MATCHED_EQUIVALENT_DUPLICATE_V551_ATOM",
    "AMBIGUOUS_V551_ATOM_MATCH",
    "UNMATCHED_SPECIAL_OR_MISSING_RESPONSE",
    "UNMATCHED_V551_RELATION_INELIGIBLE",
    "MISSING_V551_ATOM_UNEXPLAINED",
}

V551J_V2_CROSS_CONTRACT_STATUSES = {
    "CROSS_CONTRACT_CONSISTENT",
    "CROSS_CONTRACT_GAP",
    "CROSS_CONTRACT_RESPONSE_CONFLICT",
    "CROSS_CONTRACT_SEMANTIC_CONFLICT",
    "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT",
    "CROSS_CONTRACT_INTENSITY_CONFLICT",
    "CROSS_CONTRACT_STRUCTURAL_CONFLICT",
    "CROSS_CONTRACT_AUTHORITY_HASH_CONFLICT",
}

V551J_V2_JOINT_EVIDENCE_CLASSES = {
    "joint_directional_relation_observation",
    "joint_mixed_directional_relation_observation",
    "joint_relation_observation_with_context_components",
    "joint_pattern_context_only",
    "known_absence",
    "blocked_joint_pattern",
}

V551J_V2_CERTIFICATION_STATUSES = {
    "CERTIFIED_JOINT_RELATION_EVIDENCE",
    "CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT_COMPONENTS",
    "REVIEW_REQUIRED_JOINT_SEMANTIC_GAP",
    "REVIEW_REQUIRED_JOINT_DIRECTIONALITY_GAP",
    "REVIEW_REQUIRED_JOINT_TARGET_PARTITION",
    "REVIEW_REQUIRED_JOINT_STRUCTURAL_GAP",
    "REVIEW_REQUIRED_JOINT_MEASUREMENT_GAP",
    "DIAGNOSTIC_JOINT_PATTERN_CONTEXT",
    "BLOCKED_AMBIGUOUS_COMPONENT_MATCH",
    "BLOCKED_CROSS_CONTRACT_CONFLICT",
    "BLOCKED_INSUFFICIENT_JOINT_COMPONENTS",
    "BLOCKED_REGISTRY_OR_SCOPE_CONFLICT",
    "BLOCKED_MALFORMED_PATTERN_CONTRACT",
}

V551J_V2_FORBIDDEN_FUTURE_TARGETS = [
    "v553",
    "v554",
    "v555",
    "v556",
    "runtime_person",
    "runtime_household",
    "runtime_carrier",
    "runtime_orientation",
    "runtime_psyche",
]

V551J_V2_FORBIDDEN_CLAIM_IDS = V551J_FORBIDDEN_CLAIM_IDS + [
    "do_not_render_as_structural_pressure",
    "do_not_render_as_temporal_pressure",
    "do_not_render_as_contradiction",
    "do_not_render_as_rupture",
    "do_not_render_as_trajectory",
    "do_not_render_as_causal_joint_effect",
    "do_not_render_association_as_joint_pattern_support",
]

V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA = {
    "required_columns": [
        "run_id", "packet_id", "packet_contract_hash", "pattern_id", "family_id", "family_label", "family_type", "family_structure_type",
        "source", "source_family", "wave", "canonical_wave", "country_code", "survey_year", "created_at", "schema_version", "compiler_version",
        "v551_schema_version", "v551_input_artifact_hash", "v550j_schema_version", "v550j_manifest_hash", "v550j_readiness_report_hash",
        "question_family_registry_path", "question_family_registry_hash", "question_family_registry_status", "v550j_input_contract_status",
        "pattern_item_count", "matched_relation_component_count", "matched_context_component_count", "special_or_missing_component_count",
        "unmatched_explained_component_count", "unmatched_unexplained_component_count", "ambiguous_component_count", "cross_contract_conflict_count",
        "component_contract_complete", "component_order_integrity_status", "component_match_status_summary_json", "matched_atom_ids_json",
        "matched_atom_contract_hashes_json", "joint_response_identity_signature", "joint_semantic_signature", "joint_orientation_signature",
        "joint_topology_signature", "joint_target_signature", "joint_structural_signature", "joint_measurement_contract_hash",
        "component_contract_hashes_ordered_json", "component_response_vector_json", "component_semantic_vector_json", "component_orientation_vector_json",
        "component_topology_vector_json", "component_target_vector_json", "component_structural_vector_json", "joint_pattern_count_unweighted",
        "joint_pattern_count_weighted", "joint_probability_unweighted", "joint_probability_weighted", "joint_probability_basis", "joint_probability",
        "joint_n_unweighted", "joint_n_weighted", "joint_weighted_count_basis", "joint_support_threshold", "joint_support_ratio",
        "joint_support_ratio_margin", "joint_support_score", "joint_support_status", "joint_support_gate_status", "joint_prevalence_score",
        "joint_completion_rate", "joint_missingness_rate", "joint_effective_n", "joint_effective_n_ratio", "joint_confidence_score",
        "joint_weight_status", "joint_measurement_status", "joint_evidence_class", "joint_semantic_authority_status",
        "joint_directionality_authority_status", "joint_target_authority_status", "joint_structural_authority_status",
        "joint_measurement_authority_status", "joint_evidence_authority_status", "semantic_conflict_status", "target_structure_status",
        "expected_multi_target", "target_resolution_coverage", "mapping_coverage", "certification_status", "review_required",
        "review_reason_codes_json", "blocking_reason_codes_json", "ready_for_v552j_joint_evidence", "ready_for_v553",
        "pressure_anchor_eligible", "temporal_pressure_authorized", "runtime_use_class", "allowed_future_targets_json",
        "forbidden_future_targets_json", "forbidden_claim_ids_json", "known_absences_json",
        "compatibility_projection_only", "not_authoritative_v2_artifact",
    ]
}

V551J_JOINT_COMPONENT_INDEX_SCHEMA = {
    "required_columns": [
        "run_id", "packet_id", "pattern_id", "family_id", "item_order", "component_id", "component_contract_hash",
        "source", "source_family", "canonical_wave", "country_code", "v550j_item_var_code", "v550j_item_question_id",
        "v550j_item_role", "v550j_item_condition_label", "v550j_item_response_value_normalized", "v550j_item_response_label",
        "v550j_item_normalized_response_label", "v550j_item_response_direction", "v550j_item_response_intensity", "v550j_item_polarity",
        "v550j_item_directionality_authority_status", "v550j_item_directionality_authority_source", "v550j_item_response_semantics_authority_status",
        "v550j_item_response_semantics_contract_hash", "v550j_item_semantic_response_role", "v550j_item_semantic_role_authority_status",
        "v550j_item_driver_id", "v550j_item_driver_facet_id", "v550j_item_relation_axis_id", "v550j_item_target_entity_id",
        "v550j_item_target_domain", "v550j_item_target_condition_label", "v550j_item_target_group_label", "v550j_item_permission_domain",
        "v550j_item_target_resolution_grain", "v550j_item_target_resolution_status", "v550j_item_mapping_status", "v550j_item_semantic_role",
        "v550j_item_v551_evidence_role", "v551_atom_match_status", "v551_atom_match_basis", "v551_atom_id", "v551_atom_contract_hash",
        "v551_empirical_object_type", "v551_empirical_object_id", "v551_response_value_normalized", "v551_normalized_response_label",
        "v551_semantic_response_role", "v551_response_direction", "v551_response_direction_status", "v551_response_intensity",
        "v551_response_intensity_status", "v551_polarity", "v551_response_scale_signature", "v551_semantic_identity_signature",
        "v551_structural_identity_signature", "v551_measurement_contract_hash", "v551_pressure_evidence_class",
        "v551_v552_pressure_component_status", "v551_temporal_pressure_indicator_authorized", "v551_evidence_basis",
        "v551_provenance_basis", "v551_forbidden_inference", "v551_known_absences", "question_identity_consistent",
        "response_identity_consistent", "semantic_role_consistent", "directionality_consistent", "intensity_consistent",
        "polarity_consistent", "relation_axis_consistent", "target_entity_consistent", "driver_facet_consistent",
        "structural_identity_consistent", "authority_hash_consistent", "cross_contract_status", "cross_contract_reason_codes_json",
        "component_evidence_role", "component_certification_contribution", "created_at", "schema_version", "compiler_version",
    ]
}

V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA = {
    "required_columns": [column for column in V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"] if column not in {"compatibility_projection_only", "not_authoritative_v2_artifact"}]
}

V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA = {
    "required_columns": [
        "run_id", "packet_id", "pattern_id", "family_id", "certification_status", "review_required", "review_priority",
        "review_reason_codes_json", "blocking_reason_codes_json", "joint_evidence_class", "ready_for_v552j_joint_evidence",
        "review_triage_priority_score", "created_at", "schema_version", "compiler_version",
    ]
}

V551J_PATTERN_CONTEXT_SIDECAR_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "family_id", "joint_evidence_class", "context_reason", "created_at", "schema_version", "compiler_version"]}
V551J_ASSOCIATION_CONTEXT_SIDECAR_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "family_id", "association_measurement_identity_json", "association_context_status", "created_at", "schema_version", "compiler_version"]}
V551J_POSITION_CONTEXT_SIDECAR_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "family_id", "position_context_json", "created_at", "schema_version", "compiler_version"]}
V551J_MEANING_SUMMARY_SIDECAR_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "family_id", "interpretive_metadata_json", "measurement_authority", "created_at", "schema_version", "compiler_version"]}
V551J_COMPONENT_MATCH_AUDIT_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "component_id", "item_order", "v551_atom_match_status", "v551_atom_match_basis", "candidate_atom_count", "effective_atom_count", "audit_reason_codes_json", "created_at", "schema_version", "compiler_version"]}
V551J_MEASUREMENT_SEPARATION_AUDIT_SCHEMA = {"required_columns": ["run_id", "pattern_id", "packet_id", "pattern_measurement_source", "association_measurements_present", "association_measurements_used_in_core_packet", "atom_measurements_used_as_pattern_measurements", "measurement_contract_hash", "measurement_separation_status", "violations_json", "created_at", "schema_version", "compiler_version"]}
V551J_INPUT_SCOPE_AUDIT_SCHEMA = {"required_columns": ["run_id", "artifact_name", "source_family_values_json", "canonical_wave_values_json", "country_code_values_json", "scope_contract_status", "row_count", "issue_codes_json", "created_at", "schema_version", "compiler_version"]}
V551J_INPUT_PROVENANCE_AUDIT_SCHEMA = {"required_columns": ["run_id", "artifact_name", "input_path", "size_bytes", "sha256", "exists", "hash_format_valid", "hash_matches_file", "expected_governed_hash", "governed_hash_matches", "scope_status", "created_at", "schema_version", "compiler_version"]}
V551J_REGISTRY_CONTRACT_AUDIT_SCHEMA = {"required_columns": ["run_id", "registry_path", "registry_hash", "v550j_manifest_registry_path", "v550j_manifest_registry_hash", "registry_contract_status", "created_at", "schema_version", "compiler_version"]}
V551J_PACKET_CONTRACT_VALIDATION_REPORT_SCHEMA = {"required_columns": ["run_id", "candidate_contract_valid", "component_contract_valid", "issue_count", "issues_json", "created_at", "schema_version", "compiler_version"]}
V551J_JOINT_READINESS_REPORT_SCHEMA = {"required_columns": ["run_id", "schema_version", "compiler_version", "source_family", "canonical_wave", "country_code", "input_pattern_count", "input_pattern_item_count", "candidate_packet_count", "component_row_count", "certified_packet_count", "certified_with_context_count", "review_required_packet_count", "context_only_packet_count", "blocked_packet_count", "ambiguous_component_count", "cross_contract_conflict_count", "measurement_separation_violation_count", "registry_contract_status", "scope_contract_status", "candidate_contract_valid", "component_contract_valid", "ready_for_review", "ready_for_v552j_joint_evidence", "ready_for_v553", "final_status", "blockers_json", "warnings_json", "created_at"]}


# Authoritative v2.2 contract constants. These supersede the transitional v2 constants above.
V551J_V22_SCHEMA_VERSION = "v2.2.3"
V551J_V22_COMPILER_VERSION = "v551j_joint_evidence_contract_v2_2_3"
V551J_SCHEMA_VERSION = V551J_V22_SCHEMA_VERSION
V551J_COMPILER_VERSION = V551J_V22_COMPILER_VERSION

V551J_V22_COMPARISON_STATUSES = {
    "EXACT_MATCH", "BOTH_MISSING", "ONE_SIDE_MISSING", "NOT_COMPARABLE_PARALLEL_CONTRACT", "CONFLICT", "NOT_EVALUATED",
}
V551J_V22_TARGET_LAYER_RELATION_STATUSES = {
    "PARALLEL_GOVERNED_TARGET_LAYERS", "EXPLICIT_SAME_NAMESPACE_MATCH", "EXPLICIT_SAME_NAMESPACE_CONFLICT",
    "FAMILY_TARGET_CONTRACT_GAP", "STRUCTURAL_TARGET_CONTRACT_GAP", "BOTH_TARGET_CONTRACTS_MISSING",
}
V551J_V22_CROSS_CONTRACT_STATUSES = {
    "CROSS_CONTRACT_CONSISTENT", "CROSS_CONTRACT_GAP", "CROSS_CONTRACT_RESPONSE_CONFLICT",
    "CROSS_CONTRACT_SEMANTIC_CONFLICT", "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT",
    "CROSS_CONTRACT_SOURCE_INTENSITY_CONFLICT", "CROSS_CONTRACT_SHARED_STRUCTURAL_CONFLICT",
    "CROSS_CONTRACT_EXPLICIT_TARGET_CONFLICT",
}
V551J_V22_CERTIFICATION_STATUSES = {
    "CERTIFIED_JOINT_RELATION_EVIDENCE", "CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT",
    "REVIEW_REQUIRED_AUTHORITY_GAP", "REVIEW_REQUIRED_COMPONENT_GAP", "CONTEXT_ONLY_PATTERN",
    "BLOCKED_AMBIGUOUS_COMPONENT_MATCH", "BLOCKED_CROSS_CONTRACT_CONFLICT", "BLOCKED_INPUT_CONTRACT",
    "BLOCKED_PACKET_CONTRACT",
}
V551J_V22_FORBIDDEN_FUTURE_TARGETS = ["v553", "v554", "v555", "v556", "runtime_person", "runtime_household", "runtime_carrier", "runtime_orientation", "runtime_psyche"]
V551J_V22_FORBIDDEN_CLAIM_IDS = V551J_V2_FORBIDDEN_CLAIM_IDS

V551J_V22_COMPONENT_INDEX_COLUMNS = [
    "run_id", "packet_id", "pattern_id", "family_id", "item_order", "component_id", "component_contract_hash",
    "source", "source_family", "canonical_wave", "country_code", "v550j_item_var_code", "v550j_item_question_id",
    "v551_var_code", "v551_question_id",
    "v550j_item_role", "v550j_item_condition_label", "v550j_item_response_value_normalized", "v550j_item_response_label",
    "v550j_item_normalized_response_label", "v550j_item_semantic_response_role", "v550j_joint_response_stance",
    "v551_evidence_role", "v551_evidence_role_status", "joint_response_stance_alignment_status", "v550j_item_response_direction",
    "v550j_item_response_intensity", "v550j_item_polarity", "v550j_semantic_polarity_label",
    "v551_source_polarity_coordinate", "v550j_item_response_semantics_contract_hash",
    "v550j_item_directionality_authority_status", "v550j_item_directionality_authority_source",
    "v550j_family_target_entity_id", "v550j_target_domain", "v550j_target_condition_label", "v550j_target_group_label",
    "v550j_permission_domain", "v550j_target_resolution_grain", "v550j_target_resolution_status", "v550j_target_resolution_authority_source",
    "v550j_driver_id", "v550j_driver_facet_id", "v550j_relation_axis_id",
    "v551_atom_match_status", "v551_atom_match_basis", "v551_atom_id", "v551_atom_contract_hash", "v551_measurement_contract_hash",
    "v551_empirical_object_type", "v551_empirical_object_id", "v551_empirical_distribution_id",
    "v551_response_value_raw", "v551_response_value_normalized", "v551_response_label", "v551_normalized_response_label", "v551_response_family",
    "v551_semantic_response_role", "v551_response_semantics_contract_hash", "v551_response_direction", "v551_response_direction_status", "v551_response_intensity", "v551_response_intensity_status",
    "v551_observed_response_zero", "v551_polarity", "v551_ordinal_rank", "v551_scale_min", "v551_scale_max", "v551_scale_direction",
    "v551_directionality_policy", "v551_response_topology", "v551_response_scale_signature",
    "v551_n_unweighted", "v551_n_respondents", "v551_n_weighted", "v551_pct_unweighted", "v551_pct_weighted", "v551_population_share",
    "v551_weight_status", "v551_support_score", "v551_prevalence_score",
    "v551_driver_id", "v551_driver_facet_id", "v551_relation_axis_id", "v551_structural_target_entity_id", "v551_strata_path",
    "v551_subject_position_signature", "v551_semantic_identity_signature", "v551_structural_identity_signature", "v551_structural_mapping_status",
    "v551_semantic_role_authority_status", "v551_response_semantics_authority_status", "v551_directionality_authority_status",
    "v551_directional_certification_status", "v551_allowed_as_v551_relation_evidence", "v551_allowed_as_temporal_pressure_indicator",
    "v551_temporal_authority_status", "v551_v552_pressure_component_eligible", "v551_v552_pressure_component_status",
    "v551_v552_pressure_component_ineligibility_reason", "v551_evidence_basis", "v551_evidence_basis_origin", "v551_provenance_basis",
    "v551_provenance_basis_origin", "v551_forbidden_inference", "v551_known_absences",
    "question_identity_status", "var_code_status", "response_identity_status", "normalized_response_label_status",
    "semantic_response_role_status", "response_direction_status", "response_intensity_status",
    "semantic_polarity_status", "source_polarity_representation_status", "polarity_status",
    "response_semantics_hash_status", "driver_id_status", "driver_facet_id_status", "relation_axis_id_status",
    "family_target_contract_status", "structural_target_contract_status", "target_layer_relation_status", "cross_contract_status",
    "cross_contract_reason_codes_json", "comparison_value_audit_json", "component_evidence_role", "component_certification_contribution",
    "component_v552_linkage_class", "created_at", "schema_version", "compiler_version",
]
V551J_V22_COMPONENT_INDEX_SCHEMA = {"required_columns": V551J_V22_COMPONENT_INDEX_COLUMNS}
V551J_JOINT_COMPONENT_INDEX_SCHEMA = V551J_V22_COMPONENT_INDEX_SCHEMA

V551J_V22_PACKET_COLUMNS = [
    "run_id", "packet_id", "packet_contract_hash", "pattern_id", "family_id", "family_label", "family_type", "family_structure_type",
    "source", "source_family", "wave", "canonical_wave", "country_code", "survey_year", "created_at", "schema_version", "compiler_version",
    "boundary_pattern_type", "target_structure_status",
    "v551_schema_version", "v551_input_artifact_hash", "v550j_pattern_index_artifact_hash", "v550j_pattern_item_index_artifact_hash",
    "v550j_relation_signature_artifact_hash", "v550j_schema_version", "v550j_manifest_hash", "v550j_readiness_report_hash",
    "question_family_registry_path", "question_family_registry_hash", "question_family_registry_status",
    "pattern_item_count", "matched_relation_component_count", "matched_context_component_count", "special_or_missing_component_count",
    "unmatched_explained_component_count", "unmatched_unexplained_component_count", "ambiguous_component_count", "cross_contract_conflict_count",
    "component_contract_complete", "component_order_integrity_status", "matched_atom_ids_json", "matched_atom_contract_hashes_json",
    "matched_empirical_object_ids_json", "matched_empirical_distribution_ids_json", "distinct_matched_empirical_distribution_count",
    "component_question_denominator_nonnull_count", "component_question_denominator_null_count", "component_question_denominator_min",
    "component_question_denominator_max", "component_question_denominators_ordered_json", "denominator_separation_status",
    "v552_pressure_linkable_component_count", "v552_pressure_ineligible_component_count", "v552_pressure_review_required_component_count",
    "v552_pressure_linkage_status_summary_json", "joint_response_identity_signature", "joint_empirical_distribution_signature", "joint_semantic_signature",
    "joint_orientation_signature", "joint_topology_signature", "joint_target_signature", "joint_structural_signature",
    "joint_component_measurement_signature", "joint_measurement_contract_hash", "component_contract_hashes_ordered_json",
    "component_measurement_contract_hashes_ordered_json", "component_empirical_object_ids_ordered_json", "component_empirical_distribution_ids_ordered_json",
    "component_response_vector_json", "component_semantic_vector_json", "component_orientation_vector_json", "component_topology_vector_json",
    "component_target_vector_json", "component_structural_vector_json", "component_denominator_vector_json", "component_pressure_linkage_vector_json",
    "joint_pattern_count_unweighted", "joint_pattern_count_weighted", "joint_probability_unweighted", "joint_probability_weighted", "joint_probability_basis",
    "joint_probability", "joint_n_unweighted", "joint_n_weighted", "joint_weighted_count_basis", "joint_support_threshold", "joint_support_ratio",
    "joint_support_ratio_margin", "joint_support_score", "joint_support_status", "joint_support_gate_status", "joint_prevalence_score",
    "joint_completion_rate", "joint_missingness_rate", "joint_effective_n", "joint_effective_n_ratio", "joint_confidence_score", "joint_weight_status",
    "joint_measurement_status", "joint_evidence_class", "joint_semantic_authority_status", "joint_directionality_authority_status",
    "joint_family_target_authority_status", "joint_structural_authority_status", "joint_measurement_authority_status", "joint_evidence_authority_status",
    "semantic_conflict_status", "shared_structural_status", "family_target_status", "target_resolution_coverage", "mapping_coverage",
    "certification_status", "review_required", "review_reason_codes_json", "blocking_reason_codes_json", "ready_for_v552j_joint_evidence",
    "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized", "runtime_use_class",
    "allowed_future_targets_json", "forbidden_future_targets_json", "forbidden_claim_ids_json", "known_absences_json",
]
V551J_V22_PACKET_SCHEMA = {"required_columns": V551J_V22_PACKET_COLUMNS}
V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA = V551J_V22_PACKET_SCHEMA
V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA = V551J_V22_PACKET_SCHEMA

V551J_V22_REVIEW_SURFACE_SCHEMA = {"required_columns": [
    *V551J_V22_PACKET_COLUMNS,
    "review_priority",
    "review_triage_priority_score",
]}
V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA = V551J_V22_REVIEW_SURFACE_SCHEMA
V551J_CROSS_CONTRACT_COMPARISON_AUDIT_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "component_id", "item_order", "field_name", "v550j_value", "v551_value", "comparison_status", "issue_code", "created_at", "schema_version", "compiler_version"]}
V551J_TARGET_LAYER_AUDIT_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "component_id", "v550j_family_target_entity_id", "v551_structural_target_entity_id", "family_target_contract_status", "structural_target_contract_status", "target_layer_relation_status", "issue_code", "created_at", "schema_version", "compiler_version"]}
V551J_DENOMINATOR_SEPARATION_AUDIT_SCHEMA = {"required_columns": ["run_id", "packet_id", "pattern_id", "v551_empirical_distribution_id", "v551_n_respondents", "component_denominator_sum_used_as_joint_n", "component_denominator_substitution_detected", "component_denominator_equality_required_across_questions", "denominator_status", "issue_code", "created_at", "schema_version", "compiler_version"]}
