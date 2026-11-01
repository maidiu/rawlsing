#!/usr/bin/env python3
"""Execute RRIF-E original, repair and first-consumer courts in isolated processes."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R2 = ROOT / "rrif_r2"
EXT = R2 / "rrif_r3_extension"
REPO = next(parent for parent in ROOT.parents if (parent / ".git").exists())
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(name: str, command: list[str], *, env: dict | None = None, expect: int = 0) -> dict:
    environment = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        **(env or {}),
    }
    result = subprocess.run(command, cwd=REPO, env=environment, capture_output=True, text=True, timeout=300)
    (EVIDENCE / f"{name}.stdout.txt").write_text(result.stdout, encoding="utf8")
    (EVIDENCE / f"{name}.stderr.txt").write_text(result.stderr, encoding="utf8")
    summary = [line for line in result.stdout.splitlines() if " passed" in line or " failed" in line]
    return {
        "name": name,
        "command": command,
        "exit_code": result.returncode,
        "expected_exit_code": expect,
        "passed_expectation": result.returncode == expect,
        "summary": summary[-1] if summary else "",
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
    }


def main() -> int:
    py = sys.executable
    base_env = {"PYTHONPATH": f"{R2}{os.pathsep}{REPO}"}
    ext_env = {"PYTHONPATH": f"{R2}{os.pathsep}{EXT}{os.pathsep}{REPO}"}
    courts = []
    courts.append(_run(
        "r2_original_20",
        [py, "-m", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider",
         "--junitxml", str(EVIDENCE / "r2_original_20.xml"),
         str(R2 / "tests/test_join.py"), str(R2 / "tests/test_rrif_r2_c12.py")],
        env=base_env))
    courts.append(_run(
        "r3_extension_9",
        [py, "-m", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider",
         "--junitxml", str(EVIDENCE / "r3_extension_9.xml"),
         str(EXT / "tests/test_rrif_r3_extension.py")],
        env=ext_env))
    courts.append(_run(
        "rrif_e_repair_6",
        [py, "-m", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider",
         "--junitxml", str(EVIDENCE / "rrif_e_repair_6.xml"),
         str(R2 / "tests/test_rrif_e_repair.py")],
        env=ext_env))
    receipt = EVIDENCE / "first_consumer_receipt.json"
    shutil.rmtree(EVIDENCE / "first_consumer_state", ignore_errors=True)
    courts.append(_run(
        "first_consumer",
        [py, str(R2 / "first_consumer_cli.py"), "--root",
         str(EVIDENCE / "first_consumer_state")],
        env=ext_env))
    if courts[-1]["exit_code"] == 0:
        (EVIDENCE / "first_consumer_receipt.json").write_text(
            (EVIDENCE / "first_consumer.stdout.txt").read_text(encoding="utf8"),
            encoding="utf8",
        )
    payload = {
        "schema": "SOROK_RRIF_E_EXECUTED_COURTS@1",
        "repo": str(REPO),
        "candidate": str(R2),
        "courts": courts,
        "all_expected": all(court["passed_expectation"] for court in courts),
        "first_consumer_receipt_sha256": _sha(receipt) if receipt.exists() else "",
        "source_manifest_sha256": _sha(R2 / "SOURCE_MANIFEST.json"),
        "candidate_preimage_sha256": _sha(R2 / "RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json"),
    }
    (EVIDENCE / "court_results.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["all_expected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
