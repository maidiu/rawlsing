"""Independent whole-stack negative-evidence court; exact genuine I03/I05 fixtures.

No original source, scientific ranking, protected receiving, or G5 asserted.
These tests reproduce defects in the stacked #1149/#1150/#1152 code,
not in the already strict canonical EmpiricalFact top-level count validator.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt, EmpiricalFact,
)
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError, receive_ff01_observed_joint,
)
from rawlsing_next.field_forge_i05_role_ingress import (
    FF01I05IngressError, receive_i05_exact_joint_at_ff01,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04KnowledgeError, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_i05_reception import (
    S04I05ReceptionError, receive_s04_i05_role,
)
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case
from rawlsing_next.tests.test_pyat1009_ff01_i05_role_ingress import _real_frontier

PERMISSIONS = ("FF01_DESCRIPTIVE_SOURCEFREE",)


def _held_negative_fixture(topology_mode):
    _, _, _, query, execution = _case(tag="REVIEW1097-HELD-NEGATIVE")
    fact = execution.facts[0]
    fields = dict(fact.semantic_fields)
    fields["raw_numerator_support"] = 0
    fields["raw_resolved_target_support"] = 0
    if topology_mode == "INVALID_NEGATIVE_CELL":
        topology = dict(fact.target_topology)
        rows = []
        for row in topology["complete_cell_semantic_projection"]:
            cell = dict(row)
            cell["raw_numerator_support"] = 0
            cell["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
            rows.append(cell)
        assert rows
        rows[0]["raw_numerator_support"] = -1
        topology["complete_cell_semantic_projection"] = rows
        fields["target_topology"] = topology
    elif topology_mode == "NONMAPPING":
        fields["target_topology"] = "NOT_AN_I03_TOPOLOGY"
    else:
        raise AssertionError("unknown negative test")
    held = EmpiricalFact(
        typed_state="UNRESOLVED",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fields,
    )
    assert held.raw_denominator_support == 4
    assert held.raw_numerator_support == 0
    assert held.typed_state == "UNRESOLVED"
    return query, replace(execution, facts=(held,))


@pytest.mark.parametrize("poison", ["INVALID_NEGATIVE_CELL", "NONMAPPING"])
def test_held_source_topology_poison_refused_by_both_upstream_and_direct_ff(poison):
    query, execution = _held_negative_fixture(poison)
    with pytest.raises(S04KnowledgeError, match="nonpositive I03"):
        receive_s04_i03_research(query=query, execution=execution)
    with pytest.raises(FF01GenericIngressError, match="nonpositive joint"):
        receive_ff01_observed_joint(
            query=query, execution=execution, conditioner_index=0,
            producer_permission_ceiling=PERMISSIONS,
        )


def test_genuine_low_support_positive_source_cells_stay_held_without_laundering():
    _, _, _, query, execution = _case(tag="REVIEW1097-LOW-SUPPORT")
    original = execution.facts[0]
    held = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **dict(original.semantic_fields),
    )
    from_low_support = replace(execution, facts=(held,))
    observed = receive_s04_i03_research(query=query, execution=from_low_support)
    ff = receive_ff01_observed_joint(
        query=query, execution=from_low_support, conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    )
    assert observed.material()["state"] == "PRODUCER_TYPED_HELD"
    assert observed.material()["raw_fully_resolved_joint_n"] == 4
    assert observed.material()["complete_cells"] == []
    assert ff.semantic_projection()["producer_state"] == "LOW_SUPPORT"
    assert ff.semantic_projection()["held_observed_n_if_nonpositive"] == 4
    assert ff.semantic_projection()["complete_cells"] == []


def test_incomplete_i05_candidate_cannot_bypass_s04_terminal_coverage_at_ff01():
    discovery = _real_frontier()
    original = discovery.receipts[0]
    fields = dict(original.semantic_fields)
    assert original.coverage_state != "INCOMPLETE_UNEVALUATED"
    fields["coverage_state"] = "INCOMPLETE_UNEVALUATED"
    counterfeit = DiscoveryResultReceipt(
        typed_state=original.typed_state,
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **fields,
    )
    receipts = tuple(sorted(
        (counterfeit if row.ref == original.ref else row for row in discovery.receipts),
        key=lambda row: row.ref.key,
    ))
    poisoned = replace(discovery, receipts=receipts)
    # A high-level complete-frontier claim is insufficient to authenticate
    # a particular candidate's completed evaluation.
    with pytest.raises(S04I05ReceptionError, match="nonterminal"):
        receive_s04_i05_role(
            discovery=poisoned, candidate_receipt_ref=counterfeit.ref,
            query_role="BASE",
        )
    with pytest.raises(FF01I05IngressError, match="nonterminal"):
        receive_i05_exact_joint_at_ff01(
            discovery=poisoned, candidate_receipt_ref=counterfeit.ref,
            query_role="BASE", conditioner_index=0,
        )


def test_terminal_i05_fact_still_consumes_original_ff01_without_new_i03():
    discovery = _real_frontier()
    r = discovery.receipts[0]
    observed, s04_receipt = receive_s04_i05_role(
        discovery=discovery, candidate_receipt_ref=r.ref, query_role="BASE",
    )
    ff, direct_receipt = receive_i05_exact_joint_at_ff01(
        discovery=discovery, candidate_receipt_ref=r.ref,
        query_role="BASE", conditioner_index=0,
    )
    assert observed.material()["fact_ref"] == ff.semantic_projection()["producer_fact_ref"]
    assert s04_receipt.material()["candidate_validation_state"] == r.typed_state
    assert direct_receipt.material()["candidate_validation_state"] == r.typed_state


def _partial_unresolved_fixture(*, contradiction=False):
    """Hash-coherent typed UNRESOLVED with 3/4 actual resolved joint cases.

    This is a source-contract mutation of native-owned I03 fact material,
    not a claim that the caller issued a new scientific operation.
    """
    _, _, _, query, execution = _case(tag="REVIEW1097-PARTIAL-UNRESOLVED")
    actual = execution.facts[0]
    fields = dict(actual.semantic_fields)
    topo = dict(actual.target_topology)
    cells = [dict(x) for x in topo["complete_cell_semantic_projection"]]
    positive = next(row for row in cells if row["raw_numerator_support"] == 1)
    positive["raw_numerator_support"] = 0
    positive["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    topo["complete_cell_semantic_projection"] = cells
    fields["target_topology"] = topo
    fields["raw_numerator_support"] = 3
    fields["raw_resolved_target_support"] = 3
    if contradiction:
        # Full cells add to 3, but header falsely claims 2 resolved.
        fields["raw_numerator_support"] = 2
        fields["raw_resolved_target_support"] = 2
    partial = EmpiricalFact(
        typed_state="UNRESOLVED",
        authority_snapshot_refs=actual.authority_snapshot_refs,
        dependency_refs=actual.dependency_refs,
        producer_replay_locator_or_reference_root=actual.producer_replay_locator_or_reference_root,
        **fields,
    )
    return query, replace(execution, facts=(partial,))


def test_native_i03_partial_unresolved_support_survives_held_not_distributed():
    q, execution = _partial_unresolved_fixture()
    original = execution.facts[0]
    assert original.raw_numerator_support == 3
    assert original.raw_denominator_support == 4
    s04 = receive_s04_i03_research(query=q, execution=execution).material()
    ff = receive_ff01_observed_joint(
        query=q, execution=execution, conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    ).semantic_projection()
    assert s04["state"] == "PRODUCER_TYPED_HELD"
    assert s04["producer_typed_state"] == "UNRESOLVED"
    assert s04["raw_fully_resolved_joint_n"] == 3
    assert s04["raw_eligible_condition_denominator"] == 4
    assert s04["nonpositive_positive_count_retained_not_served"] == 3
    assert s04["complete_cells"] == []
    assert ff["producer_state"] == "UNRESOLVED"
    assert ff["raw_fully_resolved_joint_n"] == 3
    assert ff["raw_eligible_condition_denominator"] == 4
    assert ff["held_observed_n_if_nonpositive"] == 3
    assert ff["complete_cells"] == []
    assert ff["zero_means"] == "NO_ZERO_INFERENCE_FROM_NONPOSITIVE_PRODUCER_STATE"


def test_hash_coherent_partial_unresolved_false_nested_total_refuses():
    q, execution = _partial_unresolved_fixture(contradiction=True)
    with pytest.raises(S04KnowledgeError, match="held resolved total"):
        receive_s04_i03_research(query=q, execution=execution)
    with pytest.raises(FF01GenericIngressError, match="held resolved total"):
        receive_ff01_observed_joint(
            query=q, execution=execution, conditioner_index=0,
            producer_permission_ceiling=PERMISSIONS,
        )


def test_native_i03_legitimate_unresolved_emission_rule_is_not_heuristic():
    # This is an independently checked native source-contract invariant:
    # _pre553_query_eval sets UNRESOLVED for
    # 0 <= raw_resolved_target_support < raw_denominator_support, in either
    # ordinary/grouped source-verified evaluation. We assert the bounded
    # receiver behavior, not simulate a new issuer or original source.
    q, execution = _partial_unresolved_fixture()
    assert execution.facts[0].typed_state == "UNRESOLVED"
    assert execution.facts[0].raw_resolved_target_support < execution.facts[0].raw_denominator_support
    s04 = receive_s04_i03_research(query=q, execution=execution)
    assert s04.material()["grade"] != "RAW_FULLY_RESOLVED_SAME_RESPONDENT_SAMPLE_NOT_POPULATION"
