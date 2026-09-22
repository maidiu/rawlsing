"""FIABC-T6 live wrapper for the generic R35 physical guard.

This module is intentionally separate from I05/I08.  It verifies R35-I03
whole-source physical-equivalence receipts for the two current P2 sources using
their accepted S35 edge-class declarations.  A physical PASS never upgrades,
creates, or repairs semantic parity or source certification.
"""
from __future__ import annotations

from typing import Any, Mapping

from rawlsing_next.fiabc_whole_source_physical_equivalence import (
    PASS_STATUS,
    PhysicalEquivalenceError,
    canonical_digest,
    verify_candidate_physical_equivalence,
    verify_canonical_expectation,
)

LIVE_GUARD_SCHEMA = "FIABC_T6_LIVE_R35_PHYSICAL_GUARD_INPUT@1.0.0"
LIVE_GUARD_RECEIPT_SCHEMA = "FIABC_T6_LIVE_R35_PHYSICAL_GUARD_RECEIPT@1.0.0"
LIVE_GUARD_PASS = "FIABC_T6_CURRENT_TWO_SOURCE_PHYSICAL_GUARD_PASS__NOT_P2_SEMANTIC_OR_CERTIFICATION_PASS"

CURRENT_SOURCE_SHA = {
    "LITS_I": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
    "WVS7": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
}
CURRENT_EDGE_CLASSES = {
    "LITS_I": ("EC01","EC02","EC05","EC06","EC09","EC12"),
    "WVS7": ("EC01","EC05","EC07","EC09","EC10","EC12","EC13"),
}
CURRENT_CANDIDATES = ("A","B","C")


class LiveR35GuardError(RuntimeError):
    pass


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveR35GuardError(f"{label} must be a mapping")
    return value


def verify_live_source_physical_guard(
    source_id: str,
    *,
    expectation: Mapping[str, Any],
    realizations: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if source_id not in CURRENT_SOURCE_SHA:
        raise LiveR35GuardError(f"source {source_id!r} is not in the current P2 court")
    try:
        expectation_identity=verify_canonical_expectation(expectation)
    except PhysicalEquivalenceError as exc:
        raise LiveR35GuardError(f"{source_id} canonical physical expectation invalid") from exc
    source=_mapping(expectation.get("source_identity"),"expectation.source_identity")
    if source.get("sha256") != CURRENT_SOURCE_SHA[source_id]:
        raise LiveR35GuardError(f"{source_id} canonical source SHA drift")
    scope=_mapping(expectation.get("scope"),"expectation.scope")
    if tuple(scope.get("applicable_edge_classes") or ()) != CURRENT_EDGE_CLASSES[source_id]:
        raise LiveR35GuardError(f"{source_id} S35 edge-class declaration drift")
    if set(realizations) != set(CURRENT_CANDIDATES):
        raise LiveR35GuardError(f"{source_id} physical guard requires exactly A/B/C")
    receipts={}
    for candidate in CURRENT_CANDIDATES:
        try:
            receipt=verify_candidate_physical_equivalence(expectation,realizations[candidate])
        except PhysicalEquivalenceError as exc:
            raise LiveR35GuardError(
                f"{source_id}/{candidate} whole-source physical equivalence failed"
            ) from exc
        if receipt.get("status") != PASS_STATUS:
            raise LiveR35GuardError(f"{source_id}/{candidate} physical receipt is not PASS")
        if receipt.get("expectation_identity") != expectation_identity:
            raise LiveR35GuardError(f"{source_id}/{candidate} expectation identity drift")
        if receipt.get("semantic_parity_claimed") is not False:
            raise LiveR35GuardError("physical receipt attempted semantic promotion")
        if receipt.get("source_certification_claimed") is not False:
            raise LiveR35GuardError("physical receipt attempted source certification")
        receipts[candidate]=receipt
    return {
        "source_id":source_id,
        "canonical_source_sha256":CURRENT_SOURCE_SHA[source_id],
        "applicable_edge_classes":CURRENT_EDGE_CLASSES[source_id],
        "expectation_identity":expectation_identity,
        "candidate_receipts":receipts,
        "physical_status":PASS_STATUS,
        "semantic_parity":"NOT_ADJUDICATED_BY_T6_R35_PHYSICAL_GUARD",
        "source_certification":"NOT_ADJUDICATED_BY_T6_R35_PHYSICAL_GUARD",
        "population_weight_authority":"NOT_ADJUDICATED_BY_T6_R35_PHYSICAL_GUARD",
    }


def verify_live_two_source_physical_guard(document: Mapping[str, Any]) -> dict[str, Any]:
    doc=_mapping(document,"T6 physical guard document")
    if doc.get("schema") != LIVE_GUARD_SCHEMA:
        raise LiveR35GuardError("T6 physical guard schema drift")
    sources=_mapping(doc.get("sources"),"T6 physical guard sources")
    if set(sources) != set(CURRENT_SOURCE_SHA):
        raise LiveR35GuardError("T6 physical guard requires exactly LiTS-I and WVS7")
    receipts={}
    for source_id in ("LITS_I","WVS7"):
        row=_mapping(sources[source_id],f"sources.{source_id}")
        receipts[source_id]=verify_live_source_physical_guard(
            source_id,
            expectation=_mapping(row.get("expectation"),f"{source_id}.expectation"),
            realizations=_mapping(row.get("realizations"),f"{source_id}.realizations"),
        )
    body={
        "schema":LIVE_GUARD_RECEIPT_SCHEMA,
        "status":LIVE_GUARD_PASS,
        "sources":receipts,
        "i05_semantic_parity_owner":"UNCHANGED__PRE553_INDEPENDENT_PARITY_ORACLE",
        "i08_p2_semantic_terminal_owner":"UNCHANGED__FIABC_P2_FINAL_TERMINAL_VERIFIER",
        "physical_equivalence_upgrades_semantic_failure":False,
        "semantic_pass_manufactures_physical_pass":False,
        "whole_source_certification_claimed":False,
        "closed_35_universality_claimed":False,
        "capability_105_cells_claimed":False,
    }
    body["receipt_identity"]=canonical_digest(body)
    return body


__all__=[
    "CURRENT_CANDIDATES","CURRENT_EDGE_CLASSES","CURRENT_SOURCE_SHA",
    "LIVE_GUARD_PASS","LIVE_GUARD_RECEIPT_SCHEMA","LIVE_GUARD_SCHEMA",
    "LiveR35GuardError","verify_live_source_physical_guard",
    "verify_live_two_source_physical_guard",
]
