"""Independent C05 observation helper used by the reviewer probes.

Read-only against product state. The parent probe and the fresh process import
the exact same snapshot function so warm/cold equality is not hand-composed.
"""
from __future__ import annotations

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
ENGINE = REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.contracts import canonical, digest  # noqa: E402
from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND,
    RELATION_HEAD_KIND,
    read_actor_relative_context,
    read_relation_history,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_supporting_actor,
)


def counts(session) -> dict:
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
    }


def relation_counts(session, actor_ids) -> dict:
    episodes = session.product.store.episodes(session.branch_id)
    rows = {}
    for actor_id in actor_ids:
        rows[actor_id] = len([
            row for row in episodes
            if row.get("kind") == "P2_SUPPORTING_ACTOR"
            and (row.get("body") or {}).get("actor_id") == actor_id
        ])
    return {
        "registrations": rows,
        "relation_changes": len([
            row for row in episodes if row.get("kind") == RELATION_CHANGE_KIND
        ]),
        "relation_heads": len([
            row for row in episodes if row.get("kind") == RELATION_HEAD_KIND
        ]),
        "c04_utterances": len([
            row for row in episodes if row.get("kind") == "P2_PARENT_UTTERANCE"
        ]),
    }


def _relation_rows(session) -> list[dict]:
    rows = []
    for row in session.product.store.episodes(session.branch_id):
        if row.get("kind") not in (RELATION_CHANGE_KIND, RELATION_HEAD_KIND):
            continue
        body = row.get("body") or {}
        rows.append({
            "episode_id": row["episode_id"],
            "hash": row["hash"],
            "kind": row["kind"],
            "clock": row.get("clock"),
            "body_digest": digest(body),
            "body_keys": sorted(body),
        })
    return sorted(rows, key=lambda item: (item["clock"], item["episode_id"]))


def snapshot(session, actor_ids, event_ids, as_of_by_event, all_clocks) -> dict:
    root = session.read_root()
    supporting_ids = [
        actor_id for actor_id in actor_ids
        if actor_id not in root["actor_ids"]
    ]
    return {
        "root_hash": root["root_hash"],
        "root_actor_ids": list(root["actor_ids"]),
        "branch": session.branch_id,
        "clock": session.world().clock,
        "world_hash": digest(session.world().snapshot()),
        "counts": counts(session),
        "relation_counts": relation_counts(session, supporting_ids),
        "registrations": {
            actor_id: read_supporting_actor(session, actor_id)
            for actor_id in supporting_ids
        },
        "events": {
            event_id: {
                "event_id": session.event(event_id)["event_id"],
                "hash": session.event(event_id)["hash"],
                "clock": session.event(event_id)["clock"],
                "kind": session.event(event_id)["kind"],
                "schema": session.event(event_id)["schema"],
                "grade": session.event(event_id)["grade"],
                "native": session.event(event_id)["native"],
            }
            for event_id in event_ids
        },
        "histories": {
            f"{actor_id}|{clock}": read_relation_history(
                session, actor_id, as_of_clock=clock)
            for actor_id in actor_ids
            for clock in all_clocks
        },
        "contexts": {
            f"{actor_id}|{event_id}": read_actor_relative_context(
                session, actor_id, event_id)
            for actor_id in actor_ids
            for event_id in event_ids
        },
        "relation_rows": _relation_rows(session),
        "canonical_digest": digest({
            "world": session.world().snapshot(),
            "events": session.read_events(),
            "root": root,
        }),
    }


def public_json(value) -> str:
    return canonical(value)
