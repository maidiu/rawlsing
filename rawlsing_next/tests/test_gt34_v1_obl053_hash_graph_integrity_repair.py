from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL053_055_SUBJECT_PREDECESSOR_CONSTRUCTION_WAVE_R1/"
    "S1_ONE_OBJECT_SUBJECT_ENTITY_SEMANTIC_AUTHORITY_R1/"
    "01_ONE_OBJECT_SUBJECT_ENTITY_SEMANTIC_AUTHORITY_CANDIDATE.json"
)
REPAIRED = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/"
    "V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/"
    "01_REPAIRED_HASH_GRAPH_CANDIDATE.json"
)

EXPECTED_SEED = "b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53"
EXPECTED_AUTHORITY = "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
EXPECTED_OBJECT = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
EXPECTED_RECEIPT = "153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"

OLD_AUTHORITY = "e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed"
OLD_OBJECT = "d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53"
OLD_OBJECT_ID = (
    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
    + OLD_OBJECT
)
NEW_OBJECT_ID = (
    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
    + EXPECTED_OBJECT
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(projection: object) -> str:
    raw = json.dumps(
        projection,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _replace(value: object, old: str, new: str) -> object:
    if isinstance(value, list):
        return [_replace(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: _replace(item, old, new) for key, item in value.items()}
    return new if value == old else value


def test_historical_hash_failure_is_mechanically_reproducible() -> None:
    old = _load(HISTORICAL)
    assert _hash(old["generation_seed"]["semantic_projection"]) == EXPECTED_SEED
    assert _hash(old["candidate_authority"]["semantic_projection"]) != OLD_AUTHORITY
    assert _hash(old["prospective_semantic_object"]["semantic_projection"]) != OLD_OBJECT
    assert (
        _hash(old["objective_evidence_receipt"]["semantic_projection"])
        != old["objective_evidence_receipt"]["receipt_content_hash"]
    )


def test_repaired_candidate_declares_exact_mechanical_hashes() -> None:
    repaired = _load(REPAIRED)
    assert _hash(repaired["generation_seed"]["semantic_projection"]) == EXPECTED_SEED
    assert _hash(repaired["candidate_authority"]["semantic_projection"]) == EXPECTED_AUTHORITY
    assert (
        _hash(repaired["prospective_semantic_object"]["semantic_projection"])
        == EXPECTED_OBJECT
    )
    assert (
        _hash(repaired["objective_evidence_receipt"]["semantic_projection"])
        == EXPECTED_RECEIPT
    )


def test_declared_repaired_hashes_equal_recomputation() -> None:
    repaired = _load(REPAIRED)
    assert repaired["generation_seed"]["seed_content_hash"] == EXPECTED_SEED
    assert repaired["candidate_authority"]["authority_content_hash"] == EXPECTED_AUTHORITY
    assert (
        repaired["prospective_semantic_object"]["semantic_object_content_hash"]
        == EXPECTED_OBJECT
    )
    assert repaired["prospective_semantic_object"]["semantic_object_id"] == NEW_OBJECT_ID
    assert (
        repaired["objective_evidence_receipt"]["receipt_content_hash"]
        == EXPECTED_RECEIPT
    )


def test_seed_and_authority_semantic_projections_are_exactly_preserved() -> None:
    old = _load(HISTORICAL)
    repaired = _load(REPAIRED)
    assert (
        repaired["generation_seed"]["semantic_projection"]
        == old["generation_seed"]["semantic_projection"]
    )
    assert (
        repaired["candidate_authority"]["semantic_projection"]
        == old["candidate_authority"]["semantic_projection"]
    )


def test_object_projection_changed_only_by_corrected_authority_identity() -> None:
    old = _load(HISTORICAL)
    repaired = _load(REPAIRED)
    expected = _replace(
        old["prospective_semantic_object"]["semantic_projection"],
        OLD_AUTHORITY,
        EXPECTED_AUTHORITY,
    )
    assert repaired["prospective_semantic_object"]["semantic_projection"] == expected
    wire = json.dumps(expected, sort_keys=True)
    assert OLD_AUTHORITY not in wire
    assert wire.count(EXPECTED_AUTHORITY) == 2


def test_receipt_projection_changed_only_by_corrected_upstream_identities() -> None:
    old = _load(HISTORICAL)
    repaired = _load(REPAIRED)
    expected = _replace(
        old["objective_evidence_receipt"]["semantic_projection"],
        OLD_AUTHORITY,
        EXPECTED_AUTHORITY,
    )
    expected = _replace(expected, OLD_OBJECT, EXPECTED_OBJECT)
    expected = _replace(expected, OLD_OBJECT_ID, NEW_OBJECT_ID)
    assert repaired["objective_evidence_receipt"]["semantic_projection"] == expected
    wire = json.dumps(expected, sort_keys=True)
    assert OLD_AUTHORITY not in wire
    assert OLD_OBJECT not in wire
    assert OLD_OBJECT_ID not in wire


def test_objective_facts_and_semantic_ceilings_are_unchanged() -> None:
    old = _load(HISTORICAL)
    repaired = _load(REPAIRED)
    assert (
        repaired["prospective_semantic_object"]["semantic_projection"][
            "objective_entity_facts"
        ]
        == old["prospective_semantic_object"]["semantic_projection"][
            "objective_entity_facts"
        ]
    )
    assert (
        repaired["prospective_semantic_object"]["semantic_projection"]["semantic_ceiling"]
        == old["prospective_semantic_object"]["semantic_projection"]["semantic_ceiling"]
    )
    assert repaired["authority_ceiling"] == old["authority_ceiling"]


def test_repair_creates_no_second_seed_object_or_downstream_authority() -> None:
    repaired = _load(REPAIRED)
    jurisdiction = repaired["candidate_authority"]["semantic_projection"]["jurisdiction"]
    assert jurisdiction["object_cardinality"] == 1
    assert jurisdiction["additional_seed_hashes"] == "FORBIDDEN"
    assert jurisdiction["additional_objects"] == "FORBIDDEN"
    assert repaired["prospective_semantic_object"]["current_subject_ref"].startswith("NONE__")
    proof = repaired["semantic_no_change_proof"]
    assert proof["no_subject_classifier"] is True
    assert proof["no_actor_contact_use_encounter_exposure"] is True
    assert proof["no_comparator_psepf_metabolism_can008_v2_positive_v3"] is True


def test_repair_is_candidate_only_and_t1_hash_finding_is_explicitly_superseded() -> None:
    repaired = _load(REPAIRED)
    assert repaired["status"] == "CANDIDATE_NOT_ADOPTED__HASH_GRAPH_REPAIRED"
    assert (
        repaired["historical_disposition"]
        == "T1_HASH_RECOMPUTATION_FINDING_SUPERSEDED_BY_MECHANICAL_REPAIR_EVIDENCE"
    )
    assert "FRESH_HQ_ADOPTION_REQUIRED" in " ".join(repaired["required_next_steps"])
