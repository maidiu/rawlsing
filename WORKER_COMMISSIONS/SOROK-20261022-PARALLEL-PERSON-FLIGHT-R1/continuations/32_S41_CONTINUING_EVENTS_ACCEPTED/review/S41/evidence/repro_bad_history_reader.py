import json
import os
import sys
import tempfile
from functools import partial
from pathlib import Path

RETURN = Path(os.environ["S41_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s41.bootstrap import install

install()

import s41.session as session_module
from s41.bindings import binding_episodes
from s41.session import S41Session
from s37.harness import case_for, source_for
from s39.sources import make_source


def bad_history(session, *, first_binding, as_of, original):
    good = original(session, first_binding=first_binding, as_of=as_of)
    content = dict(good["content"])
    content["prior_b_event_hash"] = "0" * 64
    return make_source(
        source_ref="TEST_ONLY_UNRELATED_SELFSEALED",
        source_class=good["source_class"],
        actor_id=good["actor_id"],
        branch_id=good["branch_id"],
        as_of=good["as_of"],
        predicate=good["predicate"],
        value=good["value"],
        content=content,
    )


def main() -> int:
    original = session_module.history_record_from_prior
    root = Path(tempfile.mkdtemp(prefix="s41-bad-history-reader-"))
    session = S41Session.start(
        root / "state", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        first_binding = binding_episodes(session)[0]
        actual_b_hash = first_binding["source"]["b_event_hash"]
        session_module.history_record_from_prior = partial(
            bad_history, original=original
        )
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False))
        )
        first, second = session.read_events()
        second_binding = binding_episodes(session)[1]
        report = {
            "schema": "SOROK_S41_BAD_HISTORY_READER_REPRO@1",
            "actual_first_b_hash": actual_b_hash,
            "continue_status": result["status"],
            "selected_option": second.get("selected_option"),
            "generation_source_refs": second.get("generation_source_refs"),
            "history_source_ref": second_binding["history_source"]["source_ref"],
            "history_b_hash": second_binding["history_source"]["content"][
                "prior_b_event_hash"
            ],
            "warm_read_status": second["status"],
            "first_event_status": first["status"],
            "warm_verify_ok": session.verify()["ok"],
        }
    finally:
        session_module.history_record_from_prior = original
        session.close()

    cold = S41Session.open(root / "state")
    try:
        cold_second = cold.read_events()[1]
        cold_binding = binding_episodes(cold)[1]
        report.update(
            {
                "cold_read_status": cold_second["status"],
                "cold_history_source_ref": cold_binding["history_source"][
                    "source_ref"
                ],
                "cold_verify_ok": cold.verify()["ok"],
            }
        )
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
