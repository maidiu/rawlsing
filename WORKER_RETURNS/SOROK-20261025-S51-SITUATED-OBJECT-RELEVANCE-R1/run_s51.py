"""Run one bounded retained-object relevance experiment on the S49 person."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
RETURN=Path(__file__).resolve().parent
if str(RETURN) not in sys.path: sys.path.insert(0,str(RETURN))
from s51.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s51.session import S51Session

def _start(state):
 c=case_for(True)
 return S51Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),language_context={"milieu_id":"workshop"})

def main():
 base=RETURN/"runtime"
 if base.exists(): shutil.rmtree(base)
 base.mkdir(parents=True); state=base/"actual"
 s=_start(state)
 try:
  actual=s.run_experiment()
  no_h=s.run_experiment(declare=False)
  obstruct=s.run_experiment(permit=False)
  no_access=s.run_experiment(receive=False)
  cold_state=state
  verify=s.verify()["ok"]
 finally: s.close()
 cold=S51Session.open(cold_state)
 try:
  cold_verify=cold.verify()["ok"]
  cold_eps=[x for x in cold.product.store.episodes(cold.branch_id) if x.get("kind")=="S51_OBJECT_RELEVANCE"]
  match=[x for x in cold_eps if x.get("episode_id")==actual["relevance"]["episode_id"]]
  cold_hash=match[-1]["body"]["result"]["relevance_hash"] if match else ""
 finally: cold.close()
 report={
  "schema":"SOROK_S51_RUN@1",
  "grade":"TEST_ONLY_S51_RETAINED_OBJECT_HYPOTHESIS_NOT_NATIVE",
  "native":False,
  "actual_root_current_purpose_proved":False,
  "object":{k:actual["object"].get(k) for k in ("object_event_id","striving","actor_id","effective_index","work_parent_event_id","project_parent_event_id")},
  "hypothesis":actual["hypothesis"],
  "offer":actual["offer"],
  "actual_relevance":actual["relevance"],
  "actual_generation":actual["generation"],
  "no_hypothesis":no_h["relevance"],
  "obstructing":obstruct["relevance"],
  "not_received":no_access["relevance"],
  "object_removed":no_h["relevance"].get("relation"),
  "cold":{"same_relevance_hash":cold_hash==actual["relevance"]["relevance_hash"],"verify_ok":cold_verify},
  "relevance_rule_id":"S51_OBJECT_RELEVANCE_TO_S49@1",
  "native_object_formation_needed":True,
  "actual_person_commit":False,
  "profile_prose_unchanged":True,
  "provider_calls":0,
  "verify_ok":verify and cold_verify,
 }
 print(json.dumps(report,indent=2,sort_keys=True))
 return 0 if report["verify_ok"] and report["cold"]["same_relevance_hash"] else 1
if __name__=="__main__": raise SystemExit(main())
