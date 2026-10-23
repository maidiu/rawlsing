"""R61-R01V R7 independent controls and chronology/cold proofs."""
from __future__ import annotations

from copy import deepcopy
import json
import threading

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _query, _recurrence_policy,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, RecurrenceRefusal, create_campaign,
)


def _fixture(policy=None):
    return _campaign_fixture(policy=policy)


def _issue(campaign, parents, conditions):
    return campaign.issue(
        parent_lineage_refs=tuple(parents),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _active(campaign, activation_ref):
    return next(
        record["active_lineage_refs"] for record in campaign.inspect()["activations"]
        if record["activation_ref"] == activation_ref
    )


def _count_native(monkeypatch):
    import rawlsing_next.universal_grammar.native_map as nm
    calls = {"native": 0}
    original = nm.execute_exact_bounded_discovery_with_handoffs

    def counted(*args, **kwargs):
        calls["native"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(nm, "execute_exact_bounded_discovery_with_handoffs", counted)
    return calls


def test_C1_completed_issue_retry_has_no_second_native_call(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    calls = _count_native(monkeypatch)
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    assert calls["native"] == 1
    assert campaign.execute(issue) == execution
    assert calls["native"] == 1


def test_C2_zero_caps_stop_without_native_call(monkeypatch):
    for policy in (
        _recurrence_policy(per_generation=0),
        _recurrence_policy(total=0),
    ):
        source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture(policy=policy)
        calls = _count_native(monkeypatch)
        issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
        record = next(
            item for item in campaign.inspect()["issuances"]
            if item["issuance_ref"] == issue
        )
        assert record["state"] == "STOPPED_BUDGET"
        assert record["plan"]["expected_operations"] == []
        assert calls["native"] == 0
        with pytest.raises(RecurrenceRefusal):
            campaign.execute(issue)
        assert calls["native"] == 0


def test_C3_chronology_advances_through_stopped_no_work(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture(
        policy=_recurrence_policy(per_generation=0)
    )
    calls = _count_native(monkeypatch)
    first = _issue(campaign, (campaign.root_lineage_ref,), s1)
    second = _issue(campaign, (campaign.root_lineage_ref,), s2)
    records = {r["issuance_ref"]: r for r in campaign.inspect()["issuances"]}
    assert records[first]["state"] == "STOPPED_BUDGET"
    assert records[second]["state"] == "STOPPED_BUDGET"
    assert records[second]["predecessor_issuance_ref"] == first
    assert records[second]["predecessor_issued_count"] == 0
    assert records[second]["cumulative_issued_count"] == 0
    assert calls["native"] == 0
    with pytest.raises(RecurrenceRefusal):
        campaign.execute(second)
    assert calls["native"] == 0


def test_C4_multiple_generation_one_batches_are_counted(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    calls = _count_native(monkeypatch)
    first = _issue(campaign, (campaign.root_lineage_ref,), s1)
    second = _issue(campaign, (campaign.root_lineage_ref,), s2)
    first_execution = campaign.execute(first)
    second_execution = campaign.execute(second)
    records = [r for r in campaign.inspect()["issuances"] if r["generation"] == 1]
    assert [r["cumulative_issued_count"] for r in records] == [4, 8]
    assert records[1]["predecessor_issuance_ref"] == first
    assert records[1]["predecessor_issued_count"] == 4
    assert calls["native"] == 2
    assert campaign.activate(first_execution)
    assert campaign.activate(second_execution)
    assert calls["native"] == 2


def test_C5_pre_activation_restore_activates_and_runs_next(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    calls = _count_native(monkeypatch)
    issue1 = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution1 = campaign.execute(issue1)
    assert calls["native"] == 1
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    assert restored.execute(issue1) == execution1
    activation1 = restored.activate(execution1)
    active1 = _active(restored, activation1)
    assert calls["native"] == 1
    issue2 = _issue(restored, active1, s2)
    execution2 = restored.execute(issue2)
    assert calls["native"] == 2
    record2 = next(
        r for r in restored.inspect()["issuances"] if r["issuance_ref"] == issue2
    )
    assert record2["cumulative_issued_count"] == 8
    assert execution2


def test_C6_post_activation_restore_returns_existing_activation(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    calls = _count_native(monkeypatch)
    issue1 = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution1 = campaign.execute(issue1)
    activation1 = campaign.activate(execution1)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    assert restored.activate(execution1) == activation1
    assert calls["native"] == 1


def test_C7_fault_refusals_and_restoration_on_same_consumer():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue1 = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution1 = campaign.execute(issue1)
    activation1 = campaign.activate(execution1)
    active1 = _active(campaign, activation1)
    issue2 = _issue(campaign, active1, s2)
    execution2 = campaign.execute(issue2)
    activation2 = campaign.activate(execution2)
    active2 = _active(campaign, activation2)
    with pytest.raises(RecurrenceRefusal, match="LINEAGE_REFERENCE_NOT_RETAINED"):
        _issue(campaign, ("forged-lineage-ref",), s2)
    with pytest.raises(RecurrenceRefusal, match="REQUESTED_GENERATION_MISMATCH"):
        campaign.issue(
            parent_lineage_refs=(active1[0],),
            condition_refs=tuple((key, value) for key, value, _ in s2),
            requested_generation=4,
        )
    with pytest.raises(RecurrenceRefusal, match="PREDECESSOR_ISSUANCE_NOT_RETAINED_HEAD"):
        campaign.issue(
            parent_lineage_refs=active2,
            condition_refs=tuple((key, value) for key, value, _ in s3),
            predecessor_issuance_ref=issue1,
        )
    with pytest.raises(RecurrenceRefusal, match="ACTIVATION_NEXT_GENERATION_MISMATCH"):
        campaign.activate(execution2, requested_next_generation=1)
    with pytest.raises(RecurrenceRefusal, match="ISSUANCE_REFERENCE_NOT_RETAINED"):
        campaign.execute("forged-issuance")
    with pytest.raises(RecurrenceRefusal, match="EXECUTION_REFERENCE_NOT_RETAINED"):
        campaign.activate("forged-execution")
    assert campaign.execute(issue1) == execution1
    assert campaign.execute(issue2) == execution2


def test_C8_cross_campaign_lineage_is_not_accepted():
    source1, qauth1, root1, query1, policy1, s1, s2, s3, campaign1 = _fixture()
    source2, qauth2, root2, query2, policy2, t1, t2, t3, campaign2 = _fixture(
        policy=_recurrence_policy(total=11)
    )
    with pytest.raises(RecurrenceRefusal, match="LINEAGE_REFERENCE_NOT_RETAINED"):
        _issue(campaign2, (campaign1.root_lineage_ref,), t1)


def test_C9_inspect_is_detached_and_cannot_register_history():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    before = campaign.inspect()
    copied = deepcopy(before)
    copied["root"]["campaign_ref"] = "mutated"
    copied["lineage"][0]["parent_id"] = "mutated"
    copied["issuances"][0]["cumulative_issued_count"] = 999
    copied["executions"][0]["anti_join"]["no_drop_ok"] = False
    copied["activations"][0]["next_generation"] = 99
    after = campaign.inspect()
    assert after["root"]["campaign_ref"] == before["root"]["campaign_ref"]
    assert after["lineage"][0]["parent_id"] == before["lineage"][0]["parent_id"]
    assert after["issuances"][0]["cumulative_issued_count"] == 4
    assert after["executions"][0]["anti_join"]["no_drop_ok"] is True
    assert after["activations"][0]["next_generation"] == before["activations"][0]["next_generation"]
    assert campaign.campaign_ref == before["root"]["campaign_ref"]


def test_C10_fixed_original_pin_rejects_altered_snapshot_and_missing_pin():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["parent_id"] = "tampered"
    altered["checkpoint_ref"] = semantic_hash(altered["payload"])
    with pytest.raises(RecurrenceRefusal, match="SNAPSHOT_CHECKPOINT_PIN_MISMATCH"):
        RetainedRecurrenceCampaign.restore(
            snapshot=altered, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )
    with pytest.raises(RecurrenceRefusal, match="SNAPSHOT_CHECKPOINT_PIN_MISMATCH"):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref="",
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )
    genuine = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    assert genuine.inspect()["issuances"][0]["cumulative_issued_count"] == 4


def test_C11_restore_rejects_wrong_query_and_incomplete_catalog():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r7-wrong-restore-query")
    with pytest.raises(RecurrenceRefusal):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=wrong_query,
        )
    incomplete = {
        (key.key, json.dumps(value)): predicate
        for key, value, predicate in s1
    }
    with pytest.raises(RecurrenceRefusal):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=incomplete, query_object=query,
        )


def test_C12_duplicate_catalog_and_missing_release_refuse_typed():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    with pytest.raises(RecurrenceRefusal, match="DUPLICATE_CAMPAIGN_CATALOG_KEY"):
        create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],), target_label="t",
            query_object=query, condition_catalog=list(s1) + [s1[0]],
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )
    bogus = ExactRef("C11_SOURCE_RELEASE@1", "urn:test:r61-r7:bogus", "f" * 64)
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root, source_release_refs=(bogus,),
            target_label="t", query_object=query, condition_catalog=s1,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_C13_typed_receipt_states_are_retained_in_preimage():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    snapshot = campaign.snapshot()
    preimage = next(
        record["activation_preimage"] for record in snapshot["payload"]["executions"]
        if record["execution_ref"] == execution
    )
    states = {receipt["typed_state"] for receipt in preimage["receipts"]}
    assert states
    assert states <= {
        "DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY", "INSUFFICIENT_SUPPORT",
        "NONCOMPARABLE", "COVERAGE_LIMITED",
    }
    assert preimage["handoffs"] is not None


def test_C14_concurrent_execute_is_serialized_to_one_native_call(monkeypatch):
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    calls = _count_native(monkeypatch)
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    results = []
    errors = []

    def worker():
        try:
            results.append(campaign.execute(issue))
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert not errors
    assert len(results) == 4
    assert len(set(results)) == 1
    assert calls["native"] == 1


def test_C15_ambiguous_inflight_stays_typed_hold_after_restore(monkeypatch):
    import rawlsing_next.universal_grammar.native_map as nm
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    original = nm.execute_exact_bounded_discovery_with_handoffs

    def boom(*args, **kwargs):
        raise RuntimeError("synthetic ambiguous native failure")

    monkeypatch.setattr(nm, "execute_exact_bounded_discovery_with_handoffs", boom)
    with pytest.raises(RuntimeError):
        campaign.execute(issue)
    monkeypatch.setattr(nm, "execute_exact_bounded_discovery_with_handoffs", original)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    assert snapshot["payload"]["inflight_issuance_refs"] == [issue]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    with pytest.raises(RecurrenceRefusal, match="HOLD_AMBIGUOUS_NATIVE_EXECUTION"):
        restored.execute(issue)
