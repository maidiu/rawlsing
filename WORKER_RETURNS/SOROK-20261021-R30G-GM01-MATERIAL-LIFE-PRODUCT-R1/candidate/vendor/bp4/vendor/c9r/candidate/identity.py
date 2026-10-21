"""Actor identity, activation and standing-state ingress (ADP007/ADP008 seam).

Ingress is fail-closed: every refusal is a typed result, never a fabricated actor.
Demographic, identity or structural fields never become psychological state; a
record that carries belief, affect, trait or capability-claim content is refused
with `ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS`.

Source resolution (C9R): a record that claims a native owner source namespace
must be resolved through an injected, independently owned `ActorSourceResolver`.
A sealed hash alone authenticates bytes, never origin. Records namespaced
`TEST_ONLY...` are admitted only with the explicit `TEST_ONLY_SOURCEFREE_TECHNICAL`
grade and can never satisfy the native release gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .canon import digest, seal, valid

ACTOR_RECORD_SCHEMA = "C9P_ACTOR_IDENTITY_RECORD@1"
GRADE_TEST_ONLY = "TEST_ONLY_SOURCEFREE_TECHNICAL"
GRADE_NATIVE_OWNER = "NATIVE_OWNER_SOURCE"
TEST_ONLY_PREFIX = "TEST_ONLY"

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
    SOURCE_UNRESOLVED = "SOURCE_UNRESOLVED"
    RECORD_INTEGRITY_FAILURE = "RECORD_INTEGRITY_FAILURE"
    ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS = "ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"


@runtime_checkable
class ActorSourceResolver(Protocol):
    """Independently owned resolution of one actor source reference/hash."""

    def resolve_actor_source(
        self, *, actor_id: str, source_ref: str, source_hash: str, as_of: int
    ) -> bool:
        ...


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
    source_grade: str = ""
    native_source_resolved: bool = False

    @property
    def admitted(self) -> bool:
        return self.status is IngressStatus.ADMITTED


def _has_psychology_claim(raw: Mapping[str, Any]) -> str | None:
    for key in raw:
        if key in PSYCHOLOGY_CLAIM_KEYS:
            return key
    return None


def _refused(reason: IngressReason, record_hash: str = "") -> ActorIngressResult:
    return ActorIngressResult(
        status=IngressStatus.REFUSED,
        reason=reason,
        actor_id="",
        standing_state="",
        currentness_as_of=0,
        source_ref="",
        readset_refs=(),
        record_hash=record_hash,
    )


def ingress_actor(
    raw: Mapping[str, Any],
    *,
    as_of: int,
    resolver: ActorSourceResolver | None = None,
) -> ActorIngressResult:
    """Validate one actor identity record at time `as_of`.

    A native-owner source reference requires `resolver`; without one the record
    is refused with `SOURCE_UNRESOLVED`. A `TEST_ONLY` source is admitted only as
    an explicitly typed test-only record. An admitted result's readset binds the
    exact source reference and hash.
    """
    if not isinstance(raw, Mapping):
        return _refused(IngressReason.RECORD_INTEGRITY_FAILURE)
    if _has_psychology_claim(raw) is not None:
        return _refused(IngressReason.ACTOR_PSYCHOLOGY_CLAIM_AT_INGRESS)
    if raw.get("schema") != ACTOR_RECORD_SCHEMA:
        return _refused(IngressReason.SCHEMA_MISMATCH)
    if not valid(raw):
        return _refused(IngressReason.RECORD_INTEGRITY_FAILURE)
    actor_id = raw.get("actor_id")
    if not isinstance(actor_id, str) or not actor_id.strip():
        return _refused(
            IngressReason.ACTOR_ID_MISSING
            if actor_id is None
            else IngressReason.ACTOR_ID_INVALID_TYPE,
            raw.get("hash", ""),
        )
    activation = raw.get("activation_status")
    if not isinstance(activation, str) or not activation.strip():
        return _refused(IngressReason.ACTIVATION_STATUS_MISSING, raw.get("hash", ""))
    if activation != "ACTIVE":
        return _refused(IngressReason.ACTOR_NOT_ACTIVE, raw.get("hash", ""))
    standing = raw.get("standing_state")
    if not isinstance(standing, str) or not standing.strip():
        return _refused(IngressReason.STANDING_STATE_MISSING, raw.get("hash", ""))
    currentness = raw.get("currentness_as_of")
    if not isinstance(currentness, int) or isinstance(currentness, bool):
        return _refused(IngressReason.STANDING_STATE_STALE, raw.get("hash", ""))
    if currentness > as_of:
        return _refused(IngressReason.STANDING_STATE_STALE, raw.get("hash", ""))
    source_ref = raw.get("source_ref")
    if not isinstance(source_ref, str) or not source_ref.strip():
        return _refused(IngressReason.SOURCE_REF_MISSING, raw.get("hash", ""))
    source_hash = raw.get("source_hash")
    if not isinstance(source_hash, str) or not source_hash.strip():
        return _refused(IngressReason.SOURCE_HASH_MISSING, raw.get("hash", ""))
    native_resolved = False
    if source_ref.startswith(TEST_ONLY_PREFIX):
        source_grade = GRADE_TEST_ONLY
    else:
        source_grade = GRADE_NATIVE_OWNER
        if resolver is None or not resolver.resolve_actor_source(
            actor_id=actor_id, source_ref=source_ref, source_hash=source_hash, as_of=as_of
        ):
            return _refused(IngressReason.SOURCE_UNRESOLVED, raw.get("hash", ""))
        native_resolved = True
    return ActorIngressResult(
        status=IngressStatus.ADMITTED,
        reason=IngressReason.OK,
        actor_id=actor_id,
        standing_state=standing,
        currentness_as_of=currentness,
        source_ref=source_ref,
        readset_refs=(source_ref,),
        record_hash=raw["hash"],
        source_grade=source_grade,
        native_source_resolved=native_resolved,
    )


def actor_record_hash(record: Mapping[str, Any]) -> str:
    """Return the sealed identity digest of one actor record."""
    return digest({k: v for k, v in record.items() if k != "hash"})


__all__ = [
    "ACTOR_RECORD_SCHEMA",
    "ActorIdentityRecord",
    "ActorIngressResult",
    "ActorSourceResolver",
    "GRADE_NATIVE_OWNER",
    "GRADE_TEST_ONLY",
    "IngressReason",
    "IngressStatus",
    "TEST_ONLY_PREFIX",
    "actor_record_hash",
    "ingress_actor",
]
