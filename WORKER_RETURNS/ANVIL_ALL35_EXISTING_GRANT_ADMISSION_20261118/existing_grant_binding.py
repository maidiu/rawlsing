#!/usr/bin/env python3
"""Reusable existing-grant to R157 source-read binding.

Construction/source-read preparation only.  This module does not issue a new
source right, scientific eligibility, CURRENT record, or I03/I05 authority.

It deliberately follows the accepted historical SRC04 grant route
(303a57851785557fff8229e29a5554717168cbd1):
``validate_grant_document`` accepts an exact human grant, and
``FullGrantResolver.resolve_current`` rechecks the exact bound request and grant
bytes on every callback.  The grant's own currentness/revocation fields are the
controls; no bespoke signature or nonexistent current artifact is required.
No source path is opened, stat'ed, hashed, or decoded here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

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
SRC04_SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
SRC04_SOURCE_ROWS = 7337
SRC04_SOURCE_COLUMNS = 181
SRC04_SOURCE_BYTES = 1531099
SRC04_SEMANTIC_SCOPE = (
    "SOURCE_NATIVE_RESPONSE_INCIDENCE",
    "NO_SEMANTIC_ADOPTION",
    "SRC04",
    "FULL_SRC04_C11_CONSTRUCTION",
)
RETENTION_EXPORT_LIMITS = {
    "export": "DENY",
    "rowwise_response_artifacts": "DENY",
    "retention": "LOCAL_RUNTIME_ONLY",
    "source_bytes_in_git": "DENY",
}
HERE = Path(__file__).resolve().parent


class BindingRefusal(ValueError):
    """A static grant, config, request, or current check failed closed."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (f": {detail}" if detail else ""))
        self.code = code
        self.detail = detail


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _path(value: str | Path) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (HERE / p)


def _ref(value: Mapping[str, Any] | ExactRef, name: str) -> ExactRef:
    try:
        if isinstance(value, ExactRef):
            return value
        if not isinstance(value, Mapping):
            raise TypeError
        return ExactRef(str(value["kind"]), str(value["object_id"]),
                        str(value["content_hash"]))
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
    """Exact R157 config metadata, without source bytes or full config copy."""

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
        if self.source_sha256 != SRC04_SOURCE_SHA256:
            raise BindingRefusal("CONFIG_SOURCE_SHA_MISMATCH")
        if self.source_format != "SAV":
            raise BindingRefusal("CONFIG_SOURCE_FORMAT_MISMATCH")
        if self.locator_id != "SRC04_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING":
            raise BindingRefusal("CONFIG_LOCATOR_MISMATCH")
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
    """Deployment-supplied exact hashes and grant location."""

    grant_sha256: str
    grant_path: str
    config_file_sha256: str
    config_canonical_sha256: str
    config_binding_sha256: str

    def validate(self) -> None:
        for value, name in (
            (self.grant_sha256, "grant_sha256"),
            (self.config_file_sha256, "config_file_sha256"),
            (self.config_canonical_sha256, "config_canonical_sha256"),
            (self.config_binding_sha256, "config_binding_sha256"),
        ):
            if not isinstance(value, str) or len(value) != 64 or value.lower() != value:
                raise BindingRefusal("TRUST_SHA_REQUIRED", name)
        if not isinstance(self.grant_path, str) or not self.grant_path.strip():
            raise BindingRefusal("TRUST_GRANT_LOCATION_REQUIRED")


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
            "retention_export_limits": RETENTION_EXPORT_LIMITS,
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


def validate_grant_document(document: Mapping[str, Any], grant_sha256: str) -> None:
    """Accepted SRC04 grant checks; no source path is touched."""
    if not isinstance(document, Mapping):
        raise BindingRefusal("GRANT_DOCUMENT_REQUIRED")
    if document.get("schema") != SRC04_GRANT_SCHEMA:
        raise BindingRefusal("GRANT_SCHEMA_MISMATCH")
    if document.get("source_id") != "SRC04":
        raise BindingRefusal("GRANT_SOURCE_MISMATCH")
    if document.get("expected_source_sha256") != SRC04_SOURCE_SHA256:
        raise BindingRefusal("GRANT_SOURCE_SHA_MISMATCH")
    if document.get("host") != "USER_LOCAL_MAC":
        raise BindingRefusal("GRANT_HOST_MISMATCH")
    if document.get("purpose") != SRC04_PURPOSE:
        raise BindingRefusal("GRANT_PURPOSE_MISMATCH")
    if document.get("consumer") != SRC04_CONSUMER:
        raise BindingRefusal("GRANT_CONSUMER_MISMATCH")
    if document.get("full_source") is not True or document.get("first_slice_only") is not False:
        raise BindingRefusal("GRANT_SCOPE_NOT_FULL")
    if document.get("scope") != SRC04_SCOPE:
        raise BindingRefusal("GRANT_SCOPE_NOT_FULL")
    for key, expected in (("source_rows", SRC04_SOURCE_ROWS),
                          ("source_columns", SRC04_SOURCE_COLUMNS),
                          ("source_bytes", SRC04_SOURCE_BYTES)):
        if document.get(key) != expected:
            raise BindingRefusal("GRANT_" + key.upper() + "_MISMATCH")
    if document.get("currentness") != CURRENT_GRANTED:
        raise BindingRefusal("GRANT_NOT_CURRENT", str(document.get("currentness")))
    if document.get("revocation") not in (None, "NONE_RECORDED"):
        raise BindingRefusal("GRANT_REVOKED", str(document.get("revocation")))
    if not isinstance(document.get("authorization"), str) or not document["authorization"].strip():
        raise BindingRefusal("GRANT_AUTHORIZATION_REQUIRED")
    if not isinstance(document.get("source_path"), str) or not document["source_path"].strip():
        raise BindingRefusal("GRANT_SOURCE_PATH_REQUIRED")
    if (not isinstance(grant_sha256, str) or len(grant_sha256) != 64
            or grant_sha256.lower() != grant_sha256):
        raise BindingRefusal("GRANT_SHA_REQUIRED")


def _load_grant(path: str | Path, trust: ExternalTrust) -> tuple[dict[str, Any], str, ExactRef]:
    actual_path = _path(path)
    expected_path = _path(trust.grant_path)
    if actual_path.resolve() != expected_path.resolve():
        raise BindingRefusal("GRANT_LOCATION_MISMATCH", str(actual_path))
    try:
        raw = actual_path.read_bytes()
    except OSError as exc:
        raise BindingRefusal("GRANT_BYTES_UNAVAILABLE", str(actual_path)) from exc
    actual = _sha256(raw)
    if actual != trust.grant_sha256:
        raise BindingRefusal("GRANT_TRUST_HASH_MISMATCH", actual)
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BindingRefusal("GRANT_JSON_INVALID") from exc
    validate_grant_document(document, actual)
    if document.get("source_id") != "SRC04":
        raise BindingRefusal("GRANT_SOURCE_MISMATCH")
    grant_ref = ExactRef(
        "FULL_SOURCE_READ_GRANT",
        f"urn:rawlsing:full-source-grant:SRC04:{actual}", actual)
    return document, actual, grant_ref


def make_request(grant: Mapping[str, Any], config: ConfigBinding) -> SourceReadRequest:
    """Build exact request from frozen config metadata and exact grant."""
    if grant.get("source_id") != config.source_id:
        raise BindingRefusal("GRANT_CONFIG_SOURCE_MISMATCH")
    if grant.get("expected_source_sha256") != config.source_sha256:
        raise BindingRefusal("GRANT_CONFIG_SOURCE_SHA_MISMATCH")
    if grant.get("host") != "USER_LOCAL_MAC":
        raise BindingRefusal("GRANT_HOST_MISMATCH")
    if grant.get("purpose") != SRC04_PURPOSE or grant.get("consumer") != SRC04_CONSUMER:
        raise BindingRefusal("GRANT_PURPOSE_OR_CONSUMER_MISMATCH")
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


def make_decision(request: SourceReadRequest, grant_ref: ExactRef) -> IssuedSourceReadDecision:
    """Decision from the accepted grant; currentness is the grant's control."""
    return IssuedSourceReadDecision(
        decision_ref=ExactRef(
            "FULL_SOURCE_READ_DECISION",
            f"urn:rawlsing:full-source-decision:SRC04:{grant_ref.content_hash}",
            semantic_hash({
                "grant_sha256": grant_ref.content_hash,
                "source_id": request.source_id,
                "source_sha256": request.source_sha256,
                "host": request.host,
                "purpose": request.purpose,
                "consumer": request.consumer_use,
                "scope": SRC04_SCOPE,
                "read_operation": request.read_operation,
                "physical_read_extent": request.physical_read_extent,
            }),
        ),
        source_permission_refs=(grant_ref,),
        source_id=request.source_id,
        source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        read_operation=SOURCE_RESPONSE_DECODE,
        physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-10-28/FULL_SRC04_PINNED_GRANT",
        currentness=CURRENT_GRANTED,
        revocation_ref=None,
        retention_export_limits=RETENTION_EXPORT_LIMITS,
    )


def bind_existing_grant(
    *, grant_path: str | Path, config: ConfigBinding, trust: ExternalTrust
) -> BindingResult:
    """Verify exact grant/config and return allowed request-only binding."""
    trust.validate()
    config.validate(trust)
    grant, grant_sha, grant_ref = _load_grant(grant_path, trust)
    request = make_request(grant, config)
    decision = make_decision(request, grant_ref)
    return BindingResult(
        status="REQUEST_ONLY_ALLOWED",
        request=request,
        decision=decision,
        grant_sha256=grant_sha,
        grant_ref=grant_ref,
        request_digest=_request_digest(request),
        reason="EXACT_EXISTING_GRANT_AND_BOUND_REQUEST",
    )


class ExistingGrantResolver:
    """Concrete R157 resolver; rechecks bound grant/request on every call."""

    def __init__(self, grant_path: str | Path, trust: ExternalTrust,
                 request: SourceReadRequest):
        self.grant_path = _path(grant_path)
        self.trust = trust
        self.request = request
        self.calls = 0

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        self.calls += 1
        if not isinstance(request, SourceReadRequest) or request != self.request:
            raise SourceReadAdmissionRefusal("FULL_GRANT_REQUEST_MISMATCH")
        try:
            _, _, grant_ref = _load_grant(self.grant_path, self.trust)
            decision = make_decision(request, grant_ref)
        except BindingRefusal as exc:
            if exc.code == "GRANT_TRUST_HASH_MISMATCH" or exc.code == "GRANT_LOCATION_MISMATCH":
                raise SourceReadAdmissionRefusal(
                    "FULL_GRANT_CURRENTNESS_MISMATCH", exc.code) from exc
            raise SourceReadAdmissionRefusal("FULL_GRANT_CURRENT_REFUSED", exc.code) from exc
        return decision


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


__all__ = [
    "SCHEMA", "BindingRefusal", "BindingResult", "ConfigBinding",
    "ExternalTrust", "ExistingGrantResolver", "bind_existing_grant",
    "check_src17_reuse_scope", "make_decision", "make_request",
    "validate_grant_document",
]
