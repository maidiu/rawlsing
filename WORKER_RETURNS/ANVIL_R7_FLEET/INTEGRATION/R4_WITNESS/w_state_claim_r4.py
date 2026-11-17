#!/usr/bin/env python3
import copy,json,pathlib,shutil,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
INT=ROOT.parent
PKG=INT/'REPAIRED_PACKAGE/ANVIL_R7';sys.path.insert(0,str(PKG/'tools'))
from r7_integrated import check,digest,sha
REPO='/Users/matthewsmith/s2b-work/rawlsing';ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=ROOT/'OUT';OUT.mkdir(exist_ok=True)
base_ev=PKG/'EVIDENCE';source0=base_ev/'SOURCE_118'
def run_case(name,mut):
    ev=OUT/name/'EVIDENCE';shutil.copytree(base_ev,ev)
    f=json.loads((ev/'FRAME.json').read_text());d=json.loads((ev/'DECISION.json').read_text());c=json.loads((ev/'C.json').read_text())
    mut(f,d,c)
    def put(n,o):
        b=(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();(ev/n).write_bytes(b);return {'path':n,'sha256':sha(b)}
    put('FRAME.json',f);d['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())};d['frame_sha256']=digest(f);put('DECISION.json',d)
    c['integrated_decision']={'path':'DECISION.json','sha256':sha((ev/'DECISION.json').read_bytes())};c['integrated_decision_sha256']=digest(d);put('C.json',c)
    de=check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP);cc=check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)
    res={'case':name,'DECISION':de,'C':cc,'refused':de['status']=='RED' or cc['status']=='RED'}
    (OUT/name/'result.json').write_text(json.dumps(res,indent=2)+'\n');print(name,res['refused'],de['status'],cc['status']);return res
def ident(rid,state):
    def m(f,d,c):
        for x in d['identity_dispositions']:
            if x['identity_id']==rid:x['disposition']=state
    return m
def req(rid,state):
    def m(f,d,c):
        for x in d['requirement_dispositions']:
            if x['requirement_id']==rid:x['disposition']=state
    return m
def bnd(t):
    def m(f,d,c):
        x=c['boundary_court'][t];x['claim_grade']='ACTUAL_PROVED';x['grade']='EXECUTED_AT_SCOPE';x['actual_first_reader_verified']=True
    return m
cases=[('R3_1_identity_P4R_R01',ident('P4R-R01','PRESENT_PRESERVED')),('R3_2_requirement_FIELD_FORGE',req('REQ-FIELD-FORGE','PRESENT_PRESERVED')),('R3_3_boundary_T4',bnd('T4')),('ANALOG_identity_P4R_R02',ident('P4R-R02','PRESENT_PRESERVED')),('ANALOG_requirement_SEAM',req('REQ-SEAM-WORLD-ACTOR','PRESENT_PRESERVED')),('ANALOG_boundary_T6',bnd('T6'))]
results=[run_case(n,m) for n,m in cases]
# exact baseline restore
ev=OUT/'RESTORE'/'EVIDENCE';shutil.copytree(base_ev,ev);f=json.loads((ev/'FRAME.json').read_text());d=json.loads((ev/'DECISION.json').read_text());c=json.loads((ev/'C.json').read_text())
fr=check('FRAME',f,ev,ev/'SOURCE_118',REPO,ZIP);de=check('DECISION',d,ev,ev/'SOURCE_118',REPO,ZIP);cc=check('C_INTEGRATED',c,ev,ev/'SOURCE_118',REPO,ZIP)
rep={'schema':'ANVIL_R4_STATE_CLAIM','cases':results,'restore':{'FRAME':fr,'DECISION':de,'C':cc},'all_refused':all(x['refused'] for x in results),'restore_pass':all(x['status'].startswith('PASS') for x in (fr,de,cc))}
(OUT/'R4_RESULT.json').write_text(json.dumps(rep,indent=2)+'\n');print(json.dumps({'all_refused':rep['all_refused'],'restore_pass':rep['restore_pass']}))
