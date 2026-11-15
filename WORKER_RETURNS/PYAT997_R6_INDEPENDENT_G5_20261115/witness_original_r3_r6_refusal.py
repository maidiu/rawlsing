#!/usr/bin/env python3
"""Original R3 manual QUERY + matching resolver through the actual R6 join.

This is the independent G5 counterexample run: it replays the exact historical
R3 manual q101/q102/q103 QUERY construction (from 8b03) against the R6
production join and expects R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT with zero
positive attribution.  It also exercises the actual manual native Batch first
consumer first, so the refusal is not merely a pre-execution type check.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
EVID = ROOT / "WORKER_RETURNS/PYAT997_R6_INDEPENDENT_G5_20261115/evidence"
sys.path.insert(0, str(EVID / "r3_harness_8b03"))
sys.path.insert(0, str(ROOT))

import harness  # R3 exact 8b03 harness
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)

captured = []
real_compile = harness.compile_governed_frontier

def capture(*args, **kwargs):
    compilation = real_compile(*args, **kwargs)
    captured.append(compilation)
    return compilation

harness.compile_governed_frontier = capture
root = Path(tempfile.mkdtemp(prefix="pyat997-r6-r3-attack-")).resolve()
fixture = harness._make_fixture(
    root / "fixture",
    [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
     (1, 0, 1, 3), (0, 0, 1, 4)],
)
bundle = harness._materialize(root / "stage", fixture)
compiler = captured[0]
manual = bundle["issued"]
assert compiler.issued is not manual
assert compiler.issued.record is not manual.record
assert len(compiler.issued.workload.requests) == 0
assert len(compiler.issued.workload.discoveries) == 1
assert len(manual.workload.requests) == 1
assert len(manual.workload.discoveries) == 1
query = bundle["joint_query"]
predicate = bundle["predicate"]
discovery = bundle["discovery"]
admission = bundle["admission"]
issued = bundle["issued"]
query_unit = BatchUnitSpec(
    "QUERY", query.ref, (admission.release_ref,),
    (issued.record.decision_ref,),
)
discovery_unit = BatchUnitSpec(
    "DISCOVERY", discovery.ref, (admission.release_ref,),
    (issued.record.decision_ref,),
)
manifest = BatchManifest((query_unit, discovery_unit))
manual_batch = execute_saved_batch(
    admission, manifest=manifest,
    predicate_ref_by_query={query.ref.key: predicate.ref},
)
assert all(r.state == "COMPLETED" for r in manual_batch.receipts)
assert len(manual_batch.receipts) == 2

f4_like = [
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
]

def attempt(runner):
    try:
        joined = join_saved_source_operation_fates(
            handoff=bundle["handoff"], estate_receipt=bundle["estate"],
            admission=admission, compilation=bundle["compilation"],
            workload=issued.workload, resolver=bundle["resolver"],
            host=harness.HOST, purpose=harness.PURPOSE, runner=runner,
        )
        return {"refused": False, "positive": joined.audit.get(
            "positive_native_linked_operations")}
    except SourceReceiptJoinError as exc:
        return {"refused": True, "error": str(exc),
                "positive_attribution": 0}

empty_runner = BatchExecutionRunner(
    manifest=manifest, repository=admission, saved_mode=True)
empty_join = attempt(empty_runner)
executed_join = attempt(manual_batch)

accepted = (not empty_join["refused"] or not executed_join["refused"]
            or "R03_COMPILER_ISSUED_JOB_OR_PLAN_DRIFT"
            not in (empty_join.get("error", "") + executed_join.get("error", "")))
out = {
    "source": "original R3 8b03 harness manual q101/q102/q103 QUERY",
    "compiler_issued": {
        "requests": len(compiler.issued.workload.requests),
        "discoveries": len(compiler.issued.workload.discoveries),
        "expected_jobs": [list(x) for x in compiler.issued.record.expected_jobs],
    },
    "manual_r3_issued": {
        "requests": len(issued.workload.requests),
        "discoveries": len(issued.workload.discoveries),
        "expected_jobs": [list(x) for x in issued.record.expected_jobs],
        "matching_resolver": type(bundle["resolver"]).__name__,
        "same_compiler_record": issued.record == compiler.issued.record,
    },
    "joint_query_in_compiler_plan": [],
    "f4_like_operation_count": len(f4_like),
    "f4_like_dispositions": sorted({x["disposition"] for x in f4_like}),
    "f4_like_claim_classes": sorted({x["claim_class"] for x in f4_like}),
    "manual_batch": {
        "units": len(manual_batch.receipts),
        "states": [r.state for r in manual_batch.receipts],
        "executed_native_query_and_discovery": True,
    },
    "empty_runner_join": empty_join,
    "executed_runner_join": executed_join,
    "accepted": accepted,
    "passed": not accepted,
}
print(json.dumps(out, indent=2, sort_keys=True))
raise SystemExit(0 if out["passed"] else 2)
