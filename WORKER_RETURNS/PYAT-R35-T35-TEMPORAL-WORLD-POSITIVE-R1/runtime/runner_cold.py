"""Launch two independent cold child processes and compare their products."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
RETURN = RUNTIME.parent
OUT = RETURN / "02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT"
SCRIPT = RUNTIME / "two_epoch_world.py"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    children = []
    for label in ("cold_a", "cold_b"):
        target = OUT / (label + ".json")
        log = OUT / (label + ".log")
        command = [sys.executable, str(SCRIPT), str(target)]
        with log.open("wb") as handle:
            proc = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT,
                                    env=env, cwd=str(RETURN))
            code = proc.wait()
        children.append(dict(
            label=label, pid=proc.pid, exit_code=code,
            sha256=_sha(target) if target.exists() else None,
            bytes=target.stat().st_size if target.exists() else None,
            command=["python3", "runtime/two_epoch_world.py",
                     "02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/" + label + ".json"],
            log=log.name,
        ))
    a, b = (OUT / "cold_a.json"), (OUT / "cold_b.json")
    same = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
    terminals = []
    failed = {}
    for label in ("cold_a", "cold_b"):
        path = OUT / (label + ".json")
        if path.exists():
            data = json.loads(path.read_text())
            terminals.append(data["terminal"])
            failed[label] = data["failed_assertions"]
    replay = dict(
        schema="R35_T35_COLD_CHILD_REPLAY@1",
        execution="two fresh interpreter processes; no shared module state",
        interpreter=dict(executable="python3", version=platform.python_version(),
                         implementation=platform.python_implementation(),
                         hash_seed=env["PYTHONHASHSEED"]),
        children=children,
        byte_identical=same,
        sha256_equal=(children[0]["sha256"] == children[1]["sha256"]),
        terminals=terminals,
        failed_assertions=failed,
        all_children_exit_zero=all(child["exit_code"] == 0 for child in children),
        evidence_note=("The product contains no wall clock, PID or absolute host path; "
                       "byte equality is therefore a full product equality check."),
    )
    (OUT / "cold_replay.json").write_text(json.dumps(replay, sort_keys=True, indent=2) + "\n")
    print(json.dumps(replay, sort_keys=True, indent=2))
    return 0 if (same and replay["all_children_exit_zero"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
