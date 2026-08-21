import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import pytest

from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder, R5LongShardedReader
from rawlsing_next.pre553_r5_codec import canonical_json
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5IntegrityError, R5QuarantinedError, R5ReleaseIdentity


def h(text): return hashlib.sha256(text.encode()).hexdigest()


def identity(tag="x"):
    return R5ReleaseIdentity(
        release_id=f"REL-{tag}", semantic_release_hash=h(f"semantic:{tag}"),
        source_artifact_ref={"kind":"SOURCE_ARTIFACT","object_id":f"src:{tag}","content_hash":h(f"source:{tag}")},
        source_release_manifest_hash=h(f"manifest:{tag}"),
        m01_m18_coverage={f"M{i:02d}": (f"proof-{i}",) for i in range(1,19)},
        decoder_receipt={"decoder":"frozen","version":"1"},
        compiler_contract_digest=h("compiler"), c11_authority_digest=h("c11"),
    )


def rows(n=75):
    for i in range(n):
        payload={"i":i,"unique":"u"+str(i)+"-"+("x"*(i%17)),"state":"MISSING" if i%11==0 else "OBSERVED"}
        yield R5CanonicalRow("respondent_events" if i%2 else "empirical_universes",
                             "RespondentEvent@1" if i%2 else "EmpiricalUniverse@1",
                             f"urn:r5:{i:08d}", h(canonical_json(payload)), payload)


def config(**kw):
    base=dict(run_max_rows=5, run_max_bytes=900, shard_max_rows=7, shard_max_bytes=1300,
              merge_fan_in=3, verified_spool_memory_bytes=256)
    base.update(kw); return R5BuildConfig(**base)


def test_forced_multi_run_multi_shard_build_is_exact_and_cacheless(tmp_path):
    target=tmp_path/"release"
    telemetry=R5LongShardedBuilder(config()).build(rows(), release_identity=identity(), target_directory=target)
    assert telemetry["initial_runs"] > 3
    assert telemetry["merge_passes"] >= 1
    assert telemetry["final_shards"] > 3
    reader=R5LongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"])
    audit=reader.full_audit()
    assert audit["canonical_rows"] == 75
    found=list(reader.exact_scan(lambda r: r.payload["state"]=="MISSING"))
    assert len(found)==7
    assert not any((target/name).exists() for name in ("cache","index","bitmap","matrix"))


def test_exact_scan_negative_closes_exhaustive_inventory(tmp_path):
    target=tmp_path/"release"
    R5LongShardedBuilder(config()).build(rows(30), release_identity=identity("negative"), target_directory=target)
    reader=R5LongShardedReader(target)
    assert list(reader.exact_scan(lambda r: r.object_id=="no-such-object")) == []
    # Corrupt the last member: a new exact negative scan must fail, never return plausible empty.
    desc=list(reader.iter_inventory())[-1]
    p=target/"members"/desc["member"]
    b=p.read_bytes(); p.write_bytes(b[:-1]+bytes([b[-1]^1]))
    with pytest.raises(R5IntegrityError):
        list(R5LongShardedReader(target).exact_scan(lambda r: r.object_id=="no-such-object"))


def test_input_reorder_same_config_is_byte_deterministic(tmp_path):
    material=list(rows(40))
    left=tmp_path/"left"; right=tmp_path/"right"
    a=R5LongShardedBuilder(config()).build(material, release_identity=identity("det"), target_directory=left)
    b=R5LongShardedBuilder(config()).build(reversed(material), release_identity=identity("det"), target_directory=right)
    assert a["logical_stream_digest"]==b["logical_stream_digest"]
    assert a["physical_root_id"]==b["physical_root_id"]
    assert (left/"root.json").read_bytes()==(right/"root.json").read_bytes()
    assert (left/"member_inventory.jsonl").read_bytes()==(right/"member_inventory.jsonl").read_bytes()


def test_relayout_changes_physical_root_not_semantic_stream(tmp_path):
    material=list(rows(40))
    left=tmp_path/"left"; right=tmp_path/"right"
    a=R5LongShardedBuilder(config(shard_max_rows=4)).build(material, release_identity=identity("layout"), target_directory=left)
    b=R5LongShardedBuilder(config(shard_max_rows=13)).build(material, release_identity=identity("layout"), target_directory=right)
    assert a["logical_stream_digest"]==b["logical_stream_digest"]
    assert a["physical_root_id"]!=b["physical_root_id"]
    assert R5LongShardedReader(left).full_audit()["logical_stream_digest"] == R5LongShardedReader(right).full_audit()["logical_stream_digest"]


def test_duplicate_exact_identity_rejected_not_deduplicated(tmp_path):
    material=list(rows(3)); material.append(material[0])
    with pytest.raises(R5IntegrityError):
        R5LongShardedBuilder(config()).build(material, release_identity=identity("dup"), target_directory=tmp_path/"release")


def test_whole_member_corruption_quarantines_reader(tmp_path):
    target=tmp_path/"release"
    R5LongShardedBuilder(config()).build(rows(20), release_identity=identity("corrupt"), target_directory=target)
    reader=R5LongShardedReader(target)
    desc=next(reader.iter_inventory())
    p=target/"members"/desc["member"]
    raw=bytearray(p.read_bytes()); raw[len(raw)//2]^=1; p.write_bytes(raw)
    with pytest.raises(R5IntegrityError): reader.full_audit()
    assert reader.quarantined
    with pytest.raises(R5QuarantinedError): list(reader.iter_rows())


def test_inventory_corruption_fails_before_rows(tmp_path):
    target=tmp_path/"release"
    R5LongShardedBuilder(config()).build(rows(10), release_identity=identity("inv"), target_directory=target)
    p=target/"member_inventory.jsonl"; raw=bytearray(p.read_bytes()); raw[5]^=1; p.write_bytes(raw)
    reader=R5LongShardedReader(target)
    with pytest.raises(R5IntegrityError): list(reader.iter_rows())


def test_toctou_consumes_verified_spool_not_mutated_backing_path(tmp_path):
    target=tmp_path/"release"
    R5LongShardedBuilder(config(shard_max_rows=100)).build(rows(10), release_identity=identity("toctou"), target_directory=target)
    mutated={"done":False}
    def hook(phase, detail):
        if phase=="after_verified_read" and "member-" in detail["path"] and not mutated["done"]:
            p=Path(detail["path"]); data=bytearray(p.read_bytes()); data[-2]^=1; p.write_bytes(data); mutated["done"]=True
    reader=R5LongShardedReader(target, fault_hook=hook)
    # First scan interprets authenticated spool bytes and therefore remains exact.
    assert len(list(reader.iter_rows()))==10
    # A fresh verification sees the canonical corruption and fails closed.
    with pytest.raises(R5IntegrityError): list(R5LongShardedReader(target).iter_rows())

def test_temp_path_and_hash_seed_do_not_change_semantic_or_physical_identity(tmp_path):
    import os, subprocess, sys, textwrap
    code=r'''
import hashlib,json,os,sys,tempfile
from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder
from rawlsing_next.pre553_r5_model import R5BuildConfig,R5CanonicalRow,R5ReleaseIdentity

def h(s): return hashlib.sha256(s.encode()).hexdigest()
rid=R5ReleaseIdentity('REL-D',h('sem'),{'kind':'SOURCE_ARTIFACT','object_id':'s','content_hash':h('src')},h('m'),{f'M{i:02d}':('p',) for i in range(1,19)},{'decoder':'frozen'},h('c'),h('a'))
def rs():
  data=list(range(30)); data=data[::2]+data[1::2]
  for i in data:
    p={'i':i,'set_material':sorted({'z'+str(i%5),'a'+str(i%7)})}
    yield R5CanonicalRow('r','EmpiricalUniverse@1','id%04d'%i,h(json.dumps(p,sort_keys=True)),p)
cfg=R5BuildConfig(run_max_rows=3,run_max_bytes=400,shard_max_rows=5,shard_max_bytes=700,merge_fan_in=2,verified_spool_memory_bytes=128)
root=tempfile.mkdtemp(prefix='different-temp-')
t=R5LongShardedBuilder(cfg).build(rs(),release_identity=rid,target_directory=os.path.join(root,'release'))
print(json.dumps({'root':t['physical_root_id'],'logical':t['logical_stream_digest']}))
'''
    outputs=[]
    for seed in ('1','777','123456'):
        env=dict(os.environ); env['PYTHONHASHSEED']=seed
        out=subprocess.check_output([sys.executable,'-c',code],cwd=str(tmp_path.parent.parent if False else Path(__file__).resolve().parents[1]),env=env,text=True)
        outputs.append(json.loads(out))
    assert outputs[0]==outputs[1]==outputs[2]
