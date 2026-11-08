from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.sorok_history.owner import HistoricalWorld, HistoryRefusal, SurfaceParticular, digest


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
        leased = owner.lease(now=100, seconds=5)
        first = leased["job"]
        packet = leased["packet"]
        assert packet["request_id"] == job_id
        assert packet["target_ids"] == [target["id"]]
        assert packet["surface"][target["id"]]["physical"] == {"condition": "scuffed"}
        assert packet["event_refs"] == [{
            "kind": "WORLD_EVENT", "object_id": event["event_id"], "content_hash": event["hash"]
        }]
        assert packet["chronology"]["records"] == [{
            "ref": packet["event_refs"][0], "time": event["clock"], "targets": [target["id"]],
        }]
        assert packet["actor_refs"] == []
        assert packet["authority"]["allowed_H_classes"] == ["H0"]
        assert first["status"] == "RUNNING"
        assert owner.lease(now=104) is None

        # A separate owner sees the durable attempt and can recover it only after expiry.
        concurrent = fanin_api.open(root)
        try:
            recovered = HistoricalWorld(concurrent.session)
            previous = recovered.lease(now=106)
            second = previous["job"]
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
                job_id, second["lease_token"], candidate, {"grade": "MOCK"}, now=107
            ) == "STALE"
            assert "candidate" not in recovered.job(job_id)
            new_event = concurrent.session.events()[-1]
            next_target = recovered.admit_surface(
                replace(surface, referent_key="fixture:another-tool",
                        location=there, occurrence_id=new_event["event_id"])
            )
            leased = recovered.lease(now=108)
            attempt, packet = leased["job"], leased["packet"]
            assert attempt["id"] == next_target["job_id"]
            def proposal(predicate, value, group):
                body = {"predicate": predicate, "value": value,
                        "target_id": next_target["id"], "dependency_group": group,
                        "effective_time": packet["time"], "asserted_H_class": "H0"}
                checksum = digest(body)
                return {"ref": {"kind": "FACT", "object_id": "proposal:" + checksum,
                                "content_hash": checksum}, **body}

            candidate = {
                "schema": "SOROK_HISTORY_ADMISSION_CANDIDATE@1",
                "request_id": attempt["id"],
                "facts": [proposal("texture", "matte", "valid"),
                          proposal("condition", "pristine", "contradiction")],
                "occurrences": [], "links": [],
                "dependencies": [
                    {"group_id": group, "parent_refs": packet["event_refs"],
                     "parent_groups": [], "asserted_H_class": "H0"}
                    for group in ("valid", "contradiction")
                ],
            }
            assert recovered.record_candidate(
                attempt["id"], attempt["lease_token"], candidate,
                {"grade": "MOCK"}, now=109
            ) == "CANDIDATE_READY"
            assert recovered.job(attempt["id"])["candidate"] == candidate
            assert recovered.target(next_target["id"]) == next_target
            admission = recovered.commit_candidate(attempt["id"])
            assert admission["status"] == "PARTIAL_HELD"
            assert recovered.commit_candidate(attempt["id"]) == admission
            assert {row["group_id"] for row in admission["accepted"]} == {"valid"}
            assert {row["group_id"] for row in admission["rejected"]} == {"contradiction"}
            depth = recovered.target(next_target["id"])["physical_depth"]
            assert depth["texture"]["value"] == "matte"
            assert depth["texture"]["parent_hash"] == new_event["hash"]
            with pytest.raises(HistoryRefusal, match="HISTORICAL_INSPECTION_NOT_PERCEIVED"):
                recovered.read_inspection(new_event["event_id"])
            seen = recovered.inspect(next_target["id"])
            assert recovered.read_inspection(seen["event_id"])["physical"] == [
                {"predicate": "texture", "value": "matte", "fact_id": depth["texture"]["id"]}
            ]
            assert "condition" not in depth

            retry = recovered.lease(now=110, seconds=5)
            assert retry["job"]["id"] == job_id
            assert retry["job"]["attempt"] == 3
            assert retry["packet"]["world_readset"] != previous["packet"]["world_readset"]
            assert retry["job"]["stale_attempts"] == [{
                "attempt": 2, "packet_hash": previous["job"]["packet_hash"],
                "provider_receipt": {"grade": "MOCK"},
            }]
            with pytest.raises(HistoryRefusal, match="HISTORICAL_ATTEMPT_NOT_CURRENT"):
                recovered.record_candidate(
                    job_id, second["lease_token"], {"request_id": job_id}, {}, now=111
                )
            assert recovered.lease(now=116) is None
            assert recovered.job(job_id)["status"] == "FAILED_TERMINAL"
        finally:
            concurrent.close()
        assert owner.target(next_target["id"])["physical_depth"] == depth
    finally:
        reopened.close()


def test_existing_p4_surface_reads_only_locally_perceived_particulars(tmp_path, monkeypatch):
    import json

    p4_dir = ENGINE.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
    monkeypatch.syspath_prepend(str(p4_dir))
    from argparse import Namespace
    from run_p4 import act, new, open_owner, surface as foreground_surface

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
        sibling = history.admit_surface(
            SurfaceParticular(event["event_id"], "fixture:collection-3", "collection",
                              there, {"count": 3}, ())
        )
        expected = {
            target["id"]: ("artifact", {"cover": "paper"}),
            sibling["id"]: ("collection", {"count": 3}),
        }
        assert {
            row["id"]: (row["domain"], row["physical"])
            for row in foreground_surface(owner, ledger)["historical_particulars"]
        } == expected

        # Checkpoints from before the index was added rebuild the same projection.
        with history._write() as (_, state):
            assert set(state.pop("targets_by_parent")[event["event_id"]]) == set(expected)
        assert {
            row["id"]: (row["domain"], row["physical"])
            for row in foreground_surface(owner, ledger)["historical_particulars"]
        } == expected
        session.travel(here)
        assert foreground_surface(owner, ledger)["historical_particulars"] == [tool]
        result = act(owner, ledger_file, ledger, Namespace(
            command="inspect-particular", target=tool["id"], request_id="look-1"))
        assert result["performed"]
        assert result["observation"]["target_id"] == tool["id"]
        assert result["observation"]["physical"] == []
        assert result["observation"]["physical_depth_status"] == "PENDING"
    finally:
        owner.close()


@pytest.mark.parametrize("resume", [False, True])
def test_cold_p4_inspects_admitted_background_depth(tmp_path, monkeypatch, resume):
    import asyncio
    import json
    import subprocess
    import sys

    p4_dir = ENGINE.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
    monkeypatch.syspath_prepend(str(p4_dir))
    from run_p4 import new, open_owner

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    target_id = opening["historical_particulars"][0]["id"]
    from rawlsing_next.sorok_history.provider import HistoricalModelProvider
    from rawlsing_next.sorok_history.runtime import run_once

    def proposal(packet):
        body = {"target_id": target_id, "predicate": "texture", "value": "matte",
                "effective_time": packet["time"], "dependency_group": "physical",
                "asserted_H_class": "H0"}
        checksum = digest(body)
        return {
            "request_id": packet["request_id"],
            "facts": [{**body, "ref": {"kind": "FACT", "object_id": "proposal:" + checksum,
                                      "content_hash": checksum}}],
            "occurrences": [], "links": [],
            "dependencies": [{"group_id": "physical", "parent_refs": packet["event_refs"],
                              "parent_groups": [], "asserted_H_class": "H0"}],
        }

    async def transport(request):
        assert not resume
        assert not owner.base_owner.fanin.session.product.store.db.in_transaction
        packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
        result = proposal(packet)
        del result["facts"][0]["ref"]
        return {"text": json.dumps(result), "model": "mock-history"}

    if resume:
        cli = [sys.executable, str(p4_dir / "run_p4.py"), "--state", str(tmp_path)]
        for key in ("SOROK_HISTORY_MODEL_ENDPOINT", "SOROK_HISTORY_ENDPOINT",
                    "SOROK_HISTORY_MODEL", "SOROK_HISTORY_MODEL_ID"):
            monkeypatch.delenv(key, raising=False)
        unconfigured = subprocess.run(
            cli + ["history-worker"], check=True, text=True, capture_output=True
        )
        assert json.loads(unconfigured.stdout) == {"status": "LIVE_PROVIDER_NOT_RUN"}
        owner = open_owner(tmp_path / "actual-p2")
        try:
            history = HistoricalWorld(owner.base_owner.fanin.session)
            leased = history.lease()
            job = leased["job"]
            assert history.record_candidate(
                job["id"], job["lease_token"], proposal(leased["packet"]), {"grade": "MOCK"}
            ) == "CANDIDATE_READY"
        finally:
            owner.close()

    owner = open_owner(tmp_path / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        if resume:
            resumed = subprocess.run(
                cli + ["history-worker"], check=True, text=True, capture_output=True
            )
            receipt = json.loads(resumed.stdout)
        else:
            receipt = asyncio.run(run_once(history, HistoricalModelProvider(transport=transport)))
            assert history.job(receipt["job_id"])["provider_receipt"]["mode"] == "MOCK"
        assert receipt["status"] == "INDEX_READY"
    finally:
        owner.close()

    cli = [sys.executable, str(p4_dir / "run_p4.py"), "--state", str(tmp_path)]
    view = subprocess.run(cli + ["view"], check=True, text=True, capture_output=True)
    assert "matte" not in view.stdout
    args = cli + ["inspect-particular", target_id, "--request-id", "cold-inspect"]
    inspection = subprocess.run(args, check=True, text=True, capture_output=True)
    observation = json.loads(inspection.stdout)["observation"]
    assert observation["physical_depth_status"] == "OBSERVED"
    [fact] = observation["physical"]
    assert fact["value"] == "matte"
    assert fact["fact_id"] == receipt["accepted"][0]["fact_ids"][0]
    replay = subprocess.run(args, check=True, text=True, capture_output=True)
    assert json.loads(replay.stdout) == json.loads(inspection.stdout)

    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        current = session.world().positions[session.meta["user_actor"]]
        session.travel("market" if current == "workshop" else "workshop")
    finally:
        owner.close()
    changed = subprocess.run(cli + ["view"], text=True, capture_output=True)
    assert changed.returncode == 2
    assert json.loads(changed.stdout)["reason"] == "P4_COLD_STATE_MISMATCH"
