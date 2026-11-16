"""Focused regression for G5-MR01 multi-release selected-fact ownership.

The original independent G5 harness is run unmodified.  Before the adapter
repair it exited 1 because the actual world consumer accepted a product whose
determinant release was B while the selected fact's exact provenance was release
A.  After the repair the same harness must exit 0 and record a governed refusal
for that exact reason; the base positive control inside the harness still passes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


def test_g5_mr01_original_repro_refuses_for_selected_fact_release(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    harness = (
        repo / "WORKER_RETURNS" / "PYAT960_S2G_G5" / "repro_multirelease.py"
    )
    if not harness.is_file():
        pytest.skip(
            "exact G5-MR01 reviewer harness is absent from this checkout; "
            "the adapter check is still covered by the 153-test regression"
        )
    proofroot = tmp_path / "proofroot"
    proofroot.mkdir()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = str(proofroot)
    completed = subprocess.run(
        [sys.executable, str(harness), str(proofroot)],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    evidence_path = proofroot / "multirelease_evidence.json"
    assert evidence_path.is_file(), completed.stderr
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence["defect_if_accepted"] is False
    assert evidence["outcome"]["consumer_state"] == "REFUSED"
    assert (
        "consumer determinant release is not the selected fact source release"
        in evidence["outcome"]["reason_code"]
    )
    assert completed.returncode == 0, completed.stderr
