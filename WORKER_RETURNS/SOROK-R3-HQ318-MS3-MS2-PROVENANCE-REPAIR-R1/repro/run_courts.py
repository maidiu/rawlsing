"""Run unchanged original171 and separate original P3b, retaining true REDs."""
from pathlib import Path
import subprocess,sys,os,json,time,hashlib,shutil,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];M2=R/'staging/ms2';RT=M2/'staging/ms1/runtime'
phase=sys.argv[1];assert phase in ['before','after','author']
out=R/'evidence'/phase;out.mkdir(parents=True,exist_ok=True)
if sys.argv[-1]!='worker':
    courts=['author'] if phase=='author' else ['original120','ms2_51','literal_p3b'];rows=[]
    for court in courts:
        cmd=[sys.executable,__file__,phase,court,'worker'];t=time.monotonic();p=subprocess.run(cmd,cwd=R.parents[1],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
        o=out/court;o.mkdir(exist_ok=True);(o/'stdout.log').write_text(p.stdout+p.stderr)
        counts={k:sum(int(s.get(k,0)) for s in E.parse(o/'junit.xml').getroot().iter('testsuite')) for k in ['tests','failures','errors','skipped']}
        if court=='ms2_51':shutil.copytree(M2/'evidence/new/observations',o/'observations',dirs_exist_ok=True)
        if court=='literal_p3b':shutil.copyfile(M2/'evidence/literal_p3b/counterfactual.json',o/'counterfactual.json')
        row=dict(court=court,command=cmd,exit=p.returncode,seconds=time.monotonic()-t,counts=counts);rows.append(row);print(phase,court,p.returncode,counts,flush=True)
    (out/'execution.json').write_text(json.dumps(rows,indent=2)+'\n');raise SystemExit(0)
court=sys.argv[2];o=out/court;o.mkdir(exist_ok=True);sys.path.insert(0,str(RT))
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=R.parents[1])
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
paths={'original120':[RT/'candidate/can2_test_repair.py',RT/'test_ms1_serial.py'],'ms2_51':[M2/'repro/test_ms2.py'],'literal_p3b':[M2/'repro/test_literal_p3b.py'],'author':[R/'repro/test_author.py']}[court]
if court!='author':
    for path in paths:
        sha='34b96ea98de181ca5264f0eed3824cad2db7cfc0' if path.is_relative_to(M2/'repro') else 'd40cc32ecec8f681dcced6a482b6438a86080899'
        prefix='WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1' if sha.startswith('34b') else 'WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1'
        rel=path.relative_to(M2) if sha.startswith('34b') else path.relative_to(M2/'staging/ms1')
        assert path.read_bytes()==git('show',sha+':'+prefix+'/'+str(rel))
else:
    f=json.loads((R/'03_AUTHOR_FREEZE.json').read_text())
    for n,h in f['files'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h
from rawlsing_next import v3_psepf_zero_positive_guard as guard
guard_bytes=Path(guard.__file__).read_bytes();assert blob(guard_bytes)=='e0528d65215cb431196570c38bac4eae94217a1b' and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest
args=[*map(str,paths),'-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir='+str(M2 if court!='author' else R),'--junitxml='+str(o/'junit.xml')]
code=pytest.main(args)
assert Path(guard.__file__).read_bytes()==guard_bytes and not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
rows=[]
for name,m in sorted(sys.modules.items()):
    file=getattr(m,'__file__',None)
    if file and name.startswith(('candidate','ms1_serial','ms3_native_custody','rawlsing_next')) and Path(file).suffix=='.py':
        path=Path(file).resolve();b=path.read_bytes();rows.append(dict(module=name,module_file=str(path.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
(o/'actual_imports.json').write_text(json.dumps(dict(imports=rows,pytest_args=args,guard_empty=True,guard_unchanged=True),indent=2)+'\n')
raise SystemExit(code)
