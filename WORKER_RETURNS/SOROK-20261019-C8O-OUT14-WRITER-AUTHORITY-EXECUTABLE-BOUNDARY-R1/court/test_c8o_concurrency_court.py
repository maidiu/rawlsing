"""C8O hostile court A: genuine OS-process multiwriter concurrency and version-state custody.

Real subprocesses, real fcntl.flock, real fsync, real file barrier. Event
identities come from the ACCEPTED API (ledger.admit / outbox.emit).
GRAIN: TEST_ONLY source-free multiwriter on a LOCAL filesystem.
NOT exactly-once delivery. NOT power-loss durability. NOT ADP019. NOT V3.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import (  # noqa: E402
    capability,
    cold_reopen,
    legacy,
    spawn,
    write_evidence,
)

from c8o_trusted_outbox import (  # noqa: E402
    AcknowledgedPrefixRewriteRefused,
    C8OccurrenceJournal,
    GhostReplayRefused,
    StaleJournalConflict,
    VersionStateUnreadable,
    WriterCapabilityRequired,
    os_clock,
)
from outbox_prototype import Journal, make_prototype  # noqa: E402


def _durable_ids(path: Path) -> list:
    snap = Journal(path).recover()
    return [e["occurrence_id"] for e in snap.ledger.events]


def _acknowledged_ids(rows) -> list:
    ids: list = []
    for r in rows:
        for a in json.loads(r["out"])["attempts"]:
            ids.extend(a.get("acknowledged") or [])
    return sorted(set(ids))


@pytest.mark.parametrize("n", [2, 3, 5])
def test_barrier_writers_no_lost_acknowledged_event_and_monotone_version(n, tmp_path):
    rows = spawn("cas", tmp_path, [f"W{i}" for i in range(n)])
    assert all(r["rc"] == 0 for r in rows), rows
    durable = _durable_ids(tmp_path / "journal.json")
    acknowledged = _acknowledged_ids(rows)
    assert sorted(durable) == acknowledged
    assert len(durable) == n
    p, v, custody = C8OccurrenceJournal(tmp_path / "journal.json").recover_custody()
    assert v == n
    assert p.ledger.count() == n
    assert custody.status == "VERSIONED_VALID"
    commits = sorted(
        a["committed"]
        for r in rows
        for a in json.loads(r["out"])["attempts"]
        if "committed" in a
    )
    assert commits == list(range(1, n + 1))
    reopened = cold_reopen(tmp_path / "journal.json")
    assert reopened["version"] == n and reopened["count"] == n
    write_evidence(
        f"writer_race_{n}.json",
        {
            "writers": rows,
            "durable_occurrence_ids": durable,
            "acknowledged_occurrence_ids": acknowledged,
            "committed_versions": commits,
            "cold_reopen": reopened,
        },
    )


def test_stale_cas_is_typed_and_lawful_retry_succeeds(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    s1, v1 = j.recover()
    s2, v2 = j.recover()
    assert v1 == v2 == 0
    e1 = s1.ledger.admit(legacy("A"))
    s1.outbox.emit(e1["occurrence_id"])
    assert j.commit(s1, v1, capability=capability("A")).writer_version == 1
    e2 = s2.ledger.admit(legacy("B"))
    s2.outbox.emit(e2["occurrence_id"])
    with pytest.raises(StaleJournalConflict) as err:
        j.commit(s2, v2, capability=capability("B"))
    assert err.value.code == "STALE_JOURNAL_CONFLICT"
    snap, ver = j.recover()
    assert ver == 1 and snap.ledger.count() == 1
    ev = snap.ledger.admit(legacy("B"))
    snap.outbox.emit(ev["occurrence_id"])
    assert j.commit(snap, ver, capability=capability("B")).writer_version == 2
    assert _durable_ids(tmp_path / "journal.json") == ["OCC-0001", "OCC-0002"]


def test_acknowledged_ledger_prefix_cannot_be_rewritten(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for label in ("A", "B"):
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("A"))
    _p, ver = j.recover()
    stripped = make_prototype()
    with pytest.raises(AcknowledgedPrefixRewriteRefused) as err:
        j.commit(stripped, ver, capability=capability("ATTACKER"))
    assert err.value.code == "ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED"
    assert _durable_ids(tmp_path / "journal.json") == ["OCC-0001", "OCC-0002"]
    reordered = make_prototype()
    for label in ("B", "A"):
        ev = reordered.ledger.admit(legacy(label))
        reordered.outbox.emit(ev["occurrence_id"])
    with pytest.raises(AcknowledgedPrefixRewriteRefused):
        j.commit(reordered, ver, capability=capability("ATTACKER"))
    assert _durable_ids(tmp_path / "journal.json") == ["OCC-0001", "OCC-0002"]


def test_commit_without_capability_is_refused(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("A"))
    snap.outbox.emit(ev["occurrence_id"])
    with pytest.raises(WriterCapabilityRequired) as err:
        j.commit(snap, v, capability=None)
    assert err.value.code == "WRITER_CAPABILITY_REQUIRED"
    assert not (tmp_path / "journal.json").exists()


@pytest.mark.parametrize(
    "mutate",
    ["broken", None, -2, 0, False, 1.2, {}, "1", 22],
)
def test_corrupted_or_injected_version_is_never_coerced_to_zero(tmp_path, mutate):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("SEED"))
    snap.outbox.emit(ev["occurrence_id"])
    assert j.commit(snap, v, capability=capability("SEED")).writer_version == 1
    receipt = json.loads((tmp_path / "journal.json").read_text(encoding="utf8"))
    receipt["writer_version"] = mutate
    (tmp_path / "journal.json").write_text(json.dumps(receipt), encoding="utf8")
    with pytest.raises(VersionStateUnreadable) as err:
        j.recover()
    assert err.value.code == "VERSION_STATE_UNREADABLE"
    with pytest.raises(VersionStateUnreadable):
        j.commit(j.recover()[0], 0, capability=capability("SEED"))


@pytest.mark.parametrize("field_name", ["writer_version", "version_state_digest", "state_digest", "ledger_prefix_digest", "commit_receipt_id"])
def test_missing_envelope_field_is_never_genesis(tmp_path, field_name):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("SEED"))
    snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("SEED"))
    receipt = json.loads((tmp_path / "journal.json").read_text(encoding="utf8"))
    del receipt[field_name]
    (tmp_path / "journal.json").write_text(json.dumps(receipt), encoding="utf8")
    with pytest.raises(VersionStateUnreadable):
        j.recover()


def test_only_nonexistent_file_is_genesis_version_zero(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "no-journal.json")
    p, v, custody = j.recover_custody()
    assert v == 0 and custody.status == "GENESIS_V0" and p.ledger.count() == 0
    (tmp_path / "no-journal.json").write_text("", encoding="utf8")
    with pytest.raises(VersionStateUnreadable):
        j.recover()


def test_replay_of_same_commit_attempt_creates_no_ghost(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("A"))
    snap.outbox.emit(ev["occurrence_id"])
    receipt = j.commit(snap, v, capability=capability("A"))
    with pytest.raises(StaleJournalConflict):
        j.commit(snap, v, capability=capability("A"))
    snap2, v2 = j.recover()
    again = snap2.ledger.admit(legacy("A"))
    assert again["occurrence_id"] == ev["occurrence_id"]
    assert snap2.ledger.count() == 1
    j.commit(snap2, v2, capability=capability("A"))
    durable = _durable_ids(tmp_path / "journal.json")
    assert durable == ["OCC-0001"]
    assert receipt.acknowledged_occurrence_ids == ["OCC-0001"]
    reopened = cold_reopen(tmp_path / "journal.json")
    assert reopened["count"] == 1 and reopened["ids"] == ["OCC-0001"]


def test_crafted_duplicate_or_out_of_order_occurrence_is_refused(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for label in ("W0", "W1"):
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("W0"))
    before = (tmp_path / "journal.json").read_bytes()
    fresh, ver = j.recover()
    ghost = dict(fresh.ledger.events[0])
    ghost["occurrence_id"] = "OCC-0001"
    fresh.ledger._events.append(ghost)
    with pytest.raises((ValueError, GhostReplayRefused)):
        j.commit(fresh, ver, capability=capability("GHOST"))
    assert (tmp_path / "journal.json").read_bytes() == before
    assert _durable_ids(tmp_path / "journal.json") == ["OCC-0001", "OCC-0002"]


def test_unpermitted_empty_commit_preserves_other_writers_source(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for label in ("W0", "W1"):
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("W0"))
    before = (tmp_path / "journal.json").read_bytes()
    empty = make_prototype()
    _p, ver = j.recover()
    with pytest.raises(AcknowledgedPrefixRewriteRefused):
        j.commit(empty, ver, capability=capability("EMPTY"))
    assert (tmp_path / "journal.json").read_bytes() == before
    assert _durable_ids(tmp_path / "journal.json") == ["OCC-0001", "OCC-0002"]


def test_lock_timeout_is_typed_and_lock_is_released(tmp_path):
    import fcntl
    import os

    j = C8OccurrenceJournal(tmp_path / "journal.json", lock_timeout=0.3, poll=0.01)
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("SEED"))
    snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("SEED"))
    lock = Path(str(tmp_path / "journal.json") + ".lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_RDWR, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        from c8o_trusted_outbox import LockTimeoutError

        with pytest.raises(LockTimeoutError) as err:
            j.recover()
        assert err.value.code == "JOURNAL_LOCK_TIMEOUT"
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
    _p, ver = j.recover()
    assert ver == 1


def test_effective_clock_is_recorded_and_trusted_time_is_refused(tmp_path):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("A"))
    snap.outbox.emit(ev["occurrence_id"])
    receipt = j.commit(snap, v, capability=capability("A"))
    assert receipt.effective_clock["source"] == "OS_CLOCK_SOURCEFREE_FIXTURE"
    assert "T" in receipt.effective_clock["value"]
    from c8o_trusted_outbox import TrustedTimeSourceUnissued

    snap2, v2 = j.recover()
    ev2 = snap2.ledger.admit(legacy("B"))
    snap2.outbox.emit(ev2["occurrence_id"])
    with pytest.raises(TrustedTimeSourceUnissued):
        j.commit(snap2, v2, capability=capability("B"), require_trusted_time=True)
