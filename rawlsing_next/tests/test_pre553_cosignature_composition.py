from __future__ import annotations

import pytest

from rawlsing_next.pre553_cosignature_composition import (
    CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J,
    BranchCosignatureContext,
    CosignatureCompositionError,
    CosignatureCompositionPolicy,
    ExecutedCosignatureQuery,
    compose_branch_cosignatures,
    enumerate_target_tuples,
    seal_branch_cosignature_closure,
)
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, exact_ref
from rawlsing_next.pre553_empirical_query import QueryExecutionResult
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _query_authority as _base_query_authority,
    _ref,
    _registry,
)


def _query_authority(tag):
    return _base_query_authority(tag, max_target_arity_J=3)


def _context(source, qauth, *, members=None, tag="branch"):
    predicate = _branch_predicate(source, qauth, members=members, tag=tag)
    ast = predicate.predicate_ast
    parent = exact_ref(ast["parent_ancestry_ref"])
    return BranchCosignatureContext(
        branch_predicate=predicate,
        branch_replay_ref=exact_ref(ast["branch_membership_replay_ref"]),
        immediate_parent_ref=parent,
        ancestry_refs=(parent,),
        source_release_refs=(source["release_ref"],),
        universe_refs=(source["universe"].ref,),
        risk_set_ref=source["risk_refs"]["R"],
    )


def _policy(source, qauth, *, measure="RAW"):
    return CosignatureCompositionPolicy(
        topology_authority_ref=source["source_auth"].authority_ref,
        query_authority_refs=(qauth.authority_ref,),
        authority_maximum_target_arity_J=3,
        measure_kind=measure,
        measure_basis_ref=_ref("MEASURE_BASIS", measure),
        response_state_semantics_ref=_ref(
            "RESPONSE_STATE_SEMANTICS", "SOURCE_NATIVE_TYPED_STATES"
        ),
        weight_basis_id="W" if measure == "GOVERNED_WEIGHTED" else None,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
    )


def _compose(source, qauth, *, members=None, tag="branch", measure="RAW"):
    context = _context(source, qauth, members=members, tag=tag)
    result = compose_branch_cosignatures(
        repository=source["repo"],
        context=context,
        authority_registry=_registry(source, qauth),
        policy=_policy(source, qauth, measure=measure),
    )
    return context, result


def _cells(fact):
    return {
        str(row["cell"]): row["raw_numerator_support"]
        for row in fact.target_topology["complete_cell_semantic_projection"]
    }


def _rates(fact):
    denominator = fact.semantic_fields["raw_resolved_target_support"]
    return {key: (value, denominator) for key, value in _cells(fact).items()}


def test_branch_relation_differs_from_overall_even_when_target_marginals_match():
    rows = [
        {"id": "R1", "responses": {"Y": 0, "Z": 0}},
        {"id": "R2", "responses": {"Y": 0, "Z": 0}},
        {"id": "R3", "responses": {"Y": 1, "Z": 1}},
        {"id": "R4", "responses": {"Y": 1, "Z": 1}},
        {"id": "R5", "responses": {"Y": 0, "Z": 1}},
        {"id": "R6", "responses": {"Y": 0, "Z": 1}},
        {"id": "R7", "responses": {"Y": 1, "Z": 0}},
        {"id": "R8", "responses": {"Y": 1, "Z": 0}},
    ]
    source = _build_source("i04-branch-vs-overall", rows)
    qauth = _query_authority("i04-branch-vs-overall-q")
    branch_members = tuple(
        source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4")
    )

    _, branch = _compose(
        source, qauth, members=branch_members, tag="minority-shaped-branch"
    )
    _, overall = _compose(source, qauth, tag="overall")

    branch_y = next(
        item.fact for item in branch.marginal_queries
        if item.target_refs == (source["qrefs"]["Y"],)
    )
    overall_y = next(
        item.fact for item in overall.marginal_queries
        if item.target_refs == (source["qrefs"]["Y"],)
    )
    branch_z = next(
        item.fact for item in branch.marginal_queries
        if item.target_refs == (source["qrefs"]["Z"],)
    )
    overall_z = next(
        item.fact for item in overall.marginal_queries
        if item.target_refs == (source["qrefs"]["Z"],)
    )

    assert {
        key: value / denom for key, (value, denom) in _rates(branch_y).items()
    } == {
        key: value / denom for key, (value, denom) in _rates(overall_y).items()
    }
    assert {
        key: value / denom for key, (value, denom) in _rates(branch_z).items()
    } == {
        key: value / denom for key, (value, denom) in _rates(overall_z).items()
    }

    branch_joint = branch.joint_for(source["qrefs"]["Y"], source["qrefs"]["Z"]).fact
    overall_joint = overall.joint_for(source["qrefs"]["Y"], source["qrefs"]["Z"]).fact
    assert _cells(branch_joint) != _cells(overall_joint)
    assert branch_joint.ref != overall_joint.ref
    assert (
        branch.closure_receipt.branch_predicate_ref
        != overall.closure_receipt.branch_predicate_ref
    )


def test_minority_branch_preserved_complete_frontier_has_no_reachability_ranking():
    source = _build_source(
        "i04-minority",
        [
            {"id": "R1", "responses": {"A": 1, "B": 1, "C": 0}},
            {"id": "R2", "responses": {"A": 0, "B": 0, "C": 1}},
            {"id": "R3", "responses": {"A": 0, "B": 1, "C": 1}},
            {"id": "R4", "responses": {"A": 1, "B": 0, "C": 0}},
            {"id": "R5", "responses": {"A": 0, "B": 0, "C": 0}},
        ],
    )
    qauth = _query_authority("i04-minority-q")
    _, result = _compose(
        source, qauth, members=(source["respondents"]["R1"],), tag="one-member"
    )
    assert result.target_catalog.target_count == 3
    assert result.closure_receipt.target_count == 3
    assert result.closure_receipt.expected_pair_count == 3
    assert result.closure_receipt.evaluated_pair_count == 3
    assert result.closure_receipt.expected_triple_count == 1
    assert result.closure_receipt.evaluated_triple_count == 1
    assert result.closure_receipt.maximum_completed_target_arity_J == 3
    assert len(result.marginal_queries) == 3
    assert len(result.joint_queries) == 3
    assert len(result.triple_queries) == 1
    assert (
        result.target_catalog.semantic_projection()["ranking_controls_reachability"]
        is False
    )
    assert all(item.fact.raw_denominator_support == 1 for item in result.marginal_queries)
    assert all(item.fact.raw_denominator_support == 1 for item in result.joint_queries)
    assert all(item.fact.raw_denominator_support == 1 for item in result.triple_queries)


def test_caller_cannot_inject_target_winner_or_partial_target_frontier():
    source = _build_source(
        "i04-no-winner",
        [
            {"id": "R1", "responses": {"A": 1, "B": 1, "C": 1, "D": 0}},
            {"id": "R2", "responses": {"A": 1, "B": 1, "C": 0, "D": 1}},
            {"id": "R3", "responses": {"A": 0, "B": 0, "C": 1, "D": 1}},
            {"id": "R4", "responses": {"A": 0, "B": 0, "C": 0, "D": 0}},
        ],
    )
    qauth = _query_authority("i04-no-winner-q")
    context = _context(source, qauth)
    kwargs = {
        "repository": source["repo"],
        "context": context,
        "authority_registry": _registry(source, qauth),
        "policy": _policy(source, qauth),
    }
    result = compose_branch_cosignatures(**kwargs)
    assert result.target_catalog.target_count == 4
    assert result.closure_receipt.expected_pair_count == 6
    assert result.closure_receipt.expected_triple_count == 4
    assert len(result.joint_queries) == 6
    assert len(result.triple_queries) == 4
    with pytest.raises(TypeError):
        compose_branch_cosignatures(
            **kwargs,
            target_refs=(source["qrefs"]["B"],),  # type: ignore[call-arg]
        )


def test_demographic_coordinate_explicitly_excluded_and_rejected_as_target():
    source = _build_source(
        "i04-demographic-reject",
        [
            {"id": "R1", "responses": {"A": 1, "B": 0}, "coords": {"GENDER": "F"}},
            {"id": "R2", "responses": {"A": 0, "B": 1}, "coords": {"GENDER": "M"}},
        ],
    )
    qauth = _query_authority("i04-demographic-reject-q")
    _, result = _compose(source, qauth)
    coordinate_ref = source["crefs"]["GENDER"]
    assert coordinate_ref not in tuple(
        target.target_ref for target in result.target_catalog.targets
    )
    reasons = {
        item.target_ref.key: item.reason for item in result.target_catalog.exclusions
    }
    assert reasons[coordinate_ref.key] == "POSITIONAL_COORDINATE__NOT_COSIGNATURE_TARGET"
    with pytest.raises(CosignatureCompositionError):
        result.target_catalog.require_target(coordinate_ref)


def test_denominator_substitution_rejected_before_topology_closure():
    source = _build_source(
        "i04-denominator",
        [
            {"id": "R1", "responses": {"A": 1, "B": 1}},
            {"id": "R2", "responses": {"A": 0, "B": 0}},
            {"id": "R3", "responses": {"A": 1, "B": 0}},
            {"id": "R4", "responses": {"A": 0, "B": 1}},
        ],
    )
    qauth = _query_authority("i04-denominator-q")
    members = (source["respondents"]["R1"], source["respondents"]["R2"])
    context, result = _compose(source, qauth, members=members, tag="half")

    original = result.marginal_queries[0]
    fact = original.fact
    risk_members = fact.semantic_fields["risk_set_member_refs"]
    denominator_members = fact.semantic_fields["denominator_member_refs"]
    assert len(risk_members) == 4
    assert len(denominator_members) == 2

    fields = dict(fact.semantic_fields)
    fields["raw_denominator_support"] = len(risk_members)
    tampered = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fields,
    )
    tampered_result = QueryExecutionResult(
        query_ref=original.query.ref,
        facts=(tampered,),
        source_scope_mode=original.result.source_scope_mode,
        release_refs=original.result.release_refs,
    )
    tampered_executed = ExecutedCosignatureQuery(
        target_refs=original.target_refs,
        query=original.query,
        result=tampered_result,
    )
    with pytest.raises(CosignatureCompositionError, match="raw denominator"):
        seal_branch_cosignature_closure(
            repository=source["repo"],
            context=context,
            catalog=result.target_catalog,
            policy=_policy(source, qauth),
            marginals=(tampered_executed, *result.marginal_queries[1:]),
            joints=result.joint_queries,
            triples=result.triple_queries,
            authority_registry=_registry(source, qauth),
        )


def test_integrated_j3_executes_direct_exact_three_way_topology_and_j4_stays_closed():
    source = _build_source(
        "i04-j-guard",
        [
            {"id": "R1", "responses": {"A": 0, "B": 0, "C": 0}},
            {"id": "R2", "responses": {"A": 0, "B": 1, "C": 1}},
            {"id": "R3", "responses": {"A": 1, "B": 0, "C": 1}},
            {"id": "R4", "responses": {"A": 1, "B": 1, "C": 0}},
        ],
    )
    qauth = _query_authority("i04-j-guard-q")
    _, result = _compose(source, qauth)
    assert CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J == 3
    assert len(result.triple_queries) == 1
    triple = result.triple_queries[0]
    fact = triple.fact
    assert fact.target_topology["higher_order_evidence_semantics"] == "DIRECT_EXACT_SAME_RESPONDENT_THREE_WAY_JOINT"
    assert fact.target_topology["pairwise_projection_not_identity_equivalent"] is True
    assert fact.target_topology["authority37_j3_denominators"]["contract"] == "AUTHORITY37_J3_DENOMINATOR_CONSERVATION@1.0.0"
    assert result.closure_receipt.expected_triple_count == 1
    assert result.closure_receipt.evaluated_triple_count == 1
    assert result.closure_receipt.coverage_state == "COMPLETE_FOR_AUTHORIZED_J1_TO_J3_TARGET_FRONTIER"
    with pytest.raises(CosignatureCompositionError, match="exceeds exact authority"):
        enumerate_target_tuples(
            result.target_catalog,
            requested_arity=4,
            authority_maximum_target_arity_J=3,
            executor_maximum_target_arity_J=CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J,
        )


def test_deterministic_replay_and_closure_identity_survive_storage_permutation():
    rows = [
        {"id": "R1", "responses": {"A": 0, "B": 0, "C": 1}},
        {"id": "R2", "responses": {"A": 0, "B": 1, "C": 0}},
        {"id": "R3", "responses": {"A": 1, "B": 0, "C": 0}},
        {"id": "R4", "responses": {"A": 1, "B": 1, "C": 1}},
    ]
    left = _build_source("i04-replay", rows)
    right = _build_source("i04-replay", rows, reverse_sections=True)
    qauth = _query_authority("i04-replay-q")
    _, a = _compose(
        left, qauth,
        members=(left["respondents"]["R1"], left["respondents"]["R4"]),
        tag="same-branch",
    )
    _, b = _compose(
        right, qauth,
        members=(right["respondents"]["R1"], right["respondents"]["R4"]),
        tag="same-branch",
    )
    assert left["release_ref"] == right["release_ref"]
    assert a.target_catalog.ref == b.target_catalog.ref
    assert tuple(item.query.ref for item in a.marginal_queries) == tuple(
        item.query.ref for item in b.marginal_queries
    )
    assert tuple(item.fact.ref for item in a.marginal_queries) == tuple(
        item.fact.ref for item in b.marginal_queries
    )
    assert tuple(item.query.ref for item in a.joint_queries) == tuple(
        item.query.ref for item in b.joint_queries
    )
    assert tuple(item.fact.ref for item in a.joint_queries) == tuple(
        item.fact.ref for item in b.joint_queries
    )
    assert tuple(item.query.ref for item in a.triple_queries) == tuple(
        item.query.ref for item in b.triple_queries
    )
    assert tuple(item.fact.ref for item in a.triple_queries) == tuple(
        item.fact.ref for item in b.triple_queries
    )
    assert a.closure_receipt.ref == b.closure_receipt.ref
    assert a.closure_receipt.replay_ref == b.closure_receipt.replay_ref


def test_raw_and_weighted_support_remain_distinct_without_payload_copy():
    source = _build_source(
        "i04-weighted",
        [
            {"id": "R1", "responses": {"A": 1, "B": 1}},
            {"id": "R2", "responses": {"A": 0, "B": 0}},
        ],
        weights={
            "R1": ("WEIGHT_VALID_AUTHORIZED", "2"),
            "R2": ("WEIGHT_VALID_AUTHORIZED", "1"),
        },
    )
    qauth = _query_authority("i04-weighted-q")
    _, raw = _compose(source, qauth, measure="RAW", tag="weighted-branch")
    _, weighted = _compose(
        source, qauth, measure="GOVERNED_WEIGHTED", tag="weighted-branch"
    )
    raw_joint = raw.joint_for(source["qrefs"]["A"], source["qrefs"]["B"]).fact
    weighted_joint = weighted.joint_for(
        source["qrefs"]["A"], source["qrefs"]["B"]
    ).fact
    assert raw_joint.ref != weighted_joint.ref
    assert raw_joint.weighted_denominator_support_if_authorized is None
    assert weighted_joint.weighted_denominator_support_if_authorized is not None
    assert not raw.closure_receipt.measure_authority_refs
    assert weighted.closure_receipt.measure_authority_refs
    closure = weighted.closure_receipt.semantic_projection()
    assert closure["copied_empirical_payload"] is False
    assert "complete_cell_semantic_projection" not in closure
