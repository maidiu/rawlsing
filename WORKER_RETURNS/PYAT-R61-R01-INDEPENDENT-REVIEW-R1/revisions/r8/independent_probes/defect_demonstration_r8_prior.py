"""Record exact R7 candidate behavior for reviewer defect and host-trust cases."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

PROBE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBE_DIR))

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.test_universal_grammar import (
    _campaign_fixture, _query,
)
from rawlsing_next.universal_grammar.native_map import (
    RetainedRecurrenceCampaign, create_campaign,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey

OUT = Path(__file__).resolve().parents[1] / "evidence" / "defect_demonstrations.json"


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


def main() -> None:
    result = {}

    # H1: target_label not tied to the query target.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    c = create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="wrong-label", query_object=query,
        condition_catalog=s1, repository=source["repo"],
        authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    )
    i = _issue_root(c, s1)
    e = c.execute(i)
    plan = next(r["plan"] for r in c.inspect()["issuances"] if r["issuance_ref"] == i)
    result["H1_target_label_mismatch"] = {
        "create_accepted": True, "issue_accepted": True,
        "execute_accepted": bool(e), "plan_target_label": plan["target_label"],
        "expected_query_target_label": "t",
        "plan_query_ref": plan["query_ref"],
    }

    # H2: query target differs from the declared target label.
    wrong_query = _query(source, qauth, root, ("s3",), tag="r61-r7-demo-target-s3")
    c2 = create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=wrong_query,
        condition_catalog=s1, repository=source["repo"],
        authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    )
    i2 = _issue_root(c2, s1)
    e2 = c2.execute(i2)
    plan2 = next(r["plan"] for r in c2.inspect()["issuances"] if r["issuance_ref"] == i2)
    result["H2_query_target_mismatch"] = {
        "create_accepted": True, "issue_accepted": True,
        "execute_accepted": bool(e2), "plan_target_label": plan2["target_label"],
        "query_target": "s3", "plan_query_ref": plan2["query_ref"],
    }

    # H3: catalog key (s1,0) bound to the s1=1 predicate.
    wrong_predicate = next(
        predicate for key, value, predicate in s1
        if key.item_id == "s1" and value == 1
    )
    right_predicate = next(
        predicate for key, value, predicate in s1
        if key.item_id == "s1" and value == 0
    )
    c3 = create_campaign(
        policy=policy, root_predicate=root,
        source_release_refs=(source["release_ref"],),
        target_label="t", query_object=query,
        condition_catalog=[(OccurrenceKey("s1"), 0, wrong_predicate)],
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
    )
    i3 = _issue_root(c3, ((OccurrenceKey("s1"), 0, wrong_predicate),))
    e3 = c3.execute(i3)
    plan3 = next(r["plan"] for r in c3.inspect()["issuances"] if r["issuance_ref"] == i3)
    entry = plan3["condition_entries"][0]
    result["H3_catalog_key_predicate_mismatch"] = {
        "create_accepted": True, "issue_accepted": True,
        "execute_accepted": bool(e3),
        "plan_condition_key": entry["key"],
        "plan_condition_value": entry["value"],
        "bound_predicate_ref": entry["predicate_ref"],
        "semantically_expected_predicate_ref": right_predicate.ref.as_dict(),
        "bound_is_wrong_predicate": entry["predicate_ref"] == wrong_predicate.ref.as_dict(),
    }

    # H4: malformed public condition key.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    try:
        campaign.issue(
            parent_lineage_refs=(campaign.root_lineage_ref,),
            condition_refs=(("s1", 0),),
        )
        result["H4_malformed_condition_key"] = {"accepted": True}
    except Exception as exc:  # noqa: BLE001
        result["H4_malformed_condition_key"] = {
            "accepted": False, "type": type(exc).__name__, "message": str(exc),
        }

    # H5: duplicate condition refs.
    first = (s1[0][0], s1[0][1])
    try:
        campaign.issue(
            parent_lineage_refs=(campaign.root_lineage_ref,),
            condition_refs=(first, first),
        )
        result["H5_duplicate_condition_refs"] = {"accepted": True}
    except Exception as exc:  # noqa: BLE001
        result["H5_duplicate_condition_refs"] = {
            "accepted": False, "type": type(exc).__name__, "message": str(exc),
        }

    # Host-trust demonstration: forged snapshot + forged pin.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i = _issue_root(campaign, s1)
    e = campaign.execute(i)
    campaign.activate(e)
    snapshot = campaign.snapshot()
    altered = deepcopy(snapshot)
    altered["payload"]["lineage"][1]["parent_id"] = "forged-parent-id"
    altered, forged_pin = _forge_pin(altered)
    try:
        forged = _restore(altered, forged_pin, source, campaign, query)
        forged_result = {
            "restore_accepted": True,
            "same_campaign_ref": forged.campaign_ref == campaign.campaign_ref,
            "forged_lineage_parent_id": forged.inspect()["lineage"][1]["parent_id"],
        }
    except Exception as exc:  # noqa: BLE001
        forged_result = {
            "restore_accepted": False, "type": type(exc).__name__,
            "message": str(exc),
        }
    original_pin_refused = False
    try:
        _restore(altered, snapshot["checkpoint_ref"], source, campaign, query)
    except Exception:
        original_pin_refused = True
    forged_result["original_pin_rejects_altered_snapshot"] = original_pin_refused
    forged_result["note"] = (
        "R61AF: forged snapshot plus forged trusted pin is host-trust replacement, "
        "not an in-scope product-refusal gate; recorded only as a demonstration."
    )
    result["HOST_TRUST_forged_snapshot_and_pin"] = forged_result

    # Internal closure refusals with a self-consistent forged pin.
    checks = {}

    def closure_case(name, mutate):
        snap = deepcopy(snapshot)
        mutate(snap["payload"])
        snap, pin = _forge_pin(snap)
        try:
            _restore(snap, pin, source, campaign, query)
            checks[name] = "ACCEPTED"
        except Exception as exc:  # noqa: BLE001
            checks[name] = f"{type(exc).__name__}: {exc}"

    closure_case("missing_receipt", lambda p: p["executions"][0]["activation_preimage"]["receipts"].pop())
    closure_case("missing_handoff", lambda p: p["executions"][0]["activation_preimage"]["handoffs"].pop())
    closure_case("altered_lineage_ancestry", lambda p: p["lineage"][1]["ancestry_conditions"].append(
        {"key": {"item_id": "s2"}, "value": 1}))
    closure_case("altered_cumulative", lambda p: p["issuances"][0].__setitem__("cumulative_issued_count", 999))
    closure_case("duplicate_execution", lambda p: p["executions"].append(deepcopy(p["executions"][0])))
    result["internal_closure_checks"] = checks

    # Chronology positives: two gen1 batches, stopped head, pre-activation restore.
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = _issue_root(campaign, s1)
    e1 = campaign.execute(i1)
    i2 = _issue_root(campaign, s2)
    e2 = campaign.execute(i2)
    records = campaign.inspect()["issuances"]
    result["chronology_multibatch"] = {
        "cumulative": [r["cumulative_issued_count"] for r in records],
        "predecessors": [r["predecessor_issuance_ref"] for r in records],
        "counts": [r["predecessor_issued_count"] for r in records],
    }
    pre = campaign.snapshot()
    restored = _restore(pre, pre["checkpoint_ref"], source, campaign, query)
    a1 = restored.activate(e1)
    a2 = restored.activate(e2)
    result["pre_activation_restore"] = {
        "activation_1": bool(a1), "activation_2": bool(a2),
        "execution_count_after": len(restored.inspect()["executions"]),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
