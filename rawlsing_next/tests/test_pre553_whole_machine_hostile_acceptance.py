from __future__ import annotations

import importlib.util

import pytest

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


def test_r15_h10_empirical_fact_to_structure_remains_blocked_without_i04_owner() -> None:
    case = case_by_id("R15-H10")
    assert case.verdict == "BLOCKED"
    assert importlib.util.find_spec("rawlsing_next.pre553_structural_admission") is None
    # The I01 object type is deliberately inert: constructing the carrier does
    # not create the I04 admission decision service or actor-side effects.
    run_delegate(case)


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


def test_r15_inspectorate_has_no_semantic_owner_or_repair_lane() -> None:
    assert all(case.verdict != "FAIL" for case in HOSTILE_CASES)
    blocked = [case for case in HOSTILE_CASES if case.verdict == "BLOCKED"]
    assert [case.case_id for case in blocked] == ["R15-H10"]
    assert "No repair in R15" in blocked[0].smallest_repair_if_failure


def test_r15_only_declared_parallel_owner_is_allowed_to_unblock_i04_seam() -> None:
    case = case_by_id("R15-H10")
    assert "I04" in case.smallest_repair_if_failure
    assert "parallel semantic owner" in case.note
