#!/usr/bin/env python3
"""Independent COMPLETED saved-checkpoint witness on the same Q2 estate.

The R3 native proof covers NORMAL/PARTIAL/ABSENT but not an explicit COMPLETED
checkpoint.  This witness reuses the same Q2 estate, admission, issued workload
and actual existing resume API; it does not modify product code.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
r3 = ROOT / "WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/issued_batch_f4_r3"
sys.path.insert(0, str(r3))
import harness  # noqa: E402
from rawlsing_next.pre553_issued_workload import (  # noqa: E402
    capture_joined_checkpoint, execute_issued_workload, resume_joined_workloads,
)

root = Path(tempfile.mkdtemp(prefix="pyat997-completed-witness-")).resolve()
fixture = harness._make_fixture(
    root / "fixture",
    [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
     (1, 0, 1, 3), (0, 0, 1, 4)],
)
bundle = harness._materialize(root / "stage", fixture)
admission = bundle["admission"]
resolver = bundle["resolver"]
issued = bundle["issued"]

def forbidden_source(_ref):
    raise AssertionError("saved resume called source factory")

normal = execute_issued_workload(
    issued.workload, resolver,
    saved_admission_factory=lambda: admission,
    source_factory=forbidden_source,
    host=harness.HOST, purpose=harness.PURPOSE, allow_test_only=True,
)
binding = admission.binding_receipt()
checkpoint = capture_joined_checkpoint((normal,), saved_binding=binding)
assert checkpoint.entries[0].state == "COMPLETED"
completed = resume_joined_workloads(
    workloads=(issued,), resolver=resolver,
    saved_admission_factory=lambda: admission, source_factory=None,
    host=harness.HOST, purpose=harness.PURPOSE,
    checkpoint=checkpoint, expected_checkpoint_ref=checkpoint.checkpoint_hash,
    allow_test_only=True,
)
normal_refs = tuple(sorted(ref.key for ref in normal.output_refs))
completed_refs = tuple(sorted(ref.key for ref in completed.output_refs))
out = {
    "checkpoint_state": checkpoint.entries[0].state,
    "normal_states": [r.state for r in normal.receipts],
    "normal_output_refs": len(normal_refs),
    "completed_results": len(completed.completed_results),
    "resumed_results": len(completed.resumed_results),
    "completed_output_refs": len(completed_refs),
    "output_refs_equal": completed_refs == normal_refs,
    "source_opens": admission.binding_receipt().source_opens,
    "full_c11_repository_builds": admission.binding_receipt().full_c11_repository_builds,
    "passed": bool(completed.completed_results) and completed_refs == normal_refs,
}
print(json.dumps(out, indent=2, sort_keys=True))
