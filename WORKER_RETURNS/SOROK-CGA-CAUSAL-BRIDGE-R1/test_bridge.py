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
from actor_scene_context import recent_self_actions  # noqa: E402


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
        _run(state, "new", situated_house=True)


def _actual_state(state):
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        ledger = json.loads((state / "p4_receipts.json").read_text())
        scope = ledger["scope"]
        session = owner.base_owner.fanin.session
        packet = qualified_p3_read(
            owner, session, project=scope["project"], counterpart=scope["counterpart"],
            as_of=session.world().clock,
            interlocutor_role=scope["interlocutor_role"],
            relation_ref=scope["relation_ref"],
            actor_observed=bool(recent_self_actions(session)),
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
    _run(positive, "new", situated_house=True)
    _no_mediator_new(monkeypatch, negative)

    before_pos, before_speech_pos, before_head_pos = _actual_state(positive)
    before_neg, before_speech_neg, before_head_neg = _actual_state(negative)
    assert before_pos["records"] == [] and before_pos["status"] == "NO_QUALIFIED_P3_CANDIDATES"
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

    # A committed outward cue qualifies present actor perception; history
    # differs only by prior formation. Quiet/no-cue never grants B1 access.
    _run(positive, "approach", request_id="one", bridge=True,
         interpret=interpret, realize=realize)
    _run(negative, "approach", request_id="one", bridge=True,
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
    _run(state, "new", situated_house=True)
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        scope = json.loads((state / "p4_receipts.json").read_text())["scope"]
        kwargs = dict(project=scope["project"], counterpart=scope["counterpart"],
                      as_of=session.world().clock, interlocutor_role=scope["interlocutor_role"],
                      relation_ref=scope["relation_ref"],
                      actor_observed=bool(recent_self_actions(session)))
        original = qualified_p3_read(owner, session, **kwargs)
        assert original["records"] == []
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


def test_exact_same_cold_world_reader_severance_and_restoration(tmp_path):
    """Hold one actual sourced house fixed; approach produces a qualified cue."""
    import shutil

    state = tmp_path / "same-root"
    baseline = tmp_path / "frozen-baseline"
    _run(state, "new", situated_house=True)
    initial, initial_speech, initial_head = _actual_state(state)
    assert initial["records"] == []
    shutil.copytree(state, baseline)
    packets = []

    def interpret(packet):
        packets.append(packet)
        prior = packet.get("sourcefree_p3")
        return {
            "attention": "uncertain",
            "interpretation": "Bounded sourcefree prior-record counterfactual.",
            "action": "speak" if prior and prior["records"] else "continue",
            "cue_event_id": None, "channel": None,
        }

    def realize(packet, decision):
        assert packet["sourcefree_p3"]["readset"]
        return "The plan might be worth discussing."

    def go(*, bridge):
        _run(state, "approach", request_id="same-world-turn",
             interpret=interpret, realize=realize, bridge=bridge)
        _, speech, head = _actual_state(state)
        decision = json.loads((state / "p4_receipts.json").read_text())["turns"][-1][
            "receipt"]["situated"]["decision"]["action"]
        assert head == initial_head
        return decision, speech

    positive_action, positive_speech = go(bridge=True)
    assert positive_action == "speak"
    assert len(positive_speech) == len(initial_speech) + 1

    shutil.rmtree(state)
    shutil.copytree(baseline, state)
    negative_action, negative_speech = go(bridge=False)
    assert negative_action == "continue"
    assert negative_speech == initial_speech

    shutil.rmtree(state)
    shutil.copytree(baseline, state)
    restored_action, restored_speech = go(bridge=True)
    assert restored_action == "speak"
    assert len(restored_speech) == len(initial_speech) + 1
    assert restored_speech[-1]["body"]["text"] == positive_speech[-1]["body"]["text"]
    assert "sourcefree_p3" in packets[0]
    assert "sourcefree_p3" not in packets[1]
    assert packets[2]["sourcefree_p3"]["readset"] == packets[0]["sourcefree_p3"]["readset"]


def test_p3_activation_does_not_promote_inhibited_or_conflicting_history(tmp_path, monkeypatch):
    """Real P3 record, accepted P3 activation; synthetic conflict is a fault."""
    from copy import deepcopy
    from developmental_recursion.contracts import digest

    state = tmp_path / "qualification"
    _run(state, "new", situated_house=True)
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        scope = json.loads((state / "p4_receipts.json").read_text())["scope"]
        baseline = dict(
            project=scope["project"], counterpart=scope["counterpart"],
            as_of=session.world().clock, interlocutor_role=scope["interlocutor_role"],
            relation_ref=scope["relation_ref"],
        )
        head = owner.store.head()
        actual_history = owner.store.query(
            project=scope["project"], counterpart=scope["counterpart"],
            as_of=session.world().clock)
        assert len(actual_history) == 1

        # A root-bound record is *not* sufficient without the actor's
        # qualified current experience. A model may not infer that experience.
        unavailable = qualified_p3_read(owner, session, **baseline, actor_observed=False)
        assert unavailable["records"] == []
        assert unavailable["readset"] == []
        eligible_unit_probe = qualified_p3_read(
            owner, session, **baseline, actor_observed=True)
        assert [row["record_hash"] for row in eligible_unit_probe["records"]] == [
            actual_history[0]["hash"]]
        for modification in ({"interlocutor_role": "unqualified-role"},
                             {"relation_ref": "unqualified-relation"}):
            candidate = qualified_p3_read(
                owner, session, **{**baseline, **modification}, actor_observed=True)
            assert candidate["records"] == [] and candidate["readset"] == []

        # Test the existing P3 projection's incompatible-modes branch. This
        # forges a *reader result*, never a committed world/psyche record.
        competing = deepcopy(actual_history[0])
        competing["record_id"] += ":competing-mode"
        competing["payload"]["mode"] = (
            "private_check" if actual_history[0]["payload"]["mode"] == "joint_check"
            else "joint_check")
        competing["hash"] = digest({k: v for k, v in competing.items() if k != "hash"})
        with monkeypatch.context() as fault:
            fault.setattr(owner.store, "query", lambda **_kwargs: [
                deepcopy(actual_history[0]), competing])
            rejected = qualified_p3_read(
                owner, session, **baseline, actor_observed=True)
            assert rejected["status"] == "CONTRADICTION_HELD"
            assert rejected["records"] == rejected["readset"] == []
        assert qualified_p3_read(
            owner, session, **baseline, actor_observed=True) == eligible_unit_probe
        assert owner.store.head() == head
    finally:
        owner.close()


def test_quiet_wait_cannot_use_b1_as_unsourced_memory(tmp_path):
    """Earlier formation is not enough to grant current actor access."""
    state = tmp_path / "quiet"
    _run(state, "new", situated_house=True)
    _, before_speech, before_head = _actual_state(state)
    observed = []

    def interpret(packet):
        observed.append(packet["sourcefree_p3"])
        return {
            "attention": "uncertain", "interpretation": "No observed trigger.",
            "action": "continue", "cue_event_id": None, "channel": None,
        }

    _run(state, "wait", duration=4, request_id="no-cue",
         bridge=True, interpret=interpret)
    assert len(observed) == 1
    assert observed[0]["status"] == "NO_QUALIFIED_P3_CANDIDATES"
    assert observed[0]["records"] == observed[0]["readset"] == []
    _, after_speech, after_head = _actual_state(state)
    assert after_speech == before_speech
    assert after_head == before_head
