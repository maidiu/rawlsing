"""SOROK C8O — maximal lawful C8 committed-receipt to read-only downstream consumer.

Binds the byte-exact committed C8 occurrence/journal receipt to ONE existing
lawful C8 read-only recipient: the accepted OUT9 `UserProjection`/`Outbox`
viewer-client path inside `outbox_prototype` (blob 331840768ce0b5f6f73e5e93094ca0d217ddaebf).
That recipient is prototype fixture state: `perceive`/`has_perceived` always
return False and no human perception owner is imported. This consumer never
manufactures an actor, an admitted encounter, a perception witness or an
ADP019 admission.

Typed absences (NOT issuance, NOT a grant):
  ADP019_ADMISSION_RECEIPT_ABSENT  - no V3_EXTERNAL_ADMISSION_RECEIPT exists;
                                     the worker may not issue one.
  C9_LATER_ACTION_CONSUMER_UNBOUND - the C9P native later-action consumer is a
                                     separate owner-gated campaign; the exact
                                     C8->C9 receiving interface request is
                                     exposed instead of a claimed binding.

Read discipline: every view is rebuilt from an exact canonical byte re-read of
the journal file. The returned readset carries the digests the consumer
actually read so a same-named upstream severance can turn the same assertion
RED instead of crashing.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from outbox_prototype import OutboxPrototype, durable_delivery_id, make_prototype, _canonical, _hash

from c8o_trusted_outbox import (
    C8OccurrenceJournal,
    LegacyWriterBypassDetected,
    VersionStateUnreadable,
)

ADP019_ADMISSION_RECEIPT_ABSENT = "ADP019_ADMISSION_RECEIPT_ABSENT"
C9_LATER_ACTION_CONSUMER_UNBOUND = "C9_LATER_ACTION_CONSUMER_UNBOUND"
OWNER_IDENTITY_MISMATCH = "OWNER_IDENTITY_MISMATCH"
CONSUMER_READ_ONLY = "CONSUMER_READ_ONLY"
SOURCE_SEVERED = "SOURCE_SEVERED"


class OwnerIdentityMismatch(ValueError):
    def __init__(self, expected, actual) -> None:
        super().__init__(f"OWNER_IDENTITY_MISMATCH expected={expected} actual={actual}")
        self.code = OWNER_IDENTITY_MISMATCH
        self.expected = expected
        self.actual = actual


@dataclass
class C8Readset:
    journal_path: str
    canonical_bytes_sha256: str
    state_digest: str
    version_state_digest: str
    ledger_prefix_digest: str
    writer_version: int
    writer_id: Optional[str]
    commit_receipt_id: Optional[str]
    occurrence_ids: list

    def to_json(self) -> dict:
        return {
            "journal_path": self.journal_path,
            "canonical_bytes_sha256": self.canonical_bytes_sha256,
            "state_digest": self.state_digest,
            "version_state_digest": self.version_state_digest,
            "ledger_prefix_digest": self.ledger_prefix_digest,
            "writer_version": self.writer_version,
            "writer_id": self.writer_id,
            "commit_receipt_id": self.commit_receipt_id,
            "occurrence_ids": list(self.occurrence_ids),
        }


@dataclass
class C8CommittedView:
    prototype: OutboxPrototype
    readset: C8Readset
    events: list = field(default_factory=list)

    def count(self) -> int:
        return len(self.events)

    def get(self, occurrence_id: str) -> Optional[dict]:
        return self.prototype.ledger.get(occurrence_id)

    def owner_identity(self, occurrence_id: str) -> dict:
        event = self.prototype.ledger.get(occurrence_id)
        if event is None:
            raise KeyError(occurrence_id)
        return {
            "occurrence_id": event.get("occurrence_id"),
            "candidate_id": event.get("candidate_id"),
            "issuer_ref": event.get("issuer_ref"),
            "authority_ref": event.get("authority_ref"),
            "participant_refs": event.get("participant_refs"),
            "source_refs": event.get("source_refs"),
            "admission_grade": event.get("admission_grade"),
        }


class C8ReadOnlyConsumer:
    """Read-only downstream consumer of the committed C8 journal receipt."""

    def __init__(
        self,
        journal_path,
        *,
        expected_owner_identity: Optional[dict] = None,
        viewer_id: Optional[str] = None,
    ) -> None:
        self.journal_path = Path(journal_path)
        self.expected_owner_identity = expected_owner_identity
        self.viewer_id = viewer_id
        self._view: Optional[C8CommittedView] = None

    def load(self) -> C8CommittedView:
        raw = self.journal_path.read_bytes()
        self._assert_byte_exact(raw)
        view = self._build_view(raw)
        self._check_owner_identity(view)
        self._view = view
        return view

    def _assert_byte_exact(self, raw: bytes) -> None:
        text = raw.decode("utf8")
        receipt = json.loads(text)
        if _canonical(receipt) != text:
            raise VersionStateUnreadable(self.journal_path, "NONCANONICAL_RECEIPT")
        custody = C8OccurrenceJournal(self.journal_path).classify()
        if custody.status != "VERSIONED_VALID":
            if custody.status == "LEGACY_UNVERSIONED_OVERWRITE":
                raise LegacyWriterBypassDetected(self.journal_path)
            raise VersionStateUnreadable(self.journal_path, custody.reason or "UNREADABLE")

    def _build_view(self, raw: bytes) -> C8CommittedView:
        receipt = json.loads(raw.decode("utf8"))
        state = receipt["state"]
        if receipt["state_digest"] != _hash(state):
            raise VersionStateUnreadable(self.journal_path, "STATE_DIGEST_MISMATCH")
        prototype = make_prototype()
        prototype.restore(state)
        readset = C8Readset(
            journal_path=str(self.journal_path),
            canonical_bytes_sha256=_hash(raw.decode("utf8")),
            state_digest=receipt["state_digest"],
            version_state_digest=receipt["version_state_digest"],
            ledger_prefix_digest=receipt["ledger_prefix_digest"],
            writer_version=receipt["writer_version"],
            writer_id=receipt.get("writer_id"),
            commit_receipt_id=receipt.get("commit_receipt_id"),
            occurrence_ids=[e.get("occurrence_id") for e in state.get("ledger", [])],
        )
        return C8CommittedView(prototype=prototype, readset=readset, events=list(state.get("ledger", [])))

    def _check_owner_identity(self, view: C8CommittedView) -> None:
        if self.expected_owner_identity is None:
            return
        for occurrence_id, expected in self.expected_owner_identity.items():
            actual = view.owner_identity(occurrence_id)
            for key, value in expected.items():
                if actual.get(key) != value:
                    raise OwnerIdentityMismatch({key: value}, {key: actual.get(key)})

    def readset(self) -> dict:
        if self._view is None:
            self.load()
        return self._view.readset.to_json()

    def committed_state_digest(self) -> str:
        if self._view is None:
            self.load()
        return self._view.readset.state_digest

    def recipient_has_opportunity(self, user_id: str, occurrence_id: str) -> bool:
        if self._view is None:
            self.load()
        return self._view.prototype.projection.has_opportunity(user_id, occurrence_id)

    def client_delivery_receipt(self, occurrence_id: str, viewer_id: Optional[str] = None) -> Optional[dict]:
        viewer = viewer_id or self.viewer_id
        if self._view is None:
            self.load()
        key = durable_delivery_id(occurrence_id, viewer)
        return self._view.prototype.outbox.client_deliveries.get(key)
    def adp019_admission_receipt(self) -> dict:
        return {
            "status": ADP019_ADMISSION_RECEIPT_ABSENT,
            "reason": "WORKER_NOT_ADP019_ISSUER",
            "owner": "V3 External Admission Court (ADP019)",
            "action": "owner must admit the exact precipitating occurrence and emit V3_EXTERNAL_ADMISSION_RECEIPT",
        }

    def c9_later_action_receiving_interface_request(self) -> dict:
        return {
            "status": C9_LATER_ACTION_CONSUMER_UNBOUND,
            "interface": "C8_COMMITTED_OCCURRENCE_RECEIPT",
            "requires": [
                "byte-exact committed journal receipt readset (state_digest, version_state_digest, ledger_prefix_digest, commit_receipt_id)",
                "event/actor/action owner identity bound to the admitted occurrence",
                "ADP019 admission receipt for the precipitating occurrence",
                "distinct native C9 authority for person x event consequences",
            ],
            "owner_action": (
                "C9P owner binds LaterActionConsumer.read_target (or successor named "
                "consumer) to this C8 readset and issues native C9 authority; this "
                "worker issues nothing"
            ),
        }

    def assert_read_only_against(self, before_bytes: bytes) -> None:
        after = self.journal_path.read_bytes()
        if after != before_bytes:
            raise AssertionError("CONSUMER_READ_ONLY_VIOLATION: journal bytes changed under a read-only consumer")
