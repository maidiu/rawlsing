"""T3 pre-registered named assertions and dependency-severance RED witnesses.

Each named assertion is a positive claim about one edge in the candidate chain.
The sibling `<this file>.proof.json` freezes the exact source-code fault that
severs that edge. The same named assertion must FAIL BY ITS OWN ASSERTION under
the fault, never by an import error, fixture crash or unrelated exception.
"""
from __future__ import annotations

from conftest import (
    ACTOR_ID,
    TEST_ONLY_TARGET_ISSUER,
    build_actor_record,
    build_conditioning_sources,
    build_event_witness,
    build_response_rule,
    build_target_rule,
)
from candidate.action_admission import (
    AdmissionStatus,
    admit_performed_action,
    make_performed_action_receipt,
)
from candidate.canon import digest
from candidate.conditioning import ConditioningStatus, bind_conditioning
from candidate.later_action import LaterActionConsumer, LaterActionStatus, read_target_for_later_action
from candidate.response_rules import ResponseRuleRegistry, RuleLookupStatus, lookup_rule
from candidate.target_rules import (
    TargetBranch,
    TargetRuleRegistry,
    evaluate_target,
    make_target_permission,
)
from candidate.transaction import CandidateStore

EVENT_HASH_LABEL = "event-c9p-e1"


def _committed_target(store: CandidateStore, proposal_hash: str = "proposal-sev") -> dict:
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    from candidate.target_rules import TargetDecision, TargetReason
    from candidate.canon import seal as _seal

    decision = TargetDecision(
        branch=TargetBranch.CREATE,
        reason=TargetReason.OK,
        actor_id=ACTOR_ID,
        state_kind_id="V3MS_PRACTICE",
        proposal_hash=proposal_hash,
        record_hash="record-sev",
        before_target_hash=store.target_state_hash(),
        after_target_hash="after",
        readset_refs=("read-1",),
        permission_ref="grant-sev",
    )
    receipt = store.commit(
        event=admitted,
        response=_seal({"event_ref": admitted["hash"], "status": "COMMITTED"}),
        decision=decision,
        readset_refs=("read-1",),
    )
    assert receipt.committed, receipt.target_reason
    return admitted


def test_later_action_consumer_reads_committed_target_state(tmp_path) -> None:
    """Named assertion: the later-action consumer reads the exact committed target state."""
    store = CandidateStore(tmp_path / "store.sqlite")
    _committed_target(store)
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    read = read_target_for_later_action(
        store,
        consumer=consumer,
        middle_state_id="proposal-sev",
        as_of=30,
        commit_time=15,
        action_admission_owner_ref="TEST_ONLY_ACTUATOR",
    )
    assert read.status is LaterActionStatus.READ_OK, read.reason
    assert read.committed_record is not None
    assert read.state_hash == digest(read.committed_record), (
        "consumer read hash must equal the committed record digest"
    )
    assert "proposal-sev" in read.readset_refs
    store.close()


def test_response_lookup_consumes_exact_rule_registry_entry() -> None:
    """Named assertion: the CAN008 lookup consumes the exact registry entry and finds it."""
    rule = build_response_rule()
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    assert lookup.status is RuleLookupStatus.FOUND, lookup.reason
    assert lookup.issuer_verified is True
    assert lookup.rule_id == "TEST_ONLY_H1_PRACTICE_RESPONSE"


def test_target_decision_consumes_independent_permission(tmp_path) -> None:
    """Named assertion: CREATE fires only from an independently authenticated permission."""
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="grant-sev",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-sev",
        response_hash="resp-sev",
        issued_at=10,
    )
    proposal = {
        "schema": "C9P_TARGET_PROPOSAL@1",
        "actor_id": ACTOR_ID,
        "state_kind_id": "V3MS_PRACTICE",
        "operation": "CREATE",
        "proposed_effective_time": 15,
        "semantic_object_ref": "c9p:coordinated_material_inspection",
        "target_refs": ["c9p:practice"],
        "causal_parent_refs": ["event-hash", "h-a", "h-b"],
        "source_update_rule_ref": rule.rule_content_hash,
        "evaluator_receipts": ["src-1"],
        "numeric_rule_ref": None,
        "stochastic_receipt_ref": None,
    }
    from candidate.canon import seal as _seal

    sealed_proposal = _seal(proposal)
    decision = evaluate_target(
        registry=registry,
        proposal=sealed_proposal,
        permission=permission,
        actor_id=ACTOR_ID,
        before_target_hash="before-sev",
        existing_target_ids=frozenset(),
        prior_event_hash="event-hash",
        as_of=20,
        enacted_history_refs=("h-a", "h-b"),
        permitted_issuer_refs=frozenset({TEST_ONLY_TARGET_ISSUER}),
    )
    assert decision.branch is TargetBranch.CREATE, decision.reason.value
    assert decision.record_hash
    assert decision.permission_ref == "grant-sev"


def test_conditioning_readset_binds_person_world_sources() -> None:
    """Named assertion: the conditioning readset binds each person/world source."""
    sources = build_conditioning_sources()
    view = bind_conditioning(subject=ACTOR_ID, sources=sources, as_of=20)
    assert view.status is ConditioningStatus.BOUND, view.reason.value
    expected_refs = tuple(source["source_ref"] for source in sources)
    assert view.readset_refs == expected_refs, (
        "every conditioning source must appear in the bound readset"
    )
    assert "TEST_ONLY_PERSON_STATE:standing" in view.readset_refs


def test_action_admission_binds_performed_action_receipt() -> None:
    """Named assertion: performed-action admission consumes the exact owner receipt."""
    receipt = make_performed_action_receipt(
        actor_id=ACTOR_ID,
        act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
        action_time=30,
        consumed_state_hash="state-hash",
    )
    result = admit_performed_action(
        owner_receipt=receipt,
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.ADMITTED, result.reason.value
    assert result.receipt_hash == receipt["hash"]
    assert result.actuator_ref == "TEST_ONLY_ACTUATOR"


def test_transaction_readset_binds_admitted_event_witness(tmp_path) -> None:
    """Named assertion: the committed receipt binds the exact admitted event witness."""
    store = CandidateStore(tmp_path / "store.sqlite")
    event = build_event_witness()
    admitted = store.admit_occurrence(event)
    from candidate.canon import seal as _seal
    from candidate.target_rules import TargetDecision, TargetReason

    decision = TargetDecision(
        branch=TargetBranch.DENY,
        reason=TargetReason.NO_PROPOSAL,
        actor_id=ACTOR_ID,
        state_kind_id="V3MS_PRACTICE",
        proposal_hash="proposal-sev",
        record_hash="",
        before_target_hash="",
        after_target_hash="",
        readset_refs=("read-1",),
        permission_ref="",
    )
    receipt = store.commit(
        event=admitted,
        response=_seal({"event_ref": admitted["hash"], "status": "COMMITTED"}),
        decision=decision,
        readset_refs=("read-1", admitted["hash"]),
    )
    assert receipt.committed, receipt.target_reason
    assert receipt.admitted_event_ref == admitted["hash"]
    assert admitted["hash"] in receipt.readset_refs
    assert receipt.joint_transaction_id == receipt.receipt_hash, (
        "the joint transaction id must equal the sealed receipt hash"
    )
    store.close()
