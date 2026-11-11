"""Authorized expression plan over a source-bound historical repertoire."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from language_mediation.plan import (  # noqa: E402
    ExpressionPlan,
    competent_languages,
)

from .errors import S43Refusal  # noqa: E402
from .registry import (  # noqa: E402
    GRADE,
    NATIVE_LANGUAGE,
    REGISTRY_HASH,
    pair_for_unit,
    unit_for,
)
from .repertoire import compile_repertoire  # noqa: E402

PLAN_SCHEMA = "S43_HISTORICAL_LANGUAGE_EXPRESSION_PLAN@1"


def _readset(repertoire: dict, *, index: Mapping[str, Any]) -> dict:
    counterexamples = []
    for row in (
        repertoire.get("selected_relations", [])
        + repertoire.get("contrary_relations", [])
        + repertoire.get("invalidated_relations", [])
    ):
        counterexamples.extend(row.get("counterexamples") or [])
    return {
        "index_hash": index.get("index_hash", ""),
        "index_readset_hash": index.get("readset_hash", ""),
        "index_cache_status": index.get("cache_status", ""),
        "source_event_refs": list(repertoire.get("source_event_refs") or []),
        "access_receipt_ids": list(repertoire.get("access_receipt_ids") or []),
        "counterexamples": sorted(
            counterexamples,
            key=lambda row: (row.get("event_id", ""), row.get("event_hash", "")),
        ),
        "contradictions_preserved": list(repertoire.get("contradictions") or []),
        "invalidated_relation_ids": list(
            repertoire.get("invalidated_relation_ids") or []
        ),
        "s43_repertoire": {
            "schema": repertoire["schema"],
            "repertoire_id": repertoire["repertoire_id"],
            "repertoire_hash": repertoire["repertoire_hash"],
            "context": dict(repertoire["context"]),
            "intent": repertoire["intent"],
            "unit_id": repertoire["unit_id"],
            "selected_relation_ids": list(
                repertoire.get("selected_relation_ids") or []
            ),
            "selected_relations": list(
                repertoire.get("selected_relations") or []
            ),
            "contrary_relation_ids": list(
                repertoire.get("contrary_relation_ids") or []
            ),
            "contrary_relations": list(
                repertoire.get("contrary_relations") or []
            ),
            "contradictions": list(repertoire.get("contradictions") or []),
            "invalidated_relation_ids": list(
                repertoire.get("invalidated_relation_ids") or []
            ),
            "source_grades": dict(repertoire.get("source_grades") or {}),
            "registry_hash": REGISTRY_HASH,
            "index_hash": index.get("index_hash", ""),
            "index_readset_hash": index.get("readset_hash", ""),
            "index_cache_status": index.get("cache_status", ""),
            "source_dependent": True,
            "private_generation_sources_in_plan": False,
            "contains_weights_or_recency_policy": False,
        },
        "language_registry_hash": REGISTRY_HASH,
        "generated_intent": repertoire["intent"],
        "private_generation_sources_in_plan": False,
    }


def compile_historical_plan(
    session,
    *,
    intent: str,
    context: Mapping[str, Any] | None,
    contract: Mapping[str, Any] | None,
    index: Mapping[str, Any],
) -> tuple[ExpressionPlan, dict]:
    languages = competent_languages(session, "A")
    if NATIVE_LANGUAGE not in languages:
        raise S43Refusal("S43_LANGUAGE_COMPETENCE_MISSING", NATIVE_LANGUAGE)
    repertoire = compile_repertoire(
        session, intent=intent, context=context, index=index
    )
    if not repertoire["available"]:
        raise S43Refusal(
            "S43_REQUIRED_SOURCE_UNAVAILABLE",
            f"{intent}:{(context or {}).get('milieu_id', '')}",
        )
    unit = unit_for(intent, str((context or {}).get("milieu_id", "")))
    if unit is None:
        raise S43Refusal("S43_EXPRESSION_CONTEXT_UNSUPPORTED")
    pair = pair_for_unit(unit)
    readset = _readset(repertoire, index=index)
    plan = ExpressionPlan(
        schema=PLAN_SCHEMA,
        grade=GRADE,
        native=False,
        actor_id="A",
        branch_id=session.branch_id,
        unit=unit,
        pair=pair,
        intent=intent,
        authorized_atoms=sorted(pair["atoms"]),
        relation_ids=sorted(
            repertoire.get("selected_relation_ids", [])
            + repertoire.get("contrary_relation_ids", [])
        ),
        supporting_relation_ids=list(repertoire.get("selected_relation_ids") or []),
        readset=readset,
        contract_hash=(contract or {}).get("contract_hash", ""),
        trigger_kind="GENERATED_ATTEMPT",
        trigger_text="",
        fallback=False,
        fallback_reason="",
        requested_unit_id=unit["unit_id"],
    )
    plan._seal()
    return plan, repertoire


__all__ = ["PLAN_SCHEMA", "compile_historical_plan"]
