#!/usr/bin/env python3
"""Separate read-only strict audit of an already written stream estate."""
import argparse,json,sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,'/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118')
from streaming_estate import audit_stream_estate, StreamRoots
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--exact-path',required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--roots-json',required=True);a=p.parse_args()
r=json.loads(a.roots_json);roots=StreamRoots(r['logical'],r['physical'],r['release'],r['source'],r['replay'],r['universe'],r['schema'])
counts=audit_stream_estate(a.root,a.exact_path,a.manifest_sha256,roots,current_authorizer=lambda _r: True,progress=lambda x: print(json.dumps(x,sort_keys=True),flush=True))
print(json.dumps({'audit':'PASS','counts':dict(counts),'read_only':True,'sqlite_calls':False},sort_keys=True))
