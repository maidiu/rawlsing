from dataclasses import dataclass
import hashlib, json

import pytest

from rawlsing_next.pre553_r5_c11 import R5C11Facade, canonical_row_to_object, iter_release_rows, object_to_canonical_row
from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder, R5LongShardedReader
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5ReleaseIdentity


def h(v): return hashlib.sha256(v.encode()).hexdigest()

def canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True)

@dataclass(frozen=True)
class ExactRef:
    kind:str; object_id:str; content_hash:str
    @property
    def key(self): return f"{self.kind}|{self.object_id}|{self.content_hash}"

@dataclass(frozen=True)
class AuthorityRef:
    authority_id:str; authority_version:str; authority_content_hash:str

@dataclass(frozen=True)
class TypedAbsence:
    state:str; detail:object=None

class EmpiricalUniverse:
    FAMILY="EmpiricalUniverse@1.0.0"
    def __init__(self, *, typed_state, authority_snapshot_refs, dependency_refs,
                 producer_replay_locator_or_reference_root, raw_source_identity):
        self.typed_state=typed_state; self.authority_snapshot_refs=tuple(authority_snapshot_refs)
        self.dependency_refs=tuple(dependency_refs)
        self.producer_replay_locator_or_reference_root=producer_replay_locator_or_reference_root
        self.semantic_fields={"raw_source_identity":raw_source_identity}
        projection={"typed_state":typed_state,"raw_source_identity":raw_source_identity,
                    "authority":repr(self.authority_snapshot_refs),"dependency":repr(self.dependency_refs),
                    "producer":repr(producer_replay_locator_or_reference_root)}
        self.content_hash=h(canon(projection)); self.object_id=f"universe:{raw_source_identity}"
        self.ref=ExactRef("EmpiricalUniverse",self.object_id,self.content_hash)


def resolver(name):
    return {"ExactRef":ExactRef,"AuthorityRef":AuthorityRef,"TypedAbsence":TypedAbsence,"EmpiricalUniverse":EmpiricalUniverse}[name]


def test_c11_adapter_reconstructs_through_constructor_and_checks_identity():
    obj=EmpiricalUniverse(typed_state="UNIVERSE_IDENTIFIED",authority_snapshot_refs=(AuthorityRef("A","1",h("a")),),
                          dependency_refs=(ExactRef("D","d",h("d")),),producer_replay_locator_or_reference_root=ExactRef("R","r",h("r")),
                          raw_source_identity="RAW-X")
    row=object_to_canonical_row(obj)
    rebuilt=canonical_row_to_object(row,class_resolver=resolver)
    assert rebuilt.object_id==obj.object_id
    assert rebuilt.content_hash==obj.content_hash
    assert rebuilt.semantic_fields==obj.semantic_fields


def test_accepted_c11_bounded_reference_roundtrip_when_frozen_modules_present(tmp_path):
    try:
        from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate
        from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
        from rawlsing_next.pre553_c11_repository import C11Repository
    except ModuleNotFoundError:
        pytest.skip("local worker lacks repository checkout; exact accepted integration runs in repository environment")
    candidate=_candidate("r5")
    repo=C11Repository(); result=ingest_c11_source_release(candidate,repo)
    assert result.accepted
    release=repo.resolve_release_exact(result.release_ref)
    rid=R5ReleaseIdentity(
        release.release_id,release.semantic_release_hash,release.source_artifact_ref.as_dict(),release.source_release_manifest_hash,
        release.m01_m18_coverage,{"frozen_decoder_fixture":"repository_test"},h("R5_COMPILER"),h("FROZEN_C11"))
    target=tmp_path/"r5"
    cfg=R5BuildConfig(run_max_rows=2,run_max_bytes=2048,shard_max_rows=3,shard_max_bytes=4096,merge_fan_in=2,verified_spool_memory_bytes=512)
    R5LongShardedBuilder(cfg).build(iter_release_rows(release),release_identity=rid,target_directory=target)
    reader=R5LongShardedReader(target); reader.full_audit()
    facade=R5C11Facade(reader)
    rebuilt=facade.materialize_bounded_release(max_objects=100)
    assert rebuilt.release_ref==release.release_ref
    assert rebuilt.replay_manifest.ref==release.replay_manifest.ref
    assert [x.ref for x in rebuilt.public_objects]==[x.ref for x in release.public_objects]
    assert [x.ref for x in rebuilt.internal_records]==[x.ref for x in release.internal_records]
    rebuilt_repo=facade.materialize_bounded_repository(max_objects=100)
    assert rebuilt_repo.resolve_release_exact(release.release_ref).release_ref==release.release_ref
