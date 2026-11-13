"""Agent A final counter: real J1 C04 selector and admission-time custody attacks.

These use the existing P2/P6/J1 world and C12 readers, rather than private
narrative fixtures. They are pytest obligations, not author-reported PASS until
executed in a complete source-closed checkout.
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
    read_child_experience, read_child_uptake, perform_parent_utterance,
    PARENT_UTTERANCE_KIND,
)
from run_p6 import child_speech_experience  # noqa: E402


def test_both_selectors_must_identify_one_same_speech(tmp_path):
    opened = open_j1_case(tmp_path / "selectors")
    try:
        s = opened["session"]
        eid = opened["receipt"]["event_id"]
        focal = opened["focal"]
        by_event = read_child_experience(s, focal, event_id=eid)
        by_operation = read_child_experience(
            s, focal, operation_id="j1-speech")
        both = read_child_experience(
            s, focal, event_id=eid, operation_id="j1-speech")
        assert by_event["status"] == "PERCEIVED"
        assert by_operation["event_id"] == eid
        assert both["event_id"] == eid
        assert both["response_input"] == by_operation["response_input"]
        assert child_speech_experience(
            s, event_id=eid, operation_id="j1-speech")["event_id"] == eid
        for kwargs in (
            {"event_id": "NOT_AN_EVENT", "operation_id": "j1-speech"},
            {"event_id": eid, "operation_id": "NOT_AN_OPERATION"},
            {"event_id": "", "operation_id": "j1-speech"},
            {"event_id": eid, "operation_id": ""},
        ):
            with pytest.raises(RecursionRefusal):
                read_child_experience(s, focal, **kwargs)
            with pytest.raises(RecursionRefusal):
                child_speech_experience(s, **kwargs)
        # A second authentic speech cannot be cross-spliced with the first.
        later = perform_parent_utterance(
            s, PARENT_ID, decision_id="j1-decision", text="Tomorrow maybe.",
            hidden_reason={"reason": "not a child disclosure"},
            operation_id="j1-speech:later")
        assert later["event_id"] != eid
        with pytest.raises(
            RecursionRefusal, match="CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND"
        ):
            read_child_experience(
                s, focal, event_id=eid, operation_id="j1-speech:later")
    finally:
        _close(opened)


def test_severed_historically_present_child_receipt_is_not_unheard(
    tmp_path, monkeypatch
):
    opened = open_j1_case(tmp_path / "child-severed")
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        child = opened["receipt"]["child_alias"]
        assert read_child_uptake(session, opened["focal"], eid)["status"] == "PERCEIVED"
        store = session.product.store
        original = store.perceptions

        def sever(branch_id, actor_id):
            rows = original(branch_id, actor_id)
            if actor_id == child:
                return [r for r in rows if r.get("event_id") != eid]
            return rows

        monkeypatch.setattr(store, "perceptions", sever)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_PERCEPTION_SEVERED"
        ):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        monkeypatch.setattr(store, "perceptions", original)
        assert read_child_uptake(session, opened["focal"], eid)["status"] == "PERCEIVED"
    finally:
        _close(opened)


def test_unheard_parent_speech_cannot_gain_forged_child_receipt(
    tmp_path, monkeypatch
):
    opened = open_j1_case(tmp_path / "unheard", child_present=False)
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        assert opened["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
        assert read_child_uptake(session, opened["focal"], eid)["status"] == "NOT_PERCEIVED"
        store = session.product.store
        original = store.perceptions
        child = opened["receipt"]["child_alias"]

        def forge(branch_id, actor_id):
            rows = original(branch_id, actor_id)
            if actor_id == child:
                return rows + [{
                    "event_id": eid, "channel": "speech",
                    "clock": opened["receipt"]["clock"],
                }]
            return rows

        monkeypatch.setattr(store, "perceptions", forge)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_FALSE_PERCEPTION"
        ):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        monkeypatch.setattr(store, "perceptions", original)
        assert read_child_uptake(session, opened["focal"], eid)["status"] == "NOT_PERCEIVED"
    finally:
        _close(opened)


def test_parent_own_speech_receipt_is_required_for_direct_child_uptake(
    tmp_path, monkeypatch
):
    opened = open_j1_case(tmp_path / "parent-own-severed")
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        alias = opened["receipt"]["alias"]
        store = session.product.store
        original = store.perceptions

        def sever(branch_id, actor_id):
            rows = original(branch_id, actor_id)
            if actor_id == alias:
                return [r for r in rows
                        if not (r.get("event_id") == eid
                                and r.get("channel") == "own_speech")]
            return rows

        monkeypatch.setattr(store, "perceptions", sever)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_PARENT_RECEIPT_SEVERED"
        ):
            read_child_uptake(session, opened["focal"], eid)
    finally:
        _close(opened)


def test_duplicate_child_perception_or_forged_speech_episode_refuses(
    tmp_path, monkeypatch
):
    opened = open_j1_case(tmp_path / "duplicate")
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        child = opened["receipt"]["child_alias"]
        store = session.product.store
        original = store.perceptions

        def duplicate(branch_id, actor_id):
            rows = original(branch_id, actor_id)
            return rows + rows[-1:] if actor_id == child else rows

        monkeypatch.setattr(store, "perceptions", duplicate)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_RECEIPT_DUPLICATE"
        ):
            read_child_uptake(session, opened["focal"], eid)
        monkeypatch.setattr(store, "perceptions", original)

        original_eps = store.episodes

        def forged_episode(branch_id):
            rows = original_eps(branch_id)
            result = []
            for row in rows:
                if (row.get("kind") == PARENT_UTTERANCE_KIND
                        and (row.get("body") or {}).get("event_id") == eid):
                    row = dict(row)
                    row["body"] = {**row["body"], "branch": "FORGED_BRANCH"}
                result.append(row)
            return result

        monkeypatch.setattr(store, "episodes", forged_episode)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_UTTERANCE_MISMATCH"
        ):
            read_child_uptake(session, opened["focal"], eid)
    finally:
        _close(opened)
