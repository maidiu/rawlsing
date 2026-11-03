"""S35 actor-local access and actor-owned immediate-response selector.

The selector is a source-neutral adapter over the pinned C9R ResponseResult
contract. It never converts objective material availability, B's private act,
labels or history into actor uptake. Every result carries zero target proposals.
"""
from __future__ import annotations

import contextvars
from dataclasses import dataclass
from typing import Any, Mapping

from candidate import digest, seal, valid
from candidate.response_rules import (
    ResponseResult,
    ResponseStatus,
    RuleLookupResult,
    RuleLookupStatus,
)

S35_ACCESS_SCHEMA = "S35_ACTOR_LOCAL_E1_ACCESS@1"
S35_RESPONSE_SCHEMA = "S35_ACTOR_OWNED_IMMEDIATE_RESPONSE@1"
S35_RECEIPT_SCHEMA = "S35_ACTOR_ACCESS_RESPONSE_RECEIPT@1"
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
ROUTE_REFUSED = "S35_REFUSED"

CLAIM_CEILING = "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A"

_ACCESS_BODY_KEYS = (
    "schema",
    "source_ref",
    "source_class",
    "actor_id",
    "event_ref",
    "event_id",
    "root_id",
    "root_branch_hash",
    "root_state_hash",
    "branch_id",
    "branch_hash",
    "branch_parent_id",
    "branch_fork_clock",
    "clock",
    "access_time",
    "access_status",
    "scene",
    "content",
    "revoked",
)

_RESPONSE_BODY_KEYS = (
    "schema",
    "source_ref",
    "source_class",
    "actor_id",
    "event_ref",
    "event_id",
    "root_id",
    "root_branch_hash",
    "root_state_hash",
    "branch_id",
    "branch_hash",
    "branch_parent_id",
    "branch_fork_clock",
    "clock",
    "response_ref",
    "response_kind",
    "response_time",
    "performed",
    "owner_ref",
    "content",
    "revoked",
)

_CONTEXT_BINDING = (
    "actor_id",
    "event_ref",
    "event_id",
    "root_id",
    "root_branch_hash",
    "root_state_hash",
    "branch_id",
    "branch_hash",
    "branch_parent_id",
    "branch_fork_clock",
    "clock",
)

_CURRENT: contextvars.ContextVar[dict | None] = contextvars.ContextVar(
    "s35_current_context", default=None
)


@dataclass(frozen=True)
class S35Context:
    actor_id: str
    event_ref: str
    event_id: str
    event_time: int
    as_of: int
    scene: str
    root_id: str
    root_branch_hash: str
    root_state_hash: str
    branch_id: str
    branch_hash: str
    branch_parent_id: str
    branch_fork_clock: int
    clock: int
    material_eligible: bool
    eligible_material_refs: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "event_ref": self.event_ref,
            "event_id": self.event_id,
            "event_time": self.event_time,
            "as_of": self.as_of,
            "scene": self.scene,
            "root_id": self.root_id,
            "root_branch_hash": self.root_branch_hash,
            "root_state_hash": self.root_state_hash,
            "branch_id": self.branch_id,
            "branch_hash": self.branch_hash,
            "branch_parent_id": self.branch_parent_id,
            "branch_fork_clock": self.branch_fork_clock,
            "clock": self.clock,
            "material_eligible": self.material_eligible,
            "eligible_material_refs": list(self.eligible_material_refs),
        }


@dataclass(frozen=True)
class S35ActorAccessRequest:
    access_witness: Mapping[str, Any] | None = None
    response_witness: Mapping[str, Any] | None = None
    contradictory_context: bool = False
    contradictory_refs: tuple[str, ...] = ()
    revoked_source_refs: frozenset[str] = frozenset()


@dataclass(frozen=True)
class S35Evaluation:
    response: ResponseResult
    receipt: Mapping[str, Any]

    @property
    def outcome(self) -> str:
        return self.response.reason


def _value(context: Any, key: str) -> Any:
    if isinstance(context, Mapping):
        return context.get(key)
    return getattr(context, key)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _seal_body(body: dict, body_keys: tuple[str, ...]) -> dict:
    body = dict(body)
    body["source_hash"] = digest({key: body.get(key) for key in body_keys})
    return seal(body)


def make_actor_local_access_witness(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    access_status: str = "ACCESSIBLE",
    access_time: int | None = None,
    scene: str | None = None,
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
) -> dict:
    body = {
        "schema": S35_ACCESS_SCHEMA,
        "source_ref": source_ref,
        "source_class": S35_ACCESS_SOURCE_CLASS,
        "actor_id": _value(context, "actor_id"),
        "event_ref": _value(context, "event_ref"),
        "event_id": _value(context, "event_id"),
        "root_id": _value(context, "root_id"),
        "root_branch_hash": _value(context, "root_branch_hash"),
        "root_state_hash": _value(context, "root_state_hash"),
        "branch_id": _value(context, "branch_id"),
        "branch_hash": _value(context, "branch_hash"),
        "branch_parent_id": _value(context, "branch_parent_id"),
        "branch_fork_clock": _value(context, "branch_fork_clock"),
        "clock": _value(context, "clock"),
        "access_time": (
            _value(context, "event_time") if access_time is None else access_time
        ),
        "access_status": access_status,
        "scene": _value(context, "scene") if scene is None else scene,
        "content": dict(content or {}),
        "revoked": bool(revoked),
    }
    return _seal_body(body, _ACCESS_BODY_KEYS)


def make_actor_owned_response_witness(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    response_ref: str,
    response_kind: str,
    response_time: int | None = None,
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
) -> dict:
    if response_time is None:
        response_time = int(_value(context, "event_time")) + 1
    body = {
        "schema": S35_RESPONSE_SCHEMA,
        "source_ref": source_ref,
        "source_class": S35_RESPONSE_SOURCE_CLASS,
        "actor_id": _value(context, "actor_id"),
        "event_ref": _value(context, "event_ref"),
        "event_id": _value(context, "event_id"),
        "root_id": _value(context, "root_id"),
        "root_branch_hash": _value(context, "root_branch_hash"),
        "root_state_hash": _value(context, "root_state_hash"),
        "branch_id": _value(context, "branch_id"),
        "branch_hash": _value(context, "branch_hash"),
        "branch_parent_id": _value(context, "branch_parent_id"),
        "branch_fork_clock": _value(context, "branch_fork_clock"),
        "clock": _value(context, "clock"),
        "response_ref": response_ref,
        "response_kind": response_kind,
        "response_time": response_time,
        "performed": True,
        "owner_ref": source_ref,
        "content": dict(content or {}),
        "revoked": bool(revoked),
    }
    return _seal_body(body, _RESPONSE_BODY_KEYS)


def reseal_access_witness(witness: Mapping[str, Any], **changes: Any) -> dict:
    body = {
        key: value
        for key, value in witness.items()
        if key not in {"hash", "source_hash"}
    }
    body.update(changes)
    return _seal_body(body, _ACCESS_BODY_KEYS)


def reseal_response_witness(witness: Mapping[str, Any], **changes: Any) -> dict:
    body = {
        key: value
        for key, value in witness.items()
        if key not in {"hash", "source_hash"}
    }
    body.update(changes)
    return _seal_body(body, _RESPONSE_BODY_KEYS)


def _integrity_error(
    record: Any, *, body_keys: tuple[str, ...], schema: str, source_class: str,
    prefix: str,
) -> str:
    if not isinstance(record, Mapping):
        return "INTEGRITY_FAILURE"
    body = dict(record)
    if not valid(body):
        return "SEAL_INVALID"
    if body.get("source_hash") != digest(
        {key: body.get(key) for key in body_keys}
    ):
        return "SOURCE_HASH_MISMATCH"
    if body.get("schema") != schema:
        return "SCHEMA_MISMATCH"
    if body.get("source_class") != source_class:
        return "SOURCE_CLASS_INVALID"
    source_ref = body.get("source_ref")
    if not isinstance(source_ref, str) or not source_ref.startswith(prefix):
        return "SOURCE_NAMESPACE_INVALID"
    return ""


def _binding_error(record: Mapping[str, Any], context: S35Context) -> str:
    for field in _CONTEXT_BINDING:
        if record.get(field) != getattr(context, field):
            return "BINDING_MISMATCH:" + field
    return ""


def _access_error(
    record: Mapping[str, Any],
    *,
    context: S35Context,
    revoked_source_refs: frozenset[str],
) -> str:
    error = _integrity_error(
        record,
        body_keys=_ACCESS_BODY_KEYS,
        schema=S35_ACCESS_SCHEMA,
        source_class=S35_ACCESS_SOURCE_CLASS,
        prefix=S35_ACCESS_SOURCE_PREFIX,
    )
    if error:
        return "ACCESS_" + error
    if record.get("source_ref") in revoked_source_refs or record.get("revoked") is True:
        return "ACCESS_REVOKED"
    error = _binding_error(record, context)
    if error:
        return "ACCESS_" + error
    access_time = record.get("access_time")
    if not _is_int(access_time):
        return "ACCESS_TIME_INVALID"
    if access_time < context.event_time or access_time > context.clock:
        return "ACCESS_TIME_INVALID"
    if record.get("access_status") not in S35_ACCESS_STATUSES:
        return "ACCESS_STATUS_INVALID"
    scene = record.get("scene")
    if isinstance(scene, str) and scene and context.scene and scene != context.scene:
        return "ACCESS_SCENE_MISMATCH"
    return ""


def _response_error(
    record: Mapping[str, Any],
    *,
    context: S35Context,
    access_time: int,
    revoked_source_refs: frozenset[str],
) -> str:
    error = _integrity_error(
        record,
        body_keys=_RESPONSE_BODY_KEYS,
        schema=S35_RESPONSE_SCHEMA,
        source_class=S35_RESPONSE_SOURCE_CLASS,
        prefix=S35_RESPONSE_SOURCE_PREFIX,
    )
    if error:
        return "RESPONSE_" + error
    if record.get("source_ref") in revoked_source_refs or record.get("revoked") is True:
        return "RESPONSE_REVOKED"
    error = _binding_error(record, context)
    if error:
        return "RESPONSE_" + error
    response_ref = record.get("response_ref")
    if not isinstance(response_ref, str) or not response_ref.strip():
        return "RESPONSE_REF_MISSING"
    if record.get("response_kind") not in S35_RESPONSE_KINDS:
        return "RESPONSE_KIND_INVALID"
    if record.get("performed") is not True:
        return "RESPONSE_NOT_PERFORMED"
    owner_ref = record.get("owner_ref")
    if not isinstance(owner_ref, str) or not owner_ref.startswith(
        S35_RESPONSE_SOURCE_PREFIX
    ):
        return "RESPONSE_OWNER_INVALID"
    response_time = record.get("response_time")
    if not _is_int(response_time):
        return "RESPONSE_TIME_INVALID"
    if response_time < max(context.event_time, access_time) or response_time > context.clock:
        return "RESPONSE_TIME_INVALID"
    return ""


def _receipt(
    *,
    context: S35Context,
    event_ref: str,
    subject: str,
    outcome: str,
    route: str,
    readset: tuple[str, ...],
    access: Mapping[str, Any] | None,
    response: Mapping[str, Any] | None,
    recruited: tuple[str, ...],
    uptake: tuple[str, ...],
    contradictory_context: bool,
    contradictory_refs: tuple[str, ...],
    material_eligible: bool | None,
    eligible_material_refs: tuple[str, ...],
    reason: str,
) -> dict:
    access = access or {}
    response = response or {}
    return seal(
        {
            "schema": S35_RECEIPT_SCHEMA,
            "grade": S35_GRADE,
            "native": False,
            "event_ref": event_ref,
            "event_id": context.event_id,
            "actor_id": subject,
            "root_id": context.root_id,
            "root_branch_hash": context.root_branch_hash,
            "root_state_hash": context.root_state_hash,
            "branch_id": context.branch_id,
            "branch_hash": context.branch_hash,
            "branch_parent_id": context.branch_parent_id,
            "branch_fork_clock": context.branch_fork_clock,
            "clock": context.clock,
            "access_source_ref": str(access.get("source_ref", "")),
            "access_source_hash": str(access.get("source_hash", "")),
            "access_time": access.get("access_time"),
            "access_status": str(access.get("access_status", "")),
            "response_source_ref": str(response.get("source_ref", "")),
            "response_source_hash": str(response.get("source_hash", "")),
            "response_ref": str(response.get("response_ref", "")),
            "response_kind": str(response.get("response_kind", "")),
            "response_time": response.get("response_time"),
            "response_performed": response.get("performed"),
            "response_owner_ref": str(response.get("owner_ref", "")),
            "outcome": outcome,
            "candidate_route": route,
            "recruited_refs": list(recruited),
            "uptake_refs": list(uptake),
            "readset_refs": list(readset),
            "contradictory_context": bool(contradictory_context),
            "contradictory_refs": list(contradictory_refs),
            "objective_material_eligible": material_eligible,
            "objective_material_refs": list(eligible_material_refs),
            "objective_material_implies_uptake": False,
            "target_proposals": [],
            "belief_update": None,
            "emotion_update": None,
            "durable_update": None,
            "claim_ceiling": CLAIM_CEILING,
            "reason": reason,
        }
    )


def _result(
    *,
    status: ResponseStatus,
    event_ref: str,
    rule_lookup: RuleLookupResult,
    reason: str,
    route: str,
    readset: tuple[str, ...],
    receipt: Mapping[str, Any] | None,
    recruited: tuple[str, ...] = (),
    uptake: tuple[str, ...] = (),
    eligible_material_refs: tuple[str, ...] = (),
) -> S35Evaluation:
    return S35Evaluation(
        response=ResponseResult(
            status=status,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=recruited,
            uptake_refs=uptake,
            candidate_route=route,
            target_proposals=(),
            readset_refs=readset,
            reason=reason,
            receipt_hash=str((receipt or {}).get("hash", "")),
            eligible_material_refs=tuple(eligible_material_refs),
            declared_history_refs=(),
            declared_offer_ref="",
        ),
        receipt=receipt or {},
    )


def _refused(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    readset: tuple[str, ...],
    reason: str,
    status: ResponseStatus = ResponseStatus.REFUSED,
) -> S35Evaluation:
    return _result(
        status=status,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        reason=reason,
        route=ROUTE_REFUSED,
        readset=readset,
        receipt=None,
    )


def evaluate_actor_access_response(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    event_time: int,
    subject: str,
    request: S35ActorAccessRequest,
    conditioning_readset: tuple[str, ...],
    context: S35Context,
    as_of: int,
    material_eligible: bool | None = None,
    eligible_material_refs: tuple[str, ...] = (),
) -> S35Evaluation:
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
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset,
            access=None,
            response=None,
            recruited=(),
            uptake=(),
            contradictory_context=request.contradictory_context,
            contradictory_refs=tuple(request.contradictory_refs),
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            reason=UNKNOWN_RECEIVABILITY,
        )
        return _result(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            reason=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset,
            receipt=receipt,
            eligible_material_refs=eligible_material_refs,
        )

    access_reason = _access_error(
        access,
        context=context,
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
    access_readset = (access_ref, access_hash)
    if access.get("access_status") != "ACCESSIBLE":
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset + access_readset,
            access=access,
            response=None,
            recruited=(access_ref,),
            uptake=(),
            contradictory_context=request.contradictory_context,
            contradictory_refs=tuple(request.contradictory_refs),
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            reason=UNKNOWN_RECEIVABILITY,
        )
        return _result(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            reason=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=base_readset + access_readset,
            receipt=receipt,
            recruited=(access_ref,),
            eligible_material_refs=eligible_material_refs,
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
        outcome = (
            AMBIGUOUS_CONTRADICTORY
            if request.contradictory_context
            else RECEIVABLE_NO_OBSERVED_UPTAKE
        )
        route = ROUTE_CONTRADICTORY if request.contradictory_context else ROUTE_NO_UPTAKE
        readset = base_readset + access_readset + contradictory_refs
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=outcome,
            route=route,
            readset=readset,
            access=access,
            response=None,
            recruited=(access_ref, *contradictory_refs),
            uptake=(),
            contradictory_context=request.contradictory_context,
            contradictory_refs=contradictory_refs,
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            reason=outcome,
        )
        return _result(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            reason=outcome,
            route=route,
            readset=readset,
            receipt=receipt,
            recruited=(access_ref, *contradictory_refs),
            eligible_material_refs=eligible_material_refs,
        )

    response_reason = _response_error(
        response,
        context=context,
        access_time=access_time,
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
    receipt = _receipt(
        context=context,
        event_ref=event_ref,
        subject=subject,
        outcome=outcome,
        route=ROUTE_POSITIVE,
        readset=readset,
        access=access,
        response=response,
        recruited=(access_ref, *contradictory_refs),
        uptake=(response_ref,),
        contradictory_context=request.contradictory_context,
        contradictory_refs=contradictory_refs,
        material_eligible=material_eligible,
        eligible_material_refs=eligible_material_refs,
        reason=outcome,
    )
    return _result(
        status=ResponseStatus.RESPONSE_COMMITTED,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        reason=outcome,
        route=ROUTE_POSITIVE,
        readset=readset,
        receipt=receipt,
        recruited=(access_ref, *contradictory_refs),
        uptake=(response_ref,),
        eligible_material_refs=eligible_material_refs,
    )


def pipeline_selector(**kwargs: Any) -> ResponseResult:
    import candidate.pipeline as pipeline

    current = _CURRENT.get()
    if current is None:
        return pipeline._s35_original_evaluate_response(**kwargs)
    context = current["context"]
    if kwargs.get("event_ref") != context.event_ref:
        raise RuntimeError("S35_PIPELINE_EVENT_BINDING_MISMATCH")
    if kwargs.get("subject") != context.actor_id:
        raise RuntimeError("S35_PIPELINE_ACTOR_BINDING_MISMATCH")
    evaluation = current["evaluation"]
    if evaluation.response.event_ref != kwargs.get("event_ref"):
        raise RuntimeError("S35_PREFLIGHT_EVENT_BINDING_MISMATCH")
    return evaluation.response


def current_context() -> dict | None:
    return _CURRENT.get()


def set_current_context(value: dict) -> contextvars.Token:
    return _CURRENT.set(value)


def reset_current_context(token: contextvars.Token) -> None:
    _CURRENT.reset(token)


__all__ = [
    "AMBIGUOUS_CONTRADICTORY",
    "CLAIM_CEILING",
    "OBSERVED_CURRENT_REFUSAL",
    "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
    "RECEIVABLE_NO_OBSERVED_UPTAKE",
    "ROUTE_CONTRADICTORY",
    "ROUTE_NO_UPTAKE",
    "ROUTE_POSITIVE",
    "ROUTE_REFUSED",
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
    "S35Context",
    "S35Evaluation",
    "UNKNOWN_RECEIVABILITY",
    "current_context",
    "evaluate_actor_access_response",
    "make_actor_local_access_witness",
    "make_actor_owned_response_witness",
    "pipeline_selector",
    "reseal_access_witness",
    "reseal_response_witness",
    "reset_current_context",
    "set_current_context",
]
