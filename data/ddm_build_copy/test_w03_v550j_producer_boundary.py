#!/usr/bin/env python3
"""W03-B amendment regressions for the V550J producer boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (
    V550J_PRODUCER_COMPILER_VERSION,
    V550J_PRODUCER_SCHEMA_VERSION,
    V550J_V551J_GOVERNED_TABLES,
    _derive_v550j_producer_boundary_state,
    _write_table,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v550j_write_table_declares_exact_post_serialization_parquet_sha256(tmp_path: Path) -> None:
    frame = pd.DataFrame([{"run_id": "r1", "value": 1}])

    declaration = _write_table(
        frame,
        out_dir=tmp_path,
        table_name="joint_response_pattern_index",
        write_csv=False,
        write_parquet=True,
    )

    path = Path(declaration["parquet_path"])
    assert path.exists()
    assert declaration["artifact_kind"] == "canonical"
    assert declaration["artifact_file_sha256"] == _sha(path)
    assert declaration["schema_version"] == V550J_PRODUCER_SCHEMA_VERSION
    assert declaration["compiler_version"] == V550J_PRODUCER_COMPILER_VERSION


def test_v550j_complete_core_surface_is_present_and_allowed() -> None:
    state = _derive_v550j_producer_boundary_state(
        governed_family_count=1,
        core_table_row_counts={name: 1 for name in V550J_V551J_GOVERNED_TABLES},
        validation_status="pass",
    )
    assert state == (
        "PASS",
        "PRESENT",
        "ALLOW",
        "COMPLETE_V550J_JOINT_PATTERN_EVIDENCE",
    )


def test_v550j_valid_empty_core_surface_is_not_integrity_failure() -> None:
    state = _derive_v550j_producer_boundary_state(
        governed_family_count=1,
        core_table_row_counts={name: 0 for name in V550J_V551J_GOVERNED_TABLES},
        validation_status="not_applicable",
    )
    assert state == (
        "PASS",
        "VALID_EMPTY",
        "NOT_APPLICABLE",
        "VALID_EMPTY_NO_JOINT_PATTERN_EVIDENCE",
    )


def test_v550j_no_governed_family_is_typed_not_applicable() -> None:
    state = _derive_v550j_producer_boundary_state(
        governed_family_count=0,
        core_table_row_counts={name: 0 for name in V550J_V551J_GOVERNED_TABLES},
        validation_status="not_applicable",
    )
    assert state == (
        "PASS",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "NO_GOVERNED_JOINT_FAMILY_APPLICABLE",
    )


def test_v550j_partial_core_surface_is_unresolved_not_silently_allowed() -> None:
    counts = {name: 1 for name in V550J_V551J_GOVERNED_TABLES}
    counts["joint_pattern_relation_signature"] = 0
    state = _derive_v550j_producer_boundary_state(
        governed_family_count=1,
        core_table_row_counts=counts,
        validation_status="pass",
    )
    assert state == (
        "PASS",
        "APPLICABLE_UNRESOLVED",
        "DENY",
        "INCOMPLETE_V550J_CORE_PRODUCER_SURFACE",
    )


def test_v550j_failed_validation_is_nonpass_integrity() -> None:
    state = _derive_v550j_producer_boundary_state(
        governed_family_count=1,
        core_table_row_counts={name: 1 for name in V550J_V551J_GOVERNED_TABLES},
        validation_status="fail",
    )
    assert state == (
        "FAIL",
        "APPLICABLE_UNRESOLVED",
        "DENY",
        "V550J_OUTPUT_VALIDATION_FAILED",
    )
