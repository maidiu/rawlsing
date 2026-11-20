"""Actual I03 sourcefree partial condition truth -> S04 typed hold.

No count is admitted as a complete distribution if one eligible member has
unknown condition membership, even if every KNOWN-TRUE member has a target.
"""
from dataclasses import replace

import pytest

from rawlsing_next._pre553_query_predicate import UnresolvedConditionMember
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real
from rawlsing_next.tests import test_pre553_empirical_query as native


@pytest.mark.parametrize("unknown_count", [1, 4])
def test_native_i03_typed_held_condition_conserves_exact_unknown_members(
    monkeypatch, unknown_count,
):
    source, qa, pred, query, baseline = _real(
        tag=f"PREFF-UNKNOWN-{unknown_count}",
    )
    assert baseline.facts[0].typed_state == "SUPPORTED"
    import rawlsing_next._pre553_query_eval as evaluator
    original = evaluator._eval_predicate
    visited = {"n": 0}

    def injected(*args, **kwargs):
        visited["n"] += 1
        if visited["n"] <= unknown_count:
            raise UnresolvedConditionMember(
                "UNRESOLVED_CONDITION_MEMBER: sourcefree unknown recorded code"
            )
        return original(*args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(evaluator, "_eval_predicate", injected)
        actual = native._run(source, qa, pred, query)
    assert visited["n"] == 4
    fact = actual.facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert fact.raw_denominator_support == 4 - unknown_count
    assert fact.raw_numerator_support == 4 - unknown_count
    condition_witness = fact.target_topology["condition_membership_uncertainty"]
    assert condition_witness["state"] == "UNRESOLVED_CONDITION_MEMBERSHIP"
    assert len(condition_witness["member_refs"]) == unknown_count
    assert condition_witness["known_true_denominator"] == 4 - unknown_count
    assert condition_witness["eligible_risk_n"] == 4
    assert len(fact.risk_set_member_refs) == 4
    assert len(fact.denominator_member_refs) == 4 - unknown_count
    assert fact.ref != baseline.facts[0].ref
    assert fact.replay_ref != baseline.facts[0].replay_ref

    knowledge = receive_s04_i03_research(query=query, execution=actual)
    material = knowledge.material()
    assert material["state"] == "PRODUCER_TYPED_HELD"
    assert material["complete_cells"] == []
    assert material["producer_typed_state"] == "UNRESOLVED"
    assert len(material["source_unknown_condition_member_refs"]) == unknown_count
    assert material["source_known_true_denominator_n"] == 4 - unknown_count
    assert material["source_eligible_risk_n"] == 4
    answer = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
    ).query(S04Projection((0,), {})).material()
    assert answer["state"] != "SUPPORTED"
    assert answer["comparative_predictor_rank"] is None
    # Real FF01 adapter consumes the HELD S04 value, without querying
    # the original respondents again or fabricating full support.
    from rawlsing_next.pre553_s04_ff01_consumer import receive_ff01_from_s04
    from rawlsing_next.field_forge_generic_empirical_ingress import BLOCKED_GRADE
    ff01 = receive_ff01_from_s04(
        knowledge=knowledge, query=query, execution=actual,
        conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    assert ff01.semantic_projection()["claim_grade"] == BLOCKED_GRADE
    assert ff01.semantic_projection()["producer_state"] == "UNRESOLVED"
    assert ff01.semantic_projection()["complete_cells"] == []
    held = ff01.semantic_projection()["held_condition_membership_uncertainty"]
    assert held["state"] == "UNRESOLVED_CONDITION_MEMBERSHIP__NO_FULL_DISTRIBUTION"
    assert "unknown_member_ref_commitment" not in held
    assert held["roster_binding"] == (
        "EXACT_S04_KNOWLEDGE_REF_ONLY__NO_EXPORTED_ROSTER_DIGEST"
    )
    assert held["unknown_member_n"] == unknown_count
    assert held["member_refs_exported"] is False
    assert "unknown_member_refs" not in held
    assert held["source_knowledge_ref"] == knowledge.ref.as_dict()
    assert held["known_true_denominator_n"] == 4 - unknown_count
    assert held["eligible_risk_n"] == 4


def test_rehashed_inconsistent_unknown_condition_members_are_not_admitted(
    monkeypatch,
):
    source, qa, pred, query, _ = _real(tag="PREFF-MALICIOUS-UNKNOWN")
    import rawlsing_next._pre553_query_eval as evaluator
    original = evaluator._eval_predicate
    count = {"n": 0}

    def partial(*args, **kwargs):
        count["n"] += 1
        if count["n"] == 1:
            raise UnresolvedConditionMember(
                "UNRESOLVED_CONDITION_MEMBER: sourcefree uncertain"
            )
        return original(*args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(evaluator, "_eval_predicate", partial)
        actual = native._run(source, qa, pred, query)
    from rawlsing_next.pre553_empirical_objects import EmpiricalFact, exact_ref
    fact = actual.facts[0]
    source_topology = dict(fact.target_topology)
    witness = dict(source_topology["condition_membership_uncertainty"])
    witness["member_refs"] = [
        exact_ref(fact.denominator_member_refs[0], "known respondent").as_dict()
    ]
    source_topology["condition_membership_uncertainty"] = witness
    forged = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **{**dict(fact.semantic_fields), "target_topology": source_topology},
    )
    with pytest.raises(Exception, match="uncertain condition members"):
        receive_s04_i03_research(
            query=query, execution=replace(actual, facts=(forged,))
        )
