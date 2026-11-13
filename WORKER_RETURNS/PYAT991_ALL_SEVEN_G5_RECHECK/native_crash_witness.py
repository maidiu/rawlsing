"""Independent G4 native-boundary crash witness.

The author's probe kills a child that only JSON-loads a durable capsule before
native resume.  This witness instead kills the child *inside* actual saved
PARTIAL resume, after the native pending Batch receipt is recorded, and then
lets a fresh process resume the same caller-owned checkpoint.  No product code
is edited; the child monkeypatch is review-only.
"""
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys

from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint, execute_issued_workload,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for, _fixture, _fresh_process_capsule,
)


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: native_crash_witness.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "native-crash-witness"
    tmp.mkdir(parents=True, exist_ok=True)
    _, _, _, issued, root, receipt, issuer = _fixture(tmp)
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
    checkpoint = capture_joined_checkpoint(
        (partial,), saved_binding=admission.binding_receipt(),
    )
    assert checkpoint.entries[0].state == "PARTIAL"
    assert len(checkpoint.entries[0].receipt_materials) == 1
    capsule_path, base_child = _fresh_process_capsule(
        tmp, issued, admission, checkpoint, mode="partial",
    )
    # Kill only after the native pending receipt has been recorded inside the
    # actual PARTIAL resume.  The first record_receipt is the prior prefix from
    # checkpoint material; the second is the real pending native execution.
    child = base_child.replace(
        "import json\nimport sys\n",
        "import json\nimport os\nimport signal\nimport sys\n",
    ).replace(
        "resolver = TestOnlyDecisionResolver(record)\nif c[\"mode\"] == \"normal\":",
        "resolver = TestOnlyDecisionResolver(record)\n"
        "from rawlsing_next.pre553_batch_runner import BatchExecutionRunner as _BER\n"
        "_orig_record_receipt = _BER.record_receipt\n"
        "_record_calls = {\"n\": 0}\n"
        "def _record_then_kill(self, receipt):\n"
        "    _orig_record_receipt(self, receipt)\n"
        "    _record_calls[\"n\"] += 1\n"
        "    if _record_calls[\"n\"] == 2:\n"
        "        os.kill(os.getpid(), signal.SIGKILL)\n"
        "_BER.record_receipt = _record_then_kill\n"
        "if c[\"mode\"] == \"normal\":",
    )
    crashed = subprocess.run(
        [sys.executable, "-c", child, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True, text=True, timeout=120,
    )
    recovered = subprocess.run(
        [sys.executable, "-c", base_child, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True, text=True, timeout=120,
    )
    recovered_refs = (
        json.loads(recovered.stdout)["output_refs"]
        if recovered.returncode == 0 else []
    )
    expected = sorted(
        (ref.kind, ref.object_id, ref.content_hash) for ref in full.output_refs
    )
    actual = sorted(
        (ref["kind"], ref["object_id"], ref["content_hash"])
        for ref in recovered_refs
    )
    out = {
        "schema": "PYAT991_ALL_SEVEN_G5_NATIVE_CRASH_WITNESS@1",
        "fixture": "S1-D/S3 sourcefree synthetic 4 respondents/2 occasions",
        "checkpoint_state": checkpoint.entries[0].state,
        "checkpoint_prior_receipts": len(checkpoint.entries[0].receipt_materials),
        "crash_point": "after second actual BatchExecutionRunner.record_receipt inside native PARTIAL resume",
        "crashed_child_returncode": crashed.returncode,
        "crashed_child_killed_by_sigkill": crashed.returncode == -9,
        "crashed_child_stdout": crashed.stdout[:200],
        "crashed_child_stderr": crashed.stderr[-500:],
        "fresh_resume_returncode": recovered.returncode,
        "fresh_resume_stderr": recovered.stderr[-500:],
        "fresh_resume_exact_full_output_refs": actual == expected,
        "expected_output_refs": expected,
        "recovered_output_refs": actual,
        "note": "This kills actual native resume after a real pending receipt; it is not the author's JSON-load-only pre-resume dummy death.",
    }
    (proofroot / "native_crash_witness.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps({
        "checkpoint_state": out["checkpoint_state"],
        "crashed_child_returncode": out["crashed_child_returncode"],
        "fresh_resume_returncode": out["fresh_resume_returncode"],
        "fresh_resume_exact_full_output_refs": out["fresh_resume_exact_full_output_refs"],
        "crash_point": out["crash_point"],
    }, indent=2, sort_keys=True))
    return 0 if (
        out["crashed_child_returncode"] == -9
        and out["fresh_resume_returncode"] == 0
        and out["fresh_resume_exact_full_output_refs"]
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
