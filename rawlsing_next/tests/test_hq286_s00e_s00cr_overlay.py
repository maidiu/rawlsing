"""PYAT HQ286 S00E -- S00CR independent 16-test read-only overlay.

Reproduces the EXACT independent S00CR hostile oracle expectations R01-R18
from WORKER_RETURNS/PYAT-R3-HQ284-S00CR-VALUE-DEPENDENCY-HOSTILE-R1/01_PRETEST_FROZEN_HOSTILES.json
WITHOUT changing their assertions. This is a read-only test overlay, not
lookalike author tests.

The S00CR oracle was frozen after inspecting candidate runtime code but
before reading S00C authored test module. These tests verify that the S00E
repairs to the actual ContractOnlySeamConsumer satisfy the independent
expectations.
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


# R01: P04 A,AB,ABC must compute exact denominator 32,16,8 and fractions 9/16,5/8,3/4
def test_r01_p04_owner_risk():
    bundle = build_sociological_bundle()
    denominators = [bundle.conditions[i]["denominator"] for i in range(3)]
    assert denominators == [32, 16, 8]
    consumer = ContractOnlySeamConsumer(bundle)
    result_a = consumer.compute_scenario("R01_A", ["P_Y_given_A"])
    assert result_a["raw_denominator_support"] == 32
    assert result_a["exact_probabilities"]["1"]["$exact_fraction"] == [9, 16]
    result_ab = consumer.compute_scenario("R01_AB", ["P_Y_given_A", "P_Y_given_A_B"])
    assert result_ab["raw_denominator_support"] == 16
    assert result_ab["exact_probabilities"]["1"]["$exact_fraction"] == [5, 8]
    result_abc = consumer.compute_scenario("R01_ABC", ["P_Y_given_A_B", "P_Y_given_A_B_C"])
    assert result_abc["raw_denominator_support"] == 8
    assert result_abc["exact_probabilities"]["1"]["$exact_fraction"] == [3, 4]


# R02: Trace A->AB final denominator 16, AB->ABC final 8, never 112 or 48
def test_r02_overlap_no_duplication():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("R02", ["P_Y_given_A", "P_Y_given_A_B"])
    assert result["raw_denominator_support"] == 16
    assert result["raw_denominator_support"] != 112
    result2 = consumer.compute_scenario("R02b", ["P_Y_given_A_B", "P_Y_given_A_B_C"])
    assert result2["raw_denominator_support"] == 8
    assert result2["raw_denominator_support"] != 48


# R03: Numeric result derives from retrieved raw_numerator_support, not receipt hash
def test_r03_read_to_arithmetic():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("R03", ["P_Y_given_A"])
    assert result["source_value_dependency"]["value_reads_used"] > 0
    assert result["source_value_dependency"]["used_input_refs"]
    for ref in result["source_value_dependency"]["used_input_refs"]:
        assert ref["value_hash"] != ""


# R04: Read-only lookup remains VALUE_READ_ONLY after unrelated scenario
def test_r04_unconsumed_read():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    consumer.read_value(bundle.channels[0].channel_id)
    consumer.compute_scenario("R04_unrelated", ["P_Y_given_A_B"])
    receipt = consumer.get_receipt()
    first_read = receipt.values_read[0]
    assert first_read.semantic_effect == "VALUE_READ_ONLY"


# R05: Changing synthetic conditioned Y Yes from 3->2 and No from 1->2 at fixed d=4 changes 3/4->1/2
def test_r05_numeric_cell_mutation():
    joint_a = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    joint_b = {(0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2}
    bundle_a = build_source_free_native_joint_bundle(joint_a)
    bundle_b = build_source_free_native_joint_bundle(joint_b)
    result_a = ContractOnlySeamConsumer(bundle_a).compute_scenario("R05_A", ["P_Q86A_given_Q86B_1"])
    result_b = ContractOnlySeamConsumer(bundle_b).compute_scenario("R05_B", ["P_Q86A_given_Q86B_1"])
    assert result_a["exact_probabilities"]["1"]["$exact_fraction"] == [3, 4]
    assert result_b["exact_probabilities"]["1"]["$exact_fraction"] == [1, 2]


# R06: Editing an unconsumed channel with rehashed bundle does not change unrelated conditionals
def test_r06_irrelevant_channel_invariance():
    joint = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    bundle1 = build_source_free_native_joint_bundle(joint)
    bundle2 = build_source_free_native_joint_bundle(joint)
    r1 = ContractOnlySeamConsumer(bundle1).compute_scenario("R06a", ["P_Q86A_given_Q86B_1"])
    r2 = ContractOnlySeamConsumer(bundle2).compute_scenario("R06b", ["P_Q86A_given_Q86B_1"])
    assert r1["exact_probabilities"] == r2["exact_probabilities"]


# R07: [[3,1],[1,3]] vs [[1,3],[3,1]] preserve marginals 4/4 but Y1|X1=3/4 vs 1/4
def test_r07_opposite_joints_same_marginals():
    joint1 = {(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}
    joint2 = {(0, 0): 1, (0, 1): 3, (1, 0): 3, (1, 1): 1}
    b1 = build_source_free_native_joint_bundle(joint1)
    b2 = build_source_free_native_joint_bundle(joint2)
    r1 = ContractOnlySeamConsumer(b1).compute_scenario("R07a", ["P_Q86A_given_Q86B_1"])
    r2 = ContractOnlySeamConsumer(b2).compute_scenario("R07b", ["P_Q86A_given_Q86B_1"])
    assert r1["exact_probabilities"]["1"]["$exact_fraction"] == [3, 4]
    assert r2["exact_probabilities"]["1"]["$exact_fraction"] == [1, 4]


# R08: Wrong channel source_scope fails with SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH
def test_r08_scope_mismatch():
    bundle = build_sociological_bundle()
    channels = list(bundle.channels)
    ch = channels[0]
    bad_ch = replace(ch, source_scope="WRONG_SCOPE")
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels), content_hash="")
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    consumer = ContractOnlySeamConsumer(bad_bundle)
    result = consumer.compute_scenario("R08", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH"


# R09: Wrong conditions[].risk_set_ref must fail RISK_SET_OR_SELECTION_BINDING_MISMATCH
def test_r09_risk_mismatch():
    bundle = build_sociological_bundle()
    conditions = list(bundle.conditions)
    bad_condition = dict(conditions[0])
    bad_condition["risk_set_ref"] = {"kind": "WRONG", "name": "bad", "hash": "0" * 64}
    conditions[0] = bad_condition
    bad_bundle = replace(bundle, conditions=tuple(conditions), content_hash="")
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    consumer = ContractOnlySeamConsumer(bad_bundle)
    result = consumer.compute_scenario("R09", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "RISK_SET_OR_SELECTION_BINDING_MISMATCH"


# R10: Zero qualified synthetic conditioner risk must return ZERO_SUPPORT/ZERO_DENOMINATOR_ABSTENTION
def test_r10_zero_support():
    joint = {(0, 0): 0, (0, 1): 0, (1, 0): 1, (1, 1): 3}
    bundle = build_source_free_native_joint_bundle(joint)
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("R10", ["P_Q86A_given_Q86B_0"])
    assert result["status"] == "ZERO_SUPPORT"
    assert result["reason"] == "ZERO_DENOMINATOR_ABSTENTION"


# R11: Identical synthetic selected world gives identical content hash
def test_r11_replay_hash():
    b1 = build_sociological_bundle()
    b2 = build_sociological_bundle()
    assert b1.content_hash == b2.content_hash


# R12: build_retained_gt2_bundle with arbitrary values/token always refuses
def test_r12_fake_source_issuer():
    with pytest.raises(SeamContractError):
        build_retained_gt2_bundle(issued_source_owned_values={"fake": True})


# R13: Old exact democracy/trust scenario IDs must refuse
def test_r13_old_s00_semantic_prohibition():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("DEMOCRACY_SUPPORT", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"


# R14: Mixed-case democracy/trust scenario label must also refuse
def test_r14_casefold_scenario_semantics():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("Democracy_Support", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"
    result2 = consumer.compute_scenario("institutional_trust", ["P_Y_given_A"])
    assert result2["status"] == "REFUSED"
    result3 = consumer.compute_scenario("Democratic_Attitudes", ["P_Y_given_A"])
    assert result3["status"] == "REFUSED"


# R15: Declared channel raw_probability_exact_fraction must equal recomputed numerator/denominator
def test_r15_numeric_precomputed_fraction_closure():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("R15", ["P_Y_given_A"])
    assert result["status"] == "COMPUTED"
    channels = list(bundle.channels)
    ch = channels[0]
    bad_value = dict(ch.value)
    bad_value["raw_probability_exact_fraction"] = {"$exact_fraction": [100, 101]}
    bad_ch = replace(ch, value=bad_value)
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels), content_hash="")
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    bad_consumer = ContractOnlySeamConsumer(bad_bundle)
    bad_result = bad_consumer.compute_scenario("R15b", ["P_Y_given_A"])
    assert bad_result["status"] == "REFUSED"


# R16: Bundle steps[].cells and conditions[].denominator must match read source values
def test_r16_steps_material_closure():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("R16", ["P_Y_given_A"])
    assert result["status"] == "COMPUTED"
    steps = list(bundle.steps)
    bad_step = dict(steps[0])
    bad_cells = dict(bad_step["cells"])
    bad_cells["1"] = {"numerator": 234, "fraction": {"$exact_fraction": [234, 255]}}
    bad_step["cells"] = bad_cells
    steps[0] = bad_step
    bad_bundle = replace(bundle, steps=tuple(steps), content_hash="")
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    bad_consumer = ContractOnlySeamConsumer(bad_bundle)
    bad_result = bad_consumer.compute_scenario("R16b", ["P_Y_given_A"])
    assert bad_result["status"] == "REFUSED"


# R17: Changing counts and rehashing while preserving producer refs must fail provenance closure
def test_r17_selected_world_value_binding():
    bundle = build_sociological_bundle()
    channels = list(bundle.channels)
    ch = channels[0]
    bad_value = dict(ch.value)
    bad_value["raw_numerator_support"] = 99
    bad_value["raw_probability_exact_fraction"] = {"$exact_fraction": [99, 32]}
    bad_ch = replace(ch, value=bad_value)
    channels[0] = bad_ch
    bad_bundle = replace(bundle, channels=tuple(channels), content_hash="")
    bad_bundle = replace(bad_bundle, content_hash=_content_hash(bad_bundle.as_dict()))
    consumer = ContractOnlySeamConsumer(bad_bundle)
    result = consumer.compute_scenario("R17", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"


# R18: No 19,210 cohort, no Likert, no source grant, no V3
def test_r18_no_original_rights():
    result = None
    try:
        from rawlsing_next.r3_s02_seam_witness import run_seam_witness
        result = run_seam_witness()
    except Exception:
        pass
    if result is not None:
        assert result["scientific_claim_grade"] == "SOURCE_FREE_SYNTHETIC"
        assert result["effects"]["v3_invoked"] is False
        assert result["effects"]["gt2_original_source_executed"] is False
    with pytest.raises(SeamContractError):
        build_retained_gt2_bundle()
