#!/usr/bin/env python3
"""Collect C12 verification, passport, environment and SHA256SUMS."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / ".git").exists())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(*args):
    return subprocess.check_output(args, cwd=str(REPO), text=True).strip()


def main():
    sys.path.insert(0, str(ROOT))
    from r31e import bootstrap
    bootstrap.install()
    from r26e.c12_integrity import QualifiedC12Store
    verification = {}
    for name in ("available", "pressed"):
        path = ROOT / "evidence" / f"c12_{name}.sqlite"
        store = QualifiedC12Store(path)
        verification[name] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha(path),
            "verify_root": store.verify("root"),
            "verify_first_session": store.verify("first_session"),
            "branches": store.branches(),
        }
        store.close()
    (ROOT / "evidence/c12_verification.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf8")
    junit = {}
    for name in ("r31e", "r30a_baseline", "r29p_subset"):
        root = ET.parse(ROOT / "evidence" / "junit" / f"{name}.xml").getroot().find("testsuite")
        junit[name] = {k: root.attrib[k] for k in ("tests", "failures", "errors", "time")}
    passport = {
        "schema": "R31E_PASSPORT@1",
        "model_declared": "DeepSeek V4.1-Flash",
        "reasoning_declared": "MAX",
        "intelligence": "I2+",
        "harness": "OpenCode local session",
        "execution": "S2 local Git/Python/pytest/SQLite/CLI cold processes",
        "external_llm_calls": 0,
        "live_actor_model": "LIVE_ACTOR_MODEL_NOT_RUN",
        "external_provider_usage": "UNKNOWN",
        "external_cost": "UNKNOWN",
        "r30a_source_ref": "ce0dfc67ef5058338f4d7161d32a8cb5bdf733a6",
        "r29p_source_ref": "001b506fa26ae879ff5b6e57138fc2696e12b538",
        "startup_ref": "9a9b8a61daf4bf78e2885436924e5235f26f5772",
        "worktree_head_at_evidence_time": run("git", "rev-parse", "HEAD"),
        "os": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "git": run("git", "--version"),
        "junit": junit,
        "notes": [
            "Actor expression is a bounded deterministic structured grammar/admission baseline.",
            "No external model, credential, provider charge or subagent was used.",
            "Human A5 and native actor/C12/C11 authority remain NOT_RUN/HOLD.",
        ],
    }
    (ROOT / "evidence/passport.json").write_text(
        json.dumps(passport, indent=2, sort_keys=True) + "\n", encoding="utf8")
    environment = {
        "schema": "R31E_ENVIRONMENT@1",
        "worktree": str(REPO),
        "branch": run("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "head_at_evidence_time": run("git", "rev-parse", "HEAD"),
        "startup_ref": "9a9b8a61daf4bf78e2885436924e5235f26f5772",
        "r30a_ref": "ce0dfc67ef5058338f4d7161d32a8cb5bdf733a6",
        "r29p_ref": "001b506fa26ae879ff5b6e57138fc2696e12b538",
        "status_porcelain": run("git", "status", "--porcelain").splitlines(),
        "os": platform.platform(),
        "python": sys.version,
        "git": run("git", "--version"),
    }
    (ROOT / "evidence/environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf8")
    files = [
        "evidence/c12_available.sqlite", "evidence/c12_pressed.sqlite",
        "evidence/c12_verification.json", "evidence/source_manifest.json",
        "evidence/port_receipt.json", "evidence/contrasts.json",
        "evidence/session_available.json", "evidence/session_pressed.json",
        "evidence/cold_reopen.json", "evidence/faults.json",
        "evidence/attention_contrast.json", "evidence/admission_chain.json",
        "evidence/cli_available.txt", "evidence/cli_pressed.txt",
        "evidence/junit/r31e.xml", "evidence/junit/r30a_baseline.xml",
        "evidence/junit/r29p_subset.xml", "evidence/passport.json",
        "evidence/environment.json",
        "r31e/expression.py", "r31e/session.py", "r31e/cli.py",
    ]
    lines = [f"{sha(ROOT / f)}  {f}" for f in files if (ROOT / f).exists()]
    (ROOT / "evidence/SHA256SUMS.txt").write_text("\n".join(lines) + "\n",
                                                   encoding="utf8")
    print(json.dumps({"junit": junit, "c12": {
        k: {"root": v["verify_root"]["ok"],
            "first_session": v["verify_first_session"]["ok"]}
        for k, v in verification.items()}}, indent=1))


if __name__ == "__main__":
    main()
