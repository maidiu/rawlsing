"""Bounded reusable pytest court for Rabochii execution.

The court consumes a validated JSON spec and never evals shell supplied by a
worker.  It records the semantic candidate separately from the actual evidence
execution SHA so evidence-tip scaffolding cannot silently become candidate law.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.rabochii_execution_protocol import validate_court_spec

RECEIPT_SCHEMA = "RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _load(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, Mapping):
        raise ValueError("court spec must be a JSON object")
    return value


def run_court(spec_path: Path, receipt_path: Path) -> int:
    spec = _load(spec_path)
    errors = validate_court_spec(spec)
    if errors:
        receipt = {
            "schema_id": RECEIPT_SCHEMA,
            "result": "INVALID_SPEC",
            "errors": list(errors),
        }
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(_canonical_json(receipt) + "\n", encoding="utf-8")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    semantic_candidate = spec.get("semantic_candidate_sha")
    execution_sha = os.environ.get("RABOCHII_EVIDENCE_EXECUTION_SHA")
    pr_merge_sha = os.environ.get("RABOCHII_PR_SYNTHETIC_SHA")
    environment = os.environ.copy()
    for key, value in spec.get("env", {}).items():
        environment[key] = value

    command = [sys.executable, "-m", "pytest", "-q", *spec["tests"]]
    started = time.monotonic()
    completed = subprocess.run(command, env=environment, check=False)
    elapsed = time.monotonic() - started

    normalized_spec = json.loads(_canonical_json(spec))
    receipt = {
        "schema_id": RECEIPT_SCHEMA,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
        "exit_code": completed.returncode,
        "spec_sha256": hashlib.sha256(
            _canonical_json(normalized_spec).encode("utf-8")
        ).hexdigest(),
        "semantic_candidate_sha": semantic_candidate,
        "evidence_execution_sha": execution_sha,
        "pr_synthetic_merge_sha": pr_merge_sha,
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "determinism_mode": spec.get("determinism_mode", "EXACT"),
        "tests": list(spec["tests"]),
        "env": dict(spec.get("env", {})),
        "elapsed_seconds": round(elapsed, 6),
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(_canonical_json(receipt) + "\n", encoding="utf-8")
    return completed.returncode


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument(
        "--receipt",
        type=Path,
        default=Path(".rabochii/court_receipt.json"),
    )
    args = parser.parse_args(argv)
    return run_court(args.spec, args.receipt)


if __name__ == "__main__":
    raise SystemExit(main())
