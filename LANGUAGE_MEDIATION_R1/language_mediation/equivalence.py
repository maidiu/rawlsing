"""Deterministic, finite equivalence court for native/English artifacts.

This is not a translation-quality score and no model self-judgment is accepted.
It checks exact artifact identity, one shared plan hash, the finite phrase-pair
table, the finite atom universe, and that both artifacts agree on a meaning that
the plan actually authorized.  Unknown phrase/atom or evaluator authority is
UNRESOLVED; matching text that strengthens unauthorized meaning is REJECTED.
"""
from __future__ import annotations

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402

from .artifacts import (  # noqa: E402
    NATIVE_SCHEMA,
    TRANSLATION_SCHEMA,
    artifact_valid,
)
from .atoms import PHRASE_PAIRS, TEST_ONLY_ATOMS  # noqa: E402

RECEIPT_SCHEMA = "LME_EQUIVALENCE_RECEIPT@1"
EVALUATOR = "LME_DETERMINISTIC_FINITE_EQUIVALENCE@1"
EVALUATOR_VERSION = 1
GRADE = "TEST_ONLY_FINITE_EQUIVALENCE_NOT_GENERAL_TRANSLATION"


def _plan_field(plan, name, default=None):
    if isinstance(plan, dict):
        return plan.get(name, default)
    return getattr(plan, name, default)


def _lookup_pair(native: dict, translation: dict,
                 pairs: dict) -> dict | None:
    key = (
        native.get("language_tag"),
        native.get("text"),
        translation.get("target_language_tag"),
    )
    for pair in pairs.values():
        if (pair["native_language"], pair["native_text"],
                pair["target_language"]) == key:
            return pair
    return None


def evaluate_pair(plan, native: dict, translation: dict, *,
                  pairs: dict | None = None,
                  atom_universe=frozenset(TEST_ONLY_ATOMS)) -> dict:
    pairs = PHRASE_PAIRS if pairs is None else pairs
    plan_hash = _plan_field(plan, "plan_hash", "")
    authorized = set(_plan_field(plan, "authorized_atoms", ()) or ())
    checks: dict[str, bool] = {}
    codes: list[str] = []

    checks["native_schema"] = native.get("schema") == NATIVE_SCHEMA
    checks["translation_schema"] = translation.get("schema") == TRANSLATION_SCHEMA
    checks["native_artifact_hash"] = artifact_valid(native)
    checks["translation_artifact_hash"] = artifact_valid(translation)
    checks["native_plan_binding"] = native.get("plan_hash") == plan_hash
    checks["translation_plan_binding"] = translation.get("plan_hash") == plan_hash
    checks["translation_source_binding"] = (
        translation.get("source_artifact_hash") == native.get("artifact_hash")
    )

    structural = all(checks.values())
    pair = None if not structural else _lookup_pair(native, translation, pairs)
    if structural and pair is None:
        return _receipt("UNRESOLVED", ["UNKNOWN_PHRASE_PAIR"],
                        checks, plan, native, translation, authorized, [])

    native_atoms = tuple(sorted(set(native.get("atoms", []) or [])))
    translation_atoms = tuple(sorted(set(translation.get("atoms", []) or [])))
    checks["texts_bind_finite_pair"] = bool(
        pair and native.get("text") == pair["native_text"]
        and translation.get("text") == pair["target_text"]
    )
    checks["atoms_agree"] = native_atoms == translation_atoms
    checks["atoms_known"] = all(
        atom in atom_universe for atom in native_atoms + translation_atoms)

    if not structural:
        if not checks["native_plan_binding"] or not checks["translation_plan_binding"]:
            codes.append("PLAN_HASH_MISMATCH")
        if not checks["translation_source_binding"]:
            codes.append("ARTIFACT_BINDING_MISMATCH")
        if not checks["native_artifact_hash"] or not checks["translation_artifact_hash"]:
            codes.append("ARTIFACT_HASH_INVALID")
        return _receipt("REJECTED", codes or ["ARTIFACT_STRUCTURE_INVALID"],
                        checks, plan, native, translation, authorized,
                        list(native_atoms))

    if not checks["atoms_known"]:
        return _receipt("UNRESOLVED", ["UNKNOWN_SEMANTIC_ATOM"],
                        checks, plan, native, translation, authorized,
                        list(native_atoms))

    if not checks["texts_bind_finite_pair"]:
        codes.append("PHRASE_TEXT_DRIFT")
    base_atoms = set(pair["atoms"])
    if not base_atoms.issubset(set(native_atoms)):
        codes.append("PHRASE_MEANING_DRIFT")
    if not checks["atoms_agree"]:
        codes.append("NATIVE_TRANSLATION_DISAGREE")
    unauthorized = set(native_atoms) - authorized
    if unauthorized:
        # Both artifacts may agree on the stronger meaning; agreement alone is
        # never sufficient.  The pair fails against the unchanged plan.
        codes.append("UNAUTHORIZED_MEANING_STRENGTHENED")
    checks["no_unauthorized_strengthening"] = not unauthorized

    if codes:
        return _receipt("REJECTED", codes, checks, plan, native, translation,
                        authorized, list(native_atoms))
    return _receipt("ACCEPTED", [], checks, plan, native, translation,
                    authorized, list(native_atoms))


def _receipt(status: str, codes: list[str], checks: dict, plan,
             native: dict, translation: dict, authorized: set,
             compared_atoms: list[str]) -> dict:
    plan_hash = _plan_field(plan, "plan_hash", "")
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "status": status,
        "codes": list(codes),
        "checks": dict(checks),
        "evaluator": EVALUATOR,
        "evaluator_version": EVALUATOR_VERSION,
        "plan_hash": plan_hash,
        "native_artifact_hash": native.get("artifact_hash", ""),
        "translation_artifact_hash": translation.get("artifact_hash", ""),
        "compared_atoms": sorted(compared_atoms),
        "authorized_atoms": sorted(authorized),
        "model_self_judgment_used": False,
        "missing_evaluator_authority": False,
        "product_model_calls": 0,
    }
    receipt["receipt_hash"] = digest(receipt)
    return receipt


__all__ = [
    "RECEIPT_SCHEMA",
    "EVALUATOR",
    "EVALUATOR_VERSION",
    "GRADE",
    "evaluate_pair",
]
