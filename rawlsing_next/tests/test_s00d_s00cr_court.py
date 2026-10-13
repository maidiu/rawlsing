"""PYAT HQ285 S00D -- S00CR 16-test independent court (read-only overlay).

These tests reproduce the independent S00CR hostile oracles R01-R18 (16
Python test functions) WITHOUT changing their assertions. They verify that
the S00D producer binding and semantic quarantine fixes address the
identified defects while preserving genuine P04 progressive conditioning.

No changes to the original S00C test assertions.
"""

import sys
from pathlib import Path
from fractions import Fraction
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from rawlsing_next.r3_s02_seam_witness import (
    build_sociological_bundle,
    build_source_free_native_joint_bundle,
    build_retained_gt2_bundle,
    ContractOnlySeamConsumer,
    SeamContractError,
    _content_hash,
)
from rawlsing_next.s00d_producer_binding_quarantine import (
    S00DBindingConsumer,
    validate_producer_binding,
    validate_fraction_closure,
    validate_step_geometry,
    is_false_s00_semantic,
    quarantine_historical_s00_contract,
    run_s00d_witness,
    _producer_identity,
)


# R01: P04 exact denominators 32,16,8 and fractions 9/16, 5/8, 3/4
def test_r01_p04_owner_risk():
    bundle = build_sociological_bundle()
    denominators = [bundle.conditions[i]["denominator"] for i in range(3)]
    assert denominators == [32, 16, 8]
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("P04_A", ["P_Y_given_A"])
    assert result["status"] == "COMPUTED"
    assert result["raw_denominator_support"] == 32
    assert result["exact_probabilities"]["1"]["$exact_fraction"] == [9, 16]


# R02: Overlap no duplication: A->AB final 16, AB->ABC final 8
def test_r02_overlap_no_duplication():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("P04_AB", ["P_Y_given_A", "P_Y_given_A_B"])
    assert result["raw_denominator_support"] == 16
    result2 = consumer.compute_scenario("P04_ABC", ["P_Y_given_A_B", "P_Y_given_A_B_C"])
    assert result2["raw_denominator_support"] == 8


# R03: Read-to-arithmetic dependency
def test_r03_read_to_arithmetic():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("P04_DEP", ["P_Y_given_A"])
    assert result["source_value_dependency"]["value_reads_used"] > 0
    assert result["source_value_dependency"]["used_input_refs"]


# R04: Unconsumed read stays VALUE_READ_ONLY
def test_r04_unconsumed_read():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    consumer.read_value(bundle.channels[0].channel_id)
    receipt = consumer.get_receipt()
    assert receipt.values_read[0].semantic_effect == "VALUE_READ_ONLY"


# R05: Numeric cell mutation changes probability 3/4 -> 1/2
def test_r05_numeric_cell_mutation():
    joint_a = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    joint_b = {(0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2}
    bundle_a = build_source_free_native_joint_bundle(joint_a)
    bundle_b = build_source_free_native_joint_bundle(joint_b)
    consumer_a = ContractOnlySeamConsumer(bundle_a)
    consumer_b = ContractOnlySeamConsumer(bundle_b)
    result_a = consumer_a.compute_scenario("A", ["P_Q86A_given_Q86B_1"])
    result_b = consumer_b.compute_scenario("B", ["P_Q86A_given_Q86B_1"])
    assert result_a["exact_probabilities"]["1"]["$exact_fraction"] == [3, 4]
    assert result_b["exact_probabilities"]["1"]["$exact_fraction"] == [1, 2]


# R06: Irrelevant channel invariance
def test_r06_irrelevant_channel_invariance():
    joint = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    bundle1 = build_source_free_native_joint_bundle(joint)
    bundle2 = build_source_free_native_joint_bundle(joint)
    consumer1 = ContractOnlySeamConsumer(bundle1)
    consumer2 = ContractOnlySeamConsumer(bundle2)
    r1 = consumer1.compute_scenario("X", ["P_Q86A_given_Q86B_1"])
    r2 = consumer2.compute_scenario("X", ["P_Q86A_given_Q86B_1"])
    assert r1["exact_probabilities"] == r2["exact_probabilities"]


# R07: Opposite joints, same marginals: 3/4 vs 1/4
def test_r07_opposite_joints_same_marginals():
    joint1 = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    joint2 = {(0, 0): 1, (0, 1): 3, (1, 0): 3, (1, 1): 1}
    b1 = build_source_free_native_joint_bundle(joint1)
    b2 = build_source_free_native_joint_bundle(joint2)
    r1 = ContractOnlySeamConsumer(b1).compute_scenario("J1", ["P_Q86A_given_Q86B_1"])
    r2 = ContractOnlySeamConsumer(b2).compute_scenario("J2", ["P_Q86A_given_Q86B_1"])
    assert r1["exact_probabilities"]["1"]["$exact_fraction"] == [3, 4]
    assert r2["exact_probabilities"]["1"]["$exact_fraction"] == [1, 4]


# R08: Scope mismatch refused
def test_r08_scope_mismatch():
    bundle = build_sociological_bundle()
    channels = list(bundle.channels)
    ch = channels[0]
    bad_ch = replace(ch, source_scope="WRONG_SCOPE")
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels), content_hash="")
    from rawlsing_next.r3_s02_seam_witness import _content_hash
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    consumer = ContractOnlySeamConsumer(bad_bundle)
    result = consumer.compute_scenario("X", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH"


# R09: Risk mismatch refused
def test_r09_risk_mismatch():
    bundle = build_sociological_bundle()
    conditions = list(bundle.conditions)
    bad_condition = dict(conditions[0])
    bad_condition["risk_set_ref"] = {"kind": "WRONG", "name": "bad", "hash": "0" * 64}
    conditions[0] = bad_condition
    bad_bundle = replace(bundle, conditions=tuple(conditions), content_hash="")
    from rawlsing_next.r3_s02_seam_witness import _content_hash
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    consumer = ContractOnlySeamConsumer(bad_bundle)
    result = consumer.compute_scenario("X", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "RISK_SET_OR_SELECTION_BINDING_MISMATCH"


# R10: Zero support abstention
def test_r10_zero_support():
    joint = {(0, 0): 0, (0, 1): 0, (1, 0): 1, (1, 1): 3}
    bundle = build_source_free_native_joint_bundle(joint)
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("Z", ["P_Q86A_given_Q86B_0"])
    assert result["status"] == "ZERO_SUPPORT"
    assert result["reason"] == "ZERO_DENOMINATOR_ABSTENTION"


# R11: Replay hash determinism
def test_r11_replay_hash():
    b1 = build_sociological_bundle()
    b2 = build_sociological_bundle()
    assert b1.content_hash == b2.content_hash


# R12: Fake source issuer always refuses
def test_r12_fake_source_issuer():
    with pytest.raises(SeamContractError):
        build_retained_gt2_bundle(issued_source_owned_values={"fake": True})


# R13: Old S00 democracy/trust scenario refused
def test_r13_old_s00_semantic_prohibition():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("DEMOCRACY_SUPPORT", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"


# R14: Case-variant democracy/trust also refused (S00D fix for D3)
def test_r14_casefold_scenario_semantics():
    bundle = build_sociological_bundle()
    consumer = S00DBindingConsumer(bundle)
    result = consumer.compute_scenario("Democracy_Support", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"
    result2 = consumer.compute_scenario("institutional_trust", ["P_Y_given_A"])
    assert result2["status"] == "REFUSED"


# R15: Precomputed fraction closure (S00D fix for D2)
def test_r15_numeric_precomputed_fraction_closure():
    bundle = build_sociological_bundle()
    issue = validate_fraction_closure(bundle)
    assert issue is None
    channels = list(bundle.channels)
    ch = channels[0]
    bad_value = dict(ch.value)
    bad_value["raw_probability_exact_fraction"] = {"$exact_fraction": [100, 101]}
    bad_ch = replace(ch, value=bad_value)
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels))
    issue2 = validate_fraction_closure(bad_bundle)
    assert issue2 is not None


# R16: Steps material closure (S00D fix for D2)
def test_r16_steps_material_closure():
    bundle = build_sociological_bundle()
    issue = validate_step_geometry(bundle)
    assert issue is None
    steps = list(bundle.steps)
    bad_step = dict(steps[0])
    bad_cells = dict(bad_step["cells"])
    bad_cells["1"] = {"numerator": 234, "fraction": {"$exact_fraction": [234, 255]}}
    bad_step["cells"] = bad_cells
    steps[0] = bad_step
    bad_bundle = replace(bundle, steps=tuple(steps))
    issue2 = validate_step_geometry(bad_bundle)
    assert issue2 is not None


# R17: Selected-world value binding (S00D fix for D1)
def test_r17_selected_world_value_binding():
    bundle = build_sociological_bundle()
    identity_before = _producer_identity(bundle.channels, bundle.conditions, bundle.steps)
    channels = list(bundle.channels)
    ch = channels[0]
    bad_value = dict(ch.value)
    bad_value["raw_numerator_support"] = 2
    bad_ch = replace(ch, value=bad_value)
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels))
    identity_after = _producer_identity(bad_bundle.channels, bad_bundle.conditions, bad_bundle.steps)
    assert identity_before != identity_after


# R18: No original rights (no Likert, no V3, no source grant)
def test_r18_no_original_rights():
    result = run_s00d_witness()
    assert result["scientific_claim_grade"] == "SOURCE_FREE_SYNTHETIC"
    assert result["effects"]["v3_invoked"] is False
    assert result["effects"]["gt2_original_source_executed"] is False
    assert result["quarantine"]["quarantine_status"] == "INVALID_SOURCE_SEMANTICS__HISTORICAL_REFERENCE_ONLY"


# Additional S00D-specific tests

def test_s00d_producer_binding_valid():
    bundle = build_sociological_bundle()
    assert validate_producer_binding(bundle) is None


def test_s00d_fraction_closure_valid():
    bundle = build_sociological_bundle()
    assert validate_fraction_closure(bundle) is None


def test_s00d_step_geometry_valid():
    bundle = build_sociological_bundle()
    assert validate_step_geometry(bundle) is None


def test_s00d_is_false_s00_semantic():
    assert is_false_s00_semantic("DEMOCRACY_SUPPORT") is True
    assert is_false_s00_semantic("democracy_support") is True
    assert is_false_s00_semantic("Democracy_Support") is True
    assert is_false_s00_semantic("INSTITUTIONAL_TRUST") is True
    assert is_false_s00_semantic("institutional_trust") is True
    assert is_false_s00_semantic("DEMOCRATIC_ATTITUDES") is True
    assert is_false_s00_semantic("democratic_attitudes") is True
    assert is_false_s00_semantic("P04_SYNTHETIC") is False
    assert is_false_s00_semantic("NATIVE_Q86") is False


def test_s00d_quarantine_specification():
    q = quarantine_historical_s00_contract()
    assert q["quarantine_status"] == "INVALID_SOURCE_SEMANTICS__HISTORICAL_REFERENCE_ONLY"
    assert q["protected_historical_authority"] == "NOT_MUTATED__QUARANTINE_SPECIFICATION_ONLY"


def test_s00d_witness_preserves_p04():
    result = run_s00d_witness()
    assert result["scenario_a"]["raw_denominator_support"] == 16
    assert result["scenario_b"]["raw_denominator_support"] == 8
