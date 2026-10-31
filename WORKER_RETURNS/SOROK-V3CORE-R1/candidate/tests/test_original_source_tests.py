from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_unchanged_v3_source_tests_pass_in_vendored_tree() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{ROOT / 'vendor' / 'py3deps'}:{ROOT / 'vendor'}"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-o",
        "addopts=",
        "-q",
        "-p",
        "no:cacheprovider",
        "vendor/v3/tests/test_architecture_invariants.py",
        "vendor/v3/tests/test_step_logic.py",
        "vendor/v3/tests/test_v5_pressure_flow.py",
        "vendor/v3/tests/test_v5_pressureflow_golden_run.py",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "40 passed" in result.stdout, result.stdout
