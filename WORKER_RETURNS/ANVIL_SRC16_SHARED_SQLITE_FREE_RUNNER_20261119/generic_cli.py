#!/usr/bin/env python3
"""Generic source-profile injection for the existing SQLite-free operator path.

Modes:
  sourcefree  -- actual shared CLI exercise with generated keyed sourcefree data
  src16-metadata -- exact private SRC16 grant/config/binding admission, no source
  src16-run   -- exact SRC16 source path injection into the same shared path;
                 provided for owner launch only, never invoked by this task

Private SRC16 paths/config/grant bytes are accepted only from environment and
are never printed.
"""
from __future__ import annotations
import argparse, dataclasses, hashlib, importlib.util, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAND = Path(os.environ["ANVIL_CANDIDATE_TREE"])
OPER = HERE / "common"
sys.path[:0] = [str(CAND), str(OPER), str(HERE)]
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, load_source_config, canonical_config_hash, source_read_request_from_config, decode_fixture_config, row_native_keys_from_transport
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
from sqlite_free_single_pass import build_single_pass
from streaming_estate import open_stream_native_estate, StreamRoots

class Refusal(RuntimeError):
    def __init__(self, code, detail=""):
        super().__init__(code + (f": {detail}" if detail else "")); self.code=code

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def sourcefree(root: Path) -> dict:
    root=Path(root).absolute(); root.mkdir(mode=0o700,parents=True,exist_ok=True)
    private=root/'private'; private.mkdir(mode=0o700,exist_ok=True)
    f=source_fixture(root/'fixture', keyed=True, values=(1.,2.,0.,7.,None,-1.))
    progress=[]
    rec=build_single_pass(config=f['config'], source_path=f['path'], private_root=private,
                          chunk_rows=2, compact_spool=True,
                          progress=lambda x: progress.append(x))
    estate=open_stream_native_estate(private, rec.path, rec.manifest_sha256, rec.roots,
                                     current_authorizer=lambda roots: roots==rec.roots,
                                     progress=lambda x: progress.append(x))
    counts={family: sum(1 for _ in estate.iter_family(family,batch_size=2)) for family in estate.manifest['family_counts']}
    return {"status":"SOURCEFREE_KEYED_PASS","keyed":True,"family_counts":counts,
            "proof_schema":rec.roots.schema,"sqlite_present":any(p.suffix=='.sqlite' for p in private.rglob('*')),
            "progress_phases":[p.get('phase') for p in progress],"source_read":False}

def _load_resolver(binding_dir: Path):
    import importlib.util
    resolver_path=binding_dir/'SRC16.exact_resolver.py'
    spec=importlib.util.spec_from_file_location('src16_resolver_private',resolver_path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    binding_path=binding_dir/'SRC16.construction.binding.json'
    return mod.ExactSrc16Resolver(binding_path), binding_path

def src16_metadata() -> dict:
    binding_dir=Path(os.environ['ANVIL_SRC16_GRANT_DIR']).absolute()
    cfg_path=Path(os.environ['ANVIL_SRC16_CONFIG']).absolute()
    cfg=load_source_config(cfg_path)
    file_sha=sha(cfg_path); canonical=canonical_config_hash(cfg)
    if file_sha!='1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7':
        raise Refusal('SRC16_CONFIG_FILE_DRIFT')
    if canonical!='c26e8e71afbc629a9f19708cedb7b38cc2ba3cefb9ac53f11e0608044e64b534':
        raise Refusal('SRC16_CONFIG_CANONICAL_DRIFT')
    if (cfg.source_id!='SRC16' or cfg.active_source_sha256!='e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204'):
        raise Refusal('SRC16_SOURCE_IDENTITY_DRIFT')
    d=cfg.document
    if (d['binding']['row_count'],len(d['physical_slots']),len(d['response_slots']),len(d['coordinate_slots']),len(d['weight_slots']))!=(1613,216,157,2,0):
        raise Refusal('SRC16_CONFIG_SHAPE_DRIFT')
    resolver,binding_path=_load_resolver(binding_dir)
    req=resolver.request
    if (req.source_id,req.source_sha256,req.purpose,req.consumer_use)!=( 'SRC16','e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204','FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY','EXISTING_PRE553_SOURCE_BACKED_C11'):
        raise Refusal('SRC16_BINDING_SCOPE_DRIFT')
    if req.metadata_freeze_refs != (d['identity']['metadata_witness_ref'],):
        # Normalize exact mapping/ref comparison without exposing values.
        from rawlsing_next.pre553_empirical_objects import ExactRef
        if tuple(ExactRef(**x) if isinstance(x,dict) else x for x in req.metadata_freeze_refs) != (ExactRef(**d['identity']['metadata_witness_ref']),):
            raise Refusal('SRC16_METADATA_REF_DRIFT')
    decision=resolver.resolve_current(req)
    if decision.currentness!='CURRENT_GRANTED' or decision.revocation_ref is not None:
        raise Refusal('SRC16_CURRENT_OR_REVOCATION_REFUSED')
    negatives=[]
    for name,other in (
        ('other_source',dataclasses.replace(req,source_id='SRC15')),
        ('analysis_purpose',dataclasses.replace(req,purpose='ANALYSIS')),
        ('incorrect_scope',dataclasses.replace(req,semantic_use_scope=('ANALYSIS_ONLY',))),
    ):
        try: resolver.resolve_current(other)
        except Exception as exc: negatives.append({'case':name,'refused':True,'code':str(exc)})
        else: negatives.append({'case':name,'refused':False,'code':'NOT_REFUSED'})
    return {'status':'SRC16_METADATA_ADMISSION_PASS','source_id':'SRC16','config_file_sha256':file_sha,
            'config_canonical_sha256':canonical,'shape':{'rows':1613,'physical_slots':216,'response_slots':157,'coordinate_slots':2,'weight_slots':0},
            'currentness':decision.currentness,'revocation':None,'request_scope':list(req.semantic_use_scope),
            'negative_cases':negatives,'source_read_performed':False,'grant_bytes_published':False}

def src16_run(root: Path) -> dict:
    # Owner-only command path. Refuses unless the exact private admission passes;
    # it does not print private paths or grant/config values.
    meta=src16_metadata()
    binding_dir=Path(os.environ['ANVIL_SRC16_GRANT_DIR']).absolute()
    cfg_path=Path(os.environ['ANVIL_SRC16_CONFIG']).absolute()
    source_path=Path(os.environ['ANVIL_SRC16_SOURCE_PATH']).absolute()
    resolver,_=_load_resolver(binding_dir)
    cfg=load_source_config(cfg_path); root=Path(root).absolute(); private=root/'private'; private.mkdir(mode=0o700,parents=True,exist_ok=True)
    # The shared single-pass path checks resolver/current before decoding.
    rec=build_single_pass(config=cfg,source_path=source_path,private_root=private,
                          resolver=resolver,host=resolver.request.host,purpose=resolver.request.purpose,
                          consumer_use=resolver.request.consumer_use,semantic_use_scope=resolver.request.semantic_use_scope,
                          request=resolver.request,grant_ref=resolver.decision.source_permission_refs[0],
                          decision_ref=resolver.decision.decision_ref,
                          chunk_rows=512,progress=lambda x: print(json.dumps({k:v for k,v in x.items() if k not in ('path',)},sort_keys=True),flush=True))
    return {'status':'SRC16_SOURCE_LAUNCH_PATH_READY_NOT_RUN_BY_AGENT','roots':{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(rec.family_counts),'source_read_performed_by_agent':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('sourcefree','src16-metadata','src16-run'),required=True);ap.add_argument('--root');a=ap.parse_args()
    try:
        if a.mode=='sourcefree': out=sourcefree(Path(a.root))
        elif a.mode=='src16-metadata': out=src16_metadata()
        else: out=src16_run(Path(a.root))
    except Exception as exc:
        print(json.dumps({'status':'REFUSED','code':str(exc),'source_read_performed':False},sort_keys=True));return 2
    print(json.dumps(out,sort_keys=True));return 0
if __name__=='__main__': raise SystemExit(main())
