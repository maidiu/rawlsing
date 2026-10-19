"""Actor identity, activation and standing-state ingress (ADP007/ADP008 seam).

Ingress is fail-closed: every refusal is a typed result, never a fabricated actor.
Demographic, identity or structural fields never become psychological state; a
record that carries belief, affect, trait or capability-claim content is refused
with `ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS`.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .canon import canonical, digest, seal, valid

ACTOR_RECORD_SCHEMA = "C9P_ACTOR_IDENTITY_RECORD@1"

# Fields that would convert identity or structural position into psychology.
PSYCHOLOGY_CLAIM_KEYS = frozenset(
    {
        "beliefs",
        "affect",
        "emotions",
        "traits",
        "personality",
        "motives",
        "desires",
        "intentions",
        "knowledge",
        "memories",
        "competence_estimate",
        "propensity",
        "attachment",
        "wound",
    }
)


class IngressStatus(str, Enum):
    ADMITTED = "ADMITTED"
    REFUSED = "REFUSED"


class IngressReason(str, Enum):
    OK = "OK"
    ACTOR_ID_MISSING = "ACTOR_ID_MISSING"
    ACTOR_ID_INVALID_TYPE = "ACTOR_ID_INVALID_TYPE"
    ACTIVATION_STATUS_MISSING = "ACTIVATION_STATUS_MISSING"
    ACTOR_NOT_ACTIVE = "ACTOR_NOT_ACTIVE"
    STANDING_STATE_MISSING = "STANDING_STATE_MISSING"
    STANDING_STATE_STALE = "STANDING_STATE_STALE"
    SOURCE_REF_MISSING = "SOURCE_REF_MISSING"
    SOURCE_HASH_MISSING = "SOURCE_HASH_MISSING"
    RECORD_INTEGRITY_FAILURE = "RECORD_INTEGRITY_FAILURE"
    ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS = "ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"


@dataclass(frozen=True)
class ActorIdentityRecord:
    """One source-custodied actor identity record presented at ingress."""

    actor_id: str
    activation_status: str
    standing_state: str
    currentness_as_of: int
    source_ref: str
    source_hash: str
    schema: str = ACTOR_RECORD_SCHEMA

    def sealed(self) -> dict:
        return seal(
            {
                "schema": self.schema,
                "actor_id": self.actor_id,
                "activation_status": self.activation_status,
                "standing_state": self.standing_state,
                "currentness_as_of": self.currentness_as_of,
                "source_ref": self.source_ref,
                "source_hash": self.source_hash,
            }
        )


@dataclass(frozen=True)
class ActorIngressResult:
    """Typed ingress outcome. `actor_id` is empty unless status is ADMITTED."""

    status: IngressStatus
    reason: IngressReason
    actor_id: str
    standing_state: str
    currentness_as_of: int
    source_ref: str
    readset_refs: tuple[str, ...]
    record_hash: str

    @property
    def admitted(self) -> bool:
        return self.status is IngressStatus.ADMITTED


def _has_psychology_claim(raw: Mapping[str, Any]) -> str | None:
    for key in raw:
        if key in PSYCHOLOGY_CLAIM_KEYS:
            return key
    return None


def ingress_actor(raw: Mapping[str, Any], *, as_of: int) -> ActorIngressResult:
    """Validate one actor identity record at time `as_of`.

    The raw record must be a sealed mapping with schema `C9P_ACTOR_IDENTITY_RECORD@1`.
    Returns a typed refusal on any missing, stale, unsealed or psychology-bearing
    record. An admitted result's readset binds the exact source reference and hash.
    """
    empty = ActorIngressResult(
        status=IngressStatus.REFUSED,
        reason=IngressReason.RECORD_INTEGRITY_FAILURE,
        actor_id="",
        standing_state="",
        currentness_as_of=0,
        source_ref="",
        readset_refs=(),
        record_hash="",
    )
    if not isinstance(raw, Mapping):
        return empty
    claim_key = _has_psychology_claim(raw)
    if claim_key is not None:
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash="",
        )
    if raw.get("schema") != ACTOR_RECORD_SCHEMA:
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.SCHEMA_MISMATCH,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash="",
        )
    if not valid(raw):
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.RECORD_INTEGRITY_FAILURE,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash="",
        )
    actor_id = raw.get("actor_id")
    if not isinstance(actor_id, str) or not actor_id.strip():
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.ACTOR_ID_MISSING
            if actor_id is None
            else IngressReason.ACTOR_ID_INVALID_TYPE,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    activation = raw.get("activation_status")
    if not isinstance(activation, str) or not activation.strip():
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.ACTIVATION_STATUS_MISSING,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    if activation != "ACTIVE":
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.ACTOR_NOT_ACTIVE,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    standing = raw.get("standing_state")
    if not isinstance(standing, str) or not standing.strip():
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.STANDING_STATE_MISSING,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    currentness = raw.get("currentness_as_of")
    if not isinstance(currentness, int) or isinstance(currentness, bool):
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.STANDING_STATE_STALE,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    if currentness > as_of:
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.STANDING_STATE_STALE,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    source_ref = raw.get("source_ref")
    if not isinstance(source_ref, str) or not source_ref.strip():
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.SOURCE_REF_MISSING,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    source_hash = raw.get("source_hash")
    if not isinstance(source_hash, str) or not source_hash.strip():
        return ActorIngressResult(
            status=IngressStatus.REFUSED,
            reason=IngressReason.SOURCE_HASH_MISSING,
            actor_id="",
            standing_state="",
            currentness_as_of=0,
            source_ref="",
            readset_refs=(),
            record_hash=raw.get("hash", ""),
        )
    record_hash = raw["hash"]
    return ActorIngressResult(
        status=IngressStatus.ADMITTED,
        reason=IngressReason.OK,
        actor_id=actor_id,
        standing_state=standing,
        currentness_as_of=currentness,
        source_ref=source_ref,
        readset_refs=(source_ref,),
        record_hash=record_hash,
    )


def actor_record_hash(record: Mapping[str, Any]) -> str:
    """Return the sealed identity digest of one actor record."""
    return digest({k: v for k, v in record.items() if k != "hash"})


__all__ = [
    "ACTOR_RECORD_SCHEMA",
    "ActorIdentityRecord",
    "ActorIngressResult",
    "IngressReason",
    "IngressStatus",
    "actor_record_hash",
    "canonical",
    "ingress_actor",
    "seal",
    "valid",
]
