"""Independent sourcefree chronology/provenance reject-and-restore proof."""
from __future__ import annotations

import copy
import json
from argparse import Namespace
from pathlib import Path
import sys

import pytest

P6 = Path(__file__).resolve().parents[1] / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

import run_p6
from run_p6 import RecursionRefusal, experience, open_owner, save
from house import SLOT, read_house


def _run(state, command, **args):
    return experience(state, Namespace(command=command, request_id=None, **args))


def _house(state):
    owner = open_owner(state / "actual-p2")
    try:
        _, house = read_house(owner.base_owner.fanin.session)
        return copy.deepcopy(house), owner.snapshot().document(), owner.base_owner.fanin.session
    finally:
        owner.close()


def test_p6_chronology_provenance_reject_restore_and_cold_trace(tmp_path):
    state = tmp_path / "state"
    _run(state, "new")
    _run(state, "go", target="living room")
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        _, adjacent_house = read_house(session)
        assert "bench-installation" in adjacent_house["history"]
        closure = next(row for row in session.episodes("A")
                       if row["kind"] == "P6_OBJECT_CLOSURE")
        assert closure["body"]["source_event_id"] not in session.user_perceived_ids()
    finally:
        owner.close()
    _run(state, "look", target="sandals")
    _run(state, "look", target="photo")

    before, before_snapshot, _ = _house(state)
    original_history = copy.deepcopy(before["history"])
    assert set(original_history) == {"bench-installation", "strap-repair", "photo-exposure"}
    assert original_history["photo-exposure"]["depends_on"] == ["strap-repair"]
    assert original_history["photo-exposure"]["clock"] > original_history["strap-repair"]["clock"]
    assert original_history["bench-installation"]["clock"] < original_history["photo-exposure"]["clock"]
    baseline_view = _run(state, "view")

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        house["history"]["photo-exposure"]["depends_on"] = ["bench-installation"]
        session.product._checkpoint(session.branch_id, world.clock, world)
        tampered_snapshot = owner.snapshot().document()
    finally:
        owner.close()

    ledger_file = state / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    assert ledger["turns"]
    ledger["turns"][-1]["after"] = tampered_snapshot
    save(ledger_file, ledger)

    with pytest.raises(RecursionRefusal, match="P6_OBJECT_PROVENANCE_MISMATCH"):
        _run(state, "view")

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world = session.world()
        world.resources[SLOT] = copy.deepcopy(before)
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored_snapshot = owner.snapshot().document()
    finally:
        owner.close()

    ledger = json.loads(ledger_file.read_text())
    ledger["turns"][-1]["after"] = restored_snapshot
    save(ledger_file, ledger)
    restored = _run(state, "view")
    assert restored == baseline_view

    after, after_snapshot, _ = _house(state)
    assert after["history"] == original_history
    assert after_snapshot == before_snapshot
    assert after["root"] == before["root"]
    assert after["source"] == before["source"]
    assert after["epoch"] == before["epoch"]
    assert after["objects"] == before["objects"]
    assert after["rooms"] == before["rooms"]
