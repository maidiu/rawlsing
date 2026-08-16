#!/usr/bin/env python3
"""W03-B typed V551J output-state regressions."""

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import _derive_v551j_boundary_state


def test_zero_candidates_is_valid_empty_not_integrity_failure() -> None:
    state = _derive_v551j_boundary_state(
        candidate_count=0,
        certified_count=0,
        review_count=0,
        validation_issues=[],
        strict=True,
    )
    assert state == (
        "PASS",
        "VALID_EMPTY",
        "NOT_APPLICABLE",
        "VALID_EMPTY_V551J_NO_JOINT_EVIDENCE",
    )


def test_review_only_packets_preserve_evidence_but_deny_downstream() -> None:
    state = _derive_v551j_boundary_state(
        candidate_count=3,
        certified_count=0,
        review_count=2,
        validation_issues=[],
        strict=True,
    )
    assert state == (
        "PASS",
        "PRESENT",
        "DENY",
        "VALID_V551J_REVIEW_ONLY_NOT_DOWNSTREAM",
    )


def test_certified_packets_allow_downstream() -> None:
    state = _derive_v551j_boundary_state(
        candidate_count=3,
        certified_count=1,
        review_count=1,
        validation_issues=[],
        strict=True,
    )
    assert state == (
        "PASS",
        "PRESENT",
        "ALLOW",
        "READY_V551J_JOINT_EVIDENCE_CONTRACT",
    )


def test_contract_validation_failure_is_integrity_failure_not_empty_evidence() -> None:
    state = _derive_v551j_boundary_state(
        candidate_count=0,
        certified_count=0,
        review_count=0,
        validation_issues=["scope_contract_mismatch"],
        strict=True,
    )
    assert state == (
        "FAIL",
        "APPLICABLE_UNRESOLVED",
        "DENY",
        "BLOCKED_V551J_OUTPUT_CONTRACT",
    )


def test_no_strict_never_grants_downstream_permission() -> None:
    state = _derive_v551j_boundary_state(
        candidate_count=2,
        certified_count=2,
        review_count=0,
        validation_issues=[],
        strict=False,
    )
    assert state == (
        "PASS",
        "PRESENT",
        "DENY",
        "DIAGNOSTIC_V551J_NO_STRICT_NOT_READY",
    )
