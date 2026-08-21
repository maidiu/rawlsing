import hashlib, struct
from dataclasses import dataclass
from enum import Enum

from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder,R5LongShardedReader
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_json
from rawlsing_next.pre553_r5_model import R5BuildConfig,R5ReleaseIdentity
from rawlsing_next.pre553_r5_seam import iter_source_native_rows


def h(s): return hashlib.sha256(s.encode()).hexdigest()
class S(str,Enum): OBS="OBSERVED_STORAGE_VALUE"; SYS="SYSTEM_MISSING"; USER="FORMAT_USER_MISSING_VALUE"
@dataclass(frozen=True)
class V:
    ordinal:int; name:str; storage_type:str|None; variable_label:str|None; value_labels:dict; missing_declarations:tuple; display_metadata:dict; topology_metadata:dict
@dataclass(frozen=True)
class C:
    row_ordinal:int; variable_ordinal:int; variable_name:str; raw_value:object; missing_state:S; source_missing_declaration:object=None; raw_value_label:object=None
class I:
    source_sha256="1"*64; source_format="SAV"; row_count=3
    reader_configuration={"mode":"FROZEN","compatibility":None}; file_metadata={"encoding":"UTF-8"}
    variables=(
        V(0,"q0","F8","Q0",{"-1":"Missing"},({"kind":"value","value":-1},),{"format":"F2.0"},{"mr_sets":[{"id":"A","members":["q0"]},{"id":"B","members":["q0"]}]}),
        V(1,"q1","A16","Q1",{},(),{"format":"A16"},{"ranked":True}),
    )
    def iter_batches(self,batch_size):
        allcells=(
            C(1,0,"q0",-0.0,S.OBS,None,"Zero"),C(1,1,"q1","",S.OBS,None,"Blank"),
            C(2,0,"q0",None,S.SYS,{"kind":"system"},None),C(2,1,"q1","A\x00B",S.OBS,None,None),
            C(3,0,"q0",-1,S.USER,{"kind":"value","value":-1},"Missing"),C(3,1,"q1","e\u0301",S.OBS,None,None),
        )
        for i in range(0,len(allcells),batch_size): yield allcells[i:i+batch_size]

def rid(): return R5ReleaseIdentity("REL-EQ",h("sem"),{"kind":"SOURCE_ARTIFACT","object_id":"src","content_hash":I.source_sha256},h("manifest"),{f"M{i:02d}":("p",) for i in range(1,19)},{"decoder":"frozen"},h("compiler"),h("c11"))


def test_independent_source_physical_projection_survives_carrier(tmp_path):
    target=tmp_path/"eq"
    cfg=R5BuildConfig(run_max_rows=2,run_max_bytes=900,shard_max_rows=3,shard_max_bytes=1400,merge_fan_in=2,verified_spool_memory_bytes=128)
    R5LongShardedBuilder(cfg).build(iter_source_native_rows(I(),batch_size=2),release_identity=rid(),target_directory=target)
    reader=R5LongShardedReader(target); reader.full_audit()
    cells=sorted(reader.exact_scan(lambda r:r.relation=="source_physical_cells"),key=lambda r:r.object_id)
    assert len(cells)==6
    # Expected truth below is hand-derived from the frozen-decoder fixture, not from candidate output.
    expected={
        (1,0):({"t":"float64_finite","bits":struct.pack(">d",-0.0).hex()},"OBSERVED_STORAGE_VALUE","Zero"),
        (1,1):({"t":"str","v":""},"OBSERVED_STORAGE_VALUE","Blank"),
        (2,0):({"t":"none"},"SYSTEM_MISSING",None),
        (2,1):({"t":"str","v":"A\x00B"},"OBSERVED_STORAGE_VALUE",None),
        (3,0):({"t":"int","v":"-1"},"FORMAT_USER_MISSING_VALUE","Missing"),
        (3,1):({"t":"str","v":"e\u0301"},"OBSERVED_STORAGE_VALUE",None),
    }
    codec=R5TypedValueCodec()
    observed={}
    for row in cells:
        p=row.payload; key=(p["row_ordinal"],p["variable_ordinal"])
        observed[key]=(p["raw_value"],p["missing_state"],codec.decode(p["raw_value_label"]))
    assert observed==expected
    variables=list(reader.exact_scan(lambda r:r.relation=="source_variables"))
    assert len(variables)==2
    q0=next(r for r in variables if r.payload["ordinal"]==0)
    assert len(q0.payload["missing_declarations"])==1
    topo=codec.decode(q0.payload["topology_metadata"])
    assert [x["id"] for x in topo["mr_sets"]]==["A","B"]
