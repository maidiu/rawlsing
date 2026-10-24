"""Derived actor+branch language-relation index over the real C12 store.

The index contains references and hashes only.  It never copies psychological
state, remembers for the actor, or turns an encounter into competence.  Every
relation must name an exact world SPEECH event, an explicit access receipt and
a real perception row on the same branch.  A bad hash or foreign branch is a
hard refusal; missing/revoked access invalidates only that relation before any
actor wording claim is admitted.
"""
from __future__ import annotations

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402

INDEX_SCHEMA = "LME_ACTOR_LANGUAGE_RELATION_INDEX@1"
ENCOUNTER_SCHEMA = "LME_LANGUAGE_ENCOUNTER@1"
ACCESS_SCHEMA = "LME_SOURCE_ACCESS@1"
GRADE = "TEST_ONLY_DERIVED_LANGUAGE_CACHE_NOT_PSYCHOLOGY"
NOT_AUTHORIZED_FOR = (
    "CAN008_CAUSAL_RULE",
    "CAN011_DURABLE_WRITE",
    "ACTOR_HIDDEN_SELF_TRUTH",
    "LANGUAGE_COMPETENCE_FROM_DEMOGRAPHICS",
    "USER_FACING_PRIVATE_PSYCHOLOGY",
)


class LanguageRefusal(SessionRefusal):
    """Typed refusal raised before an actor claim is admitted."""


def event_hash_valid(event: dict) -> bool:
    if not isinstance(event, dict):
        return False
    stored = event.get("hash")
    if not stored:
        return False
    body = {key: value for key, value in event.items() if key != "hash"}
    return digest(body) == stored


def _episodes(session, kind: str) -> list[dict]:
    return [row for row in session.episodes() if row.get("kind") == kind]


def _receipts(episodes: list[dict]) -> dict[str, dict]:
    receipts: dict[str, dict] = {}
    for episode in episodes:
        kind = episode.get("kind")
        body = episode.get("body", {})
        if kind == "LANGUAGE_ACCESS":
            receipt = body.get("receipt") or body
            receipt_id = receipt.get("receipt_id")
            if not receipt_id:
                continue
            receipts[receipt_id] = {
                **receipt,
                "status": "GRANTED",
                "episode_id": episode.get("episode_id", ""),
            }
        elif kind == "LANGUAGE_ACCESS_REVOKED":
            receipt_id = body.get("receipt_id")
            if receipt_id in receipts:
                receipts[receipt_id]["status"] = "REVOKED"
                receipts[receipt_id]["changed_by"] = episode.get("episode_id", "")
                receipts[receipt_id]["change_reason"] = body.get("reason", "")
        elif kind == "LANGUAGE_ACCESS_RESTORED":
            receipt_id = body.get("receipt_id")
            if receipt_id in receipts:
                receipts[receipt_id]["status"] = "GRANTED"
                receipts[receipt_id]["changed_by"] = episode.get("episode_id", "")
                receipts[receipt_id]["change_reason"] = body.get("reason", "")
    return receipts


def _validate_source(session, branch_id: str, event_id: str,
                     expected_hash: str = "") -> dict:
    event = session.product.store.world_event(branch_id, event_id)
    if event is None:
        raise LanguageRefusal("SOURCE_EVENT_MISSING", event_id)
    if not event_hash_valid(event):
        raise LanguageRefusal("SOURCE_EVENT_HASH_MISMATCH", event_id)
    if expected_hash and event.get("hash") != expected_hash:
        raise LanguageRefusal("SOURCE_EVENT_HASH_MISMATCH", event_id)
    if event.get("kind") != "SPEECH":
        raise LanguageRefusal("SOURCE_EVENT_NOT_SPEECH", event_id)
    return event


def _accessible(session, branch_id: str, actor_id: str, event_id: str,
                receipts: dict[str, dict]) -> bool:
    event = session.product.store.world_event(branch_id, event_id)
    if event is None:
        return False
    perceived = {
        (row["actor_id"], row["event_id"])
        for row in session.product.store.perceptions(branch_id)
    }
    if (actor_id, event_id) not in perceived:
        return False
    return any(
        receipt.get("source_event_id") == event_id
        and receipt.get("source_event_hash") == event.get("hash")
        and receipt.get("branch_id") == branch_id
        and receipt.get("actor_id") == actor_id
        and receipt.get("status") == "GRANTED"
        for receipt in receipts.values()
    )


def build_index(session, *, actor_id: str = "A") -> dict:
    """Rebuild the derived index from immutable source events and receipts."""
    branch_id = session.branch_id
    session.product.store.branch(branch_id)
    episodes = session.episodes()
    receipts = _receipts(episodes)
    relations: list[dict] = []
    invalidated: list[dict] = []
    source_refs: set[tuple] = set()
    access_ids: set[str] = set()

    for episode in episodes:
        if episode.get("kind") != "LANGUAGE_ENCOUNTER":
            continue
        body = episode.get("body", {})
        encounter_id = body.get("encounter_id") or episode.get("episode_id", "")
        source_id = body.get("source_event_id", "")
        source_hash = body.get("source_event_hash", "")
        declared_branch = body.get("branch_id", "")
        if declared_branch != branch_id:
            raise LanguageRefusal("SOURCE_BRANCH_MISMATCH",
                                  f"{encounter_id}:{declared_branch}")
        event = _validate_source(session, branch_id, source_id, source_hash)
        source_refs.add((source_id, event["hash"], branch_id))

        reason = ""
        receipt = receipts.get(body.get("access_receipt_id", ""))
        if not receipt:
            reason = "ACCESS_RECEIPT_MISSING"
        elif receipt.get("actor_id") != actor_id:
            reason = "ACCESS_ACTOR_MISMATCH"
        elif receipt.get("source_event_id") != source_id:
            raise LanguageRefusal("ACCESS_EVENT_MISMATCH", receipt.get("receipt_id", ""))
        elif receipt.get("source_event_hash") != source_hash:
            raise LanguageRefusal("ACCESS_HASH_MISMATCH", receipt.get("receipt_id", ""))
        elif receipt.get("branch_id") != branch_id:
            raise LanguageRefusal("ACCESS_BRANCH_MISMATCH", receipt.get("receipt_id", ""))
        elif receipt.get("status") != "GRANTED":
            reason = "ACCESS_REVOKED"
        elif not _accessible(session, branch_id, actor_id, source_id, receipts):
            reason = "ACCESS_NOT_OBSERVED"

        counterexamples = []
        for ref in body.get("counterexample_event_refs", []) or []:
            if isinstance(ref, dict):
                ref_id = ref.get("event_id", "")
                ref_hash = ref.get("event_hash", "")
            else:
                ref_id, ref_hash = ref, ""
            counter_event = _validate_source(
                session, branch_id, ref_id, ref_hash)
            if not _accessible(session, branch_id, actor_id, ref_id, receipts):
                reason = reason or "COUNTEREXAMPLE_NOT_ACCESSIBLE"
            counterexamples.append({
                "event_id": ref_id,
                "event_hash": counter_event["hash"],
            })
            source_refs.add((ref_id, counter_event["hash"], branch_id))

        relation = {
            "relation_id": encounter_id,
            "concept_id": body.get("concept_id", ""),
            "milieu_id": body.get("milieu_id", ""),
            "sense_id": body.get("sense_id", ""),
            "relation_label": body.get("relation_label", ""),
            "atoms": sorted(set(body.get("atoms", []) or [])),
            "language_tag": body.get("language_tag", ""),
            "source_event_ref": {
                "event_id": source_id,
                "event_hash": event["hash"],
                "branch_id": branch_id,
                "clock": event.get("clock"),
                "speaker_actor_id": event.get("actor_id"),
            },
            "access_receipt": {
                "receipt_id": body.get("access_receipt_id", ""),
                "actor_id": receipt.get("actor_id") if receipt else "",
                "access": receipt.get("access") if receipt else "",
                "status": receipt.get("status") if receipt else "MISSING",
            },
            "counterexamples": counterexamples,
            "epistemic": "TEST_ONLY_SOURCE_INDEX",
        }
        access_ids.add(body.get("access_receipt_id", ""))
        if reason:
            invalidated.append({**relation, "status": "INVALID",
                                "invalid_reason": reason})
        else:
            relations.append({**relation, "status": "VALID"})

    relations.sort(key=lambda row: row["relation_id"])
    invalidated.sort(key=lambda row: row["relation_id"])

    groups: dict[str, list[dict]] = {}
    for relation in relations:
        concept = relation["concept_id"]
        if concept:
            groups.setdefault(concept, []).append(relation)
    contradictions = []
    for concept, group in sorted(groups.items()):
        signatures = {
            (row["milieu_id"], row["sense_id"], row["relation_label"])
            for row in group
        }
        if len(group) > 1 and len(signatures) > 1:
            contradictions.append({
                "concept_id": concept,
                "relation_ids": sorted(row["relation_id"] for row in group),
                "milieu_ids": sorted({row["milieu_id"] for row in group}),
                "sense_ids": sorted({row["sense_id"] for row in group}),
                "relation_labels": sorted({row["relation_label"] for row in group}),
            })

    counterexamples_preserved = []
    seen_counterexamples = set()
    for relation in relations:
        for counter in relation["counterexamples"]:
            key = (relation["relation_id"], counter["event_id"])
            if key in seen_counterexamples:
                continue
            seen_counterexamples.add(key)
            counterexamples_preserved.append({
                "relation_id": relation["relation_id"],
                "event_id": counter["event_id"],
                "event_hash": counter["event_hash"],
            })

    source_refs_sorted = [
        {"event_id": row[0], "event_hash": row[1], "branch_id": row[2]}
        for row in sorted(source_refs)
    ]
    readset_payload = {
        "schema": INDEX_SCHEMA,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "relations": relations,
        "invalidated_relations": invalidated,
        "counterexamples_preserved": counterexamples_preserved,
    }
    readset_hash = digest(readset_payload)
    content = {
        "schema": INDEX_SCHEMA,
        "grade": GRADE,
        "native": False,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "relations": relations,
        "invalidated_relations": invalidated,
        "contradictions_preserved": contradictions,
        "counterexamples_preserved": counterexamples_preserved,
        "source_event_refs": source_refs_sorted,
        "access_receipt_ids": sorted(access_ids),
        "readset_hash": readset_hash,
        "not_authorized_for": list(NOT_AUTHORIZED_FOR),
        "product_model_calls": 0,
    }
    index_hash = digest(content)

    cache_rows = _episodes(session, "LANGUAGE_INDEX_CACHE")
    cached_hash = ""
    if cache_rows:
        cached_hash = cache_rows[-1].get("body", {}).get("readset_hash", "")
    if not cache_rows:
        cache_status = "CACHE_ABSENT"
    elif cached_hash == readset_hash:
        cache_status = "CACHE_VALID"
    else:
        cache_status = "CACHE_INVALID"

    return {
        **content,
        "index_hash": index_hash,
        "cache_status": cache_status,
        "cached_readset_hash": cached_hash,
    }


def persist_index_cache(session, index: dict) -> dict:
    """Write a derived-cache receipt to the same C12 episode store."""
    existing = _episodes(session, "LANGUAGE_INDEX_CACHE")
    if existing and existing[-1].get("body", {}).get("readset_hash") == index["readset_hash"]:
        return existing[-1]
    body = {
        "schema": "LME_LANGUAGE_INDEX_CACHE@1",
        "grade": GRADE,
        "index": index,
        "readset_hash": index["readset_hash"],
        "index_hash": index["index_hash"],
        "product_model_calls": 0,
    }
    return session.product._append_episode(
        session.branch_id, "A", "LANGUAGE_INDEX_CACHE", session.clock(), body)


def invalidate_index(session, *, reason: str, changed_ref: str = "") -> dict:
    body = {
        "schema": "LME_LANGUAGE_INDEX_INVALIDATION@1",
        "reason": reason,
        "changed_ref": changed_ref,
        "branch_id": session.branch_id,
        "clock": session.clock(),
        "product_model_calls": 0,
    }
    return session.product._append_episode(
        session.branch_id, "A", "LANGUAGE_INDEX_INVALIDATION",
        session.clock(), body)


__all__ = [
    "INDEX_SCHEMA",
    "ENCOUNTER_SCHEMA",
    "ACCESS_SCHEMA",
    "GRADE",
    "LanguageRefusal",
    "event_hash_valid",
    "build_index",
    "persist_index_cache",
    "invalidate_index",
]
