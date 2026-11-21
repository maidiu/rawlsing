"""Cut1 prepared saved Batch: exact wrapper/context and legacy parity.

Return-local sourcefree TEST_ONLY fixture through the existing prepared-session
fixture. No source, writer, evaluator, issuer, or Batch-machine change.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchIntegrityError, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedC11AdmissionError,
)
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _fact_signature(result):
    fact = result.facts[0]
    return {
        "fact_ref": fact.ref.as_dict(),
        "projection_hash": semantic_hash(fact.semantic_projection()),
        "denominator": fact.raw_denominator_support,
        "cell_count": len(
            fact.target_topology.get("complete_cell_semantic_projection", ())
        ),
        "release_refs": tuple(ref.as_dict() for ref in result.release_refs),
    }


def _manifest(queries, predicate, admission):
    units = tuple(
        BatchUnitSpec(
            "QUERY", query.ref, (admission.release_ref,),
        )
        for query in queries.values()
    )
    return BatchManifest(units), {
        query.ref.key: predicate.ref for query in queries.values()
    }


def _prepared(tmp_path, monkeypatch, tag, grant=lambda _roots: True):
    source, qa, predicate, other, queries, admission = _fixture(
        monkeypatch, tmp_path / tag, tag, grant=grant,
    )
    assert type(admission) is PreparedSavedC11Admission
    return source, qa, predicate, other, queries, admission


def _baselines(admission, queries, predicate):
    return {
        name: admission.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref)
        for name, query in queries.items()
    }


def test_prepared_direct_wrapper_matches_baseline(tmp_path, monkeypatch):
    source, qa, predicate, _other, queries, admission = _prepared(
        tmp_path, monkeypatch, "CUT1-DIRECT")
    baseline = _baselines(admission, queries, predicate)
    observed = execute_saved_i03(
        admission,
        query_ref=queries["selected"].ref,
        predicate_ref=predicate.ref,
    )
    assert _fact_signature(observed) == _fact_signature(
        baseline["selected"])
    assert observed.facts[0].typed_state == "SUPPORTED"
    assert observed.facts[0].raw_denominator_support > 0


def test_prepared_batch_four_operations_one_build_exact_full_parity(
    tmp_path, monkeypatch,
):
    source, qa, predicate, _other, queries, admission = _prepared(
        tmp_path, monkeypatch, "CUT1-BATCH")
    unit_queries = (queries["selected"], queries["f2"],
                    queries["f4"], queries["raw"])
    assert len({query.ref.key for query in unit_queries}) == 4
    baseline = _baselines(admission, queries, predicate)
    assert _fact_signature(baseline["f2"])["denominator"] > 0
    assert _fact_signature(baseline["f4"])["denominator"] > 0
    assert _fact_signature(baseline["f4"])["cell_count"] == 8
    assert _fact_signature(baseline["selected"])["denominator"] > 0
    assert _fact_signature(baseline["raw"])["denominator"] > 0

    builds = []
    original_build = DirectEstateI03Session._build

    def counted(self):
        builds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted)
    manifest, predicate_map = _manifest(
        {query.ref.key: query for query in unit_queries}, predicate, admission)
    runner = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicate_map,
    )
    assert len(builds) == 1
    assert len(runner.receipts) == 4
    assert {receipt.state for receipt in runner.receipts} == {"COMPLETED"}
    receipt_by_unit = {r.unit_ref.key: r for r in runner.receipts}
    for name, query in zip(("selected", "f2", "f4", "raw"), unit_queries):
        receipt = receipt_by_unit[
            next(unit.unit_ref.key for unit in manifest.units
                 if unit.job_ref == query.ref)
        ]
        expected_ref = baseline[name].facts[0].ref
        assert receipt.result_refs == (expected_ref,)
        assert admission.replay_ref in receipt.provenance_refs
    assert all(
        _fact_signature(baseline[name]) == _fact_signature(
            admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref))
        for name, query in zip(("selected", "f2", "f4", "raw"), unit_queries)
    )


def test_prepared_batch_legacy_saved_path_and_cleanup(tmp_path, monkeypatch):
    source, qa, predicate, _other, queries, admission = _prepared(
        tmp_path, monkeypatch, "CUT1-LEGACY")
    manifest, predicate_map = _manifest(queries, predicate, admission)

    builds = []
    original_build = DirectEstateI03Session._build

    def counted(self):
        builds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted)
    prepared = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicate_map,
    )
    assert len(builds) == 1
    assert len(prepared.receipts) == 4

    # The plain base admission must retain its existing per-operation path and
    # produce the same full native fact/ref/replay projection.
    root = Path(admission.estate_path).parents[1]
    plain = SavedC11Admission.open(
        root=root,
        exact_path=admission.estate_path,
        independently_held_manifest_sha256=admission.manifest_sha256,
        independently_held_i02=admission.i02,
        release_ref=admission.release_ref,
        runtime_catalog=admission._runtime_catalog,
        current_authorizer=lambda _roots: True,
    )
    baseline = _baselines(plain, queries, predicate)
    legacy = execute_saved_batch(
        plain, manifest=manifest, predicate_ref_by_query=predicate_map,
    )
    assert len(legacy.receipts) == 4
    for name, query in queries.items():
        receipt = next(
            r for r in legacy.receipts
            if r.result_refs == (baseline[name].facts[0].ref,)
        )
        assert receipt.state == "COMPLETED"
        actual = plain.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref)
        assert _fact_signature(baseline[name]) == _fact_signature(actual)
    # No prepared context survives after the call: a fresh prepared call
    # builds exactly one new index and still matches the baseline.
    builds.clear()
    again = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicate_map)
    assert len(builds) == 1
    assert len(again.receipts) == 4


def test_prepared_batch_refuses_foreign_classes_release_and_revocation(
    tmp_path, monkeypatch,
):
    source, qa, predicate, _other, queries, admission = _prepared(
        tmp_path, monkeypatch, "CUT1-REFUSE")
    manifest, predicate_map = _manifest(queries, predicate, admission)

    with pytest.raises(SavedC11AdmissionError, match="PreparedSavedC11Admission"):
        execute_saved_i03(
            object(),
            query_ref=queries["selected"].ref,
            predicate_ref=predicate.ref,
        )
    with pytest.raises(BatchIntegrityError):
        BatchExecutionRunner(
            manifest=manifest, repository=object(), saved_mode=True)

    wrong_unit = BatchUnitSpec(
        "QUERY", queries["selected"].ref,
        (ExactRef("C11LogicalRelease", "wrong-release", "0" * 64),),
    )
    wrong_manifest = BatchManifest((wrong_unit,))
    with pytest.raises(SavedC11AdmissionError):
        BatchExecutionRunner(
            manifest=wrong_manifest, repository=admission, saved_mode=True)

    # A changed independently held manifest binding must refuse before any
    # prepared context or positive Batch work.
    root = Path(admission.estate_path).parents[1]
    with pytest.raises((DirectEstateError, SavedC11AdmissionError)):
        PreparedSavedC11Admission.open(
            root=root,
            exact_path=admission.estate_path,
            independently_held_manifest_sha256="0" * 64,
            independently_held_i02=admission.i02,
            release_ref=admission.release_ref,
            runtime_catalog=admission._runtime_catalog,
            current_authorizer=lambda _roots: True,
        )

    grant = {"now": True}
    source2, qa2, predicate2, _other2, queries2, admission2 = _prepared(
        tmp_path, monkeypatch, "CUT1-REVOKE", grant=lambda _roots: grant["now"])
    manifest2, map2 = _manifest(queries2, predicate2, admission2)
    grant["now"] = False
    with pytest.raises(DirectEstateError):
        execute_saved_batch(
            admission2, manifest=manifest2, predicate_ref_by_query=map2)
    grant["now"] = True
    restored = execute_saved_batch(
        admission2, manifest=manifest2, predicate_ref_by_query=map2)
    assert len(restored.receipts) == 4
    assert {r.state for r in restored.receipts} == {"COMPLETED"}


def test_prepared_batch_revoked_mid_batch_closes_and_restores(
    tmp_path, monkeypatch,
):
    state = {"n": 0, "armed": False}

    def grant(_roots):
        if not state["armed"]:
            return True
        state["n"] += 1
        return state["n"] <= 5

    source, qa, predicate, _other, queries, admission = _prepared(
        tmp_path, monkeypatch, "CUT1-MID-REVOKE", grant=grant)
    state.update(n=0, armed=True)
    manifest, predicate_map = _manifest(queries, predicate, admission)
    with pytest.raises(DirectEstateError):
        execute_saved_batch(
            admission, manifest=manifest, predicate_ref_by_query=predicate_map)
    # The failed context closed; an unarmed CURRENT permits exact restoration.
    state.update(n=0, armed=False)
    restored = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicate_map)
    assert len(restored.receipts) == 4
    assert {receipt.state for receipt in restored.receipts} == {"COMPLETED"}
