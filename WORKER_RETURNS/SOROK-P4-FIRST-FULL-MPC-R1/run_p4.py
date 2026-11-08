#!/usr/bin/env python3
"""Persistent sourcefree P4 encounter. Stdout is the user-visible surface."""
import argparse
from contextlib import contextmanager
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
P3 = ROOT.parent / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
sys.path.insert(0, str(P3 / "tests"))
sys.path.append(str(ROOT.parents[1]))

# Reuse the received sourcefree scenario constructors. They provide antecedent
# data only. All user operations come from this CLI's caller.
from p3_fixture_support import build_case
from developmental_recursion.contracts import RecursionRefusal, canonical, digest
from developmental_recursion.p2_owner import P2Owner, load_p2
from p3.p3_owner import CONFIG_FILE, P3Owner
from rawlsing_next.sorok_history.owner import (
    HistoricalWorld, HistoryRefusal, RESOURCE, VISIBLE_PHYSICAL,
)
from response import check_source, express, read_response
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
    result = {"grade": GRADE, "clock": fanin.session.clock(),
            "location": view.get("location"),
            "tool_available": view.get("tool_available"),
            "observations": observations,
            "choices": choices, "invitation": invited}
    particulars = HistoricalWorld(fanin.session).visible_surfaces()
    if particulars:
        result["historical_particulars"] = list(particulars)
    return result


def foreground_witness(owner, identity):
    """Bind all foreground and actor state while the history owner advances."""
    session = owner.base_owner.fanin.session
    world = session.world().snapshot()
    world.pop("hash")
    world["resources"].pop(RESOURCE, None)
    return digest({
        "scope": {key: value for key, value in identity.items() if key != "state_hash"},
        "world": world, "events": session.read_events(),
        "intervals": session.read_interval_states(), "encounters": session.read_encounters(),
        "psychology_head": owner.store.head(), "config_hash": owner.config_hash,
    })


def new(state, ledger_file, history):
    if ledger_file.exists() or (state / "actual-p2").exists():
        raise RecursionRefusal("P4_STATE_ALREADY_EXISTS")
    case = build_case(state, history_outcomes=(history,) if history else (),
                      include_compression=False, standpoints=False)
    try:
        owner = case.owner
        formation = owner.realize("p4-formation", case.proposals[0], owner.snapshot())
        interval = advance(case.base_owner.fanin, mode="SCHEDULED_ONLY")
        HistoricalWorld(case.base_owner.fanin.session).capture_visible_tool_resource()
        plan = case.plans[0]
        identity = owner.snapshot().document()
        ledger = {"scope": {key: plan[key] for key in
                            ("project", "counterpart", "interlocutor_role")},
                  "antecedent": {"formation": formation.receipt_ref,
                                 "identity": identity,
                                 "foreground_witness": foreground_witness(owner, identity),
                                 "interval": interval,
                                 "psychology_head": owner.store.head()},
                  "turns": [], "pending": None}
        ledger["scope"]["relation_ref"] = plan["relation_refs"][0]
        save(ledger_file, ledger)
        return surface(owner, ledger)
    finally:
        case.cycle.engine.close()
        case.owner.close()


def act(owner, ledger_file, ledger, args):
    fanin = owner.base_owner.fanin
    session = fanin.session
    before = owner.snapshot().document()
    if args.command == "say":
        action = {"operation": "SAY", "text": args.text, "request_edge": args.request_edge}
    elif args.command == "inspect-particular":
        action = {"operation": "INSPECT_PARTICULAR", "target": args.target}
        predicate = getattr(args, "property", None)
        if predicate is not None:
            action["property"] = predicate
    else:
        action = {"operation": "INSPECT_EDGE", "invitation": args.invitation}
        if args.then_wait:
            action["then_wait"] = True
    if args.request_id:
        for turn in ledger["turns"]:
            if turn["request_id"] != args.request_id:
                continue
            if turn["action"] != action:
                raise RecursionRefusal("P4_REQUEST_REUSE_MISMATCH")
            return turn["public"]

    ledger["pending"] = {"action": action, "before": before, "request_id": args.request_id}
    save(ledger_file, ledger)
    if args.command == "say":
        speech = admit_speech(session, text=args.text, actor_ref=before["actor"],
                              request_edge=args.request_edge)
        uptake = read_response(owner, speech, ledger["scope"])
        expression, observation = express(session, uptake)
        offers_inspection = uptake["mode"] == "joint_check" and observation is not None
        interval = advance(fanin) if speech["performed"] and not offers_inspection else None
        receipt = {"speech": speech, "uptake": uptake, "expression": expression,
                   "interval": interval}
        public = {"admission": speech["admission"], "performed": speech["performed"] is not None,
                  "observation": observation}
    elif args.command == "inspect-particular":
        history = HistoricalWorld(session)
        try:
            event = history.inspect(args.target, predicate=predicate)
        except HistoryRefusal as exc:
            if str(exc) != "HISTORICAL_TARGET_UNAVAILABLE":
                raise
            receipt = {"performed": None, "reason": str(exc)}
            public = {"admission": "UNAVAILABLE", "performed": False, "observation": None}
        else:
            receipt = {"performed": event}
            public = {"admission": "ADMITTED", "performed": True,
                      "observation": history.read_inspection(event["event_id"])}
    else:
        from s45_projection.projection import project_event

        valid = session.scene_open() and args.invitation == invitation(session, ledger)
        event = None
        if valid:
            session.inspect()
            event = session.events()[-1]
            if (event["kind"] != "INSPECT"
                    or event["actor_id"] != session.meta["user_actor"]
                    or event["event_id"] not in session.user_perceived_ids()):
                raise RecursionRefusal("P4_INSPECTION_RECEIPT_MISSING")
        interval = advance(fanin) if valid and args.then_wait else None
        receipt = {"performed": event, "invitation": args.invitation, "interval": interval}
        public = {"admission": "ADMITTED" if valid else "INVITATION_UNAVAILABLE",
                  "performed": valid, "observation": project_event(event) if valid else None}

    after = owner.snapshot().document()
    ledger["turns"].append({"action": action, "request_id": args.request_id,
                            "receipt": receipt, "before": before,
                            "after": after, "foreground_witness": foreground_witness(owner, after),
                            "public": public})
    ledger["pending"] = None
    public["next"] = surface(owner, ledger)
    save(ledger_file, ledger)
    return public


@contextmanager
def foreground_lock(state):
    with (state / "p4.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def wake_history_worker(state, *, candidate_ready=False):
    """Start a bounded job after the foreground checkpoint and ledger are durable."""
    from rawlsing_next.sorok_history.provider import ProviderConfig

    config = ProviderConfig.from_environment()
    if not candidate_ready and not (config.endpoint and config.model):
        return
    try:
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--state", str(state), "history-worker"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        # The durable demand remains available to the explicit recovery command.
        print("Historical worker wake failed; durable demand retained.", file=sys.stderr)


def run_history_worker(state):
    """Use the foreground lock only for local owner operations."""
    import asyncio

    from rawlsing_next.sorok_history.provider import HistoricalModelProvider
    from rawlsing_next.sorok_history.runtime import run_once

    provider = HistoricalModelProvider.from_environment()
    with foreground_lock(state):
        owner = open_owner(state / "actual-p2")
    try:
        with foreground_lock(state):
            check_source(owner)
        history = HistoricalWorld(owner.base_owner.fanin.session)
        result = asyncio.run(run_once(
            history, provider if provider.live else None, guard=lambda: foreground_lock(state)
        ))
        return result if result is not None else {"status": "NO_WORK"}
    finally:
        owner.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("new")
    initialize.add_argument("--history", choices=("recognized_plan", "imposed_plan", ""),
                            default="recognized_plan")
    commands.add_parser("view")
    commands.add_parser("history-worker")
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
    particular = commands.add_parser("inspect-particular")
    particular.add_argument("target")
    particular.add_argument("--property", choices=sorted(VISIBLE_PHYSICAL))
    particular.add_argument("--request-id")
    args = parser.parse_args()

    state = args.state.resolve()
    if args.command == "new":
        state.mkdir(parents=True, exist_ok=True)
    ledger_file = state / "p4_receipts.json"
    recover_history = candidate_ready = False
    try:
        if args.command == "history-worker":
            print(json.dumps(run_history_worker(state), ensure_ascii=False))
            return 0
        with foreground_lock(state):
            if args.command == "new":
                result = new(state, ledger_file, args.history)
            else:
                ledger = json.loads(ledger_file.read_text())
                if ledger["pending"]:
                    raise RecursionRefusal("P4_PENDING_OPERATION_REQUIRES_RECONCILIATION")
                owner = open_owner(state / "actual-p2")
                try:
                    check_source(owner)
                    boundary = ledger["turns"][-1] if ledger["turns"] else ledger["antecedent"]
                    expected = boundary.get("after", boundary.get("identity"))
                    current = owner.snapshot().document()
                    if current != expected:
                        witness = boundary.get("foreground_witness")
                        if witness is None or foreground_witness(owner, current) != witness:
                            raise RecursionRefusal("P4_COLD_STATE_MISMATCH")
                    if args.command == "view":
                        result = surface(owner, ledger)
                        history = HistoricalWorld(owner.base_owner.fanin.session)
                        candidate_ready = history.ready_candidate_id() is not None
                        recover_history = candidate_ready or bool(history.pending())
                    else:
                        result = act(owner, ledger_file, ledger, args)
                finally:
                    owner.close()
    except (RecursionRefusal, HistoryRefusal, FileNotFoundError) as exc:
        print(json.dumps({"grade": GRADE, "status": "REFUSED",
                          "reason": str(exc) if isinstance(exc, (RecursionRefusal, HistoryRefusal)) else
                          "P4_STATE_OR_SOURCE_MISSING"}))
        return 2
    if recover_history or args.command in {"new", "inspect-particular"}:
        wake_history_worker(state, candidate_ready=candidate_ready)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
