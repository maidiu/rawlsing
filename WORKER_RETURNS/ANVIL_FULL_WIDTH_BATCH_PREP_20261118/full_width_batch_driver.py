#!/usr/bin/env python3
"""Actual prepared Batch driver for the sealed combined 10k x 600 fixture.

This is a receiving template, not a benchmark.  It imports the accepted
PreparedSavedC11Admission/execute_saved_batch path from one read-only code
snapshot and runs one actual Batch context containing exactly the distinct
forward and reverse F2 QUERY operations.

It does not invent a Batch payload, re-run a baseline, build a fixture, touch
raw source, or substitute a fake runner.  Batch receipts carry result refs and
operation receipts only; full fact/semantic payloads are deliberately reported
as not carried by Batch.  A qualified baseline file is optional and is used
only for exact fact-ref parity; full payload/denominator comparison is marked
unavailable from the Batch receipt.

Usage:
  python3 full_width_batch_driver.py --snapshot /path/to/read-only/code \
      --contract /path/to/sealed_combined_contract.json \
      --runtime-catalog /path/to/runtime_catalog.json \
      --current-authorizer package.module:function --out result.json

Contract shape (sealed after build):
  schema, tag, respondents, questions, root, exact_path, manifest_sha256,
  i02, reconstructed_v1_release_ref (or release_ref),
  source_wave_country_context (one synthetic scalar),
  operations: {"f2_forward_raw": {"query_ref": "...", "predicate_ref": "..."},
               "f2_reverse_raw": {...}},
  optional runtime_catalog.

The catalog file may contain authorities/predicates/queries public documents.
No catalog is supplied here because the combined fixture is still building.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import asdict
from pathlib import Path
from unittest.mock import patch


FORWARD = ("f2_forward_raw", "f2_forward")
REVERSE = ("f2_reverse_raw", "f2_reverse")
OPERATION_KEYS = (FORWARD, REVERSE)


def fail(status: str, detail: str, **extra):
    return {"status": status, "detail": detail, **extra}


def load_json(path: Path):
    return json.loads(path.read_text())


def operation_entry(contract, aliases):
    ops = contract.get("operations", {})
    if isinstance(ops, list):
        by_label = {
            str(row.get("label") or row.get("operation")): row
            for row in ops if isinstance(row, dict)
        }
    elif isinstance(ops, dict):
        by_label = ops
    else:
        raise ValueError("contract.operations must be a mapping or list")
    for alias in aliases:
        if alias in by_label:
            return alias, by_label[alias]
    raise ValueError(f"missing contract operation {aliases[0]}")


def ref_string(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and all(k in value for k in ("kind", "object_id", "content_hash")):
        return f"{value['kind']}|{value['object_id']}|{value['content_hash']}"
    raise ValueError("expected an exact ref string or exact ref mapping")


def contract_validate(contract):
    required = ("root", "exact_path", "manifest_sha256", "i02",
                "source_wave_country_context", "operations")
    missing = [key for key in required if key not in contract]
    if missing:
        raise ValueError("contract missing fields: " + ", ".join(missing))
    release = contract.get("reconstructed_v1_release_ref", contract.get("release_ref"))
    if release is None:
        raise ValueError("contract missing reconstructed_v1_release_ref/release_ref")
    context = contract["source_wave_country_context"]
    if not isinstance(context, str) or not context.strip():
        raise ValueError("source_wave_country_context must be one nonempty string")
    if isinstance(context, (list, tuple)) or len(context.split("|")) > 1:
        raise ValueError("multi-country execution is outside this template")
    if int(contract.get("respondents", 0)) <= 0 or int(contract.get("questions", 0)) <= 0:
        raise ValueError("respondents/questions must be positive")
    forward = operation_entry(contract, FORWARD)
    reverse = operation_entry(contract, REVERSE)
    fq = ref_string(forward[1]["query_ref"])
    rq = ref_string(reverse[1]["query_ref"])
    fp = ref_string(forward[1]["predicate_ref"])
    rp = ref_string(reverse[1]["predicate_ref"])
    if fq == rq:
        raise ValueError("forward/reverse query refs must be genuinely distinct")
    return {
        "release_ref": ref_string(release),
        "forward": {"label": FORWARD[0], "query_ref": fq, "predicate_ref": fp},
        "reverse": {"label": REVERSE[0], "query_ref": rq, "predicate_ref": rp},
        "context": context,
    }


def load_catalog(contract, catalog_path):
    from rawlsing_next.pre553_carrier_execution import (
        RuntimeObjectCatalog, materialize_public_object,
    )
    raw = contract.get("runtime_catalog")
    if raw is None and catalog_path:
        raw = load_json(catalog_path)
    if not isinstance(raw, dict):
        raise ValueError(
            "runtime catalog required in contract or --runtime-catalog "
            "(authorities/predicates/queries public documents)"
        )
    return RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in raw.get("authorities", ())),
        predicates=tuple(materialize_public_object(v) for v in raw.get("predicates", ())),
        queries=tuple(materialize_public_object(v) for v in raw.get("queries", ())),
        discovery_authorities=tuple(
            materialize_public_object(v) for v in raw.get("discovery_authorities", ())
        ),
    )


def import_authorizer(spec: str):
    if ":" not in spec:
        raise ValueError("--current-authorizer must be module:callable")
    module_name, function_name = spec.split(":", 1)
    fn = getattr(importlib.import_module(module_name), function_name)
    if not callable(fn):
        raise ValueError("--current-authorizer target is not callable")
    return fn


def baseline_map(path, expected_manifest):
    if not path:
        return None, "NOT_AVAILABLE"
    data = load_json(path)
    manifest = data.get("estate_manifest")
    if manifest is not None and manifest != expected_manifest:
        return None, "BASELINE_FIXTURE_MISMATCH"
    rows = data.get("operations", data)
    if isinstance(rows, list):
        by_label = {str(r.get("label") or r.get("operation")): r for r in rows}
    elif isinstance(rows, dict):
        by_label = rows
    else:
        return None, "BASELINE_UNREADABLE"
    result = {}
    for aliases in OPERATION_KEYS:
        for alias in aliases:
            if alias in by_label:
                row = by_label[alias]
                fact = row.get("fact_ref")
                if fact is None:
                    return None, "BASELINE_FACT_REF_MISSING"
                result[aliases[0]] = {
                    "fact_ref": ref_string(fact),
                    "query_ref": ref_string(row["query_ref"]) if row.get("query_ref") else None,
                    "predicate_ref": ref_string(row["predicate_ref"]) if row.get("predicate_ref") else None,
                    "has_full_payload": row.get("payload") is not None,
                }
                break
    if set(result) != {x[0] for x in OPERATION_KEYS}:
        return None, "BASELINE_OPERATION_MISSING"
    return result, "AVAILABLE"


def run(args):
    contract = load_json(args.contract)
    spec = contract_validate(contract)
    if args.validate_only:
        return {
            "status": "VALID_CONTRACT_NO_EXECUTION",
            "contract": str(args.contract),
            "fixture": {
                "tag": contract.get("tag"),
                "respondents": contract.get("respondents"),
                "questions": contract.get("questions"),
                "manifest_sha256": contract["manifest_sha256"],
                "release_ref": spec["release_ref"],
                "source_wave_country_context": spec["context"],
            },
            "operations": [spec["forward"], spec["reverse"]],
            "session_scope": "NOT_OPENED_VALIDATION_ONLY",
            "batch_executed": False,
            "full_fact_payload": "NOT_CARRIED_BY_BATCH_RECEIPT",
            "denominator_semantics": "BATCH_RECEIPT_NOT_CARRIED",
            "multi_country_claim": False,
        }

    if not args.snapshot or not args.current_authorizer:
        raise ValueError("--snapshot and --current-authorizer are required for execution")
    sys.path.insert(0, str(Path(args.snapshot).resolve()))
    # Re-import only after the read-only snapshot is placed first.
    from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots as _I02
    from rawlsing_next.pre553_batch_runner import BatchManifest as _Manifest
    from rawlsing_next.pre553_batch_runner import BatchUnitSpec as _Unit
    from rawlsing_next.pre553_empirical_objects import exact_ref as _exact
    from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission as _Admission
    from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch as _execute
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session as _Session

    catalog = load_catalog(contract, args.runtime_catalog)
    authorizer = import_authorizer(args.current_authorizer)
    release_ref = _exact(spec["release_ref"], "release_ref")
    ops = (spec["forward"], spec["reverse"])
    units = tuple(
        _Unit("QUERY", _exact(op["query_ref"], "query_ref"), (release_ref,))
        for op in ops
    )
    manifest = _Manifest(units)
    predicates = {
        _exact(op["query_ref"], "query_ref").key: _exact(op["predicate_ref"], "predicate_ref")
        for op in ops
    }
    admission = _Admission.open(
        root=Path(contract["root"]),
        exact_path=contract["exact_path"],
        independently_held_manifest_sha256=contract["manifest_sha256"],
        independently_held_i02=_I02(**contract["i02"]),
        release_ref=release_ref,
        runtime_catalog=catalog,
        current_authorizer=authorizer,
    )

    builds = []
    original_build = _Session._build

    def counted_build(self):
        builds.append(1)
        return original_build(self)

    with patch.object(_Session, "_build", counted_build):
        runner = _execute(
            admission,
            manifest=manifest,
            predicate_ref_by_query=predicates,
        )
    summary = runner.summary()
    if len(builds) != 1:
        return fail("SESSION_COUNT_MISMATCH",
                    f"expected one prepared build, observed {len(builds)}",
                    session_builds=len(builds))
    receipts = {receipt.unit_ref.key: receipt for receipt in runner.receipts}
    operations = []
    for op in ops:
        unit = next(unit for unit in manifest.units
                    if unit.job_ref.key == _exact(op["query_ref"], "query_ref").key)
        receipt = receipts.get(unit.unit_ref.key)
        if receipt is None:
            return fail("BATCH_RECEIPT_MISSING", op["label"])
        operations.append({
            "label": op["label"],
            "query_ref": op["query_ref"],
            "predicate_ref": op["predicate_ref"],
            "unit_ref": unit.unit_ref.key,
            "receipt_ref": receipt.receipt_ref.key,
            "receipt_hash": receipt.receipt_hash,
            "state": receipt.state,
            "execution_performed": receipt.execution_performed,
            "result_refs": [ref.key for ref in receipt.result_refs],
            "provenance_refs": [ref.key for ref in receipt.provenance_refs],
        })
    if summary.completed_units != 2 or summary.full_coverage is not True:
        return fail("BATCH_NOT_COMPLETE", summary.batch_state,
                    batch_summary=asdict(summary))

    baseline, baseline_status = baseline_map(args.baseline, contract["manifest_sha256"])
    if baseline_status not in ("AVAILABLE", "NOT_AVAILABLE"):
        return fail("BASELINE_NOT_USABLE", baseline_status)
    parity = []
    for op in operations:
        row = {"label": op["label"], "baseline_status": baseline_status,
               "batch_result_refs": op["result_refs"],
               "full_payload_comparison": "NOT_CARRIED_BY_BATCH_RECEIPT",
               "denominator_comparison": "NOT_CARRIED_BY_BATCH_RECEIPT"}
        if baseline is not None:
            expected = baseline[op["label"]]
            row.update({
                "baseline_fact_ref": expected["fact_ref"],
                "fact_ref_equal": op["result_refs"] == [expected["fact_ref"]],
                "baseline_has_full_payload": expected["has_full_payload"],
                "query_ref_equal": expected["query_ref"] in (None, op["query_ref"]),
                "predicate_ref_equal": expected["predicate_ref"] in (None, op["predicate_ref"]),
            })
        parity.append(row)
    if any(row.get("fact_ref_equal") is False for row in parity):
        return fail("BASELINE_FACT_REF_MISMATCH", "batch result refs differ", parity=parity)

    return {
        "status": "PASS",
        "schema": "ANVIL_FULL_WIDTH_BATCH_RESULT@1",
        "contract": str(args.contract),
        "fixture": {
            "tag": contract.get("tag"),
            "respondents": contract.get("respondents"),
            "questions": contract.get("questions"),
            "manifest_sha256": contract["manifest_sha256"],
            "release_ref": spec["release_ref"],
            "source_wave_country_context": spec["context"],
        },
        "batch": {
            "manifest_ref": manifest.manifest_ref.key,
            "manifest_hash": manifest.manifest_hash,
            "summary": asdict(summary),
            "operation_count": len(operations),
        },
        "session_scope": {
            "builds_observed": len(builds),
            "one_prepared_session": len(builds) == 1,
            "source": "execute_saved_batch prepared_i03 context",
        },
        "operations": operations,
        "parity": {
            "baseline_status": baseline_status,
            "operations": parity,
            "note": "Batch receipts carry result refs/receipts; full payload and denominator/cell comparison require the existing direct artifact API and are not faked here.",
        },
        "full_fact_payload": {
            "status": "NOT_CARRIED_BY_BATCH_RECEIPT",
            "reuse": "existing execute_i03/artifact-receipt API; not executed by this driver",
        },
        "denominator_semantics": {
            "status": "BATCH_RECEIPT_NOT_CARRIED",
            "note": "execute_saved_batch delegates to execute_i03; no denominator is reinterpreted here.",
        },
        "claims": {
            "one_synthetic_source_wave_country_context": True,
            "multi_country_execution": False,
            "native_or_raw_source": False,
            "performance_claim": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--runtime-catalog", type=Path)
    parser.add_argument("--current-authorizer")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args)
    except Exception as exc:
        result = fail("REFUSED", f"{type(exc).__name__}: {exc}")
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") in ("PASS", "VALID_CONTRACT_NO_EXECUTION") else 2


if __name__ == "__main__":
    raise SystemExit(main())
