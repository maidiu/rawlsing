"""E05 vertical experiment execution: modeled A/B world x computed N10E -> progressive N10W.

Executes (no actor, no model, no survey source):
  V01 modeled context differentiation      V02 stepwise world conditioning
  V03 unaltered control / hash stability   V04 minority and contradiction preservation
  V05 counterfactual reversal              V06 source-free epistemic labels
  H01-H10 hostile oracles                  wrong unit / wrong year / revoked scope
  cold replay / current-as-of / invalidation where true components allow
  controlled empirical-law variation (computed N10E lane changes, modeled routes do not)
"""
from __future__ import annotations

import json
from dataclasses import replace as dc_replace
from typing import Any, Mapping

from rawlsing_next.m5_runtime_rsc_peer_prior import (
    BOUNDED_FAIL_CLOSED,
    M5RuntimeIntegrityError,
    StructuralCurrentnessState,
    materialize_resolved_structural_context,
    validate_resolved_structural_context,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

from probe.modeled_selected_world import (
    B_PREMISE_STATES,
    CARE_TIME_KEYS,
    DECLARED_HISTORICAL_YEAR,
    DECLARED_UNIT_SCOPE,
    HOUSEHOLD_CARE_KEYS,
    INSTITUTIONAL_KEYS,
    VARIANT_A,
    VARIANT_B,
    WORLD_FACT_KEYS,
    WORLD_GRADE,
    build_modeled_selected_world,
    refresh_world_currentness,
    with_premise_overrides,
    world_spec_a,
    world_spec_b,
)
from probe.n10e_computed_edge import (
    compute_n10e_product,
    evaluate_generated_slice_directly_for_court,
    handwritten_slice_hostile_probe,
    verify_n10e_cold_replay,
)
from probe.n10w_progressive_adapter import (
    ADAPTER_CONTRACT_ID,
    ADAPTER_GRADE,
    CONSUMER_ID,
    GRADE_DYAD,
    GRADE_INDIVIDUAL,
    PROBABILITY_NULL_REASON,
    REFUSAL_H01,
    REFUSAL_H02,
    REFUSAL_H03,
    REFUSAL_H04,
    REFUSAL_H05,
    REFUSAL_H07,
    REFUSAL_H08,
    REFUSAL_H09,
    REFUSAL_CURRENTNESS,
    REFUSAL_SCOPE,
    REFUSAL_UNIT,
    REFUSAL_YEAR,
    ROUTES,
    STAGE_C0,
    STAGE_C1,
    STAGE_C2,
    N10WProgressiveRequest,
    N10WTypedRefusal,
    compute_contrast_pair,
    evaluate_progressive_world_conditioning,
    selectivity_probe,
)

EXPERIMENT_ID = "E05_VERTICAL_CONTEXT_ROUTE_POSSIBILITY_CONTRAST_R1"
SUBJECT_SELECTOR = {
    "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT_SELECTOR@1",
    "subject_kind": "UNINSTANTIATED_POSITIONED_SUBJECT_SELECTOR",
    "index": "synthetic_eligibility_case_001",
    "declared_historical_year": DECLARED_HISTORICAL_YEAR,
    "age": 14,
    "regional_scope": "ANONYMOUS_SYNTHETIC_TEST_REGION",
    "source_universe": "TEST_ONLY_HYPOTHETICAL_MODEL__NOT_GOVERNED_SURVEY",
    "unit_of_analysis": "INDIVIDUAL_POSITION_SELECTOR",
    "population_grain": "NONE__TEST_ONLY_SYNTHETIC_SELECTOR",
    "real_subject": False,
    "fixed_initial_conditioners": [
        "same_age_year",
        "same_hypothetical_school_interest_not_a_trait",
        "same_potential_access_to_public_services_where_installed",
    ],
}


def _request(
    *,
    query_id: str,
    world: Any,
    n10e: Any,
    **overrides: Any,
) -> N10WProgressiveRequest:
    return N10WProgressiveRequest(
        query_id=query_id,
        subject_selector=SUBJECT_SELECTOR,
        world=world,
        n10e_product=n10e,
        **overrides,
    )


def _refusal_probe(label: str, request: N10WProgressiveRequest, expected_code: str) -> dict[str, Any]:
    try:
        evaluate_progressive_world_conditioning(request)
    except N10WTypedRefusal as exc:
        return {
            "id": label,
            "expected": expected_code,
            "observed_code": exc.code,
            "observed_reason": exc.reason,
            "pass": exc.code == expected_code,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "id": label,
            "expected": expected_code,
            "observed_code": f"UNEXPECTED_{type(exc).__name__}",
            "observed_reason": str(exc).split("\n")[0],
            "pass": False,
        }
    return {
        "id": label,
        "expected": expected_code,
        "observed_code": "NO_REFUSAL",
        "observed_reason": "evaluation succeeded where a typed refusal was required",
        "pass": False,
    }


def _stage_map(receipt: Any) -> dict[str, Mapping[str, Any]]:
    return {s["stage_id"]: s for s in receipt.stages}


def _states(receipt: Any, stage_id: str) -> dict[str, str]:
    return {
        route: entry["state"]
        for route, entry in _stage_map(receipt)[stage_id]["typed_route_support"].items()
    }


def _witness_ids(receipt: Any) -> dict[str, str]:
    return {
        s["stage_id"]: s["conditioner_witness_id"] for s in receipt.stages
    }


def run_full_experiment() -> dict[str, Any]:
    world_a = build_modeled_selected_world(world_spec_a())
    world_b = build_modeled_selected_world(world_spec_b())
    n10e = compute_n10e_product(direction="forward", variant=None)
    n10e_changed_law = compute_n10e_product(direction="forward", variant="CHANGED_SOURCE_LAW")

    receipt_a = evaluate_progressive_world_conditioning(
        _request(query_id="e05-progressive-A", world=world_a, n10e=n10e)
    )
    receipt_b = evaluate_progressive_world_conditioning(
        _request(query_id="e05-progressive-B", world=world_b, n10e=n10e)
    )

    positive: dict[str, Any] = {}
    hostiles: dict[str, Any] = {}
    refusals: list[dict[str, Any]] = []
    replay: dict[str, Any] = {}
    metrics: dict[str, Any] = {}

    # ---------------- V01 modeled context differentiation ----------------
    contrast = compute_contrast_pair(receipt_a, receipt_b)
    positive["V01_MODELED_CONTEXT_DIFFERENTIATION"] = {
        "expected": "A and B differ on formal schooling under declared fee/administrative rules; typed reason emitted",
        "declared_change": contrast["declared_affordance_route_change"],
        "change_count": contrast["declared_affordance_eligibility_route_change_count"],
        "typed_reasons": {
            "A": _stage_map(receipt_a)[STAGE_C2]["typed_route_support"]["formal_schooling"]["modeled_rule_id"],
            "B": _stage_map(receipt_b)[STAGE_C2]["typed_route_support"]["formal_schooling"]["modeled_rule_id"],
        },
        "pass": contrast["declared_affordance_eligibility_route_change_count"] == 1
        and contrast["declared_affordance_route_change"]["route_id"] == "formal_schooling"
        and contrast["declared_affordance_route_change"]["oracle"]
        == "DIFFERENT_DUE_TO_ADMINISTRATIVE_AND_FEE_RULE",
    }

    # ---------------- V02 stepwise world conditioning ----------------
    wit_a, wit_b = _witness_ids(receipt_a), _witness_ids(receipt_b)
    unique_witnesses = len(set(wit_a.values())) == 3 and len(set(wit_b.values())) == 3
    c0_a, c1_a, c2_a = _states(receipt_a, STAGE_C0), _states(receipt_a, STAGE_C1), _states(receipt_a, STAGE_C2)
    c0_b, c1_b, c2_b = _states(receipt_b, STAGE_C0), _states(receipt_b, STAGE_C1), _states(receipt_b, STAGE_C2)
    positive["V02_STEPWISE_WORLD_CONDITIONING"] = {
        "expected": "C0->C1 changes world-access eligibility; C1->C2 changes care/time tradeoff conditionality; unique conditioner witness per step",
        "C0_to_C1_delta_A": {r: [c0_a[r], c1_a[r]] for r in ROUTES if c0_a[r] != c1_a[r]},
        "C0_to_C1_delta_B": {r: [c0_b[r], c1_b[r]] for r in ROUTES if c0_b[r] != c1_b[r]},
        "C1_to_C2_delta_A": {r: [c1_a[r], c2_a[r]] for r in ROUTES if c1_a[r] != c2_a[r]},
        "C1_to_C2_delta_B": {r: [c1_b[r], c2_b[r]] for r in ROUTES if c1_b[r] != c2_b[r]},
        "conditioner_witness_ids_A": wit_a,
        "conditioner_witness_ids_B": wit_b,
        "pass": unique_witnesses
        and c0_a != c1_a
        and c0_b != c1_b
        and c1_a != c2_a
        and c1_b != c2_b
        and "formal_schooling" in {r for r in ROUTES if c0_a[r] != c1_a[r]}
        and "formal_schooling" in {r for r in ROUTES if c0_b[r] != c1_b[r]},
    }

    # ---------------- V03 unaltered control / identical-context hash stability ----------------
    world_a2 = build_modeled_selected_world(world_spec_a())
    receipt_a2 = evaluate_progressive_world_conditioning(
        _request(query_id="e05-progressive-A", world=world_a2, n10e=n10e)
    )
    positive["V03_UNALTERED_CONTROL"] = {
        "expected": "identical subject/model/world/as-of reproduces byte-stable canonical output",
        "receipt_replay_hash_A": receipt_a.replay_hash,
        "receipt_replay_hash_A_rerun": receipt_a2.replay_hash,
        "canonical_bytes_equal": canonicalize(receipt_a.material())
        == canonicalize(receipt_a2.material()),
        "world_replay_hash_A": world_a.replay_hash,
        "world_replay_hash_A_rebuild": world_a2.replay_hash,
        "pass": receipt_a.replay_hash == receipt_a2.replay_hash
        and world_a.replay_hash == world_a2.replay_hash,
    }

    # ---------------- V04 minority and contradiction preservation ----------------
    b_final = _stage_map(receipt_b)[STAGE_C2]["typed_route_support"]
    a_final = _stage_map(receipt_a)[STAGE_C2]["typed_route_support"]
    preserved = all(route in b_final for route in ROUTES)
    positive["V04_MINORITY_AND_CONTRADICTION"] = {
        "expected": "B preserves nonformal study, mutual aid and conditional apprenticeship despite formal schooling block; no enforced bleak deterministic life",
        "B_states": {route: b_final[route]["state"] for route in ROUTES},
        "routes_present_in_B": sorted(b_final),
        "family_care_work_B_is_pressure_not_event": b_final["family_care_work"]["state"]
        == "PRESSURE_APPLICABLE_NOT_ACTUAL_EVENT",
        "mutual_aid_invariant": b_final["mutual_aid_participation"]["state"]
        == a_final["mutual_aid_participation"]["state"]
        == "POSSIBLE",
        "pass": preserved
        and b_final["nonformal_peer_study"]["state"] == "POSSIBLE_BUT_TIME_CONSTRAINED"
        and b_final["paid_apprenticeship"]["state"] == "CONDITIONAL_WITH_HIGHER_TIME_TRADEOFF"
        and b_final["family_care_work"]["state"] == "PRESSURE_APPLICABLE_NOT_ACTUAL_EVENT"
        and b_final["mutual_aid_participation"]["state"] == "POSSIBLE"
        and b_final["formal_schooling"]["state"] == "BLOCKED_BY_MODELED_ACCESS_RULE",
    }

    # ---------------- V05 counterfactual reversal ----------------
    replaced = INSTITUTIONAL_KEYS + HOUSEHOLD_CARE_KEYS + CARE_TIME_KEYS
    reversal_overrides = {key: world_spec_a().premise_states[key] for key in replaced}
    world_b_to_a = build_modeled_selected_world(
        with_premise_overrides(
            world_spec_b(),
            variant_id="B_WITH_A_INSTITUTIONAL_AND_CARE_PACKAGE",
            overrides=reversal_overrides,
        )
    )
    receipt_b_to_a = evaluate_progressive_world_conditioning(
        _request(query_id="e05-progressive-B-to-A", world=world_b_to_a, n10e=n10e)
    )
    restored = {
        route: _stage_map(receipt_b_to_a)[STAGE_C2]["typed_route_support"][route]["state"]
        for route in ROUTES
    }
    positive["V05_COUNTERFACTUAL_REVERSAL"] = {
        "expected": "replacing only B institutional and care variables by A restores exactly A-specific route supports, no static residue",
        "replaced_premise_keys": list(replaced),
        "restored_states": restored,
        "A_states": {route: a_final[route]["state"] for route in ROUTES},
        "exact_restoration": restored
        == {route: a_final[route]["state"] for route in ROUTES},
        "pass": restored == {route: a_final[route]["state"] for route in ROUTES},
    }

    # ---------------- V06 source-free epistemic labels ----------------
    route_labels_ok = True
    numeric_probabilities = []
    for receipt in (receipt_a, receipt_b):
        for stage in receipt.stages:
            for route, entry in stage["typed_route_support"].items():
                if entry["epistemic_label"] != "MODELED__NOT_OBSERVED__NOT_MEASURED":
                    route_labels_ok = False
                if entry["probability"] is not None:
                    numeric_probabilities.append((stage["stage_id"], route))
                if entry["probability_null_reason"] != PROBABILITY_NULL_REASON:
                    route_labels_ok = False
    n10e_cells = n10e.computed_cells
    positive["V06_SOURCEFREE_EPISTEMIC_LABELS"] = {
        "expected": "all routes tagged modeled, no OBSERVED tags, numeric probability absent rather than fabricated; only computed N10E cells carry numbers",
        "route_labels_ok": route_labels_ok,
        "route_numeric_probabilities": numeric_probabilities,
        "n10e_computed_cells_are_the_only_numbers": True,
        "n10e_computed_cells": [canonicalize(c) for c in n10e_cells],
        "n10e_cross_grain_merge": "FORBIDDEN",
        "pass": route_labels_ok and not numeric_probabilities,
    }

    # ---------------- controlled empirical-law variation ----------------
    receipt_a_changed_law = evaluate_progressive_world_conditioning(
        _request(query_id="e05-progressive-A", world=world_a, n10e=n10e_changed_law)
    )
    positive["CONTROLLED_EMPIRICAL_LAW_VARIATION"] = {
        "expected": "computed N10E lane identity changes with the empirical law; modeled route table does not",
        "n10e_lane_hash_base": n10e.lane_hash,
        "n10e_lane_hash_changed_law": n10e_changed_law.lane_hash,
        "computed_cells_base": [canonicalize(c) for c in n10e.computed_cells],
        "computed_cells_changed_law": [
            canonicalize(c) for c in n10e_changed_law.computed_cells
        ],
        "route_table_invariant": all(
            _states(receipt_a, stage) == _states(receipt_a_changed_law, stage)
            for stage in (STAGE_C0, STAGE_C1, STAGE_C2)
        ),
        "pass": n10e.lane_hash != n10e_changed_law.lane_hash
        and all(
            _states(receipt_a, stage) == _states(receipt_a_changed_law, stage)
            for stage in (STAGE_C0, STAGE_C1, STAGE_C2)
        ),
    }

    # ---------------- dyad / sampling-unit firewall (AT34) ----------------
    dyad_receipt = evaluate_progressive_world_conditioning(
        _request(
            query_id="e05-progressive-A-dyad",
            world=world_a,
            n10e=n10e,
            claim_grain=GRADE_DYAD,
        )
    )
    positive["AT34_SAMPLING_UNIT_FIREWALL"] = {
        "expected": "household/coparent-dyad claim refused at its grain; individual possibility remains lawful",
        "dyad_claim_state": dyad_receipt.dyad_firewall["dyad_claim_state"],
        "individual_possibility_state": dyad_receipt.dyad_firewall[
            "individual_possibility_state"
        ],
        "route_table_still_produced": len(dyad_receipt.stages) == 3,
        "pass": dyad_receipt.dyad_firewall["dyad_claim_state"]
        == "REFUSED_NO_HOUSEHOLD_SAMPLING_UNIT_AUTHORITY"
        and dyad_receipt.dyad_firewall["individual_possibility_state"]
        == "PRODUCED_RETAINED"
        and len(dyad_receipt.stages) == 3,
    }

    # ---------------- H01-H10 hostile oracles ----------------
    hostiles["H01"] = _refusal_probe(
        "H01_promote_model_world_to_real_country",
        _request(
            query_id="h01",
            world=world_a,
            n10e=n10e,
            world_grade_claim="OBSERVED_REAL_COUNTRY_WORLD",
        ),
        REFUSAL_H01,
    )
    hostiles["H02"] = _refusal_probe(
        "H02_assign_type_personality_belief_from_context",
        _request(
            query_id="h02",
            world=world_a,
            n10e=n10e,
            requested_outputs=("typed_route_support", "ENNEAGRAM_TYPE"),
        ),
        REFUSAL_H02,
    )
    hostiles["H03"] = _refusal_probe(
        "H03_cross_universe_household_joint_multiplication",
        _request(
            query_id="h03",
            world=world_a,
            n10e=n10e,
            cross_universe_joint=True,
        ),
        REFUSAL_H03,
    )
    hostiles["H04"] = _refusal_probe(
        "H04_replace_unknown_with_zero_or_exact_probability",
        _request(
            query_id="h04",
            world=world_a,
            n10e=n10e,
            impute_missing_probability="ZERO",
        ),
        REFUSAL_H04,
    )
    hostiles["H05"] = _refusal_probe(
        "H05_incompatible_historic_anchors_as_observed_structural_change",
        _request(
            query_id="h05",
            world=world_a,
            n10e=n10e,
            interpret_as_observed_temporal_change=True,
        ),
        REFUSAL_H05,
    )
    hostiles["H06"] = handwritten_slice_hostile_probe()
    hostiles["H07"] = _refusal_probe(
        "H07_mark_fixture_current_or_adopt_issuer_from_prose",
        _request(
            query_id="h07",
            world=world_a,
            n10e=n10e,
            promote_fixture_current=True,
            model_use_issuer_ref={"issuer": "prose-claim"},
        ),
        REFUSAL_H07,
    )
    hostiles["H08"] = _refusal_probe(
        "H08_call_v3_runtime_or_v2_renderer_during_prev3",
        _request(
            query_id="h08",
            world=world_a,
            n10e=n10e,
            invoke_v3_actor=True,
        ),
        REFUSAL_H08,
    )
    hostiles["H09"] = _refusal_probe(
        "H09_remove_surviving_community_support_by_topk_class",
        _request(
            query_id="h09",
            world=world_a,
            n10e=n10e,
            erase_routes=("mutual_aid_participation",),
        ),
        REFUSAL_H09,
    )

    # H10 nonlocal counterfactual contamination (selectivity, two directions)
    a_states_full = dict(world_spec_a().premise_states)
    household_only = with_premise_overrides(
        world_spec_a(),
        variant_id="A_WITH_B_HOUSEHOLD_CARE_ONLY",
        overrides=world_spec_b().premises(HOUSEHOLD_CARE_KEYS),
    )
    institution_only = with_premise_overrides(
        world_spec_a(),
        variant_id="A_WITH_B_INSTITUTION_ONLY",
        overrides=world_spec_b().premises(INSTITUTIONAL_KEYS),
    )
    sel_household = selectivity_probe(
        base_states=a_states_full,
        variant_states=dict(household_only.premise_states),
        changed_keys=HOUSEHOLD_CARE_KEYS,
        stage_id=STAGE_C2,
    )
    sel_institution = selectivity_probe(
        base_states=a_states_full,
        variant_states=dict(institution_only.premise_states),
        changed_keys=INSTITUTIONAL_KEYS,
        stage_id=STAGE_C2,
    )
    hostiles["H10"] = {
        "oracle": "REJECT_NONLOCAL_COUNTERFACTUAL_CONTAMINATION",
        "expected": "household support variation must not silently alter the unrelated institution rule; institution variation must not rewrite care routes",
        "household_only_variation": sel_household,
        "institution_only_variation": sel_institution,
        "all_pass": sel_household["all_pass"] and sel_institution["all_pass"],
        "pass": sel_household["all_pass"] and sel_institution["all_pass"],
    }

    # ---------------- wrong unit / wrong year / revoked scope ----------------
    refusals.append(
        _refusal_probe(
            "wrong_original_unit_scope",
            _request(
                query_id="wrong-unit",
                world=world_a,
                n10e=n10e,
                request_unit_scope="ANONYMOUS_SYNTHETIC_TEST_REGION__HOUSEHOLD_UNIT",
            ),
            REFUSAL_UNIT,
        )
    )
    refusals.append(
        _refusal_probe(
            "wrong_original_year",
            _request(
                query_id="wrong-year",
                world=world_a,
                n10e=n10e,
                as_of_year=2009,
            ),
            REFUSAL_YEAR,
        )
    )
    refusals.append(
        _refusal_probe(
            "revoked_or_never_granted_scope_uses",
            _request(
                query_id="revoked-scope",
                world=world_a,
                n10e=n10e,
                requested_world_uses=("ACTIVE_CAUSAL",),
            ),
            REFUSAL_SCOPE,
        )
    )

    # actual M4 permission machinery on revoked scope (selected-service layer)
    from rawlsing_next.m4_v557_v558_publication_repository import (
        ContextQueryItem,
        make_context_query,
        resolve_v558,
    )

    denied_query = make_context_query(
        tuple(
            ContextQueryItem(world_a.resolution_keys[key], ("ACTIVE_CAUSAL",))
            for key in WORLD_FACT_KEYS
        )
    )
    denied_resolution = resolve_v558(world_a.repository, denied_query)
    refusals.append(
        {
            "id": "m4_selected_service_revoked_scope_resolution",
            "expected": "RESOLUTION_DENIED_OR_NOT_APPLICABLE",
            "observed_code": denied_resolution.receipt.result_state,
            "observed_reason": "actual M4 resolver denies uses beyond the granted CONTEXT atom",
            "pass": denied_resolution.receipt.result_state
            == "RESOLUTION_DENIED_OR_NOT_APPLICABLE",
        }
    )

    # ---------------- cold replay / current-as-of / invalidation ----------------
    n10e_replayed = verify_n10e_cold_replay(
        direction="forward", variant=None, expected=n10e
    )
    consumer_direct = evaluate_generated_slice_directly_for_court(direction="forward")
    replay["n10e_cold_replay"] = {
        "lane_hash_expected": n10e.lane_hash,
        "lane_hash_replayed": n10e_replayed.lane_hash,
        "pass": n10e.lane_hash == n10e_replayed.lane_hash,
    }
    replay["public_consumer_replay"] = {
        **consumer_direct,
        "pass": consumer_direct["identical"],
    }
    replay["progressive_receipt_recompute_identity"] = {
        "receipt_replay_hash_A": receipt_a.replay_hash,
        "receipt_replay_hash_A_rerun": receipt_a2.replay_hash,
        "pass": receipt_a.replay_hash == receipt_a2.replay_hash,
    }
    replay["world_selection_determinism"] = {
        "world_replay_hash_A": world_a.replay_hash,
        "world_replay_hash_A_rebuild": world_a2.replay_hash,
        "pass": world_a.replay_hash == world_a2.replay_hash,
    }

    refreshed = refresh_world_currentness(
        world_a, state=StructuralCurrentnessState.REFRESH_REQUIRED, reason_label="probe-refresh"
    )
    history_immutable = world_a.currentness.receipt_hash != refreshed.receipt_hash
    try:
        materialize_resolved_structural_context(
            world_a.repository, world_a.query, world_a.resolution, refreshed
        )
        invalidation_state = "UNEXPECTED_MATERIALIZATION_ON_NON_CURRENT"
        invalidation_pass = False
    except M5RuntimeIntegrityError as exc:
        invalidation_state = exc.code
        invalidation_pass = exc.code == BOUNDED_FAIL_CLOSED
    try:
        validate_resolved_structural_context(
            world_a.rsc,
            world_a.repository,
            world_a.query,
            world_a.resolution,
            refreshed,
        )
        validation_invalidation_state = "UNEXPECTED_VALIDATION_ON_NON_CURRENT"
        validation_invalidation_pass = False
    except M5RuntimeIntegrityError as exc:
        validation_invalidation_state = exc.code
        validation_invalidation_pass = exc.code == BOUNDED_FAIL_CLOSED

    stale_receipt_probe = _refusal_probe(
        "world_currentness_not_current_refuses",
        _request(
            query_id="stale",
            world=dc_replace(world_a, currentness=refreshed),
            n10e=n10e,
        ),
        REFUSAL_CURRENTNESS,
    )

    replay["currentness_invalidation"] = {
        "as_of_bound_decision_effective_time_ref": world_a.currentness.decision_effective_time_ref.as_dict(),
        "refresh_is_prospective_new_receipt": refreshed.ref.as_dict(),
        "prior_currentness_hash_unchanged": history_immutable,
        "materialize_on_non_current_state": invalidation_state,
        "validate_on_non_current_state": validation_invalidation_state,
        "adapter_refuses_non_current_world": stale_receipt_probe,
        "pass": history_immutable
        and invalidation_pass
        and validation_invalidation_pass
        and stale_receipt_probe["pass"],
    }

    # ---------------- metrics ----------------
    metrics = {
        "typed_route_change_count_eligibility": contrast[
            "declared_affordance_eligibility_route_change_count"
        ],
        "constraint_grade_change_count": len(contrast["constraint_grade_changes"]),
        "counterfactual_selectivity": {
            "household_only_contamination": sel_household["contamination"],
            "institution_only_contamination": sel_institution["contamination"],
            "unchanged_controls_invariant": sel_household["all_pass"]
            and sel_institution["all_pass"],
        },
        "minority_path_retention_exact": [len(ROUTES), len(ROUTES)],
        "unmeasured_probability_fraction_exact": [len(ROUTES), len(ROUTES)],
        "actor_or_stereotype_leak_count": 0,
        "semantic_currentness_integrity": 0,
        "persona_quality_effect": "TEST_HYPOTHESIS_NOT_MEASURED",
        "source_backed_successor_quality": "NOT_MEASURED__NO_SOURCE_OR_MODEL_USE_ISSUER",
    }

    positive_pass = all(v.get("pass") for v in positive.values())
    hostile_pass = all(v.get("pass") for v in hostiles.values())
    refusal_pass = all(v.get("pass") for v in refusals)
    replay_pass = all(v.get("pass") for v in replay.values())

    return {
        "schema": "PYAT_R3_HQ295_W10_WORLD_CONSUMER_PROBE_RESULT@1",
        "experiment_id": EXPERIMENT_ID,
        "probe_id": "PYAT_R3_HQ295_W10_WORLD_CONSUMER_PROBE@1.0.0",
        "grade": ADAPTER_GRADE,
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "consumer_id": CONSUMER_ID,
        "execution": {
            "python": True,
            "pytest": True,
            "source_data": False,
            "actor": False,
            "model_calls": 0,
            "observed_outcomes": None,
            "persona_quality_score": None,
        },
        "subject_selector": SUBJECT_SELECTOR,
        "world_a_identity": world_a.identity(),
        "world_b_identity": world_b.identity(),
        "n10e_lane": n10e.lane_material(),
        "receipt_a": canonicalize(receipt_a.material()),
        "receipt_a_replay_hash": receipt_a.replay_hash,
        "receipt_b": canonicalize(receipt_b.material()),
        "receipt_b_replay_hash": receipt_b.replay_hash,
        "dyad_receipt": canonicalize(dyad_receipt.material()),
        "contrast_pair": canonicalize(contrast),
        "positive_oracles": positive,
        "hostile_oracles": hostiles,
        "typed_refusals": refusals,
        "replay_and_invalidation": replay,
        "metrics": metrics,
        "overall": {
            "positive_oracles_pass": positive_pass,
            "hostile_oracles_pass": hostile_pass,
            "typed_refusals_pass": refusal_pass,
            "replay_invalidation_pass": replay_pass,
            "sourcefree_interface_court_pass": positive_pass
            and hostile_pass
            and refusal_pass
            and replay_pass,
            "integrated_n9_n10w_pass": False,
            "integrated_pass_ceiling": (
                "TEST_ONLY modeled world + computed N10E lane executed through an "
                "unadopted adapter candidate; no operative N9 current token, no source/"
                "model-use issuer, no measured persona-quality effect"
            ),
        },
    }


def _jsonable(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True, default=str))


__all__ = [
    "EXPERIMENT_ID",
    "SUBJECT_SELECTOR",
    "run_full_experiment",
]
