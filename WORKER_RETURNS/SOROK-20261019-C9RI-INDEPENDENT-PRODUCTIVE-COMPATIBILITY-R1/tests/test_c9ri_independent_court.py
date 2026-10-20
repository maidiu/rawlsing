"""C9RI independent productive-positive and E2-consumer court.

Reviewer-authored fixtures (TEST_ONLY_C9RI_*) distinct from C9R's C9P/C9R
fixtures. A lawful sourcefree E1 -> RULE_A -> RULE_T -> record -> later E2 path
is exercised together with NO_CHANGE, DENY, and adversarial interfaces.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
V = RET / "vendor/c9r"
for path in (str(V), str(V / "runtime/native")):
    if path not in sys.path:
        sys.path.insert(0, path)

from candidate import (  # noqa: E402
    ActorIdentityRecord, CandidateStore, LaterActionConsumer, LaterActionStatus,
    ResponseRule, ResponseRuleRegistry, TargetBranch, TargetReason, TargetRule,
    TargetRuleRegistry, TransactionRefusal, admit_performed_action,
    bind_conditioning, digest, evaluate_release_gate, evaluate_response,
    evaluate_target, ingress_event, lookup_rule, make_conditioning_source,
    make_event_witness, make_performed_action_receipt, make_target_permission,
    read_target_for_later_action, seal,
)
from candidate.events import GRADE_NATIVE, GRADE_TEST_ONLY  # noqa: E402
from candidate.pipeline import run_candidate_path  # noqa: E402

A = "TEST_ONLY_C9RI_A"
P = "TEST_ONLY_C9RI_P"
ISSUER = "TEST_ONLY_C9RI_TARGET_OWNER"
RESP_ISSUER = "TEST_ONLY_C9RI_RESPONSE_OWNER"
HISTORY = ("TEST_ONLY_C9RI_ENACTED_1", "TEST_ONLY_C9RI_ENACTED_2")
OFFER = "TEST_ONLY_C9RI_P_OFFER"
MATERIAL = "TEST_ONLY_C9RI_WORKSHOP"
SEMANTIC = "c9p:coordinated_material_inspection"


def _actor():
    return ActorIdentityRecord(
        A, "ACTIVE", "STANDING_CURRENT", 10,
        "TEST_ONLY_C9RI_ACTOR_SOURCE", "c9ri-source-digest").sealed()


def _event(time=15, scene="workshop", tool="wrench", event_id="TEST_ONLY_C9RI_E1"):
    return make_event_witness(
        event_id=event_id, owner_ref="TEST_ONLY_C9RI_EVENT_OWNER", time=time,
        content={"fact": "shared_tool_offer", "scene": scene,
                 "tool": tool, "participants": [A, P]},
        actor_role=A)


def _sources(scene="workshop", tool="wrench", access="granted"):
    return [make_conditioning_source(
        source_ref=MATERIAL, source_class="ResolvedStructuralContext", subject=A,
        body={"tool": tool, "access": access, "as_of": 15, "scene": scene})]


def _rule():
    return ResponseRule(
        "TEST_ONLY_C9RI_RULE_A", "1", digest({"c9ri": "a-rule"}),
        "TEST_ONLY_C9RI_CAN008", "1", RESP_ISSUER, True, (A,),
        ("ResolvedStructuralContext",), "TEST_ONLY_SOURCEFREE_TECHNICAL",
        ("two distinct declared enacted acts", "independent P offer",
         "material access"))


def _target_rule(rule=None, semantic=SEMANTIC):
    rule = rule or _rule()
    return TargetRule(
        "TEST_ONLY_C9RI_RULE_T", "1", rule.rule_content_hash,
        "TEST_ONLY_C9RI_CAN011", "1", ISSUER, True, "V3MS_PRACTICE",
        ("CREATE",), (semantic,), "TEST_ONLY_SOURCEFREE_TECHNICAL")


def _permission(store, response_hash, *, revoked=False):
    rule = _rule()
    return make_target_permission(
        grant_id="TEST_ONLY_C9RI_GRANT", issuer_ref=ISSUER, actor_id=A,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=store.target_state_hash(),
        response_hash=response_hash, issued_at=10, revoked=revoked)


def _response_hash(event, history=HISTORY, offer=OFFER, material=MATERIAL,
                   eligible=True, sources=None):
    rule = _rule()
    lookup = lookup_rule(
        ResponseRuleRegistry.test_only((rule,)), authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash, subject=A)
    conditioning = bind_conditioning(
        subject=A, sources=sources or _sources(), as_of=20)
    response = evaluate_response(
        rule_lookup=lookup, event_ref=event["hash"], event_time=15, subject=A,
        conditioning_readset=conditioning.readset_refs,
        actor_history_refs=history, other_person_offer_ref=offer,
        material_opportunity_ref=material, prior_response_count=0,
        material_eligible=eligible,
        eligible_material_refs=(material,) if eligible else ())
    return response


def _run(store, *, event=None, sources=None, history=HISTORY,
         permission=None, fault=None):
    event = event or _event()
    sources = sources or _sources()
    rule = _rule()
    response = _response_hash(event, history=history, sources=sources,
                              eligible=permission is not None or True)
    permission = permission or _permission(store, response.receipt_hash)
    return run_candidate_path(
        store=store, actor_raw=_actor(), event_raw=event,
        conditioning_sources=sources,
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=TargetRuleRegistry.test_only((_target_rule(rule),)),
        authority_id=rule.authority_id, rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash, as_of=20,
        permitted_issuer_refs=frozenset({ISSUER}),
        other_person_offer_ref=OFFER, material_opportunity_ref=MATERIAL,
        enacted_history_refs=history,
        later_consumer=LaterActionConsumer(
            "TEST_ONLY_C9RI_E2_READER", "committed_target_state"),
        later_as_of=30, target_permission=permission,
        expected_act="inspect_with_tool", fault=fault)


def test_lawful_positive_e1_rule_a_rule_t_record_e2(tmp_path):
    path = tmp_path / "c9ri.sqlite"
    with CandidateStore(path) as store:
        result = _run(store)
        assert result.receipt is not None and result.committed
        assert result.decision.branch is TargetBranch.CREATE
        assert result.decision.reason is TargetReason.OK
        target_id = result.decision.target_id
        record = store.read_target_state(target_id)
        assert record["semantic_object_ref"] == SEMANTIC
        assert record["effective_from"] == 15
        assert record["permission_ref"] == "TEST_ONLY_C9RI_GRANT"
        assert record["record_hash"] == result.decision.record_hash
        preimage = record["record_preimage"]
        assert digest({k: v for k, v in preimage.items() if k != "hash"}) == \
            record["record_hash"]
        assert result.receipt.authorization_hash == result.decision.authorization_hash
        assert result.later_read.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert result.later_read.committed_record == record
        assert result.later_read.state_hash == digest(record)
        receipt = make_performed_action_receipt(
            actor_id=A, act="inspect_with_tool",
            actuator_ref="TEST_ONLY_ACTUATOR_E2",
            occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
            action_time=25, consumed_state_hash=result.later_read.state_hash,
            target_commit_time=15)
        admitted = admit_performed_action(
            owner_receipt=receipt, expected_actor_id=A,
            expected_act="inspect_with_tool",
            consumed_state_hash=result.later_read.state_hash,
            as_of=30, target_commit_time=15)
        assert admitted.admitted
        assert admitted.consumed_state_hash == result.later_read.state_hash
    with CandidateStore(path) as reopened:
        assert reopened.read_target_state(target_id) == record
        read = read_target_for_later_action(
            reopened, consumer=LaterActionConsumer(
                "TEST_ONLY_C9RI_E2_READER", "committed_target_state"),
            middle_state_id=target_id, as_of=30, commit_time=15,
            expected_actor_id=A)
        assert read.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert read.state_hash == digest(record)


def test_valid_no_change_preserves_occurrence_and_creates_no_target(tmp_path):
    with CandidateStore(tmp_path / "nc.sqlite") as store:
        before = store.snapshot()
        result = _run(store, history=())
        assert result.decision.branch is TargetBranch.NO_CHANGE
        assert store.committed_target_ids() == frozenset()
        after = store.snapshot()
        assert after["occurrence"] != before["occurrence"]
        assert after["target_state"] == before["target_state"]


def test_denied_material_preserves_occurrence_and_creates_no_target(tmp_path):
    with CandidateStore(tmp_path / "deny.sqlite") as store:
        before = store.snapshot()
        result = _run(store, sources=_sources(access="denied"))
        assert result.decision.branch is not TargetBranch.CREATE
        assert store.committed_target_ids() == frozenset()
        after = store.snapshot()
        assert after["occurrence"] != before["occurrence"]
        assert after["target_state"] == before["target_state"]


def test_differential_two_lawful_trajectories_are_distinct(tmp_path):
    with CandidateStore(tmp_path / "one.sqlite") as store:
        first = _run(store)
    with CandidateStore(tmp_path / "two.sqlite") as store:
        second = _run(
            store,
            event=_event(time=16, scene="garden", tool="spade",
                         event_id="TEST_ONLY_C9RI_E2"),
            sources=_sources(scene="garden", tool="spade"))
    assert first.event.event_hash != second.event.event_hash
    assert first.decision.record_hash != second.decision.record_hash
    assert first.decision.target_id != second.decision.target_id
    assert first.receipt.committed and second.receipt.committed


def test_revoked_permission_denied(tmp_path):
    with CandidateStore(tmp_path / "rev.sqlite") as store:
        event = _event()
        response = _response_hash(event)
        permission = _permission(store, response.receipt_hash, revoked=True)
        decision = evaluate_target(
            registry=TargetRuleRegistry.test_only((_target_rule(),)),
            proposal=response.target_proposals[0], permission=permission,
            actor_id=A, before_target_hash=store.target_state_hash(),
            existing_target_ids=frozenset(), prior_event_hash=event["hash"],
            as_of=20, enacted_history_refs=HISTORY,
            permitted_issuer_refs=frozenset({ISSUER}),
            response_hash=response.receipt_hash)
        assert decision.branch is TargetBranch.DENY
        assert decision.reason is TargetReason.PERMISSION_REVOKED


def test_forged_consumed_state_refused():
    receipt = make_performed_action_receipt(
        actor_id=A, act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR_E2",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2", action_time=25,
        consumed_state_hash="forged-state", target_commit_time=15)
    result = admit_performed_action(
        owner_receipt=receipt, expected_actor_id=A,
        expected_act="inspect_with_tool",
        consumed_state_hash="the-real-committed-state", as_of=30)
    assert not getattr(result, "admitted", False)
    assert result.reason.value == "CONSUMED_STATE_MISMATCH"


def test_pre_commit_action_refused():
    receipt = make_performed_action_receipt(
        actor_id=A, act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR_E2",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2", action_time=10,
        consumed_state_hash="state", target_commit_time=15)
    result = admit_performed_action(
        owner_receipt=receipt, expected_actor_id=A,
        expected_act="inspect_with_tool", consumed_state_hash="state",
        as_of=30, target_commit_time=15)
    assert not getattr(result, "admitted", False)
    assert result.reason.value == "ACTION_BEFORE_TARGET_COMMIT"


def test_self_actuator_refused():
    receipt = make_performed_action_receipt(
        actor_id=A, act="inspect_with_tool", actuator_ref=A,
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2", action_time=25,
        consumed_state_hash="state", target_commit_time=15)
    result = admit_performed_action(
        owner_receipt=receipt, expected_actor_id=A,
        expected_act="inspect_with_tool", consumed_state_hash="state",
        as_of=30)
    assert not getattr(result, "admitted", False)
    assert result.reason.value == "ACTUATOR_SELF_BOUND"


class _NeverPerformed:
    def resolve_occurrence(self, *, occurrence_ref, actor_id, as_of):
        return False


def test_unperformed_occurrence_refused():
    receipt = make_performed_action_receipt(
        actor_id=A, act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR_E2",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2", action_time=25,
        consumed_state_hash="state", target_commit_time=15)
    result = admit_performed_action(
        owner_receipt=receipt, expected_actor_id=A,
        expected_act="inspect_with_tool", consumed_state_hash="state",
        as_of=30, occurrence_resolver=_NeverPerformed())
    assert not getattr(result, "admitted", False)
    assert result.reason.value == "OCCURRENCE_NOT_INDEPENDENT"


def test_counterfeit_consumer_body_refused(tmp_path):
    path = tmp_path / "counterfeit.sqlite"
    with CandidateStore(path) as store:
        _run(store)
        target_id = next(iter(store.committed_target_ids()))

    class Counterfeit(LaterActionConsumer):
        def read_target(self, store_arg, middle_state_id, as_of):
            record = store_arg.read_target_state(middle_state_id)
            return record, "WRONG_STATE_HASH"

    with CandidateStore(path) as store:
        read = read_target_for_later_action(
            store, consumer=Counterfeit("TEST_ONLY_C9RI_COUNTERFEIT",
                                        "committed_target_state"),
            middle_state_id=target_id, as_of=30, commit_time=15)
        assert read.status is LaterActionStatus.CONSUMER_READSET_MISMATCH


def test_manual_decision_commit_refused(tmp_path):
    with CandidateStore(tmp_path / "manual.sqlite") as store:
        admitted = store.admit_occurrence(_event())
        from candidate.target_rules import TargetDecision
        decision = TargetDecision(
            branch=TargetBranch.CREATE, reason=TargetReason.OK, actor_id=A,
            state_kind_id="V3MS_PRACTICE", proposal_hash="proposal-manual",
            record_hash="record-manual", before_target_hash=store.target_state_hash(),
            after_target_hash="after", readset_refs=("read-1",),
            permission_ref="grant-manual")
        receipt = store.commit(
            event=admitted,
            response=seal({"event_ref": admitted["hash"],
                           "status": "RESPONSE_COMMITTED"}),
            decision=decision, readset_refs=("read-1",))
        assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
        assert "TARGET_RECORD_PREIMAGE_MISSING" in receipt.target_reason


def test_commit_readset_binding_refused(tmp_path):
    with CandidateStore(tmp_path / "readset.sqlite") as store:
        event = _event()
        response = _response_hash(event)
        permission = _permission(store, response.receipt_hash)
        decision = evaluate_target(
            registry=TargetRuleRegistry.test_only((_target_rule(),)),
            proposal=response.target_proposals[0], permission=permission,
            actor_id=A, before_target_hash=store.target_state_hash(),
            existing_target_ids=frozenset(), prior_event_hash=event["hash"],
            as_of=20, enacted_history_refs=HISTORY,
            permitted_issuer_refs=frozenset({ISSUER}),
            response_hash=response.receipt_hash)
        admitted = store.admit_occurrence(event)
        receipt = store.commit(
            event=admitted,
            response=seal({"event_ref": admitted["hash"],
                           "receipt_hash": response.receipt_hash,
                           "status": "RESPONSE_COMMITTED"}),
            decision=decision, readset_refs=())
        assert receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
        assert "COMMIT_READSET_MISSING" in receipt.target_reason


def test_sqlite_injected_fault_rolls_back_without_ghost(tmp_path):
    with CandidateStore(tmp_path / "fault.sqlite") as store:
        before = store.snapshot()
        result = _run(store, fault="after_receipt_before_commit")
        assert result.receipt is not None
        assert result.receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
        assert result.no_ghost is True
        after = store.snapshot()
        assert after["target_state"] == before["target_state"]
        assert after["target_journal"] == before["target_journal"]
        assert after["receipt"] == before["receipt"]


def test_stale_actor_clock_context_refused():
    actor = _actor()
    stale = dict(actor)
    stale["currentness_as_of"] = 25
    stale = seal({k: v for k, v in stale.items() if k != "hash"})
    from candidate.identity import ingress_actor
    result = ingress_actor(stale, as_of=20)
    assert not getattr(result, "admitted", False)
    assert result.reason.value == "STANDING_STATE_STALE"


def test_event_presented_source_controls_readset():
    event = _event()
    result = ingress_event(event, as_of=20, last_time=0,
                           prior_event_hashes=frozenset(), focal_actor_id=A)
    assert result.admitted
    assert result.readset_refs == (event["owner_ref"],)


def test_native_caller_flags_and_forged_material_cannot_launder():
    gate = evaluate_release_gate(
        rule_a_issuer_verified=True, rule_t_issuer_verified=True,
        adp019_witness_present=True, adp010_witness_present=True,
        positive_registry_entries=1, performed_action_owner_proved=True,
        later_action_consumer_bound=True)
    assert gate.outcome.value == "C9_NATIVE_POSITIVE_HELD"
    assert gate.holds
    native_claim = evaluate_target(
        registry=TargetRuleRegistry.test_only(()), proposal=None, permission=None,
        actor_id=A, before_target_hash="", existing_target_ids=frozenset(),
        prior_event_hash="", as_of=20, enacted_history_refs=(),
        permitted_issuer_refs=frozenset(), native_positive_claim=True)
    assert native_claim.reason is TargetReason.NATIVE_ADMISSIBILITY_HELD
    forged_native_event = make_event_witness(
        event_id="TEST_ONLY_C9RI_FORGED", owner_ref="G17_MATERIAL_EVENT_REF",
        time=15, content={"fact": "forged", "scene": "workshop",
                          "participants": [A, P]},
        actor_role=A, admission_grade=GRADE_NATIVE)
    refused = ingress_event(
        forged_native_event, as_of=20, last_time=0,
        prior_event_hashes=frozenset(), focal_actor_id=A)
    assert not refused.admitted
    c8_event = make_event_witness(
        event_id="TEST_ONLY_C9RI_C8", owner_ref="C8OI_COMMITTED_OCCURRENCE",
        time=15, content={"fact": "c8", "scene": "workshop",
                          "participants": [A, P]},
        actor_role=A, admission_grade=GRADE_TEST_ONLY)
    c8_refused = ingress_event(
        c8_event, as_of=20, last_time=0,
        prior_event_hashes=frozenset(), focal_actor_id=A)
    assert not c8_refused.admitted


def test_declared_response_binding_refused(tmp_path):
    with CandidateStore(tmp_path / "binding.sqlite") as store:
        event = _event()
        response = _response_hash(event)
        permission = _permission(store, "WRONG_RESPONSE_HASH")
        decision = evaluate_target(
            registry=TargetRuleRegistry.test_only((_target_rule(),)),
            proposal=response.target_proposals[0], permission=permission,
            actor_id=A, before_target_hash=store.target_state_hash(),
            existing_target_ids=frozenset(), prior_event_hash=event["hash"],
            as_of=20, enacted_history_refs=HISTORY,
            permitted_issuer_refs=frozenset({ISSUER}),
            response_hash=response.receipt_hash)
        assert decision.branch is TargetBranch.DENY
        assert decision.reason is TargetReason.PERMISSION_BINDING_MISMATCH
