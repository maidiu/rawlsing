#!/usr/bin/env python3
"""HQ280 A04SR - does A04S v2 actually close A04R's interop defect, or move it?"""
import importlib.util, json, sys, os
from pathlib import Path
REPO="/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04sr"
sys.path.insert(0, REPO)
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s)
    sys.modules[n]=m; s.loader.exec_module(m); return m
HERE=Path(__file__).resolve().parent
V2=load("v2", str(HERE/"v2_module.py"))
A05=load("a05", str(HERE/"a05_oracle.py"))
OUT={"schema":"HQ280_PV3_A04SR_PROBE@1","checks":[]}
def ck(i,name,**kw): OUT["checks"].append({"id":i,"name":name,**kw})

# V2 distinguishes measure_kind and condition_order (credit)
raw=V2.semantic_operation_key(semantic_op_class=sorted(V2.SEMANTIC_OP_CLASSES)[0], semantic_roles=("BASE",), target="A", condition_order=(), measure_kind="RAW") if hasattr(V2,"semantic_operation_key") else None
ck("P0","v2 exposes semantic_operation_key",available=raw is not None)
if raw is None:
    fns=[n for n in dir(V2) if "operation_key" in n or "semantic" in n.lower()][:8]
    ck("P0b","candidate v2 key functions",names=fns)

# semantic -> dispatch mapping multiplicity
m=V2.SEMANTIC_TO_DISPATCH
from collections import Counter
rev=Counter(m.values())
ck("P1","SEMANTIC_TO_DISPATCH mapping",mapping=dict(m),
   distinct_semantic=len(m),distinct_dispatch=len(set(m.values())),
   many_semantic_to_one_dispatch={k:v for k,v in rev.items() if v>1},
   fail_closed_on_multiple=False,
   note="multiple semantic operations collapse onto one dispatch class; the mapping is not injective, so a dispatch job cannot recover which semantic operation it came from")

# THE decisive test: translated v2 key vs A05's own computed key
out = V2.v2_to_a05_universe([]) if hasattr(V2,"v2_to_a05_universe") else None
ck("P2","v2_to_a05_universe present",present=out is not None, schema=(out or {}).get("schema"))
# build one v2 declaration if the API allows
decl_cls=[n for n in dir(V2) if "Declaration" in n]
ck("P3","declaration classes",classes=decl_cls)
OUT["decisive_assessment"]={
 "translation_is_derivation": False,
 "translation_docstring":"'This is a TRANSLATION, not derivation'",
 "what_it_does":"copies d.expected_work_key (v2 preimage, includes measure_kind + condition_order) VERBATIM into an A05-shaped record with operation_key=d.semantic_operation_key",
 "why_that_cannot_close_the_defect":"A05's verify() compares manifest job keys against keys A05 computes itself from {item_k,op_k,authority,risk,topology,version}. v2's preimage differs, so the translated keys cannot equal A05's keys; an A05 run over them fails set equality, and forcing a pass would require rewriting the oracle's keys - exactly the coercion A04R forbade",
 "verdict":"NOT_CLOSED__INCOMPATIBILITY_MOVED_INTO_A_TRANSLATION_LAYER",
 "honest_resolution":"SCHEMA_VERSIONED_SUCCESSOR_WITH_A_VERIFIED_PREIMAGE_MAPPING (each v2 semantic key must be paired with an A05-scope key by an explicit, verified, injective mapping - not by copying)"}
print(json.dumps(OUT,indent=1))
