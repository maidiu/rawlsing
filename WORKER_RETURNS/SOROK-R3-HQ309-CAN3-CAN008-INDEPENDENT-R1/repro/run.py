"""Fresh-process unchanged historical suites, actual imports, registry custody."""
from pathlib import Path
import sys,os,json,hashlib,shutil,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];A=R/'runtime/author';C=A/'runtime_root/court_repaired';S=C/'runtime_root/source';CAN=S/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1'
if len(sys.argv)==1:
 rows=[]
 for suite in ['owners','rsm','candidate','rcp3','author','independent']:
  out=R/'evidence'/suite;out.mkdir(parents=True,exist_ok=True)
  with (out/'stdout.log').open('w') as f:code=subprocess.run([sys.executable,__file__,suite],stdout=f,stderr=subprocess.STDOUT).returncode
  p=out/'junit.xml'
  if p.exists():
   ts=list(ET.parse(p).getroot().iter('testsuite'));counts={k:sum(int(t.get(k,0)) for t in ts) for k in ['tests','failures','errors','skipped']}
  else:counts={'missing_junit':True}
  row=dict(suite=suite,exit_code=code,counts=counts);rows.append(row);print(row,flush=True)
 (R/'02_RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n');raise SystemExit()
suite=sys.argv[1];(C/'repro').mkdir(exist_ok=True)
for n in ['test_independent.py','causal_probe.py']:
 shutil.copyfile(A/'inherited/repro'/n,C/'repro'/n)
shutil.copyfile(A/'00_INHERITED_FROZEN_PREREG.json',C/'00_INHERITED_FROZEN_PREREG.json')
sys.path[:0]=[str(C/'repro'),str(S),str(CAN),str(CAN/'candidate'),str(CAN/'rsm_court_reproduction')]
os.environ.update(HQ300_STAGE=str(S),HQ298_STAGE=str(S))
N=['test_wsc_gt0_protocol','test_wsc_gt0_end_to_end_integrated','test_wsc_gt0_prev3_bridge','test_psepf_zero_positive_guard','test_sdtf_r4_world_response_redrive','test_sdtf_r4_mechanism_rule_authority_binding','test_sdtf_r4_r2_current_rule_admission_seam','test_sdtf_r4_witness_currentness','test_sdtf_r4_d1_hosting_replay','test_m6_actor_safe_expression']
paths={'owners':[S/'rawlsing_next/tests'/(n+'.py') for n in N],'rsm':[CAN/'rsm_court_reproduction/test_owner_effect_court.py'],'candidate':[CAN/'candidate/test_hq300_court.py'],'rcp3':[C/'repro/test_independent.py'],'author':[A/'repro/test_repair.py'],'independent':[R/'repro/test_can3.py']}
from rawlsing_next import v3_psepf_zero_positive_guard as g
p=Path(g.__file__);before=p.read_bytes()
def bh(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert bh(before)=='e0528d65215cb431196570c38bac4eae94217a1b';assert not g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
out=R/'evidence'/suite;out.mkdir(parents=True,exist_ok=True)
args=['-q','--tb=short','--rootdir='+str(R),'--confcutdir='+str(R),*map(str,paths[suite]),'--junitxml='+str(out/'junit.xml')]
code=pytest.main(args)
assert p.read_bytes()==before and not g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
imports=[]
for n,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and n.startswith(('candidate','rawlsing_next','owner_effect_stub')) and Path(f).suffix=='.py':
  p=Path(f).resolve();imports.append(dict(module=n,file=str(p.relative_to(R)),blob_sha1=bh(p.read_bytes())))
(out/'execution.json').write_text(json.dumps(dict(command=['python3','repro/run.py',suite],pytest_args=[x.replace(str(R),'<RETURN>') for x in args],exit_code=int(code),imports=imports,guard_byte_unchanged=True,guard_empty=True),indent=2)+'\n')
raise SystemExit(code)
