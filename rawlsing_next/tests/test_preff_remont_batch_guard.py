"""REMONT Q008: fail-closed sourcefree batch-evidence custody, macOS-friendly.

Only invokes the runner for preflight failures (never recursively executes a
suite), so no wave reads, global suite or background worker are involved.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "rawlsing_next/tests/run_preff_remont_batch.sh"


def _head():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _run(tmp_path, *cases, expected=None, proof=None):
    env = os.environ.copy()
    env["EXPECTED_PREFF_C0_HEAD"] = expected or _head()
    env["REMONT_PROOF_ROOT"] = str(proof or tmp_path / "remont-proof")
    return subprocess.run(
        ["bash", str(RUNNER), *cases],
        cwd=ROOT, env=env, capture_output=True, text=True,
        timeout=20,
    )


def test_existing_exact_head_evidence_is_not_overwritten(tmp_path):
    proof = tmp_path / "historic-red"
    proof.mkdir()
    sentinel = proof / "index.csv"
    sentinel.write_bytes(b"Q001,1,DO_NOT_REWRITE\n")
    actual = _run(tmp_path, "RMT-Q009", proof=proof)
    assert actual.returncode == 27
    assert "HOLD_EXISTING_REMONT_PROOF__DO_NOT_OVERWRITE" in actual.stderr
    assert sentinel.read_bytes() == b"Q001,1,DO_NOT_REWRITE\n"


@pytest.mark.parametrize("ids,exitcode,diagnostic", [
    (("RMT-Q001", "RMT-Q001"), 26, "HOLD_DUPLICATE_REMONT_QID"),
    (("RMT-Q006",), 2, "INVALID_OR_UNCOMMISSIONED_REMONT_CASE"),
    (("RMT-Q999",), 2, "INVALID_OR_UNCOMMISSIONED_REMONT_CASE"),
])
def test_invalid_or_duplicate_queue_items_refuse_before_proof(tmp_path, ids, exitcode, diagnostic):
    proof = tmp_path / "not-created"
    actual = _run(tmp_path, *ids, proof=proof)
    assert actual.returncode == exitcode
    assert diagnostic in actual.stderr
    assert not proof.exists()


def test_stale_head_refuses_before_touching_proof(tmp_path):
    proof = tmp_path / "untouched"
    actual = _run(
        tmp_path, "RMT-Q009",
        expected="0" * 40 if _head() != "0" * 40 else "1" * 40,
        proof=proof,
    )
    assert actual.returncode == 23
    assert "HOLD_STALE_REMONT_QUEUE_HEAD" in actual.stderr
    assert not proof.exists()


def test_default_batch_contains_all_eligible_qids_bash3_compatible():
    script = RUNNER.read_text()
    assert "cases=(RMT-Q001 RMT-Q002 RMT-Q003 RMT-Q004 RMT-Q005 RMT-Q007 RMT-Q008 RMT-Q009)" in script
    assert "declare -A" not in script
    for qid in ("RMT-Q001", "RMT-Q002", "RMT-Q003", "RMT-Q004", "RMT-Q005", "RMT-Q007", "RMT-Q008", "RMT-Q009"):
        assert qid in script
