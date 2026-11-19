#!/usr/bin/env python3
"""Sourcefree single-pass caller rehearsal; separate producer/reader processes."""
from __future__ import annotations
import json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAND=Path(os.environ['ANVIL_CANDIDATE_TREE']).resolve();sys.path.insert(0,str(CAND));sys.path.insert(0,str(HERE))
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from single_pass_handoff import build_single_pass

def producer(root):
 fixture=source_fixture(root/'src'); private=root/'private';private.mkdir(mode=0o700,parents=True)
 receipt=build_single_pass(config=fixture['config'],source_path=fixture['path'],private_root=private,chunk_rows=2,
  progress=lambda x: print(json.dumps(x),file=sys.stderr,flush=True))
 out={'producer_pid':os.getpid(),'path':receipt.path,'manifest_sha256':receipt.manifest_sha256,
      'i02':{k:getattr(receipt.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},
      'family_counts':dict(receipt.family_counts),'single_pass':True}
 (root/'build.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PRODUCER_COMMITTED'}))

def _estate(root,b,wrong=False):
 held=ExternalI02Roots(**b['i02'])
 if wrong:
  from dataclasses import replace
  held=replace(held,logical='0'*64)
 return VerifiedDirectEstate(root/'private',exact_path=b['path'],independently_held_manifest_sha256=b['manifest_sha256'],independently_held_i02=held,current_authorizer=lambda roots:roots==held)

def reader(root):
 b=json.loads((root/'build.json').read_text());alive=subprocess.run(['ps','-p',str(b['producer_pid']),'-o','pid='],capture_output=True,text=True).stdout.strip()
 if alive:raise SystemExit('PRODUCER_STILL_ALIVE')
 estate=_estate(root,b);counts={f:sum(1 for _ in estate.iter_family(f)) for f in ALL_FAMILIES}
 (root/'reader.json').write_text(json.dumps({'producer_exited_before_reader':True,'family_counts':counts},indent=2)+'\n');print(json.dumps({'status':'READER_OPENED','counts':counts}))

def wrong_root(root):
 b=json.loads((root/'build.json').read_text())
 try:_estate(root,b,True)
 except Exception as exc:
  (root/'wrong_root.json').write_text(json.dumps({'refused':True,'error_type':type(exc).__name__},indent=2)+'\n');print(json.dumps({'status':'REFUSED','type':type(exc).__name__}));return
 raise SystemExit('WRONG_ROOT_NOT_REFUSED')

if __name__=='__main__':
 mode,root=sys.argv[1],Path(sys.argv[2]);root.mkdir(mode=0o700,parents=True,exist_ok=True)
 {'producer':producer,'reader':reader,'wrong-root':wrong_root}[mode](root)
