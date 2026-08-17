from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from data.ddm_build_copy import ddm_v553_harmonization as legacy
from data.ddm_build_copy.ddm_v553_canonical_harmonization import build_v553_wave_harmonization


def _write_pickle_parquet(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_pickle(path)


def _write_overlay(path: Path, column: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{column: "fixture"}]).to_csv(path, index=False)


def test_v553_harmonization_consumes_canonical_v552j_indexes_without_legacy_packet(tmp_path, monkeypatch):
    monkeypatch.setattr(pd, "read_parquet", lambda path: pd.read_pickle(path))

    v552j_root = tmp_path / "v552j"
    input_path = v552j_root / "packets" / "v552j_v553_input_index.parquet"
    handoff_path = v552j_root / "packets" / "v552j_to_v553_handoff_index.parquet"
    canonical_row = {
        "run_id": "r",
        "v553_input_id": "i1",
        "v552j_packet_id": "p1",
        "source": "GSS",
        "source_family": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "relation_axis_id": "axis-current",
        "target_entity_id": "target-current",
        "driver_facet_id": "driver-current",
        "structural_channel_id": "channel-current",
        "horizon_constraint_id": "horizon-current",
        "semantic_signature": "semantic-current",
        "read_permission": "ALLOW",
        "comparability_status": "COMPARABLE",
        "single_wave_probe_allowed": True,
        "temporal_field_allowed": True,
        "ready_for_v553": True,
        "ready_for_runtime_consumption": False,
    }
    _write_pickle_parquet(pd.DataFrame([canonical_row]), input_path)
    _write_pickle_parquet(pd.DataFrame([canonical_row]), handoff_path)

    readiness_path = v552j_root / "manifest" / "v552j_readiness_report.json"
    readiness_path.parent.mkdir(parents=True, exist_ok=True)
    readiness_path.write_text(
        json.dumps(
            {
                "status": "READY_FOR_V553",
                "downstream_permission_status": "ALLOW",
                "blocker_context_count": 0,
                "blocker_context_breakdown_json": "{}",
            }
        ),
        encoding="utf-8",
    )
    (v552j_root / "manifest" / "v552j_v553_handoff_manifest.json").write_text(
        json.dumps(
            {
                "downstream_permission_status": "ALLOW",
                "v553_input_index_path": "packets/v552j_v553_input_index.parquet",
            }
        ),
        encoding="utf-8",
    )

    authority_dir = tmp_path / "authority"
    overlays = {
        "semantic": authority_dir / "semantic.csv",
        "directionality": authority_dir / "directionality.csv",
        "position": authority_dir / "position.csv",
    }
    _write_overlay(overlays["semantic"], "semantic_role")
    _write_overlay(overlays["directionality"], "response_direction")
    _write_overlay(overlays["position"], "relation_axis_id")
    monkeypatch.setattr(
        legacy,
        "_overlay_path",
        lambda _authority_dir, _source, _wave, kind: overlays[kind],
    )

    legacy_packet = v552j_root / "packets" / "v552j_structural_handoff_packet.json"
    assert not legacy_packet.exists()

    table, report = build_v553_wave_harmonization(
        [
            {
                "wave": "2010",
                "source": "GSS",
                "canonical_wave": "2010",
                "country_code": "US",
                "temporal_year": 2010,
                "authority_dir": str(authority_dir),
                "latest_v552j_root": str(v552j_root),
                "latest_v552j_readiness_report": str(readiness_path),
            }
        ]
    )

    row = table.iloc[0]
    assert row["wave_relation_axis_ids"] == ["axis-current"]
    assert row["wave_target_entity_ids"] == ["target-current"]
    assert row["wave_driver_facet_ids"] == ["driver-current"]
    assert row["wave_structural_channel_ids"] == ["channel-current"]
    assert row["wave_horizon_constraint_ids"] == ["horizon-current"]
    assert row["v552j_consumer_surface"] == "canonical_v552j_input_handoff_indexes"
    assert bool(row["obsolete_v552j_structural_handoff_packet_required"]) is False
    assert report["v552j_consumer_surface"] == "canonical_v552j_input_handoff_indexes"
    assert report["obsolete_v552j_structural_handoff_packet_required"] is False
    assert report["v552j_canonical_surface_by_wave"][0]["surface_present"] is True


def test_v553_compile_entrypoints_use_canonical_consumer_adapter():
    root = Path(__file__).resolve().parents[1]
    for name in (
        "compile_v553_wave_harmonization.py",
        "compile_v553_wave_harmonization_from_repo.py",
    ):
        source = (root / name).read_text(encoding="utf-8")
        assert "ddm_v553_canonical_harmonization import build_v553_wave_harmonization" in source
