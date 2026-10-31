#!/usr/bin/env python3
"""Fail-capability check for the sourcefree candidate court.

Each mutation disables one load-bearing check in a temporary copy.  The named
test must fail on the mutated copy and pass on the untouched candidate.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
CANDIDATE = HERE / "temporal_method_candidate.py"
TEST = HERE / "test_temporal_method_candidate.py"

MUTATIONS = (
    {
        "name": "disable_attestation_binding_check",
        "needle": (
            "    if attestation.left_ref != expected_left or "
            "attestation.right_ref != expected_right:\n"
            "        return None, f\"ATTESTATION_BINDING_MISMATCH:{attestation.surface}\"\n"
        ),
        "replacement": (
            "    if False:\n"
            "        return None, f\"ATTESTATION_BINDING_MISMATCH:{attestation.surface}\"\n"
        ),
        "test": "test_route_attestation_bound_to_wrong_refs_is_refused",
    },
    {
        "name": "accept_nonpositive_authority",
        "needle": (
            "    except Pre553AuthorityError:\n"
            "        return None, \"AUTHORITY_NOT_POSITIVE\"\n"
        ),
        "replacement": (
            "    except Pre553AuthorityError:\n"
            "        pass\n"
        ),
        "test": "test_denied_temporal_evidence_authority_is_insufficient_authority",
    },
)


def _hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_test(test_path: pathlib.Path, test_name: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            f"{test_path}::{test_name}",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def main() -> int:
    original_test = _run_test(TEST, "test_positive_strict_order_delta_and_replay")
    if original_test.returncode != 0:
        print(json.dumps({
            "status": "BASELINE_RED",
            "stdout": original_test.stdout[-2000:],
            "stderr": original_test.stderr[-2000:],
        }, indent=2))
        return 1
    results = []
    failures = 0
    for mutation in MUTATIONS:
        source = CANDIDATE.read_text()
        if mutation["needle"] not in source:
            results.append({
                "name": mutation["name"],
                "status": "MUTATION_NOT_APPLICABLE",
                "test": mutation["test"],
            })
            failures += 1
            continue
        with tempfile.TemporaryDirectory(prefix="pyat-f7-candidate-mutation-") as tmp:
            temp = pathlib.Path(tmp)
            mutated = temp / "temporal_method_candidate.py"
            copied_test = temp / "test_temporal_method_candidate.py"
            mutated.write_text(source.replace(
                mutation["needle"], mutation["replacement"], 1))
            shutil.copyfile(TEST, copied_test)
            red = _run_test(copied_test, mutation["test"])
            green = _run_test(TEST, mutation["test"])
            detected = red.returncode != 0 and green.returncode == 0
            if not detected:
                failures += 1
            results.append({
                "name": mutation["name"],
                "test": mutation["test"],
                "mutated_sha256": _hash(mutated),
                "mutated_exit": red.returncode,
                "restored_exit": green.returncode,
                "status": "RED_ON_MUTATION_GREEN_ON_RESTORE" if detected else "NOT_DETECTED",
            })
    receipt = {
        "schema": "PYAT_F7_P07_CANDIDATE_MUTATION_CHECK@1",
        "candidate_sha256": _hash(CANDIDATE),
        "test_sha256": _hash(TEST),
        "baseline_exit": original_test.returncode,
        "mutations": results,
        "failures": failures,
        "status": "PASS" if failures == 0 else "FAIL",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
