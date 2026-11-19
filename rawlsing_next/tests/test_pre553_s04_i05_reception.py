"""I05 source-owned real result must arrive S04 before any Field Forge claim."""
import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_s04_i05_reception import (
    S04I05ReceptionError, receive_s04_i05_role,
)
from rawlsing_next.tests.test_pyat1009_ff01_i05_role_ingress import _real_frontier


def test_all_real_eight_i05_candidates_reach_upstream_s04_without_research_loss():
    discovery = _real_frontier()
    assert discovery.candidate_count == discovery.covered_candidate_count == 8
    generated = [
        receive_s04_i05_role(
            discovery=discovery, candidate_receipt_ref=receipt.ref,
            query_role="BASE",
        )
        for receipt in discovery.receipts
    ]
    assert len(generated) == 8
    assert {row[1].material()["candidate_validation_state"] for row in generated} == {
        "VALID_EMPTY", "DISCOVERED_RESULT_SUPPORTED"
    }
    for (knowledge, receipt), owner_receipt in zip(generated, discovery.receipts):
        km, rm = knowledge.material(), receipt.material()
        assert km["target_arity"] == 3
        assert len(km["complete_cells"]) == 8
        assert km["raw_fully_resolved_joint_n"] == 4
        assert km["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
        assert rm["candidate_receipt_ref"] == owner_receipt.ref.as_dict()
        assert rm["s04_observed_ref"] == knowledge.ref.as_dict()
        assert rm["candidate_validation_state"] == owner_receipt.typed_state
        assert "NO_NEW_I03_EXECUTION" in rm["not_proven"][0]
    assert any(
        r[1].material()["candidate_validation_state"] == "VALID_EMPTY"
        and r[0].material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
        for r in generated
    )


def test_nonexistent_role_or_alien_receipt_cannot_invent_i05_research():
    discovery = _real_frontier()
    with pytest.raises(S04I05ReceptionError, match="no unique"):
        receive_s04_i05_role(
            discovery=discovery, candidate_receipt_ref=discovery.receipts[0].ref,
            query_role="NOT_A_SOURCE_ROLE",
        )
    alien = ExactRef("DiscoveryResultReceipt@1.0.0", "urn:test:alien", semantic_hash("alien"))
    with pytest.raises(S04I05ReceptionError, match="not uniquely present"):
        receive_s04_i05_role(
            discovery=discovery, candidate_receipt_ref=alien, query_role="BASE",
        )


def test_sourcefree_i05_role_replay_is_identical_on_fresh_owner_execution():
    first = _real_frontier()
    second = _real_frontier()
    a = receive_s04_i05_role(
        discovery=first, candidate_receipt_ref=first.receipts[0].ref, query_role="BASE",
    )
    b = receive_s04_i05_role(
        discovery=second, candidate_receipt_ref=second.receipts[0].ref, query_role="BASE",
    )
    assert a[0].ref == b[0].ref
    assert a[1].ref == b[1].ref
