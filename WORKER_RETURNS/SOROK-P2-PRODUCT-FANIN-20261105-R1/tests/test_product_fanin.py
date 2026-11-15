from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
from pathlib import Path

from p2_product_fanin import runtime
from p2_product_fanin.integration import (
    OPPORTUNITY_SCHEMA,
    P2ProductFanin,
    apply_explicit_interval,
)

RETURN = Path(__file__).resolve().parents[1]
CLI = RETURN / "run_fanin_cli.py"


def _projection():
    runtime.load()
    from s45_projection import projection

    return projection


def _assert_public(*values) -> None:
    projection = _projection()

    def walk(value, path="<root>") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                assert key not in projection.PRIVATE_KEYS, path + "." + str(key)
                assert key not in {"root_hash", "root_id"}, path + "." + str(key)
                walk(item, path + "." + str(key))
        elif isinstance(value, (list, tuple)):
            for index, item in enumerate(value):
                walk(item, path + "[" + str(index) + "]")
        elif isinstance(value, str):
            for marker in projection.FORBIDDEN_VALUE_MARKERS:
                assert marker not in value, path + " contains " + marker

    for value in values:
        walk(value)


def _run_cli(*args):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(CLI), *args],
        cwd=str(RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout)


def test_imported_interval_repair_source_is_loaded_and_observation_only():
    deps = runtime.load()
    from p2_explicit_interval_flow import continuation as interval_continuation

    path = Path(interval_continuation.__file__).resolve()
    assert path.is_relative_to(runtime.INTERVAL_RETURN.resolve())
    assert deps["interval_apply"].__module__ == "p2_explicit_interval_flow.continuation"
    assert callable(interval_continuation.explicit_do_help)
    observation = inspect.getsource(interval_continuation.admit_continuation)
    explicit = inspect.getsource(interval_continuation.explicit_do_help)
    assert "adapter.do_help()" not in observation
    assert "adapter.do_help()" in explicit
    assert "explicit_do_help" in interval_continuation.__all__



def test_actual_interval_later_observation_then_explicit_attempt(tmp_path):
    state = tmp_path / "actual"
    fanin = P2ProductFanin.start(state)
    root_hash = fanin.root_hash
    fanin.close()

    interval = apply_explicit_interval(state, {"mode": "ACTUAL", "span": 4})
    assert interval["status"] == "OK", interval
    assert interval["interval"]["status"] in {"PARTIAL", "REALIZED"}
    assert interval["interval"]["material_after_interval"] == 0
    assert interval["do_help_executed"] is False

    fanin = P2ProductFanin.open(state)
    try:
        assert fanin.root_hash == root_hash
        root_event = fanin.session.read_events()[0]["e1_event_id"]
        encounters_before = len(fanin.session.read_encounters())
        admitted = fanin.admit_later_event((root_event,))
        assert admitted["status"] == "OK", admitted
        assert admitted["performed"] is True
        assert admitted["c9"]["s47_source_in_readset"] is True
        assert admitted["c9"]["objective_material_eligible"] is False
        assert admitted["s43"]["language_status"] == "ACCEPTED"
        assert admitted["s43"]["repertoire_hash"]
        assert len(fanin.session.read_encounters()) == encounters_before

        opportunity = fanin.public_opportunity(admitted)
        assert opportunity["schema"] == OPPORTUNITY_SCHEMA
        assert opportunity["do_help_executed"] is False
        assert opportunity["user_attempt"] is False
        assert opportunity["c9_material_eligible"] is False
        assert opportunity["event_status"] == "OK"
        _assert_public(opportunity, fanin.view(), fanin.local_state(), fanin.verify_public())

        helped = fanin.do_help()
        assert helped["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
        assert helped["attempted"] is True
        assert helped["performed"] is False
        assert helped["status"] == "REFUSED"
        assert helped["refusal"] is True
        assert helped["actor_response"]["strategy"] == "HELP_REFUSE"
        assert helped["actor_response"]["performed"] is False
        assert len(fanin.session.read_encounters()) == encounters_before + 1

        world_events_before = len(fanin.session.events())
        clock_before = fanin.session.clock()
        attended = fanin.attend()
        assert attended["status"] == "NO_CHANGE"
        assert attended["world_event_created"] is False
        assert attended["clock_changed"] is False
        assert attended["performed"] is False
        assert len(fanin.session.events()) == world_events_before
        assert fanin.session.clock() == clock_before
        _assert_public(helped, attended, fanin.view(), fanin.status())
        event_ref = admitted["event_ref"]
    finally:
        fanin.close()

    cold = P2ProductFanin.open(state)
    try:
        assert cold.root_hash == root_hash
        read = cold.read_later_event(event_ref)
        assert read["c9"]["s47_source_hash"] == admitted["c9"]["s47_source_hash"]
        assert read["s43"]["language_status"] == "ACCEPTED"
        assert cold.verify_public()["ok"] is True
    finally:
        cold.close()


def test_scheduled_control_reads_opportunity_before_explicit_help(tmp_path):
    state = tmp_path / "scheduled"
    fanin = P2ProductFanin.start(state)
    root_hash = fanin.root_hash
    fanin.close()
    interval = apply_explicit_interval(state, {"mode": "SCHEDULED_ONLY", "span": 4})
    assert interval["status"] == "OK", interval
    assert interval["interval"]["status"] == "NOT_PERFORMED"
    assert interval["interval"]["material_after_interval"] == 1

    fanin = P2ProductFanin.open(state)
    try:
        assert fanin.root_hash == root_hash
        root_event = fanin.session.read_events()[0]["e1_event_id"]
        encounters_before = len(fanin.session.read_encounters())
        admitted = fanin.admit_later_event((root_event,))
        assert admitted["status"] == "OK", admitted
        assert admitted["c9"]["objective_material_eligible"] is True
        assert len(fanin.session.read_encounters()) == encounters_before
        opportunity = fanin.public_opportunity(admitted)
        assert opportunity["c9_material_eligible"] is True
        assert opportunity["do_help_executed"] is False
        helped = fanin.do_help()
        assert helped["status"] == "OK"
        assert helped["attempted"] is True
        assert helped["performed"] is False
        assert helped["actor_response"]["strategy"] == "HELP_ACCEPT"
        assert helped["actor_response"]["performed"] is True
        assert len(fanin.session.read_encounters()) == encounters_before + 1
    finally:
        fanin.close()


def test_outside_blocks_encounter_actions_and_local_return_does_not_mutate(tmp_path):
    state = tmp_path / "outside"
    fanin = P2ProductFanin.start(state)
    try:
        store_before = fanin.status()["current_store_hash"]
        clock_before = fanin.session.clock()
        events_before = len(fanin.session.read_events())
        exited = fanin.exit()
        assert exited["code"] == "LOCAL_EXIT_ONLY"
        assert exited["mode"] == "OUTSIDE"
        assert fanin.status()["current_store_hash"] == store_before
    finally:
        fanin.close()

    fanin = P2ProductFanin.open(state)
    try:
        assert fanin.local_mode == "OUTSIDE"
        assert fanin.view()["mode"] == "OUTSIDE"
        for control, call in (
            ("SAY", lambda: fanin.say("Can I help?")),
            ("DO_HELP", fanin.do_help),
            ("ATTEND", fanin.attend),
        ):
            blocked = call()
            assert blocked["control"] == control
            assert blocked["code"] == "LOCAL_OUTSIDE_MODE_BLOCKED"
            assert blocked["status"] == "REFUSED"
            assert blocked["actor_response"] is None
            assert blocked["world_event_created"] is False
            assert blocked["clock_changed"] is False
            assert fanin.status()["current_store_hash"] == store_before
            assert fanin.session.clock() == clock_before
            assert len(fanin.session.read_events()) == events_before
        returned = fanin.return_()
        assert returned["code"] == "LOCAL_RETURN_ONLY"
        assert returned["mode"] == "PORTAL"
        assert fanin.status()["current_store_hash"] == store_before
        assert fanin.session.clock() == clock_before
        assert len(fanin.session.read_events()) == events_before
        assert fanin.do_help()["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
    finally:
        fanin.close()


def test_interval_cut_refuses_later_event_then_restore_continues_cold(tmp_path):
    state = tmp_path / "cut"
    fanin = P2ProductFanin.start(state)
    fanin.close()
    interval = apply_explicit_interval(state, {"mode": "ACTUAL", "span": 4})
    assert interval["status"] == "OK", interval

    fanin = P2ProductFanin.open(state)
    try:
        root_hash = fanin.root_hash
        current = fanin.current_interval_state()
        assert current is not None
        state_id = current["state_id"]
        root_event = fanin.session.read_events()[0]["e1_event_id"]
        events_before = len(fanin.session.read_events())
        fanin.revoke_interval(state_id, reason="TEST_ONLY_FANIN_CUT")
        refused = fanin.admit_later_event((root_event,))
        assert refused["status"] == "REFUSED"
        assert refused["code"] == "S46_INTERVAL_CONDITION_REVOKED"
        assert len(fanin.session.read_events()) == events_before
        fanin.restore_interval(state_id, reason="TEST_ONLY_FANIN_RESTORE")
        admitted = fanin.admit_later_event((root_event,))
        assert admitted["status"] == "OK", admitted
        assert admitted["c9"]["s47_source_in_readset"] is True
        assert admitted["c9"]["objective_material_eligible"] is False
        event_ref = admitted["event_ref"]
        source_hash = admitted["c9"]["s47_source_hash"]
    finally:
        fanin.close()

    cold = P2ProductFanin.open(state)
    try:
        assert cold.root_hash == root_hash
        read = cold.read_later_event(event_ref)
        assert read["c9"]["s47_source_hash"] == source_hash
        assert cold.verify_public()["ok"] is True
    finally:
        cold.close()


def test_unknown_and_invalid_interval_are_explicit(tmp_path):
    state = tmp_path / "unknown"
    fanin = P2ProductFanin.start(state)
    try:
        said = fanin.say("What is the weather?")
        assert said["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
        assert said["status"] == "UNKNOWN"
        assert said["actor_response"] is None
        _assert_public(said, fanin.view())
    finally:
        fanin.close()
    missing = apply_explicit_interval(state, None)
    assert missing["status"] == "HELD"
    assert missing["advanced"] is False
    invalid = apply_explicit_interval(state, {"mode": "NOT_A_MODE", "span": 4})
    assert invalid["status"] == "REFUSED"
    assert invalid["reason"] == "P2_INVALID_INTERVAL_MODE"
    assert invalid["advanced"] is False
    assert invalid["do_help_executed"] is False


def test_cold_cli_sequence_observation_before_attempt(tmp_path):
    state = tmp_path / "cli"
    new = _run_cli("new", "--state", str(state))
    assert new["schema"] == "SOROK_WP19_ENCOUNTER_VIEW@1"
    assert "root_hash" not in json.dumps(new)

    interval = _run_cli(
        "interval", "--state", str(state), "--mode", "ACTUAL", "--span", "4"
    )
    assert interval["status"] == "OK", interval
    assert interval["interval"]["material_after_interval"] == 0
    assert interval["local_mode"] == "PORTAL"
    assert interval["do_help_executed"] is False

    later = _run_cli("later-event", "--state", str(state))
    assert later["schema"] == OPPORTUNITY_SCHEMA
    assert later["event_status"] == "OK"
    assert later["c9_material_eligible"] is False
    assert later["do_help_executed"] is False
    assert later["user_attempt"] is False
    assert "root_hash" not in json.dumps(later)

    fanin = P2ProductFanin.open(state)
    try:
        later_event_ref = fanin.session.read_events()[-1]["e1_event_id"]
        encounters_before_opportunity = len(fanin.session.read_encounters())
    finally:
        fanin.close()
    opportunity = _run_cli(
        "opportunity", "--state", str(state), "--event-ref", later_event_ref
    )
    assert opportunity["schema"] == OPPORTUNITY_SCHEMA
    assert opportunity["event_status"] == "OK"
    assert opportunity["do_help_executed"] is False
    assert opportunity["user_attempt"] is False
    fanin = P2ProductFanin.open(state)
    try:
        assert len(fanin.session.read_encounters()) == encounters_before_opportunity
    finally:
        fanin.close()

    helped = _run_cli("do-help", "--state", str(state))
    assert helped["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
    assert helped["status"] == "REFUSED"
    assert helped["attempted"] is True
    assert helped["performed"] is False
    assert helped["actor_response"]["strategy"] == "HELP_REFUSE"

    attended = _run_cli("attend", "--state", str(state))
    assert attended["status"] == "NO_CHANGE"
    assert attended["world_event_created"] is False

    exited = _run_cli("exit", "--state", str(state))
    assert exited["code"] == "LOCAL_EXIT_ONLY"
    blocked = _run_cli("say", "--state", str(state), "Can I help?")
    assert blocked["code"] == "LOCAL_OUTSIDE_MODE_BLOCKED"
    returned = _run_cli("return", "--state", str(state))
    assert returned["code"] == "LOCAL_RETURN_ONLY"
    assert returned["mode"] == "PORTAL"
    said = _run_cli("say", "--state", str(state), "Can I help?")
    assert said["schema"] == "SOROK_WP19_INTERACTION_RESULT@1"
    status = _run_cli("status", "--state", str(state))
    assert status["mode"] == "PORTAL"
    assert "root_hash" not in json.dumps(status)
