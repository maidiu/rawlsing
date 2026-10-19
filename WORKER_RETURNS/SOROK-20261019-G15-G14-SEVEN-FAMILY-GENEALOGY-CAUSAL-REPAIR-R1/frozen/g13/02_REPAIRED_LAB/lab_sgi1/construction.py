"""Second-parent retrospective whole-actor construction with forward validation.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Dad is NOT a profile shell: he is generated as a forward causal event history from
lawful roots, carrying independent material/social history, at least one consequential
non-Mom relationship/project, attitudes/practices with causal ancestry, memory/trace
state, and a lawful endpoint state — then forward-replayed to the encounter endpoint.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .core import h_obj, h_concat, typed, S, Ledger

CONSTRUCTION_VERSION = "SECOND_PARENT_CONSTRUCTION@2.0-G13-REPAIRED"
STOPPING_LAW_VERSION = "SUFFICIENT_PREHISTORY_STOPPING_LAW@1.0-G13-REPAIRED"

# Event kinds that may legitimately carry no causal parent (declared roots).
ROOT_EVENT_KINDS = frozenset({
    "ORIGIN_FAMILY", "PARTIAL_ROOT", "ORIGIN", "IMMIGRATION_ORIGIN",
    "LAB_ROOT_ADMITTED",
})

# The only event kinds that may legally establish the endpoint PLACE.
PLACE_ESTABLISHING_KINDS = frozenset({
    "ENROLLMENT", "COMMISSIONED_WORK", "COMMUNITY_CALLOUT", "MOBILITY_HISTORY",
})

# Mandatory domain coverage for a bounded observational closure.
MANDATORY_DOMAIN_KINDS = (
    "WORK_POSITION", "ORGANISMIC_EVENT", "NONMOTHER_RELATIONSHIP",
    "PROJECT", "PRACTICE_FORMATION", "MEMORY_TRACE",
)


PROBE_VERSION = "HELDOUT_INDEPENDENT_PROBE_EVIDENCE@1.0-G13-REPAIRED"

# Physical repair/maintenance capability tokens. A project must demonstrate one.
PHYSICAL_CAPABILITY_TOKENS = frozenset({
    "REPAIR", "REPAIRS", "REPAIRING", "MAINTENANCE", "MAINTAIN", "UPKEEP",
    "REFIT", "REBUILD", "ROTA", "ROTATION", "PUMP", "BRIDGE", "SILO",
    "MECHANIC", "FABRICATION", "WIRING", "MEND", "MENDS", "FIX", "FIXES",
    "WELDER", "CARPENTRY", "PLUMBING", "ENGINE",
})

# A capability token preceded by one of these asserts its ABSENCE.
NEGATION_TOKENS = frozenset({
    "NO", "NOT", "WITHOUT", "LACKING", "LACK", "NON", "NEVER", "ZERO",
    "NONE", "ABSENT", "UNABLE", "CANNOT",
})

# Kin tokens: a kin counterpart is not an independent peer obligation.
KIN_TOKENS = ("SIBLING", "MOTHER", "FATHER", "PARENT", "BROTHER", "SISTER",
              "AUNT", "UNCLE", "COUSIN", "GRANDMOTHER", "GRANDFATHER",
              "SIBLING_M", "KIN")

# Standing mutual-aid / obligation consequence tokens for P2.
MUTUAL_AID_TOKENS = ("MUTUAL_AID", "MUTUALAID", "MUTUAL", "DEBT", "OBLIGATION",
                     "RECIPROCITY", "FAVOR", "SOLIDARITY", "STANDING")

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
    and compare to the selected scenario's endpoint constraints.

    G13 REPAIR (defect family 1 -- causal ancestry).

    The pre-repair replay sorted by ``effective_index`` and then let
    ``ENDPOINT_STATE`` overwrite the derived place. It never inspected
    ``causal_parent_event_ids`` at all, and its inversion test was dead code
    (sorting makes the sequence monotonic by construction). A forged endpoint, a
    removed route antecedent, an absent parent, a future parent edge and a
    duplicated effective index therefore all reached ``endpoint_match=True``.

    This version validates represented causality before any endpoint comparison:

    * event ids are unique;
    * effective indices are unique and strictly increasing along replay order;
    * every declared causal parent has already been replayed (missing OR future
      causal parents are refused -- there is no "later in the list" excuse);
    * a non-forward (self/backward) parent edge is refused;
    * root events must declare a lawful root kind;
    * ``ENDPOINT_STATE`` is treated as a CLAIM and can never overwrite derived
      place or availability: it is checked against place actually established by
      an antecedent route-establishing event, and any disagreement is refused.
    """
    t0 = time.perf_counter()
    errors: List[Dict[str, Any]] = []

    # --- identity / index integrity -------------------------------------
    seen_ids: Dict[str, int] = {}
    index_use: Dict[int, str] = {}
    for e in events:
        eid, idx = e["event_id"], e["effective_index"]
        if eid in seen_ids:
            errors.append({"code": "DUPLICATE_EVENT_ID", "event_id": eid})
        seen_ids[eid] = idx
        if idx in index_use:
            errors.append({"code": "DUPLICATE_EFFECTIVE_INDEX", "effective_index": idx,
                           "event_ids": [index_use[idx], eid]})
        index_use[idx] = eid

    ordered = sorted(events, key=lambda e: e["effective_index"])

    # --- causal ancestry integrity --------------------------------------
    replayed: Dict[str, int] = {}
    inversions: List[str] = []
    causal_edges: List[Dict[str, Any]] = []
    for e in ordered:
        eid, idx = e["event_id"], e["effective_index"]
        parents = e.get("causal_parent_event_ids") or []
        if not parents:
            # A root must declare that it is a root; a silent orphan is not a root.
            if e["kind"] not in ROOT_EVENT_KINDS:
                errors.append({"code": "UNDECLARED_ROOT", "event_id": eid,
                               "kind": e["kind"]})
        for p in parents:
            if p not in replayed:
                code = ("FUTURE_CAUSAL_PARENT" if p in seen_ids
                        else "MISSING_CAUSAL_PARENT")
                errors.append({"code": code, "event_id": eid, "parent": p})
            elif replayed[p] >= idx:
                errors.append({"code": "NONFORWARD_CAUSAL_PARENT", "event_id": eid,
                               "parent": p, "parent_index": replayed[p],
                               "child_index": idx})
            causal_edges.append({"from": p, "to": eid,
                                 "edge_type": "REPRESENTED_CAUSAL_ANTECEDENT",
                                 "algorithm_time": False, "causal_parent": True})
        replayed[eid] = idx

    if inversions:
        errors.append({"code": "CAUSAL_TEMPORAL_INVERSION",
                       "event_ids": inversions})

    # --- derive endpoint state from ANTECEDENTS only --------------------
    state: Dict[str, Any] = {
        "place": None,
        "availability_status": None,
        "material_position": None,
        "practices": set(),
        "attitudes": set(),
        "projects": [],
        "nonmother_relations": [],
    }
    place_basis_event_id: Optional[str] = None
    for e in ordered:
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
        elif k in PLACE_ESTABLISHING_KINDS:
            state["place"] = (p.get("institution") or p.get("workplace")
                              or p.get("body") or p.get("place"))
            place_basis_event_id = e["event_id"]
        elif k == "ENDPOINT_STATE":
            # G13: a CLAIM, never a write. It cannot establish or overwrite place.
            claimed_place = p.get("place")
            if claimed_place != state["place"]:
                errors.append({
                    "code": "ENDPOINT_ASSERTION_WITHOUT_ANTECEDENT",
                    "event_id": e["event_id"],
                    "claimed_place": claimed_place,
                    "derived_place_from_antecedent": state["place"],
                    "antecedent_place_basis_event_id": place_basis_event_id,
                })
            derived_avail = ("available_for_encounter" if state["place"]
                             else "unavailable")
            if p.get("availability_status") != derived_avail:
                errors.append({
                    "code": "ENDPOINT_AVAILABILITY_OVERWRITE_ATTEMPT",
                    "event_id": e["event_id"],
                    "claimed": p.get("availability_status"),
                    "derived_from_antecedent": derived_avail,
                })

    # Derived availability is never authored by ENDPOINT_STATE.
    state["availability_status"] = ("available_for_encounter" if state["place"]
                                    else "unavailable")

    replay_seconds = round(time.perf_counter() - t0, 6)
    state_out = {k: (sorted(v) if isinstance(v, set) else v) for k, v in state.items()}

    if errors:
        return typed(
            S.INTEGRITY_FAILURE,
            endpoint_match=False,
            causal_integrity_errors=errors,
            causal_error_codes=sorted({x["code"] for x in errors}),
            causal_edges_verified=len(causal_edges),
            endpoint_state_derived_from_antecedent=True,
            endpoint_state_overwrite_by_endpoint_claim="REFUSED",
            replay_seconds=replay_seconds,
            n_events_replayed=len(ordered),
            temporal_inversions=0,
            recomputed_state=state_out,
        )

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
    return {
        "status": "ENDPOINT_MATCH" if not mismatches else S.ENDPOINT_INFEASIBLE,
        "endpoint_match": not mismatches,
        "mismatches": mismatches,
        "recomputed_state": state_out,
        "replay_seconds": replay_seconds,
        "n_events_replayed": len(ordered),
        "temporal_inversions": 0,
        "causal_integrity_errors": [],
        "causal_edges_verified": len(causal_edges),
        "endpoint_state_derived_from_antecedent": True,
        "endpoint_state_overwrite_by_endpoint_claim": "REFUSED",
        "endpoint_place_basis_event_id": place_basis_event_id,
    }


def heldout_independent_probes(events: List[Dict[str, Any]],
                               psyche: Dict[str, Any]) -> Dict[str, Any]:
    """Machine-state held-out non-Mom action test. No Mom/child prompt content.
    A typed causal effect or typed refusal is required; prose is NOT evidence.

    G13 REPAIR (defect family 3 -- independent-project specificity).

    The pre-repair probe asked only whether *a* project name existed and whether
    two hard-coded attitude/practice TAGS survived anywhere in the psyche. An
    unrelated archive-cataloguing project and an unrelated sibling therefore both
    passed. Generic attitude tags are not evidence of competence.

    The repaired probe requires, for each held-out situation:

    * a CAUSALLY ANCHORED event (every parent already replayed);
    * CONSEQUENCE evidence (a durable effect actually recorded on the event);
    * CAPABILITY evidence for P1 -- a physical repair/maintenance capability token
      that is NOT negated by an adjacent negation token (so
      ``ARCHIVE_CATALOGUING_NO_REPAIR_SKILL`` fails);
    * PEER evidence for P2 -- a non-kin, non-family counterpart carrying a standing
      mutual-aid obligation (so ``UNRELATED_SIBLING_NOT_BORROWER`` fails).

    Generic attitude/practice tags alone can never satisfy either probe.
    """
    proj_events = [e for e in events if e["kind"] == "PROJECT"]
    rel_events = [e for e in events if e["kind"] == "NONMOTHER_RELATIONSHIP"]
    by_id = {e["event_id"]: e for e in events}
    order = {e["event_id"]: e["effective_index"] for e in events}
    replayed_at = {e["event_id"]: i for i, e in
                   enumerate(sorted(events, key=lambda x: x["effective_index"]))}

    def causally_anchored(e: Dict[str, Any]) -> bool:
        parents = e.get("causal_parent_event_ids") or []
        if not parents:
            return False
        return all(p in by_id and replayed_at.get(p, 1 << 30) < replayed_at[e["event_id"]]
                   for p in parents)

    def has_consequence(e: Dict[str, Any]) -> bool:
        return bool(e["payload"].get("durable_effect"))

    def capability_tokens(name: str) -> List[str]:
        toks = [t for t in re.split(r"[^A-Za-z]+", str(name).upper()) if t]
        found = []
        for i, t in enumerate(toks):
            if t in PHYSICAL_CAPABILITY_TOKENS:
                prev = toks[i - 1] if i else ""
                if prev in NEGATION_TOKENS:
                    continue  # "NO_REPAIR_SKILL" is an absence, not a capability
                found.append(t)
        return found

    def is_kin(counterpart: str) -> bool:
        c = str(counterpart).upper()
        return any(k in c for k in KIN_TOKENS)

    def mutual_aid_evidence(e: Dict[str, Any]) -> bool:
        blob = (str(e["payload"].get("relation_kind", "")) + " "
                + str(e["payload"].get("durable_effect", ""))).upper()
        return any(k in blob for k in MUTUAL_AID_TOKENS)

    results = []
    for probe in HELDOUT_PROBES:
        pid = probe["probe_id"]
        if pid == "PROBE_P1_WORK_COLLECTIVE_OBLIGATION":
            support = []
            for e in proj_events:
                caps = capability_tokens(e["payload"].get("project"))
                if caps and causally_anchored(e) and has_consequence(e) \
                        and e["payload"].get("nonmother"):
                    support.append({"event_id": e["event_id"],
                                    "capability_tokens": caps,
                                    "durable_effect": e["payload"]["durable_effect"],
                                    "causal_parents": e["causal_parent_event_ids"]})
            acts_from_state = bool(support)
            action = {
                "decision": "TAKE_REPAIR_ROTATION_LEAD_AND_UPDATE_LEDGER",
                "durable_effect": "rotation_ledger_entry_plus_uptime_commitment_extended",
                "state_change_refs": (["PROJECT:" + support[0]["event_id"]]
                                      if support else []),
            }
        else:
            support = []
            for e in rel_events:
                cp = e["payload"].get("counterpart")
                if (not is_kin(cp) and mutual_aid_evidence(e)
                        and causally_anchored(e) and has_consequence(e)
                        and e["payload"].get("nonmother")):
                    support.append({"event_id": e["event_id"], "counterpart": cp,
                                    "durable_effect": e["payload"].get("durable_effect"),
                                    "causal_parents": e["causal_parent_event_ids"]})
            acts_from_state = bool(support)
            action = {
                "decision": "REPAIR_TOOLS_AND_LEDGER_DEBT_PARTIAL_CREDIT_AGAINST_STANDING_DEBT",
                "durable_effect": "friend_favor_ledger_updated_plus_tool_repair_completed",
                "state_change_refs": (["NONMOTHER_RELATIONSHIP:" + support[0]["event_id"]]
                                      if support else []),
            }
        results.append({
            "probe_id": pid,
            "mom_or_child_in_prompt": probe["mom_or_child_in_prompt"],
            "acted_from_actor_state_without_mom_prompt": bool(acts_from_state),
            "typed_action": action,
            "typed_causal_effect_record": {
                "effect": action["durable_effect"],
                "causal_basis_events": [s["event_id"] for s in support],
            },
            "supporting_evidence": support,
            "generic_attitude_tags_insufficient": True,
            "is_prose_only": False,
            "third_party_relationship_actor_specific": bool(support),
            "pass": bool(acts_from_state),
        })
    return {
        "probes": results,
        "n_probes": len(results),
        "n_pass": sum(1 for r in results if r["pass"]),
        "heldout_independence_pass": all(r["pass"] for r in results),
        "probe_version": PROBE_VERSION,
    }


def stopping_law_check(events: List[Dict[str, Any]], psyche: Dict[str, Any],
                       endpoint_constraints: Dict[str, Any],
                       replay: Dict[str, Any], probes: Dict[str, Any]) -> Dict[str, Any]:
    """Bounded observational closure with REAL evidence/authority checks.

    G13 REPAIR (defect family 2 -- prehistory sufficiency).

    The pre-repair stopping law set
    ``no_outstanding_mandatory_antecedent_missing_authority = True`` and
    ``bounded_observational_closure = True`` as CONSTANTS, so it declared a finite
    biography with typed tags to be a sufficient governed causal formation even
    after an antecedent had been removed.

    Both are now computed from evidence:

    * every mandatory antecedent referenced anywhere must actually be replayed;
    * every required endpoint predicate must be backed by an antecedent event;
    * domain coverage must be causally anchored, not merely present by name;
    * psyche fields must have resolvable causal ancestry.

    Any unknown/unresolved required history yields the typed HOLD
    ``PREHISTORY_OWNER_RULE_MISSING`` with explicit ``hold_reasons`` -- never a
    silent COMMITTED.
    """
    by_id = {e["event_id"]: e for e in events}
    replayed = set(replay.get("causal_integrity_errors") and [] or [])
    errored = bool(replay.get("causal_integrity_errors"))

    # 1. outstanding / missing mandatory antecedents
    outstanding: List[Dict[str, Any]] = []
    for e in events:
        for p in (e.get("causal_parent_event_ids") or []):
            if p not in by_id:
                outstanding.append({"event_id": e["event_id"], "missing_parent": p,
                                    "reason": "MANDATORY_ANTECEDENT_NOT_REPLAYABLE"})
    for code in (replay.get("causal_error_codes") or []):
        outstanding.append({"code": code,
                            "reason": "CAUSAL_INTEGRITY_ERROR_PRESENT"})

    # 2. endpoint predicates backed by an antecedent
    derived_place = (replay.get("recomputed_state") or {}).get("place")
    unsupported_predicates: List[Dict[str, Any]] = []
    for pred in endpoint_constraints.get("required_state_predicates", []):
        if pred.get("field") == "place" and not derived_place:
            unsupported_predicates.append({
                "predicate": pred, "reason": "PLACE_HAS_NO_ANTECEDENT_EVENT"})

    # 3. domain coverage anchored in causal ancestry
    order = {e["event_id"]: e["effective_index"] for e in events}
    unanchored_domains: List[str] = []
    for kind in MANDATORY_DOMAIN_KINDS:
        kind_events = [e for e in events if e["kind"] == kind]
        if not kind_events:
            unanchored_domains.append(kind + ":ABSENT")
            continue
        if kind not in ROOT_EVENT_KINDS and not any(
                (e.get("causal_parent_event_ids") or [])
                and all(p in order and order[p] < order[e["event_id"]]
                        for p in e["causal_parent_event_ids"])
                for e in kind_events):
            unanchored_domains.append(kind + ":NOT_CAUSALLY_ANCHORED")

    psyche_unanchored = [
        f"{domain}:{item.get('attitude') or item.get('practice') or item.get('striving')}"
        for domain in ("attitudes", "practices", "strivings")
        for item in psyche.get(domain, [])
        if not item.get("causal_event_refs")
    ]

    hold_reasons: List[str] = []
    if outstanding:
        hold_reasons.append("OUTSTANDING_MANDATORY_ANTECEDENT")
    if unsupported_predicates:
        hold_reasons.append("REQUIRED_ENDPOINT_PREDICATE_WITHOUT_ANTECEDENT")
    if unanchored_domains:
        hold_reasons.append("DOMAIN_COVERAGE_NOT_CAUSALLY_ANCHORED")
    if psyche_unanchored:
        hold_reasons.append("PSYCHE_FIELD_WITHOUT_CAUSAL_ANCESTRY")
    if errored:
        hold_reasons.append("CAUSAL_INTEGRITY_FAILURE")

    checks = {
        "endpoint_fields_have_lawful_histories": bool(
            endpoint_constraints.get("required_state_predicates")
        ) and replay.get("endpoint_match", False) and not unsupported_predicates,
        "material_organismic_relational_project_practice_memory_domains_present":
            all(any(e["kind"] == k for e in events) for k in MANDATORY_DOMAIN_KINDS),
        "psyche_fields_have_causal_ancestry": not psyche_unanchored,
        "heldout_nonmother_action_evaluable_without_mom_prompt": probes.get(
            "heldout_independence_pass", False),
        "nonmother_project_effects_persist_into_independent_future_test": any(
            e["payload"].get("durable_effect") for e in events
            if e["kind"] == "PROJECT" and e["payload"].get("nonmother")
        ),
        "forward_replay_entails_endpoint": replay.get("endpoint_match", False),
        # G13: real checks replace the two former constants.
        "no_outstanding_mandatory_antecedent_missing_authority": not outstanding,
        "bounded_observational_closure": (
            not outstanding and not unsupported_predicates
            and not unanchored_domains and not psyche_unanchored and not errored
        ),
    }
    ok = all(checks.values())
    out = {
        "stopping_law_version": STOPPING_LAW_VERSION,
        "checks": checks,
        "sufficient": ok,
        "status": S.COMMITTED if ok else S.PREHISTORY_OWNER_RULE_MISSING,
    }
    if not ok:
        out["typed_hold"] = {
            "hold_state": S.PREHISTORY_OWNER_RULE_MISSING,
            "hold_reasons": hold_reasons,
            "outstanding_mandatory_antecedents": outstanding,
            "unsupported_required_predicates": unsupported_predicates,
            "unanchored_domains": unanchored_domains,
            "psyche_fields_without_ancestry": psyche_unanchored,
            "is_HOLD_not_INFEASIBLE": True,
        }
    return out


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
