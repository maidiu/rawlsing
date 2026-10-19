"""P41 core trajectories: computed progressive chain, target roles, minorities,
zero support, measured null and the E03 N10W chain machinery."""
from __future__ import annotations

import pytest

from fixture import CONDITIONS, prepare
from p41_service import P41Service, P41ServiceError

EXPECTED = [{"0": 14, "1": 18}, {"0": 6, "1": 10}, {"0": 2, "1": 6}]


def cell_map(step):
    return {cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]}


def test_computed_progressive_chain_exact():
    service = P41Service()
    receipt = service.progressive()
    assert [step["denominator"] for step in receipt["n10e_steps"]] == [32, 16, 8]
    assert [cell_map(step) for step in receipt["n10e_steps"]] == EXPECTED
    assert [step["route"] for step in receipt["n10e_steps"]] == \
        ["N10E_PUBLIC_SINGLE", "C1_PUBLIC_MULTI_BINDING", "C1_PUBLIC_MULTI_BINDING"]
    assert receipt["n10w"]["progressive_chain_state"] == "EXACT_PROGRESSIVE_CHAIN"
    consumptions = receipt["n10w"]["positioned_consumptions"]
    assert len(consumptions) == 3
    assert all(item["result_state"] == "EXACT_SUPPORTED" for item in consumptions)
    assert all(item["same_evidence_object"] for item in consumptions)
    assert receipt["unknown"]["evidence_state"] == "EXACT_SUPPORT_ON_CONDITIONED_RISK_SET"


def test_progressive_update_changes_query_identity_and_conditioners():
    receipt = P41Service().progressive()
    identities = receipt["n10w"]["progressive_update_identity"]
    assert len(set(identities)) == 3
    assert receipt["n10e_steps"][0]["conditioners"] == [["A", 1]]
    assert receipt["n10e_steps"][1]["conditioners"] == [["A", 1], ["B", 1]]
    assert receipt["n10e_steps"][2]["conditioners"] == [["A", 1], ["B", 1], ["C", 1]]


def test_minority_and_counterpattern_cells_survive():
    receipt = P41Service().progressive()
    depth3 = cell_map(receipt["n10e_steps"][2])
    assert depth3 == {"0": 2, "1": 6}
    assert receipt["minorities"]["all_alternatives_preserved"] is True
    assert receipt["minorities"]["smallest_cell"] == \
        {"cell": "0", "raw_numerator_support": 2}
    assert all(cell["raw_numerator_support"] > 0
               for step in receipt["n10e_steps"] for cell in step["cells"])


def test_reverse_role_authorized_with_exact_denominator():
    receipt = P41Service().progressive(target="A", conditions=(("Y", 1),))
    assert receipt["query"]["role_class"] == "REVERSE_AUTHORIZED"
    assert receipt["n10e_steps"][0]["denominator"] == 29
    assert cell_map(receipt["n10e_steps"][0]) == {"0": 11, "1": 18}


def test_unauthorized_reverse_role_refuses():
    service = P41Service()
    with pytest.raises(P41ServiceError,
                       match="TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE"):
        service.progressive(target="B", conditions=(("A", 1),))
    with pytest.raises(P41ServiceError,
                       match="TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE"):
        service.progressive(target="C", conditions=(("Y", 1),))


def test_learned_release_reverse_without_record_refuses():
    service = P41Service()
    with pytest.raises(ValueError, match="RELEASE_QUERY_NOT_INCLUDED"):
        service.readthrough.provider.progressive("A", (("Y", 1),))


def test_zero_support_is_typed_not_zero_probability():
    receipt = P41Service(prepare(support_loss=True)).progressive()
    last = receipt["n10e_steps"][-1]
    assert last["state"] == "ZERO_SUPPORT"
    assert last["denominator"] == 0
    assert last["cells"] == []
    assert last["uncertainty"] == "NO_SUPPORTED_EVIDENCE"
    assert receipt["unknown"]["zero_support_steps"] == [3]
    assert receipt["unknown"]["evidence_state"] == "NO_SUPPORTED_EVIDENCE"
    assert receipt["unknown"]["never_fabricated_zero"] is True


def test_measured_null_is_a_product_not_missingness():
    receipt = P41Service(prepare(measured_null=True)).progressive()
    assert [cell_map(step) for step in receipt["n10e_steps"]] == \
        [{"0": 16, "1": 16}, {"0": 8, "1": 8}, {"0": 4, "1": 4}]
    assert receipt["unknown"]["zero_support_steps"] == []


def test_e03_n10w_chain_machinery_receipt():
    chain = P41Service().e03_chain_receipt()
    assert [step["route"] for step in chain["steps"]] == \
        ["N10E_SINGLE_CONDITIONER", "C1_MULTI_CONDITIONER", "C1_MULTI_CONDITIONER"]
    assert [step["denominator"] for step in chain["steps"]] == [32, 16, 8]
    assert [step["cells"] for step in chain["steps"]] == EXPECTED
    assert all(item["result_state"] == "EXACT_SUPPORTED"
               for item in chain["f8_consumptions"])
