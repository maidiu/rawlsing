from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def _c9_path(state: Path, schema: str) -> Path:
    if schema == "SOROK_SAME_PERSON_REFUSAL@1":
        return state / "source" / "bp2" / "c9.sqlite"
    return state / "bp2" / "c9.sqlite"


def _occurrence(c9_path: Path, e1_hash: str) -> dict:
    connection = sqlite3.connect(f"file:{c9_path}?mode=ro", uri=True)
    try:
        row = connection.execute(
            "SELECT body FROM occurrence WHERE hash=?", (e1_hash,)
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        raise RuntimeError("WP19_E1_OCCURRENCE_NOT_FOUND")
    body = json.loads(row[0])
    content = body.get("content") or {}
    return {
        "event_time": int(body.get("time", 0)),
        "event_id": body.get("event_id", ""),
        "scene": str(content.get("scene", "")),
        "event_body": body,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--join-e-root", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--disposition", default="PERFORMED")
    parser.add_argument("--perform", choices=("e2", "omit"), default="omit")
    parser.add_argument("--mode", choices=("start", "open"), default="start")
    parser.add_argument("--do-help", action="store_true")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(args.join_e_root).resolve()))
    from joined.refusal import RefusalSession
    from joined.session import JoinedSession

    state = Path(args.state).resolve()
    if args.mode == "start":
        if args.disposition == "PERFORMED":
            session = JoinedSession.start(state, perform=args.perform)
        else:
            session = RefusalSession.start(
                state, b_disposition=args.disposition
            )
    else:
        meta = json.loads((state / "session.json").read_text(encoding="utf8"))
        if meta.get("schema") == "SOROK_SAME_PERSON_JOIN@1":
            session = JoinedSession.open(state)
        else:
            session = RefusalSession.open(state)
    try:
        help_result = session.do_help() if args.do_help else None
        product = session.product
        store = product.store
        branch_id = session.branch_id
        state_now = store.latest_state(branch_id)
        life = getattr(getattr(product, "artifacts", None), "life", None)
        if life is None:
            life = getattr(product.seed, "life", None)
        if life is None:
            raise RuntimeError("WP19_ACTOR_LIFE_ABSENT")
        snapshot = life.a_snapshot
        actor_source = life.a_source
        schema = session.meta.get("schema", "")
        e1_hash = session.meta.get("j_e1_event_hash", "")
        occurrence = _occurrence(_c9_path(state, schema), e1_hash)
        bundle = {
            "schema": "SOROK_WP19_JOIN_E_BUNDLE@1",
            "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "native": False,
            "state_root": str(state),
            "session_schema": schema,
            "branch_id": branch_id,
            "root_branch_id": session.meta.get("root_branch_id", "root"),
            "source": dict(product.source),
            "source_actor_map": session.meta.get("source_actor_map", {}),
            "e1_event_hash": e1_hash,
            "event_id": occurrence["event_id"],
            "event_time": occurrence["event_time"],
            "scene": occurrence["scene"],
            "e1_event_body": occurrence["event_body"],
            "c9_path": str(_c9_path(state, schema)),
            "c8_state_digest": session.meta.get(
                "j_c8_state_digest", session.meta.get("c8_state_digest")
            ),
            "j_b_disposition": session.meta.get("j_b_disposition"),
            "target_id": session.meta.get(
                "j_target_id", session.meta.get("target_id", "")
            ),
            "branch_clock": store.last_clock(branch_id),
            "position": state_now.get("world", {}).get("positions", {}).get("U"),
            "world": {
                "clock": state_now.get("world", {}).get("clock"),
                "positions": state_now.get("world", {}).get("positions", {}),
                "resources": state_now.get("world", {}).get("resources", {}),
                "actor_state": state_now.get("actors", {}),
            },
            "actor_snapshot": {
                "state": snapshot["state"],
                "state_hash": snapshot["state_hash"],
                "last_clock": snapshot["last_clock"],
                "hash": snapshot["hash"],
                "source_ref": actor_source.source_ref,
                "source_hash": actor_source.source_hash,
            },
            "history": {
                "source_ref": actor_source.source_ref,
                "source_hash": actor_source.source_hash,
                "history_hash": snapshot.get("history_hash", ""),
                "event_head": snapshot.get("event_head", ""),
                "event_count": snapshot.get("event_count", 0),
                "last_clock": snapshot.get("last_clock", 0),
                "performed_action_refs": list(
                    snapshot.get("performed_action_refs", [])
                ),
                "objective_refs": list(snapshot.get("objective_refs", [])),
                "domain": "BP1_ACTOR_HISTORY",
                "native": False,
            },
            "world_events": store.world_events(branch_id),
            "perceptions": store.perceptions(branch_id),
            "help": help_result,
            "tools_remaining": session.world().actor_state["A"].get(
                "tools_remaining"
            ),
            "verify_ok": bool(session.verify().get("ok")),
            "c12_path": str(state / "product" / "c12.sqlite"),
        }
        Path(args.out).write_text(
            json.dumps(bundle, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8",
        )
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
