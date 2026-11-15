"""P6 history query-order invariance and unpursued-detail proof.

Run from the repository root with:
  /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
    WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py

One exact same-path P6 state snapshot is restored for each trace. Inspection
order may change real clocks/ledger/effects, so those are recorded but never
required equal. Objective roots, object/fact identities, dependency links and
cold-restore house history must remain stable.
"""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import shutil
import sys

RETURNS = Path(__file__).resolve().parents[1]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

from run_p6 import experience, open_owner, read_house  # noqa: E402
import house as house_module  # noqa: E402


def _run(state, command, **kwargs):
    return experience(state.resolve(), Namespace(command=command, request_id=None, **kwargs))


def _observe(state):
    owner = open_owner(state.resolve() / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        _, stored = read_house(session)
        facts = house_module.facts(stored["epoch"])
        return {
            "snapshot": owner.snapshot().document(),
            "ledger": json.loads((state / "p4_receipts.json").read_text()),
            "clock": session.world().clock,
            "positions": dict(session.world().positions),
            "stored": stored,
            "objective_facts": facts,
            "scene": house_module.scene(session),
            "nadia_episodes": list(session.episodes("A")),
            "user_perceived_ids": list(session.user_perceived_ids()),
        }
    finally:
        owner.close()


def _restore(state, initial):
    if state.exists():
        shutil.rmtree(state)
    shutil.copytree(initial, state)


def _inspect_order(state, initial, order):
    _restore(state, initial)
    _run(state, "go", target="living room")
    before = _observe(state)
    assert set(before["stored"]["history"]) == {"strap-repair", "bench-installation"}
    assert "photo-exposure" in before["objective_facts"]
    assert "photo-exposure" not in before["stored"]["history"]

    steps = []
    for target in order:
        result = _run(state, "look", target=target)
        assert result["admission"] == "ADMITTED"
        steps.append({"target": target, "detail": result["detail"]})
        assert "photo-exposure" in _observe(state)["stored"]["history"]

    after = _observe(state)
    # Cold restore through the actual P6 view entry point.
    cold_view = _run(state, "view")
    cold = _observe(state)
    return {"before": before, "steps": steps, "after": after,
            "cold_view": cold_view, "cold": cold}


def test_history_query_order_invariance_and_unpursued_detail(tmp_path):
    state = tmp_path / "state"
    initial = tmp_path / "initial"

    opening = _run(state, "new")
    assert opening["clock"] == 248
    shutil.copytree(state, initial)

    photo_first = _inspect_order(state, initial, ("photo", "sandals"))
    sandals_first = _inspect_order(state, initial, ("sandals", "photo"))

    # The order changes real action sequence, but not the fixed objective roots,
    # object/fact identities or dependency links.
    for trace in (photo_first, sandals_first):
        assert trace["after"]["stored"]["root"] == trace["cold"]["stored"]["root"]
        assert trace["after"]["stored"]["source"] == house_module.SOURCE
        assert trace["after"]["stored"]["branch"] == trace["cold"]["stored"]["branch"]
        assert trace["after"]["objective_facts"] == trace["cold"]["objective_facts"]
        assert trace["after"]["stored"]["history"]["photo-exposure"]["depends_on"] == [
            "strap-repair"]
        assert trace["after"]["stored"]["history"]["photo-exposure"]["clock"] == 244

    assert photo_first["after"]["stored"]["root"] == sandals_first["after"]["stored"]["root"]
    assert photo_first["after"]["stored"]["source"] == sandals_first["after"]["stored"]["source"]
    assert photo_first["after"]["objective_facts"] == sandals_first["after"]["objective_facts"]
    assert photo_first["after"]["stored"]["history"] == sandals_first["after"]["stored"]["history"]
    assert photo_first["after"]["stored"]["objects"] == sandals_first["after"]["stored"]["objects"]
    assert photo_first["after"]["scene"] == sandals_first["after"]["scene"]
    assert photo_first["cold"]["stored"]["history"] == sandals_first["cold"]["stored"]["history"]

    # The first exposed close fact is order-specific; both orders expose the
    # same fixed photo/sandal facts afterward.
    assert [step["target"] for step in photo_first["steps"]] == ["photo", "sandals"]
    assert [step["target"] for step in sandals_first["steps"]] == ["sandals", "photo"]
    assert photo_first["steps"][0]["detail"] != sandals_first["steps"][0]["detail"]
    assert photo_first["steps"][1]["detail"] == sandals_first["steps"][1]["detail"]

    # A real pre-existing detail can lawfully remain unpursued. It remains in
    # objective source facts but is absent from stored house history and is not
    # forced into the ordinary visible scene.
    _restore(state, initial)
    _run(state, "go", target="living room")
    living = _observe(state)
    leave_view = _run(state, "view")
    _run(state, "go", target="workshop")
    leave = _observe(state)
    assert "photo-exposure" in leave["objective_facts"]
    assert "photo-exposure" not in leave["stored"]["history"]
    assert "photo-exposure" not in json.dumps(leave_view)
    assert set(leave_view["available"]) == {"coaster", "photo", "sandals"}
    assert set(living["scene"]["objects"]) == {"coaster", "photo", "sandals"}
    assert living["scene"]["objects"]["photo"].startswith("A photograph leans")
    assert leave["stored"]["history"] == {
        "bench-installation": leave["objective_facts"]["bench-installation"],
        "strap-repair": leave["objective_facts"]["strap-repair"],
    }

    # The two completed inspections did change real action/clock/ledger effects
    # (recorded, not collapsed); only the requested stable objective structure is
    # compared above.
    # Clocks/ledger are real effects and are deliberately not compared across
    # order traces; each trace must remain a valid, non-collapsed run.
    assert photo_first["after"]["clock"] >= opening["clock"]
    assert sandals_first["after"]["clock"] >= opening["clock"]
    assert photo_first["after"]["ledger"] is not None
    assert sandals_first["after"]["ledger"] is not None
