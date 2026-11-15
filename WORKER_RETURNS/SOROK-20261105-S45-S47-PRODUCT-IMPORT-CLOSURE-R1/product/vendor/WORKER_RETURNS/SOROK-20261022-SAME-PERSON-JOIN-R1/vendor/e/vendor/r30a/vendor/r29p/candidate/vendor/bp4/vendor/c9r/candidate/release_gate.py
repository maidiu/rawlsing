"""T2 owner-release gate for the C9P/C9R native candidate tranche.

C9R hardening: raw caller booleans never clear a hold. A hold can be cleared only
by an exact typed `IssuedAuthorityEvidence` that a separately supplied
`AuthorityVerifier` authenticates. No verifier or sourcefree fixture can issue
native authority; the gate therefore stays `C9_NATIVE_POSITIVE_HELD` in every
sourcefree run and the seven finite owner HOLD forms are preserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .canon import digest, seal


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
class IssuedAuthorityEvidence:
    """Exact typed evidence presented for one release surface."""

    surface: str
    issuer_ref: str
    authority_ref: str
    authority_version: str
    body_hash: str
    effective_at: int
    grade: str = "UNVERIFIED_SOURCEFREE_EVIDENCE"

    def body(self) -> dict:
        return {
            "schema": "C9R_ISSUED_AUTHORITY_EVIDENCE@1",
            "surface": self.surface,
            "issuer_ref": self.issuer_ref,
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "body_hash": self.body_hash,
            "effective_at": self.effective_at,
            "grade": self.grade,
        }


@runtime_checkable
class AuthorityVerifier(Protocol):
    """Independently owned verifier of exact issued authority evidence."""

    def verify(self, evidence: IssuedAuthorityEvidence) -> bool:
        ...


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
    caller_supplied_booleans_ignored: tuple[str, ...] = ()
    evidence_authenticated: tuple[str, ...] = ()

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
        evidence_needed="owner receipt with actuator_ref, act, occurrence_ref, action_time, target_commit_time",
    ),
    OwnerHoldForm(
        hold_code=HoldCode.LATER_ACTION_CONSUMER_UNBOUND,
        required_owner="native later-action consumer owner",
        required_decision="bind the exact downstream reader of committed target state",
        evidence_needed="registered consumer module/function with a verified committed-state read",
    ),
)

_SURFACES = (
    "CAN008_RULE_A_ISSUER",
    "CAN011_RULE_T_TARGET_GRANT",
    "ADP019_EVENT_WITNESS",
    "ADP010_ENCOUNTER_WITNESS",
    "PSEPF_POSITIVE_TRANSITION_REGISTRY",
    "PERFORMED_ACTION_OWNER",
    "LATER_ACTION_CONSUMER",
)


def _authenticated(
    evidence: IssuedAuthorityEvidence | None,
    verifier: AuthorityVerifier | None,
    surface: str,
) -> bool:
    if evidence is None or verifier is None:
        return False
    if not isinstance(evidence, IssuedAuthorityEvidence):
        return False
    if evidence.surface != surface:
        return False
    if not all(
        isinstance(value, str) and value.strip()
        for value in (evidence.issuer_ref, evidence.authority_ref, evidence.body_hash)
    ):
        return False
    return bool(verifier.verify(evidence))


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
    authority_verifier: AuthorityVerifier | None = None,
    rule_a_evidence: IssuedAuthorityEvidence | None = None,
    rule_t_evidence: IssuedAuthorityEvidence | None = None,
    adp019_evidence: IssuedAuthorityEvidence | None = None,
    adp010_evidence: IssuedAuthorityEvidence | None = None,
    positive_registry_evidence: IssuedAuthorityEvidence | None = None,
    performed_action_evidence: IssuedAuthorityEvidence | None = None,
    later_action_consumer_evidence: IssuedAuthorityEvidence | None = None,
) -> ReleaseGateResult:
    """Evaluate the owner-release gate over independently verified surfaces.

    Raw booleans and fixture mappings are recorded but never clear a hold.
    """
    ignored: list[str] = []
    for name, value in (
        ("rule_a_issuer_verified", rule_a_issuer_verified),
        ("rule_t_issuer_verified", rule_t_issuer_verified),
        ("adp019_witness_present", adp019_witness_present),
        ("adp010_witness_present", adp010_witness_present),
        ("performed_action_owner_proved", performed_action_owner_proved),
        ("later_action_consumer_bound", later_action_consumer_bound),
    ):
        if value:
            ignored.append(name)
    if isinstance(positive_registry_entries, int) and positive_registry_entries > 0:
        ignored.append("positive_registry_entries")
    if fixture_supplied_authority is not None:
        ignored.append("fixture_supplied_authority")
    cleared: list[str] = []
    surface_checks = (
        ("CAN008_RULE_A_ISSUER", rule_a_evidence),
        ("CAN011_RULE_T_TARGET_GRANT", rule_t_evidence),
        ("ADP019_EVENT_WITNESS", adp019_evidence),
        ("ADP010_ENCOUNTER_WITNESS", adp010_evidence),
        ("PSEPF_POSITIVE_TRANSITION_REGISTRY", positive_registry_evidence),
        ("PERFORMED_ACTION_OWNER", performed_action_evidence),
        ("LATER_ACTION_CONSUMER", later_action_consumer_evidence),
    )
    verified: dict[str, bool] = {}
    for surface, evidence in surface_checks:
        ok = _authenticated(evidence, authority_verifier, surface)
        verified[surface] = ok
        if ok:
            cleared.append(surface)
    holds: list[OwnerHoldForm] = []
    for hold, surface in zip(DEFAULT_HOLDS, _SURFACES):
        if not verified.get(surface, False):
            holds.append(hold)
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
            "cleared": cleared,
            "caller_supplied_booleans_ignored": ignored,
            "fixture_supplied_authority_ignored": fixture_supplied_authority is not None,
        }
    )
    return ReleaseGateResult(
        outcome=outcome,
        holds=tuple(holds),
        checked_surfaces=_SURFACES,
        rule_a_issuer_verified=verified["CAN008_RULE_A_ISSUER"],
        rule_t_issuer_verified=verified["CAN011_RULE_T_TARGET_GRANT"],
        adp019_witness_present=verified["ADP019_EVENT_WITNESS"],
        adp010_witness_present=verified["ADP010_ENCOUNTER_WITNESS"],
        positive_registry_entries=1 if verified["PSEPF_POSITIVE_TRANSITION_REGISTRY"] else 0,
        gate_receipt_hash=receipt["hash"],
        caller_supplied_booleans_ignored=tuple(ignored),
        evidence_authenticated=tuple(cleared),
    )


__all__ = [
    "DEFAULT_HOLDS",
    "AuthorityVerifier",
    "HoldCode",
    "IssuedAuthorityEvidence",
    "OwnerHoldForm",
    "ReleaseGateResult",
    "ReleaseOutcome",
    "evaluate_release_gate",
]
