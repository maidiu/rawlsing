"""J42 cold replay: two full fresh builds (producers + join) must project the
identical scientific content hash and identical artifact bytes."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
REPO = PACKET.parents[1]
ARTIFACTS = (
    "actual_e41_w41_p41_joint_dependency_manifest.json",
    "n9_n10e_n10w_real_joined_consumer_receipts.json",
    "sourcefree_vs_retained_scientific_grade_matrix.json",
    "n11_actual_join_handback.json",
)


def _build(tmp_path, name):
    outdir = tmp_path / name
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, str(PACKET / "runtime/j42_build.py"),
         "--outdir", str(outdir)], env=env, cwd=str(REPO),
        capture_output=True, text=True, timeout=3600)
    assert proc.returncode == 0, proc.stderr[-2000:]
    return json.loads(proc.stdout)


def test_two_fresh_full_builds_are_identical(tmp_path):
    first = _build(tmp_path, "run1")
    first_bytes = {name: (PACKET / name).read_bytes() for name in ARTIFACTS}
    second = _build(tmp_path, "run2")
    second_bytes = {name: (PACKET / name).read_bytes() for name in ARTIFACTS}
    assert first["projection"] == second["projection"]
    for name in ARTIFACTS:
        assert first_bytes[name] == second_bytes[name], name
    assert first["coverage_ok"] is True
    assert first["no_drop"] is True
