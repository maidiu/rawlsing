"""C8O court OS-process worker: genuine simultaneous writers behind a file barrier.

Modes:
  cas      cooperating C8OccurrenceJournal writer (lock + sealed CAS)
  legacy   accepted Journal.commit bypass writer (no lock, no version)
  rollback writer that replaces the journal with an earlier valid receipt
  forge    writer that recomputes unkeyed digests over mutated fields
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "candidate"))

from c8o_court_support import capability, legacy  # noqa: E402

mode = sys.argv[1]
d = Path(sys.argv[2])
w = sys.argv[3]
extra = sys.argv[4:]

from c8o_trusted_outbox import (  # noqa: E402
    C8OccurrenceJournal,
    StaleJournalConflict,
    forged_receipt,
)
from outbox_prototype import Journal, make_prototype  # noqa: E402


def barrier(tag: str) -> None:
    (d / f"ready_{tag}").write_text("ready", encoding="utf8")
    while not (d / "go").exists():
        time.sleep(0.002)


journal_path = d / "journal.json"
out: dict = {"writer": w, "pid": os.getpid(), "mode": mode, "attempts": []}

if mode == "cas":
    j = C8OccurrenceJournal(journal_path)
    barrier(w)
    while True:
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy(w))
        if ev is None:
            out["attempts"].append({"refused": snap.ledger.last_refusal})
            break
        snap.outbox.emit(ev["occurrence_id"])
        try:
            receipt = j.commit(snap, ver, capability=capability(w))
            out["attempts"].append({"recovered": ver, "committed": receipt.writer_version,
                                   "receipt_id": receipt.receipt_id,
                                   "acknowledged": receipt.acknowledged_occurrence_ids})
            break
        except StaleJournalConflict as c:
            out["attempts"].append({"conflict": {"expected": c.expected, "actual": c.actual}})
            time.sleep(0.002)
elif mode == "legacy":
    variant = extra[0] if extra else "fresh_wipe"
    barrier(w)
    if variant == "fresh_wipe":
        p = make_prototype()
    else:
        p = Journal(journal_path).recover()
    ev = p.ledger.admit(legacy(w))
    if ev is not None:
        p.outbox.emit(ev["occurrence_id"])
    Journal(journal_path).commit(p)
    out["attempts"].append({"legacy_commit": True, "variant": variant, "admitted": ev is not None})
elif mode == "rollback":
    snapshot = Path(extra[0])
    barrier(w)
    journal_path.write_bytes(snapshot.read_bytes())
    out["attempts"].append({"rolled_back_to_bytes": len(snapshot.read_bytes())})
elif mode == "forge":
    field_name = extra[0]
    value = extra[1]
    barrier(w)
    receipt = json.loads(journal_path.read_text(encoding="utf8"))
    overrides = {field_name: json.loads(value)}
    journal_path.write_text(forged_receipt(receipt, **overrides), encoding="utf8")
    out["attempts"].append({"forged": field_name, "value": value})
elif mode == "crash":
    boundary = extra[0]
    j = C8OccurrenceJournal(journal_path)
    barrier(w)
    snap, ver = j.recover()
    ev = snap.ledger.admit(legacy(w))
    if ev is not None:
        snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, ver, capability=capability(w), crash_boundary=boundary)
    out["attempts"].append({"unreachable": boundary})
else:
    raise SystemExit("UNKNOWN_MODE")

print(json.dumps(out))
