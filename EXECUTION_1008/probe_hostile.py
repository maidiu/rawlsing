"""Exploratory hostile probe for C04 first-consumer custody (not a pytest)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J1 = ROOT / "WORKER_RETURNS" / "SOROK-E01-J1-995-R1"
if str(J1) not in sys.path:
    sys.path.insert(0, str(J1))

from test_j1_three_head_join import (  # noqa: E402
    PARENT_ID, TEXT, open_j1_case, _close,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
import developmental_recursion.parent_speech as ps  # noqa: E402
from run_p6 import child_speech_experience  # noqa: E402
import j1_join  # noqa: E402

RESULTS = []


def attempt(label, fn):
    try:
        value = fn()
        RESULTS.append((label, "ACCEPTED", value))
    except RecursionRefusal as exc:
        RESULTS.append((label, "REFUSED", str(exc)))
    except Exception as exc:  # noqa: BLE001
        RESULTS.append((label, "ERROR", type(exc).__name__ + ":" + str(exc)))


def main(tmp: Path) -> None:
    opened = open_j1_case(tmp / "base")
    try:
        session = opened["session"]
        focal = opened["focal"]
        eid = opened["receipt"]["event_id"]
        store = session.product.store
        real_eps = store.episodes
        real_per = store.perceptions
        real_event = session.event

        # 1. forged event clock only, stale hash/ID
        def forged_clock(ref):
            row = real_event(ref)
            if ref != eid or row is None:
                return row
            row = dict(row)
            row["clock"] = row["clock"] + 1
            return row
        session.event = forged_clock
        attempt("event_clock_forged/uptake",
                lambda: ps.read_child_uptake(session, focal, eid))
        attempt("event_clock_forged/p6",
                lambda: child_speech_experience(session, event_id=eid))
        session.event = real_event

        # 2. episode body tampering one field at a time
        def tamper_body(field, value):
            def episodes(branch_id):
                rows = real_eps(branch_id)
                out = []
                for row in rows:
                    if (row.get("kind") == ps.PARENT_UTTERANCE_KIND
                            and (row.get("body") or {}).get("event_id") == eid):
                        row = dict(row)
                        if field == "clock":
                            row["clock"] = value
                        else:
                            row["body"] = {**row["body"], field: value}
                    out.append(row)
                return out
            return episodes

        for field, value in (
            ("root", "0" * 64),
            ("branch", "FORGED_BRANCH"),
            ("actor_id", "FORGED_PARENT"),
            ("alias", "X"),
            ("child_actor_id", "FORGED_CHILD"),
            ("child_alias", "Z"),
            ("text", "Forged speech text."),
            ("decision_id", "forged-decision"),
            ("operation_id", "forged-operation"),
            ("event_hash", "1" * 64),
        ):
            store.episodes = tamper_body(field, value)
            attempt("episode_%s/uptake" % field,
                    lambda: ps.read_child_uptake(session, focal, eid))
            attempt("episode_%s/p6" % field,
                    lambda: child_speech_experience(session, event_id=eid))
            store.episodes = real_eps

        store.episodes = tamper_body("clock", 999999)
        attempt("episode_clock/uptake",
                lambda: ps.read_child_uptake(session, focal, eid))
        store.episodes = real_eps

        # 3. duplicate parent own_speech receipt
        alias = opened["receipt"]["alias"]
        def dup_parent(branch_id, actor_id):
            rows = real_per(branch_id, actor_id)
            if actor_id == alias:
                return rows + rows[-1:]
            return rows
        store.perceptions = dup_parent
        attempt("duplicate_parent_receipt/uptake",
                lambda: ps.read_child_uptake(session, focal, eid))
        attempt("duplicate_parent_receipt/p6",
                lambda: child_speech_experience(session, event_id=eid))
        store.perceptions = real_per

        # 4. duplicate utterance episode (same event id)
        def dup_episode(branch_id):
            rows = real_eps(branch_id)
            hit = [r for r in rows if (r.get("body") or {}).get("event_id") == eid]
            return rows + hit
        store.episodes = dup_episode
        attempt("duplicate_utterance_episode/uptake",
                lambda: ps.read_child_uptake(session, focal, eid))
        attempt("duplicate_utterance_episode/p6",
                lambda: child_speech_experience(session, event_id=eid))
        attempt("duplicate_utterance_episode/select",
                lambda: ps.read_child_experience(session, focal, operation_id="j1-speech"))
        store.episodes = real_eps

        # 5. embedded admission receipt text/decision_action tamper
        def tamper_receipt(field, value):
            def episodes(branch_id):
                rows = real_eps(branch_id)
                out = []
                for row in rows:
                    if (row.get("kind") == ps.PARENT_UTTERANCE_KIND
                            and (row.get("body") or {}).get("event_id") == eid):
                        row = dict(row)
                        body = dict(row["body"])
                        body["receipt"] = {**body["receipt"], field: value}
                        row["body"] = body
                    out.append(row)
                return out
            return episodes
        for field, value in (
            ("text", "I agree to everything."),
            ("event_kind", "MOVE"),
            ("event_authored_by", "FORGED"),
            ("decision_action", "PURCHASE"),
            ("hidden_reason_hash", "2" * 64),
            ("status", "REPLAY"),
            ("event_id", "OTHER"),
        ):
            store.episodes = tamper_receipt(field, value)
            attempt("receipt_%s/uptake" % field,
                    lambda: ps.read_child_uptake(session, focal, eid))
            store.episodes = real_eps

        # 6. D03 with forged receipt against real uptake
        base_owner = opened["case"].owner.base_owner
        p3_owner = opened["case"].owner
        real_receipt = opened["receipt"]
        for field, value in (
            ("root", "0" * 64),
            ("branch", "FORGED"),
            ("clock", int(real_receipt["clock"]) + 100),
            ("operation_id", "forged-operation"),
            ("decision_id", "forged-decision"),
            ("event_hash", "3" * 64),
            ("actor_id", "FORGED_PARENT"),
            ("alias", "X"),
            ("text", "I agree to everything."),
        ):
            forged = {**real_receipt, field: value}
            attempt("d03_receipt_%s" % field,
                    lambda forged=forged: j1_join.compose_j1(
                        p3_owner, session, child_id=focal,
                        speech_event_id=eid, utterance_receipt=forged,
                        plan=opened["plan"]))
    finally:
        _close(opened)


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        main(Path(tmp))
    for label, status, detail in RESULTS:
        if status == "REFUSED":
            print("%-48s %-9s %s" % (label, status, detail[:110]))
        else:
            print("%-48s %-9s %s" % (label, status, json.dumps(detail)[:110]))
