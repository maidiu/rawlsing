"""OUT14 supplementary source-free integrity court; NOT an OUT13 frozen oracle rewrite.
Run with PYTHONPATH=<accepted OUT9 stage>:<OUT12 candidate stage> and real pytest.
Known residual: direct accepted Journal.commit remains a legal bypass. Owner HOLD.
"""
import json, os, signal, subprocess, sys, time
from pathlib import Path
import pytest
from outbox_prototype import Journal, make_prototype, _canonical, _hash
from test_rto_hostile import legacy
from multiwriter_journal import MultiwriterJournal, VersionStateUnreadable, StaleJournalConflict, LockTimeoutError
from test_out12_multiwriter_court import _run

def _seed(path):
    j=MultiwriterJournal(path)
    p,v=j.recover()
    e=p.ledger.admit(legacy("SEED")); p.outbox.emit(e["occurrence_id"])
    assert j.commit(p,v)==1
    return j

@pytest.mark.parametrize("value", ["broken", None, -2, 0, False, 1.2, {}, "1", 22])
def test_corrupted_or_injected_version_is_never_coerced_to_zero(tmp_path,value):
    path=tmp_path/"journal.json"; j=_seed(path)
    r=json.loads(path.read_text()); r["writer_version"]=value
    path.write_text(_canonical(r))
    with pytest.raises(VersionStateUnreadable) as e: j.recover()
    assert e.value.code=="VERSION_STATE_UNREADABLE"
    with pytest.raises(VersionStateUnreadable):j.commit(j._base.recover(),0)

def test_legacy_bypass_removes_version_and_is_detected_not_prevented(tmp_path):
    path=tmp_path/"journal.json"; j=_seed(path)
    old=Journal(path)
    p=old.recover(); e=p.ledger.admit(legacy("LEGACY")); p.outbox.emit(e["occurrence_id"])
    old.commit(p)              # Documented residual writer authority: DOES bypass!
    assert "writer_version" not in json.loads(path.read_text())
    with pytest.raises(VersionStateUnreadable,match="VERSION_STATE_UNREADABLE"):
        j.recover()
    with pytest.raises(VersionStateUnreadable):j.commit(p,0)

@pytest.mark.parametrize("delete", ["writer_version","version_state_digest","state_digest"])
def test_missing_field_is_never_genesis(tmp_path,delete):
    path=tmp_path/"journal.json"; j=_seed(path)
    r=json.loads(path.read_text());del r[delete];path.write_text(_canonical(r))
    with pytest.raises(VersionStateUnreadable):j.recover()

def test_only_nonexistent_file_is_genesis_version_zero(tmp_path):
    j=MultiwriterJournal(tmp_path/"no-journal.json")
    p,v=j.recover()
    assert v==0 and p.ledger.count()==0
    path=j.path;path.write_text("")
    with pytest.raises(VersionStateUnreadable):j.recover()

def test_valid_full_envelope_binding_and_stale_retry(tmp_path):
    path=tmp_path/"journal.json"; j=_seed(path)
    snap,v=j.recover()
    r=json.loads(path.read_text())
    assert r["version_state_digest"]==_hash({"schema":r["schema"],"state":r["state"],"writer_version":v})
    assert r["state_digest"]==_hash(r["state"])
    e=snap.ledger.admit(legacy("NEXT"));snap.outbox.emit(e["occurrence_id"])
    assert j.commit(snap,v)==2
    with pytest.raises(StaleJournalConflict):j.commit(snap,v)
    p,v=j.recover();assert v==2 and p.ledger.count()==2

def test_replay_or_version_reset_without_recomputing_digest_fails(tmp_path):
    path=tmp_path/"journal.json"; j=_seed(path)
    r=json.loads(path.read_text());r["writer_version"]=0
    path.write_text(_canonical(r))
    with pytest.raises(VersionStateUnreadable):j.recover()

def test_recomputed_unkeyed_digest_is_not_writer_authentication(tmp_path):
    """This exhibits a remaining science/authority limit, rather than passing it off as security."""
    path=tmp_path/"journal.json";j=_seed(path)
    r=json.loads(path.read_text())
    r["writer_version"]=10
    r["version_state_digest"]=_hash({"schema":r["schema"],"state":r["state"],"writer_version":10})
    path.write_text(_canonical(r))
    assert j.recover()[1]==10  # Explicit unkeyed-forgery counterexample; owner HOLD.

@pytest.mark.parametrize("n",[2,3,5])
def test_barrier_writers_no_lost_acknowledged_event_and_monotonic(n,tmp_path):
    r=_run("cas",[f"W{i}" for i in range(n)],str(tmp_path))
    assert len(r)==n and all(x["rc"]==0 for x in r),r
    p=tmp_path/"journal.json";rec,ver=MultiwriterJournal(p).recover()
    assert rec.ledger.count()==n and ver==n
    d=json.loads(p.read_text())
    assert d["version_state_digest"]==_hash({"schema":d["schema"],"state":d["state"],"writer_version":ver})
    commits=sorted(a["committed"] for x in r for a in json.loads(x["out"])["attempts"] if "committed" in a)
    assert commits==list(range(1,n+1))

def test_ledger_prefix_cannot_be_rolled_back_by_fresh_expected_version(tmp_path):
    path=tmp_path/"journal.json";j=_seed(path)
    _snap,v=j.recover()
    p=make_prototype()
    with pytest.raises(ValueError,match="ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED"):
        j.commit(p,v)
    assert j.recover()[0].ledger.count()==1

def test_external_lock_timeout_is_typed(tmp_path):
    path=tmp_path/"journal.json";j=MultiwriterJournal(path,lock_timeout=0.01,poll=0.001)
    fd=j._acquire()
    try:
        with pytest.raises(LockTimeoutError) as err:j._acquire()
        assert err.value.code=="JOURNAL_LOCK_TIMEOUT"
    finally:j._release(fd)

@pytest.mark.parametrize("boundary,expected_rc,expected_ver",[("BEFORE_RENAME",79,1),
  ("SIGKILL_BEFORE_RENAME",-signal.SIGKILL,1),
  ("AFTER_COMMIT",79,2),("SIGKILL_AFTER_COMMIT",-signal.SIGKILL,2)])
def test_rename_crash_boundaries_and_true_signal(tmp_path,boundary,expected_rc,expected_ver):
    path=tmp_path/"journal.json";j=_seed(path);prior=path.read_bytes()
    worker=tmp_path/"worker.py"
    worker.write_text("""import sys
from multiwriter_journal import MultiwriterJournal
from test_rto_hostile import legacy
j=MultiwriterJournal(sys.argv[1]);p,v=j.recover()
e=p.ledger.admit(legacy("CRASH"));p.outbox.emit(e["occurrence_id"])
j.commit(p,v,crash_boundary=sys.argv[2])
""")
    proc=subprocess.run([sys.executable,str(worker),str(path),boundary],capture_output=True,text=True)
    assert proc.returncode==expected_rc,(proc.returncode,proc.stderr)
    if expected_ver==1:assert path.read_bytes()==prior
    recovered,ver=MultiwriterJournal(path).recover()
    assert ver==expected_ver and recovered.ledger.count()==expected_ver

def test_legacy_source_not_replaced_or_monkeypatched():
    assert Journal is not MultiwriterJournal
    assert Journal.commit is not MultiwriterJournal.commit
