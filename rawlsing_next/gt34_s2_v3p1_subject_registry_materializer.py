"""GT3/GT4 S2 bounded one-object V3-P1 subject registry materializer.

This module is an implementation substrate only. It preserves an already-lawful
semantic owner's exact nonactor object identity and immutable evidence bindings;
it does not create semantic authority, classify entity type, infer fields, or
create actor/encounter/exposure truth.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Final, Iterable

MATERIALIZER_ID: Final[str] = (
    "GT34_V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_REGISTRY_MATERIALIZER"
)
MATERIALIZER_VERSION: Final[str] = "1.0.0"
SUBJECT_REF_SCHEME: Final[str] = "RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1"
RECEIPT_SCHEMA: Final[str] = (
    "V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_MATERIALIZATION_RECEIPT@1.0.0"
)
OWNER_BINDING_SCHEMA: Final[str] = (
    "V3P1_OWNER_BOUND_SUBJECT_INGRESS_BINDING@1.0.0"
)
SUBJECT_REF_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
)
RECEIPT_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-S2\0V3P1-SUBJECT-MATERIALIZATION-RECEIPT-V1\0"
)
OWNER_BINDING_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class SubjectMaterializationError(ValueError):
    """Owner-bound subject materialization failed closed."""


class OneObjectRegistryOccupiedError(SubjectMaterializationError):
    """A one-object registry was asked to materialize a second distinct object."""


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _hash_domain(domain: bytes, material: object) -> str:
    return _sha256_bytes(domain + _canonical_json(material).encode("utf-8"))


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise SubjectMaterializationError(f"{field} must be a nonempty string")
    return value


def _sha256(value: object, field: str) -> str:
    value = _nonempty(value, field)
    if not _SHA256_RE.fullmatch(value):
        raise SubjectMaterializationError(f"{field} must be lowercase sha256 hex")
    return value


@dataclass(frozen=True, order=True)
class ExactImmutableRef:
    kind: str
    ref_id: str
    sha256: str

    def validated(self) -> "ExactImmutableRef":
        _nonempty(self.kind, "ref.kind")
        _nonempty(self.ref_id, "ref.ref_id")
        _sha256(self.sha256, "ref.sha256")
        return self

    def as_dict(self) -> dict[str, str]:
        self.validated()
        return {"kind": self.kind, "ref_id": self.ref_id, "sha256": self.sha256}


def _canonical_refs(
    refs: Iterable[ExactImmutableRef],
    *,
    field: str,
    require_nonempty: bool = True,
) -> tuple[ExactImmutableRef, ...]:
    material = tuple(refs)
    if require_nonempty and not material:
        raise SubjectMaterializationError(f"{field} must contain at least one exact ref")
    validated = tuple(ref.validated() for ref in material)
    if len(set(validated)) != len(validated):
        raise SubjectMaterializationError(f"{field} contains duplicate exact refs")
    return tuple(sorted(validated))


@dataclass(frozen=True)
class OwnerBoundSubjectInput:
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_hash: str
    semantic_object_ref: ExactImmutableRef
    semantic_object_bytes: bytes
    evidence_refs: tuple[ExactImmutableRef, ...]
    provenance_refs: tuple[ExactImmutableRef, ...]
    owner_binding_content_hash: str

    def owner_binding_material(self) -> dict[str, object]:
        owner_id = _nonempty(
            self.semantic_owner_authority_id, "semantic_owner_authority_id"
        )
        owner_version = _nonempty(
            self.semantic_owner_authority_version, "semantic_owner_authority_version"
        )
        owner_hash = _sha256(
            self.semantic_owner_authority_hash, "semantic_owner_authority_hash"
        )
        object_ref = self.semantic_object_ref.validated()
        if not isinstance(self.semantic_object_bytes, bytes) or not self.semantic_object_bytes:
            raise SubjectMaterializationError(
                "semantic_object_bytes must be nonempty immutable bytes"
            )
        object_hash = _sha256_bytes(self.semantic_object_bytes)
        if object_hash != object_ref.sha256:
            raise SubjectMaterializationError("semantic object bytes/hash mismatch")

        evidence = _canonical_refs(self.evidence_refs, field="evidence_refs")
        provenance = _canonical_refs(self.provenance_refs, field="provenance_refs")
        return {
            "schema_id": OWNER_BINDING_SCHEMA,
            "semantic_owner_authority": {
                "id": owner_id,
                "version": owner_version,
                "content_hash": owner_hash,
            },
            "semantic_object_ref": object_ref.as_dict(),
            "evidence_refs": [ref.as_dict() for ref in evidence],
            "provenance_refs": [ref.as_dict() for ref in provenance],
        }

    def validated_owner_binding_hash(self) -> str:
        presented = _sha256(
            self.owner_binding_content_hash, "owner_binding_content_hash"
        )
        expected = _hash_domain(OWNER_BINDING_DOMAIN, self.owner_binding_material())
        if presented != expected:
            raise SubjectMaterializationError("owner binding content hash mismatch")
        return expected


def compute_owner_binding_content_hash(
    *,
    semantic_owner_authority_id: str,
    semantic_owner_authority_version: str,
    semantic_owner_authority_hash: str,
    semantic_object_ref: ExactImmutableRef,
    semantic_object_bytes: bytes,
    evidence_refs: tuple[ExactImmutableRef, ...],
    provenance_refs: tuple[ExactImmutableRef, ...],
) -> str:
    """Compute only the mechanical owner-binding hash; creates no semantic truth."""
    probe = OwnerBoundSubjectInput(
        semantic_owner_authority_id=semantic_owner_authority_id,
        semantic_owner_authority_version=semantic_owner_authority_version,
        semantic_owner_authority_hash=semantic_owner_authority_hash,
        semantic_object_ref=semantic_object_ref,
        semantic_object_bytes=semantic_object_bytes,
        evidence_refs=evidence_refs,
        provenance_refs=provenance_refs,
        owner_binding_content_hash="0" * 64,
    )
    return _hash_domain(OWNER_BINDING_DOMAIN, probe.owner_binding_material())


@dataclass(frozen=True)
class SubjectMaterializationReceipt:
    receipt_id: str
    receipt_hash: str
    subject_ref: str
    subject_ref_hash: str
    materializer_id: str
    materializer_version: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_hash: str
    semantic_object_ref: ExactImmutableRef
    owner_binding_content_hash: str
    evidence_refs: tuple[ExactImmutableRef, ...]
    provenance_refs: tuple[ExactImmutableRef, ...]
    replay_input_hash: str
    integrity_state: str
    semantic_owner_transfer: bool
    semantic_fields_interpreted: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "receipt_hash": self.receipt_hash,
            "schema_id": RECEIPT_SCHEMA,
            "subject_ref": self.subject_ref,
            "subject_ref_hash": self.subject_ref_hash,
            "materializer_id": self.materializer_id,
            "materializer_version": self.materializer_version,
            "semantic_owner_authority": {
                "id": self.semantic_owner_authority_id,
                "version": self.semantic_owner_authority_version,
                "content_hash": self.semantic_owner_authority_hash,
            },
            "semantic_object_ref": self.semantic_object_ref.as_dict(),
            "owner_binding_content_hash": self.owner_binding_content_hash,
            "evidence_refs": [ref.as_dict() for ref in self.evidence_refs],
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
            "replay_input_hash": self.replay_input_hash,
            "integrity_state": self.integrity_state,
            "semantic_owner_transfer": self.semantic_owner_transfer,
            "semantic_fields_interpreted": self.semantic_fields_interpreted,
        }


def materialize_owner_bound_subject(
    material: OwnerBoundSubjectInput,
) -> SubjectMaterializationReceipt:
    """Materialize one exact ref from already-owner-bound opaque subject bytes.

    The semantic object is never parsed. Its fields are not normalized, inferred,
    reinterpreted, or copied into the receipt. This function verifies only exact
    transport/integrity bindings supplied by the semantic owner boundary.
    """
    if not isinstance(material, OwnerBoundSubjectInput):
        raise SubjectMaterializationError(
            "material must be OwnerBoundSubjectInput"
        )

    owner_binding_hash = material.validated_owner_binding_hash()
    owner_material = material.owner_binding_material()
    object_ref = material.semantic_object_ref.validated()
    evidence = _canonical_refs(material.evidence_refs, field="evidence_refs")
    provenance = _canonical_refs(material.provenance_refs, field="provenance_refs")

    subject_identity_material = {
        "scheme": SUBJECT_REF_SCHEME,
        "semantic_owner_authority": owner_material["semantic_owner_authority"],
        "semantic_object_ref": object_ref.as_dict(),
        "owner_binding_content_hash": owner_binding_hash,
        "evidence_refs": [ref.as_dict() for ref in evidence],
        "provenance_refs": [ref.as_dict() for ref in provenance],
    }
    subject_hash = _hash_domain(SUBJECT_REF_DOMAIN, subject_identity_material)
    subject_ref = f"urn:rawlsing:v3:subject:sha256:{subject_hash}"

    replay_input_hash = _sha256_bytes(
        _canonical_json(subject_identity_material).encode("utf-8")
    )
    receipt_body = {
        "schema_id": RECEIPT_SCHEMA,
        "subject_ref": subject_ref,
        "subject_ref_hash": subject_hash,
        "materializer_id": MATERIALIZER_ID,
        "materializer_version": MATERIALIZER_VERSION,
        "semantic_owner_authority": owner_material["semantic_owner_authority"],
        "semantic_object_ref": object_ref.as_dict(),
        "owner_binding_content_hash": owner_binding_hash,
        "evidence_refs": [ref.as_dict() for ref in evidence],
        "provenance_refs": [ref.as_dict() for ref in provenance],
        "replay_input_hash": replay_input_hash,
        "integrity_state": "VERIFIED_OWNER_BOUND_INPUT",
        "semantic_owner_transfer": False,
        "semantic_fields_interpreted": False,
    }
    receipt_hash = _hash_domain(RECEIPT_DOMAIN, receipt_body)
    receipt_id = (
        "urn:rawlsing:v3:subject-materialization-receipt:sha256:"
        f"{receipt_hash}"
    )
    return SubjectMaterializationReceipt(
        receipt_id=receipt_id,
        receipt_hash=receipt_hash,
        subject_ref=subject_ref,
        subject_ref_hash=subject_hash,
        materializer_id=MATERIALIZER_ID,
        materializer_version=MATERIALIZER_VERSION,
        semantic_owner_authority_id=material.semantic_owner_authority_id,
        semantic_owner_authority_version=material.semantic_owner_authority_version,
        semantic_owner_authority_hash=material.semantic_owner_authority_hash,
        semantic_object_ref=object_ref,
        owner_binding_content_hash=owner_binding_hash,
        evidence_refs=evidence,
        provenance_refs=provenance,
        replay_input_hash=replay_input_hash,
        integrity_state="VERIFIED_OWNER_BOUND_INPUT",
        semantic_owner_transfer=False,
        semantic_fields_interpreted=False,
    )


class OneObjectSubjectRegistry:
    """Single-slot immutable registry; a second distinct object fails closed."""

    def __init__(self) -> None:
        self._receipt: SubjectMaterializationReceipt | None = None

    @property
    def receipt(self) -> SubjectMaterializationReceipt | None:
        return self._receipt

    def materialize(
        self, material: OwnerBoundSubjectInput
    ) -> SubjectMaterializationReceipt:
        candidate = materialize_owner_bound_subject(material)
        if self._receipt is None:
            self._receipt = candidate
            return candidate
        if self._receipt.receipt_id == candidate.receipt_id:
            return self._receipt
        raise OneObjectRegistryOccupiedError(
            "one-object registry already contains a distinct subject"
        )


__all__ = [
    "MATERIALIZER_ID",
    "MATERIALIZER_VERSION",
    "OWNER_BINDING_SCHEMA",
    "RECEIPT_SCHEMA",
    "SUBJECT_REF_SCHEME",
    "ExactImmutableRef",
    "OneObjectRegistryOccupiedError",
    "OneObjectSubjectRegistry",
    "OwnerBoundSubjectInput",
    "SubjectMaterializationError",
    "SubjectMaterializationReceipt",
    "compute_owner_binding_content_hash",
    "materialize_owner_bound_subject",
]
