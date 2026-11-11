#!/usr/bin/env python3
"""Independent source-code-object witness for MII's actual P6/P5/P4 first consumers.

Unlike the old 54-vector runner, this observer NEVER accepts the adapter's
first_consumer, source_readset, trace_steps, or digests as proof that an owner
executed. It imports live owner modules itself; only actual CPython frames whose
code objects match those live imports count. It captures returned public P6
objects and computes their digests outside the adapter. An adapter may arrange
a scenario, but its claims cannot create a trusted call or source response.

Scope: engineering/sourcefree execution witness, NOT science or complete
E1-E10 acceptance. All phases and causality need independent reviewer judgment.
"""
import argparse, hashlib, importlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUNTIME_ROOT=Path(os.environ.get("MCR_QUALIFIED_RUNTIME_ROOT",str(ROOT))).resolve()
HERE=Path(__file__).resolve().parent
P6=RUNTIME_ROOT/"WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
P5=RUNTIME_ROOT/"WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P4=RUNTIME_ROOT/"WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"
ADAPTER=ROOT/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/mcr_runtime_adapter.py"
VECTORS=HERE/"mcr_frozen_oracle_vectors.jsonl"
PROOFS=ROOT/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/consumer_witness"
REFERENCE={
 "run_p6":("experience",),
 "house":("scene","read_house","perform","derive_recognition"),
 "attention":("register","select"),
 "gaze":("render","visible_events","attend"),
 "run_p5":("surface","act"),
 "actor_initiative":("visit_adjacent_room",),
}
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,default=str,separators=(",",":")).encode()).hexdigest()
def import_owners():
    # The documentary PR #889 predates the protected runtime tree. An actual
    # protected/candidate worktree must be mounted explicitly; never mint a
    # sourcefree twin beneath the author checkout.
    for p in (P6,P5,P4):
        if not p.is_dir():
            raise AssertionError("MCR_PROTECTED_RUNTIME_CHECKOUT_REQUIRED_"+str(p))
    if not (P6/"run_p6.py").is_file():
        raise AssertionError("MCR_REAL_P6_SOURCE_MISSING")
    approved=os.environ.get("MCR_QUALIFIED_RUNTIME_SHA")
    if not approved or len(approved)!=40:
        raise AssertionError("MCR_APPROVED_RUNTIME_SHA_REQUIRED")
    ref=subprocess.run(["git","-C",str(RUNTIME_ROOT),"rev-parse","HEAD"],capture_output=True,text=True)
    if ref.returncode or ref.stdout.strip()!=approved:
        raise AssertionError("MCR_RUNTIME_CHECKOUT_SHA_NOT_AUTHENTICATED")
    for p in (P6,P5,P4):
        if str(p) not in sys.path:sys.path.insert(0,str(p))
    modules={k:importlib.import_module(k) for k in REFERENCE}
    codes={}
    for key,methods in REFERENCE.items():
        module=modules[key]
        if Path(module.__file__).resolve().parent not in (P6.resolve(),P5.resolve(),P4.resolve()):
            raise AssertionError("MCR_OWNER_IMPORTED_FROM_OTHER_TREE_"+key)
        for method in methods:
            obj=getattr(module,method,None)
            if obj is not None and hasattr(obj,"__code__"):
                codes[obj.__code__]=(key,method)
    return codes
def witness(adapter,vector,phase,codes):
    calls=[]
    p6_returns=[]
    def hook(frame,event,arg):
        key=codes.get(frame.f_code)
        if key is None:return
        if event=="call":
            calls.append({"module":key[0],"function":key[1],"event":"call"})
        elif event=="return":
            if key==("run_p6","experience"):
                if not isinstance(arg,dict):
                    raise AssertionError("MCR_P6_PUBLIC_RESULT_MISSING")
                p6_returns.append({"sha256":digest(arg),"room":arg.get("room"),"clock":arg.get("clock"),
                                   "narration":arg.get("narration"),"detail":arg.get("detail"),
                                   "recognized_identity":arg.get("recognized_identity"),
                                   "available":arg.get("available")})
            calls.append({"module":key[0],"function":key[1],"event":"return"})
    old=sys.getprofile()
    try:
        sys.setprofile(hook)
        reported=adapter.execute_case(json.loads(json.dumps(vector)),phase)
        if sys.getprofile() is not hook:
            raise AssertionError("MCR_AUTHOR_DISABLED_INDEPENDENT_PROFILER")
    finally:
        sys.setprofile(old)
    if not p6_returns:
        raise AssertionError("MCR_COUNTERFEIT_ADAPTER_NO_REAL_P6_EXPERIENCE_"+phase)
    returned=[(c["module"],c["function"]) for c in calls if c["event"]=="return"]
    first=vector["first_consumer"]
    expected_module=Path(first["module"]).stem
    expected=set(first["functions"])
    if not any(module==expected_module and func in expected for module,func in returned):
        raise AssertionError("MCR_COUNTERFEIT_ADAPTER_NO_ACTUAL_NAMED_CONSUMER_"+phase)
    if not isinstance(reported,dict):
        raise AssertionError("MCR_ADAPTER_NO_PHASE_REPORT")
    expected_sha=reported.get("p6_observed_return_sha256")
    if expected_sha is None or expected_sha!=p6_returns[-1]["sha256"]:
        raise AssertionError("MCR_ADAPTER_CLAIMS_NOT_EQUAL_ACTUAL_P6_PUBLIC_RETURN_"+phase)
    # This digest is made by the separate profiler, never by the adapter.
    return {"phase":phase,"actual_call_pairs":calls,"actual_p6_returns":p6_returns,
            "independent_public_digest":p6_returns[-1]["sha256"]}
def execute_case(vector,adapter):
    codes=import_owners()
    observations=[witness(adapter,vector,phase,codes) for phase in ("control","negative","restore")]
    control,negative,restore=observations
    # Restore MUST reattain independently observed public output, not merely
    # reproduce the adapter's invented digest. A true source refusal in the
    # negative phase can be documented separately by a reviewer.
    if control["independent_public_digest"]!=restore["independent_public_digest"]:
        raise AssertionError("MCR_SOURCE_WITNESS_REAL_P6_RESTORE_DIFFERENT")
    # Do not demand negative differs universally: gaze-only changes may
    # properly leave compulsory sources unchanged.
    return {"id":vector["id"],"witness_version":"MII_INDEPENDENT_SOURCE_CODE_OBJECT_R1",
            "phases":observations,"scope":"EXACT_REAL_P6_CALL_PROVED__E1_E10_STILL_REQUIRE_FULL_GATES"}
def fake_attack():
    vec={"id":"MII-E01","source":{"commit":"4f3413fc5c37b589be3412f826bf8f68ee617d4a"},
         "first_consumer":{"module":"WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py","functions":["experience"]}}
    class Counterfeit:
        def execute_case(self,case,phase):
            return {"first_consumer":"experience","source_readset":[case["first_consumer"]["module"]],
                    "source_root":case["source"]["commit"],"trace_steps":["ACTUAL_FIRST_CONSUMER"],
                    "p6_observed_return_sha256":"0"*64}
    try:
        witness(Counterfeit(),vec,"control",import_owners())
    except AssertionError as error:
        if str(error)!="MCR_COUNTERFEIT_ADAPTER_NO_REAL_P6_EXPERIENCE_control":
            raise
        print(json.dumps({"status":"PASS_COUNTERFEIT_ADAPTER_REJECTED",
                          "reason":str(error),"independent_source_observation":True}))
        return
    raise AssertionError("MCR_COUNTERFEIT_ADAPTER_FALSE_POSITIVE")
def actual_baseline():
    # First demonstrate a REAL owned return, then source denial at the
    # original P6/house read boundary and exact restoration of the public view.
    import argparse,tempfile
    modules=import_owners()
    from developmental_recursion.contracts import RecursionRefusal
    run_p6=importlib.import_module("run_p6")
    house=importlib.import_module("house")
    with tempfile.TemporaryDirectory(prefix="mcr-real-p6-") as td:
        state=Path(td)/"sourcefree"
        class RealAdapter:
            def execute_case(self,vector,phase):
                result=run_p6.experience(state,argparse.Namespace(command="new",situated_house=False),
                                         provider_mode="INJECTED")
                return {"p6_observed_return_sha256":digest(result)}
        vector={"id":"MII-P6-BASELINE","first_consumer":{
            "module":"WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py",
            "functions":["experience"]}}
        proof=witness(RealAdapter(),vector,"control",modules)
        view=argparse.Namespace(command="view")
        before=run_p6.experience(state,view,provider_mode="INJECTED")
        original_ledger=(state/"p4_receipts.json").read_bytes()
        original_glance=house.OBJECTS["bench"]["glance"]
        denied=False
        try:
            house.OBJECTS["bench"]["glance"]=original_glance+" injected independent source fault"
            try:
                run_p6.experience(state,view,provider_mode="INJECTED")
            except RecursionRefusal as exc:
                if str(exc) not in ("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH","P6_OBJECT_PROVENANCE_MISMATCH"):
                    raise AssertionError("MCR_UNEXPECTED_SOURCE_DENIAL_REASON_"+str(exc))
                denied=True
        finally:
            house.OBJECTS["bench"]["glance"]=original_glance
        if not denied:raise AssertionError("MCR_MUTATED_UPSTREAM_HOUSE_SOURCE_NOT_REFUSED")
        after=run_p6.experience(state,view,provider_mode="INJECTED")
        if digest(before)!=digest(after):
            raise AssertionError("MCR_UPSTREAM_SOURCE_RESTORE_CHANGED_REAL_PUBLIC_VIEW")
        if original_ledger!=(state/"p4_receipts.json").read_bytes():
            raise AssertionError("MCR_SOURCE_REFUSAL_MUTATED_WORLD_LEDGER")
        print(json.dumps({"status":"PASS_ACTUAL_P6_CODE_OBJECT_AND_SOURCE_DENIAL_RESTORE_WITNESSED",
                          "observed_calls":len(proof["actual_call_pairs"]),
                          "public_digest":digest(before),"source_fault_denied":True,
                          "restored_public_equal":True,
                          "world_ledger_byte_invariant":True,
                          "grade":"SOURCEFREE_BASELINE_NOT_MII_IMPLEMENTATION"},sort_keys=True))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--id")
    p.add_argument("--counterfeit-attack",action="store_true")
    p.add_argument("--baseline",action="store_true")
    a=p.parse_args()
    if a.counterfeit_attack:return fake_attack()
    if a.baseline:return actual_baseline()
    vectors={x["id"]:x for x in (json.loads(row) for row in VECTORS.read_text().splitlines() if row)}
    if a.id not in vectors:raise ValueError("MCR_UNKNOWN_WITNESS_VECTOR_ID")
    if not ADAPTER.is_file():raise ValueError("MCR_MII_ADAPTER_NOT_IMPLEMENTED")
    spec=importlib.util.spec_from_file_location("mii_candidate",ADAPTER)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    result=execute_case(vectors[a.id],mod)
    PROOFS.mkdir(parents=True,exist_ok=True)
    dest=PROOFS/(a.id+".json")
    dest.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":"PASS_SOURCEFREE_ACTUAL_CONSUMER_WITNESS_ONLY","id":a.id,"file":str(dest.relative_to(ROOT))}))
if __name__=="__main__":
    try:main()
    except (AssertionError,ValueError,RuntimeError) as e:
        print(json.dumps({"status":"RED_INCOMPLETE","reason":str(e)}),file=sys.stderr)
        raise SystemExit(2)
