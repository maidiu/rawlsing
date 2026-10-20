"""C9 material-handoff consumer over an actual performed material action.

This is the bounded C9 *material handoff* only. It is not a RULE_A/RULE_T issuer
and does not generate a person, actor, child or route probability. Full C9 E1/E2
native authority remains a typed HOLD until the competent owners issue it.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json


class C9Refusal(Exception):
    pass


def build_handoff(action, material):
    if action.get("status") != "PERFORMED":
        raise C9Refusal("ACTION_NOT_PERFORMED")
    if material.get("event_id") not in (action.get("causal_parent_event_ids") or []):
        raise C9Refusal("MATERIAL_EVENT_NOT_IN_ACTION_CAUSAL_PARENTS")
    if action.get("material_event_ref") != material.get("event_id"):
        raise C9Refusal("MATERIAL_EVENT_REF_MISMATCH")
    body = {
        "schema": "SOROK_G17_C9_MATERIAL_HANDOFF@1",
        "handoff_id": None,
        "actor": action.get("owner_id"),
        "effective_index": action.get("effective_index"),
        "before": deepcopy(action.get("before")),
        "after": deepcopy(action.get("after")),
        "material_event_ref": material.get("event_id"),
        "material_payload": {k: material.get(k) for k in
                             ("payment_per_actor", "task_hours", "material_units")},
        "causal_parent_event_ids": list(action.get("causal_parent_event_ids") or []),
        "e1_source": "PERFORMED_MATERIAL_ACTION",
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
    """Read a material handoff; refuse if the material parent was severed."""
    if not isinstance(handoff, dict) or handoff.get("schema") != "SOROK_G17_C9_MATERIAL_HANDOFF@1":
        raise C9Refusal("NOT_A_C9_HANDOFF")
    if handoff.get("route_probability") is not None or handoff.get("selection_weight") is not None:
        raise C9Refusal("PROHIBITED_ROUTE_OR_WEIGHT")
    if handoff.get("person_or_child_generated") is not False:
        raise C9Refusal("PERSON_OR_CHILD_GENERATION")
    parents = handoff.get("causal_parent_event_ids") or []
    material_source_id = material.get("event_id")
    if material_source_id not in parents:
        raise C9Refusal("SEVERED_MATERIAL_SOURCE")
    if handoff.get("material_event_ref") != material_source_id:
        raise C9Refusal("MATERIAL_REF_MISMATCH")
    before = handoff.get("before") or {}
    after = handoff.get("after") or {}
    expected = deepcopy(before)
    try:
        expected["cash"] += material["payment_per_actor"]
        expected["free_hours"] -= material["task_hours"]
        expected["completed_units"] += material["material_units"]
    except (KeyError, TypeError):
        raise C9Refusal("MATERIAL_PAYLOAD_INCOMPLETE")
    if after != expected:
        raise C9Refusal("AFTERSTATE_NOT_MATERIAL_CONSERVING")
    if after.get("free_hours", -1) < 0 or after.get("cash", -1) < 0:
        raise C9Refusal("NEGATIVE_MATERIAL_STATE")
    return {
        "schema": "SOROK_G17_C9_MATERIAL_RECEIPT@1",
        "status": "ACCEPTED",
        "handoff_id": handoff.get("handoff_id"),
        "actor": handoff.get("actor"),
        "after": deepcopy(after),
        "material_event_ref": material_source_id,
        "e2_later_authority": "HOLD_UNISSUED",
        "route_probability": None,
        "selection_weight": None,
    }
