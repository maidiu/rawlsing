#!/usr/bin/env python3
"""One sourcefree house, using the received encounter ledger and world store."""

import argparse
import fcntl
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

from outward import OPERATIONS, establish_demo_conditions, perform as perform_outward
from situated import reconsider
from situated_provider import ModelUnavailable, SituatedProvider

def PACE(fanin, action):
    # Off-room location is not evidence of obstruction. Use the received
    # UNKNOWN mode so elapsed time records no fabricated workshop cause.
    mode = "ACTUAL" if fanin.session.world().positions.get("A") == "workshop" else "UNKNOWN"
    return advance_for_action(fanin, action, on_repair=close_on_repair, mode=mode)


def experience(state, args, *, interpret=None, realize=None, actor_context=None, provider_mode="INJECTED"):
    command = args.command
    if command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    gaze_file = state / "p6_gaze.json"
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == "new":
            def establish_scene(session):
                establish(session)
                if getattr(args, "situated_house", False):
                    establish_demo_conditions(session)

            new(state, ledger_file, "recognized_plan", seed=WORKSHOP_SEED, establish=establish_scene)
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
            if command in ({"go", "look", "wait", "attend", "inspect"} | OPERATIONS.keys()) and invitation(session, ledger):
                raise RecursionRefusal("P6_INVITATION_REQUIRES_EXPLICIT_RESPONSE")
            if command == "wait":
                if type(args.duration) is not int or not 1 <= args.duration <= 60:
                    raise RecursionRefusal("P6_WAIT_DURATION_OUT_OF_RANGE")

                def wait(current, admitted):
                    if not current.scene_open():
                        return {}, {"admission": "SCENE_CLOSED", "performed": False, "observation": None}
                    receipt = {"interval": PACE(owner.base_owner.fanin, admitted)}
                    decision = reconsider(current, receipt, interpret, realize, actor_context=actor_context, provider_mode=provider_mode)
                    if decision is not None:
                        receipt["situated"] = decision
                    return receipt, {"admission": "ADMITTED", "performed": True, "observation": None}

                outcome = act(owner, ledger_file, ledger, args,
                              conduct=({"operation": "WAIT", "duration": args.duration}, wait))
            elif command in OPERATIONS or command in {"go", "look"}:
                if command in OPERATIONS:
                    action = {"operation": OPERATIONS[command]}
                    writer = perform_outward
                else:
                    action = {"operation": "GO" if command == "go" else "INSPECT_OBJECT",
                              "target": args.target}
                    writer = perform

                def perform_with_time(current, admitted):
                    receipt, public = writer(current, admitted)
                    if public["performed"]:
                        receipt["interval"] = PACE(owner.base_owner.fanin, admitted)
                        if receipt.get("outward_cue") or any(row["recipient"] == "A" and row["eligibility"] == "ELIGIBLE"
                               for row in receipt.get("encounter_evidence", ())):
                            decision = reconsider(current, receipt, interpret, realize, actor_context=actor_context, provider_mode=provider_mode)
                            if decision is not None:
                                receipt["situated"] = decision
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
    initialize = commands.add_parser("new")
    initialize.add_argument("--situated-house", action="store_true",
                            help="Establish the sourcefree workshop sensory conditions.")
    commands.add_parser("view")
    wait = commands.add_parser("wait")
    wait.add_argument("duration", type=int)
    wait.add_argument("--request-id")
    say = commands.add_parser("say")
    say.add_argument("text")
    say.add_argument("--request-edge", action="store_true")
    say.add_argument("--request-id")
    for name in ("go", "look"):
        command = commands.add_parser(name)
        command.add_argument("target")
        command.add_argument("--request-id")
    for name in OPERATIONS:
        commands.add_parser(name).add_argument("--request-id")
    for name in ("attend", "inspect", "inspect-edge"):
        command = commands.add_parser(name)
        command.add_argument("--request-id")
        if name == "inspect-edge":
            command.add_argument("invitation")
            command.set_defaults(then_wait=False)
    args = parser.parse_args()
    try:
        provider = SituatedProvider.from_environment()
        result = experience(
            args.state.resolve(), args,
            interpret=provider.interpret if provider else None,
            realize=provider.realize if provider and provider.expressive_model else None,
            provider_mode="CONFIGURED_TRANSPORT" if provider else "UNCONFIGURED",
        )
    except (RecursionRefusal, ModelUnavailable, FileNotFoundError) as exc:
        print(json.dumps({"status": "REFUSED", "reason": str(exc) if isinstance(exc, (RecursionRefusal, ModelUnavailable))
                          else "P6_STATE_OR_SOURCE_MISSING"}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
