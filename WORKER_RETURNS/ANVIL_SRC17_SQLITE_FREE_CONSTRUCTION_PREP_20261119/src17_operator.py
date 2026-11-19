#!/usr/bin/env python3
"""Minimal SRC17 SQLite-free construction operator/preflight.

Preflight and sourcefree rehearsal only in this return.  Actual SRC17 execution
still requires the existing construction-only grant and the field-mapping gate.
"""
from __future__ import annotations
import argparse, hashlib, json, os, resource, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent; A=HERE.parents[2]
CANDIDATE=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree')
CONFIG=HERE/'fixtures/SRC17.source.config.json'; GRANT=HERE/'fixtures/SRC17_USER_GRANT.json'; AUTH=HERE/'fixtures/SRC17_GRANT_AUTHENTICATION.json'
CONFIG_SHA='ca791189e208c9b311a7261ac254ce5ffea35e9c13b4d6e2ec87e9e55a1ecca8'
GRANT_SHA='d6272ba68d737fa9da27704e18bf6ee00ef1d31f685ba76f84f4a0dcc4764e3d'
AUTH_SHA='f7fb429bb77779556e2e0a591ea2b089bf1f0a97d85d059545baf5fd66dd052b'
SOURCE_SHA='59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())

def preflight():
    assert sha(CONFIG)==CONFIG_SHA and sha(GRANT)==GRANT_SHA and sha(AUTH)==AUTH_SHA
    sys.path.insert(0,str(CANDIDATE))
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, canonical_config_hash, source_read_request_from_config
    doc=load(CONFIG); cfg=SourceConfig(doc); auth=load(AUTH); grant=load(GRANT)
    if canonical_config_hash(cfg)!='3f1eb83abe61415e01b2f67bcfe34ee6fe61d69d3aef7161be5e6e41e2a7be07':raise SystemExit('CONFIG_CANONICAL_MISMATCH')
    if cfg.source_id!='SRC17' or cfg.active_source_sha256!=SOURCE_SHA:raise SystemExit('CONFIG_SOURCE_MISMATCH')
    req=auth['request']; built=source_read_request_from_config(cfg,host=req['host'],purpose=req['purpose'],consumer_use=req['consumer_use'],semantic_use_scope=req['semantic_use_scope'],metadata_freeze_refs=req['metadata_freeze_refs'],custody_locator_binding=req['custody_locator_binding'])
    exact=built.source_id==req['source_id'] and built.source_sha256==req['source_sha256'] and built.host==req['host'] and built.purpose==req['purpose'] and built.consumer_use==req['consumer_use'] and list(built.semantic_use_scope)==sorted(req['semantic_use_scope']) and built.custody_locator_binding==req['custody_locator_binding']
    slot=doc.get('respondents',{}).get('source_native_key_slot')
    residual=[{'id':r['residual_id'],'status':r['status'],'field':r.get('field')} for r in doc.get('residuals',[]) if r.get('status') in ('DECODE_REQUIRED','NATIVE_FINITE_RULE_REQUIRED','RETAINED_ADMINISTRATIVE')]
    result={'schema':'ANVIL_SRC17_SQLITE_FREE_PREFLIGHT@1','source_id':'SRC17','config_file_sha256':sha(CONFIG),'config_canonical_sha256':canonical_config_hash(cfg),'grant_sha256':sha(GRANT),'authentication_sha256':sha(AUTH),'grant_currentness':auth.get('currentness'),'revocation':auth.get('revocation'),'request_exact':exact,'source_read_performed':False,'sqlite_proof_expected':False,'config_blockers':{'source_native_key_slot':slot,'required_residuals':residual,'continuous_held_items':51,'administrative_held_items':5},'launch_eligibility':'BLOCKED__EXACT_NATIVE_ROW_KEY_AND_CONTINUOUS_RULE_REQUIRED' if slot or residual else 'READY_METADATA_ONLY'}
    (HERE/'PREFLIGHT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return result

def sourcefree(root):
    root=Path(root).resolve();root.mkdir(mode=0o700,parents=True,exist_ok=True)
    sys.path[:0]=[str(CANDIDATE),str(HERE)]
    from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
    from sqlite_free_single_pass import build_single_pass
    from streaming_estate import StreamRoots,open_stream_native_estate
    from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
    from rawlsing_next.pre553_empirical_objects import canonical_json
    fixture=source_fixture(root/'src',values=(1.0,2.0,0.0,7.0,None,-1.0,1.0,2.0,None,-1.0)*9,config_kwargs={'response_state_overrides':{-1.0:'NOT_ASKED'}})
    private=root/'private';private.mkdir(mode=0o700,parents=True)
    progress=root/'progress.jsonl'; phases=[]
    def emit(x):
        with progress.open('a') as f:f.write(json.dumps(x,sort_keys=True)+'\n');f.flush()
        phases.append(x)
    t=time.perf_counter(); rec=build_single_pass(config=fixture['config'],source_path=fixture['path'],private_root=private,chunk_rows=2,compact_spool=True,progress=emit); elapsed=time.perf_counter()-t
    roots=StreamRoots(**{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')})
    def current(r):return r==roots
    estate=open_stream_native_estate(private,exact_path=rec.path,manifest_sha256=rec.manifest_sha256,roots=roots,current_authorizer=current,progress=emit)
    counts={f:sum(1 for _ in estate.iter_family(f)) for f in ALL_FAMILIES}
    out={'schema':'ANVIL_SRC17_SQLITE_FREE_SOURCEFREE@1','status':'PASS_SOURCEFREE_SQLITE_FREE','elapsed_seconds':elapsed,'rss_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'retained_bytes':rec.retained_bytes,'proof_scratch_bytes':json.loads((Path(rec.path)/'manifest.json').read_text()).get('proof_scratch_bytes'),'family_counts':counts,'roots':{k:getattr(roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'sqlite_files':[str(p) for p in root.rglob('*.sqlite')],'progress_phases':phases,'source_read_performed':False}
    (HERE/'SOURCEFREE_RECEIPT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'counts':counts,'elapsed':elapsed}));return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('preflight','sourcefree'),required=True);ap.add_argument('--root',type=Path);a=ap.parse_args()
    if a.mode=='preflight':print(json.dumps(preflight(),sort_keys=True))
    else:sourcefree(a.root)
