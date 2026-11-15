"""Readiness lock helpers for coordinating V550 shard launches."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from data.ddm_build_copy.ddm_v550_storage import atomic_write_json


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except Exception:
        return False
    return True


def readiness_lock_path(readiness_root: Path, shard_id: str) -> Path:
    return readiness_root / shard_id / "readiness.lock"


def claim_readiness_lock(
    readiness_root: Path,
    *,
    run_id: str,
    shard_id: str,
    source: str,
    wave: str,
) -> Path:
    lock_path = readiness_lock_path(readiness_root, shard_id)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        lock_path,
        {
            "run_id": run_id,
            "shard_id": shard_id,
            "source": source,
            "wave": wave,
            "pid": os.getpid(),
            "status": "running",
        },
    )
    return lock_path


def release_readiness_lock(lock_path: Path) -> None:
    try:
        if lock_path.exists():
            lock_path.unlink()
    except Exception:
        pass


def active_readiness_lock_for_shard(readiness_root: Path, shard_id: str) -> Path | None:
    if not readiness_root.exists():
        return None
    for run_dir in readiness_root.iterdir():
        if not run_dir.is_dir():
            continue
        candidate = run_dir / shard_id / "readiness.lock"
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            payload = {}
        pid = payload.get("pid")
        try:
            pid_int = int(pid)
        except Exception:
            pid_int = -1
        if pid_int > 0 and _pid_alive(pid_int):
            return candidate
        release_readiness_lock(candidate)
    return None

