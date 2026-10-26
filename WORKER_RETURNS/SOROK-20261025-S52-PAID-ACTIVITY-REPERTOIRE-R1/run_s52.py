"""Run one bounded S52 paid-activity repertoire experiment."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
RETURN=Path(__file__).resolve().parent
if str(RETURN) not in sys.path: sys.path.insert(0,str(RETURN))
from s52.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s52.session import PAID_OPTION, S52Session

def _start(state):
 c=case_for(True)
 return S52Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),
  language_context={"milieu_id":"workshop"})

def _last_receipt(session):
 turns=[row for row in session._episodes("S49_B_ACTOR_TURN")
  if (row.get("body") or {}).get("generation")]
 return dict(turns[-1]["body"]["generation"].get("generation") or {})

def main():
 base=RETURN/"runtime"
 if base.exists(): shutil.rmtree(base)
 base.mkdir(parents=True); state=base/"actual"
 s=_start(state)
 try:
  actual=s.run_experiment()
  candidate=actual["candidate"]; generation=actual["generation"]
  receipt=generation.get("generation_receipt") or {}
  cut_source=candidate["source"]
  s.produce_b_turn(controlled=True,source_records_override=[cut_source])
  cut_receipt=_last_receipt(s)
  s.produce_b_turn(controlled=True,source_records_override=[cut_source],
   repertoire=candidate["repertoire"])
  restored_receipt=_last_receipt(s)
  denied=s.perform_paid_participation(candidate,generation=generation,
   counterpart_performed=False)
  before=dict(s.world().actor_state["B"])
  controlled=s.perform_paid_participation(candidate,generation=generation,
   counterpart_performed=True)
  after=dict(s.world().actor_state["B"])
  verify=s.verify()["ok"]
 finally: s.close()
 cold=S52Session.open(state)
 try:
  cold_verify=cold.verify()["ok"]
  cold_candidates=[x for x in cold.product.store.episodes(cold.branch_id)
   if x.get("kind")=="S52_PAID_CANDIDATE"]
  cold_matches=bool(cold_candidates and
   cold_candidates[-1]["body"].get("candidate_hash")==candidate["candidate_hash"])
 finally: cold.close()
 report={
  "schema":"SOROK_S52_RUN@1",
  "grade":"TEST_ONLY_S52_PAID_ACTIVITY_REPERTOIRE_NOT_NATIVE",
  "native":False,"actual_current_purpose_proved":False,
  "object_event_id":candidate["object_event_id"],
  "offer_event_id":candidate["offer_event_id"],
  "candidate":{k:candidate.get(k) for k in ("candidate_hash","status",
   "objective_feasibility","reason","recruited","counterpart_status",
   "prospective_payment","earned_payment","source_ref")},
  "generation":{
   "selection_status":receipt.get("selection_status"),
   "selected_option":receipt.get("selected_option"),
   "eligible_options":receipt.get("eligible_options"),
   "options":receipt.get("options"),
   "reasons":[x for x in receipt.get("reasons",[]) if x.get("option_id")==PAID_OPTION],
   "repertoire":receipt.get("repertoire"),
  },
  "source_cut":{
   "paid_option_absent":PAID_OPTION not in [o.get("option_id") for o in cut_receipt.get("options",[])],
   "paid_option_restored":PAID_OPTION in [o.get("option_id") for o in restored_receipt.get("options",[])],
   "reason_restored":bool([x for x in restored_receipt.get("reasons",[]) if x.get("option_id")==PAID_OPTION]),
  },
  "controlled":{
   "denied":{k:denied.get(k) for k in ("status","performed","reason")},
   "performed":{k:controlled.get(k) for k in ("status","performed","reason","world_event_id","payment_earned")},
   "cash_before":before.get("cash"),"cash_after":after.get("cash"),
   "free_hours_before":before.get("free_hours"),"free_hours_after":after.get("free_hours"),
   "completed_before":before.get("completed_units"),"completed_after":after.get("completed_units"),
  },
  "cold":{"candidate_match":cold_matches,"verify_ok":cold_verify},
  "verify_ok":bool(verify and cold_verify and cold_matches),
  "missing_option_relation":"PAID_PARTICIPATION compiled as a conditional current-state alternative; no independent counterpart or generated attempt is fabricated",
  "provider_calls":0,
 }
 print(json.dumps(report,indent=2,sort_keys=True))
 return 0 if report["verify_ok"] else 1
if __name__=="__main__": raise SystemExit(main())
