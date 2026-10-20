"""(g) Later-action consumer committed-target READ and typed missing-consumer tests."""
from __future__ import annotations

from conftest import ACTOR_ID
from candidate.canon import digest, seal
from candidate.later_action import (
    LaterActionConsumer,
    LaterActionStatus,
    read_target_for_later_action,
)
from candidate.target_rules import TargetBranch, TargetDecision, TargetReason
from candidate.transaction import CandidateStore


def _commit_target(store: CandidateStore, event, proposal_hash: str = "proposal-1") -> None:
    from candidate.canon import seal

    admitted = store.admit_occurrence(event)
    decision = TargetDecision(
        branch=TargetBranch.CREATE,
        reason=TargetReason.OK,
        actor_id=ACTOR_ID,
        state_kind_id="V3MS_PRACTICE",
        proposal_hash=proposal_hash,
        record_hash="record-1",
        before_target_hash=store.target_state_hash(),
        after_target_hash="after",
        readset_refs=("read-1",),
        permission_ref="grant-1",
    )
    receipt = store.commit(
        event=admitted,
        response=seal({"event_ref": admitted["hash"], "status": "COMMITTED"}),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert receipt.committed, receipt.target_reason


def test_missing_consumer_is_typed_refusal(tmp_path) -> None:
    from conftest import build_event_witness

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    _commit_target(store, event)
    read = read_target_for_later_action(
        store,
        consumer=None,
        middle_state_id="proposal-1",
        as_of=30,
        commit_time=event["time"],
    )
    assert read.status is LaterActionStatus.MISSING_CONSUMER
    assert read.reason == "NO_REGISTERED_LATER_ACTION_CONSUMER"
    assert read.committed_record is None
    store.close()


def test_consumer_reads_exact_committed_state(tmp_path) -> None:
    from conftest import build_event_witness

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    _commit_target(store, event)
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="proposal-1",
        as_of=30,
        commit_time=event["time"],
    )
    assert read.status is LaterActionStatus.ACTION_ADMISSION_HELD
    assert read.reason == "PERFORMED_ACTION_OWNER_UNPROVED"
    assert read.committed_record is not None
    assert read.state_hash == digest(read.committed_record)
    assert "proposal-1" in read.readset_refs
    assert read.read_receipt_hash
    store.close()


def test_consumer_read_with_owner_admission_is_read_ok(tmp_path) -> None:
    from conftest import build_event_witness

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    _commit_target(store, event)
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="proposal-1",
        as_of=30,
        commit_time=event["time"],
        action_admission_owner_ref="TEST_ONLY_ACTUATOR",
    )
    assert read.status is LaterActionStatus.READ_OK
    assert read.candidate_route == "PRACTICE_MEDIATED_ACTION_ROUTE"
    store.close()


def test_absent_target_state_is_typed_state_absent(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="never-committed",
        as_of=30,
        commit_time=15,
    )
    assert read.status is LaterActionStatus.STATE_ABSENT
    assert read.reason == "COMMITTED_TARGET_STATE_ABSENT"
    store.close()


def test_as_of_before_commit_is_refused(tmp_path) -> None:
    from conftest import build_event_witness

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    _commit_target(store, event)
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="proposal-1",
        as_of=10,
        commit_time=event["time"],
    )
    assert read.status is LaterActionStatus.AS_OF_BEFORE_COMMIT
    store.close()


def test_consumer_readset_mismatch_is_typed(tmp_path) -> None:
    from conftest import build_event_witness

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    _commit_target(store, event)

    class DivergingConsumer(LaterActionConsumer):
        def read_target(self, store_arg, middle_state_id, as_of):
            record = store_arg.read_target_state(middle_state_id)
            return record, "DIVERGED_HASH"

    consumer = DivergingConsumer(
        consumer_id="TEST_ONLY_DIVERGING_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="proposal-1",
        as_of=30,
        commit_time=event["time"],
    )
    assert read.status is LaterActionStatus.CONSUMER_READSET_MISMATCH
    assert read.reason == "CONSUMER_READ_DIVERGES_FROM_COMMITTED_STATE"
    store.close()
