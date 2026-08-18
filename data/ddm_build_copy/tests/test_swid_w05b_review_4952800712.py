from __future__ import annotations

import json
from pathlib import Path

import data.ddm_build_copy.resolve_pipeline_lineage as lineage
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


class _Artifact:
    def __init__(self, *, exists=True, readable=True, row_count=1, error=""):
        self.exists = exists
        self.readable = readable
        self.row_count = row_count
        self.error = error


def _write_v550_manifest(
    root: Path,
    *,
    source: str,
    source_family: str,
    wave: str,
    canonical_wave: str,
    run_id: str,
    shard_id: str,
    source_family_uid: str = "",
    wave_uid: str = "",
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source,
        "source_family": source_family,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "success": True,
    }
    if source_family_uid:
        payload["source_family_uid"] = source_family_uid
    if wave_uid:
        payload["wave_uid"] = wave_uid
    (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    (root / "bridge").mkdir(exist_ok=True)
    (root / "core").mkdir(exist_ok=True)
    (root / "bridge/v551_bridge_index.parquet").write_bytes(b"x")
    (root / "core/question_use_contract.parquet").write_bytes(b"x")


def test_newer_valid_evs_sibling_wave_does_not_block_requested_wave(tmp_path, monkeypatch):
    requested = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    sibling = resolve_source_wave_identity("EVS", "1990", require_closed_35=True)
    base = tmp_path / "data/ddm_repository_copy/v550/shard_runs"

    sibling_root = base / "sibling-newer" / "opaque-sibling"
    _write_v550_manifest(
        sibling_root,
        source="European Values Study",
        source_family="EVS",
        wave="W2",
        canonical_wave="1990",
        run_id="sibling-run",
        shard_id="sibling-shard",
        source_family_uid=sibling.source_family_uid,
        wave_uid=sibling.wave_uid,
    )
    requested_root = base / "requested-older" / "opaque-requested"
    _write_v550_manifest(
        requested_root,
        source="EVS",
        source_family="European Values Study",
        wave="W1",
        canonical_wave="1981",
        run_id="requested-run",
        shard_id="requested-shard",
        source_family_uid=requested.source_family_uid,
        wave_uid=requested.wave_uid,
    )

    monkeypatch.setattr(
        lineage,
        "_manifest_mtime",
        lambda path: 20 if "sibling-newer" in str(path) else 10,
    )
    monkeypatch.setattr(lineage, "inspect_artifact", lambda path: _Artifact())

    resolved = lineage._resolve_v550(tmp_path, requested)
    assert resolved.usable is True
    assert resolved.root == str(requested_root)
    assert resolved.metrics["run_id"] == "requested-run"
    assert resolved.metrics["identity"]["source_family_uid"] == requested.source_family_uid
    assert resolved.metrics["identity"]["wave_uid"] == requested.wave_uid


def test_requested_v550_label_only_manifest_without_explicit_uid_transport_is_not_usable(tmp_path):
    requested = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    root = (
        tmp_path
        / "data/ddm_repository_copy/v550/shard_runs"
        / "label-only"
        / "opaque-requested"
    )
    _write_v550_manifest(
        root,
        source="European Values Study",
        source_family="EVS",
        wave="W1",
        canonical_wave="1981",
        run_id="label-only-run",
        shard_id="label-only-shard",
    )

    resolved = lineage._resolve_v550(tmp_path, requested)
    assert resolved.usable is False
    assert "v550_manifest_explicit_uid_transport_missing" in resolved.reason
