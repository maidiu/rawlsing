#!/usr/bin/env python3
"""W03-B shard-grain identity regression."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import _expected_v551_scope


def test_multi_country_v550j_scope_uses_declared_shard_identity(tmp_path: Path) -> None:
    pattern = pd.DataFrame(
        [
            {"run_id": "r1", "source_family": "EVS", "canonical_wave": "2017", "country_code": "DE"},
            {"run_id": "r1", "source_family": "EVS", "canonical_wave": "2017", "country_code": "FR"},
        ]
    )
    items = pattern.copy()
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(
        json.dumps({
            "run_id": "r1",
            "source": "EVS",
            "shard_id": "EVS__2017",
            "producer_scope_identity": {
                "run_id": "r1",
                "source": "EVS",
                "wave": "2017",
                "canonical_wave": "2017",
                "country_code": "",
                "country_codes": ["DE", "FR"],
                "shard_id": "EVS__2017",
                "scope_kind": "shard"
            }
        }),
        encoding="utf-8",
    )

    scope = _expected_v551_scope("r1", pattern, items, manifest)

    assert scope["scope_kind"] == "shard"
    assert scope["shard_id"] == "EVS__2017"
    assert scope["country_code"] == ""
    assert scope["country_codes"] == ["DE", "FR"]


def test_valid_empty_v550j_scope_can_come_from_typed_manifest(tmp_path: Path) -> None:
    pattern = pd.DataFrame(columns=["run_id", "source_family", "canonical_wave", "country_code"])
    items = pattern.copy()
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(
        json.dumps({
            "run_id": "r1",
            "source": "EVS",
            "shard_id": "EVS__2017",
            "producer_scope_identity": {
                "run_id": "r1",
                "source": "EVS",
                "wave": "2017",
                "canonical_wave": "2017",
                "country_code": "",
                "country_codes": ["DE"],
                "shard_id": "EVS__2017",
                "scope_kind": "shard"
            }
        }),
        encoding="utf-8",
    )

    scope = _expected_v551_scope("r1", pattern, items, manifest)

    assert scope["source"] == "EVS"
    assert scope["wave"] == "2017"
    assert scope["country_codes"] == ["DE"]
    assert scope["shard_id"] == "EVS__2017"
