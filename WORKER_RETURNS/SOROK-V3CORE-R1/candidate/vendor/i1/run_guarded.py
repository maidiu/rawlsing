#!/usr/bin/env python3
"""Cold-process runner for the guarded I1 joined product."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from bp2p4 import bootstrap

bootstrap.install()

from bp2p4.i1_product import GuardedJoinedProduct  # noqa: E402
from bp2p4.reunion import build_fresh  # noqa: E402


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guarded I1 source-free product")
    parser.add_argument("--root", default="")
    parser.add_argument("--branch", default="root")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("observe", "other", "reenter", "verify", "owner-material"):
        sub.add_parser(name)
    for name in ("wait", "repair", "say", "travel", "attend", "fork"):
        command = sub.add_parser(name)
        if name == "wait":
            command.add_argument("hours", type=int)
        elif name == "say":
            command.add_argument("text")
        elif name == "travel":
            command.add_argument("location", choices=["workshop", "market"])
        elif name == "fork":
            command.add_argument("branch_id")
    use = sub.add_parser("use")
    use.add_argument("branch_id")
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(tempfile.mkdtemp(prefix="i1-guarded-"))
    if (root / "bp4_join_state.json").exists():
        product = GuardedJoinedProduct.reopen(root, branch_id=args.branch)
    else:
        product = GuardedJoinedProduct(
            root, artifacts=build_fresh(root), branch_id=args.branch)
    try:
        if args.command == "observe":
            _print(product.observe())
        elif args.command == "other":
            _print(product.other())
        elif args.command == "reenter":
            _print(product.reenter())
        elif args.command == "verify":
            _print({"join": product.verify_join(), "c12": product.verify_c12()})
        elif args.command == "owner-material":
            _print(product.owner_material_readout())
        elif args.command == "wait":
            _print(product.wait(args.hours))
        elif args.command == "repair":
            _print(product.repair())
        elif args.command == "say":
            _print(product.say(args.text))
        elif args.command == "travel":
            _print(product.travel(args.location))
        elif args.command == "attend":
            _print(product.attend())
        elif args.command == "fork":
            _print(product.fork(args.branch_id))
        elif args.command == "use":
            _print(product.use(args.branch_id))
        return 0
    finally:
        product.close()


if __name__ == "__main__":
    raise SystemExit(main())
