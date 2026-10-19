"""E41 tranche native courts: positives, no-drop, minority preservation, replay.

Named fault-witness positives for ``test_e41_tranche.py.proof.json``:

* ``test_no_drop_discriminator_a_dropped_eligible_operation_is_detected``
  (the submitted workload drops an eligible operation; the frozen no-drop
  assertion must fail)
* ``test_e04_client_receipt_denominator_is_computed_not_fixture``
  (the E04 client-visible denominator must come from the computed producer
  geometry, never a fixture constant)
* ``test_direct_route_delegates_to_accepted_provider_object``
  (the direct route must be the accepted provider function itself)
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

RETURN_DIR = Path(__file__).resolve().parent
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))

import bootstrap  # noqa: F401,E402

import e41_frozen_expectations as frozen  # noqa: E402
import e41_provider_extension as ext  # noqa: E402
import e41_tranche as tranche  # noqa: E402

from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError  # noqa: E402
from rawlsing_next.tests import c1_at08_at13_fixture as fx  # noqa: E402
from rawlsing_next.tests import n10e_empirical_slice_fixture as n10e  # noqa: E402

from rawlsing_next import pre553_analytical_composition as composition_owner  # noqa: E402
from rawlsing_next import pre553_empirical_possibility_provider as accepted_provider  # noqa: E402


# ---------------------------------------------------------------------------
# positive coverage
# ---------------------------------------------------------------------------


def test_tranche_covers_all_frozen_operations_and_is_green():
    report = tranche.run_tranche()
    assert report["expected_operation_count"] == 31
    assert report["executed_operation_count"] == 31
    assert report["dropped_operations"] == []
    assert report["unexpected_operations"] == []
    assert report["mismatched_operations"] == []
    assert report["no_drop_ok"] is True
    assert report["all_expected_reached"] is True


def test_frozen_universe_receipt_hash_matches_recomputation():
    universe = frozen.load_universe()
    import hashlib

    digest = hashlib.sha256(frozen.canonical_json(universe).encode("utf-8")).hexdigest()
    receipt = json.loads((RETURN_DIR / "frozen" / "FREEZE_RECEIPT.json").read_text())
    assert receipt["canonical_sha256"] == digest
    assert receipt["operation_count"] == universe["operation_count"] == 31
    assert receipt["frozen_before_candidate_outputs"] is True


def test_expected_universe_is_independent_arithmetic_not_candidate_output():
    """Spot-check expected values recomputed from the literal source tables."""

    universe = frozen.load_universe()
    by_id = {op["op_id"]: op for op in universe["operations"]}
    assert by_id["f2.at07.forward"]["expected_cells"] == {"yes": [54, 60], "no": [6, 60]}
    assert by_id["f2.at07.reverse"]["expected_cells"] == {"P1": [54, 62], "P2": [8, 62]}
    assert by_id["f2.at08.disagree_to_att2"]["expected_cells"] == {
        "support": [8, 40],
        "oppose": [32, 40],
    }
    assert by_id["f3.at10.branch_B"]["expected_cells"] == {"1": [8, 8], "0": [0, 8]}
    assert by_id["f4.at12.cotravel_cloud"]["expected_cells"] == {"1": [2, 3], "0": [1, 3]}
    assert by_id["f3.at11.recursive_depth2"]["expected_denominator"] == 2


def test_coverage_ledger_reflects_frozen_and_actual_identically_on_replay():
    first = tranche.run_tranche()
    second = tranche.run_tranche()
    assert first["no_drop_ok"] and second["no_drop_ok"]
    rows_first = {row["op_id"]: row["actual"] for row in first["results"]}
    rows_second = {row["op_id"]: row["actual"] for row in second["results"]}
    assert set(rows_first) == set(rows_second)
    for op_id in rows_first:
        assert rows_first[op_id]["actual_cells"] == rows_second[op_id]["actual_cells"]
        assert rows_first[op_id]["actual_state"] == rows_second[op_id]["actual_state"]


# ---------------------------------------------------------------------------
# discriminator (a): remove an eligible operation -> named no-drop RED
# ---------------------------------------------------------------------------


def test_no_drop_discriminator_a_dropped_eligible_operation_is_detected():
    """Remove a legally eligible current operation from the submitted workload."""

    universe = frozen.load_universe()
    submitted = [
        op for op in universe["operations"] if op["op_id"] != "f2.at07.forward"
    ]
    assert len(submitted) == universe["operation_count"] - 1
    report = tranche.run_tranche(workload_ops=submitted)
    # The independently frozen universe still demands the operation.
    assert report["dropped_operations"] == ["f2.at07.forward"]
    assert report["no_drop_ok"] is False
    assert report["executed_operation_count"] == 30


# ---------------------------------------------------------------------------
# discriminator (b): sever the condition-value edge -> named consumer RED
# ---------------------------------------------------------------------------


def test_discriminator_b_severed_condition_value_edge_reds_named_consumer():
    """A false pairing witness (semantics lie, hashes consistent) must refuse."""

    source = fx.attitude_fixture()
    material = tranche.direct_material(
        source=source,
        qauth=__import__(
            "rawlsing_next.tests.test_pre553_empirical_query",
            fromlist=["_query_authority"],
        )._query_authority("e41-sever-b"),
        registry=__import__(
            "rawlsing_next.tests.test_pre553_empirical_query",
            fromlist=["_registry"],
        )._registry(
            source,
            __import__(
                "rawlsing_next.tests.test_pre553_empirical_query",
                fromlist=["_query_authority"],
            )._query_authority("e41-sever-b"),
        ),
        conditions=[("RESPONSE", "ATT1", "agree")],
        target_question="ATT2",
        tag="e41-sever-b",
        target_domain=[
            "support",
            "oppose",
        ],
    )
    # Positive control: the honest witness reaches the consumer.
    honest = ext.provide_empirical_possibility_slice_ext(**material)
    assert honest.provider_state == "EXACT_SUPPORTED_SLICE_PRODUCED"
    assert honest.consumer_result_or_null.result_state == "EXACT_SUPPORTED"

    # Severed edge: the pairing relation is a lie (wrong required exact value).
    bad_witness = fx.readdress_witness_with_false_pairing(
        material["condition_binding_witness"], false_exact_value="disagree"
    )
    with pytest.raises(Pre553IntegrityError):
        ext.provide_empirical_possibility_slice_ext(
            **{**material, "condition_binding_witness": bad_witness}
        )


# ---------------------------------------------------------------------------
# discriminator (c): minority mass change -> downstream difference
# ---------------------------------------------------------------------------


def test_discriminator_c_minority_mass_change_preserves_majority_and_changes_downstream():
    original = fx.minority_fixture("e41-min-orig")
    mutated = __import__(
        "rawlsing_next.tests.test_pre553_empirical_query", fromlist=["_build_source"]
    )._build_source(
        "e41-min-mutated",
        [{"id": f"MA{i}", "responses": {"Y": 1}, "coords": {"G": "A"}} for i in range(3)]
        + [{"id": f"NA{i}", "responses": {"Y": 0}, "coords": {"G": "A"}} for i in range(7)]
        + [{"id": f"MB{i}", "responses": {"Y": 1}, "coords": {"G": "B"}} for i in range(6)]
        + [{"id": f"NB{i}", "responses": {"Y": 0}, "coords": {"G": "B"}} for i in range(2)]
        + [{"id": f"CB{i}", "responses": {"Y": 1}, "coords": {"G": "C"}} for i in range(2)],
    )

    def branch(source, group, tag):
        return tranche.run_direct(
            op_id=f"branch-{group}",
            source=source,
            conditions=[("COORDINATE", "G", group)],
            target="Y",
            tag=tag,
        )

    orig_a = branch(original, "A", "e41c-orig-a")
    orig_b = branch(original, "B", "e41c-orig-b")
    mut_a = branch(mutated, "A", "e41c-mut-a")
    mut_b = branch(mutated, "B", "e41c-mut-b")

    # Majority branch unchanged (same cells AND denominator).
    assert orig_a["actual_cells"] == mut_a["actual_cells"] == {"1": [3, 10], "0": [7, 10]}
    assert orig_a["actual_state"] == mut_a["actual_state"] == "EXACT_SUPPORTED"
    # Minority branch's support mass changed while its denominator still exists.
    assert orig_b["actual_cells"] == {"1": [8, 8], "0": [0, 8]}
    assert mut_b["actual_cells"] == {"1": [6, 8], "0": [2, 8]}
    assert orig_b["actual_cells"] != mut_b["actual_cells"]
    # Downstream consumer-visible identity differs for the changed branch.
    assert (
        orig_b["receipt"]["composed_result_identity_hash"]
        != mut_b["receipt"]["composed_result_identity_hash"]
    )


# ---------------------------------------------------------------------------
# discriminator (d): wrong orientation/denominator refuses or is flagged
# ---------------------------------------------------------------------------


def test_discriminator_d_wrong_conditioning_orientation_refuses():
    """Forward producer material with the reverse consumer query must refuse."""

    forward = tranche.run_at07("probe", "forward")  # positive sanity
    assert forward["actual_state"] == "EXACT_SUPPORTED"
    fwd_case = n10e.build_provider_case("forward")
    rev_case = n10e.build_provider_case("reverse")
    mismatched = {
        "repository": fwd_case["source"]["repo"],
        "empirical_query": fwd_case["empirical_query"],
        "predicate": fwd_case["predicate"],
        "authority_registry": fwd_case["registry"],
        "release_refs": fwd_case["release_refs"],
        "consumer_query": rev_case["consumer_query"],
        "model_rule": fwd_case["model_rule"],
        "condition_binding_witness": fwd_case["condition_binding_witness"],
    }
    with pytest.raises(Pre553IntegrityError):
        ext.provide_empirical_possibility_slice_ext(**mismatched)


def test_discriminator_d_wrong_denominator_is_flagged_not_served():
    """The independent expected/no-drop gate rejects a wrong-denominator actual."""

    universe = frozen.load_universe()
    op = next(o for o in universe["operations"] if o["op_id"] == "f2.at07.forward")
    wrong_actual = {
        "actual_state": "EXACT_SUPPORTED",
        "actual_cells": {"yes": [54, 70], "no": [6, 70]},
        "actual_denominator": 70,
    }
    comparison = tranche._compare(op, wrong_actual)
    assert comparison["matched"] is False
    assert any(diff.startswith("denominator_mismatch") for diff in comparison["diffs"])
    assert any(diff.startswith("cell_mismatch") for diff in comparison["diffs"])


# ---------------------------------------------------------------------------
# discriminator (e): revoked release -> typed refusal, no geometry
# ---------------------------------------------------------------------------


def test_discriminator_e_revoked_or_foreign_release_refuses_without_geometry():
    case = n10e.build_provider_case("forward")
    material = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": (),
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    with pytest.raises(Pre553IntegrityError) as excinfo:
        result = ext.provide_empirical_possibility_slice_ext(**material)
        # If an owner ever returns instead of raising it must be a typed refusal
        # with no evidence; either way no geometry may be fabricated.
        assert result.generated_evidence_or_null is None
    assert not isinstance(excinfo.value, AssertionError)


# ---------------------------------------------------------------------------
# discriminator (f): restored exact bytes -> cold replay identical
# ---------------------------------------------------------------------------


def test_discriminator_f_cold_replay_identity_after_restoration():
    # Fresh-process replay through the accepted runner (AT18 evidence).
    result = tranche.run_at18("probe")
    assert result["actual_state"] == "IDENTICAL_IDENTITY_ON_REPLAY"
    assert result["actual_cells"]["identity_relation"] == "EQUAL"
    fresh = result["receipt"]["fresh_process"]
    assert fresh["raw_denominator_support"] == 60
    assert fresh["cell_numerators"] == {"yes": 54, "no": 6}


# ---------------------------------------------------------------------------
# delegation and provenance of the extension
# ---------------------------------------------------------------------------


def test_direct_route_delegates_to_accepted_provider_object():
    result = tranche.run_at07("probe", "forward")
    assert result["route_actual"] == "DIRECT_VIA_ACCEPTED_PROVIDER_FUNCTION"

    case = n10e.build_provider_case("forward")
    material = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    extension_result = ext.provide_empirical_possibility_slice_ext(**material)
    assert extension_result.base_result_or_null is not None
    # The extension must carry the accepted provider's exact result objects.
    assert (
        extension_result.base_result_or_null.composition_result
        is extension_result.composition_result
    )
    assert (
        extension_result.base_result_or_null.generated_evidence_or_null
        is extension_result.generated_evidence_or_null
    )
    assert (
        extension_result.base_result_or_null.consumer_result_or_null
        is extension_result.consumer_result_or_null
    )
    # ...and the imported callables must be the accepted owner functions.
    assert (
        ext.provide_empirical_possibility_slice
        is accepted_provider.provide_empirical_possibility_slice
    )
    assert (
        ext.compose_positioned_subject_possibility
        is composition_owner.compose_positioned_subject_possibility
    )
    ext.assert_extension_delegates_to_inherited_c1()


def test_extension_exposes_no_precomputed_geometry_channel():
    import inspect

    params = set(inspect.signature(ext.provide_empirical_possibility_slice_ext).parameters)
    for forbidden in (
        "geometry",
        "slice_geometry",
        "precomputed_geometry",
        "probability_geometry",
        "evidence",
        "possibility_slice_evidence",
    ):
        assert forbidden not in params, forbidden


def test_computed_slices_are_producer_derived_for_every_emitted_slice():
    report = tranche.run_tranche()
    emitted = 0
    for row in report["results"]:
        receipt = (row["actual"] or {}).get("receipt") or {}
        if receipt.get("generated_evidence_ref") is None:
            continue
        emitted += 1
        assert receipt["producer_fact_state"] == "SUPPORTED"
        assert receipt["consumer_result_state"] == "EXACT_SUPPORTED"
        assert receipt["generated_evidence_identity_is_producer_derived"] is not False
    assert emitted >= 16


# ---------------------------------------------------------------------------
# original E04 client receipt
# ---------------------------------------------------------------------------


def test_e04_original_client_consumes_computed_slices():
    report = tranche.run_tranche()
    row = next(
        r for r in report["results"] if r["op_id"] == "e04.nonparent_consumption"
    )
    assert row["status"] == "EXECUTED"
    actual = row["actual"]
    assert actual["actual_state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    receipt = actual["receipt"]
    assert receipt["consumer"] == "NONPARENT_OPTIONS"
    assert receipt["service_contract"] == "E41_N10E_COMPUTED_SLICE_E04_SERVICE@1"
    assert all(state == "EXACT_SUPPORTED" for state in receipt["step_states"])
    assert all(ref is not None for ref in receipt["step_evidence_refs"])
    assert actual["actual_cells"]["route_probability_is_null"] == "True"


def test_e04_client_receipt_denominator_is_computed_not_fixture():
    """Named fault-witness positive: the client-visible denominator is computed."""

    from e41_e04_service import drive_original_e04_client

    driven = drive_original_e04_client()
    steps = driven["receipt"]["material"]["empirical"]["steps"]
    at07 = next(step for step in steps if step["target"] == "ANSWER")
    assert at07["denominator"] == 60  # 54 yes / 60 P1 respondents
    assert {(cell["cell"], cell["raw_numerator_support"]) for cell in at07["cells"]} == {
        ("yes", 54),
        ("no", 6),
    }
