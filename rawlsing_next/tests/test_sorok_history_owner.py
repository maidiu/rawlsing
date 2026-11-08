from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.sorok_history.owner import HistoricalWorld, HistoryRefusal, SurfaceParticular


ENGINE = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
          / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1")


def test_surface_and_outbox_share_one_world_checkpoint(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ENGINE))
    from developmental_recursion.p2_owner import load_p2

    fanin_api = load_p2()
    root = tmp_path / "session"
    fanin = fanin_api.start(root)
    session = fanin.session
    try:
        current = session.world().positions[session.meta["user_actor"]]
        session.travel("market" if current == "workshop" else "workshop")
        world = session.world()
        event = next(row for row in reversed(session.events())
                     if row["kind"] in {"ARRIVAL", "MOVE", "REPAIR", "OFFSCREEN_REPAIR"}
                     and row["clock"] == world.clock)
        surface = SurfaceParticular(event["event_id"], "fixture:lease-tool-17",
                                    "item", event["location"], {"condition": "scuffed"},
                                    ("physical", "provenance"))
        owner = HistoricalWorld(session)
        checkpoint = session.world().snapshot()
        real_checkpoint = session.product._checkpoint

        def interrupted(*args):
            real_checkpoint(*args)
            raise RuntimeError("simulated failure after checkpoint insert")

        with monkeypatch.context() as patch:
            patch.setattr(session.product, "_checkpoint", interrupted)
            with pytest.raises(RuntimeError, match="simulated failure"):
                owner.admit_surface(surface)
        assert session.world().snapshot() == checkpoint
        assert owner.pending() == ()
        with pytest.raises(HistoryRefusal, match="CURRENT_OBJECTIVE_OCCURRENCE_REQUIRED"):
            owner.admit_surface(replace(surface, occurrence_id="unadmitted-model-mention"))

        target = owner.admit_surface(surface)
        assert owner.admit_surface(surface) == target
        assert session.world().actor_state == world.actor_state
        assert owner.pending()[0]["target_id"] == target["id"]
        assert len(owner.pending()) == 1
        with pytest.raises(HistoryRefusal, match="BOUND_SURFACE_CONFLICT"):
            owner.admit_surface(replace(surface, physical={"condition": "pristine"}))
    finally:
        fanin.close()

    reopened = fanin_api.open(root)
    try:
        owner = HistoricalWorld(reopened.session)
        assert owner.target(target["id"]) == target
        assert [row["id"] for row in owner.pending()] == [target["job_id"]]
    finally:
        reopened.close()
