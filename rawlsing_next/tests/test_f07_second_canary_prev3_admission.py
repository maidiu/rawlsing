from __future__ import annotations

import copy

import pytest

from rawlsing_next.f07_second_canary_prev3_admission import (
    ADMISSION_OPERATION,
    AUTHORITY_SHA256,
    CLAIM_ID,
    E10_AUTHORITY_REF,
    EXPECTED_TYPED_STATE,
    RELATION_FAMILY,
    RELATION_IDENTITY_SHA256,
    REPLAY_KEY_SHA256,
    ROSTER_ARTIFACT_SHA256,
    TARGET_USE,
    V554_RULE_REF,
    SecondCanaryIntegrity,
    build_source_snapshot,
    evaluation_material,
    execute_current_second_canary,
    execute_second_canary_m1,
    instantiate_second_canary_admission,
    load_current_governed_inputs,
    prepare_second_canary_m1,
    validate_governed_inputs,
)
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_M1_CONTRACT_ID,
    RelationPreparationState,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState


def _inputs():
    return load_current_governed_inputs()


def test_exact_current_e10_d09_inputs_validate_and_snapshot_losslessly():
    inputs = _inputs()
    validate_governed_inputs(inputs)
    snapshot = build_source_snapshot(inputs)
    assert set(snapshot["records"]) == set(inputs)
    assert snapshot["records"] == {name: inputs[name] for name in sorted(inputs)}
    assert len(snapshot["snapshot_sha256"]) == 64


def test_exact_one_receipt_preserves_authority_permission_roster_and_full_roster_ref():
    receipt = instantiate_second_canary_admission(_inputs())
    assert receipt["schema_id"] == "PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0"
    assert receipt["field_forge_relation_ref"]["object_id"] == CLAIM_ID
    assert receipt["field_forge_relation_ref"]["content_hash"] == RELATION_IDENTITY_SHA256
    assert receipt["admission_authority_ref"] == E10_AUTHORITY_REF
    assert receipt["target_use_permission_refs"] == [f"permission:{TARGET_USE}"]
    assert receipt["f07_instantiation"]["permission_ceiling"] == [TARGET_USE]
    assert receipt["f07_instantiation"]["typed_state_summary"] == EXPECTED_TYPED_STATE
    full_roster = receipt["applicable_negative_denial_noncomparability_refs"][0]["full_roster_artifact"]
    assert full_roster == {
        "name": "03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz",
        "sha256": ROSTER_ARTIFACT_SHA256,
        "observed_states": 812,
    }
    assert receipt["f07_instantiation"]["gt2_rule_reuse"] == "DENIED"
    assert receipt["f07_instantiation"]["m3_promotion"] == "DENIED"
    assert receipt["f07_instantiation"]["person_state_promotion"] == "DENIED"
    assert receipt["f07_instantiation"]["publication_authority"] == "NONE"


def test_exact_receipt_identity_is_deterministic():
    inputs = _inputs()
    a = instantiate_second_canary_admission(inputs)
    b = instantiate_second_canary_admission(inputs)
    assert a == b
    assert a["field_forge_relation_admission_id"].endswith(
        a["field_forge_relation_admission_content_hash"]
    )


def test_existing_m1_v554_ingress_accepts_and_same_input_replay_is_identical():
    inputs = _inputs()
    receipt = instantiate_second_canary_admission(inputs)
    prep = prepare_second_canary_m1(receipt, inputs)
    assert prep.state is RelationPreparationState.RELATION_BASIS_READY
    first = execute_second_canary_m1(receipt, inputs)
    second = execute_second_canary_m1(receipt, inputs)
    assert first.contract_id == RELATION_M1_CONTRACT_ID
    assert first.decision_state is M1DecisionState.ELIGIBLE
    assert first.support_count == 1
    assert first.f1 is not None
    assert first.f1["material"]["rule_id"] == ADMISSION_OPERATION
    assert first.f1["material"]["rule_hash"] == AUTHORITY_SHA256
    assert evaluation_material(first) == evaluation_material(second)


def test_current_entrypoint_seals_receipt_and_m1_replay():
    result = execute_current_second_canary()
    assert result["admission_receipt"]["field_forge_relation_ref"]["object_id"] == CLAIM_ID
    assert result["m1_evaluation"]["decision_state"] == "ELIGIBLE"
    assert len(result["m1_replay_sha256"]) == 64


def test_f07_uses_e10_operation_identity_not_gt2_rule_family():
    assert V554_RULE_REF == {
        "id": ADMISSION_OPERATION,
        "version": "1.0.0",
        "hash": AUTHORITY_SHA256,
    }
    assert "GT2" not in V554_RULE_REF["id"]
    assert "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE" not in RELATION_FAMILY


def test_e10_authority_hash_mismatch_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["e10_authority"]["authority_key_sha256"] = "0" * 64
    with pytest.raises(SecondCanaryIntegrity, match="authority identity mismatch"):
        instantiate_second_canary_admission(inputs)


def test_relation_family_or_claim_substitution_fails_closed():
    for field, replacement in [
        ("relation_family", "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"),
        ("claim_id", "GT2_Q86B_Q86A"),
    ]:
        inputs = copy.deepcopy(_inputs())
        inputs["e10_authority"]["relation_identity_key"][field] = replacement
        with pytest.raises(SecondCanaryIntegrity):
            instantiate_second_canary_admission(inputs)


def test_operand_coordinate_or_order_mutation_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["e10_authority"]["relation_identity_key"]["participants"][0]["source_variable"] = "Q86B"
    with pytest.raises(SecondCanaryIntegrity):
        instantiate_second_canary_admission(inputs)

    inputs = copy.deepcopy(_inputs())
    p = inputs["e10_authority"]["relation_identity_key"]["participants"]
    p[0], p[1] = p[1], p[0]
    with pytest.raises(SecondCanaryIntegrity):
        instantiate_second_canary_admission(inputs)


def test_state_deletion_or_exact_zero_reinterpretation_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["e10_replay_ledger"]["typed_state_preservation"]["zero_denominator_abstentions"]["count"] = 370
    with pytest.raises(SecondCanaryIntegrity, match="typed-state roster mismatch"):
        instantiate_second_canary_admission(inputs)

    inputs = copy.deepcopy(_inputs())
    inputs["e10_replay_ledger"]["typed_state_preservation"]["exact_zero_difference"]["count"] = 125
    with pytest.raises(SecondCanaryIntegrity, match="typed-state roster mismatch"):
        instantiate_second_canary_admission(inputs)


def test_permission_widening_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["e10_authority"]["authority_key"]["allowed_permission_subset"].append(
        "M3_HIGHER_ORDER_POSITIVE_PRODUCTION"
    )
    with pytest.raises(SecondCanaryIntegrity):
        instantiate_second_canary_admission(inputs)


def test_support_or_replay_identity_mutation_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["e10_authority"]["relation_identity_key"]["frozen_hashes"]["support_uncertainty"] = "0" * 64
    with pytest.raises(SecondCanaryIntegrity):
        instantiate_second_canary_admission(inputs)

    inputs = copy.deepcopy(_inputs())
    inputs["e10_replay_ledger"]["replay_key_sha256"] = "0" * 64
    with pytest.raises(SecondCanaryIntegrity, match="replay identity mismatch"):
        instantiate_second_canary_admission(inputs)


def test_d09_evidence_or_roster_artifact_mutation_fails_closed():
    inputs = copy.deepcopy(_inputs())
    inputs["d09_evidence_receipt"]["artifact_sha256"]["03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz"] = "0" * 64
    with pytest.raises(SecondCanaryIntegrity, match="roster evidence mismatch"):
        instantiate_second_canary_admission(inputs)


def test_instantiated_receipt_permission_or_authority_mutation_becomes_typed_integrity_failure():
    inputs = _inputs()
    receipt = instantiate_second_canary_admission(inputs)
    widened = copy.deepcopy(receipt)
    widened["target_use_permission_refs"].append("permission:M3_HIGHER_ORDER_POSITIVE_PRODUCTION")
    prep = prepare_second_canary_m1(widened, inputs)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE

    changed = copy.deepcopy(receipt)
    changed["admission_authority_ref"]["authority_content_hash"] = "0" * 64
    prep = prepare_second_canary_m1(changed, inputs)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE


def test_exact_binding_hash_constants_remain_frozen():
    assert AUTHORITY_SHA256 == "33c6f8b2e33758ef91d57d3eb3fa8bab7c65dfb7a6498495fb08d5261dc3a5fd"
    assert RELATION_IDENTITY_SHA256 == "1a3b1d28cecdb5b06c7b8ac927848249693324da733d1ee9649a94e50d4322ee"
    assert REPLAY_KEY_SHA256 == "0615a8668d87c5641c8a7bba4b144011d297c653a5369d6db2bd979e824fd19d"
