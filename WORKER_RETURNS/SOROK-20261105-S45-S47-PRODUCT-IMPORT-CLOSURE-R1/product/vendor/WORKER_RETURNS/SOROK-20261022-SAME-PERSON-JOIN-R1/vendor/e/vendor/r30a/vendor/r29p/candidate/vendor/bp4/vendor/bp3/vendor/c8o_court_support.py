"""Shared path/staging support for the C8O court. Not a test module."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

COURT = Path(__file__).resolve().parent
RET = COURT.parent
CANDIDATE = RET / "candidate"
CONSUMER = RET / "consumer"
ACCEPTED_STAGE = RET / "runtime" / "stage_out12"
WORKER = COURT / "c8o_worker.py"

for _p in (str(CANDIDATE), str(CONSUMER), str(ACCEPTED_STAGE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

PYTHONPATH = os.pathsep.join([str(CANDIDATE), str(CONSUMER), str(ACCEPTED_STAGE)])


def legacy(label: str = "L") -> dict:
    return {"candidate_id": label, "payload": {"utterance": "Hi"}}


def capability(writer_id: str):
    from c8o_trusted_outbox import WriterCapability

    return WriterCapability(
        writer_id=writer_id,
        capability_token="TOKEN-" + writer_id + "-" + "x" * 24,
        issuer_ref="UNISSUED_NO_TRUSTED_ISSUER",
    )


def spawn(mode: str, d: Path, writers, extra=(), timeout: float = 120.0):
    procs = []
    for w in writers:
        procs.append(
            (
                w,
                subprocess.Popen(
                    [sys.executable, str(WORKER), mode, str(d), w, *extra],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=dict(os.environ, PYTHONPATH=PYTHONPATH),
                ),
            )
        )
    deadline = time.monotonic() + 30.0
    while time.monotonic() < deadline:
        if all((d / f"ready_{w}").exists() for w in writers):
            break
        time.sleep(0.002)
    (d / "go").write_text("go", encoding="utf8")
    rows = []
    for w, p in procs:
        out, err = p.communicate(timeout=timeout)
        rows.append(
            {
                "writer": w,
                "pid": p.pid,
                "rc": p.returncode,
                "out": out.strip(),
                "err": err.strip()[-400:],
            }
        )
    return rows


def cold_reopen(journal_path: Path) -> dict:
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(CANDIDATE)!r});"
        f"sys.path.insert(0,{str(ACCEPTED_STAGE)!r});"
        "from c8o_trusted_outbox import C8OccurrenceJournal;"
        f"j=C8OccurrenceJournal({str(journal_path)!r});"
        "p,v,c=j.recover_custody();"
        "print(json.dumps({'version':v,'count':p.ledger.count(),"
        "'ids':[e['occurrence_id'] for e in p.ledger.events],"
        "'status':c.status,'writer_id':c.writer_id,'receipt_id':c.receipt_id}))"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=dict(os.environ, PYTHONPATH=PYTHONPATH),
    )
    if proc.returncode != 0:
        if "LEGACY_UNVERSIONED_OVERWRITE" in proc.stderr or "LEGACY_WRITER_BYPASS_DETECTED" in proc.stderr:
            from c8o_trusted_outbox import LegacyWriterBypassDetected

            raise LegacyWriterBypassDetected(journal_path)
        if "VERSION_STATE_UNREADABLE" in proc.stderr:
            from c8o_trusted_outbox import VersionStateUnreadable

            raise VersionStateUnreadable(journal_path, "COLD_REOPEN_UNREADABLE")
        raise RuntimeError(f"cold reopen failed rc={proc.returncode}: {proc.stderr[-500:]}")
    return json.loads(proc.stdout.strip().splitlines()[-1])


def evidence_path(name: str) -> Path:
    p = RET / "evidence"
    p.mkdir(parents=True, exist_ok=True)
    return p / name


def write_evidence(name: str, payload) -> Path:
    p = evidence_path(name)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf8")
    return p
