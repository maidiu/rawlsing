"""S39 performer refusal, cold persistence and binding mismatch refusal."""
from __future__ import annotations

import json
import sqlite3

import pytest

from s39.bootstrap import install

install()

from candidate import digest  # noqa: E402
from s39.reader import S39ReadRefusal  # noqa: E402
from s39.session import S39GeneratedSession  # noqa: E402
from s37.harness import (  # noqa: E402
    case_for,
    setup_neutral_language,
    source_for,
)


def _start(state, share: bool):
    case = case_for(share)
    return S39GeneratedSession.start(state, case=case, source=source_for(case))


def test_independent_performer_refusal_is_not_success_or_practice(tmp_path):
    session = _start(tmp_path / "refuse", share=False)
    try:
        generated = session.read_generation()
        assert generated["selected_option"] == "REQUEST_TOOL"
        assert generated["attempt_status"] == "DENIED"
        assert generated["performed"] is False
        assert generated["event_id"] == ""
        assert generated["s36"]["outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        assert generated["s36"]["target_branch"] == "NO_CHANGE"
        assert generated["s36"]["target_proposals"] == []
        assert generated["s36"]["target_state_rows"] == 0
        assert not [
            event for event in session.events()
            if event.get("actor_id") == "A"
            and event.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}
        ]
        assert session.read_s36()["outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = S39GeneratedSession.open(tmp_path / "refuse")
    try:
        assert cold.read_generation()["attempt_status"] == "DENIED"
        assert cold.read_generation()["performed"] is False
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_cold_reopen_preserves_generation_action_c9_and_language(tmp_path):
    state = tmp_path / "cold-share"
    session = _start(state, share=True)
    try:
        setup_neutral_language(session)
        said = session.say("Hello.")
        speech_id = said["admission"]["speech_event_id"]
        speech_hash = said["admission"]["speech_event_hash"]
        generated = session.read_generation()
        read = session.read_s36()
    finally:
        session.close()

    cold = S39GeneratedSession.open(state)
    try:
        cold_generated = cold.read_generation()
        cold_read = cold.read_s36()
        assert cold_generated["generation_hash"] == generated["generation_hash"]
        assert cold_generated["attempt_hash"] == generated["attempt_hash"]
        assert cold_generated["selected_option"] == "REQUEST_TOOL"
        assert cold_generated["performed"] is True
        assert cold_generated["event_hash"] == generated["event_hash"]
        assert cold_read["response_ref"] == read["response_ref"]
        assert cold_read["outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        assert cold_read["target_branch"] == "NO_CHANGE"
        assert cold_read["target_reason"] == "NO_PROPOSAL"
        assert cold_read["target_state_rows"] == 0
        event = cold.event(speech_id)
        assert event is not None and event["hash"] == speech_hash
        view = cold.language_view(speech_id, locale="en")
        assert view["status"] == "OK"
        assert view["translation_text"] == "The bench is still here."
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def _tamper_generation_episode(state):
    session = S39GeneratedSession.open(state)
    try:
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "S39_CONSTRUCTIVE_GENERATION"
        ]
        assert len(rows) == 1
        body = dict(rows[0]["body"])
        body["tamper_note"] = "duplicate-generation-binding"
        session.product._append_episode(
            session.branch_id, "A", "S39_CONSTRUCTIVE_GENERATION",
            session.clock(), body,
        )
    finally:
        session.close()


def test_generation_binding_mismatch_is_refused(tmp_path):
    state = tmp_path / "mismatch"
    session = _start(state, share=True)
    try:
        original = session.meta["s39_generation_hash"]
        session.meta["s39_generation_hash"] = "0" * 64
        with pytest.raises(S39ReadRefusal) as exc:
            session.read_generation()
        assert exc.value.code == "S39_GENERATION_HASH_MISMATCH"
        session.meta["s39_generation_hash"] = original
        assert session.read_generation()["status"] == "OK"
    finally:
        session.close()
    _tamper_generation_episode(state)
    with pytest.raises(Exception) as exc:
        S39GeneratedSession.open(state)
    assert "S39_GENERATION" in str(exc.value)
