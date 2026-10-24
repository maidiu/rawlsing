"""Finite authorized actor expression plan compiled before any wording."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402

from .atoms import (  # noqa: E402
    FALLBACK_UNIT_ID,
    UNIT_LIBRARY,
    choose_intent,
    pair_for_unit,
    unit_for_intent,
)
from .index import LanguageRefusal  # noqa: E402

PLAN_SCHEMA = "LME_ACTOR_EXPRESSION_PLAN@1"
COMPETENCE_SCHEMA = "LME_LANGUAGE_COMPETENCE_DECLARATION@1"
GRADE = "TEST_ONLY_SOURCEFREE_ACTOR_EXPRESSION_PLAN"
FORBIDDEN_COMPETENCE_KEYS = frozenset({
    "ethnicity", "race", "nationality", "birth_language", "mother_tongue",
    "native_language_from_demographics", "accent", "genetic_language",
})


@dataclass
class ExpressionPlan:
    schema: str
    grade: str
    native: bool
    actor_id: str
    branch_id: str
    unit: dict
    pair: dict
    intent: str
    authorized_atoms: list[str]
    relation_ids: list[str]
    supporting_relation_ids: list[str]
    readset: dict
    contract_hash: str
    trigger_kind: str
    trigger_text: str
    fallback: bool
    fallback_reason: str
    requested_unit_id: str
    product_model_calls: int = 0
    plan_hash: str = field(default="")

    def public(self) -> dict:
        return {
            "schema": self.schema,
            "grade": self.grade,
            "native": self.native,
            "plan_hash": self.plan_hash,
            "actor_id": self.actor_id,
            "branch_id": self.branch_id,
            "unit": {
                "unit_id": self.unit["unit_id"],
                "intent": self.unit["intent"],
                "language_tag": self.pair["native_language"],
                "native_text": self.pair["native_text"],
                "english_text": self.pair["target_text"],
                "atoms": list(self.authorized_atoms),
                "source_dependent": bool(self.unit["source_dependent"]),
            },
            "intent": self.intent,
            "authorized_atoms": list(self.authorized_atoms),
            "relation_ids": list(self.relation_ids),
            "supporting_relation_ids": list(self.supporting_relation_ids),
            "readset": self.readset,
            "contract_hash": self.contract_hash,
            "trigger": {
                "kind": self.trigger_kind,
                "text": self.trigger_text,
            },
            "fallback": self.fallback,
            "fallback_reason": self.fallback_reason,
            "requested_unit_id": self.requested_unit_id,
            "product_model_calls": self.product_model_calls,
        }

    def _seal(self) -> None:
        body = self.public()
        body.pop("plan_hash", None)
        self.plan_hash = digest(body)


def competent_languages(session, actor_id: str = "A") -> set[str]:
    languages: set[str] = set()
    for episode in session.episodes():
        if episode.get("kind") != "LANGUAGE_COMPETENCE":
            continue
        body = episode.get("body", {})
        if any(key in FORBIDDEN_COMPETENCE_KEYS for key in body):
            raise LanguageRefusal(
                "COMPETENCE_DEMOGRAPHIC_INFERENCE_REFUSED",
                episode.get("episode_id", ""))
        if body.get("actor_id") != actor_id:
            continue
        if body.get("basis") != "EXPLICIT_TEST_ONLY_DECLARATION":
            continue
        if body.get("language_tag"):
            languages.add(body["language_tag"])
    return languages


def _readset(index: dict, relations: list[dict], invalidated: list[dict],
             *, concept_id: str) -> dict:
    source_refs = []
    access_ids = []
    counterexamples = []
    for relation in relations:
        source_refs.append(relation["source_event_ref"])
        access_ids.append(relation["access_receipt"]["receipt_id"])
        counterexamples.extend(relation.get("counterexamples", []))
    contradictions = [
        group for group in index.get("contradictions_preserved", [])
        if group.get("concept_id") == concept_id
    ]
    return {
        "index_hash": index["index_hash"],
        "index_readset_hash": index["readset_hash"],
        "source_event_refs": sorted(
            source_refs, key=lambda row: (row.get("event_id", ""),
                                          row.get("event_hash", ""))),
        "access_receipt_ids": sorted(set(access_ids)),
        "counterexamples": sorted(
            counterexamples, key=lambda row: (row.get("event_id", ""),
                                              row.get("event_hash", ""))),
        "contradictions_preserved": contradictions,
        "invalidated_relation_ids": sorted(
            row.get("relation_id", "") for row in invalidated),
    }


def _relation_matches(relation: dict, unit: dict) -> bool:
    return (
        relation.get("concept_id") == unit.get("concept_id")
        and relation.get("milieu_id") == unit.get("milieu_id")
        and relation.get("sense_id") == unit.get("sense_id")
    )


def compile_plan(session, index: dict, contract: dict, *,
                 trigger_kind: str, trigger_text: str = "") -> ExpressionPlan:
    actor_id = "A"
    branch_id = session.branch_id
    languages = competent_languages(session, actor_id)
    requested_intent = choose_intent(trigger_text)
    requested_unit = unit_for_intent(requested_intent) or UNIT_LIBRARY[FALLBACK_UNIT_ID]

    if requested_unit["source_dependent"]:
        required_language = pair_for_unit(requested_unit)["native_language"]
        if required_language not in languages:
            raise LanguageRefusal(
                "LANGUAGE_COMPETENCE_UNKNOWN",
                f"{actor_id}:{required_language}")

    supporting = [row for row in index.get("relations", [])
                  if _relation_matches(row, requested_unit)]
    fallback = False
    fallback_reason = ""
    supported_unit = requested_unit
    supporting_ids = [row["relation_id"] for row in supporting]
    if requested_unit["source_dependent"] and not supporting:
        fallback = True
        fallback_reason = "SOURCE_DEPENDENT_UNIT_UNAVAILABLE"
        supported_unit = UNIT_LIBRARY[FALLBACK_UNIT_ID]
        supporting = []
        supporting_ids = []

    safe_language = pair_for_unit(supported_unit)["native_language"]
    if safe_language not in languages:
        raise LanguageRefusal(
            "LANGUAGE_COMPETENCE_UNKNOWN",
            f"{actor_id}:{safe_language}")

    pair = pair_for_unit(supported_unit)
    concept_id = supported_unit.get("concept_id") or ""
    if concept_id:
        readset_relations = [
            row for row in index.get("relations", [])
            if row.get("concept_id") == concept_id
        ]
        readset_invalidated = [
            row for row in index.get("invalidated_relations", [])
            if row.get("concept_id") == concept_id
        ]
    else:
        readset_relations = []
        readset_invalidated = []
    readset = _readset(index, readset_relations, readset_invalidated,
                       concept_id=concept_id)

    plan = ExpressionPlan(
        schema=PLAN_SCHEMA,
        grade=GRADE,
        native=False,
        actor_id=actor_id,
        branch_id=branch_id,
        unit=supported_unit,
        pair=pair,
        intent=supported_unit["intent"],
        authorized_atoms=sorted(pair["atoms"]),
        relation_ids=sorted(row["relation_id"] for row in readset_relations),
        supporting_relation_ids=sorted(supporting_ids),
        readset=readset,
        contract_hash=contract.get("contract_hash", ""),
        trigger_kind=trigger_kind,
        trigger_text=trigger_text,
        fallback=fallback,
        fallback_reason=fallback_reason,
        requested_unit_id=requested_unit["unit_id"],
    )
    plan._seal()
    return plan


__all__ = [
    "PLAN_SCHEMA",
    "COMPETENCE_SCHEMA",
    "GRADE",
    "ExpressionPlan",
    "competent_languages",
    "compile_plan",
]
