"""Exact core tests for the owner-governed batch engine.

The owner in these tests is a software fixture that keeps real durable
operation receipts and mutable actor/world state.  It deliberately carries an
explicit ``MISSING_RULE`` consequence: this suite proves execution and custody,
not unavailable developmental science.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import sys
import threading

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import developmental_recursion.engine as engine_module
from developmental_recursion.contracts import (
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    digest,
)
from developmental_recursion.engine import BatchEngine


class ControlledOwner:
    """A real, stateful owner fixture with durable operation receipts."""

    def __init__(
        self,
        *,
        root: str = "root-1",
        actor: str = "actor-1",
        branch: str = "branch-1",
        clock: int = 0,
    ):
        self.root = root
        self.actor = actor
        self.branch = branch
        self.clock = clock
        self.order: list[str] = []
        self.extra: dict = {}
        self.receipts: dict[str, RealizedEvent] = {}
        self.pending: dict[str, RealizedEvent] = {}
        self.operation_ids: list[str] = []
        self.expected_states: list[StateIdentity] = []
        self.validation_calls = 0
        self.realize_calls = 0
        self.effect_count = 0
        self.held = False
        self.mutate_on_validate = False
        self.corrupt_result = None
        self.refuse_validation_for: set[str] = set()
        self.crash_after_receipt_for: set[str] = set()
        self.crash_before_receipt_for: set[str] = set()
        self._lock = threading.RLock()

    def snapshot(self) -> StateIdentity:
        with self._lock:
            return StateIdentity(
                self.root,
                self.actor,
                self.branch,
                self.clock,
                digest({"order": self.order, "clock": self.clock, "extra": self.extra}),
            )

    def validate_proposal(self, proposal: EventProposal) -> None:
        with self._lock:
            self.validation_calls += 1
            if proposal.event_id in self.refuse_validation_for:
                raise RecursionRefusal("FIXTURE_PROPOSAL_REFUSED")
            if proposal.operation not in {"ACT", "OBSERVE"}:
                raise RecursionRefusal("FIXTURE_OPERATION_NOT_AUTHORIZED")
            if proposal.event_time <= self.clock:
                raise RecursionRefusal("FIXTURE_EVENT_CLOCK_NOT_FUTURE")
            if self.mutate_on_validate:
                self.clock += 1

    def realize(
        self,
        operation_id: str,
        proposal: EventProposal,
        expected: StateIdentity,
    ) -> RealizedEvent:
        with self._lock:
            self.operation_ids.append(operation_id)
            self.expected_states.append(expected)
            self.realize_calls += 1
            if operation_id in self.receipts:
                return self.receipts[operation_id]
            if operation_id in self.pending:
                raise RecursionRefusal("AMBIGUOUS_PRIOR_OPERATION_HOLD")
            if self.snapshot() != expected:
                raise RecursionRefusal("FIXTURE_STALE_STATE")

            before = expected
            prior = list(self.order)
            self.order.append(proposal.event_id)
            self.clock = proposal.event_time
            self.effect_count += 1
            after = self.snapshot()
            status = "HELD" if self.held else "REALIZED"
            result = RealizedEvent(
                operation_id=operation_id,
                proposal_hash=digest(proposal.document()),
                before=before,
                after=after,
                status=status,
                objective={
                    "event_id": proposal.event_id,
                    "prior_order": prior,
                },
                accessible={
                    "event_id": proposal.event_id,
                    "accessible_from_this_actor": True,
                },
                consequences={
                    "event_id": proposal.event_id,
                    "durable_psychological_transition": "MISSING_RULE",
                },
                readset=tuple(proposal.source_refs),
                receipt_ref="receipt:" + operation_id,
            )
            if proposal.event_id in self.crash_before_receipt_for:
                self.crash_before_receipt_for.discard(proposal.event_id)
                self.pending[operation_id] = result
                raise RuntimeError("simulated interruption before owner receipt")
            self.receipts[operation_id] = result
            if proposal.event_id in self.crash_after_receipt_for:
                self.crash_after_receipt_for.discard(proposal.event_id)
                raise RuntimeError("simulated interruption after owner receipt")
            if self.corrupt_result is not None:
                return self.corrupt_result(result)
            return result

    def resolve_pending(self, operation_id: str) -> None:
        with self._lock:
            self.receipts[operation_id] = self.pending.pop(operation_id)


def event(
    event_id: str,
    event_time: int,
    *,
    operation: str = "ACT",
    source_refs=("source:1",),
    participants=("actor-1",),
    circumstances=None,
    interval=None,
) -> EventProposal:
    return EventProposal(
        event_id,
        event_time,
        operation,
        tuple(source_refs),
        tuple(participants),
        {} if circumstances is None else circumstances,
        interval,
    )


def three(prefix: str = "e", start: int = 1) -> list[EventProposal]:
    return [event(f"{prefix}{i}", start + i - 1) for i in range(1, 4)]


def assert_reserved_without_result(journal: Path, batch_id: str = "batch") -> None:
    connection = sqlite3.connect(journal)
    try:
        row = connection.execute(
            "SELECT status, result_json, record_json FROM events "
            "WHERE batch_id=? AND event_index=0",
            (batch_id,),
        ).fetchone()
    finally:
        connection.close()
    assert row is not None
    assert row[0] == "RESERVED"
    assert row[1] is None
    assert row[2] is None


# ---------------------------------------------------------------------------
# Boundary and strict pre-effect validation


@pytest.mark.parametrize(
    "proposals",
    [
        pytest.param([event("e1", 1), event("e2", 2)], id="two"),
        pytest.param([event(f"e{i}", i) for i in range(1, 7)], id="six"),
        pytest.param([event("same", 1), event("same", 2), event("e3", 3)], id="duplicate-id"),
        pytest.param([event("", 1), event("e2", 2), event("e3", 3)], id="empty-id"),
        pytest.param(
            [event("e1", 1, circumstances={"x": float("nan")}), event("e2", 2), event("e3", 3)],
            id="nonfinite",
        ),
        pytest.param([event("e1", True), event("e2", 2), event("e3", 3)], id="bool-clock"),
        pytest.param([event("e1", -1), event("e2", 2), event("e3", 3)], id="negative-clock"),
        pytest.param(
            [event("e1", 1, source_refs=(123,)), event("e2", 2), event("e3", 3)],
            id="bad-source-element",
        ),
        pytest.param(
            [
                {**event("e1", 1).document(), "fixed_story": "forbidden"},
                event("e2", 2),
                event("e3", 3),
            ],
            id="extra-document-key",
        ),
    ],
)
def test_batch_requires_exactly_three_to_five_valid_proposals_before_effects(
    tmp_path, proposals
):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    with pytest.raises(RecursionRefusal):
        engine.run_batch("batch", proposals)
    assert owner.realize_calls == 0
    assert owner.effect_count == 0
    assert owner.order == []


def test_invalid_owner_snapshot_is_refused_before_effects(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    owner.root = ""
    with pytest.raises(RecursionRefusal, match="OWNER_SNAPSHOT_INVALID"):
        engine.run_batch("batch", three())
    assert owner.realize_calls == 0


def test_owner_mutation_during_validation_is_refused_before_effects(tmp_path):
    owner = ControlledOwner()
    owner.mutate_on_validate = True
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    with pytest.raises(RecursionRefusal, match="MUTATED_DURING_VALIDATION"):
        engine.run_batch("batch", three())
    assert owner.realize_calls == 0
    assert owner.effect_count == 0


def test_all_five_proposals_are_validated_before_any_realization(tmp_path):
    owner = ControlledOwner()
    owner.refuse_validation_for.add("e5")
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    with pytest.raises(RecursionRefusal, match="FIXTURE_PROPOSAL_REFUSED"):
        engine.run_batch("batch", [event(f"e{i}", i) for i in range(1, 6)])
    assert owner.validation_calls == 5
    assert owner.realize_calls == 0
    assert owner.effect_count == 0


def test_optional_interval_may_be_omitted_from_document_inputs(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    documents = []
    for index in range(1, 6):
        document = event(f"e{index}", index).document()
        document.pop("interval")
        documents.append(document)
    result = engine.run_batch("batch", documents)
    assert len(result["records"]) == 5
    assert owner.order == ["e1", "e2", "e3", "e4", "e5"]
    assert engine.run_batch("batch", [event(f"e{i}", i) for i in range(1, 6)]) == result


# ---------------------------------------------------------------------------
# Actual owner state, ordering, current state and readset


def test_order_matters_through_actual_owner_state(tmp_path):
    owner_a = ControlledOwner()
    owner_b = ControlledOwner()
    engine_a = BatchEngine(owner_a, tmp_path / "a.sqlite")
    engine_b = BatchEngine(owner_b, tmp_path / "b.sqlite")

    proposals_a = [event("A", 1), event("B", 2), event("C", 3)]
    proposals_b = [event("B", 1), event("A", 2), event("C", 3)]
    result_a = engine_a.run_batch("batch-a", proposals_a)
    result_b = engine_b.run_batch("batch-b", proposals_b)

    assert owner_a.order == ["A", "B", "C"]
    assert owner_b.order == ["B", "A", "C"]
    assert result_a["records"][1]["objective"]["prior_order"] == ["A"]
    assert result_b["records"][0]["objective"]["prior_order"] == []
    assert result_a["history_hash"] != result_b["history_hash"]
    assert all(
        record["consequences"]["durable_psychological_transition"] == "MISSING_RULE"
        for record in result_a["records"]
    )


def test_each_step_receives_the_actual_post_event_state_and_persists_readset(tmp_path):
    owner = ControlledOwner()
    initial = owner.snapshot()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    proposals = [
        event("e1", 1, source_refs=("source:a", "source:b")),
        event("e2", 2, source_refs=("source:c",)),
        event("e3", 3),
    ]
    result = engine.run_batch("batch", proposals)
    records = result["records"]

    assert owner.expected_states[0] == initial
    for index in range(1, 3):
        assert owner.expected_states[index].document() == records[index - 1]["after"]
        assert records[index]["before"] == records[index - 1]["after"]
    assert records[0]["readset"] == ["source:a", "source:b"]
    assert records[1]["readset"] == ["source:c"]
    assert len({record["operation_id"] for record in records}) == 3
    assert len({record["receipt_ref"] for record in records}) == 3
    assert records[-1]["after"] == owner.snapshot().document()
    assert engine.verify() is True


# ---------------------------------------------------------------------------
# Replay, immutable binding and conflicting reuse


def test_completed_replay_is_identical_and_does_not_call_the_owner_again(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    proposals = three()
    first = engine.run_batch("batch", proposals)
    calls = owner.realize_calls
    state = owner.snapshot()

    second = engine.run_batch("batch", [proposal.document() for proposal in proposals])

    assert second == first
    assert owner.realize_calls == calls
    assert owner.snapshot() == state
    assert engine.history("batch") == first


def test_conflicting_batch_or_event_reuse_is_refused_without_effects(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    proposals = three()
    engine.run_batch("batch", proposals)
    effects = owner.effect_count

    with pytest.raises(RecursionRefusal, match="BATCH_REUSE_MISMATCH"):
        engine.run_batch(
            "batch",
            [event("other", 4), event("e2", 5), event("e3", 6)],
        )
    with pytest.raises(RecursionRefusal, match="EVENT_ID_CONFLICT"):
        engine.run_batch("second-batch", [event("e1", 4), event("f2", 5), event("f3", 6)])
    assert owner.effect_count == effects


def test_mutating_submitted_proposal_documents_cannot_change_stored_material(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    documents = [proposal.document() for proposal in three()]
    first = engine.run_batch("batch", documents)

    documents[0]["circumstances"]["later_mutation"] = "not-the-stored-proposal"
    assert engine.run_batch("batch", [proposal.document() for proposal in three()]) == first
    with pytest.raises(RecursionRefusal, match="BATCH_REUSE_MISMATCH"):
        engine.run_batch("batch", documents)


# ---------------------------------------------------------------------------
# Forged owner results


def _wrong_operation(result):
    return replace(result, operation_id="forged-operation")


def _wrong_proposal_hash(result):
    return replace(result, proposal_hash="0" * 64)


def _wrong_before(result):
    return replace(result, before=replace(result.before, clock=result.before.clock + 1))


def _wrong_after_identity(result):
    return replace(result, after=replace(result.after, root="other-root"))


def _backward_after_clock(result):
    return replace(
        result,
        after=replace(result.after, clock=result.before.clock - 1),
    )


def _wrong_status(result):
    return replace(result, status="EVOLVED")


def _missing_receipt(result):
    return replace(result, receipt_ref="")


def _nonfinite_objective(result):
    return replace(result, objective={"x": float("inf")})


def _bad_readset(result):
    return replace(result, readset=None)


def _not_a_realized_event(result):
    return result.document()


@pytest.mark.parametrize(
    "mutator",
    [
        _wrong_operation,
        _wrong_proposal_hash,
        _wrong_before,
        _wrong_after_identity,
        _backward_after_clock,
        _wrong_status,
        _missing_receipt,
        _nonfinite_objective,
        _bad_readset,
        _not_a_realized_event,
    ],
)
def test_forged_or_malformed_owner_results_are_not_recorded(tmp_path, mutator):
    owner = ControlledOwner()
    owner.corrupt_result = mutator
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)

    with pytest.raises(RecursionRefusal):
        engine.run_batch("batch", three())

    assert owner.effect_count == 1
    assert_reserved_without_result(journal)


def test_a_forged_result_can_be_recovered_through_the_same_owner_operation(tmp_path):
    owner = ControlledOwner()
    owner.corrupt_result = _wrong_status
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    proposals = three()

    with pytest.raises(RecursionRefusal, match="STATUS"):
        engine.run_batch("batch", proposals)
    operation = owner.operation_ids[0]

    owner.corrupt_result = None
    result = engine.run_batch("batch", proposals)
    assert len(result["records"]) == 3
    assert result["records"][0]["operation_id"] == operation
    assert owner.order == ["e1", "e2", "e3"]
    assert owner.effect_count == 3


# ---------------------------------------------------------------------------
# Root, branch and clock custody


def test_invalid_root_branch_or_rolling_clock_is_refused_before_new_effects(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "root.sqlite")
    owner.root = "other-root"
    with pytest.raises(RecursionRefusal, match="ROOT_ACTOR_BRANCH"):
        engine.run_batch("root-batch", three())
    assert owner.realize_calls == 0

    branch_owner = ControlledOwner()
    branch_engine = BatchEngine(branch_owner, tmp_path / "branch.sqlite")
    branch_owner.branch = "other-branch"
    with pytest.raises(RecursionRefusal, match="ROOT_ACTOR_BRANCH"):
        branch_engine.run_batch("branch-batch", three())
    assert branch_owner.realize_calls == 0

    clock_owner = ControlledOwner()
    clock_engine = BatchEngine(clock_owner, tmp_path / "clock.sqlite")
    clock_engine.run_batch("first", three())
    effects = clock_owner.effect_count
    clock_owner.clock = 1
    with pytest.raises(RecursionRefusal, match="CLOCK"):
        clock_engine.run_batch("second", three("f", 4))
    assert clock_owner.effect_count == effects


def test_journal_binds_the_actual_owner_identity(tmp_path):
    journal = tmp_path / "journal.sqlite"
    owner = ControlledOwner(root="root-a", actor="actor-a", branch="branch-a")
    engine = BatchEngine(owner, journal)
    proposals = three()
    engine.run_batch("batch", proposals)

    with pytest.raises(RecursionRefusal, match="BINDING"):
        BatchEngine(
            ControlledOwner(root="root-b", actor="actor-a", branch="branch-a"),
            journal,
        )
    with pytest.raises(RecursionRefusal, match="BINDING"):
        BatchEngine(
            ControlledOwner(root="root-a", actor="actor-b", branch="branch-a"),
            journal,
        )

    owner.root = "root-b"
    with pytest.raises(RecursionRefusal, match="ROOT_ACTOR_BRANCH"):
        engine.verify()
    with pytest.raises(RecursionRefusal, match="ROOT_ACTOR_BRANCH"):
        engine.history("batch")
    with pytest.raises(RecursionRefusal, match="ROOT_ACTOR_BRANCH"):
        engine.run_batch("batch", proposals)


def test_between_batch_retrospective_state_is_the_actual_next_start(tmp_path):
    owner = ControlledOwner()
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    first = engine.run_batch("batch", three())

    # The retrospective half may be admitted between batches without moving the
    # owner clock.  The next batch must start from that actual state, not from
    # the previous batch's recorded after-state.
    owner.extra["retrospective_admission"] = True
    changed = owner.snapshot()
    assert changed.clock == first["records"][-1]["after"]["clock"]
    assert changed.state_hash != first["records"][-1]["after"]["state_hash"]

    second = engine.run_batch("next", three("f", 4))
    assert second["records"][0]["before"] == changed.document()
    assert owner.order == ["e1", "e2", "e3", "f1", "f2", "f3"]
    assert engine.history("batch") == first
    assert engine.verify() is True


def test_unknown_batches_and_empty_identifiers_are_explicit(tmp_path):
    owner = ControlledOwner()
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    with pytest.raises(RecursionRefusal, match="UNKNOWN_BATCH"):
        engine.history("missing")
    with pytest.raises(RecursionRefusal, match="BATCH_ID_REQUIRED"):
        engine.run_batch("", three())
    with pytest.raises(RecursionRefusal, match="BATCH_ID_REQUIRED"):
        engine.history("   ")


# ---------------------------------------------------------------------------
# Durable reservation, interruption and ambiguous recovery


def test_interrupted_after_receipt_recovers_the_same_operation_without_duplication(
    tmp_path,
):
    owner = ControlledOwner()
    owner.crash_after_receipt_for.add("e1")
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    proposals = three()

    with pytest.raises(RecursionRefusal, match="OWNER_REALIZE_FAILED"):
        engine.run_batch("batch", proposals)

    first_operation = owner.operation_ids[0]
    assert owner.effect_count == 1
    assert owner.order == ["e1"]
    assert engine.history("batch")["records"] == []

    reopened = BatchEngine(owner, journal)
    result = reopened.run_batch("batch", proposals)

    assert owner.order == ["e1", "e2", "e3"]
    assert owner.effect_count == 3
    assert owner.operation_ids[1] == first_operation
    assert result["records"][0]["operation_id"] == first_operation
    assert len(result["records"]) == 3
    assert reopened.verify() is True


def test_ambiguous_retry_is_held_and_never_silently_reissued(tmp_path):
    owner = ControlledOwner()
    owner.crash_before_receipt_for.add("e1")
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    proposals = three()

    with pytest.raises(RecursionRefusal, match="OWNER_REALIZE_FAILED"):
        engine.run_batch("batch", proposals)
    operation = owner.operation_ids[0]
    assert owner.effect_count == 1
    assert owner.order == ["e1"]
    assert operation in owner.pending

    with pytest.raises(RecursionRefusal, match="AMBIGUOUS"):
        engine.run_batch("batch", proposals)
    assert owner.operation_ids == [operation, operation]
    assert owner.effect_count == 1
    assert owner.order == ["e1"]
    assert_reserved_without_result(journal)

    owner.resolve_pending(operation)
    result = engine.run_batch("batch", proposals)
    assert owner.order == ["e1", "e2", "e3"]
    assert owner.effect_count == 3
    assert len(result["records"]) == 3


def test_interrupted_progress_is_visible_and_resumable_without_replay(tmp_path):
    owner = ControlledOwner()
    owner.crash_after_receipt_for.add("e2")
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    proposals = three()

    with pytest.raises(RecursionRefusal, match="OWNER_REALIZE_FAILED"):
        engine.run_batch("batch", proposals)
    assert owner.order == ["e1", "e2"]
    assert owner.effect_count == 2
    partial = engine.history("batch")
    assert [record["event_id"] for record in partial["records"]] == ["e1"]
    assert engine.verify() is True

    result = BatchEngine(owner, journal).run_batch("batch", proposals)
    assert [record["event_id"] for record in result["records"]] == ["e1", "e2", "e3"]
    assert owner.order == ["e1", "e2", "e3"]
    assert owner.effect_count == 3


def test_interrupted_batch_blocks_a_new_batch_until_recovery(tmp_path):
    owner = ControlledOwner()
    owner.crash_after_receipt_for.add("e1")
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    first = three()
    with pytest.raises(RecursionRefusal, match="OWNER_REALIZE_FAILED"):
        engine.run_batch("first", first)

    with pytest.raises(RecursionRefusal, match="INTERRUPTED_BATCH_REQUIRES_RECOVERY"):
        engine.run_batch("second", three("f", 2))
    assert owner.effect_count == 1

    engine.run_batch("first", first)
    result = engine.run_batch("second", three("f", 4))
    assert [record["event_id"] for record in result["records"]] == ["f1", "f2", "f3"]
    assert owner.order == ["e1", "e2", "e3", "f1", "f2", "f3"]


# ---------------------------------------------------------------------------
# Hash chain, tamper detection and exclusive execution


def test_journal_hash_chain_tamper_fails_history_and_verify(tmp_path):
    owner = ControlledOwner()
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    engine.run_batch("batch", three())

    connection = sqlite3.connect(journal)
    try:
        connection.execute(
            "UPDATE events SET chain_hash=? WHERE batch_id=? AND event_index=1",
            ("0" * 64, "batch"),
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(RecursionRefusal, match="INTEGRITY"):
        engine.history("batch")
    with pytest.raises(RecursionRefusal, match="INTEGRITY"):
        engine.verify()


def test_journal_meta_tamper_and_missing_event_fail_verify(tmp_path):
    owner = ControlledOwner()
    journal = tmp_path / "journal.sqlite"
    engine = BatchEngine(owner, journal)
    engine.run_batch("batch", three())

    connection = sqlite3.connect(journal)
    try:
        connection.execute(
            "UPDATE meta SET value=? WHERE key='root'", ("tampered-root",)
        )
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(RecursionRefusal, match="BINDING"):
        engine.verify()

    second_owner = ControlledOwner()
    second_journal = tmp_path / "second.sqlite"
    second_engine = BatchEngine(second_owner, second_journal)
    second_engine.run_batch("batch", three())
    connection = sqlite3.connect(second_journal)
    try:
        connection.execute(
            "DELETE FROM events WHERE batch_id=? AND event_index=2", ("batch",)
        )
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(RecursionRefusal, match="INTEGRITY"):
        second_engine.verify()


def test_exclusive_concurrent_same_batch_realizes_effects_once(tmp_path):
    owner = ControlledOwner()
    journal = tmp_path / "journal.sqlite"
    first_engine = BatchEngine(owner, journal)
    second_engine = BatchEngine(owner, journal)
    proposals = three()
    barrier = threading.Barrier(2)

    def run(engine):
        barrier.wait(timeout=5)
        return engine.run_batch("batch", proposals)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, engine) for engine in (first_engine, second_engine)]
        results = [future.result(timeout=20) for future in futures]

    assert results[0] == results[1]
    assert owner.order == ["e1", "e2", "e3"]
    assert owner.effect_count == 3
    assert owner.validation_calls == 3


# ---------------------------------------------------------------------------
# Scientific status is preserved; no fixed story is supplied by the engine


def test_held_and_missing_rule_are_preserved_and_never_become_no_change(tmp_path):
    owner = ControlledOwner()
    owner.held = True
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    result = engine.run_batch("batch", three())

    assert [record["status"] for record in result["records"]] == ["HELD"] * 3
    assert all(
        record["consequences"]["durable_psychological_transition"] == "MISSING_RULE"
        for record in result["records"]
    )
    assert all(record["status"] != "NO_CHANGE" for record in result["records"])
    assert engine.history("batch") == result


def test_generic_identifiers_round_trip_and_engine_has_no_fixed_story_tokens(tmp_path):
    owner = ControlledOwner(
        root="root/ζ:9",
        actor="actor-42",
        branch="branch/α",
    )
    engine = BatchEngine(owner, tmp_path / "journal.sqlite")
    proposals = [
        event("event/一", 1, source_refs=("source/α",), participants=("actor-42",)),
        event("event/二", 2, source_refs=("source/β",), participants=("actor-42",)),
        event("event/三", 3, source_refs=("source/γ",), participants=("actor-42",)),
    ]
    result = engine.run_batch("batch/一", proposals)
    assert [record["event_id"] for record in result["records"]] == [
        "event/一",
        "event/二",
        "event/三",
    ]
    assert result["records"][0]["readset"] == ["source/α"]

    source = Path(engine_module.__file__).read_text(encoding="utf-8").casefold()
    for forbidden in ("nadia", "workshop", "can011", "adp011", "questionnaire"):
        assert forbidden not in source
