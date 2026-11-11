"""S40-owned finite language registry and authorized generated-intent plan."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import digest, seal  # noqa: E402
from language_mediation.artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from language_mediation.plan import (  # noqa: E402
    ExpressionPlan,
    competent_languages,
)

GRADE = "TEST_ONLY_S40_GENERATED_INTENT_LANGUAGE_MODEL_PREMISE_NOT_GENERAL_TRANSLATION"
REGISTRY_SCHEMA = "S40_FINITE_GENERATED_INTENT_LANGUAGE_REGISTRY@1"
REGISTRY_VERSION = "1"
NATIVE_LANGUAGE = "es-MX"
TARGET_LANGUAGE = "en"

S40_ATOMS = frozenset({"TOOL_REQUEST_WORKSHOP", "EXPLICIT_REFUSAL_NOW"})

S40_PAIRS = {
    "pair_s40_request_tool": {
        "native_language": NATIVE_LANGUAGE,
        "native_text": "¿Puedo usar la herramienta?",
        "target_language": TARGET_LANGUAGE,
        "target_text": "May I use the tool?",
        "atoms": ("TOOL_REQUEST_WORKSHOP",),
    },
    "pair_s40_explicit_refusal": {
        "native_language": NATIVE_LANGUAGE,
        "native_text": "No, ahora no.",
        "target_language": TARGET_LANGUAGE,
        "target_text": "No, not now.",
        "atoms": ("EXPLICIT_REFUSAL_NOW",),
    },
}

S40_UNITS = {
    "REQUEST_TOOL": {
        "unit_id": "S40_REQUEST_TOOL",
        "intent": "REQUEST_TOOL",
        "pair_id": "pair_s40_request_tool",
        "source_dependent": False,
        "concept_id": None,
        "milieu_id": None,
        "sense_id": None,
        "gesture": "A turns toward the bench.",
        "tone": "ordinary",
    },
    "EXPLICIT_REFUSAL": {
        "unit_id": "S40_EXPLICIT_REFUSAL",
        "intent": "EXPLICIT_REFUSAL",
        "pair_id": "pair_s40_explicit_refusal",
        "source_dependent": False,
        "concept_id": None,
        "milieu_id": None,
        "sense_id": None,
        "gesture": "A raises one hand slightly.",
        "tone": "plain",
    },
}


class S40LanguageRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def registry_document() -> dict:
    body = {
        "schema": REGISTRY_SCHEMA,
        "version": REGISTRY_VERSION,
        "grade": GRADE,
        "native": False,
        "model_premise": True,
        "phrase_pairs": S40_PAIRS,
        "atom_universe": sorted(S40_ATOMS),
    }
    return seal(body)


S40_REGISTRY_HASH = registry_document()["hash"]


def _ensure_competence(session) -> None:
    if session.meta.get("s40_language_competence_allowed") is False:
        raise S40LanguageRefusal("S40_LANGUAGE_COMPETENCE_MISSING")
    if NATIVE_LANGUAGE not in competent_languages(session, "A"):
        session.declare_language_competence("A", NATIVE_LANGUAGE)


def _source_for_intent(session, intent: str) -> dict:
    if intent not in S40_UNITS:
        raise S40LanguageRefusal("S40_INTENT_NOT_IN_LANGUAGE_REGISTRY", intent)
    unit = S40_UNITS[intent]
    pair = S40_PAIRS[unit["pair_id"]]
    source = session.admit_language_event(
        pair["native_text"],
        speaker_actor="B",
        language_tag=NATIVE_LANGUAGE,
        record_access=True,
    )
    return {
        "event": source["event"],
        "access": source["access"],
        "receipt": source["access"]["receipt"],
    }


def make_plan(
    session,
    *,
    intent: str,
    contract: Mapping[str, Any],
    generation_receipt: Mapping[str, Any],
    source_event: Mapping[str, Any],
    access_receipt: Mapping[str, Any],
    e1_identity: Mapping[str, Any],
) -> ExpressionPlan:
    if intent not in S40_UNITS:
        raise S40LanguageRefusal("S40_INTENT_NOT_IN_LANGUAGE_REGISTRY", intent)
    unit = S40_UNITS[intent]
    pair = S40_PAIRS[unit["pair_id"]]
    source_refs = [{
        "event_id": source_event["event_id"],
        "event_hash": source_event["hash"],
        "branch_id": session.branch_id,
    }]
    access_ids = [access_receipt["receipt_id"]]
    index_hash = digest({
        "schema": REGISTRY_SCHEMA,
        "version": REGISTRY_VERSION,
        "registry_hash": S40_REGISTRY_HASH,
        "intent": intent,
        "source_event_refs": source_refs,
        "access_receipt_ids": access_ids,
    })
    readset = {
        "index_hash": index_hash,
        "index_readset_hash": index_hash,
        "source_event_refs": source_refs,
        "access_receipt_ids": access_ids,
        "counterexamples": [],
        "contradictions_preserved": [],
        "invalidated_relation_ids": [],
        "public_outward_facts": [
            {
                "kind": "ADMITTED_E1",
                "event_id": e1_identity["event_id"],
                "event_hash": e1_identity["event_hash"],
                "c8_occurrence_id": e1_identity["c8_occurrence_id"],
                "c8_state_digest": e1_identity["c8_state_digest"],
            },
            {
                "kind": "OBJECTIVE_TOOL_STATE",
                "tool_available": bool(
                    (generation_receipt.get("world_prerequisites") or {}).get(
                        "tool_available"
                    )
                ),
            },
        ],
        "language_registry_hash": S40_REGISTRY_HASH,
        "generated_intent": intent,
    }
    plan = ExpressionPlan(
        schema="LME_ACTOR_EXPRESSION_PLAN@1",
        grade=GRADE,
        native=False,
        actor_id="A",
        branch_id=session.branch_id,
        unit=unit,
        pair=pair,
        intent=intent,
        authorized_atoms=sorted(pair["atoms"]),
        relation_ids=[],
        supporting_relation_ids=[],
        readset=readset,
        contract_hash=contract.get("contract_hash", ""),
        trigger_kind="GENERATED_ATTEMPT",
        trigger_text="",
        fallback=False,
        fallback_reason="",
        requested_unit_id=unit["unit_id"],
    )
    plan._seal()
    return plan


def realize_speaking(
    session,
    *,
    attempt_request: Mapping[str, Any],
    generation_receipt: Mapping[str, Any],
    contract: Mapping[str, Any],
    e1_identity: Mapping[str, Any],
) -> dict:
    intent = attempt_request["option_id"]
    _ensure_competence(session)
    source = _source_for_intent(session, intent)
    plan = make_plan(
        session,
        intent=intent,
        contract=contract,
        generation_receipt=generation_receipt,
        source_event=source["event"],
        access_receipt=source["receipt"],
        e1_identity=e1_identity,
    )
    native = build_native_artifact(plan)
    translation = build_translation_artifact(plan, native)
    receipt = evaluate_pair(
        plan, native, translation, pairs=S40_PAIRS, atom_universe=S40_ATOMS
    )
    if receipt.get("status") != "ACCEPTED":
        raise S40LanguageRefusal(
            "S40_EQUIVALENCE_REJECTED",
            ",".join(receipt.get("codes", [])),
        )

    world = session.world()
    candidate = session._candidate(plan, native)
    admission_id = digest({
        "candidate": candidate,
        "contract_hash": contract.get("contract_hash", ""),
        "plan_hash": plan.plan_hash,
        "native_artifact_hash": native["artifact_hash"],
        "translation_artifact_hash": translation["artifact_hash"],
        "clock": world.clock,
    })
    event = session._write_speech_event(
        plan, native, translation, receipt, contract, candidate, admission_id
    )
    index = {
        "index_hash": plan.readset["index_hash"],
        "readset_hash": plan.readset["index_readset_hash"],
        "cache_status": "S40_FINITE_REGISTRY",
    }
    admission = session._admission(
        plan, native, translation, receipt, contract, event,
        candidate, admission_id, index,
    )
    session.product._append_episode(
        session.branch_id, "A", "SAY", world.clock,
        {
            "event_id": event["event_id"],
            "text": native["text"],
            "language_tag": native["language_tag"],
            "gesture": candidate["gesture"],
            "tone": candidate["tone"],
            "strategy": candidate["strategy"],
            "contract_hash": contract.get("contract_hash", ""),
            "admission_id": admission_id,
            "plan_hash": plan.plan_hash,
            "spans": event["body"]["spans"],
        },
    )
    session.product._append_episode(
        session.branch_id, "A", "EXPRESSION_ADMISSION", world.clock,
        {
            "admission": admission,
            "candidate": candidate,
            "plan": plan.public(),
            "contract_hash": contract.get("contract_hash", ""),
            "multilingual_port": {
                "schema": "S40_GENERATED_INTENT_LANGUAGE_PORT@1",
                "version": 1,
            },
        },
    )
    projection = session._write_translation_projection(
        event, plan, native, translation, receipt
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    binding = seal({
        "schema": "S40_GENERATED_LANGUAGE_BINDING@1",
        "grade": GRADE,
        "provenance": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "native": False,
        "intent": intent,
        "language_tag": native["language_tag"],
        "target_language_tag": translation["target_language_tag"],
        "native_text": native["text"],
        "translation_text": translation["text"],
        "plan_hash": plan.plan_hash,
        "contract_hash": contract.get("contract_hash", ""),
        "native_artifact_hash": native["artifact_hash"],
        "translation_artifact_hash": translation["artifact_hash"],
        "equivalence_receipt_hash": receipt["receipt_hash"],
        "equivalence_status": receipt["status"],
        "equivalence_codes": list(receipt.get("codes", [])),
        "source_event_id": source["event"]["event_id"],
        "source_event_hash": source["event"]["hash"],
        "access_receipt_id": source["receipt"]["receipt_id"],
        "speech_event_id": event["event_id"],
        "speech_event_hash": event["hash"],
        "admission_id": admission_id,
        "projection_episode_id": projection["episode_id"],
        "language_registry_hash": S40_REGISTRY_HASH,
        "atom_universe_hash": digest(sorted(S40_ATOMS)),
        "private_generation_sources_in_plan": False,
        "e1_event_id": e1_identity["event_id"],
        "e1_event_hash": e1_identity["event_hash"],
        "target_proposals": [],
    })
    return {
        "event": event,
        "language": binding,
        "plan": plan,
        "native": native,
        "translation": translation,
        "equivalence": receipt,
        "admission": admission,
        "projection": projection,
        "source": source,
    }


__all__ = [
    "GRADE",
    "NATIVE_LANGUAGE",
    "REGISTRY_SCHEMA",
    "REGISTRY_VERSION",
    "S40_ATOMS",
    "S40_PAIRS",
    "S40_REGISTRY_HASH",
    "S40_UNITS",
    "S40LanguageRefusal",
    "make_plan",
    "realize_speaking",
    "registry_document",
]
