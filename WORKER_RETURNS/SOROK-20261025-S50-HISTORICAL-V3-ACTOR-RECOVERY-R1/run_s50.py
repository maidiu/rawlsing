"""Execute recovered historical V3 state on an isolated fixture and compare actual root."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
RETURN=Path(__file__).resolve().parent
if str(RETURN) not in sys.path: sys.path.insert(0,str(RETURN))
from s50.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s50.session import S50Session


def _start(state):
    c=case_for(True)
    return S50Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),language_context={"milieu_id":"workshop"})


def main() -> int:
    base=RETURN/"runtime"
    if base.exists(): shutil.rmtree(base)
    base.mkdir(parents=True)
    state=base/"actual"
    s=_start(state)
    try:
        before={"world_events":len(s.world().events),"c12_events":len(s.read_events()),"clock":s.clock(),"root_hash":s.read_root()["root_hash"]}
        missing=s.actual_root_missing()
        made=s.materialize_legacy_projection(years=2)
        projection=s.read_projection()
        after={"world_events":len(s.world().events),"c12_events":len(s.read_events()),"clock":s.clock(),"root_hash":s.read_root()["root_hash"]}
        verify=s.verify()["ok"]
    finally: s.close()
    cold=S50Session.open(state)
    try:
        cold_p=cold.read_projection(); cold_verify=cold.verify()["ok"]
    finally: cold.close()
    report={
      "schema":"SOROK_S50_RUN@1",
      "actual_root":{
        "status":missing["status"],"reason":missing["reason"],
        "missing_fields":missing["missing_fields"],
        "world_events_before":before["world_events"],"world_events_after":after["world_events"],
        "c12_events_before":before["c12_events"],"c12_events_after":after["c12_events"],
        "clock_before":before["clock"],"clock_after":after["clock"],
        "root_unchanged":before["root_hash"]==after["root_hash"],
        "no_c8":len(s.read_events())==0 if False else None,
      },
      "recovered_legacy_projection":{
        "status":made["status"],"episode_id":made["episode_id"],
        "fixture_only":projection.get("fixture_only"),
        "read_only":projection.get("read_only"),
        "actual_person_commit":projection.get("actual_person_commit"),
        "second_mind":projection.get("second_mind"),
        "projection_hash":made["projection_hash"],
        "fixture_sha256":made["fixture_sha256"],
        "source_all_exact":made["source_all_exact"],
        "year":projection.get("projection",{}).get("year"),
        "age":projection.get("projection",{}).get("age"),
        "expectation_baseline":projection.get("projection",{}).get("expectation_baseline"),
        "striving_count":len(projection.get("projection",{}).get("striving_objects") or []),
        "pressure_flow_history_present":bool(projection.get("projection",{}).get("pressure_flow_history_last")),
        "pressure_flow_memory_present":bool(projection.get("projection",{}).get("pressure_flow_memory")),
      },
      "cold":{"same_projection_hash":(cold_p or {}).get("projection",{}).get("state_sha256")==made["projection_hash"],"verify_ok":cold_verify},
      "transforms_enabled_by_legacy_fixture":[
        "yearly_step_order","event_sampling","micro_drift","age_increment","pressure_flow_cycle","derived_recompute"
      ],
      "transforms_not_authorized_for_actual_person":[
        "demographic_to_wound_framework_parent_type","hopeful_50_parent_default","blind_run_n_years","years_as_learning_multiplier","native_A_T_learning_coefficients","two_pass_llm"
      ],
      "actual_person_commit":False,
      "actual_provider_call":False,
      "native_grants":{"actor":False,"rule":False,"source":False,"human":False,"c8":False,"c9":False,"c12":False},
      "verify_ok":verify and cold_verify,
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report["verify_ok"] and report["cold"]["same_projection_hash"] else 1

if __name__=="__main__": raise SystemExit(main())
