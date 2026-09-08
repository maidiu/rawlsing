"""R3 bounded repaired candidate for OBL058 CAUSAL_USE_PERMISSION.

This module is deliberately lane-local and NONCURRENT_SYNTHETIC only. It does
not install runtime state, call ADP-010, create project-current permission, or
claim HQ adoption. R3 preserves the R2 source-basis/scope/fixture repairs while
replacing caller-reproducible receipt provenance with exact issued-object
identity plus immutable source-owned ledger content.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0"
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
    actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r3-a1",
    world_id="NONCURRENT_SYNTHETIC::world::obl058-r3-w1",
    subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r3-s1",
    time_id="NONCURRENT_SYNTHETIC::time::obl058-r3-t1",
    transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r3-tr1",
)
REGISTERED_POSITIVE_BASIS_ID = "NONCURRENT_SYNTHETIC::basis::obl058-r3-source-owned-permit-001"

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
    """Content-integrity digest only; source origin is established separately."""
    return hashlib.sha256(_canonical_json(_receipt_integrity_payload(receipt)).encode("utf-8")).hexdigest()


def _freeze_receipt_body(body: Mapping[str, Any]) -> Mapping[str, Any]:
    frozen = dict(body)
    scope_value = frozen.get("scope")
    if not isinstance(scope_value, Mapping):
        raise PermissionContractError("malformed_scope")
    frozen["scope"] = MappingProxyType(dict(scope_value))
    return MappingProxyType(frozen)


def _build_source_authority_surface():
    """Build the exact bounded issuer/validator surface.

    Source origin is not represented by a transferable marker or a mutable payload
    stored on the receipt. The closure owns a strong ledger of exact issued object
    identities and the immutable body produced for each identity. Validation uses
    identity (``is``), exact concrete type, and that ledger body; caller-visible
    Mapping behavior is informational only and cannot rewrite validation content.
    """

    issued_ledger: list[tuple[object, Mapping[str, Any]]] = []

    class IssuedReceipt(Mapping[str, Any]):
        __slots__ = ()

        def _ledger_body(self) -> Mapping[str, Any]:
            for issued, body in issued_ledger:
                if self is issued:
                    return body
            raise PermissionContractError("receipt_not_issued_by_source_authority")

        def __getitem__(self, key: str) -> Any:
            value = self._ledger_body()[key]
            if key == "scope":
                return dict(value)
            return value

        def __iter__(self) -> Iterator[str]:
            return iter(self._ledger_body())

        def __len__(self) -> int:
            return len(self._ledger_body())

    def _new_issued_receipt(body: Mapping[str, Any]) -> Mapping[str, Any]:
        receipt = object.__new__(IssuedReceipt)
        issued_ledger.append((receipt, _freeze_receipt_body(body)))
        return receipt

    def _lookup_exact_issued_body(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
        if type(receipt) is not IssuedReceipt:
            raise PermissionContractError("receipt_not_issued_by_source_authority")
        for issued, body in issued_ledger:
            if receipt is issued:
                return body
        raise PermissionContractError("receipt_not_issued_by_source_authority")

    def issue(
        *,
        scope: ExactScope,
        basis_id: str,
        fixture_class: str = FIXTURE_CLASS,
    ) -> Mapping[str, Any]:
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
        return _new_issued_receipt(body)

    def validate(receipt: Mapping[str, Any], *, expected_scope: ExactScope) -> str:
        expected_scope.validate()
        body = _lookup_exact_issued_body(receipt)

        required = {
            "authority_id", "schema_version", "fixture_class", "scope",
            "scope_digest", "decision", "basis_kind", "basis_id",
            "basis_scope_digest", "basis_proof_digest", "receipt_digest",
        }
        if set(body.keys()) != required:
            raise PermissionContractError("malformed_receipt_keys")
        if body["authority_id"] != AUTHORITY_ID:
            raise PermissionContractError("wrong_authority")
        if body["schema_version"] != SCHEMA_VERSION:
            raise PermissionContractError("wrong_schema")
        if body["fixture_class"] != FIXTURE_CLASS:
            raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
        if body["decision"] not in {DECISION_PERMIT, DECISION_DENY}:
            raise PermissionContractError("invalid_decision")
        if not isinstance(body["scope"], Mapping):
            raise PermissionContractError("malformed_scope")
        if dict(body["scope"]) != expected_scope.canonical():
            raise PermissionContractError("scope_mismatch_or_stale")

        sd = scope_digest(expected_scope)
        if body["scope_digest"] != sd:
            raise PermissionContractError("scope_digest_mismatch")
        if body["basis_scope_digest"] != sd:
            raise PermissionContractError("basis_scope_mismatch")

        digest_view = {
            "authority_id": body["authority_id"],
            "schema_version": body["schema_version"],
            "fixture_class": body["fixture_class"],
            "scope": dict(body["scope"]),
            "scope_digest": body["scope_digest"],
            "decision": body["decision"],
            "basis_kind": body["basis_kind"],
            "basis_id": body["basis_id"],
            "basis_scope_digest": body["basis_scope_digest"],
            "basis_proof_digest": body["basis_proof_digest"],
        }
        if body["receipt_digest"] != receipt_digest(digest_view):
            raise PermissionContractError("receipt_integrity_mismatch")
        if not isinstance(body["basis_id"], str) or not body["basis_id"].strip():
            raise PermissionContractError("missing_basis_id")

        record = _SOURCE_BASIS_REGISTRY.get(body["basis_id"])
        if body["decision"] == DECISION_PERMIT:
            if record is None:
                raise PermissionContractError("positive_decision_without_registered_source_basis")
            if record.scope_digest != sd:
                raise PermissionContractError("positive_basis_not_bound_to_exact_scope")
            if body["basis_kind"] != record.basis_kind or record.basis_kind != SOURCE_BASIS_KIND:
                raise PermissionContractError("positive_decision_without_source_owned_basis")
            if body["basis_proof_digest"] != record.proof_digest():
                raise PermissionContractError("source_basis_proof_mismatch")
            if record.decision != DECISION_PERMIT:
                raise PermissionContractError("source_basis_does_not_permit")
        else:
            if record is not None and record.scope_digest == sd and record.decision == DECISION_PERMIT:
                raise PermissionContractError("denial_conflicts_with_registered_source_basis")
            if body["basis_kind"] != NO_MATCHING_BASIS_KIND:
                raise PermissionContractError("invalid_denial_basis_kind")
            expected_proof = _basis_proof_for_denial(
                basis_id=body["basis_id"],
                expected_scope_digest=sd,
            )
            if body["basis_proof_digest"] != expected_proof:
                raise PermissionContractError("denial_basis_proof_mismatch")

        return str(body["decision"])

    return issue, validate


issue_noncurrent_synthetic_receipt, validate_receipt = _build_source_authority_surface()
del _build_source_authority_surface
