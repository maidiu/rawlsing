#!/usr/bin/env python3
"""Local R31E actor-conditioned first-neighbor CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .session import R31ESession, SessionRefusal

PRIMER = """R31E // FIRST NEIGHBOR

A life is already in motion. You are a visitor, not the author.
SAY, DO help, DO inspect, TRAVEL, ATTEND, WAIT, LEAVE, RETURN.
What you attempt is a proposal. The person decides what they can say or do.

ENTER
"""


def _print_surface(result: dict) -> None:
    for line in result.get("surface", []):
        print(line)
    meta = {}
    for key in ("status", "accepted", "contact", "outcome", "clock", "scene_open",
                "strategy", "contract_hash"):
        if key in result:
            meta[key] = result[key]
    admission = result.get("admission")
    if admission:
        meta["admission_id"] = admission.get("admission_id")
        meta["speech_event_id"] = admission.get("speech_event_id")
        meta["action_event_id"] = admission.get("action_event_id")
        meta["motive_status"] = admission.get("motive_status")
    if meta:
        print(json.dumps({"meta": meta}, indent=2, sort_keys=True, default=str))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="R31E first-neighbor session")
    parser.add_argument("--state", required=True)
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
            session = R31ESession.start(state, scenario=args.scenario,
                                        attention=args.attention)
            print(PRIMER)
            world = session.world()
            print(f"Clock {world.clock}. Your position: {world.positions.get('U')}.")
            print("The repair worker is at the bench. The finisher is folding pieces near the door.")
            print("The scene has already started.\n")
            print(json.dumps(session.status(), indent=2, sort_keys=True))
            session.close()
            return 0
        session = R31ESession.open(state)
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
                print(json.dumps(session.advance_offscreen(args.hours),
                                 indent=2, sort_keys=True, default=str))
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
