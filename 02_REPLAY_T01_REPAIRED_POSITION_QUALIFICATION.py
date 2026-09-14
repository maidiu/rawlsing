#!/usr/bin/env python3
import copy
import hashlib
import json
from pathlib import Path

ARTIFACT = Path(__file__).with_name("01_REPAIRED_Q03_POSITION_HOSTILE_QUALIFICATION_R1.json")
EXPECTED_HASH = "60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505"
EXPECTED_ID = (
    "urn:rawlsing:prev3:objective-position-admission-candidate:sha256:"
    + EXPECTED_HASH
)
OCCUPANT = "EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY"
EXPECTED_REQUIREMENTS = [
    "PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION",
    "ACTIVE_WAGE_LABOUR_SALE_RELATION",
    "EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY",
    "EXACT_INSTITUTIONAL_RULE_CONTEXT",
]

def canonical_bytes(material):
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

def digest(material):
    return hashlib.sha256(canonical_bytes(material)).hexdigest()

doc = json.loads(ARTIFACT.read_text(encoding="utf-8"))
material = doc["canonical_identity_material"]
replay = doc["replay_assertions"]

assert digest(material) == EXPECTED_HASH
assert replay["expected_content_hash"] == EXPECTED_HASH
assert replay["expected_candidate_id"] == EXPECTED_ID
assert replay["expected_constitutive_requirements"] == EXPECTED_REQUIREMENTS
assert material["constitutive_requirements"] == EXPECTED_REQUIREMENTS
assert OCCUPANT not in material["constitutive_requirements"]
assert OCCUPANT not in json.dumps(material, sort_keys=True)

matrix = doc["qualification_matrix"]
for gate in (
    "actor_independent_semantic_identity",
    "objective_world_and_no_person_state_leakage",
    "source_claim_provenance_closure",
    "distinctness_from_q73a_prev3pos",
    "constitutive_closure_no_hidden_inference",
    "negative_ceilings",
    "deterministic_replay_and_change_sensitivity",
    "later_actor_fact_materializer_suitability",
):
    assert matrix[gate]["decision"] == "PASS"

assert matrix["source_claim_provenance_closure"]["source_worker_tip"] == (
    "0ebca9ff111bea63838f9b68c8e5c3cb93d9d128"
)
assert matrix["source_claim_provenance_closure"]["source_ledger_blob"] == (
    "606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7"
)
assert matrix["distinctness_from_q73a_prev3pos"]["baseline_variable"] == "Q73A"
assert matrix["distinctness_from_q73a_prev3pos"]["baseline_owner"] == (
    "ACTIVE_POSITION__FISCAL_INCORPORATION_OR_OBLIGATION_POSITION"
)

# Semantic change sensitivity: changing any governed semantic/provenance/authority/
# distinctness/use-ceiling coordinate must create a different identity.
mutations = []
m = copy.deepcopy(material); m["canonical_name"] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["definition"] += " MUTATED"; mutations.append(m)
for idx in range(len(EXPECTED_REQUIREMENTS)):
    m = copy.deepcopy(material)
    m["constitutive_requirements"][idx] += "_MUTATED"
    mutations.append(m)
m = copy.deepcopy(material); m["source_worker_tip"] = "1" * 40; mutations.append(m)
m = copy.deepcopy(material); m["source_ledger_blob"] = "2" * 40; mutations.append(m)
m = copy.deepcopy(material); m["documentary_loci"][0] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["semantic_owner_authority"] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["commission_tip"] = "3" * 40; mutations.append(m)
m = copy.deepcopy(material); m["hq_authority"] = "4" * 40; mutations.append(m)
m = copy.deepcopy(material); m["baseline_distinct_from"]["fact"] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["baseline_distinct_from"]["owner"] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["baseline_distinct_from"]["variable"] += "_MUTATED"; mutations.append(m)
m = copy.deepcopy(material); m["use_ceiling"][0] += "_MUTATED"; mutations.append(m)

for mutated in mutations:
    assert digest(mutated) != EXPECTED_HASH

# Occupant independence: occupant values live outside semantic canonical material.
external_fact_a = {"occupant": "ACTOR_A", "position_semantic": EXPECTED_ID}
external_fact_b = {"occupant": "ACTOR_B", "position_semantic": EXPECTED_ID}
assert external_fact_a["occupant"] != external_fact_b["occupant"]
assert digest(material) == EXPECTED_HASH
assert external_fact_a["position_semantic"] == external_fact_b["position_semantic"]

bounds = doc["boundary_preservation"]
for key in (
    "actor_indexed_prev3pos_fact_emitted",
    "real_actor_or_entity_materialized",
    "mechanism_channel_or_topology_created",
    "v555_or_m2_used",
    "v3_or_person_state_used",
    "obl063_semantics_used",
    "t02_provisional_output_consumed",
    "t03_provisional_output_consumed",
    "library_used",
    "main_mutated",
    "pre_main_mutated",
):
    assert bounds[key] is False

assert doc["successor_gate"]["direct_actor_fact_materialization_authorized"] is False
assert doc["successor_gate"]["decision"] == (
    "WAKE_SEPARATE_MATERIALIZATION_SOURCE_APPLICABILITY_LANE_ONLY"
)

print(
    "PASS",
    doc["terminal"],
    EXPECTED_HASH,
    EXPECTED_ID,
    f"change_sensitivity_mutations={len(mutations)}",
)
