from __future__ import annotations

from dataclasses import replace
import inspect

import pytest

import rawlsing_next.pre553_structural_admission as i04
from rawlsing_next.m1_temporal_v554_admission_dedup import DIRECT_SLOTS
from rawlsing_next.tests import test_pre553_empirical_objects_authority as i01_contract
from rawlsing_next.tests import test_pre553_structural_admission as i04_contract
from rawlsing_next.tests.pre553_whole_machine_hostile_helpers import (
    EXACT_BASE_SHA,
    FROZEN_BLOB_PINS,
    HOSTILE_CASES,
    MANDATORY_ATTACKS,
    case_by_id,
    git_blob_sha,
    repo_root,
    run_delegate,
)


@pytest.mark.parametrize(
    "case",
    tuple(case for case in HOSTILE_CASES if case.verdict == "PASS" and case.delegate_test),
    ids=lambda case: case.case_id,
)
def test_r15_existing_hostile_proofs_remain_green(case) -> None:
    """Re-execute accepted hostile proofs without replacing their semantics."""
    run_delegate(case)


def _assert_nonpositive_i04(out, expected: str) -> None:
    assert out.decision_state == expected
    assert out.m1_direct_projection is None
    assert out.m1_projection_hash is None
    assert not i04.DECISION_MATRIX[expected]["positive_structural_evidence"]
    assert not i04.DECISION_MATRIX[expected]["m1_direct_projection_allowed"]


def test_r15_h10_only_exact_positive_i04_admitted_projects_to_frozen_m1_basis() -> None:
    case = case_by_id("R15-H10")
    assert case.verdict == "PASS"

    # I01 public carrier existence does not itself make an admission decision.
    i01_contract.test_structural_admission_type_does_not_make_the_admission_decision()

    # Raw EmpiricalFact plus provenance and even a discovery receipt remain
    # nonpositive without the separately owned exact I04 rule/authority.
    query, fact = i04_contract.query_fact(tag="r15-h10-missing")
    assert fact.source_empirical_provenance_refs
    _, registry, _, _ = i04_contract.environment()
    missing_request = replace(
        i04_contract.request(),
        discovery_result_receipt_refs=(
            i04_contract.ref("DISCOVERY_RESULT_RECEIPT", "R15-H10"),
        ),
    )
    missing = i04.evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=i04_contract.aref("missing-r15-h10"),
        rule=None,
        request=missing_request,
        authority_registry=registry,
        producer_replay_locator_or_reference_root=i04_contract.root("r15-h10-missing"),
    )
    _assert_nonpositive_i04(missing, "MISSING_STRUCTURAL_ADMISSION_AUTHORITY")
    assert missing_request.discovery_result_receipt_refs

    # Repository/cache presence is not an I04 semantic input. The evaluator
    # consumes exact query/fact/rule/request/authority/replay identity only.
    evaluator_parameters = set(inspect.signature(i04.evaluate_structural_empirical_admission).parameters)
    assert "repository" not in evaluator_parameters
    assert "cache" not in evaluator_parameters

    # The sole positive path is exact named, hash-bound, positively authorized
    # I04 ADMITTED, and its M1 projection is the frozen 17-slot direct basis.
    _, _, positive_rule, _, positive_authority, _, admitted = i04_contract.evaluate()
    assert admitted.decision_state == "ADMITTED"
    assert admitted.receipt.admission_authority_ref == positive_authority.authority_ref.as_dict()
    assert admitted.receipt.structural_interpretation_payload["admission_rule_hash"] == positive_rule.admission_rule_hash
    assert admitted.m1_direct_projection is not None
    assert tuple(admitted.m1_direct_projection) == tuple(DIRECT_SLOTS)
    assert len(admitted.m1_direct_projection) == 17
    assert i04.DECISION_MATRIX["ADMITTED"]["positive_structural_evidence"]
    assert i04.DECISION_MATRIX["ADMITTED"]["m1_direct_projection_allowed"]

    unresolved = i04.AdmissionCondition(
        "STRUCTURAL_TARGET_UNRESOLVED",
        "R15_H10_UNRESOLVED_TARGET",
        (i04_contract.ref("BLOCK", "R15-H10-UNRESOLVED"),),
    )
    nonpositive = (
        (i04_contract.evaluate(admission_state="DENY")[-1], "ADMISSION_DENIED"),
        (i04_contract.evaluate(admission_state="DEFER")[-1], "ADMISSION_DEFERRED"),
        (i04_contract.evaluate(negative_only=True)[-1], "NEGATIVE_AUTHORITY_ONLY"),
        (
            i04_contract.evaluate(
                fact_state="NONCOMPARABLE",
                allowed_states=("NONCOMPARABLE",),
            )[-1],
            "EMPIRICAL_FACT_NONCOMPARABLE",
        ),
        (
            i04_contract.evaluate(
                req=i04_contract.request(time=(i04_contract.TIME2,)),
            )[-1],
            "TEMPORAL_SCOPE_MISMATCH",
        ),
        (
            i04_contract.evaluate(
                req=i04_contract.request(conditions=(unresolved,)),
            )[-1],
            "STRUCTURAL_TARGET_UNRESOLVED",
        ),
        (
            i04_contract.evaluate(
                fact_state="ZERO_SUPPORT",
                n=0,
                d=0,
                allowed_states=("SUPPORTED",),
            )[-1],
            "INSUFFICIENT_EVIDENCE_UNDER_RULE",
        ),
        (
            i04_contract.evaluate(
                fact_state="VALID_EMPTY",
                n=0,
                d=0,
                allowed_states=("VALID_EMPTY",),
            )[-1],
            "VALID_EMPTY",
        ),
    )
    for outcome, expected in nonpositive:
        _assert_nonpositive_i04(outcome, expected)

    # Hash/rule drift is integrity failure and cannot project.
    query, fact, rule, registry, authority, _, _ = i04_contract.evaluate()
    changed_rule = replace(
        rule,
        interpretation_or_transformation_semantics={
            "kind": "BOUNDED_STRUCTURAL_EVIDENCE",
            "changed": "R15-H10-HOSTILE",
        },
    )
    integrity = i04.evaluate_structural_empirical_admission(
        query=query,
        fact=fact,
        requested_admission_authority_ref=authority.authority_ref,
        rule=changed_rule,
        request=i04_contract.request(),
        authority_registry=registry,
        producer_replay_locator_or_reference_root=i04_contract.root("r15-h10-integrity"),
    )
    _assert_nonpositive_i04(integrity, "INTEGRITY_FAILURE")


def test_r15_h10_i04_does_not_own_v553_temporal_decision_or_mint_temporal_objects() -> None:
    case = case_by_id("R15-H10")
    assert case.verdict == "PASS"
    assert not i04.V553_INGRESS_CONTRACT["p06_i04_decides_v553_required"]
    assert not i04.V553_INGRESS_CONTRACT["p06_i04_decides_temporal_operations"]
    assert not i04.V553_INGRESS_CONTRACT["p06_i04_mints_temporal_objects"]

    admitted = i04_contract.evaluate()[-1]
    participant = i04.project_admission_to_v553_participant(
        admitted.receipt,
        role="STRUCTURAL_EMPIRICAL_ADMISSION",
        ordinal=7,
    )
    assert tuple(participant) == tuple(i04.V553_PARTICIPANT_FIELDS)
    assert tuple(participant) == (
        "role",
        "ordinal",
        "structural_empirical_admission_ref",
    )
    assert "required_temporal_operations" not in participant
    assert "V553_REQUIRED" not in participant.values()
    assert "V553_NOT_REQUIRED_FOR_THIS_USE" not in participant.values()


def test_r15_h15_frozen_semantic_blobs_are_byte_exact() -> None:
    root = repo_root()
    mismatches = {}
    for relative, expected in FROZEN_BLOB_PINS.items():
        actual = git_blob_sha(root / relative)
        if actual != expected:
            mismatches[relative] = {"expected": expected, "actual": actual}
    assert not mismatches, (
        f"frozen semantic blob drift from exact R15 base {EXACT_BASE_SHA}: {mismatches}"
    )


def test_r15_matrix_covers_every_commanded_minimum_attack() -> None:
    attacks = {case.attack for case in HOSTILE_CASES}
    assert MANDATORY_ATTACKS <= attacks
    assert len({case.case_id for case in HOSTILE_CASES}) == len(HOSTILE_CASES)
    assert {case.verdict for case in HOSTILE_CASES} <= {"PASS", "FAIL", "BLOCKED"}


def test_r15_integrated_matrix_has_no_unresolved_block_after_accepted_i04() -> None:
    assert all(case.verdict == "PASS" for case in HOSTILE_CASES)
    assert not [case for case in HOSTILE_CASES if case.verdict == "BLOCKED"]
    h10 = case_by_id("R15-H10")
    assert "exact named, hash-bound positive I04" in h10.smallest_repair_if_failure
    assert "Integrated convergence" in h10.note


def test_r15_h10_refresh_does_not_reclassify_any_other_hostile_case() -> None:
    assert len(HOSTILE_CASES) == 19
    assert tuple(case.case_id for case in HOSTILE_CASES) == tuple(
        f"R15-H{index:02d}" for index in range(1, 20)
    )
    assert case_by_id("R15-H10").delegate_module is None
    assert case_by_id("R15-H10").delegate_test is None
