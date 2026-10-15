"""Sourcefree custody protocol: typed roles, separation, mock signatures, escrow, leakage detection.

All signatures use ephemeral TEST_ONLY fixture credentials with a transparent
verification root. A mock signer does NOT create real independent custody.
Hash equality is NOT independent semantic agreement.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple


class Role(str, Enum):
    SCENARIO_AUTHOR = "SCENARIO_AUTHOR"
    SEMANTIC_ADJUDICATOR = "SEMANTIC_ADJUDICATOR"
    CUSTODIAN = "CUSTODIAN"
    EXPERIMENT_RUNNER = "EXPERIMENT_RUNNER"
    BLIND_CODER = "BLIND_CODER"
    GRANT_ISSUER = "GRANT_ISSUER"
    ACCEPTANCE_REVIEWER = "ACCEPTANCE_REVIEWER"


class ConflictError(Exception):
    pass


class SignatureError(Exception):
    pass


class LeakageError(Exception):
    pass


class RevocationError(Exception):
    pass


class EditAfterFreezeError(Exception):
    pass


class IdentityMismatchError(Exception):
    pass


class PurposeViolationError(Exception):
    pass


class LedgerRollbackError(Exception):
    pass


class DuplicateFamilyError(Exception):
    pass


class BlindIDPairingError(Exception):
    pass


# Conflict graph: no person may hold two roles that conflict
CONFLICT_PAIRS: FrozenSet[Tuple[Role, Role]] = frozenset({
    (Role.SCENARIO_AUTHOR, Role.CUSTODIAN),
    (Role.SCENARIO_AUTHOR, Role.EXPERIMENT_RUNNER),
    (Role.SCENARIO_AUTHOR, Role.BLIND_CODER),
    (Role.CUSTODIAN, Role.EXPERIMENT_RUNNER),
    (Role.CUSTODIAN, Role.BLIND_CODER),
    (Role.EXPERIMENT_RUNNER, Role.BLIND_CODER),
    (Role.GRANT_ISSUER, Role.EXPERIMENT_RUNNER),
    (Role.GRANT_ISSUER, Role.CUSTODIAN),
    (Role.SEMANTIC_ADJUDICATOR, Role.SCENARIO_AUTHOR),
})


def roles_conflict(r1: Role, r2: Role) -> bool:
    return (r1, r2) in CONFLICT_PAIRS or (r2, r1) in CONFLICT_PAIRS


@dataclass(frozen=True)
class Person:
    person_id: str
    roles: FrozenSet[Role]


@dataclass(frozen=True)
class RoleAssignment:
    person_id: str
    role: Role
    assigned_by: str
    assigned_at: float


@dataclass(frozen=True)
class MockSignature:
    signer_person_id: str
    role: Role
    content_digest: str
    context_id: str
    nonce: str
    signature_hash: str
    test_only: bool = True
    verification_root: str = "TEST_ONLY_EPHEMERAL_ROOT"


class MockSigner:
    """Ephemeral fixture signer. Not a real organizational custodian."""

    def __init__(self, person_id: str, role: Role):
        self.person_id = person_id
        self.role = role
        self._secret = hashlib.sha256(
            f"{person_id}:{role.value}:EPHEMERAL_FIXTURE".encode()
        ).hexdigest()

    def sign(self, content_digest: str, context_id: str, nonce: str) -> MockSignature:
        sig_hash = hashlib.sha256(
            f"{self._secret}:{content_digest}:{context_id}:{nonce}".encode()
        ).hexdigest()
        return MockSignature(
            signer_person_id=self.person_id,
            role=self.role,
            content_digest=content_digest,
            context_id=context_id,
            nonce=nonce,
            signature_hash=sig_hash,
            test_only=True,
        )

    @staticmethod
    def verify(sig: MockSignature, content_digest: str, context_id: str, nonce: str) -> bool:
        if not sig.test_only:
            return False
        signer = MockSigner(sig.signer_person_id, sig.role)
        expected = signer.sign(content_digest, context_id, nonce)
        return expected.signature_hash == sig.signature_hash


@dataclass(frozen=True)
class CustodyCapsule:
    capsule_id: str
    schema_version: str
    purpose: str
    scenario_frame: str
    family_graph_digest: str
    content_digest: str
    contribution_digest: str
    public_projection_digest: str
    hidden_projection_digest: str
    lawful_set_digest: str
    coder_rubric_digest: str
    split_assignment_digest: str
    generation_history_digest: str
    rejected_alternatives_digest: str
    freeze_timestamp: float
    version: int = 1
    expired: bool = False
    revoked: bool = False


@dataclass(frozen=True)
class ScenarioCase:
    case_id: str
    family_id: str
    blind_id: str
    k_label: str
    facts_digest: str
    lawful_answers: Tuple[str, ...]
    other_unscorable: bool = True
    hidden_origin_digest: Optional[str] = None
    public_projection_digest: Optional[str] = None


@dataclass
class EscrowState:
    """Tracks committed, unblinded and released state for holdout capsules."""

    committed: Dict[str, CustodyCapsule] = field(default_factory=dict)
    unblinded: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    released: Set[str] = field(default_factory=set)
    exposure_log: List[Dict[str, Any]] = field(default_factory=list)
    ledger: List[Dict[str, Any]] = field(default_factory=list)
    _ledger_seq: int = 0

    def _append_ledger(self, entry: Dict[str, Any]) -> None:
        self._ledger_seq += 1
        entry["seq"] = self._ledger_seq
        entry["ts"] = time.time()
        self.ledger.append(entry)

    def commit(self, capsule: CustodyCapsule) -> None:
        if capsule.capsule_id in self.committed:
            raise EditAfterFreezeError(f"capsule already committed: {capsule.capsule_id}")
        self.committed[capsule.capsule_id] = capsule
        self._append_ledger({"op": "COMMIT", "capsule_id": capsule.capsule_id})

    def unblind(self, capsule_id: str, holder_person_id: str) -> Dict[str, Any]:
        if capsule_id not in self.committed:
            raise IdentityMismatchError(f"uncommitted capsule: {capsule_id}")
        if capsule_id in self.unblinded:
            raise EditAfterFreezeError(f"already unblinded: {capsule_id}")
        payload = {"capsule_id": capsule_id, "holder": holder_person_id,
                    "unblinded_at": time.time()}
        self.unblinded[capsule_id] = payload
        self._append_ledger({"op": "UNBLIND", "capsule_id": capsule_id, "holder": holder_person_id})
        return payload

    def release(self, capsule_id: str) -> None:
        if capsule_id not in self.unblinded:
            raise IdentityMismatchError(f"cannot release without unblinding: {capsule_id}")
        if capsule_id in self.released:
            raise EditAfterFreezeError(f"already released: {capsule_id}")
        self.released.add(capsule_id)
        self._append_ledger({"op": "RELEASE", "capsule_id": capsule_id})

    def record_exposure(self, capsule_id: str, exposed_to: str, purpose: str) -> None:
        self.exposure_log.append({
            "capsule_id": capsule_id, "exposed_to": exposed_to,
            "purpose": purpose, "ts": time.time(),
        })
        self._append_ledger({"op": "EXPOSURE", "capsule_id": capsule_id, "exposed_to": exposed_to})

    def rollback_ledger(self, seq: int) -> None:
        if seq < 1 or seq > self._ledger_seq:
            raise LedgerRollbackError(f"invalid rollback target: {seq}")
        self.ledger = [e for e in self.ledger if e["seq"] <= seq]
        self._ledger_seq = seq

    def verify_ledger_integrity(self) -> bool:
        seqs = [e["seq"] for e in self.ledger]
        return seqs == list(range(1, len(seqs) + 1))


# ---- leakage detection ----

LEAK_TOKENS = frozenset({
    "answer_key", "lawful_answers", "hidden_origin", "oracle_digest",
    "expected_result", "arm_label", "contrast_label", "k_label",
    "case_id", "family_id", "blind_id", "expected_answer", "arm",
    "contrast", "provider", "desired_result", "expected",
})


def detect_leakage(packet: Mapping[str, Any]) -> List[str]:
    """Return list of leak token names found in a model-visible packet."""
    leaks = []
    text = json.dumps(packet, default=str).lower()
    for token in LEAK_TOKENS:
        if token.lower() in text:
            leaks.append(token)
    return leaks


def assert_no_leakage(packet: Mapping[str, Any]) -> None:
    leaks = detect_leakage(packet)
    if leaks:
        raise LeakageError(f"leaked tokens in model-visible packet: {leaks}")


# ---- second-signature requirement ----

def require_second_signature(
    capsule: CustodyCapsule,
    primary_sig: MockSignature,
    second_sig: MockSignature,
    content_digest: str,
    context_id: str,
    nonce: str,
) -> bool:
    """Require two distinct persons with non-conflicting roles to sign same content."""
    if primary_sig.signer_person_id == second_sig.signer_person_id:
        raise ConflictError("second signature must be from a different person")
    if roles_conflict(primary_sig.role, second_sig.role):
        raise ConflictError(f"conflicting roles for joint signature: {primary_sig.role} + {second_sig.role}")
    if not MockSigner.verify(primary_sig, content_digest, context_id, nonce):
        raise SignatureError("primary signature invalid")
    if not MockSigner.verify(second_sig, content_digest, context_id, nonce):
        raise SignatureError("second signature invalid")
    return True


# ---- purpose-bound verification ----

ALLOWED_PURPOSES = frozenset({
    "SOURCEFREE_TEST_ONLY",
    "PROSPECTIVE_DESIGN_REVIEW",
    "CUSTODY_READINESS_PROTOCOL",
})


def verify_purpose(purpose: str) -> None:
    if purpose not in ALLOWED_PURPOSES:
        raise PurposeViolationError(f"unauthorized purpose: {purpose}")


# ---- family independence / clone detection ----

def detect_family_clone(
    family_a_facts: Mapping[str, Any],
    family_b_facts: Mapping[str, Any],
    template_signatures: FrozenSet[str],
) -> bool:
    """Return True if family_b is a clone of family_a (same template signature)."""
    sig_a = semantic_fingerprint(family_a_facts)
    sig_b = semantic_fingerprint(family_b_facts)
    return sig_a == sig_b or (sig_a in template_signatures and sig_b in template_signatures)


def semantic_fingerprint(facts: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(facts, sort_keys=True, default=str).encode()).hexdigest()


# ---- blind-ID pairing ----

def verify_blind_pairing(
    trials: List[Dict[str, Any]],
    block_size: int = 3,
) -> bool:
    """Verify each block shares one opaque nonce and contains all arm orders."""
    blocks: Dict[str, Set[str]] = {}
    for t in trials:
        nonce = t.get("public_nonce")
        arm = t.get("arm")
        if nonce is None or arm is None:
            raise BlindIDPairingError("missing nonce or arm in trial")
        blocks.setdefault(nonce, set()).add(arm)
    for nonce, arms in blocks.items():
        if len(arms) != block_size:
            raise BlindIDPairingError(f"block {nonce} has {len(arms)} arms, expected {block_size}")
    return True
