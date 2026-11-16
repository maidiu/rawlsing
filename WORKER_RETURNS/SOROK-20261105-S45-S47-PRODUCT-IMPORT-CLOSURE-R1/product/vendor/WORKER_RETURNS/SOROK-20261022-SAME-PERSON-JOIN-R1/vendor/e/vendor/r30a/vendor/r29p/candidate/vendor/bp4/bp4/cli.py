"""A0-A3 command-line runner for the BP4 sourcefree product."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .product import BP4Product


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BP4 sourcefree C10/C12 A0-A3 alpha")
    parser.add_argument("--root", default="", help="state directory (default: temp)")
    parser.add_argument("--branch", default="root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    sub.add_parser("observe")
    sub.add_parser("other")
    sub.add_parser("attend")
    sub.add_parser("reenter")
    sub.add_parser("branches")
    for name in ("say", "travel", "wait", "repair", "inspect", "leave-tool",
                 "take-tool", "fork"):
        cmd = sub.add_parser(name)
        if name == "say":
            cmd.add_argument("text")
        elif name == "travel":
            cmd.add_argument("location", choices=["workshop", "market"])
        elif name == "wait":
            cmd.add_argument("hours", type=int)
        elif name == "fork":
            cmd.add_argument("branch_id")
    use = sub.add_parser("use")
    use.add_argument("branch_id")
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(tempfile.mkdtemp(prefix="bp4-cli-"))
    product = BP4Product(root, branch_id=args.branch)
    try:
        if args.command == "demo":
            _print({"step": "A0", "result": product.observe()})
            _print({"step": "A1_SAY", "result": product.say("I am here about the bench.")})
            _print({"step": "A1_DO_INSPECT", "result": product.inspect()})
            _print({"step": "A2_WAIT", "result": product.wait(30)})
            _print({"step": "A3_OTHER", "result": product.other()})
            _print({"step": "A2_TRAVEL", "result": product.travel("market")})
            _print({"step": "A2_ATTEND", "result": product.attend()})
            _print({"step": "A2_REENTRY", "result": product.reenter()})
            return 0
        if args.command == "say":
            _print(product.say(args.text))
        elif args.command == "travel":
            _print(product.travel(args.location))
        elif args.command == "wait":
            _print(product.wait(args.hours))
        elif args.command == "repair":
            _print(product.repair())
        elif args.command == "inspect":
            _print(product.inspect())
        elif args.command == "attend":
            _print(product.attend())
        elif args.command == "leave-tool":
            _print(product.leave_tool())
        elif args.command == "take-tool":
            _print(product.take_tool())
        elif args.command == "other":
            _print(product.other())
        elif args.command == "fork":
            _print(product.fork(args.branch_id))
        elif args.command == "use":
            _print(product.use(args.branch_id))
        elif args.command == "branches":
            _print(product.branches())
        else:
            _print(product.observe())
        return 0
    finally:
        product.close()


if __name__ == "__main__":
    raise SystemExit(main())
