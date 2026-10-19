"""B43 issuer-bound admission control: close WG0L's three provenance REDs.

WG0L proved that a copied ExecutablePlan.op_specs can change source_edition or
native_item_ids while the registered contract is unchanged, and a changed
release_tag reaches native I03 (KeyError) instead of early bound-plan refusal.

This module compares the plan's consumed descriptor fields against an
issuer-controlled contract BEFORE any native execution. Mismatch is a typed
early denial; no forged descriptor ever reaches I03/Batch or a consumer.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping


class B43AdmissionDenied(ValueError):
    """Typed early refusal at the issuer-bound admission boundary."""

    def __init__(self, code: str, detail: str = ""):
        self.code = code
        super().__init__(code + (":" + detail if detail else ""))


def _digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _norm_items(items):
    return tuple(str(x) for x in items)


@dataclass(frozen=True)
class IssuerDescriptorContract:
    """Issuer-controlled descriptor binding. Not request/plan supplied."""
    issuer_ref: str
    rows: Mapping[str, Mapping[str, Any]]
    contract_hash: str

    @classmethod
    def from_document(cls, document: Mapping[str, Any], *, issuer_ref: str):
        rows = document.get("operations")
        if not isinstance(rows, Mapping):
            raise B43AdmissionDenied("B43_ISSUER_CONTRACT_MALFORMED")
        declared = document.get("contract_hash")
        computed = _digest({"issuer_ref": issuer_ref, "operations": rows})
        if declared is not None and declared != computed:
            raise B43AdmissionDenied("B43_ISSUER_CONTRACT_HASH_MISMATCH")
        return cls(issuer_ref=issuer_ref, rows=rows, contract_hash=computed)

    def projection(self) -> dict:
        return {"issuer_ref": self.issuer_ref, "contract_hash": self.contract_hash,
                "operations": dict(self.rows)}


class IssuerBoundAdmission:
    def __init__(self, contract: IssuerDescriptorContract):
        self.contract = contract

    def admit(self, plan: Any) -> dict:
        specs = getattr(plan, "op_specs", None)
        if not isinstance(specs, Mapping) or not specs:
            raise B43AdmissionDenied("B43_PLAN_HAS_NO_OP_SPECS")
        releases = getattr(plan, "releases", {}) or {}
        checked = []
        for op_id in sorted(specs):
            spec = specs[op_id]
            row = self.contract.rows.get(op_id)
            if row is None:
                raise B43AdmissionDenied("B43_ADMISSION_UNREGISTERED_OPERATION", op_id)
            # 1) source edition must match the issuer-bound contract
            edition = getattr(spec, "source_edition", None)
            if edition != row.get("source_edition"):
                raise B43AdmissionDenied("B43_ADMISSION_BOUND_SOURCE_EDITION_MISMATCH", op_id)
            # 2) native item ids must match the issuer-bound contract
            items = _norm_items(getattr(spec, "native_item_ids", ()) or ())
            if items != _norm_items(row.get("native_item_ids") or ()):
                raise B43AdmissionDenied("B43_ADMISSION_BOUND_NATIVE_ITEM_IDS_MISMATCH", op_id)
            # 3) release tag must be bound BEFORE execution (no late I03 KeyError)
            tag = getattr(spec, "release_tag", None)
            if tag != row.get("release_tag"):
                raise B43AdmissionDenied("B43_ADMISSION_BOUND_RELEASE_TAG_MISMATCH", op_id)
            if tag not in releases:
                raise B43AdmissionDenied("B43_ADMISSION_UNBOUND_RELEASE_TAG", op_id)
            release = releases[tag]
            rel_edition = getattr(release, "source_edition", None)
            if rel_edition is not None and rel_edition != row.get("source_edition"):
                raise B43AdmissionDenied("B43_ADMISSION_RELEASE_EDITION_MISMATCH", op_id)
            checked.append({"op_id": op_id, "release_tag": tag, "source_edition": edition,
                            "native_item_ids": list(items)})
        return {"state": "B43_ISSUER_BOUND_ADMITTED",
                "issuer_ref": self.contract.issuer_ref,
                "contract_hash": self.contract.contract_hash,
                "checked_operations": checked,
                "checked_count": len(checked)}
