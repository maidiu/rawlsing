"""CLI for explicit caller-supplied interval continuation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .continuation import (
    admit_continuation,
    apply_explicit_interval,
    continue_after_request,
    explicit_do_help,
)


def _json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _interval_input(args) -> dict | None:
    if args.interval_json:
        return json.loads(args.interval_json)
    if args.mode:
        value = {"schema": "SOROK_P2_EXPLICIT_INTERVAL_INPUT@1",
                 "mode": args.mode, "span": args.span}
        if args.start is not None:
            value["start"] = args.start
        return value
    return None


def command_continue(args) -> int:
    result = continue_after_request(
        args.state,
        request=args.request,
        interval_input=_interval_input(args),
        base_root=args.base_root,
    )
    print(_json(result))
    return 0


def command_interval(args) -> int:
    result = apply_explicit_interval(
        args.state, _interval_input(args), base_root=args.base_root
    )
    print(_json(result))
    return 0


def command_admit(args) -> int:
    result = admit_continuation(
        args.state, request=args.request, base_root=args.base_root
    )
    print(_json(result))
    return 0


def command_do_help(args) -> int:
    result = explicit_do_help(
        args.state, request=args.request, base_root=args.base_root
    )
    print(_json(result))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sorok-p2-explicit-interval-flow",
        description=(
            "Explicit caller-supplied interval continuation over the shipped "
            "S45-S47 product. WAIT/ABSENCE alone remain typed holds."
        ),
    )
    parser.add_argument("--base-root", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_interval_args(target):
        target.add_argument("--mode", default=None)
        target.add_argument("--start", type=int, default=None)
        target.add_argument("--span", type=int, default=4)
        target.add_argument("--interval-json", default=None)

    cont = sub.add_parser(
        "continue", help="continue only with explicit lawful interval input"
    )
    cont.add_argument("--state", required=True)
    cont.add_argument("--request", default="WAIT", choices=("WAIT", "ABSENCE"))
    add_interval_args(cont)
    cont.set_defaults(func=command_continue)

    interval = sub.add_parser(
        "interval", help="produce the existing S46 interval without admitting"
    )
    interval.add_argument("--state", required=True)
    add_interval_args(interval)
    interval.set_defaults(func=command_interval)

    admit = sub.add_parser(
        "admit", help="admit and observe the public continued opportunity"
    )
    admit.add_argument("--state", required=True)
    admit.add_argument("--request", default="WAIT", choices=("WAIT", "ABSENCE"))
    admit.set_defaults(func=command_admit)

    do_help = sub.add_parser(
        "do-help",
        help="explicit user DO_HELP operation; never automatic",
    )
    do_help.add_argument("--state", required=True)
    do_help.add_argument("--request", default="WAIT", choices=("WAIT", "ABSENCE"))
    do_help.set_defaults(func=command_do_help)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
