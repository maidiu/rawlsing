#!/usr/bin/env python3
"""R4 state/claim-grade recheck. All writes under R4_RECHECK."""
import copy, json, pathlib, shutil, sys, tempfile

R4=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R4_RECHECK')
TS=(R4/'LOGS/STAMP').read_text().strip(); PKG=R4/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R4/'WITNESS/W_STATE_CLAIM'; OUT.mkdir(parents=True,exist_ok=True)
BASE=PKG/'EVIDENCE'
def run(tag,mut=None):
    tmp=pathlib.Path(tempfile.mkdtemp(prefix=tag+'_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(BASE,ev); source=ev/'SOURCE_118'
    f=json.loads((ev/'FRAME.json').read_text()); d=json.loads((ev/'DECISION.json').read_text()); c=json.loads((ev/'C.json').read_text())
    if mut: mut(f,d,c)
    def put(n,o):
        b=(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/n).write_bytes(b); return {'path':n,'sha256':sha(b)}
    put('FRAME.json',f); d['common_frame']=put('FRAME.json',f); d['frame_sha256']=digest(f); put('DECISION.json',d); c['integrated_decision']=put('DECISION.json',d); c['integrated_decision_sha256']=digest(d); put('C.json',c)
    return {'FRAME':check('FRAME',f,ev,source,REPO,ZIP),'DECISION':check('DECISION',d,ev,source,REPO,ZIP),'C':check('C_INTEGRATED',c,ev,source,REPO,ZIP)}
rep={'schema':'C_REVIEW_R4_STATE_CLAIM','baseline':run('baseline')}
def p4(f,d,c):
    x=next(x for x in d['identity_dispositions'] if x['identity_id']=='P4R-R01'); x['disposition']='PRESENT_PRESERVED'
rep['P4R-R01_hold_to_present']=run('p4',p4)
def req(f,d,c):
    x=next(x for x in d['requirement_dispositions'] if x['requirement_id']=='REQ-FIELD-FORGE'); x['disposition']='PRESENT_PRESERVED'
rep['REQ-FIELD-FORGE_future_to_present']=run('req',req)
def t4(f,d,c):
    x=c['boundary_court']['T4']; x['claim_grade']='ACTUAL_PROVED'; x['grade']='EXECUTED_AT_SCOPE'; x['actual_first_reader_verified']=True
rep['T4_source_static_to_actual']=run('t4',t4)
def t4fake(f,d,c):
    x=c['boundary_court']['T4']; x['claim_grade']='ACTUAL_PROVED'; x['grade']='EXECUTED_AT_SCOPE'; x['actual_first_reader_verified']=True; x['actual_reader_witness']={'reader_abi':'fake_reader.py::run','exit_code':0,'custody':'EXTERNAL_RUNNER_VERIFIED'}
rep['T4_actual_with_fake_witness']=run('t4fake',t4fake)
def p4b(f,d,c):
    x=next(x for x in d['identity_dispositions'] if x['identity_id']=='P4R-R02'); x['disposition']='PRESENT_PRESERVED'
rep['P4R-R02_analog']=run('p4b',p4b)
def reqb(f,d,c):
    x=next(x for x in d['requirement_dispositions'] if x['requirement_id']=='REQ-SEAM-WORLD-ACTOR'); x['disposition']='PRESENT_PRESERVED'
rep['REQ-SEAM-WORLD-ACTOR_analog']=run('reqb',reqb)
def t6(f,d,c):
    x=c['boundary_court']['T6']; x['claim_grade']='ACTUAL_PROVED'; x['grade']='EXECUTED_AT_SCOPE'; x['actual_first_reader_verified']=True
rep['T6_actual_analog']=run('t6',t6)
def coherent(f,d,c):
    x=next(x for x in d['identity_dispositions'] if x['identity_id']=='P4R-R01'); x['disposition']='PRESENT_PRESERVED'; x['evidence_grade']='EXECUTED_NATIVE'; x['status_assertion']='HISTORICAL_FUNCTION_RETAINED'; x['narrative_sha256']='0'*64
    y=next(x for x in d['requirement_dispositions'] if x['requirement_id']=='REQ-FIELD-FORGE'); y['disposition']='PRESENT_PRESERVED'; y['narrative_sha256']='0'*64
    z=c['boundary_court']['T4']; z['claim_grade']='ACTUAL_PROVED'; z['grade']='EXECUTED_AT_SCOPE'; z['actual_first_reader_verified']=True; z['narrative_sha256']='0'*64
rep['coherent_adversary_recomputed_flags_hashes']=run('coherent',coherent)
# restore exact baseline from fresh archive
rep['restore_exact_baseline']=run('restore')
# usability: changed proposal narrative passes; changed source-bound fate remains red
def proposal(f,d,c): d['architecture_description']='A lawfully changed candidate proposal with preserved typed/source obligations.'; d['single_selected_strategy']='Same source obligations, changed proposal narrative.'
rep['usability_changed_proposal']=run('proposal',proposal)
def fate(f,d,c):
    x=next(x for x in d['identity_dispositions'] if x['identity_id']=='K1-CAP-11'); x['design_effect']='A changed source-bound fate narrative for the same identity.'
rep['usability_changed_source_fate']=run('fate',fate)
(OUT/'r4_state_claim.json').write_text(json.dumps(rep,indent=2)+'\n'); print(json.dumps(rep,indent=2))
