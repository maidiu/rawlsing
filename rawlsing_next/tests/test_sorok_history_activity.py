"""T4 proof: independent S46 activity consumes owner-admitted depth."""

import asyncio
import json
from pathlib import Path

from rawlsing_next.sorok_history.activity import (
    ADVANCED,
    DEPTH_MISSING,
    HELD,
    advance_independent_activity,
)
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest


P4 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P4-FIRST-FULL-MPC-R1")
P3 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1")


def _actual_intervals(session):
    return [
        row for row in session.read_interval_states()
        if (row.get("domain") or {}).get("mode") == "ACTUAL"
    ]


def test_owner_admitted_depth_holds_absent_then_advances_real_s46_without_observation(
    tmp_path, monkeypatch
):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))

    from run_p4 import new, open_owner

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    assert tool["domain"] == "resource"

    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        clock_before = session.clock()
        perceived_before = set(session.user_perceived_ids())
        material_before = session.world().actor_state["A"]["material_remaining"]
        [job] = history.pending()
        assert job["target_id"] == target_id
        assert job["status"] == "ENQUEUED"

        # The same-world depth is absent until the existing history worker
        # admits the provider proposal. No private surface write is used.
        absent = advance_independent_activity(
            fanin, history, target_id=target_id,
            predicate="condition", expected="serviceable",
        )
        assert absent.status == HELD
        assert absent.refusal_code == DEPTH_MISSING
        assert absent.interval is None
        assert absent.clock_after == absent.clock_before == clock_before
        assert absent.material_after == absent.material_before == material_before
        assert not _actual_intervals(session)

        from rawlsing_next.sorok_history.provider import HistoricalModelProvider
        from rawlsing_next.sorok_history.runtime import run_once

        async def transport(request):
            packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
            return {"text": json.dumps(_proposal(packet, target_id)),
                    "model": "mock-history"}

        admission = asyncio.run(
            run_once(history, HistoricalModelProvider(transport=transport))
        )
        assert admission["status"] == "INDEX_READY"

        target = history.target(target_id)
        fact = target["physical_depth"]["condition"]
        job_after = history.job(job["id"])
        accepted_ids = {
            fact_id for group in job_after["admission"]["accepted"]
            for fact_id in group["fact_ids"]
        }
        assert fact["value"] == "serviceable"
        assert fact["job_id"] == job["id"]
        assert fact["id"] in accepted_ids
        assert job_after["status"] == "INDEX_READY"
        assert job_after["admission"]["status"] == "INDEX_READY"
        assert fact["parent_event_ref"]["object_id"] == target["surface"]["occurrence_id"]
        assert fact["parent_event_ref"]["content_hash"] == target["parent_hash"]

        advanced = advance_independent_activity(
            fanin, history, target_id=target_id,
            predicate="condition", expected="serviceable",
        )
        assert advanced.status == ADVANCED
        assert advanced.refusal_code is None
        assert advanced.fact_id == fact["id"]
        assert advanced.job_id == job["id"]
        assert advanced.job_status == "INDEX_READY"
        assert advanced.admission_status == "INDEX_READY"
        assert advanced.fact_parent_event_ref == fact["parent_event_ref"]
        assert advanced.fact_claim_ref == fact["claim_ref"]
        assert advanced.target_version == target["version"]
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
        assert not any(event["kind"] == "INSPECT" for event in session.events())
        assert set(session.user_perceived_ids()) == perceived_before
        assert advanced.as_dict()["property_source"] == "physical_depth"
        assert json.loads(json.dumps(advanced.as_dict()))["fact_id"] == fact["id"]
    finally:
        owner.close()


def _mock_provider(target_id, value="serviceable"):
    from rawlsing_next.sorok_history.provider import HistoricalModelProvider

    async def transport(request):
        packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
        return {"text": json.dumps(_proposal(packet, target_id, value=value)),
                "model": "mock-history"}

    return HistoricalModelProvider(transport=transport)


def _proposal(packet, target_id, *, value="serviceable"):
    fact = {
        "target_id": target_id, "predicate": "condition", "value": value,
        "effective_time": packet["time"], "dependency_group": "physical",
        "asserted_H_class": "H0",
    }
    checksum = digest(fact)
    fact["ref"] = {
        "kind": "FACT", "object_id": "proposal:" + checksum,
        "content_hash": checksum,
    }
    return {
        "request_id": packet["request_id"], "facts": [fact],
        "occurrences": [], "links": [],
        "dependencies": [{
            "group_id": "physical", "parent_refs": packet["event_refs"],
            "parent_groups": [], "asserted_H_class": "H0",
        }],
    }


def _work_cli(state, monkeypatch):
    import subprocess
    import sys

    monkeypatch.syspath_prepend(str(P4))
    process = subprocess.run(
        [sys.executable, str(P4 / "run_p4.py"), "--state", str(state), "work"],
        capture_output=True, text=True, timeout=120,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert process.returncode == 0, process.stderr
    return json.loads(process.stdout)


def test_d1_normal_work_cli_holds_missing_depth_and_survives_reopen(tmp_path, monkeypatch):
    from run_p4 import new, open_owner

    new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    held = _work_cli(tmp_path, monkeypatch)
    assert held["status"] == HELD
    assert held["requirement"]["status"] == HELD
    assert held["activity"]["status"] == HELD
    assert held["activity"]["refusal_code"] == DEPTH_MISSING
    assert held["activity"]["interval"] is None

    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        history = HistoricalWorld(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert session.clock() == 230
        assert not _actual_intervals(session)
        [requirement] = history.activity_requirements("HELD")
        assert requirement["target_id"] == held["requirement"]["target_id"]
        assert requirement["parent_event_ref"]["object_id"]
    finally:
        owner.close()

    reopened = open_owner(tmp_path / "actual-p2")
    try:
        history = HistoricalWorld(reopened.base_owner.fanin.session)
        assert history.activity_requirement(held["requirement"]["id"])["status"] == HELD
        repeated = _work_cli(tmp_path, monkeypatch)
        assert repeated["status"] == HELD
        assert repeated["activity"]["interval"] is None
    finally:
        reopened.close()


def test_d2_worker_admission_resumes_normal_dispatch_once(tmp_path, monkeypatch):
    from run_p4 import new, open_owner, run_history_worker

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    held = _work_cli(tmp_path, monkeypatch)
    assert held["status"] == HELD

    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        perceived_before = set(session.user_perceived_ids())
    finally:
        owner.close()

    result = run_history_worker(
        tmp_path, provider=_mock_provider(target_id, "serviceable")
    )
    assert result["status"] == "INDEX_READY"
    [activity] = result["activity"]
    assert activity["status"] == ADVANCED
    assert activity["activity"]["status"] == ADVANCED
    assert activity["activity"]["fact_id"]
    assert activity["activity"]["job_id"] == held["requirement"]["job_id"]
    assert activity["activity"]["fact_parent_event_ref"]["object_id"]
    assert activity["activity"]["fact_claim_ref"]["object_id"]

    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        [requirement] = history.activity_requirements()
        assert requirement["status"] == "CONSUMED"
        assert session.world().actor_state["A"]["material_remaining"] == 0
        assert session.clock() == 232
        actual = _actual_intervals(session)
        assert len(actual) == 1
        assert actual[0]["status"] == "PARTIAL"
        assert not any(event["kind"] == "INSPECT" for event in session.events())
        assert set(session.user_perceived_ids()) == perceived_before
        assert session.world().actor_state["A"]["material_remaining"] == 0
        from rawlsing_next.sorok_history.activity import dispatch_activity_requirement
        replay = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert replay.status == HELD
        assert replay.reason == "HISTORICAL_ACTIVITY_REQUIREMENT_CONSUMED"
        assert replay.activity is None
        assert session.world().actor_state["A"]["material_remaining"] == 0
    finally:
        owner.close()


def test_d3_incompatible_admitted_value_holds_and_consumes_nothing(tmp_path, monkeypatch):
    from run_p4 import new, open_owner, run_history_worker

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    assert _work_cli(tmp_path, monkeypatch)["status"] == HELD

    result = run_history_worker(
        tmp_path, provider=_mock_provider(target_id, "broken")
    )
    assert result["status"] == "INDEX_READY"
    [activity] = result["activity"]
    assert activity["status"] == HELD
    assert activity["activity"]["refusal_code"] == "HISTORICAL_DEPTH_VALUE_MISMATCH"

    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        history = HistoricalWorld(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert session.clock() == 230
        assert not _actual_intervals(session)
        [requirement] = history.activity_requirements()
        assert requirement["status"] == HELD
    finally:
        owner.close()


def test_d4_exact_parent_severance_holds_then_restores_requalification(tmp_path, monkeypatch):
    from run_p4 import advance_dispatched, new, open_owner
    from rawlsing_next.sorok_history.activity import produce_activity_requirement
    from rawlsing_next.sorok_history.runtime import run_once

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        admission = asyncio.run(
            run_once(history, _mock_provider(target_id, "serviceable"))
        )
        assert admission["status"] == "INDEX_READY"
        target = history.target(target_id)
        parent_id = target["surface"]["occurrence_id"]
        real_event = session.event

        with monkeypatch.context() as patch:
            patch.setattr(session, "event", lambda event_id: (
                None if event_id == parent_id else real_event(event_id)
            ))
            held = advance_dispatched(fanin)
        assert held["status"] == HELD
        assert held["activity"]["refusal_code"] == "HISTORICAL_PARENT_MISSING"
        assert held["activity"]["interval"] is None
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert not _actual_intervals(session)

        restored = advance_dispatched(fanin)
        assert restored["status"] == ADVANCED
        assert restored["activity"]["status"] == ADVANCED
        assert session.world().actor_state["A"]["material_remaining"] == 0
        [actual] = _actual_intervals(session)
        assert actual["status"] == "PARTIAL"
    finally:
        owner.close()



def test_d5_forged_requirement_scope_holds_before_interval(tmp_path, monkeypatch):
    from run_p4 import new, open_owner
    from rawlsing_next.sorok_history.activity import (
        dispatch_activity_requirement, produce_activity_requirement,
    )

    new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        forged = {
            **requirement,
            "id": requirement["id"] + ":forged",
            "target_id": "history-target:missing",
            "job_id": "history-job:missing",
            "root": "other-root",
        }
        history.hold_activity_requirement(forged)
        held = dispatch_activity_requirement(fanin, history, forged["id"])
        assert held.status == HELD
        assert held.activity.refusal_code == "HISTORICAL_ACTIVITY_REQUIREMENT_STALE"
        assert held.activity.interval is None
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert not _actual_intervals(session)
    finally:
        owner.close()


def test_d9_model_failure_cannot_authorize_activity(tmp_path, monkeypatch):
    from run_p4 import new, open_owner, run_history_worker
    from rawlsing_next.sorok_history.provider import (
        HistoricalModelProvider, ProviderTimeout,
    )

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    assert _work_cli(tmp_path, monkeypatch)["status"] == HELD

    async def transport(_request):
        raise ProviderTimeout("model unavailable")

    result = run_history_worker(
        tmp_path, provider=HistoricalModelProvider(transport=transport)
    )
    assert result["status"] in {"FAILED_RETRYABLE", "FAILED_TERMINAL"}
    [activity] = result["activity"]
    assert activity["status"] == HELD
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert not _actual_intervals(session)
    finally:
        owner.close()
