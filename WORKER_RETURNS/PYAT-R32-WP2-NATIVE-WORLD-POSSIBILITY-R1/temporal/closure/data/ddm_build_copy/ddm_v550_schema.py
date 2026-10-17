#!/usr/bin/env python3
"""Schema helpers for V550 canonical outputs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import pyarrow as pa
    PYARROW_AVAILABLE = True
except ModuleNotFoundError:
    PYARROW_AVAILABLE = False

    class _ArrowTypeShim:
        def __init__(self, name: str):
            self.name = name

        def __str__(self) -> str:
            return self.name

    class _ArrowFieldShim:
        def __init__(self, name: str, field_type: Any, nullable: bool = True):
            self.name = name
            self.type = field_type
            self.nullable = nullable

    class _ArrowSchemaShim(tuple):
        @property
        def names(self) -> list[str]:
            return [field.name for field in self]

    class _PyArrowShim:
        @staticmethod
        def schema(fields: list[Any]) -> _ArrowSchemaShim:
            return _ArrowSchemaShim(fields)

        @staticmethod
        def field(name: str, field_type: Any, nullable: bool = True) -> _ArrowFieldShim:
            return _ArrowFieldShim(name, field_type, nullable)

        @staticmethod
        def string() -> _ArrowTypeShim:
            return _ArrowTypeShim("string")

        @staticmethod
        def int64() -> _ArrowTypeShim:
            return _ArrowTypeShim("int64")

        @staticmethod
        def float64() -> _ArrowTypeShim:
            return _ArrowTypeShim("double")

        @staticmethod
        def bool_() -> _ArrowTypeShim:
            return _ArrowTypeShim("bool")

    pa = _PyArrowShim()

SHARD_PLAN_SCHEMA = {
    "required_columns": [
        "run_id",
        "created_at",
        "planner_version",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "shard_id",
        "country_count",
        "respondent_count",
        "response_row_count",
        "mapped_row_count",
        "facet_row_count",
        "position_field_count",
        "weight_status",
        "readiness_status",
        "skip_by_default",
        "skip_reason",
        "estimated_question_count",
        "output_dir",
        "command",
    ]
}

SHARD_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "shard_id",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "created_at",
        "completed_at",
        "success",
        "rows_by_table",
        "outputs",
    ]
}

SHARD_OUTPUT_TABLES = [
    "question_universe",
    "question_use_contract",
    "answer_distribution",
    "country_answer_distribution",
    "position_distribution",
    "position_indicator_summary",
    "indicator_answer_matrix",
    "outlier_cohort_summary",
    "secondary_indicator_summary",
    "recursive_branch_nodes",
    "branch_position_signature",
    "branch_relation_co_signature",
    "branch_co_signature",
    "question_response_attitude_cloud",
    "mapping_gap_report",
    "underpowered_quarantine",
    "response_option_manual_review",
    "scope_manifest",
    "substrate_readiness",
    "position_field_coverage",
    "weight_coverage",
    "mapping_status_coverage",
    "legacy_leak_report",
    "cloud_exclusion_audit",
]

# Static normalized Arrow schemas shared by every supported survey family.
# These ensure uniform schemas across all waves regardless of empty/non-empty status.

BRANCH_POSITION_SIGNATURE_ARROW_SCHEMA = pa.schema([
    pa.field("run_id", pa.string(), nullable=True),
    pa.field("source", pa.string(), nullable=True),
    pa.field("source_family", pa.string(), nullable=True),
    pa.field("wave", pa.string(), nullable=True),
    pa.field("canonical_wave", pa.string(), nullable=True),
    pa.field("country_code", pa.string(), nullable=True),
    pa.field("survey_year", pa.int64(), nullable=True),
    pa.field("canonical_var_name", pa.string(), nullable=True),
    pa.field("source_var_name", pa.string(), nullable=True),
    pa.field("source_var_names", pa.string(), nullable=True),
    pa.field("source_mapping_type", pa.string(), nullable=True),
    pa.field("source_mapping_authority", pa.string(), nullable=True),
    pa.field("var_code", pa.string(), nullable=True),
    pa.field("var_name", pa.string(), nullable=True),
    pa.field("question_id", pa.string(), nullable=True),
    pa.field("question_text", pa.string(), nullable=True),
    pa.field("driver_id", pa.string(), nullable=True),
    pa.field("driver_facet_id", pa.string(), nullable=True),
    pa.field("relation_axis_id", pa.string(), nullable=True),
    pa.field("target_entity_id", pa.string(), nullable=True),
    pa.field("mapping_status", pa.string(), nullable=True),
    pa.field("legacy_final_driver_id", pa.string(), nullable=True),
    pa.field("legacy_driver_leak_flag", pa.bool_(), nullable=True),
    pa.field("question_type", pa.string(), nullable=True),
    pa.field("handling_rule", pa.string(), nullable=True),
    pa.field("recommended_computation", pa.string(), nullable=True),
    pa.field("source_structure_classification", pa.string(), nullable=True),
    pa.field("response_direction", pa.string(), nullable=True),
    pa.field("response_intensity", pa.string(), nullable=True),
    pa.field("polarity", pa.string(), nullable=True),
    pa.field("ordinal_rank", pa.string(), nullable=True),
    pa.field("scale_min", pa.string(), nullable=True),
    pa.field("scale_max", pa.string(), nullable=True),
    pa.field("scale_direction", pa.string(), nullable=True),
    pa.field("directionality_status", pa.string(), nullable=True),
    pa.field("response_family", pa.string(), nullable=True),
    pa.field("response_semantics_status", pa.string(), nullable=True),
    pa.field("response_semantics_source", pa.string(), nullable=True),
    pa.field("response_semantics_contract_hash", pa.string(), nullable=True),
    pa.field("has_response_option_map", pa.bool_(), nullable=True),
    pa.field("response_option_confidence_min", pa.string(), nullable=True),
    pa.field("response_option_confidence_max", pa.string(), nullable=True),
    pa.field("n_response_rows", pa.int64(), nullable=True),
    pa.field("n_respondents", pa.int64(), nullable=True),
    pa.field("n_countries", pa.int64(), nullable=True),
    pa.field("weight_status", pa.string(), nullable=True),
    pa.field("readiness_status", pa.string(), nullable=True),
    pa.field("dominant_response_value", pa.string(), nullable=True),
    pa.field("dominant_response_pct", pa.float64(), nullable=True),
    pa.field("created_at", pa.string(), nullable=True),
    pa.field("shard_id", pa.string(), nullable=True),
    pa.field("question_type_structural_role", pa.string(), nullable=True),
    pa.field("source_structure_basis", pa.string(), nullable=True),
    pa.field("source_structure_confidence", pa.string(), nullable=True),
    pa.field("source_structure_review_required", pa.bool_(), nullable=True),
    pa.field("source_structure_source", pa.string(), nullable=True),
    pa.field("source_structure_fields_joined", pa.bool_(), nullable=True),
    pa.field("source_structure_join_key", pa.string(), nullable=True),
    pa.field("source_structure_join_confidence", pa.string(), nullable=True),
    pa.field("response_topology", pa.string(), nullable=True),
    pa.field("future_evidence_eligible", pa.bool_(), nullable=True),
    pa.field("future_topology_evidence_eligible", pa.bool_(), nullable=True),
    pa.field("current_directional_atom_eligible", pa.bool_(), nullable=True),
    pa.field("directional_certification_status", pa.string(), nullable=True),
    pa.field("semantic_role", pa.string(), nullable=True),
    pa.field("v551_evidence_role", pa.string(), nullable=True),
    pa.field("review_required", pa.bool_(), nullable=True),
    pa.field("disallowed_reason", pa.string(), nullable=True),
    pa.field("manual_override_used", pa.bool_(), nullable=True),
    pa.field("manual_override_basis", pa.string(), nullable=True),
    pa.field("manual_override_reason", pa.string(), nullable=True),
    pa.field("itinerary_review_priority", pa.string(), nullable=True),
    pa.field("itinerary_manual_designation_required", pa.bool_(), nullable=True),
    pa.field("itinerary_primary_docs", pa.string(), nullable=True),
    pa.field("itinerary_secondary_docs", pa.string(), nullable=True),
    pa.field("itinerary_review_notes", pa.string(), nullable=True),
    pa.field("authority_table_used", pa.bool_(), nullable=True),
    pa.field("authority_table_basis", pa.string(), nullable=True),
    pa.field("authority_semantic_lane", pa.string(), nullable=True),
    pa.field("authority_semantic_role", pa.string(), nullable=True),
    pa.field("authority_evidence_lane", pa.string(), nullable=True),
    pa.field("authority_designation_confidence", pa.string(), nullable=True),
    pa.field("authority_review_required", pa.bool_(), nullable=True),
    pa.field("question_directionality_authority_used", pa.bool_(), nullable=True),
    pa.field("question_directionality_authority_status", pa.string(), nullable=True),
    pa.field("gss2010_structural_overlay_used", pa.bool_(), nullable=True),
    pa.field("gss2010_structural_overlay_basis", pa.string(), nullable=True),
    pa.field("gss2010_structural_overlay_review_required", pa.bool_(), nullable=True),
    pa.field("allowed_as_response_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_position_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_context_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_demographic_predictor", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_splitter", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_position_signature", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_relation_cosignature", pa.bool_(), nullable=True),
    pa.field("allowed_as_attitude_cloud_anchor", pa.bool_(), nullable=True),
    pa.field("allowed_as_attitude_cloud_feature", pa.bool_(), nullable=True),
    pa.field("allowed_as_v551_relation_evidence", pa.bool_(), nullable=True),
    pa.field("allowed_as_parent_prior_coordinate", pa.bool_(), nullable=True),
    pa.field("allowed_as_temporal_pressure_indicator", pa.bool_(), nullable=True),
    pa.field("allowed_as_runtime_persona_evidence", pa.bool_(), nullable=True),
    pa.field("question_block_id", pa.string(), nullable=True),
    pa.field("structural_domain_id", pa.string(), nullable=True),
    pa.field("target_entity_rule", pa.string(), nullable=True),
    pa.field("final_driver_scope", pa.string(), nullable=True),
    pa.field("semantic_subrole", pa.string(), nullable=True),
    pa.field("semantic_tags", pa.string(), nullable=True),
    pa.field("directionality_policy", pa.string(), nullable=True),
    pa.field("semantic_confidence", pa.string(), nullable=True),
    pa.field("semantic_note", pa.string(), nullable=True),
    pa.field("position_conditioning", pa.string(), nullable=True),
    pa.field("position_modifiers", pa.string(), nullable=True),
    pa.field("conditional_strata_weights", pa.string(), nullable=True),
    pa.field("horizon_affordance", pa.string(), nullable=True),
    pa.field("position_conditioning_note", pa.string(), nullable=True),
    pa.field("position_conditioning_confidence", pa.string(), nullable=True),
    pa.field("question_use_contract_hash", pa.string(), nullable=True),
    pa.field("question_use_contract_joined", pa.bool_(), nullable=True),
    pa.field("branch_id", pa.string(), nullable=True),
    pa.field("branch_key", pa.string(), nullable=True),
    pa.field("anchor_question_id", pa.string(), nullable=True),
    pa.field("feature_rank", pa.int64(), nullable=True),
    pa.field("predictor_family", pa.string(), nullable=True),
    pa.field("feature_role", pa.string(), nullable=True),
    pa.field("support_status", pa.string(), nullable=True),
    pa.field("confidence_tier", pa.string(), nullable=True),
    pa.field("high_cardinality_flag", pa.bool_(), nullable=True),
    pa.field("rare_category_flag", pa.bool_(), nullable=True),
    pa.field("rare_category_handling", pa.string(), nullable=True),
    pa.field("cloud_lane_artifact", pa.bool_(), nullable=True),
    pa.field("diagnostic_artifact", pa.bool_(), nullable=True),
    pa.field("not_direct_evidence", pa.bool_(), nullable=True),
    pa.field("evidence_role", pa.string(), nullable=True),
    pa.field("artifact_status", pa.string(), nullable=True),
    pa.field("feature_name", pa.string(), nullable=True),
    pa.field("feature_kind", pa.string(), nullable=True),
    pa.field("demographic_feature_excluded_flag", pa.bool_(), nullable=True),
    pa.field("feature_value", pa.string(), nullable=True),
    pa.field("association_score", pa.float64(), nullable=True),
    pa.field("association_metric", pa.string(), nullable=True),
    pa.field("normalized_mutual_information", pa.float64(), nullable=True),
    pa.field("cramers_v", pa.float64(), nullable=True),
    pa.field("n_unweighted", pa.int64(), nullable=True),
    pa.field("n_unique_feature_values", pa.int64(), nullable=True),
    pa.field("n_unique_response_values", pa.int64(), nullable=True),
    pa.field("target_dominant_response", pa.string(), nullable=True),
    pa.field("target_dominant_response_share", pa.float64(), nullable=True),
])

BRANCH_RELATION_CO_SIGNATURE_ARROW_SCHEMA = pa.schema([
    pa.field("run_id", pa.string(), nullable=True),
    pa.field("source", pa.string(), nullable=True),
    pa.field("source_family", pa.string(), nullable=True),
    pa.field("wave", pa.string(), nullable=True),
    pa.field("canonical_wave", pa.string(), nullable=True),
    pa.field("country_code", pa.string(), nullable=True),
    pa.field("survey_year", pa.int64(), nullable=True),
    pa.field("canonical_var_name", pa.string(), nullable=True),
    pa.field("source_var_name", pa.string(), nullable=True),
    pa.field("source_var_names", pa.string(), nullable=True),
    pa.field("source_mapping_type", pa.string(), nullable=True),
    pa.field("source_mapping_authority", pa.string(), nullable=True),
    pa.field("var_code", pa.string(), nullable=True),
    pa.field("var_name", pa.string(), nullable=True),
    pa.field("question_id", pa.string(), nullable=True),
    pa.field("question_text", pa.string(), nullable=True),
    pa.field("driver_id", pa.string(), nullable=True),
    pa.field("driver_facet_id", pa.string(), nullable=True),
    pa.field("relation_axis_id", pa.string(), nullable=True),
    pa.field("target_entity_id", pa.string(), nullable=True),
    pa.field("mapping_status", pa.string(), nullable=True),
    pa.field("legacy_final_driver_id", pa.string(), nullable=True),
    pa.field("legacy_driver_leak_flag", pa.bool_(), nullable=True),
    pa.field("question_type", pa.string(), nullable=True),
    pa.field("handling_rule", pa.string(), nullable=True),
    pa.field("recommended_computation", pa.string(), nullable=True),
    pa.field("source_structure_classification", pa.string(), nullable=True),
    pa.field("response_direction", pa.string(), nullable=True),
    pa.field("response_intensity", pa.string(), nullable=True),
    pa.field("polarity", pa.string(), nullable=True),
    pa.field("ordinal_rank", pa.string(), nullable=True),
    pa.field("scale_min", pa.string(), nullable=True),
    pa.field("scale_max", pa.string(), nullable=True),
    pa.field("scale_direction", pa.string(), nullable=True),
    pa.field("directionality_status", pa.string(), nullable=True),
    pa.field("response_family", pa.string(), nullable=True),
    pa.field("response_semantics_status", pa.string(), nullable=True),
    pa.field("response_semantics_source", pa.string(), nullable=True),
    pa.field("response_semantics_contract_hash", pa.string(), nullable=True),
    pa.field("has_response_option_map", pa.bool_(), nullable=True),
    pa.field("response_option_confidence_min", pa.string(), nullable=True),
    pa.field("response_option_confidence_max", pa.string(), nullable=True),
    pa.field("n_response_rows", pa.int64(), nullable=True),
    pa.field("n_respondents", pa.int64(), nullable=True),
    pa.field("n_countries", pa.int64(), nullable=True),
    pa.field("weight_status", pa.string(), nullable=True),
    pa.field("readiness_status", pa.string(), nullable=True),
    pa.field("dominant_response_value", pa.string(), nullable=True),
    pa.field("dominant_response_pct", pa.float64(), nullable=True),
    pa.field("created_at", pa.string(), nullable=True),
    pa.field("shard_id", pa.string(), nullable=True),
    pa.field("question_type_structural_role", pa.string(), nullable=True),
    pa.field("source_structure_basis", pa.string(), nullable=True),
    pa.field("source_structure_confidence", pa.string(), nullable=True),
    pa.field("source_structure_review_required", pa.bool_(), nullable=True),
    pa.field("source_structure_source", pa.string(), nullable=True),
    pa.field("source_structure_fields_joined", pa.bool_(), nullable=True),
    pa.field("source_structure_join_key", pa.string(), nullable=True),
    pa.field("source_structure_join_confidence", pa.string(), nullable=True),
    pa.field("response_topology", pa.string(), nullable=True),
    pa.field("future_evidence_eligible", pa.bool_(), nullable=True),
    pa.field("future_topology_evidence_eligible", pa.bool_(), nullable=True),
    pa.field("current_directional_atom_eligible", pa.bool_(), nullable=True),
    pa.field("directional_certification_status", pa.string(), nullable=True),
    pa.field("semantic_role", pa.string(), nullable=True),
    pa.field("v551_evidence_role", pa.string(), nullable=True),
    pa.field("review_required", pa.bool_(), nullable=True),
    pa.field("disallowed_reason", pa.string(), nullable=True),
    pa.field("manual_override_used", pa.bool_(), nullable=True),
    pa.field("manual_override_basis", pa.string(), nullable=True),
    pa.field("manual_override_reason", pa.string(), nullable=True),
    pa.field("itinerary_review_priority", pa.string(), nullable=True),
    pa.field("itinerary_manual_designation_required", pa.bool_(), nullable=True),
    pa.field("itinerary_primary_docs", pa.string(), nullable=True),
    pa.field("itinerary_secondary_docs", pa.string(), nullable=True),
    pa.field("itinerary_review_notes", pa.string(), nullable=True),
    pa.field("authority_table_used", pa.bool_(), nullable=True),
    pa.field("authority_table_basis", pa.string(), nullable=True),
    pa.field("authority_semantic_lane", pa.string(), nullable=True),
    pa.field("authority_semantic_role", pa.string(), nullable=True),
    pa.field("authority_evidence_lane", pa.string(), nullable=True),
    pa.field("authority_designation_confidence", pa.string(), nullable=True),
    pa.field("authority_review_required", pa.bool_(), nullable=True),
    pa.field("question_directionality_authority_used", pa.bool_(), nullable=True),
    pa.field("question_directionality_authority_status", pa.string(), nullable=True),
    pa.field("gss2010_structural_overlay_used", pa.bool_(), nullable=True),
    pa.field("gss2010_structural_overlay_basis", pa.string(), nullable=True),
    pa.field("gss2010_structural_overlay_review_required", pa.bool_(), nullable=True),
    pa.field("allowed_as_response_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_position_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_context_distribution", pa.bool_(), nullable=True),
    pa.field("allowed_as_demographic_predictor", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_splitter", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_position_signature", pa.bool_(), nullable=True),
    pa.field("allowed_as_branch_relation_cosignature", pa.bool_(), nullable=True),
    pa.field("allowed_as_attitude_cloud_anchor", pa.bool_(), nullable=True),
    pa.field("allowed_as_attitude_cloud_feature", pa.bool_(), nullable=True),
    pa.field("allowed_as_v551_relation_evidence", pa.bool_(), nullable=True),
    pa.field("allowed_as_parent_prior_coordinate", pa.bool_(), nullable=True),
    pa.field("allowed_as_temporal_pressure_indicator", pa.bool_(), nullable=True),
    pa.field("allowed_as_runtime_persona_evidence", pa.bool_(), nullable=True),
    pa.field("question_block_id", pa.string(), nullable=True),
    pa.field("structural_domain_id", pa.string(), nullable=True),
    pa.field("target_entity_rule", pa.string(), nullable=True),
    pa.field("final_driver_scope", pa.string(), nullable=True),
    pa.field("semantic_subrole", pa.string(), nullable=True),
    pa.field("semantic_tags", pa.string(), nullable=True),
    pa.field("directionality_policy", pa.string(), nullable=True),
    pa.field("semantic_confidence", pa.string(), nullable=True),
    pa.field("semantic_note", pa.string(), nullable=True),
    pa.field("position_conditioning", pa.string(), nullable=True),
    pa.field("position_modifiers", pa.string(), nullable=True),
    pa.field("conditional_strata_weights", pa.string(), nullable=True),
    pa.field("horizon_affordance", pa.string(), nullable=True),
    pa.field("position_conditioning_note", pa.string(), nullable=True),
    pa.field("position_conditioning_confidence", pa.string(), nullable=True),
    pa.field("question_use_contract_hash", pa.string(), nullable=True),
    pa.field("question_use_contract_joined", pa.bool_(), nullable=True),
    pa.field("branch_id", pa.string(), nullable=True),
    pa.field("branch_key", pa.string(), nullable=True),
    pa.field("anchor_question_id", pa.string(), nullable=True),
    pa.field("feature_rank", pa.int64(), nullable=True),
    pa.field("predictor_family", pa.string(), nullable=True),
    pa.field("feature_role", pa.string(), nullable=True),
    pa.field("support_status", pa.string(), nullable=True),
    pa.field("confidence_tier", pa.string(), nullable=True),
    pa.field("cloud_lane_artifact", pa.bool_(), nullable=True),
    pa.field("diagnostic_artifact", pa.bool_(), nullable=True),
    pa.field("not_direct_evidence", pa.bool_(), nullable=True),
    pa.field("evidence_role", pa.string(), nullable=True),
    pa.field("artifact_status", pa.string(), nullable=True),
    pa.field("feature_name", pa.string(), nullable=True),
    pa.field("feature_kind", pa.string(), nullable=True),
    pa.field("demographic_feature_excluded_flag", pa.bool_(), nullable=True),
    pa.field("feature_value", pa.string(), nullable=True),
    pa.field("association_score", pa.float64(), nullable=True),
    pa.field("association_metric", pa.string(), nullable=True),
    pa.field("normalized_mutual_information", pa.float64(), nullable=True),
    pa.field("cramers_v", pa.float64(), nullable=True),
    pa.field("n_unweighted", pa.int64(), nullable=True),
    pa.field("n_unique_feature_values", pa.int64(), nullable=True),
    pa.field("n_unique_response_values", pa.int64(), nullable=True),
    pa.field("target_dominant_response", pa.string(), nullable=True),
    pa.field("target_dominant_response_share", pa.float64(), nullable=True),
])

BRANCH_CO_SIGNATURE_ARROW_SCHEMA = BRANCH_RELATION_CO_SIGNATURE_ARROW_SCHEMA

SOURCE_STRUCTURE_POPULATION_AUDIT_SCHEMA = {
    "required_columns": [
        "source",
        "wave",
        "canonical_wave",
        "question_id",
        "var_code",
        "question_text",
        "question_type",
        "handling_rule",
        "recommended_computation",
        "question_type_structural_role",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_join_key",
        "source_structure_join_confidence",
        "source_structure_fields_joined",
        "source_structure_review_required",
        "semantic_role",
        "allowed_as_v551_relation_evidence",
        "review_required",
        "manual_override_used",
        "high_risk_blocked_due_to_missing_structure",
        "disallowed_reason",
    ]
}

V551_ATOM_EXCLUSION_AUDIT_SCHEMA = {
    "required_columns": [
        "source",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "source_table",
        "gate_name",
        "exclusion_reason",
        "n_rows",
        "sample_source_row_hash",
    ]
}

V551_RELATION_EVIDENCE_ATOMS_SCHEMA = {
    "required_columns": [
        "atom_id",
        "shard_id",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "country_code",
        "survey_year",
        "analysis_scope",
        "empirical_object_type",
        "empirical_object_id",
        "empirical_distribution_id",
        "question_id",
        "var_code",
        "question_text",
        "position_field",
        "position_value",
        "response_value_raw",
        "response_value_normalized",
        "response_label",
        "normalized_response_label",
        "response_family",
        "bridge_evidence_lane",
        "response_direction",
        "response_intensity",
        "polarity",
        "ordinal_rank",
        "scale_min",
        "scale_max",
        "scale_direction",
        "directionality_status",
        "semantic_role",
        "v551_evidence_role",
        "evidence_stratum",
        "evidence_stratum_v2",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_id",
        "strata_relevance",
        "strata_path",
        "subject_position_signature",
        "is_substantive",
        "is_missing",
        "is_special",
        "usable_for_evidence",
        "response_option_map_matched",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "normalization_confidence",
        "n_unweighted",
        "n_respondents",
        "n_weighted",
        "pct_unweighted",
        "pct_weighted",
        "weight_status",
        "confidence_tier",
        "support_status",
        "support_gate_status",
        "support_threshold",
        "support_ratio",
        "support_ratio_margin",
        "support_score",
        "support_formula_id",
        "support_formula_version",
        "support_implementation_function",
        "support_score_family",
        "support_higher_is_better",
        "support_decision_role",
        "population_share",
        "prevalence_score",
        "prevalence_formula_id",
        "prevalence_formula_version",
        "prevalence_implementation_function",
        "prevalence_score_family",
        "prevalence_higher_is_better",
        "prevalence_decision_role",
        "question_type",
        "handling_rule",
        "recommended_computation",
        "mapping_status",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_review_required",
        "source_structure_fields_joined",
        "response_topology",
        "future_evidence_eligible",
        "future_topology_evidence_eligible",
        "current_directional_atom_eligible",
        "directional_certification_status",
        "semantic_role_authority_status",
        "response_semantics_authority_status",
        "directionality_authority_status",
        "structural_mapping_status",
        "eligibility_gate_status",
        "eligibility_failed_gates",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
        "position_conditioning",
        "position_modifiers",
        "conditional_strata_weights",
        "horizon_affordance",
        "position_conditioning_note",
        "position_conditioning_confidence",
        "question_use_contract_joined",
        "manual_review_flag",
        "manual_review_reason",
        "forbidden_inference",
        "known_absences",
        "allowed_as_v551_relation_evidence",
        "allowed_as_temporal_pressure_indicator",
        "allowed_as_runtime_persona_evidence",
        "evidence_basis",
        "evidence_basis_origin",
        "provenance_basis",
        "provenance_basis_origin",
        "temporal_authority_status",
        "empirical_observation_class",
        "source_measure_kind",
        "source_measure_status",
        "directional_measure_kind",
        "response_direction_status",
        "response_intensity_status",
        "observed_response_zero",
        "support_measure_role",
        "prevalence_measure_role",
        "support_may_be_used_as_pressure",
        "prevalence_may_be_used_as_pressure",
        "pressure_evidence_class",
        "v552_pressure_component_eligible",
        "v552_pressure_component_status",
        "v552_pressure_component_ineligibility_reason",
        "response_scale_signature",
        "semantic_identity_signature",
        "structural_identity_signature",
        "measurement_contract_hash",
        "atom_contract_hash",
        "source_table",
        "source_row_hash",
        "source_run_id",
        "question_use_contract_hash",
        "source_structure_population_hash",
        "response_option_map_hash",
        "compiled_at",
        "schema_version",
    ]
}

V551_PRESSURE_COMPONENT_AUDIT_SCHEMA = {
    "required_columns": [
        "atom_id",
        "source",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "empirical_object_type",
        "empirical_object_id",
        "empirical_distribution_id",
        "n_respondents",
        "response_value_normalized",
        "response_direction_status",
        "response_intensity_status",
        "observed_response_zero",
        "pressure_evidence_class",
        "allowed_as_temporal_pressure_indicator",
        "v552_pressure_component_eligible",
        "v552_pressure_component_status",
        "v552_pressure_component_ineligibility_reason",
        "semantic_identity_signature",
        "structural_identity_signature",
        "measurement_contract_hash",
        "atom_contract_hash",
    ]
}

V551_LINEAGE_BASIS_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "empirical_object_id",
        "empirical_distribution_id",
        "source_row_hash",
        "source_evidence_basis_nonblank",
        "source_provenance_basis_nonblank",
        "evidence_basis_origin",
        "provenance_basis_origin",
        "evidence_basis_derivation_status",
        "provenance_basis_derivation_status",
        "derivation_failure_reason",
    ]
}

V551_NUMERIC_WRAPPER_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "source_table",
        "bridge_evidence_lane",
        "semantic_role",
        "evidence_stratum",
        "evidence_stratum_v2",
        "response_label",
        "response_family",
        "response_value_normalized",
        "numeric_like_label",
        "numeric_family_compatible",
        "numeric_wrapper_status",
        "numeric_wrapper_reason",
        "numeric_wrapper_confidence",
        "support_status",
        "confidence_tier",
        "v551_relation_evidence_eligible",
        "v551_exclusion_reason",
        "source_row_hash",
        "n_rows",
        "created_at",
    ]
}

V551_RELATION_REVIEW_SURFACE_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "source_table",
        "bridge_evidence_lane",
        "semantic_role",
        "evidence_stratum",
        "evidence_stratum_v2",
        "review_surface_reason",
        "review_surface_priority",
        "support_status",
        "confidence_tier",
        "numeric_wrapper_status",
        "numeric_wrapper_reason",
        "numeric_wrapper_confidence",
        "v551_relation_evidence_eligible",
        "v551_exclusion_reason",
        "source_row_hash",
        "n_rows",
        "created_at",
    ]
}

V551_BLOCKED_SIGNAL_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "source_table",
        "bridge_evidence_lane",
        "semantic_role",
        "evidence_stratum",
        "evidence_stratum_v2",
        "gate_name",
        "blocked_signal_reason",
        "blocked_signal_priority",
        "support_status",
        "confidence_tier",
        "blocked_row_count",
        "sample_source_row_hash",
        "created_at",
    ]
}

CONDITIONAL_DETERMINICITY_INDEX_SCHEMA = {
    "required_columns": [
        "conditional_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "source_table",
        "bridge_evidence_lane",
        "semantic_role",
        "response_value_normalized",
        "response_label",
        "normalized_response_label",
        "response_family",
        "response_direction",
        "response_intensity",
        "directionality_status",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "support_status",
        "v551_conditional_determinicity_eligible",
        "question_type",
        "handling_rule",
        "recommended_computation",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_fields_joined",
        "source_structure_review_required",
        "question_use_contract_joined",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "n_unweighted",
        "n_weighted",
        "pct_unweighted",
        "pct_weighted",
        "support_basis",
        "compiler_status",
        "source_row_hash",
        "source_run_id",
        "compiled_at",
        "schema_version",
    ]
}

V552_COMMON_STRUCTURAL_COLUMNS = [
    "run_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "input_atom_count",
    "eligible_atom_count",
    "directionality_coverage",
    "support_basis",
    "compiler_status",
    "pressure_computation_status",
    "input_atom_hash",
    "input_hash",
    "schema_version",
    "created_at",
]

V552_RELATION_AXIS_PRESSURE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "relation_axis_id",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_TARGET_ENTITY_PRESSURE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "target_entity_id",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_DRIVER_FACET_PRESSURE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "driver_facet_id",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_CONTRADICTION_TENSOR_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "contradiction_id",
            "axis_a",
            "axis_b",
            "target_entity_id",
            "driver_facet_id",
            "positive_atom_count",
            "negative_atom_count",
            "opposing_directionality_present",
            "contradiction_score",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_CONTRADICTION_SURFACE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "contradiction_surface_id",
            "target_entity_id",
            "driver_facet_id",
            "n_relation_axes",
            "n_axes_positive",
            "n_axes_negative",
            "n_axes_neutral",
            "n_axes_mixed_sign",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "n_directional_atoms",
            "n_positive_atoms",
            "n_negative_atoms",
            "n_neutral_atoms",
            "n_unsigned_atoms",
            "pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
            "dominant_relation_axis_id",
            "cross_axis_opposition_present",
            "contradiction_potential",
            "axis_summary_json",
            "axis_orientation_counts_json",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "channel_id",
            "channel_type",
            "anchor_axis_id",
            "anchor_target_id",
            "anchor_driver_facet_id",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "pressure_score",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "n_atoms",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_unweighted_total",
            "n_weighted_total",
            "overall_directionality_coverage",
            "pressure_computation_status",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
        ]
    )),
}

V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "projection_surface_id",
            "strata_path",
            "projection_scope",
            "projection_mode",
            "dominant_stratum_id",
            "dominant_semantic_subrole",
            "dominant_horizon_type",
            "dominant_horizon_scope",
            "dominant_horizon_valence",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "directionality_coverage",
            "projection_score",
            "field_pressure_score",
            "entropy",
            "polarization_index",
            "dominant_orientation",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
        ]
    )),
}

V552_POSITION_CONDITIONING_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "position_conditioning_profile_id",
            "position_conditioning",
            "position_modifiers",
            "strata_path",
            "conditional_strata_path",
            "conditional_strata_weights",
            "horizon_affordance",
            "position_conditioning_note",
            "position_conditioning_confidence",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

V552_PARENT_PRIOR_COMMON_COLUMNS = [
    "run_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "prior_id",
    "prior_type",
    "position_signature",
    "attitude_domain",
    "prior_distribution",
    "confidence_tier",
    "basis",
    "known_absences",
    "forbidden_inference",
    "created_at",
]

V552_PARENT_POSITION_PRIOR_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_PARENT_PRIOR_COMMON_COLUMNS
        + [
            "birth_year_range",
            "formative_year_range",
            "child_birth_year",
            "sex_gender",
            "age_group_at_child_birth",
            "education_level",
            "income_level",
            "religion_label",
            "urban_rural",
            "region",
            "ethnicity",
            "language",
            "packet_ids",
            "channel_ids",
        ]
    )),
}

V552_PARENT_ATTITUDE_PRIOR_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_PARENT_PRIOR_COMMON_COLUMNS
        + [
            "birth_year_range",
            "formative_year_range",
            "child_birth_year",
            "sex_gender",
            "age_group_at_child_birth",
            "education_level",
            "income_level",
            "religion_label",
            "urban_rural",
            "region",
            "ethnicity",
            "language",
            "packet_ids",
            "channel_ids",
        ]
    )),
}

V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_PARENT_PRIOR_COMMON_COLUMNS
        + [
            "birth_year_range",
            "formative_year_range",
            "child_birth_year",
            "sex_gender",
            "age_group_at_child_birth",
            "education_level",
            "income_level",
            "religion_label",
            "urban_rural",
            "region",
            "ethnicity",
            "language",
            "packet_ids",
            "channel_ids",
        ]
    )),
}

V552_PARENT_CONTRADICTION_PRIOR_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_PARENT_PRIOR_COMMON_COLUMNS
        + [
            "birth_year_range",
            "formative_year_range",
            "child_birth_year",
            "sex_gender",
            "age_group_at_child_birth",
            "education_level",
            "income_level",
            "religion_label",
            "urban_rural",
            "region",
            "ethnicity",
            "language",
            "packet_ids",
            "channel_ids",
        ]
    )),
}

V552_PARENT_PRIOR_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "parent_prior_manifest_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "position_signature_count",
        "attitude_domain_count",
        "parent_position_prior_rows",
        "parent_attitude_prior_rows",
        "parent_behavior_tendency_prior_rows",
        "parent_contradiction_prior_rows",
        "basis",
        "confidence_tier",
        "status",
        "known_absences",
        "forbidden_inference",
        "created_at",
    ],
}

V552_TO_V552J_HANDOFF_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "handoff_index_id",
        "artifact_name",
        "artifact_lane",
        "artifact_status",
        "artifact_path_csv",
        "artifact_path_parquet",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "runtime_use_class",
        "downstream_permission_class",
        "downstream_consumer_layer",
        "requires_directionality",
        "ready_for_v552j_inspection",
        "ready_for_v553_after_v552j",
        "known_absences_json",
        "v553_comparability_key",
        "temporal_anchor_hint",
        "comparability_status",
        "created_at",
        "schema_version",
    ]
}

V552_READINESS_REPORT_SCHEMA = {
    "required_columns": [
        "run_id",
        "v552_compile_status",
        "v552_structural_readiness",
        "v552_directionality_readiness",
        "v552_horizon_readiness",
        "v552_contradiction_readiness",
        "v552_parent_prior_readiness",
        "v552_v552j_handoff_readiness",
        "v552_v553_comparability_readiness",
        "v552_runtime_readiness",
        "ready_for_v552j_inspection",
        "ready_for_v553_after_v552j",
        "input_atom_count",
        "input_atom_rows",
        "category_empirical_object_count",
        "unique_empirical_distribution_count",
        "unique_empirical_object_count",
        "unique_empirical_object_grain",
        "pressure_observation_candidate_count",
        "observed_pressure_count",
        "observed_zero_pressure_count",
        "noncomputable_pressure_count",
        "review_required_pressure_count",
        "pressure_linkage_eligible_count",
        "exact_pressure_rollup_count",
        "heterogeneous_pressure_summary_count",
        "contradiction_row_count",
        "structural_channel_count",
        "invalid_output_contract_rows",
        "allowed_for_v553_temporal_field_count",
        "comparability_key_count",
        "temporal_anchor_hint_count",
        "final_status",
        "output_artifact_count",
        "artifact_authority_rows",
        "known_absence_rows",
        "handoff_index_rows",
        "comparability_key_count",
        "temporal_anchor_hint_count",
        "final_status",
        "created_at",
        "schema_version",
    ]
}

V552_STRUCTURAL_FACT_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "v552_structural_fact_id",
        "source_run_id",
        "source_artifact",
        "source_row_index",
        "source_row_id",
        "source_row_hash",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "structural_fact_type",
        "structural_fact_lane",
        "structural_fact_grain",
        "empirical_distribution_id",
        "component_response_surface_signature",
        "response_surface_completeness_status",
        "pressure_measure_class",
        "pressure_formula_id",
        "pressure_formula_version",
        "pressure_scale_id",
        "pressure_measurement_hash",
        "semantic_identity_signature",
        "structural_identity_signature",
        "response_scale_signature",
        "directionality_policy",
        "response_topology",
        "question_id",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "structural_channel_id",
        "horizon_constraint_id",
        "semantic_signature",
        "pressure_score",
        "entropy",
        "polarization_index",
        "dominant_orientation",
        "n_atoms",
        "n_unweighted_total",
        "n_weighted_total",
        "support_status",
        "confidence_tier",
        "directionality_coverage",
        "pressure_computation_status",
        "compiler_status",
        "structural_fact_status",
        "allowed_v552j_use",
        "forbidden_downstream_use",
        "known_absences_json",
        "source_trace_json",
        "source_artifact_row_count",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "v552_temporal_key_source_id",
        "v552_structural_fact_id",
        "source_run_id",
        "source_artifact",
        "source_row_index",
        "source_row_id",
        "source_row_hash",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "structural_fact_type",
        "structural_fact_lane",
        "structural_fact_grain",
        "empirical_distribution_id",
        "component_response_surface_signature",
        "response_surface_completeness_status",
        "pressure_measure_class",
        "pressure_formula_id",
        "pressure_formula_version",
        "pressure_scale_id",
        "pressure_measurement_hash",
        "semantic_identity_signature",
        "structural_identity_signature",
        "response_scale_signature",
        "directionality_policy",
        "response_topology",
        "question_id",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "structural_channel_id",
        "horizon_constraint_id",
        "semantic_signature",
        "temporal_key_grain",
        "temporal_key_basis",
        "temporal_key_candidate_status",
        "temporal_key_blocker_reason",
        "fallback_permission_profile_key",
        "fallback_used",
        "resolution_status",
        "allowed_downstream_use",
        "pressure_score",
        "pressure_score_status",
        "support_status",
        "confidence_tier",
        "directionality_coverage",
        "allowed_for_v552j",
        "allowed_for_v553_probe",
        "allowed_for_v553_temporal_field",
        "known_absences_json",
        "source_trace_json",
        "source_artifact_row_count",
        "created_at",
        "schema_version",
        "compiler_version",
    ]
}

V552_PRESSURE_COMPONENT_INDEX_SCHEMA = {
    "required_columns": [
        "run_id", "v552_pressure_component_id", "v552_pressure_observation_id", "source_atom_id", "source_atom_contract_hash",
        "source_measurement_contract_hash", "source_v551_run_id", "source", "source_family", "wave", "canonical_wave", "country_code",
        "survey_year", "analysis_scope", "empirical_object_type", "empirical_object_id", "empirical_distribution_id", "question_id", "var_code", "position_field",
        "position_value", "response_value_raw", "response_value_normalized", "normalized_response_label", "response_family",
        "response_direction", "response_direction_sign", "response_intensity", "source_intensity_zero", "scale_min", "scale_max",
        "scale_direction", "directionality_policy", "response_topology", "response_scale_signature", "scale_encoding_class",
        "scale_transform_id", "scale_encoding_status", "normalized_source_coordinate", "normalized_construct_magnitude",
        "canonical_signed_component", "canonical_signed_component_zero", "direction_scale_consistency_status", "n_unweighted",
        "n_respondents", "n_weighted", "pct_unweighted", "pct_weighted", "population_share", "weight_status",
        "distribution_weight_basis", "distribution_weight_raw", "distribution_weight_normalized", "component_pressure_eligible",
        "component_pressure_status", "component_pressure_ineligibility_reason", "semantic_identity_signature",
        "structural_identity_signature", "measurement_contract_hash", "evidence_basis_json", "provenance_basis_json",
        "component_measurement_hash", "created_at", "schema_version", "compiler_version",
    ]
}

V552_PRESSURE_OBSERVATION_INDEX_SCHEMA = {
    "required_columns": [
        "run_id", "v552_pressure_observation_id", "pressure_observation_identity_hash", "source_v551_run_id",
        "source_atom_ids_json", "source_atom_contract_hashes_json", "source_measurement_contract_hashes_json", "source",
        "source_family", "wave", "canonical_wave", "country_code", "survey_year", "analysis_scope", "empirical_object_type",
        "empirical_object_id", "empirical_object_id_role", "empirical_distribution_id", "empirical_parent_identity_class",
        "component_empirical_object_ids_json", "component_response_surface_signature",
        "response_surface_completeness_status", "response_surface_component_count", "response_surface_respondent_coverage",
        "response_surface_completeness_basis", "question_id", "var_code", "position_field", "position_value", "semantic_identity_signature",
        "structural_identity_signature", "response_scale_signature", "semantic_role", "semantic_subrole", "semantic_tags",
        "directionality_policy", "response_topology", "relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id",
        "strata_relevance", "strata_path", "subject_position_signature", "position_conditioning", "position_modifiers",
        "conditional_strata_weights", "horizon_affordance", "pressure_measure_class", "pressure_formula_id",
        "pressure_formula_version", "pressure_scale_id", "pressure_scale_min", "pressure_scale_max", "source_scale_min",
        "source_scale_max", "source_scale_direction", "scale_encoding_class", "scale_transform_id", "scale_encoding_status",
        "direction_scale_consistency_status", "distribution_weight_basis", "component_atom_count", "eligible_component_atom_count",
        "unique_response_component_count", "source_intensity_zero_component_count", "canonical_signed_zero_component_count",
        "distribution_mass_raw", "distribution_mass_used", "substantive_response_coverage", "respondent_denominator_unweighted",
        "weighted_response_mass", "pressure_score", "pressure_magnitude", "pressure_orientation", "pressure_score_status",
        "observed_pressure_zero", "positive_component_share", "negative_component_share", "neutral_component_share",
        "directional_entropy", "polarization_index", "dominant_orientation", "dominant_orientation_share",
        "component_signed_intensity_min", "component_signed_intensity_max", "component_signed_intensity_std",
        "support_status_rollup", "confidence_tier_rollup", "component_permission_status", "pressure_observation_status",
        "v552j_pressure_linkage_eligible", "v552j_structural_context_eligible", "v553_probe_candidate_after_v552j",
        "allowed_for_v553_temporal_field", "pressure_observation_ineligibility_reason", "known_absences_json",
        "forbidden_inference_json", "evidence_basis_json", "provenance_basis_json", "pressure_measurement_hash",
        "input_atom_hash", "created_at", "schema_version", "compiler_version",
    ]
}

V552_PRESSURE_OBSERVATION_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id", "candidate_group_id", "source", "canonical_wave", "country_code", "empirical_object_id", "empirical_distribution_id", "question_id", "var_code",
        "component_atom_count", "eligible_component_atom_count", "ineligible_component_atom_count", "review_required_component_atom_count",
        "component_permission_status", "identity_validation_status", "direction_validation_status", "intensity_validation_status",
        "weight_basis_status", "distribution_mass_status", "pressure_observation_status", "pressure_score_status", "pressure_score",
        "ineligibility_reasons", "source_atom_ids_json", "source_atom_contract_hashes_json", "created_at", "schema_version",
    ]
}

_V552_ROLLUP_V2_1_COLUMNS = [
    "n_pressure_observations", "n_unique_empirical_objects", "sample_n_min", "sample_n_max", "sample_n_median",
    "summed_component_atom_count", "summed_category_n_unweighted_audit", "semantic_identity_count",
    "structural_identity_count", "response_scale_signature_count", "rollup_identity_status",
    "v552j_pressure_linkage_eligible", "allowed_for_v553_temporal_field", "source_pressure_observation_ids_json",
]
for _schema in [
    V552_RELATION_AXIS_PRESSURE_SCHEMA,
    V552_TARGET_ENTITY_PRESSURE_SCHEMA,
    V552_DRIVER_FACET_PRESSURE_SCHEMA,
    V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA,
    V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA,
    V552_POSITION_CONDITIONING_PROFILE_SCHEMA,
]:
    _schema["required_columns"] = list(dict.fromkeys(_schema["required_columns"] + _V552_ROLLUP_V2_1_COLUMNS))

V552_STRUCTURAL_FACT_INDEX_SCHEMA["required_columns"] = list(dict.fromkeys(
    V552_STRUCTURAL_FACT_INDEX_SCHEMA["required_columns"]
    + [
        "fact_measure_class", "pressure_formula_id", "pressure_formula_version", "pressure_scale_id",
        "pressure_score_status", "source_pressure_observation_ids_json", "semantic_identity_signature",
        "structural_identity_signature", "response_scale_signature", "directionality_policy", "response_topology",
        "empirical_distribution_id", "component_response_surface_signature", "response_surface_completeness_status",
        "pressure_measurement_hash",
        "strata_path", "subject_position_signature", "position_conditioning", "pressure_anchor_candidate_after_v552j",
        "v552j_pressure_linkage_eligible", "v552j_structural_context_eligible", "v553_probe_candidate_after_v552j",
        "allowed_for_v553_temporal_field",
    ]
))

V552_READINESS_REPORT_SCHEMA["required_columns"] = list(dict.fromkeys(
    V552_READINESS_REPORT_SCHEMA["required_columns"]
    + [
        "status", "input_contract_status", "ready_for_v552j_structural_inspection", "ready_for_v552j_pressure_linkage",
        "ready_for_v553_direct", "input_atom_rows", "unique_empirical_object_count",
        "pressure_observation_candidate_count", "observed_pressure_count", "observed_zero_pressure_count",
        "noncomputable_pressure_count", "review_required_pressure_count", "pressure_linkage_eligible_count",
        "exact_pressure_rollup_count", "heterogeneous_pressure_summary_count", "contradiction_row_count",
        "structural_channel_count", "invalid_output_contract_rows", "allowed_for_v553_temporal_field_count",
        "category_empirical_object_count", "unique_empirical_distribution_count", "unique_empirical_object_grain",
        "comparability_key_count", "temporal_anchor_hint_count",
    ]
))

V552_HORIZON_CONSTRAINT_INDEX_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "horizon_constraint_id",
            "horizon_dimension",
            "basis_relation_axis_id",
            "basis_target_entity_id",
            "basis_driver_facet_id",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "constraint_signal_score",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "constraint_reason",
        ]
    )),
}

V552_STATUS_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "artifact_name",
        "artifact_path_csv",
        "artifact_path_parquet",
        "row_count",
        "input_atom_count",
        "eligible_atom_count",
        "compiler_status",
        "status_reason",
        "requires_directionality",
        "has_sufficient_directionality",
        "support_basis",
        "input_atom_hash",
        "input_hash",
        "schema_version",
        "created_at",
    ]
}

V552_DIRECTIONALITY_COVERAGE_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "grouping_level",
        "grouping_key",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "atom_count",
        "atoms_with_response_direction",
        "atoms_with_response_intensity",
        "atoms_with_both_direction_and_intensity",
        "directionality_coverage",
        "intensity_coverage",
        "both_coverage",
        "directionality_status",
        "input_atom_hash",
        "input_hash",
        "created_at",
    ]
}

V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "gap_surface_id",
        "gap_surface_scope",
        "gap_surface_reason",
        "gap_surface_priority",
        "n_atoms",
        "n_directional_atoms",
        "n_unsigned_atoms",
        "n_unweighted_total",
        "n_weighted_total",
        "directionality_coverage",
        "directionality_gap_score",
        "support_status",
        "confidence_tier",
        "pressure_computation_status",
        "basis",
        "status",
        "created_at",
    ]
}

V552_STATUS_PRESSURE_REVIEW_SCHEMA = {
    "required_columns": [
        "run_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "relation_axis_id",
        "target_entity_id",
        "driver_facet_id",
        "status_pressure_id",
        "status_pressure_scope",
        "status_pressure_reason",
        "status_pressure_priority",
        "n_atoms",
        "n_directional_atoms",
        "n_signed_atoms",
        "n_unsigned_atoms",
        "n_unweighted_total",
        "n_weighted_total",
        "directionality_coverage",
        "support_status",
        "confidence_tier",
        "pressure_computation_status",
        "basis",
        "status",
        "created_at",
    ]
}

V552_INPUT_PROVENANCE_MANIFEST_SCHEMA = {
    "required_fields": [
        "run_id",
        "created_at",
        "compiler",
        "compiler_scope",
        "atoms_path",
        "atoms_input_hash",
        "atoms_row_count",
        "atoms_required_columns_present",
        "atoms_missing_required_columns",
        "conditional_determinicity_path",
        "conditional_determinicity_hash",
        "conditional_determinicity_row_count",
        "output_root",
        "output_dir",
        "schema_version",
        "upstream_boundary_frozen",
        "upstream_files_modified",
        "v553_implemented",
        "parent_persona_implemented",
        "final_status",
    ]
}

V552_ARTIFACT_AUTHORITY_INDEX_SCHEMA = {
    "required_columns": [
        "run_id",
        "artifact_name",
        "artifact_path_csv",
        "artifact_path_parquet",
        "lane",
        "compiler_status",
        "status_reason",
        "requires_directionality",
        "structural_level_only",
        "not_runtime_consumable",
        "allowed_v552j_use",
        "forbidden_downstream_use",
        "created_at",
        "schema_version",
    ]
}

V552_KNOWN_ABSENCE_REGISTER_SCHEMA = {
    "required_columns": [
        "run_id",
        "absence_id",
        "artifact_name",
        "absence_type",
        "absence_status",
        "absence_reason",
        "missing_condition_json",
        "lane",
        "compiler_status",
        "requires_directionality",
        "created_at",
        "schema_version",
    ]
}

V552_CONDITIONAL_DETERMINICITY_STATUS_AUDIT_SCHEMA = {
    "required_columns": [
        "run_id",
        "conditional_input_path",
        "conditional_input_hash",
        "input_hash",
        "conditional_row_count",
        "status",
        "status_reason",
        "used_as_direct_pressure",
        "used_as_status_context",
        "created_at",
    ]
}

POSITION_DISTRIBUTION_SCHEMA = {
    "required_columns": [
        "run_id",
        "shard_id",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "country_code",
        "position_field",
        "position_value",
        "n_unweighted",
        "n_weighted",
        "pct_unweighted",
        "pct_weighted",
        "weight_status",
        "semantic_role",
        "created_at",
    ]
}

V551_BRIDGE_INDEX_SCHEMA = {
    "required_columns": list(dict.fromkeys([
        "run_id",
        "shard_id",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "country_code",
        "survey_year",
        "n_respondents",
        "analysis_scope",
        "empirical_object_type",
        "empirical_object_id",
        "source_table",
        "source_row_hash",
        "question_id",
        "var_code",
        "position_field",
        "position_value",
        "response_value_raw",
        "response_value_normalized",
        "response_label",
        "normalized_response_label",
        "response_family",
        "response_direction",
        "response_intensity",
        "polarity",
        "ordinal_rank",
        "scale_min",
        "scale_max",
        "scale_direction",
        "directionality_status",
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
        "eligibility_gate_status",
        "eligibility_failed_gates",
        "bridge_evidence_lane",
        "support_status",
        "support_gate_status",
        "support_threshold",
        "support_ratio",
        "support_ratio_margin",
        "support_score",
        "support_formula_id",
        "support_formula_version",
        "support_implementation_function",
        "support_score_family",
        "support_higher_is_better",
        "support_decision_role",
        "population_share",
        "prevalence_score",
        "prevalence_formula_id",
        "prevalence_formula_version",
        "prevalence_implementation_function",
        "prevalence_score_family",
        "prevalence_higher_is_better",
        "prevalence_decision_role",
        "v551_conditional_determinicity_eligible",
        "usable_for_evidence",
        "is_substantive",
        "is_missing",
        "is_special",
        "normalization_confidence",
        "response_option_map_matched",
        "response_semantics_status",
        "response_semantics_source",
        "response_semantics_contract_hash",
        "semantic_role",
        "v551_visible",
        "v551_evidence_role",
        "v551_context_eligible",
        "v551_position_coordinate_eligible",
        "v551_relation_evidence_eligible",
        "v551_cloud_eligible",
        "v551_persona_packet_eligible",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_id",
        "strata_relevance",
        "strata_path",
        "subject_position_signature",
        "mapping_status",
        "legacy_final_driver_id",
        "legacy_driver_leak_flag",
        "forbidden_inference",
        "known_absences",
        "manual_review_flag",
        "manual_review_reason",
        "question_type",
        "handling_rule",
        "recommended_computation",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_fields_joined",
        "source_structure_review_required",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
        "position_conditioning",
        "position_modifiers",
        "conditional_strata_weights",
        "horizon_affordance",
        "position_conditioning_note",
        "position_conditioning_confidence",
        "response_direction",
        "response_intensity",
        "polarity",
        "ordinal_rank",
        "scale_min",
        "scale_max",
        "scale_direction",
        "directionality_status",
        "bridge_evidence_lane",
        "support_status",
        "v551_conditional_determinicity_eligible",
        "usable_for_evidence",
        "n_unweighted",
        "n_respondents",
        "n_weighted",
        "pct_unweighted",
        "pct_weighted",
        "weight_status",
        "confidence_tier",
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
        "question_use_contract_joined",
        "v551_eligible",
        "v551_exclusion_reason",
        "v551_failed_gates",
        "v551_failed_gate_count",
        "evidence_basis",
        "provenance_basis",
        "created_at",
    ])),
}

QUESTION_USE_CONTRACT_SCHEMA = {
    "required_columns": [
        "source",
        "wave",
        "canonical_wave",
        "question_id",
        "var_code",
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
        "semantic_role_authority_status",
        "response_semantics_authority_status",
        "directionality_authority_status",
        "directional_applicability_status",
        "structural_mapping_status",
        "runtime_authority_status",
        "eligibility_gate_status",
        "eligibility_failed_gates",
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
        "relation_axis_id",
        "target_entity_id",
        "driver_id",
        "final_driver_scope",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_fields_joined",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
        "position_conditioning",
        "position_modifiers",
        "conditional_strata_weights",
        "horizon_affordance",
        "position_conditioning_note",
        "position_conditioning_confidence",
    ]
}

V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "question_semantic_hierarchy_id",
            "question_id",
            "var_code",
            "question_text",
            "facet_id",
            "facet_label",
            "driver_id",
            "driver_label",
            "stratum_id",
            "stratum_label",
            "semantic_role",
            "semantic_subrole",
            "semantic_tags",
            "directionality_policy",
            "semantic_confidence",
            "semantic_note",
            "relation_axis_id",
            "target_entity_id",
            "relation_axes",
            "target_entities",
            "facet_ids",
            "driver_ids",
            "strata_relevance",
            "strata_path",
            "conditional_strata_weights",
            "position_conditioning",
            "position_modifiers",
            "position_conditioning_confidence",
            "horizon_affordance",
            "horizon_type",
            "horizon_scope",
            "horizon_openness",
            "horizon_reach",
            "horizon_durability",
            "horizon_enemy_relation",
            "horizon_valence",
            "horizon_sustaining_power",
            "translation_status",
            "question_count",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

V552_FACET_SEMANTIC_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "facet_semantic_profile_id",
            "facet_id",
            "facet_label",
            "driver_id",
            "driver_label",
            "stratum_id",
            "stratum_label",
            "semantic_subrole",
            "semantic_tags",
            "directionality_policy",
            "horizon_type",
            "horizon_scope",
            "horizon_openness",
            "horizon_valence",
            "horizon_sustaining_power",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

V552_DRIVER_SEMANTIC_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "driver_semantic_profile_id",
            "driver_id",
            "driver_label",
            "stratum_id",
            "stratum_label",
            "facet_ids",
            "semantic_subrole",
            "semantic_tags",
            "directionality_policy",
            "horizon_type",
            "horizon_scope",
            "horizon_openness",
            "horizon_valence",
            "horizon_sustaining_power",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

V552_STRATUM_SEMANTIC_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "stratum_semantic_profile_id",
            "stratum_id",
            "stratum_label",
            "driver_ids",
            "facet_ids",
            "semantic_subrole",
            "semantic_tags",
            "horizon_type",
            "horizon_scope",
            "horizon_openness",
            "horizon_reach",
            "horizon_valence",
            "horizon_sustaining_power",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

V552_HORIZON_SEMANTIC_PROFILE_SCHEMA = {
    "required_columns": list(dict.fromkeys(
        V552_COMMON_STRUCTURAL_COLUMNS
        + [
            "horizon_semantic_profile_id",
            "horizon_type",
            "horizon_scope",
            "horizon_openness",
            "horizon_reach",
            "horizon_durability",
            "horizon_enemy_relation",
            "horizon_valence",
            "horizon_sustaining_power",
            "translation_status",
            "driver_ids",
            "facet_ids",
            "stratum_ids",
            "semantic_tags",
            "n_questions",
            "n_relation_axes",
            "n_target_entities",
            "n_driver_facets",
            "n_atoms",
            "n_unweighted_total",
            "n_weighted_total",
            "support_status",
            "confidence_tier",
            "basis",
            "status",
            "pressure_computation_status",
        ]
    )),
}

MERGE_MANIFEST_SCHEMA = {
    "required_columns": [
        "run_id",
        "created_at",
        "completed_at",
        "success",
        "shard_count_expected",
        "shard_count_actual",
        "missing_shards",
        "row_counts",
    ]
}


def infer_dtype(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_integer_dtype(series):
        return "int64"
    if pd.api.types.is_float_dtype(series):
        return "float64"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime64[ns]"
    return "string"


def dataframe_schema_json(df: pd.DataFrame, *, name: str, run_id: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "name": name,
        "run_id": run_id,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": [
            {
                "name": col,
                "dtype": infer_dtype(df[col]) if col in df.columns and len(df) else "string",
            }
            for col in df.columns
        ],
    }
    if extra:
        payload.update(extra)
    return payload


def write_schema_json(path: Path, df: pd.DataFrame, *, name: str, run_id: str, extra: dict[str, Any] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dataframe_schema_json(df, name=name, run_id=run_id, extra=extra), indent=2, ensure_ascii=False), encoding="utf-8")


def validate_columns(df: pd.DataFrame, required_columns: list[str], table_name: str) -> list[str]:
    missing = [col for col in required_columns if col not in df.columns]
    return [f"{table_name}: missing columns {missing}"] if missing else []


def _normalized_tokens(value: object) -> set[str]:
    text = str(value or "").strip().lower()
    if not text:
        return set()
    return {token for token in re.split(r"[^a-z0-9]+", text) if token}


def validate_no_forbidden_cloud_features(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    forbidden_tokens = {
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
        "respondent_id",
        "weight",
        "metadata::",
    }
    checked_columns = [
        col
        for col in [
            "cloud_feature",
            "feature_name",
            "anchor_var_code",
            "var_code",
            "predictor_family",
            "feature_kind",
            "driver_id",
            "relation_axis_id",
            "target_entity_id",
        ]
        if col in df.columns
    ]
    if not checked_columns:
        checked_columns = list(df.columns)
    for col in checked_columns:
        values = df[col].fillna("").astype(str)
        for token in forbidden_tokens:
            if not token:
                continue
            if values.apply(lambda value: token in _normalized_tokens(value)).any():
                return [f"attitude_cloud contains forbidden feature token in {col}: {token}"]
    return []


def forbidden_cloud_feature_row_count(df: pd.DataFrame, issue: str) -> int:
    if df.empty:
        return 0
    match = re.search(r"forbidden feature token in (?P<col>[^:]+): (?P<token>.+)$", str(issue))
    if not match:
        return int(len(df))
    column = match.group("col").strip()
    token = match.group("token").strip().lower()
    if not column or column not in df.columns or not token:
        return int(len(df))
    values = df[column].fillna("").astype(str)
    return int(values.apply(lambda value: token in _normalized_tokens(value)).sum())


def validate_bridge_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_BRIDGE_INDEX_SCHEMA["required_columns"], "v551_bridge_index")


def validate_v551_numeric_wrapper_audit(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_NUMERIC_WRAPPER_AUDIT_SCHEMA["required_columns"], "v551_numeric_wrapper_audit")


def validate_v551_relation_review_surface(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_RELATION_REVIEW_SURFACE_SCHEMA["required_columns"], "v551_relation_review_surface")


def validate_v551_blocked_signal_audit(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_BLOCKED_SIGNAL_AUDIT_SCHEMA["required_columns"], "v551_blocked_signal_audit")


def validate_shard_manifest(manifest: dict[str, Any]) -> list[str]:
    missing = [key for key in SHARD_MANIFEST_SCHEMA["required_columns"] if key not in manifest]
    return [f"shard_manifest: missing keys {missing}"] if missing else []
