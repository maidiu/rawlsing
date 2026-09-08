"""Frozen-candidate implementation for OBL058 CAUSAL_USE_PERMISSION.

This module is deliberately lane-local. It can issue receipts only for
NONCURRENT_SYNTHETIC fixtures. It does not install runtime state, call ADP-010,
or create any project-current positive permission.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Any, Mapping

AUTHORITY_ID = "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0"
SCHEMA_VERSION = "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@1.0.0"
FIXTURE_CLASS = "NONCURRENT_SYNTHETIC"
DECISION_PERMIT = "PERMIT"
DECISION_DENY = "DENY"

FORBIDDEN_SURROGATE_BASIS = frozenset({
    "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
    "ADP010_REALIZATION_AUTHORITY",
    "OCCURRENCE_ADMISSION",
    "ACTOR_WORLD_TIME_PROXIMITY",
    "NARRATIVE_PLAUSIBILITY",
    "DOWNSTREAM_CONSUMPTION",
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
            if not isinstance(value, str) or not value.strip():
                raise PermissionContractError(f"missing_or_invalid_scope:{name}")

    def canonical(self) -> dict[str, str]:
        self.validate()
        return asdict(self)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def scope_digest(scope: ExactScope) -> str:
    return hashlib.sha256(_canonical_json(scope.canonical()).encode("utf-8")).hexdigest()


def _receipt_integrity_payload(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {k: receipt[k] for k in (
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id",
    )}


def receipt_digest(receipt: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(_receipt_integrity_payload(receipt)).encode("utf-8")).hexdigest()


def issue_noncurrent_synthetic_receipt(
    *,
    scope: ExactScope,
    explicit_source_permission: bool,
    basis_kind: str,
    basis_id: str,
    fixture_class: str = FIXTURE_CLASS,
) -> dict[str, Any]:
    """Issue a candidate receipt for a NONCURRENT_SYNTHETIC court fixture only."""
    scope.validate()
    if fixture_class != FIXTURE_CLASS:
        raise PermissionContractError("project_current_or_unknown_fixture_not_authorized")
    if not isinstance(basis_kind, str) or not basis_kind:
        raise PermissionContractError("missing_basis_kind")
    if not isinstance(basis_id, str) or not basis_id:
        raise PermissionContractError("missing_basis_id")

    if basis_kind in FORBIDDEN_SURROGATE_BASIS:
        decision = DECISION_DENY
    elif basis_kind != "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION":
        decision = DECISION_DENY
    else:
        decision = DECISION_PERMIT if explicit_source_permission is True else DECISION_DENY

    receipt: dict[str, Any] = {
        "authority_id": AUTHORITY_ID,
        "schema_version": SCHEMA_VERSION,
        "fixture_class": FIXTURE_CLASS,
        "scope": scope.canonical(),
        "scope_digest": scope_digest(scope),
        "decision": decision,
        "basis_kind": basis_kind,
        "basis_id": basis_id,
    }
    receipt["receipt_digest"] = receipt_digest(receipt)
    return receipt


def validate_receipt(receipt: Mapping[str, Any], *, expected_scope: ExactScope) -> str:
    """Validate a candidate receipt against an exact expected scope; fail closed."""
    expected_scope.validate()
    required = {
        "authority_id", "schema_version", "fixture_class", "scope",
        "scope_digest", "decision", "basis_kind", "basis_id", "receipt_digest",
    }
    if not isinstance(receipt, Mapping):
        raise PermissionContractError("malformed_receipt")
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
    if receipt["scope_digest"] != scope_digest(expected_scope):
        raise PermissionContractError("scope_digest_mismatch")
    if receipt["receipt_digest"] != receipt_digest(receipt):
        raise PermissionContractError("receipt_integrity_mismatch")
    if receipt["decision"] == DECISION_PERMIT:
        if receipt["basis_kind"] != "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION":
            raise PermissionContractError("positive_decision_without_source_owned_basis")
        if receipt["basis_kind"] in FORBIDDEN_SURROGATE_BASIS:
            raise PermissionContractError("surrogate_basis_cannot_permit")
    return str(receipt["decision"])
