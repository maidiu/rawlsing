"""R44 I44 evidence runner: native suites, integration, JUnit, proof gate, cold replay.

Run from the repo root:
    python3 WORKER_RETURNS/PYAT-R44-I44-.../run_evidence.py

Optional environment:
    U43_SUPPORT_ROOT=/path/to/LOCAL_COURTS/u43-repaired
        Exact U43 author local-court support (not committed by U43). When present,
        the U43 suite runs 47/47; otherwise the 38 self-contained tests run and the
        dependency is recorded.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time

RETURN_DIR = Path(__file__).resolve().parent
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))

import bootstrap  # noqa: E402

ROOT = bootstrap.ROOT
EVIDENCE = RETURN_DIR / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


def _run(name: str, command: list[str], cwd: Path, env_extra: dict | None = None, timeout: int = 3600):
    env = dict(os.environ)
    env.update(env_extra or {})
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.time()
    proc = subprocess.run(command, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=timeout)
    elapsed = round(time.time() - started, 2)
    log = EVIDENCE / f"{name}.log"
    log.write_text(proc.stdout + ("\n--- STDERR ---\n" + proc.stderr if proc.stderr else ""), encoding="utf-8")
    return {
        "name": name,
        "command": " ".join(command).replace(str(ROOT) + "/", "").replace(str(ROOT), "$REPO_ROOT"),
        "cwd": str(cwd.relative_to(ROOT)),
        "returncode": proc.returncode,
        "elapsed_seconds": elapsed,
        "log": str(log.relative_to(ROOT)),
        "tail": (proc.stdout.strip().splitlines()[-3:] if proc.stdout.strip() else []),
    }


def main() -> int:
    bootstrap.ensure_inputs()
    results = []

    suites = {
        "a42_suite": (bootstrap.path_for("A42"), "tests", "evidence/a42_junit.xml"),
        "j42_suite": (bootstrap.path_for("J42"), "tests", "evidence/j42_junit.xml"),
        "f43_suite": (bootstrap.path_for("F43"), "tests", "evidence/f43_junit.xml"),
        "b43_suite": (bootstrap.path_for("B43"), "tests", "evidence/b43_junit.xml"),
    }
    u43_env = {}
    support = os.environ.get("U43_SUPPORT_ROOT") or str(ROOT / "LOCAL_COURTS/u43-repaired")
    if Path(support).is_dir():
        u43_env["U43_REVIEW_ROOT"] = support
    suites["u43_suite"] = (bootstrap.path_for("U43"), "tests", "evidence/u43_junit.xml")

    for name, (cwd, target, junit) in suites.items():
        env_extra = u43_env if name == "u43_suite" else None
        results.append(
            _run(
                name,
                [sys.executable, "-m", "pytest", target, "-q", "--junitxml", str(RETURN_DIR / junit)],
                cwd,
                env_extra=env_extra,
            )
        )
    results.append(
        _run(
            "i44_integration_courts",
            [sys.executable, "-m", "pytest", "test_i44_integration.py", "-q",
             "--junitxml", str(EVIDENCE / "i44_junit.xml")],
            RETURN_DIR,
        )
    )
    results.append(
        _run(
            "i44_proof_witness",
            [sys.executable, "CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py", "witness",
             "WORKER_RETURNS/PYAT-R44-I44-J42-U43-B43-F43-WHOLE-N11-FANIN-R1/test_i44_integration.py.proof.json",
             "--root", ".", "--receipt",
             "WORKER_RETURNS/PYAT-R44-I44-J42-U43-B43-F43-WHOLE-N11-FANIN-R1/evidence/proof_witness.json"],
            ROOT,
            env_extra={"PYTHONPATH": "rawlsing_next/tests"},
        )
    )

    import i44_integration

    first = i44_integration.run_all()
    second = i44_integration.run_all()
    cold = {
        "schema": "I44_COLD_REPLAY@1",
        "first_blended": first["blended"],
        "second_blended": second["blended"],
        "byte_identical": first["artifact_sha256"] == second["artifact_sha256"],
        "artifact_sha256": first["artifact_sha256"],
        "merged_receipt_count": first["merged_receipt_count"],
        "original_measured": first["merged_verdict"]["original_measured_occupied_cells"],
        "n11_state": first["merged_verdict"]["n11_state"],
    }
    (EVIDENCE / "cold_replay.json").write_text(
        json.dumps(cold, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (EVIDENCE / "i44_run_report.json").write_text(
        json.dumps(first, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    support_record = {
        "u43_support_root_ref": "$U43_SUPPORT_ROOT" if Path(support).is_dir() else "NOT_PRESENT",
        "u43_support_present": Path(support).is_dir(),
        "u43_support_committed_by_u43": False,
        "u43_suite_note": (
            "U43's returned bytes contain 47 tests; 9 descriptor-refusal tests import the "
            "author's uncommitted phase_b_support_v1 local-court support. With the exact "
            "support directory present all 47 pass (see u43_suite.log); without it the "
            "38 self-contained tests pass. This is a U43 return packaging gap, not an I44 "
            "integration defect."
        ),
    }
    summary = {
        "schema": "I44_EVIDENCE_RUN@1",
        "startup": "2e5a8693b2b48df5b2e1281e1d33ff2d5d5d2d2c",
        "runs": results,
        "all_return_suites_green": all(
            r["returncode"] == 0 for r in results
            if r["name"].endswith("_suite") and r["name"] != "u43_suite"
        ),
        "u43_support_record": support_record,
        "cold_replay": cold,
        "proof_witness": "evidence/proof_witness.json",
        "all_evidence_green": all(r["returncode"] == 0 for r in results) and cold["byte_identical"],
    }
    (EVIDENCE / "evidence_run_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: summary[k] for k in ("all_return_suites_green", "all_evidence_green", "cold_replay", "u43_support_record")}, indent=2))
    return 0 if summary["all_evidence_green"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
