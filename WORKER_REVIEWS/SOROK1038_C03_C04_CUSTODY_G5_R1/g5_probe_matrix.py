"""Independent G5 hostile probe matrix for SOROK #1030 C03/C04 custody.

Reads real J1/P6/D03/C12 source; mutates only returned records in memory.
No product file is written and no browser/provider/network is used.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
J1 = ROOT / "WORKER_RETURNS" / "SOROK-E01-J1-995-R1"
P3_TESTS = ROOT / "WORKER_RETURNS" / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1" / "tests"
for path in (J1, P3_TESTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from test_j1_three_head_join import (  # noqa: E402
    HIDDEN, PARENT_ID, TEXT, _close, open_j1_case,
)
from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    PARENT_PURCHASE_KIND, read_parent_history,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    read_parent_material_prospectives,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    PARENT_UTTERANCE_KIND, perform_parent_utterance, read_child_experience,
    read_child_uptake, read_parent_utterance,
)
from run_p6 import child_speech_experience  # noqa: E402
import j1_join  # noqa: E402

RESULTS: list[dict] = []


def record(section, label, consumer, status, detail):
    RESULTS.append({
        "section": section,
        "label": label,
        "consumer": consumer,
        "outcome": status,
        "detail": detail,
    })


def call(section, label, consumer, fn):
    try:
        value = fn()
        detail = value.get("status") if isinstance(value, dict) else value
        record(section, label, consumer, "ACCEPTED", detail)
        return value
    except RecursionRefusal as exc:
        record(section, label, consumer, "REFUSED", str(exc))
    except Exception as exc:  # noqa: BLE001
        record(section, label, consumer, "ERROR",
               type(exc).__name__ + ":" + str(exc))


def episode_tamper(store, event_id, mutate):
    real = store.episodes

    def episodes(branch_id):
        rows = real(branch_id)
        out = []
        for row in rows:
            if (row.get("kind") == PARENT_UTTERANCE_KIND
                    and (row.get("body") or {}).get("event_id") == event_id):
                row = mutate(dict(row))
            out.append(row)
        return out

    store.episodes = episodes
    return real


def receipt_tamper(store, event_id, field, value):
    def forge(row):
        body = dict(row["body"])
        body["receipt"] = {**body["receipt"], field: value}
        row["body"] = body
        return row
    return episode_tamper(store, event_id, forge)


def perception_tamper(store, target_actor_id, mutate):
    real = store.perceptions

    def perceptions(branch_id, actor_id=None):
        rows = real(branch_id, actor_id)
        if actor_id == target_actor_id:
            return mutate(rows)
        return rows

    store.perceptions = perceptions
    return real


def forged(field, auth):
    values = {
        "text": "G5 forged public text.",
        "event_kind": "MOVE",
        "event_authored_by": "IMPERSONATED_PARENT",
        "actor_id": "FORGED_PARENT",
        "alias": "Z",
        "root": "0" * 64,
        "branch": "FORGED_BRANCH",
        "clock": int(auth["clock"]) + 1000,
        "decision_id": "forged-decision",
        "operation_id": "forged-operation",
        "event_id": "FORGED_EVENT",
        "event_hash": "1" * 64,
        "child_actor_id": "FORGED_CHILD",
        "child_alias": "Y",
        "child_perception_channel": "NOT_PERCEIVED",
        "hidden_reason": "G5_PRIVATE_REASON_MARKER",
        "hidden_reason_hash": "2" * 64,
        "decision_action": "DECLINE" if auth["decision_action"] != "DECLINE" else "PURCHASE",
        "public_utterance": False,
        "status": "FORGED_STATUS",
        "schema": "FORGED_SCHEMA",
        "grade": "FORGED_GRADE",
        "text_source": "GENERATED_BY_MOTHER",
        "language_generation_owner": "IMPLEMENTED",
        "private_state": "PUBLIC",
        "period_context": {"forged": True},
        "hidden_reason_source": "GENERATED_BY_MOTHER",
        "custody": "MEMORY",
        "durable_acquisition": "ACQUIRED",
        "native_science": True,
    }
    value = values[field]
    if auth.get(field) == value:
        if isinstance(value, str):
            value = value + "_DIFF"
        elif isinstance(value, int):
            value = value + 1
        elif isinstance(value, bool):
            value = not value
        elif isinstance(value, dict):
            value = {"forged": "DIFF"}
    return value


def sections(base_dir: Path) -> None:
    opened = open_j1_case(base_dir / "base")
    try:
        session = opened["session"]
        focal = opened["focal"]
        auth = opened["receipt"]
        eid = auth["event_id"]
        store = session.product.store
        child_alias = auth["child_alias"]
        parent_alias = auth["alias"]
        plan = opened["plan"]
        owner = opened["case"].owner

        def snapshot():
            return {
                "clock": session.clock(),
                "episodes": len(store.episodes(session.branch_id)),
                "world_events": len(store.world_events(session.branch_id)),
                "perceptions": len(store.perceptions(session.branch_id)),
            }

        head_before = snapshot()
        episodes_before = head_before["episodes"]

        def uptake():
            return read_child_uptake(session, focal, eid)

        def p6():
            return child_speech_experience(session, event_id=eid)

        def parent_read():
            return read_parent_utterance(
                session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)

        def d03(receipt=None):
            return j1_join.compose_j1(
                owner, session, child_id=focal, speech_event_id=eid,
                utterance_receipt=receipt or auth, plan=plan)

        for field, value in (
            ("text", forged("text", auth)),
            ("event_kind", forged("event_kind", auth)),
            ("event_authored_by", forged("event_authored_by", auth)),
            ("actor_id", forged("actor_id", auth)),
            ("alias", forged("alias", auth)),
            ("root", forged("root", auth)),
            ("branch", forged("branch", auth)),
            ("clock", forged("clock", auth)),
            ("decision_id", forged("decision_id", auth)),
            ("operation_id", forged("operation_id", auth)),
            ("event_id", forged("event_id", auth)),
            ("event_hash", forged("event_hash", auth)),
            ("child_actor_id", forged("child_actor_id", auth)),
            ("child_alias", forged("child_alias", auth)),
            ("child_perception_channel", forged("child_perception_channel", auth)),
            ("hidden_reason", forged("hidden_reason", auth)),
            ("hidden_reason_hash", forged("hidden_reason_hash", auth)),
            ("decision_action", forged("decision_action", auth)),
            ("public_utterance", forged("public_utterance", auth)),
            ("status", forged("status", auth)),
            ("schema", forged("schema", auth)),
            ("grade", forged("grade", auth)),
            ("text_source", forged("text_source", auth)),
            ("language_generation_owner", forged("language_generation_owner", auth)),
            ("private_state", forged("private_state", auth)),
            ("period_context", forged("period_context", auth)),
            ("hidden_reason_source", forged("hidden_reason_source", auth)),
            ("custody", forged("custody", auth)),
            ("durable_acquisition", forged("durable_acquisition", auth)),
            ("native_science", forged("native_science", auth)),
        ):
            real = receipt_tamper(store, eid, field, value)
            call("receipt", field, "uptake", uptake)
            call("receipt", field, "p6", p6)
            call("receipt", field, "parent_self_read", parent_read)
            store.episodes = real

        assert uptake()["status"] == "PERCEIVED"
        assert p6()["status"] == "PERCEIVED"

        for field, value in (
            ("root", "0" * 64),
            ("branch", "FORGED_BRANCH"),
            ("actor_id", "FORGED_PARENT"),
            ("alias", "Z"),
            ("text", "G5 forged episode text."),
            ("decision_id", "forged-decision"),
            ("operation_id", "forged-operation"),
            ("event_hash", "1" * 64),
            ("child_actor_id", "FORGED_CHILD"),
            ("child_alias", "Y"),
        ):
            def forge(row, field=field, value=value):
                row["body"] = {**row["body"], field: value}
                return row
            real = episode_tamper(store, eid, forge)
            call("episode", field, "uptake", uptake)
            call("episode", field, "p6", p6)
            call("episode", field, "parent_self_read", parent_read)
            store.episodes = real

        def clock_forge(row):
            row["clock"] = 999999
            return row
        real = episode_tamper(store, eid, clock_forge)
        call("episode", "clock", "uptake", uptake)
        call("episode", "clock", "p6", p6)
        store.episodes = real

        real_event = session.event
        raw_event = real_event(eid)

        def event_forge(field, value):
            event = dict(raw_event)
            if field == "body_text":
                event["body"] = {**event["body"], "text": value}
            elif field == "observable":
                event["body"] = {**event["body"], "observable": value}
            else:
                event[field] = value
            return event

        for field, value in (
            ("summary", "Mother now agrees to everything."),
            ("location", "market"),
            ("sequence", int(raw_event["sequence"]) + 1),
            ("clock", int(raw_event["clock"]) + 1),
            ("body_text", "G5 forged event body text."),
            ("observable", False),
        ):
            forged_event = event_forge(field, value)
            session.event = lambda ref, e=forged_event, old=real_event: (
                e if ref == eid else old(ref))
            call("event", field, "uptake", uptake)
            call("event", field, "p6", p6)
            call("event", field, "parent_self_read", parent_read)
            session.event = real_event

        base = dict(raw_event)
        base.pop("hash", None)
        base.pop("event_id", None)
        base["body"] = {**base["body"], "text": "G5 coherently rehashed text."}
        new_id = "TEST_ONLY_BP4_WORLD_EVT_" + digest(base)
        coherent = {"event_id": new_id, **base}
        coherent["hash"] = digest(coherent)
        session.event = lambda ref, e=coherent, old=real_event: (
            e if ref == eid else old(ref))
        call("event", "coherent_rehash_both", "uptake", uptake)
        call("event", "coherent_rehash_both", "p6", p6)
        session.event = real_event

        stale_id = dict(coherent)
        stale_id["event_id"] = raw_event["event_id"]
        stale_id["hash"] = coherent["hash"]
        session.event = lambda ref, e=stale_id, old=real_event: (
            e if ref == eid else old(ref))
        call("event", "coherent_hash_stale_id", "uptake", uptake)
        session.event = real_event

        def missing_child(rows):
            return [r for r in rows if r.get("event_id") != eid]

        def dup_child(rows):
            hit = [r for r in rows if r.get("event_id") == eid]
            return rows + hit

        def wrong_channel(rows):
            return [({**r, "channel": "sight"} if r.get("event_id") == eid else r)
                    for r in rows]

        for label, mutate in (
            ("severed_child_perception", missing_child),
            ("duplicate_child_perception", dup_child),
            ("wrong_child_channel", wrong_channel),
        ):
            real = perception_tamper(store, child_alias, mutate)
            call("perception", label, "uptake", uptake)
            call("perception", label, "p6", p6)
            store.perceptions = real

        def sever_parent(rows):
            return [r for r in rows
                    if not (r.get("event_id") == eid
                            and r.get("channel") == "own_speech")]

        real = perception_tamper(store, parent_alias, sever_parent)
        call("perception", "severed_parent_own_speech", "uptake", uptake)
        store.perceptions = real
        assert uptake()["status"] == "PERCEIVED"

        for label, event_id, operation_id in (
            ("both_valid", eid, "j1-speech"),
            ("event_only", eid, None),
            ("operation_only", None, "j1-speech"),
            ("event_valid_operation_forged", eid, "forged-operation"),
            ("event_forged_operation_valid", "forged-event", "j1-speech"),
            ("empty_event", "", None),
            ("none_both", None, None),
            ("unknown_event", "unknown-event", None),
            ("unknown_operation", None, "unknown-operation"),
        ):
            call("selector", label, "experience",
                 lambda ev=event_id, op=operation_id: read_child_experience(
                     session, focal, event_id=ev, operation_id=op))

        for field, value in (
            ("root", "0" * 64),
            ("branch", "FORGED_BRANCH"),
            ("clock", int(auth["clock"]) + 100),
            ("operation_id", "forged-operation"),
            ("decision_id", "forged-decision"),
            ("event_hash", "3" * 64),
            ("actor_id", "FORGED_PARENT"),
            ("alias", "Z"),
            ("text", "G5 forged caller receipt text."),
            ("status", "FORGED_STATUS"),
        ):
            altered = {**auth, field: value}
            call("d03_caller_receipt", field, "d03",
                 lambda r=altered: d03(r))

        marker = "G5_PRIVATE_REASON_MARKER"
        for label, value in (
            ("baseline_child_outputs", json.dumps({
                "uptake": uptake(),
                "p6": p6(),
                "d03": d03(),
                "experience": read_child_experience(session, focal, event_id=eid),
            })),
        ):
            record("privacy", label, "contains_hidden",
                   "HIDDEN" if HIDDEN in value else "ABSENT", HIDDEN)
            record("privacy", label, "contains_hidden_hash",
                   "HIDDEN" if "hidden_reason_hash" in value else "ABSENT",
                   "hidden_reason_hash")

        def outer_hidden(row):
            row["body"] = {**row["body"], "hidden_reason": {"reason": marker}}
            return row
        real = episode_tamper(store, eid, outer_hidden)
        call("privacy", "outer_hidden_reason_mutated", "uptake", uptake)
        leaked = json.dumps({
            "uptake": uptake(),
            "p6": p6(),
            "d03": d03(),
            "experience": read_child_experience(session, focal, event_id=eid),
        })
        record("privacy", "outer_hidden_reason_mutated", "marker_exposed",
               "LEAK" if marker in leaked else "ABSENT", marker)
        store.episodes = real

        real = receipt_tamper(store, eid, "hidden_reason", marker)
        call("privacy", "receipt_hidden_reason_mutated", "uptake", uptake)
        store.episodes = real

        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        episodes_after = len(store.episodes(session.branch_id))
        record("conservation", "read_only_episode_count", "exact",
               "UNCHANGED" if episodes_after == episodes_before else "CHANGED",
               {"before": episodes_before, "after": episodes_after})
        record("conservation", "read_only_snapshot", "exact",
               "UNCHANGED" if snapshot() == head_before else "CHANGED",
               {"before": head_before, "after": snapshot()})
        record("conservation", "purchase_count", "exact",
               history["purchase_episode_count"],
               {"kind": PARENT_PURCHASE_KIND})
    finally:
        _close(opened)

    remote = open_j1_case(base_dir / "remote", child_present=False)
    try:
        session = remote["session"]
        focal = remote["focal"]
        auth = remote["receipt"]
        eid = auth["event_id"]
        store = session.product.store
        child_alias = auth["child_alias"]
        assert auth["child_perception_channel"] == "NOT_PERCEIVED"
        call("false_hearing", "authentic_unheard", "uptake",
             lambda: read_child_uptake(session, focal, eid))
        call("false_hearing", "authentic_unheard", "p6",
             lambda: child_speech_experience(session, event_id=eid))

        def forge_perception(rows):
            return rows + [{
                "actor_id": child_alias, "event_id": eid,
                "clock": int(auth["clock"]), "channel": "speech",
            }]
        real = perception_tamper(store, child_alias, forge_perception)
        call("false_hearing", "forged_child_perception", "uptake",
             lambda: read_child_uptake(session, focal, eid))
        call("false_hearing", "forged_child_perception", "p6",
             lambda: child_speech_experience(session, event_id=eid))
        store.perceptions = real
        call("false_hearing", "restored_unheard", "uptake",
             lambda: read_child_uptake(session, focal, eid))

        world = session.world()
        world.positions[child_alias] = world.positions[auth["alias"]]
        session.product._checkpoint(session.branch_id, world.clock, world)
        call("false_hearing", "later_co_presence", "uptake",
             lambda: read_child_uptake(session, focal, eid))
    finally:
        _close(remote)

    for label, overrides in (
        ("baseline", {}),
        ("debt", {"debt_units": 61}),
        ("care", {"care_hours_due": 8}),
    ):
        opened = open_j1_case(base_dir / ("prospective-" + label),
                              parent_overrides=overrides)
        try:
            session = opened["session"]
            before_events = len(session.world().events)
            before_episodes = len(session.product.store.episodes(session.branch_id))
            result = read_parent_material_prospectives(
                session, PARENT_ID, as_actor=PARENT_ID)
            options = {row["candidate"]: row for row in result["options"]}
            record("c03", label, "status", result["status"],
                   {"option_count": result["option_count"],
                    "chosen": result["chosen_candidate"],
                    "performed": result["performed_event"],
                    "purchase": options["POSSIBLE_JUNIOR_PURCHASE"]["status"],
                    "quiet": options["QUIET_NONPURCHASE"]["status"]})
            record("c03", label, "no_events_or_episodes", "READ_ONLY",
                   {"events": [before_events, len(session.world().events)],
                    "episodes": [before_episodes,
                                 len(session.product.store.episodes(
                                     session.branch_id))]})
            record("c03", label, "private_absent", "ABSENT"
                   if HIDDEN not in json.dumps(result) else "LEAK", HIDDEN)
        finally:
            _close(opened)

    opened = open_j1_case(base_dir / "nonclaim")
    try:
        receipt = opened["receipt"]
        record("nonclaim", "utterance_receipt", "text_source", "EXACT",
               receipt["text_source"])
        record("nonclaim", "utterance_receipt", "language_generation_owner",
               "EXACT", receipt["language_generation_owner"])
        record("nonclaim", "utterance_receipt", "hidden_reason", "EXACT",
               receipt["hidden_reason"])
    finally:
        _close(opened)


def main() -> None:
    with tempfile.TemporaryDirectory(dir=str(ROOT / ".local-logs"
                                             / "sorok1038-custody-g5" / "tmp")) as tmp:
        sections(Path(tmp))
    for row in RESULTS:
        print(json.dumps(row, sort_keys=True))


if __name__ == "__main__":
    main()
