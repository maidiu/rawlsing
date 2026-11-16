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
    relation_episodes, start_world, viewer_document,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    read_relation_history,
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


def actor_facing(document):
    return {
        key: document[key]
        for key in ("history", "context", "event", "access")
    }


def has_withheld(value) -> bool:
    return "withheld_relation_count" in canonical(value)


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
        q_missing_named = read_relation_history(
            session, Q_ID, other_actor_id=P_ID, relation="r3-missing")
        q_hidden_named = read_relation_history(
            session, Q_ID, other_actor_id=P_ID, relation=HIDDEN)
        p_missing_named = read_relation_history(
            session, P_ID, other_actor_id=O_ID, relation="r3-missing")
        p_hidden_named = read_relation_history(
            session, P_ID, other_actor_id=O_ID, relation=HIDDEN)
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
        a_actor = actor_facing(a_doc)
        b_actor = actor_facing(b_doc)
        c_actor = actor_facing(c_doc)
        a_cold_actor = actor_facing(a_cold)
        b_cold_actor = actor_facing(b_cold)
        c_cold_actor = actor_facing(c_cold)
        b_sever_actor = actor_facing(b_sever)
        b_restored_actor = actor_facing(b_restored)
        c_sever_actor = actor_facing(c_sever)
        c_restored_actor = actor_facing(c_restored)
        checks = {
            "same_event": (
                a_doc["event"] == b_doc["event"] == c_doc["event"]
                and a_doc["context"]["event_id"]
                == b_doc["context"]["event_id"]
                == c_doc["context"]["event_id"]),
            "a_no_withheld": not has_withheld(a_actor),
            "b_hidden_no_withheld": not has_withheld(b_actor),
            "a_b_full_actor_documents_equal": a_actor == b_actor,
            "a_b_history_equal": a_actor["history"] == b_actor["history"],
            "a_b_context_equal": a_actor["context"] == b_actor["context"],
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
            "c_hidden_not_visible_and_no_withheld": (
                all(
                    relation["relation"] != HIDDEN
                    for relation in c_doc["context"]["relation_scope"][
                        "relations"])
                and not has_withheld(c_actor)),
            "c_event_perception_viewer_specific": (
                c_doc["context"]["context_effect"]["event_perception"]
                == "NOT_PERCEIVED"
                and c_doc["context"]["context_effect"][
                    "event_perception_source"] == "VIEWER_EVENT_ACCESS"
                and c_doc["context"]["context_effect"][
                    "event_perception_scope"] == "VIEWER_ONLY"
                and "C12_EVENT_PERCEPTION" not in c_doc[
                    "context"]["context_effect"]["basis"]
                and c_doc["context"]["context_effect"][
                    "relation_aware"] is True
                and c_doc["context"]["context_effect"][
                    "relation_count"] == 1
                and c_doc["context"]["context_effect"][
                    "summary_selection"]
                == "MECHANICAL_FIRST_SORTED_RELATION_KEY"
                and c_doc["context"]["context_effect"][
                    "summary_is_salience_or_psychology"] is False),
            "c_event_still_not_perceived": (
                c_doc["access"]["status"] == "NOT_PERCEIVED"),
            "named_absent_unexposed_same_hold": (
                q_missing_named == q_hidden_named
                and q_missing_named["status"] == "HOLD_NOT_EXPOSED"
                and q_hidden_named["status"] == "HOLD_NOT_EXPOSED"
                and "withheld_relation_count" not in canonical(
                    q_missing_named)),
            "named_party_scope_is_qualified": (
                p_missing_named["status"] == "HOLD_NOT_EXPOSED"
                and p_hidden_named["status"] == "QUALIFIED"
                and p_hidden_named["relations"][0]["relation"] == HIDDEN),
            "cold_a_actor_exact": a_cold_actor == a_actor,
            "cold_b_actor_exact": b_cold_actor == b_actor,
            "cold_c_actor_exact": c_cold_actor == c_actor,
            "cold_b_no_withheld": not has_withheld(b_cold_actor),
            "b_sever_no_custody_disclosure": (
                b_sever["history"]["status"] == "HOLD_NOT_EXPOSED"
                and b_sever["context"]["relation_scope"]["status"]
                == "HOLD_NOT_EXPOSED"
                and b_sever["context"]["relation_scope"]["relations"] == []
                and not has_withheld(b_sever_actor)),
            "b_sever_actor_exact": b_sever_actor == b_actor,
            "b_sever_restore_exact": b_restored_actor == b_actor,
            "c_sever_custody_hold": (
                c_sever["history"]["status"] == "HOLD_CUSTODY_SEVERED"
                and c_sever["context"]["relation_scope"]["status"]
                == "HOLD_CUSTODY_SEVERED"
                and c_sever["context"]["relation_scope"]["relations"] == []
                and c_sever["access"]["status"] == "NOT_PERCEIVED"
                and not has_withheld(c_sever_actor)),
            "c_sever_restore_exact": c_restored_actor == c_actor,
        }
        report = {
            "schema": "SOROK_C05_R3_CHALLENGE1@1",
            "source_sha": "4b33b8be1127c2186931a66f23e3a2b05feaf0a6",
            "final_report_sha": "fdce1cc266d914c8a28d290f881b42d745025d8c",
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
            "named_queries": {
                "q_missing": q_missing_named,
                "q_hidden_pair": q_hidden_named,
                "p_missing": p_missing_named,
                "p_hidden_party": p_hidden_named,
                "note": "Q/P named queries cannot name the hidden P/O pair; Q/P is absent while P/O hidden is visible to party P by mandatory exposure",
            },
            "c_sever": c_sever,
            "c_restored": c_restored,
            "counts": counts(session),
            "relation_episodes": relation_episodes(session),
            "checks": checks,
            "passed": all(checks.values()),
            "actor_facing_difference": {
                "full_actor_documents_equal": checks[
                    "a_b_full_actor_documents_equal"],
                "withheld_field_absent": (
                    checks["a_no_withheld"]
                    and checks["b_hidden_no_withheld"]
                    and checks["cold_b_no_withheld"]),
                "a_b_history_equal": checks["a_b_history_equal"],
                "a_b_context_equal": checks["a_b_context_equal"],
            },
        }
        path = EVIDENCE / "c05_challenge1_report.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True))
        print(json.dumps({
            "passed": report["passed"],
            "failed": [key for key, value in checks.items() if not value],
            "event_id": a_doc["event"]["event_id"],
            "full_actor_documents_equal": report[
                "actor_facing_difference"]["full_actor_documents_equal"],
            "withheld_field_absent": report[
                "actor_facing_difference"]["withheld_field_absent"],
            "c_status": c_doc["history"]["status"],
            "c_event_access": c_doc["access"]["status"],
            "cold_b_actor_exact": checks["cold_b_actor_exact"],
            "report": str(path),
        }, indent=2, sort_keys=True))
        return 0 if report["passed"] else 2
    finally:
        owner.close()
        fanin.close()


if __name__ == "__main__":
    raise SystemExit(main())
