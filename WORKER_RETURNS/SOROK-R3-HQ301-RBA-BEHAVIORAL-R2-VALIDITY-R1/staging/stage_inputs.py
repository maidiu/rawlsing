#!/usr/bin/env python3
"""Stage RBA review inputs with verified Git blob identities.

Every staged object is read via `git show <commit>:<path>` and verified with
SHA-1 over the actual NUL-header blob preimage. Nothing staged here is edited.
Execution copies live under ../exec/ (byte-verified at copy time).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]

R2 = "a7d2be9894bf92f81356adf14141136666e63bd1"
R2P = "WORKER_RETURNS/SOROK-R3-HQ300-BEHAVIORAL-ASSAY-R2-RECONSTRUCTION-R1/"
LAB1 = "d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09"
LAB1P = "WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/"
LAB2 = "bf5fda102f4bced41a0f18f71c4c380d5d099462"
LAB2P = "WORKER_RETURNS/SOROK-R3-HQ298-SM-LAB2-BEHAVIORAL-R1/"
RMB = "bf7518cff877ce108ef9c07f2e2eeaf990171d08"
RMBP = "WORKER_RETURNS/SOROK-R3-HQ299-RMB-BEHAVIORAL-HARNESS-INDEPENDENT-R1/"

PINS = [
    # R2 assay + tests + frozen evidence
    (R2, R2P + "assay/__init__.py", "r2/assay/__init__.py"),
    (R2, R2P + "assay/architecture.py", "r2/assay/architecture.py"),
    (R2, R2P + "assay/corpus.py", "r2/assay/corpus.py"),
    (R2, R2P + "assay/experiment.py", "r2/assay/experiment.py"),
    (R2, R2P + "assay/mock_policy.py", "r2/assay/mock_policy.py"),
    (R2, R2P + "assay/oracle.py", "r2/assay/oracle.py"),
    (R2, R2P + "assay/scoring.py", "r2/assay/scoring.py"),
    (R2, R2P + "assay/transport.py", "r2/assay/transport.py"),
    (R2, R2P + "test_r2.py", "r2/test_r2.py"),
    (R2, R2P + "data/corpus.json", "r2/data/corpus.json"),
    (R2, R2P + "data/oracle.json", "r2/data/oracle.json"),
    (R2, R2P + "data/schedule.json", "r2/data/schedule.json"),
    (R2, R2P + "freezes/v6.json", "r2/freezes/v6.json"),
    (R2, R2P + "CURRENT_FREEZE", "r2/CURRENT_FREEZE"),
    (R2, R2P + "preregistration_v6.json", "r2/preregistration_v6.json"),
    (R2, R2P + "original_R1_preregistration.json", "r2/original_R1_preregistration.json"),
    (R2, R2P + "original_R1_freeze_receipt.json", "r2/original_R1_freeze_receipt.json"),
    (R2, R2P + "RMB_23_regression_matrix.json", "r2/RMB_23_regression_matrix.json"),
    (R2, R2P + "deviations.json", "r2/deviations.json"),
    (R2, R2P + "read_cut.json", "r2/read_cut.json"),
    (R2, R2P + "reproduce.py", "r2/reproduce.py"),
    (R2, R2P + "run_experiments.py", "r2/run_experiments.py"),
    (R2, R2P + "audit_outputs.py", "r2/audit_outputs.py"),
    (R2, R2P + "baseline.py", "r2/baseline.py"),
    (R2, R2P + "freeze_candidate.py", "r2/freeze_candidate.py"),
    # LAB1 closure
    (LAB1, LAB1P + "lab/__init__.py", "lab1/lab/__init__.py"),
    (LAB1, LAB1P + "lab/hashutil.py", "lab1/lab/hashutil.py"),
    (LAB1, LAB1P + "lab/opacity.py", "lab1/lab/opacity.py"),
    (LAB1, LAB1P + "lab/owners.py", "lab1/lab/owners.py"),
    (LAB1, LAB1P + "lab/transition.py", "lab1/lab/transition.py"),
    (LAB1, LAB1P + "lab/world_fixtures.py", "lab1/lab/world_fixtures.py"),
    (LAB1, LAB1P + "lab/runner.py", "lab1/lab/runner.py"),
    (LAB1, LAB1P + "lab/experiment.py", "lab1/lab/experiment.py"),
    (LAB1, LAB1P + "lab/test_lab.py", "lab1/lab/test_lab.py"),
    (LAB1, LAB1P + "lab/run_lab.py", "lab1/lab/run_lab.py"),
    (LAB1, LAB1P + "02_FROZEN_PREREGISTRATION.json", "lab1/02_FROZEN_PREREGISTRATION.json"),
    (LAB1, LAB1P + "outputs/primary_results.json", "lab1_ref/primary_results.json"),
    # LAB2 closure
    (LAB2, LAB2P + "lab2/__init__.py", "lab2/lab2/__init__.py"),
    (LAB2, LAB2P + "lab2/behavioral_runner.py", "lab2/lab2/behavioral_runner.py"),
    (LAB2, LAB2P + "lab2/model_gate.py", "lab2/lab2/model_gate.py"),
    (LAB2, LAB2P + "lab2/packets.py", "lab2/lab2/packets.py"),
    (LAB2, LAB2P + "lab2/scoring.py", "lab2/lab2/scoring.py"),
    (LAB2, LAB2P + "lab2/test_lab2.py", "lab2/lab2/test_lab2.py"),
    (LAB2, LAB2P + "lab2/run_lab2.py", "lab2/lab2/run_lab2.py"),
    (LAB2, LAB2P + "01_PREREGISTRATION_FROZEN.json", "lab2/01_PREREGISTRATION_FROZEN.json"),
    (LAB2, LAB2P + "outputs/preregistration_freeze.json", "lab2/outputs_preregistration_freeze.json"),
    # RMB original oracle + test
    (RMB, RMBP + "test_independent.py", "rmb/test_independent.py"),
    (RMB, RMBP + "independent_expectations.json", "rmb/independent_expectations.json"),
]


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()


def main() -> int:
    rows = []
    for rev, repo_path, rel in PINS:
        raw = subprocess.check_output(["git", "-C", str(REPO), "show", f"{rev}:{repo_path}"])
        out = RET / "staging" / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(raw)
        rows.append({
            "source_rev": rev, "repo_path": repo_path,
            "git_blob_sha1": git_blob_sha1(raw), "staged_path": rel, "bytes": len(raw),
        })
        print(f"{git_blob_sha1(raw)[:12]}  {rel}")
    (RET / "staging" / "staging_manifest.json").write_text(
        json.dumps({"schema": "RBA_STAGING_MANIFEST@1",
                    "git_blob_preimage": "sha1('blob <len>\\0' + bytes)",
                    "entries": rows}, indent=2, sort_keys=True) + "\n")
    print(f"staged {len(rows)} objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
