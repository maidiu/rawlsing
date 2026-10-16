"""Execute frozen MS2 expectations without suppressing scientific REDs."""
from pathlib import Path
import subprocess,sys,os,json,hashlib,time,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];RT=R/'staging/ms1/runtime'
FREEZE='6a1e733cd92113b10ba85db4e93f13e9ef9861b5'
mode=sys.argv[1];assert mode in ['new','literal_p3b'];O=R/'evidence'/mode;O.mkdir(parents=True,exist_ok=True)
for name,h in json.loads((R/'03_REVIEWER_FREEZE.json').read_text())['files'].items():
    b=(R/name).read_bytes();assert hashlib.sha256(b).hexdigest()==h
    assert b==subprocess.check_output(['git','show',FREEZE+':'+str((R/name).relative_to(ROOT))],cwd=ROOT)
if sys.argv[-1]!='worker':
    cmd=[sys.executable,__file__,mode,'worker'];start=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
    (O/'stdout.log').write_text(p.stdout+p.stderr)
    counts={k:sum(int(s.get(k,0)) for s in E.parse(O/'junit.xml').getroot().iter('testsuite')) for k in ['tests','failures','errors','skipped']}
    (O/'execution.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode,seconds=time.monotonic()-start,freeze_commit=FREEZE,counts=counts,no_xfail_or_oracle_repair=True),indent=2)+'\n')
    print(p.stdout[-6500:]);print(counts)
    raise SystemExit(p.returncode)
sys.path.insert(0,str(RT))
import ms1_serial
from rawlsing_next import v3_psepf_zero_positive_guard as guard
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
before=Path(guard.__file__).read_bytes();assert blob(before)=='e0528d65215cb431196570c38bac4eae94217a1b' and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
path=R/'repro'/('test_ms2.py' if mode=='new' else 'test_literal_p3b.py')
args=[str(path),'-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir='+str(R),'--junitxml='+str(O/'junit.xml')]
code=pytest.main(args);assert Path(guard.__file__).read_bytes()==before and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
rows=[]
for name,m in sorted(sys.modules.items()):
    f=getattr(m,'__file__',None)
    if f and name.startswith(('candidate','ms1_serial','rawlsing_next')) and Path(f).suffix=='.py':
        path=Path(f).resolve();data=path.read_bytes();rows.append(dict(module=name,module_file=str(path.relative_to(R)),blob_sha1=blob(data),sha256=hashlib.sha256(data).hexdigest()))
(O/'actual_imports.json').write_text(json.dumps(dict(imports=rows,pytest_args=args,guard_empty=True,guard_unchanged=True),indent=2)+'\n')
raise SystemExit(code)
