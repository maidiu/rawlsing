"""GT3/GT4 U2 corrected OBL054 owner-authenticated one-object materializer.

This is a bounded successor to historical S2.  Historical S2 remains in-tree as
failed candidate evidence; this module is a distinct successor surface.

The successor authenticates exactly one adopted OBL053 semantic object against
the fresh corrected HQ adoption root before any production subject-ref receipt
can be emitted.  It preserves semantic opacity: semantic object bytes are never
parsed, normalized, classified, or copied into materializer truth.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Final, Iterable


MATERIALIZER_ID: Final[str] = (
    "GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER"
)
MATERIALIZER_VERSION: Final[str] = "2.0.0"

SUBJECT_REF_SCHEME: Final[str] = "RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1"
OWNER_BINDING_SCHEMA: Final[str] = (
    "V3P1_OWNER_BOUND_SUBJECT_INGRESS_BINDING@1.0.0"
)
RECEIPT_SCHEMA: Final[str] = (
    "V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_RECEIPT@2.0.0"
)
PERMIT_SCHEMA: Final[str] = (
    "GT34_OBL054_ONE_OBJECT_MATERIALIZATION_PERMIT@1.0.0"
)
ACCEPTED_ROOT_SCHEMA: Final[str] = (
    "GT34_OBL054_ACCEPTED_OBL053_OWNER_ROOT@1.0.0"
)

SUBJECT_REF_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
)
OWNER_BINDING_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
)
ACCEPTED_ROOT_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-U2\0OBL054-ACCEPTED-OBL053-ROOT-V1\0"
)
PERMIT_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-U2\0OBL054-ONE-OBJECT-MATERIALIZATION-PERMIT-V1\0"
)
RECEIPT_DOMAIN: Final[bytes] = (
    b"RAWLSING\0GT34-U2\0V3P1-AUTHENTICATED-SUBJECT-RECEIPT-V2\0"
)

FRESH_OBL053_ADOPTION_ARTIFACT_BLOB: Final[str] = (
    "f561765bad4fdad2bbf4591f35fe7f81f8486428"
)
HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB: Final[str] = (
    "286ff7b851e920ff2760082d8b2fb194560ab127"
)

OBL053_AUTHORITY_ID: Final[str] = (
    "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY"
)
OBL053_AUTHORITY_VERSION: Final[str] = "1.0.0"
OBL053_AUTHORITY_HASH: Final[str] = (
    "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
)
OBL053_GENERATION_SEED_HASH: Final[str] = (
    "b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53"
)
OBL053_SEMANTIC_OBJECT_ID: Final[str] = (
    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
    "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
)
OBL053_SEMANTIC_OBJECT_HASH: Final[str] = (
    "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
)
OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH: Final[str] = (
    "153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"
)

HISTORICAL_INVALID_AUTHORITY_HASH: Final[str] = (
    "e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed"
)
HISTORICAL_INVALID_OBJECT_HASH: Final[str] = (
    "d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53"
)
HISTORICAL_INVALID_RECEIPT_HASH: Final[str] = (
    "1561942f1fe4fc43b248c61be866c0bc459773b7c6dbb8e393e13b064cdacce0"
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class SubjectMaterializationError(ValueError):
    """Authenticated subject materialization failed closed."""


class AcceptedOwnerAuthenticationError(SubjectMaterializationError):
    """Presented owner/object lineage does not match the current accepted root."""


class MaterializationPermitError(SubjectMaterializationError):
    """Presented one-object materialization permit is invalid or noncurrent."""


class OneObjectRegistryOccupiedError(SubjectMaterializationError):
    """A one-object registry was asked to retain a distinct receipt."""


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


def _git_sha1(value: object, field: str) -> str:
    value = _nonempty(value, field)
    if not _GIT_SHA1_RE.fullmatch(value):
        raise SubjectMaterializationError(f"{field} must be lowercase git sha1 hex")
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
) -> tuple[ExactImmutableRef, ...]:
    material = tuple(refs)
    if not material:
        raise SubjectMaterializationError(
            f"{field} must contain at least one exact immutable ref"
        )
    validated = tuple(ref.validated() for ref in material)
    if len(set(validated)) != len(validated):
        raise SubjectMaterializationError(f"{field} contains duplicate exact refs")
    return tuple(sorted(validated))


CURRENT_SEMANTIC_OBJECT_REF: Final[ExactImmutableRef] = ExactImmutableRef(
    kind="GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_SEMANTIC_OBJECT",
    ref_id=OBL053_SEMANTIC_OBJECT_ID,
    sha256=OBL053_SEMANTIC_OBJECT_HASH,
)

CURRENT_EVIDENCE_REFS: Final[tuple[ExactImmutableRef, ...]] = (
    ExactImmutableRef(
        kind="GT34_OBL053_OBJECTIVE_EVIDENCE_RECEIPT",
        ref_id=(
            "urn:rawlsing:gt34:obl053:objective-evidence-receipt:sha256:"
            + OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH
        ),
        sha256=OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH,
    ),
)

CURRENT_PROVENANCE_REFS: Final[tuple[ExactImmutableRef, ...]] = (
    ExactImmutableRef(
        kind="GOVERNED_GENERATION_SEED",
        ref_id=(
            "urn:rawlsing:gt34:obl053:generation-seed:sha256:"
            + OBL053_GENERATION_SEED_HASH
        ),
        sha256=OBL053_GENERATION_SEED_HASH,
    ),
    ExactImmutableRef(
        kind="SEMANTIC_OWNER_AUTHORITY",
        ref_id=(
            "urn:rawlsing:gt34:obl053:semantic-owner-authority:sha256:"
            + OBL053_AUTHORITY_HASH
        ),
        sha256=OBL053_AUTHORITY_HASH,
    ),
)


@dataclass(frozen=True)
class AcceptedOwnerRoot:
    adoption_artifact_blob: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_hash: str
    generation_seed_hash: str
    semantic_object_ref: ExactImmutableRef
    objective_evidence_receipt_hash: str
    evidence_refs: tuple[ExactImmutableRef, ...]
    provenance_refs: tuple[ExactImmutableRef, ...]
    currentness_state: str
    object_cardinality: int

    def validated_structurally(self) -> "AcceptedOwnerRoot":
        _git_sha1(self.adoption_artifact_blob, "adoption_artifact_blob")
        _nonempty(self.semantic_owner_authority_id, "semantic_owner_authority_id")
        _nonempty(
            self.semantic_owner_authority_version,
            "semantic_owner_authority_version",
        )
        _sha256(
            self.semantic_owner_authority_hash,
            "semantic_owner_authority_hash",
        )
        _sha256(self.generation_seed_hash, "generation_seed_hash")
        self.semantic_object_ref.validated()
        _sha256(
            self.objective_evidence_receipt_hash,
            "objective_evidence_receipt_hash",
        )
        _canonical_refs(self.evidence_refs, field="evidence_refs")
        _canonical_refs(self.provenance_refs, field="provenance_refs")
        _nonempty(self.currentness_state, "currentness_state")
        if self.object_cardinality != 1:
            raise AcceptedOwnerAuthenticationError(
                "accepted owner root must authorize exactly one object"
            )
        return self

    def as_dict(self) -> dict[str, object]:
        self.validated_structurally()
        return {
            "schema_id": ACCEPTED_ROOT_SCHEMA,
            "adoption_artifact_blob": self.adoption_artifact_blob,
            "semantic_owner_authority": {
                "id": self.semantic_owner_authority_id,
                "version": self.semantic_owner_authority_version,
                "content_hash": self.semantic_owner_authority_hash,
            },
            "generation_seed_hash": self.generation_seed_hash,
            "semantic_object_ref": self.semantic_object_ref.as_dict(),
            "objective_evidence_receipt_hash": (
                self.objective_evidence_receipt_hash
            ),
            "evidence_refs": [
                ref.as_dict()
                for ref in _canonical_refs(self.evidence_refs, field="evidence_refs")
            ],
            "provenance_refs": [
                ref.as_dict()
                for ref in _canonical_refs(
                    self.provenance_refs,
                    field="provenance_refs",
                )
            ],
            "currentness_state": self.currentness_state,
            "object_cardinality": self.object_cardinality,
        }


CURRENT_ACCEPTED_OWNER_ROOT: Final[AcceptedOwnerRoot] = AcceptedOwnerRoot(
    adoption_artifact_blob=FRESH_OBL053_ADOPTION_ARTIFACT_BLOB,
    semantic_owner_authority_id=OBL053_AUTHORITY_ID,
    semantic_owner_authority_version=OBL053_AUTHORITY_VERSION,
    semantic_owner_authority_hash=OBL053_AUTHORITY_HASH,
    generation_seed_hash=OBL053_GENERATION_SEED_HASH,
    semantic_object_ref=CURRENT_SEMANTIC_OBJECT_REF,
    objective_evidence_receipt_hash=OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH,
    evidence_refs=CURRENT_EVIDENCE_REFS,
    provenance_refs=CURRENT_PROVENANCE_REFS,
    currentness_state="FRESHLY_HQ_ADOPTED__OBL053_CLOSED",
    object_cardinality=1,
)

CURRENT_ACCEPTED_OWNER_ROOT_HASH: Final[str] = _hash_domain(
    ACCEPTED_ROOT_DOMAIN,
    CURRENT_ACCEPTED_OWNER_ROOT.as_dict(),
)


@dataclass(frozen=True)
class OneObjectMaterializationPermit:
    permit_id: str
    permit_hash: str
    accepted_owner_root: AcceptedOwnerRoot
    accepted_owner_root_hash: str
    scope: str
    object_cardinality: int

    def permit_material(self) -> dict[str, object]:
        root = self.accepted_owner_root.validated_structurally()
        root_hash = _sha256(
            self.accepted_owner_root_hash,
            "accepted_owner_root_hash",
        )
        if self.object_cardinality != 1:
            raise MaterializationPermitError(
                "materialization permit must authorize exactly one object"
            )
        if self.scope != "EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY":
            raise MaterializationPermitError("materialization permit scope mismatch")
        return {
            "schema_id": PERMIT_SCHEMA,
            "accepted_owner_root": root.as_dict(),
            "accepted_owner_root_hash": root_hash,
            "scope": self.scope,
            "object_cardinality": self.object_cardinality,
        }

    def validated_structurally(self) -> "OneObjectMaterializationPermit":
        material = self.permit_material()
        expected_hash = _hash_domain(PERMIT_DOMAIN, material)
        if _sha256(self.permit_hash, "permit_hash") != expected_hash:
            raise MaterializationPermitError("permit content hash mismatch")
        expected_id = (
            "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:"
            + expected_hash
        )
        if self.permit_id != expected_id:
            raise MaterializationPermitError("permit id/hash mismatch")
        root_hash = _hash_domain(
            ACCEPTED_ROOT_DOMAIN,
            self.accepted_owner_root.as_dict(),
        )
        if root_hash != self.accepted_owner_root_hash:
            raise MaterializationPermitError(
                "accepted owner root hash does not authenticate root material"
            )
        return self

    def validated_for_current_root(self) -> "OneObjectMaterializationPermit":
        self.validated_structurally()
        if self.accepted_owner_root != CURRENT_ACCEPTED_OWNER_ROOT:
            raise MaterializationPermitError(
                "permit does not terminate in the current accepted OBL053 root"
            )
        if self.accepted_owner_root_hash != CURRENT_ACCEPTED_OWNER_ROOT_HASH:
            raise MaterializationPermitError(
                "permit accepted-root hash is not current"
            )
        return self


def _build_permit(root: AcceptedOwnerRoot) -> OneObjectMaterializationPermit:
    root = root.validated_structurally()
    root_hash = _hash_domain(ACCEPTED_ROOT_DOMAIN, root.as_dict())
    material = {
        "schema_id": PERMIT_SCHEMA,
        "accepted_owner_root": root.as_dict(),
        "accepted_owner_root_hash": root_hash,
        "scope": "EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY",
        "object_cardinality": 1,
    }
    permit_hash = _hash_domain(PERMIT_DOMAIN, material)
    permit_id = (
        "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:"
        + permit_hash
    )
    return OneObjectMaterializationPermit(
        permit_id=permit_id,
        permit_hash=permit_hash,
        accepted_owner_root=root,
        accepted_owner_root_hash=root_hash,
        scope="EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY",
        object_cardinality=1,
    )


CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT: Final[OneObjectMaterializationPermit] = (
    _build_permit(CURRENT_ACCEPTED_OWNER_ROOT)
)


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
            self.semantic_owner_authority_id,
            "semantic_owner_authority_id",
        )
        owner_version = _nonempty(
            self.semantic_owner_authority_version,
            "semantic_owner_authority_version",
        )
        owner_hash = _sha256(
            self.semantic_owner_authority_hash,
            "semantic_owner_authority_hash",
        )
        object_ref = self.semantic_object_ref.validated()
        if not isinstance(self.semantic_object_bytes, bytes) or not self.semantic_object_bytes:
            raise SubjectMaterializationError(
                "semantic_object_bytes must be nonempty immutable bytes"
            )
        if _sha256_bytes(self.semantic_object_bytes) != object_ref.sha256:
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
            self.owner_binding_content_hash,
            "owner_binding_content_hash",
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
    """Compute transport integrity only; this never authenticates semantic ownership."""
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


def _validate_material_against_root(
    material: OwnerBoundSubjectInput,
    root: AcceptedOwnerRoot,
) -> tuple[str, dict[str, object], tuple[ExactImmutableRef, ...], tuple[ExactImmutableRef, ...]]:
    if not isinstance(material, OwnerBoundSubjectInput):
        raise SubjectMaterializationError(
            "material must be OwnerBoundSubjectInput"
        )
    root.validated_structurally()

    if material.semantic_owner_authority_id != root.semantic_owner_authority_id:
        raise AcceptedOwnerAuthenticationError("semantic owner id mismatch")
    if material.semantic_owner_authority_version != root.semantic_owner_authority_version:
        raise AcceptedOwnerAuthenticationError("semantic owner version mismatch")
    if material.semantic_owner_authority_hash != root.semantic_owner_authority_hash:
        raise AcceptedOwnerAuthenticationError("semantic owner hash mismatch")
    if material.semantic_object_ref != root.semantic_object_ref:
        raise AcceptedOwnerAuthenticationError("semantic object ref mismatch")

    evidence = _canonical_refs(material.evidence_refs, field="evidence_refs")
    provenance = _canonical_refs(material.provenance_refs, field="provenance_refs")
    if evidence != _canonical_refs(root.evidence_refs, field="root.evidence_refs"):
        raise AcceptedOwnerAuthenticationError("evidence lineage mismatch")
    if provenance != _canonical_refs(
        root.provenance_refs,
        field="root.provenance_refs",
    ):
        raise AcceptedOwnerAuthenticationError("provenance lineage mismatch")

    owner_binding_hash = material.validated_owner_binding_hash()
    owner_material = material.owner_binding_material()
    return owner_binding_hash, owner_material, evidence, provenance


@dataclass(frozen=True)
class _MaterializationCore:
    subject_ref: str
    subject_ref_hash: str
    replay_input_hash: str
    owner_binding_content_hash: str
    owner_material: dict[str, object]
    semantic_object_ref: ExactImmutableRef
    evidence_refs: tuple[ExactImmutableRef, ...]
    provenance_refs: tuple[ExactImmutableRef, ...]


def _materialization_core(
    material: OwnerBoundSubjectInput,
    root: AcceptedOwnerRoot,
) -> _MaterializationCore:
    owner_binding_hash, owner_material, evidence, provenance = (
        _validate_material_against_root(material, root)
    )
    object_ref = material.semantic_object_ref.validated()
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
    return _MaterializationCore(
        subject_ref=subject_ref,
        subject_ref_hash=subject_hash,
        replay_input_hash=replay_input_hash,
        owner_binding_content_hash=owner_binding_hash,
        owner_material=owner_material,
        semantic_object_ref=object_ref,
        evidence_refs=evidence,
        provenance_refs=provenance,
    )


@dataclass(frozen=True)
class SubjectMaterializationReceipt:
    receipt_id: str
    receipt_hash: str
    subject_ref: str
    subject_ref_hash: str
    materializer_id: str
    materializer_version: str
    adoption_artifact_blob: str
    accepted_owner_root_hash: str
    materialization_permit_id: str
    materialization_permit_hash: str
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
            "adoption_artifact_blob": self.adoption_artifact_blob,
            "accepted_owner_root_hash": self.accepted_owner_root_hash,
            "materialization_permit_id": self.materialization_permit_id,
            "materialization_permit_hash": self.materialization_permit_hash,
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


def _build_production_receipt(
    core: _MaterializationCore,
    permit: OneObjectMaterializationPermit,
) -> SubjectMaterializationReceipt:
    root = permit.accepted_owner_root
    receipt_body = {
        "schema_id": RECEIPT_SCHEMA,
        "subject_ref": core.subject_ref,
        "subject_ref_hash": core.subject_ref_hash,
        "materializer_id": MATERIALIZER_ID,
        "materializer_version": MATERIALIZER_VERSION,
        "adoption_artifact_blob": root.adoption_artifact_blob,
        "accepted_owner_root_hash": permit.accepted_owner_root_hash,
        "materialization_permit_id": permit.permit_id,
        "materialization_permit_hash": permit.permit_hash,
        "semantic_owner_authority": core.owner_material["semantic_owner_authority"],
        "semantic_object_ref": core.semantic_object_ref.as_dict(),
        "owner_binding_content_hash": core.owner_binding_content_hash,
        "evidence_refs": [ref.as_dict() for ref in core.evidence_refs],
        "provenance_refs": [ref.as_dict() for ref in core.provenance_refs],
        "replay_input_hash": core.replay_input_hash,
        "integrity_state": "AUTHENTICATED_FRESH_OBL053_ROOT__OWNER_BOUND_INPUT_VERIFIED",
        "semantic_owner_transfer": False,
        "semantic_fields_interpreted": False,
    }
    receipt_hash = _hash_domain(RECEIPT_DOMAIN, receipt_body)
    receipt_id = (
        "urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:"
        + receipt_hash
    )
    return SubjectMaterializationReceipt(
        receipt_id=receipt_id,
        receipt_hash=receipt_hash,
        subject_ref=core.subject_ref,
        subject_ref_hash=core.subject_ref_hash,
        materializer_id=MATERIALIZER_ID,
        materializer_version=MATERIALIZER_VERSION,
        adoption_artifact_blob=root.adoption_artifact_blob,
        accepted_owner_root_hash=permit.accepted_owner_root_hash,
        materialization_permit_id=permit.permit_id,
        materialization_permit_hash=permit.permit_hash,
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=core.semantic_object_ref,
        owner_binding_content_hash=core.owner_binding_content_hash,
        evidence_refs=core.evidence_refs,
        provenance_refs=core.provenance_refs,
        replay_input_hash=core.replay_input_hash,
        integrity_state="AUTHENTICATED_FRESH_OBL053_ROOT__OWNER_BOUND_INPUT_VERIFIED",
        semantic_owner_transfer=False,
        semantic_fields_interpreted=False,
    )


def materialize_owner_bound_subject(
    material: OwnerBoundSubjectInput,
    permit: OneObjectMaterializationPermit,
) -> SubjectMaterializationReceipt:
    """Materialize only the exact object authorized by the fresh OBL053 root."""
    if not isinstance(permit, OneObjectMaterializationPermit):
        raise MaterializationPermitError(
            "a valid OneObjectMaterializationPermit is required"
        )
    permit.validated_for_current_root()
    core = _materialization_core(material, permit.accepted_owner_root)
    return _build_production_receipt(core, permit)


class OneObjectSubjectRegistry:
    """Idempotent single-slot registry whose cardinality authority lives in permit."""

    def __init__(self, permit: OneObjectMaterializationPermit) -> None:
        if not isinstance(permit, OneObjectMaterializationPermit):
            raise MaterializationPermitError(
                "registry requires OneObjectMaterializationPermit"
            )
        self._permit = permit.validated_for_current_root()
        self._receipt: SubjectMaterializationReceipt | None = None

    @property
    def receipt(self) -> SubjectMaterializationReceipt | None:
        return self._receipt

    @property
    def permit(self) -> OneObjectMaterializationPermit:
        return self._permit

    def materialize(
        self,
        material: OwnerBoundSubjectInput,
    ) -> SubjectMaterializationReceipt:
        candidate = materialize_owner_bound_subject(material, self._permit)
        if self._receipt is None:
            self._receipt = candidate
            return candidate
        if self._receipt.receipt_id == candidate.receipt_id:
            return self._receipt
        raise OneObjectRegistryOccupiedError(
            "one-object registry already contains a distinct receipt"
        )


# ---------------------------------------------------------------------------
# Noncurrent shadow fixture support
# ---------------------------------------------------------------------------
#
# Governed repair tests must exercise successful/idempotent mechanics without
# prematurely materializing the real first-canary subject.  These private helpers
# reuse the exact validation/core path with a synthetic AcceptedOwnerRoot, but
# they never produce the production receipt schema/materializer identity and are
# deliberately excluded from __all__.


@dataclass(frozen=True)
class _ShadowReceipt:
    subject_ref: str
    subject_ref_hash: str
    replay_input_hash: str
    owner_binding_content_hash: str
    permit_id: str
    permit_hash: str
    integrity_state: str
    semantic_owner_transfer: bool
    semantic_fields_interpreted: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": "NONCURRENT_SYNTHETIC_SHADOW_RECEIPT@1.0.0",
            "subject_ref": self.subject_ref,
            "subject_ref_hash": self.subject_ref_hash,
            "replay_input_hash": self.replay_input_hash,
            "owner_binding_content_hash": self.owner_binding_content_hash,
            "permit_id": self.permit_id,
            "permit_hash": self.permit_hash,
            "integrity_state": self.integrity_state,
            "semantic_owner_transfer": self.semantic_owner_transfer,
            "semantic_fields_interpreted": self.semantic_fields_interpreted,
        }


def _materialize_noncurrent_shadow_fixture(
    material: OwnerBoundSubjectInput,
    permit: OneObjectMaterializationPermit,
) -> _ShadowReceipt:
    permit.validated_structurally()
    if permit.accepted_owner_root.currentness_state != "NONCURRENT_SYNTHETIC_TEST_ONLY":
        raise MaterializationPermitError(
            "shadow fixture requires NONCURRENT_SYNTHETIC_TEST_ONLY root"
        )
    core = _materialization_core(material, permit.accepted_owner_root)
    return _ShadowReceipt(
        subject_ref=core.subject_ref,
        subject_ref_hash=core.subject_ref_hash,
        replay_input_hash=core.replay_input_hash,
        owner_binding_content_hash=core.owner_binding_content_hash,
        permit_id=permit.permit_id,
        permit_hash=permit.permit_hash,
        integrity_state="NONCURRENT_SYNTHETIC_TEST_ONLY",
        semantic_owner_transfer=False,
        semantic_fields_interpreted=False,
    )


__all__ = [
    "MATERIALIZER_ID",
    "MATERIALIZER_VERSION",
    "SUBJECT_REF_SCHEME",
    "OWNER_BINDING_SCHEMA",
    "RECEIPT_SCHEMA",
    "PERMIT_SCHEMA",
    "ACCEPTED_ROOT_SCHEMA",
    "FRESH_OBL053_ADOPTION_ARTIFACT_BLOB",
    "HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB",
    "OBL053_AUTHORITY_ID",
    "OBL053_AUTHORITY_VERSION",
    "OBL053_AUTHORITY_HASH",
    "OBL053_GENERATION_SEED_HASH",
    "OBL053_SEMANTIC_OBJECT_ID",
    "OBL053_SEMANTIC_OBJECT_HASH",
    "OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH",
    "CURRENT_SEMANTIC_OBJECT_REF",
    "CURRENT_EVIDENCE_REFS",
    "CURRENT_PROVENANCE_REFS",
    "CURRENT_ACCEPTED_OWNER_ROOT",
    "CURRENT_ACCEPTED_OWNER_ROOT_HASH",
    "CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT",
    "ExactImmutableRef",
    "AcceptedOwnerRoot",
    "OneObjectMaterializationPermit",
    "OwnerBoundSubjectInput",
    "SubjectMaterializationReceipt",
    "SubjectMaterializationError",
    "AcceptedOwnerAuthenticationError",
    "MaterializationPermitError",
    "OneObjectRegistryOccupiedError",
    "OneObjectSubjectRegistry",
    "compute_owner_binding_content_hash",
    "materialize_owner_bound_subject",
]
