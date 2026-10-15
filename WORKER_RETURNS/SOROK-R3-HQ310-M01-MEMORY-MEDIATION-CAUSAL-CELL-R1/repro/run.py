"""Fresh-process execution with JUnit/stdout and exact imported source receipts."""
import bootstrap
from bootstrap import R,S,CAN
from pathlib import Path
import subprocess,sys,json,hashlib,xml.etree.ElementTree as ET,shutil

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if len(sys.argv)==1:
 rows=[]
 for suite in ['new','can3','author','owners']:
  out=R/'evidence'/suite;out.mkdir(parents=True,exist_ok=True)
  with (out/'stdout.log').open('w') as f:run=subprocess.run([sys.executable,__file__,suite],stdout=f,stderr=subprocess.STDOUT)
  counts={};p=out/'junit.xml'
  if p.exists():
   ts=list(ET.parse(p).getroot().iter('testsuite'));counts={k:sum(int(t.get(k,0)) for t in ts) for k in ['tests','failures','errors','skipped']}
  row=dict(suite=suite,returncode=run.returncode,counts=counts);rows.append(row);print(row,flush=True)
 (R/'03_RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n');raise SystemExit(any(x['returncode'] for x in rows))
suite=sys.argv[1];out=R/'evidence'/suite;out.mkdir(parents=True,exist_ok=True)
# Keep CAN3 originals untouched; rerun exact test bytes in a distinct harness root.
T=R/'runtime/can3_rerun';(T/'repro').mkdir(parents=True,exist_ok=True)
shutil.copyfile(R/'runtime/can3/repro/test_can3.py',T/'repro/test_can3.py')
shutil.copytree(R/'runtime/can3/runtime/law',T/'runtime/law',dirs_exist_ok=True)
N=['test_psepf_zero_positive_guard','test_sdtf_r4_mechanism_rule_authority_binding','test_sdtf_r4_r2_current_rule_admission_seam','test_m6_actor_safe_expression']
paths={'new':[R/'repro/test_m01.py'],'can3':[T/'repro/test_can3.py'],'author':[R/'runtime/can3/runtime/author/repro/test_repair.py'],'owners':[S/'rawlsing_next/tests'/(n+'.py') for n in N]}
# CAN2 author tests require their staged helper and original independent harness.
A=R/'runtime/can3/runtime/author';C=A/'runtime_root/court_repaired'
(C/'repro').mkdir(exist_ok=True)
for n in ['test_independent.py','causal_probe.py']:shutil.copyfile(A/'inherited/repro'/n,C/'repro'/n)
shutil.copyfile(A/'00_INHERITED_FROZEN_PREREG.json',C/'00_INHERITED_FROZEN_PREREG.json')
sys.path[:0]=[str(C/'repro'),str(A/'repro')]
from rawlsing_next import v3_psepf_zero_positive_guard as guard
p=Path(guard.__file__);before=p.read_bytes();assert blob(before)=='e0528d65215cb431196570c38bac4eae94217a1b';assert not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
args=['-q','--tb=short','--rootdir='+str(R),'--confcutdir='+str(R),*map(str,paths[suite]),'--junitxml='+str(out/'junit.xml')]
code=pytest.main(args)
assert before==p.read_bytes() and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
imports=[]
for name,module in sorted(sys.modules.items()):
 f=getattr(module,'__file__',None)
 if f and name.startswith(('candidate','rawlsing_next','cell','bootstrap','owner_effect_stub')) and Path(f).suffix=='.py':
  p=Path(f).resolve();imports.append(dict(module=name,file=str(p.relative_to(R)),blob_sha1=blob(p.read_bytes()),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(out/'execution.json').write_text(json.dumps(dict(command=['python3','repro/run.py',suite],pytest_args=[x.replace(str(R),'<RETURN>') for x in args],exit_code=int(code),imports=imports,guard_byte_unchanged=True,guard_empty=True),indent=2)+'\n')
if suite=='can3' and (T/'evidence').exists():shutil.copytree(T/'evidence',out/'rerun_observations',dirs_exist_ok=True)
raise SystemExit(code)
