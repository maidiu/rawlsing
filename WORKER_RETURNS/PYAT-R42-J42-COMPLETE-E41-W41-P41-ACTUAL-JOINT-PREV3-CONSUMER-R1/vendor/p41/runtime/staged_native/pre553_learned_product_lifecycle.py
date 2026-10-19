"""B5 learned-product lifecycle runtime.

This module implements the project-current
PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0 contract adopted for OBL034.

It owns learned-product lifecycle state only: immutable registration, lifecycle
publication, explicit scope-bound current selection/no-current, supersession,
withdrawal/invalidation, historical replay, rebuild linkage, optional-cache
classification, and recomputable payload GC eligibility.

It deliberately does not own producer semantics, M2 release-core semantics,
AuthoritySnapshot maintenance, consumer permission, source/carrier retirement,
Field Forge admission, or physical architecture selection.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)

LIFECYCLE_CONTRACT_ID = "PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0"
LIFECYCLE_RUNTIME_SCHEMA = "PRE553_B5_LEARNED_PRODUCT_LIFECYCLE_RUNTIME@1.0.0"
LIFECYCLE_CHECKPOINT_SCHEMA = "PRE553_B5_LEARNED_PRODUCT_LIFECYCLE_CHECKPOINT@1.0.0"

PUBLICATION_STATES = frozenset({"UNPUBLISHED", "PUBLISHED"})
SELECTION_STATES = frozenset({
    "NOT_CURRENT",
    "CURRENT_SELECTED",
    "NO_CURRENT",
    "UNKNOWN_CURRENTNESS",
    "CONFLICTING_CURRENT_SELECTION",
})
VALIDITY_STATES = frozenset({"VALID", "INVALIDATED_REBUILD_REQUIRED", "WITHDRAWN"})
REPLAY_STATES = frozenset({
    "REPLAY_COMPLETE",
    "REPLAY_BLOCKED_MISSING_DETERMINANT",
    "REPLAY_BLOCKED_MISSING_AUTHORITY",
    "REPLAY_BLOCKED_MISSING_SOURCE_OR_UPSTREAM",
    "REPLAY_INTEGRITY_FAILURE",
})
REBUILD_STATES = frozenset({
    "REBUILD_NOT_REQUESTED",
    "CURRENT_REBUILD_ELIGIBLE",
    "HISTORICAL_REPLAY_ELIGIBLE",
    "REBUILD_BLOCKED",
})
MATERIALIZATION_CLASSES = frozenset({
    "MANDATORY_RETAINED_CAPITAL",
    "RECOMPUTABLE_PRODUCT_PAYLOAD",
    "OPTIONAL_CACHE_ACCELERATOR",
})

B5_EVENT_KINDS = frozenset({
    "PRODUCT_REGISTERED",
    "PRODUCT_PUBLISHED",
    "CURRENT_SELECTED",
    "CURRENT_SUPERSEDED",
    "CURRENT_CLEARED",
    "PRODUCT_INVALIDATED",
    "PRODUCT_WITHDRAWN",
    "REBUILD_ELIGIBILITY_RECORDED",
    "PRODUCT_REBUILT",
    "CACHE_MATERIALIZED",
    "CACHE_DROPPED",
    "GC_ELIGIBILITY_ATTESTED",
    "RECOMPUTABLE_PAYLOAD_GC_RECORDED",
})

# HQ118 admits these only as B5/P2-conserving M3 record refinements.
# They never mutate B5 orthogonal state or currentness by themselves.
REFINEMENT_EVENT_KINDS = frozenset({
    "RECERTIFIES",
    "CORRECTS",
    "CHANGES_SCOPE_EXPLICITLY",
    "REOPENS",
    "ONTOLOGY_OR_FAMILY_EXPANDS",
})
EVENT_KINDS = B5_EVENT_KINDS | REFINEMENT_EVENT_KINDS

FAIL_CLOSED_STATES = frozenset({
    "AMBIGUOUS_PRODUCT_IDENTITY",
    "MISSING_LIFECYCLE_AUTHORITY",
    "MISSING_SEMANTIC_AUTHORITY",
    "MISSING_REPLAY_CLOSURE",
    "MISSING_DETERMINANT",
    "CONFLICTING_CURRENT_SELECTION",
    "UNKNOWN_CURRENTNESS",
    "INVALIDATED_DEPENDENCY",
    "WITHDRAWN_NO_CURRENT_REPLACEMENT",
    "REBUILD_NOT_PROVED",
    "GC_NOT_AUTHORIZED",
    "SOURCE_OR_CARRIER_RETIREMENT_AUTHORITY_REQUIRED",
    "COMPARABILITY_AUTHORITY_REQUIRED_IF_TRANSFER_CLAIMED",
    "GENERAL_COMPOSITION_AUTHORITY_REQUIRED_IF_BROADER_COMPOSITION_CLAIMED",
})

DETERMINANT_CLASSES = frozenset({
    "SEMANTIC_AUTHORITY_REF",
    "PRODUCER_CONTRACT_REF",
    "SOURCE_ARTIFACT_OR_RELEASE_REF",
    "SOURCE_UNIVERSE_OR_RISK_SET_REF",
    "QUERY_PREDICATE_OR_DISCOVERY_RULE_REF",
    "VALIDATION_AUTHORITY_REF",
    "UPSTREAM_LEARNED_PRODUCT_REF",
    "PUBLICATION_GOVERNANCE_REF",
    "REPLAY_PROTOCOL_REF",
    "SEMANTICALLY_RELEVANT_EXECUTOR_OR_SCHEMA_REF",
})

_FORBIDDEN_SELECTOR_TOKENS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
})
_FORBIDDEN_SUBJECT_KINDS = frozenset({
    "AuthoritySnapshot",
    "AuthoritySnapshot@1.0.0",
    "AuthorityReleaseReceipt",
    "Maintenance:RELEASE",
})


class LearnedProductLifecycleError(ValueError):
    """B5 lifecycle operation is not lawful at the supplied exact grain."""


class LearnedProductLifecycleConflict(LearnedProductLifecycleError):
    """Exact immutable lifecycle/currentness evidence conflicts."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LearnedProductLifecycleError(f"{name} must be a non-empty string")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    text = _text(value, name)
    if (
        len(text) != 64
        or text.lower() != text
        or any(ch not in "0123456789abcdef" for ch in text)
    ):
        raise LearnedProductLifecycleError(f"{name} must be lowercase sha256")
    return text


def _reject_selector_text(value: Any, name: str) -> str:
    text = _text(value, name)
    upper = text.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS:
        raise LearnedProductLifecycleError(
            f"{name} may not use latest/default/fuzzy/nearest/semver selection"
        )
    if upper.startswith(
        ("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:", "SEMVER_FALLBACK:")
    ):
        raise LearnedProductLifecycleError(
            f"{name} may not use mutable/fuzzy selector syntax"
        )
    return text


def _exact(value: ExactRef | Mapping[str, Any], name: str = "ref") -> ExactRef:
    try:
        ref = exact_ref(value, name)
    except Exception as exc:
        raise LearnedProductLifecycleError(str(exc)) from exc
    if ref.kind in _FORBIDDEN_SUBJECT_KINDS:
        raise LearnedProductLifecycleError(
            "AuthoritySnapshot/AuthorityReleaseReceipt cannot alias learned-product refs"
        )
    return ref


def _exact_any(value: ExactRef | Mapping[str, Any], name: str = "ref") -> ExactRef:
    try:
        return exact_ref(value, name)
    except Exception as exc:
        raise LearnedProductLifecycleError(str(exc)) from exc


def _authority(value: AuthorityRef | Mapping[str, Any], name: str = "authority_ref") -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Exception as exc:
        raise LearnedProductLifecycleError(str(exc)) from exc


def _authority_determinant_ref(value: AuthorityRef | Mapping[str, Any]) -> ExactRef:
    """Represent an exact AuthorityRef as a neutral determinant key.

    This is not an AuthoritySnapshot alias and carries no authority-lifecycle
    semantics. It only lets B5 LCR-009 route an exact authority change through
    the product determinant graph.
    """
    ref = _authority(value)
    projection = {"determinant_class": "SEMANTIC_AUTHORITY_REF", "authority_ref": ref.as_dict()}
    digest = semantic_hash(projection)
    return ExactRef(
        "B5Lifecycle:AUTHORITY_DETERMINANT",
        f"urn:rawlsing:pre553:b5-lifecycle:authority-determinant:sha256:{digest}",
        digest,
    )


def _determinant(value: ExactRef | AuthorityRef | Mapping[str, Any]) -> ExactRef:
    if isinstance(value, AuthorityRef):
        return _authority_determinant_ref(value)
    if isinstance(value, Mapping) and set(value) == {
        "authority_id", "authority_version", "authority_content_hash"
    }:
        return _authority_determinant_ref(value)
    return _exact_any(value, "determinant_ref")


def _determinant_refs(
    values: Iterable[ExactRef | AuthorityRef | Mapping[str, Any]]
) -> tuple[ExactRef, ...]:
    refs = {_determinant(value).key: _determinant(value) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _exact_refs(values: Iterable[ExactRef | Mapping[str, Any]], *, allow_authority_kind: bool = False) -> tuple[ExactRef, ...]:
    parser = _exact_any if allow_authority_kind else _exact
    refs = {parser(value).key: parser(value) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _authority_refs(values: Iterable[AuthorityRef | Mapping[str, Any]]) -> tuple[AuthorityRef, ...]:
    refs = {_authority(value).key: _authority(value) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _optional_exact(value: ExactRef | Mapping[str, Any] | None, *, allow_authority_kind: bool = False) -> ExactRef | None:
    if value is None:
        return None
    return (_exact_any if allow_authority_kind else _exact)(value)


def _ref_dict(value: ExactRef | None) -> Mapping[str, Any] | None:
    return None if value is None else value.as_dict()


def _record_ref(kind: str, projection: Mapping[str, Any]) -> ExactRef:
    digest = semantic_hash(projection)
    return ExactRef(
        f"B5Lifecycle:{kind}",
        f"urn:rawlsing:pre553:b5-lifecycle:{kind.lower()}:sha256:{digest}",
        digest,
    )


def _validate_embedded_ref(data: Mapping[str, Any], expected: ExactRef, field: str = "record_ref") -> None:
    supplied = data.get(field)
    if supplied is not None and _exact_any(supplied, field) != expected:
        raise LearnedProductLifecycleConflict(
            f"{field} does not match deterministic lifecycle identity"
        )


@runtime_checkable
class LearnedProductReleaseProtocol(Protocol):
    """Narrow exact-ref interface that a later M2 ReleaseCore adapter may satisfy.

    This protocol defines only B5-consumed identity/closure fields. It does not
    define or implement M2 release semantics.
    """

    @property
    def release_ref(self) -> ExactRef: ...

    @property
    def product_ref(self) -> ExactRef: ...

    @property
    def product_family_ref(self) -> ExactRef: ...

    @property
    def producer_owner_ref(self) -> ExactRef: ...

    @property
    def producer_contract_ref(self) -> ExactRef: ...

    @property
    def semantic_projection_hash(self) -> str: ...

    @property
    def authority_snapshot_refs(self) -> tuple[AuthorityRef, ...]: ...

    @property
    def direct_dependency_refs(self) -> tuple[ExactRef, ...]: ...

    @property
    def determinant_refs(self) -> tuple[ExactRef, ...]: ...

    @property
    def determinant_set_hash(self) -> str: ...

    @property
    def replay_root_ref(self) -> ExactRef: ...

    @property
    def selection_scope_ref(self) -> ExactRef: ...

    @property
    def build_or_release_receipt_refs(self) -> tuple[ExactRef, ...]: ...

    @property
    def producer_permission_ceiling_ref(self) -> ExactRef: ...


@dataclass(frozen=True)
class LearnedProductLifecycleSubject:
    """Opaque exact release/product view consumed by B5.

    This is not an M2 ReleaseCore implementation. It is the minimum B5-side
    adapter surface required by the adopted lifecycle identity law.
    """

    release_ref: ExactRef
    product_ref: ExactRef
    product_family_ref: ExactRef
    producer_owner_ref: ExactRef
    producer_contract_ref: ExactRef
    semantic_projection_hash: str
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    direct_dependency_refs: tuple[ExactRef, ...]
    determinant_refs: tuple[ExactRef, ...]
    determinant_set_hash: str
    replay_root_ref: ExactRef
    selection_scope_ref: ExactRef
    build_or_release_receipt_refs: tuple[ExactRef, ...]
    producer_permission_ceiling_ref: ExactRef
    replay_state: str = "REPLAY_COMPLETE"
    rebuild_state: str = "REBUILD_NOT_REQUESTED"
    materialization_class: str = "MANDATORY_RETAINED_CAPITAL"

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref, "release_ref"))
        object.__setattr__(self, "product_ref", _exact(self.product_ref, "product_ref"))
        object.__setattr__(
            self, "product_family_ref", _exact(self.product_family_ref, "product_family_ref")
        )
        object.__setattr__(
            self, "producer_owner_ref", _exact(self.producer_owner_ref, "producer_owner_ref")
        )
        object.__setattr__(
            self,
            "producer_contract_ref",
            _exact(self.producer_contract_ref, "producer_contract_ref"),
        )
        object.__setattr__(
            self, "semantic_projection_hash", _sha(self.semantic_projection_hash, "semantic_projection_hash")
        )
        auths = _authority_refs(self.authority_snapshot_refs)
        if not auths:
            raise LearnedProductLifecycleError(
                "learned-product lifecycle subject requires exact AuthoritySnapshot refs"
            )
        object.__setattr__(self, "authority_snapshot_refs", auths)
        object.__setattr__(
            self, "direct_dependency_refs", _exact_refs(self.direct_dependency_refs)
        )
        dets = _exact_refs(self.determinant_refs, allow_authority_kind=True)
        if not dets:
            raise LearnedProductLifecycleError("determinant_refs must not be empty")
        object.__setattr__(self, "determinant_refs", dets)
        supplied_det_hash = _sha(self.determinant_set_hash, "determinant_set_hash")
        expected_det_hash = semantic_hash([ref.as_dict() for ref in dets])
        if supplied_det_hash != expected_det_hash:
            raise LearnedProductLifecycleError(
                "determinant_set_hash does not match exact determinant refs"
            )
        object.__setattr__(self, "determinant_set_hash", supplied_det_hash)
        object.__setattr__(self, "replay_root_ref", _exact(self.replay_root_ref, "replay_root_ref"))
        object.__setattr__(
            self, "selection_scope_ref", _exact(self.selection_scope_ref, "selection_scope_ref")
        )
        receipts = _exact_refs(self.build_or_release_receipt_refs)
        if not receipts:
            raise LearnedProductLifecycleError(
                "build_or_release_receipt_refs must not be empty"
            )
        object.__setattr__(self, "build_or_release_receipt_refs", receipts)
        object.__setattr__(
            self,
            "producer_permission_ceiling_ref",
            _exact(self.producer_permission_ceiling_ref, "producer_permission_ceiling_ref"),
        )
        if self.replay_state not in REPLAY_STATES:
            raise LearnedProductLifecycleError("unknown B5 replay_state")
        if self.rebuild_state not in REBUILD_STATES:
            raise LearnedProductLifecycleError("unknown B5 rebuild_state")
        if self.materialization_class not in MATERIALIZATION_CLASSES:
            raise LearnedProductLifecycleError("unknown B5 materialization_class")

    @classmethod
    def from_protocol(cls, value: LearnedProductReleaseProtocol, **overrides: Any) -> "LearnedProductLifecycleSubject":
        if not isinstance(value, LearnedProductReleaseProtocol):
            # Runtime-checkable protocol only verifies attribute presence.
            raise LearnedProductLifecycleError(
                "M2 adapter does not expose the exact B5 lifecycle protocol"
            )
        data = {
            "release_ref": value.release_ref,
            "product_ref": value.product_ref,
            "product_family_ref": value.product_family_ref,
            "producer_owner_ref": value.producer_owner_ref,
            "producer_contract_ref": value.producer_contract_ref,
            "semantic_projection_hash": value.semantic_projection_hash,
            "authority_snapshot_refs": tuple(value.authority_snapshot_refs),
            "direct_dependency_refs": tuple(value.direct_dependency_refs),
            "determinant_refs": tuple(value.determinant_refs),
            "determinant_set_hash": value.determinant_set_hash,
            "replay_root_ref": value.replay_root_ref,
            "selection_scope_ref": value.selection_scope_ref,
            "build_or_release_receipt_refs": tuple(value.build_or_release_receipt_refs),
            "producer_permission_ceiling_ref": value.producer_permission_ceiling_ref,
        }
        data.update(overrides)
        return cls(**data)

    def as_dict(self) -> dict[str, Any]:
        return {
            "release_ref": self.release_ref.as_dict(),
            "product_ref": self.product_ref.as_dict(),
            "product_family_ref": self.product_family_ref.as_dict(),
            "producer_owner_ref": self.producer_owner_ref.as_dict(),
            "producer_contract_ref": self.producer_contract_ref.as_dict(),
            "semantic_projection_hash": self.semantic_projection_hash,
            "authority_snapshot_refs": [ref.as_dict() for ref in self.authority_snapshot_refs],
            "direct_dependency_refs": [ref.as_dict() for ref in self.direct_dependency_refs],
            "determinant_refs": [ref.as_dict() for ref in self.determinant_refs],
            "determinant_set_hash": self.determinant_set_hash,
            "replay_root_ref": self.replay_root_ref.as_dict(),
            "selection_scope_ref": self.selection_scope_ref.as_dict(),
            "build_or_release_receipt_refs": [
                ref.as_dict() for ref in self.build_or_release_receipt_refs
            ],
            "producer_permission_ceiling_ref": self.producer_permission_ceiling_ref.as_dict(),
            "replay_state": self.replay_state,
            "rebuild_state": self.rebuild_state,
            "materialization_class": self.materialization_class,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LearnedProductLifecycleSubject":
        return cls(
            release_ref=_exact(data["release_ref"]),
            product_ref=_exact(data["product_ref"]),
            product_family_ref=_exact(data["product_family_ref"]),
            producer_owner_ref=_exact(data["producer_owner_ref"]),
            producer_contract_ref=_exact(data["producer_contract_ref"]),
            semantic_projection_hash=data["semantic_projection_hash"],
            authority_snapshot_refs=tuple(_authority(x) for x in data["authority_snapshot_refs"]),
            direct_dependency_refs=tuple(_exact(x) for x in data.get("direct_dependency_refs", ())),
            determinant_refs=tuple(
                _exact_any(x) for x in data.get("determinant_refs", ())
            ),
            determinant_set_hash=data["determinant_set_hash"],
            replay_root_ref=_exact(data["replay_root_ref"]),
            selection_scope_ref=_exact(data["selection_scope_ref"]),
            build_or_release_receipt_refs=tuple(
                _exact(x) for x in data["build_or_release_receipt_refs"]
            ),
            producer_permission_ceiling_ref=_exact(data["producer_permission_ceiling_ref"]),
            replay_state=data.get("replay_state", "REPLAY_COMPLETE"),
            rebuild_state=data.get("rebuild_state", "REBUILD_NOT_REQUESTED"),
            materialization_class=data.get(
                "materialization_class", "MANDATORY_RETAINED_CAPITAL"
            ),
        )


@dataclass(frozen=True)
class SelectionKey:
    product_family_ref: ExactRef
    selection_scope_ref: ExactRef
    selection_purpose_ref: ExactRef
    consumer_context_partition_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "product_family_ref", _exact(self.product_family_ref, "product_family_ref")
        )
        object.__setattr__(
            self, "selection_scope_ref", _exact(self.selection_scope_ref, "selection_scope_ref")
        )
        object.__setattr__(
            self,
            "selection_purpose_ref",
            _exact(self.selection_purpose_ref, "selection_purpose_ref"),
        )
        object.__setattr__(
            self,
            "consumer_context_partition_ref",
            _optional_exact(self.consumer_context_partition_ref),
        )

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "SelectionKey",
            "product_family_ref": self.product_family_ref.as_dict(),
            "selection_scope_ref": self.selection_scope_ref.as_dict(),
            "selection_purpose_ref": self.selection_purpose_ref.as_dict(),
            "consumer_context_partition_ref": _ref_dict(
                self.consumer_context_partition_ref
            ),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("SELECTION_KEY", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SelectionKey":
        obj = cls(
            product_family_ref=_exact(data["product_family_ref"]),
            selection_scope_ref=_exact(data["selection_scope_ref"]),
            selection_purpose_ref=_exact(data["selection_purpose_ref"]),
            consumer_context_partition_ref=_optional_exact(
                data.get("consumer_context_partition_ref")
            ),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class LearnedProductLifecycleEvent:
    ordinal: int
    event_kind: str
    release_ref: ExactRef
    product_ref: ExactRef
    selection_scope_ref: ExactRef
    event_authority_ref: ExactRef
    event_rule_ref: ExactRef
    parent_lifecycle_event_ref: ExactRef | None
    evidence_refs: tuple[ExactRef, ...] = ()
    payload: Mapping[str, Any] | None = None
    event_state: str = "COMMITTED"

    def __post_init__(self) -> None:
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 1:
            raise LearnedProductLifecycleError("event ordinal must be a positive integer")
        if self.event_kind not in EVENT_KINDS:
            raise LearnedProductLifecycleError(f"unknown lifecycle event kind {self.event_kind!r}")
        object.__setattr__(self, "release_ref", _exact(self.release_ref, "release_ref"))
        object.__setattr__(self, "product_ref", _exact(self.product_ref, "product_ref"))
        object.__setattr__(
            self, "selection_scope_ref", _exact(self.selection_scope_ref, "selection_scope_ref")
        )
        object.__setattr__(
            self, "event_authority_ref", _exact(self.event_authority_ref, "event_authority_ref")
        )
        object.__setattr__(self, "event_rule_ref", _exact(self.event_rule_ref, "event_rule_ref"))
        object.__setattr__(
            self,
            "parent_lifecycle_event_ref",
            _optional_exact(self.parent_lifecycle_event_ref, allow_authority_kind=True),
        )
        object.__setattr__(
            self, "evidence_refs", _exact_refs(self.evidence_refs, allow_authority_kind=True)
        )
        normalized = canonicalize(dict(self.payload or {}))
        if not isinstance(normalized, dict):
            raise LearnedProductLifecycleError("event payload must canonicalize to a mapping")
        object.__setattr__(self, "payload", normalized)
        if self.event_state != "COMMITTED":
            raise LearnedProductLifecycleError("lifecycle event_state must be COMMITTED")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "LearnedProductLifecycleEvent",
            "ordinal": self.ordinal,
            "event_kind": self.event_kind,
            "product_ref": self.product_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "selection_scope_ref": self.selection_scope_ref.as_dict(),
            "event_authority_ref": self.event_authority_ref.as_dict(),
            "event_rule_ref": self.event_rule_ref.as_dict(),
            "parent_lifecycle_event_ref": _ref_dict(self.parent_lifecycle_event_ref),
            "evidence_refs": [ref.as_dict() for ref in self.evidence_refs],
            "payload": dict(self.payload or {}),
            "event_state": self.event_state,
        }

    @property
    def event_content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            "B5Lifecycle:EVENT",
            f"urn:rawlsing:pre553:b5-lifecycle:event:sha256:{self.event_content_hash}",
            self.event_content_hash,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.semantic_projection(),
            "event_content_hash": self.event_content_hash,
            "record_ref": self.ref.as_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LearnedProductLifecycleEvent":
        obj = cls(
            ordinal=data["ordinal"],
            event_kind=data["event_kind"],
            release_ref=_exact(data["release_ref"]),
            product_ref=_exact(data["product_ref"]),
            selection_scope_ref=_exact(data["selection_scope_ref"]),
            event_authority_ref=_exact(data["event_authority_ref"]),
            event_rule_ref=_exact(data["event_rule_ref"]),
            parent_lifecycle_event_ref=_optional_exact(
                data.get("parent_lifecycle_event_ref"), allow_authority_kind=True
            ),
            evidence_refs=tuple(
                _exact_any(x) for x in data.get("evidence_refs", ())
            ),
            payload=data.get("payload", {}),
            event_state=data.get("event_state", "COMMITTED"),
        )
        if data.get("event_content_hash", obj.event_content_hash) != obj.event_content_hash:
            raise LearnedProductLifecycleConflict("event_content_hash mismatch")
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class CurrentSelectionReceipt:
    selection_key_ref: ExactRef
    selected_release_ref: ExactRef
    current_select_event_ref: ExactRef
    previous_selection_receipt_ref: ExactRef | None
    selection_authority_refs: tuple[ExactRef, ...]
    selection_attestation_refs: tuple[ExactRef, ...]
    determinant_snapshot_ref: ExactRef
    receipt_state: str = "CURRENT_SELECTED"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "selection_key_ref", _exact(self.selection_key_ref, "selection_key_ref")
        )
        object.__setattr__(
            self, "selected_release_ref", _exact(self.selected_release_ref, "selected_release_ref")
        )
        object.__setattr__(
            self,
            "current_select_event_ref",
            _exact_any(self.current_select_event_ref, "current_select_event_ref"),
        )
        object.__setattr__(
            self,
            "previous_selection_receipt_ref",
            _optional_exact(
                self.previous_selection_receipt_ref, allow_authority_kind=True
            ),
        )
        auths = _exact_refs(self.selection_authority_refs)
        atts = _exact_refs(self.selection_attestation_refs)
        if not auths or not atts:
            raise LearnedProductLifecycleError(
                "current selection requires exact authority and attestation refs"
            )
        object.__setattr__(self, "selection_authority_refs", auths)
        object.__setattr__(self, "selection_attestation_refs", atts)
        object.__setattr__(
            self,
            "determinant_snapshot_ref",
            _exact_any(self.determinant_snapshot_ref, "determinant_snapshot_ref"),
        )
        if self.receipt_state != "CURRENT_SELECTED":
            raise LearnedProductLifecycleError("receipt_state must be CURRENT_SELECTED")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "CurrentSelectionReceipt",
            "selection_key_ref": self.selection_key_ref.as_dict(),
            "selected_release_ref": self.selected_release_ref.as_dict(),
            "current_select_event_ref": self.current_select_event_ref.as_dict(),
            "previous_selection_receipt_ref": _ref_dict(
                self.previous_selection_receipt_ref
            ),
            "selection_authority_refs": [
                ref.as_dict() for ref in self.selection_authority_refs
            ],
            "selection_attestation_refs": [
                ref.as_dict() for ref in self.selection_attestation_refs
            ],
            "determinant_snapshot_ref": self.determinant_snapshot_ref.as_dict(),
            "receipt_state": self.receipt_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("CURRENT_SELECTION", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CurrentSelectionReceipt":
        obj = cls(
            selection_key_ref=_exact(data["selection_key_ref"]),
            selected_release_ref=_exact(data["selected_release_ref"]),
            current_select_event_ref=_exact_any(data["current_select_event_ref"]),
            previous_selection_receipt_ref=_optional_exact(
                data.get("previous_selection_receipt_ref"), allow_authority_kind=True
            ),
            selection_authority_refs=tuple(
                _exact(x) for x in data["selection_authority_refs"]
            ),
            selection_attestation_refs=tuple(
                _exact(x) for x in data["selection_attestation_refs"]
            ),
            determinant_snapshot_ref=_exact_any(data["determinant_snapshot_ref"]),
            receipt_state=data.get("receipt_state", "CURRENT_SELECTED"),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class NoCurrentReceipt:
    selection_key_ref: ExactRef
    no_current_event_ref: ExactRef
    previous_selection_receipt_ref: ExactRef | None
    selection_authority_refs: tuple[ExactRef, ...]
    selection_attestation_refs: tuple[ExactRef, ...]
    reason_ref: ExactRef
    receipt_state: str = "NO_CURRENT"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "selection_key_ref", _exact(self.selection_key_ref, "selection_key_ref")
        )
        object.__setattr__(
            self,
            "no_current_event_ref",
            _exact_any(self.no_current_event_ref, "no_current_event_ref"),
        )
        object.__setattr__(
            self,
            "previous_selection_receipt_ref",
            _optional_exact(
                self.previous_selection_receipt_ref, allow_authority_kind=True
            ),
        )
        auths = _exact_refs(self.selection_authority_refs)
        atts = _exact_refs(self.selection_attestation_refs)
        if not auths or not atts:
            raise LearnedProductLifecycleError(
                "NO_CURRENT requires exact authority and attestation refs"
            )
        object.__setattr__(self, "selection_authority_refs", auths)
        object.__setattr__(self, "selection_attestation_refs", atts)
        object.__setattr__(self, "reason_ref", _exact(self.reason_ref, "reason_ref"))
        if self.receipt_state != "NO_CURRENT":
            raise LearnedProductLifecycleError("receipt_state must be NO_CURRENT")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "NoCurrentReceipt",
            "selection_key_ref": self.selection_key_ref.as_dict(),
            "no_current_event_ref": self.no_current_event_ref.as_dict(),
            "previous_selection_receipt_ref": _ref_dict(
                self.previous_selection_receipt_ref
            ),
            "selection_authority_refs": [
                ref.as_dict() for ref in self.selection_authority_refs
            ],
            "selection_attestation_refs": [
                ref.as_dict() for ref in self.selection_attestation_refs
            ],
            "reason_ref": self.reason_ref.as_dict(),
            "receipt_state": self.receipt_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("NO_CURRENT", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "NoCurrentReceipt":
        obj = cls(
            selection_key_ref=_exact(data["selection_key_ref"]),
            no_current_event_ref=_exact_any(data["no_current_event_ref"]),
            previous_selection_receipt_ref=_optional_exact(
                data.get("previous_selection_receipt_ref"), allow_authority_kind=True
            ),
            selection_authority_refs=tuple(
                _exact(x) for x in data["selection_authority_refs"]
            ),
            selection_attestation_refs=tuple(
                _exact(x) for x in data["selection_attestation_refs"]
            ),
            reason_ref=_exact(data["reason_ref"]),
            receipt_state=data.get("receipt_state", "NO_CURRENT"),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class InvalidationReceipt:
    changed_determinant_refs: tuple[ExactRef, ...]
    directly_affected_release_refs: tuple[ExactRef, ...]
    transitively_affected_release_refs: tuple[ExactRef, ...]
    affected_product_refs: tuple[ExactRef, ...]
    unaffected_product_refs: tuple[ExactRef, ...]
    dependency_closure_receipt_ref: ExactRef
    invalidation_event_refs: tuple[ExactRef, ...]
    receipt_state: str = "INVALIDATED_DEPENDENCY"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "changed_determinant_refs",
            _exact_refs(self.changed_determinant_refs, allow_authority_kind=True),
        )
        object.__setattr__(
            self, "directly_affected_release_refs", _exact_refs(self.directly_affected_release_refs)
        )
        object.__setattr__(
            self,
            "transitively_affected_release_refs",
            _exact_refs(self.transitively_affected_release_refs),
        )
        object.__setattr__(self, "affected_product_refs", _exact_refs(self.affected_product_refs))
        object.__setattr__(
            self, "unaffected_product_refs", _exact_refs(self.unaffected_product_refs)
        )
        object.__setattr__(
            self,
            "dependency_closure_receipt_ref",
            _exact_any(self.dependency_closure_receipt_ref),
        )
        object.__setattr__(
            self,
            "invalidation_event_refs",
            _exact_refs(self.invalidation_event_refs, allow_authority_kind=True),
        )
        if self.receipt_state != "INVALIDATED_DEPENDENCY":
            raise LearnedProductLifecycleError(
                "invalidation receipt_state must be INVALIDATED_DEPENDENCY"
            )

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "InvalidationReceipt",
            "changed_determinant_refs": [
                ref.as_dict() for ref in self.changed_determinant_refs
            ],
            "directly_affected_release_refs": [
                ref.as_dict() for ref in self.directly_affected_release_refs
            ],
            "transitively_affected_release_refs": [
                ref.as_dict() for ref in self.transitively_affected_release_refs
            ],
            "affected_product_refs": [ref.as_dict() for ref in self.affected_product_refs],
            "unaffected_product_refs": [
                ref.as_dict() for ref in self.unaffected_product_refs
            ],
            "dependency_closure_receipt_ref": self.dependency_closure_receipt_ref.as_dict(),
            "invalidation_event_refs": [
                ref.as_dict() for ref in self.invalidation_event_refs
            ],
            "receipt_state": self.receipt_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("INVALIDATION", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "InvalidationReceipt":
        obj = cls(
            changed_determinant_refs=tuple(
                _exact_any(x) for x in data["changed_determinant_refs"]
            ),
            directly_affected_release_refs=tuple(
                _exact(x) for x in data["directly_affected_release_refs"]
            ),
            transitively_affected_release_refs=tuple(
                _exact(x) for x in data["transitively_affected_release_refs"]
            ),
            affected_product_refs=tuple(_exact(x) for x in data["affected_product_refs"]),
            unaffected_product_refs=tuple(
                _exact(x) for x in data["unaffected_product_refs"]
            ),
            dependency_closure_receipt_ref=_exact_any(
                data["dependency_closure_receipt_ref"]
            ),
            invalidation_event_refs=tuple(
                _exact_any(x) for x in data["invalidation_event_refs"]
            ),
            receipt_state=data.get("receipt_state", "INVALIDATED_DEPENDENCY"),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class RebuildEligibilityReceipt:
    release_ref: ExactRef
    rebuild_state: str
    blocker_states: tuple[str, ...]
    reconstruction_input_refs: tuple[ExactRef, ...]
    execution_mechanism_ref: ExactRef | None
    event_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref))
        if self.rebuild_state not in REBUILD_STATES - {"REBUILD_NOT_REQUESTED"}:
            raise LearnedProductLifecycleError("invalid recorded rebuild state")
        blockers = tuple(sorted({_text(x, "blocker_state") for x in self.blocker_states}))
        for blocker in blockers:
            if blocker not in FAIL_CLOSED_STATES:
                raise LearnedProductLifecycleError("unknown typed rebuild blocker")
        object.__setattr__(self, "blocker_states", blockers)
        object.__setattr__(
            self,
            "reconstruction_input_refs",
            _exact_refs(self.reconstruction_input_refs, allow_authority_kind=True),
        )
        object.__setattr__(
            self,
            "execution_mechanism_ref",
            _optional_exact(self.execution_mechanism_ref, allow_authority_kind=True),
        )
        object.__setattr__(self, "event_ref", _exact_any(self.event_ref))
        if self.rebuild_state == "REBUILD_BLOCKED" and not blockers:
            raise LearnedProductLifecycleError("REBUILD_BLOCKED requires typed blocker")
        if self.rebuild_state != "REBUILD_BLOCKED" and blockers:
            raise LearnedProductLifecycleError(
                "eligible rebuild receipt may not carry blocker states"
            )

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "RebuildEligibilityReceipt",
            "release_ref": self.release_ref.as_dict(),
            "rebuild_state": self.rebuild_state,
            "blocker_states": list(self.blocker_states),
            "reconstruction_input_refs": [
                ref.as_dict() for ref in self.reconstruction_input_refs
            ],
            "execution_mechanism_ref": _ref_dict(self.execution_mechanism_ref),
            "event_ref": self.event_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("REBUILD_ELIGIBILITY", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RebuildEligibilityReceipt":
        obj = cls(
            release_ref=_exact(data["release_ref"]),
            rebuild_state=data["rebuild_state"],
            blocker_states=tuple(data.get("blocker_states", ())),
            reconstruction_input_refs=tuple(
                _exact_any(x) for x in data.get("reconstruction_input_refs", ())
            ),
            execution_mechanism_ref=_optional_exact(
                data.get("execution_mechanism_ref"), allow_authority_kind=True
            ),
            event_ref=_exact_any(data["event_ref"]),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class RebuildLinkReceipt:
    old_release_ref: ExactRef
    new_release_ref: ExactRef | None
    rebuild_state: str
    rebuild_determinant_set_hash: str
    replay_or_execution_receipt_ref: ExactRef
    event_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "old_release_ref", _exact(self.old_release_ref))
        object.__setattr__(self, "new_release_ref", _optional_exact(self.new_release_ref))
        if self.rebuild_state not in {
            "REBUILT",
            "REBUILD_REQUIRED",
            "REBUILD_NOT_REQUIRED",
            "REBUILD_BLOCKED",
            "REBUILD_OUT_OF_SCOPE",
        }:
            raise LearnedProductLifecycleError("unknown rebuild-link state")
        if self.rebuild_state == "REBUILT" and self.new_release_ref is None:
            raise LearnedProductLifecycleError("REBUILT requires exact new_release_ref")
        if self.rebuild_state != "REBUILT" and self.new_release_ref is not None:
            raise LearnedProductLifecycleError(
                "only REBUILT may carry a new_release_ref"
            )
        object.__setattr__(
            self,
            "rebuild_determinant_set_hash",
            _sha(self.rebuild_determinant_set_hash, "rebuild_determinant_set_hash"),
        )
        object.__setattr__(
            self,
            "replay_or_execution_receipt_ref",
            _exact(self.replay_or_execution_receipt_ref),
        )
        object.__setattr__(self, "event_ref", _exact_any(self.event_ref))

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "RebuildLinkReceipt",
            "old_release_ref": self.old_release_ref.as_dict(),
            "new_release_ref": _ref_dict(self.new_release_ref),
            "rebuild_state": self.rebuild_state,
            "rebuild_determinant_set_hash": self.rebuild_determinant_set_hash,
            "replay_or_execution_receipt_ref": self.replay_or_execution_receipt_ref.as_dict(),
            "event_ref": self.event_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("REBUILD_LINK", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RebuildLinkReceipt":
        obj = cls(
            old_release_ref=_exact(data["old_release_ref"]),
            new_release_ref=_optional_exact(data.get("new_release_ref")),
            rebuild_state=data["rebuild_state"],
            rebuild_determinant_set_hash=data["rebuild_determinant_set_hash"],
            replay_or_execution_receipt_ref=_exact(
                data["replay_or_execution_receipt_ref"]
            ),
            event_ref=_exact_any(data["event_ref"]),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class GCElegibilityReceipt:
    release_ref: ExactRef
    materialization_class: str
    reconstruction_proof_ref: ExactRef
    historical_retention_proof_ref: ExactRef
    serving_reconstruction_proof_ref: ExactRef
    downstream_byte_dependency_absence_proof_ref: ExactRef
    source_carrier_retention_proof_ref: ExactRef
    source_carrier_retirement_authorized_false: bool
    event_ref: ExactRef
    eligibility_state: str = "GC_ELIGIBLE"

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref))
        if self.materialization_class != "RECOMPUTABLE_PRODUCT_PAYLOAD":
            raise LearnedProductLifecycleError(
                "GC eligibility is limited to RECOMPUTABLE_PRODUCT_PAYLOAD"
            )
        for name in (
            "reconstruction_proof_ref",
            "historical_retention_proof_ref",
            "serving_reconstruction_proof_ref",
            "downstream_byte_dependency_absence_proof_ref",
            "source_carrier_retention_proof_ref",
        ):
            object.__setattr__(self, name, _exact(getattr(self, name), name))
        if self.source_carrier_retirement_authorized_false is not True:
            raise LearnedProductLifecycleError(
                "B5 GC cannot authorize source/carrier retirement"
            )
        object.__setattr__(self, "event_ref", _exact_any(self.event_ref))
        if self.eligibility_state != "GC_ELIGIBLE":
            raise LearnedProductLifecycleError("eligibility_state must be GC_ELIGIBLE")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "GCElegibilityReceipt",
            "release_ref": self.release_ref.as_dict(),
            "materialization_class": self.materialization_class,
            "reconstruction_proof_ref": self.reconstruction_proof_ref.as_dict(),
            "historical_retention_proof_ref": self.historical_retention_proof_ref.as_dict(),
            "serving_reconstruction_proof_ref": self.serving_reconstruction_proof_ref.as_dict(),
            "downstream_byte_dependency_absence_proof_ref": (
                self.downstream_byte_dependency_absence_proof_ref.as_dict()
            ),
            "source_carrier_retention_proof_ref": (
                self.source_carrier_retention_proof_ref.as_dict()
            ),
            "source_carrier_retirement_authorized_false": True,
            "event_ref": self.event_ref.as_dict(),
            "eligibility_state": self.eligibility_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("GC_ELIGIBILITY", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GCElegibilityReceipt":
        obj = cls(
            release_ref=_exact(data["release_ref"]),
            materialization_class=data["materialization_class"],
            reconstruction_proof_ref=_exact(data["reconstruction_proof_ref"]),
            historical_retention_proof_ref=_exact(
                data["historical_retention_proof_ref"]
            ),
            serving_reconstruction_proof_ref=_exact(
                data["serving_reconstruction_proof_ref"]
            ),
            downstream_byte_dependency_absence_proof_ref=_exact(
                data["downstream_byte_dependency_absence_proof_ref"]
            ),
            source_carrier_retention_proof_ref=_exact(
                data["source_carrier_retention_proof_ref"]
            ),
            source_carrier_retirement_authorized_false=data[
                "source_carrier_retirement_authorized_false"
            ],
            event_ref=_exact_any(data["event_ref"]),
            eligibility_state=data.get("eligibility_state", "GC_ELIGIBLE"),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class LifecycleState:
    release_ref: ExactRef
    publication: str
    validity: str
    replay: str
    rebuild: str
    materialization_class: str
    payload_materialized: bool
    registered: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref))
        if self.publication not in PUBLICATION_STATES:
            raise LearnedProductLifecycleError("invalid publication state")
        if self.validity not in VALIDITY_STATES:
            raise LearnedProductLifecycleError("invalid validity state")
        if self.replay not in REPLAY_STATES:
            raise LearnedProductLifecycleError("invalid replay state")
        if self.rebuild not in REBUILD_STATES:
            raise LearnedProductLifecycleError("invalid rebuild state")
        if self.materialization_class not in MATERIALIZATION_CLASSES:
            raise LearnedProductLifecycleError("invalid materialization class")


@dataclass(frozen=True)
class SelectionResolution:
    selection_key_ref: ExactRef
    state: str
    selected_release_ref: ExactRef | None
    receipt_ref: ExactRef | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "selection_key_ref", _exact(self.selection_key_ref))
        if self.state not in SELECTION_STATES:
            raise LearnedProductLifecycleError("invalid selection resolution state")
        object.__setattr__(self, "selected_release_ref", _optional_exact(self.selected_release_ref))
        object.__setattr__(
            self,
            "receipt_ref",
            _optional_exact(self.receipt_ref, allow_authority_kind=True),
        )


@dataclass(frozen=True)
class LearnedProductDeterminantGraph:
    determinant_edges: tuple[tuple[ExactRef, ExactRef], ...] = ()
    dependency_edges: tuple[tuple[ExactRef, ExactRef], ...] = ()
    known_release_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        det: dict[str, tuple[ExactRef, ExactRef]] = {}
        for raw_det, raw_release in self.determinant_edges:
            determinant = _exact_any(raw_det)
            release = _exact(raw_release)
            det[f"{determinant.key}->{release.key}"] = (determinant, release)
        deps: dict[str, tuple[ExactRef, ExactRef]] = {}
        for raw_parent, raw_child in self.dependency_edges:
            parent, child = _exact(raw_parent), _exact(raw_child)
            if parent == child:
                raise LearnedProductLifecycleError("learned-product dependency graph may not self-loop")
            deps[f"{parent.key}->{child.key}"] = (parent, child)
        known = {ref.key: ref for ref in _exact_refs(self.known_release_refs)}
        for _, release in det.values():
            known[release.key] = release
        for parent, child in deps.values():
            known[parent.key] = parent
            known[child.key] = child
        object.__setattr__(
            self, "determinant_edges", tuple(det[key] for key in sorted(det))
        )
        object.__setattr__(
            self, "dependency_edges", tuple(deps[key] for key in sorted(deps))
        )
        object.__setattr__(
            self, "known_release_refs", tuple(known[key] for key in sorted(known))
        )

    @classmethod
    def from_subjects(
        cls, subjects: Iterable[LearnedProductLifecycleSubject]
    ) -> "LearnedProductDeterminantGraph":
        items = tuple(subjects)
        by_release = {item.release_ref.key: item.release_ref for item in items}
        by_product = {item.product_ref.key: item.release_ref for item in items}
        determinant_edges: list[tuple[ExactRef, ExactRef]] = []
        dependency_edges: list[tuple[ExactRef, ExactRef]] = []
        for item in items:
            authority_determinants = tuple(
                _authority_determinant_ref(ref) for ref in item.authority_snapshot_refs
            )
            seen: dict[str, ExactRef] = {
                ref.key: ref for ref in (
                    tuple(item.determinant_refs)
                    + tuple(item.direct_dependency_refs)
                    + authority_determinants
                )
            }
            for ref in seen.values():
                determinant_edges.append((ref, item.release_ref))
            for dep in item.direct_dependency_refs:
                parent = by_release.get(dep.key) or by_product.get(dep.key)
                if parent is not None and parent != item.release_ref:
                    dependency_edges.append((parent, item.release_ref))
        return cls(
            determinant_edges=tuple(determinant_edges),
            dependency_edges=tuple(dependency_edges),
            known_release_refs=tuple(item.release_ref for item in items),
        )

    def affected(
        self,
        changed_refs: Iterable[ExactRef | AuthorityRef | Mapping[str, Any]],
    ) -> tuple[tuple[ExactRef, ...], tuple[ExactRef, ...]]:
        changed = {ref.key for ref in _determinant_refs(changed_refs)}
        direct = {
            release.key: release
            for determinant, release in self.determinant_edges
            if determinant.key in changed
        }
        adjacency: dict[str, list[ExactRef]] = {}
        for parent, child in self.dependency_edges:
            adjacency.setdefault(parent.key, []).append(child)
        all_affected = dict(direct)
        queue = [direct[key] for key in sorted(direct)]
        while queue:
            parent = queue.pop(0)
            for child in sorted(adjacency.get(parent.key, ()), key=lambda ref: ref.key):
                if child.key not in all_affected:
                    all_affected[child.key] = child
                    queue.append(child)
        transitive = {
            key: ref for key, ref in all_affected.items() if key not in direct
        }
        return (
            tuple(direct[key] for key in sorted(direct)),
            tuple(transitive[key] for key in sorted(transitive)),
        )

    def unaffected(self, affected: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
        keys = {ref.key for ref in _exact_refs(affected)}
        return tuple(ref for ref in self.known_release_refs if ref.key not in keys)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "LearnedProductDeterminantGraph",
            "determinant_edges": [
                {
                    "determinant_ref": determinant.as_dict(),
                    "dependent_release_ref": release.as_dict(),
                }
                for determinant, release in self.determinant_edges
            ],
            "dependency_edges": [
                {
                    "parent_release_ref": parent.as_dict(),
                    "child_release_ref": child.as_dict(),
                }
                for parent, child in self.dependency_edges
            ],
            "known_release_refs": [ref.as_dict() for ref in self.known_release_refs],
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("DETERMINANT_GRAPH", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LearnedProductDeterminantGraph":
        obj = cls(
            determinant_edges=tuple(
                (
                    _exact_any(row["determinant_ref"]),
                    _exact(row["dependent_release_ref"]),
                )
                for row in data.get("determinant_edges", ())
            ),
            dependency_edges=tuple(
                (
                    _exact(row["parent_release_ref"]),
                    _exact(row["child_release_ref"]),
                )
                for row in data.get("dependency_edges", ())
            ),
            known_release_refs=tuple(
                _exact(x) for x in data.get("known_release_refs", ())
            ),
        )
        _validate_embedded_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class LifecycleReplayReceipt:
    original_checkpoint_hash: str
    replayed_checkpoint_hash: str
    event_refs: tuple[ExactRef, ...]
    selection_receipt_refs: tuple[ExactRef, ...]
    no_current_receipt_refs: tuple[ExactRef, ...]
    replay_state: str = "REPLAY_VERIFIED"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "original_checkpoint_hash", _sha(self.original_checkpoint_hash, "original_checkpoint_hash")
        )
        object.__setattr__(
            self, "replayed_checkpoint_hash", _sha(self.replayed_checkpoint_hash, "replayed_checkpoint_hash")
        )
        object.__setattr__(
            self, "event_refs", _exact_refs(self.event_refs, allow_authority_kind=True)
        )
        object.__setattr__(
            self,
            "selection_receipt_refs",
            _exact_refs(self.selection_receipt_refs, allow_authority_kind=True),
        )
        object.__setattr__(
            self,
            "no_current_receipt_refs",
            _exact_refs(self.no_current_receipt_refs, allow_authority_kind=True),
        )
        if self.replay_state != "REPLAY_VERIFIED":
            raise LearnedProductLifecycleError("replay_state must be REPLAY_VERIFIED")
        if self.original_checkpoint_hash != self.replayed_checkpoint_hash:
            raise LearnedProductLifecycleConflict("lifecycle replay checkpoint hash mismatch")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "record_type": "LifecycleReplayReceipt",
            "original_checkpoint_hash": self.original_checkpoint_hash,
            "replayed_checkpoint_hash": self.replayed_checkpoint_hash,
            "event_refs": [ref.as_dict() for ref in self.event_refs],
            "selection_receipt_refs": [
                ref.as_dict() for ref in self.selection_receipt_refs
            ],
            "no_current_receipt_refs": [
                ref.as_dict() for ref in self.no_current_receipt_refs
            ],
            "replay_state": self.replay_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("REPLAY", self.semantic_projection())


class LearnedProductLifecycleExecutor:
    """Append-only B5 lifecycle owner over opaque exact learned-product releases."""

    def __init__(self) -> None:
        self._repository_subjects: dict[str, LearnedProductLifecycleSubject] = {}
        self._registered: set[str] = set()
        self._events: list[LearnedProductLifecycleEvent] = []
        self._events_by_ref: dict[str, LearnedProductLifecycleEvent] = {}
        self._release_event_refs: dict[str, list[ExactRef]] = {}

        self._publication: dict[str, str] = {}
        self._validity: dict[str, str] = {}
        self._replay: dict[str, str] = {}
        self._rebuild: dict[str, str] = {}
        self._materialization: dict[str, str] = {}
        self._payload_materialized: dict[str, bool] = {}

        self._selection_keys: dict[str, SelectionKey] = {}
        self._selection_receipts: dict[str, CurrentSelectionReceipt] = {}
        self._no_current_receipts: dict[str, NoCurrentReceipt] = {}
        self._selection_index: dict[str, ExactRef] = {}
        self._selection_state_kind: dict[str, str] = {}

        self._invalidations: dict[str, InvalidationReceipt] = {}
        self._rebuild_eligibility: dict[str, RebuildEligibilityReceipt] = {}
        self._rebuild_links: dict[str, RebuildLinkReceipt] = {}
        self._gc_eligibility: dict[str, GCElegibilityReceipt] = {}
        self._gc_recorded: set[str] = set()

    @property
    def events(self) -> tuple[LearnedProductLifecycleEvent, ...]:
        return tuple(self._events)

    @property
    def registered_release_refs(self) -> tuple[ExactRef, ...]:
        return tuple(
            self._repository_subjects[key].release_ref for key in sorted(self._registered)
        )

    @property
    def staged_release_refs(self) -> tuple[ExactRef, ...]:
        return tuple(
            self._repository_subjects[key].release_ref
            for key in sorted(self._repository_subjects)
        )

    @property
    def determinant_graph(self) -> LearnedProductDeterminantGraph:
        return LearnedProductDeterminantGraph.from_subjects(
            self._repository_subjects[key] for key in sorted(self._registered)
        )

    def stage_release(
        self, subject: LearnedProductLifecycleSubject
    ) -> LearnedProductLifecycleSubject:
        if not isinstance(subject, LearnedProductLifecycleSubject):
            raise LearnedProductLifecycleError(
                "stage_release requires LearnedProductLifecycleSubject"
            )
        existing = self._repository_subjects.get(subject.release_ref.key)
        if existing is not None:
            if existing != subject:
                raise LearnedProductLifecycleConflict(
                    "same exact release ref carries conflicting B5 lifecycle view"
                )
            return existing
        duplicate_product = [
            other
            for other in self._repository_subjects.values()
            if other.product_ref == subject.product_ref
            and other.release_ref != subject.release_ref
            and other.semantic_projection_hash != subject.semantic_projection_hash
        ]
        if duplicate_product:
            raise LearnedProductLifecycleConflict(
                "same product_ref cannot carry conflicting semantic_projection_hash"
            )
        self._repository_subjects[subject.release_ref.key] = subject
        return subject

    def stage_protocol(
        self, value: LearnedProductReleaseProtocol, **overrides: Any
    ) -> LearnedProductLifecycleSubject:
        return self.stage_release(
            LearnedProductLifecycleSubject.from_protocol(value, **overrides)
        )

    def _subject(
        self, release_ref: ExactRef | Mapping[str, Any], *, require_registered: bool = True
    ) -> LearnedProductLifecycleSubject:
        ref = _exact(release_ref, "release_ref")
        subject = self._repository_subjects.get(ref.key)
        if subject is None:
            raise LearnedProductLifecycleError("exact learned-product release is unavailable")
        if require_registered and ref.key not in self._registered:
            raise LearnedProductLifecycleError(
                "repository presence is not lifecycle registration"
            )
        return subject

    def _event(
        self,
        *,
        event_kind: str,
        subject: LearnedProductLifecycleSubject,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
        payload: Mapping[str, Any] | None = None,
        parent_lifecycle_event_ref: ExactRef | None = None,
        ordinal_offset: int = 1,
    ) -> LearnedProductLifecycleEvent:
        parent = (
            self._events[-1].ref if self._events else None
        ) if parent_lifecycle_event_ref is None else _exact_any(parent_lifecycle_event_ref)
        return LearnedProductLifecycleEvent(
            ordinal=len(self._events) + ordinal_offset,
            event_kind=event_kind,
            release_ref=subject.release_ref,
            product_ref=subject.product_ref,
            selection_scope_ref=subject.selection_scope_ref,
            event_authority_ref=_exact(event_authority_ref),
            event_rule_ref=_exact(event_rule_ref),
            parent_lifecycle_event_ref=parent,
            evidence_refs=tuple(evidence_refs),
            payload=payload or {},
        )

    def _append_events(self, events: Iterable[LearnedProductLifecycleEvent]) -> None:
        planned = tuple(events)
        expected_ordinal = len(self._events) + 1
        known_refs = set(self._events_by_ref)
        for event in planned:
            if event.ordinal != expected_ordinal:
                raise LearnedProductLifecycleConflict("lifecycle event ordinal is not append-only")
            if event.parent_lifecycle_event_ref is not None:
                parent_key = event.parent_lifecycle_event_ref.key
                if parent_key not in known_refs:
                    raise LearnedProductLifecycleConflict(
                        "lifecycle event parent is not an exact prior event"
                    )
            elif expected_ordinal != 1:
                raise LearnedProductLifecycleConflict(
                    "noninitial lifecycle event requires exact parent"
                )
            if event.ref.key in known_refs:
                raise LearnedProductLifecycleConflict("lifecycle event ref collision")
            known_refs.add(event.ref.key)
            expected_ordinal += 1
        for event in planned:
            self._events.append(event)
            self._events_by_ref[event.ref.key] = event
            self._release_event_refs.setdefault(event.release_ref.key, []).append(event.ref)

    def register_product(
        self,
        release_ref: ExactRef,
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref, require_registered=False)
        if subject.release_ref.key in self._registered:
            raise LearnedProductLifecycleError("learned product is already lifecycle-registered")
        event = self._event(
            event_kind="PRODUCT_REGISTERED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "producer_owner_ref": subject.producer_owner_ref.as_dict(),
                "producer_contract_ref": subject.producer_contract_ref.as_dict(),
                "semantic_projection_hash": subject.semantic_projection_hash,
                "authority_snapshot_refs": [
                    ref.as_dict() for ref in subject.authority_snapshot_refs
                ],
                "direct_dependency_refs": [
                    ref.as_dict() for ref in subject.direct_dependency_refs
                ],
                "determinant_set_hash": subject.determinant_set_hash,
                "replay_root_ref": subject.replay_root_ref.as_dict(),
                "build_or_release_receipt_refs": [
                    ref.as_dict() for ref in subject.build_or_release_receipt_refs
                ],
                "materialization_class": subject.materialization_class,
            },
        )
        self._append_events((event,))
        key = subject.release_ref.key
        self._registered.add(key)
        self._publication[key] = "UNPUBLISHED"
        self._validity[key] = "VALID"
        self._replay[key] = subject.replay_state
        self._rebuild[key] = subject.rebuild_state
        self._materialization[key] = subject.materialization_class
        self._payload_materialized[key] = True
        return event

    def lifecycle_state(
        self, release_ref: ExactRef | Mapping[str, Any]
    ) -> LifecycleState:
        subject = self._subject(release_ref)
        key = subject.release_ref.key
        return LifecycleState(
            release_ref=subject.release_ref,
            publication=self._publication[key],
            validity=self._validity[key],
            replay=self._replay[key],
            rebuild=self._rebuild[key],
            materialization_class=self._materialization[key],
            payload_materialized=self._payload_materialized[key],
            registered=True,
        )

    def publish_product(
        self,
        release_ref: ExactRef,
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref)
        key = subject.release_ref.key
        if self._publication[key] == "PUBLISHED":
            raise LearnedProductLifecycleError("product is already PUBLISHED")
        if subject.replay_state != "REPLAY_COMPLETE":
            raise LearnedProductLifecycleError("MISSING_REPLAY_CLOSURE")
        if not subject.authority_snapshot_refs:
            raise LearnedProductLifecycleError("MISSING_SEMANTIC_AUTHORITY")
        if not subject.determinant_refs:
            raise LearnedProductLifecycleError("MISSING_DETERMINANT")
        event = self._event(
            event_kind="PRODUCT_PUBLISHED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "replay_root_ref": subject.replay_root_ref.as_dict(),
                "determinant_set_hash": subject.determinant_set_hash,
                "authority_snapshot_refs": [
                    ref.as_dict() for ref in subject.authority_snapshot_refs
                ],
                "producer_permission_ceiling": (
                    subject.producer_permission_ceiling_ref.as_dict()
                ),
            },
        )
        self._append_events((event,))
        self._publication[key] = "PUBLISHED"
        return event

    def record_recertification(
        self,
        release_ref: ExactRef,
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        attestation_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref)
        event = self._event(
            event_kind="RECERTIFIES",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={"attestation_ref": _exact(attestation_ref).as_dict()},
        )
        self._append_events((event,))
        return event

    def selection_key(
        self,
        *,
        product_family_ref: ExactRef,
        selection_scope_ref: ExactRef,
        selection_purpose_ref: ExactRef,
        consumer_context_partition_ref: ExactRef | None = None,
    ) -> SelectionKey:
        key = SelectionKey(
            product_family_ref=product_family_ref,
            selection_scope_ref=selection_scope_ref,
            selection_purpose_ref=selection_purpose_ref,
            consumer_context_partition_ref=consumer_context_partition_ref,
        )
        existing = self._selection_keys.get(key.ref.key)
        if existing is not None and existing != key:
            raise LearnedProductLifecycleConflict("selection key ref collision")
        self._selection_keys[key.ref.key] = key
        return key

    def _selection_key(self, ref: ExactRef | Mapping[str, Any]) -> SelectionKey:
        exact = _exact(ref, "selection_key_ref")
        key = self._selection_keys.get(exact.key)
        if key is None:
            raise LearnedProductLifecycleError("exact SelectionKey is unavailable")
        return key

    def _selection_receipt_ref_for_key(self, key_ref: ExactRef) -> ExactRef | None:
        return self._selection_index.get(key_ref.key)

    def _selection_state_for_key(self, key_ref: ExactRef) -> str:
        return self._selection_state_kind.get(key_ref.key, "UNKNOWN_CURRENTNESS")

    def _assert_expected_previous(
        self,
        key_ref: ExactRef,
        expected_previous_receipt_ref: ExactRef | Mapping[str, Any] | None,
    ) -> ExactRef | None:
        current = self._selection_receipt_ref_for_key(key_ref)
        expected = _optional_exact(
            expected_previous_receipt_ref, allow_authority_kind=True
        )
        if current != expected:
            raise LearnedProductLifecycleConflict(
                "CONFLICTING_CURRENT_SELECTION: exact prior selection receipt mismatch"
            )
        if self._selection_state_for_key(key_ref) == "CONFLICTING_CURRENT_SELECTION":
            raise LearnedProductLifecycleConflict("CONFLICTING_CURRENT_SELECTION")
        return current

    def _selection_subject_ok(self, key: SelectionKey, subject: LearnedProductLifecycleSubject) -> None:
        state = self.lifecycle_state(subject.release_ref)
        if state.publication != "PUBLISHED":
            raise LearnedProductLifecycleError(
                "publication lifecycle state is required before current selection"
            )
        if state.validity != "VALID":
            raise LearnedProductLifecycleError(
                "invalidated/withdrawn product cannot be selected current"
            )
        if key.product_family_ref != subject.product_family_ref:
            raise LearnedProductLifecycleError("selection key product family mismatch")
        if key.selection_scope_ref != subject.selection_scope_ref:
            raise LearnedProductLifecycleError("selection key scope mismatch")

    def _determinant_snapshot_ref(self) -> ExactRef:
        return self.determinant_graph.ref

    def select_current(
        self,
        selection_key_ref: ExactRef,
        release_ref: ExactRef,
        *,
        expected_previous_receipt_ref: ExactRef | None,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> CurrentSelectionReceipt:
        key = self._selection_key(selection_key_ref)
        subject = self._subject(release_ref)
        self._selection_subject_ok(key, subject)
        previous = self._assert_expected_previous(
            key.ref, expected_previous_receipt_ref
        )
        event = self._event(
            event_kind="CURRENT_SELECTED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "selected_product_ref": subject.product_ref.as_dict(),
                "previous_current_product_ref_or_null": (
                    None
                    if previous is None or previous.key in self._no_current_receipts
                    else self._selected_product_for_receipt(previous).as_dict()
                ),
                "selection_attestation_ref": _exact(
                    selection_attestation_ref
                ).as_dict(),
                "selection_key_ref": key.ref.as_dict(),
            },
        )
        receipt = CurrentSelectionReceipt(
            selection_key_ref=key.ref,
            selected_release_ref=subject.release_ref,
            current_select_event_ref=event.ref,
            previous_selection_receipt_ref=previous,
            selection_authority_refs=(_exact(event_authority_ref),),
            selection_attestation_refs=(_exact(selection_attestation_ref),),
            determinant_snapshot_ref=self._determinant_snapshot_ref(),
        )
        self._append_events((event,))
        self._selection_receipts[receipt.ref.key] = receipt
        self._selection_index[key.ref.key] = receipt.ref
        self._selection_state_kind[key.ref.key] = "CURRENT_SELECTED"
        return receipt

    def _selected_product_for_receipt(self, receipt_ref: ExactRef) -> ExactRef:
        current = self._selection_receipts.get(receipt_ref.key)
        if current is not None:
            return self._subject(current.selected_release_ref).product_ref
        no_current = self._no_current_receipts.get(receipt_ref.key)
        if no_current is not None:
            raise LearnedProductLifecycleError(
                "NO_CURRENT receipt has no previous current product identity"
            )
        raise LearnedProductLifecycleError("exact selection receipt is unavailable")

    def declare_no_current(
        self,
        selection_key_ref: ExactRef,
        *,
        expected_previous_receipt_ref: ExactRef | None,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        reason_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
        subject_release_ref: ExactRef | None = None,
    ) -> NoCurrentReceipt:
        key = self._selection_key(selection_key_ref)
        previous = self._assert_expected_previous(
            key.ref, expected_previous_receipt_ref
        )
        if subject_release_ref is not None:
            subject = self._subject(subject_release_ref)
        elif previous is not None and previous.key in self._selection_receipts:
            subject = self._subject(
                self._selection_receipts[previous.key].selected_release_ref
            )
        else:
            candidates = [
                subject
                for subject in self._repository_subjects.values()
                if subject.release_ref.key in self._registered
                and subject.product_family_ref == key.product_family_ref
                and subject.selection_scope_ref == key.selection_scope_ref
            ]
            if not candidates:
                raise LearnedProductLifecycleError(
                    "NO_CURRENT requires an exact subject release when no prior selection exists"
                )
            subject = sorted(candidates, key=lambda x: x.release_ref.key)[0]
        event = self._event(
            event_kind="CURRENT_CLEARED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "selection_key_ref": key.ref.as_dict(),
                "selection_attestation_ref": _exact(
                    selection_attestation_ref
                ).as_dict(),
                "reason_ref": _exact(reason_ref).as_dict(),
            },
        )
        receipt = NoCurrentReceipt(
            selection_key_ref=key.ref,
            no_current_event_ref=event.ref,
            previous_selection_receipt_ref=previous,
            selection_authority_refs=(_exact(event_authority_ref),),
            selection_attestation_refs=(_exact(selection_attestation_ref),),
            reason_ref=_exact(reason_ref),
        )
        self._append_events((event,))
        self._no_current_receipts[receipt.ref.key] = receipt
        self._selection_index[key.ref.key] = receipt.ref
        self._selection_state_kind[key.ref.key] = "NO_CURRENT"
        return receipt

    def resolve_selection_exact(
        self,
        selection_key_ref: ExactRef,
        selection_receipt_ref: ExactRef,
    ) -> SelectionResolution:
        key = self._selection_key(selection_key_ref)
        supplied = _exact_any(selection_receipt_ref)
        expected = self._selection_index.get(key.ref.key)
        if expected != supplied:
            raise LearnedProductLifecycleError(
                "currentness requires the exact current selection/no-current receipt"
            )
        state = self._selection_state_for_key(key.ref)
        if state == "CURRENT_SELECTED":
            receipt = self._selection_receipts.get(supplied.key)
            if receipt is None or receipt.selection_key_ref != key.ref:
                raise LearnedProductLifecycleConflict("current selection receipt mismatch")
            return SelectionResolution(
                key.ref, "CURRENT_SELECTED", receipt.selected_release_ref, receipt.ref
            )
        if state == "NO_CURRENT":
            receipt = self._no_current_receipts.get(supplied.key)
            if receipt is None or receipt.selection_key_ref != key.ref:
                raise LearnedProductLifecycleConflict("NO_CURRENT receipt mismatch")
            return SelectionResolution(key.ref, "NO_CURRENT", None, receipt.ref)
        if state == "CONFLICTING_CURRENT_SELECTION":
            raise LearnedProductLifecycleConflict("CONFLICTING_CURRENT_SELECTION")
        raise LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")

    def current_selection_receipt_ref(self, selection_key_ref: ExactRef) -> ExactRef:
        key = self._selection_key(selection_key_ref)
        ref = self._selection_index.get(key.ref.key)
        if ref is None:
            raise LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")
        if self._selection_state_for_key(key.ref) == "CONFLICTING_CURRENT_SELECTION":
            raise LearnedProductLifecycleConflict("CONFLICTING_CURRENT_SELECTION")
        return ref

    def supersede_current(
        self,
        selection_key_ref: ExactRef,
        *,
        predecessor_release_ref: ExactRef,
        successor_release_ref: ExactRef,
        expected_previous_receipt_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        supersession_basis_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> CurrentSelectionReceipt:
        key = self._selection_key(selection_key_ref)
        predecessor = self._subject(predecessor_release_ref)
        successor = self._subject(successor_release_ref)
        self._selection_subject_ok(key, successor)
        previous = self._assert_expected_previous(
            key.ref, expected_previous_receipt_ref
        )
        if previous is None:
            raise LearnedProductLifecycleError(
                "CURRENT_SUPERSEDED requires exact prior current selection"
            )
        current_receipt = self._selection_receipts.get(previous.key)
        if (
            current_receipt is None
            or current_receipt.selected_release_ref != predecessor.release_ref
        ):
            raise LearnedProductLifecycleError(
                "supersession predecessor is not exact current release"
            )
        if predecessor.release_ref == successor.release_ref:
            raise LearnedProductLifecycleError(
                "supersession predecessor and successor must differ"
            )
        event = self._event(
            event_kind="CURRENT_SUPERSEDED",
            subject=successor,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "predecessor_product_ref": predecessor.product_ref.as_dict(),
                "successor_product_ref": successor.product_ref.as_dict(),
                "predecessor_release_ref": predecessor.release_ref.as_dict(),
                "successor_release_ref": successor.release_ref.as_dict(),
                "supersession_basis_ref": _exact(
                    supersession_basis_ref
                ).as_dict(),
                "selection_key_ref": key.ref.as_dict(),
                "selection_attestation_ref": _exact(
                    selection_attestation_ref
                ).as_dict(),
            },
        )
        receipt = CurrentSelectionReceipt(
            selection_key_ref=key.ref,
            selected_release_ref=successor.release_ref,
            current_select_event_ref=event.ref,
            previous_selection_receipt_ref=previous,
            selection_authority_refs=(_exact(event_authority_ref),),
            selection_attestation_refs=(_exact(selection_attestation_ref),),
            determinant_snapshot_ref=self._determinant_snapshot_ref(),
        )
        self._append_events((event,))
        self._selection_receipts[receipt.ref.key] = receipt
        self._selection_index[key.ref.key] = receipt.ref
        self._selection_state_kind[key.ref.key] = "CURRENT_SELECTED"
        return receipt

    def _current_keys_for_release(self, release_ref: ExactRef) -> tuple[SelectionKey, ...]:
        keys: list[SelectionKey] = []
        for key_ref_key, state in self._selection_state_kind.items():
            if state != "CURRENT_SELECTED":
                continue
            receipt_ref = self._selection_index[key_ref_key]
            receipt = self._selection_receipts[receipt_ref.key]
            if receipt.selected_release_ref == release_ref:
                keys.append(self._selection_keys[key_ref_key])
        return tuple(sorted(keys, key=lambda key: key.ref.key))

    def _plan_current_transition_events(
        self,
        keys: tuple[SelectionKey, ...],
        transitions: Mapping[str, ExactRef | None],
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        reason_ref: ExactRef,
        ordinal_start: int,
        parent_start: ExactRef | None,
    ) -> tuple[
        tuple[LearnedProductLifecycleEvent, ...],
        tuple[CurrentSelectionReceipt | NoCurrentReceipt, ...],
    ]:
        expected_keys = {key.ref.key for key in keys}
        if set(transitions) != expected_keys:
            raise LearnedProductLifecycleError(
                "every affected current SelectionKey requires one explicit replacement or NO_CURRENT"
            )
        events: list[LearnedProductLifecycleEvent] = []
        receipts: list[CurrentSelectionReceipt | NoCurrentReceipt] = []
        parent = parent_start
        offset = ordinal_start
        for key in keys:
            previous = self._selection_index[key.ref.key]
            raw_target = transitions[key.ref.key]
            if raw_target is None:
                previous_receipt = self._selection_receipts.get(previous.key)
                if previous_receipt is None:
                    raise LearnedProductLifecycleConflict(
                        "affected current key does not resolve exact prior selection"
                    )
                subject = self._subject(previous_receipt.selected_release_ref)
                event = LearnedProductLifecycleEvent(
                    ordinal=offset,
                    event_kind="CURRENT_CLEARED",
                    release_ref=subject.release_ref,
                    product_ref=subject.product_ref,
                    selection_scope_ref=subject.selection_scope_ref,
                    event_authority_ref=_exact(event_authority_ref),
                    event_rule_ref=_exact(event_rule_ref),
                    parent_lifecycle_event_ref=parent,
                    evidence_refs=(),
                    payload={
                        "selection_key_ref": key.ref.as_dict(),
                        "selection_attestation_ref": _exact(
                            selection_attestation_ref
                        ).as_dict(),
                        "reason_ref": _exact(reason_ref).as_dict(),
                    },
                )
                receipt: CurrentSelectionReceipt | NoCurrentReceipt = NoCurrentReceipt(
                    selection_key_ref=key.ref,
                    no_current_event_ref=event.ref,
                    previous_selection_receipt_ref=previous,
                    selection_authority_refs=(_exact(event_authority_ref),),
                    selection_attestation_refs=(_exact(selection_attestation_ref),),
                    reason_ref=_exact(reason_ref),
                )
            else:
                target = self._subject(_exact(raw_target))
                self._selection_subject_ok(key, target)
                event = LearnedProductLifecycleEvent(
                    ordinal=offset,
                    event_kind="CURRENT_SELECTED",
                    release_ref=target.release_ref,
                    product_ref=target.product_ref,
                    selection_scope_ref=target.selection_scope_ref,
                    event_authority_ref=_exact(event_authority_ref),
                    event_rule_ref=_exact(event_rule_ref),
                    parent_lifecycle_event_ref=parent,
                    evidence_refs=(),
                    payload={
                        "selection_key_ref": key.ref.as_dict(),
                        "selection_attestation_ref": _exact(
                            selection_attestation_ref
                        ).as_dict(),
                        "reason_ref": _exact(reason_ref).as_dict(),
                    },
                )
                receipt = CurrentSelectionReceipt(
                    selection_key_ref=key.ref,
                    selected_release_ref=target.release_ref,
                    current_select_event_ref=event.ref,
                    previous_selection_receipt_ref=previous,
                    selection_authority_refs=(_exact(event_authority_ref),),
                    selection_attestation_refs=(_exact(selection_attestation_ref),),
                    determinant_snapshot_ref=self._determinant_snapshot_ref(),
                )
            events.append(event)
            receipts.append(receipt)
            parent = event.ref
            offset += 1
        return tuple(events), tuple(receipts)

    def _commit_selection_transition_receipts(
        self, receipts: Iterable[CurrentSelectionReceipt | NoCurrentReceipt]
    ) -> None:
        for receipt in receipts:
            key = receipt.selection_key_ref.key
            if isinstance(receipt, CurrentSelectionReceipt):
                self._selection_receipts[receipt.ref.key] = receipt
                self._selection_index[key] = receipt.ref
                self._selection_state_kind[key] = "CURRENT_SELECTED"
            else:
                self._no_current_receipts[receipt.ref.key] = receipt
                self._selection_index[key] = receipt.ref
                self._selection_state_kind[key] = "NO_CURRENT"

    def withdraw_product(
        self,
        release_ref: ExactRef,
        *,
        withdrawal_reason_ref: ExactRef,
        withdrawal_scope_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        current_transitions: Mapping[str, ExactRef | None] | None = None,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref)
        if self._validity[subject.release_ref.key] == "WITHDRAWN":
            raise LearnedProductLifecycleError("product is already withdrawn")
        keys = self._current_keys_for_release(subject.release_ref)
        transitions = dict(current_transitions or {})
        for raw_target in transitions.values():
            if raw_target is not None and _exact(raw_target) == subject.release_ref:
                raise LearnedProductLifecycleError(
                    "withdrawn release cannot be its own explicit current replacement"
                )
        withdrawal = self._event(
            event_kind="PRODUCT_WITHDRAWN",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "withdrawal_reason_ref": _exact(withdrawal_reason_ref).as_dict(),
                "withdrawal_scope_ref": _exact(withdrawal_scope_ref).as_dict(),
            },
        )
        follow_events: tuple[LearnedProductLifecycleEvent, ...] = ()
        follow_receipts: tuple[CurrentSelectionReceipt | NoCurrentReceipt, ...] = ()
        if keys:
            follow_events, follow_receipts = self._plan_current_transition_events(
                keys,
                transitions,
                event_authority_ref=event_authority_ref,
                event_rule_ref=event_rule_ref,
                selection_attestation_ref=selection_attestation_ref,
                reason_ref=withdrawal_reason_ref,
                ordinal_start=len(self._events) + 2,
                parent_start=withdrawal.ref,
            )
        elif transitions:
            raise LearnedProductLifecycleError(
                "current_transitions supplied for noncurrent withdrawal"
            )
        self._append_events((withdrawal,) + follow_events)
        self._validity[subject.release_ref.key] = "WITHDRAWN"
        self._commit_selection_transition_receipts(follow_receipts)
        return withdrawal

    def declare_invalidation(
        self,
        changed_determinant_refs: Iterable[ExactRef | AuthorityRef | Mapping[str, Any]],
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        dependency_closure_receipt_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        current_transitions: Mapping[str, ExactRef | None] | None = None,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> InvalidationReceipt:
        changed = _determinant_refs(changed_determinant_refs)
        if not changed:
            raise LearnedProductLifecycleError(
                "invalidation requires at least one exact changed determinant"
            )
        graph = self.determinant_graph
        direct, transitive = graph.affected(changed)
        affected = _exact_refs(direct + transitive)
        unaffected = graph.unaffected(affected)
        affected_subjects = tuple(self._subject(ref) for ref in affected)
        affected_current_keys: dict[str, SelectionKey] = {}
        for subject in affected_subjects:
            for key in self._current_keys_for_release(subject.release_ref):
                affected_current_keys[key.ref.key] = key
        transitions = dict(current_transitions or {})
        if set(transitions) != set(affected_current_keys):
            raise LearnedProductLifecycleError(
                "current invalidation requires explicit replacement/NO_CURRENT for every affected current key"
            )
        affected_release_keys = {ref.key for ref in affected}
        for raw_target in transitions.values():
            if raw_target is not None and _exact(raw_target).key in affected_release_keys:
                raise LearnedProductLifecycleError(
                    "invalidated release cannot be selected as its own replacement"
                )

        events: list[LearnedProductLifecycleEvent] = []
        parent = self._events[-1].ref if self._events else None
        ordinal = len(self._events) + 1
        invalidation_payload = {
            "changed_determinant_refs": [ref.as_dict() for ref in changed],
            "affected_product_refs": [
                subject.product_ref.as_dict() for subject in affected_subjects
            ],
            "unaffected_product_refs": [
                self._subject(ref).product_ref.as_dict() for ref in unaffected
            ],
            "dependency_closure_receipt_ref": _exact_any(
                dependency_closure_receipt_ref
            ).as_dict(),
        }
        for subject in affected_subjects:
            event = LearnedProductLifecycleEvent(
                ordinal=ordinal,
                event_kind="PRODUCT_INVALIDATED",
                release_ref=subject.release_ref,
                product_ref=subject.product_ref,
                selection_scope_ref=subject.selection_scope_ref,
                event_authority_ref=_exact(event_authority_ref),
                event_rule_ref=_exact(event_rule_ref),
                parent_lifecycle_event_ref=parent,
                evidence_refs=tuple(evidence_refs),
                payload=invalidation_payload,
            )
            events.append(event)
            parent = event.ref
            ordinal += 1

        follow_events: tuple[LearnedProductLifecycleEvent, ...] = ()
        follow_receipts: tuple[CurrentSelectionReceipt | NoCurrentReceipt, ...] = ()
        keys = tuple(
            affected_current_keys[key]
            for key in sorted(affected_current_keys)
        )
        if keys:
            follow_events, follow_receipts = self._plan_current_transition_events(
                keys,
                transitions,
                event_authority_ref=event_authority_ref,
                event_rule_ref=event_rule_ref,
                selection_attestation_ref=selection_attestation_ref,
                reason_ref=_exact_any(dependency_closure_receipt_ref),
                ordinal_start=ordinal,
                parent_start=parent,
            )

        # Empty affected set is still an exact no-op invalidation receipt.
        prospective_event_refs = tuple(event.ref for event in events)
        receipt = InvalidationReceipt(
            changed_determinant_refs=changed,
            directly_affected_release_refs=direct,
            transitively_affected_release_refs=transitive,
            affected_product_refs=tuple(
                subject.product_ref for subject in affected_subjects
            ),
            unaffected_product_refs=tuple(
                self._subject(ref).product_ref for ref in unaffected
            ),
            dependency_closure_receipt_ref=_exact_any(
                dependency_closure_receipt_ref
            ),
            invalidation_event_refs=prospective_event_refs,
        )
        self._append_events(tuple(events) + follow_events)
        for subject in affected_subjects:
            self._validity[subject.release_ref.key] = "INVALIDATED_REBUILD_REQUIRED"
            self._rebuild[subject.release_ref.key] = "REBUILD_NOT_REQUESTED"
        self._commit_selection_transition_receipts(follow_receipts)
        self._invalidations[receipt.ref.key] = receipt
        return receipt

    def record_rebuild_eligibility(
        self,
        release_ref: ExactRef,
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        execution_mechanism_ref: ExactRef | None,
        source_or_upstream_refs: Iterable[ExactRef] = (),
        historical: bool = False,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> RebuildEligibilityReceipt:
        subject = self._subject(release_ref)
        blockers: list[str] = []
        source_inputs = tuple(source_or_upstream_refs)
        inputs = _exact_refs(
            source_inputs
            + tuple(subject.direct_dependency_refs)
            + (subject.producer_contract_ref, subject.replay_root_ref)
            + tuple(subject.determinant_refs),
            allow_authority_kind=True,
        )
        if not source_inputs and not subject.direct_dependency_refs:
            blockers.append("REBUILD_NOT_PROVED")
        if not subject.authority_snapshot_refs:
            blockers.append("MISSING_SEMANTIC_AUTHORITY")
        if subject.replay_state != "REPLAY_COMPLETE":
            blockers.append("MISSING_REPLAY_CLOSURE")
        if execution_mechanism_ref is None:
            blockers.append("REBUILD_NOT_PROVED")
        state = (
            "REBUILD_BLOCKED"
            if blockers
            else (
                "HISTORICAL_REPLAY_ELIGIBLE"
                if historical
                else "CURRENT_REBUILD_ELIGIBLE"
            )
        )
        event = self._event(
            event_kind="REBUILD_ELIGIBILITY_RECORDED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "rebuild_state": state,
                "blocker_states": sorted(set(blockers)),
                "reconstruction_input_refs": [ref.as_dict() for ref in inputs],
                "execution_mechanism_ref": (
                    None
                    if execution_mechanism_ref is None
                    else _exact_any(execution_mechanism_ref).as_dict()
                ),
            },
        )
        receipt = RebuildEligibilityReceipt(
            release_ref=subject.release_ref,
            rebuild_state=state,
            blocker_states=tuple(sorted(set(blockers))),
            reconstruction_input_refs=inputs,
            execution_mechanism_ref=(
                None
                if execution_mechanism_ref is None
                else _exact_any(execution_mechanism_ref)
            ),
            event_ref=event.ref,
        )
        self._append_events((event,))
        self._rebuild[subject.release_ref.key] = state
        self._rebuild_eligibility[receipt.ref.key] = receipt
        return receipt

    def link_rebuild(
        self,
        old_release_ref: ExactRef,
        *,
        new_release_ref: ExactRef | None,
        rebuild_state: str,
        rebuild_determinant_set_hash: str,
        replay_or_execution_receipt_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> RebuildLinkReceipt:
        old = self._subject(old_release_ref)
        new = None if new_release_ref is None else self._subject(new_release_ref)
        if rebuild_state == "REBUILT":
            if new is None:
                raise LearnedProductLifecycleError("REBUILT requires producer-owned new release")
            changed_semantics = (
                old.semantic_projection_hash != new.semantic_projection_hash
                or old.determinant_set_hash != _sha(
                    rebuild_determinant_set_hash, "rebuild_determinant_set_hash"
                )
            )
            if changed_semantics and new.product_ref == old.product_ref:
                raise LearnedProductLifecycleError(
                    "semantic determinant/output change requires upstream new product identity"
                )
        event = self._event(
            event_kind="PRODUCT_REBUILT",
            subject=old,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "old_product_ref": old.product_ref.as_dict(),
                "new_product_ref": None if new is None else new.product_ref.as_dict(),
                "old_release_ref": old.release_ref.as_dict(),
                "new_release_ref": None if new is None else new.release_ref.as_dict(),
                "rebuild_state": rebuild_state,
                "rebuild_determinant_set_hash": _sha(
                    rebuild_determinant_set_hash, "rebuild_determinant_set_hash"
                ),
                "replay_or_execution_receipt_ref": _exact(
                    replay_or_execution_receipt_ref
                ).as_dict(),
            },
        )
        receipt = RebuildLinkReceipt(
            old_release_ref=old.release_ref,
            new_release_ref=None if new is None else new.release_ref,
            rebuild_state=rebuild_state,
            rebuild_determinant_set_hash=rebuild_determinant_set_hash,
            replay_or_execution_receipt_ref=_exact(replay_or_execution_receipt_ref),
            event_ref=event.ref,
        )
        self._append_events((event,))
        self._rebuild_links[receipt.ref.key] = receipt
        return receipt

    def record_cache_materialized(
        self,
        release_ref: ExactRef,
        *,
        cache_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref)
        if subject.materialization_class != "OPTIONAL_CACHE_ACCELERATOR":
            raise LearnedProductLifecycleError(
                "CACHE_MATERIALIZED is limited to OPTIONAL_CACHE_ACCELERATOR"
            )
        event = self._event(
            event_kind="CACHE_MATERIALIZED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            payload={"cache_ref": _exact(cache_ref).as_dict()},
        )
        self._append_events((event,))
        self._payload_materialized[subject.release_ref.key] = True
        return event

    def record_cache_dropped(
        self,
        release_ref: ExactRef,
        *,
        cache_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
    ) -> LearnedProductLifecycleEvent:
        subject = self._subject(release_ref)
        if subject.materialization_class != "OPTIONAL_CACHE_ACCELERATOR":
            raise LearnedProductLifecycleError(
                "CACHE_DROPPED is limited to OPTIONAL_CACHE_ACCELERATOR"
            )
        before = (self._validity[subject.release_ref.key], self._publication[subject.release_ref.key])
        event = self._event(
            event_kind="CACHE_DROPPED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            payload={"cache_ref": _exact(cache_ref).as_dict()},
        )
        self._append_events((event,))
        self._payload_materialized[subject.release_ref.key] = False
        after = (self._validity[subject.release_ref.key], self._publication[subject.release_ref.key])
        if before != after:
            raise LearnedProductLifecycleConflict(
                "cache loss may not mutate semantic validity/publication"
            )
        return event

    def attest_gc_eligibility(
        self,
        release_ref: ExactRef,
        *,
        reconstruction_proof_ref: ExactRef,
        historical_retention_proof_ref: ExactRef,
        serving_reconstruction_proof_ref: ExactRef,
        downstream_byte_dependency_absence_proof_ref: ExactRef,
        source_carrier_retention_proof_ref: ExactRef,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
        evidence_refs: Iterable[ExactRef] = (),
    ) -> GCElegibilityReceipt:
        subject = self._subject(release_ref)
        if subject.materialization_class != "RECOMPUTABLE_PRODUCT_PAYLOAD":
            raise LearnedProductLifecycleError("GC_NOT_AUTHORIZED")
        if subject.replay_state != "REPLAY_COMPLETE":
            raise LearnedProductLifecycleError("GC_NOT_AUTHORIZED")
        if self._rebuild[subject.release_ref.key] not in {
            "CURRENT_REBUILD_ELIGIBLE",
            "HISTORICAL_REPLAY_ELIGIBLE",
        }:
            raise LearnedProductLifecycleError("GC_NOT_AUTHORIZED")
        event = self._event(
            event_kind="GC_ELIGIBILITY_ATTESTED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            evidence_refs=evidence_refs,
            payload={
                "materialization_class": subject.materialization_class,
                "reconstruction_proof_ref": _exact(
                    reconstruction_proof_ref
                ).as_dict(),
                "historical_retention_proof_ref": _exact(
                    historical_retention_proof_ref
                ).as_dict(),
                "serving_reconstruction_proof_ref": _exact(
                    serving_reconstruction_proof_ref
                ).as_dict(),
                "downstream_byte_dependency_absence_proof_ref": _exact(
                    downstream_byte_dependency_absence_proof_ref
                ).as_dict(),
                "source_carrier_retention_proof_ref": _exact(
                    source_carrier_retention_proof_ref
                ).as_dict(),
                "source_carrier_retirement_authorized_false": True,
            },
        )
        receipt = GCElegibilityReceipt(
            release_ref=subject.release_ref,
            materialization_class=subject.materialization_class,
            reconstruction_proof_ref=_exact(reconstruction_proof_ref),
            historical_retention_proof_ref=_exact(historical_retention_proof_ref),
            serving_reconstruction_proof_ref=_exact(
                serving_reconstruction_proof_ref
            ),
            downstream_byte_dependency_absence_proof_ref=_exact(
                downstream_byte_dependency_absence_proof_ref
            ),
            source_carrier_retention_proof_ref=_exact(
                source_carrier_retention_proof_ref
            ),
            source_carrier_retirement_authorized_false=True,
            event_ref=event.ref,
        )
        self._append_events((event,))
        self._gc_eligibility[receipt.ref.key] = receipt
        return receipt

    def record_payload_gc(
        self,
        eligibility_receipt_ref: ExactRef,
        *,
        event_authority_ref: ExactRef,
        event_rule_ref: ExactRef,
    ) -> LearnedProductLifecycleEvent:
        exact = _exact_any(eligibility_receipt_ref)
        eligibility = self._gc_eligibility.get(exact.key)
        if eligibility is None:
            raise LearnedProductLifecycleError("GC_NOT_AUTHORIZED")
        subject = self._subject(eligibility.release_ref)
        event = self._event(
            event_kind="RECOMPUTABLE_PAYLOAD_GC_RECORDED",
            subject=subject,
            event_authority_ref=event_authority_ref,
            event_rule_ref=event_rule_ref,
            payload={
                "gc_eligibility_receipt_ref": eligibility.ref.as_dict(),
                "materialization_class": subject.materialization_class,
                "source_carrier_retirement_authorized_false": True,
            },
        )
        self._append_events((event,))
        self._payload_materialized[subject.release_ref.key] = False
        self._gc_recorded.add(subject.release_ref.key)
        return event

    def release_history(
        self, release_ref: ExactRef | Mapping[str, Any]
    ) -> tuple[LearnedProductLifecycleEvent, ...]:
        subject = self._subject(release_ref)
        return tuple(
            self._events_by_ref[ref.key]
            for ref in self._release_event_refs.get(subject.release_ref.key, ())
        )

    def resolve_current_as_of(
        self,
        selection_key_ref: ExactRef,
        *,
        as_of_event_ref: ExactRef | None = None,
        as_of_checkpoint: Mapping[str, Any] | None = None,
    ) -> SelectionResolution:
        key = self._selection_key(selection_key_ref)
        if (as_of_event_ref is None) == (as_of_checkpoint is None):
            raise LearnedProductLifecycleError(
                "current-as-of requires exactly one event ref or checkpoint"
            )
        if as_of_checkpoint is not None:
            restored = self.from_checkpoint(as_of_checkpoint)
            restored_key = restored._selection_keys.get(key.ref.key)
            if restored_key is None:
                return SelectionResolution(
                    key.ref, "UNKNOWN_CURRENTNESS", None, None
                )
            receipt_ref = restored._selection_index.get(key.ref.key)
            if receipt_ref is None:
                return SelectionResolution(
                    key.ref, "UNKNOWN_CURRENTNESS", None, None
                )
            return restored.resolve_selection_exact(key.ref, receipt_ref)

        event_ref = _exact_any(as_of_event_ref)
        event = self._events_by_ref.get(event_ref.key)
        if event is None:
            raise LearnedProductLifecycleError("exact as-of lifecycle event is unavailable")
        state = "UNKNOWN_CURRENTNESS"
        selected: ExactRef | None = None
        receipt_ref: ExactRef | None = None
        for candidate in self._events:
            if candidate.ordinal > event.ordinal:
                break
            for receipt in self._selection_receipts.values():
                if (
                    receipt.current_select_event_ref == candidate.ref
                    and receipt.selection_key_ref == key.ref
                ):
                    state = "CURRENT_SELECTED"
                    selected = receipt.selected_release_ref
                    receipt_ref = receipt.ref
            for receipt in self._no_current_receipts.values():
                if (
                    receipt.no_current_event_ref == candidate.ref
                    and receipt.selection_key_ref == key.ref
                ):
                    state = "NO_CURRENT"
                    selected = None
                    receipt_ref = receipt.ref
        return SelectionResolution(key.ref, state, selected, receipt_ref)

    def _checkpoint_payload(self) -> dict[str, Any]:
        return {
            "schema": LIFECYCLE_CHECKPOINT_SCHEMA,
            "contract_id": LIFECYCLE_CONTRACT_ID,
            "runtime_schema": LIFECYCLE_RUNTIME_SCHEMA,
            "repository_subjects": [
                self._repository_subjects[key].as_dict()
                for key in sorted(self._repository_subjects)
            ],
            "registered_release_refs": [
                self._repository_subjects[key].release_ref.as_dict()
                for key in sorted(self._registered)
            ],
            "events": [event.as_dict() for event in self._events],
            "selection_keys": [
                self._selection_keys[key].as_dict()
                for key in sorted(self._selection_keys)
            ],
            "selection_receipts": [
                self._selection_receipts[key].as_dict()
                for key in sorted(self._selection_receipts)
            ],
            "no_current_receipts": [
                self._no_current_receipts[key].as_dict()
                for key in sorted(self._no_current_receipts)
            ],
            "selection_index": [
                {
                    "selection_key_ref": self._selection_keys[key].ref.as_dict(),
                    "receipt_ref": self._selection_index[key].as_dict(),
                    "state": self._selection_state_kind[key],
                }
                for key in sorted(self._selection_index)
            ],
            "publication": sorted(self._publication.items()),
            "validity": sorted(self._validity.items()),
            "replay": sorted(self._replay.items()),
            "rebuild": sorted(self._rebuild.items()),
            "materialization": sorted(self._materialization.items()),
            "payload_materialized": sorted(self._payload_materialized.items()),
            "invalidations": [
                self._invalidations[key].as_dict()
                for key in sorted(self._invalidations)
            ],
            "rebuild_eligibility": [
                self._rebuild_eligibility[key].as_dict()
                for key in sorted(self._rebuild_eligibility)
            ],
            "rebuild_links": [
                self._rebuild_links[key].as_dict()
                for key in sorted(self._rebuild_links)
            ],
            "gc_eligibility": [
                self._gc_eligibility[key].as_dict()
                for key in sorted(self._gc_eligibility)
            ],
            "gc_recorded_release_refs": [
                self._repository_subjects[key].release_ref.as_dict()
                for key in sorted(self._gc_recorded)
            ],
            "determinant_graph": self.determinant_graph.as_dict(),
        }

    def export_checkpoint(self) -> dict[str, Any]:
        payload = self._checkpoint_payload()
        return {
            "checkpoint_payload": payload,
            "checkpoint_hash": semantic_hash(payload),
        }

    @classmethod
    def from_checkpoint(
        cls, checkpoint: Mapping[str, Any]
    ) -> "LearnedProductLifecycleExecutor":
        if not isinstance(checkpoint, Mapping):
            raise LearnedProductLifecycleError("lifecycle checkpoint must be a mapping")
        payload = checkpoint.get("checkpoint_payload")
        if not isinstance(payload, Mapping):
            raise LearnedProductLifecycleError("checkpoint payload is missing")
        supplied_hash = checkpoint.get("checkpoint_hash")
        if supplied_hash != semantic_hash(payload):
            raise LearnedProductLifecycleConflict("lifecycle checkpoint hash mismatch")
        if payload.get("schema") != LIFECYCLE_CHECKPOINT_SCHEMA:
            raise LearnedProductLifecycleError("lifecycle checkpoint schema mismatch")
        if payload.get("contract_id") != LIFECYCLE_CONTRACT_ID:
            raise LearnedProductLifecycleError("lifecycle contract id mismatch")

        executor = cls()
        for row in payload.get("repository_subjects", ()):
            executor.stage_release(LearnedProductLifecycleSubject.from_dict(row))

        registered = {
            _exact(x).key for x in payload.get("registered_release_refs", ())
        }
        if not registered.issubset(set(executor._repository_subjects)):
            raise LearnedProductLifecycleConflict(
                "checkpoint registered release is absent from repository subjects"
            )
        executor._registered = set(registered)

        events = [
            LearnedProductLifecycleEvent.from_dict(row)
            for row in payload.get("events", ())
        ]
        executor._append_events(events)

        executor._selection_keys = {}
        for row in payload.get("selection_keys", ()):
            key = SelectionKey.from_dict(row)
            executor._selection_keys[key.ref.key] = key

        for row in payload.get("selection_receipts", ()):
            receipt = CurrentSelectionReceipt.from_dict(row)
            executor._selection_receipts[receipt.ref.key] = receipt
        for row in payload.get("no_current_receipts", ()):
            receipt = NoCurrentReceipt.from_dict(row)
            executor._no_current_receipts[receipt.ref.key] = receipt

        for row in payload.get("selection_index", ()):
            key_ref = _exact(row["selection_key_ref"])
            receipt_ref = _exact_any(row["receipt_ref"])
            if key_ref.key not in executor._selection_keys:
                raise LearnedProductLifecycleConflict(
                    "selection index references unavailable SelectionKey"
                )
            state = row["state"]
            if state not in {"CURRENT_SELECTED", "NO_CURRENT", "CONFLICTING_CURRENT_SELECTION"}:
                raise LearnedProductLifecycleConflict("invalid checkpoint selection state")
            if state == "CURRENT_SELECTED":
                receipt = executor._selection_receipts.get(receipt_ref.key)
                if receipt is None or receipt.selection_key_ref != key_ref:
                    raise LearnedProductLifecycleConflict(
                        "checkpoint current receipt mismatch"
                    )
            elif state == "NO_CURRENT":
                receipt = executor._no_current_receipts.get(receipt_ref.key)
                if receipt is None or receipt.selection_key_ref != key_ref:
                    raise LearnedProductLifecycleConflict(
                        "checkpoint NO_CURRENT receipt mismatch"
                    )
            executor._selection_index[key_ref.key] = receipt_ref
            executor._selection_state_kind[key_ref.key] = state

        def _pairs(name: str) -> dict[str, Any]:
            raw = payload.get(name, ())
            if not isinstance(raw, list):
                raise LearnedProductLifecycleConflict(
                    f"checkpoint {name} must be canonical pair list"
                )
            return {row[0]: row[1] for row in raw}

        executor._publication = _pairs("publication")
        executor._validity = _pairs("validity")
        executor._replay = _pairs("replay")
        executor._rebuild = _pairs("rebuild")
        executor._materialization = _pairs("materialization")
        executor._payload_materialized = _pairs("payload_materialized")

        expected_state_keys = set(executor._registered)
        for mapping_name, mapping in (
            ("publication", executor._publication),
            ("validity", executor._validity),
            ("replay", executor._replay),
            ("rebuild", executor._rebuild),
            ("materialization", executor._materialization),
            ("payload_materialized", executor._payload_materialized),
        ):
            if set(mapping) != expected_state_keys:
                raise LearnedProductLifecycleConflict(
                    f"checkpoint {mapping_name} does not cover exact registered set"
                )

        for row in payload.get("invalidations", ()):
            receipt = InvalidationReceipt.from_dict(row)
            executor._invalidations[receipt.ref.key] = receipt
        for row in payload.get("rebuild_eligibility", ()):
            receipt = RebuildEligibilityReceipt.from_dict(row)
            executor._rebuild_eligibility[receipt.ref.key] = receipt
        for row in payload.get("rebuild_links", ()):
            receipt = RebuildLinkReceipt.from_dict(row)
            executor._rebuild_links[receipt.ref.key] = receipt
        for row in payload.get("gc_eligibility", ()):
            receipt = GCElegibilityReceipt.from_dict(row)
            executor._gc_eligibility[receipt.ref.key] = receipt
        executor._gc_recorded = {
            _exact(x).key for x in payload.get("gc_recorded_release_refs", ())
        }

        checkpoint_graph = LearnedProductDeterminantGraph.from_dict(
            payload["determinant_graph"]
        )
        if checkpoint_graph != executor.determinant_graph:
            raise LearnedProductLifecycleConflict(
                "checkpoint determinant graph differs from exact registered subjects"
            )

        replayed = executor.export_checkpoint()
        if replayed["checkpoint_hash"] != supplied_hash:
            raise LearnedProductLifecycleConflict(
                "fresh lifecycle replay checkpoint identity differs from original"
            )
        return executor

    def audit_replay(self) -> LifecycleReplayReceipt:
        original = self.export_checkpoint()
        replayed = self.from_checkpoint(original)
        replayed_checkpoint = replayed.export_checkpoint()
        return LifecycleReplayReceipt(
            original_checkpoint_hash=original["checkpoint_hash"],
            replayed_checkpoint_hash=replayed_checkpoint["checkpoint_hash"],
            event_refs=tuple(event.ref for event in self._events),
            selection_receipt_refs=tuple(
                receipt.ref for receipt in self._selection_receipts.values()
            ),
            no_current_receipt_refs=tuple(
                receipt.ref for receipt in self._no_current_receipts.values()
            ),
        )

    # Explicitly no source/carrier retirement or consumer-permission APIs.
    # Exact absence is part of the B5 owner boundary.


__all__ = [
    "LIFECYCLE_CONTRACT_ID",
    "LIFECYCLE_RUNTIME_SCHEMA",
    "LIFECYCLE_CHECKPOINT_SCHEMA",
    "PUBLICATION_STATES",
    "SELECTION_STATES",
    "VALIDITY_STATES",
    "REPLAY_STATES",
    "REBUILD_STATES",
    "MATERIALIZATION_CLASSES",
    "B5_EVENT_KINDS",
    "REFINEMENT_EVENT_KINDS",
    "FAIL_CLOSED_STATES",
    "DETERMINANT_CLASSES",
    "LearnedProductLifecycleError",
    "LearnedProductLifecycleConflict",
    "LearnedProductReleaseProtocol",
    "LearnedProductLifecycleSubject",
    "SelectionKey",
    "LearnedProductLifecycleEvent",
    "CurrentSelectionReceipt",
    "NoCurrentReceipt",
    "InvalidationReceipt",
    "RebuildEligibilityReceipt",
    "RebuildLinkReceipt",
    "GCElegibilityReceipt",
    "LifecycleState",
    "SelectionResolution",
    "LearnedProductDeterminantGraph",
    "LifecycleReplayReceipt",
    "LearnedProductLifecycleExecutor",
]
