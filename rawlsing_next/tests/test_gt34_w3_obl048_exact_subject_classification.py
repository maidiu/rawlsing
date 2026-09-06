from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
W3 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_W1_W2_PARALLEL_AUTHORITY_AUDIT_WAVE_R1/W3_OBL048_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_R1"
AUTHORITY = W3 / "01_EXACT_SUBJECT_CLASSIFICATION_AUTHORITY_CANDIDATE.json"
PROPOSITION = W3 / "02_EXACT_SUBJECT_CLASSIFICATION_PROPOSITION_CANDIDATE.json"
W1 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_POST_OBL054_PARALLEL_EXECUTION_WAVE_R1/W1_OBL052_FIRST_CANARY_SUBJECT_MATERIALIZATION_R1/01_CURRENT_FIRST_CANARY_MATERIALIZATION.json"
OBL053 = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/01_REPAIRED_HASH_GRAPH_CANDIDATE.json"

SUBJECT_REF = "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
SUBJECT_HASH = "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
W1_RECEIPT_ID = "urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f"
W1_RECEIPT_HASH = "e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f"
OBJECT_ID = "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
OBJECT_HASH = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
OWNER_ID = "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY"
OWNER_VERSION = "1.0.0"
OWNER_HASH = "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
EVIDENCE_ID = "urn:rawlsing:gt34:obl053:objective-evidence-receipt:sha256:153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"
EVIDENCE_HASH = "153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"
Q1_ID = "GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT"
Q1_VERSION = "1.1.0"
Q1_HASH = "219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca"
AUTHORITY_ID = "GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_AUTHORITY"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_HASH = "a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794"
PROPOSITION_HASH = "90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11"
PROPOSITION_ID = "urn:rawlsing:gt34:obl048:exact-first-canary-subject-classification-proposition:sha256:90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11"

EXPECTED_FACTS = {
    "entity_family": "NONACTOR_FACILITY",
    "facility_domain": "HEALTHCARE_DELIVERY",
    "facility_form": "CLINIC",
    "facility_function": "OUTPATIENT_HEALTHCARE_SERVICE_DELIVERY",
    "ownership_status": "PUBLIC_SECTOR",
}
AUTHORITY_KEYS = {
    "schema", "authority_id", "authority_version", "jurisdiction",
    "positive_rule", "required_bindings", "authority_ceiling",
    "currentness", "content_addressing_law"
}
PROPOSITION_KEYS = {
    "schema", "subject_ref", "subject_ref_hash", "proposition",
    "classification_result", "classification_basis",
    "classification_authority", "authenticated_bindings",
    "provenance_currentness", "does_not_assert", "content_addressing_law"
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _validate_authority(artifact: dict) -> dict:
    projection = artifact["semantic_projection"]
    assert set(projection) == AUTHORITY_KEYS
    assert artifact["status"].startswith("CANDIDATE_NOT_ADOPTED")
    assert _hash(projection) == artifact["authority_content_hash"] == AUTHORITY_HASH
    assert projection["authority_id"] == AUTHORITY_ID
    assert projection["authority_version"] == AUTHORITY_VERSION
    assert projection["jurisdiction"] == {
        "subject_cardinality": 1,
        "exact_subject_ref": SUBJECT_REF,
        "exact_subject_ref_hash": SUBJECT_HASH,
        "exact_proposition": "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
        "second_subject": "FORBIDDEN",
        "general_facility_ontology": "FORBIDDEN",
    }
    rule = projection["positive_rule"]
    assert rule["all_exact_current_bindings_required"] is True
    assert rule["required_objective_facts"] == {
        "entity_family": "NONACTOR_FACILITY",
        "facility_domain": "HEALTHCARE_DELIVERY",
        "facility_form_allowed": ["CLINIC", "HOSPITAL"],
        "ownership_status": "PUBLIC_SECTOR",
    }
    assert rule["lexical_or_category_inference"] == "FORBIDDEN"
    assert projection["currentness"] == {
        "state": "CANDIDATE_NOT_ADOPTED",
        "requires_hq_adoption": True,
    }
    return projection


def _validate_proposition_semantics(projection: dict, authority: dict) -> dict:
    assert set(projection) == PROPOSITION_KEYS
    assert projection["subject_ref"] == SUBJECT_REF
    assert projection["subject_ref_hash"] == SUBJECT_HASH
    assert projection["proposition"] == "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
    assert projection["classification_result"] is True
    assert projection["classification_authority"] == {
        "id": AUTHORITY_ID,
        "version": AUTHORITY_VERSION,
        "sha256": AUTHORITY_HASH,
    }
    assert set(projection["classification_basis"]) == {
        "objective_entity_facts", "rule_satisfaction"
    }
    assert projection["classification_basis"]["objective_entity_facts"] == EXPECTED_FACTS
    satisfaction = projection["classification_basis"]["rule_satisfaction"]
    required = authority["positive_rule"]["required_objective_facts"]
    assert satisfaction["entity_family"] == required["entity_family"]
    assert satisfaction["facility_domain"] == required["facility_domain"]
    assert satisfaction["facility_form"] in required["facility_form_allowed"]
    assert satisfaction["ownership_status"] == required["ownership_status"]
    assert projection["authenticated_bindings"] == authority["required_bindings"]
    return projection


def _validate_proposition(artifact: dict, authority: dict) -> dict:
    projection = artifact["semantic_projection"]
    assert artifact["status"].startswith("CANDIDATE_NOT_ADOPTED")
    assert _hash(projection) == artifact["proposition_content_hash"] == PROPOSITION_HASH
    assert artifact["proposition_id"] == PROPOSITION_ID
    return _validate_proposition_semantics(projection, authority)


def _artifacts() -> tuple[dict, dict, dict, dict]:
    return _load(AUTHORITY), _load(PROPOSITION), _load(W1), _load(OBL053)


def test_exact_current_chain_yields_positive_proposition() -> None:
    authority_artifact, proposition_artifact, w1, obl053 = _artifacts()
    authority = _validate_authority(authority_artifact)
    proposition = _validate_proposition(proposition_artifact, authority)
    assert w1["subject_ref"] == SUBJECT_REF
    assert w1["subject_ref_hash"] == SUBJECT_HASH
    assert w1["production_receipt_id"] == W1_RECEIPT_ID
    assert w1["production_receipt_hash"] == W1_RECEIPT_HASH
    assert w1["source_semantic_object"]["semantic_object_id"] == OBJECT_ID
    assert w1["source_semantic_object"]["semantic_object_hash"] == OBJECT_HASH
    assert w1["semantic_owner"] == {"id": OWNER_ID, "version": OWNER_VERSION, "content_hash": OWNER_HASH}
    source_object = obl053["prospective_semantic_object"]
    assert source_object["semantic_object_id"] == OBJECT_ID
    assert source_object["semantic_object_content_hash"] == OBJECT_HASH
    assert source_object["semantic_projection"]["objective_entity_facts"] == EXPECTED_FACTS
    evidence = obl053["objective_evidence_receipt"]
    assert evidence["receipt_content_hash"] == EVIDENCE_HASH
    sufficiency = evidence["semantic_projection"]["evidence_sufficiency_ceiling"]
    assert sufficiency["does_not_itself_assert"] == "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
    assert sufficiency["later_classifier_must_bind_exact_object_hash_and_authority_hash"] is True
    assert proposition["classification_result"] is True


def test_authority_and_proposition_hashes_recompute_independently() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    assert _hash(authority_artifact["semantic_projection"]) == AUTHORITY_HASH
    assert _hash(proposition_artifact["semantic_projection"]) == PROPOSITION_HASH
    assert proposition_artifact["proposition_id"].endswith(PROPOSITION_HASH)


def test_subject_ref_mutation_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["subject_ref"] = "urn:rawlsing:v3:subject:sha256:" + "0" * 64
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_materialization_receipt_mutation_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["authenticated_bindings"]["w1_materialization_receipt"]["sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


@pytest.mark.parametrize("binding", ["semantic_object", "semantic_owner_authority", "objective_evidence_receipt"])
def test_object_owner_or_evidence_mutation_fails(binding: str) -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["authenticated_bindings"][binding]["sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_non_clinic_hospital_form_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["classification_basis"]["objective_entity_facts"]["facility_form"] = "PHARMACY"
    bad["classification_basis"]["rule_satisfaction"]["facility_form"] = "PHARMACY"
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_non_public_ownership_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["classification_basis"]["objective_entity_facts"]["ownership_status"] = "PRIVATE_SECTOR"
    bad["classification_basis"]["rule_satisfaction"]["ownership_status"] = "PRIVATE_SECTOR"
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_lexical_clinic_label_without_objective_evidence_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["classification_basis"] = {"display_name": "Central Public Clinic", "rule_satisfaction": {}}
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_second_subject_fails() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["subject_ref"] = "urn:rawlsing:v3:subject:sha256:" + "1" * 64
    bad["subject_ref_hash"] = "1" * 64
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_contact_use_encounter_fields_absent_and_rejected_from_identity() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    proposition_projection = _validate_proposition(proposition_artifact, authority)
    forbidden_keys = {"actor_id", "contact", "contact_ref", "use", "encounter", "encounter_ref", "exposure", "comparator", "psepf", "metabolism", "can_008", "v2", "positive_v3"}
    assert forbidden_keys.isdisjoint(proposition_projection.keys())
    bad = deepcopy(proposition_artifact["semantic_projection"])
    bad["encounter_ref"] = "urn:forbidden:encounter"
    with pytest.raises(AssertionError):
        _validate_proposition_semantics(bad, authority)


def test_q1_requirement_hash_is_bound() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    proposition_projection = _validate_proposition(proposition_artifact, authority)
    expected = {"id": Q1_ID, "version": Q1_VERSION, "sha256": Q1_HASH}
    assert authority["required_bindings"]["q1_subject_requirement"] == expected
    assert proposition_projection["authenticated_bindings"]["q1_subject_requirement"] == expected


def test_replay_is_exact_and_idempotent() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority1 = _validate_authority(deepcopy(authority_artifact))
    proposition1 = _validate_proposition(deepcopy(proposition_artifact), authority1)
    authority2 = _validate_authority(deepcopy(authority_artifact))
    proposition2 = _validate_proposition(deepcopy(proposition_artifact), authority2)
    assert _canonical_json(authority1) == _canonical_json(authority2)
    assert _canonical_json(proposition1) == _canonical_json(proposition2)
    assert _hash(authority1) == AUTHORITY_HASH
    assert _hash(proposition1) == PROPOSITION_HASH


def test_no_broader_authority_is_emitted() -> None:
    authority_artifact, proposition_artifact, _, _ = _artifacts()
    authority = _validate_authority(authority_artifact)
    proposition_projection = _validate_proposition(proposition_artifact, authority)
    assert authority["jurisdiction"]["subject_cardinality"] == 1
    assert authority["jurisdiction"]["general_facility_ontology"] == "FORBIDDEN"
    assert authority["jurisdiction"]["exact_proposition"] == "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
    assert proposition_projection["proposition"] == "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
    assert proposition_projection["does_not_assert"] == [
        "ACTOR_CONTACTED_SUBJECT", "ACTOR_USED_SUBJECT", "ACTOR_ENCOUNTERED_SUBJECT",
        "ACTOR_EXPOSED_TO_SUBJECT", "MEDICINE_OR_SUPPLIES_PROBLEM",
        "ACTOR_AWARENESS_BELIEF_MEMORY_RESPONSE", "Q69B_RESPONSE_OR_HISTORY",
        "COMPARATOR_RESULT", "PSEPF", "METABOLISM", "CAN_008", "V2",
        "POSITIVE_V3_ACTOR_MUTATION"
    ]
