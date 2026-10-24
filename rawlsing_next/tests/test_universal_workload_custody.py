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
        )
    bad_stream = replace(bundle.physical_stream, source_sha256="f" * 64)
    with pytest.raises(WorkloadAdmissionError):
        resume_joined_workloads(
            workloads=(issued[0], issued[1]), source_factory=lambda _ref: bad_stream,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
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
    json.loads(open(sys.argv[2], encoding="utf-8").read()))
result = resume_joined_workloads(
    workloads=issued, source_factory=lambda _ref: bundle.physical_stream,
    host=sys.argv[4], purpose=sys.argv[5], checkpoint=checkpoint)
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
         AS_OF, HOST, PURPOSE],
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
