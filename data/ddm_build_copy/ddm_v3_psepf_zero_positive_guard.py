#!/usr/bin/env python3
"""Fail-closed PSEPF/structural/observer truth-to-actor transition guard.

Implements only ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE:

* empirical, structural, observer, analyst, and audit/provenance truth has
  zero actor-state effect by default;
* delegation is possible only when an exact, separately accepted positive
  transition authority is present in the production registry bound by a
  separate accepted authority change;
* this guard itself never mutates actor state, causal history, RNG state, or
  scheduler state.

An accepted registry entry is external authority evidence. Defining or
passing a registry entry here does not itself create semantic authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Sequence


GUARD_ID = "IG_PSEPF_ZERO_POSITIVE_GUARD"
GUARD_VERSION = "ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE@1"


class GuardOutcome(str, Enum):
    DENY_ZERO_EFFECT = "DENY_ZERO_EFFECT"
    DELEGATE_TO_ACCEPTED_OWNER = "DELEGATE_TO_ACCEPTED_OWNER"


class GuardReason(str, Enum):
    ZERO_POSITIVE_REGISTRY = "ZERO_POSITIVE_REGISTRY"
    NO_SEPARATELY_ACCEPTED_POSITIVE_AUTHORITY = "NO_SEPARATELY_ACCEPTED_POSITIVE_AUTHORITY"
    UNACCEPTED_AUTHORITY = "UNACCEPTED_AUTHORITY"
    AUTHORITY_BINDING_MISMATCH = "AUTHORITY_BINDING_MISMATCH"
    SOURCE_CLASS_NOT_AUTHORIZED = "SOURCE_CLASS_NOT_AUTHORIZED"
    INVALID_OR_UNTYPED_REQUEST = "INVALID_OR_UNTYPED_REQUEST"
    EXACT_ACCEPTED_AUTHORITY = "EXACT_ACCEPTED_AUTHORITY"


class GuardedTruthClass(str, Enum):
    """Truth/provenance classes that are noncausal absent a positive owner rule."""

    PSEPF = "PSEPF"
    V3_EMPIRICAL_POSSIBILITY_INPUT = "V3EmpiricalPossibilityInput"
    RESOLVED_STRUCTURAL_CONTEXT = "ResolvedStructuralContext"
    STRUCTURAL_PRIOR_REPOSITORY = "StructuralPriorRepository"
    V553_V558_STRUCTURAL_OBJECT = "V553_V558_STRUCTURAL_OBJECT"
    OBSERVER_TRUTH = "OBSERVER_TRUTH"
    ANALYST_TRUTH = "ANALYST_TRUTH"
    ACTOR_COMPARATOR_RECEIPT = "ActorComparatorReceipt"
    REPLAY_RECEIPT = "ReplayReceipt"
    OPAQUE_PROVENANCE = "OPAQUE_PROVENANCE"


@dataclass(frozen=True)
class GuardStateFingerprint:
    """Audit snapshot echoed by the pure guard; never mutated by this module."""

    actor_state_hash: str
    causal_ledger_hash: str
    causal_cursor: str
    rng_state_hash: str
    scheduler_state_hash: str


@dataclass(frozen=True)
class PositiveTransitionAuthorityPresentation:
    """Exact authority material presented with one requested transition."""

    authority_id: str
    authority_version: str
    authority_content_hash: str
    acceptance_ref: str
    acceptance_hash: str
    owner_rule_id: str
    owner_rule_version: str
    owner_rule_content_hash: str
    transition_surface_id: str
    operation_class: str


@dataclass(frozen=True)
class AcceptedPositiveTransitionAuthority:
    """Separately accepted owner binding supplied from outside this guard."""

    authority_id: str
    authority_version: str
    authority_content_hash: str
    acceptance_ref: str
    acceptance_hash: str
    owner_rule_id: str
    owner_rule_version: str
    owner_rule_content_hash: str
    transition_surface_id: str
    operation_class: str
    allowed_source_classes: tuple[GuardedTruthClass, ...]

    @property
    def registry_key(self) -> tuple[str, str, str]:
        return (
            self.authority_id,
            self.authority_version,
            self.authority_content_hash,
        )


@dataclass(frozen=True)
class GuardRequest:
    actor_id: str
    source_class: GuardedTruthClass
    source_ref: str
    source_hash: str
    source_lineage: tuple[GuardedTruthClass, ...]
    transition_surface_id: str
    operation_class: str
    state_fingerprint: GuardStateFingerprint
    authority: PositiveTransitionAuthorityPresentation | None = None


@dataclass(frozen=True)
class GuardDecision:
    guard_id: str
    guard_version: str
    outcome: GuardOutcome
    reason: GuardReason
    actor_id: str
    source_class: str
    transition_surface_id: str
    operation_class: str
    delegated_owner_rule_id: str | None
    actor_state_effect: str
    causal_ledger_appends: int
    causal_cursor_delta: int
    rng_mutations: int
    scheduler_mutations: int
    pre_state_fingerprint: GuardStateFingerprint | None
    post_guard_state_fingerprint: GuardStateFingerprint | None

    @property
    def zero_effect(self) -> bool:
        return (
            self.actor_state_effect == "ZERO"
            and self.causal_ledger_appends == 0
            and self.causal_cursor_delta == 0
            and self.rng_mutations == 0
            and self.scheduler_mutations == 0
            and self.pre_state_fingerprint == self.post_guard_state_fingerprint
        )


AcceptedAuthorityRegistry = Mapping[
    tuple[str, str, str], AcceptedPositiveTransitionAuthority
]

# The active first tranche contains no positive PSEPF/structural/observer
# transition authority. A non-empty production registry requires a separate,
# accepted authority binder/code change.
DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES: AcceptedAuthorityRegistry = (
    MappingProxyType({})
)


def _nonempty(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("expected string")
    value = value.strip()
    if not value:
        raise ValueError("expected non-empty string")
    return value


def _truth_class(value: Any) -> GuardedTruthClass:
    if isinstance(value, GuardedTruthClass):
        return value
    return GuardedTruthClass(_nonempty(value))


def _causal_cursor(value: Any) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return _nonempty(value)


def _state_fingerprint(value: Any) -> GuardStateFingerprint:
    if isinstance(value, GuardStateFingerprint):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("state_fingerprint must be a mapping")
    return GuardStateFingerprint(
        actor_state_hash=_nonempty(value.get("actor_state_hash")),
        causal_ledger_hash=_nonempty(value.get("causal_ledger_hash")),
        causal_cursor=_causal_cursor(value.get("causal_cursor")),
        rng_state_hash=_nonempty(value.get("rng_state_hash")),
        scheduler_state_hash=_nonempty(value.get("scheduler_state_hash")),
    )


def _authority_presentation(
    value: Any,
) -> PositiveTransitionAuthorityPresentation | None:
    if value is None:
        return None
    if isinstance(value, PositiveTransitionAuthorityPresentation):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("authority must be a mapping")
    return PositiveTransitionAuthorityPresentation(
        authority_id=_nonempty(value.get("authority_id")),
        authority_version=_nonempty(value.get("authority_version")),
        authority_content_hash=_nonempty(value.get("authority_content_hash")),
        acceptance_ref=_nonempty(value.get("acceptance_ref")),
        acceptance_hash=_nonempty(value.get("acceptance_hash")),
        owner_rule_id=_nonempty(value.get("owner_rule_id")),
        owner_rule_version=_nonempty(value.get("owner_rule_version")),
        owner_rule_content_hash=_nonempty(value.get("owner_rule_content_hash")),
        transition_surface_id=_nonempty(value.get("transition_surface_id")),
        operation_class=_nonempty(value.get("operation_class")),
    )


def _coerce_request(payload: Any) -> GuardRequest:
    if isinstance(payload, GuardRequest):
        return payload
    if not isinstance(payload, Mapping):
        raise ValueError("request must be GuardRequest or mapping")

    # Exact top-level source typing is mandatory. A generic wrapper cannot hide
    # a guarded source in metadata and acquire permission.
    source_class = _truth_class(payload.get("source_class"))
    raw_lineage = payload.get("source_lineage", ())
    if isinstance(raw_lineage, (str, bytes)) or not isinstance(
        raw_lineage, Sequence
    ):
        raise ValueError("source_lineage must be a sequence")
    source_lineage = tuple(_truth_class(item) for item in raw_lineage)

    return GuardRequest(
        actor_id=_nonempty(payload.get("actor_id")),
        source_class=source_class,
        source_ref=_nonempty(payload.get("source_ref")),
        source_hash=_nonempty(payload.get("source_hash")),
        source_lineage=source_lineage,
        transition_surface_id=_nonempty(payload.get("transition_surface_id")),
        operation_class=_nonempty(payload.get("operation_class")),
        state_fingerprint=_state_fingerprint(payload.get("state_fingerprint")),
        authority=_authority_presentation(payload.get("authority")),
    )


def _deny(
    *,
    reason: GuardReason,
    request: GuardRequest | None = None,
) -> GuardDecision:
    fingerprint = request.state_fingerprint if request is not None else None
    return GuardDecision(
        guard_id=GUARD_ID,
        guard_version=GUARD_VERSION,
        outcome=GuardOutcome.DENY_ZERO_EFFECT,
        reason=reason,
        actor_id=request.actor_id if request is not None else "",
        source_class=request.source_class.value if request is not None else "",
        transition_surface_id=(
            request.transition_surface_id if request is not None else ""
        ),
        operation_class=request.operation_class if request is not None else "",
        delegated_owner_rule_id=None,
        actor_state_effect="ZERO",
        causal_ledger_appends=0,
        causal_cursor_delta=0,
        rng_mutations=0,
        scheduler_mutations=0,
        pre_state_fingerprint=fingerprint,
        post_guard_state_fingerprint=fingerprint,
    )


def _presentation_matches(
    presented: PositiveTransitionAuthorityPresentation,
    accepted: AcceptedPositiveTransitionAuthority,
    request: GuardRequest,
) -> bool:
    return (
        presented.authority_id == accepted.authority_id
        and presented.authority_version == accepted.authority_version
        and presented.authority_content_hash == accepted.authority_content_hash
        and presented.acceptance_ref == accepted.acceptance_ref
        and presented.acceptance_hash == accepted.acceptance_hash
        and presented.owner_rule_id == accepted.owner_rule_id
        and presented.owner_rule_version == accepted.owner_rule_version
        and presented.owner_rule_content_hash == accepted.owner_rule_content_hash
        and presented.transition_surface_id == accepted.transition_surface_id
        and presented.operation_class == accepted.operation_class
        and request.transition_surface_id == accepted.transition_surface_id
        and request.operation_class == accepted.operation_class
    )


def _evaluate_request_against_registry(
    request: GuardRequest,
    accepted_authorities: AcceptedAuthorityRegistry,
) -> GuardDecision:
    """Internal evaluator used only after the request has been fail-closed parsed."""

    if request.authority is None:
        reason = (
            GuardReason.ZERO_POSITIVE_REGISTRY
            if not accepted_authorities
            else GuardReason.NO_SEPARATELY_ACCEPTED_POSITIVE_AUTHORITY
        )
        return _deny(reason=reason, request=request)

    key = (
        request.authority.authority_id,
        request.authority.authority_version,
        request.authority.authority_content_hash,
    )
    accepted = accepted_authorities.get(key)
    if accepted is None:
        return _deny(reason=GuardReason.UNACCEPTED_AUTHORITY, request=request)

    if not _presentation_matches(request.authority, accepted, request):
        return _deny(
            reason=GuardReason.AUTHORITY_BINDING_MISMATCH,
            request=request,
        )

    all_guarded_sources = (request.source_class,) + request.source_lineage
    if any(
        source_class not in accepted.allowed_source_classes
        for source_class in all_guarded_sources
    ):
        return _deny(
            reason=GuardReason.SOURCE_CLASS_NOT_AUTHORIZED,
            request=request,
        )

    # No transition is performed here. This result is permission to call the
    # separately accepted owner rule, not permission to synthesize or mutate
    # actor state inside this guard.
    return GuardDecision(
        guard_id=GUARD_ID,
        guard_version=GUARD_VERSION,
        outcome=GuardOutcome.DELEGATE_TO_ACCEPTED_OWNER,
        reason=GuardReason.EXACT_ACCEPTED_AUTHORITY,
        actor_id=request.actor_id,
        source_class=request.source_class.value,
        transition_surface_id=request.transition_surface_id,
        operation_class=request.operation_class,
        delegated_owner_rule_id=accepted.owner_rule_id,
        actor_state_effect="ZERO",
        causal_ledger_appends=0,
        causal_cursor_delta=0,
        rng_mutations=0,
        scheduler_mutations=0,
        pre_state_fingerprint=request.state_fingerprint,
        post_guard_state_fingerprint=request.state_fingerprint,
    )


def evaluate_psepf_zero_positive_guard(payload: Any) -> GuardDecision:
    """Evaluate the active zero-positive guard with no caller authority override.

    The active production registry is immutable and empty. A later separately
    accepted authority change must update the production registry/binder; a
    runtime caller cannot manufacture positive authority by passing a mapping.
    """

    try:
        request = _coerce_request(payload)
    except (TypeError, ValueError, KeyError):
        return _deny(reason=GuardReason.INVALID_OR_UNTYPED_REQUEST)

    return _evaluate_request_against_registry(
        request,
        DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES,
    )
