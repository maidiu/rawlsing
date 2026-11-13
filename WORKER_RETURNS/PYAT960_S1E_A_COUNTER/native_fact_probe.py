#!/usr/bin/env python3
"""Actual Q2 direct-I02 -> native I03/Batch canary fact on the Linux s2b host."""
from __future__ import annotations
import json, os, sys, tempfile
from copy import deepcopy
from pathlib import Path
ROOT = Path(os.environ.get("Q2_PROBE_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, build_governed_c11_projection, build_validated_c11_release_from_config, decode_fixture_config
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _branch_predicate, _query, _run

def _doc(f):
    d=deepcopy(f["document"])
    for s in d["authority"]["snapshots"]:
        if s["authority_id"]=="S1B-ROUTING-AUTH": s["authority_kind"]="ROUTING_RISK_SET"
    for slot in d["response_slots"]:
        for v in slot["values"]:
            if v.get("raw_value") in (0.0,1.0): v["canonical_value"]=str(int(v["raw_value"]))
    return d

def _one(root,f,document,name,members=None):
    config=SourceConfig(document)
    handoff=build(root,f,name=name,config=config)
    inc=decode_fixture_config(config,f["path"])
    try: legacy=build_validated_c11_release_from_config(config,incidence=inc,batch_size=4)
    finally: inc.close()
    p=build_governed_c11_projection(config)
    source={"universe":p.universes[0],"respondents":{r.ref.key:r for r in p.respondents},
            "qrefs":{"q101":p.questions[0].native_question_ref},
            "risk_refs":{"R":p.routing[0].risk_set_ref},
            "authorities":p.authority_snapshots,"source_auth":p.authority_snapshots[0],
            "repo":C11Repository((legacy,)),"release_ref":legacy.release_ref}
    qa=_query_authority("q2-native"); pred=_branch_predicate(source,qa,members=members,tag="q2-native")
    query=_query(source,qa,pred,("q101",),tag="q2-native",target_authority_refs=(p.questions[0].semantic_authority_ref,))
    reader=open_direct_native_i03(handoff,source["repo"],legacy.release_ref)
    try: result=_run(source,qa,pred,query)
    finally: reader.close()
    return result.facts[0], handoff

def main():
    if not os.path.isdir("/proc/self/fd"):
        print(json.dumps({"host":"non_linux","state":"HOLD_DEPENDENCY"})); return 0
    root=Path(tempfile.mkdtemp(prefix="q2-native-fact-probe-")); f=source_fixture(root/"native",values=(0.0,1.0,0.0,1.0,0.0)); doc=_doc(f)
    base,bh=_one(root/"native",f,doc,"base.sqlite")
    rows=tuple(sorted(build_governed_c11_projection(SourceConfig(doc)).respondents,key=lambda r:r.respondent_key))
    changed,_=_one(root/"native",f,deepcopy(doc),"changed.sqlite",members=rows[:3])
    restored,rh=_one(root/"native",f,deepcopy(doc),"restored.sqlite")
    def view(fact):
        return {"ref":fact.ref.key,"typed_state":fact.typed_state,
                "failure":fact.semantic_fields.get("p02_failure_state"),
                "detail":fact.semantic_fields.get("execution_detail"),
                "raw":(fact.semantic_fields.get("raw_numerator_support"),fact.semantic_fields.get("raw_denominator_support"))}
    print(json.dumps({"host":"linux_proc_self_fd","base":view(base),"changed":view(changed),"restored":view(restored),
        "restored_ref_equals_base":restored.ref==base.ref,"base_roots":{"logical":bh.roots.logical,"physical":bh.roots.physical},
        "restored_roots_equal":rh.roots.logical==bh.roots.logical,
        "engineering_fixture_correction":["routing authority kind ROUTING_RISK_SET","canonical values 0/1 match query domain"],"claims":"TEST_ONLY sourcefree canary; not original35 science"},indent=2))
    return 0
raise SystemExit(main())
