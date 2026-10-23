"""R61-R01V R7 independent hostile/closure probes."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _query,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, RecurrenceRefusal, create_campaign,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey


def _fixture():
    return _campaign_fixture()


def _issue_root(campaign, conditions):
    return campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _forge_pin(snapshot):
    snapshot = deepcopy(snapshot)
    pin = semantic_hash(snapshot["payload"])
    snapshot["checkpoint_ref"] = pin
    return snapshot, pin


def _restore(snapshot, pin, source, campaign, query):
    return RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )


def test_H1_target_label_must_match_the_query_target():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],),
            target_label="wrong-label", query_object=query,
            condition_catalog=s1, repository=source["repo"],
            authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_H2_query_target_must_match_the_declared_target_label():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r7-hostile-target-s3")
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],),
            target_label="t", query_object=wrong_query,
            condition_catalog=s1, repository=source["repo"],
            authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_H3_condition_catalog_key_must_match_its_predicate_semantics():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    wrong_predicate = next(
        predicate for key, value, predicate in s1
        if key.item_id == "s1" and value == 1
    )
    with pytest.raises(RecurrenceRefusal):
        create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],),
            target_label="t", query_object=query,
            condition_catalog=[(OccurrenceKey("s1"), 0, wrong_predicate)],
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )


def test_H4_issue_malformed_condition_key_is_typed_refusal():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    with pytest.raises(RecurrenceRefusal):
        campaign.issue(
            parent_lineage_refs=(campaign.root_lineage_ref,),
            condition_refs=(("s1", 0),),
        )


def test_H5_issue_duplicate_condition_refs_is_typed_refusal():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    first = (s1[0][0], s1[0][1])
    with pytest.raises(RecurrenceRefusal):
        campaign.issue(
            parent_lineage_refs=(campaign.root_lineage_ref,),
            condition_refs=(first, first),
        )


def test_H6_restore_missing_receipt_does_not_silently_drop():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["executions"][0]["activation_preimage"]["receipts"].pop()
    altered, pin = _forge_pin(altered)
    with pytest.raises(RecurrenceRefusal):
        _restore(altered, pin, source, campaign, query)


def test_H7_restore_missing_handoff_does_not_silently_drop():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["executions"][0]["activation_preimage"]["handoffs"].pop()
    altered, pin = _forge_pin(altered)
    with pytest.raises(RecurrenceRefusal):
        _restore(altered, pin, source, campaign, query)


def test_H8_restore_altered_lineage_ancestry_refuses():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["ancestry_conditions"].append(
        {"key": {"item_id": "s2"}, "value": 1}
    )
    altered, pin = _forge_pin(altered)
    with pytest.raises(RecurrenceRefusal):
        _restore(altered, pin, source, campaign, query)


def test_H9_restore_altered_cumulative_count_refuses():
    source, qauth, root, query, policy, s1, s2, s3, campaign = _fixture()
    issue = _issue_root(campaign, s1)
    execution = campaign.execute(issue)
    campaign.activate(execution)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["issuances"][0]["cumulative_issued_count"] = 999
    altered, pin = _forge_pin(altered)
    with pytest.raises(RecurrenceRefusal):
        _restore(altered, pin, source, campaign, query)
