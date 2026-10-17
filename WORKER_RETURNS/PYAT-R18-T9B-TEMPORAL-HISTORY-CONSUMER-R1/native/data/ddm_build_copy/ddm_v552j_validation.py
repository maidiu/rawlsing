#!/usr/bin/env python3
"""Validation helpers for the provisional V552J structural handoff adapter."""

from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v552j_schema import (
    V552J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
    V552J_INPUT_ARTIFACT_AUDIT_SCHEMA,
    V552J_STATUS_CONFLICT_AUDIT_SCHEMA,
    V552J_PERMISSION_BOUNDARY_AUDIT_SCHEMA,
    V552J_DOWNSTREAM_LEAKAGE_AUDIT_SCHEMA,
    V552J_READINESS_REPORT_SCHEMA,
    V552J_RUNTIME_HANDOFF_MANIFEST_SCHEMA,
    V552J_BLOCKED_INDEX_SCHEMA,
    V552J_DIAGNOSTIC_ONLY_INDEX_SCHEMA,
    V552J_REVIEW_ONLY_INDEX_SCHEMA,
    V552J_STRUCTURAL_CONTEXT_PACKET_SCHEMA,
    V552J_STRUCTURAL_ABSENCE_PACKET_SCHEMA,
    V552J_STRUCTURAL_CONSTRAINT_PACKET_SCHEMA,
    V552J_STRUCTURAL_CONTEXT_ONLY_INDEX_SCHEMA,
    V552J_STRUCTURAL_UNCERTAINTY_PACKET_SCHEMA,
    V552J_TO_V553_HANDOFF_INDEX_SCHEMA,
    V552J_V553_HANDOFF_MANIFEST_SCHEMA,
    validate_required_columns,
)


def validate_structural_constraint_packet(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STRUCTURAL_CONSTRAINT_PACKET_SCHEMA["required_columns"], "v552j_structural_constraint_packet")


def validate_structural_context_packet(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STRUCTURAL_CONTEXT_PACKET_SCHEMA["required_columns"], "v552j_structural_context_packet")


def validate_structural_absence_packet(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STRUCTURAL_ABSENCE_PACKET_SCHEMA["required_columns"], "v552j_structural_absence_packet")


def validate_structural_uncertainty_packet(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STRUCTURAL_UNCERTAINTY_PACKET_SCHEMA["required_columns"], "v552j_structural_uncertainty_packet")


def validate_forbidden_inference_audit(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA["required_columns"], "v552j_forbidden_inference_audit")


def validate_input_artifact_audit(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_INPUT_ARTIFACT_AUDIT_SCHEMA["required_columns"], "v552j_input_artifact_audit")


def validate_status_conflict_audit(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STATUS_CONFLICT_AUDIT_SCHEMA["required_columns"], "v552j_status_conflict_audit")


def validate_permission_boundary_audit(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_PERMISSION_BOUNDARY_AUDIT_SCHEMA["required_columns"], "v552j_permission_boundary_audit")


def validate_downstream_leakage_audit(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_DOWNSTREAM_LEAKAGE_AUDIT_SCHEMA["required_columns"], "v552j_downstream_leakage_audit")


def validate_structural_context_only_index(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_STRUCTURAL_CONTEXT_ONLY_INDEX_SCHEMA["required_columns"], "v552j_structural_context_only_index")


def validate_review_only_index(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_REVIEW_ONLY_INDEX_SCHEMA["required_columns"], "v552j_review_only_index")


def validate_diagnostic_only_index(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_DIAGNOSTIC_ONLY_INDEX_SCHEMA["required_columns"], "v552j_diagnostic_only_index")


def validate_blocked_index(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_BLOCKED_INDEX_SCHEMA["required_columns"], "v552j_blocked_index")


def validate_to_v553_handoff_index(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_TO_V553_HANDOFF_INDEX_SCHEMA["required_columns"], "v552j_to_v553_handoff_index")


def validate_v553_handoff_manifest(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_V553_HANDOFF_MANIFEST_SCHEMA["required_columns"], "v552j_v553_handoff_manifest")


def validate_runtime_handoff_manifest(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_RUNTIME_HANDOFF_MANIFEST_SCHEMA["required_columns"], "v552j_runtime_handoff_manifest")


def validate_readiness_report(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V552J_READINESS_REPORT_SCHEMA["required_columns"], "v552j_readiness_report")


__all__ = [
    "validate_structural_constraint_packet",
    "validate_structural_context_packet",
    "validate_structural_absence_packet",
    "validate_structural_uncertainty_packet",
    "validate_forbidden_inference_audit",
    "validate_input_artifact_audit",
    "validate_status_conflict_audit",
    "validate_permission_boundary_audit",
    "validate_downstream_leakage_audit",
    "validate_structural_context_only_index",
    "validate_review_only_index",
    "validate_diagnostic_only_index",
    "validate_blocked_index",
    "validate_to_v553_handoff_index",
    "validate_v553_handoff_manifest",
    "validate_runtime_handoff_manifest",
    "validate_readiness_report",
]
