"""Run producer in one interpreter, wait for exit, then consumer in a new one."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]


def _run(script: str, *args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/issued_batch_f4_r3" / script),
         *args],
        cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=300,
    )


def main() -> int:
    proofroot = Path(sys.argv[1]).resolve()
    proofroot.mkdir(parents=True, exist_ok=True)
    capsule_path = proofroot / "capsule.json"
    producer = _run("fresh_producer_3q.py", str(proofroot / "producer"), str(capsule_path))
    if producer.returncode != 0:
        print(json.dumps({
            "status": "FAIL", "phase": "producer",
            "returncode": producer.returncode,
            "stdout": producer.stdout, "stderr": producer.stderr,
        }, indent=2))
        return 1
    capsule = json.loads(capsule_path.read_text(encoding="utf-8"))
    source_path = Path(capsule["source_path"])
    source_existed = source_path.exists()
    source_path.unlink()
    source_deleted_before_consumer = not source_path.exists()

    consumer = _run("fresh_consumer_3q.py", str(capsule_path))
    if consumer.returncode != 0:
        print(json.dumps({
            "status": "FAIL", "phase": "consumer",
            "returncode": consumer.returncode,
            "source_deleted_before_consumer": source_deleted_before_consumer,
            "stdout": consumer.stdout, "stderr": consumer.stderr,
        }, indent=2))
        return 1
    observed = json.loads(consumer.stdout)
    expected = capsule["expected"]
    checks = {
        "producer_exit_before_consumer_start": producer.returncode == 0,
        "source_file_existed_before_delete": source_existed,
        "source_deleted_before_consumer": source_deleted_before_consumer,
        "consumer_process_is_new_interpreter": True,
        "consumer_source_opens_zero": observed["source_opens"] == 0,
        "consumer_full_c11_builds_zero": observed["full_c11_repository_builds"] == 0,
        "i03_facts_equal": observed["i03"]["facts"] == expected["i03"]["facts"],
        "i03_states_equal": observed["i03"]["typed_states"] == expected["i03"]["typed_states"],
        "i05_receipts_equal": observed["i05"]["receipts"] == expected["i05"]["receipts"],
        "i05_counts_equal": (
            observed["i05"]["candidate_count"], observed["i05"]["covered_candidate_count"]
        ) == (
            expected["i05"]["candidate_count"], expected["i05"]["covered_candidate_count"]
        ),
        "batch_states_equal": observed["batch"]["states"] == expected["batch"]["states"],
        "batch_count_equal": observed["batch"]["count"] == expected["batch"]["count"],
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "schema": "PYAT997_Q2_3Q_ISSUED_BATCH_FRESH_PROCESS_PROOF@1",
        "status": status,
        "sourcefree": True,
        "fixture": "TEST_ONLY generated SAV",
        "producer": {
            "returncode": producer.returncode,
            "stdout": producer.stdout,
            "stderr": producer.stderr,
            "source_reads": capsule["source_reads"],
            "decode_calls": capsule["decode_calls"],
            "cell_passes": capsule["cell_passes"],
            "source_sha256": capsule["source_sha256"],
            "family_counts": capsule["family_counts"],
        },
        "consumer": {
            "returncode": consumer.returncode,
            "stdout": consumer.stdout,
            "stderr": consumer.stderr,
            "source_opens": observed["source_opens"],
            "full_c11_repository_builds": observed["full_c11_repository_builds"],
        },
        "expected": expected,
        "observed": observed,
        "checks": checks,
        "source_deleted_before_consumer": source_deleted_before_consumer,
        "batch_shape": "1 issued QUERY unit + 1 issued DISCOVERY unit from the R3 compiler catalog",
    }
    out = proofroot / "fresh_process_proof.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": status, "proof": str(out), "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
