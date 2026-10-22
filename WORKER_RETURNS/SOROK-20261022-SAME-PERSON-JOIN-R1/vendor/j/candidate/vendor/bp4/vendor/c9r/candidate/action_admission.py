"""Performed-action owner admission or precise typed HOLD.

C9R hardening: the owner receipt must bind the exact consumed state hash, a
target-commit lower bound and an independent actuator/occurrence. A receipt for
a different state, an action before the target commit, a self-actuator, a
never-performed occurrence or a missing test-only declaration is refused. A
candidate response is never a performed action.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .canon import seal, valid

ACTION_ADMISSION_SCHEMA = "C9P_PERFORMED_ACTION_ADMISSION@1"
TEST_ONLY_ACTUATOR_PREFIX = "TEST_ONLY_ACTUATOR"
TEST_ONLY_OCCURRENCE_PREFIX = "TEST_ONLY_OCCURRENCE"
TEST_ONLY_PREFIX = "TEST_ONLY"


class AdmissionStatus(str, Enum):
    ADMITTED = "ADMITTED"
    HELD = "HELD"
    REFUSED = "REFUSED"


class AdmissionReason(str, Enum):
    OK = "OK"
    OWNER_RECEIPT_MISSING = "OWNER_RECEIPT_MISSING"
    ACTUATOR_UNBOUND = "ACTUATOR_UNBOUND"
    ACTUATOR_SELF_BOUND = "ACTUATOR_SELF_BOUND"
    ACTUATOR_NOT_INDEPENDENT = "ACTUATOR_NOT_INDEPENDENT"
    ACT_UNBOUND = "ACT_UNBOUND"
    OCCURRENCE_REF_MISSING = "OCCURRENCE_REF_MISSING"
    OCCURRENCE_NOT_INDEPENDENT = "OCCURRENCE_NOT_INDEPENDENT"
    RECEIPT_INTEGRITY_FAILURE = "RECEIPT_INTEGRITY_FAILURE"
    ACTOR_MISMATCH = "ACTOR_MISMATCH"
    TIME_REVERSED = "TIME_REVERSED"
    TARGET_COMMIT_TIME_UNBOUND = "TARGET_COMMIT_TIME_UNBOUND"
    ACTION_BEFORE_TARGET_COMMIT = "ACTION_BEFORE_TARGET_COMMIT"
    CONSUMED_STATE_MISMATCH = "CONSUMED_STATE_MISMATCH"
    HAND_AUTHORED_ACTION = "HAND_AUTHORED_ACTION"
    NO_CONSUMED_TARGET_STATE = "NO_CONSUMED_TARGET_STATE"


@runtime_checkable
class OccurrenceResolver(Protocol):
    def resolve_occurrence(self, *, occurrence_ref: str, actor_id: str, as_of: int) -> bool:
        ...


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
    target_commit_time: int = 0
    publication_grade: str = "TEST_ONLY_SOURCEFREE_TECHNICAL"

    @property
    def admitted(self) -> bool:
        return self.status is AdmissionStatus.ADMITTED


def _hold(
    status: AdmissionStatus,
    reason: AdmissionReason,
    actor_id: str,
    as_of: int,
    expected: str,
) -> PerformedActionHold:
    return PerformedActionHold(
        status=status,
        reason=reason,
        actor_id=actor_id,
        expected_owner_form=expected,
        held_at=as_of,
    )


def admit_performed_action(
    *,
    owner_receipt: Mapping[str, Any] | None,
    expected_actor_id: str,
    expected_act: str,
    consumed_state_hash: str,
    as_of: int,
    hand_authored: bool = False,
    target_commit_time: int | None = None,
    occurrence_resolver: OccurrenceResolver | None = None,
) -> PerformedActionAdmission | PerformedActionHold:
    """Admit one performed action from a genuine owner receipt."""
    if hand_authored:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.HAND_AUTHORED_ACTION,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_NOT_HAND_AUTHORABLE",
        )
    if owner_receipt is None:
        return _hold(
            AdmissionStatus.HELD,
            AdmissionReason.OWNER_RECEIPT_MISSING,
            expected_actor_id,
            as_of,
            (
                "OWNER_RECEIPT{actuator_ref, act, occurrence_ref, action_time, "
                "actor_id, consumed_state_hash, target_commit_time, hash}"
            ),
        )
    if not isinstance(owner_receipt, Mapping) or not valid(dict(owner_receipt)):
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.RECEIPT_INTEGRITY_FAILURE,
            expected_actor_id,
            as_of,
            "SEALED_OWNER_RECEIPT",
        )
    if owner_receipt.get("actor_id") != expected_actor_id:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACTOR_MISMATCH,
            expected_actor_id,
            as_of,
            "SEALED_OWNER_RECEIPT",
        )
    actuator_ref = owner_receipt.get("actuator_ref")
    if not isinstance(actuator_ref, str) or not actuator_ref.strip():
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACTUATOR_UNBOUND,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_ACTUATOR_REF",
        )
    if actuator_ref == expected_actor_id:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACTUATOR_SELF_BOUND,
            expected_actor_id,
            as_of,
            "INDEPENDENT_ACTUATOR_NOT_FOCAL_ACTOR",
        )
    if not actuator_ref.startswith(TEST_ONLY_ACTUATOR_PREFIX):
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACTUATOR_NOT_INDEPENDENT,
            expected_actor_id,
            as_of,
            "TEST_ONLY_DECLARED_INDEPENDENT_ACTUATOR",
        )
    act = owner_receipt.get("act")
    if not isinstance(act, str) or not act.strip():
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACT_UNBOUND,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_ACT",
        )
    if act != expected_act:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACT_UNBOUND,
            expected_actor_id,
            as_of,
            f"OWNER_RECEIPT_WITH_ACT={expected_act}",
        )
    occurrence_ref = owner_receipt.get("occurrence_ref")
    if not isinstance(occurrence_ref, str) or not occurrence_ref.strip():
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.OCCURRENCE_REF_MISSING,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_OCCURRENCE_REF",
        )
    if occurrence_ref == expected_actor_id:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.OCCURRENCE_NOT_INDEPENDENT,
            expected_actor_id,
            as_of,
            "INDEPENDENT_OCCURRENCE_REF",
        )
    if occurrence_resolver is not None:
        if not occurrence_resolver.resolve_occurrence(
            occurrence_ref=occurrence_ref, actor_id=expected_actor_id, as_of=as_of
        ):
            return _hold(
                AdmissionStatus.REFUSED,
                AdmissionReason.OCCURRENCE_NOT_INDEPENDENT,
                expected_actor_id,
                as_of,
                "RESOLVED_INDEPENDENT_OCCURRENCE",
            )
    elif not occurrence_ref.startswith(TEST_ONLY_OCCURRENCE_PREFIX):
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.OCCURRENCE_NOT_INDEPENDENT,
            expected_actor_id,
            as_of,
            "TEST_ONLY_DECLARED_INDEPENDENT_OCCURRENCE",
        )
    action_time = owner_receipt.get("action_time")
    if not isinstance(action_time, int) or isinstance(action_time, bool):
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.TIME_REVERSED,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_ACTION_TIME",
        )
    if action_time > as_of:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.TIME_REVERSED,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_ACTION_TIME",
        )
    lower_bound = owner_receipt.get("target_commit_time", target_commit_time)
    if not isinstance(lower_bound, int) or isinstance(lower_bound, bool):
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.TARGET_COMMIT_TIME_UNBOUND,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_TARGET_COMMIT_TIME",
        )
    if action_time < lower_bound:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.ACTION_BEFORE_TARGET_COMMIT,
            expected_actor_id,
            as_of,
            "ACTION_TIME_AFTER_TARGET_COMMIT",
        )
    receipt_consumed = owner_receipt.get("consumed_state_hash")
    if not isinstance(receipt_consumed, str) or not receipt_consumed:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.NO_CONSUMED_TARGET_STATE,
            expected_actor_id,
            as_of,
            "OWNER_RECEIPT_WITH_CONSUMED_STATE_HASH",
        )
    if not consumed_state_hash or receipt_consumed != consumed_state_hash:
        return _hold(
            AdmissionStatus.REFUSED,
            AdmissionReason.CONSUMED_STATE_MISMATCH,
            expected_actor_id,
            as_of,
            "CONSUMED_STATE_HASH_MUST_MATCH_RECEIPT",
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
        target_commit_time=lower_bound,
    )


def make_performed_action_receipt(
    *,
    actor_id: str,
    act: str,
    actuator_ref: str,
    occurrence_ref: str,
    action_time: int,
    consumed_state_hash: str,
    target_commit_time: int | None = None,
) -> dict:
    """Build one sealed performed-action owner receipt for candidate transport."""
    body = {
        "schema": ACTION_ADMISSION_SCHEMA,
        "actor_id": actor_id,
        "act": act,
        "actuator_ref": actuator_ref,
        "occurrence_ref": occurrence_ref,
        "action_time": action_time,
        "consumed_state_hash": consumed_state_hash,
    }
    if target_commit_time is not None:
        body["target_commit_time"] = target_commit_time
    return seal(body)


__all__ = [
    "ACTION_ADMISSION_SCHEMA",
    "AdmissionReason",
    "AdmissionStatus",
    "OccurrenceResolver",
    "PerformedActionAdmission",
    "PerformedActionHold",
    "TEST_ONLY_ACTUATOR_PREFIX",
    "TEST_ONLY_OCCURRENCE_PREFIX",
    "admit_performed_action",
    "make_performed_action_receipt",
]
