"""PYAT R03: versioned original-governed QUERY issuer (sourcefree ONLY).

An author-grade test fixture derived from accepted #997 saved/native tests.
No independent G5, original35 source permission, real SOURCE_REALIZED claim,
or new scientific authority can be inferred from the test outcome.
"""
from __future__ import annotations

from dataclasses import replace

import pytest
pytest.importorskip("pyarrow")

from rawlsing_next.pre553_governed_query_issuer_v2 import (
    GOVERNED_QUERY_ISSUER_SCHEMA,
    _issue_compiled_governed_queries_v2,
    compile_and_issue_governed_queries_v2,
)
from rawlsing_next.pre553_issued_workload import operation_jobs
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, WorkloadBindingRefusal,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedReleaseIdentity,
)
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)


def _v2_admission(admission: SavedC11Admission, catalog) -> SavedC11Admission:
    """Re-admit the SAME saved estate with the exact v2 issued execution catalog.

    No source is opened here: this verifies the same manifest/release/current
    pins and only adds the exact compiled role objects that v2 actually issued.
    """
    from pathlib import Path

    return SavedC11Admission.open(
        root=Path(admission.estate_path).parents[1],
        exact_path=admission.estate_path,
        independently_held_manifest_sha256=admission.manifest_sha256,
        independently_held_i02=admission.i02,
        release_ref=admission.release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )


def test_v1_discovery_is_unchanged_and_v2_jobs_come_only_from_original_eligible_roles(
    tmp_path,
):
    handoff, estate, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-eligible",
    )
    assert v1.issued.workload.requests == ()
    assert len(v1.issued.workload.discoveries) == 1

    issued_v2 = _issue_compiled_governed_queries_v2(v1)
    assert issued_v2.schema == GOVERNED_QUERY_ISSUER_SCHEMA
    assert issued_v2.issued.record.scope == "TEST_ONLY_SOURCEFREE"
    assert issued_v2.issued.workload.discoveries == v1.issued.workload.discoveries
    assert issued_v2.issued.record.original_u_root == v1.issued.record.original_u_root
    assert issued_v2.issued.record.expected_frontier_root == v1.plan.content_hash
    assert issued_v2.issued.record.expected_jobs == operation_jobs(
        issued_v2.issued.workload.requests, issued_v2.issued.workload.discoveries,
    )
    assert issued_v2.operation_jobs, "originally eligible supported QUERY roles not issued"
    expected = {
        row.operation_id for row in v1.plan.records
        if row.status == "SUPPORTED"
        and row.operation_id in v1.frontier_eligible_operation_ids
        and (v1.operation_dispositions or {}).get(row.operation_id) == "ELIGIBLE"
        and row.query_role_refs
    }
    assert expected
    assert {b.operation_id for b in issued_v2.operation_jobs} == expected
    assert all(
        v1.operation_dispositions[b.operation_id] == "ELIGIBLE"
        for b in issued_v2.operation_jobs
    )
    assert len({
        b.query_ref.key for b in issued_v2.operation_jobs
    }) == len(issued_v2.issued.workload.requests)
    assert issued_v2.issued.record.envelope_sha256 == issued_v2.issued.envelope_sha256
    assert issued_v2.material()["native_original_source_rights"] == "NOT_GRANTED"


def test_v2_valid_issued_query_runs_actual_saved_batch_without_source_reopen(
    tmp_path, monkeypatch,
):
    _, _, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-batch",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    assert workload.requests
    admission = _v2_admission(admission, workload.catalog)
    manifest, predicates = s1e._issued_manifest(workload, admission)
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
    from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
    rebuilds = []
    original_build = DirectEstateI03Session._build

    def counted_build(self):
        rebuilds.append(1)
        return original_build(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted_build)
    results = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicates,
        reuse_prepared_session=True,
    )
    assert len(rebuilds) == 1, "one R03 v2 saved Batch must share one postings build"
    assert len(results.receipts) == len(manifest.units)
    assert all(x.state == "COMPLETED" for x in results.receipts)
    assert any(x.job_kind == "QUERY" for x in manifest.units)
    # An executing saved QUERY is NOT an original-scientific F4 result, and
    # does NOT gain source-realized original operation status by itself.


def test_v1_postconsumer_guards_reject_even_consistent_v2_query_injection(
    tmp_path,
):
    handoff, estate, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-v1-negative",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    assert workload.requests
    admission = _v2_admission(admission, workload.catalog)
    manifest, _ = s1e._issued_manifest(workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    with pytest.raises(SourceReceiptJoinError, match=(
        "R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT|"
        "R03_COMPILER_ORIGINAL_ISSUER_IDENTITY_DRIFT"
    )):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=replace(v1, issued=issue.issued),
            workload=workload,
            resolver=TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=runner,
        )
    assert runner.receipts == ()


def test_sourcefree_public_compiler_rederives_frozen_frontier_and_preserves_prohibitions(
    tmp_path,
):
    root = tmp_path / "r03-v2-public"
    root.mkdir(parents=True, exist_ok=True)
    fixture = s1e._fixed_fixture(s1e._native_fixture(
        root, values=(0., 1., 0., 1., 0.),
    ))
    private = root / "private"
    private.mkdir(parents=True, exist_ok=True, mode=0o700)
    sink = SourceSavedBodySink(
        certificate_path=root / "source-i02.sqlite",
        authorized_private_root=private, chunk_rows=2,
    )
    handoff = s1e.build(
        root, fixture,
        name="source-i02.sqlite", body_sink=sink, chunk_size=2,
    )
    release = SavedReleaseIdentity(sink.receipt.reconstructed_v1_release_ref)
    bundle = s1e._native_bundle(
        handoff, fixture, fixture["projection"], release,
    )
    from rawlsing_next.tests.test_pyat960_s1e_native_fact import _NATIVE_AS_OF
    issue = compile_and_issue_governed_queries_v2(
        bundle=bundle, inventory=fixture["inventory"],
        policy=fixture["policy"], frontier=fixture["frontier"],
        as_of=_NATIVE_AS_OF, host=s1e._NATIVE_HOST,
        purpose=s1e._NATIVE_PURPOSE,
    )
    assert issue.schema == GOVERNED_QUERY_ISSUER_SCHEMA
    assert issue.issued.record.scope == "TEST_ONLY_SOURCEFREE"
    assert issue.original_compilation.issued.workload.requests == ()
    assert all(
        issue.original_compilation.operation_dispositions[b.operation_id] == "ELIGIBLE"
        for b in issue.operation_jobs
    )


def test_v2_saved_postconsumer_consumes_only_new_compiler_issued_jobs(
    tmp_path,
):
    handoff, estate, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-saved-join",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    assert workload.requests
    admission = _v2_admission(admission, workload.catalog)
    manifest, predicates = s1e._issued_manifest(workload, admission)
    from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
    runner = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicates,
    )
    assert len(runner.receipts) == len(manifest.units)
    # This is the SAME real saved-runner result later checked by S1-E.
    # A separate newly created but unexecuted Batch runner would prove nothing.
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=v1, workload=workload,
        resolver=TestOnlyDecisionResolver(issue.issued.record),
        host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
        runner=runner, issuer_v2=issue,
    )
    assert len(joined.rows) == len(handoff.operation_fates)
    assert all(
        row["postconsumer_receipt_refs"] == ()
        for row in joined.rows if row["disposition"] != "ELIGIBLE"
    )
    assert joined.audit["native_completed_units_rechecked"] == len(manifest.units)
    # POSITIVE is only allowed if the exact source-side Q2 realization and
    # the complete original compiled query role agree with that executed unit.
    assert any(
        row["postconsumer_state"] == "TEST_ONLY_SAVED_NATIVE_QUERY_RECEIPTED"
        for row in joined.rows
    )


def test_v2_changed_operation_bindings_refuse_even_matching_current_record(
    tmp_path,
):
    handoff, estate, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-forged-map",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    admission = _v2_admission(admission, workload.catalog)
    manifest, _ = s1e._issued_manifest(workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True,
    )
    forged = replace(issue, operation_jobs=())
    with pytest.raises(
        SourceReceiptJoinError,
        match="R03_V2_ORIGINAL_GOVERNED_OPERATION_ISSUER_DRIFT",
    ):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=v1, workload=workload,
            resolver=TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=runner, issuer_v2=forged,
        )
    assert runner.receipts == ()


def test_v2_issuer_refuses_caller_injected_query_in_original_issuance(
    tmp_path,
):
    _, _, _, v1, _, _ = s1e._full(tmp_path / "r03-v2-injected-original")
    query = next(iter(v1.runtime_catalog.queries))
    predicate = next(iter(v1.runtime_catalog.predicates))
    from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
    forged_workload = replace(
        v1.issued.workload,
        requests=(I03ExecutionRequest(query.ref, predicate.ref),),
    )
    forged = replace(
        v1, issued=replace(v1.issued, workload=forged_workload),
    )
    with pytest.raises(
        WorkloadBindingRefusal,
        match="R03_V2_ORIGINAL_ISSUER_MUST_BE_AUTHENTIC",
    ):
        _issue_compiled_governed_queries_v2(forged)


def test_v2_join_refuses_manifest_query_not_issued_by_v2(tmp_path):
    handoff, estate, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-unissued-saved-query",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    admission = _v2_admission(admission, workload.catalog)
    manifest, _ = s1e._issued_manifest(workload, admission)
    issued = {request.query_ref.key for request in workload.requests}
    unissued = next(
        query for query in workload.catalog.queries
        if query.ref.key not in issued
    )
    forged_manifest = BatchManifest((
        *manifest.units,
        BatchUnitSpec(
            "QUERY", unissued.ref,
            (admission.release_ref,), (workload.decision_ref,),
        ),
    ))
    runner = BatchExecutionRunner(
        manifest=forged_manifest, repository=admission, saved_mode=True,
    )
    with pytest.raises(
        SourceReceiptJoinError, match="UNISSUED_SAVED_QUERY",
    ):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=v1, workload=workload,
            resolver=TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=runner, issuer_v2=issue,
        )
    assert runner.receipts == ()


def test_r03_v2_normal_issued_saved_prepared_i03_preserves_native_s04_results(
    tmp_path, monkeypatch,
):
    """Actual original U/E_pre issuer -> saved Batch -> native I03 -> S04.

    NativeWorkloadResult is the preexisting output owner; no new result store,
    fabricated role, second native query or scientific permission is added.
    """
    _, _, initial, v1, _, _ = s1e._full(tmp_path / "r03-v2-normal-prepared")
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    assert workload.requests
    from rawlsing_next.pre553_issued_workload import execute_issued_workload
    from rawlsing_next.pre553_s04_first_consumer import receive_s04_first_consumer
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session

    original_build = DirectEstateI03Session._build
    index_builds = []

    def counted_build(self):
        index_builds.append(1)
        return original_build(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "_build", counted_build)
        result = execute_issued_workload(
            workload, TestOnlyDecisionResolver(issue.issued.record),
            saved_admission_factory=lambda: _v2_admission(initial, workload.catalog),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            allow_test_only=True, reuse_prepared_saved_session=True,
        )
    assert len(index_builds) == 1
    assert result.summary.full_coverage
    assert result.outputs_by_unit
    observed_query_count = 0
    for unit in result.manifest.units:
        if unit.job_kind != "QUERY":
            continue
        native = result.outputs_by_unit[unit.unit_hash]
        query = workload.catalog.resolve_query_exact(unit.job_ref)
        s04 = receive_s04_first_consumer(query=query, execution=native)
        assert s04.execution is native
        assert s04.knowledge.material()["fact_ref"] == native.facts[0].ref.as_dict()
        assert s04.receipt.material()["producer_operation"] == (
            "ONE_PREEXISTING_I03_RESULT__NO_ADDITIONAL_QUERY"
        )
        observed_query_count += 1
    assert observed_query_count == len(workload.requests)

    # Same original issuer, release and query: prepared and default paths
    # must return identical empirical fact/receipt refs.
    baseline = execute_issued_workload(
        workload, TestOnlyDecisionResolver(issue.issued.record),
        saved_admission_factory=lambda: _v2_admission(initial, workload.catalog),
        host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
        allow_test_only=True,
    )
    def refs(result):
        return {
            key: (tuple(f.ref for f in value.facts) if hasattr(value, "facts")
                  else tuple(x.ref for x in value.receipts))
            for key, value in result.outputs_by_unit.items()
        }
    assert refs(result) == refs(baseline)


def test_r03_v2_prepared_saved_flag_refuses_unbacked_or_truthy_grants(tmp_path):
    _, _, _, v1, _, _ = s1e._full(tmp_path / "r03-v2-no-fake-prepared")
    issue = _issue_compiled_governed_queries_v2(v1)
    from rawlsing_next.pre553_issued_workload import (
        WorkloadAdmissionError, execute_issued_workload,
    )
    with pytest.raises(WorkloadAdmissionError, match="PREPARED_SAVED_REQUIRES_SAVED_ADMISSION"):
        execute_issued_workload(
            issue.issued.workload, TestOnlyDecisionResolver(issue.issued.record),
            source_factory=lambda _: (_ for _ in ()).throw(
                AssertionError("MUST_NOT_OPEN_SOURCE")
            ),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            allow_test_only=True, reuse_prepared_saved_session=True,
        )
    with pytest.raises(WorkloadAdmissionError, match="EXACT_PREPARED_SAVED_OPT_IN_REQUIRED"):
        execute_issued_workload(
            issue.issued.workload, TestOnlyDecisionResolver(issue.issued.record),
            saved_admission_factory=lambda: None,
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            allow_test_only=True, reuse_prepared_saved_session=1,
        )
