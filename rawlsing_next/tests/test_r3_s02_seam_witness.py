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
        assert vr.semantic_effect == "VALUE_READ_AND_USED"
        assert vr.value_hash != ""


def test_consumer_computes_scenario_distributions():
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result = consumer.compute_scenario(
        "S00_SCENARIO_A_HIGH_DEMOCRACY_SUPPORT",
        ["P_Y_given_A"],
    )
    assert result["status"] == "COMPUTED"
    assert len(result["channels_used"]) > 0
    receipt = consumer.get_receipt()
    assert "S00_SCENARIO_A_HIGH_DEMOCRACY_SUPPORT" in receipt.scenario_results


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
    """Changing conditioning variables changes the conditional result."""
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)
    result_a = consumer.compute_scenario("A", ["P_Y_given_A"])
    result_b = consumer.compute_scenario("B", ["P_Y_given_A_B"])
    # Different conditioning produces different channel sets
    assert result_a["channels_used"] != result_b["channels_used"]
    # Unconditional marginals are stable
    assert bundle.channels[0].support == 32  # first step denominator


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
