#!/usr/bin/env python3
"""Independent MCR-C seven-claim review prompt/source and 54-item original mission preflight.

PASS is only predispatch source validation; substantive reviewer is independently
appointed and may return REVISE/HOLD. A nonauthor must still instrument real
consumer calls and review receipts; this script cannot certify any future MII.
"""
import csv,hashlib,io,json,subprocess,sys,tempfile
from pathlib import Path
IDS=["MII-RV-MIII-SOURCE","MII-RV-CAUSAL-ACTION-ABI","MII-RV-VIEWER-SOURCE","MII-RV-EXECUTABLE-54","MII-RV-RECEIPTS-54","MII-RV-CURRENT-CONSUMERS","MII-RV-TERMINAL-NODROP"]
AUTHOR="WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1/00_COPY_PASTE_LAUNCH.md"
REVIEW="WORKER_COMMISSIONS/SOROK-MECHANISM-II-MCR-AF-INDEPENDENT-REVIEW-20261110-R1/00_COPY_PASTE_LAUNCH.md"
REGISTRY="WORKER_COMMISSIONS/SOROK-MECHANISM-II-MCR-AF-INDEPENDENT-REVIEW-20261110-R1/mcr_frozen_review_ids.tsv"
AUTHOR_SHA="0178df262ac04d6fef074a56f6b8448c4d7fdcf9"
FREEZE_SHA="e37322219c54df2cd0084162bb0b68d016794a6b"
PROTECTED="4f3413fc5c37b589be3412f826bf8f68ee617d4a"
CHECKER="CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py"
def git(*args):
    return subprocess.check_output(["git",*args])
def verify():
    reg=git("show",FREEZE_SHA+":"+REGISTRY)
    assert hashlib.sha1(("blob "+str(len(reg))+"\0").encode()+reg).hexdigest()=="23c55f74b227a5d843e8489f65dcb45302813762","MCR_REVIEW_REGISTRY_BLOB_DRIFT"
    frozen=[x["id"] for x in csv.DictReader(io.StringIO(reg.decode()),delimiter="\t")]
    assert frozen==IDS,"MCR_7_FROZEN_REGISTRY_IDENTITY_MISMATCH"
    text=Path(REVIEW).read_text()
    block=text.split("MCR_COMPLETION_CONTRACT_BEGIN",1)[1].split("MCR_COMPLETION_CONTRACT_END",1)[0]
    objs=[json.loads(x.partition(": ")[2]) for x in block.splitlines() if x.startswith("MCR_OBLIGATION: ")]
    assert [x["id"] for x in objs]==IDS,"MCR_7_REVIEW_OBLIGATIONS_MISMATCH"
    assert len({x["output"] for x in objs})==7 and len({x["evidence"] for x in objs})==7,"MCR_REVIEW_EVIDENCE_NOT_ONE_PER_ID"
    frozenAuthor=git("show",AUTHOR_SHA+":"+AUTHOR)
    assert frozenAuthor==Path(AUTHOR).read_bytes(),"AUTHOR_SOURCE_REVIEW_NOT_EXACT"
    with tempfile.TemporaryDirectory() as temp:
        canonical=Path(temp)/"checker.py";canonical.write_bytes(git("show",PROTECTED+":"+CHECKER))
        reviewFile=Path(temp)/"review_launch.md";reviewFile.write_text(text)
        result=subprocess.run([sys.executable,str(canonical),str(reviewFile),"--source-check"],capture_output=True,text=True)
        assert result.returncode==0,("CANONICAL_REVIEW_LAUNCH_RED",result.stdout[-1300:])
    baseline="WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1/"
    for command in (["python3","-B",baseline+"mcr_completion_inventory.py","verify"],
                    ["python3","-B",baseline+"mcr_frozen_oracle_runner.py","--self-test"],
                    ["python3","-B",baseline+"mcr_terminal_receiving.py","--issued-sha",AUTHOR_SHA,"--preflight"],
                    ["python3","-B",baseline+"mcr_contract_reduction_attack.py","--self-test"],
                    ["python3","-B",baseline+"mcr_full_e1_e10_gate.py","--preflight"],
                    ["python3","-B",baseline+"mcr_full_e1_e10_gate.py","--forged-attack"]):
        subprocess.run(command,check=True)
    print(json.dumps({"status":"PASS_REVIEW_SEVEN_MCR_C_SOURCE_PREFLIGHT_ONLY","independent_judgment":"NOT_EXECUTED","review_obligations":7,"original_author_obligations":54,"author_sha":AUTHOR_SHA},sort_keys=True))
if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("enumerate","verify"):raise SystemExit("usage: enumerate / verify")
    if sys.argv[1]=="enumerate":print("\n".join(IDS))
    else:verify()
