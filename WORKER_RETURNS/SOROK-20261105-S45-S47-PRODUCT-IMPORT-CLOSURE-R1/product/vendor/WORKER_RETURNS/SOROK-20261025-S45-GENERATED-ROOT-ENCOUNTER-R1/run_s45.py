"""Runnable S45 user encounter over an actual S44 generated root."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s45.session import S45Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _encounter_summary(session):
    return [
        {
            "encounter_id": row.get("encounter_id"),
            "kind": row.get("kind"),
            "status": row.get("status"),
            "strategy": row.get("strategy"),
            "user_event_id": row.get("user_event_id"),
            "speech_event_id": row.get("speech_event_id"),
            "action_event_id": row.get("action_event_id"),
            "native_text": row.get("native_text"),
            "translation_text": row.get("translation_text"),
            "source_event_refs": row.get("source_event_refs"),
            "access_receipt_ids": row.get("access_receipt_ids"),
        }
        for row in session.read_encounters()
    ]


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s45-"))
    state = root / "person"
    case = case_for(True)
    session = S45Session.start(state, case=case, source=source_for(case))
    try:
        root_hash = session.read_root()["root_hash"]
        root_before = session.read_events()[0]
        said = session.say("Can I help?")
        state_after_say = dict(session.world().actor_state["A"])
    finally:
        session.close()

    session = S45Session.open(state)
    try:
        helped = session.do_help()
        state_after_help = dict(session.world().actor_state["A"])
    finally:
        session.close()

    session = S45Session.open(state)
    try:
        attended = session.attend()
        encounters = _encounter_summary(session)
        events = session.read_events()
        root_after = session.read_root()
        verify = session.verify()
        state_after_attend = dict(session.world().actor_state["A"])
        clock = session.clock()
    finally:
        session.close()

    cold = S45Session.open(state)
    try:
        cold_verify = cold.verify()
        cold_encounters = len(cold.read_encounters())
        cold_events = len(cold.read_events())
    finally:
        cold.close()

    report = {
        "schema": "SOROK_S45_GENERATED_ROOT_ENCOUNTER_RUN@1",
        "grade": "TEST_ONLY_SOURCEBOUND_GENERATED_ROOT_ENCOUNTER_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "root_hash": root_hash,
        "root_hash_after": root_after["root_hash"],
        "root_unchanged": root_after["root_hash"] == root_hash,
        "root_event_unchanged": (
            events[0]["e1_event_hash"] == root_before["e1_event_hash"]
        ),
        "events_before": 1,
        "events_after": len(events),
        "encounter_count": len(encounters),
        "encounters": encounters,
        "say": {
            "status": said.get("status"),
            "strategy": said.get("strategy"),
            "native_text": (said.get("language") or {}).get("native_text"),
            "translation_text": (said.get("language") or {}).get("translation_text"),
            "source_event_id": (said.get("language") or {}).get("source_event_id"),
            "surface": said.get("surface"),
        },
        "do_help": {
            "status": helped.get("status"),
            "accepted": helped.get("accepted"),
            "strategy": helped.get("strategy"),
            "action_event_id": (helped.get("admission") or {}).get("action_event_id"),
            "native_text": (helped.get("language") or {}).get("native_text"),
            "translation_text": (helped.get("language") or {}).get("translation_text"),
        },
        "attend": {
            "status": attended.get("status"),
            "new_knowledge": attended.get("new_knowledge"),
            "has_actor_response": bool(attended.get("surface")),
        },
        "material_state_after_say": state_after_say,
        "material_state_after_help": state_after_help,
        "material_state_after_attend": state_after_attend,
        "clock": clock,
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "cold_encounters": cold_encounters,
        "cold_events": cold_events,
        "target_proposals": [],
        "native_grants": {
            "actor": False, "rule": False, "source": False,
            "human": False, "c8": False, "c9": False, "c12": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
