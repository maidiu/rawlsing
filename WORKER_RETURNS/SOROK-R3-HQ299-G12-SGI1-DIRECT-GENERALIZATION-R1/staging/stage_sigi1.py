#!/usr/bin/env python3
"""Stage the true S-GI1 closure at 27ca1f2792a5213064c0b5ea2e27b89e8acce0c3.

Every staged file is verified against its Git blob SHA-1 (actual NUL
'blob <len>\\0' preimage).  Pristine copies live under staging/sigi1_src/ and
staging/sigi1_reference/; the runner executes from a byte-verified runtime
mirror under repro/sigi1_run/.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
REV = "27ca1f2792a5213064c0b5ea2e27b89e8acce0c3"
PREFIX = "WORKER_RETURNS/SOROK-SGI1-SOURCEFREE-K11-LAB-R1/"

# (repo-relative path under PREFIX, staged area)
SRC_PY = [
    "01_LAB_IMPLEMENTATION/run_k11.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/__init__.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/core.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/world.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/mother.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/proposal.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/qualification.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/selection.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/construction.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/relation.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/continuation.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/dag.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/pipeline.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/k11_contract.py",
    "01_LAB_IMPLEMENTATION/lab_sgi1/k11_runner.py",
]
LLM_RECORDS = [
    "08_LLM_PROPOSAL_RECORDS/proposal_index.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M0_GENERAL.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M0_LOCAL.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M0_INST.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M0_MOBILITY.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M0_UNCONVENTIONAL.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_M2_GENERAL.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_MP_GENERAL.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_MP_CONFLICTING.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_DEDUPE_CLEAN.json",
    "08_LLM_PROPOSAL_RECORDS/proposal_DEDUPE_DUP.json",
]
REFERENCE = [
    "03_RUN_LOGS/k11_summary.json",
    "03_RUN_LOGS/k11_run_log.json",
    "05_MEASUREMENTS/suite_fingerprints.json",
    "05_MEASUREMENTS/suite_replay_comparison.json",
    "05_MEASUREMENTS/cost_report.json",
    "05_MEASUREMENTS/feasibility.json",
    "02_K11_FIXTURES/fixture_manifest.json",
    "00_RETURN.md",
]


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def stage(rel: str, area: Path) -> dict:
    raw = subprocess.check_output(["git", "-C", str(REPO), "show", f"{REV}:{PREFIX}{rel}"])
    observed = git_blob(raw)
    out = area / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    return {"path": rel, "blob_sha1": observed, "bytes": len(raw)}


def main() -> int:
    rows = []
    for rel in SRC_PY + LLM_RECORDS:
        rows.append({**stage(rel, RETURN / "staging" / "sigi1_src"), "area": "src"})
    for rel in REFERENCE:
        rows.append({**stage(rel, RETURN / "staging" / "sigi1_reference"), "area": "reference"})
    manifest = {
        "schema": "G12_SGI1_STAGING_MANIFEST@1",
        "source_rev": REV,
        "git_blob_preimage": "sha1('blob <len>\\0' + bytes)",
        "entries": rows,
        "n_entries": len(rows),
    }
    (RETURN / "staging" / "sigi1_staging_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    for r in rows:
        print(f"{r['blob_sha1'][:12]}  {r['area']:9} {r['path']}")
    print(f"staged {len(rows)} objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
