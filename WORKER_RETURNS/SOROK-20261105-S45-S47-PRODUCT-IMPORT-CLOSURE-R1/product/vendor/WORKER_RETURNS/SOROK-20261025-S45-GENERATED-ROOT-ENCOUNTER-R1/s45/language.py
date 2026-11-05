"""Finite source-bound HELP language plans over S44's admitted root evidence."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from language_mediation.index import build_index  # noqa: E402
from language_mediation.plan import ExpressionPlan  # noqa: E402

from .errors import S45Refusal  # noqa: E402

GRADE = "TEST_ONLY_S45_HISTORICAL_HELP_LANGUAGE_NOT_GENERAL_TRANSLATION"
NATIVE = "es-MX"
TARGET = "en"

PAIRS: dict[str, dict] = {
    "help_invite_1": {
        "native_text": "Si te ofreces, el borde cercano necesita una mano.",
        "target_text": "If you're offering, the near edge needs a hand.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_INVITE",),
    },
    "help_invite_2": {
        "native_text": "Puedes sostener el borde cercano si lo dices en serio.",
        "target_text": "You can hold the near edge if you mean it.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_INVITE",),
    },
    "help_accept_1": {
        "native_text": "Sostén el borde cercano. Revisaré la costura.",
        "target_text": "Hold the near edge. I'll check the seam.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_ACCEPT",),
    },
    "help_accept_2": {
        "native_text": "Pon la mano en el borde cercano. Yo tomo la holgura.",
        "target_text": "Put your hand on the near edge. I'll take the slack.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_ACCEPT",),
    },
    "help_invite_refuse_1": {
        "native_text": "No puedo tomar eso ahora. Tengo que terminar.",
        "target_text": "I can't take that on now. I have to finish.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_REFUSE",),
    },
    "help_refuse_time_1": {
        "native_text": "No puedo tomar eso ahora. Tengo que terminar.",
        "target_text": "I can't take that on now. I have to finish.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_REFUSE",),
    },
    "help_refuse_time_2": {
        "native_text": "Hoy no. El mercado cierra.",
        "target_text": "Not today. The market closes.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_REFUSE",),
    },
    "help_refuse_material_1": {
        "native_text": "Me quedé sin material. No puedo empezar eso ahora.",
        "target_text": "I'm out of material. I can't start that now.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_REFUSE",),
    },
    "help_refuse_material_2": {
        "native_text": "La herramienta no está. Hoy no puedo hacerlo.",
        "target_text": "The tool's gone. I can't do it today.",
        "native_language": "es-MX",
        "target_language": "en",
        "atoms": ("HELP_REFUSE",),
    },
}

UNITS: dict[str, dict] = {
    key: {
        "unit_id": "S45_" + key.upper(),
        "intent": key,
        "concept_id": (
            "concept:help-invite" if key.startswith("help_invite")
            else "concept:help-accept" if key.startswith("help_accept")
            else "concept:help-refuse"
        ),
        "milieu_id": "workshop",
        "sense_id": "sense:workshop-" + key.replace("_", "-"),
        "atoms": pair["atoms"],
        "template_id": key,
    }
    for key, pair in PAIRS.items()
}
ATOMS = frozenset({"HELP_INVITE", "HELP_ACCEPT", "HELP_REFUSE"})


def unit_for_candidate(candidate: Mapping[str, Any]) -> dict:
    template_id = candidate.get("template_id", "")
    unit = UNITS.get(template_id)
    if unit is None:
        raise S45Refusal("S45_HELP_LANGUAGE_MEANING_UNSUPPORTED", str(template_id))
    if candidate.get("strategy") not in {"HELP_INVITE", "HELP_ACCEPT", "HELP_REFUSE"}:
        raise S45Refusal("S45_HELP_LANGUAGE_MEANING_UNSUPPORTED",
                         str(candidate.get("strategy")))
    return dict(unit)


def pair_for(unit: Mapping[str, Any]) -> dict:
    return dict(PAIRS[unit["template_id"]])


def compile_help_plan(session, candidate: Mapping[str, Any],
                      contract: Mapping[str, Any] | None = None):
    unit = unit_for_candidate(candidate)
    pair = pair_for(unit)
    index = build_index(session, actor_id="A")
    relations = [
        row for row in index.get("relations", [])
        if row.get("concept_id") == unit["concept_id"]
        and row.get("milieu_id") == unit["milieu_id"]
        and row.get("sense_id") == unit["sense_id"]
        and row.get("language_tag") == NATIVE
        and set(pair["atoms"]).issubset(set(row.get("atoms") or []))
    ]
    if not relations:
        raise S45Refusal("S45_LANGUAGE_SOURCE_UNAVAILABLE", unit["sense_id"])
    source_refs = []
    access_ids = []
    counterexamples = []
    for row in relations:
        source_refs.append(row["source_event_ref"])
        access_ids.append(row["access_receipt"]["receipt_id"])
        counterexamples.extend(row.get("counterexamples", []))
    contradictions = [
        row for row in index.get("contradictions_preserved", [])
        if row.get("concept_id") == unit["concept_id"]
    ]
    readset = {
        "index_hash": index["index_hash"],
        "index_readset_hash": index["readset_hash"],
        "source_event_refs": source_refs,
        "access_receipt_ids": sorted(set(access_ids)),
        "counterexamples": counterexamples,
        "contradictions_preserved": contradictions,
        "invalidated_relation_ids": [],
        "s45": {
            "schema": "S45_HELP_LANGUAGE_READSET@1",
            "strategy": candidate.get("strategy"),
            "template_id": unit["template_id"],
            "concept_id": unit["concept_id"],
            "milieu_id": unit["milieu_id"],
            "sense_id": unit["sense_id"],
            "atoms": list(pair["atoms"]),
            "private_generation_sources_in_plan": False,
        },
        "private_generation_sources_in_plan": False,
    }
    plan = ExpressionPlan(
        schema="LME_ACTOR_EXPRESSION_PLAN@1",
        grade=GRADE,
        native=False,
        actor_id="A",
        branch_id=session.branch_id,
        unit={
            **unit,
            "pair_id": unit["template_id"],
            "source_dependent": True,
            "gesture": candidate.get("gesture", ""),
            "tone": candidate.get("tone", "ordinary"),
        },
        pair={
            "native_language": NATIVE,
            "native_text": pair["native_text"],
            "target_language": TARGET,
            "target_text": pair["target_text"],
            "atoms": pair["atoms"],
        },
        intent=str(candidate.get("strategy")),
        authorized_atoms=sorted(pair["atoms"]),
        relation_ids=sorted(row["relation_id"] for row in relations),
        supporting_relation_ids=sorted(row["relation_id"] for row in relations),
        readset=readset,
        contract_hash=(contract or {}).get("contract_hash", ""),
        trigger_kind="USER_ENCOUNTER",
        trigger_text="",
        fallback=False,
        fallback_reason="",
        requested_unit_id=unit["unit_id"],
    )
    plan._seal()
    index_ref = {
        "index_hash": index["index_hash"],
        "readset_hash": index["readset_hash"],
        "cache_status": index["cache_status"],
    }
    return plan, index_ref


__all__ = [
    "GRADE", "PAIRS", "UNITS", "ATOMS", "unit_for_candidate", "pair_for",
    "compile_help_plan",
]
