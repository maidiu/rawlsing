"""S36 TEST_ONLY bridge for S35 actor-local access and observed response.

The bridge is a non-native adapter over the existing C9R response/target/commit
path. It reports only an explicitly source-bound actor-local access witness and
a separately source-bound actor-owned immediate response witness. Objective
material availability, historical acts, labels and B's private motive are not
converted into A uptake. The bridge always returns zero target proposals; the
existing CAN011 path therefore evaluates `proposal=None` and emits
NO_CHANGE/NO_PROPOSAL.

All records are TEST_ONLY transport. No native CAN008/CAN011/ADP source, rule,
permission, actor, event or human subject is issued here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .canon import digest, seal, valid
from .response_rules import (
    ResponseResult,
    ResponseStatus,
    RuleLookupResult,
    RuleLookupStatus,
)

S35_ACCESS_SCHEMA = "S35_ACTOR_LOCAL_E1_ACCESS@1"
S35_RESPONSE_SCHEMA = "S35_ACTOR_OWNED_IMMEDIATE_RESPONSE@1"
S35_RECEIPT_SCHEMA = "S35_OBSERVED_IMMEDIATE_RESPONSE_RECEIPT@1"
S35_GRADE = "TEST_ONLY_SOURCEFREE_TECHNICAL_NOT_NATIVE"
S35_ACCESS_SOURCE_CLASS = "ADP017_ACTOR_LOCAL_ACCESS"
S35_RESPONSE_SOURCE_CLASS = "A_ACTOR_PERFORMED_IMMEDIATE_RESPONSE"
S35_ACCESS_SOURCE_PREFIX = "TEST_ONLY_ADP017_ACCESS"
S35_RESPONSE_SOURCE_PREFIX = "TEST_ONLY_A_RESPONSE"
S35_ACCESS_STATUSES = frozenset({"ACCESSIBLE", "NOT_WITNESSED", "UNKNOWN"})
S35_RESPONSE_KINDS = frozenset({"ATTEND_OBJECT", "REQUEST_TOOL", "EXPLICIT_REFUSAL"})

OBSERVED_IMMEDIATE_OBJECT_ORIENTATION = "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
OBSERVED_CURRENT_REFUSAL = "OBSERVED_CURRENT_REFUSAL"
RECEIVABLE_NO_OBSERVED_UPTAKE = "RECEIVABLE_NO_OBSERVED_UPTAKE"
UNKNOWN_RECEIVABILITY = "UNKNOWN_RECEIVABILITY"
AMBIGUOUS_CONTRADICTORY = "AMBIGUOUS_CONTRADICTORY"

ROUTE_POSITIVE = "S35_OBSERVED_PRESENT_ORIENTATION"
ROUTE_UNKNOWN = "S35_VALID_EMPTY_UNKNOWN_RECEIVABILITY"
ROUTE_NO_UPTAKE = "S35_VALID_EMPTY_NO_OBSERVED_UPTAKE"
ROUTE_CONTRADICTORY = "S35_VALID_EMPTY_CONTRADICTORY"

_ACCESS_SOURCE_KEYS = (
    "source_ref",
    "source_class",
    "actor_id",
    "event_ref",
    "access_time",
    "access_status",
    "scene",
    "content",
    "revoked",
)
_RESPONSE_SOURCE_KEYS = (
    "source_ref",
    "source_class",
    "actor_id",
    "event_ref",
    "response_ref",
    "response_kind",
    "response_time",
    "content",
    "revoked",
)


@dataclass(frozen=True)
class S35ActorAccessRequest:
    """One TEST_ONLY request for actor-local access and observed response."""

    access_witness: Mapping[str, Any] | None = None
    response_witness: Mapping[str, Any] | None = None
    contradictory_context: bool = False
    contradictory_refs: tuple[str, ...] = ()
    revoked_source_refs: frozenset[str] = frozenset()


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _access_source_digest(record: Mapping[str, Any]) -> str:
    return digest({key: record.get(key) for key in _ACCESS_SOURCE_KEYS})


def _response_source_digest(record: Mapping[str, Any]) -> str:
    return digest({key: record.get(key) for key in _RESPONSE_SOURCE_KEYS})


def make_actor_local_access_witness(
    *,
    actor_id: str,
    event_ref: str,
    access_time: int,
    source_ref: str,
    access_status: str = "ACCESSIBLE",
    scene: str = "",
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
) -> dict:
    """Build one source-bound TEST_ONLY ADP017-style access witness."""
    body = {
        "source_ref": source_ref,
        "source_class": S35_ACCESS_SOURCE_CLASS,
        "actor_id": actor_id,
        "event_ref": event_ref,
        "access_time": access_time,
        "access_status": access_status,
        "scene": scene,
        "content": dict(content or {}),
        "revoked": revoked,
    }
    return seal(dict(body, source_hash=digest(body)))


def make_actor_owned_response_witness(
    *,
    actor_id: str,
    event_ref: str,
    response_ref: str,
    response_kind: str,
    response_time: int,
    source_ref: str,
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
) -> dict:
    """Build one source-bound TEST_ONLY actor-performed response witness."""
    body = {
        "source_ref": source_ref,
        "source_class": S35_RESPONSE_SOURCE_CLASS,
        "actor_id": actor_id,
        "event_ref": event_ref,
        "response_ref": response_ref,
        "response_kind": response_kind,
        "response_time": response_time,
        "content": dict(content or {}),
        "revoked": revoked,
    }
    return seal(dict(body, source_hash=digest(body)))


def _refused(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    readset: tuple[str, ...],
    reason: str,
    status: ResponseStatus = ResponseStatus.REFUSED,
) -> ResponseResult:
    return ResponseResult(
        status=status,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        recruited_refs=(),
        uptake_refs=(),
        candidate_route="S35_REFUSED" if status is ResponseStatus.REFUSED else "",
        target_proposals=(),
        readset_refs=readset,
        reason=reason,
        receipt_hash="",
    )


def _valid_empty(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    subject: str,
    outcome: str,
    route: str,
    readset: tuple[str, ...],
    access: Mapping[str, Any] | None,
    contradictory_context: bool,
    contradictory_refs: tuple[str, ...],
    material_eligible: bool | None,
    eligible_material_refs: tuple[str, ...],
    recruited: tuple[str, ...] = (),
) -> ResponseResult:
    access_ref = str(access.get("source_ref", "")) if isinstance(access, Mapping) else ""
    access_hash = str(access.get("source_hash", "")) if isinstance(access, Mapping) else ""
    access_time = access.get("access_time") if isinstance(access, Mapping) else None
    access_status = str(access.get("access_status", "")) if isinstance(access, Mapping) else ""
    receipt = seal(
        {
            "schema": S35_RECEIPT_SCHEMA,
            "event_ref": event_ref,
            "actor_id": subject,
            "access_source_ref": access_ref,
            "access_source_hash": access_hash,
            "access_time": access_time,
            "access_status": access_status,
            "observed_response_ref": "",
            "response_source_ref": "",
            "response_source_hash": "",
            "response_kind": "",
            "response_time": None,
            "outcome": outcome,
            "candidate_route": route,
            "recruited_refs": list(recruited),
            "uptake_refs": [],
            "readset_refs": list(readset),
            "contradictory_context": contradictory_context,
            "contradictory_refs": list(contradictory_refs),
            "objective_material_eligible": material_eligible,
            "objective_material_refs": list(eligible_material_refs),
            "objective_material_implies_uptake": False,
            "target_proposals": [],
            "belief_update": None,
            "emotion_update": None,
            "durable_update": None,
            "claim_ceiling": "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A",
            "reason": outcome,
            "grade": S35_GRADE,
        }
    )
    return ResponseResult(
        status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        recruited_refs=recruited,
        uptake_refs=(),
        candidate_route=route,
        target_proposals=(),
        readset_refs=readset,
        reason=outcome,
        receipt_hash=receipt["hash"],
        eligible_material_refs=tuple(eligible_material_refs),
        declared_history_refs=(),
        declared_offer_ref="",
        s35_receipt=receipt,
    )


def _access_error(
    record: Mapping[str, Any],
    *,
    subject: str,
    event_ref: str,
    event_time: int,
    event_scene: str,
    as_of: int,
    revoked_source_refs: frozenset[str],
) -> str:
    if not isinstance(record, Mapping) or not valid(dict(record)):
        return "S35_ACCESS_INTEGRITY_FAILURE"
    if record.get("source_ref") in revoked_source_refs or record.get("revoked") is True:
        return "S35_ACCESS_REVOKED"
    if record.get("source_class") != S35_ACCESS_SOURCE_CLASS:
        return "S35_ACCESS_SOURCE_CLASS_INVALID"
    if not str(record.get("source_ref", "")).startswith(S35_ACCESS_SOURCE_PREFIX):
        return "S35_ACCESS_SOURCE_NAMESPACE_INVALID"
    if record.get("source_hash") != _access_source_digest(record):
        return "S35_ACCESS_SOURCE_HASH_MISMATCH"
    if record.get("actor_id") != subject:
        return "S35_ACCESS_ACTOR_MISMATCH"
    if record.get("event_ref") != event_ref:
        return "S35_ACCESS_EVENT_MISMATCH"
    scene = record.get("scene")
    if not isinstance(scene, str) or not scene:
        return "S35_ACCESS_SCENE_MISSING"
    if not isinstance(event_scene, str) or not event_scene:
        return "S35_ACCESS_EVENT_SCENE_MISSING"
    if scene != event_scene:
        return "S35_ACCESS_SCENE_MISMATCH"
    access_time = record.get("access_time")
    if not _is_int(access_time):
        return "S35_ACCESS_TIME_INVALID"
    if access_time < event_time or access_time > as_of:
        return "S35_ACCESS_TIME_INVALID"
    if record.get("access_status") not in S35_ACCESS_STATUSES:
        return "S35_ACCESS_STATUS_INVALID"
    return ""


def _response_error(
    record: Mapping[str, Any],
    *,
    subject: str,
    event_ref: str,
    event_time: int,
    access_time: int,
    as_of: int,
    revoked_source_refs: frozenset[str],
) -> str:
    if not isinstance(record, Mapping) or not valid(dict(record)):
        return "S35_RESPONSE_INTEGRITY_FAILURE"
    if record.get("source_ref") in revoked_source_refs or record.get("revoked") is True:
        return "S35_RESPONSE_REVOKED"
    if record.get("source_class") != S35_RESPONSE_SOURCE_CLASS:
        return "S35_RESPONSE_SOURCE_CLASS_INVALID"
    if not str(record.get("source_ref", "")).startswith(S35_RESPONSE_SOURCE_PREFIX):
        return "S35_RESPONSE_SOURCE_NAMESPACE_INVALID"
    if record.get("source_hash") != _response_source_digest(record):
        return "S35_RESPONSE_SOURCE_HASH_MISMATCH"
    if record.get("actor_id") != subject:
        return "S35_RESPONSE_ACTOR_MISMATCH"
    if record.get("event_ref") != event_ref:
        return "S35_RESPONSE_EVENT_MISMATCH"
    response_ref = record.get("response_ref")
    if not isinstance(response_ref, str) or not response_ref.strip():
        return "S35_RESPONSE_REF_MISSING"
    if record.get("response_kind") not in S35_RESPONSE_KINDS:
        return "S35_RESPONSE_KIND_INVALID"
    response_time = record.get("response_time")
    if not _is_int(response_time):
        return "S35_RESPONSE_TIME_INVALID"
    if response_time < event_time or response_time < access_time or response_time > as_of:
        return "S35_RESPONSE_TIME_INVALID"
    return ""


def evaluate_actor_access_response(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    event_time: int,
    subject: str,
    request: S35ActorAccessRequest,
    conditioning_readset: tuple[str, ...],
    event_scene: str = "",
    as_of: int,
    material_eligible: bool | None = None,
    eligible_material_refs: tuple[str, ...] = (),
) -> ResponseResult:
    """Evaluate S35 access/response witnesses through the C9R response contract.

    A valid access witness plus a separately witnessed actor-owned response is a
    positive observed-response result with zero target proposals. Missing access
    is UNKNOWN_RECEIVABILITY, missing response is RECEIVABLE_NO_OBSERVED_UPTAKE,
    and contradictory context without a response is AMBIGUOUS_CONTRADICTORY.
    Invalid, foreign, stale, future, hash-mismatched or revoked sources are typed
    refusals. Objective material eligibility never creates uptake.
    """
    base_readset = tuple([event_ref, *conditioning_readset])
    status = rule_lookup.status
    if status is RuleLookupStatus.RULE_ABSENT:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset,
            reason="CAN008_RULE_ABSENT_FROM_REGISTRY",
        )
    if status is RuleLookupStatus.RULE_ISSUER_UNVERIFIED:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset,
            reason=rule_lookup.reason or "CAN008_RULE_ISSUER_UNVERIFIED",
            status=ResponseStatus.HELD,
        )
    if status in (RuleLookupStatus.RULE_BINDING_MISMATCH, RuleLookupStatus.REQUEST_INVALID):
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset,
            reason=rule_lookup.reason,
        )

    access = request.access_witness
    if access is None:
        return _valid_empty(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            subject=subject,
            outcome=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset,
            access=None,
            contradictory_context=request.contradictory_context,
            contradictory_refs=tuple(request.contradictory_refs),
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
        )
    access_reason = _access_error(
        access,
        subject=subject,
        event_ref=event_ref,
        event_time=event_time,
        event_scene=event_scene,
        as_of=as_of,
        revoked_source_refs=request.revoked_source_refs,
    )
    if access_reason:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset + (str(access.get("source_ref", "")),),
            reason=access_reason,
        )
    access_ref = str(access.get("source_ref", ""))
    access_hash = str(access.get("source_hash", ""))
    access_time = access.get("access_time")
    access_status = str(access.get("access_status", ""))
    access_readset = (access_ref, access_hash)
    if access_status != "ACCESSIBLE":
        return _valid_empty(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            subject=subject,
            outcome=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset + access_readset,
            access=access,
            contradictory_context=request.contradictory_context,
            contradictory_refs=tuple(request.contradictory_refs),
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            recruited=(access_ref,),
        )

    contradictory_refs = tuple(request.contradictory_refs)
    if request.contradictory_context:
        if not contradictory_refs or any(
            not isinstance(ref, str) or not ref.strip() for ref in contradictory_refs
        ):
            return _refused(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset + access_readset,
                reason="S35_CONTRADICTORY_CONTEXT_UNBOUND",
            )

    response = request.response_witness
    if response is None:
        outcome = AMBIGUOUS_CONTRADICTORY if request.contradictory_context else RECEIVABLE_NO_OBSERVED_UPTAKE
        route = ROUTE_CONTRADICTORY if request.contradictory_context else ROUTE_NO_UPTAKE
        return _valid_empty(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            subject=subject,
            outcome=outcome,
            route=route,
            readset=base_readset + access_readset + contradictory_refs,
            access=access,
            contradictory_context=request.contradictory_context,
            contradictory_refs=contradictory_refs,
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            recruited=(access_ref, *contradictory_refs),
        )
    response_reason = _response_error(
        response,
        subject=subject,
        event_ref=event_ref,
        event_time=event_time,
        access_time=access_time,
        as_of=as_of,
        revoked_source_refs=request.revoked_source_refs,
    )
    if response_reason:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset
            + access_readset
            + (str(response.get("source_ref", "")),),
            reason=response_reason,
        )

    response_ref = str(response.get("response_ref", ""))
    response_source_ref = str(response.get("source_ref", ""))
    response_source_hash = str(response.get("source_hash", ""))
    response_kind = str(response.get("response_kind", ""))
    response_time = response.get("response_time")
    outcome = (
        OBSERVED_CURRENT_REFUSAL
        if response_kind == "EXPLICIT_REFUSAL"
        else OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    )
    readset = (
        base_readset
        + access_readset
        + (response_source_ref, response_source_hash, response_ref)
        + contradictory_refs
    )
    recruited = (access_ref, *contradictory_refs)
    uptake = (response_ref,)
    receipt = seal(
        {
            "schema": S35_RECEIPT_SCHEMA,
            "event_ref": event_ref,
            "actor_id": subject,
            "access_source_ref": access_ref,
            "access_source_hash": access_hash,
            "access_time": access_time,
            "access_status": access_status,
            "observed_response_ref": response_ref,
            "response_source_ref": response_source_ref,
            "response_source_hash": response_source_hash,
            "response_kind": response_kind,
            "response_time": response_time,
            "outcome": outcome,
            "candidate_route": ROUTE_POSITIVE,
            "recruited_refs": list(recruited),
            "uptake_refs": list(uptake),
            "readset_refs": list(readset),
            "contradictory_context": request.contradictory_context,
            "contradictory_refs": list(contradictory_refs),
            "objective_material_eligible": material_eligible,
            "objective_material_refs": list(eligible_material_refs),
            "objective_material_implies_uptake": False,
            "target_proposals": [],
            "belief_update": None,
            "emotion_update": None,
            "durable_update": None,
            "claim_ceiling": "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A",
            "reason": outcome,
            "grade": S35_GRADE,
        }
    )
    return ResponseResult(
        status=ResponseStatus.RESPONSE_COMMITTED,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        recruited_refs=recruited,
        uptake_refs=uptake,
        candidate_route=ROUTE_POSITIVE,
        target_proposals=(),
        readset_refs=readset,
        reason=outcome,
        receipt_hash=receipt["hash"],
        eligible_material_refs=tuple(eligible_material_refs),
        declared_history_refs=(),
        declared_offer_ref="",
        s35_receipt=receipt,
    )


__all__ = [
    "AMBIGUOUS_CONTRADICTORY",
    "OBSERVED_CURRENT_REFUSAL",
    "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
    "RECEIVABLE_NO_OBSERVED_UPTAKE",
    "ROUTE_CONTRADICTORY",
    "ROUTE_NO_UPTAKE",
    "ROUTE_POSITIVE",
    "ROUTE_UNKNOWN",
    "S35_ACCESS_SCHEMA",
    "S35_ACCESS_SOURCE_CLASS",
    "S35_ACCESS_SOURCE_PREFIX",
    "S35_ACCESS_STATUSES",
    "S35_GRADE",
    "S35_RECEIPT_SCHEMA",
    "S35_RESPONSE_KINDS",
    "S35_RESPONSE_SCHEMA",
    "S35_RESPONSE_SOURCE_CLASS",
    "S35_RESPONSE_SOURCE_PREFIX",
    "S35ActorAccessRequest",
    "UNKNOWN_RECEIVABILITY",
    "evaluate_actor_access_response",
    "make_actor_local_access_witness",
    "make_actor_owned_response_witness",
]
