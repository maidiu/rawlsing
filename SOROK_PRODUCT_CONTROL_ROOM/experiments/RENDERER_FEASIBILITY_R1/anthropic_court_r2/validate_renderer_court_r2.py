#!/usr/bin/env python3
"""RFA-06B independent R2 offline integrity gate. No key or Anthropic calls."""
from __future__ import annotations

import argparse
from collections import Counter

from court_common_r2 import (
    RAW, BLINDED, FREEZE, IDS, assert_freeze, evidence_files, freeze_inputs,
    read, require, verify_static,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-empty", action="store_true",
                        help="Pre-execution handoff gate: zero model outputs mandatory")
    parser.add_argument("--require-complete", action="store_true",
                        help="Post-execution: require 60 terminal primary records and 60 blinded exports")
    args = parser.parse_args()
    require(not (args.expect_empty and args.require_complete), "Choose one completion gate")
    c, runs, transport, packet_hashes, payload_hashes, files = verify_static()
    print("20_INPUT_PACKETS_PRESENT = PASS")
    print("10_WP_N_PAIRS_PRESENT = PASS")
    print("PAIR_SHARED_PARITY = PASS")
    print("RFA05B_PAYLOADS_UNCHANGED = PASS")
    print("REQUIRED_FIXTURE_ID_TRANSMITTED = PASS")
    print("PROVIDER_SCHEMA_FIXTURE_CONST_MATCH = PASS")
    print("LOCAL_EXPECTED_FIXTURE_ID_MATCH = PASS")
    print("NO_HIDDEN_REQUIRED_OUTPUT_IDENTITIES = PASS")
    print("EVALUATOR_ORACLE_NOT_TRANSMITTED = PASS")
    print("USER_PHENOMENAL_STATE_NOT_TRANSMITTED = PASS")
    print("CONDITION_MAPPING_SEPARATED = PASS")
    print("60_R2_PRIMARY_RUN_IDENTITIES = PASS")
    print("R1_EVIDENCE_NOT_MIXED_WITH_R2 = PASS")
    print("API_KEY_NOT_SERIALIZED = PASS")
    responses = [read(p) for p in files]
    model_outputs = sum(r.get("raw_provider_response") is not None for r in responses)
    print(f"R2_MODEL_OUTPUTS_PRESENT = {model_outputs}")
    require(not args.expect_empty or (not files and
            not list(BLINDED.glob("*.json")) and model_outputs == 0),
            "R2_EVIDENCE_PRESENT_BEFORE_FIRST_COURT")
    if args.require_complete:
        from run_anthropic_renderer_court_r2 import latest_terminal, is_terminal, require_r2_smoke_pass
        require_r2_smoke_pass()
        require(FREEZE.exists(), "MISSING_FROZEN_EXPERIMENT")
        assert_freeze(freeze_inputs(c, packet_hashes, payload_hashes, transport))
        completed = []
        for run in runs:
            record = latest_terminal(run["run_id"])
            require(record is not None and is_terminal(record),
                    f"UNFINISHED_PRIMARY_RUN: {run['run_id']}")
            completed.append(record)
        require(len(completed) == 60, "WRONG_TERMINAL_PRIMARY_COUNT")
        for record in completed:
            require(record.get("provider_message_id") or
                    record["status"] in {"PROVIDER_SCHEMA_FAILURE", "PERMANENT_PROVIDER_FAILURE"},
                    f"MISSING_PROVIDER_ID: {record['run_id']}")
        expected = {f"R2RUN-{i:04d}.json" for i in range(1, 61)}
        actual = {p.name for p in BLINDED.glob("*.json")}
        require(actual == expected, f"BLINDED_EXPORT_INCOMPLETE: {len(actual)}/60")
        for name in expected:
            result = read(BLINDED / name)
            require(set(result) == {"run_id", "candidate_occurrence", "raw_candidate_text",
                                   "transport_status", "parse_status", "schema_status",
                                   "structural_checks"}, f"BLIND_EXPORT_METADATA_DRIFT: {name}")
            require(result["run_id"] + ".json" == name, f"BLIND_EXPORT_ID_DRIFT: {name}")
        print("60_TERMINAL_PRIMARY_RUNS = PASS")
        print("60_BLINDED_EXPORTS = PASS")
        print("PRIMARY_OUTCOME_DISTRIBUTION = " + str(dict(Counter(r["status"] for r in completed))))
    print("OFFLINE_R2_RENDERER_COURT_VALIDATION = PASS")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        raise SystemExit("OFFLINE_VALIDATION_HOLD: " + str(exc))
