#!/usr/bin/env python3
"""FFX002-R2 mechanical execution harness. Never mints authority or runs empirical arms."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from typing import Any, Iterable, Mapping

DESIGN_REF="5343862783959a1455735c0a5eb7b330c76f42d5"
SCHEMA_VERSION="FFX002_R2_COMMON_SEMANTIC_INPUT_MANIFEST@1"
ARMS={"A":"EXACT_CONFIGURATION_SET","B":"LOCAL_GEOMETRIC","C":"DIRECT_CONDITIONAL_REDISTRIBUTION",
      "D":"MEASUREMENT_INCIDENCE_GRAPH_HYPERGRAPH","E":"MOTIF","F":"LATENT_PROFILE_MODEL"}
CORE=("A","B","C")
REQUIRED=("manifest_schema_version","current_execution_sha","observation_substrate_ref",
"respondent_entity_binding_ref","exposure_risk_set_ref","source_scope_ref","source_native_measurement_refs",
"qimpl_measurement_binding_refs","response_state_semantics_ref","special_state_semantics_ref",
"ttar_execution_sequence","post_transform_state_manifest","claim_scope_ref","estimand_ref","weight_design_refs",
"analytic_role_authority_refs","ancestry_disjointness_receipt","unresolved_noncomparable_manifest",
"source_native_ancestry_ref","loss_profile","holdout_generation_inputs_hash","canonicalization_spec","manifest_hash")
SET_PATHS=frozenset(("/source_native_measurement_refs","/qimpl_measurement_binding_refs",
                     "/weight_design_refs","/analytic_role_authority_refs"))
CANON={"spec_id":"FFX002_R2_CANONICAL_JSON_SHA256_V1","encoding":"UTF-8",
       "object_key_order":"SORTED_LEXICOGRAPHIC","semantic_array_order":"PRESERVE",
       "set_array_order":"SORT_BY_IMMUTABLE_ID_THEN_CANONICAL_ITEM","set_array_paths":sorted(SET_PATHS),
       "typed_null_empty_distinct":True,"forbid_nonsemantic_timestamps":True,
       "hash_algorithm":"sha256","excluded_top_level_hash_fields":["manifest_hash"]}
BINDINGS=REQUIRED[2:20]
LOSS={"PRESERVED","PRESERVED_BY_CONSTRUCTION","PRESERVES_APPROXIMATELY","APPROXIMATED","LOST",
      "MAY_DESTROY","DOES_NOT_REPRESENT","REQUIRES_SEPARATE_TEST","UNKNOWN"}
MATERIAL={"NOT_MATERIAL","MATERIAL","CRITICAL","NOT_APPLICABLE","UNASSESSED"}
PLACE={"","<REF>","<REFS>","<REF/HASH>","<REFS/NONE>","TBD","TODO","MISSING","UNBOUND","UNKNOWN_REF"}

class HarnessViolation(ValueError):
    def __init__(self,state:str,detail:str=""):
        self.state,self.detail=state,detail
        super().__init__(f"{state}: {detail}" if detail else state)

def _clone(v:Any)->Any:
    try:return json.loads(json.dumps(v,ensure_ascii=False,allow_nan=False))
    except (TypeError,ValueError) as e:raise HarnessViolation("HARNESS_NONCANONICAL_JSON_VALUE",str(e)) from e

def _hex(v:Any,n:int,field:str)->str:
    if not isinstance(v,str) or len(v)!=n:raise HarnessViolation("HARNESS_INVALID_HASH",field)
    try:int(v,16)
    except ValueError as e:raise HarnessViolation("HARNESS_INVALID_HASH",field) from e
    return v.lower()

def _placeholder(v:Any)->bool:
    if isinstance(v,str): return v.strip() in PLACE or (v.strip().startswith("<") and v.strip().endswith(">"))
    if isinstance(v,list): return not v or any(_placeholder(x) for x in v)
    if isinstance(v,dict):
        if not v:return True
        return any(k in v and _placeholder(v[k]) for k in ("id","ref","authority_ref","immutable_id"))
    return v is None

def _identity(v:Any)->str:
    if isinstance(v,str):return v
    if isinstance(v,dict):
        for k in ("immutable_id","id","ref","authority_ref","measurement_id","qimpl_id","state_id"):
            if isinstance(v.get(k),str) and v[k]:return f"{k}:{v[k]}"
    raise HarnessViolation("HARNESS_SET_ITEM_IMMUTABLE_ID_MISSING")

def _norm(v:Any,path:str="")->Any:
    if isinstance(v,dict):return {k:_norm(v[k],path+"/"+k) for k in sorted(v)}
    if isinstance(v,list):
        a=[_norm(x,path+f"/{i}") for i,x in enumerate(v)]
        if path in SET_PATHS:a.sort(key=lambda x:(_identity(x),json.dumps(x,sort_keys=True,separators=(",",":"))))
        return a
    if isinstance(v,float) and not math.isfinite(v):raise HarnessViolation("HARNESS_NONCANONICAL_JSON_VALUE","nonfinite")
    return v

def canonical_bytes(payload:Mapping[str,Any],exclude:Iterable[str]=())->bytes:
    x=_clone(dict(payload))
    for k in exclude:x.pop(k,None)
    return json.dumps(_norm(x),ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def hash_payload(payload:Mapping[str,Any],exclude:Iterable[str]=())->str:
    return hashlib.sha256(canonical_bytes(payload,exclude)).hexdigest()

def compute_common_hash(m:Mapping[str,Any])->str:
    if m.get("canonicalization_spec",CANON)!=CANON:raise HarnessViolation("COMMON_INPUT_CANONICALIZATION_SPEC_DIVERGENCE")
    return hash_payload(m,("manifest_hash",))

def compile_common_manifest(source:Mapping[str,Any])->dict[str,Any]:
    m=_clone(dict(source));m.pop("manifest_hash",None);m.setdefault("canonicalization_spec",_clone(CANON))
    expected=set(REQUIRED)-{"manifest_hash"}
    if set(m)!=expected:
        miss=expected-set(m);extra=set(m)-expected
        raise HarnessViolation("COMMON_INPUT_SCHEMA_SHAPE",f"missing={sorted(miss)} extra={sorted(extra)}")
    if m["manifest_schema_version"]!=SCHEMA_VERSION:raise HarnessViolation("COMMON_INPUT_SCHEMA_VERSION_MISMATCH")
    _hex(m["current_execution_sha"],40,"current_execution_sha");_hex(m["holdout_generation_inputs_hash"],64,"holdout_generation_inputs_hash")
    if m["canonicalization_spec"]!=CANON:raise HarnessViolation("COMMON_INPUT_CANONICALIZATION_SPEC_DIVERGENCE")
    for f in BINDINGS:
        if f in ("ttar_execution_sequence","weight_design_refs") and m[f]=="NONE":continue
        if _placeholder(m[f]):raise HarnessViolation("COMMON_INPUT_UNRESOLVED_AUTHORITY",f)
    m["manifest_hash"]=compute_common_hash(m);return validate_common_manifest(m)

def validate_common_manifest(m:Mapping[str,Any])->dict[str,Any]:
    x=_clone(dict(m))
    if set(x)!=set(REQUIRED):raise HarnessViolation("COMMON_INPUT_SCHEMA_SHAPE")
    if x["manifest_schema_version"]!=SCHEMA_VERSION or x["canonicalization_spec"]!=CANON:raise HarnessViolation("COMMON_INPUT_SCHEMA_VERSION_MISMATCH")
    for f in BINDINGS:
        if not (f in ("ttar_execution_sequence","weight_design_refs") and x[f]=="NONE") and _placeholder(x[f]):
            raise HarnessViolation("COMMON_INPUT_UNRESOLVED_AUTHORITY",f)
    if _hex(x["manifest_hash"],64,"manifest_hash")!=compute_common_hash(x):raise HarnessViolation("COMMON_INPUT_ARM_HASH_DIVERGENCE")
    return x

def attest_arm(arm_id:str,received:Mapping[str,Any])->dict[str,Any]:
    if arm_id not in ARMS:raise HarnessViolation("HARNESS_UNKNOWN_ARM",arm_id)
    r=received.get("manifest_hash");h=compute_common_hash(received);ok=isinstance(r,str) and r.lower()==h
    return {"schema_version":"FFX002_R2_ARM_HASH_ATTESTATION@1","arm_id":arm_id,"view_family":ARMS[arm_id],
            "received_manifest_hash":r,"recomputed_manifest_hash":h,
            "attestation_status":"ATTESTED_EQUAL" if ok else "COMMON_INPUT_ARM_HASH_DIVERGENCE"}

def reject_fork_semantic_tamper(expected:Mapping[str,Any],received:Mapping[str,Any],arm_id:str)->dict[str,Any]:
    e=validate_common_manifest(expected);a=attest_arm(arm_id,received)
    if a["attestation_status"]!="ATTESTED_EQUAL" or a["recomputed_manifest_hash"]!=e["manifest_hash"]:
        raise HarnessViolation("EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE",arm_id)
    return a

def holdout_inputs(unit_ids:Iterable[str],seed:str,basis_points:int,code_version_ref:str,tolerances:Mapping[str,Any]|None=None)->dict[str,Any]:
    ids=sorted(set(map(str,unit_ids)))
    if not ids or not seed or not 0<basis_points<10000 or not code_version_ref:raise HarnessViolation("EXPERIMENT_INVALID__HOLDOUT")
    return {"partition_algorithm":"SHA256_BASIS_POINTS_V1","unit_ids":ids,"seed":seed,"holdout_basis_points":basis_points,
            "code_version_ref":code_version_ref,"tolerances":_clone(dict(tolerances or {}))}

def freeze_holdout(common:Mapping[str,Any],inputs:Mapping[str,Any])->dict[str,Any]:
    c=validate_common_manifest(common);i=_clone(dict(inputs));ih=hash_payload(i)
    if ih!=c["holdout_generation_inputs_hash"]:raise HarnessViolation("EXPERIMENT_INVALID__HOLDOUT","input hash")
    design,final,rows=[],[],[]
    for uid in i["unit_ids"]:
        b=int.from_bytes(hashlib.sha256(f"{i['seed']}\0{uid}".encode()).digest()[:8],"big")%10000
        s="FINAL_HOLDOUT" if b<i["holdout_basis_points"] else "DESIGN";(final if s=="FINAL_HOLDOUT" else design).append(uid)
        rows.append({"unit_id":uid,"bucket":b,"split":s})
    out={"schema_version":"FFX002_R2_HOLDOUT_MANIFEST@1","common_manifest_hash":c["manifest_hash"],
         "holdout_generation_inputs_hash":ih,"generation_inputs":i,"design_unit_ids":design,"final_holdout_unit_ids":final,
         "partition_hash":hash_payload({"assignments":rows})}
    out["holdout_manifest_hash"]=hash_payload(out);return out

def _verified(a:Mapping[str,Any],field:str,state:str)->str:
    x=_clone(dict(a));sup=_hex(x.pop(field,None),64,field);exp=hash_payload(x)
    if sup!=exp:raise HarnessViolation(state,field)
    return sup

def freeze_queries(common:Mapping[str,Any],holdout:Mapping[str,Any],rows:Iterable[Mapping[str,Any]])->dict[str,Any]:
    c=validate_common_manifest(common);hh=_verified(holdout,"holdout_manifest_hash","EXPERIMENT_INVALID__HOLDOUT")
    if holdout.get("common_manifest_hash")!=c["manifest_hash"]:raise HarnessViolation("EXPERIMENT_INVALID__HOLDOUT","binding")
    q=sorted((_clone(dict(x)) for x in rows),key=lambda x:x["query_id"])
    if not q or len({x["query_id"] for x in q})!=len(q):raise HarnessViolation("HARNESS_QUERY_MANIFEST_INVALID")
    out={"schema_version":"FFX002_R2_QUERY_MANIFEST@1","design_ref":DESIGN_REF,"common_manifest_hash":c["manifest_hash"],
         "holdout_manifest_hash":hh,"queries":q};out["query_manifest_hash"]=hash_payload(out);return out

def _method(m:Mapping[str,Any])->dict[str,Any]:
    x=_clone(dict(m))
    for f in x.get("preprocessing_functions",[]):
        cls=f.get("classification")
        if cls not in {"IDENTITY_PRESERVING_METHOD","AUTHORIZED_PREFORK_TRANSFORM_ALREADY_IN_MANIFEST",
                       "FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM"}:raise HarnessViolation("HARNESS_METHOD_MANIFEST_INVALID")
        if cls=="FORBIDDEN_UNDECLARED_SEMANTIC_TRANSFORM":raise HarnessViolation("EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE")
    return x

def dispatch(arm_id:str,common:Mapping[str,Any],holdout:Mapping[str,Any],queries:Mapping[str,Any],method:Mapping[str,Any])->dict[str,Any]:
    c=validate_common_manifest(common);att=reject_fork_semantic_tamper(c,c,arm_id)
    hh=_verified(holdout,"holdout_manifest_hash","EXPERIMENT_INVALID__HOLDOUT");qh=_verified(queries,"query_manifest_hash","HARNESS_QUERY_MANIFEST_HASH_DIVERGENCE")
    if holdout.get("common_manifest_hash")!=c["manifest_hash"] or queries.get("common_manifest_hash")!=c["manifest_hash"] or queries.get("holdout_manifest_hash")!=hh:
        raise HarnessViolation("COMMON_INPUT_ARM_HASH_DIVERGENCE")
    mm=_method(method);out={"schema_version":"FFX002_R2_ARM_DISPATCH_ENVELOPE@1","arm_id":arm_id,"view_family":ARMS[arm_id],
      "common_semantic_input_manifest":c,"common_manifest_hash":c["manifest_hash"],"arm_hash_attestation":att,
      "holdout_manifest_hash":hh,"query_manifest_hash":qh,"method_manifest":mm,"method_manifest_hash":hash_payload(mm)}
    out["dispatch_hash"]=hash_payload(out);return out

def loss_receipt(arm_id:str,entries:Iterable[Mapping[str,Any]])->dict[str,Any]:
    e=sorted((_clone(dict(x)) for x in entries),key=lambda x:x["invariant_id"])
    if any(x.get("loss_status") not in LOSS or x.get("materiality") not in MATERIAL for x in e):raise HarnessViolation("HARNESS_LOSS_RECEIPT_INVALID")
    out={"schema_version":"FFX002_R2_TYPED_LOSS_RECEIPT@1","arm_id":arm_id,"entries":e};out["loss_receipt_hash"]=hash_payload(out);return out

def replay_receipt(arm_id:str,common_hash:str,method_hash:str,code_ref:str,holdout_hash:str,query_hash:str,
                   hostile_refs:Iterable[Any],loss_hash:str,output_hashes:Mapping[str,str],
                   deterministic_ops:Iterable[Mapping[str,Any]],nondeterministic_ops:Iterable[Mapping[str,Any]]=(),
                   tolerances:Mapping[str,Any]|None=None)->dict[str,Any]:
    for n,v in {"common":common_hash,"method":method_hash,"holdout":holdout_hash,"query":query_hash,"loss":loss_hash,**output_hashes}.items():_hex(v,64,n)
    nd=list(nondeterministic_ops)
    if nd and not tolerances:raise HarnessViolation("HARNESS_REPLAY_RECEIPT_INVALID","tolerances")
    out={"schema_version":"FFX002_R2_REPLAY_RECEIPT@1","arm_id":arm_id,"common_manifest_hash":common_hash,
         "method_manifest_hash":method_hash,"code_version_ref":code_ref,"holdout_manifest_hash":holdout_hash,
         "query_manifest_hash":query_hash,"hostile_fixture_refs":list(hostile_refs),"loss_receipt_hash":loss_hash,
         "output_hashes":dict(output_hashes),"deterministic_operations":list(deterministic_ops),
         "nondeterministic_operations":nd,"tolerances":dict(tolerances or {})}
    out["replay_receipt_hash"]=hash_payload(out);return out

def result(dispatch_envelope:Mapping[str,Any],status:str,outputs:Mapping[str,str],loss:Mapping[str,Any],replay:Mapping[str,Any])->dict[str,Any]:
    d=_clone(dict(dispatch_envelope));dh=_verified(d,"dispatch_hash","HARNESS_DISPATCH_HASH_DIVERGENCE")
    lh=_verified(loss,"loss_receipt_hash","HARNESS_LOSS_RECEIPT_HASH_DIVERGENCE");rh=_verified(replay,"replay_receipt_hash","HARNESS_REPLAY_RECEIPT_HASH_DIVERGENCE")
    if replay.get("common_manifest_hash")!=d["common_manifest_hash"] or replay.get("method_manifest_hash")!=d["method_manifest_hash"] or replay.get("loss_receipt_hash")!=lh or replay.get("output_hashes")!=dict(outputs):
        raise HarnessViolation("HARNESS_RESULT_BINDING_DIVERGENCE")
    out={"schema_version":"FFX002_R2_ARM_RESULT_ENVELOPE@1","arm_id":d["arm_id"],"dispatch_hash":dh,
         "common_manifest_hash":d["common_manifest_hash"],"result_status":status,"output_hashes":dict(outputs),
         "loss_receipt":dict(loss),"loss_receipt_hash":lh,"replay_receipt":dict(replay),"replay_receipt_hash":rh}
    out["result_hash"]=hash_payload(out);return out

def hostile_plan(common:Mapping[str,Any],rows:Iterable[Mapping[str,Any]],admitted:Iterable[str],variant_bindings:Mapping[str,str]|None=None)->dict[str,Any]:
    c=validate_common_manifest(common);arms=sorted(set(admitted));bindings=dict(variant_bindings or {});cases=[]
    for r0 in rows:
        r=_clone(dict(r0));pid=r["perturbation_id"];handling=str(r.get("semantic_input_handling",""))
        need=any(x in handling for x in ("NEW_COMMON_INPUT_VARIANT","COMMON_INPUT_FIXTURE_VARIANT","REGISTERED_NULL_VARIANTS"))
        b=bindings.get(pid);bound=_hex(b,64,pid) if b else (None if need else c["manifest_hash"])
        cases.append({"perturbation_id":pid,"target_arms":arms if r.get("views_attacked","ALL")=="ALL" else [a for a in arms if a in str(r["views_attacked"])],
                      "bound_common_manifest_hash":bound,"framework_status":"BLOCKED__EXTERNAL_COMMON_VARIANT_BINDING_REQUIRED" if need and not b else "READY",
                      "expected_failure_state":r.get("failure_state")})
    out={"schema_version":"FFX002_R2_HOSTILE_ORCHESTRATION_PLAN@1","design_ref":DESIGN_REF,"base_common_manifest_hash":c["manifest_hash"],"cases":sorted(cases,key=lambda x:x["perturbation_id"])}
    out["hostile_plan_hash"]=hash_payload(out);return out

def query_plan(query_manifest:Mapping[str,Any],admitted:Iterable[str])->dict[str,Any]:
    qh=_verified(query_manifest,"query_manifest_hash","HARNESS_QUERY_MANIFEST_HASH_DIVERGENCE");arms=sorted(set(admitted));rows=[]
    for q in query_manifest["queries"]:
        p=q.get("views_permitted",[]);p=[x.strip() for x in p.replace(";",",").split(",")] if isinstance(p,str) else list(p)
        for a in arms:rows.append({"query_id":q["query_id"],"arm_id":a,"framework_disposition":"DISPATCH_QUERY" if a in p else "DOES_NOT_REPRESENT","abstention_rule":q.get("abstention_rule")})
    out={"schema_version":"FFX002_R2_QUERY_ORCHESTRATION_PLAN@1","query_manifest_hash":qh,"dispatch_rows":rows};out["query_plan_hash"]=hash_payload(out);return out

def ablation_plan(common_hash:str,query_hash:str,admitted:Iterable[str])->dict[str,Any]:
    _hex(common_hash,64,"common");_hex(query_hash,64,"query");a=set(admitted)
    if not set(CORE)<=a:raise HarnessViolation("HARNESS_ABLATION_CORE_ARM_MISSING")
    packages=[{"package_id":"C","views":["C"]},{"package_id":"A+C","views":["A","C"]},{"package_id":"B+C","views":["B","C"]},{"package_id":"A+B+C","views":["A","B","C"]}]
    comparisons=[("C","A+C","A"),("C","B+C","B"),("C","A+B+C","A+B"),("A+C","A+B+C","B"),("B+C","A+B+C","A")]
    out={"schema_version":"FFX002_R2_ABLATION_ORCHESTRATION_PLAN@1","design_ref":DESIGN_REF,"common_manifest_hash":common_hash,"query_manifest_hash":query_hash,
         "packages":packages,"comparisons":[{"baseline_package":x,"target_package":y,"added_view":z} for x,y,z in comparisons],
         "metric_contract":"08_INCREMENTAL_VALUE_METRICS.tsv@"+DESIGN_REF,"execution_status":"FRAMEWORK_ONLY__NO_EMPIRICAL_RESULTS"}
    out["ablation_plan_hash"]=hash_payload(out);return out

def _read(p:Path):return json.loads(p.read_text())
def _write(p:Path,x:Any):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def main(argv=None)->int:
    ap=argparse.ArgumentParser(description="FFX002-R2 mechanical harness; no empirical execution");sp=ap.add_subparsers(dest="cmd",required=True)
    for name,args in {"compile":[("input",),("output",)],"attest":[("manifest",),("arm-id",),("output",)],
                      "holdout":[("manifest",),("inputs",),("output",)],"queries":[("manifest",),("holdout",),("rows",),("output",)]}.items():
        p=sp.add_parser(name)
        for (n,) in args:p.add_argument("--"+n,type=Path if n not in ("arm-id",) else str,required=True)
    a=ap.parse_args(argv)
    if a.cmd=="compile":_write(a.output,compile_common_manifest(_read(a.input)))
    elif a.cmd=="attest":_write(a.output,attest_arm(a.arm_id,_read(a.manifest)))
    elif a.cmd=="holdout":_write(a.output,freeze_holdout(_read(a.manifest),_read(a.inputs)))
    elif a.cmd=="queries":_write(a.output,freeze_queries(_read(a.manifest),_read(a.holdout),_read(a.rows)))
    return 0
if __name__=="__main__":raise SystemExit(main())
