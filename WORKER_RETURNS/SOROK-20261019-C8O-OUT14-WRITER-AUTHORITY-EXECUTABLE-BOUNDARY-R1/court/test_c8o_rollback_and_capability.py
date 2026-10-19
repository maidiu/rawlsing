"""C8O hostile court D: unkeyed digests, capability separation and rollback reality.

Demonstrates why a recomputable unkeyed digest cannot authenticate a writer and
cannot prevent rollback to an earlier valid journal without a separately trusted
anchor. These are falsifying counterexamples against any security reading of
`state_digest` / `version_state_digest` / capability fingerprints.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import capability, legacy, spawn, write_evidence  # noqa: E402

from c8o_trusted_outbox import (  # noqa: E402
    ANTI_ROLLBACK_WITHOUT_ANCHOR,
    CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION,
    SECURITY_CLAIM_NOT_PROVED,
    AnchorRollbackDetected,
    C8OccurrenceJournal,
    FileBackedMonotonicAnchor,
    TrustedAnchorUnissued,
    UnkeyedFormatCapabilityVerifier,
    WriterCapability,
    forged_receipt,
)
from outbox_prototype import Journal, make_prototype  # noqa: E402


def _seed(tmp_path: Path, labels=("A",), writer="SEED"):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for label in labels:
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
    receipt = j.commit(snap, v, capability=capability(writer))
    return j, receipt


def test_recomputed_unkeyed_digest_is_not_writer_authentication(tmp_path):
    j, receipt = _seed(tmp_path, ("A",))
    journal = tmp_path / "journal.json"
    original = json.loads(journal.read_text(encoding="utf8"))
    forged = dict(original)
    forged["writer_version"] = 10
    forged["writer_id"] = "FORGED_WRITER"
    forged["capability_fingerprint"] = "f" * 64
    journal.write_text(forged_receipt(forged), encoding="utf8")
    p, v, custody = C8OccurrenceJournal(journal).recover_custody()
    assert custody.status == "VERSIONED_VALID"
    assert v == 10 and custody.writer_id == "FORGED_WRITER"
    write_evidence(
        "unkeyed_digest_forgery_counterexample.json",
        {
            "original_writer_id": receipt.writer_id,
            "original_writer_version": receipt.writer_version,
            "forged_writer_id": custody.writer_id,
            "forged_writer_version": v,
            "digest_recomputed": True,
            "accepted_reader_verdict": custody.status,
            "security_claim": SECURITY_CLAIM_NOT_PROVED,
            "meaning": "unkeyed digest detects accidental corruption only, never forgery by a writer-capable actor",
        },
    )


def test_mutated_history_with_recomputed_digests_is_accepted(tmp_path):
    from outbox_prototype import _hash as _h

    j, receipt = _seed(tmp_path, ("A", "B"))
    journal = tmp_path / "journal.json"
    original = json.loads(journal.read_text(encoding="utf8"))
    mutated = json.loads(json.dumps(original))
    event = mutated["state"]["ledger"][0]
    event["payload"]["utterance"] = "REWROTE-HISTORY"
    event["content_hash"] = _h(event["payload"])
    event["identity_preimage"]["payload"]["utterance"] = "REWROTE-HISTORY"
    event["identity_digest"] = _h(event["identity_preimage"])
    journal.write_text(forged_receipt(mutated), encoding="utf8")
    p, v, custody = C8OccurrenceJournal(journal).recover_custody()
    assert custody.status == "VERSIONED_VALID"
    assert p.ledger.events[0]["payload"]["utterance"] == "REWROTE-HISTORY"
    write_evidence(
        "history_rewrite_counterexample.json",
        {
            "occurrence_ids": [e["occurrence_id"] for e in p.ledger.events],
            "rewritten_payload": p.ledger.events[0]["payload"],
            "recomputed": ["content_hash", "identity_digest", "state_digest", "version_state_digest", "commit_receipt_id"],
            "accepted_reader_verdict": custody.status,
            "security_claim": SECURITY_CLAIM_NOT_PROVED,
            "meaning": "any actor allowed to rewrite the file can rewrite history and recompute every unkeyed digest",
        },
    )


def test_capability_format_check_is_not_writer_authentication(tmp_path):
    verifier = UnkeyedFormatCapabilityVerifier()
    honest = capability("HONEST")
    assert verifier.present(honest)
    with pytest.raises(Exception):
        verifier.verify_trust(honest)
    forged = WriterCapability(
        writer_id="FORGED",
        capability_token="x" * 32,
        issuer_ref="SELF_SIGNED_NOT_AN_ISSUER",
    )
    assert verifier.present(forged)
    assert verifier.trust_grade == CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("FORGED"))
    snap.outbox.emit(ev["occurrence_id"])
    receipt = j.commit(snap, v, capability=forged)
    assert receipt.writer_id == "FORGED"
    assert receipt.capability_trust_grade == CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION
    assert receipt.anti_rollback_grade == ANTI_ROLLBACK_WITHOUT_ANCHOR
    write_evidence(
        "capability_format_not_authentication.json",
        {
            "forged_capability_accepted": True,
            "trust_grade": receipt.capability_trust_grade,
            "authority_form": "C8_CAPABILITY_TRUST_ANCHOR_UNISSUED",
            "security_claim": SECURITY_CLAIM_NOT_PROVED,
        },
    )


def test_without_trusted_anchor_anti_rollback_claim_is_refused(tmp_path):
    j, receipt = _seed(tmp_path, ("A",))
    with pytest.raises(TrustedAnchorUnissued) as err:
        j.anti_rollback_check(receipt.writer_version, receipt.receipt_id)
    assert err.value.code == "C8_TRUSTED_ANCHOR_UNISSUED"
    assert receipt.anti_rollback_grade == ANTI_ROLLBACK_WITHOUT_ANCHOR


def test_rollback_to_earlier_valid_receipt_is_undetectable_without_anchor_and_detectable_with_one(tmp_path):
    journal = tmp_path / "journal.json"
    anchor = FileBackedMonotonicAnchor(tmp_path / "anchor.json")
    j = C8OccurrenceJournal(journal, anchor=anchor)
    snap, v = j.recover()
    for label in ("A", "B", "C"):
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
    first = j.commit(snap, v, capability=capability("W"))
    assert first.writer_version == 1
    snapshot_v1 = journal.read_bytes()
    snap2, v2 = j.recover()
    ev = snap2.ledger.admit(legacy("D"))
    snap2.outbox.emit(ev["occurrence_id"])
    second = j.commit(snap2, v2, capability=capability("W"))
    assert second.writer_version == 2
    snap3, v3 = j.recover()
    ev = snap3.ledger.admit(legacy("E"))
    snap3.outbox.emit(ev["occurrence_id"])
    third = j.commit(snap3, v3, capability=capability("W"))
    assert third.writer_version == 3
    j.anti_rollback_check(third.writer_version, third.receipt_id)
    journal.write_bytes(snapshot_v1)
    p, v, custody = C8OccurrenceJournal(journal).recover_custody()
    assert custody.status == "VERSIONED_VALID"
    assert v == 1
    with pytest.raises(AnchorRollbackDetected) as err:
        j.anti_rollback_check(v, custody.receipt_id)
    assert err.value.code == "ANCHOR_ROLLBACK_DETECTED"
    write_evidence(
        "rollback_detected_only_by_external_anchor.json",
        {
            "anchor_receipts": anchor.latest(),
            "rolled_back_writer_version": v,
            "rolled_back_receipt_id": custody.receipt_id,
            "unkeyed_digest_accepts_rollback": True,
            "anchor_detects_rollback": True,
            "anchor_grade": anchor.grade,
            "authority_form": "TEST_FIXTURE_ONLY_LOCAL_ANCHOR_NOT_OWNER_ISSUED",
        },
    )


def test_anchor_observation_is_monotone(tmp_path):
    anchor = FileBackedMonotonicAnchor(tmp_path / "anchor.json")
    anchor.observe(1, "r1")
    anchor.observe(2, "r2")
    with pytest.raises(AnchorRollbackDetected):
        anchor.observe(1, "r1")
    with pytest.raises(AnchorRollbackDetected):
        anchor.check(1, "r1")
    assert anchor.latest() == [2, "r2"]


def test_forged_receipt_helper_is_the_documented_counterexample_tool():
    source = Path(__file__).resolve().parent.parent / "candidate" / "c8o_trusted_outbox.py"
    text = source.read_text(encoding="utf8")
    assert "def forged_receipt" in text
    assert "unkeyed" in text
