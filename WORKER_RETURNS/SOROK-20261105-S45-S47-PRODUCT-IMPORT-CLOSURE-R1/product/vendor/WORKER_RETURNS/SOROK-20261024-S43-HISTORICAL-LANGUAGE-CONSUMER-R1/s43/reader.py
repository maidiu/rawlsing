"""Read S43 source-bound language provenance from the existing S42 event."""
from __future__ import annotations

from .bootstrap import install

install()

from language_mediation.index import LanguageRefusal, build_index  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402

from .errors import S43Refusal  # noqa: E402
from .repertoire import compile_repertoire  # noqa: E402


class S43ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _current_repertoire(session, s43: dict) -> dict:
    try:
        index = build_index(session, actor_id="A")
        current = compile_repertoire(
            session,
            intent=s43.get("intent", ""),
            context=s43.get("context") or {},
            index=index,
        )
        return {
            "currently_available": bool(current.get("available")),
            "current_selected_relation_ids": list(
                current.get("selected_relation_ids") or []
            ),
            "current_contrary_relation_ids": list(
                current.get("contrary_relation_ids") or []
            ),
            "current_invalidated_relation_ids": list(
                current.get("invalidated_relation_ids") or []
            ),
            "current_cache_status": current.get("index_cache_status", ""),
            "current_index_hash": current.get("index_hash", ""),
            "current_index_readset_hash": current.get("index_readset_hash", ""),
        }
    except (LanguageRefusal, S43Refusal) as exc:
        return {
            "currently_available": False,
            "current_refusal": getattr(exc, "code", type(exc).__name__),
        }


def read_s43_event(session, event_ref: str) -> dict:
    base = session.read_event(event_ref)
    if base.get("event_ordinal") == 1:
        return {**base, "s43": None}
    if base.get("status") == "OK" and base.get("attempt_status") == "DENIED":
        binding = next(
            (
                row for row in binding_episodes(session)
                if row.get("e1_event_id") == event_ref
            ),
            None,
        )
        reason = ((binding or {}).get("attempt") or {}).get("reason", "")
        return {**base, "s43": None, "s43_refusal": reason}
    if (
        base.get("status") != "OK"
        or not base.get("performed")
        or base.get("action_event_kind") != "SPEECH"
    ):
        return {**base, "s43": None}
    language = base.get("language") or {}
    event_id = base.get("action_event_id", "")
    admission = session._admission_for(language.get("plan_hash", ""), event_id)
    if not admission:
        raise S43ReadRefusal("S43_ADMISSION_MISSING")
    plan = admission.get("plan") or {}
    readset = plan.get("readset") or {}
    s43 = admission.get("s43")
    if not isinstance(s43, dict):
        raise S43ReadRefusal("S43_REPERTOIRE_BINDING_MISSING")
    summary = readset.get("s43_repertoire") or {}
    if summary.get("repertoire_hash") != s43.get("repertoire_hash"):
        raise S43ReadRefusal("S43_REPERTOIRE_READSET_MISMATCH")
    if plan.get("plan_hash") != language.get("plan_hash"):
        raise S43ReadRefusal("S43_PLAN_HASH_MISMATCH")
    if sorted(plan.get("supporting_relation_ids") or []) != sorted(
        s43.get("selected_relation_ids") or []
    ):
        raise S43ReadRefusal("S43_SUPPORTING_RELATION_MISMATCH")
    if summary.get("private_generation_sources_in_plan") is not False:
        raise S43ReadRefusal("S43_PRIVATE_SOURCES_IN_PLAN")
    source_id = language.get("source_event_id", "")
    source_hash = language.get("source_event_hash", "")
    source_refs = readset.get("source_event_refs") or []
    if not any(
        row.get("event_id") == source_id and row.get("event_hash") == source_hash
        for row in source_refs
    ):
        raise S43ReadRefusal("S43_SOURCE_EVENT_NOT_IN_READSET")
    if language.get("access_receipt_id") not in (
        readset.get("access_receipt_ids") or []
    ):
        raise S43ReadRefusal("S43_ACCESS_RECEIPT_NOT_IN_READSET")
    current = _current_repertoire(session, {
        **s43,
        "intent": summary.get("intent", ""),
        "context": summary.get("context") or s43.get("context") or {},
    })
    return {
        **base,
        "s43": {
            "schema": "S43_HISTORICAL_LANGUAGE_READ@1",
            "repertoire_id": s43.get("repertoire_id", ""),
            "repertoire_hash": s43.get("repertoire_hash", ""),
            "context": dict(s43.get("context") or {}),
            "selected_relation_ids": list(s43.get("selected_relation_ids") or []),
            "selected_relations": list(s43.get("selected_relations") or []),
            "contrary_relation_ids": list(s43.get("contrary_relation_ids") or []),
            "contrary_relations": list(s43.get("contrary_relations") or []),
            "invalidated_relations": list(
                s43.get("invalidated_relations") or []
            ),
            "contradictions": list(s43.get("contradictions") or []),
            "source_event_refs": list(s43.get("source_event_refs") or []),
            "access_receipt_ids": list(s43.get("access_receipt_ids") or []),
            "source_grades": dict(s43.get("source_grades") or {}),
            "invalidated_relation_ids": list(
                readset.get("invalidated_relation_ids") or []
            ),
            "private_generation_sources_in_plan": False,
            **current,
        },
    }


__all__ = ["S43ReadRefusal", "read_s43_event"]
