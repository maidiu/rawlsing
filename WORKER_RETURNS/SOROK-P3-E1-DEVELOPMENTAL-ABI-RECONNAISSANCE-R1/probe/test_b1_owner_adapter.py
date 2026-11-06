"""Executable compatibility matrix for the B1 -> DevelopmentOwner adapter."""
from __future__ import annotations

import importlib.util
import json
import os
from dataclasses import replace
from pathlib import Path
import shutil
import sys

import pytest

HERE = Path(__file__).resolve()
PROBE = HERE.parent
REPO = Path(
    os.environ.get(
        "SOROK_REPO_ROOT", str(PROBE.parents[2] if len(PROBE.parents) > 2 else PROBE)
    )
)
ENGINE = Path(
    os.environ.get(
        "SOROK_ENGINE_PATH",
        str(REPO / "WORKER_RETURNS" / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"),
    )
)
if not ENGINE.is_dir():
    raise RuntimeError("SOROK_ENGINE_PATH is not a directory: " + str(ENGINE))
for path in (str(ENGINE), str(PROBE)):
    if path not in sys.path:
        sys.path.insert(0, path)

from developmental_recursion.contracts import EventProposal, RecursionRefusal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402

from b1_owner_adapter import GRADE, OPERATION, B1Owner  # noqa: E402


def make_owner(tmp_path: Path, name: str, *, journal_only: bool = False,
               root: str | None = None) -> B1Owner:
    return B1Owner(
        tmp_path / (name + ".sqlite"),
        root=root or ("root-" + name),
        branch="main",
        journal_only=journal_only,
    )


def make_proposals(source_ref: str) -> list[EventProposal]:
    def proposal(event_id: str, event_time: int, *, interrupted: bool, plan: str,
                 objective: str) -> EventProposal:
        return EventProposal(
            event_id,
            event_time,
            OPERATION,
            (source_ref,),
            ("child", "caretaker"),
            {
                "b1": {
                    "world_ref": "world:garage",
                    "objective_occurrence": objective,
                    "project": "repair_route",
                    "power_ref": "power:caretaker_controls_tools",
                    "offers": [["caretaker", "Let us check what can be secured.", plan]],
                    "interrupted": interrupted,
                }
            },
            None,
        )

    return [
        proposal("event1", 2, interrupted=True, plan="joint_inventory",
                 objective="bike_stolen"),
        proposal("event2", 3, interrupted=False, plan="no_plan",
                 objective="shared_tool_offer"),
        proposal("event3", 4, interrupted=False, plan="joint_inventory",
                 objective="shared_tool_offer"),
    ]


def scenario(tmp_path: Path, name: str, *, journal_only: bool = False):
    owner = make_owner(tmp_path, name, journal_only=journal_only)
    journal = tmp_path / (name + ".journal.sqlite")
    engine = BatchEngine(owner, journal)
    proposals = make_proposals(owner.source_ref)
    result = engine.run_batch("batch-" + name, proposals)
    return owner, engine, result, proposals, journal


def test_positive_three_event_batch_persists_mediator_and_later_reader(tmp_path):
    owner, engine, result, proposals, journal = scenario(tmp_path, "positive")
    try:
        records = result["records"]
        assert [row["status"] for row in records] == ["REALIZED", "NO_CHANGE", "REALIZED"]
        mediator = records[0]["consequences"]["middle_state_ids"]
        mediator_records = records[0]["consequences"]["middle_state_record_hashes"]
        assert len(mediator) == 1 and len(mediator_records) == 1
        assert records[1]["consequences"]["middle_state_ids"] == mediator
        assert records[1]["consequences"]["practical_activity"] == []
        assert records[1]["accessible"]["actor_surface"]["actions"] == []
        assert records[2]["consequences"]["recruited"] == mediator_records
        assert records[2]["consequences"]["practical_activity"] == ["joint_check:caretaker"]
        assert records[0]["accessible"]["actor_surface"] == {
            "actions": ["compare_current_plan:caretaker"],
            "origin_explanation": "NOT_ACCESSIBLE",
        }
        assert "joint_check" not in json.dumps(records[0]["accessible"])
        assert records[0]["readset"][0] == owner.source_ref
        assert records[0]["readset"][1] == records[0]["objective"]["event"]["hash"]
        assert records[0]["receipt_ref"].startswith("B1_JOINT:")
        assert records[0]["consequences"]["durable_psychological_transition"] == (
            "TEST_ONLY_B1_V3MS_MEDIATOR"
        )
        assert records[0]["consequences"]["native_science"] == "NOT_ISSUED"
        assert records[0]["consequences"]["source_rule_ids"] == [
            "TEST_ONLY_CAN008_B1", "TEST_ONLY_CAN011_B1"
        ]
        assert engine.verify()

        before_reopen = owner.snapshot()
        owner.close()
        engine.close()
        reopened = B1Owner(tmp_path / "positive.sqlite", root="root-positive", branch="main")
        try:
            assert reopened.snapshot() == before_reopen
            reopened_engine = BatchEngine(reopened, journal)
            try:
                assert reopened_engine.history("batch-positive") == result
                replay = reopened_engine.run_batch("batch-positive", proposals)
                assert replay == result
                assert len(reopened.state()["middle"]) == 1
                assert len(reopened.state()["responses"]) == 3
                assert reopened.db.execute(
                    "SELECT COUNT(*) FROM b1_operations WHERE status='COMPLETE'"
                ).fetchone()[0] == 3
            finally:
                reopened_engine.close()
        finally:
            reopened.close()
    finally:
        if owner.db:
            try:
                owner.close()
            except Exception:
                pass
        engine.close()


def test_identical_later_event_differs_under_changed_prior_state(tmp_path):
    positive, positive_engine, positive_result, positive_props, _ = scenario(
        tmp_path, "positive-compare"
    )
    control, control_engine, control_result, control_props, _ = scenario(
        tmp_path, "control-compare", journal_only=True
    )
    try:
        assert positive_props == control_props
        p3 = positive_result["records"][2]
        c3 = control_result["records"][2]
        assert p3["objective"]["event"]["hash"] == c3["objective"]["event"]["hash"]
        assert p3["consequences"]["practical_activity"] == ["joint_check:caretaker"]
        assert c3["consequences"]["practical_activity"] == ["inspect_alone:caretaker"]
        mediator = positive_result["records"][0]["consequences"]["middle_state_record_hashes"]
        assert p3["consequences"]["recruited"] == mediator
        assert c3["consequences"]["recruited"] == []
        assert len(positive.state()["middle"]) == 1
        assert control.state()["middle"] == []
    finally:
        for item in (positive, control):
            try:
                item.close()
            except Exception:
                pass
        positive_engine.close()
        control_engine.close()


def test_invalid_actor_source_clock_interval_and_operation_do_not_mutate(tmp_path):
    owner = make_owner(tmp_path, "negative")
    engine = BatchEngine(owner, tmp_path / "negative.journal.sqlite")
    proposals = make_proposals(owner.source_ref)
    before = owner.snapshot()
    try:
        bads = [
            replace(proposals[0], participants=("child", "stranger")),
            replace(proposals[0], source_refs=("B1_FIXTURE:wrong",)),
            replace(proposals[0], event_time=before.clock),
            replace(proposals[0], interval={"mode": "ACTUAL", "span": 1}),
            replace(proposals[0], operation="CAN008_NATIVE"),
        ]
        for bad in bads:
            with pytest.raises(RecursionRefusal):
                engine.run_batch("bad-batch", [bad, proposals[1], proposals[2]])
            assert owner.snapshot() == before
            assert owner.db.execute("SELECT COUNT(*) FROM occurrence").fetchone()[0] == 0
            assert owner.db.execute(
                "SELECT COUNT(*) FROM b1_operations"
            ).fetchone()[0] == 0
            assert engine._connect().execute(
                "SELECT COUNT(*) FROM batches"
            ).fetchone()[0] == 0
        with pytest.raises(RecursionRefusal, match="STALE"):
            owner.realize(
                "wrong-expected", proposals[0],
                replace(before, root="foreign-root"),
            )
        assert owner.snapshot() == before
        assert owner.db.execute("SELECT COUNT(*) FROM occurrence").fetchone()[0] == 0
        assert engine.verify()
    finally:
        engine.close()
        owner.close()


def test_foreign_root_and_source_tamper_with_exact_restore(tmp_path):
    db = tmp_path / "binding.sqlite"
    owner = B1Owner(db, root="root-a", branch="main")
    try:
        before = owner.snapshot()
        copy = tmp_path / "binding-copy.sqlite"
        owner.close()
        shutil.copy2(db, copy)
        with pytest.raises(RecursionRefusal, match="BINDING"):
            B1Owner(copy, root="root-b", branch="main")
        owner = B1Owner(db, root="root-a", branch="main")
        body = owner.db.execute("SELECT body FROM b1_source WHERE id=1").fetchone()[0]
        tampered = json.loads(body)
        tampered["response_rule_hash"] = "FORGED"
        owner.db.execute(
            "UPDATE b1_source SET body=? WHERE id=1", (json.dumps(tampered),)
        )
        owner.db.commit()
        with pytest.raises(RecursionRefusal, match="SOURCE_IDENTITY_TAMPERED"):
            owner.snapshot()
        owner.db.execute("UPDATE b1_source SET body=? WHERE id=1", (body,))
        owner.db.commit()
        assert owner.snapshot() == before
    finally:
        owner.close()


def test_operation_idempotency_and_ambiguous_reservation_hold(tmp_path):
    owner = make_owner(tmp_path, "operations")
    proposals = make_proposals(owner.source_ref)
    before = owner.snapshot()
    try:
        first = owner.realize("op-1", proposals[0], before)
        again = owner.realize("op-1", proposals[0], before)
        assert first == again
        with pytest.raises(RecursionRefusal, match="REUSE_MISMATCH"):
            owner.realize("op-1", replace(proposals[0], event_id="other"), before)

        before_second = owner.snapshot()
        from developmental_recursion.contracts import canonical, digest
        owner.db.execute(
            "INSERT INTO b1_operations VALUES (?,?,?,'RESERVED',NULL,NULL)",
            (
                "op-2",
                digest(proposals[1].document()),
                canonical(before_second.document()),
            ),
        )
        owner.db.commit()
        with pytest.raises(RecursionRefusal, match="AMBIGUOUS"):
            owner.realize("op-2", proposals[1], before_second)
        assert owner.snapshot() == before_second
        owner.db.execute("DELETE FROM b1_operations WHERE id='op-2'")
        owner.db.commit()
        result = owner.realize("op-2", proposals[1], before_second)
        assert result.after.clock == proposals[1].event_time
        assert result.status == "NO_CHANGE"
        assert len(owner.state()["responses"]) == 2
        assert len(owner.state()["middle"]) == 1
    finally:
        owner.close()


def test_middle_rule_version_tamper_is_refused_without_mutation(tmp_path):
    owner = make_owner(tmp_path, "rule-version")
    proposals = make_proposals(owner.source_ref)
    try:
        owner.realize("op-1", proposals[0], owner.snapshot())
        state = owner.state()
        state["middle"][0]["creation_or_update_rule_ref"]["rule_version"] = "2"
        owner.db.execute(
            "UPDATE checkpoint SET body=? WHERE id=1", (json.dumps(state),)
        )
        owner.db.commit()
        before = owner.snapshot()
        with pytest.raises(RecursionRefusal, match="MIDDLE_STATE_INTEGRITY_FAILURE"):
            owner.realize("op-2", proposals[1], before)
        assert owner.snapshot() == before
        assert len(owner.state()["middle"]) == 1
    finally:
        owner.close()


def test_mediator_severance_breaks_later_reader_and_restoration_restores(tmp_path):
    db_a = tmp_path / "sever-a.sqlite"
    owner_a = B1Owner(db_a, root="root-sever-a", branch="main")
    proposals = make_proposals(owner_a.source_ref)
    mediator = None
    try:
        owner_a.realize("a1", proposals[0], owner_a.snapshot())
        owner_a.realize("a2", proposals[1], owner_a.snapshot())
        state = owner_a.state()
        assert len(state["middle"]) == 1
        mediator = state["middle"][0]["middle_state_record_hash"]
        owner_a.close()

        db_b = tmp_path / "sever-b.sqlite"
        shutil.copy2(db_a, db_b)
        owner_b = B1Owner(db_b, root="root-sever-a", branch="main")
        try:
            tampered = owner_b.state()
            tampered["middle"] = []
            owner_b.db.execute(
                "UPDATE checkpoint SET body=? WHERE id=1", (json.dumps(tampered),)
            )
            owner_b.db.commit()
            result_b = owner_b.realize("b3", proposals[2], owner_b.snapshot())
            assert result_b.consequences["practical_activity"] == [
                "inspect_alone:caretaker"
            ]
            assert result_b.consequences["recruited"] == []
        finally:
            owner_b.close()

        owner_a = B1Owner(db_a, root="root-sever-a", branch="main")
        result_a = owner_a.realize("a3", proposals[2], owner_a.snapshot())
        assert result_a.consequences["practical_activity"] == ["joint_check:caretaker"]
        assert result_a.consequences["recruited"] == [mediator]
    finally:
        try:
            owner_a.close()
        except Exception:
            pass


def test_production_zero_positive_guard_still_denies():
    guard_path = REPO / "rawlsing_next" / "v3_psepf_zero_positive_guard.py"
    spec = importlib.util.spec_from_file_location("p3_zero_guard", guard_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert dict(module.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    decision = module.evaluate_psepf_zero_positive_guard(
        {
            "actor_id": "child",
            "source_class": "ResolvedStructuralContext",
            "source_ref": "B1:event1",
            "source_hash": "a" * 64,
            "source_lineage": [],
            "transition_surface_id": "B1_CAN011_MEDIATOR",
            "operation_class": "CREATE",
            "state_fingerprint": {
                "actor_state_hash": "b" * 64,
                "causal_ledger_hash": "c" * 64,
                "causal_cursor": "1",
                "rng_state_hash": "d" * 64,
                "scheduler_state_hash": "e" * 64,
            },
            "authority": None,
        }
    )
    assert decision.outcome == module.GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason == module.GuardReason.ZERO_POSITIVE_REGISTRY
    assert decision.zero_effect


def test_adapter_grade_and_source_pin_are_declared():
    assert GRADE == "TEST_ONLY_B1_DEVELOPMENT_OWNER_ADAPTER_NOT_NATIVE"
    assert OPERATION == "B1_RESPOND"
    from b1_owner_adapter import B1_BLOB, B1_SHA256
    assert B1_BLOB == "94ffc52847e4c8ae760212d1bc8543594ba793fa"
    assert B1_SHA256.startswith("478b989730f49a5")
