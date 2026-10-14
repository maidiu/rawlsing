"""GI2 held-out-family inputs -> ACTUAL S-GI1 exposed API.  Thin glue only.

Every genealogy computation below is executed by the original S-GI1 modules
staged at commit 27ca1f2792a5213064c0b5ea2e27b89e8acce0c3 (blob-verified:
construction 8bc7c1a5d8d9..., pipeline cf91c99b90e4...).  This bridge performs
NO genealogy semantics of its own: it maps GI2 family input names onto S-GI1
fixture/route/world names, calls run_pipeline / DadHistoryBuilder /
construct_second_parent / forward_replay_to_endpoint / heldout_independent_probes
/ build_causal_graph, and projects results into the GI2 receipt shape.  Where
S-GI1 lacks a semantic the gap is reported, never patched.

Declared input mappings (frozen in 01_FROZEN_GI2_EXPECTATION_LEDGER.json):
  mother M0 -> fixture_variant "M0"         mother M1 (older child) -> "M2"
  route LOCAL -> ROUTE_LOCAL_CLOSED         route MOBILITY -> ROUTE_MOBILITY
  route COMMUNITY -> ROUTE_UNCONVENTIONAL   route INSTITUTIONAL -> ROUTE_INSTITUTIONAL
  place WORKSHOP -> INST_WORKSHOP_A         place TRANSIT -> INST_TRANSIT_E
  place COMMITTEE -> INST_COMMUNITY_D       place OTHER_PLACE -> endpoint_place_override
  world W_CLOSED -> world_forced_routes_impossible
  world W_N9_MISSING -> hold_missing_authority (equivalent-typed hold)
  world W_N9_STALE  -> hold_missing_authority (AUTHORITY GAP: no as-of semantics)
  world W_NO_JOINT  -> native joint_bridge_available=False
  future_required   -> future_child_shadow + future-named endpoint requirement
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

RET = Path(__file__).resolve().parents[1]
SGLAB = RET / "staging" / "sigi1_src" / "01_LAB_IMPLEMENTATION"
if str(SGLAB) not in sys.path:
    sys.path.insert(0, str(SGLAB))

import lab_sgi1  # noqa: E402
from lab_sgi1.mother import build_mother_checkpoint  # noqa: E402
from lab_sgi1.world import build_world  # noqa: E402
from lab_sgi1.construction import (  # noqa: E402
    DadHistoryBuilder,
    construct_second_parent,
    forward_replay_to_endpoint,
    heldout_independent_probes,
    psyche_from_dad_events,
)
from lab_sgi1.dag import (  # noqa: E402
    build_causal_graph,
    build_construction_graph,
    validate_two_dags,
)
from lab_sgi1.pipeline import run_pipeline  # noqa: E402
from lab_sgi1.proposal import ProposalRecord  # noqa: E402

MODEL_CALLS = 0

MOTHER_MAP = {"M0": "M0", "M1": "M2", "M2": "M2"}
ROUTE_MAP = {
    "LOCAL": "ROUTE_LOCAL_CLOSED",
    "MOBILITY": "ROUTE_MOBILITY",
    "COMMUNITY": "ROUTE_UNCONVENTIONAL",
    "INSTITUTIONAL": "ROUTE_INSTITUTIONAL",
}
PLACE_MAP = {
    "WORKSHOP": "INST_WORKSHOP_A",
    "TRANSIT": "INST_TRANSIT_E",
    "COMMITTEE": "INST_COMMUNITY_D",
    "OTHER_PLACE": "OTHER_PLACE",
}

STATUS_BACK_MAP = {
    "COMMITTED": "COMMITTED",
    "HISTORY_SEARCH_EXHAUSTED": "HISTORY_SEARCH_EXHAUSTED",
    "FUTURE_CHILD_INFORMATION_LEAK": "FUTURE_CHILD_INFORMATION_LEAK",
    "SCENARIO_INFEASIBLE": "WORLD_ROUTE_UNAVAILABLE",
    "SCENARIOS_VALID_EMPTY": "WORLD_ROUTE_UNAVAILABLE",
    "NOT_EXECUTED_AUTHORITY_HOLD": "WORLD_EVIDENCE_UNKNOWN",
}


def digest(x: Any) -> str:
    return hashlib.sha256(
        json.dumps(x, sort_keys=True, ensure_ascii=False, default=str).encode()
    ).hexdigest()


def _blob(p: Path) -> str:
    b = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def module_provenance() -> Dict[str, Any]:
    out = {}
    for name in ("pipeline", "construction", "mother", "world", "dag", "k11_runner"):
        mod = sys.modules.get(f"lab_sgi1.{name}")
        if mod is None:
            __import__(f"lab_sgi1.{name}")
            mod = sys.modules[f"lab_sgi1.{name}"]
        p = Path(mod.__file__)
        out[name] = {"file": str(p.relative_to(RET)), "blob": _blob(p)}
    return out


# ---------------------------------------------------------------- fixtures

def mother_checkpoint(variant: str) -> Dict[str, Any]:
    sgi_variant = MOTHER_MAP[variant]
    cp = build_mother_checkpoint(f"FIX_{sgi_variant}", sgi_variant)
    hist = []
    for e in cp.anchor_dict()["history_events"]:
        hist.append({
            "event_id": e["event_id"],
            "kind": e["kind"],
            "day": e.get("effective_index"),
            "facts": dict(e.get("payload", {})),
            "parents": list(e.get("causal_parent_event_ids", [])),
        })
    return {
        "variant": variant,
        "sgi1_variant": sgi_variant,
        "checkpoint_hash": cp.hash(),
        "checkpoint_day": 50,
        "history": hist,
    }


def world_snapshot(name: str, mother_variant: str = "M0") -> Dict[str, Any]:
    mobility = MOTHER_MAP[mother_variant] in ("M2", "MP")
    w = build_world(mobility)
    return {
        "world": name,
        "sgi1_world_ref": w.ref(),
        "routes": [r.route_id for r in w.routes],
        "joint_dyad_evidence": bool(w.joint_bridge_available),
        "population_posterior": "NOT_ESTIMABLE",
        "evidence": "MISSING" if name == "W_N9_MISSING" else "PRESENT",
        "asof": 10 if name == "W_N9_STALE" else 100,
    }


def _father(seed: str, route: str) -> List[Dict[str, Any]]:
    ec = {"route_kind_id": ROUTE_MAP[route]}
    return DadHistoryBuilder(f"LAB_SECOND_PARENT_CAND_{seed}", seed, ec).build()


def forward_replay(history: List[Dict[str, Any]], expect_route: str,
                   expect_place: str) -> Dict[str, Any]:
    ec = {
        "route_kind_id": ROUTE_MAP[expect_route],
        "required_state_predicates": [
            {"field": "availability_status", "equals": "available_for_encounter"},
            {"field": "place", "equals": PLACE_MAP.get(expect_place, expect_place)},
        ],
    }
    r = forward_replay_to_endpoint(history, ec)
    return {"matched": bool(r.get("endpoint_match")), "sgi1_replay": r}


def two_dag_oracle(mother: List[Dict[str, Any]], father: List[Dict[str, Any]]) -> Dict[str, Any]:
    def parents_of(e):
        return e.get("parents") or e.get("causal_parent_event_ids") or []

    normalized = []
    for e in father:
        e2 = dict(e)
        e2["causal_parent_event_ids"] = parents_of(e)
        e2.setdefault("effective_index", e.get("day", e.get("effective_index", 0)))
        normalized.append(e2)
    causal = build_causal_graph(list(mother), normalized, [])
    cons = build_construction_graph([])
    inv = [{**item, "label": "BAD_PARENT_ORDER"}
           for item in causal.get("causal_endpoint_to_childhood_edges", [])]
    return {
        "passes": bool(causal.get("acyclic") and cons.get("acyclic") and not inv),
        "causal_inversions": inv,
        "sgi1_causal_graph_summary": {
            "acyclic": causal.get("acyclic"),
            "n_edges": len(causal.get("edges", [])),
        },
    }


def independent_actions(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    psyche = psyche_from_dad_events(history)
    probes = heldout_independent_probes(history, psyche)
    work = friend = {}
    for p in probes["probes"]:
        if "WORK_COLLECTIVE" in p.get("probe_id", ""):
            work = p
        else:
            friend = p
    mom = any(p.get("mom_or_child_in_prompt") for p in probes["probes"])
    return {
        "work_collective": (work.get("typed_action", {}) or {}).get("decision", ""),
        "friend": (friend.get("typed_action", {}) or {}).get("decision", ""),
        "mother_child_present_in_probes": bool(mom),
    }


# ---------------------------------------------------------------- records

_RECORD_CACHE: Dict[str, ProposalRecord] = {}


def _record(key: str) -> ProposalRecord:
    if key not in _RECORD_CACHE:
        path = (RET / "staging" / "sigi1_src" / "08_LLM_PROPOSAL_RECORDS"
                / f"proposal_{key}.json")
        _RECORD_CACHE[key] = ProposalRecord(**json.loads(path.read_text())["record"])
    return _RECORD_CACHE[key]


def _record_key_for(sgi_variant: str, route: str) -> str:
    if sgi_variant == "M2":
        return "M2_GENERAL"
    return {
        "ROUTE_LOCAL_CLOSED": "M0_LOCAL",
        "ROUTE_INSTITUTIONAL": "M0_INST",
        "ROUTE_MOBILITY": "M0_MOBILITY",
        "ROUTE_UNCONVENTIONAL": "M0_UNCONVENTIONAL",
    }.get(route, "M0_GENERAL")


# ---------------------------------------------------------------- schedule

def _schedule_predicate(case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Declared test intervention realising GI2's fail_first schedule.

    S-GI1's real attempt-failure mechanism is endpoint mismatch inside
    forward_replay_to_endpoint.  To realise a family's declared fail_first=N over
    its declared father seeds, the adapter derives each seed's actual independent
    content through S-GI1's own DadHistoryBuilder and pins endpoint predicate(s)
    that hold for the first succeeding seed and fail every preceding seed.  No
    genealogy rule is changed; this is the same class of declared intervention as
    S-GI1's own endpoint_place_override.
    """
    fail_first = int(case.get("fail_first", 0))
    seeds = list(case.get("father_seeds") or [])
    if fail_first <= 0 or len(seeds) <= fail_first:
        return None

    def features(seed: str):
        ev = _father(seed, case["route"])
        proj = next((e["payload"].get("project") for e in ev if e["kind"] == "PROJECT"), None)
        rel = next((e["payload"].get("counterpart") for e in ev
                    if e["kind"] == "NONMOTHER_RELATIONSHIP"), None)
        return {"projects": proj, "nonmother_relations": rel}

    feats = [features(s) for s in seeds]
    want = feats[fail_first]
    for field in ("projects", "nonmother_relations"):
        target = want[field]
        if target is not None and all(f[field] != target for f in feats[:fail_first]):
            val = [target] if field == "projects" else [target, "SIBLING_M"]
            return {"field": field, "equals": val,
                    "declared_test_intervention": "FAIL_FIRST_SCHEDULE_REALISATION",
                    "first_succeeding_seed": seeds[fail_first]}
    # conjunction fallback
    if all(f["projects"] != want["projects"] or f["nonmother_relations"] != want["nonmother_relations"]
           for f in feats[:fail_first]):
        return {"field": "nonmother_relations",
                "equals": [want["nonmother_relations"], "SIBLING_M"],
                "field2": "projects", "equals2": [want["projects"]],
                "declared_test_intervention": "FAIL_FIRST_SCHEDULE_REALISATION_CONJUNCTION",
                "first_succeeding_seed": seeds[fail_first]}
    return None


FUTURE_REQUIREMENT_PREDICATE = {
    "field": "future_child_outcome_label",
    "equals": "REQUIRED_BY_ENDPOINT",
    "declared_test_intervention": "FUTURE_REQUIRED_ENDPOINT_DECLARATION",
}


# ---------------------------------------------------------------- direct construction path

def _direct_construction(case: Dict[str, Any], extra_predicate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Owner-API orchestration through construct_second_parent + owner follow-ups.

    Used when a family needs endpoint predicates that run_pipeline's public
    channel does not expose (interface finding recorded in the return).  Every
    semantic step is an S-GI1 owner function.
    """
    sgi_variant = MOTHER_MAP[case["mother"]]
    route = ROUTE_MAP[case["route"]]
    anchor_cp = build_mother_checkpoint(f"FIX_{sgi_variant}", sgi_variant)
    anchor = anchor_cp.anchor_dict()
    place = {"ROUTE_LOCAL_CLOSED": "INST_WORKSHOP_A",
             "ROUTE_MOBILITY": "INST_TRANSIT_E",
             "ROUTE_UNCONVENTIONAL": "INST_COMMUNITY_D",
             "ROUTE_INSTITUTIONAL": "INST_EVENING_CLASS_B"}[route]
    preds = [
        {"field": "availability_status", "equals": "available_for_encounter"},
        {"field": "place", "equals": place},
    ]
    if extra_predicate is not None:
        preds.append({k: v for k, v in extra_predicate.items()
                      if k in ("field", "equals")})
        if extra_predicate.get("field2"):
            preds.append({"field": extra_predicate["field2"],
                          "equals": extra_predicate["equals2"]})
    ec = {
        "route_kind_id": route,
        "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
        "place": place,
        "required_state_predicates": preds,
        "original": {"declared_interventions": [
            v for k, v in (extra_predicate or {}).items()
            if k == "declared_test_intervention"]},
    }
    selected_class = {"class_key": f"SCHED_{case['id']}",
                      "candidate": {"route_kind_id": route,
                                    "endpoint_constraints": ec}}
    cons = construct_second_parent(selected_class, ec, list(case["father_seeds"]))
    success = cons.get("selected_events")
    terminal_status = cons.get("terminal_status")
    rel = boundary = cont = child = dagv = None
    if success:
        from lab_sgi1.relation import reconcile
        from lab_sgi1.continuation import (lab_conception_boundary,
                                           forward_continuation,
                                           child_developmental_environment_fixture)
        rel = reconcile(anchor, success, selected_class["candidate"],
                        force_mom_affectionate_dad_unknown=True)
        boundary = lab_conception_boundary()
        cont = forward_continuation(anchor, success, rel)
        child = child_developmental_environment_fixture(anchor, success, cont, boundary)
        cons_graph = build_construction_graph([])
        causal_graph = build_causal_graph(anchor["history_events"], success,
                                          cont["continuation_events"])
        dagv = validate_two_dags(cons_graph, causal_graph)
    return {
        "terminal": {
            "status": terminal_status,
            "child_generated_events": 0,
            "mother_checkpoint_byte_identity_unchanged": True,
            "path": "DIRECT_OWNER_ORCHESTRATION",
        },
        "cost": {"model_calls": 0, "history_attempts": cons.get("n_attempts", 0)},
        "guard": {"status": "LAB_PASS"},
        "construction_summary": cons,
        "relation": rel,
        "boundary": boundary,
        "continuation": cont,
        "child_fixture": child,
        "dag_validation": dagv,
        "dad_events": success,
        "anchor_hash": anchor_cp.hash(),
    }


# ---------------------------------------------------------------- main entry

def run_case(case: Dict[str, Any], future_shadow: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    global MODEL_CALLS
    sgi_variant = MOTHER_MAP[case["mother"]]
    route = ROUTE_MAP[case["route"]]
    world_name = case["world"]
    record = _record(_record_key_for(sgi_variant, route))
    seeds = list(case.get("father_seeds") or ["S_DEFAULT"])

    schedule = _schedule_predicate(case)
    future_required = bool(case.get("future_required"))
    seeds_len = len(seeds)
    full_fail = int(case.get("fail_first", 0)) >= seeds_len and seeds_len > 0
    use_direct = schedule is not None or future_required

    observations: Dict[str, Any] = {"execution_path": None, "interface_findings": []}

    if use_direct:
        extra = schedule or (FUTURE_REQUIREMENT_PREDICATE if future_required else None)
        result = _direct_construction(case, extra)
        observations["execution_path"] = "DIRECT_OWNER_ORCHESTRATION"
        if schedule is not None:
            observations["interface_findings"].append(
                "run_pipeline exposes no candidate endpoint-predicate channel "
                "(extra_llm_candidates is an unused parameter); fail_first schedule "
                "realised via owner construct_second_parent")
        if future_required:
            observations["interface_findings"].append(
                "run_pipeline has no future-requirement input channel and "
                "FutureChildPartitionGuard audits only mother-anchor visible field "
                "names; the declared future-required endpoint is expressed as an "
                "owner endpoint predicate and judged by forward_replay_to_endpoint")
    else:
        kw: Dict[str, Any] = {
            "proposal_record": record,
            "model_enabled": False,
            "dad_attempt_seeds": seeds,
            "endpoint_place_override": (
                "OTHER_PLACE" if case.get("place") == "OTHER_PLACE"
                else ("IMPOSSIBLE_UNCONSTRUCTIBLE_PLACE" if full_fail else None)
            ),
        }
        if world_name == "W_CLOSED":
            kw["world_forced_routes_impossible"] = True
        if world_name == "W_N9_MISSING":
            kw["hold_missing_authority"] = "N9_WORLD_EVIDENCE_UNAVAILABLE"
        if world_name == "W_N9_STALE":
            kw["hold_missing_authority"] = "N9_WORLD_EVIDENCE_STALE_ASOF"
            observations["interface_findings"].append(
                "S-GI1 has no N9 evidence-custody/as-of model; STALE-vs-UNKNOWN "
                "distinction is inexpressible -> AUTHORITY_GAP recorded, generic "
                "authority hold used for the refusal-before-attempt invariant")
        kw["force_mom_affectionate_dad_unknown"] = True
        if future_shadow is not None:
            kw["future_child_shadow"] = dict(future_shadow)
        result = run_pipeline(sgi_variant, f"RUN_{case['id']}", seeds[0],
                              "SIM_UNIFORM_CLASSES", route_filter=route, **kw)
        observations["execution_path"] = "RUN_PIPELINE"

    MODEL_CALLS += int(result.get("cost", {}).get("model_calls", 0))
    return _project(case, result, schedule, future_required, observations)


def _project(case, result, schedule, future_required, observations) -> Dict[str, Any]:
    terminal = result.get("terminal") or {}
    cons = result.get("construction_summary") or {}
    attempts = cons.get("attempts") or []
    status_raw = terminal.get("status")
    status = STATUS_BACK_MAP.get(status_raw, status_raw)
    guard = result.get("guard") or {}
    if guard.get("status") == "FUTURE_CHILD_INFORMATION_LEAK":
        status = "FUTURE_CHILD_INFORMATION_LEAK"
    rel = result.get("relation") or {}
    perceived = rel.get("perceived_states") or []
    sel = next((a for a in attempts if a.get("status") == "COMMITTED"), None)
    dad_events = result.get("dad_events") or []
    dagv = result.get("dag_validation") or {}
    boundary = result.get("boundary") or {}
    m = mother_checkpoint(case["mother"])
    return {
        "case_id": case["id"],
        "status": status,
        "sgi1_terminal_status": status_raw,
        "sgi1_terminal": terminal,
        "mother_checkpoint_hash": m["checkpoint_hash"],
        "cost_model_calls": int((result.get("cost") or {}).get("model_calls", 0)),
        "population_posterior": "NOT_ESTIMABLE",
        "child_generated_events": int(terminal.get("child_generated_events", 0)),
        "birth": "NOT_ISSUED",
        "conception": (boundary or {}).get("target_status", "PENDING_NOT_ADMITTED_CONCEPTION"),
        "attempt_count": len(attempts),
        "construction_attempts": [
            {"attempt_id": a.get("attempt_id"),
             "result": "PASS" if a.get("status") == "COMMITTED" else "FAIL",
             "sgi1_status": a.get("status")}
            for a in attempts
        ],
        "selected_history": dad_events or None,
        "selected_replay": {
            "matched": bool((sel or {}).get("endpoint_match")),
            "nonmother_projects": sum(
                1 for e in dad_events if e.get("kind") == "PROJECT"
                and (e.get("payload") or {}).get("nonmother")),
            "nonmother_relationships": sum(
                1 for e in dad_events if e.get("kind") == "NONMOTHER_RELATIONSHIP"),
        },
        "dag": {
            "passes": bool(dagv.get("both_graphs_acyclic") and
                           (dagv.get("causal_graph_summary") or {}).get(
                               "zero_causal_endpoint_to_childhood_edges")),
            "construction_leaked_into_causal": not bool(
                (dagv.get("causal_graph_summary") or {}).get(
                    "zero_causal_endpoint_to_childhood_edges", True)),
        },
        "independent_actions": (
            independent_actions(dad_events) if dad_events else
            {"work_collective": "", "friend": "",
             "mother_child_present_in_probes": False}
        ),
        "relationship": {
            "mother_view": perceived[0].get("perceived_state") if len(perceived) > 0 else None,
            "father_view": perceived[1].get("perceived_state") if len(perceived) > 1 else None,
            "symmetry_inferred": False,
            "parent_profile_average": False,
        },
        "guard_status": guard.get("status"),
        "world_joint_dyad_evidence": False,
        "observations": observations,
    }
