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
        job_id = target["job_id"]
        assert [row["id"] for row in owner.pending()] == [job_id]
        first = owner.lease(now=100, seconds=5)["job"]
        assert first["status"] == "RUNNING"
        assert owner.lease(now=104) is None

        # A separate owner sees the durable attempt and can recover it only after expiry.
        concurrent = fanin_api.open(root)
        try:
            recovered = HistoricalWorld(concurrent.session)
            second = recovered.lease(now=106)["job"]
            assert second["attempt"] == 2
            assert second["lease_token"] != first["lease_token"]
            candidate = {"request_id": job_id, "facts": []}
            with pytest.raises(HistoryRefusal, match="HISTORICAL_ATTEMPT_NOT_CURRENT"):
                owner.record_candidate(job_id, first["lease_token"], candidate, {}, now=107)
            # Movement changes the owner's causal snapshot while the provider is away.
            actor = concurrent.session.meta["user_actor"]
            here = concurrent.session.world().positions[actor]
            there = "market" if here == "workshop" else "workshop"
            concurrent.session.travel(there)
            assert recovered.record_candidate(
                job_id, second["lease_token"], candidate, {}, now=107
            ) == "STALE"
            assert "candidate" not in recovered.job(job_id)
            new_event = concurrent.session.events()[-1]
            next_target = recovered.admit_surface(
                replace(surface, referent_key="fixture:another-tool",
                        location=there, occurrence_id=new_event["event_id"])
            )
            attempt = recovered.lease(now=108)["job"]
            assert attempt["id"] == next_target["job_id"]
            candidate = {"request_id": attempt["id"], "facts": []}
            assert recovered.record_candidate(
                attempt["id"], attempt["lease_token"], candidate,
                {"grade": "MOCK"}, now=109
            ) == "CANDIDATE_READY"
            assert recovered.job(attempt["id"])["candidate"] == candidate
            assert recovered.target(next_target["id"]) == next_target
        finally:
            concurrent.close()
    finally:
        reopened.close()


def test_existing_p4_surface_reads_only_locally_perceived_particulars(tmp_path, monkeypatch):
    import json

    p4_dir = ENGINE.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
    monkeypatch.syspath_prepend(str(p4_dir))
    from run_p4 import new, open_owner, surface as foreground_surface

    ledger_file = tmp_path / "p4_receipts.json"
    opening = new(tmp_path, ledger_file, "recognized_plan")
    [tool] = opening["historical_particulars"]
    assert tool["domain"] == "resource"
    assert tool["physical"] == {"tool_available": True}
    ledger = json.loads(ledger_file.read_text())
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        history = HistoricalWorld(session)
        assert history.capture_visible_tool_resource() == tool["id"]
        assert [job["target_id"] for job in history.pending()] == [tool["id"]]
        actor = session.meta["user_actor"]
        here = session.world().positions[actor]
        there = "market" if here == "workshop" else "workshop"
        session.travel(there)
        event = session.events()[-1]
        history = HistoricalWorld(session)
        target = history.admit_surface(
            SurfaceParticular(event["event_id"], "fixture:document-2", "artifact",
                              there, {"cover": "paper"}, ("provenance",))
        )
        assert foreground_surface(owner, ledger)["historical_particulars"] == [
            {"id": target["id"], "domain": "artifact", "physical": {"cover": "paper"}}
        ]
        session.travel(here)
        assert foreground_surface(owner, ledger)["historical_particulars"] == [tool]
    finally:
        owner.close()
