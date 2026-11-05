"""CLI for the additive P2 later-event continuation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .continuation import (
    P2Continuation,
    cold_read,
    run_cut_restore,
    run_positive,
    run_scheduled,
)


def _json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sorok-p2-later-event-continuation",
        description="TEST_ONLY sourcefree S41-S43 later-event continuation",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    positive = sub.add_parser("positive")
    positive.add_argument("--state", required=True)
    positive.add_argument("--seed", default="01" * 32)

    scheduled = sub.add_parser("scheduled")
    scheduled.add_argument("--state", required=True)
    scheduled.add_argument("--seed", default="01" * 32)

    cut_restore = sub.add_parser("cut-restore")
    cut_restore.add_argument("--state", required=True)
    cut_restore.add_argument("--seed", default="01" * 32)

    new = sub.add_parser("new")
    new.add_argument("--state", required=True)
    new.add_argument("--seed", default="01" * 32)

    admit = sub.add_parser("admit")
    admit.add_argument("--state", required=True)
    admit.add_argument("--history-ref", action="append", default=[])

    say = sub.add_parser("say")
    say.add_argument("--state", required=True)
    say.add_argument("text")

    do_help = sub.add_parser("do-help")
    do_help.add_argument("--state", required=True)

    attend = sub.add_parser("attend")
    attend.add_argument("--state", required=True)

    view = sub.add_parser("view")
    view.add_argument("--state", required=True)

    verify = sub.add_parser("verify")
    verify.add_argument("--state", required=True)

    cold = sub.add_parser("cold")
    cold.add_argument("--state", required=True)
    cold.add_argument("--event-ref", action="append", required=True)

    args = parser.parse_args(argv)
    state = Path(args.state).expanduser().resolve()

    if args.command == "positive":
        report = run_positive(state, seed=args.seed)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "scheduled":
        report = run_scheduled(state, seed=args.seed)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "cut-restore":
        report = run_cut_restore(state, seed=args.seed)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "cold":
        report = cold_read(state, tuple(args.event_ref))
        print(_json(report))
        return 0 if report["verify_ok"] else 1

    continuation = P2Continuation.start(state, seed=args.seed) if args.command == "new" else P2Continuation.open(state)
    try:
        if args.command == "new":
            result = continuation.view()
        elif args.command == "admit":
            history_refs = tuple(args.history_ref)
            if not history_refs:
                history_refs = (
                    continuation.session.read_events()[0]["e1_event_id"],
                )
            result = continuation.admit_later_event(history_refs)
        elif args.command == "say":
            result = continuation.project_say(args.text)
        elif args.command == "do-help":
            result = continuation.project_do_help()
        elif args.command == "attend":
            result = continuation.project_attend()
        elif args.command == "view":
            result = continuation.view()
        elif args.command == "verify":
            result = continuation.verify()
        else:
            raise AssertionError(args.command)
    finally:
        continuation.close()
    print(_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
