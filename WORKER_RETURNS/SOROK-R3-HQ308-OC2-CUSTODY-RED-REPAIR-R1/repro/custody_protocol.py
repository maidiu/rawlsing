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



# =============================================================================
# OC2 BOUNDED TEST-ONLY ENFORCEMENT LAYER
# These checks replace OC1's illustrative permissive methods. They do NOT
# provide trusted credentials, external rollback anchors, or real custody.
# =============================================================================
import copy as _copy
import re as _re
import unicodedata as _ud
from dataclasses import asdict as _asdict


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _snapshot(obj):
    return _canonical(_asdict(obj))


_LegacyEscrowState = EscrowState


@dataclass
class EscrowState(_LegacyEscrowState):
    """Local source-free fixture: fail closed on capsule/ledger mutations.

    The explicitly declared 'runner1' mock grant retains OC1's documented
    fixture identity. It is NOT an externally verified role assignment.
    Other holders must receive an explicit local test grant.
    """
    _capsule_seals: Dict[str, str] = field(default_factory=dict, repr=False)
    _event_proofs: List[str] = field(default_factory=list, repr=False)
    holder_roles: Dict[str, Role] = field(default_factory=lambda: {"runner1": Role.CUSTODIAN})

    def authorize_holder(self, person_id: str, role: Role) -> None:
        if not isinstance(person_id, str) or not person_id.strip():
            raise IdentityMismatchError("empty fixture holder")
        if not isinstance(role, Role):
            raise IdentityMismatchError("unrecognized fixture role")
        if role != Role.CUSTODIAN:
            raise ConflictError("only CUSTODIAN may unblind fixture capsule")
        if person_id in self.holder_roles and self.holder_roles[person_id] != role:
            raise ConflictError("conflicting fixture role grant")
        self.holder_roles[person_id] = role

    def _append_ledger(self, entry: Dict[str, Any]) -> None:
        # Record an immutable internal preimage after each append. The anchor is
        # in the same Python process, NOT in an independent protected store.
        super()._append_ledger(entry)
        self._event_proofs.append(_canonical(self.ledger[-1]))

    def _validate_capsule(self, capsule_id: str) -> CustodyCapsule:
        if capsule_id not in self.committed:
            raise IdentityMismatchError(f"uncommitted capsule: {capsule_id}")
        capsule = self.committed[capsule_id]
        if capsule.revoked or capsule.expired:
            raise RevocationError(f"inactive capsule: {capsule_id}")
        verify_purpose(capsule.purpose)
        if self._capsule_seals.get(capsule_id) != _snapshot(capsule):
            raise EditAfterFreezeError(f"capsule changed after freeze: {capsule_id}")
        return capsule

    def commit(self, capsule: CustodyCapsule) -> None:
        if not isinstance(capsule, CustodyCapsule):
            raise IdentityMismatchError("expected a CustodyCapsule")
        verify_purpose(capsule.purpose)
        if capsule.revoked or capsule.expired:
            raise RevocationError("cannot commit an inactive capsule")
        if not isinstance(capsule.capsule_id, str) or not capsule.capsule_id:
            raise IdentityMismatchError("missing capsule ID")
        if capsule.capsule_id in self.committed:
            raise EditAfterFreezeError("capsule already committed")
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("existing ledger corrupted")
        frozen = _copy.deepcopy(capsule)
        self.committed[frozen.capsule_id] = frozen
        self._capsule_seals[frozen.capsule_id] = _snapshot(frozen)
        self._append_ledger({"op": "COMMIT", "capsule_id": frozen.capsule_id})

    def unblind(self, capsule_id: str, holder_person_id: str) -> Dict[str, Any]:
        self._validate_capsule(capsule_id)
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("corrupt ledger before unblind")
        if self.holder_roles.get(holder_person_id) != Role.CUSTODIAN:
            raise IdentityMismatchError("unissued sourcefree holder authorization")
        if capsule_id in self.unblinded:
            raise EditAfterFreezeError("already unblinded")
        payload = {"capsule_id": capsule_id, "holder": holder_person_id,
                   "unblinded_at": time.time()}
        self.unblinded[capsule_id] = _copy.deepcopy(payload)
        self._append_ledger({"op": "UNBLIND", "capsule_id": capsule_id,
                             "holder": holder_person_id})
        return _copy.deepcopy(payload)

    def release(self, capsule_id: str) -> None:
        self._validate_capsule(capsule_id)
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("corrupt ledger before release")
        if capsule_id not in self.unblinded:
            raise IdentityMismatchError("cannot release without unblinding")
        holder = self.unblinded[capsule_id]["holder"]
        if self.holder_roles.get(holder) != Role.CUSTODIAN:
            raise RevocationError("holder grant revoked before release")
        if capsule_id in self.released:
            raise EditAfterFreezeError("already released")
        self.released.add(capsule_id)
        self._append_ledger({"op": "RELEASE", "capsule_id": capsule_id})

    def record_exposure(self, capsule_id: str, exposed_to: str, purpose: str) -> None:
        self._validate_capsule(capsule_id)
        if purpose != "development" and purpose not in ALLOWED_PURPOSES:
            raise PurposeViolationError(f"unauthorized test-only exposure: {purpose}")
        if not isinstance(exposed_to, str) or not exposed_to.strip():
            raise IdentityMismatchError("missing exposure recipient")
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("corrupt ledger before exposure")
        row = {"capsule_id": capsule_id, "exposed_to": exposed_to,
               "purpose": purpose, "ts": time.time()}
        self.exposure_log.append(_copy.deepcopy(row))
        self._append_ledger({"op": "EXPOSURE", "capsule_id": capsule_id,
                             "exposed_to": exposed_to, "purpose": purpose,
                             "exposure_ts": row["ts"]})

    def rollback_ledger(self, seq: int) -> None:
        raise LedgerRollbackError("append-only: rollback requires a separate compensating event")

    def verify_ledger_integrity(self) -> bool:
        if self._ledger_seq != len(self.ledger) or len(self.ledger) != len(self._event_proofs):
            return False
        if any(_canonical(item) != proof for item, proof in zip(self.ledger, self._event_proofs)):
            return False
        if any(row.get("seq") != i for i, row in enumerate(self.ledger, 1)):
            return False
        if set(self.committed) != set(self._capsule_seals):
            return False
        if any(_snapshot(cap) != self._capsule_seals.get(cid) for cid, cap in self.committed.items()):
            return False
        commits, unblinds, releases, exposures = set(), {}, set(), []
        for row in self.ledger:
            cid, op = row.get("capsule_id"), row.get("op")
            if op == "COMMIT":
                if cid in commits:
                    return False
                commits.add(cid)
            elif op == "UNBLIND":
                if cid not in commits or cid in unblinds:
                    return False
                unblinds[cid] = row.get("holder")
            elif op == "RELEASE":
                if cid not in unblinds or cid in releases:
                    return False
                releases.add(cid)
            elif op == "EXPOSURE":
                if cid not in commits:
                    return False
                exposures.append((cid, row.get("exposed_to"), row.get("purpose"), row.get("exposure_ts")))
            else:
                return False
        if commits != set(self.committed) or releases != self.released:
            return False
        if set(unblinds) != set(self.unblinded):
            return False
        if any(self.unblinded[cid].get("holder") != holder for cid, holder in unblinds.items()):
            return False
        actual_exposures = [(e.get("capsule_id"), e.get("exposed_to"), e.get("purpose"), e.get("ts"))
                            for e in self.exposure_log]
        return exposures == actual_exposures


def _strict_mock_verify(sig: MockSignature, content_digest: str, context_id: str, nonce: str) -> bool:
    if not isinstance(sig, MockSignature) or not sig.test_only:
        return False
    if sig.verification_root != "TEST_ONLY_EPHEMERAL_ROOT":
        return False
    if (sig.content_digest, sig.context_id, sig.nonce) != (content_digest, context_id, nonce):
        return False
    try:
        expected = MockSigner(sig.signer_person_id, sig.role).sign(content_digest, context_id, nonce)
        return expected.signature_hash == sig.signature_hash
    except (TypeError, AttributeError, ValueError):
        return False


MockSigner.verify = staticmethod(_strict_mock_verify)


def require_second_signature(
    capsule: CustodyCapsule, primary_sig: MockSignature, second_sig: MockSignature,
    content_digest: str, context_id: str, nonce: str,
) -> bool:
    """Mock signatures bind to the *actual* capsule content digest (not ID)."""
    if primary_sig is None or second_sig is None:
        raise SignatureError("both signatures required")
    if primary_sig.signer_person_id == second_sig.signer_person_id:
        raise ConflictError("two distinct persons required")
    if roles_conflict(primary_sig.role, second_sig.role):
        raise ConflictError("conflicting fixture signer roles")
    if not isinstance(capsule, CustodyCapsule):
        raise SignatureError("real capsule argument required for fixture binding")
    if capsule.revoked or capsule.expired:
        raise RevocationError("inactive capsule cannot be countersigned")
    verify_purpose(capsule.purpose)
    if content_digest != capsule.content_digest:
        raise SignatureError("signature does not bind capsule content")
    if not _strict_mock_verify(primary_sig, content_digest, context_id, nonce):
        raise SignatureError("invalid primary mock signature")
    if not _strict_mock_verify(second_sig, content_digest, context_id, nonce):
        raise SignatureError("invalid secondary mock signature")
    return True


def verify_blind_pairing(trials: List[Dict[str, Any]], block_size: int = 3) -> bool:
    """Exactly A/B/C once per nonce, with coherent optional trial/case joins."""
    if not isinstance(trials, list) or not trials or block_size != 3:
        raise BlindIDPairingError("three-arm nonempty pairing required")
    blocks: Dict[str, List[Dict[str, Any]]] = {}
    trial_ids = set()
    for t in trials:
        if not isinstance(t, dict):
            raise BlindIDPairingError("malformed trial")
        nonce, arm = t.get("public_nonce"), t.get("arm")
        if not isinstance(nonce, str) or not nonce or arm not in {"A", "B", "C"}:
            raise BlindIDPairingError("missing or unknown trial arm/nonce")
        trial_id = t.get("trial_id")
        if trial_id is not None:
            if not isinstance(trial_id, str) or not trial_id or trial_id in trial_ids:
                raise BlindIDPairingError("duplicate or invalid trial ID")
            trial_ids.add(trial_id)
        blocks.setdefault(nonce, []).append(t)
    for nonce, rows in blocks.items():
        if len(rows) != 3 or [r["arm"] for r in rows].count("A") != 1 or \
            [r["arm"] for r in rows].count("B") != 1 or \
            [r["arm"] for r in rows].count("C") != 1:
            raise BlindIDPairingError(f"not exactly A/B/C for nonce {nonce}")
        for join_key in ("case_id", "family_id"):
            values = [r.get(join_key) for r in rows]
            if any(v is not None for v in values) and (
                any(not isinstance(v, str) or not v for v in values) or len(set(values)) != 1
            ):
                raise BlindIDPairingError(f"inconsistent {join_key} under nonce {nonce}")
    return True


_ALLOWED_TOP_KEYS = frozenset({"public_projection", "menu", "request_id", "response", "schema_rubric"})
_ALLOWED_PUBLIC_KEYS = frozenset({"context"})
_LEAK_REGEX = {
    t: _re.compile(r"(?<![a-z0-9])" + _re.escape(t) + r"(?![a-z0-9])", _re.I)
    for t in LEAK_TOKENS
}
_LEAK_REGEX.update({
    "solution": _re.compile(r"(?<![a-z0-9])solution(?![a-z0-9])", _re.I),
    "truth": _re.compile(r"(?<![a-z0-9])truth(?![a-z0-9])", _re.I),
})


def _normalized(s):
    s = _ud.normalize("NFKC", str(s))
    return "".join(c for c in s if _ud.category(c) not in {"Cf", "Cc"}).lower()


def detect_leakage(packet: Mapping[str, Any]) -> List[str]:
    """Narrow allowed fixture projections; no claim of semantic noninterference."""
    if not isinstance(packet, dict):
        return ["invalid_packet_type"]
    found = set()

    def scan(obj, depth=0, public=False):
        if depth > 8:
            found.add("excess_nesting")
            return
        if isinstance(obj, dict):
            allowed = _ALLOWED_PUBLIC_KEYS if public else (_ALLOWED_TOP_KEYS if depth == 0 else frozenset())
            for k, v in obj.items():
                normalized_key = _normalized(k)
                if normalized_key not in allowed:
                    found.add(normalized_key if normalized_key in LEAK_TOKENS else f"unapproved_field:{normalized_key}")
                for name, pattern in _LEAK_REGEX.items():
                    if pattern.search(normalized_key):
                        found.add(name)
                scan(v, depth+1, public=normalized_key == "public_projection")
        elif isinstance(obj, (list, tuple)):
            for val in obj:
                scan(val, depth+1)
        else:
            val = _normalized(obj)
            for name, pattern in _LEAK_REGEX.items():
                if pattern.search(val):
                    found.add(name)

    scan(packet)
    return sorted(found)


def assert_no_leakage(packet: Mapping[str, Any]) -> None:
    issues = detect_leakage(packet)
    if issues:
        raise LeakageError(f"unauthorized test-only projection: {issues}")
