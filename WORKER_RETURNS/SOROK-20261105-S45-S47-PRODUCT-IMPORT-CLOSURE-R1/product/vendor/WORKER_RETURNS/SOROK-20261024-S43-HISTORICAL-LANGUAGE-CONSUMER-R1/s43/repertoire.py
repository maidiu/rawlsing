"""Bounded source-bound repertoire compiled from the accepted language index.

The repertoire is a derivative readset over existing C12 speech events, access
receipts and encounter episodes.  It is not a second event ledger, not memory,
and not a source of motive, practice or language competence.
"""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import digest  # noqa: E402
from language_mediation.index import LanguageRefusal, build_index  # noqa: E402

from .errors import S43Refusal  # noqa: E402
from .registry import (  # noqa: E402
    GRADE,
    NATIVE_LANGUAGE,
    REGISTRY_HASH,
    pair_for_unit,
    unit_for,
)

SCHEMA = "S43_BOUNDED_HISTORICAL_LANGUAGE_REPERTOIRE@1"
MAX_RELATIONS = 64
MAX_SOURCE_REFS = 128
NOT_AUTHORIZED_FOR = (
    "WHOLE_PERSON_REPLACEMENT",
    "MOTIVE_OR_PRACTICE_CREATION",
    "LANGUAGE_COMPETENCE_INFERENCE",
    "DEMOGRAPHIC_TO_PSYCHE_MAPPING",
    "RECENCY_OR_WEIGHTED_SELECTION",
    "PRIVATE_GENERATION_REASON_DISCLOSURE",
)


def _source_grade(session, event_id: str) -> str:
    event = session.event(event_id)
    if not event:
        return "MISSING_SOURCE_EVENT"
    return str((event.get("body") or {}).get("source_grade", "UNSPECIFIED_SOURCE_GRADE"))


def _ref(row: Mapping[str, Any]) -> dict:
    return {
        "event_id": row.get("event_id", ""),
        "event_hash": row.get("event_hash", ""),
        "branch_id": row.get("branch_id", ""),
    }


def _relation_view(session, row: Mapping[str, Any]) -> dict:
    source = row.get("source_event_ref") or {}
    return {
        "relation_id": row.get("relation_id", ""),
        "concept_id": row.get("concept_id", ""),
        "milieu_id": row.get("milieu_id", ""),
        "sense_id": row.get("sense_id", ""),
        "relation_label": row.get("relation_label", ""),
        "atoms": list(row.get("atoms") or []),
        "language_tag": row.get("language_tag", ""),
        "source_event_ref": _ref(source),
        "access_receipt": dict(row.get("access_receipt") or {}),
        "counterexamples": [dict(item) for item in row.get("counterexamples") or []],
        "epistemic": row.get("epistemic", ""),
        "source_grade": _source_grade(session, source.get("event_id", "")),
        "status": row.get("status", ""),
    }


def _dedupe_refs(rows: list[Mapping[str, Any]]) -> list[dict]:
    seen = set()
    result = []
    for row in rows:
        key = (row.get("event_id", ""), row.get("event_hash", ""),
               row.get("branch_id", ""))
        if not key[0] or key in seen:
            continue
        seen.add(key)
        result.append(dict(row))
    return sorted(result, key=lambda item: (item["event_id"], item["event_hash"]))


def compile_repertoire(
    session,
    *,
    intent: str,
    context: Mapping[str, Any] | None,
    index: Mapping[str, Any] | None = None,
) -> dict:
    if not isinstance(context, Mapping) or not context.get("milieu_id"):
        raise S43Refusal("S43_EXPRESSION_CONTEXT_REQUIRED")
    milieu_id = str(context["milieu_id"])
    unit = unit_for(intent, milieu_id)
    if unit is None:
        raise S43Refusal("S43_EXPRESSION_CONTEXT_UNSUPPORTED",
                         f"{intent}:{milieu_id}")
    if index is None:
        index = build_index(session, actor_id="A")
    pair = pair_for_unit(unit)
    if pair["native_language"] != NATIVE_LANGUAGE:
        raise S43Refusal("S43_LANGUAGE_TAG_UNSUPPORTED", pair["native_language"])

    all_relations = [
        row for row in index.get("relations", [])
        if row.get("concept_id") == unit["concept_id"]
    ]
    if len(all_relations) > MAX_RELATIONS:
        raise S43Refusal("S43_REPERTOIRE_BOUND_EXCEEDED", "relations")

    selected = [
        row for row in all_relations
        if row.get("milieu_id") == unit["milieu_id"]
        and row.get("sense_id") == unit["sense_id"]
        and row.get("language_tag") == pair["native_language"]
        and set(pair["atoms"]).issubset(set(row.get("atoms") or []))
    ]
    selected_ids = sorted(row["relation_id"] for row in selected)
    selected_set = set(selected_ids)
    contrary = [row for row in all_relations if row["relation_id"] not in selected_set]
    invalidated = [
        row for row in index.get("invalidated_relations", [])
        if row.get("concept_id") == unit["concept_id"]
    ]
    contradictions = [
        dict(row) for row in index.get("contradictions_preserved", [])
        if row.get("concept_id") == unit["concept_id"]
    ]

    refs: list[dict] = []
    for row in selected + contrary + invalidated:
        refs.append(_ref(row.get("source_event_ref") or {}))
        refs.extend(_ref(item) for item in row.get("counterexamples") or [])
    refs = _dedupe_refs(refs)
    if len(refs) > MAX_SOURCE_REFS:
        raise S43Refusal("S43_REPERTOIRE_BOUND_EXCEEDED", "source_refs")

    selected_views = [_relation_view(session, row) for row in selected]
    contrary_views = [_relation_view(session, row) for row in contrary]
    invalidated_views = [
        {**_relation_view(session, row), "invalid_reason": row.get("invalid_reason", "")}
        for row in invalidated
    ]
    access_ids = sorted({
        (row.get("access_receipt") or {}).get("receipt_id", "")
        for row in selected + contrary + invalidated
        if (row.get("access_receipt") or {}).get("receipt_id")
    })
    source_grades = {
        row["event_id"]: _source_grade(session, row["event_id"]) for row in refs
    }
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "actor_id": index.get("actor_id", "A"),
        "branch_id": index.get("branch_id", session.branch_id),
        "intent": intent,
        "unit_id": unit["unit_id"],
        "context": {"milieu_id": milieu_id},
        "concept_id": unit["concept_id"],
        "sense_id": unit["sense_id"],
        "language_tag": pair["native_language"],
        "available": bool(selected),
        "reason": "" if selected else "S43_REQUIRED_SOURCE_UNAVAILABLE",
        "selected_relation_ids": selected_ids,
        "selected_relations": selected_views,
        "contrary_relation_ids": sorted(row["relation_id"] for row in contrary),
        "contrary_relations": contrary_views,
        "contradictions": contradictions,
        "invalidated_relation_ids": sorted(
            row["relation_id"] for row in invalidated
        ),
        "invalidated_relations": invalidated_views,
        "source_event_refs": refs,
        "access_receipt_ids": access_ids,
        "source_grades": source_grades,
        "index_hash": index.get("index_hash", ""),
        "index_readset_hash": index.get("readset_hash", ""),
        "index_cache_status": index.get("cache_status", ""),
        "registry_hash": REGISTRY_HASH,
        "maximum_relations": MAX_RELATIONS,
        "maximum_source_refs": MAX_SOURCE_REFS,
        "replaces_person": False,
        "creates_motive": False,
        "creates_practice": False,
        "creates_competence": False,
        "contains_private_generation_reasons": False,
        "contains_weights_or_recency_policy": False,
        "not_authorized_for": list(NOT_AUTHORIZED_FOR),
        "product_model_calls": 0,
    }
    hash_body = dict(body)
    hash_body.pop("index_cache_status", None)
    body["repertoire_hash"] = digest(hash_body)
    body["repertoire_id"] = "S43_REP_" + body["repertoire_hash"][:24].upper()
    return body


__all__ = [
    "SCHEMA", "MAX_RELATIONS", "MAX_SOURCE_REFS", "NOT_AUTHORIZED_FOR",
    "compile_repertoire",
]
