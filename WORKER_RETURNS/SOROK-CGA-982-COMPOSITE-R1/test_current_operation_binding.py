"""CG-A #982 composite: the current operation, not a caller interval, authorizes access."""
from argparse import Namespace
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from house import read_house
from situated import current_p3_actor_access


def _run(state, command, request_id, *, duration=None, **kwargs):
    return run_p6.experience(state, Namespace(
        command=command, request_id=request_id, duration=duration,
        situated_house=True, **kwargs,
    ))


def _receipt(state):
    ledger = json.loads((state / "p4_receipts.json").read_text())
    return ledger["turns"][-1]["receipt"]


def _owner(state):
    return run_p6.open_owner(state / "actual-p2")


def _access(session, interval, world, house, packet, receipt):
    return current_p3_actor_access(
        session, interval, world, house, packet, source_receipt=receipt,
    )


def test_current_owner_receipt_authorizes_only_its_operation(tmp_path):
    state = tmp_path / "positive"
    _run(state, "new", None)
    _run(state, "approach", "current")
    receipt = _receipt(state)
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [receipt["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        assert _access(session, receipt["interval"], world, house, packet, receipt) is True
        assert _access(session, receipt["interval"], world, house, packet, None) is False
        assert _access(session, receipt["interval"], world, house, packet, {}) is False
        assert _access(session, receipt["interval"], world, house, packet,
                       {"interval": None}) is False
        assert _access(session, receipt["interval"], world, house, packet,
                       {"interval": {}}) is False
    finally:
        owner.close()


def test_missing_or_forged_current_operation_provenance_is_refused(tmp_path):
    state = tmp_path / "provenance"
    _run(state, "new", None)
    _run(state, "approach", "current")
    receipt = _receipt(state)
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [receipt["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        for key in ("state_id", "receipt_hash", "episode_id", "domain_issuance_id"):
            forged = deepcopy(receipt)
            forged["interval"].pop(key)
            assert _access(session, forged["interval"], world, house, packet, forged) is False
        for key in ("state_id", "receipt_hash", "episode_id", "domain_issuance_id"):
            forged = deepcopy(receipt)
            forged["interval"][key] = "0" * 64
            assert _access(session, forged["interval"], world, house, packet, forged) is False
        widened = dict(receipt["interval"])
        widened["start"] -= 1
        assert _access(session, widened, world, house, packet, receipt) is False
        forged = deepcopy(receipt)
        forged["interval"]["end"] += 1
        assert _access(session, forged["interval"], world, house, packet, forged) is False
    finally:
        owner.close()


def test_old_event_cannot_be_laundered_through_current_interval_fields(tmp_path):
    state = tmp_path / "launder"
    _run(state, "new", None)
    _run(state, "approach", "old")
    old = _receipt(state)
    _run(state, "wait", "later", duration=4)
    current = _receipt(state)
    assert current["interval"]["state_id"] != old["interval"]["state_id"]
    forged = deepcopy(old)
    forged["interval"] = deepcopy(current["interval"])
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [old["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        assert _access(session, forged["interval"], world, house, packet, forged) is False
    finally:
        owner.close()


def test_same_clock_other_operation_receipt_is_not_current_authority(tmp_path, monkeypatch):
    original = run_p6.establish_demo_conditions

    def establish_facing(session):
        original(session)
        world, house = read_house(session)
        house["situated_conditions"] = {
            **house["situated_conditions"], "bench_view": "facing_player",
        }
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish_demo_conditions", establish_facing)
    base = tmp_path / "base"
    other = tmp_path / "other"
    _run(base, "new", None)
    _run(other, "new", None)

    _run(base, "approach", "a")
    _run(other, "orient", "b")
    receipt_a = _receipt(base)
    receipt_b = _receipt(other)
    assert receipt_a["interval"]["start"] == receipt_b["interval"]["start"]
    assert receipt_a["interval"]["end"] == receipt_b["interval"]["end"]
    assert receipt_a["performed"]["event_id"] != receipt_b["performed"]["event_id"]
    assert receipt_b["outward_cue"]["kind"] == "ORIENT"

    owner = _owner(base)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet_b = {"cues": [receipt_b["outward_cue"]],
                    "recent_self_actions": [], "recent_speech": []}
        assert _access(session, receipt_b["interval"], world, house, packet_b, receipt_b) is False
        packet_a = {"cues": [receipt_a["outward_cue"]],
                    "recent_self_actions": [], "recent_speech": []}
        assert _access(session, receipt_a["interval"], world, house, packet_a, receipt_a) is True
    finally:
        owner.close()


def test_cold_reopen_and_retry_conserve_the_current_operation(tmp_path):
    state = tmp_path / "cold"
    _run(state, "new", None)
    _run(state, "approach", "replayed")
    receipt = _receipt(state)
    ledger_file = state / "p4_receipts.json"
    saved = ledger_file.read_bytes()
    _run(state, "approach", "replayed")
    assert ledger_file.read_bytes() == saved

    for _ in range(2):
        owner = _owner(state)
        try:
            session = owner.base_owner.fanin.session
            world, house = read_house(session)
            packet = {"cues": [receipt["outward_cue"]],
                      "recent_self_actions": [], "recent_speech": []}
            assert _access(session, receipt["interval"], world, house, packet, receipt) is True
        finally:
            owner.close()

    _run(state, "wait", "later", duration=4)
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [receipt["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        assert _access(session, receipt["interval"], world, house, packet, receipt) is False
    finally:
        owner.close()
