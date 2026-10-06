"""HQ221 N10E provider -> consumer -> dependency/lifecycle/replay closure court.

This is the *bounded* integration court for the remaining named C1 residual. It does
not build a provider and does not invent a semantic owner. It proves that one accepted
owner path carries:

    EXACT DETERMINANTS
      -> provide_empirical_possibility_slice          (N10E provider seam)
      -> compose_positioned_subject_possibility       (accepted analytical producer)
      -> producer-derived PossibilitySliceEvidence
      -> evaluate_positioned_subject_possibility      (named positioned-subject consumer)
      -> provider receipt
      -> AnalyticalProductRegistration / determinant graph  (dependency registration)
      -> transition_analytical_dependencies           (accepted lifecycle owner)
      -> resolve_current_analytical_product           (lifecycle currentness)
      -> fresh-process recomputation at the claimed replay grade

and that the chain is hostile to answer smuggling.

Proof grades are kept separate and explicit. This court proves:

  * ``SOURCE_FREE_EXECUTED_ACCEPTED_OWNERS`` -- the accepted owner chain executed here;
  * ``FRESH_PROCESS_PROVIDER_RECOMPUTATION`` -- the same chain recomputed in a genuinely
    fresh interpreter from retained determinants only, with the oracle held by the
    parent court and never written into the runner's input;
  * ``ACCEPTED_LIFECYCLE_OWNER_DEPENDENCY_TRANSITION`` -- the accepted
    ``AuthorityMaintenanceExecutor`` computed the affected/unaffected set and issued
    the invalidation receipt; the adapter never did.

This court deliberately does NOT claim live survey-source occupancy. It is
source-free: a synthetic AT07 empirical law plus frozen synthetic C1-00 authority
snapshots, exactly as the accepted C1-00/C1-01/C1-03R courts do.

Owner discipline: no production module is mutated by this court. Where the accepted
owners could not represent a required step, the correct outcome would be a named
contract gap, not an edit. None was required.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import replace
from typing import Any

import pytest

import rawlsing_next.pre553_analytical_composition as composition_module
import rawlsing_next.pre553_empirical_possibility_provider as provider_module
from rawlsing_next.pre553_analytical_composition import (
    ConditionValueRelationMismatch,
    ConditionValueBindingWitness,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_analytical_replay_dependency import (
    MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER,
    MECHANISM_STORED_RECEIPT_DESERIALIZATION,
    REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    REPLAY_GRADE_SERIALIZATION_REPLAY,
    AnalyticalDependencyRegistry,
    AnalyticalProductRegistration,
    AnalyticalReplayClaim,
    ExplicitNoncurrentDependent,
    MissingCrossOwnerEdge,
    OwnerUnknownDependent,
    ReplayGradeOverclaim,
    RunnerInputCarriesAnswer,
    assert_closure_covers_registered_products,
    assert_replay_claim,
    assert_runner_input_carries_no_answer,
    build_owner_recompiler,
    resolve_current_analytical_product,
    transition_analytical_dependencies,
)
from rawlsing_next.pre553_authority_maintenance import (
    DEPENDENT_LIFECYCLE_CURRENT,
    DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
    AuthorityMaintenanceExecutor,
    AuthorityMaintenanceError,
    NoncurrentDependentOutcome,
    NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import (
    EmpiricalPossibilityProviderRequest,
    EmpiricalPossibilitySliceProviderResult,
    FORBIDDEN_AUTHORITATIVE_INPUT_NAMES,
    ProviderRequestShapeError,
    provide_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
)
from rawlsing_next.tests import c1_at18_at19_fixture as fx

DIRECTION = "forward"
PRODUCT_KIND = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PRODUCT@1"


def _product_object_id(direction: str = DIRECTION) -> str:
    return f"urn:test:hq221:n10e:provider-product:{direction}"

PROVIDER_PATH = (
    "rawlsing_next.pre553_empirical_possibility_provider."
    "provide_empirical_possibility_slice"
)
PRODUCER_PATH = (
    "rawlsing_next.pre553_analytical_composition."
    "compose_positioned_subject_possibility"
)
CONSUMER_PATH = (
    "rawlsing_next.source_backed_positioned_subject_possibility."
    "evaluate_positioned_subject_possibility"
)
RUNNER_MODULE = (
    "rawlsing_next.tests.n10e_provider_replay_lifecycle_runner"
)

#: Substrings that must never appear anywhere in the fresh-runner input artifact.
FORBIDDEN_INPUT_SUBSTRINGS = (
    "expected",
    "probabilit",
    "geometry",
    "numerator",
    "denominator",
    "support",
    "cell_",
    "oracle",
    "answer",
    "evidence_ref",
    "fact_ref",
    "composed_result",
    "consumer_result_hash",
)


# ==========================================================================
# helpers
# ==========================================================================
def _case(direction: str = DIRECTION) -> dict[str, Any]:
    return fx.build_case(direction)


def _provide(case: dict[str, Any], **overrides: Any) -> Any:
    kwargs: dict[str, Any] = {
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


def _product_ref(
    product_identity_hash: str, direction: str = DIRECTION
) -> ExactRef:
    return ExactRef(PRODUCT_KIND, _product_object_id(direction), product_identity_hash)


def _register(case: dict[str, Any], result: Any) -> tuple[
    AnalyticalDependencyRegistry, ExactRef
]:
    """Register the provider product with exactly the determinants it consumed."""

    registry = AnalyticalDependencyRegistry()
    product_ref = _product_ref(result.result_identity_hash, case["direction"])
    registry.register(
        AnalyticalProductRegistration(
            product_ref=product_ref,
            product_identity_hash=result.result_identity_hash,
            determinant_authority_refs=(case["model_rule"].model_authority_ref,),
            determinant_exact_refs=(
                case["empirical_query"].ref,
                case["predicate"].ref,
                case["consumer_query"].ref,
                case["condition_binding_witness"].witness_ref,
            ),
        )
    )
    return registry, product_ref


def _recomposer(case: dict[str, Any]):
    """A real recomposition path: re-runs the accepted PROVIDER under a new authority."""

    base_rule = case["model_rule"]

    def recompose(affected_ref: ExactRef, authority: Any) -> ExactRef:
        rule = PositionedSubjectPossibilityModelRule(
            authority,
            base_rule.walkback_authority_ref,
            base_rule.source_universe_refs,
            base_rule.walkback_steps,
            base_rule.positive_proxy_authority_refs,
        )
        recomposed = _provide(case, model_rule=rule)
        assert recomposed.provider_state == "EXACT_SUPPORTED_SLICE_PRODUCED"
        return ExactRef(
            affected_ref.kind, affected_ref.object_id, recomposed.result_identity_hash
        )

    return recompose


def _stage_transition(
    case: dict[str, Any],
    product_ref: ExactRef,
    old_model: Any,
    registry: AnalyticalDependencyRegistry | None = None,
) -> dict[str, Any]:
    """Stage one governed model-authority revision around the provider product.

    The determinant graph binds ONLY the authorities the registered products actually
    consumed, and the successor is minted and adjudicated through the accepted owner's
    own candidate -> APPROVED -> seal ceremony. The unsealed decoy authority is
    retained for the hostile suite and must never be used as a successor.
    """

    direction = case["direction"]
    if registry is None:
        registry, _ = _register(case, _provide(case))
    graph = registry.build_graph()
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(fx.model_authority_snapshot(direction),),
        initial_current_selection={old_model.authority_id: old_model},
        determinant_graph=graph,
    )
    evidence = _evidence_receipt(direction)
    executor.intake_evidence(evidence)
    revision = fx._model_candidate(
        fx.revised_model_authority(direction),
        version="2.0.0",
        evidence_ref=evidence.ref,
        parent=(old_model,),
        supersession=(old_model,),
        semantics=f"{direction}-hq221-v2",
    )
    executor.intake_candidate(revision)
    adjudication = executor.adjudicate_candidate(
        revision.ref,
        decision="APPROVED",
        adjudicator_ref=fx._ref_for("ADJUDICATOR", f"hq221-{direction}-v2"),
        adjudication_authority_ref=fx._ref_for("GOVERNING_AUTHORITY", "HQ221"),
        findings_ref=fx._ref_for("FINDINGS", f"hq221-{direction}-v2"),
    )
    seal = executor.seal_revision(
        revision.ref,
        adjudication.ref,
        seal_attestation_ref=fx._ref_for("SEAL_ATTESTATION", f"hq221-{direction}-v2"),
    )
    successor = revision.proposed_authority_ref
    # The governed successor must be a genuinely different authority.
    assert successor.authority_content_hash != old_model.authority_content_hash
    return {
        "executor": executor,
        "seal_ref": seal.ref,
        "successor": successor,
        "decoy": fx.revised_model_authority(direction),
        "selection_rule_ref": fx._ref_for("SELECTION_RULE", f"hq221-{direction}-v2"),
        "selection_attestation_ref": fx._ref_for(
            "SELECTION_ATTESTATION", f"hq221-{direction}-v2"
        ),
    }


def _evidence_receipt(direction: str) -> Any:
    from rawlsing_next.pre553_authority_maintenance import AuthorityEvidenceReceipt

    return AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(fx._ref_for("EVIDENCE", f"hq221-{direction}-model"),),
        provenance_refs=(fx._ref_for("PROVENANCE", f"hq221-{direction}-model"),),
        source_release_refs=(),
    )


def _transition(
    case: dict[str, Any],
    registry: AnalyticalDependencyRegistry,
    staged: dict[str, Any],
    recompose: dict[str, ExactRef],
    **kwargs: Any,
) -> Any:
    return transition_analytical_dependencies(
        executor=staged["executor"],
        registry=registry,
        seal_ref=staged["seal_ref"],
        selection_rule_ref=staged["selection_rule_ref"],
        selection_attestation_ref=staged["selection_attestation_ref"],
        recompose=recompose,
        **kwargs,
    )


def _runner_input(tmp_path: Any, case: dict[str, Any] | None = None) -> Any:
    """Write the retained-determinant INPUT artifact (never an answer)."""

    case = case or _case()
    determinants = fx.retained_determinants(case)
    path = tmp_path / "hq221_retained_determinants_input.json"
    path.write_text(json.dumps(determinants, sort_keys=True), encoding="utf-8")
    return path


def _run_fresh(input_path: Any, *extra: str) -> dict[str, Any]:
    """Execute the runner in a genuinely fresh interpreter process."""

    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [sys.executable, "-m", RUNNER_MODULE, str(input_path), *extra],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode == 0, (
        f"fresh runner failed ({completed.returncode}): {completed.stderr}"
    )
    return json.loads(completed.stdout)


# ==========================================================================
# 1-2. the fresh-runner INPUT carries only exact determinants, no answer
# ==========================================================================
def test_01_runner_input_carries_only_exact_determinants():
    determinants = fx.retained_determinants(_case())

    assert_runner_input_carries_no_answer(determinants)

    allowed = {
        "schema",
        "direction",
        "empirical_query_ref",
        "predicate_ref",
        "predicate_hash",
        "condition_binding_witness_ref",
        "consumer_query_ref",
        "model_rule_hash",
        "release_refs",
        "source_universe_ref",
        "authority_snapshot_refs",
        "conditioner_binding_refs",
    }
    assert set(determinants) == allowed, sorted(set(determinants) ^ allowed)

    # Every leaf is an identity/hierarchy material, never a measured value.
    def leaves(node: Any):
        if isinstance(node, dict):
            for key, value in node.items():
                yield key
                yield from leaves(value)
        elif isinstance(node, list):
            for value in node:
                yield from leaves(value)

    for key in leaves(determinants):
        assert not any(bad in key for bad in FORBIDDEN_INPUT_SUBSTRINGS), key


def test_02_serialized_runner_input_contains_no_answer_field():
    serialized = json.dumps(fx.retained_determinants(_case()), sort_keys=True)
    for forbidden in (
        "expected_output_identity",
        "composed_result_identity_hash",
        "producer_fact_ref",
        "evidence_ref",
        "consumer_result_hash",
        "raw_denominator_support",
        "geometry",
        "exact_fraction",
        "cell_numerators",
        "probability",
        "probabilities",
        "oracle",
    ):
        assert forbidden not in serialized, forbidden


# ==========================================================================
# 3-6. the positive provider -> producer -> consumer path
# ==========================================================================
def test_03_provider_invokes_the_accepted_analytical_composition_path(monkeypatch):
    """The provider is a seam, not a second calculator.

    Exactly one composition call and exactly one named-consumer call occur inside a
    single provider invocation, and both are the *accepted* owners' functions.
    """

    calls: dict[str, int] = {"compose": 0, "consume": 0}
    original_compose = provider_module.compose_positioned_subject_possibility
    original_consume = composition_module.evaluate_positioned_subject_possibility

    def spy_compose(**kwargs):
        calls["compose"] += 1
        return original_compose(**kwargs)

    def spy_consume(**kwargs):
        calls["consume"] += 1
        return original_consume(**kwargs)

    monkeypatch.setattr(
        provider_module, "compose_positioned_subject_possibility", spy_compose
    )
    monkeypatch.setattr(
        composition_module, "evaluate_positioned_subject_possibility", spy_consume
    )

    case = _case()
    result = _provide(case)

    assert calls == {"compose": 1, "consume": 1}
    # The provider itself carries no geometry/probability computation of its own.
    assert result.provider_receipt.provider_route == (
        "EMPIRICAL_QUERY__C1_ANALYTICAL_COMPOSITION__GENERATED_EVIDENCE"
    )
    assert PROVIDER_PATH in provider_module.__doc__ or "provider seam" in (
        provider_module.__doc__ or ""
    )


def test_04_slice_evidence_identity_is_producer_derived_not_caller_supplied():
    """The evidence object IS the accepted producer's generated object."""

    case = _case()
    result = _provide(case)
    receipt = result.provider_receipt

    assert receipt.generated_evidence_identity_is_producer_derived is True
    # Object identity, not merely equal hashes: nothing was re-wrapped or injected.
    assert (
        result.generated_evidence_or_null
        is result.composition_result.possibility_slice_evidence_or_null
    )
    # The receipt's evidence ref is the generated evidence's own ref.
    assert receipt.generated_evidence_ref == (
        result.generated_evidence_or_null.evidence_ref
    )
    # The geometry is exact and recomputed from the empirical fact.
    assert result.composition_result.raw_denominator_support == 60
    numerators = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in result.generated_evidence_or_null.geometry["cells"]
    }
    assert numerators == {"yes": 54, "no": 6}


def test_05_named_positioned_subject_consumer_is_invoked_on_generated_evidence():
    case = _case()
    result = _provide(case)

    consumer = result.consumer_result_or_null
    assert consumer is not None
    assert consumer is result.composition_result.consumer_result_or_null
    assert consumer.result_state == "EXACT_SUPPORTED"
    # The consumer consumed the generated slice, and the receipt binds its identity.
    assert result.provider_receipt.consumer_result_state == consumer.result_state
    assert result.provider_receipt.consumer_result_identity_hash == consumer.result_hash
    assert result.provider_receipt.consumer_query_ref == (
        result.composition_result.consumer_query_ref
    )
    # A fresh consumer pass over the same generated evidence reproduces the identity,
    # which is what proves the consumer really evaluated THIS slice.
    replay = provider_module.evaluate_generated_slice_directly(
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        generated_evidence=result.generated_evidence_or_null,
    )
    assert replay.result_hash == consumer.result_hash


def test_06_provider_receipt_binds_the_whole_exact_chain():
    """Producer query, predicate, releases, model rule, witness, evidence, consumer."""

    case = _case()
    result = _provide(case)
    receipt = result.provider_receipt
    composition = result.composition_result

    assert receipt.producer_query_ref == composition.producer_query_ref
    assert receipt.producer_predicate_ref == composition.producer_predicate_ref
    assert receipt.producer_fact_ref == composition.producer_fact_ref
    assert receipt.producer_fact_state == "SUPPORTED"
    assert receipt.release_refs == tuple(case["release_refs"])
    assert receipt.model_rule_hash == case["model_rule"].rule_hash
    assert receipt.condition_binding_witness_ref == (
        case["condition_binding_witness"].witness_ref
    )
    assert receipt.generated_evidence_ref == (
        result.generated_evidence_or_null.evidence_ref
    )
    assert receipt.consumer_result_identity_hash == (
        result.consumer_result_or_null.result_hash
    )
    assert receipt.composed_result_identity_hash == (
        composition.composed_result_identity_hash
    )
    assert receipt.refusal_state is None
    # The request identity bindings are all present and exact.
    request = EmpiricalPossibilityProviderRequest(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    bindings = request.identity_bindings()
    assert bindings["model_rule_hash"] == case["model_rule"].rule_hash
    assert bindings["empirical_query_ref"] == case["empirical_query"].ref.as_dict()
    assert bindings["predicate_hash"] == case["predicate"].predicate_hash
    assert bindings["release_refs"] == [
        x.as_dict() for x in case["release_refs"]
    ]
    assert bindings["condition_binding_witness_ref"] == (
        case["condition_binding_witness"].witness_ref.as_dict()
    )


# ==========================================================================
# 7-8. dependency registration and fresh-process replay at the claimed grade
# ==========================================================================
def test_07_exact_product_and_determinants_register_through_current_machinery():
    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)

    (registration,) = registry.registrations
    assert registration.product_ref == product_ref
    assert registration.product_identity_hash == result.result_identity_hash
    # Only determinants the product ACTUALLY consumed are registered.
    assert registration.determinant_authority_refs == (
        case["model_rule"].model_authority_ref,
    )
    assert set(registration.determinant_exact_refs) == {
        case["empirical_query"].ref,
        case["predicate"].ref,
        case["consumer_query"].ref,
        case["condition_binding_witness"].witness_ref,
    }
    # The graph reaches the product through exactly those determinant edges.
    graph = registry.build_graph()
    assert graph.affected(
        (case["model_rule"].model_authority_ref,)
    ) == (product_ref,)
    assert product_ref in graph.unaffected(())


def test_08_fresh_process_recomputes_provider_consumer_and_lifecycle(tmp_path):
    """The whole chain, recomputed in a fresh interpreter from determinants only."""

    input_path = _runner_input(tmp_path)
    observed = _run_fresh(input_path)

    # The fresh process genuinely recomputed on the positive path.
    assert observed["provider_state"] == "EXACT_SUPPORTED_SLICE_PRODUCED"
    assert observed["evidence_identity_is_producer_derived"] is True
    assert observed["consumer_result_state_or_null"] == "EXACT_SUPPORTED"
    assert observed["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT

    # It did not read an answer: it reproduced the exact empirical support itself.
    assert observed["raw_denominator_support"] == 60
    assert observed["cell_numerators"] == {"yes": 54, "no": 6}

    # The oracle side agrees, identity for identity.
    case = _case()
    result = _provide(case)
    assert observed["product_identity_hash"] == result.result_identity_hash
    assert observed["receipt_ref_hash"] == result.provider_receipt.receipt_hash
    assert observed["composed_result_identity_hash"] == (
        result.composition_result.composed_result_identity_hash
    )
    assert observed["evidence_ref_or_null"] == (
        result.generated_evidence_or_null.evidence_ref.as_dict()
    )
    assert observed["consumer_result_hash_or_null"] == (
        result.consumer_result_or_null.result_hash
    )

    # The declared public paths are the accepted owners'.
    assert observed["producer_path"] == PROVIDER_PATH
    assert observed["consumer_path"] == CONSUMER_PATH

    # The fresh process registered the product and drove the lifecycle owner.
    assert len(observed["graph_affected"]) == 1
    assert observed["graph_affected"][0]["object_id"] == _product_object_id()
    assert observed["current_replacement_ref_or_null"] is not None
    assert observed["current_replacement_ref_or_null"] != observed["product_ref"]


def test_08b_fresh_process_claim_is_bounded_at_the_fresh_recomputation_grade(
    tmp_path,
):
    """AT18: the replay claim names its grade, and the grade is honest."""

    case = _case()
    result = _provide(case)
    composition = result.composition_result
    product_ref = _product_ref(result.result_identity_hash)
    observed = _run_fresh(_runner_input(tmp_path))

    claim = AnalyticalReplayClaim(
        claim_id="hq221-n10e-provider-replay-lifecycle-forward",
        replayed_product_ref=product_ref,
        retained_determinant_refs=(
            case["empirical_query"].ref,
            case["predicate"].ref,
            case["consumer_query"].ref,
            case["condition_binding_witness"].witness_ref,
        ),
        producer_route=result.provider_receipt.provider_route,
        producer_path=PROVIDER_PATH,
        authority_refs=tuple(composition.authority_refs),
        expected_output_identity_hash=result.result_identity_hash,
        actual_replay_mechanism=MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER,
        replay_grade=REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
        limitations=(
            "source-free synthetic fixture; proves provider/consumer/lifecycle "
            "closure only, not live survey-source occupancy",
        ),
        replay_protocol_ref=fx.replay_protocol_ref(case),
        deterministic_order_or_tie_rule_refs=(fx.deterministic_order_ref(case),),
    )
    assertion = assert_replay_claim(
        claim, observed_output_identity_hash=observed["product_identity_hash"]
    )
    assert assertion.identity_reproduced is True
    assert assertion.asserted_grade_is_honest is True
    assert assertion.replay_grade == REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION

    receipt = claim.to_replay_receipt()
    assert receipt.semantic_fields["replay_grade"] == (
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION
    )
    assert receipt.semantic_fields["actual_replay_mechanism"] == (
        MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER
    )
    # The claim binds the exact consumed determinants and nothing else.
    assert set(claim.retained_determinant_refs) == {
        case["empirical_query"].ref,
        case["predicate"].ref,
        case["consumer_query"].ref,
        case["condition_binding_witness"].witness_ref,
    }


def test_08c_fresh_process_determinant_mismatch_fails_closed(tmp_path):
    """The fresh runner rebuilds determinants and fails if a retained ref is wrong."""

    determinants = fx.retained_determinants(_case())
    determinants["predicate_hash"] = "0" * 64
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(determinants), encoding="utf-8")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [sys.executable, "-m", RUNNER_MODULE, str(path)],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode != 0
    assert "did not rebuild exactly" in completed.stderr


# ==========================================================================
# 9. lifecycle distinguishes current / explicitly noncurrent / unknown dependent
# ==========================================================================
def test_09_lifecycle_distinguishes_current_noncurrent_and_unknown():
    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    old_model = case["model_rule"].model_authority_ref
    staged = _stage_transition(case, product_ref, old_model)

    # (a) CURRENT: replaced by a real recomposition under the successor authority.
    recompose = _recomposer(case)
    outcome = _transition(
        case, registry, staged, {product_ref.key: recompose}
    )
    status = resolve_current_analytical_product(
        executor=staged["executor"], dependent_ref=product_ref
    )
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    (old, new), = outcome.invalidation_receipt.recompilation_pairs
    assert old.key == product_ref.key
    assert status["current_replacement_ref"] == new

    # (b) EXPLICITLY NONCURRENT: same governed transition, but the domain declares
    #     there is no lawful replacement, with grounds.
    other = _case()
    other_result = _provide(other)
    other_registry, other_ref = _register(other, other_result)
    other_staged = _stage_transition(
        other, other_ref, other["model_rule"].model_authority_ref
    )
    policy_ref = fx._ref_for("REPLACEMENT_POLICY", "hq221-no-source")
    row = NoncurrentDependentOutcome(
        old_ref=other_ref,
        disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
        reason_code="NO_LAWFUL_REPLACEMENT_SOURCE",
        supporting_refs=(policy_ref,),
    )
    noncurrent_outcome = _transition(
        other,
        other_registry,
        other_staged,
        {},
        noncurrent_dependents={other_ref.key: row},
    )
    assert noncurrent_outcome.invalidation_receipt.noncurrent_old_refs == (
        other_ref,
    )
    # The owner recorded the EXPLICITLY NONCURRENT state for that dependent.
    recorded = dict(
        other_staged["executor"].dependent_lifecycle_status(other_ref)
    )
    assert recorded["lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT
    assert recorded["disposition"] == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
    assert recorded["reason_code"] == "NO_LAWFUL_REPLACEMENT_SOURCE"
    with pytest.raises(
        ExplicitNoncurrentDependent, match="may not be served as current"
    ):
        resolve_current_analytical_product(
            executor=other_staged["executor"], dependent_ref=other_ref
        )
    # The historical exact artifact remains addressable even though it is noncurrent.
    assert other_staged["executor"].resolve_historical_exact(
        other_staged["successor"]
    ).authority_ref == other_staged["successor"]

    # (c) UNKNOWN DEPENDENT: a ref the owner never spoke about is not current.
    stranger = ExactRef("N10E_UNKNOWN", "urn:test:hq221:never-registered", "3" * 64)
    with pytest.raises(
        OwnerUnknownDependent, match="does not know this dependent"
    ):
        resolve_current_analytical_product(
            executor=other_staged["executor"], dependent_ref=stranger
        )


def test_09b_currentness_is_not_inferred_from_cache_or_object_presence():
    """A registered-but-never-transitioned product is not laundered into current."""

    case = _case()
    result = _provide(case)
    _, product_ref = _register(case, result)
    old_model = case["model_rule"].model_authority_ref
    staged = _stage_transition(case, product_ref, old_model)

    # The ref is fully known and the product object exists in memory, but no
    # governed transition has ever spoken about it.
    assert product_ref.key in {
        ref.key for ref in staged["executor"].determinant_graph.known_dependent_refs
    }
    status = dict(staged["executor"].dependent_lifecycle_status(product_ref))
    assert status["lifecycle_state"] != DEPENDENT_LIFECYCLE_CURRENT
    with pytest.raises(OwnerUnknownDependent):
        resolve_current_analytical_product(
            executor=staged["executor"], dependent_ref=product_ref
        )


# ==========================================================================
# 10-11. invalidation reaches the exact dependent; identity cannot be replayed stale
# ==========================================================================
def test_10_invalidating_a_consumed_determinant_reaches_the_exact_product():
    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    old_model = case["model_rule"].model_authority_ref
    staged = _stage_transition(case, product_ref, old_model)
    recompose = _recomposer(case)

    outcome = _transition(case, registry, staged, {product_ref.key: recompose})
    receipt = outcome.invalidation_receipt

    # Exactly the dependent whose consumed determinant changed was reached.
    assert receipt.affected_dependent_refs == (product_ref,)
    assert receipt.unaffected_dependent_refs == ()
    # The receipt was built by the accepted owner, not by the adapter.
    assert outcome.material()["lifecycle_performed_by"] == (
        "AuthorityMaintenanceExecutor.promote_current"
    )
    # The successor is the owner's sealed revision, never the unsealed decoy.
    assert staged["successor"].key != staged["decoy"].key
    # Closure holds over the owner's own affected set.
    assert_closure_covers_registered_products(
        outcome=outcome,
        registry=registry,
        recompose={product_ref.key: recompose},
        successor_authority=staged["successor"],
    )


def test_11_changed_determinant_cannot_replay_to_the_old_product_identity():
    """A revision must move the product; a stale identity is refused by the owner."""

    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    old_model = case["model_rule"].model_authority_ref
    staged = _stage_transition(case, product_ref, old_model)

    # The successor authority genuinely re-identifies the provider product.
    successor_rule = PositionedSubjectPossibilityModelRule(
        staged["successor"],
        case["model_rule"].walkback_authority_ref,
        case["model_rule"].source_universe_refs,
        case["model_rule"].walkback_steps,
        case["model_rule"].positive_proxy_authority_refs,
    )
    recomposed = _provide(case, model_rule=successor_rule)
    assert recomposed.result_identity_hash != result.result_identity_hash
    # The consumer result identity moves too: the model rule is a determinant the
    # named consumer actually consumes, so a changed authority must re-identify it.
    assert recomposed.consumer_result_or_null.result_hash != (
        result.consumer_result_or_null.result_hash
    )
    # The empirical substance itself is untouched by an authority revision: the same
    # exact conditional law is measured and consumed, under a different governed
    # authority. This is an identity movement, not a probability change.
    assert recomposed.composition_result.raw_denominator_support == 60
    assert {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in recomposed.generated_evidence_or_null.geometry["cells"]
    } == {"yes": 54, "no": 6}
    assert recomposed.consumer_result_or_null.result_state == "EXACT_SUPPORTED"

    # A "recompiler" that tries to hand back the OLD identity is refused by the owner.
    with pytest.raises(
        AuthorityMaintenanceError, match="must produce a new exact ref"
    ):
        _transition(
            case,
            registry,
            staged,
            {product_ref.key: lambda old_ref, authority: old_ref},
        )

    # And the honest path does move it, with the owner recording the pair.
    outcome = _transition(
        case, registry, staged, {product_ref.key: _recomposer(case)}
    )
    (old, new), = outcome.invalidation_receipt.recompilation_pairs
    assert old.content_hash == result.result_identity_hash
    assert new.content_hash == recomposed.result_identity_hash


def test_11b_unaffected_product_is_reached_by_neither_revision():
    """Selective invalidation reaches all AND ONLY the affected dependents."""

    affected_case = _case(DIRECTION)
    affected_result = _provide(affected_case)
    affected_registry, affected_ref = _register(affected_case, affected_result)

    sibling_case = _case("reverse")
    sibling_result = _provide(sibling_case)
    sibling_ref = _product_ref(sibling_result.result_identity_hash, "reverse")
    sibling_registry = AnalyticalDependencyRegistry()
    sibling_registry.register(
        AnalyticalProductRegistration(
            product_ref=sibling_ref,
            product_identity_hash=sibling_result.result_identity_hash,
            determinant_authority_refs=(
                sibling_case["model_rule"].model_authority_ref,
            ),
            determinant_exact_refs=(
                sibling_case["empirical_query"].ref,
                sibling_case["predicate"].ref,
                sibling_case["consumer_query"].ref,
                sibling_case["condition_binding_witness"].witness_ref,
            ),
        )
    )
    # Two genuinely distinct model authorities, so the graph can discriminate.
    assert (
        affected_case["model_rule"].model_authority_ref.key
        != sibling_case["model_rule"].model_authority_ref.key
    )
    registry = AnalyticalDependencyRegistry()
    for registration in (
        *affected_registry.registrations,
        *sibling_registry.registrations,
    ):
        registry.register(registration)

    staged = _stage_transition(
        affected_case,
        affected_ref,
        affected_case["model_rule"].model_authority_ref,
        registry=registry,
    )
    graph = registry.build_graph()
    changed = (
        affected_case["model_rule"].model_authority_ref,
        staged["successor"],
    )
    reached = graph.affected(changed)
    assert reached == (affected_ref,)
    assert sibling_ref in graph.unaffected(reached)

    outcome = _transition(
        affected_case,
        registry,
        staged,
        {affected_ref.key: _recomposer(affected_case)},
    )
    assert outcome.invalidation_receipt.unaffected_dependent_refs == (sibling_ref,)
    assert sibling_ref not in {
        old.key for old, _ in outcome.invalidation_receipt.recompilation_pairs
    }
    # The sibling stays current and identity-stable through its own determinants.
    status = resolve_current_analytical_product(
        executor=staged["executor"], dependent_ref=sibling_ref
    )
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert "current_replacement_ref" not in status


# ==========================================================================
# 12. fresh recomputation proves execution, not receipt deserialization
# ==========================================================================
def test_12_fresh_runner_computes_rather_than_deserializing_a_stored_receipt(
    tmp_path,
):
    """The runner's own source proves it recomputes, and it detects a stale answer.

    Two independent checks:

    1. Static: the runner module names no stored receipt/product and reads no expected
       identity; it calls the provider seam and asserts a positive provider state.
    2. Behavioural: presented with an oracle that contradicts a genuine
       recomputation, the fresh runner exits non-zero rather than echoing the oracle.
    """

    import inspect

    from rawlsing_next.tests import n10e_provider_replay_lifecycle_runner as runner

    source = inspect.getsource(runner)
    assert "provide_empirical_possibility_slice(" in source
    assert "assert_runner_input_carries_no_answer" in source
    # No stored receipt/product deserialization anywhere in the runner: the only
    # place a provider receipt is named is where the runner *computes* one.
    for forbidden in (
        "EmpiricalPossibilitySliceProviderReceipt(",
        "AnalyticalReplayClaim(",
        "pickle",
        "marshal",
        "shelve",
        "np.load",
        "jsonpickle",
    ):
        assert forbidden not in source, forbidden
    # Every provider receipt the runner names is one it just produced locally: the
    # only `provide(...)` calls are the two positive recompositions, and both bind
    # receipts from their own return values.
    assert source.count("= provide(case,") == 2
    assert "produced.provider_receipt" in source
    assert "recomposed.provider_receipt" not in source
    # It never reads the oracle before computing, only after.
    run_index = source.index("payload = run(determinants)")
    oracle_index = source.index('if "--expect" in argv:')
    assert run_index < oracle_index, "the oracle must be consulted only after computing"

    # Behavioural: a contradicting oracle is detected, not echoed.
    input_path = _runner_input(tmp_path)
    oracle = {
        "product_identity_hash": "0" * 64,
        "consumer_result_hash_or_null": "0" * 64,
    }
    oracle_path = tmp_path / "contradicting_oracle.json"
    oracle_path.write_text(json.dumps(oracle), encoding="utf-8")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            RUNNER_MODULE,
            str(input_path),
            "--expect",
            str(oracle_path),
        ],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode == 3
    assert "disagreed with the oracle" in completed.stderr
    # The stale identity was NOT echoed as a result.
    assert "0" * 64 not in completed.stdout

    # Control: a matching oracle is accepted, proving the check is discriminating.
    good = {"provider_state": "EXACT_SUPPORTED_SLICE_PRODUCED"}
    good_path = tmp_path / "agreeing_oracle.json"
    good_path.write_text(json.dumps(good), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            RUNNER_MODULE,
            str(input_path),
            "--expect",
            str(good_path),
        ],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["oracle_agreement"] is True


# ==========================================================================
# MANDATORY HOSTILE SUITE
# ==========================================================================
def test_h01_handwritten_precomputed_slice_geometry_is_refused():
    """Hostile: handwritten geometry supplied to the provider.

    The provider public API has no channel for it, and a caller-supplied evidence
    object cannot be claimed as the provider's generated evidence.
    """

    import inspect

    params = set(inspect.signature(provider_module.provide_empirical_possibility_slice).parameters)
    assert not params & FORBIDDEN_AUTHORITATIVE_INPUT_NAMES
    assert not params & {
        "evidence",
        "possibility_slice_evidence",
        "geometry",
        "probability",
        "probabilities",
    }
    # The guard is live, not decorative.
    provider_module.assert_provider_public_api_excludes_handwritten_slice()

    # Constructing a result that claims a substituted evidence object fails closed.
    case = _case()
    result = _provide(case)
    with pytest.raises(
        ProviderRequestShapeError, match="composition_result is required"
    ):
        EmpiricalPossibilitySliceProviderResult(
            provider_state="EXACT_SUPPORTED_SLICE_PRODUCED",
            provider_receipt=result.provider_receipt,
            composition_result=None,
            generated_evidence_or_null=None,
            consumer_result_or_null=None,
        )
    # And a typed refusal may never carry evidence at all.
    assert result.generated_evidence_or_null is not None


def test_h02_answer_fields_embedded_in_runner_input_are_rejected(tmp_path):
    """Hostile: every forbidden answer field, at top level and nested."""

    clean = fx.retained_determinants(_case())
    assert_runner_input_carries_no_answer(clean)

    from rawlsing_next.pre553_analytical_replay_dependency import (
        FORBIDDEN_RUNNER_INPUT_FIELDS,
    )

    for field in sorted(FORBIDDEN_RUNNER_INPUT_FIELDS):
        poisoned = dict(clean)
        poisoned[field] = {"anything": "answer-bearing"}
        with pytest.raises(
            RunnerInputCarriesAnswer, match="RUNNER_INPUT_CARRIES_ANSWER"
        ):
            assert_runner_input_carries_no_answer(poisoned)

    nested = dict(clean)
    nested["scope"] = {"deeper": [{"cell_numerators": {"yes": 54}}]}
    with pytest.raises(RunnerInputCarriesAnswer):
        assert_runner_input_carries_no_answer(nested)

    # And the fresh runner refuses such an artifact outright.
    poisoned = dict(clean)
    poisoned["expected_output_identity"] = {"composed_result_identity_hash": "0" * 64}
    path = tmp_path / "poisoned.json"
    path.write_text(json.dumps(poisoned), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [sys.executable, "-m", RUNNER_MODULE, str(path)],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode != 0
    assert "RUNNER_INPUT_CARRIES_ANSWER" in completed.stderr


def test_h03_stale_release_ref_fails_closed():
    """Hostile: a stale/forged release ref and an empty release set."""

    case = _case()
    stale = ExactRef("RELEASE", "urn:test:hq221:stale-release", "4" * 64)
    with pytest.raises(Exception) as excinfo:
        _provide(case, release_refs=(stale,))
    # The owner's own typed error propagates unchanged; the provider does not
    # launder or bridge it.
    assert type(excinfo.value).__name__ == "AnalyticalCompositionError"
    assert "SOURCE_RELEASE_MISMATCH" in str(excinfo.value)

    with pytest.raises(
        ProviderRequestShapeError, match="release_refs may not be empty"
    ):
        _provide(case, release_refs=())


def test_h04_changed_predicate_or_query_determinant_reidentifies_output():
    """Hostile: mutating a consumed determinant must move the product identity.

    Determinants are mutated through their *own* accepted constructors, so each one is
    a genuinely well-formed different determinant rather than a corrupted object.
    """

    case = _case()
    base = _provide(case)

    # (a) A different empirical QUERY: an explicit extra scope ref changes the query
    #     identity the provider receipt binds.
    query = case["empirical_query"]
    mutated_query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        target_refs=query.target_refs,
        target_arity_and_topology=query.target_arity_and_topology,
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=(*query.scope_refs, "HQ221_EXTRA_SCOPE"),
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=query.requested_output_grain,
        query_authority_refs=query.query_authority_refs,
    )
    assert mutated_query.ref != query.ref

    # (a1) The ORIGINAL custody witness refuses the changed query: the witness binds
    #      the exact producer query ref, so a changed query is caught, not recomputed.
    with pytest.raises(
        ConditionValueRelationMismatch,
        match="CONDITION_VALUE_RELATION_MISMATCH",
    ):
        _provide(case, empirical_query=mutated_query)

    # (a2) A witness lawfully rebuilt against the changed query moves the product.
    query_witness = fx.build_witness(
        case["source"],
        DIRECTION,
        case["consumer_query"],
        case["conditioner_binding"],
        mutated_query,
        case["predicate"],
    )
    query_witness.verify_identity()
    moved_query = _provide(
        case, empirical_query=mutated_query, condition_binding_witness=query_witness
    )
    assert moved_query.result_identity_hash != base.result_identity_hash
    assert moved_query.provider_receipt.producer_query_ref == mutated_query.ref
    assert moved_query.provider_receipt.condition_binding_witness_ref == (
        query_witness.witness_ref
    )

    # (b) A different conditioner binding determinant: an explicit effective-time
    #     change re-identifies the consumer query, the witness and the result.
    binding = case["conditioner_binding"]
    mutated_binding = ConditionerBinding(
        binding.binding_id,
        binding.subject_fact_ref,
        binding.empirical_coordinate_ref,
        binding.comparability_authority_ref,
        binding.source_universe_ref,
        binding.release_ref,
        "HQ221_HOSTILE_TIME_MUTATION",
    )
    consumer_query = case["consumer_query"]
    mutated_consumer_query = PositionedSubjectPossibilityQuery(
        consumer_query.query_id,
        consumer_query.subject_ref,
        consumer_query.target_ref,
        consumer_query.source_universe_ref,
        consumer_query.release_ref,
        (mutated_binding,),
        consumer_query.requested_projection,
        purpose=consumer_query.purpose,
    )
    mutated_witness = fx.build_witness(
        case["source"],
        DIRECTION,
        mutated_consumer_query,
        mutated_binding,
        case["empirical_query"],
        case["predicate"],
    )
    mutated_witness.verify_identity()
    moved_binding = _provide(
        case,
        consumer_query=mutated_consumer_query,
        condition_binding_witness=mutated_witness,
    )
    assert moved_binding.result_identity_hash != base.result_identity_hash
    assert moved_binding.provider_receipt.consumer_query_ref != (
        base.provider_receipt.consumer_query_ref
    )
    assert moved_binding.provider_receipt.condition_binding_witness_ref == (
        mutated_witness.witness_ref
    )
    # The empirical support is unchanged: a conditioner-time mutation is an identity
    # movement, not an invented measurement.
    assert moved_binding.generated_evidence_or_null.raw_support == 60


def test_h05_changed_model_authority_reidentifies_the_provider_product():
    """Hostile: a changed model authority must not replay to the old identity."""

    case = _case()
    base = _provide(case)
    mutated = replace(
        case["model_rule"],
        model_authority_ref=fx.revised_model_authority(DIRECTION),
    )
    moved = _provide(case, model_rule=mutated)
    assert moved.result_identity_hash != base.result_identity_hash
    assert moved.provider_receipt.model_rule_hash != base.provider_receipt.model_rule_hash


def test_h06_changed_conditioner_binding_witness_is_caught_by_custody():
    """Hostile: a tampered witness must fail the custody law, not be recomputed."""

    case = _case()
    witness = case["condition_binding_witness"]
    material = dict(witness.identity_material)
    material["hostile_extra_field"] = "smuggled"
    tampered = ConditionValueBindingWitness(
        witness_ref=ExactRef(
            witness.witness_ref.kind,
            witness.witness_ref.object_id,
            semantic_hash(material),
        ),
        identity_material=material,
        subject_condition_preimage_ref=witness.subject_condition_preimage_ref,
        subject_condition_preimage_material=(
            witness.subject_condition_preimage_material
        ),
        producer_predicate_leaf_ref=witness.producer_predicate_leaf_ref,
        producer_predicate_leaf_projection=(
            witness.producer_predicate_leaf_projection
        ),
        pairing_ground_truth_ref=witness.pairing_ground_truth_ref,
        pairing_ground_truth_material=witness.pairing_ground_truth_material,
        pairing_authority_ref=witness.pairing_authority_ref,
    )
    with pytest.raises(
        ConditionValueRelationMismatch, match="CONDITION_VALUE_RELATION_MISMATCH"
    ):
        _provide(case, condition_binding_witness=tampered)


def test_h07_missing_dependency_edge_fails_closure_even_with_object_presence():
    """Hostile: a product whose edge is missing is unreachable, and closure fails."""

    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    old_model = case["model_rule"].model_authority_ref
    staged = _stage_transition(case, product_ref, old_model)
    recompose = _recomposer(case)

    # The honest transition reaches it and closure holds.
    outcome = _transition(case, registry, staged, {product_ref.key: recompose})
    assert_closure_covers_registered_products(
        outcome=outcome,
        registry=registry,
        recompose={product_ref.key: recompose},
        successor_authority=staged["successor"],
    )

    # Now build the graph with the consumed determinant edge deliberately omitted.
    incomplete = registry.build_graph(
        omit_authority_edges=((old_model, product_ref),)
    )
    assert incomplete.affected((old_model, staged["successor"])) == ()
    # The product ref is still known/present, yet nothing reaches it.
    assert product_ref in incomplete.known_dependent_refs

    # A receipt claiming "nothing affected" is refused by the closure check.
    from rawlsing_next.pre553_authority_maintenance import AuthorityInvalidationReceipt
    from rawlsing_next.pre553_analytical_replay_dependency import (
        OwnerDependencyInvalidationOutcome,
    )

    fabricated = AuthorityInvalidationReceipt(
        changed_authority_refs=(old_model,),
        affected_dependent_refs=(),
        unaffected_dependent_refs=(product_ref,),
        recompilation_pairs=(),
    )
    fabricated_outcome = OwnerDependencyInvalidationOutcome(
        release_ref=ExactRef("RELEASE", "urn:test:hq221:incomplete", "5" * 64),
        invalidation_receipt=fabricated,
        changed_authority_refs=(old_model,),
        recomposed_products=(),
    )
    with pytest.raises(MissingCrossOwnerEdge, match="MISSING_CROSS_OWNER_EDGE"):
        assert_closure_covers_registered_products(
            outcome=fabricated_outcome,
            registry=registry,
            recompose={product_ref.key: recompose},
            successor_authority=staged["successor"],
        )


def test_h08_unknown_dependent_is_not_current():
    """Hostile: the owner never spoke about this ref, so there is no currentness."""

    case = _case()
    result = _provide(case)
    _, product_ref = _register(case, result)
    staged = _stage_transition(
        case, product_ref, case["model_rule"].model_authority_ref
    )
    stranger = ExactRef(
        "N10E_EMPIRICAL_POSSIBILITY_SLICE_PRODUCT@1",
        "urn:test:hq221:never-registered-product",
        "6" * 64,
    )
    with pytest.raises(OwnerUnknownDependent) as excinfo:
        resolve_current_analytical_product(
            executor=staged["executor"], dependent_ref=stranger
        )
    assert "cached or resident bytes do not make it current" in str(excinfo.value)


def test_h09_explicitly_noncurrent_dependent_is_not_served_as_current():
    """Hostile: a governed noncurrent outcome is honoured, not overridden."""

    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    staged = _stage_transition(
        case, product_ref, case["model_rule"].model_authority_ref
    )
    policy_ref = fx._ref_for("REPLACEMENT_POLICY", "hq221-hostile")
    row = NoncurrentDependentOutcome(
        old_ref=product_ref,
        disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
        reason_code="NO_LAWFUL_REPLACEMENT_SOURCE",
        supporting_refs=(policy_ref,),
    )
    outcome = _transition(
        case, registry, staged, {}, noncurrent_dependents={product_ref.key: row}
    )
    assert outcome.invalidation_receipt.noncurrent_old_refs == (product_ref,)
    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=staged["executor"], dependent_ref=product_ref
        )
    # No replacement was invented anywhere in the receipt.
    assert outcome.invalidation_receipt.recompilation_pairs == ()


def test_h10_stale_stored_receipt_cannot_claim_a_fresh_replay_grade():
    """Hostile: a stored receipt mechanism may not claim the fresh grade."""

    case = _case()
    result = _provide(case)
    composition = result.composition_result
    common = dict(
        claim_id="hq221-hostile-stale-receipt",
        replayed_product_ref=_product_ref(result.result_identity_hash),
        retained_determinant_refs=(
            case["empirical_query"].ref,
            case["predicate"].ref,
            case["consumer_query"].ref,
            case["condition_binding_witness"].witness_ref,
        ),
        producer_route=result.provider_receipt.provider_route,
        producer_path=PROVIDER_PATH,
        authority_refs=tuple(composition.authority_refs),
        expected_output_identity_hash=result.result_identity_hash,
        replay_protocol_ref=fx.replay_protocol_ref(case),
        deterministic_order_or_tie_rule_refs=(fx.deterministic_order_ref(case),),
        limitations=("hostile: a stored receipt is not fresh recomputation",),
    )
    # A stored receipt is only a serialization replay.
    stale = AnalyticalReplayClaim(
        actual_replay_mechanism=MECHANISM_STORED_RECEIPT_DESERIALIZATION,
        replay_grade=REPLAY_GRADE_SERIALIZATION_REPLAY,
        **common,
    )
    assert stale.replay_grade == REPLAY_GRADE_SERIALIZATION_REPLAY
    # Claiming the fresh grade on that mechanism is refused.
    with pytest.raises(ReplayGradeOverclaim, match="REPLAY_GRADE_OVERCLAIM"):
        AnalyticalReplayClaim(
            actual_replay_mechanism=MECHANISM_STORED_RECEIPT_DESERIALIZATION,
            replay_grade=REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
            **common,
        )


def test_h11_mismatched_consumer_result_identity_is_rejected():
    """Hostile: a receipt cannot be paired with a foreign composition/consumer."""

    case = _case()
    result = _provide(case)
    foreign = _provide(_case("reverse"))

    with pytest.raises(
        ProviderRequestShapeError, match="receipt/composition identity mismatch"
    ):
        EmpiricalPossibilitySliceProviderResult(
            provider_state="EXACT_SUPPORTED_SLICE_PRODUCED",
            provider_receipt=result.provider_receipt,
            composition_result=foreign.composition_result,
            generated_evidence_or_null=result.generated_evidence_or_null,
            consumer_result_or_null=result.consumer_result_or_null,
        )
    # And the two directions genuinely differ, so the mismatch was not vacuous.
    assert (
        foreign.consumer_result_or_null.result_hash
        != result.consumer_result_or_null.result_hash
    )
    assert (
        foreign.receipt_ref.content_hash != result.receipt_ref.content_hash
    )


def test_h12_lifecycle_and_cache_presence_cannot_restore_currentness():
    """Hostile: a cached/retained historical artifact is not current.

    After a governed transition replaces the provider product, the OLD ref must not be
    resolvable as the current product even though its exact bytes/objects remain
    perfectly present and recomputable.
    """

    case = _case()
    result = _provide(case)
    registry, product_ref = _register(case, result)
    staged = _stage_transition(
        case, product_ref, case["model_rule"].model_authority_ref
    )
    outcome = _transition(
        case, registry, staged, {product_ref.key: _recomposer(case)}
    )
    (old, new), = outcome.invalidation_receipt.recompilation_pairs
    assert old.content_hash == result.result_identity_hash

    # The old product is still fully present and recomputable from its determinants.
    replayed = _provide(case)
    assert replayed.result_identity_hash == old.content_hash

    # ...yet the owner names the NEW ref as the current product.
    status = resolve_current_analytical_product(
        executor=staged["executor"], dependent_ref=product_ref
    )
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert status["current_replacement_ref"] == new
    assert status["current_replacement_ref"].content_hash != old.content_hash
    # The historical exact artifact is still addressable, just not current.
    assert staged["executor"].resolve_historical_exact(staged["successor"])


def test_h12b_owner_recompiler_refuses_an_unregistered_affected_dependent():
    """The adapter never guesses a successor for an unregistered product."""

    case = _case()
    result = _provide(case)
    _, product_ref = _register(case, result)
    staged = _stage_transition(
        case, product_ref, case["model_rule"].model_authority_ref
    )
    stranger = _product_ref("7" * 64)
    recompiler = build_owner_recompiler(
        executor=staged["executor"],
        registry=AnalyticalDependencyRegistry(),
        recompose={},
    )
    with pytest.raises(
        AuthorityMaintenanceError, match="not a registered analytical product"
    ):
        recompiler(
            stranger, (case["model_rule"].model_authority_ref, staged["successor"])
        )


# ==========================================================================
# productive adequacy (HQD-216): the lane must travel the POSITIVE path
# ==========================================================================
def test_productive_adequacy_the_positive_path_is_actually_occupied(tmp_path):
    """HQD-216: REFUSAL_CORRECTNESS != N10E_COMPLETION.

    This commissioned function has a mandatory positive role. The court must show
    the positive producer -> consumer -> lifecycle/replay path is genuinely occupied,
    not merely that refusals are correct.
    """

    observed = _run_fresh(_runner_input(tmp_path))

    positive = {
        "provider_state": observed["provider_state"],
        "consumer_result_state_or_null": observed["consumer_result_state_or_null"],
        "lifecycle_state": observed["lifecycle_state"],
    }
    assert positive == {
        "provider_state": "EXACT_SUPPORTED_SLICE_PRODUCED",
        "consumer_result_state_or_null": "EXACT_SUPPORTED",
        "lifecycle_state": DEPENDENT_LIFECYCLE_CURRENT,
    }
    # No refusal state was reached anywhere on the positive path.
    assert "refusal_state_or_null" not in observed
    # The empirical product is substantive: an exact, non-degenerate conditional law.
    assert observed["raw_denominator_support"] == 60
    assert observed["cell_numerators"] == {"yes": 54, "no": 6}
    assert observed["evidence_identity_is_producer_derived"] is True
    # The product genuinely moved under the governed revision (AT19 real closure).
    assert observed["current_replacement_ref_or_null"]["content_hash"] != (
        observed["product_ref"]["content_hash"]
    )


def test_productive_adequacy_no_production_owner_was_mutated_by_this_court():
    """The seam was sufficient: the court needed no production mutation.

    If a production file named in the commission's permitted-mutation list had been
    changed, this assertion would fail loudly rather than let a silent edit stand in
    for a proven chain.
    """

    import inspect

    from rawlsing_next import pre553_analytical_replay_dependency as adapter
    from rawlsing_next import pre553_empirical_possibility_provider as provider

    # The provider is still a seam: it delegates and does not compute geometry.
    provider_source = inspect.getsource(provider)
    assert "compose_positioned_subject_possibility(" in provider_source
    assert "def _compute" not in provider_source

    # The adapter is still not a lifecycle owner.
    adapter_source = inspect.getsource(adapter)
    assert "promote_current(" in adapter_source
    assert "AuthorityInvalidationReceipt(" not in adapter_source
    for forbidden in (
        "def promote_current",
        "def rollback_current",
        "def adjudicate_candidate",
        "def seal_revision",
    ):
        assert forbidden not in adapter_source, forbidden


def test_productive_adequacy_runner_source_has_no_answer_channel():
    """Static guarantee that the fresh runner cannot read an answer."""

    import inspect

    from rawlsing_next.tests import n10e_provider_replay_lifecycle_runner as runner

    source = inspect.getsource(runner)
    for forbidden in (
        "oracle_expected_output",
        "FROZEN_ORACLE",
        "FROZEN_CHANGED_ORACLE",
        "frozen_evidence_ref",
        "frozen_consumer_result_hash",
        "ADOPTED_SUCCESSOR",
        "successor_digest",
    ):
        assert forbidden not in source, forbidden
    # The only expected-identity material the runner touches is the optional oracle
    # file it compares against strictly after recomputing.
    assert source.count('argv.index("--expect")') == 1
    assert "assert_runner_input_carries_no_answer" in source