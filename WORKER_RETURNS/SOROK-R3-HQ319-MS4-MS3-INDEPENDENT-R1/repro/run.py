"""Independent MS4 runner: literal source suites, real pytest/JUnit/stdout/imports."""
from pathlib import Path
import sys, os, subprocess, json, hashlib, time, xml.etree.ElementTree as ET, shutil
R=Path(__file__).resolve().parents[1]; S=R/'staging/ms3'; M2=S/'staging/ms2'; RT=M2/'staging/ms1/runtime'
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def suites():return {'original120':[RT/'candidate/can2_test_repair.py',RT/'test_ms1_serial.py'],'ms2_51':[M2/'repro/test_ms2.py'],'p3b':[M2/'repro/test_literal_p3b.py'],'author47':[S/'repro/test_author.py'],'selector12':[S/'repro/test_selector_extension_v2.py'],'hostile':[R/'repro/test_ms4.py']}
if __name__=='__main__':
    phase=sys.argv[1]
    if sys.argv[-1]!='worker':
        rows=[]
        for court in sys.argv[2:]:
            o=R/'evidence'/phase/court; o.mkdir(parents=True,exist_ok=True)
            cmd=[sys.executable,str(Path(__file__).relative_to(R)),phase,court,'worker']; start=time.monotonic()
            p=subprocess.run(cmd,cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
            (o/'stdout.log').write_text(p.stdout+p.stderr)
            counts={k:sum(int(s.get(k,0)) for s in ET.parse(o/'junit.xml').getroot().iter('testsuite')) for k in ['tests','failures','errors','skipped']}
            rows.append(dict(court=court,command=cmd,exit=p.returncode,seconds=time.monotonic()-start,counts=counts));print(phase,court,p.returncode,counts,flush=True)
        (R/'evidence'/phase/'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
    else:
        court=sys.argv[2];o=R/'evidence'/phase/court;o.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(RT))
        import pytest
        args=[str(p.relative_to(R)) for p in suites()[court]]+['-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir=.', '--junitxml='+str((o/'junit.xml').relative_to(R))]
        code=pytest.main(args)
        imports=[]
        for name,m in sorted(sys.modules.items()):
            f=getattr(m,'__file__',None)
            if f and name.startswith(('candidate','ms1_serial','ms3_native_custody','rawlsing_next')) and Path(f).suffix=='.py':
                p=Path(f).resolve(); b=p.read_bytes();imports.append(dict(module=name,module_file=str(p.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
        (o/'actual_imports.json').write_text(json.dumps(dict(imports=imports,pytest_args=args),indent=2)+'\n');raise SystemExit(code)
