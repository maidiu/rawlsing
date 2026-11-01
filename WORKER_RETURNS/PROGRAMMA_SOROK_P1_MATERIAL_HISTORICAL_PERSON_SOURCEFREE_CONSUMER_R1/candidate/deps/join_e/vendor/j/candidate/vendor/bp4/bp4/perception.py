"""Actor-limited V2 claim ingress over the current M6 actor-safe contract.

Only events actually recorded as perceived by an actor may become user-visible
claims. The M6 ingress is executed for each requested claim; a non-perceived
event is typed NONRENDERABLE rather than inferred. The actor can be wrong or
uninformed; objective world truth is never exposed merely because the user asks.
"""
from __future__ import annotations

from typing import Any

from rawlsing_next.m6_actor_safe_expression import (
    ActorSafeRef,
    ReceiverSnapshot,
    evaluate_actor_safe_ingress,
    make_actor_safe_claim_entry,
    make_actor_accessible_render_envelope,
    make_replay_closure,
)

from .canon import digest


class PerceptionRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def claim_ref(event: dict) -> ActorSafeRef:
    return ActorSafeRef("C12_WORLD_EVENT", event["event_id"], event["hash"])


def _state_hashes(actor_id: str, clock: int, state: dict) -> dict:
    world = state["world"]
    actor_rows = state["actors"][actor_id]
    knowledge = sorted(state.get("knowledge", {}).get(actor_id, []))
    episodes = [e for e in state.get("episodes", []) if e["actor_id"] == actor_id]
    return {
        "source_generated_person_record_hash": digest(
            {"actor": actor_id, "history": actor_rows.get("history_hash", ""),
             "grade": "TEST_ONLY_SOURCEFREE_C12"}),
        "source_actor_state_hash": digest(actor_rows.get("state", {})),
        "source_memory_state_hash": digest({"knowledge": knowledge}),
        "source_epistemic_state_hash": digest(
            {"perception": state.get("perceptions", {}).get(actor_id, [])}),
        "exact_causal_parent_sequence_ref_hash": digest(
            [e["hash"] for e in episodes]),
        "clock": int(clock),
        "world_hash": world.get("hash", ""),
    }


def render_perceived_claims(actor_id: str, clock: int, state: dict,
                           events: list[dict]) -> dict:
    """Return user-visible claims approved by the actual M6 ingress."""
    perceived_ids = set(state.get("knowledge", {}).get(actor_id, []))
    perceived = [e for e in events if e["event_id"] in perceived_ids]
    if not perceived:
        return {"state": "VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS",
                "claims": [], "refused": []}
    hashes = _state_hashes(actor_id, clock, state)
    refs = [claim_ref(e) for e in perceived]
    entries = []
    for event, ref in zip(perceived, refs):
        entries.append(make_actor_safe_claim_entry(
            claim_ref=ref,
            stance_record_ref=ActorSafeRef("C12_STANCE", event["event_id"], event["hash"]),
            accessibility_state="CLAIM_ACCESSIBLE",
            first_person_permission="PERMIT_FIRST_PERSON_KNOWLEDGE",
            actor_perceived_view_refs=(ref,),
            source_transition_refs=(ActorSafeRef("C12_EVENT_SOURCE", event["event_id"], event["hash"]),),
        ))
    closure = make_replay_closure(
        actor_id=actor_id,
        as_of_causal_time=clock,
        source_generated_person_record_hash=hashes["source_generated_person_record_hash"],
        source_actor_state_hash=hashes["source_actor_state_hash"],
        source_memory_state_hash=hashes["source_memory_state_hash"],
        source_epistemic_state_hash=hashes["source_epistemic_state_hash"],
        exact_causal_parent_sequence_ref_hash=hashes["exact_causal_parent_sequence_ref_hash"],
        causal_event_or_generated_fact_state_refs=refs,
        actor_perceived_view_refs=refs,
        entry_hashes=tuple(entry.entry_hash for entry in entries),
    )
    envelope = make_actor_accessible_render_envelope(
        actor_id=actor_id,
        as_of_causal_time=clock,
        source_generated_person_record_hash=hashes["source_generated_person_record_hash"],
        source_actor_state_hash=hashes["source_actor_state_hash"],
        source_memory_state_hash=hashes["source_memory_state_hash"],
        source_epistemic_state_hash=hashes["source_epistemic_state_hash"],
        replay_closure=closure,
        allowed_claim_entries=tuple(entries),
    )
    bindings: dict[str, str] = {}
    for entry in entries:
        for bound in (entry.stance_record_ref, *entry.memory_refs,
                      *entry.actor_perceived_view_refs, *entry.source_transition_refs):
            bindings[bound.key] = actor_id
    receiver = ReceiverSnapshot(
        actor_id=actor_id,
        causal_time=clock,
        source_generated_person_record_hash=hashes["source_generated_person_record_hash"],
        source_actor_state_hash=hashes["source_actor_state_hash"],
        source_memory_state_hash=hashes["source_memory_state_hash"],
        source_epistemic_state_hash=hashes["source_epistemic_state_hash"],
        ref_actor_bindings=bindings,
    )
    claims = []
    refused = []
    for event, ref in zip(perceived, refs):
        decision = evaluate_actor_safe_ingress(envelope, closure, receiver, ref)
        if decision.positive_semantics:
            claims.append({
                "event_id": event["event_id"],
                "kind": event["kind"],
                "clock": event["clock"],
                "summary": event["summary"],
                "m6_receiver_state": decision.receiver_state.value,
                "m6_permission": decision.first_person_permission,
                "claim_hash": decision.entry_hash,
            })
        else:
            refused.append({"event_id": event["event_id"],
                            "m6_receiver_state": decision.receiver_state.value})
    return {"state": "READY" if claims else "NONRENDERABLE",
            "claims": claims, "refused": refused}


def render_requested_event(actor_id: str, clock: int, state: dict,
                          events: list[dict], event_id: str) -> dict:
    perceived_ids = set(state.get("knowledge", {}).get(actor_id, []))
    if event_id not in perceived_ids:
        return {"state": "NONRENDERABLE", "code": "NO_ACTOR_PERCEPTION",
                "event_id": event_id}
    selected = [e for e in events if e["event_id"] == event_id]
    if not selected:
        return {"state": "NONRENDERABLE", "code": "EVENT_NOT_IN_BRANCH",
                "event_id": event_id}
    rendered = render_perceived_claims(actor_id, clock, state, selected)
    if rendered["state"] != "READY":
        return {"state": "NONRENDERABLE", "code": rendered["state"],
                "event_id": event_id}
    return {"state": "READY", "event_id": event_id, **rendered["claims"][0]}
