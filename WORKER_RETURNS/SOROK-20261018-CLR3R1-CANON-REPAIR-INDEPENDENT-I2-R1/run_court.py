"""Independent runner; exact frozen tests, explicit candidate binding, separate REDs."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,xml.etree.ElementTree as ET
from datetime import datetime,timezone

R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def clean(s):
    s=s.replace(str(R),'RETURN').replace(str(R.parents[1]),'WORKTREE')
    s=re.sub(r'hostname="[^"]*"','hostname="independent-host"',s)
    return s
def frozen_check():
    rows=json.loads((R/'staging_manifest.json').read_text())
    for row in rows:assert sha((R/row['staged']).read_bytes())==row['sha256'],row['staged']
    return len(rows)
def main():
    frozen_check();receipts=[]
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'}
    suites=[
      ('clr3_unchanged','frozen/reconstructed/clr3/test_recursive_court.py',True),
      ('i2_unchanged','frozen/test_independent.py',True),
      ('repair_controls','frozen/repair_r1/test_repair_contracts.py',True),
      ('fresh','test_fresh.py',True),
      ('original_six_red','frozen/reconstructed/clr3/preserved/r1_court/test_falsifiers.py',False),
      ('original_i2_baseline','frozen/test_independent.py',False)]
    for name,test,candidate in suites:
        paths=[str(R/'frozen/repair_r1')] if candidate else [str(R/'frozen/reconstructed/clr3/preserved/r1_court')]
        suite_env={**env,'PYTHONPATH':os.pathsep.join(paths)}
        cmd=[sys.executable,'-m','pytest','-c','/dev/null','--rootdir=.','--confcutdir=.','--import-mode=importlib','-p','no:cacheprovider','-vv']
        if candidate:cmd+=['-p','candidate_binding']
        cmd+=[test,'--junitxml=evidence/'+name+'.xml']
        p=subprocess.run(cmd,cwd=R,env=suite_env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (R/'evidence'/f'{name}.log').write_text(clean(p.stdout))
        x=R/'evidence'/f'{name}.xml';x.write_text(clean(x.read_text()))
        suite=ET.parse(x).getroot().find('testsuite')
        row=dict(suite=name,exit_code=p.returncode,candidate_bound=candidate,command=clean(' '.join(cmd)),pythonpath=clean(suite_env['PYTHONPATH']),**{k:int(suite.attrib[k]) for k in ('tests','failures','errors','skipped')})
        receipts.append(row);print(json.dumps(row),flush=True)
    result=dict(observed_utc=datetime.now(timezone.utc).isoformat(),suites=receipts,frozen_blobs_unchanged=frozen_check(),preregistration_sha256=sha((R/'evidence/preregistration.json').read_bytes()),fresh_suite_sha256=sha((R/'test_fresh.py').read_bytes()))
    (R/'evidence/execution_receipts.json').write_text(json.dumps(result,indent=2)+'\n')
    expected=[(38,0,0,0),(6,0,0,0),(11,0,0,0),(34,0,0,0),(6,6,0,0),(6,2,0,0)]
    observed=[tuple(s[k] for k in ('tests','failures','errors','skipped')) for s in receipts]
    assert observed==expected,(observed,expected)
    return 1  # RED is preserved as an actual failing historical assertion.
if __name__=='__main__':raise SystemExit(main())
