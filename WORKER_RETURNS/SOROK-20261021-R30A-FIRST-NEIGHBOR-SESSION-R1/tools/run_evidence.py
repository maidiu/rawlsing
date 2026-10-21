#!/usr/bin/env python3
"""Execute real first-session receipts and write evidence JSON."""
from __future__ import annotations

import json
import shutil
import sqlite3
import tempfile
import traceback
from pathlib import Path

from r30a.first_session import FirstSession, SessionRefusal, USER_ACTOR
from r30a.faults import (
    copy_state,
    delete_episode_kinds,
    delete_offscreen_activity,
    private_tokens,
    tamper_speech_text,
)

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
R29P_REF = "001b506fa26ae879ff5b6e57138fc2696e12b538"


def dump_result(result):
    return {
        key: value
        for key, value in result.items()
        if key not in {"actor_events", "user_event"}
    }


def run_available(base):
    state = Path(base) / "available"
    session = FirstSession.start(state, scenario="available", attention="focused")
    receipt = {"schema": "R30A_SESSION_RECEIPT@1", "scenario": "available",
               "r29p_source_ref": R29P_REF, "actions": []}
    try:
        steps = [
            ("SAY", session.say("Hello. I just moved in.")),
            ("DO_HELP", session.do_help()),
            ("ATTEND", session.attend()),
            ("ASK_CONTACT", session.ask_contact()),
            ("WAIT", session.wait(30)),
            ("OFFSCREEN", session.advance_offscreen(30)),
            ("MESSAGES", session.check_messages()),
            ("RETURN", session.return_session()),
        ]
        for name, result in steps:
            receipt["actions"].append({"action": name, "result": dump_result(result)})
        receipt["verify"] = session.verify()
        receipt["custody"] = session.custody()
        receipt["b_public_after_return"] = session.product.other("A")["public"]
        receipt["status_after_return"] = session.status()
        receipt["events"] = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "actor_id", "clock", "location",
              "summary", "body")}
            for event in session.events()
        ]
        receipt["episodes"] = session.episodes()
        receipt["messages"] = session.messages()
        db_copy = EVID / "c12_available.sqlite"
        shutil.copy2(session.product.store.path, db_copy)
        receipt["c12_persisted_copy"] = {
            "path": str(db_copy.relative_to(ROOT)),
            "sha256": __import__("hashlib").sha256(db_copy.read_bytes()).hexdigest(),
        }
        return session, receipt
    finally:
        session.close()


def run_pressed(base):
    state = Path(base) / "pressed"
    session = FirstSession.start(state, scenario="pressed", attention="focused")
    receipt = {"schema": "R30A_SESSION_RECEIPT@1", "scenario": "pressed",
               "r29p_source_ref": R29P_REF, "actions": []}
    try:
        steps = [
            ("SAY", session.say("Hello. Do you need a hand?")),
            ("DO_HELP", session.do_help()),
            ("ASK_CONTACT", session.ask_contact()),
            ("WAIT", session.wait(30)),
            ("OFFSCREEN", session.advance_offscreen(30)),
            ("MESSAGES", session.check_messages()),
            ("RETURN", session.return_session()),
        ]
        for name, result in steps:
            receipt["actions"].append({"action": name, "result": dump_result(result)})
        receipt["verify"] = session.verify()
        receipt["custody"] = session.custody()
        receipt["events"] = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "actor_id", "clock", "location",
              "summary", "body")}
            for event in session.events()
        ]
        receipt["episodes"] = session.episodes()
        db_copy = EVID / "c12_pressed.sqlite"
        shutil.copy2(session.product.store.path, db_copy)
        receipt["c12_persisted_copy"] = {
            "path": str(db_copy.relative_to(ROOT)),
            "sha256": __import__("hashlib").sha256(db_copy.read_bytes()).hexdigest(),
        }
        return receipt
    finally:
        session.close()


def run_early_exit(base):
    state = Path(base) / "early"
    session = FirstSession.start(state, scenario="available", attention="focused")
    receipt = {"schema": "R30A_SESSION_RECEIPT@1", "scenario": "available_early_exit",
               "r29p_source_ref": R29P_REF, "actions": []}
    try:
        steps = [
            ("SAY", session.say("Hello.")),
            ("DO_HELP", session.do_help()),
            ("ASK_CONTACT", session.ask_contact()),
            ("LEAVE", session.leave()),
            ("OFFSCREEN", session.advance_offscreen(30)),
            ("MESSAGES", session.check_messages()),
            ("RETURN", session.return_session()),
        ]
        for name, result in steps:
            receipt["actions"].append({"action": name, "result": dump_result(result)})
        receipt["verify"] = session.verify()
        receipt["b_public_after_return"] = session.product.other("A")["public"]
        receipt["status_after_return"] = session.status()
        receipt["events"] = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "actor_id", "clock", "location",
              "summary", "body")}
            for event in session.events()
        ]
        return receipt
    finally:
        session.close()


def cold_reopen(state):
    before = None
    session = FirstSession.open(state)
    try:
        before = session.custody()
        verify_before = session.verify()
    finally:
        session.close()
    session = FirstSession.open(state)
    try:
        after = session.custody()
        verify_after = session.verify()
        return {
            "schema": "R30A_COLD_REOPEN@1",
            "before_target": before["source"]["custody"]["target_id"],
            "after_target": after["source"]["custody"]["target_id"],
            "before_consumed": before["source"]["custody"]["consumed_state_hash"],
            "after_consumed": after["source"]["custody"]["consumed_state_hash"],
            "same_person": before["source"]["custody"]["target_id"]
            == after["source"]["custody"]["target_id"],
            "same_consumed_state": before["source"]["custody"]["consumed_state_hash"]
            == after["source"]["custody"]["consumed_state_hash"],
            "verify_before": verify_before,
            "verify_after": verify_after,
            "counts_before": before["c12_counts"],
            "counts_after": after["c12_counts"],
        }
    finally:
        session.close()


def run_faults(base, available_state):
    out = {"schema": "R30A_FAULTS@1", "trials": []}

    def trial(name, func):
        try:
            detail = func()
            out["trials"].append({"name": name, "pass": True, "detail": detail})
        except Exception as exc:  # noqa: BLE001 - record exact fault
            out["trials"].append({"name": name, "pass": False,
                                  "detail": type(exc).__name__ + ": " + str(exc)})

    # Interior published-utterance tamper: verifier must refuse.
    def tamper_refusal():
        copied = copy_state(available_state, Path(base) / "fault_tamper")
        session = FirstSession.open(copied)
        try:
            event = next(e for e in session.events()
                         if e.get("kind") == "SPEECH" and e.get("actor_id") == "A")
            event_id = event["event_id"]
            original = event["hash"]
        finally:
            session.close()
        tamper_speech_text(copied, event_id, "A different sentence.", recompute=False)
        try:
            FirstSession.open(copied)
        except Exception as exc:  # noqa: BLE001
            return {"expected": "REFUSED", "actual": "REFUSED",
                    "error": type(exc).__name__ + ": " + str(exc),
                    "event_id": event_id, "original_hash": original}
        raise AssertionError("tampered C12 reopened without refusal")

    trial("tampered_committed_utterance_refused", tamper_refusal)

    # Recompute-only tamper: the original commitment identity changes.
    def recompute_identity():
        copied = copy_state(available_state, Path(base) / "fault_recompute")
        session = FirstSession.open(copied)
        try:
            event = next(e for e in session.events()
                         if e.get("kind") == "SPEECH" and e.get("actor_id") == "A")
            event_id, original = event["event_id"], event["hash"]
        finally:
            session.close()
        result = tamper_speech_text(copied, event_id, "A different sentence.",
                                    recompute=True)
        assert result["new_hash"] != original
        return result

    trial("recomputed_utterance_identity_differs", recompute_identity)

    # Remove B's offscreen episode/world events: C12 must refuse.
    def remove_b():
        copied = copy_state(available_state, Path(base) / "fault_b")
        removed = delete_offscreen_activity(copied)
        assert removed["events"] or removed["episodes"]
        try:
            FirstSession.open(copied)
        except Exception as exc:  # noqa: BLE001
            return {"removed": removed, "expected": "REFUSED",
                    "actual": "REFUSED", "error": type(exc).__name__ + ": " + str(exc)}
        raise AssertionError("C12 with B activity removed reopened")

    trial("removed_b_offscreen_refused", remove_b)

    # Remove the admitted user DO: C12 must refuse.
    def remove_user_do():
        copied = copy_state(available_state, Path(base) / "fault_udo")
        removed = delete_episode_kinds(copied, {"DO"})
        assert removed
        try:
            FirstSession.open(copied)
        except Exception as exc:  # noqa: BLE001
            return {"removed": removed, "expected": "REFUSED",
                    "actual": "REFUSED", "error": type(exc).__name__ + ": " + str(exc)}
        raise AssertionError("C12 with user DO removed reopened")

    trial("removed_user_do_refused", remove_user_do)

    # Retroactive time.
    def retroactive():
        session = FirstSession.open(available_state)
        try:
            from bp4.store import StoreRefusal
            try:
                session.product.store.append_episode(
                    session.branch_id, actor_id=USER_ACTOR, kind="SAY",
                    clock=1, body={"text": "backdated"})
            except StoreRefusal as exc:
                return {"expected": "REFUSED", "actual": "REFUSED", "code": exc.code}
            raise AssertionError("retroactive episode accepted")
        finally:
            session.close()

    trial("retroactive_time_refused", retroactive)

    # Hidden state must not cross the surface.
    def hidden():
        session = FirstSession.open(available_state)
        try:
            if not session.scene_open():
                session.return_session()
            text = "\n".join([
                json.dumps(session.status(), sort_keys=True),
                *session.say("Hello again.").get("surface", []),
                *session.attend().get("surface", []),
            ])
            leaked = [token for token in private_tokens(session) if token in text]
            assert not leaked, leaked
            return {"leaked": leaked, "expected": "none"}
        finally:
            session.close()

    trial("hidden_actor_state_not_leaked", hidden)

    # ATTEND without access: at the market, A is not present.
    def no_access():
        state = Path(base) / "fault_access"
        session = FirstSession.start(state, scenario="available", attention="focused")
        try:
            session.travel("market")
            attended = session.attend()
            said = session.say("Hello?")
            assert said["actor_events"] == []
            return {"attend_status": attended["status"], "actor_events": [],
                    "verify": session.verify()}
        finally:
            session.close()

    trial("attend_without_access", no_access)

    # Message without a channel.
    def no_channel():
        state = Path(base) / "fault_channel"
        session = FirstSession.start(state, scenario="pressed", attention="focused")
        try:
            session.say("Hello.")
            session.do_help()
            session.ask_contact()
            session.leave()
            session.advance_offscreen(30)
            try:
                session.send_message("Are you there?")
            except SessionRefusal as exc:
                return {"expected": "REFUSED", "actual": "REFUSED", "code": exc.code}
            raise AssertionError("message sent without channel")
        finally:
            session.close()

    trial("message_without_channel_refused", no_channel)

    out["all_pass"] = all(t["pass"] for t in out["trials"])
    return out


def attention_contrast(base):
    def run(name, attention):
        state = Path(base) / name
        session = FirstSession.start(state, scenario="available", attention=attention)
        try:
            first = session.say("Hello. I just moved in.")
            second = session.do_help()
            return {
                "events": [e["event_id"] for e in session.events()],
                "hashes": [e["hash"] for e in session.events()],
                "surface": first.get("surface", []) + second.get("surface", []),
                "verify": session.verify(),
            }
        finally:
            session.close()

    focused = run("attn_focused", "focused")
    distracted = run("attn_distracted", "distracted")
    return {
        "schema": "R30A_ATTENTION_CONTRAST@1",
        "same_event_ids": focused["events"] == distracted["events"],
        "same_event_hashes": focused["hashes"] == distracted["hashes"],
        "surface_differs": focused["surface"] != distracted["surface"],
        "focused_surface": focused["surface"],
        "distracted_surface": distracted["surface"],
        "verify": {"focused": focused["verify"], "distracted": distracted["verify"]},
    }


def main():
    base = Path(tempfile.mkdtemp(prefix="r30a-evidence-"))
    try:
        available, available_receipt = run_available(base)
        available_state = base / "available"
        (EVID / "session_available.json").write_text(
            json.dumps(available_receipt, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        cold = cold_reopen(available_state)
        (EVID / "cold_reopen.json").write_text(
            json.dumps(cold, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        pressed = run_pressed(base)
        (EVID / "session_pressed.json").write_text(
            json.dumps(pressed, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        early = run_early_exit(base)
        (EVID / "session_early_exit.json").write_text(
            json.dumps(early, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        faults = run_faults(base, available_state)
        (EVID / "faults.json").write_text(
            json.dumps(faults, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        attention = attention_contrast(base)
        (EVID / "attention_contrast.json").write_text(
            json.dumps(attention, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        # A compact event-commitment list from the primary available session.
        events = available_receipt["events"]
        commitments = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "actor_id", "clock", "summary")}
            for event in events
            if event.get("kind") in {"SPEECH", "REPAIR", "REFUSAL", "ARRIVAL"}
        ]
        (EVID / "event_commitments_available.json").write_text(
            json.dumps({"schema": "R30A_EVENT_COMMITMENTS@1",
                        "branch_id": "first_session",
                        "commitments": commitments},
                       indent=2, sort_keys=True) + "\n", encoding="utf8")
        print(json.dumps({
            "available_verify": available_receipt["verify"]["ok"],
            "pressed_verify": pressed["verify"]["ok"],
            "early_verify": early["verify"]["ok"],
            "cold_same_person": cold["same_person"],
            "cold_verify": cold["verify_after"]["ok"],
            "faults_all_pass": faults["all_pass"],
            "attention_same_events": attention["same_event_hashes"],
            "attention_surface_differs": attention["surface_differs"],
        }, indent=1))
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    main()
