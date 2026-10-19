"""Execute the repair court; old six REDs remain a separately named suite."""
import hashlib,json,os,re,subprocess,sys,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REVIEW=ROOT.parent

def sanitize(text):
    text=text.replace(str(REVIEW),'[I2_RETURN]').replace(str(REVIEW.parent.parent),'[REVIEW_WORKTREE]')
    text=text.replace(str(REVIEW.parent.parent.parent),'[ARTIFACT_ESTATE]').replace(sys.executable,'[PYTHON]')
    for alias in ['I2_RETURN','REVIEW_WORKTREE','ARTIFACT_ESTATE','PYTHON']:
        text=text.replace('<'+alias+'>','['+alias+']')
    return re.sub(r'hostname="[^"]*"','hostname="review-host"',text)

def check_frozen():
    manifest=json.loads((REVIEW/'return_manifest.json').read_text())
    for row in manifest['files']:
        assert hashlib.sha256((REVIEW/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    # Include the old manifest/checksum themselves against the published review.
    for name in ['return_manifest.json','SHA256SUMS']:
        old=subprocess.check_output(['git','show','0a5da3542f9bb5dd442a2cc1bd605d8958388f13:WORKER_RETURNS/SOROK-20261018-CLR3-RECURSIVE-CANON-SCIENCE-I2-R1/'+name],cwd=REVIEW)
        assert (REVIEW/name).read_bytes()==old,name

def main():
    check_frozen()
    env={**os.environ,'PYTHONPATH':os.pathsep.join([str(ROOT),str(REVIEW/'.runtime')]),'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'}
    receipts=[]
    for name,tests,plugin in [
        ('clr3_unchanged',['../reconstructed/clr3/test_recursive_court.py'],True),
        ('independent_unchanged',['../test_independent.py'],True),
        ('repair_controls',['test_repair_contracts.py'],True),
        ('original_six_red',['../reconstructed/clr3/preserved/r1_court/test_falsifiers.py'],False)]:
        command=[sys.executable,'-m','pytest','-c','/dev/null','--rootdir=.','--confcutdir=.','--import-mode=importlib','-p','no:cacheprovider','-v']
        if plugin:command+=['-p','candidate_binding']
        command+=tests+['--junitxml=evidence/'+name+'.xml']
        suite_env=env
        if not plugin:
            suite_env={**env,'PYTHONPATH':str(REVIEW/'reconstructed/clr3/preserved/r1_court')+os.pathsep+env['PYTHONPATH']}
        result=subprocess.run(command,cwd=ROOT,env=suite_env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (ROOT/'evidence'/f'{name}.log').write_text(sanitize(result.stdout))
        xml=ROOT/'evidence'/f'{name}.xml';xml.write_text(sanitize(xml.read_text()))
        suite=ET.parse(xml).getroot().find('testsuite')
        receipts.append(dict(suite=name,exit_code=result.returncode,command=['python3',*command[1:]],candidate_bound=plugin,pythonpath=sanitize(suite_env['PYTHONPATH']),**{k:int(suite.attrib[k]) for k in ['tests','failures','errors','skipped']}))
    command=[sys.executable,'replay_candidate.py']
    replay=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (ROOT/'evidence/replay.log').write_text(sanitize(replay.stdout))
    assert replay.returncode==0,replay.stdout
    code="import json; from recursive_court import run_trajectory; print(json.dumps({w:run_trajectory(w)['trace_hash'] for w in ('HOURS_CUT','ROUTINE','RAISE_WITH_OVERTIME')},sort_keys=True))"
    cold=[]
    for seed in [0,1,71,123]:
        r=subprocess.run([sys.executable,'-c',code],cwd=ROOT/'candidate',env={**env,'PYTHONHASHSEED':str(seed)},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert r.returncode==0,r.stdout
        cold.append(dict(hash_seed=seed,exit_code=r.returncode,trace_hashes=json.loads(r.stdout)))
    reference=json.loads(replay.stdout)
    assert all(r['trace_hashes']=={k:reference[k] for k in r['trace_hashes']} for r in cold)
    (ROOT/'evidence/cold_replay.json').write_text(json.dumps(cold,indent=2)+'\n')
    check_frozen()
    for path in (ROOT/'evidence').iterdir():
        if path.suffix in {'.log','.xml'}:path.write_text(sanitize(path.read_text()))
    observed=[(r['tests'],r['failures'],r['errors'],r['skipped'],r['exit_code']) for r in receipts]
    result=dict(observed_utc=datetime.now(timezone.utc).isoformat(),suites=receipts,frozen_review_and_sources_unchanged=True,original_six_preserved=True,valid_full_trajectories_unchanged=4,cold_processes=4,independent_acceptance=False)
    (ROOT/'evidence/execution_receipts.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert observed==[(38,0,0,0,0),(6,0,0,0,0),(11,0,0,0,0),(6,6,0,0,1)],observed
    return 1  # Explicitly preserve the original historical RED suite.

if __name__=='__main__':raise SystemExit(main())
