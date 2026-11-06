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
    assert result.accessible["status"] == "OBSERVED"
    assert result.accessible["actor_ref"] == owner.actor
    assert result.accessible["events"]
    assert all("perceived_by_user" not in row for row in result.accessible["events"])
    # A user's receipt must not stand in for the developing actor's receipt.
    from unittest.mock import patch
    store = owner.fanin.session.product.store
    original_perceptions = store.perceptions
    alias = result.accessible["actor_alias"]
    assert original_perceptions(owner.fanin.session.branch_id,
                                actor_id=owner.fanin.session.meta["user_actor"])
    with patch.object(store, "perceptions", side_effect=lambda branch, actor_id=None:
                      [] if actor_id == alias else original_perceptions(branch, actor_id)):
        held = owner.actor_experience(result.objective["event"], after_clock=before.clock)
        assert held["status"] == "HELD"
        assert held["reason"] == "P2_ACTOR_PERCEPTION_UNAVAILABLE"
        assert held["events"] == []
    assert owner.actor_experience(result.objective["event"], after_clock=before.clock) == result.accessible
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


def test_bad_history_in_later_proposal_is_refused_before_first_interval(tmp_path):
    from developmental_recursion.engine import BatchEngine
    owner = start(tmp_path / "grounding")
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    try:
        before = owner.snapshot()
        native = owner.fanin.session.read_events()[0]
        first = event(owner)
        second = replace(first, event_id="second", event_time=before.clock + 12, interval=None)
        third = replace(first, event_id="third", event_time=before.clock + 18, interval=None)
        for times in ((18, 6, 24), (6, 6, 18)):
            with pytest.raises(RecursionRefusal):
                engine.run_batch("bad-native-times", [
                    replace(p, event_time=before.clock + t)
                    for p, t in zip((first, second, third), times)])
            assert owner.snapshot() == before
            assert owner.fanin.session.read_interval_states() == []
            assert owner.db.execute("SELECT COUNT(*) FROM operations").fetchone()[0] == 0
        for bad in (["does-not-exist"], "not-a-ref-list", [None],
                    [native["e1_event_id"], native["e1_event_id"]],
                    [native["e1_event_hash"], native["e1_event_id"]]):
            with pytest.raises(RecursionRefusal):
                engine.run_batch("bad-grounding", [first, second,
                    replace(third, circumstances={"history_refs": bad})])
            assert owner.snapshot() == before
            assert owner.fanin.session.read_interval_states() == []
            assert owner.db.execute("SELECT COUNT(*) FROM operations").fetchone()[0] == 0
        # The owner's existing ID and hash reference forms remain legitimate.
        for ref in (native["e1_event_id"], native["e1_event_hash"]):
            owner.validate_proposal(replace(first, circumstances={"history_refs": [ref]}))
        assert owner.snapshot() == before
        assert engine.verify()
    finally:
        engine.close()
        owner.close()


def test_invalid_language_context_is_refused_before_actual_interval(tmp_path):
    from developmental_recursion.engine import BatchEngine
    owner = start(tmp_path / "context")
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    try:
        before = owner.snapshot()
        first = event(owner)
        later = [replace(first, event_id=str(i), event_time=before.clock + 6*i,
                         interval=None) for i in (2, 3)]
        for context in ("invalid-context", [], {}, {"milieu_id": []},
                        {"milieu_id": ""}, {"milieu_id": "MISSING_NATIVE_CONTEXT"}):
            with pytest.raises(RecursionRefusal):
                engine.run_batch("bad-context", [
                    replace(first, circumstances={"language_context": context}), *later])
            assert owner.snapshot() == before
            assert owner.fanin.session.read_interval_states() == []
            assert owner.db.execute("SELECT COUNT(*) FROM operations").fetchone()[0] == 0
        # The explicit context is supplied by the existing native session,
        # rather than a new wrapper-owned context vocabulary.
        native_context = owner.fanin.session.s43_context()
        for context in (None, native_context):
            owner.validate_proposal(replace(first, circumstances={
                "language_context": context}))
        assert owner.snapshot() == before
        result = owner.realize("valid-context", replace(first, circumstances={
            "language_context": native_context}), before)
        assert result.status == "REALIZED"
        assert result.after.clock == first.event_time
        assert result.accessible["status"] == "OBSERVED"
        assert result.consequences["immediate_response"]["objective_material_eligible"] is False
        assert engine.verify()
    finally:
        engine.close()
        owner.close()
