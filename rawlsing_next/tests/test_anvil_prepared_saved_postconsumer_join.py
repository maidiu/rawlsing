"""Exact prepared saved admission through the real postconsumer join.

This is a focused sourcefree regression for the only production change in the
2026-11-18 grant: the exact PreparedSavedC11Admission type at the existing
join boundary.  It does not mint QUERY authority or change native semantics.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_governed_query_issuer_v2 import (
    _issue_compiled_governed_queries_v2,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.tests.test_pyat997_r03_governed_query_issuer_v2 import (
    _v2_admission,
)


def _open_prepared(base, catalog, current=lambda _roots: True):
    return PreparedSavedC11Admission.open(
        root=Path(base.estate_path).parents[1],
        exact_path=base.estate_path,
        independently_held_manifest_sha256=base.manifest_sha256,
        independently_held_i02=base.i02,
        release_ref=base.release_ref,
        runtime_catalog=catalog,
        current_authorizer=current,
    )


def _fixture(tmp_path):
    handoff, estate, base0, v1, _resolver, _sink = s1e._full(
        tmp_path / "sourcefree-q2",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    base = _v2_admission(base0, workload.catalog)
    prepared = _open_prepared(base, workload.catalog)
    manifest, predicates = s1e._issued_manifest(workload, base)
    return {
        "handoff": handoff,
        "estate": estate,
        "base": base,
        "prepared": prepared,
        "v1": v1,
        "issue": issue,
        "workload": workload,
        "manifest": manifest,
        "predicates": predicates,
    }


def _run(admission, fixture):
    return execute_saved_batch(
        admission,
        manifest=fixture["manifest"],
        predicate_ref_by_query=fixture["predicates"],
    )


def _join(admission, runner, fixture):
    return join_saved_source_operation_fates(
        handoff=fixture["handoff"],
        estate_receipt=fixture["estate"],
        admission=admission,
        compilation=fixture["v1"],
        workload=fixture["workload"],
        resolver=TestOnlyDecisionResolver(fixture["issue"].issued.record),
        host=s1e._NATIVE_HOST,
        purpose=s1e._NATIVE_PURPOSE,
        runner=runner,
        issuer_v2=fixture["issue"],
    )


def test_prepared_exact_join_has_base_parity_and_one_prepared_build(
    tmp_path, monkeypatch,
):
    fixture = _fixture(tmp_path)
    assert type(fixture["base"]) is SavedC11Admission
    assert type(fixture["prepared"]) is PreparedSavedC11Admission

    base_runner = _run(fixture["base"], fixture)
    assert len(base_runner.receipts) == len(fixture["manifest"].units) == 13
    assert {r.state for r in base_runner.receipts} == {"COMPLETED"}

    builds = []
    original_build = DirectEstateI03Session._build

    def counted_build(self):
        builds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted_build)
    prepared_runner = _run(fixture["prepared"], fixture)
    assert len(builds) == 1
    assert len(prepared_runner.receipts) == 13
    assert {r.state for r in prepared_runner.receipts} == {"COMPLETED"}

    base_joined = _join(fixture["base"], base_runner, fixture)
    prepared_joined = _join(fixture["prepared"], prepared_runner, fixture)

    assert len(base_joined.rows) == len(prepared_joined.rows) == 22
    assert base_joined.rows == prepared_joined.rows
    assert base_joined.audit == prepared_joined.audit
    assert base_joined.result_hash == prepared_joined.result_hash
    assert prepared_joined.audit["operation_count"] == 22
    assert prepared_joined.audit["preconsumer_fate_counts"] == {
        "ELIGIBLE": 8, "HELD": 14,
    }
    assert prepared_joined.audit["positive_native_linked_operations"] == 6
    assert prepared_joined.audit["pending_eligible_operations"] == 2
    assert prepared_joined.audit["native_completed_units_rechecked"] == 13
    assert prepared_joined.audit["native_discovery_candidates_exactly_joined"] == 8
    assert prepared_joined.audit["issue_grants_created"] == 0
    assert prepared_joined.audit["preconsumer_handoff_unchanged"] is True
    assert all(
        row["postconsumer_receipt_refs"]
        == base_row["postconsumer_receipt_refs"]
        and row["postconsumer_native_output_refs"]
        == base_row["postconsumer_native_output_refs"]
        for row, base_row in zip(prepared_joined.rows, base_joined.rows)
    )
    assert all(
        prepared.provenance_refs == base.provenance_refs
        for prepared, base in zip(
            prepared_runner.receipts, base_runner.receipts,
        )
    )


def test_prepared_type_guard_rejects_subclasses_and_unrelated_admission(
    tmp_path,
):
    fixture = _fixture(tmp_path)
    runner = _run(fixture["prepared"], fixture)

    class PreparedChild(PreparedSavedC11Admission):
        __slots__ = ()

    class BaseChild(SavedC11Admission):
        __slots__ = ()

    for admission in (
        object.__new__(PreparedChild),
        object.__new__(BaseChild),
        object(),
    ):
        with pytest.raises(
            SourceReceiptJoinError,
            match="EXACT_ACCEPTED_PRODUCER_AND_NATIVE_TYPES_REQUIRED",
        ):
            _join(admission, runner, fixture)


def test_prepared_join_rejects_foreign_runner_repository(tmp_path):
    fixture = _fixture(tmp_path)
    base_runner = _run(fixture["base"], fixture)
    assert base_runner.repository is fixture["base"]
    with pytest.raises(
        SourceReceiptJoinError,
        match="BATCH_RUNNER_NOT_BOUND_TO_SAVED_ADMISSION",
    ):
        _join(fixture["prepared"], base_runner, fixture)


@pytest.mark.parametrize("drift", ["manifest", "roots"])
def test_prepared_join_rejects_estate_manifest_or_root_drift(tmp_path, drift):
    fixture = _fixture(tmp_path)
    runner = _run(fixture["prepared"], fixture)
    if drift == "manifest":
        estate = replace(fixture["estate"], manifest_sha256="0" * 64)
    else:
        estate = replace(
            fixture["estate"],
            i02=replace(fixture["estate"].i02, logical="0" * 64),
        )
    with pytest.raises(
        SourceReceiptJoinError,
        match="Q2_SAVED_REPLAY_AND_RELEASE_IDENTITY_DRIFT",
    ):
        join_saved_source_operation_fates(
            handoff=fixture["handoff"], estate_receipt=estate,
            admission=fixture["prepared"], compilation=fixture["v1"],
            workload=fixture["workload"],
            resolver=TestOnlyDecisionResolver(fixture["issue"].issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=runner, issuer_v2=fixture["issue"],
        )


def test_prepared_join_rechecks_revoked_current(tmp_path):
    fixture = _fixture(tmp_path)
    live = [True]
    prepared = _open_prepared(
        fixture["base"], fixture["workload"].catalog,
        current=lambda _roots: live[0],
    )
    runner = _run(prepared, fixture)
    live[0] = False
    with pytest.raises(
        DirectEstateError,
        match="current source/operation authority refused",
    ):
        _join(prepared, runner, fixture)


def test_prepared_join_rejects_unissued_query(tmp_path):
    fixture = _fixture(tmp_path)
    issued = {request.query_ref.key for request in fixture["workload"].requests}
    unissued = next(
        query for query in fixture["workload"].catalog.queries
        if query.ref.key not in issued
    )
    forged_manifest = BatchManifest((
        *fixture["manifest"].units,
        BatchUnitSpec(
            "QUERY", unissued.ref,
            (fixture["prepared"].release_ref,),
            (fixture["workload"].decision_ref,),
        ),
    ))
    runner = BatchExecutionRunner(
        manifest=forged_manifest, repository=fixture["prepared"],
        saved_mode=True,
    )
    with pytest.raises(
        SourceReceiptJoinError,
        match="UNISSUED_SAVED_QUERY",
    ):
        _join(fixture["prepared"], runner, fixture)
    assert runner.receipts == ()


def test_prepared_join_rejects_forged_completed_receipt(tmp_path):
    fixture = _fixture(tmp_path)
    runner = _run(fixture["prepared"], fixture)
    query_unit = next(
        unit for unit in fixture["manifest"].units if unit.job_kind == "QUERY"
    )
    target = next(
        receipt for receipt in runner.receipts
        if receipt.unit_ref == query_unit.unit_ref
    )
    forged = replace(target, result_refs=())
    forged_runner = BatchExecutionRunner(
        manifest=fixture["manifest"], repository=fixture["prepared"],
        prior_receipts=tuple(
            forged if receipt == target else receipt
            for receipt in runner.receipts
        ),
        saved_mode=True,
    )
    with pytest.raises(
        SourceReceiptJoinError,
        match="RECEIPT_NATIVE_FIRST_CONSUMER_OUTPUT_DRIFT",
    ):
        _join(fixture["prepared"], forged_runner, fixture)
