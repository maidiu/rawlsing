"""Read-only publication gate. No candidate code imported; no polling loop."""
import datetime,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
BRANCH='agent/rabochii-pyat-r26-wg0p5-bound-descriptor-provenance-repair-r1'
START='7e589c19c693c150d0cf622fc43e84bbc40d1b31'
RETURN='WORKER_RETURNS/PYAT-R26-WG0P5-DESCRIPTOR-PROVENANCE-REPAIR-R1/'
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=R).decode().strip()
remote=git('ls-remote','origin','refs/heads/'+BRANCH);sha=remote.split()[0]
git('fetch','--no-tags','origin',BRANCH)
# ls-tree pathspec magic is not portable across Git versions: use root cwd.
files=subprocess.check_output(['git','-c','gc.auto=0','ls-tree','-r','--name-only',sha,RETURN],cwd=R.parents[1]).decode().splitlines()
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'branch':BRANCH,'direct_remote_sha':sha,'startup_sha':START,'return_path':RETURN,'returned_files':files,'WG0P5_code_imported':False,'status':'WAIT_FOR_GOVERNED_WG0P5_PUSH' if sha==START or not files else 'RETURN_PRESENT_REQUIRES_EXACT_READ_CUT_BEFORE_EXECUTION','reason':'Remote is the sealed commission startup and has no WG0P5 return files.' if sha==START else 'Inspect exact candidate return identity and return-only change scope before Phase B.'}
(R/'observations/WG0P5_publication_gate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
