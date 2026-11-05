from __future__ import annotations

import hashlib
import json
import subprocess
import sys

import _pinned
from s45_projection import cli, projection
from s45_projection.adapter import S45Projection
from s45_projection.contract import load_contract


def _walk_public(value, path="<root>"):
    if isinstance(value, dict):
        for key, item in value.items():
            assert key not in projection.PRIVATE_KEYS, path + "." + str(key)
            _walk_public(item, path + "." + str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _walk_public(item, path + "[" + str(index) + "]")
    elif isinstance(value, str):
        for marker in projection.FORBIDDEN_VALUE_MARKERS:
            assert marker not in value, path + " contains " + marker


def _assert_public(*values):
    for value in values:
        _walk_public(value)


def test_contract_matches_pinned_wp19_and_s11(pinned):
    contract = load_contract()
    assert contract["schema"] == "SOROK_S45_WP19_PROJECTION_CONTRACT@1"
    assert contract["pins"]["base"] == "078d9c57bc835a34e90b3671bdef6c28a0f43747"
    assert contract["pins"]["s45_commit"] == pinned["s45_commit"]
    assert contract["pins"]["wp19_commit"] == pinned["wp19_commit"]
    assert contract["pins"]["s11_commit"] == pinned["s11_commit"]
    wp19 = pinned["wp19_interface"]
    assert contract["surface"]["view_schema"] == wp19.VIEW_SCHEMA
    assert contract["surface"]["result_schema"] == wp19.RESULT_SCHEMA
    assert projection.VIEW_SCHEMA == wp19.VIEW_SCHEMA
    assert projection.RESULT_SCHEMA == wp19.RESULT_SCHEMA
    s11 = json.loads(pinned["s11_spec"].read_text(encoding="utf8"))
    assert list(projection.HIDDEN_FIELDS) == s11["hidden_fields"]
    assert list(projection.PORTAL_CONTROLS) == s11["surfaces"]["PORTAL"]["controls"]
    assert list(contract["surface"]["controls"]) == s11["surfaces"]["PORTAL"]["controls"]
    assert list(contract["surface"]["hidden_fields"]) == s11["hidden_fields"]
    missing = {row["id"] for row in s11["missing_producers"]}
    remaining = set(contract["surface"]["remaining_missing_producers"])
    supplied = set(contract["surface"]["supplied_by_s45"])
    assert remaining < missing
    assert supplied == {
        "USER_SAY_DO_ATTEMPT_ADMISSION",
        "USER_ATTEND_RECEIPT",
    }
    assert not remaining & supplied
    assert projection.TYPED_HOLDS["WAIT"] == (
        s11["control_semantics"]["WAIT"]["interim_result"]
    )
    assert projection.TYPED_HOLDS["EXIT"] == (
        s11["control_semantics"]["EXIT"]["interim_label"]
    )
    assert projection.TYPED_HOLDS["RETURN"] == (
        s11["control_semantics"]["RETURN"]["interim_result"]
    )
    assert contract["consumed_callables"]["session_say"] == (
        "s45.session.S45Session.say"
    )
    assert contract["consumed_callables"]["session_do_help"] == (
        "s45.session.S45Session.do_help"
    )
    assert contract["consumed_callables"]["session_attend"] == (
        "s45.session.S45Session.attend"
    )


def test_pinned_source_files_are_exact(pinned):
    pairs = (
        (pinned["s45_commit"], _pinned.S45_RETURN + "/s45/session.py"),
        (pinned["s45_commit"], _pinned.S45_RETURN + "/s45/language.py"),
        (pinned["s45_commit"], _pinned.S45_RETURN + "/s45/fixtures.py"),
        (pinned["wp19_commit"], _pinned.WP19_RETURN + "/wp19/interface.py"),
        (pinned["s11_commit"], _pinned.S11_SPEC),
    )
    for commit, relative in pairs:
        runtime_bytes = (pinned["runtime"] / relative).read_bytes()
        git_bytes = subprocess.check_output(
            ["git", "show", commit + ":" + relative],
            cwd=str(pinned["repo"]),
        )
        assert hashlib.sha256(runtime_bytes).hexdigest() == (
            hashlib.sha256(git_bytes).hexdigest()
        )


def test_actual_say_is_public_attempt_not_performance(happy):
    result = happy["say"]
    raw = happy["raw_say"]
    assert raw["status"] == "OK"
    assert result["schema"] == projection.RESULT_SCHEMA
    assert result["status"] == "OK"
    assert result["attempted"] is True
    assert result["performed"] is False
    assert result["user_attempt"]["control"] == "SAY"
    assert result["user_attempt"]["input"] == "Can I help?"
    assert result["user_attempt"]["performed"] is False
    assert result["actor_response"]["strategy"] == "HELP_INVITE"
    assert result["actor_response"]["performed"] is False
    assert result["actor_response"]["speech"] == raw["language"]["native_text"]
    assert result["actor_response"]["speech_english"] == (
        raw["language"]["translation_text"]
    )
    assert result["world_event_created"] is True
    assert result["actor_response_generated"] is True
    assert result["simulated_delivery"] is False
    _assert_public(result, happy["view_initial"])


def test_actual_do_help_separates_attempt_from_actor_repair(happy):
    result = happy["do_help"]
    raw = happy["raw_do_help"]
    assert raw["accepted"] is True
    assert result["status"] == "OK"
    assert result["attempted"] is True
    assert result["performed"] is False
    assert result["user_attempt"]["control"] == "DO_HELP"
    assert result["user_attempt"]["performed"] is False
    assert result["actor_response"]["strategy"] == "HELP_ACCEPT"
    assert result["actor_response"]["action"] == "REPAIR"
    assert result["actor_response"]["performed"] is True
    assert result["actor_response"]["performed_by"] == "A"
    assert result["actor_response"]["speech"] == raw["language"]["native_text"]
    assert result["actor_response"]["speech_english"] == (
        raw["language"]["translation_text"]
    )
    assert result["world_event_created"] is True
    _assert_public(result)


def test_actual_attend_is_no_change_and_public(happy):
    result = happy["attend"]
    raw = happy["raw_attend"]
    assert raw["status"] == "NO_CHANGE"
    assert result["status"] == "NO_CHANGE"
    assert result["code"] == "LOCAL_ATTEND_ONLY"
    assert result["attempted"] is True
    assert result["performed"] is False
    assert result["world_event_created"] is False
    assert result["clock_changed"] is False
    assert result["actor_response"] is None
    assert result["actor_response_generated"] is False
    _assert_public(result)


def test_view_exposes_only_public_perceived_surface(happy):
    view = happy["view"]
    assert view["schema"] == projection.VIEW_SCHEMA
    assert view["source"] == "s45"
    assert view["mode"] == "PORTAL"
    assert view["hidden_state_held"] is True
    assert view["hidden_fields"] == list(projection.HIDDEN_FIELDS)
    assert view["controls"] == list(projection.PORTAL_CONTROLS)
    assert view["accessible"]["keyboard_only"] is True
    assert view["accessible"]["exit_always_visible"] is True
    assert view["exit_control"]["always_visible"] is True
    assert view["return_control"]["available"] is False
    assert view["return_control"]["reason"] == projection.TYPED_HOLDS["RETURN"]
    assert view["accessibility_announcement"]
    assert len(view["visible_events"]) == happy["perceived_event_count"]
    assert view["unperceived_event_count"] == (
        happy["raw_event_count"] - happy["perceived_event_count"]
    )
    for event in view["visible_events"]:
        assert set(event) == set(projection.PUBLIC_EVENT_FIELDS)
        assert event["perceived_by_user"] is True
        assert set(event["body_public"]) <= set(projection.PUBLIC_BODY_FIELDS)
    raw = happy["raw_do_help"]
    speech = next(
        row for row in view["visible_speech"]
        if row["event_id"] == raw["language"]["speech_event_id"]
    )
    assert speech["speaker"] == "A"
    assert speech["labeled_english"] == raw["language"]["translation_text"]
    assert any(row["kind"] == "REPAIR" for row in view["visible_actions"])
    assert view["encounter_admission"]["kind"] == "DO_HELP"
    assert view["encounter_admission"]["accepted"] is True
    assert view["encounter_admission"]["refusal"] is False
    assert view["encounter_admission"]["speech"] == raw["language"]["native_text"]
    _assert_public(view)
    assert happy["status"]["schema"] == projection.STATUS_SCHEMA
    assert happy["status"]["source"] == "s45"
    assert happy["status"]["store_mutated_since_load"] is True
    _assert_public(happy["status"])


def test_actual_refusal_is_preserved_without_action(refusal):
    from s45.language import PAIRS

    raw = refusal["raw"]
    result = refusal["result"]
    assert raw["status"] == "OK"
    assert raw["accepted"] is False
    assert raw["strategy"] == "HELP_REFUSE"
    assert result["status"] == "REFUSED"
    assert result["code"] == "S45_HELP_REFUSE"
    assert result["attempted"] is True
    assert result["performed"] is False
    assert result["refusal"] is True
    assert result["actor_response"]["strategy"] == "HELP_REFUSE"
    assert result["actor_response"]["performed"] is False
    assert result["actor_response"]["action"] == ""
    assert result["world_event_created"] is True
    pairs = {
        (row["native_text"], row["target_text"])
        for row in PAIRS.values()
        if "HELP_REFUSE" in row["atoms"]
    }
    assert (
        result["actor_response"]["speech"],
        result["actor_response"]["speech_english"],
    ) in pairs
    view = refusal["view"]
    assert view["refusal_present"] is True
    assert view["encounter_admission"]["kind"] == "DO_HELP"
    assert view["encounter_admission"]["accepted"] is False
    assert view["encounter_admission"]["refusal"] is True
    assert view["encounter_admission"]["speech"] == result["actor_response"]["speech"]
    assert not any(row["kind"] == "REPAIR" for row in view["visible_actions"])
    _assert_public(result, view)


def test_actual_unsupported_is_unknown(unsupported):
    raw = unsupported["raw"]
    result = unsupported["result"]
    assert raw["status"] == "UNSUPPORTED"
    assert raw["reason"].startswith("S45_")
    assert result["status"] == "UNKNOWN"
    assert result["code"] == "S45_UNSUPPORTED_INPUT"
    assert result["reason"].startswith("S45_")
    assert result["attempted"] is True
    assert result["performed"] is False
    assert result["actor_response"] is None
    assert result["actor_response_generated"] is False
    assert result["refusal"] is False
    view = unsupported["view"]
    assert view["encounter_admission"]["kind"] == "SAY"
    assert view["encounter_admission"]["status"] == "UNSUPPORTED"
    assert view["encounter_admission"]["speech"] == ""
    assert view["encounter_admission"]["refusal"] is False
    _assert_public(result, view)


def test_attend_local_exit_and_typed_holds(local_adapter):
    attend = local_adapter.attend()
    assert attend["status"] == "NO_CHANGE"
    assert attend["world_event_created"] is False
    before = local_adapter.status()["current_store_hash"]
    wait = local_adapter.wait()
    assert wait["status"] == "HELD"
    assert wait["code"] == projection.TYPED_HOLDS["WAIT"]
    assert wait["clock_changed"] is False
    assert wait["world_event_created"] is False
    assert wait["store_hash_before"] == wait["store_hash_after"] == before
    returned = local_adapter.return_()
    assert returned["status"] == "HELD"
    assert returned["code"] == projection.TYPED_HOLDS["RETURN"]
    assert returned["store_hash_before"] == returned["store_hash_after"] == before
    exited = local_adapter.exit()
    assert exited["status"] == "OK"
    assert exited["code"] == projection.TYPED_HOLDS["EXIT"]
    assert exited["mode"] == "OUTSIDE"
    assert exited["world_event_created"] is False
    assert exited["store_hash_before"] == exited["store_hash_after"] == before
    absence = local_adapter.absence()
    assert absence["status"] == "UNKNOWN"
    assert absence["code"] == projection.TYPED_HOLDS["ABSENCE"]
    assert absence["store_hash_before"] == absence["store_hash_after"] == before
    view = local_adapter.view()
    assert view["mode"] == "OUTSIDE"
    assert view["return_control"]["available"] is False
    assert local_adapter.status()["current_store_hash"] == before
    _assert_public(wait, returned, exited, absence, view)


def test_cli_contract_end_to_end(tmp_path, pinned, capsys):
    root = tmp_path / "cli-person"

    def run(*args):
        capsys.readouterr()
        code = cli.main(["--root", str(root), *args])
        captured = capsys.readouterr()
        assert code == 0, captured.err
        return json.loads(captured.out)

    view = run("--start", "view")
    assert view["schema"] == projection.VIEW_SCHEMA
    assert view["mode"] == "PORTAL"
    say = run("say", "Can I help?")
    assert say["attempted"] is True
    assert say["performed"] is False
    assert say["actor_response"]["strategy"] == "HELP_INVITE"
    helped = run("do", "help")
    assert helped["attempted"] is True
    assert helped["performed"] is False
    assert helped["actor_response"]["performed"] is True
    attended = run("attend")
    assert attended["status"] == "NO_CHANGE"
    assert attended["world_event_created"] is False
    waited = run("wait")
    assert waited["code"] == projection.TYPED_HOLDS["WAIT"]
    assert waited["store_hash_before"] == waited["store_hash_after"]
    returned = run("return")
    assert returned["code"] == projection.TYPED_HOLDS["RETURN"]
    assert returned["store_hash_before"] == returned["store_hash_after"]
    capsys.readouterr()
    code = cli.main(["--root", str(root), "view", "--text"])
    text = capsys.readouterr().out
    assert code == 0
    assert "Mode: PORTAL" in text
    assert "Announcement:" in text
    assert "Exit:" in text
    assert "Return:" in text
    exited = run("exit")
    assert exited["code"] == projection.TYPED_HOLDS["EXIT"]
    assert exited["mode"] == "OUTSIDE"
    assert exited["store_hash_before"] == exited["store_hash_after"]
    status = run("status")
    assert status["schema"] == projection.STATUS_SCHEMA
    assert status["mode"] == "PORTAL"
    _assert_public(view, say, helped, attended, waited, returned, exited, status)


def test_cli_module_runs_on_pinned_source(tmp_path, pinned):
    env = _pinned.pinned_env()
    root = tmp_path / "subprocess-person"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "s45_projection.cli",
            "--root",
            str(root),
            "--start",
            "view",
        ],
        cwd=str(_pinned.RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stderr
    view = json.loads(completed.stdout)
    assert view["schema"] == projection.VIEW_SCHEMA
    assert view["source"] == "s45"
    assert view["hidden_state_held"] is True
    _assert_public(view)
