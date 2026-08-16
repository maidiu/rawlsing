#!/usr/bin/env python3
"""W03-B valid-empty V550J -> V551J typed-stop regression."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import (
    _clear_v551j_stage_outputs,
    _write_v550j_typed_stop,
)
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs


def test_valid_empty_v550j_surface_stops_cleanly_without_packet_artifacts(tmp_path: Path) -> None:
    output_dirs = ensure_output_dirs(tmp_path / "v551j", "r1")
    stale = output_dirs["packets"] / "v551j_packet_candidate_trace.parquet"
    stale.write_bytes(b"stale")
    _clear_v551j_stage_outputs(output_dirs)
    args = SimpleNamespace(run_id="r1", strict=True)
    surface_report = {
        "producer_evidence_status": "VALID_EMPTY",
        "producer_downstream_permission_status": "NOT_APPLICABLE",
        "producer_state_detail": "VALID_EMPTY_NO_JOINT_PATTERN_EVIDENCE",
        "producer_contract_version": "rawlsing_pipeline_boundary_v1",
        "producer_schema_version": "v1",
        "producer_compiler_version": "v550j_joint_response_patterns_producer_v1",
        "producer_run_integrity_status": "PASS",
        "producer_artifact_hash_contract_status": "PRODUCER_DECLARED_ARTIFACT_FILE_SHA256_VERIFIED",
        "manifest_sha256": "a" * 64,
        "source": "EVS",
        "wave": "2017",
        "shard_id": "EVS__2017",
        "tables": {},
    }

    exit_code = _write_v550j_typed_stop(
        args=args,
        output_dirs=output_dirs,
        surface_report=surface_report,
        started=0.0,
    )

    assert exit_code == 0
    assert not stale.exists()
    assert list(output_dirs["packets"].iterdir()) == []
    readiness = json.loads((output_dirs["manifest"] / "v551j_readiness_report.json").read_text(encoding="utf-8"))
    manifest = json.loads((output_dirs["manifest"] / "manifest.json").read_text(encoding="utf-8"))
    assert readiness["run_integrity_status"] == "PASS"
    assert readiness["evidence_status"] == "VALID_EMPTY"
    assert readiness["downstream_permission_status"] == "NOT_APPLICABLE"
    assert readiness["ready_for_v552j_joint_evidence"] is False
    assert manifest["artifacts"] == []
    assert manifest["output_artifacts"] == {}
    assert manifest["v550j_upstream_hash_contract_status"] == "PRODUCER_DECLARED_ARTIFACT_FILE_SHA256_VERIFIED"
