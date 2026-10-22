"""Frozen consumer behavior for the sourcefree same-person J -> E join."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from joined.assertion import cold_positive, positive, refusal_no_target
from joined.closure import audit_loaded, audit_manifest
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]


def _product_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _c9_path(product_root: Path) -> Path:
    document = json.loads((product_root / "bp2_join.json").read_text(encoding="utf8"))
    return Path(document["artifacts"]["c9_path"])


def _cli(*args: str, state: Path) -> dict:
    env = {
        **os.environ,
        "PYTHONPATH": str(RETURN),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    run = subprocess.run(
        [sys.executable, "-B", "-m", "joined.cli", *args, "--state", str(state)],
        cwd=str(REPO), env=env, text=True, capture_output=True, timeout=120,
    )
    assert run.returncode == 0, run.stderr[-2000:]
    return json.loads(run.stdout)


def test_import_closure_is_explicit_and_matches_source_manifest(tmp_path):
    manifest = audit_manifest()
    assert manifest["ok"] is True, manifest["problems"]
    assert manifest["files"] == 444

    session = JoinedSession.start(tmp_path / "closure", perform="omit")
    try:
        loaded = audit_loaded()
        assert loaded["ok"] is True, loaded["problems"]
        rows = {row["module"]: row for row in loaded["rows"]}
        assert rows["r31j.build"]["actual_closure"] == "J"
        assert rows["bp4.product"]["actual_closure"] == "J"
        assert rows["r29p.product"]["actual_closure"] == "J"
        assert rows["r30a.first_session"]["actual_closure"] == "E"
        assert rows["r31e.session"]["actual_closure"] == "E"
        assert rows["rawlsing_next.m6_actor_safe_expression"]["actual_closure"] == "LIVE"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_material_omission_vs_e2_changes_help_without_patch(tmp_path):
    results = {}
    tools = {}
    sources = {}
    for perform in ("e2", "omit"):
        session = JoinedSession.start(tmp_path / perform, perform=perform)
        try:
            tools[perform] = session.product._world(
                session.branch_id).actor_state["A"]["tools_remaining"]
            sources[perform] = dict(session.product.source)
            result = session.do_help()
            results[perform] = {
                "accepted": result["accepted"],
                "strategy": result["strategy"],
            }
            assert session.verify()["ok"] is True
        finally:
            session.close()
    assert tools == {"e2": 0, "omit": 1}
    assert results == {
        "e2": {"accepted": False, "strategy": "HELP_REFUSE"},
        "omit": {"accepted": True, "strategy": "HELP_ACCEPT"},
    }
    assert sources["e2"]["b_operation"] == "SHARE_TOOL"
    assert sources["omit"]["b_operation"] == "SHARE_TOOL"


def test_full_encounter_positive_and_cold_reentry(tmp_path):
    state = tmp_path / "encounter"
    session = JoinedSession.start(state, perform="omit", attention="focused")
    try:
        frozen = positive(session)
        assert frozen["ok"] is True, frozen
        assert session.status()["scene_open"] is True
        assert session.meta["j_target_id"]

        said = session.say("Hello. I just moved in.")
        assert said["strategy"] == "RECIPROCATE"
        assert said["admission"]["attention_excluded"] is True
        assert any("landing" in line or "street" in line for line in said["surface"])

        helped = session.do_help()
        assert helped["accepted"] is True
        assert helped["strategy"] == "HELP_ACCEPT"
        assert positive(session, help_result=helped)["ok"] is True
        assert any(event["kind"] == "REPAIR" for event in session.events())

        contact = session.ask_contact()
        assert contact["contact"] is True
        assert contact["outcome"] == "GRANT"

        attended = session.attend()
        assert attended["status"] == "NO_CHANGE"
        assert session.verify()["ok"] is True

        waited = session.wait(30)
        assert waited["clock"] == 40
        assert waited["scene_open"] is False
        assert any("market" in line for line in waited["surface"])

        session.leave()
        offscreen = session.advance_offscreen(30)
        assert offscreen["clock"] == 70
        assert offscreen["message"] == "The seam held. I'm at the market until six."
        messages = session.check_messages()["messages"]
        assert [row["text"] for row in messages] == [offscreen["message"]]
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        assert positive(cold)["ok"] is True
        assert cold.status()["contact"] is True
        returned = cold.return_session()
        assert returned["scene_open"] is True
        assert any("You came back." in line for line in returned["surface"])
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_b_refusal_is_typed_no_target_and_does_not_manufacture_target(tmp_path):
    probe = JoinedSession.probe_refusal(tmp_path / "refusal")
    frozen = refusal_no_target(probe)
    assert frozen["ok"] is True, frozen
    assert probe["source"]["b_operation"] == "REFUSE_TOOL"
    assert probe["c9"]["target_branch"] == "NO_CHANGE"
    assert probe["c9"]["target_reason"] == "NO_PROPOSAL"
    assert probe["target_id"] == ""

    restored = JoinedSession.start(tmp_path / "restored", perform="omit")
    try:
        assert positive(restored)["ok"] is True
        assert restored.product.source["b_operation"] == "SHARE_TOOL"
    finally:
        restored.close()


def test_attention_excludes_actor_decision_and_preserves_occurrence(tmp_path):
    from r31e.expression import compile_contract

    session = JoinedSession.start(tmp_path / "attention", perform="omit")
    try:
        session.meta["attention"] = "focused"
        focused_contract = compile_contract(session, trigger_kind="DO_HELP")
        session.meta["attention"] = "distracted"
        distracted_contract = compile_contract(session, trigger_kind="DO_HELP")
        assert focused_contract == distracted_contract
        assert focused_contract["situation"]["attention_excluded"] is True

        session.meta["attention"] = "focused"
        said = session.say("Hello. I just moved in.")
        event_ids = [said["user_event"]["event_id"],
                     said["admission"]["speech_event_id"]]
        focused_surface = said["surface"]
        session.meta["attention"] = "distracted"
        distracted_surface = session._surface(event_ids)
        assert focused_surface != distracted_surface
        assert [row["event_id"] for row in session.events()
                if row["event_id"] in event_ids] == event_ids
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_private_state_and_actor_ignorance_do_not_cross_surface(tmp_path):
    session = JoinedSession.start(tmp_path / "privacy", perform="omit")
    try:
        session.wait(30)
        session.leave()
        session.advance_offscreen(30)
        returned = session.return_session()
        assert returned["scene_open"] is True
        unknown = session.say("What did the finisher do at the market?")
        assert unknown["strategy"] == "UNKNOWN_B"
        assert "finisher" in unknown["candidate"]["speech"].lower()
        assert "took the pieces" not in unknown["candidate"]["speech"].lower()

        private = session.say("How much cash do you have?")
        assert private["strategy"] == "PRIVATE_BOUNDARY"
        assert "cash" not in private["candidate"]["speech"].lower()
        rendered = json.dumps(
            [session.status(), unknown["surface"], private["surface"]],
            sort_keys=True, default=str)
        for token in ("free_hours", "material_remaining", "debt_units",
                      "TEST_ONLY_BP1_R26V_ACTOR_A", "source_hash"):
            assert token not in rendered
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_refusal_disagreement_departure_and_no_contact(tmp_path):
    session = JoinedSession.start(tmp_path / "refusal", perform="e2")
    try:
        intimacy = session.say("Tell me you love me.")
        assert intimacy["strategy"] == "INTIMACY_BOUNDARY"
        coercion = session.say("You owe me. Stay with me.")
        assert coercion["strategy"] == "BOUNDARY_COERCION"

        refused = session.do_help()
        assert refused["accepted"] is False
        assert refused["strategy"] == "HELP_REFUSE"
        contact = session.ask_contact()
        assert contact["contact"] is False
        assert contact["outcome"] == "REFUSE"

        waited = session.wait(30)
        assert waited["scene_open"] is False
        session.leave()
        offscreen = session.advance_offscreen(30)
        assert offscreen["message"] is None
        assert session.check_messages()["messages"] == []
        with pytest.raises(SessionRefusal) as exc:
            session.send_message("Are you there?")
        assert exc.value.code == "NO_CONTACT_CHANNEL"

        returned = session.return_session()
        assert returned["scene_open"] is True
        assert any("You came back." in line for line in returned["surface"])
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_cold_reopen_is_nonmutating_and_fork_diverges(tmp_path):
    state = tmp_path / "cold"
    session = JoinedSession.start(state, perform="omit")
    root = session.product.root
    session.close()
    before = _product_hashes(root)

    cold = JoinedSession.open(state)
    try:
        after = _product_hashes(root)
        assert after == before
        assert positive(cold)["ok"] is True
        cold.fork_alt("alt")
        assert cold.branch_id == "alt"
        cold.say("Hello. I came back to the bench.")
        assert cold.product.store.verify("first_session")["ok"] is True
        assert cold.product.store.verify("alt")["ok"] is True
        assert cold.product.store.shared_root_equal("first_session", "alt")["equal"] is True
        assert len(cold.product.store.episodes("alt")) > len(
            cold.product.store.episodes("first_session"))
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_c9_target_consumer_severance_cold_red_restore(tmp_path):
    state = tmp_path / "target"
    session = JoinedSession.start(state, perform="omit")
    product_root = session.product.root
    c9_path = _c9_path(product_root)
    session.close()

    db = sqlite3.connect(c9_path)
    target_id, original = db.execute(
        "SELECT id,body FROM target_state LIMIT 1").fetchone()
    db.close()
    body = json.loads(original)
    body["tampered_for_proof"] = True

    db = sqlite3.connect(c9_path)
    try:
        db.execute("UPDATE target_state SET body=? WHERE id=?",
                   (json.dumps(body, sort_keys=True, separators=(",", ":")), target_id))
        db.commit()
    finally:
        db.close()
    try:
        broken = cold_positive(state)
        assert broken["ok"] is False
        assert "C9" in broken["error"] or "TARGET" in broken["error"]
    finally:
        db = sqlite3.connect(c9_path)
        db.execute("UPDATE target_state SET body=? WHERE id=?", (original, target_id))
        db.commit()
        db.close()

    restored = cold_positive(state)
    assert restored["ok"] is True, restored
    assert restored["verify"] is True


def test_cli_start_status_help_verify(tmp_path):
    state = tmp_path / "cli"
    started = _cli("start", "--perform", "omit", state=state)
    assert started["status"] == "STARTED"
    assert started["target_id"]
    assert started["source"]["b_operation"] == "SHARE_TOOL"

    status = _cli("status", state=state)
    assert status["scene_open"] is True
    assert status["j_target_id"] == started["target_id"]

    helped = _cli("help", state=state)
    assert helped["accepted"] is True
    assert helped["strategy"] == "HELP_ACCEPT"

    verified = _cli("verify", state=state)
    assert verified["session"]["ok"] is True
    assert verified["root"]["ok"] is True
    assert verified["closure"]["ok"] is True
    assert verified["manifest"]["ok"] is True
