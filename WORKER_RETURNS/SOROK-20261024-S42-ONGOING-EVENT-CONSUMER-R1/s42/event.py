"""Generic later-event admission over the same continuing person."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .bootstrap import install

install()

from bp2_joined.binding import WorldOccurrence, validate_occurrence_payload  # noqa: E402
from candidate import digest  # noqa: E402
from s41.event import (  # noqa: E402
    ContinuationProducer,
    S41EventRefusal,
    history_record_from_prior,
    world_prerequisites,
)


def _current_snapshot(session, predecessor: Mapping[str, Any],
                      history_bindings: list[Mapping[str, Any]]) -> dict:
    template = dict(session.product.seed.life.a_snapshot)
    template.pop("hash", None)
    state = dict(session.world().actor_state.get("A", {}))
    history_refs = [{
        "event_ordinal": row["event_ordinal"],
        "event_id": row["e1_event_id"],
        "event_hash": row["e1_event_hash"],
        "c8_occurrence_id": row["c8"]["occurrence_id"],
    } for row in history_bindings]
    prior_action = (predecessor.get("action") or {}).get("event_id", "")
    performed = list(template.get("performed_action_refs", []))
    if prior_action and prior_action not in performed:
        performed.append(prior_action)
    template.update({
        "state": state,
        "state_hash": digest(state),
        "last_clock": session.clock(),
        "history_hash": digest({
            "predecessor": predecessor["e1_event_hash"],
            "history_refs": history_refs,
            "world_clock": session.clock(),
        }),
        "event_head": prior_action or predecessor["e1_event_hash"],
        "event_count": int(template.get("event_count", 0)) + 1,
        "performed_action_refs": performed,
    })
    template["hash"] = digest(template)
    return template


def build_ongoing_occurrence(
    session,
    *,
    first_binding: Mapping[str, Any],
    first_payload: Mapping[str, Any],
    predecessor: Mapping[str, Any],
    history_bindings: list[Mapping[str, Any]],
    second_source: Mapping[str, Any],
    ordinal: int,
    event_time: int,
) -> WorldOccurrence:
    snapshot = _current_snapshot(session, predecessor, history_bindings)
    state = dict(session.world().actor_state.get("A", {}))
    payload = deepcopy(dict(first_payload))
    actor = dict(payload["actor"])
    actor.update({
        "state": state,
        "state_hash": snapshot["state_hash"],
        "snapshot_hash": snapshot["hash"],
        "history_hash": snapshot["history_hash"],
        "clock": session.clock(),
        "event_head": snapshot["event_head"],
        "performed_act_ref": snapshot["performed_action_refs"][-1]
        if snapshot["performed_action_refs"] else actor.get("performed_act_ref", ""),
    })
    payload["actor"] = actor
    world = dict(payload["world"])
    world.update({
        "material_ref": second_source["b_event_ref"],
        "material_receipt_id": second_source["b_event_hash"],
        "tool_available": world_prerequisites(session)["tool_available"],
        "material_remaining": state.get("material_remaining"),
        "predecessor_e1_ref": predecessor["e1_event_id"],
        "predecessor_e1_event_hash": predecessor["e1_event_hash"],
        "predecessor_c8_occurrence_id": predecessor["c8"]["occurrence_id"],
        "predecessor_c8_content_hash": predecessor["c8"].get("c8_content_hash", ""),
        "event_ordinal": ordinal,
    })
    payload["world"] = world
    payload["clock"] = int(event_time)
    payload["gm01_pre_c9_source"] = dict(second_source)
    payload["causal_parent_event_ids"] = [
        predecessor["e1_event_hash"],
        predecessor["c8"].get("c8_content_hash", ""),
    ]
    payload["s42_continuation"] = {
        "schema": "S42_CONTINUING_OCCURRENCE@1",
        "event_ordinal": ordinal,
        "branch_id": session.branch_id,
        "actor_id": actor["actor_id"],
        "predecessor_e1_ref": predecessor["e1_event_id"],
        "predecessor_e1_event_hash": predecessor["e1_event_hash"],
        "predecessor_c8_occurrence_id": predecessor["c8"]["occurrence_id"],
        "predecessor_c8_content_hash": predecessor["c8"].get("c8_content_hash", ""),
        "history_refs": [{
            "event_ordinal": row["event_ordinal"],
            "e1_event_id": row["e1_event_id"],
            "e1_event_hash": row["e1_event_hash"],
            "c8_occurrence_id": row["c8"]["occurrence_id"],
            "c8_content_hash": row["c8"].get("c8_content_hash", ""),
        } for row in history_bindings],
        "source_operation": second_source["b_operation"],
        "current_world_clock": session.clock(),
        "tool_available": world_prerequisites(session)["tool_available"],
        "material_remaining": state.get("material_remaining"),
        "actor_state_hash": digest(state),
    }
    validate_occurrence_payload(payload)
    candidate = {
        "candidate_id": "S42-OCC-" + digest(payload)[:24].upper(),
        "payload": payload,
        "source_refs": [snapshot["source_ref"], payload["other_actor"]["source_ref"]],
        "causal_time": int(event_time),
    }
    return WorldOccurrence(
        actor_key="A",
        actor_id=actor["actor_id"],
        other_id=payload["other_actor"]["actor_id"],
        event_time=int(event_time),
        candidate=candidate,
        payload=payload,
        causal_parent_event_ids=tuple(payload["causal_parent_event_ids"]),
        actor_snapshot=snapshot,
        other_snapshot=session.product.seed.life.b_snapshot,
        performed_act_ref=actor.get("performed_act_ref", ""),
        other_act_ref=second_source["b_event_ref"],
        objective_ref=world["bp1_objective_ref"],
        objective_hash=world["bp1_objective_hash"],
        material_ref=second_source["b_event_ref"],
        material_receipt_id=second_source["b_event_hash"],
        witness_ref=world["witness_ref"],
        actor_source_ref=actor["source_ref"],
        actor_source_hash=actor["source_hash"],
        other_source_ref=payload["other_actor"]["source_ref"],
        other_source_hash=payload["other_actor"]["source_hash"],
        actor_performed_receipt_id=world.get("performed_act_receipt_id", ""),
        other_performed_receipt_id=second_source["b_event_hash"],
        life=session.product.seed.life,
    )


def make_history_records(session, history_bindings: list[Mapping[str, Any]],
                         as_of: int) -> list[dict]:
    return [
        history_record_from_prior(session, first_binding=row, as_of=as_of)
        for row in history_bindings
    ]


__all__ = [
    "ContinuationProducer",
    "S41EventRefusal",
    "build_ongoing_occurrence",
    "make_history_records",
    "world_prerequisites",
]
