#!/usr/bin/env python3
"""Static W03-B regression for the V551J shared producer boundary."""

from __future__ import annotations

import ast
from pathlib import Path


MODULE = Path(__file__).with_name("compile_v551j_joint_evidence_packets.py")


def test_v551j_compiler_source_is_syntactically_valid() -> None:
    ast.parse(MODULE.read_text(encoding="utf-8"), filename=str(MODULE))


def test_v551j_output_manifest_carries_shared_typed_boundary_and_file_hashes() -> None:
    source = MODULE.read_text(encoding="utf-8")
    assert '"contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION' in source
    assert '"boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION' in source
    assert '"run_integrity_status": outputs["readiness_report"].get("run_integrity_status")' in source
    assert '"evidence_status": outputs["readiness_report"].get("evidence_status")' in source
    assert '"downstream_permission_status": outputs["readiness_report"].get("downstream_permission_status")' in source
    assert '"artifact_file_sha256": artifact_hash' in source
    assert 'raise BoundaryContractError("PARQUET_CANONICAL_OUTPUT_REQUIRED")' in source
