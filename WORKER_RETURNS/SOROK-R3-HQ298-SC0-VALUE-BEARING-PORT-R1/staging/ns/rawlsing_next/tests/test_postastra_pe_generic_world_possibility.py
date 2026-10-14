"""POST-ASTRA R3 PE — executed generic world-situated possibility test court.

Real Python tests over the candidate generic seam.  Two independent synthetic
source laws (N100 / N110), three consumers through the SAME abstract service,
and the eight required negative falsifiers.  All source-free: synthetic fixture
rows only; no raw survey, no real-source C11, no V3, no actor, no model calls.

Every expected value is exact arithmetic frozen in
``test_postastra_pe_fixture`` BEFORE any service output is used as expected
truth.  These tests execute the accepted C1 composition seam through the new
versioned boundary; they are not a science claim and not an N9 current claim.
"""
from __future__ import annotations

import copy

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_analytical_composition import ConditionValueBindingWitness
from rawlsing_next.pre553_postastra_pe_generic_world_possibility import (
    EPISTEMIC_CEILING,
    GenericWorldRequestLawError,
    LANE_N10E,
    LANE_WORLD_ONLY,
    N9_INVALIDATED,
    REFUSAL_ARTIFICIAL_PARENT_SAMPLING,
    REFUSAL_FAKE_MODEL_USE,
    REFUSAL_FUTURE_TIME,
    REFUSAL_INVALIDATED_CURRENT,
    REFUSAL_MISSING_DENOMINATOR,
    REFUSAL_NEW_UNIT,
    REFUSAL_REVERSED_UNAUTHORIZED_ROLE,
    ROLE_REVERSE,
    GenericWorldSituatedRequest,
    serve_generic_world_situated_possibility,
    verify_generic_world_situated_replay,
)

from rawlsing_next.tests.test_postastra_pe_fixture import (
    LAW_A_ID,
    LAW_A_ORACLE,
    LAW_B_ID,
    LAW_B_ORACLE,
    build_three_consumer_cases,
    law_a_cases,
    law_a_rows,
    law_b_cases,
    make_n9_world_dependency,
    make_role_reversal_authority,
    make_unit_refs,
)

CONSUMERS = ("multi_binding_parent_context", "nonparent_reverse", "conception_scenario")


def _serve(c):
    return serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=c["request"],
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )


def _yes_fraction(geometry):
    if not geometry:
        return None
    for cell in geometry.get("cells", ()):
        if cell.get("cell") == "yes":
            return cell.get("raw_probability_exact_fraction")
    return None


def _cell_fraction(geometry, cell_name):
    if not geometry:
        return None
    for cell in geometry.get("cells", ()):
        if cell.get("cell") == cell_name:
            return cell.get("raw_probability_exact_fraction")
    return None


@pytest.fixture(scope="module")
def law_a():
    return law_a_cases()


@pytest.fixture(scope="module")
def law_b():
    return law_b_cases()


# ---------------------------------------------------------------------------
# Two independent law fixtures x three consumers through the SAME service
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_law_a_consumer_computes_exact_fraction_at_declared_grain(law_a, consumer):
    c = law_a[consumer]
    result = _serve(c)
    receipt = result.receipt
    assert result.result_state == "EXACT_SUPPORTED"
    assert receipt.inference_lane == LANE_N10E
    assert receipt.refusal_state is None
    geometry = receipt.consumer_exact_geometry
    assert geometry is not None
    expected_key = c["expected"]
    oracle = LAW_A_ORACLE[expected_key]
    assert geometry["denominator"]["raw_denominator_support"] == oracle["denominator"]
    if expected_key == "reverse_single":
        assert _cell_fraction(geometry, "P1") == oracle["expected_fraction_P1"]
    else:
        assert _yes_fraction(geometry) == oracle["expected_fraction_yes"]


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_law_b_consumer_computes_exact_fraction_at_declared_grain(law_b, consumer):
    c = law_b[consumer]
    result = _serve(c)
    receipt = result.receipt
    assert result.result_state == "EXACT_SUPPORTED"
    assert receipt.inference_lane == LANE_N10E
    geometry = receipt.consumer_exact_geometry
    expected_key = c["expected"]
    oracle = LAW_B_ORACLE[expected_key]
    assert geometry["denominator"]["raw_denominator_support"] == oracle["denominator"]
    if expected_key == "reverse_single":
        assert _cell_fraction(geometry, "P1") == oracle["expected_fraction_P1"]
    else:
        assert _yes_fraction(geometry) == oracle["expected_fraction_yes"]


def test_two_independent_laws_are_empirically_discriminating(law_a, law_b):
    """A changed source law moves the multi-binding slice but not the cohort-B slice."""
    a_multi = _serve(law_a["multi_binding_parent_context"]).receipt.consumer_exact_geometry
    b_multi = _serve(law_b["multi_binding_parent_context"]).receipt.consumer_exact_geometry
    a_conc = _serve(law_a["conception_scenario"]).receipt.consumer_exact_geometry
    b_conc = _serve(law_b["conception_scenario"]).receipt.consumer_exact_geometry
    assert _yes_fraction(a_multi) != _yes_fraction(b_multi)
    assert (
        a_multi["denominator"]["raw_denominator_support"]
        != b_multi["denominator"]["raw_denominator_support"]
    )
    # Legitimate null effect: the untouched cohort-B slice is invariant.
    assert _yes_fraction(a_conc) == _yes_fraction(b_conc)
    assert (
        a_conc["denominator"]["raw_denominator_support"]
        == b_conc["denominator"]["raw_denominator_support"]
    )


def test_law_a_and_law_b_oracles_match_independent_arithmetic(law_a, law_b):
    """The frozen oracle equals arithmetic computed from the row law itself."""
    assert law_a["_arithmetic"]["multi_a"] == {"yes": 27, "no": 3, "denominator": 30}
    assert law_b["_arithmetic"]["multi_a"] == {"yes": 37, "no": 3, "denominator": 40}
    assert LAW_A_ORACLE["multi_binding"]["expected_fraction_yes"] == {"$exact_fraction": [9, 10]}
    assert LAW_B_ORACLE["multi_binding"]["expected_fraction_yes"] == {"$exact_fraction": [37, 40]}


# ---------------------------------------------------------------------------
# Role/target reversal and generic parent-noun-free boundary
# ---------------------------------------------------------------------------


def test_role_direction_reversal_preserves_target_condition_semantics(law_a):
    """P(POSITION | ANSWER=yes) is computed in its own direction, not the forward one."""
    forward = _serve(law_a["multi_binding_parent_context"]).receipt
    reverse = _serve(law_a["nonparent_reverse"]).receipt
    assert forward.role_direction == "MULTI_CONDITION_INTERSECTION"
    assert reverse.role_direction == ROLE_REVERSE
    assert forward.target_ref != reverse.target_ref
    forward_frac = _yes_fraction(forward.consumer_exact_geometry)
    reverse_frac = _cell_fraction(reverse.consumer_exact_geometry, "P1")
    assert forward_frac == {"$exact_fraction": [9, 10]}
    assert reverse_frac == {"$exact_fraction": [3, 4]}
    assert forward_frac != reverse_frac


def test_request_schema_carries_no_parent_nouns(law_a):
    """The generic request material contains no parent / type / household noun."""
    material = law_a["multi_binding_parent_context"]["request"].material()
    blob = str(material).upper()
    for token in ("IS_FATHER", "IS_MOTHER", "IS_PARENT", "ENNEAGRAM", "TYPE_5"):
        assert token not in blob
    # Consumer flavor is a downstream TEST-ONLY scenario label only.
    assert "TEST_ONLY_FAMILY_CARE_CONTEXT" in str(material)


# ---------------------------------------------------------------------------
# N9 world dependency binding and inference-lane distinction
# ---------------------------------------------------------------------------


def test_receipt_binds_immutable_n9_selected_and_asof_dependency_ids(law_a):
    receipt = _serve(law_a["multi_binding_parent_context"]).receipt
    world = receipt.n9_world
    assert world.n9_snapshot_state == "SELECTED_IMMUTABLE"
    assert world.selected_dependency_refs
    assert world.asof_dependency_refs
    material = receipt.material()
    assert material["n9_world"]["selected_dependency_refs"]
    assert material["n9_world"]["asof_dependency_refs"]
    assert material["n9_world"]["n9_snapshot_state"] == "SELECTED_IMMUTABLE"


def test_inference_lane_is_declared_n10e_conditioned_not_world_only(law_a):
    """Computed slices declare the N10E lane; the world carriage is not a probability."""
    receipt = _serve(law_a["multi_binding_parent_context"]).receipt
    assert receipt.inference_lane == LANE_N10E
    assert receipt.world_carriage_is_not_route_probability is True
    assert LANE_WORLD_ONLY != receipt.inference_lane
    assert "WORLD_ROUTE_ELIGIBILITY != N10E_CONDITIONED_NUMERICAL_INFERENCE" in EPISTEMIC_CEILING


# ---------------------------------------------------------------------------
# Replay determinism
# ---------------------------------------------------------------------------


def test_replay_reproduces_exactly_the_same_receipt_identity(law_a):
    c = law_a["multi_binding_parent_context"]
    first = _serve(c)
    replayed = verify_generic_world_situated_replay(
        first,
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=c["request"],
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert replayed.receipt.receipt_hash == first.receipt.receipt_hash
    assert replayed.result_hash == first.result_hash


# ---------------------------------------------------------------------------
# The eight required negative falsifiers
# ---------------------------------------------------------------------------


def test_negative_reversed_unauthorized_role(law_a):
    """REVERSE without positively scoped role-reversal authority is refused."""
    base = law_a["nonparent_reverse"]["request"]
    unauth = GenericWorldSituatedRequest(
        request_id=base.request_id + "-unauth",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=ROLE_REVERSE,
        native_unit_ref=base.native_unit_ref,
        analysis_unit_ref=base.analysis_unit_ref,
        denominator_basis_ref=base.denominator_basis_ref,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=base.model_use_ref,
        n9_world=base.n9_world,
        request_time=base.request_time,
        role_reversal_authority_ref=None,
        requested_projection=dict(base.requested_projection),
    )
    c = law_a["nonparent_reverse"]
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=unauth,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_REVERSED_UNAUTHORIZED_ROLE
    assert result.receipt.consumer_exact_geometry is None
    assert result.receipt.inference_lane == LANE_WORLD_ONLY


def test_negative_new_unit_not_authorized(law_a):
    """A new analysis unit (household/dyad) is refused: same-respondent != dyad."""
    base = law_a["multi_binding_parent_context"]["request"]
    native, household = make_unit_refs(analysis_unit="HOUSEHOLD_DYAD_UNIT")
    assert household != native
    new_unit = GenericWorldSituatedRequest(
        request_id=base.request_id + "-newunit",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=base.role_direction,
        native_unit_ref=native,
        analysis_unit_ref=household,
        denominator_basis_ref=base.denominator_basis_ref,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=base.model_use_ref,
        n9_world=base.n9_world,
        request_time=base.request_time,
        requested_projection=dict(base.requested_projection),
    )
    c = law_a["multi_binding_parent_context"]
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=new_unit,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_NEW_UNIT
    assert result.receipt.consumer_exact_geometry is None


def test_negative_artificial_parent_sampling_refused_at_boundary(law_a):
    """Parent-assignment / type tokens in the request are refused at construction."""
    base = law_a["multi_binding_parent_context"]["request"]
    with pytest.raises(GenericWorldRequestLawError) as excinfo:
        GenericWorldSituatedRequest(
            request_id=base.request_id + "-parent",
            subject_ref=base.subject_ref,
            target_ref=base.target_ref,
            conditioner_bindings=base.conditioner_bindings,
            role_direction=base.role_direction,
            native_unit_ref=base.native_unit_ref,
            analysis_unit_ref=base.analysis_unit_ref,
            denominator_basis_ref=base.denominator_basis_ref,
            operation_authority_ref=base.operation_authority_ref,
            model_use_ref=base.model_use_ref,
            n9_world=base.n9_world,
            request_time=base.request_time,
            requested_projection={
                "kind": "GENERIC_WORLD_SITATED_POSSIBILITY",
                "claim": "IS_PARENT ARTIFICIAL_PARENT_SAMPLING",
            },
        )
    assert REFUSAL_ARTIFICIAL_PARENT_SAMPLING in str(excinfo.value)


def test_negative_fake_model_use_refused(law_a):
    """A request model-use ref that does not match the governed model rule is refused."""
    base = law_a["multi_binding_parent_context"]["request"]
    c = law_a["multi_binding_parent_context"]
    fake_model = type(c["model_rule"].model_authority_ref)(
        authority_id="urn:test:postastra-pe:fake-model",
        authority_version="0.0.1",
        authority_content_hash=semantic_hash({"fake": True}),
    )
    forged = GenericWorldSituatedRequest(
        request_id=base.request_id + "-fakemodel",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=base.role_direction,
        native_unit_ref=base.native_unit_ref,
        analysis_unit_ref=base.analysis_unit_ref,
        denominator_basis_ref=base.denominator_basis_ref,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=fake_model,
        n9_world=base.n9_world,
        request_time=base.request_time,
        requested_projection=dict(base.requested_projection),
    )
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=forged,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_FAKE_MODEL_USE
    assert result.receipt.consumer_exact_geometry is None


def test_negative_source_hash_forgery_rejected_by_custody_witness(law_a):
    """A self-consistent but forged producer-predicate hash is caught semantically."""
    c = law_a["multi_binding_parent_context"]
    original = c["witness"]
    identity = dict(original.identity_material)
    identity["producer_predicate_hash"] = "0" * 64
    forged = ConditionValueBindingWitness(
        witness_ref=ExactRef(original.witness_ref.kind, original.witness_ref.object_id, semantic_hash(identity)),
        identity_material=identity,
        subject_condition_preimage_refs=original.subject_condition_preimage_refs,
        subject_condition_preimage_materials=original.subject_condition_preimage_materials,
        producer_predicate_leaf_refs=original.producer_predicate_leaf_refs,
        producer_predicate_leaf_projections=original.producer_predicate_leaf_projections,
        pairing_ground_truth_refs=original.pairing_ground_truth_refs,
        pairing_ground_truth_materials=original.pairing_ground_truth_materials,
        pairing_authority_refs=original.pairing_authority_refs,
    )
    # Structural hash integrity holds, but the semantic comparison against the
    # actual predicate must reject the forgery.
    with pytest.raises(Exception):
        serve_generic_world_situated_possibility(
            repository=c["repository"],
            empirical_query=c["empirical_query"],
            predicate=c["predicate"],
            authority_registry=c["registry"],
            release_refs=c["release_refs"],
            request=c["request"],
            model_rule=c["model_rule"],
            condition_binding_witness=forged,
        )


def test_negative_missing_conditional_denominator_refused(law_a):
    """A denominator basis that does not match the producer risk set is refused."""
    base = law_a["multi_binding_parent_context"]["request"]
    forged_denominator = ExactRef(
        base.denominator_basis_ref.kind,
        "urn:test:postastra-pe:forged-denominator",
        semantic_hash({"forged": "denominator"}),
    )
    forged = GenericWorldSituatedRequest(
        request_id=base.request_id + "-nodedenom",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=base.role_direction,
        native_unit_ref=base.native_unit_ref,
        analysis_unit_ref=base.analysis_unit_ref,
        denominator_basis_ref=forged_denominator,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=base.model_use_ref,
        n9_world=base.n9_world,
        request_time=base.request_time,
        requested_projection=dict(base.requested_projection),
    )
    c = law_a["multi_binding_parent_context"]
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=forged,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_MISSING_DENOMINATOR
    assert result.receipt.consumer_exact_geometry is None


def test_negative_invalidated_current_refused(law_a):
    """An invalidated N9 snapshot yields a typed refusal, never a stale positive."""
    base = law_a["multi_binding_parent_context"]["request"]
    invalidated = GenericWorldSituatedRequest(
        request_id=base.request_id + "-invalid",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=base.role_direction,
        native_unit_ref=base.native_unit_ref,
        analysis_unit_ref=base.analysis_unit_ref,
        denominator_basis_ref=base.denominator_basis_ref,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=base.model_use_ref,
        n9_world=make_n9_world_dependency(
            tag="invalidated", snapshot_state=N9_INVALIDATED, asof_time="2021-06-30"
        ),
        request_time=base.request_time,
        requested_projection=dict(base.requested_projection),
    )
    c = law_a["multi_binding_parent_context"]
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=invalidated,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_INVALIDATED_CURRENT
    assert result.receipt.consumer_exact_geometry is None


def test_negative_future_time_availability_refused(law_a):
    """An as-of at/after the request time is not knowledge available to this request."""
    base = law_a["multi_binding_parent_context"]["request"]
    future = GenericWorldSituatedRequest(
        request_id=base.request_id + "-future",
        subject_ref=base.subject_ref,
        target_ref=base.target_ref,
        conditioner_bindings=base.conditioner_bindings,
        role_direction=base.role_direction,
        native_unit_ref=base.native_unit_ref,
        analysis_unit_ref=base.analysis_unit_ref,
        denominator_basis_ref=base.denominator_basis_ref,
        operation_authority_ref=base.operation_authority_ref,
        model_use_ref=base.model_use_ref,
        n9_world=make_n9_world_dependency(
            tag="future", asof_time="2099-01-01", request_time="2026-10-14"
        ),
        request_time="2026-10-14",
        requested_projection=dict(base.requested_projection),
    )
    c = law_a["multi_binding_parent_context"]
    result = serve_generic_world_situated_possibility(
        repository=c["repository"],
        empirical_query=c["empirical_query"],
        predicate=c["predicate"],
        authority_registry=c["registry"],
        release_refs=c["release_refs"],
        request=future,
        model_rule=c["model_rule"],
        condition_binding_witness=c["witness"],
    )
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == REFUSAL_FUTURE_TIME
    assert result.receipt.consumer_exact_geometry is None
