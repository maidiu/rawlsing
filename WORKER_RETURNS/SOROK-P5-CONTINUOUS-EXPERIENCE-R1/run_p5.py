#!/usr/bin/env python3
"""Sourcefree situated reader over the received P4 encounter."""

import argparse
import fcntl
import json
from pathlib import Path
import sys

P4 = Path(__file__).resolve().parent.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
sys.path.insert(0, str(P4))

from run_p4 import act, check_boundary, invitation, new, open_owner, save, surface
from response import check_source
from developmental_recursion.contracts import RecursionRefusal

from gaze import attend, render
from pacing import advance_for_action

# This received S44 draw has stock for more than one repair after its prehistory.
WORKSHOP_SEED = "05" * 32


def experience(state, args):
    command = args.command
    if command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    gaze_file = state / "p5_gaze.json"
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == "new":
            new(state, ledger_file, args.history, seed=WORKSHOP_SEED)
        ledger = json.loads(ledger_file.read_text())
        if ledger["pending"]:
            raise RecursionRefusal("P4_PENDING_OPERATION_REQUIRES_RECONCILIATION")
        owner = open_owner(state / "actual-p2")
        try:
            check_source(owner)
            check_boundary(owner, ledger)
            outcome = None
            if command in {"say", "inspect", "inspect-particular", "inspect-edge", "attend"}:
                if (command in {"inspect", "attend"}
                        and invitation(owner.base_owner.fanin.session, ledger)):
                    raise RecursionRefusal("P5_INVITATION_REQUIRES_EXPLICIT_RESPONSE")
                outcome = act(owner, ledger_file, ledger, args, pacing=advance_for_action)
            view = surface(owner, ledger)
        finally:
            owner.close()

        history = json.loads(gaze_file.read_text()) if gaze_file.exists() else []
        if command == "orient":
            history = attend(view, history, args.event_id)
            if history is None:
                raise RecursionRefusal("P5_OCCURRENCE_UNAVAILABLE")
            save(gaze_file, history)
        candidates = None
        boundary = view["invitation"]
        if ledger["turns"]:
            latest = ledger["turns"][-1]
            start = latest["before"]["clock"]
            # Keep a direct answer audible when the received perception
            # confirms it, including a response that offers no joint work.
            reply = latest["receipt"].get("expression")
            if boundary is None and reply is not None:
                boundary = reply["event_id"]
            candidates = [event["event_id"] for event in view["observations"]
                          if event["clock"] >= start]
        narration = render(view, history, candidates=candidates, boundary=boundary)
        result = {
            "grade": view["grade"],
            "clock": view["clock"],
            "location": view["location"],
            "narration": narration,
            "choices": view["choices"] if view["invitation"] else [*view["choices"], "ATTEND", "INSPECT"],
            "invitation": view["invitation"],
        }
        if view.get("historical_particulars"):
            result["historical_particulars"] = view["historical_particulars"]
        if command == "inspect-particular" and outcome is not None:
            result["observation"] = outcome["observation"]
        if outcome is not None:
            result["admission"] = outcome["admission"]
            result["performed"] = outcome["performed"]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("new")
    initialize.add_argument("--history", choices=("recognized_plan", "imposed_plan", ""),
                            default="recognized_plan")
    say = commands.add_parser("say")
    say.add_argument("text")
    say.add_argument("--request-edge", action="store_true")
    say.add_argument("--request-id")
    inspect_edge = commands.add_parser("inspect-edge")
    inspect_edge.add_argument("invitation")
    inspect_edge.set_defaults(then_wait=False)
    inspect_edge.add_argument("--request-id")
    inspect = commands.add_parser("inspect")
    for examination in (inspect, inspect_edge):
        examination.add_argument("--thorough", action="store_true",
                                 help="Continue a closer examination for two work periods.")
    inspect.add_argument("--request-id")
    commands.add_parser("attend").add_argument("--request-id")
    particular = commands.add_parser("inspect-particular")
    particular.add_argument("target")
    particular.add_argument("--property")
    particular.add_argument("--request-id")
    commands.add_parser("view")
    orient = commands.add_parser("orient", help="Register interest in a perceived occurrence.")
    orient.add_argument("event_id")
    args = parser.parse_args()
    try:
        result = experience(args.state.resolve(), args)
    except (RecursionRefusal, FileNotFoundError) as exc:
        reason = str(exc) if isinstance(exc, RecursionRefusal) else "P5_STATE_OR_SOURCE_MISSING"
        print(json.dumps({"status": "REFUSED", "reason": reason}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
