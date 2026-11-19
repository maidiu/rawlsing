"""Sourcefree native cold estate 1/10/100 DISTINCT question-role operations.

Existing I03, not another evaluator. Test selector-based native cold parity,
one index session, post-first-result CURRENT revocation and duplicate refusal.
High-width original-source/100k/6GiB economics separately held.
"""
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_distinct_cold_i03_batch import (
    ColdI03BatchError, ColdI03Operation, execute_distinct_native_cold_i03,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_direct_estate_i03 import _cold


def _case(tmp_path, monkeypatch, size, *, current=None, name="BATCH-COLD"):
    captured = {}
    original_ingest = native.ingest_c11_source_release

    def catch(candidate, repo):
        captured["candidate"] = candidate
        return original_ingest(candidate, repo)

    names = [f"Q{i:03d}" for i in range(size)]
    rows = [
        {"id": f"R{r}", "responses": {
            q: ((r + i) % 2) for i, q in enumerate(names)
        }} for r in range(4)
    ]
    with monkeypatch.context() as guard:
        guard.setattr(native, "ingest_c11_source_release", catch)
        source = native._build_source(
            name, rows, question_namespace="BATCH-COLD-REAL-QUESTIONS",
        )
    candidate = captured["candidate"]
    qauth = native._query_authority(name)
    predicate = native._branch_predicate(source, qauth)
    queries = tuple(
        native._query(source, qauth, predicate, (q,), tag=f"role-{q}")
        for q in names
    )
    root, receipt = _cold(tmp_path, candidate, source["universe"].ref, name)
    estate = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=current if current is not None else (lambda _: True),
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(predicate,),
        queries=queries,
        discovery_authorities=(),
    )
    executor = CarrierNeutralResearchExecutor(
        repository=estate, release_refs=(source["release_ref"],),
        runtime_catalog=catalog,
    )
    requests = tuple(ColdI03Operation(query.ref, predicate.ref) for query in queries)
    return source, qauth, predicate, queries, executor, requests, root


@pytest.mark.parametrize("distinct", [1, 10, 100])
def test_distinct_saved_queries_reuse_one_authentic_native_session(
    tmp_path, monkeypatch, distinct,
):
    source, qauth, predicate, queries, executor, requests, root = _case(
        tmp_path, monkeypatch, distinct, name=f"ONE-COLD-SESSION-{distinct}",
    )
    physical_opens = []
    original_enter = DirectEstateI03Session.__enter__

    def audited_enter(self):
        physical_opens.append(self.estate.i02.release)
        return original_enter(self)

    import pyarrow.parquet as pq

    def forbidden(*_args, **_kwargs):
        raise AssertionError("no full C11 graph or pq.read_table in native batch")

    with monkeypatch.context() as guard:
        guard.setattr(DirectEstateI03Session, "__enter__", audited_enter)
        guard.setattr(C11Repository, "__init__", forbidden)
        guard.setattr(pq, "read_table", forbidden)
        result = execute_distinct_native_cold_i03(
            executor=executor, operations=requests,
        )
    assert len(physical_opens) == 1
    assert result.prepared_session_count == 1
    assert len(result.results) == distinct
    assert len({q.ref for q in queries}) == distinct
    assert len({q.target_refs[0] for q in queries}) == distinct
    assert result.source_release_ref == source["release_ref"]
    assert [r.query_ref for r in result.results] == [q.ref for q in queries]
    assert not list(Path(root).glob(".s2c-native-i03-*"))
    # Independent original in-memory I03 oracle for both ends of the batch.
    for i in sorted({0, distinct - 1}):
        oracle = native._run(source, qauth, predicate, queries[i])
        assert tuple(f.ref for f in result.results[i].facts) == tuple(
            f.ref for f in oracle.facts
        )


def test_duplicate_selected_query_is_refused_before_native_session_build(
    tmp_path, monkeypatch,
):
    *_, executor, requests, root = _case(
        tmp_path, monkeypatch, 2, name="BATCH-DUPLICATE",
    )
    with pytest.raises(ColdI03BatchError, match="duplicate"):
        execute_distinct_native_cold_i03(
            executor=executor, operations=(requests[0], requests[0]),
        )
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_mid_batch_revocation_refuses_and_removes_temporary_postings(
    tmp_path, monkeypatch,
):
    permit = {"allowed": True}
    source, qauth, predicate, queries, executor, requests, root = _case(
        tmp_path, monkeypatch, 2, current=lambda _: permit["allowed"],
        name="BATCH-CURRENT-REVOKED",
    )
    import rawlsing_next.pre553_distinct_cold_i03_batch as subject

    original_execute = subject.execute_empirical_query
    count = {"n": 0}

    def revoke_after_one(*args, **kwargs):
        result = original_execute(*args, **kwargs)
        count["n"] += 1
        if count["n"] == 1:
            permit["allowed"] = False
        return result

    with monkeypatch.context() as guard:
        guard.setattr(subject, "execute_empirical_query", revoke_after_one)
        with pytest.raises(DirectEstateError, match="current source"):
            execute_distinct_native_cold_i03(
                executor=executor, operations=requests,
            )
    assert count["n"] == 1
    assert not list(Path(root).glob(".s2c-native-i03-*"))
