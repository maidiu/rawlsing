"""R2 bounded repaired candidate for OBL058 CAUSAL_USE_PERMISSION.

This module is deliberately lane-local and NONCURRENT_SYNTHETIC only.  It does
not install runtime state, call ADP-010, create project-current permission, or
claim HQ adoption.  R2 repairs provenance, exact-basis binding, receipt-origin,
and fixture-boundary defects found by the independent R1 review.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0"
FIXTURE_CLASS = "NONCURRENT_SYNTHETIC"
DECISION_PERMIT = "PERMIT"
DECISION_DENY = "DENY"
SOURCE_BASIS_KIND = "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION"
NO_MATCHING_BASIS_KIND = "NO_MATCHING_SOURCE_OWNED_CAUSAL_USE_PERMISSION"

_SCOPE_PREFIXES = MappingProxyType({
    "actor_id": "NONCURRENT_SYNTHETIC::actor::",
    "world_id": "NONCURRENT_SYNTHETIC::world::",
    "subject_id": "NONCURRENT_SYNTHETIC::subject::",
    "time_id": "NONCURRENT_SYNTHETIC::time::",
    "transition_id": "NONCURRENT_SYNTHETIC::transition::",
})


class PermissionContractError(ValueError):
    """Fail-closed contract violation."""


@dataclass(frozen=True)
class ExactScope:
    actor_id: str
    world_id: str
    subject_id: str
    time_id: str
    transition_id: str

    def validate(self) -> None:
        for name, value in asdict(self).items():
            prefix = _SCOPE_PREFIXES[name]
            if not isinstance(value, str) or not value.startswith(prefix):
                raise PermissionContractError(f"noncurrent_synthetic_scope_required:{name}")
            suffix = value[len(prefix):]
            if not suffix.strip():
                raise PermissionContractError(f"missing_or_invalid_scope:{name}")

    def canonical(self) -> dict[str, str]:
        self.validate()
        return asdict(self)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def scope_digest(scope: ExactScope) -> str:
    return hashlib.sha256(_canonical_json(scope.canonical()).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class _SourceBasisRecord:
    basis_id: str
    scope_digest: str
    basis_kind: str
    decision: str

    def proof_payload(self) -> dict[str, str]:
        return {
            "basis_id": self.basis_id,
            "scope_digest": self.scope_digest,
            "basis_kind": self.basis_kind,
            "decision": self.decision,
        }

    def proof_digest(self) -> str:
        return hashlib.sha256(_canonical_json(self.proof_payload()).encode("utf-8")).hexdigest()


REGISTERED_POSITIVE_SCOPE = ExactScope(
    actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r2-a1",
    world_id="NONCURRENT_SYNTHETIC::world::obl058-r2-w1",
    subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r2-s1",
    time_id="NONCURRENT_SYNTHETIC::time::obl058-r2-t1",
    transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r2-tr1",
)
REGISTERED_POSITIVE_BASIS_ID = "NONCURRENT_SYNTHETIC::basis::obl058-r2-source-owned-permit-001"

_REGISTERED_POSITIVE_RECORD = _SourceBasisRecord(
    basis_id=REGISTERED_POSITIVE_BASIS_ID,
    scope_digest=scope_digest(REGISTERED_POSITIVE_SCOPE),
    basis_kind=SOURCE_BASIS_KIND,
    decision=DECISION_PERMIT,
)
_SOURCE_BASIS_REGISTRY = MappingProxyType({
    REGISTERED_POSITIVE_BASIS_ID: _REGISTERED_POSITIVE_RECORD,
})


def _basis_proof_for_denial(*, basis_id: str, expected_scope_digest: str) -> str:
    payload = {
        "basis_id": basis_id,
        "scope_digest": expected_scope_digest,
        "basis_kind": NO_MATCHING_BASIS_KIND,
        "decision": DECISION_DENY,
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _receipt_integrity_payload(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {k: receipt[k] for k in (
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id",
        "basis_scope_digest", "basis_proof_digest",
    )}


def receipt_digest(receipt: Mapping[str, Any]) -> str:
    """Content-integrity digest only; authority provenance is checked separately."""
    return hashlib.sha256(_canonical_json(_receipt_integrity_payload(receipt)).encode("utf-8")).hexdigest()


def _build_source_authority_receipt_boundary():
    """Return source-owned issue/validation provenance functions.

    The issuance marker and concrete receipt class are closure-local.  Public callers
    may inspect receipt fields, but cannot turn an arbitrary Mapping into a receipt
    recognized as emitted by this bounded source-authority instance.
    """
    issuance_marker = object()

    class IssuedReceipt(Mapping[str, Any]):
        __slots__ = ("_data", "_marker")

        def __init__(self, data: Mapping[str, Any], marker: object) -> None:
            if marker is not issuance_marker:
                raise PermissionContractError("receipt_not_issued_by_source_authority")
            self._data = MappingProxyType(dict(data))
            self._marker = marker

        def __getitem__(self, key: str) -> Any:
            return self._data[key]

        def __iter__(self) -> Iterator[str]:
            return iter(self._data)

        def __len__(self) -> int:
            return len(self._data)

        def _has_source_provenance(self) -> bool:
            return self._marker is issuance_marker

    def wrap(data: Mapping[str, Any]) -> Mapping[str, Any]:
        return IssuedReceipt(data, issuance_marker)

    def has_provenance(receipt: Mapping[str, Any]) -> bool:
        return isinstance(receipt, IssuedReceipt) and receipt._has_source_provenance()

    return wrap, has_provenance


_wrap_source_issued_receipt, _has_source_issued_provenance = _build_source_authority_receipt_boundary()


def issue_noncurrent_synthetic_receipt(
    *,
    scope: ExactScope,
    basis_id: str,
    fixture_class: str = FIXTURE_CLASS,
) -> Mapping[str, Any]:
    """Issue one bounded candidate receipt from source-owned basis state only."""
    scope.validate()
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_id, str) or not basis_id.strip():
        raise PermissionContractError("missing_basis_id")

    sd = scope_digest(scope)
    record = _SOURCE_BASIS_REGISTRY.get(basis_id)
    if record is not None and record.scope_digest == sd:
        decision = record.decision
        basis_kind = record.basis_kind
        basis_scope_digest = record.scope_digest
        basis_proof_digest = record.proof_digest()
    else:
        decision = DECISION_DENY
        basis_kind = NO_MATCHING_BASIS_KIND
        basis_scope_digest = sd
        basis_proof_digest = _basis_proof_for_denial(
            basis_id=basis_id,
            expected_scope_digest=sd,
        )

    body: dict[str, Any] = {
        "authority_id": AUTHORITY_ID,
        "schema_version": SCHEMA_VERSION,
        "fixture_class": FIXTURE_CLASS,
        "scope": scope.canonical(),
        "scope_digest": sd,
        "decision": decision,
        "basis_kind": basis_kind,
        "basis_id": basis_id,
        "basis_scope_digest": basis_scope_digest,
        "basis_proof_digest": basis_proof_digest,
    }
    body["receipt_digest"] = receipt_digest(body)
    return _wrap_source_issued_receipt(body)


def validate_receipt(receipt: Mapping[str, Any], *, expected_scope: ExactScope) -> str:
    """Validate exact scope, source basis, and source-issued provenance; fail closed."""
    expected_scope.validate()
    required = {
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id",
        "basis_scope_digest", "basis_proof_digest", "receipt_digest",
    }
    if not isinstance(receipt, Mapping):
        raise PermissionContractError("malformed_receipt")
    if not _has_source_issued_provenance(receipt):
        raise PermissionContractError("receipt_not_issued_by_source_authority")
    if set(receipt.keys()) != required:
        raise PermissionContractError("malformed_receipt_keys")
    if receipt["authority_id"] != AUTHORITY_ID:
        raise PermissionContractError("wrong_authority")
    if receipt["schema_version"] != SCHEMA_VERSION:
        raise PermissionContractError("wrong_schema")
    if receipt["fixture_class"] != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if receipt["decision"] not in {DECISION_PERMIT, DECISION_DENY}:
        raise PermissionContractError("invalid_decision")
    if not isinstance(receipt["scope"], Mapping):
        raise PermissionContractError("malformed_scope")
    if dict(receipt["scope"]) != expected_scope.canonical():
        raise PermissionContractError("scope_mismatch_or_stale")

    sd = scope_digest(expected_scope)
    if receipt["scope_digest"] != sd:
        raise PermissionContractError("scope_digest_mismatch")
    if receipt["basis_scope_digest"] != sd:
        raise PermissionContractError("basis_scope_mismatch")
    if receipt["receipt_digest"] != receipt_digest(receipt):
        raise PermissionContractError("receipt_integrity_mismatch")
    if not isinstance(receipt["basis_id"], str) or not receipt["basis_id"].strip():
        raise PermissionContractError("missing_basis_id")

    record = _SOURCE_BASIS_REGISTRY.get(receipt["basis_id"])
    if receipt["decision"] == DECISION_PERMIT:
        if record is None:
            raise PermissionContractError("positive_decision_without_registered_source_basis")
        if record.scope_digest != sd:
            raise PermissionContractError("positive_basis_not_bound_to_exact_scope")
        if receipt["basis_kind"] != record.basis_kind or record.basis_kind != SOURCE_BASIS_KIND:
            raise PermissionContractError("positive_decision_without_source_owned_basis")
        if receipt["basis_proof_digest"] != record.proof_digest():
            raise PermissionContractError("source_basis_proof_mismatch")
        if record.decision != DECISION_PERMIT:
            raise PermissionContractError("source_basis_does_not_permit")
    else:
        if record is not None and record.scope_digest == sd and record.decision == DECISION_PERMIT:
            raise PermissionContractError("denial_conflicts_with_registered_source_basis")
        if receipt["basis_kind"] != NO_MATCHING_BASIS_KIND:
            raise PermissionContractError("invalid_denial_basis_kind")
        expected_proof = _basis_proof_for_denial(
            basis_id=receipt["basis_id"],
            expected_scope_digest=sd,
        )
        if receipt["basis_proof_digest"] != expected_proof:
            raise PermissionContractError("denial_basis_proof_mismatch")

    return str(receipt["decision"])
