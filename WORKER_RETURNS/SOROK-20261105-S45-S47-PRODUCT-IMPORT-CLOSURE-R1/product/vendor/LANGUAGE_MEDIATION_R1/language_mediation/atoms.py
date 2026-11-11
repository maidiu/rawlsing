"""Finite TEST_ONLY semantic atoms, phrase pairs and plan units.

Nothing here is a general lexicon, a language-competence model or a claim about
a real person.  The evaluator may only reason over these explicit atoms and
phrase pairs.  An atom or phrase outside this table is UNRESOLVED.
"""
from __future__ import annotations

TEST_ONLY_ATOMS = frozenset({
    "BENCH_PRESENT",
    "SELF_RELIANCE_FAMILY",
    "MUTUAL_AID_WORK",
    "CERTAINTY",
})

PHRASE_PAIRS: dict[str, dict] = {
    "pair_bench": {
        "native_language": "es-MX",
        "native_text": "El banco sigue aquí.",
        "target_language": "en",
        "target_text": "The bench is still here.",
        "atoms": ("BENCH_PRESENT",),
    },
    "pair_self_reliance": {
        "native_language": "es-MX",
        "native_text": "Uno se arregla.",
        "target_language": "en",
        "target_text": "You handle it yourself.",
        "atoms": ("SELF_RELIANCE_FAMILY",),
    },
    "pair_mutual_aid": {
        "native_language": "es-MX",
        "native_text": "Aquí nos ayudamos.",
        "target_language": "en",
        "target_text": "Here we help each other.",
        "atoms": ("MUTUAL_AID_WORK",),
    },
}

UNIT_LIBRARY: dict[str, dict] = {
    "SAFE_BENCH": {
        "unit_id": "SAFE_BENCH",
        "intent": "SAFE_GREETING",
        "pair_id": "pair_bench",
        "source_dependent": False,
        "concept_id": None,
        "milieu_id": None,
        "sense_id": None,
        "gesture": "A keeps one hand on the bench.",
        "tone": "ordinary",
    },
    "SELF_RELIANCE": {
        "unit_id": "SELF_RELIANCE",
        "intent": "SELF_RELIANCE",
        "pair_id": "pair_self_reliance",
        "source_dependent": True,
        "concept_id": "concept:independence",
        "milieu_id": "family",
        "sense_id": "sense:family-self-reliance",
        "gesture": "A does not look up from the bench.",
        "tone": "plain",
    },
    "MUTUAL_AID": {
        "unit_id": "MUTUAL_AID",
        "intent": "MUTUAL_AID",
        "pair_id": "pair_mutual_aid",
        "source_dependent": True,
        "concept_id": "concept:independence",
        "milieu_id": "work",
        "sense_id": "sense:work-mutual-aid",
        "gesture": "A tilts the piece toward the near edge.",
        "tone": "practical",
    },
}

# A bounded, documented trigger classifier.  It does not read persona, history
# or demographics; it only selects an intent from the current user text.
INTENT_RULES = (
    (("alone", "yourself", "self", "hard", "family", "steady"), "SELF_RELIANCE"),
    (("help", "together", "neighbor", "aid", "work"), "MUTUAL_AID"),
)
FALLBACK_UNIT_ID = "SAFE_BENCH"


def choose_intent(text: str) -> str:
    low = (text or "").lower()
    for words, intent in INTENT_RULES:
        if any(word in low for word in words):
            return intent
    return "SAFE_GREETING"


def unit_for_intent(intent: str) -> dict | None:
    for unit in UNIT_LIBRARY.values():
        if unit["intent"] == intent:
            return unit
    return None


def pair_for_unit(unit: dict) -> dict:
    return PHRASE_PAIRS[unit["pair_id"]]


__all__ = [
    "TEST_ONLY_ATOMS",
    "PHRASE_PAIRS",
    "UNIT_LIBRARY",
    "INTENT_RULES",
    "FALLBACK_UNIT_ID",
    "choose_intent",
    "unit_for_intent",
    "pair_for_unit",
]
