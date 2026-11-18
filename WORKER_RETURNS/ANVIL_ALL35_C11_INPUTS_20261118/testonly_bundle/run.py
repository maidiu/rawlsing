#!/usr/bin/env python3
"""Run one existing small sourcefree bundle through emit/build/reopen/refusal children."""
from __future__ import annotations
import json,subprocess,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
shutil.rmtree(HERE/'estate',ignore_errors=True)
(HERE/'proof').mkdir(exist_ok=True)
def run(name):
 p=subprocess.run([sys.executable,'-B',str(HERE/name)],cwd=str(HERE),text=True,capture_output=True,env={**__import__('os').environ,'PYTHONPATH':str(HERE.parents[2]),'PYTHONDONTWRITEBYTECODE':'1'})
 if p.returncode: raise SystemExit(f'{name} FAILED\n{p.stdout}\n{p.stderr}')
 print(p.stdout.strip())
run('make_bundle.py');run('build_bundle.py');run('reopen_bundle.py');run('check_refusal.py')
print('TESTONLY_BUNDLE_PASS')
