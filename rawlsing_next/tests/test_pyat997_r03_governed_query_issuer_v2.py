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
from rawlsing_next.pre553_saved_c11_admission import SavedReleaseIdentity
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner


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
    tmp_path,
):
    _, _, admission, v1, _, _ = s1e._full(
        tmp_path / "r03-v2-batch",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    assert workload.requests
    manifest, predicates = s1e._issued_manifest(workload, admission)
    results = s1e.execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicates,
    )
    assert len(results.receipts) == len(manifest.units)
    assert all(x.state == "COMPLETED" for x in results.receipts)
    assert any(x.unit_kind == "QUERY" for x in manifest.units)
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
    private.mkdir(parents=True, exist_ok=True)
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
