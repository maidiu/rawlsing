"""Precipitating event witness ingress (ADP010 generated encounter / ADP019 admitted occurrence).

A witness is either source-custodied and admitted, or it is a `TypedMissingWitness`
naming exactly which owner receipt is absent. Missing witnesses are never
fabricated, backdated or inferred from an offer, label or narrative sentence.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .canon import seal, valid

EVENT_WITNESS_SCHEMA = "C9P_EVENT_WITNESS@1"

# Admission grades carried by a witness record.
GRADE_NATIVE = "ADMITTED_NATIVE"
GRADE_TEST_ONLY = "ADMITTED_TEST_ONLY_SOURCEFREE"
GRADE_MISSING = "TYPED_MISSING"


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

    @property
    def admitted(self) -> bool:
        return self.status is WitnessStatus.ADMITTED


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
    )


def ingress_event(
    raw: Mapping[str, Any],
    *,
    as_of: int,
    last_time: int,
    prior_event_hashes: frozenset[str],
) -> EventWitnessResult:
    """Validate one precipitating event witness at frame time `as_of`.

    `last_time` is the greatest previously committed event time; `prior_event_hashes`
    are the exact hashes of already admitted causal parents. A witness whose owner
    receipt is absent returns `MISSING` with the exact missing kind, never a
    synthetic occurrence.
    """
    if not isinstance(raw, Mapping):
        return _missing(WitnessReason.WITNESS_INTEGRITY_FAILURE)
    if raw.get("schema") != EVENT_WITNESS_SCHEMA:
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.SCHEMA_MISMATCH,
            event_id="",
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade="",
            readset_refs=(),
        )
    if not valid(raw):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.WITNESS_INTEGRITY_FAILURE,
            event_id=raw.get("event_id", ""),
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade="",
            readset_refs=(),
        )
    event_id = raw.get("event_id")
    if not isinstance(event_id, str) or not event_id.strip():
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.EVENT_ID_MISSING,
            event_id="",
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade="",
            readset_refs=(),
        )
    grade = raw.get("admission_grade")
    owner_ref = raw.get("owner_ref")
    owner_receipt = raw.get("owner_receipt_ref")
    if grade == GRADE_MISSING:
        if not owner_receipt:
            return _missing(WitnessReason.MISSING_ADP019_OWNER_RECEIPT, event_id)
        return _missing(WitnessReason.MISSING_ADP010_ENCOUNTER_RECEIPT, event_id)
    if grade not in (GRADE_NATIVE, GRADE_TEST_ONLY):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.ADMISSION_GRADE_UNAUTHORIZED,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    if grade == GRADE_NATIVE and not owner_receipt:
        return _missing(WitnessReason.MISSING_ADP019_OWNER_RECEIPT, event_id)
    if not isinstance(owner_ref, str) or not owner_ref.strip():
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.OWNER_MISSING,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    if grade == GRADE_TEST_ONLY and not owner_ref.startswith("TEST_ONLY"):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.OWNER_GRADE_MISMATCH,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    event_time = raw.get("time")
    if not isinstance(event_time, int) or isinstance(event_time, bool):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.CLOCK_OUTSIDE_FRAME,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    if event_time > as_of or event_time <= last_time:
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.CLOCK_OUTSIDE_FRAME
            if event_time > as_of
            else WitnessReason.TIME_REVERSED,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    content = raw.get("content")
    content_hash = raw.get("content_hash")
    from .canon import digest as _digest

    if not isinstance(content, Mapping) or content_hash != _digest(dict(content)):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.CONTENT_HASH_MISMATCH,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    actor_role = raw.get("actor_role")
    if not isinstance(actor_role, str) or not actor_role.strip():
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.ACTOR_ROLE_MISSING,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    parents = raw.get("causal_parent_refs")
    if parents is None:
        parents = ()
    if not isinstance(parents, (list, tuple)):
        return EventWitnessResult(
            status=WitnessStatus.REFUSED,
            reason=WitnessReason.CAUSAL_PARENT_UNRESOLVED,
            event_id=event_id,
            event_hash="",
            owner_ref="",
            event_time=0,
            admission_grade=str(grade),
            readset_refs=(),
        )
    for parent in parents:
        if parent not in prior_event_hashes:
            return EventWitnessResult(
                status=WitnessStatus.REFUSED,
                reason=WitnessReason.CAUSAL_PARENT_UNRESOLVED,
                event_id=event_id,
                event_hash="",
                owner_ref="",
                event_time=0,
                admission_grade=str(grade),
                readset_refs=(),
            )
    from .canon import digest as _digest

    event_hash = _digest({k: v for k, v in raw.items() if k != "hash"})
    readset = [owner_ref]
    if owner_receipt:
        readset.append(owner_receipt)
    return EventWitnessResult(
        status=WitnessStatus.ADMITTED,
        reason=WitnessReason.OK,
        event_id=event_id,
        event_hash=event_hash,
        owner_ref=owner_ref,
        event_time=event_time,
        admission_grade=grade,
        readset_refs=tuple(readset),
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
    from .canon import digest as _digest

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
            "content_hash": _digest(content_dict),
            "causal_parent_refs": list(causal_parent_refs),
        }
    )


__all__ = [
    "EVENT_WITNESS_SCHEMA",
    "GRADE_MISSING",
    "GRADE_NATIVE",
    "GRADE_TEST_ONLY",
    "EventWitnessResult",
    "TypedMissingWitness",
    "WitnessReason",
    "WitnessStatus",
    "ingress_event",
    "make_event_witness",
]
