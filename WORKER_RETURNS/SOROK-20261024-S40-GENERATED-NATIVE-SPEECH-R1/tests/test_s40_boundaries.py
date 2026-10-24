"""S40 denial/nonverbal/OPEN and language-source/binding boundaries."""
from __future__ import annotations

import sqlite3

import pytest

from s40.bootstrap import install

install()

from s40.performer import S40LanguageRefusal  # noqa: E402
from s40.reader import S40ReadRefusal  # noqa: E402
from s40.session import S40GeneratedSession  # noqa: E402
from s39.model import S39GenerationRefusal  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _records(tmp_path, *, share=True, **flags):
    from s39.producer import GeneratedProducer

    case = case_for(share)
    source = source_for(case)
    probe = GeneratedProducer(tmp_path / "probe", case=case, source=source)
    try:
        probe.stage_m35()
        records = context_records(
            actor_id=probe.occurrence.actor_id,
            branch_id="first_session",
            as_of=probe.as_of,
            **flags,
        )
    finally:
        probe.close()
    return case, source, records


def test_denied_request_and_nonverbal_inspection_have_no_speech(tmp_path):
    case = case_for(False)
    denied = S40GeneratedSession.start(
        tmp_path / "denied", case=case, source=source_for(case)
    )
    try:
        s40 = denied.read_s40()
        assert s40["selected_option"] == "REQUEST_TOOL"
        assert s40["attempt_status"] == "DENIED"
        assert s40["performed"] is False
        assert s40["language_status"] == "NONE"
        assert s40["speech_event_id"] == ""
        assert s40["s36"]["outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        assert s40["s36"]["target_proposals"] == []
        assert not [
            event for event in denied.events()
            if event.get("actor_id") == "A"
            and event.get("kind") == "SPEECH"
        ]
        assert denied.verify()["ok"] is True
    finally:
        denied.close()

    case, source, records = _records(
        tmp_path, share=True, avoid_debt=True, prefer_independent=True
    )
    nonverbal = S40GeneratedSession.start(
        tmp_path / "nonverbal", case=case, source=source, source_records=records
    )
    try:
        s40 = nonverbal.read_s40()
        assert s40["selected_option"] == "ATTEND_OBJECT"
        assert s40["performed"] is True
        assert s40["language_status"] == "NONVERBAL"
        event = nonverbal.event(s40["action_event_id"])
        assert event["kind"] == "INSPECT"
        assert not [
            item for item in nonverbal.events()
            if item.get("actor_id") == "A"
            and item.get("kind") == "SPEECH"
        ]
        assert nonverbal.verify()["ok"] is True
    finally:
        nonverbal.close()


def test_open_start_appends_no_action(tmp_path):
    case, source, records = _records(tmp_path, share=True)
    state = tmp_path / "open"
    with pytest.raises(S39GenerationRefusal) as exc:
        S40GeneratedSession.start(
            state, case=case, source=source, source_records=records
        )
    assert exc.value.code == "S39_GENERATION_UNRESOLVED"
    assert not (state / "product").exists()
    assert not (state / "session.json").exists()


def test_missing_language_competence_refuses_without_fake_speech(tmp_path):
    case = case_for(True)
    state = tmp_path / "no-competence"
    with pytest.raises(S40LanguageRefusal) as exc:
        S40GeneratedSession.start(
            state, case=case, source=source_for(case), language_competence=False
        )
    assert exc.value.code == "S40_LANGUAGE_COMPETENCE_MISSING"
    c12 = state / "product" / "c12.sqlite"
    if c12.is_file():
        conn = sqlite3.connect(c12)
        try:
            bodies = [
                row[0] for row in conn.execute("SELECT body FROM world_event")
            ]
        finally:
            conn.close()
        assert not any('"kind": "SPEECH"' in body or '"kind":"SPEECH"' in body
                       for body in bodies)
    c9 = state / "source" / "bp2" / "c9.sqlite"
    if c9.is_file():
        conn = sqlite3.connect(c9)
        try:
            assert conn.execute("SELECT count(*) FROM response").fetchone()[0] == 0
            assert conn.execute("SELECT count(*) FROM target_state").fetchone()[0] == 0
        finally:
            conn.close()

    restored = S40GeneratedSession.start(
        tmp_path / "restored", case=case, source=source_for(case)
    )
    try:
        assert restored.read_s40()["language_status"] == "ACCEPTED"
        assert restored.read_s40()["native_text"] == "¿Puedo usar la herramienta?"
        assert restored.verify()["ok"] is True
    finally:
        restored.close()


def test_mismatched_projection_plan_binding_is_refused(tmp_path):
    case = case_for(True)
    state = tmp_path / "projection"
    session = S40GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        s40 = session.read_s40()
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "LANGUAGE_TRANSLATION_PROJECTION"
        ]
        assert len(rows) == 1
        body = dict(rows[0]["body"])
        body["plan_hash"] = "0" * 64
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
            session.clock(), body,
        )
        with pytest.raises(S40ReadRefusal):
            session.read_s40()
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S40GeneratedSession.open(state)


def test_wrong_public_e1_identity_refused_warm_and_cold(tmp_path):
    case = case_for(True)
    state = tmp_path / "wrong-e1"
    session = S40GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        s40 = session.read_s40()
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "EXPRESSION_ADMISSION"
            and (row.get("body") or {}).get("admission", {}).get(
                "speech_event_id"
            ) == s40["speech_event_id"]
        ]
        assert len(rows) == 1
        body = dict(rows[0]["body"])
        admission = dict(body["admission"])
        plan = dict(admission["plan"])
        readset = dict(plan["readset"])
        facts = [dict(item) for item in readset.get("public_outward_facts", [])]
        for fact in facts:
            if fact.get("kind") == "ADMITTED_E1":
                fact["event_id"] = "TEST_ONLY_WRONG_E1_ID"
                fact["event_hash"] = "0" * 64
        readset["public_outward_facts"] = facts
        plan["readset"] = readset
        admission["plan"] = plan
        body["admission"] = admission
        body["tamper_note"] = "wrong-e1-public-fact"
        session.product._append_episode(
            session.branch_id, "A", "EXPRESSION_ADMISSION",
            session.clock(), body,
        )
        with pytest.raises(S40ReadRefusal) as exc:
            session.read_s40()
        assert exc.value.code in {
            "S40_PLAN_E1_ID_MISMATCH",
            "S40_PLAN_E1_HASH_MISMATCH",
        }
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S40GeneratedSession.open(state)
