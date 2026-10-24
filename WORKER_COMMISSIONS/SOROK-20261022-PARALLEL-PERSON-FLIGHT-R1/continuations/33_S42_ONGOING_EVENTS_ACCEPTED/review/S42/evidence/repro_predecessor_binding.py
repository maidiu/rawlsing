import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S42_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s42.bootstrap import install

install()

from candidate import seal
from c8_readonly_consumer import C8ReadOnlyConsumer
from s41.bindings import binding_episodes as s41_bindings
from s42.bindings import binding_episodes
from s42.session import S42Session
from s37.harness import case_for, source_for

import s42.session as session_module


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s42-predecessor-repro-"))
    session = S42Session.start(
        root / "state", case=case_for(True), source=source_for(case_for(True))
    )
    original = session_module.make_event_binding
    try:
        first = session.read_events()[0]
        second_result = session.admit_event(
            case=case_for(False),
            source=source_for(case_for(False)),
            history_event_refs=(first["e1_event_id"],),
        )
        second = session.read_events()[1]

        def bad_binding(*args, **kwargs):
            binding = original(*args, **kwargs)
            if binding.get("event_ordinal") == 3:
                body = {
                    key: value
                    for key, value in binding.items()
                    if key != "hash"
                }
                body["predecessor"] = dict(s41_bindings(session)[0])
                return seal(body)
            return binding

        session_module.make_event_binding = bad_binding
        try:
            third_result = session.admit_event(
                case=case_for(False),
                source=source_for(case_for(False)),
                history_event_refs=(first["e1_event_id"],),
                event_time=244,
            )
        finally:
            session_module.make_event_binding = original

        third_binding = binding_episodes(session)[-1]
        third_c8 = C8ReadOnlyConsumer(
            third_binding["c8"]["journal_path"]
        ).load().get(third_binding["c8"]["occurrence_id"])
        third_read = session.read_event(third_binding["e1_event_id"])
        report = {
            "schema": "SOROK_S42_PREDECESSOR_REPRO@1",
            "event2_status": second_result["status"],
            "event2_e1_event_id": second["e1_event_id"],
            "actual_predecessor_for_event3": second["e1_event_id"],
            "c8_predecessor_for_event3": (
                (third_c8.get("payload") or {}).get("s42_continuation") or {}
            ).get("predecessor_e1_ref"),
            "persisted_predecessor_for_event3": third_binding["predecessor"][
                "e1_event_id"
            ],
            "event3_status": third_result["status"],
            "event3_read_status": third_read["status"],
            "event3_performed": third_read.get("performed"),
            "warm_verify_ok": session.verify()["ok"],
        }
    finally:
        session_module.make_event_binding = original
        session.close()

    cold = S42Session.open(root / "state")
    try:
        cold_third = cold.read_events()[2]
        report.update(
            {
                "cold_event3_status": cold_third["status"],
                "cold_verify_ok": cold.verify()["ok"],
            }
        )
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
