"""Independent G5 full-parity witness for the five-reader delivery.

This harness intentionally compares complete native result material, not just
receipt/result counts.  It uses only the existing test-only sourcefree fixture
and the author's public owners.  No product code is edited.
"""
from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path
import sys
from types import SimpleNamespace

from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint,
    execute_issued_workload,
    material,
    resume_joined_workloads,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    HOST, PURPOSE, CurrentIssuer,
)
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for,
    _fixture,
    _fixture_bundle,
)


def _canon(value):
    return material(value)


def _paths_equal(left, right):
    return _canon(left) == _canon(right)


def _compare(label, left, right):
    return {
        "label": label,
        "equal": _canon(left) == _canon(right),
        "left": _canon(left),
        "right": _canon(right),
    }


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_parity.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    proofroot.mkdir(parents=True, exist_ok=True)
    tmp = proofroot / "saved-parity"
    tmp.mkdir(parents=True, exist_ok=True)
    path, oracle_bundle, saved_bundle, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    oracle = execute_issued_workload(
        issued.workload, issuer,
        source_factory=lambda _ref: oracle_bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    saved = execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission,
        source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    comparisons = [
        _compare("manifest", oracle.manifest, saved.manifest),
        _compare("receipts", oracle.receipts, saved.receipts),
        _compare("native_outputs", oracle.native_outputs, saved.native_outputs),
        _compare("output_refs", oracle.output_refs, saved.output_refs),
        _compare("summary", oracle.summary, saved.summary),
        _compare("routes", oracle.route_results, saved.route_results),
        _compare("envelope_sha256", oracle.envelope_sha256, saved.envelope_sha256),
        _compare("decision_ref", oracle.decision_ref, saved.decision_ref),
        _compare("scope", oracle.scope, saved.scope),
        _compare("source_sha256", oracle.source_sha256, saved.source_sha256),
        _compare("outputs_by_unit", oracle.outputs_by_unit, saved.outputs_by_unit),
    ]

    binding = admission.binding_receipt()
    completed = capture_joined_checkpoint((saved,), saved_binding=binding)
    resumed = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=completed,
        expected_checkpoint_ref=completed.checkpoint_hash,
        allow_test_only=True,
    )
    completed_cmp = _compare(
        "completed_result", saved, resumed.completed_results[0],
    )
    completed_outputs_cmp = _compare(
        "completed_outputs", saved.native_outputs,
        resumed.completed_results[0].native_outputs,
    )
    completed_receipts_cmp = _compare(
        "completed_receipts", saved.receipts,
        resumed.completed_results[0].receipts,
    )

    partial = execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission,
        source_factory=None,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    partial_ckpt = capture_joined_checkpoint((partial,), saved_binding=binding)
    partial_resumed = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=partial_ckpt,
        expected_checkpoint_ref=partial_ckpt.checkpoint_hash,
        allow_test_only=True,
    )
    partial_cmp = _compare(
        "partial_resume_result", saved, partial_resumed.resumed_results[0],
    )
    partial_outputs_cmp = _compare(
        "partial_resume_outputs", saved.native_outputs,
        partial_resumed.resumed_results[0].native_outputs,
    )
    partial_receipts_cmp = _compare(
        "partial_resume_receipts", saved.receipts,
        partial_resumed.resumed_results[0].receipts,
    )

    empty = capture_joined_checkpoint((), saved_binding=binding)
    absent_resumed = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=empty,
        expected_checkpoint_ref=empty.checkpoint_hash,
        allow_test_only=True,
    )
    absent_cmp = _compare(
        "absent_resume_result", saved, absent_resumed.resumed_results[0],
    )
    absent_outputs_cmp = _compare(
        "absent_resume_outputs", saved.native_outputs,
        absent_resumed.resumed_results[0].native_outputs,
    )
    absent_receipts_cmp = _compare(
        "absent_resume_receipts", saved.receipts,
        absent_resumed.resumed_results[0].receipts,
    )

    report = {
        "schema": "PYAT991_ALL_SEVEN_G5_INDEPENDENT_PARITY@1",
        "fixture": "S1-D S3 sourcefree synthetic 4 respondents/2 occasions",
        "normal": comparisons,
        "completed": [
            completed_cmp, completed_outputs_cmp, completed_receipts_cmp,
        ],
        "partial": [
            partial_cmp, partial_outputs_cmp, partial_receipts_cmp,
        ],
        "absent": [
            absent_cmp, absent_outputs_cmp, absent_receipts_cmp,
        ],
        "all_compared_equal": all(
            row["equal"]
            for section in (
                comparisons,
                (completed_cmp, completed_outputs_cmp, completed_receipts_cmp),
                (partial_cmp, partial_outputs_cmp, partial_receipts_cmp),
                (absent_cmp, absent_outputs_cmp, absent_receipts_cmp),
            )
            for row in section
        ),
    }
    (proofroot / "independent_parity.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps({
        "all_compared_equal": report["all_compared_equal"],
        "normal": [
            {"label": row["label"], "equal": row["equal"]}
            for row in comparisons
        ],
        "completed": [
            {"label": row["label"], "equal": row["equal"]}
            for row in (completed_cmp, completed_outputs_cmp, completed_receipts_cmp)
        ],
        "partial": [
            {"label": row["label"], "equal": row["equal"]}
            for row in (partial_cmp, partial_outputs_cmp, partial_receipts_cmp)
        ],
        "absent": [
            {"label": row["label"], "equal": row["equal"]}
            for row in (absent_cmp, absent_outputs_cmp, absent_receipts_cmp)
        ],
    }, indent=2, sort_keys=True))
    return 0 if report["all_compared_equal"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
