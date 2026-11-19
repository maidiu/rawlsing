"""Cold persisted SOURCEFREE S2-C -> real I03 -> generic FF01 joint first reader.

Not a native original survey, statistical estimator, FF02 admission, or G5.
The fixture intentionally uses the accepted 13-family direct-estate writer.
"""
from dataclasses import replace
from hashlib import sha256
from itertools import product
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest, ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.field_forge_generic_empirical_ingress import (
    receive_ff01_observed_joint, replay_ff01_observed_joint,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_direct_estate_i03 import _cold, _executor


def _source_and_original_candidate(monkeypatch, tag: str, parity: int):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original(candidate, repo)

    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
        for x, y in product((0, 1), repeat=2)
    ]
    with monkeypatch.context() as scope:
        scope.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(tag, rows, question_namespace="FF01-NATIVE-SHARED")
    assert holder.get("candidate") is not None
    candidate = holder["candidate"]
    if parity == 1:
        # A changed response vector is new source bytes. The original test
        # fixture hashes only its *tag*, so explicitly version the physical
        # artifact/retention/replay instead of laundering changed bytes under
        # an unchanged historical source identity.
        old = candidate.source_release_manifest
        digest = sha256((tag + ":parity1-altered-source-bytes").encode()).hexdigest()
        changed_manifest = replace(
            old,
            release_id=old.release_id + "-ALTERED",
            source_artifact_content_hash=digest,
            source_snapshot_retention_ref=ExactRef(
                old.source_snapshot_retention_ref.kind,
                old.source_snapshot_retention_ref.object_id + "-ALTERED",
                digest,
            ),
        )
        altered = replace(
            candidate, source_release_manifest=changed_manifest,
            candidate_replay_manifest=None,
        )
        replay = candidate.candidate_replay_manifest
        altered = replace(altered, candidate_replay_manifest=build_candidate_replay_manifest(
            altered,
            replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
            replay_protocol_version=replay.replay_protocol_version,
        ))
        updated_repo = C11Repository()
        admitted = ingest_c11_source_release(altered, updated_repo)
        assert admitted.accepted, admitted.errors
        source = {**source, "repo": updated_repo, "release_ref": admitted.release_ref}
        candidate = altered
    return source, candidate


def _actual_cold_ff01(tmp_path, monkeypatch, *, parity, tag, saved_name):
    source, candidate = _source_and_original_candidate(monkeypatch, tag, parity)
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("X", "Y", "Z"), tag=tag)
    expected = native._run(source, qauth, predicate, query)
    root, receipt = _cold(tmp_path, candidate, source["universe"].ref, saved_name)
    executor = _executor(root, receipt, source, qauth, predicate, query)
    assert Path(receipt.path).is_dir()
    assert receipt.reconstructed_v1_release_ref == source["release_ref"]

    import pyarrow.parquet as pq

    def denied_full_materialization(*_args, **_kwargs):
        raise AssertionError("FF01 first read must not rebuild full C11 or read entire parquet table")

    with monkeypatch.context() as guard:
        guard.setattr(C11Repository, "__init__", denied_full_materialization)
        guard.setattr(pq, "read_table", denied_full_materialization)
        observed = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        consumed = receive_ff01_observed_joint(
            execution=observed, query=query, conditioner_index=0,
            producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
        )

    assert tuple(f.ref for f in observed.facts) == tuple(f.ref for f in expected.facts)
    assert observed.query_ref == expected.query_ref
    assert consumed.semantic_projection()["producer_fact_ref"] == observed.facts[0].ref.as_dict()
    assert consumed.semantic_projection()["joint_arity"] == 3
    return consumed, observed, query, receipt


def test_true_cold_saved_i03_to_ff01_triplet_changed_and_restored(tmp_path, monkeypatch):
    tag = "FF01-COLD-SAVED-TRIPLE"
    first, first_i03, query, receipt = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=0, tag=tag, saved_name="source-a",
    )
    changed, changed_i03, changed_query, changed_receipt = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=1, tag=tag, saved_name="source-b",
    )
    assert first.ref != changed.ref
    assert first_i03.facts[0].ref != changed_i03.facts[0].ref
    assert first.semantic_projection()["complete_cells"] != changed.semantic_projection()["complete_cells"]
    restored, restored_i03, restored_query, restored_receipt = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=0, tag=tag, saved_name="source-restored",
    )
    assert restored.ref == first.ref
    assert restored_i03.facts[0].ref == first_i03.facts[0].ref
    assert restored.semantic_projection() == first.semantic_projection()
    assert replay_ff01_observed_joint(
        first.ref, execution=restored_i03, query=restored_query,
        conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    ).ref == first.ref
    assert receipt.manifest_sha256 == restored_receipt.manifest_sha256
    assert changed_receipt.manifest_sha256 != receipt.manifest_sha256


def test_cold_saved_ff01_does_not_claim_population_or_ff02_science(tmp_path, monkeypatch):
    received, _, _, _ = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=0, tag="FF01-NO-STRUCTURE", saved_name="no-structure",
    )
    material = received.semantic_projection()
    assert "SAMPLE_ONLY" in material["claim_grade"]
    assert "PREDICTOR_IMPORTANCE_ESTIMATOR_NOT_ISSUED" in material["not_proven"]
    assert "FF02_OR_MATERIAL_POWER_NOT_ISSUED" in material["not_proven"]
    assert "PER_CELL_RESPONDENT_MEMBERSHIP_NOT_PRESENT_IN_AGGREGATE_FACT" in material["not_proven"]
