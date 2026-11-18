#!/usr/bin/env python3
"""Offline oracle check for the 10k/5-role F2 forward/reverse operations.

This script performs no query, build, fixture construction or product import.
It only reads the pinned oracle and a forthcoming matched-output JSON file.

Input contract
--------------
The matched output may be the candidate JSON emitted by the existing matched
runner: a top-level ``operations`` list (or mapping) whose entries have
``label``, ``risk_set_member_refs``, ``denominator_member_refs``, ``cells``,
``fact_ref``, ``payload``/``payload_sha256``, ``provenance_refs``,
``replay_ref``, ``query_ref``, ``predicate_ref``, ``raw_numerator`` and
``raw_denominator``.  Top-level ``estate_manifest`` is checked when present.

Exit status: 0 PASS; 2 MISMATCH/ORDER_MISMATCH; 3 MISSING_PRIOR_EVIDENCE or
MISSING_OUTPUT_FIELD.  Missing output fields are deliberately distinct from a
value mismatch and from missing prior evidence.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_PINS = HERE / "ORACLE_PINS.json.gz"
ALIASES = {
    "f2_forward_raw": ("f2_forward_raw", "f2_forward"),
    "f2_reverse_raw": ("f2_reverse_raw", "f2_reverse"),
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def load_pins(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if path.suffix == ".gz":
        raw = gzip.decompress(raw)
    data = json.loads(raw)
    if data.get("schema") != "ANVIL_ROUTING_10K_F2_ORACLE_PINS@1":
        raise ValueError("unexpected oracle pin schema")
    return data


def ref_key(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        raise ValueError("member ref is neither string nor mapping")
    if all(k in value for k in ("kind", "object_id", "content_hash")):
        return f"{value['kind']}|{value['object_id']}|{value['content_hash']}"
    if all(k in value for k in ("object_id", "content_hash")):
        return f"{value['object_id']}|{value['content_hash']}"
    raise ValueError("member ref lacks exact identity fields")


def normalize_refs(values: Any) -> list[str]:
    if not isinstance(values, list):
        raise ValueError("member refs must be a list")
    return [ref_key(value) for value in values]


def operation_map(payload: Any) -> dict[str, dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("operations"), list):
        entries = payload["operations"]
    elif isinstance(payload, dict) and isinstance(payload.get("operations"), dict):
        entries = [
            dict(value, label=value.get("label", key))
            for key, value in payload["operations"].items()
        ]
    elif isinstance(payload, list):
        entries = payload
    elif isinstance(payload, dict):
        entries = [
            dict(value, label=value.get("label", key))
            for key, value in payload.items()
            if isinstance(value, dict)
        ]
    else:
        raise ValueError("output has no operation entries")
    result = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        label = entry.get("label") or entry.get("operation")
        if label:
            result[str(label)] = entry
    return result


def find_operation(operations: dict[str, dict[str, Any]], label: str):
    for alias in ALIASES[label]:
        if alias in operations:
            return operations[alias]
    return None


def check_cells(actual: Any, expected: list[dict[str, Any]]) -> tuple[str | None, list[str]]:
    if not isinstance(actual, list):
        return "MISSING_OUTPUT_FIELD", ["cells"]
    expected_by_cell = {str(item["cell"]): item for item in expected}
    actual_by_cell = {}
    for item in actual:
        if not isinstance(item, dict) or "cell" not in item:
            return "MISMATCH", ["cells: malformed entry"]
        actual_by_cell[str(item["cell"])] = item
    if set(actual_by_cell) != set(expected_by_cell):
        return "MISMATCH", [
            f"cells: expected {sorted(expected_by_cell)} actual {sorted(actual_by_cell)}"
        ]
    problems = []
    for cell, expected_cell in expected_by_cell.items():
        actual_cell = actual_by_cell[cell]
        for field in ("cell_state", "raw_numerator_support"):
            if field not in actual_cell:
                return "MISSING_OUTPUT_FIELD", [f"cells[{cell}].{field}"]
            if actual_cell[field] != expected_cell[field]:
                problems.append(
                    f"cells[{cell}].{field}: expected {expected_cell[field]!r} "
                    f"actual {actual_cell[field]!r}"
                )
    return ("MISMATCH", problems) if problems else (None, [])


def check_refs(
    actual: Any, expected_order: list[str], expected_set_sha: str,
    expected_count: int, name: str,
) -> tuple[str | None, list[str]]:
    if not isinstance(actual, list):
        return "MISSING_OUTPUT_FIELD", [name]
    try:
        actual_refs = normalize_refs(actual)
    except ValueError as exc:
        return "MISMATCH", [f"{name}: {exc}"]
    if len(actual_refs) != expected_count:
        return "MISMATCH", [
            f"{name}: count expected {expected_count} actual {len(actual_refs)}"
        ]
    actual_set_sha = sha_bytes(canonical_json(sorted(set(actual_refs))))
    if actual_set_sha != expected_set_sha:
        missing = len(set(expected_order) - set(actual_refs))
        extra = len(set(actual_refs) - set(expected_order))
        return "MISMATCH", [
            f"{name}: set digest expected {expected_set_sha} actual {actual_set_sha}; "
            f"missing {missing} extra {extra}"
        ]
    if actual_refs != expected_order:
        return "ORDER_MISMATCH", [
            f"{name}: set is exact but ordered refs differ from pinned pin"
        ]
    return None, []


def compare_operation(
    label: str, pin: dict[str, Any], actual: dict[str, Any],
) -> dict[str, Any]:
    statuses: list[str] = []
    details: list[str] = []

    def add(status: str | None, problems: list[str]) -> None:
        if status:
            statuses.append(status)
            details.extend(problems)

    # Ordered refs and expected set identity.
    for field, key in (
        ("risk_set_member_refs", "risk"),
        ("denominator_member_refs", "denominator"),
    ):
        spec = pin[key]
        add(*check_refs(actual.get(field), spec["ordered_refs"],
                        spec["expected_set_sha256"], spec["expected_count"], field))

    add(*check_cells(actual.get("cells"), pin["expected_cells"]))

    # Fact and replay identity.
    for field in ("fact_ref", "query_ref", "predicate_ref", "replay_ref"):
        expected = pin["fact"].get(field)
        if expected is None:
            continue
        if field not in actual:
            add("MISSING_OUTPUT_FIELD", [field])
        elif actual[field] != expected:
            add("MISMATCH", [f"{field}: expected {expected!r} actual {actual[field]!r}"])

    if "typed_state" in actual and actual["typed_state"] != pin["fact"]["typed_state"]:
        add("MISMATCH", [
            f"typed_state: expected {pin['fact']['typed_state']!r} "
            f"actual {actual['typed_state']!r}"
        ])

    # Full fact canonical bytes.
    expected_fact_sha = pin["fact"]["fact_canonical_sha256"]
    actual_payload_sha = actual.get("payload_sha256")
    if actual.get("payload") is not None:
        computed = sha_bytes(canonical_json(actual["payload"]))
        if computed != expected_fact_sha:
            add("MISMATCH", [f"payload canonical sha256 expected {expected_fact_sha} actual {computed}"])
        if actual_payload_sha is not None and actual_payload_sha != computed:
            add("MISMATCH", ["payload_sha256 disagrees with supplied payload"])
    elif actual_payload_sha is None:
        add("MISSING_OUTPUT_FIELD", ["payload/payload_sha256"])
    elif actual_payload_sha != expected_fact_sha:
        add("MISMATCH", [
            f"payload_sha256 expected {expected_fact_sha} actual {actual_payload_sha}"
        ])

    # Raw support.
    expected_raw = pin["expected_raw"]
    for actual_field, pin_field in (
        ("raw_numerator", "raw_numerator_support"),
        ("raw_denominator", "raw_denominator_support"),
    ):
        if actual_field not in actual:
            add("MISSING_OUTPUT_FIELD", [actual_field])
        elif actual[actual_field] != expected_raw[pin_field]:
            add("MISMATCH", [
                f"{actual_field}: expected {expected_raw[pin_field]!r} "
                f"actual {actual[actual_field]!r}"
            ])

    # Provenance exact order/digest.
    actual_prov = actual.get("provenance_refs")
    if not isinstance(actual_prov, list):
        add("MISSING_OUTPUT_FIELD", ["provenance_refs"])
    else:
        try:
            actual_prov = normalize_refs(actual_prov)
        except ValueError as exc:
            add("MISMATCH", [f"provenance_refs: {exc}"])
        else:
            prov_sha = sha_bytes(canonical_json(actual_prov))
            if len(actual_prov) != pin["fact"]["provenance_count"]:
                add("MISMATCH", [
                    f"provenance count expected {pin['fact']['provenance_count']} "
                    f"actual {len(actual_prov)}"
                ])
            if prov_sha != pin["fact"]["provenance_sha256"]:
                add("MISMATCH", [
                    f"provenance sha256 expected {pin['fact']['provenance_sha256']} "
                    f"actual {prov_sha}"
                ])

    if "MISMATCH" in statuses:
        status = "MISMATCH"
    elif "ORDER_MISMATCH" in statuses:
        status = "ORDER_MISMATCH"
    elif "MISSING_OUTPUT_FIELD" in statuses:
        status = "MISSING_OUTPUT_FIELD"
    else:
        status = "PASS"
    return {"label": label, "status": status, "details": details}


def verify_sources(pins: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    results = []
    for name, source in pins.get("sources", {}).items():
        path = root / source["path"]
        if not path.exists():
            results.append({"source": name, "status": "MISSING_PRIOR_EVIDENCE",
                            "path": source["path"], "detail": "file absent"})
            continue
        actual = sha_bytes(path.read_bytes())
        if actual != source["sha256"]:
            results.append({"source": name, "status": "MISSING_PRIOR_EVIDENCE",
                            "path": source["path"],
                            "detail": f"hash mismatch expected {source['sha256']} actual {actual}"})
        else:
            results.append({"source": name, "status": "PASS",
                            "path": source["path"], "sha256": actual})
    return results


def self_test(pins: dict[str, Any], root: Path, verify: bool) -> int:
    problems = []
    for label, op in pins["operations"].items():
        order = op["risk"]["ordered_refs"]
        if sha_bytes(canonical_json(order)) != op["risk"]["order_sha256"]:
            problems.append(f"{label}: risk order digest")
        order = op["denominator"]["ordered_refs"]
        if sha_bytes(canonical_json(order)) != op["denominator"]["order_sha256"]:
            problems.append(f"{label}: denominator order digest")
        if op["risk"]["actual_set_sha256"] != op["risk"]["expected_set_sha256"]:
            problems.append(f"{label}: risk set differs from accepted expected set")
        if op["denominator"]["actual_set_sha256"] != op["denominator"]["expected_set_sha256"]:
            problems.append(f"{label}: denominator set differs from accepted expected set")
        if op["risk"]["count"] != op["risk"]["expected_count"]:
            problems.append(f"{label}: risk count")
        if op["denominator"]["count"] != op["denominator"]["expected_count"]:
            problems.append(f"{label}: denominator count")
    if verify:
        for item in verify_sources(pins, root):
            if item["status"] != "PASS":
                problems.append(f"{item['source']}: {item['detail']}")
    out = {"status": "SELFTEST_PASS" if not problems else "SELFTEST_FAIL",
           "problems": problems}
    if verify:
        out["source_checks"] = verify_sources(pins, root)
    print(json.dumps(out, indent=2))
    return 0 if not problems else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", type=Path, default=DEFAULT_PINS)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--root", type=Path,
                        default=Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117"),
                        help="repository root for pinned source paths")
    parser.add_argument("--verify-sources", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    try:
        pins = load_pins(args.pins)
    except Exception as exc:
        print(json.dumps({"status": "MISSING_PRIOR_EVIDENCE",
                          "detail": f"cannot load oracle pins: {exc}"}, indent=2))
        return 3
    if args.self_test:
        return self_test(pins, args.root, args.verify_sources)
    if args.input is None:
        parser.error("--input is required unless --self-test is used")
    try:
        payload = json.loads(args.input.read_text())
    except Exception as exc:
        out = {"status": "MISSING_OUTPUT_FIELD",
               "detail": f"cannot parse matched output: {exc}"}
        print(json.dumps(out, indent=2))
        return 3

    source_checks = verify_sources(pins, args.root) if args.verify_sources else []
    if any(item["status"] != "PASS" for item in source_checks):
        out = {"status": "MISSING_PRIOR_EVIDENCE",
               "source_checks": source_checks}
        print(json.dumps(out, indent=2))
        return 3

    try:
        operations = operation_map(payload)
    except Exception as exc:
        out = {"status": "MISSING_OUTPUT_FIELD", "detail": str(exc)}
        print(json.dumps(out, indent=2))
        return 3

    results = []
    fixture_checks = []
    expected_manifest = pins["fixture_identity"]["manifest_sha256"]
    actual_manifest = payload.get("estate_manifest") if isinstance(payload, dict) else None
    if actual_manifest is None:
        fixture_checks.append({"check": "estate_manifest",
                               "status": "MISSING_OUTPUT_FIELD"})
    elif actual_manifest != expected_manifest:
        fixture_checks.append({"check": "estate_manifest", "status": "MISMATCH",
                               "expected": expected_manifest,
                               "actual": actual_manifest})
    else:
        fixture_checks.append({"check": "estate_manifest", "status": "PASS"})

    for label, pin in pins["operations"].items():
        actual = find_operation(operations, label)
        if actual is None:
            results.append({"label": label, "status": "MISSING_OUTPUT_FIELD",
                            "details": ["operation label absent"]})
        else:
            results.append(compare_operation(label, pin, actual))

    statuses = {item["status"] for item in results} | {
        item["status"] for item in fixture_checks
    }
    if "MISMATCH" in statuses:
        status = "MISMATCH"
        code = 2
    elif "ORDER_MISMATCH" in statuses:
        status = "ORDER_MISMATCH"
        code = 2
    elif "MISSING_PRIOR_EVIDENCE" in statuses:
        status = "MISSING_PRIOR_EVIDENCE"
        code = 3
    elif "MISSING_OUTPUT_FIELD" in statuses:
        status = "MISSING_OUTPUT_FIELD"
        code = 3
    else:
        status = "PASS"
        code = 0
    out = {
        "schema": "ANVIL_ROUTING_10K_F2_ORACLE_CHECK@1",
        "status": status,
        "fixture_identity": pins["fixture_identity"],
        "fixture_checks": fixture_checks,
        "operation_checks": results,
        "source_checks": source_checks,
    }
    if args.json_out:
        args.json_out.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
