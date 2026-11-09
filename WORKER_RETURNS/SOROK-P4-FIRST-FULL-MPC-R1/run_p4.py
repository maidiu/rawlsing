#!/usr/bin/env python3
"""Persistent sourcefree P4 encounter. Stdout is the user-visible surface."""
import argparse
import fcntl
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
P3 = ROOT.parent / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
sys.path.insert(0, str(P3 / "tests"))

# Reuse the received sourcefree scenario constructors. They provide antecedent
# data only. All user operations come from this CLI's caller.
from p3_fixture_support import build_case
from developmental_recursion.contracts import RecursionRefusal, canonical
from developmental_recursion.p2_owner import P2Owner, load_p2
from p3.p3_owner import CONFIG_FILE, P3Owner
from response import OPENING_FORMATION_ID, check_source, express, read_response
from speech import admit_speech

GRADE = "SOURCEFREE_TEST_ONLY"


def save(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(canonical(value), encoding="utf-8")
    temporary.replace(path)


def advance(fanin, *, mode="ACTUAL"):
    session = fanin.session
    start = session.clock()
    domain = fanin.deps["make_domain"](mode=mode, start=start, end=start + 2)
    return session.produce_interval(domain)


def open_owner(root):
    config = json.loads((root / CONFIG_FILE).read_text())["config"]
    fanin = load_p2().open(root)
    case = fanin.deps["case_for"](True)
    base = P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
                   participants=tuple(fanin.session.read_root()["actor_ids"]))
    try:
        return P3Owner(base, **{key: config[key] for key in
                               ("source", "history", "plans", "catalog",
                                "compression_specs", "standpoints")})
    except BaseException:
        base.close()
        raise


def invitation(session, ledger):
    latest = next((turn for turn in reversed(ledger["turns"])
                   if turn["public"]["performed"]), {})
    receipt = latest.get("receipt", {})
    event = receipt.get("expression")
    if (receipt.get("uptake", {}).get("mode") == "joint_check" and event
            and session.event(event["event_id"]) == event
            and event["event_id"] in session.user_perceived_ids()):
        return event["event_id"]
    return None


def surface(owner, ledger):
    fanin = owner.base_owner.fanin
    view = fanin.view()
    invited = invitation(fanin.session, ledger)
    choices = ["SAY", "REQUEST_EDGE"]
    if invited:
        choices.append("INSPECT_EDGE")
    opening_clock = ledger["antecedent"]["identity"]["clock"]
    observations = [
        row for row in view["visible_events"]
        if row["clock"] >= opening_clock or row["kind"] == "ARRIVAL"
    ]
    return {"grade": GRADE, "clock": fanin.session.clock(),
            "location": view.get("location"),
            "tool_available": view.get("tool_available"),
            "observations": observations,
            "choices": choices, "invitation": invited}


def new(state, ledger_file, history, *, seed="01" * 32, establish=None):
    if ledger_file.exists() or (state / "actual-p2").exists():
        raise RecursionRefusal("P4_STATE_ALREADY_EXISTS")
    case = build_case(state, history_outcomes=(history,) if history else (),
                      include_compression=False, standpoints=False, seed=seed)
    try:
        owner = case.owner
        formation = owner.realize(OPENING_FORMATION_ID, case.proposals[0], owner.snapshot())
        interval = advance(case.base_owner.fanin, mode="SCHEDULED_ONLY")
        if establish is not None:
            establish(case.base_owner.fanin.session)
        plan = case.plans[0]
        ledger = {"scope": {key: plan[key] for key in
                            ("project", "counterpart", "interlocutor_role")},
                  "antecedent": {"formation": formation.receipt_ref,
                                 "identity": owner.snapshot().document(),
                                 "interval": interval,
                                 "psychology_head": owner.store.head()},
                  "turns": [], "pending": None}
        ledger["scope"]["relation_ref"] = plan["relation_refs"][0]
        save(ledger_file, ledger)
        return surface(owner, ledger)
    finally:
        case.cycle.engine.close()
        case.owner.close()


def act(owner, ledger_file, ledger, args, *, pacing=None, conduct=None, transduce=None):
    fanin = owner.base_owner.fanin
    session = fanin.session
    before = owner.snapshot().document()
    if conduct is not None:
        action, perform = conduct
    elif args.command == "say":
        action = {"operation": "SAY", "text": args.text, "request_edge": args.request_edge}
    elif args.command == "inspect-edge":
        action = {"operation": "INSPECT_EDGE", "invitation": args.invitation}
        if args.then_wait:
            action["then_wait"] = True
    elif pacing is not None and args.command in {"inspect", "attend"}:
        action = {"operation": args.command.upper()}
    else:
        raise RecursionRefusal("P4_ACTION_UNSUPPORTED")
    if pacing is not None:
        action["pacing"] = "P5"
        if args.command in {"inspect", "inspect-edge"} and getattr(args, "thorough", False):
            action["thorough"] = True
    if args.request_id:
        for turn in ledger["turns"]:
            if turn["request_id"] != args.request_id:
                continue
            if turn["action"] != action:
                raise RecursionRefusal("P4_REQUEST_REUSE_MISMATCH")
            return turn["public"]

    ledger["pending"] = {"action": action, "before": before, "request_id": args.request_id}
    save(ledger_file, ledger)
    if conduct is not None:
        receipt, public = perform(session, action)
    elif args.command == "say":
        speech = admit_speech(session, text=args.text, actor_ref=before["actor"],
                              request_edge=args.request_edge)
        uptake = read_response(owner, speech, ledger["scope"], transduce=transduce)
        expression, observation = express(session, uptake)
        offers_inspection = uptake["mode"] == "joint_check" and observation is not None
        interval = None
        if speech["performed"] and not offers_inspection:
            interval = (advance(fanin) if pacing is None else pacing(fanin, action))
        receipt = {"speech": speech, "uptake": uptake, "expression": expression,
                   "interval": interval}
        public = {"admission": speech["admission"], "performed": speech["performed"] is not None,
                  "observation": observation}
    elif args.command in {"inspect", "inspect-edge"}:
        from s45_projection.projection import project_event

        token = action.get("invitation")
        valid = session.scene_open() and (
            args.command == "inspect" or token == invitation(session, ledger)
        )
        event = None
        if valid:
            session.inspect()
            event = session.events()[-1]
            if (event["kind"] != "INSPECT"
                    or event["actor_id"] != session.meta["user_actor"]
                    or event["event_id"] not in session.user_perceived_ids()):
                raise RecursionRefusal("P4_INSPECTION_RECEIPT_MISSING")
        interval = None
        if valid:
            if pacing is not None:
                interval = pacing(fanin, action)
            elif args.then_wait:
                interval = advance(fanin)
        receipt = {"performed": event, "invitation": token, "interval": interval}
        public = {"admission": "ADMITTED" if valid else "INVITATION_UNAVAILABLE",
                  "performed": valid, "observation": project_event(event) if valid else None}
    else:
        valid = session.scene_open()
        interval = None
        result = None
        if valid:
            before_ids = session.user_perceived_ids()
            result = session.attend()
            # The received attention action can cause an actor to initiate.
            # Return before compressing time if a new utterance is perceived.
            newly_perceived = session.user_perceived_ids() - before_ids
            if not any(session.event(ref)["kind"] == "SPEECH" for ref in newly_perceived):
                interval = pacing(fanin, action)
        receipt = {"attention": result, "interval": interval}
        public = {"admission": "ADMITTED" if valid else "SCENE_CLOSED",
                  "performed": valid, "observation": None}

    ledger["turns"].append({"action": action, "request_id": args.request_id,
                            "receipt": receipt, "before": before,
                            "after": owner.snapshot().document(), "public": public})
    ledger["pending"] = None
    public["next"] = surface(owner, ledger)
    save(ledger_file, ledger)
    return public


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("new")
    initialize.add_argument("--history", choices=("recognized_plan", "imposed_plan", ""),
                            default="recognized_plan")
    commands.add_parser("view")
    say = commands.add_parser("say")
    say.add_argument("text")
    say.add_argument("--request-edge", action="store_true",
                     help="Explicitly ask the Other to look at the edge with you.")
    say.add_argument("--request-id")
    inspect = commands.add_parser("inspect-edge")
    inspect.add_argument("invitation")
    inspect.add_argument("--request-id")
    inspect.add_argument("--then-wait", action="store_true",
                         help="After inspection, let two workshop clock units pass.")
    args = parser.parse_args()

    state = args.state.resolve()
    if args.command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    try:
        with (state / "p4.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if args.command == "new":
                result = new(state, ledger_file, args.history)
            else:
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
                    result = (surface(owner, ledger) if args.command == "view" else
                              act(owner, ledger_file, ledger, args))
                finally:
                    owner.close()
    except (RecursionRefusal, FileNotFoundError) as exc:
        print(json.dumps({"grade": GRADE, "status": "REFUSED",
                          "reason": str(exc) if isinstance(exc, RecursionRefusal) else
                          "P4_STATE_OR_SOURCE_MISSING"}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
