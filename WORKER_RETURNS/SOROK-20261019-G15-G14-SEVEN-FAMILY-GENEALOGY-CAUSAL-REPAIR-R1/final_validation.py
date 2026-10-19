"""Final serial validation; do not audit a temporarily faulted source tree."""
import json,subprocess,sys
from pathlib import Path
from court_runner import ROOT,REPO,ENV,courts,run,dump
from run_witnesses import main as witnesses
from audit_return import main as audit

def main():
 courts('candidate')
 witnesses()
 result=run('prospective','g15_causal',ROOT,['test_g15_causal.py'])
 dump(ROOT/'execution/prospective/results.json',[result]);assert result['exit']==0
 dump(ROOT/'execution/validation_commands.json',dict(candidate_courts='court_runner.py candidate',faults='run_witnesses.py',prospective=result['command']))
 for label,args in [('joined_positive',['--output',str(ROOT/'execution/joined_positive.json')]),('joined_cold_replay',['--replay',str(ROOT/'execution/joined_positive.json'),'--output',str(ROOT/'execution/joined_cold_replay.json')])]:
  cmd=[sys.executable,'-B',str(ROOT/'candidate/run_candidate.py'),*args]
  p=subprocess.run(cmd,cwd=REPO,env=ENV,capture_output=True,text=True)
  (ROOT/'execution'/(label+'.txt')).write_text((p.stdout+p.stderr).replace(str(REPO),'$WORKTREE'));assert p.returncode==0,p.stdout+p.stderr
 audit()
 print('FINAL SERIAL VALIDATION COMPLETE',flush=True)
if __name__=='__main__':main()
