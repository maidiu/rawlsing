"""Sourcefree parent decision and performed-action admission.

The parent is the C01 stable supporting actor. This module turns its actual
C02 material/obligations and the actual B03/B04 household/market facts into an
explicit, reproducible decision. It does not use an LLM, a fixture-supplied
answer, Nadia's state, or a new owner/scheduler/ledger. The decision rule is an
explicit sourcefree hypothesis, not native parent psychology.
"""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Mapping

from .contracts import RecursionRefusal, canonical, detached, digest
from .parent_activity import (
    PARENT_GRADE, _parent_write_lock, _read_material, _StoreWrite,
    parent_feasible_actions, read_parent_history,
)

PARENT_REQUEST_SCHEMA = "SOROK_PARENT_REQUEST@1"
PARENT_PROPOSAL_SCHEMA = "SOROK_PARENT_DECISION_PROPOSAL@1"
PARENT_PROSPECTIVE_READ_SCHEMA = "SOROK_PARENT_MATERIAL_PROSPECTIVES@1"
PARENT_DECISION_SCHEMA = "SOROK_PARENT_DECISION@1"
PARENT_DECISION_RECEIPT_SCHEMA = "SOROK_PARENT_DECISION_RECEIPT@1"
PARENT_ACTION_RECEIPT_SCHEMA = "SOROK_PARENT_ACTION_RECEIPT@1"
PARENT_DECISION_KIND = "P2_PARENT_DECISION"
PARENT_ACTION_KIND = "P2_PARENT_ACTION"
DECISION_RULE_ID = "SOROK_SOURCEFREE_PARENT_OBLIGATION_PURCHASE"
DECISION_RULE_VERSION = 1
DECISION_GRADE = "SOURCEFREE_S2_ONLY"
REQUEST_FIELDS = frozenset({
    "schema", "grade", "request_id", "objective_request", "owner_actor_id",
})
ACTION_PURCHASE = "PURCHASE"
ACTION_DECLINE = "DECLINE"
ACTION_HOLD = "HOLD"
DECISION_RULE = {
    "rule_id": DECISION_RULE_ID,
    "version": DECISION_RULE_VERSION,
    "grade": DECISION_GRADE,
    "native_science": False,
    "premises": [
        "request currency matches the parent material currency and the market currency",
        "B03 material constraints other than household affordability hold",
        "market stock exists and price/kind match the request",
        "parent cash and free hours cover the purchase",
        "after purchase, parent cash is not below debt_units and free hours are not below care_hours_due",
        "owner_actor_id is the registered parent or the focal household holder",
        "the B02 current period is qualified",
    ],
    "selection": "PURCHASE when every premise holds; DECLINE for a refused material premise; HOLD for a missing/unknown premise",
    "child_outcome": "NOT_READ",
    "nadia_state": "NOT_READ",
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hash_text(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _b04_module():
    path = (Path(__file__).resolve().parents[2] / "SOROK-DUEL-B04-R1")
    if path.is_dir() and str(path) not in sys.path:
        sys.path.insert(0, str(path))
    try:
        import material_operations
        return material_operations
    except ImportError:
        return None


def _house_module():
    path = (Path(__file__).resolve().parents[2] / "SOROK-P6-ONE-LIVING-HOUSE-R1")
    if path.is_dir() and str(path) not in sys.path:
        sys.path.insert(0, str(path))
    try:
        import house
        return house
    except ImportError:
        return None


def parent_request_fixture(*, kind: str = "junior", owner_actor_id: str) -> dict:
    house = _house_module()
    if house is None or kind not in house.DRUM_KIT_REQUESTS:
        raise RecursionRefusal("PARENT_REQUEST_SCHEMA")
    return {
        "schema": PARENT_REQUEST_SCHEMA,
        "grade": PARENT_GRADE,
        "request_id": "parent-request:" + kind,
        "objective_request": detached(house.DRUM_KIT_REQUESTS[kind]),
        "owner_actor_id": owner_actor_id,
    }


def _validate_request(session, request: Any) -> dict:
    if not isinstance(request, Mapping) or set(request) != REQUEST_FIELDS:
        raise RecursionRefusal("PARENT_REQUEST_SCHEMA")
    value = detached(request)
    house = _house_module()
    objective = value.get("objective_request")
    if (value.get("schema") != PARENT_REQUEST_SCHEMA
            or value.get("grade") != PARENT_GRADE
            or not _text(value.get("request_id"))
            or not _text(value.get("owner_actor_id"))
            or not isinstance(objective, Mapping)):
        raise RecursionRefusal("PARENT_REQUEST_SCHEMA")
    if house is None:
        raise RecursionRefusal("PARENT_REQUEST_HOUSE_UNAVAILABLE")
    # B03 owns the concrete request validation; this call also validates the
    # request schema/price/currency when the decision reads material feasibility.
    try:
        house.material_feasibility(session, objective)
    except RecursionRefusal as exc:
        raise RecursionRefusal("PARENT_REQUEST_OBJECTIVE_INVALID") from exc
    return value


def _market_and_owned(session):
    b04 = _b04_module()
    if b04 is None:
        raise RecursionRefusal("PARENT_DECISION_MARKET_UNAVAILABLE")
    return b04, b04.read_market_inventory(session), b04.read_owned_objects(session)


def _evaluate_purchase(session, parent_id: str, request: Mapping[str, Any],
                       material: Mapping[str, Any]) -> dict:
    house = _house_module()
    b04, market, owned = _market_and_owned(session)
    objective = request["objective_request"]
    reasons, unknowns = [], []
    period = material["period_context"]
    if period.get("status") != "B02_PERIOD_CONTEXT_READ":
        unknowns.append("B02_PERIOD_UNAVAILABLE")
    market_currency = market.get("currency_unit")
    request_currency = objective.get("currency_unit")
    parent_currency = material["material"].get("currency_unit")
    if (request_currency != market_currency
            or request_currency != parent_currency):
        reasons.append("CURRENCY_MISMATCH")
    item = next((row for row in market["items"]
                 if row.get("kind") == objective.get("kind")), None)
    if item is None or item.get("quantity", 0) < 1:
        reasons.append("STOCK_UNAVAILABLE")
    elif item.get("unit_price") != objective.get("purchase_price"):
        reasons.append("PRICE_MISMATCH")
    feasibility = house.material_feasibility(session, objective)
    if feasibility.get("status") == "UNKNOWN":
        unknowns.extend(feasibility.get("unknowns") or ["B03_MATERIAL_UNKNOWN"])
    else:
        material_reasons = [
            reason for reason in feasibility.get("reasons") or []
            if reason != "REFUSED_AFFORDABILITY"
        ]
        if material_reasons:
            reasons.extend(material_reasons)
    focal_id = session.world().actor_state.get("A", {}).get("actor_id")
    if request["owner_actor_id"] not in {focal_id, parent_id}:
        reasons.append("OWNER_UNKNOWN")
    fields = material["material"]
    price = objective.get("purchase_price")
    if not isinstance(price, int) or price < 0:
        reasons.append("PRICE_MISMATCH")
        price = 0
    if fields["cash_units"] < price:
        reasons.append("INSUFFICIENT_PARENT_CASH")
    if fields["free_hours"] < 1:
        reasons.append("NO_PARENT_TIME")
    after_cash = fields["cash_units"] - price
    after_free = fields["free_hours"] - 1
    if after_cash < fields["debt_units"]:
        reasons.append("OBLIGATION_DEBT")
    if after_free < fields["care_hours_due"]:
        reasons.append("OBLIGATION_CARE")
    if reasons:
        action = ACTION_DECLINE
        status = "REFUSED"
    elif unknowns:
        action = ACTION_HOLD
        status = "HELD"
    else:
        action = ACTION_PURCHASE
        status = "ADMISSIBLE"
    return {
        "action": action,
        "status": status,
        "reasons": reasons,
        "unknowns": unknowns,
        "request": detached(request),
        "material": detached(material["material"]),
        "material_source": material["source"],
        "period_context": detached(period),
        "market": {
            "source": market["source"],
            "currency_unit": market_currency,
            "item": detached(item) if item is not None else None,
        },
        "owned": {
            "status": owned["status"],
            "source": owned["source"],
        },
        "b03_feasibility": detached(feasibility),
        "obligation_check": {
            "cash_before": fields["cash_units"],
            "cash_after": after_cash,
            "debt_units": fields["debt_units"],
            "free_hours_before": fields["free_hours"],
            "free_hours_after": after_free,
            "care_hours_due": fields["care_hours_due"],
        },
    }


def _proposal_source(evaluation: Mapping[str, Any]) -> str:
    return digest({
        "schema": PARENT_PROPOSAL_SCHEMA,
        "rule": DECISION_RULE,
        "request": evaluation["request"],
        "material_source": evaluation["material_source"],
        "period": evaluation["period_context"].get("plan_source"),
        "period_id": evaluation["period_context"].get("period", {}).get("period_id"),
        "market_source": evaluation["market"]["source"],
        "owned_source": evaluation["owned"]["source"],
        "b03_material": {
            "reasons": [
                reason for reason in
                (evaluation["b03_feasibility"].get("reasons") or [])
                if reason != "REFUSED_AFFORDABILITY"
            ],
            "unknowns": list(
                evaluation["b03_feasibility"].get("unknowns") or []),
        },
        "action": evaluation["action"],
        "reasons": evaluation["reasons"],
        "unknowns": evaluation["unknowns"],
    })


def _proposal(session, parent_id: str, request: Mapping[str, Any]) -> dict:
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    evaluation = _evaluate_purchase(session, parent_id, request, material)
    source = _proposal_source(evaluation)
    return {
        "schema": PARENT_PROPOSAL_SCHEMA,
        "grade": DECISION_GRADE,
        "status": "PROPOSED",
        "request_id": request["request_id"],
        "actor_id": parent_id,
        "alias": material["alias"],
        "root": material["root"],
        "branch": material["branch"],
        "clock": material["clock"],
        "source": source,
        "rule": detached(DECISION_RULE),
        "evaluation": detached(evaluation),
        "decision": "NOT_ADMITTED",
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "SELF_ONLY_DECISION_BASIS",
        "request_source": "CALLER_SUPPLIED_OBJECTIVE_REQUEST",
        "decision_evidence": "EXPLICIT_SOURCEFREE_RULE_NOT_NATIVE",
    }


def propose_parent_decision(session, parent_id: str, *, request: Any,
                            as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    return _proposal(session, parent_id, _validate_request(session, request))



def read_parent_material_prospectives(session, parent_id: str, *,
                                      as_actor: str | None) -> dict:
    """Read five conditioned alternatives WITHOUT issuing maternal volition.

    This is a C03 actor-local, read-only bridge over existing C02 history,
    P2 material activity, B02 date qualification and B03/B04 opportunity.
    It intentionally never converts ELIGIBLE into CHOSEN/PERFORMED. Neither
    sourcefree purchase auto-selection nor a caller request counts as
    independently issued parent intent. Existing C03 legacy demo remains
    separately labelled an experimental rule, not parent-owned psychology.
    """
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    current = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    feasible = parent_feasible_actions(session, parent_id, as_actor=parent_id)
    history = read_parent_history(session, parent_id, as_actor=parent_id)
    if (not history.get("material_consistent")
            or history.get("root") != current["root"]
            or history.get("branch") != current["branch"]
            or history.get("clock") != current["clock"]
            or history.get("material_source") != current["source"]
            or feasible.get("source") != current["source"]
            or feasible.get("root") != current["root"]
            or feasible.get("branch") != current["branch"]
            or feasible.get("clock") != current["clock"]):
        raise RecursionRefusal("PARENT_PROSPECTIVES_SOURCE_STALE")

    # A known object is a possibility in the world, not a private wish.
    # Use the inherited B03/B04 evidence/readers, not a second market.
    request = parent_request_fixture(kind="junior", owner_actor_id=parent_id)
    purchase = _proposal(session, parent_id, request)
    if (purchase.get("root") != current["root"]
            or purchase.get("branch") != current["branch"]
            or purchase.get("clock") != current["clock"]
            or purchase["evaluation"]["material_source"] != current["source"]):
        raise RecursionRefusal("PARENT_PROSPECTIVES_SOURCE_STALE")
    purchase_eval = purchase["evaluation"]
    choice_labels = {
        "ADMISSIBLE": "ELIGIBLE_NOT_SELECTED",
        "REFUSED": "MATERIALLY_INELIGIBLE",
        "HELD": "MATERIAL_UNKNOWN_HELD",
    }
    purchase_status = choice_labels.get(purchase_eval["status"])
    if purchase_status is None:
        raise RecursionRefusal("PARENT_PROSPECTIVES_EVALUATION_INVALID")
    options = [{
        "candidate": "POSSIBLE_JUNIOR_PURCHASE",
        "status": purchase_status,
        "reasons": list(purchase_eval["reasons"]),
        "unknowns": list(purchase_eval["unknowns"]),
        "material_evaluation_source": purchase["source"],
        "chosen": False,
        "performed": False,
    }]
    for activity in ("PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"):
        rows = [row for row in feasible["options"]
                if row.get("activity") == activity]
        if len(rows) != 1:
            raise RecursionRefusal("PARENT_PROSPECTIVES_ACTIVITY_UNAVAILABLE")
        row = rows[0]
        options.append({
            "candidate": activity,
            "status": {
                "ADMISSIBLE": "ELIGIBLE_NOT_SELECTED",
                "REFUSED": "MATERIALLY_INELIGIBLE",
                "HELD": "MATERIAL_UNKNOWN_HELD",
            }.get(row["status"], "MATERIAL_UNKNOWN_HELD"),
            "reasons": list(row.get("reasons") or []),
            "unknowns": [],
            "material_evaluation_source": feasible["source"],
            "chosen": False,
            "performed": False,
        })
    options.append({
        "candidate": "QUIET_NONPURCHASE",
        "status": "ELIGIBLE_NOT_SELECTED",
        "reasons": [],
        "unknowns": [],
        "material_evaluation_source": current["source"],
        "chosen": False,
        "performed": False,
    })
    # Preserve chronology and actual history identity; do not expose the
    # mother's private registration/claims as child-consumable truth.
    historical_source = digest({
        "root": history["root"],
        "branch": history["branch"],
        "clock": history["clock"],
        "material_source": history["material_source"],
        "history": history["history"],
        "period_qualification": history["period_qualification"],
    })
    result = {
        "schema": PARENT_PROSPECTIVE_READ_SCHEMA,
        "grade": DECISION_GRADE,
        "status": "CANDIDATES_ONLY_ACTOR_SELECTION_UNISSUED",
        "actor_id": parent_id,
        "alias": current["alias"],
        "root": current["root"],
        "branch": current["branch"],
        "clock": current["clock"],
        "material_source": current["source"],
        "history_source": historical_source,
        "period_qualification": history["period_qualification"],
        "options": options,
        "option_count": len(options),
        "chosen_candidate": None,
        "performed_event": None,
        "decision_rule": "NO_PARENT_VOLITION_ISSUED",
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "NOT_EXPOSED",
        "language_generation_owner": "NOT_IMPLEMENTED",
        "native_science": False,
        "first_consumer": "PARENT_OWNED_PROSPECTIVE_PERFORMER_HELD",
    }
    result["source"] = digest(result)
    return result



def _decision_episodes(session, alias: str, operation_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias
        and row.get("kind") == PARENT_DECISION_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    ]


def _action_episodes(session, alias: str, decision_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias
        and row.get("kind") == PARENT_ACTION_KIND
        and (row.get("body") or {}).get("decision_id") == decision_id
    ]


def admit_parent_decision(session, parent_id: str, *, operation_id: str,
                          request: Any, as_actor: str | None = None,
                          expected_clock: int | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    if not _text(operation_id):
        raise RecursionRefusal("PARENT_DECISION_SCHEMA")
    request = _validate_request(session, request)
    with _parent_write_lock(session):
        material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
        alias = material["alias"]
        if expected_clock is not None and expected_clock != material["clock"]:
            raise RecursionRefusal("PARENT_DECISION_CLOCK_MISMATCH")
        episodes = _decision_episodes(session, alias, operation_id)
        if len(episodes) > 1:
            raise RecursionRefusal("PARENT_DECISION_DUPLICATE")
        if episodes:
            body = episodes[0].get("body") or {}
            if (body.get("actor_id") != parent_id
                    or body.get("request") != request):
                raise RecursionRefusal("PARENT_DECISION_REUSE_MISMATCH")
            proposal = body.get("proposal") or {}
            current = _proposal(session, parent_id, request)
            if proposal.get("source") != current.get("source"):
                raise RecursionRefusal("PARENT_DECISION_REPLAY_STALE")
            receipt = dict(body.get("receipt") or {})
            receipt["status"] = "REPLAY"
            return receipt
        proposal = _proposal(session, parent_id, request)
        evaluation = proposal["evaluation"]
        decision = {
            "action": evaluation["action"],
            "status": evaluation["status"],
            "reasons": list(evaluation["reasons"]),
            "unknowns": list(evaluation["unknowns"]),
            "proposal_source": proposal["source"],
            "rule": detached(DECISION_RULE),
        }
        receipt = {
            "schema": PARENT_DECISION_RECEIPT_SCHEMA,
            "grade": DECISION_GRADE,
            "status": "ADMITTED",
            "operation_id": operation_id,
            "decision_id": operation_id,
            "actor_id": parent_id,
            "alias": alias,
            "root": material["root"],
            "branch": material["branch"],
            "clock": material["clock"],
            "request_id": request["request_id"],
            "request": detached(request),
            "proposal": proposal,
            "decision": decision,
            "performed": False,
            "action_effect": "NONE_UNTIL_PERFORM",
            "child_request": "NOT_EVALUATED",
            "nadia_state": "NOT_READ",
            "private_state": "SELF_ONLY_DECISION_BASIS",
            "request_source": "CALLER_SUPPLIED_OBJECTIVE_REQUEST",
            "decision_evidence": "EXPLICIT_SOURCEFREE_RULE_NOT_NATIVE",
            "physical_admission": "NOT_YET_PERFORMED",
            "language_generation_owner": "C04_CALLER_SUPPLIED_TEXT",
            "native_science": False,
        }
        store = session.product.store
        with _StoreWrite(store):
            store.append_episode(
                session.branch_id, actor_id=alias,
                kind=PARENT_DECISION_KIND, clock=material["clock"],
                body={
                    "schema": PARENT_DECISION_RECEIPT_SCHEMA,
                    "grade": DECISION_GRADE,
                    "root": material["root"],
                    "branch": material["branch"],
                    "actor_id": parent_id,
                    "alias": alias,
                    "operation_id": operation_id,
                    "decision_id": operation_id,
                    "request": detached(request),
                    "proposal": proposal,
                    "decision": decision,
                    "receipt": receipt,
                },
            )
        return receipt


def read_parent_decision(session, parent_id: str, decision_id: str, *,
                         as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    alias = material["alias"]
    episodes = _decision_episodes(session, alias, decision_id)
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_DECISION_NOT_FOUND")
    body = episodes[0].get("body") or {}
    if (body.get("actor_id") != parent_id
            or body.get("root") != material["root"]
            or body.get("branch") != material["branch"]):
        raise RecursionRefusal("PARENT_DECISION_SEVERED")
    receipt = dict(body.get("receipt") or {})
    actions = _action_episodes(session, alias, decision_id)
    action = (actions[0].get("body") or {}).get("receipt") if actions else None
    return {
        "schema": PARENT_DECISION_RECEIPT_SCHEMA,
        "grade": DECISION_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "decision_id": decision_id,
        "clock": episodes[0]["clock"],
        "request_id": (body.get("request") or {}).get("request_id"),
        "proposal": detached(body.get("proposal") or {}),
        "decision": detached(body.get("decision") or {}),
        "receipt": receipt,
        "action": detached(action) if action is not None else None,
        "performed": bool((action or {}).get("performed")),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "SELF_ONLY_DECISION_BASIS",
    }


def _perform_purchase(session, parent_id: str, decision: Mapping[str, Any],
                      request: Mapping[str, Any], decision_id: str) -> dict:
    b04 = _b04_module()
    if b04 is None or not hasattr(b04, "_purchase_drum_kit"):
        raise RecursionRefusal("PARENT_DECISION_MARKET_UNAVAILABLE")
    objective = request["objective_request"]
    try:
        return b04._purchase_drum_kit(
            session, parent_id,
            operation_id=decision_id + ":purchase",
            owner_actor_id=request["owner_actor_id"],
            request=objective,
            expected_clock=None,
        )
    except RecursionRefusal as exc:
        return {
            "schema": "SOROK_PARENT_PURCHASE_RECEIPT@1",
            "grade": DECISION_GRADE,
            "status": "REFUSED",
            "operation_id": decision_id + ":purchase",
            "parent_id": parent_id,
            "reasons": [str(exc)],
            "event_effect": "NONE",
            "possession": "NONE",
            "error": str(exc),
        }


def _perform_parent_decision_locked(session, parent_id: str, *, decision_id: str,
                            as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    alias = material["alias"]
    episodes = _decision_episodes(session, alias, decision_id)
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_DECISION_NOT_FOUND")
    body = episodes[0].get("body") or {}
    if (body.get("actor_id") != parent_id
            or body.get("root") != material["root"]
            or body.get("branch") != material["branch"]):
        raise RecursionRefusal("PARENT_DECISION_SEVERED")
    decision = body.get("decision") or {}
    request = body.get("request") or {}
    existing = _action_episodes(session, alias, decision_id)
    if len(existing) > 1:
        raise RecursionRefusal("PARENT_ACTION_DUPLICATE")
    if existing:
        receipt = dict((existing[0].get("body") or {}).get("receipt") or {})
        receipt["status"] = "REPLAY"
        return receipt
    current = _proposal(
        session, parent_id, _validate_request(session, request))
    if current.get("source") != decision.get("proposal_source"):
        raise RecursionRefusal("PARENT_DECISION_STALE")
    action = decision.get("action")
    purchase = None
    if action == ACTION_PURCHASE:
        purchase = _perform_purchase(
            session, parent_id, decision, request, decision_id)
        if (purchase.get("status") in {"ADMITTED", "REPLAY"}
                and purchase.get("possession")
                == "OBJECT_STOCK_AND_OWNERSHIP_WRITTEN"):
            action_status = "PERFORMED"
            performed = True
            valid_empty = False
        else:
            action_status = "REFUSED"
            performed = False
            valid_empty = True
    elif action == ACTION_DECLINE:
        action_status = "VALID_EMPTY"
        performed = False
        valid_empty = True
    elif action == ACTION_HOLD:
        action_status = "HELD"
        performed = False
        valid_empty = True
    else:
        raise RecursionRefusal("PARENT_DECISION_ACTION_UNKNOWN")
    receipt = {
        "schema": PARENT_ACTION_RECEIPT_SCHEMA,
        "grade": DECISION_GRADE,
        "status": action_status,
        "decision_id": decision_id,
        "operation_id": decision_id + ":action",
        "actor_id": parent_id,
        "alias": alias,
        "root": material["root"],
        "branch": material["branch"],
        "clock": session.clock(),
        "request_id": request.get("request_id"),
        "decision_action": action,
        "performed": performed,
        "valid_empty": valid_empty,
        "purchase": detached(purchase) if purchase is not None else None,
        "material_before_source": material["source"],
        "material_after_source": (
            (purchase or {}).get("parent_material_source_after")
            or material["source"]),
        "owned_source_after": (purchase or {}).get("owned_source_after"),
        "event_effect": (
            "NONE" if purchase is None
            else (purchase or {}).get("event_effect", "NONE")),
        "possession": (
            "NONE" if purchase is None
            else (purchase or {}).get("possession", "NONE")),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "SELF_ONLY_DECISION_BASIS",
        "decision_evidence": "ADMITTED_DECISION_REEVALUATED_AT_PERFORM",
        "physical_admission": (
            "PERFORMED" if performed else
            "HELD" if action_status == "HELD" else "VALID_EMPTY"),
        "language_generation_owner": "C04_CALLER_SUPPLIED_TEXT",
        "native_science": False,
    }
    store = session.product.store
    with _StoreWrite(store):
        store.append_episode(
            session.branch_id, actor_id=alias,
            kind=PARENT_ACTION_KIND, clock=session.clock(),
            body={
                "schema": PARENT_ACTION_RECEIPT_SCHEMA,
                "grade": DECISION_GRADE,
                "root": material["root"],
                "branch": material["branch"],
                "actor_id": parent_id,
                "alias": alias,
                "decision_id": decision_id,
                "operation_id": decision_id + ":action",
                "action": action,
                "status": action_status,
                "receipt": receipt,
            },
        )
    return receipt


def perform_parent_decision(session, parent_id: str, *, decision_id: str,
                            as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    b04 = _b04_module()
    if (b04 is None or not hasattr(b04, "_purchase_lock")
            or not hasattr(b04, "_purchase_drum_kit")):
        raise RecursionRefusal("PARENT_DECISION_B04_UNLOCKED_WRITER_UNAVAILABLE")
    # B04's public purchase wrapper locks market/material first, then the
    # parent lock. Hold the same order here and call its unlocked actual
    # writer, so the decision revalidation and purchase stay in one lock
    # composition instead of recursively taking the parent lock.
    with b04._purchase_lock(session):
        with _parent_write_lock(session):
            return _perform_parent_decision_locked(
                session, parent_id, decision_id=decision_id,
                as_actor=as_actor,
            )


def read_parent_action(session, parent_id: str, decision_id: str, *,
                       as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    alias = material["alias"]
    episodes = _action_episodes(session, alias, decision_id)
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_ACTION_NOT_FOUND")
    body = episodes[0].get("body") or {}
    if (body.get("actor_id") != parent_id
            or body.get("root") != material["root"]
            or body.get("branch") != material["branch"]):
        raise RecursionRefusal("PARENT_ACTION_SEVERED")
    return {
        "schema": PARENT_ACTION_RECEIPT_SCHEMA,
        "grade": DECISION_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "decision_id": decision_id,
        "clock": episodes[0]["clock"],
        "receipt": detached(body.get("receipt") or {}),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "SELF_ONLY_DECISION_BASIS",
    }
