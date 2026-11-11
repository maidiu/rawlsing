#!/usr/bin/env python3
"""Immutable MCR-C per-identity positive/negative/restore execution oracle.

FROZEN BEFORE IMPLEMENTATION. No synthesized fake responses. Each real candidate
must provide a source-instrumented diagnostic adapter on the existing P6/P5/P4
consumer, not a second conversational/world implementation. An absent adapter or
unproved source-readset is RED. Independent reviewer must re-run from this frozen
reference code, not trust the implementation author's self-written tests.
"""
import argparse,importlib.util,json,sys,hashlib,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
VECTORS=HERE/"mcr_frozen_oracle_vectors.jsonl"
REGISTRY=HERE/"mcr_frozen_identities.tsv"
ADAPTER=ROOT/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/mcr_runtime_adapter.py"
OUTPUT=ROOT/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/outputs"
EVIDENCE=ROOT/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/evidence"
TRACE_REQUIRED={"P6_SESSION_ROOT","COMMITTED_WORLD_READ","ACTUAL_FIRST_CONSUMER","QUALIFIED_SOURCE_READSET","FIRST_READER_OUTPUT","SOURCE_DENIAL_OR_COUNTERFACTUAL","EXACT_RESTORE"}
FIELDS_REQUIRED={"world_digest","actor_digest","mandatory_speech","optional_ids","source_root","source_receipts","source_readset","first_consumer","root","branch","clock","actor_decision_hash"}
def git(*args):
    p=subprocess.run(["git","-C",str(ROOT),*args],text=True,capture_output=True,check=False)
    if p.returncode:raise RuntimeError("MCR_SOURCE_UNRESOLVED "+repr(args)+" "+p.stderr[:400])
    return p.stdout.strip()
def index():
    vecs=[json.loads(x) for x in VECTORS.read_text(encoding="utf-8").splitlines() if x]
    registry=[x.split("\t")[0] for x in REGISTRY.read_text(encoding="utf-8").splitlines()[1:] if x]
    ids=[x["id"] for x in vecs]
    if len(ids)!=54 or len(set(ids))!=54 or ids!=registry:
        raise ValueError("MCR_FROZEN_SCOPE_IDENTITY_SET_OR_ORDER_MISMATCH")
    for v in vecs:
        if not v["assertions"] or not v["required_trace"]:raise ValueError("MCR_MISSING_ASSERTION")
        source=v["source"]
        if git("rev-parse",source["commit"]+":"+source["path"])!=source["blob"]:
            raise ValueError("MCR_RUNTIME_SOURCE_BLOB_UNVERIFIED_"+v["id"])
    return {v["id"]:v for v in vecs}
def output_field(record,field):
    if field not in record:raise AssertionError("MCR_MISSING_FROZEN_OBSERVABLE "+field)
    return record[field]
def run_case(vector):
    if not ADAPTER.is_file():raise RuntimeError("MCR_REAL_IMPLEMENTATION_ADAPTER_MISSING__NOT_RUN")
    spec=importlib.util.spec_from_file_location("mcr_real_candidate_adapter",ADAPTER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if not callable(getattr(module,"execute_case",None)):
        raise RuntimeError("MCR_REAL_ADAPTER_API_MISSING")
    receipts=[]
    for phase in ("control","negative","restore"):
        ret=module.execute_case(json.loads(json.dumps(vector)),phase)
        if not isinstance(ret,dict):raise AssertionError("MCR_ADAPTER_DID_NOT_RETURN_EVIDENCE")
        for x in FIELDS_REQUIRED:
            if x not in ret:raise AssertionError("MCR_MISSING_REQUIRED_ACTUAL_FIRST_READER_"+x)
        if ret["first_consumer"] not in vector["first_consumer"]["functions"]:
            raise AssertionError("MCR_WRONG_FIRST_CONSUMER_"+phase)
        if ret["source_root"]!=vector["source"]["commit"]:
            # implementation may advance runtime code, but shall not silently call
            # the frozen original source historical document its runtime producer
            raise AssertionError("MCR_UNQUALIFIED_RUNTIME_SOURCE_CUT_"+phase)
        readset=ret.get("source_readset")
        if not isinstance(readset,list) or vector["source"]["path"] not in readset:
            raise AssertionError("MCR_REAL_CURRENT_SOURCE_NOT_READ_"+phase)
        if set(ret.get("trace_steps",[]))!=TRACE_REQUIRED:
            raise AssertionError("MCR_SOURCE_FIRST_READER_NEGATIVE_RESTORE_TRACE_MISSING_"+phase)
        if ret.get("fixture_only") or ret.get("simulated_outcome"):
            raise AssertionError("MCR_FIXTURE_AS_CLAIMED_REAL_CONSUMER_"+phase)
        receipts.append(ret)
    control,negative,restore=receipts
    for phase,rec in (("negative",negative),("restore",restore)):
        if rec["root"]!=control["root"] or rec["branch"]!=control["branch"] or rec["clock"]!=control["clock"]:
            raise AssertionError("MCR_CHANGED_UNAUTHORIZED_ROOT_BRANCH_CLOCK_"+phase)
    for field in FIELDS_REQUIRED-{"source_receipts","source_readset","first_consumer","source_root"}:
        if output_field(control,field)!=output_field(restore,field):
            raise AssertionError("MCR_RESTORE_NOT_EXACT_"+field)
    comparisons=[]
    for a in vector["assertions"]:
        op,field=a["op"],a["field"]
        cv=output_field(control,field);nv=output_field(negative,field)
        if op=="EQ": ok=cv==nv
        elif op=="DIFF":ok=cv!=nv
        elif op=="ZERO_NEG":ok=nv in (0,False,None,[],{})
        else:raise AssertionError("MCR_UNKNOWN_PRE_FROZEN_ORACLE_"+op)
        comparisons.append({"op":op,"field":field,"positive":cv,"mutated":nv,"pass":ok})
        if not ok:raise AssertionError("MCR_FROZEN_ORACLE_RED_"+field)
    return {"id":vector["id"],"source":vector["source"],"expected_consumer":vector["first_consumer"],"checks":comparisons,"control":control,"negative":negative,"restore":restore}
def record(case):
    id=case["id"];dest=OUTPUT/(id+".json");proof=EVIDENCE/(id+".json")
    OUTPUT.mkdir(parents=True,exist_ok=True);EVIDENCE.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(case,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n"
    dest.write_text(raw,encoding="utf-8")
    proof.write_text(json.dumps({"id":id,"status":"PASS","source":case["source"],"consumer":case["expected_consumer"],"control_source_events":case["control"].get("source_receipts"),"denial_source_events":case["negative"].get("source_receipts"),"restore_source_events":case["restore"].get("source_receipts"),"three_phase_comparisons":case["checks"]},sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"id":id,"result":"PASS","output":str(dest.relative_to(ROOT)),"evidence":str(proof.relative_to(ROOT))},sort_keys=True))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--id")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    vectors=index()
    if args.self_test:
        assert len(vectors)==54
        print(json.dumps({"status":"PASS_FROZEN_REGISTRY_STRUCTURE_ONLY","count":54,"no_sourcefree_execution":True}))
        return 0
    if args.id not in vectors:raise SystemExit("MCR_UNKNOWN_ID")
    record(run_case(vectors[args.id]))
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except (AssertionError,RuntimeError,ValueError) as ex:
        print(json.dumps({"status":"RED_INCOMPLETE","reason":str(ex)}),file=sys.stderr)
        raise SystemExit(2)
