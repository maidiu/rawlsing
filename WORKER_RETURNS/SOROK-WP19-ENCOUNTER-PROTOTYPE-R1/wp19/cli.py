from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .interface import EncounterInterface, render_text


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WP-19 bounded encounter interface")
    parser.add_argument("--source", choices=("join-e", "cp-a5"), required=True)
    parser.add_argument("--root", default="")
    parser.add_argument(
        "--disposition",
        choices=("PERFORMED", "OMITTED", "REFUSED"),
        default="PERFORMED",
    )
    parser.add_argument("--perform", choices=("e2", "omit"), default="omit")
    sub = parser.add_subparsers(dest="command", required=True)
    view = sub.add_parser("view")
    view.add_argument("--text", action="store_true")
    sub.add_parser("status")
    sub.add_parser("demo")
    sub.add_parser("wait")
    sub.add_parser("exit")
    sub.add_parser("return")
    sub.add_parser("absence")
    sub.add_parser("persona-response")
    say = sub.add_parser("say")
    say.add_argument("text")
    do = sub.add_parser("do")
    do.add_argument("intent")
    attend = sub.add_parser("attend")
    attend.add_argument("target")
    ask = sub.add_parser("ask")
    ask.add_argument("question")
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(
        tempfile.mkdtemp(prefix="wp19-" + args.source + "-")
    )
    interface = EncounterInterface(
        args.source,
        root,
        disposition=args.disposition,
        perform=args.perform,
    )
    if args.command == "view":
        value = interface.view()
        if args.text:
            print(render_text(value))
        else:
            _print(value)
    elif args.command == "status":
        _print(interface.status())
    elif args.command == "demo":
        value = interface.view()
        demo = {
            "view": value,
            "asks": (
                [
                    interface.ask("What happened to the workshop tool?"),
                    interface.ask("What did B do at the market?"),
                ]
                if args.source == "cp-a5"
                else [interface.ask("What happened to the workshop tool?")]
            ),
            "say": interface.say("Hello."),
            "do": interface.do("inspect the bench"),
            "wait": interface.wait(),
            "exit": interface.exit(),
            "return": interface.return_(),
            "absence": interface.absence(),
            "status": interface.status(),
        }
        _print(demo)
    elif args.command == "say":
        _print(interface.say(args.text))
    elif args.command == "do":
        _print(interface.do(args.intent))
    elif args.command == "attend":
        _print(interface.attend(args.target))
    elif args.command == "ask":
        _print(interface.ask(args.question))
    elif args.command == "wait":
        _print(interface.wait())
    elif args.command == "exit":
        _print(interface.exit())
    elif args.command == "return":
        _print(interface.return_())
    elif args.command == "absence":
        _print(interface.absence())
    elif args.command == "persona-response":
        _print(interface.persona_response())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
