"""HQ118 I2 — generic learned-product release / exact-resolution runtime.

This module implements the adopted M2 jurisdiction only:

    producer-owned exact subject
        -> immutable ReleaseCore
        -> immutable PublicationBinding (resolver/locator representation only)
        -> exact ResolutionReceipt

It deliberately does not implement lifecycle publication/currentness, semantic
adjudication, consumer permission, structural admission, or source semantics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    exact_ref,
    semantic_hash,
)

M2_CONTRACT_ID = "PRE553_LEARNED_PRODUCT_RELEASE_RUNTIME@1.0.0"
RELEASE_CORE_SCHEMA = "PRE553_M2_RELEASE_CORE@1.0.0"
PUBLICATION_BINDING_SCHEMA = "PRE553_M2_PUBLICATION_BINDING@1.0.0"
RESOLUTION_RECEIPT_SCHEMA = "PRE553_M2_RESOLUTION_RECEIPT@1.0.0"
CLOSURE_SCHEMA = "PRE553_M2_EXACT_CLOSURE@1.0.0"

SUBJECT_KINDS = frozenset({
    "IMMUTABLE_LEARNED_PRODUCT",
    "TYPED_DISPOSITION",
    "LEARNED_SERVICE_CONTRACT",
})
CLOSURE_KINDS = frozenset({
    "AUTHORITY",
    "DEPENDENCY",
    "DETERMINANT",
    "REPLAY_RECONSTRUCTION",
    "EXPLANATION_LINEAGE",
})
RESOLUTION_MODES = frozenset({
    "DIRECT_PRODUCER_REF",
    "CONTENT_ADDRESSED_MATERIALIZATION",
    "IMMUTABLE_REPOSITORY_LOCATOR",
    "GOVERNED_VIRTUAL_REBUILDER",
    "GOVERNED_SERVICE_RESOLVER",
})
REPLAY_GRADES = frozenset({
    "EXACT_MATERIALIZED_DEREFERENCE",
    "EXACT_DETERMINISTIC_REBUILD",
    "EXACT_SERVICE_REEXECUTION",
    "HISTORICAL_EXPLANATION_ONLY",
})
FORBIDDEN_SELECTOR_WORDS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "*",
})


class M2ReleaseError(Pre553IntegrityError):
    """Typed fail-closed M2 runtime error."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _fail(code: str, message: str) -> None:
    raise M2ReleaseError(code, message)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("RELEASE_CONTRACT_MISMATCH", f"{name} must be a non-empty string")
    return value.strip()


def _selector_forbidden(text: str) -> bool:
    upper = text.strip().upper()
    if upper in FORBIDDEN_SELECTOR_WORDS:
        return True
    probes = (
        ":LATEST", "/LATEST", "=LATEST",
        ":DEFAULT", "/DEFAULT", "=DEFAULT",
        ":FUZZY", "/FUZZY", "=FUZZY",
        ":NEAREST", "/NEAREST", "=NEAREST",
        ":SEMVER", "/SEMVER", "=SEMVER",
    )
    return any(probe in upper for probe in probes)


def _exact(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    if isinstance(value, str):
        _fail("FORBIDDEN_SELECTOR", f"{name} requires an exact ref, not selector text")
    try:
        ref = exact_ref(value, name)
    except (Pre553IntegrityError, TypeError, ValueError) as exc:
        _fail("RELEASE_SUBJECT_REF_NOT_EXACT", f"{name} is not an exact ref: {exc}")
    if _selector_forbidden(ref.kind) or _selector_forbidden(ref.object_id):
        _fail("FORBIDDEN_SELECTOR", f"{name} contains latest/default/fuzzy/nearest/semver selector")
    return ref


def _ref_key(ref: ExactRef) -> str:
    return ref.key


def _canonical_ref_set(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    refs = {_exact(value, name) for value in values}
    return tuple(sorted(refs, key=_ref_key))


def _ordered_refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    return tuple(_exact(value, name) for value in values)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    material = canonicalize(dict(value or {}))
    return MappingProxyType(material)


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:m2:{namespace}:sha256:{digest}",
        digest,
    )


M2_RELEASE_CONTRACT_REF = _derived_ref(
    "M2ReleaseContract",
    "release-contract",
    {
        "contract_id": M2_CONTRACT_ID,
        "schema": RELEASE_CORE_SCHEMA,
        "jurisdiction": "IMMUTABLE_RELEASE_CORE_ONLY",
    },
)
M2_PUBLICATION_CONTRACT_REF = _derived_ref(
    "M2PublicationBindingContract",
    "publication-binding-contract",
    {
        "contract_id": M2_CONTRACT_ID,
        "schema": PUBLICATION_BINDING_SCHEMA,
        "jurisdiction": "RESOLVER_LOCATOR_REPRESENTATION_ONLY",
        "lifecycle_publication_effect": False,
    },
)
M2_RESOLUTION_CONTRACT_REF = _derived_ref(
    "M2ResolutionContract",
    "resolution-contract",
    {
        "contract_id": M2_CONTRACT_ID,
        "schema": RESOLUTION_RECEIPT_SCHEMA,
        "exact_only": True,
        "latest_default_fuzzy_fallback": False,
    },
)


@dataclass(frozen=True)
class ClosureObject:
    closure_kind: str
    member_refs: tuple[ExactRef, ...]
    complete: bool
    ordering_semantics: str = "SET"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    closure_id: str = field(init=False)
    content_hash: str = field(init=False)

    def __post_init__(self) -> None:
        kind = _text(self.closure_kind, "closure_kind").upper()
        if kind not in CLOSURE_KINDS:
            _fail("RELEASE_CONTRACT_MISMATCH", f"unknown closure kind {kind!r}")
        ordering = _text(self.ordering_semantics, "ordering_semantics").upper()
        if ordering not in {"SET", "ORDERED"}:
            _fail("RELEASE_CONTRACT_MISMATCH", "closure ordering must be SET or ORDERED")
        members = (
            tuple(sorted(set(self.member_refs), key=_ref_key))
            if ordering == "SET"
            else tuple(self.member_refs)
        )
        if any(not isinstance(ref, ExactRef) for ref in members):
            _fail("RELEASE_SUBJECT_REF_NOT_EXACT", "closure members must be ExactRef")
        metadata = _freeze_mapping(self.metadata)
        projection = {
            "schema": CLOSURE_SCHEMA,
            "closure_kind": kind,
            "member_refs": [ref.as_dict() for ref in members],
            "complete": bool(self.complete),
            "ordering_semantics": ordering,
            "metadata": metadata,
        }
        digest = semantic_hash(projection)
        object.__setattr__(self, "closure_kind", kind)
        object.__setattr__(self, "member_refs", members)
        object.__setattr__(self, "ordering_semantics", ordering)
        object.__setattr__(self, "metadata", metadata)
        object.__setattr__(
            self,
            "closure_id",
            f"urn:rawlsing:pre553:m2:closure:{kind.lower()}:sha256:{digest}",
        )
        object.__setattr__(self, "content_hash", digest)

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M2Closure", self.closure_id, self.content_hash)


@dataclass(frozen=True)
class ProducerSubject:
    """M2 registration metadata for an already producer-owned exact subject."""

    ref: ExactRef
    subject_kind: str
    producer_contract_ref: ExactRef
    typed_state: str
    semantic_anatomy_ref: ExactRef
    required_authority_refs: tuple[ExactRef, ...] = ()
    required_dependency_refs: tuple[ExactRef, ...] = ()
    required_determinant_refs: tuple[ExactRef, ...] = ()
    required_replay_refs: tuple[ExactRef, ...] = ()
    required_explanation_refs: tuple[ExactRef, ...] = ()
    complete: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.ref, ExactRef):
            _fail("RELEASE_SUBJECT_REF_NOT_EXACT", "producer subject ref must be exact")
        kind = _text(self.subject_kind, "subject_kind").upper()
        if kind not in SUBJECT_KINDS:
            _fail("RELEASE_SUBJECT_KIND_MISMATCH", f"unsupported subject kind {kind!r}")
        if not isinstance(self.producer_contract_ref, ExactRef):
            _fail("PRODUCER_CONTRACT_MISMATCH", "producer contract ref must be exact")
        state = _text(self.typed_state, "typed_state")
        if not isinstance(self.semantic_anatomy_ref, ExactRef):
            _fail("RELEASE_SUBJECT_REF_NOT_EXACT", "semantic anatomy ref must be exact")
        object.__setattr__(self, "subject_kind", kind)
        object.__setattr__(self, "typed_state", state)
        for field_name in (
            "required_authority_refs",
            "required_dependency_refs",
            "required_determinant_refs",
            "required_replay_refs",
            "required_explanation_refs",
        ):
            refs = tuple(sorted(set(getattr(self, field_name)), key=_ref_key))
            if any(not isinstance(ref, ExactRef) for ref in refs):
                _fail("RELEASE_SUBJECT_REF_NOT_EXACT", f"{field_name} must contain exact refs")
            object.__setattr__(self, field_name, refs)


@dataclass(frozen=True)
class ReleaseCore:
    release_contract_ref: ExactRef
    release_subject_ref: ExactRef
    release_subject_kind: str
    semantic_producer_contract_ref: ExactRef
    authority_closure_ref: ExactRef
    dependency_closure_ref: ExactRef
    determinant_closure_ref: ExactRef
    replay_reconstruction_ref: ExactRef
    explanation_lineage_ref: ExactRef
    release_id: str = field(init=False)
    content_hash: str = field(init=False)

    def __post_init__(self) -> None:
        projection = self.semantic_projection()
        digest = semantic_hash(projection)
        object.__setattr__(
            self,
            "release_id",
            f"urn:rawlsing:pre553:m2:release:sha256:{digest}",
        )
        object.__setattr__(self, "content_hash", digest)

    def semantic_projection(self) -> Mapping[str, Any]:
        return {
            "schema": RELEASE_CORE_SCHEMA,
            "release_contract_ref": self.release_contract_ref.as_dict(),
            "release_subject_ref": self.release_subject_ref.as_dict(),
            "release_subject_kind": self.release_subject_kind,
            "semantic_producer_contract_ref": self.semantic_producer_contract_ref.as_dict(),
            "authority_closure_ref": self.authority_closure_ref.as_dict(),
            "dependency_closure_ref": self.dependency_closure_ref.as_dict(),
            "determinant_closure_ref": self.determinant_closure_ref.as_dict(),
            "replay_reconstruction_ref": self.replay_reconstruction_ref.as_dict(),
            "explanation_lineage_ref": self.explanation_lineage_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        return ExactRef("LearnedProductReleaseCore", self.release_id, self.content_hash)


@dataclass(frozen=True)
class RepresentationRecord:
    release_ref: ExactRef
    resolved_subject_ref: ExactRef
    producer_contract_ref: ExactRef
    resolution_mode: str
    resolver_or_locator_ref: ExactRef
    representation_integrity_ref: ExactRef
    representation_record_id: str = field(init=False)
    content_hash: str = field(init=False)

    def __post_init__(self) -> None:
        mode = _text(self.resolution_mode, "resolution_mode").upper()
        if mode not in RESOLUTION_MODES:
            _fail("RESOLVER_NOT_EXACT", f"unsupported resolution mode {mode!r}")
        projection = {
            "release_ref": self.release_ref.as_dict(),
            "resolved_subject_ref": self.resolved_subject_ref.as_dict(),
            "producer_contract_ref": self.producer_contract_ref.as_dict(),
            "resolution_mode": mode,
            "resolver_or_locator_ref": self.resolver_or_locator_ref.as_dict(),
            "representation_integrity_ref": self.representation_integrity_ref.as_dict(),
        }
        digest = semantic_hash(projection)
        object.__setattr__(self, "resolution_mode", mode)
        object.__setattr__(
            self,
            "representation_record_id",
            f"urn:rawlsing:pre553:m2:representation:sha256:{digest}",
        )
        object.__setattr__(self, "content_hash", digest)

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M2RepresentationRecord", self.representation_record_id, self.content_hash)


@dataclass(frozen=True)
class PublicationBinding:
    release_ref: ExactRef
    publication_contract_ref: ExactRef
    resolution_mode: str
    resolver_or_locator_ref: ExactRef
    representation_integrity_ref: ExactRef
    publication_binding_id: str = field(init=False)
    content_hash: str = field(init=False)

    def __post_init__(self) -> None:
        mode = _text(self.resolution_mode, "resolution_mode").upper()
        if mode not in RESOLUTION_MODES:
            _fail("RESOLVER_NOT_EXACT", f"unsupported resolution mode {mode!r}")
        projection = self.semantic_projection()
        digest = semantic_hash(projection)
        object.__setattr__(self, "resolution_mode", mode)
        object.__setattr__(
            self,
            "publication_binding_id",
            f"urn:rawlsing:pre553:m2:binding:sha256:{digest}",
        )
        object.__setattr__(self, "content_hash", digest)

    def semantic_projection(self) -> Mapping[str, Any]:
        return {
            "schema": PUBLICATION_BINDING_SCHEMA,
            "release_ref": self.release_ref.as_dict(),
            "publication_contract_ref": self.publication_contract_ref.as_dict(),
            "resolution_mode": self.resolution_mode,
            "resolver_or_locator_ref": self.resolver_or_locator_ref.as_dict(),
            "representation_integrity_ref": self.representation_integrity_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M2PublicationBinding", self.publication_binding_id, self.content_hash)


@dataclass(frozen=True)
class ResolutionReceipt:
    requested_release_ref: ExactRef
    attempted_publication_binding_refs: tuple[ExactRef, ...]
    used_publication_binding_ref: ExactRef | None
    resolved_release_core_ref: ExactRef
    resolved_release_subject_ref: ExactRef | None
    semantic_producer_contract_ref: ExactRef
    resolver_contract_ref: ExactRef
    resolution_state: str
    representation_integrity_state: str
    selector_substitution: bool = False
    lifecycle_publication_effect: bool = False
    current_selection_effect: bool = False
    consumer_permission_effect: bool = False
    resolution_receipt_id: str = field(init=False)
    content_hash: str = field(init=False)

    def __post_init__(self) -> None:
        projection = self.semantic_projection()
        digest = semantic_hash(projection)
        object.__setattr__(
            self,
            "resolution_receipt_id",
            f"urn:rawlsing:pre553:m2:resolution:sha256:{digest}",
        )
        object.__setattr__(self, "content_hash", digest)

    def semantic_projection(self) -> Mapping[str, Any]:
        return {
            "schema": RESOLUTION_RECEIPT_SCHEMA,
            "requested_release_ref": self.requested_release_ref.as_dict(),
            "attempted_publication_binding_refs": [
                ref.as_dict() for ref in self.attempted_publication_binding_refs
            ],
            "used_publication_binding_ref": (
                None if self.used_publication_binding_ref is None
                else self.used_publication_binding_ref.as_dict()
            ),
            "resolved_release_core_ref": self.resolved_release_core_ref.as_dict(),
            "resolved_release_subject_ref": (
                None if self.resolved_release_subject_ref is None
                else self.resolved_release_subject_ref.as_dict()
            ),
            "semantic_producer_contract_ref": self.semantic_producer_contract_ref.as_dict(),
            "resolver_contract_ref": self.resolver_contract_ref.as_dict(),
            "resolution_state": self.resolution_state,
            "representation_integrity_state": self.representation_integrity_state,
            "selector_substitution": self.selector_substitution,
            "lifecycle_publication_effect": self.lifecycle_publication_effect,
            "current_selection_effect": self.current_selection_effect,
            "consumer_permission_effect": self.consumer_permission_effect,
        }

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M2ResolutionReceipt", self.resolution_receipt_id, self.content_hash)


@dataclass(frozen=True)
class ResolutionResult:
    release_core: ReleaseCore
    subject: ProducerSubject | None
    receipt: ResolutionReceipt


@dataclass(frozen=True)
class ReleaseExplanation:
    release_ref: ExactRef
    release_subject_ref: ExactRef
    semantic_producer_contract_ref: ExactRef
    authority_closure_ref: ExactRef
    authority_members: tuple[ExactRef, ...]
    dependency_closure_ref: ExactRef
    dependency_members: tuple[ExactRef, ...]
    determinant_closure_ref: ExactRef
    determinant_members: tuple[ExactRef, ...]
    replay_reconstruction_ref: ExactRef
    replay_members: tuple[ExactRef, ...]
    explanation_lineage_ref: ExactRef
    explanation_members: tuple[ExactRef, ...]


class M2Repository:
    """In-memory exact-index runtime; indexes are nonauthoritative projections."""

    def __init__(self) -> None:
        self._subjects: dict[str, ProducerSubject] = {}
        self._closures: dict[str, ClosureObject] = {}
        self._releases: dict[str, ReleaseCore] = {}
        self._representations: dict[str, RepresentationRecord] = {}
        self._bindings: dict[str, PublicationBinding] = {}

    @staticmethod
    def _insert(store: dict[str, Any], ref: ExactRef, value: Any, code: str) -> Any:
        previous = store.get(ref.key)
        if previous is not None and previous != value:
            _fail(code, "exact identity collision with different preimage")
        store[ref.key] = value
        return value

    def register_subject(self, subject: ProducerSubject) -> ProducerSubject:
        if not isinstance(subject, ProducerSubject):
            _fail("RELEASE_SUBJECT_REF_NOT_EXACT", "subject registration requires ProducerSubject")
        return self._insert(
            self._subjects, subject.ref, subject, "SEMANTIC_REOWNERSHIP_ATTEMPT"
        )

    def register_closure(self, closure: ClosureObject) -> ClosureObject:
        if not isinstance(closure, ClosureObject):
            _fail("RELEASE_CONTRACT_MISMATCH", "closure registration requires ClosureObject")
        return self._insert(
            self._closures, closure.ref, closure, "RELEASE_ID_MISMATCH"
        )

    def register_release(self, release: ReleaseCore) -> ReleaseCore:
        return self._insert(self._releases, release.ref, release, "RELEASE_ID_MISMATCH")

    def register_representation(self, representation: RepresentationRecord) -> RepresentationRecord:
        return self._insert(
            self._representations,
            representation.resolver_or_locator_ref,
            representation,
            "REPRESENTATION_INTEGRITY_FAILURE",
        )

    def register_binding(self, binding: PublicationBinding) -> PublicationBinding:
        return self._insert(
            self._bindings, binding.ref, binding, "PUBLICATION_BINDING_MISMATCH"
        )

    def subject_exact(self, ref: ExactRef | Mapping[str, Any]) -> ProducerSubject:
        exact = _exact(ref, "release_subject_ref")
        value = self._subjects.get(exact.key)
        if value is None:
            _fail("RELEASE_SUBJECT_NOT_FOUND", "exact producer subject is not registered")
        return value

    def closure_exact(self, ref: ExactRef | Mapping[str, Any]) -> ClosureObject:
        exact = _exact(ref, "closure_ref")
        value = self._closures.get(exact.key)
        if value is None:
            _fail("RELEASE_ID_MISMATCH", "exact closure is unavailable")
        return value

    def release_exact(self, ref: ExactRef | Mapping[str, Any]) -> ReleaseCore:
        exact = _exact(ref, "release_ref")
        value = self._releases.get(exact.key)
        if value is None:
            _fail("RELEASE_UNAVAILABLE", "requested exact release is unavailable")
        _verify_release_core(value)
        return value

    def representation_exact(self, locator_ref: ExactRef | Mapping[str, Any]) -> RepresentationRecord:
        exact = _exact(locator_ref, "resolver_or_locator_ref")
        value = self._representations.get(exact.key)
        if value is None:
            _fail("RESOLVER_NOT_EXACT", "exact representation locator is unavailable")
        return value

    def binding_exact(self, ref: ExactRef | Mapping[str, Any]) -> PublicationBinding:
        exact = _exact(ref, "publication_binding_ref")
        value = self._bindings.get(exact.key)
        if value is None:
            _fail("PUBLICATION_BINDING_MISMATCH", "requested exact publication binding is unavailable")
        _verify_publication_binding(value)
        return value

    @property
    def releases(self) -> tuple[ReleaseCore, ...]:
        return tuple(sorted(self._releases.values(), key=lambda item: item.ref.key))


def register_producer_subject(
    repository: M2Repository,
    *,
    subject_ref: ExactRef | Mapping[str, Any],
    subject_kind: str,
    producer_contract_ref: ExactRef | Mapping[str, Any],
    typed_state: str,
    semantic_anatomy_ref: ExactRef | Mapping[str, Any] | None = None,
    required_authority_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    required_dependency_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    required_determinant_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    required_replay_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    required_explanation_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    complete: bool = True,
) -> ProducerSubject:
    if not isinstance(repository, M2Repository):
        _fail("RELEASE_CONTRACT_MISMATCH", "repository must be M2Repository")
    subject = _exact(subject_ref, "subject_ref")
    producer = _exact(producer_contract_ref, "producer_contract_ref")
    anatomy = subject if semantic_anatomy_ref is None else _exact(
        semantic_anatomy_ref, "semantic_anatomy_ref"
    )
    record = ProducerSubject(
        ref=subject,
        subject_kind=subject_kind,
        producer_contract_ref=producer,
        typed_state=typed_state,
        semantic_anatomy_ref=anatomy,
        required_authority_refs=_canonical_ref_set(required_authority_refs, "required_authority_ref"),
        required_dependency_refs=_canonical_ref_set(required_dependency_refs, "required_dependency_ref"),
        required_determinant_refs=_canonical_ref_set(required_determinant_refs, "required_determinant_ref"),
        required_replay_refs=_canonical_ref_set(required_replay_refs, "required_replay_ref"),
        required_explanation_refs=_canonical_ref_set(required_explanation_refs, "required_explanation_ref"),
        complete=bool(complete),
    )
    return repository.register_subject(record)


def constitute_closure(
    repository: M2Repository,
    *,
    closure_kind: str,
    member_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    complete: bool = True,
    ordering_semantics: str = "SET",
    metadata: Mapping[str, Any] | None = None,
) -> ClosureObject:
    ordering = _text(ordering_semantics, "ordering_semantics").upper()
    members = (
        _canonical_ref_set(member_refs, "closure_member_ref")
        if ordering == "SET"
        else _ordered_refs(member_refs, "closure_member_ref")
    )
    closure = ClosureObject(
        closure_kind=closure_kind,
        member_refs=members,
        complete=bool(complete),
        ordering_semantics=ordering,
        metadata=metadata or {},
    )
    return repository.register_closure(closure)


def _require_closure(
    repository: M2Repository,
    ref: ExactRef | Mapping[str, Any],
    kind: str,
    error_code: str,
) -> ClosureObject:
    closure = repository.closure_exact(ref)
    if closure.closure_kind != kind:
        _fail(error_code, f"expected {kind} closure, found {closure.closure_kind}")
    if not closure.complete:
        _fail(error_code, f"{kind} closure is explicitly incomplete")
    return closure


def _missing(required: Iterable[ExactRef], actual: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    actual_keys = {ref.key for ref in actual}
    return tuple(ref for ref in required if ref.key not in actual_keys)


def _require_members(
    closure: ClosureObject,
    required: Iterable[ExactRef],
    error_code: str,
    label: str,
) -> None:
    missing = _missing(required, closure.member_refs)
    if missing:
        _fail(
            error_code,
            f"{label} closure missing exact producer-required refs: "
            + ", ".join(ref.key for ref in missing),
        )


def constitute_release(
    repository: M2Repository,
    *,
    release_subject_ref: ExactRef | Mapping[str, Any],
    release_subject_kind: str,
    semantic_producer_contract_ref: ExactRef | Mapping[str, Any],
    authority_closure_ref: ExactRef | Mapping[str, Any],
    dependency_closure_ref: ExactRef | Mapping[str, Any],
    determinant_closure_ref: ExactRef | Mapping[str, Any],
    replay_reconstruction_ref: ExactRef | Mapping[str, Any],
    explanation_lineage_ref: ExactRef | Mapping[str, Any],
    release_contract_ref: ExactRef | Mapping[str, Any] = M2_RELEASE_CONTRACT_REF,
) -> ReleaseCore:
    contract = _exact(release_contract_ref, "release_contract_ref")
    if contract != M2_RELEASE_CONTRACT_REF:
        _fail("RELEASE_CONTRACT_MISMATCH", "release contract is not the adopted M2 runtime contract")
    subject_ref = _exact(release_subject_ref, "release_subject_ref")
    subject = repository.subject_exact(subject_ref)
    if not subject.complete:
        _fail("RELEASE_SUBJECT_NOT_FOUND", "producer subject is not complete at producer grain")
    requested_kind = _text(release_subject_kind, "release_subject_kind").upper()
    if requested_kind != subject.subject_kind:
        _fail("RELEASE_SUBJECT_KIND_MISMATCH", "requested subject kind differs from producer record")
    producer_ref = _exact(semantic_producer_contract_ref, "semantic_producer_contract_ref")
    if producer_ref != subject.producer_contract_ref:
        _fail("PRODUCER_CONTRACT_MISMATCH", "producer contract does not own this exact subject")

    authority = _require_closure(
        repository, authority_closure_ref, "AUTHORITY", "AUTHORITY_CLOSURE_INCOMPLETE"
    )
    dependency = _require_closure(
        repository, dependency_closure_ref, "DEPENDENCY", "DEPENDENCY_CLOSURE_INCOMPLETE"
    )
    determinant = _require_closure(
        repository, determinant_closure_ref, "DETERMINANT", "DETERMINANT_CLOSURE_INCOMPLETE"
    )
    replay = _require_closure(
        repository,
        replay_reconstruction_ref,
        "REPLAY_RECONSTRUCTION",
        "REPLAY_CLOSURE_INCOMPLETE",
    )
    explanation = _require_closure(
        repository,
        explanation_lineage_ref,
        "EXPLANATION_LINEAGE",
        "EXPLANATION_LINEAGE_INCOMPLETE",
    )

    _require_members(
        authority,
        (subject.producer_contract_ref,) + subject.required_authority_refs,
        "AUTHORITY_CLOSURE_INCOMPLETE",
        "authority",
    )
    _require_members(
        dependency,
        subject.required_dependency_refs,
        "DEPENDENCY_CLOSURE_INCOMPLETE",
        "dependency",
    )
    _require_members(
        determinant,
        subject.required_determinant_refs,
        "DETERMINANT_CLOSURE_INCOMPLETE",
        "determinant",
    )
    _require_members(
        replay,
        subject.required_replay_refs,
        "REPLAY_CLOSURE_INCOMPLETE",
        "replay",
    )
    _require_members(
        explanation,
        (subject.ref, subject.producer_contract_ref) + subject.required_explanation_refs,
        "EXPLANATION_LINEAGE_INCOMPLETE",
        "explanation",
    )
    replay_grade = replay.metadata.get("replay_grade")
    if replay_grade not in REPLAY_GRADES:
        _fail("REPLAY_CLOSURE_INCOMPLETE", "replay closure must declare one exact replay_grade")

    release = ReleaseCore(
        release_contract_ref=contract,
        release_subject_ref=subject.ref,
        release_subject_kind=subject.subject_kind,
        semantic_producer_contract_ref=subject.producer_contract_ref,
        authority_closure_ref=authority.ref,
        dependency_closure_ref=dependency.ref,
        determinant_closure_ref=determinant.ref,
        replay_reconstruction_ref=replay.ref,
        explanation_lineage_ref=explanation.ref,
    )
    return repository.register_release(release)


def _verify_release_core(release: ReleaseCore) -> None:
    expected = semantic_hash(release.semantic_projection())
    if release.content_hash != expected:
        _fail("RELEASE_ID_MISMATCH", "release core content hash mismatch")
    if release.release_id != f"urn:rawlsing:pre553:m2:release:sha256:{expected}":
        _fail("RELEASE_ID_MISMATCH", "release id does not match canonical preimage")
    if release.ref.content_hash != expected:
        _fail("RELEASE_ID_MISMATCH", "release exact ref is inconsistent")


def register_representation(
    repository: M2Repository,
    *,
    release_ref: ExactRef | Mapping[str, Any],
    resolution_mode: str,
    resolver_or_locator_ref: ExactRef | Mapping[str, Any],
    representation_integrity_ref: ExactRef | Mapping[str, Any],
    resolved_subject_ref: ExactRef | Mapping[str, Any],
    producer_contract_ref: ExactRef | Mapping[str, Any],
) -> RepresentationRecord:
    release = repository.release_exact(release_ref)
    mode = _text(resolution_mode, "resolution_mode").upper()
    if mode not in RESOLUTION_MODES:
        _fail("RESOLVER_NOT_EXACT", f"unsupported resolution mode {mode!r}")
    locator = _exact(resolver_or_locator_ref, "resolver_or_locator_ref")
    integrity = _exact(representation_integrity_ref, "representation_integrity_ref")
    resolved_subject = _exact(resolved_subject_ref, "resolved_subject_ref")
    producer = _exact(producer_contract_ref, "producer_contract_ref")
    if producer != release.semantic_producer_contract_ref:
        _fail("PRODUCER_CONTRACT_MISMATCH", "representation producer does not match release producer")
    if resolved_subject != release.release_subject_ref:
        code = (
            "REBUILD_SEMANTIC_MISMATCH"
            if mode in {"GOVERNED_VIRTUAL_REBUILDER", "GOVERNED_SERVICE_RESOLVER"}
            else "REPRESENTATION_INTEGRITY_FAILURE"
        )
        _fail(code, "representation resolves a different semantic subject")
    replay = repository.closure_exact(release.replay_reconstruction_ref)
    replay_grade = replay.metadata.get("replay_grade")
    if mode == "GOVERNED_VIRTUAL_REBUILDER" and replay_grade != "EXACT_DETERMINISTIC_REBUILD":
        _fail("REBUILD_UNAVAILABLE", "virtual rebuilder requires EXACT_DETERMINISTIC_REBUILD grade")
    if mode == "GOVERNED_SERVICE_RESOLVER" and replay_grade != "EXACT_SERVICE_REEXECUTION":
        _fail("REBUILD_UNAVAILABLE", "service resolver requires EXACT_SERVICE_REEXECUTION grade")
    record = RepresentationRecord(
        release_ref=release.ref,
        resolved_subject_ref=resolved_subject,
        producer_contract_ref=producer,
        resolution_mode=mode,
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    return repository.register_representation(record)


def publish_binding(
    repository: M2Repository,
    *,
    release_ref: ExactRef | Mapping[str, Any],
    resolution_mode: str,
    resolver_or_locator_ref: ExactRef | Mapping[str, Any],
    representation_integrity_ref: ExactRef | Mapping[str, Any],
    publication_contract_ref: ExactRef | Mapping[str, Any] = M2_PUBLICATION_CONTRACT_REF,
) -> PublicationBinding:
    release = repository.release_exact(release_ref)
    contract = _exact(publication_contract_ref, "publication_contract_ref")
    if contract != M2_PUBLICATION_CONTRACT_REF:
        _fail("PUBLICATION_BINDING_MISMATCH", "publication binding contract mismatch")
    mode = _text(resolution_mode, "resolution_mode").upper()
    locator = _exact(resolver_or_locator_ref, "resolver_or_locator_ref")
    integrity = _exact(representation_integrity_ref, "representation_integrity_ref")
    representation = repository.representation_exact(locator)
    if representation.release_ref != release.ref:
        _fail("PUBLICATION_BINDING_MISMATCH", "representation belongs to a different release")
    if representation.resolution_mode != mode:
        _fail("PUBLICATION_BINDING_MISMATCH", "resolution mode does not match representation")
    if representation.representation_integrity_ref != integrity:
        _fail("REPRESENTATION_INTEGRITY_FAILURE", "representation integrity ref mismatch")
    if representation.resolved_subject_ref != release.release_subject_ref:
        _fail("REPRESENTATION_INTEGRITY_FAILURE", "representation subject does not match release subject")
    binding = PublicationBinding(
        release_ref=release.ref,
        publication_contract_ref=contract,
        resolution_mode=mode,
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    return repository.register_binding(binding)


def _verify_publication_binding(binding: PublicationBinding) -> None:
    expected = semantic_hash(binding.semantic_projection())
    if binding.content_hash != expected:
        _fail("PUBLICATION_BINDING_MISMATCH", "publication binding content hash mismatch")
    if binding.publication_binding_id != f"urn:rawlsing:pre553:m2:binding:sha256:{expected}":
        _fail("PUBLICATION_BINDING_MISMATCH", "publication binding id mismatch")


def resolve_subject_exact(
    repository: M2Repository,
    release_ref: ExactRef | Mapping[str, Any],
) -> ProducerSubject:
    release = repository.release_exact(release_ref)
    subject = repository.subject_exact(release.release_subject_ref)
    if subject.producer_contract_ref != release.semantic_producer_contract_ref:
        _fail("PRODUCER_CONTRACT_MISMATCH", "release dereference no longer resolves its producer")
    if subject.subject_kind != release.release_subject_kind:
        _fail("RELEASE_SUBJECT_KIND_MISMATCH", "release dereference subject-kind mismatch")
    return subject


def _receipt(
    *,
    release: ReleaseCore,
    attempted_binding_refs: tuple[ExactRef, ...],
    used_binding_ref: ExactRef | None,
    subject_ref: ExactRef | None,
    resolution_state: str,
    integrity_state: str,
) -> ResolutionReceipt:
    return ResolutionReceipt(
        requested_release_ref=release.ref,
        attempted_publication_binding_refs=attempted_binding_refs,
        used_publication_binding_ref=used_binding_ref,
        resolved_release_core_ref=release.ref,
        resolved_release_subject_ref=subject_ref,
        semantic_producer_contract_ref=release.semantic_producer_contract_ref,
        resolver_contract_ref=M2_RESOLUTION_CONTRACT_REF,
        resolution_state=resolution_state,
        representation_integrity_state=integrity_state,
        selector_substitution=False,
        lifecycle_publication_effect=False,
        current_selection_effect=False,
        consumer_permission_effect=False,
    )


def resolve_release_exact(
    repository: M2Repository,
    release_ref: ExactRef | Mapping[str, Any],
    *,
    publication_binding_refs: Sequence[ExactRef | Mapping[str, Any]] = (),
    unavailable_binding_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
) -> ResolutionResult:
    release = repository.release_exact(release_ref)
    bindings = tuple(
        repository.binding_exact(ref) for ref in publication_binding_refs
    )
    for binding in bindings:
        if binding.release_ref != release.ref:
            _fail(
                "PUBLICATION_BINDING_MISMATCH",
                "endpoint failover list contains a binding for a different release",
            )
    unavailable = {
        _exact(ref, "unavailable_binding_ref").key for ref in unavailable_binding_refs
    }
    attempted_refs = tuple(binding.ref for binding in bindings)

    if not bindings:
        subject = resolve_subject_exact(repository, release.ref)
        receipt = _receipt(
            release=release,
            attempted_binding_refs=(),
            used_binding_ref=None,
            subject_ref=subject.ref,
            resolution_state="RESOLVED_EXACT_DIRECT_PRODUCER",
            integrity_state="VERIFIED",
        )
        return ResolutionResult(release, subject, receipt)

    chosen: PublicationBinding | None = None
    for binding in bindings:
        if binding.ref.key not in unavailable:
            chosen = binding
            break
    if chosen is None:
        receipt = _receipt(
            release=release,
            attempted_binding_refs=attempted_refs,
            used_binding_ref=None,
            subject_ref=None,
            resolution_state="RELEASE_UNAVAILABLE",
            integrity_state="NOT_EVALUATED",
        )
        return ResolutionResult(release, None, receipt)

    representation = repository.representation_exact(chosen.resolver_or_locator_ref)
    if representation.release_ref != release.ref:
        _fail("PUBLICATION_BINDING_MISMATCH", "binding resolved a representation for another release")
    if representation.representation_integrity_ref != chosen.representation_integrity_ref:
        _fail("REPRESENTATION_INTEGRITY_FAILURE", "binding/representation integrity mismatch")
    if representation.resolved_subject_ref != release.release_subject_ref:
        _fail("REBUILD_SEMANTIC_MISMATCH", "resolved representation changed semantic subject")
    if representation.producer_contract_ref != release.semantic_producer_contract_ref:
        _fail("PRODUCER_CONTRACT_MISMATCH", "resolved representation changed producer ownership")
    subject = resolve_subject_exact(repository, release.ref)
    receipt = _receipt(
        release=release,
        attempted_binding_refs=attempted_refs,
        used_binding_ref=chosen.ref,
        subject_ref=subject.ref,
        resolution_state="RESOLVED_EXACT_BINDING",
        integrity_state="VERIFIED",
    )
    return ResolutionResult(release, subject, receipt)


def explain_release(
    repository: M2Repository,
    release_ref: ExactRef | Mapping[str, Any],
) -> ReleaseExplanation:
    release = repository.release_exact(release_ref)
    authority = repository.closure_exact(release.authority_closure_ref)
    dependency = repository.closure_exact(release.dependency_closure_ref)
    determinant = repository.closure_exact(release.determinant_closure_ref)
    replay = repository.closure_exact(release.replay_reconstruction_ref)
    explanation = repository.closure_exact(release.explanation_lineage_ref)
    return ReleaseExplanation(
        release_ref=release.ref,
        release_subject_ref=release.release_subject_ref,
        semantic_producer_contract_ref=release.semantic_producer_contract_ref,
        authority_closure_ref=authority.ref,
        authority_members=authority.member_refs,
        dependency_closure_ref=dependency.ref,
        dependency_members=dependency.member_refs,
        determinant_closure_ref=determinant.ref,
        determinant_members=determinant.member_refs,
        replay_reconstruction_ref=replay.ref,
        replay_members=replay.member_refs,
        explanation_lineage_ref=explanation.ref,
        explanation_members=explanation.member_refs,
    )


def affected_release_refs(
    repository: M2Repository,
    changed_ref: ExactRef | Mapping[str, Any],
) -> tuple[ExactRef, ...]:
    """Graph-only affected set. No lifecycle event/currentness inference."""
    changed = _exact(changed_ref, "changed_ref")
    affected: list[ExactRef] = []
    for release in repository.releases:
        dependency = repository.closure_exact(release.dependency_closure_ref)
        determinant = repository.closure_exact(release.determinant_closure_ref)
        member_keys = {ref.key for ref in dependency.member_refs + determinant.member_refs}
        if changed.key in member_keys:
            affected.append(release.ref)
    return tuple(sorted(affected, key=_ref_key))


__all__ = [
    "M2_CONTRACT_ID",
    "RELEASE_CORE_SCHEMA",
    "PUBLICATION_BINDING_SCHEMA",
    "RESOLUTION_RECEIPT_SCHEMA",
    "CLOSURE_SCHEMA",
    "M2_RELEASE_CONTRACT_REF",
    "M2_PUBLICATION_CONTRACT_REF",
    "M2_RESOLUTION_CONTRACT_REF",
    "SUBJECT_KINDS",
    "CLOSURE_KINDS",
    "RESOLUTION_MODES",
    "REPLAY_GRADES",
    "M2ReleaseError",
    "ClosureObject",
    "ProducerSubject",
    "ReleaseCore",
    "RepresentationRecord",
    "PublicationBinding",
    "ResolutionReceipt",
    "ResolutionResult",
    "ReleaseExplanation",
    "M2Repository",
    "register_producer_subject",
    "constitute_closure",
    "constitute_release",
    "register_representation",
    "publish_binding",
    "resolve_release_exact",
    "resolve_subject_exact",
    "explain_release",
    "affected_release_refs",
]
