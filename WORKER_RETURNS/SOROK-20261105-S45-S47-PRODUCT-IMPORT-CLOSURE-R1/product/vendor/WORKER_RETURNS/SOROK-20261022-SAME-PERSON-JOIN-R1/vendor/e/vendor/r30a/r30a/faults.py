"""Source/actor fault helpers for R30A tests.

All destructive operations run on a copied state root, never the evidence root.
The copied DB is a real SQLite C12 store; triggers are dropped only to simulate
an external tamper, and the qualified verifier or product open is expected to
refuse or the surface is expected to change.
"""
from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path

from .first_session import FirstSession, SessionRefusal, USER_ACTOR


def copy_state(source, destination) -> Path:
    source = Path(source)
    destination = Path(destination)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    meta_path = destination / "session.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf8"))
        meta["state_root"] = str(destination)
        meta["product_root"] = str(destination / "product")
        meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n",
                             encoding="utf8")
    return destination


def _db(state_root: Path) -> Path:
    return Path(state_root) / "product" / "c12.sqlite"


def _rows(db_path: Path, table: str, branch: str = "first_session"):
    with sqlite3.connect(db_path) as db:
        for row in db.execute(f"SELECT body FROM {table} WHERE branch_id=? ORDER BY seq",
                              (branch,)):
            yield json.loads(row[0])


def delete_events(state_root, predicate) -> list[str]:
    db_path = _db(Path(state_root))
    removed = []
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS world_event_no_delete")
        db.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        db.execute("DROP TRIGGER IF EXISTS perception_no_delete")
        events = list(db.execute(
            "SELECT seq,event_id,body FROM world_event WHERE branch_id='first_session' "
            "ORDER BY seq"))
        for seq, event_id, body in events:
            parsed = json.loads(body)
            if predicate(parsed):
                removed.append(event_id)
                db.execute("DELETE FROM world_event WHERE branch_id='first_session' AND event_id=?",
                           (event_id,))
                db.execute("DELETE FROM perception WHERE branch_id='first_session' AND event_id=?",
                           (event_id,))
        db.commit()
    return removed


def delete_offscreen_activity(state_root) -> dict:
    """Delete B's offscreen episode + world events + perceptions in a copy."""
    db_path = _db(Path(state_root))
    removed_episodes = []
    removed_events = []
    with sqlite3.connect(db_path) as db:
        for trigger in ("episode_no_delete", "world_event_no_delete",
                        "perception_no_delete"):
            db.execute(f"DROP TRIGGER IF EXISTS {trigger}")
        for seq, episode_id, body in db.execute(
                "SELECT seq,episode_id,body FROM episode "
                "WHERE branch_id='first_session' AND actor_id='B' ORDER BY seq"):
            parsed = json.loads(body)
            if parsed.get("kind") in {"OFFSCREEN", "SAY", "DO"}:
                removed_episodes.append(episode_id)
                db.execute("DELETE FROM episode WHERE branch_id='first_session' "
                           "AND episode_id=?", (episode_id,))
        for seq, event_id, body in db.execute(
                "SELECT seq,event_id,body FROM world_event "
                "WHERE branch_id='first_session' ORDER BY seq"):
            parsed = json.loads(body)
            if parsed.get("kind") in {"OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE"}:
                removed_events.append(event_id)
                db.execute("DELETE FROM world_event WHERE branch_id='first_session' "
                           "AND event_id=?", (event_id,))
                db.execute("DELETE FROM perception WHERE branch_id='first_session' "
                           "AND event_id=?", (event_id,))
        db.commit()
    return {"episodes": removed_episodes, "events": removed_events}


def delete_episode_kinds(state_root, kinds: set[str]) -> list[str]:
    db_path = _db(Path(state_root))
    removed = []
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        rows = list(db.execute(
            "SELECT seq,episode_id,kind FROM episode WHERE branch_id='first_session' ORDER BY seq"))
        for seq, episode_id, kind in rows:
            if kind in kinds:
                removed.append(episode_id)
                db.execute("DELETE FROM episode WHERE branch_id='first_session' AND episode_id=?",
                           (episode_id,))
        db.commit()
    return removed


def tamper_speech_text(state_root, event_id: str, new_text: str, *,
                       recompute: bool = False) -> dict:
    """Replace committed speech text, optionally recomputing the internal hash.

    If ``recompute`` is False the qualified C12 verifier must go RED. If True,
    the local chain is internally consistent but the original published event
    identity is gone; callers must compare the original hash to detect it.
    """
    from bp1.canon import digest
    db_path = _db(Path(state_root))
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS world_event_no_update")
        row = db.execute(
            "SELECT body FROM world_event WHERE branch_id='first_session' AND event_id=?",
            (event_id,)).fetchone()
        if row is None:
            raise ValueError("EVENT_NOT_FOUND")
        body = json.loads(row[0])
        original_hash = body.get("hash")
        body["body"]["text"] = new_text
        body["summary"] = f"{body['actor_id']} says: {new_text}"
        if recompute:
            body.pop("hash", None)
            body["hash"] = digest(body)
        db.execute(
            "UPDATE world_event SET body=?, hash=? WHERE branch_id='first_session' AND event_id=?",
            (json.dumps(body, sort_keys=True, separators=(",", ":")), body["hash"], event_id))
        db.commit()
    return {"event_id": event_id, "original_hash": original_hash,
            "new_hash": body["hash"], "recomputed": recompute}


def open_copied_session(state_root):
    return FirstSession.open(Path(state_root))


def private_tokens(session) -> list[str]:
    """Field names and stable identities that must never appear in a surface."""
    return [
        "cash", "debt_units", "free_hours", "material_remaining",
        "projects", "practice_label", "nonmother_relations", "actor_id",
        "TEST_ONLY_BP1_R26V_ACTOR_A", "source_hash", "history_hash",
    ]
