#!/usr/bin/env python3
"""One-shot Claude actor feasibility court. All API generation requires explicit local execution.

No requests occur on import. --preflight and --export-blinded never call the provider.
The commission does not execute this file against Anthropic.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from court_common import (
    HERE, RAW, BLINDED, RECEIPTS, FREEZE, IDS, atomic_new_json,
    assert_freeze, canonical, deterministic_candidate, evidence_files,
    file_sha256, freeze_inputs, read, request_for, require, sdk_version, sha256,
    utcnow, verify_static,
)


def existing_attempts(run_id):
    return sorted(RAW.glob(run_id + "-A????.json"))


def next_attempt(run_id):
    attempts = existing_attempts(run_id)
    if attempts:
        highest = max(int(p.stem.rsplit("-A", 1)[1]) for p in attempts)
    else:
        highest = 0
    require(highest < 9999, "ATTEMPT_ID_EXHAUSTED")
    return f"{run_id}-A{highest + 1:04d}"


def is_terminal(record):
    # Any actual model generation, even a refusal, truncation or invalid JSON,
    # is evidence and must never be silently rendered again.
    return record.get("status") in {
        "SCHEMA_VALID", "SCHEMA_INVALID", "JSON_PARSE_INVALID",
        "STRUCTURAL_INVALID", "MODEL_REFUSAL", "MODEL_TRUNCATED",
        "PROVIDER_SCHEMA_FAILURE", "PERMANENT_PROVIDER_FAILURE",
        "NO_TEXT_CANDIDATE",
    }


def latest_terminal(run_id):
    attempts = existing_attempts(run_id)
    for path in reversed(attempts):
        item = read(path)
        if is_terminal(item):
            return item
    return None


def snapshot(run, request_hash, input_hash, packet_name, config, start, latency, attempt_id):
    return {
        "kind": "ANTHROPIC_COURT_RAW_PROVIDER_ATTEMPT",
        "run_id": run["run_id"], "attempt_id": attempt_id,
        "case_id": run["case_id"], "condition": run["condition"],
        "replicate_ordinal": run["replicate"],
        "request_identity_sha256": request_hash,
        "model_payload_sha256": input_hash,
        "input_packet_file": packet_name,
        "input_packet_raw_sha256": file_sha256(HERE.parent / "render_inputs_r1" / packet_name),
        "model": config["model"], "effort": config["effort"],
        "max_tokens": config["max_tokens"],
        "api_endpoint": config["api_endpoint"], "api_version": config["api_version"],
        "sdk_package": "anthropic", "sdk_version": sdk_version(),
        "provider_seed_status": config["provider_seed_status"],
        "started_at_utc": start, "ended_at_utc": utcnow(),
        "latency_seconds": round(latency, 6),
        "provider_message_id": None, "stop_reason": None, "usage": None,
        "raw_provider_response": None, "structured_candidate": None,
        "parse_status": "NO_CANDIDATE", "schema_status": "NOT_APPLICABLE",
        "structural_checks": [], "error_status": None, "status": None,
    }


def persist(record):
    destination = RAW / (record["attempt_id"] + ".json")
    atomic_new_json(destination, record)
    print(f"{record['run_id']} attempt {record['attempt_id']}: {record['status']}")
    return destination


def take_one(client, run, config, transport_schema, original_schema):
    """Only invoked for --smoke or deliberate main execution with freeze verified."""
    import anthropic

    request, request_hash, input_hash, packet_name = request_for(run, config, transport_schema)
    content = request["messages"][0]["content"]
    require(sha256(content.encode("utf-8")) == input_hash, "INPUT_SERIALIZATION_HASH_DRIFT")
    require("audit_metadata_NOT_FOR_MODEL" not in content, "UNSAFE_TRANSMISSION")

    max_operational_retries = config["operational_retries"]
    for try_index in range(max_operational_retries + 1):
        attempt_id = next_attempt(run["run_id"])
        start = utcnow()
        began = time.perf_counter()
        captured = None
        error = None
        try:
            # No system message, no sampling seed, temperature, top_p or top_k.
            captured = client.messages.create(**request)
        except (anthropic.APIConnectionError, anthropic.APITimeoutError) as exc:
            error = {"type": type(exc).__name__, "class": "OPERATIONAL_TRANSIENT_NO_CANDIDATE"}
        except anthropic.APIStatusError as exc:
            status = getattr(exc, "status_code", None)
            kind = ("OPERATIONAL_TRANSIENT_NO_CANDIDATE" if status == 429 or (isinstance(status, int) and 500 <= status <= 599)
                    else "PERMANENT_PROVIDER_FAILURE")
            if status == 400:
                kind = "PROVIDER_SCHEMA_FAILURE"
            error = {"type": type(exc).__name__, "http_status": status, "class": kind}
        except Exception as exc:
            # No message/traceback/headers, because some SDK exception payloads may
            # contain sensitive request details. Unexpected errors are permanent.
            error = {"type": type(exc).__name__, "class": "PERMANENT_PROVIDER_FAILURE"}

        receipt = snapshot(run, request_hash, input_hash, packet_name, config,
                           start, time.perf_counter() - began, attempt_id)
        # Exact semantic input is in this private receipt, never a blinded export.
        receipt["transmitted_user_message"] = content
        receipt["transmitted_user_message_sha256"] = input_hash
        if error:
            receipt["error_status"] = error
            receipt["status"] = error["class"]
            receipt["parse_status"] = "NO_MODEL_CANDIDATE"
            persist(receipt)
            if error["class"] != "OPERATIONAL_TRANSIENT_NO_CANDIDATE":
                return
            if try_index < max_operational_retries:
                backoff = min(30, 2 ** (try_index + 1))
                print(f"Operational transport retry after {backoff}s (no captured candidate).")
                time.sleep(backoff)
                continue
            return

        raw = captured.model_dump(mode="json")
        receipt["raw_provider_response"] = raw
        receipt["provider_message_id"] = raw.get("id")
        receipt["stop_reason"] = raw.get("stop_reason")
        receipt["usage"] = raw.get("usage")
        receipt["provider_returned_model"] = raw.get("model")
        texts = [block.get("text") for block in raw.get("content", [])
                 if block.get("type") == "text" and isinstance(block.get("text"), str)]
        if raw.get("stop_reason") == "refusal":
            receipt["status"] = "MODEL_REFUSAL"
            receipt["parse_status"] = "REFUSAL_EVIDENCE"
        elif raw.get("stop_reason") == "max_tokens":
            receipt["status"] = "MODEL_TRUNCATED"
            receipt["parse_status"] = "MAX_TOKENS_EVIDENCE"
        elif len(texts) != 1:
            receipt["status"] = "NO_TEXT_CANDIDATE"
            receipt["parse_status"] = "TEXT_BLOCK_COUNT_INVALID"
        else:
            receipt["raw_text"] = texts[0]
            try:
                candidate = json.loads(texts[0])
                receipt["structured_candidate"] = candidate
                receipt["parse_status"] = "JSON_PARSED"
                Draft202012Validator(original_schema).validate(candidate)
                receipt["schema_status"] = "EXACT_ORIGINAL_SCHEMA_VALID"
                scene = read(HERE.parent / "render_inputs_r1" / packet_name)["model_payload"]["shared"]["scene"]
                refs = [fact["source_ref"] for fact in scene["facts"]]
                issues = deterministic_candidate(candidate, run["case_id"], refs)
                receipt["structural_checks"] = issues
                receipt["status"] = "STRUCTURAL_INVALID" if issues else "SCHEMA_VALID"
            except json.JSONDecodeError:
                receipt["parse_status"] = "JSON_PARSE_INVALID"
                receipt["schema_status"] = "NOT_CHECKED"
                receipt["status"] = "JSON_PARSE_INVALID"
            except ValidationError as exc:
                receipt["schema_status"] = "EXACT_ORIGINAL_SCHEMA_INVALID"
                receipt["error_status"] = {"type": "LOCAL_SCHEMA_VIOLATION",
                                           "path": list(exc.absolute_path),
                                           "validator": exc.validator}
                receipt["status"] = "SCHEMA_INVALID"
        persist(receipt)
        # Even a bad model output is a terminal observation, never an operational retry.
        return


def export_blinded(runs):
    """Only scorer-visible per-run candidate/status. Never exports arm, prompt or usage."""
    selected = 0
    for run in runs:
        result = latest_terminal(run["run_id"])
        if result is None:
            continue
        candidate = result.get("structured_candidate")
        bundle = {
            "run_id": run["run_id"],
            "candidate_occurrence": candidate,
            "raw_candidate_text": result.get("raw_text"),
            "transport_status": result.get("status"),
            "parse_status": result.get("parse_status"),
            "schema_status": result.get("schema_status"),
            "structural_checks": result.get("structural_checks", []),
        }
        target = BLINDED / (run["run_id"] + ".json")
        if target.exists():
            # No silent overwrite or changing the scoring bundle after a reviewer
            # has seen it; explicit manual review is needed before re-export.
            require(read(target) == bundle, f"BLIND_EXPORT_COLLISION: {target.name}")
        else:
            atomic_new_json(target, bundle)
        selected += 1
    print(f"Blinded export: {selected}/60 opaque runs; condition mapping remains private.")


def freeze(c, packet_hashes, payload_hashes, transport):
    require(not [p for p in evidence_files() if p.name.startswith("RUN-")],
            "PRIMARY_OUTPUTS_EXIST_BEFORE_FREEZE")
    fingerprints = freeze_inputs(c, packet_hashes, payload_hashes, transport)
    item = {"kind": "RFA06A_EXACT_EXPERIMENT_FREEZE", "frozen_at_utc": utcnow(),
            "fingerprints": fingerprints}
    if FREEZE.exists():
        assert_freeze(fingerprints)
        print("Freeze already present and unchanged.")
    else:
        atomic_new_json(FREEZE, item)
        print("Frozen: EXPERIMENT_FREEZE_R1.json (local, never overwrite).")
    return fingerprints


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--preflight", action="store_true", help="Offline preflight; requires key presence, no provider calls")
    group.add_argument("--freeze", action="store_true", help="Write immutable local freeze before provider execution")
    group.add_argument("--smoke", action="store_true", help="ONE billable NON-PRIMARY transport probe")
    group.add_argument("--export-blinded", action="store_true", help="Offline scoring export without condition metadata")
    parser.add_argument("--count-tokens", action="store_true",
                        help="With --preflight only: explicitly contact non-generative provider count-tokens API")
    parser.add_argument("--force-rerun", metavar="RUN-XXXX",
                        help="Explicitly create a new attempt for ONE primary run (never overwrite)")
    args = parser.parse_args()
    require(not args.count_tokens or args.preflight, "--count-tokens requires --preflight")
    require(not args.force_rerun or not (args.preflight or args.freeze or args.smoke or args.export_blinded),
            "--force-rerun applies only to primary execution")
    preflight = args.preflight
    generated = args.smoke or (not args.preflight and not args.freeze and not args.export_blinded)
    c, runs, transport, packet_hashes, payload_hashes, existing = verify_static(
        key_required=preflight or generated or args.count_tokens,
        sdk_required=preflight or generated or args.freeze)
    orig = read(HERE / c["output_schema_path"])
    print(f"Validated: 20 packets, 10 matched pairs, 60 opaque identities; {len(existing)} attempt files.")
    if preflight:
        print(f"SDK: {sdk_version()} | model: {c['model']} | key: PRESENT (not printed)")
        if FREEZE.exists():
            assert_freeze(freeze_inputs(c, packet_hashes, payload_hashes, transport))
            print("Existing freeze verified.")
        print("PREFLIGHT_PASS: zero Messages calls.")
        if args.count_tokens:
            import anthropic
            probe = {"case_id": "RF001", "condition": "N"}
            request, _, _, _ = request_for(probe, c, transport)
            client = anthropic.Anthropic(max_retries=0, timeout=c["timeout_seconds"], default_headers={"anthropic-version": c["api_version"]})
            counted = client.messages.count_tokens(model=request["model"],
                      messages=request["messages"], output_config=request["output_config"])
            print("Non-generative count-tokens request: " + str(counted.input_tokens))
        return
    if args.freeze:
        freeze(c, packet_hashes, payload_hashes, transport)
        return
    if args.export_blinded:
        if any(p.name.startswith("RUN-") for p in existing):
            assert_freeze(freeze_inputs(c, packet_hashes, payload_hashes, transport))
        export_blinded(runs)
        return
    assert_freeze(freeze_inputs(c, packet_hashes, payload_hashes, transport))
    import anthropic
    client = anthropic.Anthropic(max_retries=0, timeout=c["timeout_seconds"],
                                default_headers={"anthropic-version": c["api_version"]})
    if args.smoke:
        smoke = {"run_id": "SMOKE-0001", "case_id": "RF001", "condition": "N", "replicate": 0}
        if latest_terminal(smoke["run_id"]):
            print("SMOKE-0001 already completed; no duplicate probe.")
        else:
            take_one(client, smoke, c, transport, orig)
        print("Smoke output is NEVER part of the 60 primary runs.")
        return
    if args.force_rerun:
        require(args.force_rerun in {r["run_id"] for r in runs}, "UNKNOWN_FORCE_RUN_ID")
        runs = [r for r in runs if r["run_id"] == args.force_rerun]
    for run in runs:
        if latest_terminal(run["run_id"]) and not args.force_rerun:
            print(f"{run['run_id']}: terminal evidence already captured; skipped.")
            continue
        take_one(client, run, c, transport, orig)
    print("Primary execution pass complete. Run --export-blinded then offline validator.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as err:
        # Deliberately avoid SDK exception dumps, request headers and key values.
        print(f"COURT_HOLD: {err}", file=sys.stderr)
        sys.exit(2)
