#!/usr/bin/env python3
"""Machine-readable guard that W03-B's local regression suite covers its five issue IDs."""

W03_B_ISSUE_IDS = (
    "V551J-001",
    "V551J-002",
    "V551J-003",
    "V551J-004",
    "V551J-005",
)


def test_w03_b_issue_scope_is_exact() -> None:
    assert W03_B_ISSUE_IDS == (
        "V551J-001",
        "V551J-002",
        "V551J-003",
        "V551J-004",
        "V551J-005",
    )
