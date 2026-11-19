"""Savage sourcefree tests: cold persisted original-I03 preimage + S04->FF01.

These are INTERNAL sourcefree proofs, not external source/grant attestation.
"""
from dataclasses import replace
from json import dumps
from pathlib import Path
from subprocess import run
from sys import executable

import pytest

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, ExactRef, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_s04_cold_custody import (
    S04ColdBundle, S04ColdCustodyError, S04ExternalRootPin,
    freeze_s04_i03_sourcefree, read_s04_cold_preimages,
    read_s04_sourcefree_private, receive_ff01_from_pinned_cold,
    write_s04_sourcefree_private,
)
from rawlsing_next.pre553_s04_ff01_consumer import receive_ff01_from_s04
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, ask_s04_exact_condition, receive_s04_i03_research,
)
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case


PERMISSIONS = ("FF01_DESCRIPTIVE_SOURCEFREE",)


def _ready(parity=0, *, tag="S04-COLD-REPLAY"):
    _, _, _, q, r = _case(parity, tag=tag)
    s04 = receive_s04_i03_research(query=q, execution=r)
    original = freeze_s04_i03_sourcefree(query=q, execution=r, knowledge=s04)
    pin = S04ExternalRootPin(q.ref, r.facts[0].ref, r.release_refs[0])
    return original, pin, q, r, s04


def test_roundtrip_cold_exact_preimages_replay_same_s04_ff01_without_i03():
    bundle, anchor, query, execution, knowledge = _ready()
    verified = read_s04_cold_preimages(bundle, external_root=anchor)
    assert verified.query.ref == query.ref
    assert verified.execution.facts[0].ref == execution.facts[0].ref
    assert verified.execution.release_refs == execution.release_refs
    assert verified.knowledge.ref == knowledge.ref
    assert verified.pin_grade.startswith("CALLER_SUPPLIED_EXACT_ROOTS_MATCH")
    cold_ff01 = receive_ff01_from_pinned_cold(
        bundle=bundle, external_root=anchor,
        conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
    )
    hot_ff01 = receive_ff01_from_s04(
        knowledge=knowledge, query=query, execution=execution,
        conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
    )
    assert cold_ff01.ref == hot_ff01.ref
    assert cold_ff01.semantic_projection() == hot_ff01.semantic_projection()


def test_unpinned_cold_read_is_inspection_only_not_ff01_grant():
    bundle, anchor, _, _, _ = _ready()
    read = read_s04_cold_preimages(bundle)
    assert read.pin_grade == "INSPECT_ONLY_UNPINNED__NO_FF01_COLD_ADMISSION"
    with pytest.raises(S04ColdCustodyError, match="pin required"):
        receive_ff01_from_pinned_cold(
            bundle=bundle, external_root=None,
            conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
        )


def test_external_root_is_not_allowed_to_come_from_wrong_fact_or_release():
    bundle, anchor, q, r, s04 = _ready()
    foreign = ExactRef("EmpiricalFact@1.0.0", "urn:test:alien", semantic_hash("alien"))
    with pytest.raises(S04ColdCustodyError, match="EXTERNAL_ROOT_MISMATCH"):
        read_s04_cold_preimages(
            bundle,
            external_root=S04ExternalRootPin(anchor.query_ref, foreign, anchor.release_ref),
        )
    bad_release = ExactRef("RELEASE", "urn:test:wrong-release", semantic_hash("wrong-release"))
    with pytest.raises(S04ColdCustodyError, match="EXTERNAL_ROOT_MISMATCH"):
        receive_ff01_from_pinned_cold(
            bundle=bundle,
            external_root=S04ExternalRootPin(anchor.query_ref, anchor.fact_ref, bad_release),
            conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
        )


def test_self_rehashed_counterfeit_source_cannot_borrow_external_original_pin():
    original, pin, _, _, _ = _ready(parity=0, tag="S04-COLD-CORRECT")
    alternate, alternate_pin, *_ = _ready(parity=1, tag="S04-COLD-CORRECT")
    assert original.ref != alternate.ref
    assert pin.fact_ref != alternate_pin.fact_ref
    with pytest.raises(S04ColdCustodyError, match="EXTERNAL_ROOT_MISMATCH"):
        receive_ff01_from_pinned_cold(
            bundle=alternate, external_root=pin,
            conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
        )


def test_rehashed_corrupted_knowledge_is_not_replayable_to_original_fact():
    bundle, _, _, _, _ = _ready()
    forged = bundle.material()
    forged["knowledge_hash"] = semantic_hash("fake")
    recomputed = S04ColdBundle(canonical_json(forged), semantic_hash(forged))
    with pytest.raises(S04ColdCustodyError, match="regenerate saved S04"):
        read_s04_cold_preimages(recomputed)


def test_rehashed_query_object_id_cannot_reconstruct_trusted_preimage():
    bundle, _, _, _, _ = _ready()
    forged = bundle.material()
    forged["query_preimage"]["object_id"] = "urn:test:wrong"
    recomputed = S04ColdBundle(canonical_json(forged), semantic_hash(forged))
    with pytest.raises(S04ColdCustodyError, match="cannot reconstruct"):
        read_s04_cold_preimages(recomputed)


def test_sourcefree_cold_persistence_is_private_content_addressed_and_repeatable(tmp_path):
    bundle, anchor, _, _, _ = _ready()
    private = tmp_path / "private-s04"
    path = write_s04_sourcefree_private(private, bundle)
    assert path.name == bundle.digest + ".s04-sourcefree.json"
    assert write_s04_sourcefree_private(private, bundle) == path
    assert read_s04_sourcefree_private(path).ref == bundle.ref
    assert receive_ff01_from_pinned_cold(
        bundle=read_s04_sourcefree_private(path), external_root=anchor,
        conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
    ).semantic_projection()["joint_arity"] == 3


def test_private_storage_refuses_world_readable_directory_and_symlink(tmp_path):
    bundle, _, _, _, _ = _ready()
    unsafe = tmp_path / "public-s04"
    unsafe.mkdir(mode=0o755)
    unsafe.chmod(0o755)
    with pytest.raises(S04ColdCustodyError, match="exclude group/world"):
        write_s04_sourcefree_private(unsafe, bundle)
    good = write_s04_sourcefree_private(tmp_path / "private", bundle)
    link = tmp_path / "symlink-to-cold.json"
    link.symlink_to(good)
    with pytest.raises(S04ColdCustodyError, match="symbolic link"):
        read_s04_sourcefree_private(link)
    with pytest.raises(S04ColdCustodyError, match="symlink"):
        write_s04_sourcefree_private(link, bundle)


def test_wrong_filename_and_bytes_refuse_read_without_making_false_zero(tmp_path):
    bundle, _, _, _, _ = _ready()
    path = write_s04_sourcefree_private(tmp_path / "private", bundle)
    renamed = path.parent / ("0" * 64 + ".s04-sourcefree.json")
    renamed.write_bytes(path.read_bytes())
    with pytest.raises(S04ColdCustodyError, match="content-addressed path"):
        read_s04_sourcefree_private(renamed)
    path.write_bytes(b"{}")
    with pytest.raises(S04ColdCustodyError):
        read_s04_sourcefree_private(path)


def test_low_support_counts_stay_held_across_cold_storage():
    _, _, q, r, _ = _ready()
    original = r.facts[0]
    held = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **dict(original.semantic_fields),
    )
    altered_result = replace(r, facts=(held,))
    knowledge = receive_s04_i03_research(query=q, execution=altered_result)
    bundle = freeze_s04_i03_sourcefree(
        query=q, execution=altered_result, knowledge=knowledge,
    )
    pin = S04ExternalRootPin(q.ref, held.ref, r.release_refs[0])
    cold = receive_ff01_from_pinned_cold(
        bundle=bundle, external_root=pin,
        conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
    ).semantic_projection()
    assert cold["producer_state"] == "LOW_SUPPORT"
    assert cold["complete_cells"] == []
    assert cold["held_observed_n_if_nonpositive"] == 4
    assert cold["zero_means"] == "NO_ZERO_INFERENCE_FROM_NONPOSITIVE_PRODUCER_STATE"


def test_cold_saved_parquet_native_i03_replays_without_reopening_source(tmp_path, monkeypatch):
    pytest.importorskip("pyarrow")
    from rawlsing_next.tests.test_pyat1009_ff01_cold_direct_estate import _actual_cold_ff01
    old_ff, actual, query, receipt = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=0, tag="S04-COLD-PARQUET-FIRST",
        saved_name="original-persisted",
    )
    s04 = receive_s04_i03_research(query=query, execution=actual)
    bundle = freeze_s04_i03_sourcefree(query=query, execution=actual, knowledge=s04)
    pin = S04ExternalRootPin(query.ref, actual.facts[0].ref, actual.release_refs[0])
    path = write_s04_sourcefree_private(tmp_path / "private-replay", bundle)
    del actual, query, s04
    # Rehydrate the exact original I03 preimage after these in-memory source
    # references are dropped; this step MUST NOT execute I03 or open Parquet.
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
    from rawlsing_next.pre553_c11_repository import C11Repository
    def no_new_source(*args, **kwargs):
        raise AssertionError("cold S04 must not construct C11 / reexecute source")
    with monkeypatch.context() as guard:
        guard.setattr(C11Repository, "__init__", no_new_source)
        restored = receive_ff01_from_pinned_cold(
            bundle=read_s04_sourcefree_private(path), external_root=pin,
            conditioner_index=0, producer_permission_ceiling=PERMISSIONS,
        )
    assert restored.ref == old_ff.ref


def test_fresh_python_process_rehydrates_without_parent_i03_objects(tmp_path):
    bundle, pin, _, _, _ = _ready()
    file = write_s04_sourcefree_private(tmp_path / "fresh-process", bundle)
    code = (
        "import sys;"
        "from rawlsing_next.pre553_s04_cold_custody import *;"
        "from rawlsing_next.pre553_empirical_objects import ExactRef;"
        "pin=S04ExternalRootPin("
        "ExactRef('EmpiricalQuerySpec@1.0.0',sys.argv[2],sys.argv[3]),"
        "ExactRef('EmpiricalFact@1.0.0',sys.argv[4],sys.argv[5]),"
        "ExactRef(sys.argv[6],sys.argv[7],sys.argv[8]));"
        "ff=receive_ff01_from_pinned_cold("
        "bundle=read_s04_sourcefree_private(sys.argv[1]),external_root=pin,"
        "conditioner_index=0,producer_permission_ceiling=('FF01_DESCRIPTIVE_SOURCEFREE',));"
        "assert ff.semantic_projection()['joint_arity']==3;"
        "print(ff.ref.content_hash)"
    )
    result = run(
        [executable, "-c", code, str(file),
         pin.query_ref.object_id, pin.query_ref.content_hash,
         pin.fact_ref.object_id, pin.fact_ref.content_hash,
         pin.release_ref.kind, pin.release_ref.object_id, pin.release_ref.content_hash],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip()) == 64
