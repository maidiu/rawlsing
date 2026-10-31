"""Sourcefree P41-style progressive/as-of/revoke/read service over current E03.

The service calls the current synthetic E03 producer, which itself calls the
current N10E provider, C1 composition and F8 evaluator. It does not claim an
operative N9 world, N10W owner, source rule, actor state or model use.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping

from rawlsing_next.pre553_n9_n10w_progressive_candidate import (
    E03_ORACLE,
    E03_TAG,
    build_synthetic_world,
    run_progressive_chain,
)

SERVICE_VERSION = "RRIF_P41_CURRENT_SOURCEFREE@1.0.0"
RECEIPT_SCHEMA = "RRIF_P41_CURRENT_RECEIPT@1"
GRADE = "SOURCEFREE_SYNTHETIC_ONLY__NOT_OPERATIVE_N9__NOT_MODEL_USE"
CLOCK_DOMAIN = "ADAPTER_TEST_ONLY_CLOCK__NO_SOURCE_RULE"


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class CurrentP41Receipt:
    material: Mapping[str, Any]
    content_hash: str

    def as_dict(self) -> dict[str, Any]:
        return dict(self.material)


def _ref_dict(value: Any) -> Any:
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if isinstance(value, Mapping):
        return dict(value)
    return value


def _step_material(step: Any) -> dict[str, Any]:
    return {
        "step_id": step.step_id,
        "target": "Y",
        "conditioners": [list(c) for c in step.conditioners],
        "producer_route": step.producer_route,
        "state": step.producer_fact_state,
        "consumer_state": step.consumer_state,
        "denominator": step.raw_denominator_support,
        "cells": {
            cell: {
                "numerator": int(value["raw_numerator_support"]),
                "fraction": dict(value["raw_probability_exact_fraction"]),
            }
            for cell, value in step.cells.items()
        },
        "uncertainty_state": step.uncertainty_state,
        "evidence_ref": _ref_dict(step.produced_evidence.evidence_ref),
        "risk_set_ref": dict(step.risk_set_ref),
        "release_ref": _ref_dict(step.release_ref),
    }


class CurrentP41Service:
    def __init__(self, world: Mapping[str, Any] | None = None):
        self._world = world or build_synthetic_world(tag=E03_TAG)
        self._receipts: dict[str, dict[str, Any]] = {}
        self._revoked: set[str] = set()
        self._clock = {
            "observation_effective": "2026-10-31",
            "reference_time": "2026-10-31",
            "as_of": "2026-10-31",
            "publication": "2026-10-31",
            "rule_revision": 1,
            "clock_domain": CLOCK_DOMAIN,
        }

    def _build_receipt(self, chain: Any) -> CurrentP41Receipt:
        steps = [_step_material(step) for step in chain.steps]
        f8 = {
            item["step_id"]: {
                "result_state": item["result_state"],
                "exact_disposition": item.get("exact_disposition"),
                "exact_reason": item.get("exact_reason"),
                "evidence_ref": _ref_dict(item.get("exact_evidence_ref")),
            }
            for item in chain.f8_consumptions
        }
        material = {
            "schema": RECEIPT_SCHEMA,
            "service": SERVICE_VERSION,
            "grade": GRADE,
            "provider": {
                "n10e": "current pre553_empirical_possibility_provider",
                "c1": "current pre553_analytical_composition",
                "f8": "current source_backed_positioned_subject_possibility",
                "e03": "current pre553_n9_n10w_progressive_candidate",
            },
            "n9_world": {
                "world_tag": E03_TAG,
                "selection_kind": "SOURCE_FREE_SYNTHETIC",
                "real_current": False,
                "n9_owner_implemented": False,
                "n10w_owner_implemented": False,
                "scope": GRADE,
            },
            "clocks": dict(self._clock),
            "revoked_scopes": sorted(self._revoked),
            "steps": steps,
            "f8_consumptions": f8,
            "minority_cells_present": all(len(step["cells"]) == 2 for step in steps),
            "actor_state_present": False,
            "personhood_present": False,
            "route_probability_present": False,
            "consumer": {
                "name": "GENERIC_POSITIONED_SUBJECT",
                "permission_state": "TEST_ONLY_SOURCEFREE",
            },
            "effects": {
                "real_current_claim": False,
                "source_meaning_inference": False,
                "model_use_grant": False,
                "actor_v3_effect": False,
            },
        }
        content_hash = _hash(material)
        material["content_hash"] = content_hash
        self._receipts[content_hash] = material
        return CurrentP41Receipt(material=dict(material), content_hash=content_hash)

    def progressive(self) -> CurrentP41Receipt | dict[str, Any]:
        if "progressive" in self._revoked:
            return {"status": "REFUSED", "reason": "PROGRESSIVE_SCOPE_REVOKED", "grade": GRADE}
        return self._build_receipt(run_progressive_chain(self._world))

    def consumer_read(self) -> dict[str, Any]:
        if "empirical" in self._revoked:
            return {"status": "REFUSED", "reason": "EMPIRICAL_SCOPE_REVOKED", "grade": GRADE}
        receipt = self.progressive()
        if isinstance(receipt, dict):
            return receipt
        material = receipt.as_dict()
        return {
            "status": "EXACT_SUPPORTED",
            "grade": GRADE,
            "consumer": "GENERIC_POSITIONED_SUBJECT",
            "steps": material["steps"],
            "f8_consumptions": material["f8_consumptions"],
            "values_read": [
                {
                    "step_id": step["step_id"],
                    "cell": cell,
                    "numerator": value["numerator"],
                    "fraction": value["fraction"],
                }
                for step in material["steps"]
                for cell, value in step["cells"].items()
            ],
            "actor_state_present": False,
        }

    def historical(self, receipt_hash: str) -> dict[str, Any] | None:
        receipt = self._receipts.get(receipt_hash)
        if receipt is None:
            return None
        return {
            "archival_only": True,
            "fresh_use_authorized": False,
            "receipt": json.loads(json.dumps(receipt)),
        }

    def revoke(self, scope: str) -> dict[str, Any]:
        self._revoked.add(str(scope))
        return {
            "scope": scope,
            "revoked": True,
            "historical_receipts_retained": bool(self._receipts),
        }

    def as_of(self, valid_at: str, published_asof: str, *, rule_revision: int = 1) -> dict[str, Any]:
        self._clock.update({
            "reference_time": str(valid_at),
            "as_of": str(valid_at),
            "publication": str(published_asof),
            "rule_revision": int(rule_revision),
        })
        return dict(self._clock)

    def cold_restore(self, payload: str | Mapping[str, Any]) -> dict[str, Any]:
        material = json.loads(payload) if isinstance(payload, str) else dict(payload)
        saved_hash = material.get("content_hash")
        check = {k: v for k, v in material.items() if k != "content_hash"}
        if saved_hash != _hash(check):
            return {"status": "REFUSED", "reason": "RECEIPT_HASH_MISMATCH"}
        if material.get("n9_world", {}).get("real_current") is not False:
            return {"status": "REFUSED", "reason": "REAL_CURRENT_NOT_AUTHORIZED"}
        if material.get("actor_state_present") is not False:
            return {"status": "REFUSED", "reason": "ACTOR_STATE_NOT_AUTHORIZED"}
        for step, oracle_key in zip(material.get("steps", []), ("step1", "step2", "step3")):
            oracle = E03_ORACLE[oracle_key]
            if step.get("denominator") != oracle["denominator"]:
                return {"status": "REFUSED", "reason": "SOURCE_GEOMETRY_MISMATCH"}
            if {k: v["numerator"] for k, v in step.get("cells", {}).items()} != oracle["cells"]:
                return {"status": "REFUSED", "reason": "SOURCE_COUNT_MISMATCH"}
        return {"status": "RESTORED", "content_hash": saved_hash, "material": material}

    def validate_receipt(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        material = dict(payload)
        saved_hash = material.get("content_hash")
        check = {k: v for k, v in material.items() if k != "content_hash"}
        if saved_hash != _hash(check):
            return {"status": "REFUSED", "reason": "RECEIPT_HASH_MISMATCH"}
        return self.cold_restore(material)
