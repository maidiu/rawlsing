from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

import data.ddm_build_copy.resolve_pipeline_lineage as r
from data.ddm_build_copy.ddm_pipeline_boundary_contract import DependencyLedgerError


def _ready(path: Path, status: str = "READY_V550") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status}), encoding="utf-8")


def test_missing_default_dependency_ledger_is_not_opened(tmp_path: Path) -> None:
    assert r._load_dependency_ledger(None) is None


def test_external_ledger_requires_verified_hash(tmp_path: Path) -> None:
    p = tmp_path / "ledger.json"
    p.write_text(json.dumps({"stages": {}}), encoding="utf-8")
    with pytest.raises(DependencyLedgerError):
        r._load_dependency_ledger(p, "0" * 64)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    assert r._load_dependency_ledger(p, digest) == {"stages": {}}


def test_malformed_required_readiness_fails_closed(tmp_path: Path) -> None:
    root = tmp_path / "run"
    root.mkdir()
    (root / "manifest.json").write_text("{bad", encoding="utf-8")
    result = r._validate_root(root, stage="x", required_files=("manifest.json",), status_paths=("manifest.json",), ready_key_names=("status",))
    assert result.usable is False
    assert "unreadable required file" in result.reason or "unverifiable" in result.reason


def test_unknown_status_fails_closed(tmp_path: Path) -> None:
    root = tmp_path / "run"
    root.mkdir()
    _ready(root / "manifest.json", "MAYBE_READY_LATER")
    result = r._validate_root(root, stage="x", required_files=("manifest.json",), status_paths=("manifest.json",), ready_key_names=("status",))
    assert result.usable is False
    assert "unverifiable" in result.reason


def test_corrupt_parquet_is_not_valid_empty(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "run"
    root.mkdir()
    p = root / "a.parquet"
    p.write_bytes(b"bad")
    _ready(root / "manifest.json")
    monkeypatch.setattr(pd, "read_parquet", lambda _p: (_ for _ in ()).throw(ValueError("corrupt")))
    result = r._validate_root(root, stage="x", required_files=("a.parquet", "manifest.json"), status_paths=("manifest.json",), ready_key_names=("status",))
    assert result.usable is False
    assert "unreadable required file" in result.reason


def test_v550j_resolution_is_exactly_bound_to_selected_v550_run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo = tmp_path
    v550 = repo / "data/ddm_repository_copy/v550/shard_runs/run_old/GSS__2010"
    v550.mkdir(parents=True)
    newer_wrong = repo / "data/ddm_repository_copy/v550j/runs/run_new/GSS__2010/joint_patterns"
    newer_wrong.mkdir(parents=True)

    calls: list[tuple[str, Path]] = []
    def fake_latest(*args, **kwargs):
        return r.StageResolution("v550", str(v550), True, "READY_V550")
    def fake_validate(root: Path, *, stage: str, **kwargs):
        calls.append((stage, Path(root)))
        return r.StageResolution(stage, str(root), False, "BLOCKED", "fixture")
    monkeypatch.setattr(r, "_latest_usable_candidate", fake_latest)
    monkeypatch.setattr(r, "_validate_root", fake_validate)
    r.resolve_stage_roots(repo, "GSS", "2010")
    v550j_call = next(path for stage, path in calls if stage == "v550j")
    assert v550j_call == repo / "data/ddm_repository_copy/v550j/runs/run_old"
    assert "run_new" not in str(v550j_call)
