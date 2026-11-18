#!/usr/bin/env python3
"""Run one existing small sourcefree bundle through emit/build/reopen/refusal children."""
from __future__ import annotations
import json,subprocess,sys,shutil,os,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
root=(Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp(prefix='anvil-all35-testonly-'))).resolve()
if root.exists() and any(root.iterdir()): raise SystemExit('FRESH_EMPTY_ROOT_REQUIRED')
root.mkdir(parents=True,exist_ok=True)
(root/'proof').mkdir(parents=True,exist_ok=True)
env={**os.environ,'ANVIL_TESTONLY_ROOT':str(root),'PYTHONPATH':str(HERE.parents[2]),'PYTHONDONTWRITEBYTECODE':'1'}
if root.resolve()==HERE.resolve(): raise SystemExit('FRESH_DISJOINT_ROOT_REQUIRED')
def run(name, extra_env=None):
 e=dict(env);e.update(extra_env or {})
 p=subprocess.run([sys.executable,'-B',str(HERE/name)],cwd=str(root),text=True,capture_output=True,env=e)
 if p.returncode: raise SystemExit(f'{name} FAILED\n{p.stdout}\n{p.stderr}')
 print(p.stdout.strip())
run('make_bundle.py');run('build_bundle.py');run('reopen_bundle.py');run('check_refusal.py');run('reopen_bundle.py',{'ANVIL_REOPEN_MODE':'revoked'});run('reopen_bundle.py',{'ANVIL_REOPEN_MODE':'wrong_root'});run('check_digest.py')
print(json.dumps({'TESTONLY_BUNDLE_PASS':True,'root':str(root)},sort_keys=True))
