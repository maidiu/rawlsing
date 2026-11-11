"""Independent replay/idempotence probes for final MII head 5eabd82."""

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
for rel in (
    "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1",
    "WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1",
    "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1",
    "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests",
):
    path = ROOT / rel
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import mii
from run_p6 import experience


def _run(state, command, **kwargs):
    kwargs.setdefault("request_id", None)
    return experience(state, Namespace(command=command, **kwargs))


def _profile(state):
    return json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))


def test_successful_duplicate_returns_same_surface_and_ledger(tmp_path):
    state = tmp_path / "duplicate"
    _run(state, "new")
    _run(state, "go", target="living room")
    _run(state, "mii-enable-learning")
    first = _run(state, "look", target="sandals", request_id="same-look")
    first_profile = _profile(state)
    first_ledger = (state / "p4_receipts.json").read_bytes()
    second = _run(state, "look", target="sandals", request_id="same-look")
    second_profile = _profile(state)
    assert second["clock"] == first["clock"]
    assert second["mii_surface"] == first["mii_surface"]
    assert second["detail"] == first["detail"]
    assert (state / "p4_receipts.json").read_bytes() == first_ledger
    assert second_profile["hypotheses"]["sandals"]["weight"] == first_profile["hypotheses"]["sandals"]["weight"]
    assert len(second_profile["exposures"]) == len(first_profile["exposures"])


def test_interrupted_save_retry_applies_evidence_once(tmp_path, monkeypatch):
    state = tmp_path / "interrupted"
    _run(state, "new")
    _run(state, "go", target="living room")
    _run(state, "mii-enable-learning")
    real_save = mii.save_profile

    def fail_save(path, profile):
        raise RuntimeError("injected save interruption")

    monkeypatch.setattr(mii, "save_profile", fail_save)
    with pytest.raises(RuntimeError, match="injected save interruption"):
        _run(state, "look", target="sandals", request_id="retry-look")
    ledger_after_failure = (state / "p4_receipts.json").read_bytes()

    monkeypatch.setattr(mii, "save_profile", real_save)
    retry = _run(state, "look", target="sandals", request_id="retry-look")
    retry_profile = _profile(state)
    assert retry["admission"] == "ADMITTED"
    assert retry["mii_surface"]["optional"]["target"] == "sandals"
    assert retry["recognition"]["sandals"]["event_id"]
    assert retry_profile["hypotheses"]["sandals"]["weight"] == 2
    assert (state / "p4_receipts.json").read_bytes() == ledger_after_failure

    duplicate = _run(state, "look", target="sandals", request_id="retry-look")
    duplicate_profile = _profile(state)
    assert duplicate["clock"] == retry["clock"]
    assert duplicate["mii_surface"] == retry["mii_surface"]
    assert duplicate_profile["hypotheses"]["sandals"]["weight"] == 2
    assert len(duplicate_profile["exposures"]) == len(retry_profile["exposures"])
    assert (state / "p4_receipts.json").read_bytes() == ledger_after_failure
