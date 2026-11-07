#!/usr/bin/env python3
"""Sourcefree situated reader over the received P4 encounter."""

import argparse
import fcntl
import json
from pathlib import Path
import sys

P4 = Path(__file__).resolve().parent.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
sys.path.insert(0, str(P4))

from run_p4 import new, open_owner, save, surface
from response import check_source
from developmental_recursion.contracts import RecursionRefusal

from gaze import attend, render


def experience(state, command, *, event_id=None):
    if command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    gaze_file = state / "p5_gaze.json"
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == "new":
            new(state, ledger_file, "recognized_plan")
        ledger = json.loads(ledger_file.read_text())
        if ledger["pending"]:
            raise RecursionRefusal("P4_PENDING_OPERATION_REQUIRES_RECONCILIATION")
        owner = open_owner(state / "actual-p2")
        try:
            check_source(owner)
            expected = (ledger["turns"][-1]["after"] if ledger["turns"]
                        else ledger["antecedent"]["identity"])
            if owner.snapshot().document() != expected:
                raise RecursionRefusal("P4_COLD_STATE_MISMATCH")
            view = surface(owner, ledger)
        finally:
            owner.close()

        history = json.loads(gaze_file.read_text()) if gaze_file.exists() else []
        if command == "orient":
            history = attend(view, history, event_id)
            if history is None:
                raise RecursionRefusal("P5_OCCURRENCE_UNAVAILABLE")
            save(gaze_file, history)
        return {
            "grade": view["grade"],
            "clock": view["clock"],
            "location": view["location"],
            "narration": render(view, history, boundary=view["invitation"]),
            "choices": view["choices"],
            "invitation": view["invitation"],
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("new")
    commands.add_parser("view")
    orient = commands.add_parser("orient", help="Register interest in a perceived occurrence.")
    orient.add_argument("event_id")
    args = parser.parse_args()
    try:
        result = experience(args.state.resolve(), args.command,
                            event_id=getattr(args, "event_id", None))
    except (RecursionRefusal, FileNotFoundError) as exc:
        reason = str(exc) if isinstance(exc, RecursionRefusal) else "P5_STATE_OR_SOURCE_MISSING"
        print(json.dumps({"status": "REFUSED", "reason": reason}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
