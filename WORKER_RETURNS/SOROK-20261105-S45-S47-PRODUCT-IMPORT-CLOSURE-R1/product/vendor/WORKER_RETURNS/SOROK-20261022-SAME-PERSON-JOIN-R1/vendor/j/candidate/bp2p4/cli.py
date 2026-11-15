"""A0-A3 command-line runner over the joined BP2 -> BP4 product.

First invocation on a fresh ``--root`` produces the real BP2 joined artifacts
(C8 keyed journal + C9 durable target + performed E2) and then creates the BP4
C12 world root. Every later invocation is a cold reentry: it recovers and
re-verifies the BP2 artifacts and reopens the C12 store.

``--origin`` consumes the surviving literal BP2 origin runtime (target
``950a4c79…``) when it is present on this machine, for a direct literal-origin
cross-check.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from . import bootstrap

bootstrap.install()

from .product import JoinedProduct  # noqa: E402
from .reunion import (  # noqa: E402
    DEFAULT_ORIGIN_RUNTIME,
    ReunionRefusal,
    build_fresh,
    load_origin_literal,
    origin_runtime_available,
    recover,
)
from .assertion import joined_downstream_a0_a2_assertion  # noqa: E402

DEFAULT_EVIDENCE = Path(__file__).resolve().parent.parent / "vendor" / "bp2" / "evidence" / "joined_positive_receipt.json"


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _open(root: Path, *, origin: str | None):
    root.mkdir(parents=True, exist_ok=True)
    binding = root / "bp2_join.json"
    if origin:
        runtime = origin_runtime_available(origin)
        if runtime is None:
            raise ReunionRefusal("ORIGIN_RUNTIME_ABSENT", origin)
        artifacts = load_origin_literal(runtime, evidence_path=DEFAULT_EVIDENCE,
                                        workspace=root)
    elif binding.exists():
        artifacts = recover(root)
    else:
        artifacts = build_fresh(root)
    return JoinedProduct(root, artifacts=artifacts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Joined BP2->BP4 source-free C10/C12 A0-A3 alpha")
    parser.add_argument("--root", default="", help="state directory (default: temp)")
    parser.add_argument("--branch", default="root")
    parser.add_argument("--origin", default="",
                        help="literal BP2 origin runtime directory")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("demo", "observe", "other", "attend", "reenter", "branches",
                 "repair", "inspect", "leave-tool", "take-tool", "source",
                 "verify", "assert"):
        sub.add_parser(name)
    for name in ("say", "travel", "wait", "fork"):
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
    root = Path(args.root) if args.root else Path(tempfile.mkdtemp(prefix="bp2p4j-"))
    product = _open(root, origin=args.origin or None)
    try:
        if args.command == "demo":
            _print({"step": "SOURCE", "result": product.joined_source()})
            _print({"step": "A0", "result": product.observe()})
            _print({"step": "A1_SAY", "result": product.say("I am here about the bench.")})
            _print({"step": "A1_DO_INSPECT", "result": product.inspect()})
            _print({"step": "A1_DO_REPAIR", "result": product.repair()})
            _print({"step": "A2_WAIT", "result": product.wait(30)})
            _print({"step": "A3_OTHER", "result": product.other()})
            _print({"step": "A2_TRAVEL", "result": product.travel("market")})
            _print({"step": "A2_ATTEND", "result": product.attend()})
            _print({"step": "A2_REENTRY", "result": product.reenter()})
            return 0
        if args.command == "assert":
            receipt = joined_downstream_a0_a2_assertion(root, product.artifacts)
            _print(receipt)
        elif args.command == "source":
            _print(product.joined_source())
        elif args.command == "verify":
            _print(product.verify_join())
        elif args.command == "say":
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
        elif args.command == "reenter":
            _print(product.reenter())
        else:
            _print(product.observe())
        return 0
    finally:
        product.close()


if __name__ == "__main__":
    raise SystemExit(main())
