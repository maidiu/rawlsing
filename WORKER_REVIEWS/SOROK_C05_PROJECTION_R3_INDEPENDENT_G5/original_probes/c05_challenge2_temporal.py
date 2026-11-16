"""Challenge 2: later same-clock relation knowledge in an earlier event context.

One real P2 owner event at clock 228 is read before and after:
- a relation ENTER appended after the event at the same clock 228;
- a depth-2 PROMOTE appended after the event at the same clock 228;
- a later event at 234 and a relation CHANGE at 234 (later-clock control).
The event document and event access are compared before/after; the relation
context is reconstructed at event clock 228. Cold replay is included.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVIDENCE = HERE.parent / "evidence"
if str(HERE) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(HERE))

from c05_r3_common import (  # noqa: E402
    O_ID, P_ID, cold_document, counts, later_event, owner_operations,
    start_world, store_sequences, viewer_document,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    promote_relation,
    record_relation_change,
)

RELATION = "r3-temporal-relation"


def relation_view(document: dict) -> dict:
    return {
        "history": document["history"],
        "relation_scope": document["context"]["relation_scope"],
        "context_effect": document["context"]["context_effect"],
        "event_id": document["context"]["event_id"],
        "event_clock": document["context"]["event_clock"],
        "event_access_status": document["context"]["event_access"]["status"],
        "event_hash": document["event"]["hash"],
        "event_clock_doc": document["event"]["clock"],
        "read_boundary": document["context"]["read_boundary"],
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    fanin, session, focal, owner, state = start_world("temporal")
    try:
        result1, proposal1, event1 = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch2:event1", proposal_id="r3:ch2:event1",
            delta=6)
        event_clock = session.event(event1)["clock"]
        state_root = str(state)
        before = viewer_document(session, P_ID, event1, event_clock)
        event_before = session.event(event1)
        enter = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch2:enter", exposed_actor_ids=[P_ID, O_ID],
            value="guest")
        after_enter = viewer_document(session, P_ID, event1, event_clock)
        promote = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, depth=2, clock=session.world().clock,
            operation_id="r3:ch2:promote")
        after_promote = viewer_document(session, P_ID, event1, event_clock)
        event_after = session.event(event1)
        result2, proposal2, event2 = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch2:event2", proposal_id="r3:ch2:event2",
            delta=6)
        later_change = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="CHANGE", clock=session.world().clock,
            operation_id="r3:ch2:change", exposed_actor_ids=[P_ID, O_ID],
            value="later")
        after_later = viewer_document(session, P_ID, event1, event_clock)
        cold = cold_document(state_root, P_ID, event1, event_clock)
        event_cold = session.event(event1)
        sequences = store_sequences(session)
        operations = owner_operations(owner)
        before_view = relation_view(before)
        enter_view = relation_view(after_enter)
        promote_view = relation_view(after_promote)
        later_view = relation_view(after_later)
        checks = {
            "event_document_unchanged": (
                event_before == event_after == event_cold),
            "event_access_still_perceived": (
                before["access"]["status"] == "PERCEIVED"
                and after_enter["access"]["status"] == "PERCEIVED"
                and after_promote["access"]["status"] == "PERCEIVED"
                and after_later["access"]["status"] == "PERCEIVED"),
            "before_relation_hold": (
                before["history"]["status"] == "HOLD_NOT_EXPOSED"
                and before["context"]["relation_scope"]["status"]
                == "HOLD_NOT_EXPOSED"
                and before["context"]["context_effect"]["relation_aware"]
                is False),
            "same_clock_enter_changes_prior_context": (
                after_enter["history"]["status"] == "QUALIFIED"
                and after_enter["context"]["relation_scope"]["status"]
                == "QUALIFIED"
                and after_enter["context"]["context_effect"]["relation_aware"]
                is True
                and after_enter["context"]["context_effect"]["basis"]
                == ["DATED_RELATION_HISTORY", "C12_EVENT_PERCEPTION"]),
            "same_clock_promote_changes_prior_context": (
                after_promote["context"]["relation_scope"][
                    "representation_depth"] == 2
                and len(after_promote["context"]["relation_scope"][
                    "relations"][0]["promotions"]) == 1
                and promote["status"] == "RECORDED"),
            "prior_event_relation_view_changed": (
                before_view != promote_view
                and enter_view != promote_view),
            "later_clock_change_not_included_in_event_228": (
                later_view["relation_scope"] == promote_view["relation_scope"]
                and later_view["context_effect"]
                == promote_view["context_effect"]
                and later_view["history"] == promote_view["history"]),
            "later_event_and_change_realized": (
                result2.status == "REALIZED"
                and later_change["status"] == "RECORDED"
                and session.event(event2)["clock"] == 234),
            "cold_event_228_context_exact": (
                cold["history"] == after_later["history"]
                and cold["context"] == after_later["context"]
                and cold["event"] == after_later["event"]
                and cold["access"] == after_later["access"]
                and cold["counts"] == after_later["counts"]),
            "c12_event_and_relation_sequences_are_separate": (
                len(sequences["world_events"]) >= 2
                and len(sequences["episodes"]) >= 2),
            "owner_operations_contain_events_not_relation_changes": (
                "r3:ch2:event1" in operations
                and "r3:ch2:event2" in operations
                and "r3:ch2:enter" not in operations
                and "r3:ch2:promote" not in operations
                and "r3:ch2:change" not in operations),
        }
        report = {
            "schema": "SOROK_C05_R3_CHALLENGE2@1",
            "source_sha": "5d771dd86767655534b23576075e5da2db4fba78",
            "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
            "relation": RELATION,
            "event1": event1,
            "event2": event2,
            "event_clock": event_clock,
            "before": before,
            "after_enter": after_enter,
            "after_promote": after_promote,
            "after_later": after_later,
            "cold": cold,
            "event_before": event_before,
            "event_after": event_after,
            "event_cold": event_cold,
            "enter": enter,
            "promote": promote,
            "later_change": later_change,
            "sequences": sequences,
            "owner_operations": operations,
            "views": {
                "before": before_view,
                "after_enter": enter_view,
                "after_promote": promote_view,
                "after_later": later_view,
            },
            "checks": checks,
            "witness_reproduced": (
                checks["same_clock_enter_changes_prior_context"]
                and checks["same_clock_promote_changes_prior_context"]
                and checks["prior_event_relation_view_changed"]),
            "pass_controls": (
                checks["event_document_unchanged"]
                and checks["event_access_still_perceived"]
                and checks["later_clock_change_not_included_in_event_228"]
                and checks["cold_event_228_context_exact"]),
        }
        path = EVIDENCE / "c05_challenge2_report.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True))
        print(json.dumps({
            "witness_reproduced": report["witness_reproduced"],
            "pass_controls": report["pass_controls"],
            "failed_checks": [
                key for key, value in checks.items() if not value],
            "event_id": event1,
            "before_relation_status": before["history"]["status"],
            "after_enter_status": after_enter["history"]["status"],
            "after_promote_depth": after_promote["context"][
                "relation_scope"]["representation_depth"],
            "after_later_scope_same_as_promote": later_view[
                "relation_scope"] == promote_view["relation_scope"],
            "cold_exact": checks["cold_event_228_context_exact"],
            "owner_ops": operations,
            "report": str(path),
        }, indent=2, sort_keys=True))
        return 0 if report["witness_reproduced"] and report["pass_controls"] else 2
    finally:
        owner.close()
        fanin.close()


if __name__ == "__main__":
    raise SystemExit(main())
