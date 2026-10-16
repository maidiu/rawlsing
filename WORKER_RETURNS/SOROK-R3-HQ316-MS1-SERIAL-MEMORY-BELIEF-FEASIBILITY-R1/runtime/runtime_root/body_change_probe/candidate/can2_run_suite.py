"""Fresh-process independent rerun; pin provenance and guard before/after."""
from pathlib import Path
import sys,os,json,hashlib,time,subprocess
RET=Path(__file__).resolve().parents[1];ROOT=RET/'runtime_root/source';CAN=ROOT/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1'
sys.path[:0]=[str(Path(__file__).parent),str(ROOT),str(CAN),str(CAN/'candidate'),str(CAN/'rsm_court_reproduction')]
name=sys.argv[1];base=name.split('__')[0];out=RET/'repro/runs'/name;out.mkdir(parents=True,exist_ok=False)
os.environ['HQ300_STAGE']=str(ROOT);os.environ['HQ298_STAGE']=str(ROOT)
if base=='candidate_unset':os.environ.pop('HQ300_STAGE',None)
import rawlsing_next.v3_psepf_zero_positive_guard as guard
from types import MappingProxyType
assert isinstance(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES,MappingProxyType)
assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)=={}
gp=Path(guard.__file__);before=gp.read_bytes();assert hashlib.sha1(b'blob '+str(len(before)).encode()+b'\0'+before).hexdigest()=='e0528d65215cb431196570c38bac4eae94217a1b'
TESTS=['test_wsc_gt0_protocol','test_wsc_gt0_end_to_end_integrated','test_wsc_gt0_prev3_bridge','test_psepf_zero_positive_guard','test_sdtf_r4_world_response_redrive','test_sdtf_r4_mechanism_rule_authority_binding','test_sdtf_r4_r2_current_rule_admission_seam','test_sdtf_r4_witness_currentness','test_sdtf_r4_d1_hosting_replay','test_m6_actor_safe_expression']
paths={'owners':[ROOT/'rawlsing_next/tests'/(n+'.py') for n in TESTS], 'rsm':[CAN/'rsm_court_reproduction/test_owner_effect_court.py'],'candidate':[CAN/'candidate/test_hq300_court.py'],'candidate_unset':[CAN/'candidate/test_hq300_court.py'],'reviewer':[RET/'repro/test_independent.py']}
import pytest
start=time.time();code=pytest.main(['-q','--tb=short','--rootdir='+str(RET),'--confcutdir='+str(RET),*map(str,paths[base]),'--junitxml='+str(out/'junit.xml')])
assert gp.read_bytes()==before and dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)=={}
imports=[]
for n,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and n.startswith(('candidate','rawlsing_next','owner_effect_stub')):
  p=Path(f).resolve()
  if p.is_file() and p.suffix=='.py':
   b=p.read_bytes();imports.append(dict(module=n,file=str(p.relative_to(RET)),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
(out/'execution.json').write_text(json.dumps(dict(suite=name,exit_code=int(code),seconds=time.time()-start,imports=imports,guard_before_after='mappingproxy({}) unchanged',guard_blob='e0528d65215cb431196570c38bac4eae94217a1b',command='python3 repro/run_suite.py '+name),indent=2)+'\n')
raise SystemExit(code)
