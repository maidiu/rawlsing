"""OUT13 real child writer process.

Uses the ACCEPTED real API surface (make_prototype / ledger.admit / outbox.emit /
Journal.commit) so identities are genuine, not synthesised by this court.

Usage: out13_worker.py <mode:cas|base> <dir> <writer> <syspath>
Barrier files make the writers genuinely simultaneous.
"""
import json
import os
import sys
import time

mode, d, w, syspath = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
sys.path.insert(0, syspath)

from outbox_prototype import Journal, make_prototype          # noqa: E402
from test_rto_hostile import legacy                          # noqa: E402

if mode == "cas":
    from multiwriter_journal import MultiwriterJournal as J, StaleJournalConflict
else:
    J = Journal
    StaleJournalConflict = None


def barrier(tag):
    open(os.path.join(d, "ready_" + tag), "w").close()
    while not os.path.exists(os.path.join(d, "go")):
        time.sleep(0.002)


j = J(os.path.join(d, "journal.json"))
out = {"writer": w, "pid": os.getpid(), "admitted": [], "conflicts": 0,
       "retries": 0, "committed": None}

if mode == "cas":
    barrier(w)
    while True:
        snap, ver = j.recover()
        try:
            ev = snap.ledger.admit(legacy(w + str(len(out["admitted"]))))
            occ = snap.outbox.emit(ev["occurrence_id"])
            newv = j.commit(snap, ver)
            out["admitted"].append(ev["occurrence_id"])
            out["committed"] = newv
            break
        except StaleJournalConflict as c:
            out["conflicts"] += 1
            out["retries"] += 1
            time.sleep(0.002)
else:
    snap = j.recover()
    barrier(w)
    ev = snap.ledger.admit(legacy(w))
    occ = snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap)
    out["admitted"].append(ev["occurrence_id"])
    out["committed"] = "last-writer-wins"

print(json.dumps(out))