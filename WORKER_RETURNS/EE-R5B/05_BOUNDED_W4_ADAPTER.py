#!/usr/bin/env python3
"""EE-R5B bounded mechanical bridge from EE-W4 JSON envelopes to bound A/B/C owners.

This module does not implement survey semantics, query logic, storage design, or
candidate selection.  It only validates the frozen EE-W4 single-step transport,
pins the exact EE-R4B owner identity for A/B/C, invokes a supplied bound owner
executor, and normalizes the executor receipt to the independently-qualified
EE-W4 response shape.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping

HARNESS_SCHEMA = "RAWLSING_EE_W4_ABC_MEASUREMENT_HARNESS@1.0.0"
BRIDGE_SCHEMA = "RAWLSING_EE_R5B_OWNER_BOUND_W4_BRIDGE@1.0.0"
BRIDGE_ID = "EE_R5B_W4_OWNER_BOUND_MECHANICAL_BRIDGE_V1"

OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
OWNER_BINDINGS = {
    "A": {
        "candidate_id": "A",
        "implementation_owner_commit": OWNER_COMMIT,
        "path": "rawlsing_next/pre553_r5_source_backed_adapter.py",
        "blob": "d4915e7e6755ba1850756aebff72f982f73a332b",
        "physical_meaning": "R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE",
    },
    "B": {
        "candidate_id": "B",
        "implementation_owner_commit": OWNER_COMMIT,
        "path": "rawlsing_next/pre553_source_backed_c11_facade.py",
        "blob": "7c509c2098d0030f253344eb3f682471378812a8",
        "physical_meaning": "SOURCE_BACKED_VIRTUAL_C11",
    },
    "C": {
        "candidate_id": "C",
        "implementation_owner_commit": OWNER_COMMIT,
        "path": "rawlsing_next/pre553_route_c_accelerators.py",
        "blob": "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889",
        "physical_meaning": "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS",
    },
}

OPERATIONS = tuple(f"EEW1-OP{i:03d}" for i in (1, 2, 3, 4, 5, 6, 20, 21, 22))
ALLOWED_ACTIONS = {
    "EEW1-OP001": frozenset({"EXECUTE"}),
    "EEW1-OP002": frozenset({"EXECUTE"}),
    "EEW1-OP003": frozenset({"EXECUTE"}),
    "EEW1-OP004": frozenset({"EXECUTE"}),
    "EEW1-OP005": frozenset({"EXECUTE"}),
    "EEW1-OP006": frozenset({"EXECUTE"}),
    "EEW1-OP020": frozenset({"REBUILD", "REPLAY", "AUDIT"}),
    "EEW1-OP021": frozenset({"REBUILD", "INVALIDATE_SOURCE", "REPLAY", "AUDIT"}),
    "EEW1-OP022": frozenset({"REBUILD", "INVALIDATE_AUTHORITY", "REPLAY", "AUDIT"}),
}
C_ALLOWED_ACCELERATORS = frozenset({
    "CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE",
    "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK",
})

class BridgeError(ValueError):
    pass


def _hex64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _exact_owner_binding(candidate: str) -> Mapping[str, Any]:
    try:
        return OWNER_BINDINGS[candidate]
    except KeyError as exc:
        raise BridgeError("candidate must be exactly A, B, or C") from exc


def validate_w4_request(candidate: str, envelope: Mapping[str, Any]) -> dict[str, Any]:
    _exact_owner_binding(candidate)
    if not isinstance(envelope, Mapping):
        raise BridgeError("EE-W4 request must be an object")
    if envelope.get("schema") != HARNESS_SCHEMA:
        raise BridgeError("unexpected EE-W4 harness schema")
    op = envelope.get("operation_id")
    if op not in OPERATIONS:
        raise BridgeError("operation is outside the exact EE-R5B nine-operation surface")
    action = envelope.get("action")
    if action not in ALLOWED_ACTIONS[op]:
        raise BridgeError(f"{op} does not authorize action {action!r} at the candidate boundary")
    for key in ("workload_id", "plan_sha256", "step_id", "universe_id"):
        if not isinstance(envelope.get(key), str) or not envelope[key]:
            raise BridgeError(f"missing/invalid {key}")
    if not _hex64(envelope["plan_sha256"]):
        raise BridgeError("plan_sha256 must be lowercase SHA-256")
    request = envelope.get("request")
    if not isinstance(request, Mapping):
        raise BridgeError("candidate action requires an exact request object")
    invalidation_targets = envelope.get("invalidation_targets")
    if invalidation_targets is not None and (
        not isinstance(invalidation_targets, list) or not all(isinstance(x, str) and x for x in invalidation_targets)
    ):
        raise BridgeError("invalidation_targets must be absent or a string list")
    return dict(envelope)


def _validate_owner_receipt(candidate: str, receipt: Mapping[str, Any]) -> None:
    expected = OWNER_BINDINGS[candidate]
    observed = receipt.get("owner_binding")
    if not isinstance(observed, Mapping):
        raise BridgeError("bound owner executor omitted owner_binding")
    for key in ("candidate_id", "implementation_owner_commit", "path", "blob"):
        if observed.get(key) != expected[key]:
            raise BridgeError(f"bound owner identity mismatch at {key}")


def _validate_c_surface(candidate: str, receipt: Mapping[str, Any]) -> None:
    physical = receipt.get("physical_execution")
    if physical is None:
        return
    if not isinstance(physical, Mapping):
        raise BridgeError("physical_execution must be an object")
    accelerators = physical.get("accelerators")
    if accelerators is None:
        return
    if not isinstance(accelerators, list) or not all(isinstance(x, str) for x in accelerators):
        raise BridgeError("accelerators must be a string list")
    aset = set(accelerators)
    if candidate == "C":
        if not aset.issubset(C_ALLOWED_ACCELERATORS):
            raise BridgeError("candidate C attempted an accelerator outside the exact R4B-permitted CACC1/CACC2 surface")
    elif aset:
        raise BridgeError("candidate A/B receipt declared an accelerator surface")


def normalize_owner_receipt(candidate: str, receipt: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(receipt, Mapping):
        raise BridgeError("bound owner executor must return an object")
    _validate_owner_receipt(candidate, receipt)
    _validate_c_surface(candidate, receipt)
    digest = receipt.get("semantic_output_sha256")
    if not _hex64(digest):
        raise BridgeError("bound owner receipt requires semantic_output_sha256")
    identities = receipt.get("identities") or {}
    telemetry = receipt.get("telemetry") or {}
    if not isinstance(identities, Mapping) or not isinstance(telemetry, Mapping):
        raise BridgeError("identities/telemetry must be objects")
    for key in ("source_open_count", "source_decode_count"):
        value = telemetry.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise BridgeError(f"telemetry.{key} must be a nonnegative integer")
    forbidden = {"rank", "ranking", "score", "winner", "selection", "recommendation"}
    if forbidden.intersection(receipt):
        raise BridgeError("ranking/selection field forbidden at EE-R5B bridge")
    return {
        "status": "OK",
        "semantic_output_sha256": digest,
        "identities": dict(identities),
        "telemetry": dict(telemetry),
    }


def adapt_step(
    candidate: str,
    envelope: Mapping[str, Any],
    *,
    scratch: Path,
    durable: Path,
    owner_executor: Callable[..., Mapping[str, Any]],
) -> dict[str, Any]:
    request = validate_w4_request(candidate, envelope)
    scratch = Path(scratch)
    durable = Path(durable)
    scratch.mkdir(parents=True, exist_ok=True)
    durable.mkdir(parents=True, exist_ok=True)
    binding = dict(_exact_owner_binding(candidate))
    receipt = owner_executor(
        candidate_id=candidate,
        owner_binding=binding,
        operation_id=request["operation_id"],
        action=request["action"],
        request=dict(request["request"]),
        invalidation_targets=list(request.get("invalidation_targets") or []),
        scratch=scratch,
        durable=durable,
    )
    return normalize_owner_receipt(candidate, receipt)


def _load_provider(spec: str) -> Callable[..., Mapping[str, Any]]:
    if ":" not in spec:
        raise BridgeError("provider must use module:function syntax")
    module_name, function_name = spec.rsplit(":", 1)
    if not module_name or not function_name:
        raise BridgeError("provider must use module:function syntax")
    module = importlib.import_module(module_name)
    provider = getattr(module, function_name, None)
    if not callable(provider):
        raise BridgeError("provider target is not callable")
    return provider


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, choices=("A", "B", "C"))
    parser.add_argument("--provider", required=True, help="bound owner executor as module:function")
    parser.add_argument("--request", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--scratch", required=True)
    parser.add_argument("--durable", required=True)
    args = parser.parse_args(argv)
    envelope = json.loads(Path(args.request).read_text(encoding="utf-8"))
    response = adapt_step(
        args.candidate,
        envelope,
        scratch=Path(args.scratch),
        durable=Path(args.durable),
        owner_executor=_load_provider(args.provider),
    )
    path = Path(args.response)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
