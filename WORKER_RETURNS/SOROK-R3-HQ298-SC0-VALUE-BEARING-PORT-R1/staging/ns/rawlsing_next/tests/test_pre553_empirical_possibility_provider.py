"""N10E empirical possibility-slice provider court (P1-P7).

Every proof claim here distinguishes the grades the commission requires:

* static inspection (signature / source inspection);
* source-free executed producer (exact synthetic AT07 law);
* generated evidence identity;
* consumer execution;
* deterministic replay.

Expected truth comes from the frozen oracle in
``n10e_empirical_slice_fixture``; the provider's own output is never used as its
own expected value.
"""
from __future__ import annotations

import inspect
from dataclasses import replace

import pytest

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionError,
    ConditionValueBindingWitness,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    FORBIDDEN_AUTHORITATIVE_INPUT_NAMES,
    PROVIDER_STATE_EXACT,
    PROVIDER_STATE_REFUSED,
    REFUSAL_STATE_SLICE_NOT_SUPPORTED,
    EmpiricalPossibilityProviderError,
    assert_provider_public_api_excludes_handwritten_slice,
    evaluate_generated_slice_directly,
    provide_empirical_possibility_slice,
    replay_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityQuery,
    PossibilitySliceEvidence,
)

from n10e_at17_successor_requal import (
    ADOPTED_SUCCESSOR,
    CONSERVED_HISTORICAL_FIELDS,
    HISTORICAL_R8,
    SUCCESSOR_SIX,
    digest,
    historical_canonical,
    historical_digest,
    successor_canonical,
)
from rawlsing_next.tests import n10e_empirical_slice_fixture as fx
import rawlsing_next.tests.test_pre553_empirical_query as i03


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _provide(case, **overrides):
    kwargs = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    kwargs.update(overrides)
    return provide_empirical_possibility_slice(**kwargs)


def _cell_numerators(result):
    return {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in result.generated_evidence_or_null.geometry["cells"]
    }


def _cell_fractions(result):
    return {
        cell["cell"]: canonicalize(cell["raw_probability_exact_fraction"])
        for cell in result.generated_evidence_or_null.geometry["cells"]
    }


def _query_with_binding(query, binding):
    return PositionedSubjectPossibilityQuery(
        query.query_id,
        query.subject_ref,
        query.target_ref,
        query.source_universe_ref,
        query.release_ref,
        (binding,),
        query.requested_projection,
        purpose=query.purpose,
    )


def _witness_with_identity(witness, material):
    return ConditionValueBindingWitness(
        witness_ref=ExactRef(
            witness.witness_ref.kind, witness.witness_ref.object_id, semantic_hash(material)
        ),
        identity_material=material,
        subject_condition_preimage_ref=witness.subject_condition_preimage_ref,
        subject_condition_preimage_material=witness.subject_condition_preimage_material,
        producer_predicate_leaf_ref=witness.producer_predicate_leaf_ref,
        producer_predicate_leaf_projection=witness.producer_predicate_leaf_projection,
        pairing_ground_truth_ref=witness.pairing_ground_truth_ref,
        pairing_ground_truth_material=witness.pairing_ground_truth_material,
        pairing_authority_ref=witness.pairing_authority_ref,
    )


# --------------------------------------------------------------------------
# P1 - actual computed forward slice
# --------------------------------------------------------------------------
def test_p1_forward_slice_is_actually_computed_and_producer_derived():
    case = fx.build_provider_case("forward")
    oracle = fx.FROZEN_ORACLE["forward"]
    result = _provide(case)

    assert result.provider_state == PROVIDER_STATE_EXACT
    evidence = result.generated_evidence_or_null
    assert evidence is not None and result.consumer_result_or_null is not None

    # Geometry truth is frozen arithmetic on the synthetic source law (54 yes / 60).
    assert evidence.raw_support == oracle["denominator"] == 60
    assert _cell_numerators(result) == oracle["cells"] == {"yes": 54, "no": 6}
    assert _cell_fractions(result) == {
        "yes": oracle["expected_fraction"],
        "no": {"$exact_fraction": [1, 10]},
    }

    # Denominators/member support flow from the producer fact, not from the caller.
    geometry = canonicalize(evidence.geometry)
    assert geometry["denominator"]["raw_denominator_support"] == 60
    assert geometry["denominator"]["denominator_member_refs"] == [
        x.as_dict()
        for x in result.composition_result.denominator_member_refs
    ]
    assert len(geometry["denominator"]["denominator_member_refs"]) == 60
    assert evidence.source_universe_ref == case["consumer_query"].source_universe_ref
    assert evidence.release_ref == case["consumer_query"].release_ref
    assert evidence.target_ref == case["consumer_query"].target_ref
    assert evidence.retained_conditioner_ids == case["consumer_query"].conditioner_ids

    # Consumer execution on the generated evidence.
    assert result.consumer_result_or_null.result_state == oracle["expected_consumer_state"]
    assert result.consumer_result_or_null.exact_evidence_ref == evidence.evidence_ref
    assert result.consumer_result_or_null.exact_geometry == evidence.geometry


def test_p1_evidence_identity_is_the_producer_generated_object_not_handwritten():
    case = fx.build_provider_case("forward")
    result = _provide(case)
    composition = result.composition_result

    # Identity grade: same object, same ref, hash over the producer evidence preimage.
    assert result.generated_evidence_or_null is composition.possibility_slice_evidence_or_null
    assert (
        result.generated_evidence_or_null.evidence_ref
        == composition.possibility_slice_evidence_or_null.evidence_ref
    )
    assert (
        result.provider_receipt.generated_evidence_identity_is_producer_derived is True
    )
    assert (
        result.provider_receipt.generated_evidence_ref
        == composition.possibility_slice_evidence_or_null.evidence_ref
    )
    assert (
        result.consumer_result_or_null
        is composition.consumer_result_or_null
    )


def test_p1_receipt_binds_producer_and_consumer_identities_exactly():
    case = fx.build_provider_case("forward")
    result = _provide(case)
    receipt = result.provider_receipt.material()

    assert receipt["producer_input"]["producer_query_ref"] == (
        case["empirical_query"].ref.as_dict()
    )
    assert receipt["producer_input"]["producer_predicate_ref"] == (
        case["predicate"].ref.as_dict()
    )
    assert receipt["producer_input"]["producer_fact_ref"] == (
        result.composition_result.producer_fact_ref.as_dict()
    )
    assert receipt["consumer"]["consumer_query_ref"] == (
        case["consumer_query"].ref.as_dict()
    )
    assert receipt["consumer"]["condition_binding_witness_ref"] == (
        case["condition_binding_witness"].witness_ref.as_dict()
    )
    assert receipt["consumer"]["result_identity_hash_or_null"] == (
        result.consumer_result_or_null.result_hash
    )
    assert receipt["composed_result_identity_hash"] == (
        result.composition_result.composed_result_identity_hash
    )
    # Exact dependency closure: the receipt loses no producer/evidence identity.
    assert receipt["generated_evidence"]["evidence_ref_or_null"] == (
        result.generated_evidence_or_null.evidence_ref.as_dict()
    )
    assert case["release_refs"] == tuple(result.composition_result.release_refs)


def test_p1_provider_does_not_recompute_or_duplicate_owner_geometry():
    """The provider must not carry its own probability arithmetic."""

    import rawlsing_next.pre553_empirical_possibility_provider as provider

    source = inspect.getsource(provider)
    assert "Fraction(" not in source
    assert "float(" not in source
    assert "_exact_fraction" not in source


# --------------------------------------------------------------------------
# P2 - actual computed reverse slice
# --------------------------------------------------------------------------
def test_p2_reverse_slice_preserves_target_topology_risk_support_and_exact_fraction():
    case = fx.build_provider_case("reverse")
    oracle = fx.FROZEN_ORACLE["reverse"]
    result = _provide(case)

    assert result.provider_state == PROVIDER_STATE_EXACT
    evidence = result.generated_evidence_or_null
    assert evidence.raw_support == oracle["denominator"] == 62
    assert _cell_numerators(result) == oracle["cells"] == {"P1": 54, "P2": 8}
    assert _cell_fractions(result)["P1"] == oracle["expected_fraction"]

    # Target topology and risk support are the accepted reverse direction's.
    assert evidence.target_ref == case["consumer_query"].target_ref
    assert evidence.retained_conditioner_ids == case["consumer_query"].conditioner_ids
    topology = canonicalize(result.composition_result.target_arity_and_topology)
    assert topology["arity"] == 1
    assert topology["components"][0]["target_ref"] == evidence.target_ref.as_dict()
    assert result.consumer_result_or_null.result_state == oracle["expected_consumer_state"]
    assert result.consumer_result_or_null.exact_evidence_ref == evidence.evidence_ref

    forward = _provide(fx.build_provider_case("forward"))
    assert evidence.evidence_ref != forward.generated_evidence_or_null.evidence_ref
    assert (
        result.receipt_ref != forward.receipt_ref
    ), "direction is an identity-bearing determinant"


def test_p2_forward_and_reverse_share_no_receipt_or_slice_identity():
    forward = _provide(fx.build_provider_case("forward"))
    reverse = _provide(fx.build_provider_case("reverse"))
    assert forward.receipt_ref != reverse.receipt_ref
    assert forward.result_identity_hash != reverse.result_identity_hash
    assert (
        forward.provider_receipt.producer_predicate_ref
        != reverse.provider_receipt.producer_predicate_ref
    )


# --------------------------------------------------------------------------
# P3 - identity/dependency closure
# --------------------------------------------------------------------------
def test_p3_identity_bearing_conditioner_determinant_reidentifies_provider_output():
    case = fx.build_provider_case("forward")
    baseline = _provide(case)
    binding = case["conditioner_binding"]

    # Legitimate source-free determinant mutation: the conditioner's effective time.
    mutated_binding = ConditionerBinding(
        binding.binding_id,
        binding.subject_fact_ref,
        binding.empirical_coordinate_ref,
        binding.comparability_authority_ref,
        binding.source_universe_ref,
        binding.release_ref,
        "N10E_FIXTURE_ONLY_TIME_MUTATION",
    )
    mutated_query = _query_with_binding(case["consumer_query"], mutated_binding)
    mutated_witness = fx.build_witness(
        case["source"],
        "forward",
        mutated_query,
        mutated_binding,
        case["empirical_query"],
        case["predicate"],
    )
    assert mutated_witness.witness_ref != case["condition_binding_witness"].witness_ref
    mutated_witness.verify_identity()

    mutated = _provide(
        case, consumer_query=mutated_query, condition_binding_witness=mutated_witness
    )

    # The provider receipt reidentifies with the mutated determinant.
    assert mutated.receipt_ref != baseline.receipt_ref
    assert mutated.result_identity_hash != baseline.result_identity_hash
    assert (
        mutated.provider_receipt.condition_binding_witness_ref
        != baseline.provider_receipt.condition_binding_witness_ref
    )
    assert (
        mutated.provider_receipt.consumer_query_ref
        != baseline.provider_receipt.consumer_query_ref
    )
    assert (
        mutated.provider_receipt.consumed_binding_fingerprint
        if False
        else mutated.provider_receipt.consumer_binding_fingerprint
    ) != baseline.provider_receipt.consumer_binding_fingerprint
    # The unconsumed empirical geometry is unchanged by a conditioner-time mutation.
    assert mutated.generated_evidence_or_null.raw_support == 60
    assert (
        mutated.generated_evidence_or_null.evidence_ref
        != baseline.generated_evidence_or_null.evidence_ref
    )


def test_p3_model_rule_determinant_reidentifies_receipt_and_result():
    case = fx.build_provider_case("forward")
    baseline = _provide(case)

    rule = case["model_rule"]
    mutated_rule = type(rule)(
        fx.fixture_authority("FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL"),
        fx.fixture_authority("FIXTURE_ONLY_WALKBACK_POLICY"),
        rule.source_universe_refs,
        rule.walkback_steps,
        rule.positive_proxy_authority_refs,
    )
    # Same rule identity must reproduce; a different rule identity must reidentify.
    assert mutated_rule.rule_hash == rule.rule_hash

    hostile_rule = type(rule)(
        fx.fixture_authority("FIXTURE_ONLY_WALKBACK_POLICY"),
        fx.fixture_authority("FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL"),
        rule.source_universe_refs,
        rule.walkback_steps,
        rule.positive_proxy_authority_refs,
    )
    assert hostile_rule.rule_hash != rule.rule_hash
    mutated = _provide(case, model_rule=hostile_rule)
    assert mutated.receipt_ref != baseline.receipt_ref
    assert (
        mutated.composition_result.composed_result_identity_hash
        != baseline.composition_result.composed_result_identity_hash
    )


def test_p3_unconsumed_irrelevant_material_is_not_a_determinant():
    """An unused extra object in the same universe must not change provider identity."""

    case = fx.build_provider_case("forward")
    baseline = _provide(case)
    # An extra authority snapshot that is never consumed by the producer or consumer.
    extra = i03._auth(
        "n10e-unconsumed", "COORDINATE_SEMANTICS", families=("EmpiricalCoordinateFact@1.0.0",)
    )
    registry_with_extra = AuthorityRegistry(
        (*case["source"]["authorities"], case["query_authority"], extra)
    )
    with_extra = _provide(case, authority_registry=registry_with_extra)

    assert with_extra.receipt_ref == baseline.receipt_ref
    assert with_extra.result_identity_hash == baseline.result_identity_hash
    assert (
        with_extra.generated_evidence_or_null.evidence_ref
        == baseline.generated_evidence_or_null.evidence_ref
    )


def test_p3_receipt_declares_exact_dependency_closure_over_producer_evidence():
    case = fx.build_provider_case("forward")
    result = _provide(case)
    receipt = result.provider_receipt
    composition = result.composition_result

    assert receipt.producer_query_ref == composition.producer_query_ref
    assert receipt.producer_predicate_ref == composition.producer_predicate_ref
    assert receipt.producer_fact_ref == composition.producer_fact_ref
    assert set(receipt.source_universe_refs) == set(composition.source_universe_refs)
    assert set(receipt.release_refs) == set(composition.release_refs)
    assert receipt.composed_result_identity_hash == (
        composition.composed_result_identity_hash
    )
    assert receipt.model_rule_hash == case["model_rule"].rule_hash


# --------------------------------------------------------------------------
# P4 - no handwritten slice substitution
# --------------------------------------------------------------------------
def test_p4_public_api_exposes_no_precomputed_slice_channel():
    signature = inspect.signature(provide_empirical_possibility_slice)
    assert set(signature.parameters) == {
        "repository",
        "empirical_query",
        "predicate",
        "authority_registry",
        "release_refs",
        "consumer_query",
        "model_rule",
        "condition_binding_witness",
    }
    assert FORBIDDEN_AUTHORITATIVE_INPUT_NAMES.isdisjoint(signature.parameters)
    assert_provider_public_api_excludes_handwritten_slice()

    with pytest.raises(TypeError):
        provide_empirical_possibility_slice(
            repository=None,
            empirical_query=None,
            predicate=None,
            authority_registry=None,
            release_refs=(),
            consumer_query=None,
            model_rule=None,
            condition_binding_witness=None,
            evidence=object(),
        )


def test_p4_provider_recomputes_and_ignores_attacker_evidence_in_scope():
    """A handwritten evidence object must not be able to satisfy the provider."""

    case = fx.build_provider_case("forward")
    real = _provide(case)
    generated = real.generated_evidence_or_null

    hostile_geometry = canonicalize(generated.geometry)
    hostile_cells = [dict(cell) for cell in hostile_geometry["cells"]]
    for cell in hostile_cells:
        if cell["cell"] == "yes":
            cell["raw_numerator_support"] = 999
            cell["raw_probability_exact_fraction"] = {"$exact_fraction": [999, 60]}
    hostile_geometry["cells"] = hostile_cells
    hostile_preimage = {"fixture_only": "N10E_HANDWRITTEN_SLICE_SUBSTITUTION"}
    hostile_evidence = PossibilitySliceEvidence(
        evidence_ref=ExactRef(
            generated.evidence_ref.kind,
            "urn:test:n10e:handwritten-slice",
            semantic_hash(hostile_preimage),
        ),
        source_universe_ref=generated.source_universe_ref,
        release_ref=generated.release_ref,
        target_ref=generated.target_ref,
        retained_conditioner_ids=generated.retained_conditioner_ids,
        evidence_state="SUPPORTED",
        geometry=hostile_geometry,
        raw_support=999,
        uncertainty_state=generated.uncertainty_state,
        provenance_refs=(),
        authority_refs=(),
    )

    # The provider has no channel for it: re-running still yields computed truth.
    assert "evidence" not in inspect.signature(
        provide_empirical_possibility_slice
    ).parameters
    assert real.generated_evidence_or_null.raw_support == 60
    assert real.generated_evidence_or_null.evidence_ref != hostile_evidence.evidence_ref

    # The low-level consumer helper consumes whatever object it is handed. That is
    # exactly why it grants no authority and is not the provider path.
    laundered = evaluate_generated_slice_directly(
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        generated_evidence=hostile_evidence,
    )
    assert laundered.exact_evidence_ref == hostile_evidence.evidence_ref
    assert laundered.result_hash != real.consumer_result_or_null.result_hash
    assert (
        laundered.exact_evidence_ref
        != real.consumer_result_or_null.exact_evidence_ref
    )


def test_p4_provider_result_cannot_claim_evidence_it_did_not_generate():
    case = fx.build_provider_case("forward")
    real = _provide(case)
    fabricated = PossibilitySliceEvidence(
        evidence_ref=ExactRef("C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1", "urn:test:n10e:fake", "a" * 64),
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
        target_ref=case["consumer_query"].target_ref,
        retained_conditioner_ids=case["consumer_query"].conditioner_ids,
        evidence_state="SUPPORTED",
        geometry=real.generated_evidence_or_null.geometry,
        raw_support=60,
        uncertainty_state=real.generated_evidence_or_null.uncertainty_state,
    )
    with pytest.raises(EmpiricalPossibilityProviderError, match="generated evidence object"):
        type(real)(
            provider_state=PROVIDER_STATE_EXACT,
            provider_receipt=real.provider_receipt,
            composition_result=real.composition_result,
            generated_evidence_or_null=fabricated,
            consumer_result_or_null=real.consumer_result_or_null,
        )


# --------------------------------------------------------------------------
# P5 - fail-closed context mismatch
# --------------------------------------------------------------------------
def test_p5_source_release_mismatch_fails_closed_with_owner_typed_error():
    case = fx.build_provider_case("forward")
    wrong_release = i03._ref("C11LogicalRelease", "n10e-wrong-release")
    with pytest.raises(AnalyticalCompositionError, match="SOURCE_RELEASE_MISMATCH"):
        _provide(case, release_refs=(wrong_release,))


def test_p5_target_topology_mismatch_fails_closed_with_owner_typed_error():
    case = fx.build_provider_case("forward")
    # Reverse consumer target (POSITION) against the forward producer (ANSWER).
    reverse_case = fx.build_provider_case("reverse")
    with pytest.raises(
        AnalyticalCompositionError, match="TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH"
    ):
        _provide(case, consumer_query=reverse_case["consumer_query"])


def _foreign_universe_consumer_query(case, foreign_universe):
    """A *coherent* consumer query whose universe is foreign to the producer."""

    binding = case["conditioner_binding"]
    foreign_binding = ConditionerBinding(
        binding.binding_id,
        binding.subject_fact_ref,
        binding.empirical_coordinate_ref,
        binding.comparability_authority_ref,
        foreign_universe,
        binding.release_ref,
        binding.effective_time_or_interval,
    )
    return PositionedSubjectPossibilityQuery(
        case["consumer_query"].query_id,
        case["consumer_query"].subject_ref,
        case["consumer_query"].target_ref,
        foreign_universe,
        case["consumer_query"].release_ref,
        (foreign_binding,),
        case["consumer_query"].requested_projection,
    )


def test_p5_consumer_query_rejects_implicit_universe_bridge_at_construction():
    """Owner law: a conditioner may not silently bridge to another universe."""

    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityError,
    )

    case = fx.build_provider_case("forward")
    foreign_universe = i03._ref("EmpiricalUniverse", "n10e-foreign-universe")

    # Coherent foreign pair (binding and query agree) is constructible...
    coherent = _foreign_universe_consumer_query(case, foreign_universe)
    assert coherent.source_universe_ref == foreign_universe

    # ...but keeping the original binding while moving the query is refused.
    with pytest.raises(
        PositionedSubjectPossibilityError,
        match="conditioner source/release mismatch",
    ):
        PositionedSubjectPossibilityQuery(
            case["consumer_query"].query_id,
            case["consumer_query"].subject_ref,
            case["consumer_query"].target_ref,
            foreign_universe,
            case["consumer_query"].release_ref,
            (case["conditioner_binding"],),
            case["consumer_query"].requested_projection,
        )


def test_p5_foreign_universe_consumer_query_fails_closed_against_producer():
    case = fx.build_provider_case("forward")
    foreign_universe = i03._ref("EmpiricalUniverse", "n10e-foreign-universe")
    foreign_query = _foreign_universe_consumer_query(case, foreign_universe)

    assert foreign_query.release_ref == case["consumer_query"].release_ref
    assert foreign_query.target_ref == case["consumer_query"].target_ref
    assert foreign_query.source_universe_ref != case["consumer_query"].source_universe_ref

    with pytest.raises(AnalyticalCompositionError, match="SOURCE_UNIVERSE_MISMATCH"):
        _provide(case, consumer_query=foreign_query)


def test_p5_foreign_universe_producer_fails_closed_when_consumer_matches_source():
    """Producer whose empirical universe differs from the consumer's source universe."""

    case = fx.build_provider_case("forward")
    foreign_universe = i03._ref("EmpiricalUniverse", "n10e-foreign-universe")

    foreign_empirical_query = i03._query(
        case["source"],
        case["query_authority"],
        case["predicate"],
        ("ANSWER",),
        risk="R",
        universe_refs=(foreign_universe,),
        tag="n10e-foreign-universe",
    )
    assert foreign_empirical_query.risk_set_ref == case["empirical_query"].risk_set_ref
    assert foreign_empirical_query.target_refs == case["empirical_query"].target_refs

    with pytest.raises(AnalyticalCompositionError, match="SOURCE_UNIVERSE_MISMATCH"):
        _provide(case, empirical_query=foreign_empirical_query)


def test_p5_model_source_universe_out_of_scope_returns_fail_closed_result():
    case = fx.build_provider_case("forward")
    rule = case["model_rule"]
    foreign = i03._ref("EmpiricalUniverse", "n10e-foreign-universe")
    out_of_scope = type(rule)(
        rule.model_authority_ref,
        rule.walkback_authority_ref,
        (foreign,),
        rule.walkback_steps,
        rule.positive_proxy_authority_refs,
    )
    result = _provide(case, model_rule=out_of_scope)
    assert result.provider_state == PROVIDER_STATE_EXACT
    assert result.consumer_result_or_null.result_state == "FAIL_CLOSED"
    assert (
        result.consumer_result_or_null.exact_reason
        == "MODEL_SOURCE_UNIVERSE_OUT_OF_SCOPE"
    )


# --------------------------------------------------------------------------
# P6 - no unauthorized smoothing / proxy laundering
# --------------------------------------------------------------------------
def test_p6_non_supported_slice_returns_typed_refusal_without_invented_geometry(
    monkeypatch,
):
    """A producer fact that is not SUPPORTED yields a typed refusal, never geometry.

    The refusal branch is exercised through the real provider entry point by
    substituting only the *producer fact state*: the real composition still runs,
    and the provider's own fail-closed law is what is under test.
    """

    import rawlsing_next.pre553_empirical_possibility_provider as provider

    case = fx.build_provider_case("forward")
    composition = _provide(case).composition_result
    unsupported = replace(
        composition,
        producer_fact_state="ZERO_SUPPORT",
        analytical_state="ZERO_SUPPORT",
        possibility_slice_evidence_or_null=None,
        consumer_result_or_null=None,
        complete_cell_geometry=(),
    )
    monkeypatch.setattr(
        provider,
        "compose_positioned_subject_possibility",
        lambda **kwargs: unsupported,
    )

    result = _provide(case)

    assert result.provider_state == PROVIDER_STATE_REFUSED
    assert result.refusal_state == REFUSAL_STATE_SLICE_NOT_SUPPORTED
    assert result.refusal_owner_error_code == "ZERO_SUPPORT"
    assert result.generated_evidence_or_null is None
    assert result.consumer_result_or_null is None
    assert result.composition_result.complete_cell_geometry == ()
    assert result.composition_result.possibility_slice_evidence_or_null is None
    assert result.provider_receipt.generated_evidence_ref is None
    assert (
        result.provider_receipt.generated_evidence_identity_is_producer_derived is False
    )
    assert result.provider_receipt.consumer_result_identity_hash is None
    assert result.provider_receipt.refusal_state == REFUSAL_STATE_SLICE_NOT_SUPPORTED
    assert "no smoothing" in result.refusal_reason


def test_p6_exact_result_shape_guards_reject_refusal_and_substituted_evidence():
    """Result-constructor guards: an exact result cannot carry refusal geometry."""

    case = fx.build_provider_case("forward")
    real = _provide(case)
    assert real.generated_evidence_or_null is not None

    # A refusal-shaped claim carrying evidence is refused by the provider shape law.
    with pytest.raises(EmpiricalPossibilityProviderError):
        type(real)(
            provider_state=PROVIDER_STATE_REFUSED,
            provider_receipt=real.provider_receipt,
            composition_result=real.composition_result,
            generated_evidence_or_null=real.generated_evidence_or_null,
            consumer_result_or_null=real.consumer_result_or_null,
        )


def test_p6_zero_support_predicate_mutation_is_caught_by_custody_witness():
    """The empirical producer cannot be re-pointed without matching custody."""

    case = fx.build_provider_case("forward")
    source = case["source"]
    query_auth = case["query_authority"]

    empty_leaf = i03._response_leaf(source, query_auth, "POSITION", "P3")
    empty_predicate = i03._predicate(source, query_auth, empty_leaf, tag="n10e-empty")
    empty_query = i03._query(
        source, query_auth, empty_predicate, ("ANSWER",), risk="R", tag="n10e-empty"
    )
    # The ZERO_SUPPORT predicate is real, but the AT07 custody witness does not
    # match it, so the provider fails closed before any evidence is produced.
    with pytest.raises(Exception) as excinfo:
        _provide(case, empirical_query=empty_query, predicate=empty_predicate)
    assert "CONDITION_VALUE_RELATION_MISMATCH" in str(excinfo.value)


def test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes():
    """Changed-source proof (REV-N10E-001).

    A second, genuinely different source-free empirical law is built through the same
    fixture procedure and the *real* provider is run against it. The provider's
    denominator and cell geometry must follow the changed empirical product — proving
    the geometry is derived from the empirical source law rather than fixed.
    """

    canonical = fx.build_provider_case("forward")
    changed = fx.build_provider_case("forward", variant=fx.CHANGED_SOURCE_VARIANT)
    oracle = fx.FROZEN_CHANGED_ORACLE
    relation = oracle["expected_relation_to_canonical"]

    # --- the changed case really is a different empirical source -----------------
    assert changed["variant"] == fx.CHANGED_SOURCE_VARIANT
    assert changed["source"]["universe"].ref != canonical["source"]["universe"].ref
    assert changed["source"]["release_ref"] != canonical["source"]["release_ref"]
    assert relation["source_universe_ref_differs"] is True
    assert relation["source_release_ref_differs"] is True
    assert len(changed["source"]["respondents"]) == oracle["fixture_rows"] == 110
    assert len(canonical["source"]["respondents"]) == 100
    # Same fixture procedure: same question refs, same conditioner grain, same domains.
    assert changed["source"]["qrefs"] == canonical["source"]["qrefs"]
    assert (
        changed["consumer_query"].conditioner_ids
        == canonical["consumer_query"].conditioner_ids
    )

    # --- run the real provider on both ------------------------------------------
    canonical_result = _provide(canonical)
    changed_result = _provide(changed)

    assert canonical_result.provider_state == PROVIDER_STATE_EXACT
    assert changed_result.provider_state == PROVIDER_STATE_EXACT

    # --- geometry follows the changed source law, not a constant -----------------
    assert canonical_result.generated_evidence_or_null.raw_support == 60
    assert changed_result.generated_evidence_or_null.raw_support == oracle["forward"]["denominator"] == 70
    assert (
        changed_result.generated_evidence_or_null.raw_support
        != canonical_result.generated_evidence_or_null.raw_support
    ), "changed empirical law must change the produced denominator"

    changed_cells = _cell_numerators(changed_result)
    assert changed_cells == oracle["forward"]["cells"] == {"yes": 54, "no": 16}
    assert changed_cells != _cell_numerators(canonical_result)
    assert _cell_fractions(changed_result) == {
        "yes": oracle["forward"]["expected_fraction_yes"],
        "no": oracle["forward"]["expected_fraction_no"],
    }
    # The conditioner cohort is unchanged, so the "yes" cell is unchanged while the
    # denominator and the "no" cell move: the change is in the empirical product.
    assert changed_cells["yes"] == _cell_numerators(canonical_result)["yes"]
    assert relation["forward_yes_cell_unchanged"] is True
    assert relation["forward_denominator_differs"] is True
    assert relation["forward_cells_differ"] is True

    # --- the changed slice still comes through the accepted seam -----------------
    changed_composition = changed_result.composition_result
    changed_evidence = changed_result.generated_evidence_or_null
    assert (
        changed_evidence
        is changed_composition.possibility_slice_evidence_or_null
    ), "changed-source evidence must be the composition's generated object"
    assert (
        changed_result.consumer_result_or_null
        is changed_composition.consumer_result_or_null
    )
    assert changed_result.provider_receipt.generated_evidence_identity_is_producer_derived
    # ... and it tracks the changed producer fact, not a fabricated one.
    changed_fact = changed_composition.producer_result.facts[0]
    assert (
        changed_evidence.raw_support
        == changed_fact.raw_denominator_support
        == changed_composition.raw_denominator_support
        == 70
    )
    assert changed_composition.producer_fact_ref == changed_fact.ref
    assert changed_composition.producer_fact_ref != canonical_result.composition_result.producer_fact_ref
    assert changed_evidence.evidence_ref != canonical_result.generated_evidence_or_null.evidence_ref
    assert changed_result.receipt_ref != canonical_result.receipt_ref
    assert changed_result.consumer_result_or_null.result_state == (
        oracle["forward"]["expected_consumer_state"]
    )

    # --- the reverse direction of the changed law is a genuine control -----------
    # It shares the unchanged 62 respondents, so its geometry must NOT move: this
    # rules out "the provider just returned something different for any second case".
    changed_reverse = _provide(
        fx.build_provider_case("reverse", variant=fx.CHANGED_SOURCE_VARIANT)
    )
    canonical_reverse = _provide(fx.build_provider_case("reverse"))
    assert changed_reverse.generated_evidence_or_null.raw_support == (
        oracle["reverse"]["denominator"]
    ) == 62
    assert (
        changed_reverse.generated_evidence_or_null.raw_support
        == canonical_reverse.generated_evidence_or_null.raw_support
    )
    assert _cell_numerators(changed_reverse) == oracle["reverse"]["cells"] == {
        "P1": 54,
        "P2": 8,
    }
    assert relation["reverse_denominator_unchanged"] is True
    # The reverse slices are distinct because the source identity differs, even
    # though the counts agree: identity follows the empirical source, not the number.
    assert (
        changed_reverse.generated_evidence_or_null.evidence_ref
        != canonical_reverse.generated_evidence_or_null.evidence_ref
    )


def test_p6_exact_supported_evidence_stays_exact_and_unweighted():
    case = fx.build_provider_case("forward")
    result = _provide(case)
    evidence = result.generated_evidence_or_null
    geometry = canonicalize(evidence.geometry)

    assert evidence.evidence_state == "SUPPORTED"
    assert geometry["measure"]["measure_kind"] == "RAW"
    assert geometry["measure"]["weight_basis_id_or_null"] is None
    assert geometry["measure"]["weight_design_estimand_context"] is None
    for cell in geometry["cells"]:
        assert cell["weighted_numerator_support_if_authorized"] is None
        assert cell["weighted_probability_exact_fraction_if_authorized"] is None
        assert cell["raw_probability_exact_fraction"] is not None


def test_p6_provider_declares_no_new_proxy_or_actor_authority():
    import rawlsing_next.pre553_empirical_possibility_provider as provider

    source = inspect.getsource(provider)
    assert "SpecificityWalkbackStep" not in source
    assert "ProxyPossibilityProjection" not in source
    # The provider creates no proxy lane: it never selects a broader slice itself.
    assert "positive_proxy_authority_refs=(" not in source.replace(" ", "")
    text = source.lower()
    for forbidden in ("stereotype", "actor_inference_allowed", "persona", "belief"):
        assert forbidden not in text


def test_p6_no_float_or_approximate_geometry_anywhere_in_provider_output():
    case = fx.build_provider_case("forward")
    result = _provide(case)

    def walk(value):
        if isinstance(value, float):
            raise AssertionError("float geometry present")
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    walk(result.material())
    walk(canonicalize(result.generated_evidence_or_null.geometry))


# --------------------------------------------------------------------------
# P7 - replay
# --------------------------------------------------------------------------
def test_p7_receipt_and_result_identity_replay_deterministically():
    case = fx.build_provider_case("forward")
    first = _provide(case)
    second = replay_empirical_possibility_slice(
        first,
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    assert second.receipt_ref == first.receipt_ref
    assert second.result_identity_hash == first.result_identity_hash
    assert second.material() == first.material()
    assert (
        second.generated_evidence_or_null.evidence_ref
        == first.generated_evidence_or_null.evidence_ref
    )
    assert (
        second.consumer_result_or_null.result_hash
        == first.consumer_result_or_null.result_hash
    )


def test_p7_replay_detects_a_different_result_identity():
    case = fx.build_provider_case("forward")
    first = _provide(case)
    other = _provide(fx.build_provider_case("reverse"))
    with pytest.raises(EmpiricalPossibilityProviderError, match="replay mismatch"):
        replay_empirical_possibility_slice(
            other,
            repository=case["source"]["repo"],
            empirical_query=case["empirical_query"],
            predicate=case["predicate"],
            authority_registry=case["registry"],
            release_refs=case["release_refs"],
            consumer_query=case["consumer_query"],
            model_rule=case["model_rule"],
            condition_binding_witness=case["condition_binding_witness"],
        )
    assert first.receipt_ref != other.receipt_ref


def test_p7_fresh_process_replay_reproduces_provider_receipt():
    """Fresh interpreter, same frozen inputs -> same receipt/result identity."""

    import json
    import os
    import subprocess
    import sys

    case = fx.build_provider_case("forward")
    in_process = _provide(case)

    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "rawlsing_next.tests.n10e_empirical_slice_fresh_process_runner",
            "forward",
        ],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert completed.returncode == 0, completed.stderr
    fresh = json.loads(completed.stdout)

    assert fresh["provider_state"] == in_process.provider_state
    assert fresh["receipt_ref_hash"] == in_process.receipt_ref.content_hash
    assert fresh["result_identity_hash"] == in_process.result_identity_hash
    assert (
        fresh["evidence_ref_hash"]
        == in_process.generated_evidence_or_null.evidence_ref.content_hash
    )
    assert (
        fresh["consumer_result_hash"]
        == in_process.consumer_result_or_null.result_hash
    )
    assert fresh["composed_result_identity_hash"] == (
        in_process.composition_result.composed_result_identity_hash
    )
    assert fresh["raw_denominator_support"] == 60
    assert fresh["cell_numerators"] == {"yes": 54, "no": 6}


def test_p7_historical_fixture_law_bindings_still_hold():
    """AT07 fixture law is still the accepted law, not a drifting copy.

    Every binding the R8 spine recorded about the FIXTURE LAW is unchanged under the
    adopted C1-02 owner: universe, release scope, query authority, predicate and
    predicate hash, producer and consumer queries, the 16-field witness, the generated
    evidence ref, and the raw denominator support.
    """
    spine = fx.frozen_spine()
    case = fx.build_provider_case("forward")
    assert case["source"]["universe"].ref.as_dict() == spine["universe_ref"]
    assert case["source"]["release_ref"].as_dict() == spine["release_ref"]
    assert case["query_authority"].authority_ref.as_dict() == spine["query_authority_ref"]
    assert case["predicate"].ref.as_dict() == spine["forward"]["producer_predicate_ref"]
    assert case["predicate"].predicate_hash == spine["forward"]["producer_predicate_hash"]
    assert case["empirical_query"].ref.as_dict() == spine["forward"]["producer_query_ref"]
    assert (
        case["consumer_query"].ref.as_dict() == spine["forward"]["consumer_query_ref"]
    )
    assert (
        case["condition_binding_witness"].witness_ref.as_dict()
        == spine["forward"]["witness_ref"]
    )

    result = _provide(case)
    assert result.generated_evidence_or_null.evidence_ref.as_dict() == (
        spine["forward"]["evidence_ref"]
    )
    assert result.composition_result.raw_denominator_support == (
        spine["forward"]["raw_denominator_support"]
    )


def test_p7_historical_r8_composed_identity_is_preserved_as_historical_only():
    """The R8 composed identity remains historical C1-01 truth, never current.

    Astra requires the old assertion to survive as historical evidence. It is
    asserted STRONGER than before: the historical digest is re-derived from the pinned
    38-field historical preimage, and the current C1-02 composed identity is proved to
    be a DIFFERENT value in both directions.
    """
    spine = fx.frozen_spine()
    for direction in ("forward", "reverse"):
        recorded = spine[direction]["composed_result_identity_hash"]
        # (a) the historical value still reproduces from the pinned historical preimage
        assert historical_digest(direction) == recorded
        # (b) it is NOT the current C1-02 composed identity
        current = _provide(fx.build_provider_case(direction))
        assert current.composition_result.composed_result_identity_hash != recorded, (
            f"{direction}: the historical R8 identity must never be presented as the "
            "current C1-02 identity"
        )
    assert len(historical_canonical("forward")) == CONSERVED_HISTORICAL_FIELDS
    assert len(historical_canonical("reverse")) == CONSERVED_HISTORICAL_FIELDS




# ==========================================================================
# Successor requalification (AT17/N10E) -- PHASE 5
#
# Expected truth comes ONLY from the HQ-adopted successor oracle. Production is
# compared against it; it never defines it.
# ==========================================================================
def _canonical_production(direction):
    from rawlsing_next.pre553_empirical_objects import canonicalize

    case = fx.build_provider_case(direction)
    return case, _provide(case), canonicalize(
        _provide(case).composition_result.identity_material()
    )


def test_s1_historical_r8_forward_identity_preserved_as_historical():
    """1: historical R8 forward identity remains historical truth."""
    assert historical_digest("forward") == HISTORICAL_R8["forward"]
    assert len(historical_canonical("forward")) == CONSERVED_HISTORICAL_FIELDS
    assert historical_digest("forward") != ADOPTED_SUCCESSOR["forward"]


def test_s2_historical_r8_reverse_identity_preserved_as_historical():
    """2: historical R8 reverse identity remains historical truth."""
    assert historical_digest("reverse") == HISTORICAL_R8["reverse"]
    assert len(historical_canonical("reverse")) == CONSERVED_HISTORICAL_FIELDS
    assert historical_digest("reverse") != ADOPTED_SUCCESSOR["reverse"]


def test_s3_current_forward_complete_preimage_equals_adopted_successor():
    """3: the whole 44-field production preimage equals the adopted successor."""
    _, _, prod = _canonical_production("forward")
    expected = successor_canonical("forward")
    assert set(prod) == set(expected)
    assert len(prod) == 44
    mismatched = [k for k in prod if prod[k] != expected[k]]
    assert mismatched == [], f"forward preimage drift: {mismatched}"


def test_s4_current_reverse_complete_preimage_equals_adopted_successor():
    """4: the whole 44-field reverse production preimage equals the successor."""
    _, _, prod = _canonical_production("reverse")
    expected = successor_canonical("reverse")
    assert set(prod) == set(expected)
    assert len(prod) == 44
    mismatched = [k for k in prod if prod[k] != expected[k]]
    assert mismatched == [], f"reverse preimage drift: {mismatched}"


def test_s5_current_forward_digest_equals_adopted_successor():
    """5: forward composed identity equals the adopted successor identity."""
    _, result, _ = _canonical_production("forward")
    assert result.composition_result.composed_result_identity_hash == (
        ADOPTED_SUCCESSOR["forward"]
    )


def test_s6_current_reverse_digest_equals_adopted_successor():
    """6: reverse composed identity equals the adopted successor identity."""
    _, result, _ = _canonical_production("reverse")
    assert result.composition_result.composed_result_identity_hash == (
        ADOPTED_SUCCESSOR["reverse"]
    )


def test_s7_wrong_successor_direction_fails():
    """7: neither direction may satisfy the other's successor identity."""
    _, fwd, _ = _canonical_production("forward")
    _, rev, _ = _canonical_production("reverse")
    assert fwd.composition_result.composed_result_identity_hash != (
        ADOPTED_SUCCESSOR["reverse"]
    )
    assert rev.composition_result.composed_result_identity_hash != (
        ADOPTED_SUCCESSOR["forward"]
    )
    assert ADOPTED_SUCCESSOR["forward"] != ADOPTED_SUCCESSOR["reverse"]


def test_s8_one_six_field_omission_fails():
    """8: omitting any single successor field breaks the digest."""
    base = successor_canonical("forward")
    good = digest(base)
    for field in SUCCESSOR_SIX:
        mutated = {k: v for k, v in base.items() if k != field}
        assert digest(mutated) != good, f"omitting {field} must change the identity"
    assert good == ADOPTED_SUCCESSOR["forward"]


def test_s9_one_six_field_wrong_value_fails():
    """9: any single wrong successor value breaks the digest."""
    base = successor_canonical("forward")
    good = digest(base)
    wrong = {
        "discovery_receipt_refs": [{"kind": "X", "object_id": "y", "content_hash": "z" * 64}],
        "discovery_frontier_ref": {"kind": "X", "object_id": "y", "content_hash": "z" * 64},
        "recursive_handoff_refs": [{"kind": "X", "object_id": "y", "content_hash": "z" * 64}],
        "recursive_lineage_refs": [{"kind": "X", "object_id": "y", "content_hash": "z" * 64}],
        "joint_component_count": 2,
        "joint_order_semantics": "INPUT_ORDERED",
    }
    for field, value in wrong.items():
        mutated = dict(base)
        mutated[field] = value
        assert digest(mutated) != good, f"wrong {field} must change the identity"


def test_s10_old_r8_digest_cannot_masquerade_as_current_c1_02_digest():
    """10: the historical R8 digest is not accepted as the current identity."""
    for direction in ("forward", "reverse"):
        assert HISTORICAL_R8[direction] != ADOPTED_SUCCESSOR[direction]
        _, result, _ = _canonical_production(direction)
        assert result.composition_result.composed_result_identity_hash != (
            HISTORICAL_R8[direction]
        )
    # Both historical values still reproduce exactly as historical.
    assert historical_digest("forward") == HISTORICAL_R8["forward"]
    assert historical_digest("reverse") == HISTORICAL_R8["reverse"]


def test_s11_production_six_successor_values_are_the_direct_path_law():
    """The six current direct-path values are exactly the adopted direct-path law."""
    for direction in ("forward", "reverse"):
        _, _, prod = _canonical_production(direction)
        for field, value in SUCCESSOR_SIX.items():
            assert prod[field] == value, f"{direction}.{field}"
        # And no discovery/recursive/joint material leaked into the direct path.
        assert prod["discovery_receipt_refs"] == []
        assert prod["recursive_handoff_refs"] == []
        assert prod["joint_component_count"] == 1


def test_s12_both_directions_reach_the_named_consumer_and_refuse_geometry():
    """Phase 4 chain + anti-handwritten geometry law survive requalification."""
    import inspect

    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )

    for direction, denominator, cells in (
        ("forward", 60, {"yes": 54, "no": 6}),
        ("reverse", 62, {"P1": 54, "P2": 8}),
    ):
        _, result, _ = _canonical_production(direction)
        assert result.generated_evidence_or_null is not None
        consumer = result.composition_result.consumer_result_or_null
        assert consumer is not None
        assert consumer.result_state == "EXACT_SUPPORTED"
        assert result.composition_result.raw_denominator_support == denominator
        params = set(inspect.signature(provide_empirical_possibility_slice).parameters)
        for forbidden in ("geometry", "slice_geometry", "precomputed_geometry",
                          "probability_geometry"):
            assert forbidden not in params
