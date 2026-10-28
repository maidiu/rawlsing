"""Focused tests for the exact native workload builder and V2 scope."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from campaign_src04_completion.empirical import fixture_native_workload_evidence as fixture_evidence
from campaign_src04_completion.empirical.native_workload import (
    NativeWorkloadRefusal,
    WorkloadPolicy,
    execute_native_workload,
    plan_from_scope,
)
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_observed_response import ObservedResponseContract

ROOT = Path(__file__).resolve().parents[2]
EMPIRICAL = ROOT / "campaign_src04_completion/empirical"
SCOPE_PATH = EMPIRICAL / "SCOPE_LEDGER_V2.json"
CONTRACT_PATH = EMPIRICAL / "CONTRACT_APPROVAL_READY_V2.json"
EVIDENCE_PATH = EMPIRICAL / "NATIVE_WORKLOAD_EVIDENCE.json"


def _scope():
    return json.loads(SCOPE_PATH.read_text(encoding="utf-8"))


def _contract():
    raw = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    return ObservedResponseContract.from_mapping(raw["contract"])


def test_scope_uses_current_175_qualified_and_residuals_are_explicit():
    scope = _scope()
    assert scope["physical_accounting"]["available_response_fields"] == 175
    assert scope["physical_accounting"]["held_response_fields"] == 3
    assert scope["physical_accounting"]["all_181_slots_accounted"] is True
    assert set(scope["held_field_ids"]) == {
        "q217", "q715withoutmorocco", "q716withoutmorocco",
    }
    assert scope["physical_accounting"]["available_analytical_coordinates"] == 0
    ser = next(c for c in scope["coordinate_ledger"] if c["name"] == "ser")
    assert ser["status"] == "IDENTITY_ONLY"
    assert ser["analytical_eligible"] is False


def test_plan_is_release_bound_and_does_not_use_stale_163_or_triples():
    scope = _scope()
    contract = _contract()
    policy = WorkloadPolicy.from_mapping(scope["workload_policy"])
    plan = plan_from_scope(scope=scope, contract=contract, policy=policy)
    assert plan["scope"]["available_response_fields"] == 175
    assert plan["operations"]["unary_operations"] == 175
    assert plan["operations"]["joint_pair_operations"] == 15_225
    assert plan["operations"]["conditional_target_pairs_awaiting_release_values"] == 30_450
    assert plan["operations"]["higher_order_requested_not_authorized"] == 877_975
    assert "higher_order" not in plan["operations"]


def test_fixture_builder_executes_real_native_operations_and_resumes():
    fixture_evidence.main()
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    assert evidence["scope"] == "SRC04_NONRESPONDENT_FIXTURE_ONLY"
    assert evidence["builder"]["operations_built"] == 44
    assert evidence["builder"]["operations_executed"] == 44
    assert evidence["builder"]["operations_refused"] == 0
    assert evidence["builder"]["operations_by_family"] == {
        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION": 38,
        "SAME_RESPONDENT_JOINT_DISTRIBUTION": 3,
        "UNARY_OBSERVED_DISTRIBUTION": 3,
    }
    assert all(item["raw_denominator"] == 7 for item in evidence["actual_results"]["unary"].values())
    assert len(evidence["operation_receipts"]) == 44
    assert all(receipt["query_ref"] is not None for receipt in evidence["operation_receipts"])
    assert all(receipt["fact_ref"] is not None for receipt in evidence["operation_receipts"])
    assert evidence["resume_check"]["operations_executed_after_resume"] == 43
    assert evidence["resume_check"]["prefix_not_reexecuted"] is True


def test_pending_contract_refuses_execution_before_query_issuance():
    contract = _contract()
    policy = WorkloadPolicy.from_mapping(_scope()["workload_policy"])
    with pytest.raises(NativeWorkloadRefusal, match="NOT_AUTHORIZED"):
        execute_native_workload(
            repository=None,
            release_ref=ExactRef("C11LogicalRelease", "urn:test:not-a-release", "0" * 64),
            contract=contract,
            authority_registry=None,
            policy=policy,
        )


def test_contract_target_scope_excludes_identity_and_context_coordinates():
    contract = _contract()
    assert len(contract.target_refs) == 175
    assert all(ref.kind == "NATIVE_QUESTION" for ref in contract.target_refs)
    assert "REFUSAL" in contract.observed_states
    assert contract.missing_states == ("MISSING",)
