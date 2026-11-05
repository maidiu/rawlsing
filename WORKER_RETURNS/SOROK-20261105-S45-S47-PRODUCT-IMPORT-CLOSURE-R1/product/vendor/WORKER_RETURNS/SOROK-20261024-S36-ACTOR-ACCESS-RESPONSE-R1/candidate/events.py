"""Precipitating event witness ingress (ADP010 encounter / ADP019 admitted occurrence).

A witness is either source-custodied and admitted, or it is a `TypedMissingWitness`
naming exactly which owner receipt is absent. Missing witnesses are never
fabricated, backdated or inferred from an offer, label or narrative sentence.

C9R hardening: a native-grade witness requires an injected independent owner
receipt resolver. A caller-sealed `ADP019:` reference with no resolvable owner
receipt is refused/missing, never admitted by hash equality. When a focal actor
is supplied, the witness `actor_role` must bind that exact actor, and the focal
actor must appear in the event participants.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .canon import digest, seal, valid

EVENT_WITNESS_SCHEMA = "C9P_EVENT_WITNESS@1"

GRADE_NATIVE = "ADMITTED_NATIVE"
GRADE_TEST_ONLY = "ADMITTED_TEST_ONLY_SOURCEFREE"
GRADE_MISSING = "TYPED_MISSING"

TEST_ONLY_PREFIX = "TEST_ONLY"


class WitnessStatus(str, Enum):
    ADMITTED = "ADMITTED"
    REFUSED = "REFUSED"
    MISSING = "MISSING"


class WitnessReason(str, Enum):
    OK = "OK"
    WITNESS_INTEGRITY_FAILURE = "WITNESS_INTEGRITY_FAILURE"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    EVENT_ID_MISSING = "EVENT_ID_MISSING"
    OWNER_MISSING = "OWNER_MISSING"
    OWNER_GRADE_MISMATCH = "OWNER_GRADE_MISMATCH"
    CLOCK_OUTSIDE_FRAME = "CLOCK_OUTSIDE_FRAME"
    TIME_REVERSED = "TIME_REVERSED"
    CONTENT_HASH_MISMATCH = "CONTENT_HASH_MISMATCH"
    CAUSAL_PARENT_UNRESOLVED = "CAUSAL_PARENT_UNRESOLVED"
    ADMISSION_GRADE_UNAUTHORIZED = "ADMISSION_GRADE_UNAUTHORIZED"
    MISSING_ADP019_OWNER_RECEIPT = "MISSING_ADP019_OWNER_RECEIPT"
    MISSING_ADP010_ENCOUNTER_RECEIPT = "MISSING_ADP010_ENCOUNTER_RECEIPT"
    ACTOR_ROLE_MISSING = "ACTOR_ROLE_MISSING"
    ACTOR_ROLE_NOT_FOCAL = "ACTOR_ROLE_NOT_FOCAL"
    FOCAL_ACTOR_NOT_PARTICIPANT = "FOCAL_ACTOR_NOT_PARTICIPANT"


@runtime_checkable
class OwnerReceiptResolver(Protocol):
    """Independently owned resolution of an ADP019/ADP010 owner receipt."""

    def resolve_owner_receipt(
        self, *, owner_ref: str, owner_receipt_ref: str, event_id: str, as_of: int
    ) -> bool:
        ...


@dataclass(frozen=True)
class TypedMissingWitness:
    """A precisely typed absence of an owner receipt, never a substitute event."""

    missing_kind: str
    reason: WitnessReason
    event_id: str
    expected_owner_ref: str

    @property
    def status(self) -> WitnessStatus:
        return WitnessStatus.MISSING


@dataclass(frozen=True)
class EventWitnessResult:
    """Typed outcome of precipitating-event ingress."""

    status: WitnessStatus
    reason: WitnessReason
    event_id: str
    event_hash: str
    owner_ref: str
    event_time: int
    admission_grade: str
    readset_refs: tuple[str, ...]
    content: Mapping[str, Any] | None = None

    @property
    def admitted(self) -> bool:
        return self.status is WitnessStatus.ADMITTED

    @property
    def scene(self) -> str:
        if isinstance(self.content, Mapping):
            value = self.content.get("scene")
            return value if isinstance(value, str) else ""
        return ""


def _missing(reason: WitnessReason, event_id: str = "") -> EventWitnessResult:
    return EventWitnessResult(
        status=WitnessStatus.MISSING,
        reason=reason,
        event_id=event_id,
        event_hash="",
        owner_ref="",
        event_time=0,
        admission_grade=GRADE_MISSING,
        readset_refs=(),
        content=None,
    )


def _refused(
    reason: WitnessReason, *, event_id: str = "", grade: str = ""
) -> EventWitnessResult:
    return EventWitnessResult(
        status=WitnessStatus.REFUSED,
        reason=reason,
        event_id=event_id,
        event_hash="",
        owner_ref="",
        event_time=0,
        admission_grade=grade,
        readset_refs=(),
        content=None,
    )


def _participants(content: Mapping[str, Any] | None) -> list:
    if not isinstance(content, Mapping):
        return []
    value = content.get("participants")
    return list(value) if isinstance(value, (list, tuple)) else []


def ingress_event(
    raw: Mapping[str, Any],
    *,
    as_of: int,
    last_time: int,
    prior_event_hashes: frozenset[str],
    focal_actor_id: str | None = None,
    owner_resolver: OwnerReceiptResolver | None = None,
) -> EventWitnessResult:
    """Validate one precipitating event witness at frame time `as_of`."""
    if not isinstance(raw, Mapping):
        return _missing(WitnessReason.WITNESS_INTEGRITY_FAILURE)
    if raw.get("schema") != EVENT_WITNESS_SCHEMA:
        return _refused(WitnessReason.SCHEMA_MISMATCH)
    if not valid(raw):
        return _refused(
            WitnessReason.WITNESS_INTEGRITY_FAILURE, event_id=raw.get("event_id", "")
        )
    event_id = raw.get("event_id")
    if not isinstance(event_id, str) or not event_id.strip():
        return _refused(WitnessReason.EVENT_ID_MISSING)
    grade = raw.get("admission_grade")
    owner_ref = raw.get("owner_ref")
    owner_receipt = raw.get("owner_receipt_ref")
    if grade == GRADE_MISSING:
        if not owner_receipt:
            return _missing(WitnessReason.MISSING_ADP019_OWNER_RECEIPT, event_id)
        return _missing(WitnessReason.MISSING_ADP010_ENCOUNTER_RECEIPT, event_id)
    if grade not in (GRADE_NATIVE, GRADE_TEST_ONLY):
        return _refused(
            WitnessReason.ADMISSION_GRADE_UNAUTHORIZED, event_id=event_id, grade=str(grade)
        )
    if grade == GRADE_NATIVE:
        if not owner_receipt:
            return _missing(WitnessReason.MISSING_ADP019_OWNER_RECEIPT, event_id)
        if owner_resolver is None or not owner_resolver.resolve_owner_receipt(
            owner_ref=str(owner_ref or ""),
            owner_receipt_ref=str(owner_receipt),
            event_id=event_id,
            as_of=as_of,
        ):
            return _missing(WitnessReason.MISSING_ADP019_OWNER_RECEIPT, event_id)
    if not isinstance(owner_ref, str) or not owner_ref.strip():
        return _refused(WitnessReason.OWNER_MISSING, event_id=event_id, grade=str(grade))
    if grade == GRADE_TEST_ONLY and not owner_ref.startswith(TEST_ONLY_PREFIX):
        return _refused(
            WitnessReason.OWNER_GRADE_MISMATCH, event_id=event_id, grade=str(grade)
        )
    event_time = raw.get("time")
    if not isinstance(event_time, int) or isinstance(event_time, bool):
        return _refused(
            WitnessReason.CLOCK_OUTSIDE_FRAME, event_id=event_id, grade=str(grade)
        )
    if event_time > as_of or event_time <= last_time:
        return _refused(
            WitnessReason.CLOCK_OUTSIDE_FRAME
            if event_time > as_of
            else WitnessReason.TIME_REVERSED,
            event_id=event_id,
            grade=str(grade),
        )
    content = raw.get("content")
    content_hash = raw.get("content_hash")
    if not isinstance(content, Mapping) or content_hash != digest(dict(content)):
        return _refused(
            WitnessReason.CONTENT_HASH_MISMATCH, event_id=event_id, grade=str(grade)
        )
    actor_role = raw.get("actor_role")
    if not isinstance(actor_role, str) or not actor_role.strip():
        return _refused(
            WitnessReason.ACTOR_ROLE_MISSING, event_id=event_id, grade=str(grade)
        )
    if focal_actor_id is not None:
        if actor_role != focal_actor_id:
            return _refused(
                WitnessReason.ACTOR_ROLE_NOT_FOCAL,
                event_id=event_id,
                grade=str(grade),
            )
        if focal_actor_id not in _participants(content):
            return _refused(
                WitnessReason.FOCAL_ACTOR_NOT_PARTICIPANT,
                event_id=event_id,
                grade=str(grade),
            )
    parents = raw.get("causal_parent_refs")
    if parents is None:
        parents = ()
    if not isinstance(parents, (list, tuple)):
        return _refused(
            WitnessReason.CAUSAL_PARENT_UNRESOLVED, event_id=event_id, grade=str(grade)
        )
    for parent in parents:
        if parent not in prior_event_hashes:
            return _refused(
                WitnessReason.CAUSAL_PARENT_UNRESOLVED,
                event_id=event_id,
                grade=str(grade),
            )
    event_hash = digest({k: v for k, v in raw.items() if k != "hash"})
    readset = [owner_ref]
    if owner_receipt:
        readset.append(str(owner_receipt))
    return EventWitnessResult(
        status=WitnessStatus.ADMITTED,
        reason=WitnessReason.OK,
        event_id=event_id,
        event_hash=event_hash,
        owner_ref=owner_ref,
        event_time=event_time,
        admission_grade=grade,
        readset_refs=tuple(readset),
        content=dict(content),
    )


def make_event_witness(
    *,
    event_id: str,
    owner_ref: str,
    time: int,
    content: Mapping[str, Any],
    actor_role: str,
    admission_grade: str = GRADE_TEST_ONLY,
    causal_parent_refs: tuple[str, ...] = (),
    owner_receipt_ref: str = "",
) -> dict:
    """Build one sealed event witness record for candidate transport."""
    content_dict = dict(content)
    return seal(
        {
            "schema": EVENT_WITNESS_SCHEMA,
            "event_id": event_id,
            "owner_ref": owner_ref,
            "owner_receipt_ref": owner_receipt_ref,
            "admission_grade": admission_grade,
            "time": time,
            "actor_role": actor_role,
            "content": content_dict,
            "content_hash": digest(content_dict),
            "causal_parent_refs": list(causal_parent_refs),
        }
    )


__all__ = [
    "EVENT_WITNESS_SCHEMA",
    "GRADE_MISSING",
    "GRADE_NATIVE",
    "GRADE_TEST_ONLY",
    "EventWitnessResult",
    "OwnerReceiptResolver",
    "TypedMissingWitness",
    "WitnessReason",
    "WitnessStatus",
    "ingress_event",
    "make_event_witness",
]
