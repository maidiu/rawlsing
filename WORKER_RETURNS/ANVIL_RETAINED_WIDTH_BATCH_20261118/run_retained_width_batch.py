#!/usr/bin/env python3
"""One actual retained-WIDTH128 prepared Batch, with hard process caps.

This is a reuse run over the sealed 128x600 WIDTH128 estate.  It builds the
exact forward/reverse F2 catalog from the existing fixture/query provider,
preflights exact refs and independent pins, then supervises exactly one child
driver process.  No baseline is executed here; the earlier qualified baseline
is read only for exact receipt/fact-ref comparison.  No retry occurs after a
started child.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
OWNER = ROOT / "OWNER"
HERE = OWNER / "WORKER_RETURNS" / "ANVIL_RETAINED_WIDTH_BATCH_20261118"
PREP = OWNER / "WORKER_RETURNS" / "ANVIL_FULL_WIDTH_BATCH_PREP_20261118"
SNAPSHOT = Path("/tmp/anvil_retained_width_snapshot")
MP = ROOT / "MEASUREMENT_PREP" / "WORKER_RETURNS" / "ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117"
W = ROOT / "MEASUREMENT_PREP" / "WORKER_RETURNS" / "ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118" / "WIDTH128"
CONTRACT = W / "fixture_contract_width128.json"
BASELINE = MP / ".." / "ANVIL_ROUTING_MATCHED_RUNNER_20261118" / "RUN_aee95429609c" / "baseline.json"
# The path above is normalized below from the actual measurement return.
BASELINE = ROOT / "MEASUREMENT_PREP" / "WORKER_RETURNS" / "ANVIL_ROUTING_MATCHED_RUNNER_20261118" / "RUN_aee95429609c" / "baseline.json"
CHILD = PREP / "full_width_batch_driver.py"
COMMIT = "aee95429609c372564e996c2d3d3eb30e9253cbf"
CAP_SECONDS = 240.0
CAP_RSS = 6 * 1024**3
CAP_SCRATCH = 4 * 1024**3
MIN_FREE = 8 * 1024**3


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def ref_key(value):
    if isinstance(value, str):
        kind, rest = value.split("|", 1)
        obj, digest = rest.rsplit("|", 1)
        return f"{kind}|{obj}|{digest}"
    return f"{value['kind']}|{value['object_id']}|{value['content_hash']}"


def dir_bytes(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        try:
            if p.is_file():
                total += p.stat().st_size
        except OSError:
            pass
    return total


def tree_rss(pid: int) -> int:
    out = subprocess.check_output(["ps", "-axo", "pid=,ppid=,rss="], text=True)
    rows = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        p, pp, rss = map(int, parts)
        rows[p] = (pp, rss * 1024)
    total = 0
    stack = [pid]
    seen = set()
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        total += rows.get(current, (0, 0))[1]
        stack.extend(p for p, (pp, _) in rows.items() if pp == current)
    return total


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    preflight = {"status": "READY", "checks": {}}
    try:
        free = shutil.disk_usage(HERE).free
        preflight["checks"]["free_bytes"] = free
        if free < MIN_FREE:
            raise RuntimeError(f"free space below 8GiB: {free}")

        # Exact sealed WIDTH128 contract and baseline identity.
        width = json.loads(CONTRACT.read_text())
        baseline = json.loads(BASELINE.read_text())
        preflight["checks"]["width_manifest"] = width["manifest_sha256"]
        preflight["checks"]["baseline_manifest"] = baseline.get("estate_manifest")
        if width["manifest_sha256"] != "4d9604dc886ff9655ad25941fdcad2e412d18de4ab07c813524068c1dad09eea":
            raise RuntimeError("WIDTH128 manifest is not the pinned retained manifest")
        if baseline.get("estate_manifest") != width["manifest_sha256"]:
            raise RuntimeError("baseline manifest differs from sealed WIDTH128")
        base_ops = {x["label"]: x for x in baseline["operations"]}
        if set(base_ops) != {"f2_forward", "f2_reverse"}:
            raise RuntimeError("baseline lacks exact forward/reverse operations")

        # Existing fixture/query provider: exact catalog and operation refs.
        # The parent imports the exact source snapshot too, so provider imports
        # resolve rawlsing_next from the same frozen code as the child.
        if SNAPSHOT.exists():
            shutil.rmtree(SNAPSHOT)
        SNAPSHOT.mkdir(parents=True)
        archive = subprocess.check_output([
            "git", "-C", str(ROOT / "IMPLEMENTER"), "archive", COMMIT, "rawlsing_next",
        ])
        subprocess.run(["tar", "-x", "-C", str(SNAPSHOT)], input=archive, check=True)
        sys.path.insert(0, str(SNAPSHOT))
        sys.path.insert(0, str(MP / "vendor"))
        from fixture_1006 import ShapeSpec, build_context
        from query_1006 import build_query_bundle
        ctx = build_context(ShapeSpec("width128", width["respondents"], include_weights=True, tag=width["tag"]))
        bundle = build_query_bundle(ctx)
        fwd_q, fwd_p = bundle.by_name("f2_forward")
        rev_q, rev_p = bundle.by_name("f2_reverse")
        operation_refs = {
            "f2_forward_raw": {"query_ref": fwd_q.ref.as_dict(), "predicate_ref": fwd_p.ref.as_dict()},
            "f2_reverse_raw": {"query_ref": rev_q.ref.as_dict(), "predicate_ref": rev_p.ref.as_dict()},
        }
        # Exact preflight against the earlier qualified direct baseline.
        for ours, base_label in (("f2_forward_raw", "f2_forward"), ("f2_reverse_raw", "f2_reverse")):
            b = base_ops[base_label]
            if ref_key(operation_refs[ours]["query_ref"]) != ref_key(b["query_ref"]):
                raise RuntimeError(f"{ours} query ref differs from baseline")
            if ref_key(operation_refs[ours]["predicate_ref"]) != ref_key(b["predicate_ref"]):
                raise RuntimeError(f"{ours} predicate ref differs from baseline")
        preflight["checks"]["operation_refs"] = operation_refs
        preflight["checks"]["baseline_fact_refs"] = {
            k: v["fact_ref"] for k, v in base_ops.items()
        }
        preflight["checks"]["i02"] = width["i02"]
        preflight["checks"]["release_ref"] = width["reconstructed_v1_release_ref"]
        preflight["checks"]["catalog_counts"] = {
            "authorities": len(bundle.catalog.authorities),
            "predicates": len(bundle.catalog.predicates),
            "queries": len(bundle.catalog.queries),
        }

        # Materialize the exact catalog and sealed receiving contract.
        catalog = {
            "authorities": [x.as_dict() for x in bundle.catalog.authorities],
            "predicates": [x.as_dict() for x in bundle.catalog.predicates],
            "queries": [x.as_dict() for x in bundle.catalog.queries],
            "discovery_authorities": [x.as_dict() for x in bundle.catalog.discovery_authorities],
        }
        sealed = {
            "schema": "ANVIL_RETAINED_WIDTH_BATCH_CONTRACT@1",
            "status": "SEALED_RETAINED_WIDTH128_REUSE",
            "tag": width["tag"],
            "respondents": width["respondents"],
            "questions": width["questions"],
            "root": width["root"],
            "exact_path": width["exact_path"],
            "manifest_sha256": width["manifest_sha256"],
            "i02": width["i02"],
            "reconstructed_v1_release_ref": width["reconstructed_v1_release_ref"],
            "source_wave_country_context": "SYNTHETIC_SINGLE_SOURCE_WAVE_COUNTRY_WIDTH128",
            "operations": operation_refs,
        }
        write_json(HERE / "sealed_contract.json", sealed)
        write_json(HERE / "runtime_catalog.json", catalog)
        write_json(HERE / "PRECHECK.json", preflight)

        env = dict(os.environ)
        env["ANVIL_WIDTH128_CONTRACT"] = str(HERE / "sealed_contract.json")
        env["PYTHONPATH"] = str(HERE)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        cmd = [
            sys.executable, str(CHILD),
            "--snapshot", str(SNAPSHOT),
            "--contract", str(HERE / "sealed_contract.json"),
            "--runtime-catalog", str(HERE / "runtime_catalog.json"),
            "--current-authorizer", "width_current_scope:authorize",
            "--baseline", str(BASELINE),
            "--out", str(HERE / "BATCH_RESULT.json"),
        ]
        start = time.monotonic()
        proc = subprocess.Popen(
            cmd, cwd=str(HERE), env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
        )
        peak_rss = 0
        peak_scratch = 0
        samples = 0
        abort = None
        estate_root = Path(width["root"])
        retained = int(width["retained_bytes"])
        while proc.poll() is None:
            time.sleep(0.2)
            samples += 1
            rss = tree_rss(proc.pid)
            scratch = max(0, dir_bytes(estate_root) - retained) + dir_bytes(HERE / "tmp")
            peak_rss = max(peak_rss, rss)
            peak_scratch = max(peak_scratch, scratch)
            elapsed = time.monotonic() - start
            if elapsed > CAP_SECONDS:
                abort = "CHILD_240S"
            elif rss > CAP_RSS:
                abort = "RSS_6GIB"
            elif scratch > CAP_SCRATCH:
                abort = "SCRATCH_4GIB"
            if abort:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait(timeout=3)
                break
        stdout, stderr = proc.communicate(timeout=20)
        caps = {
            "schema": "ANVIL_RETAINED_WIDTH_BATCH_CAPS@1",
            "limits": {"child_seconds": CAP_SECONDS, "rss": CAP_RSS,
                       "scratch": CAP_SCRATCH, "minimum_free": MIN_FREE},
            "observed": {"exit": proc.returncode, "abort": abort,
                         "wall_seconds": time.monotonic() - start,
                         "samples": samples, "rss_peak": peak_rss,
                         "scratch_peak": peak_scratch,
                         "free_before": free},
            "stdout_tail": stdout[-4000:], "stderr_tail": stderr[-4000:],
        }
        write_json(HERE / "CAPS.json", caps)
        (HERE / "child.stdout.txt").write_text(stdout)
        (HERE / "child.stderr.txt").write_text(stderr)
        if abort or proc.returncode != 0:
            write_json(HERE / "VERDICT.json", {
                "status": "FAILED_BOUNDARY",
                "boundary": abort or f"CHILD_EXIT_{proc.returncode}",
                "caps": caps,
            })
            print(json.dumps({"status": "FAILED_BOUNDARY", "boundary": abort or proc.returncode}, indent=2))
            return 2
        result = json.loads((HERE / "BATCH_RESULT.json").read_text())
        summary = result["batch"]["summary"]
        checks = {
            "one_prepared_session": result["session_scope"]["one_prepared_session"] is True
            and result["session_scope"]["builds_observed"] == 1,
            "two_completed_units": summary["completed_units"] == 2
            and summary["total_units"] == 2 and summary["full_coverage"] is True,
            "distinct_operations": len({x["query_ref"] for x in result["operations"]}) == 2
            and len({x["predicate_ref"] for x in result["operations"]}) == 2,
            "baseline_exact": all(
                r.get("fact_ref_equal") is True
                and r.get("query_ref_equal") is True
                and r.get("predicate_ref_equal") is True
                for r in result["parity"]["operations"]
            ),
            "receipts_present": all(x["receipt_ref"] and x["receipt_hash"] for x in result["operations"]),
            "provenance_present": all(x["provenance_refs"] for x in result["operations"]),
        }
        verdict = {"status": "PASS" if all(checks.values()) else "FAILED_CHECKS",
                   "checks": checks, "result": "BATCH_RESULT.json", "caps": caps}
        write_json(HERE / "VERDICT.json", verdict)
        print(json.dumps(verdict, indent=2))
        return 0 if all(checks.values()) else 2
    except Exception as exc:
        preflight["status"] = "BLOCKED"
        preflight["detail"] = f"{type(exc).__name__}: {exc}"
        write_json(HERE / "PRECHECK.json", preflight)
        write_json(HERE / "VERDICT.json", {"status": "BLOCKED", "detail": preflight["detail"]})
        print(json.dumps(preflight, indent=2))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
