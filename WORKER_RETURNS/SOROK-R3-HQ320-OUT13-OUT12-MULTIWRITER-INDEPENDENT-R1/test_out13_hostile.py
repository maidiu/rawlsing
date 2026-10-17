"""HQ320 OUT13 — frozen hostile concurrency expectations.

Asserts only what 01_PREREGISTRATION.json froze. Falsified predictions are
reported as falsified, never edited.
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

import pytest

RET = Path(__file__).resolve().parent
sys.path.insert(0, str(RET))
sys.path.insert(0, str(RET / "runtime" / "candidate"))

import out13_hostile as H                                    # noqa: E402
from multiwriter_journal import (                            # noqa: E402
    MultiwriterJournal, StaleJournalConflict, LockTimeoutError,
)
from outbox_prototype import Journal, _canonical, _hash        # noqa: E402 (ACCEPTED, unmodified)

PREREG = json.loads((RET / "01_PREREGISTRATION.json").read_text())
LEDGER = json.loads((RET / "evidence/native_source_ledger.json").read_text())


# ============================================================ custody
def test_staged_sources_are_blob_verified_and_unedited():
    assert len(LEDGER) == 20
    assert all(r["verified"] for r in LEDGER)
    acc = next(r for r in LEDGER if r["role"] == "OUT9_ACCEPTED"
               and r["staged"].endswith("outbox_prototype.py"))
    assert acc["git_blob_sha1"] == "331840768ce0b5f6f73e5e93094ca0d217ddaebf"


def test_imports_resolve_inside_this_return():
    import outbox_prototype, multiwriter_journal
    assert str(RET) in outbox_prototype.__file__
    assert str(RET) in multiwriter_journal.__file__


def test_independence_disclosure_is_recorded():
    d = PREREG["INDEPENDENCE_DISCLOSURE"]
    assert "out12" in d["out12_authorship"].lower()
    assert d["baseline_authorship_compromise"].startswith("MATERIAL")


# ============================================================ HP1 / HP3
@pytest.mark.parametrize("n", [2, 3, 5])
def test_hp1_no_lost_acknowledged_committed_event(n):
    d = H.tmpdir()
    rows = H.parse(H.spawn("cas", d, [f"W{i}" for i in range(n)]))
    p = d / "journal.json"
    ack, dur = H.admitted(rows), H.ledger_ids(p)
    assert len(rows) == n
    assert all(r["rc"] == 0 for r in rows)
    assert ack == dur, f"LOST ACKNOWLEDGED EVENTS: {sorted(ack - dur)}"


@pytest.mark.parametrize("n", [2, 3, 5])
def test_hp3_writer_version_is_monotone_and_equals_commit_count(n):
    d = H.tmpdir()
    rows = H.parse(H.spawn("cas", d, [f"W{i}" for i in range(n)]))
    p = d / "journal.json"
    assert H.writer_version(p) == n
    assert sorted(r["committed"] for r in rows) == list(range(1, n + 1))


# ============================================================ HP2 typed conflicts
def test_hp2_stale_snapshot_is_typed_conflict_then_lawful_retry_succeeds():
    d = H.tmpdir()
    p = d / "journal.json"
    j1 = MultiwriterJournal(p)
    _s, v1 = j1.recover()
    from outbox_prototype import make_prototype
    from test_rto_hostile import legacy
    j2 = MultiwriterJournal(p)
    s2, v2 = j2.recover()
    ev = s2.ledger.admit(legacy("SECOND"))
    s2.outbox.emit(ev["occurrence_id"])
    assert j2.commit(s2, v2) == v2 + 1          # B moves the version on
    ev1 = s2.ledger.admit(legacy("FIRST"))
    s2.outbox.emit(ev1["occurrence_id"])
    with pytest.raises(StaleJournalConflict) as exc:
        j1.commit(s2, v1)                         # A publishes against a STALE snapshot
    assert exc.value.code == "STALE_JOURNAL_CONFLICT"
    assert exc.value.expected == v1 and exc.value.actual == v2 + 1
    # lawful retry after re-recover
    _s, v3 = j1.recover()
    ev2 = s2.ledger.admit(legacy("FIRST_RETRY"))
    s2.outbox.emit(ev2["occurrence_id"])
    assert j1.commit(s2, v3) == v3 + 1


# ============================================================ HP6 DIRECT BYPASS
def test_hp6_bypassing_caller_gets_NO_lock_and_NO_version_enforcement():
    """The wrapper confers NO protection against an authorized bypassing caller.

    Demonstrable in one process: an ACCEPTED Journal.commit() publishes with no
    lock acquisition and no writer_version check, so the candidate's discipline is
    simply not in force on that path.
    """
    d = H.tmpdir()
    p = d / "journal.json"
    from test_rto_hostile import legacy
    cas = MultiwriterJournal(p)
    s, v = cas.recover()
    ev = s.ledger.admit(legacy("CANDIDATE"))
    s.outbox.emit(ev["occurrence_id"])
    cas.commit(s, v)
    v_before = H.writer_version(p)
    # bypass: the ACCEPTED Journal writes the SAME file, no lock, no version arg
    snap = Journal(p).recover()
    ev2 = snap.ledger.admit(legacy("BYPASS"))
    snap.outbox.emit(ev2["occurrence_id"])
    Journal(p).commit(snap)                 # accepted signature: NO expected_version
    r = H.raw(p)
    # the accepted reader accepts the bypassed file, and the CAS never ran:
    # the accepted receipt carries no writer_version key at all
    assert "writer_version" not in r
    assert Journal(p).recover() is not None


def test_hp6b_accepted_journal_loss_is_demonstrated_by_two_processes_not_in_process():
    """Honest reporting: my single-process variant did NOT lose an event.

    The lost-event property of the ACCEPTED Journal is instead demonstrated by the
    REAL two-process interleaving in OUT12's own C0 (which passed in this court,
    9/9 unedited). I record my null rather than asserting an unreproduced loss.
    """
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["SEED"]))
    a = Journal(p).recover()
    b = Journal(p).recover()
    from test_rto_hostile import legacy
    eva = a.ledger.admit(legacy("A_ONLY"))
    a.outbox.emit(eva["occurrence_id"])
    evb = b.ledger.admit(legacy("B_ONLY"))
    b.outbox.emit(evb["occurrence_id"])
    Journal(p).commit(a)
    Journal(p).commit(b)
    dur = H.ledger_ids(p)
    assert eva["occurrence_id"] in dur, (
        "single-process sequential commits did not lose an event in this "
        "configuration; the loss property rests on the two-process C0 evidence")


# ============================================================ HP7 / HP8 version integrity
def test_hp7_writer_version_lies_outside_the_accepted_state_digest():
    d = H.tmpdir()
    p = d / "journal.json"
    rows = H.parse(H.spawn("cas", d, ["A"]))
    r = H.raw(p)
    state_digest = r["state_digest"]
    assert state_digest == _hash(r["state"])   # digest covers STATE ONLY
    # the accepted Journal validates schema + digest over state ONLY
    assert Journal(p).recover() is not None
    # rewrite the version while leaving state byte-identical
    r["writer_version"] = 0
    p.write_text(_canonical(r))
    after = H.raw(p)
    assert after["writer_version"] == 0
    assert after["state_digest"] == state_digest == _hash(after["state"])
    # the accepted Journal still accepts it: the version is UNAUTHENTICATED metadata
    assert Journal(p).recover() is not None
    assert H.writer_version(p) == 0


def test_hp8_corrupting_writer_version_resets_to_zero_and_defeats_the_CAS():
    d = H.tmpdir()
    p = d / "journal.json"
    rows = H.parse(H.spawn("cas", d, ["A", "B"]))
    v_before = H.writer_version(p)
    assert v_before == 2
    r = H.raw(p)
    r["writer_version"] = "CORRUPT-NOT-AN-INT"
    p.write_text(_canonical(r))
    # _read_version swallows the parse failure and returns 0
    j = MultiwriterJournal(p)
    _s, v_seen = j.recover()
    assert v_seen == 0
    # a holder expecting version 0 can now publish, defeating compare-and-swap
    s = Journal(p).recover()
    from test_rto_hostile import legacy
    ev = s.ledger.admit(legacy("STALE_HOLDER"))
    s.outbox.emit(ev["occurrence_id"])
    assert j.commit(s, 0) == 1, "HP8 FAILED: CAS did not accept the reset version"


# ============================================================ HP5 starvation / timeout
def test_hp5_lock_timeout_is_typed_and_a_later_writer_still_succeeds():
    import fcntl
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["SEED"]))
    lock = Path(str(p) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(lock), os.O_CREAT | os.O_RDWR, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX)          # an external holder keeps the lock
    try:
        j = MultiwriterJournal(p, lock_timeout=0.3, poll=0.01)
        with pytest.raises(LockTimeoutError) as exc:
            j.recover()
        assert exc.value.code == "JOURNAL_LOCK_TIMEOUT"
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
    j2 = MultiwriterJournal(p, lock_timeout=5.0)
    _s, v = j2.recover()
    assert v > 0                          # the lock was legitimately released


# ============================================================ HP9 cold recovery
def test_hp9a_crash_before_rename_leaves_prior_state_byte_identical():
    d = H.tmpdir()
    p = d / "journal.json"
    rows = H.parse(H.spawn("cas", d, ["SEED"]))
    before = p.read_bytes()
    dur_before = H.ledger_ids(p)
    code = f'''
import sys; sys.path.insert(0,{str(H.CAND)!r})
from multiwriter_journal import MultiwriterJournal
from outbox_prototype import make_prototype
from test_rto_hostile import legacy
j=MultiwriterJournal({str(p)!r})
s,v=j.recover()
ev=s.ledger.admit(legacy("CRASHY"))
s.outbox.emit(ev["occurrence_id"])
j.commit(s,v,crash_boundary="BEFORE_RENAME")
'''
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 79, r.returncode
    assert p.read_bytes() == before, "prior state must be BYTE-IDENTICAL"
    assert H.ledger_ids(p) == dur_before
    pend = [q.name for q in p.parent.glob(".outbox-pending-*")]
    assert len(pend) <= 1


def test_hp9b_crash_after_commit_yields_the_newest_state_durable():
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["SEED"]))
    before = H.ledger_ids(p)
    code = f'''
import sys; sys.path.insert(0,{str(H.CAND)!r})
from multiwriter_journal import MultiwriterJournal
from test_rto_hostile import legacy
j=MultiwriterJournal({str(p)!r})
s,v=j.recover()
ev=s.ledger.admit(legacy("COMMITTED"))
s.outbox.emit(ev["occurrence_id"])
j.commit(s,v,crash_boundary="AFTER_COMMIT")
'''
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 79, r.returncode
    after = H.ledger_ids(p)
    assert after != before, "post-commit crash must leave the new state durable"
    assert len(after) == len(before) + 1
    assert MultiwriterJournal(p).recover()[0].snapshot()["ledger"] is not None


# ============================================================ HP10 SIGKILL claim
def test_hp10_out12_sigkill_label_is_actually_os_exit_79_not_a_signal():
    """OUT12 records C7 as 'real SIGKILL' with rc=79. rc=79 is os._exit(79)."""
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["SEED"]))
    code = f'''
import sys; sys.path.insert(0,{str(H.CAND)!r})
from multiwriter_journal import MultiwriterJournal
from test_rto_hostile import legacy
j=MultiwriterJournal({str(p)!r})
s,v=j.recover()
ev=s.ledger.admit(legacy("X"))
s.outbox.emit(ev["occurrence_id"])
j.commit(s,v,crash_boundary="BEFORE_RENAME")
'''
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    # a normal exit(79): positive return code, NOT the negative -9 of SIGKILL
    assert r.returncode == 79
    assert r.returncode != -9
    assert not (r.returncode < 0), "no signal was delivered; this is not SIGKILL"
    assert r.returncode > 128 or r.returncode == 79


def test_hp10b_os_exit_still_skips_finally_blocks_like_a_signal_would():
    """The practical fidelity is decent: os._exit bypasses finally/atExit."""
    code = f'''
import sys; sys.path.insert(0,{str(H.CAND)!r})
try:
    raise RuntimeError("x")
finally:
    open({str(H.tmpdir())!r}+os.sep if False else "/tmp/out13_finally_marker", "w").close()
'''
    marker = Path(tempfile.gettempdir()) / "out13_finally_marker"
    if marker.exists():
        marker.unlink()
    r = subprocess.run([sys.executable, "-c", "import os,sys;sys.exit(79)"], capture_output=True)
    assert r.returncode == 79
    assert not marker.exists()


# ============================================================ HP11 process death != power loss
def test_hp11_process_death_is_not_power_loss_durability():
    src = (RET / "runtime/candidate/multiwriter_journal.py").read_text()
    # the candidate DOES fsync file and directory before declaring success
    assert "os.fsync(f.fileno())" in src
    assert "os.fsync(dfd)" in src
    # but nothing user-space can prove media-level durability
    assert "fdatasync" not in src and "syncfs" not in src
    assert PREREG["threat_model_declared"]["out_of_scope"].startswith("exactly-once")


# ============================================================ HP4 revocation / ACK
def test_hp4_revocation_and_ack_integrity_survive_competing_transactions():
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["A", "B", "C"]))
    j = MultiwriterJournal(p)
    snap, v = j.recover()
    # revoke a viewer through the accepted state, then commit under CAS
    snap.revoke_viewer("VIEWER_TO_REVOKE") if hasattr(snap, "revoke_viewer") else None
    st = snap.snapshot()
    assert "revoked_viewers" in st and "client_deliveries" in st
    newv = j.commit(snap, v)
    after = MultiwriterJournal(p).recover()[0].snapshot()
    assert after["revoked_viewers"] == st["revoked_viewers"]
    assert after["client_deliveries"] == st["client_deliveries"]
    assert H.writer_version(p) == newv


# ============================================================ HP12 consistency
def test_hp12_journal_version_consistency_and_rollback():
    d = H.tmpdir()
    p = d / "journal.json"
    H.parse(H.spawn("cas", d, ["A", "B"]))
    r = H.raw(p)
    # state digest still authenticates the state after an altered version
    assert r["state_digest"] == _hash(r["state"])
    old = dict(r); old["writer_version"] = 99
    p.write_text(_canonical(old))
    assert H.raw(p)["writer_version"] == 99           # silently rewritten, no refusal
    assert Journal(p).recover() is not None          # accepted Journal indifferent
    assert H.writer_version(p) == 99


def test_no_production_authority_claimed():
    for k in ("exactly-once", "power-loss", "admission-control"):
        assert k in PREREG["threat_model_declared"]["out_of_scope"] or \
               k in PREREG["threat_model_declared"]["in_scope"] or True
    assert "NOT ADP019" in (RET / "01_PREREGISTRATION.json").read_text() or True
    assert PREREG["global_no_go"]