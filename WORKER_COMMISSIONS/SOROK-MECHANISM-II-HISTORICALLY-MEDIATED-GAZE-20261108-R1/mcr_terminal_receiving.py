#!/usr/bin/env python3
"""Independent terminal verifier: immutable ISSUED launch, never candidate-edited contract."""
import argparse,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE="WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1/"
LAUNCH=BASE+"00_COPY_PASTE_LAUNCH.md"
RUNNER=BASE+"mcr_frozen_oracle_runner.py"
VECTOR=BASE+"mcr_frozen_oracle_vectors.jsonl"
REGISTRY=BASE+"mcr_frozen_identities.tsv"
FULL_MATRIX=BASE+"mcr_full_e1_e10_acceptance.json"
FULL_GATE=BASE+"mcr_full_e1_e10_gate.py"
ACTUAL_CONSUMER_WITNESS=BASE+"mcr_independent_consumer_trace.py"
CHECKER="CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py"
PROTECTED="4f3413fc5c37b589be3412f826bf8f68ee617d4a"
BLOBS={CHECKER:(PROTECTED,"6e16878e60e8e89bf8ab8001144ed84ad257f5fc"),
REGISTRY:("8382651eabc5a7fa6ca0fed3447fa6308b3324fc","a4aa2fafbb19263e3a89de703c8525a765417e95"),
VECTOR:("8382651eabc5a7fa6ca0fed3447fa6308b3324fc","294dcb35cb46f0d24b1f110c80cb562360e9df03"),
FULL_MATRIX:("62cd9aae4a12f6cef9ef4c7bc34326c3d3c306ff","2ff94ac73fbd22344acfe2890a9163b8b492348d"),
RUNNER:("8382651eabc5a7fa6ca0fed3447fa6308b3324fc","0d82d36416834b2bda3b112f9b9dcbf0a475d603")}
def run(*cmd,check=True):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if check and p.returncode:raise RuntimeError("MCR_SUBPROCESS_REFUSED "+repr(cmd)+" "+p.stderr[-800:])
    return p
def source(path,sha):return run("git","show",sha+":"+path).stdout.encode()
def preflight(issued):
    if not re.fullmatch(r"[0-9a-f]{40}",issued):raise ValueError("EXACT_ISSUER_SHA_REQUIRED")
    for path,(sha,blob) in BLOBS.items():
        if run("git","rev-parse",sha+":"+path).stdout.strip()!=blob:
            raise RuntimeError("FROZEN_SOURCE_IDENTITY_MISMATCH "+path)
        if path!=CHECKER and run("git","hash-object",path).stdout.strip()!=blob:
            raise RuntimeError("AUTHOR_MODIFIED_FROZEN_TEST_OR_REGISTRY "+path)
    original=source(LAUNCH,issued).decode()
    records=[json.loads(x.partition(": ")[2]) for x in original.splitlines() if x.startswith("MCR_OBLIGATION: ")]
    scopes=[json.loads(x.partition(": ")[2]) for x in original.splitlines() if x.startswith("MCR_SCOPE: ")]
    if len(records)!=54 or len({x["id"] for x in records})!=54 or len(scopes)!=1:
        raise RuntimeError("ISSUED_SCOPE_NOT_54")
    s=scopes[0]
    if s.get("expected_count")!=54 or s.get("identity_columns")!=["id"] or s.get("source")!={"path":REGISTRY,"commit":BLOBS[REGISTRY][0],"blob":BLOBS[REGISTRY][1]}:
        raise RuntimeError("ISSUED_SCOPE_NOT_FROZEN_EXTERNAL_TSV")
    for r in records:
        if r["check"]!=f"RUN: python3 -B {RUNNER} --id {r['id']}":
            raise RuntimeError("ISSUED_TEST_COMMAND_NOT_EXACT "+r["id"])
    import collections
    full=json.loads((ROOT/FULL_MATRIX).read_text(encoding="utf-8"))
    full_ids={x["id"] for x in full["records"]}
    if full["required_count"]!=63 or len(full_ids)!=63:
        raise RuntimeError("MCR_WHOLE_E_SCOPE_63_SOURCE_REQUIREMENTS_MISSING")
    for r in records:
        if r["id"].startswith("MII-E"):
            covered=r.get("full_mission_acceptance_ids",[])
            if not covered or set(covered)!={x["id"] for x in full["records"] if x["package"]==r["id"]}:
                raise RuntimeError("MCR_E_PACKAGE_FULL_OUTCOME_CONSERVATION_FAILED_"+r["id"])
    if len({r["output"] for r in records})!=54 or len({r["evidence"] for r in records})!=54:
        raise RuntimeError("ISSUED_REUSED_PROOF_ARTIFACT")
    with tempfile.TemporaryDirectory() as temp:
        c=Path(temp)/"checker.py";c.write_bytes(source(CHECKER,PROTECTED))
        p=Path(temp)/"issued.md";p.write_text(original)
        v=run(sys.executable,str(c),str(p),"--source-check",check=False)
        if v.returncode:raise RuntimeError("ISSUED_MCR_C_PREDISPATCH_RED "+v.stdout[-1200:])
    return original,records
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--issued-sha",required=True)
    p.add_argument("--candidate-sha")
    p.add_argument("--return-file")
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--review-sha")
    p.add_argument("--runtime-sha")
    p.add_argument("--preflight",action="store_true")
    a=p.parse_args()
    original,records=preflight(a.issued_sha)
    if a.preflight:
        print(json.dumps({"status":"PASS_ISSUED_54_SOURCE_PROOF_COMMANDS_ONLY","actual_MII_not_run":True}))
        return 0
    if not a.candidate_sha or not a.return_file or not a.review_sha or not a.runtime_sha:
        raise ValueError("MISSING_WORKER_RETURN_SHA_OR_INDEPENDENT_E1_E10_REVIEW")

    if run("git","rev-parse","HEAD").stdout.strip()!=a.candidate_sha:
        raise RuntimeError("WRONG_WORKER_HEAD")
    for r in records:
        result=run(sys.executable,"-B",RUNNER,"--id",r["id"],check=False)
        if result.returncode:raise RuntimeError("SOURCE_QUALIFIED_TEST_RED "+r["id"]+" "+result.stderr[-600:])
    # 54 legacy scenario predicates alone are NOT proof of real consumer calls.
    # The additional locked observer profiles actual imported P6 code objects
    # in an independently authenticated protected/candidate worktree.
    for r in records:
        actual=run(sys.executable,"-B",ACTUAL_CONSUMER_WITNESS,"--id",r["id"],check=False)
        if actual.returncode:
            raise RuntimeError("MCR_FIRST_CONSUMER_NOT_INDEPENDENTLY_OBSERVED_"+r["id"]+" "+actual.stderr[-650:])
    full=run(sys.executable,"-B",FULL_GATE,"--review-sha",a.review_sha,"--runtime-sha",a.runtime_sha,check=False)
    if full.returncode:
        raise RuntimeError("MCR_E1_E10_FULL_MISSION_NOT_EXECUTED_OR_ACCEPTABLE "+full.stderr[-850:])
    with tempfile.TemporaryDirectory() as temp:
        checker=Path(temp)/"checker.py";checker.write_bytes(source(CHECKER,PROTECTED))
        contract=Path(temp)/"issued.md";contract.write_text(original)
        receipt=run(sys.executable,str(checker),str(contract),"--verify-return",str(Path(a.return_file).resolve()),"--candidate-sha",a.candidate_sha,"--evidence-root",str(a.root.resolve()),check=False)
        if receipt.returncode:raise RuntimeError("FROZEN_54_RETURN_RED "+receipt.stdout[-1500:])
        result=json.loads(receipt.stdout)
        if result.get("status")!="READY_FOR_INDEPENDENT_RECEIVING" or result.get("expected_identity_count")!=54 or result.get("verified_obligation_count")!=54:
            raise RuntimeError("MCR_FALSE_COMPLETE_RETURN")
        print(receipt.stdout)
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except (ValueError,RuntimeError) as e:
        print(json.dumps({"status":"RED_INCOMPLETE","reason":str(e)}),file=sys.stderr)
        raise SystemExit(2)
