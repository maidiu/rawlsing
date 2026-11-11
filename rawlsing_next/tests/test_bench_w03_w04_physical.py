"""Focused sourcefree tests for the W03/W04 physical benchmark harness."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rawlsing_next import bench_w03_w04_physical as bench


@pytest.mark.parametrize("profile_name", ["narrow", "wide", "repeat"])
def test_profiles_build_actual_c11_and_real_i03_i05(profile_name, tmp_path):
    profile = bench._profile(profile_name, 24)
    stages = {}
    release, meta = bench._build_release(profile, root=tmp_path / "roots", stages=stages)
    assert meta["projection_identity"]
    assert release.release_ref.kind == "C11LogicalRelease"
    assert release.public_objects
    assert release.internal_records
    assert meta["event_count"] == (48 if profile_name == "narrow" else 144)
    assert meta["derived_cache"]["derived_cache_write"] is True
    assert meta["derived_cache"]["after"]["envelope"]["schema"] == "PRE553_I02_EVENT_ACCELERATOR@2"
    consumer = bench._consumer(profile, release, stages=stages)
    states = [state for item in consumer["i03"] for state in item["fact_states"]]
    assert states == (["SUPPORTED"] if profile_name == "narrow" else ["SUPPORTED", "SUPPORTED"])
    assert consumer["i05_receipt_refs"]
    assert consumer["i05_fact_refs"]
    assert consumer["i05_candidate_count"] >= 1
    assert stages["normal_current_cold_build"]["rss_peak_bytes"] > 0
    assert stages["cold_combined"]["status"].startswith("STREAMING_CELLS")
    assert stages["i02validation"]["status"].startswith("COMBINED_INSIDE")
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
        assert run["canonical_files"] > 0
        assert run["derived_cache_files"] > 0
    assert result["cold"]["runs"][0]["derived_cache_write"] is True
    assert result["warm"]["runs"][0]["derived_cache_hit"] is True
    assert result["warm"]["runs"][0]["canonical_reopen_hit"] is True
    assert result["warm"]["runs"][0]["cache_fingerprint_parity"] is True
    assert result["delete_rebuild"]["runs"][0]["derived_cache_write"] is True


def test_cells_and_hash_is_explicit_about_non_applicable_decode(tmp_path):
    profile = bench._profile("wide", 16)
    stages = {}
    bench._build_release(profile, root=tmp_path / "roots", stages=stages)
    assert stages["decode"]["status"].startswith("NOT_APPLICABLE")
    assert stages["cells"]["cell_count"] == 96
    assert stages["canonicalhash"]["status"].startswith("COMBINED")
    assert stages["seal"]["status"].startswith("COMBINED")


def test_cli_cells_and_hash_uses_same_actual_consumer(tmp_path):
    output = tmp_path / "cells.json"
    assert bench.main([
        "--scenario", "cells-and-hash",
        "--profiles", "wide",
        "--rows", "24",
        "--repetitions", "1",
        "--jsonpath", str(output),
    ]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    run = payload["results"]["cells-and-hash"]["wide"]["cold"]["runs"][0]
    assert run.get("scenario") == "cells-and-hash"
    assert run["consumer_fact_states"] == ["SUPPORTED", "SUPPORTED"]
    assert run["stages"]["cells"]["cell_count"] == 144


def test_derived_cache_is_not_canonical_and_corrupt_cache_is_safe_miss(tmp_path):
    from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier

    root = tmp_path / "roots"
    profile = bench._profile("narrow", 24)
    release1, meta1 = bench._build_release(profile, root=root, stages={})
    derived_files = list((root / "derived-accelerator").glob("c11-events-*.parquet"))
    assert len(derived_files) == 1
    assert meta1["derived_cache"]["derived_cache_write"] is True
    assert meta1["derived_cache"]["after"]["envelope"]["schema"] == "PRE553_I02_EVENT_ACCELERATOR@2"

    canonical = tmp_path / "canonical"
    ParquetC11Carrier(canonical).persist(release1)
    assert list(canonical.glob("releases/**/*.parquet"))
    assert not list(canonical.glob("c11-events-*.parquet"))

    release2, meta2 = bench._build_release(profile, root=root, stages={})
    assert release2.release_ref == release1.release_ref
    assert meta2["derived_cache"]["derived_cache_hit"] is True
    assert meta2["derived_cache"]["derived_cache_write"] is False

    # A corrupt derived slot must be a safe miss/write, never a false hit.
    derived_files[0].write_bytes(b"corrupt-derived-cache")
    release3, meta3 = bench._build_release(profile, root=root, stages={})
    assert release3.release_ref == release1.release_ref
    assert meta3["derived_cache"]["derived_cache_hit"] is False
    assert meta3["derived_cache"]["derived_cache_write"] is True
