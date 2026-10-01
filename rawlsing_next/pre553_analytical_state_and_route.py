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

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

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
    """One competent owner's native negative/positive state, bound to its refs.

    ``owner`` names the actual public owner that produced ``producer_state``.
    Nothing in this record is inferred; it is a custody projection.
    """

    owner: str
    producer_state: str
    retained_state: str
    reason: str
    producer_ref: ExactRef
    supporting_refs: tuple[ExactRef, ...] = ()
    coverage_state: str = "NOT_APPLICABLE"

    def __post_init__(self) -> None:
        _text(self.owner, "owner")
        _text(self.producer_state, "producer_state")
        _text(self.reason, "reason")
        if self.retained_state not in RETAINABLE_STATES:
            raise C103AStateRouteError(
                f"retained_state {self.retained_state!r} is not a retainable analytical state"
            )


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
    required_route_class: str,
    producer_state: str,
    reason: str,
) -> None:
    """Fail closed if a route label is used to bypass a genuine requirement.

    The route label never creates authority. If current owner state shows the
    route requires learned/adjudicated support and the caller claims a direct
    empirical route, that is a laundering attempt and must raise.
    """
    require_route_class(route_class)
    if (
        required_route_class == ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED
        and route_class == ROUTE_DIRECT_EMPIRICAL
    ):
        raise RouteLegitimacyError(
            "ROUTE_LAUNDERING_REJECTED: "
            f"producer_state={producer_state!r} requires "
            f"{ROUTE_LEARNED_OR_ADJUDICATED_REQUIRED} but was labelled "
            f"{ROUTE_DIRECT_EMPIRICAL} ({reason})"
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
) -> AnalyticalStateRouteResult:
    """Assemble the bounded envelope, enforcing the anti-collapse invariants."""
    require_route_class(route_class)
    _text(reason, "reason")
    _text(coverage_state, "coverage_state")

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
                   "negative_claim_authorized",
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
    "RouteLegitimacyError",
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
