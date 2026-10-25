"""S49 independent B producer: actual root hold and controlled role test."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
RETURN=Path(__file__).resolve().parent
if str(RETURN) not in sys.path: sys.path.insert(0,str(RETURN))
from s49.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s49.session import S49Session

def _start(state):
    c=case_for(True)
    return S49Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),language_context={"milieu_id":"workshop"})

def main() -> int:
    base=RETURN/"runtime"
    if base.exists(): shutil.rmtree(base)
    base.mkdir(parents=True)
    actual_state=base/"actual"; controlled_state=base/"controlled"
    actual=_start(actual_state)
    try:
        before=(len(actual.world().events),actual.clock(),len(actual.read_events()))
        actual_result=actual.produce_b_turn(controlled=False)
        actual_after=(len(actual.world().events),actual.clock(),len(actual.read_events()))
        actual_verify=actual.verify()["ok"]
    finally: actual.close()
    controlled=_start(controlled_state)
    try:
        result=controlled.produce_b_turn(controlled=True)
        c9=controlled.read_c9_conditioning(result["event_ref"]) if result.get("event_ref") else None
        controlled_verify=controlled.verify()["ok"]
    finally: controlled.close()
    cold=S49Session.open(controlled_state)
    try:
        cold_turns=cold.b_turns(); cold_verify=cold.verify()["ok"]
    finally: cold.close()
    report={
      "schema":"SOROK_S49_RUN@1",
      "actual_root":{
        "status":actual_result.get("stage"),"reason":actual_result.get("reason"),
        "missing_context":actual_result.get("reason"),
        "world_events_before":before[0],"world_events_after":actual_after[0],
        "clock_before":before[1],"clock_after":actual_after[1],
        "c12_events_before":before[2],"c12_events_after":actual_after[2],
        "event_ref":actual_result.get("event_ref",""),"verify_ok":actual_verify,
        "source_grade":"UNAVAILABLE_CURRENT_B_ACTOR_OWNED_CONTEXT",
      },
      "controlled_b":{
        "status":result.get("status"),"controlled":True,
        "b_actor":result.get("attempt",{}).get("actor_id"),
        "option_id":result.get("attempt",{}).get("option_id"),
        "attempt_status":result.get("attempt",{}).get("status"),
        "attempt_performed":result.get("attempt",{}).get("performed"),
        "source_operation":result.get("b_source_operation"),
        "b_source_event_ref":result.get("b_source_event_ref"),
        "event_ref":result.get("event_ref"),"event_ordinal":result.get("event_ordinal"),
        "target_proposals":result.get("target_proposals",[]),
        "c9":c9,"verify_ok":controlled_verify,
        "source_grade":"TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE",
      },
      "cold":{
        "s49_turns":len(cold_turns),"same_canonical_store":True,
        "verify_ok":cold_verify,
      },
      "actual_provider_call":False,
      "native_grants":{"actor":False,"rule":False,"source":False,"human":False,"c8":False,"c9":False,"c12":False},
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report["actual_root"]["verify_ok"] and report["controlled_b"]["verify_ok"] else 1

if __name__=="__main__": raise SystemExit(main())
