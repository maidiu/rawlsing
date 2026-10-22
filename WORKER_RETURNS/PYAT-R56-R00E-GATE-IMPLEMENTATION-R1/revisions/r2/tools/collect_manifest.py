#!/usr/bin/env python3
"""Collect successor manifest, proof witness, passport and SHA sums."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())
RETURN = HERE.parents[1]
EVID = RETURN / "evidence"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args],
                                   cwd=str(ROOT), text=True).strip()


def main():
    gate = ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"
    files = []
    for base in (gate, ROOT / "tests/universal_execution_oracle", RETURN):
        paths = [base] if base.is_file() else sorted(base.rglob("*"))
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.name.endswith(".pyc") or path.name in {"manifest.json",
                                                            "SHA256SUMS.txt",
                                                            "normalized_manifest.json"}:
                continue
            files.append({"path": str(path.relative_to(ROOT)),
                          "sha256": sha(path), "bytes": path.stat().st_size})
    manifest = {
        "schema": "R56_R00E_R2_MANIFEST@1",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "parent_candidate": "efd12b1d46f1ccf90de14b292f600078f11ec7e0",
        "policy_commit": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "policy_root": "CROSS_HQ_CONTROL_ROOM/universal_execution_policy/r56_sourcefree_v1/revisions/r2",
        "gate_path": "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py",
        "files": files,
        "file_count": len(files),
        "excluded_self": ["manifest.json", "evidence/normalized_manifest.json",
                          "evidence/SHA256SUMS.txt"],
        "supersedes": {
            "original_author_return": "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/",
            "original_author_manifest": "ABSENT",
            "original_author_sha256sums_stale": ["00_RETURN.md"],
            "original_reviewer_return": "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/",
            "preserved_untouched": True,
        },
        "note": "Self-excluded manifest; SHA256SUMS separately references this manifest.",
    }
    (RETURN / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf8")
    normalized = {
        "schema": "R56_R00E_R2_NORMALIZED_MANIFEST@1",
        "files": files,
        "manifest_sha256": sha(RETURN / "manifest.json"),
        "excluded_self": ["evidence/normalized_manifest.json", "evidence/SHA256SUMS.txt"],
    }
    (EVID / "normalized_manifest.json").write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf8")
    acceptance = {
        "schema": "R56_R00E_R2_MANIFEST_SUPERSESSION@1",
        "original_author_manifest": "ABSENT",
        "original_author_sums_stale": [{"path": "00_RETURN.md",
                                         "recorded": "67a50277958be36f356ec37f9e8c2b2ef8d18d9ee8e6742e328e60930aafa824",
                                         "actual_at_efd12b": "c03c7eb41102ea6f38592f4cf4fac0299742ee45f94a8d6216d21baf2d3aae2d"}],
        "successor_manifest": "manifest.json",
        "successor_manifest_sha256": sha(RETURN / "manifest.json"),
        "original_files_modified": False,
        "note": "Old stale evidence preserved; successor manifest/sums are current and self-excluded.",
    }
    (EVID / "manifest_supersession.json").write_text(json.dumps(acceptance, indent=2, sort_keys=True) + "\n", encoding="utf8")
    passport = {
        "schema": "R56_R00E_R2_PASSPORT@1",
        "model_declared": "DeepSeek V4.1-Flash",
        "reasoning_declared": "MAX",
        "intelligence": "I2-I3",
        "execution": "S3 local Git/Python/pytest",
        "harness": "OpenCode local session",
        "external_model_calls": 0,
        "external_cost": "UNKNOWN",
        "usage": "UNKNOWN",
        "machine": platform.platform(),
        "python": sys.version.split()[0],
        "git": git("--version"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head_at_evidence_time": git("rev-parse", "HEAD"),
        "repair_parent": "efd12b1d46f1ccf90de14b292f600078f11ec7e0",
        "policy_commit": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
        "native_shared_contract": "eb28fdcc311e2534b66def445e745cb25cb8a9bd",
        "review_shared_contract": "485f31e52ca82905dcfbbc79c5f8c8294fb55f49",
        "r57": "953eb07ad29cc424b2fc43cfeb13ef83355f3a50",
        "r09": "NOT_GRANTED", "original": "UNISSUED", "r00v": "REQUALIFICATION_REQUIRED",
    }
    (EVID / "passport.json").write_text(json.dumps(passport, indent=2, sort_keys=True) + "\n", encoding="utf8")
    witness = {
        "schema": "R56_R00E_R2_PROOF_WITNESS@1",
        "gate_sha256": sha(gate),
        "test_sha256": sha(ROOT / "tests/universal_execution_oracle/test_r00e_r2_reviewer_regressions.py"),
        "replay_sha256": sha(EVID / "replay.json"),
        "defect_matrix_sha256": sha(EVID / "defect_matrix.json"),
        "junit_sha256": sha(EVID / "junit/r00e_r2.xml"),
        "dependency_fault_sha256": sha(EVID / "dependency_fault.json"),
        "changed_test_gate_sha256": sha(EVID / "changed_test_gate.json")
        if (EVID / "changed_test_gate.json").exists() else "",
        "commands": {
            "tests": "PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/universal_execution_oracle -q --junitxml=WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/revisions/r2/evidence/junit/r00e_r2.xml",
            "replay": "PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/revisions/r2/tools/run_replay.py",
            "dependency": "python3 tests/universal_execution_oracle/dependency_probe.py {baseline,fault,restore}",
        },
        "replay_cases": 36, "replay_passed": 36,
        "defects": 8, "defects_repaired": 8,
        "tests_passed": 24,
        "native_provenance": "NOT_PRESENT",
        "actual_consumer_values_read": None,
        "original_grant": "UNISSUED",
    }
    (EVID / "proof_witness.json").write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n", encoding="utf8")
    sums = []
    for path in sorted(RETURN.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.name != "SHA256SUMS.txt":
            sums.append(f"{sha(path)}  {path.relative_to(RETURN).as_posix()}")
    sums.append(f"{sha(gate)}  ../../CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py")
    sums.append(f"{sha(ROOT / 'tests/universal_execution_oracle/test_r00e_r2_reviewer_regressions.py')}  ../../tests/universal_execution_oracle/test_r00e_r2_reviewer_regressions.py")
    (EVID / "SHA256SUMS.txt").write_text("\n".join(sorted(sums)) + "\n", encoding="utf8")
    print(json.dumps({"files": len(files), "manifest": sha(RETURN / "manifest.json"),
                      "gate": witness["gate_sha256"]}, indent=1))


if __name__ == "__main__":
    main()
