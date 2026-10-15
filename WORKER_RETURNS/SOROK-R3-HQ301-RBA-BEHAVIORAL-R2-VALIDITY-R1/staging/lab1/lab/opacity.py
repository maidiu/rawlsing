"""Actor-opacity machinery: actor-safe projection vs evaluator-only graph.

The actor-safe projection is a strict derivative of ADP016 accessibility and
ADP017 claim permissions.  Evaluator-only metadata may carry the full causal
graph, including hidden causal origins; injecting such an origin must leave the
actor-safe payload byte-identical.  Self-explanations are actor testimony, never
analyst truth.
"""
from __future__ import annotations

from typing import Any, Mapping

from lab.hashutil import canonical_json, canonicalize

EXPLANATION_MODES = (
    "NO_EXPLANATION",
    "MISTAKEN_EXPLANATION_BELIEVED",
    "WRONGLY_CONFIDENT_EXPLANATION",
)

NON_DISCLOSABLE = "NON_DISCLOSABLE_ORIGIN"


def build_actor_safe_projection(
    *,
    state_material: Mapping[str, Any],
    present_event: Mapping[str, Any],
    selected_route: str | None,
    uptake_refs: list[Mapping[str, Any]],
    trace_records: list[Mapping[str, Any]],
    memory_access_refs: list[Mapping[str, Any]],
    claim_permission_refs: list[Mapping[str, Any]],
    invalid_and_hold_codes: list[str],
) -> dict[str, Any]:
    """Actor-visible content only.  No evaluator graph, no hidden origins."""

    adp016 = state_material.get("ADP016", {})
    adp017 = state_material.get("ADP017", {})
    memory_view = []
    for key, entry in sorted((adp016.get("view") or {}).items()):
        if entry.get("trace_kind") == "NONDECLARATIVE_TRACE":
            memory_view.append(
                {
                    "key": key,
                    "kind": "NONDECLARATIVE_TRACE_EFFECT_PRESENT",
                    "recall_granted": False,
                    "origin": NON_DISCLOSABLE,
                }
            )
        else:
            access = entry.get("access_state")
            if access == "RECALLABLE":
                memory_view.append(
                    {
                        "key": key,
                        "kind": "EPISODIC",
                        "recall_granted": True,
                        "origin": NON_DISCLOSABLE,
                    }
                )
            else:
                memory_view.append(
                    {
                        "key": key,
                        "kind": "EPISODIC",
                        "recall_granted": False,
                        "origin": NON_DISCLOSABLE,
                    }
                )
    beliefs = []
    for key, entry in sorted((adp017.get("view") or {}).items()):
        if entry.get("content"):
            beliefs.append(
                {
                    "belief_key": key,
                    "content": entry.get("content"),
                    "warrant": entry.get("warrant"),
                    "confidence": entry.get("confidence"),
                    "claim_permission": entry.get("claim_permission", "OWN_STATE_ONLY"),
                    "parent_event_refs": [],
                }
            )
    return {
        "schema": "LAB_ACTOR_SAFE_PROJECTION@1",
        "present_reception": canonicalize(dict(present_event.get("actor_receivable_features") or {})),
        "present_event_id": present_event.get("event_id"),
        "selected_route": selected_route,
        "memory_view": memory_view,
        "beliefs": beliefs,
        "claim_permissions": [
            {"key": c["key"], "permission": c["permission"]} for c in claim_permission_refs
        ],
        "uptake_refs": canonicalize(list(uptake_refs)),
        "invalid_and_hold_codes": sorted(set(invalid_and_hold_codes)),
        "hidden_origin_refs": [],
    }


def build_evaluator_metadata(
    *,
    outcome: Mapping[str, Any],
    history_events: list[Mapping[str, Any]],
    hidden_causal_origin: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Full analyst-side graph.  Never copied into the actor-safe projection."""

    meta = {
        "schema": "LAB_EVALUATOR_METADATA@1",
        "full_causal_parent_refs": outcome.get("causal_parent_refs"),
        "history_event_ids": [e["event_id"] for e in history_events],
        "recruitment_refs": outcome.get("recruitment_refs"),
        "relation_view": outcome.get("relation_view"),
        "event_local_conation": outcome.get("event_local_conation"),
        "trace_records": outcome.get("trace_records"),
        "hidden_causal_origin": None,
    }
    if hidden_causal_origin is not None:
        meta["hidden_causal_origin"] = canonicalize(dict(hidden_causal_origin))
    return meta


def actor_safe_unchanged_by_hidden_origin(
    *,
    state_material: Mapping[str, Any],
    present_event: Mapping[str, Any],
    selected_route: str | None,
    uptake_refs: list[Mapping[str, Any]],
    trace_records: list[Mapping[str, Any]],
    memory_access_refs: list[Mapping[str, Any]],
    claim_permission_refs: list[Mapping[str, Any]],
    invalid_and_hold_codes: list[str],
    hidden_causal_origin: Mapping[str, Any],
) -> dict[str, Any]:
    """Hard opacity check: evaluator-only origin injection must not move the payload."""

    base = build_actor_safe_projection(
        state_material=state_material,
        present_event=present_event,
        selected_route=selected_route,
        uptake_refs=uptake_refs,
        trace_records=trace_records,
        memory_access_refs=memory_access_refs,
        claim_permission_refs=claim_permission_refs,
        invalid_and_hold_codes=invalid_and_hold_codes,
    )
    meta = build_evaluator_metadata(
        outcome={"causal_parent_refs": [], "recruitment_refs": [], "trace_records": trace_records},
        history_events=[],
        hidden_causal_origin=hidden_causal_origin,
    )
    after = build_actor_safe_projection(
        state_material=state_material,
        present_event=present_event,
        selected_route=selected_route,
        uptake_refs=uptake_refs,
        trace_records=trace_records,
        memory_access_refs=memory_access_refs,
        claim_permission_refs=claim_permission_refs,
        invalid_and_hold_codes=invalid_and_hold_codes,
    )
    identical = canonical_json(base) == canonical_json(after)
    return {
        "check": "INJECTED_HIDDEN_ORIGIN_EVALUATOR_ONLY",
        "actor_safe_byte_identical": identical,
        "payload_sha256": __import__("hashlib").sha256(canonical_json(base).encode()).hexdigest(),
        "evaluator_hidden_origin_present": meta["hidden_causal_origin"] is not None,
        "pass": identical and meta["hidden_causal_origin"] is not None,
    }


def actor_testimony(
    *,
    mode: str,
    machine_identified_parent_refs: list[str],
    mistaken_claim: str = "I acted because the supervisor dislikes me",
    adp017_warrant: str = "ACTOR_TESTIMONY_MISTAKEN_ADMITTED",
) -> dict[str, Any]:
    """Record an actor self-explanation as testimony, never as analyst truth."""

    if mode not in EXPLANATION_MODES:
        raise ValueError(f"unknown explanation mode {mode!r}")
    if mode == "NO_EXPLANATION":
        return {
            "mode": mode,
            "utterance": None,
            "claim_parent_refs": [],
            "machine_identified_parent_refs": list(machine_identified_parent_refs),
            "objective_effects_changed": False,
            "status": "NO_UTTERANCE_REQUIRED",
        }
    return {
        "mode": mode,
        "utterance": mistaken_claim,
        "claim_parent_refs": ["CLAIMED_PARENT_SUPERVISOR_DISLIKES_ME"],
        "machine_identified_parent_refs": list(machine_identified_parent_refs),
        "warrant": adp017_warrant,
        "confidence": "HIGH" if mode == "WRONGLY_CONFIDENT_EXPLANATION" else "MODERATE",
        "objective_effects_changed": False,
        "status": "ADMITTED_ACTOR_TESTIMONY__NOT_ANALYST_TRUTH",
        "separately_admitted": mode == "WRONGLY_CONFIDENT_EXPLANATION",
    }
