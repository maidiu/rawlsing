"""T4 proof: independent S46 activity consumes owner-admitted depth."""

import asyncio
import json
from pathlib import Path

from rawlsing_next.sorok_history.activity import (
    ADVANCED,
    DEPTH_MISSING,
    HELD,
    advance_independent_activity,
    dispatch_activity_requirement,
    produce_activity_requirement,
)
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest
from rawlsing_next.sorok_history.runtime import run_once


P4 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P4-FIRST-FULL-MPC-R1")
P3 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1")
ENGINE = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
          / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1")


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
    """In-process parent-event read severance; this is not a cold fixture."""
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
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
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
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


def test_d4_cold_detached_depth_holds_and_restore_requalifies(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import advance_dispatched, new, open_owner

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        admission = asyncio.run(run_once(history, _mock_provider(target_id)))
        assert admission["status"] == "INDEX_READY"
        fact = history.target(target_id)["physical_depth"]["condition"]
        detached = history.test_detach_physical_depth(target_id, "condition")
        assert detached == fact
    finally:
        owner.close()

    cold = open_owner(tmp_path / "actual-p2")
    try:
        fanin = cold.base_owner.fanin
        history = HistoricalWorld(fanin.session)
        held = advance_dispatched(fanin)
        assert held["status"] == HELD
        assert held["activity"]["refusal_code"] == DEPTH_MISSING
        assert held["activity"]["interval"] is None
        assert fanin.session.world().actor_state["A"]["material_remaining"] == 1
        assert not _actual_intervals(fanin.session)
        history.test_restore_physical_depth(target_id, detached)
    finally:
        cold.close()

    restored = open_owner(tmp_path / "actual-p2")
    try:
        fanin = restored.base_owner.fanin
        advanced = advance_dispatched(fanin)
        assert advanced["status"] == ADVANCED
        assert fanin.session.world().actor_state["A"]["material_remaining"] == 0
        [actual] = _actual_intervals(fanin.session)
        assert actual["status"] == "PARTIAL"
    finally:
        restored.close()


def test_d5_wrong_place_and_resource_hold_before_interval(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import new, open_owner
    from rawlsing_next.sorok_history.activity import dispatch_activity_requirement

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    target_id = tool["id"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        assert asyncio.run(run_once(history, _mock_provider(target_id)))["status"] == "INDEX_READY"

        history.test_set_actor_position("A", "market")
        wrong_place = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert wrong_place.status == HELD
        assert wrong_place.activity.refusal_code == "HISTORICAL_MATERIAL_NOT_IN_ACTIVITY_PLACE"
        assert wrong_place.activity.interval is None
        assert not _actual_intervals(session)

        history.test_set_actor_position("A", "workshop")
        history.test_set_resource_property("workshop", "condition", "broken")
        wrong_resource = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert wrong_resource.status == HELD
        assert wrong_resource.activity.refusal_code == "HISTORICAL_MATERIAL_WORLD_MISMATCH"
        assert wrong_resource.activity.interval is None
        assert session.world().actor_state["A"]["material_remaining"] == 1

        history.test_set_resource_property("workshop", "condition", "serviceable")
        advanced = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert advanced.status == ADVANCED
        assert session.world().actor_state["A"]["material_remaining"] == 0
    finally:
        owner.close()


def test_d5_cross_root_requirement_is_not_admitted(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import new, open_owner
    from rawlsing_next.sorok_history.activity import dispatch_activity_requirement

    monkeypatch.syspath_prepend(str(ENGINE))
    from developmental_recursion.p2_owner import load_p2

    foreign = tmp_path / "foreign-root"
    foreign_fanin = load_p2().start(foreign, seed="02" * 32)
    try:
        foreign_history = HistoricalWorld(foreign_fanin.session)
        foreign_history.capture_visible_tool_resource()
        foreign_requirement = produce_activity_requirement(foreign_fanin, foreign_history)
        foreign_root = foreign_history.scope()[0]
    finally:
        foreign_fanin.close()

    new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        assert history.scope()[0] != foreign_root
        try:
            dispatch_activity_requirement(fanin, history, foreign_requirement["id"])
        except Exception as exc:
            assert str(exc) == "ACTIVITY_REQUIREMENT_NOT_RECORDED"
        else:
            raise AssertionError("foreign root requirement was admitted")
        assert not _actual_intervals(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert history.activity_requirement(foreign_requirement["id"]) is None

        # A genuinely recorded foreign-scope requirement keeps valid target
        # resolution and changes only root/branch scope. It must fail closed for
        # the scope violation, not because its target is merely unknown.
        current = produce_activity_requirement(fanin, history)
        foreign_scope = {
            **current,
            "id": current["id"] + ":foreign-scope",
            "root": foreign_root,
            "branch": "foreign-branch",
        }
        history.hold_activity_requirement(foreign_scope)
        recorded = dispatch_activity_requirement(
            fanin, history, foreign_scope["id"]
        )
        assert recorded.status == HELD
        assert recorded.reason == "HISTORICAL_ACTIVITY_REQUIREMENT_STALE"
        assert recorded.activity.interval is None
        assert history.target(foreign_scope["target_id"]) is not None
        assert not _actual_intervals(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert history.activity_requirement(foreign_scope["id"])["status"] == HELD
    finally:
        owner.close()


def test_d8_user_hypothesis_does_not_change_activity_requirement(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import advance_dispatched, new, open_owner
    from speech import admit_speech

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    held = _work_cli(tmp_path, monkeypatch)
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        [before] = history.activity_requirements("HELD")
        admit_speech(
            session, text="Suppose the tool is broken.",
            actor_ref=owner.snapshot().document()["actor"], request_edge=False,
        )
        session.attend()
        [after] = history.activity_requirements("HELD")
        assert after["id"] == before["id"]
        assert after["expected"] == "serviceable"
        result = advance_dispatched(fanin)
        assert result["status"] == HELD
        assert result["activity"]["refusal_code"] == DEPTH_MISSING
        assert not _actual_intervals(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert history.target(tool["id"]).get("physical_depth", {}) == {}
    finally:
        owner.close()


def test_d10_child_branch_pending_admission_consumption_and_parent_readback(
    tmp_path, monkeypatch
):
    import copy
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import advance_dispatched, new, open_owner
    from rawlsing_next.sorok_history.activity import resume_activity_requirements

    new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        parent = session.branch_id
        parent_history = HistoricalWorld(session)
        parent_requirement = produce_activity_requirement(fanin, parent_history)
        assert advance_dispatched(fanin)["status"] == HELD

        def read_branch(branch):
            session.product.use(branch)
            session.branch_id = branch
            return HistoricalWorld(session), session.world().actor_state["A"]["material_remaining"]

        def read_parent():
            history, material = read_branch(parent)
            assert history.activity_requirement(parent_requirement["id"])["status"] == HELD
            assert [row["id"] for row in history.activity_requirements()] == [
                parent_requirement["id"]
            ]
            assert history.target(child_target_id) is None
            assert material == 1
            assert not [
                row for row in session.read_interval_states()
                if (row.get("domain") or {}).get("mode") == "ACTUAL"
            ]

        def read_sibling():
            history, material = read_branch(sibling)
            assert history.activity_requirements() == ()
            assert history.target(child_target_id) is None
            assert material == 1
            assert session.clock() == 230

        # Sibling and child are both forks of the parent. Create the sibling
        # first, then restore the saved parent lineage before forking the child.
        parent_meta = copy.deepcopy(session.meta)
        session.fork_alt("t4-sibling")
        sibling = session.branch_id
        session.product.use(parent)
        session.branch_id = parent
        session.meta = parent_meta
        session.fork_alt("t4-child")
        child = session.branch_id
        child_history = HistoricalWorld(session)
        child_target_id = child_history.capture_visible_tool_resource()
        assert child_target_id
        child_requirement = produce_activity_requirement(fanin, child_history)
        assert child_requirement["id"] != parent_requirement["id"]
        assert advance_dispatched(fanin)["status"] == HELD

        read_parent()
        read_sibling()
        session.product.use(child)
        session.branch_id = child

        session.product.use(child)
        session.branch_id = child
        child_history = HistoricalWorld(session)
        assert asyncio.run(run_once(child_history, _mock_provider(child_target_id)))["status"] == "INDEX_READY"
        read_parent()
        read_sibling()
        session.product.use(child)
        session.branch_id = child
        resumed = resume_activity_requirements(fanin, child_history)
        assert [row.status for row in resumed] == [ADVANCED]
        assert session.world().actor_state["A"]["material_remaining"] == 0
        assert child_history.activity_requirement(child_requirement["id"])["status"] == "CONSUMED"

        read_parent()
        read_sibling()
        session.product.use(child)
        session.branch_id = child
        assert session.world().actor_state["A"]["material_remaining"] == 0
        assert HistoricalWorld(session).activity_requirement(parent_requirement["id"]) is None
    finally:
        owner.close()


def _run_process_script(script, state):
    import os
    import subprocess
    import sys

    process = subprocess.run(
        [sys.executable, "-c", script, str(P4.parents[1]), str(state)],
        capture_output=True, text=True, timeout=180,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert process.returncode == 0, process.stderr
    return json.loads(process.stdout)


_ADMIT_AND_CRASH = r'''
import asyncio, json, sys
from pathlib import Path
repo = Path(sys.argv[1]); state = Path(sys.argv[2])
sys.path[:0] = [str(repo), str(repo / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"),
                str(repo / "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests")]
from run_p4 import open_owner
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest
from rawlsing_next.sorok_history.provider import HistoricalModelProvider
from rawlsing_next.sorok_history.runtime import run_once
from rawlsing_next.sorok_history.activity import dispatch_activity_requirement
owner = open_owner(state / "actual-p2")
fanin = owner.base_owner.fanin; history = HistoricalWorld(fanin.session)
requirement = history.activity_requirements("HELD")[0]
target_id = requirement["target_id"]
async def transport(request):
    packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
    body = {"target_id": target_id, "predicate": "condition", "value": "serviceable",
            "effective_time": packet["time"], "dependency_group": "physical",
            "asserted_H_class": "H0"}
    checksum = digest(body)
    body["ref"] = {"kind": "FACT", "object_id": "proposal:" + checksum,
                   "content_hash": checksum}
    return {"text": json.dumps({"request_id": packet["request_id"], "facts": [body],
            "occurrences": [], "links": [], "dependencies": [{"group_id": "physical",
            "parent_refs": packet["event_refs"], "parent_groups": [],
            "asserted_H_class": "H0"}]}), "model": "mock-history"}
assert asyncio.run(run_once(history, HistoricalModelProvider(transport=transport)))["status"] == "INDEX_READY"
original = HistoricalWorld.mark_activity_requirement
def fail(self, requirement_id, status, *, receipt=None):
    if status == "CONSUMED":
        raise RuntimeError("injected crash after interval")
    return original(self, requirement_id, status, receipt=receipt)
HistoricalWorld.mark_activity_requirement = fail
try:
    dispatch_activity_requirement(fanin, history, requirement["id"])
except RuntimeError:
    pass
actual = [row for row in fanin.session.read_interval_states()
          if (row.get("domain") or {}).get("mode") == "ACTUAL"]
print(json.dumps({"requirement": history.activity_requirement(requirement["id"])["status"],
                  "material": fanin.session.world().actor_state["A"]["material_remaining"],
                  "clock": fanin.session.clock(), "actual": len(actual)}))
owner.close()
'''

_RESUME = r'''
import json, sys
from pathlib import Path
repo = Path(sys.argv[1]); state = Path(sys.argv[2])
sys.path[:0] = [str(repo), str(repo / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"),
                str(repo / "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests")]
from run_p4 import open_owner
from rawlsing_next.sorok_history.owner import HistoricalWorld
from rawlsing_next.sorok_history.activity import resume_activity_requirements
owner = open_owner(state / "actual-p2")
fanin = owner.base_owner.fanin; history = HistoricalWorld(fanin.session)
results = resume_activity_requirements(fanin, history)
actual = [row for row in fanin.session.read_interval_states()
          if (row.get("domain") or {}).get("mode") == "ACTUAL"]
print(json.dumps({"statuses": [row.status for row in results],
                  "reasons": [row.reason for row in results],
                  "fact_ids": [row.activity.fact_id if row.activity else None
                               for row in results],
                  "material": fanin.session.world().actor_state["A"]["material_remaining"],
                  "clock": fanin.session.clock(), "actual": len(actual),
                  "requirements": [row["status"] for row in history.activity_requirements()]}))
owner.close()
'''


def test_d6_separate_process_crash_after_interval_recovers_without_double_use(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import new

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    assert _work_cli(tmp_path, monkeypatch)["status"] == HELD
    crashed = _run_process_script(_ADMIT_AND_CRASH, tmp_path)
    assert crashed["requirement"] == "DISPATCHING"
    assert crashed["material"] == 0
    assert crashed["actual"] == 1

    recovered = _run_process_script(_RESUME, tmp_path)
    assert recovered["statuses"] == ["ADVANCED"]
    assert recovered["reasons"] == ["HISTORICAL_ACTIVITY_DISPATCH_RECOVERED"]
    assert recovered["fact_ids"] and recovered["fact_ids"][0]
    assert recovered["material"] == 0
    assert recovered["clock"] == 232
    assert recovered["actual"] == 1
    assert recovered["requirements"] == ["CONSUMED"]

    replay = _run_process_script(_RESUME, tmp_path)
    assert replay["statuses"] == []
    assert replay["material"] == 0
    assert replay["actual"] == 1

_ADMIT_AND_CRASH_BEFORE = r'''
import asyncio, json, sys
from pathlib import Path
repo = Path(sys.argv[1]); state = Path(sys.argv[2])
sys.path[:0] = [str(repo), str(repo / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"),
                str(repo / "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests")]
from run_p4 import open_owner
from rawlsing_next.sorok_history.owner import HistoricalWorld, digest
from rawlsing_next.sorok_history.provider import HistoricalModelProvider
from rawlsing_next.sorok_history.runtime import run_once
import rawlsing_next.sorok_history.activity as activity
owner = open_owner(state / "actual-p2")
fanin = owner.base_owner.fanin; history = HistoricalWorld(fanin.session)
requirement = history.activity_requirements("HELD")[0]
target_id = requirement["target_id"]
async def transport(request):
    packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
    body = {"target_id": target_id, "predicate": "condition", "value": "serviceable",
            "effective_time": packet["time"], "dependency_group": "physical",
            "asserted_H_class": "H0"}
    checksum = digest(body)
    body["ref"] = {"kind": "FACT", "object_id": "proposal:" + checksum,
                   "content_hash": checksum}
    return {"text": json.dumps({"request_id": packet["request_id"], "facts": [body],
            "occurrences": [], "links": [], "dependencies": [{"group_id": "physical",
            "parent_refs": packet["event_refs"], "parent_groups": [],
            "asserted_H_class": "H0"}]}), "model": "mock-history"}
assert asyncio.run(run_once(history, HistoricalModelProvider(transport=transport)))["status"] == "INDEX_READY"
def crash(*args, **kwargs):
    raise RuntimeError("injected crash before interval")
activity._default_advance = crash
try:
    activity.dispatch_activity_requirement(fanin, history, requirement["id"])
except RuntimeError:
    pass
actual = [row for row in fanin.session.read_interval_states()
          if (row.get("domain") or {}).get("mode") == "ACTUAL"]
print(json.dumps({"requirement": history.activity_requirement(requirement["id"])["status"],
                  "material": fanin.session.world().actor_state["A"]["material_remaining"],
                  "actual": len(actual)}))
owner.close()
'''


def test_d6_crash_before_interval_redispaches_once(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import new

    state = tmp_path / "before"
    new(state, state / "p4_receipts.json", "recognized_plan")
    assert _work_cli(state, monkeypatch)["status"] == HELD
    crashed = _run_process_script(_ADMIT_AND_CRASH_BEFORE, state)
    assert crashed == {"requirement": "DISPATCHING", "material": 1, "actual": 0}
    recovered = _run_process_script(_RESUME, state)
    assert recovered["statuses"] == ["ADVANCED"]
    assert recovered["actual"] == 1
    assert recovered["material"] == 0
    assert recovered["requirements"] == ["CONSUMED"]


def test_d10_separate_root_state_consumption_isolated(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import new, open_owner, run_history_worker

    one = tmp_path / "one"
    two = tmp_path / "two"
    opening = new(one, one / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    new(two, two / "p4_receipts.json", "recognized_plan")
    assert _work_cli(one, monkeypatch)["status"] == HELD
    result = run_history_worker(
        one, provider=_mock_provider(tool["id"], "serviceable")
    )
    assert result["status"] == "INDEX_READY"
    [activity] = result["activity"]
    assert activity["status"] == ADVANCED

    other = open_owner(two / "actual-p2")
    try:
        session = other.base_owner.fanin.session
        history = HistoricalWorld(session)
        assert session.world().actor_state["A"]["material_remaining"] == 1
        assert history.activity_requirements() == ()
        assert not _actual_intervals(session)
        assert history.target(tool["id"]).get("physical_depth", {}) == {}
    finally:
        other.close()


def test_d6_same_start_unrelated_interval_is_not_credited(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P4))
    monkeypatch.syspath_prepend(str(P3 / "tests"))
    from run_p4 import advance, new, open_owner
    from rawlsing_next.sorok_history.activity import dispatch_activity_requirement

    new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        history.mark_activity_requirement(requirement["id"], "DISPATCHING")
        unrelated = advance(fanin)
        [actual] = _actual_intervals(session)
        assert actual["domain"]["start"] == requirement["required_at"]
        assert actual["domain"].get("activity_requirement_ref") is None
        assert unrelated["status"] in {"PARTIAL", "REALIZED"}

        result = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert result.status == HELD
        assert result.activity.refusal_code == DEPTH_MISSING
        assert result.activity.interval is None
        assert result.activity.fact_id is None
        stored = history.activity_requirement(requirement["id"])
        assert stored["status"] == HELD
        assert stored.get("dispatch_receipt", {}).get("fact_id") is None
        assert len(_actual_intervals(session)) == 1
    finally:
        owner.close()


def test_d6_ambiguous_recovery_is_durable_and_not_retried(tmp_path, monkeypatch):
    from run_p4 import advance, new, open_owner
    from rawlsing_next.sorok_history.activity import (
        AMBIGUOUS, dispatch_activity_requirement, resume_activity_requirements,
    )

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        assert asyncio.run(run_once(history, _mock_provider(tool["id"])))["status"] == "INDEX_READY"
        history.mark_activity_requirement(requirement["id"], "DISPATCHING")
        advance(fanin, dispatch_ref=requirement["id"])
        [matching] = [
            row for row in session.read_interval_states()
            if (row.get("domain") or {}).get("activity_requirement_ref") == requirement["id"]
        ]
        real_read = session.read_interval_states
        session.read_interval_states = lambda: [matching, matching]
        ambiguous = dispatch_activity_requirement(fanin, history, requirement["id"])
        assert ambiguous.status == HELD
        assert ambiguous.reason == "HISTORICAL_ACTIVITY_RECOVERY_AMBIGUOUS"
        assert history.activity_requirement(requirement["id"])["status"] == AMBIGUOUS
        session.read_interval_states = real_read
        assert len(_actual_intervals(session)) == 1
        assert resume_activity_requirements(fanin, history) == ()
        assert history.activity_requirement(requirement["id"])["status"] == AMBIGUOUS
        assert len(_actual_intervals(session)) == 1
    finally:
        owner.close()

    cold = open_owner(tmp_path / "actual-p2")
    try:
        fanin = cold.base_owner.fanin
        history = HistoricalWorld(fanin.session)
        assert history.activity_requirement(requirement["id"])["status"] == AMBIGUOUS
        assert resume_activity_requirements(fanin, history) == ()
        assert len(_actual_intervals(fanin.session)) == 1
        assert history.activity_requirement(requirement["id"])["status"] == AMBIGUOUS
    finally:
        cold.close()


def test_d6_old_ambiguous_held_is_rechecked_not_retried(tmp_path, monkeypatch):
    from run_p4 import advance, new, open_owner
    from rawlsing_next.sorok_history.activity import (
        AMBIGUOUS, dispatch_activity_requirement, resume_activity_requirements,
    )

    opening = new(tmp_path, tmp_path / "p4_receipts.json", "recognized_plan")
    [tool] = opening["historical_particulars"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        history = HistoricalWorld(session)
        requirement = produce_activity_requirement(fanin, history)
        assert asyncio.run(run_once(history, _mock_provider(tool["id"])))["status"] == "INDEX_READY"
        history.mark_activity_requirement(requirement["id"], "DISPATCHING")
        advance(fanin, dispatch_ref=requirement["id"])
        [matching] = [
            row for row in session.read_interval_states()
            if (row.get("domain") or {}).get("activity_requirement_ref") == requirement["id"]
        ]
        history.mark_activity_requirement(
            requirement["id"], "HELD",
            receipt={"refusal_code": "HISTORICAL_ACTIVITY_RECOVERY_AMBIGUOUS"},
        )
        real_read = session.read_interval_states
        session.read_interval_states = lambda: [matching, matching]
        results = resume_activity_requirements(fanin, history)
        assert len(results) == 1
        assert results[0].status == HELD
        assert results[0].reason == "HISTORICAL_ACTIVITY_RECOVERY_AMBIGUOUS"
        assert history.activity_requirement(requirement["id"])["status"] == AMBIGUOUS
        session.read_interval_states = real_read
        assert len(_actual_intervals(session)) == 1
        assert resume_activity_requirements(fanin, history) == ()
    finally:
        owner.close()
