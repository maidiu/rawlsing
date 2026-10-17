from __future__ import annotations

from dataclasses import fields, replace
import hashlib

import pytest

from rawlsing_next.gt34_s2_v3p1_subject_registry_materializer import (
    MATERIALIZER_ID,
    MATERIALIZER_VERSION,
    RECEIPT_SCHEMA,
    SUBJECT_REF_SCHEME,
    ExactImmutableRef,
    OneObjectRegistryOccupiedError,
    OneObjectSubjectRegistry,
    OwnerBoundSubjectInput,
    SubjectMaterializationError,
    compute_owner_binding_content_hash,
    materialize_owner_bound_subject,
)


def _ref(kind: str, ref_id: str, payload: bytes) -> ExactImmutableRef:
    return ExactImmutableRef(kind, ref_id, hashlib.sha256(payload).hexdigest())


def _fixture(
    *,
    semantic_object_bytes: bytes = b'{"fixture":"SYNTHETIC_NONACTOR_OBJECT_A","opaque_semantics":["alpha","beta"]}',
    owner_id: str = "SYNTHETIC_OWNER_AUTHORITY",
    owner_version: str = "fixture-1.0.0",
    owner_hash: str = hashlib.sha256(b"synthetic-owner-authority").hexdigest(),
    reverse_refs: bool = False,
) -> OwnerBoundSubjectInput:
    semantic_object_ref = _ref(
        "SYNTHETIC_OWNER_BOUND_NONACTOR_OBJECT",
        "urn:synthetic:gt34:s2:subject-object:a",
        semantic_object_bytes,
    )
    evidence = (
        _ref("SYNTHETIC_EVIDENCE", "urn:synthetic:evidence:1", b"evidence-1"),
        _ref("SYNTHETIC_EVIDENCE", "urn:synthetic:evidence:2", b"evidence-2"),
    )
    provenance = (
        _ref("SYNTHETIC_PROVENANCE", "urn:synthetic:provenance:1", b"provenance-1"),
        _ref("SYNTHETIC_PROVENANCE", "urn:synthetic:provenance:2", b"provenance-2"),
    )
    if reverse_refs:
        evidence = tuple(reversed(evidence))
        provenance = tuple(reversed(provenance))
    binding = compute_owner_binding_content_hash(
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=semantic_object_ref,
        semantic_object_bytes=semantic_object_bytes,
        evidence_refs=evidence,
        provenance_refs=provenance,
    )
    return OwnerBoundSubjectInput(
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=semantic_object_ref,
        semantic_object_bytes=semantic_object_bytes,
        evidence_refs=evidence,
        provenance_refs=provenance,
        owner_binding_content_hash=binding,
    )


def test_synthetic_fixture_only_and_no_real_canary_identity() -> None:
    material = _fixture()
    assert b"Q69B" not in material.semantic_object_bytes
    assert b"clinic" not in material.semantic_object_bytes.lower()
    assert b"hospital" not in material.semantic_object_bytes.lower()
    assert material.semantic_object_ref.ref_id.startswith("urn:synthetic:")


def test_exact_materialization_is_deterministic_across_registry_instances() -> None:
    material = _fixture()
    a = OneObjectSubjectRegistry().materialize(material)
    b = OneObjectSubjectRegistry().materialize(material)
    assert a == b
    assert a.materializer_id == MATERIALIZER_ID
    assert a.materializer_version == MATERIALIZER_VERSION
    assert a.subject_ref.startswith("urn:rawlsing:v3:subject:sha256:")
    assert a.receipt_id.startswith(
        "urn:rawlsing:v3:subject-materialization-receipt:sha256:"
    )


def test_duplicate_identical_input_is_idempotent_in_one_object_registry() -> None:
    registry = OneObjectSubjectRegistry()
    material = _fixture()
    first = registry.materialize(material)
    second = registry.materialize(material)
    assert first is second
    assert registry.receipt is first


def test_second_distinct_object_fails_closed_in_one_object_registry() -> None:
    registry = OneObjectSubjectRegistry()
    registry.materialize(_fixture())
    other = _fixture(
        semantic_object_bytes=b'{"fixture":"SYNTHETIC_NONACTOR_OBJECT_B","opaque_semantics":["alpha","beta"]}'
    )
    with pytest.raises(OneObjectRegistryOccupiedError):
        registry.materialize(other)


def test_changed_semantic_object_changes_subject_and_receipt_identity() -> None:
    a = materialize_owner_bound_subject(_fixture())
    b = materialize_owner_bound_subject(
        _fixture(
            semantic_object_bytes=b'{"fixture":"SYNTHETIC_NONACTOR_OBJECT_A","opaque_semantics":["alpha","gamma"]}'
        )
    )
    assert a.subject_ref != b.subject_ref
    assert a.receipt_id != b.receipt_id


def test_changed_owner_authority_changes_subject_identity() -> None:
    a = materialize_owner_bound_subject(_fixture())
    b = materialize_owner_bound_subject(
        _fixture(
            owner_id="SYNTHETIC_OWNER_AUTHORITY_2",
            owner_hash=hashlib.sha256(b"synthetic-owner-authority-2").hexdigest(),
        )
    )
    assert a.subject_ref != b.subject_ref


def test_reference_input_order_is_not_identity_authority() -> None:
    a = materialize_owner_bound_subject(_fixture(reverse_refs=False))
    b = materialize_owner_bound_subject(_fixture(reverse_refs=True))
    assert a.subject_ref == b.subject_ref
    assert a.receipt_id == b.receipt_id


def test_semantic_owner_transfer_is_explicitly_false_and_fields_are_not_interpreted() -> None:
    receipt = materialize_owner_bound_subject(_fixture())
    assert receipt.semantic_owner_transfer is False
    assert receipt.semantic_fields_interpreted is False
    wire = receipt.as_dict()
    assert wire["schema_id"] == RECEIPT_SCHEMA
    assert wire["semantic_owner_transfer"] is False
    assert wire["semantic_fields_interpreted"] is False
    serialized = repr(wire).lower()
    assert "opaque_semantics" not in serialized
    assert "clinic" not in serialized
    assert "hospital" not in serialized


def test_display_label_geography_wall_clock_and_random_uuid_are_not_inputs() -> None:
    names = {field.name for field in fields(OwnerBoundSubjectInput)}
    assert "display_label" not in names
    assert "geography" not in names
    assert "wall_clock" not in names
    assert "uuid" not in names
    assert "rng" not in names


def test_semantic_object_hash_mismatch_fails_closed() -> None:
    material = _fixture()
    bad_ref = replace(material.semantic_object_ref, sha256="0" * 64)
    bad = replace(material, semantic_object_ref=bad_ref)
    with pytest.raises(SubjectMaterializationError, match="bytes/hash mismatch"):
        materialize_owner_bound_subject(bad)


def test_owner_binding_hash_mismatch_fails_closed() -> None:
    material = replace(_fixture(), owner_binding_content_hash="0" * 64)
    with pytest.raises(SubjectMaterializationError, match="owner binding"):
        materialize_owner_bound_subject(material)


@pytest.mark.parametrize(
    "change",
    [
        {"semantic_owner_authority_id": ""},
        {"semantic_owner_authority_version": ""},
        {"semantic_owner_authority_hash": "not-a-hash"},
        {"evidence_refs": ()},
        {"provenance_refs": ()},
        {"semantic_object_bytes": b""},
    ],
)
def test_malformed_unknown_or_unowned_input_fails_closed(change: dict[str, object]) -> None:
    material = replace(_fixture(), **change)
    with pytest.raises(SubjectMaterializationError):
        materialize_owner_bound_subject(material)


def test_duplicate_exact_evidence_ref_fails_closed() -> None:
    material = _fixture()
    duplicated = (material.evidence_refs[0], material.evidence_refs[0])
    changed = replace(material, evidence_refs=duplicated)
    with pytest.raises(SubjectMaterializationError, match="duplicate exact refs"):
        materialize_owner_bound_subject(changed)


def test_receipt_binds_exact_owner_object_evidence_provenance_and_replay() -> None:
    material = _fixture()
    receipt = materialize_owner_bound_subject(material)
    wire = receipt.as_dict()
    assert wire["materializer_id"] == MATERIALIZER_ID
    assert wire["materializer_version"] == MATERIALIZER_VERSION
    assert wire["semantic_owner_authority"]["id"] == material.semantic_owner_authority_id
    assert (
        wire["semantic_owner_authority"]["content_hash"]
        == material.semantic_owner_authority_hash
    )
    assert wire["semantic_object_ref"] == material.semantic_object_ref.as_dict()
    assert wire["owner_binding_content_hash"] == material.owner_binding_content_hash
    assert len(wire["evidence_refs"]) == 2
    assert len(wire["provenance_refs"]) == 2
    assert len(wire["replay_input_hash"]) == 64
    assert wire["integrity_state"] == "VERIFIED_OWNER_BOUND_INPUT"


def test_contract_names_are_bounded_implementation_not_semantic_authority() -> None:
    assert MATERIALIZER_ID == (
        "GT34_V3P1_ONE_OBJECT_OWNER_PRESERVING_SUBJECT_REGISTRY_MATERIALIZER"
    )
    assert MATERIALIZER_VERSION == "1.0.0"
    assert SUBJECT_REF_SCHEME == "RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1"
    assert "AUTHORITY" not in MATERIALIZER_ID
