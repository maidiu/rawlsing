"""R61-R01V R6 independent expected-refusal probes against the retained owner."""
from __future__ import annotations

from copy import deepcopy

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _condition_predicates, _recurrence_policy, _recurrence_source,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, RecurrenceRefusal, create_campaign,
)


def _fixture(policy=None):
    return _campaign_fixture(policy=policy)


def _issue_root(campaign, conditions):
    return campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _active_refs(campaign, activation_ref):
    return next(
        record["active_lineage_refs"] for record in campaign.inspect()["activations"]
        if record["activation_ref"] == activation_ref
    )


def test_H1_multiple_explicit_batches_at_generation_one_are_allowed():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    first = _issue_root(campaign, s1)
    assert first
    second = _issue_root(campaign, s1)
    assert second
    records = campaign.inspect()["issuances"]
    assert len(records) == 2
    assert all(record["generation"] == 1 for record in records)


def test_H2_create_validates_root_source_release_compatibility():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    bogus = ExactRef("C11_SOURCE_RELEASE@1", "urn:test:r61-r6:bogus-release", "f" * 64)
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root, source_release_refs=(bogus,),
            target_label="t", query_object=query, condition_catalog=s1 + s2 + s3,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_H3_restore_rejects_wrong_query_context():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    from rawlsing_next.tests.test_universal_grammar import _query
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r6-wrong-restore-query")
    with pytest.raises(RecurrenceRefusal):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=wrong_query,
        )


def test_H4_self_consistent_forged_snapshot_cannot_be_admitted():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["parent_id"] = "forged-parent-id"
    forged_pin = semantic_hash(altered["payload"])
    altered["checkpoint_ref"] = forged_pin
    with pytest.raises(RecurrenceRefusal):
        RetainedRecurrenceCampaign.restore(
            snapshot=altered, expected_checkpoint_ref=forged_pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )


def test_H5_restore_before_activation_can_continue_to_activation():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    restored_execution = restored.execute(issue)
    assert restored.activate(restored_execution)


def test_H6_stopped_issuance_keeps_the_issuance_predecessor_chain():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture(
        policy=_recurrence_policy(per_generation=0)
    )
    first = _issue_root(campaign, s1)
    second = _issue_root(campaign, s2)
    records = {
        record["issuance_ref"]: record for record in campaign.inspect()["issuances"]
    }
    assert records[first]["state"] == "STOPPED_BUDGET"
    assert records[second]["state"] == "STOPPED_BUDGET"
    assert records[second]["predecessor_issuance_ref"] == first


def test_H7_duplicate_condition_catalog_is_refused():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    duplicate_catalog = list(s1) + list(s1)
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],), target_label="t",
            query_object=query, condition_catalog=duplicate_catalog,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_H8_restore_requires_the_full_frozen_condition_context():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    incomplete_catalog = {
        (key.key, __import__("json").dumps(value)): predicate
        for key, value, predicate in s1
    }
    with pytest.raises(RecurrenceRefusal):
        RetainedRecurrenceCampaign.restore(
            snapshot=snapshot, expected_checkpoint_ref=pin,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=incomplete_catalog, query_object=query,
        )
