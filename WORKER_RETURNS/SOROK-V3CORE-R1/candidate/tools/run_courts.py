#!/usr/bin/env python3
"""Execute the V3CORE-R1 source, adapter and mutation courts."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
PYTHONPATH = f"{ROOT}:{ROOT / 'vendor'}:{ROOT / 'vendor' / 'py3deps'}"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _run(name: str, command: list[str], *, cwd: Path = ROOT, env: dict | None = None, expect: int = 0) -> dict:
    environment = dict(os.environ)
    environment.update(env or {})
    started = time.time()
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
    )
    duration = round(time.time() - started, 3)
    (EVIDENCE / f"{name}.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (EVIDENCE / f"{name}.stderr.txt").write_text(result.stderr, encoding="utf-8")
    summary = ""
    for line in result.stdout.splitlines():
        if " passed" in line or " failed" in line or " error" in line:
            summary = line.strip()
    record = {
        "name": name,
        "command": command,
        "cwd": str(cwd),
        "env_overrides": {k: v for k, v in (env or {}).items()},
        "exit_code": result.returncode,
        "expected_exit_code": expect,
        "passed_expectation": result.returncode == expect,
        "duration_seconds": duration,
        "summary": summary,
        "stdout_sha256": _sha256(result.stdout.encode()),
        "stderr_sha256": _sha256(result.stderr.encode()),
    }
    if result.returncode != expect:
        record["failure_tail"] = (result.stdout + result.stderr)[-2000:]
    return record


def _mutated_order_court(tmp: Path) -> dict:
    target = tmp / "mutated-order"
    shutil.copytree(ROOT / "vendor" / "v3", target / "v3")
    sys.path.insert(0, str(ROOT / "vendor" / "py3deps"))
    import yaml

    order_path = target / "v3" / "v3_yearly_step_order.yaml"
    order = yaml.safe_load(order_path.read_text())
    render = next(step for step in order["steps"] if step["id"] == "render_layer")
    order["steps"].remove(render)
    order["steps"].insert(0, render)
    order_path.write_text(yaml.safe_dump(order, sort_keys=False))
    env = {"PYTHONPATH": f"{target}:{ROOT / 'vendor' / 'py3deps'}", "PYTHONDONTWRITEBYTECODE": "1"}
    return _run(
        "mutated_19_step_order",
        [
            sys.executable,
            "-m",
            "pytest",
            "-o",
            "addopts=",
            "-q",
            "-p",
            "no:cacheprovider",
            "v3/tests/test_architecture_invariants.py::test_step_order_immutable",
        ],
        cwd=target,
        env=env,
        expect=1,
    )


def main() -> int:
    env = {"PYTHONPATH": PYTHONPATH, "PYTHONDONTWRITEBYTECODE": "1"}
    courts = []
    courts.append(
        _run(
            "unchanged_v3_source_tests",
            [
                sys.executable,
                "-m",
                "pytest",
                "-o",
                "addopts=",
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml",
                str(EVIDENCE / "unchanged_v3_source_junit.xml"),
                "vendor/v3/tests/test_architecture_invariants.py",
                "vendor/v3/tests/test_step_logic.py",
                "vendor/v3/tests/test_v5_pressure_flow.py",
                "vendor/v3/tests/test_v5_pressureflow_golden_run.py",
            ],
            env=env,
        )
    )
    courts.append(
        _run(
            "v3core_adapter_tests",
            [
                sys.executable,
                "-m",
                "pytest",
                "-o",
                "addopts=",
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml",
                str(EVIDENCE / "v3core_adapter_junit.xml"),
                "tests",
            ],
            env=env,
        )
    )
    courts.append(
        _run(
            "i1_unchanged_consumer_tests",
            [
                sys.executable,
                "-m",
                "pytest",
                "-o",
                "addopts=",
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml",
                str(EVIDENCE / "i1_unchanged_junit.xml"),
                "tests/test_i1_guarded_consumer.py",
            ],
            cwd=ROOT / "vendor" / "i1",
            env={"PYTHONPATH": str(ROOT / "vendor" / "i1"), "PYTHONDONTWRITEBYTECODE": "1"},
        )
    )
    with tempfile.TemporaryDirectory(prefix="v3core-order-") as directory:
        courts.append(_mutated_order_court(Path(directory)))
    payload = {
        "schema": "SOROK_V3CORE_R1_COURT_RESULTS@1",
        "root": str(ROOT),
        "python": sys.version,
        "platform": sys.platform,
        "courts": courts,
        "all_expected": all(court["passed_expectation"] for court in courts),
    }
    (EVIDENCE / "court_results.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["all_expected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
