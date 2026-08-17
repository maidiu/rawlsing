from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy import ddm_pipeline_boundary_contract as boundary
from data.ddm_build_copy import ddm_v553_canonical_harmonization as adapter
from data.ddm_build_copy import ddm_v553_harmonization as legacy
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    ArtifactInspection,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
)
from data.ddm_build_copy.ddm_v552j_handoff import (
    AUDIT_COLUMNS,
    JOIN_COLUMNS,
    V552J_JOIN_COMPILER_VERSION,
    V552J_JOIN_SCHEMA_VERSION,
)
from data.ddm_build_copy.ddm_v553_canonical_harmonization import (
    SURFACE_MISSING,
    SURFACE_SCHEMA_INVALID,
    SURFACE_UNREADABLE,
    SURFACE_VALID_EMPTY,
    SURFACE_VALID_PRESENT,
    V553_CANONICAL_INDEX_REQUIRED_COLUMNS,
    V553CanonicalSurfaceError,
    build_v553_wave_harmonization,
    inspect_v552j_canonical_surface,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_pickle_parquet(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_pickle(path)


def _write_overlay(path: Path, column: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{column: "fixture"}]).to_csv(path, index=False)


def _compat_frame(*, empty: bool = False) -> pd.DataFrame:
    columns = list(V553_CANONICAL_INDEX_REQUIRED_COLUMNS)
    if empty:
        return pd.DataFrame(columns=columns)
    row = {column: "" for column in columns}
    row.update(
        {
            "run_id": "r",
            "v552j_join_id": "j1",
            "packet_id": "p1",
            "v552j_packet_id": "p1",
            "v553_input_id": "j1",
            "source": "GSS",
            "source_family": "GSS",
            "wave": "2010",
            "canonical_wave": "2010",
            "country_code": "US",
            "country": "US",
            "relation_axis_id": "axis-current",
            "target_entity_id": "target-current",
            "driver_facet_id": "driver-current",
            "structural_channel_id": "channel-current",
            "horizon_constraint_id": "horizon-current",
            "structural_dimension_status": "resolved",
            "join_status": "MATCHED_EXACT_SCOPE",
            "join_permission": "ALLOW",
            "allowed_downstream_use": True,
            "ready_for_v553_probe": True,
            "ready_for_v553_temporal_field": False,
            "allowed_for_v553_probe": True,
            "allowed_for_v553_temporal_field": False,
            "v553_handoff_allowed": True,
            "v553_probe_allowed": True,
            "v553_temporal_field_allowed": False,
            "single_wave_probe_allowed": True,
            "ready_for_v553": True,
            "packet_ready_for_v553": True,
            "temporal_field_allowed": False,
            "must_temporalize": True,
            "temporal_anchor_required": True,
            "comparability_required": True,
            "ready_for_runtime_consumption": False,
            "comparability_status": "not_supplied",
            "read_permission": "v553_constraint_candidate",
            "schema_version": V552J_JOIN_SCHEMA_VERSION,
            "compiler_version": V552J_JOIN_COMPILER_VERSION,
        }
    )
    return pd.DataFrame([row], columns=columns)


def _audit_frame(*, empty: bool = True) -> pd.DataFrame:
    if empty:
        return pd.DataFrame(columns=AUDIT_COLUMNS)
    row = {column: "" for column in AUDIT_COLUMNS}
    row.update(
        {
            "run_id": "r",
            "packet_id": "p1",
            "source": "GSS",
            "canonical_wave": "2010",
            "country_code": "US",
            "join_status": "MATCHED_EXACT_SCOPE",
            "reason": "fixture",
            "scope_candidate_count": 1,
            "semantic_match_count": 1,
            "schema_version": V552J_JOIN_SCHEMA_VERSION,
            "compiler_version": V552J_JOIN_COMPILER_VERSION,
        }
    )
    return pd.DataFrame([row], columns=AUDIT_COLUMNS)


def _artifact_decl(root: Path, relative: str, name: str, kind: str) -> dict[str, object]:
    path = root / relative
    return {
        "artifact": name,
        "path": relative,
        "artifact_kind": kind,
        "row_count": int(len(pd.read_pickle(path))),
        "artifact_file_sha256": _sha(path),
        "schema_version": V552J_JOIN_SCHEMA_VERSION,
        "compiler_version": V552J_JOIN_COMPILER_VERSION,
    }


def _write_v552j_publication(
    root: Path,
    *,
    empty: bool = False,
    evidence_status: str | None = None,
    permission_status: str | None = None,
) -> dict[str, Path]:
    compat = _compat_frame(empty=empty)
    join = compat.loc[:, JOIN_COLUMNS].copy()
    audit = _audit_frame(empty=True)
    paths = {
        "join": root / "packets/v552j_structural_join_index.parquet",
        "audit": root / "audits/v552j_join_audit.parquet",
        "input": root / "packets/v552j_v553_input_index.parquet",
        "handoff": root / "packets/v552j_to_v553_handoff_index.parquet",
    }
    for key, frame in (("join", join), ("audit", audit), ("input", compat), ("handoff", compat.copy())):
        _write_pickle_parquet(frame, paths[key])

    evidence = evidence_status or ("VALID_EMPTY" if empty else "PRESENT")
    permission = permission_status or ("NOT_APPLICABLE" if empty else "ALLOW")
    state = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": "r",
        "run_id": "r",
        "source": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "shard_id": "",
        "producer_scope_identity": {
            "run_id": "r",
            "source": "GSS",
            "wave": "2010",
            "canonical_wave": "2010",
            "country_code": "US",
            "shard_id": "",
        },
        "schema_version": V552J_JOIN_SCHEMA_VERSION,
        "compiler_version": V552J_JOIN_COMPILER_VERSION,
        "run_integrity_status": "PASS",
        "evidence_status": evidence,
        "downstream_permission_status": permission,
        "blocker_context_count": 0,
        "blocker_context_breakdown_json": "{}",
    }
    manifest = {
        **state,
        "canonical_artifact_names": ["v552j_structural_join_index", "v552j_join_audit"],
        "artifacts": [
            _artifact_decl(root, "packets/v552j_structural_join_index.parquet", "v552j_structural_join_index", "canonical"),
            _artifact_decl(root, "audits/v552j_join_audit.parquet", "v552j_join_audit", "canonical"),
            _artifact_decl(root, "packets/v552j_v553_input_index.parquet", "v552j_v553_input_index", "compatibility"),
            _artifact_decl(root, "packets/v552j_to_v553_handoff_index.parquet", "v552j_to_v553_handoff_index", "compatibility"),
        ],
    }
    manifest_path = root / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    readiness_path = root / "manifest/v552j_readiness_report.json"
    readiness_path.parent.mkdir(parents=True, exist_ok=True)
    readiness_path.write_text(json.dumps(state), encoding="utf-8")
    handoff_manifest_path = root / "manifest/v552j_v553_handoff_manifest.json"
    handoff_manifest_path.write_text(
        json.dumps(
            {
                **state,
                "v553_input_index_path": "packets/v552j_v553_input_index.parquet",
                "v553_probe_row_count": 0 if empty else 1,
                "v553_temporal_field_row_count": 0,
            }
        ),
        encoding="utf-8",
    )
    paths.update(
        {
            "manifest": manifest_path,
            "readiness": readiness_path,
            "handoff_manifest": handoff_manifest_path,
        }
    )
    return paths


def _descriptor(root: Path, authority_dir: Path | None = None) -> dict[str, object]:
    return {
        "wave": "2010",
        "source": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "temporal_year": 2010,
        "authority_dir": str(authority_dir) if authority_dir else "",
        "latest_v552j_root": str(root),
        "latest_v552j_readiness_report": str(root / "manifest/v552j_readiness_report.json"),
    }


@pytest.fixture(autouse=True)
def _portable_parquet(monkeypatch):
    monkeypatch.setattr(pd, "read_parquet", lambda path: pd.read_pickle(path))
    monkeypatch.setattr(boundary, "_parquet_row_count", lambda path: int(len(pd.read_pickle(path))))


def test_v553_harmonization_consumes_fully_verified_v552j_publication_without_legacy_packet(tmp_path, monkeypatch):
    v552j_root = tmp_path / "v552j"
    _write_v552j_publication(v552j_root)

    authority_dir = tmp_path / "authority"
    overlays = {
        "semantic": authority_dir / "semantic.csv",
        "directionality": authority_dir / "directionality.csv",
        "position": authority_dir / "position.csv",
    }
    _write_overlay(overlays["semantic"], "semantic_role")
    _write_overlay(overlays["directionality"], "response_direction")
    _write_overlay(overlays["position"], "relation_axis_id")
    monkeypatch.setattr(legacy, "_overlay_path", lambda _authority_dir, _source, _wave, kind: overlays[kind])

    legacy_packet = v552j_root / "packets/v552j_structural_handoff_packet.json"
    assert not legacy_packet.exists()

    table, report = build_v553_wave_harmonization([_descriptor(v552j_root, authority_dir)])
    row = table.iloc[0]
    assert row["wave_relation_axis_ids"] == ["axis-current"]
    assert row["wave_target_entity_ids"] == ["target-current"]
    assert row["wave_driver_facet_ids"] == ["driver-current"]
    assert row["wave_structural_channel_ids"] == ["channel-current"]
    assert row["wave_horizon_constraint_ids"] == ["horizon-current"]
    assert row["v552j_consumer_surface_status"] == SURFACE_VALID_PRESENT
    assert bool(row["v552j_consumer_surface_valid"]) is True
    assert report["v552j_consumer_surface_validation"] == "fail_closed_full_publication_verification"
    assert report["v552j_canonical_surface_by_wave"][0]["surface_status"] == SURFACE_VALID_PRESENT
    assert report["v552j_canonical_surface_by_wave"][0]["surface_valid"] is True
    assert report["obsolete_v552j_structural_handoff_packet_required"] is False


def test_valid_empty_publication_is_distinct_from_missing_or_corrupt(tmp_path):
    root = tmp_path / "v552j"
    _write_v552j_publication(root, empty=True)
    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_VALID_EMPTY
    assert context["surface_valid"] is True
    assert context["surface_present"] is True
    assert context["relation_axis_ids"] == []


def test_incomplete_publication_missing_required_handoff_index_fails_closed(tmp_path):
    root = tmp_path / "v552j"
    paths = _write_v552j_publication(root)
    paths["handoff"].unlink()
    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_MISSING
    assert context["surface_valid"] is False
    assert context["surface_present"] is False
    with pytest.raises(V553CanonicalSurfaceError, match="CANONICAL_SURFACE_MISSING"):
        build_v553_wave_harmonization([_descriptor(root)])


def test_corrupt_canonical_input_index_fails_closed_as_unreadable(tmp_path):
    root = tmp_path / "v552j"
    paths = _write_v552j_publication(root)
    paths["input"].write_bytes(b"not-a-parquet-or-pickle")
    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_UNREADABLE
    assert context["surface_valid"] is False
    with pytest.raises(V553CanonicalSurfaceError, match="CANONICAL_SURFACE_UNREADABLE_OR_CORRUPT"):
        build_v553_wave_harmonization([_descriptor(root)])


def test_unreadable_canonical_handoff_index_fails_closed(tmp_path, monkeypatch):
    root = tmp_path / "v552j"
    paths = _write_v552j_publication(root)
    real_inspect = adapter.inspect_artifact

    def unreadable_handoff(path):
        path = Path(path)
        if path == paths["handoff"]:
            return ArtifactInspection(str(path), True, False, None, _sha(path), "READ_ERROR:PermissionError:denied")
        return real_inspect(path)

    monkeypatch.setattr(adapter, "inspect_artifact", unreadable_handoff)
    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_UNREADABLE
    assert context["surface_valid"] is False
    with pytest.raises(V553CanonicalSurfaceError, match="CANONICAL_SURFACE_UNREADABLE_OR_CORRUPT"):
        build_v553_wave_harmonization([_descriptor(root)])


def test_schema_invalid_canonical_index_fails_closed_even_when_hash_and_row_count_match(tmp_path):
    root = tmp_path / "v552j"
    paths = _write_v552j_publication(root)
    frame = pd.read_pickle(paths["input"]).drop(columns=["read_permission"])
    _write_pickle_parquet(frame, paths["input"])
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    for declaration in manifest["artifacts"]:
        if declaration["artifact"] == "v552j_v553_input_index":
            declaration["artifact_file_sha256"] = _sha(paths["input"])
            declaration["row_count"] = int(len(frame))
    paths["manifest"].write_text(json.dumps(manifest), encoding="utf-8")

    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_SCHEMA_INVALID
    assert context["surface_valid"] is False
    with pytest.raises(V553CanonicalSurfaceError, match="CANONICAL_SURFACE_SCHEMA_INVALID"):
        build_v553_wave_harmonization([_descriptor(root)])


def test_path_existence_alone_never_marks_surface_valid(tmp_path):
    root = tmp_path / "v552j"
    paths = _write_v552j_publication(root)
    paths["manifest"].write_text("{not-json", encoding="utf-8")
    assert paths["input"].exists() and paths["handoff"].exists()
    context = inspect_v552j_canonical_surface(_descriptor(root))
    assert context["surface_status"] == SURFACE_UNREADABLE
    assert context["surface_valid"] is False
    assert context["surface_present"] is False


def test_v553_compile_entrypoints_use_canonical_consumer_adapter():
    root = Path(__file__).resolve().parents[1]
    for name in (
        "compile_v553_wave_harmonization.py",
        "compile_v553_wave_harmonization_from_repo.py",
    ):
        source = (root / name).read_text(encoding="utf-8")
        assert "ddm_v553_canonical_harmonization import build_v553_wave_harmonization" in source
