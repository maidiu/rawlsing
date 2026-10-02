"""AT17/N10E successor requalification helper.

Reads the HQ-adopted AT07 successor-spine oracle package and exposes its expected
preimages. NOTHING here derives expected truth from production output: the expected
preimage comes only from the adopted oracle artifacts, so a production identity can
be compared against it but can never define it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PKG = Path(__file__).resolve().parents[2] / (
    "WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1"
)

ADOPTED_SUCCESSOR = {
    "forward": "01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd",
    "reverse": "a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca",
}
HISTORICAL_R8 = {
    "forward": "03610f9d91b23cfb6f862dc91b5de92c7f4e4b8e44a53b9efdacb1cf73af6b9e",
    "reverse": "1202822cf98d802c04440328496dc64ee02e6d6030a3da6c9bf10ef1a6490a3c",
}
SUCCESSOR_SIX = {
    "discovery_receipt_refs": [],
    "discovery_frontier_ref": None,
    "recursive_handoff_refs": [],
    "recursive_lineage_refs": [],
    "joint_component_count": 1,
    "joint_order_semantics": "SEMANTIC_ORDERED",
}
CONSERVED_HISTORICAL_FIELDS = 38


def _load(name: str) -> Any:
    return json.loads((PKG / name).read_text())


def wire(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value).encode("utf-8")).hexdigest()


def successor_canonical(direction: str) -> dict:
    return _load(f"{direction.upper()}_SUCCESSOR_CANONICAL.json")


def historical_canonical(direction: str) -> dict:
    return _load(f"{direction.upper()}_HISTORICAL_CANONICAL.json")


def successor_digest(direction: str) -> str:
    return digest(successor_canonical(direction))


def historical_digest(direction: str) -> str:
    return digest(historical_canonical(direction))


def r8_spine() -> dict:
    return _load("INPUTS/r8_spine.json")["identity_spine"]


def frozen_consumer_result_hash(direction: str) -> str | None:
    pre = _load(f"{direction.upper()}_DERIVATION_PREIMAGES.json")
    node = pre["consumer_result_preimage"]
    result = node.get("exact_lane") or node.get("negative_lane")
    return None if result is None else result.get("result_hash")


def frozen_evidence_ref(direction: str) -> dict:
    return _load(f"{direction.upper()}_DERIVATION_PREIMAGES.json")[
        "evidence_preimage"]["ref"]


def frozen_witness_preimage(direction: str) -> dict:
    return _load(f"{direction.upper()}_DERIVATION_PREIMAGES.json")["witness_preimage"]


__all__ = [
    "ADOPTED_SUCCESSOR", "HISTORICAL_R8", "SUCCESSOR_SIX",
    "CONSERVED_HISTORICAL_FIELDS", "PKG",
    "successor_canonical", "historical_canonical",
    "successor_digest", "historical_digest",
    "r8_spine", "frozen_consumer_result_hash", "frozen_evidence_ref",
    "frozen_witness_preimage", "wire", "digest",
]
