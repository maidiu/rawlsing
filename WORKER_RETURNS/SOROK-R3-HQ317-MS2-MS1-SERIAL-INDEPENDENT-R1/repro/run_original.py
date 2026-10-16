"""Literal original120 court. An exit1 with two failures remains two failures."""
from pathlib import Path
import subprocess,sys,os,json,hashlib,time,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];RT=R/'staging/ms1/runtime';O=R/'evidence/original';O.mkdir(parents=True,exist_ok=True)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if len(sys.argv)==1:
    cmd=[sys.executable,__file__,'worker'];t=time.monotonic();p=subprocess.run(cmd,cwd=RT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
    (O/'stdout.log').write_text(p.stdout+p.stderr);counts={k:sum(int(s.get(k,0)) for s in E.parse(O/'junit.xml').getroot().iter('testsuite')) for k in ['tests','failures','errors','skipped']}
    (O/'execution.json').write_text(json.dumps(dict(command=cmd,cwd=str(RT),exit=p.returncode,seconds=time.monotonic()-t,counts=counts,expected_original_failures_retained=True),indent=2)+'\n')
    print(p.stdout[-4000:]);assert counts==dict(tests=120,failures=2,errors=0,skipped=0) and p.returncode==1
    raise SystemExit(0)
sys.path.insert(0,str(RT))
from rawlsing_next import v3_psepf_zero_positive_guard as guard
p=Path(guard.__file__);before=p.read_bytes();assert blob(before)=='e0528d65215cb431196570c38bac4eae94217a1b' and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
args=[str(RT/'candidate/can2_test_repair.py'),str(RT/'test_ms1_serial.py'),'-vv','--tb=short','--noconftest','-p','no:cacheprovider','--rootdir='+str(RT),'--junitxml='+str(O/'junit.xml')]
code=pytest.main(args);assert p.read_bytes()==before and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
rows=[]
for name,m in sorted(sys.modules.items()):
    f=getattr(m,'__file__',None)
    if f and name.startswith(('candidate','ms1_serial','rawlsing_next')) and Path(f).suffix=='.py':
        path=Path(f).resolve();b=path.read_bytes();rows.append(dict(module=name,module_file=str(path.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
(O/'actual_imports.json').write_text(json.dumps(dict(imports=rows,pytest_args=args,guard_empty=True,guard_unchanged=True),indent=2)+'\n')
raise SystemExit(code)
