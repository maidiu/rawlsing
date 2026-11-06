from dataclasses import replace
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from developmental_recursion.contracts import EventProposal, RecursionRefusal
from developmental_recursion.p2_owner import P2Owner, load_p2


def start(root):
    fanin = load_p2().start(root)
    case = fanin.deps["case_for"](True)
    return P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
                   participants=tuple(fanin.session.read_root()["actor_ids"]))


def event(owner, mode="ACTUAL"):
    return EventProposal("later", owner.snapshot().clock + 6, "ADMIT_EVENT",
                         (owner.source_ref,), owner.participants, {},
                         {"mode": mode, "span": 4})


def test_actual_material_effect_reaches_c9_and_owner_receipt_survives_reopen(tmp_path):
    owner = start(tmp_path / "actual")
    proposal = event(owner)
    before = owner.snapshot()
    result = owner.realize("op-1", proposal, before)
    assert result.after.clock == proposal.event_time
    assert result.after.state_hash != before.state_hash
    assert result.consequences["material_state_changed"] is True
    assert result.consequences["immediate_response"]["objective_material_eligible"] is False
    assert result.consequences["durable_psychological_transition"] == "MISSING_RULE"
    assert result.accessible["user_attempt"] is False
    assert result.objective["event"]["e1_event_hash"] in result.readset
    case, source, participants = owner.case, owner.source, owner.participants
    owner.close()
    reopened = P2Owner(load_p2().open(tmp_path / "actual"), case=case,
                       source=source, participants=participants)
    try:
        assert reopened.snapshot() == result.after
        assert reopened.realize("op-1", proposal, before) == result
        with pytest.raises(RecursionRefusal, match="REUSE_MISMATCH"):
            reopened.realize("op-1", replace(proposal, event_id="forged"), before)
    finally:
        reopened.close()


def test_scheduled_interval_does_not_fabricate_material_participation(tmp_path):
    owner = start(tmp_path / "scheduled")
    try:
        before = owner.snapshot()
        result = owner.realize("op-1", event(owner, "SCHEDULED_ONLY"), before)
        assert result.consequences["immediate_response"]["objective_material_eligible"] is True
        assert result.consequences["interval"]["status"] == "NOT_PERFORMED"
        assert result.consequences["durable_psychological_transition"] == "MISSING_RULE"
    finally:
        owner.close()


def test_wrong_source_clock_state_and_unknown_operation_do_not_mutate_owner(tmp_path):
    owner = start(tmp_path / "negative")
    try:
        before = owner.snapshot()
        proposal = event(owner)
        for changed in [replace(proposal, source_refs=("ABSENT",)),
                        replace(proposal, operation="ACQUIRE_PRACTICE"),
                        replace(proposal, event_time=before.clock),
                        replace(proposal, participants=("invented-B",))]:
            with pytest.raises(RecursionRefusal):
                owner.realize("op-negative", changed, before)
            assert owner.snapshot() == before
        for changed in [replace(before, root="wrong-root"),
                        replace(before, branch="wrong-branch"),
                        replace(before, clock=before.clock + 1)]:
            with pytest.raises(RecursionRefusal, match="STALE"):
                owner.realize("op-negative", proposal, changed)
            assert owner.snapshot() == before
        # A durable reservation without an owner result is genuinely ambiguous.
        from developmental_recursion.contracts import canonical, digest
        owner.db.execute("INSERT INTO operations VALUES (?,?,?,NULL)",
                         ("interrupted", digest(proposal.document()),
                          canonical(before.document())))
        owner.db.commit()
        with pytest.raises(RecursionRefusal, match="AMBIGUOUS"):
            owner.realize("interrupted", proposal, before)
        assert owner.snapshot() == before
        original = owner.source.copy()
        owner.source["unissued_source_mutation"] = True
        with pytest.raises(RecursionRefusal, match="SOURCE_MUTATED"):
            owner.realize("severed", proposal, before)
        owner.source.clear()
        owner.source.update(original)
        assert owner.snapshot() == before
    finally:
        owner.close()
