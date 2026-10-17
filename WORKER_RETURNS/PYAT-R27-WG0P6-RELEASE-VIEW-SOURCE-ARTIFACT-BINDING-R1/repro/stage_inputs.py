"""Stage exact sourcefree WG0M/P5 closure from Git; never executes source."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ROOT=R.parents[1]
M='b91642ce98ec2c74b6d0c5d06ec8b83f67f02e86'
MP='WORKER_RETURNS/PYAT-R26-WG0M-ORIGINAL-FRONTIER-INDEPENDENT-DELTA-R1/'
COURT=R/'court'
if (R/'CANDIDATE_CODE_PIN.json').exists():
 raise SystemExit('REFUSE_RESTAGING_OVER_P6: use committed source and verify custody; this constructor stages the historical P5 baseline only')
rows={}
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),'-c','gc.auto=0',*a])
def stage(commit,source,dest,expected=None):
 b=git('show',commit+':'+source)
 sha=hashlib.sha256(b).hexdigest()
 if expected is not None:assert sha==expected,(source,sha,expected)
 path=COURT/dest;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
 rows[dest]=dict(commit=commit,source_path=source,staged_path='court/'+dest,
                 sha256=sha,git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),bytes=len(b))
paths=git('ls-tree','-r','--name-only',M,'--',MP).decode().splitlines()
for p in paths:
 rel=p.removeprefix(MP)
 if rel.startswith(('repro/','tests/','bootstrap_p5/')) or '/' not in rel or rel in ['observations/WG0P5_candidate_read_cut.json','observations/inheritance_source_selector.json','observations/DESCRIPTOR_PREREGISTRATION_ROOT.json','observations/PRECOMMITTED_TEST_ROOT.json']:
  stage(M,p,rel)
for sel in ['observations/inheritance_source_selector.json','observations/WG0P5_candidate_read_cut.json']:
 obj=json.loads((COURT/sel).read_text())
 for row in obj['files']:
  stage(row['commit'],row['source_path'],row['staged_path'],row['sha256'])
# Original M publication selectors are documentary pins, never silently rewritten.
(R/'SOURCE_INPUTS.json').write_text(json.dumps(dict(scope='SOURCEFREE_ONLY; unchanged original oracles/owners/tests; candidate module is the sole productive patch',files=list(rows.values())),indent=2)+'\n')
for rel in ['observations','runtime/raw_logs','tests']:(R/rel).mkdir(parents=True,exist_ok=True)
(COURT/'runtime_phase_b/p5_return/review/runtime_phase_b/candidate/observations').mkdir(parents=True,exist_ok=True)
print('exact staged inputs',len(rows))
