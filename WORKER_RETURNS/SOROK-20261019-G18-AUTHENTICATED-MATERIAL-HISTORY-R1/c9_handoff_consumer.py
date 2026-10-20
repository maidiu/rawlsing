"""C9 material-handoff consumer over an authenticated performed material action.

This is the bounded C9 *material handoff* only. It is not a RULE_A/RULE_T issuer
and does not generate a person, actor, child or route probability. Full C9 E1/E2
native authority remains a typed HOLD until the competent owners issue it.

G18 repair: the handoff is not accepted merely because the caller-supplied
packet is internally consistent. Both the material event and the performed
action must carry exact source-issued fixture-origin receipts; the consumer
recomputes the material afterstate from that authenticated source and refuses a
forged owner, permission, payment (including fake 100000 cash) or after-state.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json


class C9Refusal(Exception):
    pass


def _source_api():
    # Imported lazily so the consumer can be reviewed/imported without a package
    # path side effect; the package is still the only source of fixture receipts.
    from lab_sgi1.joint import (
        verify_material_source, verify_performed_action,
        NATIVE_GRANT, SOURCE_GRADE, SOURCE_RECEIPT_SCHEMA, ACTION_RECEIPT_SCHEMA,
        JOINT_OWNER,
    )
    return dict(
        verify_material_source=verify_material_source,
        verify_performed_action=verify_performed_action,
        native_grant=NATIVE_GRANT,
        source_grade=SOURCE_GRADE,
        source_receipt_schema=SOURCE_RECEIPT_SCHEMA,
        action_receipt_schema=ACTION_RECEIPT_SCHEMA,
        joint_owner=JOINT_OWNER,
    )


def build_handoff(action, material):
    api = _source_api()
    if not isinstance(action, dict):
        raise C9Refusal("ACTION_NOT_OBJECT")
    if action.get("status") != "PERFORMED":
        raise C9Refusal("ACTION_NOT_PERFORMED")
    accepted, reason, _payload = api["verify_material_source"](material)
    if not accepted:
        raise C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTICATED:" + str(reason))
    accepted, reason = api["verify_performed_action"](action, material)
    if not accepted:
        raise C9Refusal("PERFORMED_ACTION_NOT_AUTHENTICATED:" + str(reason))
    if material.get("event_id") not in (action.get("causal_parent_event_ids") or []):
        raise C9Refusal("MATERIAL_EVENT_NOT_IN_ACTION_CAUSAL_PARENTS")
    if action.get("material_event_ref") != material.get("event_id"):
        raise C9Refusal("MATERIAL_EVENT_REF_MISMATCH")
    body = {
        "schema": "SOROK_G18_C9_AUTHENTICATED_MATERIAL_HANDOFF@1",
        "handoff_id": None,
        "actor": action.get("owner_id"),
        "effective_index": action.get("effective_index"),
        "before": deepcopy(action.get("before")),
        "after": deepcopy(action.get("after")),
        "material_event_ref": material.get("event_id"),
        "material_receipt_id": "sha256:" + sha256(
            json.dumps(material.get("source_receipt"), sort_keys=True,
                       default=str).encode()).hexdigest(),
        "material_payload": {k: material.get(k) for k in
                             ("payment_per_actor", "task_hours", "material_units")},
        "material_source_receipt": deepcopy(material.get("source_receipt")),
        "action_event_ref": action.get("event_id"),
        "performed_action": deepcopy(action),
        "action_source_receipt": deepcopy(action.get("source_receipt")),
        "causal_parent_event_ids": list(action.get("causal_parent_event_ids") or []),
        "e1_source": "AUTHENTICATED_PERFORMED_MATERIAL_ACTION",
        "source_grade": api["source_grade"],
        "native_grant": api["native_grant"],
        "e2_later_authority": "HOLD_UNISSUED",
        "route_probability": None,
        "selection_weight": None,
        "person_or_child_generated": False,
    }
    body["handoff_id"] = "sha256:" + sha256(
        json.dumps({k: v for k, v in body.items() if k != "handoff_id"},
                   sort_keys=True, default=str).encode()).hexdigest()
    return body


def receive_handoff(handoff, material):
    """Read an authenticated material handoff; refuse severed or forged sources."""
    api = _source_api()
    if not isinstance(handoff, dict) or handoff.get("schema") != (
            "SOROK_G18_C9_AUTHENTICATED_MATERIAL_HANDOFF@1"):
        raise C9Refusal("NOT_A_C9_HANDOFF")
    if handoff.get("route_probability") is not None or handoff.get(
            "selection_weight") is not None:
        raise C9Refusal("PROHIBITED_ROUTE_OR_WEIGHT")
    if handoff.get("person_or_child_generated") is not False:
        raise C9Refusal("PERSON_OR_CHILD_GENERATION")
    if handoff.get("source_grade") != api["source_grade"]:
        raise C9Refusal("SOURCE_GRADE_NOT_DECLARED")
    if handoff.get("native_grant") != api["native_grant"]:
        raise C9Refusal("NATIVE_GRANT_MUST_BE_HELD")
    parents = handoff.get("causal_parent_event_ids") or []
    material_source_id = material.get("event_id") if isinstance(material, dict) else None
    if material_source_id not in parents:
        raise C9Refusal("SEVERED_MATERIAL_SOURCE")
    if handoff.get("material_event_ref") != material_source_id:
        raise C9Refusal("MATERIAL_REF_MISMATCH")
    accepted, reason, payload = api["verify_material_source"](material)
    if not accepted:
        raise C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTICATED:" + str(reason))
    performed = handoff.get("performed_action")
    accepted, reason = api["verify_performed_action"](performed, material)
    if not accepted:
        raise C9Refusal("PERFORMED_ACTION_NOT_AUTHENTICATED:" + str(reason))
    if handoff.get("action_event_ref") != performed.get("event_id"):
        raise C9Refusal("ACTION_EVENT_REF_MISMATCH")
    if handoff.get("actor") != performed.get("owner_id"):
        raise C9Refusal("ACTOR_NOT_PERFORMED_OWNER")
    if handoff.get("effective_index") != performed.get("effective_index"):
        raise C9Refusal("EFFECTIVE_INDEX_MISMATCH")
    if handoff.get("before") != performed.get("before"):
        raise C9Refusal("BEFORE_STATE_NOT_PERFORMED_BEFORE")
    if handoff.get("after") != performed.get("after"):
        raise C9Refusal("AFTER_STATE_NOT_PERFORMED_AFTER")
    if handoff.get("material_source_receipt") != material.get("source_receipt"):
        raise C9Refusal("MATERIAL_RECEIPT_NOT_THE_CONSUMED_SOURCE")
    if handoff.get("action_source_receipt") != performed.get("source_receipt"):
        raise C9Refusal("ACTION_RECEIPT_NOT_THE_CONSUMED_ACTION")
    before = performed.get("before") or {}
    after = performed.get("after") or {}
    expected = deepcopy(before)
    expected["cash"] += payload["payment_per_actor"]
    expected["free_hours"] -= payload["task_hours"]
    expected["completed_units"] += payload["material_units"]
    if after != expected:
        raise C9Refusal("AFTERSTATE_NOT_MATERIAL_CONSERVING")
    if after.get("free_hours", -1) < 0 or after.get("cash", -1) < 0:
        raise C9Refusal("NEGATIVE_MATERIAL_STATE")
    return {
        "schema": "SOROK_G18_C9_AUTHENTICATED_MATERIAL_RECEIPT@1",
        "status": "ACCEPTED",
        "handoff_id": handoff.get("handoff_id"),
        "actor": handoff.get("actor"),
        "after": deepcopy(after),
        "material_event_ref": material_source_id,
        "action_event_ref": performed.get("event_id"),
        "source_grade": api["source_grade"],
        "e2_later_authority": "HOLD_UNISSUED",
        "route_probability": None,
        "selection_weight": None,
    }
