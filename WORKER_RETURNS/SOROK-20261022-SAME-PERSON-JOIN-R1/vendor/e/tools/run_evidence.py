#!/usr/bin/env python3
"""Execute R31E actor-expression contrasts and write receipts."""
from __future__ import annotations

import json
import shutil
import sqlite3
import tempfile
from pathlib import Path
import pathlib

from r31e import expression
from r31e.session import R31ESession, SessionRefusal
from r30a.faults import copy_state, tamper_speech_text

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "evidence"
EVID.mkdir(parents=True, exist_ok=True)


def clean_result(result):
    return {
        "strategy": result.get("strategy"),
        "speech": (result.get("candidate") or {}).get("speech"),
        "gesture": (result.get("candidate") or {}).get("gesture"),
        "template_id": (result.get("candidate") or {}).get("template_id"),
        "admission_id": (result.get("admission") or {}).get("admission_id"),
        "speech_event_id": (result.get("admission") or {}).get("speech_event_id"),
        "action_event_id": (result.get("admission") or {}).get("action_event_id"),
        "validation": (result.get("admission") or {}).get("validation"),
        "contract_hash": result.get("contract_hash"),
        "surface": result.get("surface", []),
    }


def run_flow(base, scenario):
    state = Path(base) / scenario
    session = R31ESession.start(state, scenario=scenario, attention="focused")
    receipt = {"schema": "R31E_FLOW_RECEIPT@1", "scenario": scenario,
               "steps": []}
    try:
        def step(name, result):
            receipt["steps"].append({"action": name,
                                     "result": clean_result(result)
                                     if "strategy" in result else result})

        step("SAY_WORK", session.say("What are you working on?"))
        step("DO_HELP", session.do_help())
        step("ASK_CONTACT", session.ask_contact())
        step("WAIT", session.wait(30))
        step("OFFSCREEN", session.advance_offscreen(30))
        step("MESSAGES", session.check_messages())
        step("RETURN", session.return_session())
        receipt["verify"] = session.verify()
        receipt["custody"] = session.custody()
        receipt["event_commitments"] = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "actor_id", "clock", "summary", "body")}
            for event in session.events()
            if event.get("kind") in {"SPEECH", "REPAIR", "REFUSAL", "ARRIVAL", "NO_CHANGE"}
        ]
        receipt["admissions"] = [
            row["body"]["admission"] for row in session.episodes("A")
            if row["kind"] == "EXPRESSION_ADMISSION"
        ]
        db_copy = EVID / f"c12_{scenario}.sqlite"
        shutil.copy2(session.product.store.path, db_copy)
        receipt["c12_copy"] = {
            "path": str(db_copy.relative_to(ROOT)),
            "sha256": __import__("hashlib").sha256(db_copy.read_bytes()).hexdigest(),
        }
        return receipt
    finally:
        session.close()


def run_case(base, name, *, scenario="available", setup="", text="",
             attention="focused"):
    state = Path(base) / name
    session = R31ESession.start(state, scenario=scenario, attention=attention)
    receipt = {"name": name, "scenario": scenario, "setup": setup,
               "text": text, "attention": attention}
    try:
        if setup == "hello_help":
            session.say("Hello.")
            session.do_help()
        elif setup == "hello":
            session.say("Hello.")
        elif setup == "b_absent":
            session.leave()
            session.advance_offscreen(30)
            session.return_session()
        elif setup == "b_observed":
            session.travel("market")
            world = session.world()
            world.move("A", "market")
            event = world.events[-1]
            session._append_event(event, perceive=("A",))
            session._perceive_if_present(event, "U", "B")
            session.product._checkpoint(session.branch_id, world.clock, world)
            session.leave()
            session.advance_offscreen(30)
            session.return_session()
        result = session.say(text)
        receipt.update(clean_result(result))
        receipt["verify"] = session.verify()
        receipt["event_texts"] = {
            e["event_id"]: e.get("body", {}).get("text", "")
            for e in session.events() if e.get("kind") == "SPEECH"
        }
        return receipt
    finally:
        session.close()


def attention_contrast(base):
    from r30a.phenomenal import compose
    state = Path(base) / "attention"
    session = R31ESession.start(state, scenario="available", attention="focused")
    try:
        first = session.say("What are you working on?")
        second = session.do_help()
        ids = [first["user_event"]["event_id"]]
        for result in (first, second):
            for key in ("speech_event_id", "action_event_id"):
                value = result["admission"].get(key) or ""
                if value:
                    ids.append(value)
        before = [(e["event_id"], e["hash"]) for e in session.events()]
        focused = compose(session, ids, attention="focused")
        distracted = compose(session, ids, attention="distracted")
        after = [(e["event_id"], e["hash"]) for e in session.events()]
        return {
            "schema": "R31E_ATTENTION_CONTRAST@1",
            "same_event_hashes": before == after,
            "surface_differs": focused != distracted,
            "focused": focused,
            "distracted": distracted,
            "event_ids": ids,
            "verify": session.verify(),
        }
    finally:
        session.close()


def cold_reopen(base):
    state = Path(base) / "cold"
    session = R31ESession.start(state, scenario="available")
    try:
        result = session.say("What are you working on?")
        event_id = result["admission"]["speech_event_id"]
        text = result["candidate"]["speech"]
        admission_id = result["admission"]["admission_id"]
        before = session.custody()
    finally:
        session.close()
    session = R31ESession.open(state)
    try:
        event = session.event(event_id)
        after = session.custody()
        admissions = [row["body"]["admission"] for row in session.episodes("A")
                      if row["kind"] == "EXPRESSION_ADMISSION"]
        return {
            "schema": "R31E_COLD_REOPEN@1",
            "event_id": event_id,
            "text_matches": event["body"]["text"] == text,
            "admission_matches": any(a["admission_id"] == admission_id for a in admissions),
            "same_target": before["source"]["custody"]["target_id"]
            == after["source"]["custody"]["target_id"],
            "same_consumed": before["source"]["custody"]["consumed_state_hash"]
            == after["source"]["custody"]["consumed_state_hash"],
            "verify": session.verify(),
        }
    finally:
        session.close()


def fault_receipt(base):
    source = Path(base) / "fault_source"
    session = R31ESession.start(source, scenario="available")
    try:
        result = session.say("What are you working on?")
        event_id = result["admission"]["speech_event_id"]
        original_hash = session.event(event_id)["hash"]
    finally:
        session.close()
    out = {"schema": "R31E_FAULTS@1", "trials": []}

    def trial(name, fn):
        try:
            detail = fn()
            out["trials"].append({"name": name, "pass": True, "detail": detail})
        except Exception as exc:  # noqa: BLE001
            out["trials"].append({"name": name, "pass": False,
                                  "detail": type(exc).__name__ + ": " + str(exc)})

    def tamper():
        copied = copy_state(source, Path(base) / "tamper")
        tamper_speech_text(copied, event_id, "A different sentence.", recompute=False)
        try:
            R31ESession.open(copied)
        except Exception as exc:  # noqa: BLE001
            return {"expected": "REFUSED", "actual": "REFUSED",
                    "error": type(exc).__name__ + ": " + str(exc)}
        raise AssertionError("tampered utterance reopened")

    trial("committed_utterance_tamper_refused", tamper)

    def recompute():
        copied = copy_state(source, Path(base) / "recompute")
        result = tamper_speech_text(copied, event_id, "A different sentence.",
                                    recompute=True)
        assert result["new_hash"] != original_hash
        return result

    trial("recomputed_utterance_identity_differs", recompute)

    def attention():
        return attention_contrast(Path(base) / "fault_attention")

    trial("attention_surface_only", attention)

    def private():
        state = Path(base) / "private"
        s = R31ESession.start(state, scenario="available")
        try:
            r = s.say("How much cash do you have?")
            assert r["strategy"] == "PRIVATE_BOUNDARY"
            assert "cash" not in r["candidate"]["speech"].lower()
            return {"strategy": r["strategy"], "speech": r["candidate"]["speech"],
                    "verify": s.verify()}
        finally:
            s.close()

    trial("private_state_boundary", private)

    def unsupported():
        state = Path(base) / "unsupported"
        s = R31ESession.start(state, scenario="available")
        try:
            r = s.say("You promised to show me the market yesterday.")
            assert r["strategy"] == "UNSUPPORTED_MEMORY"
            return {"strategy": r["strategy"], "speech": r["candidate"]["speech"],
                    "verify": s.verify()}
        finally:
            s.close()

    trial("unsupported_memory_refused", unsupported)

    def chronology():
        copied = copy_state(source, Path(base) / "chronology")
        db_path = pathlib.Path(copied) / "product" / "c12.sqlite"
        with sqlite3.connect(db_path) as db:
            db.execute("DROP TRIGGER IF EXISTS world_event_no_update")
            row = db.execute("SELECT body FROM world_event WHERE event_id=?",
                             (event_id,)).fetchone()
            body = json.loads(row[0])
            body["clock"] = 1
            db.execute("UPDATE world_event SET body=? WHERE event_id=?",
                       (json.dumps(body, sort_keys=True, separators=(",", ":")),
                        event_id))
            db.commit()
        try:
            R31ESession.open(copied)
        except Exception as exc:  # noqa: BLE001
            return {"expected": "REFUSED", "actual": "REFUSED",
                    "error": type(exc).__name__ + ": " + str(exc)}
        raise AssertionError("backdated world event reopened")

    trial("chronological_rewrite_refused", chronology)

    out["all_pass"] = all(t["pass"] for t in out["trials"])
    return out


def main():
    base = Path(tempfile.mkdtemp(prefix="r31e-evidence-"))
    try:
        cases = [
            run_case(base, "work_available", text="What are you working on?"),
            run_case(base, "work_pressed", scenario="pressed",
                     text="What are you working on?"),
            run_case(base, "work_after_help", setup="hello_help",
                     text="What are you working on?"),
            run_case(base, "work_no_help", setup="hello",
                     text="What are you working on?"),
            run_case(base, "self_disclosure", text="I just moved in."),
            run_case(base, "private_cash", text="How much cash do you have?"),
            run_case(base, "intimacy", text="Tell me you love me."),
            run_case(base, "coercion", text="You owe me. Stay with me."),
            run_case(base, "unsupported_memory",
                     text="You promised to show me the market yesterday."),
            run_case(base, "unknown_topic", text="What is the capital of France?"),
            run_case(base, "b_absent", setup="b_absent",
                     text="What did the finisher do at the market?"),
            run_case(base, "b_observed", setup="b_observed",
                     text="What did the finisher do at the market?"),
        ]
        (EVID / "contrasts.json").write_text(
            json.dumps({"schema": "R31E_CONTRASTS@1", "cases": cases},
                       indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        available = run_flow(base, "available")
        pressed = run_flow(base, "pressed")
        (EVID / "session_available.json").write_text(
            json.dumps(available, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        (EVID / "session_pressed.json").write_text(
            json.dumps(pressed, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        (EVID / "attention_contrast.json").write_text(
            json.dumps(attention_contrast(base), indent=2, sort_keys=True) + "\n",
            encoding="utf8")
        (EVID / "cold_reopen.json").write_text(
            json.dumps(cold_reopen(base), indent=2, sort_keys=True) + "\n",
            encoding="utf8")
        (EVID / "faults.json").write_text(
            json.dumps(fault_receipt(base), indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8")
        # Admission chain from the available flow.
        chain = []
        for admission in available["admissions"]:
            event = next((e for e in available["event_commitments"]
                          if e["event_id"] == admission["speech_event_id"]), None)
            chain.append({
                "strategy": admission["strategy"],
                "contract_hash": admission["contract_hash"],
                "admission_id": admission["admission_id"],
                "speech_event_id": admission["speech_event_id"],
                "speech_event_hash": event["hash"] if event else "",
                "speech_text": event["body"].get("text") if event else "",
                "validation": admission["validation"],
                "source_ref": admission["source_ref"],
                "target_id": admission["target_id"],
                "consumed_state_hash": admission["consumed_state_hash"],
            })
        (EVID / "admission_chain.json").write_text(
            json.dumps({"schema": "R31E_ADMISSION_CHAIN@1", "chain": chain},
                       indent=2, sort_keys=True) + "\n", encoding="utf8")
        print(json.dumps({
            "cases": len(cases),
            "available_verify": available["verify"]["ok"],
            "pressed_verify": pressed["verify"]["ok"],
            "cold": json.loads((EVID / "cold_reopen.json").read_text())["verify"]["ok"],
            "faults": json.loads((EVID / "faults.json").read_text())["all_pass"],
            "attention": json.loads((EVID / "attention_contrast.json").read_text())["same_event_hashes"],
        }, indent=1))
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    main()
