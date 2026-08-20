import pytest

from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import Pre553SemanticCollapseError
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_discovery_adaptive import (
    I05_ACCEPTED_PARENT_HEAD, I08_COVERAGE_CLAIM, AdaptiveExploratoryDiscoveryError,
    execute_adaptive_exploratory_discovery,
)
from rawlsing_next.tests._pre553_discovery_adaptive_test_support import (
    _adaptive_authority, _exact_authority, _fixture, _ref, _run,
)

def test_deterministic_replay_exact_authority_and_config():
    fx = _fixture("replay")
    authority = _adaptive_authority(fx)
    first = _run(fx, authority)
    second = _run(fx, authority)
    assert first.replay_ref == second.replay_ref
    assert first.adaptive_coverage_ref == second.adaptive_coverage_ref
    assert first.proposal_trace == second.proposal_trace
    assert tuple(r.ref for r in first.receipts) == tuple(r.ref for r in second.receipts)
    assert first.frontier_candidate_count == 2 == first.evaluated_count
    assert first.pruned_count == first.unevaluated_count == 0


def test_budget_exhaustion_partitions_remaining_candidates_as_unevaluated():
    fx = _fixture("budget")
    authority = _adaptive_authority(fx, max_candidates=1)
    result = _run(fx, authority)
    assert result.stopping_reason == "BUDGET_EXHAUSTED"
    assert (result.evaluated_count, result.pruned_count, result.unevaluated_count) == (1, 0, 1)
    unevaluated = [r for r in result.receipts if r.coverage_state == "UNEVALUATED"]
    assert len(unevaluated) == 1
    assert unevaluated[0].typed_state == "UNEVALUATED"
    assert unevaluated[0].empirical_fact_refs == ()
    assert unevaluated[0].negative_evidence is False
    assert unevaluated[0].semantic_absence is False


def test_valid_empty_exploration_is_only_about_evaluated_candidates():
    fx = _fixture("empty", valid_empty=True)
    result = _run(fx, _adaptive_authority(fx))
    assert result.evaluated_count == 2
    assert result.unevaluated_count == 0
    assert result.evaluated_valid_empty is True
    assert all(r.typed_state == "VALID_EMPTY" for r in result.receipts)
    assert result.coverage_claim == I08_COVERAGE_CLAIM


def test_proposal_order_is_invariant_to_catalog_input_order():
    fx = _fixture("order")
    authority = _adaptive_authority(fx)
    normal = _run(fx, authority)
    reversed_run = execute_adaptive_exploratory_discovery(
        repository=fx["source"]["repo"],
        discovery_authority=authority,
        authority_registry=fx["registry"],
        release_refs=(fx["source"]["release_ref"],),
        predicate_catalog=tuple(reversed(fx["predicates"])),
        query_template_catalog=tuple(reversed(fx["queries"])),
    )
    assert normal.proposal_trace == reversed_run.proposal_trace
    assert normal.replay_ref == reversed_run.replay_ref


def test_rng_identity_drift_requires_new_exact_execution_contract():
    fx = _fixture("rng")
    a = _adaptive_authority(
        fx,
        strategy="SEEDED_HASH_ORDER",
        rng={"kind": "DETERMINISTIC_SEEDED_HASH", "seed": "seed-A"},
    )
    stale = a.adaptive_execution_contract_ref
    b = _adaptive_authority(
        fx,
        strategy="SEEDED_HASH_ORDER",
        rng={"kind": "DETERMINISTIC_SEEDED_HASH", "seed": "seed-B"},
    )
    assert a.ref != b.ref
    assert _run(fx, a).replay_ref != _run(fx, b).replay_ref
    tampered = _adaptive_authority(
        fx,
        strategy="SEEDED_HASH_ORDER",
        rng={"kind": "DETERMINISTIC_SEEDED_HASH", "seed": "seed-B"},
        stale_execution_ref=stale,
    )
    with pytest.raises(AdaptiveExploratoryDiscoveryError, match="contract hash mismatch"):
        _run(fx, tampered)


def test_stopping_rule_tamper_fails_closed_against_presearch_contract_hash():
    fx = _fixture("stop-tamper")
    original = _adaptive_authority(fx)
    tampered = _adaptive_authority(
        fx,
        stop={"kind": "STOP_AFTER_SUPPORTED_COUNT", "supported_count": 1},
        stale_execution_ref=original.adaptive_execution_contract_ref,
    )
    with pytest.raises(AdaptiveExploratoryDiscoveryError, match="contract hash mismatch"):
        _run(fx, tampered)


def test_supported_count_stopping_is_explicit_and_nonexhaustive():
    fx = _fixture("stop")
    authority = _adaptive_authority(
        fx,
        stop={"kind": "STOP_AFTER_SUPPORTED_COUNT", "supported_count": 1},
    )
    result = _run(fx, authority)
    assert result.stopping_reason == "STOPPING_RULE_REACHED"
    assert result.evaluated_count == 1
    assert result.unevaluated_count == 1
    assert result.coverage_claim == I08_COVERAGE_CLAIM


def test_static_pruning_is_visible_and_never_negative_evidence():
    fx = _fixture("prune")
    authority = _adaptive_authority(
        fx,
        pruning={"kind": "STATIC_FAMILY_PRUNE", "families": ["UNARY_SOCIAL_FORK"], "prune_rule_ref": _ref("PRUNE_RULE", "unary")},
    )
    result = _run(fx, authority)
    assert (result.evaluated_count, result.pruned_count, result.unevaluated_count) == (0, 2, 0)
    assert all(r.typed_state == "PRUNED_BY_AUTHORITY" for r in result.receipts)
    assert all(r.negative_evidence is False for r in result.receipts)



def test_out_of_scope_frontier_member_fails_before_proposal():
    fx = _fixture("scope")
    authority = _adaptive_authority(
        fx,
        source_scope_override={"allowed_universe_refs": [_ref("EmpiricalUniverse@1.0.0", "other-universe")]},
    )
    with pytest.raises(Pre553AuthorityError, match="source-universe authority|source universe exceeds"):
        _run(fx, authority)

def test_out_of_scope_diagnostic_candidate_is_rejected_not_proposed():
    fx = _fixture("diag-scope")
    authority = _adaptive_authority(
        fx,
        strategy="DIAGNOSTIC_PRIORITY",
        permissible=("MI",),
        proposal_extra={"diagnostic_kind": "MI", "direction": "HIGH_FIRST"},
    )
    with pytest.raises(Pre553SemanticCollapseError, match="out-of-frontier"):
        _run(fx, authority, diagnostic_values={"f" * 64: {"MI": "1/2"}})


def test_diagnostics_cannot_authorize_semantic_widening():
    fx = _fixture("diag-widen")
    authority = _adaptive_authority(
        fx,
        proposal_extra={"allows_new_candidates_from_diagnostics": True},
    )
    with pytest.raises(Pre553SemanticCollapseError, match="may not widen"):
        _run(fx, authority)


def test_diagnostic_priority_changes_order_only_never_empirical_truth():
    fx = _fixture("diag-order")
    canonical = _run(fx, _adaptive_authority(fx))
    hashes = [r.candidate_identity["candidate_hash"] for r in canonical.receipts]
    diagnostics = {hashes[0]: {"MI": "1/10"}, hashes[1]: {"MI": "9/10"}}
    authority = _adaptive_authority(
        fx,
        strategy="DIAGNOSTIC_PRIORITY",
        permissible=("MI",),
        proposal_extra={"diagnostic_kind": "MI", "direction": "HIGH_FIRST"},
    )
    result = _run(fx, authority, diagnostic_values=diagnostics)
    assert result.proposal_trace[0] == hashes[1]
    assert all(r.diagnostic_score_is_empirical_fact is False for r in result.receipts)
    assert all(r.structural_truth_effect is False for r in result.receipts)
    assert all(r.actor_v3_effect is False for r in result.receipts)


def test_accepted_i05_exact_result_remains_independent_and_immutable():
    fx = _fixture("i05-independent")
    exact = execute_exact_bounded_discovery(
        repository=fx["source"]["repo"],
        discovery_authority=_exact_authority(fx),
        authority_registry=fx["registry"],
        release_refs=(fx["source"]["release_ref"],),
        predicate_catalog=fx["predicates"],
        query_template_catalog=fx["queries"],
    )
    before = (
        exact.replay_ref,
        exact.evaluated_frontier_ref,
        exact.candidate_count,
        exact.covered_candidate_count,
        tuple(r.ref for r in exact.receipts),
    )
    adaptive = _run(
        fx,
        _adaptive_authority(fx, max_candidates=1),
        accepted_i05_result=exact,
    )
    after = (
        exact.replay_ref,
        exact.evaluated_frontier_ref,
        exact.candidate_count,
        exact.covered_candidate_count,
        tuple(r.ref for r in exact.receipts),
    )
    assert before == after
    assert adaptive.accepted_i05_parent_head == I05_ACCEPTED_PARENT_HEAD
    assert exact.coverage_claim == "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"
    assert adaptive.coverage_claim == I08_COVERAGE_CLAIM
