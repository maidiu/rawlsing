#!/usr/bin/env python3
"""Authority-37 hostile fracture-map acceptance adapter (prep-only).

This module is deliberately production-independent. It sanitizes the frozen G04
source fixture into an answer-free controller seed, optionally invokes a future
HQ-supplied production adapter, and compares the adapter's canonical projection
against the frozen G04 oracle. With no production adapter supplied it fails
closed by design.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

G04_COMMIT = "8620265b95f5b3bf8c210674a7735e0ce8dac88c"
FIXTURE_SHA256 = "83c496c9482c2e9736a6797e243965110899c1aa97436d752795b15d483a8215"
FIXTURE_LOGICAL_DIGEST = "e4ef71ccf3815b0734013a5ebf1c85f9f3ac94720b30f2c5cf6285aa784a0017"

# Keys that express answers/derived conclusions rather than lawful seed authority.
FORBIDDEN_SEED_KEY_FRAGMENTS = (
    "expected", "oracle", "modal_pattern", "modal_response", "winner",
    "winning_predictor", "primary_predictor", "branch_membership", "branch_id",
    "secondary_predictor", "grandchild", "cotravel_target", "cosignature_target",
    "stable_minority", "underpowered_branch", "valid_empty_branch",
    "determinicity_result", "selective_invalidation_result",
)
FORBIDDEN_SOURCE_COLUMNS = {"segment"}  # G04's derived/oracle branch label.

REQUIRED_FIXTURE_COLUMNS = {
    "respondent_id", "replay_key", "eligible", "response_state",
    "response_pattern", "P", "Q", "R", "S", "U", "C1", "C2",
    "FOLLOWUP", "XOR_A", "XOR_B", "XOR_C", "weight", "segment",
}

CANONICAL_ORACLE_FILES = {
    "fracture_map": "EXPECTED_FRACTURE_MAP.json",
    "cosignatures": "EXPECTED_COSIGNATURES.json",
    "branch_determinicity": "EXPECTED_BRANCH_DETERMINICITY.csv",
}

def _walk_keys(value: Any, prefix: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{prefix}.{key}" if prefix else str(key)
            yield here, str(key)
            yield from _walk_keys(child, here)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from _walk_keys(child, f"{prefix}[{i}]")

def assert_seed_no_answer_leakage(seed: dict[str, Any]) -> None:
    for path, key in _walk_keys(seed):
        lowered = key.lower()
        for fragment in FORBIDDEN_SEED_KEY_FRAGMENTS:
            if fragment in lowered:
                raise ValueError(f"answer leakage: forbidden seed key {path!r}")
    rows = seed.get("respondents")
    if not isinstance(rows, list) or not rows:
        raise ValueError("seed respondents missing")
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"respondent {i} is not an object")
        leaked = FORBIDDEN_SOURCE_COLUMNS.intersection(row)
        if leaked:
            raise ValueError(f"answer leakage: derived source column(s) {sorted(leaked)} remain")

def build_seed(fixture_csv: Path) -> dict[str, Any]:
    raw = fixture_csv.read_bytes()
    import hashlib
    digest = hashlib.sha256(raw).hexdigest()
    if digest != FIXTURE_SHA256:
        raise ValueError(f"fixture SHA-256 mismatch: {digest}")
    text = raw.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    if set(reader.fieldnames or ()) != REQUIRED_FIXTURE_COLUMNS:
        raise ValueError("fixture column contract mismatch")
    rows = []
    for source_row in reader:
        row = {k: v for k, v in source_row.items() if k not in FORBIDDEN_SOURCE_COLUMNS}
        rows.append(row)
    if len(rows) != 52:
        raise ValueError(f"expected 52 source rows, got {len(rows)}")

    # This is authority, not an answer key. All governed source coordinates and
    # response fields are exposed uniformly; none is identified as a winner,
    # branch role, secondary splitter, grandchild route, or cotravel target.
    seed = {
        "seed_schema": "AUTH37_G04_CONTROLLER_SEED_R1",
        "source_authority": {
            "g04_commit": G04_COMMIT,
            "fixture_path": (
                "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
                "R1_20260825/ORIGINARY_FRACTURE_MAP_COURT_R1/G04_HOSTILE_ORACLE/"
                "SYNTHETIC_RESPONDENTS.csv"
            ),
            "fixture_sha256": FIXTURE_SHA256,
            "fixture_logical_digest": FIXTURE_LOGICAL_DIGEST,
            "governed_coordinate_fields": ["P", "Q", "R", "S", "U"],
            "available_response_fields": [
                "response_pattern", "C1", "C2", "FOLLOWUP", "XOR_A", "XOR_B", "XOR_C"
            ],
            "typed_state_field": "response_state",
            "weight_field": "weight",
            "replay_key_field": "replay_key",
            "eligibility_field": "eligible",
        },
        "root_response_surface": {
            "question_id": "TARGET_MULTISELECT",
            "response_field": "response_pattern",
            "state_field": "response_state",
        },
        "controller_policy": {
            "policy_id": "AUTH37_G04_HOSTILE_ACCEPTANCE_POLICY_R1",
            "minimum_split_raw_n": 3,
            "maximum_depth": 4,
            "maximum_target_arity_J": 3,
            "enumerate_all_governed_response_patterns": True,
            "enumerate_all_governed_positional_conditions": True,
            "retain_stopped_supported_and_residual_branches": True,
            "exclude_typed_nonpositive_states_from_boolean_complements": True,
            "current_invocation_frontier_nonadaptive": True,
        },
        "respondents": rows,
    }
    assert_seed_no_answer_leakage(seed)
    return seed

def _load_expected(oracle_dir: Path) -> dict[str, Any]:
    fracture = json.loads((oracle_dir / CANONICAL_ORACLE_FILES["fracture_map"]).read_text())
    cosig = json.loads((oracle_dir / CANONICAL_ORACLE_FILES["cosignatures"]).read_text())
    with (oracle_dir / CANONICAL_ORACLE_FILES["branch_determinicity"]).open(
        newline="", encoding="utf-8"
    ) as f:
        det = list(csv.DictReader(f))
    return {
        "actual_schema": "I05_HOSTILE_ACCEPTANCE_ACTUAL_R1",
        "fracture_map": fracture,
        "cosignatures": cosig,
        "branch_determinicity": det,
    }

def compare_actual_to_oracle(actual: dict[str, Any], oracle_dir: Path) -> list[str]:
    expected = _load_expected(oracle_dir)
    failures: list[str] = []
    if actual.get("actual_schema") != expected["actual_schema"]:
        failures.append("actual_schema")
    if actual.get("fracture_map") != expected["fracture_map"]:
        failures.append("fracture_map")
    if actual.get("cosignatures") != expected["cosignatures"]:
        failures.append("cosignatures")
    if actual.get("branch_determinicity") != expected["branch_determinicity"]:
        failures.append("branch_determinicity")
    return failures

def invoke_future_adapter(command: str, seed: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="i05-hostile-") as td:
        td_path = Path(td)
        seed_path = td_path / "seed.json"
        out_path = td_path / "actual.json"
        seed_path.write_text(json.dumps(seed, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        argv = shlex.split(command) + [
            "--seed-json", str(seed_path),
            "--output-json", str(out_path),
        ]
        completed = subprocess.run(argv, text=True, capture_output=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"future production adapter failed rc={completed.returncode}: "
                f"{completed.stderr.strip()}"
            )
        if not out_path.exists():
            raise RuntimeError("future production adapter did not emit --output-json")
        return json.loads(out_path.read_text(encoding="utf-8"))

def self_test() -> None:
    clean = {
        "source_authority": {"governed_coordinate_fields": ["P", "Q", "R", "S", "U"]},
        "root_response_surface": {"question_id": "TARGET_MULTISELECT"},
        "controller_policy": {"minimum_split_raw_n": 3},
        "respondents": [{"respondent_id": "X", "response_pattern": "A+B", "P": "1"}],
    }
    assert_seed_no_answer_leakage(clean)

    leaked = json.loads(json.dumps(clean))
    leaked["expected_modal_pattern"] = "A+B"
    try:
        assert_seed_no_answer_leakage(leaked)
    except ValueError:
        pass
    else:
        raise AssertionError("expected-answer key leakage was not detected")

    leaked_segment = json.loads(json.dumps(clean))
    leaked_segment["respondents"][0]["segment"] = "P_MODAL_CONFORMER"
    try:
        assert_seed_no_answer_leakage(leaked_segment)
    except ValueError:
        pass
    else:
        raise AssertionError("derived segment leakage was not detected")

    print("SELF_TEST_PASS")
    print("MISSING_INTEGRATION_DISPOSITION=FAIL_CLOSED__PRODUCTION_CONTROLLER_ADAPTER_ABSENT")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--fixture-csv", type=Path)
    parser.add_argument("--oracle-dir", type=Path)
    parser.add_argument("--production-adapter-command")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    if args.fixture_csv is None or args.oracle_dir is None:
        parser.error("--fixture-csv and --oracle-dir are required outside --self-test")

    seed = build_seed(args.fixture_csv)

    if not args.production_adapter_command:
        print("FAIL_CLOSED__PRODUCTION_CONTROLLER_ADAPTER_ABSENT")
        return 42

    actual = invoke_future_adapter(args.production_adapter_command, seed)
    failures = compare_actual_to_oracle(actual, args.oracle_dir)
    if failures:
        print("FAIL__HOSTILE_ACCEPTANCE_MISMATCH=" + ",".join(failures))
        return 1

    print("PASS__AUTH37_G04_HOSTILE_ACCEPTANCE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
