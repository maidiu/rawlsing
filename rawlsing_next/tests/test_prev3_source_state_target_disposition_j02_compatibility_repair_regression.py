from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SELFTEST = ROOT / "evidence" / "selftest" / "prev3_source_state_target_disposition_production.py"


def test_original_k02_producer_selftest_remains_green_after_j02_vocabulary_repair():
    proc = subprocess.run(
        [sys.executable, str(SELFTEST)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert len(payload["checks"]) == 15
    assert all(row["status"] == "PASS" for row in payload["checks"])
