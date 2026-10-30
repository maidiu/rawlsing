"""Full lab pipeline orchestration: mother checkpoint -> pending target -> proposals ->
qualification -> dedup -> selection -> second-parent construction -> forward replay ->
relation reconciliation -> continuation -> child developmental-environment fixture.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. In-memory source-free runner only.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from . import (LAB_RULE_STATUS, CONTRACT_VERSION, LAB_CONCEPTION_BOUNDARY,
               K11_CONTRACT)
from .core import h_obj, h_concat, typed, S, Ledger, CostCounters
from .mother import build_mother_checkpoint, validate_no_demographic_psyche, EMBARGOED_PARTITION_MANIFEST
from .world import build_world, WORLD_PREMISE_VERSION
from .proposal import (build_proposal_prompt, PROPOSAL_SYSTEM_PROMPT, call_model,
                       freeze_proposal_record, frozen_fallback_record,
                       PROPOSAL_GRAMMAR_VERSION)
from .qualification import qualify
from .selection import adp020_select, scope_hash, POLICIES, policy_hash
from .construction import construct_second_parent
from .relation import reconcile
from .continuation import (lab_conception_boundary, forward_continuation,
                           child_developmental_environment_fixture)
from .dag import build_construction_graph, build_causal_graph, validate_two_dags

PIPELINE_VERSION = "G15_CAUSAL_RESEARCH_PIPELINE@1.0.0"
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o"


def _nested_field_names(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _nested_field_names(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _nested_field_names(child)
    elif isinstance(value, str):
        yield value


class FutureChildPartitionGuard:
    """Tracks reads; any access to an embargoed partition name is a hard leak."""

    def __init__(self):
        self.reads: List[str] = []
        self.leaks: List[str] = []

    def enter(self, component: str, visible_field_names: Any):
        self.reads.append(component)
        for f in _nested_field_names(visible_field_names):
            for banned in EMBARGOED_PARTITION_MANIFEST:
                if banned in f or f in banned:
                    self.leaks.append({"component": component, "field": f})

    def assert_clean(self) -> Dict[str, Any]:
        return typed(
            S.FUTURE_CHILD_INFORMATION_LEAK if self.leaks else S.LAB_PASS,
            leaks=self.leaks,
            components_with_visible_inputs=self.reads,
        )


def run_pipeline(
    fixture_variant: str,
    causal_run_id: str,
    root_seed: str,
    policy_name: str,
    route_filter: Optional[str] = None,
    proposal_record: Optional[Any] = None,
    force_selection_index: Optional[int] = None,
    future_child_shadow: Optional[Dict[str, Any]] = None,
    dad_attempt_seeds: Optional[List[str]] = None,
    max_proposals: int = 6,
    model_enabled: bool = False,
    hold_missing_authority: Optional[str] = None,
    force_mom_affectionate_dad_unknown: bool = False,
    only_demographic_dad: bool = False,
    force_same_time_conflict: bool = False,
    alter_subject_hash: bool = False,
    world_forced_routes_impossible: bool = False,
    ordinal_only_no_policy: bool = False,
    mutate_existing_shared_event: bool = False,
    endpoint_place_override: Optional[str] = None,
    extra_llm_candidates: Optional[List[Dict[str, Any]]] = None,
    joint_material_opportunity: Optional[Dict[str, Any]] = None,
    continued_joint_material: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute the full lab pipeline. Every stage leaves receipts.

    future_child_shadow is ONLY consumed by the embargo-comparison harness OUTSIDE
    this function's visible-input set; it is never read by any preconception
    component. It is accepted here solely to prove it is not consulted: the guard
    records that no component listed it among visible fields.
    """
    t0 = time.perf_counter()
    costs = CostCounters()
    ledger = Ledger(f"pipeline_{fixture_variant}_{root_seed}")
    guard = FutureChildPartitionGuard()

    # The joint material/context packets are actual visible inputs. A future-child
    # partition name in either packet is a hard source leak, refused before any
    # proposal, selection, construction or committed causal output.
    for label, packet in (("joint_material_opportunity", joint_material_opportunity),
                          ("continued_joint_material", continued_joint_material)):
        if isinstance(packet, dict):
            guard.enter(label, packet)
    leaked = guard.assert_clean()
    if leaked["status"] == S.FUTURE_CHILD_INFORMATION_LEAK:
        terminal = typed(
            S.FUTURE_CHILD_INFORMATION_LEAK,
            reason="future-child partition present in joined material/context input",
            leaks=leaked["leaks"],
            refused_before_any_proposal_or_committed_output=True,
        )
        return {"terminal": terminal, "anchor": None, "target": None,
                "lab_rule": LAB_RULE_STATUS,
                "future_child_source_leak_refused": True}

    # ---- G0-style preflight (lab) ----
    lab_grants = {
        "SOURCE_FREE_SYNTHETIC_ACTOR_FIXTURES": True,
        "SYNTHETIC_WORLD_FIXTURES": True,
        "IMPLEMENT_PROPOSED_CONSTRUCTION_CONTRACT_ISOLATED": True,
        "MODEL_ASSISTED_CANDIDATE_PROPOSAL_LAB_ONLY": False,
        "DETERMINISTIC_RNG_SELECTION_EXPERIMENTS": True,
        "K11_EXECUTION": True,
        "GENERATED_MOTHER_SECOND_PARENT_CHILD_LAB_HISTORIES": False,
        "EXACT_REPLAY_COST_MEASUREMENT": True,
        "CANONICAL_SEMANTIC_ADOPTION": False,
        "PRODUCTION_V3_WAKE": False,
        "REAL_PREV3_INTEGRATION": False,
        "ORIGINAL_SURVEY_SOURCE_EXECUTION": False,
        "REAL_PERSON_INFERENCE": False,
        "PHYSICAL_WELD": False,
        "PRODUCT_RELEASE": False,
    }
    ledger.add("LAB_GRANTS", lab_grants)

    # ---- mother checkpoint ----
    anchor_cp = build_mother_checkpoint(f"FIX_{fixture_variant}", fixture_variant)
    anchor = anchor_cp.anchor_dict()
    anchor_hash = anchor_cp.hash()
    psyche_check = validate_no_demographic_psyche(anchor_cp)
    ledger.add("MOTHER_CHECKPOINT", {
        "fixture_id": anchor_cp.fixture_id,
        "anchor_hash": anchor_hash,
        "history_prefix_commit_hash": anchor_cp.history_prefix_commit_hash,
        "psyche_causal_ancestry_check": psyche_check,
    })

    # ---- pending target (NONCAUSAL) ----
    target = {
        "target_id": h_concat("TARGET", anchor_hash, root_seed),
        "mother_anchor_hash": anchor_hash,
        "focal_slot_ref": "FOCAL_CHILD_SLOT_0",
        "planned_boundary_time_or_interval": "T_PRECONCEPTION_LAB_BOUNDARY",
        "target_status": S.TARGET_PENDING,
        "known_counterpart_ref_or_null": anchor.get(
            "known_counterpart_identity_ref_or_null"
        ),
        "candidate_generation_policy_ref": "LAB_FINITE_SCENARIO_PROPOSAL",
        "cursor_increments": 0,
        "prohibited_future_input_hash": anchor_cp.prohibited_future_input_hash,
        "hidden_future_child_shadow_present": future_child_shadow is not None,
    }
    target_hash = h_obj({k: v for k, v in target.items()
                         if k != "hidden_future_child_shadow_present"})
    ledger.add("PENDING_TARGET", {
        "target_id": target["target_id"],
        "target_status": target["target_status"],
        "cursor_increments": 0,
        "target_hash": target_hash,
    })

    # ---- world ----
    mobility_reachable = bool(anchor_cp.mobility_history_present
                              or anchor_cp.prospective_opportunity_refs)
    world = build_world(mobility_reachable)
    if world_forced_routes_impossible:
        # Negative control: all routes become impossible under immutable world facts.
        import dataclasses as _dc
        impossible = [
            type(r)(r.route_id, r.route_kind, r.via_institution,
                    r.requires_mobility, False, False,
                    "FORCED_NEGATIVE_CONTROL_ALL_ROUTES_IMPOSSIBLE")
            for r in world.routes
        ]
        world = _dc.replace(world, routes=impossible)
    ledger.add("WORLD_SNAPSHOT", {"world_ref": world.ref(),
                                  "premise_version": WORLD_PREMISE_VERSION})

    # ---- scenario proposal (real model call or frozen record) ----
    guard.enter("proposal", list(anchor.keys()))
    call_rec: Dict[str, Any] = {"ok": False}
    if proposal_record is not None:
        import copy
        record = copy.deepcopy(proposal_record)
    elif model_enabled:
        prompt = build_proposal_prompt(
            anchor, {k: v for k, v in target.items()
                     if k not in ("hidden_future_child_shadow_present",)},
            {
                "world_id": world.world_id,
                "premise_version": world.premise_version,
                "routes": [{"route_id": r.route_id, "route_kind": r.route_kind,
                            "premise_note": r.premise_note} for r in world.routes],
                "institutions": [{"inst_id": i.inst_id, "kind": i.kind}
                                 for i in world.institutions],
            },
            route_filter, max_proposals,
        )
        try:
            call_rec = call_model(prompt, PROPOSAL_SYSTEM_PROMPT, MODEL_NAME,
                                  MODEL_PROVIDER)
            costs.model_calls += 1
            costs.prompt_tokens += call_rec.get("prompt_tokens", 0)
            costs.completion_tokens += call_rec.get("completion_tokens", 0)
            costs.total_tokens += call_rec.get("total_tokens", 0)
        except Exception as exc:  # transport failure -> frozen fallback, NOT faked
            call_rec = {"ok": False, "error": repr(exc)}
        record = freeze_proposal_record(
            anchor_cp.fixture_id, route_filter, prompt if model_enabled else "",
            PROPOSAL_SYSTEM_PROMPT, call_rec, max_proposals
        )
        if not call_rec.get("ok") and not record.parsed_candidates:
            record = frozen_fallback_record(anchor_cp.fixture_id, route_filter)
    else:
        record = frozen_fallback_record(anchor_cp.fixture_id, route_filter)
    ledger.add("PROPOSAL_RECORD", {
        "record_id": record.record_id,
        "proposal_hash": record.proposal_hash,
        "provider": record.provider,
        "model_returned": record.model_returned,
        "candidate_ids": record.candidate_ids,
        "n_classes": record.dedup["n_classes"],
        "class_set_hash": record.dedup["class_set_hash"],
        "automated_status": record.lmm_automated_status,
        "usage": record.usage,
        "wall_seconds": record.wall_seconds,
    })

    # ---- qualification over deduped classes ----
    from .proposal import dedup_candidates
    # Cache contents are not authority. Always screen and rederive from raw input.
    from .membrane import output_findings
    original_candidates=record.parsed_candidates
    record.dedup=dedup_candidates(original_candidates)
    classes = record.dedup["classes"]
    raw_hold=any(output_findings(c) for c in original_candidates) or record.dedup.get('status')=='DEDUP_UNDERDETERMINED'
    if raw_hold:
        terminal=typed(S.NOT_EXECUTED_AUTHORITY_HOLD,reason='OUTPUT_MEMBRANE_OR_CANDIDATE_ID_HOLD',n_draws=0)
        return _finish(ledger,costs,t0,terminal,anchor_hash,target_hash,guard,record,world,[],None,None,None,None,None,None,None,causal_run_id,root_seed,policy_name)
    quals = []
    for c in classes:
        cand = dict(c["candidate"])
        cand["class_key"] = c["class_key"]
        q = qualify(cand, anchor, world)
        quals.append(q)
        costs.generic_queries += 1
    eligible=[]
    for c,q in zip(classes,quals):
        if q['eligibility']['eligible']:
            import copy
            e=copy.deepcopy(c)
            e.update(candidate_authority_id='G15_CLOSED_RESEARCH_SCHEMA',candidate_authority_version='1.0.0',
                eligibility_or_admission_receipt_hash=h_obj(q),qualification_receipt=q,world_snapshot_hash=world.ref(),native_admission='NOT_GRANTED')
            eligible.append(e)
    ledger.add("QUALIFICATION", {
        "per_class": [
            {"class_key": q.get("class_key"),
             "candidate_local_id": q.get("candidate_local_id"),
             "route_id": (q["hard_feasibility"] or {}).get("route_id"),
             "route_truth_note": next(
                 (r.premise_note for r in world.routes
                  if r.route_id == (q["hard_feasibility"] or {}).get("route_id")), None),
             "eligibility": q["eligibility"],
             "hard": q["hard_feasibility"].get("status"),
             "empirical": q["empirical_or_synthetic_support"].get("result_state")}
            for q in quals
        ],
        "n_eligible": len(eligible),
    })

    if not eligible:
        contradiction = any(
            q["eligibility"].get("reason") == S.SHARED_HISTORY_CONTRADICTION_HOLD
            for q in quals
        )
        if contradiction and anchor.get("known_counterpart_identity_ref_or_null"):
            existing_shared = [
                e for e in anchor.get("history_events", [])
                if e.get("kind") == "SHARED_ENCOUNTER"
            ]
            terminal = typed(
                S.SHARED_HISTORY_CONTRADICTION_HOLD,
                reason="mother history identifies counterpart; all proposed candidates "
                       "conflict — exact contradiction hold, actor reuse required",
                existing_actor_reused_or_exact_contradiction_HOLD=True,
                no_duplicate_actor_or_event=True,
                mother_history_unchanged=True,
                unapproved_rng_draws=0,
                held_before_any_new_shared_event=True,
                existing_E_pre_hash_unchanged=True,
                existing_E_pre_refs=[e["event_id"] for e in existing_shared],
                retroactive_repair_attempted=False,
            )
        else:
            terminal = typed(S.SCENARIOS_VALID_EMPTY, n_candidates=len(classes))
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, [], None, None, None, None, None, None,
                       None, causal_run_id, root_seed, policy_name)

    if ordinal_only_no_policy:
        terminal = typed(S.SELECTION_AUTHORITY_UNBOUND,
                         reason="only model ordinal rankings present; no adopted "
                                "numeric/equiprobable simulation policy owner",
                         rng_draw_count=0,
                         no_ordinal_to_weight_normalization=True)
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, None, None, None, None, None, None,
                       None, causal_run_id, root_seed, policy_name)

    if hold_missing_authority:
        terminal = typed(S.NOT_EXECUTED_AUTHORITY_HOLD,
                         reason="essential external rule/denominator/organismic witness unknown",
                         missing_authority=[hold_missing_authority],
                         status_is_HOLD_not_INFEASIBLE=True,
                         filler_facts_or_events=0)
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, None, None, None, None, None, None,
                       None, causal_run_id, root_seed, policy_name)

    # ---- selection ----
    scope = scope_hash(causal_run_id, anchor_hash, target_hash,
                       PROPOSAL_GRAMMAR_VERSION,
                       anchor_event_index=anchor["history_events"][-1]["effective_index"],
                       anchor_event_id=anchor["history_events"][-1]["event_id"])
    sel = adp020_select(policy_name, eligible, root_seed, scope,
                        occurrence_index=0, force_index=force_selection_index,
                        upstream_class_set_hash=record.dedup["class_set_hash"])
    costs.rng_draws += sel.get("n_draws", 0)
    ledger.add("SELECTION", sel)
    if sel.get("status") != S.COMMITTED:
        return _finish(ledger, costs, t0, sel, anchor_hash, target_hash,
                       guard, record, world, quals, sel, None, None, None, None, None,
                       None, causal_run_id, root_seed, policy_name)

    chosen_class = next(c for c in eligible
                        if c["class_key"] == sel["selected_class_key"])
    scenario = dict(chosen_class["candidate"])
    scenario["class_key"] = chosen_class["class_key"]

    # ---- existing shared event mutation control (K11-C2) ----
    if mutate_existing_shared_event:
        terminal = typed(
            S.SHARED_HISTORY_CONTRADICTION_HOLD,
            reason="back-generation proposed mismatched existing shared event E_pre",
            existing_E_pre_hash_unchanged=True,
            retroactive_repair_attempted=False,
            held_before_any_new_shared_event=True,
        )
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, sel, scenario, None, None, None,
                       None, None, causal_run_id, root_seed, policy_name)

    # ---- endpoint constraints for construction ----
    ec = scenario.get("endpoint_constraints") or {}
    if not isinstance(ec, dict):
        ec = {}
    place_by_route = {
        "ROUTE_INSTITUTIONAL": "INST_EVENING_CLASS_B",
        "ROUTE_LOCAL_CLOSED": "INST_WORKSHOP_A",
        "ROUTE_UNCONVENTIONAL": "INST_COMMUNITY_D",
        "ROUTE_MOBILITY": "INST_TRANSIT_E",
    }
    import copy
    ec_full=copy.deepcopy(ec)
    ec_full['route_kind_id']=scenario.get('route_kind_id')
    ec_full.setdefault('time_or_interval','T_ENCOUNTER_LAB_WINDOW')
    if 'required_state_predicates' not in ec_full:
        ec_full['required_state_predicates']=[dict(field='availability_status',equals='available_for_encounter'),
            dict(field='place',equals=place_by_route.get(scenario.get('route_kind_id')))]
    if endpoint_place_override is not None:
        ec_full['required_state_predicates']=[p for p in ec_full['required_state_predicates'] if p.get('field')!='place']+[dict(field='place',equals=endpoint_place_override)]
        ec_full['declared_test_intervention']='ENDPOINT_PLACE_OVERRIDE'

    # ---- second-parent construction ----
    if only_demographic_dad:
        terminal = typed(
            S.INDEPENDENT_PROJECT_PROOF_MISSING,
            reason="father supplied only as demographic profile; no independently "
                   "causal projects/memory/owner events",
            child_generation_commit=False,
            alt_status=S.PREHISTORY_OWNER_RULE_MISSING,
        )
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, sel, scenario, None, None, None,
                       None, None, causal_run_id, root_seed, policy_name)

    if dad_attempt_seeds is None:
        dad_attempt_seeds = [h_concat(root_seed, "DAD", str(i)) for i in range(4)]
    cons = construct_second_parent(chosen_class, ec_full, dad_attempt_seeds)
    costs.history_attempts += cons["n_attempts"]
    for a in cons["attempts"]:
        costs.actor_events += a["n_events"]
    ledger.add("CONSTRUCTION", {
        "terminal_status": cons["terminal_status"],
        "n_attempts": cons["n_attempts"],
        "selected_attempt_id": cons["selected_attempt_id"],
        "attempts": cons["attempts"],
    })
    if cons["terminal_status"] != S.COMMITTED:
        # Declared conditional selection/rejection sampler receipt: all attempts and
        # draws are persisted; NO silent resample; induced bias is reported or held.
        bias_report = {
            "sampler_kind": "DECLARED_CONDITIONAL_SELECTION_WITH_REJECTION",
            "selected_class_key": sel.get("selected_class_key"),
            "attempts_for_selected_class": cons["n_attempts"],
            "successes_for_selected_class": 0,
            "acceptance_rate_for_selected_class": 0.0,
            "unselected_class_acceptance_rates": "NOT_MEASURED_IN_THIS_RUN",
            "induced_distribution_note": (
                "success-conditional selection changes effective class frequencies; "
                "acceptance rate of the selected class is 0 under the tested endpoint"
            ),
            "unknown_bias_bounds": (
                "acceptance rates of unselected classes not measured here; residual "
                "selection bias not fully quantifiable from this run alone"
            ),
            "disposition": "SELECTION_BIAS_REPORTED_WITH_UNKNOWN_BOUNDS",
            "silent_resample_performed": False,
            "all_attempt_receipts_persisted": True,
            "causal_commit_for_failed_scenario": False,
        }
        terminal = typed(
            cons["terminal_status"],
            n_attempts=cons["n_attempts"],
            attempt_receipts=[{
                "attempt_id": a["attempt_id"], "status": a["status"],
                "endpoint_match": a["endpoint_match"],
            } for a in cons["attempts"]],
            silent_resample_performed=False,
            effective_selection_bias_report=bias_report,
        )
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, sel, scenario, cons, None, None,
                       None, None, causal_run_id, root_seed, policy_name,
                       dad_events=(cons["attempts"][-1].get("events")
                                   if cons.get("attempts") else None))

    dad_events = cons["selected_events"]
    dad_psyche = cons["selected_psyche"]

    if force_same_time_conflict:
        terminal = typed(
            S.AMBIGUOUS_SAME_TIME_CAUSAL_ORDER,
            reason="conflicting same-effective-time encounter/relationship proposals "
                   "without admitted precedence",
            lexicographic_priority_used=False,
            fictitious_events=0,
        )
        ledger.add("TERMINAL", terminal)
        return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                       guard, record, world, quals, sel, scenario, cons, None, None,
                       None, None, causal_run_id, root_seed, policy_name)

    # ---- relation reconciliation ----
    if joint_material_opportunity is not None:
        from .joint import observe_joint_actions
        scenario['joint_evidence']=observe_joint_actions(anchor,dad_events,joint_material_opportunity)
    rel = reconcile(anchor, dad_events, scenario,
                    force_mom_affectionate_dad_unknown=force_mom_affectionate_dad_unknown)
    ledger.add("RELATION", rel)
    if rel.get("status") not in (S.COMMITTED,):
        return _finish(ledger, costs, t0, rel, anchor_hash, target_hash,
                       guard, record, world, quals, sel, scenario, cons, rel, None,
                       None, None, causal_run_id, root_seed, policy_name)

    from .endpoint import joint_obligations
    endpoint_obligations=joint_obligations(anchor,dad_events,rel,ec_full)
    ledger.add('SELECTED_ENDPOINT_JOINT_OBLIGATIONS',endpoint_obligations)
    if endpoint_obligations['errors']:
        terminal=typed(endpoint_obligations['status'],selected_endpoint_obligations=endpoint_obligations)
        return _finish(ledger,costs,t0,terminal,anchor_hash,target_hash,guard,record,world,quals,sel,scenario,cons,rel,None,None,None,causal_run_id,root_seed,policy_name)

    # ---- boundary + continuation + child env fixture ----
    boundary = lab_conception_boundary()
    cont = forward_continuation(anchor, dad_events, rel,contact_material=continued_joint_material)
    child = child_developmental_environment_fixture(anchor, dad_events, cont, boundary)
    ledger.add("BOUNDARY_CONTINUATION_CHILD", {
        "boundary": boundary,
        "continuation_events": len(cont["continuation_events"]),
        "child_fixture_id": child["fixture_id"],
    })

    # ---- two DAGs ----
    cons_graph = build_construction_graph([])
    from .joint import joint_event_closure
    causal_graph = build_causal_graph(anchor["history_events"], dad_events,
                                      cont["continuation_events"]+joint_event_closure(rel,cont))
    dag = validate_two_dags(cons_graph, causal_graph)
    ledger.add("DAG_VALIDATION", dag)

    # ---- mother invariance re-check ----
    anchor_hash_after = anchor_cp.hash()
    mother_invariant = anchor_hash_after == anchor_hash

    terminal = {
        "status": S.COMMITTED if dag["status"]==S.LAB_PASS else S.CAUSAL_TEMPORAL_INVERSION,
        "lab_terminal": dag["status"],
        "lab_rule": LAB_RULE_STATUS,
        "contract_version": CONTRACT_VERSION,
        "k11_contract": K11_CONTRACT,
        "pipeline_version": PIPELINE_VERSION,
        "mother_checkpoint_byte_identity_unchanged": mother_invariant,
        "target_status": S.TARGET_PENDING,
        "conception_admitted": False,
        "child_generated_events": 0,
        "lab_conception_boundary": LAB_CONCEPTION_BOUNDARY,
    }
    ledger.add("TERMINAL", terminal)
    return _finish(ledger, costs, t0, terminal, anchor_hash, target_hash,
                   guard, record, world, quals, sel, scenario, cons, rel, boundary,
                   child, cont, causal_run_id, root_seed, policy_name,
                   dag=dag, anchor_cp=anchor_cp, dad_events=dad_events,
                   dad_psyche=dad_psyche, anchor=anchor, world_obj=world)


def _finish(ledger, costs, t0, terminal, anchor_hash, target_hash, guard,
            record, world, quals, sel, scenario, cons, rel, boundary, child, cont,
            causal_run_id, root_seed, policy_name, dag=None, anchor_cp=None,
            dad_events=None, dad_psyche=None, anchor=None, world_obj=None):
    costs.wall_seconds = round(time.perf_counter() - t0, 6)
    replay_seconds = 0.0
    if cons and cons.get("attempts"):
        replay_seconds = sum(a.get("replay", {}).get("replay_seconds", 0)
                             for a in cons["attempts"])
    costs.replay_seconds = round(replay_seconds, 6)
    guard_result = guard.assert_clean()
    result = {
        "terminal": terminal,
        "cost": costs.as_dict(),
        "guard": guard_result,
        "ledger_hash": ledger.hash(),
        "ledger": ledger.as_dict(),
        "inputs": {
            "causal_run_id": causal_run_id,
            "root_seed": root_seed,
            "policy_name": policy_name,
            "mother_anchor_hash": anchor_hash,
            "target_hash": target_hash,
        },
        "proposal_record_summary": {
            "record_id": record.record_id if record else None,
            "proposal_hash": record.proposal_hash if record else None,
            "automated_status": record.lmm_automated_status if record else None,
            "model_returned": record.model_returned if record else None,
        } if record is not None else None,
        "selection_summary": {
            k: sel.get(k) for k in (
                "decision_kind", "stream", "scope_hash", "policy_name", "policy_hash",
                "candidate_set_hash", "upstream_class_set_hash",
                "canonical_class_order", "eligible_set",
                "class_weights", "n_draws", "draw_mode", "selected_class_key",
                "selected_representative_id", "unreported_redraws",
                "no_population_frequency_claim",
            )
        } if sel is not None else None,
        "scenario": scenario,
        "construction_summary": {
            "n_attempts": cons.get("n_attempts"),
            "attempt_seeds": cons.get("attempt_seeds"),
            "selected_attempt_id": cons.get("selected_attempt_id"),
            "terminal_status": cons.get("terminal_status"),
            "attempts": cons.get("attempts"),
        } if cons is not None else None,
        "relation": rel,
        "boundary": boundary,
        "continuation": cont,
        "child_fixture": child,
        "dag_validation": dag,
        "dad_events": dad_events,
        "dad_psyche": dad_psyche,
        "anchor": anchor,
        "world_ref": world.ref() if world is not None else None,
    }
    # replay ledger byte estimate
    import json as _json
    result["cost"]["replay_ledger_bytes"] = len(
        _json.dumps(result["construction_summary"] or {}, sort_keys=True).encode()
    )
    def semantic(v):
        if isinstance(v,dict):return {k:semantic(x) for k,x in v.items() if not k.endswith('seconds')}
        if isinstance(v,list):return [semantic(x) for x in v]
        return v
    # Complete recoverable causal record, separate from measured run duration.
    result['causal_replay_record']=semantic(dict(inputs=result['inputs'],terminal=terminal,
        selected_decision_receipt=sel,scenario=scenario,construction=cons,
        anchor=anchor if anchor is not None else (anchor_cp.anchor_dict() if anchor_cp else None),
        relation=rel,boundary=boundary,child_context=child,continuation=cont,
        dag=dag,guard=guard_result,ledger=ledger.as_dict(),dad_events=dad_events,dad_psyche=dad_psyche))
    result['causal_replay_hash']=h_obj(result['causal_replay_record'])
    return result
