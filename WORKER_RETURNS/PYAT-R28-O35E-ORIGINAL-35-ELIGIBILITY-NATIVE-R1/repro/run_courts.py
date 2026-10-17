"""Reproducible cold subprocess evidence; no new dependencies or source reads."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parents[1];REPO=HERE.parents[1];OBS=HERE/'observations'
WORKER=HERE/'repro/run_pytest.py'
def main():
 OBS.mkdir(exist_ok=True)
 own=[str(HERE/'tests/test_o35e_native.py'),str(HERE/'tests/test_o35e_metadata.py')]
 native=[str(HERE/'runtime/pinned/rawlsing_next/tests'/f) for f in ('test_pre553_route_b_production.py','test_pre553_batch_runner.py')]
 groups=[('o35e_final',own),('o35e_cold',own),('native_c11_route_batch',native),
  ('native_d07_missing_fixture',[str(HERE/'runtime/pinned/rawlsing_next/tests/test_objective_consumer_bounded_evidence_d07.py')])]
 receipts=[]
 for label,tests in groups:
  args=[sys.executable,str(WORKER),label,*tests]
  result=subprocess.run(args,cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
  # Preserve raw local output privately, publish only path-normalized output.
  raw=HERE/'runtime/rawlogs';raw.mkdir(exist_ok=True)
  (raw/f'{label}.stdout').write_bytes(result.stdout)
  normalized=result.stdout.decode(errors='replace').replace(str(HERE),'$RETURN').replace(str(REPO),'$WORKTREE')
  (OBS/f'{label}.stdout').write_text(normalized)
  receipts.append({'label':label,'command':['python3','$RETURN/repro/run_pytest.py',label,*[t.replace(str(HERE),'$RETURN') for t in tests]],
   'exit_code':result.returncode,'stdout':f'observations/{label}.stdout','junit':f'observations/{label}.xml',
   'stdout_raw_sha256':hashlib.sha256(result.stdout).hexdigest(),'published_paths_normalized':True})
  print(label,result.returncode,normalized.strip().splitlines()[-1])
 (OBS/'process_receipts.json').write_text(json.dumps({'at_utc':datetime.now(timezone.utc).isoformat(),'runs':receipts},indent=2)+'\n')
 assert all(r['exit_code']==0 for r in receipts[:3])
 assert receipts[3]['exit_code']==2,'D07 fixture absence characterization changed; investigate, do not silently reclassify'

if __name__=='__main__':main()
