from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as a
import rawlsing_next.tests.test_gt34_obl056_r3_current_entry_provenance_hostile_audit as h3


ROOT = Path(__file__).resolve().parents[2]
HOSTILE = "rawlsing_next/tests/test_gt34_obl056_r3_current_entry_provenance_hostile_audit.py"
SCAFFOLD_ONLY_MISCLASSIFICATION = "test_16_matched_integrity_invalid_member_rejected"


def test_01_fresh_h3_surface_except_known_scaffold_only_misclassification_is_green():
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", HOSTILE, "-k", f"not {SCAFFOLD_ONLY_MISCLASSIFICATION}"],
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


def test_02_matched_integrity_invalid_member_rejected_at_entry_integrity_gate(monkeypatch):
    e0 = h3._entry()
    # schema_id is hashed into the entry body but is not duplicated on the receipt,
    # so corrupting only schema_id reaches the matched-entry integrity gate rather
    # than being classified earlier as a consumer/role/scope mismatch.
    e = replace(e0, schema_id="CORRUPTED_WITHOUT_READDRESS")
    s = h3._snapshot((e,))
    r = h3._receipt(e, s)
    monkeypatch.setattr(a, "_CURRENT_REGISTRY", s)
    with pytest.raises(a.AcceptanceIntegrityError, match="registry entry content/hash mismatch"):
        h3._validate(r, currentness=a.CURRENT_ACCEPTED)
