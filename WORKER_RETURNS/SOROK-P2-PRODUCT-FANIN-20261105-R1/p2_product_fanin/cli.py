"""Additive unified CLI for the P2 product throughline."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .integration import P2ProductFanin, apply_explicit_interval
from .runtime import load

sys.dont_write_bytecode = True


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sorok-p2-product-fanin",
        description="TEST_ONLY P2 throughline: lifecycle, interval, later events.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="create a fresh compatible S47 root")
    new.add_argument("--state", required=True)
    new.add_argument("--seed", default="01" * 32)

    view = sub.add_parser("view", help="public WP19 encounter view")
    view.add_argument("--state", required=True)
    view.add_argument("--text", action="store_true")

    say = sub.add_parser("say", help="explicit user SAY attempt")
    say.add_argument("--state", required=True)
    say.add_argument("text")

    do_help = sub.add_parser("do-help", help="explicit user DO_HELP attempt")
    do_help.add_argument("--state", required=True)

    attend = sub.add_parser("attend", help="explicit user ATTEND")
    attend.add_argument("--state", required=True)

    exit_parser = sub.add_parser("exit", help="local UI-only exit")
    exit_parser.add_argument("--state", required=True)

    return_parser = sub.add_parser("return", help="local return when outside")
    return_parser.add_argument("--state", required=True)

    status = sub.add_parser("status", help="adapter status")
    status.add_argument("--state", required=True)

    lifecycle = sub.add_parser("lifecycle", help="public local lifecycle state")
    lifecycle.add_argument("--state", required=True)

    interval = sub.add_parser("interval", help="explicit supplied interval")
    interval.add_argument("--state", required=True)
    interval.add_argument("--mode", required=True, choices=(
        "ACTUAL", "SCHEDULED_ONLY", "DECLINED", "CONSTRAINED", "BLOCKED",
        "UNKNOWN",
    ))
    interval.add_argument("--start", type=int, default=None)
    interval.add_argument("--span", type=int, default=4)

    later = sub.add_parser("later-event", help="admit and observe a later event")
    later.add_argument("--state", required=True)
    later.add_argument("--history-ref", action="append", default=[])

    opportunity = sub.add_parser(
        "opportunity", help="read an existing later event without a user attempt"
    )
    opportunity.add_argument("--state", required=True)
    opportunity.add_argument("--event-ref", required=True)

    verify = sub.add_parser("verify", help="public continuity verification")
    verify.add_argument("--state", required=True)
    return parser


def _open(state: str) -> P2ProductFanin:
    return P2ProductFanin.open(Path(state).expanduser().resolve())


def main(argv: list[str] | None = None) -> int:
    load()
    args = build_parser().parse_args(argv)
    state = Path(args.state).expanduser().resolve()
    try:
        if args.command == "new":
            fanin = P2ProductFanin.start(state, seed=args.seed)
            try:
                value = fanin.view()
            finally:
                fanin.close()
            _print(value)
            return 0
        if args.command == "interval":
            interval_input = {
                "mode": args.mode,
                "span": args.span,
            }
            if args.start is not None:
                interval_input["start"] = args.start
            value = apply_explicit_interval(state, interval_input)
            if value.get("status") == "OK":
                fanin = _open(state)
                try:
                    value["local_mode"] = fanin.local_mode
                    value["view"] = fanin.view()
                finally:
                    fanin.close()
            _print(value)
            return 0
        if args.command == "later-event":
            fanin = _open(state)
            try:
                admitted = fanin.admit_later_event(tuple(args.history_ref))
                value = fanin.public_opportunity(admitted)
            finally:
                fanin.close()
            _print(value)
            return 0
        if args.command == "opportunity":
            fanin = _open(state)
            try:
                read = fanin.read_later_event(args.event_ref)
                value = fanin.public_opportunity(read)
            finally:
                fanin.close()
            _print(value)
            return 0

        fanin = _open(state)
        try:
            if args.command == "view":
                value = fanin.view()
                if args.text:
                    from wp19.interface import render_text

                    print(render_text(value))
                    return 0
            elif args.command == "say":
                value = fanin.say(args.text)
            elif args.command == "do-help":
                value = fanin.do_help()
            elif args.command == "attend":
                value = fanin.attend()
            elif args.command == "exit":
                value = fanin.exit()
            elif args.command == "return":
                value = fanin.return_()
            elif args.command == "status":
                value = fanin.status()
            elif args.command == "lifecycle":
                value = fanin.local_state()
            elif args.command == "verify":
                value = fanin.verify_public()
            else:
                raise AssertionError(args.command)
        finally:
            fanin.close()
    except Exception as exc:
        refusal_type = load()["LifecycleRefusal"]
        if not isinstance(exc, (refusal_type, FileNotFoundError)):
            raise
        _print({
            "schema": "SOROK_P2_PRODUCT_FANIN_REFUSAL@1",
            "grade": "TEST_ONLY_SOURCEFREE_P2_PRODUCT_FANIN_NOT_NATIVE",
            "native": False,
            "code": getattr(exc, "code", type(exc).__name__),
            "detail": getattr(exc, "detail", str(exc)),
        })
        return 2
    _print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
