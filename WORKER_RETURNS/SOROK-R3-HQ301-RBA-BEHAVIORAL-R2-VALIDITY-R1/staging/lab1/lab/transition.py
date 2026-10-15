"""Bounded CAN-008-compatible transition implementation (lab rules T0-T8).

Arms:
  A = minimal world-conditioned event/relation/history + existing owner state
      (CAN010/CAN011/ADP015/ADP016/ADP017) + CAN-008-style recruitment.  No new
      durable conation/recognition/attractor store.
  B = A + event-local conation/recognition/pressure/route-cost projection
      (compiled per event; never persisted; never its own effect parent).
  C = B + minimal typed relational topology (COMPENSATES_FOR /
      CONDITIONS_RECOGNITION) with exact admitted formation parents.

All rules are SYNTHETIC LAB RULES proposed for this experiment only; none is an
adopted causal law.  Selection is deterministic given (state, event, arm, seed);
the seeded RNG only breaks preregistered ties.
"""
from __future__ import annotations

import random
from typing import Any, Mapping

from lab.hashutil import canonicalize, semantic_hash, token_estimate
from lab.owners import (
    OwnerEffectError,
    OwnerState,
    apply_effect,
    effect_receipt,
    empty_state,
)

ARMS = ("A", "B", "C")

HOLD_UNDERSPECIFIED = "UNDERSPECIFIED"
HOLD_NO_WORLD_CONTEXT = "NO_WORLD_CONTEXT"
HOLD_NO_ADMISSION = "UNADMITTED_EVENT"
HOLD_REJECTED = "REJECTED_EVENT"
HOLD_WORLD_MISMATCH = "WORLD_SNAPSHOT_MISMATCH"
INVALID_PUBLIC_STANDING = "NO_OBJECTIVE_PUBLIC_STANDING_FROM_UNEMPOWERED_WITNESS"
INVALID_CATEGORY_SANCTION = "NO_CATEGORY_TO_BEHAVIOR_DIRECT_EDGE"
INVALID_SANCTION_CAPACITY = "NO_SANCTION_ROUTE_OR_CAPACITY"
INVALID_WEIGHT_WITHOUT_ISSUER = "WEIGHT_OR_SEED_WITHOUT_ISSUER"
INVALID_FREE_EDGE = "NO_UNAUTHORIZED_C_GRAPH_EDGE"
INVALID_PRIOR_REWRITE = "NO_REWRITE_PRIOR_EVENTS"
VALID_EMPTY = "VALID_EMPTY"

RULE_T0 = "T0_WORLD_CONTEXT_GATE"
RULE_T1 = "T1_RECEIVABILITY"
RULE_T2 = "T2_SITUATED_RECRUITMENT"
RULE_T3 = "T3_EVENT_LOCAL_CONATION"
RULE_T4 = "T4_RECOGNITION"
RULE_T5 = "T5_CORRECTIVE_REINTERPRETATION"
RULE_T6 = "T6_NONDECLARATIVE_TRACE"
RULE_T7 = "T7_CATEGORY_ENFORCEMENT"
RULE_T8 = "T8_TYPED_TOPOLOGY_OPTION"

COST_RANK = {"NONE": 0, "LOW_TIME": 1, "MEDIUM_TIME": 2, "HIGH_TIME": 3}

# support keys may be qualified: "KEY" or "KEY#STATUS"
ROUTE_SUPPORT_RULES: dict[str, dict[str, list[str]]] = {
    "REQUEST_FEEDBACK": {
        "practice": ["ASK_CLARIFICATION"],
        "expectation": ["SCOPE_HELP_POSSIBLE"],
        "striving": ["VERIFY_TOGETHER"],
    },
    "SILENCE": {
        "expectation": ["SCOPE_SPEAKING_COSTLY"],
        "tension": ["APPROACH_WITHDRAW"],
    },
    "APPEAL": {"tension": ["APPROACH_WITHDRAW"]},
    "HEIGHTENED_GUARD": {"trace": ["TRACE_PUBLIC_SHAMING"]},
    "NEUTRAL_RESPONSE": {},
    "REQUEST_WITH_REPAIR": {"tension": ["APPROVAL_CRITICISM_TENSION"]},
    "REQUEST_WITH_CONDITIONAL_CAUTION": {"tension": ["APPROVAL_CRITICISM_TENSION"]},
    "WITHDRAW_REQUEST": {"expectation": ["SCOPE_APPROVAL_CONDITIONAL"]},
    "NARROWED_CONSULT": {"tension": ["APPROACH_WITHDRAW#NARROWED"]},
    "REPEATED_QUESTION": {"tension": ["APPROACH_WITHDRAW#REINFORCED"]},
    "NO_ACTION": {},
    "ACCEPT_CERTIFICATE": {},
    "REMAIN_DOUBTFUL": {"belief": ["BELIEF_OWN_WORK_UNCERTAIN"]},
    "POLICING_CANDIDATE": {
        "practice": ["PROCEDURE_ENFORCEMENT"],
        "expectation": ["SCOPE_NORM_MUST_HOLD"],
    },
    "NO_SANCTION": {},
}

ROUTE_GOAL_MATCH: dict[str, list[str]] = {
    "REQUEST_FEEDBACK": ["VERIFY_TOGETHER", "SCOPE_HELP_POSSIBLE"],
    "REQUEST_WITH_REPAIR": ["SCOPE_APPROVAL_CONDITIONAL"],
    "NARROWED_CONSULT": ["SCOPE_HELP_POSSIBLE"],
    "REPEATED_QUESTION": ["VERIFY_TOGETHER"],
    "POLICING_CANDIDATE": ["SCOPE_NORM_MUST_HOLD"],
}

ROUTE_RELATION_SUPPORT: dict[str, dict[str, int]] = {
    "COMPENSATES_FOR": {"REQUEST_WITH_REPAIR": 1},
    "CONDITIONS_RECOGNITION": {"REQUEST_WITH_CONDITIONAL_CAUTION": 1},
}

CONTENT_TO_RELATION = {
    "COMPENSATION_READING_FORMED": "COMPENSATES_FOR",
    "CONDITIONAL_RECOGNITION_READING_FORMED": "CONDITIONS_RECOGNITION",
}

ROUTE_GATE = {
    "REQUEST_FEEDBACK": "ASK_CLARIFICATION_PRACTICE_OR_HELP_EXPECTATION",
    "POLICING_CANDIDATE": "VALID_SANCTION_CAPACITY_AND_ROUTE",
    "ACCEPT_CERTIFICATE": "PUBLIC_STANDING_CERTIFIED",
}


def seed_rng(seed_name: str) -> random.Random:
    return random.Random(int(semantic_hash({"seed": seed_name}), 16))


# ---------------------------------------------------------------------------
# T0 world-context gate
# ---------------------------------------------------------------------------

def t0_world_context_gate(
    event: Mapping[str, Any], world: Mapping[str, Any]
) -> tuple[bool, list[str]]:
    codes: list[str] = []
    required = (
        "world_receipt_ref",
        "position_receipt_ref",
        "relationship_ref",
        "opportunity_ref",
        "exposure_ref",
        "history_refs",
        "effective_time",
    )
    missing = [f for f in required if f not in event or event.get(f) in (None, "")]
    if missing:
        codes.append(f"{HOLD_NO_WORLD_CONTEXT}:{','.join(sorted(missing))}")
        return False, codes
    if event.get("admission") == "DRAFT":
        codes.append(HOLD_NO_ADMISSION)
        return False, codes
    if event.get("admission") == "REJECTED":
        codes.append(HOLD_REJECTED)
        return False, codes
    wr = event.get("world_receipt_ref") or {}
    if wr.get("world_id") != world.get("world_id") or wr.get("fixture_hash") != world.get("fixture_hash"):
        codes.append(HOLD_WORLD_MISMATCH)
        return False, codes
    return True, codes


# ---------------------------------------------------------------------------
# relation-view reconstruction (A/B) vs typed index (C)
# ---------------------------------------------------------------------------

def reconstruct_relation_view(events: list[Mapping[str, Any]]) -> dict[str, Any] | None:
    """A/B equivalent-causal-ancestry reconstruction (RECONSTRUCT_REL_VIEW).

    Derived from admitted formation events (exact parents + content token).  No
    new store is created; this is a view over admitted ancestry.
    """

    for ev in events:
        parents = ev.get("formation_parents")
        content = (ev.get("actor_receivable_features") or {}).get("content", "")
        rel_type = CONTENT_TO_RELATION.get(content)
        if parents and rel_type:
            return {
                "edge_id": f"RECONSTRUCTED_{rel_type}",
                "type": rel_type,
                "from": parents[0],
                "to": parents[1] if len(parents) > 1 else None,
                "scope": ev.get("relationship_ref"),
                "formed_by": ev["event_id"],
                "formation_event": ev["event_id"],
                "view_source": "RECONSTRUCTED_FROM_ADMITTED_ANCESTRY",
            }
    return None


def c_relation_edge(history: list[Mapping[str, Any]]) -> dict[str, Any] | None:
    """C's typed relation index: same semantic content as the reconstructed view."""

    view = reconstruct_relation_view(history)
    if view is None:
        return None
    return {
        "edge_id": f"EDGE_{view['type']}",
        "type": view["type"],
        "from": view["from"],
        "to": view["to"],
        "scope": view["scope"],
        "formed_by": view["formation_event"],
        "formation_event": view["formation_event"],
        "view_source": "C_TYPED_RELATION_INDEX",
    }


# ---------------------------------------------------------------------------
# owner-state recruitment
# ---------------------------------------------------------------------------

def _view(state: OwnerState, owner: str) -> dict[str, Any]:
    return getattr(state, owner).get("view", {})


def _stream_recruitment(state: OwnerState, event: Mapping[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for key, entry in _view(state, "CAN010").items():
        kind = "striving" if entry.get("axis") else "expectation"
        refs.append(
            {
                "stream": "CAN010",
                "matched_key": key,
                "match_kind": kind,
                "parent_event_refs": list(entry.get("parent_event_refs", [])),
            }
        )
    for key, entry in _view(state, "CAN011").items():
        kind = "practice" if entry.get("practice") else "tension"
        refs.append(
            {
                "stream": "CAN011",
                "matched_key": key,
                "match_kind": kind,
                "parent_event_refs": list(entry.get("parent_event_refs", [])),
            }
        )
    for key, entry in _view(state, "ADP015").items():
        refs.append(
            {
                "stream": "ADP015",
                "matched_key": key,
                "match_kind": "relationship",
                "parent_event_refs": list(entry.get("parent_event_refs", [])),
            }
        )
    for key, entry in _view(state, "ADP016").items():
        if entry.get("trace_kind") == "NONDECLARATIVE_TRACE" and entry.get("activation") == "RECRUITABLE":
            refs.append(
                {
                    "stream": "ADP016",
                    "matched_key": key,
                    "match_kind": "trace",
                    "parent_event_refs": list(entry.get("parent_event_refs", [])),
                }
            )
        elif key.startswith("EPISODIC_") and entry.get("access_state") == "RECALLABLE":
            refs.append(
                {
                    "stream": "ADP016",
                    "matched_key": key,
                    "match_kind": "episodic",
                    "parent_event_refs": list(entry.get("parent_event_refs", [])),
                }
            )
    for key, entry in _view(state, "ADP017").items():
        if entry.get("content"):
            refs.append(
                {
                    "stream": "ADP017",
                    "matched_key": key,
                    "match_kind": "belief",
                    "parent_event_refs": list(entry.get("parent_event_refs", [])),
                }
            )
    return refs


def _route_support(
    route_id: str,
    state: OwnerState,
    relation_view: Mapping[str, Any] | None,
    recruitment: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    support: list[dict[str, Any]] = []
    rules = ROUTE_SUPPORT_RULES.get(route_id, {})
    views = {
        "practice": _view(state, "CAN011"),
        "tension": _view(state, "CAN011"),
        "expectation": _view(state, "CAN010"),
        "striving": _view(state, "CAN010"),
        "trace": _view(state, "ADP016"),
        "belief": _view(state, "ADP017"),
    }
    for match_kind, specs in rules.items():
        view = views.get(match_kind, {})
        for spec in specs:
            if "#" in spec:
                key, status = spec.split("#", 1)
                entry = view.get(key)
                if entry is not None and entry.get("status") == status:
                    parent = next((r for r in recruitment if r["matched_key"] == key), None)
                    support.append(
                        {
                            "support_kind": match_kind,
                            "support_key": spec,
                            "parent_event_refs": list(parent["parent_event_refs"]) if parent else [],
                        }
                    )
            else:
                if spec in view:
                    parent = next((r for r in recruitment if r["matched_key"] == spec), None)
                    support.append(
                        {
                            "support_kind": match_kind,
                            "support_key": spec,
                            "parent_event_refs": list(parent["parent_event_refs"]) if parent else [],
                        }
                    )
    if relation_view is not None:
        bump = ROUTE_RELATION_SUPPORT.get(relation_view.get("type", ""), {})
        if route_id in bump:
            support.append(
                {
                    "support_kind": "relation_view",
                    "support_key": relation_view.get("type"),
                    "parent_event_refs": [relation_view.get("formation_event")],
                }
            )
    return support


def _gate_route(
    route: Mapping[str, Any],
    state: OwnerState,
    position: Mapping[str, Any],
    public_standing: str,
) -> tuple[bool, str | None]:
    route_id = route["route_id"]
    gate = ROUTE_GATE.get(route_id)
    if gate is None or gate == "NONE":
        return True, None
    if gate == "ASK_CLARIFICATION_PRACTICE_OR_HELP_EXPECTATION":
        ok = "ASK_CLARIFICATION" in _view(state, "CAN011") or "SCOPE_HELP_POSSIBLE" in _view(state, "CAN010")
        return ok, None if ok else "ROUTE_REQUIREMENT_UNMET"
    if gate == "VALID_SANCTION_CAPACITY_AND_ROUTE":
        cap = position.get("sanction_capacity")
        if cap != "VALID_SMALL_SCHEDULE_POWER":
            return False, INVALID_SANCTION_CAPACITY
        if "PROCEDURE_ENFORCEMENT" not in _view(state, "CAN011"):
            return False, INVALID_CATEGORY_SANCTION
        return True, None
    if gate == "PUBLIC_STANDING_CERTIFIED":
        ok = public_standing == "CERTIFIED"
        return ok, None if ok else "ROUTE_REQUIREMENT_UNMET"
    return True, None


# ---------------------------------------------------------------------------
# event-local conation (B/C only, never persisted)
# ---------------------------------------------------------------------------

def _event_local_conation(
    state: OwnerState,
    event: Mapping[str, Any],
    opportunity: Mapping[str, Any],
    witness: Mapping[str, Any] | None,
) -> dict[str, Any]:
    striving = _view(state, "CAN010")
    tensions = {k: v for k, v in _view(state, "CAN011").items() if v.get("poles")}
    routes = []
    for route in opportunity.get("available_routes", []):
        routes.append(
            {
                "route_id": route["route_id"],
                "desired_end_match": [
                    g for g in ROUTE_GOAL_MATCH.get(route["route_id"], []) if g in striving
                ],
                "cost_rank": COST_RANK.get(route.get("cost", "NONE"), 0),
                "cost_label": route.get("cost", "NONE"),
            }
        )
    return {
        "event_id": event.get("event_id"),
        "direction_from_strivings": sorted(striving),
        "witness_stakes": (
            {
                "speaker": (witness or {}).get("speaker"),
                "institutional_power": (witness or {}).get("institutional_power"),
                "relationship_ref": event.get("relationship_ref"),
            }
            if witness
            else None
        ),
        "pressure_conflict": {
            k: {"poles": v.get("poles"), "status": v.get("status")} for k, v in tensions.items()
        },
        "route_configuration": routes,
        "persistence": "EVENT_LOCAL_ONLY__NOT_PERSISTED__NOT_EFFECT_PARENT",
    }


# ---------------------------------------------------------------------------
# history admission with owner gates (T4/T5/T6/T7)
# ---------------------------------------------------------------------------

def validate_effect_gate(
    effect: Mapping[str, Any],
    events_by_id: Mapping[str, Mapping[str, Any]],
) -> tuple[bool, str | None]:
    """Destination-owner gate for one declared durable effect."""

    kind = effect.get("effect_kind", "")
    parents = [events_by_id[p] for p in effect.get("parent_event_refs", []) if p in events_by_id]
    if kind == "PUBLIC_STANDING_CHANGE":
        for ev in parents:
            wit = ev.get("witness") or {}
            if wit.get("institutional_power") == "CAN_RATIFY" and ev.get("kind") == "INSTITUTIONAL_RATIFICATION":
                return True, None
        return False, INVALID_PUBLIC_STANDING
    if kind == "TENSION_REVISED":
        if len(effect.get("parent_event_refs", [])) < 2:
            return False, INVALID_PRIOR_REWRITE
        return True, None
    if kind == "TRACE_FORMED":
        if not effect.get("parent_event_refs"):
            return False, "TRACE_WITHOUT_EXACT_EVENT_PARENT"
        return True, None
    if kind == "SANCTION_ASSIGNMENT_CANDIDATE":
        # candidate-only record; never a committed actual sanction
        return True, None
    if kind == "SANCTION_ASSIGNMENT":
        return False, INVALID_CATEGORY_SANCTION
    return True, None


def admit_history(
    *,
    history: Mapping[str, Any],
    position: Mapping[str, Any],
) -> tuple[OwnerState, list[dict[str, Any]], list[str], str]:
    """Apply admitted owner effects of the history to a fresh owner state.

    Returns (state, committed_effect_receipts, hold_codes, public_standing).
    """

    state = empty_state()
    committed: list[dict[str, Any]] = []
    holds: list[str] = []
    public_standing = "UNCERTIFIED"
    events = list(history.get("events", []))
    events_by_id = {e["event_id"]: e for e in events}
    for effect in history.get("effects", []):
        ok, code = validate_effect_gate(effect, events_by_id)
        if not ok:
            holds.append(f"{code}:{effect['effect_id']}")
            continue
        try:
            pre = state.state_hash()
            record = apply_effect(
                state,
                owner=effect["owner"],
                effect_kind=effect["effect_kind"],
                target_key=effect["target_key"],
                payload=effect["payload"],
                parent_event_refs=tuple(effect["parent_event_refs"]),
                effect_id=effect["effect_id"],
            )
            committed.append(effect_receipt(record, pre, state.state_hash()))
            if effect["effect_kind"] == "PUBLIC_STANDING_CHANGE":
                public_standing = "CERTIFIED"
        except OwnerEffectError as exc:
            holds.append(f"{exc.code}:{effect['effect_id']}")
    return state, committed, holds, public_standing


# ---------------------------------------------------------------------------
# present-event transition
# ---------------------------------------------------------------------------

def run_transition(
    *,
    arm: str,
    state: OwnerState,
    history_events: list[Mapping[str, Any]],
    present_event: Mapping[str, Any],
    world: Mapping[str, Any],
    position: Mapping[str, Any],
    opportunity: Mapping[str, Any],
    seed_name: str,
    public_standing: str = "UNCERTIFIED",
    unissued_weights: Mapping[str, Any] | None = None,
    c_edge: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """One situated transition: admitted occurrence -> response candidate + effects."""

    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}")
    rules_used: list[str] = []
    invalid_and_hold: list[str] = []
    pre_hash = state.state_hash()
    read_refs: list[str] = []
    read_material: list[Any] = []

    if unissued_weights:
        invalid_and_hold.append(INVALID_WEIGHT_WITHOUT_ISSUER)
        return _outcome(
            arm, seed_name, pre_hash, pre_hash, rules_used, invalid_and_hold,
            read_refs, read_material, None, [], [], [], state, present_event, held=True,
        )

    ok, t0_codes = t0_world_context_gate(present_event, world)
    rules_used.append(RULE_T0)
    if not ok:
        invalid_and_hold.extend(t0_codes)
        return _outcome(
            arm, seed_name, pre_hash, pre_hash, rules_used, invalid_and_hold,
            read_refs, read_material, None, [], [], [], state, present_event, held=True,
        )

    read_refs.append(present_event["event_id"])
    read_material.append(present_event)
    read_refs.append(world["world_id"])
    read_material.append(world)

    rules_used.append(RULE_T1)
    receivable = dict(present_event.get("actor_receivable_features") or {})
    receivability_refs = [
        {"ref": f"RECV:{present_event['event_id']}:{k}", "feature": k, "value": v}
        for k, v in sorted(receivable.items())
    ]
    if not receivable:
        invalid_and_hold.append(VALID_EMPTY)

    rules_used.append(RULE_T2)
    recruitment = _stream_recruitment(state, present_event)
    for ref in recruitment:
        read_refs.extend(ref["parent_event_refs"])
    uptake_refs = [
        {"ref": f"UPTAKE:{present_event['event_id']}", "receivable": receivable}
    ]

    relation_view: dict[str, Any] | None
    if arm == "C":
        rules_used.append(RULE_T8)
        relation_view = dict(c_edge) if c_edge is not None else c_relation_edge(history_events)
        if relation_view is not None and relation_view.get("formation_event") not in {
            e.get("event_id") for e in history_events
        }:
            invalid_and_hold.append(INVALID_FREE_EDGE)
            relation_view = None
    else:
        relation_view = reconstruct_relation_view(history_events)
    if relation_view is not None:
        read_refs.append(relation_view.get("formation_event") or "")
        read_material.append(relation_view)

    rules_used.append(RULE_T6)
    trace_records = [
        {"key": k, **v}
        for k, v in sorted(_view(state, "ADP016").items())
        if v.get("trace_kind") == "NONDECLARATIVE_TRACE"
    ]
    memory_access_refs = [
        {"key": k, "access_state": v.get("access_state"), "kind": v.get("trace_kind", "EPISODIC")}
        for k, v in sorted(_view(state, "ADP016").items())
    ]
    claim_permission_refs = [
        {"key": k, "permission": v.get("claim_permission", v.get("permission"))}
        for k, v in sorted(_view(state, "ADP017").items())
    ]

    conation = None
    if arm in ("B", "C"):
        rules_used.append(RULE_T3)
        conation = _event_local_conation(
            state, present_event, opportunity, present_event.get("witness")
        )
        read_material.append(conation)

    proposed_effects: list[dict[str, Any]] = []
    public_standing_effects: list[dict[str, Any]] = []
    action_effects: list[dict[str, Any]] = []

    witness = present_event.get("witness")
    if witness is not None:
        rules_used.append(RULE_T4)
        if witness.get("institutional_power") == "CAN_RATIFY":
            eff = {
                "effect_kind": "PUBLIC_STANDING_CHANGE",
                "target_key": "STANDING_A_TEST",
                "owner": "WORLD_PUBLIC_RECORD",
                "payload": {"standing": "CERTIFIED", "witness": witness.get("speaker")},
                "parent_event_refs": [present_event["event_id"]],
            }
            proposed_effects.append(eff)
            public_standing_effects.append(dict(eff))
        else:
            invalid_and_hold.append(f"{INVALID_PUBLIC_STANDING}:{witness.get('speaker')}")

    candidates = []
    for route in opportunity.get("available_routes", []):
        permitted, gate_code = _gate_route(route, state, position, public_standing)
        support = _route_support(route["route_id"], state, relation_view, recruitment)
        goal_match = [
            g for g in ROUTE_GOAL_MATCH.get(route["route_id"], []) if g in _view(state, "CAN010")
        ]
        candidates.append(
            {
                "route_id": route["route_id"],
                "permitted": permitted,
                "gate_code": gate_code,
                "support": support,
                "support_count": len(support),
                "goal_match": goal_match,
                "cost_rank": COST_RANK.get(route.get("cost", "NONE"), 0),
            }
        )

    permitted = [c for c in candidates if c["permitted"]]
    selected: Mapping[str, Any] | None = None
    no_op_route = opportunity.get("no_op_route")

    def _score(c: dict[str, Any]) -> int:
        if arm == "A":
            return c["support_count"]
        return c["support_count"] + len(c["goal_match"])

    if not permitted:
        invalid_and_hold.append(VALID_EMPTY)
    else:
        best = max(_score(c) for c in permitted)
        if best == 0 and no_op_route:
            # preregistered DEFAULT_TO_NO_OP_WHEN_NO_RECRUITMENT: without any
            # recruitment support the engine takes the declared no-op route.
            selected = next(c for c in permitted if c["route_id"] == no_op_route)
        else:
            tied = [c for c in permitted if _score(c) == best]
            if arm == "A":
                if len(tied) == 1:
                    selected = tied[0]
                else:
                    idx = seed_rng(f"{seed_name}:TIEBREAK").randrange(len(tied))
                    selected = sorted(tied, key=lambda c: c["route_id"])[idx]
            else:
                tied.sort(key=lambda c: (-len(c["goal_match"]), c["route_id"]))
                if len(tied) == 1 or tied[0]["goal_match"] != tied[1]["goal_match"]:
                    selected = tied[0]
                else:
                    selected = tied[seed_rng(f"{seed_name}:TIEBREAK").randrange(len(tied))]

    if selected is not None and selected["route_id"] == "POLICING_CANDIDATE":
        rules_used.append(RULE_T7)
        cap = position.get("sanction_capacity")
        if cap != "VALID_SMALL_SCHEDULE_POWER":
            invalid_and_hold.append(INVALID_CATEGORY_SANCTION)
        else:
            eff = {
                "effect_kind": "SANCTION_ASSIGNMENT_CANDIDATE",
                "target_key": "ACTION_A_TEST",
                "owner": "WORLD_PUBLIC_RECORD",
                "payload": {
                    "action": "SCHEDULE_ADJUSTMENT_CANDIDATE",
                    "status": "CANDIDATE_NOT_MANDATORY",
                    "capacity": cap,
                },
                "parent_event_refs": [present_event["event_id"]],
            }
            proposed_effects.append(eff)
            action_effects.append(dict(eff))

    rules_used.append(RULE_T5)

    outcome = _outcome(
        arm,
        seed_name,
        pre_hash,
        state.state_hash(),
        rules_used,
        invalid_and_hold,
        read_refs,
        read_material,
        selected,
        receivability_refs,
        uptake_refs,
        recruitment,
        state,
        present_event,
        relation_view=relation_view,
        conation=conation,
        candidates=candidates,
        trace_records=trace_records,
        memory_access_refs=memory_access_refs,
        claim_permission_refs=claim_permission_refs,
        public_standing_effect=public_standing_effects,
        action_effects=action_effects,
    )
    outcome["proposed_effects"] = [dict(e) for e in proposed_effects]
    outcome["relation_index_cost"] = (
        {"mode": "C_TYPED_RELATION_INDEX", "edge_lookups": 1, "events_scanned": 0}
        if arm == "C"
        else {
            "mode": "RECONSTRUCT_FROM_ADMITTED_ANCESTRY",
            "edge_lookups": 0,
            "events_scanned": len(history_events),
        }
    )

    committed = []
    authorized: list[dict[str, Any]] = []
    for eff in outcome["proposed_effects"]:
        ok, gate_code = validate_effect_gate(eff, {present_event["event_id"]: present_event})
        if not ok:
            outcome["invalid_and_hold_codes"].append(gate_code or "EFFECT_GATE_REFUSED")
            continue
        try:
            pre = state.state_hash()
            record = apply_effect(
                state,
                owner=eff["owner"],
                effect_kind=eff["effect_kind"],
                target_key=eff["target_key"],
                payload=eff["payload"],
                parent_event_refs=tuple(eff["parent_event_refs"]),
                effect_id=f"EFF_PRESENT_{present_event['event_id']}_{eff['effect_kind']}",
            )
            committed.append(effect_receipt(record, pre, state.state_hash()))
            authorized.append(dict(eff))
        except OwnerEffectError as exc:
            outcome["invalid_and_hold_codes"].append(exc.code)
    outcome["authorized_effects"] = authorized
    outcome["committed_effect_receipts"] = committed
    outcome["owner_state_after_hash"] = state.state_hash()
    outcome["full_replay_digest"] = semantic_hash(
        {
            "pre": pre_hash,
            "post": state.state_hash(),
            "selected": outcome["selected_route"],
            "rules": outcome["transition_rule_ids"],
            "holds": outcome["invalid_and_hold_codes"],
            "causal_parents": outcome["causal_parent_refs"],
        }
    )
    return outcome


def _outcome(
    arm: str,
    seed_name: str,
    pre_hash: str,
    post_hash: str,
    rules_used: list[str],
    invalid_and_hold: list[str],
    read_refs: list[str],
    read_material: list[Any],
    selected: Mapping[str, Any] | None,
    receivability_refs: list[dict[str, Any]],
    uptake_refs: list[dict[str, Any]],
    recruitment: list[dict[str, Any]],
    state: OwnerState,
    present_event: Mapping[str, Any],
    *,
    held: bool = False,
    relation_view: Mapping[str, Any] | None = None,
    conation: Mapping[str, Any] | None = None,
    candidates: list[Mapping[str, Any]] | None = None,
    trace_records: list[Mapping[str, Any]] | None = None,
    memory_access_refs: list[Mapping[str, Any]] | None = None,
    claim_permission_refs: list[Mapping[str, Any]] | None = None,
    public_standing_effect: list[Mapping[str, Any]] | None = None,
    action_effects: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    parent_refs: list[str] = []
    for ref in recruitment:
        parent_refs.extend(ref.get("parent_event_refs", []))
    if selected is not None:
        for s in selected.get("support", []):
            parent_refs.extend(s.get("parent_event_refs", []))
    return {
        "arm": arm,
        "seed": seed_name,
        "held": held,
        "selected_route": None if selected is None else selected["route_id"],
        "selected_not_mandatory": bool(
            selected and selected["route_id"] == "POLICING_CANDIDATE"
        ),
        "candidate_routes": list(candidates or []),
        "transition_rule_ids": sorted(set(rules_used)),
        "receivability_refs": receivability_refs,
        "uptake_refs": uptake_refs,
        "recruitment_refs": recruitment,
        "causal_parent_refs": sorted(set(parent_refs)),
        "proposed_effects": [],
        "authorized_effects": [],
        "committed_effect_receipts": [],
        "owner_state_before_hash": pre_hash,
        "owner_state_after_hash": post_hash,
        "invalid_and_hold_codes": sorted(set(invalid_and_hold)),
        "full_replay_digest": semantic_hash(
            {
                "pre": pre_hash,
                "post": post_hash,
                "selected": None if selected is None else selected["route_id"],
                "rules": sorted(set(rules_used)),
                "holds": sorted(set(invalid_and_hold)),
                "causal_parents": sorted(set(parent_refs)),
            }
        ),
        "relation_view": dict(relation_view) if relation_view else None,
        "event_local_conation": canonicalize(conation) if conation else None,
        "relation_index_cost": {"mode": "NONE", "edge_lookups": 0, "events_scanned": 0},
        "trace_records": list(trace_records or []),
        "memory_access_and_trace_refs": list(memory_access_refs or []),
        "actor_claim_permission_refs": list(claim_permission_refs or []),
        "objective_public_standing_effects": list(public_standing_effect or []),
        "present_action_and_material_effects": list(action_effects or []),
        "read_evidence_ref_list": sorted({r for r in read_refs if r}),
        "retrieval_token_count": token_estimate(read_material),
        "model_call_count": 0,
        "model_version": "MODEL_BEHAVIORAL_COMPARISON_HOLD__NO_PINNED_MODEL_SURFACE",
    }
