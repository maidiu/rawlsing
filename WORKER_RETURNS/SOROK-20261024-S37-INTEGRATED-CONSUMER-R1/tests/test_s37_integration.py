"""One integrated chain for both lawful B histories and cold persistence."""
from __future__ import annotations

import json
import sqlite3

import pytest

from s37.harness import (
    NATIVE_BENCH,
    setup_neutral_language,
    start_session,
    summary,
)
from s37.reader import S37ReadRefusal
from s37.session import S37IntegratedSession


@pytest.mark.parametrize("share", [True, False])
def test_same_targetless_session_reader_for_share_and_refuse(share, tmp_path):
    session = start_session(tmp_path / ("share" if share else "refuse"), share=share)
    try:
        data = summary(session)
        assert type(session) is S37IntegratedSession
        assert data["session_class"] == "S37IntegratedSession"
        assert data["source_operation"] == (
            "SHARE_TOOL" if share else "REFUSE_TOOL"
        )
        assert data["tools_remaining"] == (1 if share else 0)
        assert data["tool_available"] is share
        assert data["target_branch"] == "NO_CHANGE"
        assert data["target_reason"] == "NO_PROPOSAL"
        assert data["target_id"] == ""
        assert data["target_proposals"] == []
        assert data["target_state_rows"] == 0
        assert data["outcome"] == (
            "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
            if share
            else "OBSERVED_CURRENT_REFUSAL"
        )
        assert data["response_kind"] == (
            "REQUEST_TOOL" if share else "EXPLICIT_REFUSAL"
        )
        assert data["native"] is False
        assert data["e1_event_hash"] == session.meta["c8"]["e1_event_hash"]
        assert data["c8_occurrence_id"] in session.meta["s36"]["e1_event_id"]
        assert session.read_s36()["response_ref"] == data["response_ref"]
        assert session.status()["s36"]["response_ref"] == data["response_ref"]
        assert session.status()["s36"]["target_branch"] == "NO_CHANGE"
        assert session.status()["s36"]["target_reason"] == "NO_PROPOSAL"
        assert session.verify()["ok"] is True
    finally:
        session.close()


@pytest.mark.parametrize("share", [True, False])
def test_same_neutral_language_speech_and_resource_governed_help(share, tmp_path):
    session = start_session(tmp_path / ("lang-share" if share else "lang-refuse"),
                            share=share)
    try:
        setup_neutral_language(session)
        said = session.say("Hello.")
        assert said["strategy"] == "SAFE_GREETING"
        assert said["candidate"]["speech"] == NATIVE_BENCH
        assert said["language"]["plan"]["unit"]["unit_id"] == "SAFE_BENCH"
        assert said["language"]["native_artifact"]["text"] == NATIVE_BENCH
        assert said["language"]["translation_artifact"]["text"] == (
            "The bench is still here."
        )
        assert said["language"]["equivalence"]["status"] == "ACCEPTED"
        assert any("labeled English view" in line for line in said["surface"])
        plan_readset = said["language"]["plan"]["readset"]
        assert session.meta["c8"]["e1_event_hash"] not in {
            row.get("event_hash") for row in plan_readset.get("source_event_refs", [])
        }
        event_id = said["admission"]["speech_event_id"]
        view = session.language_view(event_id, locale="en")
        assert view["status"] == "OK"
        assert view["display_mode"] == "LABELED_ENGLISH"
        assert view["translation_text"] == "The bench is still here."
        assert view["source_preserved"] is True

        before = session.read_s36()["response_ref"]
        helped = session.do_help()
        assert helped["accepted"] is share
        assert helped["strategy"] == ("HELP_ACCEPT" if share else "HELP_REFUSE")
        assert session.read_s36()["response_ref"] == before
        assert session.read_s36()["target_branch"] == "NO_CHANGE"
        assert session.read_s36()["target_state_rows"] == 0
        assert session.verify()["ok"] is True
    finally:
        session.close()


@pytest.mark.parametrize("share", [True, False])
def test_cold_reopen_preserves_c9_reader_c12_and_language(share, tmp_path):
    state = tmp_path / ("cold-share" if share else "cold-refuse")
    session = start_session(state, share=share)
    try:
        setup_neutral_language(session)
        said = session.say("Hello.")
        event_id = said["admission"]["speech_event_id"]
        event_hash = said["admission"]["speech_event_hash"]
        response_ref = session.read_s36()["response_ref"]
        response_hashes = session.read_s36()["response_receipt_hash"]
        c9_receipt_hash = session.read_s36()["c9_receipt_hash"]
    finally:
        session.close()

    cold = S37IntegratedSession.open(state)
    try:
        read = cold.read_s36()
        assert read["response_ref"] == response_ref
        assert read["response_receipt_hash"] == response_hashes
        assert read["c9_receipt_hash"] == c9_receipt_hash
        assert read["target_branch"] == "NO_CHANGE"
        assert read["target_reason"] == "NO_PROPOSAL"
        assert read["target_state_rows"] == 0
        event = cold.event(event_id)
        assert event is not None
        assert event["hash"] == event_hash
        assert event["body"]["text"] == NATIVE_BENCH
        view = cold.language_view(event_id, locale="en")
        assert view["status"] == "OK"
        assert view["translation_status"] == "AVAILABLE"
        assert view["source_event_hash"] == event_hash
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_reader_reads_actual_committed_c9_rows_not_summary(tmp_path):
    session = start_session(tmp_path / "actual", share=True)
    try:
        read = session.read_s36()
        c9_path = session._c9_path()
        conn = sqlite3.connect(f"file:{c9_path}?mode=ro", uri=True)
        try:
            response_row = conn.execute(
                "SELECT body FROM response WHERE hash=?", (read["response_ref"],)
            ).fetchone()
            receipt_row = conn.execute(
                "SELECT body FROM receipt WHERE hash=?", (read["c9_receipt_hash"],)
            ).fetchone()
            target_count = conn.execute(
                "SELECT count(*) FROM target_state"
            ).fetchone()[0]
        finally:
            conn.close()
        assert response_row is not None
        assert receipt_row is not None
        assert target_count == 0
        stored_response = json.loads(response_row[0])
        stored_receipt = json.loads(receipt_row[0])
        assert stored_response["receipt_hash"] == read["response_receipt_hash"]
        assert stored_response["s35_receipt"]["hash"] == read["s35_receipt"]["hash"]
        assert stored_response["target_proposal_ref"] == ""
        assert stored_receipt["target_branch"] == read["target_branch"]
        assert stored_receipt["target_reason"] == read["target_reason"]
        assert stored_receipt["response_ref"] == read["response_ref"]
        assert read["s35_receipt"]["target_proposals"] == []
        session.meta["s36"]["response_ref"] = "0" * 64
        with pytest.raises(S37ReadRefusal):
            session.read_s36()
    finally:
        session.close()


def test_no_duplicate_actor_roots_or_replacement_ledger(tmp_path):
    session = start_session(tmp_path / "roots", share=True)
    try:
        root = session.product.store.branch("root")
        branch = session.product.store.branch(session.branch_id)
        assert sorted(root["actor_ids"]) == ["A", "B"]
        assert sorted(branch["actor_ids"]) == ["A", "B", "U"]
        assert session.meta["source_actor_map"] == {
            "TEST_ONLY_R31J_A": session.product.seed.public()["actor_a"],
            "TEST_ONLY_R31J_B": session.product.seed.public()["actor_b"],
        }
        assert session.product.seed.public()["actor_a"] == (
            "TEST_ONLY_BP1_R26V_ACTOR_A"
        )
        assert session.product.seed.public()["actor_b"] == (
            "TEST_ONLY_BP1_R26V_ACTOR_B"
        )
        assert session.product.seed.public()["c8_state_digest"] == (
            session.meta["c8"]["c8_state_digest"]
        )
        assert session.product.seed.public()["e1_event_hash"] == (
            session.meta["c8"]["e1_event_hash"]
        )
        assert session.product.seed.custody()["target_id"] == ""
        assert all(
            value is False
            for value in session.product.seed.custody()["native_grants"].values()
        )
        assert len(session.product.store.branches()) == 2
    finally:
        session.close()
