"""C1-03A (AT14-AT16) source-free fixtures driven through competent current owners.

Every fixture here executes a real public owner. No state label is manufactured:

* observed zero / valid-empty / zero-support / unresolved / noncomparable come
  from ``pre553_empirical_query.execute_empirical_query`` and its I03 evaluator;
* integrity failure comes from the empirical owner refusing a tampered identity;
* unvisited coverage comes from
  ``pre553_discovery_adaptive.execute_adaptive_exploration`` with its real
  budget-truncation machinery;
* structural-admission route legitimacy comes from
  ``pre553_structural_admission.evaluate_structural_empirical_admission``.

Reused owner-native fixture builders only; no parallel empirical substrate.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Any

from rawlsing_next.pre553_analytical_state_and_route import (
    BLOCKED_REQUIRED_AUTHORITY,
    CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE,
    INTEGRITY_FAILURE,
    NONCOMPARABLE,
    OBSERVED_ZERO,
    ROUTE_DIRECT_EMPIRICAL,
    ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED,
    UNDERPOWERED,
    UNKNOWN_UNRESOLVED,
    UNVISITED,
    VALID_EMPTY,
    ConsumerDisposition,
    ProducerStateEvidence,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash

OWNER_EMPIRICAL = "rawlsing_next.pre553_empirical_query.execute_empirical_query"
OWNER_ADAPTIVE = "rawlsing_next.pre553_discovery_adaptive.execute_adaptive_exploration"
OWNER_DISCOVERY_EXACT = "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery"
OWNER_STRUCTURAL_ADMISSION = (
    "rawlsing_next.pre553_structural_admission.evaluate_structural_empirical_admission"
)
OWNER_CONSUMER = (
    "rawlsing_next.source_backed_positioned_subject_possibility."
    "evaluate_positioned_subject_possibility"
)


def _ref(kind: str, namespace: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "namespace": namespace})
    return ExactRef(kind, f"urn:test:c1-03a:{namespace}:sha256:{digest}", digest)


# ---------------------------------------------------------------------------
# AT14 state fixtures -- each returns (owner_state, fact, reason)
# ---------------------------------------------------------------------------


def observed_zero_fixture():
    """Positive denominator, zero numerator in a specific cell."""
    from rawlsing_next.tests.pre553_query_frontier_fixtures import (
        observed_zero_zero_support_fixture,
    )

    supported, _empty = observed_zero_zero_support_fixture()
    rows = {
        row["cell"]: row for row in supported.target_topology["complete_cell_semantic_projection"]
    }
    zero_cells = [
        cell for cell, row in rows.items()
        if row["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    ]
    assert zero_cells, "fixture must contain a supported observed-zero cell"
    return {
        "owner": OWNER_EMPIRICAL,
        "fact": supported,
        "producer_state": supported.typed_state,
        "observed_zero_cells": tuple(zero_cells),
        "raw_denominator_support": supported.raw_denominator_support,
        "reason": "positive denominator with an exact zero numerator cell",
    }


def zero_support_fixture():
    """Nonempty risk set, zero condition-selected denominator."""
    from rawlsing_next.tests.pre553_query_frontier_fixtures import (
        observed_zero_zero_support_fixture,
    )

    _supported, zero_support = observed_zero_zero_support_fixture()
    return {
        "owner": OWNER_EMPIRICAL,
        "fact": zero_support,
        "producer_state": zero_support.typed_state,
        "raw_denominator_support": zero_support.raw_denominator_support,
        "reason": "exact risk set is nonempty but the condition selects zero members",
    }


def valid_empty_fixture():
    """Query-declared exact target domain is empty."""
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _build_source,
        _query,
        _query_authority,
        _run,
    )
    from rawlsing_next.tests.c1_at08_at13_fixture import with_target_domains

    source = _build_source("c1-03a-valid-empty", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qauth = _query_authority("c1-03a-valid-empty")
    predicate = _branch_predicate(source, qauth, tag="c1-03a-valid-empty-branch")
    query = with_target_domains(
        _query(source, qauth, predicate, ("Y",), tag="c1-03a-valid-empty-query"),
        [[]],
    )
    fact = _run(source, qauth, predicate, query).facts[0]
    assert fact.typed_state == "VALID_EMPTY", fact.typed_state
    return {
        "owner": OWNER_EMPIRICAL,
        "fact": fact,
        "producer_state": fact.typed_state,
        "raw_denominator_support": fact.raw_denominator_support,
        "reason": "query-declared exact target domain is empty",
    }


def underpowered_fixture():
    """Exact discovery classifies a too-small branch as underpowered."""
    from rawlsing_next.tests.test_pre553_discovery_exact import (
        _atom,
        _d_auth,
        _discovery_authority,
        _execute,
        _grammar,
        _qt,
        _query,
        _query_authority,
        _registry,
        _rule,
    )
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _build_source,
        _branch_predicate,
        _coordinate_leaf,
        _predicate,
    )

    rows = (
        [{"id": f"A{i}", "responses": {"Y": 1}, "coords": {"G": "A"}} for i in range(6)]
        + [{"id": f"B{i}", "responses": {"Y": 0}, "coords": {"G": "B"}} for i in range(2)]
    )
    source = _build_source("c1-03a-underpowered", rows)
    qauth = _query_authority("c1-03a-underpowered")
    dauth = _d_auth("c1-03a-underpowered-discovery")

    all_p = _branch_predicate(source, qauth, tag="c1-03a-underpowered-all")
    b_atom = _predicate(source, qauth, _coordinate_leaf(source, "G", "B"), tag="c1-03a-underpowered-b")
    yq = _query(source, qauth, all_p, ("Y",), tag="c1-03a-underpowered-y")
    grammar = _grammar(
        operation="I03-OP-c1-03a-underpowered-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("B", b_atom, "COORDINATE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "underpowered", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
            atom_ids=("B",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="c1-03a-underpowered")
    # Raise the minimum raw denominator so the 2-member branch is underpowered.
    # DiscoveryAuthority is an immutable semantic object, so it is rebuilt with
    # the changed support rule rather than mutated.
    from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority

    authority = DiscoveryAuthority(
        typed_state=authority.typed_state,
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=authority.producer_replay_locator_or_reference_root,
        **{**dict(authority.semantic_fields), "support_rules": {"minimum_raw_denominator": 5}},
    )
    registry = _registry(source, qauth, dauth)
    result = _execute(
        source, qauth, dauth, grammar, (all_p, b_atom), (yq,), authority=authority,
    )
    receipt = result.receipts[0]
    return {
        "owner": OWNER_DISCOVERY_EXACT,
        "authority": authority,
        "registry": registry,
        "discovery": result,
        "receipt": receipt,
        "producer_state": receipt.typed_state,
        "coverage_state": receipt.coverage_state,
        "minimum_raw_denominator": 5,
        "reason": "supported branch below the exact minimum raw denominator",
    }


def unresolved_fixture():
    """Positive denominator but the target configuration is unresolved."""
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _build_source,
        _predicate,
        _query,
        _query_authority,
        _response_leaf,
        _run,
    )

    # A respondent with no event for the target question leaves the target
    # unresolved for one denominator member.
    source = _build_source("c1-03a-unresolved", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Z": 1}, "routing": {"Y": "NOT_ASKED"}},
    ])
    qauth = _query_authority("c1-03a-unresolved")
    predicate = _branch_predicate(source, qauth, tag="c1-03a-unresolved-branch")
    query = _query(source, qauth, predicate, ("Y",), tag="c1-03a-unresolved-query")
    fact = _run(source, qauth, predicate, query).facts[0]
    return {
        "owner": OWNER_EMPIRICAL,
        "fact": fact,
        "producer_state": fact.typed_state,
        "raw_denominator_support": fact.raw_denominator_support,
        "reason": "positive denominator with an unresolved target configuration member",
    }


def noncomparable_fixture():
    """Multi-universe composition without authority stays NONCOMPARABLE."""
    from rawlsing_next.tests.pre553_query_frontier_fixtures import (
        multi_universe_noncomparable_fixture as _nc,
    )

    fact = _nc()
    return {
        "owner": OWNER_EMPIRICAL,
        "fact": fact,
        "producer_state": fact.typed_state,
        "raw_denominator_support": fact.raw_denominator_support,
        "reason": "multi-universe structural composition lacks pooling authority",
    }


def blocked_required_authority_fixture():
    """Exact discovery blocked because a required authority is absent."""
    from rawlsing_next.tests.test_pre553_discovery_exact import (
        _atom,
        _branch_predicate,
        _d_auth,
        _discovery_authority,
        _grammar,
        _qt,
        _query,
        _query_authority,
        _registry,
        _rule,
    )
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _build_source,
        _predicate,
        _response_leaf,
    )

    source = _build_source("c1-03a-blocked", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "Y": 0}},
        {"id": "R3", "responses": {"X": 0, "Y": 1}},
    ])
    qauth = _query_authority("c1-03a-blocked")
    dauth = _d_auth("c1-03a-blocked-discovery")
    all_p = _branch_predicate(source, qauth, tag="c1-03a-blocked-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-03a-blocked-x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="c1-03a-blocked-y")
    grammar = _grammar(
        operation="I03-OP-c1-03a-blocked-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "blocked", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="c1-03a-blocked")
    # Deny the required discovery operation at the authority layer. The owner
    # refuses to execute when its governing operation is not named by a positive
    # authority snapshot; nothing here is simulated.
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot

    denied_snapshot = AuthoritySnapshot(
        typed_state="DENY",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=dauth.producer_replay_locator_or_reference_root,
        authority_id=dauth.authority_id,
        authority_version=dauth.authority_version,
        authority_content_hash=dauth.authority_content_hash,
        authority_kind=dauth.authority_kind,
        decision_state="DENY",
        governed_operations=(),
        governed_object_families=dauth.governed_object_families,
        scope_envelope=dict(dauth.scope_envelope),
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=dauth.interpretation_semantics_fingerprint,
        replay_protocol_ref=dauth.replay_protocol_ref,
    )
    blocked_registry = AuthorityRegistry((*source["authorities"], qauth, denied_snapshot))
    return {
        "owner": OWNER_DISCOVERY_EXACT,
        "authority": authority,
        "registry": blocked_registry,
        "denied_snapshot": denied_snapshot,
        "discovery_authority": authority,
        "query_authority": qauth,
        "source": source,
        "predicates": (all_p, x1),
        "queries": (yq,),
        "producer_state": BLOCKED_REQUIRED_AUTHORITY,
        "reason": "required discovery operation authority denies use",
    }


def integrity_failure_fixture():
    """The empirical object owner refuses a tampered body with a stale sealed identity.

    This is the owner-native INTEGRITY_FAILURE path: a reconstructed
    RespondentEvent whose body changed while retaining the original
    object_id/content_hash is rejected by the canonical constructor before it can
    enter ordinary execution. Nothing is fabricated here; the refusal is the
    owner's own.
    """
    from rawlsing_next.pre553_c11_integrity import RespondentIdentity, RespondentEvent
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    source = _build_source("c1-03a-integrity", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    release = source["repo"].resolve_release_exact(source["release_ref"])
    event = next(
        record for record in release.public_objects if isinstance(record, RespondentEvent)
    )

    # Governed identity plus the tampered body that keeps its sealed identity. The
    # fixture supplies only the repository, the declared release ref and the exact
    # RespondentEvent ref; the capture wrapper resolves the object from that release
    # and invokes the real canonical owner itself. The refusal is NOT captured here.
    corrupted_fields = dict(event.as_dict()["semantic_fields"])
    corrupted_fields["raw_response_value"] = "CHANGED"

    return {
        # The competent owner truthfully named: this state does NOT occur on
        # execute_empirical_query. It occurs on the canonical RespondentEvent
        # construction/integrity path.
        "owner": (
            "rawlsing_next.pre553_empirical_objects.RespondentEvent "
            "(canonical integrity construction)"
        ),
        "repository": source["repo"],
        "release_ref": source["release_ref"],
        "respondent_event_ref": event.ref,
        "original_object": event,
        "object_class": RespondentEvent,
        "object_family": event.FAMILY,
        "tampered_semantic_fields": corrupted_fields,
        "producer_state": INTEGRITY_FAILURE,
        "corrupted_object_ref": event.ref,
        "reason": "tampered object body retained a stale sealed identity; owner refused",
    }


def unvisited_adaptive_fixture():
    """Real adaptive budget truncation leaves explicit unvisited territory."""
    from rawlsing_next.pre553_discovery_adaptive import execute_adaptive_exploration
    from rawlsing_next.tests.test_pre553_discovery_adaptive import (
        _authority,
        _no_proposal_evaluator,
        _unit,
        _ref,
    )

    authority, registry, root_rule, _child = _authority("c1-03a-unvisited")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "c1-03a-unvisited")
    roots = (
        _unit("c1-03a-unvisited-a", determinant, root_rule, rank=30),
        _unit("c1-03a-unvisited-b", determinant, root_rule, rank=20),
        _unit("c1-03a-unvisited-c", determinant, root_rule, rank=10),
    )
    result = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=1,
    )
    assert result.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert result.unvisited_unit_refs
    assert result.global_negative_claim is False
    return {
        "owner": OWNER_ADAPTIVE,
        "authority": authority,
        "registry": registry,
        "determinant_state_ref": determinant,
        "roots": roots,
        "adaptive_result": result,
        "producer_state": result.completeness_state,
        "coverage_state": result.completeness_state,
        "visited_refs": result.visited_unit_refs,
        "unvisited_refs": result.unvisited_unit_refs,
        "global_negative_claim": result.global_negative_claim,
        "semantic_truth_effect": result.semantic_truth_effect,
        "reason": "adaptive budget exhausted with explicit unvisited territory",
    }


# ---------------------------------------------------------------------------
# AT14 -> consumer disposition mapping
# ---------------------------------------------------------------------------


def consumer_disposition_for(retained_state: str, *, invoked=None) -> ConsumerDisposition:
    """Decide, from the retained state alone, whether the consumer may be called.

    A bare envelope never claims a consumer invocation: doing so would require
    real consumer output, which only the AT16 final-consumer courts actually
    obtain. Callers that really invoked the consumer pass ``invoked``.

    For OBSERVED_ZERO the consumer *may* lawfully be invoked, because the owning
    fact is SUPPORTED and the zero rides inside the evidence geometry. That is
    recorded as the reason rather than asserted as an invocation.
    """
    if invoked is not None:
        return invoked
    if retained_state == OBSERVED_ZERO:
        return ConsumerDisposition(
            disposition=CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE,
            consumer_query_ref=None,
            consumer_rule_hash=None,
            consumer_result_state=None,
            consumer_result_hash=None,
            evidence_ref=None,
            non_invocation_reason=(
                "retained state OBSERVED_ZERO_IN_SUPPORTED_RISK_SET is lawfully "
                "consumer-invocable because the owning fact is SUPPORTED with an "
                "observed-zero cell; no consumer invocation was supplied to this envelope"
            ),
        )
    return ConsumerDisposition(
        disposition=CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE,
        consumer_query_ref=None,
        consumer_rule_hash=None,
        consumer_result_state=None,
        consumer_result_hash=None,
        evidence_ref=None,
        non_invocation_reason=(
            f"retained state {retained_state} has no lawful final-consumer projection; "
            "invocation would fabricate SUPPORTED/VALID_EMPTY/UNKNOWN semantics"
        ),
    )


def producer_evidence_for(
    *, owner: str, producer_state: str, retained_state: str, reason: str,
    producer_ref: ExactRef, supporting_refs=(), coverage_state: str = "NOT_APPLICABLE",
) -> ProducerStateEvidence:
    """Deprecated caller-label path, retained only to prove it is now refused.

    ``ProducerStateEvidence`` may no longer be built from a caller-supplied
    retained-state label. This helper therefore always raises, and the courts use
    the owner-derived projection factories instead.
    """
    from rawlsing_next.pre553_analytical_state_and_route import OwnerProjectionError

    raise OwnerProjectionError(
        "producer_evidence_for() may no longer mint analytical state from a caller "
        "label; use OwnerStateProjection.from_empirical_fact / "
        ".from_discovery_receipt / .from_adaptive_result / .from_owner_refusal"
    )


# ---------------------------------------------------------------------------
# Owner-derived projections (C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001)
# ---------------------------------------------------------------------------


def project_empirical(fixture_name: str, *, reason: str = ""):
    """Derive an OwnerStateProjection from a real empirical-owner fixture."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    data = globals()[fixture_name]()
    return OwnerStateProjection.from_empirical_fact(data["fact"], reason=reason), data


def project_receipt(fixture_name: str, *, reason: str = ""):
    """Derive an OwnerStateProjection from a real exact-discovery receipt."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    data = globals()[fixture_name]()
    return OwnerStateProjection.from_discovery_receipt(data["receipt"], reason=reason), data


def project_adaptive(fixture_name: str = "unvisited_adaptive_fixture", *, reason: str = ""):
    """Derive an OwnerStateProjection from a real adaptive-owner result.

    The projection now carries the owner's own visited/unvisited/determinant refs
    itself, so no reconstruction or ``supporting_refs`` substitution happens here.
    """
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    data = globals()[fixture_name]()
    projection = OwnerStateProjection.from_adaptive_result(data["adaptive_result"], reason=reason)
    return projection, data


def capture_integrity_refusal(fixture_name: str):
    """Capture a genuine empirical integrity refusal by invoking the real owner.

    The C1-03A capture wrapper performs the owner execution itself and derives the
    refused ref and supporting refs from the genuine owner object. No exception is
    handed to the projection layer.
    """
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_empirical_integrity_refusal,
    )

    data = globals()[fixture_name]()
    return capture_empirical_integrity_refusal(
        repository=data["repository"],
        release_ref=data["release_ref"],
        respondent_event_ref=data["respondent_event_ref"],
        tampered_semantic_fields=data["tampered_semantic_fields"],
    ), data


def capture_blocked_authority_refusal(fixture_name: str):
    """Capture a genuine required-authority refusal by invoking the real owner."""
    from rawlsing_next.pre553_analytical_state_and_route import (
        capture_required_authority_refusal,
    )

    data = globals()[fixture_name]()
    return capture_required_authority_refusal(
        repository=data["source"]["repo"],
        discovery_authority=data["authority"],
        authority_registry=data["registry"],
        release_refs=(data["source"]["release_ref"],),
        predicate_catalog=data["predicates"],
        query_template_catalog=data["queries"],
    ), data


def project_empirical_integrity_refusal(fixture_name: str):
    """Derive INTEGRITY_FAILURE from a witnessed real owner refusal."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    witness, data = capture_integrity_refusal(fixture_name)
    return OwnerStateProjection.from_empirical_integrity_refusal(witness=witness), data


def project_blocked_authority_refusal(fixture_name: str):
    """Derive BLOCKED_REQUIRED_AUTHORITY from a witnessed real owner refusal."""
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    witness, data = capture_blocked_authority_refusal(fixture_name)
    return OwnerStateProjection.from_blocked_authority_refusal(witness=witness), data


def structural_admission_evaluation(*, admission_state="ALLOW", fact_state="SUPPORTED", tag="c1-03a-admission"):
    """Run the real current structural-admission owner once."""
    from rawlsing_next.pre553_structural_admission import evaluate_structural_empirical_admission
    from rawlsing_next.tests.test_pre553_structural_admission import (
        environment,
        query_fact,
        request,
    )

    query, fact = query_fact(state=fact_state, tag=tag)
    rule, registry, snapshot, _parity = environment(admission_state=admission_state)
    evaluation = evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=snapshot.authority_ref,
        rule=rule,
        request=request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
    )
    return evaluation


def recursive_handoff_custody(handoff):
    """Derive RecursiveCoverageCustody from a real RecursiveBranchHandoff.

    There is no ``completeness_state`` parameter: the handoff does not own a
    completeness grade, so no caller may assert one.

    There is also no ``supporting`` parameter. The custody admits no
    caller-supplied supporting evidence, because the exact handoff ref, the exact
    evaluated frontier and the handoff's own retained scope identity are already
    owner-derived.
    """
    from rawlsing_next.pre553_analytical_state_and_route import RecursiveCoverageCustody

    return RecursiveCoverageCustody.from_handoff(handoff)


def project_recursive_handoff(handoff):
    """Derive a positive handoff projection through the typed factory.

    Positive handoff state is never built by direct ``OwnerStateProjection(...)``
    construction; it always goes through ``from_recursive_handoff`` with
    owner-derived custody.
    """
    from rawlsing_next.pre553_analytical_state_and_route import OwnerStateProjection

    custody = recursive_handoff_custody(handoff)
    return OwnerStateProjection.from_recursive_handoff(handoff, custody), custody


__all__ = [
    "OWNER_EMPIRICAL",
    "OWNER_ADAPTIVE",
    "OWNER_DISCOVERY_EXACT",
    "OWNER_STRUCTURAL_ADMISSION",
    "OWNER_CONSUMER",
    "observed_zero_fixture",
    "zero_support_fixture",
    "valid_empty_fixture",
    "underpowered_fixture",
    "unresolved_fixture",
    "noncomparable_fixture",
    "blocked_required_authority_fixture",
    "integrity_failure_fixture",
    "unvisited_adaptive_fixture",
    "consumer_disposition_for",
    "producer_evidence_for",
    "project_empirical",
    "project_receipt",
    "project_adaptive",
    "capture_integrity_refusal",
    "capture_blocked_authority_refusal",
    "project_empirical_integrity_refusal",
    "project_blocked_authority_refusal",
    "structural_admission_evaluation",
    "recursive_handoff_custody",
    "project_recursive_handoff",
]
