"""Shared ABI. State changes and scientific decisions belong to the supplied owner.

Engine-owned history records outcomes. It never applies psychological deltas.
An owner must resolve a repeated operation_id from its durable receipt or refuse
it as ambiguous. It must never repeat a possibly committed effect blindly.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol


class RecursionRefusal(ValueError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def detached(value: Any) -> Any:
    return json.loads(canonical(value))


@dataclass(frozen=True)
class StateIdentity:
    root: str
    actor: str
    branch: str
    clock: int
    state_hash: str

    def document(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class EventProposal:
    event_id: str
    event_time: int
    operation: str
    source_refs: tuple[str, ...]
    participants: tuple[str, ...]
    circumstances: Mapping[str, Any]
    interval: Mapping[str, Any] | None = None

    def document(self) -> dict:
        return detached(asdict(self))


@dataclass(frozen=True)
class RealizedEvent:
    operation_id: str
    proposal_hash: str
    before: StateIdentity
    after: StateIdentity
    status: str
    objective: Mapping[str, Any]
    accessible: Mapping[str, Any]
    consequences: Mapping[str, Any]
    readset: tuple[str, ...]
    receipt_ref: str

    def document(self) -> dict:
        return detached(asdict(self))


class DevelopmentOwner(Protocol):
    """Version-selected actor/world boundary, including owner-governed time.

    validate_proposal is read-only and checks sources, chronology, participants
    and operation authority. realize validates expected identity before effects.
    Its result describes interval and event outcomes in their actual order.
    Missing science is HELD/MISSING_RULE, never an evaluated NO_CHANGE.
    No fixed source, event, participant or answer identifiers belong in the engine.
    """

    def snapshot(self) -> StateIdentity: ...

    def validate_proposal(self, proposal: EventProposal) -> None: ...

    def realize(self, operation_id: str, proposal: EventProposal,
                expected: StateIdentity) -> RealizedEvent: ...


class CallProvider(Protocol):
    """Receives detached actor-accessible history, never a state writer.

    request.mode is BOOTSTRAP, ORDINARY or TERMINAL. response has retrospective
    and prospective keys. retrospective is null only on bootstrap. Otherwise
    it binds batch_id, history_hash, ordered event_ids and proposed impressions.
    Prospective contains 3–5 EventProposal documents, or is null on terminal.
    Impressions are render proposals with provenance, not canonical psychology.
    """

    def call(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
