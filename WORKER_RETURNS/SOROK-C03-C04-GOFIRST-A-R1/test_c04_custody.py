"""Hostile real-store C04 replay and parent self-read tests.

Uses the existing J1 fixture, ordinary P2 C12 world/perception stores and
registered parent. No new event/speech/psyche owner or mocked happy-path model.
"""
from __future__ import annotations

from pathlib import Path
import sys
import pytest

J1 = Path(__file__).resolve().parents[1] / "SOROK-E01-J1-995-R1"
if str(J1) not in sys.path:
    sys.path.insert(0, str(J1))
from test_j1_three_head_join import (  # noqa: E402
    PARENT_ID, HIDDEN, TEXT, open_j1_case, _close,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_speech import (  # noqa: E402
    perform_parent_utterance, read_parent_utterance,
    PARENT_UTTERANCE_KIND,
)


def _replay(session):
    return perform_parent_utterance(
        session, PARENT_ID, decision_id="j1-decision", text=TEXT,
        hidden_reason={"reason": HIDDEN}, operation_id="j1-speech",
    )


def test_replay_preserves_one_real_event_and_child_receipt(tmp_path):
    opened = open_j1_case(tmp_path / "intact")
    try:
        session = opened["session"]
        before = session.world()
        original = session.event(opened["receipt"]["event_id"])
        episode_count = len([
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == PARENT_UTTERANCE_KIND
            and (row.get("body") or {}).get("operation_id") == "j1-speech"
        ])
        assert episode_count == 1
        assert _replay(session)["status"] == "REPLAY"
        assert read_parent_utterance(
            session, PARENT_ID, "j1-speech", as_actor=PARENT_ID
        )["status"] == "READ"
        assert session.event(opened["receipt"]["event_id"]) == original
        assert session.world().clock == before.clock
        assert len([
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == PARENT_UTTERANCE_KIND
        ]) == episode_count
    finally:
        _close(opened)


def test_severed_speech_event_cannot_replay_or_pass_self_read(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "severed-event")
    try:
        session = opened["session"]
        actual = session.event
        event_id = opened["receipt"]["event_id"]
        monkeypatch.setattr(
            session, "event",
            lambda ref: None if ref == event_id else actual(ref),
        )
        with pytest.raises(RecursionRefusal, match="PARENT_UTTERANCE_EVENT_SEVERED"):
            _replay(session)
        with pytest.raises(RecursionRefusal, match="PARENT_UTTERANCE_EVENT_SEVERED"):
            read_parent_utterance(
                session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
        assert len([
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == PARENT_UTTERANCE_KIND
        ]) == 1
    finally:
        _close(opened)


def test_severed_own_speech_receipt_cannot_replay(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "severed-own-perception")
    try:
        session = opened["session"]
        store = session.product.store
        real_perceptions = store.perceptions
        parent_alias = opened["receipt"]["alias"]
        event_id = opened["receipt"]["event_id"]

        def sever_own(branch_id, actor_id):
            records = real_perceptions(branch_id, actor_id)
            if actor_id == parent_alias:
                return [
                    p for p in records
                    if not (p.get("event_id") == event_id
                            and p.get("channel") == "own_speech")
                ]
            return records

        monkeypatch.setattr(store, "perceptions", sever_own)
        with pytest.raises(
            RecursionRefusal, match="PARENT_UTTERANCE_OWN_SPEECH_SEVERED"
        ):
            _replay(session)
    finally:
        _close(opened)


def test_child_perception_missing_breaks_replay_without_granting_child_knowledge(
    tmp_path, monkeypatch
):
    opened = open_j1_case(tmp_path / "severed-child-perception")
    try:
        session = opened["session"]
        store = session.product.store
        real_perceptions = store.perceptions
        child_alias = opened["receipt"]["child_alias"]
        event_id = opened["receipt"]["event_id"]

        def sever_child(branch_id, actor_id):
            records = real_perceptions(branch_id, actor_id)
            if actor_id == child_alias:
                return [
                    p for p in records if p.get("event_id") != event_id
                ]
            return records

        monkeypatch.setattr(store, "perceptions", sever_child)
        with pytest.raises(
            RecursionRefusal, match="PARENT_UTTERANCE_CHILD_RECEIPT_SEVERED"
        ):
            _replay(session)
    finally:
        _close(opened)


def test_historically_unheard_speech_replays_without_invented_child_hearing(
    tmp_path,
):
    opened = open_j1_case(tmp_path / "unheard", child_present=False)
    try:
        session = opened["session"]
        assert opened["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
        assert _replay(session)["status"] == "REPLAY"
        assert read_parent_utterance(
            session, PARENT_ID, "j1-speech", as_actor=PARENT_ID
        )["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
    finally:
        _close(opened)


@pytest.mark.parametrize(
    "tamper,refusal",
    [
        ("actor", "PARENT_UTTERANCE_EVENT_SEVERED"),
        ("text", "PARENT_UTTERANCE_EVENT_SEVERED"),
        ("source", "PARENT_UTTERANCE_SOURCE_SEVERED"),
    ],
)
def test_forged_public_event_cannot_gain_parent_self_read(
    tmp_path, monkeypatch, tamper, refusal
):
    opened = open_j1_case(tmp_path / tamper)
    try:
        session = opened["session"]
        raw = session.event
        event_id = opened["receipt"]["event_id"]

        def fake(ref):
            event = raw(ref)
            if ref != event_id or event is None:
                return event
            event = dict(event)
            if tamper == "actor":
                event["actor_id"] = "IMPERSONATED_PARENT"
            else:
                event["body"] = dict(event["body"])
                if tamper == "text":
                    event["body"]["text"] = "I never said that."
                else:
                    event["body"]["utterance_source"] = "0" * 64
            return event

        monkeypatch.setattr(session, "event", fake)
        with pytest.raises(RecursionRefusal, match=refusal):
            _replay(session)
        with pytest.raises(RecursionRefusal, match=refusal):
            read_parent_utterance(
                session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
    finally:
        _close(opened)
