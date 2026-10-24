"""Finite TEST_ONLY expressive registry for generated request/refusal language.

These are explicit test fixtures, not a lexicon, translation system, demographic
mapping or claim about any real person's speech.  The registry only names the
small set of generated intents and context-scoped senses this slice evaluates.
"""
from __future__ import annotations

from .bootstrap import install

install()

from candidate import seal  # noqa: E402

SCHEMA = "S43_FINITE_EXPRESSIVE_REPERTOIRE_REGISTRY@1"
VERSION = "1"
GRADE = "TEST_ONLY_S43_FINITE_EXPRESSIVE_REGISTRY_NOT_GENERAL_TRANSLATION"
NATIVE_LANGUAGE = "es-MX"
TARGET_LANGUAGE = "en"

ATOMS = frozenset({
    "TOOL_REQUEST_WORKSHOP",
    "EXPLICIT_REFUSAL_NOW",
    "BENCH_PRESENT",
})

PAIRS = {
    "pair_s43_request_tool": {
        "native_language": NATIVE_LANGUAGE,
        "native_text": "¿Puedo usar la herramienta?",
        "target_language": TARGET_LANGUAGE,
        "target_text": "May I use the tool?",
        "atoms": ("TOOL_REQUEST_WORKSHOP",),
    },
    "pair_s43_explicit_refusal": {
        "native_language": NATIVE_LANGUAGE,
        "native_text": "No, ahora no.",
        "target_language": TARGET_LANGUAGE,
        "target_text": "No, not now.",
        "atoms": ("EXPLICIT_REFUSAL_NOW",),
    },
    "pair_s43_ordinary_bench": {
        "native_language": NATIVE_LANGUAGE,
        "native_text": "El banco sigue aquí.",
        "target_language": TARGET_LANGUAGE,
        "target_text": "The bench is still here.",
        "atoms": ("BENCH_PRESENT",),
    },
}

UNITS = {
    "S43_REQUEST_TOOL_FAMILY": {
        "unit_id": "S43_REQUEST_TOOL_FAMILY",
        "intent": "REQUEST_TOOL",
        "pair_id": "pair_s43_request_tool",
        "source_dependent": True,
        "concept_id": "concept:request-tool",
        "milieu_id": "family",
        "sense_id": "sense:family-request",
        "gesture": "A turns slightly toward the workbench.",
        "tone": "ordinary",
    },
    "S43_REQUEST_TOOL_WORK": {
        "unit_id": "S43_REQUEST_TOOL_WORK",
        "intent": "REQUEST_TOOL",
        "pair_id": "pair_s43_request_tool",
        "source_dependent": True,
        "concept_id": "concept:request-tool",
        "milieu_id": "workshop",
        "sense_id": "sense:workshop-request",
        "gesture": "A keeps a hand near the bench edge.",
        "tone": "ordinary",
    },
    "S43_EXPLICIT_REFUSAL_FAMILY": {
        "unit_id": "S43_EXPLICIT_REFUSAL_FAMILY",
        "intent": "EXPLICIT_REFUSAL",
        "pair_id": "pair_s43_explicit_refusal",
        "source_dependent": True,
        "concept_id": "concept:refusal",
        "milieu_id": "family",
        "sense_id": "sense:family-refusal",
        "gesture": "A raises one hand slightly.",
        "tone": "plain",
    },
    "S43_EXPLICIT_REFUSAL_WORK": {
        "unit_id": "S43_EXPLICIT_REFUSAL_WORK",
        "intent": "EXPLICIT_REFUSAL",
        "pair_id": "pair_s43_explicit_refusal",
        "source_dependent": True,
        "concept_id": "concept:refusal",
        "milieu_id": "workshop",
        "sense_id": "sense:workshop-refusal",
        "gesture": "A keeps both hands on the bench.",
        "tone": "plain",
    },
    "S43_ORDINARY_BENCH": {
        "unit_id": "S43_ORDINARY_BENCH",
        "intent": "ORDINARY_GREETING",
        "pair_id": "pair_s43_ordinary_bench",
        "source_dependent": True,
        "concept_id": "concept:bench",
        "milieu_id": "public",
        "sense_id": "sense:bench-present",
        "gesture": "A rests one hand on the bench.",
        "tone": "ordinary",
    },
}


def registry_document() -> dict:
    return seal({
        "schema": SCHEMA,
        "version": VERSION,
        "grade": GRADE,
        "native": False,
        "model_premise": True,
        "phrase_pairs": PAIRS,
        "unit_library": UNITS,
        "atom_universe": sorted(ATOMS),
    })


REGISTRY_HASH = registry_document()["hash"]


def unit_for(intent: str, milieu_id: str) -> dict | None:
    for unit in UNITS.values():
        if unit["intent"] == intent and unit["milieu_id"] == milieu_id:
            return dict(unit)
    return None


def pair_for_unit(unit: dict) -> dict:
    return dict(PAIRS[unit["pair_id"]])


def available_contexts(intent: str) -> list[str]:
    return sorted(
        unit["milieu_id"] for unit in UNITS.values()
        if unit["intent"] == intent
    )


__all__ = [
    "SCHEMA", "VERSION", "GRADE", "NATIVE_LANGUAGE", "TARGET_LANGUAGE",
    "ATOMS", "PAIRS", "UNITS", "REGISTRY_HASH", "registry_document",
    "unit_for", "pair_for_unit", "available_contexts",
]
