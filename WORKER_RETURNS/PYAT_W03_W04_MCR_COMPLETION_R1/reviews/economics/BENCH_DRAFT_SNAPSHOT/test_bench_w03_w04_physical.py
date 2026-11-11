"""Focused sourcefree tests for the W03/W04 physical benchmark harness."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rawlsing_next import bench_w03_w04_physical as bench


@pytest.mark.parametrize("profile_name", ["narrow", "wide", "repeat"])
def test_profiles_build_actual_c11_and_real_i03_i05(profile_name):
    profile = bench._profile(profile_name, 24)
    stages = {}
    release, meta = bench._build_release(profile, stages=stages)
    assert meta["projection_identity"]
    assert release.release_ref.kind == "C11LogicalRelease"
    assert release.public_objects
    assert release.internal_records
    consumer = bench._consumer(profile, release, stages=stages)
    states = [state for item in consumer["i03"] for state in item["fact_states"]]
    assert states == (["SUPPORTED"] if profile_name == "narrow" else ["SUPPORTED", "SUPPORTED"])
    assert consumer["i05_receipt_refs"]
    assert consumer["i05_fact_refs"]
    assert consumer["i05_candidate_count"] >= 1
    assert stages["projection_objectconstruction_canonicalhash"]["rss_peak_bytes"] > 0
    assert stages["i02_validation_seal"]["rss_peak_bytes"] > 0
    assert stages["firstconsumer"]["rss_peak_bytes"] > 0
    if profile_name == "repeat":
        assert profile["repeat_count"] == 3
        assert "repeat_firstconsumer" in stages


def test_cli_cold_small_writes_machine_readable_json(tmp_path):
    output = tmp_path / "cold.json"
    assert bench.main([
        "--scenario", "cold",
        "--profiles", "narrow",
        "--rows", "32",
        "--repetitions", "1",
        "--jsonpath", str(output),
    ]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"] == bench.SCHEMA
    run = payload["results"]["cold"]["narrow"]["cold"]["runs"][0]
    assert run.get("status") != "BLOCKED_EXACT_DEPENDENCY", run.get("stderr")
    assert run["rows"] == 32
    assert run["consumer_fact_count"] == 1
    assert run["consumer_fact_states"] == ["SUPPORTED"]
    assert run["cell_count"] == 96


def test_cli_full_matrix_persists_reopens_and_rebuilds_small(tmp_path):
    output = tmp_path / "matrix.json"
    root = tmp_path / "cache"
    assert bench.main([
        "--scenario", "full-matrix",
        "--profiles", "narrow",
        "--rows", "24",
        "--repetitions", "1",
        "--root", str(root),
        "--jsonpath", str(output),
    ]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    result = payload["results"]["full-matrix"]["narrow"]
    for section in ("cold", "warm", "delete_rebuild"):
        run = result[section]["runs"][0]
        assert run.get("status") != "BLOCKED_EXACT_DEPENDENCY", run.get("stderr")
        assert run["consumer_fact_states"] == ["SUPPORTED"]
    assert result["warm"]["runs"][0]["cache_hit"] is True
    assert result["warm"]["runs"][0]["cache_files"] > 0
    assert result["delete_rebuild"]["runs"][0]["cache_hit"] is False


def test_cells_and_hash_is_explicit_about_non_applicable_decode(tmp_path):
    profile = bench._profile("wide", 16)
    stages = {}
    bench._build_release(profile, stages=stages)
    assert stages["decode"]["status"].startswith("NOT_APPLICABLE")
    assert stages["cells"]["cell_count"] == 96
    assert stages["canonicalhash"]["status"].startswith("COMBINED")
    assert stages["seal"]["stage"] == "seal"
