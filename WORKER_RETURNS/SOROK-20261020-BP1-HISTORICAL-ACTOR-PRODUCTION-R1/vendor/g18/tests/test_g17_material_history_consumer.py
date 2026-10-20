"""G17 material-conserving history/current-state consumer court.

The frozen G16I hostile expectations are preserved: the directly material
counterexamples must be refused, and the incompatible M2/MP archive demands
must remain typed HOLDs, never fabricated positives.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "candidate"))
from lab_sgi1.history import PersonHistoryBuilder, replay_history, make_event, h_obj
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.continuation import forward_continuation, continue_person
from lab_sgi1.joint import material_joint_opportunity, observe_joint_actions, validate_joint
from lab_sgi1.relation import reconcile
from lab_sgi1.research import inputs, run
from lab_sgi1.proposal import frozen_fallback_record
sys.path.insert(0, str(ROOT))
import c9_handoff_consumer as C9


def world(units=5):
    w = deepcopy(next(e["payload"] for e in PersonHistoryBuilder("G17_ADULT", "G17_SOURCE").build()
                      if e["kind"] == "WORLD_MATERIAL"))
    w["material_units"] = units
    return w


def history(material=None):
    return PersonHistoryBuilder("G17_ADULT", "G17_SOURCE", material=material).build()


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


def test_repeated_project_cannot_spend_same_material_twice():
    e = history(world(5))
    project = deepcopy(next(x for x in e if x["kind"] == "PROJECT"))
    project["effective_index"] = 100
    project["event_id"] = h_obj({k: v for k, v in project.items() if k != "event_id"})
    e.append(project)
    r = replay_history(e)
    assert not r["valid"] or r["state"]["completed_units"] <= 5


def test_repeated_training_cannot_overspend_current_time():
    e = history(world())
    e.append(make_event(100, "SCHOOLING", "G17_ADULT", dict(hours=30), [e[0]["event_id"]]))
    r = replay_history(e)
    assert not r["valid"] or r["state"]["free_hours"] >= 0


def test_repeated_peer_actions_cannot_return_nonexistent_tools():
    e = history(world())
    pa = deepcopy(next(x for x in e if x["kind"] == "PEER_ACTION"))
    pa["effective_index"] = 100
    pa["event_id"] = "G17_SECOND_PEER_RETURN"
    e.append(pa)
    r = replay_history(e)
    returned = sum(x["effect"]["returned_units"] for x in r["value_witnesses"]
                   if x["kind"] == "PEER_ACTION")
    assert not r["valid"] or returned <= 3


def test_forged_participation_cannot_supply_unperformed_cash():
    a, e, w, rel = relation_packet()
    action = deepcopy(w["actions"][1])
    action["after"]["cash"] += 100000
    action["event_id"] = h_obj({k: v for k, v in action.items() if k != "event_id"})
    assert continue_person(e, participation=action,
                           material_event=w["material"]) is None


def test_late_participation_cannot_parent_earlier_continuation():
    a, e, w, rel = relation_packet(material_joint_opportunity(1100))
    out = forward_continuation(a, e, rel)
    assert out["continuation_events"] == []
    assert out["maternal_continuation_admitted"] is False
    assert out["relationship_continuation_admitted"] is False


def test_singular_owned_event_cannot_silently_add_other_actor():
    e = history(world())
    next(x for x in e if x["kind"] == "WORK_POSITION")["actors"].append("UNPERFORMED_OTHER_PERSON")
    assert replay_history(e)["valid"] is False


def test_future_child_material_cannot_enter_committed_causal_output():
    data = inputs()
    data["joint_material_opportunity"]["future_child_personality"] = "G17_DESIRED_WOUND"
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items() if k != "event_id"})
    out = run(data)
    assert out["terminal"]["status"] != "COMMITTED"
    assert out["terminal"]["status"] == "FUTURE_CHILD_INFORMATION_LEAK"


def test_joined_terminal_refuses_material_overspend(monkeypatch):
    original = PersonHistoryBuilder.build

    def overspend(self):
        events = original(self)
        if self.role == "repair":
            project = deepcopy(next(e for e in events if e["kind"] == "PROJECT"))
            project["effective_index"] = 80
            project["event_id"] = h_obj({k: v for k, v in project.items() if k != "event_id"})
            events.append(project)
        return events

    monkeypatch.setattr(PersonHistoryBuilder, "build", overspend)
    bad = run()
    available = next(e["payload"]["material_units"] for e in bad["dad_events"]
                     if e["kind"] == "WORLD_MATERIAL")
    spent = sum(e["payload"]["durable_effect"]["materials_used"] for e in bad["dad_events"]
                if e["kind"] == "PROJECT")
    assert spent > available
    assert bad["terminal"]["status"] != "COMMITTED"


def test_m2_archive_is_exact_typed_coverage_hold():
    anchor = build_mother_checkpoint("FIX_M2", "M2").anchor_dict()
    before = deepcopy(anchor)
    out = forward_continuation(anchor, [], {})
    assert anchor == before
    assert anchor["already_generated_child_refs"] == ["LAB_OLDER_CHILD_O1"]
    assert out["maternal_continuation_admitted"] is False
    assert out["continuation_events"] == []
    assert out["parental_status"] == "NOT_GRANTED"


def test_mp_known_counterpart_is_exact_typed_coverage_hold():
    data = inputs()
    data["fixture_variant"] = "MP"
    data["proposal_record"] = frozen_fallback_record("MP", "ROUTE_LOCAL_CLOSED")
    out = run(data)
    cp = build_mother_checkpoint("FIX_MP", "MP")
    assert cp.known_counterpart_identity_ref_or_null == "F_EXISTING"
    assert out["terminal"]["status"] == "SHARED_HISTORY_CONTRADICTION_HOLD"
    assert out["terminal"]["no_duplicate_actor_or_event"] is True
    assert out["terminal"]["mother_history_unchanged"] is True
    assert out["relation"] is None


def test_positive_material_remainder_is_not_vacuous():
    e = history(world(5))
    r = replay_history(e)
    p = continue_person(e)
    assert r["valid"] is True
    assert p is not None
    assert p["payload"]["units_performed"] == 2
    assert p["payload"]["after"]["completed_units"] == 5


def test_c9_handoff_reads_material_afterstate():
    a, e, w, rel = relation_packet()
    act = w["actions"][0]
    handoff = C9.build_handoff(act, w["material"])
    out = C9.receive_handoff(handoff, w["material"])
    assert out["status"] == "ACCEPTED"
    assert out["after"]["completed_units"] == act["after"]["completed_units"]
    assert out["route_probability"] is None
    assert out["selection_weight"] is None
    assert out["e2_later_authority"] == "HOLD_UNISSUED"


def test_c9_handoff_refuses_severed_material_source():
    a, e, w, rel = relation_packet()
    act = w["actions"][0]
    handoff = C9.build_handoff(act, w["material"])
    severed = deepcopy(handoff)
    severed["causal_parent_event_ids"] = [
        x for x in severed["causal_parent_event_ids"]
        if x != w["material"]["event_id"]]
    with pytest.raises(C9.C9Refusal, match="SEVERED_MATERIAL_SOURCE"):
        C9.receive_handoff(severed, w["material"])
