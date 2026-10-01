"""C1-03A bounded analytical state-conservation and route-legitimacy owner.

AT14 + AT15 + AT16.

This module does NOT invent semantic states. It is a routing and custody
envelope over the states that competent current owners already produce:

* direct empirical fact states come from
  ``rawlsing_next.pre553_empirical_query.execute_empirical_query``
  (owner vocabulary in ``_pre553_query_eval``);
* exact discovery states come from
  ``rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery``;
* adaptive coverage states, including ``EXPLICIT_UNKNOWN_UNVISITED`` and the
  nonexhaustive completeness vocabulary, come from
  ``rawlsing_next.pre553_discovery_adaptive.execute_adaptive_exploration``;
* structural admission decisions come from
  ``rawlsing_next.pre553_structural_admission.evaluate_structural_empirical_admission``.

Every retained state here is a *projection* of a producer-native state, bound to
the exact producer refs that produced it. The module never collapses the negative
estate: each mandatory state keeps its own retained identity, reason and coverage
state, and where the final consumer cannot losslessly represent a state the
consumer is explicitly NOT invoked and the reason is recorded.

Authority ceiling: this module is analytical/custodial. It creates no survey,
semantic, comparability, model or pooling authority, and it cannot promote a
non-positive producer result to a positive one.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    exact_ref,
    semantic_hash,
)

C1_03A_ENVELOPE_CONTRACT = "PRE553_C1_03A_ANALYTICAL_STATE_AND_ROUTE@1.0.0"

# --------------------------------------------------------------------------
# Mandatory AT14 negative-state estate.
#
# These are the *retained* names the envelope guarantees to keep distinct.
# Each is populated only from a producer-native state; none is synthesized.
# --------------------------------------------------------------------------
OBSERVED_ZERO = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
VALID_EMPTY = "VALID_EMPTY"
UNDERPOWERED = "UNDERPOWERED"
UNKNOWN_UNRESOLVED = "UNKNOWN_OR_UNRESOLVED"
UNVISITED = "UNVISITED"
NONCOMPARABLE = "NONCOMPARABLE"
BLOCKED_REQUIRED_AUTHORITY = "BLOCKED_REQUIRED_AUTHORITY"
INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
SUPPORTED = "SUPPORTED"

MANDATORY_AT14_STATES = frozenset({
    OBSERVED_ZERO,
    VALID_EMPTY,
    UNDERPOWERED,
    UNKNOWN_UNRESOLVED,
    UNVISITED,
    NONCOMPARABLE,
    BLOCKED_REQUIRED_AUTHORITY,
    INTEGRITY_FAILURE,
})

# The positive baseline is retainable too, so a competent supported result can be
# carried through the same envelope. It is deliberately NOT part of the
# mandatory negative estate.
SUPPORTED_BASELINE = "SUPPORTED"
RETAINABLE_STATES = frozenset(MANDATORY_AT14_STATES | {SUPPORTED_BASELINE})

# Producer-native empirical fact states that must NOT be collapsed together.
# Mapping is explicit and total over the owner vocabulary we consume.
EMPIRICAL_FACT_STATE_TO_RETAINED: Mapping[str, str] = {
    "SUPPORTED": SUPPORTED,
    "OBSERVED_ZERO": OBSERVED_ZERO,
    "LOW_SUPPORT": UNDERPOWERED,
    "VALID_EMPTY": VALID_EMPTY,
    "ZERO_SUPPORT": UNDERPOWERED,
    "ZERO_OVERLAP": UNDERPOWERED,
    "UNRESOLVED": UNKNOWN_UNRESOLVED,
    "NONCOMPARABLE": NONCOMPARABLE,
    "NOT_APPLICABLE": NONCOMPARABLE,
    "UNAVAILABLE": BLOCKED_REQUIRED_AUTHORITY,
    "INTEGRITY_FAILURE": INTEGRITY_FAILURE,
    "UNCERTAINTY_UNQUANTIFIED": SUPPORTED,
}

# Exact-discovery receipt states, as produced by the current I05 owner.
DISCOVERY_RECEIPT_STATE_TO_RETAINED: Mapping[str, str] = {
    "DISCOVERED_RESULT_SUPPORTED": SUPPORTED,
    "INSUFFICIENT_SUPPORT": UNDERPOWERED,
    "VALID_EMPTY": VALID_EMPTY,
    "NONCOMPARABLE": NONCOMPARABLE,
    "UNRESOLVED": UNKNOWN_UNRESOLVED,
    "BLOCKED_REQUIRED_AUTHORITY": BLOCKED_REQUIRED_AUTHORITY,
    "INTEGRITY_FAILURE": INTEGRITY_FAILURE,
    "OBSERVED_ZERO": OBSERVED_ZERO,
}

# Coverage states the exact owner emits, mapped to the same retained estate so a
# coverage-state read can never disagree with a receipt-state read.
DISCOVERY_COVERAGE_STATE_TO_RETAINED: Mapping[str, str] = {
    "EVALUATED_UNDERPOWERED": UNDERPOWERED,
    "EVALUATED_VALID_EMPTY": VALID_EMPTY,
    "EVALUATED_UNRESOLVED": UNKNOWN_UNRESOLVED,
    "EVALUATED_NONCOMPARABLE": NONCOMPARABLE,
    "EVALUATED_BLOCKED_REQUIRED_AUTHORITY": BLOCKED_REQUIRED_AUTHORITY,
    "EVALUATED_INTEGRITY_FAILURE": INTEGRITY_FAILURE,
    "EVALUATED_OBSERVED_ZERO": OBSERVED_ZERO,
}

# Adaptive search completeness states. These are owner-native and carry their own
# coverage meaning; the envelope records them verbatim plus the unvisited refs.
ADAPTIVE_PARTIAL_STATES = frozenset({
    "PARTIAL_BUDGET_EXHAUSTED",
    "PARTIAL_INTERRUPTED",
    "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED",
})

# Route classification (AT15).
ROUTE_DIRECT_EMPIRICAL = "DIRECT_EMPIRICAL"
ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED = "LEARNED_OR_ADJUDICATED_REQUIRED"
ROUTE_CLASSES = frozenset({ROUTE_DIRECT_EMPIRICAL, ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED})

# Consumer disposition.
CONSUMER_INVOKED = "CONSUMER_INVOKED"
CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE = (
    "CONSUMER_NOT_INVOKED__STATE_NOT_LOSSLESSLY_REPRESENTABLE"
)


class C103AStateRouteError(Exception):
    """Raised on a malformed or self-inconsistent C1-03A envelope input."""


class RouteLegitimacyError(Exception):
    """Raised when a route label would be laundered over an unmet requirement."""


class OwnerProjectionError(C103AStateRouteError):
    """Raised when a retained state cannot be derived from an owner object."""


# Only the owner-projection factories below may mint analytical state. A caller
# supplied ``retained_state`` string can never establish one on its own.
_PROJECTION_TOKEN = object()

# Only the typed factories below may mint a projection, a route obligation, or a
# coverage custody record. The generic derive/derive_fn injection point is gone, so
# no external caller can supply arbitrary retained state or projection logic.
_TRUST_TOKEN = object()

OWNER_EMPIRICAL_PROJECTION_LABEL = (
    "rawlsing_next.pre553_empirical_query.execute_empirical_query"
)
OWNER_DISCOVERY_PROJECTION_LABEL = (
    "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery"
)
OWNER_ADAPTIVE_PROJECTION_LABEL = (
    "rawlsing_next.pre553_discovery_adaptive.execute_adaptive_exploration"
)
OWNER_ADMISSION_PROJECTION_LABEL = (
    "rawlsing_next.pre553_structural_admission.evaluate_structural_empirical_admission"
)
OWNER_RECURSIVE_HANDOFF_LABEL = (
    "rawlsing_next.pre553_recursive_handoff.execute_exact_bounded_discovery_with_handoffs"
)


def _exact_cell_projection(fact: Any) -> tuple[Mapping[str, Any], ...]:
    """Read the producer's own complete cell projection from an empirical fact.

    A SUPPORTED fact must carry its cell projection, otherwise an observed-zero
    cell could not be derived and a plain positive would be indistinguishable
    from an observed zero. Owner-native nonpositive failure states (NONCOMPARABLE,
    ZERO_SUPPORT, UNAVAILABLE, ...) legitimately carry no cell projection, and
    for those the fact state alone is decisive because no cell can be observed
    zero.
    """
    state = str(getattr(fact, "typed_state", "") or "")
    topology = getattr(fact, "target_topology", None)
    if not isinstance(topology, Mapping):
        if state and state != "SUPPORTED":
            return ()
        raise OwnerProjectionError("empirical fact carries no target_topology mapping")
    rows = topology.get("complete_cell_semantic_projection")
    if rows is None:
        if state and state != "SUPPORTED":
            return ()
        raise OwnerProjectionError(
            "SUPPORTED empirical fact carries no complete_cell_semantic_projection; "
            "an observed-zero cell could not be derived, so a plain positive would be "
            "indistinguishable from an observed zero"
        )
    return tuple(rows)



@dataclass(frozen=True)
class RouteObligation:
    """The route obligation derived from an exact current owner/use contract.

    The obligation is *derived* from a real owner-produced admission evaluation.
    A caller cannot weaken it by choosing a different label, and it cannot be
    forged at all: direct construction requires the module-private trust token,
    so only :meth:`from_structural_admission` -- which reads a real
    ``AdmissionEvaluation`` -- can produce a lawful one.
    """

    owner: str
    requested_use: str
    target_use: str
    decision_state: str
    reason_code: str
    required_route_class: str
    relation_ref: Mapping[str, Any]
    admission_receipt_ref: Mapping[str, Any]
    admission_authority_ref: Mapping[str, Any]
    admission_rule_ref: Mapping[str, Any]
    blocking_refs: tuple[ExactRef, ...]
    _TRUST_TOKEN: Any = None

    def __post_init__(self) -> None:
        if self._TRUST_TOKEN is not _TRUST_TOKEN:
            raise OwnerProjectionError(
                "RouteObligation may only be built by "
                "RouteObligation.from_structural_admission() from a real "
                "AdmissionEvaluation; a directly constructed obligation is not "
                "route legitimacy (C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001)"
            )
        if self.required_route_class not in ROUTE_CLASSES:
            raise C103AStateRouteError(
                f"required_route_class {self.required_route_class!r} is not a route class"
            )
        if not self.admission_receipt_ref.get("content_hash"):
            raise OwnerProjectionError("obligation does not bind an exact admission receipt")

    @classmethod
    def from_structural_admission(
        cls,
        evaluation: Any,
        *,
        requested_use: str,
        owner: str = OWNER_ADMISSION_PROJECTION_LABEL,
    ) -> "RouteObligation":
        """Derive the route obligation from one real AdmissionEvaluation."""
        decision = str(getattr(evaluation, "decision_state", ""))
        if not decision:
            raise OwnerProjectionError("admission evaluation carries no decision_state")
        receipt = getattr(evaluation, "receipt", None)
        if receipt is None:
            raise OwnerProjectionError("admission evaluation carries no receipt")
        receipt_ref = getattr(receipt, "ref", None)
        if not isinstance(receipt_ref, ExactRef):
            raise OwnerProjectionError("admission receipt carries no exact ref")
        semantic = getattr(receipt, "semantic_fields", None)
        if not isinstance(semantic, Mapping):
            raise OwnerProjectionError("admission receipt carries no semantic fields")
        target_use = str(semantic.get("target_use", "") or "")
        if not target_use:
            raise OwnerProjectionError("admission receipt does not bind a target use")
        blocking = tuple(
            exact_ref(value) for value in (getattr(evaluation, "blocking_refs", ()) or ())
        )
        payload = semantic.get("structural_interpretation_payload")
        rule_hash = ""
        if isinstance(payload, Mapping):
            rule_hash = str(payload.get("admission_rule_hash", "") or "")
        elif decision == "ADMITTED":
            # A positive admission must bind its exact rule identity. A negative
            # evaluation legitimately has no rule payload, because no rule passed.
            raise OwnerProjectionError(
                "ADMITTED receipt carries no structural_interpretation_payload; "
                "the admission rule identity cannot be bound"
            )
        if decision == "ADMITTED" and not rule_hash:
            raise OwnerProjectionError(
                "ADMITTED receipt does not bind an exact admission rule hash"
            )
        authority_ref = semantic.get("admission_authority_ref")
        if not isinstance(authority_ref, Mapping) or not authority_ref.get("authority_content_hash"):
            raise OwnerProjectionError(
                "admission receipt does not bind an exact admission authority"
            )
        fact_ref = semantic.get("empirical_fact_ref")
        if not isinstance(fact_ref, Mapping) or not fact_ref.get("content_hash"):
            raise OwnerProjectionError("admission receipt does not bind the exact empirical fact")
        # Derivation law: a structural-mediation use always routes through the
        # learned/adjudicated owner. Whether the claim succeeded only decides if
        # the envelope may proceed at all -- it never downgrades the route.
        required = ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            requested_use=requested_use,
            target_use=target_use,
            decision_state=decision,
            reason_code=str(getattr(evaluation, "reason_code", "") or ""),
            required_route_class=required,
            relation_ref=dict(fact_ref),
            admission_receipt_ref=receipt_ref.as_dict(),
            admission_authority_ref=dict(authority_ref),
            admission_rule_ref={"admission_rule_hash": rule_hash},
            blocking_refs=blocking,
        )

    @property
    def is_positive_admission(self) -> bool:
        return self.decision_state == "ADMITTED"

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "owner": self.owner,
            "requested_use": self.requested_use,
            "target_use": self.target_use,
            "decision_state": self.decision_state,
            "reason_code": self.reason_code,
            "required_route_class": self.required_route_class,
            "relation_ref": dict(self.relation_ref),
            "admission_receipt_ref": dict(self.admission_receipt_ref),
            "admission_authority_ref": dict(self.admission_authority_ref),
            "admission_rule_ref": dict(self.admission_rule_ref),
            "blocking_refs": [ref.as_dict() for ref in self.blocking_refs],
        }

    @property
    def obligation_hash(self) -> str:
        return semantic_hash(self.identity_material())


@dataclass(frozen=True)
class RecursiveCoverageCustody:
    """Binds a selected positive handoff to the coverage record it came from.

    A recursive handoff is a *positive selection*. Without retained custody of
    the exact discovery/adaptive coverage record it was selected from, the handoff
    is not a coverage statement.

    The custody is factory-only: direct construction requires the module-private
    trust token, and :meth:`from_handoff` reads ``handoff.evaluated_frontier_ref``
    itself. A caller can therefore neither forge the custody nor substitute a
    different coverage record.

    There is deliberately no ``completeness_state`` field. ``RecursiveBranchHandoff``
    does not own a completeness grade, so recording one here would let a caller
    assert a coverage completeness the owner never produced.
    """

    handoff_ref: ExactRef
    coverage_record_ref: ExactRef
    handoff_scope_identity: Mapping[str, Any]
    supporting_refs: tuple[ExactRef, ...] = ()
    _TRUST_TOKEN: Any = None

    def __post_init__(self) -> None:
        if self._TRUST_TOKEN is not _TRUST_TOKEN:
            raise OwnerProjectionError(
                "RecursiveCoverageCustody may only be built by "
                "RecursiveCoverageCustody.from_handoff() from a real "
                "RecursiveBranchHandoff; a directly constructed custody record is "
                "not coverage custody (C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001)"
            )
        if not isinstance(self.handoff_ref, ExactRef) or not isinstance(self.coverage_record_ref, ExactRef):
            raise OwnerProjectionError("custody refs must be exact refs")

    @classmethod
    def from_handoff(
        cls,
        handoff: Any,
        *,
        required_supporting_refs: Sequence[ExactRef] = (),
    ) -> "RecursiveCoverageCustody":
        """Derive custody from a real RecursiveBranchHandoff.

        ``completeness_state`` is intentionally not a parameter: the handoff does
        not own a completeness grade, so no caller may supply one.
        """
        from rawlsing_next.pre553_recursive_handoff import RecursiveBranchHandoff

        if type(handoff) is not RecursiveBranchHandoff:
            raise OwnerProjectionError(
                "coverage custody requires a real RecursiveBranchHandoff; got "
                f"{type(handoff).__name__}"
            )
        handoff_ref = getattr(handoff, "ref", None)
        if not isinstance(handoff_ref, ExactRef):
            raise OwnerProjectionError("handoff carries no exact ref")
        coverage_ref = getattr(handoff, "evaluated_frontier_ref", None)
        if not isinstance(coverage_ref, ExactRef):
            raise OwnerProjectionError(
                "handoff carries no exact evaluated_frontier_ref; a selected positive "
                "handoff cannot stand in for its coverage record"
            )
        scoped = getattr(handoff, "scope_context", None)
        scope_identity: dict[str, Any] = {}
        if isinstance(scoped, Mapping):
            scoped_frontier = scoped.get("evaluated_frontier_ref")
            if scoped_frontier is not None and exact_ref(scoped_frontier) != coverage_ref:
                raise OwnerProjectionError(
                    "handoff frontier ref disagrees with its own retained scope context"
                )
            # Bind the handoff's own internally retained scope/frontier identity so
            # custody cannot be separated from the scope it was selected under.
            scope_identity = {
                "candidate_universe_definition": _exact_identity(
                    getattr(handoff, "candidate_universe_definition", None), "candidate_universe_definition"
                ),
                "winning_predicate": _exact_identity(
                    getattr(handoff, "winning_predicate", None), "winning_predicate"
                ),
                "discovery_authority_ref": _exact_identity(
                    getattr(handoff, "discovery_authority_ref", None), "discovery_authority_ref"
                ),
                "branch_replay_binding": _exact_identity(
                    getattr(handoff, "branch_replay_binding", None), "branch_replay_binding"
                ),
            }
        supporting = []
        for value in required_supporting_refs:
            if not isinstance(value, ExactRef):
                raise OwnerProjectionError("supporting coverage refs must be exact refs")
            supporting.append(value)
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            handoff_ref=handoff_ref,
            coverage_record_ref=coverage_ref,
            handoff_scope_identity=scope_identity,
            supporting_refs=tuple(supporting),
        )

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "handoff_ref": self.handoff_ref.as_dict(),
            "coverage_record_ref": self.coverage_record_ref.as_dict(),
            "handoff_scope_identity": dict(self.handoff_scope_identity),
            "supporting_refs": [ref.as_dict() for ref in self.supporting_refs],
        }

    @property
    def custody_hash(self) -> str:
        return semantic_hash(self.identity_material())


def _exact_identity(value: Any, label: str) -> Mapping[str, Any]:
    """Reduce an owner identity to its exact deterministic content hash.

    These handoff fields are nested structures (a full candidate-universe
    definition, a branch replay binding), so there is no single ref to bind. A
    deterministic content hash over the owner-produced structure is the exact
    identity, and it is what the custody record carries.
    """
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, str) and value:
        return {"content_hash": value}
    inner = getattr(value, "ref", None)
    if isinstance(inner, ExactRef):
        # Owner's own identity-bearing object (e.g. DiscoveryBranchReplayBinding).
        return {"content_hash": str(inner.content_hash), "object_id": str(inner.object_id)}
    if value is None:
        raise OwnerProjectionError(f"handoff carries no {label} to bind")
    return {"content_hash": semantic_hash(value)}


@dataclass(frozen=True)
class OwnerStateProjection:
    """One competent owner's native state and its *derived* retained projection.

    This type is **factory-only and fail-closed**. Direct construction requires
    the module-private trust token, and the generic ``derive``/``derive_fn``
    injection point has been deleted outright, so no external caller can supply
    arbitrary retained state or arbitrary projection logic. Each factory below
    calls its own fixed classification function directly.

    The retained state is therefore always a function of a real owner object.
    """

    owner: str
    producer_state: str
    retained_state: str
    projection_law: str
    reason: str
    producer_ref: ExactRef
    supporting_refs: tuple[ExactRef, ...] = ()
    coverage_state: str = "NOT_APPLICABLE"
    unvisited_refs: tuple[ExactRef, ...] = ()
    visited_refs: tuple[ExactRef, ...] = ()
    _TRUST_TOKEN: Any = None

    def __post_init__(self) -> None:
        if self._TRUST_TOKEN is not _TRUST_TOKEN:
            raise OwnerProjectionError(
                "OwnerStateProjection may only be built by one of its typed owner "
                "factories (from_empirical_fact, from_discovery_receipt, "
                "from_adaptive_result, from_empirical_integrity_refusal, "
                "from_blocked_authority_refusal, from_recursive_handoff); a "
                "directly constructed projection is not owner-derived state "
                "(C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001)"
            )
        if self.retained_state not in RETAINABLE_STATES:
            raise C103AStateRouteError(
                f"retained_state {self.retained_state!r} is not a retainable analytical state"
            )

    @classmethod
    def from_empirical_fact(
        cls,
        fact: Any,
        *,
        owner: str = OWNER_EMPIRICAL_PROJECTION_LABEL,
        reason: str = "",
    ) -> "OwnerStateProjection":
        """Project a real empirical fact, reading its own cell projection."""
        state = str(getattr(fact, "typed_state", ""))
        if not state:
            raise OwnerProjectionError("empirical fact carries no typed_state")
        ref = getattr(fact, "ref", None)
        if not isinstance(ref, ExactRef):
            raise OwnerProjectionError("empirical fact carries no exact ref")
        cells = _exact_cell_projection(fact)
        try:
            retained = classify_empirical_cells(state, cells)
        except Exception as exc:  # noqa: BLE001 - a projection must fail closed
            raise OwnerProjectionError(
                "classify_empirical_cells could not project the owner fact for "
                f"{owner}: {exc}"
            ) from exc
        replay = getattr(fact, "replay_ref", None)
        supporting = ()
        if isinstance(replay, Mapping):
            supporting = (exact_ref(replay),)
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state=state,
            retained_state=retained,
            projection_law="classify_empirical_cells(fact.typed_state, complete_cell_semantic_projection)",
            reason=reason or "empirical fact state and exact cell projection",
            producer_ref=ref,
            supporting_refs=supporting,
        )

    @classmethod
    def from_discovery_receipt(
        cls,
        receipt: Any,
        *,
        owner: str = OWNER_DISCOVERY_PROJECTION_LABEL,
        reason: str = "",
    ) -> "OwnerStateProjection":
        """Project a real exact-discovery receipt, cross-checking its coverage."""
        state = str(getattr(receipt, "typed_state", ""))
        coverage = str(getattr(receipt, "coverage_state", "") or "NOT_APPLICABLE")
        ref = getattr(receipt, "ref", None)
        if not isinstance(ref, ExactRef):
            raise OwnerProjectionError("discovery receipt carries no exact ref")
        try:
            retained = classify_discovery_receipt_state(state, coverage or None)
        except Exception as exc:  # noqa: BLE001 - a projection must fail closed
            raise OwnerProjectionError(
                "classify_discovery_receipt_state could not project the owner receipt "
                f"for {owner}: {exc}"
            ) from exc
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state=state,
            retained_state=retained,
            projection_law="classify_discovery_receipt_state(typed_state, coverage_state)",
            reason=reason or "exact discovery receipt state with coverage cross-check",
            producer_ref=ref,
            coverage_state=coverage,
        )

    @classmethod
    def from_adaptive_result(
        cls,
        adaptive_result: Any,
        *,
        owner: str = OWNER_ADAPTIVE_PROJECTION_LABEL,
        reason: str = "",
        producer_ref: ExactRef | None = None,
    ) -> "OwnerStateProjection":
        """Project a real adaptive result, carrying its own unvisited territory.

        The projection carries the owner's own visited/unvisited/determinant refs.
        No caller can substitute them, and no separate reconstruction is needed.
        """
        completeness = str(getattr(adaptive_result, "completeness_state", ""))
        if not completeness:
            raise OwnerProjectionError("adaptive result carries no completeness_state")
        unvisited = tuple(getattr(adaptive_result, "unvisited_unit_refs", ()) or ())
        visited = tuple(getattr(adaptive_result, "visited_unit_refs", ()) or ())
        if not unvisited:
            raise OwnerProjectionError(
                "an adaptive projection requires the owner's own unvisited refs"
            )
        for group, label in ((unvisited, "unvisited"), (visited, "visited")):
            for item in group:
                if not isinstance(item, ExactRef):
                    raise OwnerProjectionError(f"adaptive {label} refs must be exact refs")
        if not isinstance(getattr(adaptive_result, "global_negative_claim", None), bool):
            raise OwnerProjectionError(
                "adaptive result does not carry the owner's global_negative_claim fact"
            )
        if adaptive_result.global_negative_claim:
            raise OwnerProjectionError(
                "adaptive result claims a global negative; refused by owner contract"
            )
        ref = producer_ref
        if ref is None:
            candidate = getattr(adaptive_result, "determinant_state_ref", None)
            ref = candidate if isinstance(candidate, ExactRef) else None
        if not isinstance(ref, ExactRef):
            raise OwnerProjectionError("adaptive result carries no exact determinant ref")
        checkpoint = getattr(adaptive_result, "checkpoint", None)
        checkpoint_ref = getattr(checkpoint, "ref", None)
        try:
            retained = classify_adaptive_coverage(completeness)
        except Exception as exc:  # noqa: BLE001 - a projection must fail closed
            raise OwnerProjectionError(
                f"classify_adaptive_coverage could not project the owner result for "
                f"{owner}: {exc}"
            ) from exc
        # supporting_refs = (checkpoint?, determinant, *visited)
        supporting: list[ExactRef] = []
        if isinstance(checkpoint_ref, ExactRef):
            supporting.append(checkpoint_ref)
        supporting.append(ref)
        supporting.extend(visited)
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state=completeness,
            retained_state=retained,
            projection_law="classify_adaptive_coverage(completeness_state) with owner unvisited refs",
            reason=reason or "adaptive nonexhaustive coverage with explicit unvisited territory",
            producer_ref=ref,
            supporting_refs=tuple(supporting),
            coverage_state=completeness,
            unvisited_refs=unvisited,
            visited_refs=visited,
        )

    @classmethod
    def from_recursive_handoff(
        cls,
        handoff: Any,
        custody: RecursiveCoverageCustody,
        *,
        owner: str = OWNER_RECURSIVE_HANDOFF_LABEL,
        reason: str = "",
    ) -> "OwnerStateProjection":
        """Project a selected positive recursive handoff.

        A handoff is a positive *selection*, so the derived retained state is
        SUPPORTED. That claim is only lawful when the handoff is real and the
        owner-derived custody is supplied for it, which is why custody is a
        required argument rather than an optional extra.
        """
        from rawlsing_next.pre553_recursive_handoff import RecursiveBranchHandoff

        if type(handoff) is not RecursiveBranchHandoff:
            raise OwnerProjectionError(
                "a recursive-handoff projection requires a real RecursiveBranchHandoff; "
                f"got {type(handoff).__name__}"
            )
        if type(custody) is not RecursiveCoverageCustody:
            raise OwnerProjectionError(
                "a positive recursive handoff requires owner-derived RecursiveCoverageCustody"
            )
        handoff_ref = getattr(handoff, "ref", None)
        if not isinstance(handoff_ref, ExactRef):
            raise OwnerProjectionError("handoff carries no exact ref")
        if custody.handoff_ref != handoff_ref:
            raise OwnerProjectionError(
                "coverage custody names a different handoff than the projection"
            )
        frontier = getattr(handoff, "evaluated_frontier_ref", None)
        if not isinstance(frontier, ExactRef) or frontier != custody.coverage_record_ref:
            raise OwnerProjectionError(
                "handoff frontier ref does not match the custody coverage record"
            )
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state="RECURSIVE_BRANCH_HANDOFF_SELECTED",
            retained_state=SUPPORTED,
            projection_law=(
                "a RecursiveBranchHandoff is a positive selection bound to its exact "
                "evaluated frontier; SUPPORTED with owner-derived coverage custody"
            ),
            reason=reason or "selected recursive branch handoff with exact coverage custody",
            producer_ref=handoff_ref,
            supporting_refs=(frontier,),
        )

    @classmethod
    def from_empirical_integrity_refusal(
        cls,
        *,
        exception: BaseException,
        reason: str,
        producer_ref: ExactRef,
        owner: str = OWNER_EMPIRICAL_PROJECTION_LABEL,
        supporting_refs: Sequence[ExactRef] = (),
    ) -> "OwnerStateProjection":
        """Project INTEGRITY_FAILURE from the exact empirical integrity refusal.

        Only the exact owner type is accepted. Note that
        ``Pre553AuthorityError`` *subclasses* ``Pre553IntegrityError``, so this
        check is exact-type identity rather than ``isinstance``: an isinstance
        check would silently collapse BLOCKED_REQUIRED_AUTHORITY into
        INTEGRITY_FAILURE.
        """
        from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError
        from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError

        if type(exception) is Pre553AuthorityError:
            raise OwnerProjectionError(
                "Pre553AuthorityError is a blocked-required-authority refusal, not an "
                "integrity refusal; use from_blocked_authority_refusal() so the two "
                "mandatory states stay distinct"
            )
        if type(exception) is not Pre553IntegrityError:
            raise OwnerProjectionError(
                "an integrity-refusal projection requires the exact empirical owner "
                f"refusal Pre553IntegrityError; got {type(exception).__name__}. "
                "Refusals are never classified by exception class-name substring"
            )
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state=f"OWNER_REFUSED:{type(exception).__name__}",
            retained_state=INTEGRITY_FAILURE,
            projection_law=(
                "exact empirical owner refusal Pre553IntegrityError -> INTEGRITY_FAILURE"
            ),
            reason=reason,
            producer_ref=producer_ref,
            supporting_refs=tuple(supporting_refs),
        )

    @classmethod
    def from_blocked_authority_refusal(
        cls,
        *,
        exception: BaseException,
        reason: str,
        producer_ref: ExactRef,
        owner: str = OWNER_DISCOVERY_PROJECTION_LABEL,
        supporting_refs: Sequence[ExactRef] = (),
    ) -> "OwnerStateProjection":
        """Project BLOCKED_REQUIRED_AUTHORITY from the exact authority refusal."""
        from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError

        if type(exception) is not Pre553AuthorityError:
            raise OwnerProjectionError(
                "a blocked-authority projection requires the exact current "
                f"authority/discovery refusal Pre553AuthorityError; got "
                f"{type(exception).__name__}. An arbitrary exception is never "
                "defaulted to a governed BLOCKED state"
            )
        return cls(
            _TRUST_TOKEN=_TRUST_TOKEN,
            owner=owner,
            producer_state=f"OWNER_REFUSED:{type(exception).__name__}",
            retained_state=BLOCKED_REQUIRED_AUTHORITY,
            projection_law=(
                "exact authority/discovery owner refusal Pre553AuthorityError -> "
                "BLOCKED_REQUIRED_AUTHORITY"
            ),
            reason=reason,
            producer_ref=producer_ref,
            supporting_refs=tuple(supporting_refs),
        )

    def as_evidence(self) -> "ProducerStateEvidence":
        return ProducerStateEvidence(
            _token=_PROJECTION_TOKEN,
            owner=self.owner,
            producer_state=self.producer_state,
            retained_state=self.retained_state,
            reason=self.reason,
            producer_ref=self.producer_ref,
            supporting_refs=self.supporting_refs,
            coverage_state=self.coverage_state,
            projection_law=self.projection_law,
        )


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise C103AStateRouteError(f"{label} must be a nonempty string")
    return value


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise C103AStateRouteError(f"{label} must be a mapping")
    return value


def _refs(values: Any, label: str) -> tuple[ExactRef, ...]:
    from rawlsing_next.pre553_analytical_composition import _exact, _refs as _c1_refs

    return _c1_refs(values, label)

@dataclass(frozen=True)
class ProducerStateEvidence:
    """One competent owner's native state and its owner-derived retained state.

    ``owner`` names the actual public owner that produced ``producer_state``.

    The retained state may only be minted by an :class:`OwnerStateProjection`
    factory that reads a real owner object. Direct construction requires the
    module-private projection token, so a caller-supplied label alone can never
    establish analytical state.
    """

    owner: str
    producer_state: str
    retained_state: str
    reason: str
    producer_ref: ExactRef
    supporting_refs: tuple[ExactRef, ...] = ()
    coverage_state: str = "NOT_APPLICABLE"
    projection_law: str = "OWNER_DERIVED"
    _token: Any = None

    def __post_init__(self) -> None:
        if self._token is not _PROJECTION_TOKEN:
            raise OwnerProjectionError(
                "ProducerStateEvidence may only be built by an OwnerStateProjection "
                "factory that derives the retained state from a real owner object; "
                "a caller-supplied retained-state label is not authority "
                "(C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001)"
            )
        _text(self.owner, "owner")
        _text(self.producer_state, "producer_state")
        _text(self.reason, "reason")
        _text(self.projection_law, "projection_law")
        if self.retained_state not in RETAINABLE_STATES:
            raise C103AStateRouteError(
                f"retained_state {self.retained_state!r} is not a retainable analytical state"
            )
        if not isinstance(self.producer_ref, ExactRef):
            raise C103AStateRouteError("producer_ref must be an exact ref")

    @staticmethod
    def from_projection(projection: OwnerStateProjection) -> "ProducerStateEvidence":
        return projection.as_evidence()


@dataclass(frozen=True)
class ConsumerDisposition:
    """Whether the final consumer was lawfully invoked, and why or why not."""

    disposition: str
    consumer_query_ref: ExactRef | None
    consumer_rule_hash: str | None
    consumer_result_state: str | None
    consumer_result_hash: str | None
    evidence_ref: ExactRef | None
    non_invocation_reason: str | None

    @property
    def consumer_invoked(self) -> bool:
        return self.disposition == CONSUMER_INVOKED


@dataclass(frozen=True)
class AnalyticalStateRouteResult:
    """Bounded envelope preserving the negative-state estate end to end."""

    contract: str
    route_class: str
    retained_analytical_state: str
    coverage_state: str
    reason: str
    producer_evidence: tuple[ProducerStateEvidence, ...]
    producer_refs: tuple[ExactRef, ...]
    coverage_record_ref: ExactRef | None
    unvisited_refs: tuple[ExactRef, ...]
    visited_refs: tuple[ExactRef, ...]
    consumer_disposition: ConsumerDisposition
    upstream_composed_result_hash: str | None
    authority_refs: tuple[AuthorityRef, ...] = ()
    negative_claim_authorized: bool = False
    route_obligation_hash: str | None = None
    coverage_custody_hash: str | None = None
    projection_laws: tuple[str, ...] = ()
    envelope_identity_hash: str = ""
    identity_material: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def identity_preimage(self) -> Mapping[str, Any]:
        return {
            "contract": self.contract,
            "route_class": self.route_class,
            "retained_analytical_state": self.retained_analytical_state,
            "coverage_state": self.coverage_state,
            "reason": self.reason,
            "producer_evidence": [
                {
                    "owner": item.owner,
                    "producer_state": item.producer_state,
                    "retained_state": item.retained_state,
                    "reason": item.reason,
                    "producer_ref": item.producer_ref.as_dict(),
                    "supporting_refs": [ref.as_dict() for ref in item.supporting_refs],
                    "coverage_state": item.coverage_state,
                }
                for item in self.producer_evidence
            ],
            "producer_refs": [ref.as_dict() for ref in self.producer_refs],
            "coverage_record_ref": (
                self.coverage_record_ref.as_dict() if self.coverage_record_ref else None
            ),
            "unvisited_refs": [ref.as_dict() for ref in self.unvisited_refs],
            "visited_refs": [ref.as_dict() for ref in self.visited_refs],
            "consumer_disposition": {
                "disposition": self.consumer_disposition.disposition,
                "consumer_query_ref": (
                    self.consumer_disposition.consumer_query_ref.as_dict()
                    if self.consumer_disposition.consumer_query_ref
                    else None
                ),
                "consumer_rule_hash": self.consumer_disposition.consumer_rule_hash,
                "consumer_result_state": self.consumer_disposition.consumer_result_state,
                "consumer_result_hash": self.consumer_disposition.consumer_result_hash,
                "evidence_ref": (
                    self.consumer_disposition.evidence_ref.as_dict()
                    if self.consumer_disposition.evidence_ref
                    else None
                ),
                "non_invocation_reason": self.consumer_disposition.non_invocation_reason,
            },
            "upstream_composed_result_hash": self.upstream_composed_result_hash,
            "authority_refs": [ref.as_dict() for ref in self.authority_refs],
            "negative_claim_authorized": self.negative_claim_authorized,
            "route_obligation_hash": self.route_obligation_hash,
            "coverage_custody_hash": self.coverage_custody_hash,
            "projection_laws": list(self.projection_laws),
        }

    @property
    def envelope_ref(self) -> ExactRef:
        return ExactRef(
            "PRE553_C1_03A_STATE_ROUTE_ENVELOPE@1",
            f"urn:rawlsing:pre553:c1-03a:state-route-envelope:sha256:{self.envelope_identity_hash}",
            self.envelope_identity_hash,
        )


def classify_empirical_fact_state(state: str) -> str:
    """Project one producer-native empirical fact state to its retained state."""
    _text(state, "empirical fact state")
    if state not in EMPIRICAL_FACT_STATE_TO_RETAINED:
        raise C103AStateRouteError(
            f"empirical fact state {state!r} has no declared retained AT14 projection; "
            "the negative estate must not be extended silently"
        )
    return EMPIRICAL_FACT_STATE_TO_RETAINED[state]


# The producer's own cell-state vocabulary. An observed zero is a CELL property,
# not a fact state: the owning fact stays SUPPORTED and the zero lives in the
# complete cell projection. Classifying it from the fact state alone would
# silently collapse observed zero into a plain positive.
EMPIRICAL_CELL_STATE_OBSERVED_ZERO = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
EMPIRICAL_CELL_STATE_ZERO_SUPPORT = "ZERO_SUPPORT"
EMPIRICAL_CELL_STATE_OBSERVED_POSITIVE = "OBSERVED_POSITIVE"


def classify_empirical_cells(
    fact_state: str,
    complete_cell_semantic_projection: Sequence[Mapping[str, Any]],
) -> str:
    """Project an exact producer cell projection to its retained analytical state.

    This is the only honest way to separate observed zero from plain support: the
    owner keeps the fact SUPPORTED and records the zero per cell. A positive
    denominator with any observed-zero cell is retained as OBSERVED_ZERO; a cell
    whose zero is unsupported (ZERO_SUPPORT) keeps the fact-level state instead,
    so observed zero can never be manufactured from a zero-support cell.
    """
    base = classify_empirical_fact_state(fact_state)
    projection = tuple(complete_cell_semantic_projection or ())
    if not projection:
        return base

    states = {row.get("cell_state") for row in projection}
    unknown = states - {
        EMPIRICAL_CELL_STATE_OBSERVED_ZERO,
        EMPIRICAL_CELL_STATE_ZERO_SUPPORT,
        EMPIRICAL_CELL_STATE_OBSERVED_POSITIVE,
    }
    if unknown:
        raise C103AStateRouteError(
            f"unknown producer cell states {sorted(str(u) for u in unknown)}; "
            "the retained estate must not be extended silently"
        )
    if EMPIRICAL_CELL_STATE_OBSERVED_ZERO in states:
        # An observed zero only exists inside positive denominator support.
        if base != SUPPORTED_BASELINE:
            raise C103AStateRouteError(
                f"observed-zero cell observed on a {fact_state!r} fact; "
                "observed zero requires positive supported denominator"
            )
        return OBSERVED_ZERO
    return base


def observed_zero_cells(
    complete_cell_semantic_projection: Sequence[Mapping[str, Any]],
) -> tuple[Any, ...]:
    """Return the exact producer cell keys retained as observed zero."""
    return tuple(
        row["cell"]
        for row in complete_cell_semantic_projection or ()
        if row.get("cell_state") == EMPIRICAL_CELL_STATE_OBSERVED_ZERO
    )


def classify_discovery_receipt_state(state: str, coverage_state: str | None = None) -> str:
    """Project one producer-native exact-discovery receipt state.

    The receipt state is authoritative. When the owner also supplies a coverage
    state, the two must agree on the retained estate; a disagreement is a defect
    in the caller's reading of the owner and fails closed rather than silently
    preferring one signal.
    """
    _text(state, "discovery receipt state")
    if state not in DISCOVERY_RECEIPT_STATE_TO_RETAINED:
        raise C103AStateRouteError(
            f"discovery receipt state {state!r} has no declared retained AT14 projection"
        )
    retained = DISCOVERY_RECEIPT_STATE_TO_RETAINED[state]
    if coverage_state is not None:
        _text(coverage_state, "discovery coverage state")
        if coverage_state in DISCOVERY_COVERAGE_STATE_TO_RETAINED:
            by_coverage = DISCOVERY_COVERAGE_STATE_TO_RETAINED[coverage_state]
            if by_coverage != retained:
                raise C103AStateRouteError(
                    f"receipt state {state!r} and coverage state {coverage_state!r} "
                    f"disagree on the retained estate ({retained} vs {by_coverage})"
                )
    return retained


def classify_adaptive_coverage(completeness_state: str) -> str:
    """Project an adaptive owner's nonexhaustive coverage into the retained estate.

    Any adaptive state that retains unvisited territory is retained as UNVISITED
    at the envelope level, while the owner-native completeness state is preserved
    verbatim in ``coverage_state`` so the distinction between budget exhaustion,
    interruption and exploratory exhaustion is never lost.
    """
    _text(completeness_state, "adaptive completeness state")
    if completeness_state not in ADAPTIVE_PARTIAL_STATES:
        raise C103AStateRouteError(
            f"adaptive completeness state {completeness_state!r} is not a declared "
            "partial/nonexhaustive adaptive state"
        )
    return UNVISITED


def require_route_class(route_class: str) -> str:
    _text(route_class, "route_class")
    if route_class not in ROUTE_CLASSES:
        raise C103AStateRouteError(
            f"route_class {route_class!r} is not one of {sorted(ROUTE_CLASSES)}"
        )
    return route_class


def assert_route_not_laundered(
    *,
    route_class: str,
    obligation: RouteObligation,
) -> None:
    """Fail closed if a claimed route contradicts the owner-derived obligation.

    The obligation is derived from a real current admission evaluation, so the
    caller cannot weaken it by choosing a different label. Relabelling the same
    underlying evidence as ``DIRECT_EMPIRICAL`` when the owner-derived
    obligation is learned/adjudicated is rejected.

    This replaces the previous signature that trusted a caller-supplied
    ``required_route_class`` (C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001).
    """
    if not isinstance(obligation, RouteObligation):
        raise RouteLegitimacyError(
            "route legitimacy requires an owner-derived RouteObligation, not a "
            "caller-supplied required_route_class"
        )
    require_route_class(route_class)
    if (
        obligation.required_route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
        and route_class == ROUTE_DIRECT_EMPIRICAL
    ):
        raise RouteLegitimacyError(
            "ROUTE_LAUNDERING_REJECTED: the owner-derived route obligation for "
            f"use={obligation.requested_use!r} decision={obligation.decision_state!r} "
            f"reason={obligation.reason_code!r} (receipt "
            f"{obligation.admission_receipt_ref.get('content_hash')}) is "
            f"{ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED} but was labelled "
            f"{ROUTE_DIRECT_EMPIRICAL}"
        )


def require_positive_route(obligation: RouteObligation) -> None:
    """Require the owner-derived route to actually be a positive ADMITTED route."""
    if not isinstance(obligation, RouteObligation):
        raise RouteLegitimacyError("positive route requires an owner-derived RouteObligation")
    if obligation.required_route_class != ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED:
        raise RouteLegitimacyError(
            f"positive route requires {ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED}, got "
            f"{obligation.required_route_class!r}"
        )
    if not obligation.is_positive_admission:
        raise RouteLegitimacyError(
            f"route may not proceed: owner decision is {obligation.decision_state!r} "
            f"({obligation.reason_code!r}) with blocking refs "
            f"{[ref.object_id for ref in obligation.blocking_refs]}"
        )


def build_state_route_result(
    *,
    route_class: str,
    producer_evidence: Sequence[ProducerStateEvidence],
    producer_refs: Sequence[ExactRef],
    consumer_disposition: ConsumerDisposition,
    reason: str,
    coverage_state: str = "NOT_APPLICABLE",
    coverage_record_ref: ExactRef | None = None,
    unvisited_refs: Sequence[ExactRef] = (),
    visited_refs: Sequence[ExactRef] = (),
    upstream_composed_result_hash: str | None = None,
    authority_refs: Sequence[AuthorityRef] = (),
    negative_claim_authorized: bool = False,
    route_obligation: RouteObligation | None = None,
    coverage_custody: RecursiveCoverageCustody | None = None,
) -> AnalyticalStateRouteResult:
    """Assemble the bounded envelope, enforcing the anti-collapse invariants."""
    require_route_class(route_class)
    _text(reason, "reason")
    _text(coverage_state, "coverage_state")

    if route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED and route_obligation is None:
        # A learned/adjudicated route is legitimate only when it carries an
        # owner/use-derived obligation. A bare label is not legitimacy
        # (C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001).
        raise RouteLegitimacyError(
            "a LEARNED_OR_ADJUDICATED_REQUIRED envelope must carry a valid "
            "owner-derived RouteObligation; changing the route label alone can never "
            "create a lawful learned route "
            "(C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001)"
        )

    if route_obligation is not None:
        # The claimed route must match the owner-derived obligation exactly.
        assert_route_not_laundered(route_class=route_class, obligation=route_obligation)
        if route_class != route_obligation.required_route_class:
            raise RouteLegitimacyError(
                f"route {route_class!r} does not match the owner-derived obligation "
                f"{route_obligation.required_route_class!r}"
            )

    evidence = tuple(producer_evidence)
    if not evidence:
        raise C103AStateRouteError("at least one competent producer state is required")
    refs = tuple(producer_refs)
    if not refs:
        raise C103AStateRouteError("exact producer refs are required")

    retained = evidence[0].retained_state
    for item in evidence:
        if item.retained_state != retained:
            raise C103AStateRouteError(
                "producer evidence must agree on one retained analytical state; "
                f"got {sorted({i.retained_state for i in evidence})}"
            )

    unvisited = tuple(unvisited_refs)
    if retained == UNVISITED and not unvisited:
        raise C103AStateRouteError(
            "an UNVISITED retained state must carry exact unvisited refs from the adaptive owner"
        )
    if retained != UNVISITED and unvisited:
        raise C103AStateRouteError(
            "unvisited territory may only be retained on the UNVISITED state"
        )
    if retained == UNVISITED and negative_claim_authorized:
        raise C103AStateRouteError(
            "adaptive unvisited territory can never authorize a global negative claim"
        )

    # A selected recursive handoff is a positive selection, never a coverage
    # statement. It must remain bound to the exact coverage record it was
    # selected from (C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001).
    handoff_owners = {
        OWNER_RECURSIVE_HANDOFF_LABEL,
    }
    uses_handoff = any(item.owner in handoff_owners for item in evidence)
    if uses_handoff or coverage_custody is not None:
        if coverage_custody is None:
            raise OwnerProjectionError(
                "a selected positive recursive handoff requires retained custody of its "
                "exact discovery/adaptive coverage record "
                "(C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001)"
            )
        if not isinstance(coverage_custody, RecursiveCoverageCustody):
            raise OwnerProjectionError(
                "coverage_custody must be an owner-derived RecursiveCoverageCustody"
            )
        handoff_refs = {ref.key for ref in refs}
        if coverage_custody.handoff_ref.key not in handoff_refs:
            raise OwnerProjectionError(
                "coverage custody names a handoff that is not among the producer refs"
            )
        if retained == UNVISITED:
            raise C103AStateRouteError(
                "UNVISITED coverage comes from the adaptive owner; a recursive handoff "
                "custody record may not be used to represent unvisited territory"
            )
        if coverage_record_ref is not None and coverage_record_ref != coverage_custody.coverage_record_ref:
            raise OwnerProjectionError(
                "declared coverage_record_ref disagrees with the owner-derived custody record"
            )
        if retained != SUPPORTED_BASELINE and coverage_custody.completeness_state.startswith(
            "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"
        ) and retained not in RETAINABLE_STATES:
            raise C103AStateRouteError("unreachable custody/state combination")
        # Bind the custody into the envelope identity.
        coverage_record_ref = coverage_custody.coverage_record_ref
        reason = f"{reason}; handoff custody {coverage_custody.custody_hash[:16]}"

    disposition = consumer_disposition
    if not isinstance(disposition, ConsumerDisposition):
        raise C103AStateRouteError("consumer_disposition must be a ConsumerDisposition")
    if disposition.consumer_invoked:
        if disposition.consumer_result_state is None:
            raise C103AStateRouteError("an invoked consumer must record its result state")
    elif disposition.non_invocation_reason is None:
        raise C103AStateRouteError(
            "a non-invoked consumer must record an explicit non-invocation reason"
        )

    authorities = tuple(authority_refs)
    for ref in authorities:
        if not isinstance(ref, AuthorityRef):
            raise C103AStateRouteError("authority_refs must be exact AuthorityRef objects")

    provisional = AnalyticalStateRouteResult(
        contract=C1_03A_ENVELOPE_CONTRACT,
        route_class=route_class,
        retained_analytical_state=retained,
        coverage_state=coverage_state,
        reason=reason,
        producer_evidence=evidence,
        producer_refs=refs,
        coverage_record_ref=coverage_record_ref,
        unvisited_refs=unvisited,
        visited_refs=tuple(visited_refs),
        consumer_disposition=disposition,
        upstream_composed_result_hash=upstream_composed_result_hash,
        authority_refs=authorities,
        negative_claim_authorized=negative_claim_authorized,
        route_obligation_hash=route_obligation.obligation_hash if route_obligation else None,
        coverage_custody_hash=coverage_custody.custody_hash if coverage_custody else None,
        projection_laws=tuple(item.projection_law for item in evidence),
        envelope_identity_hash="0" * 64,
        identity_material={},
    )
    preimage = provisional.identity_preimage()
    digest = semantic_hash(preimage)
    return AnalyticalStateRouteResult(
        **{
            **{field_name: getattr(provisional, field_name)
               for field_name in (
                   "contract", "route_class", "retained_analytical_state", "coverage_state",
                   "reason", "producer_evidence", "producer_refs", "coverage_record_ref",
                   "unvisited_refs", "visited_refs", "consumer_disposition",
                   "upstream_composed_result_hash", "authority_refs",
                   "negative_claim_authorized", "route_obligation_hash",
                   "coverage_custody_hash", "projection_laws",
               )},
            "envelope_identity_hash": digest,
            "identity_material": preimage,
        }
    )


__all__ = [
    "C1_03A_ENVELOPE_CONTRACT",
    "MANDATORY_AT14_STATES",
    "OBSERVED_ZERO",
    "VALID_EMPTY",
    "UNDERPOWERED",
    "UNKNOWN_UNRESOLVED",
    "UNVISITED",
    "NONCOMPARABLE",
    "BLOCKED_REQUIRED_AUTHORITY",
    "INTEGRITY_FAILURE",
    "SUPPORTED",
    "EMPIRICAL_FACT_STATE_TO_RETAINED",
    "DISCOVERY_RECEIPT_STATE_TO_RETAINED",
    "DISCOVERY_COVERAGE_STATE_TO_RETAINED",
    "ADAPTIVE_PARTIAL_STATES",
    "ROUTE_DIRECT_EMPIRICAL",
    "ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED",
    "ROUTE_CLASSES",
    "CONSUMER_INVOKED",
    "CONSUMER_NOT_INVOKED_STATE_NOT_LOSSLESSLY_REPRESENTABLE",
    "C103AStateRouteError",
    "OwnerProjectionError",
    "RouteLegitimacyError",
    "OwnerStateProjection",
    "RouteObligation",
    "RecursiveCoverageCustody",
    "OWNER_EMPIRICAL_PROJECTION_LABEL",
    "OWNER_DISCOVERY_PROJECTION_LABEL",
    "OWNER_ADAPTIVE_PROJECTION_LABEL",
    "OWNER_ADMISSION_PROJECTION_LABEL",
    "OWNER_RECURSIVE_HANDOFF_LABEL",
    "require_positive_route",
    "ProducerStateEvidence",
    "ConsumerDisposition",
    "AnalyticalStateRouteResult",
    "classify_empirical_fact_state",
    "classify_empirical_cells",
    "observed_zero_cells",
    "EMPIRICAL_CELL_STATE_OBSERVED_ZERO",
    "EMPIRICAL_CELL_STATE_ZERO_SUPPORT",
    "EMPIRICAL_CELL_STATE_OBSERVED_POSITIVE",
    "RETAINABLE_STATES",
    "SUPPORTED_BASELINE",
    "classify_discovery_receipt_state",
    "classify_adaptive_coverage",
    "require_route_class",
    "assert_route_not_laundered",
    "build_state_route_result",
]
