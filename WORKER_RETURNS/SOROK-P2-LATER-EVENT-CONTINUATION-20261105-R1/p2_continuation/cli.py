"""CLI for the additive P2 later-event continuation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .continuation import (
    GRADE,
    P2Continuation,
    PUBLIC_SCHEMA,
    cold_read,
    public_cold_report,
    public_cut_restore_report,
    public_opportunity,
    public_report,
    run_cut_restore,
    run_positive,
    run_scheduled,
)


def _json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _write_engineering(path: str | None, report) -> None:
    if not path:
        return
    target = Path(path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_json(report) + "\n")


def _public_error(scenario: str, reason: str) -> dict:
    return {
        "schema": PUBLIC_SCHEMA,
        "grade": GRADE,
        "native": False,
        "scenario": scenario,
        "status": "REFUSED",
        "reason": reason,
        "ok": False,
    }


def _add_actions(target) -> None:
    target.add_argument("--say", action="store_true",
                        help="explicit user SAY action")
    target.add_argument("--do-help", action="store_true",
                        help="explicit user DO_HELP action")
    target.add_argument("--attend", action="store_true",
                        help="explicit user ATTEND action")
    target.add_argument("--engineering-out", default=None)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sorok-p2-later-event-continuation",
        description="TEST_ONLY sourcefree S41-S43 later-event continuation",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    positive = sub.add_parser("positive")
    positive.add_argument("--state", required=True)
    positive.add_argument("--seed", default="01" * 32)
    _add_actions(positive)

    scheduled = sub.add_parser("scheduled")
    scheduled.add_argument("--state", required=True)
    scheduled.add_argument("--seed", default="01" * 32)
    _add_actions(scheduled)

    cut_restore = sub.add_parser("cut-restore")
    cut_restore.add_argument("--state", required=True)
    cut_restore.add_argument("--seed", default="01" * 32)
    cut_restore.add_argument("--engineering-out", default=None)

    new = sub.add_parser("new")
    new.add_argument("--state", required=True)
    new.add_argument("--seed", default="01" * 32)

    admit = sub.add_parser("admit")
    admit.add_argument("--state", required=True)
    admit.add_argument("--history-ref", action="append", default=[])
    admit.add_argument("--engineering-out", default=None)

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
    verify.add_argument("--engineering-out", default=None)

    cold = sub.add_parser("cold")
    cold.add_argument("--state", required=True)
    cold.add_argument("--event-ref", action="append", required=True)
    cold.add_argument("--engineering-out", default=None)

    args = parser.parse_args(argv)
    state = Path(args.state).expanduser().resolve()

    if args.command == "positive":
        engineering = run_positive(
            state, seed=args.seed, execute_say=args.say,
            execute_do_help=args.do_help, execute_attend=args.attend,
        )
        _write_engineering(args.engineering_out, engineering)
        report = public_report(engineering)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "scheduled":
        engineering = run_scheduled(
            state, seed=args.seed, execute_say=args.say,
            execute_do_help=args.do_help, execute_attend=args.attend,
        )
        _write_engineering(args.engineering_out, engineering)
        report = public_report(engineering)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "cut-restore":
        engineering = run_cut_restore(state, seed=args.seed)
        _write_engineering(args.engineering_out, engineering)
        report = public_cut_restore_report(engineering)
        print(_json(report))
        return 0 if report["ok"] else 1
    if args.command == "cold":
        engineering = cold_read(state, tuple(args.event_ref))
        _write_engineering(args.engineering_out, engineering)
        report = public_cold_report(engineering)
        print(_json(report))
        return 0 if report["ok"] else 1

    continuation = (
        P2Continuation.start(state, seed=args.seed)
        if args.command == "new" else P2Continuation.open(state)
    )
    try:
        if args.command == "new":
            result = continuation.view()
        elif args.command == "admit":
            history_refs = tuple(args.history_ref)
            if not history_refs:
                history_refs = (
                    continuation.session.read_events()[0]["e1_event_id"],
                )
            before = len(continuation.session.read_encounters())
            try:
                engineering = continuation.admit_later_event(history_refs)
            except Exception as exc:
                print(_json(_public_error(
                    "ADMIT_LATER_EVENT_PUBLIC",
                    getattr(exc, "code", type(exc).__name__),
                )))
                return 1
            view = continuation.view()
            after = len(continuation.session.read_encounters())
            _write_engineering(args.engineering_out, {
                **engineering, "view": view,
            })
            result = {
                "schema": PUBLIC_SCHEMA,
                "grade": GRADE,
                "native": False,
                "scenario": "ADMIT_LATER_EVENT_PUBLIC",
                "status": engineering.get("status"),
                "opportunity": public_opportunity(view),
                "view": view,
                "do_help_executed": False,
                "encounter_count_before_action": before,
                "encounter_count_after_action": after,
                "ok": engineering.get("status") == "OK",
            }
        elif args.command == "say":
            result = continuation.project_say(args.text)
        elif args.command == "do-help":
            result = continuation.project_do_help()
        elif args.command == "attend":
            result = continuation.project_attend()
        elif args.command == "view":
            result = continuation.view()
        elif args.command == "verify":
            engineering = continuation.verify()
            _write_engineering(args.engineering_out, engineering)
            result = {
                "schema": PUBLIC_SCHEMA,
                "grade": GRADE,
                "native": False,
                "scenario": "VERIFY_PUBLIC",
                "verify_ok": bool(engineering.get("ok")),
                "event_count": len(continuation.session.read_events()),
                "encounter_count": len(continuation.session.read_encounters()),
                "ok": bool(engineering.get("ok")),
            }
        else:
            raise AssertionError(args.command)
    finally:
        continuation.close()
    print(_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
