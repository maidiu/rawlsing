from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
W3 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_W1_W2_PARALLEL_AUTHORITY_AUDIT_WAVE_R1/W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_R1"
REVIEW = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/GT34_OBL048_INDEPENDENT_HOSTILE_REVIEW_R1"
AUTHORITY = W3 / "01_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE.json"
PROPOSITION = W3 / "02_EXACT_SUBJECT_CLASSIFICATION_PROPOSITION_CANDIDATE.json"
W1 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_OBL054_PARALLEL_EXECUTION_WAVE_R1/W1_OBL052_FIRST_CANARY_SUBJECT_MATERIALIZATION_R1/01_CURRENT_FIRST_CANARY_MATERIALIZATION.json"
OBL053 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/01_REPAIRED_HASH_GRAPH_CANDIDATE.json"
MATRIX = REVIEW / "01_INDEPENDENT_ATTACK_MATRIX.json"
RED_COMPAT = REVIEW / "02_W3_RED_COURT_COMPATIBILITY.json"

SUBJECT_HASH = "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
SUBJECT_REF = "urn:rawlsing:v3:subject:sha256:" + SUBJECT_HASH
W1_RECEIPT_HASH = "e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f"
W1_RECEIPT_ID = "urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:" + W1_RECEIPT_HASH
OBJECT_HASH = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
OBJECT_ID = "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:" + OBJECT_HASH
OWNER_ID = "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY"
OWNER_VERSION = "1.0.0"
OWNER_HASH = "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
EVIDENCE_HASH = "153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"
EVIDENCE_ID = "urn:rawlsing:gt34:obl053:objective-evidence-receipt:sha256:" + EVIDENCE_HASH
Q1_ID = "GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT"
Q1_VERSION = "1.1.0"
Q1_HASH = "219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca"
AUTHORITY_ID = "GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_AUTHORITY"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_HASH = "a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794"
PROPOSITION_TEXT = "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
PROPOSITION_HASH = "90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11"
PROPOSITION_ID = "urn:rawlsing:gt34:obl048:exact-first-canary-subject-classification-proposition:sha256:" + PROPOSITION_HASH

EXPECTED_FACTS = {
    "entity_family": "NONACTOR_FACILITY",
    "facility_domain": "HEALTHCARE_DELIVERY",
    "facility_form": "CLINIC",
    "facility_function": "OUTPATIENT_HEALTHCARE_SERVICE_DELIVERY",
    "ownership_status": "PUBLIC_SECTOR",
}
EXPECTED_BINDINGS = {
    "w1_materialization_receipt": {"id": W1_RECEIPT_ID, "sha256": W1_RECEIPT_HASH},
    "semantic_object": {"id": OBJECT_ID, "sha256": OBJECT_HASH},
    "semantic_owner_authority": {"id": OWNER_ID, "version": OWNER_VERSION, "sha256": OWNER_HASH},
    "objective_evidence_receipt": {"id": EVIDENCE_ID, "sha256": EVIDENCE_HASH},
    "q1_subject_requirement": {"id": Q1_ID, "version": Q1_VERSION, "sha256": Q1_HASH},
}
CONTENT_LAW = {
    "algorithm": "SHA-256",
    "encoding": "UTF-8",
    "canonical_json": {
        "mapping_key_order": "LEXICOGRAPHIC_ASCENDING",
        "separators": "COMPACT_COMMA_COLON",
        "unicode": "PRESERVE_UNICODE_NO_ASCII_ESCAPE",
        "ordered_sequences": "PRESERVE_EXACT_ORDER",
    },
    "derived_hash_field_rule": "EXCLUDE_ONLY_THE_OBJECTS_OWN_DERIVED_HASH_AND_CONTENT_ADDRESSED_ID_FROM_ITS_SEMANTIC_PROJECTION",
}
AUTHORITY_CEILING = [
    "EXACT_ONE_CURRENT_SUBJECT_CLASSIFICATION_ONLY",
    "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL_ONLY",
    "NO_ACTOR_CONTACT_USE_ENCOUNTER_EXPOSURE",
    "NO_MEDICINE_SUPPLIES_Q69B_RESPONSE_HISTORY",
    "NO_AWARENESS_BELIEF_MEMORY_RESPONSE",
    "NO_COMPARATOR_PSEPF_METABOLISM_CAN008_V2_POSITIVE_V3",
    "NO_SECOND_SUBJECT_CLASSIFICATION",
    "NO_GENERAL_FACILITY_ONTOLOGY",
]
DOES_NOT_ASSERT = [
    "ACTOR_CONTACTED_SUBJECT",
    "ACTOR_USED_SUBJECT",
    "ACTOR_ENCOUNTERED_SUBJECT",
    "ACTOR_EXPOSED_TO_SUBJECT",
    "MEDICINE_OR_SUPPLIES_PROBLEM",
    "ACTOR_AWARENESS_BELIEF_MEMORY_RESPONSE",
    "Q69B_RESPONSE_OR_HISTORY",
    "COMPARATOR_RESULT",
    "PSEPF",
    "METABOLISM",
    "CAN_008",
    "V2",
    "POSITIVE_V3_ACTOR_MUTATION",
]
PROVENANCE_CURRENTNESS = {
    "subject_materialization_state": "CURRENT_PRODUCTION_MATERIALIZATION_EXECUTED_UNDER_ADOPTED_OBL054",
    "objective_fact_source": "ADOPTED_OBL053_EXACT_OBJECTIVE_EVIDENCE",
    "classification_authority_state": "CANDIDATE_NOT_ADOPTED",
    "proof_scope": "EXACT_FIRST_CANARY_SUBJECT_ONLY",
}
AUTHORITY_PROJECTION_KEYS = {
    "schema", "authority_id", "authority_version", "jurisdiction", "positive_rule",
    "required_bindings", "authority_ceiling", "currentness", "content_addressing_law",
}
PROPOSITION_PROJECTION_KEYS = {
    "schema", "subject_ref", "subject_ref_hash", "proposition", "classification_result",
    "classification_basis", "classification_authority", "authenticated_bindings",
    "provenance_currentness", "does_not_assert", "content_addressing_law",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _validate_authority(artifact: dict) -> dict:
    assert set(artifact) == {"artifact_schema", "status", "authority_content_hash", "semantic_projection"}
    assert artifact["artifact_schema"] == "GT34_W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE@1.0.0"
    assert artifact["status"] == "CANDIDATE_NOT_ADOPTED__INDEPENDENT_HOSTILE_REVIEW_REQUIRED"
    projection = artifact["semantic_projection"]
    assert set(projection) == AUTHORITY_PROJECTION_KEYS
    assert _digest(projection) == artifact["authority_content_hash"] == AUTHORITY_HASH
    assert projection["schema"] == "GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_AUTHORITY@1.0.0"
    assert projection["authority_id"] == AUTHORITY_ID
    assert projection["authority_version"] == AUTHORITY_VERSION
    assert projection["jurisdiction"] == {
        "subject_cardinality": 1,
        "exact_subject_ref": SUBJECT_REF,
        "exact_subject_ref_hash": SUBJECT_HASH,
        "exact_proposition": PROPOSITION_TEXT,
        "second_subject": "FORBIDDEN",
        "general_facility_ontology": "FORBIDDEN",
    }
    assert projection["positive_rule"] == {
        "all_exact_current_bindings_required": True,
        "required_objective_facts": {
            "entity_family": "NONACTOR_FACILITY",
            "facility_domain": "HEALTHCARE_DELIVERY",
            "facility_form_allowed": ["CLINIC", "HOSPITAL"],
            "ownership_status": "PUBLIC_SECTOR",
        },
        "current_object_satisfaction": {
            "facility_form": "CLINIC",
            "ownership_status": "PUBLIC_SECTOR",
            "classification_result": True,
        },
        "lexical_or_category_inference": "FORBIDDEN",
    }
    assert projection["required_bindings"] == EXPECTED_BINDINGS
    assert projection["authority_ceiling"] == AUTHORITY_CEILING
    assert projection["currentness"] == {"state": "CANDIDATE_NOT_ADOPTED", "requires_hq_adoption": True}
    assert projection["content_addressing_law"] == CONTENT_LAW
    return projection


def _validate_proposition(artifact: dict, authority: dict) -> dict:
    assert set(artifact) == {
        "artifact_schema", "status", "proposition_id", "proposition_content_hash", "semantic_projection"
    }
    assert artifact["artifact_schema"] == "GT34_W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_PROPOSITION_CANDIDATE@1.0.0"
    assert artifact["status"] == "CANDIDATE_NOT_ADOPTED__INDEPENDENT_HOSTILE_REVIEW_REQUIRED"
    projection = artifact["semantic_projection"]
    assert set(projection) == PROPOSITION_PROJECTION_KEYS
    assert _digest(projection) == artifact["proposition_content_hash"] == PROPOSITION_HASH
    assert artifact["proposition_id"] == PROPOSITION_ID
    assert projection["schema"] == "GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_PROPOSITION@1.0.0"
    assert projection["subject_ref"] == SUBJECT_REF
    assert projection["subject_ref_hash"] == SUBJECT_HASH
    assert projection["proposition"] == PROPOSITION_TEXT
    assert projection["classification_result"] is True
    assert projection["classification_basis"] == {
        "objective_entity_facts": EXPECTED_FACTS,
        "rule_satisfaction": {
            "entity_family": "NONACTOR_FACILITY",
            "facility_domain": "HEALTHCARE_DELIVERY",
            "facility_form": "CLINIC",
            "facility_form_allowed": ["CLINIC", "HOSPITAL"],
            "ownership_status": "PUBLIC_SECTOR",
        },
    }
    assert projection["classification_authority"] == {
        "id": AUTHORITY_ID, "version": AUTHORITY_VERSION, "sha256": AUTHORITY_HASH
    }
    assert projection["authenticated_bindings"] == EXPECTED_BINDINGS == authority["required_bindings"]
    assert projection["provenance_currentness"] == PROVENANCE_CURRENTNESS
    assert projection["does_not_assert"] == DOES_NOT_ASSERT
    assert projection["content_addressing_law"] == CONTENT_LAW
    return projection


def _valid_artifacts() -> tuple[dict, dict]:
    authority_artifact = _load(AUTHORITY)
    proposition_artifact = _load(PROPOSITION)
    authority = _validate_authority(authority_artifact)
    _validate_proposition(proposition_artifact, authority)
    return authority_artifact, proposition_artifact


def _rehash_authority(artifact: dict) -> None:
    artifact["authority_content_hash"] = _digest(artifact["semantic_projection"])


def _rehash_proposition(artifact: dict) -> None:
    h = _digest(artifact["semantic_projection"])
    artifact["proposition_content_hash"] = h
    artifact["proposition_id"] = "urn:rawlsing:gt34:obl048:exact-first-canary-subject-classification-proposition:sha256:" + h


def test_matrix_frozen_before_w3_rationale_and_has_34_attacks() -> None:
    matrix = _load(MATRIX)
    assert matrix["frozen_before_w3_return_evidence_or_focused_test_rationale"] is True
    assert matrix["attack_count"] == 34 == len(matrix["attacks"])
    assert [item["id"] for item in matrix["attacks"]] == [f"A{i:02d}" for i in range(1, 35)]


def test_exact_candidate_chain_and_content_addresses_are_valid() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    assert authority_artifact["authority_content_hash"] == AUTHORITY_HASH
    assert proposition_artifact["proposition_content_hash"] == PROPOSITION_HASH


def test_exact_current_w1_and_obl053_bindings_match_candidate() -> None:
    w1 = _load(W1)
    obl053 = _load(OBL053)
    assert w1["status"] == "CURRENT_PRODUCTION_MATERIALIZATION_EXECUTED_UNDER_ADOPTED_OBL054"
    assert (w1["subject_ref"], w1["subject_ref_hash"]) == (SUBJECT_REF, SUBJECT_HASH)
    assert (w1["production_receipt_id"], w1["production_receipt_hash"]) == (W1_RECEIPT_ID, W1_RECEIPT_HASH)
    assert w1["source_semantic_object"]["semantic_object_id"] == OBJECT_ID
    assert w1["source_semantic_object"]["semantic_object_hash"] == OBJECT_HASH
    assert w1["semantic_owner"] == {"id": OWNER_ID, "version": OWNER_VERSION, "content_hash": OWNER_HASH}
    obj = obl053["prospective_semantic_object"]
    assert obj["semantic_object_id"] == OBJECT_ID
    assert obj["semantic_object_content_hash"] == OBJECT_HASH
    assert obj["semantic_projection"]["objective_entity_facts"] == EXPECTED_FACTS
    receipt = obl053["objective_evidence_receipt"]
    assert receipt["receipt_content_hash"] == EVIDENCE_HASH
    sufficiency = receipt["semantic_projection"]["evidence_sufficiency_ceiling"]
    assert sufficiency["does_not_itself_assert"] == PROPOSITION_TEXT
    assert sufficiency["later_classifier_must_bind_exact_object_hash_and_authority_hash"] is True


@pytest.mark.parametrize(("field", "value"), [
    ("subject_ref", "urn:rawlsing:v3:subject:sha256:" + "0" * 64),
    ("subject_ref_hash", "0" * 64),
])
def test_subject_ref_or_hash_mutation_rejected(field: str, value: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"][field] = value
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


@pytest.mark.parametrize(("binding", "field", "value"), [
    ("w1_materialization_receipt", "id", "urn:substitute:w1"),
    ("w1_materialization_receipt", "sha256", "0" * 64),
    ("semantic_object", "id", "urn:substitute:object"),
    ("semantic_object", "sha256", "0" * 64),
    ("semantic_owner_authority", "id", "SUBSTITUTE_OWNER"),
    ("semantic_owner_authority", "version", "9.9.9"),
    ("semantic_owner_authority", "sha256", "0" * 64),
    ("objective_evidence_receipt", "id", "urn:substitute:evidence"),
    ("objective_evidence_receipt", "sha256", "0" * 64),
    ("q1_subject_requirement", "id", "SUBSTITUTE_Q1"),
    ("q1_subject_requirement", "version", "9.9.9"),
    ("q1_subject_requirement", "sha256", "0" * 64),
])
def test_exact_binding_substitution_rejected(binding: str, field: str, value: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["authenticated_bindings"][binding][field] = value
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_objective_fact_omission_rejected_even_after_rehash() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    del bad["semantic_projection"]["classification_basis"]["objective_entity_facts"]["facility_function"]
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_objective_fact_extra_field_ambiguity_rejected_even_after_rehash() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["classification_basis"]["objective_entity_facts"]["display_name"] = "Public Clinic"
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_current_clinic_cannot_be_rewritten_as_hospital_even_though_rule_allows_hospital() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    facts = bad["semantic_projection"]["classification_basis"]["objective_entity_facts"]
    sat = bad["semantic_projection"]["classification_basis"]["rule_satisfaction"]
    facts["facility_form"] = "HOSPITAL"
    sat["facility_form"] = "HOSPITAL"
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_non_public_ownership_rejected() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["classification_basis"]["objective_entity_facts"]["ownership_status"] = "PRIVATE_SECTOR"
    bad["semantic_projection"]["classification_basis"]["rule_satisfaction"]["ownership_status"] = "PRIVATE_SECTOR"
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_lexical_label_without_authenticated_objective_evidence_rejected() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["classification_basis"] = {
        "objective_entity_facts": {"display_name": "Central Public Clinic"},
        "rule_satisfaction": {"facility_form": "CLINIC"},
    }
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_second_subject_rejected_after_full_content_address_recomputation() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["subject_ref_hash"] = "1" * 64
    bad["semantic_projection"]["subject_ref"] = "urn:rawlsing:v3:subject:sha256:" + "1" * 64
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_generic_taxonomy_widening_rejected_after_authority_rehash() -> None:
    authority_artifact, _ = _valid_artifacts()
    bad = deepcopy(authority_artifact)
    bad["semantic_projection"]["jurisdiction"]["subject_cardinality"] = "UNBOUNDED"
    bad["semantic_projection"]["jurisdiction"]["general_facility_ontology"] = "ALLOWED"
    _rehash_authority(bad)
    with pytest.raises(AssertionError):
        _validate_authority(bad)


@pytest.mark.parametrize(("field", "value"), [
    ("proposition", "SUBJECT_IS_ANY_HEALTHCARE_FACILITY"),
    ("classification_result", False),
    ("classification_result", "POSITIVE"),
])
def test_proposition_or_result_mutation_rejected(field: str, value: object) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"][field] = value
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_authority_currentness_substitution_rejected() -> None:
    authority_artifact, _ = _valid_artifacts()
    bad = deepcopy(authority_artifact)
    bad["semantic_projection"]["currentness"]["state"] = "CURRENT_ADOPTED"
    bad["semantic_projection"]["currentness"]["requires_hq_adoption"] = False
    _rehash_authority(bad)
    with pytest.raises(AssertionError):
        _validate_authority(bad)


@pytest.mark.parametrize(("field", "value"), [
    ("subject_materialization_state", "NONCURRENT_SYNTHETIC_TEST_ONLY"),
    ("objective_fact_source", "LEXICAL_LABEL"),
    ("classification_authority_state", "CURRENT_ADOPTED"),
    ("proof_scope", "GENERAL_TAXONOMY"),
])
def test_proposition_currentness_or_provenance_substitution_rejected(field: str, value: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"]["provenance_currentness"][field] = value
    _rehash_proposition(bad)
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


def test_authority_and_proposition_content_addresses_recompute_exactly() -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    assert _digest(authority_artifact["semantic_projection"]) == AUTHORITY_HASH
    assert _digest(proposition_artifact["semantic_projection"]) == PROPOSITION_HASH
    assert proposition_artifact["proposition_id"] == PROPOSITION_ID


def test_canonicalization_edge_cases_follow_declared_law() -> None:
    authority_artifact, _ = _valid_artifacts()
    projection = authority_artifact["semantic_projection"]
    reordered = {key: projection[key] for key in reversed(list(projection))}
    assert _digest(reordered) == AUTHORITY_HASH
    reversed_sequence = deepcopy(projection)
    reversed_sequence["authority_ceiling"] = list(reversed(reversed_sequence["authority_ceiling"]))
    assert _digest(reversed_sequence) != AUTHORITY_HASH
    unicode_probe = {"é": "café", "a": 1}
    raw = _canonical_json(unicode_probe)
    assert "é" in raw and "café" in raw and "\\u00e9" not in raw


@pytest.mark.parametrize(("artifact_kind", "field_name"), [
    ("authority", "authority_content_hash"),
    ("authority", "content_addressed_id"),
    ("proposition", "proposition_content_hash"),
    ("proposition", "proposition_id"),
])
def test_derived_field_self_reference_malleability_rejected(artifact_kind: str, field_name: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    if artifact_kind == "authority":
        bad = deepcopy(authority_artifact)
        bad["semantic_projection"][field_name] = "0" * 64
        _rehash_authority(bad)
        with pytest.raises(AssertionError):
            _validate_authority(bad)
    else:
        bad = deepcopy(proposition_artifact)
        bad["semantic_projection"][field_name] = "0" * 64
        _rehash_proposition(bad)
        with pytest.raises(AssertionError):
            _validate_proposition(bad, _validate_authority(authority_artifact))


@pytest.mark.parametrize("forbidden_field", [
    "actor_contact",
    "causal_use_permission",
    "actor_encounter",
    "actor_exposure",
    "q69b_response_history",
    "actor_empirical_comparator",
    "psepf",
    "metabolism",
    "can_008",
    "v2_authority",
    "positive_v3_actor_mutation",
])
def test_forbidden_semantic_insertion_changes_hash_and_is_rejected(forbidden_field: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    original_hash = proposition_artifact["proposition_content_hash"]
    bad = deepcopy(proposition_artifact)
    bad["semantic_projection"][forbidden_field] = {"claim": "FORBIDDEN_INSERTION"}
    _rehash_proposition(bad)
    assert bad["proposition_content_hash"] != original_hash
    with pytest.raises(AssertionError):
        _validate_proposition(bad, _validate_authority(authority_artifact))


@pytest.mark.parametrize(("target", "where"), [
    ("authority", "top"),
    ("authority", "projection"),
    ("authority", "positive_rule"),
    ("proposition", "top"),
    ("proposition", "projection"),
    ("proposition", "classification_basis"),
])
def test_optional_or_unknown_field_authority_ceiling_escape_rejected(target: str, where: str) -> None:
    authority_artifact, proposition_artifact = _valid_artifacts()
    if target == "authority":
        bad = deepcopy(authority_artifact)
        if where == "top":
            bad["optional_extension"] = {"authority": "widened"}
        elif where == "projection":
            bad["semantic_projection"]["optional_extension"] = {"authority": "widened"}
            _rehash_authority(bad)
        else:
            bad["semantic_projection"]["positive_rule"]["optional_extension"] = {"authority": "widened"}
            _rehash_authority(bad)
        with pytest.raises(AssertionError):
            _validate_authority(bad)
    else:
        bad = deepcopy(proposition_artifact)
        if where == "top":
            bad["optional_extension"] = {"authority": "widened"}
        elif where == "projection":
            bad["semantic_projection"]["optional_extension"] = {"authority": "widened"}
            _rehash_proposition(bad)
        else:
            bad["semantic_projection"]["classification_basis"]["optional_extension"] = {"authority": "widened"}
            _rehash_proposition(bad)
        with pytest.raises(AssertionError):
            _validate_proposition(bad, _validate_authority(authority_artifact))


def test_replay_idempotence_exact() -> None:
    a1, p1 = _valid_artifacts()
    a2, p2 = _valid_artifacts()
    assert _canonical_json(a1) == _canonical_json(a2)
    assert _canonical_json(p1) == _canonical_json(p2)
    assert _digest(a1["semantic_projection"]) == _digest(a2["semantic_projection"]) == AUTHORITY_HASH
    assert _digest(p1["semantic_projection"]) == _digest(p2["semantic_projection"]) == PROPOSITION_HASH


def test_exact_candidate_blob_compatibility_in_review_checkout() -> None:
    assert _git_blob_sha(AUTHORITY) == "a0be5530a3fab5a0b18746750ff461b0e7ff2d91"
    assert _git_blob_sha(PROPOSITION) == "c8c9ec0d708acfe864beede72c062b13b5aa0f58"


def test_w3_first_red_court_is_banked_as_harness_only_without_semantic_change() -> None:
    evidence = _load(RED_COMPAT)
    assert evidence["frozen_semantic_candidate"] == "01645806c98b8a83070389e5375e2b7fde781c6a"
    assert evidence["authority_blob"] == "a0be5530a3fab5a0b18746750ff461b0e7ff2d91"
    assert evidence["proposition_blob"] == "c8c9ec0d708acfe864beede72c062b13b5aa0f58"
    assert evidence["first_red"]["candidate_to_red_delta"] == [".rabochii/court_spec.json__ADDED_ONLY"]
    assert evidence["first_red"]["authority_or_proposition_changed"] is False
    assert evidence["first_red"]["failure_exception"] == "KeyError: 'objective_entity_facts'"
    assert evidence["first_red"]["expected_by_harness"] == "AssertionError"
    assert evidence["later_green"]["authority_or_proposition_changed"] is False
    assert evidence["independent_holding"] == "FIRST_RED_WAS_HARNESS_ONLY__NO_SEMANTIC_ARTIFACT_CHANGE"
