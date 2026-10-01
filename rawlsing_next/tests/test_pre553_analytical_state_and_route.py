"""C1-03A courts: AT14 negative-state conservation, AT15 route legitimacy, AT16 final consumer.

Every court drives a competent current owner through its public path. No state
label is manufactured inside a wrapper, and no handmade final slice is used to
satisfy AT16.
"""
from __future__ import annotations

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
    classify_adaptive_coverage,
    classify_discovery_receipt_state,
    classify_empirical_cells,
    classify_empirical_fact_state,
    observed_zero_cells,
)
from rawlsing_next.tests import c1_at14_at16_fixture as fx


def _envelope(retained, *, route=ROUTE_DIRECT_EMPIRICAL, fixture_refs=(), **kwargs):
    """Build a bounded envelope from one competent producer state."""
    disposition = kwargs.pop("disposition", None) or fx.consumer_disposition_for(retained)
    owner = kwargs.pop("owner", fx.OWNER_EMPIRICAL)
    producer_state = kwargs.pop("producer_state", retained)
    reason = kwargs.pop("reason", "owner-native state")
    coverage_state = kwargs.pop("coverage_state", "NOT_APPLICABLE")
    evidence = fx.producer_evidence_for(
        owner=owner,
        producer_state=producer_state,
        retained_state=retained,
        reason=reason,
        producer_ref=fixture_refs[0],
        supporting_refs=fixture_refs,
        coverage_state=coverage_state,
    )
    return build_state_route_result(
        route_class=route,
        producer_evidence=[evidence],
        producer_refs=list(fixture_refs),
        consumer_disposition=disposition,
        reason=reason,
        coverage_state=coverage_state,
        **kwargs,
    )


# ===========================================================================
# AT14 - negative-state conservation
# ===========================================================================


def test_at14_observed_zero_is_retained_and_is_not_valid_empty():
    """AT14(1): observed zero in a nonzero denominator stays its own state."""
    data = fx.observed_zero_fixture()
    fact = data["fact"]
    assert fact.raw_denominator_support == 2, "observed zero requires positive support"
    zero_cells = data["observed_zero_cells"]
    assert zero_cells, "fixture must expose a supported observed-zero cell"

    retained = classify_empirical_cells(
        fact.typed_state, fact.target_topology["complete_cell_semantic_projection"]
    )
    assert fact.typed_state == "SUPPORTED"
    assert retained == OBSERVED_ZERO
    assert tuple(zero_cells) == observed_zero_cells(
        fact.target_topology["complete_cell_semantic_projection"]
    )
    # Observed zero is NOT valid-empty and NOT zero support.
    assert retained != VALID_EMPTY
    assert retained != UNDERPOWERED

    result = _envelope(
        retained,
        producer_state=fact.typed_state,
        reason="positive denominator with an exact zero numerator cell",
        fixture_refs=(fact.ref,),
    )
    assert result.retained_analytical_state == OBSERVED_ZERO
    # Observed zero is lawfully consumer-invocable, but this AT14 court asserts
    # only the state conservation. The real invocation is proven in the AT16
    # positive-path court, which drives the actual consumer.
    assert not result.consumer_disposition.consumer_invoked
    assert "lawfully" in result.consumer_disposition.non_invocation_reason


def test_at14_zero_support_is_distinct_from_observed_zero_and_valid_empty():
    """AT14(1)+(2): zero support is neither observed zero nor valid-empty."""
    zero_support = fx.zero_support_fixture()
    observed = fx.observed_zero_fixture()

    zero_retained = classify_empirical_fact_state(zero_support["producer_state"])
    observed_retained = classify_empirical_fact_state(observed["producer_state"])
    valid_empty_retained = classify_empirical_fact_state(fx.valid_empty_fixture()["producer_state"])

    assert zero_support["producer_state"] == "ZERO_SUPPORT"
    assert zero_support["raw_denominator_support"] == 0
    assert zero_retained == UNDERPOWERED
    # Three distinct retained states, no collapse.
    assert len({zero_retained, observed_retained, valid_empty_retained}) == 3


def test_at14_valid_empty_is_retained_from_its_own_owner():
    """AT14(2): VALID_EMPTY comes from the declared-empty target domain."""
    data = fx.valid_empty_fixture()
    assert data["producer_state"] == "VALID_EMPTY"
    assert data["raw_denominator_support"] > 0, "valid-empty has a positive denominator"
    retained = classify_empirical_fact_state(data["producer_state"])
    assert retained == VALID_EMPTY
    result = _envelope(retained, producer_state=data["producer_state"],
                       reason=data["reason"], fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == VALID_EMPTY
    assert not result.consumer_disposition.consumer_invoked
    assert result.consumer_disposition.non_invocation_reason


def test_at14_underpowered_is_retained_and_distinct_from_unresolved():
    """AT14(3)+(4): underpowered never collapses into unknown/unresolved."""
    underpowered = fx.underpowered_fixture()
    unresolved = fx.unresolved_fixture()

    under_retained = classify_discovery_receipt_state(
        underpowered["producer_state"], underpowered["coverage_state"]
    )
    unresolved_retained = classify_empirical_fact_state(unresolved["producer_state"])

    assert underpowered["producer_state"] == "INSUFFICIENT_SUPPORT"
    assert underpowered["coverage_state"] == "EVALUATED_UNDERPOWERED"
    assert under_retained == UNDERPOWERED
    assert unresolved_retained == UNKNOWN_UNRESOLVED
    # The two remain distinct, and neither becomes valid-empty or observed zero.
    assert under_retained != unresolved_retained
    assert under_retained not in (VALID_EMPTY, OBSERVED_ZERO, UNVISITED)


def test_at14_unresolved_is_retained_from_the_empirical_owner():
    """AT14(4): UNKNOWN/UNRESOLVED is retained with its own reason."""
    data = fx.unresolved_fixture()
    assert data["producer_state"] == "UNRESOLVED"
    retained = classify_empirical_fact_state(data["producer_state"])
    assert retained == UNKNOWN_UNRESOLVED
    result = _envelope(retained, producer_state=data["producer_state"],
                       reason=data["reason"], fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == UNKNOWN_UNRESOLVED
    # Never coerced into valid-empty, observed zero, or a supported result.
    assert result.retained_analytical_state not in (VALID_EMPTY, OBSERVED_ZERO)
    assert result.negative_claim_authorized is False


def test_at14_unvisited_comes_from_the_real_adaptive_owner():
    """AT14(5): UNVISITED is produced by the adaptive owner, not invented."""
    data = fx.unvisited_adaptive_fixture()
    adaptive = data["adaptive_result"]

    # The adaptive owner really ran and really left territory unvisited.
    assert adaptive.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert adaptive.unvisited_unit_refs
    assert adaptive.visited_unit_refs
    assert adaptive.global_negative_claim is False
    assert adaptive.semantic_truth_effect is False

    retained = classify_adaptive_coverage(adaptive.completeness_state)
    assert retained == UNVISITED

    result = _envelope(
        retained,
        owner=fx.OWNER_ADAPTIVE,
        producer_state=adaptive.completeness_state,
        reason=data["reason"],
        fixture_refs=(data["determinant_state_ref"],),
        coverage_state=adaptive.completeness_state,
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
    data = fx.noncomparable_fixture()
    assert data["producer_state"] == "NONCOMPARABLE"
    retained = classify_empirical_fact_state(data["producer_state"])
    assert retained == NONCOMPARABLE
    assert retained != UNKNOWN_UNRESOLVED
    assert retained != VALID_EMPTY
    result = _envelope(retained, producer_state=data["producer_state"],
                       reason=data["reason"], fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == NONCOMPARABLE


def test_at14_blocked_by_absent_or_denying_authority_is_its_own_state():
    """AT14(7): a denying authority blocks; it is not empirical absence."""
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery

    data = fx.blocked_required_authority_fixture()
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

    retained = classify_discovery_receipt_state(data["producer_state"])
    assert retained == BLOCKED_REQUIRED_AUTHORITY
    # Blocked is not absence, not valid-empty, not observed zero, not unresolved.
    assert retained not in (OBSERVED_ZERO, VALID_EMPTY, UNKNOWN_UNRESOLVED, UNVISITED)


def test_at14_integrity_failure_cannot_become_valid_empty():
    """AT14(8): INTEGRITY_FAILURE stays integrity failure."""
    data = fx.integrity_failure_fixture()
    assert data["exception_type"] == "Pre553IntegrityError"
    retained = classify_empirical_fact_state(data["producer_state"])
    assert retained == INTEGRITY_FAILURE
    assert retained != VALID_EMPTY
    assert retained != OBSERVED_ZERO
    result = _envelope(retained, producer_state=data["producer_state"],
                       reason=data["reason"], fixture_refs=(data["corrupted_object_ref"],))
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

    # Claiming UNVISITED while handing over only the positive handoff, with no
    # unvisited territory from the adaptive owner, must fail closed.
    with pytest.raises(C103AStateRouteError, match="must carry exact unvisited refs"):
        _envelope(
            UNVISITED,
            owner=fx.OWNER_ADAPTIVE,
            producer_state="PARTIAL_BUDGET_EXHAUSTED",
            reason="positive handoff relabelled as unvisited coverage",
            fixture_refs=(handoff.ref,),
            coverage_state="PARTIAL_BUDGET_EXHAUSTED",
            coverage_record_ref=gen1.discovery_result.evaluated_frontier_ref,
            unvisited_refs=(),
        )

    # And a retained positive may not smuggle in unvisited territory either.
    with pytest.raises(C103AStateRouteError, match="only be retained on the UNVISITED state"):
        _envelope(
            OBSERVED_ZERO,
            producer_state="OBSERVED_ZERO",
            reason="positive relabelled with unvisited territory",
            fixture_refs=(handoff.ref,),
            unvisited_refs=(handoff.ref,),
        )


# ===========================================================================
# AT15 - direct-route legitimacy
# ===========================================================================


def test_at15_competent_direct_empirical_route_stays_direct():
    """AT15(1): a competent direct empirical route is consumed without a learned wrapper."""
    data = fx.observed_zero_fixture()
    fact = data["fact"]
    retained = classify_empirical_fact_state(fact.typed_state)

    result = _envelope(
        retained,
        route=ROUTE_DIRECT_EMPIRICAL,
        producer_state=fact.typed_state,
        reason="exact direct empirical contract is already sufficient",
        fixture_refs=(fact.ref,),
    )
    # No learned/adjudicated authority was demanded or invented.
    assert result.route_class == ROUTE_DIRECT_EMPIRICAL
    assert result.authority_refs == ()


def test_at15_structural_use_requires_learned_adjudication_on_this_base():
    """AT15(2): structural use of a fact requires a named rule and authority.

    The competent current owner is structural admission (I04). Without a named
    rule and matching authority it cannot return ADMITTED, which is exactly the
    LEARNED_OR_ADJUDICATED_REQUIRED case.
    """
    from rawlsing_next.pre553_structural_admission import (
        evaluate_structural_empirical_admission,
    )
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state="SUPPORTED", tag="c1-03a-admission")
    rule, registry, admitted_snapshot, _parity = environment(admission_state="ALLOW")
    authority_ref = admitted_snapshot.authority_ref

    denied = evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=authority_ref,
        rule=None,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
    )
    assert denied.decision_state != "ADMITTED", denied.reason_code

    # A competent direct route exists for the same fact without any admission rule.
    direct = _envelope(
        classify_empirical_fact_state(fact.typed_state),
        route=ROUTE_DIRECT_EMPIRICAL,
        producer_state=fact.typed_state,
        reason="direct empirical use needs no learned rule",
        fixture_refs=(fact.ref,),
    )
    assert direct.route_class == ROUTE_DIRECT_EMPIRICAL
    # ...while the structural use of the same fact is legitimately gated.
    assert_route_not_laundered(
        route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
        required_route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
        producer_state=fact.typed_state,
        reason="structural mediation input requires a named admission rule",
    )


def test_at15_failed_learned_claim_cannot_be_route_laundered_as_direct():
    """AT15 hostile: a failed learned/adjudicated claim cannot be relabelled DIRECT."""
    from rawlsing_next.pre553_structural_admission import (
        evaluate_structural_empirical_admission,
    )
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state="UNRESOLVED", tag="c1-03a-launder")
    rule, registry, admitted_snapshot, _parity = environment(admission_state="ALLOW")
    authority_ref = admitted_snapshot.authority_ref

    # The claim genuinely fails: an unresolved fact cannot be admitted.
    failed = evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=authority_ref,
        rule=rule,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
    )
    assert failed.decision_state != "ADMITTED", f"the learned claim must not succeed here: {failed.reason_code}"

    # Relabelling it as a direct empirical route is rejected.
    with pytest.raises(RouteLegitimacyError) as excinfo:
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            required_route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
            producer_state=fact.typed_state,
            reason="learned claim relabelled direct to reach the consumer",
        )
    assert "ROUTE_LAUNDERING_REJECTED" in str(excinfo.value)


def test_at15_denying_authority_cannot_be_relabelled_direct():
    """AT15 hostile: a denied admission authority cannot be relabelled direct."""
    from rawlsing_next.pre553_structural_admission import (
        evaluate_structural_empirical_admission,
    )
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state="SUPPORTED", tag="c1-03a-deny-launder")
    rule, registry, denied_snapshot, _parity = environment(admission_state="DENY")
    authority_ref = denied_snapshot.authority_ref
    denied = evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=authority_ref,
        rule=rule,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
    )
    assert denied.decision_state != "ADMITTED", denied.reason_code

    with pytest.raises(RouteLegitimacyError):
        assert_route_not_laundered(
            route_class=ROUTE_DIRECT_EMPIRICAL,
            required_route_class=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
            producer_state=fact.typed_state,
            reason="denied authority relabelled direct",
        )


def test_at15_route_label_alone_creates_no_authority():
    """AT15: the route label must not itself confer authority or support."""
    data = fx.observed_zero_fixture()
    fact = data["fact"]

    # Two envelopes differing only in route class are distinct identities, and
    # neither carries authority it did not receive from an owner.
    direct = _envelope(OBSERVED_ZERO, route=ROUTE_DIRECT_EMPIRICAL,
                       producer_state=fact.typed_state, reason="r",
                       fixture_refs=(fact.ref,))
    learned = _envelope(OBSERVED_ZERO, route=ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
                        producer_state=fact.typed_state, reason="r",
                        fixture_refs=(fact.ref,))
    assert direct.envelope_identity_hash != learned.envelope_identity_hash
    assert direct.authority_refs == () and learned.authority_refs == ()
    # Labelling a route never turns a negative state into a positive one.
    assert direct.retained_analytical_state == learned.retained_analytical_state == OBSERVED_ZERO
    assert direct.negative_claim_authorized is False


# ===========================================================================
# AT16 - final-consumer witness
# ===========================================================================


def test_at16_direct_empirical_positive_path_reaches_the_named_consumer():
    """AT16(1): real producer output -> composition -> actual consumer."""
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

    consumer_result = composed.consumer_result_or_null
    assert consumer_result is not None
    assert consumer_result.result_state == "EXACT_SUPPORTED"

    # The consumer really is the current public consumer, reached by the public
    # path, and its evidence came from the producer fact.
    evidence = composed.possibility_slice_evidence_or_null
    assert evidence is not None
    assert evidence.evidence_ref == consumer_result.exact_evidence_ref
    geometry_ref = evidence.geometry["source_fact_ref"]
    assert geometry_ref == composed.producer_fact_ref.as_dict()

    # A hand-built consumer call with a fabricated slice is NOT this witness: the
    # real path is required to produce the composed identity.
    handmade = evaluate_positioned_subject_possibility(
        query=consumer_query,
        rule=c1.make_model_rule(source["universe"].ref, "at16positive"),
        evidence=(evidence,),
    )
    assert handmade.result_hash == consumer_result.result_hash
    assert composed.composed_result_identity_hash not in (
        handmade.result_hash,
    ), "the composed identity is strictly more than a consumer primitive result"

    result = _envelope(
        OBSERVED_ZERO,
        producer_state=composed.analytical_state,
        reason="direct empirical positive reaches the named current consumer",
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
    # Every identity AT16 requires is recorded and bound.
    assert result.consumer_disposition.consumer_query_ref == consumer_query.ref
    assert result.consumer_disposition.consumer_result_state == "EXACT_SUPPORTED"
    assert result.consumer_disposition.evidence_ref == evidence.evidence_ref
    assert result.upstream_composed_result_hash == composed.composed_result_identity_hash
    assert composed.producer_fact_ref in result.producer_refs


def test_at16_negative_path_preserves_non_invocation_explicitly():
    """AT16(2): a negative path records consumer behavior or explicit non-invocation."""
    data = fx.valid_empty_fixture()
    retained = classify_empirical_fact_state(data["producer_state"])
    result = _envelope(retained, producer_state=data["producer_state"],
                       reason=data["reason"], fixture_refs=(data["fact"].ref,))
    assert result.retained_analytical_state == VALID_EMPTY
    assert result.consumer_disposition.disposition == (
        CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE
    )
    assert result.consumer_disposition.consumer_result_state is None
    assert "VALID_EMPTY" in result.consumer_disposition.non_invocation_reason
    # The non-invocation is part of the envelope identity, so it cannot be dropped.
    other = _envelope(VALID_EMPTY, producer_state="VALID_EMPTY",
                      reason="different reason", fixture_refs=(data["fact"].ref,))
    assert other.envelope_identity_hash != result.envelope_identity_hash


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
    for fixture, retained in (
        (fx.unresolved_fixture, UNKNOWN_UNRESOLVED),
        (fx.noncomparable_fixture, NONCOMPARABLE),
        (fx.integrity_failure_fixture, INTEGRITY_FAILURE),
    ):
        data = fixture()
        result = _envelope(
            retained,
            producer_state=data["producer_state"],
            reason=data["reason"],
            fixture_refs=(data.get("fact").ref if "fact" in data else data["corrupted_object_ref"],),
        )
        assert result.retained_analytical_state == retained
        assert not result.consumer_disposition.consumer_invoked
        assert result.consumer_disposition.consumer_result_state is None
        assert result.negative_claim_authorized is False
