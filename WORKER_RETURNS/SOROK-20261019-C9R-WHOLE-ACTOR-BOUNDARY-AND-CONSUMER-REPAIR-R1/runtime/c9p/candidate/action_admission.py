"""Performed-action owner admission or precise typed HOLD.

A performed action is never hand-authored from a response label or a candidate
route. Admission requires a genuine owner receipt naming the actuator, the
performed act and an independent occurrence reference. Without one, the result
is a typed HOLD naming the exact missing owner form.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .canon import seal, valid

ACTION_ADMISSION_SCHEMA = "C9P_PERFORMED_ACTION_ADMISSION@1"


class AdmissionStatus(str, Enum):
    ADMITTED = "ADMITTED"
    HELD = "HELD"
    REFUSED = "REFUSED"


class AdmissionReason(str, Enum):
    OK = "OK"
    OWNER_RECEIPT_MISSING = "OWNER_RECEIPT_MISSING"
    ACTUATOR_UNBOUND = "ACTUATOR_UNBOUND"
    ACT_UNBOUND = "ACT_UNBOUND"
    OCCURRENCE_REF_MISSING = "OCCURRENCE_REF_MISSING"
    RECEIPT_INTEGRITY_FAILURE = "RECEIPT_INTEGRITY_FAILURE"
    ACTOR_MISMATCH = "ACTOR_MISMATCH"
    TIME_REVERSED = "TIME_REVERSED"
    HAND_AUTHORED_ACTION = "HAND_AUTHORED_ACTION"
    NO_CONSUMED_TARGET_STATE = "NO_CONSUMED_TARGET_STATE"


@dataclass(frozen=True)
class PerformedActionHold:
    """A precise typed HOLD naming the exact missing performed-action owner form."""

    status: AdmissionStatus
    reason: AdmissionReason
    actor_id: str
    expected_owner_form: str
    held_at: int

    @property
    def held(self) -> bool:
        return self.status is AdmissionStatus.HELD


@dataclass(frozen=True)
class PerformedActionAdmission:
    """One admitted performed action bound to its owner receipt and occurrence."""

    status: AdmissionStatus
    reason: AdmissionReason
    actor_id: str
    act: str
    actuator_ref: str
    occurrence_ref: str
    consumed_state_hash: str
    action_time: int
    receipt_hash: str

    @property
    def admitted(self) -> bool:
        return self.status is AdmissionStatus.ADMITTED


def admit_performed_action(
    *,
    owner_receipt: Mapping[str, Any] | None,
    expected_actor_id: str,
    expected_act: str,
    consumed_state_hash: str,
    as_of: int,
    hand_authored: bool = False,
) -> PerformedActionAdmission | PerformedActionHold:
    """Admit one performed action from a genuine owner receipt.

    The receipt must be a sealed mapping carrying `actuator_ref`, `act`,
    `occurrence_ref` and `action_time`. A missing or unsealed receipt returns a
    typed HOLD naming the exact missing owner form. `hand_authored=True` is
    always refused: a candidate response is never a performed action.
    """
    if hand_authored:
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.HAND_AUTHORED_ACTION,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_NOT_HAND_AUTHORABLE",
            held_at=as_of,
        )
    if owner_receipt is None:
        return PerformedActionHold(
            status=AdmissionStatus.HELD,
            reason=AdmissionReason.OWNER_RECEIPT_MISSING,
            actor_id=expected_actor_id,
            expected_owner_form=(
                "OWNER_RECEIPT{actuator_ref, act, occurrence_ref, action_time, "
                "actor_id, consumed_state_hash, hash}"
            ),
            held_at=as_of,
        )
    if not isinstance(owner_receipt, Mapping) or not valid(owner_receipt):
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.RECEIPT_INTEGRITY_FAILURE,
            actor_id=expected_actor_id,
            expected_owner_form="SEALED_OWNER_RECEIPT",
            held_at=as_of,
        )
    if owner_receipt.get("actor_id") != expected_actor_id:
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.ACTOR_MISMATCH,
            actor_id=expected_actor_id,
            expected_owner_form="SEALED_OWNER_RECEIPT",
            held_at=as_of,
        )
    actuator_ref = owner_receipt.get("actuator_ref")
    if not isinstance(actuator_ref, str) or not actuator_ref.strip():
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.ACTUATOR_UNBOUND,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_ACTUATOR_REF",
            held_at=as_of,
        )
    act = owner_receipt.get("act")
    if not isinstance(act, str) or not act.strip():
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.ACT_UNBOUND,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_ACT",
            held_at=as_of,
        )
    if act != expected_act:
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.ACT_UNBOUND,
            actor_id=expected_actor_id,
            expected_owner_form=f"OWNER_RECEIPT_WITH_ACT={expected_act}",
            held_at=as_of,
        )
    occurrence_ref = owner_receipt.get("occurrence_ref")
    if not isinstance(occurrence_ref, str) or not occurrence_ref.strip():
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.OCCURRENCE_REF_MISSING,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_OCCURRENCE_REF",
            held_at=as_of,
        )
    action_time = owner_receipt.get("action_time")
    if not isinstance(action_time, int) or isinstance(action_time, bool):
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.TIME_REVERSED,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_ACTION_TIME",
            held_at=as_of,
        )
    if action_time > as_of:
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.TIME_REVERSED,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_ACTION_TIME",
            held_at=as_of,
        )
    if not consumed_state_hash:
        return PerformedActionHold(
            status=AdmissionStatus.REFUSED,
            reason=AdmissionReason.NO_CONSUMED_TARGET_STATE,
            actor_id=expected_actor_id,
            expected_owner_form="OWNER_RECEIPT_WITH_CONSUMED_STATE_HASH",
            held_at=as_of,
        )
    return PerformedActionAdmission(
        status=AdmissionStatus.ADMITTED,
        reason=AdmissionReason.OK,
        actor_id=expected_actor_id,
        act=act,
        actuator_ref=actuator_ref,
        occurrence_ref=occurrence_ref,
        consumed_state_hash=consumed_state_hash,
        action_time=action_time,
        receipt_hash=owner_receipt["hash"],
    )


def make_performed_action_receipt(
    *,
    actor_id: str,
    act: str,
    actuator_ref: str,
    occurrence_ref: str,
    action_time: int,
    consumed_state_hash: str,
) -> dict:
    """Build one sealed performed-action owner receipt for candidate transport."""
    return seal(
        {
            "schema": ACTION_ADMISSION_SCHEMA,
            "actor_id": actor_id,
            "act": act,
            "actuator_ref": actuator_ref,
            "occurrence_ref": occurrence_ref,
            "action_time": action_time,
            "consumed_state_hash": consumed_state_hash,
        }
    )


__all__ = [
    "ACTION_ADMISSION_SCHEMA",
    "AdmissionReason",
    "AdmissionStatus",
    "PerformedActionAdmission",
    "PerformedActionHold",
    "admit_performed_action",
    "make_performed_action_receipt",
]
