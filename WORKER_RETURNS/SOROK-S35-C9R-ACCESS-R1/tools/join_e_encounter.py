from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def _find_c9(state_root: Path, e1_hash: str) -> tuple[Path, dict]:
    for path in sorted(state_root.rglob("c9.sqlite")):
        try:
            connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            row = connection.execute(
                "SELECT body FROM occurrence WHERE hash=?", (e1_hash,)
            ).fetchone()
        finally:
            connection.close()
        if row:
            return path, json.loads(row[0])
    raise RuntimeError("JOIN_E_C9_E1_OCCURRENCE_NOT_FOUND")


def _actor_record(life) -> tuple[dict, dict]:
    from candidate import ActorIdentityRecord

    snapshot = life.a_snapshot
    source = life.a_source
    record = ActorIdentityRecord(
        actor_id=source.actor_id,
        activation_status="ACTIVE",
        standing_state=snapshot["state_hash"],
        currentness_as_of=int(snapshot["last_clock"]),
        source_ref=source.source_ref,
        source_hash=snapshot["hash"],
    ).sealed()
    return record, {
        "state": snapshot["state"],
        "state_hash": snapshot["state_hash"],
        "last_clock": snapshot["last_clock"],
        "hash": snapshot["hash"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--join-e-root", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--disposition", required=True)
    parser.add_argument("--mode", choices=("start", "open"), default="start")
    parser.add_argument("--do-help", action="store_true")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    join_e_root = Path(args.join_e_root).resolve()
    sys.path.insert(0, str(join_e_root))
    from joined.refusal import RefusalSession
    from joined.session import JoinedSession

    state = Path(args.state).resolve()
    disposition = args.disposition
    if args.mode == "start":
        if disposition == "PERFORMED":
            session = JoinedSession.start(state, perform="omit")
        else:
            session = RefusalSession.start(state, b_disposition=disposition)
    else:
        meta = json.loads((state / "session.json").read_text(encoding="utf8"))
        if meta.get("schema") == "SOROK_SAME_PERSON_JOIN@1":
            session = JoinedSession.open(state)
        else:
            session = RefusalSession.open(state)
    try:
        help_result = session.do_help() if args.do_help else None
        product = session.product
        life = None
        if getattr(product, "artifacts", None) is not None:
            life = product.artifacts.life
        elif getattr(product, "seed", None) is not None:
            life = product.seed.life
        if life is None:
            raise RuntimeError("JOIN_E_ACTOR_LIFE_ABSENT")
        actor_record, actor_snapshot = _actor_record(life)
        e1_hash = session.meta.get("j_e1_event_hash", "")
        c9_path, event_body = _find_c9(state, e1_hash)
        e1_event = dict(event_body, hash=e1_hash)
        source = dict(product.source)
        store = product.store
        branch_id = session.branch_id
        branch = store.branch(branch_id)
        root_branch = store.branch("root")
        root_state = store.checkpoints("root")[-1]
        branch_state = store.checkpoints(branch_id)[-1]
        bundle = {
            "schema": "SOROK_JOIN_E_S35_ENCOUNTER_BUNDLE@1",
            "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "native": False,
            "mode": args.mode,
            "disposition": disposition,
            "state_root": str(state),
            "session_schema": session.meta.get("schema"),
            "branch_id": branch_id,
            "root_branch_id": session.meta.get("root_branch_id", "root"),
            "source": source,
            "source_actor_map": session.meta.get("source_actor_map", {}),
            "actor_record": actor_record,
            "actor_snapshot": actor_snapshot,
            "e1_event": e1_event,
            "e1_event_hash": e1_hash,
            "c8_state_digest": session.meta.get(
                "j_c8_state_digest", session.meta.get("c8_state_digest")
            ),
            "c9_path": str(c9_path),
            "c12_path": str(state / "product" / "c12.sqlite"),
            "event_time": int(e1_event.get("time", 0)),
            "event_id": e1_event.get("event_id"),
            "scene": str((e1_event.get("content") or {}).get("scene", "")),
            "material_feasible_after": source.get("material_feasible_after"),
            "target_id": session.meta.get("j_target_id", session.meta.get("target_id", "")),
            "j_b_disposition": session.meta.get("j_b_disposition"),
            "b_performer_receipt": session.meta.get("b_performer_receipt"),
            "c8": session.meta.get("c8"),
            "c9": {
                key: session.meta.get("c9", {}).get(key)
                for key in ("c8_state_digest", "e1_adp019", "target_branch",
                            "target_reason", "target_id", "response_status")
                if key in session.meta.get("c9", {})
            },
            "c12": {
                "branch_id": branch_id,
                "root_branch": root_branch,
                "branch": branch,
                "root_state": root_state,
                "branch_state": branch_state,
                "branch_clock": store.last_clock(branch_id),
                "root_clock": store.last_clock("root"),
            },
            "help": help_result,
            "tools_remaining": session.world().actor_state["A"].get(
                "tools_remaining"
            ),
            "verify_ok": bool(session.verify().get("ok")),
        }
        if not session.verify().get("ok"):
            raise RuntimeError("JOIN_E_VERIFY_FAILED")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(bundle, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf8",
        )
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
