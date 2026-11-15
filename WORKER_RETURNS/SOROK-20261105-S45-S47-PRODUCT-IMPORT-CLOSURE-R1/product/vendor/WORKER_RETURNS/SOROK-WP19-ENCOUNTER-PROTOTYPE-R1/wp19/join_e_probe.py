from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
        bundle = {
            "schema": "SOROK_WP19_JOIN_E_BUNDLE@1",
            "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "native": False,
            "state_root": str(state),
            "session_schema": session.meta.get("schema"),
            "branch_id": branch_id,
            "root_branch_id": session.meta.get("root_branch_id", "root"),
            "source": dict(product.source),
            "source_actor_map": session.meta.get("source_actor_map", {}),
            "e1_event_hash": session.meta.get("j_e1_event_hash", ""),
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
