"""Real independent pytest, stdout/JUnit, per-court source/import custody."""
from pathlib import Path
import os,sys,subprocess,time,json,hashlib,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];RT=R/'staging/runtime'
def main():
    court=sys.argv[1];out=R/'evidence'/court;out.mkdir(parents=True,exist_ok=True)
    if sys.argv[-1]!='worker':
        cmd=[sys.executable,'repro/run.py',court,'worker'];start=time.monotonic()
        env=dict(os.environ,C0P_RUNTIME=str(RT),C0P_REPO=str(R.parents[1]),C0P_ORACLES=str(R/'staging/oracles'),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',C0I_COURT=court)
        p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True);(out/'stdout.log').write_text(p.stdout+p.stderr)
        counts={k:sum(int(x.get(k,0)) for x in E.parse(out/'junit.xml').getroot().iter('testsuite')) for k in ['tests','failures','errors','skipped']}
        row=dict(command=cmd,exit=p.returncode,seconds=time.monotonic()-start,counts=counts);(out/'execution.json').write_text(json.dumps(row,indent=2)+'\n');print(court,row)
    else:
        sys.path.insert(0,str(RT))
        paths={'author49':['staging/c0p/tests/test_c0p_generic_port.py'],'hostile':['repro/test_c0i.py']}[court]
        if court=='hostile':
            for n,h in json.loads((R/'03_FREEZE.json').read_text())['files'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h
        import pytest
        args=paths+['-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir=.','--junitxml='+str((out/'junit.xml').relative_to(R))];code=pytest.main(args)
        imports=[]
        for name,m in sorted(sys.modules.items()):
            f=getattr(m,'__file__',None)
            if f and Path(f).suffix=='.py' and Path(f).resolve().is_relative_to(R):
                p=Path(f).resolve();b=p.read_bytes();imports.append(dict(module=name,module_file=str(p.relative_to(R)),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
        (out/'actual_imports.json').write_text(json.dumps(dict(pytest_args=args,imports=imports),indent=2)+'\n');raise SystemExit(code)
if __name__=='__main__':main()
