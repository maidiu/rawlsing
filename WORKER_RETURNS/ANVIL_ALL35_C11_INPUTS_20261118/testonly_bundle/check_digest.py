#!/usr/bin/env python3
"""Prove the local TEST_ONLY pickle digest is checked before deserialization."""
from __future__ import annotations
import json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(os.environ.get('ANVIL_TESTONLY_ROOT',str(Path(__file__).resolve().parent))).resolve()
tmp=HERE/'digest_tamper';shutil.rmtree(tmp,ignore_errors=True)
shutil.copytree(HERE/'inputs',tmp/'inputs')
p=tmp/'inputs'/'typed_inputs.pkl';p.write_bytes(p.read_bytes()+b'\x00tamper')
env={**os.environ,'ANVIL_TESTONLY_ROOT':str(tmp),'PYTHONPATH':str(Path(__file__).resolve().parents[3]),'PYTHONDONTWRITEBYTECODE':'1'}
run=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve().parent/'build_bundle.py')],cwd=str(tmp),text=True,capture_output=True,env=env)
# The manifest itself is forged here only to reach the emitted-digest check.
if run.returncode==0 or 'TESTONLY_PICKLE_DIGEST_MISMATCH' not in (run.stdout+run.stderr):
    raise SystemExit(f'DIGEST_REFUSAL_DID_NOT_OCCUR\n{run.stdout}\n{run.stderr}')
proof={'schema':'ANVIL_TESTONLY_Q2_PICKLE_REFUSAL@1','sourcefree_test_only':True,'refused':True,'error':'TESTONLY_PICKLE_DIGEST_MISMATCH','before_deserialization':True}
(HERE/'proof'/'digest_refusal.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
print(json.dumps(proof,sort_keys=True))
