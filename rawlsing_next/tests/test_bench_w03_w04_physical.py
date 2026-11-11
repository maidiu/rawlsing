"""Focused sourcefree tests for the W03/W04 physical benchmark harness."""
from __future__ import annotations

import json
import os
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
    assert run["i05_receipt_count"] >= 1
    assert run["i05_fact_count"] >= 1


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
    entry = stage["stage_entry_current_rss_bytes"]
    peak = stage["stage_peak_current_rss_bytes"]
    assert peak >= entry
    # The stage's current-RSS sampler must see the later allocation, not merely
    # replay the process-wide high-water counter.  The 8 MiB allocation is held
    # through stage exit, so a 4 MiB lower bound is conservative and non-vacuous.
    assert peak - entry >= 4 * 1024 * 1024, stage
    # ru_maxrss is a separate cumulative kernel high-water counter.  It is
    # monotone within the process but is not a valid upper bound for a
    # concurrently sampled current-RSS peak (Linux CI demonstrated a small
    # cross-counter difference).  Keep its truthful contract separate.
    assert stage["process_ru_maxrss_after_bytes"] >= stage["process_ru_maxrss_before_bytes"]
    assert stage["rss_peak_bytes"] == stage["process_ru_maxrss_after_bytes"]


def test_stage_peak_is_not_aliased_to_process_highwater(monkeypatch):
    # Deterministic counter-falsifier: even when the cumulative-process counter
    # is deliberately fixed low, the stage metric must remain a separately
    # observed current-RSS value.  This is not a tolerance or a mirror test; it
    # would fail if _stage copied ru_maxrss into the stage peak.
    hold = bytearray(20 * 1024 * 1024)
    assert hold
    monkeypatch.setattr(bench, "_rss_peak_bytes", lambda: 123456)
    value, stage = bench._stage("separate_counter", lambda: 1)
    assert value == 1
    assert stage["process_ru_maxrss_before_bytes"] == 123456
    assert stage["process_ru_maxrss_after_bytes"] == 123456
    assert stage["rss_peak_bytes"] == 123456
    assert stage["stage_peak_current_rss_bytes"] > 123456


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
    assert payload["acceptance"]["cap_pass"] is False


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


def _cap_run(cap_bytes=bench.MAX_CHILD_BYTES):
    return {
        "pid": 1,
        "status": "COMPLETE",
        "cap_bytes": cap_bytes,
        "cap_enforced": True,
        "cap_monitor_active": True,
        "cap_method": bench.CAP_METHOD,
        "cap_peak_sampled_bytes": 1024,
    }


def _receipt_section(aggregate, *, with_cap=True):
    return {
        "aggregate": aggregate,
        "runs": [_cap_run() if with_cap else {"pid": 1, "status": "COMPLETE"}],
    }


def _receipt_profile(aggregate, *, with_cap=True):
    return {
        "cold": _receipt_section(aggregate, with_cap=with_cap),
        "warm": _receipt_section(aggregate, with_cap=with_cap),
        "delete_rebuild": _receipt_section(aggregate, with_cap=with_cap),
        "actual_event_counts": {"cold": [10], "warm": [10], "delete_rebuild": [10]},
        "consumer_fingerprints": {"cold": ["fp"], "warm": ["fp"], "delete_rebuild": ["fp"]},
    }


def _gate_fixture(tmp_path, *, with_cap=True):
    import argparse
    invocation = {
        "command": "python -m rawlsing_next.bench_w03_w04_physical --scenario cold,full-matrix",
        "scenario": "cold,full-matrix",
        "profiles": ["narrow", "wide", "repeat"],
        "rows": 100000,
        "repetitions": 3,
    }
    baseline = {
        "schema": bench.SCHEMA,
        "source_head": bench.EXPECTED_BASELINE_HEAD,
        "method_sha256": bench._method_sha256(),
        "command": invocation["command"],
        "invocation": invocation,
        "rows": 100000,
        "profiles": ["narrow", "wide", "repeat"],
        "repetitions": 3,
        "host": {"node": bench.platform.node()},
        "results": {
            "cold": {
                "narrow": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 100, "median_launch_to_firstconsumer_seconds": 100, "median_parent_wall_seconds": 100}, with_cap=with_cap),
                "wide": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 1000, "median_launch_to_firstconsumer_seconds": 100, "median_parent_wall_seconds": 100}, with_cap=with_cap),
                "repeat": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 100, "median_launch_to_firstconsumer_seconds": 200, "median_parent_wall_seconds": 200}, with_cap=with_cap),
            },
            "full-matrix": {
                "narrow": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 100, "median_launch_to_firstconsumer_seconds": 100, "median_parent_wall_seconds": 100}, with_cap=with_cap),
                "wide": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 100, "median_launch_to_firstconsumer_seconds": 100, "median_parent_wall_seconds": 100}, with_cap=with_cap),
                "repeat": _receipt_profile({"median_cold_to_firstconsumer_stage_peak_rss_bytes": 100, "median_launch_to_firstconsumer_seconds": 100, "median_parent_wall_seconds": 100}, with_cap=with_cap),
            },
        },
    }
    results = json.loads(json.dumps(baseline["results"]))
    results["cold"]["wide"]["cold"]["aggregate"]["median_cold_to_firstconsumer_stage_peak_rss_bytes"] = 100
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(baseline, sort_keys=True) + "\n", encoding="utf-8")
    args = argparse.Namespace(
        rows=100000, repetitions=3, profiles="narrow,wide,repeat",
        scenario="cold,full-matrix", cap_bytes=bench.MAX_CHILD_BYTES,
        baseline_json=str(baseline_path), regression_resolutions={},
        invocation=invocation, method_sha256=bench._method_sha256(),
    )
    return baseline, results, args


def test_acceptance_gate_threshold_and_identity_falsifiers(tmp_path):
    base, results, args = _gate_fixture(tmp_path)
    baseline_sha = __import__("hashlib").sha256((tmp_path / "baseline.json").read_bytes()).hexdigest()
    passing = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert passing["cold_pass"] is True and passing["warm_pass"] is True
    assert passing["pass"] is True
    bad_rows = dict(base, rows=999)
    assert bench._acceptance_gate(results, bad_rows, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)["pass"] is False
    bad_host = dict(base, host={"node": "not-this-host"})
    assert bench._acceptance_gate(results, bad_host, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)["pass"] is False
    cold_only = dict(base, results={"cold": {"wide": base["results"]["cold"]["wide"]}})
    gate = bench._acceptance_gate(results, cold_only, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert gate["pass"] is False and gate["warm_pass"] is False


def test_acceptance_gate_requires_active_cap_evidence(tmp_path):
    base, results, args = _gate_fixture(tmp_path, with_cap=False)
    baseline_sha = __import__("hashlib").sha256((tmp_path / "baseline.json").read_bytes()).hexdigest()
    gate = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert gate["cap_pass"] is False
    assert gate["pass"] is False
    assert gate["cap"]["method"] == bench.CAP_METHOD


def test_acceptance_gate_uses_launch_to_firstconsumer_clock(tmp_path):
    base, results, args = _gate_fixture(tmp_path)
    base["results"]["cold"]["repeat"]["cold"]["aggregate"]["median_launch_to_firstconsumer_seconds"] = 100
    results["full-matrix"]["repeat"]["warm"]["aggregate"]["median_launch_to_firstconsumer_seconds"] = 200
    baseline_sha = __import__("hashlib").sha256((tmp_path / "baseline.json").read_bytes()).hexdigest()
    gate = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert gate["warm_pass"] is False
    assert gate["repeat_wall_ratio"] == 2.0


def test_acceptance_gate_requires_event_command_and_hash_identity(tmp_path):
    base, results, args = _gate_fixture(tmp_path)
    del base["invocation"]
    del base["command"]
    del base["method_sha256"]
    base["results"]["cold"]["wide"].pop("actual_event_counts")
    base["results"]["cold"]["wide"].pop("consumer_fingerprints")
    baseline_sha = __import__("hashlib").sha256((tmp_path / "baseline.json").read_bytes()).hexdigest()
    gate = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=None)
    assert gate["pass"] is False
    assert gate["identity"]["actual_event_counts_match"] is False
    assert gate["identity"]["baseline_file_sha256_matches"] is False


def test_acceptance_gate_other_profile_regression_needs_explicit_resolution(tmp_path):
    base, results, args = _gate_fixture(tmp_path)
    results["cold"]["narrow"]["cold"]["aggregate"]["median_cold_to_firstconsumer_stage_peak_rss_bytes"] = 120
    baseline_sha = __import__("hashlib").sha256((tmp_path / "baseline.json").read_bytes()).hexdigest()
    unresolved = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert unresolved["pass"] is False
    assert unresolved["regression_pass"] is False
    assert unresolved["unresolved_regressions"]
    args.regression_resolutions = {
        "cold/narrow/cold/median_cold_to_firstconsumer_stage_peak_rss_bytes": {
            "status": "JUSTIFIED_CORRECTION",
            "justification": "explicit tiny falsifier: other-profile 20% RSS regression is reported for independent correction",
            "correction": "retain result as diagnostic RED and correct before final scale",
        }
    }
    resolved = bench._acceptance_gate(results, base, args, "candidate", invocation=args.invocation, baseline_sha256=baseline_sha)
    assert resolved["pass"] is True
    assert resolved["regression_pass"] is True
    assert resolved["resolved_regressions"]


def test_derived_amortization_uses_measured_write_and_restart_savings():
    receipt = bench._derived_amortization_receipt(
        [{"metrics": {"derived_write_wall_seconds": 10.0, "canonical_persist_wall_seconds": 100.0}}],
        [{"launch_to_firstconsumer_seconds": 4.0}],
        {"median_launch_to_firstconsumer_seconds": 10.0},
    )
    assert receipt["derived_write_wall_seconds_total"] == 10.0
    assert receipt["warm_restart_savings_seconds"] == 6.0
    assert receipt["break_even_warm_restarts"] == 10.0 / 6.0
    assert receipt["canonical_persist_is_separate"] is True
    assert receipt["repeat_count_is_not_divisor"] is True


def test_same_size_same_mtime_derived_corruption_is_not_a_hit(tmp_path):
    import os
    root = tmp_path / "roots"
    profile = bench._profile("narrow", 24)
    release1, meta1 = bench._build_release(profile, root=root, stages={})
    assert meta1["derived_cache"]["derived_cache_hit"] is False
    path = sorted((root / "derived-accelerator").glob("c11-events-*.parquet"))[0]
    before = path.stat()
    data = bytearray(path.read_bytes())
    import pyarrow.parquet as pq
    data_page_offset = pq.ParquetFile(path).metadata.row_group(0).column(0).data_page_offset
    data[data_page_offset + 8] ^= 0xFF
    path.write_bytes(data)
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    release2, meta2 = bench._build_release(profile, root=root, stages={})
    assert release2.release_ref == release1.release_ref
    assert meta2["derived_cache"]["derived_cache_hit"] is False
    assert meta2["derived_cache"]["derived_cache_write"] is True
    assert meta2["derived_cache"]["write_observations"]


def test_cold_clears_inherited_policy_before_actual_call(tmp_path):
    import os
    foreign = tmp_path / "foreign"
    old_policy = os.environ.get(bench.POLICY_ENV)
    old_legacy = os.environ.get(bench.LEGACY_ENV)
    try:
        bench._ensure_policy(foreign)
        output = tmp_path / "cold.json"
        assert bench.main([
            "--scenario", "cold", "--profiles", "narrow", "--rows", "8",
            "--repetitions", "1", "--jsonpath", str(output),
        ]) == 0
        payload = json.loads(output.read_text(encoding="utf-8"))
        run = payload["results"]["cold"]["narrow"]["cold"]["runs"][0]
        assert not list((foreign / "derived-accelerator").glob("c11-events-*.parquet"))
        assert run["derived_cache"]["status"] == "NO_GOVERNED_DERIVED_CACHE_WRITE"
        assert run["derived_cache"]["derived_cache_hit"] is False
        assert run["env_isolation"]["parent_policy_env_stripped"] is True
        assert run["env_isolation"]["policy_env_present_after_isolation"] is False
    finally:
        if old_policy is None:
            os.environ.pop(bench.POLICY_ENV, None)
        else:
            os.environ[bench.POLICY_ENV] = old_policy
        if old_legacy is None:
            os.environ.pop(bench.LEGACY_ENV, None)
        else:
            os.environ[bench.LEGACY_ENV] = old_legacy


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


def test_full_matrix_uses_own_qualified_policy_when_inherited_policy_exists(tmp_path):
    import os
    foreign = tmp_path / "foreign"
    own_root = tmp_path / "own"
    old_policy = os.environ.get(bench.POLICY_ENV)
    old_legacy = os.environ.get(bench.LEGACY_ENV)
    try:
        bench._ensure_policy(foreign)
        output = tmp_path / "matrix.json"
        assert bench.main([
            "--scenario", "full-matrix", "--profiles", "narrow", "--rows", "8",
            "--repetitions", "1", "--root", str(own_root), "--jsonpath", str(output),
        ]) == 0
        payload = json.loads(output.read_text(encoding="utf-8"))
        result = payload["results"]["full-matrix"]["narrow"]
        cold = result["cold"]["runs"][0]
        warm = result["warm"]["runs"][0]
        assert cold["env_isolation"]["mode"] == "EXPLICIT_OWN_POLICY_FULL_MATRIX"
        assert str(own_root) in (cold["derived_cache"].get("policy_path") or "")
        assert cold["derived_cache_write"] is True
        assert warm["derived_cache_hit"] is True
        assert not list((foreign / "derived-accelerator").glob("c11-events-*.parquet"))
    finally:
        if old_policy is None:
            os.environ.pop(bench.POLICY_ENV, None)
        else:
            os.environ[bench.POLICY_ENV] = old_policy
        if old_legacy is None:
            os.environ.pop(bench.LEGACY_ENV, None)
        else:
            os.environ[bench.LEGACY_ENV] = old_legacy
