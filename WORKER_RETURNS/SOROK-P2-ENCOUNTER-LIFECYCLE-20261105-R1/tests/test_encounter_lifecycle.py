from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from sorok_p2_lifecycle import runtime
from sorok_p2_lifecycle.lifecycle import (
    BLOCKED_CODE,
    RESULT_SCHEMA,
    RETURN_CODE,
    LifecycleEncounter,
    LifecycleRefusal,
    local_state_path,
)

RETURN = Path(__file__).resolve().parents[1]
CLI = RETURN / "run_lifecycle_cli.py"


def _projection():
    runtime.install()
    from s45_projection import projection

    return projection


def _assert_public(*values) -> None:
    for value in values:
        _walk_public(value)


def _walk_public(value, path="<root>") -> None:
    projection = _projection()
    if isinstance(value, dict):
        for key, item in value.items():
            assert key not in projection.PRIVATE_KEYS, path + "." + str(key)
            assert key not in {"root_hash", "root_id"}, path + "." + str(key)
            _walk_public(item, path + "." + str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _walk_public(item, path + "[" + str(index) + "]")
    elif isinstance(value, str):
        for marker in projection.FORBIDDEN_VALUE_MARKERS:
            assert marker not in value, path + " contains " + marker


def _run_cli(*args):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(CLI), *args],
        cwd=str(RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout)


def test_positive_actions_then_exit_cold_reopen_and_return(tmp_path):
    state = tmp_path / "person"
    encounter = LifecycleEncounter.start(state)
    try:
        assert encounter.mode == "PORTAL"
        view = encounter.view()
        said = encounter.say("Can I help?")
        helped = encounter.do_help()
        attended = encounter.attend()
        assert view["schema"] == "SOROK_WP19_ENCOUNTER_VIEW@1"
        assert said["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
        assert said["actor_response"]["strategy"] == "HELP_INVITE"
        assert helped["actor_response"]["strategy"] == "HELP_ACCEPT"
        assert helped["actor_response"]["performed"] is True
        assert attended["status"] == "NO_CHANGE"
        before = encounter.status()["current_store_hash"]
        root_hash = encounter.root_hash
        exited = encounter.exit()
        assert exited["code"] == "LOCAL_EXIT_ONLY"
        assert exited["mode"] == "OUTSIDE"
        assert encounter.mode == "OUTSIDE"
        assert encounter.status()["current_store_hash"] == before
        assert encounter.local_state_path.is_file()
        _assert_public(view, said, helped, attended, exited, encounter.local_state())
    finally:
        encounter.close()

    encounter = LifecycleEncounter.open(state)
    try:
        assert encounter.mode == "OUTSIDE"
        assert encounter.root_hash == root_hash
        before = encounter.status()["current_store_hash"]
        assert encounter.view()["mode"] == "OUTSIDE"
        for control, call in (
            ("SAY", lambda: encounter.say("Can I help?")),
            ("DO_HELP", encounter.do_help),
            ("ATTEND", encounter.attend),
        ):
            blocked = call()
            assert blocked["schema"] == RESULT_SCHEMA
            assert blocked["control"] == control
            assert blocked["status"] == "REFUSED"
            assert blocked["code"] == BLOCKED_CODE
            assert blocked["refusal"] is True
            assert blocked["actor_response"] is None
            assert blocked["world_event_created"] is False
            assert blocked["clock_changed"] is False
            assert blocked["simulated_delivery"] is False
            assert encounter.status()["current_store_hash"] == before
            _assert_public(blocked)
        returned = encounter.return_()
        assert returned["schema"] == RESULT_SCHEMA
        assert returned["code"] == RETURN_CODE
        assert returned["status"] == "OK"
        assert returned["mode"] == "PORTAL"
        assert encounter.mode == "PORTAL"
        assert encounter.status()["current_store_hash"] == before
        _assert_public(returned)
        said_after = encounter.say("Can I help?")
        assert said_after["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
        assert said_after["actor_response"]["strategy"] in {"HELP_INVITE", "HELP_REFUSE"}
    finally:
        encounter.close()

    encounter = LifecycleEncounter.open(state)
    try:
        assert encounter.mode == "PORTAL"
        assert encounter.view()["mode"] == "PORTAL"
    finally:
        encounter.close()


def test_return_inside_preserves_existing_world_hold(tmp_path):
    encounter = LifecycleEncounter.start(tmp_path / "person")
    try:
        result = encounter.return_()
        assert result["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
        assert result["status"] == "HELD"
        assert result["code"] == "RETURN_UNSUPPORTED_TYPED_HOLD"
        assert result["world_event_created"] is False
        assert encounter.mode == "PORTAL"
    finally:
        encounter.close()


def test_another_root_cannot_inherit_persisted_mode(tmp_path):
    root_a = tmp_path / "a"
    root_b = tmp_path / "b"
    a = LifecycleEncounter.start(root_a)
    try:
        a.exit()
        assert a.mode == "OUTSIDE"
        source = a.local_state_path
    finally:
        a.close()
    b = LifecycleEncounter.start(root_b, seed="02" * 32)
    try:
        target = b.local_state_path
    finally:
        b.close()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    with pytest.raises(LifecycleRefusal) as exc:
        LifecycleEncounter.open(root_b)
    assert exc.value.code == "LOCAL_LIFECYCLE_ROOT_MISMATCH"


def test_local_mode_cut_resets_and_restore_recovers_cold(tmp_path):
    state = tmp_path / "person"
    encounter = LifecycleEncounter.start(state)
    try:
        encounter.exit()
        path = encounter.local_state_path
    finally:
        encounter.close()
    backup = path.with_suffix(".restore")
    os.replace(path, backup)
    encounter = LifecycleEncounter.open(state)
    try:
        assert encounter.mode == "PORTAL"
        assert encounter.view()["mode"] == "PORTAL"
    finally:
        encounter.close()
    os.replace(backup, path)
    encounter = LifecycleEncounter.open(state)
    try:
        assert encounter.mode == "OUTSIDE"
        assert encounter.view()["mode"] == "OUTSIDE"
    finally:
        encounter.close()


def test_cli_cold_commands_persist_exit_and_local_return(tmp_path):
    state = tmp_path / "cli-person"
    new = _run_cli("new", "--state", str(state))
    assert new["schema"] == "SOROK_WP19_ENCOUNTER_VIEW@1"
    assert "root_hash" not in json.dumps(new)
    exited = _run_cli("exit", "--state", str(state))
    assert exited["code"] == "LOCAL_EXIT_ONLY"
    withdrawn = _run_cli("view", "--state", str(state))
    assert withdrawn["mode"] == "OUTSIDE"
    status = _run_cli("status", "--state", str(state))
    assert status["mode"] == "OUTSIDE"
    blocked = _run_cli("say", "--state", str(state), "Can I help?")
    assert blocked["schema"] == RESULT_SCHEMA
    assert blocked["code"] == BLOCKED_CODE
    assert blocked["status"] == "REFUSED"
    returned = _run_cli("return", "--state", str(state))
    assert returned["schema"] == RESULT_SCHEMA
    assert returned["code"] == RETURN_CODE
    assert returned["mode"] == "PORTAL"
    said = _run_cli("say", "--state", str(state), "Can I help?")
    assert said["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
    assert said["actor_response"]["strategy"] == "HELP_INVITE"
    lifecycle = _run_cli("lifecycle", "--state", str(state))
    assert lifecycle["mode"] == "PORTAL"
    assert "root_hash" not in json.dumps(lifecycle)
