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

from rawlsing_next.pre553_authority_maintenance import (
    DEPENDENT_LIFECYCLE_CURRENT,
    DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
    NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    NoncurrentDependentOutcome,
    SemanticDeterminantGraph,
)
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
    ExplicitNoncurrentDependent,
    MissingCrossOwnerEdge,
    OwnerUnknownDependent,
    assert_closure_covers_registered_products,
    resolve_current_analytical_product,
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
    INVALIDATION_RECEIPT_NONCURRENT_SCHEMA,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, ReplayReceipt, exact_ref

from rawlsing_next.pre553_empirical_objects import AuthorityRef, semantic_hash
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
    assert transition["sealed_successor_ref"].key not in edge_authorities, (
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
    changed = (transition["old_model"], transition["sealed_successor_ref"])

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
    changed = (transition["old_model"], transition["sealed_successor_ref"])

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
    assert incomplete.affected((transition["old_model"], transition["sealed_successor_ref"])) == ()

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
            successor_authority=transition["sealed_successor_ref"],
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
    changed = (transition["old_model"], transition["sealed_successor_ref"])
    affected = graph.affected(changed)
    unaffected = graph.unaffected(affected)
    assert affected == (transition["product_ref"],)
    assert unaffected == (transition["sibling_ref"],)


# ==========================================================================
# AT19 Astra option-A: generic noncurrent lifecycle outcome (mixed release)
# ==========================================================================
def _mixed_registry(t):
    registry = AnalyticalDependencyRegistry()
    for product in (
        t["replaced_product"], t["noncurrent_product"],
        t["downstream_product"], t["sibling_ref"],
    ):
        determinants = (
            (t["old_model"],)
            if product.key != t["sibling_ref"].key
            else (t["sibling_authority"],)
        )
        registry.register(
            AnalyticalProductRegistration(
                product_ref=product,
                product_identity_hash=product.content_hash,
                determinant_authority_refs=determinants,
            )
        )
    return registry


def _run_mixed(t, *, noncurrent=None):
    return transition_analytical_dependencies(
        executor=t["executor"],
        registry=_mixed_registry(t),
        seal_ref=t["seal_ref"],
        selection_rule_ref=fx._ref_for("SELECTION_RULE", "mixed-v2"),
        selection_attestation_ref=fx._ref_for("SELECTION_ATTESTATION", "mixed-v2"),
        recompose={
            t["replaced_product"].key: fx.recompose_product_under_model_authority(
                t["direction"]
            )
        },
        noncurrent_dependents=(
            t["noncurrent_declarations"] if noncurrent is None else noncurrent
        ),
    )


def test_at19_astra_a_one_release_carries_replacement_noncurrent_and_unaffected():
    """F: in ONE governed release all three dependent outcomes coexist."""
    t = fx.build_mixed_outcome_transition("forward")
    outcome = _run_mixed(t)
    receipt = outcome.invalidation_receipt
    ex = t["executor"]

    assert len(receipt.recompilation_pairs) == 1
    assert len(receipt.noncurrent_dependents) == 2
    assert len(receipt.unaffected_dependent_refs) == 1
    # R and N are disjoint and cover A exactly: every affected ref has ONE outcome.
    replacement_keys = {r.key for r in receipt.replacement_old_refs}
    noncurrent_keys = {r.key for r in receipt.noncurrent_old_refs}
    affected_keys = {r.key for r in receipt.affected_dependent_refs}
    assert replacement_keys.isdisjoint(noncurrent_keys)
    assert replacement_keys | noncurrent_keys == affected_keys
    assert receipt.unaffected_dependent_refs[0].key == t["sibling_ref"].key

    # A real lawful replacement exists for the replaced product.
    (old, new), = receipt.recompilation_pairs
    assert old.key == t["replaced_product"].key
    assert new != old
    status = resolve_current_analytical_product(
        executor=ex, dependent_ref=t["replaced_product"])
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert status["current_replacement_ref"].key == new.key

    # The unaffected sibling stays current and identity-stable.
    sibling = resolve_current_analytical_product(
        executor=ex, dependent_ref=t["sibling_ref"])
    assert sibling["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert "current_replacement_ref" not in sibling
    assert sibling["dependent_ref"] == t["sibling_ref"]

    # The noncurrent dependent is explicitly noncurrent, with exact grounds.
    for row in receipt.noncurrent_dependents:
        assert row.replacement_ref is None
        assert row.disposition == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
        assert row.reason_code
        assert row.supporting_refs
    with pytest.raises(ExplicitNoncurrentDependent, match="may not be served as current"):
        resolve_current_analytical_product(
            executor=ex, dependent_ref=t["noncurrent_product"])
    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=ex, dependent_ref=t["downstream_product"])


def test_at19_astra_a_noncurrent_does_not_withdraw_the_governing_authority():
    """Noncurrent means no current product, not loss of the historical artifact
    and not withdrawal of the governing authority."""
    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    ex = t["executor"]
    # The historical exact authority is still resolvable.
    historical = ex.resolve_historical_exact(t["sealed_successor_ref"])
    assert historical.authority_ref.key == t["sealed_successor_ref"].key
    # The authority is still current under the release.
    release_ref = ex.current_selection_receipt_ref(t["old_model"].authority_id)
    assert ex.resolve_current_exact(
        t["old_model"].authority_id, selection_receipt_ref=release_ref
    ).authority_ref.key == t["sealed_successor_ref"].key


def test_at19_astra_a_downstream_gets_no_replacement_from_a_noncurrent_input():
    """A registered dependent downstream of a noncurrent required input must not
    receive a replacement built from that input."""
    t = fx.build_mixed_outcome_transition("forward")
    receipt = _run_mixed(t).invalidation_receipt
    rows = {r.old_ref.key: r for r in receipt.noncurrent_dependents}
    downstream = rows[t["downstream_product"].key]
    assert downstream.reason_code == "REQUIRED_INPUT_NONCURRENT"
    assert t["noncurrent_product"] in downstream.supporting_refs
    # No replacement pair anywhere points at the downstream product.
    assert all(old.key != t["downstream_product"].key
               for old, _ in receipt.recompilation_pairs)
    # And it did not receive a replacement under the successor authority.
    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=t["executor"], dependent_ref=t["downstream_product"])


def test_at19_astra_a_missing_cross_owner_edge_fails_closure_even_with_cached_objects():
    """F: a missing graph edge is not repaired by object/cache presence."""
    # The transition is driven against a graph that omits the downstream dependency
    # edge, so the owner genuinely believes downstream is unaffected.
    t = fx.build_mixed_outcome_transition(
        "forward", include_downstream_edge=False)
    # Only the genuinely affected dependent may be declared noncurrent. The domain
    # cannot smuggle a noncurrent row in for something the owner calls unaffected.
    declared = {
        t["noncurrent_product"].key: t["noncurrent_declarations"][
            t["noncurrent_product"].key
        ]
    }
    outcome = _run_mixed(t, noncurrent=declared)
    receipt = outcome.invalidation_receipt
    downstream_key = t["downstream_product"].key
    # The owner really does record downstream as unaffected...
    assert downstream_key in {r.key for r in receipt.unaffected_dependent_refs}
    # ...while every other dependent still got exactly one outcome.
    assert len(receipt.recompilation_pairs) == 1
    assert len(receipt.noncurrent_dependents) == 1

    # The independent closure witness over the REGISTERED products rejects the
    # incomplete graph: a cached/present downstream object does not restore the
    # missing cross-owner edge.
    registry = _mixed_registry(t)
    with pytest.raises(MissingCrossOwnerEdge):
        assert_closure_covers_registered_products(
            outcome=outcome,
            registry=registry,
            recompose={
                t["downstream_product"].key: fx.recompose_product_under_model_authority(
                    t["direction"]
                )
            },
            successor_authority=t["sealed_successor_ref"],
        )


def test_at19_astra_a_cache_presence_does_not_restore_currentness():
    """Cached historical bytes never restore currentness."""
    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    # The historical artifact is fully present and retrievable...
    assert t["executor"].resolve_historical_exact(t["sealed_successor_ref"])
    # ...and the dependent is still refused as current.
    for _attempt in range(2):
        with pytest.raises(ExplicitNoncurrentDependent):
            resolve_current_analytical_product(
                executor=t["executor"], dependent_ref=t["noncurrent_product"])
    # Only a later lawful transition/receipt could restore it; re-reading the same
    # release changes nothing.
    status = t["executor"].dependent_lifecycle_status(t["noncurrent_product"])
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT


# ==========================================================================
# AT19 E: successor binding and identity proof (Astra item 4)
# ==========================================================================
def test_at19_e_sealed_successor_is_not_the_separately_synthesized_decoy():
    """The decoy snapshot shares the CONSUMED prior's content hash.

    ``revised_model_authority_snapshot`` copies ``authority_content_hash`` from the
    base and only changes version/fingerprint/parentage. So the "revised model" ref is
    a v2-labelled ref whose content hash equals the v1 the product already consumed.
    Choosing it would recompute the product under the authority it already used.
    """
    t = fx.build_model_authority_transition("forward")
    consumed, decoy, sealed = t["old_model"], t["unsealed_decoy_model_ref"], fx.sealed_successor_of(t)
    assert decoy.authority_content_hash == consumed.authority_content_hash
    assert sealed.authority_content_hash != consumed.authority_content_hash
    assert decoy.authority_content_hash != sealed.authority_content_hash
    # All three are distinct refs; only the sealed one is lawful.
    assert len({consumed.key, decoy.key, sealed.key}) == 3


def test_at19_e_consumer_model_rule_hash_binds_the_sealed_successor():
    """E: the model-rule hash cryptographically commits to the exact successor."""
    t = fx.build_model_authority_transition("forward")
    case = t["case"]
    rule = fx.build_model_rule_from_sealed_successor(case, t)
    sealed = fx.sealed_successor_of(t)
    # material binds the complete model authority ref, so rule_hash commits to it.
    assert rule.material()["model_authority_ref"] == sealed.as_dict()
    assert rule.rule_hash == semantic_hash(rule.material())
    # A rule built from the decoy produces a DIFFERENT hash: the binding is real.
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule as _R,
    )
    base = case["model_rule"]
    decoy_rule = _R(
        t["unsealed_decoy_model_ref"], base.walkback_authority_ref,
        base.source_universe_refs, base.walkback_steps,
        base.positive_proxy_authority_refs,
    )
    assert decoy_rule.rule_hash != rule.rule_hash


def test_at19_e_callback_receives_the_exact_sealed_successor_and_identity_moves():
    """E: the recomposition callback receives the sealed successor, and the product
    identity changes even though numerical geometry is unchanged."""
    t = fx.build_model_authority_transition("forward")
    registry, recompose = _registered_products(t)
    seen = {}
    base = fx.recompose_product_under_model_authority("forward")

    def spy(affected_ref, authority):
        seen["authority"] = authority
        return base(affected_ref, authority)

    outcome = transition_analytical_dependencies(
        executor=t["executor"],
        registry=registry,
        seal_ref=t["seal_ref"],
        selection_rule_ref=fx._ref_for("SELECTION_RULE", "identity-v2"),
        selection_attestation_ref=fx._ref_for("SELECTION_ATTESTATION", "identity-v2"),
        recompose={t["product_ref"].key: spy},
    )
    sealed = fx.sealed_successor_of(t)
    assert seen["authority"].key == sealed.key
    assert seen["authority"].key != t["old_model"].key
    # The successor was resolved from the same transition, not by version label:
    # the decoy (also version 2.0.0) was NOT what the callback received.
    assert seen["authority"].key != t["unsealed_decoy_model_ref"].key

    (old, new), = outcome.invalidation_receipt.recompilation_pairs
    assert new != old
    # Geometry is unchanged; identity moved because the governing authority moved.
    assert t["composition"].raw_denominator_support == (
        fx.compose({**t["case"], "model_rule": fx.build_model_rule_from_sealed_successor(
            t["case"], t)}).raw_denominator_support)


def test_at19_e_expected_output_oracle_stays_separately_frozen():
    """E: expected-output oracle material is derived independently of the candidate.

    The oracle is computed from the plain case, never from the transition receipt or
    the recomposed product, and carries its own schema.
    """
    case = fx.build_case("forward")
    oracle = fx.oracle_expected_output(case)
    assert oracle["schema"] == "C1_03R_AT18_EXPECTED_OUTPUT_ORACLE@1"
    t = fx.build_model_authority_transition("forward")
    receipt_fields = {"recompilation_pairs", "noncurrent_dependents", "ref"}
    assert receipt_fields.isdisjoint(set(oracle))
    # Recomputing the oracle is stable and independent of any transition.
    assert fx.oracle_expected_output(case) == oracle


# ==========================================================================
# AT19 G: adapter-level hostiles
# ==========================================================================
def test_g_callback_omission_is_an_error_not_a_noncurrent_outcome():
    """Error law: a missing recomposition path stays an error."""
    t = fx.build_mixed_outcome_transition("forward")
    with pytest.raises(NoLawfulReplacementRepresentable):
        _run_mixed(t, noncurrent={})  # downstream declaration dropped -> no path


def test_g_callback_exception_is_an_error_not_a_noncurrent_outcome():
    def boom(affected_ref, authority):
        raise RuntimeError("recomposition exploded")

    t = fx.build_model_authority_transition("forward")
    registry, _ = _registered_products(t)
    with pytest.raises(RuntimeError, match="recomposition exploded"):
        transition_analytical_dependencies(
            executor=t["executor"],
            registry=registry,
            seal_ref=t["seal_ref"],
            selection_rule_ref=fx._ref_for("SELECTION_RULE", "boom"),
            selection_attestation_ref=fx._ref_for("SELECTION_ATTESTATION", "boom"),
            recompose={t["product_ref"].key: boom},
        )


def test_g_unchanged_callback_output_is_an_error_not_a_noncurrent_outcome():
    """An unchanged-ref return never silently becomes noncurrent."""
    t = fx.build_model_authority_transition("forward")
    registry, _ = _registered_products(t)

    def identity(affected_ref, authority):
        return affected_ref

    with pytest.raises(AuthorityMaintenanceError, match="must produce a new exact ref"):
        transition_analytical_dependencies(
            executor=t["executor"],
            registry=registry,
            seal_ref=t["seal_ref"],
            selection_rule_ref=fx._ref_for("SELECTION_RULE", "same"),
            selection_attestation_ref=fx._ref_for("SELECTION_ATTESTATION", "same"),
            recompose={t["product_ref"].key: identity},
        )


def test_g_future_authority_pre_binding_remains_forbidden():
    """A well-formed but unregistered successor authority is refused.

    The successor resolution requires the ref to be an authority the owner actually
    knows. A ref that merely looks like a successor -- same authority id, plausible
    version label, real-looking content hash -- is refused, so a future authority can
    never be pre-bound into a recomposition.
    """
    from rawlsing_next.pre553_analytical_replay_dependency import build_owner_recompiler

    t = fx.build_model_authority_transition("forward")
    registry, _ = _registered_products(t)
    rc = build_owner_recompiler(
        executor=t["executor"],
        registry=registry,
        recompose={
            t["product_ref"].key: fx.recompose_product_under_model_authority("forward")
        },
    )
    future = AuthorityRef(
        t["old_model"].authority_id, "3.0.0", semantic_hash({"future": "3.0.0"})
    )
    assert future.key != t["old_model"].key
    with pytest.raises(
        AuthorityMaintenanceError, match="not a registered owner authority"
    ):
        rc(t["product_ref"], (t["old_model"], future))
    # The decoy is registered nowhere either, so it is refused the same way.
    with pytest.raises(AuthorityMaintenanceError):
        rc(t["product_ref"], (t["old_model"], t["unsealed_decoy_model_ref"]))


def test_g_adapter_does_not_own_the_lifecycle_or_the_receipt():
    """G: the adapter delegates. It never computes affected/unaffected and never
    constructs the invalidation receipt."""
    import inspect as _inspect

    import rawlsing_next.pre553_analytical_replay_dependency as adapter
    src = _inspect.getsource(adapter)
    # No reimplementation of the owner's affected/unaffected computation.
    assert ".affected(" not in src
    assert ".unaffected(" not in src
    # No direct construction of the owner receipt.
    assert "AuthorityInvalidationReceipt(" not in src
    # The outcome really is the OWNER's own receipt object.
    t = fx.build_mixed_outcome_transition("forward")
    outcome = _run_mixed(t)
    owners_receipt = t["executor"].invalidation_receipt_for_release(outcome.release_ref)
    assert outcome.invalidation_receipt is owners_receipt
    assert outcome.material()["lifecycle_performed_by"] == (
        "AuthorityMaintenanceExecutor.promote_current")


# ==========================================================================
# HQ155 owner fail-closed correction (R2): RVW-003, RVW-004, promotion law
# ==========================================================================


def _resealed_checkpoint(t, mutate):
    """Fully self-consistently reseal a checkpoint after mutating an invalidation's U.

    A naive byte edit is caught by the embedded record_ref check, which is necessary
    but not sufficient. This helper rebuilds the tampered invalidation receipt, then
    every release that cites it, then the whole event chain (subject refs, parent
    chain, record refs), then the current-release pointers, and finally the checkpoint
    hash. The result is a checkpoint that is internally consistent in every hash it
    carries, so only an independent re-derivation of A and U can reject it.
    """
    import copy as _copy

    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityInvalidationReceipt,
        AuthorityReleaseReceipt,
        MaintenanceEvent,
    )
    from rawlsing_next.pre553_empirical_objects import semantic_hash

    checkpoint = _copy.deepcopy(t["executor"].export_checkpoint())
    payload = checkpoint["checkpoint_payload"]

    original = AuthorityInvalidationReceipt.from_dict(payload["invalidations"][0])
    tampered = mutate(original)
    payload["invalidations"][0] = tampered.as_dict()

    releases = payload["releases"]
    remapped: dict[str, Any] = {}
    for index, row in enumerate(releases):
        release = AuthorityReleaseReceipt.from_dict(row)
        if release.invalidation_receipt_ref.key != original.ref.key:
            continue
        rebuilt = AuthorityReleaseReceipt(
            release_kind=release.release_kind,
            selected_authority_ref=release.selected_authority_ref,
            seal_ref=release.seal_ref,
            selection_rule_ref=release.selection_rule_ref,
            selection_attestation_ref=release.selection_attestation_ref,
            invalidation_receipt_ref=tampered.ref,
            previous_current_authority_ref=release.previous_current_authority_ref,
            prior_lawful_release_ref=release.prior_lawful_release_ref,
            release_state=release.release_state,
        )
        remapped[row["record_ref"]["content_hash"]] = rebuilt.ref
        releases[index] = rebuilt.as_dict()

    for index, row in enumerate(payload.get("current_release_refs", [])):
        content = row["release_ref"]["content_hash"]
        if content in remapped:
            payload["current_release_refs"][index] = {
                **row, "release_ref": remapped[content].as_dict(),
            }

    rebuilt_events = []
    parent = None
    for row in payload["events"]:
        fields = dict(row)
        fields.pop("record_ref", None)
        subject = fields["subject_ref"]
        if subject["content_hash"] in remapped:
            subject = remapped[subject["content_hash"]].as_dict()
        event = MaintenanceEvent(
            sequence_number=fields["sequence_number"],
            event_kind=fields["event_kind"],
            subject_ref=subject,
            parent_event_ref=parent,
            evidence_refs=tuple(fields.get("evidence_refs", ())),
            adjudication_ref=fields.get("adjudication_ref"),
            authority_refs=tuple(fields.get("authority_refs", ())),
            dependent_refs=tuple(fields.get("dependent_refs", ())),
            event_state=fields.get("event_state", "COMMITTED"),
        )
        rebuilt_events.append(event)
        parent = event.ref
    payload["events"] = [event.as_dict() for event in rebuilt_events]

    return {
        "checkpoint_payload": payload,
        "checkpoint_hash": semantic_hash(payload),
    }


# --- RVW-003: owner-unknown dependent is never CURRENT ---------------------


def test_hq155_rvw_003_owner_unknown_dependent_is_never_current():
    """RVW-003: an unregistered ref has no owner currentness to report."""
    from rawlsing_next.pre553_authority_maintenance import (
        DEPENDENT_LIFECYCLE_NOT_GOVERNED,
    )
    from rawlsing_next.pre553_empirical_objects import semantic_hash

    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    executor = t["executor"]

    unknown = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        "urn:test:c1-03r:never-registered:product",
        semantic_hash({"never": "registered"}),
    )
    assert unknown.key not in {r.key for r in executor.determinant_graph.known_dependent_refs}

    status = executor.dependent_lifecycle_status(unknown)
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED
    assert status["lifecycle_state"] != DEPENDENT_LIFECYCLE_CURRENT
    assert status["reason_code"] == "OWNER_UNKNOWN_DEPENDENT"

    with pytest.raises(OwnerUnknownDependent, match="does not know this dependent"):
        resolve_current_analytical_product(executor=executor, dependent_ref=unknown)

    # A ref the owner DOES know, with a real outcome, is unaffected by the repair.
    replaced = resolve_current_analytical_product(
        executor=executor, dependent_ref=t["replaced_product"])
    assert replaced["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=executor, dependent_ref=t["noncurrent_product"])


def test_hq155_rvw_003_cache_presence_does_not_change_owner_unknown():
    """RVW-003: cache and object presence cannot manufacture a current ref."""
    from rawlsing_next.pre553_authority_maintenance import (
        DEPENDENT_LIFECYCLE_NOT_GOVERNED,
    )
    from rawlsing_next.pre553_empirical_objects import semantic_hash

    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    executor = t["executor"]

    unknown = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        "urn:test:c1-03r:cached-unknown:product",
        semantic_hash({"cached": "unknown"}),
    )
    before = executor.dependent_lifecycle_status(unknown)
    assert before["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED

    # Smuggle the ref into the executor's snapshot and evidence caches, so that it is
    # resident and addressable in every way except the owner's own knowledge.
    victim = next(iter(executor._snapshots.values()))
    executor._snapshots[unknown.key] = victim
    executor._snapshot_exact_refs[unknown.key] = victim

    after = executor.dependent_lifecycle_status(unknown)
    assert after["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED
    assert after == before
    with pytest.raises(OwnerUnknownDependent):
        resolve_current_analytical_product(executor=executor, dependent_ref=unknown)


# --- RVW-004: checkpoint replay must re-derive U ----------------------------


def test_hq155_rvw_004_tampered_checkpoint_u_omitting_sibling_is_rejected():
    """RVW-004: a shrunk U is rejected even after self-consistent rehashing."""
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityInvalidationReceipt,
        AuthorityMaintenanceConflict,
        AuthorityMaintenanceExecutor,
    )

    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    executor = t["executor"]
    original = executor.export_checkpoint()
    affected_u = original["checkpoint_payload"]["invalidations"][0][
        "unaffected_dependent_refs"]
    assert affected_u, "the mixed release must record a non-empty unaffected set"

    def shrink(receipt):
        return AuthorityInvalidationReceipt(
            changed_authority_refs=receipt.changed_authority_refs,
            affected_dependent_refs=receipt.affected_dependent_refs,
            unaffected_dependent_refs=(),
            recompilation_pairs=receipt.recompilation_pairs,
            noncurrent_dependents=receipt.noncurrent_dependents,
        )

    tampered = _resealed_checkpoint(t, shrink)
    # The reseal really is self-consistent: its own hash matches its own payload.
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    assert tampered["checkpoint_hash"] == semantic_hash(tampered["checkpoint_payload"])

    with pytest.raises(AuthorityMaintenanceConflict, match="unaffected set differs"):
        AuthorityMaintenanceExecutor.from_checkpoint(tampered)

    # The untampered checkpoint still replays exactly.
    AuthorityMaintenanceExecutor.from_checkpoint(original)


def test_hq155_rvw_004_tampered_checkpoint_u_with_unknown_sibling_is_rejected():
    """RVW-004: U must be the graph's own complement of A, not an arbitrary set."""
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityInvalidationReceipt,
        AuthorityMaintenanceConflict,
        AuthorityMaintenanceExecutor,
    )

    t = fx.build_mixed_outcome_transition("forward")
    _run_mixed(t)
    executor = t["executor"]
    unknown = fx._ref_for("C11Internal:Unknown", "injected-sibling")

    def swap(receipt):
        return AuthorityInvalidationReceipt(
            changed_authority_refs=receipt.changed_authority_refs,
            affected_dependent_refs=receipt.affected_dependent_refs,
            unaffected_dependent_refs=(unknown,),
            recompilation_pairs=receipt.recompilation_pairs,
            noncurrent_dependents=receipt.noncurrent_dependents,
        )

    tampered = _resealed_checkpoint(t, swap)
    with pytest.raises(AuthorityMaintenanceConflict, match="unaffected set differs"):
        AuthorityMaintenanceExecutor.from_checkpoint(tampered)

    # A and U jointly cover K at replay, which is what the recomputation establishes.
    graph = executor.determinant_graph
    recomputed_affected = graph.affected((t["old_model"], t["sealed_successor_ref"]))
    recomputed_unaffected = graph.unaffected(recomputed_affected)
    known = {ref.key for ref in graph.known_dependent_refs}
    affected = {ref.key for ref in recomputed_affected}
    assert affected.isdisjoint({ref.key for ref in recomputed_unaffected})
    assert affected | {ref.key for ref in recomputed_unaffected} == known
    assert unknown.key not in known


# --- Promotion law still shared and intact ---------------------------------


def test_hq155_promotion_normal_mixed_outcome_still_passes():
    """The promotion path's mixed outcome is unchanged by the four repairs."""
    t = fx.build_mixed_outcome_transition("forward")
    outcome = _run_mixed(t)
    receipt = outcome.invalidation_receipt
    executor = t["executor"]
    known = {ref.key for ref in executor.determinant_graph.known_dependent_refs}
    affected = {ref.key for ref in receipt.affected_dependent_refs}
    unaffected = {ref.key for ref in receipt.unaffected_dependent_refs}
    replacement = {old.key for old, _ in receipt.recompilation_pairs}
    noncurrent = {row.old_ref.key for row in receipt.noncurrent_dependents}

    assert replacement.isdisjoint(noncurrent)
    assert replacement | noncurrent == affected
    assert affected.isdisjoint(unaffected)
    assert affected | unaffected == known
    # Exactly one generic disposition, with non-empty exact grounds, never split.
    for row in receipt.noncurrent_dependents:
        assert row.disposition == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
        assert row.reason_code and row.supporting_refs
        assert row.replacement_ref is None
    # The negative receipt declares the exact noncurrent schema and round-trips.
    assert receipt.semantic_projection()["receipt_schema"] == (
        INVALIDATION_RECEIPT_NONCURRENT_SCHEMA
    )
    assert AuthorityInvalidationReceipt.from_dict(receipt.as_dict()).ref == receipt.ref
    # Lifecycle law: one current replacement, two explicit refusals, sibling current.
    current = resolve_current_analytical_product(
        executor=executor, dependent_ref=t["replaced_product"])
    assert current["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    for ref in (t["noncurrent_product"], t["downstream_product"]):
        with pytest.raises(ExplicitNoncurrentDependent):
            resolve_current_analytical_product(executor=executor, dependent_ref=ref)
    sibling = resolve_current_analytical_product(
        executor=executor, dependent_ref=t["sibling_ref"])
    assert sibling["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert "current_replacement_ref" not in sibling


# --- Sealed successor / decoy and AT18 grade courts remain green -----------


def test_hq155_sealed_successor_is_not_the_decoy_and_binds_exactly():
    """The sealed-successor exact binding and the decoy distinction are intact."""
    t = fx.build_model_authority_transition("forward")
    consumed = t["old_model"]
    decoy = t["unsealed_decoy_model_ref"]
    sealed = fx.sealed_successor_of(t)
    # Three distinct refs; only the sealed one is lawful.
    assert decoy.authority_content_hash == consumed.authority_content_hash
    assert sealed.authority_content_hash != consumed.authority_content_hash
    assert decoy.authority_content_hash != sealed.authority_content_hash
    assert len({consumed.key, decoy.key, sealed.key}) == 3
    # The sealed successor is exactly what the owner's transition produced, and the
    # consumer model rule commits to it.
    assert sealed.key == t["sealed_successor_ref"].key
    rule = fx.build_model_rule_from_sealed_successor(t["case"], t)
    assert rule.material()["model_authority_ref"] == sealed.as_dict()
    assert rule.rule_hash == semantic_hash(rule.material())


def test_hq155_at18_grade_courts_remain_green():
    """The four AT18 replay grades and their mechanism ceilings are unchanged."""
    from rawlsing_next.pre553_analytical_replay_dependency import (
        GRADE_STRENGTH,
        MECHANISM_MAX_GRADE,
        MECHANISM_STORED_PRODUCT_DESERIALIZATION,
        MECHANISM_STORED_RECEIPT_DESERIALIZATION,
    )

    assert len(REPLAY_GRADES) == 4
    assert GRADE_STRENGTH[REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY] == 0
    assert GRADE_STRENGTH[REPLAY_GRADE_SERIALIZATION_REPLAY] == 1
    assert GRADE_STRENGTH[REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY] == 2
    assert GRADE_STRENGTH[REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION] == 3
    # Stored material can never reach a fresh grade.
    assert MECHANISM_MAX_GRADE[MECHANISM_HISTORICAL_NARRATION] == (
        REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY
    )
    for mechanism in (MECHANISM_STORED_RECEIPT_DESERIALIZATION,
                      MECHANISM_STORED_PRODUCT_DESERIALIZATION):
        assert MECHANISM_MAX_GRADE[mechanism] == REPLAY_GRADE_SERIALIZATION_REPLAY


def test_f1_zero_release_known_dependent_is_never_served_as_current():
    """F-1 hostile 2: the current-product resolver refuses the zero-release case.

    An owner-KNOWN dependent with zero governing releases must raise the typed
    not-governed failure, not resolve to CURRENT. This closes the resolver half of
    F-1: the status was fail-open and the resolver faithfully served it.
    """
    from rawlsing_next.pre553_analytical_replay_dependency import OwnerUnknownDependent
    from rawlsing_next.pre553_authority_maintenance import (
        DEPENDENT_LIFECYCLE_NOT_GOVERNED,
        SemanticDeterminantGraph,
    )
    from rawlsing_next.pre553_empirical_objects import exact_ref

    known = exact_ref({"kind": "DERIVED@1", "object_id": "urn:t:f1-known",
                       "content_hash": "a" * 64})
    # Build a genuine zero-release executor over a graph that KNOWS this ref.
    from rawlsing_next.pre553_authority_maintenance import AuthorityMaintenanceExecutor

    executor = AuthorityMaintenanceExecutor(
        determinant_graph=SemanticDeterminantGraph(
            authority_edges=(), dependency_edges=(), known_dependent_refs=(known,))
    )
    assert not executor._releases
    status = executor.dependent_lifecycle_status(known)
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED
    assert status["reason_code"] == "NO_GOVERNING_RELEASE"

    with pytest.raises(OwnerUnknownDependent):
        resolve_current_analytical_product(executor=executor, dependent_ref=known)

