"""Focused tests for GAP-007 repaired C11/I03/I05/Batch binding."""
from __future__ import annotations
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
TRACE = json.loads((HERE / "actual_trace.json").read_text())


def test_01_exact_c11_release_and_p1_operation_identity():
    assert TRACE["source"]["release_ref"]["kind"] == "C11LogicalRelease"
    assert TRACE["source"]["release_object_count"] > 0
    assert TRACE["p1"]["operation_identity_preserved"] is True
    assert TRACE["p1"]["original_plan_ref"] == TRACE["p1"]["bound_plan_ref"]


def test_02_all_840_p1_operations_accounted_with_no_invention():
    assert TRACE["p1"]["operation_count"] == 840
    assert TRACE["no_drop"]["all_840_accounted"] is True
    assert TRACE["no_drop"]["bound_210"] is True
    assert TRACE["no_drop"]["unsupported_630"] is True
    assert TRACE["no_drop"]["no_invented_operations"] is True


def test_03_bound_i03_batch_actual_output():
    assert TRACE["p1"]["manifest_unit_count"] == 210
    assert TRACE["batch"]["receipt_count"] == 210
    assert TRACE["batch"]["completed"] == 210
    assert TRACE["batch"]["states"] == {"COMPLETED": 210}
    assert TRACE["batch"]["fact_state_counts"] == {"SUPPORTED": 210}


def test_04_actual_i05_receiver_and_wrong_release_authority_refusals():
    assert TRACE["i05"]["status"] == "EXECUTED"
    assert TRACE["i05"]["native_result_type"] == "ExactBoundedDiscoveryResult"
    assert TRACE["i05"]["receipt_count"] > 0
    assert TRACE["i05"]["fact_count"] > 0
    assert TRACE["wrong_release_refusal"]["status"] == "TYPED_REFUSAL"
    assert "exact C11 release unavailable" in TRACE["wrong_release_refusal"]["detail"]
    assert TRACE["wrong_authority_refusal"]["status"] == "TYPED_REFUSAL"
    assert "query_ref exact preimage unavailable" in TRACE["wrong_authority_refusal"]["detail"]


def test_05_unsupported_p1_kinds_are_typed_refusals_not_invented_queries():
    counts = TRACE["p1"]["unsupported_typed_refusals"]
    assert counts == {"CONDITIONAL": 210, "HETEROGENEITY": 105, "JOINT": 210, "RECURSIVE_BRANCH": 105}
    assert len([x for x in TRACE["p1"]["accounting"] if x["status"] == "TYPED_REFUSAL"]) == 630
    assert all(x.get("reason") == "P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING" for x in TRACE["p1"]["accounting"] if x["status"] == "TYPED_REFUSAL")
