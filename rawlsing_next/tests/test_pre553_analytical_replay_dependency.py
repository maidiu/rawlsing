"""C1-03R court: AT18 replay grade and AT19 selective invalidation.

Everything here is source-free: the synthetic AT07 law and frozen synthetic C1-00
authority snapshots. No raw survey material, no real-source C11 execution, no C4, no
N10E duplication, and no AT14-AT17 implementation.

Proof grades are kept explicit and separate:
  * static inspection;
  * source-free executed accepted producer/composition;
  * fresh-process recomputation from retained determinants;
  * existing-owner invalidation/closure execution.
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys

import pytest

from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_analytical_replay_dependency import (
    DEPENDENCY_CONTRACT_ID,
    MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER,
    MECHANISM_HISTORICAL_NARRATION,
    MECHANISM_STORED_PRODUCT_DESERIALIZATION,
    MECHANISM_STORED_RECEIPT_DESERIALIZATION,
    REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
    REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    REPLAY_GRADE_SERIALIZATION_REPLAY,
    REPLAY_GRADES,
    AnalyticalDependencyRegistry,
    AnalyticalProductRegistration,
    AnalyticalReplayClaim,
    AnalyticalReplayDependencyError,
    DependencyClosureFailure,
    MissingCrossOwnerEdge,
    MissingExactDeterminant,
    ReplayGradeOverclaim,
    assert_closure_against_actual_identity_change,
    assert_replay_claim,
    invalidate_for_changed_determinants,
)
from rawlsing_next.pre553_authority_maintenance import (
    AuthorityInvalidationReceipt,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    ReplayReceipt,
    exact_ref,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityModelRule,
)

from rawlsing_next.tests import c1_at18_at19_fixture as fx

COMPOSED_PRODUCT_KIND = "C1_ANALYTICAL_COMPOSED_PRODUCT@1"
PRODUCER_PATH = (
    "rawlsing_next.pre553_analytical_composition."
    "compose_positioned_subject_possibility"
)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _product_ref(direction: str, identity_hash: str) -> ExactRef:
    return ExactRef(
        COMPOSED_PRODUCT_KIND,
        f"urn:test:c1-03r:composed:{direction}",
        identity_hash,
    )


def _compose_with_model_authority(case, model_authority):
    rule = case["model_rule"]
    mutated_rule = PositionedSubjectPossibilityModelRule(
        model_authority,
        rule.walkback_authority_ref,
        rule.source_universe_refs,
        rule.walkback_steps,
        rule.positive_proxy_authority_refs,
    )
    return compose_positioned_subject_possibility(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=mutated_rule,
        condition_binding_witness=case["condition_binding_witness"],
    )


def _recompose_forward(case):
    """A real recompiler: re-executes the accepted composition owner.

    The product reidentifies exactly when the supplied determinant is the governed
    *revision* of its model authority; presented with its own unchanged determinant it
    recomposes to its existing identity, which is the correct closure behaviour.
    """

    def recompose(changed: tuple[AuthorityRef, ...]) -> ExactRef:
        composition = _compose_with_model_authority(case, changed[0])
        return _product_ref("forward", composition.composed_result_identity_hash)

    return recompose


def _fresh_process_observed(tmp_path) -> dict:
    determinants = fx.retained_determinants(fx.build_case("forward"))
    path = tmp_path / "retained_determinants.json"
    path.write_text(json.dumps(determinants), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(fx.ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "rawlsing_next.tests.c1_at18_at19_fresh_process_runner",
            str(path),
        ],
        cwd=str(fx.ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout)


def _revised_forward_model() -> AuthorityRef:
    """A distinct exact revised model authority used as the mutated determinant."""

    from rawlsing_next.pre553_empirical_objects import semantic_hash

    return AuthorityRef(
        "C1-AT07-MODEL-FORWARD-REVISED",
        "1.0.0",
        semantic_hash({"revised": True, "direction": "forward"}),
    )


def _claim(case, composition, **overrides) -> AnalyticalReplayClaim:
    kwargs = dict(
        claim_id="c1-03r-at18-forward",
        replayed_product_ref=_product_ref(
            "forward", composition.composed_result_identity_hash
        ),
        retained_determinant_refs=(
            case["empirical_query"].ref,
            case["predicate"].ref,
            case["consumer_query"].ref,
            case["condition_binding_witness"].witness_ref,
        ),
        producer_route=composition.producer_route,
        producer_path=PRODUCER_PATH,
        authority_refs=tuple(composition.authority_refs),
        expected_output_identity_hash=composition.composed_result_identity_hash,
        actual_replay_mechanism=MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER,
        replay_grade=REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
        limitations=("source-free synthetic fixture; not live occupancy",),
        replay_protocol_ref=fx.replay_protocol_ref(case),
        deterministic_order_or_tie_rule_refs=(fx.deterministic_order_ref(case),),
    )
    kwargs.update(overrides)
    return AnalyticalReplayClaim(**kwargs)


def _registered_pair():
    """Register the two real analytical products with their real determinants."""

    forward_case = fx.build_case("forward")
    reverse_case = fx.build_case("reverse")
    forward = fx.compose(forward_case)
    reverse = fx.compose(reverse_case)
    forward_model = forward_case["model_rule"].model_authority_ref
    reverse_model = reverse_case["model_rule"].model_authority_ref
    registry = AnalyticalDependencyRegistry()
    registry.register(
        AnalyticalProductRegistration(
            product_ref=_product_ref("forward", forward.composed_result_identity_hash),
            product_identity_hash=forward.composed_result_identity_hash,
            determinant_authority_refs=tuple(forward.authority_refs),
            determinant_exact_refs=(forward_case["empirical_query"].ref,),
            consumer_lane_authority_refs=(forward_model, _revised_forward_model()),
            recompose=_recompose_forward(forward_case),
        )
    )
    registry.register(
        AnalyticalProductRegistration(
            product_ref=_product_ref("reverse", reverse.composed_result_identity_hash),
            product_identity_hash=reverse.composed_result_identity_hash,
            determinant_authority_refs=tuple(reverse.authority_refs),
            determinant_exact_refs=(reverse_case["empirical_query"].ref,),
            consumer_lane_authority_refs=(reverse_model,),
            recompose=None,
        )
    )
    return registry, forward, reverse, forward_model, reverse_model


# --------------------------------------------------------------------------
# AT18 - replay grade
# --------------------------------------------------------------------------
def test_at18_forward_product_identity_is_stable_in_process():
    case = fx.build_case("forward")
    composition = fx.compose(case)
    assert composition.analytical_state == "SUPPORTED"
    assert composition.raw_denominator_support == fx.FROZEN_AT07_FORWARD["denominator"]
    assert {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in composition.complete_cell_geometry
    } == fx.FROZEN_AT07_FORWARD["cells"]
    assert composition.producer_route == "DIRECT_I03_TO_POSITIONED_SUBJECT"


def test_at18_fresh_process_recomputes_from_retained_determinants(tmp_path):
    """AT18 positive: a fresh process recomputes the accepted product exactly."""

    case = fx.build_case("forward")
    composition = fx.compose(case)
    determinants = fx.retained_determinants(case)

    # The retained artifact must carry no stored analytical output.
    serialized = json.dumps(determinants)
    assert "complete_cell_geometry" not in serialized
    assert '"geometry"' not in serialized
    assert "exact_fraction" not in serialized

    observed = _fresh_process_observed(tmp_path)

    assert observed["composed_result_identity_hash"] == (
        composition.composed_result_identity_hash
    )
    assert observed["composed_result_identity_hash"] == (
        determinants["expected_output_identity"]["composed_result_identity_hash"]
    )
    assert observed["producer_fact_ref"] == composition.producer_fact_ref.as_dict()
    assert observed["evidence_ref_or_null"] == (
        composition.possibility_slice_evidence_or_null.evidence_ref.as_dict()
    )
    assert observed["consumer_result_hash_or_null"] == (
        composition.consumer_result_or_null.result_hash
    )
    assert observed["raw_denominator_support"] == 60
    assert observed["cell_numerators"] == {"yes": 54, "no": 6}
    assert observed["producer_route"] == composition.producer_route


def test_at18_fresh_process_identity_binds_claim_at_fresh_grade(tmp_path):
    case = fx.build_case("forward")
    composition = fx.compose(case)
    observed = _fresh_process_observed(tmp_path)
    claim = _claim(case, composition)

    assertion = assert_replay_claim(
        claim, observed_output_identity_hash=observed["composed_result_identity_hash"]
    )
    assert assertion.identity_reproduced is True
    assert assertion.asserted_grade_is_honest is True
    assert assertion.replay_grade == REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION

    receipt = claim.to_replay_receipt()
    assert isinstance(receipt, ReplayReceipt)
    assert receipt.replay_state == "REPLAY_VERIFIED"
    assert receipt.semantic_fields["replay_grade"] == (
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION
    )
    assert receipt.semantic_fields["actual_replay_mechanism"] == (
        MECHANISM_FRESH_PROCESS_ACCEPTED_PRODUCER
    )
    assert exact_ref(receipt.replayed_object_ref, "replayed_object_ref") == (
        claim.replayed_product_ref
    )
    # The owner canonicalizes set-like refs, so compare as exact sets.
    assert sorted(
        (exact_ref(x, "input_content_identity_ref") for x in receipt.input_content_identity_refs),
        key=lambda r: r.key,
    ) == sorted(claim.retained_determinant_refs, key=lambda r: r.key)


def test_at18_grade_contract_distinguishes_all_four_grades():
    assert REPLAY_GRADES == (
        REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
        REPLAY_GRADE_SERIALIZATION_REPLAY,
        REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    )
    case = fx.build_case("forward")
    composition = fx.compose(case)

    # Each weaker mechanism may assert at most its own (or weaker) grade.
    historical = _claim(
        case,
        composition,
        actual_replay_mechanism=MECHANISM_HISTORICAL_NARRATION,
        replay_grade=REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    )
    assert historical.replay_grade == REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY

    serialization = _claim(
        case,
        composition,
        actual_replay_mechanism=MECHANISM_STORED_RECEIPT_DESERIALIZATION,
        replay_grade=REPLAY_GRADE_SERIALIZATION_REPLAY,
    )
    assert serialization.replay_grade == REPLAY_GRADE_SERIALIZATION_REPLAY


@pytest.mark.parametrize(
    ("mechanism", "claimed_grade"),
    (
        (MECHANISM_HISTORICAL_NARRATION, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION),
        (MECHANISM_STORED_RECEIPT_DESERIALIZATION, REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY),
        (MECHANISM_STORED_PRODUCT_DESERIALIZATION, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION),
        (MECHANISM_HISTORICAL_NARRATION, REPLAY_GRADE_SERIALIZATION_REPLAY),
    ),
)
def test_at18_hostile_stored_explanation_cannot_claim_fresh_grade(
    mechanism, claimed_grade
):
    """AT18 hostile: stored explanation/serialization is not fresh recomputation."""

    case = fx.build_case("forward")
    composition = fx.compose(case)
    with pytest.raises(ReplayGradeOverclaim, match="REPLAY_GRADE_OVERCLAIM"):
        _claim(
            case,
            composition,
            actual_replay_mechanism=mechanism,
            replay_grade=claimed_grade,
        )


def test_at18_missing_exact_determinant_or_authority_fails_closed():
    case = fx.build_case("forward")
    composition = fx.compose(case)
    with pytest.raises(MissingExactDeterminant, match="MISSING_EXACT_DETERMINANT"):
        _claim(case, composition, retained_determinant_refs=())
    with pytest.raises(MissingExactDeterminant, match="MISSING_EXACT_DETERMINANT"):
        _claim(case, composition, authority_refs=())


def test_at18_claimed_grade_does_not_silently_downgrade_on_identity_mismatch():
    """A stronger claim whose identity does not reproduce must fail, not downgrade."""

    case = fx.build_case("forward")
    composition = fx.compose(case)
    claim = _claim(case, composition)
    with pytest.raises(AnalyticalReplayDependencyError, match="did not reproduce"):
        assert_replay_claim(claim, observed_output_identity_hash="0" * 64)


def test_at18_runner_does_not_read_stored_expected_output():
    """Static inspection: the fresh runner computes rather than deserializes an answer."""

    from rawlsing_next.tests import c1_at18_at19_fresh_process_runner as runner

    source = inspect.getsource(runner)
    assert "compose_positioned_subject_possibility(" in source
    # It must not read the expected output identity from the retained artifact.
    assert "expected_output_identity" not in source
    assert "composed_result_identity_hash\"] =" not in source
    # And it must verify the rebuilt determinants match the retained refs.
    assert "did not rebuild exactly" in source


# --------------------------------------------------------------------------
# AT19 - selective invalidation
# --------------------------------------------------------------------------
def test_at19_single_determinant_mutation_invalidates_only_affected_product():
    registry, forward, reverse, forward_model, reverse_model = _registered_pair()
    assert forward_model != reverse_model

    outcome = invalidate_for_changed_determinants(
        registry=registry, changed_determinant_refs=(_revised_forward_model(),)
    )
    receipt = outcome.invalidation_receipt

    assert isinstance(receipt, AuthorityInvalidationReceipt)
    assert tuple(receipt.changed_authority_refs) == (_revised_forward_model(),)
    assert receipt.affected_dependent_refs == (
        _product_ref("forward", forward.composed_result_identity_hash),
    )
    assert receipt.unaffected_dependent_refs == (
        _product_ref("reverse", reverse.composed_result_identity_hash),
    )
    assert len(receipt.recompilation_pairs) == 1
    old_ref, new_ref = receipt.recompilation_pairs[0]
    assert old_ref == _product_ref("forward", forward.composed_result_identity_hash)
    assert new_ref != old_ref, "the affected product must recompile to a new identity"
    # Replacement identity is exact: it is the real recomposed identity, not a label.
    recomposed = _compose_with_model_authority(
        fx.build_case("forward"), _revised_forward_model()
    )
    assert new_ref.content_hash == recomposed.composed_result_identity_hash

    # The unaffected sibling keeps its identity and was never recompiled.
    assert outcome.noncurrent_product_refs == ()
    assert reverse.composed_result_identity_hash not in outcome.recompiled_identity_hashes


def test_at19_unaffected_sibling_remains_usable_and_identity_stable():
    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    before = reverse.composed_result_identity_hash
    invalidate_for_changed_determinants(
        registry=registry, changed_determinant_refs=(_revised_forward_model(),)
    )
    # Recomputing the sibling from its own untouched determinants is still exact.
    after = fx.compose(fx.build_case("reverse"))
    assert after.composed_result_identity_hash == before
    assert (
        after.consumer_result_or_null.result_state
        == reverse.consumer_result_or_null.result_state
        == "EXACT_SUPPORTED"
    )


def test_at19_lawful_replacement_unavailable_yields_explicit_noncurrent():
    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    outcome = invalidate_for_changed_determinants(
        registry=registry, changed_determinant_refs=(_revised_forward_model(),)
    )
    receipt = outcome.invalidation_receipt
    # Every affected product is accounted for by exactly one governed outcome.
    covered = {old.key for old, _ in receipt.recompilation_pairs}
    assert covered == {ref.key for ref in receipt.affected_dependent_refs}

    # Now register a second product with an affected determinant but no recompiler:
    # it must be recorded noncurrent rather than silently treated as current.
    second = AnalyticalDependencyRegistry()
    second.register(
        AnalyticalProductRegistration(
            product_ref=_product_ref("forward", forward.composed_result_identity_hash),
            product_identity_hash=forward.composed_result_identity_hash,
            determinant_authority_refs=(_revised_forward_model(),),
            determinant_exact_refs=(),
            recompose=None,
        )
    )
    no_replacement = invalidate_for_changed_determinants(
        registry=second, changed_determinant_refs=(_revised_forward_model(),)
    )
    assert no_replacement.noncurrent_product_refs == (
        _product_ref("forward", forward.composed_result_identity_hash),
    )
    sentinel = no_replacement.invalidation_receipt.recompilation_pairs[0][1]
    assert sentinel.kind == "C1_03R_NONCURRENT_PRODUCT"
    assert sentinel != no_replacement.noncurrent_product_refs[0]


def test_at19_invalidation_receipt_distinguishes_affected_from_unaffected():
    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    outcome = invalidate_for_changed_determinants(
        registry=registry, changed_determinant_refs=(_revised_forward_model(),)
    )
    projection = outcome.invalidation_receipt.semantic_projection()
    assert projection["contract_id"]
    affected = {row["object_id"] for row in projection["affected_dependent_refs"]}
    unaffected = {row["object_id"] for row in projection["unaffected_dependent_refs"]}
    assert affected and unaffected
    assert affected.isdisjoint(unaffected)


def test_at19_graph_is_built_from_real_registrations_not_similarity():
    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    graph = registry.build_graph()
    assert isinstance(graph, SemanticDeterminantGraph)
    # Only real registered determinants appear as authority edges.
    edge_authorities = {auth.key for auth, _ in graph.authority_edges}
    assert forward_model.key in edge_authorities
    for registration in registry.registrations:
        for authority in registration.all_determinant_authority_refs:
            assert authority.key in edge_authorities
    assert {
        ref.key for ref in graph.known_dependent_refs
    } == {
        _product_ref("forward", forward.composed_result_identity_hash).key,
        _product_ref("reverse", reverse.composed_result_identity_hash).key,
    }


# --------------------------------------------------------------------------
# AT19 mandatory missing-cross-owner-edge hostile
# --------------------------------------------------------------------------
def test_at19_missing_cross_owner_edge_is_a_failed_closure_witness():
    """Mandatory hostile: an incomplete cross-owner graph must fail closed.

    The forward product genuinely reidentifies under the changed determinant, but the
    graph deliberately omits the edge that connects them. Closure must fail; cache or
    object presence cannot restore authority.
    """

    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    forward_ref = _product_ref("forward", forward.composed_result_identity_hash)
    incomplete = registry.build_graph(
        omit_authority_edges=(
            (forward_model, forward_ref),
            (_revised_forward_model(), forward_ref),
        )
    )
    # With the edge omitted the graph claims nothing is affected ...
    assert incomplete.affected((forward_model,)) == ()
    # ... but the product's identity genuinely moves, so the closure claim is false.
    with pytest.raises(MissingCrossOwnerEdge, match="MISSING_CROSS_OWNER_EDGE"):
        assert_closure_against_actual_identity_change(
            registry=registry,
            changed_determinant_refs=(_revised_forward_model(),),
            graph=incomplete,
        )


def test_at19_presence_of_bytes_cannot_restore_current_authority():
    """A cached/registered product ref is not currentness."""

    registry, forward, reverse, forward_model, _reverse_model = _registered_pair()
    forward_ref = _product_ref("forward", forward.composed_result_identity_hash)
    # The product ref is present in the registry (its "bytes" exist) ...
    assert forward_ref.key in {r.product_ref.key for r in registry.registrations}
    incomplete = registry.build_graph(
        omit_authority_edges=(
            (forward_model, forward_ref),
            (_revised_forward_model(), forward_ref),
        )
    )
    assert forward_ref.key in {ref.key for ref in incomplete.known_dependent_refs}
    # ... yet presence alone does not make the closure witness hold.
    with pytest.raises(MissingCrossOwnerEdge):
        assert_closure_against_actual_identity_change(
            registry=registry,
            changed_determinant_refs=(_revised_forward_model(),),
            graph=incomplete,
        )


def test_at19_lane_does_not_infer_the_missing_dependency():
    """The adapter must not repair a missing edge by similarity or inference."""

    registry, forward, _reverse, forward_model, _reverse_model = _registered_pair()
    forward_ref = _product_ref("forward", forward.composed_result_identity_hash)
    incomplete = registry.build_graph(
        omit_authority_edges=(
            (forward_model, forward_ref),
            (_revised_forward_model(), forward_ref),
        )
    )
    # No inference: the omitted edge is simply absent, never fabricated.
    assert (forward_model, forward_ref) not in incomplete.authority_edges
    assert all(
        auth.key != forward_model.key or dep.key != forward_ref.key
        for auth, dep in incomplete.authority_edges
    )


def test_at19_affected_product_without_identity_change_fails_closed():
    """A registered affected product that does not move is a closure contradiction."""

    case = fx.build_case("forward")
    composition = fx.compose(case)
    model = case["model_rule"].model_authority_ref
    registry = AnalyticalDependencyRegistry()
    registry.register(
        AnalyticalProductRegistration(
            product_ref=_product_ref("forward", composition.composed_result_identity_hash),
            product_identity_hash=composition.composed_result_identity_hash,
            determinant_authority_refs=(_revised_forward_model(),),
            determinant_exact_refs=(),
            # A recompiler that returns the same ref cannot evidence invalidation.
            recompose=lambda changed: _product_ref(
                "forward", composition.composed_result_identity_hash
            ),
        )
    )
    with pytest.raises(DependencyClosureFailure, match="DEPENDENCY_CLOSURE_FAILURE"):
        invalidate_for_changed_determinants(
            registry=registry, changed_determinant_refs=(_revised_forward_model(),)
        )


def test_at19_adapter_does_not_become_a_second_maintenance_owner():
    """Static inspection of the ownership boundary."""

    import rawlsing_next.pre553_analytical_replay_dependency as adapter

    source = inspect.getsource(adapter)
    for forbidden in (
        "def promote_current",
        "def rollback_current",
        "def adjudicate_candidate",
        "def seal_revision",
        "def intake_candidate",
    ):
        assert forbidden not in source, forbidden
    # It must delegate closure to the existing owner rather than reimplementing it.
    assert "SemanticDeterminantGraph" in source
    assert "AuthorityInvalidationReceipt" in source
    assert adapter.DEPENDENCY_CONTRACT_ID
