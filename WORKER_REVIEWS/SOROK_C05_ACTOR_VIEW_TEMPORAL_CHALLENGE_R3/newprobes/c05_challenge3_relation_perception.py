"""Challenge 3: prior qualified relation context versus current non-perception,
and two simultaneously available relations.

P has two qualified prior relations (P/O and P/R) and does not perceive the
current event (focal/O). The actor-facing reader is inspected directly. No
salience or psychological priority rule is invented; the plural list and the
singular first-sorted summary are both exposed.
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
    O_ID, P_ID, R_ID, cold_document, counts, later_event, start_world,
    viewer_document,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    record_relation_change,
)

REL_ONE = "r3-known-one"
REL_TWO = "r3-known-two"


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    fanin, session, focal, owner, state = start_world("relper")
    try:
        first = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=REL_ONE, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch3:one", exposed_actor_ids=[P_ID, O_ID],
            value="known-one")
        second = record_relation_change(
            session, actor_id=P_ID, other_actor_id=R_ID,
            relation=REL_TWO, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch3:two", exposed_actor_ids=[P_ID, R_ID],
            value="known-two")
        result, proposal, event_id = later_event(
            owner, session, (focal, O_ID),
            operation_id="r3:ch3:event", proposal_id="r3:ch3:event",
            delta=6)
        event_clock = session.event(event_id)["clock"]
        document = viewer_document(session, P_ID, event_id, event_clock)
        cold = cold_document(str(state), P_ID, event_id, event_clock)
        relations = document["context"]["relation_scope"]["relations"]
        first_relation = relations[0]
        effect = document["context"]["context_effect"]
        access = document["access"]
        relation_keys = sorted(relation["relation_key"] for relation in relations)
        checks = {
            "viewer_does_not_perceive_event": (
                access["status"] == "NOT_PERCEIVED"
                and result.consequences
                and document["context"]["event_access"]["status"]
                == "NOT_PERCEIVED"),
            "prior_relations_qualified": (
                document["history"]["status"] == "QUALIFIED"
                and document["context"]["relation_scope"]["status"]
                == "QUALIFIED"
                and len(relations) == 2),
            "both_relations_present": (
                sorted(relation["relation"] for relation in relations)
                == sorted([REL_ONE, REL_TWO])
                and all(relation["viewer_is_party"] for relation in relations)
                and sorted(relation["counterpart"]["actor_id"]
                           for relation in relations)
                == sorted([O_ID, R_ID])),
            "relation_aware_true_while_event_not_perceived": (
                effect["relation_aware"] is True
                and effect["reason"] == "QUALIFIED_RELATION_CONTEXT"),
            "basis_includes_c12_event_perception_without_own_perception": (
                "C12_EVENT_PERCEPTION" in effect["basis"]
                and access["status"] == "NOT_PERCEIVED"),
            "party_access_flag_false": (
                effect["both_parties_event_access"] is False),
            "plural_output_present": (
                len(document["context"]["relation_scope"]["relations"]) == 2),
            "singular_summary_is_first_sorted": (
                first_relation["relation_key"] == relation_keys[0]
                and effect["relation_status"] == first_relation["status"]
                and effect["relation_value"] == first_relation["value"]
                and effect["representation_depth"]
                == first_relation["representation_depth"]),
            "cold_exact": cold == document,
            "private_state_not_read": (
                document["context"]["private_state"] == "NOT_READ"
                and all(relation["private_state"] == "NOT_READ"
                        for relation in relations)),
        }
        report = {
            "schema": "SOROK_C05_R3_CHALLENGE3@1",
            "source_sha": "5d771dd86767655534b23576075e5da2db4fba78",
            "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
            "event_id": event_id,
            "event_clock": event_clock,
            "relation_one": REL_ONE,
            "relation_two": REL_TWO,
            "document": document,
            "cold": cold,
            "relation_keys": relation_keys,
            "first_relation": first_relation,
            "effect": effect,
            "checks": checks,
            "event_perception_separate_from_relation_knowledge": (
                access["status"] == "NOT_PERCEIVED"
                and document["context"]["relation_scope"]["status"]
                == "QUALIFIED"),
            "basis_actual_defect": (
                "C12_EVENT_PERCEPTION" in effect["basis"]
                and access["status"] == "NOT_PERCEIVED"),
            "plural_actual": {
                "relations": len(relations),
                "summary_selects_first_sorted_key": (
                    first_relation["relation_key"] == relation_keys[0]),
                "summary_is_not_a_salience_rule": True,
            },
            "downstream_c12_event_perception_consumers": [],
            "first_consumer": "read_actor_relative_context",
        }
        path = EVIDENCE / "c05_challenge3_report.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True))
        print(json.dumps({
            "checks": checks,
            "failed": [key for key, value in checks.items() if not value],
            "event_access": access["status"],
            "relation_scope": document["context"]["relation_scope"]["status"],
            "relation_aware": effect["relation_aware"],
            "basis": effect["basis"],
            "plural_relations": [relation["relation"] for relation in relations],
            "summary_relation_status": effect["relation_status"],
            "summary_first_sorted_key": (
                first_relation["relation_key"] == relation_keys[0]),
            "cold_exact": checks["cold_exact"],
            "report": str(path),
        }, indent=2, sort_keys=True))
        return 0 if all(checks.values()) else 2
    finally:
        owner.close()
        fanin.close()


if __name__ == "__main__":
    raise SystemExit(main())
