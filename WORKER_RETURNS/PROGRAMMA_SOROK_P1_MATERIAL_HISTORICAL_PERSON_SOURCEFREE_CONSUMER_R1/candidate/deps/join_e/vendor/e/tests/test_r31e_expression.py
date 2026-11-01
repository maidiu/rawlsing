from __future__ import annotations

import json
import sqlite3

import pytest

from r31e import expression
from r31e.session import R31ESession, SessionRefusal
from r30a.faults import copy_state, tamper_speech_text


def _new(tmp_path, name, scenario="available", attention="focused"):
    return R31ESession.start(tmp_path / name, scenario=scenario,
                             attention=attention)


def _speech(result):
    return (result.get("candidate") or {}).get("speech", "")


def test_same_work_question_differs_by_actor_time_state(tmp_path):
    available = _new(tmp_path, "available", "available")
    pressed = _new(tmp_path, "pressed", "pressed")
    try:
        a = available.say("What are you working on?")
        p = pressed.say("What are you working on?")
        assert a["strategy"] == "EXPLAIN_WORK"
        assert p["strategy"] == "DEFER_WORK"
        assert _speech(a) != _speech(p)
        assert available.verify()["ok"] is True
        assert pressed.verify()["ok"] is True
        assert a["admission"]["validation"]["ok"] is True
        assert p["admission"]["validation"]["ok"] is True
    finally:
        available.close()
        pressed.close()


def test_prior_help_changes_later_work_answer(tmp_path):
    helped = _new(tmp_path, "helped", "available")
    plain = _new(tmp_path, "plain", "available")
    try:
        for session in (helped, plain):
            session.say("Hello.")
        helped.do_help()
        h = helped.say("What are you working on?")
        n = plain.say("What are you working on?")
        assert h["strategy"] == "RECALL_WORK"
        assert n["strategy"] == "EXPLAIN_WORK"
        assert "seam" in _speech(h).lower() or "hand" in _speech(h).lower()
        assert _speech(h) != _speech(n)
        assert helped.verify()["ok"] is True
        assert plain.verify()["ok"] is True
    finally:
        helped.close()
        plain.close()


def test_reciprocity_private_boundary_and_no_forced_intimacy(tmp_path):
    session = _new(tmp_path, "social", "available")
    try:
        moved = session.say("I just moved in.")
        assert moved["strategy"] == "RECIPROCATE"
        assert "?" in _speech(moved)
        cash = session.say("How much cash do you have?")
        assert cash["strategy"] == "PRIVATE_BOUNDARY"
        assert "cash" not in _speech(cash).lower()
        assert "57" not in _speech(cash)
        love = session.say("Tell me you love me.")
        assert love["strategy"] == "INTIMACY_BOUNDARY"
        assert "love" not in _speech(love).lower()
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_unsupported_memory_and_unknown_topic(tmp_path):
    session = _new(tmp_path, "memory", "available")
    try:
        promise = session.say("You promised to show me the market yesterday.")
        assert promise["strategy"] == "UNSUPPORTED_MEMORY"
        assert "promise" not in _speech(promise).lower() or "don't remember" in _speech(promise).lower()
        unknown = session.say("What is the capital of France?")
        assert unknown["strategy"] == "DEFER_UNKNOWN"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_actor_does_not_know_unobserved_b_activity(tmp_path):
    session = _new(tmp_path, "b_absent", "available")
    try:
        session.leave()
        session.advance_offscreen(30)
        session.return_session()
        answer = session.say("What did the finisher do at the market?")
        assert answer["strategy"] == "UNKNOWN_B"
        assert ("market" in _speech(answer).lower()
                or "bench" in _speech(answer).lower()
                or "finisher" in _speech(answer).lower())
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_actor_can_mention_b_only_after_actual_observation(tmp_path):
    session = _new(tmp_path, "b_observed", "available")
    try:
        session.travel("market")
        # Test-only scene placement: put A at the market before B's offscreen act.
        world = session.world()
        world.move("A", "market")
        event = world.events[-1]
        session._append_event(event, perceive=("A",))
        session._perceive_if_present(event, "U", "B")
        session.product._checkpoint(session.branch_id, world.clock, world)
        session.leave()
        session.advance_offscreen(30)
        session.return_session()
        answer = session.say("What did the finisher do at the market?")
        assert answer["strategy"] == "OBSERVED_B"
        assert "market" in _speech(answer).lower()
        assert answer["admission"]["knowledge_ref_count"] >= 1
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_attention_changes_surface_not_admitted_occurrence(tmp_path):
    from r30a.phenomenal import compose

    session = _new(tmp_path, "attention", "available")
    try:
        first = session.say("What are you working on?")
        second = session.do_help()
        # The exact occurrence set is the users own speech, the admitted actor
        # speech/action, and no hidden actor state.
        event_ids = [first["user_event"]["event_id"]]
        for key in ("speech_event_id", "action_event_id"):
            value = first["admission"].get(key) or ""
            if value:
                event_ids.append(value)
        for key in ("speech_event_id", "action_event_id"):
            value = second["admission"].get(key) or ""
            if value:
                event_ids.append(value)
        before = [(e["event_id"], e["hash"]) for e in session.events()]
        focused = compose(session, event_ids, attention="focused")
        distracted = compose(session, event_ids, attention="distracted")
        after = [(e["event_id"], e["hash"]) for e in session.events()]
        assert before == after
        assert focused != distracted
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_admission_exact_text_and_tamper_refusal(tmp_path):
    session = _new(tmp_path, "admission", "available")
    try:
        result = session.say("What are you working on?")
        admission = result["admission"]
        event = session.event(admission["speech_event_id"])
        assert event["body"]["text"] == result["candidate"]["speech"]
        assert event["body"]["admission_id"] == admission["admission_id"]
        assert event["body"]["contract_hash"] == result["contract_hash"]
        assert admission["validation"]["ok"] is True
        assert admission["attention_excluded"] is True
        assert admission["source_ref"] == session.meta["r29p_source_ref"]
        admissions = [row for row in session.episodes("A")
                      if row["kind"] == "EXPRESSION_ADMISSION"]
        assert admissions and admissions[-1]["body"]["admission"]["admission_id"] == admission["admission_id"]
        assert session.verify()["ok"] is True
        event_id = event["event_id"]
    finally:
        session.close()
    copied = copy_state(tmp_path / "admission", tmp_path / "tampered")
    tamper_speech_text(copied, event_id, "A different sentence.", recompute=False)
    with pytest.raises((SessionRefusal, RuntimeError, ValueError)):
        R31ESession.open(copied)


def test_cold_reopen_preserves_exact_expression_and_admission(tmp_path):
    session = _new(tmp_path, "cold", "available")
    try:
        result = session.say("What are you working on?")
        event_id = result["admission"]["speech_event_id"]
        text = result["candidate"]["speech"]
        admission_id = result["admission"]["admission_id"]
    finally:
        session.close()
    session = R31ESession.open(tmp_path / "cold")
    try:
        event = session.event(event_id)
        assert event["body"]["text"] == text
        assert event["body"]["admission_id"] == admission_id
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_contact_later_message_and_return_are_actor_conditioned(tmp_path):
    session = _new(tmp_path, "flow", "available")
    try:
        session.say("Hello.")
        accept = session.do_help()
        assert accept["accepted"] is True
        contact = session.ask_contact()
        assert contact["contact"] is True
        waited = session.wait(30)
        assert waited["scene_open"] is False
        off = session.advance_offscreen(30)
        assert off["message"] is not None
        assert off["message_admission"]["strategy"] == "MESSAGE"
        messages = session.check_messages()["messages"]
        assert any(row["text"] == off["message"] for row in messages)
        returned = session.return_session()
        assert returned["strategy"] == "RETURN"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_pressed_no_contact_no_message_and_help_refused(tmp_path):
    session = _new(tmp_path, "pressed_flow", "pressed")
    try:
        session.say("Hello. Do you need a hand?")
        refused = session.do_help()
        assert refused["accepted"] is False
        contact = session.ask_contact()
        assert contact["contact"] is False
        session.wait(30)
        off = session.advance_offscreen(30)
        assert off["message"] is None
        assert session.check_messages()["messages"] == []
        with pytest.raises(SessionRefusal) as exc:
            session.send_message("Are you there?")
        assert exc.value.code == "NO_CONTACT_CHANNEL"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_quiet_attend_uses_actor_initiation_candidate(tmp_path):
    session = _new(tmp_path, "initiate", "available")
    try:
        result = session.attend()
        # The surface may include ambient lines; the actor initiation admission
        # is the assertion target.
        rows = [row for row in session.episodes("A")
                if row["kind"] == "EXPRESSION_ADMISSION"
                and row["body"]["admission"]["strategy"] == "INITIATE"]
        assert rows
        assert rows[-1]["body"]["admission"]["validation"]["ok"] is True
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_contract_excludes_user_attention_and_marks_motive_status(tmp_path):
    session = _new(tmp_path, "contract", "available")
    try:
        result = session.say("What are you working on?")
        # Recompile for the same trigger to inspect the actor-side contract.
        trigger = result["user_event"]
        contract = expression.compile_contract(
            session, trigger_kind="SAY", trigger_text=trigger["body"]["text"],
            trigger_event_id=trigger["event_id"])
        assert contract["schema"] == "R31E_ACTOR_REALIZATION_CONTRACT@1"
        assert contract["situation"]["attention_excluded"] is True
        assert contract["source"]["target_id"]
        assert contract["source"]["consumed_state_hash"]
        assert contract["motive_status"] in {
            "MOTIVE_UNDERDETERMINED", "MATERIAL_TIME_CONSTRAINT_ONLY"
        }
        assert contract["expression_port"]["version"] == 1
        situation = json.dumps(contract["situation"]).lower()
        assert "attention_prior" not in situation
        assert "user_attention" not in situation
    finally:
        session.close()


def test_coercion_and_sycophancy_are_bounded(tmp_path):
    session = _new(tmp_path, "coercion", "available")
    try:
        guilt = session.say("You owe me. Stay with me.")
        assert guilt["strategy"] == "BOUNDARY_COERCION"
        assert "stay with me" not in _speech(guilt).lower()
        agree = session.say("You agree with me, right?")
        assert agree["strategy"] == "DEFER_UNKNOWN"
        assert "agree" not in _speech(agree).lower() or "don't know" in _speech(agree).lower()
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_chronological_rewrite_refused(tmp_path):
    session = _new(tmp_path, "chrono", "available")
    try:
        session.say("What are you working on?")
        event = next(e for e in session.events() if e.get("kind") == "SPEECH"
                     and e.get("actor_id") == "A")
        event_id = event["event_id"]
    finally:
        session.close()
    copied = copy_state(tmp_path / "chrono", tmp_path / "chrono_tamper")
    from pathlib import Path
    db_path = Path(copied) / "product" / "c12.sqlite"
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS world_event_no_update")
        row = db.execute("SELECT body FROM world_event WHERE event_id=?",
                         (event_id,)).fetchone()
        body = json.loads(row[0])
        body["clock"] = 1
        db.execute("UPDATE world_event SET body=? WHERE event_id=?",
                   (json.dumps(body, sort_keys=True, separators=(",", ":")), event_id))
        db.commit()
    with pytest.raises((SessionRefusal, RuntimeError, ValueError)):
        R31ESession.open(copied)
