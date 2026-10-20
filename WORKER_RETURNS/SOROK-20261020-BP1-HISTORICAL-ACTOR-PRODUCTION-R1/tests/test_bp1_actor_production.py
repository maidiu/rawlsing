"""BP1 historical actor production and C4→C9 consumed-life court.

Author tests. They exercise the sourcefree historical actor composer, the
per-actor append-only ledgers, independent performed actions, NO_CHANGE/DENY,
future firewall, and the exact C9R sourcefree ingress→target→later E2 consumer.
No native actor, rule, person or parent is claimed.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for _path in (
    ROOT / "candidate",
    ROOT / "vendor/g18/candidate",
    ROOT / "vendor/c9r",
    ROOT / "vendor/c9r/runtime/native",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from bp1 import (  # noqa: E402
    ActorLedger,
    BP1_ACTOR_SOURCE_GRADE,
    BP1_NATIVE_GRANT,
    BP1C9Result,
    LedgerRefusal,
    SourceRefusal,
    TwoActorLife,
    build_c9_actor_record,
    build_denied_life,
    build_no_change_life,
    build_two_actor_life,
    future_child_findings,
    issue_actor_source,
    make_objective_event,
    reseal_with_changed_source_ref,
    run_bp1_c9,
    verify_actor_source,
    verify_snapshot,
)
from bp1.composer import assert_no_future_child  # noqa: E402
from bp1.c9_bridge import _consumed_state  # noqa: E402
from bp1.c9_bridge import (  # noqa: E402
    ACTUATOR,
    EXPECTED_ACT,
    OCCURRENCE,
    build_c9_conditioning,
    build_c9_event,
)
from bp1.c9_bridge import BP1C9Refusal  # noqa: E402
from candidate import (  # noqa: E402
    CandidateStore,
    LaterActionConsumer,
    LaterActionStatus,
    admit_performed_action,
    ingress_actor,
    make_performed_action_receipt,
    read_target_for_later_action,
)
from lab_sgi1.core import h_obj  # noqa: E402
from lab_sgi1.joint import material_joint_opportunity, observe_joint_actions  # noqa: E402


def _forged_material(material: dict) -> dict:
    forged = deepcopy(material)
    forged["payment_per_actor"] = 100000
    forged["event_id"] = h_obj({k: v for k, v in forged.items()
                                if k != "event_id"})
    return forged


def _fresh_ledger_with_objective(life: TwoActorLife, actor: str = "A"):
    if actor == "A":
        source = life.a_source
        history = life.a_events
    else:
        source = life.b_source
        history = life.b_events
    ledger = ActorLedger(source, prior_history_events=history)
    ledger.append_shared_objective(
        life.objective, parents=(ledger.prior_history_event_id,))
    return ledger


def _action_for(life: TwoActorLife, actor: str) -> dict:
    owner = life.a_source.actor_id if actor == "A" else life.b_source.actor_id
    return next(x for x in life.witness["actions"] if x["owner_id"] == owner)


def test_two_actor_sourcefree_lives_are_distinct_not_one_seeded_adult():
    life = build_two_actor_life()
    assert life.a_source.actor_id != life.b_source.actor_id
    assert life.a_source.source_ref != life.b_source.source_ref
    assert life.a_source.source_grade == BP1_ACTOR_SOURCE_GRADE
    assert life.a_source.native_grant == BP1_NATIVE_GRANT
    assert life.b_source.native_grant == BP1_NATIVE_GRANT
    assert life.a_replay["history_hash"] != life.b_replay["history_hash"]
    assert ({e["event_id"] for e in life.a_events}.isdisjoint(
        {e["event_id"] for e in life.b_events}))
    a = life.a_snapshot
    b = life.b_snapshot
    assert a["state"]["role"] == "repair"
    assert b["state"]["role"] == "finishing"
    assert a["state"]["cash"] == 55
    assert b["state"]["cash"] == 54
    assert a["state"]["completed_units"] == 4
    assert b["state"]["completed_units"] == 3
    assert a["state"]["material_remaining"] == 2
    assert b["state"]["material_remaining"] == 0
    assert a["state"]["free_hours"] == 12
    assert b["state"]["free_hours"] == 13
    assert a["hash"] != b["hash"]
    assert life.witness["status"] == "WITNESSED"
    assert life.objective["objective_event_id"] == (
        life.a_ledger.objective_events[0].payload["objective_event_id"])
    assert life.objective["objective_event_id"] == (
        life.b_ledger.objective_events[0].payload["objective_event_id"])
    assert life.objective["objective_hash"] == (
        life.b_ledger.objective_events[0].payload["objective_hash"])
    a_action = _action_for(life, "A")
    b_action = _action_for(life, "B")
    assert a_action["owner_id"] != b_action["owner_id"]
    assert a_action["event_id"] != b_action["event_id"]
    assert a_action["before"]["completed_units"] == 3
    assert a_action["after"]["completed_units"] == 4
    assert b_action["before"]["completed_units"] == 2
    assert b_action["after"]["completed_units"] == 3
    assert [e.kind for e in life.a_ledger.events] == [
        "PRIOR_HISTORY", "SHARED_OBJECTIVE", "PERFORMED_ACTION",
        "OTHER_ACTION", "RELATION_VIEW"]
    assert [e.kind for e in life.b_ledger.events] == [
        "PRIOR_HISTORY", "SHARED_OBJECTIVE", "PERFORMED_ACTION",
        "OTHER_ACTION", "RELATION_VIEW"]
    assert life.receipt()["claim"].startswith("TWO_SOURCEFREE_HISTORICAL")
    assert life.receipt()["native_actor_claim"] is False
    assert life.receipt()["psychology_claim"] is False


def test_shared_objective_event_does_not_change_actor_state():
    life = build_two_actor_life()
    ledger = ActorLedger(life.a_source, prior_history_events=life.a_events)
    before = ledger.state
    ledger.append_shared_objective(
        life.objective, parents=(ledger.prior_history_event_id,))
    assert ledger.state == before
    assert ledger.events[-1].kind == "SHARED_OBJECTIVE"
    assert ledger.events[-1].payload["objective_hash"] == (
        life.objective["objective_hash"])


def test_actor_own_action_changes_only_own_state():
    life = build_two_actor_life()
    a_before = life.a_ledger.events[1]
    assert a_before.kind == "SHARED_OBJECTIVE"
    a_action_event = life.a_ledger.performed_action_events[0]
    b_action_event = life.b_ledger.performed_action_events[0]
    assert a_action_event.payload["g18_action"]["owner_id"] == life.a_source.actor_id
    assert b_action_event.payload["g18_action"]["owner_id"] == life.b_source.actor_id
    assert a_action_event.payload["delta"]["completed_units"] == 1
    assert b_action_event.payload["delta"]["completed_units"] == 1
    assert life.a_ledger.events[3].payload["other_actor_id"] == life.b_source.actor_id
    assert life.b_ledger.events[3].payload["other_actor_id"] == life.a_source.actor_id
    assert life.a_ledger.events[4].payload["perceived_state"] == (
        "UNKNOWN_OR_NONRECIPROCAL")
    assert life.b_ledger.events[4].payload["perceived_state"] == (
        "UNKNOWN_OR_NONRECIPROCAL")
    assert life.a_ledger.verify()[0] is True
    assert life.b_ledger.verify()[0] is True


def test_no_change_exhausted_actor_is_lawful():
    no_change = build_no_change_life()
    assert no_change["state_unchanged"] is True
    assert no_change["state_before"] == no_change["state_after"]
    assert "NO_CHANGE" in no_change["ledger_event_kinds"]
    assert "PERFORMED_ACTION" not in no_change["ledger_event_kinds"]
    assert no_change["refusal"] == "OWN_MATERIAL_EXHAUSTED"
    assert no_change["snapshot"]["native_grant"] == BP1_NATIVE_GRANT
    assert no_change["snapshot"]["state"]["material_remaining"] == 0


def test_denied_actor_is_lawful():
    denied = build_denied_life()
    assert denied["state_unchanged"] is True
    assert denied["state_before"] == denied["state_after"]
    assert "DENY" in denied["ledger_event_kinds"]
    assert "PERFORMED_ACTION" not in denied["ledger_event_kinds"]
    assert denied["refusal"].startswith("ACTOR_PERMISSION_DENIED")
    assert denied["snapshot"]["native_grant"] == BP1_NATIVE_GRANT


def test_future_child_payload_refused():
    payload = {"metadata": {"future_child_personality": "NESTED_ALIAS"}}
    findings = future_child_findings(payload)
    assert findings
    assert findings[0]["reason"] == "PROHIBITED_KEY"
    with pytest.raises(LedgerRefusal, match="FUTURE_CHILD_INFORMATION_LEAK"):
        assert_no_future_child(payload)
    serialized = {"note": '{"future_child_education_outcome":"X"}'}
    assert future_child_findings(serialized)


def test_forged_actor_source_refused():
    source = issue_actor_source(
        actor_id="TEST_ONLY_BP1_ACTOR_FORGED", role="repair",
        seed="BP1_SEED_FORGED")
    forged = reseal_with_changed_source_ref(source, "NATIVE_ADMIN_ACTOR")
    accepted, reason = verify_actor_source(forged)
    assert accepted is False
    assert reason == "ACTOR_SOURCE_REF_NOT_TEST_ONLY_BP1"
    with pytest.raises(SourceRefusal, match="ACTOR_SOURCE_REF_NOT_TEST_ONLY_BP1"):
        from bp1.source import require_actor_source
        require_actor_source(forged)


def test_forged_material_source_refused():
    life = build_two_actor_life()
    ledger = _fresh_ledger_with_objective(life, "A")
    action = _action_for(life, "A")
    forged = _forged_material(life.material)
    with pytest.raises(LedgerRefusal, match="MATERIAL_SOURCE_NOT_AUTHENTICATED"):
        ledger.append_performed_action(
            action, forged, life.objective["objective_event_id"],
            parents=(ledger.events[-1].event_id,))


def test_fake_afterstate_action_refused():
    life = build_two_actor_life()
    ledger = _fresh_ledger_with_objective(life, "A")
    action = deepcopy(_action_for(life, "A"))
    action["after"]["cash"] += 100000
    action["event_id"] = h_obj({k: v for k, v in action.items()
                                if k != "event_id"})
    with pytest.raises(LedgerRefusal,
                       match="PERFORMED_ACTION_NOT_AUTHENTICATED"):
        ledger.append_performed_action(
            action, life.material, life.objective["objective_event_id"],
            parents=(ledger.events[-1].event_id,))


def test_c9_actor_ingress_is_explicitly_test_only():
    life = build_two_actor_life()
    record = build_c9_actor_record(life)
    ingress = ingress_actor(record, as_of=int(life.a_snapshot["last_clock"]) + 1)
    assert ingress.admitted is True
    assert ingress.source_grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    assert ingress.native_source_resolved is False
    assert ingress.actor_id == life.a_source.actor_id
    assert record["source_ref"].startswith("TEST_ONLY_BP1_")
    assert life.a_snapshot["native_grant"] == BP1_NATIVE_GRANT


def test_c9_end_to_end_positive_and_exact_consumed_state(tmp_path):
    life = build_two_actor_life()
    with CandidateStore(tmp_path / "bp1.sqlite") as store:
        result = run_bp1_c9(life, store)
        assert result.committed is True
        assert result.pipeline.receipt.committed is True
        assert result.target_id
        assert result.state_hash
        committed = store.read_target_state(result.target_id)
        assert committed is not None
        assert committed["record_hash"] == result.pipeline.decision.record_hash
        assert result.pipeline.later_read.state_hash == result.state_hash
        assert result.pipeline.later_read.committed_record == committed
        assert result.e2 is not None and result.e2.admitted is True
        assert result.e2.actuator_ref == ACTUATOR
        assert result.e2.occurrence_ref == OCCURRENCE
        assert result.e2.consumed_state_hash == result.state_hash
        receipt = result.receipt()
        assert receipt["e2_admitted"] is True
        assert receipt["e2_reason"] == "AdmissionReason.OK"
        assert receipt["native_actor_claim"] is False
        assert receipt["native_rule_claim"] is False
        assert receipt["native_e2_claim"] is False
        assert receipt["actor_source_grade"] == BP1_ACTOR_SOURCE_GRADE
        assert receipt["native_grant"] == BP1_NATIVE_GRANT
        assert receipt["material_event_ref"] == life.material["event_id"]
        assert receipt["other_offer_ref"] == (
            life.b_ledger.performed_action_events[0].event_id)
        assert set(receipt["enacted_history_refs"]) >= {
            life.a_ledger.prior_history_event_id,
            life.a_ledger.performed_action_events[0].event_id}
        assert result.event["content"]["material_event_ref"] == (
            life.material["event_id"])
        assert result.event["content"]["objective_hash"] == (
            life.objective["objective_hash"])


def test_c9_consumed_state_fault_is_held(tmp_path):
    life = build_two_actor_life()
    with CandidateStore(tmp_path / "bp1.sqlite") as store:
        result = run_bp1_c9(life, store)
        wrong = make_performed_action_receipt(
            actor_id=life.a_source.actor_id,
            act=EXPECTED_ACT,
            actuator_ref=ACTUATOR,
            occurrence_ref=OCCURRENCE,
            action_time=int(result.pipeline.later_read.as_of) + 1,
            consumed_state_hash="sha256:" + "00" * 32,
            target_commit_time=int(result.commit_time),
        )
        held = admit_performed_action(
            owner_receipt=wrong,
            expected_actor_id=life.a_source.actor_id,
            expected_act=EXPECTED_ACT,
            consumed_state_hash=result.state_hash,
            as_of=int(result.pipeline.later_read.as_of) + 2,
            target_commit_time=int(result.commit_time),
        )
        assert getattr(held, "admitted", False) is False
        assert "CONSUMED_STATE_MISMATCH" in str(held.reason)


def test_c9_source_fault_snapshot_is_refused():
    life = build_two_actor_life()
    forged_snapshot = deepcopy(life.a_snapshot)
    forged_snapshot["state"]["cash"] += 100000
    from bp1.canon import digest, seal
    forged_snapshot["state_hash"] = digest(forged_snapshot["state"])
    forged_snapshot = seal({k: v for k, v in forged_snapshot.items()
                            if k != "hash"})
    with pytest.raises(BP1C9Refusal,
                       match="ACTOR_SNAPSHOT_NOT_AUTHENTICATED"):
        build_c9_actor_record(life, snapshot=forged_snapshot)


def test_c9_cold_reopen_reads_exact_committed_record(tmp_path):
    life = build_two_actor_life()
    with CandidateStore(tmp_path / "bp1.sqlite") as store:
        result = run_bp1_c9(life, store)
        record = store.read_target_state(result.target_id)
        state_hash = result.state_hash
    with CandidateStore(tmp_path / "bp1.sqlite") as reopened:
        cold = read_target_for_later_action(
            reopened,
            consumer=LaterActionConsumer("TEST_ONLY_BP1_E2_READER",
                                         "committed_target_state"),
            middle_state_id=result.target_id,
            as_of=int(result.pipeline.later_read.as_of),
            commit_time=int(result.commit_time),
            expected_actor_id=life.a_source.actor_id,
        )
        assert cold.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert cold.committed_record == record
        assert cold.state_hash == state_hash


def test_c9_fixed_default_consumed_state_would_break_positive(tmp_path):
    life = build_two_actor_life()
    with CandidateStore(tmp_path / "bp1.sqlite") as store:
        result = run_bp1_c9(life, store)
        assert result.e2.admitted is True
        fixed = "sha256:" + "11" * 32
        receipt = make_performed_action_receipt(
            actor_id=life.a_source.actor_id,
            act=EXPECTED_ACT,
            actuator_ref=ACTUATOR,
            occurrence_ref=OCCURRENCE,
            action_time=int(result.pipeline.later_read.as_of) + 1,
            consumed_state_hash=fixed,
            target_commit_time=int(result.commit_time),
        )
        held = admit_performed_action(
            owner_receipt=receipt,
            expected_actor_id=life.a_source.actor_id,
            expected_act=EXPECTED_ACT,
            consumed_state_hash=result.state_hash,
            as_of=int(result.pipeline.later_read.as_of) + 2,
            target_commit_time=int(result.commit_time),
        )
        assert getattr(held, "admitted", False) is False
        assert _consumed_state(result.pipeline) == result.state_hash
