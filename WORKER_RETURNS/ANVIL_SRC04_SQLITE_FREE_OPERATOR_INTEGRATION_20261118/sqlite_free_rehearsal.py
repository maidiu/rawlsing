#!/usr/bin/env python3
"""Sourcefree normal/resume path for the isolated SQLite-free operator."""
from __future__ import annotations
import json,os,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAND=Path(os.environ['ANVIL_CANDIDATE_TREE']).resolve();sys.path[:0]=[str(CAND),str(HERE)]
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from streaming_estate import StreamRoots,open_stream_native_estate
from sqlite_free_single_pass import build_single_pass,resume_single_pass,CheckpointStop
from rawlsing_next.pre553_empirical_objects import canonical_json
import hashlib

def fixture(root):
 p=root/'fixture_config.json';q=root/'source_path.txt'
 if p.is_file():
  from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
  return SourceConfig(json.loads(p.read_text())),Path(q.read_text().strip())
 vals=(1.0,2.0,0.0,7.0,None,-1.0,1.0,2.0,None,-1.0)*9
 f=source_fixture(root/'src',values=vals,config_kwargs={'response_state_overrides':{-1.0:'NOT_ASKED'}});p.write_text(json.dumps(f['document'],indent=2,sort_keys=True)+'\n');q.write_text(str(f['path'])+'\n');return f['config'],f['path']

def refs(cfg):
 sha=cfg.document['binding']['source_sha256'];req=types.SimpleNamespace(source_id=cfg.source_id,source_sha256=sha,source_format='SAV',custody_locator_binding='TEST_LOCAL',host='TEST_HOST',purpose='TEST_ONLY',consumer_use='TEST_ONLY',read_operation='SOURCE_RESPONSE_DECODE',physical_read_extent='EXACT_FILE',metadata_freeze_refs=(ExactRef('TEST_METADATA','test','a'*64),),semantic_use_scope=('TEST_ONLY',));return req,ExactRef('TEST_GRANT','grant','b'*64),ExactRef('TEST_DECISION','decision','c'*64)

def progress(root):
 path=root/'progress.jsonl'
 def emit(x):
  with path.open('a') as f:f.write(json.dumps(x,sort_keys=True)+'\n');f.flush()
 return emit

def normal(root):
 cfg,path=fixture(root);private=root/'normal-private';private.mkdir(mode=0o700,parents=True);r,g,d=refs(cfg);rec=build_single_pass(config=cfg,source_path=path,private_root=private,chunk_rows=2,compact_spool=True,progress=progress(root));out={'path':rec.path,'manifest_sha256':rec.manifest_sha256,'roots':{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(rec.family_counts),'proof_schema':rec.roots.schema,'decode_called':True};(root/'normal.json').write_text(json.dumps(out,indent=2)+'\n');print('NORMAL_OK')

def stop(root):
 cfg,path=fixture(root);private=root/'resume-private';private.mkdir(mode=0o700,parents=True);r,g,d=refs(cfg)
 try:build_single_pass(config=cfg,source_path=path,private_root=private,chunk_rows=2,compact_spool=True,request=r,grant_ref=g,decision_ref=d,stop_after_checkpoint=True,progress=progress(root))
 except CheckpointStop:pass
 (root/'stop.json').write_text(json.dumps({'checkpoint':str(private/'prepared-sections.checkpoint.json')},indent=2)+'\n');print('STOP_OK')

def resume(root):
 cfg,path=fixture(root);private=root/'resume-private';r,g,d=refs(cfg)
 import rawlsing_next.pre553_source_i02_handoff as h
 def trap(*a,**k):raise AssertionError('SOURCE_DECODE_TRAP_TRIGGERED')
 h.decode_sav=trap;h.decode_dta=trap
 rec=resume_single_pass(checkpoint=private/'prepared-sections.checkpoint.json',root=private,config=cfg,request=r,grant_ref=g,decision_ref=d,chunk_rows=2,progress=progress(root))
 out={'path':rec.path,'manifest_sha256':rec.manifest_sha256,'roots':{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(rec.family_counts),'proof_schema':rec.roots.schema,'decode_called':False};(root/'resumed.json').write_text(json.dumps(out,indent=2)+'\n');print('RESUMED_NO_DECODE')

def reader(root):
 outs=[]
 for name,private in [('normal.json','normal-private'),('resumed.json','resume-private')]:
  b=json.loads((root/name).read_text());roots=StreamRoots(**b['roots']);est=open_stream_native_estate(root/private,exact_path=b['path'],manifest_sha256=b['manifest_sha256'],roots=roots,current_authorizer=lambda r,h=roots:r==h,progress=progress(root));counts={};digests={}
  for f in ALL_FAMILIES:
   vals=[o.as_dict() for o in est.iter_family(f)];counts[f]=len(vals);digests[f]=hashlib.sha256(canonical_json(vals).encode()).hexdigest()
  outs.append({'name':name,'counts':counts,'digests':digests,'roots_equal':est.i02==roots})
 (root/'readers.json').write_text(json.dumps(outs,indent=2)+'\n');print(json.dumps({'status':'READERS_OPENED','equal':outs[0]['digests']==outs[1]['digests'] and outs[0]['counts']==outs[1]['counts']}))

if __name__=='__main__':
 mode,root=sys.argv[1],Path(sys.argv[2]);root.mkdir(mode=0o700,parents=True,exist_ok=True)
 {'normal':normal,'stop':stop,'resume':resume,'reader':reader}[mode](root)
