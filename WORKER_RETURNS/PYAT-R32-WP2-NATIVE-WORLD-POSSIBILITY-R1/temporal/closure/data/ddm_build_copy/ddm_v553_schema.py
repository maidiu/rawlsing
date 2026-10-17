#!/usr/bin/env python3
"""Schema definitions for the provisional V553 temporal pressure layer."""

from __future__ import annotations

from typing import Any

import pandas as pd

V553_SCHEMA_VERSION = "v0.2"
V553_COMPILER_VERSION = "v553_temporal_pressure_0.2_sparse"

V553_TEMPORAL_PRESSURE_FIELD_SCHEMA = {
    "required_columns": [
        "run_id",
        "layer",
        "wave",
        "canonical_wave",
        "source_wave_anchor",
        "source",
        "temporal_index",
        "temporal_year",
        "years_since_first_wave",
        "years_since_previous_wave",
        "temporal_scope",
        "pressure_status",
        "pressure_intensity",
        "pressure_intensity_band",
        "contradiction_pressure",
        "absence_pressure",
        "uncertainty_pressure",
        "shared_semantic_column_count",
        "shared_directionality_column_count",
        "shared_position_column_count",
        "v552j_readiness_status",
        "v552j_blocker_context_count",
        "wave_status",
        "thin_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_YEAR_INDEXED_PRESSURE_OVER_TIME_SCHEMA = {
    "required_columns": V553_TEMPORAL_PRESSURE_FIELD_SCHEMA["required_columns"],
}

V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA = {
    "required_columns": [
        "run_id",
        "prior_wave",
        "current_wave",
        "prior_canonical_wave",
        "current_canonical_wave",
        "source",
        "prior_wave_status",
        "current_wave_status",
        "shared_semantic_columns_json",
        "shared_directionality_columns_json",
        "shared_position_columns_json",
        "shared_semantic_column_count",
        "shared_directionality_column_count",
        "shared_position_column_count",
        "pair_missing_authority_count",
        "pair_harmonization_status",
        "pair_harmonization_score",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_WAVE_HARMONIZATION_TABLE_SCHEMA = {
    "required_columns": [
        "wave",
        "source",
        "canonical_wave",
        "authority_dir",
        "run_root",
        "latest_v552j_root",
        "latest_v552j_readiness_report",
        "v552j_readiness_status",
        "v552j_blocker_context_breakdown_json",
        "v552j_blocker_context_count",
        "v552j_handoff_authority_status",
        "overlay_paths",
        "overlay_row_counts",
        "overlay_columns",
        "missing_authority_kinds",
        "wave_status",
        "thin_readiness",
        "thin_status",
        "thin_ready",
        "thin_layer_count",
        "created_at",
    ]
}

V553_WAVE_ANCHOR_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "wave",
        "canonical_wave",
        "wave_year",
        "anchor_status",
        "anchor_authority",
        "anchor_confidence",
        "v552j_run_id",
        "v552j_readiness_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_SOURCE_WAVE_ANCHOR_MANIFEST_SCHEMA = V553_WAVE_ANCHOR_INDEX_SCHEMA

V553_TEMPORAL_ANCHOR_INDEX_SCHEMA = {
    "required_columns": V553_WAVE_ANCHOR_INDEX_SCHEMA["required_columns"],
}

V553_HARMONIZATION_AUTHORITY_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "authority_status",
        "wave_count",
        "wave_pair_count",
        "multiple_waves_present",
        "ready_for_v553",
        "comparability_status",
        "harmonization_score",
        "required_authority_kinds_json",
        "blocking_conditions_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_HARMONIZATION_DIFFERENCE_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "prior_wave",
        "current_wave",
        "source",
        "prior_canonical_wave",
        "current_canonical_wave",
        "prior_wave_status",
        "current_wave_status",
        "shared_semantic_columns_json",
        "shared_directionality_columns_json",
        "shared_position_columns_json",
        "shared_relation_axis_ids_json",
        "shared_target_entity_ids_json",
        "shared_driver_facet_ids_json",
        "shared_structural_channel_ids_json",
        "shared_horizon_constraint_ids_json",
        "shared_semantic_column_count",
        "shared_directionality_column_count",
        "shared_position_column_count",
        "shared_relation_axis_id_count",
        "shared_target_entity_id_count",
        "shared_driver_facet_id_count",
        "shared_structural_channel_id_count",
        "shared_horizon_constraint_id_count",
        "pair_missing_authority_count",
        "pair_harmonization_status",
        "pair_harmonization_score",
        "difference_kind",
        "difference_reason",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "source_v552_structural_fact_id",
        "source_v552_structural_fact_ids_json",
        "source_v552_structural_fact_ids_diagnostic_json",
        "source_v552_temporal_key_source_id",
        "source_v552_temporal_key_source_ids_json",
        "source_v552_temporal_key_source_ids_diagnostic_json",
        "structural_fact_lane",
        "structural_fact_grain",
        "source_v552_structural_fact_lane",
        "source_v552_structural_fact_grain",
        "relation_axis",
        "target_entity",
        "driver_facet",
        "structural_channel",
        "horizon_constraint",
        "semantic_signature",
        "canonical_semantic_signature",
        "comparable_temporal_key",
        "comparable_key_grain",
        "comparable_key_basis_json",
        "key_basis_json",
        "structural_dimension_status",
        "fallback_permission_profile_key",
        "pressure_value_kind",
        "probe_pressure_value",
        "structural_pressure_value",
        "authorized_structural_pressure_value",
        "probe_structural_score",
        "source_wave_ids_json",
        "key_candidate_count",
        "key_blocker_count",
        "contributing_wave_ids_json",
        "contributing_packet_ids_json",
        "contributing_input_ids_json",
        "distinct_wave_count",
        "eligible_wave_count",
        "probe_ready_wave_count",
        "resolved_wave_count",
        "authorized_anchor_count",
        "probe_anchor_count",
        "readiness_score",
        "support_score",
        "directionality_score",
        "authority_score",
        "comparability_score",
        "confidence_score",
        "harmonization_authority_status",
        "semantic_compatibility_status",
        "directionality_compatibility_status",
        "position_compatibility_status",
        "structural_identity_compatibility_status",
        "multi_wave_authorization_status",
        "multi_wave_authorization_reason",
        "ready_for_v554",
        "key_authority_status",
        "comparability_class",
        "comparability_status",
        "comparability_reason",
        "blocked_reason",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "wave_id",
        "temporal_pressure_key",
        "country",
        "source_v552_structural_fact_id",
        "source_v552_structural_fact_ids_json",
        "source_v552_structural_fact_ids_diagnostic_json",
        "source_v552_temporal_key_source_id",
        "source_v552_temporal_key_source_ids_json",
        "source_v552_temporal_key_source_ids_diagnostic_json",
        "structural_fact_lane",
        "structural_fact_grain",
        "source_v552_structural_fact_lane",
        "source_v552_structural_fact_grain",
        "relation_axis",
        "target_entity",
        "driver_facet",
        "structural_channel",
        "horizon_constraint",
        "semantic_signature",
        "canonical_semantic_signature",
        "comparable_temporal_key",
        "comparable_key_grain",
        "comparable_key_basis_json",
        "key_basis_json",
        "structural_dimension_status",
        "fallback_permission_profile_key",
        "pressure_value_kind",
        "probe_pressure_value",
        "structural_pressure_value",
        "authorized_structural_pressure_value",
        "probe_structural_score",
        "candidate_status",
        "key_authority_status",
        "candidate_count",
        "resolution_grain",
        "ready_for_v553_input_count",
        "probe_ready_input_count",
        "packet_ready_input_count",
        "ready_for_runtime_consumption_input_count",
        "probe_only_input_count",
        "blocked_input_count",
        "temporal_allowed_input_count",
        "temporal_blocked_input_count",
        "readiness_score",
        "support_score",
        "directionality_score",
        "authority_score",
        "comparability_score",
        "confidence_score",
        "pressure_value",
        "source_wave_ids_json",
        "source_v552j_packet_ids_json",
        "source_v552j_input_ids_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "wave_id",
        "temporal_pressure_key",
        "country",
        "source_v552_structural_fact_id",
        "source_v552_structural_fact_ids_json",
        "source_v552_structural_fact_ids_diagnostic_json",
        "source_v552_temporal_key_source_id",
        "source_v552_temporal_key_source_ids_json",
        "source_v552_temporal_key_source_ids_diagnostic_json",
        "structural_fact_lane",
        "structural_fact_grain",
        "blocker_class",
        "blocker_reason",
        "blocking_reason_detail",
        "packet_class",
        "read_permission",
        "comparability_status",
        "temporal_field_allowed",
        "ready_for_v553",
        "structural_dimension_status",
        "fallback_permission_profile_key",
        "probe_pressure_value",
        "structural_pressure_value",
        "source_v552j_packet_ids_json",
        "source_v552j_input_ids_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave_before",
        "wave_after",
        "wave_year_before",
        "wave_year_after",
        "pressure_domain",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "structural_channel_id",
        "horizon_constraint_id",
        "pressure_value_distribution",
        "pressure_intensity_band",
        "pressure_status",
        "interpolation_method",
        "confidence_penalty",
        "basis_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_PRESSURE_OBSERVATION_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "comparable_temporal_key",
        "comparable_key_grain",
        "country",
        "wave_id",
        "survey_year",
        "source_v552_structural_fact_id",
        "source_v552_structural_fact_ids_json",
        "source_v552_structural_fact_ids_diagnostic_json",
        "source_v552_temporal_key_source_id",
        "source_v552_temporal_key_source_ids_json",
        "source_v552_temporal_key_source_ids_diagnostic_json",
        "structural_fact_lane",
        "structural_fact_grain",
        "source_v552_structural_fact_lane",
        "source_v552_structural_fact_grain",
        "canonical_semantic_signature",
        "pressure_value",
        "pressure_value_kind",
        "support_score",
        "confidence_score",
        "directionality_score",
        "authority_score",
        "uncertainty_score",
        "structural_pressure_value",
        "authorized_structural_pressure_value",
        "probe_pressure_value",
        "probe_structural_score",
        "evidence_coverage_score",
        "structural_pressure_authority",
        "structural_dimension_status",
        "fallback_permission_profile_key",
        "source_v552j_packet_ids_json",
        "source_lane_summary",
        "temporal_status",
        "allowed_downstream_use",
        "probe_only",
        "ready_for_v553_inputs",
        "probe_ready_inputs",
        "temporal_field_allowed_inputs",
        "single_wave_probe_allowed_inputs",
        "ready_for_runtime_consumption_inputs",
        "multi_wave_authorization_status",
        "multi_wave_authorization_reason",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_PRESSURE_BASIS_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "wave_id",
        "survey_year",
        "pressure_basis",
        "pressure_basis_source",
        "pressure_basis_summary_json",
        "basis_relation_axis_id",
        "basis_target_entity_id",
        "basis_driver_facet_id",
        "basis_structural_channel_id",
        "basis_horizon_constraint_id",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_CONFIDENCE_PENALTY_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "wave_id",
        "survey_year",
        "confidence_penalty",
        "confidence_penalty_reason",
        "confidence_penalty_basis_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_CROSS_WAVE_DELTA_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "comparable_temporal_key",
        "country",
        "from_wave_id",
        "to_wave_id",
        "from_year",
        "to_year",
        "delta_value",
        "delta_value_kind",
        "structural_delta_value",
        "authorized_structural_delta_value",
        "probe_delta_value",
        "coverage_delta_value",
        "delta_direction",
        "delta_magnitude_class",
        "confidence_delta",
        "authority_delta",
        "comparability_status",
        "delta_basis",
        "blocked_reason",
        "delta_interpretation_permission",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_INTERPOLATION_SEGMENT_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "segment_start_year",
        "segment_end_year",
        "interpolation_status",
        "interpolation_method",
        "interpolation_allowed",
        "interpolation_reason",
        "key_authorization_status",
        "anchor_count",
        "confidence_decay",
        "gap_length_years",
        "warning_flags_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "missing_year_or_span",
        "absence_type",
        "known_absence",
        "missingness_reason",
        "downstream_permission",
        "key_authorization_status",
        "value_inference_allowed",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "rupture_window_start",
        "rupture_window_end",
        "rupture_signal_type",
        "rupture_signal_strength",
        "source_delta_ids_json",
        "rupture_status",
        "external_event_claim_made",
        "interpretation_permission",
        "blocked_reason",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_PRESSURE_FIELD_CONTRACT_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "year_or_period",
        "pressure_level",
        "pressure_direction",
        "pressure_volatility",
        "pressure_confidence",
        "pressure_authority",
        "structural_pressure_value",
        "authorized_structural_pressure_value",
        "probe_pressure_value",
        "probe_structural_score",
        "pressure_value_kind",
        "evidence_coverage_score",
        "structural_pressure_authority",
        "temporal_status",
        "allowed_downstream_use",
        "source_observation_ids_json",
        "source_delta_ids_json",
        "blocked_reason",
        "pressure_basis",
        "probe_only",
        "key_authorization_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_V554_HANDOFF_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "temporal_pressure_key",
        "country",
        "permitted_seed_affordance_inputs_json",
        "blocked_seed_affordance_inputs_json",
        "uncertainty_payload_json",
        "required_v554_absence_handling",
        "ready_for_v554_seed_affordance",
        "v553_handoff_mode",
        "v553_handoff_allowed",
        "v553_probe_allowed",
        "v553_temporal_field_allowed",
        "v553_handoff_blocked_reason",
        "not_personhood_reason",
        "key_authorization_status",
        "authorized_anchor_count",
        "probe_anchor_count",
        "unknown_gap_count",
        "interpolated_row_count",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_FORBIDDEN_INFERENCE_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "artifact_name",
        "forbidden_claim_id",
        "claim_text",
        "violation_detected",
        "reason",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_FORBIDDEN_ACTOR_GENERATION_AUDIT_SCHEMA = V553_FORBIDDEN_INFERENCE_AUDIT_SCHEMA

V553_RUN_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_runs_json",
        "artifact_paths_json",
        "artifact_row_counts_json",
        "compiler_version",
        "readiness_status",
        "blocker_counts_json",
        "completeness_status",
        "created_at",
        "schema_version",
    ]
}

V553_INTERPOLATION_POLICY_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave_before",
        "wave_after",
        "interpolation_method",
        "interpolation_allowed",
        "interpolation_status",
        "interpolation_authority",
        "interpolation_reason",
        "confidence_penalty",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_PRESSURE_COMPONENT_BREAKDOWN_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "pressure_domain",
        "coverage_pressure",
        "structural_domain_pressure",
        "contradiction_pressure",
        "absence_pressure",
        "uncertainty_pressure",
        "rupture_pressure",
        "comparability_pressure",
        "authority_pressure",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_RUPTURE_EVENT_SLOT_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "slot_name",
        "slot_status",
        "event_authority_ref",
        "rupture_override_status",
        "event_registry_status",
        "manual_review_required",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_COHORT_WINDOW_REQUIREMENT_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "window_name",
        "window_status",
        "window_required",
        "window_authority",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_ABSENCE_NONCOMPARABILITY_REGISTER_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave",
        "canonical_wave",
        "register_kind",
        "register_status",
        "register_reason",
        "missing_authority_kinds_json",
        "comparability_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_INTERPOLATION_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave_before",
        "wave_after",
        "distance_to_nearest_wave",
        "distance_between_anchors",
        "interpolation_method",
        "interpolation_authority",
        "confidence_penalty",
        "event_override_flag",
        "event_ids_json",
        "rupture_blocked",
        "manual_review_required",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_EVENT_OVERRIDE_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "event_registry_status",
        "interpolation_across_rupture_allowed",
        "override_count",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_AUTHORITY_LEDGER_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave",
        "canonical_wave",
        "anchor_status",
        "anchor_authority",
        "anchor_confidence",
        "authority_status",
        "use_permission_class",
        "confidence_penalty",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_COMPARABILITY_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "prior_wave",
        "current_wave",
        "shared_semantic_column_count",
        "shared_directionality_column_count",
        "shared_position_column_count",
        "pair_missing_authority_count",
        "comparability_status",
        "wave_pair_evidence_score",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_RUPTURE_BLOCK_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "source_family",
        "source",
        "country_code",
        "year",
        "wave",
        "canonical_wave",
        "rupture_blocked",
        "rupture_reason",
        "manual_review_required",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_DOWNSTREAM_V554_HANDOFF_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "status",
        "ready_for_v554",
        "handoff_role",
        "legacy_compatibility_only",
        "authoritative_handoff_path",
        "authoritative_handoff_status",
        "pressure_field_rows",
        "country_year_rows",
        "contradiction_rows",
        "absence_rows",
        "blocked_rows",
        "review_required_rows",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_CONTRADICTION_OVER_TIME_SCHEMA = {
    "required_columns": [
        "run_id",
        "wave",
        "canonical_wave",
        "source",
        "contradiction_pressure",
        "pressure_status",
        "wave_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_PRESSURE_ABSENCE_OVER_TIME_SCHEMA = {
    "required_columns": [
        "run_id",
        "wave",
        "canonical_wave",
        "source",
        "absence_pressure",
        "pressure_status",
        "wave_status",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V553_TEMPORAL_READINESS_REPORT_SCHEMA = {
    "required_columns": [
        "run_id",
        "status",
        "ready_for_v554",
        "multiple_waves_present",
        "wave_count",
        "wave_coverage_score",
        "shared_semantic_score",
        "shared_directionality_score",
        "shared_position_score",
        "overlay_presence_score",
        "harmonization_score",
        "readiness_score",
        "pressure_field_rows",
        "contradiction_rows",
        "absence_rows",
        "v552j_readiness_status",
        "v552j_blocker_context_count",
        "input_status",
        "missing_required_inputs_json",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}


def validate_required_columns(frame: pd.DataFrame, required_columns: list[str], name: str) -> list[str]:
    errors: list[str] = []
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        errors.append(f"{name}: missing columns {missing}")
    return errors


__all__ = [
    "V553_SCHEMA_VERSION",
    "V553_COMPILER_VERSION",
    "V553_TEMPORAL_PRESSURE_FIELD_SCHEMA",
    "V553_YEAR_INDEXED_PRESSURE_OVER_TIME_SCHEMA",
    "V553_WAVE_HARMONIZATION_EVIDENCE_SCHEMA",
    "V553_WAVE_ANCHOR_INDEX_SCHEMA",
    "V553_SOURCE_WAVE_ANCHOR_MANIFEST_SCHEMA",
    "V553_TEMPORAL_ANCHOR_INDEX_SCHEMA",
    "V553_HARMONIZATION_AUTHORITY_INDEX_SCHEMA",
    "V553_HARMONIZED_PRESSURE_KEY_INDEX_SCHEMA",
    "V553_TEMPORAL_KEY_CANDIDATE_INDEX_SCHEMA",
    "V553_TEMPORAL_KEY_BLOCKER_INDEX_SCHEMA",
    "V553_COUNTRY_YEAR_PRESSURE_FIELD_SCHEMA",
    "V553_TEMPORAL_PRESSURE_OBSERVATION_INDEX_SCHEMA",
    "V553_CROSS_WAVE_DELTA_INDEX_SCHEMA",
    "V553_INTERPOLATION_SEGMENT_INDEX_SCHEMA",
    "V553_TEMPORAL_GAP_AND_ABSENCE_INDEX_SCHEMA",
    "V553_STRUCTURAL_RUPTURE_CANDIDATE_INDEX_SCHEMA",
    "V553_TEMPORAL_PRESSURE_FIELD_CONTRACT_SCHEMA",
    "V553_V554_HANDOFF_INDEX_SCHEMA",
    "V553_FORBIDDEN_INFERENCE_AUDIT_SCHEMA",
    "V553_INTERPOLATION_POLICY_LEDGER_SCHEMA",
    "V553_PRESSURE_COMPONENT_BREAKDOWN_SCHEMA",
    "V553_RUPTURE_EVENT_SLOT_LEDGER_SCHEMA",
    "V553_COHORT_WINDOW_REQUIREMENT_INDEX_SCHEMA",
    "V553_ABSENCE_NONCOMPARABILITY_REGISTER_SCHEMA",
    "V553_INTERPOLATION_MANIFEST_SCHEMA",
    "V553_EVENT_OVERRIDE_MANIFEST_SCHEMA",
    "V553_TEMPORAL_AUTHORITY_LEDGER_SCHEMA",
    "V553_COMPARABILITY_AUDIT_SCHEMA",
    "V553_RUPTURE_BLOCK_AUDIT_SCHEMA",
    "V553_DOWNSTREAM_V554_HANDOFF_INDEX_SCHEMA",
    "V553_CONTRADICTION_OVER_TIME_SCHEMA",
    "V553_PRESSURE_ABSENCE_OVER_TIME_SCHEMA",
    "V553_TEMPORAL_READINESS_REPORT_SCHEMA",
    "V553_RUN_MANIFEST_SCHEMA",
    "V553_FORBIDDEN_ACTOR_GENERATION_AUDIT_SCHEMA",
    "validate_required_columns",
]
