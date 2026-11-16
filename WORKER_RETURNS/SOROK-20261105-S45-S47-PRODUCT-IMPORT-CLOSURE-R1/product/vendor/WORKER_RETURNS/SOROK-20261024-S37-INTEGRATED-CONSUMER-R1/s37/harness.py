"""Focused TEST_ONLY helpers shared by S37 tests and evidence."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

import firstclass  # noqa: E402
from candidate import CandidateStore, digest, seal  # noqa: E402
from r31j.scenarios import evaluated  # noqa: E402

from .producer import IntegratedProducer  # noqa: E402
from .session import S37IntegratedSession  # noqa: E402

TRIGGER = "What do you say when things get hard?"
NATIVE_SELF = "Uno se arregla."
NATIVE_BENCH = "El banco sigue aquí."


def case_for(share: bool) -> dict:
    return evaluated(share=share, e2=False)["case"]


def source_for(case: Mapping[str, Any]) -> dict:
    return firstclass.source_from_case(dict(case))


def start_session(state_root, *, share: bool, variant: str = "A_REPAIR_LONG"):
    case = case_for(share)
    source = source_for(case)
    return S37IntegratedSession.start(
        state_root, case=case, source=source, variant=variant
    )


def setup_neutral_language(session) -> None:
    session.declare_language_competence("A", "es-MX")
    session.enable_mediation(trigger_kinds=("SAY",))


def setup_source_language(session) -> dict:
    session.declare_language_competence("A", "es-MX")
    counter_help = session.admit_language_event(
        "A veces hace falta ayuda.", speaker_actor="B"
    )
    counter_alone = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B"
    )
    family = session.admit_language_encounter(
        text=NATIVE_SELF,
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
    return {
        "family": family,
        "work": work,
        "counter_help": counter_help,
        "counter_alone": counter_alone,
        "enabled": enabled,
        "family_receipt": family["encounter"]["access_receipt_id"],
        "work_receipt": work["encounter"]["access_receipt_id"],
        "family_relation": family["encounter"]["encounter_id"],
        "work_relation": work["encounter"]["encounter_id"],
        "family_source": family["event"]["event_id"],
        "work_source": work["event"]["event_id"],
    }


def producer_for(state_root, *, share: bool, variant: str = "A_REPAIR_LONG"):
    case = case_for(share)
    source = source_for(case)
    producer = IntegratedProducer(
        state_root, case=case, source=source, variant=variant
    )
    producer.stage_m35()
    return producer, case, source


def fresh_store(path) -> CandidateStore:
    return CandidateStore(path)


def reseal_with(record: Mapping[str, Any], **changes: Any) -> dict:
    body = {key: value for key, value in record.items() if key != "hash"}
    body.update(changes)
    return seal(body)


def summary(session) -> dict:
    read = session.read_s36()
    world = session.world()
    return {
        "session_class": type(session).__name__,
        "case": session.meta.get("case"),
        "source_operation": session.meta["source"]["b_operation"],
        "source_b_event_hash": session.meta["source"]["b_event_hash"],
        "source_actor_map": session.meta["source_actor_map"],
        "c8_occurrence_id": session.meta["c8"]["occurrence_id"],
        "c8_state_digest": session.meta["c8"]["c8_state_digest"],
        "e1_event_id": session.meta["c8"]["e1_event_id"],
        "e1_event_hash": session.meta["c8"]["e1_event_hash"],
        "tools_remaining": world.actor_state["A"].get("tools_remaining"),
        "tool_available": world.resources["workshop"].get("tool_available"),
        "response_ref": read["response_ref"],
        "response_receipt_hash": read["response_receipt_hash"],
        "c9_receipt_hash": read["c9_receipt_hash"],
        "outcome": read["outcome"],
        "response_kind": read["response_kind"],
        "target_branch": read["target_branch"],
        "target_reason": read["target_reason"],
        "target_id": read["target_id"],
        "target_proposals": read["target_proposals"],
        "target_state_rows": read["target_state_rows"],
        "s35_receipt_hash": read["s35_receipt"].get("hash"),
        "access_source_ref": read["s35_receipt"].get("access_source_ref"),
        "response_source_ref": read["s35_receipt"].get("response_source_ref"),
        "native": read["native"],
    }


__all__ = [
    "NATIVE_BENCH",
    "NATIVE_SELF",
    "TRIGGER",
    "case_for",
    "digest",
    "fresh_store",
    "producer_for",
    "reseal_with",
    "setup_neutral_language",
    "setup_source_language",
    "source_for",
    "start_session",
    "summary",
]
