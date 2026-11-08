"""T4 proof: independent S46 activity consumes the HistoricalWorld material index."""

from pathlib import Path
import json

from rawlsing_next.sorok_history.activity import (
    ADVANCED,
    HELD,
    PROPERTY_MISSING,
    PROPERTY_UNAVAILABLE,
    advance_independent_activity,
)
from rawlsing_next.sorok_history.owner import HistoricalWorld


P4 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P4-FIRST-FULL-MPC-R1")
P3 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1")


def _set_surface_property(history, target_id, predicate, value, *, present):
    with history._write() as (_world, state):
        target = state["targets"][target_id]
        if present:
            target["surface"]["physical"][predicate] = value
        else:
            target["surface"]["physical"].pop(predicate, None)


def _actual_intervals(session):
    return [
        row for row in session.read_interval_states()
        if (row.get("domain") or {}).get("mode") == "ACTUAL"
    ]


def test_independent_s46_activity_holds_on_missing_or_unavailable_material_and_advances_on_restore(
    tmp_path, monkeypatch
):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))

    from run_p4 import new, open_owner

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    assert tool["domain"] == "resource"
    assert tool["physical"] == {"tool_available": True}

    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        clock_before = session.clock()
        perceived_before = set(session.user_perceived_ids())
        material_before = session.world().actor_state["A"]["material_remaining"]
        assert clock_before == opening["clock"]
        assert material_before == 1
        assert not _actual_intervals(session)

        _set_surface_property(history, target_id, "tool_available", None, present=False)
        held_missing = advance_independent_activity(
            fanin, history, target_id=target_id, predicate="tool_available", expected=True
        )
        assert held_missing.status == HELD
        assert held_missing.refusal_code == PROPERTY_MISSING
        assert held_missing.interval is None
        assert held_missing.clock_before == held_missing.clock_after == clock_before
        assert held_missing.material_before == held_missing.material_after == material_before
        assert not _actual_intervals(session)

        _set_surface_property(history, target_id, "tool_available", False, present=True)
        held_unavailable = advance_independent_activity(
            fanin, history, target_id=target_id, predicate="tool_available", expected=True
        )
        assert held_unavailable.status == HELD
        assert held_unavailable.refusal_code == PROPERTY_UNAVAILABLE
        assert held_unavailable.interval is None
        assert session.clock() == clock_before
        assert not _actual_intervals(session)

        _set_surface_property(history, target_id, "tool_available", True, present=True)
        advanced = advance_independent_activity(
            fanin, history, target_id=target_id, predicate="tool_available", expected=True
        )
        assert advanced.status == ADVANCED
        assert advanced.refusal_code is None
        assert advanced.clock_before == clock_before
        assert advanced.clock_after > advanced.clock_before
        assert advanced.material_before == 1
        assert advanced.material_after == 0
        assert advanced.interval is not None
        assert advanced.interval["status"] in {"PARTIAL", "REALIZED"}
        actual = _actual_intervals(session)
        assert len(actual) == 1
        assert actual[0]["domain"]["mode"] == "ACTUAL"
        assert any(
            segment["world"]["actual_action_event_id"]
            for segment in actual[0]["segments"]
        )
        assert advanced.user_visible is False
        assert advanced.writes_authority is False
        assert advanced.psychology_claim is False

        events = session.events()
        assert not any(event["kind"] == "INSPECT" for event in events)
        assert set(session.user_perceived_ids()) == perceived_before
        assert advanced.property_hash and advanced.target_hash
        assert advanced.property_source == "surface.physical"
        assert advanced.as_dict()["status"] == ADVANCED
        assert json.loads(json.dumps(advanced.as_dict()))["interval"]["status"] in {
            "PARTIAL", "REALIZED",
        }
    finally:
        owner.close()
