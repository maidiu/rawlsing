"""Independent G5 receiving tests for SOROK #1030 C03/C04 custody.

These tests are not authored by the #1030 implementer and do not patch product
source. They use the real J1/P6/D03/C12 stores and only substitute returned
records in memory to attack the embedded admission receipt, event seal,
perception history, selectors, privacy and cold replay.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

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

G5_DIR = Path(__file__).resolve().parent
FRESH_CHILD = G5_DIR / "g5_fresh_cold_child.py"
RENT_KIND = "P2_HOUSEHOLD_RENT"
SECOND_TEXT = "G5 second legitimate public sentence."


def _episode_override(store, event_id, mutate):
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


def _receipt_override(store, event_id, field, value):
    def forge(row):
        body = dict(row["body"])
        body["receipt"] = {**body["receipt"], field: value}
        row["body"] = body
        return row
    return _episode_override(store, event_id, forge)


def _perception_override(store, target_actor_id, mutate):
    real = store.perceptions

    def perceptions(branch_id, actor_id=None):
        rows = real(branch_id, actor_id)
        if actor_id == target_actor_id:
            return mutate(rows)
        return rows

    store.perceptions = perceptions
    return real


def _snapshot(session):
    store = session.product.store
    return {
        "clock": session.clock(),
        "episodes": len(store.episodes(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def _count(session, kind):
    return sum(1 for row in session.product.store.episodes(session.branch_id)
               if row.get("kind") == kind)


def _receipt_value(field, auth):
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
        "decision_action": "DECLINE",
        "public_utterance": False,
        "status": "FORGED_STATUS",
        "schema": "FORGED_SCHEMA",
    }
    value = values[field]
    return value if auth.get(field) != value else value + "_DIFF"


def test_embedded_admission_receipt_refused_and_restored(tmp_path):
    opened = open_j1_case(tmp_path / "receipt")
    try:
        session = opened["session"]
        focal = opened["focal"]
        auth = opened["receipt"]
        eid = auth["event_id"]
        store = session.product.store
        before = _snapshot(session)
        fields = (
            "text", "event_kind", "event_authored_by", "actor_id", "alias",
            "root", "branch", "clock", "decision_id", "operation_id",
            "event_id", "event_hash", "child_actor_id", "child_alias",
            "child_perception_channel", "hidden_reason", "hidden_reason_hash",
            "decision_action", "public_utterance", "status", "schema",
        )
        for field in fields:
            real = _receipt_override(
                store, eid, field, _receipt_value(field, auth))
            with pytest.raises(RecursionRefusal):
                read_child_uptake(session, focal, eid)
            with pytest.raises(RecursionRefusal):
                child_speech_experience(session, event_id=eid)
            store.episodes = real
            assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"
            assert child_speech_experience(
                session, event_id=eid)["status"] == "PERCEIVED"
        assert _snapshot(session) == before
    finally:
        _close(opened)


def test_selector_conjunction_and_failure(tmp_path):
    opened = open_j1_case(tmp_path / "selectors")
    try:
        session = opened["session"]
        focal = opened["focal"]
        eid = opened["receipt"]["event_id"]
        assert read_child_experience(
            session, focal, event_id=eid,
            operation_id="j1-speech")["status"] == "PERCEIVED"
        assert read_child_experience(
            session, focal, event_id=eid)["status"] == "PERCEIVED"
        assert read_child_experience(
            session, focal, operation_id="j1-speech")["status"] == "PERCEIVED"
        for kwargs, code in (
            ({"event_id": eid, "operation_id": "forged"}, "CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND"),
            ({"event_id": "forged", "operation_id": "j1-speech"}, "CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND"),
            ({"event_id": "", "operation_id": None}, "CHILD_EXPERIENCE_SELECTOR_SCHEMA"),
            ({"event_id": None, "operation_id": None}, "CHILD_EXPERIENCE_SCHEMA"),
            ({"event_id": "unknown", "operation_id": None}, "CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND"),
            ({"event_id": None, "operation_id": "unknown"}, "CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND"),
        ):
            with pytest.raises(RecursionRefusal, match=code):
                read_child_experience(session, focal, **kwargs)
    finally:
        _close(opened)


def test_event_seal_and_event_receipt_divergence(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "event")
    try:
        session = opened["session"]
        focal = opened["focal"]
        eid = opened["receipt"]["event_id"]
        store = session.product.store
        real_event = session.event
        raw = real_event(eid)
        for field, value in (
            ("summary", "Mother now agrees to everything."),
            ("location", "market"),
            ("sequence", int(raw["sequence"]) + 1),
            ("observable", False),
            ("clock", int(raw["clock"]) + 1),
        ):
            event = dict(raw)
            if field == "observable":
                event["body"] = {**event["body"], "observable": value}
            else:
                event[field] = value
            session.event = lambda ref, e=event, old=real_event: (
                e if ref == eid else old(ref))
            with pytest.raises(RecursionRefusal):
                read_child_uptake(session, focal, eid)
            with pytest.raises(RecursionRefusal):
                child_speech_experience(session, event_id=eid)
            with pytest.raises(RecursionRefusal):
                read_parent_utterance(
                    session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
            session.event = real_event

        base = dict(raw)
        base.pop("hash", None)
        base.pop("event_id", None)
        base["body"] = {**base["body"], "text": "G5 coherently rehashed text."}
        new_id = "TEST_ONLY_BP4_WORLD_EVT_" + digest(base)
        coherent = {"event_id": new_id, **base}
        coherent["hash"] = digest(coherent)
        session.event = lambda ref, e=coherent, old=real_event: (
            e if ref == eid else old(ref))
        with pytest.raises(RecursionRefusal):
            read_child_uptake(session, focal, eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        session.event = real_event

        real_eps = _episode_override(
            store, eid,
            lambda row: dict(row, body={**row["body"], "event_hash": "1" * 64}))
        with pytest.raises(RecursionRefusal):
            read_child_uptake(session, focal, eid)
        store.episodes = real_eps

        assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"
        assert session.event(eid)["hash"] == opened["receipt"]["event_hash"]
        assert perform_parent_utterance(
            session, PARENT_ID, decision_id="j1-decision", text=TEXT,
            hidden_reason={"reason": HIDDEN}, operation_id="j1-speech",
        )["status"] == "REPLAY"
    finally:
        _close(opened)


def test_false_hearing_severance_and_late_presence(tmp_path):
    remote = open_j1_case(tmp_path / "remote", child_present=False)
    try:
        session = remote["session"]
        focal = remote["focal"]
        auth = remote["receipt"]
        eid = auth["event_id"]
        store = session.product.store
        child_alias = auth["child_alias"]
        assert auth["child_perception_channel"] == "NOT_PERCEIVED"
        assert read_child_uptake(session, focal, eid)["status"] == "NOT_PERCEIVED"
        assert child_speech_experience(
            session, event_id=eid)["status"] == "NOT_PERCEIVED"

        def forge(rows):
            return rows + [{
                "actor_id": child_alias, "event_id": eid,
                "clock": int(auth["clock"]), "channel": "speech"}]

        real = _perception_override(store, child_alias, forge)
        with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_FALSE_PERCEPTION"):
            read_child_uptake(session, focal, eid)
        with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_FALSE_PERCEPTION"):
            child_speech_experience(session, event_id=eid)
        store.perceptions = real
        assert read_child_uptake(session, focal, eid)["status"] == "NOT_PERCEIVED"

        world = session.world()
        world.positions[child_alias] = world.positions[auth["alias"]]
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_child_uptake(session, focal, eid)["status"] == "NOT_PERCEIVED"
    finally:
        _close(remote)

    heard = open_j1_case(tmp_path / "heard")
    try:
        session = heard["session"]
        focal = heard["focal"]
        auth = heard["receipt"]
        eid = auth["event_id"]
        store = session.product.store
        child_alias = auth["child_alias"]
        parent_alias = auth["alias"]

        real = _perception_override(
            store, child_alias,
            lambda rows: [r for r in rows if r.get("event_id") != eid])
        with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_PERCEPTION_SEVERED"):
            read_child_uptake(session, focal, eid)
        store.perceptions = real
        assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"

        real = _perception_override(
            store, child_alias,
            lambda rows: rows + [r for r in rows if r.get("event_id") == eid])
        with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_RECEIPT_DUPLICATE"):
            read_child_uptake(session, focal, eid)
        store.perceptions = real

        real = _perception_override(
            store, parent_alias,
            lambda rows: [r for r in rows
                          if not (r.get("event_id") == eid
                                  and r.get("channel") == "own_speech")])
        with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_PARENT_RECEIPT_SEVERED"):
            read_child_uptake(session, focal, eid)
        store.perceptions = real
        assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"
    finally:
        _close(heard)


def test_private_reason_not_reachable_by_child_consumers(tmp_path):
    opened = open_j1_case(tmp_path / "privacy")
    try:
        session = opened["session"]
        focal = opened["focal"]
        eid = opened["receipt"]["event_id"]
        store = session.product.store
        experience = read_child_experience(session, focal, event_id=eid)
        joined = j1_join.compose_j1(
            opened["case"].owner, session, child_id=focal,
            speech_event_id=eid, utterance_receipt=opened["receipt"],
            plan=opened["plan"])
        child_outputs = json.dumps({
            "uptake": read_child_uptake(session, focal, eid),
            "p6": child_speech_experience(session, event_id=eid),
            "experience": experience,
        })
        d03_output = json.dumps(joined["immediate_uptake"])
        assert HIDDEN not in child_outputs
        assert HIDDEN not in d03_output
        assert "hidden_reason_hash" not in child_outputs
        assert "hidden_reason_hash" not in d03_output
        assert "PURCHASE" not in child_outputs
        assert "PURCHASE" not in d03_output

        marker = "G5_PRIVATE_REASON_MARKER"
        real = _episode_override(
            store, eid,
            lambda row: dict(
                row, body={**row["body"], "hidden_reason": {"reason": marker}}))
        assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"
        mutated = json.dumps({
            "uptake": read_child_uptake(session, focal, eid),
            "p6": child_speech_experience(session, event_id=eid),
            "experience": read_child_experience(session, focal, event_id=eid),
        })
        assert marker not in mutated
        store.episodes = real

        real = _receipt_override(store, eid, "hidden_reason", marker)
        with pytest.raises(RecursionRefusal) as exc:
            read_child_uptake(session, focal, eid)
        assert marker not in str(exc.value)
        store.episodes = real
        assert read_child_uptake(session, focal, eid)["status"] == "PERCEIVED"
    finally:
        _close(opened)


def test_changed_legitimate_speech_qualified_and_restored(tmp_path):
    opened = open_j1_case(tmp_path / "changed")
    try:
        session = opened["session"]
        focal = opened["focal"]
        first = opened["receipt"]
        store = session.product.store
        purchase_before = _count(session, PARENT_PURCHASE_KIND)
        rent_before = _count(session, RENT_KIND)
        speech_before = _count(session, PARENT_UTTERANCE_KIND)
        assert purchase_before == 1
        assert rent_before == 0
        assert speech_before == 1

        second = perform_parent_utterance(
            session, PARENT_ID, decision_id="j1-decision", text=SECOND_TEXT,
            hidden_reason={"reason": "g5-second-private"},
            operation_id="g5-speech-2")
        assert second["status"] == "ADMITTED"
        assert second["event_id"] != first["event_id"]
        assert read_child_uptake(
            session, focal, second["event_id"])["status"] == "PERCEIVED"
        assert child_speech_experience(
            session, event_id=second["event_id"])["status"] == "PERCEIVED"
        assert child_speech_experience(
            session, event_id=second["event_id"])["response_input"][
                "public_text"] == SECOND_TEXT
        assert read_child_uptake(
            session, focal, first["event_id"])["status"] == "PERCEIVED"
        assert _count(session, PARENT_UTTERANCE_KIND) == 2
        assert _count(session, PARENT_PURCHASE_KIND) == 1
        assert _count(session, RENT_KIND) == 0

        real = _receipt_override(
            store, second["event_id"], "text", "G5 mutated second speech.")
        with pytest.raises(RecursionRefusal):
            read_child_uptake(session, focal, second["event_id"])
        assert read_child_uptake(
            session, focal, first["event_id"])["status"] == "PERCEIVED"
        store.episodes = real
        assert child_speech_experience(
            session, event_id=second["event_id"])["status"] == "PERCEIVED"
        assert child_speech_experience(
            session, event_id=second["event_id"])["response_input"][
                "public_text"] == SECOND_TEXT

        with pytest.raises(
                RecursionRefusal, match="PARENT_UTTERANCE_REUSE_MISMATCH"):
            perform_parent_utterance(
                session, PARENT_ID, decision_id="j1-decision",
                text="G5 changed text under the same operation",
                hidden_reason={"reason": HIDDEN}, operation_id="j1-speech")
        assert session.event(first["event_id"])["hash"] == first["event_hash"]
        assert read_child_uptake(
            session, focal, first["event_id"])["status"] == "PERCEIVED"
        assert _count(session, PARENT_PURCHASE_KIND) == 1
        assert _count(session, RENT_KIND) == 0
    finally:
        _close(opened)


def test_c03_material_prospectives_are_candidates_only(tmp_path):
    cases = {
        "baseline": open_j1_case(tmp_path / "baseline"),
        "debt": open_j1_case(
            tmp_path / "debt", parent_overrides={"debt_units": 61}),
        "care": open_j1_case(
            tmp_path / "care", parent_overrides={"care_hours_due": 8}),
    }
    try:
        results = {}
        for label, opened in cases.items():
            session = opened["session"]
            before = _snapshot(session)
            result = read_parent_material_prospectives(
                session, PARENT_ID, as_actor=PARENT_ID)
            results[label] = result
            assert result["status"] == "CANDIDATES_ONLY_ACTOR_SELECTION_UNISSUED"
            assert result["option_count"] == 5
            assert result["chosen_candidate"] is None
            assert result["performed_event"] is None
            assert all(not row["chosen"] and not row["performed"]
                       for row in result["options"])
            assert HIDDEN not in json.dumps(result)
            assert "CALLER_SUPPLIED_OBJECTIVE_REQUEST" not in json.dumps(result)
            assert _snapshot(session) == before
        base = {row["candidate"]: row for row in results["baseline"]["options"]}
        debt = {row["candidate"]: row for row in results["debt"]["options"]}
        care = {row["candidate"]: row for row in results["care"]["options"]}
        assert base["POSSIBLE_JUNIOR_PURCHASE"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert debt["POSSIBLE_JUNIOR_PURCHASE"]["status"] == "MATERIALLY_INELIGIBLE"
        assert care["POSSIBLE_JUNIOR_PURCHASE"]["status"] == "MATERIALLY_INELIGIBLE"
        assert debt["QUIET_NONPURCHASE"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert care["QUIET_NONPURCHASE"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert results["baseline"]["source"] != results["debt"]["source"]
        assert results["baseline"]["source"] != results["care"]["source"]

        receipt = cases["baseline"]["receipt"]
        assert receipt["text_source"] == "CALLER_SUPPLIED_NOT_GENERATED"
        assert receipt["language_generation_owner"] == "NOT_IMPLEMENTED"
        assert receipt["hidden_reason"] == "NOT_READ"
    finally:
        for opened in cases.values():
            _close(opened)


def test_fresh_process_cold_replay_exact(tmp_path):
    opened = open_j1_case(tmp_path / "cold")
    payload_path = tmp_path / "cold_case.json"
    try:
        case = opened["case"]
        payload = {
            "case": {
                "source": case.source,
                "history": case.history,
                "plans": case.plans,
                "catalog": case.catalog,
                "compression_specs": case.compression_specs,
                "standpoints": case.standpoints,
                "state_root": str(case.state_root),
            },
            "focal": opened["focal"],
            "speech_event_id": opened["receipt"]["event_id"],
            "utterance_receipt": opened["receipt"],
            "plan": opened["plan"],
            "event_hash": opened["receipt"]["event_hash"],
            "text": TEXT,
            "hidden": HIDDEN,
        }
        payload_path.write_text(json.dumps(payload))
        assert _count(opened["session"], PARENT_UTTERANCE_KIND) == 1
        assert _count(opened["session"], PARENT_PURCHASE_KIND) == 1
        assert _count(opened["session"], RENT_KIND) == 0
    finally:
        _close(opened)

    env = dict(os.environ)
    env["TMPDIR"] = str(ROOT / ".local-logs" / "sorok1038-custody-g5" / "tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    outputs = []
    for _ in range(2):
        completed = subprocess.run(
            [sys.executable, "-B", str(FRESH_CHILD), str(payload_path)],
            capture_output=True, text=True, env=env, timeout=600,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    for result in outputs:
        assert result["process"] == "FRESH_INTERPRETER"
        assert result["event_hash_exact"] is True
        assert result["event_text_exact"] is True
        assert result["uptake_status"] == "PERCEIVED"
        assert result["p6_status"] == "PERCEIVED"
        assert result["joined_status"] == j1_join.UPSTREAM_PROVEN
        assert result["d03_status"] == "COMPUTED_TEST_ONLY_IMMEDIATE"
        assert result["d03_modes"]
        assert result["subsequent_performed"] is False
        assert result["durable_formation"] == "MISSING_RULE"
        assert result["language_generation_owner"] == "NOT_IMPLEMENTED"
        assert result["text_source"] == "CALLER_SUPPLIED_NOT_GENERATED"
        assert result["speech_episode_count"] == 1
        assert result["purchase_episode_count"] == 1
        assert result["rent_episode_count"] == 0
        assert result["history_purchase_count"] == 1
        assert result["hidden_absent_from_child"] is True
        assert result["hidden_hash_absent_from_child"] is True
        assert result["parent_read_status"] == "READ"
        assert result["parent_hidden_exact"] is True
        assert result["snapshot_unchanged"] is True
        assert result["p3_head_unchanged"] is True
    assert outputs[0] == outputs[1]
