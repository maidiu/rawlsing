"""HQ297 independent SC0 x PE interface court (UNEXECUTED at authoring).

Executed ONLY by a qualified isolated Python host with an exact PE tree and the
reviewer overlay. Does not import SC0 into PE as a fictitious production owner.
Tests marked 'strict' intentionally require SC0 value-bearing semantics which
PE does not currently provide; preserve failures, DO NOT xfail.

SC0 independent oracle roots:
  K9 9ccb66f9b08a4aa8b96582295bb2966d250fd72d
  K10 e78b3ee91da1fb18deaf8d8f226800ad855adbae
Exact candidate module blob 58484f4c3d9aae148d4116dcf00420c432aefcbd.
"""
from __future__ import annotations
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import hashlib
import os

import pytest

from rawlsing_next.tests.test_postastra_pe_fixture import (
    law_a_cases, law_b_cases, make_n9_world_dependency,
)
from rawlsing_next.pre553_postastra_pe_generic_world_possibility import (
    N9WorldDependency, serve_generic_world_situated_possibility,
)


PE_MODULE_GIT_BLOB = "58484f4c3d9aae148d4116dcf00420c432aefcbd"


def _git_blob(path: Path):
    buf = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(buf)).encode() + b"\0" + buf).hexdigest()


@pytest.fixture(scope="session", autouse=True)
def qualify_exact_candidate():
    root = os.environ.get("HQ297_EXACT_PE_ROOT")
    if not root:
        pytest.fail(
            "EXECUTION_TERRAIN_HOLD: exact PE worktree env HQ297_EXACT_PE_ROOT missing"
        )
    target = Path(root).resolve() / "rawlsing_next/pre553_postastra_pe_generic_world_possibility.py"
    if not target.is_file():
        pytest.fail("EXECUTION_TERRAIN_HOLD: PE module absent")
    if _git_blob(target) != PE_MODULE_GIT_BLOB:
        pytest.fail("EXECUTION_TERRAIN_HOLD: PE candidate module blob mismatch")
    import rawlsing_next.pre553_postastra_pe_generic_world_possibility as pe
    if _git_blob(Path(pe.__file__).resolve()) != PE_MODULE_GIT_BLOB:
        pytest.fail("EXECUTION_TERRAIN_HOLD: imported PE module is not pinned candidate")


@pytest.fixture(scope="module")
def worlds():
    return {"A": law_a_cases(), "B": law_b_cases()}


def _serve(case, *, request=None):
    return serve_generic_world_situated_possibility(
        repository=case["repository"], empirical_query=case["empirical_query"],
        predicate=case["predicate"], authority_registry=case["registry"],
        release_refs=case["release_refs"],
        request=case["request"] if request is None else request,
        model_rule=case["model_rule"], condition_binding_witness=case["witness"],
    )


def _cell_fraction(receipt, cell):
    for entry in receipt.consumer_exact_geometry["cells"]:
        if entry["cell"] == cell:
            return Fraction(*entry["raw_probability_exact_fraction"]["$exact_fraction"])
    raise AssertionError("TARGET_CELL_MISSING")


def test_independent_pe_multi_condition_n100_n110_and_null_control(worlds):
    """Independently specified row-mass arithmetic; NOT an SC0 world port PASS."""
    a = worlds["A"]
    b = worlds["B"]
    for scope, numerator, denominator in ((a, 27, 30), (b, 37, 40)):
        p = _serve(scope["multi_binding_parent_context"])
        assert p.result_state == "EXACT_SUPPORTED"
        assert _cell_fraction(p.receipt, "yes") == Fraction(numerator, denominator)
        assert p.receipt.consumer_exact_geometry["denominator"]["raw_denominator_support"] == denominator
        assert p.receipt.n9_world.n9_snapshot_state == "SELECTED_IMMUTABLE"
    x = _serve(a["conception_scenario"]).receipt
    y = _serve(b["conception_scenario"]).receipt
    assert _cell_fraction(x, "yes") == _cell_fraction(y, "yes") == Fraction(7, 10)
    assert x.consumer_exact_geometry["denominator"]["raw_denominator_support"] == 30


def test_independent_nonparent_reverse_has_its_own_denominator(worlds):
    """No illicit P(P1|yes)=P(yes|P1) substitution."""
    a = _serve(worlds["A"]["nonparent_reverse"])
    b = _serve(worlds["B"]["nonparent_reverse"])
    assert a.result_state == b.result_state == "EXACT_SUPPORTED"
    assert _cell_fraction(a.receipt, "P1") == Fraction(48, 64)
    assert _cell_fraction(b.receipt, "P1") == Fraction(58, 74)
    assert a.receipt.consumer_exact_geometry["denominator"]["raw_denominator_support"] == 64
    assert b.receipt.consumer_exact_geometry["denominator"]["raw_denominator_support"] == 74
    assert a.receipt.role_direction == "REVERSE_TARGET_VALUE_TO_SUBJECT"


def test_world_ref_change_is_only_carry_not_joint_computation(worlds):
    """A distinct opaque world ref changes receipt identity, NOT empirical law."""
    case = worlds["A"]["multi_binding_parent_context"]
    first = _serve(case)
    changed_world = make_n9_world_dependency(tag="separately-proposed-other-world")
    req = replace(case["request"], n9_world=changed_world)
    second = _serve(case, request=req)
    assert first.result_state == second.result_state == "EXACT_SUPPORTED"
    assert first.receipt.receipt_hash != second.receipt.receipt_hash
    assert first.receipt.consumer_exact_geometry == second.receipt.consumer_exact_geometry
    assert first.receipt.world_carriage_is_not_route_probability
    # This confirms an N10E-only null effect, NOT that an N9 route was resolved.


def test_invalidated_snapshot_refuses_without_reusing_cached_geometry(worlds):
    case = worlds["A"]["multi_binding_parent_context"]
    req = replace(case["request"], n9_world=replace(
        case["request"].n9_world, n9_snapshot_state="INVALIDATED"
    ))
    result = _serve(case, request=req)
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == "INVALIDATED_CURRENT_REFUSED"
    assert result.receipt.consumer_exact_geometry is None


def test_strict_reverse_scoped_issuer_forgery_must_refuse(worlds):
    """Expected SC0 rejection: merely non-null *caller* authority is not science."""
    case = worlds["A"]["nonparent_reverse"]
    old = case["request"].role_reversal_authority_ref
    false = type(old)(authority_id="urn:test:unissued:reversal:WRONG_TOPOLOGY",
        authority_version="999.0.0",
        authority_content_hash="f" * 64)
    req = replace(case["request"], role_reversal_authority_ref=false)
    result = _serve(case, request=req)
    assert result.result_state == "TYPED_REFUSAL", (
        "STATIC_EXPECTED_FAILURE__PE_ACCEPTS_ANY_NON_NULL_REVERSAL_AUTHORITY"
    )
    assert result.receipt.consumer_exact_geometry is None


def test_strict_selected_world_nary_F2_AH_strata_roundtrip(worlds):
    """SC0 two-owner world contract, NOT a claim generic PE already implements it."""
    receipt = _serve(worlds["A"]["multi_binding_parent_context"]).receipt
    world = receipt.material()["n9_world"]
    for name in (
        "absolute_horizon", "native_strata", "nary", "f2",
        "public_sanctions", "public_categories", "contradictory_alternatives",
    ):
        assert name in world, "SC0_REQUIRED_N9_VALUE_ABSENT:" + name


def test_strict_generated_runtime_fact_echo_not_source_promotion(worlds):
    receipt = _serve(worlds["A"]["multi_binding_parent_context"]).receipt
    world = receipt.material()["n9_world"]
    assert world["binding_echo"]["tag"] == "GENERATED_RUNTIME_FACT_REF"
    assert world["binding_echo"]["may_use_as_source_observation"] is False


def test_strict_two_distinct_world_refresh_receipts(worlds):
    receipt = _serve(worlds["A"]["multi_binding_parent_context"]).receipt
    mat = receipt.material()
    assert mat["structural_publication_refresh_receipt"]["world_result_ref"]
    assert mat["generated_binding_refresh_receipt"]["world_result_ref"]
    assert mat["structural_publication_refresh_receipt"] != mat[
        "generated_binding_refresh_receipt"]


def test_strict_four_clocks_historical_knowledge(worlds):
    receipt = _serve(worlds["A"]["multi_binding_parent_context"]).receipt
    c = receipt.material()["n9_world"]["clocks"]
    assert set(c) == {
        "observation_effective", "publication_knowledge",
        "actor_event", "request_currentness"}


def test_strict_negative_status_algebra_and_source_risk(worlds):
    mat = _serve(worlds["A"]["conception_scenario"]).receipt.material()
    world = mat["n9_world"]
    statuses = {s["state"] for s in world["scoped_status_rows"]}
    assert {"OBSERVED_ZERO", "VALID_EMPTY", "MISSING", "UNDERPOWERED",
            "NOT_ASKED", "NONCOMPARABLE", "HELD_AUTHORITY", "DENIED_USE"} <= statuses
    assert world["native_sampling_unit"] == "RESPONDENT"
    assert world["native_risk_set_ref"]
    assert world["original_routing_ref"]


def test_strict_values_read_not_only_hash_or_inferred_label(worlds):
    mat = _serve(worlds["A"]["nonparent_reverse"]).receipt.material()
    assert mat["n9_values_read_receipt"]["exact_owner_value_refs"]
    assert mat["n10e_values_read_receipt"]["exact_numerator_and_denominator"]
    assert mat["consumer_effect"]["NONPARENT_APPRENTICESHIP_ENTRY"]


def test_strict_nonparent_apprenticeship_world_effect(worlds):
    mat = _serve(worlds["A"]["nonparent_reverse"]).receipt.material()
    effects = mat["generic_consumers"]["NONPARENT_APPRENTICESHIP_ENTRY"]
    assert effects["route_constraints"]
    assert effects["no_generated_person"] is True


def test_strict_parent_scenario_remains_input_only(worlds):
    mat = _serve(worlds["A"]["conception_scenario"]).receipt.material()
    effects = mat["generic_consumers"]["CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"]
    assert effects["proposed_constraints"]
    assert effects["no_parent_actor_created"] is True
