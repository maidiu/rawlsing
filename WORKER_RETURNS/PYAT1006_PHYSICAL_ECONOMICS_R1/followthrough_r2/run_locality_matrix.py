"""Run baseline/candidate locality pairs on reviewer-retained accepted estates."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Any

HERE = Path(__file__).resolve().parent
AUTHOR_ROOT = HERE.parent
REPO = AUTHOR_ROOT.parents[1]
sys.path.insert(0, str(AUTHOR_ROOT))
from resources_1006 import CAP_BYTES, disk, host_info, run_monitored

REVIEW_DATA = Path(
    "/Users/matthewsmith/.codex/worktrees/pyat1007-dual-series-prep/Rawlsing/"
    "WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/data"
)
CASES = {
    "diag-1k": REVIEW_DATA / "diag-1k" / "capsule.json",
    "diag-10k": REVIEW_DATA / "diag-10k" / "capsule.json",
    "hist-100k": REVIEW_DATA / "hist-100k" / "capsule.json",
}
QUERIES = {
    "diag-1k": "selected,f2_reverse,f4_three",
    "diag-10k": "selected,f2_reverse,f4_three",
    "hist-100k": "selected",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(
    case: str, mode: str, queries: str, *, outdir: Path, env: dict[str, str],
    timeout: int,
) -> dict[str, Any]:
    capsule = CASES[case]
    out = outdir / f"{case}.{mode}.json"
    command = [
        sys.executable, str(HERE / "locality_probe.py"),
        "--capsule", str(capsule),
        "--mode", mode,
        "--queries", queries,
        "--out", str(out),
    ]
    monitored = run_monitored(
        command, cwd=REPO, env=env, timeout_seconds=timeout,
        cap_bytes=CAP_BYTES,
    )
    result: dict[str, Any] = {
        "case": case,
        "mode": mode,
        "queries": queries,
        "capsule": str(capsule),
        "capsule_sha256": _sha(capsule),
        "command": command,
        "returncode": monitored["returncode"],
        "timed_out": monitored["timed_out"],
        "killed_for_cap": monitored["killed_for_cap"],
        "seconds": monitored["seconds"],
        "process_tree": monitored["process_tree"],
        "disk_after": monitored["disk_after"],
        "stderr_tail": monitored["stderr"][-3000:],
        "stdout_tail": monitored["stdout"][-3000:],
    }
    if out.exists():
        result["probe"] = json.loads(out.read_text(encoding="utf-8"))
    else:
        result["probe"] = None
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--cases", default="diag-1k,diag-10k")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result: dict[str, Any] = {
        "schema": "PYAT1006_LOCALITY_MATRIX@1",
        "label": "EXPERIMENT_NOT_IMPLEMENTED",
        "host": host_info(outdir),
        "cases": {},
        "queries": QUERIES,
        "cap_bytes": CAP_BYTES,
        "review_data": str(REVIEW_DATA),
        "status": "RUNNING",
    }
    path = outdir / "locality_matrix.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for case in [value for value in args.cases.split(",") if value]:
        queries = QUERIES[case]
        pair: dict[str, Any] = {"queries": queries, "runs": {}}
        for mode in ("baseline", "candidate"):
            pair["runs"][mode] = _run(
                case, mode, queries, outdir=outdir, env=env, timeout=args.timeout,
            )
            path.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        baseline = pair["runs"]["baseline"].get("probe") or {}
        candidate = pair["runs"]["candidate"].get("probe") or {}
        comparison: dict[str, Any] = {}
        for name in [value for value in queries.split(",") if value]:
            left = (baseline.get("queries") or {}).get(name, {})
            right = (candidate.get("queries") or {}).get(name, {})
            comparison[name] = {
                "fact_refs_equal": [
                    fact.get("ref") for fact in left.get("facts", ())
                ] == [fact.get("ref") for fact in right.get("facts", ())],
                "projection_sha256_equal": [
                    fact.get("projection_sha256") for fact in left.get("facts", ())
                ] == [fact.get("projection_sha256") for fact in right.get("facts", ())],
                "replay_refs_equal": [
                    fact.get("replay_ref") for fact in left.get("facts", ())
                ] == [fact.get("replay_ref") for fact in right.get("facts", ())],
                "release_refs_equal": left.get("release_refs") == right.get("release_refs"),
                "baseline_wall_seconds": left.get("wall_seconds"),
                "candidate_wall_seconds": right.get("wall_seconds"),
                "baseline_cpu_seconds": left.get("cpu_seconds"),
                "candidate_cpu_seconds": right.get("cpu_seconds"),
                "baseline_reads": (left.get("reads") or {}).get("total_reads"),
                "candidate_reads": (right.get("reads") or {}).get("total_reads"),
            }
        pair["comparison"] = comparison
        result["cases"][case] = pair
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["status"] = "MEASURED"
    result["disk_after"] = disk(outdir)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "cases": {
            case: {
                "comparison": pair["comparison"],
                "baseline_tree_rss": pair["runs"]["baseline"]["process_tree"]["tree_peak_rss_bytes"],
                "candidate_tree_rss": pair["runs"]["candidate"]["process_tree"]["tree_peak_rss_bytes"],
                "baseline_returncode": pair["runs"]["baseline"]["returncode"],
                "candidate_returncode": pair["runs"]["candidate"]["returncode"],
            }
            for case, pair in result["cases"].items()
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
