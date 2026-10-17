from __future__ import annotations

from dataclasses import fields, replace
import hashlib
import inspect
import json
from pathlib import Path
import re

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

U2_RETURN = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL054_CORRECTED_OWNER_AUTHENTICATION_REPAIR_WAVE_R1/"
    "U2_OBL054_CORRECTED_OWNER_AUTH_ONE_OBJECT_REPAIR_R1/00_RETURN.md"
)

U2_EVIDENCE = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL054_CORRECTED_OWNER_AUTHENTICATION_REPAIR_WAVE_R1/"
    "U2_OBL054_CORRECTED_OWNER_AUTH_ONE_OBJECT_REPAIR_R1/"
    "01_GOVERNED_REPAIR_EVIDENCE.json"
)

U2_MODULE = ROOT / "rawlsing_next/gt34_u2_v3p1_authenticated_subject_materializer.py"
U2_TEST = ROOT / "rawlsing_next/tests/test_gt34_u2_obl054_corrected_owner_auth_materializer.py"

ACCEPTED_ROOT_DOMAIN = (
    b"RAWLSING\0GT34-U2\0OBL054-ACCEPTED-OBL053-ROOT-V1\0"
)
PERMIT_DOMAIN = (
    b"RAWLSING\0GT34-U2\0OBL054-ONE-OBJECT-MATERIALIZATION-PERMIT-V1\0"
)
OWNER_BINDING_DOMAIN = (
    b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
)

REAL_SUBJECT_PATTERN = re.compile(
    r"urn:rawlsing:v3:subject:sha256:[0-9a-f]{64}"
)

EXPECTED_U2_MODULE_BLOB = "b0cb39a9a975381f3f3b4a03e7e435b2932e89b9"
EXPECTED_FRESH_ADOPTION_BLOB = "f561765bad4fdad2bbf4591f35fe7f81f8486428"
EXPECTED_CURRENT_ROOT_HASH = (
    "1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8"
)
EXPECTED_CURRENT_PERMIT_HASH = (
    "3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc"
)
HISTORICAL_ADOPTION_BLOB = "286ff7b851e920ff2760082d8b2fb194560ab127"
HISTORICAL_AUTHORITY_HASH = (
    "e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed"
)
HISTORICAL_OBJECT_HASH = (
    "d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53"
)
HISTORICAL_RECEIPT_HASH = (
    "1561942f1fe4fc43b248c61be866c0bc459773b7c6dbb8e393e13b064cdacce0"
)

U3_TEST = ROOT / "rawlsing_next/tests/test_gt34_u3_obl054_corrected_owner_auth_hostile_audit.py"
COURT_SPEC = ROOT / ".rabochii/court_spec.json"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _hash_domain(domain: bytes, value: object) -> str:
    return hashlib.sha256(
        domain + _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _sorted_refs(refs: tuple[u2.ExactImmutableRef, ...]) -> list[dict[str, str]]:
    return [
        {"kind": ref.kind, "ref_id": ref.ref_id, "sha256": ref.sha256}
        for ref in sorted(refs)
    ]


def _manual_root_material(root: u2.AcceptedOwnerRoot) -> dict[str, object]:
    return {
        "schema_id": "GT34_OBL054_ACCEPTED_OBL053_OWNER_ROOT@1.0.0",
        "adoption_artifact_blob": root.adoption_artifact_blob,
        "semantic_owner_authority": {
            "id": root.semantic_owner_authority_id,
            "version": root.semantic_owner_authority_version,
            "content_hash": root.semantic_owner_authority_hash,
        },
        "generation_seed_hash": root.generation_seed_hash,
        "semantic_object_ref": {
            "kind": root.semantic_object_ref.kind,
            "ref_id": root.semantic_object_ref.ref_id,
            "sha256": root.semantic_object_ref.sha256,
        },
        "objective_evidence_receipt_hash": root.objective_evidence_receipt_hash,
        "evidence_refs": _sorted_refs(root.evidence_refs),
        "provenance_refs": _sorted_refs(root.provenance_refs),
        "currentness_state": root.currentness_state,
        "object_cardinality": root.object_cardinality,
    }


def _manual_permit(root: u2.AcceptedOwnerRoot) -> u2.OneObjectMaterializationPermit:
    root_material = _manual_root_material(root)
    root_hash = _hash_domain(ACCEPTED_ROOT_DOMAIN, root_material)
    permit_material = {
        "schema_id": "GT34_OBL054_ONE_OBJECT_MATERIALIZATION_PERMIT@1.0.0",
        "accepted_owner_root": root_material,
        "accepted_owner_root_hash": root_hash,
        "scope": "EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY",
        "object_cardinality": 1,
    }
    permit_hash = _hash_domain(PERMIT_DOMAIN, permit_material)
    return u2.OneObjectMaterializationPermit(
        permit_id=(
            "urn:rawlsing:gt34:obl054:one-object-materialization-permit:"
            "sha256:" + permit_hash
        ),
        permit_hash=permit_hash,
        accepted_owner_root=root,
        accepted_owner_root_hash=root_hash,
        scope="EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY",
        object_cardinality=1,
    )


def _ref(kind: str, ref_id: str, raw: bytes) -> u2.ExactImmutableRef:
    return u2.ExactImmutableRef(kind, ref_id, _sha256(raw))


def _hostile_material(tag: str = "A") -> u2.OwnerBoundSubjectInput:
    raw = b"HOSTILE_U3_" + tag.encode("ascii")
    object_ref = _ref("HOSTILE_OBJECT", f"urn:hostile:u3:{tag}", raw)
    evidence = (_ref("HOSTILE_EVIDENCE", "urn:hostile:u3:evidence", b"e"),)
    provenance = (_ref("HOSTILE_PROVENANCE", "urn:hostile:u3:prov", b"p"),)
    owner_hash = _sha256(b"hostile-u3-owner")

    owner_binding_material = {
        "schema_id": u2.OWNER_BINDING_SCHEMA,
        "semantic_owner_authority": {
            "id": "HOSTILE_U3_OWNER",
            "version": "999.0.0",
            "content_hash": owner_hash,
        },
        "semantic_object_ref": {
            "kind": object_ref.kind,
            "ref_id": object_ref.ref_id,
            "sha256": object_ref.sha256,
        },
        "evidence_refs": _sorted_refs(evidence),
        "provenance_refs": _sorted_refs(provenance),
    }
    binding = _hash_domain(OWNER_BINDING_DOMAIN, owner_binding_material)

    return u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id="HOSTILE_U3_OWNER",
        semantic_owner_authority_version="999.0.0",
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        semantic_object_bytes=raw,
        evidence_refs=evidence,
        provenance_refs=provenance,
        owner_binding_content_hash=binding,
    )


def _shadow_fixture() -> tuple[
    u2.AcceptedOwnerRoot,
    u2.OneObjectMaterializationPermit,
    u2.OwnerBoundSubjectInput,
]:
    raw = b'{"shadow":"ONLY","clinic":"public","label":"hostile-looking"}'
    object_ref = _ref("SHADOW_OBJECT", "urn:shadow:u3:object", raw)
    evidence = (_ref("SHADOW_EVIDENCE", "urn:shadow:u3:evidence", b"e"),)
    provenance = (_ref("SHADOW_PROVENANCE", "urn:shadow:u3:prov", b"p"),)
    root = u2.AcceptedOwnerRoot(
        adoption_artifact_blob=hashlib.sha1(b"u3-shadow-root").hexdigest(),
        semantic_owner_authority_id="U3_SHADOW_OWNER",
        semantic_owner_authority_version="test-only",
        semantic_owner_authority_hash=_sha256(b"u3-shadow-owner"),
        generation_seed_hash=_sha256(b"u3-shadow-seed"),
        semantic_object_ref=object_ref,
        objective_evidence_receipt_hash=_sha256(b"u3-shadow-receipt"),
        evidence_refs=evidence,
        provenance_refs=provenance,
        currentness_state="NONCURRENT_SYNTHETIC_TEST_ONLY",
        object_cardinality=1,
    )
    permit = _manual_permit(root)
    binding = u2.compute_owner_binding_content_hash(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=raw,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
    )
    material = u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=raw,
        evidence_refs=root.evidence_refs,
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash=binding,
    )
    return root, permit, material


def test_independently_recompute_current_root_and_permit_from_fresh_adoption() -> None:
    adoption_raw = ADOPTION.read_bytes()
    independent_adoption_blob = _git_blob_sha1(adoption_raw)
    assert independent_adoption_blob == EXPECTED_FRESH_ADOPTION_BLOB

    u2_module_raw = U2_MODULE.read_bytes()
    assert _git_blob_sha1(u2_module_raw) == EXPECTED_U2_MODULE_BLOB

    adoption = json.loads(adoption_raw)

    evidence_ref = {
        "kind": "GT34_OBL053_OBJECTIVE_EVIDENCE_RECEIPT",
        "ref_id": (
            "urn:rawlsing:gt34:obl053:objective-evidence-receipt:sha256:"
            + adoption["generated_fact_provenance_integrity_receipt_hash"]
        ),
        "sha256": adoption["generated_fact_provenance_integrity_receipt_hash"],
    }
    provenance_refs = sorted(
        [
            {
                "kind": "GOVERNED_GENERATION_SEED",
                "ref_id": (
                    "urn:rawlsing:gt34:obl053:generation-seed:sha256:"
                    + adoption["admitted_generation_seed_hash"]
                ),
                "sha256": adoption["admitted_generation_seed_hash"],
            },
            {
                "kind": "SEMANTIC_OWNER_AUTHORITY",
                "ref_id": (
                    "urn:rawlsing:gt34:obl053:semantic-owner-authority:sha256:"
                    + adoption["authority"]["authority_content_hash"]
                ),
                "sha256": adoption["authority"]["authority_content_hash"],
            },
        ],
        key=lambda item: (item["kind"], item["ref_id"], item["sha256"]),
    )
    root_material = {
        "schema_id": "GT34_OBL054_ACCEPTED_OBL053_OWNER_ROOT@1.0.0",
        "adoption_artifact_blob": independent_adoption_blob,
        "semantic_owner_authority": {
            "id": adoption["authority"]["authority_id"],
            "version": adoption["authority"]["authority_version"],
            "content_hash": adoption["authority"]["authority_content_hash"],
        },
        "generation_seed_hash": adoption["admitted_generation_seed_hash"],
        "semantic_object_ref": {
            "kind": "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_SEMANTIC_OBJECT",
            "ref_id": adoption["semantic_object"]["object_id"],
            "sha256": adoption["semantic_object"]["object_content_hash"],
        },
        "objective_evidence_receipt_hash": (
            adoption["generated_fact_provenance_integrity_receipt_hash"]
        ),
        "evidence_refs": [evidence_ref],
        "provenance_refs": provenance_refs,
        "currentness_state": "FRESHLY_HQ_ADOPTED__OBL053_CLOSED",
        "object_cardinality": 1,
    }
    root_hash = _hash_domain(ACCEPTED_ROOT_DOMAIN, root_material)
    assert root_hash == EXPECTED_CURRENT_ROOT_HASH
    assert root_hash == u2.CURRENT_ACCEPTED_OWNER_ROOT_HASH

    permit_material = {
        "schema_id": "GT34_OBL054_ONE_OBJECT_MATERIALIZATION_PERMIT@1.0.0",
        "accepted_owner_root": root_material,
        "accepted_owner_root_hash": root_hash,
        "scope": "EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY",
        "object_cardinality": 1,
    }
    permit_hash = _hash_domain(PERMIT_DOMAIN, permit_material)
    assert permit_hash == EXPECTED_CURRENT_PERMIT_HASH
    assert permit_hash == u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT.permit_hash
    assert (
        u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT.permit_id
        == "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:"
        + permit_hash
    )


def test_self_consistent_hostile_owner_binding_is_not_authentication() -> None:
    hostile = _hostile_material()
    # Independently verify the attacker really has a self-consistent checksum.
    expected = _hash_domain(
        OWNER_BINDING_DOMAIN,
        hostile.owner_binding_material(),
    )
    assert hostile.owner_binding_content_hash == expected

    with pytest.raises(u2.AcceptedOwnerAuthenticationError):
        u2.materialize_owner_bound_subject(
            hostile,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_structurally_valid_hostile_root_and_permit_are_noncurrent() -> None:
    hostile = _hostile_material()
    root = u2.AcceptedOwnerRoot(
        adoption_artifact_blob=hashlib.sha1(b"u3-hostile-adoption").hexdigest(),
        semantic_owner_authority_id=hostile.semantic_owner_authority_id,
        semantic_owner_authority_version=hostile.semantic_owner_authority_version,
        semantic_owner_authority_hash=hostile.semantic_owner_authority_hash,
        generation_seed_hash=_sha256(b"u3-hostile-seed"),
        semantic_object_ref=hostile.semantic_object_ref,
        objective_evidence_receipt_hash=_sha256(b"u3-hostile-receipt"),
        evidence_refs=hostile.evidence_refs,
        provenance_refs=hostile.provenance_refs,
        currentness_state="HOSTILE_SELF_ASSERTED_CURRENT",
        object_cardinality=1,
    )
    forged = _manual_permit(root)
    assert forged.validated_structurally() is forged
    with pytest.raises(u2.MaterializationPermitError, match="current accepted OBL053 root"):
        forged.validated_for_current_root()
    with pytest.raises(u2.MaterializationPermitError):
        u2.materialize_owner_bound_subject(hostile, forged)


@pytest.mark.parametrize(
    "root",
    [
        replace(
            u2.CURRENT_ACCEPTED_OWNER_ROOT,
            adoption_artifact_blob=HISTORICAL_ADOPTION_BLOB,
        ),
        replace(
            u2.CURRENT_ACCEPTED_OWNER_ROOT,
            semantic_owner_authority_hash=HISTORICAL_AUTHORITY_HASH,
        ),
        replace(
            u2.CURRENT_ACCEPTED_OWNER_ROOT,
            semantic_object_ref=replace(
                u2.CURRENT_ACCEPTED_OWNER_ROOT.semantic_object_ref,
                ref_id=(
                    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:"
                    "sha256:" + HISTORICAL_OBJECT_HASH
                ),
                sha256=HISTORICAL_OBJECT_HASH,
            ),
        ),
        replace(
            u2.CURRENT_ACCEPTED_OWNER_ROOT,
            objective_evidence_receipt_hash=HISTORICAL_RECEIPT_HASH,
        ),
    ],
)
def test_historical_root_or_identity_reversions_are_rejected(root) -> None:
    permit = _manual_permit(root)
    assert permit.validated_structurally() is permit
    with pytest.raises(u2.MaterializationPermitError):
        permit.validated_for_current_root()


@pytest.mark.parametrize(
    "permit",
    [
        replace(
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
            permit_hash="0" * 64,
        ),
        replace(
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
            permit_id="urn:hostile:wrong-permit-id",
        ),
        replace(
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
            accepted_owner_root_hash="0" * 64,
        ),
    ],
)
def test_permit_identity_or_root_hash_tampering_fails(permit) -> None:
    with pytest.raises(u2.MaterializationPermitError):
        permit.validated_structurally()


def test_direct_materialization_without_permit_is_impossible() -> None:
    hostile = _hostile_material()
    with pytest.raises(TypeError):
        u2.materialize_owner_bound_subject(hostile)  # type: ignore[call-arg]
    with pytest.raises(u2.MaterializationPermitError):
        u2.materialize_owner_bound_subject(hostile, None)  # type: ignore[arg-type]


def test_exact_current_permit_cannot_authorize_a_second_object() -> None:
    hostile = _hostile_material("SECOND")
    material = replace(
        hostile,
        semantic_owner_authority_id=u2.OBL053_AUTHORITY_ID,
        semantic_owner_authority_version=u2.OBL053_AUTHORITY_VERSION,
        semantic_owner_authority_hash=u2.OBL053_AUTHORITY_HASH,
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="semantic object ref"):
        u2.materialize_owner_bound_subject(
            material,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_registry_reinstantiation_does_not_create_cardinality_authority() -> None:
    hostile = _hostile_material("REGISTRY")
    permit = u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT
    registries = (
        u2.OneObjectSubjectRegistry(permit),
        u2.OneObjectSubjectRegistry(permit),
        u2.OneObjectSubjectRegistry(permit),
    )
    for registry in registries:
        with pytest.raises(u2.AcceptedOwnerAuthenticationError):
            registry.materialize(hostile)
        assert registry.receipt is None


def test_evidence_and_provenance_mutation_fail_before_receipt_emission() -> None:
    root = u2.CURRENT_ACCEPTED_OWNER_ROOT
    bad_evidence = replace(
        root.evidence_refs[0],
        ref_id="urn:hostile:u3:mutated-evidence",
    )
    material = u2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=root.semantic_owner_authority_id,
        semantic_owner_authority_version=root.semantic_owner_authority_version,
        semantic_owner_authority_hash=root.semantic_owner_authority_hash,
        semantic_object_ref=root.semantic_object_ref,
        semantic_object_bytes=b"not-consumed-before-lineage-failure",
        evidence_refs=(bad_evidence,),
        provenance_refs=root.provenance_refs,
        owner_binding_content_hash="0" * 64,
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="evidence lineage"):
        u2.materialize_owner_bound_subject(
            material,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )

    bad_prov = replace(
        root.provenance_refs[0],
        ref_id="urn:hostile:u3:mutated-provenance",
    )
    material = replace(
        material,
        evidence_refs=root.evidence_refs,
        provenance_refs=(bad_prov, root.provenance_refs[1]),
    )
    with pytest.raises(u2.AcceptedOwnerAuthenticationError, match="provenance lineage"):
        u2.materialize_owner_bound_subject(
            material,
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_historical_s2_bypass_remains_historical_and_is_not_u2_surface() -> None:
    hostile = _hostile_material("OLD")
    old_material = historical_s2.OwnerBoundSubjectInput(
        semantic_owner_authority_id=hostile.semantic_owner_authority_id,
        semantic_owner_authority_version=hostile.semantic_owner_authority_version,
        semantic_owner_authority_hash=hostile.semantic_owner_authority_hash,
        semantic_object_ref=historical_s2.ExactImmutableRef(
            hostile.semantic_object_ref.kind,
            hostile.semantic_object_ref.ref_id,
            hostile.semantic_object_ref.sha256,
        ),
        semantic_object_bytes=hostile.semantic_object_bytes,
        evidence_refs=tuple(
            historical_s2.ExactImmutableRef(ref.kind, ref.ref_id, ref.sha256)
            for ref in hostile.evidence_refs
        ),
        provenance_refs=tuple(
            historical_s2.ExactImmutableRef(ref.kind, ref.ref_id, ref.sha256)
            for ref in hostile.provenance_refs
        ),
        owner_binding_content_hash=hostile.owner_binding_content_hash,
    )
    old_receipt = historical_s2.materialize_owner_bound_subject(old_material)
    assert old_receipt.materializer_id == historical_s2.MATERIALIZER_ID
    assert old_receipt.materializer_id != u2.MATERIALIZER_ID
    assert historical_s2.MATERIALIZER_ID not in " ".join(u2.__all__)
    assert (
        "gt34_s2_v3p1_subject_registry_materializer"
        not in U2_MODULE.read_text(encoding="utf-8")
    )


def test_private_shadow_path_cannot_accept_current_root() -> None:
    with pytest.raises(u2.MaterializationPermitError, match="NONCURRENT_SYNTHETIC_TEST_ONLY"):
        # Material is irrelevant: currentness is rejected before core execution.
        u2._materialize_noncurrent_shadow_fixture(
            _hostile_material("SHADOW-CURRENT"),
            u2.CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT,
        )


def test_private_shadow_output_cannot_masquerade_as_production_receipt() -> None:
    _, permit, material = _shadow_fixture()
    shadow = u2._materialize_noncurrent_shadow_fixture(material, permit)
    wire = shadow.as_dict()

    assert "_materialize_noncurrent_shadow_fixture" not in u2.__all__
    assert "_build_permit" not in u2.__all__
    assert not isinstance(shadow, u2.SubjectMaterializationReceipt)
    assert wire["schema_id"] == "NONCURRENT_SYNTHETIC_SHADOW_RECEIPT@1.0.0"
    assert wire["integrity_state"] == "NONCURRENT_SYNTHETIC_TEST_ONLY"
    assert "materializer_id" not in wire
    assert u2.MATERIALIZER_ID not in json.dumps(wire, sort_keys=True)


def test_production_receipt_contract_binds_adoption_root_and_permit() -> None:
    names = {field.name for field in fields(u2.SubjectMaterializationReceipt)}
    assert {
        "adoption_artifact_blob",
        "accepted_owner_root_hash",
        "materialization_permit_id",
        "materialization_permit_hash",
        "semantic_owner_authority_hash",
        "semantic_object_ref",
        "evidence_refs",
        "provenance_refs",
        "semantic_owner_transfer",
        "semantic_fields_interpreted",
    } <= names

    source = inspect.getsource(u2._build_production_receipt)
    for exact_binding in (
        "root.adoption_artifact_blob",
        "permit.accepted_owner_root_hash",
        "permit.permit_id",
        "permit.permit_hash",
        "semantic_owner_authority_id=root.semantic_owner_authority_id",
        "semantic_owner_authority_version=root.semantic_owner_authority_version",
        "semantic_owner_authority_hash=root.semantic_owner_authority_hash",
        "semantic_owner_transfer=False",
        "semantic_fields_interpreted=False",
    ):
        assert exact_binding in source


def test_public_production_path_does_not_parse_semantic_object_bytes() -> None:
    source = "\n".join(
        [
            inspect.getsource(u2.materialize_owner_bound_subject),
            inspect.getsource(u2._materialization_core),
            inspect.getsource(u2._validate_material_against_root),
            inspect.getsource(u2.OwnerBoundSubjectInput.owner_binding_material),
        ]
    ).lower()
    assert "json.loads" not in source
    assert ".decode(" not in source
    for semantic_field in (
        "entity_family",
        "facility_domain",
        "facility_form",
        "facility_function",
        "ownership_status",
        "q69b",
        "actor_id",
    ):
        assert semantic_field not in source


def test_public_contract_adds_no_downstream_semantic_authority() -> None:
    public = " ".join(u2.__all__).lower()
    for forbidden in (
        "classifier",
        "actor",
        "encounter",
        "comparator",
        "psepf",
        "metabolism",
        "can008",
        "can_008",
        "positive_v3",
        "actor_effect",
        "v2_authority",
    ):
        assert forbidden not in public
    assert u2.MATERIALIZER_VERSION == "2.0.0"


def test_u2_u3_artifacts_persist_no_concrete_real_subject_ref() -> None:
    corpus = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (U2_MODULE, U2_TEST, U2_RETURN, U2_EVIDENCE, U3_TEST, COURT_SPEC)
    )
    assert REAL_SUBJECT_PATTERN.search(corpus) is None

    evidence = json.loads(U2_EVIDENCE.read_text(encoding="utf-8"))
    assert (
        evidence["test_materialization_disposition"][
            "real_first_canary_subject_ref_materialized"
        ]
        is False
    )
    assert evidence["test_materialization_disposition"]["production_receipt_emitted"] is False
