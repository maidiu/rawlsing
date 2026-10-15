"""Rehydrate exact sourcefree Git objects and rerun without overwriting receipts.

Run from this repository with the pinned source commits present in its object
store. Expected review REDs remain nonzero exits, never xfails or acceptance.
"""
from pathlib import Path
import sys,subprocess,re
RET=Path(__file__).resolve().parent
if len(sys.argv)!=2 or not re.fullmatch('[A-Za-z0-9_-]+',sys.argv[1]):raise SystemExit('Usage: python3 reproduce.py fresh_id')
tag=sys.argv[1]
subprocess.run([sys.executable,str(RET/'repro/stage.py')],check=True)
expected={'owners':0,'rsm':0,'candidate':0,'candidate_unset':0,'reviewer':1}
for suite,wanted in expected.items():
 name=suite+'__'+tag
 with (RET/'repro'/(name+'.log')).open('x') as f:
  result=subprocess.run([sys.executable,str(RET/'repro/run_suite.py'),name],stdout=f,stderr=subprocess.STDOUT)
 print(name,'exit',result.returncode,'expected',wanted,flush=True)
 if result.returncode!=wanted:raise SystemExit('Unexpected execution disposition: '+name)
print('Use JUnit to verify exact counts:220,60,37,36+1skip; reviewer37PASS45RED. Legacy greens do not change REVIEW_REVISE.')
