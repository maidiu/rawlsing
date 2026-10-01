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
    A caller cannot weaken it by choosing a different label.
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

    @staticmethod
    def from_structural_admission(
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
        return RouteObligation(
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
    """

    handoff_ref: ExactRef
    coverage_record_ref: ExactRef
    completeness_state: str
    supporting_refs: tuple[ExactRef, ...] = ()

    @staticmethod
    def from_handoff(
        handoff: Any,
        *,
        completeness_state: str = "COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        required_supporting_refs: Sequence[ExactRef] = (),
    ) -> "RecursiveCoverageCustody":
        """Derive custody from a real RecursiveBranchHandoff."""
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
        if isinstance(scoped, Mapping):
            scoped_frontier = scoped.get("evaluated_frontier_ref")
            if scoped_frontier is not None:
                if exact_ref(scoped_frontier) != coverage_ref:
                    raise OwnerProjectionError(
                        "handoff frontier ref disagrees with its own retained scope context"
                    )
        supporting = []
        for value in required_supporting_refs:
            if not isinstance(value, ExactRef):
                raise OwnerProjectionError("supporting coverage refs must be exact refs")
            supporting.append(value)
        return RecursiveCoverageCustody(
            handoff_ref=handoff_ref,
            coverage_record_ref=coverage_ref,
            completeness_state=completeness_state,
            supporting_refs=tuple(supporting),
        )

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "handoff_ref": self.handoff_ref.as_dict(),
            "coverage_record_ref": self.coverage_record_ref.as_dict(),
            "completeness_state": self.completeness_state,
            "supporting_refs": [ref.as_dict() for ref in self.supporting_refs],
        }

    @property
    def custody_hash(self) -> str:
        return semantic_hash(self.identity_material())


@dataclass(frozen=True)
class OwnerStateProjection:
    """One competent owner's native state and its *derived* retained projection.

    ``retained_state`` is always computed by :meth:`derive` from the real owner
    object; it is never accepted from a caller. The projection law used is
    recorded so a reviewer can re-derive it.
    """

    owner: str
    producer_state: str
    retained_state: str
    projection_law: str
    reason: str
    producer_ref: ExactRef
    supporting_refs: tuple[ExactRef, ...] = ()
    coverage_state: str = "NOT_APPLICABLE"

    @staticmethod
    def derive(
        *,
        owner: str,
        owner_object: Any,
        projection_law: str,
        derive_fn,
        reason: str,
        producer_ref: ExactRef,
        producer_state: Any,
        supporting_refs: Sequence[ExactRef] = (),
        coverage_state: str = "NOT_APPLICABLE",
    ) -> "OwnerStateProjection":
        """Derive the retained state from a real owner object."""
        try:
            retained = derive_fn(owner_object)
        except C103AStateRouteError:
            raise
        except Exception as exc:  # noqa: BLE001 - a projection must fail closed
            raise OwnerProjectionError(
                f"{projection_law} could not project the owner object for {owner}: {exc}"
            ) from exc
        return OwnerStateProjection(
            owner=owner,
            producer_state=str(producer_state),
            retained_state=str(retained),
            projection_law=projection_law,
            reason=reason,
            producer_ref=producer_ref,
            supporting_refs=tuple(supporting_refs),
            coverage_state=coverage_state,
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
        projection = _exact_cell_projection(fact)
        supporting = ()
        replay = getattr(fact, "replay_ref", None)
        if isinstance(replay, Mapping):
            from rawlsing_next.pre553_empirical_objects import exact_ref

            supporting = (exact_ref(replay),)
        return cls.derive(
            owner=owner,
            owner_object=projection,
            projection_law="classify_empirical_cells(fact.typed_state, complete_cell_semantic_projection)",
            derive_fn=lambda cells: classify_empirical_cells(state, cells),
            reason=reason or "empirical fact state and exact cell projection",
            producer_ref=ref,
            producer_state=state,
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
        return cls.derive(
            owner=owner,
            owner_object=state,
            projection_law="classify_discovery_receipt_state(typed_state, coverage_state)",
            derive_fn=lambda s: classify_discovery_receipt_state(s, coverage or None),
            reason=reason or "exact discovery receipt state with coverage cross-check",
            producer_ref=ref,
            producer_state=state,
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
        """Project a real adaptive search result, requiring its unvisited refs."""
        completeness = str(getattr(adaptive_result, "completeness_state", ""))
        unvisited = tuple(getattr(adaptive_result, "unvisited_unit_refs", ()))
        visited = tuple(getattr(adaptive_result, "visited_unit_refs", ()))
        if not unvisited:
            raise OwnerProjectionError(
                "an adaptive projection requires the owner's own unvisited refs"
            )
        checkpoint = getattr(adaptive_result, "checkpoint", None)
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
        supporting = ref
        checkpoint_ref = getattr(checkpoint, "ref", None)
        if isinstance(checkpoint_ref, ExactRef):
            supporting = (checkpoint_ref, ref)
        return cls.derive(
            owner=owner,
            owner_object=completeness,
            projection_law="classify_adaptive_coverage(completeness_state) with owner unvisited refs",
            derive_fn=lambda s: classify_adaptive_coverage(s),
            reason=reason or "adaptive nonexhaustive coverage with explicit unvisited territory",
            producer_ref=ref,
            producer_state=completeness,
            supporting_refs=supporting,
            coverage_state=completeness,
        )

    @classmethod
    def from_owner_refusal(
        cls,
        *,
        owner: str,
        exception: BaseException,
        reason: str,
        producer_ref: ExactRef,
        supporting_refs: Sequence[ExactRef] = (),
    ) -> "OwnerStateProjection":
        """Project a state proven by the owner *refusing* to proceed.

        Used for INTEGRITY_FAILURE and BLOCKED_REQUIRED_AUTHORITY, where the
        competent owner's own refusal is the evidence. The exception type is
        recorded so the refusal is auditable rather than asserted.
        """
        if not isinstance(exception, BaseException):
            raise OwnerProjectionError("an owner-refusal projection requires the real exception")
        return OwnerStateProjection(
            owner=owner,
            producer_state=f"OWNER_REFUSED:{type(exception).__name__}",
            retained_state=INTEGRITY_FAILURE if "Integrity" in type(exception).__name__ else (
                BLOCKED_REQUIRED_AUTHORITY
            ),
            projection_law="owner refusal (the competent owner declined to proceed)",
            reason=reason,
            producer_ref=producer_ref,
            supporting_refs=tuple(supporting_refs),
            coverage_state="NOT_APPLICABLE",
        )

    @property
    def unvisited_refs(self) -> tuple[ExactRef, ...]:
        return tuple(self.supporting_refs[1:]) if self.coverage_state != "NOT_APPLICABLE" else ()

    def visited_refs(self) -> tuple[ExactRef, ...]:
        return ()

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
