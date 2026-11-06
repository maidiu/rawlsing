"""Runnable S43 historical-language consumer over one continuing S42 person."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s43.fixtures import seed_histories  # noqa: E402
from s43.session import S43Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _admit(session, *, context, share, history_ordinal=1):
    events = session.read_events()
    return session.admit_event(
        language_context={"milieu_id": context},
        case=case_for(share),
        source=source_for(case_for(share)),
        history_event_refs=(events[history_ordinal - 1]["e1_event_id"],),
    )


def _event_summary(session, result):
    read = session.read_s43_event(result["event"]["e1_event_id"])
    language = read.get("language") or {}
    s43 = read.get("s43") or {}
    return {
        "event_ordinal": read["event_ordinal"],
        "status": read["status"],
        "selected_option": read.get("selected_option"),
        "attempt_status": read.get("attempt_status"),
        "performed": read.get("performed"),
        "native_text": language.get("native_text", ""),
        "translation_text": language.get("translation_text", ""),
        "plan_hash": language.get("plan_hash", ""),
        "source_event_id": language.get("source_event_id", ""),
        "access_receipt_id": language.get("access_receipt_id", ""),
        "retrieved_from_history": True,
        "repertoire_id": s43.get("repertoire_id", ""),
        "repertoire_hash": s43.get("repertoire_hash", ""),
        "context": s43.get("context"),
        "selected_relation_ids": s43.get("selected_relation_ids", []),
        "contrary_relation_ids": s43.get("contrary_relation_ids", []),
        "source_grades": s43.get("source_grades", {}),
        "currently_available": s43.get("currently_available"),
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s43-"))
    state = root / "person"
    first_case = case_for(True)
    session = S43Session.start(
        state, case=first_case, source=source_for(first_case)
    )
    histories = seed_histories(session)
    session.close()

    summaries = []
    session = S43Session.open(state)
    try:
        summaries.append(_event_summary(session, _admit(session, context="family", share=True)))
    finally:
        session.close()

    session = S43Session.open(state)
    try:
        summaries.append(_event_summary(session, _admit(session, context="workshop", share=False)))
    finally:
        session.close()

    session = S43Session.open(state)
    try:
        summaries.append(_event_summary(session, _admit(session, context="family", share=True)))
        index = session.language_index()
        verify = session.verify()
        events = session.read_events()
        clock = session.clock()
        tools = session.world().actor_state["A"]["tools_remaining"]
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(session.product.store.branch(session.branch_id)["actor_ids"])
        views = {
            row["event_ordinal"]: session.language_view(row["action_event_id"], locale="en")
            for row in events if row.get("performed") and row.get("action_event_id")
        }
    finally:
        session.close()

    report = {
        "schema": "SOROK_S43_HISTORICAL_LANGUAGE_RUN@1",
        "grade": "TEST_ONLY_SOURCEFREE_HISTORICAL_LANGUAGE_CONSUMER_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "histories": {
            "family_independence_relation": histories["family_independence"]["encounter"]["encounter_id"],
            "work_independence_relation": histories["work_independence"]["encounter"]["encounter_id"],
            "family_request_relation": histories["family_request_relation"],
            "work_request_relation": histories["work_request_relation"],
        },
        "index_relations": len(index["relations"]),
        "index_contradictions": len(index["contradictions_preserved"]),
        "index_cache_status": index["cache_status"],
        "events": summaries,
        "views": views,
        "clock": clock,
        "tools_remaining": tools,
        "root_actors": root_actors,
        "branch_actors": branch_actors,
        "verify_ok": verify["ok"],
        "cold_reopen_per_admission": True,
        "private_generation_sources_in_plan": False,
        "target_proposals": [],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
