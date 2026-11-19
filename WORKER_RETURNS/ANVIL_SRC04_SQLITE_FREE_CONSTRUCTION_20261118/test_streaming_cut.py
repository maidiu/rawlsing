from __future__ import annotations
import hashlib, itertools, json, sqlite3, time, os
from pathlib import Path
from types import MappingProxyType
from unittest.mock import patch

import pytest
from rawlsing_next.tests.test_pyat960_s1e_source_i02 import _fixture
from rawlsing_next import pre553_source_i02_handoff as handoff
from rawlsing_next.pre553_r157_projection_adapter import decode_fixture_config
from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate, VerifiedDirectEstate
from streaming_estate import write_streaming_estate, verify_streaming_estate, StreamRefusal

BASE=Path('/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T')

def _sections(tmp_path):
    root=Path(tmp_path); private=root/'private'; private.mkdir(mode=0o700)
    f=_fixture(root/'fixture'); path,sha,rows,cfg,doc,inv,policy,frontier,census=f
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
    newroot=root/'new';newroot.mkdir(mode=0o700)
    t0=time.perf_counter(); new=write_streaming_estate(make(),uref,newroot,chunk_rows=2,expected_i02=old.i02); new_s=time.perf_counter()-t0
    assert new.roots.logical==old.i02.logical
    assert new.roots.schema=='ANVIL_STREAM_C11_ESTATE@1'
    assert new.roots.physical!=old.i02.physical
    assert new.family_counts==old.family_counts
    for member in old.family_counts:
        assert (Path(new.path)/(member+'.parquet')).read_bytes()==(Path(old.path)/(member+'.parquet')).read_bytes()
    # legacy reader still reads the old estate
    legacy=VerifiedDirectEstate(oldroot,exact_path=old.path,independently_held_manifest_sha256=old.manifest_sha256,independently_held_i02=old.i02,current_authorizer=lambda _r: True)
    assert sum(1 for _ in legacy.iter_family('RespondentEvent',batch_size=2))==5
    counts=verify_streaming_estate(newroot,new.path,new.manifest_sha256,new.roots,current_authorizer=lambda r: True)
    assert counts==old.family_counts
    # no sqlite in new normal path
    with patch('sqlite3.connect',side_effect=AssertionError('SQLite reached normal path')):
        root2=root/'new2';root2.mkdir(mode=0o700)
        new2=write_streaming_estate(make(),uref,root2,chunk_rows=2,expected_i02=old.i02)
        assert not any(p.suffix == '.sqlite' for p in Path(root2).rglob('*'))
    verify_streaming_estate(root2,new2.path,new2.manifest_sha256,new2.roots,current_authorizer=lambda r: True)
    # measured split
    old_bytes=sum(p.stat().st_size for p in Path(old.path).rglob('*') if p.is_file())
    new_bytes=sum(p.stat().st_size for p in Path(new.path).rglob('*') if p.is_file())
    (Path(tmp_path)/'METRICS.json').write_text(json.dumps({'old_seconds':old_s,'new_seconds':new_s,'old_bytes':old_bytes,'new_bytes':new_bytes,'sqlite_proof_built':False,'read_back_audit':False},sort_keys=True)+'\n')

def test_drop_duplicate_and_locator_refusals(tmp_path):
    p,uref,root,make=_sections(tmp_path); oldroot=root/'old';oldroot.mkdir(mode=0o700); old=write_direct_estate(make(),uref,oldroot,chunk_rows=2)
    def drop(gen):
        it=iter(gen); next(it); return it
    with pytest.raises(StreamRefusal,match='FAMILY_CENSUS_MISMATCH|EVENT_LOCATOR_COUNT_MISMATCH'):
        r=root/'drop';r.mkdir(mode=0o700);write_streaming_estate(make({'RespondentEvent':drop}),uref,r,chunk_rows=2,expected_i02=old.i02)
    def dup(gen):
        it=iter(gen); first=next(it); return itertools.chain([first, first], it)
    with pytest.raises(StreamRefusal,match='DUPLICATE_EXACT_REF'):
        r=root/'dup';r.mkdir(mode=0o700);write_streaming_estate(make({'RespondentEvent':dup}),uref,r,chunk_rows=2,expected_i02=old.i02)
    r=root/'new';r.mkdir(mode=0o700); new=write_streaming_estate(make(),uref,r,chunk_rows=2,expected_i02=old.i02)
    mp=Path(new.path)/'manifest.json'; m=json.loads(mp.read_text()); m['event_locator_count']+=1; raw=(json.dumps(m,sort_keys=True)+'\n').encode(); mp.write_bytes(raw)
    with pytest.raises(StreamRefusal,match='LOCATOR_COUNT_MISMATCH'):
        verify_streaming_estate(r,new.path,hashlib.sha256(raw).hexdigest(),new.roots,current_authorizer=lambda r: True)
    with pytest.raises(StreamRefusal,match='CURRENT_AUTHORITY_REFUSED'):
        verify_streaming_estate(r,new.path,new.manifest_sha256,new.roots,current_authorizer=lambda r: False)
