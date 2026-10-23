"""R61-R01V R6 independent positive/negative owner controls that must pass."""
from __future__ import annotations

from copy import deepcopy

import pytest

from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _recurrence_policy,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, RecurrenceRefusal,
)


def _active(campaign, activation_ref):
    return next(
        record["active_lineage_refs"] for record in campaign.inspect()["activations"]
        if record["activation_ref"] == activation_ref
    )


def _issue(campaign, parents, conditions):
    return campaign.issue(
        parent_lineage_refs=tuple(parents),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _counted(campaign):
    calls = []
    original = campaign._authority_factory

    def factory(grammar):
        calls.append(grammar)
        return original(grammar)

    campaign._authority_factory = factory
    return calls


def test_C1_completed_issue_retry_is_idempotent_without_second_native_call():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    calls = _counted(campaign)
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    assert len(calls) == 1
    assert campaign.execute(issue) == execution
    assert len(calls) == 1


def test_C2_zero_caps_are_stopped_budget_and_never_call_native():
    for policy in (
        _recurrence_policy(per_generation=0),
        _recurrence_policy(total=0),
    ):
        source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture(
            policy=policy
        )
        calls = _counted(campaign)
        issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
        record = next(
            item for item in campaign.inspect()["issuances"]
            if item["issuance_ref"] == issue
        )
        assert record["state"] == "STOPPED_BUDGET"
        assert record["plan"]["expected_operations"] == []
        assert calls == []
        with pytest.raises(RecurrenceRefusal):
            campaign.execute(issue)
        assert calls == []


def test_C3_forged_lineage_requested_generation_and_predecessor_refuse():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
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


def test_C4_cross_campaign_lineage_is_not_accepted():
    source1, qauth1, root1, query1, policy1, s1, s2, s3, campaign1 = _campaign_fixture()
    source2, qauth2, root2, query2, policy2, t1, t2, t3, campaign2 = _campaign_fixture(
        policy=_recurrence_policy(total=11)
    )
    with pytest.raises(RecurrenceRefusal, match="LINEAGE_REFERENCE_NOT_RETAINED"):
        _issue(campaign2, (campaign1.root_lineage_ref,), t1)


def test_C5_inspect_is_deep_detached_and_cannot_register_history():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    activation = campaign.activate(execution)
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
    assert after["issuances"][0]["cumulative_issued_count"] == (
        before["issuances"][0]["cumulative_issued_count"]
    )
    assert after["executions"][0]["anti_join"]["no_drop_ok"] is True
    assert after["activations"][0]["next_generation"] == before["activations"][0]["next_generation"]
    assert campaign.campaign_ref == before["root"]["campaign_ref"]


def test_C6_altered_snapshot_with_original_pin_and_missing_pin_refuse():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    issue = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["parent_id"] = "tampered"
    altered["checkpoint_ref"] = __import__(
        "rawlsing_next.pre553_empirical_objects", fromlist=["semantic_hash"]
    ).semantic_hash(altered["payload"])
    with pytest.raises(RecurrenceRefusal, match="CHECKPOINT_PIN_MISMATCH"):
        RetainedRecurrenceCampaign.restore(
            snapshot=altered, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )
    with pytest.raises(RecurrenceRefusal, match="CHECKPOINT_PIN_MISMATCH"):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref="wrong-pin",
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )


def test_C7_multiple_batches_at_generation_two_are_counted():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    issue1 = _issue(campaign, (campaign.root_lineage_ref,), s1)
    execution1 = campaign.execute(issue1)
    activation1 = campaign.activate(execution1)
    active1 = _active(campaign, activation1)
    issue2a = _issue(campaign, active1, s2)
    execution2a = campaign.execute(issue2a)
    activation2a = campaign.activate(execution2a)
    issue2b = _issue(campaign, active1, s3)
    execution2b = campaign.execute(issue2b)
    records = [
        record for record in campaign.inspect()["issuances"]
        if record["generation"] == 2
    ]
    assert len(records) == 2
    assert records[0]["cumulative_issued_count"] == 8
    assert records[1]["cumulative_issued_count"] == 12
    assert records[1]["predecessor_issued_count"] == 8
    assert issue2a != issue2b
    assert execution2a != execution2b
    assert activation2a


def test_C8_run_local_concurrent_execute_is_serialized_and_idempotent():
    import threading

    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    calls = _counted(campaign)
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
    assert len(calls) == 1
