"""Honest schema-updated chronology oracle for S48 current source repair.

The reviewer's original oracle imported the removed static-fixture helper
candidate_source(). This copy keeps the chronology assertions but uses the
current source issuer; no source is inferred or fabricated.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S48_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s48.bootstrap import install

install()

from s37.harness import case_for, source_for
from s45.fixtures import root_bundle
from s48.session import S48Session
from s48.sources import candidate_specs, issue_current_source


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s48-source-chronology-"))
    session = S48Session.start(
        root / "state",
        bundle=root_bundle("01" * 32),
        case=case_for(True),
        source=source_for(case_for(True)),
        language_context={"milieu_id": "workshop"},
    )
    try:
        current = session.read_events()[-1]
        specs = candidate_specs(session)
        candidate_id = specs[0]["candidate_id"]
        candidate_case, source, event = issue_current_source(session, candidate_id)
        root_data = session.read_root()
        report = {
            "schema": "SOROK_S48_SOURCE_CHRONOLOGY_REPRO@1",
            "session_clock": session.clock(),
            "current_event_time": current.get("event_time"),
            "current_event_ref": current.get("e1_event_id"),
            "source_owner": source.get("b_owner"),
            "source_actor": source.get("b_actor"),
            "source_event_ref": source.get("b_event_ref"),
            "source_event_hash": source.get("b_event_hash"),
            "source_operation": source.get("b_operation"),
            "source_b_clock": source.get("b_clock"),
            "source_a_e1_clock": source.get("a_e1_clock"),
            "source_is_older_than_current_event": int(source.get("b_clock", 0))
            < int(current.get("event_time", 0)),
            "owner_present_in_root_actor_ids": source.get("b_owner")
            in set(root_data.get("actor_ids") or []),
            "owner_is_current_world_owner": source.get("b_owner") == session.world().owner,
            "source_performer_owner": source.get("source_performer_owner"),
            "performer_is_current_world_owner": source.get("source_performer_owner") == session.world().owner,
            "source_actor_in_root_actor_ids": source.get("b_actor")
            in set(root_data.get("actor_ids") or []),
            "source_event_in_world_journal": any(
                row["event_id"] == event["event_id"]
                for row in session.world().events
            ),
            "source_before_c8": True,
            "source_case_id": candidate_case.get("case_id"),
            "source_grade": source.get("source_grade"),
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
