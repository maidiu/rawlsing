#!/usr/bin/env python3
"""R3 state/claim-grade witness: test whether EXACT_OWNER_HOLD/FUTURE_NONPRECLUDED
can be promoted to PRESENT_PRESERVED, and whether a C SOURCE_STATIC boundary can
be relabelled ACTUAL_PROVED with only a self-asserted boolean. Typed machine and
frozen prose hashes are left intact."""
import json, pathlib, shutil, sys, tempfile

R3=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R3_RECHECK')
TS=(R3/'LOGS/STAMP').read_text().strip(); PKG=R3/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R3/'WITNESS/W_STATE_CLAIM'; OUT.mkdir(parents=True,exist_ok=True)
def run(tag, mut):
    tmp=pathlib.Path(tempfile.mkdtemp(prefix=tag+'_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
    f=json.loads((ev/'FRAME.json').read_text()); d=json.loads((ev/'DECISION.json').read_text()); c=json.loads((ev/'C.json').read_text())
    mut(f,d,c)
    def put(n,o):
        b=(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/n).write_bytes(b)
    put('FRAME.json',f); d['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())}; d['frame_sha256']=digest(f); put('DECISION.json',d); c['integrated_decision']={'path':'DECISION.json','sha256':sha((ev/'DECISION.json').read_bytes())}; c['integrated_decision_sha256']=digest(d); put('C.json',c)
    return {'DECISION':check('DECISION',d,ev,source,REPO,ZIP),'C':check('C_INTEGRATED',c,ev,source,REPO,ZIP)}
rep={'schema':'C_REVIEW_R3_STATE_CLAIM'}
def m1(f,d,c):
    x=next(x for x in d['identity_dispositions'] if x['identity_id']=='P4R-R01'); x['disposition']='PRESENT_PRESERVED'
rep['identity_hold_to_preserved']=run('m1',m1)
def m2(f,d,c):
    x=next(x for x in d['requirement_dispositions'] if x['requirement_id']=='REQ-FIELD-FORGE'); x['disposition']='PRESENT_PRESERVED'
rep['requirement_future_to_present']=run('m2',m2)
def m3(f,d,c):
    x=c['boundary_court']['T4']; x['claim_grade']='ACTUAL_PROVED'; x['grade']='EXECUTED_AT_SCOPE'; x['actual_first_reader_verified']=True
rep['boundary_source_static_to_actual']=run('m3',m3)
(OUT/'w_state_claim.json').write_text(json.dumps(rep,indent=2)+'\n'); print(json.dumps(rep,indent=2))
