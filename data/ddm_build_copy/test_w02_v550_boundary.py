#!/usr/bin/env python3
"""W02-A regression tests for the V550 applicability/projection boundary."""
from __future__ import annotations

import ast
from pathlib import Path

from data.ddm_build_copy.ddm_v550_authority_contract import (
    APPLICABILITY_UNRESOLVED,
    APPLICABLE_BY_AUTHORITY,
    NOT_APPLICABLE_BY_AUTHORITY,
    derive_question_use_eligibility,
)
from data.ddm_build_copy.ddm_v550_bridge import _apply_directionality_overlay


def _applicable_row(**overrides):
    row = {
        "semantic_role": "RELATION_EVIDENCE",
        "semantic_role_authority_status": "CERTIFIED",
        "response_semantics_authority_status": "CERTIFIED",
        "response_topology": "scalar",
        "directionality_authority_status": "CERTIFIED",
        "source_structure_fields_joined": True,
        "mapping_status": "complete",
        "relation_axis_id": "institutional_trust",
        "target_entity_id": "government",
        "review_required": False,
    }
    row.update(overrides)
    return row


def test_applicability_survives_nonpromotable_response_and_structure_state():
    result = derive_question_use_eligibility(
        _applicable_row(
            response_semantics_authority_status="MISSING",
            source_structure_fields_joined=False,
            review_required=True,
        )
    )
    assert result["directional_applicability_status"] == APPLICABLE_BY_AUTHORITY
    assert result["current_directional_atom_eligible"] is True
    assert result["allowed_as_v551_relation_evidence"] is False


def test_row_level_directional_certification_cannot_create_applicability():
    result = derive_question_use_eligibility(
        _applicable_row(
            directionality_authority_status="",
            directional_certification_status="CERTIFIED",
        )
    )
    assert result["directional_applicability_status"] == APPLICABILITY_UNRESOLVED
    assert result["current_directional_atom_eligible"] is False
    assert result["allowed_as_v551_relation_evidence"] is False


def test_nonrelation_or_nondirectional_topology_is_not_applicable():
    role_result = derive_question_use_eligibility(
        _applicable_row(semantic_role="STRUCTURAL_CONTEXT")
    )
    topology_result = derive_question_use_eligibility(
        _applicable_row(response_topology="nominal_multicategory")
    )
    assert role_result["directional_applicability_status"] == NOT_APPLICABLE_BY_AUTHORITY
    assert topology_result["directional_applicability_status"] == NOT_APPLICABLE_BY_AUTHORITY


def test_v550_overlay_compatibility_helper_never_projects_signed_fields():
    direction, intensity, polarity, scale_direction, status = _apply_directionality_overlay(
        response_family="agreement_scale",
        response_label="Neither agree nor disagree",
        response_direction="positive",
        response_intensity=0.5,
        polarity="positive",
        scale_direction="ascending_positive",
        directionality_status="CERTIFIED",
        ordinal_rank=3,
        scale_min=1,
        scale_max=5,
        overlay_row={
            "signed_polarity_status": "signed_attitude",
            "bridge_directionality_action": "project",
            "manual_review_required": False,
        },
    )
    assert direction == ""
    assert polarity == ""
    assert scale_direction == ""
    assert intensity == 0.5
    assert status == "NOT_PROJECTED_V550"


def test_manual_review_overlay_stays_unsigned_and_preserves_raw_intensity():
    direction, intensity, polarity, scale_direction, status = _apply_directionality_overlay(
        response_family="ordinal_scale",
        response_label="3",
        response_direction="negative",
        response_intensity=0.5,
        polarity="negative",
        scale_direction="ascending_positive",
        directionality_status="CERTIFIED",
        ordinal_rank=3,
        scale_min=1,
        scale_max=5,
        overlay_row={"manual_review_required": True},
    )
    assert (direction, polarity, scale_direction) == ("", "", "")
    assert intensity == 0.5
    assert status == "manual_review_required_by_directionality_overlay"


def test_bridge_numeric_label_helpers_have_single_effective_definition():
    bridge_path = Path(__file__).with_name("ddm_v550_bridge.py")
    module = ast.parse(bridge_path.read_text(encoding="utf-8"))
    names = [node.name for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for helper in (
        "_is_numeric_only_label",
        "_response_family_allows_numeric_only_label",
        "_numeric_only_label_allowed",
    ):
        assert names.count(helper) == 1, f"duplicate helper definition: {helper}"
