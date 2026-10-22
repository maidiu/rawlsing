#!/usr/bin/env python3
"""Collect reviewer environment, JUnit, normalized manifest and SHA256SUMS."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RETURN = Path(__file__).resolve().parents[1]
EVID = RETURN / "evidence"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args], cwd=str(ROOT), text=True).strip()


def main():
    junit = {}
    path = EVID / "junit/r00v.xml"
    if path.exists():
        root = ET.parse(path).getroot().find("testsuite")
        junit["r00v"] = {k: root.attrib[k] for k in ("tests", "failures", "errors", "skipped", "time")}
    env = {
        "schema": "R56_R00V_ENVIRONMENT@1",
        "reviewer_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head_at_evidence_time": git("rev-parse", "HEAD"),
        "candidate_commit": "efd12b1d46f1ccf90de14b292f600078f11ec7e0",
        "policy_commit": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "status_porcelain": git("status", "--porcelain").splitlines(),
        "os": platform.platform(),
        "python": sys.version,
        "git": git("--version"),
        "junit": junit,
    }
    (EVID / "environment.json").write_text(json.dumps(env, indent=2, sort_keys=True) + "\n", encoding="utf8")
    normalized = {
        "schema": "R56_R00V_NORMALIZED_MANIFEST@1",
        "candidate_commit": "efd12b1d46f1ccf90de14b292f600078f11ec7e0",
        "reviewer_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "files": [
            {"path": str(path.relative_to(ROOT)), "sha256": sha(path),
             "bytes": path.stat().st_size}
            for path in sorted([RETURN] + [ROOT / "tests/universal_execution_oracle"] + [ROOT / "CROSS_HQ_CONTROL_ROOM"], key=str)
            for path in ([path] if path.is_file() else sorted(path.rglob("*")))
            if path.is_file() and "__pycache__" not in path.parts
            and not path.name.endswith(".pyc")
            and (path == ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"
                 or str(path).startswith(str(RETURN))
                 or str(path).startswith(str(ROOT / "tests/universal_execution_oracle")))
            and path.name != "normalized_manifest.json"
        ],
        "author_manifest_absent": True,
        "author_sha256sums_stale": ["WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/00_RETURN.md"],
    }
    (EVID / "normalized_manifest.json").write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf8")
    files = [
        "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py",
        "tests/universal_execution_oracle/test_r56_gate.py",
        "tests/universal_execution_oracle/test_r00v_reviewer.py",
        "tests/universal_execution_oracle/conftest.py",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/00_RETURN.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/01_REVIEW_SESSION_AND_SCOPE.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/02_REPRODUCTION_AND_VARIATION.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/03_DEFECTS_FOUND.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/04_CUSTODY_MANIFEST_AND_WITNESS.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/05_VERDICT_AND_HANDOFF.md",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/session.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/shared_contract_status.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/reviewer_replay.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/defect_probes.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/reviewer_proof_witness.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/candidate_manifest_reconstruction.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/normalized_manifest.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/environment.json",
        "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/junit/r00v.xml",
    ]
    lines = [f"{sha(ROOT / f)}  {f}" for f in files if (ROOT / f).exists()]
    (EVID / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(json.dumps({"junit": junit, "files": len(lines)}, indent=1))


if __name__ == "__main__":
    main()
