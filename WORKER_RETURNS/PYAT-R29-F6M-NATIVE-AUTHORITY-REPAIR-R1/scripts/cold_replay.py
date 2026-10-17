"""Replay a relocatable, Git-independent source-free packet in a path with spaces."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,os,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
 with tempfile.TemporaryDirectory(prefix='f6m-cold-') as tmp:
  dest=Path(tmp)/'return with spaces'
  shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('runtime','__pycache__','.environment-marker'))
  # No repository, shared-store lookup, symlink or current working directory dependency.
  assert not any(p.is_symlink() for p in dest.rglob('*'))
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
  commands=[[sys.executable,'-B',str(dest/'scripts/build_candidate.py')],
            [sys.executable,'-B',str(dest/'scripts/run_courts.py'),'compat']]
  runs=[]
  for argv in commands:
   p=subprocess.run(argv,cwd=tmp,env=env,capture_output=True,text=True)
   runs.append(dict(argv=[a.replace(str(dest),'$COLD_RETURN') for a in argv],exit=p.returncode,stdout=p.stdout.replace(str(dest),'$COLD_RETURN'),stderr=p.stderr.replace(str(dest),'$COLD_RETURN')))
   assert p.returncode==0,runs[-1]
  courts=json.loads((dest/'evidence/compat/courts.json').read_text())
  assert all(r['exit']==0 for r in courts),courts
  rational=json.loads((dest/'evidence/compat/native_vs_frozen.json').read_text())
  assert rational['comparisons_total']==rational['comparisons_passed']==82
  candidate=dest/'candidate/rawlsing_next/pre553_heterogeneous_synthesis.py'
  assert candidate.read_bytes()==(ROOT/'candidate/rawlsing_next/pre553_heterogeneous_synthesis.py').read_bytes()
  copy=ROOT/'evidence/cold';copy.mkdir(exist_ok=True)
  for p in (dest/'evidence/compat').glob('*'):
   if p.is_file():shutil.copyfile(p,copy/p.name)
  receipt=dict(schema='F6M_COLD_RELOCATION@1',repo_present=False,symlink_count=0,path_contains_spaces=True,temporary_stage_removed_on_exit=True,runs=runs,courts=courts,rational_comparisons=82,producer_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
  (ROOT/'evidence/cold_replay.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print('Cold relocation: all courts exit 0; rational 82/82; no Git repository or live symlinks')
if __name__=='__main__':main()
