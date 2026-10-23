"""Record exact R6 candidate behavior for the reviewer's failing probes."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

PROBE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBE_DIR))

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _condition_predicates, _query, _recurrence_policy,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, create_campaign,
)

OUT = Path(__file__).resolve().parents[1] / "evidence" / "defect_demonstrations.json"


def _issue_root(campaign, conditions):
    return campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _active(campaign, activation_ref):
    return next(
        record["active_lineage_refs"] for record in campaign.inspect()["activations"]
        if record["activation_ref"] == activation_ref
    )


def main() -> None:
    result = {}

    # H1: second explicit batch at generation 1.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    first = _issue_root(campaign, s1)
    try:
        second = _issue_root(campaign, s1)
        result["H1_multiple_gen1_batches"] = {"accepted": True, "ref": second}
    except Exception as exc:  # noqa: BLE001
        result["H1_multiple_gen1_batches"] = {
            "accepted": False, "type": type(exc).__name__, "message": str(exc),
        }

    # H2: create with a release absent from the repository, then execute.
    bogus = ExactRef("C11_SOURCE_RELEASE@1", "urn:test:r61-r6:bogus-release", "f" * 64)
    cbad = create_campaign(
        policy=policy, root_predicate=root, source_release_refs=(bogus,),
        target_label="t", query_object=query, condition_catalog=s1 + s2 + s3,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    )
    ib = _issue_root(cbad, s1)
    eb = cbad.execute(ib)
    native = cbad._executions[eb].native_result
    receipt = native.execution.discovery_result.receipts[0]
    result["H2_bogus_release"] = {
        "create_accepted": True,
        "issue_accepted": True,
        "execute_accepted": True,
        "receipt_count": len(native.execution.discovery_result.receipts),
        "anti_join_no_drop_ok": native.anti_join["no_drop_ok"],
        "first_receipt_release_refs": [dict(ref) for ref in receipt.source_release_refs],
        "requested_bogus_release": bogus.as_dict(),
    }

    # H3: restore with a different query context.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    a1 = campaign.activate(e1)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r6-wrong-restore-query")
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=wrong_query,
    )
    restored_active = _active(restored, next(
        record["activation_ref"] for record in restored.inspect()["activations"]
    ))
    i2 = restored.issue(
        parent_lineage_refs=restored_active,
        condition_refs=tuple((key, value) for key, value, _ in s2),
    )
    e2 = restored.execute(i2)
    plan2 = next(
        record["plan"] for record in restored.inspect()["issuances"]
        if record["issuance_ref"] == i2
    )
    result["H3_wrong_restore_query"] = {
        "restore_accepted": True,
        "root_query_ref": restored.inspect()["root"]["query_ref"],
        "supplied_query_ref": wrong_query.ref.as_dict(),
        "next_issue_accepted": True,
        "next_execute_accepted": bool(e2),
        "plan_query_ref": plan2["query_ref"],
        "query_matches_root": plan2["query_ref"] == restored.inspect()["root"]["query_ref"],
    }

    # H4: self-consistent forged snapshot with a supplied forged pin.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    campaign.activate(e1)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["parent_id"] = "forged-parent-id"
    forged_pin = semantic_hash(altered["payload"])
    altered["checkpoint_ref"] = forged_pin
    forged = RetainedRecurrenceCampaign.restore(
        snapshot=altered, expected_checkpoint_ref=forged_pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    result["H4_forged_snapshot_forged_pin"] = {
        "restore_accepted": True,
        "same_campaign_ref_as_original": forged.campaign_ref == campaign.campaign_ref,
        "forged_lineage_parent_id": forged.inspect()["lineage"][1]["parent_id"],
        "original_pin_rejects_altered_snapshot": True,
    }
    try:
        RetainedRecurrenceCampaign.restore(
            snapshot=altered, expected_checkpoint_ref=snapshot["checkpoint_ref"],
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
            condition_catalog=campaign._condition_catalog, query_object=query,
        )
        result["H4_forged_snapshot_forged_pin"]["original_pin_rejects_altered_snapshot"] = False
    except Exception as exc:  # noqa: BLE001
        result["H4_forged_snapshot_forged_pin"]["original_pin_error"] = str(exc)

    # H5: restore a completed execution before activation.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    restored_execution = restored.execute(i1)
    try:
        activation = restored.activate(restored_execution)
        result["H5_restore_pre_activation"] = {"activate_accepted": True, "ref": activation}
    except Exception as exc:  # noqa: BLE001
        result["H5_restore_pre_activation"] = {
            "activate_accepted": False, "type": type(exc).__name__, "message": str(exc),
        }

    # H6: two stopped-budget issuances and their predecessor chain.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture(
        policy=_recurrence_policy(per_generation=0)
    )
    first = _issue_root(campaign, s1)
    second = _issue_root(campaign, s2)
    records = {
        record["issuance_ref"]: record for record in campaign.inspect()["issuances"]
    }
    result["H6_stopped_issuance_chain"] = {
        "first_ref": first, "second_ref": second,
        "first_predecessor": records[first]["predecessor_issuance_ref"],
        "second_predecessor": records[second]["predecessor_issuance_ref"],
        "second_should_predecessor_first": records[second]["predecessor_issuance_ref"] == first,
        "first_cumulative": records[first]["cumulative_issued_count"],
        "second_cumulative": records[second]["cumulative_issued_count"],
    }

    # H7: duplicate condition catalog.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    duplicate = list(s1) + list(s1)
    try:
        cdup = create_campaign(
            policy=policy, root_predicate=root,
            source_release_refs=(source["release_ref"],), target_label="t",
            query_object=query, condition_catalog=duplicate,
            repository=source["repo"], authority_registry=campaign._registry,
            authority_factory=campaign._authority_factory,
        )
        result["H7_duplicate_catalog"] = {
            "accepted": True, "catalog_size": len(cdup._condition_catalog),
        }
    except Exception as exc:  # noqa: BLE001
        result["H7_duplicate_catalog"] = {
            "accepted": False, "type": type(exc).__name__, "message": str(exc),
        }

    # H8: restore with an incomplete frozen condition context.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    campaign.activate(e1)
    snapshot = campaign.snapshot()
    pin = snapshot["checkpoint_ref"]
    incomplete = {
        (key.key, __import__("json").dumps(value)): predicate
        for key, value, predicate in s1
    }
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=incomplete, query_object=query,
    )
    active = _active(restored, next(
        record["activation_ref"] for record in restored.inspect()["activations"]
    ))
    try:
        restored.issue(
            parent_lineage_refs=active,
            condition_refs=tuple((key, value) for key, value, _ in s2),
        )
        next_issue = "accepted"
    except Exception as exc:  # noqa: BLE001
        next_issue = f"{type(exc).__name__}: {exc}"
    result["H8_incomplete_restore_catalog"] = {
        "restore_accepted": True,
        "snapshot_catalog_size": len(snapshot["payload"]["condition_catalog"]),
        "supplied_catalog_size": len(incomplete),
        "subsequent_issue": next_issue,
    }

    # Context: a second batch at generation 2 is accepted and counted.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    a1 = campaign.activate(e1)
    active1 = _active(campaign, a1)
    i2a = campaign.issue(
        parent_lineage_refs=active1,
        condition_refs=tuple((key, value) for key, value, _ in s2),
    )
    e2a = campaign.execute(i2a)
    campaign.activate(e2a)
    i2b = campaign.issue(
        parent_lineage_refs=active1,
        condition_refs=tuple((key, value) for key, value, _ in s3),
    )
    e2b = campaign.execute(i2b)
    records = [
        record for record in campaign.inspect()["issuances"]
        if record["generation"] == 2
    ]
    result["CONTEXT_multiple_gen2_batches"] = {
        "accepted": True,
        "count": len(records),
        "cumulative": [record["cumulative_issued_count"] for record in records],
        "predecessor_counts": [record["predecessor_issued_count"] for record in records],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
