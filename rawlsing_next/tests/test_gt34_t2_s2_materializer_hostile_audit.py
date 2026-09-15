from __future__ import annotations

import hashlib
import json

import pytest

import rawlsing_next.gt34_s2_v3p1_subject_registry_materializer as s2


OWNER_BINDING_DOMAIN = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
)
SUBJECT_REF_DOMAIN = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
)
RECEIPT_DOMAIN = (
    b"RAWLSING\0GT34-S2\0V3P1-SUBJECT-MATERIALIZATION-RECEIPT-V1\0"
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash_domain(domain: bytes, value: object) -> str:
    return hashlib.sha256(domain + _canonical_json(value).encode("utf-8")).hexdigest()


def _ref(kind: str, ref_id: str, payload: bytes) -> s2.ExactImmutableRef:
    return s2.ExactImmutableRef(kind, ref_id, hashlib.sha256(payload).hexdigest())


def _hostile_input(tag: str = "A") -> s2.OwnerBoundSubjectInput:
    # Deliberately NOT an accepted Rawlsing semantic authority.  The attack asks
    # whether S2 authenticates ownership or merely checks self-consistent strings.
    owner_id = "HOSTILE_UNREGISTERED_OWNER"
    owner_version = "999.999.999"
    owner_hash = hashlib.sha256(b"not-an-accepted-authority").hexdigest()
    object_bytes = (
        b"\xff\x00HOSTILE_OPAQUE_OBJECT_"
        + tag.encode("ascii")
        + b'{"clinic":"public","label":"looks-real"}'
    )
    object_ref = _ref(
        "HOSTILE_NONACTOR_OBJECT",
        f"urn:hostile:object:{tag.lower()}",
        object_bytes,
    )
    evidence = (
        _ref("HOSTILE_EVIDENCE", "urn:hostile:evidence:2", b"e2"),
        _ref("HOSTILE_EVIDENCE", "urn:hostile:evidence:1", b"e1"),
    )
    provenance = (
        _ref("HOSTILE_PROVENANCE", "urn:hostile:prov:2", b"p2"),
        _ref("HOSTILE_PROVENANCE", "urn:hostile:prov:1", b"p1"),
    )
    owner_binding = s2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=evidence,
        provenance_refs=provenance,
    )
    return s2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=evidence,
        provenance_refs=provenance,
        owner_binding_content_hash=owner_binding,
    )


def _manual_identities(material: s2.OwnerBoundSubjectInput) -> tuple[str, str, str, str]:
    evidence = sorted(
        (ref.as_dict() for ref in material.evidence_refs),
        key=lambda item: (item["kind"], item["ref_id"], item["sha256"]),
    )
    provenance = sorted(
        (ref.as_dict() for ref in material.provenance_refs),
        key=lambda item: (item["kind"], item["ref_id"], item["sha256"]),
    )
    owner = {
        "id": material.semantic_owner_authority_id,
        "version": material.semantic_owner_authority_version,
        "content_hash": material.semantic_owner_authority_hash,
    }
    owner_binding_material = {
        "schema_id": s2.OWNER_BINDING_SCHEMA,
        "semantic_owner_authority": owner,
        "semantic_object_ref": material.semantic_object_ref.as_dict(),
        "evidence_refs": evidence,
        "provenance_refs": provenance,
    }
    owner_binding_hash = _hash_domain(OWNER_BINDING_DOMAIN, owner_binding_material)
    subject_material = {
        "scheme": s2.SUBJECT_REF_SCHEME,
        "semantic_owner_authority": owner,
        "semantic_object_ref": material.semantic_object_ref.as_dict(),
        "owner_binding_content_hash": owner_binding_hash,
        "evidence_refs": evidence,
        "provenance_refs": provenance,
    }
    subject_hash = _hash_domain(SUBJECT_REF_DOMAIN, subject_material)
    subject_ref = f"urn:rawlsing:v3:subject:sha256:{subject_hash}"
    replay_hash = hashlib.sha256(
        _canonical_json(subject_material).encode("utf-8")
    ).hexdigest()
    receipt_body = {
        "schema_id": s2.RECEIPT_SCHEMA,
        "subject_ref": subject_ref,
        "subject_ref_hash": subject_hash,
        "materializer_id": s2.MATERIALIZER_ID,
        "materializer_version": s2.MATERIALIZER_VERSION,
        "semantic_owner_authority": owner,
        "semantic_object_ref": material.semantic_object_ref.as_dict(),
        "owner_binding_content_hash": owner_binding_hash,
        "evidence_refs": evidence,
        "provenance_refs": provenance,
        "replay_input_hash": replay_hash,
        "integrity_state": "VERIFIED_OWNER_BOUND_INPUT",
        "semantic_owner_transfer": False,
        "semantic_fields_interpreted": False,
    }
    receipt_hash = _hash_domain(RECEIPT_DOMAIN, receipt_body)
    return owner_binding_hash, subject_hash, replay_hash, receipt_hash


def test_independent_recompute_matches_candidate_identity_law() -> None:
    material = _hostile_input("A")
    expected_binding, expected_subject, expected_replay, expected_receipt = (
        _manual_identities(material)
    )
    actual = s2.materialize_owner_bound_subject(material)
    assert material.owner_binding_content_hash == expected_binding
    assert actual.subject_ref_hash == expected_subject
    assert actual.replay_input_hash == expected_replay
    assert actual.receipt_hash == expected_receipt


def test_attack_unregistered_owner_can_self_bind_and_emit_subject_ref() -> None:
    # DEFECT PROOF: no accepted-authority snapshot/registry/capability is required.
    # Any caller can choose an arbitrary owner id/version/hash, compute the public
    # owner-binding hash, and receive a VERIFIED_OWNER_BOUND_INPUT receipt.
    material = _hostile_input("A")
    receipt = s2.materialize_owner_bound_subject(material)
    assert receipt.semantic_owner_authority_id == "HOSTILE_UNREGISTERED_OWNER"
    assert receipt.integrity_state == "VERIFIED_OWNER_BOUND_INPUT"
    assert receipt.subject_ref.startswith("urn:rawlsing:v3:subject:sha256:")


def test_attack_owner_binding_helper_is_not_an_authentication_primitive() -> None:
    material = _hostile_input("A")
    # The exact binding accepted by the materializer is reproducible by the
    # untrusted caller using only public inputs; no upstream acceptance proof is
    # part of the binding material.
    expected, _, _, _ = _manual_identities(material)
    assert material.owner_binding_content_hash == expected


def test_attack_stateless_export_emits_second_distinct_object_at_v1_grain() -> None:
    # DEFECT PROOF: exported stateless API bypasses OneObjectSubjectRegistry.
    a = s2.materialize_owner_bound_subject(_hostile_input("A"))
    b = s2.materialize_owner_bound_subject(_hostile_input("B"))
    assert a.subject_ref != b.subject_ref
    assert a.receipt_id != b.receipt_id
    assert "materialize_owner_bound_subject" in s2.__all__


def test_attack_multiple_registry_instances_escape_one_object_ceiling() -> None:
    # DEFECT PROOF: single-slot state is instance-local, not a V1 scope invariant.
    a = s2.OneObjectSubjectRegistry().materialize(_hostile_input("A"))
    b = s2.OneObjectSubjectRegistry().materialize(_hostile_input("B"))
    assert a.subject_ref != b.subject_ref


def test_same_registry_instance_does_block_second_distinct_object() -> None:
    registry = s2.OneObjectSubjectRegistry()
    registry.materialize(_hostile_input("A"))
    with pytest.raises(s2.OneObjectRegistryOccupiedError):
        registry.materialize(_hostile_input("B"))


def test_identical_input_is_idempotent() -> None:
    registry = s2.OneObjectSubjectRegistry()
    material = _hostile_input("A")
    first = registry.materialize(material)
    second = registry.materialize(material)
    assert first == second


def test_owner_hash_mutation_changes_identity_when_rebound() -> None:
    a = _hostile_input("A")
    b_hash = hashlib.sha256(b"different-unaccepted-owner-hash").hexdigest()
    b_binding = s2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=a.semantic_owner_authority_id,
        semantic_owner_authority_version=a.semantic_owner_authority_version,
        semantic_owner_authority_hash=b_hash,
        semantic_object_ref=a.semantic_object_ref,
        semantic_object_bytes=a.semantic_object_bytes,
        evidence_refs=a.evidence_refs,
        provenance_refs=a.provenance_refs,
    )
    b = s2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=a.semantic_owner_authority_id,
        semantic_owner_authority_version=a.semantic_owner_authority_version,
        semantic_owner_authority_hash=b_hash,
        semantic_object_ref=a.semantic_object_ref,
        semantic_object_bytes=a.semantic_object_bytes,
        evidence_refs=a.evidence_refs,
        provenance_refs=a.provenance_refs,
        owner_binding_content_hash=b_binding,
    )
    assert (
        s2.materialize_owner_bound_subject(a).subject_ref
        != s2.materialize_owner_bound_subject(b).subject_ref
    )


def test_object_bytes_ref_tamper_fails_closed() -> None:
    material = _hostile_input("A")
    tampered = s2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=material.semantic_owner_authority_id,
        semantic_owner_authority_version=material.semantic_owner_authority_version,
        semantic_owner_authority_hash=material.semantic_owner_authority_hash,
        semantic_object_ref=material.semantic_object_ref,
        semantic_object_bytes=material.semantic_object_bytes + b"x",
        evidence_refs=material.evidence_refs,
        provenance_refs=material.provenance_refs,
        owner_binding_content_hash=material.owner_binding_content_hash,
    )
    with pytest.raises(s2.SubjectMaterializationError, match="bytes/hash mismatch"):
        s2.materialize_owner_bound_subject(tampered)


def test_evidence_provenance_order_is_mechanical_not_semantic_precedence() -> None:
    a = _hostile_input("A")
    b_binding = s2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=a.semantic_owner_authority_id,
        semantic_owner_authority_version=a.semantic_owner_authority_version,
        semantic_owner_authority_hash=a.semantic_owner_authority_hash,
        semantic_object_ref=a.semantic_object_ref,
        semantic_object_bytes=a.semantic_object_bytes,
        evidence_refs=tuple(reversed(a.evidence_refs)),
        provenance_refs=tuple(reversed(a.provenance_refs)),
    )
    b = s2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=a.semantic_owner_authority_id,
        semantic_owner_authority_version=a.semantic_owner_authority_version,
        semantic_owner_authority_hash=a.semantic_owner_authority_hash,
        semantic_object_ref=a.semantic_object_ref,
        semantic_object_bytes=a.semantic_object_bytes,
        evidence_refs=tuple(reversed(a.evidence_refs)),
        provenance_refs=tuple(reversed(a.provenance_refs)),
        owner_binding_content_hash=b_binding,
    )
    assert s2.materialize_owner_bound_subject(a) == s2.materialize_owner_bound_subject(b)


def test_semantic_bytes_are_opaque_and_not_reemitted_as_materializer_truth() -> None:
    receipt = s2.materialize_owner_bound_subject(_hostile_input("A"))
    wire = receipt.as_dict()
    serialized = json.dumps(wire, sort_keys=True).lower()
    assert receipt.semantic_owner_transfer is False
    assert receipt.semantic_fields_interpreted is False
    assert '"clinic":"public"' not in serialized
    assert "looks-real" not in serialized


def test_identity_has_no_random_time_label_or_environment_inputs() -> None:
    material = _hostile_input("A")
    a = s2.materialize_owner_bound_subject(material)
    b = s2.materialize_owner_bound_subject(material)
    assert a == b
    assert not any(
        name in s2.OwnerBoundSubjectInput.__dataclass_fields__
        for name in ("uuid", "wall_clock", "display_label", "filesystem_order", "environment")
    )
