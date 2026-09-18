from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def test_ee_p2xd_commissioned_browser_hostile_court():
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    target = Path("tests/test_ee_p2x_darwin_court_driver.py")
    assert target.is_file(), "commission-required EE-P2XD qualification file is missing"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(target)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    assert completed.returncode == 0, completed.stdout
    assert "19 passed" in completed.stdout, completed.stdout
