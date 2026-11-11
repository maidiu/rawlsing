"""Immutable cross-spine protocol wrappers for WSC002 Golden Thread 0.

These objects are deliberately non-semantic. They conserve exact producer,
authority, permission, typed-state and replay references across seams; they do
not transfer ownership or mint source/FIELD-FORGE/PRE-V3/V3/V2 meaning.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any, Iterable, Mapping, Sequence

GT0_PROTOCOL_VERSION = "WSC002_GT0_PROTOCOL@1"
GT0_ENVELOPE_SCHEMA = "WSC002_GT0_CONSERVATION_ENVELOPE@1"
GT0_STAGE_RECEIPT_SCHEMA = "WSC002_GT0_STAGE_RECEIPT@1"
GT0_REFERENCE_SCHEMA = "WSC002_GT0_EXACT_UPSTREAM_REF@1"

_DIGEST_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
_MUTABLE_SELECTOR_RE = re.compile(
    r"(^|[:/@._-])(latest|default|fuzzy|nearest|semver(?:_fallback)?|\*)(?:$|[:/@._-])",
    re.IGNORECASE,
)


class GT0ProtocolError(ValueError):
    """Base error for invalid GT0 protocol material."""


class GT0ReferenceError(GT0ProtocolError):
    """An upstream reference is not exact enough for GT0 conservation."""


class GT0IntegrityError(GT0ProtocolError):
    """Deterministic identity or cross-field closure is invalid."""


class GT0PermissionError(GT0ProtocolError):
    """A consumer permission ceiling widened beyond its upstream ceiling."""


class GT0StageStatus(str, Enum):
    PASS = "PASS"
    OBSERVED_ZERO = "OBSERVED_ZERO"
    VALID_EMPTY = "VALID_EMPTY"
    UNDEFINED_FOR_OBJECT = "UNDEFINED_FOR_OBJECT"
    BLOCKED_EXPLICIT_AUTHORITY = "BLOCKED_EXPLICIT_AUTHORITY"
    BLOCKED_COMPARATOR_ANCESTRY = "BLOCKED_COMPARATOR_ANCESTRY"
    BLOCKED_POSITIVE_TRANSITION_AUTHORITY = "BLOCKED_POSITIVE_TRANSITION_AUTHORITY"
    BLOCKED_NAMED_AUTHORITY_REQUIRED = "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNRESOLVED = "UNRESOLVED"
    DENIED = "DENIED"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT0ProtocolError(f"{name} must be a non-empty string")
    return value.strip()


def _exact_text(value: Any, name: str) -> str:
    out = _text(value, name)
    if _MUTABLE_SELECTOR_RE.search(out):
        raise GT0ReferenceError(
            f"{name} may not contain latest/default/fuzzy/nearest/semver fallback selection"
        )
    return out


def _digest(value: Any, name: str) -> str:
    value = _exact_text(value, name)
    if not _DIGEST_RE.fullmatch(value):
        raise GT0IntegrityError(f"{name} must be an exact lowercase 40- or 64-hex digest")
    return value


def _sha256(value: Any, name: str) -> str:
    value = _text(value, name)
    if len(value) != 64 or not _DIGEST_RE.fullmatch(value):
        raise GT0IntegrityError(f"{name} must be an exact lowercase sha256")
    return value


@dataclass(frozen=True, order=True, slots=True)
class GT0ExactRef:
    """Typed immutable reference to an upstream producer-owned identity."""

    kind: str
    value: str
    content_hash: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _exact_text(self.kind, "reference.kind"))
        object.__setattr__(self, "value", _exact_text(self.value, "reference.value"))
        if self.content_hash is not None:
            object.__setattr__(
                self,
                "content_hash",
                _digest(self.content_hash, "reference.content_hash"),
            )

    @property
    def key(self) -> str:
        return f"{self.kind}|{self.value}|{self.content_hash or ''}"

    def as_dict(self) -> dict[str, str | None]:
        return {
            "schema": GT0_REFERENCE_SCHEMA,
            "kind": self.kind,
            "value": self.value,
            "content_hash": self.content_hash,
        }


def validate_exact_upstream_ref(value: Any, name: str = "upstream_ref") -> GT0ExactRef:
    """Coerce one explicit producer reference and reject mutable selectors."""
    if isinstance(value, GT0ExactRef):
        return value

    if all(hasattr(value, attr) for attr in ("kind", "object_id", "content_hash")):
        return GT0ExactRef(
            kind=getattr(value, "kind"),
            value=getattr(value, "object_id"),
            content_hash=getattr(value, "content_hash"),
        )

    if isinstance(value, Mapping):
        keys = set(value)
        if keys in ({"kind", "value"}, {"kind", "value", "content_hash"}):
            return GT0ExactRef(
                kind=value["kind"],
                value=value["value"],
                content_hash=value.get("content_hash"),
            )
        if keys == {"kind", "object_id", "content_hash"}:
            return GT0ExactRef(
                kind=value["kind"],
                value=value["object_id"],
                content_hash=value["content_hash"],
            )
        raise GT0ReferenceError(
            f"{name} mapping must contain exact kind/value[/content_hash] "
            "or kind/object_id/content_hash"
        )

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        if len(value) == 2:
            return GT0ExactRef(value[0], value[1])
        if len(value) == 3:
            return GT0ExactRef(value[0], value[1], value[2])
        raise GT0ReferenceError(f"{name} tuple/list must have 2 or 3 items")

    if isinstance(value, str):
        token = _exact_text(value, name)
        if _DIGEST_RE.fullmatch(token):
            kind = "GIT_OR_CONTENT_DIGEST" if len(token) == 40 else "CONTENT_DIGEST"
            return GT0ExactRef(kind, token, token if len(token) == 64 else None)
        if token.startswith(("urn:", "cssu.", "rawlsing:")) or ":" in token or "/" in token:
            return GT0ExactRef("OPAQUE_EXACT_ID", token)
        raise GT0ReferenceError(
            f"{name} bare string is not demonstrably exact; supply a typed kind/value reference"
        )

    raise GT0ReferenceError(f"{name} has unsupported reference type {type(value).__name__}")


def _refs(values: Iterable[Any], name: str) -> tuple[GT0ExactRef, ...]:
    by_key: dict[str, GT0ExactRef] = {}
    for value in values:
        ref = validate_exact_upstream_ref(value, name)
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _tokens(values: Iterable[Any], name: str) -> tuple[str, ...]:
    by_value: dict[str, str] = {}
    for value in values:
        token = _exact_text(value, name)
        by_value[token] = token
    return tuple(by_value[key] for key in sorted(by_value))


def _status(value: GT0StageStatus | str) -> GT0StageStatus:
    if isinstance(value, GT0StageStatus):
        return value
    try:
        return GT0StageStatus(_text(value, "status"))
    except ValueError as exc:
        raise GT0IntegrityError(f"unknown GT0 stage status {value!r}") from exc


def _canonical(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise GT0IntegrityError("binary float/NaN/Infinity forbidden in GT0 identity material")
    if isinstance(value, Enum):
        return _canonical(value.value)
    if isinstance(value, GT0ExactRef):
        return value.as_dict()
    if isinstance(value, GT0ConservationEnvelope):
        return value.identity_material()
    if isinstance(value, GT0StageReceipt):
        return value.identity_material()
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise GT0IntegrityError("GT0 identity mapping keys must be strings")
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (set, frozenset)):
        items = [_canonical(item) for item in value]
        return sorted(items, key=_canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_canonical(item) for item in value]
    raise GT0IntegrityError(f"unsupported GT0 identity material type {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def gt0_content_hash(value: Any) -> str:
    """Deterministic sha256 over canonical GT0 identity material."""
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def assert_permission_narrowing(upstream: Iterable[Any], downstream: Iterable[Any]) -> tuple[str, ...]:
    """Return canonical downstream permission tokens iff no permission widened."""
    before = frozenset(_tokens(upstream, "upstream_permission"))
    after = _tokens(downstream, "downstream_permission")
    widened = sorted(set(after) - before)
    if widened:
        raise GT0PermissionError(
            f"consumer permission widened beyond upstream ceiling: {widened!r}"
        )
    return after


@dataclass(frozen=True, slots=True)
class GT0ConservationEnvelope:
    """Non-semantic courier over exact producer-owned references."""

    semantic_owner_ref: GT0ExactRef | Any
    object_refs: tuple[GT0ExactRef | Any, ...]
    authority_refs: tuple[GT0ExactRef | Any, ...] = ()
    current_selection_refs: tuple[GT0ExactRef | Any, ...] = ()
    scope_refs: tuple[GT0ExactRef | Any, ...] = ()
    relation_query_refs: tuple[GT0ExactRef | Any, ...] = ()
    permission_ceiling: tuple[str, ...] = ()
    status: GT0StageStatus | str = GT0StageStatus.PASS
    dependency_refs: tuple[GT0ExactRef | Any, ...] = ()
    provenance_refs: tuple[GT0ExactRef | Any, ...] = ()
    replay_refs: tuple[GT0ExactRef | Any, ...] = ()
    information_loss: str = "NONE__REFERENCE_PRESERVING"

    def __post_init__(self) -> None:
        owner = validate_exact_upstream_ref(self.semantic_owner_ref, "semantic_owner_ref")
        objects = _refs(self.object_refs, "object_ref")
        if not objects:
            raise GT0IntegrityError("GT0ConservationEnvelope requires at least one object_ref")
        object.__setattr__(self, "semantic_owner_ref", owner)
        object.__setattr__(self, "object_refs", objects)
        object.__setattr__(self, "authority_refs", _refs(self.authority_refs, "authority_ref"))
        object.__setattr__(
            self,
            "current_selection_refs",
            _refs(self.current_selection_refs, "current_selection_ref"),
        )
        object.__setattr__(self, "scope_refs", _refs(self.scope_refs, "scope_ref"))
        object.__setattr__(
            self,
            "relation_query_refs",
            _refs(self.relation_query_refs, "relation_query_ref"),
        )
        object.__setattr__(
            self,
            "permission_ceiling",
            _tokens(self.permission_ceiling, "permission_ceiling"),
        )
        object.__setattr__(self, "status", _status(self.status))
        object.__setattr__(self, "dependency_refs", _refs(self.dependency_refs, "dependency_ref"))
        object.__setattr__(self, "provenance_refs", _refs(self.provenance_refs, "provenance_ref"))
        object.__setattr__(self, "replay_refs", _refs(self.replay_refs, "replay_ref"))
        object.__setattr__(self, "information_loss", _text(self.information_loss, "information_loss"))

    def identity_material(self) -> dict[str, Any]:
        return {
            "schema": GT0_ENVELOPE_SCHEMA,
            "semantic_owner_ref": self.semantic_owner_ref,
            "object_refs": self.object_refs,
            "authority_refs": self.authority_refs,
            "current_selection_refs": self.current_selection_refs,
            "scope_refs": self.scope_refs,
            "relation_query_refs": self.relation_query_refs,
            "permission_ceiling": self.permission_ceiling,
            "status": self.status,
            "dependency_refs": self.dependency_refs,
            "provenance_refs": self.provenance_refs,
            "replay_refs": self.replay_refs,
            "information_loss": self.information_loss,
        }

    @property
    def content_hash(self) -> str:
        return gt0_content_hash(self.identity_material())

    def as_dict(self) -> dict[str, Any]:
        return _canonical({**self.identity_material(), "content_hash": self.content_hash})

    def narrowed_permissions(self, permissions: Iterable[Any]) -> tuple[str, ...]:
        return assert_permission_narrowing(self.permission_ceiling, permissions)


@dataclass(frozen=True, slots=True)
class GT0StageReceipt:
    """Deterministic non-semantic record of one cross-spine stage disposition."""

    stage_id: str
    status: GT0StageStatus | str
    input_envelope_hashes: tuple[str, ...]
    output_envelope: GT0ConservationEnvelope
    upstream_refs: tuple[GT0ExactRef | Any, ...] = ()
    authority_refs: tuple[GT0ExactRef | Any, ...] = ()
    replay_refs: tuple[GT0ExactRef | Any, ...] = ()
    detail_code: str = "NONE"

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage_id", _text(self.stage_id, "stage_id"))
        stage_status = _status(self.status)
        object.__setattr__(self, "status", stage_status)
        hashes = tuple(sorted({_sha256(value, "input_envelope_hash") for value in self.input_envelope_hashes}))
        object.__setattr__(self, "input_envelope_hashes", hashes)
        if not isinstance(self.output_envelope, GT0ConservationEnvelope):
            raise GT0IntegrityError("output_envelope must be GT0ConservationEnvelope")
        if self.output_envelope.status != stage_status:
            raise GT0IntegrityError("stage status must exactly match output envelope status")
        object.__setattr__(self, "upstream_refs", _refs(self.upstream_refs, "upstream_ref"))
        object.__setattr__(self, "authority_refs", _refs(self.authority_refs, "authority_ref"))
        object.__setattr__(self, "replay_refs", _refs(self.replay_refs, "replay_ref"))
        object.__setattr__(self, "detail_code", _text(self.detail_code, "detail_code"))

    def identity_material(self) -> dict[str, Any]:
        return {
            "schema": GT0_STAGE_RECEIPT_SCHEMA,
            "stage_id": self.stage_id,
            "status": self.status,
            "input_envelope_hashes": self.input_envelope_hashes,
            "output_envelope_hash": self.output_envelope.content_hash,
            "upstream_refs": self.upstream_refs,
            "authority_refs": self.authority_refs,
            "replay_refs": self.replay_refs,
            "detail_code": self.detail_code,
        }

    @property
    def content_hash(self) -> str:
        return gt0_content_hash(self.identity_material())

    def as_dict(self) -> dict[str, Any]:
        return _canonical({
            **self.identity_material(),
            "output_envelope": self.output_envelope.as_dict(),
            "content_hash": self.content_hash,
        })


__all__ = [
    "GT0_PROTOCOL_VERSION",
    "GT0_ENVELOPE_SCHEMA",
    "GT0_STAGE_RECEIPT_SCHEMA",
    "GT0_REFERENCE_SCHEMA",
    "GT0ProtocolError",
    "GT0ReferenceError",
    "GT0IntegrityError",
    "GT0PermissionError",
    "GT0StageStatus",
    "GT0ExactRef",
    "GT0ConservationEnvelope",
    "GT0StageReceipt",
    "gt0_content_hash",
    "validate_exact_upstream_ref",
    "assert_permission_narrowing",
]
