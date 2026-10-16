"""Execute frozen reviewer expectations and record live imported file identities."""
from pathlib import Path
import sys, os, json, subprocess, hashlib, time, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];O=R/'evidence/new';O.mkdir(parents=True,exist_ok=True)
M1=R/'runtime/m05/runtime/m02/runtime/m01'
FREEZE='8f6d11c54f313665e9320d4d58af7b6d1825796e'
freeze=json.loads((R/'03_REVIEWER_FREEZE.json').read_text())
for name,h in freeze['files'].items():
    data=(R/name).read_bytes();assert hashlib.sha256(data).hexdigest()==h
    assert subprocess.check_output(['git','show',FREEZE+':'+str((R/name).relative_to(R.parents[1]))],cwd=R.parents[1])==data
if len(sys.argv)==1:
    cmd=[sys.executable,__file__,'worker'];start=time.monotonic()
    p=subprocess.run(cmd,cwd=R.parents[1],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
    (O/'stdout.log').write_text(p.stdout+p.stderr)
    counts={k:sum(int(s.get(k,0)) for s in ET.parse(O/'junit.xml').getroot().iter('testsuite')) for k in ('tests','failures','errors','skipped')}
    (O/'execution.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode,seconds=time.monotonic()-start,counts=counts,freeze_commit=FREEZE),indent=2)+'\n')
    print(p.stdout[-5000:]);print(counts);raise SystemExit(p.returncode)
sys.path.insert(0,str(M1/'repro'))
import bootstrap
import cell, claim_provenance
from rawlsing_next import v3_psepf_zero_positive_guard as guard
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
guard_before=Path(guard.__file__).read_bytes();assert blob(guard_before)=='e0528d65215cb431196570c38bac4eae94217a1b'
assert not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
args=[str(R/'repro/test_m06.py'),'-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir='+str(R),'--confcutdir='+str(R),'--junitxml='+str(O/'junit.xml')]
code=pytest.main(args)
assert Path(guard.__file__).read_bytes()==guard_before and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
rows=[]
for name,mod in sorted(sys.modules.items()):
    f=getattr(mod,'__file__',None)
    if f and name.startswith(('candidate','rawlsing_next','cell','bootstrap','claim_provenance')) and Path(f).suffix=='.py':
        path=Path(f).resolve();data=path.read_bytes();rows.append(dict(module=name,module_file=str(path.relative_to(R)),blob_sha1=blob(data),sha256=hashlib.sha256(data).hexdigest()))
(O/'actual_imports.json').write_text(json.dumps(dict(imports=rows,guard_empty=True,guard_unchanged=True,pytest_args=args,exit=int(code)),indent=2)+'\n')
raise SystemExit(code)
