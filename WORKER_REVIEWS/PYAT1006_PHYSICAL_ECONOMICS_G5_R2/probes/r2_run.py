"""Run one workload child under the independent R2 process-tree monitor."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time

from r2_monitor import MIN_FREE_DISK_BYTES, disk, run_monitored, TreeMonitor  # noqa: F401

REVIEW = Path(__file__).resolve().parents[1]
REPO = REVIEW.parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--timeout", type=float, default=1800)
    parser.add_argument("--watch", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    outdir = Path(args.outdir).absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    watch = Path(args.watch).absolute()
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = str(REVIEW / "data" / "tmp")
    (REVIEW / "data" / "tmp").mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    result = run_monitored(
        command, cwd=REPO, env=env, timeout_seconds=args.timeout, watch=watch,
    )
    result.update({
        "schema": "PYAT1006_R2_MONITORED_RUN@1",
        "label": args.label,
        "command": command,
        "cwd": str(REPO),
        "watch": str(watch),
        "wall_seconds": time.monotonic() - start,
        "disk_after": disk(outdir),
    })
    path = outdir / f"{args.label}.monitored.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "label": args.label,
        "returncode": result["returncode"],
        "timed_out": result["timed_out"],
        "killed_for_cap": result["killed_for_cap"],
        "seconds": result["seconds"],
        "process_tree": result["process_tree"],
        "stdout_tail": result["stdout"][-1000:],
        "stderr_tail": result["stderr"][-1000:],
    }, indent=2, sort_keys=True))
    return 0 if result["returncode"] == 0 and not result["timed_out"] and not result["killed_for_cap"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
