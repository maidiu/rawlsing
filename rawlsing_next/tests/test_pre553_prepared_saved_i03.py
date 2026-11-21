"""Prepared cold saved I03: one posting index reused by many operations."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_prepared_saved_i03 import (
    PreparedSavedC11Admission, PreparedSavedI03Error,
)
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError


def _capture_source(monkeypatch, tag, rows, weights):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original(candidate, repo)

    with monkeypatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(tag, rows, weights=weights)
    return source, holder["candidate"]


def _fixture(monkeypatch, tmp_path, tag, *, grant=lambda _roots: True):
    ids = [f"R{i}" for i in range(1, 9)]
    rows = [
        {"id": respondent, "responses": {
            "X": i % 2, "Y": (i // 2) % 2, "Z": (i // 3) % 2,
        }}
        for i, respondent in enumerate(reversed(ids), start=1)
    ]
    weights = {
        respondent: ("WEIGHT_VALID_AUTHORIZED", ("1/3", "5/7", "11/13", "17/19",
                                                 "1/10", "1/5", "7/3", "2/9")[index])
        for index, respondent in enumerate(ids)
    }
    tmp_path.mkdir(parents=True, exist_ok=True)
    source, candidate = _capture_source(monkeypatch, tag, rows, weights)
    qa = native._query_authority(tag)
    predicate = native._branch_predicate(source, qa, tag=tag)
    other_predicate = native._branch_predicate(source, qa, tag=f"{tag}-other")
    queries = {
        "selected": native._query(source, qa, predicate, ("Y",),
                                  measure="GOVERNED_WEIGHTED", tag=f"{tag}-s"),
        "f2": native._query(source, qa, predicate, ("Y", "X"),
                            measure="GOVERNED_WEIGHTED", tag=f"{tag}-f2"),
        "f4": native._query(source, qa, predicate, ("X", "Y", "Z"),
                            measure="GOVERNED_WEIGHTED", tag=f"{tag}-f4"),
        "raw": native._query(source, qa, predicate, ("Y",), tag=f"{tag}-raw"),
    }
    root, receipt = s2c._cold(tmp_path, candidate, source["universe"].ref, tag)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=(predicate, other_predicate),
        queries=tuple(queries.values()),
        discovery_authorities=(),
    )
    admission = PreparedSavedC11Admission.open(
        root=root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=grant,
    )
    return source, qa, predicate, other_predicate, queries, admission


def _projection(fact):
    return hashlib.sha256(
        canonical_json(fact.semantic_projection()).encode()).hexdigest()


def test_prepared_session_matches_baseline_and_builds_one_index(
    tmp_path, monkeypatch,
):
    source, qa, predicate, other_predicate, queries, admission = _fixture(
        monkeypatch, tmp_path / "prepared", "PREP",
    )
    builds = []
    original_build = DirectEstateI03Session._build

    def counted(self):
        builds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted)
    baseline = {}
    for name, query in queries.items():
        result = admission.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref)
        oracle = native._run(source, qa, predicate, query)
        assert result.facts[0].ref == oracle.facts[0].ref
        assert _projection(result.facts[0]) == _projection(oracle.facts[0])
        baseline[name] = result.facts[0].ref
    assert len(builds) == len(queries)

    builds.clear()
    prepared_facts = {}
    with admission.prepared_i03() as prepared:
        for name, query in queries.items():
            result = prepared.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref)
            prepared_facts[name] = result.facts[0].ref
            assert result.facts[0].ref == baseline[name]
        assert prepared.receipt().operations == len(queries)
    assert len(builds) == 1
    assert prepared_facts == baseline
    with pytest.raises(PreparedSavedI03Error, match="closed"):
        prepared.execute_i03(
            query_ref=queries["selected"].ref, predicate_ref=predicate.ref)


def test_prepared_session_revocation_and_condition_refusal(tmp_path, monkeypatch):
    grant = {"now": True}
    source, qa, predicate, other_predicate, queries, admission = _fixture(
        monkeypatch, tmp_path / "revoked", "PREP-REV",
        grant=lambda _roots: grant["now"],
    )
    with admission.prepared_i03() as prepared:
        prepared.execute_i03(
            query_ref=queries["selected"].ref, predicate_ref=predicate.ref)
        grant["now"] = False
        with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
            prepared.execute_i03(
                query_ref=queries["f2"].ref, predicate_ref=predicate.ref)
        grant["now"] = True
        prepared.execute_i03(
            query_ref=queries["f4"].ref, predicate_ref=predicate.ref)
        with pytest.raises(PreparedSavedI03Error, match="exact query condition"):
            prepared.execute_i03(
                query_ref=queries["selected"].ref,
                predicate_ref=other_predicate.ref,
            )


def test_prepared_i05_reuses_session_with_exact_discovery_parity(
    tmp_path, monkeypatch,
):
    from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
    handoff, estate, admission, v1, _, _ = s1e._full(tmp_path / "prepared-i05")
    workload = v1.issued.workload
    prepared_admission = PreparedSavedC11Admission.open(
        root=Path(admission.estate_path).parents[1],
        exact_path=admission.estate_path,
        independently_held_manifest_sha256=admission.manifest_sha256,
        independently_held_i02=admission.i02,
        release_ref=admission.release_ref,
        runtime_catalog=workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    authority = workload.discoveries[0]
    baseline = prepared_admission.execute_i05(
        discovery_authority_ref=authority)
    with prepared_admission.prepared_i03() as prepared:
        observed = prepared.execute_i05(discovery_authority_ref=authority)
        assert prepared.receipt().operations == 1
    assert [r.ref.key for r in observed.receipts] == [
        r.ref.key for r in baseline.receipts
    ]
    assert observed.evaluated_frontier_ref == baseline.evaluated_frontier_ref


def test_plain_saved_admission_can_reuse_inherited_prepared_index_without_repin(
    tmp_path, monkeypatch,
):
    """P0 existing C11→I03: 1/10/100 sourcefree operations, one index, no new issuer.

    Repeated queries are deliberately not asserted distinct scientific jobs.
    Q014/R03 uses a separate issued-distinct saved Batch test.
    """
    from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
    source, qa, predicate, _, queries, prepared_admission = _fixture(
        monkeypatch, tmp_path / "plain-to-prepared", "SAVED-REUSE",
    )
    ordinary = SavedC11Admission.open(
        root=Path(prepared_admission.estate_path).parents[1],
        exact_path=prepared_admission.estate_path,
        independently_held_manifest_sha256=prepared_admission.manifest_sha256,
        independently_held_i02=prepared_admission.i02,
        release_ref=prepared_admission.release_ref,
        runtime_catalog=prepared_admission._runtime_catalog,
        current_authorizer=lambda _roots: True,
    )
    original_build = DirectEstateI03Session._build
    builds = []

    def counted(self):
        builds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted)
    native_query = queries["selected"]
    oracle = ordinary.execute_i03(
        query_ref=native_query.ref, predicate_ref=predicate.ref,
    )
    assert len(builds) == 1
    for count in (1, 10, 100):
        builds.clear()
        upgraded = PreparedSavedC11Admission.from_verified_admission(ordinary)
        with upgraded.prepared_i03() as session:
            observed = tuple(
                session.execute_i03(
                    query_ref=native_query.ref, predicate_ref=predicate.ref,
                ) for _ in range(count)
            )
            assert session.receipt().operations == count
        assert len(builds) == 1
        assert all(result.facts[0].ref == oracle.facts[0].ref
                   for result in observed)
        assert not list(Path(ordinary.estate_path).parents[1].glob(
            ".s2c-native-i03-*",
        ))
    with pytest.raises(PreparedSavedI03Error, match="EXACT_EXISTING_SAVED_ADMISSION"):
        PreparedSavedC11Admission.from_verified_admission(object())


def test_plain_to_prepared_rechecks_revoked_current_before_build(tmp_path, monkeypatch):
    from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
    grant = {"allowed": True}
    _, _, _, _, _, admission = _fixture(
        monkeypatch, tmp_path / "revoked-upgrade", "SAVED-UPGRADE-REV",
        grant=lambda _roots: grant["allowed"],
    )
    ordinary = SavedC11Admission.open(
        root=Path(admission.estate_path).parents[1],
        exact_path=admission.estate_path,
        independently_held_manifest_sha256=admission.manifest_sha256,
        independently_held_i02=admission.i02,
        release_ref=admission.release_ref,
        runtime_catalog=admission._runtime_catalog,
        current_authorizer=lambda _roots: grant["allowed"],
    )
    grant["allowed"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        PreparedSavedC11Admission.from_verified_admission(ordinary)
