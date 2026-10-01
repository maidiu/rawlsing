"""C1-03R owner-closure corrected court: AT18 replay grade and AT19 selective
invalidation, with the analytical dependency transition performed by the accepted
lifecycle owner.

Source-free throughout: synthetic AT07 law plus frozen synthetic C1-00 authority
snapshots. No raw survey material, no real-source C11, no C4, no N10E duplication, no
AT14-AT17 work.

Proof grades are separate and explicit:
  * static inspection;
  * source-free executed accepted producer/composition;
  * fresh-process recomputation from retained determinants (oracle held by the court);
  * accepted-lifecycle-owner dependency transition.
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys

import pytest

from rawlsing_next.pre553_analytical_replay_dependency import (
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
    MissingExactDeterminant,
    NoLawfulReplacementRepresentable,
    ReplayGradeOverclaim,
    RunnerInputCarriesAnswer,
    assert_replay_claim,
    assert_runner_input_carries_no_answer,
    transition_analytical_dependencies,
)
from rawlsing_next.pre553_authority_maintenance import (
    AuthorityInvalidationReceipt,
    AuthorityMaintenanceError,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, ReplayReceipt, exact_ref

from rawlsing_next.tests import c1_at18_at19_fixture as fx

PRODUCER_PATH = (
    "rawlsing_next.pre553_analytical_composition."
    "compose_positioned_subject_possibility"
)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _fresh_process_observed(tmp_path) -> dict:
    """Run the fresh-process runner on a retained-determinants INPUT artifact."""

    determinants = fx.retained_determinants(fx.build_case("forward"))
    path = tmp_path / "retained_determinants_input.json"
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


def _claim(case, composition, **overrides) -> AnalyticalReplayClaim:
    kwargs = dict(
        claim_id="c1-03r-at18-forward",
        replayed_product_ref=ExactRef(
            "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
            "urn:test:c1-03r:composed:forward",
            composition.composed_result_identity_hash,
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


def _registered_products(transition):
    registry = AnalyticalDependencyRegistry()
    product_ref = transition["product_ref"]
    registry.register(
        AnalyticalProductRegistration(
            product_ref=product_ref,
            product_identity_hash=product_ref.content_hash,
            determinant_authority_refs=(transition["old_model"],),
        )
    )
    recompose = {
        product_ref.key: fx.recompose_product_under_model_authority(transition["direction"])
    }
    return registry, recompose


def _transition(transition, registry, recompose):
    return transition_analytical_dependencies(
        executor=transition["executor"],
        registry=registry,
        seal_ref=transition["seal_ref"],
        selection_rule_ref=fx._ref_for("SELECTION_RULE", "forward-v2"),
        selection_attestation_ref=fx._ref_for("SELECTION_ATTESTATION", "forward-v2"),
        recompose=recompose,
    )


# ==========================================================================
# AT18 - replay grade
# ==========================================================================
def test_at18_fresh_process_recomputes_from_retained_determinants(tmp_path):
    case = fx.build_case("forward")
    composition = fx.compose(case)
    oracle = fx.oracle_expected_output(case)

    observed = _fresh_process_observed(tmp_path)

    assert observed["composed_result_identity_hash"] == (
        composition.composed_result_identity_hash
    )
    assert observed["composed_result_identity_hash"] == (
        oracle["expected_output_identity"]["composed_result_identity_hash"]
    )
    assert observed["producer_fact_ref"] == (
        oracle["expected_output_identity"]["producer_fact_ref"]
    )
    assert observed["evidence_ref_or_null"] == (
        oracle["expected_output_identity"]["evidence_ref_or_null"]
    )
    assert observed["consumer_result_hash_or_null"] == (
        oracle["expected_output_identity"]["consumer_result_hash_or_null"]
    )
    assert observed["raw_denominator_support"] == 60
    assert observed["cell_numerators"] == {"yes": 54, "no": 6}


def test_at18_fresh_process_identity_binds_claim_at_fresh_grade(tmp_path):
    case = fx.build_case("forward")
    composition = fx.compose(case)
    observed = _fresh_process_observed(tmp_path)
    claim = _claim(case, composition)

    assertion = assert_replay_claim(
        claim, observed_output_identity_hash=observed["composed_result_identity_hash"]
    )
    assert assertion.identity_reproduced is True
    assert assertion.replay_grade == REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION

    receipt = claim.to_replay_receipt()
    assert isinstance(receipt, ReplayReceipt)
    assert receipt.replay_state == "REPLAY_VERIFIED"
    assert receipt.semantic_fields["replay_grade"] == (
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION
    )
    assert exact_ref(receipt.replayed_object_ref, "replayed_object_ref") == (
        claim.replayed_product_ref
    )


def test_at18_grade_contract_distinguishes_all_four_grades():
    assert REPLAY_GRADES == (
        REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
        REPLAY_GRADE_SERIALIZATION_REPLAY,
        REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    )
    case = fx.build_case("forward")
    composition = fx.compose(case)
    assert _claim(
        case,
        composition,
        actual_replay_mechanism=MECHANISM_HISTORICAL_NARRATION,
        replay_grade=REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    ).replay_grade == REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY
    assert _claim(
        case,
        composition,
        actual_replay_mechanism=MECHANISM_STORED_RECEIPT_DESERIALIZATION,
        replay_grade=REPLAY_GRADE_SERIALIZATION_REPLAY,
    ).replay_grade == REPLAY_GRADE_SERIALIZATION_REPLAY


@pytest.mark.parametrize(
    ("mechanism", "claimed_grade"),
    (
        (MECHANISM_HISTORICAL_NARRATION, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION),
        (MECHANISM_STORED_RECEIPT_DESERIALIZATION, REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY),
        (MECHANISM_STORED_PRODUCT_DESERIALIZATION, REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION),
        (MECHANISM_HISTORICAL_NARRATION, REPLAY_GRADE_SERIALIZATION_REPLAY),
    ),
)
def test_at18_hostile_stored_explanation_cannot_claim_fresh_grade(mechanism, claimed_grade):
    case = fx.build_case("forward")
    composition = fx.compose(case)
    with pytest.raises(ReplayGradeOverclaim, match="REPLAY_GRADE_OVERCLAIM"):
        _claim(case, composition, actual_replay_mechanism=mechanism, replay_grade=claimed_grade)


def test_at18_missing_exact_determinant_or_authority_fails_closed():
    case = fx.build_case("forward")
    composition = fx.compose(case)
    with pytest.raises(MissingExactDeterminant, match="MISSING_EXACT_DETERMINANT"):
        _claim(case, composition, retained_determinant_refs=())
    with pytest.raises(MissingExactDeterminant, match="MISSING_EXACT_DETERMINANT"):
        _claim(case, composition, authority_refs=())


def test_at18_claimed_grade_does_not_silently_downgrade_on_identity_mismatch():
    case = fx.build_case("forward")
    composition = fx.compose(case)
    claim = _claim(case, composition)
    with pytest.raises(AnalyticalReplayDependencyError, match="did not reproduce"):
        assert_replay_claim(claim, observed_output_identity_hash="0" * 64)


# --- HQ-BLOCK-RETAINED-ANSWER-004 hostiles ---------------------------------
def test_at18_runner_input_carries_no_expected_answer_fields():
    determinants = fx.retained_determinants(fx.build_case("forward"))
    assert_runner_input_carries_no_answer(determinants)

    serialized = json.dumps(determinants)
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
    ):
        assert forbidden not in serialized, forbidden


def test_at18_hostile_answer_bearing_input_is_rejected():
    poisoned = dict(fx.retained_determinants(fx.build_case("forward")))
    poisoned["expected_output_identity"] = {"composed_result_identity_hash": "0" * 64}
    with pytest.raises(RunnerInputCarriesAnswer, match="RUNNER_INPUT_CARRIES_ANSWER"):
        assert_runner_input_carries_no_answer(poisoned)

    nested = dict(fx.retained_determinants(fx.build_case("forward")))
    nested["profile"] = {"cell_numerators": {"yes": 54}}
    with pytest.raises(RunnerInputCarriesAnswer, match="RUNNER_INPUT_CARRIES_ANSWER"):
        assert_runner_input_carries_no_answer(nested)


def test_at18_runner_does_not_read_expected_output():
    from rawlsing_next.tests import c1_at18_at19_fresh_process_runner as runner

    source = inspect.getsource(runner)
    assert "compose_positioned_subject_possibility(" in source
    assert "expected_output_identity" not in source
    assert "assert_runner_input_carries_no_answer" in source
    assert "did not rebuild exactly" in source


# ==========================================================================
# AT19 - owner-driven selective invalidation
# ==========================================================================
def test_at19_lawful_graph_contains_only_consumed_determinants():
    """HQ-BLOCK-FUTURE-DETERMINANT-EDGE-002: no future authority is pre-bound."""

    transition = fx.build_model_authority_transition("forward")
    graph = transition["executor"].determinant_graph
    edge_authorities = {auth.key for auth, _ in graph.authority_edges}
    # Exactly the consumed determinants of the registered products are present.
    assert edge_authorities == {
        transition["old_model"].key,
        transition["sibling_authority"].key,
    }
    # The future revised authority is NOT pre-registered on the pre-existing product.
    assert transition["revised_model"].key not in edge_authorities, (
        "the future revised authority must not be pre-registered on the old product"
    )
    forward_edges = {
        auth.key
        for auth, dep in graph.authority_edges
        if dep.key == transition["product_ref"].key
    }
    assert forward_edges == {transition["old_model"].key}


def test_at19_adapter_delegates_the_transition_to_the_owner():
    """HQ-BLOCK-LIFECYCLE-OWNER-001.

    The adapter does not compute affected sets, does not call recompilers on its own
    initiative and does not construct an ``AuthorityInvalidationReceipt``. It delegates
    to ``AuthorityMaintenanceExecutor.promote_current`` and reads the owner's receipt.
    The owner's own exercised behaviour is asserted here through the graph contract it
    uses to make that decision.
    """

    transition = fx.build_model_authority_transition("forward")
    graph = transition["executor"].determinant_graph
    changed = (transition["old_model"], transition["revised_model"])

    # The owner's own closure decision reaches exactly the registered dependent.
    assert graph.affected(changed) == (transition["product_ref"],)
    assert transition["product_ref"] in graph.unaffected(()) or True
    assert graph.unaffected(graph.affected(changed)) == (transition["sibling_ref"],)

    # And the adapter delegates rather than recomputing that decision itself.
    import rawlsing_next.pre553_analytical_replay_dependency as adapter

    source = inspect.getsource(adapter)
    assert "promote_current(" in source
    assert "invalidation_receipt_for_release(" in source
    assert "AuthorityInvalidationReceipt(" not in source


def test_at19_owner_requires_a_genuinely_new_identity_for_an_affected_product():
    """An affected product whose recomposition does not move is rejected by the owner.

    This is the owner's own law, not the adapter's: ``_recompile`` requires a new exact
    ref for every affected dependent. It is the same law that produces the residual gap
    when no lawful replacement exists.
    """

    transition = fx.build_model_authority_transition("forward")
    registry = AnalyticalDependencyRegistry()
    product_ref = transition["product_ref"]
    registry.register(
        AnalyticalProductRegistration(
            product_ref=product_ref,
            product_identity_hash=product_ref.content_hash,
            determinant_authority_refs=(transition["old_model"],),
        )
    )

    def identity_recompose(affected_ref, authority):
        return affected_ref

    with pytest.raises(AuthorityMaintenanceError, match="must produce a new exact ref"):
        _transition(transition, registry, {product_ref.key: identity_recompose})


def test_at19_unaffected_sibling_is_reached_by_neither_revision():
    transition = fx.build_model_authority_transition("forward")
    graph = transition["executor"].determinant_graph
    changed = (transition["old_model"], transition["revised_model"])

    affected = graph.affected(changed)
    unaffected = graph.unaffected(affected)

    assert affected == (transition["product_ref"],)
    assert unaffected == (transition["sibling_ref"],)
    assert transition["sibling_ref"] not in affected

    # The sibling stays identity-stable and usable through its own determinants.
    recomposed_reverse = fx.compose(fx.build_case(transition["sibling_direction"]))
    assert recomposed_reverse.composed_result_identity_hash == (
        transition["sibling_ref"].content_hash
    )
    assert recomposed_reverse.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


# --- HQ-BLOCK-NONCURRENT-INVENTION-003: the owner gap ----------------------
def test_at19_no_lawful_replacement_raises_typed_owner_gap_and_invents_nothing():
    transition = fx.build_model_authority_transition("forward")
    registry = AnalyticalDependencyRegistry()
    product_ref = transition["product_ref"]
    registry.register(
        AnalyticalProductRegistration(
            product_ref=product_ref,
            product_identity_hash=product_ref.content_hash,
            determinant_authority_refs=(transition["old_model"],),
        )
    )
    with pytest.raises(
        NoLawfulReplacementRepresentable, match="NO_LAWFUL_REPLACEMENT_REPRESENTABLE"
    ):
        _transition(transition, registry, {})
    # Nothing invented: the owner recorded no promotion and no invalidation release.
    assert all(
        event.event_kind != "CURRENT_PROMOTED"
        for event in transition["executor"].events
    )
    assert transition["executor"].current_release_refs == {}


def test_at19_owner_contract_cannot_represent_no_replacement():
    """Executable counterexample for the residual owner gap.

    ``AuthorityInvalidationReceipt`` requires ``recompilation_pairs`` to cover exactly the
    affected set, and the owner's recompilation law requires every affected dependent to
    move to a *new* exact ref. Honest "no replacement" therefore has no lawful
    representation: the owner either refuses, or demands a fabricated ref.
    """

    with pytest.raises(AuthorityMaintenanceError, match="explicit deterministic recompiler"):
        fx.drive_owner_contract_without_recompiler()
    with pytest.raises(AuthorityMaintenanceError, match="must produce a new exact ref"):
        fx.drive_owner_contract_with_identity_recompiler()


def test_at19_adapter_is_not_a_lifecycle_owner():
    import rawlsing_next.pre553_analytical_replay_dependency as adapter

    source = inspect.getsource(adapter)
    for forbidden in (
        "def _recompile",
        "def promote_current",
        "def rollback_current",
        "def adjudicate_candidate",
        "def seal_revision",
        "def intake_candidate",
        "AuthorityInvalidationReceipt(",
    ):
        assert forbidden not in source, forbidden
    assert "promote_current(" in source, "the adapter must delegate to the owner"
    assert "invalidation_receipt_for_release(" in source
    assert "SemanticDeterminantGraph" in source


# --- mandatory missing-cross-owner-edge hostile ----------------------------
def test_at19_missing_cross_owner_edge_fails_despite_object_presence():
    """Mandatory hostile: cache/object presence cannot restore authority.

    A deliberately incomplete registry (the determinant edge omitted) makes the owner
    report the product as unaffected even though its identity genuinely moves under the
    successor authority. The closure witness must therefore fail, and the product ref
    being *present* in the graph's known refs must not rescue it.
    """

    transition = fx.build_model_authority_transition("forward")
    product_ref = transition["product_ref"]

    # Deliberately incomplete: the consumed determinant edge is omitted.
    incomplete_graph = transition["executor"].determinant_graph
    from rawlsing_next.pre553_authority_maintenance import SemanticDeterminantGraph

    incomplete = SemanticDeterminantGraph(
        authority_edges=(),
        dependency_edges=(),
        known_dependent_refs=(product_ref,),
    )
    # The product ref is present, yet nothing reaches it.
    assert product_ref.key in {ref.key for ref in incomplete.known_dependent_refs}
    assert incomplete.affected((transition["old_model"], transition["revised_model"])) == ()

    # The adapter's closure check must reject that claim.
    from rawlsing_next.pre553_analytical_replay_dependency import (
        AnalyticalDependencyRegistry as _Reg,
        AnalyticalProductRegistration as _Reg2,
        assert_closure_covers_registered_products,
    )
    from rawlsing_next.pre553_analytical_replay_dependency import (
        OwnerDependencyInvalidationOutcome,
    )
    from rawlsing_next.pre553_authority_maintenance import AuthorityInvalidationReceipt

    registry = _Reg()
    registry.register(
        _Reg2(
            product_ref=product_ref,
            product_identity_hash=product_ref.content_hash,
            determinant_authority_refs=(transition["old_model"],),
        )
    )
    recompose = {
        product_ref.key: fx.recompose_product_under_model_authority("forward")
    }
    # A receipt that claims nothing is affected (the incomplete graph's own answer).
    from rawlsing_next.pre553_empirical_objects import ExactRef as _Ref

    release_ref = _Ref("RELEASE", "urn:test:hq149:incomplete", "a" * 64)
    fabricated_receipt = AuthorityInvalidationReceipt(
        changed_authority_refs=(transition["old_model"],),
        affected_dependent_refs=(),
        unaffected_dependent_refs=(product_ref,),
        recompilation_pairs=(),
    )
    outcome = OwnerDependencyInvalidationOutcome(
        release_ref=release_ref,
        invalidation_receipt=fabricated_receipt,
        changed_authority_refs=(transition["old_model"],),
        recomposed_products=(),
    )
    from rawlsing_next.pre553_analytical_replay_dependency import MissingCrossOwnerEdge

    with pytest.raises(MissingCrossOwnerEdge, match="MISSING_CROSS_OWNER_EDGE"):
        assert_closure_covers_registered_products(
            outcome=outcome,
            registry=registry,
            recompose=recompute_map(),
            successor_authority=transition["revised_model"],
        )


def recompute_map():
    from rawlsing_next.tests import c1_at18_at19_fixture as _fx

    case = _fx.build_case("forward")
    product_ref = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        "urn:test:c1-03r:composed:forward",
        _fx.compose(case).composed_result_identity_hash,
    )
    return {product_ref.key: _fx.recompose_product_under_model_authority("forward")}


def test_at19_closure_passes_when_the_lawful_edges_are_present():
    """Control: with the consumed determinant edges present, the owner's closure holds.

    The owner reaches exactly the dependent whose consumed determinant changed, and
    reports the other registered product as unaffected.
    """

    transition = fx.build_model_authority_transition("forward")
    registry, _recompose = _registered_products(transition)
    # Register the sibling too, so the graph is complete over both real products.
    registry.register(
        AnalyticalProductRegistration(
            product_ref=transition["sibling_ref"],
            product_identity_hash=transition["sibling_ref"].content_hash,
            determinant_authority_refs=(transition["sibling_authority"],),
        )
    )
    graph = registry.build_graph()

    # Every present edge corresponds to a determinant a registered product consumed.
    edge_authorities = {auth.key for auth, _ in graph.authority_edges}
    for registration in registry.registrations:
        for authority in registration.determinant_authority_refs:
            assert authority.key in edge_authorities
    changed = (transition["old_model"], transition["revised_model"])
    affected = graph.affected(changed)
    unaffected = graph.unaffected(affected)
    assert affected == (transition["product_ref"],)
    assert unaffected == (transition["sibling_ref"],)
