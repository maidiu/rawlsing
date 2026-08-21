import hashlib
from pathlib import Path

import pytest

from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5IntegrityError, R5ReleaseIdentity
from rawlsing_next.pre553_r5_shadow import R5GenerationStampedCASSimulator, R5InactiveShadowPublisher, R5InjectedFault


def h(s): return hashlib.sha256(s.encode()).hexdigest()

def identity(tag):
    return R5ReleaseIdentity(
        f"REL-{tag}", h("sem-"+tag), {"kind":"SOURCE_ARTIFACT","object_id":"src-"+tag,"content_hash":h("src-"+tag)},
        h("manifest-"+tag), {f"M{i:02d}":("proof",) for i in range(1,19)},
        {"decoder":"frozen"}, h("compiler"), h("c11"))

def rows(n=15):
    for i in range(n):
        payload={"i":i}
        yield R5CanonicalRow("respondent_events","RespondentEvent@1",f"e{i:04d}",h(str(payload)),payload)

def cfg(): return R5BuildConfig(run_max_rows=3,run_max_bytes=500,shard_max_rows=4,shard_max_bytes=700,merge_fan_in=2,verified_spool_memory_bytes=128)


def semantic_validator(reader):
    audit=reader.full_audit()
    assert audit["canonical_rows"]==15


def test_inactive_publication_never_creates_active_selector(tmp_path):
    pub=R5InactiveShadowPublisher(tmp_path,config=cfg())
    receipt=pub.publish(rows(),release_identity=identity("ok"),semantic_validator=semantic_validator)
    assert receipt.publication_state=="SHADOW_CANDIDATE__NON_SERVING__NONAUTHORITATIVE"
    assert Path(receipt.inactive_release_path).is_dir()
    assert not (tmp_path/"active").exists()
    assert not (tmp_path/"current").exists()


@pytest.mark.parametrize("fault_phase",[
    "staging_created","build_start","members_closed","root_sealed","staging_built",
    "staging_integrity_verified","staging_semantic_validated","before_inactive_promote",
    "after_inactive_promote","sealed_reopen_verified",
])
def test_fault_injection_never_creates_serving_pointer(tmp_path,fault_phase):
    def fault(phase, detail):
        if phase==fault_phase: raise R5InjectedFault(phase)
    pub=R5InactiveShadowPublisher(tmp_path,config=cfg(),fault_hook=fault)
    with pytest.raises(R5InjectedFault):
        pub.publish(rows(),release_identity=identity(fault_phase),semantic_validator=semantic_validator)
    assert not (tmp_path/"active").exists()
    assert not (tmp_path/"current").exists()
    # If fault occurred after content-addressed promotion, only a complete inactive root may remain.
    for path in (tmp_path/"releases").glob("*") if (tmp_path/"releases").exists() else ():
        from rawlsing_next.pre553_r5_carrier import R5LongShardedReader
        R5LongShardedReader(path).full_audit()


def test_generation_stamped_cas_rejects_stale_and_aba(tmp_path):
    cas=R5GenerationStampedCASSimulator()
    a=cas.compare_and_swap(expected_generation=0,expected_root=None,new_root="A",semantic_release_id="S1",admission_binding="ADM1")
    b=cas.compare_and_swap(expected_generation=1,expected_root="A",new_root="B",semantic_release_id="S2",admission_binding="ADM2")
    a2=cas.compare_and_swap(expected_generation=2,expected_root="B",new_root="A",semantic_release_id="S1",admission_binding="ADM1")
    assert a2.generation==3
    with pytest.raises(R5IntegrityError):
        cas.compare_and_swap(expected_generation=1,expected_root="A",new_root="C",semantic_release_id="S3",admission_binding="ADM3")


def test_selector_wrong_semantic_or_admission_binding_rejected_and_query_generation_pinned():
    cas=R5GenerationStampedCASSimulator()
    cas.compare_and_swap(expected_generation=0,expected_root=None,new_root="A",semantic_release_id="S1",admission_binding="ADM1")
    with pytest.raises(R5IntegrityError): cas.pin_query(expected_semantic_release_id="WRONG",expected_admission_binding="ADM1")
    with pytest.raises(R5IntegrityError): cas.pin_query(expected_semantic_release_id="S1",expected_admission_binding="WRONG")
    pin=cas.pin_query(expected_semantic_release_id="S1",expected_admission_binding="ADM1")
    cas.compare_and_swap(expected_generation=1,expected_root="A",new_root="B",semantic_release_id="S2",admission_binding="ADM2")
    with pytest.raises(R5IntegrityError): cas.validate_query_end(pin)
