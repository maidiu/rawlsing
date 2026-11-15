"""Challenge 1: hidden-relationship existence/cardinality through actor-facing reads.

One real P2 fixture and one real event. The same state/event is read before and
after controlled C12 relation writes:
A: no relation.
B: P/O relation exposed only to P/O; viewer Q has no exposure.
C: additionally, a P/R relation exposed to Q (genuine positive for Q); the
   hidden P/O relation remains unexposed.
The event ID/hash/clock/world are identical in every read; only relation writes
differ.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVIDENCE = HERE.parent / "evidence"
if str(HERE) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(HERE))

from c05_r3_common import (  # noqa: E402
    O_ID, P_ID, Q_ID, R_ID, canonical, cold_document, counts, later_event,
    relation_episodes, start_world, strip_withheld, viewer_document,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    record_relation_change,
)

HIDDEN = "r3-hidden-relation"
VISIBLE = "r3-visible-relation"


def hide_scope_read(session, viewer, event_id, as_of_clock, episode_id):
    store = session.product.store
    original = store.episodes

    def hider(scope_episode_id):
        def patched(branch_id):
            return [
                row for row in original(branch_id)
                if row.get("episode_id") != scope_episode_id
            ]
        return patched

    with patch.object(store, "episodes", side_effect=hider(episode_id)):
        return viewer_document(session, viewer, event_id, as_of_clock)


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    fanin, session, focal, owner, state = start_world("leak-sequential")
    try:
        result, proposal, event_id = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch1:event", proposal_id="r3:ch1:event",
            delta=6)
        event_clock = session.event(event_id)["clock"]
        state_root = str(state)
        a_doc = viewer_document(session, Q_ID, event_id, event_clock)
        a_cold = cold_document(state_root, Q_ID, event_id, event_clock)
        hidden = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=HIDDEN, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch1:hidden", exposed_actor_ids=[P_ID, O_ID],
            value="hidden-guest")
        b_doc = viewer_document(session, Q_ID, event_id, event_clock)
        b_cold = cold_document(state_root, Q_ID, event_id, event_clock)
        b_sever = hide_scope_read(
            session, Q_ID, event_id, event_clock,
            hidden["primary_episode_id"])
        b_restored = viewer_document(session, Q_ID, event_id, event_clock)
        visible = record_relation_change(
            session, actor_id=P_ID, other_actor_id=R_ID,
            relation=VISIBLE, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch1:visible",
            exposed_actor_ids=[P_ID, R_ID, Q_ID], value="visible-guest")
        c_doc = viewer_document(session, Q_ID, event_id, event_clock)
        c_cold = cold_document(state_root, Q_ID, event_id, event_clock)
        c_sever = hide_scope_read(
            session, Q_ID, event_id, event_clock,
            visible["primary_episode_id"])
        c_restored = viewer_document(session, Q_ID, event_id, event_clock)
        a_hist = strip_withheld(a_doc["history"])
        b_hist = strip_withheld(b_doc["history"])
        a_ctx = strip_withheld(a_doc["context"])
        b_ctx = strip_withheld(b_doc["context"])
        checks = {
            "same_event": (
                a_doc["event"] == b_doc["event"] == c_doc["event"]
                and a_doc["context"]["event_id"]
                == b_doc["context"]["event_id"]
                == c_doc["context"]["event_id"]),
            "a_no_withheld": a_doc["history"][
                "withheld_relation_count"] == 0
            and a_doc["context"]["relation_scope"][
                "withheld_relation_count"] == 0,
            "b_hidden_withheld_one": b_doc["history"][
                "withheld_relation_count"] == 1
            and b_doc["context"]["relation_scope"][
                "withheld_relation_count"] == 1,
            "a_b_history_equal_except_withheld": a_hist == b_hist,
            "a_b_context_equal_except_withheld": a_ctx == b_ctx,
            "a_b_both_hold_not_exposed": (
                a_doc["history"]["status"] == "HOLD_NOT_EXPOSED"
                and b_doc["history"]["status"] == "HOLD_NOT_EXPOSED"
                and a_doc["context"]["relation_scope"]["status"]
                == "HOLD_NOT_EXPOSED"
                and b_doc["context"]["relation_scope"]["status"]
                == "HOLD_NOT_EXPOSED"),
            "a_b_context_effect_same_hold": (
                a_doc["context"]["context_effect"]
                == b_doc["context"]["context_effect"]),
            "a_b_event_access_same": (
                a_doc["access"]["status"] == "NOT_PERCEIVED"
                and b_doc["access"]["status"] == "NOT_PERCEIVED"),
            "c_positive_visible_qualified": (
                c_doc["history"]["status"] == "QUALIFIED"
                and c_doc["context"]["relation_scope"]["status"]
                == "QUALIFIED"
                and any(
                    relation["relation"] == VISIBLE
                    and relation["entries"][0]["change"] == "ENTER"
                    and relation["viewer_is_party"] is False
                    for relation in c_doc["context"]["relation_scope"][
                        "relations"])),
            "c_hidden_still_withheld": (
                c_doc["history"]["withheld_relation_count"] == 1
                and c_doc["context"]["relation_scope"][
                    "withheld_relation_count"] == 1
                and all(
                    relation["relation"] != HIDDEN
                    for relation in c_doc["context"]["relation_scope"][
                        "relations"])),
            "c_event_still_not_perceived": (
                c_doc["access"]["status"] == "NOT_PERCEIVED"),
            "cold_a_exact": a_cold == a_doc,
            "cold_b_exact": b_cold == b_doc,
            "cold_c_exact": c_cold == c_doc,
            "cold_hidden_count_one": b_cold["history"][
                "withheld_relation_count"] == 1,
            "b_sever_no_custody_disclosure": (
                b_sever["history"]["status"] == "HOLD_NOT_EXPOSED"
                and b_sever["history"]["withheld_relation_count"] == 1
                and b_sever["context"]["relation_scope"]["status"]
                == "HOLD_NOT_EXPOSED"
                and b_sever["context"]["relation_scope"]["relations"] == []),
            "b_sever_restore_exact": b_restored == b_doc,
            "c_sever_custody_hold": (
                c_sever["history"]["status"] == "HOLD_CUSTODY_SEVERED"
                and c_sever["context"]["relation_scope"]["status"]
                == "HOLD_CUSTODY_SEVERED"
                and c_sever["context"]["relation_scope"]["relations"] == []
                and c_sever["access"]["status"] == "NOT_PERCEIVED"),
            "c_sever_restore_exact": c_restored == c_doc,
        }
        report = {
            "schema": "SOROK_C05_R3_CHALLENGE1@1",
            "source_sha": "5d771dd86767655534b23576075e5da2db4fba78",
            "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
            "hidden_relation": HIDDEN,
            "visible_relation": VISIBLE,
            "viewer": Q_ID,
            "event": a_doc["event"],
            "a": a_doc,
            "b": b_doc,
            "c": c_doc,
            "a_cold": a_cold,
            "b_cold": b_cold,
            "c_cold": c_cold,
            "b_sever": b_sever,
            "b_restored": b_restored,
            "c_sever": c_sever,
            "c_restored": c_restored,
            "counts": counts(session),
            "relation_episodes": relation_episodes(session),
            "checks": checks,
            "passed": all(checks.values()),
            "actor_facing_difference": {
                "history_withheld": [
                    a_doc["history"]["withheld_relation_count"],
                    b_doc["history"]["withheld_relation_count"],
                ],
                "context_withheld": [
                    a_doc["context"]["relation_scope"][
                        "withheld_relation_count"],
                    b_doc["context"]["relation_scope"][
                        "withheld_relation_count"],
                ],
                "all_other_compared_actor_fields_equal": (
                    checks["a_b_history_equal_except_withheld"]
                    and checks["a_b_context_equal_except_withheld"]),
            },
        }
        path = EVIDENCE / "c05_challenge1_report.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True))
        print(json.dumps({
            "passed": report["passed"],
            "failed": [key for key, value in checks.items() if not value],
            "event_id": a_doc["event"]["event_id"],
            "withheld_history": report["actor_facing_difference"][
                "history_withheld"],
            "withheld_context": report["actor_facing_difference"][
                "context_withheld"],
            "c_status": c_doc["history"]["status"],
            "c_event_access": c_doc["access"]["status"],
            "cold_b_exact": checks["cold_b_exact"],
            "report": str(path),
        }, indent=2, sort_keys=True))
        return 0 if report["passed"] else 2
    finally:
        owner.close()
        fanin.close()


if __name__ == "__main__":
    raise SystemExit(main())
