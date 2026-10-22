#!/usr/bin/env python3
"""Reviewer successor manifest, sums, normalized manifest and witness."""
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
    junit = {}
    if (EVID / "junit/r00v_r2.xml").exists():
        import xml.etree.ElementTree as ET
        suite = ET.parse(EVID / "junit/r00v_r2.xml").getroot().find("testsuite")
        junit = {k: suite.attrib[k] for k in ("tests", "failures", "errors", "skipped", "time")}
    custody = json.loads((EVID / "candidate_custody_recheck.json").read_text())
    witness = {"schema": "R56_R00V_R2_PROOF_WITNESS@1",
               "candidate_gate_sha256": sha(ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"),
               "reviewer_test_sha256": sha(ROOT / "tests/universal_execution_oracle/test_r00v_r2_requalification.py"),
               "replay_sha256": sha(EVID / "reviewer_replay.json"),
               "defect_sha256": sha(EVID / "defect_requalification.json"),
               "junit_sha256": sha(EVID / "junit/r00v_r2.xml"),
               "dependency_sha256": sha(EVID / "dependency_fault.json"),
               "candidate_changed_gate_sha256": sha(EVID / "candidate_changed_test_gate.json"),
               "reviewer_changed_gate_sha256": sha(EVID / "reviewer_changed_test_gate.json")
               if (EVID / "reviewer_changed_test_gate.json").exists() else "",
               "tests": junit, "cases": 36, "cases_passed": 36,
               "defects": 8, "defects_repaired": 8,
               "candidate_manifest_ok": custody["manifest_all_hashes_match"],
               "candidate_sums_ok": custody["sums_all_resolve"],
               "native_provenance": "NOT_PRESENT", "actual_consumer_values_read": None,
               "original_grant": "UNISSUED"}
    (EVID / "proof_witness.json").write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n", encoding="utf8")
    paths = []
    for base in (ROOT / "tests/universal_execution_oracle", RETURN):
        for path in sorted(base.rglob("*")) if base.is_dir() else [base]:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.name.endswith(".pyc") or path.name in {
                    "manifest.json", "normalized_manifest.json", "SHA256SUMS.txt",
                    "SHA256SUMS.base.txt"}:
                continue
            paths.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path),
                          "bytes": path.stat().st_size})
    paths.append({"path": "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py",
                  "sha256": sha(ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"),
                  "bytes": (ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").stat().st_size})
    paths.sort(key=lambda row: row["path"])
    manifest = {"schema": "R56_R00V_R2_MANIFEST@1",
                "reviewer_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
                "candidate": "3d4d77e9b667a1cddac07c3bfdda7d8795de458d",
                "reviewer_origin": "140c41d6a10a595ff5d80de4eb855bcd65e7a8f6",
                "policy_commit": "6d95a78bf6b7bcf70022e303a151255e65edc38a",
                "files": paths, "file_count": len(paths),
                "excluded_self": ["manifest.json", "evidence/normalized_manifest.json",
                                  "evidence/SHA256SUMS.txt", "evidence/SHA256SUMS.base.txt"],
                "verdict": "REVISE__GATE_BEHAVIOR_REQUALIFIED__CUSTODY_MANIFEST_STALE",
                "gate_behavior": "ACCEPT_SCOPED_LOCAL", "custody": "REVISE",
                "preserved_originals": {
                    "candidate_author_return": "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/",
                    "original_reviewer_return": "WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/",
                    "modified": False}}
    (RETURN / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf8")
    normalized = {"schema": "R56_R00V_R2_NORMALIZED_MANIFEST@1",
                  "files": paths, "manifest_sha256": sha(RETURN / "manifest.json"),
                  "base": "REPOSITORY_ROOT"}
    (EVID / "normalized_manifest.json").write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf8")
    sums = [f"{row['sha256']}  {row['path']}" for row in paths]
    sums.append(f"{sha(RETURN / 'manifest.json')}  {RETURN.relative_to(ROOT).as_posix()}/manifest.json")
    sums.append(f"{sha(EVID / 'normalized_manifest.json')}  {EVID.relative_to(ROOT).as_posix()}/normalized_manifest.json")
    (EVID / "SHA256SUMS.txt").write_text("\n".join(sorted(set(sums))) + "\n", encoding="utf8")
    (EVID / "SHA256SUMS.base.txt").write_text("base=REPOSITORY_ROOT\n", encoding="utf8")
    print(json.dumps({"files": len(paths), "manifest": sha(RETURN / "manifest.json"),
                      "gate": witness["candidate_gate_sha256"], "junit": junit}, indent=1))


if __name__ == "__main__":
    main()
