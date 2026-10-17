import pytest

from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_discovery_exact import (
    CANDIDATE_GRAMMAR_SCHEMA,
    COVERAGE_CLAIM,
    ExactBoundedCoverageError,
    ExactBoundedDiscoveryError,
    _allowed_validation_kinds,
    execute_exact_bounded_discovery,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _build_source,
    _cell_map,
    _coordinate_leaf,
    _h,
    _predicate,
    _query,
    _query_authority,
    _registry,
    _response_leaf,
    _run,
)


def _gref(grammar, tag="g"):
    digest = semantic_hash(grammar)
    return ExactRef(
        "PRE553_I05_CANDIDATE_GRAMMAR",
        f"urn:test:i05:grammar:{tag}:{digest}",
        digest,
    )


def _atom(atom_id, predicate, kind, *, ancestry=()):
    return {
        "atom_id": atom_id,
        "predicate_ref": predicate.ref,
        "kind": kind,
        "ancestry_refs": tuple(ancestry),
    }


def _qt(template_id, query):
    return {"template_id": template_id, "query_ref": query.ref}


def _grammar(*, operation, atoms, templates, rules, k=3, j=4, allow_empty=False):
    return {
        "schema": CANDIDATE_GRAMMAR_SCHEMA,
        "discovery_operation": operation,
        "atoms": tuple(atoms),
        "query_templates": tuple(templates),
        "rules": tuple(rules),
        "limits": {
            "maximum_conditioner_arity_K": k,
            "maximum_target_arity_J": j,
        },
        "allow_empty_frontier": allow_empty,
    }


def _discovery_authority(source, grammar, dauth, *, tag="d", pruning=None, ranking=None, grammar_ref=None):
    if pruning is None:
        pruning = {"kind": "NONE_EXACT_EVALUATE_ALL"}
    if ranking is None:
        ranking = {"kind": "NONE", "controls_frontier": False}
    if grammar_ref is None:
        grammar_ref = _gref(grammar, tag)
    return DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(dauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", f"urn:test:i05:authority-replay:{tag}", _h(f"i05-authority-replay:{tag}")
        ),
        candidate_grammar_ref=grammar_ref,
        candidate_universe_definition=grammar,
        source_universe_scope={"allowed_universe_refs": (source["universe"].ref,)},
        risk_set_scope={"allowed_risk_set_refs": tuple(source["risk_refs"].values())},
        topology_scope={"maximum_target_arity_J": grammar["limits"]["maximum_target_arity_J"]},
        measure_scope={"allowed_measure_kinds": ("RAW", "GOVERNED_WEIGHTED")},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": (
            "DISTRIBUTION_DIFFERS_FROM_BASELINE",
            "JOINT_NOT_PRODUCT_OF_MARGINALS",
            "CONDITIONAL_REVERSAL",
            "TARGET_CELL_SUPPORTED",
        )},
        coverage_claim=COVERAGE_CLAIM,
        pruning_contract=pruning,
        algorithm_identity_if_semantically_required="PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0",
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
        rng_policy_if_any="NONE",
        mode="EXACT_BOUNDED",
        candidate_scoring_or_ranking_rule_if_any=ranking,
    )


def _d_auth(tag="discovery"):
    return _auth(
        tag,
        "DISCOVERY_FRONTIER",
        families=("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"),
    )


def _execute(source, qauth, dauth, grammar, predicates, queries, *, authority=None):
    if authority is None:
        authority = _discovery_authority(source, grammar, dauth)
    return execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=predicates,
        query_template_catalog=queries,
    )


def _rule(rule_id, family, form, **kwargs):
    return {
        "rule_id": rule_id,
        "family": family,
        "form": form,
        **kwargs,
    }


def test_rules_only_validation_authority_is_exact_and_fail_closed():
    kinds = {
        "DISTRIBUTION_DIFFERS_FROM_BASELINE",
        "JOINT_NOT_PRODUCT_OF_MARGINALS",
        "CONDITIONAL_REVERSAL",
        "TARGET_CELL_SUPPORTED",
    }
    rules = {"rules": tuple({"kind": kind} for kind in sorted(kinds))}
    assert _allowed_validation_kinds(rules) == kinds
    assert _allowed_validation_kinds({}) == set()
    with pytest.raises(Pre553AuthorityError, match="unknown"):
        _allowed_validation_kinds({"rules": ({"kind": "NMI"},)})
    with pytest.raises(Pre553AuthorityError, match="contradict"):
        _allowed_validation_kinds({
            "kinds": ("TARGET_CELL_SUPPORTED",),
            "rules": ({"kind": "CONDITIONAL_REVERSAL"},),
        })


def test_rules_only_validation_authority_executes_only_its_literal_kind():
    source = _build_source("i05-rules-only", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
    ])
    qauth, dauth = _query_authority("i05-rules-only"), _d_auth("i05-rules-only-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    validation = {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}
    grammar = _grammar(
        operation="I03-OP-i05-rules-only-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation=validation,
        )],
    )
    base_authority = _discovery_authority(source, grammar, dauth)
    authority = DiscoveryAuthority(
        typed_state=base_authority.typed_state,
        authority_snapshot_refs=base_authority.authority_snapshot_refs,
        dependency_refs=base_authority.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base_authority.producer_replay_locator_or_reference_root
        ),
        **{
            **dict(base_authority.semantic_fields),
            "validation_rules": {"rules": (validation,)},
        },
    )
    result = _execute(
        source, qauth, dauth, grammar, (all_p, x1), (yq,), authority=authority
    )
    assert result.candidate_count == result.covered_candidate_count == 1
    assert tuple(fact.ref for fact in result.empirical_facts) == result.empirical_fact_refs


def test_xor_zero_unary_signal_is_reached_without_unary_screen():
    source = _build_source("i05-xor", [
        {"id": "R00", "responses": {"X": 0, "Y": 0, "Z": 0}},
        {"id": "R01", "responses": {"X": 0, "Y": 1, "Z": 1}},
        {"id": "R10", "responses": {"X": 1, "Y": 0, "Z": 1}},
        {"id": "R11", "responses": {"X": 1, "Y": 1, "Z": 0}},
    ])
    qauth, dauth = _query_authority("i05-xor"), _d_auth("i05-xor-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    y1 = _predicate(source, qauth, _response_leaf(source, qauth, "Y", 1), tag="y1")
    zq = _query(source, qauth, all_p, ("Z",), tag="z-template")

    # Hostile precondition: each unary relation is exactly flat.
    for p in (x1, y1):
        fact = _run(source, qauth, p, _query(source, qauth, p, ("Z",), tag=f"unary-{p.ref.content_hash[:6]}"), registry=_registry(source, qauth)).facts[0]
        assert _cell_map(fact)["1"]["raw_numerator_support"] == 1
        assert fact.raw_denominator_support == 2

    operation = "I03-OP-i05-xor-discovery"
    grammar = _grammar(
        operation=operation,
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE"), _atom("Y1", y1, "RESPONSE")],
        templates=[_qt("Z", zq)],
        rules=[_rule(
            "xor", "RESPONSE_X_COORDINATE_CONJUNCTION", "XOR_EXACTLY_ONE_COMBINATIONS",
            atom_ids=("X1", "Y1"), arity=2, baseline_atom_id="ALL", query_template_id="Z",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, x1, y1), (zq,))
    assert result.candidate_count == result.covered_candidate_count == 1
    assert result.coverage_claim == COVERAGE_CLAIM
    assert result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert result.receipts[0].coverage_state == "EVALUATED_SUPPORTED"
    assert result.valid_empty is False


def test_simpson_reversal_is_detected_from_exact_pooled_and_stratified_facts():
    rows = []
    for i in range(3): rows.append({"id": f"A1-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A"}})
    for i in range(8): rows.append({"id": f"A0s-{i}", "responses": {"X": 0, "Y": 1}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"A0f-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"B1s-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "B"}})
    for i in range(8): rows.append({"id": f"B1f-{i}", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}})
    for i in range(2): rows.append({"id": f"B0-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "B"}})
    source = _build_source("i05-simpson", rows)
    qauth, dauth = _query_authority("i05-simpson"), _d_auth("i05-simpson-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    x0 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="x0")
    ga = _predicate(source, qauth, _coordinate_leaf(source, "G", "A"), tag="ga")
    gb = _predicate(source, qauth, _coordinate_leaf(source, "G", "B"), tag="gb")
    yq = _query(source, qauth, all_p, ("Y",), tag="y-template")
    grammar = _grammar(
        operation="I03-OP-i05-simpson-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE"), _atom("X0", x0, "RESPONSE"), _atom("GA", ga, "COORDINATE"), _atom("GB", gb, "COORDINATE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "simpson", "CONDITIONAL_REVERSAL_OR_SIMPSON", "REVERSAL_GRID",
            baseline_atom_id="ALL", exposure_positive_atom_id="X1", exposure_negative_atom_id="X0",
            stratum_atom_ids=("GA", "GB"), query_template_id="Y",
            validation={"kind": "CONDITIONAL_REVERSAL", "target_cell": "1"},
        )],
        k=2,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, x1, x0, ga, gb), (yq,))
    assert result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert len(result.receipts[0].empirical_fact_refs) == 6


def test_supported_non_top_minority_is_not_prevalence_pruned():
    rows = []
    for i in range(10): rows.append({"id": f"A{i}", "responses": {"Y": 0}, "coords": {"G": "A"}})
    for i in range(8): rows.append({"id": f"B{i}", "responses": {"Y": 0}, "coords": {"G": "B"}})
    for i in range(2): rows.append({"id": f"C{i}", "responses": {"Y": 1}, "coords": {"G": "C"}})
    source = _build_source("i05-minority", rows)
    qauth, dauth = _query_authority("i05-minority"), _d_auth("i05-minority-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    c = _predicate(source, qauth, _coordinate_leaf(source, "G", "C"), tag="c")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-minority-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("C", c, "COORDINATE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "minority", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
            atom_ids=("C",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, c), (yq,))
    assert result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert result.receipts[0].support_uncertainty_state["raw_denominators"][0] in {2, 20}


def test_recursive_subgroup_fork_preserves_exact_parent_ancestry():
    source = _build_source("i05-recursive", [
        {"id": "R1", "responses": {"Y": 1}, "coords": {"H": 1}},
        {"id": "R2", "responses": {"Y": 0}, "coords": {"H": 0}},
        {"id": "R3", "responses": {"Y": 0}, "coords": {"H": 0}},
        {"id": "R4", "responses": {"Y": 0}, "coords": {"H": 1}},
    ])
    qauth, dauth = _query_authority("i05-recursive"), _d_auth("i05-recursive-discovery")
    parent = _branch_predicate(source, qauth, members=(source["respondents"]["R1"], source["respondents"]["R2"], source["respondents"]["R3"]), tag="parent")
    h1 = _predicate(source, qauth, _coordinate_leaf(source, "H", 1), tag="h1")
    yq = _query(source, qauth, parent, ("Y",), tag="y")
    ancestry = ExactRef("DISCOVERY_BRANCH_ANCESTRY", "urn:test:i05:parent", _h("i05-parent-ancestry"))
    grammar = _grammar(
        operation="I03-OP-i05-recursive-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH", ancestry=(ancestry,)), _atom("H1", h1, "COORDINATE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("H1",), baseline_atom_id="PARENT", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    result = _execute(source, qauth, dauth, grammar, (parent, h1), (yq,))
    receipt = result.receipts[0]
    assert receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert ancestry.as_dict() in receipt.branch_or_parent_ancestry_refs


def test_same_respondent_cotravel_and_branch_conditioned_cotravel_both_work():
    source = _build_source("i05-cotravel", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "Y": 1}},
        {"id": "R3", "responses": {"X": 0, "Y": 0}},
        {"id": "R4", "responses": {"X": 0, "Y": 0}},
    ])
    qauth, dauth = _query_authority("i05-cotravel"), _d_auth("i05-cotravel-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    branch = _branch_predicate(source, qauth, members=(source["respondents"]["R1"], source["respondents"]["R2"], source["respondents"]["R3"]), tag="branch")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    yq_all = _query(source, qauth, all_p, ("Y",), tag="y-all")
    yq_branch = _query(source, qauth, branch, ("Y",), tag="y-branch")
    grammar = _grammar(
        operation="I03-OP-i05-cotravel-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("BRANCH", branch, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("YALL", yq_all), _qt("YBR", yq_branch)],
        rules=[
            _rule("pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM", atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="YALL", validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}),
            _rule("branch-pair", "BRANCH_CONDITIONED_COTRAVEL", "SINGLE_ATOM", atom_ids=("X1",), baseline_atom_id="BRANCH", query_template_id="YBR", validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}),
        ],
        k=2,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, branch, x1), (yq_all, yq_branch))
    assert result.candidate_count == 2
    assert {r.typed_state for r in result.receipts} == {"DISCOVERED_RESULT_SUPPORTED"}


def test_bounded_response_x_position_cartesian_frontier_is_fully_evaluated():
    source = _build_source("i05-rxp", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A"}},
        {"id": "R2", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}},
        {"id": "R3", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A"}},
        {"id": "R4", "responses": {"X": 0, "Y": 1}, "coords": {"G": "B"}},
    ])
    qauth, dauth = _query_authority("i05-rxp"), _d_auth("i05-rxp-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    x0 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="x0")
    ga = _predicate(source, qauth, _coordinate_leaf(source, "G", "A"), tag="ga")
    gb = _predicate(source, qauth, _coordinate_leaf(source, "G", "B"), tag="gb")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-rxp-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE"), _atom("X0", x0, "RESPONSE"), _atom("GA", ga, "COORDINATE"), _atom("GB", gb, "COORDINATE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "rxp", "RESPONSE_X_COORDINATE_CONJUNCTION", "AND_CARTESIAN_GROUPS",
            atom_groups=(("X1", "X0"), ("GA", "GB")), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, x1, x0, ga, gb), (yq,))
    assert result.candidate_count == result.covered_candidate_count == 4
    assert all(r.coverage_state.startswith("EVALUATED_") for r in result.receipts)


def test_higher_order_parity_uses_exact_joint_not_lower_order_signal():
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                rows.append({"id": f"R{a}{b}{c}", "responses": {"A": a, "B": b, "C": c, "Z": a ^ b ^ c}})
    source = _build_source("i05-parity4", rows)
    qauth, dauth = _query_authority("i05-parity4"), _d_auth("i05-parity4-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    joint = _query(source, qauth, all_p, ("A", "B", "C", "Z"), tag="joint")
    marginals = [_query(source, qauth, all_p, (q,), tag=f"m-{q}") for q in ("A", "B", "C", "Z")]
    grammar = _grammar(
        operation="I03-OP-i05-parity4-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH")],
        templates=[_qt("J", joint), *[_qt(f"M{i}", q) for i, q in enumerate(marginals)]],
        rules=[_rule(
            "parity4", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "JOINT_DEPENDENCE",
            baseline_atom_id="ALL", joint_template_id="J", marginal_template_ids=("M0", "M1", "M2", "M3"),
            validation={"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"},
        )],
        k=3, j=4,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p,), (joint, *marginals))
    assert result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert len(result.receipts[0].empirical_fact_refs) == 5


def test_bounded_higher_order_configuration_cells_are_individually_covered():
    source = _build_source("i05-config3", [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y}}
        for x in (0, 1) for y in (0, 1)
    ])
    qauth, dauth = _query_authority("i05-config3"), _d_auth("i05-config3-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    joint = _query(source, qauth, all_p, ("X", "Y", "Z"), tag="joint")
    cells = tuple((str(x), str(y), str(z)) for x in (0, 1) for y in (0, 1) for z in (0, 1))
    grammar = _grammar(
        operation="I03-OP-i05-config3-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH")],
        templates=[_qt("J", joint)],
        rules=[_rule(
            "config3", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "BASE_QUERY",
            baseline_atom_id="ALL", query_template_id="J", target_cells=cells,
            validation={"kind": "TARGET_CELL_SUPPORTED"},
        )],
        k=2, j=3,
    )
    result = _execute(source, qauth, dauth, grammar, (all_p,), (joint,))
    assert result.candidate_count == result.covered_candidate_count == 8
    assert sum(r.typed_state == "DISCOVERED_RESULT_SUPPORTED" for r in result.receipts) == 4
    assert sum(r.typed_state == "VALID_EMPTY" for r in result.receipts) == 4
    assert result.valid_empty is False


def test_valid_empty_frontier_is_typed_and_complete():
    source = _build_source("i05-empty", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ])
    qauth, dauth = _query_authority("i05-empty"), _d_auth("i05-empty-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    empty = _branch_predicate(source, qauth, members=(), tag="empty")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-empty-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("EMPTY", empty, "BRANCH")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "empty", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
            atom_ids=("EMPTY",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, empty), (yq,))
    assert result.valid_empty is True
    assert result.receipts[0].typed_state == "VALID_EMPTY"
    assert result.receipts[0].coverage_state == "EVALUATED_VALID_EMPTY"
    assert result.candidate_count == result.covered_candidate_count == 1


def test_catalog_order_does_not_change_frontier_or_receipt_identity():
    source = _build_source("i05-order", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
    ])
    qauth, dauth = _query_authority("i05-order"), _d_auth("i05-order-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-order-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule("pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM", atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y", validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"})],
    )
    authority = _discovery_authority(source, grammar, dauth)
    a = _execute(source, qauth, dauth, grammar, (all_p, x1), (yq,), authority=authority)
    b = _execute(source, qauth, dauth, grammar, (x1, all_p), (yq,), authority=authority)
    assert a.evaluated_frontier_ref == b.evaluated_frontier_ref
    assert tuple(r.ref for r in a.receipts) == tuple(r.ref for r in b.receipts)
    assert a.replay_ref == b.replay_ref


def test_frontier_hash_mismatch_adaptive_and_score_pruning_fail_closed():
    source = _build_source("i05-authority", [{"id": "R1", "responses": {"Y": 1}}])
    qauth, dauth = _query_authority("i05-authority"), _d_auth("i05-authority-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-authority-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH")], templates=[_qt("Y", yq)], rules=[], allow_empty=True,
    )
    wrong = ExactRef("PRE553_I05_CANDIDATE_GRAMMAR", "urn:test:i05:wrong", _h("wrong"))
    bad_hash = _discovery_authority(source, grammar, dauth, grammar_ref=wrong)
    with pytest.raises(ExactBoundedDiscoveryError):
        _execute(source, qauth, dauth, grammar, (all_p,), (yq,), authority=bad_hash)

    topk = _discovery_authority(source, grammar, dauth, pruning={"kind": "TOP_K", "k": 1})
    with pytest.raises(ExactBoundedCoverageError):
        _execute(source, qauth, dauth, grammar, (all_p,), (yq,), authority=topk)

    ranking = _discovery_authority(source, grammar, dauth, ranking={"kind": "NMI", "controls_frontier": True})
    with pytest.raises(ExactBoundedCoverageError):
        _execute(source, qauth, dauth, grammar, (all_p,), (yq,), authority=ranking)

    adaptive = DiscoveryAuthority(
        typed_state="ADAPTIVE_EXPLORATORY_AUTHORIZED",
        authority_snapshot_refs=bad_hash.authority_snapshot_refs,
        dependency_refs=bad_hash.dependency_refs,
        producer_replay_locator_or_reference_root=bad_hash.producer_replay_locator_or_reference_root,
        **{**dict(bad_hash.semantic_fields), "coverage_claim": "EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE", "mode": "ADAPTIVE_EXPLORATORY", "candidate_grammar_ref": _gref(grammar, "adaptive")},
    )
    with pytest.raises(ExactBoundedDiscoveryError):
        _execute(source, qauth, dauth, grammar, (all_p,), (yq,), authority=adaptive)


def test_diagnostic_validation_cannot_become_canonical_empirical_truth():
    source = _build_source("i05-diagnostic", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
    ])
    qauth, dauth = _query_authority("i05-diagnostic"), _d_auth("i05-diagnostic-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-i05-diagnostic-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "bad", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "NMI"},
        )],
    )
    with pytest.raises(ExactBoundedDiscoveryError):
        _execute(source, qauth, dauth, grammar, (all_p, x1), (yq,))
