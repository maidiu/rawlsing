"""Read-only person and world conditioning (CAN008 R2 conditioning-input role).

C9R hardening: a source's declared `source_hash` must equal the canonical digest
of its actual ref/class/content preimage; a resealed false-digest source is
refused. Bound sources are deeply immutable, and material eligibility is
evaluated from the actual source content (access, scene, effective time), not
from a caller's bare reference string. The native zero-positive guard is still
consulted per source class and its denial is preserved.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .canon import digest, seal, valid

CONDITIONING_SCHEMA = "C9P_CONDITIONING_BUNDLE@1"

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

MATERIAL_SOURCE_CLASSES = frozenset(
    {"ResolvedStructuralContext", "V553_V558_STRUCTURAL_OBJECT"}
)

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
    SOURCE_HASH_MISMATCH = "SOURCE_HASH_MISMATCH"
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
        raise ConditioningRefusal(
            ConditioningReason.WRITE_ATTEMPTED.value,
            "conditioning view is read-only; no Pyat-source-to-psyche write exists",
        )


class ConditioningRefusal(Exception):
    """A conditioning source was unbound, unauthorized or mutated."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


def _guard_decision(source_class: str, source_ref: str, source_hash: str) -> tuple[str, str]:
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


def _refused(reason: ConditioningReason, subject: str) -> ConditioningView:
    return ConditioningView(
        status=ConditioningStatus.REFUSED,
        reason=reason,
        subject=subject,
        sources=(),
        readset_refs=(),
        guard_outcome="",
        guard_reason="",
        bundle_hash="",
    )


def bind_conditioning(
    *,
    subject: str,
    sources: list[Mapping[str, Any]],
    as_of: int,
    requested_conversions: Mapping[str, bool] | None = None,
) -> ConditioningView:
    """Bind person/world conditioning sources as a deeply read-only view."""
    if requested_conversions:
        for key, requested in requested_conversions.items():
            if requested and key in FORBIDDEN_CONVERSIONS:
                view = _refused(ConditioningReason.FORBIDDEN_CONVERSION, subject)
                return ConditioningView(
                    status=view.status,
                    reason=view.reason,
                    subject=view.subject,
                    sources=view.sources,
                    readset_refs=view.readset_refs,
                    guard_outcome="",
                    guard_reason=FORBIDDEN_CONVERSIONS[key],
                    bundle_hash="",
                )
    bound_sources: list[Mapping[str, Any]] = []
    bundle_sources: list[dict] = []
    readset: list[str] = []
    guard_outcomes: list[str] = []
    guard_reasons: list[str] = []
    for raw in sources:
        if not isinstance(raw, Mapping):
            return _refused(ConditioningReason.BUNDLE_INTEGRITY_FAILURE, subject)
        if not valid(raw):
            return _refused(ConditioningReason.SOURCE_UNSEALED, subject)
        source_ref = raw.get("source_ref")
        source_hash = raw.get("source_hash")
        source_class = raw.get("source_class")
        if (
            not isinstance(source_ref, str)
            or not source_ref.strip()
            or not isinstance(source_hash, str)
            or not source_hash.strip()
            or not isinstance(source_class, str)
        ):
            return _refused(ConditioningReason.BUNDLE_INTEGRITY_FAILURE, subject)
        if raw.get("subject") != subject:
            return _refused(ConditioningReason.BUNDLE_INTEGRITY_FAILURE, subject)
        if source_class not in NON_PSYCHOLOGICAL_SOURCE_CLASSES:
            view = _refused(ConditioningReason.SOURCE_CLASS_UNAUTHORIZED, subject)
            return ConditioningView(
                status=view.status,
                reason=view.reason,
                subject=view.subject,
                sources=view.sources,
                readset_refs=view.readset_refs,
                guard_outcome="",
                guard_reason=source_class,
                bundle_hash="",
            )
        content = raw.get("content", {})
        if not isinstance(content, Mapping):
            return _refused(ConditioningReason.BUNDLE_INTEGRITY_FAILURE, subject)
        content_dict = dict(content)
        expected_hash = digest(
            {"ref": source_ref, "class": source_class, "content": content_dict}
        )
        if source_hash != expected_hash:
            return _refused(ConditioningReason.SOURCE_HASH_MISMATCH, subject)
        outcome, guard_reason = _guard_decision(source_class, source_ref, source_hash)
        guard_outcomes.append(outcome)
        guard_reasons.append(guard_reason)
        bound_sources.append(
            _freeze(
                {
                    "source_ref": source_ref,
                    "source_hash": source_hash,
                    "source_class": source_class,
                    "subject": subject,
                    "content": content_dict,
                }
            )
        )
        bundle_sources.append(
            {
                "source_ref": source_ref,
                "source_hash": source_hash,
                "source_class": source_class,
                "subject": subject,
                "content": content_dict,
            }
        )
        readset.append(source_ref)
    bundle = {
        "schema": CONDITIONING_SCHEMA,
        "subject": subject,
        "sources": bundle_sources,
    }
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


def eligible_material(
    view: ConditioningView, *, event_scene: str, event_time: int, as_of: int
) -> tuple[bool, tuple[str, ...], str]:
    """Return whether any bound source is an eligible present material opportunity.

    Eligibility is read from the actual source content: granted access, a scene
    equal to the event scene, and an effective time no later than the event.
    Observer/analyst truth and private beliefs never qualify as material access.
    """
    if not view.bound:
        return (False, (), "CONDITIONING_NOT_BOUND")
    eligible: list[str] = []
    for source in view.sources:
        if source.get("source_class") not in MATERIAL_SOURCE_CLASSES:
            continue
        content = source.get("content", {})
        if not isinstance(content, Mapping):
            continue
        access = content.get("access")
        scene = content.get("scene")
        effective = content.get("as_of")
        if access != "granted":
            continue
        if not isinstance(scene, str) or scene != event_scene:
            continue
        if not isinstance(effective, int) or isinstance(effective, bool):
            continue
        if effective > event_time or effective > as_of:
            continue
        eligible.append(source.get("source_ref", ""))
    if not eligible:
        return (False, (), "NO_ELIGIBLE_MATERIAL_SOURCE")
    return (True, tuple(eligible), "OK")


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
    "MATERIAL_SOURCE_CLASSES",
    "NON_PSYCHOLOGICAL_SOURCE_CLASSES",
    "bind_conditioning",
    "eligible_material",
    "make_conditioning_source",
]
