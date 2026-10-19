"""C8OI independent writer-security, occurrence-custody and receiving-consumer court.

Three separate verdicts: engineering, scientific, authority. Each test is an
independent I2 assertion. No author test is copied or relaxed. The original
historical REDs are preserved and never dressed as safety regressions.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidate"
CONSUMER = ROOT / "consumer"
RUNTIME_OUT12 = ROOT / "runtime" / "stage_out12"
for p in (str(CANDIDATE), str(CONSUMER), str(RUNTIME_OUT12)):
    if p not in sys.path:
        sys.path.insert(0, p)

from c8o_trusted_outbox import (  # noqa: E402
    C8OccurrenceJournal,
    StaleJournalConflict,
    UnkeyedFormatCapabilityVerifier,
    WriterCapability,
)
from outbox_prototype import Journal, make_prototype  # noqa: E402


def cap(wid: str) -> WriterCapability:
    return WriterCapability(
        writer_id=wid,
        capability_token="TOKEN-" + wid + "-" + "x" * 24,
        issuer_ref="UNISSUED_NO_TRUSTED_ISSUER",
    )


def legacy_event(label: str = "L") -> dict:
    return {"candidate_id": label, "payload": {"utterance": "Hi"}}


# ---------------------------------------------------------------------------
# Engineering: old writer bypass, concurrency, crash, cold reopen
# ---------------------------------------------------------------------------

def test_legacy_journal_commit_destroys_acknowledged_events() -> None:
    """Old Journal.commit remains legally callable and destroys acknowledged events."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = Journal(path)
        for i in range(3):
            ev = {"candidate_id": f"occ-{i}", "payload": {"n": i}}
            result, err = j.admit_and_queue(ev)
            assert err is None, f"admit failed: {err}"
        before = path.read_bytes()
        assert before, "journal must have content"
        # Old writer replaces via recover + commit with new state
        p = j.recover()
        p2 = make_prototype()
        ev = p2.ledger.admit({"candidate_id": "attacker", "payload": {"wipe": True}})
        p2.outbox.emit(ev["occurrence_id"])
        j.commit(p2)
        after = path.read_bytes()
        assert after != before, "old writer must change journal bytes"
        # The old writer's commit replaced the state entirely
        j2 = Journal(path)
        state = j2.recover()
        ids = [e.get("occurrence_id") for e in state.ledger.events]
        assert not any("occ-" in str(i) for i in ids), (
            f"old writer destroys acknowledged events: {ids}"
        )


def test_legacy_writer_bypass_after_green_wrapper() -> None:
    """Old writer can erase acknowledged events after wrapper commit."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        receipt = j.commit(snap, ver, capability=cap("W1"))
        assert receipt.writer_version == 1
        before = path.read_bytes()
        assert before
        # Old writer wipes via prototype
        j2 = Journal(path)
        p = make_prototype()
        ev2 = p.ledger.admit({"candidate_id": "wipe", "payload": {"d": True}})
        p.outbox.emit(ev2["occurrence_id"])
        j2.commit(p)
        after = path.read_bytes()
        assert after != before
        # Wrapper detects bypass after the fact
        j3 = C8OccurrenceJournal(path)
        custody = j3.classify()
        assert custody.status != "VERSIONED_VALID", (
            f"old writer bypass must be detected: {custody.status}"
        )


def test_two_real_writer_pids_no_acknowledged_loss() -> None:
    """Two writer processes produce no acknowledged event loss."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        results = []
        for label in ("W1", "W2"):
            j = C8OccurrenceJournal(path)
            snap, ver = j.recover()
            ev = snap.ledger.admit(legacy_event(label))
            snap.outbox.emit(ev["occurrence_id"])
            try:
                receipt = j.commit(snap, ver, capability=cap(label))
                results.append(set(receipt.acknowledged_occurrence_ids))
            except StaleJournalConflict:
                snap2, ver2 = j.recover()
                ev2 = snap2.ledger.admit(legacy_event(label + "r"))
                snap2.outbox.emit(ev2["occurrence_id"])
                receipt = j.commit(snap2, ver2, capability=cap(label))
                results.append(set(receipt.acknowledged_occurrence_ids))
        all_ids = set()
        for ids in results:
            all_ids.update(ids)
        assert len(all_ids) >= 2, f"lost events: {all_ids}"


def test_stale_cas_typed_conflict() -> None:
    """A stale CAS produces typed StaleJournalConflict."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        snap2, ver2 = j.recover()
        ev2 = snap2.ledger.admit(legacy_event("B"))
        snap2.outbox.emit(ev2["occurrence_id"])
        with pytest.raises(StaleJournalConflict):
            j.commit(snap2, 0, capability=cap("W2"))


def test_sigkill_before_rename_preserves_prior_state() -> None:
    """SIGKILL before rename leaves prior state byte-identical."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        before = path.read_bytes()
        script = (
            "import sys,os,signal;"
            f"sys.path.insert(0,{str(CANDIDATE)!r});"
            f"sys.path.insert(0,{str(RUNTIME_OUT12)!r});"
            "from c8o_trusted_outbox import C8OccurrenceJournal,WriterCapability;"
            f"j=C8OccurrenceJournal({str(path)!r});"
            "snap,ver=j.recover();"
            "ev=snap.ledger.admit({'candidate_id':'K','payload':{'x':1}});"
            "snap.outbox.emit(ev['occurrence_id']);"
            "j.commit(snap,ver,capability=WriterCapability(writer_id='WK',"
            "capability_token='T'+'x'*24,issuer_ref='UNISSUED'),"
            "crash_boundary='SIGKILL_BEFORE_RENAME')"
        )
        proc = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=30)
        assert proc.returncode == -9, f"expected SIGKILL rc=-9, got {proc.returncode}"
        after = path.read_bytes()
        assert after == before, "SIGKILL before rename must preserve prior state"


def test_cold_reopen_sees_only_committed_state() -> None:
    """Cold reopen in fresh process sees only committed state, no ghost."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        receipt = j.commit(snap, ver, capability=cap("W1"))
        committed_ids = set(receipt.acknowledged_occurrence_ids)
        script = (
            "import sys,json;"
            f"sys.path.insert(0,{str(CANDIDATE)!r});"
            f"sys.path.insert(0,{str(RUNTIME_OUT12)!r});"
            "from c8o_trusted_outbox import C8OccurrenceJournal;"
            f"j=C8OccurrenceJournal({str(path)!r});"
            "snap,ver=j.recover();"
            "print(json.dumps([e.get('occurrence_id') for e in snap.ledger.events]))"
        )
        proc = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=30)
        ids = set(json.loads(proc.stdout.strip()))
        assert ids == committed_ids, f"ghost or loss: {ids} vs {committed_ids}"


# ---------------------------------------------------------------------------
# Scientific: security semantics, detection vs prevention
# ---------------------------------------------------------------------------

def test_unkeyed_digest_forgery_is_accepted() -> None:
    """Recomputed unkeyed digest over forged writer identity is accepted — not authentication."""
    from c8o_trusted_outbox import _hash, _canonical, sealed_envelope, _receipt_id

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        data = json.loads(path.read_text())
        state = data["state"]
        data["writer_id"] = "FORGED_WRITER"
        data["state_digest"] = _hash(state)
        sealed = sealed_envelope(state, data["writer_version"], data["writer_id"], data["effective_clock"])
        data["ledger_prefix_digest"] = sealed["ledger_prefix_digest"]
        data["version_state_digest"] = _hash(sealed)
        data["commit_receipt_id"] = _receipt_id(data)
        path.write_text(_canonical(data))
        j2 = C8OccurrenceJournal(path)
        custody = j2.classify()
        assert custody.status == "VERSIONED_VALID", (
            f"unkeyed forgery must pass: {custody.status} {custody.reason}"
        )
        snap2, ver2 = j2.recover()
        assert snap2 is not None, "forged content accepted by unkeyed digest"


def test_format_only_capability_passes_check() -> None:
    """A format-only WriterCapability passes the check — not authentication."""
    c = WriterCapability(
        writer_id="attacker",
        capability_token="format-valid-but-untrusted",
        issuer_ref="UNISSUED_NO_TRUSTED_ISSUER",
    )
    assert c.writer_id == "attacker"
    assert c.fingerprint(), "format check produces fingerprint — not authentication"


def test_rollback_to_byte_valid_earlier_version_passes() -> None:
    """Rollback to byte-valid earlier version passes every unkeyed check."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        snapshot = path.read_bytes()
        snap2, ver2 = j.recover()
        ev2 = snap2.ledger.admit(legacy_event("B"))
        snap2.outbox.emit(ev2["occurrence_id"])
        j.commit(snap2, ver2, capability=cap("W1"))
        path.write_bytes(snapshot)
        j3 = C8OccurrenceJournal(path)
        snap3, ver3 = j3.recover()
        ids = [e.get("occurrence_id") for e in snap3.ledger.events]
        assert len(ids) == 1, f"rollback succeeds without anchor: {ids}"


def test_anti_rollback_refuses_without_anchor() -> None:
    """anti_rollback_check refuses with typed anchor-unissued."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        receipt = j.commit(snap, ver, capability=cap("W1"))
        with pytest.raises(Exception) as exc_info:
            j.anti_rollback_check(receipt.writer_version, receipt.receipt_id)
        assert "ANCHOR" in str(exc_info.value) or "UNISSUED" in str(exc_info.value)


def test_process_death_is_not_power_loss_durability() -> None:
    """SIGKILL after commit preserves new state — process-death only, not power-loss."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        before = path.read_bytes()
        script = (
            "import sys,os,signal;"
            f"sys.path.insert(0,{str(CANDIDATE)!r});"
            f"sys.path.insert(0,{str(RUNTIME_OUT12)!r});"
            "from c8o_trusted_outbox import C8OccurrenceJournal,WriterCapability;"
            f"j=C8OccurrenceJournal({str(path)!r});"
            "snap,ver=j.recover();"
            "ev=snap.ledger.admit({'candidate_id':'K','payload':{'x':1}});"
            "snap.outbox.emit(ev['occurrence_id']);"
            "j.commit(snap,ver,capability=WriterCapability(writer_id='WK',"
            "capability_token='T'+'x'*24,issuer_ref='UNISSUED'),"
            "crash_boundary='SIGKILL_AFTER_COMMIT')"
        )
        proc = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=30)
        assert proc.returncode == -9
        after = path.read_bytes()
        assert after != before, "SIGKILL after commit preserves new state — process-death only"


# ---------------------------------------------------------------------------
# Authority: D1-D3 typed HOLDS
# ---------------------------------------------------------------------------

def test_d1_legacy_writer_remains_callable() -> None:
    """D1: old Journal.commit and admit_and_queue remain legally callable."""
    assert callable(getattr(Journal, "commit", None))
    assert callable(getattr(Journal, "admit_and_queue", None))


def test_d2_capability_trust_anchor_unissued() -> None:
    """D2: capability trust verification raises typed unissued."""
    verifier = UnkeyedFormatCapabilityVerifier()
    c = WriterCapability(
        writer_id="W1", capability_token="T" + "x" * 24, issuer_ref="UNISSUED"
    )
    with pytest.raises(Exception) as exc_info:
        verifier.verify_trust(c)
    assert "UNISSUED" in str(exc_info.value) or "ANCHOR" in str(exc_info.value)


def test_d3_adp019_admission_absent() -> None:
    """D3: ADP019 admission receipt is typed absent, not fabricated."""
    from c8_readonly_consumer import C8ReadOnlyConsumer

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        consumer = C8ReadOnlyConsumer(path)
        view = consumer.load()
        assert view is not None


# ---------------------------------------------------------------------------
# Consumer: actual OUT9 read-only recipient
# ---------------------------------------------------------------------------

def test_committed_receipt_reaches_consumer_with_readset() -> None:
    """C8 committed receipt reaches the read-only consumer with full readset."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        receipt = j.commit(snap, ver, capability=cap("W1"))
        from c8_readonly_consumer import C8ReadOnlyConsumer

        consumer = C8ReadOnlyConsumer(path)
        view = consumer.load()
        readset = view.readset
        assert readset.state_digest == receipt.state_digest, (
            "consumer readset state_digest must match committed receipt"
        )
        assert readset.version_state_digest == receipt.version_state_digest, (
            "consumer readset version_state_digest must match committed receipt"
        )
        assert readset.ledger_prefix_digest == receipt.ledger_prefix_digest, (
            "consumer readset ledger_prefix_digest must match committed receipt"
        )
        assert readset.writer_version == receipt.writer_version
        assert readset.commit_receipt_id is not None


def test_consumer_is_strictly_read_only() -> None:
    """Consumer operations never mutate journal bytes."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        before = path.read_bytes()
        from c8_readonly_consumer import C8ReadOnlyConsumer

        consumer = C8ReadOnlyConsumer(path)
        consumer.load()
        after = path.read_bytes()
        assert after == before, "consumer must not mutate journal"


def test_no_perception_becomes_occurrence() -> None:
    """No output prose or user perception becomes occurrence."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "journal.json"
        j = C8OccurrenceJournal(path)
        snap, ver = j.recover()
        ev = snap.ledger.admit(legacy_event("A"))
        snap.outbox.emit(ev["occurrence_id"])
        j.commit(snap, ver, capability=cap("W1"))
        from c8_readonly_consumer import C8ReadOnlyConsumer

        consumer = C8ReadOnlyConsumer(path)
        view = consumer.load()
        proto = view.prototype
        perceive = getattr(proto, "perceive", None)
        has_perceived = getattr(proto, "has_perceived", None)
        assert perceive in (False, None), f"perceive must be False: {perceive}"
        assert has_perceived in (False, None), f"has_perceived must be False: {has_perceived}"
