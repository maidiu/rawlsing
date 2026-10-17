"""Cold subprocess courts; originals stay byte-frozen, all adaptations are explicit."""
from pathlib import Path
import subprocess,sys,os,shutil,json,hashlib,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(mode):
 base=ROOT/'runtime'/mode
 for alias in ('F6C','F6J','F6L'):
  shutil.copytree(ROOT/'inherited'/alias,base/alias,dirs_exist_ok=True)
 # The inherited author symlink is replaced with a byte-identified regular fixture.
 fix=base/'F6C/02_TESTS/run/WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py'
 fix.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ROOT/'inherited/F6J/04_TESTS/run/WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py',fix)
 native=(ROOT/'candidate/rawlsing_next' if mode in ('repaired','compat') else ROOT/'inherited/F6J/01_STAGED_NATIVE/rawlsing_next')
 for path in ('F6C/05_NATIVE_STAGE/rawlsing_next','F6J/01_STAGED_NATIVE/rawlsing_next','F6L/01_STAGED_NATIVE/rawlsing_next'):
  shutil.copytree(native,base/path,dirs_exist_ok=True)
 (base/'F6J/07_EVIDENCE').mkdir(exist_ok=True)
 return base

def main(mode):
 if mode not in ('original','repaired','compat'):raise ValueError('unknown court mode')
 base=prepare(mode)
 if mode=='compat':
  from compatibility import adapt
  adapt(base)
 evidence=ROOT/'evidence'/mode;evidence.mkdir(parents=True,exist_ok=True)
 native=base/'F6C/05_NATIVE_STAGE'
 bootstrap='''import sys,runpy,json,hashlib,atexit
from pathlib import Path
stage,receipt,kind,path,*args=sys.argv[1:]
sys.path.insert(0,stage)
import rawlsing_next.pre553_heterogeneous_synthesis as m
import rawlsing_next.pre553_empirical_objects as e
root=Path(stage).resolve().parents[4]
def identity():
 out={}
 for module in (m,e):
  p=Path(module.__file__).resolve();raw=p.read_bytes()
  out[module.__name__]={"module_file":str(p).replace(str(root),"$RETURN"),"sha256":hashlib.sha256(raw).hexdigest(),"git_blob":hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()}
 Path(receipt).write_text(json.dumps(out,indent=2)+'\\n')
atexit.register(identity)
if kind=='pytest':
 import pytest
 sys.exit(pytest.main(args+[path]))
else:
 sys.argv=[path]+args
 runpy.run_path(path,run_name='__main__')
'''
 jobs=[('consumer20','pytest',ROOT/'tests/test_consumer_repair.py'),
       ('inherited35','pytest',base/'F6J/04_TESTS/run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py'),
       ('f6c57','pytest',base/'F6C/02_TESTS/test_f6c_frozen_court.py'),
       ('f6j53','pytest',base/'F6J/04_TESTS/test_f6j_adversarial.py'),
       ('f6l26','pytest',base/'F6L/02_PHASE_A/04_TESTS/test_f6l_phase_a.py'),
       ('rational82','script',base/'F6J/03_SCRIPTS/execute_native_vs_frozen.py'),
       ('rational_analysis','script',base/'F6J/03_SCRIPTS/rational_recomputation.py'),
       ('f6j_falsifiers','script',base/'F6J/03_SCRIPTS/falsifier_attacks.py'),
       ('f6j_admission','script',base/'F6J/03_SCRIPTS/admission_and_consumer_attacks.py')]
 rows=[]
 for name,kind,path in jobs:
  args=['-q','-p','no:cacheprovider','--import-mode=importlib','--rootdir',str(base),f'--junitxml={evidence/name}.xml'] if kind=='pytest' else []
  cmd=[sys.executable,'-B','-c',bootstrap,str(native),str(evidence/(name+'.imports.json')),kind,str(path),*args]
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONPATH=str(ROOT/'scripts'))
  p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
  log=f'exit={p.returncode}\n--- stdout ---\n{p.stdout}\n--- stderr ---\n{p.stderr}'
  (evidence/(name+'.log')).write_text(log.replace(str(ROOT),'$RETURN').replace(str(ROOT.parents[1]),'$WORKTREE'))
  row=dict(name=name,kind=kind,exit=p.returncode,argv=[str(x).replace(str(ROOT),'$RETURN') for x in cmd],cwd='$RETURN',log_sha256=sha(evidence/(name+'.log')),log=f'evidence/{mode}/{name}.log',imports=f'evidence/{mode}/{name}.imports.json')
  if kind=='pytest':
   jp=evidence/(name+'.xml')
   if jp.exists():
    text=jp.read_text().replace(str(ROOT),'$RETURN');jp.write_text(text)
    suites=list(ET.parse(jp).getroot().iter('testsuite'))
    row['counts']={k:sum(int(s.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
    row['failures']=[c.get('name') for c in ET.parse(jp).getroot().iter('testcase') if c.find('failure') is not None or c.find('error') is not None]
  print(name,row.get('counts','script'), 'exit',p.returncode,flush=True);rows.append(row)
 for name in ('native_vs_frozen.json','falsifier_attacks.json','admission_and_consumer_attacks.json'):
  origin=base/'F6J/07_EVIDENCE'/name
  if origin.exists():shutil.copyfile(origin,evidence/name)
 rational=base/'F6J/02_RATIONAL_RECOMPUTATION.json'
 if rational.exists():shutil.copyfile(rational,evidence/rational.name)
 (evidence/'courts.json').write_text(json.dumps(rows,indent=2)+'\n')
 return 1 if mode=='compat' and any(r['exit'] for r in rows) else 0
if __name__=='__main__':sys.exit(main(sys.argv[1]))
