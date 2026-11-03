"""Connect persisted JOIN-E A perception/history to the S35 response boundary."""
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

from candidate import (  # noqa: E402
    TargetRuleRegistry,
    evaluate_target,
    lookup_rule,
)
from candidate.response_rules import ResponseRuleRegistry  # noqa: E402
from bridge import access, join_e_compat, occurrence_consumer  # noqa: E402
from bridge.access import S35ActorAccessRequest, S35Context  # noqa: E402

from . import s39_audit, sources  # noqa: E402

GRADE = "TEST_ONLY_SOURCEFREE_PERSONA_INPUT_NOT_NATIVE"
INPUT_SCHEMA = "SOROK_PERSONA_INPUT@1"
RESULT_SCHEMA = "SOROK_PERSONA_RESPONSE_BOUNDARY@1"


def _public_body(kind: str, body: Mapping[str, Any]) -> dict:
    if kind == "SPEECH":
        keys = ("text", "gesture", "strategy", "template_id")
    elif kind == "REPAIR":
        keys = (
            "cash_delta", "completed_delta", "hours_delta",
            "material_delta", "source_owned",
        )
    elif kind == "INSPECT":
        keys = ("changed",)
    elif kind == "ARRIVAL":
        keys = ("present_with", "public_role")
    elif kind == "REFUSAL":
        keys = ("text", "observable")
    else:
        keys = ()
    return {key: body[key] for key in keys if key in body}


def _event_public(event: Mapping[str, Any], order: int) -> dict:
    return {
        "event_id": event.get("event_id", ""),
        "kind": event.get("kind", ""),
        "clock": event.get("clock"),
        "location": event.get("location", ""),
        "summary": event.get("summary", ""),
        "body_public": _public_body(
            str(event.get("kind", "")), event.get("body") or {}
        ),
        "order": order,
    }


def _select_event(
    bundle: Mapping[str, Any], event_id: str | None
) -> tuple[dict | None, int | None, dict | None]:
    events = list(bundle.get("world_events") or [])
    perceptions = list(bundle.get("perceptions") or [])
    a_perceptions = {
        row.get("event_id"): row
        for row in perceptions
        if row.get("actor_id") == "A"
    }
    if event_id is not None:
        for order, event in enumerate(events):
            if event.get("event_id") == event_id:
                return event, order, a_perceptions.get(event_id)
        return None, None, a_perceptions.get(event_id)
    candidates = [
        (order, event)
        for order, event in enumerate(events)
        if event.get("event_id") in a_perceptions
    ]
    if not candidates:
        return (events[-1], len(events) - 1, None) if events else (None, None, None)
    order, event = candidates[-1]
    return event, order, a_perceptions.get(event.get("event_id"))


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
    event, order, perception = _select_event(bundle, event_id)
    history = bundle.get("history") or {}
    objective_present = event is not None
    perception_present = bool(include_perception and perception)
    history_present = bool(include_history and history)
    checks = {
        "occurrence_ok": True,
        "objective_event_present": objective_present,
        "event_order_present": order is not None,
        "perception_present": bool(perception),
        "perception_enabled": bool(include_perception),
        "perception_actor_a": bool(
            perception and perception.get("actor_id") == "A"
        ),
        "perception_event_matches": bool(
            perception and event
            and perception.get("event_id") == event.get("event_id")
        ),
        "perception_clock_matches_event": bool(
            perception and event
            and perception.get("clock") == event.get("clock")
        ),
        "history_present": bool(history),
        "history_enabled": bool(include_history),
        "history_hash_present": bool(history.get("history_hash")),
        "history_source_matches_actor": bool(
            history.get("source_ref")
            == (bundle.get("actor_snapshot") or {}).get("source_ref")
        ),
        "history_before_e1": bool(
            history.get("last_clock", 0) < occurrence["event_clock"]
        ),
        "history_domain_distinguished": True,
        "history_order_comparable": False,
    }
    missing = []
    if not perception_present:
        missing.append("A_LOCAL_PERCEPTION_INPUT_MISSING")
    if not history_present:
        missing.append("ACTOR_HISTORY_INPUT_MISSING")
    if perception_present and history_present:
        missing.extend(
            [
                "A_ACTION_RESPONSE_PRODUCER_MISSING",
                "PERSONA_HISTORY_RESPONSE_RULE_MISSING",
                "ISSUED_A_RESPONSE_RULE_MISSING",
            ]
        )
    record = {
        "schema": INPUT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "occurrence_ok": True,
        "occurrence": {
            "event_ref": occurrence["event_hash"],
            "event_id": occurrence["event_id"],
            "event_clock": occurrence["event_clock"],
            "branch_clock": occurrence["branch_clock"],
            "root_id": "root",
            "root_branch_hash": occurrence["root_branch_hash"],
            "branch_id": occurrence["branch_id"],
            "branch_hash": occurrence["branch_hash"],
            "branch_fork_clock": occurrence["branch_fork_clock"],
            "clock_binding_hash": occurrence["clock_binding_hash"],
        },
        "event": (
            _event_public(event, order)
            if objective_present and perception_present
            else (
                {"event_id": event.get("event_id", ""), "objective_present": True}
                if objective_present
                else None
            )
        ),
        "objective_event_present": objective_present,
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
        "history": (
            {
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
            if history_present
            else None
        ),
        "checks": checks,
        "missing_inputs": missing,
        "objective_availability_implies_perception": False,
        "history_used_for_choice": False,
        "s39_synthetic_premises_used": False,
        "selected_event_id": event.get("event_id", "") if event else "",
        "selected_event_order": order,
    }
    return record


def _persona_context(occurrence: Mapping[str, Any], event: Mapping[str, Any]):
    base = occurrence_consumer.build_context(occurrence)
    context = S35Context(
        actor_id=occurrence["actor_id"],
        event_ref=str(event.get("event_id", "")),
        event_id=str(event.get("event_id", "")),
        event_time=int(event.get("clock", 0)),
        as_of=int(occurrence["branch_clock"]),
        scene=str(event.get("location", "")),
        root_id="root",
        root_branch_hash=occurrence["root_branch_hash"],
        root_state_hash=str(occurrence["root_state_hash"]),
        branch_id=occurrence["branch_id"],
        branch_hash=occurrence["branch_hash"],
        branch_parent_id=str(occurrence["branch_parent_id"]),
        branch_fork_clock=int(occurrence["branch_fork_clock"]),
        clock=int(occurrence["branch_clock"]),
        material_eligible=base["material_eligible"],
        eligible_material_refs=base["material_refs"],
    )
    return context, base


def _hold_result(
    *,
    code: str,
    persona_input: Mapping[str, Any],
    store_before: str,
    store_after: str,
    extra: Mapping[str, Any] | None = None,
) -> dict:
    return {
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
        **(dict(extra or {})),
    }


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
    if not persona_input["objective_event_present"]:
        return _hold_result(
            code="PERSISTED_EVENT_MISSING",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
            extra={"missing_inputs": ["PERSISTED_OBJECTIVE_EVENT"]},
        )
    if not persona_input["perception"]:
        return _hold_result(
            code="A_LOCAL_PERCEPTION_INPUT_MISSING",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    if not persona_input["history"]:
        return _hold_result(
            code="ACTOR_HISTORY_INPUT_MISSING",
            persona_input=persona_input,
            store_before=store_before,
            store_after=store_after,
        )
    read = occurrence_consumer.read_occurrence(bundle)
    occurrence = read.occurrence
    event = next(
        item
        for item in bundle["world_events"]
        if item.get("event_id") == persona_input["selected_event_id"]
    )
    context, base = _persona_context(occurrence, event)
    perception_receipt = access.make_a_local_perception_receipt(
        context=context,
        source_ref="TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION_PERSISTED",
        perception_ref=persona_input["perception"]["source_ref"],
        access_status="ACCESSIBLE",
        perceived_at=int(persona_input["perception"]["clock"]),
        scene=context.scene,
        content={
            "producer": "R31J_C12_PERCEPTION_ROW",
            "event_id": persona_input["perception"]["event_id"],
            "channel": persona_input["perception"]["channel"],
            "history_hash": persona_input["history"]["history_hash"],
            "sourcefree_fixture": True,
        },
        evidence_grade=access.S35_GRADE_CONTROLLED,
        actual_actor_input=False,
        qualification=access.S35_QUALIFICATION_CONTROLLED,
    )
    perception_gate = (
        access.validate_a_local_perception(perception_receipt, context=context)
        or "OK"
    )
    rule = join_e_compat.make_rule(context.actor_id)
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=context.actor_id,
    )
    evaluation = access.evaluate_actor_access_response(
        rule_lookup=lookup,
        event_ref=context.event_ref,
        event_time=context.event_time,
        subject=context.actor_id,
        request=S35ActorAccessRequest(
            perception_receipt=perception_receipt,
            action_receipt=None,
        ),
        conditioning_readset=base["conditioning"].readset_refs,
        context=context,
        as_of=context.clock,
        material_eligible=base["material_eligible"],
        eligible_material_refs=base["material_refs"],
    )
    decision = evaluate_target(
        registry=TargetRuleRegistry.production(),
        proposal=None,
        permission=None,
        actor_id=context.actor_id,
        before_target_hash=occurrence["c9"]["target_state_hash"],
        existing_target_ids=frozenset(occurrence["c9"]["target_ids"]),
        prior_event_hash=context.event_ref,
        as_of=context.clock,
        enacted_history_refs=(),
        permitted_issuer_refs=frozenset(),
        response_hash=evaluation.response.receipt_hash,
    )
    return {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "status": "HELD",
        "outcome": evaluation.response.reason,
        "response_status": evaluation.response.status.value,
        "perception_gate": perception_gate,
        "persona_input": persona_input,
        "response_receipt_hash": evaluation.response.receipt_hash,
        "target_branch": decision.branch.value,
        "target_reason": decision.reason.value,
        "target_proposals": len(evaluation.response.target_proposals),
        "missing_inputs": list(persona_input["missing_inputs"]),
        "history_used_for_choice": False,
        "s39_synthetic_premises_used": False,
        "s39_audit": s39_audit.audit(),
        "store_hash_before": store_before,
        "store_hash_after": store_after,
        "store_mutated": store_before != store_after,
    }


__all__ = [
    "GRADE",
    "INPUT_SCHEMA",
    "RESULT_SCHEMA",
    "build_persona_input",
    "evaluate_persona_response",
]
