#!/usr/bin/env python3
"""Independent RED witness: R3 Batch QUERY is constructed, not compiler-issued.

Run inside an isolated copy of the candidate checkout:
  PYTHONPATH=<proof-copy>:<R3 harness dir> python3 -B witness_issuer_binding.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
r3 = ROOT / "WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/issued_batch_f4_r3"
sys.path.insert(0, str(r3))
import harness  # noqa: E402  (return-local harness; product imports from checkout)

captured = []
real_compile = harness.compile_governed_frontier

def capture_compile(*args, **kwargs):
    compilation = real_compile(*args, **kwargs)
    captured.append(compilation)
    return compilation

harness.compile_governed_frontier = capture_compile

root = Path(tempfile.mkdtemp(prefix="pyat997-issuer-witness-")).resolve()
fixture = harness._make_fixture(
    root / "fixture",
    [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
     (1, 0, 1, 3), (0, 0, 1, 4)],
)
bundle = harness._materialize(root / "stage", fixture)
assert len(captured) == 1, captured
compiler = captured[0]
manual = bundle["issued"]
manual_compilation = bundle["compilation"]
assert manual_compilation.issued is manual
assert compiler.issued is not manual
assert compiler.issued.record is not manual.record

query_ref = bundle["joint_query"].ref.key
plan_query_matches = []
for record in compiler.plan.records:
    refs = []
    for raw in record.query_refs:
        if isinstance(raw, dict):
            raw = {key: raw[key] for key in ("kind", "object_id", "content_hash")}
        from rawlsing_next.pre553_empirical_objects import exact_ref
        refs.append(exact_ref(raw).key)
    if query_ref in refs:
        plan_query_matches.append({
            "operation_id": record.operation_id,
            "status": record.status,
            "disposition": compiler.operation_dispositions.get(record.operation_id),
            "claim_class": compiler.operation_claim_classes.get(record.operation_id),
        })

out = {
    "checkout": str(ROOT),
    "compiler_issued": {
        "decision_ref": compiler.issued.record.decision_ref.key,
        "workload_requests": len(compiler.issued.workload.requests),
        "workload_discoveries": len(compiler.issued.workload.discoveries),
        "record_expected_jobs": [list(x) for x in compiler.issued.record.expected_jobs],
        "scope": compiler.issued.record.scope,
    },
    "manual_r3_issued": {
        "decision_ref": manual.record.decision_ref.key,
        "workload_requests": len(manual.workload.requests),
        "workload_discoveries": len(manual.workload.discoveries),
        "record_expected_jobs": [list(x) for x in manual.record.expected_jobs],
        "scope": manual.record.scope,
        "same_compiler_record": manual.record == compiler.issued.record,
        "same_compiler_workload": manual.workload == compiler.issued.workload,
    },
    "replaced_compilation": {
        "same_compiler_compilation": manual_compilation == compiler,
        "its_issued_is_manual": manual_compilation.issued is manual,
    },
    "joint_query_ref": query_ref,
    "joint_query_in_compiler_plan": plan_query_matches,
    "f4_like_frontier_operations": [
        {
            "operation_id": op.op_id,
            "disposition": op.disposition,
            "claim_class": op.claim_class,
            "measure_kind": op.measure_kind,
            "targets": [key.item_id for key in op.targets],
            "conditions": len(op.conditions),
        }
        for op in fixture["frontier"].operations
        if {key.item_id for key in op.targets} == {"q101", "q102", "q103"}
        and op.measure_kind == "SAMPLE" and not op.conditions
    ],
    "compiler_has_query_unit": len(compiler.issued.workload.requests) > 0,
    "manual_has_query_unit": len(manual.workload.requests) > 0,
    "red": (
        len(compiler.issued.workload.requests) == 0
        and len(manual.workload.requests) > 0
        and manual.record != compiler.issued.record
    ),
    "rightful_owner_repair_path": (
        "Do not replace compilation.issued. Either execute only the actual "
        "compiler-issued DISCOVERY workload and mark Batch QUERY NOT_ISSUED, or "
        "obtain an owner-level R03/issuer change that emits the exact QUERY job "
        "for the eligible operation with its own decision/envelope, then rebuild "
        "the postconsumer join against that unchanged compiler record."
    ),
}
print(json.dumps(out, indent=2, sort_keys=True, default=str))
raise SystemExit(1 if out["red"] else 0)
