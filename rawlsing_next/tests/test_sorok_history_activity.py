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


def _proposal(packet, target_id):
    fact = {
        "target_id": target_id, "predicate": "condition", "value": "serviceable",
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
