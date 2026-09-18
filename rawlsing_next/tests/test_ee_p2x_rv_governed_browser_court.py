from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def test_ee_p2x_rv_commissioned_browser_requalification_court():
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    targets = [
        Path("rawlsing_next/tests/test_ee_p2x_local_court_receipts.py"),
        Path("tests/test_ee_p2x_darwin_court_driver.py"),
        Path("rawlsing_next/tests/test_ee_p2x_local_court_driver_integration.py"),
    ]
    for target in targets:
        assert target.is_file(), f"commission-required qualification file is missing: {target}"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", *map(str, targets)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    assert completed.returncode == 0, completed.stdout
    assert "failed" not in completed.stdout.lower(), completed.stdout
