from __future__ import annotations

from dataclasses import replace
import hashlib
import inspect
import json
from pathlib import Path

import pytest

import rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer as u2


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1"
)
SOURCE = BASE / (
    "GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/"
    "V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/01_REPAIRED_HASH_GRAPH_CANDIDATE.json"
)
ADOPTION = BASE / (
    "GT3_GT4_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION_R1/"
    "01_OBL054_CORRECTED_MATERIALIZER_HQ_ADOPTION.json"
)
OUTPUT = BASE / (
    "GT3_GT4_POST_OBL054_PARALLEL_EXECUTION_WAVE_R1/"
    "W1_OBL052_FIRST_CANARY_SUBJECT_MATERIALIZATION_R1/"
    "01_CURRENT_FIRST_CANARY_MATERIALIZATION.json"
)

EXPECTED_OBJECT_HASH = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
EXPECTED_OBL054_ADOPTION_BLOB = "fc46d377dafa5b2c4e274d702e7f26268aa429cb"
EXPECTED_ROOT_HASH = "1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8"
EXPECTED_PERMIT_HASH = "3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc"
SUBJECT_DOMAIN = b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
RECEIPT_DOMAIN = b"RAWLSING\0GT34-U2\0V3P1-AUTHENTICATED-SUBJECT-RECEIPT-V2\0"


def _canon(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash_domain(domain: bytes, value: object) -> str:
    return hashlib.sha256(domain + _canon(value).encode("utf-8")).hexdigest()


def _canonical_object_bytes() -> bytes:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    projection = source["prospective_semantic_object"]["semantic_projection"]
    return _canon(projection).encode("utf-8")


def _material() -> u2.OwnerBoundSubjectInput:
    raw = _canonical_object_bytes()
    binding = u2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=u2.OBL053_AUTHORITY_ID,
        semantic_owner_authority_version=u2.OBL053_AUTHORITY_VERSION,
        semantic_owner_authority_hash=u2.OBL053_AUTHORITY_HASH,
        semantic_object_ref=u2.CURRENT_SEMANTIC_OBJECT_REF,
        semantic_object_bytes=raw,
        evidence_refs=u2.CURRENT_EVIDENCE_REFS,
        provenance_refs=u2.CURRENT_PROVENANCE_REFS,
    )
    return u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=u2.OBL053_AUTHORITY_ID,
        semantic_owner_authority_version=u2.OBL053_AUTHORITY_VERSION,
        semantic_owner_authority_hash=u2.OBL053_AUTHORITY_HASH,
        semantic_object_ref=u2.CURRENT_SEMANTIC_OBJECT_REF,
        semantic_object_bytes=raw,
        evidence_refs=u2.CURRENT_EVIDENCE_REFS,
        provenance_refs=u2.CURRENT_PROVENANCE_REFS,
        owner_binding_content_hash=binding,
    )


def _persisted() -> dict[str, object]:
    return json.loads(OUTPUT.read_text(encoding="utf-8"))


def test_01_canonical_object_hash_exact() -> None:
    raw = _canonical_object_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_OBJECT_HASH
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert source["prospective_semantic_object"]["semantic_object_content_hash"] == EXPECTED_OBJECT_HASH
    assert u2.CURRENT_SEMANTIC_OBJECT_REF.sha256 == EXPECTED_OBJECT_HASH


def test_02_adopted_root_and_permit_are_exact_and_valid() -> None:
    adoption_raw = ADOPTION.read_bytes()
    blob = hashlib.sha1(f"blob {len(adoption_raw)}\0".encode("ascii") + adoption_raw).hexdigest()
    assert blob == EXPECTED_OBL054_ADOPTION_BLOB
    adoption = json.loads(adoption_raw)
    assert adoption["adopted_identity"]["accepted_root_hash"] == EXPECTED_ROOT_HASH
    assert adoption["adopted_identity"]["one_object_permit_hash"] == EXPECTED_PERMIT_HASH
    assert u2.CURRENT_ACCEPTED_OWNER_ROOT_HASH == EXPECTED_ROOT_HASH
    assert u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT.permit_hash == EXPECTED_PERMIT_HASH
    assert u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT.validated_for_current_root() is u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT


def test_03_production_materialization_succeeds_and_matches_persisted() -> None:
    receipt = u2.materialize_owner_bound_subject(
        _material(), u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
    )
    persisted = _persisted()
    assert receipt.as_dict() == persisted["production_receipt"]
    assert receipt.subject_ref == persisted["subject_ref"]
    assert receipt.receipt_id == persisted["production_receipt_id"]


def test_04_subject_ref_identity_is_independently_recomputed() -> None:
    material = _material()
    owner_material = material.owner_binding_material()
    identity = {
        "scheme": u2.SUBJECT_REF_SCHEME,
        "semantic_owner_authority": owner_material["semantic_owner_authority"],
        "semantic_object_ref": material.semantic_object_ref.as_dict(),
        "owner_binding_content_hash": material.owner_binding_content_hash,
        "evidence_refs": [r.as_dict() for r in sorted(material.evidence_refs)],
        "provenance_refs": [r.as_dict() for r in sorted(material.provenance_refs)],
    }
    expected_hash = _hash_domain(SUBJECT_DOMAIN, identity)
    persisted = _persisted()
    assert persisted["subject_ref_hash"] == expected_hash
    assert persisted["subject_ref"] == f"urn:rawlsing:v3:subject:sha256:{expected_hash}"


def test_05_production_receipt_hash_is_independently_recomputed() -> None:
    persisted = _persisted()
    wire = dict(persisted["production_receipt"])
    receipt_hash = wire.pop("receipt_hash")
    wire.pop("receipt_id")
    expected = _hash_domain(RECEIPT_DOMAIN, wire)
    assert expected == receipt_hash
    assert persisted["production_receipt_hash"] == expected
    assert persisted["production_receipt_id"].endswith(expected)


def test_06_exact_replay_is_byte_for_model_identical() -> None:
    a = u2.materialize_owner_bound_subject(_material(), u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)
    b = u2.materialize_owner_bound_subject(_material(), u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)
    assert a == b
    assert _canon(a.as_dict()) == _canon(b.as_dict())


def test_07_fresh_registry_is_idempotent_for_exact_input() -> None:
    registry = u2.OneObjectSubjectRegistry(u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)
    a = registry.materialize(_material())
    b = registry.materialize(_material())
    assert a is b
    assert a.as_dict() == _persisted()["production_receipt"]


def test_08_one_bit_object_mutation_fails() -> None:
    material = _material()
    raw = bytearray(material.semantic_object_bytes)
    raw[0] ^= 1
    with pytest.raises(u2.SubjectMaterializationError):
        u2.materialize_owner_bound_subject(
            replace(material, semantic_object_bytes=bytes(raw)),
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


@pytest.mark.parametrize("field", ["owner", "object", "evidence", "provenance"])
def test_09_identity_lineage_mutations_fail(field: str) -> None:
    material = _material()
    if field == "owner":
        mutated = replace(material, semantic_owner_authority_hash="0" * 64)
    elif field == "object":
        mutated = replace(
            material,
            semantic_object_ref=replace(material.semantic_object_ref, ref_id="urn:hostile:other"),
        )
    elif field == "evidence":
        mutated = replace(
            material,
            evidence_refs=(replace(material.evidence_refs[0], ref_id="urn:hostile:evidence"),),
        )
    else:
        mutated = replace(
            material,
            provenance_refs=(
                replace(material.provenance_refs[0], ref_id="urn:hostile:provenance"),
                material.provenance_refs[1],
            ),
        )
    with pytest.raises(u2.SubjectMaterializationError):
        u2.materialize_owner_bound_subject(mutated, u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)


def test_10_historical_obl053_root_fails() -> None:
    historical = replace(
        u2.CURRENT_ACCEPTED_OWNER_ROOT,
        adoption_artifact_blob=u2.HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB,
    )
    permit = u2._build_permit(historical)
    with pytest.raises(u2.MaterializationPermitError):
        permit.validated_for_current_root()


def test_11_second_object_fails_under_current_permit() -> None:
    material = _material()
    other_ref = replace(
        material.semantic_object_ref,
        ref_id="urn:rawlsing:gt34:hostile-second-object",
        sha256=hashlib.sha256(b"second").hexdigest(),
    )
    other = replace(material, semantic_object_ref=other_ref, semantic_object_bytes=b"second")
    with pytest.raises(u2.AcceptedOwnerAuthenticationError):
        u2.materialize_owner_bound_subject(other, u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)


def test_12_shadow_path_cannot_satisfy_persisted_production_artifact() -> None:
    persisted = _persisted()
    assert "_materialize_noncurrent_shadow_fixture" not in u2.__all__
    assert persisted["production_receipt"]["schema_id"] == u2.RECEIPT_SCHEMA
    assert persisted["production_receipt"]["integrity_state"].startswith("AUTHENTICATED_FRESH_OBL053_ROOT")
    assert "NONCURRENT_SYNTHETIC_TEST_ONLY" not in _canon(persisted["production_receipt"])


def test_13_receipt_is_bound_to_adoption_root_and_permit() -> None:
    persisted = _persisted()
    wire = persisted["production_receipt"]
    assert wire["adoption_artifact_blob"] == u2.FRESH_OBL053_ADOPTION_ARTIFACT_BLOB
    assert wire["accepted_owner_root_hash"] == EXPECTED_ROOT_HASH
    assert wire["materialization_permit_id"] == u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT.permit_id
    assert wire["materialization_permit_hash"] == EXPECTED_PERMIT_HASH
    assert persisted["adopted_materializer"]["obl054_hq_adoption_artifact_blob"] == EXPECTED_OBL054_ADOPTION_BLOB


def test_14_semantic_fields_are_not_interpreted() -> None:
    source = "\n".join([
        inspect.getsource(u2.materialize_owner_bound_subject),
        inspect.getsource(u2._materialization_core),
        inspect.getsource(u2._validate_material_against_root),
        inspect.getsource(u2.OwnerBoundSubjectInput.owner_binding_material),
    ]).lower()
    assert "json.loads" not in source
    assert ".decode(" not in source
    for field in ("entity_family", "facility_domain", "facility_form", "facility_function", "ownership_status"):
        assert field not in source
    assert _persisted()["semantic_fields_interpreted"] is False


def test_15_no_classifier_proposition_is_emitted() -> None:
    wire = _canon(_persisted()["production_receipt"]).lower()
    assert "subject_is_public_clinic_or_hospital" not in wire
    assert "classifier" not in wire


def test_16_no_actor_contact_use_encounter_exposure_is_emitted() -> None:
    wire = _canon(_persisted()["production_receipt"]).lower()
    for forbidden in ("actor_id", "contact", "encounter", "exposure", "actor_used_subject"):
        assert forbidden not in wire


def test_17_no_downstream_authority_is_created() -> None:
    public = " ".join(u2.__all__).lower()
    receipt_wire = _canon(_persisted()["production_receipt"]).lower()
    for forbidden in ("comparator", "psepf", "metabolism", "can008", "positive_v3"):
        assert forbidden not in public
        assert forbidden not in receipt_wire
    assert _persisted()["semantic_owner_transfer"] is False


def test_18_exactly_one_current_materialization_artifact_in_lane() -> None:
    lane = OUTPUT.parent
    current = []
    for path in lane.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") == "GT34_W1_OBL052_FIRST_CANARY_CURRENT_MATERIALIZATION@1.0.0":
            current.append(path)
    assert current == [OUTPUT]
