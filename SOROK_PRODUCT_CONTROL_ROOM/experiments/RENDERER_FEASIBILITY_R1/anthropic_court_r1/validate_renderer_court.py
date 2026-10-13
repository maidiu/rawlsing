#!/usr/bin/env python3
"""RFA-06A entirely offline gate. No key required, no Anthropic import/call."""
from __future__ import annotations

import argparse
from collections import Counter

from court_common import (
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
    print("NARROW_UNCHANGED = PASS")
    print("EVALUATOR_ORACLE_NOT_TRANSMITTED = PASS")
    print("USER_PHENOMENAL_STATE_NOT_TRANSMITTED = PASS")
    print("CONDITION_MAPPING_SEPARATED = PASS")
    print("60_PRIMARY_RUN_IDENTITIES = PASS")
    print("API_KEY_NOT_SERIALIZED = PASS")
    responses = [read(p) for p in files]
    model_outputs = sum(r.get("raw_provider_response") is not None for r in responses)
    print(f"MODEL_OUTPUTS_PRESENT = {model_outputs}")
    require(not args.expect_empty or model_outputs == 0, "OUTPUTS_PRESENT_BEFORE_FIRST_COURT")
    if args.require_complete:
        from run_anthropic_renderer_court import latest_terminal, is_terminal
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
        expected = {f"RUN-{i:04d}.json" for i in range(1, 61)}
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
    print("OFFLINE_RENDERER_COURT_VALIDATION = PASS")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        raise SystemExit("OFFLINE_VALIDATION_HOLD: " + str(exc))
