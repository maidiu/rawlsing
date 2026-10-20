"""G18 authenticated material source, whole continuation and C9 consumer court.

This author court is NOT an independent reviewer and does NOT issue native
authority. It exercises the repaired source-owner boundary:

* a sourcefree trusted fixture origin issues exact material/action receipts;
* forged owner, permission, payment (including 100000) and after-state are
  refused even when the caller recomputes public hashes;
* nested/alias/serialized future-child material is denied before COMMITTED;
* the named C9 material consumer reads only the authenticated source/action;
* genuine performed action, material remainder, NO_CHANGE and a bounded
  two-actor materially distinct history survive.

The G17I reviewer oracle is kept byte-identical in
``tests/reviewer_oracle/test_g17i_independent.py`` and run through
``tools/run_g18_courts.py`` against the staged live candidate.
"""
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "candidate"))
sys.path.insert(0, str(ROOT))
from lab_sgi1.history import PersonHistoryBuilder, replay_history, h_obj
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.joint import (
    ACTION_RECEIPT_SCHEMA,
    FIXTURE_SCOPE,
    MATERIAL_PAYMENT_PER_ACTOR,
    MATERIAL_TASK_HOURS,
    NATIVE_GRANT,
    SOURCE_GRADE,
    SOURCE_RECEIPT_SCHEMA,
    material_joint_opportunity,
    observe_joint_actions,
    verify_material_source,
    verify_performed_action,
)
from lab_sgi1.continuation import (
    child_developmental_environment_fixture,
    continue_person,
    forward_continuation,
    lab_conception_boundary,
)
from lab_sgi1.relation import reconcile
from lab_sgi1.research import inputs, run
import c9_handoff_consumer as C9

TWO_ACTOR_RECEIPT = {}


def world(units=5):
    w = deepcopy(next(e["payload"] for e in PersonHistoryBuilder("R", "S").build()
                      if e["kind"] == "WORLD_MATERIAL"))
    w["material_units"] = units
    return w


def history(material=None, actor="G18_SOURCE_ADULT", seed="G18_SOURCE_SEED",
            role="repair"):
    return PersonHistoryBuilder(actor, seed, role=role, material=material).build()


def relation_packet(material=None, units=5):
    a = build_mother_checkpoint("FIX_M0", "M0").anchor_dict()
    e = history(world(units))
    w = observe_joint_actions(a, e, material or material_joint_opportunity())
    rel = reconcile(a, e, dict(candidate_kind="PROVISIONAL_COUNTERPART",
                               joint_evidence=w))
    return a, e, w, rel


def forged_100000(material):
    mat = deepcopy(material)
    mat["payment_per_actor"] = 100000
    mat["event_id"] = h_obj({k: v for k, v in mat.items() if k != "event_id"})
    return mat


def forged_action_with_cash(material):
    _, _, w, _ = relation_packet()
    act = deepcopy(w["actions"][1])
    mat = forged_100000(material)
    act["material_event_ref"] = mat["event_id"]
    act["causal_parent_event_ids"] = [
        x for x in act["causal_parent_event_ids"] if x != material["event_id"]
    ] + [mat["event_id"]]
    after = deepcopy(act["before"])
    after["cash"] += mat["payment_per_actor"]
    after["free_hours"] -= mat["task_hours"]
    after["completed_units"] += mat["material_units"]
    act["after"] = after
    act["event_id"] = h_obj({k: v for k, v in act.items() if k != "event_id"})
    return act, mat


def test_source_issued_material_and_action_receipts_verify():
    material = material_joint_opportunity()
    accepted, reason, payload = verify_material_source(material)
    assert accepted is True and reason is None
    assert payload["payment_per_actor"] == MATERIAL_PAYMENT_PER_ACTOR
    assert payload["task_hours"] == MATERIAL_TASK_HOURS
    assert material["source_receipt"]["schema"] == SOURCE_RECEIPT_SCHEMA
    assert material["source_receipt"]["scope"] == FIXTURE_SCOPE
    assert material["source_receipt"]["source_grade"] == SOURCE_GRADE
    assert material["source_receipt"]["native_grant"] == NATIVE_GRANT
    a, e, witness, _ = relation_packet()
    assert witness["status"] == "WITNESSED"
    for action in witness["actions"]:
        accepted, reason = verify_performed_action(action, material)
        assert accepted is True and reason is None
        assert action["source_receipt"]["schema"] == ACTION_RECEIPT_SCHEMA
        assert action["source_receipt"]["native_grant"] == NATIVE_GRANT


def test_forged_100000_material_is_refused():
    material = material_joint_opportunity()
    forged = forged_100000(material)
    accepted, reason, payload = verify_material_source(forged)
    assert accepted is False
    assert payload is None
    assert reason == "MATERIAL_BODY_HASH_MISMATCH"


def test_forged_owner_and_permission_are_refused():
    material = material_joint_opportunity()
    forged = deepcopy(material)
    forged["owner_id"] = "FAKE_SOURCE_OWNER"
    forged["permission"] = "FAKE"
    forged["event_id"] = h_obj({k: v for k, v in forged.items()
                                if k != "event_id"})
    accepted, reason, _ = verify_material_source(forged)
    assert accepted is False
    assert reason == "MATERIAL_BODY_HASH_MISMATCH"


def test_rehashed_source_wrapper_with_extra_nested_key_is_refused():
    material = material_joint_opportunity()
    wrapper = deepcopy(material)
    wrapper["metadata"] = {"benign": "but_not_source_schema"}
    wrapper["event_id"] = h_obj({k: v for k, v in wrapper.items()
                                 if k != "event_id"})
    accepted, reason, _ = verify_material_source(wrapper)
    assert accepted is False
    assert reason == "MATERIAL_PACKET_SHAPE_NOT_SOURCE_SCHEMA"


def test_public_hash_recompute_does_not_replace_the_source_mac():
    material = material_joint_opportunity()
    forged = deepcopy(material)
    forged["payment_per_actor"] = 7
    payload = {k: forged[k] for k in (
        "owner_id", "permission", "effective_index", "place",
        "material_units", "payment_per_actor", "task_hours", "permit")}
    forged["source_receipt"]["body_hash"] = h_obj(payload)
    forged["event_id"] = h_obj({k: v for k, v in forged.items()
                                if k != "event_id"})
    accepted, reason, _ = verify_material_source(forged)
    assert accepted is False
    assert reason == "SOURCE_RECEIPT_MAC_INVALID"


def test_receipt_cannot_self_upgrade_to_native_authority():
    material = material_joint_opportunity()
    forged = deepcopy(material)
    forged["source_receipt"]["native_grant"] = "GRANTED"
    forged["event_id"] = h_obj({k: v for k, v in forged.items()
                                if k != "event_id"})
    accepted, reason, _ = verify_material_source(forged)
    assert accepted is False
    assert reason == "SOURCE_RECEIPT_CANNOT_CARRY_NATIVE_GRANT"


def test_forged_material_cannot_supply_continue_person_cash():
    material = material_joint_opportunity()
    act, mat = forged_action_with_cash(material)
    _, e, _, _ = relation_packet()
    assert continue_person(e, participation=act, material_event=mat) is None
    assert verify_material_source(mat)[0] is False
    assert verify_performed_action(act, mat)[0] is False


def test_forged_action_afterstate_is_refused():
    material = material_joint_opportunity()
    _, e, w, _ = relation_packet()
    act = deepcopy(w["actions"][1])
    act["after"]["cash"] += 100000
    act["event_id"] = h_obj({k: v for k, v in act.items() if k != "event_id"})
    accepted, reason = verify_performed_action(act, material)
    assert accepted is False
    assert reason == "ACTION_BODY_HASH_MISMATCH"
    assert continue_person(e, participation=act, material_event=material) is None


def test_issuer_refuses_out_of_schedule_material():
    with pytest.raises(ValueError,
                       match="MATERIAL_UNITS_OUTSIDE_SOURCE_SCHEDULE"):
        material_joint_opportunity(units=999)
    with pytest.raises(ValueError,
                       match="MATERIAL_PAYMENT_OUTSIDE_SOURCE_SCHEDULE"):
        material_joint_opportunity(payment_per_actor=100000)
    with pytest.raises(ValueError,
                       match="MATERIAL_TASK_HOURS_OUTSIDE_SOURCE_SCHEDULE"):
        material_joint_opportunity(task_hours=99)


def test_source_issued_variable_schedule_reaches_continued_context():
    material = material_joint_opportunity(payment_per_actor=7, task_hours=2)
    a, e, w, rel = relation_packet(material)
    out = forward_continuation(a, e, rel)
    p = next(x for x in out["continuation_events"] if x["actor"] == "G18_SOURCE_ADULT")
    s = replay_history(e)["state"]
    context = child_developmental_environment_fixture(
        a, e, out, lab_conception_boundary())
    assert rel["relationship_committed"] is True
    assert p["payload"]["before"]["cash"] == s["cash"] + 7
    assert p["payload"]["before"]["free_hours"] == s["free_hours"] - 2
    adult = next(x for x in context["potential_material_contexts"]
                 if x["actor"] == "G18_SOURCE_ADULT")
    assert adult["material_context"]["cash_after"] == s["cash"] + 11
    assert context["exposures"] == []


def test_nested_future_child_metadata_refused_before_commit():
    data = inputs()
    data["joint_material_opportunity"]["metadata"] = {
        "future_child_personality": "NESTED_ALIAS"}
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items()
         if k != "event_id"})
    out = run(data)
    assert out["terminal"]["status"] == "FUTURE_CHILD_INFORMATION_LEAK"
    assert out["future_child_source_leak_refused"] is True
    assert out["causal_replay_record"]["causal_events_emitted"] == 0


def test_serialized_future_child_string_refused():
    data = inputs()
    data["joint_material_opportunity"]["note"] = json.dumps(
        {"future_child_education_outcome": "SERIALIZED_ALIAS"})
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items()
         if k != "event_id"})
    out = run(data)
    assert out["terminal"]["status"] == "FUTURE_CHILD_INFORMATION_LEAK"
    assert any("serialized-json" in x["path"]
               for x in out["terminal"]["leaks"])


def test_future_child_alias_key_is_typed_denied_before_commit():
    data = inputs()
    data["joint_material_opportunity"]["fc_personality"] = "ALIAS"
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items()
         if k != "event_id"})
    out = run(data)
    assert out["terminal"]["status"] != "COMMITTED"
    assert out["terminal"]["status"] in {
        "FUTURE_CHILD_INFORMATION_LEAK", "UNAUTHENTICATED_MATERIAL_SOURCE"}


def test_c9_forged_material_is_refused():
    material = material_joint_opportunity()
    mat = forged_100000(material)
    _, _, w, _ = relation_packet()
    with pytest.raises(C9.C9Refusal) as exc:
        C9.build_handoff(w["actions"][0], mat)
    assert str(exc.value).startswith("MATERIAL_SOURCE_NOT_AUTHENTICATED")


def test_c9_genuine_positive_and_severed_source():
    material = material_joint_opportunity()
    _, _, w, _ = relation_packet()
    handoff = C9.build_handoff(w["actions"][0], material)
    receipt = C9.receive_handoff(handoff, material)
    assert receipt["status"] == "ACCEPTED"
    assert receipt["e2_later_authority"] == "HOLD_UNISSUED"
    assert receipt["route_probability"] is None
    assert receipt["selection_weight"] is None
    severed = deepcopy(handoff)
    severed["causal_parent_event_ids"] = [
        x for x in severed["causal_parent_event_ids"]
        if x != material["event_id"]]
    with pytest.raises(C9.C9Refusal, match="SEVERED_MATERIAL_SOURCE"):
        C9.receive_handoff(severed, material)


def test_authentic_material_remainder_and_lawful_no_change():
    e = history(world(5))
    r = replay_history(e)
    p = continue_person(e)
    assert r["valid"] is True
    assert p is not None
    assert p["payload"]["units_performed"] == 2
    assert p["payload"]["after"]["completed_units"] == 5
    assert p["payload"]["after"]["material_remaining"] == 0
    exhausted = history(world(2))
    assert replay_history(exhausted)["state"]["material_remaining"] == 0
    assert continue_person(exhausted) is None


def test_two_actor_materially_distinct_histories():
    e_repair = history(world(5), actor="G18_REPAIR", seed="SEED_REPAIR",
                       role="repair")
    e_finish = history(world(4), actor="G18_FINISH", seed="SEED_FINISH",
                       role="finishing")
    r_repair = replay_history(e_repair)
    r_finish = replay_history(e_finish)
    assert r_repair["valid"] is True and r_finish["valid"] is True
    assert r_repair["state"]["role"] != r_finish["state"]["role"]
    assert r_repair["state"]["material_remaining"] != r_finish["state"]["material_remaining"]
    assert r_repair["state"]["cash"] != r_finish["state"]["cash"]
    assert r_repair["history_hash"] != r_finish["history_hash"]
    assert {e["event_id"] for e in e_repair}.isdisjoint(
        {e["event_id"] for e in e_finish})

    material = material_joint_opportunity(effective_index=200)
    anchor = dict(actor_id="G18_REPAIR", history_events=e_repair)
    witness = observe_joint_actions(anchor, e_finish, material)
    assert witness["status"] == "WITNESSED"
    assert witness["participants"] == ["G18_REPAIR", "G18_FINISH"]
    a0, a1 = witness["actions"]
    assert a0["owner_id"] == "G18_REPAIR" and a1["owner_id"] == "G18_FINISH"
    assert a0["before"] != a1["before"]
    assert a0["before"]["material_remaining"] != a1["before"]["material_remaining"]
    assert a0["before"]["cash"] != a1["before"]["cash"]
    assert a0["after"] != a1["after"]
    assert verify_material_source(witness["material"])[0] is True
    assert all(verify_performed_action(x, material)[0]
               for x in witness["actions"])

    rel = reconcile(anchor, e_finish, dict(
        candidate_kind="PROVISIONAL_COUNTERPART", joint_evidence=witness))
    out = forward_continuation(anchor, e_finish, rel)
    assert rel["status"] == "COMMITTED"
    assert len(out["continuation_events"]) == 2
    performed = {x["actor"]: x["payload"]["units_performed"]
                 for x in out["continuation_events"]}
    assert performed == {"G18_REPAIR": 2, "G18_FINISH": 1}
    after_units = {x["actor"]: x["payload"]["after"]["completed_units"]
                   for x in out["continuation_events"]}
    assert after_units == {"G18_REPAIR": 6, "G18_FINISH": 5}
    assert out["parental_status"] == "NOT_GRANTED"
    assert out["household_admission"] == "NOT_GRANTED"
    TWO_ACTOR_RECEIPT.update(dict(
        actors=["G18_REPAIR", "G18_FINISH"],
        repair_state=r_repair["state"], finish_state=r_finish["state"],
        witness_status=witness["status"],
        action_before_completed=[a0["before"]["completed_units"],
                                 a1["before"]["completed_units"]],
        continuation_units=performed, continuation_after_units=after_units,
        source_grade=material["source_receipt"]["source_grade"],
        native_grant=material["source_receipt"]["native_grant"],
        claim="TWO_FINITE_SOURCEFREE_MATERIAL_HISTORIES_NOT_TWO_HUMAN_LIVES",
    ))


def test_exhausted_second_actor_is_a_lawful_no_change_alternative():
    e_repair = history(world(5), actor="G18_REPAIR", seed="SEED_REPAIR",
                       role="repair")
    e_finish = history(world(3), actor="G18_FINISH", seed="SEED_FINISH",
                       role="finishing")
    assert replay_history(e_finish)["state"]["material_remaining"] == 0
    material = material_joint_opportunity(effective_index=200)
    anchor = dict(actor_id="G18_REPAIR", history_events=e_repair)
    witness = observe_joint_actions(anchor, e_finish, material)
    rel = reconcile(anchor, e_finish, dict(
        candidate_kind="PROVISIONAL_COUNTERPART", joint_evidence=witness))
    out = forward_continuation(anchor, e_finish, rel)
    actors = [x["actor"] for x in out["continuation_events"]]
    assert actors == ["G18_REPAIR"]
    assert out["continuation_events"][0]["payload"]["units_performed"] == 2
    assert out["parental_status"] == "NOT_GRANTED"


def test_pipeline_committed_positive_is_source_authenticated():
    out = run(inputs())
    assert out["terminal"]["status"] == "COMMITTED"
    witness = out["relation"]["objective_relation"]["witness"]
    assert witness["status"] == "WITNESSED"
    assert verify_material_source(witness["material"])[0] is True
    for action in witness["actions"]:
        assert verify_performed_action(action, witness["material"])[0] is True
    assert out["terminal"]["child_generated_events"] == 0
    assert out["terminal"]["conception_admitted"] is False
    assert out["terminal"]["lab_conception_boundary"]


def test_cold_replay_with_authenticated_receipts(tmp_path):
    first = tmp_path / "first.json"
    replay = tmp_path / "replay.json"
    tampered = tmp_path / "tampered.json"
    tamper_out = tmp_path / "tamper_out.json"
    cmd = [sys.executable, "-B", str(ROOT / "candidate/run_candidate.py")]
    p1 = subprocess.run(cmd + ["--output", str(first)], cwd=str(ROOT),
                        capture_output=True, text=True)
    p2 = subprocess.run(cmd + ["--replay", str(first), "--output", str(replay)],
                        cwd=str(ROOT), capture_output=True, text=True)
    assert p1.returncode == 0 and p2.returncode == 0
    saved = json.loads(first.read_text())
    replayed = json.loads(replay.read_text())
    assert replayed["complete_causal_record_equal"] is True
    packet = json.loads(first.read_text())
    packet["frozen_inputs"]["joint_material_opportunity"]["payment_per_actor"] = 100000
    tampered.write_text(json.dumps(packet))
    p3 = subprocess.run(cmd + ["--replay", str(tampered), "--output",
                               str(tamper_out)], cwd=str(ROOT),
                        capture_output=True, text=True)
    assert p3.returncode == 1
    bad = json.loads(tamper_out.read_text())
    assert bad["complete_causal_record_equal"] is False
    assert bad["result"]["terminal"]["status"] == "UNAUTHENTICATED_MATERIAL_SOURCE"
    assert saved["result"]["terminal"]["status"] == "COMMITTED"
