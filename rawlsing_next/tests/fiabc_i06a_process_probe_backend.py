"""Hostile-test-only backend for FIABC-W3-I06A process isolation."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"

_SESSIONS: dict[tuple[str, str], dict] = {}
_HEAP: list[bytearray] = []


def _files(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    )


def _child_identity() -> dict:
    code = (
        "import json,os;"
        "print(json.dumps({"
        "'pid':os.getpid(),"
        "'ppid':os.getppid(),"
        "'source':os.environ.get('RAWLSING_EE_P2X_CELL_SOURCE'),"
        "'candidate':os.environ.get('RAWLSING_EE_P2X_CELL_CANDIDATE'),"
        "'cell_key':os.environ.get('RAWLSING_EE_P2X_CELL_KEY'),"
        "'freeze':os.environ.get('RAWLSING_EE_P2X_UPSTREAM_FREEZE_SHA256')"
        "},sort_keys=True))"
    )
    run = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return json.loads(run.stdout.strip())


def run_stage(context, services):
    key = (context.stage.source, context.stage.candidate)
    before = sorted("/".join(k) for k in _SESSIONS)
    payload = {
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "cell_key": "/".join(key),
        "session_keys_before": before,
        "scratch_files_before": _files(context.roots.scratch),
        "durable_files_before": _files(context.roots.durable),
    }

    op = context.stage.stage_id
    if op == "PROBE_SET_SESSION":
        _SESSIONS[key] = {"pid": os.getpid()}
    elif op == "PROBE_ALLOCATE_RSS":
        _HEAP.append(bytearray(8 * 1024 * 1024))
        payload["allocated_bytes"] = len(_HEAP[-1])
    elif op == "PROBE_WRITE_STATE":
        target = context.roots.scratch / f"probe-from-{context.stage.candidate}.txt"
        target.write_text(context.stage.candidate + "\n", encoding="utf-8")
        payload["written"] = target.name
    elif op == "PROBE_LIST_STATE":
        pass
    elif op == "PROBE_SPAWN_CHILD":
        payload["child"] = _child_identity()
    else:
        raise RuntimeError(f"unknown hostile-test probe operation: {op}")

    _SESSIONS.setdefault(key, {"pid": os.getpid()})
    payload.update({
        "session_keys_after": sorted("/".join(k) for k in _SESSIONS),
        "scratch_files_after": _files(context.roots.scratch),
        "durable_files_after": _files(context.roots.durable),
    })
    return {
        "terminal_disposition": "PASS",
        "receipt": {
            "schema": "RAWLSING_FIABC_I06A_PROCESS_PROBE@1.0.0",
            "stage_payload": payload,
        },
        "output_artifacts": {},
        "verifier_complete": True,
    }
