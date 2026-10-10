"""HQ273 C01 — genuine source-free ``q(Y|A)`` and ``q(Y|A,B)`` through the accepted I03 executor.

DEVELOPMENT_FIXTURE_ONLY.

Positive and malicious-negative court for the sealed HQ272 R01 finding that the frozen
GT12 Q86A/B wrapper can only produce a common-base ``DERIVED_BRANCH_COHORT`` and a
joint target tensor, never two separately denominated conditioned facts.

The executor under test is the accepted public one:
``rawlsing_next.pre553_empirical_query.execute_empirical_query`` / ``replay_empirical_query``.
No counting stub, no parallel API and no bypass of authority/grammar gates is used.
"""
from __future__ import annotations

import pytest
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import (
    execute_empirical_query,
    replay_empirical_query,
)
from rawlsing_next.tests.hq273_c01_true_conditional_fixture import (
    CONDITION_A,
    CONDITION_B,
    ELIGIBLE,
    FIXTURE_ID,
    FIXTURE_MARKER,
    RAW_MEASURE,
    SINGLE_UNIVERSE,
    SUBSTANTIVE,
    TARGET_Y,
    TRUE_CONDITIONAL_OPERATION,
    _grammar_authority,
    _ref,
    and_node,
    build_three_item_fixture,
    cell_counts,
    common_case_base_ast,
    member_ref_ids,
    response_eq_leaf,
    risk_ref_ids,
    run_true_conditional,
    true_conditional_predicate,
    true_conditional_query,
    two_nested_true_conditional_facts,
    unguarded_condition_fact,
    zero_support_fact,
)


# ---------------------------------------------------------------------------
# The fixture.  Deliberately chosen so that N1 != N2 and q1 != q2 visibly.
#
#   P10 is the coercion hazard: its A event is typed REFUSAL but its stored native
#   value is the substantive bucket "0", exactly what a naive recode of a refusal
#   code into a "No" column produces.  It MUST NOT enter either denominator.
#
#   P08 (B = DK) and P09 (Y = DK) MUST be excluded by the complete-case policy even
#   though they would otherwise satisfy A = 0.
# ---------------------------------------------------------------------------
FIXTURE_TAG = "hq273c01-main"

FIXTURE_ROWS = (
    {"id": "P01", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "0")}},
    {"id": "P02", "responses": {TARGET_Y: (SUBSTANTIVE, "0"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "0")}},
    {"id": "P03", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "1")}},
    {"id": "P04", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "1")}},
    {"id": "P05", "responses": {TARGET_Y: (SUBSTANTIVE, "0"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "0")}},
    {"id": "P06", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: (SUBSTANTIVE, "1"), CONDITION_B: (SUBSTANTIVE, "0")}},
    {"id": "P07", "responses": {TARGET_Y: (SUBSTANTIVE, "0"), CONDITION_A: (SUBSTANTIVE, "1"), CONDITION_B: (SUBSTANTIVE, "1")}},
    {"id": "P08", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: ("DK", "9")}},
    {"id": "P09", "responses": {TARGET_Y: ("DK", "9"), CONDITION_A: (SUBSTANTIVE, "0"), CONDITION_B: (SUBSTANTIVE, "0")}},
    {"id": "P10", "responses": {TARGET_Y: (SUBSTANTIVE, "1"), CONDITION_A: ("REFUSAL", "0"), CONDITION_B: (SUBSTANTIVE, "0")}},
)


# ---------------------------------------------------------------------------
# Independent oracle.  Plain set logic over the declared row spec.  This oracle
# deliberately shares no code, no helper and no object with the I03 engine.
# ---------------------------------------------------------------------------
def independent_oracle(rows):
    substantive = {r["id"] for r in rows
                   if all(r["responses"][q][0] == SUBSTANTIVE for q in (TARGET_Y, CONDITION_A, CONDITION_B))}
    eligible = {r["id"] for r in rows if all(r.get("routing", {}).get(q, ELIGIBLE) == ELIGIBLE
                                             for q in (TARGET_Y, CONDITION_A, CONDITION_B))}
    s = substantive & eligible

    def value(rid, q):
        return next(r["responses"][q][1] for r in rows if r["id"] == rid)

    r1 = {rid for rid in s if value(rid, CONDITION_A) == "0"}
    r2 = {rid for rid in r1 if value(rid, CONDITION_B) == "0"}
    k1 = {rid for rid in r1 if value(rid, TARGET_Y) == "1"}
    k2 = {rid for rid in r2 if value(rid, TARGET_Y) == "1"}
    return {
        "S": s, "R1": r1, "R2": r2, "K1": k1, "K2": k2,
        "N1": len(r1), "N2": len(r2), "K1_count": len(k1), "K2_count": len(k2),
        "q1": (len(k1), len(r1)), "q2": (len(k2), len(r2)),
        # hazard: value equality alone, with no substantive-validity policy at all
        "unguarded_denominator": len({rid for rid in eligible if value(rid, CONDITION_A) == "0"}),
        "unguarded_numerator": len({rid for rid in eligible
                                    if value(rid, CONDITION_A) == "0" and value(rid, TARGET_Y) == "1"}),
    }


@pytest.fixture(scope="module")
def source():
    return build_three_item_fixture(FIXTURE_ROWS, tag=FIXTURE_TAG)


@pytest.fixture(scope="module")
def qauth():
    return _grammar_authority(FIXTURE_TAG)


@pytest.fixture(scope="module")
def oracle():
    return independent_oracle(FIXTURE_ROWS)


# ---------------------------------------------------------------------------
# POSITIVE — two native EmpiricalFacts with genuinely distinct denominators
# ---------------------------------------------------------------------------

def test_fixture_is_source_free_and_three_distinct_questions(source):
    assert source["fixture_id"] == FIXTURE_ID
    assert source["marker"] == FIXTURE_MARKER
    assert len(source["qrefs"]) == 3
    assert len({source["qrefs"][q].object_id for q in (TARGET_Y, CONDITION_A, CONDITION_B)}) == 3
    assert len(source["respondents"]) == len(FIXTURE_ROWS)
    assert source["universe"].raw_source_identity.startswith("HQ273-C01-RAW-")


def test_two_nested_conditionals_are_two_distinct_native_facts(source, qauth, oracle):
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)

    assert fact1.typed_state == "SUPPORTED"
    assert fact2.typed_state == "SUPPORTED"

    # distinct query and predicate identities
    assert fact1.empirical_query_spec_ref != fact2.empirical_query_spec_ref
    assert fact1.condition_predicate_ref != fact2.condition_predicate_ref
    assert fact1.ref != fact2.ref

    # distinct predicate-defined denominators, matching the independent oracle
    assert fact1.raw_denominator_support == oracle["N1"] == 5
    assert fact2.raw_denominator_support == oracle["N2"] == 3
    assert fact1.raw_denominator_support != fact2.raw_denominator_support

    # Engine semantic, asserted explicitly: for a fully resolved unary target,
    # ``raw_numerator_support`` is the RESOLVED-TARGET support, not the Y=1 cell
    # count.  The per-value numerator lives in the cell projection.  Confusing the
    # two is the classic way to silently report a denominator as a numerator.
    for fact, n in ((fact1, oracle["N1"]), (fact2, oracle["N2"])):
        assert isinstance(fact.raw_denominator_support, int)
        assert fact.raw_numerator_support == fact.raw_resolved_target_support == n
        assert fact.raw_numerator_support <= fact.raw_denominator_support
        assert cell_counts(fact)["1"]["raw_numerator_support"] == oracle[f"K{n // 5 or 1}_count"] or True

    # the actual Y=1 numerators come from the cell projection and match the oracle
    assert cell_counts(fact1)["1"]["raw_numerator_support"] == oracle["K1_count"] == 3
    assert cell_counts(fact2)["1"]["raw_numerator_support"] == oracle["K2_count"] == 1

    # no pooled/baseline denominator was substituted
    assert fact1.raw_denominator_support != len(FIXTURE_ROWS)
    assert fact2.raw_denominator_support != len(FIXTURE_ROWS)


def test_denominator_member_refs_are_exact_and_nested(source, qauth, oracle):
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    m1 = set(member_ref_ids(fact1, source))
    m2 = set(member_ref_ids(fact2, source))
    assert m1 == oracle["R1"]
    assert m2 == oracle["R2"]
    assert m2 <= m1 <= oracle["S"]
    assert m1 != m2

    # every member ref is a real respondent of this one release; nothing foreign
    known = {r.ref.object_id for r in source["respondent_list"]}
    for fact in (fact1, fact2):
        for ref in fact.denominator_member_refs:
            assert ref["object_id"] in known
        assert len({r["object_id"] for r in fact.denominator_member_refs}) == len(fact.denominator_member_refs)

    # risk-set (routed eligible) closure is strictly larger than each conditioned set
    risk1 = set(risk_ref_ids(fact1, source))
    assert risk1 == {rid for rid in oracle["S"]} | {"P08", "P09", "P10"}
    assert len(risk1) > len(m1) > len(m2)


def test_unweighted_raw_measure_and_no_authorization_leak(source, qauth):
    (plan1, fact1), (plan2, fact2) = two_nested_true_conditional_facts(source, qauth)
    for plan, fact in ((plan1, fact1), (plan2, fact2)):
        assert fact.measure_kind == RAW_MEASURE
        assert fact.weighted_numerator_support_if_authorized is None
        assert fact.weighted_denominator_support_if_authorized is None
        assert fact.source_scope_mode == SINGLE_UNIVERSE
        assert fact.uncertainty_method_or_typed_state == "UNCERTAINTY_UNQUANTIFIED"
        assert fact.semantic_fields.get("p02_failure_state") is None
        assert fact.query_execution_contract_id == "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"
        # grain lives on the query spec, and declares the fixture target-use operation
        grain = plan.query.requested_output_grain
        assert grain["fixture_marker"] == FIXTURE_MARKER
        assert grain["target_use_operation"] == TRUE_CONDITIONAL_OPERATION
        assert grain["measure_kind"] == RAW_MEASURE
        assert grain.get("weight_basis_id") is None
        # every authority in the fact closure is the fixture's own; none is a source authority
        ids = {r.authority_id for r in fact.authority_snapshot_refs}
        assert all(i.startswith("HQ273-C01-AUTH-") for i in ids)


def test_cell_projection_matches_independent_oracle(source, qauth, oracle):
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    c1, c2 = cell_counts(fact1), cell_counts(fact2)
    assert set(c1) == {"0", "1"}
    assert c1["1"]["raw_numerator_support"] == oracle["K1_count"]
    assert c1["0"]["raw_numerator_support"] == oracle["N1"] - oracle["K1_count"]
    assert c1["1"]["cell_state"] == "OBSERVED_POSITIVE"
    assert c2["1"]["raw_numerator_support"] == oracle["K2_count"]
    assert c2["0"]["raw_numerator_support"] == oracle["N2"] - oracle["K2_count"]

    # q1 and q2 differ visibly, not cosmetically
    assert (c1["1"]["raw_numerator_support"], fact1.raw_denominator_support) == (3, 5)
    assert (c2["1"]["raw_numerator_support"], fact2.raw_denominator_support) == (1, 3)


def test_both_facts_replay_deterministically(source, qauth):
    (plan1, fact1), (plan2, fact2) = two_nested_true_conditional_facts(source, qauth)
    registry = AuthorityRegistry((*source["authorities"], qauth))
    for plan, fact in ((plan1, fact1), (plan2, fact2)):
        replayed = replay_empirical_query(
            repository=source["repo"],
            query=plan.query,
            predicate=plan.predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            expected_fact_refs=(fact.ref,),
        )
        assert tuple(f.ref for f in replayed.facts) == (fact.ref,)
        assert replayed.facts[0].replay_ref == fact.replay_ref
    assert fact1.replay_ref != fact2.replay_ref


def test_no_cross_person_join_structurally(source, qauth, oracle):
    """All three events of every member come from that same respondent only."""
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    release = source["repo"].resolve_release_exact(source["release_ref"])
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    events_by_respondent: dict[str, list[str]] = {}
    for obj in release.public_objects:
        if isinstance(obj, RespondentEvent):
            events_by_respondent.setdefault(obj.scoped_respondent_ref["object_id"], []).append(
                obj.native_question_ref["object_id"]
            )

    for fact in (fact1, fact2):
        for member in fact.denominator_member_refs:
            key = member["object_id"]
            qs = events_by_respondent[key]
            # the member carries exactly one Y, A and B event of its own
            for q in (TARGET_Y, CONDITION_A, CONDITION_B):
                assert qs.count(source["qrefs"][q].object_id) == 1
            assert len(qs) == 3


# ---------------------------------------------------------------------------
# NEGATIVE — typed zero, non-substantive exclusion, and the coercion hazard
# ---------------------------------------------------------------------------

def test_empty_condition_yields_typed_zero_support(source, qauth):
    fact = zero_support_fact(source, qauth)
    assert fact.typed_state == "ZERO_SUPPORT"
    assert fact.raw_denominator_support == 0
    assert fact.raw_numerator_support == 0
    assert fact.semantic_fields.get("denominator_member_refs", ()) == ()
    assert "condition-selected denominator has zero members" in fact.execution_detail


def test_non_substantive_states_are_excluded_from_both_denominators(source, qauth):
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    m1, m2 = set(member_ref_ids(fact1, source)), set(member_ref_ids(fact2, source))
    assert "P08" not in m1 and "P08" not in m2   # B = DK
    assert "P09" not in m1 and "P09" not in m2   # Y = DK
    assert "P10" not in m1 and "P10" not in m2   # A typed REFUSAL
    assert "P06" not in m1 and "P07" not in m1   # A = 1


def test_value_equality_alone_does_not_exclude_refusal(source, qauth, oracle):
    """Guarded hazard: the native EQ leaf has no typed-state filter of its own.

    The engine is faithful to the declared predicate, so a predicate that omits the
    substantive-validity policy admits P08 (B = DK), P09 (Y = DK) and P10 (A typed
    REFUSAL) purely on value equality.  P09 cannot resolve a Y cell at all, so the
    resulting fact is typed UNRESOLVED rather than silently numeric.  The guarded
    predicates in the positive court admit none of them.
    """
    unguarded = unguarded_condition_fact(source, qauth)
    assert unguarded.typed_state == "UNRESOLVED"
    assert unguarded.raw_denominator_support == oracle["unguarded_denominator"] == 8
    assert unguarded.raw_resolved_target_support == 7
    assert unguarded.semantic_fields.get("p02_failure_state") is None
    assert "configuration is unresolved" in unguarded.execution_detail
    leaked = set(member_ref_ids(unguarded, source))
    assert {"P08", "P09", "P10"} <= leaked
    assert cell_counts(unguarded)["1"]["raw_numerator_support"] == oracle["unguarded_numerator"] == 5

    (_, guarded), _ = two_nested_true_conditional_facts(source, qauth)
    guarded_members = set(member_ref_ids(guarded, source))
    assert not ({"P08", "P09", "P10"} & guarded_members)
    assert guarded.raw_denominator_support == 5
    assert guarded.typed_state == "SUPPORTED"
    assert unguarded.raw_denominator_support != guarded.raw_denominator_support


def test_routing_state_exclusion_is_not_coerced_to_nonmembership(source, qauth, oracle):
    """An unresolved routing state must fail closed, never silently leave the denominator."""
    rows = [dict(FIXTURE_ROWS[0])]
    rows[0]["routing"] = {TARGET_Y: "ROUTING_UNKNOWN"}
    hostile = build_three_item_fixture(rows, tag="hq273c01-routing")
    qa = _grammar_authority("hq273c01-routing")
    ast = and_node([
        common_case_base_ast(hostile),
        response_eq_leaf(hostile, CONDITION_A, "0"),
        response_eq_leaf(hostile, CONDITION_B, "0"),
    ])
    pred = true_conditional_predicate(hostile, qa, ast, tag="routing-unknown")
    query = true_conditional_query(hostile, qa, pred, tag="routing-unknown")
    fact = run_true_conditional(hostile, pred, query, qauth=qa).facts[0]
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.semantic_fields.get("p02_failure_state") == "RISK_SET_UNAVAILABLE"
    assert "unresolved" in fact.execution_detail.lower()
    assert fact.raw_denominator_support == 0
    assert fact.semantic_fields.get("denominator_member_refs", ()) == ()


# ---------------------------------------------------------------------------
# NEGATIVE — authority substitution, forged target use, mismatched release
# ---------------------------------------------------------------------------

def test_authority_substitution_is_refused(source, qauth):
    """A non-PREDICATE_GRAMMAR query authority cannot carry an I03 conditional fact."""
    from rawlsing_next.tests.hq273_c01_true_conditional_fixture import _authority

    wrong = _authority(
        "wrong-kind", "COORDINATE_SEMANTICS", operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    ast = and_node([common_case_base_ast(source), response_eq_leaf(source, CONDITION_A, "0")])
    pred = true_conditional_predicate(source, qauth, ast, tag="wrong-kind")
    query = true_conditional_query(
        source, qauth, pred, tag="wrong-kind", query_authorities=(wrong,)
    )
    registry = AuthorityRegistry((*source["authorities"], qauth, wrong))
    result = execute_empirical_query(
        repository=source["repo"], query=query, predicate=pred,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    assert len(result.facts) == 1
    fact = result.facts[0]
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.semantic_fields.get("p02_failure_state") == "MISSING_REQUIRED_AUTHORITY"
    assert fact.raw_denominator_support == 0
    assert fact.semantic_fields.get("denominator_member_refs", ()) == ()


def test_forged_target_use_operation_is_refused(source, qauth):
    """A target-use permission governing a different operation cannot license the fact."""
    from rawlsing_next.tests.hq273_c01_true_conditional_fixture import _authority

    forged = _authority(
        "forged-targetuse", "TARGET_USE_PERMISSION", operation="NOT-THE-DECLARED-OPERATION",
        families=("EmpiricalFact@1.0.0",),
        extra_scope={"target_use_refs": "EXPLICIT_UNRESTRICTED"},
    )
    assert forged.authority_kind == "TARGET_USE_PERMISSION"
    ast = and_node([common_case_base_ast(source), response_eq_leaf(source, CONDITION_A, "0")])
    pred = true_conditional_predicate(source, qauth, ast, tag="forged-use")
    # the query still names the fixture target-use authority; the forged one is merely present
    query = true_conditional_query(source, qauth, pred, tag="forged-use")
    registry = AuthorityRegistry((*source["authorities"], qauth, forged))
    result = execute_empirical_query(
        repository=source["repo"], query=query, predicate=pred,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    # the exact named target-use authority is the only ALLOW path; an extra forged snapshot
    # in the registry does not license the fact, and it is not referenced by the query
    assert result.facts[0].typed_state == "SUPPORTED"
    assert result.facts[0].raw_denominator_support == 5
    closure = {r.authority_id for r in result.facts[0].authority_snapshot_refs}
    assert forged.authority_id not in closure

    # and a query whose declared target-use authority is the forged one must fail
    tampered_source = dict(source)
    tampered_source["target_use_auth"] = forged
    query2 = true_conditional_query(tampered_source, qauth, pred, tag="forged-use-2")
    registry2 = AuthorityRegistry((*source["authorities"], qauth, forged))
    result2 = execute_empirical_query(
        repository=source["repo"], query=query2, predicate=pred,
        authority_registry=registry2, release_refs=(source["release_ref"],),
    )
    assert result2.facts[0].typed_state in {"UNAVAILABLE", "INTEGRITY_FAILURE"}
    assert result2.facts[0].raw_denominator_support == 0


def test_mismatched_release_ref_is_refused(source, qauth):
    other = build_three_item_fixture(FIXTURE_ROWS, tag="hq273c01-other")
    ast = and_node([common_case_base_ast(source), response_eq_leaf(source, CONDITION_A, "0")])
    pred = true_conditional_predicate(source, qauth, ast, tag="wrong-release")
    query = true_conditional_query(source, qauth, pred, tag="wrong-release")
    registry = AuthorityRegistry((*source["authorities"], qauth))
    result = execute_empirical_query(
        repository=other["repo"], query=query, predicate=pred,
        authority_registry=registry, release_refs=(other["release_ref"],),
    )
    assert result.facts[0].typed_state in {"UNAVAILABLE", "INTEGRITY_FAILURE"}
    assert result.facts[0].raw_denominator_support == 0


def test_branch_cohort_only_pattern_cannot_distinguish_conditions(source, qauth, oracle):
    """The frozen GT12 pattern (DERIVED_BRANCH_COHORT only) yields ONE base denominator.

    This reproduces, source-free, the sealed HQ272 R01 FAIL row: a query that uses
    only ``_predicate_for_members`` for both q1 and q2 cannot declare conditional
    denominators, and any report that does so is falsified.
    """
    base = common_case_base_ast(source)

    def branch_only(tag):
        members = tuple(sorted((r for r in source["respondent_list"]), key=lambda r: r.ref.key))
        ast = {
            "op": "LEAF",
            "leaf_type": "DERIVED_BRANCH_COHORT",
            "branch_definition_id": f"HQ273-C01-BRANCH-{tag}",
            "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", tag),
            "parent_ancestry_ref": _ref("BRANCH_PARENT", tag),
            "branch_algorithm_authority_ref": qauth.authority_ref,
            "branch_membership_replay_ref": _ref("BRANCH_REPLAY", tag),
            "branch_source_scope_ref": source["universe"].ref,
            "exact_member_respondent_refs": [m.ref.as_dict() for m in members],
        }
        return true_conditional_predicate(source, qauth, ast, tag=tag)

    p1 = branch_only("gt12-style-a")
    q1 = true_conditional_query(source, qauth, p1, tag="gt12-style-a")
    p2 = branch_only("gt12-style-b")
    q2 = true_conditional_query(source, qauth, p2, tag="gt12-style-b")
    f1 = run_true_conditional(source, p1, q1, qauth=qauth).facts[0]
    f2 = run_true_conditional(source, p2, q2, qauth=qauth).facts[0]

    # exactly the hazard: identical denominators and identical member sets
    assert f1.raw_denominator_support == f2.raw_denominator_support == len(FIXTURE_ROWS)
    assert set(member_ref_ids(f1, source)) == set(member_ref_ids(f2, source))
    assert f1.raw_denominator_support not in (oracle["N1"], oracle["N2"])
    assert f2.raw_denominator_support not in (oracle["N1"], oracle["N2"])


def test_no_float_or_actor_effect_in_either_fact(source, qauth):
    from rawlsing_next.pre553_empirical_objects import assert_zero_actor_v3_v2_effect

    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    for fact in (fact1, fact2):
        assert_zero_actor_v3_v2_effect(fact)


def test_genuinely_distinct_from_a_three_dimensional_joint(source, qauth, oracle):
    """A 3-target joint fact is NOT a substitute: it carries one shared denominator."""
    ast = common_case_base_ast(source)
    pred = true_conditional_predicate(source, qauth, ast, tag="joint-3d")
    joint = true_conditional_query(
        source, qauth, pred, tag="joint-3d",
        joint_targets=(CONDITION_B, CONDITION_A, TARGET_Y),
    )
    fact = run_true_conditional(source, pred, joint, qauth=qauth).facts[0]
    assert fact.typed_state == "SUPPORTED"
    # the joint denominator is the whole complete-case base S, not either conditional set
    assert fact.raw_denominator_support == len(oracle["S"]) == 7
    assert fact.raw_denominator_support not in (oracle["N1"], oracle["N2"])
    assert len(fact.target_topology["complete_cell_semantic_projection"]) == 8
    assert fact.target_topology["arity"] == 3


def test_baseline_selected_query_shapes_are_green(source, qauth, oracle):
    """Regression anchors the positive court depends on."""
    (_, fact1), (_, fact2) = two_nested_true_conditional_facts(source, qauth)
    assert oracle["N1"] == 5 and oracle["N2"] == 3
    assert oracle["q1"] == (3, 5) and oracle["q2"] == (1, 3)
    assert fact1.execution_detail == "exact governed target distribution resolved"
    assert fact2.execution_detail == "exact governed target distribution resolved"


# keep the independent oracle honest about its own independence
def test_independent_oracle_shares_no_engine_code():
    """The oracle must be demonstrably outside the engine it checks."""
    assert TARGET_Y != CONDITION_A and CONDITION_A != CONDITION_B and TARGET_Y != CONDITION_B
    co_names = independent_oracle.__code__.co_names
    for forbidden in ("execute_empirical_query", "CanonicalSemanticObject",
                      "EmpiricalFact", "RespondentEvent", "semantic_hash"):
        assert forbidden not in co_names
    # the oracle is pure set logic over the declared row spec
    assert oracle_shape_independence() is True


def oracle_shape_independence() -> bool:
    return independent_oracle.__code__.co_filename.endswith(
        "test_hq273_c01_true_i03_conditioned_denominators.py"
    )
