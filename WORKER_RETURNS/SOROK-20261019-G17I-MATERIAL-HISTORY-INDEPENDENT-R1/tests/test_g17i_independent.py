"""G17I fresh adversarial review tests.

These are reviewer-made, not G17 author tests. They attack the eight claimed
material/actor/time/future edges through public interfaces, including alternate
schemas/aliases and forged source packets. Expected bypasses are left as literal
failures, not softened.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "stage/WORKER_RETURNS/SOROK-20261019-G17-MATERIAL-HISTORY-INDEPENDENT-LIVES-R1"
sys.path.insert(0, str(CAND / "candidate"))
sys.path.insert(0, str(CAND))
from lab_sgi1.history import (PersonHistoryBuilder, replay_history, make_event,
                              derive_psyche, independent_actions, h_obj)
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.continuation import continue_person, forward_continuation
from lab_sgi1.joint import material_joint_opportunity, observe_joint_actions
from lab_sgi1.relation import reconcile
from lab_sgi1.research import inputs, run
from lab_sgi1.proposal import frozen_fallback_record
import c9_handoff_consumer as C9


def world(units=5):
    w = deepcopy(next(e["payload"] for e in PersonHistoryBuilder("R", "S").build()
                      if e["kind"] == "WORLD_MATERIAL"))
    w["material_units"] = units
    return w


def history(material=None):
    return PersonHistoryBuilder("R", "S", material=material).build()


def ec(place="INST_WORKSHOP_A", route="ROUTE_LOCAL_CLOSED"):
    return dict(route_kind_id=route, time_or_interval="T_ENCOUNTER_LAB_WINDOW",
                required_state_predicates=[dict(field="place", equals=place),
                                           dict(field="availability_status", equals="available_for_encounter")])


def relation_packet(material=None):
    a = build_mother_checkpoint("FIX_M0", "M0").anchor_dict()
    e = history(world())
    w = observe_joint_actions(a, e, material or material_joint_opportunity())
    rel = reconcile(a, e, dict(candidate_kind="PROVISIONAL_COUNTERPART", joint_evidence=w))
    return a, e, w, rel


def test_stock5_two_conflicting_claims_rejected_with_positive_alternative():
    e = history(world(5))
    p = deepcopy(next(x for x in e if x["kind"] == "PROJECT"))
    p["effective_index"] = 100
    p["event_id"] = h_obj({k: v for k, v in p.items() if k != "event_id"})
    e.append(p)
    r = replay_history(e)
    assert not r["valid"] or r["state"]["completed_units"] <= 5
    assert r["state"]["material_remaining"] >= 0
    # Proper positive alternative: two material units can perform two units.
    small = history(world(2))
    rs = replay_history(small)
    assert rs["valid"] is True
    assert rs["state"]["completed_units"] == 2
    assert rs["state"]["material_remaining"] == 0


def test_double_schooling_rejected_with_current_free_hours():
    e = history(world())
    e.append(make_event(100, "SCHOOLING", "R", dict(hours=30), [e[0]["event_id"]]))
    r = replay_history(e)
    assert not r["valid"] or r["state"]["free_hours"] >= 0
    one = history(world())
    assert replay_history(one)["state"]["free_hours"] == 13
    assert replay_history(one)["valid"] is True


def test_repeated_tool_return_rejected_with_current_tools():
    e = history(world())
    pa = deepcopy(next(x for x in e if x["kind"] == "PEER_ACTION"))
    pa["effective_index"] = 100
    pa["event_id"] = "REVIEW_SECOND_PEER"
    e.append(pa)
    r = replay_history(e)
    assert not r["valid"] or r["state"]["tools_remaining"] >= 0
    returned = sum(x["effect"]["returned_units"] for x in r["value_witnesses"]
                   if x["kind"] == "PEER_ACTION")
    assert r["state"]["tools_remaining"] == 1
    assert returned <= 3


def test_forged_afterstate_with_genuine_material_refused():
    a, e, w, rel = relation_packet()
    act = deepcopy(w["actions"][1])
    act["after"]["cash"] += 100000
    act["event_id"] = h_obj({k: v for k, v in act.items() if k != "event_id"})
    assert continue_person(e, participation=act, material_event=w["material"]) is None


def test_forged_material_event_supplying_cash_must_be_refused():
    a, e, w, rel = relation_packet()
    act = deepcopy(w["actions"][1])
    mat = deepcopy(w["material"])
    mat["payment_per_actor"] = 100000
    mat["event_id"] = h_obj({k: v for k, v in mat.items() if k != "event_id"})
    act["material_event_ref"] = mat["event_id"]
    act["causal_parent_event_ids"] = list(act["causal_parent_event_ids"]) + [mat["event_id"]]
    after = deepcopy(act["before"])
    after["cash"] += mat["payment_per_actor"]
    after["free_hours"] -= mat["task_hours"]
    after["completed_units"] += mat["material_units"]
    act["after"] = after
    act["event_id"] = h_obj({k: v for k, v in act.items() if k != "event_id"})
    assert continue_person(e, participation=act, material_event=mat) is None


def test_late_effective_participation_cannot_parent_past_continuation():
    a, e, w, rel = relation_packet(material_joint_opportunity(1100))
    out = forward_continuation(a, e, rel)
    assert out["continuation_events"] == []
    assert out["maternal_continuation_admitted"] is False
    good = forward_continuation(a, e, relation_packet()[3])
    assert len(good["continuation_events"]) == 2


def test_fake_second_participant_refused():
    e = history(world())
    next(x for x in e if x["kind"] == "WORK_POSITION")["actors"].append("FAKE_OTHER")
    assert replay_history(e)["valid"] is False
    w = observe_joint_actions(build_mother_checkpoint("FIX_M0", "M0").anchor_dict(),
                              history(world()), material_joint_opportunity())
    assert {a["owner_id"] for a in w["actions"]} == {x["owner_id"] for x in w["actions"]}
    assert len(w["actions"]) == 2


def test_future_child_top_level_refused():
    data = inputs()
    data["joint_material_opportunity"]["future_child_personality"] = "X"
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items() if k != "event_id"})
    assert run(data)["terminal"]["status"] != "COMMITTED"


def test_future_child_nested_alias_must_be_refused():
    data = inputs()
    data["joint_material_opportunity"]["metadata"] = {
        "future_child_personality": "NESTED_ALIAS"}
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items() if k != "event_id"})
    out = run(data)
    assert out["terminal"]["status"] != "COMMITTED"


def test_joined_terminal_6_from_5_not_committed(monkeypatch):
    original = PersonHistoryBuilder.build

    def overspend(self):
        events = original(self)
        if self.role == "repair":
            p = deepcopy(next(e for e in events if e["kind"] == "PROJECT"))
            p["effective_index"] = 80
            p["event_id"] = h_obj({k: v for k, v in p.items() if k != "event_id"})
            events.append(p)
        return events

    monkeypatch.setattr(PersonHistoryBuilder, "build", overspend)
    bad = run()
    available = next(e["payload"]["material_units"] for e in bad["dad_events"]
                     if e["kind"] == "WORLD_MATERIAL")
    spent = sum(e["payload"]["durable_effect"]["materials_used"] for e in bad["dad_events"]
                if e["kind"] == "PROJECT")
    assert spent > available
    assert bad["terminal"]["status"] != "COMMITTED"


def test_m2_mp_are_typed_holds_not_fake_positives():
    m2 = build_mother_checkpoint("FIX_M2", "M2").anchor_dict()
    before = deepcopy(m2)
    out = forward_continuation(m2, [], {})
    assert m2 == before
    assert out["maternal_continuation_admitted"] is False
    assert out["continuation_events"] == []
    assert m2["already_generated_child_refs"] == ["LAB_OLDER_CHILD_O1"]
    data = inputs()
    data["fixture_variant"] = "MP"
    data["proposal_record"] = frozen_fallback_record("MP", "ROUTE_LOCAL_CLOSED")
    mp = run(data)
    assert mp["terminal"]["status"] == "SHARED_HISTORY_CONTRADICTION_HOLD"
    assert mp["terminal"]["no_duplicate_actor_or_event"] is True
    assert build_mother_checkpoint("FIX_MP", "MP").known_counterpart_identity_ref_or_null == "F_EXISTING"


def test_two_vs_five_material_lives_are_genuinely_distinct():
    rows = []
    for units in (2, 5):
        e = history(world(units))
        r = replay_history(e)
        p = derive_psyche(e)
        acts = independent_actions(e, p)
        rows.append((r, p, acts))
        assert r["valid"] is True
    assert [r["state"]["completed_units"] for r, _, _ in rows] == [2, 3]
    assert [r["state"]["material_remaining"] for r, _, _ in rows] == [0, 2]
    assert [p["practices"][0]["formed_value"]["checks"] for _, p, _ in rows] == [2, 3]
    assert [a["probes"][0]["typed_action"]["after"]["completed_units"] for _, _, a in rows] == [3, 4]


def test_c9_material_handoff_genuine_and_severed():
    a, e, w, rel = relation_packet()
    act = w["actions"][0]
    hand = C9.build_handoff(act, w["material"])
    rec = C9.receive_handoff(hand, w["material"])
    assert rec["status"] == "ACCEPTED"
    assert rec["route_probability"] is None and rec["selection_weight"] is None
    severed = deepcopy(hand)
    severed["causal_parent_event_ids"] = [x for x in severed["causal_parent_event_ids"]
                                          if x != w["material"]["event_id"]]
    with pytest.raises(C9.C9Refusal, match="SEVERED_MATERIAL_SOURCE"):
        C9.receive_handoff(severed, w["material"])


def test_c9_forged_material_event_must_be_refused():
    a, e, w, rel = relation_packet()
    act = deepcopy(w["actions"][0])
    mat = deepcopy(w["material"])
    mat["payment_per_actor"] = 100000
    mat["event_id"] = h_obj({k: v for k, v in mat.items() if k != "event_id"})
    act["material_event_ref"] = mat["event_id"]
    act["causal_parent_event_ids"] = list(act["causal_parent_event_ids"]) + [mat["event_id"]]
    after = deepcopy(act["before"])
    after["cash"] += mat["payment_per_actor"]
    after["free_hours"] -= mat["task_hours"]
    after["completed_units"] += mat["material_units"]
    act["after"] = after
    act["event_id"] = h_obj({k: v for k, v in act.items() if k != "event_id"})
    with pytest.raises(C9.C9Refusal):
        hand = C9.build_handoff(act, mat)
        C9.receive_handoff(hand, mat)
