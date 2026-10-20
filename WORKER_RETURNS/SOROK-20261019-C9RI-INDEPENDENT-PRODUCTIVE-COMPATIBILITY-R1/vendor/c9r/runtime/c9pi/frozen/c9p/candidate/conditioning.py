"""Read-only person and world conditioning (CAN008 R2 conditioning-input role).

Conditioning sources are bound as a read-only view. Any attempted mutation is
refused. Source-class truth (PSEPF, structural, observer, analyst) never becomes
actor psychological state: the native `v3_psepf_zero_positive_guard` is consulted
for every source class, and its zero-effect denial is preserved.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .canon import digest, seal, valid

CONDITIONING_SCHEMA = "C9P_CONDITIONING_BUNDLE@1"

# Source classes that may never be converted into actor psychological state.
NON_PSYCHOLOGICAL_SOURCE_CLASSES = frozenset(
    {
        "PSEPF",
        "V3EmpiricalPossibilityInput",
        "ResolvedStructuralContext",
        "StructuralPriorRepository",
        "V553_V558_STRUCTURAL_OBJECT",
        "OBSERVER_TRUTH",
        "ANALYST_TRUTH",
        "ActorComparatorReceipt",
        "ReplayReceipt",
        "OPAQUE_PROVENANCE",
    }
)

# The exact Pyat-source-to-psyche conversion operations that must be refused.
FORBIDDEN_CONVERSIONS = {
    "structural_position_to_trait": "STRUCTURAL_TO_PSYCHOLOGY",
    "observer_note_to_belief": "OBSERVER_TO_BELIEF",
    "demographic_to_propensity": "DEMOGRAPHY_TO_PSYCHOLOGY",
    "source_text_to_affect": "SOURCE_TEXT_TO_AFFECT",
    "world_fact_to_actor_knowledge": "WORLD_FACT_TO_ACTOR_KNOWLEDGE",
    "other_private_motive_to_actor_state": "OTHER_PRIVATE_MOTIVE_LEAK",
}


class ConditioningStatus(str, Enum):
    BOUND = "BOUND"
    REFUSED = "REFUSED"


class ConditioningReason(str, Enum):
    OK = "OK"
    BUNDLE_INTEGRITY_FAILURE = "BUNDLE_INTEGRITY_FAILURE"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    SOURCE_UNSEALED = "SOURCE_UNSEALED"
    SOURCE_CLASS_UNAUTHORIZED = "SOURCE_CLASS_UNAUTHORIZED"
    WRITE_ATTEMPTED = "WRITE_ATTEMPTED"
    FORBIDDEN_CONVERSION = "FORBIDDEN_CONVERSION"
    READSET_INCOMPLETE = "READSET_INCOMPLETE"
    NATIVE_GUARD_DENIED = "NATIVE_GUARD_DENIED"


@dataclass(frozen=True)
class ConditioningSource:
    """One source-custodied conditioning input, bound read-only."""

    source_ref: str
    source_hash: str
    source_class: str
    subject: str
    sealed_record: Mapping[str, Any] = field(repr=False, default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "source_ref": self.source_ref,
            "source_hash": self.source_hash,
            "source_class": self.source_class,
            "subject": self.subject,
        }


@dataclass(frozen=True)
class ConditioningView:
    """Read-only projection of the bound conditioning sources for one event."""

    status: ConditioningStatus
    reason: ConditioningReason
    subject: str
    sources: tuple[Mapping[str, Any], ...]
    readset_refs: tuple[str, ...]
    guard_outcome: str
    guard_reason: str
    bundle_hash: str

    @property
    def bound(self) -> bool:
        return self.status is ConditioningStatus.BOUND

    def assert_read_only(self) -> None:
        """Raise when a caller attempts to mutate the conditioning view."""
        raise ConditioningRefusal(
            ConditioningReason.WRITE_ATTEMPTED.value,
            "conditioning view is read-only; no Pyat-source-to-psyche write exists",
        )


class ConditioningRefusal(Exception):
    """A conditioning source was unbound, unauthorized or mutated."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def _guard_decision(source_class: str, source_ref: str, source_hash: str) -> tuple[str, str]:
    """Consult the native zero-positive guard for one conditioning source class.

    Returns the guard's (outcome, reason) pair. The guard's production registry is
    empty, so every guarded truth class denies zero effect; this module preserves
    that denial and never mutates actor state from a conditioning source.
    """
    from rawlsing_next import v3_psepf_zero_positive_guard as native_guard

    fingerprint = {
        "actor_state_hash": digest({"subject": source_ref, "state": "CONDITIONING_BASELINE"}),
        "causal_ledger_hash": digest({"events": []}),
        "causal_cursor": "0",
        "rng_state_hash": digest({"rng": "UNCHANGED_BASELINE"}),
        "scheduler_state_hash": digest({"scheduler": "UNCHANGED_BASELINE"}),
    }
    try:
        guarded = native_guard.GuardedTruthClass(source_class)
    except ValueError:
        return ("DENY_ZERO_EFFECT", "SOURCE_CLASS_NOT_AUTHORIZED")
    decision = native_guard.evaluate_psepf_zero_positive_guard(
        {
            "actor_id": "C9P_CONDITIONING_SUBJECT",
            "source_class": guarded.value,
            "source_ref": source_ref,
            "source_hash": source_hash,
            "source_lineage": [],
            "transition_surface_id": "C9P.CONDITIONING.ZERO_EFFECT",
            "operation_class": "VALIDATE_ZERO_EFFECT_ONLY",
            "state_fingerprint": fingerprint,
        }
    )
    return (decision.outcome.value, decision.reason.value)


def bind_conditioning(
    *,
    subject: str,
    sources: list[Mapping[str, Any]],
    as_of: int,
    requested_conversions: Mapping[str, bool] | None = None,
) -> ConditioningView:
    """Bind person/world conditioning sources as a read-only view.

    Every source must be a sealed mapping with `source_ref`, `source_hash`,
    `source_class` and `subject`. Any requested conversion named in
    `FORBIDDEN_CONVERSIONS` refuses the bundle. The native zero-positive guard is
    consulted per source class and its denial is recorded, not bypassed.
    """
    empty = ConditioningView(
        status=ConditioningStatus.REFUSED,
        reason=ConditioningReason.BUNDLE_INTEGRITY_FAILURE,
        subject=subject,
        sources=(),
        readset_refs=(),
        guard_outcome="",
        guard_reason="",
        bundle_hash="",
    )
    if requested_conversions:
        for key, requested in requested_conversions.items():
            if requested and key in FORBIDDEN_CONVERSIONS:
                return ConditioningView(
                    status=ConditioningStatus.REFUSED,
                    reason=ConditioningReason.FORBIDDEN_CONVERSION,
                    subject=subject,
                    sources=(),
                    readset_refs=(),
                    guard_outcome="",
                    guard_reason=FORBIDDEN_CONVERSIONS[key],
                    bundle_hash="",
                )
    bound_sources: list[Mapping[str, Any]] = []
    readset: list[str] = []
    guard_outcomes: list[str] = []
    guard_reasons: list[str] = []
    for raw in sources:
        if not isinstance(raw, Mapping):
            return empty
        if not valid(raw):
            return ConditioningView(
                status=ConditioningStatus.REFUSED,
                reason=ConditioningReason.SOURCE_UNSEALED,
                subject=subject,
                sources=(),
                readset_refs=(),
                guard_outcome="",
                guard_reason="",
                bundle_hash="",
            )
        source_ref = raw.get("source_ref")
        source_hash = raw.get("source_hash")
        source_class = raw.get("source_class")
        if (
            not isinstance(source_ref, str)
            or not isinstance(source_hash, str)
            or not isinstance(source_class, str)
        ):
            return empty
        if raw.get("subject") != subject:
            return empty
        if source_class not in NON_PSYCHOLOGICAL_SOURCE_CLASSES:
            return ConditioningView(
                status=ConditioningStatus.REFUSED,
                reason=ConditioningReason.SOURCE_CLASS_UNAUTHORIZED,
                subject=subject,
                sources=(),
                readset_refs=(),
                guard_outcome="",
                guard_reason=source_class,
                bundle_hash="",
            )
        outcome, guard_reason = _guard_decision(source_class, source_ref, source_hash)
        guard_outcomes.append(outcome)
        guard_reasons.append(guard_reason)
        bound_sources.append(
            {
                "source_ref": source_ref,
                "source_hash": source_hash,
                "source_class": source_class,
                "subject": subject,
            }
        )
        readset.append(source_ref)
    bundle = {"schema": CONDITIONING_SCHEMA, "subject": subject, "sources": bound_sources}
    bundle_sealed = seal(bundle)
    return ConditioningView(
        status=ConditioningStatus.BOUND,
        reason=ConditioningReason.OK,
        subject=subject,
        sources=tuple(bound_sources),
        readset_refs=tuple(readset),
        guard_outcome="|".join(guard_outcomes),
        guard_reason="|".join(guard_reasons),
        bundle_hash=bundle_sealed["hash"],
    )


def make_conditioning_source(
    *,
    source_ref: str,
    source_class: str,
    subject: str,
    body: Mapping[str, Any] | None = None,
) -> dict:
    """Build one sealed conditioning source record for candidate transport."""
    body_dict = dict(body or {})
    return seal(
        {
            "schema": CONDITIONING_SCHEMA,
            "source_ref": source_ref,
            "source_class": source_class,
            "subject": subject,
            "content": body_dict,
            "source_hash": digest({"ref": source_ref, "class": source_class, "content": body_dict}),
        }
    )


__all__ = [
    "CONDITIONING_SCHEMA",
    "ConditioningReason",
    "ConditioningRefusal",
    "ConditioningSource",
    "ConditioningStatus",
    "ConditioningView",
    "FORBIDDEN_CONVERSIONS",
    "NON_PSYCHOLOGICAL_SOURCE_CLASSES",
    "bind_conditioning",
    "make_conditioning_source",
]
