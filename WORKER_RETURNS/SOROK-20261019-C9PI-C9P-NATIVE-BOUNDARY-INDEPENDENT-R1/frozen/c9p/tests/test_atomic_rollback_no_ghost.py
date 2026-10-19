"""(f) Atomic occurrence/effect commit, no-ghost rollback and readset binding tests."""
from __future__ import annotations

from conftest import ACTOR_ID, build_event_witness
from candidate.target_rules import TargetBranch, TargetDecision, TargetReason
from candidate.transaction import CandidateStore, TransactionRefusal


def _decision(branch: TargetBranch, reason: TargetReason, record_hash: str = "") -> TargetDecision:
    return TargetDecision(
        branch=branch,
        reason=reason,
        actor_id=ACTOR_ID,
        state_kind_id="V3MS_PRACTICE",
        proposal_hash="proposal-1",
        record_hash=record_hash,
        before_target_hash="",
        after_target_hash="",
        readset_refs=("read-1",),
        permission_ref="grant-1",
    )


def _response(event_hash: str) -> dict:
    from candidate.canon import seal

    return seal(
        {
            "event_ref": event_hash,
            "status": "RESPONSE_COMMITTED",
            "rule_status": "FOUND",
        }
    )


def test_committed_transaction_binds_readset_and_event(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    decision = _decision(TargetBranch.DENY, TargetReason.NO_PROPOSAL)
    receipt = store.commit(
        event=admitted,
        response=_response(admitted["hash"]),
        decision=decision,
        readset_refs=("read-1", "read-2"),
    )
    assert receipt.committed
    assert receipt.readset_refs == ("read-1", "read-2")
    assert receipt.admitted_event_ref == admitted["hash"]
    store.close()


def test_denied_decision_leaves_no_target_rows(tmp_path) -> None:
    from candidate.canon import digest

    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    decision = _decision(TargetBranch.DENY, TargetReason.PERMISSION_MISSING)
    store.commit(
        event=admitted,
        response=_response(admitted["hash"]),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert store.committed_target_ids() == frozenset()
    assert store.target_state_hash() == digest([])
    store.close()


def test_injected_fault_rolls_back_with_no_ghost(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    before = store.snapshot()
    decision = _decision(TargetBranch.DENY, TargetReason.NO_PROPOSAL)
    receipt = store.commit(
        event=admitted,
        response=_response(admitted["hash"]),
        decision=decision,
        readset_refs=("read-1",),
        fault="after_receipt_before_commit",
    )
    assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert receipt.no_mutation is True
    assert store.snapshot() == before
    store.close()


def test_unadmitted_event_is_refused_with_rollback(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    decision = _decision(TargetBranch.DENY, TargetReason.NO_PROPOSAL)
    receipt = store.commit(
        event=event,
        response=_response(event["hash"]),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert "EVENT_NOT_ADMITTED" in receipt.target_reason
    store.close()


def test_response_event_mismatch_is_refused(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    decision = _decision(TargetBranch.DENY, TargetReason.NO_PROPOSAL)
    receipt = store.commit(
        event=admitted,
        response=_response("other-event-hash"),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert "RESPONSE_EVENT_MISMATCH" in receipt.target_reason
    store.close()


def test_create_decision_requires_matching_prestate(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    decision = TargetDecision(
        branch=TargetBranch.CREATE,
        reason=TargetReason.OK,
        actor_id=ACTOR_ID,
        state_kind_id="V3MS_PRACTICE",
        proposal_hash="proposal-1",
        record_hash="record-1",
        before_target_hash="WRONG",
        after_target_hash="after",
        readset_refs=("read-1",),
        permission_ref="grant-1",
    )
    receipt = store.commit(
        event=admitted,
        response=_response(admitted["hash"]),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert "STALE_TARGET_PRESTATE" in receipt.target_reason
    store.close()


def test_occurrence_survives_response_rollback(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    decision = _decision(TargetBranch.DENY, TargetReason.NO_PROPOSAL)
    first = store.commit(
        event=admitted,
        response=_response("mismatch"),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert first.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert admitted["hash"] in store.committed_event_hashes()
    store.close()
