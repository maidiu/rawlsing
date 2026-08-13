from __future__ import annotations

import sys
from pathlib import Path


CODE = Path(__file__).resolve().parents[1] / "runtime_reproducibility_code" / "data" / "ddm_build_copy"
sys.path.insert(0, str(CODE))

from ddm_v550_authority_contract import derive_question_use_eligibility  # noqa: E402

MATCHER = Path(__file__).resolve().parents[2] / "phase_d" / "code"
sys.path.insert(0, str(MATCHER))
from compile_positioned_relational_evidence import _impls_from_row  # noqa: E402


def test_blocked_relation_keeps_diagnostic_permission_without_v551_permission():
    result = derive_question_use_eligibility(
        {
            "semantic_role": "RELATION_EVIDENCE",
            "semantic_role_authority_status": "BLOCKED",
            "response_semantics_authority_status": "REVIEW_REQUIRED",
            "directionality_authority_status": "REVIEW_REQUIRED",
            "structural_mapping_status": "PENDING",
            "response_topology": "binary_contrast",
            "response_semantics_contract_hash": "contract-q306c",
            "review_required": True,
        }
    )
    assert result["allowed_as_attitude_cloud_anchor"] is True
    assert result["allowed_as_branch_relation_cosignature"] is True
    assert result["allowed_as_v551_relation_evidence"] is False
    assert result["current_directional_atom_eligible"] is False


def test_structural_context_can_be_diagnostic_feature_without_promotion():
    result = derive_question_use_eligibility(
        {
            "semantic_role": "STRUCTURAL_CONTEXT",
            "semantic_role_authority_status": "CERTIFIED",
            "response_semantics_authority_status": "REVIEW_REQUIRED",
            "directionality_authority_status": "NOT_APPLICABLE",
            "structural_mapping_status": "PENDING",
            "response_topology": "ranked_choice",
            "response_semantics_contract_hash": "contract-q305-1",
            "review_required": True,
        }
    )
    assert result["allowed_as_attitude_cloud_feature"] is True
    assert result["allowed_as_attitude_cloud_anchor"] is False
    assert result["allowed_as_v551_relation_evidence"] is False
    assert result["current_directional_atom_eligible"] is False


def test_technical_role_cannot_enter_diagnostic_surface():
    result = derive_question_use_eligibility(
        {
            "semantic_role": "ADMINISTRATIVE_METADATA",
            "response_topology": "scalar",
            "response_semantics_contract_hash": "contract-admin",
        }
    )
    assert result["allowed_as_attitude_cloud_anchor"] is False
    assert result["allowed_as_attitude_cloud_feature"] is False
    assert result["allowed_as_branch_relation_cosignature"] is False
    assert result["allowed_as_v551_relation_evidence"] is False


def test_cloud_matching_requires_exact_governed_ids_for_both_members():
    row = __import__("pandas").Series(
        {"anchor_var_code": "q306c", "cotravelling_var_code": "q305_1"}
    )
    resolved, basis, reference = _impls_from_row(
        row,
        item_crosswalk={
            "Q306C": "question_impl.phase0.q306c",
            "Q305_1": "question_impl.phase0.q305_1",
        },
    )
    assert resolved == {
        "question_impl.phase0.q306c",
        "question_impl.phase0.q305_1",
    }
    assert basis == "EXACT_GOVERNED_ITEM_CROSSWALK"
    assert "anchor_var_code:q306c" in reference
    assert "cotravelling_var_code:q305_1" in reference
