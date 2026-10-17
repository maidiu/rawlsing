"""Independent, source-free adversarial court against the pinned B2 import closure.

Set B2_REVIEW_ROOT to a fresh materialization of the exact B2 commit. No
upstream source or frozen fixture is patched by this court.
"""
from copy import deepcopy
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

ROOT = Path(os.environ["B2_REVIEW_ROOT"]).resolve()
sys.path.insert(0, str(ROOT))
bridge_module = importlib.import_module("bridge")
Bridge = bridge_module.Bridge
b1 = bridge_module.b1
p1 = bridge_module.p1


def setup(tmp_path, *, history="recognized_plan", alternative="ALT-CARE", other=None):
    initial = b1.initialize(b1.prehistory(history))
    bridge = Bridge(tmp_path / "state.sqlite", initial)
    packet, context, policy = bridge_module.input_pair(initial, alternative=alternative, other=other)
    witness = bridge_module.occurrence_witness(initial, packet, context, alternative=alternative, other=other)
    cap, registry = bridge_module.capability_fixture()
    bridge.witnesses = {witness["hash"]: witness}
    bridge.capability_witnesses = registry
    return bridge, packet, context, policy, witness, cap


def register(bridge, witness, **changes):
    body = {k: deepcopy(v) for k, v in witness.items() if k != "hash"}
    body.update(changes)
    result = b1.sealed(body)
    bridge.witnesses[result["hash"]] = result
    return result


def assert_untouched(bridge, before):
    assert bridge.store.state() == before
    assert bridge.store.db.execute("SELECT count(*) FROM occurrence").fetchone()[0] == 0


@pytest.mark.parametrize("mutation,reason", [
    ("missing", "INDEPENDENT_OCCURRENCE_WITNESS_REQUIRED"),
    ("issuer", "WITNESS_SCHEMA_OR_ISSUER_INVALID"),
    ("candidate_hash", "WITNESS_BINDING_OR_STALE_STATE"),
    ("parent_fact_hash", "WITNESS_BINDING_OR_STALE_STATE"),
    ("state_hash", "WITNESS_BINDING_OR_STALE_STATE"),
    ("utterance", "UTTERANCE_NOT_INDEPENDENTLY_WITNESSED"),
    ("child_visibility", "CHILD_NOT_EXPOSED"),
    ("group_truth", "PEER_PREJUDICE_LAUNDERED_AS_FACT"),
])
def test_proposal_and_forged_witness_never_become_fact(tmp_path, mutation, reason):
    bridge, packet, context, policy, witness, cap = setup(tmp_path, alternative="ALT-PEER" if mutation == "group_truth" else "ALT-CARE")
    before = bridge.store.state()
    if mutation == "missing":
        bridge.witnesses = {}
    elif mutation == "issuer":
        witness = register(bridge, witness, issuer="P1_MODEL")
    elif mutation == "candidate_hash":
        witness = register(bridge, witness, candidate_hash="0" * 64)
    elif mutation == "parent_fact_hash":
        witness = register(bridge, witness, parent_fact_hash="0" * 64)
    elif mutation == "state_hash":
        witness = register(bridge, witness, expected_actor_state_hash="0" * 64)
    elif mutation == "utterance":
        witness = register(bridge, witness, observed_interpretations=[dict(witness["observed_interpretations"][0], utterance="unwitnessed model speech")])
    elif mutation == "child_visibility":
        selected = next(c for c in packet["candidates"] if c["candidate_id"] == "ALT-CARE")
        selected["visibility"] = []
        packet = bridge_module.rehash(packet, "proposal_hash")
        evaluation = p1.evaluate(packet, context)
        policy["candidate_set_hash"] = evaluation["candidate_set_hash"]
        policy = bridge_module.rehash(policy, "policy_hash")
        witness = bridge_module.occurrence_witness(before, packet, context)
        bridge.witnesses = {witness["hash"]: witness}
    else:
        witness = register(bridge, witness, world_facts={"known_thief": "ethnic_group", "group_criminality": "TRUE"})
    result = bridge.advance(packet, context, policy, witness, cap)
    assert result["reason"] == reason
    assert not result["b1_invoked"]
    assert_untouched(bridge, before)
    bridge.close()


def test_unowned_permission_and_post_checkpoint_rollback(tmp_path):
    for label, kwargs in (("denied", {"grant": False}), ("checkpoint", {"fault": "after_checkpoint"})):
        sub = tmp_path / label
        sub.mkdir()
        bridge, packet, context, policy, witness, cap = setup(sub)
        before = bridge.store.state()
        result = bridge.advance(packet, context, policy, witness, cap, **kwargs)
        assert result["status"] == "TRANSACTION_ABORTED_ROLLBACK"
        assert bridge.store.state() == before
        assert bridge.store.db.execute("SELECT count(*) FROM occurrence").fetchone()[0] == 1
        assert bridge.store.db.execute("SELECT count(*) FROM joint_receipt").fetchone()[0] == 0
        bridge.close()
        reopened = Bridge(sub / "state.sqlite")
        assert reopened.store.state() == before
        reopened.close()


def test_stale_target_permission_after_separate_target_change(tmp_path):
    bridge, packet, context, policy, witness, cap = setup(tmp_path)
    admitted = bridge.store.admit_fixture(b1.episode())
    before = bridge.store.state()
    response = b1.propose(before, admitted)
    permission = b1.TestOnlyCAN011Owner.permission(before, response)
    changed = deepcopy(before)
    changed["middle"].append({"separate_owner_change": True})
    owner = b1.TestOnlyCAN011Owner([permission["hash"]])
    with pytest.raises(b1.Refusal, match="PERMISSION_BINDING_INVALID"):
        owner.validate(changed, admitted, response, permission)
    assert bridge.store.state() == before
    bridge.close()


def test_cosmetic_history_label_is_actual_response_switch(tmp_path):
    outcomes = []
    for label in ("recognized_plan", "imposed_plan"):
        sub = tmp_path / label
        sub.mkdir()
        bridge, packet, context, policy, witness, cap = setup(sub, history=label)
        state = bridge.store.state()
        assert state["history"][1]["activity"] == "compare_plans_in_task"
        result = bridge.advance(packet, context, policy, witness, cap)
        assert result["status"] == "COMMITTED"
        outcomes.append((result["response"]["practical_activity"], bridge.store.state()["middle"][0]["governed_payload"]["mode"]))
        bridge.close()
    assert outcomes[0] != outcomes[1], "Label sensitivity no longer exists; reexamine the science grade"
    assert [mode for _, mode in outcomes] == ["joint_check", "private_check"]


def test_independent_caregiver_activity_controls_offer_without_child_alias(tmp_path):
    offers = []
    for outcome in ("tools_available", "deadline_due"):
        sub = tmp_path / outcome
        sub.mkdir()
        other = {"CARE-1": b1.participant(outcome=outcome)}
        bridge, packet, context, policy, witness, cap = setup(sub, other=other)
        result = bridge.advance(packet, context, policy, witness, cap)
        assert result["status"] == "COMMITTED"
        offers.append((witness["other_actions"][0]["action"], len(bridge.store.state()["middle"])))
        assert witness["other_actions"][0]["participant"]["history"][0]["actor_id"] == "caretaker"
        bridge.close()
    assert offers == [("joint_inventory", 1), ("secure_alone", 0)]


def test_unknown_and_uncomparable_absence_cannot_diagnose(tmp_path):
    for status, reason in (("CAPABILITY_UNKNOWN", "CAPABILITY_UNKNOWN"), ("CAPABILITY_ABSENT", "ABSENCE_EVIDENCE_MISSING")):
        sub = tmp_path / status
        sub.mkdir()
        bridge, packet, context, policy, witness, cap = setup(sub)
        cap["actor"]["capabilities"]["C07"]["status"] = status
        result = bridge.advance(packet, context, policy, witness, cap)
        assert result["reason"] == reason
        assert result["event_admission"]["status"] == "ADMITTED_SYNTHETIC_FIXTURE_ONLY"
        assert bridge.store.state()["middle"] == []
        bridge.close()


def test_c02_witnessed_affect_remains_proposable_when_c07_unknown():
    source = (ROOT / "imports/D1/07_CORRECTED_ABSENCE_CONTRACT_COURT.js").read_text()
    cases = json.loads(re.search(r"const cases=(\[.*\]);\nlet n=", source).group(1))
    packet = deepcopy(cases[0]["p"])
    assert packet["candidate"]["capabilities"] == ["C02"]
    assert packet["actor"]["capabilities"]["C07"]["status"] == "CAPABILITY_UNKNOWN"
    result = subprocess.run(["node", str(ROOT / "d1_gate.js"), str(ROOT / "imports/D1/07_CORRECTED_ABSENCE_CONTRACT_COURT.js")],
                            input=json.dumps(packet), capture_output=True, text=True, check=True)
    decision = json.loads(result.stdout)
    assert decision["self_tests"] == 17
    assert decision["result"]["decision"] == "PROPOSABLE_ONLY"


def test_private_caregiver_history_does_not_enter_actor_surface(tmp_path):
    bridge, packet, context, policy, witness, cap = setup(tmp_path)
    result = bridge.advance(packet, context, policy, witness, cap)
    surface = json.dumps(result["actor_safe"])
    for private in ("recognized_plan", "shared_task", "caregiver-private", "source_history_hash"):
        assert private not in surface
    assert result["actor_safe"]["origin_explanation"] == "NOT_ACCESSIBLE"
    bridge.close()


def test_f1_expected_gate_is_only_reporting_metadata():
    f1 = importlib.import_module("f1_adapter")
    cases = json.loads((ROOT / "imports/F1/court/f1_frozen_court/frozen_cases.json").read_text())["cases"]
    case = deepcopy(cases[0])
    original = f1.run_case(case)
    case["expected_gate"] = "ADMITTED" if case["expected_gate"] != "ADMITTED" else "DENIED"
    altered = f1.run_case(case)
    assert original == altered


def test_same_event_id_accepts_distinct_objective_payload_hashes(tmp_path):
    """Observed custody gap: occurrence table uses content hash, not event identity."""
    bridge, packet, context, policy, witness, cap = setup(tmp_path)
    original = bridge.advance(packet, context, policy, witness, cap, grant=False)
    assert original["event_admission"]["status"] == "ADMITTED_SYNTHETIC_FIXTURE_ONLY"
    altered = register(bridge, witness, objective_occurrence="DIFFERENT_OBJECTIVE_EVENT")
    second = bridge.advance(packet, context, policy, altered, cap, grant=False)
    rows = [json.loads(row[0]) for row in bridge.store.db.execute("SELECT body FROM occurrence")]
    assert second["event_admission"]["status"] == "ADMITTED_SYNTHETIC_FIXTURE_ONLY"
    assert len(rows) == 2
    assert len({row["event_id"] for row in rows}) == 1
    assert len({row["hash"] for row in rows}) == 2
    bridge.close()
