"""Additive lifecycle CLI over the accepted S45 projection adapter."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .lifecycle import LifecycleEncounter, LifecycleRefusal

sys.dont_write_bytecode = True


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _open(args) -> LifecycleEncounter:
    root = Path(args.state).expanduser().resolve()
    if args.command == "new":
        return LifecycleEncounter.start(root, seed=args.seed)
    return LifecycleEncounter.open(root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sorok-p2-lifecycle",
        description="Persistent LOCAL encounter lifecycle CLI (TEST_ONLY).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create a fresh local encounter")
    new.add_argument("--state", required=True)
    new.add_argument("--seed", default="01" * 32)
    view = sub.add_parser("view", help="public WP19 encounter view")
    view.add_argument("--state", required=True)
    view.add_argument("--text", action="store_true")
    for name, help_text in (
        ("say", "user SAY attempt when locally permitted"),
        ("do-help", "user DO_HELP attempt when locally permitted"),
        ("attend", "user ATTEND when locally permitted"),
        ("exit", "local UI-only exit"),
        ("return", "local return when outside, world hold when inside"),
        ("status", "adapter status"),
        ("lifecycle", "public local lifecycle state"),
    ):
        item = sub.add_parser(name, help=help_text)
        item.add_argument("--state", required=True)
        if name == "say":
            item.add_argument("text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        encounter = _open(args)
        try:
            if args.command == "new":
                value = encounter.view()
            elif args.command == "view":
                value = encounter.view()
                if args.text:
                    from wp19.interface import render_text

                    print(render_text(value))
                    return 0
            elif args.command == "say":
                value = encounter.say(args.text)
            elif args.command == "do-help":
                value = encounter.do_help()
            elif args.command == "attend":
                value = encounter.attend()
            elif args.command == "exit":
                value = encounter.exit()
            elif args.command == "return":
                value = encounter.return_()
            elif args.command == "status":
                value = encounter.status()
            elif args.command == "lifecycle":
                value = encounter.local_state()
            else:
                raise AssertionError(args.command)
        finally:
            encounter.close()
    except LifecycleRefusal as exc:
        _print({
            "schema": "SOROK_P2_LOCAL_LIFECYCLE_REFUSAL@1",
            "grade": "TEST_ONLY_LOCAL_UI_LIFECYCLE_NOT_NATIVE",
            "native": False,
            "code": exc.code,
            "detail": exc.detail,
        })
        return 2
    _print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
