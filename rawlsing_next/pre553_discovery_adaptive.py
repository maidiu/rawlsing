"""PRE553 I08 adaptive exploratory discovery; exact results, nonexhaustive coverage."""
from __future__ import annotations

from typing import Iterable, Mapping, Any

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority, EmpiricalPredicate, EmpiricalQuerySpec, ExactRef, canonicalize, exact_ref
from rawlsing_next.pre553_discovery_exact import (
    ExactBoundedDiscoveryResult, _canonical_refs, _catalog_atoms, _catalog_templates,
    _compile_frontier, _derived_ref, _evaluate_candidate, _mapping, _validate_catalog_scope,
)
from rawlsing_next._pre553_discovery_adaptive_contract import (
    I08_CONTRACT_ID, I08_COVERAGE_CLAIM, I08_EXEC_SCHEMA, I05_ACCEPTED_PARENT_HEAD,
    AdaptiveCoverageError, AdaptiveExploratoryDiscoveryError, AdaptiveExploratoryDiscoveryResult,
    adaptive_execution_contract_material, exact_int, make_adaptive_execution_contract_ref,
    verify_adaptive_authority,
)
from rawlsing_next._pre553_discovery_adaptive_exec import (
    choose_next, frontier_ref, i05_binding, make_receipt, prune_reason, validate_diagnostics,
)


def execute_adaptive_exploratory_discovery(*, repository, discovery_authority: DiscoveryAuthority,
        authority_registry: AuthorityRegistry, release_refs: Iterable[ExactRef],
        predicate_catalog: Iterable[EmpiricalPredicate], query_template_catalog: Iterable[EmpiricalQuerySpec],
        diagnostic_values: Mapping[str, Mapping[str, Any]] | None = None,
        accepted_i05_result: ExactBoundedDiscoveryResult | None = None):
    if not isinstance(authority_registry, AuthorityRegistry):
        raise AdaptiveExploratoryDiscoveryError("exact AuthorityRegistry required")
    i05_before = i05_binding(accepted_i05_result)
    definition, proposal, budget, stopping, pruning, permitted, execution_ref = verify_adaptive_authority(discovery_authority, authority_registry)
    atoms = _catalog_atoms(definition, predicate_catalog)
    templates = _catalog_templates(definition, query_template_catalog)
    _validate_catalog_scope(discovery_authority, atoms, templates)
    candidates = _compile_frontier(definition, atoms, templates)
    allowed_validation = set(_mapping(discovery_authority.validation_rules, "validation_rules").get("kinds", ()))
    if {candidate.validation["kind"] for candidate in candidates} - allowed_validation:
        raise Pre553AuthorityError("adaptive validation exceeds authority")
    grammar_ref = exact_ref(discovery_authority.candidate_grammar_ref)
    frontier = frontier_ref(discovery_authority, candidates)
    diagnostics = validate_diagnostics(diagnostic_values, candidates, permitted)
    if proposal["strategy"] == "DIAGNOSTIC_PRIORITY" and any(
        proposal["diagnostic_kind"] not in diagnostics.get(candidate.candidate_hash, {}) for candidate in candidates
    ):
        raise AdaptiveExploratoryDiscoveryError("diagnostic-priority requires value for every frontier candidate")

    pruned, remaining = {}, []
    for candidate in candidates:
        reason = prune_reason(candidate, pruning)
        if reason:
            pruned[candidate.candidate_hash] = reason
        else:
            remaining.append(candidate)
    max_candidates = budget["max_evaluated_candidates"]
    max_queries = budget["max_query_executions"]
    minimum_n = exact_int(_mapping(discovery_authority.support_rules, "support_rules").get("minimum_raw_denominator", 1), "minimum_raw_denominator")
    releases = _canonical_refs(exact_ref(ref, "release_ref") for ref in release_refs)
    if not releases:
        raise AdaptiveExploratoryDiscoveryError("exact C11 release required")

    evaluated, trace = {}, []
    used_queries = supported_count = 0
    supported_families = {}
    stop_reason = "FRONTIER_EXHAUSTED"
    while remaining:
        if len(evaluated) >= max_candidates:
            stop_reason = "BUDGET_EXHAUSTED"
            break
        candidate = choose_next(remaining, proposal, discovery_authority.rng_policy_if_any, diagnostics, supported_families)
        cost = len(candidate.query_roles)
        if used_queries + cost > max_queries:
            stop_reason = "BUDGET_EXHAUSTED"
            break
        remaining.remove(candidate)
        trace.append(candidate.candidate_hash)
        exact_state, typed_state, facts, support = _evaluate_candidate(
            candidate, repository=repository, registry=authority_registry,
            release_refs=releases, minimum_raw_denominator=minimum_n,
        )
        support = dict(canonicalize(support))
        support["exact_i05_candidate_coverage_state"] = exact_state
        support["proposal_diagnostics_nonauthoritative"] = canonicalize(diagnostics.get(candidate.candidate_hash, {}))
        evaluated[candidate.candidate_hash] = make_receipt(
            discovery_authority, grammar_ref, frontier, execution_ref, candidate,
            "EVALUATED", typed_state, facts=facts, support=support,
            diagnostics=diagnostics.get(candidate.candidate_hash),
        )
        used_queries += cost
        if typed_state == "DISCOVERED_RESULT_SUPPORTED":
            supported_count += 1
            supported_families[candidate.family] = supported_families.get(candidate.family, 0) + 1
        if stopping["kind"] == "STOP_AFTER_SUPPORTED_COUNT" and supported_count >= stopping["supported_count"]:
            stop_reason = "STOPPING_RULE_REACHED"
            break

    unevaluated_reason = "BUDGET_EXHAUSTED" if stop_reason == "BUDGET_EXHAUSTED" else "STOPPING_RULE_REACHED" if stop_reason == "STOPPING_RULE_REACHED" else "NOT_REACHED_BY_TRAVERSAL"
    receipts = []
    for candidate in candidates:
        if candidate.candidate_hash in evaluated:
            receipts.append(evaluated[candidate.candidate_hash])
        elif candidate.candidate_hash in pruned:
            receipts.append(make_receipt(
                discovery_authority, grammar_ref, frontier, execution_ref, candidate,
                "PRUNED", "PRUNED_BY_AUTHORITY", reason={
                    "candidate_id_or_deterministic_candidate_set_descriptor": candidate.candidate_id,
                    "prune_rule_ref": pruning.get("prune_rule_ref"),
                    "prune_reason_code": pruned[candidate.candidate_hash],
                    "prune_class": "HEURISTIC", "proposal_state_at_prune": "PRETRAVERSAL",
                    "safe_theorem_ref_or_null": None, "negative_evidence": False,
                },
            ))
        else:
            receipts.append(make_receipt(
                discovery_authority, grammar_ref, frontier, execution_ref, candidate,
                "UNEVALUATED", "UNEVALUATED", reason={
                    "candidate_id_or_deterministic_remaining_set_descriptor": candidate.candidate_id,
                    "unevaluated_reason": unevaluated_reason,
                    "frontier_membership_proof_or_replay_rule": frontier.as_dict(),
                    "negative_evidence": False, "semantic_absence": False,
                },
            ))
    receipts = tuple(sorted(receipts, key=lambda receipt: receipt.ref.key))
    evaluated_count = sum(r.coverage_state == "EVALUATED" for r in receipts)
    pruned_count = sum(r.coverage_state == "PRUNED" for r in receipts)
    unevaluated_count = sum(r.coverage_state == "UNEVALUATED" for r in receipts)
    if len(candidates) != evaluated_count + pruned_count + unevaluated_count:
        raise AdaptiveCoverageError("candidate partition incomplete")
    budget_receipt = canonicalize({
        "max_evaluated_candidates": max_candidates, "evaluated_candidates_used": evaluated_count,
        "max_query_executions": max_queries, "query_executions_used": used_queries,
        "supported_results": supported_count, "stopping_reason": stop_reason,
    })
    coverage_material = {
        "contract": I08_CONTRACT_ID, "authority_ref": discovery_authority.ref.as_dict(),
        "frontier_ref": frontier.as_dict(), "execution_ref": execution_ref.as_dict(),
        "counts": [len(candidates), evaluated_count, pruned_count, unevaluated_count],
        "trace": trace, "stop": stop_reason, "budget": budget_receipt,
        "receipt_refs": [receipt.ref.as_dict() for receipt in receipts], "i05": i05_before,
    }
    coverage_ref = _derived_ref("PRE553_I08_ADAPTIVE_COVERAGE_RECEIPT", "adaptive-coverage", coverage_material)
    replay_ref = _derived_ref("PRE553_I08_ADAPTIVE_REPLAY", "adaptive-replay", {
        **coverage_material, "coverage_ref": coverage_ref.as_dict(),
        "diagnostics_nonauthoritative": canonicalize(diagnostics),
    })
    if i05_binding(accepted_i05_result) != i05_before:
        raise AdaptiveCoverageError("accepted I05 result mutated")
    evaluated_receipts = [receipt for receipt in receipts if receipt.coverage_state == "EVALUATED"]
    return AdaptiveExploratoryDiscoveryResult(
        I08_CONTRACT_ID, discovery_authority.ref, grammar_ref, frontier, coverage_ref,
        I08_COVERAGE_CLAIM, len(candidates), evaluated_count, pruned_count, unevaluated_count,
        receipts, tuple(trace), stop_reason, budget_receipt,
        bool(evaluated_receipts) and all(receipt.typed_state == "VALID_EMPTY" for receipt in evaluated_receipts),
        not candidates, I05_ACCEPTED_PARENT_HEAD, replay_ref,
    )


__all__ = [
    "I08_CONTRACT_ID", "I08_COVERAGE_CLAIM", "I08_EXEC_SCHEMA", "I05_ACCEPTED_PARENT_HEAD",
    "AdaptiveExploratoryDiscoveryError", "AdaptiveCoverageError", "AdaptiveExploratoryDiscoveryResult",
    "adaptive_execution_contract_material", "make_adaptive_execution_contract_ref",
    "execute_adaptive_exploratory_discovery",
]
