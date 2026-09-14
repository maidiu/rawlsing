#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ARTIFACT = Path(__file__).with_name("01_REPAIRED_Q03_OBJECTIVE_POSITION_SEMANTIC_CANDIDATE.json")
OLD_HASH = "e040ae101388d0c9a87befa4fcd88ab3e861424376ad00b9e864c885d5bb12f9"
EXPECTED_SOURCE_TIP = "0ebca9ff111bea63838f9b68c8e5c3cb93d9d128"
EXPECTED_SOURCE_BLOB = "606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7"
OCCUPANT = "EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY"

doc = json.loads(ARTIFACT.read_text(encoding="utf-8"))
identity = doc["identity_replay"]
material = identity["canonical_identity_material"]
encoded = json.dumps(
    material,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")
replayed = hashlib.sha256(encoded).hexdigest()
expected_id = f"urn:rawlsing:prev3:objective-position-admission-candidate:sha256:{replayed}"

assert replayed == identity["content_hash"], (replayed, identity["content_hash"])
assert expected_id == identity["candidate_id"], (expected_id, identity["candidate_id"])
assert replayed != OLD_HASH
assert OCCUPANT not in material["constitutive_requirements"]
assert OCCUPANT not in doc["admitted_position"]["constitutive_requirements"]
assert OCCUPANT in doc["semantic_fact_split"]["forbidden_in_position_semantic_identity"]
assert OCCUPANT in doc["semantic_fact_split"]["later_actor_fact_materialization_requirements"]
assert material["source_worker_tip"] == EXPECTED_SOURCE_TIP
assert material["source_ledger_blob"] == EXPECTED_SOURCE_BLOB
assert doc["source_authority"]["source_worker_tip"] == EXPECTED_SOURCE_TIP
assert doc["source_authority"]["source_ledger_blob"] == EXPECTED_SOURCE_BLOB
assert doc["boundary_preservation"]["actor_indexed_prev3pos_fact_emitted"] is False
assert doc["boundary_preservation"]["real_actor_or_entity_materialized"] is False
assert "DIRECT_PREV3POS_FACT_EMISSION" in doc["use_ceiling"]["forbidden"]
assert "ACTOR_OR_ENTITY_OCCUPANCY_ASSERTION" in doc["use_ceiling"]["forbidden"]

print(
    "PASS",
    doc["terminal"],
    identity["content_hash"],
    identity["candidate_id"],
)
