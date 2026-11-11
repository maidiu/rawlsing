#!/usr/bin/env python3
"""Static contract guards for the G3B V550J -> V551J amendment."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).parent
PRODUCER = ROOT / "compile_v550j_joint_response_patterns.py"
CONSUMER = ROOT / "compile_v551j_joint_evidence_packets.py"
LEGACY_HASH_STATE = "LEGACY_V550J_PRODUCER_DOES_NOT_DECLARE_ARTIFACT_FILE_SHA256"


def test_amended_producer_and_consumer_are_syntactically_valid() -> None:
    ast.parse(PRODUCER.read_text(encoding="utf-8"), filename=str(PRODUCER))
    ast.parse(CONSUMER.read_text(encoding="utf-8"), filename=str(CONSUMER))


def test_v550j_producer_manifest_surface_declares_shared_typed_contract_and_hash() -> None:
    source = PRODUCER.read_text(encoding="utf-8")
    assert '"artifact_file_sha256": _file_sha256(parquet_path)' in source
    assert '"contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION' in source
    assert '"run_integrity_status": run_integrity_status' in source
    assert '"evidence_status": evidence_status' in source
    assert '"downstream_permission_status": downstream_permission_status' in source
    assert '"producer_scope_identity": producer_scope_identity' in source


def test_v551j_no_longer_accepts_legacy_unhashed_v550j_boundary() -> None:
    source = CONSUMER.read_text(encoding="utf-8")
    assert LEGACY_HASH_STATE not in source
    assert "PRODUCER_DECLARED_ARTIFACT_FILE_SHA256_VERIFIED" in source
    assert "V550J_TABLE_ARTIFACT_FILE_SHA256_MISSING_OR_INVALID" in source
    assert "V550J_TABLE_ARTIFACT_FILE_SHA256_MISMATCH" in source
