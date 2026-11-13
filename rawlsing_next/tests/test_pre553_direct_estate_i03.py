"""Cold authenticated S2-C sourcefree estate -> actual native I03 first reader.

These are executable first-consumer claims, NOT original35/source/rights or
independent G5 acceptance. No fake C11 seal and no permanent event-body SQLite.
"""
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_direct_i02_sourcefree import direct_sections_from_candidate
from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest, ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError, CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate, write_direct_estate,
)
import rawlsing_next.tests.test_pre553_empirical_query as native


def _source_with_candidate(monkeypatch, tag, y2):
    """Capture native test owner's genuine C11 candidate, not a mock schema."""
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original(candidate, repo)

    with monkeypatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(
            tag,
            [{"id": "R1", "responses": {"Y": 0}},
             {"id": "R2", "responses": {"Y": y2}}],
        )
    return source, holder["candidate"]


def _cold(tmp_path, candidate, universe_ref, tag):
    replay = candidate.candidate_replay_manifest
    assert replay is not None
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    root = tmp_path / tag
    root.mkdir(mode=0o700)
    receipt = write_direct_estate(
        direct, universe_ref, root, chunk_rows=2,
    )
    return root, receipt


def _executor(root, receipt, source, qauth, predicate, query, grant=lambda _: True):
    estate = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=grant,
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )
    return CarrierNeutralResearchExecutor(
        repository=estate,
        release_refs=(source["release_ref"],),
        runtime_catalog=catalog,
    )


def _fact_signature(result):
    return tuple(fact.semantic_projection() for fact in result.facts)


def test_original_native_carrier_execute_i03_from_cold_sourcefree_parquet(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(monkeypatch, "S2C-NATIVE-I03", 1)
    qauth = native._query_authority("S2C-NATIVE-I03")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag="S2C-NATIVE-I03")

    oracle = native._run(source, qauth, predicate, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    root, receipt = _cold(tmp_path, candidate, source["universe"].ref, "private-native")
    assert receipt.reconstructed_v1_release_ref == source["release_ref"]
    assert receipt.i02.release != source["release_ref"].key
    executor = _executor(root, receipt, source, qauth, predicate, query)
    # Native first consumer MUST NOT silently fall back to full C11 rebuild
    # or whole-Parquet table materialization after source is unavailable.
    import pyarrow.parquet as pq
    def forbidden(*_args, **_kwargs):
        raise AssertionError("forbidden full-graph repository or pq.read_table fallback")
    with monkeypatch.context() as guard:
        guard.setattr(C11Repository, "__init__", forbidden)
        guard.setattr(pq, "read_table", forbidden)
        observed = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert observed.query_ref == oracle.query_ref
    assert observed.release_refs == oracle.release_refs
    assert _fact_signature(observed) == _fact_signature(oracle)
    assert tuple(f.ref for f in observed.facts) == tuple(f.ref for f in oracle.facts)
    assert not list(Path(receipt.path).glob("*.sqlite"))
    assert not list(root.glob(".s2c-native-i03-*"))
    assert executor.binding_receipt()["repository_snapshot_identity"]["i02"]["logical"] == receipt.i02.logical


def test_cold_i03_denied_authority_refuses_before_native_first_consumer(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(monkeypatch, "S2C-NATIVE-DENIED", 1)
    qauth = native._query_authority("S2C-NATIVE-DENIED")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag="S2C-NATIVE-DENIED")
    root, receipt = _cold(tmp_path, candidate, source["universe"].ref, "private-denied")
    allow = {"value": True}
    executor = _executor(root, receipt, source, qauth, predicate, query,
                         lambda _: allow["value"])
    allow["value"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert not list(root.glob(".s2c-native-i03-*"))


def test_cold_i03_rejects_grouped_cache_and_i05_outside_s2c_scope(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(monkeypatch, "S2C-NATIVE-SCOPE", 1)
    qauth = native._query_authority("S2C-NATIVE-SCOPE")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag="S2C-NATIVE-SCOPE")
    root, receipt = _cold(tmp_path, candidate, source["universe"].ref, "private-scope")
    executor = _executor(root, receipt, source, qauth, predicate, query)
    with pytest.raises(CarrierExecutionBindingError, match="grouped saved I03"):
        executor.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref,
            group_scope=executor.grouped_i03_scope(),
        )
    with pytest.raises(CarrierExecutionBindingError, match="I05/Batch saved wiring"):
        executor.execute_i05(discovery_authority_ref=source["universe"].ref)


def test_cold_i03_new_source_content_changes_fact_and_old_root_restores(
    tmp_path, monkeypatch,
):
    tag = "S2C-NATIVE-CHANGE"
    source, initial = _source_with_candidate(monkeypatch, tag, 1)
    changed_source, changed = _source_with_candidate(monkeypatch, tag, 0)
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    oracle = native._run(source, qauth, predicate, query)
    original_root, original_receipt = _cold(
        tmp_path, initial, source["universe"].ref, "private-original",
    )
    first = _executor(
        original_root, original_receipt, source, qauth, predicate, query
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert _fact_signature(first) == _fact_signature(oracle)

    old_manifest = changed.source_release_manifest
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
        changed, source_release_manifest=changed_manifest,
        candidate_replay_manifest=None,
    )
    replay = changed.candidate_replay_manifest
    altered = replace(altered, candidate_replay_manifest=build_candidate_replay_manifest(
        altered,
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
        replay_protocol_version=replay.replay_protocol_version,
    ))
    changed_repo = C11Repository()
    admitted = ingest_c11_source_release(altered, changed_repo)
    assert admitted.accepted, admitted.errors
    assert admitted.release_ref != source["release_ref"]
    changed_source = {**changed_source, "repo": changed_repo,
                      "release_ref": admitted.release_ref}
    changed_oracle = native._run(changed_source, qauth, predicate, query)
    new_root, new_receipt = _cold(
        tmp_path, altered, source["universe"].ref, "private-changed",
    )
    changed_fact = _executor(
        new_root, new_receipt, changed_source, qauth, predicate, query
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert _fact_signature(changed_fact) == _fact_signature(changed_oracle)
    assert changed_fact.facts[0].raw_denominator_support == 2
    assert changed_fact.facts[0].ref != first.facts[0].ref

    restored = _executor(
        original_root, original_receipt, source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert restored.facts[0].ref == first.facts[0].ref
    assert _fact_signature(restored) == _fact_signature(first)


def test_fresh_interpreter_cold_native_i03_without_original_c11_or_source(
    tmp_path, monkeypatch,
):
    """G2: isolated new Python interpreter, only exact held physical/source
    roots and exact serialized query/authority catalog are transferable.
    The old C11 repository/candidate/first-process fact never reaches child.
    """
    source, candidate = _source_with_candidate(monkeypatch, "S2C-NATIVE-COLD-PROC", 1)
    qauth = native._query_authority("S2C-NATIVE-COLD-PROC")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag="S2C-NATIVE-COLD-PROC")
    oracle = native._run(source, qauth, predicate, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    root, receipt = _cold(
        tmp_path, candidate, source["universe"].ref, "private-fresh-process",
    )
    capsule = tmp_path / "held-outside-estate.json"
    capsule.write_text(json.dumps({
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "release": source["release_ref"].as_dict(),
        "authorities": [obj.as_dict() for obj in (*source["authorities"], qauth)],
        "predicate": predicate.as_dict(),
        "query": query.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child = """
import json
import sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, RuntimeObjectCatalog, materialize_public_object,
)
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_empirical_objects import exact_ref
capsule = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
estate = VerifiedDirectEstate(
    capsule["root"], exact_path=capsule["exact_path"],
    independently_held_manifest_sha256=capsule["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**capsule["i02"]),
    current_authorizer=lambda _r: True,  # SOURCEFREE TEST_ONLY, not production issuer
)
query = materialize_public_object(capsule["query"])
predicate = materialize_public_object(capsule["predicate"])
catalog = RuntimeObjectCatalog(
    authorities=tuple(materialize_public_object(v) for v in capsule["authorities"]),
    queries=(query,), predicates=(predicate,), discovery_authorities=(),
)
executor = CarrierNeutralResearchExecutor(
    repository=estate, release_refs=(exact_ref(capsule["release"]),),
    runtime_catalog=catalog,
)
result = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
print(json.dumps({"fact_refs": [f.ref.as_dict() for f in result.facts],
                  "release_refs": [r.as_dict() for r in result.release_refs],
                  "fact_projections": [f.semantic_projection() for f in result.facts]},
                 sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-c", child, str(capsule)],
        check=False, capture_output=True, text=True,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["fact_refs"] == [fact.ref.as_dict() for fact in oracle.facts]
    assert result["release_refs"] == [ref.as_dict() for ref in oracle.release_refs]
    assert result["fact_projections"] == [
        json.loads(json.dumps(fact.semantic_projection(), sort_keys=True))
        for fact in oracle.facts
    ]
    assert not list(root.glob(".s2c-native-i03-*"))
