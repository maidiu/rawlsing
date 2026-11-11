#!/usr/bin/env python3
"""Independent CCF5-R01 API text/path binding recheck probe.

Synthetic temporary Git/evidence fixture only; uses the existing validator and
the existing focused test fixture helper. No source/respondent/native/science/
actor operation. Writes only under this review lease tmp/log.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from CROSS_HQ_CONTROL_ROOM import verify_copy_paste_commission_r1 as validator
from CROSS_HQ_CONTROL_ROOM.test_verify_copy_paste_commission_r1 import _fixture

ROOT = Path(__file__).resolve().parents[5]
VALIDATOR = ROOT / "CROSS_HQ_CONTROL_ROOM" / "verify_copy_paste_commission_r1.py"
TMP_ROOT = Path(__file__).resolve().parents[1] / "tmp"


def _cli(commission_path: Path, evidence_path: Path, candidate: str, repo: Path):
    command = [
        sys.executable, "-B", str(VALIDATOR), str(commission_path),
        "--verify-return", str(evidence_path),
        "--candidate-sha", candidate, "--evidence-root", str(repo),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"stdout": result.stdout, "stderr": result.stderr}
    return {"returncode": result.returncode, "payload": payload}


def main() -> int:
    base = Path(tempfile.mkdtemp(prefix="ccf5-r01-probe-", dir=TMP_ROOT))
    repo, commission, candidate, evidence_text, external = _fixture(base)
    commission_path = base / "commission.md"
    commission_path.write_text(commission, encoding="utf-8")
    junk = base / "external-junk.md"
    junk.write_text("not an MCR evidence block\n", encoding="utf-8")
    missing = base / "missing-evidence.md"
    unreadable_dir = base / "external-unreadable-dir"
    unreadable_dir.mkdir()

    results = {}
    results["api_mismatch_junk_path"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=junk)
    results["api_valid_external_pair"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=external)
    results["api_missing_path"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=missing)
    results["api_unreadable_directory"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=unreadable_dir)
    results["cli_positive_external"] = _cli(commission_path, external, candidate, repo)
    results["cli_junk_path"] = _cli(commission_path, junk, candidate, repo)

    payload = {
        "schema": "CCF5_R01_API_BINDING_INDEPENDENT_RECHECK_V1",
        "runner": sys.version,
        "validator_sha256": __import__("hashlib").sha256(VALIDATOR.read_bytes()).hexdigest(),
        "candidate": candidate,
        "results": {
            key: ({"status": value.get("status"), "errors": value.get("errors", [])}
                  if isinstance(value, dict) and "status" in value else value)
            for key, value in results.items()
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
