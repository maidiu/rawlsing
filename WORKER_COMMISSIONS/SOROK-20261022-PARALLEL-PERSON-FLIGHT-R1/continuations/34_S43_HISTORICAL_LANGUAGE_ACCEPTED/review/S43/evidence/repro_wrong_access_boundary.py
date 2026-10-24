import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S43_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s43.bootstrap import install

install()

from language_mediation.plan import competent_languages
from s37.harness import case_for, source_for
from s43.session import S43Session


def _counts(session):
    return {
        "event_count": len(session.read_events()),
        "a_speech": len([
            event for event in session.events()
            if event.get("actor_id") == "A" and event.get("kind") == "SPEECH"
        ]),
        "b_speech": len([
            event for event in session.events()
            if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
        ]),
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s43-wrong-access-"))
    session = S43Session.start(
        root / "state", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        if "es-MX" not in competent_languages(session, "A"):
            session.declare_language_competence("A", "es-MX")
        session.admit_language_encounter(
            text="¿Puedo usar la herramienta?",
            concept_id="concept:request-tool",
            milieu_id="family",
            sense_id="sense:family-request",
            relation_label="AFFIRMED",
            atoms=["TOOL_REQUEST_WORKSHOP"],
            access_declared_branch="other-branch",
        )
        first = session.read_events()[0]
        before = _counts(session)
        result = session.admit_event(
            language_context={"milieu_id": "family"},
            case=case_for(True),
            source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
        )
        event = result["event"]
        denied_id = event["e1_event_id"]
        after = _counts(session)
        read = session.read_s43_event(denied_id)
        report = {
            "schema": "SOROK_S43_WRONG_ACCESS_BOUNDARY@1",
            "before": before,
            "after": after,
            "attempt_status": event.get("attempt_status"),
            "performed": event.get("performed"),
            "language": event.get("language"),
            "s43_refusal": read.get("s43_refusal"),
            "warm_verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()

    cold = S43Session.open(root / "state")
    try:
        cold_read = cold.read_s43_event(denied_id)
        report.update({
            "cold_attempt_status": cold_read.get("attempt_status"),
            "cold_s43_refusal": cold_read.get("s43_refusal"),
            "cold_verify_ok": cold.verify()["ok"],
        })
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
