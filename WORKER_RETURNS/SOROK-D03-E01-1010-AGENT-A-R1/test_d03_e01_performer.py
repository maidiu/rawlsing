"""Agent A #1010: real P2 first-consumer tests, not response-mode tests.

Requires the frozen PR #996 multi-head checkout and its test-only dependencies.
Run from repository root:
  python -B -m pytest -q -p no:cacheprovider \
    WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
WR = HERE.parent
for item in (
    HERE,
    WR / "SOROK-E01-J1-995-R1",
    WR / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1",
    WR / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1" / "tests",
    WR / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1",
    WR / "SOROK-DUEL-B02-R1",
    WR / "SOROK-DUEL-B04-R1",
    WR / "SOROK-DUEL-B05-R1",
    WR / "SOROK-P6-ONE-LIVING-HOUSE-R1",
    WR / "SOROK-P4-FIRST-FULL-MPC-R1",
    WR / "SOROK-S45-S47-PROJECTION-20261105-R1",
    WR / "SOROK-DUEL-D03-R1" / "tests",
):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, digest,
)
from developmental_recursion.engine import BatchEngine  # noqa: E402
from p3_fixture_support import reopen_owner  # noqa: E402
from test_j1_three_head_join import open_j1_case  # noqa: E402
import d03_e01_performer as a  # noqa: E402
import run_p6  # noqa: E402
import j1_join  # noqa: E402


class ExactActorProvider:
    """Explicit sourcefree provider; no psychological chooser is implied.

    Its proposals are fully specified before it sees the actor context. This
    proves the writer and context transport, NOT context-dependent motive.
    The adversary should replace this with a tested context-sensitive yet
    actor/owner-qualified proposer before claiming autonomous history.
    """

    def __init__(self, base, *, events=3, expect_hash=None, actor=None):
        self.before = base.snapshot()
        self.base = base
        self.events = events
        self.expect_hash = expect_hash
        self.actor = actor
        self.calls = []
        self.proposals = []
        for index in range(events):
            self.proposals.append(EventProposal(
                event_id=f"nadia:e01:subsequent:{index}",
                event_time=self.before.clock + 20 * (index + 1),
                operation="ADMIT_EVENT",
                source_refs=(base.source_ref,),
                participants=tuple(base.participants),
                circumstances={},
                interval=None,
            ))

    def call(self, request):
        self.calls.append(copy.deepcopy(request))
        assert request["mode"] == "BOOTSTRAP"
        assert request["previous"] is None
        context = request["context"]
        assert context["schema"] == a.CONTEXT_SCHEMA
        assert context["actor"]["actor_id"] == self.before.actor
        assert context["actor"]["root"] == self.before.root
        assert context["actor"]["branch"] == self.before.branch
        assert context["actor"]["p2_state_hash"] == self.before.state_hash
        assert context["hash"] == digest(
            {k: v for k, v in context.items() if k != "hash"})
        assert context["boundaries"]["parent_private_reason"] == "NOT_READ"
        assert context["boundaries"]["durable_formation"] == "MISSING_RULE"
        if self.expect_hash:
            assert context["actual_access"]["event_hash"] == self.expect_hash
        if self.actor:
            assert context["actor"]["actor_id"] == self.actor
        return {
            "retrospective": None,
            "prospective": [item.document() for item in self.proposals],
        }


def _invoke(opened, provider, *, base_path=None, **overrides):
    target = Path(base_path or opened["path"])
    arguments = {
        "child_id": opened["focal"],
        "speech_event_id": opened["receipt"]["event_id"],
        "utterance_receipt": opened["receipt"],
        "plan": opened["plan"],
        "provider": provider,
        "journal_path": target / "e01_p2_journal.sqlite",
        "cycle_path": target / "e01_recursion_cycle.json",
    }
    arguments.update(overrides)
    return a.run_d03_e01_first_batch(
        opened["case"].owner, opened["session"], **arguments)


def _close(opened):
    opened["case"].owner.close()


def test_event_is_real_world_history_and_cold_first_consumer(tmp_path):
    opened = open_j1_case(tmp_path / "performed")
    base = opened["case"].owner.base_owner
    session = opened["session"]
    provider = ExactActorProvider(
        base, expect_hash=opened["receipt"]["event_hash"])
    pre_head = copy.deepcopy(opened["case"].owner.store.head())
    prior = session.read_events()
    try:
        report = _invoke(opened, provider)
        assert report["schema"] == a.SCHEMA
        assert report["grade"] == "SOURCEFREE_P2_EVENT_ONLY"
        assert report["status"] in {
            "SOURCEFREE_P2_EVENT_ACTOR_OBSERVED",
            "SOURCEFREE_P2_EVENT_ACTOR_ACCESS_PARTIAL",
        }
        assert len(provider.calls) == 1
        assert report["world_events_written"] == 3
        assert len(report["world_readbacks"]) == 3
        assert report["motive_selection"] == "NOT_ASSERTED"
        assert report["psychological_causation_by_d03"] == "NOT_ESTABLISHED"
        assert report["durable_formation"] == "MISSING_RULE"
        assert opened["case"].owner.store.head() == pre_head
        assert len(session.read_events()) >= len(prior) + 3
        for item in report["world_readbacks"]:
            real = session.read_event(item["admitted_e1_event_id"])
            assert real["e1_event_hash"] == item["admitted_e1_event_hash"]
            assert real["performed"] is True
            # Independent ordinary C9 consumer, not adapter echo:
            downstream = session.read_c9_conditioning(item["admitted_e1_event_id"])
            assert downstream is not None
        # P6 ordinary child reader still sees only the original public speech.
        perceived = run_p6.child_speech_experience(
            session, event_id=opened["receipt"]["event_id"])
        assert perceived["status"] == "PERCEIVED"
        assert "private-motive" not in json.dumps(perceived)
        ids = [item["admitted_e1_event_id"] for item in report["world_readbacks"]]
        raw = [session.read_event(item) for item in ids]
        count_before_retry = len(session.read_events())
        with pytest.raises(RecursionRefusal, match="bootstrap is exactly-once"):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert len(session.read_events()) == count_before_retry
        batch_id, history_hash = report["batch_id"], report["history_hash"]
    finally:
        _close(opened)

    base2, owner2 = reopen_owner(opened["case"])
    try:
        session2 = base2.fanin.session
        assert owner2.store.head() == pre_head
        assert [session2.read_event(item) for item in ids] == raw
        with BatchEngine(base2, opened["path"] / "e01_p2_journal.sqlite") as engine:
            history = engine.history(batch_id)
        assert history["history_hash"] == history_hash
        assert len(history["records"]) == 3
        assert len(session2.read_events()) == count_before_retry
    finally:
        owner2.close()


def test_absence_does_not_recruit_or_write_any_event(tmp_path):
    opened = open_j1_case(tmp_path / "absent", child_present=False)
    provider = ExactActorProvider(opened["case"].owner.base_owner)
    before_events = list(opened["session"].read_events())
    before_p3 = copy.deepcopy(opened["case"].owner.store.head())
    try:
        result = _invoke(opened, provider)
        assert result["status"] == a.HELDED
        assert result["world_events_written"] == 0
        assert result["provider_called"] is False
        assert provider.calls == []
        assert opened["session"].read_events() == before_events
        assert opened["case"].owner.store.head() == before_p3
        assert not (opened["path"] / "e01_recursion_cycle.json").exists()
    finally:
        _close(opened)


def test_forged_speech_refuses_before_provider_or_world_write(tmp_path):
    opened = open_j1_case(tmp_path / "forged")
    provider = ExactActorProvider(opened["case"].owner.base_owner)
    before = list(opened["session"].read_events())
    forged = copy.deepcopy(opened["receipt"])
    forged["text"] = "Altered public words after admission"
    try:
        with pytest.raises(RecursionRefusal):
            _invoke(opened, provider, utterance_receipt=forged)
        assert provider.calls == []
        assert opened["session"].read_events() == before
    finally:
        _close(opened)


def test_wrong_source_closure_and_wrong_child_fail_closed(tmp_path):
    opened = open_j1_case(tmp_path / "closure")
    provider = ExactActorProvider(opened["case"].owner.base_owner)
    before = list(opened["session"].read_events())
    try:
        with pytest.raises(RecursionRefusal, match="J1_SOURCE_CLOSURE_CHANGED"):
            _invoke(opened, provider, expected_source_closure={"hash": "0" * 64})
        with pytest.raises(RecursionRefusal, match="E01_CHILD_OR_CLOCK_MISMATCH"):
            _invoke(opened, provider, child_id="IMPOSTER")
        assert provider.calls == []
        assert opened["session"].read_events() == before
    finally:
        _close(opened)


def test_invalid_two_event_prospective_cannot_claim_performance(tmp_path):
    opened = open_j1_case(tmp_path / "two")
    provider = ExactActorProvider(opened["case"].owner.base_owner, events=2)
    before = list(opened["session"].read_events())
    try:
        with pytest.raises(RecursionRefusal):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == before
        assert (opened["path"] / "e01_recursion_cycle.json").exists()
    finally:
        _close(opened)


def test_same_public_speech_different_history_yields_distinct_context(tmp_path):
    a_case = open_j1_case(tmp_path / "history_a", outcome="recognized_plan")
    b_case = open_j1_case(tmp_path / "history_b", outcome="imposed_plan")
    try:
        assert a_case["receipt"]["text"] == b_case["receipt"]["text"]
        # No requirement that two histories necessarily select different acts.
        # The proved distinction is sourcefree P3 organization, not motive law.
        first = j1_join.compose_j1(
            a_case["case"].owner, a_case["session"],
            child_id=a_case["focal"], speech_event_id=a_case["receipt"]["event_id"],
            utterance_receipt=a_case["receipt"], plan=a_case["plan"])
        second = j1_join.compose_j1(
            b_case["case"].owner, b_case["session"],
            child_id=b_case["focal"], speech_event_id=b_case["receipt"]["event_id"],
            utterance_receipt=b_case["receipt"], plan=b_case["plan"])
        ac = a._context(first, a._identity(
            a_case["case"].owner, a_case["case"].owner.base_owner,
            a_case["session"], a_case["focal"]))
        bc = a._context(second, a._identity(
            b_case["case"].owner, b_case["case"].owner.base_owner,
            b_case["session"], b_case["focal"]))
        assert ac["actual_access"]["public_text"] == bc["actual_access"]["public_text"]
        assert (ac["plural_prior_organization"] !=
                bc["plural_prior_organization"])
        assert ac["hash"] != bc["hash"]
        assert "private-motive" not in json.dumps(ac)
        assert "private-motive" not in json.dumps(bc)
    finally:
        _close(a_case)
        _close(b_case)
