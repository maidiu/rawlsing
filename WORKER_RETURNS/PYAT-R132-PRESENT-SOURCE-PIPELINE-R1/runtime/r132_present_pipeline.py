#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_issued_workload import (
    NativeWorkload,
    WorkloadAdmissionError,
    execute_issued_workload,
)

HANDOFF = Path(".r61/r132-present-source-pipeline/s44_source_runtime_handoff.json")
RUNTIME_MEMBERS = ("resolver", "workloads", "source_factory", "host", "purpose")


class R132Refused(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(code + (":" + detail if detail else ""))


def load_handoff(path: Path) -> dict[str, Any]:
    doc = json.loads(path.read_text())
    if doc.get("schema") != "S44_SOURCE_RUNTIME_HANDOFF@1":
        raise R132Refused("R132_HANDOFF_SCHEMA_MISMATCH")
    if doc.get("raw_source_read") is not False or doc.get("grant_present") is not False:
        raise R132Refused("R132_HANDOFF_EVIDENCE_GRADE_MISMATCH")
    if doc.get("single_decision", {}).get("selected_wave") != "SRC27":
        raise R132Refused("R132_SELECTED_SOURCE_MISMATCH")
    return doc


def validate_runtime(runtime: Any) -> dict[str, Any]:
    missing = [name for name in RUNTIME_MEMBERS if not hasattr(runtime, name)]
    if missing:
        raise R132Refused("R132_RUNTIME_INCOMPLETE", ",".join(missing))
    if not getattr(runtime, "host") or not getattr(runtime, "purpose"):
        raise R132Refused("R132_RUNTIME_MISSING_HOST_OR_PURPOSE")
    workloads = getattr(runtime, "workloads")
    if not isinstance(workloads, dict) or "SRC27" not in workloads:
        raise R132Refused("R132_RUNTIME_MISSING_SRC27_WORKLOAD")
    selected = workloads["SRC27"]
    packets = (selected,) if isinstance(selected, NativeWorkload) else tuple(selected)
    if not packets or any(not isinstance(x, NativeWorkload) for x in packets):
        raise R132Refused("R132_RUNTIME_SRC27_NOT_NATIVE_WORKLOAD")
    return {
        "members": list(RUNTIME_MEMBERS),
        "host": str(runtime.host),
        "purpose": str(runtime.purpose),
        "src27_packet_count": len(packets),
    }


def run(runtime_module: str | None, handoff_path: Path) -> dict[str, Any]:
    handoff = load_handoff(handoff_path)
    if runtime_module is None:
        return {
            "schema": "PYAT_R132_PRESENT_PIPELINE_ATTEMPT@1",
            "status": "BLOCKED__CURRENT_NATIVE_RUNTIME_MODULE_NOT_PROVIDED",
            "source_dependent_operation": "SOURCE_FILES -> PRE553 EMPIRICAL/LEARNED -> FF/V553",
            "source_read": False,
            "pipeline_code_present": True,
            "pipeline_code_unavailable": False,
            "handoff": {
                "path": str(handoff_path),
                "sha256": __import__("hashlib").sha256(handoff_path.read_bytes()).hexdigest(),
                "grant_present": handoff["grant_present"],
                "raw_source_read": handoff["raw_source_read"],
                "selected_wave": handoff["single_decision"]["selected_wave"],
                "selected_source": handoff["single_decision"]["selected_source"],
            },
            "runtime_contract": handoff["runtime_contract"],
            "missing_runtime_fields": [
                "runtime_module",
                "runtime.resolver",
                "runtime.workloads[SRC27]",
                "runtime.source_factory",
                "runtime.host",
                "runtime.purpose",
            ],
            "missing_current_decisions": handoff["single_decision"]["exact_missing_competent_decisions"],
            "responsible_owners": [
                {
                    "field": "SOURCE_HOST_PURPOSE",
                    "owner": "competent original source access/licence custodian and deployment host operator",
                    "evidence": "exact current source edition/hash, host identity, purpose, expiry/revocation, private retention/export scope",
                },
                {
                    "field": "COMPLETE_NATIVE_U",
                    "owner": "original questionnaire/instrument and source-structure issuer",
                    "evidence": "complete administered occurrence inventory and exact native item/occurrence bindings",
                },
                {
                    "field": "RESPONSE_ROUTING_CARRIER",
                    "owner": "source response/routing/subject identity and sampling-design issuers",
                    "evidence": "response states, routing/risk sets, respondent namespace, design/weights/estimand",
                },
                {
                    "field": "SCIENTIFIC_E_PRE",
                    "owner": "competent source-specific scientific operation issuer",
                    "evidence": "frozen U/Epre roots and exact target/conditioner/query/predicate/discovery grammar",
                },
                {
                    "field": "CONSUMER_PURPOSE",
                    "owner": "original purpose issuer and existing consumer authorities",
                    "evidence": "permitted aggregate empirical/learned/FF/V553 consumer scope",
                },
            ],
            "ready_executable_call": {
                "api": "rawlsing_next.pre553_issued_workload.execute_issued_workload",
                "api_blob": "be5ffc75287ad25ac35eb03bc5e506c00a5837a2",
                "call": "execute_issued_workload(workload=runtime.workloads['SRC27'], resolver=runtime.resolver, source_factory=runtime.source_factory, host=runtime.host, purpose=runtime.purpose, allow_test_only=False, prior_receipts=(), max_units=None)",
                "executes_only_after": "runtime.resolver returns CURRENT_GRANTED exact IssuedWorkloadRecord and workload admission succeeds",
            },
        }
    runtime = importlib.import_module(runtime_module)
    contract = validate_runtime(runtime)
    workloads = runtime.workloads["SRC27"]
    packets = (workloads,) if isinstance(workloads, NativeWorkload) else tuple(workloads)
    results = []
    for packet in packets:
        result = execute_issued_workload(
            packet,
            runtime.resolver,
            source_factory=runtime.source_factory,
            host=runtime.host,
            purpose=runtime.purpose,
            allow_test_only=False,
            prior_receipts=(),
            max_units=None,
        )
        results.append({
            "decision_ref": result.decision_ref.as_dict(),
            "envelope_sha256": result.envelope_sha256,
            "scope": result.scope,
            "manifest_identity": getattr(result.manifest, "manifest_identity", None),
            "output_refs": [x.as_dict() for x in result.output_refs],
            "receipt_count": len(result.receipts),
        })
    return {
        "schema": "PYAT_R132_PRESENT_PIPELINE_ATTEMPT@1",
        "status": "SOURCE_PIPELINE_EXECUTED",
        "source_read": True,
        "runtime_contract": contract,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-module")
    parser.add_argument("--handoff", type=Path, default=HANDOFF)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.runtime_module, args.handoff)
        status = 0 if result.get("status") == "SOURCE_PIPELINE_EXECUTED" else 2
    except (R132Refused, WorkloadAdmissionError) as exc:
        result = {
            "schema": "PYAT_R132_PRESENT_PIPELINE_ATTEMPT@1",
            "status": "BLOCKED__NATIVE_ADMISSION_REFUSED",
            "source_read": False,
            "failure": {
                "type": type(exc).__name__,
                "code": getattr(exc, "code", None),
                "message": str(exc),
            },
        }
        status = 2
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
