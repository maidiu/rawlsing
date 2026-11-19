from __future__ import annotations
import hashlib, itertools, json, sqlite3, time, os
from pathlib import Path
from types import MappingProxyType
from unittest.mock import patch

import pytest
from rawlsing_next.tests.test_pyat960_s1e_source_i02 import _fixture
from rawlsing_next import pre553_source_i02_handoff as handoff
from rawlsing_next.pre553_r157_projection_adapter import decode_fixture_config, SourceConfig
from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate, VerifiedDirectEstate
from streaming_estate import write_streaming_estate, open_stream_native_estate, audit_stream_estate, StreamRefusal

BASE=Path('/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T')

def _sections(tmp_path, *, changed=False):
    root=Path(tmp_path); root.mkdir(parents=True,mode=0o700,exist_ok=True); private=root/'private'; private.mkdir(mode=0o700)
    f=_fixture(root/'fixture'); path,sha,rows,cfg,doc,inv,policy,frontier,census=f
    if changed:
        doc=json.loads(json.dumps(doc)); doc["response_slots"][0]["values"][0]["response_state"]="DK"; cfg=SourceConfig(doc)
    inc=decode_fixture_config(cfg,path)
    try:
        p=handoff.build_governed_c11_projection(cfg,source_sha256=sha,row_count=rows,row_native_keys=None)
        spool=root/'spool';spool.mkdir();paths={fam:spool/(fam+'.jsonl') for fam in handoff.SPOOL_FAMILIES}
        counts,metrics,slots,key=handoff._project_spooled_families(config=cfg,projection=p,incidence=inc,spool_paths=paths,batch_size=2,row_native_keys=None)
        manifest,source,declared,_=handoff._manifest_and_sections(projection=p,incidence=inc,spool_paths=paths,counts=counts,universe_ref=p.universes[0].ref)
    finally:
        inc.close()
    def make(override=None):
        secs={}
        for fam in handoff.ALL_FAMILIES:
            if fam in handoff.SPOOL_FAMILIES:
                base=handoff._spool_section(paths[fam],fam)
            else:
                base=tuple(source.sections[fam])
            if override and fam in override: base=override[fam](base)
            secs[fam]=base
        return SourcefreeDirectI02Sections(manifest=manifest,sections=MappingProxyType(secs),typed_absences=source.typed_absences,replay_protocol_authority_ref=source.replay_protocol_authority_ref,replay_protocol_version=source.replay_protocol_version,deterministic_tie_order_rules_ref=source.deterministic_tie_order_rules_ref)
    return p, p.universes[0].ref, root, make

def test_old_new_writer_fresh_reader_parity_no_sqlite(tmp_path):
    p,uref,root,make=_sections(tmp_path)
    oldroot=root/'old';oldroot.mkdir(mode=0o700)
    t0=time.perf_counter(); old=write_direct_estate(make(),uref,oldroot,chunk_rows=2); old_s=time.perf_counter()-t0
    newroot=root/'new';newroot.mkdir(mode=0o700); progress=[]
    t0=time.perf_counter(); new=write_streaming_estate(make(),uref,newroot,chunk_rows=2,progress=progress.append); new_s=time.perf_counter()-t0
    assert new.roots.schema=='ANVIL_STREAM_C11_ESTATE@1'
    assert new.roots.logical != old.i02.logical
    assert new.family_counts==old.family_counts
    for member in old.family_counts:
        assert (Path(new.path)/(member+'.parquet')).read_bytes()==(Path(old.path)/(member+'.parquet')).read_bytes()
    # legacy reader still reads the old estate
    legacy=VerifiedDirectEstate(oldroot,exact_path=old.path,independently_held_manifest_sha256=old.manifest_sha256,independently_held_i02=old.i02,current_authorizer=lambda _r: True)
    assert sum(1 for _ in legacy.iter_family('RespondentEvent',batch_size=2))==5
    estate=open_stream_native_estate(newroot,new.path,new.manifest_sha256,new.roots,current_authorizer=lambda r: True,progress=progress.append)
    assert {f:sum(1 for _ in estate.iter_family(f,batch_size=2)) for f in old.family_counts}==old.family_counts
    events=tuple(estate.iter_family('RespondentEvent',batch_size=2))
    selected=tuple(estate.select_events(events[0].scoped_respondent_ref,events[0].native_question_ref))
    assert any(x.ref==events[0].ref for x in selected)
    assert any(p['phase']=='reopened_validation' for p in progress)
    # no sqlite in new normal path
    with patch('sqlite3.connect',side_effect=AssertionError('SQLite reached normal path')):
        root2=root/'new2';root2.mkdir(mode=0o700)
        new2=write_streaming_estate(make(),uref,root2,chunk_rows=2)
        assert not any(p.suffix == '.sqlite' for p in Path(root2).rglob('*'))
    open_stream_native_estate(root2,new2.path,new2.manifest_sha256,new2.roots,current_authorizer=lambda r: True)
    # measured split
    old_bytes=sum(p.stat().st_size for p in Path(old.path).rglob('*') if p.is_file())
    new_bytes=sum(p.stat().st_size for p in Path(new.path).rglob('*') if p.is_file())
    (Path(tmp_path)/'METRICS.json').write_text(json.dumps({'old_seconds':old_s,'new_seconds':new_s,'old_bytes':old_bytes,'new_bytes':new_bytes,'new_proof_scratch_bytes':json.loads((Path(new.path)/'manifest.json').read_text()).get('proof_scratch_bytes'),'sqlite_proof_built':False,'read_back_audit':False},sort_keys=True)+'\n')

def test_changed_legal_input_and_exact_restore(tmp_path):
    p,u,root0,make0=_sections(tmp_path/'base'); p1,u1,root1,make1=_sections(tmp_path/'changed',changed=True)
    b=root0/'b';b.mkdir(mode=0o700); base=write_streaming_estate(make0(),u,b,chunk_rows=2)
    c=root1/'c';c.mkdir(mode=0o700); changed=write_streaming_estate(make1(),u1,c,chunk_rows=2)
    assert changed.roots.logical != base.roots.logical
    assert changed.roots.replay != base.roots.replay
    p2,u2,root2,make2=_sections(tmp_path/'restore'); r=root2/'r';r.mkdir(mode=0o700); restored=write_streaming_estate(make2(),u2,r,chunk_rows=2)
    # same sourcefree content and manifest => same stream identity
    assert restored.roots.logical == base.roots.logical
    assert restored.roots.replay == base.roots.replay

def test_audit_is_readonly_and_separate(tmp_path):
    p,u,root,make=_sections(tmp_path); r=root/'e';r.mkdir(mode=0o700); new=write_streaming_estate(make(),u,r,chunk_rows=2)
    before=hashlib.sha256((Path(new.path)/'manifest.json').read_bytes()).hexdigest()
    roots={'logical':new.roots.logical,'physical':new.roots.physical,'release':new.roots.release,'source':new.roots.source,'replay':new.roots.replay,'universe':new.roots.universe,'schema':new.roots.schema}
    import subprocess,sys
    cmd=[sys.executable,'-B','-c',f"import sys;sys.path.insert(0,'{Path(__file__).resolve().parent}');from streaming_estate import audit_stream_estate,StreamRoots;r=StreamRoots(**{roots!r});print(dict(audit_stream_estate('{r}','{new.path}','{new.manifest_sha256}',r,current_authorizer=lambda _r: True)))"]
    out=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
    assert out.returncode==0,out.stderr
    assert hashlib.sha256((Path(new.path)/'manifest.json').read_bytes()).hexdigest()==before

def test_drop_duplicate_and_locator_refusals(tmp_path):
    p,uref,root,make=_sections(tmp_path); oldroot=root/'old';oldroot.mkdir(mode=0o700); old=write_direct_estate(make(),uref,oldroot,chunk_rows=2)
    with pytest.raises(StreamRefusal,match='LEGACY_EXPECTED_ROOT_UNVERIFIABLE'):
        r=root/'stale';r.mkdir(mode=0o700);write_streaming_estate(make(),uref,r,chunk_rows=2,expected_i02=old.i02)
    def drop(gen):
        it=iter(gen); next(it); return it
    with pytest.raises(StreamRefusal,match='FAMILY_CENSUS_MISMATCH|EVENT_LOCATOR_COUNT_MISMATCH'):
        r=root/'drop';r.mkdir(mode=0o700);write_streaming_estate(make({'RespondentEvent':drop}),uref,r,chunk_rows=2)
    def dup(gen):
        it=iter(gen); first=next(it); return itertools.chain([first, first], it)
    with pytest.raises(StreamRefusal,match='DUPLICATE_EXACT_REF'):
        r=root/'dup';r.mkdir(mode=0o700);write_streaming_estate(make({'RespondentEvent':dup}),uref,r,chunk_rows=2)
    r=root/'new';r.mkdir(mode=0o700); new=write_streaming_estate(make(),uref,r,chunk_rows=2)
    mp=Path(new.path)/'manifest.json'; m=json.loads(mp.read_text()); m['event_locator_count']+=1; raw=(json.dumps(m,sort_keys=True)+'\n').encode(); mp.write_bytes(raw)
    with pytest.raises(StreamRefusal,match='LOCATOR_COUNT_MISMATCH'):
        open_stream_native_estate(r,new.path,hashlib.sha256(raw).hexdigest(),new.roots,current_authorizer=lambda r: True)
    with pytest.raises(StreamRefusal,match='CURRENT_AUTHORITY_REFUSED'):
        open_stream_native_estate(r,new.path,new.manifest_sha256,new.roots,current_authorizer=lambda r: False)
