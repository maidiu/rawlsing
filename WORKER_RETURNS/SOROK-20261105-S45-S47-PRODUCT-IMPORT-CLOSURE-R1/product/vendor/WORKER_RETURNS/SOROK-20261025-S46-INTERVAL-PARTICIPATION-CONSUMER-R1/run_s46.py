"""Runnable S46 actual interval participation on the generated-root person."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s46.bootstrap import install  # noqa: E402

install()

from s37.harness import case_for, source_for  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s46.session import S46Session  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s46-"))
    state = root / "person"
    case = case_for(True)
    session = S46Session.start(
        state, bundle=root_bundle("01" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )
    try:
        root_hash = session.read_root()["root_hash"]
        before = session.world_prerequisites()
        before_b = dict(session.world().actor_state["B"])
        domain = make_domain(mode="ACTUAL", start=session.clock(),
                             end=session.clock() + 4)
        produced = session.produce_interval(domain)
        after = session.world_prerequisites()
        said = session.say("Can I help?")
        helped = session.do_help()
        attended = session.attend()
        events = session.read_events()
        first = events[0]
        later = session.admit_event(
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
            event_time=session.clock() + 1,
        )
        world_readset = binding_episodes(session)[-1].get(
            "generation", {}
        ).get("world_prerequisites", {})
        verify = session.verify()
        interval_read = session.read_interval_states()[-1]
        scenes = [
            {"kind": row.get("kind"), "status": row.get("status")}
            for row in session.read_encounters()
        ]
        after_b = dict(session.world().actor_state["B"])
    finally:
        session.close()

    cold = S46Session.open(state)
    try:
        cold_state = cold.read_interval_states()[-1]
        cold_verify = cold.verify()
        cold_root = cold.read_root()["root_hash"]
    finally:
        cold.close()

    report = {
        "schema": "SOROK_S46_INTERVAL_PARTICIPATION_RUN@1",
        "grade": "TEST_ONLY_S46_ACTUAL_INTERVAL_PARTICIPATION_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "root_hash": root_hash,
        "root_hash_after": cold_root,
        "root_unchanged": cold_root == root_hash,
        "domain": {
            "domain_id": domain["domain_id"],
            "mode": domain["mode"],
            "start": domain["start"],
            "end": domain["end"],
            "segments": domain["segments"],
            "model_hash": domain["model_hash"],
        },
        "interval": {
            "state_id": produced["state_id"],
            "status": produced["status"],
            "coverage": produced["coverage"],
            "segment_statuses": [row["status"] for row in produced["segments"]],
            "action_event_ids": [
                row["world"]["actual_action_event_id"]
                for row in produced["segments"]
            ],
            "actual_daily_events_invented": produced["actual_daily_events_invented"],
            "actor_knowledge_inferred": produced["actor_knowledge_inferred"],
            "psychology_state_written": produced["psychology_state_written"],
        },
        "world_prerequisites_before": before,
        "world_prerequisites_after": after,
        "s42_generation_world": world_readset,
        "same_scene_sequence": [
            {"kind": first.get("action_event_kind") or "SPEECH",
             "status": first.get("status")},
        ] + scenes,
        "s45": {
            "say_status": said.get("status"),
            "do_help_status": helped.get("status"),
            "do_help_accepted": helped.get("accepted"),
            "do_help_strategy": helped.get("strategy"),
            "attend_status": attended.get("status"),
        },
        "later_s42": {
            "status": later.get("status"),
            "selected_option": later["event"].get("selected_option"),
            "attempt_status": later["event"].get("attempt_status"),
            "performed": later["event"].get("performed"),
        },
        "other_actor_preserved": before_b == after_b,
        "cold_interval": {
            "status": cold_state["status"],
            "coverage": cold_state["coverage"],
            "currentness": cold_state["currentness"],
        },
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "target_proposals": [],
        "native_grants": {
            "actor": False, "rule": False, "source": False, "human": False,
            "c8": False, "c9": False, "c12": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
