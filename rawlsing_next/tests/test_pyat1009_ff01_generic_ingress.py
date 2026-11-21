"""PYAT #1009: actual native I03 -> generic FF01 descriptive SOURCEFREE consumer.

The fixture calls the protected C11Repository/I03 owners, not a fabricated
precomputed joint.  It is NOT a persisted cold estate or independent G5 court.
"""
from dataclasses import replace
from itertools import product

import pytest

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, semantic_hash
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError,
    execute_ff01_observed_joint,
    receive_ff01_observed_joint,
    replay_ff01_observed_joint,
)
from rawlsing_next.tests import test_pre553_empirical_query as native


PERMISSIONS = ("FF01_DESCRIPTIVE_SOURCEFREE",)


def _case(parity: int = 0, *, tag="FF01-GENERIC"):
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
        for x, y in product((0, 1), repeat=2)
    ]
    source = native._build_source(tag, rows, question_namespace="FF01-SHARED")
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("X", "Y", "Z"), tag=tag)
    result = native._run(source, qauth, predicate, query)
    assert len(result.facts) == 1
    assert result.facts[0].typed_state == "SUPPORTED"
    return source, qauth, predicate, query, result


def _receive(query, result, **kw):
    return receive_ff01_observed_joint(
        execution=result, query=query,
        conditioner_index=kw.pop("conditioner_index", 0),
        producer_permission_ceiling=kw.pop("producer_permission_ceiling", PERMISSIONS),
        **kw,
    )


def _replace_fact(fact, **fields):
    material = dict(fact.semantic_fields)
    material.update(fields)
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **material,
    )


def _changed_result(result: QueryExecutionResult, **fields):
    return replace(result, facts=(_replace_fact(result.facts[0], **fields),))


def _cell_count(received, *states):
    material = received.semantic_projection()
    return next(
        row["raw_support"] for row in material["complete_cells"]
        if row["cell"] == list(states)
    )


def test_actual_native_three_way_i03_consumed_without_synthetic_pairwise_joint():
    _, _, _, query, result = _case()
    received = _receive(query, result)
    p = received.semantic_projection()
    assert p["joint_arity"] == 3
    assert len(p["complete_cells"]) == 8
    assert p["raw_eligible_condition_denominator"] == 4
    assert p["raw_fully_resolved_joint_n"] == 4
    assert p["producer_fact_ref"] == result.facts[0].ref.as_dict()
    assert p["source_permission_grade"] == "CALLER_DECLARED__NOT_INDEPENDENTLY_ISSUED"
    assert _cell_count(received, "0", "0", "0") == 1
    assert _cell_count(received, "0", "0", "1") == 0
    assert sum(row["fully_resolved_condition_n"] for row in p["conditioned_complete_case_support"]) == 4
    assert "N10E_V3_ACTOR_NOT_CONSUMED_HERE" in p["not_proven"]


def test_same_pairwise_marginals_but_opposite_triples_survive_at_real_ff01_reader():
    # The parity and anti-parity populations agree on all unary/pairwise
    # marginals while the 3-way joint changes.
    _, _, _, q0, r0 = _case(0, tag="FF01-PARITY")
    _, _, _, q1, r1 = _case(1, tag="FF01-ANTIPARITY")
    left, right = _receive(q0, r0), _receive(q1, r1)
    assert _cell_count(left, "0", "0", "0") == 1
    assert _cell_count(right, "0", "0", "0") == 0
    assert left.ref != right.ref


def test_direct_I03_execution_is_one_real_producer_and_no_learned_gate():
    source, qa, predicate, query, _ = _case()
    observed = execute_ff01_observed_joint(
        repository=source["repo"],
        query=query, predicate=predicate,
        authority_registry=native._registry(source, qa),
        release_refs=(source["release_ref"],),
        conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    )
    assert observed.semantic_projection()["joint_arity"] == 3
    assert observed.semantic_projection()["producer_state"] == "SUPPORTED"


def test_choice_of_actual_conditioner_changes_profile_without_requerying_source():
    _, _, _, query, result = _case()
    a = _receive(query, result, conditioner_index=0)
    b = _receive(query, result, conditioner_index=2)
    assert a.ref != b.ref
    assert a.semantic_projection()["conditioner_ref"] == query.target_refs[0]
    assert b.semantic_projection()["conditioner_ref"] == query.target_refs[2]
    assert all(
        sum(row["raw_support"] for row in group["remaining_joint_cells"])
        == group["fully_resolved_condition_n"]
        for group in b.semantic_projection()["conditioned_complete_case_support"]
    )


def test_source_mutation_changes_ff01_result_and_exact_replay_refuses_old():
    _, _, _, q0, r0 = _case(0, tag="FF01-SOURCE-CHANGE")
    _, _, _, q1, r1 = _case(1, tag="FF01-SOURCE-CHANGE")
    old = _receive(q0, r0)
    changed = _receive(q1, r1)
    assert old.ref != changed.ref
    assert replay_ff01_observed_joint(
        old.ref, execution=r0, query=q0, conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    ).ref == old.ref
    with pytest.raises(FF01GenericIngressError, match="replay|changed"):
        replay_ff01_observed_joint(
            old.ref, execution=r1, query=q1, conditioner_index=0,
            producer_permission_ceiling=PERMISSIONS,
        )


def test_untrusted_export_cannot_mutate_hash_identified_ff01_result():
    _, _, _, query, result = _case()
    original = _receive(query, result)
    out = original.semantic_projection()
    out["complete_cells"][0]["raw_support"] = 1_000_000
    assert original.semantic_projection()["complete_cells"][0]["raw_support"] != 1_000_000
    assert original.ref == _receive(query, result).ref


def test_permission_ceiling_cannot_widen_into_causal_use():
    _, _, _, query, result = _case()
    # The protected-use filter may reject first; the assertion tests denial,
    # not incidental ordering or wording of two independent fail-closed guards.
    with pytest.raises(FF01GenericIngressError, match="protected use|widen"):
        _receive(query, result, relation_permission_ceiling=("STRONG_CAUSAL",))
    # Exercise the separate strict-subset guard with otherwise lawful labels.
    with pytest.raises(FF01GenericIngressError, match="widen"):
        _receive(query, result, relation_permission_ceiling=(
            "FF01_DESCRIPTIVE_SOURCEFREE", "FF01_DIAGNOSTIC_READ_ONLY",
        ))
    accepted = _receive(query, result, relation_permission_ceiling=PERMISSIONS)
    assert accepted.semantic_projection()["relation_permission_ceiling"] == list(PERMISSIONS)


def test_fact_query_risk_and_universe_substitutions_are_rejected():
    _, _, _, query, result = _case()
    wrong = ExactRef("RISK_SET", "urn:test:foreign-risk", semantic_hash("foreign-risk"))
    bad = _changed_result(result, risk_set_ref=wrong)
    with pytest.raises(FF01GenericIngressError, match="risk"):
        _receive(query, bad)
    bad = _changed_result(result, empirical_universe_refs=(wrong,))
    with pytest.raises(FF01GenericIngressError, match="universe"):
        _receive(query, bad)


def test_complete_cell_omission_and_zero_as_positive_are_rejected():
    _, _, _, query, result = _case()
    fact = result.facts[0]
    topology = dict(fact.target_topology)
    cells = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    topology["complete_cell_semantic_projection"] = cells[:-1]
    with pytest.raises(FF01GenericIngressError, match="incomplete"):
        _receive(query, _changed_result(result, target_topology=topology))
    cells = [dict(row) for row in fact.target_topology["complete_cell_semantic_projection"]]
    zero = next(row for row in cells if row["raw_numerator_support"] == 0)
    zero["cell_state"] = "OBSERVED_POSITIVE"
    topology["complete_cell_semantic_projection"] = cells
    with pytest.raises(FF01GenericIngressError, match="cell status"):
        _receive(query, _changed_result(result, target_topology=topology))


def test_missing_producer_provenance_and_release_are_not_accepted():
    _, _, _, query, result = _case()
    wrong = ExactRef("RELEASE", "urn:test:foreign-release", semantic_hash("release"))
    with pytest.raises(FF01GenericIngressError, match="release"):
        _receive(query, replace(result, release_refs=(wrong,)))
    with pytest.raises(FF01GenericIngressError, match="evidence"):
        _receive(query, _changed_result(result, source_empirical_provenance_refs=()))


def test_raw_measurement_cannot_carry_weighted_joint_cell():
    _, _, _, query, result = _case()
    topology = dict(result.facts[0].target_topology)
    cells = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    cells[0]["weighted_numerator_support_if_authorized"] = {"$exact_fraction": [1, 1]}
    topology["complete_cell_semantic_projection"] = cells
    with pytest.raises(FF01GenericIngressError, match="RAW weight"):
        _receive(query, _changed_result(result, target_topology=topology))


def test_ordered_scalar_components_only_not_implicit_repetition_collapse():
    _, _, _, query, result = _case()
    assert _receive(query, result).semantic_projection()["joint_order_semantics"] == "SEMANTIC_ORDERED"
    assert tuple(ref["object_id"] for ref in _receive(query, result).semantic_projection()["target_refs"]) == tuple(
        ref["object_id"] for ref in query.target_refs
    )


@pytest.mark.parametrize("mutation", [
    "duplicate_denominator", "duplicate_risk", "foreign_denominator",
    "wrong_kind", "denominator_short", "risk_only", "denominator_only",
])
def test_adversarial_respondent_roster_closure_not_washed_out(mutation):
    # These are re-signed *I03-shaped* facts, not an imaginary FF01 count
    # table. A self-consistent but fictional roster still requires source trust.
    _, _, _, query, result = _case(tag="FF01-ROSTER-HOSTILE")
    fact = result.facts[0]
    risk = list(getattr(fact, "risk_set_member_refs"))
    denominator = list(getattr(fact, "denominator_member_refs"))
    assert risk and denominator
    if mutation == "duplicate_denominator":
        denominator[1] = denominator[0]
    elif mutation == "duplicate_risk":
        risk[1] = risk[0]
    elif mutation == "foreign_denominator":
        denominator[0] = ExactRef(
            "C11Internal:RespondentIdentity",
            "urn:test:alien-respondent",
            semantic_hash("alien-respondent"),
        )
    elif mutation == "wrong_kind":
        denominator[0] = ExactRef(
            "RespondentEvent@1.0.0",
            "urn:test:wrong-respondent-family",
            semantic_hash("wrong-respondent-family"),
        )
    elif mutation == "denominator_short":
        denominator.pop()
    fields = {"risk_set_member_refs": tuple(risk), "denominator_member_refs": tuple(denominator)}
    if mutation == "risk_only":
        fields["denominator_member_refs"] = None
    elif mutation == "denominator_only":
        fields["risk_set_member_refs"] = None
    bad = _changed_result(result, **fields)
    with pytest.raises(FF01GenericIngressError, match="respondent|denominator"):
        _receive(query, bad)


def test_actual_native_roster_is_labeled_internally_consistent_not_independently_issued():
    _, _, _, query, result = _case(tag="FF01-ROSTER-GRADE")
    received = _receive(query, result)
    assert (received.semantic_projection()["respondent_extent_grade"]
            == "INTERNALLY_CONSISTENT_I03_ENUMERATION__SOURCE_AUTHORITY_UNVERIFIED")


def test_false_supported_all_zero_joint_cannot_be_promoted():
    _, _, _, query, result = _case(tag="FF01-FALSE-SUPPORTED")
    fact = result.facts[0]
    top = dict(fact.target_topology)
    cells = [dict(row) for row in top["complete_cell_semantic_projection"]]
    for row in cells:
        row["raw_numerator_support"] = 0
        row["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    top["complete_cell_semantic_projection"] = cells
    bad = _changed_result(
        result, target_topology=top,
        raw_numerator_support=0, raw_resolved_target_support=0,
    )
    with pytest.raises(FF01GenericIngressError, match="zero resolved joint"):
        _receive(query, bad)


def test_falsified_empty_issuer_cannot_self_sign_as_genuine_ff01_research():
    _, _, _, query, result = _case(tag="FF01-EMPTY-ISSUER")
    assert query.query_authority_refs
    # Query and fact are both hash-coherent, but have no operation issuer.
    changed_query = native.EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        **{**dict(query.semantic_fields), "query_authority_refs": ()},
    )
    changed_fact = _replace_fact(
        result.facts[0], empirical_query_spec_ref=changed_query.ref,
    )
    # Rebind exact query dependency rather than accidentally passing only due
    # to a stale ref, to reach the authority-issuance test itself.
    old = result.facts[0]
    changed_fact = EmpiricalFact(
        typed_state=changed_fact.typed_state,
        authority_snapshot_refs=changed_fact.authority_snapshot_refs,
        dependency_refs=tuple(changed_query.ref if v == query.ref else v for v in old.dependency_refs),
        producer_replay_locator_or_reference_root=changed_fact.producer_replay_locator_or_reference_root,
        **dict(changed_fact.semantic_fields),
    )
    with pytest.raises(FF01GenericIngressError, match="issuer|authority|query"):
        _receive(changed_query, replace(result, query_ref=changed_query.ref, facts=(changed_fact,)))


def test_negative_state_cannot_hide_positive_cell_evidence():
    _, _, _, query, result = _case(tag="FF01-TYPED-NEGATIVE-ATTACK")
    previous = result.facts[0]
    changed = dict(previous.semantic_fields)
    changed["raw_numerator_support"] = 0
    changed["raw_resolved_target_support"] = 0
    retagged = EmpiricalFact(
        typed_state="UNRESOLVED",
        authority_snapshot_refs=previous.authority_snapshot_refs,
        dependency_refs=previous.dependency_refs,
        producer_replay_locator_or_reference_root=previous.producer_replay_locator_or_reference_root,
        **changed,
    )
    with pytest.raises(FF01GenericIngressError, match="contradictory positive cell"):
        _receive(query, replace(result, facts=(retagged,)))


def test_forged_condition_subset_cannot_retain_more_resolved_cells_than_denominator():
    _, _, _, query, result = _case(tag="FF01-ROSTER-SUBSET")
    fact = result.facts[0]
    risk = list(fact.risk_set_member_refs)
    denominator = list(fact.denominator_member_refs)
    assert len(risk) == len(denominator) == 4
    # Internally consistent sourcefree conditional subset need not equal the
    # full eligible risk enumeration. This is NOT a source-native authority.
    reduced = _changed_result(
        result,
        denominator_member_refs=tuple(denominator[:3]),
        raw_denominator_support=3,
        raw_numerator_support=3,
        raw_resolved_target_support=3,
    )
    # Four resolved cells cannot legitimately survive a three-member
    # denominator: first ensure this contradiction is refused.
    with pytest.raises(FF01GenericIngressError, match="joint count"):
        _receive(query, reduced)


def test_genuine_native_condition_selected_denominator_subset_is_accepted():
    source, qauth, _, _, _ = _case(tag="FF01-GENUINE-SUBSET")
    members = (source["respondents"]["R00"], source["respondents"]["R10"])
    predicate = native._branch_predicate(
        source, qauth, members=members, tag="TWO-OF-FOUR",
    )
    query = native._query(source, qauth, predicate, ("X", "Y", "Z"), tag="subset")
    result = native._run(source, qauth, predicate, query)
    assert result.facts[0].typed_state == "SUPPORTED"
    assert result.facts[0].raw_denominator_support == 2
    received = _receive(query, result)
    assert received.semantic_projection()["raw_eligible_condition_denominator"] == 2
    assert received.semantic_projection()["raw_fully_resolved_joint_n"] == 2


def test_actual_pairwise_i03_marginals_identical_while_triples_differ():
    left_source, left_qa, left_pred, left_query, left_triple = _case(
        parity=0, tag="FF01-XOR-EQUAL-PAIR",
    )
    right_source, right_qa, right_pred, right_query, right_triple = _case(
        parity=1, tag="FF01-XNOR-EQUAL-PAIR",
    )
    assert _receive(left_query, left_triple).ref != _receive(right_query, right_triple).ref
    for targets in (("X", "Y"), ("X", "Z"), ("Y", "Z")):
        lhs = native._run(
            left_source, left_qa, left_pred,
            native._query(left_source, left_qa, left_pred, targets, tag="pair"),
        ).facts[0]
        rhs = native._run(
            right_source, right_qa, right_pred,
            native._query(right_source, right_qa, right_pred, targets, tag="pair"),
        ).facts[0]
        left_cells = {
            tuple(row["cell"]): row["raw_numerator_support"]
            for row in lhs.target_topology["complete_cell_semantic_projection"]
        }
        right_cells = {
            tuple(row["cell"]): row["raw_numerator_support"]
            for row in rhs.target_topology["complete_cell_semantic_projection"]
        }
        assert left_cells == right_cells


def test_sourcefree_caller_cannot_mint_strong_causal_or_actor_permission():
    _, _, _, query, result = _case(tag="FF01-NO-CALLER-CAUSAL")
    for forbidden in ("STRONG_CAUSAL", "FF02_MATERIAL_POWER", "V3_ACTOR_AUTHORITY", "SOROK_WORLD"):
        with pytest.raises(FF01GenericIngressError, match="protected use"):
            _receive(query, result, producer_permission_ceiling=(forbidden,))


def test_new_generic_supported_ingress_requires_actual_i03_respondent_enumeration():
    _, _, _, query, result = _case(tag="FF01-NO-ROSTER")
    invalid = _changed_result(
        result, risk_set_member_refs=None, denominator_member_refs=None,
    )
    with pytest.raises(FF01GenericIngressError, match="missing both respondent"):
        _receive(query, invalid)


def test_no_duplicate_question_position_can_masquerade_as_three_independent_dimensions():
    from rawlsing_next.field_forge_generic_empirical_ingress import _domain
    _, _, _, query, _ = _case(tag="FF01-DUPLICATE-DIMENSION")
    fields = dict(query.semantic_fields)
    refs = list(query.target_refs)
    components = dict(query.target_arity_and_topology)
    comps = [dict(row) for row in components["components"]]
    refs[2] = refs[0]
    comps[2] = comps[0]
    fields["target_refs"] = refs
    fields["target_arity_and_topology"] = {**components, "components": comps}
    duplicate = native.EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        **fields,
    )
    with pytest.raises(FF01GenericIngressError, match="duplicate target ref"):
        _domain(duplicate)


def test_held_positive_low_support_is_conserved_but_never_promoted_to_ff01_joint():
    _, _, _, query, result = _case(tag="FF01-HELD-LOW-SUPPORT")
    actual = result.facts[0]
    held = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=actual.authority_snapshot_refs,
        dependency_refs=actual.dependency_refs,
        producer_replay_locator_or_reference_root=actual.producer_replay_locator_or_reference_root,
        **dict(actual.semantic_fields),
    )
    received = _receive(query, replace(result, facts=(held,)))
    m = received.semantic_projection()
    assert m["producer_state"] == "LOW_SUPPORT"
    assert m["producer_state"] != "SUPPORTED"
    assert m["raw_fully_resolved_joint_n"] == 4
    assert m["held_observed_n_if_nonpositive"] == 4
    assert m["complete_cells"] == []
    assert m["conditioned_complete_case_support"] == []
    assert m["zero_means"] == "NO_ZERO_INFERENCE_FROM_NONPOSITIVE_PRODUCER_STATE"
