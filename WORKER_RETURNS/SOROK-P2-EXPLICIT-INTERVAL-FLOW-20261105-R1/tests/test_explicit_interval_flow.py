"""Focused explicit interval continuation tests."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from p2_explicit_interval_flow.bootstrap import install, paths
from p2_explicit_interval_flow.continuation import (
    admit_continuation,
    apply_explicit_interval,
    continue_after_request,
)

REPO = Path(__file__).resolve().parents[3]
DEFAULT_BASE = REPO / ".local-logs" / "p2-explicit-interval-flow" / "base"


@pytest.fixture(scope="session")
def base_root() -> Path:
    return Path(os.environ.get("SOROK_P2_BASE_ROOT", str(DEFAULT_BASE)))


@pytest.fixture()
def state(tmp_path, base_root) -> Path:
    info = install(base_root)
    target = tmp_path / "state"
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/sbin:/sbin"),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "C"),
        "LC_ALL": os.environ.get("LC_ALL", "C"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOROK_S45_S47_PACKAGE_ROOT": str(info["product"]),
        "SOROK_S45_S47_PROJECTION_ROOT": str(info["projection_return"]),
    }
    run = subprocess.run(
        [sys.executable, "-I", "-B", str(info["product_cli"]),
         "new", "--state", str(target)],
        cwd=str(info["product"]), env=env, capture_output=True, text=True,
    )
    assert run.returncode == 0, run.stderr
    return target


def _identity(state: Path) -> tuple:
    from s47.session import S47Session

    session = S47Session.open(state)
    try:
        return (session.clock(), len(session.world().events),
                len(session.read_events()), session.verify().get("ok"))
    finally:
        session.close()


def test_wait_and_absence_without_interval_remain_typed_holds(state):
    for request, reason in (
        ("WAIT", "WAIT_UNSUPPORTED_TYPED_HOLD"),
        ("ABSENCE", "USER_ABSENCE_LIFE_ADVANCE_MISSING"),
    ):
        before = _identity(state)
        result = continue_after_request(state, request=request)
        after = _identity(state)
        assert result["status"] == "HELD"
        assert result["advanced"] is False
        assert result["reason"] == reason
        assert result["general_autonomous_absence_life"] is False
        assert before == after


def test_invalid_or_missing_mode_is_not_forced_to_actual(state):
    before = _identity(state)
    for interval in ({}, {"mode": "ACTUAL_PLEASE"}, {"mode": "FORCED_ACTUAL"}):
        result = continue_after_request(
            state, request="WAIT", interval_input=interval
        )
        assert result["status"] in {"HELD", "REFUSED"}
        assert result["advanced"] is False
    assert _identity(state) == before


def test_actual_interval_changes_material_and_refuses_do_help(state):
    result = continue_after_request(
        state, request="WAIT",
        interval_input={"mode": "ACTUAL", "span": 4},
    )
    assert result["status"] == "CONTINUED"
    assert result["interval"]["status"] == "PARTIAL"
    assert result["interval"]["material_after_interval"] == 0
    assert result["interval"]["actual_daily_events_invented"] == 0
    assert result["c9"]["objective_material_eligible"] is False
    assert result["c9"]["s47_source_in_readset"] is True
    assert result["do_help"]["status"] == "REFUSED"
    assert result["do_help"]["actor_response"]["strategy"] == "HELP_REFUSE"
    assert result["cold_continuity"] is True
    assert result["general_autonomous_absence_life"] is False


def test_scheduled_only_preserves_material_and_accepts_do_help(state):
    result = continue_after_request(
        state, request="ABSENCE",
        interval_input={"mode": "SCHEDULED_ONLY", "span": 4},
    )
    assert result["status"] == "CONTINUED"
    assert result["interval"]["status"] == "NOT_PERFORMED"
    assert result["interval"]["material_after_interval"] == 1
    assert result["interval"]["actual_daily_events_invented"] == 0
    assert result["c9"]["objective_material_eligible"] is True
    assert result["do_help"]["status"] == "OK"
    assert result["do_help"]["actor_response"]["strategy"] == "HELP_ACCEPT"
    assert result["cold_continuity"] is True


def test_unknown_mode_preserves_unknown_without_material_invention(state):
    result = continue_after_request(
        state, request="WAIT",
        interval_input={"mode": "UNKNOWN", "span": 2},
    )
    assert result["status"] == "CONTINUED"
    assert result["interval"]["status"] == "UNKNOWN"
    assert result["interval"]["material_after_interval"] == 1
    assert result["interval"]["actor_knowledge_inferred"] is False


def test_dependency_cut_refuses_then_restore_continues(state, base_root):
    interval = apply_explicit_interval(
        state, {"mode": "ACTUAL", "span": 4}, base_root=base_root
    )
    assert interval["status"] == "OK"
    from s47.session import S47Session

    session = S47Session.open(state)
    try:
        current = [
            row for row in session.read_interval_states()
            if row.get("currentness") == "CURRENT"
        ]
        assert current
        session.revoke_interval_condition(
            current[-1]["state_id"], reason="TEST_ONLY_CUT"
        )
    finally:
        session.close()
    cut = admit_continuation(state, request="WAIT", base_root=base_root)
    assert cut["status"] == "REFUSED"
    assert "S46_INTERVAL_CONDITION_REVOKED" in cut["reason"]
    session = S47Session.open(state)
    try:
        current = [
            row for row in session.read_interval_states()
            if row.get("currentness") == "CURRENT"
        ]
        session.restore_interval_condition(
            current[-1]["state_id"], reason="TEST_ONLY_RESTORE"
        )
    finally:
        session.close()
    restored = admit_continuation(state, request="WAIT", base_root=base_root)
    assert restored["status"] == "CONTINUED"
    assert restored["c9"]["objective_material_eligible"] is False
    assert restored["do_help"]["actor_response"]["strategy"] == "HELP_REFUSE"
    assert restored["cold_continuity"] is True
