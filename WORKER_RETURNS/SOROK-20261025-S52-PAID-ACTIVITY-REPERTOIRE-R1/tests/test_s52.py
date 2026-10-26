"""Focused S52 paid-activity repertoire tests."""
from __future__ import annotations
import tempfile
from pathlib import Path
from s52.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s51.session import S51Refusal
from s52.session import PAID_OPTION, S52Session


def _start(state):
 c=case_for(True)
 return S52Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),
  language_context={"milieu_id":"workshop"})


def test_paid_candidate_and_conditional_reason_enter_normal_generation():
 s=_start(tempfile.mkdtemp())
 try:
  r=s.run_experiment()
  gen=r["generation"]; receipt=gen.get("generation_receipt") or {}
  assert r["candidate"]["status"]=="CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"
  assert receipt["selection_status"]=="OPEN_CHOICE_SET"
  assert receipt["selected_option"]==""
  assert PAID_OPTION in [o["option_id"] for o in receipt["options"]]
  assert PAID_OPTION in receipt["eligible_options"]
  paid_reasons=[x for x in receipt["reasons"] if x["option_id"]==PAID_OPTION]
  assert paid_reasons and paid_reasons[0]["relation"]=="CONDITIONAL_SUPPORTS"
  assert paid_reasons[0]["source_ref"]==r["candidate"]["source_ref"]
  assert receipt["repertoire"]["candidate_hash"]==r["candidate"]["candidate_hash"]
  assert not r["candidate"]["performed"]
  assert s.verify()["ok"] is True
 finally:s.close()


def test_candidate_source_cut_removes_paid_option_from_normal_generation():
 s=_start(tempfile.mkdtemp())
 try:
  r=s.run_experiment(); candidate=r["candidate"]
  def last_receipt(session):
   turns=[row for row in session._episodes("S49_B_ACTOR_TURN")
    if (row.get("body") or {}).get("generation")]
   return turns[-1]["body"]["generation"]["generation"]
  s.produce_b_turn(controlled=True,source_records_override=[candidate["source"]])
  cut_receipt=last_receipt(s)
  assert PAID_OPTION not in [o["option_id"] for o in cut_receipt.get("options",[])]
  s.produce_b_turn(controlled=True,source_records_override=[candidate["source"]],
   repertoire=candidate["repertoire"])
  restored_receipt=last_receipt(s)
  assert PAID_OPTION in [o["option_id"] for o in restored_receipt.get("options",[])]
  assert [x for x in restored_receipt.get("reasons",[]) if x["option_id"]==PAID_OPTION]
 finally:s.close()


def test_inaccessible_or_obstructing_offer_has_no_positive_paid_reason():
 s=_start(tempfile.mkdtemp())
 try:
  no_access=s.run_experiment(receive=False)
  assert no_access["generation"] is None
  obstruct=s.run_experiment(permit=False)
  assert obstruct["candidate"]["recruited"] is False
  receipt=obstruct["generation"]["generation_receipt"]
  assert PAID_OPTION not in receipt["eligible_options"]
  assert not [x for x in receipt["reasons"] if x["option_id"]==PAID_OPTION]
 finally:s.close()


def test_blocked_physical_state_is_not_recruited_and_no_side_effect():
 s=_start(tempfile.mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  rel=s.evaluate(obj,hyp,offer,access)
  world=s.world(); world.actor_state["B"]["free_hours"]=0
  s.product._checkpoint(s.branch_id,s.clock(),world)
  cand=s.compile_candidate(obj,hyp,offer,access,rel)
  assert cand["status"]=="BLOCKED"
  assert cand["recruited"] is False
  assert cand["performed"] is False
 finally:s.close()


def test_controlled_port_performs_current_state_effects_and_denies_without_counterpart():
 s=_start(tempfile.mkdtemp())
 try:
  r=s.run_experiment(); candidate=r["candidate"]; generation=r["generation"]
  denied=s.perform_paid_participation(candidate,generation=generation,
   counterpart_performed=False)
  assert denied["performed"] is False
  assert denied["status"]=="CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"
  before=dict(s.world().actor_state["B"])
  ok=s.perform_paid_participation(candidate,generation=generation,
   counterpart_performed=True)
  after=dict(s.world().actor_state["B"])
  assert ok["performed"] is True
  assert ok["generation_hash"]==generation["generation_hash"]
  assert after["cash"]==before["cash"]+candidate["task_parameters"]["payment_per_actor"]
  assert after["free_hours"]==before["free_hours"]-candidate["task_parameters"]["task_hours"]
  assert after["completed_units"]==before["completed_units"]+candidate["task_parameters"]["material_units"]
  assert ok["world_event_id"] in {e["event_id"] for e in s.world().events}
  duplicate=s.perform_paid_participation(candidate,generation=generation,
   counterpart_performed=True)
  assert duplicate["performed"] is False and duplicate["reason"]=="S52_DUPLICATE_PARTICIPATION"
 finally:s.close()


def test_cold_replay_preserves_candidate_generation_and_controlled_effect():
 root=Path(tempfile.mkdtemp()); s=_start(root)
 try:
  r=s.run_experiment(); candidate=r["candidate"]; generation=r["generation"]
  ok=s.perform_paid_participation(candidate,generation=generation,counterpart_performed=True)
  before_after=(ok["before"],ok["after"])
 finally:s.close()
 c=S52Session.open(root)
 try:
  candidates=[x for x in c.product.store.episodes(c.branch_id) if x.get("kind")=="S52_PAID_CANDIDATE"]
  assert candidates and candidates[-1]["body"]["candidate_hash"]==candidate["candidate_hash"]
  results=[x for x in c.product.store.episodes(c.branch_id) if x.get("kind")=="S52_PAID_ACTIVITY_RESULT"]
  assert results and results[-1]["body"]["after"]==before_after[1]
  assert c.verify()["ok"] is True
 finally:c.close()


def test_unknown_free_hours_is_unknown_not_a_positive_reason():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  rel=s.evaluate(obj,hyp,offer,access)
  world=s.world(); world.actor_state["B"]["free_hours"]=None
  s.product._checkpoint(s.branch_id,s.clock(),world)
  cand=s.compile_candidate(obj,hyp,offer,access,rel)
  assert cand["status"]=="UNKNOWN"
  assert cand["recruited"] is False
  assert not (cand.get("repertoire") or {}).get("reason")
 finally:s.close()


def test_foreign_or_stale_offer_cannot_compile_a_paid_candidate():
 s=_start(__import__('tempfile').mkdtemp())
 try:
  obj=s.recover_object(); hyp=s.declare_hypothesis(obj)
  offer=s.issue_offer(); access=s._offer_access(offer)
  rel=s.evaluate(obj,hyp,offer,access)
  forged={"episode_id":"FORGED_STALE_OFFER"}
  try:
   s.compile_candidate(obj,hyp,forged,access,rel)
  except S51Refusal:
   pass
  else:
   raise AssertionError("foreign offer accepted")
 finally:s.close()
