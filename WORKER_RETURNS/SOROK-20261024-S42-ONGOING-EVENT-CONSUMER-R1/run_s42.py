"""Minimal runnable S42 variable-length ongoing-event entrypoint."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s42.session import S42Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _summary(row: dict) -> dict:
    language = row.get("language") or {}
    c9 = row.get("c9") or {}
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
        "native_text": language.get("native_text", ""),
        "translation_text": language.get("translation_text", ""),
        "target_branch": c9.get("target_branch"),
        "target_reason": c9.get("target_reason"),
        "target_proposals": c9.get("target_proposals", []),
        "history_refs": row.get("history_refs", []),
        "world_tools_remaining": row.get("world_tools_remaining"),
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s42-"))
    state = root / "person"
    first_case = case_for(True)
    session = S42Session.start(state, case=first_case, source=source_for(first_case))
    session.close()

    # Variable-length stream: event 2 uses event 1; event 3 uses event 1;
    # event 4 uses event 3; event 5 uses event 3. Cold reopen before each call.
    stream = [
        (False, 1),
        (True, 1),
        (False, 3),
        (True, 3),
    ]
    for share, history_ordinal in stream:
        session = S42Session.open(state)
        try:
            events = session.read_events()
            refs = (events[history_ordinal - 1]["e1_event_id"],)
            result = session.admit_event(
                case=case_for(share),
                source=source_for(case_for(share)),
                history_event_refs=refs,
            )
            assert result["status"] == "OK"
        finally:
            session.close()

    final = S42Session.open(state)
    try:
        events = final.read_events()
        latest = final.read_latest()
        verify = final.verify()
        clock = final.clock()
        tools = final.world().actor_state["A"]["tools_remaining"]
        tool_available = final.world().resources["workshop"]["tool_available"]
        root_actors = sorted(final.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(final.product.store.branch(final.branch_id)["actor_ids"])
    finally:
        final.close()

    report = {
        "schema": "SOROK_S42_ONGOING_EVENT_RUN@1",
        "grade": "TEST_ONLY_SOURCEFREE_ONGOING_PERSON_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "root_actors": root_actors,
        "branch_actors": branch_actors,
        "events": [_summary(row) for row in events],
        "latest_ordinal": latest["event_ordinal"],
        "clock": clock,
        "tools_remaining": tools,
        "tool_available": tool_available,
        "verify_ok": verify["ok"],
        "cold_reopen_per_call": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
