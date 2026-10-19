"""HQ320 OUT13 — independent hostile multiwriter concurrency court.

Real OS processes, real fcntl locks, real fsync, real crash injection.
All event identities come from the ACCEPTED real API (ledger.admit / outbox.emit),
not from anything this court synthesises.

GRAIN: TEST_ONLY sourcefree multiwriter on a LOCAL filesystem.
NOT exactly-once delivery. NOT power-loss durability. NOT ADP019. NOT V3.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAND = HERE / "runtime" / "candidate"
if str(CAND) not in sys.path:
    sys.path.insert(0, str(CAND))

from outbox_prototype import Journal, _canonical, _hash   # noqa: E402 (ACCEPTED, unmodified)
from multiwriter_journal import (                          # noqa: E402
    MultiwriterJournal, StaleJournalConflict, LockTimeoutError,
)

WORKER = HERE / "out13_worker.py"


def tmpdir() -> Path:
    return Path(tempfile.mkdtemp(prefix="out13-"))


def spawn(mode: str, d: Path, writers, timeout=180, release_after=None):
    """Launch genuinely simultaneous OS writers, released by a real barrier."""
    ps = []
    for w in writers:
        ps.append((w, subprocess.Popen(
            [sys.executable, str(WORKER), mode, str(d), w, str(CAND)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=dict(os.environ, PYTHONPATH=str(CAND)))))
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if all((d / f"ready_{w}").exists() for w in writers):
            break
        time.sleep(0.002)
    (d / "go").write_text("go")
    outs = []
    for w, p in ps:
        if release_after is not None:
            try:
                o, e = p.communicate(timeout=release_after)
            except subprocess.TimeoutExpired:
                p.kill()
                o, e = p.communicate()
                outs.append(dict(writer=w, rc="TIMEOUT_KILLED", out=o.strip(), err=e.strip()[-200:]))
                continue
        else:
            o, e = p.communicate(timeout=timeout)
        outs.append(dict(writer=w, rc=p.returncode, out=o.strip(), err=e.strip()[-300:]))
    return outs


def parse(outs):
    rows = []
    for o in outs:
        if o["rc"] != 0:
            rows.append(dict(writer=o["writer"], rc=o["rc"], error=o["err"], admitted=[]))
        else:
            j = json.loads(o["out"].strip().splitlines()[-1])
            j["rc"] = o["rc"]          # real OS exit status of the child process
            rows.append(j)
    return rows


def admitted(rows):
    s = set()
    for r in rows:
        s.update(r.get("admitted") or [])
    return s


def ledger_ids(path: Path) -> set:
    """Read the durable admitted identities back through the ACCEPTED Journal."""
    snap = Journal(path).recover()
    ids = set()
    led = snap.snapshot()["ledger"]
    for e in led:
        ids.add(e.get("occurrence_id") or e.get("event_id"))
    return {i for i in ids if i}


def raw(path: Path) -> dict:
    return json.loads(path.read_text())


def writer_version(path: Path) -> int:
    return int(raw(path).get("writer_version", 0))