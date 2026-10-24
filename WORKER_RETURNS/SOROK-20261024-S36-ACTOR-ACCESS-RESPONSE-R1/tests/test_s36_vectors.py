"""S36 six-vector TEST_ONLY execution against the existing C9R pipeline."""
from __future__ import annotations

from candidate import (
    CandidateStore,
    LaterActionConsumer,
    LaterActionStatus,
    ResponseStatus,
    TargetBranch,
    TargetReason,
    valid,
)
from candidate.actor_access_response import (
    AMBIGUOUS_CONTRADICTORY,
    OBSERVED_CURRENT_REFUSAL,
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    RECEIVABLE_NO_OBSERVED_UPTAKE,
    UNKNOWN_RECEIVABILITY,
)
from s36_harness import (
    B,
    LEGACY_HISTORY,
    committed_response,
    run_s35_case,
)


def _assert_no_target(result, store):
    assert result.response.target_proposals == ()
    assert len(result.response.target_proposals) == 0
    assert result.decision.branch is TargetBranch.NO_CHANGE
    assert result.decision.reason is TargetReason.NO_PROPOSAL
    assert result.decision.target_id == ""
    assert result.decision.record_hash == ""
    assert result.receipt.committed
    assert result.receipt.target_branch == "NO_CHANGE"
    assert result.receipt.target_reason == "NO_PROPOSAL"
    assert result.receipt.record_hash == ""
    assert store.committed_target_ids() == frozenset()


def test_p1_observed_immediate_positive_zero_proposals(tmp_path):
    with CandidateStore(tmp_path / "p1.sqlite") as store:
        result, event = run_s35_case(store)
        assert result.actor.admitted
        assert result.event.admitted
        assert result.material_eligible is True
        assert result.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert result.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert result.response.uptake_refs == ("TEST_ONLY_S36_A_REQUEST_TOOL",)
        assert result.response.recruited_refs[0].startswith("TEST_ONLY_ADP017_ACCESS")
        assert result.response.declared_history_refs == ()
        assert result.response.declared_offer_ref == ""
        _assert_no_target(result, store)
        assert event["hash"] in store.committed_event_hashes()
        body = committed_response(store, result.receipt.response_ref)
        assert body is not None
        assert body["status"] == "RESPONSE_COMMITTED"
        assert body["target_proposal_ref"] == ""
        receipt = body["s35_receipt"]
        assert valid(receipt)
        assert receipt["target_proposals"] == []
        assert receipt["outcome"] == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert receipt["observed_response_ref"] == "TEST_ONLY_S36_A_REQUEST_TOOL"
        assert receipt["objective_material_eligible"] is True
        assert receipt["objective_material_implies_uptake"] is False
        assert receipt["belief_update"] is None
        assert receipt["emotion_update"] is None
        assert receipt["durable_update"] is None
        assert receipt["claim_ceiling"] == (
            "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A"
        )


def test_n1_objective_material_without_actor_access_is_unknown(tmp_path):
    with CandidateStore(tmp_path / "n1.sqlite") as store:
        result, _ = run_s35_case(store, access=None)
        assert result.material_eligible is True
        assert result.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert result.response.reason == UNKNOWN_RECEIVABILITY
        assert result.response.uptake_refs == ()
        _assert_no_target(result, store)
        body = committed_response(store, result.receipt.response_ref)
        assert body is not None
        receipt = body["s35_receipt"]
        assert receipt["outcome"] == UNKNOWN_RECEIVABILITY
        assert receipt["target_proposals"] == []
        assert receipt["objective_material_eligible"] is True
        assert receipt["objective_material_implies_uptake"] is False
        assert receipt["access_source_ref"] == ""


def test_n1_typed_not_witnessed_access_is_unknown(tmp_path):
    with CandidateStore(tmp_path / "n1b.sqlite") as store:
        result, _ = run_s35_case(
            store,
            access_kwargs={"access_status": "NOT_WITNESSED"},
            response=None,
        )
        assert result.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert result.response.reason == UNKNOWN_RECEIVABILITY
        _assert_no_target(result, store)


def test_n2_contradictory_context_no_response_is_ambiguous(tmp_path):
    with CandidateStore(tmp_path / "n2.sqlite") as store:
        result, _ = run_s35_case(
            store,
            response=None,
            contradictory_context=True,
            contradictory_refs=("TEST_ONLY_S36_CONTRARY_PROJECT",),
        )
        assert result.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert result.response.reason == AMBIGUOUS_CONTRADICTORY
        assert "TEST_ONLY_S36_CONTRARY_PROJECT" in result.response.readset_refs
        _assert_no_target(result, store)
        body = committed_response(store, result.receipt.response_ref)
        receipt = body["s35_receipt"]
        assert receipt["outcome"] == AMBIGUOUS_CONTRADICTORY
        assert receipt["contradictory_context"] is True
        assert receipt["contradictory_refs"] == ["TEST_ONLY_S36_CONTRARY_PROJECT"]
        assert receipt["target_proposals"] == []


def test_n2_contradictory_context_with_observed_response_preserves_both(tmp_path):
    with CandidateStore(tmp_path / "n2b.sqlite") as store:
        result, _ = run_s35_case(
            store,
            contradictory_context=True,
            contradictory_refs=("TEST_ONLY_S36_CONTRARY_PROJECT",),
        )
        assert result.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert result.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert "TEST_ONLY_S36_CONTRARY_PROJECT" in result.response.readset_refs
        _assert_no_target(result, store)
        body = committed_response(store, result.receipt.response_ref)
        receipt = body["s35_receipt"]
        assert receipt["contradictory_refs"] == ["TEST_ONLY_S36_CONTRARY_PROJECT"]
        assert receipt["target_proposals"] == []


def test_n3_same_public_surface_from_different_b_causes(tmp_path):
    with CandidateStore(tmp_path / "n3_share.sqlite") as store:
        share, _ = run_s35_case(
            store,
            event_id="TEST_ONLY_S36_N3_SHARE",
            b_act="SHARE_TOOL",
            response_kwargs={
                "response_ref": "TEST_ONLY_S36_A_EXPLICIT_REFUSAL",
                "response_kind": "EXPLICIT_REFUSAL",
                "content": {
                    "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                    "actor_knows_b_motive": False,
                },
            },
        )
    with CandidateStore(tmp_path / "n3_refuse.sqlite") as store:
        refuse, _ = run_s35_case(
            store,
            event_id="TEST_ONLY_S36_N3_REFUSE",
            b_act="REFUSE_TOOL",
            response_kwargs={
                "response_ref": "TEST_ONLY_S36_A_EXPLICIT_REFUSAL",
                "response_kind": "EXPLICIT_REFUSAL",
                "content": {
                    "public_surface": "HELP_REFUSE_DUE_TO_CURRENT_TOOL_SHORTAGE",
                    "actor_knows_b_motive": False,
                },
            },
        )
    assert share.response.reason == OBSERVED_CURRENT_REFUSAL
    assert refuse.response.reason == OBSERVED_CURRENT_REFUSAL
    assert share.response.reason == refuse.response.reason
    assert share.response.uptake_refs == refuse.response.uptake_refs
    assert share.response.uptake_refs == ("TEST_ONLY_S36_A_EXPLICIT_REFUSAL",)
    assert share.decision.branch is TargetBranch.NO_CHANGE
    assert refuse.decision.branch is TargetBranch.NO_CHANGE
    assert share.decision.reason is TargetReason.NO_PROPOSAL
    assert refuse.decision.reason is TargetReason.NO_PROPOSAL
    assert B not in share.response.readset_refs
    assert B not in refuse.response.readset_refs
    assert share.response.target_proposals == ()
    assert refuse.response.target_proposals == ()


def test_n4_label_only_perturbation_is_invariant(tmp_path):
    labels = {
        "class_label": "TEST_ONLY_CLASS_LABEL",
        "demographic_label": "TEST_ONLY_DEMOGRAPHIC_LABEL",
        "Enneagram_label": "TEST_ONLY_ENNEAGRAM_LABEL",
    }
    with CandidateStore(tmp_path / "n4_base.sqlite") as store:
        base, _ = run_s35_case(store)
    with CandidateStore(tmp_path / "n4_labels.sqlite") as store:
        labelled, _ = run_s35_case(store, actor_labels=labels)
    assert base.response.status is labelled.response.status
    assert base.response.reason == labelled.response.reason
    assert base.response.receipt_hash == labelled.response.receipt_hash
    assert base.response.target_proposals == labelled.response.target_proposals == ()
    assert base.decision.branch is labelled.decision.branch
    assert base.decision.reason is labelled.decision.reason
    assert base.receipt.target_branch == labelled.receipt.target_branch
    assert base.receipt.target_reason == labelled.receipt.target_reason


def test_n5_prior_history_does_not_create_practice(tmp_path):
    with CandidateStore(tmp_path / "n5_history_empty.sqlite") as store:
        empty, _ = run_s35_case(store, history=LEGACY_HISTORY, access=None, response=None)
        assert empty.response.reason == UNKNOWN_RECEIVABILITY
        assert empty.response.declared_history_refs == ()
        _assert_no_target(empty, store)
    with CandidateStore(tmp_path / "n5_history_present.sqlite") as store:
        present, _ = run_s35_case(store, history=LEGACY_HISTORY)
        assert present.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert present.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert present.response.declared_history_refs == ()
        _assert_no_target(present, store)


def test_missing_response_after_access_is_receivable_no_uptake(tmp_path):
    with CandidateStore(tmp_path / "no_uptake.sqlite") as store:
        result, _ = run_s35_case(store, response=None)
        assert result.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert result.response.reason == RECEIVABLE_NO_OBSERVED_UPTAKE
        assert result.response.uptake_refs == ()
        _assert_no_target(result, store)
        body = committed_response(store, result.receipt.response_ref)
        receipt = body["s35_receipt"]
        assert receipt["outcome"] == RECEIVABLE_NO_OBSERVED_UPTAKE
        assert receipt["access_source_ref"].startswith("TEST_ONLY_ADP017_ACCESS")
        assert receipt["observed_response_ref"] == ""


def test_targetless_later_consumer_has_no_ghost_target(tmp_path):
    consumer = LaterActionConsumer(
        "TEST_ONLY_S36_E2_READER", "committed_target_state"
    )
    with CandidateStore(tmp_path / "later_read.sqlite") as store:
        result, _ = run_s35_case(store, later_consumer=consumer)
        assert result.response.target_proposals == ()
        assert result.decision.branch is TargetBranch.NO_CHANGE
        assert result.decision.reason is TargetReason.NO_PROPOSAL
        assert result.committed is True
        assert store.committed_target_ids() == frozenset()
        assert result.later_read.status is LaterActionStatus.STATE_ABSENT
        assert result.later_read.state_hash == ""
        assert result.later_read.committed_record is None
