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
  assert r["hypothesis"]["status"]=="ACTIVE"
  assert r["offer"]["event_id"]
  assert r["access"]["access_status"]=="ACCESSIBLE"
  assert r["relevance"]["relation"]=="FACILITATES"
  assert r["relevance"]["object_event_id"]==obj["object_event_id"]
  assert r["generation"]["source_ref"].startswith("S51_SOURCE_")
  assert any(x.get("predicate")=="S51_OBJECT_RELEVANCE" for x in r["generation"]["reasons"])
  assert r["generation"]["selected_option"]==""  # qualified open, no invented winner
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
  assert any(x.get("kind")=="S51_S49_CONSUMER" for x in c.product.store.episodes(c.branch_id))
  assert c.verify()["ok"] is True
 finally:c.close()
