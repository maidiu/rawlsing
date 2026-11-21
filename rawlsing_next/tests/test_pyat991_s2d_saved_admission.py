"""S2-D saved C11 admission tests.

These tests exercise the accepted S2-C physical estate through the existing
native I03/I05 owners.  They deliberately do not fake the five shared-owner
readers whose source files are READONLY pending acknowledgement.
"""
from __future__ import annotations

from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_discovery_exact as discovery_tests
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority, ExactRef
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission,
    SavedC11AdmissionError,
    SavedWorkloadOwnerHandoffRequired,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_absent,
    execute_saved_batch,
    execute_saved_completed,
    execute_saved_i03,
    execute_saved_i05,
    execute_saved_normal,
    execute_saved_partial,
    saved_reader_capabilities,
)


def _source_with_candidate(monkeypatch, tag, rows):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repository):
        holder["candidate"] = candidate
        return original(candidate, repository)

    with monkeypatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(tag, rows)
    assert "candidate" in holder
    return source, holder["candidate"]


def _admission(root, receipt, source, catalog, *, allow=True):
    return SavedC11Admission.open(
        root=root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=source["release_ref"],
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: allow,
    )


def _i03_parts(source, tag):
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth, tag=f"{tag}-pred")
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )
    return qauth, predicate, query, catalog


def _i05_parts(source, tag):
    qauth = native._query_authority(tag)
    dauth = discovery_tests._d_auth(f"{tag}-discovery")
    all_p = native._branch_predicate(source, qauth, tag=f"{tag}-all")
    x1 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 1),
        tag=f"{tag}-x1",
    )
    yq = native._query(source, qauth, all_p, ("Y",), tag=f"{tag}-y")
    grammar = discovery_tests._grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[
            discovery_tests._atom("ALL", all_p, "BRANCH"),
            discovery_tests._atom("X1", x1, "RESPONSE"),
        ],
        templates=[discovery_tests._qt("Y", yq)],
        rules=[discovery_tests._rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL",
            query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    base = discovery_tests._discovery_authority(source, grammar, dauth)
    authority = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base.producer_replay_locator_or_reference_root
        ),
        **{
            **dict(base.semantic_fields),
            "validation_rules": {
                "rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},),
            },
        },
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(all_p, x1),
        queries=(yq,),
        discovery_authorities=(authority,),
    )
    return qauth, dauth, all_p, x1, yq, authority, catalog


def _fact_sig(result):
    return tuple(fact.semantic_projection() for fact in result.facts)


def test_cold_saved_i03_matches_native_oracle_without_c11_or_source(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I03-COLD",
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, catalog = _i03_parts(source, "S2D-I03-COLD")
    oracle = native._run(source, qauth, predicate, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "cold-i03",
    )
    admission = _admission(root, receipt, source, catalog)
    assert admission.binding_receipt().source_opens == 0
    assert admission.binding_receipt().full_c11_repository_builds == 0

    import pyarrow.parquet as pq
    def forbidden(*_args, **_kwargs):
        raise AssertionError("hidden C11 repository or whole Parquet fallback")

    with monkeypatch.context() as guard:
        guard.setattr(C11Repository, "__init__", forbidden)
        guard.setattr(pq, "read_table", forbidden)
        observed = execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=predicate.ref,
        )
    assert tuple(f.ref for f in observed.facts) == tuple(f.ref for f in oracle.facts)
    assert _fact_sig(observed) == _fact_sig(oracle)
    assert observed.release_refs == oracle.release_refs
    assert not list(root.glob(".s2c-native-i03-*"))


def test_fresh_process_saved_i03_after_producer_source_is_gone(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I03-FRESH",
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, catalog = _i03_parts(source, "S2D-I03-FRESH")
    oracle = native._run(source, qauth, predicate, query)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "fresh-i03",
    )
    capsule = tmp_path / "held-saved-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "release": source["release_ref"].as_dict(),
        "authorities": [obj.as_dict() for obj in catalog.authorities],
        "predicate": predicate.as_dict(),
        "query": query.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child = """
import json
import sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
capsule = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
query = materialize_public_object(capsule["query"])
predicate = materialize_public_object(capsule["predicate"])
catalog = RuntimeObjectCatalog(
    authorities=tuple(materialize_public_object(v) for v in capsule["authorities"]),
    predicates=(predicate,), queries=(query,), discovery_authorities=(),
)
admission = SavedC11Admission.open(
    root=capsule["root"], exact_path=capsule["exact_path"],
    independently_held_manifest_sha256=capsule["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**capsule["i02"]),
    release_ref=exact_ref(capsule["release"]), runtime_catalog=catalog,
    current_authorizer=lambda _roots: True,
)
result = execute_saved_i03(admission, query_ref=query.ref, predicate_ref=predicate.ref)
print(json.dumps({
    "fact_refs": [f.ref.as_dict() for f in result.facts],
    "fact_projections": [f.semantic_projection() for f in result.facts],
    "release_refs": [r.as_dict() for r in result.release_refs],
}, sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-c", child, str(capsule)],
        check=False, capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["fact_refs"] == [f.ref.as_dict() for f in oracle.facts]
    assert observed["release_refs"] == [r.as_dict() for r in oracle.release_refs]
    assert observed["fact_projections"] == [
        json.loads(json.dumps(f.semantic_projection(), sort_keys=True))
        for f in oracle.facts
    ]


def test_cold_saved_i05_matches_native_frontier_without_c11_or_source(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I05-COLD",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qauth, dauth, all_p, x1, yq, authority, catalog = _i05_parts(
        source, "S2D-I05-COLD",
    )
    oracle = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=native._registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1),
        query_template_catalog=(yq,),
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "cold-i05",
    )
    admission = _admission(root, receipt, source, catalog)

    import pyarrow.parquet as pq
    def forbidden(*_args, **_kwargs):
        raise AssertionError("hidden C11 repository or whole Parquet fallback")

    with monkeypatch.context() as guard:
        guard.setattr(C11Repository, "__init__", forbidden)
        guard.setattr(pq, "read_table", forbidden)
        observed = execute_saved_i05(
            admission, discovery_authority_ref=authority.ref,
        )
    assert observed.candidate_count == oracle.candidate_count
    assert observed.covered_candidate_count == oracle.covered_candidate_count
    assert tuple(r.ref for r in observed.receipts) == tuple(r.ref for r in oracle.receipts)
    assert tuple(f.ref for f in observed.empirical_facts) == tuple(
        f.ref for f in oracle.empirical_facts
    )
    assert observed.valid_empty == oracle.valid_empty == False
    assert observed.covered_candidate_count == 1


def test_fresh_process_saved_i05_after_producer_source_is_gone(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I05-FRESH",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qauth, dauth, all_p, x1, yq, authority, catalog = _i05_parts(
        source, "S2D-I05-FRESH",
    )
    oracle = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=native._registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1),
        query_template_catalog=(yq,),
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "fresh-i05",
    )
    capsule = tmp_path / "held-saved-i05-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "release": source["release_ref"].as_dict(),
        "authorities": [obj.as_dict() for obj in catalog.authorities],
        "predicates": [obj.as_dict() for obj in catalog.predicates],
        "queries": [obj.as_dict() for obj in catalog.queries],
        "discovery_authority": authority.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child = """
import json
import sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i05
capsule = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
catalog = RuntimeObjectCatalog(
    authorities=tuple(materialize_public_object(v) for v in capsule["authorities"]),
    predicates=tuple(materialize_public_object(v) for v in capsule["predicates"]),
    queries=tuple(materialize_public_object(v) for v in capsule["queries"]),
    discovery_authorities=(materialize_public_object(capsule["discovery_authority"]),),
)
admission = SavedC11Admission.open(
    root=capsule["root"], exact_path=capsule["exact_path"],
    independently_held_manifest_sha256=capsule["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**capsule["i02"]),
    release_ref=exact_ref(capsule["release"]), runtime_catalog=catalog,
    current_authorizer=lambda _roots: True,
)
result = execute_saved_i05(
    admission,
    discovery_authority_ref=catalog.discovery_authorities[0].ref,
)
print(json.dumps({
    "candidate_count": result.candidate_count,
    "covered_candidate_count": result.covered_candidate_count,
    "fact_refs": [f.ref.as_dict() for f in result.empirical_facts],
    "receipt_refs": [r.ref.as_dict() for r in result.receipts],
}, sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-c", child, str(capsule)],
        check=False, capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["candidate_count"] == oracle.candidate_count
    assert observed["covered_candidate_count"] == oracle.covered_candidate_count
    assert observed["fact_refs"] == [f.ref.as_dict() for f in oracle.empirical_facts]
    assert observed["receipt_refs"] == [r.ref.as_dict() for r in oracle.receipts]


def test_changed_cold_estate_changes_native_i03_and_restore_is_exact(
    tmp_path, monkeypatch,
):
    tag = "S2D-I03-CHANGE"
    base_source, base_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    changed_source, changed_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 0}}],
    )
    qauth, predicate, query, catalog = _i03_parts(base_source, tag)
    base_oracle = native._run(base_source, qauth, predicate, query)
    old_manifest = changed_candidate.source_release_manifest
    digest = hashlib.sha256((tag + ":changed-source-bytes").encode()).hexdigest()
    changed_manifest = replace(
        old_manifest,
        release_id=old_manifest.release_id + "-CHANGED",
        source_artifact_content_hash=digest,
        source_snapshot_retention_ref=ExactRef(
            old_manifest.source_snapshot_retention_ref.kind,
            old_manifest.source_snapshot_retention_ref.object_id + "-CHANGED",
            digest,
        ),
    )
    altered = replace(
        changed_candidate, source_release_manifest=changed_manifest,
        candidate_replay_manifest=None,
    )
    replay = changed_candidate.candidate_replay_manifest
    altered = replace(altered, candidate_replay_manifest=build_candidate_replay_manifest(
        altered,
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
        replay_protocol_version=replay.replay_protocol_version,
    ))
    changed_repo = C11Repository()
    admitted = ingest_c11_source_release(altered, changed_repo)
    assert admitted.accepted, admitted.errors
    assert admitted.release_ref != base_source["release_ref"]
    changed_source = {
        **changed_source, "repo": changed_repo,
        "release_ref": admitted.release_ref,
    }
    changed_oracle = native._run(changed_source, qauth, predicate, query)
    base_root, base_receipt = s2c._cold(
        tmp_path, base_candidate, base_source["universe"].ref, "base-i03",
    )
    changed_root, changed_receipt = s2c._cold(
        tmp_path, altered, base_source["universe"].ref, "changed-i03",
    )
    base_admission = _admission(base_root, base_receipt, base_source, catalog)
    changed_admission = _admission(
        changed_root, changed_receipt, changed_source, catalog,
    )
    first = execute_saved_i03(
        base_admission, query_ref=query.ref, predicate_ref=predicate.ref,
    )
    changed = execute_saved_i03(
        changed_admission, query_ref=query.ref, predicate_ref=predicate.ref,
    )
    restored = execute_saved_i03(
        base_admission, query_ref=query.ref, predicate_ref=predicate.ref,
    )
    assert first.facts[0].typed_state == "SUPPORTED"
    assert changed.facts[0].ref != first.facts[0].ref
    assert tuple(f.ref for f in first.facts) == tuple(f.ref for f in base_oracle.facts)
    assert tuple(f.ref for f in changed.facts) == tuple(
        f.ref for f in changed_oracle.facts
    )
    assert tuple(f.ref for f in restored.facts) == tuple(f.ref for f in first.facts)
    assert _fact_sig(restored) == _fact_sig(first)


def test_revoked_current_wrong_pin_and_missing_body_refuse(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I03-NEG",
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, catalog = _i03_parts(source, "S2D-I03-NEG")
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "neg-i03",
    )
    allow = {"value": True}
    admission = SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=source["release_ref"], runtime_catalog=catalog,
        current_authorizer=lambda _roots: allow["value"],
    )
    assert execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref,
    ).facts[0].typed_state == "SUPPORTED"
    allow["value"] = False
    with pytest.raises(Exception, match="current source/operation authority refused"):
        execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=predicate.ref,
        )
    # Wrong independently held manifest cannot be repaired by a locally
    # rehashed manifest or by the admitted object's own evidence.
    with pytest.raises(Exception, match="manifest differs from independently held root"):
        SavedC11Admission.open(
            root=root, exact_path=receipt.path,
            independently_held_manifest_sha256="0" * 64,
            independently_held_i02=receipt.i02,
            release_ref=source["release_ref"], runtime_catalog=catalog,
            current_authorizer=lambda _roots: True,
        )
    # Missing body is a refusal, never EMPTY/UNKNOWN.
    body = Path(receipt.path) / "RespondentEvent.parquet"
    backup = body.with_suffix(".parquet.bak")
    body.rename(backup)
    try:
        with pytest.raises(Exception, match="committed estate member missing"):
            SavedC11Admission.open(
                root=root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                release_ref=source["release_ref"], runtime_catalog=catalog,
                current_authorizer=lambda _roots: True,
            )
    finally:
        backup.rename(body)


def test_batch_guard_actually_refuses_until_owner_ack(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-I03-BATCH-HOLD",
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    _, predicate, query, catalog = _i03_parts(source, "S2D-I03-BATCH-HOLD")
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "batch-hold",
    )
    admission = _admission(root, receipt, source, catalog)
    unit = BatchUnitSpec(
        "QUERY", query.ref, (source["release_ref"],), (predicate.ref,),
    )
    with pytest.raises(
        BatchIntegrityError,
        match="repository must be accepted I02 C11Repository",
    ):
        BatchExecutionRunner(
            manifest=BatchManifest((unit,)), repository=admission,
        )


def test_shared_owner_readers_are_typed_holds_not_fake_seven_pass():
    capabilities = saved_reader_capabilities()
    assert capabilities["implemented_here"] == ["I03", "I05"]
    for func in (
        execute_saved_batch,
        execute_saved_normal,
        execute_saved_completed,
        execute_saved_partial,
        execute_saved_absent,
    ):
        with pytest.raises(SavedWorkloadOwnerHandoffRequired) as exc:
            func()
        assert exc.value.owner
        assert exc.value.path
        assert exc.value.function
        assert exc.value.minimum_edit
    assert set(capabilities["blocked_owner_ack"]) == {
        "Batch", "NORMAL", "COMPLETED", "PARTIAL", "ABSENT",
    }
