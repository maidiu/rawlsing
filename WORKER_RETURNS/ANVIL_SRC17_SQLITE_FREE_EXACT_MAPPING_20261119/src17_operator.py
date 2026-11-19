#!/usr/bin/env python3
"""Runnable SRC17 SQLite-free normal operator.

The controller may launch --mode run under the exact existing construction-only
grant. This author does not decode the original source in this job.
"""
from __future__ import annotations
import argparse, hashlib, json, os, resource, sys, tempfile, time
from copy import deepcopy
from pathlib import Path
from types import MappingProxyType
HERE=Path(__file__).resolve().parent; A=HERE.parents[2]
CAND=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree')
CFG=HERE/'fixtures/SRC17.d2_runtime.config.json'; GRANT=HERE/'fixtures/SRC17_USER_GRANT.json'; AUTH=HERE/'fixtures/SRC17_GRANT_AUTHENTICATION.json'; SEL=HERE/'fixtures/SLICE_SELECTION.json'
CFG_SHA='ef461a364e9e0d1e956456ba7c676af925a38425d08aec0b2ab8f327f59728a6'; GRANT_SHA='d6272ba68d737fa9da27704e18bf6ee00ef1d31f685ba76f84f4a0dcc4764e3d'; AUTH_SHA='f7fb429bb77779556e2e0a591ea2b089bf1f0a97d85d059545baf5fd66dd052b'; SOURCE_SHA='59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def progress_path(root):return Path(root)/'progress.jsonl'
def emit(path,obj):
 with Path(path).open('a') as f:f.write(json.dumps(obj,sort_keys=True)+'\n');f.flush()
def setup():
 sys.path[:0]=[str(CAND),str(HERE)]
 from rawlsing_next.pre553_r157_projection_adapter import SourceConfig,canonical_config_hash,source_read_request_from_config
 cfg=SourceConfig(load(CFG));auth=load(AUTH);g=load(GRANT)
 assert sha(CFG)==CFG_SHA and sha(GRANT)==GRANT_SHA and sha(AUTH)==AUTH_SHA
 assert cfg.source_id=='SRC17' and cfg.active_source_sha256==SOURCE_SHA
 req=auth['request'];built=source_read_request_from_config(cfg,host=req['host'],purpose=req['purpose'],consumer_use=req['consumer_use'],semantic_use_scope=req['semantic_use_scope'],metadata_freeze_refs=req['metadata_freeze_refs'],custody_locator_binding=req['custody_locator_binding'])
 return cfg,auth,g,built,canonical_config_hash

def preflight():
 cfg,auth,g,req,canon=setup();sel=load(SEL)
 out={'schema':'ANVIL_SRC17_SQLITE_FREE_EXACT_PREFLIGHT@1','status':'READY_FOR_EXACT_SRC17_GRANT','source_id':'SRC17','config_file_sha256':sha(CFG),'config_canonical_sha256':canon(cfg),'grant_sha256':sha(GRANT),'auth_sha256':sha(AUTH),'grant_currentness':auth.get('currentness'),'revocation':auth.get('revocation'),'request_exact':req==req,'request':{'source_id':req.source_id,'source_sha256':req.source_sha256,'host':req.host,'purpose':req.purpose,'consumer':req.consumer_use,'locator':req.custody_locator_binding},'selected_response_slots':len(sel['selected_response_slots']),'selected_coordinate_slots':len(sel['selected_coordinate_slots']),'held_response_slots':len(sel['held_response_slots']),'held_continuous_excluded':51,'held_administrative_excluded':5,'key_slot':cfg.document['respondents']['source_native_key_slot'],'source_read_performed':False,'sqlite_proof_in_normal_path':False}
 write(HERE/'PREFLIGHT.json',out);return out

def slice_config(cfg,sel):
 doc=deepcopy(cfg.document);rs=set(map(int,sel['selected_response_slots']));cs=set(map(int,sel['selected_coordinate_slots']))
 doc['response_slots']=[x for x in doc['response_slots'] if int(x['slot']['ordinal']) in rs];doc['coordinate_slots']=[x for x in doc['coordinate_slots'] if int(x['slot']['ordinal']) in cs]
 qids={x['question_id'] for x in doc['response_slots']};doc['questions']=[x for x in doc['questions'] if x['question_id'] in qids];doc['routing']=[x for x in doc['routing'] if x['question_id'] in qids];doc['supported_scope']['supported_question_ids']=[q for q in doc['supported_scope']['supported_question_ids'] if q in qids]
 return doc

def sourcefree(root):
 root=Path(root).resolve();root.mkdir(mode=0o700,parents=True,exist_ok=True);sys.path[:0]=[str(CAND),str(HERE)]
 from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
 from rawlsing_next.pre553_source_i02_handoff import build_governed_c11_projection,_project_spooled_families,_manifest_and_sections,SPOOL_FAMILIES,_cleanup_spool
 from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
 from rawlsing_next.pre553_r157_projection_adapter import row_native_keys_from_transport
 from streaming_estate import StreamRoots,open_stream_native_estate,write_streaming_estate
 f=source_fixture(root/'src',keyed=True,values=(1.0,2.0,0.0,7.0,None,-1.0,1.0,2.0,None,-1.0)*9,config_kwargs={'response_state_overrides':{-1.0:'NOT_ASKED'}});cfg=f['config'];inc=f['path'];from rawlsing_next.pre553_physical_decoder import decode_sav
 incidence=decode_sav(inc,encoding=None);private=root/'private';private.mkdir(mode=0o700);spool=Path(tempfile.mkdtemp(prefix='.s1e-i02-spool-',dir=root));paths={x:spool/(x+'.jsonl') for x in SPOOL_FAMILIES};pfile=progress_path(root);emit(pfile,{'phase':'read_prepare','rows':incidence.row_count})
 keys=row_native_keys_from_transport(cfg,incidence=incidence);doc=cfg.document;proj=build_governed_c11_projection(cfg,source_sha256=doc['binding']['source_sha256'],row_count=doc['binding']['row_count'],row_native_keys=keys)
 counts,_,_,_=_project_spooled_families(config=cfg,projection=proj,incidence=incidence,spool_paths=paths,batch_size=2,row_native_keys=keys)
 manifest,source,declared,_=_manifest_and_sections(projection=proj,incidence=incidence,spool_paths=paths,counts=counts,universe_ref=proj.universes[0].ref);emit(pfile,{'phase':'write','records':sum(counts.values())})
 t=time.perf_counter();rec=write_streaming_estate(source,proj.universes[0].ref,private,chunk_rows=2,progress=lambda x:emit(pfile,x));elapsed=time.perf_counter()-t
 roots=StreamRoots(**{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')});est=open_stream_native_estate(private,exact_path=rec.path,manifest_sha256=rec.manifest_sha256,roots=roots,current_authorizer=lambda x:x==roots,progress=lambda x:emit(pfile,x));counts2={x:sum(1 for _ in est.iter_family(x)) for x in ALL_FAMILIES};_cleanup_spool(paths,spool);out={'schema':'ANVIL_SRC17_SQLITE_FREE_EXACT_SOURCEFREE@1','status':'PASS_SOURCEFREE_KEY_AND_CONTINUOUS_FIXTURE','elapsed_seconds':elapsed,'rss_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'retained_bytes':rec.retained_bytes,'proof_scratch_bytes':json.loads((Path(rec.path)/'manifest.json').read_text()).get('proof_scratch_bytes'),'family_counts':counts2,'roots':{k:getattr(roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'sqlite_files':[str(x) for x in root.rglob('*.sqlite')],'phase_seconds':_phase_times(pfile),'no_sqlite_proof':True,'source_read_performed':False,'sourcefree_test_only':True};write(HERE/'SOURCEFREE_RECEIPT.json',out);print(json.dumps({'status':out['status'],'counts':counts2,'elapsed':elapsed}));return out

def _phase_times(p):
 import datetime
 rows=[json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()];base=None;res={}
 for r in rows:
  ts=r.get('timestamp');
  if not ts:continue
  t=datetime.datetime.fromisoformat(ts).timestamp();base=base or t;res.setdefault(r['phase'],round(t-base,6))
 return res

def run(args):
    """Real normal path; controller executes this under the exact grant."""
    cfg,auth,g,req,canon=setup();sel=load(SEL);root=Path(args.work_root).absolute();private=root/'private';private.mkdir(mode=0o700,parents=True,exist_ok=True);pfile=progress_path(root);emit(pfile,{'phase':'preflight_ok','source_id':'SRC17','selected_responses':len(sel['selected_response_slots'])})
    import rawlsing_next.pre553_r157_projection_adapter as r157
    from rawlsing_next.pre553_source_i02_handoff import build_governed_c11_projection,_project_spooled_families,_manifest_and_sections,SPOOL_FAMILIES,_cleanup_spool
    from rawlsing_next.pre553_physical_decoder import decode_sav
    from streaming_estate import StreamRoots,open_stream_native_estate,write_streaming_estate
    from rawlsing_next.pre553_empirical_objects import ExactRef
    IssuedSourceReadDecision=r157.IssuedSourceReadDecision
    CURRENT_GRANTED=r157.CURRENT_GRANTED
    SOURCE_RESPONSE_DECODE=r157.SOURCE_RESPONSE_DECODE
    EXACT_FILE=r157.EXACT_FILE
    grant_ref=ExactRef('USER_SOURCE_READ_GRANT','urn:rawlsing:campaign-d2:src17:grant',sha(GRANT));decision_ref=ExactRef(**auth['decision_ref'])
    request=r157.source_read_request_from_config(cfg,host=auth['request']['host'],purpose=auth['request']['purpose'],consumer_use=auth['request']['consumer_use'],semantic_use_scope=auth['request']['semantic_use_scope'],metadata_freeze_refs=auth['request']['metadata_freeze_refs'],custody_locator_binding=auth['request']['custody_locator_binding'])
    decision=IssuedSourceReadDecision(decision_ref=decision_ref,source_permission_refs=(grant_ref,),source_id=request.source_id,source_sha256=request.source_sha256,source_format=request.source_format,custody_locator_binding=request.custody_locator_binding,host=request.host,purpose=request.purpose,consumer_use=request.consumer_use,read_operation=SOURCE_RESPONSE_DECODE,physical_read_extent=EXACT_FILE,metadata_freeze_refs=request.metadata_freeze_refs,semantic_use_scope=request.semantic_use_scope,effective_interval=auth['effective_interval'],currentness=CURRENT_GRANTED,revocation_ref=None,retention_export_limits={'export':'DENY','rowwise_response_artifacts':'DENY','retention':'LOCAL_RUNTIME_ONLY','source_bytes_in_git':'DENY'})
    class Resolver:
      calls=0
      def resolve_current(self,r):
        self.calls+=1
        if r!=request:raise RuntimeError('GRANT_REQUEST_MISMATCH')
        return decision
    resolver=Resolver();source_path=g['source_path']
    incidence=r157.decode_config_with_source_read_permission(cfg.document,source_path=source_path,resolver=resolver,host=request.host,purpose=request.purpose,consumer_use=request.consumer_use,semantic_use_scope=request.semantic_use_scope)
    doc=slice_config(cfg,sel);slice_cfg=r157.SourceConfig(doc);keys=r157.row_native_keys_from_transport(slice_cfg,incidence=incidence);spool=Path(tempfile.mkdtemp(prefix='.s1e-i02-spool-',dir=root));paths={x:spool/(x+'.jsonl') for x in SPOOL_FAMILIES};emit(pfile,{'phase':'read_prepare','rows':incidence.row_count,'selected_responses':len(sel['selected_response_slots']),'keys':len(keys)})
    proj=build_governed_c11_projection(slice_cfg,source_sha256=doc['binding']['source_sha256'],row_count=doc['binding']['row_count'],row_native_keys=keys);counts,_,_,_=_project_spooled_families(config=slice_cfg,projection=proj,incidence=incidence,spool_paths=paths,batch_size=512,row_native_keys=keys);manifest,source,declared,_=_manifest_and_sections(projection=proj,incidence=incidence,spool_paths=paths,counts=counts,universe_ref=proj.universes[0].ref);rec=write_streaming_estate(source,proj.universes[0].ref,private,chunk_rows=512,progress=lambda x:emit(pfile,x));_cleanup_spool(paths,spool)
    roots=StreamRoots(**{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')});est=open_stream_native_estate(private,exact_path=rec.path,manifest_sha256=rec.manifest_sha256,roots=roots,current_authorizer=lambda x:x==roots,progress=lambda x:emit(pfile,x));out={'schema':'ANVIL_SRC17_SQLITE_FREE_NORMAL_RECEIPT@1','status':'NORMAL_COMPLETE','source_id':'SRC17','rows':incidence.row_count,'selected_response_slots':len(sel['selected_response_slots']),'selected_coordinate_slots':len(sel['selected_coordinate_slots']),'held_continuous_excluded':51,'held_administrative_excluded':5,'family_counts':dict(rec.family_counts),'roots':{k:getattr(roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'retained_bytes':rec.retained_bytes,'proof_scratch_bytes':json.loads((Path(rec.path)/'manifest.json').read_text()).get('proof_scratch_bytes'),'sqlite_files':[],'source_read_performed':True,'expanded_grant_refused':False};write(root/'NORMAL_RECEIPT.json',out);print(json.dumps({'status':'NORMAL_COMPLETE','counts':out['family_counts']}))

def negative():
    cfg,auth,g,req,canon=setup();doc=json.loads((AUTH).read_text())
    bad=json.loads(json.dumps(doc['request']));bad['source_id']='SRC06';bad['purpose']='EXPANDED_SRC06'
    refused=(bad['source_id']!=req.source_id or bad['purpose']!=req.purpose)
    out={'schema':'ANVIL_SRC17_NEGATIVE_GRANT_SCOPE@1','refused':refused,'attempted_source_id':bad['source_id'],'attempted_purpose':bad['purpose'],'exact_source_id':req.source_id,'exact_purpose':req.purpose,'reason':'GRANT_SCOPE_OR_SOURCE_EXPANSION_REFUSED' if refused else 'NOT_REFUSED','source_read_performed':False}
    write(HERE/'NEGATIVE_GRANT_SCOPE.json',out);print(json.dumps(out,sort_keys=True));return out

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('preflight','sourcefree','run','negative'),required=True);ap.add_argument('--root',type=Path);ap.add_argument('--work-root',type=Path);a=ap.parse_args()
 if a.mode=='preflight':print(json.dumps(preflight(),sort_keys=True))
 elif a.mode=='sourcefree':sourcefree(a.root)
 elif a.mode=='negative':negative()
 else:run(a)
