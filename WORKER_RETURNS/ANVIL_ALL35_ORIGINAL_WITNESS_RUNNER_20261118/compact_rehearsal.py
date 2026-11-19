#!/usr/bin/env python3
"""Sourcefree compact-vs-baseline spool rehearsal with checkpoint resume."""
from __future__ import annotations
import json,os,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAND=Path(os.environ['ANVIL_CANDIDATE_TREE']).resolve();sys.path.insert(0,str(CAND));sys.path.insert(0,str(HERE))
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from single_pass_handoff import build_single_pass,resume_single_pass,CheckpointStop

def fixture(root):
 p=root/'fixture_config.json';q=root/'source_path.txt'
 if p.is_file() and q.is_file():
  from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
  return SourceConfig(json.loads(p.read_text())),Path(q.read_text().strip())
 # repeated zero, missing, DK and substantive values to exercise typed distinctions
 values=(1.0,2.0,0.0,7.0,None,-1.0,1.0,2.0,None,-1.0)*9
 f=source_fixture(root/'src',values=values,config_kwargs={'response_state_overrides':{-1.0:'NOT_ASKED'}});p.write_text(json.dumps(f['document'],indent=2,sort_keys=True)+'\n');q.write_text(str(f['path'])+'\n');return f['config'],f['path']

def req(cfg):
 sha=cfg.document['binding']['source_sha256'];return types.SimpleNamespace(source_id=cfg.source_id,source_sha256=sha,source_format='SAV',custody_locator_binding='TEST_LOCAL',host='TEST_HOST',purpose='TEST_ONLY',consumer_use='TEST_ONLY',read_operation='SOURCE_RESPONSE_DECODE',physical_read_extent='EXACT_FILE',metadata_freeze_refs=(ExactRef('TEST_METADATA','test','a'*64),),semantic_use_scope=('TEST_ONLY',)),ExactRef('TEST_GRANT','grant','b'*64),ExactRef('TEST_DECISION','decision','c'*64)

def stop(root,compact):
 cfg,path=fixture(root);private=root/('compact-private' if compact else 'baseline-private');private.mkdir(mode=0o700,parents=True,exist_ok=True);r,g,d=req(cfg)
 try:build_single_pass(config=cfg,source_path=path,private_root=private,chunk_rows=2,compact_spool=compact,request=r,grant_ref=g,decision_ref=d,stop_after_checkpoint=True)
 except CheckpointStop:pass
 spool=private/'.s1e-i02-spool-'+next(p.name for p in []) if False else None
 dirs=list(private.glob('.s1e-i02-spool-*'));files=list(dirs[0].glob('*')) if dirs else [];cp=private/'prepared-sections.checkpoint.json'
 out={'compact':compact,'checkpoint':str(cp),'checkpoint_bytes':cp.stat().st_size if cp.is_file() else 0,'spool_bytes':sum(x.stat().st_size for x in files),'spool_files':len(files)}
 (root/('compact-stop.json' if compact else 'baseline-stop.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

def resume(root,compact):
 cfg,path=fixture(root);private=root/('compact-private' if compact else 'baseline-private');r,g,d=req(cfg);cp=private/'prepared-sections.checkpoint.json'
 import rawlsing_next.pre553_source_i02_handoff as handoff
 def trap(*a,**k):raise AssertionError('SOURCE_DECODE_TRAP_TRIGGERED')
 handoff.decode_sav=trap;handoff.decode_dta=trap
 rec=resume_single_pass(checkpoint=cp,root=private,config=cfg,request=r,grant_ref=g,decision_ref=d,chunk_rows=2)
 out={'compact':compact,'path':rec.path,'manifest_sha256':rec.manifest_sha256,'i02':{k:getattr(rec.i02,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(rec.family_counts),'decode_called':False}
 (root/('compact-resume.json' if compact else 'baseline-resume.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'RESUMED','compact':compact,'decode_called':False}))

def reader(root):
 for name in ('baseline-resume.json','compact-resume.json'):
  b=json.loads((root/name).read_text());private=root/('baseline-private' if name.startswith('baseline') else 'compact-private');held=ExternalI02Roots(**b['i02'])
  e=VerifiedDirectEstate(private,exact_path=b['path'],independently_held_manifest_sha256=b['manifest_sha256'],independently_held_i02=held,current_authorizer=lambda roots,h=held:roots==h)
  from rawlsing_next.pre553_empirical_objects import canonical_json
  import hashlib
  counts={};digests={}
  for f in ALL_FAMILIES:
   vals=[o.as_dict() for o in e.iter_family(f)];counts[f]=len(vals);digests[f]=hashlib.sha256(canonical_json(vals).encode()).hexdigest()
  (root/(name.replace('.json','-reader.json'))).write_text(json.dumps({'counts':counts,'payload_digests':digests,'roots_equal':e.i02==held},indent=2)+'\n')
 print(json.dumps({'status':'READERS_OPENED'}))

if __name__=='__main__':
 mode,root=sys.argv[1],Path(sys.argv[2]);root.mkdir(mode=0o700,parents=True,exist_ok=True)
 if mode=='baseline-stop':stop(root,False)
 elif mode=='compact-stop':stop(root,True)
 elif mode=='baseline-resume':resume(root,False)
 elif mode=='compact-resume':resume(root,True)
 elif mode=='reader':reader(root)
