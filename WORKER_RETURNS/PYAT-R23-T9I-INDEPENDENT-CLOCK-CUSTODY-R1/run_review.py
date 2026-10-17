"""Reproduce retained suites. Exit 1 means independent RED, never fake PASS."""
import json
import os
from pathlib import Path
import subprocess
import sys

RET=Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE']='1'
for name in ['evidence','logs','junit','scratch']:(RET/name).mkdir(exist_ok=True)
subprocess.run([sys.executable,'-B',str(RET/'audit_and_stage.py')],check=True)
results={}
for suite in ['author','legacy','independent']:
    p=subprocess.run([sys.executable,'-B',str(RET/'guarded_runner.py'),suite],capture_output=True,text=True)
    (RET/'logs'/f'{suite}.log').write_text(p.stdout+p.stderr)
    print(suite,p.returncode,p.stdout.splitlines()[-2:])
    results[suite]=p.returncode
(RET/'evidence/reproduction_exits.json').write_text(json.dumps(results,indent=2)+'\n')
if results['author']!=0 or results['legacy']!=0:sys.exit(2)
subprocess.run([sys.executable,'-B',str(RET/'assemble_receipts.py')],check=True)
sys.exit(results['independent'])
