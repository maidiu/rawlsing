#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET_PATH = HERE / "01_SOURCE_APPLICABILITY_PACKET.json"
FIXTURE_PATH = HERE / "02_REPLAY_FIXTURE.json"

EXPECTED_CANDIDATE_HASH = "60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505"
EXPECTED_CANDIDATE_ID = (
    "urn:rawlsing:prev3:objective-position-admission-candidate:sha256:"
    + EXPECTED_CANDIDATE_HASH
)
EXPECTED_PACKET_SHA256 = "8fb2f9774309dd35d50387bb4764a6543856661da2ba7a8da9c7be8f4e1194ab"
EXPECTED_REQUIREMENTS = [
    "PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION",
    "ACTIVE_WAGE_LABOUR_SALE_RELATION",
    "EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY",
    "EXACT_INSTITUTIONAL_RULE_CONTEXT",
]
EXPECTED_MISSING = [
    "EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY",
    *EXPECTED_REQUIREMENTS,
    "EXACT_VALID_TIME_OR_CURRENTNESS",
]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

assert file_sha256(PACKET_PATH) == EXPECTED_PACKET_SHA256
assert fixture["packet_sha256"] == EXPECTED_PACKET_SHA256

assert packet["task_id"] == "D12"
assert packet["run_id"] == "PSC05_T01_EXACT_M10_POSITION_MATERIALIZATION_SOURCE_APPLICABILITY_PACKET_ONLY_R1"
assert packet["status"] == "BLOCKED_TYPED_MISSING_INPUT"
assert packet["terminal"] == fixture["expected_terminal"]

candidate = packet["frozen_semantic_candidate"]
assert candidate["candidate_hash"] == EXPECTED_CANDIDATE_HASH
assert candidate["candidate_id"] == EXPECTED_CANDIDATE_ID
assert candidate["constitutive_requirements"] == EXPECTED_REQUIREMENTS
assert candidate["semantic_only"] is True
assert candidate["actor_fact_truth_established"] is False

assert fixture["expected_candidate_hash"] == EXPECTED_CANDIDATE_HASH
assert fixture["expected_candidate_id"] == EXPECTED_CANDIDATE_ID
assert fixture["expected_constitutive_requirements"] == EXPECTED_REQUIREMENTS
assert fixture["expected_missing_instance_predicates"] == EXPECTED_MISSING

audit = packet["position_level_predicate_audit"]
assert list(audit.keys()) == EXPECTED_MISSING
for predicate in EXPECTED_MISSING:
    row = audit[predicate]
    assert row["status"] == "MISSING_COMPETENT_SOURCE_OWNED_INSTANCE_EVIDENCE"
    assert row["exact_value"] is None
    assert row["evidence_refs"]

four = packet["four_constitutive_predicate_audit"]
assert list(four.keys()) == EXPECTED_REQUIREMENTS
for predicate in EXPECTED_REQUIREMENTS:
    assert four[predicate]["position_instance_status"] == "MISSING_COMPETENT_SOURCE_OWNED_INSTANCE_EVIDENCE"
    assert four[predicate]["source_or_absence_evidence"]

app = packet["applicability_determination"]
assert app["q73a_q84_real_position_instance_applicable"] is False
assert app["determination"] == "NOT_ESTABLISHED__MISSING_REAL_POSITION_LEVEL_SOURCE_FACTS"
assert app["missing_witness_predicates"] == EXPECTED_MISSING

missing = packet["typed_missing_input_report"]
assert missing["blocker_type"] == "MISSING_REAL_POSITION_LEVEL_SOURCE_WITNESS"
assert [row["kind"] for row in missing["missing_inputs"]] == EXPECTED_MISSING

law = packet["substitution_law"]
assert all(value is False for value in law.values())
for case in fixture["substitution_cases"]:
    assert case["accept_as_real_witness"] is False
    assert case["candidate_value"] not in {
        row["exact_value"] for row in audit.values() if row["exact_value"] is not None
    }

gate = packet["successor_gate"]
assert gate["D13_wake"] is False
assert gate["decision"] == "DO_NOT_WAKE_D13"
assert gate["position_fact_emitted"] is False
assert gate["downstream_reconciliation_performed"] is False

bounds = packet["boundary_preservation"]
assert all(value is False for value in bounds.values())
assert packet["commission"]["library_mode"] == "NO"
assert packet["commission"]["library_used"] is False
assert packet["commission"]["main_mutated"] is False
assert packet["commission"]["pre_main_mutated"] is False

result = {
    "validation": "PASS",
    "task_status": packet["status"],
    "terminal": packet["terminal"],
    "packet_sha256": EXPECTED_PACKET_SHA256,
    "candidate_hash": EXPECTED_CANDIDATE_HASH,
    "missing_instance_predicate_count": len(EXPECTED_MISSING),
    "rejected_substitution_case_count": len(fixture["substitution_cases"]),
    "D13_wake": False,
    "library_used": False,
}
print(json.dumps(result, sort_keys=True))
