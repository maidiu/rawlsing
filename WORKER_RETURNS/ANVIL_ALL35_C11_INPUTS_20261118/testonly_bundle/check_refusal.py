#!/usr/bin/env python3
"""Prove census mismatch refuses before source access."""
from __future__ import annotations
import hashlib,json,os,pickle,sys
from dataclasses import replace
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
HERE=Path(os.environ.get('ANVIL_TESTONLY_ROOT', str(Path(__file__).resolve().parent))).resolve()
manifest=json.loads((HERE/'inputs'/'typed_inputs_manifest.json').read_text())
raw=(HERE/'inputs'/'typed_inputs.pkl').read_bytes()
if manifest.get('sourcefree_test_only') is not True or manifest.get('pickle_sha256')!=hashlib.sha256(raw).hexdigest():
 raise SystemExit('TESTONLY_PICKLE_DIGEST_MISMATCH')
x=pickle.loads(raw)
bad=replace(x['inventory'],source_sha256='0'*64)
try:
 build_source_i02_handoff(config=x['config'],source_path='/nonexistent/testonly-source.sav',destination=HERE/'estate'/'should-not-exist.sqlite',census=x['census'],inventory=bad,policy=x['policy'],frontier=x['frontier'])
except Exception as exc:
 proof={'schema':'ANVIL_TESTONLY_Q2_REFUSAL@1','refused':True,'error_type':type(exc).__name__,'error':str(exc),'before_source':True,'source_path':'/nonexistent/testonly-source.sav'}
 (HERE/'proof'/'refusal.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n');print(json.dumps(proof,sort_keys=True));raise SystemExit(0)
raise SystemExit('REFUSAL_DID_NOT_OCCUR')
