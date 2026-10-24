"""Explicit invented histories for the S43 consumer/evidence fixtures.

The family/work independence texts are the architecture-05 hypothetical Nadia
example rendered as fabricated TEST_ONLY source events.  No real-person or
demographic inference is made.  Request/refusal/bench encounters provide the
finite generated-intent and ordinary-language repertoire used by S43.
"""
from __future__ import annotations

from .bootstrap import install

install()

from language_mediation.plan import competent_languages  # noqa: E402


def seed_histories(session) -> dict:
    if "es-MX" not in competent_languages(session, "A"):
        session.declare_language_competence("A", "es-MX")

    family_help = session.admit_language_event(
        "A veces hace falta ayuda.", speaker_actor="B"
    )
    work_alone = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B"
    )
    family_independence = session.admit_language_encounter(
        text="Uno se arregla.",
        concept_id="concept:independence",
        milieu_id="family",
        sense_id="sense:family-self-reliance",
        relation_label="AMBIVALENT",
        atoms=["SELF_RELIANCE_FAMILY"],
        counterexample_event_ids=[family_help["event"]["event_id"]],
    )
    work_independence = session.admit_language_encounter(
        text="Aquí nos ayudamos.",
        concept_id="concept:independence",
        milieu_id="work",
        sense_id="sense:work-mutual-aid",
        relation_label="AFFIRMED_FOR_OTHERS",
        atoms=["MUTUAL_AID_WORK"],
        counterexample_event_ids=[work_alone["event"]["event_id"]],
    )

    family_counter = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B"
    )
    work_counter = session.admit_language_event(
        "Aquí no se pide, se hace.", speaker_actor="B"
    )
    family_request = session.admit_language_encounter(
        text="¿Puedo usar la herramienta?",
        concept_id="concept:request-tool",
        milieu_id="family",
        sense_id="sense:family-request",
        relation_label="CONTESTED",
        atoms=["TOOL_REQUEST_WORKSHOP"],
        counterexample_event_ids=[family_counter["event"]["event_id"]],
    )
    work_request = session.admit_language_encounter(
        text="¿Puedo usar la herramienta?",
        concept_id="concept:request-tool",
        milieu_id="workshop",
        sense_id="sense:workshop-request",
        relation_label="AFFIRMED",
        atoms=["TOOL_REQUEST_WORKSHOP"],
        counterexample_event_ids=[work_counter["event"]["event_id"]],
    )
    family_refusal = session.admit_language_encounter(
        text="No, ahora no.",
        concept_id="concept:refusal",
        milieu_id="family",
        sense_id="sense:family-refusal",
        relation_label="AFFIRMED",
        atoms=["EXPLICIT_REFUSAL_NOW"],
    )
    work_refusal = session.admit_language_encounter(
        text="No, ahora no.",
        concept_id="concept:refusal",
        milieu_id="workshop",
        sense_id="sense:workshop-refusal",
        relation_label="AFFIRMED",
        atoms=["EXPLICIT_REFUSAL_NOW"],
    )
    bench = session.admit_language_encounter(
        text="El banco sigue aquí.",
        concept_id="concept:bench",
        milieu_id="public",
        sense_id="sense:bench-present",
        relation_label="AFFIRMED",
        atoms=["BENCH_PRESENT"],
    )
    return {
        "family_independence": family_independence,
        "work_independence": work_independence,
        "family_request": family_request,
        "work_request": work_request,
        "family_refusal": family_refusal,
        "work_refusal": work_refusal,
        "bench": bench,
        "family_help": family_help,
        "work_alone": work_alone,
        "family_counter": family_counter,
        "work_counter": work_counter,
        "family_request_relation": family_request["encounter"]["encounter_id"],
        "work_request_relation": work_request["encounter"]["encounter_id"],
        "family_request_source": family_request["event"]["event_id"],
        "work_request_source": work_request["event"]["event_id"],
        "family_request_receipt": family_request["encounter"]["access_receipt_id"],
        "work_request_receipt": work_request["encounter"]["access_receipt_id"],
        "family_counter_receipt": family_counter["access"]["receipt"]["receipt_id"],
        "work_counter_receipt": work_counter["access"]["receipt"]["receipt_id"],
    }


__all__ = ["seed_histories"]
