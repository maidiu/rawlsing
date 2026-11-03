from __future__ import annotations

import json

from wp19 import spec
from wp19.interface import EncounterInterface, render_text


def test_consumes_pinned_s11_spec():
    loaded = spec.load()
    assert loaded["schema"] == "SOROK_S11_WP19_INTERFACE_SPEC@1"
    assert loaded["native"] is False
    portal = loaded["surfaces"]["PORTAL"]["controls"]
    assert portal == ["SAY", "DO", "ATTEND", "WAIT", "EXIT"]
    assert "USER_ATTEND_RECEIPT" in {
        row["id"] for row in loaded["missing_producers"]
    }
    assert len(loaded["acceptance_examples"]) == 8


def test_cp_a5_real_reader_visible_and_unknown(tmp_path):
    interface = EncounterInterface("cp-a5", tmp_path / "cp-a5")
    view = interface.view()
    assert view["source"] == "cp-a5"
    assert view["mode"] == "PORTAL"
    assert view["visible_events"]
    assert view["unperceived_event_count"] > 0
    assert view["hidden_state_held"] is True
    tool = interface.ask("What happened to the workshop tool?")
    market = interface.ask("What did B do at the market?")
    assert tool["status"] == "OK"
    assert tool["answer"] == (
        "A perceived B take the workshop tool, could not repair while it "
        "was away, and perceived its return."
    )
    assert market["status"] == "UNKNOWN"
    assert market["answer"] == "UNKNOWN: A did not perceive B's market commission."
    assert market["evidence_event_ids"] == []
    assert tool["read_only"] is True
    assert market["read_only"] is True
    assert not any(
        event["kind"] == "B_MARKET_COMMISSION"
        for event in view["visible_events"]
    )
    assert interface.status()["store_mutated_since_load"] is False


def test_join_e_real_reader_accept_and_refusal(tmp_path):
    accept = EncounterInterface(
        "join-e",
        tmp_path / "join-e-accept",
        disposition="PERFORMED",
        perform="omit",
    )
    view = accept.view()
    assert view["source"] == "join-e"
    assert view["encounter_admission"]["accepted"] is True
    assert view["encounter_admission"]["strategy"] == "HELP_ACCEPT"
    accept_speech = [
        item for item in view["visible_speech"]
        if item["strategy"] == "HELP_ACCEPT"
    ]
    assert accept_speech
    assert (
        accept_speech[0]["text"],
        accept_speech[0]["gesture"],
    ) in {
        (
            "Put your hand on the near edge. I'll take the slack.",
            "A clears a space at the bench.",
        ),
        (
            "Hold the near edge. I'll check the seam.",
            "A sets the tool beside your hand.",
        ),
    }
    assert any(item["kind"] == "REPAIR" for item in view["visible_actions"])
    assert "SHARE_TOOL" not in json.dumps(view, sort_keys=True)
    refusal = EncounterInterface(
        "join-e",
        tmp_path / "join-e-refusal",
        disposition="REFUSED",
    )
    refusal_view = refusal.view()
    assert refusal_view["encounter_admission"]["accepted"] is False
    assert refusal_view["encounter_admission"]["strategy"] == "HELP_REFUSE"
    assert refusal_view["refusal_present"] is True
    assert any(
        item["text"] == "The tool's gone. I can't do it today."
        for item in refusal_view["visible_speech"]
    )
    assert not any(
        item["kind"] == "REPAIR" for item in refusal_view["visible_actions"]
    )
    assert accept.status()["store_mutated_since_load"] is False
    assert refusal.status()["store_mutated_since_load"] is False


def test_user_controls_are_typed_holds_not_world_actions(tmp_path):
    interface = EncounterInterface("join-e", tmp_path / "join-e")
    before = interface.status()["current_store_hash"]
    say = interface.say("Hello.")
    do = interface.do("inspect the bench")
    wait = interface.wait()
    return_result = interface.return_()
    for result in (say, do, wait, return_result):
        assert result["status"] in {"HELD", "OK"}
        assert result["world_event_created"] is False
        assert result["actor_response_generated"] is False
        assert result["simulated_delivery"] is False
    assert say["code"] == "USER_SAY_DO_ATTEMPT_ADMISSION_MISSING"
    assert do["code"] == "USER_SAY_DO_ATTEMPT_ADMISSION_MISSING"
    assert wait["code"] == "WAIT_UNSUPPORTED_TYPED_HOLD"
    assert return_result["code"] == "RETURN_UNSUPPORTED_TYPED_HOLD"
    exit_result = interface.exit()
    assert exit_result["code"] == "LOCAL_EXIT_ONLY"
    assert interface.mode == "OUTSIDE"
    status = interface.status()
    assert status["store_mutated_since_load"] is False
    assert status["current_store_hash"] == before


def test_attend_known_and_unperceived_targets(tmp_path):
    cp = EncounterInterface("cp-a5", tmp_path / "cp-a5")
    view = cp.view()
    known = view["visible_events"][0]
    attended = cp.attend(known["event_id"])
    assert attended["status"] == "OK"
    assert attended["code"] == "LOCAL_ATTEND_ONLY"
    assert attended["target"]["event_id"] == known["event_id"]
    hidden = cp.attend("TEST_ONLY_UNPERCEIVED_MARKET_COMMISSION")
    assert hidden["status"] == "UNKNOWN"
    assert hidden["code"] == "UNPERCEIVED_TARGET"
    assert "target" not in hidden
    join_e = EncounterInterface("join-e", tmp_path / "join-e")
    join_hidden = join_e.attend("TEST_ONLY_UNPERCEIVED_MARKET_COMMISSION")
    assert join_hidden["status"] == "UNKNOWN"
    assert "market commission" not in json.dumps(join_hidden, sort_keys=True).lower()


def test_accessibility_surface_and_text_rendering(tmp_path):
    interface = EncounterInterface("join-e", tmp_path / "join-e")
    view = interface.view()
    accessible = view["accessible"]
    assert accessible["keyboard_only"] is True
    assert accessible["focus_order"][0] == "transcript"
    assert accessible["focus_order"][-1] == "RETURN"
    assert accessible["exit_always_visible"] is True
    assert accessible["color_only_meaning"] is False
    assert accessible["typed_holds_announced"] is True
    assert view["exit_control"]["always_visible"] is True
    assert view["return_control"]["available"] is False
    assert view["return_control"]["reason"] == "RETURN_UNSUPPORTED_TYPED_HOLD"
    text = render_text(view)
    assert "Announcement:" in text
    assert "Exit:" in text
    assert "Return:" in text
    assert "UNKNOWN" in text or "Clock:" in text


def test_absence_and_status_are_honest(tmp_path):
    interface = EncounterInterface("cp-a5", tmp_path / "cp-a5")
    absence = interface.absence()
    assert absence["status"] == "UNKNOWN"
    assert absence["code"] == "USER_ABSENCE_LIFE_ADVANCE_MISSING"
    assert absence["world_event_created"] is False
    assert absence["clock_changed"] is False
    status = interface.status()
    assert status["native"] is False
    assert status["store_mutated_since_load"] is False
    assert status["baseline_store_hash"] == status["current_store_hash"]
