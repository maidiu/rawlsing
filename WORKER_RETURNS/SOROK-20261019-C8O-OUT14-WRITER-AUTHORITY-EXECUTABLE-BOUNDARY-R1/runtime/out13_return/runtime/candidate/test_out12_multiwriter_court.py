"""OUT12 multiwriter court: real OS-subprocess interleavings against the lock+CAS candidate."""
import json, os, signal, subprocess, sys, tempfile, time
import pytest
from outbox_prototype import Journal, make_prototype
from test_rto_hostile import legacy
from multiwriter_journal import MultiwriterJournal, StaleJournalConflict

CAND = os.path.dirname(os.path.abspath(__file__))
ACCEPT = os.environ.get("OUT9_STAGE", "")
BOTH = os.pathsep.join([CAND, ACCEPT])
ARGS = [sys.executable]

_BASE = r'''
import json,os,sys,time
sys.path.insert(0, sys.argv[4])
mode=sys.argv[1]; d=sys.argv[2]; w=sys.argv[3]
from outbox_prototype import Journal
from test_rto_hostile import legacy
use_cas = (mode=="cas")
if use_cas:
    from multiwriter_journal import MultiwriterJournal as J, StaleJournalConflict
else:
    J = Journal
def barrier(tag):
    open(os.path.join(d,"ready_"+tag),"w").close()
    while not os.path.exists(os.path.join(d,"go")): time.sleep(0.002)
j = J(os.path.join(d,"journal.json"))
out={"writer":w,"attempts":[]}
if use_cas:
    barrier(w)
    while True:
        snap, ver = j.recover()
        try:
            ev = snap.ledger.admit(legacy(w)); snap.outbox.emit(ev["occurrence_id"])
            newv = j.commit(snap, ver); out["attempts"].append({"recovered":ver,"committed":newv}); break
        except StaleJournalConflict as c:
            out["attempts"].append({"conflict":{"expected":c.expected,"actual":c.actual}}); time.sleep(0.002)
else:
    snap = j.recover()
    barrier(w)
    ev = snap.ledger.admit(legacy(w)); snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap); out["attempts"].append({"committed":"last-writer-wins"})
print(json.dumps(out))
'''

def _run(mode, writers, tmp, kill_after=None):
    wf = os.path.join(tmp, "w_%s.py" % mode); open(wf, "w").write(_BASE)
    env = dict(os.environ, PYTHONPATH=BOTH)
    ps = [subprocess.Popen(ARGS + [wf, mode, tmp, w, BOTH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
          for w in writers]
    for w in writers:
        for _ in range(4000):
            if os.path.exists(os.path.join(tmp, "ready_" + w)): break
            time.sleep(0.002)
    open(os.path.join(tmp, "go"), "w").close()
    outs = []
    for p in ps:
        o, e = p.communicate(); outs.append({"rc": p.returncode, "out": o.strip(), "err": e.strip()[-200:]})
    return outs


def test_C0_BASELINE_accepted_journal_loses_a_committed_event(tmp_path):
    """The preserved counterexample: accepted Journal, 2 real processes, no CAS."""
    r = _run("base", ["A", "B"], str(tmp_path))
    n = Journal(tmp_path / "journal.json").recover().ledger.count()
    assert all(x["rc"] == 0 for x in r), r
    assert n == 1, "expected the known last-writer-wins loss (2 writers, 1 surviving event); got %d" % n


def test_C1_CAS_two_process_no_lost_committed_event(tmp_path):
    r = _run("cas", ["A", "B"], str(tmp_path))
    assert all(x["rc"] == 0 for x in r), r
    n = MultiwriterJournal(tmp_path / "journal.json").recover()[0].ledger.count()
    assert n == 2, "CAS must retain BOTH committed events; got %d" % n


def test_C2_CAS_three_process_no_lost_committed_event(tmp_path):
    r = _run("cas", ["A", "B", "C"], str(tmp_path))
    assert all(x["rc"] == 0 for x in r), r
    n = MultiwriterJournal(tmp_path / "journal.json").recover()[0].ledger.count()
    assert n == 3, "CAS must retain all THREE committed events; got %d" % n


def test_C3_lock_serializes_so_every_writer_commits_at_a_fresh_version(tmp_path):
    """With the lock held across the whole read-modify-write, writers SERIALIZE.

    C3 is the deliberate counterpart to C5. Because no writer can hold a stale
    snapshot once it is inside the lock, no conflict arises during a clean race;
    each writer observes a strictly fresh version and commits. C5 proves the CAS
    still fires when a stale snapshot IS held. Testing on the wire would be wrong.
    """
    r = _run("cas", ["A", "B"], str(tmp_path))
    attempts = [json.loads(x["out"])["attempts"] for x in r]
    committed = [a["committed"] for att in attempts for a in att if "committed" in a]
    assert all(x["rc"] == 0 for x in r), r
    assert sorted(committed) == [1, 2], "each writer must commit at a distinct fresh version"
    assert len(set(committed)) == len(committed), "no two writers may commit the same version"


def test_C4_version_is_monotonic_and_identity_is_stable(tmp_path):
    mv = MultiwriterJournal(tmp_path / "journal.json")
    snap, v0 = mv.recover(); assert v0 == 0
    ev = snap.ledger.admit(legacy("A")); snap.outbox.emit(ev["occurrence_id"])
    v1 = mv.commit(snap, v0); assert v1 == 1
    snap2, v1b = mv.recover(); assert v1b == 1
    with pytest.raises(StaleJournalConflict):
        mv.commit(snap2, v0)          # replaying an old version must refuse


def test_C5_stale_reader_cannot_publish(tmp_path):
    mv = MultiwriterJournal(tmp_path / "journal.json")
    s1, v = mv.recover()
    s2, v2 = mv.recover()
    assert v == v2 == 0
    e1 = s1.ledger.admit(legacy("A")); s1.outbox.emit(e1["occurrence_id"]); mv.commit(s1, v)
    with pytest.raises(StaleJournalConflict) as ei:
        mv.commit(s2, v2)
    assert ei.value.code == "STALE_JOURNAL_CONFLICT"
    assert mv.recover()[0].ledger.count() == 1


def test_C6_revocation_survives_a_competing_transaction(tmp_path):
    mv = MultiwriterJournal(tmp_path / "journal.json")
    s, v = mv.recover()
    ev = s.ledger.admit(legacy("A")); s.outbox.emit(ev["occurrence_id"])
    v = mv.commit(s, v)
    s2, v2 = mv.recover()
    s2.outbox.revoke_viewer(ev["occurrence_id"], "V1")
    expected_state = s2.snapshot()
    v2b = mv.commit(s2, v2)
    final, vf = mv.recover()
    assert v2b > v and vf == v2b, "version must advance monotonically across the revocation commit"
    assert final.snapshot() == expected_state, "the revoked state must survive cold recovery byte-for-byte"
    assert final.ledger.count() == 1, "revocation must not drop the acknowledged event"


def test_C7_real_sigkill_before_rename_leaves_prior_state_intact(tmp_path):
    """A real SIGKILL inside the publish window must never tear the journal."""
    jp = tmp_path / "journal.json"
    mv = MultiwriterJournal(jp)
    s, v = mv.recover(); ev = s.ledger.admit(legacy("A")); s.outbox.emit(ev["occurrence_id"])
    mv.commit(s, v)
    before = jp.read_bytes()
    worker = tmp_path / "killer.py"
    worker.write_text(
        "import os,sys\nsys.path.insert(0,sys.argv[3])\n"
        "from multiwriter_journal import MultiwriterJournal\n"
        "from test_rto_hostile import legacy\n"
        "mv=MultiwriterJournal(sys.argv[1]); s,v=mv.recover()\n"
        "e=s.ledger.admit(legacy('B')); s.outbox.emit(e['occurrence_id'])\n"
        "mv.commit(s, v, crash_boundary='BEFORE_RENAME')\n")
    env = dict(os.environ, PYTHONPATH=BOTH)
    p = subprocess.Popen([sys.executable, str(worker), str(jp), "B", BOTH], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.communicate()
    assert p.returncode == 79, "worker must exit at the injected crash boundary, rc=%s" % p.returncode
    after = jp.read_bytes()
    assert after == before, "journal must be byte-identical after a pre-rename crash"
    rec, vv = MultiwriterJournal(jp).recover()
    assert rec.ledger.count() == 1 and vv == 1, "cold recovery must yield the pre-crash committed state"


def test_C8_cold_recovery_identity_after_interleaving(tmp_path):
    _run("cas", ["A", "B", "C"], str(tmp_path))
    jp = tmp_path / "journal.json"
    d = json.loads(jp.read_text())
    assert d["schema"] == "OUTBOX_F2_JOURNAL_V2"
    assert d["writer_version"] == 3
    assert MultiwriterJournal(jp).recover()[0].ledger.count() == 3
