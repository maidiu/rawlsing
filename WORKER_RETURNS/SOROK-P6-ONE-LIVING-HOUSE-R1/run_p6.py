#!/usr/bin/env python3
"""One sourcefree house, using the received encounter ledger and world store."""

import argparse
import fcntl
import json
from pathlib import Path
import sys
import time

RETURNS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RETURNS / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"))

from run_p5 import WORKSHOP_SEED, act, advance_for_action, check_boundary, check_source, invitation, new, open_owner, save, surface
from developmental_recursion.contracts import RecursionRefusal
from attention import register
from gaze import render
from house import close_on_repair, derive_recognition, establish, establish_gallery, establish_symbolic, perform, read_house, scene
import mii

from outward import OPERATIONS, establish_demo_conditions, perform as perform_outward
from situated import reconsider
from situated_provider import ModelUnavailable, SituatedProvider

def PACE(fanin, action):
    # Off-room location is not evidence of obstruction. Use the received
    # UNKNOWN mode so elapsed time records no fabricated workshop cause.
    mode = "ACTUAL" if fanin.session.world().positions.get("A") == "workshop" else "UNKNOWN"
    return advance_for_action(fanin, action, on_repair=close_on_repair, mode=mode)


def experience(state, args, *, interpret=None, realize=None, actor_context=None,
               provider_mode="INJECTED", timings=None, sourcefree_p3_bridge=False):
    started = time.perf_counter()
    cursor = started
    command = args.command
    if command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    gaze_file = state / "p6_gaze.json"
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == "new":
            def establish_scene(session):
                if getattr(args, "scene", "house") == "gallery":
                    establish_gallery(session)
                elif getattr(args, "scene", "house") == "symbolic":
                    establish_symbolic(session)
                else:
                    establish(session)
                    if getattr(args, "situated_house", False):
                        establish_demo_conditions(session)

            new(state, ledger_file, "recognized_plan", seed=WORKSHOP_SEED, establish=establish_scene)
        ledger = json.loads(ledger_file.read_text())
        turns_before = len(ledger["turns"])
        if ledger["pending"]:
            raise RecursionRefusal("P4_PENDING_OPERATION_REQUIRES_RECONCILIATION")
        owner = open_owner(state / "actual-p2")
        try:
            check_source(owner)
            session = owner.base_owner.fanin.session
            _world, committed_house = read_house(session)
            committed_objects = {ref: dict(row) for ref, row in committed_house["objects"].items()}
            if command.startswith("mii-"):
                if command in {"mii-learn-label", "mii-correct-label",
                               "mii-correct-attention"}:
                    target = getattr(args, "target", None)
                    if target not in committed_objects:
                        raise RecursionRefusal("MII_TARGET_UNKNOWN")
                profile = mii.load_profile(gaze_file, session)
                try:
                    profile, result = mii.control(
                        profile, command, args,
                        turn=len(ledger["turns"]), clock=session.clock(),
                    )
                except ValueError as exc:
                    raise RecursionRefusal(str(exc)) from exc
                mii.save_profile(gaze_file, profile)
                return result
            check_boundary(owner, ledger)
            bridge_kwargs = ({"psyche_owner": owner, "psyche_scope": ledger["scope"]}
                             if sourcefree_p3_bridge else {})
            prior = scene(session)
            outcome = None
            if command in ({"go", "look", "wait", "attend", "inspect", "inspect-particular"} | OPERATIONS.keys()) and invitation(session, ledger):
                raise RecursionRefusal("P6_INVITATION_REQUIRES_EXPLICIT_RESPONSE")
            if command == "wait":
                if type(args.duration) is not int or not 1 <= args.duration <= 60:
                    raise RecursionRefusal("P6_WAIT_DURATION_OUT_OF_RANGE")

                def wait(current, admitted):
                    if not current.scene_open():
                        return {}, {"admission": "SCENE_CLOSED", "performed": False, "observation": None}
                    receipt = {"interval": PACE(owner.base_owner.fanin, admitted)}
                    decision = reconsider(current, receipt, interpret, realize, actor_context=actor_context, provider_mode=provider_mode, **bridge_kwargs)
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
                            decision = reconsider(current, receipt, interpret, realize, actor_context=actor_context, provider_mode=provider_mode, **bridge_kwargs)
                            if decision is not None:
                                receipt["situated"] = decision
                    return receipt, public

                outcome = act(owner, ledger_file, ledger, args,
                              conduct=(action, perform_with_time))
            elif command in {"say", "attend", "inspect", "inspect-particular", "inspect-edge"}:
                outcome = act(owner, ledger_file, ledger, args, pacing=PACE)
            view = surface(owner, ledger)
            authoritative_events = {
                row["event_id"]: row for row in session.events()
                if row.get("event_id")
            }
            user_visible_ids = set(session.user_perceived_ids())
            frame = scene(session)
            profile = mii.load_profile(gaze_file, session)
            if timings is not None:
                now = time.perf_counter()
                timings["initialization_s"] = now - cursor
                cursor = now
        finally:
            owner.close()
        replayed = len(ledger["turns"]) == turns_before
        latest = ledger["turns"][-1] if ledger["turns"] else None
        event_candidates = None
        boundary = view["invitation"]
        if latest:
            start = latest["before"]["clock"]
            event_candidates = [row["event_id"] for row in view["observations"] if row["clock"] >= start]
            evidence = latest["receipt"].get("expression") or latest["receipt"].get("performed")
            if boundary is None and evidence:
                boundary = evidence["event_id"]
        if command == "look" and outcome["performed"] and latest["action"].get("target") == args.target:
            register(profile, prior, args.target, len(ledger["turns"]))
        mii.merge_recognition(profile, derive_recognition(
            committed_objects, ledger["turns"], authoritative_events, user_visible_ids))
        if timings is not None:
            now = time.perf_counter()
            timings["ledger_s"] = now - cursor
            cursor = now
        objects = frame.pop("objects")
        detail_candidates = mii.candidate_details(
            committed_house, frame["room"], objects, session.meta["user_actor"]
        )
        if timings is not None:
            now = time.perf_counter()
            timings["availability_s"] = now - cursor
            cursor = now
        selected, basis = mii.select_detail(
            objects, profile, command=command,
            target=getattr(args, "target", None), offered=detail_candidates,
        )
        offered = (
            {selected: detail_candidates[selected]} if selected in detail_candidates else {}
        )
        prior_offered = (
            profile["exposures"][-1].get("offered") if profile["exposures"] else {}
        )
        narration = render(view, [], candidates=event_candidates, boundary=boundary)
        rendered = [{"kind": "event", "event_id": row["event_id"]} for row in narration]
        exposure_count_before = len(profile["exposures"])
        exposure = mii.record_exposure(
            profile, turn=len(ledger["turns"]), clock=view["clock"],
            available=sorted(objects), candidates=detail_candidates,
            offered=offered, selected=selected, rendered=rendered, basis=basis,
            request_id=getattr(args, "request_id", None),
            context={"room": frame["room"], "command": command},
        )
        exposure_created = len(profile["exposures"]) > exposure_count_before
        if (command == "look" and outcome["performed"]
                and latest["action"].get("target") == getattr(args, "target", None)
                and (not replayed or exposure_created)):
            mii.update_attention(
                profile, target=args.target, prior_offered=prior_offered,
                command=command, turn=len(ledger["turns"]),
            )
        if timings is not None:
            now = time.perf_counter()
            timings["recognition_update_s"] = now - cursor
            cursor = now
        mii.save_profile(gaze_file, profile)
        recognized = mii.recognized_for(profile, selected)
        mii_surface = mii.surface(
            room=frame["room"], orientation=frame["orientation"],
            exit_name=frame["exit"], available=objects, candidates=detail_candidates,
            offered=offered, selected=selected, basis=basis, narration=narration,
            recognition=profile["recognized"],
        )
        if timings is not None:
            now = time.perf_counter()
            timings["composition_s"] = now - cursor
            cursor = now
        result = {"clock": view["clock"], **frame, "available": sorted(objects),
                  "detail": objects.get(selected),
                  "recognized_identity": (recognized["identity"] if recognized else None),
                  "recognition": dict(profile["recognized"]),
                  "recognition_source": (recognized or {}).get("recognition_source"),
                  "narration": narration,
                  "mii_surface": mii_surface,
                  "mii": mii.status(profile),
                  "mii_exposure_id": exposure["exposure_id"],
                  "invitation": view["invitation"]}
        if view.get("historical_particulars"):
            result["historical_particulars"] = view["historical_particulars"]
        if command == "inspect-particular" and outcome is not None:
            result["observation"] = outcome["observation"]
        if outcome is not None:
            result["admission"] = outcome["admission"]
        if timings is not None:
            timings["total_s"] = time.perf_counter() - started
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--sourcefree-p3-bridge", action="store_true",
                        help="Explicit test-only P3 actor readset in P6 situated decisions")
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("new")
    initialize.add_argument("--situated-house", action="store_true",
                            help="Establish the sourcefree workshop sensory conditions.")
    initialize.add_argument("--scene", choices=("house", "gallery", "symbolic"), default="house",
                            help="Select the sourcefree presentation fixture.")
    particular = commands.add_parser("inspect-particular")
    particular.add_argument("target")
    particular.add_argument("--property")
    particular.add_argument("--request-id")
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
    commands.add_parser("mii-status")
    commands.add_parser("mii-export")
    commands.add_parser("mii-reset")
    commands.add_parser("mii-stop-learning")
    commands.add_parser("mii-enable-learning")
    learn = commands.add_parser("mii-learn-label")
    learn.add_argument("--target", required=True)
    learn.add_argument("--label", required=True)
    correct_label = commands.add_parser("mii-correct-label")
    correct_label.add_argument("--target", required=True)
    correct_label.add_argument("--label", default="")
    correct_attention = commands.add_parser("mii-correct-attention")
    correct_attention.add_argument("--target", required=True)
    correct_attention.add_argument("--weight", type=int, default=0)
    args = parser.parse_args()
    try:
        provider = SituatedProvider.from_environment()
        result = experience(
            args.state.resolve(), args,
            interpret=provider.interpret if provider else None,
            realize=provider.realize if provider and provider.expressive_model else None,
            provider_mode="CONFIGURED_TRANSPORT" if provider else "UNCONFIGURED",
            sourcefree_p3_bridge=args.sourcefree_p3_bridge,
        )
    except (RecursionRefusal, ModelUnavailable, FileNotFoundError) as exc:
        print(json.dumps({"status": "REFUSED", "reason": str(exc) if isinstance(exc, (RecursionRefusal, ModelUnavailable))
                          else "P6_STATE_OR_SOURCE_MISSING"}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
