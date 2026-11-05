"""Runnable S44 generated antecedent root consumed by the actual S43 person."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s44.bundle import default_bundle  # noqa: E402
from s44.session import S44Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _summary(result):
    read = result["event"]
    language = read.get("language") or {}
    c9 = read.get("c9") or {}
    return {
        "event_ordinal": read["event_ordinal"],
        "status": read.get("status"),
        "selected_option": read.get("selected_option"),
        "attempt_status": read.get("attempt_status"),
        "performed": read.get("performed"),
        "native_text": language.get("native_text", ""),
        "translation_text": language.get("translation_text", ""),
        "source_event_id": language.get("source_event_id", ""),
        "target_branch": c9.get("target_branch"),
        "target_reason": c9.get("target_reason"),
        "target_proposals": c9.get("target_proposals"),
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s44-"))
    state = root / "person"
    case = case_for(True)
    session = S44Session.start(
        state,
        bundle=default_bundle(root_seed="11" * 32),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )
    try:
        root_read = session.read_root()
        first = session.read_events()[0]
        events = session.read_events()
        second = session.admit_event(
            language_context={"milieu_id": "workshop"},
            case=case_for(True),
            source=source_for(case_for(True)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        second_read = session.read_s43_event(second["event"]["e1_event_id"])
        verify = session.verify()
        root_hash = root_read["root_hash"]
        actor_ids = root_read["actor_ids"]
        root_language = root_read["language_evidence"]
    finally:
        session.close()

    cold = S44Session.open(state)
    try:
        cold_root = cold.read_root()
        events = cold.read_events()
        third = cold.admit_event(
            language_context={"milieu_id": "workshop"},
            case=case_for(True),
            source=source_for(case_for(True)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        cold_verify = cold.verify()
        final_events = cold.read_events()
        latest = cold.read_latest()
        clock = cold.clock()
        tools = cold.world().actor_state["A"]["tools_remaining"]
    finally:
        cold.close()

    report = {
        "schema": "SOROK_S44_SAMPLED_ROOT_RUN@1",
        "grade": "TEST_ONLY_SOURCEFREE_SAMPLED_ROOT_CONSUMER_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "root_hash": root_hash,
        "root_id": root_read["root_id"],
        "bundle_hash": root_read["bundle_hash"],
        "actor_ids": actor_ids,
        "source_hashes": root_read["source_hashes"],
        "root_event_refs": root_read["event_refs"],
        "root_snapshot_hashes": root_read["snapshot_hashes"],
        "root_draw_receipt_count": len(root_read["draw_receipts"]),
        "root_selected_branches": root_read["selected_branches"],
        "root_language_evidence": root_language,
        "first_event": {
            "event_ordinal": first["event_ordinal"],
            "status": first.get("status"),
            "selected_option": first.get("selected_option"),
            "e1_event_hash": first["e1_event_hash"],
            "source_event_id": (first.get("language") or {}).get(
                "source_event_id", ""
            ),
            "source_is_root_evidence": (
                (first.get("language") or {}).get("source_event_id")
                in {row["source_event_id"] for row in root_language}
            ),
        },
        "second_event": _summary(second),
        "second_s43": {
            "status": second_read.get("status"),
            "selected_relation_ids": (second_read.get("s43") or {}).get(
                "selected_relation_ids", []
            ),
            "repertoire_hash": (second_read.get("s43") or {}).get(
                "repertoire_hash", ""
            ),
        },
        "cold_reopen_root_same": cold_root["root_hash"] == root_hash,
        "cold_reopen_actor_ids_same": cold_root["actor_ids"] == actor_ids,
        "third_event": _summary(third),
        "event_count": len(final_events),
        "latest_ordinal": latest["event_ordinal"],
        "clock": clock,
        "tools_remaining": tools,
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "selected_finished_life": False,
        "target_proposals": [],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
