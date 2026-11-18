#!/usr/bin/env python3
"""Reusable existing-grant to R157 source-read binding.

This is construction/source-*read* preparation only.  It does not issue a
source right, CURRENT decision, scientific eligibility, or I03/I05 authority.

The grant document is static evidence.  Its hash does NOT establish CURRENT.
A deployment must supply an independently trusted current-evidence verifier
(public key plus issuer identity) and a signed current record.  This module
constructs the exact R157 SourceReadRequest, verifies the static grant bytes
against externally supplied trust, verifies the signed current record against
that same external trust, and only then returns an IssuedSourceReadDecision.
No source path is opened, stat'ed, hashed, or decoded here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_r157_projection_adapter import (
    CURRENT_GRANTED,
    EXACT_FILE,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
    SourceReadRequest,
)

SCHEMA = "ANVIL_EXISTING_GRANT_TO_C11_BINDING@1"
SRC04_GRANT_SCHEMA = "PYAT_FULL_SOURCE_READ_GRANT@1.0.0"
SRC04_SCOPE = "ALL_181_PHYSICAL_SLOTS__ALL_QUALIFIED_RESPONSE_FIELDS"
SRC04_PURPOSE = "FULL_SRC04_ORIGINAL_C11_CONSTRUCTION"
SRC04_CONSUMER = "EXISTING_PRE553_SOURCE_BACKED_C11"
SRC04_SEMANTIC_SCOPE = (
    "SOURCE_NATIVE_RESPONSE_INCIDENCE",
    "NO_SEMANTIC_ADOPTION",
    "SRC04",
    "FULL_SRC04_C11_CONSTRUCTION",
)


class BindingRefusal(ValueError):
    """A static grant, config, request, or current record failed closed."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (f": {detail}" if detail else ""))
        self.code = code
        self.detail = detail


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _ref(value: Mapping[str, Any] | ExactRef, name: str) -> ExactRef:
    try:
        if isinstance(value, ExactRef):
            return value
        if not isinstance(value, Mapping):
            raise TypeError
        ref = ExactRef(str(value["kind"]), str(value["object_id"]),
                       str(value["content_hash"]))
        return ref
    except Exception as exc:
        raise BindingRefusal("BINDING_REF_INVALID", name) from exc


def _ref_dict(ref: ExactRef) -> dict[str, str]:
    return ref.as_dict()


def _refs(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise BindingRefusal("BINDING_REFS_REQUIRED", name)
    refs = tuple(sorted((_ref(v, name) for v in value), key=lambda r: r.key))
    if not refs:
        raise BindingRefusal("BINDING_REFS_REQUIRED", name)
    return refs


@dataclass(frozen=True)
class ConfigBinding:
    """Exact R157 config metadata, without copying or reading source bytes.

    ``config_path`` and the hashes identify the frozen config blob; this class
    does not parse the full config.  The request fields below are the exact
    R157 identity/locator/metadata witness fields needed for admission.
    """

    source_id: str
    source_sha256: str
    source_format: str
    locator_id: str
    metadata_freeze_refs: tuple[ExactRef, ...]
    config_commit: str
    config_path: str
    config_file_sha256: str
    config_canonical_sha256: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata_freeze_refs", _refs(
            list(self.metadata_freeze_refs), "metadata_freeze_refs"))

    def binding_sha256(self) -> str:
        return _sha256(_canonical({
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "source_format": self.source_format,
            "locator_id": self.locator_id,
            "metadata_freeze_refs": [_ref_dict(r) for r in self.metadata_freeze_refs],
            "config_commit": self.config_commit,
            "config_path": self.config_path,
            "config_file_sha256": self.config_file_sha256,
            "config_canonical_sha256": self.config_canonical_sha256,
        }))

    def validate(self, trust: "ExternalTrust") -> None:
        if self.source_id != "SRC04":
            raise BindingRefusal("CONFIG_SOURCE_NOT_SRC04", self.source_id)
        if self.source_sha256 != "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18":
            raise BindingRefusal("CONFIG_SOURCE_SHA_MISMATCH")
        if self.source_format != "SAV":
            raise BindingRefusal("CONFIG_SOURCE_FORMAT_MISMATCH")
        if not self.locator_id:
            raise BindingRefusal("CONFIG_LOCATOR_REQUIRED")
        if (self.config_file_sha256 != trust.config_file_sha256
                or self.config_canonical_sha256 != trust.config_canonical_sha256
                or self.binding_sha256() != trust.config_binding_sha256):
            raise BindingRefusal("CONFIG_TRUST_MISMATCH")
        if self.config_commit != "da23c65d1e211cb7e8ce416e98757f321b78d25e":
            raise BindingRefusal("CONFIG_COMMIT_MISMATCH")
        if self.config_path != "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json":
            raise BindingRefusal("CONFIG_PATH_MISMATCH")


@dataclass(frozen=True)
class ExternalTrust:
    """Deployment-supplied trust anchors, not a caller authority claim."""

    grant_sha256: str
    config_file_sha256: str
    config_canonical_sha256: str
    config_binding_sha256: str
    current_issuer: str
    current_public_key_hex: str
    current_evidence_sha256: str | None = None

    def validate(self) -> None:
        for value, name in (
            (self.grant_sha256, "grant_sha256"),
            (self.config_file_sha256, "config_file_sha256"),
            (self.config_canonical_sha256, "config_canonical_sha256"),
            (self.config_binding_sha256, "config_binding_sha256"),
            (self.current_public_key_hex, "current_public_key_hex"),
        ):
            if not isinstance(value, str) or len(value) != 64 or value.lower() != value:
                raise BindingRefusal("TRUST_SHA_REQUIRED", name)
        if self.current_evidence_sha256 is not None:
            if (not isinstance(self.current_evidence_sha256, str)
                    or len(self.current_evidence_sha256) != 64
                    or self.current_evidence_sha256.lower() != self.current_evidence_sha256):
                raise BindingRefusal("TRUST_EVIDENCE_SHA_REQUIRED")
        if not isinstance(self.current_issuer, str) or not self.current_issuer.strip():
            raise BindingRefusal("TRUST_CURRENT_ISSUER_REQUIRED")


@dataclass(frozen=True)
class BindingResult:
    status: str
    request: SourceReadRequest
    decision: IssuedSourceReadDecision | None
    grant_sha256: str
    grant_ref: ExactRef
    request_digest: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "status": self.status,
            "grant_sha256": self.grant_sha256,
            "grant_ref": self.grant_ref.as_dict(),
            "request": _request_payload(self.request),
            "request_digest": self.request_digest,
            "decision_ref": None if self.decision is None else self.decision.decision_ref.as_dict(),
            "effective_interval": None if self.decision is None else self.decision.effective_interval,
            "currentness": None if self.decision is None else self.decision.currentness,
            "revocation_ref": None if self.decision is None or self.decision.revocation_ref is None
                              else self.decision.revocation_ref.as_dict(),
            "reason": self.reason,
            "source_read_performed": False,
            "self_issued_authority": False,
        }


def _request_payload(request: SourceReadRequest) -> dict[str, Any]:
    return {
        "source_id": request.source_id,
        "source_sha256": request.source_sha256,
        "source_format": request.source_format,
        "custody_locator_binding": request.custody_locator_binding,
        "host": request.host,
        "purpose": request.purpose,
        "consumer_use": request.consumer_use,
        "read_operation": request.read_operation,
        "physical_read_extent": request.physical_read_extent,
        "metadata_freeze_refs": [_ref_dict(r) for r in request.metadata_freeze_refs],
        "semantic_use_scope": list(request.semantic_use_scope),
    }


def _request_digest(request: SourceReadRequest) -> str:
    return _sha256(_canonical(_request_payload(request)))


def _load_grant(grant_path: str | Path, trust: ExternalTrust) -> tuple[dict[str, Any], str, ExactRef]:
    path = Path(grant_path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise BindingRefusal("GRANT_BYTES_UNAVAILABLE", str(path)) from exc
    actual = _sha256(raw)
    if actual != trust.grant_sha256:
        raise BindingRefusal("GRANT_TRUST_HASH_MISMATCH", actual)
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BindingRefusal("GRANT_JSON_INVALID") from exc
    if not isinstance(document, dict):
        raise BindingRefusal("GRANT_DOCUMENT_REQUIRED")
    if document.get("schema") != SRC04_GRANT_SCHEMA:
        raise BindingRefusal("GRANT_SCHEMA_MISMATCH", str(document.get("schema")))
    if document.get("source_id") != "SRC04":
        raise BindingRefusal("GRANT_SOURCE_MISMATCH", str(document.get("source_id")))
    if document.get("expected_source_sha256") != "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18":
        raise BindingRefusal("GRANT_SOURCE_SHA_MISMATCH")
    if document.get("host") != "USER_LOCAL_MAC":
        raise BindingRefusal("GRANT_HOST_MISMATCH")
    if document.get("purpose") != SRC04_PURPOSE:
        raise BindingRefusal("GRANT_PURPOSE_MISMATCH")
    if document.get("consumer") != SRC04_CONSUMER:
        raise BindingRefusal("GRANT_CONSUMER_MISMATCH")
    if document.get("full_source") is not True or document.get("first_slice_only") is not False:
        raise BindingRefusal("GRANT_FULL_SOURCE_REQUIRED")
    if document.get("scope") != SRC04_SCOPE:
        raise BindingRefusal("GRANT_SCOPE_MISMATCH")
    if document.get("currentness") != CURRENT_GRANTED:
        raise BindingRefusal("GRANT_STATIC_CURRENTNESS_NOT_CURRENT")
    if document.get("revocation") not in (None, "NONE_RECORDED"):
        raise BindingRefusal("GRANT_STATIC_REVOKED")
    if not isinstance(document.get("authorization"), str) or not document["authorization"].strip():
        raise BindingRefusal("GRANT_AUTHORIZATION_REQUIRED")
    if not isinstance(document.get("source_path"), str) or not document["source_path"].strip():
        raise BindingRefusal("GRANT_SOURCE_PATH_REQUIRED")
    grant_ref = ExactRef("FULL_SOURCE_READ_GRANT",
                         f"urn:rawlsing:full-source-grant:SRC04:{actual}", actual)
    return document, actual, grant_ref


def make_request(grant: Mapping[str, Any], config: ConfigBinding) -> SourceReadRequest:
    """Build the exact request; metadata config comes from the frozen config."""
    if grant.get("source_id") != config.source_id:
        raise BindingRefusal("GRANT_CONFIG_SOURCE_MISMATCH")
    if grant.get("expected_source_sha256") != config.source_sha256:
        raise BindingRefusal("GRANT_CONFIG_SOURCE_SHA_MISMATCH")
    if grant.get("host") != "USER_LOCAL_MAC":
        raise BindingRefusal("GRANT_HOST_MISMATCH")
    return SourceReadRequest(
        source_id=config.source_id,
        source_sha256=config.source_sha256,
        source_format=config.source_format,
        custody_locator_binding=config.locator_id,
        host=grant["host"],
        purpose=grant["purpose"],
        consumer_use=grant["consumer"],
        read_operation=SOURCE_RESPONSE_DECODE,
        physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=config.metadata_freeze_refs,
        semantic_use_scope=SRC04_SEMANTIC_SCOPE,
    )


def _expected_decision_ref(request: SourceReadRequest, grant_ref: ExactRef) -> ExactRef:
    return ExactRef(
        "USER_SOURCE_READ_DECISION",
        f"urn:rawlsing:existing-grant:SRC04:{grant_ref.content_hash}",
        semantic_hash({
            "schema": SCHEMA,
            "grant_ref": grant_ref.as_dict(),
            "request_digest": _request_digest(request),
            "source_id": request.source_id,
            "source_sha256": request.source_sha256,
            "host": request.host,
            "purpose": request.purpose,
            "consumer_use": request.consumer_use,
            "read_operation": request.read_operation,
            "physical_read_extent": request.physical_read_extent,
        }),
    )


def _verify_current_evidence(
    *,
    request: SourceReadRequest,
    grant_ref: ExactRef,
    trust: ExternalTrust,
    current_evidence_path: str | Path,
) -> IssuedSourceReadDecision:
    path = Path(current_evidence_path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise BindingRefusal("CURRENT_EVIDENCE_UNAVAILABLE") from exc
    if trust.current_evidence_sha256 is not None and _sha256(raw) != trust.current_evidence_sha256:
        raise BindingRefusal("CURRENT_EVIDENCE_TRUST_HASH_MISMATCH")
    try:
        envelope = json.loads(raw.decode("utf-8"))
        payload = envelope["payload"]
        signature = bytes.fromhex(envelope["signature"])
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise BindingRefusal("CURRENT_EVIDENCE_MALFORMED") from exc
    if not isinstance(payload, dict):
        raise BindingRefusal("CURRENT_EVIDENCE_PAYLOAD_REQUIRED")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(trust.current_public_key_hex))
        public_key.verify(signature, _canonical(payload))
    except (ValueError, InvalidSignature) as exc:
        raise BindingRefusal("CURRENT_EVIDENCE_SIGNATURE_INVALID") from exc
    if payload.get("issuer") != trust.current_issuer:
        raise BindingRefusal("CURRENT_EVIDENCE_ISSUER_MISMATCH")
    if payload.get("grant_sha256") != grant_ref.content_hash:
        raise BindingRefusal("CURRENT_EVIDENCE_GRANT_MISMATCH")
    if payload.get("request_digest") != _request_digest(request):
        raise BindingRefusal("CURRENT_EVIDENCE_REQUEST_MISMATCH")
    expected_decision = _expected_decision_ref(request, grant_ref)
    if _ref(payload.get("decision_ref"), "decision_ref") != expected_decision:
        raise BindingRefusal("CURRENT_EVIDENCE_DECISION_MISMATCH")
    permission_refs = _refs(payload.get("source_permission_refs"), "source_permission_refs")
    if permission_refs != (grant_ref,):
        raise BindingRefusal("CURRENT_EVIDENCE_PERMISSION_MISMATCH")
    if payload.get("currentness") != CURRENT_GRANTED:
        raise BindingRefusal("CURRENT_EVIDENCE_NOT_CURRENT")
    revocation = payload.get("revocation_ref")
    if revocation is not None:
        raise BindingRefusal("CURRENT_EVIDENCE_REVOKED")
    if not isinstance(payload.get("effective_interval"), str) or not payload["effective_interval"].strip():
        raise BindingRefusal("CURRENT_EVIDENCE_INTERVAL_REQUIRED")
    limits = payload.get("retention_export_limits")
    if not isinstance(limits, dict):
        raise BindingRefusal("CURRENT_EVIDENCE_LIMITS_REQUIRED")
    try:
        return IssuedSourceReadDecision(
            decision_ref=expected_decision,
            source_permission_refs=(grant_ref,),
            source_id=request.source_id,
            source_sha256=request.source_sha256,
            source_format=request.source_format,
            custody_locator_binding=request.custody_locator_binding,
            host=request.host,
            purpose=request.purpose,
            consumer_use=request.consumer_use,
            read_operation=request.read_operation,
            physical_read_extent=request.physical_read_extent,
            metadata_freeze_refs=request.metadata_freeze_refs,
            semantic_use_scope=request.semantic_use_scope,
            effective_interval=payload["effective_interval"],
            currentness=payload["currentness"],
            revocation_ref=None,
            retention_export_limits=limits,
        )
    except (SourceReadAdmissionRefusal, TypeError, ValueError) as exc:
        raise BindingRefusal("CURRENT_EVIDENCE_DECISION_INVALID") from exc


def bind_existing_grant(
    *,
    grant_path: str | Path,
    config: ConfigBinding,
    trust: ExternalTrust,
    current_evidence_path: str | Path | None = None,
) -> BindingResult:
    """Verify static grant/config and return a request or an exact hold.

    Missing independently authenticated current evidence is a hold, not a
    fabricated CURRENT and not a caller-supplied boolean.  No source path is
    touched.
    """
    trust.validate()
    config.validate(trust)
    grant, grant_sha, grant_ref = _load_grant(grant_path, trust)
    request = make_request(grant, config)
    if current_evidence_path is None:
        return BindingResult(
            status="RUNTIME_ISSUER_HOLD__INDEPENDENT_CURRENT_EVIDENCE_MISSING",
            request=request,
            decision=None,
            grant_sha256=grant_sha,
            grant_ref=grant_ref,
            request_digest=_request_digest(request),
            reason="STATIC_GRANT_HASH_IS_NOT_CURRENT",
        )
    decision = _verify_current_evidence(
        request=request,
        grant_ref=grant_ref,
        trust=trust,
        current_evidence_path=current_evidence_path,
    )
    return BindingResult(
        status="CURRENT_BOUND_REQUEST_ONLY",
        request=request,
        decision=decision,
        grant_sha256=grant_sha,
        grant_ref=grant_ref,
        request_digest=_request_digest(request),
        reason="EXTERNALLY_AUTHENTICATED_CURRENT_EVIDENCE",
    )


def check_src17_reuse_scope(
    *,
    grant_path: str | Path,
    authentication_path: str | Path,
    expected_grant_sha256: str,
    expected_authentication_sha256: str,
) -> dict[str, Any]:
    """Read-only scope check; never adapts SRC17 into an SRC04/I03/I05 grant."""
    grant_raw = Path(grant_path).read_bytes()
    auth_raw = Path(authentication_path).read_bytes()
    if _sha256(grant_raw) != expected_grant_sha256:
        raise BindingRefusal("SRC17_GRANT_TRUST_HASH_MISMATCH")
    if _sha256(auth_raw) != expected_authentication_sha256:
        raise BindingRefusal("SRC17_AUTH_TRUST_HASH_MISMATCH")
    grant = json.loads(grant_raw.decode("utf-8"))
    auth = json.loads(auth_raw.decode("utf-8"))
    if grant.get("source_id") != "SRC17":
        raise BindingRefusal("SRC17_SOURCE_MISMATCH")
    if grant.get("purpose") != "SECOND_FAMILY_ORIGINAL_SOURCE_C11_POSITIVE":
        raise BindingRefusal("SRC17_PURPOSE_UNEXPECTED")
    if grant.get("consumer") != SRC04_CONSUMER:
        raise BindingRefusal("SRC17_CONSUMER_UNEXPECTED")
    if auth.get("source_id") != "SRC17" or auth.get("purpose") != grant.get("purpose"):
        raise BindingRefusal("SRC17_AUTH_BINDING_MISMATCH")
    if auth.get("currentness") != CURRENT_GRANTED or auth.get("revocation") not in (None, "NONE_RECORDED"):
        raise BindingRefusal("SRC17_AUTH_NOT_CURRENT")
    return {
        "schema": "ANVIL_SRC17_REUSE_SCOPE_CHECK@1",
        "source_id": "SRC17",
        "grant_sha256": expected_grant_sha256,
        "authentication_sha256": expected_authentication_sha256,
        "purpose": grant["purpose"],
        "scope_is_source_specific": True,
        "reusable_for_src04_binding": False,
        "reusable_for_i03_i05": False,
        "no_i03_i05_expansion": True,
        "scientific_allow_claimed": False,
        "reason": "SRC17_IS_EXACT_CONSTRUCTION_SOURCE_READ_C11_ONLY__NOT_A_CROSS_SOURCE_OR_SCIENTIFIC_GRANT",
    }


class ExistingGrantResolver:
    """Thin R157 resolver over a verified BindingResult.

    It never creates CURRENT; a hold is a refusal, and a verified decision is
    returned only after external signature/trust and exact request matching.
    """

    def __init__(self, binding: BindingResult):
        if not isinstance(binding, BindingResult):
            raise BindingRefusal("BINDING_RESULT_REQUIRED")
        self.binding = binding
        self.calls = 0

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        self.calls += 1
        if not isinstance(request, SourceReadRequest) or request != self.binding.request:
            raise SourceReadAdmissionRefusal("SOURCE_READ_REQUEST_MISMATCH")
        if self.binding.decision is None:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_CURRENT_EVIDENCE_HOLD", self.binding.status)
        return self.binding.decision


__all__ = [
    "SCHEMA", "BindingRefusal", "BindingResult", "ConfigBinding",
    "ExternalTrust", "ExistingGrantResolver", "bind_existing_grant",
    "check_src17_reuse_scope", "make_request",
]
