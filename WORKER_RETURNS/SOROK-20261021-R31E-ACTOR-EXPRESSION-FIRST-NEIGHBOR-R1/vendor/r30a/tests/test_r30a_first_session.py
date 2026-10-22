from __future__ import annotations

import json
import sqlite3

import pytest

from r30a.first_session import FirstSession, SessionRefusal, USER_ACTOR
from r30a.faults import (
    copy_state,
    delete_episode_kinds,
    delete_events,
    delete_offscreen_activity,
    tamper_speech_text,
)


def _event_texts(session):
    return {
        event["event_id"]: event.get("body", {}).get("text", "")
        for event in session.events()
        if event.get("kind") == "SPEECH"
    }


def _first_actor_speech(session, actor="A"):
    return next(
        event for event in session.events()
        if event.get("kind") == "SPEECH" and event.get("actor_id") == actor
    )


def test_available_session_help_contact_exit_offscreen_return_and_cold_reopen(tmp_path):
    state = tmp_path / "available"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        assert session.scene_open() is True
        assert session.verify()["ok"] is True
        said = session.say("Hello. I just moved in.")
        assert said["user_event"]["body"]["text"] == "Hello. I just moved in."
        first_speech = _first_actor_speech(session)
        assert first_speech["body"]["text"] == "Which side of the landing?"

        helped = session.do_help()
        assert helped["accepted"] is True
        repair = next(event for event in session.events() if event.get("kind") == "REPAIR")
        assert repair["owner_receipt"]["performed"] is True
        assert repair["owner_receipt"]["actor_id"] == "A"
        assert any(event.get("body", {}).get("text") ==
                   "Hold the near edge. I'll check the seam."
                   for event in session.events() if event.get("kind") == "SPEECH")

        attended = session.attend()
        assert attended["status"] == "NO_CHANGE"
        contact = session.ask_contact()
        assert contact["contact"] is True
        assert session.contact_status() is True

        waited = session.wait(30)
        assert waited["clock"] == 40
        assert session.scene_open() is False
        assert session.verify()["ok"] is True

        # The user leaves; the scene is already closed by A's departure.
        session.leave()
        off = session.advance_offscreen(30)
        assert off["clock"] == 70
        assert off["message"] is not None
        messages = session.check_messages()
        assert messages["contact"] is True
        assert len(messages["messages"]) == 1
        assert messages["messages"][0]["text"] == "The seam held. I'm at the market until six."

        before = session.custody()
        session.close()
        session = FirstSession.open(state)
        after = session.custody()
        assert after["source"]["custody"]["target_id"] == before["source"]["custody"]["target_id"]
        assert after["source"]["custody"]["consumed_state_hash"] == before["source"]["custody"]["consumed_state_hash"]
        assert session.contact_status() is True
        assert session.verify()["ok"] is True
        returned = session.return_session()
        assert returned["scene_open"] is True
        assert any("The seam held. You came back." in line for line in returned["surface"])
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_pressed_session_refuses_help_contact_and_message(tmp_path):
    state = tmp_path / "pressed"
    session = FirstSession.start(state, scenario="pressed", attention="focused")
    try:
        session.say("Hello. Do you need a hand?")
        refused = session.do_help()
        assert refused["accepted"] is False
        assert any("I can't take that on now." in line for line in refused["surface"])
        assert not any(event.get("kind") == "REPAIR" for event in session.events())
        contact = session.ask_contact()
        assert contact["contact"] is False
        assert session.contact_status() is False
        session.wait(30)
        assert session.scene_open() is False
        session.leave()
        off = session.advance_offscreen(30)
        assert off["message"] is None
        assert session.check_messages()["messages"] == []
        with pytest.raises(SessionRefusal) as exc:
            session.send_message("Are you there?")
        assert exc.value.code == "NO_CONTACT_CHANNEL"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_attention_changes_surface_not_occurrence(tmp_path):
    def run(name, attention):
        state = tmp_path / name
        session = FirstSession.start(state, scenario="available", attention=attention)
        try:
            said = session.say("Hello. I just moved in.")
            helped = session.do_help()
            events = [e["event_id"] for e in session.events()]
            bodies = [e["hash"] for e in session.events()]
            surface = said["surface"] + helped["surface"]
            return events, bodies, surface, session.verify()
        finally:
            session.close()

    focused = run("focused", "focused")
    distracted = run("distracted", "distracted")
    assert focused[0] == distracted[0]
    assert focused[1] == distracted[1]
    assert focused[2] != distracted[2]
    assert focused[3]["ok"] is True and distracted[3]["ok"] is True


def test_private_state_does_not_cross_surface(tmp_path):
    state = tmp_path / "private"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        output = []
        output.append(json.dumps(session.status(), sort_keys=True))
        for result in (session.say("Hello."), session.do_help(), session.ask_contact()):
            output.extend(result.get("surface", []))
        output.append(json.dumps(session.check_messages(), sort_keys=True, default=str))
        text = "\n".join(output)
        for token in ("cash", "debt_units", "free_hours", "material_remaining",
                      "practice_label", "nonmother_relations",
                      "TEST_ONLY_BP1_R26V_ACTOR_A", "projects"):
            assert token not in text
    finally:
        session.close()


def test_attend_before_access_does_not_see_other_room(tmp_path):
    state = tmp_path / "access"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        session.travel("market")
        attended = session.attend()
        assert attended["status"] == "NO_CHANGE"
        said = session.say("Hello?")
        assert said["actor_events"] == []
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_tampered_committed_speech_is_refused_on_reopen(tmp_path):
    source = tmp_path / "source"
    session = FirstSession.start(source, scenario="available", attention="focused")
    try:
        session.say("Hello.")
        speech = _first_actor_speech(session)
        event_id = speech["event_id"]
        original_hash = speech["hash"]
        session.close()
        copied = copy_state(source, tmp_path / "copied")
        tamper_speech_text(copied, event_id, "A different sentence.", recompute=False)
        with pytest.raises((SessionRefusal, RuntimeError, ValueError)):
            FirstSession.open(copied)
        # A recomputed but non-original utterance no longer carries the committed identity.
        copied2 = copy_state(source, tmp_path / "copied2")
        result = tamper_speech_text(copied2, event_id, "A different sentence.", recompute=True)
        assert result["new_hash"] != original_hash
        assert result["original_hash"] == original_hash
    finally:
        pass


def test_removed_b_activity_and_removed_user_do_break_c12(tmp_path):
    source = tmp_path / "fault_source"
    session = FirstSession.start(source, scenario="available", attention="focused")
    try:
        session.do_help()
        session.leave()
        session.advance_offscreen(30)
        assert session.verify()["ok"] is True
    finally:
        session.close()

    copied_b = copy_state(source, tmp_path / "copied_b")
    removed = delete_offscreen_activity(copied_b)
    assert removed["events"]
    with pytest.raises((SessionRefusal, RuntimeError, ValueError)):
        FirstSession.open(copied_b)

    copied_u = copy_state(source, tmp_path / "copied_u")
    removed = delete_episode_kinds(copied_u, {"DO"})
    assert removed
    with pytest.raises((SessionRefusal, RuntimeError, ValueError)):
        FirstSession.open(copied_u)


def test_retroactive_event_is_refused(tmp_path):
    state = tmp_path / "time"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        from bp4.store import StoreRefusal
        with pytest.raises(StoreRefusal) as exc:
            session.product.store.append_episode(
                session.branch_id, actor_id=USER_ACTOR, kind="SAY",
                clock=1, body={"text": "backdated"})
        assert exc.value.code == "RETROACTIVE_EPISODE"
    finally:
        session.close()


def test_fork_shares_past_and_verifies_both_branches(tmp_path):
    state = tmp_path / "fork"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        session.say("Hello.")
        fork = session.fork_alt()
        assert fork["status"] == "OK"
        session.product.use("alt")
        session.product.say("The alternate branch says this.", actor=USER_ACTOR)
        root_verify = session.product.store.verify("first_session")
        alt_verify = session.product.store.verify("alt")
        assert root_verify["ok"] is True
        assert alt_verify["ok"] is True
        assert alt_verify["counts"]["episode"] > root_verify["counts"]["episode"]
        shared = session.product.store.shared_root_equal("first_session", "alt")
        assert shared["equal"] is True
    finally:
        session.close()


def test_quiet_attend_can_trigger_actor_owned_question(tmp_path):
    state = tmp_path / "quiet"
    session = FirstSession.start(state, scenario="available", attention="focused")
    try:
        attended = session.attend()
        assert any("Can you see the gap?" in line for line in attended["surface"])
        initiate = [row for row in session.episodes("A") if row["kind"] == "INITIATE"]
        assert len(initiate) == 1
        assert initiate[0]["body"]["text"] == "You're looking at the seam. Can you see the gap?"
        assert session.verify()["ok"] is True
    finally:
        session.close()
