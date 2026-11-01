"""The CP-A5 multicontact continuing-person assertion.

This assertion runs on the actual stored history produced by the scenario. It
requires A's cross-context inspection evidence, the test-only custody decision,
B's independent tool-taking market commission, A's later blocked repair, A's
bounded knowledge, and the read-only encounter. Any missing source edge raises a
named AssertionError at this same consumer.
"""
from __future__ import annotations

from pathlib import Path

from bp4.canon import digest

from .encounter import EncounterReader, render_encounter

ASSERTION_NAME = "cp_a5.assertion.multicontext_encounter_assertion"
RECEIPT_SCHEMA = "SOROK_CP_A5_ASSERTION_RECEIPT@1"


def _events(reader: EncounterReader) -> list[dict]:
    return reader.all_events()


def _of(events: list[dict], kind: str, actor: str | None = None) -> list[dict]:
    return [event for event in events
            if event.get("kind") == kind
            and (actor is None or event.get("actor_id") == actor)]


def _a_repairs(events: list[dict]) -> list[dict]:
    return [event for event in events
            if event.get("kind") == "REPAIR"
            and event.get("actor_id") == "A"]


def run_a5_assertion(root: str | Path, *, branch_id: str = "root") -> dict:
    """Assert the intact multicontact life at the same A5 consumer."""
    with EncounterReader(root, branch_id=branch_id) as reader:
        view = reader.view()
        events = _events(reader)
        known_ids = set(view["known_event_ids"])
        if view["disposition"]["state"] != "ESTABLISHED":
            raise AssertionError("A3_CONTEXT_EVIDENCE_INSUFFICIENT")
        if view["disposition"]["inspection_count"] < 3:
            raise AssertionError("A3_INSPECTION_COUNT_INSUFFICIENT")
        if len(view["disposition"]["contexts"]) < 2:
            raise AssertionError("A3_CONTEXT_DIVERSITY_MISSING")

        decisions = _of(events, "A4_CUSTODY_DECISION", "A")
        if not decisions:
            raise AssertionError("A4_CUSTODY_DECISION_MISSING")
        decision = decisions[-1]
        if decision["body"].get("decision") != "RETAIN_TOOL":
            raise AssertionError("A4_CUSTODY_DECISION_NOT_RETAIN")
        if _of(events, "A4_CUSTODY_HELD", "A"):
            raise AssertionError("A4_CUSTODY_HELD_PRESENT")

        if not _of(events, "C_TOOL_REQUEST", "C"):
            raise AssertionError("A4_COACTOR_C_REQUEST_MISSING")
        if not _of(events, "C_WITHDRAW", "C"):
            raise AssertionError("A4_COACTOR_C_RELATION_MISSING")
        if not any(row.get("relation") == "REQUEST_UNMET"
                   for row in view["relations"]):
            raise AssertionError("A4_COACTOR_C_UNMET_RELATION_MISSING")
        if not _of(events, "B_TAKE_TOOL", "B"):
            raise AssertionError("A4_B_INDEPENDENT_ACTIVITY_MISSING")
        commission = _of(events, "B_MARKET_COMMISSION", "B")
        if not commission:
            raise AssertionError("A4_B_MARKET_COMMISSION_MISSING")
        if not _of(events, "A_REPAIR_BLOCKED", "A"):
            raise AssertionError("A4_B_TOOL_CONSEQUENCE_MISSING")
        repairs = _a_repairs(events)
        if not repairs:
            raise AssertionError("A5_LATER_REPAIR_MISSING")

        state = reader.product.store.latest_state(reader.branch_id)
        b_state = state["actors"]["B"]["state"]
        a_state = state["actors"]["A"]["state"]
        if int(b_state.get("cash", 0)) != 58:
            raise AssertionError("A4_B_CASH_CONSEQUENCE:" + str(b_state.get("cash")))
        if int(b_state.get("completed_units", 0)) != 5:
            raise AssertionError("A4_B_COMPLETED_CONSEQUENCE")
        if not state["world"]["resources"]["workshop"].get("tool_available"):
            raise AssertionError("A4_TOOL_NOT_RETURNED")
        if int(a_state.get("material_remaining", 0)) != 1:
            raise AssertionError("A5_A_MATERIAL_CONSEQUENCE")
        if int(a_state.get("completed_units", 0)) != 5:
            raise AssertionError("A5_A_COMPLETED_CONSEQUENCE")

        if commission[-1]["event_id"] in known_ids:
            raise AssertionError("A5_UNPERCEIVED_EVENT_LEAK")
        if _of(events, "B_TAKE_TOOL", "B")[-1]["event_id"] not in known_ids:
            raise AssertionError("A5_A_TOOL_ACCESS_MISSING")
        if any(event["kind"] == "C_TOOL_REQUEST"
               and event["event_id"] not in known_ids for event in events):
            raise AssertionError("A5_C_REQUEST_ACCESS_MISSING")

        tool_answer = reader.ask("What happened to the workshop tool?")
        market_answer = reader.ask("What did B do at the market?")
        if tool_answer["status"] != "OK":
            raise AssertionError("A5_TOOL_ANSWER_NOT_GROUNDED")
        if market_answer["status"] != "UNKNOWN":
            raise AssertionError("A5_MARKET_UNKNOWN_LEAK")
        before = reader.canonical_digest()
        render_encounter(view, "plain")
        render_encounter(view, "compact")
        after = reader.canonical_digest()
        if before != after:
            raise AssertionError("A5_RENDER_MUTATED_CANONICAL_STATE")

        receipt = {
            "schema": RECEIPT_SCHEMA,
            "assertion": ASSERTION_NAME,
            "status": "PASS",
            "grade": "TEST_ONLY_SOURCEFREE_CP_A5_NOT_NATIVE",
            "native": False,
            "actor": "A",
            "branch_id": reader.branch_id,
            "clock": view["as_of_clock"],
            "evidence": view["disposition"],
            "decision": decision["body"]["decision"],
            "coactor_relation": view["relations"][-1] if view["relations"] else None,
            "material": {
                "tool_available": state["world"]["resources"]["workshop"].get(
                    "tool_available"),
                "a_material_remaining": a_state.get("material_remaining"),
                "a_completed_units": a_state.get("completed_units"),
                "a_cash": a_state.get("cash"),
                "b_cash": b_state.get("cash"),
                "b_completed_units": b_state.get("completed_units"),
            },
            "known_event_ids": view["known_event_ids"],
            "unperceived_event_count": view["unperceived_event_count"],
            "encounter": {"tool": tool_answer, "market": market_answer},
            "read_only": tool_answer["read_only"] and market_answer["read_only"],
            "canonical_digest": after,
            "native_claims": {"person": False, "actor": False, "c9": False,
                              "c12": False, "anchor": False},
        }
        receipt["receipt_hash"] = digest(receipt)
        return receipt


__all__ = ["ASSERTION_NAME", "RECEIPT_SCHEMA", "run_a5_assertion"]
