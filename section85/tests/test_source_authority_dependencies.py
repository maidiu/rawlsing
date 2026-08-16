from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
V551_REGISTRY = ROOT / "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv"
V551_MANIFEST = ROOT / "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json"
ASSOCIATION_THRESHOLD = ROOT / "data/ddm_registries/association_threshold_profiles.yaml"
ASSOCIATION_LANE = ROOT / "data/ddm_registries/association_lane_registry.yaml"
ASSOCIATION_DEPENDENCIES = ROOT / "data/ddm_registries/GOVERNED_ASSOCIATION_REGISTRIES.json"
ASSOCIATION_MATERIALIZER = ROOT / "data/ddm_registries/materialize_governed_association_registries.py"

V551_REGISTRY_SHA256 = "d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8"
ASSOCIATION_THRESHOLD_SHA256 = "8d4e11b507bb4626e4c08fe508b0ea1fd196cfdeb211f90fb08634ac0c82259b"
ASSOCIATION_LANE_SHA256 = "1848ae6b1c0823cfe7d34e34f71076543484a67a4721ea4de0d9ffef25b5d138"
ASSOCIATION_LANE_SIZE = 5_539_418


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def test_v551_scale_registry_is_exact_pinned_authority() -> None:
    assert V551_REGISTRY.is_file()
    assert sha256(V551_REGISTRY) == V551_REGISTRY_SHA256
    manifest = json.loads(V551_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["registry_path"] == "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv"
    assert manifest["registry_sha256"] == V551_REGISTRY_SHA256


def test_association_threshold_profile_is_exact_pinned_authority() -> None:
    assert ASSOCIATION_THRESHOLD.is_file()
    assert ASSOCIATION_THRESHOLD.stat().st_size == 2558
    assert sha256(ASSOCIATION_THRESHOLD) == ASSOCIATION_THRESHOLD_SHA256


def test_association_lane_is_explicit_external_fail_closed_dependency() -> None:
    dependency = json.loads(ASSOCIATION_DEPENDENCIES.read_text(encoding="utf-8"))
    lane = next(row for row in dependency["registries"] if row["path"].endswith("association_lane_registry.yaml"))
    assert lane["delivery"] == "external_governed_dependency"
    assert lane["sha256"] == ASSOCIATION_LANE_SHA256
    assert lane["size_bytes"] == ASSOCIATION_LANE_SIZE
    assert lane["missing_behavior"] == "FAIL_CLOSED_NO_HARDCODED_SUBSTITUTE"

    if ASSOCIATION_LANE.exists():
        assert ASSOCIATION_LANE.stat().st_size == ASSOCIATION_LANE_SIZE
        assert sha256(ASSOCIATION_LANE) == ASSOCIATION_LANE_SHA256
        return

    result = subprocess.run(
        [sys.executable, str(ASSOCIATION_MATERIALIZER), "--repo-root", str(ROOT)],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "ASSOCIATION_LANE_EXTERNAL_DEPENDENCY_REQUIRED" in (result.stdout + result.stderr)


def test_retained_external_lane_bytes_match_if_fixture_is_supplied() -> None:
    external = os.environ.get("RAWLSING_ASSOCIATION_LANE_AUTHORITY")
    if not external:
        pytest.skip("set RAWLSING_ASSOCIATION_LANE_AUTHORITY to verify retained external governed bytes")
    path = Path(external)
    assert path.stat().st_size == ASSOCIATION_LANE_SIZE
    assert sha256(path) == ASSOCIATION_LANE_SHA256
