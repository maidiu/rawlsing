#!/usr/bin/env python3
"""W03-B V550J producer-surface binding regression."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import _verify_v550j_producer_surface
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError


def _frame(run_id: str = "r1") -> pd.DataFrame:
    return pd.DataFrame([{"run_id": run_id, "source_family": "EVS", "canonical_wave": "2017", "country_code": "DE"}])


def test_v550j_declared_paths_and_rows_are_bound(tmp_path: Path) -> None:
    frames = {}
    tables = {}
    for table_name in (
        "joint_response_pattern_index",
        "joint_response_pattern_item_index",
        "joint_pattern_relation_signature",
    ):
        path = tmp_path / f"{table_name}.parquet"
        frame = _frame()
        frame.to_parquet(path, index=False)
        frames[table_name] = (path, frame)
        tables[table_name] = {"parquet_path": str(path), "rows": 1}
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(json.dumps({"run_id": "r1", "source": "EVS", "shard_id": "", "tables": tables}), encoding="utf-8")
    readiness = tmp_path / "v550j_readiness.json"
    readiness.write_text(json.dumps({"run_id": "r1", "source": "EVS", "readiness_status": "validated_for_internal_analysis"}), encoding="utf-8")

    report = _verify_v550j_producer_surface(
        run_id="r1",
        manifest_path=manifest,
        readiness_path=readiness,
        expected_scope={"source": "EVS", "wave": "2017", "country_codes": ["DE"], "country_code": "DE", "shard_id": ""},
        table_inputs=frames,
    )

    assert report["producer_artifact_hash_contract_status"] == "LEGACY_V550J_PRODUCER_DOES_NOT_DECLARE_ARTIFACT_FILE_SHA256"
    assert report["tables"]["joint_response_pattern_index"]["row_count"] == 1


def test_v550j_wrong_declared_path_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "joint_response_pattern_index.parquet"
    frame = _frame()
    frame.to_parquet(path, index=False)
    tables = {
        "joint_response_pattern_index": {"parquet_path": str(tmp_path / "wrong.parquet"), "rows": 1},
        "joint_response_pattern_item_index": {"parquet_path": str(path), "rows": 1},
        "joint_pattern_relation_signature": {"parquet_path": str(path), "rows": 1},
    }
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(json.dumps({"run_id": "r1", "source": "EVS", "tables": tables}), encoding="utf-8")
    readiness = tmp_path / "v550j_readiness.json"
    readiness.write_text(json.dumps({"run_id": "r1", "source": "EVS"}), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_TABLE_PATH_MISMATCH"):
        _verify_v550j_producer_surface(
            run_id="r1",
            manifest_path=manifest,
            readiness_path=readiness,
            expected_scope={"source": "EVS", "wave": "2017", "country_codes": ["DE"], "country_code": "DE", "shard_id": ""},
            table_inputs={
                "joint_response_pattern_index": (path, frame),
                "joint_response_pattern_item_index": (path, frame),
                "joint_pattern_relation_signature": (path, frame),
            },
        )
