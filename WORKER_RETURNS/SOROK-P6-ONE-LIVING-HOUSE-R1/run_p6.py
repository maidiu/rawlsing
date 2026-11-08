#!/usr/bin/env python3
"""One sourcefree house, using the received encounter ledger and world store."""

import argparse
import fcntl
from functools import partial
import json
from pathlib import Path
import sys

RETURNS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RETURNS / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"))

from run_p5 import WORKSHOP_SEED, act, advance_for_action, check_source, invitation, new, open_owner, save, surface
from developmental_recursion.contracts import RecursionRefusal
from attention import register, select
from gaze import render
from house import close_on_repair, derive_recognition, establish, perform, read_house, scene

PACE = partial(advance_for_action, on_repair=close_on_repair)


def experience(state, args):
    command = args.command
    if command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    gaze_file = state / "p6_gaze.json"
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == "new":
            new(state, ledger_file, "recognized_plan", seed=WORKSHOP_SEED, establish=establish)
        ledger = json.loads(ledger_file.read_text())
        if ledger["pending"]:
            raise RecursionRefusal("P4_PENDING_OPERATION_REQUIRES_RECONCILIATION")
        owner = open_owner(state / "actual-p2")
        try:
            check_source(owner)
            session = owner.base_owner.fanin.session
            _world, committed_house = read_house(session)
            committed_objects = {ref: dict(row) for ref, row in committed_house["objects"].items()}
            expected = (ledger["turns"][-1]["after"] if ledger["turns"]
                        else ledger["antecedent"]["identity"])
            if owner.snapshot().document() != expected:
                raise RecursionRefusal("P4_COLD_STATE_MISMATCH")
            prior = scene(session)
            outcome = None
            if command in {"go", "look", "attend", "inspect"} and invitation(session, ledger):
                raise RecursionRefusal("P6_INVITATION_REQUIRES_EXPLICIT_RESPONSE")
            if command in {"go", "look"}:
                action = {"operation": "GO" if command == "go" else "INSPECT_OBJECT",
                          "target": args.target}

                def perform_with_time(current, admitted):
                    receipt, public = perform(current, admitted)
                    if public["performed"]:
                        receipt["interval"] = PACE(owner.base_owner.fanin, admitted)
                    return receipt, public

                outcome = act(owner, ledger_file, ledger, args,
                              conduct=(action, perform_with_time))
            elif command in {"say", "attend", "inspect", "inspect-edge"}:
                outcome = act(owner, ledger_file, ledger, args, pacing=PACE)
            view = surface(owner, ledger)
            authoritative_events = {
                row["event_id"]: row for row in session.events()
                if row.get("event_id")
            }
            user_visible_ids = set(session.user_perceived_ids())
            frame = scene(session)
        finally:
            owner.close()
        latest = ledger["turns"][-1] if ledger["turns"] else None
        candidates = None
        boundary = view["invitation"]
        if latest:
            start = latest["before"]["clock"]
            candidates = [row["event_id"] for row in view["observations"] if row["clock"] >= start]
            evidence = latest["receipt"].get("expression") or latest["receipt"].get("performed")
            if boundary is None and evidence:
                boundary = evidence["event_id"]
        profile = (json.loads(gaze_file.read_text()) if gaze_file.exists()
                   else {"history": [], "exposure": {}})
        if command == "look" and outcome["performed"] and latest["action"].get("target") == args.target:
            register(profile, prior, args.target, len(ledger["turns"]))
        profile["recognized"] = derive_recognition(
            committed_objects, ledger["turns"], authoritative_events, user_visible_ids)
        objects = frame.pop("objects")
        selected = select(objects, profile["history"])
        profile["exposure"] = {"room": frame["room"], "detail": selected}
        save(gaze_file, profile)
        recognized = profile["recognized"].get(selected) if selected else None
        result = {"clock": view["clock"], **frame, "available": sorted(objects),
                  "detail": objects.get(selected),
                  "recognized_identity": (recognized["identity"] if recognized else None),
                  "recognition": dict(profile["recognized"]),
                  "narration": render(view, [], candidates=candidates, boundary=boundary),
                  "invitation": view["invitation"]}
        if outcome is not None:
            result["admission"] = outcome["admission"]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("new")
    commands.add_parser("view")
    say = commands.add_parser("say")
    say.add_argument("text")
    say.add_argument("--request-edge", action="store_true")
    say.add_argument("--request-id")
    for name in ("go", "look"):
        command = commands.add_parser(name)
        command.add_argument("target")
        command.add_argument("--request-id")
    for name in ("attend", "inspect", "inspect-edge"):
        command = commands.add_parser(name)
        command.add_argument("--request-id")
        if name == "inspect-edge":
            command.add_argument("invitation")
            command.set_defaults(then_wait=False)
    args = parser.parse_args()
    try:
        result = experience(args.state.resolve(), args)
    except (RecursionRefusal, FileNotFoundError) as exc:
        print(json.dumps({"status": "REFUSED", "reason": str(exc) if isinstance(exc, RecursionRefusal)
                          else "P6_STATE_OR_SOURCE_MISSING"}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
