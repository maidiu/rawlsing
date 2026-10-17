from __future__ import annotations

from dataclasses import fields, replace
import hashlib
import inspect
import json
from pathlib import Path

import pytest

import rawlsing_next.gt34_s2_v3p1_subject_registry_materializer as historical_s2
import rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer as u2


ROOT = Path(__file__).resolve().parents[2]
ADOPTION = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL053_REPAIRED_HASH_GRAPH_HQ_ADOPTION_R1/"
    "01_OBL053_REPAIRED_HQ_ADOPTION.json"
)


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _ref(kind: str, ref_id: str, raw: bytes) -> u2.ExactImmutableRef:
    return u2.ExactImmutableRef(kind, ref_id, _sha256(raw))


def _shadow_root(tag: str = "A") -> tuple[u2.AcceptedOwnerRoot, bytes]:
    object_bytes = (
        b'{"fixture":"SYNTHETIC_SHADOW_'
        + tag.encode("ascii")
        + b'","opaque_semantics":{"clinic":"public","label":"looks-real"}}'
    )
    object_ref = _ref(
        "SYNTHETIC_NONCURRENT_OBJECT",
        f"urn:synthetic:u2:shadow:{tag.lower()}",
        object_bytes,
    )
    evidence = (
        _ref("SYNTHETIC_EVIDENCE", "urn:synthetic:u2:evidence:1", b"e1"),
    )
    provenance = (
        _ref("SYNTHETIC_PROVENANCE", "urn:synthetic:u2:prov:1", b"p1"),
        _ref("SYNTHETIC_PROVENANCE", "urn:synthetic:u2:prov:2", b"p2"),
    )
    root = u2.AcceptedOwnerRoot(
        adoption_artifact_blob=hashlib.sha1(
            f"synthetic-shadow-root-{tag}".encode("ascii")
        ).hexdigest(),
        semantic_owner_authority_id=f"SYNTHETIC_SHADOW_OWNER_{tag}",
        semantic_owner_authority_version="test-only-1.0.0",
        semantic_owner_authority_hash=_sha256(
            f"synthetic-shadow-owner-{tag}".encode("ascii")
        ),
        generation_seed_hash=_sha256(
            f"synthetic-shadow-seed-{tag}".encode("ascii")
        ),
        semantic_object_ref=object_ref,
        objective_evidence_receipt_hash=_sha256(
            f"synthetic-shadow-receipt-{tag}".encode("ascii")
        ),
        evidence_refs=evidence,
        provenance_refs=provenance,
        currentness_state="NONCURRENT_SYNTHETIC_TEST_ONLY",
        object_cardinality=1,
    )
    return root, object_bytes


def _material_for_root(
    root: u2.AcceptedOwnerRoot,
    object_bytes: bytes,
) -> u2.OwnerBoundSubjectInput:
    binding = u2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
    )
    return u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=object_bytes,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash=binding,
    )


def _hostile_material(tag: str = "A") -> u2.OwnerBoundSubjectInput:
    raw = b"HOSTILE_" + tag.encode("ascii")
    object_ref = _ref(
        "HOSTILE_OBJECT",
        f"urn:hostile:u2:{tag.lower()}",
        raw,
    )
    evidence = (_ref("HOSTILE_EVIDENCE", "urn:hostile:evidence", b"e"),)
    provenance = (_ref("HOSTILE_PROVENANCE", "urn:hostile:prov", b"p"),)
    owner_hash = _sha256(b"hostile-owner")
    binding = u2.compute_owner_binding_content_hash(
        semantic_owner_authority_id="HOSTILE_UNREGISTERED_OWNER",
        semantic_owner_authority_version="999.999.999",
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        semantic_object_bytes=raw,
        evidence_refs=evidence,
        provenance_refs=provenance,
    )
    return u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id="HOSTILE_UNREGISTERED_OWNER",
        semantic_owner_authority_version="999.999.999",
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        semantic_object_bytes=raw,
        evidence_refs=evidence,
        provenance_refs=provenance,
        owner_binding_content_hash=binding,
    )


def test_current_root_matches_fresh_hq_adoption_artifact_exactly() -> None:
    adoption = json.loads(ADOPTION.read_text(encoding="utf-8"))
    root = u2.CURRENT_ACCEPTED_OWNER_ROOT

    assert root.adoption_artifact_blob == u2.FRESH_OBL053_ADOPTION_ARTIFACT_BLOB
    assert adoption["authority"]["authority_id"] == root.semantic_owner_authority_id
    assert adoption["authority"]["authority_version"] == root.semantic_owner_authority_version
    assert adoption["authority"]["authority_content_hash"] == root.semantic_owner_authority_hash
    assert adoption["admitted_generation_seed_hash"] == root.generation_seed_hash
    assert adoption["semantic_object"]["object_id"] == root.semantic_object_ref.ref_id
    assert (
        adoption["semantic_object"]["object_content_hash"]
        == root.semantic_object_ref.sha256
    )
    assert (
        adoption["generated_fact_provenance_integrity_receipt_hash"]
        == root.objective_evidence_receipt_hash
    )
    assert root.object_cardinality == 1


def test_current_one_object_permit_is_content_addressed_and_current() -> None:
    permit = u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
    assert permit.validated_structurally() is permit
    assert permit.validated_for_current_root() is permit
    assert permit.accepted_owner_root == u2.CURRENT_ACCEPTED_OWNER_ROOT
    assert permit.accepted_owner_root_hash == u2.CURRENT_ACCEPTED_OWNER_ROOT_HASH
    assert permit.permit_id.endswith(permit.permit_hash)
    assert permit.object_cardinality == 1


def test_historical_adoption_blob_cannot_authenticate_current_permit() -> None:
    old_root = replace(
        u2.CURRENT_ACCEPTED_OWNER_ROOT,
        adoption_artifact_blob=u2.HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB,
    )
    old_permit = u2._build_permit(old_root)
    with pytest.raises(u2.MaterializationPermitError, match="current accepted OBL053 root"):
        old_permit.validated_for_current_root()


@pytest.mark.parametrize(
    "changed_root",
    [
        lambda root: replace(
            root,
            semantic_owner_authority_hash=u2.HISTORICAL_INVALID_AUTHORITY_HASH,
        ),
        lambda root: replace(
            root,
            semantic_object_ref=replace(
                root.semantic_object_ref,
                ref_id=(
                    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:"
                    "sha256:" + u2.HISTORICAL_INVALID_OBJECT_HASH
                ),
                sha256=u2.HISTORICAL_INVALID_OBJECT_HASH,
            ),
        ),
        lambda root: replace(
            root,
            objective_evidence_receipt_hash=u2.HISTORICAL_INVALID_RECEIPT_HASH,
        ),
    ],
)
def test_historical_invalid_identity_roots_cannot_become_current(changed_root) -> None:
    forged = u2._build_permit(changed_root(u2.CURRENT_ACCEPTED_OWNER_ROOT))
    with pytest.raises(u2.MaterializationPermitError):
        forged.validated_for_current_root()


def test_unregistered_owner_self_binding_attack_now_fails_before_ref_emission() -> None:
    hostile = _hostile_material()
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="semantic owner id"):
        u2.materialize_owner_bound_subject(
            hostile,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_hostile_caller_cannot_mint_an_alternate_current_permit() -> None:
    hostile = _hostile_material()
    hostile_root = u2.AcceptedOwnerRoot(
        adoption_artifact_blob=hashlib.sha1(b"hostile-adoption").hexdigest(),
        semantic_owner_authority_id=hostile.semantic_owner_authority_id,
        semantic_owner_authority_version=hostile.semantic_owner_authority_version,
        semantic_owner_authority_hash=hostile.semantic_owner_authority_hash,
        generation_seed_hash=_sha256(b"hostile-seed"),
        semantic_object_ref=hostile.semantic_object_ref,
        objective_evidence_receipt_hash=_sha256(b"hostile-receipt"),
        evidence_refs=hostile.evidence_refs,
        provenance_refs=hostile.provenance_refs,
        currentness_state="HOSTILE_SELF_ASSERTED_CURRENT",
        object_cardinality=1,
    )
    hostile_permit = u2._build_permit(hostile_root)
    assert hostile_permit.validated_structurally() is hostile_permit
    with pytest.raises(u2.MaterializationPermitError, match="current accepted OBL053 root"):
        hostile_permit.validated_for_current_root()
    with pytest.raises(u2.MaterializationPermitError):
        u2.materialize_owner_bound_subject(hostile, hostile_permit)


def test_stateless_materialization_requires_explicit_valid_permit() -> None:
    hostile = _hostile_material()
    with pytest.raises(TypeError):
        u2.materialize_owner_bound_subject(hostile)  # type: ignore[call-arg]
    with pytest.raises(u2.MaterializationPermitError):
        u2.materialize_owner_bound_subject(hostile, None)  # type: ignore[arg-type]


def test_same_current_permit_rejects_any_distinct_object() -> None:
    hostile = _hostile_material("B")
    exact_owner_but_other_object = replace(
        hostile,
        semantic_owner_authority_id=u2.OBL053_AUTHORITY_ID,
        semantic_owner_authority_version=u2.OBL053_AUTHORITY_VERSION,
        semantic_owner_authority_hash=u2.OBL053_AUTHORITY_HASH,
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="semantic object ref"):
        u2.materialize_owner_bound_subject(
            exact_owner_but_other_object,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_fresh_registry_instances_do_not_create_new_object_permission() -> None:
    permit = u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
    registry_a = u2.OneObjectSubjectRegistry(permit)
    registry_b = u2.OneObjectSubjectRegistry(permit)
    hostile = _hostile_material("C")

    for registry in (registry_a, registry_b):
        with pytest.raises(u2.AcceptedOwnerAuthenticationError):
            registry.materialize(hostile)
        assert registry.receipt is None


def test_evidence_and_provenance_lineage_mutations_fail_before_materialization() -> None:
    root = u2.CURRENT_ACCEPTED_OWNER_ROOT
    bad_evidence = replace(
        u2.CURRENT_EVIDENCE_REFS[0],
        ref_id="urn:hostile:replacement-evidence",
    )
    bad_material_evidence = u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=b"not-read-because-lineage-fails-first",
        evidence_refs=(bad_evidence,),
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash="0" * 64,
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="evidence lineage"):
        u2.materialize_owner_bound_subject(
            bad_material_evidence,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )

    bad_provenance = replace(
        u2.CURRENT_PROVENANCE_REFS[0],
        ref_id="urn:hostile:replacement-provenance",
    )
    bad_material_provenance = replace(
        bad_material_evidence,
        evidence_refs=root.evidence_refs,
        provenance_refs=(bad_provenance, u2.CURRENT_PROVENANCE_REFS[1]),
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="provenance lineage"):
        u2.materialize_owner_bound_subject(
            bad_material_provenance,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_semantic_object_bytes_hash_mismatch_fails_closed() -> None:
    root = u2.CURRENT_ACCEPTED_OWNER_ROOT
    material = u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=b"definitely-not-the-adopted-object",
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash="0" * 64,
    )
    with pytest.raises(u2.SubjectMaterializationError, match="bytes/hash mismatch"):
        u2.materialize_owner_bound_subject(
            material,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_noncurrent_shadow_fixture_proves_determinism_and_idempotence() -> None:
    root, raw = _shadow_root("A")
    permit = u2._build_permit(root)
    material = _material_for_root(root, raw)

    first = u2._materialize_noncurrent_shadow_fixture(material, permit)
    second = u2._materialize_noncurrent_shadow_fixture(material, permit)

    assert first == second
    assert first.subject_ref.startswith("urn:rawlsing:v3:subject:sha256:")
    assert first.integrity_state == "NONCURRENT_SYNTHETIC_TEST_ONLY"
    assert first.semantic_owner_transfer is False
    assert first.semantic_fields_interpreted is False


def test_noncurrent_shadow_permit_rejects_second_distinct_object() -> None:
    root, raw = _shadow_root("A")
    permit = u2._build_permit(root)
    u2._materialize_noncurrent_shadow_fixture(
        _material_for_root(root, raw),
        permit,
    )

    other_root, other_raw = _shadow_root("B")
    other_material = _material_for_root(other_root, other_raw)
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="semantic owner id"):
        u2._materialize_noncurrent_shadow_fixture(other_material, permit)


def test_shadow_receipt_is_semantically_opaque_despite_hostile_looking_bytes() -> None:
    root, raw = _shadow_root("OPAQUE")
    permit = u2._build_permit(root)
    receipt = u2._materialize_noncurrent_shadow_fixture(
        _material_for_root(root, raw),
        permit,
    )
    wire = json.dumps(receipt.as_dict(), sort_keys=True).lower()
    assert "clinic" not in wire
    assert "public" not in wire
    assert "looks-real" not in wire
    assert "opaque_semantics" not in wire
    assert receipt.semantic_owner_transfer is False
    assert receipt.semantic_fields_interpreted is False


def test_production_receipt_contract_binds_root_permit_and_no_semantic_fields() -> None:
    receipt_fields = {field.name for field in fields(u2.SubjectMaterializationReceipt)}
    assert {
        "adoption_artifact_blob",
        "accepted_owner_root_hash",
        "materialization_permit_id",
        "materialization_permit_hash",
        "semantic_owner_authority_hash",
        "semantic_object_ref",
        "evidence_refs",
        "provenance_refs",
    } <= receipt_fields
    assert not {
        "entity_family",
        "facility_domain",
        "facility_form",
        "facility_function",
        "ownership_status",
        "classifier",
        "actor_id",
        "encounter",
    } & receipt_fields


def test_random_time_label_environment_are_not_identity_inputs() -> None:
    for cls in (
        u2.OwnerBoundSubjectInput,
        u2.AcceptedOwnerRoot,
        u2.OneObjectMaterializationPermit,
        u2.SubjectMaterializationReceipt,
    ):
        names = {field.name for field in fields(cls)}
        assert not {
            "uuid",
            "rng",
            "wall_clock",
            "timestamp",
            "display_label",
            "filesystem_order",
            "environment",
        } & names


def test_successor_is_distinct_from_historical_failed_s2_and_shadow_is_not_public() -> None:
    assert u2.MATERIALIZER_ID != historical_s2.MATERIALIZER_ID
    assert u2.MATERIALIZER_VERSION == "2.0.0"
    assert "materialize_owner_bound_subject" in u2.__all__
    assert "_materialize_noncurrent_shadow_fixture" not in u2.__all__
    assert "_build_permit" not in u2.__all__
    assert historical_s2.materialize_owner_bound_subject is not u2.materialize_owner_bound_subject


def test_no_downstream_semantic_authority_was_added_to_public_contract() -> None:
    public = " ".join(u2.__all__).lower()
    assert "classifier" not in public
    assert "encounter" not in public
    assert "psepf" not in public
    assert "metabolism" not in public
    assert "can008" not in public
    assert "positive_v3" not in public

    source = inspect.getsource(u2.materialize_owner_bound_subject)
    assert "semantic_object_bytes" not in source
    assert "json.loads" not in source
