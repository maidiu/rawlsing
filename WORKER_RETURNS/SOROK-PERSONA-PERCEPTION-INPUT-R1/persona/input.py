"""Exact-E1 persona perception/history input for the S35 boundary.

The adapter keeps the JOIN-E E1 actor event as the only response event. A C12
perception of any other event is evidence of a different event, never an E1
perception receipt. When the exact E1 provenance is absent the result is a
typed hold produced by the normal S35 occurrence boundary.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S35_RETURN = REPO / "WORKER_RETURNS" / "SOROK-S35-C9R-ACCESS-R1"
if str(S35_RETURN) not in sys.path:
    sys.path.insert(0, str(S35_RETURN))
import install as s35_install  # noqa: E402

s35_install.install()

from bridge import occurrence_consumer  # noqa: E402

from . import s39_audit, sources  # noqa: E402

GRADE = "TEST_ONLY_SOURCEFREE_PERSONA_INPUT_NOT_NATIVE"
INPUT_SCHEMA = "SOROK_PERSONA_INPUT@1"
RESULT_SCHEMA = "SOROK_PERSONA_RESPONSE_BOUNDARY@1"
ALWAYS_MISSING = (
    "A_ACTION_OR_OMISSION_RECEIPT_BOUND_TO_E1_CLOCK_AND_ORDER",
    "QUALIFIED_A_SOURCE_OWNER_RECEIPT",
    "A_RESPONSE_RULE_ISSUED",
)


def _exact_e1_perception(
    bundle: Mapping[str, Any], e1_event_id: str, e1_event_clock: int
) -> tuple[dict | None, list[dict], list[dict]]:
    a_rows = [
        dict(row)
        for row in (bundle.get("perceptions") or [])
        if row.get("actor_id") == "A"
    ]
    exact = [row for row in a_rows if row.get("event_id") == e1_event_id]
    matching = [
        row for row in exact if row.get("clock") == e1_event_clock
    ]
    return (matching[0] if matching else None, exact, a_rows)


def _history_public(history: Mapping[str, Any]) -> dict:
    return {
        "source_ref": history.get("source_ref", ""),
        "source_hash": history.get("source_hash", ""),
        "history_hash": history.get("history_hash", ""),
        "event_head": history.get("event_head", ""),
        "event_count": history.get("event_count", 0),
        "last_clock": history.get("last_clock", 0),
        "performed_action_refs": list(
            history.get("performed_action_refs", [])
        ),
        "objective_refs": list(history.get("objective_refs", [])),
        "domain": history.get("domain", "BP1_ACTOR_HISTORY"),
    }


def build_persona_input(
    bundle: Mapping[str, Any],
    *,
    event_id: str | None = None,
    include_perception: bool = True,
    include_history: bool = True,
) -> dict:
    read = occurrence_consumer.read_occurrence(bundle)
    if not read.ok:
        return {
            "schema": INPUT_SCHEMA,
            "grade": GRADE,
            "native": False,
            "occurrence_ok": False,
            "missing_contract": read.missing_contract,
            "checks": dict(read.checks),
            "missing_inputs": ["S35_PERSISTED_OCCURRENCE_BINDING"],
        }
    occurrence = read.occurrence
    e1_event_id = str(occurrence["event_id"])
    e1_event_clock = int(occurrence["event_clock"])
    requested_event_id = event_id or e1_event_id
    identity_ok = requested_event_id == e1_event_id
    perception, exact_rows, a_rows = _exact_e1_perception(
        bundle, e1_event_id, e1_event_clock
    )
    clock_mismatch = bool(exact_rows) and perception is None
    perception_present = bool(include_perception and perception)
    history = bundle.get("history") or {}
    history_present = bool(include_history and history)
    other_ids = sorted(
        {
            str(row.get("event_id", ""))
            for row in a_rows
            if row.get("event_id") != e1_event_id
        }
    )
    checks = {
        "occurrence_ok": True,
        "event_identity_ok": identity_ok,
        "requested_event_is_e1": identity_ok,
        "objective_e1_present": True,
        "perception_present": bool(perception),
        "perception_enabled": bool(include_perception),
        "perception_actor_a": bool(
            perception and perception.get("actor_id") == "A"
        ),
        "perception_event_matches_e1": bool(
            perception and perception.get("event_id") == e1_event_id
        ),
        "perception_clock_matches_e1": bool(
            perception and perception.get("clock") == e1_event_clock
        ),
        "perception_substitution": False,
        "other_event_perceptions_ignored": bool(other_ids),
        "history_present": bool(history),
        "history_enabled": bool(include_history),
        "history_hash_present": bool(history.get("history_hash")),
        "history_source_matches_actor": bool(
            history.get("source_ref")
            == (bundle.get("actor_snapshot") or {}).get("source_ref")
        ),
        "history_before_e1": bool(
            history.get("last_clock", 0) < e1_event_clock
        ),
        "history_domain_distinguished": True,
        "history_order_comparable": False,
    }
    missing: list[str] = []
    if not identity_ok:
        missing.append("PERCEPTION_EVENT_IDENTITY_MISMATCH")
    if not perception_present:
        missing.extend(
            [
                "A_LOCAL_OBSERVATION_RECEIPT_OF_E1",
                "A_LOCAL_OBSERVATION_OF_E1",
            ]
        )
    if clock_mismatch:
        missing.append("A_LOCAL_PERCEPTION_CLOCK_MISMATCH")
    if not history_present:
        missing.append("ACTOR_HISTORY_INPUT_MISSING")
    if perception_present:
        missing.append("QUALIFIED_A_PERCEPTION_RECEIPT")
    missing.extend(ALWAYS_MISSING)
    return {
        "schema": INPUT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "occurrence_ok": True,
        "occurrence": {
            "event_ref": occurrence["event_hash"],
            "event_id": e1_event_id,
            "event_clock": e1_event_clock,
            "branch_clock": occurrence["branch_clock"],
            "root_id": "root",
            "root_branch_hash": occurrence["root_branch_hash"],
            "branch_id": occurrence["branch_id"],
            "branch_hash": occurrence["branch_hash"],
            "branch_fork_clock": occurrence["branch_fork_clock"],
            "clock_binding_hash": occurrence["clock_binding_hash"],
        },
        "requested_event_id": requested_event_id,
        "selected_event_id": e1_event_id,
        "event": (
            {
                "event_id": e1_event_id,
                "event_clock": e1_event_clock,
                "scene": occurrence["scene"],
            }
            if perception_present
            else {"event_id": e1_event_id, "objective_present": True}
        ),
        "objective_event_present": True,
        "perception": (
            {
                "actor_id": "A",
                "event_id": perception.get("event_id", ""),
                "clock": perception.get("clock"),
                "channel": perception.get("channel", ""),
                "source_ref": "TEST_ONLY_R31J_A_PERCEPTION_"
                + str(perception.get("event_id", "")),
            }
            if perception_present
            else None
        ),
        "history": _history_public(history) if history_present else None,
        "c12_a_perception_count": len(a_rows),
        "c12_other_event_perception_event_ids": other_ids,
        "c12_perceptions_are_not_e1_receipts": True,
        "checks": checks,
        "missing_inputs": missing,
        "objective_availability_implies_perception": False,
        "history_used_for_choice": False,
        "s39_synthetic_premises_used": False,
    }


def _hold_result(
    *,
    code: str,
    persona_input: Mapping[str, Any],
    store_before: str,
    store_after: str,
    s35: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict:
    result = {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "status": "HELD",
        "outcome": code,
        "persona_input": persona_input,
        "target_branch": "NO_CHANGE",
        "target_reason": "NO_PROPOSAL",
        "target_proposals": 0,
        "missing_inputs": list(persona_input.get("missing_inputs", [])),
        "history_used_for_choice": False,
        "s39_synthetic_premises_used": False,
        "store_hash_before": store_before,
        "store_hash_after": store_after,
        "store_mutated": store_before != store_after,
    }
    if s35 is not None:
        result["s35"] = dict(s35)
        for key in (
            "response_status",
            "perception_gate",
            "action_gate",
            "event_ref",
            "event_id",
            "event_clock",
            "branch_clock",
            "clock_binding_hash",
            "s35_receipt_hash",
            "target_branch",
            "target_reason",
            "target_proposals",
            "actual_actor_input",
            "qualification",
            "hold_reason",
        ):
            if key in s35:
                result[key] = s35[key]
    result.update(dict(extra or {}))
    return result


def evaluate_persona_response(
    bundle: Mapping[str, Any],
    *,
    event_id: str | None = None,
    include_perception: bool = True,
    include_history: bool = True,
) -> dict:
    store_before = sources.store_hash(bundle)
    persona_input = build_persona_input(
        bundle,
        event_id=event_id,
        include_perception=include_perception,
        include_history=include_history,
    )
    store_after = sources.store_hash(bundle)
    if not persona_input.get("occurrence_ok"):
        return _hold_result(
            code="S35_PERSISTED_OCCURRENCE_BINDING_HOLD",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    if not persona_input["checks"]["event_identity_ok"]:
        return _hold_result(
            code="PERCEPTION_EVENT_IDENTITY_MISMATCH",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    read = occurrence_consumer.read_occurrence(bundle)
    occurrence = read.occurrence
    if not persona_input["perception"]:
        s35 = occurrence_consumer.summary(
            occurrence_consumer.evaluate_occurrence(
                occurrence,
                controlled=False,
                perception_receipt=None,
                action_receipt=None,
            )
        )
        return _hold_result(
            code=s35["outcome"],
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
            s35=s35,
        )
    if not persona_input["history"]:
        return _hold_result(
            code="ACTOR_HISTORY_INPUT_MISSING",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    perception_receipt = bundle.get("perception_receipt")
    if perception_receipt is None:
        return _hold_result(
            code="QUALIFIED_E1_PERCEPTION_RECEIPT_MISSING",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    s35 = occurrence_consumer.summary(
        occurrence_consumer.evaluate_occurrence(
            occurrence,
            controlled=False,
            perception_receipt=perception_receipt,
            action_receipt=bundle.get("action_receipt"),
        )
    )
    return _hold_result(
        code=s35["outcome"],
        persona_input=persona_input,
        store_before=store_before,
        store_after=store_after,
        s35=s35,
        extra={"s39_audit": s39_audit.audit()},
    )


__all__ = [
    "GRADE",
    "INPUT_SCHEMA",
    "RESULT_SCHEMA",
    "build_persona_input",
    "evaluate_persona_response",
]
