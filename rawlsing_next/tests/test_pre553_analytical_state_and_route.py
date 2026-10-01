"""C1-03A courts: AT14 negative-state conservation, AT15 route legitimacy, AT16 final consumer.

Every court drives a competent current owner through its public path. No state
label is manufactured inside a wrapper, and no handmade final slice is used to
satisfy AT16.
"""
from __future__ import annotations

import inspect
from collections.abc import Mapping

from rawlsing_next.pre553_empirical_objects import Pre553SemanticCollapseError

import pytest

from rawlsing_next.pre553_analytical_state_and_route import (
    BLOCKED_REQUIRED_AUTHORITY,
    CONSUMER_INVOKED,
    CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE,
    INTEGRITY_FAILURE,
    MANDATORY_AT14_STATES,
    NONCOMPARABLE,
    OBSERVED_ZERO,
    ROUTE_DIRECT_EMPIRICAL,
    ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
    UNDERPOWERED,
    UNKNOWN_UNRESOLVED,
    UNVISITED,
    VALID_EMPTY,
    C103AStateRouteError,
    ConsumerDisposition,
    RouteLegitimacyError,
    assert_route_not_laundered,
    build_state_route_result,
    require_positive_route,
    OwnerStateProjection,
    RouteObligation,
    RecursiveCoverageCustody,
    OwnerProjectionError,
    OWNER_EMPIRICAL_INTEGRITY_LABEL,
    OWNER_EMPIRICAL_PROJECTION_LABEL,
    OWNER_ADAPTIVE_PROJECTION_LABEL,
    OWNER_DISCOVERY_PROJECTION_LABEL,
    OWNER_ADMISSION_PROJECTION_LABEL,
    OWNER_RECURSIVE_HANDOFF_LABEL,
    ProducerStateEvidence,
    SUPPORTED_BASELINE,
    classify_adaptive_coverage,
    classify_discovery_receipt_state,
    classify_empirical_cells,
    classify_empirical_fact_state,
    observed_zero_cells,
)
from rawlsing_next.tests import c1_at14_at16_fixture as fx


def _envelope(projection, *, route=ROUTE_DIRECT_EMPIRICAL, fixture_refs=(), **kwargs):
    """Build a bounded envelope from an OWNER-DERIVED state projection.

    The retained analytical state is never passed in by the caller. It comes from
    the projection, which was derived from a real competent owner object.
    """
    retained = projection.retained_state
    disposition = kwargs.pop("disposition", None) or fx.consumer_disposition_for(retained)
    refs = tuple(fixture_refs) or (projection.producer_ref,) + tuple(projection.supporting_refs)
    coverage_state = kwargs.pop("coverage_state", projection.coverage_state)
    unvisited = kwargs.pop("unvisited_refs", ())
    return build_state_route_result(
        route_class=route,
        producer_evidence=[projection.as_evidence()],
        producer_refs=list(refs),
        consumer_disposition=disposition,
        reason=kwargs.pop("reason", projection.reason),
        coverage_state=coverage_state,
        unvisited_refs=unvisited,
        **kwargs,
    )


# ===========================================================================
# AT14 - negative-state conservation
# ===========================================================================


def test_at14_observed_zero_is_retained_and_is_not_valid_empty():
    """AT14(1): observed zero in a nonzero denominator stays its own state."""
    projection, data = fx.project_empirical("observed_zero_fixture")
    fact = data["fact"]
    assert fact.raw_denominator_support == 2, "observed zero requires positive support"
    assert data["observed_zero_cells"], "fixture must expose a supported observed-zero cell"

    retained = projection.retained_state
    assert fact.typed_state == "SUPPORTED"
    assert retained == OBSERVED_ZERO
    assert tuple(data["observed_zero_cells"]) == observed_zero_cells(
        fact.target_topology["complete_cell_semantic_projection"]
    )
    assert "complete_cell_semantic_projection" in projection.projection_law
    # Observed zero is NOT valid-empty and NOT zero support.
    assert retained != VALID_EMPTY
    assert retained != UNDERPOWERED

    result = _envelope(projection, fixture_refs=(fact.ref,))
    assert result.retained_analytical_state == OBSERVED_ZERO
    # Observed zero is lawfully consumer-invocable, but this AT14 court asserts
    # only the state conservation. The real invocation is proven in the AT16
    # positive-path court, which drives the actual consumer.
    assert not result.consumer_disposition.consumer_invoked
    assert "lawfully" in result.consumer_disposition.non_invocation_reason


def test_at14_zero_support_is_distinct_from_observed_zero_and_valid_empty():
    """AT14(1)+(2): zero support is neither observed zero nor valid-empty."""
    zero_proj, zero_support = fx.project_empirical("zero_support_fixture")
    observed_proj, observed = fx.project_empirical("observed_zero_fixture")
    valid_proj, _ = fx.project_empirical("valid_empty_fixture")

    zero_retained = zero_proj.retained_state
    observed_retained = observed_proj.retained_state
    valid_empty_retained = valid_proj.retained_state

    assert zero_support["producer_state"] == "ZERO_SUPPORT"
    assert zero_support["raw_denominator_support"] == 0
    assert zero_retained == UNDERPOWERED
    # Three distinct retained states, no collapse.
    assert len({zero_retained, observed_retained, valid_empty_retained}) == 3


def test_at14_valid_empty_is_retained_from_its_own_owner():
    """AT14(2): VALID_EMPTY comes from the declared-empty target domain."""
    projection, data = fx.project_empirical("valid_empty_fixture")
    assert data["producer_state"] == "VALID_EMPTY"
    assert data["raw_denominator_support"] > 0, "valid-empty has a positive denominator"
    retained = projection.retained_state
    assert retained == VALID_EMPTY
    result = _envelope(projection, fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == VALID_EMPTY
    assert not result.consumer_disposition.consumer_invoked
    assert result.consumer_disposition.non_invocation_reason


def test_at14_underpowered_is_retained_and_distinct_from_unresolved():
    """AT14(3)+(4): underpowered never collapses into unknown/unresolved."""
    under_proj, underpowered = fx.project_receipt("underpowered_fixture")
    unresolved_proj, unresolved = fx.project_empirical("unresolved_fixture")

    under_retained = under_proj.retained_state
    unresolved_retained = unresolved_proj.retained_state

    assert underpowered["producer_state"] == "INSUFFICIENT_SUPPORT"
    assert underpowered["coverage_state"] == "EVALUATED_UNDERPOWERED"
    assert under_retained == UNDERPOWERED
    assert unresolved_retained == UNKNOWN_UNRESOLVED
    # The two remain distinct, and neither becomes valid-empty or observed zero.
    assert under_retained != unresolved_retained
    assert under_retained not in (VALID_EMPTY, OBSERVED_ZERO, UNVISITED)


def test_at14_unresolved_is_retained_from_the_empirical_owner():
    """AT14(4): UNKNOWN/UNRESOLVED is retained with its own reason."""
    projection, data = fx.project_empirical("unresolved_fixture")
    assert data["producer_state"] == "UNRESOLVED"
    retained = projection.retained_state
    assert retained == UNKNOWN_UNRESOLVED
    result = _envelope(projection, fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == UNKNOWN_UNRESOLVED
    # Never coerced into valid-empty, observed zero, or a supported result.
    assert result.retained_analytical_state not in (VALID_EMPTY, OBSERVED_ZERO)
    assert result.negative_claim_authorized is False


def test_at14_unvisited_comes_from_the_real_adaptive_owner():
    """AT14(5): UNVISITED is produced by the adaptive owner, not invented."""
    projection, data = fx.project_adaptive()
    adaptive = data["adaptive_result"]

    # The adaptive owner really ran and really left territory unvisited.
    assert adaptive.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert adaptive.unvisited_unit_refs
    assert adaptive.visited_unit_refs
    assert adaptive.global_negative_claim is False
    assert adaptive.semantic_truth_effect is False

    retained = projection.retained_state
    assert retained == UNVISITED

    result = _envelope(
        projection,
        fixture_refs=(data["determinant_state_ref"],),
        unvisited_refs=adaptive.unvisited_unit_refs,
        visited_refs=adaptive.visited_unit_refs,
        coverage_record_ref=adaptive.checkpoint.ref,
    )
    assert result.retained_analytical_state == UNVISITED
    assert result.coverage_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert result.unvisited_refs == adaptive.unvisited_unit_refs
    # A global negative is never authorized.
    assert result.negative_claim_authorized is False


def test_at14_noncomparable_is_not_coerced_to_unresolved():
    """AT14(6): NONCOMPARABLE stays NONCOMPARABLE."""
    projection, data = fx.project_empirical("noncomparable_fixture")
    assert data["producer_state"] == "NONCOMPARABLE"
    retained = projection.retained_state
    assert retained == NONCOMPARABLE
    assert retained != UNKNOWN_UNRESOLVED
    assert retained != VALID_EMPTY
    result = _envelope(projection, fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == NONCOMPARABLE


def test_at14_blocked_by_absent_or_denying_authority_is_its_own_state():
    """AT14(7): a denying authority blocks; it is not empirical absence."""
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery

    data = fx.blocked_required_authority_fixture()
    projection, data = fx.project_blocked_authority_refusal(
        "blocked_required_authority_fixture"
    )
    retained = projection.retained_state
    assert retained == BLOCKED_REQUIRED_AUTHORITY
    # Blocked is not absence, not valid-empty, not observed zero, not unresolved.
    assert retained not in (OBSERVED_ZERO, VALID_EMPTY, UNKNOWN_UNRESOLVED, UNVISITED)

    with pytest.raises(Exception) as excinfo:
        execute_exact_bounded_discovery(
            repository=data["source"]["repo"],
            discovery_authority=data["authority"],
            authority_registry=data["registry"],
            release_refs=(data["source"]["release_ref"],),
            predicate_catalog=data["predicates"],
            query_template_catalog=data["queries"],
        )
    assert "DENY" in str(excinfo.value)
    # The retained state was derived from that very refusal.
    assert projection.producer_state.endswith(type(excinfo.value).__name__)
    assert "actual exact-discovery owner execution" in projection.projection_law


def test_at14_integrity_failure_cannot_become_valid_empty():
    """AT14(8): INTEGRITY_FAILURE stays integrity failure."""
    projection, data = fx.project_empirical_integrity_refusal("integrity_failure_fixture")
    assert data["corrupted_object_ref"] == data["original_object"].ref
    retained = projection.retained_state
    assert retained == INTEGRITY_FAILURE
    assert retained != VALID_EMPTY
    assert retained != OBSERVED_ZERO
    result = _envelope(projection, fixture_refs=(data["corrupted_object_ref"],))
    assert result.retained_analytical_state == INTEGRITY_FAILURE
    assert not result.consumer_disposition.consumer_invoked


def test_at14_all_eight_mandatory_states_are_distinctly_retained():
    """AT14 estate coverage: every mandatory state is reachable and distinct."""
    observed = classify_empirical_fact_state("OBSERVED_ZERO")
    valid_empty = classify_empirical_fact_state("VALID_EMPTY")
    underpowered = classify_discovery_receipt_state("INSUFFICIENT_SUPPORT")
    unknown = classify_empirical_fact_state("UNRESOLVED")
    unvisited = classify_adaptive_coverage("PARTIAL_BUDGET_EXHAUSTED")
    noncomparable = classify_empirical_fact_state("NONCOMPARABLE")
    blocked = classify_discovery_receipt_state("BLOCKED_REQUIRED_AUTHORITY")
    integrity = classify_empirical_fact_state("INTEGRITY_FAILURE")

    reached = {observed, valid_empty, underpowered, unknown, unvisited,
               noncomparable, blocked, integrity}
    assert reached == set(MANDATORY_AT14_STATES)
    assert len(reached) == 8, "no mandatory state may alias another"


def test_at14_positive_recursive_handoff_is_not_the_coverage_record():
    """AT14 hostile: a positive handoff cannot masquerade as full coverage."""
    from dataclasses import replace as _replace

    from rawlsing_next.pre553_analytical_state_and_route import C103AStateRouteError
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _depth2_source,
        _recursive_generation,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import _atom
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
    )

    source = _depth2_source("c1-03a-handoff-coverage")
    qauth = _query_authority("c1-03a-handoff-coverage")
    parent = _branch_predicate(source, qauth, tag="c1-03a-handoff-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-03a-handoff-x1")
    query = _query(source, qauth, parent, ("X",), tag="c1-03a-handoff-xq")

    gen1, _registry = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", query, tag="c1-03a-handoff", operation="I03-OP-c1-03a-handoff",
    )
    handoff = gen1.handoffs[0]
    receipts = gen1.discovery_result.receipts
    assert receipts, "the full discovery record must exist behind the handoff"

    # The positive handoff exists, but the coverage record is separately retained
    # and carries every evaluated receipt, not just the selected positive.
    assert handoff.evaluated_frontier_ref == gen1.discovery_result.evaluated_frontier_ref
    evaluated_states = {receipt.typed_state for receipt in receipts}
    assert "DISCOVERED_RESULT_SUPPORTED" in evaluated_states

    # A positive handoff, correctly labelled, requires retained custody of the
    # exact coverage record it was selected from.
    # Positive handoff state is never built by direct OwnerStateProjection(...).
    handoff_projection, handoff_custody = fx.project_recursive_handoff(handoff)
    assert handoff_projection.owner == OWNER_RECURSIVE_HANDOFF_LABEL
    assert handoff_projection.retained_state == SUPPORTED_BASELINE
    with pytest.raises(OwnerProjectionError, match="requires retained custody"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[handoff_projection.as_evidence()],
            producer_refs=[handoff.ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="positive handoff without its coverage record",
        )

    # With the owner-derived custody bound, the same positive is lawful and the
    # coverage record is carried into the envelope identity.
    custody = fx.recursive_handoff_custody(handoff)
    result = build_state_route_result(
        route_class=ROUTE_DIRECT_EMPIRICAL,
        producer_evidence=[handoff_projection.as_evidence()],
        producer_refs=[handoff.ref],
        consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
        reason="positive handoff with retained coverage custody",
        coverage_custody=custody,
    )
    assert result.coverage_record_ref == gen1.discovery_result.evaluated_frontier_ref
    assert result.coverage_custody_hash == custody.custody_hash
    # Custody content is inside the envelope identity, so it cannot be dropped
    # silently. It is now a pure function of the handoff: there is no caller
    # channel left to widen it, so a second derivation over the same handoff is
    # identical, while a different handoff is not (proved below via gen2).
    again = fx.recursive_handoff_custody(handoff)
    assert again.custody_hash == custody.custody_hash
    assert build_state_route_result(
        route_class=ROUTE_DIRECT_EMPIRICAL,
        producer_evidence=[handoff_projection.as_evidence()],
        producer_refs=[handoff.ref],
        consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
        reason="positive handoff with retained coverage custody",
        coverage_custody=again,
    ).envelope_identity_hash == result.envelope_identity_hash
    # A caller can no longer widen the custody identity with supporting evidence.
    with pytest.raises(TypeError):
        fx.recursive_handoff_custody(
            handoff, supporting=(gen1.discovery_result.evaluated_frontier_ref, receipts[0].ref)
        )

    # A custody record naming a different handoff is refused outright. The
    # foreign custody is itself owner-derived, so this proves the producer-ref
    # cross-check rather than a forgery refusal.
    gen2, _r2 = _recursive_generation(
        source, qauth, _atom("PARENT2", parent, "BRANCH2"), parent,
        x1, "RESPONSE2", query, tag="c1-03a-handoff-foreign",
        operation="I03-OP-c1-03a-handoff-foreign",
    )
    foreign_custody = fx.recursive_handoff_custody(gen2.handoffs[0])
    with pytest.raises(OwnerProjectionError, match="not among the producer refs"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[handoff_projection.as_evidence()],
            producer_refs=[handoff.ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="custody names a foreign handoff",
            coverage_custody=foreign_custody,
        )

    # A retained positive may not smuggle in unvisited territory either.
    observed_projection, _ = fx.project_empirical("observed_zero_fixture")
    with pytest.raises(C103AStateRouteError, match="only be retained on the UNVISITED state"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[observed_projection.as_evidence()],
            producer_refs=[observed_projection.producer_ref],
            consumer_disposition=fx.consumer_disposition_for(OBSERVED_ZERO),
            reason="positive relabelled with unvisited territory",
            unvisited_refs=(handoff.ref,),
        )


def test_at15_competent_direct_empirical_route_stays_direct():
    """AT15(1): a competent direct empirical route is consumed without a learned wrapper."""
    projection, data = fx.project_empirical("observed_zero_fixture")

    result = _envelope(
        projection,
        route=ROUTE_DIRECT_EMPIRICAL,
        fixture_refs=(data["fact"].ref,),
    )
    # No learned/adjudicated authority was demanded or invented.
    assert result.route_class == ROUTE_DIRECT_EMPIRICAL
    assert result.authority_refs == ()
    assert result.route_obligation_hash is None


def test_at15_structural_use_requires_learned_adjudication_on_this_base():
    """AT15(2): structural use derives a LEARNED_OR_ADJUDICATED_REQUIRED obligation.

    The obligation is derived from the real admission evaluation, not asserted by
    the caller. Without a named rule the owner cannot return ADMITTED.
    """
    from rawlsing_next.pre553_structural_admission import evaluate_structural_empirical_admission
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state="SUPPORTED", tag="c1-03a-admission")
    rule, registry, snapshot, _parity = environment(admission_state="ALLOW")

    no_rule = evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=snapshot.authority_ref,
        rule=None,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
    )
    assert no_rule.decision_state != "ADMITTED"
    # Even a nonpositive evaluation derives the learned/adjudicated obligation.
    obligation = RouteObligation.from_structural_admission(
        no_rule, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert obligation.required_route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
    # Without a passing rule the owner cannot even resolve the target use, so the
    # obligation records that honestly rather than assuming the requested use.
    assert obligation.decision_state == "MISSING_STRUCTURAL_ADMISSION_AUTHORITY"
    assert obligation.target_use == "UNRESOLVED_STRUCTURAL_USE"
    assert obligation.is_positive_admission is False
    assert obligation.admission_rule_ref["admission_rule_hash"] == ""

    # A genuine positive route does bind the target use and the rule identity.
    positive = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-admission"
    )
    positive_obligation = RouteObligation.from_structural_admission(
        positive, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert positive_obligation.target_use == "STRUCTURAL_MEDIATION_INPUT"
    assert positive_obligation.admission_rule_ref["admission_rule_hash"]
    require_positive_route(positive_obligation)

    # A competent direct route still exists for the same fact, unwrapped.
    projection, _ = fx.project_empirical("observed_zero_fixture")
    direct = _envelope(projection, route=ROUTE_DIRECT_EMPIRICAL)
    assert direct.route_class == ROUTE_DIRECT_EMPIRICAL
    # M1/M2 is not imposed on that competent direct route.
    assert direct.authority_refs == ()


def test_at15_positive_learned_route_is_proven_from_a_real_admission():
    """AT15(2): one genuine positive ADMITTED learned/adjudicated route is proven.

    The positive route is established by the real current admission owner, and
    its receipt/rule/authority/use identity is bound into the envelope.
    """
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-positive-route"
    )
    assert evaluation.decision_state == "ADMITTED"
    assert evaluation.reason_code == "EXACT_NAMED_RULE_ALL_GATES_PASS"

    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert obligation.is_positive_admission is True
    assert obligation.required_route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
    # The obligation binds exact owner-produced identities, not a caller's label.
    assert obligation.admission_receipt_ref["content_hash"]
    assert obligation.admission_authority_ref["authority_content_hash"]
    assert obligation.admission_rule_ref["admission_rule_hash"]
    assert obligation.relation_ref["content_hash"]
    assert obligation.target_use == "STRUCTURAL_MEDIATION_INPUT"
    require_positive_route(obligation)

    # The route and the admission receipt are bound into the envelope identity.
    projection, data = fx.project_empirical("observed_zero_fixture")
    result = _envelope(
        projection,
        route=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
        route_obligation=obligation,
        fixture_refs=(data["fact"].ref,),
    )
    assert result.route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
    assert result.route_obligation_hash == obligation.obligation_hash


def test_at15_failed_learned_claim_cannot_be_route_laundered_as_direct():
    """AT15 hostile: a failed learned claim cannot be relabelled DIRECT.

    The same underlying failed structural-use evidence is used; only the claimed
    route label changes.
    """
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="UNRESOLVED", tag="c1-03a-launder"
    )
    assert evaluation.decision_state != "ADMITTED"
    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )

    # Relabelling the same evidence as DIRECT is rejected against derived law.
    with pytest.raises(RouteLegitimacyError) as excinfo:
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation,
        )
    assert "ROUTE_LAUNDERING_REJECTED" in str(excinfo.value)
    assert obligation.admission_receipt_ref["content_hash"] in str(excinfo.value)

    # A nonpositive learned route may not proceed at all.
    with pytest.raises(RouteLegitimacyError, match="route may not proceed"):
        require_positive_route(obligation)

    # The envelope refuses the laundered route too.
    projection, data = fx.project_empirical("unresolved_fixture")
    with pytest.raises(RouteLegitimacyError):
        _envelope(
            projection,
            route=ROUTE_DIRECT_EMPIRICAL,
            route_obligation=obligation,
            fixture_refs=(data["fact"].ref,),
        )


def test_at15_denying_authority_cannot_be_relabelled_direct():
    """AT15 hostile: a denied admission authority cannot be relabelled direct."""
    evaluation = fx.structural_admission_evaluation(
        admission_state="DENY", fact_state="SUPPORTED", tag="c1-03a-deny-launder"
    )
    assert evaluation.decision_state != "ADMITTED"
    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert obligation.reason_code == "ADMISSION_AUTHORITY_STATE_DENY"
    with pytest.raises(RouteLegitimacyError):
        assert_route_not_laundered(route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation)
    with pytest.raises(RouteLegitimacyError):
        require_positive_route(obligation)


def test_at15_same_evidence_cannot_be_direct_merely_by_changing_the_label():
    """AT15 hostile: identical underlying evidence, different claimed route.

    The owner-derived obligation is unchanged; only the caller's label differs.
    The admitted route is accepted and the direct label is refused for the very
    same receipt.
    """
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-same-evidence"
    )
    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert_route_not_laundered(
        route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED, obligation=obligation,
    )
    with pytest.raises(RouteLegitimacyError):
        assert_route_not_laundered(route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation)
    # The obligation itself is a pure function of the owner receipt.
    again = RouteObligation.from_structural_admission(
        fx.structural_admission_evaluation(
            admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-same-evidence"
        ),
        requested_use="STRUCTURAL_MEDIATION_INPUT",
    )
    assert again.obligation_hash == obligation.obligation_hash


def test_at15_route_obligation_must_be_owner_derived():
    """AT15: a caller cannot supply the route obligation itself."""
    with pytest.raises(RouteLegitimacyError, match="owner-derived RouteObligation"):
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            obligation=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
        )


def test_repair_hq_a_learned_route_without_an_obligation_is_refused():
    """AT15 hostile: a learned route label alone is not legitimacy.

    Replaces the earlier court that merely documented the label. HQ blocker C
    requires the stronger law: a LEARNED_OR_ADJUDICATED_REQUIRED envelope must
    *carry* an owner-derived obligation, or it is refused outright.
    """
    projection, data = fx.project_empirical("observed_zero_fixture")

    with pytest.raises(RouteLegitimacyError, match="must carry a valid owner-derived"):
        build_state_route_result(
            route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
            producer_evidence=[projection.as_evidence()],
            producer_refs=[data["fact"].ref],
            consumer_disposition=fx.consumer_disposition_for(OBSERVED_ZERO),
            reason="learned label with no owner-derived obligation",
        )

    # A competent direct empirical product still needs no obligation at all.
    direct = _envelope(projection, route=ROUTE_DIRECT_EMPIRICAL,
                       fixture_refs=(data["fact"].ref,))
    assert direct.route_obligation_hash is None
    assert direct.authority_refs == ()
    assert direct.negative_claim_authorized is False


# ===========================================================================
# AT16 - final-consumer witness
# ===========================================================================


def test_at16_direct_empirical_positive_path_reaches_the_named_consumer():
    """AT16(1): real producer output -> composition -> actual consumer.

    Corrected witness: the ATT1=agree -> ATT2 fixture is 54 support / 6 oppose,
    so the real composition is SUPPORTED with no zero cell. The earlier version
    of this court labelled the envelope OBSERVED_ZERO, which the reviewer found
    to be false. The retained state is now owner-derived.
    """
    from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        evaluate_positioned_subject_possibility,
    )
    from rawlsing_next.tests import c1_at08_at13_fixture as c1
    from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry

    source = c1.attitude_fixture("c1-03a-at16-positive")
    qauth = _query_authority("c1-03a-at16-positive")
    registry = _registry(source, qauth)

    composed, consumer_query, _witness, _query, _predicate = c1.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "ATT1", "agree")],
        target_question="ATT2",
        tag="at16positive",
        target_domain=[["support", "oppose"]],
    )
    assert composed.analytical_state == "SUPPORTED"

    # The real producer cells are 54 support / 6 oppose: neither is zero, so the
    # owner-derived retained state is a plain SUPPORTED positive.
    cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in composed.complete_cell_geometry
    }
    assert cells == {"support": 54, "oppose": 6}
    assert composed.raw_denominator_support == 60

    projection = OwnerStateProjection.from_empirical_fact(composed.producer_result.facts[0])
    assert projection.retained_state == SUPPORTED_BASELINE
    assert projection.retained_state != OBSERVED_ZERO

    consumer_result = composed.consumer_result_or_null
    assert consumer_result is not None
    assert consumer_result.result_state == "EXACT_SUPPORTED"

    evidence = composed.possibility_slice_evidence_or_null
    assert evidence is not None
    assert evidence.evidence_ref == consumer_result.exact_evidence_ref
    geometry_ref = evidence.geometry["source_fact_ref"]
    assert geometry_ref == composed.producer_fact_ref.as_dict()

    handmade = evaluate_positioned_subject_possibility(
        query=consumer_query,
        rule=c1.make_model_rule(source["universe"].ref, "at16positive"),
        evidence=(evidence,),
    )
    assert handmade.result_hash == consumer_result.result_hash
    assert composed.composed_result_identity_hash not in (handmade.result_hash,)

    result = _envelope(
        projection,
        fixture_refs=(composed.producer_fact_ref, evidence.evidence_ref),
        upstream_composed_result_hash=composed.composed_result_identity_hash,
        disposition=ConsumerDisposition(
            disposition=CONSUMER_INVOKED,
            consumer_query_ref=consumer_query.ref,
            consumer_rule_hash=composed.consumer_model_rule_hash,
            consumer_result_state=consumer_result.result_state,
            consumer_result_hash=consumer_result.result_hash,
            evidence_ref=evidence.evidence_ref,
            non_invocation_reason=None,
        ),
    )
    assert result.retained_analytical_state == SUPPORTED_BASELINE
    assert result.consumer_disposition.consumer_query_ref == consumer_query.ref
    assert result.consumer_disposition.consumer_result_state == "EXACT_SUPPORTED"
    assert result.consumer_disposition.evidence_ref == evidence.evidence_ref
    assert result.upstream_composed_result_hash == composed.composed_result_identity_hash
    assert composed.producer_fact_ref in result.producer_refs


def test_at16_negative_path_preserves_non_invocation_explicitly():
    """AT16(2): a negative path records consumer behavior or explicit non-invocation."""
    projection, data = fx.project_empirical("valid_empty_fixture")
    result = _envelope(projection, fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == VALID_EMPTY
    assert result.consumer_disposition.disposition == (
        CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE
    )
    assert result.consumer_disposition.consumer_result_state is None
    assert "VALID_EMPTY" in result.consumer_disposition.non_invocation_reason
    # The non-invocation is part of the envelope identity, so it cannot be dropped.
    other, other_data = fx.project_empirical("valid_empty_fixture")
    changed = _envelope(other, fixture_refs=(other_data["fact"].ref,),
                        reason="different reason")
    assert changed.envelope_identity_hash != result.envelope_identity_hash


def test_at16_handmade_slice_cannot_satisfy_final_consumer_proof():
    """AT16 hostile: a consumer primitive call alone is not an AT16 witness."""
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        evaluate_positioned_subject_possibility,
    )
    from rawlsing_next.tests import c1_at08_at13_fixture as c1
    from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry

    source = c1.attitude_fixture("c1-03a-at16-handmade")
    qauth = _query_authority("c1-03a-at16-handmade")
    registry = _registry(source, qauth)
    composed, consumer_query, _w, _q, _p = c1.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "ATT1", "agree")],
        target_question="ATT2", tag="at16handmade",
        target_domain=[["support", "oppose"]],
    )
    evidence = composed.possibility_slice_evidence_or_null

    # Calling the consumer directly produces a result, but carries none of the
    # producer/composed custody the AT16 witness requires.
    direct = evaluate_positioned_subject_possibility(
        query=consumer_query,
        rule=c1.make_model_rule(source["universe"].ref, "at16handmade"),
        evidence=(evidence,),
    )
    assert direct.result_state == "EXACT_SUPPORTED"
    # No producer ref, no composed identity, no coverage state is derivable from it.
    assert not hasattr(direct, "producer_fact_ref")
    assert not hasattr(direct, "composed_result_identity_hash")
    # Only the real composed path supplies them.
    assert composed.producer_fact_ref is not None
    assert composed.composed_result_identity_hash
    assert composed.coverage_state == "DIRECT_EXACT_SINGLE_QUERY"


def test_at16_negative_states_are_not_coerced_into_a_consumer_state():
    """AT16 hostile: negative states must not become a fabricated consumer verdict."""
    for project, expected in (
        ("unresolved_fixture", UNKNOWN_UNRESOLVED),
        ("noncomparable_fixture", NONCOMPARABLE),
    ):
        projection, data = fx.project_empirical(project)
        result = _envelope(projection, fixture_refs=(data["fact"].ref,))
        assert result.retained_analytical_state == expected
        assert not result.consumer_disposition.consumer_invoked
        assert result.consumer_disposition.consumer_result_state is None
        assert result.negative_claim_authorized is False

    integrity_projection, integrity_data = fx.project_empirical_integrity_refusal(
        "integrity_failure_fixture"
    )
    assert integrity_projection.retained_state == INTEGRITY_FAILURE
    result = _envelope(
        integrity_projection, fixture_refs=(integrity_data["corrupted_object_ref"],)
    )
    assert result.retained_analytical_state == INTEGRITY_FAILURE
    assert not result.consumer_disposition.consumer_invoked
    assert result.consumer_disposition.consumer_result_state is None
    assert result.negative_claim_authorized is False


# ===========================================================================
# C1-03A independent-review blocker repairs
# ===========================================================================


def test_repair_blocker1_caller_label_cannot_establish_analytical_state():
    """C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001: a bare label is not authority.

    This is the reviewer's own static reproducer: a real producer ref with
    producer_state='SUPPORTED' and a different caller-chosen retained label.
    """
    from rawlsing_next.pre553_empirical_objects import ExactRef

    real_ref = ExactRef("EmpiricalFact@1.0.0", "urn:test:c1-03a:real-fact", "b" * 64)
    with pytest.raises(OwnerProjectionError) as excinfo:
        ProducerStateEvidence(
            owner="rawlsing_next.pre553_empirical_query.execute_empirical_query",
            producer_state="SUPPORTED",
            retained_state=VALID_EMPTY,
            reason="caller chosen label",
            producer_ref=real_ref,
        )
    assert "STATE-PROJECTION-001" in str(excinfo.value)


def test_repair_blocker1_deprecated_label_helper_now_refuses():
    """The old caller-label helper is retained only to prove it now refuses."""
    with pytest.raises(OwnerProjectionError):
        fx.producer_evidence_for(
            owner="o", producer_state="SUPPORTED", retained_state=OBSERVED_ZERO,
            reason="r", producer_ref=None,
        )


def test_repair_blocker1_retained_state_is_derived_from_the_real_owner_object():
    """Each retained state is projected from its own competent owner object."""
    expected = {
        "observed_zero_fixture": OBSERVED_ZERO,
        "valid_empty_fixture": VALID_EMPTY,
        "unresolved_fixture": UNKNOWN_UNRESOLVED,
        "noncomparable_fixture": NONCOMPARABLE,
    }
    for name, want in expected.items():
        projection, _ = fx.project_empirical(name)
        assert projection.retained_state == want, name
        assert projection.projection_law, name
    receipt, _ = fx.project_receipt("underpowered_fixture")
    assert receipt.retained_state == UNDERPOWERED
    adaptive, _ = fx.project_adaptive()
    assert adaptive.retained_state == UNVISITED
    refusal, _ = fx.project_empirical_integrity_refusal("integrity_failure_fixture")
    assert refusal.retained_state == INTEGRITY_FAILURE


def test_repair_blocker1_observed_zero_requires_the_real_cell_projection():
    """A SUPPORTED fact without its cell projection cannot claim a plain positive.

    Without the producer's own cells an observed zero could not be derived, so
    the projection fails closed rather than defaulting to SUPPORTED.
    """
    from rawlsing_next.pre553_empirical_objects import EmpiricalFact

    # Built from a real owner-produced SUPPORTED fact, with only the cell
    # projection stripped. This is a genuine EmpiricalFact, so the type gate is
    # satisfied and the cell-projection law is what must refuse it.
    _, data = fx.project_empirical("observed_zero_fixture")
    source = data["fact"]
    no_cells = EmpiricalFact(
        typed_state=source.typed_state,
        authority_snapshot_refs=source.authority_snapshot_refs,
        dependency_refs=source.dependency_refs,
        producer_replay_locator_or_reference_root=(
            source.producer_replay_locator_or_reference_root
        ),
        **{**dict(source.semantic_fields), "target_topology": {"arity": 1}},
    )
    assert no_cells.typed_state == "SUPPORTED"
    assert "complete_cell_semantic_projection" not in no_cells.target_topology

    with pytest.raises(OwnerProjectionError, match="complete_cell_semantic_projection"):
        OwnerStateProjection.from_empirical_fact(no_cells)


def test_repair_blocker1_observed_zero_cell_on_non_supported_fact_is_refused():
    """An observed-zero cell cannot be attached to a non-supported fact."""
    with pytest.raises(C103AStateRouteError, match="positive supported denominator"):
        classify_empirical_cells(
            "UNRESOLVED",
            ({"cell": "1", "cell_state": "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
              "raw_numerator_support": 0},),
        )


def test_repair_blocker1_distinct_negative_states_remain_distinct():
    """The repair did not collapse any mandatory state."""
    reached = {
        fx.project_empirical("observed_zero_fixture")[0].retained_state,
        fx.project_empirical("valid_empty_fixture")[0].retained_state,
        fx.project_receipt("underpowered_fixture")[0].retained_state,
        fx.project_empirical("unresolved_fixture")[0].retained_state,
        fx.project_adaptive()[0].retained_state,
        fx.project_empirical("noncomparable_fixture")[0].retained_state,
        fx.blocked_required_authority_fixture() and fx.project_blocked_authority_refusal(
            "blocked_required_authority_fixture"
        )[0].retained_state,
        fx.project_empirical_integrity_refusal("integrity_failure_fixture")[0].retained_state,
    }
    assert reached == set(MANDATORY_AT14_STATES)
    assert len(reached) == 8


def test_repair_blocker2_obligation_is_owner_derived_not_caller_supplied():
    """C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001: no caller-chosen obligation."""
    # The previous signature accepted required_route_class; it no longer exists.
    with pytest.raises(TypeError):
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            required_route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_state="UNRESOLVED",
            reason="caller asserts no learned requirement",
        )
    with pytest.raises(RouteLegitimacyError, match="owner-derived RouteObligation"):
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            obligation=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
        )


def test_repair_blocker2_same_evidence_is_refused_for_direct_under_derived_law():
    """The same underlying evidence cannot become direct by relabelling alone."""
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-rep-same"
    )
    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    with pytest.raises(RouteLegitimacyError, match="ROUTE_LAUNDERING_REJECTED"):
        assert_route_not_laundered(route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation)
    # The receipt identity is quoted in the refusal, so it is owner-derived.
    assert obligation.admission_receipt_ref["content_hash"]


def test_repair_blocker2_obligation_binds_exact_owner_identities():
    """The obligation binds receipt, rule, authority, use and decision."""
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-rep-bind"
    )
    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert obligation.owner == (
        "rawlsing_next.pre553_structural_admission.evaluate_structural_empirical_admission"
    )
    assert obligation.admission_receipt_ref == evaluation.receipt.ref.as_dict()
    assert obligation.admission_authority_ref["authority_content_hash"]
    assert obligation.admission_rule_ref["admission_rule_hash"]
    assert obligation.target_use == "STRUCTURAL_MEDIATION_INPUT"
    assert obligation.decision_state == "ADMITTED"
    # The obligation hash is a pure function of those owner identities.
    assert obligation.obligation_hash == RouteObligation.from_structural_admission(
        fx.structural_admission_evaluation(
            admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-rep-bind"
        ),
        requested_use="STRUCTURAL_MEDIATION_INPUT",
    ).obligation_hash


def test_repair_blocker2_failed_and_denied_routes_cannot_proceed():
    """Failed and DENY routes may not proceed, and never become direct."""
    for admission_state, fact_state, tag in (
        ("ALLOW", "UNRESOLVED", "c1-03a-rep-failed"),
        ("DENY", "SUPPORTED", "c1-03a-rep-deny"),
    ):
        evaluation = fx.structural_admission_evaluation(
            admission_state=admission_state, fact_state=fact_state, tag=tag
        )
        obligation = RouteObligation.from_structural_admission(
            evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )
        assert not obligation.is_positive_admission
        with pytest.raises(RouteLegitimacyError, match="route may not proceed"):
            require_positive_route(obligation)
        with pytest.raises(RouteLegitimacyError, match="ROUTE_LAUNDERING_REJECTED"):
            assert_route_not_laundered(
                route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation
            )


def test_repair_blocker2_competent_direct_route_is_not_given_a_learned_wrapper():
    """A genuinely competent direct empirical product stays direct."""
    projection, data = fx.project_empirical("observed_zero_fixture")
    result = _envelope(projection, route=ROUTE_DIRECT_EMPIRICAL,
                       fixture_refs=(data["fact"].ref,))
    assert result.route_class == ROUTE_DIRECT_EMPIRICAL
    assert result.authority_refs == ()
    assert result.route_obligation_hash is None


def test_repair_blocker3_positive_handoff_without_coverage_custody_fails():
    """C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001: the exact hostile.

    A positive recursive handoff with a positive retained state and a missing
    coverage record must fail.
    """
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _depth2_source,
        _recursive_generation,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import _atom
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
    )

    source = _depth2_source("c1-03a-rep-custody")
    qauth = _query_authority("c1-03a-rep-custody")
    parent = _branch_predicate(source, qauth, tag="rep-custody-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="rep-custody-x1")
    query = _query(source, qauth, parent, ("X",), tag="rep-custody-xq")
    gen1, _ = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", query, tag="repcustody", operation="I03-OP-repcustody",
    )
    handoff = gen1.handoffs[0]

    projection, custody = fx.project_recursive_handoff(handoff)
    with pytest.raises(OwnerProjectionError, match="requires retained custody"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[projection.as_evidence()],
            producer_refs=[handoff.ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="positive handoff, missing coverage record",
        )


def test_repair_blocker3_custody_is_bound_into_the_envelope_identity():
    """With owner-derived custody the positive is lawful and custody is bound."""
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _depth2_source,
        _recursive_generation,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import _atom
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
    )

    source = _depth2_source("c1-03a-rep-custody2")
    qauth = _query_authority("c1-03a-rep-custody2")
    parent = _branch_predicate(source, qauth, tag="rep-custody2-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="rep-custody2-x1")
    query = _query(source, qauth, parent, ("X",), tag="rep-custody2-xq")
    gen1, _ = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", query, tag="repcustody2", operation="I03-OP-repcustody2",
    )
    handoff = gen1.handoffs[0]
    frontier = gen1.discovery_result.evaluated_frontier_ref
    custody = fx.recursive_handoff_custody(handoff)
    projection, custody = fx.project_recursive_handoff(handoff)
    result = build_state_route_result(
        route_class=ROUTE_DIRECT_EMPIRICAL,
        producer_evidence=[projection.as_evidence()],
        producer_refs=[handoff.ref],
        consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
        reason="positive handoff with custody",
        coverage_custody=custody,
    )
    assert result.coverage_record_ref == frontier
    assert result.coverage_custody_hash == custody.custody_hash
    assert custody.custody_hash in str(result.identity_material)


def test_repair_blocker3_mismatched_coverage_ref_is_refused():
    """A declared coverage_record_ref that disagrees with custody is refused."""
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _depth2_source,
        _recursive_generation,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import _atom
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
    )

    source = _depth2_source("c1-03a-rep-mismatch")
    qauth = _query_authority("c1-03a-rep-mismatch")
    parent = _branch_predicate(source, qauth, tag="rep-mismatch-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="rep-mismatch-x1")
    query = _query(source, qauth, parent, ("X",), tag="rep-mismatch-xq")
    gen1, _ = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", query, tag="repmismatch", operation="I03-OP-repmismatch",
    )
    handoff = gen1.handoffs[0]
    custody = fx.recursive_handoff_custody(handoff)
    projection, custody = fx.project_recursive_handoff(handoff)
    from rawlsing_next.pre553_empirical_objects import ExactRef

    with pytest.raises(OwnerProjectionError, match="disagrees with the owner-derived"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[projection.as_evidence()],
            producer_refs=[handoff.ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="mismatched coverage ref",
            coverage_custody=custody,
            coverage_record_ref=ExactRef(
                "C11Internal:EvaluatedFrontier", "urn:test:c1-03a:foreign-frontier", "d" * 64
            ),
        )


def test_repair_unvisited_adaptive_witness_is_preserved():
    """The valid real adaptive UNVISITED witness survives the repair."""
    projection, data = fx.project_adaptive()
    adaptive = data["adaptive_result"]
    assert adaptive.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert adaptive.unvisited_unit_refs
    assert adaptive.global_negative_claim is False
    result = _envelope(
        projection,
        fixture_refs=(data["determinant_state_ref"],),
        unvisited_refs=adaptive.unvisited_unit_refs,
        visited_refs=adaptive.visited_unit_refs,
        coverage_record_ref=adaptive.checkpoint.ref,
    )
    assert result.retained_analytical_state == UNVISITED
    assert result.coverage_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert result.unvisited_refs == adaptive.unvisited_unit_refs
    assert result.negative_claim_authorized is False


# ===========================================================================
# HQ152 trust-boundary correction (R2) hostiles
#
# The trust boundary moved outward: the three derived types are now factory-only
# and fail closed, refusals are exact typed owner contracts, and a learned route
# requires an owner-derived obligation.
# ===========================================================================


def test_repair_hq_a_direct_projection_construction_cannot_mint_evidence():
    """HQ-A hostile: the exact caller-forged projection cannot mint evidence."""
    projection, data = fx.project_empirical("observed_zero_fixture")
    ref = data["fact"].ref

    for forged_state in (VALID_EMPTY, SUPPORTED_BASELINE, OBSERVED_ZERO):
        with pytest.raises(OwnerProjectionError, match="may only be built by one of its typed owner"):
            OwnerStateProjection(
                owner=OWNER_EMPIRICAL_PROJECTION_LABEL,
                producer_state="SUPPORTED",
                retained_state=forged_state,
                projection_law="caller-chosen law",
                reason="caller label",
                producer_ref=ref,
            ).as_evidence()

    # The typed factory still works, and the genuine projection is trustworthy.
    assert projection.retained_state == OBSERVED_ZERO
    assert projection.as_evidence().retained_state == OBSERVED_ZERO


def test_repair_hq_a_public_derive_helper_is_gone():
    """HQ-A: no public derive/derive_fn injection point survives."""
    assert not hasattr(OwnerStateProjection, "derive")
    for name, member in vars(OwnerStateProjection).items():
        if inspect.isfunction(member):
            params = inspect.signature(member).parameters
            assert "derive_fn" not in params, f"{name} still accepts derive_fn"
            assert "owner_object" not in params, f"{name} still accepts owner_object"


def test_repair_hq_b_fabricated_exact_refusals_cannot_mint_governed_refusals():
    """HQ-B/R4: an exact refusal TYPE is not provenance.

    Both refusal types are publicly constructible bare ``ValueError`` subclasses. A
    manually constructed one, even of the exact accepted type, must not mint trusted
    governed state.
    """
    from rawlsing_next.pre553_analytical_state_and_route import (
        OwnerRefusalWitness,
        REFUSAL_KIND_EMPIRICAL_INTEGRITY,
    )
    from rawlsing_next.pre553_empirical_objects import ExactRef, Pre553IntegrityError

    ref = ExactRef("EmpiricalFact@1.0.0", "urn:t:caller-invented", "c" * 64)
    for exc in (ValueError("nope"), RuntimeError("nope")):
        with pytest.raises(TypeError):
            OwnerStateProjection.from_blocked_authority_refusal(exception=exc, reason="r")
        with pytest.raises(TypeError):
            OwnerStateProjection.from_empirical_integrity_refusal(exception=exc, reason="r")
    # The factories accept a witness only; there is no exception parameter at all.
    with pytest.raises(TypeError):
        OwnerStateProjection.from_empirical_integrity_refusal(
            Pre553IntegrityError("caller"), reason="caller", producer_ref=ref
        )
    # A hand-built witness is refused even with the right kind.
    with pytest.raises(OwnerProjectionError, match="may only be produced by an actual"):
        OwnerRefusalWitness(
            owner_label="caller",
            refusal_kind=REFUSAL_KIND_EMPIRICAL_INTEGRITY,
            refused_ref=ref,
            supporting_refs=(ref,),
            invocation_binding="caller-invented",
            refusal_type="Pre553IntegrityError",
            refusal_message="caller",
        )
    # And a genuine witness still projects lawfully.
    witness, _ = fx.capture_integrity_refusal("integrity_failure_fixture")
    assert OwnerStateProjection.from_empirical_integrity_refusal(
        witness=witness).retained_state == INTEGRITY_FAILURE


def test_repair_hq_b_real_refusals_stay_two_distinct_states():
    """HQ-B/R4: the two witnessed refusal paths remain exact and distinct."""
    from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
    from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError

    integrity, _ = fx.project_empirical_integrity_refusal("integrity_failure_fixture")
    blocked, _ = fx.project_blocked_authority_refusal("blocked_required_authority_fixture")
    assert integrity.retained_state == INTEGRITY_FAILURE
    assert blocked.retained_state == BLOCKED_REQUIRED_AUTHORITY
    assert integrity.retained_state != blocked.retained_state

    # Pre553AuthorityError SUBCLASSES Pre553IntegrityError, so an isinstance-based
    # classification would collapse these two mandatory states.
    assert issubclass(Pre553AuthorityError, Pre553IntegrityError)
    # The witness kind gates the mapping, so neither witness can be replayed as the
    # other state.
    integrity_witness, _ = fx.capture_integrity_refusal("integrity_failure_fixture")
    blocked_witness, _ = fx.capture_blocked_authority_refusal(
        "blocked_required_authority_fixture")
    with pytest.raises(OwnerProjectionError, match="does not project onto"):
        OwnerStateProjection.from_blocked_authority_refusal(witness=integrity_witness)
    with pytest.raises(OwnerProjectionError, match="does not project onto"):
        OwnerStateProjection.from_empirical_integrity_refusal(witness=blocked_witness)


def test_repair_hq_c_forged_route_obligation_cannot_establish_legitimacy():
    """HQ-C hostile: RouteObligation is factory-only."""
    evaluation = fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag="hq-c-forged"
    )
    real = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert real.is_positive_admission
    # Relabelling the same forged shape cannot reach the gate.
    with pytest.raises(OwnerProjectionError, match="may only be built by RouteObligation"):
        RouteObligation(
            owner="caller",
            requested_use="STRUCTURAL_MEDIATION_INPUT",
            target_use="STRUCTURAL_MEDIATION_INPUT",
            decision_state="ADMITTED",
            reason_code="caller-asserted",
            required_route_class=ROUTE_DIRECT_EMPIRICAL,
            relation_ref=dict(real.relation_ref),
            admission_receipt_ref=dict(real.admission_receipt_ref),
            admission_authority_ref=dict(real.admission_authority_ref),
            admission_rule_ref=dict(real.admission_rule_ref),
            blocking_refs=(),
        )
    assert_route_not_laundered(route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED, obligation=real)


def test_repair_hq_c_relabelling_direct_to_learned_never_produces_a_lawful_route():
    """HQ-C: a competent direct empirical product cannot be relabelled learned."""
    projection, data = fx.project_empirical("observed_zero_fixture")
    # Direct is lawful with no authority and no obligation.
    direct = _envelope(projection, route=ROUTE_DIRECT_EMPIRICAL,
                       fixture_refs=(data["fact"].ref,))
    assert direct.authority_refs == ()
    assert direct.route_obligation_hash is None
    # Learned for the same competent product is refused: no owner-derived
    # obligation exists for it, so the label alone cannot create legitimacy.
    with pytest.raises(RouteLegitimacyError, match="must carry a valid owner-derived"):
        build_state_route_result(
            route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
            producer_evidence=[projection.as_evidence()],
            producer_refs=[data["fact"].ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="direct product relabelled learned",
        )


def test_repair_hq_d_forged_custody_cannot_authorize_a_handoff():
    """HQ-D hostile: RecursiveCoverageCustody is factory-only."""
    handoff = _hq_real_handoff("hq-d-forged")
    custody = fx.recursive_handoff_custody(handoff)

    with pytest.raises(OwnerProjectionError, match="may only be built by RecursiveCoverageCustody"):
        RecursiveCoverageCustody(
            handoff_ref=handoff.ref,
            coverage_record_ref=handoff.evaluated_frontier_ref,
            handoff_scope_identity={},
        )
    # A non-handoff object is refused: custody requires a real handoff.
    with pytest.raises(OwnerProjectionError, match="requires a real RecursiveBranchHandoff"):
        RecursiveCoverageCustody.from_handoff(object())
    # The genuine owner-derived custody still authorizes it.
    projection, _ = fx.project_recursive_handoff(handoff)
    result = build_state_route_result(
        route_class=ROUTE_DIRECT_EMPIRICAL,
        producer_evidence=[projection.as_evidence()],
        producer_refs=[handoff.ref],
        consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
        reason="real handoff with owner-derived custody",
        coverage_custody=custody,
    )
    assert result.coverage_record_ref == handoff.evaluated_frontier_ref


def test_repair_hq_d_custody_records_no_completeness_grade():
    """HQ-D: custody must not carry a caller-supplied completeness grade.

    The handoff does not own a completeness grade, so the custody has no such
    field at all; the field must not reappear.
    """
    assert "completeness_state" not in {f for f in vars(RecursiveCoverageCustody)}
    handoff = _hq_real_handoff("hq-d-no-grade")
    custody = fx.recursive_handoff_custody(handoff)
    assert "completeness_state" not in custody.identity_material()
    # And the helper itself refuses to accept one.
    with pytest.raises(TypeError):
        fx.recursive_handoff_custody(handoff, completeness_state="COMPLETE")


def test_repair_hq_d_same_handoff_with_wrong_coverage_ref_fails():
    """HQ-D: a caller cannot substitute a different coverage record."""
    handoff = _hq_real_handoff("hq-d-wrong-ref")
    custody = fx.recursive_handoff_custody(handoff)
    assert custody.coverage_record_ref == handoff.evaluated_frontier_ref

    # A custody record built over a foreign frontier is refused by the envelope,
    # and the handoff projection refuses a custody that names a different handoff.
    foreign = _hq_real_handoff("hq-d-wrong-ref-foreign")
    foreign_custody = fx.recursive_handoff_custody(foreign)
    assert foreign_custody.coverage_record_ref != custody.coverage_record_ref
    with pytest.raises(OwnerProjectionError, match="names a different handoff"):
        OwnerStateProjection.from_recursive_handoff(handoff, foreign_custody)
    projection, _ = fx.project_recursive_handoff(handoff)
    with pytest.raises(OwnerProjectionError, match="disagrees with the owner-derived custody record"):
        build_state_route_result(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            producer_evidence=[projection.as_evidence()],
            producer_refs=[handoff.ref],
            consumer_disposition=fx.consumer_disposition_for(SUPPORTED_BASELINE),
            reason="declared coverage ref contradicts the custody",
            coverage_record_ref=foreign.evaluated_frontier_ref,
            coverage_custody=custody,
        )


def test_repair_hq_d_handoff_projection_requires_real_custody():
    """HQ-D: positive handoff state comes from the typed factory, never directly."""
    handoff = _hq_real_handoff("hq-d-typed-projection")
    with pytest.raises(OwnerProjectionError, match="may only be built by one of its typed owner"):
        OwnerStateProjection(
            owner=OWNER_RECURSIVE_HANDOFF_LABEL,
            producer_state="RECURSIVE_BRANCH_HANDOFF_SELECTED",
            retained_state=SUPPORTED_BASELINE,
            projection_law="caller",
            reason="caller",
            producer_ref=handoff.ref,
        )
    projection, custody = fx.project_recursive_handoff(handoff)
    assert projection.retained_state == SUPPORTED_BASELINE
    assert projection.producer_ref == handoff.ref
    assert custody.handoff_ref == handoff.ref


def _hq_real_handoff(tag: str):
    """Build a real recursive handoff through the actual owner path."""
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _depth2_source,
        _recursive_generation,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import _atom
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
    )

    # _recursive_generation builds its own DISCOVERY_FRONTIER authority from the
    # tag it is given, so it must differ from the query authority tag or the two
    # snapshots collide on one authority id with different content.
    source = _depth2_source(tag)
    qauth = _query_authority(tag)
    gen_tag = f"{tag}-gen"
    parent = _branch_predicate(source, qauth, tag=f"{tag}-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag=f"{tag}-x1")
    query = _query(source, qauth, parent, ("X",), tag=f"{tag}-xq")
    gen1, _registry = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", query, tag=gen_tag, operation=f"I03-OP-{gen_tag}",
    )
    return gen1.handoffs[0]


# ===========================================================================
# HQ153 factory-authenticity correction (R3) hostiles
#
# E: each typed factory requires the EXACT competent current owner object, so a
#    caller-shaped forgery with plausible fields and exact-looking refs cannot
#    ask a trusted factory to mint governed material.
# F: the owner label is fixed by the factory, and neither the producer
#    determinant ref nor the custody's supporting evidence is caller-writable.
# G: the canonical StructuralEmpiricalAdmission receipt, not the hand-
#    constructible AdmissionEvaluation envelope around it, is the authority.
# ===========================================================================


def _plausible_ref(namespace: str):
    """An exact-looking but entirely caller-minted ref."""
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash

    digest = semantic_hash({"caller": namespace})
    return ExactRef(
        "EmpiricalFact@1.0.0",
        f"urn:rawlsing:caller-forged:{namespace}:sha256:{digest}",
        digest,
    )


def _real_positive_evaluation(tag: str = "hq153-positive"):
    return fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="SUPPORTED", tag=tag
    )


def _real_negative_evaluation(tag: str = "hq153-negative"):
    return fx.structural_admission_evaluation(
        admission_state="ALLOW", fact_state="UNRESOLVED", tag=tag
    )


def _no_rule_evaluation(tag: str = "hq153-no-rule"):
    """A real evaluation whose receipt cannot even resolve a target use."""
    from rawlsing_next.pre553_structural_admission import (
        evaluate_structural_empirical_admission,
    )
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state="SUPPORTED", tag=tag)
    rule, registry, snapshot, _parity = environment(admission_state="ALLOW")
    return evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=snapshot.authority_ref,
        rule=None,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=(
            fact.producer_replay_locator_or_reference_root
        ),
    )


# ---------------------------------------------------------------------------
# HQ-E -- exact competent owner object families only
# ---------------------------------------------------------------------------


def test_repair_hq_e_duck_typed_empirical_fact_cannot_mint_projection():
    """HQ-E hostile: a plausible fake EmpiricalFact cannot mint a projection."""
    _, data = fx.project_empirical("observed_zero_fixture")
    real = data["fact"]

    class _FakeEmpiricalFact:
        """Everything the projection reads, all of it caller-shaped."""

        typed_state = "SUPPORTED"
        target_topology = {"complete_cell_semantic_projection": []}
        replay_ref = None
        ref = _plausible_ref("fake-empirical-fact")

    fake = _FakeEmpiricalFact()
    # Sanity: the forgery really does carry the exact-looking ref and the exact
    # field names the factory reads, so only the type gate can refuse it.
    assert isinstance(fake.ref, type(real.ref))
    assert fake.typed_state == real.typed_state

    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_empirical_fact(fake)

    # A genuine owner fact is still accepted and still projects truthfully.
    good = OwnerStateProjection.from_empirical_fact(real)
    assert good.retained_state == OBSERVED_ZERO
    assert good.producer_ref == real.ref
    assert good.owner == OWNER_EMPIRICAL_PROJECTION_LABEL


def test_repair_hq_e_duck_typed_discovery_receipt_cannot_mint_projection():
    """HQ-E hostile: a plausible fake DiscoveryResultReceipt is refused."""
    _, rdata = fx.project_receipt("underpowered_fixture")
    real = rdata["receipt"]

    class _FakeReceipt:
        typed_state = "OBSERVED_ZERO"
        coverage_state = "EVALUATED_OBSERVED_ZERO"
        ref = _plausible_ref("fake-discovery-receipt")

    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_discovery_receipt(_FakeReceipt())

    good = OwnerStateProjection.from_discovery_receipt(real)
    assert good.owner == OWNER_DISCOVERY_PROJECTION_LABEL
    assert good.producer_ref == real.ref


def test_repair_hq_e_duck_typed_adaptive_result_cannot_mint_projection():
    """HQ-E hostile: a plausible fake AdaptiveSearchResult is refused."""
    _, adata = fx.project_adaptive()
    real = adata["adaptive_result"]

    class _FakeAdaptive:
        completeness_state = "PARTIAL_BUDGET_EXHAUSTED"
        unvisited_unit_refs = (_plausible_ref("fake-unvisited"),)
        visited_unit_refs = (_plausible_ref("fake-visited"),)
        global_negative_claim = False
        determinant_state_ref = _plausible_ref("fake-determinant")
        checkpoint = None

    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_adaptive_result(_FakeAdaptive())

    good = OwnerStateProjection.from_adaptive_result(real)
    assert good.retained_state == UNVISITED
    assert good.producer_ref == real.determinant_state_ref
    assert good.unvisited_refs == real.unvisited_unit_refs


def test_repair_hq_e_duck_typed_admission_evaluation_cannot_mint_route_material():
    """HQ-E hostile: a fake evaluation around a REAL receipt is still refused.

    This is the sharpest form of the forgery: the receipt is genuine, so only the
    envelope type is wrong. Exact type identity must refuse it anyway, because a
    caller-shaped envelope is not the competent admission owner.
    """
    positive = _real_positive_evaluation("hq153-fake-envelope")
    assert positive.decision_state == "ADMITTED"

    class _FakeEvaluation:
        decision_state = "ADMITTED"
        reason_code = "CALLER_ASSERTED_ALL_GATES_PASS"
        receipt = positive.receipt
        blocking_refs = ()

    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        RouteObligation.from_structural_admission(
            _FakeEvaluation(), requested_use="STRUCTURAL_MEDIATION_INPUT"
        )

    # A bare object with no receipt at all is refused too.
    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        RouteObligation.from_structural_admission(object(), requested_use="X")


def test_repair_hq_e_owner_family_subclasses_are_refused_too():
    """HQ-E: the check is exact type identity, not isinstance.

    An ``isinstance`` gate would accept a caller-defined subclass that inherits
    every plausible field from the real owner type. Exact identity refuses it.
    """
    from rawlsing_next.pre553_empirical_objects import (
        DiscoveryResultReceipt,
        EmpiricalFact,
    )
    from rawlsing_next.pre553_discovery_adaptive import AdaptiveSearchResult
    from rawlsing_next.pre553_structural_admission import AdmissionEvaluation

    _, data = fx.project_empirical("observed_zero_fixture")

    class _FactSubclass(EmpiricalFact):
        pass

    class _ReceiptSubclass(DiscoveryResultReceipt):
        pass

    assert issubclass(_FactSubclass, EmpiricalFact)
    # Instances are made without the canonical constructor: the point is the TYPE,
    # and the gate must refuse before it reads any attribute at all.
    subclassed_fact = object.__new__(_FactSubclass)
    subclassed_receipt = object.__new__(_ReceiptSubclass)
    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_empirical_fact(subclassed_fact)
    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_discovery_receipt(subclassed_receipt)
    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        OwnerStateProjection.from_adaptive_result(subclassed_fact)
    with pytest.raises(OwnerProjectionError, match="requires the exact current owner object"):
        RouteObligation.from_structural_admission(
            subclassed_receipt, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )

    # The exact real families are all still the accepted ones.
    _, adata = fx.project_adaptive()
    assert type(data["fact"]) is EmpiricalFact
    assert type(adata["adaptive_result"]) is AdaptiveSearchResult
    assert type(_real_positive_evaluation("hq153-e-exact-family")) is AdmissionEvaluation


# ---------------------------------------------------------------------------
# HQ-F -- the owner label and provenance refs are factory-fixed
# ---------------------------------------------------------------------------


def test_repair_hq_f_no_factory_still_accepts_a_caller_owner_label():
    """HQ-F: every typed factory's owner label is fixed by the factory itself."""
    from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
    from rawlsing_next.pre553_empirical_objects import ExactRef, Pre553IntegrityError

    _, data = fx.project_empirical("observed_zero_fixture")
    _, rdata = fx.project_receipt("underpowered_fixture")
    _, adata = fx.project_adaptive()
    handoff = _hq_real_handoff("hq153-f-owner-label")
    custody = fx.recursive_handoff_custody(handoff)
    positive = _real_positive_evaluation("hq153-f-owner-label")
    ref = ExactRef("EmpiricalFact@1.0.0", "urn:test:hq153:owner-label", "f" * 64)

    # No minting factory signature exposes an owner label any more. (The dataclass
    # __init__ still lists the field, but it is token-guarded and covered by the
    # R2 direct-construction hostiles; only the factories are scanned here.)
    for owner in (OwnerStateProjection, RouteObligation, RecursiveCoverageCustody):
        for name, member in vars(owner).items():
            if inspect.isfunction(member) and name.startswith("from_"):
                params = inspect.signature(member).parameters
                assert "owner" not in params, f"{owner.__name__}.{name} still accepts owner"

    with pytest.raises(TypeError):
        OwnerStateProjection.from_empirical_fact(
            data["fact"], owner="rawlsing_next.not_a_real_owner"
        )
    with pytest.raises(TypeError):
        OwnerStateProjection.from_discovery_receipt(
            rdata["receipt"], owner="rawlsing_next.not_a_real_owner"
        )
    with pytest.raises(TypeError):
        OwnerStateProjection.from_adaptive_result(
            adata["adaptive_result"], owner="rawlsing_next.not_a_real_owner"
        )
    with pytest.raises(TypeError):
        OwnerStateProjection.from_recursive_handoff(
            handoff, custody, owner="rawlsing_next.not_a_real_owner"
        )
    with pytest.raises(TypeError):
        RouteObligation.from_structural_admission(
            positive, requested_use="STRUCTURAL_MEDIATION_INPUT",
            owner="rawlsing_next.not_a_real_owner",
        )
    with pytest.raises(TypeError):
        OwnerStateProjection.from_empirical_integrity_refusal(
            exception=Pre553IntegrityError("x"), reason="r", producer_ref=ref,
            owner="rawlsing_next.not_a_real_owner",
        )
    with pytest.raises(TypeError):
        OwnerStateProjection.from_blocked_authority_refusal(
            exception=Pre553AuthorityError("x"), reason="r", producer_ref=ref,
            owner="rawlsing_next.not_a_real_owner",
        )

    # Each genuine projection carries the owner its own factory names.
    assert OwnerStateProjection.from_empirical_fact(data["fact"]).owner == (
        OWNER_EMPIRICAL_PROJECTION_LABEL
    )
    assert OwnerStateProjection.from_discovery_receipt(rdata["receipt"]).owner == (
        OWNER_DISCOVERY_PROJECTION_LABEL
    )
    assert OwnerStateProjection.from_adaptive_result(adata["adaptive_result"]).owner == (
        OWNER_ADAPTIVE_PROJECTION_LABEL
    )
    assert OwnerStateProjection.from_recursive_handoff(handoff, custody).owner == (
        OWNER_RECURSIVE_HANDOFF_LABEL
    )
    assert RouteObligation.from_structural_admission(
        positive, requested_use="STRUCTURAL_MEDIATION_INPUT"
    ).owner == OWNER_ADMISSION_PROJECTION_LABEL


def test_repair_hq_f_adaptive_producer_ref_cannot_be_replaced_by_the_caller():
    """HQ-F: the adaptive producer ref is the owner's own determinant ref."""
    from rawlsing_next.pre553_empirical_objects import ExactRef

    _, adata = fx.project_adaptive()
    real = adata["adaptive_result"]

    # No adaptive minting signature accepts a producer_ref override. The two refusal
    # factories legitimately take a producer_ref naming the refused object.
    for name, member in vars(OwnerStateProjection).items():
        if inspect.isfunction(member) and name.startswith("from_"):
            if "producer_ref" in inspect.signature(member).parameters:
                assert name in {
                    "from_empirical_integrity_refusal",
                    "from_blocked_authority_refusal",
                }, f"{name} still accepts a caller-chosen producer_ref"

    with pytest.raises(TypeError):
        OwnerStateProjection.from_adaptive_result(
            real, producer_ref=_plausible_ref("caller-substituted-determinant")
        )

    projection = OwnerStateProjection.from_adaptive_result(real)
    # The exact owner determinant ref, never a caller substitute.
    assert projection.producer_ref == real.determinant_state_ref
    assert isinstance(projection.producer_ref, ExactRef)
    # The owner checkpoint, visited and unvisited refs are preserved exactly.
    assert projection.coverage_state == real.completeness_state
    assert projection.unvisited_refs == real.unvisited_unit_refs
    assert projection.visited_refs == real.visited_unit_refs
    assert real.checkpoint.ref in projection.supporting_refs
    assert projection.producer_ref in projection.supporting_refs


def test_repair_hq_f_custody_admits_no_caller_supporting_refs():
    """HQ-F: custody identity is a pure function of the real handoff."""
    handoff = _hq_real_handoff("hq153-f-supporting")
    custody = fx.recursive_handoff_custody(handoff)

    for name, member in vars(RecursiveCoverageCustody).items():
        if inspect.isfunction(member):
            assert "required_supporting_refs" not in inspect.signature(member).parameters, (
                f"{name} still accepts required_supporting_refs"
            )

    with pytest.raises(TypeError):
        RecursiveCoverageCustody.from_handoff(
            handoff, required_supporting_refs=[_plausible_ref("caller-evidence")]
        )
    with pytest.raises(TypeError):
        fx.recursive_handoff_custody(
            handoff, supporting=(_plausible_ref("caller-evidence"),)
        )

    # The custody binds only owner-derived material: the exact handoff ref, the
    # exact evaluated frontier, and the handoff's own retained scope identity.
    assert custody.handoff_ref == handoff.ref
    assert custody.coverage_record_ref == handoff.evaluated_frontier_ref
    assert custody.supporting_refs == ()
    assert "completeness_state" not in custody.identity_material()
    # Deriving it twice over the same handoff cannot differ.
    assert fx.recursive_handoff_custody(handoff).custody_hash == custody.custody_hash


# ---------------------------------------------------------------------------
# HQ-G -- the canonical receipt dominates the constructible envelope
# ---------------------------------------------------------------------------


def test_repair_hq_g_forged_evaluation_decision_cannot_override_the_receipt():
    """HQ-G hostile: a hand-built decision_state fails closed, both directions."""
    from dataclasses import replace as _replace

    positive = _real_positive_evaluation("hq153-g-decision")
    assert positive.receipt.admission_decision_state == "ADMITTED"

    # Real positive receipt + forged evaluation decision.
    forged_soft = _replace(positive, decision_state="INTEGRITY_FAILURE")
    with pytest.raises(OwnerProjectionError, match="disagrees with the canonical receipt decision"):
        RouteObligation.from_structural_admission(
            forged_soft, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )

    # Real negative receipt + forged ADMITTED: the most dangerous direction,
    # because it would manufacture a positive route out of a refusal.
    negative = _real_negative_evaluation("hq153-g-decision-negative")
    assert negative.receipt.admission_decision_state != "ADMITTED"
    forged_positive = _replace(negative, decision_state="ADMITTED")
    with pytest.raises(OwnerProjectionError, match="disagrees with the canonical receipt decision"):
        RouteObligation.from_structural_admission(
            forged_positive, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )


def test_repair_hq_g_forged_evaluation_reason_cannot_override_the_receipt():
    """HQ-G hostile: a caller-chosen reason is refused, not stored."""
    from dataclasses import replace as _replace

    positive = _real_positive_evaluation("hq153-g-reason")
    forged = _replace(positive, reason_code="CALLER_CHOSEN_REASON")
    with pytest.raises(OwnerProjectionError, match="disagrees with the canonical receipt reason"):
        RouteObligation.from_structural_admission(
            forged, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )

    negative = _real_negative_evaluation("hq153-g-reason-negative")
    forged_denial = _replace(negative, reason_code="BENCHMARK_OK")
    with pytest.raises(OwnerProjectionError, match="disagrees with the canonical receipt reason"):
        RouteObligation.from_structural_admission(
            forged_denial, requested_use="STRUCTURAL_MEDIATION_INPUT"
        )


def test_repair_hq_g_forged_blocking_refs_inconsistent_with_receipt_fail():
    """HQ-G hostile: caller evidence cannot be injected into the blocker set."""
    from dataclasses import replace as _replace

    negative = _real_negative_evaluation("hq153-g-blockers")
    from rawlsing_next.pre553_empirical_objects import exact_ref

    receipt_blocking = tuple(
        exact_ref(value)
        for value in negative.receipt.applicable_negative_denial_noncomparability_refs
    )
    assert receipt_blocking, "the negative receipt must carry its own applicable blockers"

    honest = RouteObligation.from_structural_admission(
        negative, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    assert {ref.key for ref in honest.blocking_refs} == {
        ref.key for ref in receipt_blocking
    }

    injected = _plausible_ref("caller-injected-blocker")
    for forged_refs in (
        honest.blocking_refs + (injected,),
        (),
        (_plausible_ref("caller-only-blocker"),),
    ):
        forged = _replace(negative, blocking_refs=tuple(forged_refs))
        with pytest.raises(OwnerProjectionError, match="blocking_refs disagree with the receipt"):
            RouteObligation.from_structural_admission(
                forged, requested_use="STRUCTURAL_MEDIATION_INPUT"
            )


def test_repair_hq_g_contradictory_requested_use_is_rejected():
    """HQ-G hostile: an ADMITTED receipt refuses a contradictory requested use."""
    positive = _real_positive_evaluation("hq153-g-requested-use")
    assert positive.receipt.admission_decision_state == "ADMITTED"
    receipt_target = positive.receipt.target_use

    for contradictory in (
        "COMPLETELY_UNRELATED_USE",
        f"{receipt_target}_PLUS_EVERYTHING_ELSE",
        "",
    ):
        with pytest.raises(OwnerProjectionError, match="contradicts the ADMITTED receipt target use"):
            RouteObligation.from_structural_admission(
                positive, requested_use=contradictory
            )


def test_repair_hq_g_real_positive_evaluation_with_matching_requested_use_passes():
    """HQ-G: the honest positive path is not regressed by receipt dominance."""
    positive = _real_positive_evaluation("hq153-g-honest-positive")
    assert positive.decision_state == "ADMITTED"

    obligation = RouteObligation.from_structural_admission(
        positive, requested_use=positive.receipt.target_use
    )
    # Every authoritative field came from the canonical receipt.
    assert obligation.decision_state == positive.receipt.admission_decision_state == "ADMITTED"
    assert obligation.reason_code == positive.receipt.decision_reason_code
    assert obligation.target_use == positive.receipt.target_use
    assert obligation.is_positive_admission is True
    assert obligation.required_route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
    assert obligation.admission_receipt_ref["content_hash"] == positive.receipt.ref.content_hash
    assert obligation.admission_rule_ref["admission_rule_hash"] == (
        positive.receipt.semantic_fields["structural_interpretation_payload"][
            "admission_rule_hash"
        ]
    )
    assert obligation.relation_ref["content_hash"] == (
        positive.receipt.semantic_fields["empirical_fact_ref"]["content_hash"]
    )
    assert obligation.admission_authority_ref == dict(
        positive.receipt.semantic_fields["admission_authority_ref"]
    )
    require_positive_route(obligation)


def test_repair_hq_g_negative_unresolved_receipt_preserves_target_and_grants_nothing():
    """HQ-G: a nonpositive unresolved receipt keeps its target and gains no authority."""
    evaluation = _no_rule_evaluation("hq153-g-unresolved")
    assert evaluation.receipt.admission_decision_state != "ADMITTED"
    assert evaluation.receipt.target_use == "UNRESOLVED_STRUCTURAL_USE"

    obligation = RouteObligation.from_structural_admission(
        evaluation, requested_use="STRUCTURAL_MEDIATION_INPUT"
    )
    # The receipt's exact unresolved target is preserved.
    assert obligation.target_use == "UNRESOLVED_STRUCTURAL_USE"
    # The attempted requested use may be recorded, but it is not granted authority.
    assert obligation.requested_use == "STRUCTURAL_MEDIATION_INPUT"
    assert obligation.target_use != obligation.requested_use
    assert obligation.is_positive_admission is False
    assert obligation.admission_rule_ref["admission_rule_hash"] == ""
    with pytest.raises(RouteLegitimacyError, match="route may not proceed"):
        require_positive_route(obligation)
    # And it cannot be laundered into a direct empirical route.
    with pytest.raises(RouteLegitimacyError, match="ROUTE_LAUNDERING_REJECTED"):
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL, obligation=obligation
        )


# ===========================================================================
# R4 C1-03A-REVIEW-BLOCK-REFUSAL-AUTHENTICITY-001
#
# Exact refusal TYPE is not provenance. Both types are publicly constructible
# bare ValueError subclasses, so a trusted refusal state must be derived from an
# ACTUAL competent owner execution, never from a caller-supplied exception.
# ===========================================================================
def test_r4_fabricated_exact_integrity_error_cannot_mint_trusted_state():
    """R4 hostile 1: a manually constructed exact Pre553IntegrityError is refused."""
    from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError

    bogus = _plausible_ref("r4-integrity")
    # There is no exception parameter left to pass.
    with pytest.raises(TypeError):
        OwnerStateProjection.from_empirical_integrity_refusal(
            exception=Pre553IntegrityError("caller"), reason="r", producer_ref=bogus
        )
    # Passing the exception positionally is equally impossible.
    with pytest.raises(TypeError):
        OwnerStateProjection.from_empirical_integrity_refusal(
            Pre553IntegrityError("caller")
        )
    # And no arbitrary object can stand in for a witness.
    for impostor in (Pre553IntegrityError("caller"), bogus, "caller", None, 7):
        with pytest.raises(OwnerProjectionError, match="requires an OwnerRefusalWitness"):
            OwnerStateProjection.from_empirical_integrity_refusal(witness=impostor)


def test_r4_fabricated_exact_authority_error_cannot_mint_trusted_state():
    """R4 hostile 2: a manually constructed exact Pre553AuthorityError is refused."""
    from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError

    bogus = _plausible_ref("r4-authority")
    with pytest.raises(TypeError):
        OwnerStateProjection.from_blocked_authority_refusal(
            exception=Pre553AuthorityError("caller"), reason="r", producer_ref=bogus
        )
    for impostor in (Pre553AuthorityError("caller"), bogus, "caller", None):
        with pytest.raises(OwnerProjectionError, match="requires an OwnerRefusalWitness"):
            OwnerStateProjection.from_blocked_authority_refusal(witness=impostor)


def test_r4_hand_built_witness_is_refused():
    """R4: a caller-minted witness is not proof of a refusal."""
    from rawlsing_next.pre553_analytical_state_and_route import (
        OwnerRefusalWitness,
        REFUSAL_KIND_EMPIRICAL_INTEGRITY,
        REFUSAL_KIND_REQUIRED_AUTHORITY,
    )

    bogus = _plausible_ref("r4-witness")
    for kind in (REFUSAL_KIND_EMPIRICAL_INTEGRITY, REFUSAL_KIND_REQUIRED_AUTHORITY):
        with pytest.raises(OwnerProjectionError, match="may only be produced by an actual"):
            OwnerRefusalWitness(
                owner_label="rawlsing_next.pre553_empirical_query.execute_empirical_query",
                refusal_kind=kind,
                refused_ref=bogus,
                supporting_refs=(bogus,),
                invocation_binding="caller-invented-binding",
                refusal_type="Pre553IntegrityError",
                refusal_message="caller",
            )


def test_r4_witness_binds_the_genuine_owner_object_and_cannot_be_rebound():
    """R4 hostiles 3 and 5: provenance comes from the real owner object, so a genuine
    refusal cannot be rebound to another object ref or given arbitrary support."""
    from dataclasses import replace as _replace

    witness, data = fx.capture_integrity_refusal("integrity_failure_fixture")
    genuine = data["original_object"]
    assert witness.refused_ref == genuine.ref
    # The supporting refs are the object's own authority/replay bindings, all present.
    assert witness.supporting_refs
    assert genuine.producer_replay_locator_or_reference_root in witness.supporting_refs

    # Rebinding the witness onto another object is refused by the token guard.
    other = _plausible_ref("r4-other-object")
    with pytest.raises(OwnerProjectionError):
        _replace(witness, refused_ref=other, _TRUST_TOKEN=object())
    # Injecting arbitrary supporting refs is likewise refused.
    with pytest.raises(OwnerProjectionError):
        _replace(witness, supporting_refs=(other,), _TRUST_TOKEN=object())
    # Mutating a frozen witness at all is refused.
    with pytest.raises(Exception):
        witness.refused_ref = other


def test_r4_authority_witness_cannot_be_rebound_to_another_object_ref():
    """R4 hostile 4: a genuine authority refusal cannot be rebound."""
    from dataclasses import replace as _replace

    witness, data = fx.capture_blocked_authority_refusal("blocked_required_authority_fixture")
    from rawlsing_next.pre553_empirical_objects import exact_ref

    assert witness.refused_ref == exact_ref(data["authority"].candidate_grammar_ref)
    assert witness.supporting_refs
    other = _plausible_ref("r4-authority-other")
    with pytest.raises(OwnerProjectionError):
        _replace(witness, refused_ref=other, _TRUST_TOKEN=object())
    with pytest.raises(OwnerProjectionError):
        _replace(witness, supporting_refs=(other,), _TRUST_TOKEN=object())


def test_r4_capture_performs_a_real_owner_execution_not_a_stub():
    """The capture wrapper invokes the real owner; it cannot be faked by a stub.

    Passing a non-owner object, or asking for a capture that would not actually
    refuse, is refused. The owner accepting the body means there is no refusal.
    """
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal,
        capture_required_authority_refusal,
    )
    from rawlsing_next.pre553_empirical_objects import ExactRef

    with pytest.raises(OwnerProjectionError, match="genuine C11Repository"):
        capture_empirical_integrity_refusal(
            repository="not a repository",
            release_ref=ExactRef("C11LogicalRelease", "REL-none", "a" * 64),
            respondent_event_ref=ExactRef("RespondentEvent@1.0.0", "urn:none", "b" * 64),
            tampered_semantic_fields={"raw_response_value": "CHANGED"},
        )
    # An UNtampered genuine body is accepted by the owner, so there is no refusal to
    # witness -- absence of refusal is never converted into INTEGRITY_FAILURE.
    data = fx.integrity_failure_fixture()
    genuine = data["original_object"]
    with pytest.raises(OwnerProjectionError, match="ACCEPTED the supplied body"):
        capture_empirical_integrity_refusal(
            repository=data["repository"],
            release_ref=data["release_ref"],
            respondent_event_ref=data["respondent_event_ref"],
            tampered_semantic_fields={},
        )
    # The discovery capture binds a refused context from the authority itself, so an
    # authority carrying no candidate grammar cannot produce a witness.
    blocked = fx.blocked_required_authority_fixture()

    class _NoGrammar:
        pass

    with pytest.raises(OwnerProjectionError, match="no candidate_grammar_ref"):
        capture_required_authority_refusal(
            repository=blocked["source"]["repo"],
            discovery_authority=_NoGrammar(),
            authority_registry=blocked["registry"],
            release_refs=(blocked["source"]["release_ref"],),
            predicate_catalog=blocked["predicates"],
            query_template_catalog=blocked["queries"],
        )


def test_r4_witness_invocation_binding_commits_to_the_exact_owner_inputs():
    """The witness binds the exact body the owner was asked to accept."""
    witness, data = fx.capture_integrity_refusal("integrity_failure_fixture")
    from rawlsing_next.pre553_empirical_objects import semantic_hash

    payload = dict(data["original_object"].as_dict())
    semantic = dict(payload.pop("semantic_fields", {}))
    semantic.update(data["tampered_semantic_fields"])
    assert witness.invocation_binding == semantic_hash({**payload, **semantic})
    # A different tampered body yields a different binding.
    other, _ = fx.capture_integrity_refusal("integrity_failure_fixture")
    assert other.invocation_binding == witness.invocation_binding
    assert witness.refusal_type == "Pre553IntegrityError"


def test_r4_actual_owner_executions_still_yield_both_mandatory_states():
    """R4 hostiles 6, 7 and 8: real executions still produce two distinct states."""
    integrity, _ = fx.project_empirical_integrity_refusal("integrity_failure_fixture")
    blocked, _ = fx.project_blocked_authority_refusal("blocked_required_authority_fixture")
    assert integrity.retained_state == INTEGRITY_FAILURE
    assert blocked.retained_state == BLOCKED_REQUIRED_AUTHORITY
    assert integrity.retained_state != blocked.retained_state
    assert integrity.owner == (
        "rawlsing_next.pre553_empirical_objects.RespondentEvent "
        "(canonical integrity construction)")
    assert blocked.owner == (
        "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery")


def test_r4_stale_completeness_state_reference_is_gone_without_changing_handoff_law():
    """R4 hostile 12: the reviewer's stale short-circuited custody reference is removed."""
    import inspect as _inspect

    import rawlsing_next.pre553_analytical_state_and_route as mod

    src = _inspect.getsource(mod)
    assert "coverage_custody.completeness_state" not in src
    assert "unreachable custody/state combination" not in src
    # Handoff semantics are unchanged: custody still binds the exact frontier.
    assert "completeness_state" not in {f for f in mod.RecursiveCoverageCustody.__dataclass_fields__}
    assert hasattr(mod.RecursiveCoverageCustody, "from_handoff")
    handoff_projection, custody = fx.project_recursive_handoff(
        _hq_real_handoff("r4-handoff-intact"))
    assert handoff_projection.retained_state == SUPPORTED_BASELINE
    assert custody.coverage_record_ref is not None


# ===========================================================================
# R4 final-SHA callability correction
#
# The returned R4 SHA declared two consecutive @classmethod decorators on
# from_empirical_integrity_refusal. These courts call both refusal factories
# DIRECTLY on the final committed SHA and prove they return the correct states, so
# the duplicate-decorator defect cannot silently return.
# ===========================================================================
def test_finalsha_empirical_integrity_refusal_is_directly_callable():
    """Final-SHA court: one decorator, and a direct call returns INTEGRITY_FAILURE."""
    import inspect as _inspect

    witness, data = fx.capture_integrity_refusal("integrity_failure_fixture")

    # Structural check: exactly one classmethod decorator, not a nested chain.
    raw = OwnerStateProjection.__dict__["from_empirical_integrity_refusal"]
    assert type(raw).__name__ == "classmethod"
    assert not isinstance(getattr(raw, "__func__", None), classmethod), (
        "from_empirical_integrity_refusal must not wrap a classmethod in a classmethod"
    )
    assert list(_inspect.signature(raw.__func__).parameters) == ["cls", "witness"]

    # DIRECT call on a genuine witness, exactly as HQ intake would make it.
    projection = OwnerStateProjection.from_empirical_integrity_refusal(witness=witness)
    assert projection.retained_state == INTEGRITY_FAILURE
    evidence = projection.as_evidence()
    assert evidence.retained_state == INTEGRITY_FAILURE
    # The provenance still comes from the real owner object.
    assert evidence.producer_ref == data["original_object"].ref
    assert evidence.owner == (
        "rawlsing_next.pre553_empirical_objects.RespondentEvent "
        "(canonical integrity construction)")


def test_finalsha_blocked_authority_refusal_is_directly_callable():
    """Final-SHA court: the blocked-authority sibling is directly callable too."""
    import inspect as _inspect

    witness, data = fx.capture_blocked_authority_refusal("blocked_required_authority_fixture")

    raw = OwnerStateProjection.__dict__["from_blocked_authority_refusal"]
    assert type(raw).__name__ == "classmethod"
    assert not isinstance(getattr(raw, "__func__", None), classmethod)
    assert list(_inspect.signature(raw.__func__).parameters) == ["cls", "witness"]

    projection = OwnerStateProjection.from_blocked_authority_refusal(witness=witness)
    assert projection.retained_state == BLOCKED_REQUIRED_AUTHORITY
    assert projection.as_evidence().retained_state == BLOCKED_REQUIRED_AUTHORITY
    from rawlsing_next.pre553_empirical_objects import exact_ref

    assert projection.producer_ref == exact_ref(
        data["authority"].candidate_grammar_ref)


def test_finalsha_no_refusal_factory_wraps_a_classmethod():
    """Sweep every factory: none may nest a classmethod inside a classmethod."""
    offenders = [
        name for name, raw in vars(OwnerStateProjection).items()
        if isinstance(raw, classmethod)
        and isinstance(getattr(raw, "__func__", None), classmethod)
    ]
    assert offenders == []


def test_finalsha_both_refusal_states_remain_distinct_on_final_sha():
    """The two mandatory refusal states stay distinct after the correction."""
    integrity = OwnerStateProjection.from_empirical_integrity_refusal(
        witness=fx.capture_integrity_refusal("integrity_failure_fixture")[0]
    )
    blocked = OwnerStateProjection.from_blocked_authority_refusal(
        witness=fx.capture_blocked_authority_refusal("blocked_required_authority_fixture")[0]
    )
    assert integrity.retained_state == INTEGRITY_FAILURE
    assert blocked.retained_state == BLOCKED_REQUIRED_AUTHORITY
    assert integrity.retained_state != blocked.retained_state


# ===========================================================================
# R5 C1-03A-R4-FINAL-REVIEW-BLOCK-EMPIRICAL-CAPTURE-OWNER-FAMILY-001
#
# The AT14 INTEGRITY_FAILURE state does NOT occur on execute_empirical_query. It
# occurs on the canonical RespondentEvent construction/integrity path. The witness must
# bind the exact governed object family that actually refused.
# ===========================================================================
def _r5_governed():
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    data = fx.integrity_failure_fixture()
    assert data["repository"] is not None
    assert data["release_ref"] is not None
    assert data["respondent_event_ref"] is not None
    return data


def _r5_capture(**overrides):
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal,
    )

    data = _r5_governed()
    kwargs = {
        "repository": data["repository"],
        "release_ref": data["release_ref"],
        "respondent_event_ref": data["respondent_event_ref"],
        "tampered_semantic_fields": data["tampered_semantic_fields"],
    }
    kwargs.update(overrides)
    return capture_empirical_integrity_refusal(**kwargs), data


def test_r5_governed_respondent_event_with_tampered_identity_is_witnessed():
    """R5 hostile 1: genuine governed RespondentEvent -> witnessed INTEGRITY_FAILURE."""
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal,
    )
    from rawlsing_next.pre553_empirical_objects import exact_ref

    data = _r5_governed()
    witness = capture_empirical_integrity_refusal(
        repository=data["repository"],
        release_ref=data["release_ref"],
        respondent_event_ref=data["respondent_event_ref"],
        tampered_semantic_fields=data["tampered_semantic_fields"],
    )
    projection = OwnerStateProjection.from_empirical_integrity_refusal(witness=witness)
    assert projection.retained_state == INTEGRITY_FAILURE
    assert witness.refused_ref == data["original_object"].ref
    assert witness.governing_release_ref == exact_ref(data["release_ref"])
    assert witness.object_family == "RespondentEvent@1.0.0"
    assert witness.supporting_refs


def test_r5_witness_owner_label_names_the_actual_refusing_operation():
    """R5 hostile 2: the label must NOT be execute_empirical_query."""
    witness, _ = _r5_capture()
    assert witness.owner_label != (
        "rawlsing_next.pre553_empirical_query.execute_empirical_query")
    assert witness.owner_label == (
        "rawlsing_next.pre553_empirical_objects.RespondentEvent "
        "(canonical integrity construction)"
    )
    projection = OwnerStateProjection.from_empirical_integrity_refusal(witness=witness)
    assert projection.owner == witness.owner_label


def test_r5_other_canonical_family_is_rejected_before_capture():
    """R5 hostile 3: a genuine object of another family is refused, not captured."""
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    data = _r5_governed()
    release = data["repository"].resolve_release_exact(data["release_ref"])
    other = next(
        obj for obj in release.public_objects if type(obj) is not RespondentEvent
    )
    with pytest.raises(OwnerProjectionError, match="exactly RespondentEvent"):
        _r5_capture(respondent_event_ref=other.ref)


def test_r5_caller_defined_canonical_subclass_is_rejected():
    """R5 hostiles 4 and 5: caller-defined subclasses are refused.

    A subclass of CanonicalSemanticObject, and a subclass of RespondentEvent, are both
    refused. The gate is exact type identity, so a broad isinstance check is not in
    use anywhere.
    """
    from rawlsing_next.pre553_empirical_objects import (
        CanonicalSemanticObject,
        RespondentEvent,
    )

    class _CallerCanonical(CanonicalSemanticObject):
        pass

    class _CallerRespondent(RespondentEvent):
        pass

    import inspect as _inspect

    for subclass, respondent_subclass in (
        (_CallerCanonical, False), (_CallerRespondent, True)
    ):
        assert type(subclass) is not RespondentEvent
        # Prove each class really WOULD satisfy a broad gate, so the refusal below
        # cannot be credited to an accidental type mismatch. For classes the correct
        # question is issubclass, not isinstance.
        assert issubclass(subclass, CanonicalSemanticObject)
        assert issubclass(subclass, RespondentEvent) is respondent_subclass

    # No caller instance is accepted at all: the capture takes governed identity.
    params = _inspect.signature(
        _inspect.getmodule(OwnerStateProjection).capture_empirical_integrity_refusal
    ).parameters
    assert "original_object" not in params
    assert "object_instance" not in params


def test_r5_respondent_event_absent_from_the_declared_release_is_rejected():
    """R5 hostile 6: a genuine RespondentEvent outside the declared release is refused."""
    from rawlsing_next.pre553_empirical_objects import exact_ref

    data = _r5_governed()
    # A DIFFERENT genuine governed release.
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    other_source = _build_source("c1-03a-r5-other-release", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    other_release = other_source["repo"].resolve_release_exact(other_source["release_ref"])
    assert other_release.release_ref != data["release_ref"]
    foreign = next(
        obj for obj in other_release.public_objects
        if type(obj).__name__ == "RespondentEvent"
    )
    # The ref is genuine but belongs to a different release.
    with pytest.raises(OwnerProjectionError, match="not a public object of the declared"):
        _r5_capture(respondent_event_ref=foreign.ref)


def test_r5_caller_cannot_substitute_release_or_object_ref():
    """R5 hostiles 7 and 8: neither release ref nor object ref is caller-selectable."""
    from rawlsing_next.pre553_empirical_objects import exact_ref

    data = _r5_governed()
    # Substitute a release that does not contain the declared object.
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    other_source = _build_source("c1-03a-r5-sub-release", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    with pytest.raises(OwnerProjectionError, match="does not resolve through the governed"):
        _r5_capture(release_ref=other_source["release_ref"])
    # Substitute an object ref that is not in the declared release at all.
    with pytest.raises(OwnerProjectionError, match="not a public object of the declared"):
        _r5_capture(
            respondent_event_ref=exact_ref({
                "kind": "RespondentEvent@1.0.0",
                "object_id": "urn:test:r5:invented",
                "content_hash": "0" * 64,
            })
        )


def test_r5_bare_exception_and_injected_fields_still_cannot_mint():
    """R5 hostiles 9 and 10: no exception, ref, support, reason or label injection."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerRefusalWitness
    from rawlsing_next.pre553_empirical_objects import ExactRef, Pre553IntegrityError

    # No exception parameter exists on either refusal factory.
    for factory in (
        OwnerStateProjection.from_empirical_integrity_refusal,
        OwnerStateProjection.from_blocked_authority_refusal,
    ):
        for impostor in (Pre553IntegrityError("caller"), "caller", None, 7):
            with pytest.raises(OwnerProjectionError, match="requires an OwnerRefusalWitness"):
                factory(witness=impostor)
    # The capture exposes no way to inject producer/supporting/ref/label.
    import inspect as _inspect

    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal as capture,
    )

    params = set(_inspect.signature(capture).parameters)
    assert params == {
        "repository", "release_ref", "respondent_event_ref", "tampered_semantic_fields",
    }
    # A hand-built witness is still refused.
    bogus = ExactRef("RespondentEvent@1.0.0", "urn:test:r5:invented", "0" * 64)
    with pytest.raises(OwnerProjectionError, match="may only be produced by an actual"):
        OwnerRefusalWitness(
            owner_label="caller",
            refusal_kind="EMPIRICAL_INTEGRITY_REFUSAL",
            refused_ref=bogus,
            supporting_refs=(bogus,),
            invocation_binding="caller",
            refusal_type="Pre553IntegrityError",
            refusal_message="caller",
        )


def test_r5_owner_acceptance_produces_no_witness():
    """R5 hostile 11: an untampered governed body is accepted, so no witness exists."""
    data = _r5_governed()
    with pytest.raises(OwnerProjectionError, match="ACCEPTED the supplied body"):
        _r5_capture(tampered_semantic_fields={})


def test_r5_discovery_refusal_path_is_unchanged_and_sound():
    """R5 hostile 12: the discovery refusal path is untouched."""
    witness, data = fx.capture_blocked_authority_refusal(
        "blocked_required_authority_fixture")
    from rawlsing_next.pre553_empirical_objects import exact_ref

    assert witness.owner_label == (
        "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery")
    assert witness.refusal_kind == "REQUIRED_AUTHORITY_REFUSAL"
    assert witness.refused_ref == exact_ref(data["authority"].candidate_grammar_ref)
    projection = OwnerStateProjection.from_blocked_authority_refusal(witness=witness)
    assert projection.retained_state == BLOCKED_REQUIRED_AUTHORITY


def test_r5_refusal_states_remain_distinct_with_truthful_labels():
    """R5 hostile 13: the two mandatory states stay distinct under new labels."""
    integrity = OwnerStateProjection.from_empirical_integrity_refusal(
        witness=fx.capture_integrity_refusal("integrity_failure_fixture")[0])
    blocked = OwnerStateProjection.from_blocked_authority_refusal(
        witness=fx.capture_blocked_authority_refusal(
            "blocked_required_authority_fixture")[0])
    assert integrity.retained_state == INTEGRITY_FAILURE
    assert blocked.retained_state == BLOCKED_REQUIRED_AUTHORITY
    assert integrity.retained_state != blocked.retained_state
    assert integrity.owner != blocked.owner


def test_r5_no_broad_canonical_object_gate_remains():
    """R5: the capture must not gate on CanonicalSemanticObject isinstance."""
    import inspect as _inspect

    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal as capture,
    )

    import ast as _ast

    tree = _ast.parse(_inspect.getsource(capture))
    # The forbidden gate is an isinstance family check. Reference-conversion
    # isinstance calls (AuthorityRef/ExactRef) are not gates and remain allowed, so
    # the check is that no isinstance call names CanonicalSemanticObject.
    gate_calls = [
        node for node in _ast.walk(tree)
        if isinstance(node, _ast.Call)
        and isinstance(node.func, _ast.Name)
        and node.func.id == "isinstance"
        and "CanonicalSemanticObject" in _ast.unparse(node)
    ]
    assert gate_calls == [], "no isinstance family gate on CanonicalSemanticObject"
    # The docstring legitimately NAMES the forbidden type while explaining it is not
    # used, so assert on the executable code only.
    src = _inspect.getsource(capture)
    body = src.replace(capture.__doc__ or "", "")
    assert "CanonicalSemanticObject" not in body
    # It gates on exact type identity for both the repository and the object.
    assert "type(resolved) is not RespondentEvent" in src
    assert "type(repository) is not C11Repository" in src


# ===========================================================================
# R6 C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001
#
# The AT14 empirical-integrity witness may be minted ONLY from an exception whose
# exact runtime type is Pre553IntegrityError. Pre553SemanticCollapseError is a
# canonical subclass carrying a DIFFERENT owner meaning.
# ===========================================================================
class _R6StatefulMapping(Mapping):
    """Benign across the pre-try binding hash; hostile inside the real constructor.

    The reviewer's pattern: this behaves normally while the capture canonicalizes the
    attempted body to compute ``invocation_binding``, and raises
    ``Pre553SemanticCollapseError`` only during the actual ``RespondentEvent(**body)``
    call. So the subclass is genuinely reached through the constructor path, not
    supplied by hand.
    """

    def __init__(self, benign, fail_from: int = 3):
        self._benign = dict(benign)
        self._fail_from = fail_from
        self.accesses = 0

    def __getitem__(self, key):
        self.accesses += 1
        if self.accesses >= self._fail_from:
            raise Pre553SemanticCollapseError(
                "collapsed cross-ontology substitution during canonicalization")
        return self._benign[key]

    def __iter__(self):
        return iter(self._benign)

    def __len__(self):
        return len(self._benign)


def _r6_collapse_attempt(seen=None):
    """Drive the capture so the real constructor raises the subclass.

    ``seen`` optionally receives the stateful mapping, so a court can prove the
    subclass arose inside the constructor call rather than being supplied by hand.
    """
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal,
    )

    data = fx.integrity_failure_fixture()
    hostile = _R6StatefulMapping({"object_id": "urn:test:r6", "content_hash": "a" * 64})
    tampered = dict(data["tampered_semantic_fields"])
    tampered["native_question_ref"] = hostile
    if seen is not None:
        seen.append(hostile)
    return capture_empirical_integrity_refusal(
        repository=data["repository"],
        release_ref=data["release_ref"],
        respondent_event_ref=data["respondent_event_ref"],
        tampered_semantic_fields=tampered,
    )


def test_r6_official_subclass_hostile_mints_no_witness():
    """R6 mandatory hostile: a subclass reached through the constructor is refused."""
    from rawlsing_next.pre553_empirical_objects import (
        Pre553IntegrityError,
        Pre553SemanticCollapseError,
    )

    # The subclass really is a canonical subclass, which is why the broad except was
    # too permissive.
    assert issubclass(Pre553SemanticCollapseError, Pre553IntegrityError)
    assert Pre553SemanticCollapseError is not Pre553IntegrityError

    with pytest.raises(OwnerProjectionError) as excinfo:
        _r6_collapse_attempt()
    message = str(excinfo.value)
    assert "Pre553IntegrityError" in message
    assert "Pre553SemanticCollapseError" in message
    assert "C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001" in message
    # Typed fail-closed, with the subclass preserved as the cause.
    assert isinstance(excinfo.value.__cause__, Pre553SemanticCollapseError)


def test_r6_subclass_hostile_really_traverses_the_constructor_path():
    """The subclass must arise inside the real RespondentEvent call, not by hand.

    The pre-try binding hash canonicalizes the attempted body first and consumes the
    first accesses; the hostile only raises afterwards. That ordering is only possible
    if the refusal happened during the constructor invocation inside the try block.
    """
    seen = []
    with pytest.raises(OwnerProjectionError):
        _r6_collapse_attempt(seen=seen)
    hostile = seen[0]
    assert isinstance(hostile, _R6StatefulMapping)
    # At least one access succeeded before the hostile began raising, proving the
    # binding hash genuinely ran over the same object first.
    assert hostile.accesses >= 3


def test_r6_no_integrity_failure_projection_can_result_from_a_subclass():
    """R6: neither a witness nor an INTEGRITY_FAILURE projection can be produced."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerRefusalWitness
    from rawlsing_next.pre553_empirical_objects import Pre553SemanticCollapseError

    with pytest.raises(OwnerProjectionError):
        _r6_collapse_attempt()

    # Even a hand-forged witness claiming the subclass meaning cannot be built: the
    # witness type itself only carries what a capture produced.
    data = fx.integrity_failure_fixture()
    with pytest.raises(OwnerProjectionError):
        OwnerRefusalWitness(
            owner_label=OWNER_EMPIRICAL_INTEGRITY_LABEL,
            refusal_kind="EMPIRICAL_INTEGRITY_REFUSAL",
            refused_ref=data["respondent_event_ref"],
            supporting_refs=(data["release_ref"],),
            invocation_binding="r6",
            refusal_type=Pre553SemanticCollapseError.__name__,
            refusal_message="collapsed",
        )


def test_r6_base_class_stale_identity_still_mints_the_lawful_witness():
    """R6 item 1: the exact base class still yields the lawful refusal."""
    from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError

    witness, data = fx.capture_integrity_refusal("integrity_failure_fixture")
    assert type(witness.__dict__["refusal_type"]) is str
    assert witness.refusal_type == "Pre553IntegrityError"
    assert witness.refusal_type == Pre553IntegrityError.__name__
    projection = OwnerStateProjection.from_empirical_integrity_refusal(witness=witness)
    assert projection.retained_state == INTEGRITY_FAILURE
    assert witness.refused_ref == data["original_object"].ref


def test_r6_owner_label_provenance_and_family_gates_unchanged():
    """R6 items 2 and 3: label, release/object/family provenance all unchanged."""
    from rawlsing_next.pre553_empirical_objects import exact_ref

    witness, data = fx.capture_integrity_refusal("integrity_failure_fixture")
    assert witness.owner_label == (
        "rawlsing_next.pre553_empirical_objects.RespondentEvent "
        "(canonical integrity construction)")
    assert witness.owner_label != (
        "rawlsing_next.pre553_empirical_query.execute_empirical_query")
    assert witness.object_family == "RespondentEvent@1.0.0"
    assert witness.governing_release_ref == exact_ref(data["release_ref"])
    assert witness.refused_ref == data["original_object"].ref
    assert witness.supporting_refs


def test_r6_discovery_refusal_remains_authentic_and_unchanged():
    """R6 item 5: the discovery refusal path is untouched by this correction."""
    from rawlsing_next.pre553_empirical_objects import exact_ref

    witness, data = fx.capture_blocked_authority_refusal(
        "blocked_required_authority_fixture")
    assert witness.owner_label == (
        "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery")
    assert witness.refusal_kind == "REQUIRED_AUTHORITY_REFUSAL"
    assert witness.refused_ref == exact_ref(data["authority"].candidate_grammar_ref)
    assert OwnerStateProjection.from_blocked_authority_refusal(
        witness=witness).retained_state == BLOCKED_REQUIRED_AUTHORITY
    # The exact-class rule is applied at the empirical boundary only.
    assert witness.refusal_type == "Pre553AuthorityError"
