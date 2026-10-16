"""Run unchanged pinned suites, preserving actual output and fail counts."""
from pathlib import Path
import subprocess, os, sys, json, shutil, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]; M=R/'runtime/m05'
def counts(folder):
    result={k:0 for k in ('tests','failures','errors','skipped')}
    for path in folder.rglob('junit.xml'):
        for suite in ET.parse(path).getroot().iter('testsuite'):
            for key in result: result[key]+=int(suite.get(key,0))
    return result
def run():
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    result=[]
    for script,source,dest,n,f in [('review/run_phase.py','evidence/after','baseline638',638,0),('review/run_author.py','evidence/m05_author','m05_author48',48,0),('repro/run_historical.py','evidence/historical_nine','historical_nine',9,9)]:
        cmd=[sys.executable,str(M/script)]+(['after'] if dest=='baseline638' else [])
        p=subprocess.run(cmd,cwd=R.parents[1],env=env,capture_output=True,text=True)
        out=R/'evidence'/dest;shutil.copytree(M/source,out,dirs_exist_ok=True)
        (out/'m06_launcher.stdout').write_text(p.stdout+p.stderr)
        row=dict(command=cmd,exit=p.returncode,counts=counts(out),court=dest);result.append(row)
        print(dest,row['counts'],flush=True)
        assert p.returncode==0 and row['counts']==dict(tests=n,failures=f,errors=0,skipped=0)
    (R/'evidence/baseline_execution.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':run()
