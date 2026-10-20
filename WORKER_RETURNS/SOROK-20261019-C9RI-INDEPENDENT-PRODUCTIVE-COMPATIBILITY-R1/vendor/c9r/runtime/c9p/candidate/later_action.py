"""Later-action consumer: E2 target-state READ and typed missing-consumer refusal.

A registered consumer must actually read the committed target state; the read is
bound into a readset receipt. When no consumer is registered the result is a
typed `TypedMissingConsumer` refusal, never a hand-authored later action.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .canon import digest, seal
from .transaction import CandidateStore


class LaterActionStatus(str, Enum):
    READ_OK = "READ_OK"
    MISSING_CONSUMER = "MISSING_CONSUMER"
    STATE_ABSENT = "STATE_ABSENT"
    AS_OF_BEFORE_COMMIT = "AS_OF_BEFORE_COMMIT"
    CONSUMER_READSET_MISMATCH = "CONSUMER_READSET_MISMATCH"
    ACTION_ADMISSION_HELD = "ACTION_ADMISSION_HELD"


@dataclass(frozen=True)
class TypedMissingConsumer:
    """A precisely typed absence of a registered later-action consumer."""

    consumer_id: str
    expected_surface: str
    reason: LaterActionStatus

    @property
    def status(self) -> LaterActionStatus:
        return LaterActionStatus.MISSING_CONSUMER


@dataclass(frozen=True)
class LaterActionRead:
    """One committed target-state read performed by a named later-action consumer."""

    status: LaterActionStatus
    consumer_id: str
    middle_state_id: str
    state_hash: str
    committed_record: Mapping[str, Any] | None
    as_of: int
    readset_refs: tuple[str, ...]
    candidate_route: str
    read_receipt_hash: str
    reason: str

    @property
    def ok(self) -> bool:
        return self.status is LaterActionStatus.READ_OK


@dataclass(frozen=True)
class LaterActionConsumer:
    """A named downstream reader of committed target state.

    `read_target` is the exact consumer entrypoint that reads committed state;
    it must return the state hash it read so the readset can be verified.
    """

    consumer_id: str
    expected_surface: str

    def read_target(
        self, store: CandidateStore, middle_state_id: str, as_of: int
    ) -> tuple[Mapping[str, Any] | None, str]:
        record = store.read_target_state(middle_state_id)
        if record is None:
            return None, ""
        return record, digest(record)


def read_target_for_later_action(
    store: CandidateStore,
    *,
    consumer: LaterActionConsumer | None,
    middle_state_id: str,
    as_of: int,
    commit_time: int,
    action_admission_owner_ref: str = "",
) -> LaterActionRead:
    """Read committed target state at `as_of` through the named consumer.

    Without a registered consumer this returns a typed `MISSING_CONSUMER` refusal.
    When the consumer is present, the exact record and the hash the consumer
    returned are compared; a mismatch is a typed `CONSUMER_READSET_MISMATCH`.
    A later performed action is never hand-authored here; without a genuine
    performed-action owner the result stays at `ACTION_ADMISSION_HELD`.
    """
    if consumer is None:
        return LaterActionRead(
            status=LaterActionStatus.MISSING_CONSUMER,
            consumer_id="",
            middle_state_id=middle_state_id,
            state_hash="",
            committed_record=None,
            as_of=as_of,
            readset_refs=(),
            candidate_route="",
            read_receipt_hash="",
            reason="NO_REGISTERED_LATER_ACTION_CONSUMER",
        )
    if as_of < commit_time:
        return LaterActionRead(
            status=LaterActionStatus.AS_OF_BEFORE_COMMIT,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            state_hash="",
            committed_record=None,
            as_of=as_of,
            readset_refs=(),
            candidate_route="",
            read_receipt_hash="",
            reason="AS_OF_PRECEDES_TARGET_COMMIT",
        )
    record, state_hash = consumer.read_target(store, middle_state_id, as_of)
    if record is None:
        return LaterActionRead(
            status=LaterActionStatus.STATE_ABSENT,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            state_hash="",
            committed_record=None,
            as_of=as_of,
            readset_refs=(),
            candidate_route="",
            read_receipt_hash="",
            reason="COMMITTED_TARGET_STATE_ABSENT",
        )
    independently_read = store.read_target_state(middle_state_id)
    if independently_read is None or digest(independently_read) != state_hash:
        return LaterActionRead(
            status=LaterActionStatus.CONSUMER_READSET_MISMATCH,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            state_hash=state_hash,
            committed_record=record,
            as_of=as_of,
            readset_refs=(middle_state_id,),
            candidate_route="",
            read_receipt_hash="",
            reason="CONSUMER_READ_DIVERGES_FROM_COMMITTED_STATE",
        )
    readset = (middle_state_id, state_hash, consumer.consumer_id)
    read_receipt = seal(
        {
            "schema": "C9P_LATER_ACTION_READ@1",
            "consumer_id": consumer.consumer_id,
            "middle_state_id": middle_state_id,
            "state_hash": state_hash,
            "as_of": as_of,
            "readset_refs": list(readset),
        }
    )
    route = "PRACTICE_MEDIATED_ACTION_ROUTE"
    status = LaterActionStatus.READ_OK
    reason = "OK"
    if not action_admission_owner_ref:
        status = LaterActionStatus.ACTION_ADMISSION_HELD
        reason = "PERFORMED_ACTION_OWNER_UNPROVED"
    return LaterActionRead(
        status=status,
        consumer_id=consumer.consumer_id,
        middle_state_id=middle_state_id,
        state_hash=state_hash,
        committed_record=record,
        as_of=as_of,
        readset_refs=readset,
        candidate_route=route,
        read_receipt_hash=read_receipt["hash"],
        reason=reason,
    )


__all__ = [
    "LaterActionConsumer",
    "LaterActionRead",
    "LaterActionStatus",
    "TypedMissingConsumer",
    "read_target_for_later_action",
]
