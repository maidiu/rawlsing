"""S2-G durable learned-product (M1/M2/B5) lifecycle custody adapter.

This module is deliberately an *external custody* seam, not a new M1/M2/B5
engine and not a scientific/current issuer.  It takes an already-produced
``LearnedWorldCompositionResult`` from the protected owners, stores its exact
M1 disposition / M2 release closure / B5 checkpoint and the selected B5 current
selection in an isolated content-addressed archive, and reopens that archive in
a fresh process.

The cold consumer path re-executes the *actual existing* N10E/C1 composition
owner using the accepted S2-F empirical closure (discovery route, no source
reread), then calls the actual existing
``evaluate_learned_world_consumer``.  A TEST_ONLY external issuer attestation is
required before any product is called CURRENT; a self-hash alone never grants
currentness.  Production issuer/host/original35 rights remain external holds.
"""
from __future__ import annotations

from dataclasses import dataclass, fields as dataclass_fields, is_dataclass
import hashlib
import os
from pathlib import Path
import shutil
from typing import Any, Iterable, Mapping, Sequence
import uuid
import zlib

from rawlsing_next.pre553_analytical_composition import (
    ConditionValueBindingWitness,
    _validate_discovery_consumption,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_durable_empirical_closure import (
    DurableEmpiricalClosure,
    open_empirical_closure,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_learned_empirical_adjudication import (
    LearnedEmpiricalDisposition,
    M1DeterminantExplanationReceipt,
)
from rawlsing_next.pre553_learned_product_lifecycle import (
    CurrentSelectionReceipt,
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
    LifecycleReplayReceipt,
    SelectionResolution,
)
from rawlsing_next.pre553_learned_product_release import (
    ClosureObject,
    M2Repository,
    ProducerSubject,
    ReleaseCore,
)
from rawlsing_next.pre553_learned_world_composition import (
    LearnedWorldCompositionReceipt,
    LearnedWorldCompositionResult,
    M2B5LifecycleProtocolView,
    M2ProductArtifacts,
    evaluate_learned_world_consumer,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    SpecificityWalkbackStep,
)


DURABLE_LEARNED_CONTRACT_ID = "PYAT960_S2G_DURABLE_LEARNED_LIFECYCLE@1.0.0"
DURABLE_LEARNED_SCHEMA = "PYAT960_S2G_DURABLE_LEARNED_ARTIFACT@1.0.0"
DURABLE_LEARNED_ROOT_SCHEMA = "PYAT960_S2G_DURABLE_LEARNED_ROOT@1.0.0"
DURABLE_LEARNED_CONTRACT_SHA = (
    "635a423beea158a67653d8c03ea7aee9c158f21986d4d598018d0976db73552b"
)
EVIDENCE_GRADE = "S2_SOURCEFREE_ISOLATED_FIXTURE"
RIGHTS_STATE = "HISTORICAL_LOCAL_REPLAY_ONLY__NO_EXTERNAL_CURRENT_MINTED"
CURRENT_TRUST = "TEST_ONLY_EXTERNAL_ISSUER_REQUIRED"
MANIFEST_NAME = "manifest.json"
BLOB_SUFFIX = ".json.z"
BLOB_DIR = "blobs"
ARTIFACT_DIR = "artifacts"
STAGING_PREFIX = ".staging-"


class DurableLearnedLifecycleError(ValueError):
    """The learned-product custody artifact is absent, corrupt, or inconsistent."""


class DurableLearnedLifecycleUntrusted(DurableLearnedLifecycleError):
    """The artifact has no independent external root/attestation pin."""


class DurableLearnedLifecycleRefusal(DurableLearnedLifecycleError):
    """A governed current/as-of/consumer refusal; not an integrity exception."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DurableLearnedLifecycleError(f"{name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DurableLearnedLifecycleError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise DurableLearnedLifecycleError(f"{name} must be a sequence")
    return value


def _exact(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except ValueError as exc:
        raise DurableLearnedLifecycleError(str(exc)) from exc


def _refs(values: Iterable[Any], name: str) -> tuple[ExactRef, ...]:
    return tuple(sorted({_exact(value, name) for value in values}, key=lambda r: r.key))


def _canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def _compress(value: Any) -> tuple[bytes, bytes]:
    raw = _canonical_bytes(value)
    return raw, zlib.compress(raw, 9)


def _decompress(blob: bytes) -> Any:
    import json

    return json.loads(zlib.decompress(blob).decode("utf-8"))


def _fsync_dir(path: Path) -> None:
    if not path.is_dir():
        return
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _cleanup_stale(root: Path) -> None:
    """Remove dead-publisher staging/tmp leftovers only."""
    blob_dir = root / BLOB_DIR
    artifact_dir = root / ARTIFACT_DIR
    for path in blob_dir.glob(".*.tmp-*") if blob_dir.is_dir() else ():
        tail = path.name.rsplit(".tmp-", 1)
        if len(tail) != 2:
            continue
        try:
            pid = int(tail[1].split("-", 1)[0])
        except ValueError:
            continue
        if not _pid_alive(pid):
            try:
                path.unlink()
            except OSError:
                pass
    for path in artifact_dir.glob(f"{STAGING_PREFIX}*") if artifact_dir.is_dir() else ():
        tail = path.name[len(STAGING_PREFIX):]
        try:
            pid = int(tail.split("-", 1)[0])
        except ValueError:
            continue
        if not _pid_alive(pid):
            shutil.rmtree(path, ignore_errors=True)


def _build(value: Any) -> Any:
    """Turn JSON material into exact refs/absence objects, recursively."""
    if isinstance(value, Mapping):
        keys = set(value)
        if keys == {"kind", "object_id", "content_hash"}:
            return ExactRef(**value)
        if keys == {"authority_id", "authority_version", "authority_content_hash"}:
            return AuthorityRef(**value)
        if keys == {"typed_absence_state", "detail"}:
            return TypedAbsence(value["typed_absence_state"], value["detail"])
        return {key: _build(item) for key, item in value.items()}
    if isinstance(value, list):
        return tuple(_build(item) for item in value)
    return value


def _generic_doc(value: Any) -> Mapping[str, Any]:
    if hasattr(value, "as_dict"):
        return canonicalize(value.as_dict())
    if is_dataclass(value):
        return canonicalize({
            field.name: getattr(value, field.name)
            for field in dataclass_fields(value)
            if field.init
        })
    raise DurableLearnedLifecycleError(
        f"cannot serialize exact object type {type(value).__name__}"
    )


def _construct(cls: type, document: Mapping[str, Any], *, extra: Mapping[str, Any] | None = None) -> Any:
    document = _mapping(document, cls.__name__)
    source = document.get("semantic_fields", document)
    source = _mapping(source, f"{cls.__name__}.semantic_fields")
    allowed = {field.name for field in dataclass_fields(cls) if field.init}
    kwargs = {
        key: _build(value) for key, value in source.items() if key in allowed
    }
    if extra:
        kwargs.update(extra)
    try:
        return cls(**kwargs)
    except Exception as exc:
        raise DurableLearnedLifecycleError(
            f"{cls.__name__} exact reconstruction failed: {exc}"
        ) from exc


def _verify_projection_document(document: Mapping[str, Any], expected_ref: ExactRef, label: str) -> None:
    item = _mapping(document, label)
    content_hash = _text(item.get("content_hash"), f"{label}.content_hash")
    projection = {
        key: item[key]
        for key in ("schema_id", "schema_version", "semantic_fields")
        if key in item
    }
    if semantic_hash(projection) != content_hash:
        raise DurableLearnedLifecycleError(f"{label} content hash mismatch")
    schema = item.get("schema_id")
    version = item.get("schema_version")
    object_id = item.get("object_id")
    if schema is None or version is None or object_id is None:
        raise DurableLearnedLifecycleError(f"{label} identity is incomplete")
    if ExactRef(f"{schema}@{version}", object_id, content_hash) != expected_ref:
        raise DurableLearnedLifecycleError(f"{label} ref mismatch")


def _m1_doc(disposition: LearnedEmpiricalDisposition) -> Mapping[str, Any]:
    return {
        "disposition": canonicalize(disposition.as_dict()),
        "determinant_receipt": canonicalize(
            disposition.determinant_explanation_receipt.as_dict()
        ),
    }


def _m1_from_doc(document: Mapping[str, Any]) -> LearnedEmpiricalDisposition:
    item = _mapping(document, "m1")
    receipt = _construct(
        M1DeterminantExplanationReceipt,
        _mapping(item.get("determinant_receipt"), "determinant_receipt"),
    )
    disposition = _construct(
        LearnedEmpiricalDisposition,
        _mapping(item.get("disposition"), "m1_disposition"),
        extra={"determinant_explanation_receipt": receipt},
    )
    return disposition


def _m2_docs(artifacts: M2ProductArtifacts) -> Mapping[str, Any]:
    names = (
        "subject",
        "authority_closure",
        "dependency_closure",
        "determinant_closure",
        "replay_closure",
        "explanation_closure",
        "release",
    )
    return {name: _generic_doc(getattr(artifacts, name)) for name in names}


def _m2_from_docs(document: Mapping[str, Any]) -> tuple[M2ProductArtifacts, M2Repository]:
    item = _mapping(document, "m2_artifacts")
    subject = _construct(ProducerSubject, _mapping(item.get("subject"), "subject"))
    closures = {
        name: _construct(ClosureObject, _mapping(item.get(name), name))
        for name in (
            "authority_closure",
            "dependency_closure",
            "determinant_closure",
            "replay_closure",
            "explanation_closure",
        )
    }
    release = _construct(ReleaseCore, _mapping(item.get("release"), "release"))
    repository = M2Repository()
    repository.register_subject(subject)
    for closure in closures.values():
        repository.register_closure(closure)
    repository.register_release(release)
    artifacts = M2ProductArtifacts(
        subject=subject,
        authority_closure=closures["authority_closure"],
        dependency_closure=closures["dependency_closure"],
        determinant_closure=closures["determinant_closure"],
        replay_closure=closures["replay_closure"],
        explanation_closure=closures["explanation_closure"],
        release=release,
    )
    return artifacts, repository


def _conditioner_doc(value: ConditionerBinding) -> Mapping[str, Any]:
    return canonicalize({
        "binding_id": value.binding_id,
        "subject_fact_ref": value.subject_fact_ref,
        "empirical_coordinate_ref": value.empirical_coordinate_ref,
        "comparability_authority_ref": value.comparability_authority_ref,
        "source_universe_ref": value.source_universe_ref,
        "release_ref": value.release_ref,
        "effective_time_or_interval": value.effective_time_or_interval,
    })


def _conditioner_from_doc(document: Mapping[str, Any]) -> ConditionerBinding:
    item = _mapping(document, "conditioner")
    return ConditionerBinding(
        binding_id=_text(item.get("binding_id"), "binding_id"),
        subject_fact_ref=_exact(item.get("subject_fact_ref"), "subject_fact_ref"),
        empirical_coordinate_ref=_exact(
            item.get("empirical_coordinate_ref"), "empirical_coordinate_ref"
        ),
        comparability_authority_ref=_build(item.get("comparability_authority_ref")),
        source_universe_ref=_exact(
            item.get("source_universe_ref"), "source_universe_ref"
        ),
        release_ref=_exact(item.get("release_ref"), "release_ref"),
        effective_time_or_interval=_build(item.get("effective_time_or_interval")),
    )


def _query_doc(value: PositionedSubjectPossibilityQuery) -> Mapping[str, Any]:
    return canonicalize({
        "query_id": value.query_id,
        "subject_ref": value.subject_ref,
        "target_ref": value.target_ref,
        "source_universe_ref": value.source_universe_ref,
        "release_ref": value.release_ref,
        "conditioner_bindings": [_conditioner_doc(b) for b in value.conditioner_bindings],
        "requested_projection": value.requested_projection,
        "purpose": value.purpose,
    })


def _query_from_doc(document: Mapping[str, Any]) -> PositionedSubjectPossibilityQuery:
    item = _mapping(document, "consumer_query")
    return PositionedSubjectPossibilityQuery(
        query_id=_text(item.get("query_id"), "query_id"),
        subject_ref=_exact(item.get("subject_ref"), "subject_ref"),
        target_ref=_exact(item.get("target_ref"), "target_ref"),
        source_universe_ref=_exact(
            item.get("source_universe_ref"), "source_universe_ref"
        ),
        release_ref=_exact(item.get("release_ref"), "release_ref"),
        conditioner_bindings=tuple(
            _conditioner_from_doc(value)
            for value in _sequence(item.get("conditioner_bindings"), "conditioners")
        ),
        requested_projection=_mapping(
            item.get("requested_projection"), "requested_projection"
        ),
        purpose=item.get("purpose", "EMPIRICAL_POSSIBILITY_ONLY"),
    )


def _step_doc(value: SpecificityWalkbackStep) -> Mapping[str, Any]:
    return _generic_doc(value)


def _step_from_doc(document: Mapping[str, Any]) -> SpecificityWalkbackStep:
    return _construct(SpecificityWalkbackStep, document)


def _model_doc(value: PositionedSubjectPossibilityModelRule) -> Mapping[str, Any]:
    return canonicalize({
        "model_authority_ref": value.model_authority_ref,
        "walkback_authority_ref": value.walkback_authority_ref,
        "source_universe_refs": value.source_universe_refs,
        "walkback_steps": [_step_doc(step) for step in value.walkback_steps],
        "positive_proxy_authority_refs": value.positive_proxy_authority_refs,
        "model_rule_id": value.model_rule_id,
        "algorithm_id": value.algorithm_id,
    })


def _model_from_doc(document: Mapping[str, Any]) -> PositionedSubjectPossibilityModelRule:
    item = _mapping(document, "model_rule")
    return PositionedSubjectPossibilityModelRule(
        model_authority_ref=_build(item.get("model_authority_ref")),
        walkback_authority_ref=_build(item.get("walkback_authority_ref")),
        source_universe_refs=_refs(item.get("source_universe_refs", ()), "source_universes"),
        walkback_steps=tuple(
            _step_from_doc(value)
            for value in _sequence(item.get("walkback_steps", ()), "walkback_steps")
        ),
        positive_proxy_authority_refs=tuple(
            _build(value)
            for value in _sequence(
                item.get("positive_proxy_authority_refs", ()),
                "positive_proxy_authority_refs",
            )
        ),
        model_rule_id=item.get("model_rule_id"),
        algorithm_id=item.get("algorithm_id"),
    )


def _witness_doc(value: ConditionValueBindingWitness) -> Mapping[str, Any]:
    return canonicalize({
        "witness_ref": value.witness_ref,
        "identity_material": value.identity_material,
        "subject_condition_preimage_refs": value.subject_condition_preimage_refs,
        "subject_condition_preimage_materials": value.subject_condition_preimage_materials,
        "producer_predicate_leaf_refs": value.producer_predicate_leaf_refs,
        "producer_predicate_leaf_projections": value.producer_predicate_leaf_projections,
        "pairing_ground_truth_refs": value.pairing_ground_truth_refs,
        "pairing_ground_truth_materials": value.pairing_ground_truth_materials,
        "pairing_authority_refs": value.pairing_authority_refs,
    })


def _witness_from_doc(document: Mapping[str, Any]) -> ConditionValueBindingWitness:
    item = _mapping(document, "witness")
    return ConditionValueBindingWitness(
        witness_ref=_exact(item.get("witness_ref"), "witness_ref"),
        identity_material=_mapping(item.get("identity_material"), "identity_material"),
        subject_condition_preimage_refs=_refs(
            item.get("subject_condition_preimage_refs", ()), "subject_preimages"
        ),
        subject_condition_preimage_materials=tuple(
            _mapping(value, "subject_preimage_material")
            for value in _sequence(
                item.get("subject_condition_preimage_materials", ()),
                "subject_preimage_materials",
            )
        ),
        producer_predicate_leaf_refs=_refs(
            item.get("producer_predicate_leaf_refs", ()), "leaf_refs"
        ),
        producer_predicate_leaf_projections=tuple(
            _mapping(value, "leaf_projection")
            for value in _sequence(
                item.get("producer_predicate_leaf_projections", ()),
                "leaf_projections",
            )
        ),
        pairing_ground_truth_refs=_refs(
            item.get("pairing_ground_truth_refs", ()), "pairing_refs"
        ),
        pairing_ground_truth_materials=tuple(
            _mapping(value, "pairing_material")
            for value in _sequence(
                item.get("pairing_ground_truth_materials", ()),
                "pairing_materials",
            )
        ),
        pairing_authority_refs=tuple(
            _build(value)
            for value in _sequence(
                item.get("pairing_authority_refs", ()), "pairing_authorities"
            )
        ),
    )


@dataclass(frozen=True)
class LearnedConsumerDeterminants:
    """Exact input determinants for the actual cold N10E/C1 consumer."""

    s2f_root_identity: str
    discovery_receipt_ref: ExactRef
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    release_ref: ExactRef
    consumer_query: PositionedSubjectPossibilityQuery
    model_rule: PositionedSubjectPossibilityModelRule
    condition_binding_witness: ConditionValueBindingWitness
    expected_composition_identity: str
    expected_consumer_result_hash: str | None
    purpose_ref: ExactRef

    def __post_init__(self) -> None:
        for name in (
            "s2f_root_identity",
            "expected_composition_identity",
        ):
            value = _text(getattr(self, name), name)
            if len(value) != 64:
                raise DurableLearnedLifecycleError(f"{name} must be sha256")
        if self.expected_consumer_result_hash is not None:
            _text(self.expected_consumer_result_hash, "expected_consumer_result_hash")
        for name in (
            "discovery_receipt_ref",
            "producer_query_ref",
            "producer_predicate_ref",
            "release_ref",
            "purpose_ref",
        ):
            object.__setattr__(self, name, _exact(getattr(self, name), name))
        if not isinstance(self.consumer_query, PositionedSubjectPossibilityQuery):
            raise DurableLearnedLifecycleError("exact consumer query required")
        if not isinstance(self.model_rule, PositionedSubjectPossibilityModelRule):
            raise DurableLearnedLifecycleError("exact model rule required")
        if not isinstance(self.condition_binding_witness, ConditionValueBindingWitness):
            raise DurableLearnedLifecycleError("exact condition witness required")

    def document(self) -> Mapping[str, Any]:
        return canonicalize({
            "s2f_root_identity": self.s2f_root_identity,
            "discovery_receipt_ref": self.discovery_receipt_ref,
            "producer_query_ref": self.producer_query_ref,
            "producer_predicate_ref": self.producer_predicate_ref,
            "release_ref": self.release_ref,
            "consumer_query": _query_doc(self.consumer_query),
            "model_rule": _model_doc(self.model_rule),
            "condition_binding_witness": _witness_doc(self.condition_binding_witness),
            "expected_composition_identity": self.expected_composition_identity,
            "expected_consumer_result_hash": self.expected_consumer_result_hash,
            "purpose_ref": self.purpose_ref,
        })

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "LearnedConsumerDeterminants":
        item = _mapping(document, "consumer_determinants")
        return cls(
            s2f_root_identity=_text(item.get("s2f_root_identity"), "s2f_root_identity"),
            discovery_receipt_ref=_exact(
                item.get("discovery_receipt_ref"), "discovery_receipt_ref"
            ),
            producer_query_ref=_exact(
                item.get("producer_query_ref"), "producer_query_ref"
            ),
            producer_predicate_ref=_exact(
                item.get("producer_predicate_ref"), "producer_predicate_ref"
            ),
            release_ref=_exact(item.get("release_ref"), "release_ref"),
            consumer_query=_query_from_doc(_mapping(item.get("consumer_query"), "consumer_query")),
            model_rule=_model_from_doc(_mapping(item.get("model_rule"), "model_rule")),
            condition_binding_witness=_witness_from_doc(
                _mapping(item.get("condition_binding_witness"), "witness")
            ),
            expected_composition_identity=_text(
                item.get("expected_composition_identity"),
                "expected_composition_identity",
            ),
            expected_consumer_result_hash=item.get("expected_consumer_result_hash"),
            purpose_ref=_exact(item.get("purpose_ref"), "purpose_ref"),
        )


@dataclass(frozen=True)
class LearnedPublishReceipt:
    artifact_path: str
    artifact_identity: str
    root_identity: str
    published: bool
    selection_receipt_ref: ExactRef | None
    selection_key_ref: ExactRef | None
    checkpoint_hash: str
    event_refs: tuple[ExactRef, ...]
    object_counts: Mapping[str, int]
    logical_bytes: int
    compressed_bytes: int
    manifest_bytes: int
    peak_scratch_bytes: int
    source_open_count: int
    evidence_grade: str = EVIDENCE_GRADE
    rights_state: str = RIGHTS_STATE

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "artifact_path": self.artifact_path,
            "artifact_identity": self.artifact_identity,
            "root_identity": self.root_identity,
            "published": self.published,
            "selection_receipt_ref": None
            if self.selection_receipt_ref is None
            else self.selection_receipt_ref.as_dict(),
            "selection_key_ref": None
            if self.selection_key_ref is None
            else self.selection_key_ref.as_dict(),
            "checkpoint_hash": self.checkpoint_hash,
            "event_refs": [ref.as_dict() for ref in self.event_refs],
            "object_counts": dict(self.object_counts),
            "logical_bytes": self.logical_bytes,
            "compressed_bytes": self.compressed_bytes,
            "manifest_bytes": self.manifest_bytes,
            "peak_scratch_bytes": self.peak_scratch_bytes,
            "source_open_count": self.source_open_count,
            "evidence_grade": self.evidence_grade,
            "rights_state": self.rights_state,
        }


@dataclass(frozen=True)
class ExternalCurrentAttestation:
    """TEST_ONLY external current/as-of attestation shape.

    A real production issuer must sign its own root.  This adapter only checks
    exact fields plus a caller-supplied independent root pin; it never treats a
    self-hash as current authority.
    """

    issuer_id: str
    artifact_root: str
    selection_key_ref: ExactRef
    selection_receipt_ref: ExactRef | None
    checkpoint_hash: str
    purpose_ref: ExactRef
    as_of_event_ref: ExactRef | None
    revoked: bool
    issued_at: str
    content_root: str

    def __post_init__(self) -> None:
        _text(self.issuer_id, "issuer_id")
        _text(self.artifact_root, "artifact_root")
        _text(self.checkpoint_hash, "checkpoint_hash")
        _text(self.issued_at, "issued_at")
        _text(self.content_root, "content_root")
        object.__setattr__(self, "selection_key_ref", _exact(self.selection_key_ref, "selection_key_ref"))
        if self.selection_receipt_ref is not None:
            object.__setattr__(
                self,
                "selection_receipt_ref",
                _exact(self.selection_receipt_ref, "selection_receipt_ref"),
            )
        object.__setattr__(self, "purpose_ref", _exact(self.purpose_ref, "purpose_ref"))
        if self.as_of_event_ref is not None:
            object.__setattr__(
                self, "as_of_event_ref", _exact(self.as_of_event_ref, "as_of_event_ref")
            )

    def material(self) -> Mapping[str, Any]:
        return canonicalize({
            "issuer_id": self.issuer_id,
            "artifact_root": self.artifact_root,
            "selection_key_ref": self.selection_key_ref,
            "selection_receipt_ref": self.selection_receipt_ref,
            "checkpoint_hash": self.checkpoint_hash,
            "purpose_ref": self.purpose_ref,
            "as_of_event_ref": self.as_of_event_ref,
            "revoked": self.revoked,
            "issued_at": self.issued_at,
        })

    @property
    def computed_root(self) -> str:
        return semantic_hash(self.material())


@dataclass(frozen=True)
class LearnedCurrentView:
    state: str
    selected_release_ref: ExactRef | None
    selection_receipt_ref: ExactRef | None
    checkpoint_hash: str
    attestation_root: str
    product_identity: str

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "state": self.state,
            "selected_release_ref": None
            if self.selected_release_ref is None
            else self.selected_release_ref.as_dict(),
            "selection_receipt_ref": None
            if self.selection_receipt_ref is None
            else self.selection_receipt_ref.as_dict(),
            "checkpoint_hash": self.checkpoint_hash,
            "attestation_root": self.attestation_root,
            "product_identity": self.product_identity,
        }


@dataclass(frozen=True)
class LearnedConsumerReceipt:
    state: str
    reason_code: str
    learned_receipt_ref: ExactRef
    m1_disposition_ref: ExactRef | None
    m2_release_ref: ExactRef | None
    b5_selection_receipt_ref: ExactRef | None
    composition_identity: str
    consumer_result_hash: str | None
    source_open_count: int
    material: Mapping[str, Any]


def _doc_ref(document: Mapping[str, Any], name: str) -> ExactRef:
    item = _mapping(document, name)
    schema = _text(item.get("schema_id"), f"{name}.schema_id")
    version = _text(item.get("schema_version"), f"{name}.schema_version")
    return ExactRef(
        f"{schema}@{version}",
        _text(item.get("object_id"), f"{name}.object_id"),
        _text(item.get("content_hash"), f"{name}.content_hash"),
    )


_M1_EVIDENCE_FAMILIES = (
    ("discovery_receipts", "DiscoveryResultReceipt@1.0.0"),
    ("empirical_facts", "EmpiricalFact@1.0.0"),
    ("empirical_queries", "EmpiricalQuerySpec@1.0.0"),
    ("empirical_predicates", "EmpiricalPredicate@1.0.0"),
)


def _bundle_evidence_refs(
    bundle_document: Mapping[str, Any],
) -> tuple[Mapping[str, Mapping[str, ExactRef]], set[str]]:
    """Extract exact evidence refs from the stored M1 input-bundle preimage."""

    bundle = _mapping(bundle_document, "m1_input_bundle")
    fields = _mapping(bundle.get("semantic_fields"), "m1_input_bundle.semantic_fields")
    evidence: dict[str, dict[str, ExactRef]] = {}
    for family, expected_kind in _M1_EVIDENCE_FAMILIES:
        rows = _sequence(fields.get(family, ()), family)
        refs: dict[str, ExactRef] = {}
        for row in rows:
            ref = _doc_ref(_mapping(row, family), family)
            if ref.kind != expected_kind:
                raise DurableLearnedLifecycleError(
                    f"M1 input bundle {family} contains {ref.kind}, expected {expected_kind}"
                )
            refs[ref.key] = ref
        evidence[family] = refs
    additional = {
        _exact(value, "m1 additional dependency").key
        for value in _sequence(
            fields.get("additional_dependency_refs", ()),
            "m1 additional dependency refs",
        )
    }
    return evidence, additional


def _core_document(
    learned: LearnedWorldCompositionResult,
    executor: LearnedProductLifecycleExecutor,
    determinants: LearnedConsumerDeterminants,
    m1_input_bundle: Mapping[str, Any] | None = None,
    m1_family_rule_binding: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    if not isinstance(learned, LearnedWorldCompositionResult):
        raise DurableLearnedLifecycleError("exact LearnedWorldCompositionResult required")
    if not isinstance(executor, LearnedProductLifecycleExecutor):
        raise DurableLearnedLifecycleError("exact B5 executor required")
    if not isinstance(determinants, LearnedConsumerDeterminants):
        raise DurableLearnedLifecycleError("exact consumer determinants required")
    if learned.receipt.terminal_state != "RULE_SATISFIED":
        raise DurableLearnedLifecycleError("only a productive learned result can be published")
    if learned.m1_disposition is None or learned.m2_artifacts is None:
        raise DurableLearnedLifecycleError("M1 disposition and M2 artifacts are required")
    if learned.b5_protocol_view is None or learned.b5_subject is None:
        raise DurableLearnedLifecycleError("B5 protocol view/subject are required")
    if m1_input_bundle is None or m1_family_rule_binding is None:
        raise DurableLearnedLifecycleError(
            "exact M1 input bundle and family rule binding preimages are required"
        )
    if m1_input_bundle is not None:
        bundle_ref = _exact(
            _mapping(m1_input_bundle, "m1_input_bundle").get("object_id") and {
                "kind": "M1AdjudicationInputBundle@1.0.0",
                "object_id": m1_input_bundle["object_id"],
                "content_hash": m1_input_bundle["content_hash"],
            },
            "m1_input_bundle_ref",
        )
        if bundle_ref != _exact(
            learned.m1_disposition.determinant_explanation_receipt.input_bundle_ref,
            "disposition input bundle",
        ):
            raise DurableLearnedLifecycleError("M1 input bundle differs from disposition")
        _verify_projection_document(m1_input_bundle, bundle_ref, "m1_input_bundle")
    rule_ref = _exact(
        _mapping(m1_family_rule_binding, "m1_family_rule_binding").get("object_id") and {
            "kind": "M1FamilyRuleBinding@1.0.0",
            "object_id": m1_family_rule_binding["object_id"],
            "content_hash": m1_family_rule_binding["content_hash"],
        },
        "m1_family_rule_binding_ref",
    )
    if rule_ref != _exact(
        learned.m1_disposition.family_rule_binding_ref, "disposition family rule"
    ):
        raise DurableLearnedLifecycleError("M1 family rule differs from disposition")
    _verify_projection_document(m1_family_rule_binding, rule_ref, "m1_family_rule_binding")
    checkpoint = executor.export_checkpoint()
    selection = learned.b5_selection_receipt
    release_ref = learned.m2_artifacts.release.ref
    if learned.m2_artifacts.subject.ref != learned.m1_disposition.ref:
        raise DurableLearnedLifecycleError("M2 subject/M1 disposition mismatch")
    if learned.receipt.m1_disposition_ref != learned.m1_disposition.ref:
        raise DurableLearnedLifecycleError("learned receipt/M1 disposition mismatch")
    if learned.receipt.m2_release_ref != release_ref:
        raise DurableLearnedLifecycleError("learned receipt/M2 release mismatch")
    if learned.b5_subject.release_ref != release_ref:
        raise DurableLearnedLifecycleError("B5 subject/M2 release mismatch")
    if learned.b5_protocol_view.release_ref != release_ref:
        raise DurableLearnedLifecycleError("B5 protocol/M2 release mismatch")
    if selection is not None:
        resolution = executor.resolve_selection_exact(
            selection.selection_key_ref, selection.ref
        )
        if (
            resolution.state != "CURRENT_SELECTED"
            or resolution.selected_release_ref != release_ref
        ):
            raise DurableLearnedLifecycleError(
                "B5 current selection does not resolve the retained M2 release"
            )
    # Event refs are in the canonical checkpoint payload.
    events = tuple(
        _exact(row["record_ref"], "lifecycle event")
        for row in checkpoint["checkpoint_payload"]["events"]
    )
    core = {
        "schema": DURABLE_LEARNED_SCHEMA,
        "contract": DURABLE_LEARNED_CONTRACT_ID,
        "contract_sha": DURABLE_LEARNED_CONTRACT_SHA,
        "evidence_grade": EVIDENCE_GRADE,
        "rights_state": RIGHTS_STATE,
        "current_trust": CURRENT_TRUST,
        "s2f_root_identity": determinants.s2f_root_identity,
        "consumer_determinants": determinants.document(),
        "m1": _m1_doc(learned.m1_disposition),
        "m1_evidence": {
            "input_bundle": None if m1_input_bundle is None else canonicalize(m1_input_bundle),
            "family_rule_binding": None
            if m1_family_rule_binding is None
            else canonicalize(m1_family_rule_binding),
        },
        "m2": _m2_docs(learned.m2_artifacts),
        "b5": {
            "checkpoint": checkpoint,
            "subject": _generic_doc(learned.b5_subject),
            "protocol_view": _generic_doc(learned.b5_protocol_view),
            "selection": None if selection is None else _generic_doc(selection),
            "replay": None
            if learned.b5_replay_receipt is None
            else _generic_doc(learned.b5_replay_receipt),
        },
        "learned_receipt": _generic_doc(learned.receipt),
        "purpose_ref": determinants.purpose_ref,
        "counts": {
            "events": len(events),
            "m2_closures": 5,
            "m1_determinant_material": len(
                learned.m1_disposition.determinant_explanation_receipt.determinant_manifest
            ),
        },
    }
    return canonicalize(core)


def _root_identity(artifact_identity: str, blob_hash: str) -> str:
    return semantic_hash({
        "schema": DURABLE_LEARNED_ROOT_SCHEMA,
        "artifact_identity": artifact_identity,
        "blob_hash": blob_hash,
    })


def publish_learned_lifecycle(
    root_dir: str | Path,
    *,
    learned: LearnedWorldCompositionResult,
    executor: LearnedProductLifecycleExecutor,
    determinants: LearnedConsumerDeterminants,
    m1_input_bundle: Mapping[str, Any] | None = None,
    m1_family_rule_binding: Mapping[str, Any] | None = None,
    expected_root: str | None = None,
    failpoint: Any | None = None,
) -> LearnedPublishReceipt:
    """Publish the exact M1/M2/B5 product and cold-consumer determinants once."""
    root = Path(root_dir)
    blob_dir = root / BLOB_DIR
    artifact_dir = root / ARTIFACT_DIR
    blob_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    _cleanup_stale(root)
    core = _core_document(
        learned,
        executor,
        determinants,
        m1_input_bundle=m1_input_bundle,
        m1_family_rule_binding=m1_family_rule_binding,
    )
    artifact_identity = semantic_hash(core)
    raw, compressed = _compress(core)
    blob_hash = hashlib.sha256(raw).hexdigest()
    if blob_hash != artifact_identity:
        raise DurableLearnedLifecycleError("learned artifact identity/hash drift")
    root_identity = _root_identity(artifact_identity, blob_hash)
    if expected_root is not None and expected_root != root_identity:
        raise DurableLearnedLifecycleError("external root pin does not match artifact")
    manifest = {
        "schema": DURABLE_LEARNED_SCHEMA,
        "contract": DURABLE_LEARNED_CONTRACT_ID,
        "contract_sha": DURABLE_LEARNED_CONTRACT_SHA,
        "publication": {
            "artifact_identity": artifact_identity,
            "root_identity": root_identity,
            "blob_hash": blob_hash,
            "compressed_bytes": len(compressed),
            "uncompressed_bytes": len(raw),
        },
    }
    manifest_raw = _canonical_bytes(manifest)
    artifact_path = artifact_dir / f"artifact-{artifact_identity}"
    checkpoint = core["b5"]["checkpoint"]
    selection_doc = core["b5"]["selection"]
    selection_ref = None
    selection_key_ref = None
    if selection_doc is not None:
        selection_ref = _exact(selection_doc.get("record_ref"), "selection_ref")
        selection_key_ref = _exact(
            selection_doc.get("selection_key_ref"), "selection_key_ref"
        )
    event_refs = tuple(
        _exact(row["record_ref"], "event ref")
        for row in checkpoint["checkpoint_payload"]["events"]
    )
    counts = dict(core["counts"])
    common = dict(
        artifact_path=str(artifact_path),
        artifact_identity=artifact_identity,
        root_identity=root_identity,
        selection_receipt_ref=selection_ref,
        selection_key_ref=selection_key_ref,
        checkpoint_hash=checkpoint["checkpoint_hash"],
        event_refs=event_refs,
        object_counts=counts,
        logical_bytes=len(raw),
        compressed_bytes=len(compressed),
        manifest_bytes=len(manifest_raw),
        source_open_count=0,
    )
    if artifact_path.exists():
        existing = _read_json(artifact_path / MANIFEST_NAME)
        if existing.get("publication", {}).get("root_identity") != root_identity:
            raise DurableLearnedLifecycleError("artifact identity already has a different root")
        open_learned_lifecycle(artifact_path, expected_root=root_identity).require_trusted()
        return LearnedPublishReceipt(
            **{**common, "published": False, "peak_scratch_bytes": 0}
        )
    staged = artifact_dir / f"{STAGING_PREFIX}{os.getpid()}-{uuid.uuid4().hex}"
    staged.mkdir(parents=False, exist_ok=False)
    scratch_peak = 0
    try:
        blob_path = blob_dir / f"{blob_hash}{BLOB_SUFFIX}"
        if blob_path.exists():
            existing = _read_blob(blob_path, blob_hash, {
                "compressed_bytes": len(compressed),
                "uncompressed_bytes": len(raw),
            })
            if canonical_json(existing) != canonical_json(core):
                raise DurableLearnedLifecycleError("existing artifact blob content drift")
        else:
            tmp = blob_path.with_name(
                f".{blob_path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
            )
            try:
                with open(tmp, "wb") as handle:
                    handle.write(compressed)
                    handle.flush()
                    os.fsync(handle.fileno())
                scratch_peak = max(scratch_peak, len(compressed))
                os.replace(tmp, blob_path)
            finally:
                if tmp.exists():
                    tmp.unlink()
        _fsync_dir(blob_dir)
        if failpoint is not None:
            failpoint("after_blob_write")
        with open(staged / MANIFEST_NAME, "wb") as handle:
            handle.write(manifest_raw)
            handle.flush()
            os.fsync(handle.fileno())
        scratch_peak = max(scratch_peak, len(manifest_raw))
        _fsync_dir(staged)
        if failpoint is not None:
            failpoint("before_manifest_replace")
        os.replace(staged, artifact_path)
        _fsync_dir(artifact_dir)
    except Exception:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)
        raise
    finally:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)
    return LearnedPublishReceipt(
        **{**common, "published": True, "peak_scratch_bytes": scratch_peak}
    )


def _read_json(path: Path) -> Mapping[str, Any]:
    import json

    try:
        with open(path, "rb") as handle:
            value = json.loads(handle.read().decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise DurableLearnedLifecycleError(f"learned artifact file cannot be read: {path}") from exc
    if not isinstance(value, Mapping):
        raise DurableLearnedLifecycleError(f"learned artifact file is not a mapping: {path}")
    return value


def _read_blob(path: Path, expected_hash: str, entry: Mapping[str, Any]) -> Any:
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        raise DurableLearnedLifecycleError(f"learned artifact blob is missing: {path.name}") from exc
    try:
        value = _decompress(data)
    except Exception as exc:
        raise DurableLearnedLifecycleError("learned artifact blob is not decodable") from exc
    raw = _canonical_bytes(value)
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise DurableLearnedLifecycleError("learned artifact blob hash drift")
    if int(entry.get("compressed_bytes", len(data))) != len(data):
        raise DurableLearnedLifecycleError("learned artifact blob compressed size drift")
    if int(entry.get("uncompressed_bytes", len(raw))) != len(raw):
        raise DurableLearnedLifecycleError("learned artifact blob uncompressed size drift")
    return value


@dataclass(frozen=True)
class DurableLearnedLifecycle:
    artifact_path: Path
    artifact_identity: str
    root_identity: str
    trust_state: str
    core: Mapping[str, Any]
    m1_disposition: LearnedEmpiricalDisposition
    m2_artifacts: M2ProductArtifacts
    m2_repository: M2Repository
    b5_executor: LearnedProductLifecycleExecutor
    b5_subject: LearnedProductLifecycleSubject
    b5_protocol_view: M2B5LifecycleProtocolView
    b5_selection_receipt: CurrentSelectionReceipt | None
    b5_replay_receipt: LifecycleReplayReceipt | None
    learned_receipt: LearnedWorldCompositionReceipt
    determinants: LearnedConsumerDeterminants

    @property
    def exact_ref(self) -> ExactRef:
        return ExactRef(
            "PYAT960_S2G_DURABLE_LEARNED_ARTIFACT@1.0.0",
            f"urn:rawlsing:pyat960:s2g:artifact:sha256:{self.root_identity}",
            self.root_identity,
        )

    def require_trusted(self) -> "DurableLearnedLifecycle":
        if self.trust_state != "EXTERNALLY_PINNED":
            raise DurableLearnedLifecycleUntrusted(
                "learned artifact has no independent external root pin"
            )
        return self

    def learned_result(self) -> LearnedWorldCompositionResult:
        return LearnedWorldCompositionResult(
            receipt=self.learned_receipt,
            m1_disposition=self.m1_disposition,
            m2_artifacts=self.m2_artifacts,
            b5_protocol_view=self.b5_protocol_view,
            b5_subject=self.b5_subject,
            b5_selection_receipt=self.b5_selection_receipt,
            b5_replay_receipt=self.b5_replay_receipt,
        )

    def _m1_evidence_binding(self, closure: DurableEmpiricalClosure) -> None:
        """Require the retained M1 product to be drawn from the declared S2-F closure.

        A cold consumer that reuses a different native evidence chain would
        otherwise be able to serve an M1 disposition/M2/B5 product against an
        unrelated S2-F closure whenever the producer predicate and source
        universe happen to overlap.  The bundle, the disposition refs, the
        consumer receipt/query/predicate and the source release must all be
        exact members of the same retained closure.
        """

        evidence = _mapping(self.core.get("m1_evidence"), "m1_evidence")
        bundle = _mapping(evidence.get("input_bundle"), "m1_input_bundle")
        bundle_refs, additional_refs = _bundle_evidence_refs(bundle)
        closure_refs = {
            "discovery_receipts": {
                obj.ref.key: obj.ref for obj in closure.object_graph.discovery_receipts
            },
            "empirical_facts": {
                obj.ref.key: obj.ref for obj in closure.object_graph.empirical_facts
            },
            "empirical_queries": {
                obj.ref.key: obj.ref for obj in closure.object_graph.executed_queries
            },
            "empirical_predicates": {
                obj.ref.key: obj.ref for obj in closure.object_graph.executed_predicates
            },
        }
        for family, _ in _M1_EVIDENCE_FAMILIES:
            missing = [
                key for key in bundle_refs[family] if key not in closure_refs[family]
            ]
            if missing:
                raise DurableLearnedLifecycleError(
                    f"M1 input bundle {family} is not drawn from the declared S2F closure"
                )
        disposition_refs = {
            "discovery_receipts": {
                ref.key for ref in self.m1_disposition.discovery_result_receipt_refs
            },
            "empirical_facts": {
                ref.key for ref in self.m1_disposition.empirical_fact_refs
            },
            "empirical_queries": {
                ref.key for ref in self.m1_disposition.empirical_query_spec_refs
            },
            "empirical_predicates": {
                ref.key for ref in self.m1_disposition.empirical_predicate_refs
            },
        }
        for family, _ in _M1_EVIDENCE_FAMILIES:
            if not disposition_refs[family].issubset(bundle_refs[family]):
                raise DurableLearnedLifecycleError(
                    f"M1 disposition {family} are not a subset of the retained input bundle"
                )
            if not disposition_refs[family].issubset(closure_refs[family]):
                raise DurableLearnedLifecycleError(
                    f"M1 disposition {family} are not drawn from the declared S2F closure"
                )
        if self.determinants.discovery_receipt_ref.key not in disposition_refs[
            "discovery_receipts"
        ]:
            raise DurableLearnedLifecycleError(
                "consumer discovery receipt is absent from the M1 evidence chain"
            )
        if self.determinants.producer_query_ref.key not in disposition_refs[
            "empirical_queries"
        ]:
            raise DurableLearnedLifecycleError(
                "consumer producer query is absent from the M1 evidence chain"
            )
        if self.determinants.producer_predicate_ref.key not in disposition_refs[
            "empirical_predicates"
        ]:
            raise DurableLearnedLifecycleError(
                "consumer producer predicate is absent from the M1 evidence chain"
            )
        closure_receipts = {
            obj.ref.key: obj for obj in closure.object_graph.discovery_receipts
        }
        closure_fact_keys = set(closure_refs["empirical_facts"])
        disposition_validation_keys = {
            ref.key for ref in self.m1_disposition.validation_fact_refs
        }
        for receipt_ref in self.m1_disposition.discovery_result_receipt_refs:
            receipt = closure_receipts.get(receipt_ref.key)
            if receipt is None:
                raise DurableLearnedLifecycleError(
                    "M1 disposition discovery receipt is absent from the declared S2F closure"
                )
            receipt_empirical_keys = {
                _exact(dict(ref), "receipt empirical fact").key
                for ref in receipt.empirical_fact_refs
            }
            receipt_validation_keys = {
                _exact(dict(ref), "receipt validation fact").key
                for ref in getattr(receipt, "validation_fact_refs", ())
            }
            if not receipt_empirical_keys.issubset(
                disposition_refs["empirical_facts"]
            ):
                raise DurableLearnedLifecycleError(
                    "M1 disposition omits an empirical fact owned by a retained discovery receipt"
                )
            if not receipt_validation_keys.issubset(disposition_validation_keys):
                raise DurableLearnedLifecycleError(
                    "M1 disposition omits a validation fact owned by a retained discovery receipt"
                )
            if not (
                receipt_empirical_keys | receipt_validation_keys
            ).issubset(bundle_refs["empirical_facts"]):
                raise DurableLearnedLifecycleError(
                    "M1 input bundle omits a fact owned by a retained discovery receipt"
                )
            if not (
                receipt_empirical_keys | receipt_validation_keys
            ).issubset(closure_fact_keys):
                raise DurableLearnedLifecycleError(
                    "retained discovery receipt fact is absent from the declared S2F closure"
                )
        if self.determinants.release_ref.key not in additional_refs:
            raise DurableLearnedLifecycleError(
                "consumer source release is absent from the M1 input bundle"
            )
        if _doc_ref(bundle, "m1_input_bundle") != _exact(
            self.m1_disposition.determinant_explanation_receipt.input_bundle_ref,
            "m1 disposition input bundle",
        ):
            raise DurableLearnedLifecycleError(
                "M1 input bundle preimage differs from the retained disposition"
            )

    def consumer_composition(
        self,
        s2f_closure_path: str | Path,
    ) -> tuple[Any, ExactRef, ExactRef, int]:
        """Re-run the actual C1/N10E composition from the accepted S2F closure."""
        self.require_trusted()
        closure = open_empirical_closure(
            s2f_closure_path,
            expected_root=self.determinants.s2f_root_identity,
        ).require_trusted()
        self._m1_evidence_binding(closure)
        receipt = next(
            (
                item
                for item in closure.i05_result.receipts
                if item.ref == self.determinants.discovery_receipt_ref
            ),
            None,
        )
        if receipt is None:
            raise DurableLearnedLifecycleError("declared discovery receipt is absent from S2F closure")
        receipt_releases = {
            _exact(dict(ref), "receipt source release").key
            for ref in receipt.source_release_refs
        }
        if self.determinants.release_ref.key not in receipt_releases:
            raise DurableLearnedLifecycleError(
                "declared consumer release is not owned by the discovery receipt"
            )
        if self.determinants.release_ref not in {
            identity.release_ref for identity in closure.release_identities
        }:
            raise DurableLearnedLifecycleError(
                "declared consumer release is absent from S2F closure"
            )
        fact, predicate, query = _validate_discovery_consumption(
            discovery_result=closure.i05_result,
            consumer_query=self.determinants.consumer_query,
            receipt_ref=receipt.ref,
        )
        selected_fact_releases = {
            _exact(dict(ref), "selected fact source release").key
            for ref in fact.source_empirical_provenance_refs
            if _exact(dict(ref), "selected fact source release").kind
            == "C11LogicalRelease"
        }
        if self.determinants.release_ref.key not in selected_fact_releases:
            raise DurableLearnedLifecycleRefusal(
                "consumer determinant release is not the selected fact source release"
            )
        if predicate.ref != self.determinants.producer_predicate_ref:
            raise DurableLearnedLifecycleError("cold producer predicate differs from declared")
        if query.ref != self.determinants.producer_query_ref:
            raise DurableLearnedLifecycleError("cold producer query differs from declared")
        registry = AuthorityRegistry(closure.object_graph.authority_snapshots)
        composition = compose_positioned_subject_possibility(
            repository=None,
            empirical_query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(self.determinants.release_ref,),
            consumer_query=self.determinants.consumer_query,
            model_rule=self.determinants.model_rule,
            condition_binding_witness=self.determinants.condition_binding_witness,
            discovery_result=closure.i05_result,
            discovery_receipt_ref=receipt.ref,
        )
        if composition.composed_result_identity_hash != self.determinants.expected_composition_identity:
            raise DurableLearnedLifecycleError("cold composition identity differs from declared")
        return composition, predicate.ref, query.ref, len(closure.object_graph.empirical_facts)

    def consume(
        self,
        s2f_closure_path: str | Path,
        *,
        require_current_selection: bool = True,
    ) -> LearnedConsumerReceipt:
        """Run the actual existing `evaluate_learned_world_consumer` cold."""
        self.require_trusted()
        composition, predicate_ref, query_ref, _ = self.consumer_composition(
            s2f_closure_path
        )
        learned = self.learned_result()
        result = evaluate_learned_world_consumer(
            learned,
            composition=composition,
            consumer_query=self.determinants.consumer_query,
            model_rule=self.determinants.model_rule,
            producer_query_ref=query_ref,
            producer_predicate_ref=predicate_ref,
            require_current_selection=require_current_selection,
        )
        if (
            self.determinants.expected_consumer_result_hash is not None
            and result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
            and result.consumer_result is not None
            and result.consumer_result.result_hash != self.determinants.expected_consumer_result_hash
        ):
            raise DurableLearnedLifecycleError("cold consumer result hash differs from declared")
        return LearnedConsumerReceipt(
            state=result.state,
            reason_code=result.reason_code,
            learned_receipt_ref=result.learned_receipt_ref,
            m1_disposition_ref=result.m1_disposition_ref,
            m2_release_ref=result.m2_release_ref,
            b5_selection_receipt_ref=result.b5_selection_receipt_ref,
            composition_identity=composition.composed_result_identity_hash,
            consumer_result_hash=None
            if result.consumer_result is None
            else result.consumer_result.result_hash,
            source_open_count=0,
            material=canonicalize(result.material()),
        )

    def consume_current(
        self,
        s2f_closure_path: str | Path,
        *,
        attestation: ExternalCurrentAttestation,
        expected_attestation_root: str | None,
    ) -> tuple[LearnedCurrentView, LearnedConsumerReceipt]:
        """Require externally attested currentness before serving the product."""
        current = self.resolve_current(
            attestation, expected_attestation_root=expected_attestation_root
        )
        return current, self.consume(
            s2f_closure_path, require_current_selection=True
        )

    def resolve_current(
        self,
        attestation: ExternalCurrentAttestation,
        *,
        expected_attestation_root: str | None,
    ) -> LearnedCurrentView:
        """Require a TEST_ONLY externally pinned current attestation."""
        self.require_trusted()
        if not isinstance(attestation, ExternalCurrentAttestation):
            raise DurableLearnedLifecycleError("exact external current attestation required")
        if expected_attestation_root is None:
            raise DurableLearnedLifecycleUntrusted(
                "current attestation has no independent external pin"
            )
        if expected_attestation_root != attestation.content_root:
            raise DurableLearnedLifecycleError("current attestation external pin mismatch")
        if attestation.content_root != attestation.computed_root:
            raise DurableLearnedLifecycleError("current attestation self-hash mismatch")
        if attestation.artifact_root != self.root_identity:
            raise DurableLearnedLifecycleError("current attestation artifact root mismatch")
        if attestation.revoked:
            raise DurableLearnedLifecycleRefusal("current attestation is revoked")
        if attestation.purpose_ref != self.determinants.purpose_ref:
            raise DurableLearnedLifecycleRefusal("current attestation purpose mismatch")
        if attestation.checkpoint_hash != self.b5_executor.export_checkpoint()["checkpoint_hash"]:
            raise DurableLearnedLifecycleRefusal("current attestation checkpoint is stale")
        if self.b5_selection_receipt is None:
            raise DurableLearnedLifecycleRefusal("NO_CURRENT: no selected product")
        if attestation.selection_key_ref != self.b5_selection_receipt.selection_key_ref:
            raise DurableLearnedLifecycleRefusal("current attestation selection key mismatch")
        if attestation.selection_receipt_ref != self.b5_selection_receipt.ref:
            raise DurableLearnedLifecycleRefusal("current attestation selection receipt mismatch")
        events = {
            _exact(row["record_ref"], "event ref").key: row
            for row in self.b5_executor.export_checkpoint()["checkpoint_payload"]["events"]
        }
        if attestation.as_of_event_ref is not None and attestation.as_of_event_ref.key not in events:
            raise DurableLearnedLifecycleRefusal("current attestation as-of event is unavailable")
        if attestation.as_of_event_ref is not None:
            current_event = events.get(self.b5_selection_receipt.current_select_event_ref.key)
            as_of_event = events[attestation.as_of_event_ref.key]
            if current_event is None:
                raise DurableLearnedLifecycleRefusal("current selection event is unavailable")
            if int(as_of_event["ordinal"]) < int(current_event["ordinal"]):
                raise DurableLearnedLifecycleRefusal(
                    "current attestation as-of predates the current selection"
                )
        resolution = self.b5_executor.resolve_selection_exact(
            attestation.selection_key_ref, attestation.selection_receipt_ref
        )
        if resolution.state != "CURRENT_SELECTED" or resolution.selected_release_ref is None:
            raise DurableLearnedLifecycleRefusal("attested selection is not CURRENT_SELECTED")
        if resolution.selected_release_ref != self.m2_artifacts.release.ref:
            raise DurableLearnedLifecycleRefusal(
                "attested current release differs from retained M2 release"
            )
        return LearnedCurrentView(
            state=resolution.state,
            selected_release_ref=resolution.selected_release_ref,
            selection_receipt_ref=resolution.receipt_ref,
            checkpoint_hash=attestation.checkpoint_hash,
            attestation_root=attestation.content_root,
            product_identity=self.m2_artifacts.release.ref.content_hash,
        )

    def resolve_as_of_checkpoint(
        self,
        checkpoint: Mapping[str, Any],
        *,
        expected_checkpoint_hash: str | None = None,
    ) -> SelectionResolution:
        """Exact historical checkpoint replay; the caller pins its hash.

        The checkpoint must be a prefix of the artifact's retained event/history
        chain.  A coherently self-rehashed foreign checkpoint is not an
        independent authority and is refused even when its own hash is supplied.
        """

        self.require_trusted()
        if expected_checkpoint_hash is None:
            raise DurableLearnedLifecycleUntrusted(
                "as-of checkpoint has no independent external pin"
            )
        document = _mapping(checkpoint, "as_of_checkpoint")
        supplied = _text(document.get("checkpoint_hash"), "checkpoint_hash")
        if supplied != expected_checkpoint_hash:
            raise DurableLearnedLifecycleRefusal(
                "as-of checkpoint external hash pin mismatch"
            )
        if self.b5_selection_receipt is None:
            raise DurableLearnedLifecycleRefusal(
                "NO_CURRENT: no selected product history is present"
            )
        retained = self.b5_executor.export_checkpoint()
        retained_payload = _mapping(
            retained.get("checkpoint_payload"), "retained checkpoint payload"
        )
        supplied_payload = _mapping(
            document.get("checkpoint_payload"), "as-of checkpoint payload"
        )
        retained_events = tuple(
            _exact(row["record_ref"], "retained event").key
            for row in _sequence(retained_payload.get("events", ()), "retained events")
        )
        supplied_events = tuple(
            _exact(row["record_ref"], "as-of event").key
            for row in _sequence(supplied_payload.get("events", ()), "as-of events")
        )
        if supplied_events != retained_events[: len(supplied_events)]:
            raise DurableLearnedLifecycleRefusal(
                "as-of checkpoint is not on the retained event history"
            )
        retained_selection = {
            _exact(dict(row["record_ref"]), "retained selection").key
            for row in _sequence(
                retained_payload.get("selection_receipts", ()),
                "retained selection receipts",
            )
        }
        supplied_selection = {
            _exact(dict(row["record_ref"]), "as-of selection").key
            for row in _sequence(
                supplied_payload.get("selection_receipts", ()),
                "as-of selection receipts",
            )
        }
        if not supplied_selection.issubset(retained_selection):
            raise DurableLearnedLifecycleRefusal(
                "as-of checkpoint selection is not on the retained history"
            )
        retained_no_current = {
            _exact(dict(row["record_ref"]), "retained no-current").key
            for row in _sequence(
                retained_payload.get("no_current_receipts", ()),
                "retained no-current receipts",
            )
        }
        supplied_no_current = {
            _exact(dict(row["record_ref"]), "as-of no-current").key
            for row in _sequence(
                supplied_payload.get("no_current_receipts", ()),
                "as-of no-current receipts",
            )
        }
        if not supplied_no_current.issubset(retained_no_current):
            raise DurableLearnedLifecycleRefusal(
                "as-of checkpoint no-current receipt is not on the retained history"
            )
        return self.b5_executor.resolve_current_as_of(
            self.b5_selection_receipt.selection_key_ref,
            as_of_checkpoint=document,
        )

    def resolve_as_of(
        self,
        as_of_event_ref: ExactRef,
    ) -> SelectionResolution:
        """Historical as-of resolution over the retained B5 event chain."""
        self.require_trusted()
        event_ref = _exact(as_of_event_ref, "as_of_event_ref")
        checkpoint = self.b5_executor.export_checkpoint()
        known = {
            _exact(row["record_ref"], "event ref").key
            for row in checkpoint["checkpoint_payload"]["events"]
        }
        if event_ref.key not in known:
            raise DurableLearnedLifecycleRefusal("as-of event is not in retained history")
        if self.b5_selection_receipt is None:
            # A published-but-never-selected artifact preserves true no-current;
            # there is no exact selection key to resolve as-of against.
            raise DurableLearnedLifecycleRefusal(
                "NO_CURRENT: no selected product history is present"
            )
        return self.b5_executor.resolve_current_as_of(
            self.b5_selection_receipt.selection_key_ref,
            as_of_event_ref=event_ref,
        )


def open_learned_lifecycle(
    artifact_path: str | Path,
    *,
    expected_root: str | None,
    allow_unpinned: bool = False,
) -> DurableLearnedLifecycle:
    path = Path(artifact_path)
    if path.is_file():
        path = path.parent
    manifest = _read_json(path / MANIFEST_NAME)
    if manifest.get("schema") != DURABLE_LEARNED_SCHEMA:
        raise DurableLearnedLifecycleError("learned artifact schema mismatch")
    if manifest.get("contract") != DURABLE_LEARNED_CONTRACT_ID:
        raise DurableLearnedLifecycleError("learned artifact contract mismatch")
    if manifest.get("contract_sha") != DURABLE_LEARNED_CONTRACT_SHA:
        raise DurableLearnedLifecycleError("learned artifact contract SHA mismatch")
    publication = _mapping(manifest.get("publication"), "publication")
    artifact_identity = _text(publication.get("artifact_identity"), "artifact_identity")
    blob_hash = _text(publication.get("blob_hash"), "blob_hash")
    root_identity = _root_identity(artifact_identity, blob_hash)
    if publication.get("root_identity") != root_identity:
        raise DurableLearnedLifecycleError("learned artifact root self-hash mismatch")
    trust_state = "UNPINNED_SELF_HASH"
    if expected_root is not None:
        if expected_root != root_identity:
            raise DurableLearnedLifecycleError("learned artifact external root pin mismatch")
        trust_state = "EXTERNALLY_PINNED"
    elif not allow_unpinned:
        raise DurableLearnedLifecycleUntrusted(
            "learned artifact has no independent external root pin"
        )
    root = path.parent.parent
    blob_path = root / BLOB_DIR / f"{blob_hash}{BLOB_SUFFIX}"
    core = _read_blob(blob_path, blob_hash, publication)
    if semantic_hash(core) != artifact_identity:
        raise DurableLearnedLifecycleError("learned artifact core hash drift")
    if core.get("schema") != DURABLE_LEARNED_SCHEMA:
        raise DurableLearnedLifecycleError("learned artifact core schema mismatch")
    if core.get("contract_sha") != DURABLE_LEARNED_CONTRACT_SHA:
        raise DurableLearnedLifecycleError("learned artifact core contract mismatch")
    m1 = _m1_from_doc(_mapping(core.get("m1"), "m1"))
    m1_evidence = _mapping(core.get("m1_evidence"), "m1_evidence")
    if m1_evidence.get("input_bundle") is None or m1_evidence.get("family_rule_binding") is None:
        raise DurableLearnedLifecycleError("M1 input bundle/family rule preimages are absent")
    if m1_evidence.get("input_bundle") is not None:
        _verify_projection_document(
            _mapping(m1_evidence["input_bundle"], "m1_input_bundle"),
            _exact(
                m1.determinant_explanation_receipt.input_bundle_ref,
                "m1 input bundle ref",
            ),
            "m1_input_bundle",
        )
    if m1_evidence.get("family_rule_binding") is not None:
        _verify_projection_document(
            _mapping(m1_evidence["family_rule_binding"], "m1_family_rule_binding"),
            _exact(m1.family_rule_binding_ref, "m1 family rule ref"),
            "m1_family_rule_binding",
        )
    try:
        m2, repository = _m2_from_docs(_mapping(core.get("m2"), "m2"))
    except DurableLearnedLifecycleError:
        raise
    except Exception as exc:
        raise DurableLearnedLifecycleError(
            f"retained M2 closure reconstruction refused: {exc}"
        ) from exc
    b5 = _mapping(core.get("b5"), "b5")
    checkpoint = _mapping(b5.get("checkpoint"), "b5_checkpoint")
    try:
        executor = LearnedProductLifecycleExecutor.from_checkpoint(checkpoint)
    except Exception as exc:
        raise DurableLearnedLifecycleError(
            f"retained B5 checkpoint reconstruction refused: {exc}"
        ) from exc
    if executor.export_checkpoint()["checkpoint_hash"] != checkpoint.get("checkpoint_hash"):
        raise DurableLearnedLifecycleError("B5 checkpoint replay identity drift")
    subject_doc = _mapping(b5.get("subject"), "b5_subject")
    try:
        subject = LearnedProductLifecycleSubject.from_dict(subject_doc)
    except Exception as exc:
        raise DurableLearnedLifecycleError(
            f"retained B5 subject reconstruction refused: {exc}"
        ) from exc
    protocol = _construct(
        M2B5LifecycleProtocolView, _mapping(b5.get("protocol_view"), "protocol_view")
    )
    selection_doc = b5.get("selection")
    selection = (
        None
        if selection_doc is None
        else CurrentSelectionReceipt.from_dict(_mapping(selection_doc, "b5_selection"))
    )
    if selection is not None:
        try:
            resolution = executor.resolve_selection_exact(
                selection.selection_key_ref, selection.ref
            )
        except Exception as exc:
            raise DurableLearnedLifecycleError(
                f"retained B5 selection reconstruction refused: {exc}"
            ) from exc
        if resolution.state != "CURRENT_SELECTED" or resolution.selected_release_ref != selection.selected_release_ref:
            raise DurableLearnedLifecycleError("B5 selection does not resolve CURRENT_SELECTED")
    replay_doc = b5.get("replay")
    replay = (
        None
        if replay_doc is None
        else _construct(LifecycleReplayReceipt, _mapping(replay_doc, "b5_replay"))
    )
    receipt = _construct(
        LearnedWorldCompositionReceipt,
        _mapping(core.get("learned_receipt"), "learned_receipt"),
    )
    checkpoint_event_keys = tuple(
        _exact(row["record_ref"], "checkpoint event").key
        for row in _sequence(
            checkpoint["checkpoint_payload"].get("events", ()),
            "checkpoint events",
        )
    )
    product_event_keys = {
        _exact(row["record_ref"], "checkpoint event").key
        for row in _sequence(
            checkpoint["checkpoint_payload"].get("events", ()),
            "checkpoint events",
        )
        if _exact(dict(row["release_ref"]), "checkpoint release").key
        == m2.release.ref.key
    }
    receipt_event_keys = tuple(
        _exact(ref, "learned receipt event").key for ref in receipt.b5_event_refs
    )
    if set(receipt_event_keys) != product_event_keys:
        raise DurableLearnedLifecycleError(
            "learned receipt event refs do not match the retained product history"
        )
    if receipt_event_keys and not product_event_keys:
        raise DurableLearnedLifecycleError(
            "learned receipt names events absent from the retained product history"
        )
    if not receipt_event_keys and any(
        receipt.side_effects.get(name)
        for name in (
            "b5_registration_effect",
            "b5_publication_effect",
            "b5_current_selection_effect",
        )
    ):
        raise DurableLearnedLifecycleError(
            "learned receipt claims B5 effects without lifecycle events"
        )
    if checkpoint_event_keys and replay is None:
        raise DurableLearnedLifecycleError(
            "retained B5 history has no lifecycle replay receipt"
        )
    if replay is not None:
        if receipt.b5_replay_receipt_ref is None:
            raise DurableLearnedLifecycleError(
                "retained replay receipt is absent from the learned receipt"
            )
        if _exact(receipt.b5_replay_receipt_ref, "learned replay ref") != replay.ref:
            raise DurableLearnedLifecycleError(
                "retained lifecycle replay ref differs from learned receipt"
            )
        expected_replay = executor.audit_replay()
        if (
            replay.original_checkpoint_hash != checkpoint["checkpoint_hash"]
            or replay.replayed_checkpoint_hash != checkpoint["checkpoint_hash"]
            or {ref.key for ref in replay.event_refs}
            != set(checkpoint_event_keys)
            or {ref.key for ref in replay.selection_receipt_refs}
            != {ref.key for ref in expected_replay.selection_receipt_refs}
            or {ref.key for ref in replay.no_current_receipt_refs}
            != {ref.key for ref in expected_replay.no_current_receipt_refs}
        ):
            raise DurableLearnedLifecycleError(
                "retained lifecycle replay receipt does not reproduce the checkpoint history"
            )
    elif receipt.b5_replay_receipt_ref is not None:
        raise DurableLearnedLifecycleError(
            "learned receipt references an absent lifecycle replay receipt"
        )
    determinants = LearnedConsumerDeterminants.from_document(
        _mapping(core.get("consumer_determinants"), "consumer_determinants")
    )
    if _exact(core.get("purpose_ref"), "purpose_ref") != determinants.purpose_ref:
        raise DurableLearnedLifecycleError("purpose ref mismatch")
    if core.get("s2f_root_identity") != determinants.s2f_root_identity:
        raise DurableLearnedLifecycleError("S2F closure root identity mismatch")
    if receipt.terminal_state != "RULE_SATISFIED":
        raise DurableLearnedLifecycleError("retained learned receipt is not productive")
    if m1.adjudication_outcome != receipt.terminal_state:
        raise DurableLearnedLifecycleError("M1 outcome differs from retained learned receipt")
    if receipt.m1_disposition_ref != m1.ref:
        raise DurableLearnedLifecycleError("M1 disposition ref differs from learned receipt")
    if not isinstance(m1.family_rule_binding_ref, ExactRef):
        raise DurableLearnedLifecycleError("productive M1 disposition lacks exact family rule")
    if not isinstance(m1.validator_authority_ref, AuthorityRef):
        raise DurableLearnedLifecycleError("productive M1 disposition lacks exact validator authority")
    if (
        receipt.m1_family_rule_binding_ref is not None
        and receipt.m1_family_rule_binding_ref != m1.family_rule_binding_ref
    ):
        raise DurableLearnedLifecycleError("M1 family rule ref differs from learned receipt")
    if m2.subject.ref != m1.ref:
        raise DurableLearnedLifecycleError("M2 subject differs from M1 disposition")
    registered_release_keys = {
        _exact(dict(value), "registered release").key
        for value in checkpoint["checkpoint_payload"].get("registered_release_refs", ())
    }
    if m2.release.ref.key not in registered_release_keys:
        raise DurableLearnedLifecycleError("M2 release is absent from B5 registration history")
    if subject.release_ref != m2.release.ref:
        raise DurableLearnedLifecycleError("B5 subject release differs from M2 release")
    if receipt.m2_release_ref != m2.release.ref:
        raise DurableLearnedLifecycleError("M2 release ref differs from learned receipt")
    if protocol.release_ref != m2.release.ref:
        raise DurableLearnedLifecycleError("B5 protocol release differs from M2 release")
    if receipt.b5_lifecycle_subject_ref != subject.release_ref:
        raise DurableLearnedLifecycleError("B5 subject ref differs from learned receipt")
    if selection is not None and receipt.b5_selection_receipt_ref != selection.ref:
        raise DurableLearnedLifecycleError("B5 selection ref differs from learned receipt")
    for name in (
        "release_ref",
        "product_ref",
        "product_family_ref",
        "producer_owner_ref",
        "producer_contract_ref",
        "semantic_projection_hash",
        "authority_snapshot_refs",
        "direct_dependency_refs",
        "determinant_refs",
        "determinant_set_hash",
        "replay_root_ref",
        "selection_scope_ref",
        "build_or_release_receipt_refs",
        "producer_permission_ceiling_ref",
    ):
        if getattr(protocol, name) != getattr(subject, name):
            raise DurableLearnedLifecycleError(
                f"B5 protocol view {name} differs from the retained B5 subject"
            )
    for name in (
        "authority_closure",
        "dependency_closure",
        "determinant_closure",
        "replay_closure",
        "explanation_closure",
    ):
        if getattr(protocol, f"m2_{name}_ref") != getattr(m2, name).ref:
            raise DurableLearnedLifecycleError(
                f"B5 protocol view {name} differs from the retained M2 closure"
            )
    if protocol.producer_typed_state != m1.adjudication_outcome:
        raise DurableLearnedLifecycleError(
            "B5 protocol producer typed state differs from the retained M1 outcome"
        )
    if (
        receipt.m1_input_bundle_ref is not None
        and receipt.m1_input_bundle_ref
        != m1.determinant_explanation_receipt.input_bundle_ref
    ):
        raise DurableLearnedLifecycleError(
            "learned receipt input bundle differs from the retained M1 disposition"
        )
    if receipt.m2_subject_ref != m2.subject.ref:
        raise DurableLearnedLifecycleError(
            "learned receipt M2 subject differs from the retained M2 subject"
        )
    for name in (
        "authority_closure",
        "dependency_closure",
        "determinant_closure",
        "replay_closure",
        "explanation_closure",
    ):
        if getattr(receipt, f"m2_{name}_ref") != getattr(m2, name).ref:
            raise DurableLearnedLifecycleError(
                f"learned receipt {name} differs from the retained M2 closure"
            )
    if receipt.determinant_root_ref != m1.determinant_manifest_ref:
        raise DurableLearnedLifecycleError("learned receipt determinant root drift")
    if receipt.replay_root_ref != m1.replay_ref:
        raise DurableLearnedLifecycleError("learned receipt replay root drift")
    if receipt.explanation_root_ref != m1.explanation_ref:
        raise DurableLearnedLifecycleError("learned receipt explanation root drift")
    if selection is not None and receipt.b5_selection_key_ref != selection.selection_key_ref:
        raise DurableLearnedLifecycleError(
            "learned receipt B5 selection key differs from the retained selection"
        )
    return DurableLearnedLifecycle(
        artifact_path=path,
        artifact_identity=artifact_identity,
        root_identity=root_identity,
        trust_state=trust_state,
        core=core,
        m1_disposition=m1,
        m2_artifacts=m2,
        m2_repository=repository,
        b5_executor=executor,
        b5_subject=subject,
        b5_protocol_view=protocol,
        b5_selection_receipt=selection,
        b5_replay_receipt=replay,
        learned_receipt=receipt,
        determinants=determinants,
    )


__all__ = [
    "DURABLE_LEARNED_CONTRACT_ID",
    "DURABLE_LEARNED_SCHEMA",
    "DURABLE_LEARNED_CONTRACT_SHA",
    "EVIDENCE_GRADE",
    "RIGHTS_STATE",
    "CURRENT_TRUST",
    "DurableLearnedLifecycleError",
    "DurableLearnedLifecycleUntrusted",
    "DurableLearnedLifecycleRefusal",
    "LearnedConsumerDeterminants",
    "LearnedPublishReceipt",
    "ExternalCurrentAttestation",
    "LearnedCurrentView",
    "LearnedConsumerReceipt",
    "publish_learned_lifecycle",
    "open_learned_lifecycle",
    "DurableLearnedLifecycle",
]
