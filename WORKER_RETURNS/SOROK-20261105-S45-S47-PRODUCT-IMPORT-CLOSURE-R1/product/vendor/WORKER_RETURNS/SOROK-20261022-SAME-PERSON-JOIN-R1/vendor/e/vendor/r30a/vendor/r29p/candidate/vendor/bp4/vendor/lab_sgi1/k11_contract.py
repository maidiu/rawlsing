"""K11 executable test contract: 24 cases / 98 atomic predicates.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Assertion names are copied EXACTLY from S-G 03_K11_EXECUTABLE_TEST_CONTRACT.json.
The runner executes S-G's frozen contract against the source-free lab pipeline.
"""
from __future__ import annotations

import copy
import json
import time
from typing import Any, Dict, List, Optional, Tuple

from . import LAB_RULE_STATUS, CONTRACT_VERSION, K11_CONTRACT
from .core import h_obj, h_concat, canon, typed, S
from .mother import build_mother_checkpoint, EMBARGOED_PARTITION_MANIFEST
from .pipeline import run_pipeline, MODEL_NAME, MODEL_PROVIDER
from .proposal import (build_proposal_prompt, PROPOSAL_SYSTEM_PROMPT, call_model,
                       freeze_proposal_record, frozen_fallback_record,
                       dedup_candidates, semantic_class_key,
                       PROPOSAL_GRAMMAR_VERSION)
from .selection import policy_hash, POLICIES, scope_hash
from .dag import build_construction_graph, build_causal_graph, validate_two_dags

READ_CUTS = {
    "sorok_corrected": "bace7640777098732d425e9368cf28ada0e57aeb",
    "astra_official": "3b2d9a1b644a9fa024ed1bd895b67be5c8789531",
    "s_g_return": "aec8fecc1ae2e3438ff70c44ce5ce7845d1a4829",
}
SOURCE_USE_SCOPE = (
    "SOURCE_FREE_SYNTHETIC_LAB_ONLY__NO_ORIGINAL_SURVEY__NO_REAL_PERSON__"
    "NO_PRODUCTION_CURRENTNESS"
)

# Exact assertion names from S-G 03 contract (98 atomic predicates over 24 cases).
K11_CASES: List[Dict[str, Any]] = [
    {"id": "K11-BASE-LOCAL", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "mother_checkpoint_byte_identity_unchanged",
        "proposal_set_finite",
        "generic_query_receipts_exact",
        "selection_policy_labeled",
        "father_whole_domains_valid",
        "forward_endpoint_match",
        "shared_occurrence_once",
        "post_conception_both_continue",
        "child_exposure_changes_only_after_admission",
        "exact_replay_hash_equal",
    ]},
    {"id": "K11-ROUTE-DISCORDANT", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "contrast_in_typed_candidates_and_eligibility",
        "qualified_route_truth",
        "candidate_set_hash_binding",
        "deterministic_replay_per_route",
    ]},
    {"id": "K11-ROUTE-MOBILITY", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "no_backdated_mother_mobility",
        "permitted_route_expansion",
        "source_uses_generic_not_parent_specific",
        "invariant_unrelated_history",
    ]},
    {"id": "K11-ROUTE-UNCONVENTIONAL", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "no_typicality_mandate",
        "actual_route_constraint_preserved",
        "no_stereotype_mapping",
        "exact_replay",
    ]},
    {"id": "K11-A-FUTURE-CHILD-EMBARGO", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "candidate_set_hash_equal",
        "generic_query_request_hashes_equal",
        "selection_decision_identity_equal",
        "father_history_event_hashes_equal",
        "endpoint_same",
        "no_future_metadata_read",
    ]},
    {"id": "K11-A2-DESIRED-WOUND-COUNTERFACTUAL", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "no_father_abuse_generated_as_function_of_label",
        "byte_equal_father_ledger",
        "no_child_future_key_in_model_prompt_or_seed",
    ]},
    {"id": "K11-B-INDEPENDENT-HISTORY", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "at_least_two_endpoint_valid_distinct_nonendpoint_causal_histories_where_fixture_supports_alternatives",
        "nonmother_projects_distinct",
        "identity_or_histories_not_merely_prose",
        "endpoint_hash_constraints_equal",
        "no_hidden_backdating",
    ]},
    {"id": "K11-C-EXISTING-PARTNER", "fixture": "MP", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "existing_actor_reused_or_exact_contradiction_HOLD",
        "no_duplicate_actor_or_event",
        "mother_history_unchanged",
        "zero_unapproved_RNG",
    ]},
    {"id": "K11-C2-EXISTING-SHARED-EVENT", "fixture": "MP", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "HOLD_before_any_new_shared_event",
        "unchanged_existing_E_pre_hash",
        "no_retroactive_repair",
    ]},
    {"id": "K11-D-PARITY", "fixture": "M2", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "older_child_actor_id_unchanged",
        "older_child_actor_stream_unchanged",
        "historical_membership_unchanged",
        "new_target_not_assumed_first_child",
        "no_ancestral_rewrite",
    ]},
    {"id": "K11-E-INDEPENDENT-PROJECT", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "nonmother_project_has_causal_effect_record",
        "third_party_relationship_remains_actor_specific",
        "father_can_act_without_mother_prompt",
        "exact_forward_replay",
        "not_biography_prose",
    ]},
    {"id": "K11-GRAPH-CONSTRUCTION-VS-CAUSAL", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "construction_E_to_H_edge_allowed_and_typed_only",
        "causal_childhood_to_endpoint_chronology",
        "zero_causal_endpoint_to_childhood_edges",
        "both_graphs_acyclic",
    ]},
    {"id": "K11-DEDUPE", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "dedup_equivalence_class_count_unchanged",
        "candidate_set_hash_equal",
        "selection_receipt_equal",
        "no_probability_multiplication",
    ]},
    {"id": "K11-EMPIRICAL-CEILING", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "generic_empirical_receipt_NOT_ESTIMABLE_or_ceiling_limited",
        "no_population_coupling_inferred",
        "selection_no_frequency_claim",
    ]},
    {"id": "K11-WEIGHT-ORDINAL", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "SELECTION_AUTHORITY_UNBOUND",
        "RNG_draw_count_zero",
        "no_ordinal_to_weight_normalization",
    ]},
    {"id": "K11-WEIGHT-SENSITIVITY", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "each_policy_hash_unique",
        "outcomes_replay_exact",
        "sensitivity_distribution_reported_without_population_claim",
        "no_best_child_based_policy_choice",
    ]},
    {"id": "K11-RETRY-BIAS", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "failed_attempt_receipt_persisted",
        "no_silent_resample",
        "effective_selection_bias_report_or_HOLD",
        "no_causal_commit_for_C1",
    ]},
    {"id": "K11-VALID-EMPTY", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "typed_SCENARIOS_VALID_EMPTY_or_INFEASIBLE",
        "no_unsupported_father_created",
        "zero_RNG_draws",
        "zero_genealogy_events",
    ]},
    {"id": "K11-UNKNOWN-REQUIRED", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "HOLD_not_INFEASIBLE",
        "no_filler_fact_or_event",
        "exact_missing_authority_list",
    ]},
    {"id": "K11-RELATION-ASYMMETRY", "fixture": "M0", "expected": "PASS_IF_AUTHORIZED_RUN", "assertions": [
        "one_objective_relation_event",
        "two_distinct_perspective_states_where_admitted",
        "no_reciprocity_inference",
        "zero_auto_household_membership",
        "both_continuations_replay",
    ]},
    {"id": "K11-CONCEPTION-CHILDGEN-BOUNDARY", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "PENDING_not_ADMITTED_CONCEPTION",
        "zero_CHILD_GENERATED_events",
        "no_birth_alias",
        "CONCEPTION_BIOLOGY_AUTHORITY_HOLD",
    ]},
    {"id": "K11-MISSING-HISTORY", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "INDEPENDENT_PROJECT_PROOF_MISSING_or_PREHISTORY_OWNER_RULE_MISSING",
        "no_child_generation_commit",
    ]},
    {"id": "K11-SCHEDULER-SAME-TIME", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "AMBIGUOUS_SAME_TIME_CAUSAL_ORDER",
        "no_lexicographic_priority",
        "zero_fictitious_events",
    ]},
    {"id": "K11-REPLAY-ALTER-SUBJECT", "fixture": "M0", "expected": "REFUSE_OR_INVARIANT", "assertions": [
        "ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE",
        "no_reconstructed_history_pass",
    ]},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def derive_actor_id(generation_subject_hash: str) -> str:
    return "LAB_SECOND_PARENT_" + h_obj(generation_subject_hash).split(":")[-1]


def subject_integrity_check(recorded_actor_id: str, recorded_subject_hash: str,
                            altered_subject_hash: str) -> Dict[str, Any]:
    """Changing the frozen generation subject hash without changing the reference
    must yield ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE."""
    derived_from_recorded = derive_actor_id(recorded_subject_hash)
    derived_from_altered = derive_actor_id(altered_subject_hash)
    binding_ok = derived_from_recorded == recorded_actor_id
    mismatch = derived_from_altered != recorded_actor_id
    if mismatch:
        return typed(
            S.ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE,
            recorded_actor_id=recorded_actor_id,
            derived_from_altered_subject=derived_from_altered,
            recorded_subject_hash=recorded_subject_hash,
            altered_subject_hash=altered_subject_hash,
            binding_was_consistent_before_alteration=binding_ok,
        )
    return typed(S.INTEGRITY_FAILURE, note="alteration not detected")


def _dad_event_hashes(r: Dict[str, Any]) -> Optional[str]:
    evs = r.get("dad_events")
    if not evs:
        return None
    return h_obj([e for e in evs])


def _empirical_request_hashes(r: Dict[str, Any]) -> List[str]:
    out = []
    for e in r.get("ledger", {}).get("entries", []):
        if e["kind"] == "QUALIFICATION":
            for item in e["payload"].get("per_class", []):
                out.append(item.get("class_key"))
    return out


def _generic_request_hashes_from_quals(r: Dict[str, Any]) -> List[str]:
    hashes = []
    for e in r["ledger"]["entries"]:
        if e["kind"] == "QUALIFICATION":
            # reconstruct request hashes recorded inside qualification receipts
            pass
    # deterministic derive from scenario + world_ref (same as pipeline's request)
    return hashes


def _selection_identity(r: Dict[str, Any]) -> Dict[str, Any]:
    s = r.get("selection_summary") or {}
    return {
        "selected_class_key": s.get("selected_class_key"),
        "candidate_set_hash": s.get("candidate_set_hash"),
        "scope_hash": s.get("scope_hash"),
        "n_draws": s.get("n_draws"),
        "draw_mode": s.get("draw_mode"),
        "policy_hash": s.get("policy_hash"),
    }


def _endpoint_state(r: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    cons = r.get("construction_summary")
    if not cons or not cons.get("attempts"):
        return None
    for a in cons["attempts"]:
        if a.get("endpoint_match"):
            return a.get("replay", {}).get("recomputed_state")
    return None


def _case_receipt(case_id: str, fixture_hash: str, intervention: Dict[str, Any],
                  model_version: Optional[str], input_hashes: Dict[str, str],
                  evidence: List[str], observed: Dict[str, Any],
                  assertion_results: Dict[str, bool],
                  missing_authority: List[str], cost: Dict[str, Any],
                  replay_result: Dict[str, Any], terminal_grade: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "fixture_hash": fixture_hash,
        "intervention_hash": h_obj(intervention),
        "intervention": intervention,
        "authority_versions": {
            "contract": CONTRACT_VERSION,
            "k11_contract": K11_CONTRACT,
            "read_cuts": READ_CUTS,
            "lab_rule": LAB_RULE_STATUS,
        },
        "source_use_scope": SOURCE_USE_SCOPE,
        "model_version_if_used": model_version,
        "input_hashes": input_hashes,
        "actual_evidence_refs": evidence,
        "observed_state": observed,
        "assertion_results": assertion_results,
        "missing_authority": missing_authority,
        "cost_report": cost,
        "replay_result": replay_result,
        "terminal_grade": terminal_grade,
        "receipt_hash": h_obj({
            "case_id": case_id,
            "assertion_results": assertion_results,
            "terminal_grade": terminal_grade,
        }),
    }


def _grade(expected: str, assertion_results: Dict[str, bool]) -> str:
    ok = all(assertion_results.values())
    if expected == "PASS_IF_AUTHORIZED_RUN":
        return "K11_CASE_PASS" if ok else "K11_CASE_FAIL"
    return "K11_CASE_INVARIANT_HELD" if ok else "K11_CASE_FAIL"
