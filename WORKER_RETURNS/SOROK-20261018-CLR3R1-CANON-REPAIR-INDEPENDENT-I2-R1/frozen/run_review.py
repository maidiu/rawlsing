"""Reproduce exact suites; deliberately exit 1 for preserved RED evidence."""
import hashlib,json,os,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from reconstruct import ROOT

def sanitize(text):
    text=text.replace(str(ROOT),'<I2_RETURN>').replace(str(ROOT.parent.parent),'<REVIEW_WORKTREE>')
    text=text.replace(str(ROOT.parent.parent.parent),'<ARTIFACT_ESTATE>').replace(sys.executable,'<PYTHON>')
    return re.sub(r'hostname="[^"]*"','hostname="review-host"',text)

def verify_sources():
    for r in json.loads((ROOT/'evidence/reconstruction_manifest.json').read_text()):
        assert hashlib.sha256((ROOT/r['local_path']).read_bytes()).hexdigest()==r['sha256'],r['local_path']
    pre=json.loads((ROOT/'evidence/independent_preregistration.json').read_text())
    assert hashlib.sha256((ROOT/'test_independent.py').read_bytes()).hexdigest()==pre['suite_sha256']

def run():
    verify_sources()
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONPATH':str(ROOT/'.runtime')}
    receipts=[]
    suites=[('clr3',ROOT/'reconstructed/clr3','test_recursive_court.py'),('original_six_red',ROOT/'reconstructed/clr3/preserved/r1_court','test_falsifiers.py'),('independent',ROOT,'test_independent.py')]
    for name,cwd,test in suites:
        xml=ROOT/'evidence'/f'{name}.xml'
        command=[sys.executable,'-m','pytest','-c','/dev/null','--rootdir=.','--confcutdir=.','-v','-p','no:cacheprovider',test,'--junitxml='+os.path.relpath(xml,cwd)]
        result=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (ROOT/'evidence'/f'{name}.log').write_text(sanitize(result.stdout))
        xml.write_text(sanitize(xml.read_text()))
        suite=ET.parse(xml).getroot().find('testsuite')
        receipts.append(dict(suite=name,command=['python3',*command[1:]],cwd=str(cwd.relative_to(ROOT)),exit_code=result.returncode,**{k:int(suite.attrib[k]) for k in ['tests','failures','errors','skipped']},junit=f'evidence/{name}.xml'))
    capture=subprocess.run([sys.executable,str(ROOT/'capture_execution.py')],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (ROOT/'evidence/capture_execution.log').write_text(sanitize(capture.stdout))
    assert capture.returncode==0,capture.stdout
    # Whole trajectories in cold interpreters, not just one label/endpoint.
    code="import json; from recursive_court import run_trajectory; print(json.dumps({w:run_trajectory(w)['trace_hash'] for w in ('HOURS_CUT','ROUTINE','RAISE_WITH_OVERTIME')},sort_keys=True))"
    cold=[]
    for seed in [0,1,71,123]:
        p=subprocess.run([sys.executable,'-c',code],cwd=ROOT/'reconstructed/clr3',env={**env,'PYTHONHASHSEED':str(seed)},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert p.returncode==0,p.stdout
        cold.append(dict(hash_seed=seed,exit_code=p.returncode,trace_hashes=json.loads(p.stdout)))
    assert len({json.dumps(r['trace_hashes'],sort_keys=True) for r in cold})==1
    (ROOT/'evidence/cold_replay.json').write_text(json.dumps(cold,indent=2)+'\n')
    verify_sources()
    versions=subprocess.check_output([sys.executable,'-c','import platform,pytest,yaml;print(platform.python_version(),pytest.__version__,yaml.__version__)'],env=env,text=True).strip()
    result=dict(observed_utc=datetime.now(timezone.utc).isoformat(),versions=versions,environment={'PYTHONPATH':'<I2_RETURN>/.runtime','PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'},suites=receipts,cold_processes=len(cold),source_bytes_verified_before_after=True,original_assertions_edited=False)
    (ROOT/'evidence/execution_receipts.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert [(r['tests'],r['failures'],r['errors'],r['skipped'],r['exit_code']) for r in receipts]==[(38,0,0,0,0),(6,6,0,0,1),(6,2,0,0,1)]
    return 1

if __name__=='__main__':raise SystemExit(run())
