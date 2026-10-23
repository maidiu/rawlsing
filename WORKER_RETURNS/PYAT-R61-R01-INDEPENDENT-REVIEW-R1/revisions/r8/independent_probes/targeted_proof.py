"""R8 targeted proof: the four R7 defects now refuse; retained owner still works."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

PROBE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBE_DIR))

from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _query,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, create_campaign,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey

OUT = Path(__file__).resolve().parents[1] / "evidence" / "targeted_results.json"


def _issue_root(campaign, conditions):
    return campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in conditions),
    )


def _capture(fn):
    try:
        value = fn()
        return {"accepted": True,
                "value": getattr(value, "campaign_ref", bool(value))}
    except Exception as exc:  # noqa: BLE001
        return {"accepted": False, "type": type(exc).__name__, "message": str(exc)}


def main() -> None:
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    result = {}

    result["H1_wrong_target_label"] = _capture(lambda: create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="wrong-label", query_object=query,
        condition_catalog=s1, repository=source["repo"],
        authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    ))
    result["H1_correct_target_label"] = _capture(lambda: create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=query,
        condition_catalog=s1, repository=source["repo"],
        authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    ))
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r8-target-s3")
    result["H2_query_target_mismatch"] = _capture(lambda: create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=wrong_query,
        condition_catalog=s1, repository=source["repo"],
        authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    ))
    wrong_predicate = next(
        predicate for key, value, predicate in s1
        if key.item_id == "s1" and value == 1
    )
    right_predicate = next(
        predicate for key, value, predicate in s1
        if key.item_id == "s1" and value == 0
    )
    result["H3_wrong_condition_predicate"] = _capture(lambda: create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=query,
        condition_catalog=[(OccurrenceKey("s1"), 0, wrong_predicate)],
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    ))
    result["H3_correct_condition_predicate"] = _capture(lambda: create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=query,
        condition_catalog=[(OccurrenceKey("s1"), 0, right_predicate)],
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    ))
    result["H4_malformed_condition_key"] = _capture(lambda: campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=(("s1", 0),),
    ))
    first = (s1[0][0], s1[0][1])
    result["H5_duplicate_condition_refs"] = _capture(lambda: campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=(first, first),
    ))

    # Retained owner positive and chronology.
    source2, qauth2, root2, query2, policy2, t1, t2, t3, c = _campaign_fixture()
    i1 = _issue_root(c, t1)
    e1 = c.execute(i1)
    i2 = _issue_root(c, t2)
    e2 = c.execute(i2)
    result["retained_multibatch"] = {
        "accepted": True,
        "cumulative": [r["cumulative_issued_count"]
                       for r in c.inspect()["issuances"]],
        "predecessors": [r["predecessor_issuance_ref"]
                         for r in c.inspect()["issuances"]],
        "predecessor_counts": [r["predecessor_issued_count"]
                               for r in c.inspect()["issuances"]],
    }
    snapshot = c.snapshot()
    pin = snapshot["checkpoint_ref"]
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=pin,
        repository=source2["repo"], authority_registry=c._registry,
        authority_factory=c._authority_factory,
        condition_catalog=c._condition_catalog, query_object=query2,
    )
    result["pre_activation_restore"] = {
        "restore_accepted": True,
        "activation_1": bool(restored.activate(e1)),
        "activation_2": bool(restored.activate(e2)),
        "executions_after": len(restored.inspect()["executions"]),
    }

    # Genuine restore vs wrong context through the same validator.
    altered = deepcopy(snapshot)
    altered["payload"]["root"]["target_label"] = "wrong-label"
    altered["checkpoint_ref"] = __import__(
        "rawlsing_next.pre553_empirical_objects", fromlist=["semantic_hash"]
    ).semantic_hash(altered["payload"])
    result["restore_altered_target_context"] = _capture(lambda: RetainedRecurrenceCampaign.restore(
        snapshot=altered, expected_checkpoint_ref=pin,
        repository=source2["repo"], authority_registry=c._registry,
        authority_factory=c._authority_factory,
        condition_catalog=c._condition_catalog, query_object=query2,
    ))
    result["restore_genuine"] = {
        "accepted": True,
        "executions": len(restored.inspect()["executions"]),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
