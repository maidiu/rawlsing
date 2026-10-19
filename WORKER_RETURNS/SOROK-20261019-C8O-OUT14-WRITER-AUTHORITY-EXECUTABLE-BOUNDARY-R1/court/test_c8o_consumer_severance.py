"""C8O hostile court E: committed C8 receipt to the actual read-only downstream consumer.

Binds the byte-exact committed journal receipt to the accepted OUT9
`UserProjection`/`Outbox` read-only recipient path and to typed absences for
ADP019 admission and the C9 later-action consumer. Same-named severance
witnesses live in `court/test_c8o_consumer_severance.py.proof.json` and are
executed by the shared CROSS_HQ proof-integrity gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import capability, legacy  # noqa: E402

from c8_readonly_consumer import (  # noqa: E402
    ADP019_ADMISSION_RECEIPT_ABSENT,
    C9_LATER_ACTION_CONSUMER_UNBOUND,
    C8ReadOnlyConsumer,
    OwnerIdentityMismatch,
)
from c8o_trusted_outbox import (  # noqa: E402
    AcknowledgedPrefixRewriteRefused,
    C8OccurrenceJournal,
    LegacyWriterBypassDetected,
    VersionStateUnreadable,
    forged_receipt,
)
from outbox_prototype import Journal, _canonical, _hash, make_prototype  # noqa: E402


def _committed_journal(tmp_path: Path, labels=("W0", "W1"), viewer="U1", writer="W0"):
    j = C8OccurrenceJournal(tmp_path / "journal.json")
    snap, v = j.recover()
    for label in labels:
        ev = snap.ledger.admit(legacy(label))
        snap.outbox.emit(ev["occurrence_id"])
        assert snap.outbox.authorize_viewer(ev["occurrence_id"], viewer) is True
        assert snap.outbox.emit_to(ev["occurrence_id"], viewer) is not None
        assert snap.outbox.deliver_to(ev["occurrence_id"], viewer) is not None
        assert snap.projection.offer(viewer, ev["occurrence_id"]) is True
    receipt = j.commit(snap, v, capability=capability(writer))
    return j, receipt


def test_consumer_reads_exact_committed_source(tmp_path):
    j, receipt = _committed_journal(tmp_path)
    journal = tmp_path / "journal.json"
    consumer = C8ReadOnlyConsumer(journal)
    view = consumer.load()
    raw = json.loads(journal.read_text(encoding="utf8"))
    assert view.events == raw["state"]["ledger"]
    assert consumer.readset()["state_digest"] == _hash(raw["state"])
    assert consumer.readset()["occurrence_ids"] == ["OCC-0001", "OCC-0002"]
    assert consumer.committed_state_digest() == receipt.state_digest


def test_consumer_readset_matches_independently_recomputed_digests(tmp_path):
    j, receipt = _committed_journal(tmp_path)
    journal = tmp_path / "journal.json"
    consumer = C8ReadOnlyConsumer(journal)
    consumer.load()
    raw = json.loads(journal.read_text(encoding="utf8"))
    readset = consumer.readset()
    assert readset["version_state_digest"] == raw["version_state_digest"]
    assert readset["ledger_prefix_digest"] == raw["ledger_prefix_digest"]
    assert readset["commit_receipt_id"] == raw["commit_receipt_id"]
    assert readset["writer_version"] == receipt.writer_version


def test_consumer_owner_identity_mismatch_is_typed(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0",))
    journal = tmp_path / "journal.json"
    consumer = C8ReadOnlyConsumer(
        journal,
        expected_owner_identity={"OCC-0001": {"candidate_id": "W0"}},
    )
    view = consumer.load()
    assert view.owner_identity("OCC-0001")["candidate_id"] == "W0"
    bad = C8ReadOnlyConsumer(
        journal,
        expected_owner_identity={"OCC-0001": {"candidate_id": "NOT-W0"}},
    )
    with pytest.raises(OwnerIdentityMismatch) as err:
        bad.load()
    assert err.value.code == "OWNER_IDENTITY_MISMATCH"


def test_consumer_refuses_unreadable_source(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0",))
    journal = tmp_path / "journal.json"
    raw = json.loads(journal.read_text(encoding="utf8"))
    raw["writer_version"] = "CORRUPT"
    journal.write_text(_canonical(raw), encoding="utf8")
    with pytest.raises(VersionStateUnreadable) as err:
        C8ReadOnlyConsumer(journal).load()
    assert err.value.code == "VERSION_STATE_UNREADABLE"


def test_consumer_refuses_legacy_overwritten_source(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0",))
    journal = tmp_path / "journal.json"
    Journal(journal).commit(Journal(journal).recover())
    with pytest.raises(VersionStateUnreadable) as err:
        C8ReadOnlyConsumer(journal).load()
    assert err.value.code == "LEGACY_WRITER_BYPASS_DETECTED"
    assert isinstance(err.value, LegacyWriterBypassDetected)


def test_consumer_operations_are_read_only(tmp_path):
    j, receipt = _committed_journal(tmp_path)
    journal = tmp_path / "journal.json"
    consumer = C8ReadOnlyConsumer(journal, viewer_id="U1")
    before = journal.read_bytes()
    consumer.load()
    assert consumer.recipient_has_opportunity("U1", "OCC-0001") is True
    delivery = consumer.client_delivery_receipt("OCC-0001")
    assert delivery is not None and delivery["event_id"] == "OCC-0001"
    assert delivery["state"] == "DELIVERED_UNACKED"
    consumer.assert_read_only_against(before)
    assert journal.read_bytes() == before


def test_consumer_typed_absences_are_not_issuance(tmp_path):
    j, receipt = _committed_journal(tmp_path)
    consumer = C8ReadOnlyConsumer(tmp_path / "journal.json")
    consumer.load()
    adp = consumer.adp019_admission_receipt()
    assert adp["status"] == ADP019_ADMISSION_RECEIPT_ABSENT
    assert adp["owner"] == "V3 External Admission Court (ADP019)"
    c9 = consumer.c9_later_action_receiving_interface_request()
    assert c9["status"] == C9_LATER_ACTION_CONSUMER_UNBOUND
    assert c9["interface"] == "C8_COMMITTED_OCCURRENCE_RECEIPT"
    assert any("ADP019" in r for r in c9["requires"])


def test_valid_empty_commit_preserves_other_writers_committed_source(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0", "W1"))
    journal = tmp_path / "journal.json"
    consumer = C8ReadOnlyConsumer(journal)
    before_view = consumer.load()
    before_ids = consumer.readset()["occurrence_ids"]
    empty = make_prototype()
    _p, ver = j.recover()
    with pytest.raises(AcknowledgedPrefixRewriteRefused):
        j.commit(empty, ver, capability=capability("EMPTY"))
    after = C8ReadOnlyConsumer(journal).load()
    assert after.events == before_view.events
    assert C8ReadOnlyConsumer(journal).readset()["occurrence_ids"] == before_ids


def test_replay_at_consumer_creates_no_duplicate_or_out_of_order_ghost(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0", "W1"))
    journal = tmp_path / "journal.json"
    snap, v = j.recover()
    again = snap.ledger.admit(legacy("W0"))
    assert again["occurrence_id"] == "OCC-0001"
    j.commit(snap, v, capability=capability("W0"))
    consumer = C8ReadOnlyConsumer(journal)
    view = consumer.load()
    ids = consumer.readset()["occurrence_ids"]
    assert ids == ["OCC-0001", "OCC-0002"]
    assert len(ids) == len(set(ids))
    assert [e["occurrence_id"] for e in view.events] == ids


def test_consumer_sees_forged_receipt_as_valid_until_owner_or_anchor_acts(tmp_path):
    j, receipt = _committed_journal(tmp_path, labels=("W0",))
    journal = tmp_path / "journal.json"
    forged = json.loads(journal.read_text(encoding="utf8"))
    forged["writer_id"] = "FORGED"
    journal.write_text(forged_receipt(forged), encoding="utf8")
    consumer = C8ReadOnlyConsumer(journal)
    view = consumer.load()
    assert view.readset.writer_id == "FORGED"
    assert consumer.adp019_admission_receipt()["status"] == ADP019_ADMISSION_RECEIPT_ABSENT
