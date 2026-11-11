#!/usr/bin/env python3
"""MCR-C whole E1-E10 receiving, independent of the 54 supporting scenario probes.

This verifier deliberately refuses a self-claimed 63/63 PASS table. A real
nonauthor reviewer must commit a separately identified test suite and run it
against the source-qualified current P6/P5/P4 first consumers. Each required
outcome must carry independently observed source, source-fault and restoration
evidence, including persistent data, uncertainty/decay, rights and real
performance measurements. Coverage and hashes alone can never return ACCEPT.

The independent reviewer author and source authority remain human/HQ judgment;
this program only enforces an external test/evidence interface and fails closed.
"""
import argparse,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent
SCOPE=BASE/"mcr_full_e1_e10_acceptance.json"
WITNESS=BASE/"mcr_independent_consumer_trace.py"
REVIEW="WORKER_REVIEWS/SOROK-MII-MCR-AF-889-R1/independent_full_e1_e10_suite.py"
def git(*args):
    result=subprocess.run(["git","-C",str(ROOT),*args],capture_output=True,text=True)
    if result.returncode:raise RuntimeError("MCR_MISSION_GIT_UNRESOLVED "+repr(args)+" "+result.stderr[-400:])
    return result.stdout.strip()
def matrix():
    data=json.loads(SCOPE.read_text(encoding="utf-8"))
    rows=data["records"]; ids=[x["id"] for x in rows]
    if data.get("required_count")!=63 or len(ids)!=63 or len(set(ids))!=63:
        raise ValueError("MCR_FULL_E1_E10_63_SOURCE_REQUIREMENTS_NOT_CONSERVED")
    from collections import Counter
    p=Counter(x["package"] for x in rows)
    if set(p)!={f"MII-E{i:02d}" for i in range(1,11)}:
        raise ValueError("MCR_FULL_E1_E10_PACKAGE_LOSS")
    for r in rows:
        if not r["required"] or not r["negative"] or r.get("independent_receiving_required") is not True:
            raise ValueError("MCR_FULL_E1_E10_MISSING_DISCRIMINATOR_"+r["id"])
    return ids
def assess_receipts(ids,records):
    if not isinstance(records,list) or [x.get("id") for x in records]!=ids:
        raise RuntimeError("MCR_MISSION_63_PER_OUTCOME_EVIDENCE_INCOMPLETE")
    for x in records:
        if x.get("status")!="PASS" or x.get("grade")!="SOURCEFREE_S2":
            raise RuntimeError("MCR_MISSION_FULL_SOURCEFREE_PROOF_NOT_PASS_"+x["id"])
        evidence=x.get("independent_actual_source_witness")
        if not isinstance(evidence,dict) or not isinstance(evidence.get("actual_source_calls"),list):
            raise RuntimeError("MCR_MISSION_ADAPTER_ONLY_EVIDENCE_REJECTED_"+x["id"])
        if not any(r.get("module")=="run_p6" and r.get("function")=="experience" and r.get("event")=="return"
                   for r in evidence["actual_source_calls"]):
            raise RuntimeError("MCR_MISSION_NO_INDEPENDENT_REAL_P6_RETURN_"+x["id"])
        if not x.get("qualified_source_denial") or not x.get("exact_source_restore"):
            raise RuntimeError("MCR_MISSION_NO_SOURCE_DENIAL_RESTORE_"+x["id"])
        if not x.get("actual_first_reader_output_sha256") or not re.fullmatch("[0-9a-f]{64}",x["actual_first_reader_output_sha256"]):
            raise RuntimeError("MCR_MISSION_MISSING_INDEPENDENT_FIRST_READER_DIGEST_"+x["id"])
        if not x.get("reviewer_command") or x.get("reviewer_command_origin")!="INDEPENDENT_NONAUTHOR_SOURCE":
            raise RuntimeError("MCR_MISSION_AUTHOR_ONLY_TEST_NOT_ACCEPTABLE_"+x["id"])
    return True
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--preflight",action="store_true")
    p.add_argument("--forged-attack",action="store_true")
    p.add_argument("--review-sha")
    p.add_argument("--runtime-sha")
    p.add_argument("--verified-test-path",default=REVIEW)
    args=p.parse_args()
    ids=matrix()
    if args.preflight:
        print(json.dumps({"status":"PASS_FULL_MISSION_63_DISCRIMINATORS_PRESERVED","e_packages":10,
                          "claims":63,"actual_MII_implementation":"NOT_RUN","independent_acceptance":"PENDING"}))
        return
    if args.forged_attack:
        false=[{"id":i,"status":"PASS","grade":"SOURCEFREE_S2",
                "independent_actual_source_witness":{"actual_source_calls":[{"module":"run_p6","function":"experience","event":"return"}]},
                "qualified_source_denial":True,"exact_source_restore":True,
                "actual_first_reader_output_sha256":"0"*64,
                "reviewer_command":"echo PASS","reviewer_command_origin":"AUTHOR_ADAPTER"} for i in ids]
        try:
            assess_receipts(ids,false)
        except RuntimeError as exc:
            if "MCR_MISSION_AUTHOR_ONLY_TEST_NOT_ACCEPTABLE" not in str(exc):raise
            print(json.dumps({"status":"PASS_FORGED_63_OF_63_AUTHOR_RECEIPTS_REJECTED",
                              "error":str(exc),"actual_MII_test":"NOT_RUN"}))
            return
        raise RuntimeError("MCR_FALSE_AUTHOR_63_RECEIPT_ACCEPTED")
    if not args.review_sha or not args.runtime_sha:
        raise RuntimeError("MCR_INDEPENDENT_REVIEW_SHA_AND_ACTUAL_RUNTIME_SHA_REQUIRED")
    if not re.fullmatch("[0-9a-f]{40}",args.review_sha) or not re.fullmatch("[0-9a-f]{40}",args.runtime_sha):
        raise RuntimeError("MCR_UNQUALIFIED_REVIEW_SOURCE_SHA")
    if not args.verified_test_path.startswith("WORKER_REVIEWS/SOROK-MII-MCR-AF-889-R1/"):
        raise RuntimeError("MCR_REVIEW_TEST_MUST_BE_EXTERNAL_NONAUTHOR_BRANCH")
    # Pull independent suite from immutable separately reviewed object, not
    # the candidate's mutable test file. The reviewer needs an actual S2 host.
    suite=git("show",args.review_sha+":"+args.verified_test_path)
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/"independent_e_suite.py";p.write_text(suite,encoding="utf-8")
        ret=subprocess.run([sys.executable,"-B",str(p),"--runtime-sha",args.runtime_sha,
                            "--criteria",str(SCOPE.resolve()),"--observed-only"],
                           cwd=ROOT,capture_output=True,text=True)
        if ret.returncode:
            raise RuntimeError("MCR_INDEPENDENT_E_SUITE_NOT_EXECUTED "+ret.stderr[-800:])
        results=json.loads(ret.stdout)
        assess_receipts(ids,results["records"])
        print(json.dumps({"status":"READY_FOR_INDEPENDENT_HQ_JUDGMENT_NOT_AUTO_ACCEPTED",
                          "mission_criteria":63,"E_packages":10,"review_sha":args.review_sha,
                          "runtime_sha":args.runtime_sha}))
if __name__=="__main__":
    try:main()
    except (ValueError,RuntimeError) as e:
        print(json.dumps({"status":"RED_INCOMPLETE","reason":str(e)}),file=sys.stderr)
        raise SystemExit(2)
