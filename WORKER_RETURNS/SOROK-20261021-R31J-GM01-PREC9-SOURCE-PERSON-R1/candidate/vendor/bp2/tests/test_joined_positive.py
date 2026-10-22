"""The whole joined BP3 -> BP1 -> C9R source-free positive.

This is the terminal engineering claim of the return: one physically committed
BP3 occurrence carrying two distinct BP1 actor histories, read back through
OUT9, bound into C9R, committed as a durable CAN011 target, cold-reopened in a
separate process, and consumed by an independently performed TEST_ONLY E2.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import bp2_joined
from bp2_joined.producer import (
    ACTUATOR,
    EXPECTED_ACT,
    OCCURRENCE_E2,
    JoinedProducer,
    joined_consumer_assertion,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def positive(tmp_path):
    producer = JoinedProducer(tmp_path / "root")
    outcome = producer.run()
    yield producer, outcome
    producer.close()


def test_joined_positive_commits_create_and_later_e2(positive):
    producer, outcome = positive
    assert outcome.ok is True, outcome.receipt()
    joined_consumer_assertion(outcome)
    receipt = outcome.receipt()
    assert receipt["target_branch"] == "CREATE"
    assert receipt["e2_admitted"] is True
    assert receipt["e2_actuator_ref"] == ACTUATOR
    assert receipt["e2_occurrence_ref"] == OCCURRENCE_E2
    assert receipt["e2_self_performed"] is False
    assert receipt["consumed_state_hash"] == receipt["computed_state_digest"]
    assert receipt["consumed_state_hash"] == receipt["e2_consumed_state_hash"]
    assert receipt["linearized_record_hash"] == receipt["target_record_hash"]
    assert receipt["creation_rule_ref"] == receipt["rule_t_dependency_hash"]


def test_joined_identity_chain_is_the_same_occurrence_everywhere(positive):
    producer, outcome = positive
    receipt = outcome.receipt()
    world = receipt["world"]
    c8 = receipt["c8"]
    c9 = receipt["c9"]
    assert receipt["c8_occurrence_id"] == "OCC-0001"
    assert receipt["out9_occurrence_id"] == receipt["c8_occurrence_id"]
    assert receipt["c8_state_digest"] == receipt["out9_state_digest"]
    assert receipt["c8_state_digest"] == c8["state_digest"]
    assert receipt["c8_commit_receipt_id"] == c9["c8_commit_receipt_id"]
    assert receipt["actor_source_hash"] == world["actor_source_hash"]
    assert receipt["other_source_hash"] == world["other_source_hash"]
    assert receipt["actor_source_hash"] != receipt["other_source_hash"]
    assert receipt["performed_act_ref"] == world["performed_act_ref"]
    assert receipt["other_act_ref"] == world["other_act_ref"]
    assert receipt["performed_act_ref"] != receipt["other_act_ref"]
    event_id = c9["event_id"]
    assert event_id == "TEST_ONLY_BP2_E1_" + receipt["c8_occurrence_id"]
    content = producer.e1_event["content"]
    assert content["c8_occurrence_id"] == receipt["c8_occurrence_id"]
    assert content["c8_state_digest"] == receipt["c8_state_digest"]
    assert content["bp1_causal_parent_event_ids"] == list(world["causal_parent_event_ids"])
    assert content["performed_act_ref"] == receipt["performed_act_ref"]
    assert content["other_act_ref"] == receipt["other_act_ref"]
    assert content["native_grant"] == "NOT_GRANTED"
    assert content["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"


def test_joined_no_native_or_psychology_claim(positive):
    producer, outcome = positive
    receipt = outcome.receipt()
    assert receipt["native_claims"] == []
    assert receipt["psychology_claims"] == []
    assert receipt["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"
    assert receipt["world"]["native_grant"] == "NOT_GRANTED"
    assert receipt["world"]["psychology_claim"] is False
    assert receipt["c9"]["actor_source_grade"] == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    assert producer.e1.admission_status == "TEST_ONLY_E1_BOUND_ADP019_NOT_ISSUED"
    assert producer.e1.native_grant == "NOT_GRANTED"


def test_joined_durable_record_is_reloaded_from_sqlite(positive):
    producer, outcome = positive
    receipt = outcome.receipt()
    record = producer.c9.read_target_state(receipt["target_id"])
    assert record is not None
    assert record["record_hash"] == receipt["target_record_hash"]
    assert record["actor_id"] == receipt["actor_id"]
    assert record["creation_rule_ref"] == receipt["rule_t_dependency_hash"]
    assert record["publication_grade"] == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    assert record["native_admissibility"] == "HELD_UNISSUED"
    assert record["response_hash"] == receipt["response_hash"]
    assert record["permission_ref"] == "TEST_ONLY_BP2_TARGET_GRANT"
    preimage = record["record_preimage"]
    parents = preimage["causal_parent_refs"]
    assert parents[0] == producer.pipeline.event.event_hash
    assert parents[1:] == list(JoinedProducer._history_refs(producer.occurrence))
    assert preimage["governed_payload"]["practice_label"] == (
        "coordinated_material_inspection")


def test_joined_receipt_survives_a_cold_process(tmp_path):
    root = tmp_path / "cold"
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "cold_probe.py"), "build",
         str(root), str(tmp_path / "receipt.json")],
        capture_output=True, text=True, cwd=tmp_path,
        env=_env(),
    )
    assert build.returncode == 0, build.stderr
    verify = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "cold_probe.py"), "verify",
         str(root), str(tmp_path / "receipt.json")],
        capture_output=True, text=True, cwd=tmp_path,
        env=_env(),
    )
    assert verify.returncode == 0, verify.stderr
    cold = json.loads(verify.stdout.strip().splitlines()[-1])
    hot = json.loads((tmp_path / "receipt.json").read_text())
    for key in (
        "c8_occurrence_id", "c8_state_digest", "c8_commit_receipt_id",
        "c8_canonical_bytes_sha256", "target_record_hash",
        "consumed_state_hash", "rule_a_content_hash", "rule_t_content_hash",
        "grant_hash", "response_hash", "e2_receipt_hash",
    ):
        assert cold[key] == hot["persisted"][key], key
    assert cold["journal_proof_verified"] is True
    assert cold["out9_read_equal"] is True
    assert cold["target_record_equal"] is True
    assert cold["e2_readmitted"] is True
    assert cold["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"


def test_joined_duplicate_occurrence_is_a_no_change_not_a_second_event(positive):
    producer, outcome = positive
    assert outcome.ok is True
    before = producer.env.journal_path.read_bytes()
    second = producer.run()
    assert second.ok is False
    assert second.stage_reached == "c8_exclusive_append"
    assert second.failure_code == "C8_OCCURRENCE_NOT_ADMITTED"
    assert "DUPLICATE_NO_CHANGE" in second.failure_detail
    assert producer.env.journal_path.read_bytes() == before
    assert producer.pipeline.decision.branch.value == "CREATE"


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env
