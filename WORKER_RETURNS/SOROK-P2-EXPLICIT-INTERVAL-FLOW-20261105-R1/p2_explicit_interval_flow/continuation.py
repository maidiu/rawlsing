"""Explicit caller-supplied interval continuation over the shipped S45-S47 CLI."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from .bootstrap import RETURN, install, paths

RESULT_SCHEMA = "SOROK_P2_EXPLICIT_INTERVAL_CONTINUATION@1"
INTERVAL_INPUT_SCHEMA = "SOROK_P2_EXPLICIT_INTERVAL_INPUT@1"
GRADE = "TEST_ONLY_S45_S47_EXPLICIT_INTERVAL_CONTINUATION_NOT_NATIVE"
ALLOWED_MODES = (
    "ACTUAL", "SCHEDULED_ONLY", "DECLINED", "CONSTRAINED", "BLOCKED", "UNKNOWN",
)
HOLD_REASONS = {
    "WAIT": "WAIT_UNSUPPORTED_TYPED_HOLD",
    "ABSENCE": "USER_ABSENCE_LIFE_ADVANCE_MISSING",
}


def _result(*, request: str, status: str, **extra) -> dict:
    body = {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "request": request,
        "status": status,
        "advanced": False,
        "general_autonomous_absence_life": False,
        "interval": None,
        "admission": None,
        "c9": None,
        "view": None,
        "opportunity": None,
        "do_help": None,
        "do_help_executed": False,
        "user_attempt_executed": False,
        "encounter_count_before": None,
        "encounter_count_after": None,
        "encounters_unchanged": None,
        "cold_continuity": None,
    }
    body.update(extra)
    return body


def _env(info: dict) -> dict:
    tmp = Path(os.environ.get("TMPDIR", str(RETURN / "logs" / "tmp")))
    tmp.mkdir(parents=True, exist_ok=True)
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/sbin:/sbin"),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "C"),
        "LC_ALL": os.environ.get("LC_ALL", "C"),
        "TMPDIR": str(tmp),
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOROK_S45_S47_PACKAGE_ROOT": str(info["product"]),
        "SOROK_S45_S47_PROJECTION_ROOT": str(info["projection_return"]),
    }


def _run_cli(info: dict, args: list[str]) -> dict:
    command = [
        sys.executable, "-I", "-B", str(info["product_cli"]), *args,
    ]
    completed = subprocess.run(
        command,
        cwd=str(info["product"]),
        env=_env(info),
        capture_output=True,
        text=True,
        timeout=180,
    )
    payload = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
    return {
        "command": command,
        "returncode": completed.returncode,
        "payload": payload,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _error_code(stderr: str) -> str:
    for line in reversed(stderr.splitlines()):
        if "S46_INTERVAL_CONDITION_REVOKED" in line:
            return "S46_INTERVAL_CONDITION_REVOKED"
        for code in (
            "P2_INVALID_INTERVAL_MODE",
            "S46Refusal",
            "ValueError",
            "RuntimeError",
        ):
            if code in line:
                return code
    return "PRODUCT_CLI_REFUSED"


def _public_interval(report: dict) -> dict:
    interval = report.get("interval") or {}
    return {
        "mode": interval.get("mode"),
        "status": interval.get("status"),
        "coverage": interval.get("coverage"),
        "start": interval.get("start"),
        "end": interval.get("end"),
        "material_after_interval": report.get("material_after_interval"),
        "actual_daily_events_invented": interval.get("actual_daily_events_invented"),
        "actor_knowledge_inferred": interval.get("actor_knowledge_inferred"),
        "psychology_state_written": interval.get("psychology_state_written"),
    }


def _public_c9(report: dict) -> dict:
    c9 = report.get("c9") or {}
    return {
        "objective_material_eligible": c9.get("objective_material_eligible"),
        "target_branch": c9.get("target_branch"),
        "target_reason": c9.get("target_reason"),
        "s47_source_in_readset": c9.get("s47_source_in_readset"),
    }


def _projection(state: Path):
    from s45_projection.adapter import S45Projection
    from s47.session import S47Session

    session = S47Session.open(state)
    return session, S45Projection(session)


def _public_opportunity(view: dict) -> dict:
    return {
        "schema": "SOROK_P2_CONTINUED_PUBLIC_OPPORTUNITY@1",
        "source": view.get("source"),
        "clock": view.get("clock"),
        "location": view.get("location"),
        "visible_event_count": len(view.get("visible_events") or []),
        "encounter_admission": view.get("encounter_admission"),
        "tool_available": view.get("tool_available"),
        "controls": view.get("controls"),
        "return_available": (view.get("return_control") or {}).get("available"),
    }


def apply_explicit_interval(
    state: str | Path,
    interval_input: dict | None,
    *,
    base_root: str | Path | None = None,
) -> dict:
    info = install(base_root)
    if not isinstance(interval_input, dict):
        return _result(
            request="INTERVAL", status="HELD",
            reason="P2_EXPLICIT_INTERVAL_INPUT_MISSING",
        )
    if interval_input.get("schema") not in (None, INTERVAL_INPUT_SCHEMA):
        return _result(
            request="INTERVAL", status="REFUSED",
            reason="P2_INTERVAL_INPUT_SCHEMA_MISMATCH",
        )
    mode = str(interval_input.get("mode") or "").upper()
    if mode not in ALLOWED_MODES:
        return _result(
            request="INTERVAL", status="REFUSED",
            reason="P2_INVALID_INTERVAL_MODE", mode=mode,
        )
    start = interval_input.get("start")
    span = interval_input.get("span", 4)
    if not isinstance(span, int) or isinstance(span, bool) or span <= 0:
        return _result(
            request="INTERVAL", status="REFUSED",
            reason="P2_INVALID_INTERVAL_SPAN", span=span,
        )
    args = ["interval", "--state", str(Path(state).expanduser().resolve()),
            "--mode", mode, "--span", str(span)]
    if start is not None:
        if not isinstance(start, int) or isinstance(start, bool) or start < 0:
            return _result(
                request="INTERVAL", status="REFUSED",
                reason="P2_INVALID_INTERVAL_START", start=start,
            )
        args.extend(["--start", str(start)])
    run = _run_cli(info, args)
    if run["returncode"] != 0 or not isinstance(run["payload"], dict):
        return _result(
            request="INTERVAL", status="REFUSED",
            reason=_error_code(run["stderr"]),
            command=" ".join(run["command"]),
            stderr=run["stderr"][-2000:],
        )
    return {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "request": "INTERVAL",
        "status": "OK",
        "advanced": False,
        "interval": _public_interval(run["payload"]),
        "method": "EXISTING_COMMAND_INTERVAL",
    }


def admit_continuation(
    state: str | Path,
    *,
    request: str = "WAIT",
    base_root: str | Path | None = None,
) -> dict:
    info = install(base_root)
    state = Path(state).expanduser().resolve()
    request = str(request).upper()
    admitted = _run_cli(info, ["admit", "--state", str(state)])
    if admitted["returncode"] != 0 or not isinstance(admitted["payload"], dict):
        return _result(
            request=request, status="REFUSED",
            reason=_error_code(admitted["stderr"]),
            command=" ".join(admitted["command"]),
            stderr=admitted["stderr"][-2000:],
        )
    c9_run = _run_cli(info, ["c9", "--state", str(state)])
    if c9_run["returncode"] != 0 or not isinstance(c9_run["payload"], dict):
        return _result(
            request=request, status="REFUSED",
            reason=_error_code(c9_run["stderr"]),
            command=" ".join(c9_run["command"]),
            stderr=c9_run["stderr"][-2000:],
        )
    session, adapter = _projection(state)
    try:
        encounters_before = len(session.read_encounters())
        view = adapter.view()
        encounters_after = len(session.read_encounters())
    finally:
        adapter.close()
    cold_session, cold_adapter = _projection(state)
    try:
        cold_view = cold_adapter.view()
        cold_encounters = len(cold_session.read_encounters())
    finally:
        cold_adapter.close()
    return _result(
        request=request,
        status="CONTINUED",
        advanced=True,
        interval=None,
        admission={"status": admitted["payload"].get("status")},
        c9=_public_c9(c9_run["payload"]),
        view=view,
        opportunity=_public_opportunity(view),
        do_help=None,
        do_help_executed=False,
        user_attempt_executed=False,
        encounter_count_before=encounters_before,
        encounter_count_after=encounters_after,
        encounters_unchanged=(
            encounters_before == encounters_after == cold_encounters
        ),
        cold_continuity=cold_view == view,
        method="EXISTING_COMMAND_ADMIT_PLUS_PUBLIC_OBSERVATION",
    )




def explicit_do_help(
    state: str | Path,
    *,
    request: str = "WAIT",
    base_root: str | Path | None = None,
) -> dict:
    """Execute a user DO_HELP only when the caller explicitly requests it."""
    install(base_root)
    state = Path(state).expanduser().resolve()
    request = str(request).upper()
    session, adapter = _projection(state)
    try:
        encounters_before = len(session.read_encounters())
        helped = adapter.do_help()
        view = adapter.view()
        encounters_after = len(session.read_encounters())
    finally:
        adapter.close()
    cold_session, cold_adapter = _projection(state)
    try:
        cold_view = cold_adapter.view()
        cold_encounters = len(cold_session.read_encounters())
    finally:
        cold_adapter.close()
    return _result(
        request=request,
        status="DO_HELP_EXECUTED",
        advanced=False,
        view=view,
        opportunity=_public_opportunity(view),
        do_help=helped,
        do_help_executed=True,
        user_attempt_executed=True,
        encounter_count_before=encounters_before,
        encounter_count_after=encounters_after,
        encounters_unchanged=(
            encounters_before == encounters_after == cold_encounters
        ),
        cold_continuity=cold_view == view,
        method="EXPLICIT_USER_DO_HELP",
    )


def continue_after_request(
    state: str | Path,
    *,
    request: str = "WAIT",
    interval_input: dict | None = None,
    base_root: str | Path | None = None,
) -> dict:
    request = str(request).upper()
    if request not in HOLD_REASONS:
        return _result(
            request=request, status="REFUSED",
            reason="P2_UNSUPPORTED_REQUEST_CONTROL",
        )
    if not isinstance(interval_input, dict) or not interval_input.get("mode"):
        return _result(
            request=request,
            status="HELD",
            reason=HOLD_REASONS[request],
            note=(
                "A WAIT/ABSENCE request alone does not select or perform "
                "independent interval activity."
            ),
        )
    interval = apply_explicit_interval(
        state, interval_input, base_root=base_root
    )
    if interval["status"] != "OK":
        interval["request"] = request
        return interval
    continuation = admit_continuation(
        state, request=request, base_root=base_root
    )
    continuation["interval"] = interval["interval"]
    continuation["method"] = (
        "EXISTING_COMMAND_INTERVAL_ADMIT_PLUS_PUBLIC_PROJECTION"
    )
    return continuation


__all__ = [
    "ALLOWED_MODES",
    "GRADE",
    "HOLD_REASONS",
    "INTERVAL_INPUT_SCHEMA",
    "RESULT_SCHEMA",
    "admit_continuation",
    "apply_explicit_interval",
    "continue_after_request",
    "explicit_do_help",
]
