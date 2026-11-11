#!/usr/bin/env python3
"""Actual 53/54 forged-receipt attack: terminal checker must reject source-root drift."""
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LAUNCH="WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1/00_COPY_PASTE_LAUNCH.md"
PROTECTED="4f3413fc5c37b589be3412f826bf8f68ee617d4a"
CHECKER="CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py"
def git(root,*args):
    p=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError("ATTACK_GIT_FAILED "+repr(args)+" "+p.stderr[-600:])
    return p.stdout.strip()
def h(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    argparse.ArgumentParser().add_argument("--self-test",action="store_true",required=True)
    with tempfile.TemporaryDirectory(prefix="mcr-c-attack-") as td:
        tmp=Path(td);work=tmp/"candidate"
        git(ROOT,"worktree","add","--detach",str(work),"HEAD")
        try:
            checker=tmp/"checker.py";checker.write_text(git(ROOT,"show",PROTECTED+":"+CHECKER))
            spec=importlib.util.spec_from_file_location("mcr_c_immutable",checker)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            target=work/LAUNCH;lines=target.read_text().splitlines()
            at=next(i for i,x in enumerate(lines) if x.startswith("MCR_SCOPE: "))
            original=[(i,x) for i,x in enumerate(lines) if x.startswith("MCR_OBLIGATION: ")]
            if len(original)!=54:raise RuntimeError("ATTACK_EXPECTED_54")
            dropped=json.loads(original[-1][1].partition(": ")[2])["id"]
            lines.pop(original[-1][0])
            scope=json.loads(lines[at].partition(": ")[2]);scope["expected_count"]=53
            lines[at]="MCR_SCOPE: "+json.dumps(scope,separators=(",",":"))
            target.write_text("\n".join(lines)+"\n")
            mutated=target.read_text()
            if module.validate(mutated)["status"]!="PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH":
                raise RuntimeError("ATTACK_PRECHECK_NOT_SELF_CONSISTENT")
            c=module.completion_contract(mutated,[])
            records=c["obligations"];assert len(records)==53
            for r in records:
                for key in ("output","evidence"):
                    p=work/r[key];p.parent.mkdir(parents=True,exist_ok=True)
                    p.write_text("FORGED RECEIPT; NOT REAL MII PROOF\n")
            coverage=work/"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1/attack_53_ids.txt"
            coverage.parent.mkdir(parents=True,exist_ok=True);coverage.write_text("\n".join(r["id"] for r in records)+"\n")
            git(work,"add",LAUNCH,"WORKER_RETURNS/SOROK-MII-MCR-AF-FULL-20261110-R1")
            git(work,"-c","user.name=MCR Negative Test","-c","user.email=mcr@invalid.example","commit","-qm","synthetic 53 internally consistent fake receipts")
            sha=git(work,"rev-parse","HEAD")
            proof=["MCR_COMPLETION_EVIDENCE_BEGIN","MCR_COVERAGE: "+json.dumps({"candidate_sha":sha,"contract_sha256":c["sha256"],"delivered_ids_file":str(coverage.relative_to(work)),"delivered_ids_sha256":h(coverage)})]
            for r in records:
                proof.append("MCR_EVIDENCE: "+json.dumps({"id":r["id"],"candidate_sha":sha,"contract_sha256":c["sha256"],"status":"PASS","grade":"S2","evidence_file":r["evidence"],"evidence_sha256":h(work/r["evidence"]),"output_file":r["output"],"output_sha256":h(work/r["output"])}))
            proof.append("MCR_COMPLETION_EVIDENCE_END")
            result=module.verify_return(mutated,"\n".join(proof),sha,work)
            required={"MCR_C_FROZEN_UNIVERSE_COUNT_OR_DUPLICATE_MISMATCH","MCR_C_NO_DROP_SET_MISMATCH"}
            if result["status"]!="RED_INCOMPLETE" or not required.issubset(set(result["errors"])):
                raise RuntimeError("DANGEROUS_53_FALSE_PASS "+repr(result))
            print(json.dumps({"status":"PASS_REJECTED_53_FORGED_PROOFS","missing":dropped,"frozen_tsv_source":scope["source"],"actual_verifier_status":result["status"],"errors":sorted(required),"scope":"synthetic attack; NOT_MII_EXECUTION"},sort_keys=True))
        finally:
            git(ROOT,"worktree","remove","--force",str(work))
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except Exception as e:
        print(json.dumps({"status":"RED_ATTACK_TEST_FAILED","error":str(e)}),file=sys.stderr);raise SystemExit(2)
