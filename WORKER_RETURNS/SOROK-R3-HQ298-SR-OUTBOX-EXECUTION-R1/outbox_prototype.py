"""SOROK HQ298 SR -- Minimal source-free admission/outbox/projection prototype.

Preserves the distinction between:
  committed objective occurrence
  external emission
  client delivery
  user opportunity to perceive
  actual human perception

No renderer-model calls. No physical-world authority. Source-free only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class OccurrenceState(str, Enum):
    CANDIDATE = "CANDIDATE"
    ADMITTED = "ADMITTED"
    EMITTED = "EMITTED"
    DELIVERED = "DELIVERED"
    PERCEIVED = "PERCEIVED"


class DeliveryState(str, Enum):
    NOT_SENT = "NOT_SENT"
    ADMITTED_UNDELIVERED = "ADMITTED_UNDELIVERED"
    DELIVERED_UNACKED = "DELIVERED_UNACKED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    FAILED = "FAILED"


def _hash(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()


@dataclass
class OccurrenceLedger:
    events: list[dict] = field(default_factory=list)
    _by_id: dict[str, dict] = field(default_factory=dict)

    def admit(self, candidate: dict) -> Optional[dict]:
        """Admit a candidate as an objective occurrence. Returns the ledger event."""
        candidate_id = candidate.get("candidate_id")
        if candidate_id is None:
            return None
        content_hash = _hash(candidate.get("payload", {}))
        existing = self._by_id.get(candidate_id)
        if existing is not None:
            if existing["content_hash"] == content_hash:
                return existing
            return None
        event = {
            "occurrence_id": f"OCC-{len(self.events)+1:04d}",
            "candidate_id": candidate_id,
            "content_hash": content_hash,
            "payload": candidate.get("payload", {}),
            "state": OccurrenceState.ADMITTED.value,
            "source_refs": candidate.get("source_refs", []),
        }
        self.events.append(event)
        self._by_id[candidate_id] = event
        return event

    def get(self, occurrence_id: str) -> Optional[dict]:
        for e in self.events:
            if e["occurrence_id"] == occurrence_id:
                return e
        return None

    def count(self) -> int:
        return len(self.events)


@dataclass
class Outbox:
    deliveries: dict[str, dict] = field(default_factory=dict)

    def emit(self, occurrence_id: str) -> DeliveryState:
        entry = self.deliveries.setdefault(occurrence_id, {
            "state": DeliveryState.NOT_SENT.value,
            "ack_count": 0,
            "attempts": 0,
        })
        if entry["state"] in (DeliveryState.NOT_SENT.value, DeliveryState.FAILED.value):
            entry["state"] = DeliveryState.ADMITTED_UNDELIVERED.value
            entry["attempts"] += 1
        return DeliveryState(entry["state"])

    def deliver(self, occurrence_id: str) -> DeliveryState:
        entry = self.deliveries.get(occurrence_id)
        if entry is None:
            return DeliveryState.NOT_SENT
        if entry["state"] == DeliveryState.ADMITTED_UNDELIVERED.value:
            entry["state"] = DeliveryState.DELIVERED_UNACKED.value
        return DeliveryState(entry["state"])

    def ack(self, occurrence_id: str) -> DeliveryState:
        entry = self.deliveries.get(occurrence_id)
        if entry is None:
            return DeliveryState.NOT_SENT
        if entry["state"] == DeliveryState.DELIVERED_UNACKED.value:
            entry["state"] = DeliveryState.ACKNOWLEDGED.value
            entry["ack_count"] += 1
        return DeliveryState(entry["state"])

    def fail(self, occurrence_id: str) -> DeliveryState:
        entry = self.deliveries.get(occurrence_id)
        if entry is None:
            return DeliveryState.NOT_SENT
        entry["state"] = DeliveryState.FAILED.value
        return DeliveryState(entry["state"])

    def retry(self, occurrence_id: str) -> DeliveryState:
        entry = self.deliveries.get(occurrence_id)
        if entry is None:
            return DeliveryState.NOT_SENT
        if entry["state"] == DeliveryState.FAILED.value:
            entry["state"] = DeliveryState.ADMITTED_UNDELIVERED.value
            entry["attempts"] += 1
        return DeliveryState(entry["state"])


@dataclass
class UserProjection:
    perceived: dict[str, list[str]] = field(default_factory=dict)
    opportunity: dict[str, list[str]] = field(default_factory=dict)

    def offer(self, user_id: str, occurrence_id: str) -> bool:
        self.opportunity.setdefault(user_id, [])
        if occurrence_id not in self.opportunity[user_id]:
            self.opportunity[user_id].append(occurrence_id)
            return True
        return False

    def perceive(self, user_id: str, occurrence_id: str) -> bool:
        self.perceived.setdefault(user_id, [])
        if occurrence_id not in self.perceived[user_id]:
            self.perceived[user_id].append(occurrence_id)
            return True
        return False

    def has_opportunity(self, user_id: str, occurrence_id: str) -> bool:
        return occurrence_id in self.opportunity.get(user_id, [])

    def has_perceived(self, user_id: str, occurrence_id: str) -> bool:
        return occurrence_id in self.perceived.get(user_id, [])


@dataclass
class OutboxPrototype:
    ledger: OccurrenceLedger = field(default_factory=OccurrenceLedger)
    outbox: Outbox = field(default_factory=Outbox)
    projection: UserProjection = field(default_factory=UserProjection)
    world_state: dict = field(default_factory=dict)
    _snapshot: dict = field(default_factory=dict)

    def snapshot(self) -> dict:
        self._snapshot = {
            "ledger": [dict(e) for e in self.ledger.events],
            "outbox": {k: dict(v) for k, v in self.outbox.deliveries.items()},
            "perceived": {k: list(v) for k, v in self.projection.perceived.items()},
            "world": dict(self.world_state),
        }
        return dict(self._snapshot)

    def restore(self, snap: dict) -> None:
        self.ledger.events = snap.get("ledger", [])
        self.ledger._by_id = {e["candidate_id"]: e for e in self.ledger.events}
        self.outbox.deliveries = snap.get("outbox", {})
        self.projection.perceived = snap.get("perceived", {})
        self.world_state = snap.get("world", {})


def make_prototype() -> OutboxPrototype:
    return OutboxPrototype()
