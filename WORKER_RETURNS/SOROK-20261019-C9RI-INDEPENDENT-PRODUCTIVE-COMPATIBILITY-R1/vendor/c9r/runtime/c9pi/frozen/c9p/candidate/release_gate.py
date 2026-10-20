"""T2 owner-release gate for the C9P native candidate tranche.

The gate independently checks for a qualified concrete CAN008 `RULE_A` issuer,
a separate CAN011 `RULE_T` target grant, ADP019/ADP010 witnesses and a positive
native transition registry. When any is absent the gate preserves
`C9_NATIVE_POSITIVE_HELD` and emits finite owner HOLD forms. A fixture, a
recomputed digest or a locally granted owner never clears the gate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .canon import seal


class ReleaseOutcome(str, Enum):
    C9_NATIVE_POSITIVE_HELD = "C9_NATIVE_POSITIVE_HELD"
    C9_NATIVE_POSITIVE_AUTHORIZED = "C9_NATIVE_POSITIVE_AUTHORIZED"


class HoldCode(str, Enum):
    CAN008_RULE_ISSUER_UNVERIFIED = "CAN008_RULE_ISSUER_UNVERIFIED"
    CAN011_TARGET_UNISSUED = "CAN011_TARGET_UNISSUED"
    ADP019_ACTOR_EVENT_WITNESS_MISSING = "ADP019_ACTOR_EVENT_WITNESS_MISSING"
    ADP010_ENCOUNTER_WITNESS_MISSING = "ADP010_ENCOUNTER_WITNESS_MISSING"
    POSITIVE_TRANSITION_REGISTRY_EMPTY = "POSITIVE_TRANSITION_REGISTRY_EMPTY"
    PERFORMED_ACTION_OWNER_UNPROVED = "PERFORMED_ACTION_OWNER_UNPROVED"
    LATER_ACTION_CONSUMER_UNBOUND = "LATER_ACTION_CONSUMER_UNBOUND"


@dataclass(frozen=True)
class OwnerHoldForm:
    """One finite owner HOLD naming the exact missing competent issuer decision."""

    hold_code: HoldCode
    required_owner: str
    required_decision: str
    evidence_needed: str


@dataclass(frozen=True)
class ReleaseGateResult:
    """Typed outcome of the T2 owner-release gate."""

    outcome: ReleaseOutcome
    holds: tuple[OwnerHoldForm, ...]
    checked_surfaces: tuple[str, ...]
    rule_a_issuer_verified: bool
    rule_t_issuer_verified: bool
    adp019_witness_present: bool
    adp010_witness_present: bool
    positive_registry_entries: int
    gate_receipt_hash: str

    @property
    def held(self) -> bool:
        return self.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD


DEFAULT_HOLDS: tuple[OwnerHoldForm, ...] = (
    OwnerHoldForm(
        hold_code=HoldCode.CAN008_RULE_ISSUER_UNVERIFIED,
        required_owner="V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE competent concrete rule issuer",
        required_decision=(
            "sign one exact RULE_A body/version/content-hash with allowed subjects, "
            "witnessed enacted history predicates, effective time and current source/use registry"
        ),
        evidence_needed="issuing office evidence, signed adoption record, rule body hash, registry entry",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.CAN011_TARGET_UNISSUED,
        required_owner="V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY separate target-owner authority",
        required_decision=(
            "adopt exact RULE_T body and a conditional V3MS_PRACTICE CREATE/NO_CHANGE/DENY "
            "grant with before/read/write sets, replay, rollback, expiry and revocation law"
        ),
        evidence_needed="separate target-rule adoption record, grant id/scope/expiry, registry snapshot hash",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.ADP019_ACTOR_EVENT_WITNESS_MISSING,
        required_owner="External Admission Court (ADP019)",
        required_decision="admit the exact precipitating occurrence with owner receipt and effective clock",
        evidence_needed="ADP019 admission receipt, immutable event id/hash/time, actor encounter receivability",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.ADP010_ENCOUNTER_WITNESS_MISSING,
        required_owner="ADP010 generated encounter owner",
        required_decision="admit the generated encounter/exposure basis for the actor",
        evidence_needed="ADP010 encounter receipt bound to the actor identity",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.POSITIVE_TRANSITION_REGISTRY_EMPTY,
        required_owner="PSEPF production positive-transition registry binder",
        required_decision=(
            "a separate accepted authority change registering the concrete positive "
            "transition authority outside any test caller"
        ),
        evidence_needed="accepted authority binder/code change with non-empty production registry",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.PERFORMED_ACTION_OWNER_UNPROVED,
        required_owner="later performed-action actuator owner",
        required_decision="admit one genuine performed action with independent occurrence receipt",
        evidence_needed="owner receipt with actuator_ref, act, occurrence_ref, action_time",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.LATER_ACTION_CONSUMER_UNBOUND,
        required_owner="native later-action consumer owner",
        required_decision="bind the exact downstream reader of committed target state",
        evidence_needed="registered consumer module/function with a verified committed-state read",
    ),
)


def evaluate_release_gate(
    *,
    rule_a_issuer_verified: bool = False,
    rule_t_issuer_verified: bool = False,
    adp019_witness_present: bool = False,
    adp010_witness_present: bool = False,
    positive_registry_entries: int = 0,
    performed_action_owner_proved: bool = False,
    later_action_consumer_bound: bool = False,
    fixture_supplied_authority: Mapping[str, Any] | None = None,
) -> ReleaseGateResult:
    """Evaluate the owner-release gate over independently checked surfaces.

    Any `fixture_supplied_authority` is recorded but never clears a hold: a
    fixture's `CURRENT_ACCEPTED`, a recomputed digest or a locally granted owner
    is not competent issuance. The gate stays HELD until every surface is backed
    by an independently authenticated competent issuer.
    """
    holds: list[OwnerHoldForm] = []
    if not rule_a_issuer_verified:
        holds.append(DEFAULT_HOLDS[0])
    if not rule_t_issuer_verified:
        holds.append(DEFAULT_HOLDS[1])
    if not adp019_witness_present:
        holds.append(DEFAULT_HOLDS[2])
    if not adp010_witness_present:
        holds.append(DEFAULT_HOLDS[3])
    if positive_registry_entries <= 0:
        holds.append(DEFAULT_HOLDS[4])
    if not performed_action_owner_proved:
        holds.append(DEFAULT_HOLDS[5])
    if not later_action_consumer_bound:
        holds.append(DEFAULT_HOLDS[6])
    checked = (
        "CAN008_RULE_A_ISSUER",
        "CAN011_RULE_T_TARGET_GRANT",
        "ADP019_EVENT_WITNESS",
        "ADP010_ENCOUNTER_WITNESS",
        "PSEPF_POSITIVE_TRANSITION_REGISTRY",
        "PERFORMED_ACTION_OWNER",
        "LATER_ACTION_CONSUMER",
    )
    outcome = (
        ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
        if holds
        else ReleaseOutcome.C9_NATIVE_POSITIVE_AUTHORIZED
    )
    receipt = seal(
        {
            "schema": "C9P_RELEASE_GATE@1",
            "outcome": outcome.value,
            "holds": [hold.hold_code.value for hold in holds],
            "fixture_supplied_authority_ignored": fixture_supplied_authority is not None,
        }
    )
    return ReleaseGateResult(
        outcome=outcome,
        holds=tuple(holds),
        checked_surfaces=checked,
        rule_a_issuer_verified=rule_a_issuer_verified,
        rule_t_issuer_verified=rule_t_issuer_verified,
        adp019_witness_present=adp019_witness_present,
        adp010_witness_present=adp010_witness_present,
        positive_registry_entries=positive_registry_entries,
        gate_receipt_hash=receipt["hash"],
    )


__all__ = [
    "DEFAULT_HOLDS",
    "HoldCode",
    "OwnerHoldForm",
    "ReleaseGateResult",
    "ReleaseOutcome",
    "evaluate_release_gate",
]
