"""Externally authenticated source-read admission before R04 response decode.

This module is transport only. It creates no source right, issuer, current grant,
or scientific permission. A trusted deployment resolver authenticates the
supplied exact decision; fixture resolvers only exercise call order.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    PhysicalSourceIncidence,
    decode_dta,
    decode_sav,
)

SOURCE_RESPONSE_DECODE = "SOURCE_RESPONSE_DECODE"
EXACT_FILE = "EXACT_FILE"
CURRENT_GRANTED = "CURRENT_GRANTED"
TERMINAL_STATES = frozenset({"REVOKED", "EXPIRED", "SUPERSEDED", "SUSPENDED"})
SOURCE_FORMATS = frozenset({"SAV", "DTA"})


class SourceReadAdmissionRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _sha(value: Any, name: str) -> str:
    if (not isinstance(value, str) or len(value) != 64 or value.lower() != value
            or any(ch not in "0123456789abcdef" for ch in value)):
        raise SourceReadAdmissionRefusal("SOURCE_READ_SHA_REQUIRED", name)
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceReadAdmissionRefusal("SOURCE_READ_FIELD_REQUIRED", name)
    return value


def _refs(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or not value:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_REQUIRED", name)
    try:
        return tuple(sorted((exact_ref(item, name) for item in value), key=lambda ref: ref.key))
    except Exception as exc:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REFS_INVALID", name) from exc


@dataclass(frozen=True)
class SourceReadRequest:
    """Metadata-only request; it contains no decoded response capability."""

    source_id: str
    source_sha256: str
    source_format: str
    custody_locator_binding: str
    host: str
    purpose: str
    consumer_use: str
    read_operation: str = SOURCE_RESPONSE_DECODE
    physical_read_extent: str = EXACT_FILE
    metadata_freeze_refs: tuple[ExactRef, ...] = ()
    semantic_use_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.source_id, "source_id")
        _sha(self.source_sha256, "source_sha256")
        if not isinstance(self.source_format, str) or self.source_format.upper() not in SOURCE_FORMATS:
            raise SourceReadAdmissionRefusal("SOURCE_READ_FORMAT_REQUIRED", self.source_format)
        object.__setattr__(self, "source_format", self.source_format.upper())
        for name in ("custody_locator_binding", "host", "purpose", "consumer_use"):
            _text(getattr(self, name), name)
        if self.read_operation != SOURCE_RESPONSE_DECODE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_OPERATION_UNSUPPORTED", self.read_operation)
        if self.physical_read_extent != EXACT_FILE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_EXTENT_UNSUPPORTED", self.physical_read_extent)
        object.__setattr__(self, "metadata_freeze_refs", _refs(
            self.metadata_freeze_refs, "metadata_freeze_refs"))
        if (isinstance(self.semantic_use_scope, (str, bytes))
                or not isinstance(self.semantic_use_scope, Sequence)
                or not self.semantic_use_scope
                or any(not isinstance(item, str) or not item.strip()
                       for item in self.semantic_use_scope)):
            raise SourceReadAdmissionRefusal("SOURCE_READ_SEMANTIC_SCOPE_REQUIRED")
        object.__setattr__(self, "semantic_use_scope", tuple(sorted(set(self.semantic_use_scope))))


@dataclass(frozen=True)
class IssuedSourceReadDecision:
    """External issuer read result; construction here does not authenticate it."""

    decision_ref: ExactRef
    source_permission_refs: tuple[ExactRef, ...]
    source_id: str
    source_sha256: str
    source_format: str
    custody_locator_binding: str
    host: str
    purpose: str
    consumer_use: str
    read_operation: str
    physical_read_extent: str
    metadata_freeze_refs: tuple[ExactRef, ...]
    semantic_use_scope: tuple[str, ...]
    effective_interval: str
    currentness: str
    revocation_ref: ExactRef | None
    retention_export_limits: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_ref", exact_ref(self.decision_ref, "decision_ref"))
        object.__setattr__(self, "source_permission_refs", _refs(
            self.source_permission_refs, "source_permission_refs"))
        _text(self.source_id, "source_id")
        _sha(self.source_sha256, "source_sha256")
        if not isinstance(self.source_format, str) or self.source_format.upper() not in SOURCE_FORMATS:
            raise SourceReadAdmissionRefusal("SOURCE_READ_FORMAT_REQUIRED", self.source_format)
        object.__setattr__(self, "source_format", self.source_format.upper())
        for name in ("custody_locator_binding", "host", "purpose", "consumer_use",
                     "read_operation", "physical_read_extent", "effective_interval",
                     "currentness"):
            _text(getattr(self, name), name)
        if self.read_operation != SOURCE_RESPONSE_DECODE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_OPERATION_UNSUPPORTED", self.read_operation)
        if self.physical_read_extent != EXACT_FILE:
            raise SourceReadAdmissionRefusal("SOURCE_READ_EXTENT_UNSUPPORTED", self.physical_read_extent)
        object.__setattr__(self, "metadata_freeze_refs", _refs(
            self.metadata_freeze_refs, "metadata_freeze_refs"))
        if (isinstance(self.semantic_use_scope, (str, bytes))
                or not isinstance(self.semantic_use_scope, Sequence)
                or not self.semantic_use_scope
                or any(not isinstance(item, str) or not item.strip()
                       for item in self.semantic_use_scope)):
            raise SourceReadAdmissionRefusal("SOURCE_READ_SEMANTIC_SCOPE_REQUIRED")
        object.__setattr__(self, "semantic_use_scope", tuple(sorted(set(self.semantic_use_scope))))
        if self.revocation_ref is not None:
            object.__setattr__(self, "revocation_ref", exact_ref(self.revocation_ref, "revocation_ref"))
        if not isinstance(self.retention_export_limits, Mapping):
            raise SourceReadAdmissionRefusal("SOURCE_READ_LIMITS_REQUIRED")


@dataclass(frozen=True)
class SourceReaderConfiguration:
    """Qualified exact-SHA reader configuration supplied before source I/O.

    The object carries no source right.  It only proves that an encoding choice
    is the exact allowlisted choice for the request's source SHA, or that no
    override is requested.
    """

    source_sha256: str
    encoding: str | None = None
    authority_status: str | None = None
    configuration_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        _sha(self.source_sha256, "source_sha256")
        if self.configuration_ref is not None:
            object.__setattr__(
                self, "configuration_ref",
                exact_ref(self.configuration_ref, "configuration_ref"))
        if self.encoding in ("auto", "guess", "fallback"):
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_GUESS_FORBIDDEN", str(self.encoding))
        if self.encoding is None:
            if self.authority_status is not None:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_ENCODING_STATUS_WITHOUT_ENCODING")
            return
        if not isinstance(self.encoding, str) or not self.encoding.strip():
            raise SourceReadAdmissionRefusal("SOURCE_READ_ENCODING_REQUIRED")
        qualified = COMPATIBILITY_ALLOWLIST.get(self.source_sha256)
        if qualified != self.encoding:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_NOT_QUALIFIED", self.encoding)
        if self.authority_status != COMPATIBILITY_ONLY:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_ENCODING_STATUS_REQUIRED", str(self.authority_status))


class SourceReadDecisionResolver(Protocol):
    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        """Authenticate issuer/currentness/revocation/host/purpose externally."""
        ...


def _assert_current(decision: IssuedSourceReadDecision, request: SourceReadRequest) -> None:
    if not isinstance(decision, IssuedSourceReadDecision):
        raise SourceReadAdmissionRefusal("SOURCE_READ_DECISION_REQUIRED")
    if decision.currentness != CURRENT_GRANTED:
        raise SourceReadAdmissionRefusal("SOURCE_READ_NOT_CURRENT", decision.currentness)
    if decision.revocation_ref is not None:
        raise SourceReadAdmissionRefusal("SOURCE_READ_REVOKED")
    pairs = (
        ("source_id", decision.source_id, request.source_id),
        ("source_sha256", decision.source_sha256, request.source_sha256),
        ("source_format", decision.source_format, request.source_format),
        ("custody_locator_binding", decision.custody_locator_binding, request.custody_locator_binding),
        ("host", decision.host, request.host),
        ("purpose", decision.purpose, request.purpose),
        ("consumer_use", decision.consumer_use, request.consumer_use),
        ("read_operation", decision.read_operation, request.read_operation),
        ("physical_read_extent", decision.physical_read_extent, request.physical_read_extent),
        ("metadata_freeze_refs", decision.metadata_freeze_refs, request.metadata_freeze_refs),
        ("semantic_use_scope", decision.semantic_use_scope, request.semantic_use_scope),
    )
    for name, actual, expected in pairs:
        if actual != expected:
            raise SourceReadAdmissionRefusal(f"SOURCE_READ_{name.upper()}_MISMATCH")


def decode_with_source_read_permission(
    *,
    source_path: Any,
    request: SourceReadRequest,
    resolver: SourceReadDecisionResolver,
    reader: SourceReaderConfiguration | None = None,
) -> PhysicalSourceIncidence:
    """Resolve exact current predecode permission, then invoke the R04 decoder.

    ``source_path`` is not opened, stat'ed, hashed or inspected by this function
    before ``resolver.resolve_current(request)`` returns a valid current decision.
    A supplied ``reader`` is qualified against the request's exact source SHA
    before any source I/O; it cannot select an unallowlisted encoding.
    """
    if not isinstance(request, SourceReadRequest):
        raise SourceReadAdmissionRefusal("SOURCE_READ_REQUEST_REQUIRED")
    if reader is not None:
        if not isinstance(reader, SourceReaderConfiguration):
            raise SourceReadAdmissionRefusal("SOURCE_READ_READER_CONFIGURATION_REQUIRED")
        if reader.source_sha256 != request.source_sha256:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_READER_SOURCE_SHA_MISMATCH", reader.source_sha256)
    decision = resolver.resolve_current(request)
    _assert_current(decision, request)
    decoder = decode_sav if request.source_format == "SAV" else decode_dta
    encoding = None if reader is None else reader.encoding
    incidence = decoder(
        source_path, expected_source_sha256=decision.source_sha256, encoding=encoding)
    try:
        current = resolver.resolve_current(request)
        _assert_current(current, request)
        if current != decision:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECISION_CHANGED_AFTER_DECODE")
        if incidence.source_sha256 != decision.source_sha256:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECODED_EDITION_MISMATCH")
        if str(incidence.source_format).upper() != decision.source_format:
            raise SourceReadAdmissionRefusal("SOURCE_READ_DECODED_FORMAT_MISMATCH")
        if reader is not None:
            actual = incidence.reader_configuration
            if actual.get("encoding") != reader.encoding:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_READER_ENCODING_MISMATCH", str(actual.get("encoding")))
            if reader.encoding is not None and actual.get("authority_status") != COMPATIBILITY_ONLY:
                raise SourceReadAdmissionRefusal(
                    "SOURCE_READ_READER_ENCODING_AUTHORITY_MISMATCH",
                    str(actual.get("authority_status")))
        return incidence
    except BaseException:
        incidence.close()
        raise


__all__ = [
    "CURRENT_GRANTED", "EXACT_FILE", "SOURCE_RESPONSE_DECODE",
    "IssuedSourceReadDecision", "SourceReadAdmissionRefusal",
    "SourceReadDecisionResolver", "SourceReadRequest", "SourceReaderConfiguration",
    "decode_with_source_read_permission",
]
