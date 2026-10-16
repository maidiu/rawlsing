#!/usr/bin/env python3
"""OUT11 - REAL two-process reproduction of the inherited two-writer stale-journal loss.
Uses the OUT9 closure's OWN legacy() helper so the admitted candidate is authentic."""
import json, os, subprocess, sys, tempfile, time
STAGE = sys.argv[1]
WORKER = r'''
import sys, os, json, time
sys.path.insert(0, sys.argv[1])
from outbox_prototype import Journal
from test_rto_hostile import legacy          # the closure's own authentic candidate builder
d = sys.argv[2]; w = sys.argv[3]
j = Journal(os.path.join(d, "journal.json"))
snap = j.recover()                            # BOTH processes recover the SAME version
open(os.path.join(d, "ready_"+w), "w").close()
while not os.path.exists(os.path.join(d, "go")):   # real synchronization barrier
    time.sleep(0.002)
ev = snap.ledger.admit(legacy(w))
snap.outbox.emit(ev["occurrence_id"])
j.commit(snap)
print(json.dumps({"writer": w, "committed": True, "occurrence_id": ev["occurrence_id"]}))
'''
d = tempfile.mkdtemp(prefix="out11_"); wf = os.path.join(d, "writer.py"); open(wf, "w").write(WORKER)
env = dict(os.environ, PYTHONPATH=STAGE)
ps = [subprocess.Popen([sys.executable, wf, STAGE, d, w], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env) for w in ("A","B")]
for w in ("A","B"):
    for _ in range(3000):
        if os.path.exists(os.path.join(d,"ready_"+w)): break
        time.sleep(0.002)
open(os.path.join(d, "go"), "w").close()
outs=[]
for p in ps:
    o,e = p.communicate(); outs.append({"rc":p.returncode,"out":o.strip()[:160],"err":e.strip()[-240:]})
sys.path.insert(0, STAGE)
from outbox_prototype import Journal
after = Journal(os.path.join(d,"journal.json")).recover()
n = after.ledger.count(); first = after.ledger.get("OCC-0001")
print(json.dumps({"schema":"OUT11_TWO_PROCESS_REPRO@1",
 "mechanism":"two REAL OS processes, both recover() the same journal version, synchronized barrier, then both commit",
 "processes":outs,"events_after":n,"occurrence_1_candidate_id":(first or {}).get("candidate_id"),
 "EXPECTED_IF_SAFE":2,"LOST_COMMITTED_EVENTS":max(0,2-n),
 "verdict":"TWO_WRITER_STALE_JOURNAL_LOSS_CONFIRMED_AT_PROCESS_LEVEL" if n<2 else "NO_LOSS_OBSERVED_AT_PROCESS_LEVEL"}, indent=1))
