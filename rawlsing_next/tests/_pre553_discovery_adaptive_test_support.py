from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    ExactRef,
    Pre553SemanticCollapseError,
    semantic_hash,
)
from rawlsing_next.pre553_discovery_exact import (
    CANDIDATE_GRAMMAR_SCHEMA,
    I05_CONTRACT_ID,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_discovery_adaptive import (
    I05_ACCEPTED_PARENT_HEAD,
    I08_CONTRACT_ID,
    I08_COVERAGE_CLAIM,
    AdaptiveExploratoryDiscoveryError,
    execute_adaptive_exploratory_discovery,
    make_adaptive_execution_contract_ref,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _build_source,
    _predicate,
    _query,
    _ref,
    _response_leaf,
)


def _fixture(tag="i08", *, valid_empty=False):
    rows = (
        [
            {"id": "R1", "responses": {"X": 0, "Y": 0}},
            {"id": "R2", "responses": {"X": 0, "Y": 0}},
            {"id": "R3", "responses": {"X": 1, "Y": 1}},
            {"id": "R4", "responses": {"X": 1, "Y": 1}},
        ]
        if not valid_empty
        else [
            {"id": "R1", "responses": {"X": 0, "Y": 0}},
            {"id": "R2", "responses": {"X": 0, "Y": 1}},
            {"id": "R3", "responses": {"X": 1, "Y": 0}},
            {"id": "R4", "responses": {"X": 1, "Y": 1}},
        ]
    )
    source = _build_source(tag, rows)
    qauth = _auth(
        f"query-{tag}",
        "PREDICATE_GRAMMAR",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    )
    frontier_auth = _auth(
        f"frontier-{tag}",
        "DISCOVERY_FRONTIER",
        families=("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"),
    )
    baseline = _branch_predicate(source, qauth, tag="all")
    x0 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="x0")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    query = _query(source, qauth, baseline, ("Y",), tag="Y")
    operation = tuple(frontier_auth.governed_operations)[0]
    definition = {
        "schema": CANDIDATE_GRAMMAR_SCHEMA,
        "discovery_operation": operation,
        "limits": {"maximum_conditioner_arity_K": 2, "maximum_target_arity_J": 1},
        "atoms": [
            {"atom_id": "ALL", "kind": "BRANCH_BASELINE", "predicate_ref": baseline.ref, "ancestry_refs": []},
            {"atom_id": "X0", "kind": "SURVEY_RESPONSE_EVENT", "predicate_ref": x0.ref, "ancestry_refs": []},
            {"atom_id": "X1", "kind": "SURVEY_RESPONSE_EVENT", "predicate_ref": x1.ref, "ancestry_refs": []},
        ],
        "query_templates": [{"template_id": "Y", "query_ref": query.ref}],
        "rules": [{
            "rule_id": "X-FORK",
            "family": "UNARY_SOCIAL_FORK",
            "form": "SINGLE_ATOM",
            "baseline_atom_id": "ALL",
            "query_template_id": "Y",
            "atom_ids": ["X0", "X1"],
            "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        }],
    }
    grammar_hash = semantic_hash(definition)
    grammar_ref = ExactRef(
        "PRE553_I05_CANDIDATE_GRAMMAR",
        f"urn:test:i08:grammar:{tag}",
        grammar_hash,
    )
    registry = AuthorityRegistry((*source["authorities"], qauth, frontier_auth))
    return {
        "source": source,
        "qauth": qauth,
        "frontier_auth": frontier_auth,
        "baseline": baseline,
        "x0": x0,
        "x1": x1,
        "query": query,
        "definition": definition,
        "grammar_ref": grammar_ref,
        "registry": registry,
        "predicates": (baseline, x0, x1),
        "queries": (query,),
    }


def _adaptive_authority(
    fx,
    *,
    strategy="CANONICAL_CANDIDATE_HASH_ORDER",
    max_candidates=10,
    max_queries=100,
    stop=None,
    pruning=None,
    rng=None,
    permissible=(),
    proposal_extra=None,
    stale_execution_ref=None,
    source_scope_override=None,
):
    proposal = {"strategy": strategy, **(proposal_extra or {})}
    if stop is None:
        stop = {"kind": "EXHAUST_OR_BUDGET"}
    if pruning is None:
        pruning = {"kind": "NONE"}
    if rng is None:
        rng = {"kind": "NONE"}
    budget = {
        "max_evaluated_candidates": max_candidates,
        "max_query_executions": max_queries,
    }
    validation_partition = {"kind": "NONE__EXACT_I03_I05_VALIDATION"}
    tie = {
        "CANONICAL_CANDIDATE_HASH_ORDER": "CANONICAL_CANDIDATE_HASH_ORDER",
        "SEEDED_HASH_ORDER": "SEEDED_HASH_THEN_CANDIDATE_HASH",
        "STATE_FEEDBACK_PRIORITY": "STATE_FEEDBACK_THEN_SEEDED_HASH_THEN_CANDIDATE_HASH",
        "DIAGNOSTIC_PRIORITY": "DIAGNOSTIC_EXACT_VALUE_THEN_CANDIDATE_HASH",
    }[strategy]
    execution_ref = stale_execution_ref or make_adaptive_execution_contract_ref(
        proposal_contract=proposal,
        budget_contract=budget,
        stopping_rule=stop,
        pruning_contract=pruning,
        rng_policy_if_any=rng,
        validation_partition_contract=validation_partition,
        permissible_diagnostics=permissible,
        tie_order_rules=tie,
        algorithm_identity=I08_CONTRACT_ID,
    )
    return DiscoveryAuthority(
        typed_state="ADAPTIVE_EXPLORATORY_AUTHORIZED",
        authority_snapshot_refs=(fx["frontier_auth"].authority_ref,),
        dependency_refs=(fx["grammar_ref"],),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "i08-adaptive-authority"),
        candidate_grammar_ref=fx["grammar_ref"],
        candidate_universe_definition=fx["definition"],
        source_universe_scope=(
            source_scope_override
            if source_scope_override is not None
            else {"allowed_universe_refs": [fx["source"]["universe"].ref]}
        ),
        risk_set_scope={"allowed_risk_set_refs": list(fx["source"]["risk_refs"].values())},
        topology_scope={"maximum_target_arity_J": 1},
        measure_scope={"allowed_measure_kinds": ["RAW"]},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": ["DISTRIBUTION_DIFFERS_FROM_BASELINE"]},
        coverage_claim=I08_COVERAGE_CLAIM,
        pruning_contract=pruning,
        algorithm_identity_if_semantically_required=I08_CONTRACT_ID,
        tie_order_rules=tie,
        rng_policy_if_any=rng,
        mode="ADAPTIVE_EXPLORATORY",
        proposal_contract=proposal,
        budget_contract=budget,
        stopping_rule=stop,
        validation_partition_contract=validation_partition,
        permissible_diagnostics=permissible,
        adaptive_execution_contract_ref=execution_ref,
    )


def _exact_authority(fx):
    return DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(fx["frontier_auth"].authority_ref,),
        dependency_refs=(fx["grammar_ref"],),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "i05-exact-authority"),
        candidate_grammar_ref=fx["grammar_ref"],
        candidate_universe_definition=fx["definition"],
        source_universe_scope={"allowed_universe_refs": [fx["source"]["universe"].ref]},
        risk_set_scope={"allowed_risk_set_refs": list(fx["source"]["risk_refs"].values())},
        topology_scope={"maximum_target_arity_J": 1},
        measure_scope={"allowed_measure_kinds": ["RAW"]},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": ["DISTRIBUTION_DIFFERS_FROM_BASELINE"]},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required=I05_CONTRACT_ID,
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
        rng_policy_if_any=None,
        mode="EXACT_BOUNDED",
    )


def _run(fx, authority, **kwargs):
    return execute_adaptive_exploratory_discovery(
        repository=fx["source"]["repo"],
        discovery_authority=authority,
        authority_registry=fx["registry"],
        release_refs=(fx["source"]["release_ref"],),
        predicate_catalog=fx["predicates"],
        query_template_catalog=fx["queries"],
        **kwargs,
    )

