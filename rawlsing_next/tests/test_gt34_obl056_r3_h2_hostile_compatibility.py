from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
H2 = "rawlsing_next/tests/test_gt34_obl056_repaired_input_authority_acceptance_hostile_audit.py"
OBSOLETE_BLOCKER = "ADOPTION_BLOCKER_current_entry_empty_immutable_provenance_is_accepted"
PREDECESSOR_IDENTITY_PIN = "repaired_candidate_relevant_git_blobs_are_exact"


def test_h2_applicable_hostile_surface_remains_green():
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    selection = f"not {OBSOLETE_BLOCKER} and not {PREDECESSOR_IDENTITY_PIN}"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", H2, "-k", selection],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    assert completed.returncode == 0
