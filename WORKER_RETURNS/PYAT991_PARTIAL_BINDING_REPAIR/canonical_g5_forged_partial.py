"""Decisive G5 counterexample: forged saved binding on a genuinely PARTIAL checkpoint.

The completed branch validates the saved binding before parsing retained output.
The partial branch restores the prior receipts/outputs first and only then checks
the binding.  This harness measures the protected-output restore calls before the
refusal and includes a completed control.
"""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import sys

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import _admission_for, _fixture


def _forged(checkpoint, binding):
    forged = replace(
        checkpoint,
        saved_binding=replace(binding, manifest_sha256="0" * 64),
    )
    return replace(
        forged, checkpoint_hash=issued_module._checkpoint_content_hash(forged),
    )


def _resume(issued, issuer, admission, checkpoint):
    calls = {"n": 0}
    original = issued_module._restore_output_material

    def spy(row):
        calls["n"] += 1
        return original(row)

    issued_module._restore_output_material = spy
    error = None
    try:
        issued_module.resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        issued_module._restore_output_material = original
    return calls["n"], error


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: forged_partial_binding.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "forged-binding-witness"
    tmp.mkdir(parents=True, exist_ok=True)
    path, oracle_bundle, saved_bundle, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    full = issued_module.execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = issued_module.execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    binding = admission.binding_receipt()
    completed = issued_module.capture_joined_checkpoint(
        (full,), saved_binding=binding,
    )
    partial_checkpoint = issued_module.capture_joined_checkpoint(
        (partial,), saved_binding=binding,
    )
    assert completed.entries[0].state == "COMPLETED"
    assert partial_checkpoint.entries[0].state == "PARTIAL"
    completed_forged = _forged(completed, binding)
    partial_forged = _forged(partial_checkpoint, binding)
    completed_calls, completed_error = _resume(
        issued, issuer, admission, completed_forged,
    )
    partial_calls, partial_error = _resume(
        issued, issuer, admission, partial_forged,
    )
    evidence = {
        "schema": "PYAT991_ALL_SEVEN_G5_FORGED_PARTIAL_BINDING@1",
        "fixture": "S1-D/S3 sourcefree synthetic 4 respondents/2 occasions",
        "completed_control": {
            "entry_state": completed_forged.entries[0].state,
            "restore_output_calls_before_refusal": completed_calls,
            "error": completed_error,
        },
        "partial_counterexample": {
            "entry_state": partial_forged.entries[0].state,
            "restore_output_calls_before_refusal": partial_calls,
            "error": partial_error,
        },
        "defect_reproduced": (
            partial_forged.entries[0].state == "PARTIAL"
            and partial_calls > 0
            and "SAVED_BINDING_MISMATCH" in (partial_error or "")
            and completed_calls == 0
        ),
        "expected": (
            "forged coherently rehashed saved binding must refuse before any "
            "protected retained output/receipt restore for both COMPLETED and PARTIAL"
        ),
    }
    (proofroot / "forged_partial_binding.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if evidence["defect_reproduced"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
