"""Independent sourcefree P3 -> actual P6 first-reader behavioral counterfactual.

No native CAN/ADP issue, no mother performed action, no home-period writer.
The real P3 owner supplies the historical mediator and the real P6 situated
decision commits (or does not commit) an actor's sourcefree speech event.
"""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

REPO = Path(__file__).resolve().parents[2]
P6 = REPO / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from sourcefree_p3_bridge import qualified_p3_read  # noqa: E402


def _run(state, command, *, interpret=None, realize=None, bridge=False, **kwargs):
    args = Namespace(command=command, request_id=kwargs.pop("request_id", None), **kwargs)
    return run_p6.experience(state, args, interpret=interpret, realize=realize,
                             sourcefree_p3_bridge=bridge)


def _no_mediator_new(monkeypatch, state):
    """Use the same actual P2/P3/P6 constructors with zero sourcefree history."""
    original_new = run_p6.new

    def no_history_new(root, ledger_path, history, *, seed, establish):
        return original_new(root, ledger_path, "", seed=seed, establish=establish)

    with monkeypatch.context() as patch:
        patch.setattr(run_p6, "new", no_history_new)
        _run(state, "new")


def _actual_state(state):
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        ledger = json.loads((state / "p4_receipts.json").read_text())
        scope = ledger["scope"]
        session = owner.base_owner.fanin.session
        packet = qualified_p3_read(
            owner, session, project=scope["project"], counterpart=scope["counterpart"],
            as_of=session.world().clock,
        )
        speeches = [
            event for event in session.events()
            if event["kind"] == "SPEECH" and event["actor_id"] == "A"
        ]
        return packet, speeches, owner.store.head()
    finally:
        owner.close()


def test_real_p6_first_consumer_positive_no_mediator_and_sourcefree_speech(tmp_path, monkeypatch):
    positive = tmp_path / "actual-history"
    negative = tmp_path / "no-history"
    _run(positive, "new")
    _no_mediator_new(monkeypatch, negative)

    before_pos, before_speech_pos, before_head_pos = _actual_state(positive)
    before_neg, before_speech_neg, before_head_neg = _actual_state(negative)
    assert len(before_pos["records"]) == 1, before_pos
    assert before_neg["records"] == []
    assert before_pos["native_memory"] == "MISSING_RULE"
    assert len(before_speech_pos) == len(before_speech_neg)
    assert [(e["clock"], e["body"].get("text")) for e in before_speech_pos] == [(e["clock"], e["body"].get("text")) for e in before_speech_neg]
    assert before_head_pos["count"] == 1
    assert before_head_neg["count"] == 0

    packets = []
    utterance = "We could inspect the plan together."

    def interpret(packet):
        packets.append(packet)
        bridge = packet["sourcefree_p3"]
        assert bridge["grade"] == "SOURCEFREE_TEST_ONLY"
        assert bridge["native_memory"] == "MISSING_RULE"
        assert bridge["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        assert "kitchen" not in json.dumps(bridge)
        assert "mother-invitation" not in json.dumps(bridge)
        return {
            "attention": "uncertain",
            "interpretation": "Test-only historical candidate present or absent.",
            "action": "speak" if bridge["records"] else "continue",
            "cue_event_id": None,
            "channel": None,
        }

    def realize(packet, decision):
        assert decision["action"] == "speak"
        assert packet["sourcefree_p3"]["records"]
        return utterance

    # Both runs use exactly the same actual P6 reader and injected decision;
    # only the sourcefree historical formation is absent in the negative.
    _run(positive, "wait", duration=4, request_id="one", bridge=True,
         interpret=interpret, realize=realize)
    _run(negative, "wait", duration=4, request_id="one", bridge=True,
         interpret=interpret, realize=realize)

    assert len(packets) == 2
    assert len(packets[0]["sourcefree_p3"]["records"]) == 1
    assert packets[1]["sourcefree_p3"]["records"] == []
    after_pos, speech_pos, head_pos = _actual_state(positive)
    after_neg, speech_neg, head_neg = _actual_state(negative)
    assert head_pos == before_head_pos and head_neg == before_head_neg
    assert len(speech_pos) == len(before_speech_pos) + 1
    assert speech_pos[-1]["body"]["text"] == utterance
    assert speech_neg == before_speech_neg
    assert len(after_pos["records"]) == 1 and after_neg["records"] == []

    actual = json.loads((positive / "p4_receipts.json").read_text())["turns"][-1]
    control = json.loads((negative / "p4_receipts.json").read_text())["turns"][-1]
    assert actual["receipt"]["situated"]["decision"]["action"] == "speak"
    assert actual["receipt"]["situated"]["speech"]["admitted"]
    assert control["receipt"]["situated"]["decision"]["action"] == "continue"
    assert "speech" not in control["receipt"]["situated"]


def test_p3_to_p6_source_registry_and_clock_sever_then_restore(tmp_path, monkeypatch):
    state = tmp_path / "bound"
    _run(state, "new")
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        scope = json.loads((state / "p4_receipts.json").read_text())["scope"]
        kwargs = dict(project=scope["project"], counterpart=scope["counterpart"],
                      as_of=session.world().clock)
        original = qualified_p3_read(owner, session, **kwargs)
        assert len(original["records"]) == 1
        initial_head = owner.store.head()
        with monkeypatch.context() as fault:
            fault.setattr(owner, "source_hash", "0" * 64)
            with pytest.raises(RecursionRefusal, match="P6_P3_SOURCE_REGISTRY_MISMATCH"):
                qualified_p3_read(owner, session, **kwargs)
        with pytest.raises(RecursionRefusal, match="P6_P3_CLOCK_MISMATCH"):
            qualified_p3_read(owner, session, **{**kwargs, "as_of": kwargs["as_of"] - 1})
        assert qualified_p3_read(owner, session, **kwargs) == original
        assert owner.store.head() == initial_head
    finally:
        owner.close()
