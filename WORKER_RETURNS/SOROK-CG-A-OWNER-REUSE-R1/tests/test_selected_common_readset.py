"""Cold, later, actor-local read of the selected common P3 sidecar write."""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = ROOT / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3_ROOT = ROOT / "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (str(ENGINE_ROOT), str(P3_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402

BINDING = {"root": "root:nadia", "actor": "actor:nadia", "branch": "branch:home"}
REGISTRY_HASH = "registry:cga:test-only"
SOURCE_HASH = "source:cga:home-period"
GRADE = "SOURCEFREE_TEST_ONLY"
RULE = {"rule_id": "rule.cga.home", "rule_version": "1", "rule_hash": "rule:cga:home:1"}
PROJECT = "home:period:1"
MOTHER = "actor:mother"


def plan() -> dict:
    return {
        **BINDING,
        "source_hash": SOURCE_HASH,
        "authority": "TEST_ONLY",
        "grade": GRADE,
        "permitted_rules": [dict(RULE)],
    }


def state(clock: int, tag: str) -> dict:
    return {
        **BINDING,
        "clock": clock,
        "state_hash": digest({"tag": tag, "clock": clock}),
    }


def event_binding(clock: int) -> dict:
    event_hash = "event:cga:home:1"
    return {
        **BINDING,
        "event_id": "event:cga:home:1",
        "event_hash": event_hash,
        "clock": clock,
    }


def base_result(clock: int, before: dict) -> dict:
    return {
        **BINDING,
        "event_id": "event:cga:home:1",
        "event_hash": "event:cga:home:1",
        "clock": clock,
        "before": before,
        "after": state(clock, "base-after"),
        "objective": {"event": {"e1_event_id": "event:cga:home:1",
                                "e1_event_hash": "event:cga:home:1"}},
        "receipt_ref": "P2_EVENT:event:cga:home:1",
    }


def record(clock: int) -> dict:
    body = {
        **BINDING,
        "project": PROJECT,
        "counterpart": MOTHER,
        "record_id": "record:cga:home:1",
        "kind": "MEDIATOR",
        "payload": {"room": "kitchen", "qualified_speech": "mother-invitation"},
        "rule_id": RULE["rule_id"],
        "rule_version": RULE["rule_version"],
        "rule_hash": RULE["rule_hash"],
        "registry_hash": REGISTRY_HASH,
        "source_hash": SOURCE_HASH,
        "effective_from": clock,
        "causal_parents": ["event:cga:home:1"],
        "grade": GRADE,
    }
    return body


def open_store(path: Path, *, binding=None, source_hash=SOURCE_HASH) -> PsycheStore:
    return PsycheStore(path, binding=binding or BINDING,
                       registry_hash=REGISTRY_HASH, source_hash=source_hash)


def write_home_record(path: Path) -> str:
    store = open_store(path)
    clock = 10
    expected = state(clock - 1, "expected")
    before = state(clock - 1, "base-before")
    store.reserve(
        "op:cga:home:1",
        proposal_hash="proposal:cga:home:1",
        expected=expected,
        plan_hash=digest(plan()),
        base_before=before,
        psyche_before=store.head(),
        plan=plan(),
    )
    store.save_world("op:cga:home:1", base_result(clock, before))
    receipt = store.commit_effects(
        "op:cga:home:1",
        records=[record(clock)],
        response={"status": "COMPUTED_TEST_ONLY_HOME_READ"},
        event_binding=event_binding(clock),
    )
    stored = store.query(project=PROJECT, counterpart=MOTHER, as_of=clock)
    assert len(stored) == 1
    record_hash = stored[0]["hash"]
    store.finish("op:cga:home:1", {
        "operation_id": "op:cga:home:1",
        "proposal_hash": "proposal:cga:home:1",
        "before": expected,
        "after": state(clock, "combined"),
        "status": "REALIZED",
        "objective": {"event": {"event_id": "event:cga:home:1"}},
        "accessible": {"event_id": "event:cga:home:1"},
        "consequences": {"effects_receipt_hash": receipt["receipt_hash"]},
        "readset": ["event:cga:home:1"],
        "receipt_ref": "P3_PSYCH:" + str(receipt.get("response_hash", "cga")),
    })
    store.close()
    return record_hash


def later_decision(store: PsycheStore, *, as_of: int) -> dict:
    rows = store.query(project=PROJECT, counterpart=MOTHER, as_of=as_of)
    if not rows:
        return {"action": "HOLD_NO_QUALIFIED_HOME", "basis": None}
    return {"action": "ENTER_KITCHEN", "basis": rows[0]["hash"]}


def test_cold_reopen_later_actor_local_read_consumes_exact_record(tmp_path):
    path = tmp_path / "psyche.sqlite3"
    record_hash = write_home_record(path)
    reopened = open_store(path)
    try:
        assert reopened.verify() is True
        assert later_decision(reopened, as_of=12) == {
            "action": "ENTER_KITCHEN", "basis": record_hash}
        assert later_decision(reopened, as_of=9) == {
            "action": "HOLD_NO_QUALIFIED_HOME", "basis": None}
        other_actor = open_store(
            tmp_path / "mother.sqlite3",
            binding={"root": "root:nadia", "actor": MOTHER, "branch": "branch:home"},
        )
        try:
            assert later_decision(other_actor, as_of=12) == {
                "action": "HOLD_NO_QUALIFIED_HOME", "basis": None}
        finally:
            other_actor.close()
        assert reopened.head()["count"] == 1
    finally:
        reopened.close()


def test_missing_source_or_wrong_root_refuses_before_read(tmp_path):
    path = tmp_path / "psyche.sqlite3"
    write_home_record(path)
    with pytest.raises(RecursionRefusal, match="SOURCE"):
        open_store(path, source_hash="source:cga:removed")
    with pytest.raises(RecursionRefusal, match="BINDING"):
        open_store(path, binding={"root": "root:other", "actor": "actor:nadia",
                                  "branch": "branch:home"})


def test_same_input_replay_and_conflicting_reuse_are_distinct(tmp_path):
    path = tmp_path / "psyche.sqlite3"
    record_hash = write_home_record(path)
    store = open_store(path)
    try:
        op = store.get_operation("op:cga:home:1")
        assert op["phase"] == "COMPLETE"
        assert later_decision(store, as_of=12)["basis"] == record_hash
    finally:
        store.close()
