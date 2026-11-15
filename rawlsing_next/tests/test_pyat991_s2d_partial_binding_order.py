"""G5 PARTIAL binding-order regression.

A coherently rehashed forged saved binding must refuse before any protected
PARTIAL checkpoint receipt/output restore, just as the COMPLETED branch does.
The positive PARTIAL prefix/final-output conservation and ABSENT path remain
unchanged.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint,
    execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for,
    _fixture,
)


def _forged(checkpoint, binding):
    forged = replace(
        checkpoint,
        saved_binding=replace(binding, manifest_sha256="0" * 64),
    )
    return replace(
        forged, checkpoint_hash=issued_module._checkpoint_content_hash(forged),
    )


def _resume_with_restore_spy(issued, issuer, admission, checkpoint):
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


def test_forged_partial_binding_refuses_before_restore(tmp_path):
    """RED before the ordering repair: 2 protected restores; GREEN: zero."""

    path, oracle_bundle, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    full = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
        max_units=1,
    )
    binding = admission.binding_receipt()
    completed = capture_joined_checkpoint((full,), saved_binding=binding)
    partial_cp = capture_joined_checkpoint((partial,), saved_binding=binding)
    completed_forged = _forged(completed, binding)
    partial_forged = _forged(partial_cp, binding)
    completed_calls, completed_error = _resume_with_restore_spy(
        issued, issuer, admission, completed_forged,
    )
    partial_calls, partial_error = _resume_with_restore_spy(
        issued, issuer, admission, partial_forged,
    )
    assert completed_calls == 0
    assert partial_calls == 0
    assert "JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH" in partial_error
    # Legitimate partial prefix still resumes to the same final native outputs.
    legitimate = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=partial_cp,
        expected_checkpoint_ref=partial_cp.checkpoint_hash,
        allow_test_only=True,
    )
    assert legitimate.resumed_results
    assert tuple(sorted(ref.key for ref in legitimate.output_refs)) == tuple(
        sorted(ref.key for ref in full.output_refs)
    )


def test_forged_partial_binding_and_revoked_current_leave_no_restore(
    tmp_path,
):
    _, _, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    partial = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
        max_units=1,
    )
    forged = _forged(
        capture_joined_checkpoint(
            (partial,), saved_binding=admission.binding_receipt(),
        ),
        admission.binding_receipt(),
    )
    issuer.revoke()
    calls, error = _resume_with_restore_spy(
        issued, issuer, admission, forged,
    )
    assert calls == 0
    assert error is not None
