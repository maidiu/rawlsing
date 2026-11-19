"""Source-static adversarial #1155 receivers: 3/4 is never SUPPORTED."""
from dataclasses import replace
import pytest
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, canonical_json, semantic_hash
from rawlsing_next.pre553_s04_observed_research import S04KnowledgeError, S04ObservedKnowledge, receive_s04_i03_research
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralAlgebraError, S04GeneralJointWorkspace, S04Projection
from rawlsing_next.field_forge_generic_empirical_ingress import FF01GenericIngressError, receive_ff01_observed_joint
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case

def _false_supported_partial():
    _, _, _, query, execution = _case(tag="HOSTILE1155-SUPPORTED-THREE-OF-FOUR")
    original = execution.facts[0]
    fields = dict(original.semantic_fields)
    topology = dict(original.target_topology)
    rows = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    chosen = next(row for row in rows if row["raw_numerator_support"] == 1)
    chosen["raw_numerator_support"] = 0
    chosen["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    topology["complete_cell_semantic_projection"] = rows
    fields.update(target_topology=topology, raw_numerator_support=3, raw_resolved_target_support=3)
    forged = EmpiricalFact(
        typed_state="SUPPORTED",
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **fields,
    )
    assert forged.raw_denominator_support == 4
    assert forged.raw_numerator_support == 3
    return query, replace(execution, facts=(forged,))

def test_supported_partial_3_of_4_refused_by_s04_and_direct_ff01():
    query, execution = _false_supported_partial()
    with pytest.raises(S04KnowledgeError, match="complete eligible/resolved"):
        receive_s04_i03_research(query=query, execution=execution)
    with pytest.raises(FF01GenericIngressError, match="complete eligible/resolved"):
        receive_ff01_observed_joint(
            query=query, execution=execution, conditioner_index=0,
            producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
        )

@pytest.mark.parametrize("mutation", ("partial", "typed", "cell_state"))
def test_self_rehashed_inconsistent_s04_is_not_valid_general_knowledge(mutation):
    _, _, _, query, execution = _case(tag="HOSTILE1155-VALID-FULL-RISK")
    valid = receive_s04_i03_research(query=query, execution=execution)
    m = valid.material()
    if mutation == "partial":
        m["raw_eligible_condition_denominator"] += 1
    elif mutation == "typed":
        m["producer_typed_state"] = "UNRESOLVED"
    else:
        selected = next(row for row in m["complete_cells"] if row["raw_count"] > 0)
        selected["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    forged = S04ObservedKnowledge(canonical_json(m), semantic_hash(m))
    with pytest.raises(S04GeneralAlgebraError):
        S04GeneralJointWorkspace(knowledge=forged, expected_knowledge_ref=forged.ref)

@pytest.mark.parametrize("sentinel", (0, "", "DENIED", False))
def test_current_guard_cannot_return_failure_sentinel_as_grant(sentinel):
    _, _, _, q, r = _case(tag="HOSTILE1155-CURRENT")
    k = receive_s04_i03_research(query=q, execution=r)
    with pytest.raises(S04GeneralAlgebraError, match="CURRENT"):
        S04GeneralJointWorkspace(
            knowledge=k, expected_knowledge_ref=k.ref,
            current_guard=lambda: sentinel,
        )

def test_native_none_return_on_success_still_accepted():
    _, _, _, q, r = _case(tag="HOSTILE1155-NATIVE-VOID-GUARD")
    k = receive_s04_i03_research(query=q, execution=r)
    w = S04GeneralJointWorkspace(
        knowledge=k, expected_knowledge_ref=k.ref,
        current_guard=lambda: None,
    )
    assert w.query(S04Projection((0,), {})).material()["raw_selected_full_case_n"] == 4
