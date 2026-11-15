"""Later-action consumer: E2 committed-state READ and typed missing-consumer refusal.

C9R hardening: the returned body itself must hash to the returned state hash and
must equal an independent re-read of the committed row; a counterfeit body
paired with the real row's digest is refused. The committed record's exact
identity, actor binding and effective time are checked. A later performed action
is never hand-authored: without an authentic performed-action owner receipt the
result stays typed `ACTION_ADMISSION_HELD`.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .canon import digest, seal, valid
from .transaction import CandidateStore


class LaterActionStatus(str, Enum):
    READ_OK = "READ_OK"
    MISSING_CONSUMER = "MISSING_CONSUMER"
    STATE_ABSENT = "STATE_ABSENT"
    AS_OF_BEFORE_COMMIT = "AS_OF_BEFORE_COMMIT"
    CONSUMER_READSET_MISMATCH = "CONSUMER_READSET_MISMATCH"
    CONSUMER_ACTOR_MISMATCH = "CONSUMER_ACTOR_MISMATCH"
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
    """A named downstream reader of committed target state."""

    consumer_id: str
    expected_surface: str

    def read_target(
        self, store: CandidateStore, middle_state_id: str, as_of: int
    ) -> tuple[Mapping[str, Any] | None, str]:
        record = store.read_target_state(middle_state_id)
        if record is None:
            return None, ""
        return record, digest(record)


def _read(
    status: LaterActionStatus,
    *,
    consumer_id: str,
    middle_state_id: str,
    as_of: int,
    reason: str,
    state_hash: str = "",
    record: Mapping[str, Any] | None = None,
    readset_refs: tuple[str, ...] = (),
    route: str = "",
    receipt_hash: str = "",
) -> LaterActionRead:
    return LaterActionRead(
        status=status,
        consumer_id=consumer_id,
        middle_state_id=middle_state_id,
        state_hash=state_hash,
        committed_record=record,
        as_of=as_of,
        readset_refs=readset_refs,
        candidate_route=route,
        read_receipt_hash=receipt_hash,
        reason=reason,
    )


def read_target_for_later_action(
    store: CandidateStore,
    *,
    consumer: LaterActionConsumer | None,
    middle_state_id: str,
    as_of: int,
    commit_time: int,
    action_admission_owner_ref: str = "",
    expected_actor_id: str = "",
    expected_act: str = "",
) -> LaterActionRead:
    """Read committed target state at `as_of` through the named consumer."""
    if consumer is None:
        return _read(
            LaterActionStatus.MISSING_CONSUMER,
            consumer_id="",
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="NO_REGISTERED_LATER_ACTION_CONSUMER",
        )
    if as_of < commit_time:
        return _read(
            LaterActionStatus.AS_OF_BEFORE_COMMIT,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="AS_OF_PRECEDES_TARGET_COMMIT",
        )
    record, state_hash = consumer.read_target(store, middle_state_id, as_of)
    if record is None:
        return _read(
            LaterActionStatus.STATE_ABSENT,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="COMMITTED_TARGET_STATE_ABSENT",
        )
    if not isinstance(record, Mapping):
        return _read(
            LaterActionStatus.CONSUMER_READSET_MISMATCH,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="CONSUMER_RETURNED_NON_MAPPING",
        )
    independently_read = store.read_target_state(middle_state_id)
    if (
        not state_hash
        or digest(record) != state_hash
        or independently_read is None
        or digest(independently_read) != state_hash
        or dict(record) != dict(independently_read)
    ):
        return _read(
            LaterActionStatus.CONSUMER_READSET_MISMATCH,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="RETURNED_BODY_OR_READSET_DIVERGES_FROM_COMMITTED_STATE",
            state_hash=state_hash,
            record=record,
            readset_refs=(middle_state_id,),
        )
    record_hash = record.get("record_hash", "")
    preimage = record.get("record_preimage")
    if preimage is not None:
        if not isinstance(preimage, Mapping) or not valid(dict(preimage)):
            return _read(
                LaterActionStatus.CONSUMER_READSET_MISMATCH,
                consumer_id=consumer.consumer_id,
                middle_state_id=middle_state_id,
                as_of=as_of,
                reason="COMMITTED_RECORD_PREIMAGE_UNSEALED",
                state_hash=state_hash,
                record=record,
                readset_refs=(middle_state_id,),
            )
        preimage_body = {k: v for k, v in preimage.items() if k != "hash"}
        if preimage.get("hash") != record_hash or digest(preimage_body) != record_hash:
            return _read(
                LaterActionStatus.CONSUMER_READSET_MISMATCH,
                consumer_id=consumer.consumer_id,
                middle_state_id=middle_state_id,
                as_of=as_of,
                reason="COMMITTED_RECORD_PREIMAGE_DIGEST_MISMATCH",
                state_hash=state_hash,
                record=record,
                readset_refs=(middle_state_id,),
            )
    if expected_actor_id and record.get("actor_id") != expected_actor_id:
        return _read(
            LaterActionStatus.CONSUMER_ACTOR_MISMATCH,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="COMMITTED_RECORD_ACTOR_MISMATCH",
            state_hash=state_hash,
            record=record,
            readset_refs=(middle_state_id,),
        )
    effective_from = record.get("effective_from")
    if isinstance(effective_from, int) and as_of < effective_from:
        return _read(
            LaterActionStatus.AS_OF_BEFORE_COMMIT,
            consumer_id=consumer.consumer_id,
            middle_state_id=middle_state_id,
            as_of=as_of,
            reason="AS_OF_PRECEDES_RECORD_EFFECTIVE_TIME",
        )
    readset = (middle_state_id, state_hash, consumer.consumer_id)
    read_receipt = seal(
        {
            "schema": "C9P_LATER_ACTION_READ@1",
            "consumer_id": consumer.consumer_id,
            "middle_state_id": middle_state_id,
            "state_hash": state_hash,
            "record_hash": record_hash,
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
    return _read(
        status,
        consumer_id=consumer.consumer_id,
        middle_state_id=middle_state_id,
        as_of=as_of,
        reason=reason,
        state_hash=state_hash,
        record=record,
        readset_refs=readset,
        route=route,
        receipt_hash=read_receipt["hash"],
    )


__all__ = [
    "LaterActionConsumer",
    "LaterActionRead",
    "LaterActionStatus",
    "TypedMissingConsumer",
    "read_target_for_later_action",
]
