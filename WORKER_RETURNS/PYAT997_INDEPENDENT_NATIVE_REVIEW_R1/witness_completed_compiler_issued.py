#!/usr/bin/env python3
"""COMPLETED checkpoint on the actual compiler-issued discovery workload.

Uses the patched test helper only to build the same Q2 persisted estate; the
issued workload here is compilation.issued (0 QUERY requests, 1 DISCOVERY).
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_issued_workload import (  # noqa: E402
    capture_joined_checkpoint, execute_issued_workload, resume_joined_workloads,
)
from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (  # noqa: E402
    _NATIVE_HOST, _NATIVE_PURPOSE, _full,
)

root = Path(tempfile.mkdtemp(prefix="pyat997-completed-compiler-")).resolve()
handoff, estate, admission, compilation, resolver, sink = _full(root / "full")
workload = compilation.issued.workload
assert len(workload.requests) == 0
assert len(workload.discoveries) == 1
assert tuple(compilation.issued.record.expected_jobs) == (
    ("DISCOVERY", workload.discoveries[0].key, ""),
)

def forbidden_source(_ref):
    raise AssertionError("saved resume called source factory")

normal = execute_issued_workload(
    workload, resolver, saved_admission_factory=lambda: admission,
    source_factory=forbidden_source, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
    allow_test_only=True,
)
checkpoint = capture_joined_checkpoint(
    (normal,), saved_binding=admission.binding_receipt())
assert checkpoint.entries[0].state == "COMPLETED"
completed = resume_joined_workloads(
    workloads=(compilation.issued,), resolver=resolver,
    saved_admission_factory=lambda: admission, source_factory=None,
    host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
    checkpoint=checkpoint, expected_checkpoint_ref=checkpoint.checkpoint_hash,
    allow_test_only=True,
)
normal_refs = tuple(sorted(ref.key for ref in normal.output_refs))
completed_refs = tuple(sorted(ref.key for ref in completed.output_refs))
out = {
    "compiler_issued_query_requests": len(workload.requests),
    "compiler_issued_discoveries": len(workload.discoveries),
    "record_expected_jobs": [list(x) for x in compilation.issued.record.expected_jobs],
    "normal_states": [r.state for r in normal.receipts],
    "checkpoint_state": checkpoint.entries[0].state,
    "completed_results": len(completed.completed_results),
    "resumed_results": len(completed.resumed_results),
    "normal_output_refs": len(normal_refs),
    "completed_output_refs": len(completed_refs),
    "output_refs_equal": completed_refs == normal_refs,
    "source_opens": admission.binding_receipt().source_opens,
    "full_c11_repository_builds": admission.binding_receipt().full_c11_repository_builds,
    "passed": bool(completed.completed_results) and completed_refs == normal_refs,
}
print(json.dumps(out, indent=2, sort_keys=True))
