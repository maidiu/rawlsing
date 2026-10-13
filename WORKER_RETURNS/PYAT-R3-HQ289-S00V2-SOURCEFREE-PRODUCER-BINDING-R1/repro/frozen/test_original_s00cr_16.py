"""PYAT HQ284 S00CR independent source-free value dependency hostiles.

Frozen before reading S00C's test module.  The qualified L01 host may execute
this file in its isolated copy of the exact candidate, recording full commands,
dependency versions, exits and a per-case JSON/JUnit record.  Failures here
are deliberate scientific/security falsifiers, not an automatically adopted
acceptance pass.  No original SAV/DTA, GT2 aggregate or V3 permission.

Commit under S00CR review ownership only; do not modify S00C producer.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import pytest

from rawlsing_next import r3_s02_seam_witness as seam


def _rehash(bundle, **kwargs):
    changed = replace(bundle, content_hash="", **kwargs)
    return replace(changed, content_hash=seam._content_hash(changed.as_dict()))


def _fixture():
    return seam.build_source_free_native_joint_bundle({
        (0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3
    })


def _native_result(bundle, label="s00cr_numerical"):
    return seam.ContractOnlySeamConsumer(bundle).compute_scenario(
        label, ["P_Q86A_given_Q86B_1"])


def _rewrite_channel(bundle, cid, modifications):
    changed = []
    for ch in bundle.channels:
        if ch.channel_id == cid:
            val = dict(ch.value)
            val.update(modifications)
            changed.append(replace(ch, value=val))
        else:
            changed.append(ch)
    return _rehash(bundle, channels=tuple(changed))


def test_s00cr_p04_risk_and_fraction_oracle():
    b = seam.build_sociological_bundle()
    consumer = seam.ContractOnlySeamConsumer(b)
    for step, denom, count, frac in (
        ("P_Y_given_A", 32, 18, [9, 16]),
        ("P_Y_given_A_B", 16, 10, [5, 8]),
        ("P_Y_given_A_B_C", 8, 6, [3, 4]),
    ):
        r = consumer.compute_scenario("s00cr_" + step, [step])
        assert r["status"] == "COMPUTED"
        assert r["raw_denominator_support"] == denom
        assert r["raw_numerators"]["1"] == count
        assert r["exact_probabilities"]["1"] == {"$exact_fraction": frac}
    assert b.world_scope["status"] == "SOURCE_FREE_SYNTHETIC"


def test_s00cr_cumulative_step_risks_not_overlapping_support_sums():
    b = seam.build_sociological_bundle()
    consumer = seam.ContractOnlySeamConsumer(b)
    a = consumer.compute_scenario("trace_A", ["P_Y_given_A", "P_Y_given_A_B"])
    z = consumer.compute_scenario("trace_B", ["P_Y_given_A_B", "P_Y_given_A_B_C"])
    assert (a["total_support"], z["total_support"]) == (16, 8)
    assert [t["raw_denominator_support"] for t in a["progressive_trace"]] == [32, 16]
    assert [t["raw_denominator_support"] for t in z["progressive_trace"]] == [16, 8]


def test_s00cr_read_receipts_precisely_contribute_to_arithmetic():
    c = seam.ContractOnlySeamConsumer(_fixture())
    c.read_value("CH_P_Q86A_given_Q86B_0_0")
    assert c.get_receipt().values_read[0].semantic_effect == "VALUE_READ_ONLY"
    r = c.compute_scenario("s00cr", ["P_Q86A_given_Q86B_1"])
    assert r["exact_probabilities"]["1"] == {"$exact_fraction": [3, 4]}
    receipt = c.get_receipt()
    assert receipt.values_read[0].semantic_effect == "VALUE_READ_ONLY"
    consumed = [v for v in receipt.values_read
                if v.semantic_effect == "VALUE_USED_IN_EXACT_CONDITIONAL"]
    assert len(consumed) == 2
    assert {v.channel_id for v in consumed} == {
        "CH_P_Q86A_given_Q86B_1_0", "CH_P_Q86A_given_Q86B_1_1"}
    assert {x["channel_id"] for x in r["source_value_dependency"]["used_input_refs"]} == {
        x.channel_id for x in consumed}


def test_s00cr_numeric_mutation_changes_conditional_not_just_receipt_hash():
    first = _fixture()
    other = seam.build_source_free_native_joint_bundle({
        (0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2
    })
    a = _native_result(first)
    b = _native_result(other)
    assert a["status"] == b["status"] == "COMPUTED"
    assert a["raw_denominator_support"] == b["raw_denominator_support"] == 4
    assert a["exact_probabilities"]["1"] == {"$exact_fraction": [3, 4]}
    assert b["exact_probabilities"]["1"] == {"$exact_fraction": [1, 2]}
    assert a["source_value_dependency"]["used_input_refs"] != b[
        "source_value_dependency"]["used_input_refs"]


def test_s00cr_same_margins_opposite_joint_change_conditional():
    one = _fixture()
    two = seam.build_source_free_native_joint_bundle({
        (0, 0): 1, (0, 1): 3, (1, 0): 3, (1, 1): 1
    })
    for table in ({(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3},
                  {(0, 0): 1, (0, 1): 3, (1, 0): 3, (1, 1): 1}):
        assert [sum(table[x, y] for y in (0, 1)) for x in (0, 1)] == [4, 4]
        assert [sum(table[x, y] for x in (0, 1)) for y in (0, 1)] == [4, 4]
    assert _native_result(one)["exact_probabilities"]["1"] == {
        "$exact_fraction": [3, 4]}
    assert _native_result(two)["exact_probabilities"]["1"] == {
        "$exact_fraction": [1, 4]}


def test_s00cr_unused_changed_value_no_numeric_effect():
    b = seam.build_sociological_bundle()
    unrelated = b.channels[-1]
    altered = _rewrite_channel(
        b, unrelated.channel_id,
        {"raw_numerator_support": 999, "raw_probability_exact_fraction": None}
    )
    a = seam.ContractOnlySeamConsumer(b).compute_scenario(
        "keep", ["P_Y_given_A"])
    z = seam.ContractOnlySeamConsumer(altered).compute_scenario(
        "keep", ["P_Y_given_A"])
    assert a["status"] == z["status"] == "COMPUTED"
    assert a["exact_probabilities"] == z["exact_probabilities"]
    assert a["raw_denominator_support"] == z["raw_denominator_support"]


def test_s00cr_wrong_channel_scope_typed_refusal():
    b = seam.build_sociological_bundle()
    bad = replace(b.channels[0], source_scope="OTHER_UNISSUED")
    b2 = _rehash(b, channels=(bad,) + b.channels[1:])
    r = seam.ContractOnlySeamConsumer(b2).compute_scenario("x", ["P_Y_given_A"])
    assert (r["status"], r["reason"]) == (
        "REFUSED", "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH")


def test_s00cr_wrong_risk_typed_refusal():
    b = seam.build_sociological_bundle()
    risk = dict(b.conditions[0])
    risk["risk_set_ref"] = {"wrong": "risk"}
    b2 = _rehash(b, conditions=(risk,) + b.conditions[1:])
    r = seam.ContractOnlySeamConsumer(b2).compute_scenario("x", ["P_Y_given_A"])
    assert (r["status"], r["reason"]) == (
        "REFUSED", "RISK_SET_OR_SELECTION_BINDING_MISMATCH")


def test_s00cr_zero_denominator_distinct_from_unknown_selector():
    b = seam.build_source_free_native_joint_bundle({
        (0, 0): 3, (0, 1): 2, (1, 0): 0, (1, 1): 0
    })
    c = seam.ContractOnlySeamConsumer(b)
    r = c.compute_scenario("zero", ["P_Q86A_given_Q86B_1"])
    assert (r["status"], r["reason"]) == (
        "ZERO_SUPPORT", "ZERO_DENOMINATOR_ABSTENTION")
    no = c.compute_scenario("unknown", ["NONEXISTENT"])
    assert (no["status"], no["reason"]) == ("NO_SUPPORT", "NO_MATCHING_CHANNELS")


def test_s00cr_stable_replay_and_self_excluded_receipt_hash():
    a = seam.build_sociological_bundle()
    b = seam.build_sociological_bundle()
    assert a.content_hash == b.content_hash
    c = seam.ContractOnlySeamConsumer(a)
    assert c.compute_scenario("x", ["P_Y_given_A"])["status"] == "COMPUTED"
    first = c.get_receipt().output_hash
    second = c.get_receipt().output_hash
    assert first == second
    assert seam.run_seam_witness()["replay_verified"] is True


def test_s00cr_unissued_source_value_must_refuse():
    with pytest.raises(seam.SeamContractError, match="SOURCE_VALUE_UNAVAILABLE"):
        seam.build_retained_gt2_bundle(
            issued_source_owned_values={"value": 19210, "Q86A": 1},
            issued_use_authority="caller-asserted-token")


def test_s00cr_uppercase_historical_s00_semantics_refused():
    b = seam.build_sociological_bundle()
    r = seam.ContractOnlySeamConsumer(b).compute_scenario(
        "S00_SCENARIO_A_HIGH_DEMOCRACY_SUPPORT", ["P_Y_given_A"])
    assert r["status"] == "REFUSED"
    assert r["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"


# Expected security/science FAILURES on the frozen S00C implementation:
# These should not be xfailed: a failed hostile records an actionable defect.

def test_s00cr_mixed_case_false_construct_label_is_also_refused():
    b = seam.build_sociological_bundle()
    r = seam.ContractOnlySeamConsumer(b).compute_scenario(
        "s00_high_democracy_support", ["P_Y_given_A"])
    assert r["status"] == "REFUSED"
    assert r["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"


def test_s00cr_source_fraction_claim_must_match_numeric_count():
    b = _fixture()
    bad = _rewrite_channel(
        b, "CH_P_Q86A_given_Q86B_1_1",
        {"raw_probability_exact_fraction": {"$exact_fraction": [100, 101]}}
    )
    r = _native_result(bad)
    assert r["status"] == "REFUSED"
    assert r["reason"] == "SOURCE_COUNT_CLOSURE_MISMATCH"


def test_s00cr_step_geometry_cannot_disagree_with_read_values():
    b = _fixture()
    changed_steps = list(b.steps)
    first = dict(changed_steps[1])
    original_cells = dict(first["cells"])
    original_cells["1"] = {"numerator": 234}
    first["cells"] = original_cells
    changed_steps[1] = first
    edited = _rehash(b, steps=tuple(changed_steps))
    r = _native_result(edited)
    assert r["status"] == "REFUSED"
    assert r["reason"] == "SOURCE_COUNT_CLOSURE_MISMATCH"


def test_s00cr_numeric_mutation_with_stale_producer_ref_must_refuse():
    b = _fixture()
    # Rehash bundle, but DO NOT change selected-world risk/release/row law.
    after = _rewrite_channel(
        b, "CH_P_Q86A_given_Q86B_1_1", {"raw_numerator_support": 2}
    )
    after = _rewrite_channel(
        after, "CH_P_Q86A_given_Q86B_1_0", {"raw_numerator_support": 2}
    )
    r = _native_result(after)
    assert r["status"] == "REFUSED"
    assert r["reason"] in {
        "SOURCE_COUNT_CLOSURE_MISMATCH", "SELECTED_WORLD_BINDING_MISMATCH",
        "PRODUCER_VALUE_IDENTITY_MISMATCH"}


