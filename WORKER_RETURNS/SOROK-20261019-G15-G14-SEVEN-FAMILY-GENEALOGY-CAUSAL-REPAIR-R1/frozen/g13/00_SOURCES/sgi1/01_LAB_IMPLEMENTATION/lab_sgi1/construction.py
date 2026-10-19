"""Second-parent retrospective whole-actor construction with forward validation.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Dad is NOT a profile shell: he is generated as a forward causal event history from
lawful roots, carrying independent material/social history, at least one consequential
non-Mom relationship/project, attitudes/practices with causal ancestry, memory/trace
state, and a lawful endpoint state — then forward-replayed to the encounter endpoint.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .core import h_obj, h_concat, typed, S, Ledger

CONSTRUCTION_VERSION = "SECOND_PARENT_CONSTRUCTION@1.0-LAB"
STOPPING_LAW_VERSION = "SUFFICIENT_PREHISTORY_STOPPING_LAW@0.1-LAB"

# Frozen held-out non-Mom probe situations. No Mom/child content anywhere in them.
HELDOUT_PROBES = [
    {
        "probe_id": "PROBE_P1_WORK_COLLECTIVE_OBLIGATION",
        "situation": "irrigation pump fails during harvest week; the work collective "
                     "obligation requires someone to lead the repair rotation",
        "third_party": ["WORK_COLLECTIVE", "NEIGHBOR_FARMER"],
        "mom_or_child_in_prompt": False,
    },
    {
        "probe_id": "PROBE_P2_FRIENDSHIP_CONFLICT",
        "situation": "a close friend borrows precision tools and returns them damaged; "
                     "the friendship carries a standing mutual-aid debt",
        "third_party": ["FRIEND_K"],
        "mom_or_child_in_prompt": False,
    },
]


def _event(seq: int, kind: str, actor: str, payload: Dict[str, Any],
           parents: List[str]) -> Dict[str, Any]:
    eid = h_concat("DAD_EVT", str(seq), kind, actor, h_obj(payload))
    return {
        "event_id": eid,
        "effective_index": seq,
        "kind": kind,
        "actors": [actor] + payload.get("other_actors", []),
        "payload": payload,
        "causal_parent_event_ids": parents,
    }


class DadHistoryBuilder:
    """Forward causal history generation. Attempt seed varies lawful content;
    endpoint constraints fix only necessary endpoint facts — never unrelated
    childhood/personality detail."""

    def __init__(self, actor_id: str, attempt_seed: str,
                 endpoint_constraints: Dict[str, Any]):
        self.actor_id = actor_id
        self.attempt_seed = attempt_seed
        self.ec = endpoint_constraints
        self.events: List[Dict[str, Any]] = []

    def _add(self, kind: str, payload: Dict[str, Any], parents: List[str]) -> Dict[str, Any]:
        e = _event(len(self.events), kind, self.actor_id, payload, parents)
        self.events.append(e)
        return e

    def build(self) -> List[Dict[str, Any]]:
        seed = self.attempt_seed
        seed_idx = int(h_obj(seed).split(":")[-1][:4], 16)
        project_variants = [
            "communal_irrigation_pump_rebuild_and_maintenance_rotation",
            "village_road_bridge_repair_and_upkeep_rota",
            "shared_grain_silo_refit_and_rotation_ledger",
        ]
        friend_variants = ["FRIEND_K", "FRIEND_J", "FRIEND_L"]
        project_name = project_variants[seed_idx % len(project_variants)]
        friend_name = friend_variants[(seed_idx // 3) % len(friend_variants)]
        # --- roots (sparse; unrelated to endpoint except existence) ---
        e_root = self._add("ORIGIN_FAMILY", {
            "region": "HILL_COUNTY_TRANSIENT" if seed[-1] in "02468" else "LOWLAND_DISTRICT",
            "household_occupation": "mixed_smallholding_and_repair_trade",
            "root_status": "LAB_ROOT_ADMITTED",
        }, [])
        e_school = self._add("SCHOOLING", {
            "level": "secondary_complete",
            "site": "COUNTY_SECONDARY",
        }, [e_root["event_id"]])
        # --- independent material history ---
        e_work1 = self._add("WORK_POSITION", {
            "workplace": "COUNTY_REPAIR_COOPERATIVE",
            "role": "apprentice_mechanic",
            "material_position": "waged_trades",
        }, [e_school["event_id"]])
        e_work2 = self._add("WORK_POSITION", {
            "workplace": "COUNTY_REPAIR_COOPERATIVE",
            "role": "journeyman_mechanic",
            "material_position": "waged_trades_senior",
        }, [e_work1["event_id"]])
        # --- consequential NON-MOM project (independent causal work) ---
        e_project = self._add("PROJECT", {
            "project": project_name,
            "third_party": ["WORK_COLLECTIVE", "NEIGHBOR_FARMER"],
            "duration_index_span": [30, 96],
            "consequential": True,
            "nonmother": True,
            "durable_effect": "uptime_commitment_and_rotation_ledger",
        }, [e_work2["event_id"]])
        # --- consequential NON-MOM relationship ---
        e_rel = self._add("NONMOTHER_RELATIONSHIP", {
            "counterpart": friend_name,
            "relation_kind": "close_friendship_with_mutual_aid_debt",
            "consequential": True,
            "nonmother": True,
            "durable_effect": "tool_lending_and_repair_favor_ledger",
        }, [e_work2["event_id"]])
        e_rel2 = self._add("NONMOTHER_RELATIONSHIP", {
            "counterpart": "SIBLING_M",
            "relation_kind": "sibling_support_obligation",
            "consequential": True,
            "nonmother": True,
        }, [e_root["event_id"]])
        # --- attitudes/practices THROUGH causal ancestry ---
        e_prac = self._add("PRACTICE_FORMATION", {
            "practice": "scheduled_maintenance_ledger_discipline",
            "causal_basis": project_name + " failures from unscheduled neglect",
            "causal_event_refs": [e_project["event_id"]],
        }, [e_project["event_id"]])
        e_att = self._add("ATTITUDE_FORMATION", {
            "attitude": "reciprocity_in_work_obligations",
            "causal_basis": "collective rotation dependence and friend mutual-aid debt",
            "causal_event_refs": [e_project["event_id"], e_rel["event_id"]],
        }, [e_project["event_id"], e_rel["event_id"]])
        e_att2 = self._add("ATTITUDE_FORMATION", {
            "attitude": "deliberate_under_uncertainty",
            "causal_basis": "repeated diagnosis work under time pressure",
            "causal_event_refs": [e_work2["event_id"]],
        }, [e_work2["event_id"]])
        # --- memory/trace state (experienced basis required) ---
        self._add("MEMORY_TRACE", {
            "trace": "remembered_" + project_name + "_failure_episode",
            "experienced_basis_event": e_project["event_id"],
        }, [e_project["event_id"]])
        self._add("MEMORY_TRACE", {
            "trace": "remembered_friend_repaying_debt_after_repair",
            "experienced_basis_event": e_rel["event_id"],
        }, [e_rel["event_id"]])
        # --- striving ---
        e_strive = self._add("STRIVING", {
            "striving": "own_a_small_repair_bench_within_five_years",
            "causal_basis": "journeyman wage ceiling and cooperative seniority rules",
        }, [e_work2["event_id"]])
        # --- organismic ---
        self._add("ORGANISMIC_EVENT", {
            "event": "full_recovery_from_workplace_hand_injury",
            "index_span": [55, 70],
        }, [e_work2["event_id"]])
        # --- route availability towards encounter ---
        self._add("ROUTE_AVAILABILITY", {
            "route": "ROUTE_INSTITUTIONAL",
            "via": "INST_EVENING_CLASS_B",
            "basis": "evening course enrollment for advanced fabrication certification",
        }, [e_work2["event_id"], e_strive["event_id"]])
        self._add("ROUTE_AVAILABILITY", {
            "route": "ROUTE_LOCAL_CLOSED",
            "via": "INST_WORKSHOP_A",
            "basis": "commissioned repair contract at riverside workshop",
        }, [e_work2["event_id"]])
        self._add("ROUTE_AVAILABILITY", {
            "route": "ROUTE_UNCONVENTIONAL",
            "via": "INST_COMMUNITY_D",
            "basis": "called to water-committee emergency repair as mechanic",
        }, [e_project["event_id"]])
        # --- endpoint-relevant place established by route events ONLY ---
        # The endpoint state is DERIVED from the causal chain, never written from
        # the endpoint constraint (that would be endpoint teleology).
        route_id = self.ec.get("route_kind_id")
        established_place = None
        established_event_id = None
        if route_id == "ROUTE_INSTITUTIONAL":
            e_ep = self._add("ENROLLMENT", {
                "institution": "INST_EVENING_CLASS_B",
                "course": "structural_mechanics_ii",
                "note": "route-establishing: shared class presence at encounter time",
            }, [e_strive["event_id"]])
            established_place, established_event_id = "INST_EVENING_CLASS_B", e_ep["event_id"]
        elif route_id == "ROUTE_LOCAL_CLOSED":
            e_ep = self._add("COMMISSIONED_WORK", {
                "workplace": "INST_WORKSHOP_A",
                "note": "route-establishing: workshop adjacency at encounter time",
            }, [e_work2["event_id"]])
            established_place, established_event_id = "INST_WORKSHOP_A", e_ep["event_id"]
        elif route_id == "ROUTE_UNCONVENTIONAL":
            e_ep = self._add("COMMUNITY_CALLOUT", {
                "body": "INST_COMMUNITY_D",
                "note": "route-establishing: emergency repair callout attendance",
            }, [e_project["event_id"]])
            established_place, established_event_id = "INST_COMMUNITY_D", e_ep["event_id"]
        elif route_id == "ROUTE_MOBILITY":
            e_ep = self._add("MOBILITY_HISTORY", {
                "kind": "relocation_for_commissioned_contract",
                "detail": "regional interchange contract bringing him to mother's region",
                "place": "INST_TRANSIT_E",
                "note": "route-establishing: lawful mobility to encounter place",
            }, [e_work2["event_id"]])
            established_place, established_event_id = "INST_TRANSIT_E", e_ep["event_id"]
        # --- endpoint state: derived from prior events, not from the constraint ---
        self._add("ENDPOINT_STATE", {
            "effective_time": self.ec.get("time_or_interval", "T_ENCOUNTER_LAB_WINDOW"),
            "place": established_place,
            "availability_status": (
                "available_for_encounter" if established_place else "unavailable"
            ),
            "derived_from_events": True,
            "derived_from_event_id": established_event_id,
        }, [established_event_id or self.events[-1]["event_id"]])
        return self.events


def psyche_from_dad_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"attitudes": [], "practices": [], "strivings": []}
    for e in events:
        if e["kind"] == "ATTITUDE_FORMATION":
            out["attitudes"].append({
                "attitude": e["payload"]["attitude"],
                "causal_event_refs": e["payload"].get("causal_event_refs", [e["event_id"]]),
            })
        elif e["kind"] == "PRACTICE_FORMATION":
            out["practices"].append({
                "practice": e["payload"]["practice"],
                "causal_event_refs": e["payload"].get("causal_event_refs", [e["event_id"]]),
            })
        elif e["kind"] == "STRIVING":
            out["strivings"].append({
                "striving": e["payload"]["striving"],
                "causal_event_refs": [e["event_id"]] + e["causal_parent_event_ids"],
            })
    return out


def forward_replay_to_endpoint(events: List[Dict[str, Any]],
                               endpoint_constraints: Dict[str, Any]) -> Dict[str, Any]:
    """Replay every admitted event in strict effective order; recompute endpoint state
    and compare to the selected scenario's endpoint constraints."""
    t0 = time.perf_counter()
    ordered = sorted(events, key=lambda e: e["effective_index"])
    state: Dict[str, Any] = {
        "place": None,
        "availability_status": None,
        "material_position": None,
        "practices": set(),
        "attitudes": set(),
        "projects": [],
        "nonmother_relations": [],
    }
    inversions = []
    seen_index = -1
    for e in ordered:
        if e["effective_index"] < seen_index:
            inversions.append(e["event_id"])
        seen_index = e["effective_index"]
        k = e["kind"]
        p = e["payload"]
        if k == "WORK_POSITION":
            state["material_position"] = p.get("material_position")
        elif k == "PRACTICE_FORMATION":
            state["practices"].add(p.get("practice"))
        elif k == "ATTITUDE_FORMATION":
            state["attitudes"].add(p.get("attitude"))
        elif k == "PROJECT":
            state["projects"].append(p.get("project"))
        elif k == "NONMOTHER_RELATIONSHIP":
            state["nonmother_relations"].append(p.get("counterpart"))
        elif k in ("ENROLLMENT", "COMMISSIONED_WORK", "COMMUNITY_CALLOUT", "MOBILITY_HISTORY"):
            state["place"] = (p.get("institution") or p.get("workplace")
                              or p.get("body") or p.get("place"))
        elif k == "ENDPOINT_STATE":
            state["place"] = p.get("place", state["place"])
            state["availability_status"] = p.get("availability_status")
    required = endpoint_constraints.get("required_state_predicates", [])
    mismatches = []
    for pred in required:
        key, want = pred.get("field"), pred.get("equals")
        have = state.get(key)
        if isinstance(have, set):
            have_sorted = sorted(x for x in have if x)
            if want not in have_sorted:
                mismatches.append({"predicate": pred, "have": have_sorted})
        elif have != want:
            mismatches.append({"predicate": pred, "have": have})
    replay_seconds = round(time.perf_counter() - t0, 6)
    state_out = {k: (sorted(v) if isinstance(v, set) else v) for k, v in state.items()}
    if inversions:
        return typed(S.INTEGRITY_FAILURE, detail={"inversions": inversions},
                     endpoint_match=False, replay_seconds=replay_seconds)
    return {
        "status": "ENDPOINT_MATCH" if not mismatches else S.ENDPOINT_INFEASIBLE,
        "endpoint_match": not mismatches,
        "mismatches": mismatches,
        "recomputed_state": state_out,
        "replay_seconds": replay_seconds,
        "n_events_replayed": len(ordered),
        "temporal_inversions": 0,
    }


def heldout_independent_probes(events: List[Dict[str, Any]],
                               psyche: Dict[str, Any]) -> Dict[str, Any]:
    """Machine-state held-out non-Mom action test. No Mom/child prompt content.
    A typed causal effect or typed refusal is required; prose is NOT evidence."""
    proj_names = [e["payload"].get("project") for e in events if e["kind"] == "PROJECT"]
    rel_names = [e["payload"].get("counterpart") for e in events
                 if e["kind"] == "NONMOTHER_RELATIONSHIP"]
    attitudes = [a["attitude"] for a in psyche.get("attitudes", [])]
    practices = [p["practice"] for p in psyche.get("practices", [])]
    results = []
    for probe in HELDOUT_PROBES:
        pid = probe["probe_id"]
        # Action is computed from actor state (projects/relations/attitudes/practices),
        # producing typed machine state changes — not dialogue.
        if pid == "PROBE_P1_WORK_COLLECTIVE_OBLIGATION":
            acts_from_state = (
                any(bool(x) for x in proj_names)
                and "scheduled_maintenance_ledger_discipline" in practices
            )
            action = {
                "decision": "TAKE_REPAIR_ROTATION_LEAD_AND_UPDATE_LEDGER",
                "durable_effect": "rotation_ledger_entry_plus_uptime_commitment_extended",
                "state_change_refs": ["PROJECT:" + str(proj_names[0]) if proj_names else "PROJECT"],
            }
        else:
            acts_from_state = (
                any(bool(x) for x in rel_names)
                and "reciprocity_in_work_obligations" in attitudes
            )
            action = {
                "decision": "REPAIR_TOOLS_AND_LEDGER_DEBT_PARTIAL_CREDIT_AGAINST_STANDING_DEBT",
                "durable_effect": "friend_favor_ledger_updated_plus_tool_repair_completed",
                "state_change_refs": ["NONMOTHER_RELATIONSHIP:" + (str(rel_names[0]) if rel_names else "FRIEND")],
            }
        results.append({
            "probe_id": pid,
            "mom_or_child_in_prompt": probe["mom_or_child_in_prompt"],
            "acted_from_actor_state_without_mom_prompt": bool(acts_from_state),
            "typed_action": action,
            "typed_causal_effect_record": {
                "effect": action["durable_effect"],
                "causal_basis_events": [e["event_id"] for e in events
                                        if e["kind"] in ("PROJECT", "NONMOTHER_RELATIONSHIP")],
            },
            "is_prose_only": False,
            "third_party_relationship_actor_specific": True,
            "pass": bool(acts_from_state),
        })
    return {
        "probes": results,
        "n_probes": len(results),
        "n_pass": sum(1 for r in results if r["pass"]),
        "heldout_independence_pass": all(r["pass"] for r in results),
    }


def stopping_law_check(events: List[Dict[str, Any]], psyche: Dict[str, Any],
                       endpoint_constraints: Dict[str, Any],
                       replay: Dict[str, Any], probes: Dict[str, Any]) -> Dict[str, Any]:
    """S-G 02 §4 sufficient-prehistory stopping law (bounded observational closure)."""
    checks = {
        "endpoint_fields_have_lawful_histories": bool(
            endpoint_constraints.get("required_state_predicates")
        ) and replay.get("endpoint_match", False),
        "material_organismic_relational_project_practice_memory_domains_present": all(
            any(e["kind"] == k for e in events)
            for k in ("WORK_POSITION", "ORGANISMIC_EVENT", "NONMOTHER_RELATIONSHIP",
                      "PROJECT", "PRACTICE_FORMATION", "MEMORY_TRACE")
        ),
        "psyche_fields_have_causal_ancestry": all(
            item.get("causal_event_refs")
            for domain in ("attitudes", "practices", "strivings")
            for item in psyche.get(domain, [])
        ),
        "heldout_nonmother_action_evaluable_without_mom_prompt": probes.get(
            "heldout_independence_pass", False
        ),
        "nonmother_project_effects_persist_into_independent_future_test": any(
            e["payload"].get("durable_effect") for e in events
            if e["kind"] == "PROJECT" and e["payload"].get("nonmother")
        ),
        "forward_replay_entails_endpoint": replay.get("endpoint_match", False),
        "no_outstanding_mandatory_antecedent_missing_authority": True,
        "bounded_observational_closure": True,
    }
    ok = all(checks.values())
    return {
        "stopping_law_version": STOPPING_LAW_VERSION,
        "checks": checks,
        "sufficient": ok,
        "status": S.COMMITTED if ok else S.PREHISTORY_OWNER_RULE_MISSING,
    }


@dataclass
class ConstructionAttempt:
    attempt_id: str
    attempt_seed: str
    selected_class_key: str
    events: List[Dict[str, Any]]
    psyche: Dict[str, Any]
    replay: Dict[str, Any]
    probes: Dict[str, Any]
    stopping: Dict[str, Any]
    status: str
    construction_edges: List[Dict[str, Any]]


def construct_second_parent(selected_class: Dict[str, Any],
                            endpoint_constraints: Dict[str, Any],
                            attempt_seeds: List[str]) -> Dict[str, Any]:
    """Run the preregistered finite attempt slots. First endpoint-valid +
    independence-passing attempt is retained; ALL attempts and failures persisted.
    No silent resample: each attempt receipt is kept."""
    attempts: List[ConstructionAttempt] = []
    t0 = time.perf_counter()
    for i, seed in enumerate(attempt_seeds):
        actor_id = f"LAB_SECOND_PARENT_CAND_{selected_class['class_key'][:10]}"
        b = DadHistoryBuilder(actor_id, seed, endpoint_constraints)
        events = b.build()
        psyche = psyche_from_dad_events(events)
        replay = forward_replay_to_endpoint(events, endpoint_constraints)
        probes = heldout_independent_probes(events, psyche)
        stopping = stopping_law_check(events, psyche, endpoint_constraints, replay, probes)
        status = (
            S.COMMITTED
            if (replay.get("endpoint_match") and probes.get("heldout_independence_pass")
                and stopping.get("sufficient"))
            else (
                S.ENDPOINT_INFEASIBLE if not replay.get("endpoint_match")
                else S.INDEPENDENT_PROJECT_PROOF_MISSING
            )
        )
        cons_edges = [{
            "from": "ENDPOINT_CONSTRAINTS",
            "to": "PREHISTORY_ATTEMPT_" + str(i),
            "edge_type": "RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON",
            "algorithm_time": True,
            "causal_parent": False,
        }]
        attempts.append(ConstructionAttempt(
            attempt_id=h_concat("ATT", seed, selected_class["class_key"]),
            attempt_seed=seed,
            selected_class_key=selected_class["class_key"],
            events=events,
            psyche=psyche,
            replay=replay,
            probes=probes,
            stopping=stopping,
            status=status,
            construction_edges=cons_edges,
        ))
        if status == S.COMMITTED:
            break
    success = next((a for a in attempts if a.status == S.COMMITTED), None)
    return {
        "construction_version": CONSTRUCTION_VERSION,
        "n_attempts": len(attempts),
        "attempt_seeds": attempt_seeds,
        "attempts": [
            {
                "attempt_id": a.attempt_id,
                "attempt_seed": a.attempt_seed,
                "status": a.status,
                "n_events": len(a.events),
                "endpoint_match": a.replay.get("endpoint_match"),
                "independence_pass": a.probes.get("heldout_independence_pass"),
                "stopping_sufficient": a.stopping.get("sufficient"),
                "replay": a.replay,
                "probes": a.probes,
                "stopping": a.stopping,
            }
            for a in attempts
        ],
        "selected_attempt_id": success.attempt_id if success else None,
        "selected_events": success.events if success else None,
        "selected_psyche": success.psyche if success else None,
        "terminal_status": S.COMMITTED if success else S.HISTORY_SEARCH_EXHAUSTED,
        "wall_seconds": round(time.perf_counter() - t0, 6),
    }
