#!/usr/bin/env python3
"""Focused CC-F05 API/CLI evidence-binding and negative probe.

Synthetic temporary Git repository only; no source/respondent/native/science/
actor operation. Uses the author's focused fixture helper and the existing
validator API/CLI.
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


def _parts(evidence_text: str):
    records = []
    coverage = None
    for line in evidence_text.splitlines():
        if line.startswith("MCR_EVIDENCE: "):
            records.append(json.loads(line.split(": ", 1)[1]))
        elif line.startswith("MCR_COVERAGE: "):
            coverage = json.loads(line.split(": ", 1)[1])
    return records, coverage


def _evidence_text(records, coverage):
    return (
        "MCR_COMPLETION_EVIDENCE_BEGIN\n"
        + "".join("MCR_EVIDENCE: " + json.dumps(r, sort_keys=True) + "\n" for r in records)
        + "MCR_COVERAGE: " + json.dumps(coverage, sort_keys=True) + "\n"
        + "MCR_COMPLETION_EVIDENCE_END\n"
    )


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
    base = Path(tempfile.mkdtemp(prefix="verifier-probe-", dir=Path(__file__).resolve().parent.parent / "tmp"))
    repo, commission, candidate, evidence_text, external = _fixture(base)
    records, coverage = _parts(evidence_text)
    commission_path = base / "commission.md"
    commission_path.write_text(commission, encoding="utf-8")
    junk = base / "external-junk.md"
    junk.write_text("not an MCR evidence block\n", encoding="utf-8")
    copy = base / "external-copy.md"
    copy.write_text(evidence_text, encoding="utf-8")
    tracked = repo / "RECEIVING_EVIDENCE.md"
    alias = base / "alias-to-tracked.md"
    try:
        alias.symlink_to(tracked)
    except OSError:
        alias = None

    result = {}
    result["api_positive_external"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=external)
    result["api_no_path"] = validator.verify_return(
        commission, evidence_text, candidate, repo)
    result["api_tracked"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=tracked)
    if alias is not None:
        result["api_symlink_to_tracked"] = validator.verify_return(
            commission, evidence_text, candidate, repo, returned_path=alias)
    result["api_copy_outside"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=copy)
    # Deliberate API path/text mismatch: path exists outside the candidate but is junk.
    result["api_path_text_mismatch"] = validator.verify_return(
        commission, evidence_text, candidate, repo, returned_path=junk)

    missing = _evidence_text([r for r in records if r["id"] != "OBL-B"], coverage)
    result["api_missing_id"] = validator.verify_return(
        commission, missing, candidate, repo, returned_path=external)
    extra_records = records + [dict(records[0], id="OBL-EXTRA")]
    result["api_extra_id"] = validator.verify_return(
        commission, _evidence_text(extra_records, coverage), candidate, repo, returned_path=external)
    bad_grade = [dict(r) for r in records]
    bad_grade[0]["grade"] = "S0"
    result["api_bad_grade"] = validator.verify_return(
        commission, _evidence_text(bad_grade, coverage), candidate, repo, returned_path=external)

    result["cli_positive_external"] = _cli(commission_path, external, candidate, repo)
    result["cli_tracked"] = _cli(commission_path, tracked, candidate, repo)
    result["cli_path_text_mismatch"] = _cli(commission_path, junk, candidate, repo)

    print(json.dumps({
        "runner": sys.version,
        "candidate": candidate,
        "results": {k: {"status": v.get("status"), "errors": v.get("errors", [])}
                    if isinstance(v, dict) and "status" in v else v
                    for k, v in result.items()},
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
