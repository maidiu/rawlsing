"""Minimal runnable S41 two-event continuing-person entrypoint."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s41.session import S41Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s41-"))
    state = root / "person"
    first_case = case_for(True)
    session = S41Session.start(state, case=first_case, source=source_for(first_case))
    try:
        first = session.read_events()[0]
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
    finally:
        session.close()

    session = S41Session.open(state)
    try:
        second_case = case_for(False)
        result = session.continue_event(
            case=second_case, source=source_for(second_case)
        )
        events = session.read_events()
        latest = session.read_latest()
        verify = session.verify()
        clock = session.clock()
        tools = session.world().actor_state["A"]["tools_remaining"]
        tool_available = session.world().resources["workshop"]["tool_available"]
    finally:
        session.close()

    cold = S41Session.open(state)
    try:
        cold_events = cold.read_events()
        cold_verify = cold.verify()
    finally:
        cold.close()

    def summary(row):
        return {
            "event_ordinal": row["event_ordinal"],
            "status": row["status"],
            "e1_event_id": row["e1_event_id"],
            "e1_event_hash": row["e1_event_hash"],
            "c8_occurrence_id": row["c8_occurrence_id"],
            "source_operation": row["source_operation"],
            "event_time": row["event_time"],
            "selected_option": row.get("selected_option"),
            "attempt_status": row.get("attempt_status"),
            "performed": row.get("performed"),
            "action_event_id": row.get("action_event_id", ""),
            "native_text": (row.get("language") or {}).get("native_text", ""),
            "translation_text": (row.get("language") or {}).get("translation_text", ""),
            "target_branch": (row.get("c9") or {}).get("target_branch"),
            "target_reason": (row.get("c9") or {}).get("target_reason"),
            "target_proposals": (row.get("c9") or {}).get("target_proposals", []),
            "history_predicate": row.get("history_predicate"),
            "generation_source_refs": row.get("generation_source_refs", []),
        }

    report = {
        "schema": "SOROK_S41_CONTINUING_PERSON_RUN@1",
        "grade": "TEST_ONLY_SOURCEFREE_CONTINUING_PERSON_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "root_actors": root_actors,
        "events": [summary(row) for row in events],
        "latest_ordinal": latest["event_ordinal"],
        "continue_status": result["status"],
        "actor_action_appended": result["actor_action_appended"],
        "clock": clock,
        "tools_remaining": tools,
        "tool_available": tool_available,
        "verify_ok": verify["ok"],
        "cold": {
            "events": [summary(row) for row in cold_events],
            "latest_ordinal": cold_events[-1]["event_ordinal"],
            "verify_ok": cold_verify["ok"],
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
