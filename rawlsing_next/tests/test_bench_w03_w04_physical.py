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
    assert run["derived_cache_files"] == 0
    assert run.get("canonical_files", 0) == 0
    assert run["derived_cache"]["status"] == "NO_GOVERNED_DERIVED_CACHE_WRITE"


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


def test_stage_peak_tracks_post_highwater_allocation():
    import time as _time
    hold = bytearray(20 * 1024 * 1024)
    assert hold
    def alloc():
        _time.sleep(0.08)
        return bytearray(8 * 1024 * 1024)
    value, stage = bench._stage("later_allocation", alloc)
    assert len(value) == 8 * 1024 * 1024
    assert stage["stage_peak_current_rss_bytes"] >= stage["stage_entry_current_rss_bytes"]
    assert stage["process_ru_maxrss_after_bytes"] >= stage["stage_peak_current_rss_bytes"]


def test_small_cap_refuses_over_limit_without_host_stress(tmp_path):
    output = tmp_path / "cap.json"
    rc = bench.main([
        "--scenario", "cold", "--profiles", "narrow", "--rows", "16",
        "--repetitions", "1", "--cap-bytes", str(8 * 1024 * 1024),
        "--root", str(tmp_path / "cache"), "--jsonpath", str(output),
    ])
    assert rc == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    run = payload["results"]["cold"]["narrow"]["cold"]["runs"][0]
    assert run["status"] == "BLOCKED_EXACT_DEPENDENCY"
    assert run["cap_enforced"] is True
    assert run["blocked_reason"] == "CHILD_RSS_EXCEEDED_AUTHORIZED_CAP_BEFORE_COMPLETION"


def test_acceptance_gate_requires_baseline_and_is_nonzero(tmp_path):
    output = tmp_path / "gate.json"
    rc = bench.main([
        "--scenario", "cold", "--profiles", "wide", "--rows", "16",
        "--repetitions", "1", "--acceptance-gate", "--jsonpath", str(output),
    ])
    assert rc == 2
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["acceptance"]["status"] == "NO_BASELINE"
    assert payload["acceptance"]["pass"] is False


def _synthetic_baseline(rows=100000, reps=3, host=None, source_head=bench.EXPECTED_BASELINE_HEAD):
    return {
        "schema": bench.SCHEMA,
        "source_head": source_head,
        "rows": rows,
        "profiles": ["narrow", "wide", "repeat"],
        "repetitions": reps,
        "host": {"node": host or bench.platform.node()},
        "results": {
            "cold": {
                "wide": {"cold": {"aggregate": {
                    "median_cold_to_firstconsumer_stage_peak_rss_bytes": 1000,
                    "median_parent_wall_seconds": 100,
                }}},
                "repeat": {"cold": {"aggregate": {
                    "median_cold_to_firstconsumer_stage_peak_rss_bytes": 100,
                    "median_parent_wall_seconds": 200,
                }}},
            },
        },
    }


def test_acceptance_gate_threshold_and_identity_falsifiers(monkeypatch):
    import argparse
    args = argparse.Namespace(rows=100000, repetitions=3, profiles="narrow,wide,repeat", scenario="cold,full-matrix")
    results = {
        "cold": {"wide": {"cold": {"aggregate": {
            "median_cold_to_firstconsumer_stage_peak_rss_bytes": 99,
            "median_parent_wall_seconds": 99,
        }}}},
        "full-matrix": {"repeat": {"warm": {"aggregate": {
            "median_parent_wall_seconds": 99,
            "median_cold_to_firstconsumer_stage_peak_rss_bytes": 99,
        }}}},
    }
    base = _synthetic_baseline()
    passing = bench._acceptance_gate(results, base, args, "candidate")
    assert passing["cold_pass"] is True and passing["warm_pass"] is True
    assert passing["pass"] is True
    bad_rows = dict(base, rows=999)
    assert bench._acceptance_gate(results, bad_rows, args, "candidate")["pass"] is False
    bad_host = dict(base, host={"node": "not-this-host"})
    assert bench._acceptance_gate(results, bad_host, args, "candidate")["pass"] is False
    cold_only = dict(base, results={"cold": {"wide": base["results"]["cold"]["wide"]}})
    gate = bench._acceptance_gate(results, cold_only, args, "candidate")
    assert gate["pass"] is False and gate["warm_pass"] is False


def test_full_matrix_three_fresh_warm_restarts_share_persisted_root(tmp_path):
    output = tmp_path / "restarts.json"
    rc = bench.main([
        "--scenario", "full-matrix", "--profiles", "narrow",
        "--rows", "16", "--repetitions", "3",
        "--root", str(tmp_path / "cache"), "--jsonpath", str(output),
    ])
    assert rc == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    result = payload["results"]["full-matrix"]["narrow"]
    assert result["warm_fresh_process_count"] == 3
    assert len(set(result["warm_fresh_process_pids"])) == 3
    assert all(x["derived_cache_hit"] for x in result["warm"]["runs"])
    assert all(x["canonical_reopen_hit"] for x in result["warm"]["runs"])
    assert result["cache_write_amortization"] is not None
    assert payload["final_matrix_eligible"] is False
