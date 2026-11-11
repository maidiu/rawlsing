#!/usr/bin/env python3
"""Measure the integrated P6/MII sourcefree encounter without provider calls."""

from __future__ import annotations

from argparse import Namespace
import json
import os
from pathlib import Path
import resource
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P3 = ROOT / "WORKER_RETURNS" / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
sys.path.insert(0, str(P6))
sys.path.insert(0, str(P3 / "tests"))
sys.path.insert(0, str(ROOT))

import run_p6  # noqa: E402


def _summary(values):
    values = sorted(values)
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "p50_s": round(statistics.median(values), 6),
        "p95_s": round(values[min(len(values) - 1, int(0.95 * (len(values) - 1)))], 6),
        "max_s": round(max(values), 6),
        "min_s": round(min(values), 6),
    }


def _size(path):
    path = Path(path)
    if not path.exists():
        return 0
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def _rss_mib(kind):
    value = resource.getrusage(kind).ru_maxrss
    return round(value / (1024 * 1024), 3) if sys.platform == "darwin" else round(value / 1024, 3)


def _cli(state, *args, env):
    started = time.perf_counter()
    process = subprocess.run(
        [sys.executable, "-B", str(P6 / "run_p6.py"), "--state", str(state), *args],
        cwd=str(P6), capture_output=True, text=True, timeout=180, env=env,
    )
    elapsed = time.perf_counter() - started
    try:
        payload = json.loads(process.stdout) if process.stdout.strip() else {}
    except ValueError:
        payload = {"parse_error": True, "stdout": process.stdout[:200]}
    return process.returncode, elapsed, payload, process.stderr[:200]


def main():
    base = ROOT / ".mii-test-state" / "measure"
    if base.exists():
        import shutil
        shutil.rmtree(base)
    state = base / "house"
    state.mkdir(parents=True)
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("SOROK_SITUATED_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cold = []
    commands = []
    first = _cli(state, "new", env=env)
    cold.append(first[1])
    commands.append({"command": "new", "exit": first[0], "seconds": first[1],
                     "stderr": first[3]})
    for parts in (("view",), ("view",), ("view",), ("go", "living room"),
                  ("look", "sandals"), ("view",), ("mii-status",),
                  ("mii-enable-learning",), ("look", "photo"), ("mii-export",),
                  ("mii-stop-learning",), ("mii-reset",)):
        command = " ".join(parts)
        result = _cli(state, *parts, env=env)
        cold.append(result[1])
        commands.append({"command": command, "exit": result[0],
                         "seconds": result[1], "stderr": result[3]})
    gallery = base / "gallery"
    gallery.mkdir(parents=True)
    gallery_result = _cli(gallery, "new", "--scene", "gallery", env=env)
    gallery_look = _cli(gallery, "look", "hinge", env=env)

    warm = []
    warm_state = base / "warm"
    for index in range(5):
        started = time.perf_counter()
        run_p6.experience(
            warm_state,
            Namespace(command="new" if index == 0 else "view", request_id=None,
                      scene="house"),
        )
        warm.append(time.perf_counter() - started)
    last_surface = run_p6.experience(
        warm_state, Namespace(command="view", request_id=None, scene="house")
    )
    profile = json.loads((warm_state / "p6_gaze.json").read_text(encoding="utf8"))
    state_size = _size(state)
    profile_size = (state / "p6_gaze.json").stat().st_size if (state / "p6_gaze.json").exists() else 0
    p2_size = _size(state / "actual-p2")
    result = {
        "schema": "SOROK_MII_MEASUREMENT@1",
        "workload": "one sourcefree house; cold separate-process CLI; warm same-process imports",
        "provider_calls": 0,
        "provider_tokens": 0,
        "cold_cli": _summary(cold),
        "warm_import": _summary(warm),
        "commands": commands,
        "cold_replay_failures": sum(1 for row in commands if row["exit"] != 0),
        "features": {
            "exposures": len(profile.get("exposures") or []),
            "available": last_surface.get("available"),
            "offered": last_surface.get("mii_surface", {}).get("optional"),
            "omitted_available": last_surface.get("mii_surface", {}).get("omitted_available"),
            "recognized": sorted(profile.get("recognized") or {}),
            "mode": profile.get("mode"),
        },
        "storage_bytes": {
            "state": state_size,
            "p6_gaze": profile_size,
            "actual_p2": p2_size,
        },
        "peak_rss_mib": {
            "children": _rss_mib(resource.RUSAGE_CHILDREN),
            "self": _rss_mib(resource.RUSAGE_SELF),
        },
        "gallery_fixture": {
            "new_exit": gallery_result[0],
            "new_seconds": round(gallery_result[1], 6),
            "look_exit": gallery_look[0],
            "look_seconds": round(gallery_look[1], 6),
            "identity": gallery_look[2].get("recognized_identity"),
        },
    }
    output = Path(__file__).with_name("measurements.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps(result, indent=2, sort_keys=True))
    import shutil
    shutil.rmtree(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
