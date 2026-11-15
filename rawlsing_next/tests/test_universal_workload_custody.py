"""R91 R04_JOINED sourcefree custody/resume qualification (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_issued_workload import (
    WorkloadAdmissionError, capture_joined_checkpoint,
    restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
from rawlsing_next.pre553_universal_workload import compile_universal_workload
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3, s3_rows,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
AS_OF = "2026-10-24"
HOST = "local-r91-r04"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def _issued_workloads(tmp_path):
    path = tmp_path / "r91_r04.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    issued = tuple(
        item.issued for item in compilation.compiled if item.issued is not None
    )
    assert len(issued) >= 3
    return bundle, issued


def _execute_all(issued, source_factory):
    return tuple(
        execute_test_only_workload(
            issued=item, source_factory=source_factory,
            host=HOST, purpose=PURPOSE,
        ) for item in issued
    )


def _refs(results):
    return tuple(sorted(
        {ref for result in results for receipt in result.receipts
         for ref in receipt.result_refs},
        key=lambda ref: ref.key,
    ))


def test_r91_partial_resume_matches_uninterrupted_without_rerun(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    uninterrupted = _execute_all(
        issued, lambda _ref: bundle.physical_stream)
    first = execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    checkpoint = capture_joined_checkpoint((first,))
    calls = {"count": 0}
    def counted(_ref):
        calls["count"] += 1
        return bundle.physical_stream
    resumed = resume_joined_workloads(
        workloads=issued, source_factory=counted,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    assert len(resumed.completed_results) == 1
    assert len(resumed.resumed_results) == len(issued) - 1
    assert calls["count"] == len(issued) - 1
    assert resumed.output_refs == _refs(uninterrupted)
    assert len(resumed.receipt_materials) == sum(
        len(result.receipts) for result in uninterrupted)
    # Completed workload is not executed twice.
    assert resumed.completed_results[0].decision_ref == issued[0].record.decision_ref


def test_r91_revoked_and_wrong_source_refuse_before_native(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    first = execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    checkpoint = capture_joined_checkpoint((first,))
    revoked = replace(
        issued[1], record=replace(issued[1].record, currentness="REVOKED"),
    )
    with pytest.raises(WorkloadAdmissionError):
        resume_joined_workloads(
            workloads=(issued[0], revoked), source_factory=lambda _ref: bundle.physical_stream,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
        )
    bad_stream = replace(bundle.physical_stream, source_sha256="f" * 64)
    with pytest.raises(WorkloadAdmissionError):
        resume_joined_workloads(
            workloads=(issued[0], issued[1]), source_factory=lambda _ref: bad_stream,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
        )


def test_r91_cold_fresh_process_resume_with_checkpoint(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    uninterrupted = _execute_all(
        issued, lambda _ref: bundle.physical_stream)
    first = execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    checkpoint = capture_joined_checkpoint((first,))
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(checkpoint.material(), sort_keys=True))
    source_path = tmp_path / "r91_r04.sav"
    code = """
import json, sys
from rawlsing_next.pre553_issued_workload import (
    restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_universal_workload import compile_universal_workload
from pathlib import Path
from rawlsing_next.tests.test_universal_source_projection import load_s3
bundle = load_s3(Path(sys.argv[1]))
compilation = compile_universal_workload(
    bundle=bundle, as_of=sys.argv[3], host=sys.argv[4], purpose=sys.argv[5])
issued = tuple(item.issued for item in compilation.compiled if item.issued is not None)
checkpoint = restore_joined_checkpoint(
    json.loads(open(sys.argv[2], encoding="utf-8").read()),
    expected_checkpoint_ref=sys.argv[6])
result = resume_joined_workloads(
    workloads=issued, source_factory=lambda _ref: bundle.physical_stream,
    host=sys.argv[4], purpose=sys.argv[5], checkpoint=checkpoint,
    expected_checkpoint_ref=sys.argv[6])
print(json.dumps({
    "completed": len(result.completed_results),
    "resumed": len(result.resumed_results),
    "output_refs": [ref.as_dict() for ref in result.output_refs],
}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code, str(source_path), str(checkpoint_path),
         AS_OF, HOST, PURPOSE, checkpoint.checkpoint_hash],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    child = json.loads(proc.stdout)
    assert child["completed"] == 1
    assert child["resumed"] == len(issued) - 1
    assert tuple(
        (ref["kind"], ref["object_id"], ref["content_hash"])
        for ref in child["output_refs"]
    ) == tuple(
        (ref.kind, ref.object_id, ref.content_hash)
        for ref in _refs(uninterrupted)
    )


def test_r91_actual_r03_governed_discovery_capture_and_retained_facts(tmp_path):
    from rawlsing_next.tests.test_universal_workload import (
        _frontier_bundle, _frontier_fixture,
    )
    from rawlsing_next.pre553_universal_workload import (
        compile_governed_frontier, execute_governed_frontier,
    )
    bundle, _ = _frontier_bundle(tmp_path / "r91_governed.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    governed = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    native_execution = governed.native_execution
    checkpoint = capture_joined_checkpoint(
        (native_execution,),
        source_sha256_by_decision={
            native_execution.decision_ref.key: compilation.issued.record.source_sha256
        },
    )
    pin = checkpoint.checkpoint_hash
    restored = restore_joined_checkpoint(
        checkpoint.material(), expected_checkpoint_ref=pin)
    resumed = resume_joined_workloads(
        workloads=(compilation.issued,), source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=restored,
        expected_checkpoint_ref=pin,
    )
    retained = resumed.completed_results[0]
    original_facts = tuple(fact.ref for fact in native_execution.native_result.empirical_facts)
    retained_facts = tuple(fact.ref for fact in retained.native_result.empirical_facts)
    assert retained_facts == original_facts
    assert retained.manifest.manifest_hash == native_execution.manifest.manifest_hash
    assert retained.decision_ref == native_execution.decision_ref
    with pytest.raises(WorkloadAdmissionError, match="PIN_MISMATCH|HASH_MISMATCH"):
        restore_joined_checkpoint(
            checkpoint.material(), expected_checkpoint_ref="f" * 64)


def test_r91_partial_multiunit_native_prefix_resume(tmp_path):
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
    from rawlsing_next.pre553_issued_workload import (
        IssuedWorkloadRecord, NativeWorkload, execute_issued_workload,
        operation_jobs,
    )
    from rawlsing_next.pre553_native_workload_binding import (
        OperationFixture, TestOnlyDecisionResolver, TestOnlyIssuedWorkload,
        build_projection_catalog,
    )
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
    bundle, issued = _issued_workloads(tmp_path)
    first, second = issued[0], issued[1]
    catalogs = []
    for item, variable, value in (
        (first, "SCORE", "0"), (second, "SCORE", "1"),
    ):
        fixture = OperationFixture(
            fixture_id="R91-PARTIAL-" + variable + value,
            target_variable_code=variable, response_value=value)
        catalog, request = build_projection_catalog(
            bundle=bundle, operation=fixture, as_of=AS_OF)
        catalogs.append((catalog, request))
    authorities = {}
    predicates = {}
    queries = {}
    for catalog, _ in catalogs:
        for obj in catalog.authorities:
            authorities[obj.authority_ref.key] = obj
        for obj in catalog.predicates:
            predicates[obj.ref.key] = obj
        for obj in catalog.queries:
            queries[obj.ref.key] = obj
    runtime_catalog = RuntimeObjectCatalog(
        authorities=tuple(authorities.values()),
        predicates=tuple(predicates.values()),
        queries=tuple(queries.values()),
        discovery_authorities=(),
    )
    requests = tuple(request for _, request in catalogs)
    base = first.workload
    workload = NativeWorkload(
        decision_ref=ExactRef("R91_PARTIAL_DECISION", "urn:test:r91:partial", "9" * 64),
        source_factory_ref=base.source_factory_ref,
        descriptor=base.descriptor, projection=base.projection,
        catalog=runtime_catalog, requests=requests, discoveries=(),
        original_u_root=base.original_u_root,
        expected_frontier_root=base.expected_frontier_root,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=first.record.source_permission_ref,
        scientific_permission_refs=first.record.scientific_permission_refs,
        host=HOST, purpose=PURPOSE,
        source_sha256=first.record.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(requests, ()),
        currentness="CURRENT_GRANTED", scope=first.record.scope,
    )
    multi = TestOnlyIssuedWorkload(
        workload=workload, record=record, descriptor=first.descriptor,
        envelope_sha256=record.envelope_sha256)
    resolver = TestOnlyDecisionResolver(record)
    partial = execute_issued_workload(
        workload, resolver, source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    assert len(partial.receipts) == 1
    assert len(partial.manifest.units) == 2
    checkpoint = capture_joined_checkpoint((partial,))
    assert checkpoint.entries[0].state == "PARTIAL"
    resumed = resume_joined_workloads(
        workloads=(multi,), source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    assert len(resumed.resumed_results) == 1
    final = resumed.resumed_results[0]
    assert len(final.receipts) == 2
    assert final.outputs_by_unit and len(final.outputs_by_unit) == 2
    uninterrupted = execute_issued_workload(
        workload, resolver, source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    assert resumed.output_refs == tuple(sorted(
        {ref for receipt in uninterrupted.receipts for ref in receipt.result_refs},
        key=lambda ref: ref.key))
    assert len({receipt.unit_ref.key for receipt in final.receipts}) == 2
    assert all(receipt.state == "COMPLETED" for receipt in final.receipts)


def test_r93_restored_outputs_preserve_query_and_discovery_identity(tmp_path):
    from dataclasses import FrozenInstanceError
    from rawlsing_next._pre553_query_common import QueryExecutionResult
    from rawlsing_next.pre553_issued_workload import RetainedDiscoveryResultView
    from rawlsing_next.tests.test_universal_workload import (
        _frontier_bundle, _frontier_fixture,
    )
    from rawlsing_next.pre553_universal_workload import (
        compile_governed_frontier, execute_governed_frontier,
    )
    bundle, issued = _issued_workloads(tmp_path)
    first = execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )
    checkpoint = capture_joined_checkpoint((first,))
    restored = resume_joined_workloads(
        workloads=(issued[0],), source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    output = restored.completed_results[0].native_outputs[0]
    assert isinstance(output, QueryExecutionResult)
    assert output.query_ref == first.native_outputs[0].query_ref
    assert output.facts == first.native_outputs[0].facts
    assert output.release_refs == first.native_outputs[0].release_refs

    governed_bundle, _ = _frontier_bundle(tmp_path / "r93_governed.sav")
    inventory, policy, frontier = _frontier_fixture(governed_bundle)
    compilation = compile_governed_frontier(
        bundle=governed_bundle, inventory=inventory, policy=policy,
        frontier=frontier, as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    governed = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: governed_bundle.physical_stream,
    )
    native = governed.native_execution
    checkpoint = capture_joined_checkpoint(
        (native,),
        source_sha256_by_decision={
            native.decision_ref.key: compilation.issued.record.source_sha256
        },
    )
    resumed = resume_joined_workloads(
        workloads=(compilation.issued,),
        source_factory=lambda _ref: governed_bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    view = resumed.completed_results[0].native_result
    assert isinstance(view, RetainedDiscoveryResultView)
    assert view.evaluated_frontier_ref == native.native_result.evaluated_frontier_ref
    assert view.replay_ref == native.native_result.replay_ref
    assert view.empirical_fact_refs == native.native_result.empirical_fact_refs
    assert view.receipts == native.native_result.receipts
    with pytest.raises(FrozenInstanceError):
        view.candidate_count = 0
