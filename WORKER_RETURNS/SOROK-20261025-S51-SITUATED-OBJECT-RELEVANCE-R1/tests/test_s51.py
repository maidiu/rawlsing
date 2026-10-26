"""Focused S51 retained-object relevance tests."""
from __future__ import annotations
import pytest
from s51.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s51.session import S51Session


def _start(state):
 c=case_for(True)
 return S51Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),language_context={"milieu_id":"workshop"})


def test_actual_root_object_and_hypothesis_and_offer_relevance():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object()
  assert obj["striving"]=="fund_finishing_equipment"
  assert obj["actor_id"]!="G15_WORLD"
  assert obj["work_parent_event_id"] and obj["project_parent_event_id"]
  assert obj["route_usage"]
  r=s.run_experiment()
  assert r["hypothesis"]["actual_current_purpose_proved"] is False
  assert r["hypothesis"]["status"]=="DECLARED_IMMUTABLE"
  assert r["offer"]["event_id"]
  assert r["access"]["access_status"]=="ACCESSIBLE"
  assert r["relevance"]["relation"]=="FACILITATES"
  assert r["relevance"]["object_event_id"]==obj["object_event_id"]
  assert r["generation"]["source_ref"].startswith("S51_SOURCE_")
  assert r["generation"]["source_ref"] in r["generation"]["source_refs"]
  assert r["generation"]["selection_status"]=="OPEN_CHOICE_SET"
  assert r["generation"]["selected_option"]==""  # qualified open, no invented winner
  assert not r["generation"]["reasons"]  # no invented option-specific preference
  qualified=[x for x in r["generation"]["qualified_sources"] if x["source_ref"]==r["generation"]["source_ref"]]
  assert qualified and qualified[0]["content"]["relation"]=="FACILITATES"
  source=r["generation"]["source"]
  def last_turn_generation(session):
   return [row["body"]["generation"]["generation"] for row in session.b_turns() if row["kind"]=="S49_B_ACTOR_TURN"][-1]
  s.produce_b_turn(controlled=True,source_records_override=[])
  cut=last_turn_generation(s)
  assert source["source_ref"] not in cut.get("source_refs",[])
  s.produce_b_turn(controlled=True,source_records_override=[source])
  restored=last_turn_generation(s)
  assert source["source_ref"] in restored.get("source_refs",[])
  restored_q=[x for x in restored.get("qualified_sources",[]) if x["source_ref"]==source["source_ref"]]
  assert restored_q and restored_q[0]["content"]["relation"]=="FACILITATES"
  assert r["actual_root_current_purpose_proved"] is False
  assert s.verify()["ok"] is True
 finally:s.close()


def test_hypothesis_absent_and_not_received_hold():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  no_h=s.run_experiment(declare=False)
  assert no_h["relevance"]["status"]=="OBJECT_RELEVANCE_HOLD"
  assert no_h["generation"] is None
  no_access=s.run_experiment(receive=False)
  assert no_access["relevance"]["status"]=="NOT_RECEIVED"
  assert no_access["generation"] is None
 finally:s.close()


def test_obstructing_offer_changes_relation_not_actor_action():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  r=s.run_experiment(permit=False)
  assert r["relevance"]["relation"]=="OBSTRUCTS"
  assert r["relevance"]["selected_action"] is None
  assert r["relevance"]["performed"] is False
  assert r["generation"]["selected_option"]==""
 finally:s.close()


def test_cold_reopen_reproduces_hypothesis_relevance_and_generation():
 import tempfile
 from pathlib import Path
 root=Path(tempfile.mkdtemp()); s=_start(root)
 try:
  r=s.run_experiment(); h=r["relevance"]["relevance_hash"]; g=r["generation"]["generation_hash"]
 finally:s.close()
 c=S51Session.open(root)
 try:
  rows=[x for x in c.product.store.episodes(c.branch_id) if x.get("kind")=="S51_OBJECT_RELEVANCE"]
  assert rows and rows[-1]["body"]["result"]["relevance_hash"]==h
  assert any(x.get("kind")=="S51_S49_CONSUMER_BINDING" for x in c.product.store.episodes(c.branch_id))
  assert any(x.get("kind")=="S49_B_ACTOR_TURN" for x in c.product.store.episodes(c.branch_id))
  assert c.verify()["ok"] is True
 finally:c.close()


def test_offer_and_access_are_the_actual_world_event():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  r=s.run_experiment(); offer_id=r["offer"]["event_id"]
  assert offer_id in {e["event_id"] for e in s.world().events}
  assert any(p["event_id"]==offer_id for p in s.product.store.perceptions(s.branch_id,"B"))
  assert r["access"]["event_ref"]==offer_id
  assert r["access"]["content"]["received_offer_event_id"]==offer_id
  assert r["access"]["content"]["material_event_id"]==r["offer"]["material_event_id"]
 finally:s.close()


def test_same_hypothesis_cannot_be_reused_for_a_second_offer():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  first=s.evaluate(obj,hyp,offer,access)
  assert first["status"]=="RELEVANCE_WARRANTED"
  assert s._hypothesis_status(hyp["hypothesis_id"])=="CONSUMED"
  second_offer=s.issue_offer(); second_access=s._offer_access(second_offer)
  second=s.evaluate(obj,hyp,second_offer,second_access)
  assert second["status"]=="OBJECT_RELEVANCE_HOLD"
  assert second["relation"]=="HYPOTHESIS_CONSUMED"
 finally:s.close()


def test_foreign_object_hypothesis_offer_access_and_relevance_are_refused():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  forged={"object_event_id":"FORGED_OBJECT","striving":"FORGED_STRIVING"}
  assert s.declare_hypothesis(forged)["status"]=="S51_FOREIGN_INPUT_REFUSED"
  rel=s.evaluate(forged,hyp,offer,access)
  assert rel["status"]=="OBJECT_RELEVANCE_HOLD" and rel["relation"]=="FOREIGN_INPUT"
  rel=s.evaluate(obj,{"hypothesis_id":"FORGED_HYPOTHESIS","status":"ACTIVE"},offer,access)
  assert rel["relation"]=="FOREIGN_INPUT"
  rel=s.evaluate(obj,hyp,{"offer_event_id":"FORGED_OFFER"},access)
  assert rel["relation"]=="FOREIGN_INPUT"
  rel=s.evaluate(obj,hyp,offer,{"access_status":"ACCESSIBLE","source_ref":"FORGED_ACCESS"})
  assert rel["relation"]=="FOREIGN_INPUT"
  consumed=s.consume_generation(obj,hyp,offer,access,{"relevance_hash":"FORGED_RELEVANCE"})
  assert consumed["selection_status"]=="S51_INPUT_REFUSED"
 finally:s.close()


def test_cold_foreign_relevance_episode_invalidates_verify():
 import tempfile
 from pathlib import Path
 root=Path(tempfile.mkdtemp()); s=_start(root)
 try:
  s.run_experiment()
 finally:s.close()
 c=S51Session.open(root)
 try:
  assert c.verify()["ok"] is True
  c._append("S51_OBJECT_RELEVANCE",{"schema":"FORGED","stage":"OBJECT_RELEVANCE","result":{"relation":"FORGED"}})
  assert c.verify()["ok"] is False
 finally:c.close()


def test_missing_free_hours_is_unknown_not_obstruction():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  world=s.world(); world.actor_state["B"]["free_hours"]=None
  s.product._checkpoint(s.branch_id,s.clock(),world)
  rel=s.evaluate(obj,hyp,offer,access)
  assert rel["relation"]=="UNKNOWN"
  assert rel["status"]=="RELEVANCE_WARRANTED"
  assert rel["selected_action"] is None and rel["performed"] is False
 finally:s.close()


def test_second_experiment_has_a_separate_declaration_and_no_false_active_extension():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  first=s.run_experiment(); second=s.run_experiment()
  assert first["hypothesis"]["hypothesis_id"]!=second["hypothesis"]["hypothesis_id"]
  assert s._hypothesis_status(first["hypothesis"]["hypothesis_id"])=="CONSUMED"
  assert s._hypothesis_status(second["hypothesis"]["hypothesis_id"])=="CONSUMED"
  assert s._active_hypothesis() is None
 finally:s.close()
