#!/usr/bin/env python3
"""Local executable CLI for the R30A first-neighbor session."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .first_session import FirstSession, SessionRefusal

PRIMER = """R30A // FIRST NEIGHBOR

A life is already in motion here. You did not choose it; you are only visiting.
You may SAY, DO, ATTEND, WAIT, or LEAVE. What you attempt is a proposal; the
world decides what actually happens. The person at the bench is not a quest and
not yours to command.

ENTER
"""


def _print_surface(result: dict) -> None:
    for line in result.get("surface", []):
        print(line)
    meta = {}
    for key in ("status", "accepted", "contact", "clock", "scene_open", "new_knowledge"):
        if key in result:
            meta[key] = result[key]
    if "user_event" in result and result["user_event"]:
        event = result["user_event"]
        meta["user_event"] = {k: event.get(k) for k in
                              ("event_id", "hash", "kind", "clock", "actor_id")}
    if "actor_events" in result:
        meta["actor_events"] = [
            {k: event.get(k) for k in
             ("event_id", "hash", "kind", "clock", "actor_id")}
            for event in result["actor_events"]
        ]
    if meta:
        print(json.dumps({"meta": meta}, indent=2, sort_keys=True, default=str))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="R30A first neighbor session")
    parser.add_argument("--state", required=True, help="persistent session directory")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start")
    start.add_argument("--scenario", choices=["available", "pressed"], default="available")
    start.add_argument("--attention", choices=["focused", "distracted", "tool_focused"],
                       default="focused")
    for name in ("status", "attend", "leave", "messages", "ask-contact", "return",
                 "verify", "custody", "fork-alt"):
        sub.add_parser(name)
    say = sub.add_parser("say")
    say.add_argument("text")
    do = sub.add_parser("do")
    do.add_argument("action", choices=["help", "inspect"])
    travel = sub.add_parser("travel")
    travel.add_argument("location", choices=["workshop", "market"])
    wait = sub.add_parser("wait")
    wait.add_argument("hours", type=int, nargs="?", default=30)
    off = sub.add_parser("offscreen")
    off.add_argument("hours", type=int, nargs="?", default=30)
    msg = sub.add_parser("message")
    msg.add_argument("text")
    args = parser.parse_args(argv)
    state = Path(args.state)

    try:
        if args.command == "start":
            session = FirstSession.start(state, scenario=args.scenario,
                                         attention=args.attention)
            print(PRIMER)
            world = session.world()
            print(f"Clock {world.clock}. Your position: {world.positions.get('U')}.")
            print("The repair worker is at the bench. The finisher is folding pieces near the door.")
            print("The scene has already started.\n")
            print(json.dumps(session.status(), indent=2, sort_keys=True))
            session.close()
            return 0

        session = FirstSession.open(state)
        try:
            if args.command == "status":
                print(json.dumps(session.status(), indent=2, sort_keys=True))
            elif args.command == "say":
                _print_surface(session.say(args.text))
            elif args.command == "do":
                _print_surface(session.do_help() if args.action == "help" else session.inspect())
            elif args.command == "travel":
                _print_surface(session.travel(args.location))
            elif args.command == "attend":
                _print_surface(session.attend())
            elif args.command == "wait":
                _print_surface(session.wait(args.hours))
            elif args.command == "leave":
                _print_surface(session.leave())
            elif args.command == "offscreen":
                result = session.advance_offscreen(args.hours)
                print(json.dumps(result, indent=2, sort_keys=True, default=str))
            elif args.command == "messages":
                print(json.dumps(session.check_messages(), indent=2, sort_keys=True, default=str))
            elif args.command == "message":
                print(json.dumps(session.send_message(args.text), indent=2, sort_keys=True))
            elif args.command == "ask-contact":
                _print_surface(session.ask_contact())
            elif args.command == "return":
                _print_surface(session.return_session())
            elif args.command == "verify":
                print(json.dumps({"verify": session.verify(),
                                  "custody": session.custody()},
                                 indent=2, sort_keys=True, default=str))
            elif args.command == "custody":
                print(json.dumps(session.custody(), indent=2, sort_keys=True, default=str))
            elif args.command == "fork-alt":
                print(json.dumps(session.fork_alt(), indent=2, sort_keys=True, default=str))
            return 0
        finally:
            session.close()
    except SessionRefusal as exc:
        print(json.dumps({"status": "REFUSED", "code": exc.code,
                          "detail": exc.detail}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
