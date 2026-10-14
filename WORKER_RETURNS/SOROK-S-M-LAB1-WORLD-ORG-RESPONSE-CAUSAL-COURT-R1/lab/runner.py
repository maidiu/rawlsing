"""Trial runner: machine-first receipts, cold replay, cost telemetry."""
from __future__ import annotations

import time
from typing import Any, Mapping

from lab.hashutil import canonicalize, semantic_hash, token_estimate
from lab.opacity import build_actor_safe_projection, build_evaluator_metadata
from lab.owners import committed_effects, empty_state
from lab.transition import admit_history, run_transition
from lab.world_fixtures import case_fixture, world_receipt_hash

SEEDS = tuple(f"S{i:02d}" for i in range(1, 13))

AUDIT_OUTPUT_REQUIRED = (
    "case_id",
    "baseline",
    "arm",
    "seed",
    "model_version",
    "world_receipt_hash",
    "admitted_event_hashes",
    "owner_state_before_hash",
    "read_evidence_ref_list",
    "retrieval_token_count",
    "model_call_count",
    "latency_ms",
    "transition_rule_ids",
    "receivability_refs",
    "uptake_refs",
    "recruitment_refs",
    "proposed_effects",
    "authorized_effects",
    "committed_effect_receipts",
    "owner_state_after_hash",
    "actor_safe_projection",
    "actor_claim_permission_refs",
    "memory_access_and_trace_refs",
    "objective_public_standing_effects",
    "present_action_and_material_effects",
    "invalid_and_hold_codes",
    "full_replay_digest",
    "prose_optional",
)


def _position_for(fixture: Mapping[str, Any], contrast: str) -> Mapping[str, Any]:
    positions = fixture.get("positions", {})
    if contrast in positions:
        return positions[contrast]
    return positions.get("default") or positions.get("H_RESPONSIVE") or next(iter(positions.values()))


def run_single(
    *,
    k_id: str,
    contrast: str,
    baseline: str,
    seed: str,
    unissued_weights: Mapping[str, Any] | None = None,
    forced_event: Mapping[str, Any] | None = None,
    forced_c_edge: Mapping[str, Any] | None = None,
    event_override: Mapping[str, Any] | None = None,
    opportunity_override: Mapping[str, Any] | None = None,
    history_override: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """One deterministic trial; returns the strict machine-first receipt."""

    fixture = case_fixture(k_id)
    history = history_override or fixture["histories"][contrast]
    world = fixture["world"]
    position = _position_for(fixture, contrast)
    opportunity = opportunity_override or fixture["opportunity"]
    present_event = dict(event_override or forced_event or fixture["present_event"])

    t0 = time.perf_counter()
    state, history_committed, history_holds, public_standing = admit_history(
        history=history, position=position
    )
    before_hash = state.state_hash()

    outcome = run_transition(
        arm=baseline,
        state=state,
        history_events=list(history.get("events", [])),
        present_event=present_event,
        world=world,
        position=position,
        opportunity=opportunity,
        seed_name=f"{k_id}:{contrast}:{baseline}:{seed}",
        public_standing=public_standing,
        unissued_weights=unissued_weights,
        c_edge=forced_c_edge,
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)

    actor_safe = build_actor_safe_projection(
        state_material=state.material(),
        present_event=present_event,
        selected_route=outcome["selected_route"],
        uptake_refs=outcome["uptake_refs"],
        trace_records=outcome["trace_records"],
        memory_access_refs=outcome["memory_access_and_trace_refs"],
        claim_permission_refs=outcome["actor_claim_permission_refs"],
        invalid_and_hold_codes=outcome["invalid_and_hold_codes"] + history_holds,
    )
    evaluator = build_evaluator_metadata(
        outcome=outcome,
        history_events=list(history.get("events", [])),
    )

    all_committed = history_committed + outcome["committed_effect_receipts"]
    holds = sorted(set(outcome["invalid_and_hold_codes"] + history_holds))
    standing_effects = [
        c for c in all_committed if c["effect_kind"] == "PUBLIC_STANDING_CHANGE"
    ]
    receipt = {
        "case_id": k_id,
        "baseline": baseline,
        "arm": contrast,
        "seed": seed,
        "model_version": outcome["model_version"],
        "world_receipt_hash": world_receipt_hash(world),
        "admitted_event_hashes": [
            semantic_hash(e) for e in history.get("events", [])
        ],
        "owner_state_before_hash": before_hash,
        "read_evidence_ref_list": outcome["read_evidence_ref_list"],
        "retrieval_token_count": outcome["retrieval_token_count"],
        "model_call_count": 0,
        "latency_ms": latency_ms,
        "transition_rule_ids": outcome["transition_rule_ids"],
        "receivability_refs": outcome["receivability_refs"],
        "uptake_refs": outcome["uptake_refs"],
        "recruitment_refs": outcome["recruitment_refs"],
        "proposed_effects": outcome["proposed_effects"],
        "authorized_effects": outcome["authorized_effects"],
        "committed_effect_receipts": all_committed,
        "owner_state_after_hash": outcome["owner_state_after_hash"],
        "actor_safe_projection": actor_safe,
        "actor_claim_permission_refs": outcome["actor_claim_permission_refs"],
        "memory_access_and_trace_refs": outcome["memory_access_and_trace_refs"],
        "objective_public_standing_effects": standing_effects,
        "present_action_and_material_effects": outcome["present_action_and_material_effects"],
        "invalid_and_hold_codes": holds,
        "full_replay_digest": outcome["full_replay_digest"],
        "prose_optional": "MACHINE_FIRST__NO_PROSE_SCORED",
        # lab extension fields (not scored as prose)
        "lab_extension": {
            "selected_route": outcome["selected_route"],
            "selected_not_mandatory": outcome["selected_not_mandatory"],
            "candidate_routes": outcome["candidate_routes"],
            "causal_parent_refs": outcome["causal_parent_refs"],
            "relation_view": outcome["relation_view"],
            "relation_index_cost": outcome["relation_index_cost"],
            "event_local_conation": outcome["event_local_conation"],
            "trace_records": outcome["trace_records"],
            "evaluator_metadata": evaluator,
            "history_effect_receipts": history_committed,
            "present_effect_receipts": outcome["committed_effect_receipts"],
            "public_standing": public_standing,
            "present_event_id": present_event.get("event_id"),
            "position_receipt": position.get("position_receipt"),
            "sanction_capacity": position.get("sanction_capacity"),
        },
    }
    missing = [f for f in AUDIT_OUTPUT_REQUIRED if f not in receipt]
    if missing:
        raise AssertionError(f"receipt missing audit fields: {missing}")
    return receipt


def run_trial_with_replay(**kwargs: Any) -> dict[str, Any]:
    """Run one trial twice from scratch; require identical replay digest."""

    first = run_single(**kwargs)
    second = run_single(**kwargs)
    identical = (
        first["full_replay_digest"] == second["full_replay_digest"]
        and first["owner_state_after_hash"] == second["owner_state_after_hash"]
        and first["actor_safe_projection"] == second["actor_safe_projection"]
    )
    first["lab_extension"]["cold_replay"] = {
        "digest_first": first["full_replay_digest"],
        "digest_second": second["full_replay_digest"],
        "state_hash_first": first["owner_state_after_hash"],
        "state_hash_second": second["owner_state_after_hash"],
        "identical": identical,
    }
    return first
