import hashlib
from dataclasses import FrozenInstanceError

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchDeferred,
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
    UnitExecutionReceipt,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{label}", _h(f"{kind}:{label}"))


def _release(label: str) -> ExactRef:
    return ExactRef("C11LogicalRelease", f"release-{label}", _h(f"release:{label}"))


def _repo(*release_refs: ExactRef) -> C11Repository:
    repository = C11Repository()
    # R16 only calls the accepted I02 exact resolver. These are opaque harness
    # occupants; no C11 semantics are manufactured by this test helper.
    for ref in release_refs:
        repository._by_ref[ref.key] = object()
    return repository


def _unit(
    kind: str,
    label: str,
    release_ref: ExactRef,
    *,
    semantic_inputs=(),
) -> BatchUnitSpec:
    job_kind = kind.upper()
    if job_kind == "QUERY":
        job_ref = _ref("EmpiricalQuerySpec@1.0.0", label)
    else:
        job_ref = _ref("DiscoveryJob", label)
    return BatchUnitSpec(
        job_kind=job_kind,
        job_ref=job_ref,
        release_refs=(release_ref,),
        semantic_input_refs=tuple(semantic_inputs),
    )


def _result_for(unit: BatchUnitSpec, suffix: str = "ok") -> ExecutionOutcome:
    return ExecutionOutcome(
        result_refs=(_ref("RESULT", f"{unit.unit_hash}:{suffix}"),),
        provenance_refs=(_ref("EXECUTION_TRACE", f"{unit.unit_hash}:{suffix}"),),
    )


def _binding(kind: str, execute) -> ExecutorBinding:
    return ExecutorBinding(_ref("EXECUTOR", kind.lower()), execute)


def test_manifest_is_immutable_and_storage_order_independent():
    release = _release("A")
    query = _unit("QUERY", "q", release)
    discovery = _unit(
        "DISCOVERY",
        "d",
        release,
        semantic_inputs=(_ref("DiscoveryAuthority@1.0.0", "auth"),),
    )

    left = BatchManifest((query, discovery))
    right = BatchManifest((discovery, query))

    assert left.manifest_hash == right.manifest_hash
    assert left.manifest_ref == right.manifest_ref
    assert tuple(unit.unit_ref for unit in left.units) == tuple(
        unit.unit_ref for unit in right.units
    )
    assert tuple(unit.unit_hash for unit in left.units) == tuple(
        sorted((query.unit_hash, discovery.unit_hash))
    )
    with pytest.raises(FrozenInstanceError):
        left.units = ()
    with pytest.raises(FrozenInstanceError):
        query.job_kind = "DISCOVERY"


def test_exact_release_identity_only_no_latest_default_fuzzy_or_wrong_kind():
    with pytest.raises(BatchIntegrityError):
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", "q"),
            release_refs=(ExactRef("C11LogicalRelease", "latest", _h("latest")),),
        )
    with pytest.raises(BatchIntegrityError):
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", "q"),
            release_refs=(_ref("SOURCE", "not-c11"),),
        )

    release = _release("A")
    manifest = BatchManifest((_unit("QUERY", "q", release),))
    with pytest.raises(BatchIntegrityError, match="no latest/default/fuzzy/nearest fallback"):
        BatchExecutionRunner(manifest=manifest, repository=_repo())


def test_semantic_unit_identity_is_independent_of_input_container_order():
    release_a = _release("A")
    release_b = _release("B")
    input_a = _ref("INPUT", "A")
    input_b = _ref("INPUT", "B")
    job = _ref("EmpiricalQuerySpec@1.0.0", "q")

    left = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=job,
        release_refs=(release_a, release_b),
        semantic_input_refs=(input_a, input_b),
    )
    right = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=job,
        release_refs=(release_b, release_a, release_a),
        semantic_input_refs=(input_b, input_a, input_b),
    )
    assert left.unit_ref == right.unit_ref
    assert left.semantic_projection() == right.semantic_projection()


def test_deterministic_schedule_and_executor_mapping_order_do_not_change_results():
    release = _release("A")
    units = (
        _unit("QUERY", "q2", release),
        _unit("DISCOVERY", "d1", release),
        _unit("QUERY", "q1", release),
    )
    manifest = BatchManifest(tuple(reversed(units)))
    repository = _repo(release)
    called = []

    def execute(unit):
        called.append(unit.unit_ref)
        return _result_for(unit)

    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    created = runner.run(
        executors={
            "DISCOVERY": _binding("discovery", execute),
            "QUERY": _binding("query", execute),
        }
    )

    assert tuple(called) == tuple(unit.unit_ref for unit in manifest.units)
    assert tuple(receipt.unit_ref for receipt in created) == tuple(called)
    assert all(receipt.state == "COMPLETED" for receipt in created)
    summary = runner.summary()
    assert summary.batch_state == "COMPLETED"
    assert summary.full_coverage is True
    assert summary.coverage_state == "FULL_MANIFEST_COVERAGE"
    assert summary.completed_units == len(units)
    assert summary.populated_data_execution_claim is False


def test_completed_receipt_has_exact_job_release_input_executor_and_trace_provenance():
    release = _release("A")
    semantic_input = _ref("PREDICATE", "p")
    unit = _unit("QUERY", "q", release, semantic_inputs=(semantic_input,))
    manifest = BatchManifest((unit,))
    executor_ref = _ref("EXECUTOR", "query")
    extra_trace = _ref("EXECUTION_TRACE", "trace")

    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))
    receipt = runner.run(
        executors={
            "QUERY": ExecutorBinding(
                executor_ref,
                lambda _: ExecutionOutcome(
                    result_refs=(_ref("RESULT", "r"),),
                    provenance_refs=(extra_trace,),
                ),
            )
        }
    )[0]

    assert receipt.state == "COMPLETED"
    assert receipt.execution_performed is True
    assert receipt.executor_ref == executor_ref
    provenance = set(receipt.provenance_refs)
    assert unit.job_ref in provenance
    assert release in provenance
    assert semantic_input in provenance
    assert executor_ref in provenance
    assert extra_trace in provenance


def test_max_units_throttle_cannot_masquerade_as_full_coverage():
    release = _release("A")
    manifest = BatchManifest(
        (_unit("QUERY", "q1", release), _unit("QUERY", "q2", release))
    )
    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))
    created = runner.run(
        executors={"QUERY": _binding("query", _result_for)},
        max_units=1,
    )

    assert len(created) == 1
    summary = runner.summary()
    assert summary.batch_state == "IN_PROGRESS"
    assert summary.full_coverage is False
    assert summary.coverage_state == "INCOMPLETE_MANIFEST_COVERAGE"
    assert summary.completed_units == 1
    assert summary.pending_units == 1


def test_missing_discovery_executor_is_explicit_deferred_then_resumable():
    release = _release("A")
    query = _unit("QUERY", "q", release)
    discovery = _unit("DISCOVERY", "d", release)
    manifest = BatchManifest((query, discovery))
    repository = _repo(release)

    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    first = runner.run(executors={"QUERY": _binding("query", _result_for)})
    by_unit = {receipt.unit_ref: receipt for receipt in first}
    assert by_unit[query.unit_ref].state == "COMPLETED"
    assert by_unit[discovery.unit_ref].state == "DEFERRED"
    assert by_unit[discovery.unit_ref].execution_performed is False
    assert by_unit[discovery.unit_ref].failure_code == "EXECUTOR_UNAVAILABLE"
    assert runner.summary().batch_state == "DEFERRED"
    assert runner.summary().full_coverage is False

    resumed = BatchExecutionRunner(
        manifest=manifest,
        repository=repository,
        prior_receipts=runner.receipts,
    )
    second = resumed.run(
        executors={"DISCOVERY": _binding("discovery", _result_for)}
    )
    assert len(second) == 1
    assert second[0].unit_ref == discovery.unit_ref
    assert second[0].attempt_index == 2
    assert second[0].state == "COMPLETED"
    assert resumed.summary().batch_state == "COMPLETED"
    assert resumed.summary().full_coverage is True


def test_failed_attempt_resume_keeps_exact_semantic_unit_identity():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))
    repository = _repo(release)

    def fail(_):
        raise RuntimeError("hostile deterministic failure")

    first_runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    failed = first_runner.run(executors={"QUERY": _binding("query-v1", fail)})[0]
    assert failed.state == "FAILED"
    assert failed.attempt_index == 1
    assert failed.unit_ref == unit.unit_ref
    assert first_runner.summary().full_coverage is False

    resumed = BatchExecutionRunner(
        manifest=manifest,
        repository=repository,
        prior_receipts=first_runner.receipts,
    )
    completed = resumed.run(
        executors={"QUERY": _binding("query-v2", _result_for)}
    )[0]
    assert completed.state == "COMPLETED"
    assert completed.attempt_index == 2
    assert completed.unit_ref == failed.unit_ref == unit.unit_ref
    assert resumed.manifest.manifest_ref == manifest.manifest_ref
    assert resumed.summary().actual_execution_receipts == 2


def test_executor_can_explicitly_defer_without_laundering_to_completion():
    release = _release("A")
    unit = _unit("DISCOVERY", "d", release)
    manifest = BatchManifest((unit,))

    def defer(_):
        raise BatchDeferred("DEPENDENCY_NOT_ACCEPTED", "I05 semantic executor unavailable")

    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))
    receipt = runner.run(
        executors={"DISCOVERY": _binding("discovery", defer)}
    )[0]
    assert receipt.state == "DEFERRED"
    assert receipt.execution_performed is True
    assert receipt.failure_code == "DEPENDENCY_NOT_ACCEPTED"
    assert runner.summary().batch_state == "DEFERRED"
    assert runner.summary().coverage_state == "INCOMPLETE_MANIFEST_COVERAGE"


def test_generic_executor_error_is_explicit_failed_not_semantic_result():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))

    def explode(_):
        raise ValueError("boom")

    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))
    receipt = runner.run(executors={"QUERY": _binding("query", explode)})[0]
    assert receipt.state == "FAILED"
    assert receipt.result_refs == ()
    assert receipt.failure_code == "EXECUTOR_EXCEPTION:ValueError"
    assert runner.summary().batch_state == "FAILED"
    assert runner.summary().full_coverage is False


def test_resume_receipt_storage_order_is_nonsemantic():
    release = _release("A")
    units = (_unit("QUERY", "q1", release), _unit("QUERY", "q2", release))
    manifest = BatchManifest(units)
    repository = _repo(release)

    original = BatchExecutionRunner(manifest=manifest, repository=repository)
    original.run(executors={"QUERY": _binding("query", _result_for)})
    canonical_hash = original.summary().receipt_set_hash

    reversed_resume = BatchExecutionRunner(
        manifest=manifest,
        repository=repository,
        prior_receipts=tuple(reversed(original.receipts)),
    )
    assert reversed_resume.receipts == original.receipts
    assert reversed_resume.summary().receipt_set_hash == canonical_hash
    assert reversed_resume.summary().full_coverage is True


def test_receipt_manifest_unit_attempt_and_provenance_tamper_fail_closed():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))
    repository = _repo(release)
    executor = _ref("EXECUTOR", "query")
    result = _ref("RESULT", "r")
    unrelated = _ref("PROVENANCE", "unrelated")

    bad_manifest = UnitExecutionReceipt(
        manifest_hash=_h("wrong-manifest"),
        unit_ref=unit.unit_ref,
        attempt_index=1,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=executor,
        result_refs=(result,),
        provenance_refs=(unit.job_ref, release, executor),
    )
    with pytest.raises(BatchIntegrityError, match="manifest hash mismatch"):
        BatchExecutionRunner(
            manifest=manifest,
            repository=repository,
            prior_receipts=(bad_manifest,),
        )

    gap = UnitExecutionReceipt(
        manifest_hash=manifest.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=2,
        state="FAILED",
        execution_performed=True,
        executor_ref=executor,
        failure_code="FAIL",
        detail_hash=_h("detail"),
    )
    with pytest.raises(BatchIntegrityError, match="contiguous"):
        BatchExecutionRunner(
            manifest=manifest,
            repository=repository,
            prior_receipts=(gap,),
        )

    missing_provenance = UnitExecutionReceipt(
        manifest_hash=manifest.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=1,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=executor,
        result_refs=(result,),
        provenance_refs=(unrelated,),
    )
    with pytest.raises(BatchIntegrityError, match="provenance closure"):
        BatchExecutionRunner(
            manifest=manifest,
            repository=repository,
            prior_receipts=(missing_provenance,),
        )


def test_completed_receipt_cannot_be_retried_or_rewritten():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))
    repository = _repo(release)
    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    runner.run(executors={"QUERY": _binding("query", _result_for)})

    assert runner.pending_units() == ()
    assert runner.run(executors={"QUERY": _binding("query-v2", _result_for)}) == ()
    with pytest.raises(BatchIntegrityError, match="completed unit is not retryable"):
        runner.next_attempt_index(unit)


def test_result_and_provenance_storage_order_do_not_change_receipt_identity():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))
    executor = _ref("EXECUTOR", "query")
    r1, r2 = _ref("RESULT", "1"), _ref("RESULT", "2")
    p1, p2 = unit.job_ref, release

    left = UnitExecutionReceipt(
        manifest_hash=manifest.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=1,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=executor,
        result_refs=(r1, r2),
        provenance_refs=(p1, p2, executor),
    )
    right = UnitExecutionReceipt(
        manifest_hash=manifest.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=1,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=executor,
        result_refs=(r2, r1, r2),
        provenance_refs=(executor, p2, p1, p1),
    )
    assert left.receipt_ref == right.receipt_ref
    assert left.result_refs == right.result_refs
    assert left.provenance_refs == right.provenance_refs


def test_cache_like_presence_is_not_a_receipt_and_cannot_complete_work():
    release = _release("A")
    unit = _unit("QUERY", "q", release)
    manifest = BatchManifest((unit,))
    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))

    fake_cache = {unit.unit_ref.key: _ref("RESULT", "cached")}
    assert fake_cache
    assert runner.receipts == ()
    assert runner.pending_units() == (unit,)
    assert runner.summary().batch_state == "READY"
    assert runner.summary().full_coverage is False

    called = []

    def execute(exact_unit):
        called.append(exact_unit.unit_ref)
        return _result_for(exact_unit, "fresh")

    runner.run(executors={"QUERY": _binding("query", execute)})
    assert called == [unit.unit_ref]
    assert runner.summary().full_coverage is True
    assert runner.summary().populated_data_execution_claim is False


def test_discovery_job_is_opaque_exact_identity_not_candidate_definition():
    release = _release("A")
    discovery_job = _ref("DiscoveryResultReceipt@1.0.0", "job")
    authority = _ref("DiscoveryAuthority@1.0.0", "authority")
    candidate_frontier = _ref("DECLARED_DISCOVERY_FRONTIER", "frontier")
    unit = BatchUnitSpec(
        job_kind="DISCOVERY",
        job_ref=discovery_job,
        release_refs=(release,),
        semantic_input_refs=(authority, candidate_frontier),
    )
    manifest = BatchManifest((unit,))
    runner = BatchExecutionRunner(manifest=manifest, repository=_repo(release))

    seen = []

    def execute(exact_unit):
        seen.append(exact_unit.semantic_projection())
        return _result_for(exact_unit)

    runner.run(executors={"DISCOVERY": _binding("discovery", execute)})
    assert seen == [unit.semantic_projection()]
    assert authority in unit.semantic_input_refs
    assert candidate_frontier in unit.semantic_input_refs
    assert runner.summary().full_coverage is True
