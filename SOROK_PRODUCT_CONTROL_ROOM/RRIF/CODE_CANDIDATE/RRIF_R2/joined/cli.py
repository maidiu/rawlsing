"""Small runnable CLI for the sourcefree J/E same-person join.

Run from the repository root with the return directory on PYTHONPATH:

  PYTHONPATH=WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
    python3 -m joined.cli start --state /tmp/join-demo

No external model, provider, human participant, native grant or production
service is used.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .session import JoinedSession


def _dump(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _open(args) -> JoinedSession:
    return JoinedSession.open(args.state, attention=args.attention)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("--state", required=True)
    start.add_argument("--perform", choices=("e2", "omit"), default="omit")
    start.add_argument("--attention", default="focused")
    start.add_argument("--variant", default="A_REPAIR_LONG")

    for name in ("say", "help", "contact", "attend", "wait", "leave",
                 "offscreen", "return", "status", "verify", "messages",
                 "fork"):
        command = sub.add_parser(name)
        command.add_argument("--state", required=True)
        command.add_argument("--attention", default=None)
        if name == "say":
            command.add_argument("text")
        if name in ("wait", "offscreen"):
            command.add_argument("--hours", type=int, default=30)
        if name == "fork":
            command.add_argument("--branch", default="alt")

    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            session = JoinedSession.start(
                args.state, perform=args.perform,
                attention=args.attention, variant=args.variant)
        else:
            session = _open(args)

        if args.command == "start":
            result = {"status": "STARTED", "session": session.status(),
                      "source": session.product.source,
                      "target_id": session.meta.get("j_target_id")}
        elif args.command == "say":
            result = session.say(args.text)
        elif args.command == "help":
            result = session.do_help()
        elif args.command == "contact":
            result = session.ask_contact()
        elif args.command == "attend":
            result = session.attend()
        elif args.command == "wait":
            result = session.wait(args.hours)
        elif args.command == "leave":
            result = session.leave()
        elif args.command == "offscreen":
            result = session.advance_offscreen(args.hours)
        elif args.command == "return":
            result = session.return_session()
        elif args.command == "status":
            result = session.status()
        elif args.command == "verify":
            from .closure import audit_loaded, audit_manifest
            result = {"session": session.verify(),
                      "root": session.product.c12_verify("root"),
                      "closure": audit_loaded(),
                      "manifest": {k: audit_manifest()[k]
                                   for k in ("ok", "files", "problems",
                                             "manifest_sha256")}}
        elif args.command == "messages":
            result = session.check_messages()
        elif args.command == "fork":
            result = session.fork_alt(args.branch)
        else:
            parser.error("unknown command")
            return 2
        _dump(result)
        session.close()
        return 0
    except Exception as exc:
        _dump({"status": "REFUSED", "code": getattr(exc, "code", ""),
               "error": type(exc).__name__ + ":" + str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
