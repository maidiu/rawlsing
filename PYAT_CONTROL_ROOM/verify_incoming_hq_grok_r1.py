#!/usr/bin/env python3
"""Check structural completeness of a proposed Pyat HQ accession dossier.

NOT a scientific, source-use, persona-quality, or independent-review verifier.
By default the template FAILS. This script never grants HQ legitimacy.
Usage: python PYAT_CONTROL_ROOM/verify_incoming_hq_grok_r1.py path/to/accession.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_FUNCTIONS = {
    "crosswave_atlas_semantic_mapping",
    "driver_facet_scale_semantic_authority",
    "source_population_conditioning_weights",
    "cross_source_statistical_synthesis_proxies",
    "recursive_empirical_discovery_higher_order",
    "temporal_wave_harmonization",
    "temporal_structural_pressure_and_age_cohort",
    "selected_world_to_v3_development_to_v2",
}
REQUIRED_PROOFS = {
    "live_control_and_handoff",
    "original_persona_and_terminal_demand",
    "pre_main_pyat_full_machine",
    "dva_trii_chetiri",
    "long_memory_current_succession",
    "crosswave_semantic_driver_facet",
    "empirical_inference_and_synthesis",
    "historical_temporal_and_current_successor",
    "objective_selected_world_and_v3_v2",
    "fresh_methods_comparison_and_improvement",
    "end_product_test_and_sensitivity",
    "scientific_scope_35wave_and_authority",
    "resource_privacy_and_worktree",
    "parallel_flight_and_model_economy",
    "terminal_artifact_continuity",
}
VALID_DECISIONS = {
    "REUSE_AS_IS",
    "INTEGRATE_OR_ADAPT",
    "IMPROVE_OR_COMPLETE",
    "REPLACE_AFTER_COMPARATIVE_PROOF",
    "NO_DECISION__NEEDS_EVIDENCE",
}
VALID_FUNCTIONAL_STATES = {
    "CURRENT_ADOPTED",
    "IMPLEMENTED_UNADOPTED",
    "HISTORICAL_FUNCTIONAL_CANDIDATE",
    "STRANDED",
    "SUPERSEDED_PROVED",
    "UNKNOWN_NEEDS_CHECK",
    "REAL_FUNCTIONAL_GAP",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")

def meaningful(x):
    return isinstance(x, str) and bool(x.strip()) and x.strip() not in {
        "UNKNOWN", "NONE", "TBD", "NOT_PROVED", "NOT_YET_VERIFIED", "UNVERIFIED",
    }

def check(record):
    errors = []
    if record.get("schema") != "PYAT_INCOMING_HQ_GROK_ATTESTATION_R1":
        errors.append("wrong schema")
    if record.get("template") is not False:
        errors.append("template is not an accession: set template=false in a distinct new dossier")
    identity = record.get("candidate") or {}
    for key in ("session_or_accession_id", "branch", "proposed_hq_label",
                "prior_sealed_handoff_sha", "current_remote_control_sha"):
        val = identity.get(key)
        if not meaningful(val):
            errors.append(f"candidate.{key}: missing")
    for k in ("prior_sealed_handoff_sha", "current_remote_control_sha"):
        if meaningful(identity.get(k)) and not HEX40.fullmatch(identity[k]):
            errors.append(f"candidate.{k}: not a full 40-character SHA")

    proofs = record.get("proof_sections") or {}
    for cat in sorted(REQUIRED_PROOFS):
        p = proofs.get(cat) or {}
        if p.get("status") != "PASS":
            errors.append(f"proof {cat}: not PASS")
        if not meaningful(p.get("substantive_conclusion")):
            errors.append(f"proof {cat}: no substantive conclusion")
        e = p.get("evidence")
        if not isinstance(e, list) or not e:
            errors.append(f"proof {cat}: no cited evidence")
        else:
            for i, row in enumerate(e):
                if not isinstance(row, dict) or any(not meaningful(row.get(k)) for k in
                                                    ("repository_path_or_source", "source_commit_or_sha",
                                                     "verified_fact", "currentness")):
                    errors.append(f"proof {cat}[{i}]: lacks exact source/evidence/currentness")

    # User-directed 2026-10-18: fail accession when only the latest return is
    # processed and no whole-machine, capacity-aware parallel flight is evidenced.
    # This is only a STRUCTURAL check; factual capacity, model sufficiency,
    # independence, and semantic authority still require competent review.
    flight = record.get("parallel_flight_board") or {}
    if flight.get("status") != "PASS":
        errors.append("parallel_flight_board: not PASS")
    lanes = flight.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("parallel_flight_board: no critical-path lanes")
        lanes = []
    if len(lanes) < 4 and not meaningful(flight.get("fewer_than_four_lanes_justification")):
        errors.append("parallel_flight_board: fewer than four candidate lanes without evidence")
    valid_states = {
        "READY_PARALLEL", "ACTIVE_VERIFIED", "PUBLISHED_NOT_LAUNCHED",
        "RETURNED_NEEDS_HQ_DECISION", "DEPENDENCY_HELD",
        "RESOURCE_HELD", "COMPLETED_SCOPED", "NOT_SELECTED",
    }
    selected_count = 0
    seen_lanes = set()
    for i, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            errors.append(f"parallel_flight_board.lanes[{i}]: not an object")
            continue
        lid = lane.get("lane_id")
        if not meaningful(lid) or lid in seen_lanes:
            errors.append(f"parallel_flight_board.lanes[{i}]: missing/duplicate lane_id")
        if isinstance(lid, str):
            seen_lanes.add(lid)
        if lane.get("parallel_status") not in valid_states:
            errors.append(f"parallel_flight_board.lanes[{i}]: invalid parallel_status")
        for key in (
            "terminal_persona_effect", "owner_and_target", "dependency_or_none_with_evidence",
            "model_recommended_or_none", "model_sufficiency_rationale", "execution_needs",
            "surface_choice", "editor_harness_status", "capacity_slot_or_unknown",
            "dispatch_decision",
        ):
            if not meaningful(lane.get(key)):
                errors.append(f"parallel_flight_board.lanes[{i}]: missing {key}")
        if lane.get("dispatch_decision") == "DISPATCH_NEW":
            selected_count += 1
    if selected_count == 1 and not meaningful(flight.get("one_commission_sequentialism_exception")):
        errors.append("parallel_flight_board: one new commission requires serialism/resource justification")
    for key in ("terminal_persona_chain_delta", "reviewer_independence_plan",
                "model_economy_evidence", "live_ref_timestamp"):
        if not meaningful(flight.get(key)):
            errors.append(f"parallel_flight_board: missing {key}")
    if flight.get("editor_harness_user_choice_respected") is not True:
        errors.append("parallel_flight_board: editor/harness user choice not attested")
    capacity = flight.get("capacity_matrix") or {}
    for slot in ("machine_A", "machine_B", "chatgpt_codex_account_A",
                 "chatgpt_codex_account_B", "opencode_account_A", "opencode_account_B"):
        entry = capacity.get(slot) or {}
        if entry.get("status") not in {"UNKNOWN", "LIVE_VERIFIED", "UNAVAILABLE", "STALE_RECHECK_REQUIRED", "RESOURCE_HELD"}:
            errors.append(f"parallel_flight_board.capacity_matrix.{slot}: invalid/missing status")

    # 2026-10-19 terminal-first accession safeguard. This is structural ONLY:
    # a competent HQ must judge scope, actual product maturity and owner permissions.
    # A filled field cannot by itself prove scientific validity or dispatch authority.
    terminal = record.get("terminal_artifact_continuity") or {}
    if terminal.get("status") != "PASS":
        errors.append("terminal_artifact_continuity: not PASS")
    for key in (
        "adopted_HQD125_HQD216_and_Astra_R3_read_ref",
        "missing_n11_artifacts_and_scope",
        "missing_n12_seam_artifacts_and_permissions",
        "estate_f1_f8_current_qualified_status",
        "largest_lawfully_completable_productive_tranche",
        "why_this_outcome_over_next_microtest",
        "real_original_or_generic_consumer_to_be_changed",
        "exact_source_issuer_actor_holds_and_parallel_work",
        "return_intake_terminal_delta_or_not_applicable",
        "verified_current_progress_pair_ref",
    ):
        if not meaningful(terminal.get(key)):
            errors.append(f"terminal_artifact_continuity.{key}: missing")
    scopes = terminal.get("candidate_new_commission_scopes")
    if not isinstance(scopes, list) or not scopes:
        errors.append("terminal_artifact_continuity: no named terminal completion campaign")
        scopes = []
    for i, scope in enumerate(scopes):
        if not isinstance(scope, dict):
            errors.append(f"terminal_artifact_continuity.scopes[{i}]: non-object")
            continue
        for key in (
            "parent_terminal_artifact", "current_missing_product",
            "largest_lawful_tranche", "actual_consumer", "inherited_current_owner",
            "independent_falsification", "terminal_hand_back",
            "small_job_exception_or_not_applicable",
        ):
            if not meaningful(scope.get(key)):
                errors.append(f"terminal_artifact_continuity.scopes[{i}].{key}: missing")

    got = set()
    for row in record.get("function_adjudications") or []:
        if not isinstance(row, dict):
            errors.append("function_adjudication: non-object row")
            continue
        name = row.get("function")
        if name in got:
            errors.append(f"duplicate function: {name}")
        got.add(name)
        if name not in REQUIRED_FUNCTIONS:
            continue
        for key in ("historical_ref", "current_owner_ref", "current_proof",
                    "alternatives_comparison", "persona_consumer",
                    "first_missing_edge", "positive_test"):
            if not meaningful(row.get(key)):
                errors.append(f"function {name}: missing {key} (use precise negative evidence if genuinely absent)")
        if row.get("functional_status") not in VALID_FUNCTIONAL_STATES:
            errors.append(f"function {name}: invalid functional state")
        if row.get("decision") not in VALID_DECISIONS or row.get("decision") == "NO_DECISION__NEEDS_EVIDENCE":
            errors.append(f"function {name}: no supported improvement/reuse adjudication")
    for absent in sorted(REQUIRED_FUNCTIONS - got):
        errors.append(f"missing required function: {absent}")

    e = record.get("end_product_evaluation") or {}
    for key in ("target_persona_scenario", "actual_source_inputs_and_claim_grades",
                "actual_accepted_or_pending_production_route", "actual_v3_v2_consumer",
                "observable_output_or_scoped_interface_test", "normal_control",
                "historical_or_material_counterfactual",
                "uncertainty_and_approximation_analysis",
                "required_approvals_and_missing_edges"):
        if not meaningful(e.get(key)):
            errors.append(f"end_product_evaluation.{key}: missing")

    review = record.get("independent_acceptance") or {}
    if review.get("status") != "ACCEPTED":
        errors.append("independent acceptance not recorded")
    if review.get("reviewer_type") not in {"USER", "AUTHORIZED_INDEPENDENT_REVIEWER"}:
        errors.append("independent acceptance: reviewer type invalid")
    for key in ("reviewer_identity_or_user_ack", "review_artifact_ref",
                "review_sha", "reviewed_candidate_sha"):
        if not meaningful(review.get(key)):
            errors.append(f"independent acceptance: missing {key}")
    if record.get("final_readiness") != "ACCESSION_REVIEW_ACCEPTED__OPERATIVE_CONTROL_STILL_SUBJECT_TO_EXISTING_HQD":
        errors.append("final readiness did not preserve original authority hierarchy")
    return errors

def main(argv):
    if len(argv) != 2:
        print("usage: verify_incoming_hq_grok_r1.py accession.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        errors = check(data)
    except (OSError, ValueError, TypeError) as exc:
        print(f"HQ_GROK_STRUCTURAL_CHECK_FAIL: {exc}", file=sys.stderr)
        return 2
    if errors:
        print(f"HQ_GROK_STRUCTURAL_CHECK_FAIL ({len(errors)} findings)")
        for e in errors[:150]:
            print(f"- {e}")
        return 1
    print("HQ_GROK_DOSSIER_STRUCTURALLY_COMPLETE")
    print("NOT AN HQ AUTHORIZATION. Verify source truth, reviewer consent, and governing HQD independently.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
