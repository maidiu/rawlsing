"""Private delivery of an already executed Q006 recorded-outcome distribution.

Not a query, scientific issuer, C11 reader or S04 eligible-population product.
Read only the original aggregate receipt and its separately pinned owner and
operation preimages. Both historical driver envelopes are supported; no
respondent-bearing artifact is needed. A prior result does not prove CURRENT.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import re
from typing import Any

Q103 = "ANVIL_Q006_RECORDED_Q103_PRIVATE_RESULT@1"
SRC16 = "ANVIL_Q006_SRC16_RECORDED_PRIVATE_RESULT@1"


class RecordedDeliveryError(ValueError):
    pass


def _require(condition, reason):
    if not condition:
        raise RecordedDeliveryError(reason)


def _key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _ref(value):
    if isinstance(value, str):
        # Q103's existing JSON default=str serializes its frozen replay
        # mapping as the literal repr of a dict. SRC16 uses a plain dict.
        # Decode that one historical representation, not arbitrary Python.
        if value.startswith("{") and len(value) <= 4096:
            value = ast.literal_eval(value)
        else:
            pieces = value.split("|")
            _require(len(pieces) == 3, "EXACT_REF_REQUIRED")
            value = dict(zip(("kind", "object_id", "content_hash"), pieces))
    _require(isinstance(value, dict) and set(value) == {"kind", "object_id", "content_hash"}
             and all(isinstance(x, str) and x for x in value.values())
             and re.fullmatch(r"[0-9a-f]{64}", value["content_hash"]) is not None,
             "EXACT_REF_REQUIRED")
    return value


def _pin(path, expected):
    _require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
             "INDEPENDENT_SHA256_PIN_REQUIRED")
    raw = Path(path).read_bytes()
    _require(sha256(raw).hexdigest() == expected, "PRIVATE_INPUT_HASH_MISMATCH")
    # Reject ambiguous duplicate JSON keys rather than select one silently.
    def object_hook(pairs):
        result = {}
        for k, v in pairs:
            _require(k not in result, "DUPLICATE_JSON_KEY")
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=object_hook)


def _nonnegative(value):
    return type(value) is int and value >= 0


def _state(value):
    return value[0] if isinstance(value, list) and value else value


def _code(value):
    _require(type(value) in (str, int), "RAW_CODE_NOT_SCALAR")
    return str(value)


def _state_cell(code, state):
    if state != "SUBSTANTIVE_RESPONSE":
        return {"typed_response_state": state}
    return int(code) if re.fullmatch(r"-?[0-9]+", code) else code


def deliver_recorded_result(*, result_path, result_sha256, owner_path, owner_sha256,
                            operation_path, operation_sha256):
    """Return a private, exact-pinned *historical* descriptive display.

    The caller on the already authorized private host must obtain the three
    expected digests independently from the controller's accepted run/decision
    evidence. Computing new pins from an untrusted candidate is not receiving.
    No assertion of present permission, new execution or native fact issuance.
    """
    result = _pin(result_path, result_sha256)
    owner = _pin(owner_path, owner_sha256)
    op = _pin(operation_path, operation_sha256)
    schema = result.get("schema")
    _require(schema in (Q103, SRC16), "RECORDED_NATIVE_RESULT_SCHEMA_REQUIRED")
    _require(result.get("owner_decision_sha256") == owner_sha256 ==
             op.get("owner_decision_sha256"), "OWNER_OPERATION_RESULT_MISMATCH")
    _require(owner.get("source_id") == op.get("source_id"), "SOURCE_MISMATCH")
    _require(isinstance(owner.get("source_binding"), dict), "SOURCE_BINDING_REQUIRED")
    binding = owner["source_binding"]
    roots = binding.get("saved_i02", {})
    _require(all(op.get(k + "_root") == roots.get(k) and roots.get(k)
                 for k in ("source", "release", "universe", "replay")),
             "SAVED_ROOT_BINDING_MISMATCH")
    _require(op.get("authorized_operation") in (
        "Q103-OP-RECORDED-RESPONSE-ONLY", "SRC16-RACPRES-RECORDED-RESPONSE-ONLY"),
        "ONLY_EXISTING_RECORDED_OPERATIONS_SUPPORTED")
    expected = ("SRC04", "Q103-OP-RECORDED-RESPONSE-ONLY") if schema == Q103 else (
        "SRC16", "SRC16-RACPRES-RECORDED-RESPONSE-ONLY")
    _require((op.get("source_id"), op.get("authorized_operation")) == expected,
             "RESULT_OPERATION_SCHEMA_MISMATCH")
    owner_domain = owner.get("denominator", {}).get("recorded_raw_codes")
    if owner_domain is None:
        owner_domain = owner.get("recorded_raw_codes")
    codes = tuple(_code(v) for v in op["allowed_raw_codes"])
    _require(bool(codes) and len(set(codes)) == len(codes)
             and tuple(_code(v) for v in owner_domain) == codes, "OWNER_RAW_DOMAIN_MISMATCH")
    states = {str(code): state for code, state in op["interpretation"]}
    _require(len(op["interpretation"]) == len(states) == len(codes)
             and set(states) == set(codes), "OPERATION_INTERPRETATION_DOMAIN_MISMATCH")
    original = owner["interpretation"]
    _require(set(original) == set(codes) and all(
        _state(original[c]) == states[c] for c in codes), "OWNER_STATE_MAP_MISMATCH")
    _require(result.get("positive_counts_accepted") is True and len(result.get("facts", [])) == 1,
             "NO_POSITIVE_NATIVE_RESULT")
    fact = result["facts"][0]
    _require(fact.get("typed_state") == "SUPPORTED", "NATIVE_RESULT_NOT_SUPPORTED")
    n = fact.get("raw_denominator_support")
    _require(type(n) is int and n > 0 and fact.get("raw_numerator_support") == n,
             "RECORDED_DENOMINATOR_MISMATCH")
    missing = result.get("missing")
    _require(isinstance(missing, dict) and set(missing) == {"system_missing", "absent"}
             and all(_nonnegative(x) for x in missing.values()), "MISSING_ABSENT_ACCOUNTING_REQUIRED")
    cells = {}
    for row in fact.get("cells", []):
        _require(isinstance(row, list) and len(row) == 3, "MALFORMED_NATIVE_CELL")
        value, count, state = row
        key = _key(value)
        _require(key not in cells and _nonnegative(count), "DUPLICATE_OR_INVALID_NATIVE_CELL")
        _require(state == ("OBSERVED_POSITIVE" if count else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"),
                 "NATIVE_CELL_STATE_MISMATCH")
        cells[key] = count
    _require(sum(cells.values()) == n, "NATIVE_CELL_DENOMINATOR_NOT_CONSERVED")
    rows = []
    seen = set()
    if schema == SRC16:
        _require(result.get("source_id") == op["source_id"]
                 and result.get("scope_kind") == "OBSERVED_STORED_CODE_FREQUENCIES"
                 and result.get("asked_eligibility") == "HELD_NOT_PROVEN"
                 and result.get("substantive_vote_denominator") is False,
                 "STORED_CODE_SCOPE_NOT_CONSERVED")
        _require(_ref(result["question_ref"]) == _ref(op["question_ref"]), "QUESTION_REF_MISMATCH")
        _require(_ref(result["historical_snapshot_ref"]) == _ref(op["historical_snapshot_ref"]),
                 "HISTORICAL_AUTHORITY_MISMATCH")
        positive = result.get("positive_snapshot_ref")
        _ref(positive)
        stored = result.get("stored_code_bins", [])
        bins = {_code(b["raw_code"]): b for b in stored}
        _require(len(bins) == len(stored) == len(codes) and set(bins) == set(codes),
                 "STORED_CODE_BIN_CENSUS_MISMATCH")
    else:
        bins = {}
        _require(len(result.get("release_refs", [])) == 1
                 and _ref(result["release_refs"][0]) == _ref(roots["release"]),
                 "NATIVE_RELEASE_REF_MISMATCH")
        _ref(result["query_ref"])
        _ref(result["predicate_ref"])
    for code in codes:
        if schema == SRC16:
            b = bins[code]
            cell = _state_cell(code, states[code])
            _require(b["state"] == states[code] and b["cell"] == cell,
                     "STORED_CODE_INTERPRETATION_MISMATCH")
            key = _key(cell)
            _require(key in cells and b["raw_numerator_support"] == cells[key],
                     "STORED_CODE_NATIVE_COUNT_MISMATCH")
        else:
            # Q103's native owner retains every recorded code as a separate
            # raw scalar, including nonanswers. No reinterpretation as votes.
            options = [key for key in cells if _code(json.loads(key)) == code]
            _require(len(options) == 1, "RECORDED_CODE_CELL_MISMATCH")
            key = options[0]
        _require(key not in seen, "COLLAPSED_RECORDED_CODES")
        seen.add(key)
        count = cells[key]
        ratio = Fraction(count, n)
        interpretation = original[code]
        # Preserve owner material exactly; do not infer a missing label.
        rows.append({"raw_code": code, "source_state": states[code],
                     "owner_interpretation": interpretation,
                     "raw_count": count, "recorded_fraction": [ratio.numerator, ratio.denominator]})
    _require(seen == set(cells), "UNACCOUNTED_NATIVE_CELLS")
    result_replay = _ref(fact["replay_ref"])
    return {
        "schema": "PYAT_PRIVATE_RECORDED_RESULT_DISPLAY@1",
        "status": "HISTORICAL_NATIVE_RESULT_DISPLAY__CURRENT_NOT_REVALIDATED",
        "source_id": op["source_id"],
        "question_id": owner["question_id"],
        "question_ref": _ref(op["question_ref"]),
        "questionnaire_sha256": owner.get("questionnaire_sha256"),
        "authorized_operation": op["authorized_operation"],
        "owner_scope": owner["scope"],
        "owner_denominator": owner["denominator"],
        "source_binding": binding,
        "input_sha256": {"result": result_sha256, "owner": owner_sha256, "operation": operation_sha256},
        "native_receipt_schema": schema,
        "native_replay_ref": result_replay,
        "native_query_ref_if_retained": result.get("query_ref"),
        "native_predicate_ref_if_retained": result.get("predicate_ref"),
        "native_release_refs_if_retained": result.get("release_refs"),
        "raw_recorded_denominator": n,
        "missing_outside_denominator": missing,
        "cells": rows,
        "claim_ceiling": ["UNWEIGHTED_RECORDED_OUTCOMES_ONLY", "ASKED_ELIGIBILITY_NOT_ESTABLISHED",
                          "NO_SUBSTANTIVE_VOTE_OR_POPULATION_DENOMINATOR",
                          "NO_CONDITIONING_COTRAVEL_DISCOVERY_OR_ACTOR_INFERENCE",
                          "NO_CURRENT_RIGHTS_OR_NATIVE_FACT_ISSUANCE"],
    }


def markdown(report):
    def escape(x):
        return str(x).replace("|", r"\|").replace("\r", " ").replace("\n", " ")
    lines = [
        "# Recorded survey outcomes — " + escape(report["source_id"]) + " / " + escape(report["question_id"]),
        "", "Historical native I03 result; not a new source execution or current-use authorization.",
        "", "Unweighted recorded-outcome denominator: **" + str(report["raw_recorded_denominator"]) + "**.",
        "", "| Raw code | Owner state | Owner interpretation | Count | Share of recorded outcomes |",
        "|---|---|---|---:|---:|",
    ]
    for row in report["cells"]:
        ratio = Fraction(*row["recorded_fraction"])
        lines.append("| " + " | ".join((escape(row["raw_code"]), escape(row["source_state"]),
                    escape(row["owner_interpretation"]), str(row["raw_count"]),
                    f"{float(ratio * 100):.2f}%")) + " |")
    lines += ["", "Outside denominator: physical system missing = " +
              str(report["missing_outside_denominator"]["system_missing"]) +
              "; absent = " + str(report["missing_outside_denominator"]["absent"]) + ".",
              "", "Asked/eligible coverage, population inference, comparability and vote preference are not established.",
              "No conditions, joint relationships, learned actor state or CURRENT authority were issued.",
              "", "Native replay: " + escape(_key(report["native_replay_ref"])),
              "Input receipt SHA-256: " + report["input_sha256"]["result"], ""]
    return "\n".join(lines)


def _write_private(path, text):
    # Exclusive creation prevents overwriting a prior received product and
    # following a pre-existing symlink. Never write results to stdout.
    fd = os.open(Path(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ("result", "owner", "operation"):
        ap.add_argument("--" + name, type=Path, required=True)
        ap.add_argument("--" + name + "-sha256", required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--markdown-output", type=Path)
    args = ap.parse_args()
    try:
        report = deliver_recorded_result(
            result_path=args.result, result_sha256=args.result_sha256,
            owner_path=args.owner, owner_sha256=args.owner_sha256,
            operation_path=args.operation, operation_sha256=args.operation_sha256)
        _write_private(args.output, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        if args.markdown_output:
            _write_private(args.markdown_output, markdown(report))
    except (RecordedDeliveryError, KeyError, TypeError, ValueError, SyntaxError, OSError) as exc:
        # Input content, paths and counts deliberately never reach stdout.
        print(json.dumps({"status": "REFUSED", "error_type": type(exc).__name__,
                          "reason": str(exc) if isinstance(exc, RecordedDeliveryError) else "INVALID_OR_UNAVAILABLE_PRIVATE_INPUT"}))
        return 1
    print(json.dumps({"status": report["status"],
                      "private_display_sha256": sha256(args.output.read_bytes()).hexdigest(),
                      "counts_emitted": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
