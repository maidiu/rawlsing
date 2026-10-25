"""Focused S45 same-consumer user encounter tests over an actual S44 root."""
from __future__ import annotations

import pytest

from s45.bootstrap import install

install()

from s45.fixtures import root_bundle  # noqa: E402
from s45.session import S45Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(state, *, seed="01" * 32, bundle=None, attention="focused"):
    case = case_for(True)
    return S45Session.start(
        state,
        bundle=bundle or root_bundle(seed),
        case=case,
        source=source_for(case),
        attention=attention,
        language_context={"milieu_id": "workshop"},
    )


def _b_speech(session):
    return (
        len([event for event in session.events()
             if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"]),
        len([event for event in session.events()
             if event.get("actor_id") == "A" and event.get("kind") == "SPEECH"]),
    )


def test_say_do_help_attend_with_cold_reopen_and_same_language_source(tmp_path):
    state = tmp_path / "person"
    session = _start(state)
    try:
        root = session.read_root()
        root_hash = root["root_hash"]
        assert len(session.read_events()) == 1
        before_b, before_a = _b_speech(session)

        said = session.say("Can I help?")
        assert said["status"] == "OK"
        assert said["strategy"] == "HELP_INVITE"
        assert said["candidate"]["speech"] in {
            "Si te ofreces, el borde cercano necesita una mano.",
            "Puedes sostener el borde cercano si lo dices en serio.",
        }
        assert said["language"]["native_text"] == said["candidate"]["speech"]
        assert said["language"]["translation_text"] in {
            "If you're offering, the near edge needs a hand.",
            "You can hold the near edge if you mean it.",
        }
        speech_id = said["language"]["speech_event_id"]
        view = session.language_view(speech_id, locale="en")
        assert view["display_mode"] == "LABELED_ENGLISH"
        assert view["source_preserved"] is True
        assert any("labeled English view" in line for line in said["surface"])
        assert session.read_encounters()[-1]["kind"] == "SAY"
        assert session.read_encounters()[-1]["source_event_refs"]
        assert _b_speech(session) == (before_b, before_a + 1)
        assert len(session.read_events()) == 2
    finally:
        session.close()

    session = S45Session.open(state)
    try:
        assert session.read_root()["root_hash"] == root_hash
        helped = session.do_help()
        assert helped["status"] == "OK"
        assert helped["accepted"] is True
        assert helped["strategy"] == "HELP_ACCEPT"
        assert helped["admission"]["action_event_id"]
        assert helped["admission"]["speech_event_id"]
        assert helped["language"]["native_text"] in {
            "Sostén el borde cercano. Revisaré la costura.",
            "Pon la mano en el borde cercano. Yo tomo la holgura.",
        }
        assert helped["language"]["translation_text"] in {
            "Hold the near edge. I'll check the seam.",
            "Put your hand on the near edge. I'll take the slack.",
        }
        assert session.read_encounters()[-1]["kind"] == "DO_HELP"
        assert session.read_encounters()[-1]["action_event_id"] == (
            helped["admission"]["action_event_id"]
        )
        assert len(session.read_events()) == 3
    finally:
        session.close()

    session = S45Session.open(state)
    try:
        attended = session.attend()
        assert attended["status"] == "NO_CHANGE"
        assert len(session.read_events()) == 4
        assert len(session.read_encounters()) == 3
        assert session.read_encounters()[-1]["kind"] == "ATTEND"
        assert session.read_encounters()[-1]["speech_event_id"] == ""
        assert session.read_root()["root_hash"] == root_hash
        assert _b_speech(session)[0] == before_b
        assert session.verify()["ok"] is True
        assert session.verify()["s45_encounters"]["count"] == 3
    finally:
        session.close()

    cold = S45Session.open(state)
    try:
        assert cold.read_root()["root_hash"] == root_hash
        assert len(cold.read_events()) == 4
        assert len(cold.read_encounters()) == 3
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_missing_help_source_is_typed_unsupported_not_silence(tmp_path):
    state = tmp_path / "unsupported"
    session = _start(state)
    try:
        before_a = _b_speech(session)[1]
        result = session.say("What is the weather?")
        assert result["status"] == "UNSUPPORTED"
        assert result["reason"].startswith("S45_")
        assert result["candidate"] is None
        assert _b_speech(session)[1] == before_a
        assert session.read_encounters()[-1]["status"] == "UNSUPPORTED"
        assert session.read_encounters()[-1]["speech_event_id"] == ""
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_user_help_attempt_refused_by_actual_material_state(tmp_path):
    state = tmp_path / "denied"
    session = _start(state, seed="00" * 32)
    try:
        assert session.world().actor_state["A"]["material_remaining"] == 0
        result = session.do_help()
        assert result["status"] == "OK"
        assert result["accepted"] is False
        assert result["admission"]["action_event_id"] == ""
        assert result["strategy"] == "HELP_REFUSE"
        assert result["language"]["native_text"] in {
            "Me quedé sin material. No puedo empezar eso ahora.",
            "La herramienta no está. Hoy no puedo hacerlo.",
        }
        assert session.read_encounters()[-1]["action_event_id"] == ""
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_source_access_revocation_refuses_then_restores(tmp_path):
    state = tmp_path / "fault"
    session = _start(state)
    try:
        first = session.say("Can I help?")
        receipts = [
            row["access_receipt_id"]
            for row in session.read_root()["language_evidence"]
            if "HELP_INVITE" in row["evidence_id"]
        ]
        for receipt in receipts:
            session.revoke_language_access(receipt, reason="TEST_ONLY_S45_FAULT")
        failed = session.say("Can I help?")
        assert failed["status"] == "UNSUPPORTED"
        assert failed["reason"] == "S45_LANGUAGE_SOURCE_UNAVAILABLE"
        assert session.read_encounters()[-1]["speech_event_id"] == ""
        for receipt in receipts:
            session.restore_language_access(receipt, reason="TEST_ONLY_S45_RESTORE")
        restored = session.say("Can I help?")
        assert restored["status"] == "OK"
        assert restored["strategy"] == "HELP_INVITE"
        assert restored["language"]["source_event_id"] in {
            row["source_event_id"]
            for row in session.read_root()["language_evidence"]
            if "HELP_INVITE" in row["evidence_id"]
        }
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_prior_root_events_and_root_hash_remain_unchanged(tmp_path):
    state = tmp_path / "root"
    session = _start(state)
    try:
        before = session.read_events()[0]
        root_hash = session.read_root()["root_hash"]
        session.say("Can I help?")
        session.do_help()
        session.attend()
        after = session.read_events()[0]
        assert after["e1_event_id"] == before["e1_event_id"]
        assert after["e1_event_hash"] == before["e1_event_hash"]
        assert session.read_root()["root_hash"] == root_hash
    finally:
        session.close()


def test_inherited_contact_semantics_are_not_downgraded(tmp_path):
    state = tmp_path / "contact"
    session = _start(state)
    try:
        session.say("Can I help?")
        session.do_help()
        asked = session.ask_contact()
        assert asked["status"] == "OK"
        assert asked["strategy"] in {
            "CONTACT_GRANT", "CONTACT_DEFER", "CONTACT_REFUSE",
        }
        assert "UNSUPPORTED" not in asked["surface"]
        assert session.verify()["ok"] is True
    finally:
        session.close()
