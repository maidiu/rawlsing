"""Documented CLI demo for the TEST_ONLY language-mediation slice.

Run from the worker root:

  PYTHONPATH=LANGUAGE_MEDIATION_R1 \
    python3 -m language_mediation.cli demo

The demo admits two invented source encounters to the real C12 store, declares
explicit test-only competence, compiles a plan before wording, admits exact
native speech through the real writer, attaches a labeled English view and
cold-reopens the state.  It makes zero product-model/provider calls.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .session import MediatedJoinedSession

TRIGGER = "What do you say when things get hard?"


def _dump(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _fixture(state: Path):
    session = MediatedJoinedSession.start(state, perform="omit")
    session.declare_language_competence("A", "es-MX")
    counter_help = session.admit_language_event(
        "A veces hace falta ayuda.", speaker_actor="B")
    counter_alone = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B")
    family = session.admit_language_encounter(
        text="Uno se arregla.",
        concept_id="concept:independence",
        milieu_id="family",
        sense_id="sense:family-self-reliance",
        relation_label="AMBIVALENT",
        atoms=["SELF_RELIANCE_FAMILY"],
        counterexample_event_ids=[counter_help["event"]["event_id"]],
    )
    work = session.admit_language_encounter(
        text="Aquí nos ayudamos.",
        concept_id="concept:independence",
        milieu_id="work",
        sense_id="sense:work-mutual-aid",
        relation_label="AFFIRMED_FOR_OTHERS",
        atoms=["MUTUAL_AID_WORK"],
        counterexample_event_ids=[counter_alone["event"]["event_id"]],
    )
    enabled = session.enable_mediation(trigger_kinds=("SAY",))
    return session, family, work, counter_help, counter_alone, enabled


def _demo(state_root: Path | None) -> dict:
    if state_root is not None:
        state = Path(state_root)
    else:
        state = Path(tempfile.mkdtemp(prefix="lme-demo-")) / "state"
    session, family, work, counter_help, counter_alone, enabled = _fixture(state)
    index = session.language_index()
    said = session.say(TRIGGER)
    event_id = said["admission"]["speech_event_id"]
    view_en = session.language_view(event_id, locale="en")
    view_es = session.language_view(event_id, locale="es")
    view_dual = session.language_view(event_id, locale="dual")
    event_before = session.event(event_id)
    session_hash = said["admission"]["speech_event_hash"]
    session.close()

    cold = MediatedJoinedSession.open(state)
    cold_event = cold.event(event_id)
    cold_view = cold.language_view(event_id, locale="en")
    cold_index = cold.language_index()
    cold_status = cold.status()
    cold.close()

    return {
        "schema": "LME_CLI_DEMO@1",
        "grade": "TEST_ONLY_SOURCEFREE_LANGUAGE_MEDIATION_NOT_NATIVE",
        "state_root": str(state),
        "binding": enabled["binding"],
        "index": {
            "index_hash": index["index_hash"],
            "readset_hash": index["readset_hash"],
            "cache_status": index["cache_status"],
            "relation_count": len(index["relations"]),
            "contradictions_preserved": index["contradictions_preserved"],
            "counterexamples_preserved": index["counterexamples_preserved"],
            "invalidated_relations": index["invalidated_relations"],
        },
        "source_events": {
            "family_encounter": family["encounter"],
            "work_encounter": work["encounter"],
            "counterexample_help": counter_help["event"]["event_id"],
            "counterexample_alone": counter_alone["event"]["event_id"],
        },
        "say": {
            "strategy": said["strategy"],
            "speech": said["candidate"]["speech"],
            "surface": said["surface"],
            "admission_id": said["admission"]["admission_id"],
            "speech_event_id": event_id,
            "speech_event_hash": said["admission"]["speech_event_hash"],
            "plan_hash": said["language"]["plan"]["plan_hash"],
            "native_artifact_hash": said["language"]["native_artifact"][
                "artifact_hash"],
            "translation_artifact_hash": said["language"][
                "translation_artifact"]["artifact_hash"],
            "equivalence": said["language"]["equivalence"],
            "source_dependent_refused": said["language"][
                "source_dependent_refused"],
            "product_model_calls": 0,
        },
        "views": {"en": view_en, "es": view_es, "dual": view_dual},
        "event_immutable_after_views": event_before["hash"] == session_hash,
        "cold_reopen": {
            "event_hash_equal": cold_event["hash"] == session_hash,
            "view": cold_view,
            "index_cache_status": cold_index["cache_status"],
            "index_readset_hash": cold_index["readset_hash"],
            "status": cold_status,
        },
        "product_model_calls": 0,
    }


def _open(args) -> MediatedJoinedSession:
    return MediatedJoinedSession.open(args.state)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo")
    demo.add_argument("--state", default=None)

    inspect = sub.add_parser("inspect")
    inspect.add_argument("--state", required=True)

    say = sub.add_parser("say")
    say.add_argument("--state", required=True)
    say.add_argument("text")

    view = sub.add_parser("view")
    view.add_argument("--state", required=True)
    view.add_argument("--event", required=True)
    view.add_argument("--locale", default="en")
    view.add_argument("--fail-translation", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            _dump(_demo(args.state))
            return 0
        session = _open(args)
        try:
            if args.command == "inspect":
                _dump({
                    "status": session.status(),
                    "index": session.language_index(),
                    "events": session.events(),
                    "episodes": session.episodes(),
                })
            elif args.command == "say":
                _dump(session.say(args.text))
            elif args.command == "view":
                _dump(session.language_view(
                    args.event, locale=args.locale,
                    fail_translation=args.fail_translation))
            else:
                parser.error("unknown command")
                return 2
        finally:
            session.close()
        return 0
    except Exception as exc:
        _dump({"status": "REFUSED", "code": getattr(exc, "code", ""),
               "error": type(exc).__name__ + ":" + str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
