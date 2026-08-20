from __future__ import annotations

from typing import Mapping

from rawlsing_next.pre553_empirical_objects import DiscoveryResultReceipt, Pre553SemanticCollapseError, canonicalize, semantic_hash
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID, ExactBoundedDiscoveryResult, _canonical_auths, _canonical_refs,
    _derived_ref, _mapping,
)
from rawlsing_next._pre553_discovery_adaptive_contract import (
    I08_CONTRACT_ID, I08_COVERAGE_CLAIM, I05_ACCEPTED_PARENT_HEAD,
    AdaptiveCoverageError, AdaptiveExploratoryDiscoveryError, exact_int, exact_number,
)


def frontier_ref(authority, candidates):
    return _derived_ref("PRE553_I08_AUTHORIZED_FRONTIER", "authorized-frontier", {
        "contract": I08_CONTRACT_ID, "authority_ref": authority.ref.as_dict(),
        "candidate_grammar_ref": canonicalize(authority.candidate_grammar_ref),
        "candidates": [{"candidate_id": c.candidate_id, "candidate_hash": c.candidate_hash} for c in candidates],
        "coverage": I08_COVERAGE_CLAIM,
    })


def validate_diagnostics(values, candidates, allowed):
    if values is None:
        return {}
    if not isinstance(values, Mapping):
        raise AdaptiveExploratoryDiscoveryError("diagnostic_values must be mapping")
    hashes = {c.candidate_hash for c in candidates}
    if set(values) - hashes:
        raise Pre553SemanticCollapseError("out-of-frontier diagnostic candidate")
    out = {}
    for candidate_hash, raw in values.items():
        if not isinstance(raw, Mapping) or set(raw) - set(allowed):
            raise Pre553SemanticCollapseError("diagnostic kind not authorized")
        out[candidate_hash] = {kind: exact_number(value, kind) for kind, value in raw.items()}
    return out


def prune_reason(candidate, pruning):
    kind = pruning["kind"]
    if kind == "NONE":
        return None
    if kind == "STATIC_RULE_ID_PRUNE" and candidate.rule_id in set(pruning.get("rule_ids", ())):
        return "STATIC_RULE_ID_PRUNE"
    if kind == "STATIC_FAMILY_PRUNE" and candidate.family in set(pruning.get("families", ())):
        return "STATIC_FAMILY_PRUNE"
    return None


def choose_next(remaining, proposal, rng, diagnostics, supported_families):
    strategy = proposal["strategy"]
    if strategy == "CANONICAL_CANDIDATE_HASH_ORDER":
        return min(remaining, key=lambda c: c.candidate_hash)
    if strategy in {"SEEDED_HASH_ORDER", "STATE_FEEDBACK_PRIORITY"}:
        seed = _mapping(rng, "rng")["seed"]
        tie = lambda c: semantic_hash({"seed": seed, "candidate_hash": c.candidate_hash})
        if strategy == "SEEDED_HASH_ORDER":
            return min(remaining, key=lambda c: (tie(c), c.candidate_hash))
        bonus = exact_int(proposal.get("supported_family_bonus", 1), "supported_family_bonus")
        return min(remaining, key=lambda c: (
            -(supported_families.get(c.family, 0) * bonus), tie(c), c.candidate_hash,
        ))
    kind = proposal["diagnostic_kind"]
    high_first = proposal["direction"] == "HIGH_FIRST"
    return min(remaining, key=lambda c: (
        (-1 if high_first else 1) * diagnostics[c.candidate_hash][kind], c.candidate_hash,
    ))


def candidate_identity(candidate):
    return canonicalize({
        "candidate_id": candidate.candidate_id,
        "candidate_hash": candidate.candidate_hash,
        "family": candidate.family,
        "rule_id": candidate.rule_id,
        "validation": candidate.validation,
        "query_roles": [
            {"role": role.role, "predicate_ref": role.predicate.ref, "query_ref": role.query.ref}
            for role in candidate.query_roles
        ],
    })


def make_receipt(authority, grammar_ref, frontier, execution_ref, candidate, state, typed,
        *, facts=(), support=None, reason=None, diagnostics=None):
    fact_refs = _canonical_refs(f.ref for f in facts)
    replay = _derived_ref("PRE553_I08_CANDIDATE_REPLAY", "candidate-replay", {
        "authority": authority.ref.as_dict(), "frontier": frontier.as_dict(),
        "execution": execution_ref.as_dict(), "candidate": candidate_identity(candidate),
        "state": state, "typed": typed, "facts": [ref.as_dict() for ref in fact_refs],
        "reason": reason, "diagnostics": canonicalize(diagnostics or {}),
    })
    auths = _canonical_auths([*authority.authority_snapshot_refs, *(ref for fact in facts for ref in fact.authority_snapshot_refs)])
    return DiscoveryResultReceipt(
        typed_state=typed,
        authority_snapshot_refs=auths,
        dependency_refs=_canonical_refs([authority.ref, grammar_ref, frontier, execution_ref, candidate.winning_predicate.ref, *fact_refs]),
        producer_replay_locator_or_reference_root=replay,
        discovery_authority_ref=authority.ref,
        candidate_identity=candidate_identity(candidate),
        winning_predicate_ref=candidate.winning_predicate.ref,
        empirical_fact_refs=fact_refs,
        validation_fact_refs=fact_refs,
        coverage_state=state,
        evaluated_frontier_ref=frontier,
        branch_or_parent_ancestry_refs=candidate.ancestry_refs,
        support_uncertainty_state=canonicalize(support or reason or {}),
        replay_ref=replay,
        adaptive_execution_contract_ref=execution_ref,
        negative_evidence=(False if state != "EVALUATED" else "CANDIDATE_SPECIFIC_TYPED_ONLY"),
        semantic_absence=(False if state != "EVALUATED" else None),
        diagnostic_score_is_empirical_fact=False,
        structural_truth_effect=False,
        actor_v3_effect=False,
    )


def i05_binding(value):
    if value is None:
        return {"head": I05_ACCEPTED_PARENT_HEAD, "runtime_result_supplied": False}
    if not isinstance(value, ExactBoundedDiscoveryResult) or value.contract_id != I05_CONTRACT_ID or value.coverage_claim != "COMPLETE_FOR_EXACT_DECLARED_FRONTIER":
        raise AdaptiveCoverageError("supplied I05 result is not accepted exact-frontier class")
    return {
        "head": I05_ACCEPTED_PARENT_HEAD,
        "runtime_result_supplied": True,
        "frontier_ref": value.evaluated_frontier_ref.as_dict(),
        "replay_ref": value.replay_ref.as_dict(),
        "candidate_count": value.candidate_count,
        "covered_count": value.covered_candidate_count,
    }
