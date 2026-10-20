"""Reproduce preserved REDs and scoped positives. Successful replay is not acceptance."""
from pathlib import Path
import os,subprocess,sys
R=Path(__file__).resolve().parent;ROOT=R/'runs/runtime';P='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
def script(name,*args):subprocess.run([sys.executable,'-B',str(R/name),*args],cwd=R,check=True)
def main():
 script('prepare_runtime.py')
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'runs/tmp'))
 for name,node,expected_exit in [('author_full',P+'/tests',0),('hostile','review/test_hostile.py',1),('record_custody','review/test_record_custody.py',1),('positive_edges','review/test_edges.py',0)]:
  cmd=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--basetemp',str(R/'runs/pytest'/name),'--junitxml',str(R/'evidence'/(name+'.xml')),node]
  p=subprocess.run(cmd,cwd=ROOT,env=dict(env,C9PI_IMPORT_RECEIPT=str(R/'evidence'/(name+'_imports.json'))),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  (R/'evidence'/(name+'.log')).write_text(p.stdout)
  if p.returncode!=expected_exit:raise RuntimeError((name,p.returncode,p.stdout[-1500:]))
  print(name,'exit',p.returncode,flush=True)
 script('run_faults.py');script('run_faults.py','--extra-consumer')
 script('run_shared_gate.py');script('probe_closure.py');script('cold_replay.py')
 script('summarize_evidence.py');script('sanitize_evidence.py')
 print('REPRODUCTION_COMPLETE__REVISE_NATIVE_HOLD. Hostile pytest remains RED; no candidate repair.')
if __name__=='__main__':main()
