from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ROOT_COURTS = (
    "tests/test_fiabc_derivative_parentage.py",
    "tests/test_r35_generic_guard_court.py",
    "tests/test_fiabc_telemetry_semantics.py",
    "tests/test_fiabc_lifecycle_accounting.py",
)


def test_required_root_source_independent_courts():
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    for rel in ROOT_COURTS:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", rel],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        assert proc.returncode == 0, f"{rel} failed:\n{proc.stdout}"
