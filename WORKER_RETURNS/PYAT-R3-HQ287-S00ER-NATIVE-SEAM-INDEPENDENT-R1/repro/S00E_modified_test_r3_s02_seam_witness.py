"""PYAT R3 S00-S02 — seam witness tests.

Development-only.  These tests verify the sociological bundle, consumer
receipts, deterministic replay, and failure cases.

No V3 actor, developmental psychology, parents, biography or V2 rendering.
"""

from __future__ import annotations

import pytest

import rawlsing_next.r3_s02_seam_witness as seam
from rawlsing_next.r3_s02_seam_witness import (
    build_sociological_bundle,
    run_seam_witness,
    ContractOnlySeamConsumer,
    SeamContractError,
)


# ==========================================================================
# S00: contract manifest
# ==========================================================================
def test_s00_contract_manifest_exists_and_is_valid():
    import json
    import pathlib
    manifest = json.loads(
        pathlib.Path("WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/"
                     "s00_target_contract.json").read_text()
    )
    assert manifest["contract_version"] == "R3_S00_SOCIOLOGICAL_TARGET@1.0.0"
    assert manifest["status"] == "FROZEN_FOR_S03_S04_COORDINATION"
    assert len(manifest["scenarios"]) == 2
    assert len(manifest["required_channels"]) == 3
    assert manifest["evidence_boundary"]["strongest_output_status"] == "RETAINED_SOURCE_CONDITIONED"


# ==========================================================================
# S01: bundle construction
# ==========================================================================
def test_bundle_builds_with_channels_and_evidence():
    bundle = build_sociological_bundle()
    assert bundle.bundle_id is not None
    assert bundle.content_hash != ""
    assert len(bundle.channels) > 0
    assert len(bundle.evidence_graph) > 0
    assert len(bundle.steps) == 3
    assert bundle.selected_world_contract.real_current is False


def test_bundle_channels_have_provenance():
    bundle = build_sociological_bundle()
    for ch in bundle.channels:
        assert ch.evidence_mode in ("MEASURED", "TRANSFORMED", "INFERRED", "PRIOR")
        assert ch.test_origin is True  # P04 fixture is synthetic
        assert ch.support > 0


def test_bundle_preserves_progressive_geometry():
    bundle = build_sociological_bundle()
    step_ids = [s["step_id"] for s in bundle.steps]
    assert step_ids == ["P_Y_given_A", "P_Y_given_A_B", "P_Y_given_A_B_C"]
    # denominators 32, 16, 8
    denominators = [bundle.conditions[i]["denominator"] for i in range(3)]
    assert denominators == [32, 16, 8]


# ==========================================================================
# S02: consumer receipts and semantic effects
# ==========================================================================
def test_consumer_reads_values_and_records_receipts():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    for ch in bundle.channels[:3]:
        consumer.read_value(ch.channel_id)
    receipt = consumer.get_receipt()
    assert len(receipt.values_read) == 3
    for vr in receipt.values_read:
        assert vr.semantic_effect == "VALUE_READ_ONLY"  # a lookup is not yet use
        assert vr.value_hash != ""


def test_consumer_computes_scenario_distributions():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario(
        "P04_SYNTHETIC_PROBABILITY_A",
        ["P_Y_given_A"],
    )
    assert result["status"] == "COMPUTED"
    assert len(result["channels_used"]) > 0
    receipt = consumer.get_receipt()
    assert "P04_SYNTHETIC_PROBABILITY_A" in receipt.scenario_results


def test_consumer_refuses_unsupported_condition():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("S00_SCENARIO_X", ["NONEXISTENT"])
    assert result["status"] == "NO_SUPPORT"
    receipt = consumer.get_receipt()
    assert len(receipt.refused_fields) == 1
    assert receipt.refused_fields[0]["reason"] == "NO_MATCHING_CHANNELS"


def test_consumer_refuses_unknown_channel():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.read_value("NONEXISTENT_CHANNEL")
    assert result is None
    receipt = consumer.get_receipt()
    assert receipt.refused_fields[0]["reason"] == "CHANNEL_NOT_FOUND"


# ==========================================================================
# S02: deterministic replay
# ==========================================================================
def test_bundle_replay_is_deterministic():
    bundle1 = build_sociological_bundle()
    bundle2 = build_sociological_bundle()
    assert bundle1.content_hash == bundle2.content_hash


def test_full_witness_replay_is_deterministic():
    result1 = run_seam_witness()
    result2 = run_seam_witness()
    assert result1["bundle"]["content_hash"] == result2["bundle"]["content_hash"]
    assert result1["consumer_receipt"]["output_hash"] == result2["consumer_receipt"]["output_hash"]


# ==========================================================================
# S02: semantic differences (not merely changed hashes)
# ==========================================================================
def test_same_marginals_different_joints_produce_different_conditionals():
    """Same X/Y marginals but opposite X-Y joints change P(Y|X)."""
    from rawlsing_next.r3_s02_seam_witness import build_source_free_native_joint_bundle
    one = build_source_free_native_joint_bundle({
        (0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3,
    })
    two = build_source_free_native_joint_bundle({
        (0, 0): 1, (0, 1): 3, (1, 0): 3, (1, 1): 1,
    })
    for x in (0, 1):
        assert sum(v for (r, y), v in {
            (0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3}.items() if r == x) == 4
    result_a = ContractOnlySeamConsumer(one).compute_scenario(
        "NATIVE_SYNTH_A", ["P_Q86A_given_Q86B_1"])
    result_b = ContractOnlySeamConsumer(two).compute_scenario(
        "NATIVE_SYNTH_B", ["P_Q86A_given_Q86B_1"])
    assert result_a["exact_probabilities"]["1"] == {"$exact_fraction": [3, 4]}
    assert result_b["exact_probabilities"]["1"] == {"$exact_fraction": [1, 4]}
    assert result_a["raw_denominator_support"] == result_b["raw_denominator_support"] == 4


def test_cumulative_conditioning_narrows_denominator():
    """Adding conditions narrows the risk set."""
    bundle = build_sociological_bundle()
    denominators = [bundle.conditions[i]["denominator"] for i in range(3)]
    assert denominators[0] > denominators[1] > denominators[2]
    # Minority cells survive at every depth
    for step in bundle.steps:
        assert set(step["cells"].keys()) == {"0", "1"}
        for cell in step["cells"].values():
            assert cell["numerator"] >= 1


def test_irrelevant_inputs_do_not_change_result():
    """Irrelevant channels do not affect scenario computation."""
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("A", ["P_Y_given_A"])
    # Reading an unrelated channel does not change the result
    consumer.read_value(bundle.channels[-1].channel_id)
    result2 = consumer.compute_scenario("A", ["P_Y_given_A"])
    assert result == result2


# ==========================================================================
# S02: failure cases
# ==========================================================================
def test_zero_support_produces_typed_refusal():
    """A scenario with no matching channels produces a typed refusal."""
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario("ZERO", ["IMPOSSIBLE_CONDITION"])
    assert result["status"] == "NO_SUPPORT"


def test_scope_mismatch_produces_refusal():
    """A channel outside the bundle scope is refused."""
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.read_value("CH_OUTSIDE_SCOPE")
    assert result is None


# ==========================================================================
# Governance: no V3, no actor, no biography
# ==========================================================================
def test_effects_declare_no_v3_no_actor():
    result = run_seam_witness()
    assert result["effects"]["v3_invoked"] is False
    assert result["effects"]["v2_invoked"] is False
    assert result["effects"]["actor_created"] is False
    assert result["effects"]["biography_generated"] is False
    assert result["effects"]["parent_created"] is False
    assert result["effects"]["real_current_claim"] is False


def test_module_import_surface_contains_no_forbidden_owner():
    import inspect
    source = inspect.getsource(seam)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in ("v3_adp", "m5_runtime", "m6_actor", "field_forge",
                  "childhood", "biography", "parent", "coparent"):
        assert token not in imports


def test_no_raw_sav_dta():
    import pathlib
    source = pathlib.Path(seam.__file__).read_text()
    for forbidden in (".sav", ".dta", "pyreadstat"):
        assert forbidden not in source


# ==========================================================================
# S00C independent frozen S00R repair hostiles (SOURCE FREE ONLY)
# ==========================================================================
def test_s00c_synthetic_bundle_never_claims_real_r5_or_measured_source():
    bundle = build_sociological_bundle()
    assert bundle.world_scope["status"] == "SOURCE_FREE_SYNTHETIC"
    assert bundle.world_scope["qualified_real_source_value_read"] is False
    assert "Afrobarometer" not in str(bundle.world_scope)
    assert bundle.replay["source_permission"] == "SOURCE_FREE_ONLY"
    assert all(c.test_origin and c.evidence_mode == "TRANSFORMED"
               for c in bundle.channels)
    assert run_seam_witness()["real_gt2_value_use"].startswith("SOURCE_VALUE_UNAVAILABLE")


def test_s00c_false_frozen_s00_democracy_semantics_refused():
    bundle = build_sociological_bundle()
    result = ContractOnlySeamConsumer(bundle).compute_scenario(
        "S00_SCENARIO_A_HIGH_DEMOCRACY_SUPPORT", ["P_Y_given_A"])
    assert result["status"] == "REFUSED"
    assert result["reason"] == "FALSE_S00_Q86_SOURCE_MEANING"


def test_s00c_exact_32_16_8_denominators_not_112_or_48():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    expected = (
        ("P_Y_given_A", 32, [9, 16]),
        ("P_Y_given_A_B", 16, [5, 8]),
        ("P_Y_given_A_B_C", 8, [3, 4]),
    )
    for step, denom, fraction in expected:
        result = consumer.compute_scenario("EXACT_" + step, [step])
        assert result["status"] == "COMPUTED"
        assert result["raw_denominator_support"] == denom
        assert result["exact_probabilities"]["1"] == {"$exact_fraction": fraction}
        assert result["raw_numerators"]["1"] > 0
    a = consumer.compute_scenario("A_TRACE", ["P_Y_given_A", "P_Y_given_A_B"])
    b = consumer.compute_scenario("B_TRACE", ["P_Y_given_A_B", "P_Y_given_A_B_C"])
    assert (a["total_support"], b["total_support"]) == (16, 8)
    assert [x["raw_denominator_support"] for x in a["progressive_trace"]] == [32, 16]
    assert [x["raw_denominator_support"] for x in b["progressive_trace"]] == [16, 8]


def test_s00c_unused_read_is_not_misrepresented_as_use():
    bundle = build_sociological_bundle()
    c = ContractOnlySeamConsumer(bundle)
    c.read_value(bundle.channels[0].channel_id)
    assert c.get_receipt().values_read[0].semantic_effect == "VALUE_READ_ONLY"
    c.compute_scenario("EXACT_P04_USE", ["P_Y_given_A"])
    receipt = c.get_receipt()
    assert receipt.values_read[0].semantic_effect == "VALUE_READ_ONLY"
    used = [x for x in receipt.values_read if x.semantic_effect == "VALUE_USED_IN_EXACT_CONDITIONAL"]
    assert len(used) == 2
    assert set(x.channel_id for x in used) == {
        "CH_P_Y_given_A_0", "CH_P_Y_given_A_1"}
    first_hash = receipt.output_hash
    assert c.get_receipt().output_hash == first_hash


def test_s00c_change_source_owned_synthetic_numeric_values_changes_result():
    from dataclasses import replace
    from rawlsing_next.r3_s02_seam_witness import (
        build_source_free_native_joint_bundle, _content_hash)
    original = build_source_free_native_joint_bundle({
        (0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3,
    })
    before = ContractOnlySeamConsumer(original).compute_scenario(
        "T", ["P_Q86A_given_Q86B_1"])
    edited = []
    for c in original.channels:
        if c.channel_id in ("CH_P_Q86A_given_Q86B_1_0", "CH_P_Q86A_given_Q86B_1_1"):
            value = dict(c.value)
            value["raw_numerator_support"] = 2
            value["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 2]}
            edited.append(replace(c, value=value))
        else:
            edited.append(c)
    edited_steps = []
    for s in original.steps:
        if s["step_id"] == "P_Q86A_given_Q86B_1":
            new_cells = {}
            for k, v in s["cells"].items():
                new_cells[k] = {"numerator": 2, "fraction": {"$exact_fraction": [1, 2]}}
            edited_steps.append({**s, "cells": new_cells})
        else:
            edited_steps.append(s)
    temporary = replace(original, channels=tuple(edited), steps=tuple(edited_steps), content_hash="")
    changed = replace(temporary, content_hash=_content_hash(temporary.as_dict()))
    after = ContractOnlySeamConsumer(changed).compute_scenario(
        "T", ["P_Q86A_given_Q86B_1"])
    assert before["exact_probabilities"]["1"] == {"$exact_fraction": [3, 4]}
    assert after["exact_probabilities"]["1"] == {"$exact_fraction": [1, 2]}
    assert before["raw_denominator_support"] == after["raw_denominator_support"] == 4
    assert before["source_value_dependency"]["used_input_refs"] != after[
        "source_value_dependency"]["used_input_refs"]
    stale = []
    for c in original.channels:
        if c.channel_id in ("CH_P_Q86A_given_Q86B_1_0", "CH_P_Q86A_given_Q86B_1_1"):
            value = dict(c.value)
            value["raw_numerator_support"] = 2
            stale.append(replace(c, value=value))
        else:
            stale.append(c)
    stale_tmp = replace(original, channels=tuple(stale), content_hash="")
    stale_bundle = replace(stale_tmp, content_hash=_content_hash(stale_tmp.as_dict()))
    stale_result = ContractOnlySeamConsumer(stale_bundle).compute_scenario(
        "T", ["P_Q86A_given_Q86B_1"])
    assert stale_result["status"] == "REFUSED"


def test_s00c_irrelevant_context_changes_stable_numeric_output():
    from dataclasses import replace
    from rawlsing_next.r3_s02_seam_witness import _content_hash
    original = build_sociological_bundle()
    scope = dict(original.world_scope)
    scope["unrelated_test_note"] = "This is not a measured value"
    temporary = replace(original, world_scope=scope, content_hash="")
    changed = replace(temporary, content_hash=_content_hash(temporary.as_dict()))
    a = ContractOnlySeamConsumer(original).compute_scenario("T", ["P_Y_given_A_B"])
    b = ContractOnlySeamConsumer(changed).compute_scenario("T", ["P_Y_given_A_B"])
    assert a == b


def test_s00c_scope_and_risk_mismatch_both_typed_refusals():
    from dataclasses import replace
    from rawlsing_next.r3_s02_seam_witness import _content_hash
    original = build_sociological_bundle()
    bad = replace(original.channels[0], source_scope="FOREIGN_UNISSUED_SURVEY")
    temporary = replace(original, channels=(bad,) + original.channels[1:],
                        content_hash="")
    wrong_scope = replace(temporary, content_hash=_content_hash(temporary.as_dict()))
    r = ContractOnlySeamConsumer(wrong_scope).compute_scenario("T", ["P_Y_given_A"])
    assert (r["status"], r["reason"]) == (
        "REFUSED", "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH")
    cond = dict(original.conditions[0])
    cond["risk_set_ref"] = {"forged_risk": True}
    temporary = replace(original, conditions=(cond,) + original.conditions[1:],
                        content_hash="")
    wrong_risk = replace(temporary, content_hash=_content_hash(temporary.as_dict()))
    r = ContractOnlySeamConsumer(wrong_risk).compute_scenario("T", ["P_Y_given_A"])
    assert (r["status"], r["reason"]) == (
        "REFUSED", "RISK_SET_OR_SELECTION_BINDING_MISMATCH")


def test_s00c_zero_denominator_distinct_from_missing_channel():
    from rawlsing_next.r3_s02_seam_witness import build_source_free_native_joint_bundle
    zero = build_source_free_native_joint_bundle({
        (0, 0): 2, (0, 1): 3, (1, 0): 0, (1, 1): 0,
    })
    r = ContractOnlySeamConsumer(zero).compute_scenario(
        "SYNTH_ZERO", ["P_Q86A_given_Q86B_1"])
    assert r["status"] == "ZERO_SUPPORT"
    assert r["reason"] == "ZERO_DENOMINATOR_ABSTENTION"


def test_s00c_unissued_real_gt2_never_accepts_arbitrary_dict_as_source():
    from rawlsing_next.r3_s02_seam_witness import build_retained_gt2_bundle
    with pytest.raises(SeamContractError, match="SOURCE_VALUE_UNAVAILABLE"):
        build_retained_gt2_bundle(
            issued_source_owned_values={"Q86B": 1, "Q86A": 1, "count": 19210},
            issued_use_authority="FAKE_SIGNATURE")
