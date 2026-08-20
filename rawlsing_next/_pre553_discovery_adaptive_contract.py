from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError, validate_object_authority_closure
from rawlsing_next.pre553_empirical_objects import (
    DIAGNOSTIC_ONLY_KINDS, DiscoveryAuthority, DiscoveryResultReceipt, ExactRef,
    Pre553IntegrityError, Pre553SemanticCollapseError, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_discovery_exact import CANDIDATE_GRAMMAR_SCHEMA, _mapping, _text, _verify_object_identity

I08_CONTRACT_ID = "PRE553_I08_ADAPTIVE_EXPLORATORY_DISCOVERY@1.0.0"
I08_COVERAGE_CLAIM = "EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE"
I08_EXEC_SCHEMA = "PRE553_I08_ADAPTIVE_EXECUTION_CONTRACT@1.0.0"
I05_ACCEPTED_PARENT_HEAD = "6a75433b9a12b66e75f1def97f69163587970fd1"
STRATEGY_TIE = {
    "CANONICAL_CANDIDATE_HASH_ORDER": "CANONICAL_CANDIDATE_HASH_ORDER",
    "SEEDED_HASH_ORDER": "SEEDED_HASH_THEN_CANDIDATE_HASH",
    "STATE_FEEDBACK_PRIORITY": "STATE_FEEDBACK_THEN_SEEDED_HASH_THEN_CANDIDATE_HASH",
    "DIAGNOSTIC_PRIORITY": "DIAGNOSTIC_EXACT_VALUE_THEN_CANDIDATE_HASH",
}


class AdaptiveExploratoryDiscoveryError(Pre553IntegrityError):
    pass


class AdaptiveCoverageError(AdaptiveExploratoryDiscoveryError):
    pass


@dataclass(frozen=True)
class AdaptiveExploratoryDiscoveryResult:
    contract_id: str
    discovery_authority_ref: ExactRef
    candidate_grammar_ref: ExactRef
    authorized_frontier_ref: ExactRef
    adaptive_coverage_ref: ExactRef
    coverage_claim: str
    frontier_candidate_count: int
    evaluated_count: int
    pruned_count: int
    unevaluated_count: int
    receipts: tuple[DiscoveryResultReceipt, ...]
    proposal_trace: tuple[str, ...]
    stopping_reason: str
    budget_accounting: Mapping[str, Any]
    evaluated_valid_empty: bool
    authorized_frontier_empty: bool
    accepted_i05_parent_head: str
    replay_ref: ExactRef

    def __post_init__(self):
        if self.contract_id != I08_CONTRACT_ID or self.coverage_claim != I08_COVERAGE_CLAIM:
            raise AdaptiveCoverageError("I08 contract/coverage mismatch")
        if self.accepted_i05_parent_head != I05_ACCEPTED_PARENT_HEAD:
            raise AdaptiveCoverageError("accepted I05 parent drift")
        if self.frontier_candidate_count != self.evaluated_count + self.pruned_count + self.unevaluated_count:
            raise AdaptiveCoverageError("EVALUATED+PRUNED+UNEVALUATED must partition F")
        if len(self.receipts) != self.frontier_candidate_count:
            raise AdaptiveCoverageError("one receipt per frontier candidate required")
        if tuple(sorted(self.receipts, key=lambda r: r.ref.key)) != self.receipts:
            raise AdaptiveCoverageError("receipts not canonical")


def seq(value, name, allow_empty=False):
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence) or (not allow_empty and not value):
        raise AdaptiveExploratoryDiscoveryError(f"{name} must be a sequence")
    return value


def exact_int(value, name, minimum=0):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise AdaptiveExploratoryDiscoveryError(f"{name} must be integer >= {minimum}")
    return value


def exact_number(value, name):
    if isinstance(value, bool):
        raise AdaptiveExploratoryDiscoveryError(f"{name} not exact numeric")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except Exception as exc:
            raise AdaptiveExploratoryDiscoveryError(f"{name} not exact numeric") from exc
    if isinstance(value, Mapping) and set(value) == {"$exact_fraction"}:
        pair = value["$exact_fraction"]
        if isinstance(pair, Sequence) and len(pair) == 2 and all(isinstance(x, int) and not isinstance(x, bool) for x in pair):
            return Fraction(pair[0], pair[1])
    if isinstance(value, Mapping) and set(value) == {"$exact_decimal"} and isinstance(value["$exact_decimal"], str):
        return Fraction(value["$exact_decimal"])
    raise AdaptiveExploratoryDiscoveryError(f"{name} not exact numeric")


def adaptive_execution_contract_material(*, proposal_contract, budget_contract, stopping_rule,
        pruning_contract, rng_policy_if_any, validation_partition_contract,
        permissible_diagnostics, tie_order_rules, algorithm_identity):
    return canonicalize({
        "schema": I08_EXEC_SCHEMA,
        "proposal_contract": proposal_contract,
        "budget_contract": budget_contract,
        "stopping_rule": stopping_rule,
        "pruning_contract": pruning_contract,
        "rng_policy_if_any": rng_policy_if_any,
        "validation_partition_contract": validation_partition_contract,
        "permissible_diagnostics": list(permissible_diagnostics),
        "tie_order_rules": tie_order_rules,
        "algorithm_identity": algorithm_identity,
    })


def make_adaptive_execution_contract_ref(**kwargs):
    digest = semantic_hash(adaptive_execution_contract_material(**kwargs))
    return ExactRef(
        "PRE553_I08_ADAPTIVE_EXECUTION_CONTRACT",
        f"urn:rawlsing:pre553:i08:adaptive-execution-contract:sha256:{digest}",
        digest,
    )


def verify_adaptive_authority(authority: DiscoveryAuthority, registry: AuthorityRegistry):
    _verify_object_identity(authority, DiscoveryAuthority, "discovery_authority")
    if authority.typed_state != "ADAPTIVE_EXPLORATORY_AUTHORIZED" or authority.coverage_claim != I08_COVERAGE_CLAIM:
        raise AdaptiveCoverageError("adaptive authority state/coverage mismatch")
    if authority.semantic_fields.get("mode", "ADAPTIVE_EXPLORATORY") != "ADAPTIVE_EXPLORATORY":
        raise AdaptiveExploratoryDiscoveryError("adaptive mode mismatch")
    validate_object_authority_closure(authority, registry)
    definition = _mapping(authority.candidate_universe_definition, "candidate_universe_definition")
    if definition.get("schema") != CANDIDATE_GRAMMAR_SCHEMA:
        raise AdaptiveExploratoryDiscoveryError("I08 must use accepted I05 candidate grammar")
    grammar_ref = exact_ref(authority.candidate_grammar_ref, "candidate_grammar_ref")
    if grammar_ref.content_hash != semantic_hash(definition):
        raise AdaptiveExploratoryDiscoveryError("candidate grammar hash mismatch")
    operation = _text(definition.get("discovery_operation"), "discovery_operation")
    authorized = False
    for ref in authority.authority_snapshot_refs:
        snapshot = registry.resolve_exact(ref).snapshot
        if snapshot.authority_kind == "DISCOVERY_FRONTIER":
            for family in ("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"):
                registry.require(ref, authority_kind="DISCOVERY_FRONTIER", operation=operation, object_family=family)
            authorized = True
    if not authorized:
        raise Pre553AuthorityError("exact DISCOVERY_FRONTIER authority required")
    if authority.algorithm_identity_if_semantically_required != I08_CONTRACT_ID:
        raise AdaptiveExploratoryDiscoveryError("I08 algorithm identity not pinned")

    proposal = _mapping(authority.semantic_fields.get("proposal_contract"), "proposal_contract")
    budget = _mapping(authority.semantic_fields.get("budget_contract"), "budget_contract")
    stopping = _mapping(authority.semantic_fields.get("stopping_rule"), "stopping_rule")
    pruning = _mapping(authority.pruning_contract, "pruning_contract")
    validation = _mapping(authority.semantic_fields.get("validation_partition_contract"), "validation_partition_contract")
    diagnostics = tuple(_text(x, "diagnostic") for x in seq(authority.semantic_fields.get("permissible_diagnostics", ()), "permissible_diagnostics", True))
    strategy = proposal.get("strategy")
    if strategy not in STRATEGY_TIE or authority.tie_order_rules != STRATEGY_TIE[strategy]:
        raise AdaptiveExploratoryDiscoveryError("proposal strategy/tie-order mismatch")
    if proposal.get("allows_new_candidates_from_diagnostics") not in (None, False):
        raise Pre553SemanticCollapseError("diagnostics may not widen semantic candidate frontier")
    if any(kind not in DIAGNOSTIC_ONLY_KINDS for kind in diagnostics):
        raise Pre553SemanticCollapseError("invalid proposal diagnostic")
    if stopping.get("kind") not in {"EXHAUST_OR_BUDGET", "STOP_AFTER_SUPPORTED_COUNT"}:
        raise AdaptiveExploratoryDiscoveryError("bad stopping rule")
    if pruning.get("kind") not in {"NONE", "STATIC_RULE_ID_PRUNE", "STATIC_FAMILY_PRUNE"}:
        raise AdaptiveExploratoryDiscoveryError("bad pruning rule")
    if validation.get("kind") != "NONE__EXACT_I03_I05_VALIDATION":
        raise AdaptiveExploratoryDiscoveryError("holdout requires separate authority")
    exact_int(budget.get("max_evaluated_candidates"), "max_evaluated_candidates")
    exact_int(budget.get("max_query_executions"), "max_query_executions")
    if stopping["kind"] == "STOP_AFTER_SUPPORTED_COUNT":
        exact_int(stopping.get("supported_count"), "supported_count", 1)
    rng = authority.rng_policy_if_any
    if strategy in {"SEEDED_HASH_ORDER", "STATE_FEEDBACK_PRIORITY"}:
        rng_map = _mapping(rng, "rng_policy_if_any")
        if rng_map.get("kind") != "DETERMINISTIC_SEEDED_HASH":
            raise AdaptiveExploratoryDiscoveryError("seeded strategy requires deterministic seeded hash")
        _text(rng_map.get("seed"), "seed")
    elif rng not in (None, "NONE", {"kind": "NONE"}):
        raise AdaptiveExploratoryDiscoveryError("unexpected RNG state")
    if strategy == "DIAGNOSTIC_PRIORITY":
        kind = _text(proposal.get("diagnostic_kind"), "diagnostic_kind")
        if kind not in diagnostics or proposal.get("direction") not in {"HIGH_FIRST", "LOW_FIRST"}:
            raise Pre553SemanticCollapseError("diagnostic proposal not exactly authorized")
    execution_ref = exact_ref(authority.semantic_fields.get("adaptive_execution_contract_ref"), "adaptive_execution_contract_ref")
    expected = make_adaptive_execution_contract_ref(
        proposal_contract=proposal, budget_contract=budget, stopping_rule=stopping,
        pruning_contract=pruning, rng_policy_if_any=rng,
        validation_partition_contract=validation, permissible_diagnostics=diagnostics,
        tie_order_rules=authority.tie_order_rules,
        algorithm_identity=authority.algorithm_identity_if_semantically_required,
    )
    if execution_ref != expected:
        raise AdaptiveExploratoryDiscoveryError("adaptive execution contract hash mismatch")
    return definition, proposal, budget, stopping, pruning, diagnostics, execution_ref
