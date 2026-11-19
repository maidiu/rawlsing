"""Real I05 exact-frontier -> FF01 same-respondent joint and validation grades."""
import pytest

from rawlsing_next.field_forge_i05_role_ingress import (
    FF01I05IngressError, receive_i05_exact_joint_at_ff01,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import test_pre553_discovery_exact as i05


def _real_frontier():
    source = i05._build_source("ff01-i05-config3", [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y}}
        for x in (0, 1) for y in (0, 1)
    ])
    qauth, dauth = i05._query_authority("ff01-i05-config3"), i05._d_auth("ff01-i05-config3-discovery")
    all_p = i05._branch_predicate(source, qauth, tag="all")
    joint = i05._query(source, qauth, all_p, ("X", "Y", "Z"), tag="joint")
    cells = tuple((str(x), str(y), str(z)) for x in (0, 1) for y in (0, 1) for z in (0, 1))
    grammar = i05._grammar(
        operation="I03-OP-ff01-i05-config3-discovery",
        atoms=[i05._atom("ALL", all_p, "BRANCH")],
        templates=[i05._qt("J", joint)],
        rules=[i05._rule(
            "config3", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "BASE_QUERY",
            baseline_atom_id="ALL", query_template_id="J", target_cells=cells,
            validation={"kind": "TARGET_CELL_SUPPORTED"},
        )],
        k=2, j=3,
    )
    return i05._execute(source, qauth, dauth, grammar, (all_p,), (joint,))


def test_i05_real_complete_eight_cell_frontier_has_four_supported_and_four_empty():
    discovery = _real_frontier()
    assert discovery.candidate_count == discovery.covered_candidate_count == 8
    states = [r.typed_state for r in discovery.receipts]
    assert states.count("DISCOVERED_RESULT_SUPPORTED") == 4
    assert states.count("VALID_EMPTY") == 4
    outputs = [
        receive_i05_exact_joint_at_ff01(
            discovery=discovery, candidate_receipt_ref=receipt.ref,
            query_role="BASE", conditioner_index=0,
        )
        for receipt in discovery.receipts
    ]
    assert len(outputs) == 8
    for (ff01, handoff), original in zip(outputs, discovery.receipts):
        assert ff01.semantic_projection()["joint_arity"] == 3
        assert len(ff01.semantic_projection()["complete_cells"]) == 8
        assert ff01.semantic_projection()["raw_fully_resolved_joint_n"] == 4
        assert handoff.material()["candidate_validation_state"] == original.typed_state
        assert handoff.material()["candidate_receipt_ref"] == original.ref.as_dict()
        assert handoff.material()["role_fact_ref"] == ff01.semantic_projection()["producer_fact_ref"]
        assert "NO_SCIENTIFIC_RANK" in handoff.material()["grade"]
    # A candidate cell with source-observed zero is still a genuine full joint
    # to preserve. I05 VALID_EMPTY did not erase its underlying I03 fact.
    assert any(r.typed_state == "VALID_EMPTY" and f.semantic_projection()["complete_cells"]
               for (f, _), r in zip(outputs, discovery.receipts))


def test_unknown_i05_role_and_foreign_receipt_refuse():
    result = _real_frontier()
    valid = result.receipts[0]
    with pytest.raises(FF01I05IngressError, match="absent or ambiguous"):
        receive_i05_exact_joint_at_ff01(
            discovery=result, candidate_receipt_ref=valid.ref,
            query_role="NOT_AN_I05_ROLE", conditioner_index=0,
        )
    fabricated = ExactRef("DiscoveryResultReceipt@1.0.0", "urn:test:alien", semantic_hash("alien"))
    with pytest.raises(FF01I05IngressError, match="unique member"):
        receive_i05_exact_joint_at_ff01(
            discovery=result, candidate_receipt_ref=fabricated,
            query_role="BASE", conditioner_index=0,
        )


def test_replay_rebuilds_same_exact_ff01_and_i05_role_receipt():
    first = _real_frontier()
    receipt = first.receipts[0]
    a = receive_i05_exact_joint_at_ff01(
        discovery=first, candidate_receipt_ref=receipt.ref,
        query_role="BASE", conditioner_index=2,
    )
    second = _real_frontier()
    b = receive_i05_exact_joint_at_ff01(
        discovery=second, candidate_receipt_ref=second.receipts[0].ref,
        query_role="BASE", conditioner_index=2,
    )
    assert a[0].ref == b[0].ref
    assert a[1].ref == b[1].ref
