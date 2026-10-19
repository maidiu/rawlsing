"""C8O hostile court C: the accepted Journal.commit writer bypass, actually executed.

The accepted OUT9 `Journal.commit` is a legally callable writer of the same
journal path. It takes no lock, no version precondition and no capability, and
its receipt carries no version envelope. This court runs the bypass as a REAL
separate OS process against a journal that the wrapper has already committed,
records before/after bytes, and enumerates every write entrypoint that a
competent owner would have to restrict. It does NOT claim to close the bypass.
"""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import (  # noqa: E402
    ACCEPTED_STAGE,
    CANDIDATE,
    RET,
    capability,
    cold_reopen,
    legacy,
    spawn,
    write_evidence,
)

from c8o_trusted_outbox import (  # noqa: E402
    LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED,
    C8OccurrenceJournal,
    LegacyWriterBypassDetected,
    VersionStateUnreadable,
)
from outbox_prototype import Journal  # noqa: E402


def _cooperative_committed(tmp_path: Path, n: int = 3):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for i in range(n):
        ev = snap.ledger.admit(legacy(f"W{i}"))
        snap.outbox.emit(ev["occurrence_id"])
    receipt = j.commit(snap, v, capability=capability("COOPERATIVE"))
    return j, receipt


def test_legacy_writer_bypass_destroys_committed_journal_in_a_real_process(tmp_path):
    j, receipt = _cooperative_committed(tmp_path, 3)
    journal = tmp_path / "journal.json"
    before_bytes = journal.read_bytes()
    before_ids = [e["occurrence_id"] for e in Journal(journal).recover().ledger.events]
    assert before_ids == ["OCC-0001", "OCC-0002", "OCC-0003"]
    rows = spawn("legacy", tmp_path, ["ATTACKER"], extra=("fresh_wipe",))
    assert rows and rows[0]["rc"] == 0, rows
    after_bytes = journal.read_bytes()
    assert after_bytes != before_bytes
    after_receipt = json.loads(after_bytes.decode("utf8"))
    assert "writer_version" not in after_receipt
    assert "version_state_digest" not in after_receipt
    surviving = Journal(journal).recover().ledger.events
    assert [e["candidate_id"] for e in surviving] == ["ATTACKER"]
    assert receipt.acknowledged_occurrence_ids == ["OCC-0001", "OCC-0002", "OCC-0003"]
    with pytest.raises(LegacyWriterBypassDetected) as err:
        j.recover()
    assert err.value.code == "LEGACY_WRITER_BYPASS_DETECTED"
    assert err.value.reason == "LEGACY_UNVERSIONED_OVERWRITE"
    detection = j.detect_legacy_bypass()
    assert detection["bypass_detected"] is True
    assert detection["prevention"] == "NOT_POSSIBLE_WITH_CURRENT_LEGAL_CALLABLE_API"
    assert detection["authority_form"] == LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED
    write_evidence(
        "legacy_writer_bypass_counterexample.json",
        {
            "accepted_api": "outbox_prototype.Journal.commit(p)",
            "attacker": {"writer": rows[0]["writer"], "pid": rows[0]["pid"], "rc": rows[0]["rc"]},
            "before": {
                "sha_state": receipt.state_digest,
                "writer_version": receipt.writer_version,
                "occurrence_ids": before_ids,
                "bytes_len": len(before_bytes),
            },
            "after": {
                "occurrence_ids": [e["occurrence_id"] for e in surviving],
                "writer_version_key_present": "writer_version" in after_receipt,
                "bytes_len": len(after_bytes),
            },
            "destroyed_acknowledged_occurrence_ids": before_ids,
            "detection": detection,
            "claim": "DETECTED_AFTER_DESTRUCTION_NOT_PREVENTED",
            "authority_form": LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED,
        },
    )


def test_wrapper_tests_can_be_green_while_the_legacy_bypass_erases_state(tmp_path):
    j, receipt = _cooperative_committed(tmp_path, 2)
    journal = tmp_path / "journal.json"
    green_proof = {
        "wrapper_commit_acknowledged": receipt.acknowledged_occurrence_ids,
        "wrapper_commit_version": receipt.writer_version,
        "wrapper_digest_valid": j.classify().status == "VERSIONED_VALID",
    }
    assert green_proof["wrapper_digest_valid"] is True
    rows = spawn("legacy", tmp_path, ["LATE_WRITER"], extra=("fresh_wipe",))
    assert rows[0]["rc"] == 0
    assert json.loads(journal.read_text(encoding="utf8")).get("writer_version") is None
    surviving = Journal(journal).recover().ledger.events
    assert [e["candidate_id"] for e in surviving] == ["LATE_WRITER"]
    with pytest.raises(LegacyWriterBypassDetected):
        cold_reopen(journal)
    write_evidence(
        "green_wrapper_then_bypass_erasure.json",
        {
            "green_proof": green_proof,
            "after_bypass_occurrence_ids": [e["occurrence_id"] for e in surviving],
            "wrapper_cold_reopen": "LEGACY_WRITER_BYPASS_DETECTED",
            "interpretation": (
                "a green wrapper commit receipt does not bind the legacy writer; "
                "state acknowledged before the bypass is already erased"
            ),
        },
    )


def test_no_competent_accepted_authority_restricts_the_legacy_writer_in_source():
    from c8o_trusted_outbox import C8OccurrenceJournal as C8

    journal_sig = inspect.signature(Journal.commit)
    assert list(journal_sig.parameters) == ["self", "p", "crash_boundary"]
    assert "expected_version" not in journal_sig.parameters
    assert "capability" not in journal_sig.parameters
    admit_sig = inspect.signature(Journal.admit_and_queue)
    assert "expected_version" not in admit_sig.parameters
    assert "capability" not in admit_sig.parameters
    source = (ACCEPTED_STAGE / "outbox_prototype.py").read_text(encoding="utf8")
    for forbidden in ("fcntl", "flock", "writer_version", "LOCK_EX", "os.getuid", "StaleJournal"):
        assert forbidden not in source, forbidden
    prose_only = {
        "capability_occurrences": source.count("capability"),
        "permission_occurrences": source.count("permission"),
        "note": "prose mentions of an external admission decision, not writer gates",
    }
    assert prose_only["capability_occurrences"] == 1
    assert prose_only["permission_occurrences"] == 1
    wrapped = inspect.signature(C8.commit)
    assert "expected_version" in wrapped.parameters
    assert "capability" in wrapped.parameters
    enumeration = {
        "legally_callable_write_entrypoints": [
            {
                "entrypoint": "outbox_prototype.Journal.commit",
                "signature": str(journal_sig),
                "lock": False,
                "version_precondition": False,
                "capability_required": False,
                "restricted_by_competent_authority_in_source": False,
            },
            {
                "entrypoint": "outbox_prototype.Journal.admit_and_queue",
                "signature": str(admit_sig),
                "lock": False,
                "version_precondition": False,
                "capability_required": False,
                "restricted_by_competent_authority_in_source": False,
            },
            {
                "entrypoint": "c8o_trusted_outbox.C8OccurrenceJournal.commit",
                "signature": str(wrapped),
                "lock": True,
                "version_precondition": True,
                "capability_required": True,
                "restricted_by_competent_authority_in_source": False,
                "note": "opt-in discipline only; does not bind the accepted writer",
            },
            {
                "entrypoint": "direct filesystem write / os.replace to the journal path",
                "signature": "OS-level",
                "lock": False,
                "version_precondition": False,
                "capability_required": False,
                "restricted_by_competent_authority_in_source": False,
            },
        ],
        "verdict": "LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED",
        "who_can_close_it": (
            "a competent owner with jurisdiction over the accepted Journal public "
            "interface: deprecate/deny Journal.commit and Journal.admit_and_queue as "
            "writers of this path, or install a capability-checked writer gate; this "
            "worker may not issue or grant that authority"
        ),
    }
    write_evidence("write_entrypoint_enumeration.json", enumeration)
    assert enumeration["verdict"] == LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED


def test_bypass_then_wrapper_recover_is_typed_refusal_not_silent_migration(tmp_path):
    j, _receipt = _cooperative_committed(tmp_path, 1)
    journal = tmp_path / "journal.json"
    spawn("legacy", tmp_path, ["MIGRATOR"])
    with pytest.raises(LegacyWriterBypassDetected):
        j.recover()
    with pytest.raises(LegacyWriterBypassDetected):
        j.recover_custody()
    with pytest.raises(VersionStateUnreadable):
        j.commit(Journal(journal).recover(), 1, capability=capability("X"))
    assert j.detect_legacy_bypass()["code"] == "LEGACY_WRITER_BYPASS_DETECTED"


def test_legacy_bypass_replay_of_old_receipt_is_invisible_without_anchor(tmp_path):
    from c8o_trusted_outbox import TrustedAnchorUnissued

    j, receipt = _cooperative_committed(tmp_path, 2)
    journal = tmp_path / "journal.json"
    snapshot = journal.read_bytes()
    j2 = C8OccurrenceJournal(journal)
    snap, v = j2.recover()
    assert v == 1
    ev = snap.ledger.admit(legacy("LATER"))
    snap.outbox.emit(ev["occurrence_id"])
    later = j2.commit(snap, v, capability=capability("LATER"))
    assert later.writer_version == 2
    (tmp_path / "old.json").write_bytes(snapshot)
    rows = spawn("rollback", tmp_path, ["ROLLBACKER"], extra=(str(tmp_path / "old.json"),))
    assert rows[0]["rc"] == 0, rows
    rolled_back_p, rolled_back_v, custody = C8OccurrenceJournal(journal).recover_custody()
    assert custody.status == "VERSIONED_VALID"
    assert rolled_back_v == 1
    assert rolled_back_p.ledger.count() == 2
    with pytest.raises(TrustedAnchorUnissued):
        j2.anti_rollback_check(rolled_back_v, custody.receipt_id)
    write_evidence(
        "legacy_receipt_rollback_without_anchor.json",
        {
            "anchored_receipt": later.to_json(),
            "rolled_back_writer_version": rolled_back_v,
            "rolled_back_occurrence_ids": [e["occurrence_id"] for e in rolled_back_p.ledger.events],
            "detectable_by_unkeyed_digest": False,
            "detectable_without_trusted_anchor": False,
            "authority_form": "C8_TRUSTED_ANCHOR_UNISSUED",
        },
    )


def test_interleaved_legacy_commit_loses_the_cooperative_event(tmp_path):
    j, _receipt = _cooperative_committed(tmp_path, 1)
    journal = tmp_path / "journal.json"
    stale = Journal(journal).recover()
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("COOPERATIVE"))
    snap.outbox.emit(ev["occurrence_id"])
    j.commit(snap, v, capability=capability("COOPERATIVE"))
    attacker_ev = stale.ledger.admit(legacy("ATTACKER"))
    stale.outbox.emit(attacker_ev["occurrence_id"])
    Journal(journal).commit(stale)
    surviving = [e["candidate_id"] for e in Journal(journal).recover().ledger.events]
    assert "COOPERATIVE" not in surviving
    assert "ATTACKER" in surviving
    write_evidence(
        "interleaved_legacy_lost_event.json",
        {
            "lost_candidate": "COOPERATIVE",
            "surviving_candidates": surviving,
            "mechanism": "accepted Journal.commit is whole-file last-writer-wins with no version precondition",
        },
    )
