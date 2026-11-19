#!/usr/bin/env python3
"""Thin sourcefree producer/reader adapter around the established compact boundary."""
from __future__ import annotations
import json,os,subprocess,sys,time,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAND=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree');sys.path[:0]=[str(CAND),str(HERE)]
def producer(root):
 from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
 from rawlsing_next.pre553_source_i02_handoff import build_governed_c11_projection,_project_spooled_families,_manifest_and_sections,SPOOL_FAMILIES,_cleanup_spool
 from rawlsing_next.pre553_r157_projection_adapter import row_native_keys_from_transport
 from rawlsing_next.pre553_physical_decoder import decode_sav
 from streaming_estate import write_streaming_estate
 import tempfile
 p=Path(root);p.mkdir(mode=0o700,parents=True,exist_ok=True);f=source_fixture(p/'src',keyed=True,values=(1.0,2.0,0.0,7.0,None,-1.0,1.0,2.0,None,-1.0)*9,config_kwargs={'response_state_overrides':{-1.0:'NOT_ASKED'}});cfg=f['config'];inc=decode_sav(f['path'],encoding=None);private=p/'private';private.mkdir(mode=0o700,parents=True,exist_ok=True);spool=Path(tempfile.mkdtemp(prefix='.s1e-i02-spool-',dir=p));paths={x:spool/(x+'.jsonl') for x in SPOOL_FAMILIES};keys=row_native_keys_from_transport(cfg,incidence=inc);doc=cfg.document;proj=build_governed_c11_projection(cfg,source_sha256=doc['binding']['source_sha256'],row_count=doc['binding']['row_count'],row_native_keys=keys);counts,_,_,_=_project_spooled_families(config=cfg,projection=proj,incidence=inc,spool_paths=paths,batch_size=2,row_native_keys=keys);manifest,source,declared,_=_manifest_and_sections(projection=proj,incidence=inc,spool_paths=paths,counts=counts,universe_ref=proj.universes[0].ref);t=time.perf_counter();rec=write_streaming_estate(source,proj.universes[0].ref,private,chunk_rows=2,progress=lambda x:(p/'progress.jsonl').open('a').write(json.dumps(x,sort_keys=True)+'\n'));_cleanup_spool(paths,spool);out={'producer_pid':os.getpid(),'path':rec.path,'manifest_sha256':rec.manifest_sha256,'roots':{k:getattr(rec.roots,k) for k in ('logical','physical','release','source','replay','universe','schema')},'family_counts':dict(rec.family_counts),'elapsed':time.perf_counter()-t,'rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'retained_bytes':rec.retained_bytes,'sqlite_files':[str(x) for x in p.rglob('*.sqlite')]};(p/'build.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PRODUCER_COMMITTED'}))

def reader(root):
 from streaming_estate import StreamRoots,open_stream_native_estate
 from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
 p=Path(root);b=json.loads((p/'build.json').read_text());alive=subprocess.run(['ps','-p',str(b['producer_pid']),'-o','pid='],capture_output=True,text=True).stdout.strip()
 if alive:
  raise SystemExit('PRODUCER_STILL_ALIVE')
 roots=StreamRoots(**b['roots'])
 est=open_stream_native_estate(p/'private',exact_path=b['path'],manifest_sha256=b['manifest_sha256'],roots=roots,current_authorizer=lambda x:x==roots)
 counts={f:sum(1 for _ in est.iter_family(f)) for f in ALL_FAMILIES}
 out={'reader_pid':os.getpid(),'producer_exited_before_reader':True,'family_counts':counts,'roots_equal':est.i02==roots,'sqlite_files':[str(x) for x in p.rglob('*.sqlite')]}
 (p/'reader.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':'READER_OPENED','counts':counts}))
if __name__=='__main__':
 mode,root=sys.argv[1],sys.argv[2]
 {'producer':producer,'reader':reader}[mode](root)
