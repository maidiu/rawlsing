#!/usr/bin/env python3
"""Collect environment, passport and SHA256SUMS for R00E."""
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
    for name in ("r00e",):
        path = EVID / "junit" / f"{name}.xml"
        if path.exists():
            root = ET.parse(path).getroot().find("testsuite")
            junit[name] = {k: root.attrib[k] for k in ("tests", "failures", "errors", "time")}
    passport = {
        "schema": "R56_R00E_PASSPORT@1",
        "model_declared": "DeepSeek V4.1-Flash",
        "reasoning_declared": "MAX",
        "intelligence": "I2-I3",
        "execution": "S3 local Git/Python/pytest",
        "harness": "OpenCode local session",
        "external_model_calls": 0,
        "external_cost": "UNKNOWN",
        "machine": platform.platform(),
        "python": sys.version.split()[0],
        "git": git("--version"),
        "worktree_head_at_evidence_time": git("rev-parse", "HEAD"),
        "startup_ref": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "policy_commit": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "policy_root": "CROSS_HQ_CONTROL_ROOM/universal_execution_policy/r56_sourcefree_v1/revisions/r2",
        "junit": junit,
        "native_shared_contract": "NOT_PRESENT_AT_STARTUP_6D95A78B",
        "r09": "NOT_GRANTED",
        "scientific_original": "UNISSUED",
        "r00v": "NOT_RUN",
        "notes": [
            "Launched on direct user Vozhd instruction; no separate HQ technical seal was supplied.",
            "Implementation is a candidate gate only; no native, generic or original positive claim.",
            "The R00P policy was read only at its frozen R2 paths.",
        ],
    }
    (EVID / "passport.json").write_text(json.dumps(passport, indent=2, sort_keys=True) + "\n", encoding="utf8")
    env = {
        "schema": "R56_R00E_ENVIRONMENT@1",
        "worktree": str(ROOT),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head_at_evidence_time": git("rev-parse", "HEAD"),
        "startup_ref": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "status_porcelain": git("status", "--porcelain").splitlines(),
        "os": platform.platform(),
        "python": sys.version,
        "git": git("--version"),
    }
    (EVID / "environment.json").write_text(json.dumps(env, indent=2, sort_keys=True) + "\n", encoding="utf8")
    files = [
        "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py",
        "tests/universal_execution_oracle/test_r56_gate.py",
        "tests/universal_execution_oracle/conftest.py",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/replay.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/proof_witness.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/imports.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/author_verdict.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/passport.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/environment.json",
        "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/evidence/junit/r00e.xml",
    ]
    lines = [f"{sha(ROOT / f)}  {f}" for f in files if (ROOT / f).exists()]
    (EVID / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(json.dumps({"junit": junit, "files": len(lines)}, indent=1))


if __name__ == "__main__":
    main()
