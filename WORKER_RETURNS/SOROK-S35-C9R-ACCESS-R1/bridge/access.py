"""S35 actor-local perception and actor-owned action selector.

A witness is a sealed perception receipt or action-occurrence receipt, never a
default inferred from B's operation. If actual A input is unavailable the
result is a typed hold. Explicit TEST_ONLY controlled evidence is accepted only
with its own grade and is never presented as actual A input.
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

S35_PERCEPTION_SCHEMA = "S35_A_LOCAL_PERCEPTION_RECEIPT@1"
S35_ACTION_SCHEMA = "S35_A_OWNED_ACTION_OCCURRENCE@1"
S35_ACCESS_SCHEMA = S35_PERCEPTION_SCHEMA
S35_RESPONSE_SCHEMA = S35_ACTION_SCHEMA
S35_RECEIPT_SCHEMA = "S35_ACTOR_ACCESS_RESPONSE_RECEIPT@2"
S35_GRADE = "TEST_ONLY_SOURCEFREE_TECHNICAL_NOT_NATIVE"
S35_ACCESS_SOURCE_CLASS = "ADP017_ACTOR_LOCAL_ACCESS"
S35_ACTION_SOURCE_CLASS = "A_ACTOR_PERFORMED_IMMEDIATE_RESPONSE"
S35_ACCESS_SOURCE_PREFIX = "TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION"
S35_ACTION_SOURCE_PREFIX = "TEST_ONLY_A_ACTION_S35_A_OWNED"
S35_ACCESS_STATUSES = frozenset({"ACCESSIBLE", "NOT_WITNESSED", "UNKNOWN"})
S35_ACTION_KINDS = frozenset(
    {"REQUEST_TOOL", "ATTEND_OBJECT", "EXPLICIT_REFUSAL", "NO_OBSERVED_ACTION"}
)

S35_GRADE_CONTROLLED = "TEST_ONLY_CONTROLLED_FIXTURE"
S35_GRADE_QUALIFIED = "QUALIFIED_ACTUAL_A_INPUT"
S35_GRADE_UNAVAILABLE = "ACTUAL_A_INPUT_UNAVAILABLE"
S35_QUALIFICATION_CONTROLLED = (
    "CONTROLLED_ENGINEERING_EVIDENCE_NOT_ACTUAL_A_INPUT"
)
S35_QUALIFICATION_QUALIFIED = "QUALIFIED_OWNER_RECEIPT"
S35_QUALIFICATION_UNAVAILABLE = "TYPED_HOLD_ACTUAL_A_INPUT_UNAVAILABLE"

OBSERVED_IMMEDIATE_OBJECT_ORIENTATION = "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
OBSERVED_CURRENT_REFUSAL = "OBSERVED_CURRENT_REFUSAL"
RECEIVABLE_NO_OBSERVED_UPTAKE = "RECEIVABLE_NO_OBSERVED_UPTAKE"
UNKNOWN_RECEIVABILITY = "UNKNOWN_RECEIVABILITY"
AMBIGUOUS_CONTRADICTORY = "AMBIGUOUS_CONTRADICTORY"
A_LOCAL_PERCEPTION_HOLD = "A_LOCAL_PERCEPTION_HOLD"
A_OWNED_ACTION_HOLD = "A_OWNED_ACTION_HOLD"

ROUTE_POSITIVE = "S35_OBSERVED_PRESENT_ORIENTATION"
ROUTE_UNKNOWN = "S35_VALID_EMPTY_UNKNOWN_RECEIVABILITY"
ROUTE_NO_UPTAKE = "S35_VALID_EMPTY_NO_OBSERVED_UPTAKE"
ROUTE_CONTRADICTORY = "S35_VALID_EMPTY_CONTRADICTORY"
ROUTE_PERCEPTION_HOLD = "S35_TYPED_HOLD_NO_A_LOCAL_PERCEPTION"
ROUTE_ACTION_HOLD = "S35_TYPED_HOLD_NO_A_OWNED_ACTION"
ROUTE_REFUSED = "S35_REFUSED"

CLAIM_CEILING = "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A"
PUBLIC_B_OPERATION_TOKENS = ("SHARE_TOOL", "REFUSE_TOOL")

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
    perception_receipt: Mapping[str, Any] | None = None
    action_receipt: Mapping[str, Any] | None = None
    contradictory_context: bool = False
    contradictory_refs: tuple[str, ...] = ()
    revoked_source_refs: frozenset[str] = frozenset()
    qualified_owner_resolver: Any = None


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


def _seal_receipt(body: dict) -> dict:
    body = dict(body)
    body["source_hash"] = digest(
        {key: value for key, value in body.items() if key not in {"hash", "source_hash"}}
    )
    return seal(body)


def _perception_body(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    perception_ref: str,
    access_status: str,
    perceived_at: int,
    scene: str | None,
    content: Mapping[str, Any] | None,
    revoked: bool,
    evidence_grade: str,
    actual_actor_input: bool,
    native: bool,
    qualification: str,
) -> dict:
    return {
        "schema": S35_PERCEPTION_SCHEMA,
        "source_ref": source_ref,
        "source_class": S35_ACCESS_SOURCE_CLASS,
        "owner_ref": source_ref,
        "perception_ref": perception_ref,
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
        "perceived_at": perceived_at,
        "access_status": access_status,
        "scene": _value(context, "scene") if scene is None else scene,
        "content": dict(content or {}),
        "revoked": bool(revoked),
        "evidence_grade": evidence_grade,
        "actual_actor_input": bool(actual_actor_input),
        "native": bool(native),
        "qualification": qualification,
    }


def make_a_local_perception_receipt(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    perception_ref: str,
    access_status: str,
    perceived_at: int,
    scene: str | None = None,
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
    evidence_grade: str = S35_GRADE_CONTROLLED,
    actual_actor_input: bool = False,
    native: bool = False,
    qualification: str = S35_QUALIFICATION_CONTROLLED,
) -> dict:
    return _seal_receipt(
        _perception_body(
            context=context,
            source_ref=source_ref,
            perception_ref=perception_ref,
            access_status=access_status,
            perceived_at=perceived_at,
            scene=scene,
            content=content,
            revoked=revoked,
            evidence_grade=evidence_grade,
            actual_actor_input=actual_actor_input,
            native=native,
            qualification=qualification,
        )
    )


def _action_body(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    action_ref: str,
    action_kind: str,
    performed: bool,
    action_time: int,
    content: Mapping[str, Any] | None,
    revoked: bool,
    evidence_grade: str,
    actual_actor_input: bool,
    native: bool,
    qualification: str,
) -> dict:
    return {
        "schema": S35_ACTION_SCHEMA,
        "source_ref": source_ref,
        "source_class": S35_ACTION_SOURCE_CLASS,
        "owner_ref": source_ref,
        "action_ref": action_ref,
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
        "action_kind": action_kind,
        "performed": performed,
        "action_time": action_time,
        "content": dict(content or {}),
        "revoked": bool(revoked),
        "evidence_grade": evidence_grade,
        "actual_actor_input": bool(actual_actor_input),
        "native": bool(native),
        "qualification": qualification,
    }


def make_a_owned_action_receipt(
    *,
    context: S35Context | Mapping[str, Any],
    source_ref: str,
    action_ref: str,
    action_kind: str,
    performed: bool,
    action_time: int,
    content: Mapping[str, Any] | None = None,
    revoked: bool = False,
    evidence_grade: str = S35_GRADE_CONTROLLED,
    actual_actor_input: bool = False,
    native: bool = False,
    qualification: str = S35_QUALIFICATION_CONTROLLED,
) -> dict:
    return _seal_receipt(
        _action_body(
            context=context,
            source_ref=source_ref,
            action_ref=action_ref,
            action_kind=action_kind,
            performed=performed,
            action_time=action_time,
            content=content,
            revoked=revoked,
            evidence_grade=evidence_grade,
            actual_actor_input=actual_actor_input,
            native=native,
            qualification=qualification,
        )
    )


def reseal_perception_receipt(receipt: Mapping[str, Any], **changes: Any) -> dict:
    body = {
        key: value
        for key, value in receipt.items()
        if key not in {"hash", "source_hash"}
    }
    body.update(changes)
    return _seal_receipt(body)


def reseal_action_receipt(receipt: Mapping[str, Any], **changes: Any) -> dict:
    body = {
        key: value
        for key, value in receipt.items()
        if key not in {"hash", "source_hash"}
    }
    body.update(changes)
    return _seal_receipt(body)


def _integrity_error(
    receipt: Any, *, schema: str, source_class: str, prefix: str
) -> str:
    if not isinstance(receipt, Mapping):
        return "INTEGRITY_FAILURE"
    body = dict(receipt)
    if not valid(body):
        return "SEAL_INVALID"
    body_without_hash = {
        key: value for key, value in body.items() if key not in {"hash", "source_hash"}
    }
    if body.get("source_hash") != digest(body_without_hash):
        return "SOURCE_HASH_MISMATCH"
    if body.get("schema") != schema:
        return "SCHEMA_MISMATCH"
    if body.get("source_class") != source_class:
        return "SOURCE_CLASS_INVALID"
    source_ref = body.get("source_ref")
    if not isinstance(source_ref, str) or not source_ref.startswith(prefix):
        return "SOURCE_NAMESPACE_INVALID"
    if body.get("owner_ref") != source_ref:
        return "OWNER_REF_INVALID"
    return ""


def _grade_error(receipt: Mapping[str, Any]) -> str:
    grade = receipt.get("evidence_grade")
    actual = receipt.get("actual_actor_input")
    native = receipt.get("native")
    qualification = receipt.get("qualification")
    if native is not False:
        return "NATIVE_CLAIM_REFUSED"
    if grade == S35_GRADE_CONTROLLED:
        if actual is not False:
            return "CONTROLLED_GRADE_ACTUAL_CLAIM"
        if qualification != S35_QUALIFICATION_CONTROLLED:
            return "CONTROLLED_QUALIFICATION_INVALID"
        return ""
    if grade == S35_GRADE_QUALIFIED:
        if actual is not True:
            return "QUALIFIED_GRADE_ACTUAL_MISSING"
        if qualification != S35_QUALIFICATION_QUALIFIED:
            return "QUALIFIED_QUALIFICATION_INVALID"
        return ""
    return "EVIDENCE_GRADE_INVALID"


def _binding_error(receipt: Mapping[str, Any], context: S35Context) -> str:
    for field in _CONTEXT_BINDING:
        if receipt.get(field) != getattr(context, field):
            return "BINDING_MISMATCH:" + field
    return ""


def _perception_error(
    receipt: Mapping[str, Any],
    *,
    context: S35Context,
    revoked_source_refs: frozenset[str],
) -> str:
    error = _integrity_error(
        receipt,
        schema=S35_PERCEPTION_SCHEMA,
        source_class=S35_ACCESS_SOURCE_CLASS,
        prefix=S35_ACCESS_SOURCE_PREFIX,
    )
    if error:
        return "PERCEPTION_" + error
    error = _grade_error(receipt)
    if error:
        return "PERCEPTION_" + error
    if receipt.get("source_ref") in revoked_source_refs or receipt.get("revoked") is True:
        return "PERCEPTION_REVOKED"
    error = _binding_error(receipt, context)
    if error:
        return "PERCEPTION_" + error
    perception_ref = receipt.get("perception_ref")
    if not isinstance(perception_ref, str) or not perception_ref.strip():
        return "PERCEPTION_REF_MISSING"
    perceived_at = receipt.get("perceived_at")
    if not _is_int(perceived_at):
        return "PERCEPTION_TIME_INVALID"
    if perceived_at < context.event_time or perceived_at > context.clock:
        return "PERCEPTION_TIME_INVALID"
    if receipt.get("access_status") not in S35_ACCESS_STATUSES:
        return "PERCEPTION_STATUS_INVALID"
    scene = receipt.get("scene")
    if isinstance(scene, str) and scene and context.scene and scene != context.scene:
        return "PERCEPTION_SCENE_MISMATCH"
    return ""


def _action_error(
    receipt: Mapping[str, Any],
    *,
    context: S35Context,
    perceived_at: int,
    revoked_source_refs: frozenset[str],
) -> str:
    error = _integrity_error(
        receipt,
        schema=S35_ACTION_SCHEMA,
        source_class=S35_ACTION_SOURCE_CLASS,
        prefix=S35_ACTION_SOURCE_PREFIX,
    )
    if error:
        return "ACTION_" + error
    error = _grade_error(receipt)
    if error:
        return "ACTION_" + error
    if receipt.get("source_ref") in revoked_source_refs or receipt.get("revoked") is True:
        return "ACTION_REVOKED"
    error = _binding_error(receipt, context)
    if error:
        return "ACTION_" + error
    action_ref = receipt.get("action_ref")
    if not isinstance(action_ref, str) or not action_ref.strip():
        return "ACTION_REF_MISSING"
    action_kind = receipt.get("action_kind")
    if action_kind not in S35_ACTION_KINDS:
        return "ACTION_KIND_INVALID"
    performed = receipt.get("performed")
    if not isinstance(performed, bool):
        return "ACTION_PERFORMED_INVALID"
    if performed and action_kind == "NO_OBSERVED_ACTION":
        return "ACTION_PERFORMED_INCONSISTENT"
    if not performed and action_kind != "NO_OBSERVED_ACTION":
        return "ACTION_NOT_PERFORMED"
    action_time = receipt.get("action_time")
    if not _is_int(action_time):
        return "ACTION_TIME_INVALID"
    if action_time > context.clock:
        return "ACTION_TIME_INVALID"
    if performed and action_time < max(context.event_time, perceived_at):
        return "ACTION_TIME_INVALID"
    return ""


def _resolve_qualified(
    request: S35ActorAccessRequest, receipt: Mapping[str, Any], kind: str
) -> bool | None:
    resolver = request.qualified_owner_resolver
    if resolver is None:
        return None
    try:
        return bool(resolver(receipt=dict(receipt), kind=kind))
    except Exception:
        return False


def _iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str):
                yield key
            yield from _iter_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_strings(item)


def public_privacy_error(value: Any) -> str:
    for text in _iter_strings(value):
        for token in PUBLIC_B_OPERATION_TOKENS:
            if token in text:
                return "S35_PUBLIC_VALUE_PRIVACY_VIOLATION:" + token
    return ""


def _grade_pair(perception: Mapping[str, Any] | None, action: Mapping[str, Any] | None) -> tuple[str, bool, str]:
    grades = [
        receipt.get("evidence_grade")
        for receipt in (perception, action)
        if isinstance(receipt, Mapping)
    ]
    if not grades:
        return (
            S35_GRADE_UNAVAILABLE,
            False,
            S35_QUALIFICATION_UNAVAILABLE,
        )
    if all(grade == S35_GRADE_CONTROLLED for grade in grades):
        return (
            S35_GRADE_CONTROLLED,
            False,
            S35_QUALIFICATION_CONTROLLED,
        )
    if all(grade == S35_GRADE_QUALIFIED for grade in grades):
        return (
            S35_GRADE_QUALIFIED,
            True,
            S35_QUALIFICATION_QUALIFIED,
        )
    return (S35_GRADE_UNAVAILABLE, False, S35_QUALIFICATION_UNAVAILABLE)


def _receipt(
    *,
    context: S35Context,
    event_ref: str,
    subject: str,
    outcome: str,
    route: str,
    readset: tuple[str, ...],
    perception: Mapping[str, Any] | None,
    action: Mapping[str, Any] | None,
    recruited: tuple[str, ...],
    uptake: tuple[str, ...],
    contradictory_context: bool,
    contradictory_refs: tuple[str, ...],
    material_eligible: bool | None,
    eligible_material_refs: tuple[str, ...],
    reason: str,
    hold_reason: str = "",
    force_unavailable_grade: bool = False,
) -> dict:
    perception_map = perception if isinstance(perception, Mapping) else None
    action_map = action if isinstance(action, Mapping) else None
    if force_unavailable_grade:
        grade, actual, qualification = (
            S35_GRADE_UNAVAILABLE,
            False,
            S35_QUALIFICATION_UNAVAILABLE,
        )
    else:
        grade, actual, qualification = _grade_pair(perception_map, action_map)
    perception = perception or {}
    action = action or {}
    receipt = seal(
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
            "perception_ref": str(perception.get("perception_ref", "")),
            "perception_hash": str(perception.get("hash", "")),
            "perception_source_ref": str(perception.get("source_ref", "")),
            "perceived_at": perception.get("perceived_at"),
            "access_status": str(perception.get("access_status", "")),
            "action_ref": str(action.get("action_ref", "")),
            "action_receipt_hash": str(action.get("hash", "")),
            "action_source_ref": str(action.get("source_ref", "")),
            "action_owner_ref": str(action.get("owner_ref", "")),
            "action_kind": str(action.get("action_kind", "")),
            "action_time": action.get("action_time"),
            "action_performed": action.get("performed"),
            "outcome": outcome,
            "candidate_route": route,
            "hold_reason": hold_reason,
            "recruited_refs": list(recruited),
            "uptake_refs": list(uptake),
            "readset_refs": list(readset),
            "contradictory_context": bool(contradictory_context),
            "contradictory_refs": list(contradictory_refs),
            "objective_material_eligible": material_eligible,
            "objective_material_refs": list(eligible_material_refs),
            "objective_material_implies_uptake": False,
            "evidence_grade": grade,
            "actual_actor_input": actual,
            "qualification": qualification,
            "target_proposals": [],
            "belief_update": None,
            "emotion_update": None,
            "durable_update": None,
            "claim_ceiling": CLAIM_CEILING,
            "reason": reason,
        }
    )
    privacy = public_privacy_error(receipt)
    if privacy:
        raise ValueError(privacy)
    return receipt


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


def _hold(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    readset: tuple[str, ...],
    reason: str,
    route: str,
    hold_reason: str,
    context: S35Context,
    subject: str,
    perception: Mapping[str, Any] | None,
    action: Mapping[str, Any] | None,
    recruited: tuple[str, ...],
    contradictory_context: bool,
    contradictory_refs: tuple[str, ...],
    material_eligible: bool | None,
    eligible_material_refs: tuple[str, ...],
    force_unavailable_grade: bool = False,
) -> S35Evaluation:
    receipt = _receipt(
        context=context,
        event_ref=event_ref,
        subject=subject,
        outcome=reason,
        route=route,
        readset=readset,
        perception=perception,
        action=action,
        recruited=recruited,
        uptake=(),
        contradictory_context=contradictory_context,
        contradictory_refs=contradictory_refs,
        material_eligible=material_eligible,
        eligible_material_refs=eligible_material_refs,
        reason=reason,
        hold_reason=hold_reason,
        force_unavailable_grade=force_unavailable_grade,
    )
    return _result(
        status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        reason=reason,
        route=route,
        readset=readset,
        receipt=receipt,
        recruited=recruited,
        eligible_material_refs=eligible_material_refs,
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

    perception = request.perception_receipt
    if perception is None:
        return _hold(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset,
            reason=A_LOCAL_PERCEPTION_HOLD,
            route=ROUTE_PERCEPTION_HOLD,
            hold_reason="ACTUAL_A_LOCAL_PERCEPTION_UNAVAILABLE",
            context=context,
            subject=subject,
            perception=None,
            action=None,
            recruited=(),
            contradictory_context=request.contradictory_context,
            contradictory_refs=tuple(request.contradictory_refs),
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
        )

    perception_error = _perception_error(
        perception,
        context=context,
        revoked_source_refs=request.revoked_source_refs,
    )
    if perception_error:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset + (str(perception.get("source_ref", "")),),
            reason=perception_error,
        )
    if perception.get("evidence_grade") == S35_GRADE_QUALIFIED:
        resolved = _resolve_qualified(request, perception, "perception")
        if resolved is None:
            return _hold(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset + (str(perception.get("source_ref", "")),),
                reason=A_LOCAL_PERCEPTION_HOLD,
                route=ROUTE_PERCEPTION_HOLD,
                hold_reason="QUALIFIED_A_LOCAL_PERCEPTION_RESOLVER_UNAVAILABLE",
                context=context,
                subject=subject,
                perception=perception,
                action=None,
                recruited=(str(perception.get("perception_ref", "")),),
                contradictory_context=request.contradictory_context,
                contradictory_refs=tuple(request.contradictory_refs),
                material_eligible=material_eligible,
                eligible_material_refs=eligible_material_refs,
            )
        if not resolved:
            return _refused(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset + (str(perception.get("source_ref", "")),),
                reason="A_LOCAL_PERCEPTION_UNVERIFIED",
            )

    perception_ref = str(perception.get("perception_ref", ""))
    perception_hash = str(perception.get("hash", ""))
    perception_source_ref = str(perception.get("source_ref", ""))
    perceived_at = int(perception.get("perceived_at"))
    perception_readset = (perception_ref, perception_hash)
    if perception.get("access_status") != "ACCESSIBLE":
        readset = base_readset + perception_readset + tuple(request.contradictory_refs)
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=UNKNOWN_RECEIVABILITY,
            route=ROUTE_UNKNOWN,
            readset=readset,
            perception=perception,
            action=None,
            recruited=(perception_ref,),
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
            readset=readset,
            receipt=receipt,
            recruited=(perception_ref,),
            eligible_material_refs=eligible_material_refs,
        )

    contradictory_refs = tuple(request.contradictory_refs)
    if request.contradictory_context:
        if not contradictory_refs or any(
            not isinstance(ref, str) or not ref.strip()
            for ref in contradictory_refs
        ):
            return _refused(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset + perception_readset,
                reason="S35_CONTRADICTORY_CONTEXT_UNBOUND",
            )
        privacy = public_privacy_error(contradictory_refs)
        if privacy:
            return _refused(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset + perception_readset,
                reason=privacy,
            )

    action = request.action_receipt
    if action is None and request.contradictory_context:
        readset = base_readset + perception_readset + contradictory_refs
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=AMBIGUOUS_CONTRADICTORY,
            route=ROUTE_CONTRADICTORY,
            readset=readset,
            perception=perception,
            action=None,
            recruited=(perception_ref, *contradictory_refs),
            uptake=(),
            contradictory_context=True,
            contradictory_refs=contradictory_refs,
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            reason=AMBIGUOUS_CONTRADICTORY,
        )
        return _result(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            reason=AMBIGUOUS_CONTRADICTORY,
            route=ROUTE_CONTRADICTORY,
            readset=readset,
            receipt=receipt,
            recruited=(perception_ref, *contradictory_refs),
            eligible_material_refs=eligible_material_refs,
        )
    if action is None:
        return _hold(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset
            + perception_readset
            + contradictory_refs,
            reason=A_OWNED_ACTION_HOLD,
            route=ROUTE_ACTION_HOLD,
            hold_reason="ACTUAL_A_OWNED_ACTION_UNAVAILABLE",
            context=context,
            subject=subject,
            perception=perception,
            action=None,
            recruited=(perception_ref, *contradictory_refs),
            contradictory_context=request.contradictory_context,
            contradictory_refs=contradictory_refs,
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            force_unavailable_grade=True,
        )

    action_error = _action_error(
        action,
        context=context,
        perceived_at=perceived_at,
        revoked_source_refs=request.revoked_source_refs,
    )
    if action_error:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset
            + perception_readset
            + (str(action.get("source_ref", "")),),
            reason=action_error,
        )

    perception_grade = perception.get("evidence_grade")
    action_grade = action.get("evidence_grade")
    if perception_grade != action_grade:
        return _refused(
            rule_lookup=rule_lookup,
            event_ref=event_ref,
            readset=base_readset + perception_readset,
            reason="S35_EVIDENCE_GRADE_MIXED",
        )
    if action_grade == S35_GRADE_QUALIFIED:
        resolved = _resolve_qualified(request, action, "action")
        if resolved is None:
            return _hold(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset
                + perception_readset
                + (str(action.get("source_ref", "")),),
                reason=A_OWNED_ACTION_HOLD,
                route=ROUTE_ACTION_HOLD,
                hold_reason="QUALIFIED_A_OWNED_ACTION_RESOLVER_UNAVAILABLE",
                context=context,
                subject=subject,
                perception=perception,
                action=action,
                recruited=(perception_ref, *contradictory_refs),
                contradictory_context=request.contradictory_context,
                contradictory_refs=contradictory_refs,
                material_eligible=material_eligible,
                eligible_material_refs=eligible_material_refs,
            )
        if not resolved:
            return _refused(
                rule_lookup=rule_lookup,
                event_ref=event_ref,
                readset=base_readset
                + perception_readset
                + (str(action.get("source_ref", "")),),
                reason="A_OWNED_ACTION_UNVERIFIED",
            )

    action_ref = str(action.get("action_ref", ""))
    action_hash = str(action.get("hash", ""))
    action_source_ref = str(action.get("source_ref", ""))
    action_kind = str(action.get("action_kind", ""))
    action_time = action.get("action_time")
    performed = action.get("performed")
    action_readset = (action_ref, action_hash)
    if performed is False:
        readset = (
            base_readset
            + perception_readset
            + action_readset
            + contradictory_refs
        )
        receipt = _receipt(
            context=context,
            event_ref=event_ref,
            subject=subject,
            outcome=RECEIVABLE_NO_OBSERVED_UPTAKE,
            route=ROUTE_NO_UPTAKE,
            readset=readset,
            perception=perception,
            action=action,
            recruited=(perception_ref, *contradictory_refs),
            uptake=(),
            contradictory_context=request.contradictory_context,
            contradictory_refs=contradictory_refs,
            material_eligible=material_eligible,
            eligible_material_refs=eligible_material_refs,
            reason=RECEIVABLE_NO_OBSERVED_UPTAKE,
        )
        return _result(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            reason=RECEIVABLE_NO_OBSERVED_UPTAKE,
            route=ROUTE_NO_UPTAKE,
            readset=readset,
            receipt=receipt,
            recruited=(perception_ref, *contradictory_refs),
            eligible_material_refs=eligible_material_refs,
        )

    outcome = (
        OBSERVED_CURRENT_REFUSAL
        if action_kind == "EXPLICIT_REFUSAL"
        else OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    )
    readset = (
        base_readset
        + perception_readset
        + action_readset
        + contradictory_refs
    )
    receipt = _receipt(
        context=context,
        event_ref=event_ref,
        subject=subject,
        outcome=outcome,
        route=ROUTE_POSITIVE,
        readset=readset,
        perception=perception,
        action=action,
        recruited=(perception_ref, *contradictory_refs),
        uptake=(action_ref,),
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
        recruited=(perception_ref, *contradictory_refs),
        uptake=(action_ref,),
        eligible_material_refs=eligible_material_refs,
    )


def _rule_lookup_equal(actual: Any, expected: Any) -> bool:
    if actual is None or expected is None:
        return actual is expected
    fields = (
        "status",
        "rule_id",
        "rule_version",
        "rule_content_hash",
        "authority_id",
        "issuer_verified",
        "grade",
        "reason",
    )
    return all(getattr(actual, field, None) == getattr(expected, field, None) for field in fields)


def validate_consumer_inputs(current: Mapping[str, Any], kwargs: Mapping[str, Any]) -> None:
    context = current["context"]
    expected = current["expected"]
    checks = {
        "event_ref": kwargs.get("event_ref") == context.event_ref,
        "subject": kwargs.get("subject") == context.actor_id,
        "event_time": kwargs.get("event_time") == expected["event_time"],
        "conditioning_readset": tuple(kwargs.get("conditioning_readset") or ())
        == tuple(expected["conditioning_readset"]),
        "material_eligible": kwargs.get("material_eligible")
        == expected["material_eligible"],
        "eligible_material_refs": tuple(kwargs.get("eligible_material_refs") or ())
        == tuple(expected["eligible_material_refs"]),
        "actor_history_refs": tuple(kwargs.get("actor_history_refs") or ())
        == tuple(expected["actor_history_refs"]),
        "other_person_offer_ref": kwargs.get("other_person_offer_ref")
        == expected["other_person_offer_ref"],
        "material_opportunity_ref": kwargs.get("material_opportunity_ref")
        == expected["material_opportunity_ref"],
        "prior_response_count": kwargs.get("prior_response_count")
        == expected["prior_response_count"],
        "rule_lookup": _rule_lookup_equal(
            kwargs.get("rule_lookup"), expected["rule_lookup"]
        ),
    }
    for field, accepted in checks.items():
        if not accepted:
            raise RuntimeError("S35_CONSUMER_INPUT_MISMATCH:" + field)


def pipeline_selector(**kwargs: Any) -> ResponseResult:
    import candidate.pipeline as pipeline

    current = _CURRENT.get()
    if current is None:
        return pipeline._s35_original_evaluate_response(**kwargs)
    validate_consumer_inputs(current, kwargs)
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
    "A_LOCAL_PERCEPTION_HOLD",
    "A_OWNED_ACTION_HOLD",
    "CLAIM_CEILING",
    "OBSERVED_CURRENT_REFUSAL",
    "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
    "PUBLIC_B_OPERATION_TOKENS",
    "RECEIVABLE_NO_OBSERVED_UPTAKE",
    "ROUTE_ACTION_HOLD",
    "ROUTE_CONTRADICTORY",
    "ROUTE_NO_UPTAKE",
    "ROUTE_PERCEPTION_HOLD",
    "ROUTE_POSITIVE",
    "ROUTE_REFUSED",
    "ROUTE_UNKNOWN",
    "S35_ACCESS_SCHEMA",
    "S35_ACCESS_SOURCE_CLASS",
    "S35_ACCESS_SOURCE_PREFIX",
    "S35_ACCESS_STATUSES",
    "S35_ACTION_KINDS",
    "S35_ACTION_SCHEMA",
    "S35_ACTION_SOURCE_CLASS",
    "S35_ACTION_SOURCE_PREFIX",
    "S35ActorAccessRequest",
    "S35Context",
    "S35Evaluation",
    "S35_GRADE_CONTROLLED",
    "S35_GRADE_QUALIFIED",
    "S35_GRADE_UNAVAILABLE",
    "S35_PERCEPTION_SCHEMA",
    "S35_QUALIFICATION_CONTROLLED",
    "S35_QUALIFICATION_QUALIFIED",
    "S35_QUALIFICATION_UNAVAILABLE",
    "S35_RECEIPT_SCHEMA",
    "UNKNOWN_RECEIVABILITY",
    "current_context",
    "evaluate_actor_access_response",
    "make_a_local_perception_receipt",
    "make_a_owned_action_receipt",
    "pipeline_selector",
    "public_privacy_error",
    "reseal_action_receipt",
    "reseal_perception_receipt",
    "reset_current_context",
    "set_current_context",
    "validate_consumer_inputs",
]
