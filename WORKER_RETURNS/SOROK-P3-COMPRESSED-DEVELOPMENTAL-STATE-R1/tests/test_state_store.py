"""Mechanical tests for the normalized P3 sidecar state store.

No P2 world, native rule, model or psychological evaluation is used here.  The
tests exercise real SQLite transactions, cold reopening, indexed targeted reads,
immutable record hashes, recoverable phases, CAS and rollback.
"""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import sys
import threading

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = PACKAGE_ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for entry in (str(PACKAGE_ROOT), str(ENGINE_ROOT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal,
    canonical,
    digest,
)
from p3.state_store import (  # noqa: E402
    PHASE_COMPLETE,
    PHASE_PREPARED,
    PHASE_PSYCH,
    PHASE_WORLD,
    RECORD_COLUMNS,
    PsycheStore,
)


BINDING = {"root": "root-a", "actor": "actor-a", "branch": "branch-a"}
REGISTRY_HASH = "registry-test-only-1"
SOURCE_HASH = "source-test-only-1"
GRADE = "TEST_ONLY_SOURCEFREE_PSYCH_STATE"
RULE = {"rule_id": "rule.mediator", "rule_version": "1", "rule_hash": "rule-hash-1"}
RULE_2 = {"rule_id": "rule.tension", "rule_version": 2, "rule_hash": "rule-hash-2"}


def plan(**overrides):
    value = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "source_hash": SOURCE_HASH,
        "authority": "TEST_ONLY",
        "grade": GRADE,
        "permitted_rules": [dict(RULE), dict(RULE_2)],
    }
    value.update(overrides)
    return value


def state(clock: int, tag: str) -> dict:
    return {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "clock": clock,
        "state_hash": digest({"tag": tag, "clock": clock}),
    }


def event_hash(event_id: str) -> str:
    return "event-hash:" + event_id


def event_binding(clock: int, event_id: str = "event-1", **overrides):
    value = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "event_id": event_id,
        "event_hash": event_hash(event_id),
        "clock": clock,
    }
    value.update(overrides)
    return value


def base_result(
    clock: int,
    event_id: str = "event-1",
    *,
    before: dict | None = None,
    after: dict | None = None,
    **overrides,
):
    value = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "event_id": event_id,
        "event_hash": event_hash(event_id),
        "clock": clock,
        "before": before if before is not None else state(clock - 1, "base-before:" + event_id),
        "after": after if after is not None else state(clock, "base-after:" + event_id),
        "objective": {
            "event": {
                "e1_event_id": event_id,
                "e1_event_hash": event_hash(event_id),
            }
        },
        "receipt_ref": "P2_EVENT:" + event_hash(event_id),
    }
    value.update(overrides)
    return value


def record(
    record_id: str = "record-1",
    *,
    kind: str = "MEDIATOR",
    project: str | None = "project-a",
    counterpart: str | None = "counterpart-a",
    clock: int = 1,
    event_id: str = "event-1",
    payload=None,
    rule=None,
    **overrides,
):
    descriptor = rule or RULE
    value = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "project": project,
        "counterpart": counterpart,
        "record_id": record_id,
        "kind": kind,
        "payload": {"label": record_id} if payload is None else payload,
        "rule_id": descriptor["rule_id"],
        "rule_version": descriptor["rule_version"],
        "rule_hash": descriptor["rule_hash"],
        "registry_hash": REGISTRY_HASH,
        "source_hash": SOURCE_HASH,
        "effective_from": clock,
        "causal_parents": [event_hash(event_id)],
        "grade": GRADE,
    }
    value.update(overrides)
    return value


def opened(tmp_path: Path, name: str = "store.sqlite") -> PsycheStore:
    return PsycheStore(
        tmp_path / name,
        binding=BINDING,
        registry_hash=REGISTRY_HASH,
        source_hash=SOURCE_HASH,
    )


def ready(
    store: PsycheStore,
    operation_id: str = "op-1",
    *,
    clock: int = 1,
    event_id: str = "event-1",
    plan_value=None,
    save: bool = True,
):
    plan_value = plan_value or plan()
    expected = state(clock - 1, "expected:" + operation_id)
    base_before = state(clock - 1, "base-before:" + event_id)
    store.reserve(
        operation_id,
        proposal_hash="proposal:" + operation_id,
        expected=expected,
        plan_hash=digest(plan_value),
        base_before=base_before,
        psyche_before=store.head(),
        plan=plan_value,
    )
    base = base_result(clock, event_id, before=base_before)
    if save:
        store.save_world(operation_id, base)
    return {
        "operation_id": operation_id,
        "plan": plan_value,
        "expected": expected,
        "base_before": base_before,
        "base": base,
        "event": event_binding(clock, event_id),
        "clock": clock,
        "event_id": event_id,
    }


def committed(store: PsycheStore, context: dict, records=None) -> dict:
    records = records if records is not None else [
        record(clock=context["clock"], event_id=context["event_id"])
    ]
    return store.commit_effects(
        context["operation_id"],
        records=records,
        response={"selected": "candidate", "authority": "TEST_ONLY"},
        event_binding=context["event"],
    )


def result_for(store: PsycheStore, context: dict, receipt: dict, **overrides):
    value = {
        "operation_id": context["operation_id"],
        "proposal_hash": "proposal:" + context["operation_id"],
        "before": context["expected"],
        "after": state(context["clock"], "combined:" + context["operation_id"]),
        "status": "REALIZED",
        "objective": {"event": {"event_id": context["event_id"]}},
        "accessible": {"event_id": context["event_id"]},
        "consequences": {"effects_receipt_hash": receipt["receipt_hash"]},
        "readset": [event_hash(context["event_id"])],
        "receipt_ref": "P3:" + context["operation_id"],
    }
    value.update(overrides)
    return value


# ---------------------------------------------------------------------------
# Construction, head, reopening


def test_initial_head_is_derived_and_reopen_is_identical(tmp_path):
    store = opened(tmp_path)
    first = store.head()
    assert set(first) == {"hash", "count"}
    assert first["count"] == 0
    assert first["hash"]
    store.close()
    reopened = opened(tmp_path)
    assert reopened.head() == first
    reopened.close()


def test_reopen_rejects_wrong_binding_registry_source_and_schema(tmp_path):
    store = opened(tmp_path)
    store.close()
    with pytest.raises(RecursionRefusal, match="BINDING|REGISTRY|SOURCE|SCHEMA"):
        PsycheStore(
            tmp_path / "store.sqlite",
            binding={**BINDING, "actor": "other"},
            registry_hash=REGISTRY_HASH,
            source_hash=SOURCE_HASH,
        )
    with pytest.raises(RecursionRefusal, match="REGISTRY"):
        PsycheStore(
            tmp_path / "store.sqlite",
            binding=BINDING,
            registry_hash="other-registry",
            source_hash=SOURCE_HASH,
        )
    with pytest.raises(RecursionRefusal, match="SOURCE"):
        PsycheStore(
            tmp_path / "store.sqlite",
            binding=BINDING,
            registry_hash=REGISTRY_HASH,
            source_hash="other-source",
        )
    connection = sqlite3.connect(tmp_path / "store.sqlite")
    connection.execute("UPDATE p3_meta SET schema='wrong' WHERE id=1")
    connection.commit()
    connection.close()
    with pytest.raises(RecursionRefusal, match="SCHEMA"):
        opened(tmp_path)


def test_head_tamper_and_missing_meta_are_refused(tmp_path):
    store = opened(tmp_path)
    connection = sqlite3.connect(tmp_path / "store.sqlite")
    connection.execute("UPDATE p3_meta SET head_hash='0'*64 WHERE id=1")
    connection.commit()
    connection.close()
    with pytest.raises(RecursionRefusal, match="HEAD"):
        store.head()
    store.close()


# ---------------------------------------------------------------------------
# Reservation and plan validation


def test_reserve_prepared_exact_replay_and_pending(tmp_path):
    store = opened(tmp_path)
    context = ready(store, save=False)
    op = store.get_operation("op-1")
    assert op["phase"] == PHASE_PREPARED
    assert op["proposal_hash"] == "proposal:op-1"
    assert op["expected"] == context["expected"]
    assert op["base_before"] == context["base_before"]
    assert op["psyche_before"] == store.head()
    assert op["base_result"] is None
    assert op["effects_receipt"] is None
    assert op["result"] is None
    assert [item["operation_id"] for item in store.pending()] == ["op-1"]

    again = store.reserve(
        "op-1",
        proposal_hash="proposal:op-1",
        expected=context["expected"],
        plan_hash=digest(context["plan"]),
        base_before=context["base_before"],
        psyche_before=store.head(),
        plan=context["plan"],
    )
    assert again["phase"] == PHASE_PREPARED
    store.close()


def test_reserve_reuse_mismatch_stale_head_and_bad_plans(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    for changed in (
        {"proposal_hash": "other"},
        {"expected": state(0, "other-expected")},
        {"plan_hash": "other-plan-hash"},
        {"base_before": state(0, "other-before")},
    ):
        arguments = {
            "proposal_hash": "proposal:op-1",
            "expected": context["expected"],
            "plan_hash": digest(context["plan"]),
            "base_before": context["base_before"],
            "psyche_before": store.head(),
            "plan": context["plan"],
        }
        arguments.update(changed)
        with pytest.raises(RecursionRefusal, match="REUSE_MISMATCH"):
            store.reserve("op-1", **arguments)

    with pytest.raises(RecursionRefusal, match="STALE_PSYCHE_HEAD"):
        store.reserve(
            "op-old",
            proposal_hash="proposal:old",
            expected=state(0, "old-expected"),
            plan_hash=digest(plan()),
            base_before=state(0, "old-before"),
            psyche_before={"hash": "0" * 64, "count": 0},
            plan=plan(),
        )

    bad_plans = [
        plan(authority="PRODUCTION"),
        plan(grade="NATIVE_SOURCE"),
        plan(production=True),
        plan(native=True),
        plan(source_hash="other-source"),
        plan(root="other-root"),
        plan(permitted_rules=[{**RULE, "extra": "field"}]),
        plan(permitted_rules="not-a-list"),
        {key: value for key, value in plan().items() if key != "permitted_rules"},
    ]
    for index, bad_plan in enumerate(bad_plans):
        with pytest.raises(RecursionRefusal):
            store.reserve(
                f"bad-plan-{index}",
                proposal_hash="proposal:bad",
                expected=state(0, "bad-expected"),
                plan_hash=digest(bad_plan),
                base_before=state(0, "bad-before"),
                psyche_before=store.head(),
                plan=bad_plan,
            )
    store.close()


def test_nested_plan_identity_and_source_are_accepted(tmp_path):
    store = opened(tmp_path)
    nested = {
        "identity": dict(BINDING),
        "source": {"hash": SOURCE_HASH},
        "authority": "TEST_ONLY",
        "grade": GRADE,
        "permitted_rules": [dict(RULE)],
    }
    op = store.reserve(
        "op-nested",
        proposal_hash="proposal:nested",
        expected=state(0, "expected:nested"),
        plan_hash="opaque-plan-hash",
        base_before=state(0, "base:nested"),
        psyche_before=store.head(),
        plan=nested,
    )
    assert op["phase"] == PHASE_PREPARED
    store.close()


def test_frozen_sourcefree_test_only_grade_without_authority_is_accepted(tmp_path):
    store = opened(tmp_path)
    frozen = plan(grade="SOURCEFREE_TEST_ONLY")
    frozen.pop("authority")
    context = ready(store, plan_value=frozen)
    value = record("frozen-sealed", kind="V3MS_MEDIATOR", grade="SOURCEFREE_TEST_ONLY")
    value["hash"] = digest({k: v for k, v in value.items() if k != "hash"})
    receipt = store.commit_effects(
        "op-1",
        records=[value],
        response={"status": "COMPUTED_TEST_ONLY_RESPONSE"},
        event_binding=context["event"],
    )
    assert receipt["authority"] == "TEST_ONLY"
    assert receipt["grade"] == "SOURCEFREE_TEST_ONLY"
    stored = store.query(project="project-a", counterpart="counterpart-a", as_of=1)
    assert len(stored) == 1
    assert stored[0]["kind"] == "V3MS_MEDIATOR"
    assert stored[0]["hash"] == value["hash"]
    store.close()
    reopened = opened(tmp_path)
    assert reopened.query(
        project="project-a", counterpart="counterpart-a", as_of=1
    )[0]["hash"] == value["hash"]
    assert reopened.verify() is True
    reopened.close()


def test_frozen_provenance_conflicts_unknown_and_production_deny(tmp_path):
    store = opened(tmp_path)
    frozen = plan(grade="SOURCEFREE_TEST_ONLY")
    frozen.pop("authority")
    cases = [
        {**frozen, "authority": "PRODUCTION"},
        {**frozen, "authority": "NATIVE"},
        {**frozen, "authority": "UNKNOWN"},
        {**frozen, "authority": "SOURCEFREE_TEST_ONLY"},
        {**frozen, "grade": GRADE},
        {**frozen, "grade": "UNKNOWN"},
        {**frozen, "production": True},
        {**frozen, "native": True},
        {**frozen, "provenance": {"authority": "PRODUCTION"}},
        {**frozen, "provenance": {"grade": "TEST_ONLY_DIFFERENT"}},
        {key: value for key, value in frozen.items() if key != "grade"},
    ]
    for index, bad_plan in enumerate(cases):
        with pytest.raises(RecursionRefusal):
            store.reserve(
                f"bad-frozen-{index}",
                proposal_hash="proposal:bad",
                expected=state(0, "bad-expected"),
                plan_hash=digest(bad_plan),
                base_before=state(0, "bad-before"),
                psyche_before=store.head(),
                plan=bad_plan,
            )
    assert store.pending() == []
    store.close()


def test_save_world_is_idempotent_and_rejects_changed_result(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    op = store.get_operation("op-1")
    assert op["phase"] == PHASE_WORLD
    assert op["base_result"] == context["base"]
    assert store.save_world("op-1", context["base"])["phase"] == PHASE_WORLD
    changed = {**context["base"], "event_hash": "other"}
    with pytest.raises(RecursionRefusal, match="BASE_RESULT_REUSE_MISMATCH"):
        store.save_world("op-1", changed)

    before_mismatch = {**context["base"], "before": state(0, "other-before")}
    store2 = opened(tmp_path, "second.sqlite")
    context2 = {
        "operation_id": "op-2",
        "plan": plan(),
        "expected": state(0, "expected:op-2"),
        "base_before": state(0, "base-before:event-2"),
        "clock": 1,
        "event_id": "event-2",
        "event": event_binding(1, "event-2"),
    }
    store2.reserve(
        "op-2",
        proposal_hash="proposal:op-2",
        expected=context2["expected"],
        plan_hash=digest(context2["plan"]),
        base_before=context2["base_before"],
        psyche_before=store2.head(),
        plan=context2["plan"],
    )
    with pytest.raises(RecursionRefusal, match="BEFORE_MISMATCH"):
        store2.save_world("op-2", before_mismatch)
    store.close()
    store2.close()


def test_commit_requires_world_then_commits_and_replays(tmp_path):
    store = opened(tmp_path)
    context = ready(store, save=False)
    with pytest.raises(RecursionRefusal, match="WORLD_NOT_COMMITTED"):
        store.commit_effects(
            "op-1",
            records=[record()],
            response={},
            event_binding=context["event"],
        )

    store.save_world("op-1", context["base"])
    receipt = committed(store, context)
    assert receipt["phase"] == PHASE_PSYCH
    assert receipt["record_ids"] == ["record-1"]
    assert store.head()["count"] == 1
    assert store.get_operation("op-1")["phase"] == PHASE_PSYCH
    assert [item["operation_id"] for item in store.pending()] == ["op-1"]
    assert [item["record_id"] for item in store.query(
        project="project-a", counterpart="counterpart-a", as_of=1
    )] == ["record-1"]

    replay = store.commit_effects(
        "op-1",
        records=[record()],
        response={"selected": "candidate", "authority": "TEST_ONLY"},
        event_binding=context["event"],
    )
    assert replay == receipt
    with pytest.raises(RecursionRefusal, match="EFFECTS_REPLAY_MISMATCH"):
        store.commit_effects(
            "op-1",
            records=[record(payload={"different": True})],
            response={"selected": "candidate", "authority": "TEST_ONLY"},
            event_binding=context["event"],
        )
    store.close()


def test_finish_completes_and_replays_exact_result(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    receipt = committed(store, context)
    result = result_for(store, context, receipt)
    op = store.finish("op-1", result)
    assert op["phase"] == PHASE_COMPLETE
    assert op["result"] == result
    assert store.pending() == []
    assert store.finish("op-1", result) == op
    with pytest.raises(RecursionRefusal, match="RESULT_REPLAY_MISMATCH"):
        store.finish("op-1", {**result, "status": "HELD"})
    store.close()


def test_finish_before_commit_and_receipt_link_mismatch_refuse(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    with pytest.raises(RecursionRefusal, match="PSYCH_NOT_COMMITTED"):
        store.finish("op-1", result_for(store, context, {"receipt_hash": "none"}))
    receipt = committed(store, context)
    bad = result_for(store, context, receipt)
    bad["consequences"]["effects_receipt_hash"] = "wrong"
    with pytest.raises(RecursionRefusal, match="RECEIPT_LINK_MISMATCH"):
        store.finish("op-1", bad)
    store.close()


def test_zero_record_response_leaves_head_unchanged(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    before = store.head()
    receipt = store.commit_effects(
        "op-1",
        records=[],
        response={"selected": "HELD_EMPTY"},
        event_binding=context["event"],
    )
    assert receipt["records"] == []
    assert receipt["record_ids"] == []
    assert receipt["psyche_before"] == receipt["psyche_after"] == before
    assert store.head() == before
    store.finish("op-1", result_for(store, context, receipt))
    assert store.head() == before
    store.close()


# ---------------------------------------------------------------------------
# Record validation and atomic rollback


def test_one_bad_target_rolls_back_all_records(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    good = record("good")
    bad = record("bad", rule={"rule_id": "not.permitted", "rule_version": "1", "rule_hash": "x"})
    with pytest.raises(RecursionRefusal, match="RULE_NOT_PERMITTED"):
        store.commit_effects(
            "op-1",
            records=[good, bad],
            response={},
            event_binding=context["event"],
        )
    assert store.head()["count"] == 0
    assert store.query(project="project-a", counterpart="counterpart-a", as_of=1) == []
    op = store.get_operation("op-1")
    assert op["phase"] == PHASE_WORLD
    assert op["effects_receipt"] is None
    receipt = committed(store, context, [good])
    assert receipt["record_ids"] == ["good"]
    store.close()


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"root": "other-root"}, id="root"),
        pytest.param({"actor": "other-actor"}, id="actor"),
        pytest.param({"branch": "other-branch"}, id="branch"),
        pytest.param({"source_hash": "other-source"}, id="source"),
        pytest.param({"registry_hash": "other-registry"}, id="registry"),
        pytest.param({"rule_id": "not.permitted"}, id="rule-id"),
        pytest.param({"rule_version": "9"}, id="rule-version"),
        pytest.param({"rule_hash": "wrong"}, id="rule-hash"),
        pytest.param({"kind": "UNKNOWN"}, id="kind"),
        pytest.param({"effective_from": 2}, id="time"),
        pytest.param({"causal_parents": ["not-the-event"]}, id="parent"),
        pytest.param({"grade": "PRODUCTION"}, id="grade"),
        pytest.param({"operation": "REINFORCE"}, id="operation"),
        pytest.param({"payload": {"x": float("nan")}}, id="nonfinite"),
        pytest.param({"hash": "0" * 64}, id="hash"),
        pytest.param({"lifecycle": "ACTIVE"}, id="extra"),
    ],
)
def test_bad_record_targets_do_not_mutate(tmp_path, changes):
    store = opened(tmp_path)
    context = ready(store)
    with pytest.raises(RecursionRefusal):
        store.commit_effects(
            "op-1",
            records=[record(**changes)],
            response={},
            event_binding=context["event"],
        )
    assert store.head()["count"] == 0
    assert store.get_operation("op-1")["phase"] == PHASE_WORLD
    assert store.get_operation("op-1")["effects_receipt"] is None
    store.close()


def test_missing_record_field_is_refused(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    missing = record()
    missing.pop("payload")
    with pytest.raises(RecursionRefusal, match="MISSING_FIELD"):
        store.commit_effects(
            "op-1", records=[missing], response={}, event_binding=context["event"]
        )
    store.close()


def test_kind_alias_operation_create_and_optional_hash_are_normalized(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    value = record("alias", kind="V3MS_MEDIATOR", operation="CREATE")
    receipt = store.commit_effects(
        "op-1",
        records=[value],
        response={},
        event_binding=context["event"],
    )
    stored = store.query(project="project-a", counterpart="counterpart-a", as_of=1)[0]
    assert stored["kind"] == "V3MS_MEDIATOR"
    assert stored["record_id"] == "alias"
    assert stored["hash"] == receipt["record_hashes"][0]
    assert digest({k: v for k, v in stored.items() if k != "hash"}) == stored["hash"]
    store.close()


def test_record_with_correct_explicit_hash_is_accepted(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    value = record("explicit")
    value["hash"] = digest({k: v for k, v in value.items() if k != "hash"})
    receipt = store.commit_effects(
        "op-1", records=[value], response={}, event_binding=context["event"]
    )
    assert receipt["record_ids"] == ["explicit"]
    store.close()


@pytest.mark.parametrize(
    "kind",
    [
        "V3MS_MEDIATOR",
        "V3MS_TENSION",
        "V3MS_PRACTICE",
        "MEDIATOR",
        "TENSION",
        "PRACTICE",
    ],
)
def test_all_allowed_kind_spellings_keep_sealed_hash_through_cold_reopen(tmp_path, kind):
    store = opened(tmp_path)
    context = ready(store)
    value = record("sealed-" + kind, kind=kind)
    value["hash"] = digest({k: v for k, v in value.items() if k != "hash"})
    receipt = store.commit_effects(
        "op-1", records=[value], response={}, event_binding=context["event"]
    )
    stored = store.query(project="project-a", counterpart="counterpart-a", as_of=1)
    assert stored[0]["kind"] == kind
    assert stored[0]["hash"] == value["hash"] == receipt["record_hashes"][0]
    store.close()
    reopened = opened(tmp_path)
    stored = reopened.query(project="project-a", counterpart="counterpart-a", as_of=1)
    assert stored[0]["kind"] == kind
    assert stored[0]["hash"] == value["hash"]
    assert reopened.verify() is True
    reopened.close()


# ---------------------------------------------------------------------------
# Contradiction, CAS and targeted reads


def test_contradictory_records_coexist_and_cas_refuses_stale_commit(tmp_path):
    store = opened(tmp_path)
    first = ready(store, "op-a")
    second = ready(store, "op-b")
    first_receipt = committed(store, first, [record("a", payload={"stance": "open"})])
    with pytest.raises(RecursionRefusal, match="STALE_PSYCHE_HEAD"):
        store.commit_effects(
            "op-b",
            records=[record("b", payload={"stance": "closed"})],
            response={},
            event_binding=second["event"],
        )
    assert store.head()["count"] == 1
    assert [item["record_id"] for item in store.query(
        project="project-a", counterpart="counterpart-a", as_of=1
    )] == ["a"]

    third = ready(store, "op-c")
    store.commit_effects(
        "op-c",
        records=[record("c", payload={"stance": "closed"})],
        response={},
        event_binding=third["event"],
    )
    records = store.query(project="project-a", counterpart="counterpart-a", as_of=1)
    assert [item["record_id"] for item in records] == ["a", "c"]
    assert {item["payload"]["stance"] for item in records} == {"open", "closed"}
    store.close()


def test_query_is_exact_scope_effective_time_and_indexed(tmp_path):
    store = opened(tmp_path)
    context = ready(store, "op-base", clock=1, event_id="event-1")
    store.commit_effects(
        "op-base",
        records=[
            record("p1c1-early", project="p1", counterpart="c1", clock=1),
            record("p1c1-late", project="p1", counterpart="c1", clock=1, payload={"n": 2}),
            record("p1c2", project="p1", counterpart="c2", clock=1),
            record("p2c1", project="p2", counterpart="c1", clock=1),
        ],
        response={},
        event_binding=context["event"],
    )
    before = store.stats()
    matched = store.query(project="p1", counterpart="c1", as_of=1)
    after = store.stats()
    assert [item["record_id"] for item in matched] == ["p1c1-early", "p1c1-late"]
    assert after["targeted_queries"] == before["targeted_queries"] + 1
    assert after["row_reads"] - before["row_reads"] == len(matched)
    assert after["full_scans"] == before["full_scans"] == 0
    assert store.query(project="p1", counterpart="c1", as_of=0) == []
    assert [item["record_id"] for item in store.query(
        project=None, counterpart=None, as_of=1
    )] == []
    store.close()


def test_query_effective_time_order_and_null_scope(tmp_path):
    store = opened(tmp_path)
    for index, clock in enumerate((1, 2, 3), start=1):
        context = ready(store, f"op-{index}", clock=clock, event_id=f"event-{index}")
        store.commit_effects(
            f"op-{index}",
            records=[
                record(
                    f"r{index}",
                    clock=clock,
                    event_id=f"event-{index}",
                    project=None,
                    counterpart="c1",
                )
            ],
            response={},
            event_binding=context["event"],
        )
    assert [item["record_id"] for item in store.query(
        project=None, counterpart="c1", as_of=2
    )] == ["r1", "r2"]
    assert [item["record_id"] for item in store.query(
        project=None, counterpart="c1", as_of=3
    )] == ["r1", "r2", "r3"]
    store.close()


# ---------------------------------------------------------------------------
# P2-like base result, event binding, cold reopen and integrity


def test_actual_p2_event_object_shape_is_accepted(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    receipt = store.commit_effects(
        "op-1",
        records=[record()],
        response={},
        event_binding=context["event"],
    )
    assert receipt["event_binding"]["event_id"] == "event-1"
    store.close()


def test_nested_owner_event_binding_and_top_level_base_fallback(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    nested_event = {
        "owner": dict(BINDING),
        "event_id": "event-1",
        "event_hash": event_hash("event-1"),
        "clock": 1,
    }
    receipt = store.commit_effects(
        "op-1", records=[record()], response={}, event_binding=nested_event
    )
    assert receipt["phase"] == PHASE_PSYCH
    store.close()

    store2 = opened(tmp_path, "fallback.sqlite")
    context2 = ready(store2, "op-2", event_id="event-2", save=False)
    fallback_base = {
        "root": BINDING["root"],
        "actor": BINDING["actor"],
        "branch": BINDING["branch"],
        "event_id": "event-2",
        "event_hash": event_hash("event-2"),
        "clock": 1,
    }
    # The reserved base is replaced only for this isolated fallback check.
    store2.save_world("op-2", {**fallback_base, "before": context2["base_before"]})
    receipt2 = store2.commit_effects(
        "op-2",
        records=[record("r2", event_id="event-2")],
        response={},
        event_binding=context2["event"],
    )
    assert receipt2["phase"] == PHASE_PSYCH
    store2.close()


def test_prior_three_kind_schema_migrates_and_accepts_v3ms_losslessly(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    legacy = record("legacy-canonical", kind="MEDIATOR")
    legacy["hash"] = digest({k: v for k, v in legacy.items() if k != "hash"})
    store.commit_effects(
        "op-1", records=[legacy], response={}, event_binding=context["event"]
    )
    store.close()

    connection = sqlite3.connect(tmp_path / "store.sqlite")
    try:
        connection.execute("ALTER TABLE p3_records RENAME TO p3_records_current")
        connection.execute(
            "CREATE TABLE p3_records ("
            "seq INTEGER PRIMARY KEY AUTOINCREMENT,"
            "record_id TEXT NOT NULL UNIQUE,"
            "root TEXT NOT NULL,"
            "actor TEXT NOT NULL,"
            "branch TEXT NOT NULL,"
            "project TEXT,"
            "counterpart TEXT,"
            "kind TEXT NOT NULL CHECK(kind IN ('MEDIATOR','TENSION','PRACTICE')),"
            "payload_json TEXT NOT NULL,"
            "rule_id TEXT NOT NULL,"
            "rule_version_json TEXT NOT NULL,"
            "rule_hash TEXT NOT NULL,"
            "registry_hash TEXT NOT NULL,"
            "source_hash TEXT NOT NULL,"
            "effective_from INTEGER NOT NULL,"
            "causal_parents_json TEXT NOT NULL,"
            "grade TEXT NOT NULL,"
            "hash TEXT NOT NULL UNIQUE,"
            "record_json TEXT NOT NULL,"
            "previous_chain TEXT NOT NULL,"
            "chain_hash TEXT NOT NULL UNIQUE,"
            "operation_id TEXT NOT NULL)"
        )
        columns = ", ".join(RECORD_COLUMNS)
        connection.execute(
            "INSERT INTO p3_records (" + columns + ") "
            "SELECT " + columns + " FROM p3_records_current"
        )
        connection.execute("DROP TABLE p3_records_current")
        connection.commit()
    finally:
        connection.close()

    reopened = opened(tmp_path)
    assert reopened._connection.execute("PRAGMA user_version").fetchone()[0] == 2
    assert reopened.query(project="project-a", counterpart="counterpart-a", as_of=1)[0]["hash"] == legacy["hash"]
    second = ready(reopened, "op-2", clock=2, event_id="event-2")
    upgraded = record("v3ms-after-migration", kind="V3MS_MEDIATOR", clock=2, event_id="event-2")
    upgraded["hash"] = digest({k: v for k, v in upgraded.items() if k != "hash"})
    reopened.commit_effects(
        "op-2", records=[upgraded], response={}, event_binding=second["event"]
    )
    rows = reopened.query(project="project-a", counterpart="counterpart-a", as_of=2)
    assert [row["record_id"] for row in rows] == [
        "legacy-canonical",
        "v3ms-after-migration",
    ]
    assert rows[1]["kind"] == "V3MS_MEDIATOR"
    assert rows[1]["hash"] == upgraded["hash"]
    assert reopened.verify() is True
    reopened.close()


def test_cold_reopen_preserves_head_records_operations_and_pending(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    receipt = committed(store, context)
    store.finish("op-1", result_for(store, context, receipt))
    pending_context = ready(store, "op-pending", clock=2, event_id="event-2")
    head = store.head()
    records = store.query(project="project-a", counterpart="counterpart-a", as_of=2)
    store.close()

    reopened = opened(tmp_path)
    assert reopened.head() == head
    assert reopened.query(project="project-a", counterpart="counterpart-a", as_of=2) == records
    assert reopened.get_operation("op-1")["phase"] == PHASE_COMPLETE
    assert reopened.get_operation("op-pending")["phase"] == PHASE_WORLD
    assert [item["operation_id"] for item in reopened.pending()] == ["op-pending"]
    assert reopened.verify() is True
    reopened.close()


def test_record_json_tamper_is_detected_by_query_and_verify(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    committed(store, context)
    store.close()
    connection = sqlite3.connect(tmp_path / "store.sqlite")
    connection.execute(
        "UPDATE p3_records SET record_json=replace(record_json, 'record-1', 'record-X') "
        "WHERE record_id='record-1'"
    )
    connection.commit()
    connection.close()
    reopened = opened(tmp_path)
    with pytest.raises(RecursionRefusal, match="JOURNAL_INTEGRITY"):
        reopened.query(project="project-a", counterpart="counterpart-a", as_of=1)
    with pytest.raises(RecursionRefusal, match="JOURNAL_INTEGRITY"):
        reopened.verify()
    reopened.close()


def test_operation_phase_and_result_tamper_is_detected(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    receipt = committed(store, context)
    store.finish("op-1", result_for(store, context, receipt))
    store.close()
    connection = sqlite3.connect(tmp_path / "store.sqlite")
    connection.execute("UPDATE p3_operations SET phase='PREPARED' WHERE operation_id='op-1'")
    connection.commit()
    connection.close()
    reopened = opened(tmp_path)
    # The operation document still has durable later-phase payloads; the phase
    # itself is a valid enum value, but full verification catches the linkage.
    with pytest.raises(RecursionRefusal):
        reopened.verify()
    reopened.close()


# ---------------------------------------------------------------------------
# O(1) head, storage shape and lifecycle


def test_head_uses_constant_reads_with_many_records(tmp_path):
    store = opened(tmp_path)
    context = ready(store)
    records = [record(f"r{index}") for index in range(25)]
    store.commit_effects(
        "op-1", records=records, response={}, event_binding=context["event"]
    )
    before = store.stats()
    head = store.head()
    after = store.stats()
    assert head["count"] == 25
    assert after["row_reads"] - before["row_reads"] <= 2
    assert after["full_scans"] == before["full_scans"] == 0
    store.close()


def test_storage_rows_and_targeted_read_cost_grow_without_full_scan(tmp_path):
    store = opened(tmp_path)
    counts = []
    for index in range(1, 13):
        context = ready(store, f"op-{index}", clock=index, event_id=f"event-{index}")
        store.commit_effects(
            f"op-{index}",
            records=[
                record(
                    f"r{index}",
                    clock=index,
                    event_id=f"event-{index}",
                    project=f"p{index % 3}",
                    counterpart=f"c{index % 2}",
                )
            ],
            response={},
            event_binding=context["event"],
        )
        counts.append(store.head()["count"])
    assert counts == list(range(1, 13))
    before = store.stats()
    matched = store.query(project="p1", counterpart="c1", as_of=12)
    after = store.stats()
    assert after["row_reads"] - before["row_reads"] == len(matched)
    assert after["full_scans"] == before["full_scans"] == 0
    assert after["db_bytes"] + after["wal_bytes"] > 0
    store.close()


def test_unknown_operation_close_and_idempotent_close(tmp_path):
    store = opened(tmp_path)
    assert store.get_operation("missing") is None
    store.close()
    store.close()
    with pytest.raises(RecursionRefusal, match="STORE_CLOSED"):
        store.head()
