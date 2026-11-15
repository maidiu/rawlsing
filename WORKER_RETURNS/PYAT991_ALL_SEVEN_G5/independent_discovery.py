"""Independent G5 integrated NORMAL+Batch witness including an actual I05.

The author's five-reader test workload contains two I03 queries and no
discovery.  This harness builds the existing S1-D same-source issued workload
with one I03 query and one I05 discovery, then compares the saved owner path to
the normal source-backed owner on the same exact fixture.  No product edit.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, NativeWorkload,
    capture_joined_checkpoint, execute_issued_workload, material,
    operation_jobs, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, TestOnlyIssuedWorkload,
)
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, compile_universal_workload,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for, _saved_estate,
)
from rawlsing_next.tests.test_universal_workload import (
    _frontier_bundle, _frontier_fixture,
)


def _merge_refs(values):
    return tuple({value.ref.key: value for value in values}[key] for key in sorted(
        {value.ref.key for value in values}
    ))


def _merge_authority_refs(values):
    return tuple({value.authority_ref.key: value for value in values}[key] for key in sorted(
        {value.authority_ref.key for value in values}
    ))


def _compare(label, left, right):
    return {
        "label": label,
        "equal": material(left) == material(right),
        "left": material(left),
        "right": material(right),
    }


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_discovery.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "discovery-witness"
    tmp.mkdir(parents=True, exist_ok=True)
    bundle, _ = _frontier_bundle(tmp / "same-source.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    governed = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of="2026-10-24", host=HOST, purpose=PURPOSE,
    )
    universal = compile_universal_workload(
        bundle=bundle, as_of="2026-10-24", host=HOST, purpose=PURPOSE,
    )
    query_issued = universal.compiled[0].issued
    base = query_issued.workload
    discovery = governed.issued.workload
    catalog = RuntimeObjectCatalog(
        authorities=_merge_authority_refs(
            base.catalog.authorities + discovery.catalog.authorities
        ),
        predicates=_merge_refs(base.catalog.predicates + discovery.catalog.predicates),
        queries=_merge_refs(base.catalog.queries + discovery.catalog.queries),
        discovery_authorities=_merge_refs(
            base.catalog.discovery_authorities
            + discovery.catalog.discovery_authorities
        ),
    )
    workload = NativeWorkload(
        decision_ref=ExactRef(
            "TEST_ONLY_DECISION", "urn:test:s2d:discovery-five", "9" * 64,
        ),
        source_factory_ref=base.source_factory_ref,
        descriptor=base.descriptor, projection=base.projection,
        catalog=catalog,
        requests=base.requests, discoveries=discovery.discoveries,
        original_u_root=base.original_u_root,
        expected_frontier_root=base.expected_frontier_root,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=query_issued.record.source_permission_ref,
        scientific_permission_refs=query_issued.record.scientific_permission_refs,
        host=HOST, purpose=PURPOSE,
        source_sha256=query_issued.record.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(workload.requests, workload.discoveries),
        currentness="CURRENT_GRANTED", scope=query_issued.record.scope,
    )
    issued = TestOnlyIssuedWorkload(
        workload=workload, record=record,
        descriptor=query_issued.descriptor,
        envelope_sha256=record.envelope_sha256,
    )
    root, receipt = _saved_estate(tmp, bundle)
    issuer = TestOnlyDecisionResolver(record)
    admission = _admission_for(
        root, receipt, workload,
        lambda _roots: issuer.resolve_current(record.decision_ref) == record,
    )
    normal = execute_issued_workload(
        workload, issuer,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    saved = execute_issued_workload(
        workload, issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    normal_cmp = [
        _compare("manifest", normal.manifest, saved.manifest),
        _compare("receipts", normal.receipts, saved.receipts),
        _compare("native_outputs", normal.native_outputs, saved.native_outputs),
        _compare("output_refs_sorted", sorted(normal.output_refs, key=lambda r: r.key),
                 sorted(saved.output_refs, key=lambda r: r.key)),
        _compare("summary", normal.summary, saved.summary),
        _compare("route_results", normal.route_results, saved.route_results),
        _compare("outputs_by_unit", normal.outputs_by_unit, saved.outputs_by_unit),
    ]
    binding = admission.binding_receipt()
    full_ckpt = capture_joined_checkpoint((saved,), saved_binding=binding)
    completed = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=full_ckpt,
        expected_checkpoint_ref=full_ckpt.checkpoint_hash,
        allow_test_only=True,
    )
    completed_view = completed.completed_results[0]
    completed_cmp = [
        _compare("completed_outputs", saved.native_outputs, completed_view.native_outputs),
        _compare("completed_receipts", saved.receipts, completed_view.receipts),
        _compare("completed_output_refs_sorted",
                 sorted(saved.output_refs, key=lambda r: r.key),
                 sorted(completed_view.output_refs, key=lambda r: r.key)),
    ]
    partial = execute_issued_workload(
        workload, issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    partial_ckpt = capture_joined_checkpoint((partial,), saved_binding=binding)
    partial_resume = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=partial_ckpt,
        expected_checkpoint_ref=partial_ckpt.checkpoint_hash,
        allow_test_only=True,
    )
    partial_view = partial_resume.resumed_results[0]
    partial_cmp = [
        _compare("partial_outputs", saved.native_outputs, partial_view.native_outputs),
        _compare("partial_receipts", saved.receipts, partial_view.receipts),
        _compare("partial_output_refs_sorted",
                 sorted(saved.output_refs, key=lambda r: r.key),
                 sorted(partial_view.output_refs, key=lambda r: r.key)),
    ]
    report = {
        "schema": "PYAT991_ALL_SEVEN_G5_DISCOVERY_PARITY@1",
        "fixture": "S1-D same-source 12-row S1-D sourcefree, one I03 + one I05",
        "normal": normal_cmp,
        "completed": completed_cmp,
        "partial": partial_cmp,
        "all_relevant_equal": all(
            row["equal"] for row in (*normal_cmp, *completed_cmp, *partial_cmp)
        ),
        "normal_route_count": len(normal.route_results),
        "saved_route_count": len(saved.route_results),
    }
    (proofroot / "discovery_parity.json").write_text(
        json.dumps(report, indent=2, sort_keys=True, default=repr), encoding="utf-8",
    )
    print(json.dumps({
        "all_relevant_equal": report["all_relevant_equal"],
        "normal": [{"label": x["label"], "equal": x["equal"]} for x in normal_cmp],
        "completed": [{"label": x["label"], "equal": x["equal"]} for x in completed_cmp],
        "partial": [{"label": x["label"], "equal": x["equal"]} for x in partial_cmp],
        "normal_route_count": len(normal.route_results),
        "saved_route_count": len(saved.route_results),
    }, indent=2, sort_keys=True))
    return 0 if report["all_relevant_equal"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
