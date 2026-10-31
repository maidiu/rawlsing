from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

import f1c
import targetless_c10_consumer as T


def eval_receipt():
    body = {"decision_state": "NO_CHANGE", "rule_ref": "TEST_ONLY_I1_NO_CHANGE_RULE",
            "evaluated_at_tick": 251}
    body["receipt_hash"] = T.digest(body)
    return body


def test_i1_market_work_requires_prior_stock_or_refusal():
    with pytest.raises(T.ContinuityRefusal, match="MATERIAL_EXHAUSTED"):
        T.MaterialLedger.consume(
            stock_before=0, replenish=0, consume=1, hours_before=10,
            hours_after=9, tick=40,
        )
    balanced = T.MaterialLedger.consume(
        stock_before=0, replenish=1, consume=1, hours_before=10,
        hours_after=9, tick=40, replenishment_ref="TESTONLY_I1_PRIOR_STOCK",
    )
    assert balanced.state == "MATERIAL_BALANCED"
    assert (balanced.stock_before, balanced.replenished, balanced.consumed,
            balanced.stock_after) == (0, 1, 1, 0)
    assert balanced.receipt["clamped"] is False
    assert [e["kind"] for e in balanced.events] == [
        "MATERIAL_REPLENISHMENT", "I1_MARKET_WORK"
    ]
    refused = T.MaterialLedger.explicit_refusal(
        stock_before=0, replenish=0, hours_before=10, tick=40,
    )
    assert refused.state == "REFUSED_MATERIAL_EXHAUSTED"
    assert refused.consumed == 0 and refused.stock_after == 0
    non_stock = T.MaterialLedger.consume(
        stock_before=0, replenish=0, consume=0, hours_before=10,
        hours_after=10, tick=40, work_ref="B_TOOL_ACTION_NO_MATERIAL",
    )
    assert non_stock.stock_after == 0 and non_stock.consumed == 0


def test_refuse_silence_and_no_proposal_are_distinct_targetless_states():
    world = T.BWorld()
    refuse = T.TargetlessC10Ledger.build(world.action("REFUSE"))
    silence = T.TargetlessC10Ledger.build(world.action("SILENCE"))
    no_prop = T.TargetlessC10Ledger.build(world.action("NO_PROPOSAL"))
    assert refuse.state == "TARGETLESS_REFUSE"
    assert silence.state == "TARGETLESS_SILENCE"
    assert no_prop.state == "TARGETLESS_NO_PROPOSAL"
    assert refuse.action.performer == "B" and refuse.action.performed
    assert silence.action.performer is None and not silence.action.performed
    assert no_prop.action.performer is None and not no_prop.action.performed
    assert refuse.action.a_event_access is True
    assert silence.action.a_event_access is False
    assert no_prop.action.a_event_access is False
    for ledger in (refuse, silence, no_prop):
        assert ledger.c9_proposal is None and ledger.c9_target is None
        assert ledger.performed_e2 is False and ledger.learned_practice is False
        assert ledger.utterance is None and ledger.tick_after > ledger.tick_before
        assert ledger.receipt["receipt_hash"]
    assert len({refuse.receipt["receipt_hash"], silence.receipt["receipt_hash"],
                no_prop.receipt["receipt_hash"]}) == 3


def test_observed_vs_unobserved_access_differs():
    world = T.BWorld()
    observed = T.TargetlessC10Ledger.build(world.action("SHARE", observed=True))
    unobserved = T.TargetlessC10Ledger.build(world.action("SHARE", observed=False))
    a = T.ContinuingPerson()
    a.consume(observed)
    b = T.ContinuingPerson()
    b.consume(unobserved)
    ra, rb = a.read_later(), b.read_later()
    assert ra["can_read_B_behavior"] is True
    assert ra["b_event_kinds"] == ["B_SHARED_TOOL"]
    assert rb["can_read_B_behavior"] is False
    assert rb["tool_access"] == 1
    assert ra["tool_access"] == 1
    assert ra["memory"] != rb["memory"]


def test_refuse_observed_vs_unobserved_differs():
    world = T.BWorld()
    a = T.ContinuingPerson()
    a.consume(T.TargetlessC10Ledger.build(world.action("REFUSE", observed=True)))
    b = T.ContinuingPerson()
    b.consume(T.TargetlessC10Ledger.build(world.action("REFUSE", observed=False)))
    assert a.read_later()["can_read_B_behavior"] is True
    assert b.read_later()["can_read_B_behavior"] is False
    assert a.read_later()["tool_access"] == 0
    assert b.read_later()["tool_access"] == 0


def test_no_change_requires_competent_receipt():
    world = T.BWorld()
    held = T.TargetlessC10Ledger.build(world.action("NO_CHANGE"))
    evaluated = T.TargetlessC10Ledger.build(
        world.action("NO_CHANGE", evaluation_receipt=eval_receipt())
    )
    assert held.state == "HELD_MISSING_RULE"
    assert evaluated.state == "EVALUATED_NO_CHANGE"
    person = T.ContinuingPerson()
    person.consume(held)
    assert person.read_later()["evaluated_no_change"] is False
    person2 = T.ContinuingPerson()
    person2.consume(evaluated)
    assert person2.read_later()["evaluated_no_change"] is True


def test_negative_sever_b_live_prehistory():
    world = T.BWorld()
    event = next(e for e in world.life.b_ledger.events if e.kind == "RELATION_VIEW")
    event.payload["perceived_state"] = "B_FORCED_DRIFT"
    with pytest.raises(T.ContinuityRefusal, match="LIVE_B_HISTORY_CHANGED"):
        world.action("REFUSE")


def test_negative_forged_shared_and_b_digests():
    world = T.BWorld()
    with pytest.raises(T.ContinuityRefusal, match="SHARED_HISTORY_CHANGED"):
        world.action("SHARE", forged_shared=True)
    with pytest.raises(T.ContinuityRefusal, match="B_HISTORY_CHANGED"):
        world.action("SHARE", forged_b=True)


def test_negative_remove_b_resource_or_time():
    world = T.BWorld()
    with pytest.raises(f1c.Hold, match="B_HAS_NO_TRANSFERABLE_TOOL"):
        world.action("SHARE", no_resource=True)
    with pytest.raises(f1c.Hold, match="B_TOOL_TRANSFER_RIGHT_DENIED"):
        world.action("SHARE", encumbered=True)


def test_negative_refuse_without_performed_event():
    world = T.BWorld()
    action = world.action("REFUSE")
    with pytest.raises(T.ContinuityRefusal, match="REFUSE_REQUIRES_PERFORMER"):
        replace(action, performer=None, performed=False, kind="NON_EVENT_CONDITION",
                a_event_access=False)


def test_negative_no_change_without_receipt_is_held_not_no_change():
    world = T.BWorld()
    held = T.TargetlessC10Ledger.build(world.action("NO_CHANGE"))
    assert held.state == "HELD_MISSING_RULE"
    assert held.state != "EVALUATED_NO_CHANGE"
    with pytest.raises(T.ContinuityRefusal, match="NO_CHANGE_RECEIPT"):
        world.action("NO_CHANGE", evaluation_receipt={"decision_state": "NO_CHANGE"})


def test_negative_unobserved_event_in_a_memory_is_refused():
    world = T.BWorld()
    ledger = T.TargetlessC10Ledger.build(world.action("SHARE", observed=False))
    person = T.ContinuingPerson()
    person.consume(ledger)
    person.memory.append({
        "kind": "B_SHARED_TOOL", "actor": "B", "observed": False,
        "performed": True, "tick": ledger.tick_after, "receipt_hash": "forged",
    })
    with pytest.raises(T.ContinuityRefusal, match="UNOBSERVED_EVENT_IN_MEMORY"):
        person.read_later()


def test_restore_preimages_reproduces_intended_state():
    first = T.TargetlessC10Ledger.build(T.BWorld().action("REFUSE"))
    second = T.TargetlessC10Ledger.build(T.BWorld().action("REFUSE"))
    assert first.receipt["receipt_hash"] == second.receipt["receipt_hash"]
    assert first.action.b_history_digest == second.action.b_history_digest
    assert first.action.shared_history_digest == second.action.shared_history_digest
    assert first.durable_history == second.durable_history


def test_cold_replay_in_two_fresh_processes(tmp_path):
    world = T.BWorld()
    ledger = T.TargetlessC10Ledger.build(world.action("REFUSE"))
    person = T.ContinuingPerson()
    person.consume(ledger)
    payload = {"ledger": ledger.to_dict(), "person": person.to_dict()}
    source = tmp_path / "payload.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    runner = Path(__file__).resolve().parent / "cold_replay_runner.py"
    outputs = []
    for index in (1, 2):
        out = tmp_path / f"replay-{index}.json"
        completed = subprocess.run(
            [sys.executable, str(runner), str(source), str(out)],
            cwd=str(Path(__file__).resolve().parent), text=True,
            capture_output=True, check=True,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(out.read_text(encoding="utf-8")))
    assert outputs[0] == outputs[1]
    assert outputs[0]["ledger_hash"] == ledger.receipt["receipt_hash"]
    assert outputs[0]["state"] == "TARGETLESS_REFUSE"
    assert outputs[0]["read"]["tool_access"] == 0


def test_market_work_ledger_attached_to_targetless_refuse():
    world = T.BWorld()
    market = T.MaterialLedger.consume(
        stock_before=0, replenish=1, consume=1, hours_before=12,
        hours_after=11, tick=250, replenishment_ref="TESTONLY_I1_PRIOR_STOCK",
    )
    ledger = T.TargetlessC10Ledger.build(world.action("REFUSE", market_work=market))
    assert ledger.action.material.stock_after == 0
    assert ledger.action.material.receipt["clamped"] is False
    assert ledger.durable_history[1]["receipt_hash"] == market.receipt["receipt_hash"]
