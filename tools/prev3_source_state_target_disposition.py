"""Source-agnostic PRE-V3 empirical source-state disposition contract."""

from __future__ import annotations

from copy import deepcopy

RAW_SOURCE_STATE = "RAW_SOURCE_STATE"
SOURCE_LOCAL_GOVERNED_STATE = "SOURCE_LOCAL_GOVERNED_STATE"
PRODUCT_TARGET_DISPOSITION = "PRODUCT_TARGET_DISPOSITION"
DENOMINATOR_RESOLUTION_CHECK = "DENOMINATOR_RESOLUTION_CHECK"
EMPIRICAL_RESULT = "EMPIRICAL_RESULT"

NUMERATOR_AND_DENOMINATOR = "NUMERATOR_AND_DENOMINATOR"
DENOMINATOR_ONLY = "DENOMINATOR_ONLY"
EXCLUDED_FROM_TARGET_DENOMINATOR = "EXCLUDED_FROM_TARGET_DENOMINATOR"
UNRESOLVED = "UNRESOLVED"

_ALLOWED_DISPOSITIONS = {
    NUMERATOR_AND_DENOMINATOR,
    DENOMINATOR_ONLY,
    EXCLUDED_FROM_TARGET_DENOMINATOR,
    UNRESOLVED,
}


class ContractError(ValueError):
    """Raised when a contract stage is absent, invalid, or not yet resolved."""


def _require_nonempty_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field_name} must be non-empty text")
    return value


def audit_record(record):
    """Validate one record and return its independently auditable stage trail."""
    if not isinstance(record, dict):
        raise ContractError("record must be a mapping")

    record_id = _require_nonempty_text(record.get("record_id"), "record_id")
    raw = record.get("raw_source_state")
    governed = record.get("source_local_governed_state")
    disposition = record.get("product_target_disposition")

    if not isinstance(raw, dict):
        raise ContractError(f"{record_id}: raw_source_state must be a mapping")
    source_id = _require_nonempty_text(raw.get("source_id"), f"{record_id}.source_id")
    if "native_state" not in raw:
        raise ContractError(f"{record_id}: native_state is required")

    if not isinstance(governed, dict):
        raise ContractError(
            f"{record_id}: source_local_governed_state must be a mapping"
        )
    authority_id = _require_nonempty_text(
        governed.get("authority_id"), f"{record_id}.authority_id"
    )
    semantic_state = _require_nonempty_text(
        governed.get("semantic_state"), f"{record_id}.semantic_state"
    )

    if disposition not in _ALLOWED_DISPOSITIONS:
        raise ContractError(f"{record_id}: unsupported product_target_disposition")

    return {
        "record_id": record_id,
        "source_id": source_id,
        "audit_trail": [
            {
                "stage": RAW_SOURCE_STATE,
                "value": deepcopy(raw),
            },
            {
                "stage": SOURCE_LOCAL_GOVERNED_STATE,
                "value": {
                    "authority_id": authority_id,
                    "semantic_state": semantic_state,
                },
            },
            {
                "stage": PRODUCT_TARGET_DISPOSITION,
                "value": disposition,
            },
        ],
    }


def denominator_resolution_check(payload):
    """Validate the concrete objective target and report whether its gate passes."""
    if not isinstance(payload, dict):
        raise ContractError("payload must be a mapping")
    target_id = _require_nonempty_text(payload.get("target_id"), "target_id")
    if payload.get("world_scope") != "OBJECTIVE":
        raise ContractError("world_scope must be OBJECTIVE")
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise ContractError("records must be a non-empty list")

    audited = [audit_record(record) for record in records]
    unresolved_record_ids = [
        item["record_id"]
        for item in audited
        if item["audit_trail"][2]["value"] == UNRESOLVED
    ]
    return {
        "stage": DENOMINATOR_RESOLUTION_CHECK,
        "target_id": target_id,
        "passed": not unresolved_record_ids,
        "unresolved_record_ids": unresolved_record_ids,
        "audited_records": audited,
    }


def emit_empirical_result(payload):
    """Emit empirical counts only after the denominator-resolution gate passes."""
    gate = denominator_resolution_check(payload)
    if not gate["passed"]:
        unresolved = ", ".join(gate["unresolved_record_ids"])
        raise ContractError(
            "empirical result forbidden while target disposition is unresolved: "
            + unresolved
        )

    dispositions = [
        item["audit_trail"][2]["value"] for item in gate["audited_records"]
    ]
    numerator = sum(value == NUMERATOR_AND_DENOMINATOR for value in dispositions)
    denominator = sum(
        value in {NUMERATOR_AND_DENOMINATOR, DENOMINATOR_ONLY}
        for value in dispositions
    )
    excluded = sum(
        value == EXCLUDED_FROM_TARGET_DENOMINATOR for value in dispositions
    )
    value = None if denominator == 0 else numerator / denominator

    return {
        "stage": EMPIRICAL_RESULT,
        "target_id": gate["target_id"],
        "denominator_resolution_check": {
            "stage": gate["stage"],
            "passed": gate["passed"],
            "unresolved_record_ids": gate["unresolved_record_ids"],
        },
        "numerator": numerator,
        "denominator": denominator,
        "excluded": excluded,
        "value": value,
        "audited_records": gate["audited_records"],
    }
