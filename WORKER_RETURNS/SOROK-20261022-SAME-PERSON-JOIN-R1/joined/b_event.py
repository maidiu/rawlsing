"""B's independent source occurrence for the JOIN-E upstream contrast.

The source is the existing R31J/R29M TEST_ONLY sealed observation, not a new
action law. B either performs the qualified ``SHARE_TOOL`` occurrence or seals
the same occurrence with ``performed=False`` (omission). A ``REFUSE_TOOL``
occurrence remains the existing refusal path. An absent or unqualified B record
is unavailable source, not omission and not refusal.

This module neither mints a C9 target nor edits a material-feasibility flag.
The existing R29M evaluator derives the material access from the sealed B
record, and the existing R31J producer binds that result before C8.
"""
from __future__ import annotations

from typing import Any, Mapping

from .imports import install
install()

from generative_resource import evaluate, observation, sha  # noqa: E402
from r31j.scenarios import (A, B, RESOURCE, case as r31j_case,
                            evaluated as r31j_evaluated)  # noqa: E402

SCHEMA = "SOROK_JOIN_E_B_PERFORMER_RECEIPT@1"
BINDING_SCHEMA = "SOROK_JOIN_E_B_EVENT_BINDING@1"
BINDING_KIND = "B_EVENT_BINDING"
GRADE = "TEST_ONLY_SOURCEFREE_B_EVENT_NOT_NATIVE"
B_EVENT_CONTRACT = "R31J_B_EVENT_UPSTREAM@1"
SHARE_TOOL = "SHARE_TOOL"
REFUSE_TOOL = "REFUSE_TOOL"
PERFORMED = "PERFORMED"
OMITTED = "OMITTED"
REFUSED = "REFUSED"
UNAVAILABLE = "UNAVAILABLE"
DISPOSITIONS = (PERFORMED, OMITTED, REFUSED)


class BSourceUnavailable(ValueError):
    """No qualified B source occurrence can be consumed."""

    def __init__(self, code: str = "B_SOURCE_UNAVAILABLE", detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _records(case_obj: Mapping[str, Any]) -> list[dict]:
    records = case_obj.get("records")
    if not isinstance(records, list):
        raise BSourceUnavailable("B_SOURCE_RECORDS_MISSING")
    return records


def _b_record(case_obj: Mapping[str, Any]) -> dict:
    found = [row for row in _records(case_obj)
             if row.get("kind") == "OTHER_PERFORMED"]
    if len(found) != 1:
        raise BSourceUnavailable(
            "B_SOURCE_OCCURRENCE_COUNT", str(len(found)))
    return found[0]


def _replace_b(case_obj: Mapping[str, Any], record: dict) -> dict:
    records = list(_records(case_obj))
    indexes = [index for index, row in enumerate(records)
               if row.get("kind") == "OTHER_PERFORMED"]
    if len(indexes) != 1:
        raise BSourceUnavailable(
            "B_SOURCE_OCCURRENCE_COUNT", str(len(indexes)))
    records[indexes[0]] = record
    result = dict(case_obj)
    result["records"] = records
    return result


def disposition_from_source(source: Mapping[str, Any]) -> str:
    """Read the source disposition without inventing a motive or action law."""
    operation = source.get("b_operation")
    performed = source.get("b_performed")
    if operation == REFUSE_TOOL and performed is True:
        return REFUSED
    if operation == SHARE_TOOL and performed is True:
        return PERFORMED
    if operation == SHARE_TOOL and performed is False:
        return OMITTED
    return UNAVAILABLE


def _receipt_body(case_obj: Mapping[str, Any], expected: str | None = None) -> dict:
    record = _b_record(case_obj)
    if record.get("subject") != B:
        raise BSourceUnavailable("B_SOURCE_SUBJECT_NOT_B")
    owner = record.get("owner")
    if (not isinstance(owner, str) or owner in (A, B)
            or not owner.startswith("TEST_ONLY_OWNER_")):
        raise BSourceUnavailable("B_SOURCE_OWNER_NOT_INDEPENDENT")
    ref = record.get("ref")
    event_hash = record.get("content_hash")
    if not isinstance(ref, str) or not ref.startswith("TEST_ONLY_EVENT_"):
        raise BSourceUnavailable("B_SOURCE_EVENT_REF_INVALID")
    if not isinstance(event_hash, str) or len(event_hash) != 64:
        raise BSourceUnavailable("B_SOURCE_EVENT_HASH_INVALID")
    clock = record.get("at")
    if type(clock) is not int or clock < 0:
        raise BSourceUnavailable("B_SOURCE_CLOCK_INVALID")
    payload = record.get("payload")
    if not isinstance(payload, dict):
        raise BSourceUnavailable("B_SOURCE_PAYLOAD_MISSING")
    operation = payload.get("operation")
    quantity = payload.get("quantity")
    to_actor = payload.get("to_actor")
    performed = record.get("performed")
    if type(performed) is not bool:
        raise BSourceUnavailable("B_SOURCE_PERFORMED_FLAG_INVALID")
    if to_actor != A:
        raise BSourceUnavailable("B_SOURCE_RECIPIENT_NOT_A")
    if type(quantity) is not int or quantity < 0:
        raise BSourceUnavailable("B_SOURCE_QUANTITY_INVALID")
    if operation == SHARE_TOOL:
        if quantity < 1:
            raise BSourceUnavailable("B_SOURCE_SHARE_QUANTITY_INVALID")
    elif operation == REFUSE_TOOL:
        if quantity != 0 or performed is not True:
            raise BSourceUnavailable("B_SOURCE_REFUSAL_INVALID")
    else:
        raise BSourceUnavailable("B_SOURCE_OPERATION_INVALID", str(operation))
    disposition = disposition_from_source({
        "b_operation": operation,
        "b_performed": performed,
    })
    if disposition == UNAVAILABLE:
        raise BSourceUnavailable("B_SOURCE_DISPOSITION_INVALID")
    if expected is not None and disposition != expected:
        raise BSourceUnavailable(
            "B_SOURCE_DISPOSITION_MISMATCH",
            f"{disposition}!={expected}")
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "psychology_claim": False,
        "actor": record["subject"],
        "owner": owner,
        "event_ref": ref,
        "event_hash": event_hash,
        "clock": clock,
        "operation": operation,
        "quantity": quantity,
        "to_actor": to_actor,
        "performed": performed,
        "disposition": disposition,
        "source_available": True,
        "as_of": case_obj.get("as_of"),
    }
    body["receipt_hash"] = sha(body)
    return body


def receipt_for_case(case_obj: Mapping[str, Any],
                     expected: str | None = None) -> dict:
    """Public performer-receipt derivation used by actor-limit checks."""
    return _receipt_body(case_obj, expected)


def binding_from_receipt(receipt: Mapping[str, Any],
                         source: Mapping[str, Any]) -> dict:
    """Persisted C12 binding that makes the receipt requirement non-optional."""
    check = validate_receipt(receipt, source)
    if not check.get("ok"):
        raise BSourceUnavailable(
            "B_SOURCE_RECEIPT_MISMATCH",
            ",".join(name for name, ok in check.get("checks", {}).items()
                     if not ok))
    disposition = disposition_from_source(source)
    if disposition != PERFORMED:
        raise BSourceUnavailable("B_SOURCE_BINDING_NOT_PERFORMED", disposition)
    return {
        "schema": BINDING_SCHEMA,
        "b_event_contract": B_EVENT_CONTRACT,
        "b_event_ref": source.get("b_event_ref"),
        "b_event_hash": source.get("b_event_hash"),
        "b_performer_receipt_hash": receipt.get("receipt_hash"),
        "j_b_disposition": disposition,
        "native": False,
        "psychology_claim": False,
    }


def persisted_binding(product, branch_id: str) -> dict | None:
    """Read the append-only C12 binding; absence means genuine legacy session."""
    rows = [row for row in product.store.episodes(branch_id)
            if row.get("kind") == BINDING_KIND]
    if not rows:
        return None
    if len(rows) != 1:
        raise BSourceUnavailable("B_EVENT_BINDING_COUNT", str(len(rows)))
    body = rows[0].get("body") or {}
    if (body.get("schema") != BINDING_SCHEMA
            or body.get("b_event_contract") != B_EVENT_CONTRACT):
        raise BSourceUnavailable("B_EVENT_BINDING_INVALID")
    return body


def validate_binding(meta: Mapping[str, Any], persisted: Mapping[str, Any] | None,
                     source: Mapping[str, Any]) -> dict:
    """Require the receipt whenever persisted C12 evidence marks a new session."""
    required = bool(
        persisted is not None
        or meta.get("b_event_contract") == B_EVENT_CONTRACT
        or meta.get("b_performer_receipt"))
    checks: dict[str, bool] = {}
    observed: dict = {"required": required}
    if not required:
        return {"ok": True, "required": False, "checks": checks,
                "observed": observed}
    receipt = meta.get("b_performer_receipt")
    receipt_check = validate_receipt(receipt, source)
    checks.update({
        "meta_contract_present": meta.get("b_event_contract") == B_EVENT_CONTRACT,
        "meta_disposition_performed": meta.get("j_b_disposition") == PERFORMED,
        "receipt_present": isinstance(receipt, Mapping),
        "receipt_matches_source": receipt_check.get("ok") is True,
        "source_is_performed": source.get("b_performed") is True,
    })
    if persisted is not None:
        checks.update({
            "persisted_contract_present": (
                persisted.get("b_event_contract") == B_EVENT_CONTRACT),
            "persisted_event_ref_matches": (
                persisted.get("b_event_ref") == source.get("b_event_ref")),
            "persisted_event_hash_matches": (
                persisted.get("b_event_hash") == source.get("b_event_hash")),
            "persisted_receipt_hash_matches": (
                isinstance(receipt, Mapping)
                and persisted.get("b_performer_receipt_hash")
                == receipt.get("receipt_hash")),
            "persisted_disposition_matches": (
                persisted.get("j_b_disposition") == PERFORMED),
        })
        observed.update({
            "persisted_event_hash": persisted.get("b_event_hash"),
            "persisted_receipt_hash": persisted.get("b_performer_receipt_hash"),
        })
    observed.update(receipt_check.get("observed", {}))
    return {"ok": all(checks.values()), "required": True, "checks": checks,
            "observed": observed}


def _with_receipt(scenario: Mapping[str, Any], expected: str) -> dict:
    result = dict(scenario)
    result["b_performer_receipt"] = _receipt_body(result["case"], expected)
    result["b_disposition"] = expected
    return result


def performed_scenario(*, e2: bool = False) -> dict:
    """B performs the qualified SHARE_TOOL source occurrence."""
    scenario = _with_receipt(
        r31j_evaluated(share=True, e2=e2), PERFORMED)
    if scenario["gm01"].get("material_feasible_after") is not True:
        raise BSourceUnavailable("B_PERFORMED_SOURCE_NOT_FEASIBLE")
    return scenario


def omitted_scenario(*, e2: bool = False) -> dict:
    """B seals the qualified SHARE_TOOL occurrence without performing it."""
    if e2:
        raise BSourceUnavailable("B_OMISSION_HAS_NO_E2")
    record = observation(
        "OTHER_PERFORMED", B, "TEST_ONLY_OWNER_omit", 5,
        ref="TEST_ONLY_EVENT_omit", performed=False,
        operation=SHARE_TOOL, to_actor=A, quantity=1)
    case_obj = _replace_b(r31j_case(share=True, e2=False), record)
    gm01 = evaluate(case_obj, RESOURCE)
    if gm01.get("material_feasible_after") is not False:
        raise BSourceUnavailable("B_OMISSION_MATERIAL_STILL_FEASIBLE")
    scenario = {
        "case": case_obj,
        "gm01": gm01,
        "resource_hash": RESOURCE["content_hash"],
    }
    return _with_receipt(scenario, OMITTED)


def refused_scenario(*, e2: bool = False) -> dict:
    """Preserve B's existing qualified REFUSE_TOOL / NO_CHANGE source."""
    if e2:
        raise BSourceUnavailable("B_REFUSAL_HAS_NO_E2")
    scenario = _with_receipt(
        r31j_evaluated(share=False, e2=False), REFUSED)
    if scenario["gm01"].get("material_feasible_after") is not False:
        raise BSourceUnavailable("B_REFUSAL_MATERIAL_STILL_FEASIBLE")
    return scenario


def scenario_for(disposition: str, *, e2: bool = False) -> dict:
    if disposition == PERFORMED:
        return performed_scenario(e2=e2)
    if disposition == OMITTED:
        return omitted_scenario(e2=e2)
    if disposition == REFUSED:
        return refused_scenario(e2=e2)
    if disposition == UNAVAILABLE:
        raise BSourceUnavailable("B_SOURCE_OCCURRENCE_ABSENT")
    raise BSourceUnavailable("B_SOURCE_DISPOSITION_UNKNOWN", str(disposition))


def unavailable_scenario(*, e2: bool = False) -> dict:
    """Refuse absent B source; never turn it into omission or refusal."""
    base = r31j_case(share=True, e2=e2)
    without_b = dict(base)
    without_b["records"] = [row for row in _records(base)
                            if row.get("kind") != "OTHER_PERFORMED"]
    if any(row.get("kind") == "OTHER_PERFORMED"
           for row in without_b["records"]):
        raise BSourceUnavailable("B_SOURCE_CUT_INVALID")
    raise BSourceUnavailable("B_SOURCE_OCCURRENCE_ABSENT")


def validate_receipt(receipt: Any, source: Mapping[str, Any]) -> dict:
    """Compare a performer receipt with the actual C8/C12 source fields."""
    checks: dict[str, bool] = {}
    observed: dict = {"source_disposition": disposition_from_source(source)}
    try:
        if not isinstance(receipt, Mapping):
            raise BSourceUnavailable("B_SOURCE_RECEIPT_MISSING")
        body = dict(receipt)
        recorded_hash = body.pop("receipt_hash", "")
        expected_disposition = disposition_from_source(source)
        checks.update({
            "receipt_hash_valid": recorded_hash == sha(body),
            "receipt_schema": receipt.get("schema") == SCHEMA,
            "receipt_grade": receipt.get("grade") == GRADE,
            "native_false": receipt.get("native") is False,
            "psychology_false": receipt.get("psychology_claim") is False,
            "event_ref_matches": receipt.get("event_ref") == source.get("b_event_ref"),
            "event_hash_matches": receipt.get("event_hash") == source.get("b_event_hash"),
            "actor_matches": receipt.get("actor") == source.get("b_actor"),
            "owner_matches": receipt.get("owner") == source.get("b_owner"),
            "clock_matches": receipt.get("clock") == source.get("b_clock"),
            "operation_matches": receipt.get("operation") == source.get("b_operation"),
            "quantity_matches": receipt.get("quantity") == source.get("b_quantity"),
            "recipient_matches": receipt.get("to_actor") == source.get("b_to_actor"),
            "performed_matches": receipt.get("performed") is source.get("b_performed"),
            "disposition_matches": receipt.get("disposition") == expected_disposition,
            "source_available": receipt.get("source_available") is True,
        })
        observed.update({
            "receipt_disposition": receipt.get("disposition"),
            "source_operation": source.get("b_operation"),
            "source_performed": source.get("b_performed"),
            "event_hash": source.get("b_event_hash"),
        })
    except Exception as exc:  # unreadable receipt is a failed provenance check
        checks["receipt_readable"] = False
        observed["error"] = type(exc).__name__ + ":" + str(exc)
    checks.setdefault("receipt_readable", True)
    return {"ok": all(checks.values()), "checks": checks, "observed": observed}


__all__ = [
    "A", "B", "BINDING_KIND", "BINDING_SCHEMA", "B_EVENT_CONTRACT",
    "BSourceUnavailable", "DISPOSITIONS", "GRADE", "OMITTED", "PERFORMED",
    "REFUSED", "SCHEMA", "UNAVAILABLE", "binding_from_receipt",
    "disposition_from_source", "omitted_scenario", "performed_scenario",
    "persisted_binding", "receipt_for_case", "refused_scenario",
    "scenario_for", "unavailable_scenario", "validate_binding",
    "validate_receipt",
]
