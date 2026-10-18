"""GF1H independent hostile mutations of a genuine source-free 2×2 relation."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

COURT = Path(os.environ["GF1H_COURT"]).resolve()
GF1G = Path(os.environ["GF1H_GF1G"]).resolve()
os.environ["GF1G_COURT"] = str(COURT)
os.environ["GF1G_ORACLE"] = str(GF1G / "01_FROZEN_ORACLE.json")
spec = importlib.util.spec_from_file_location("gf1g_fixture", GF1G / "phase_a/test_gf1g_precommitted.py")
gf1g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf1g)
G = gf1g.G
CONS = gf1g.CONS


def mutation(change):
    source = gf1g._template()
    fields = dict(source.__dict__)
    fields.pop("content_hash")
    fields.pop("object_id")
    fields["conditional_count_profile"] = deepcopy(fields["conditional_count_profile"])
    change(fields)
    digest = G.semantic_hash(G._projection(fields))
    return G.GenericNativePairRelation(
        **fields, content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")


def cell(fields, c=0, t=0):
    return fields["conditional_count_profile"][c]["target_counts"][t]


@pytest.mark.parametrize("field,value", [
    ("condition_denominator_support", -1),
    ("condition_denominator_support", True),
    ("condition_denominator_support", 1.0),
    ("condition_denominator_support", "1"),
    ("joint_support_count", -1),
    ("joint_support_count", False),
    ("joint_support_count", 1.0),
    ("joint_support_count", "1"),
    ("eligible_joint_risk_total", -1),
    ("eligible_joint_risk_total", True),
    ("eligible_joint_risk_total", 2.0),
    ("excluded_ineligible_target_count", "0"),
])
def test_exact_nonnegative_counts_or_typed_refusal(field, value):
    def change(fields):
        if field == "joint_support_count":
            cell(fields)[field] = value
        elif field == "condition_denominator_support":
            fields["conditional_count_profile"][0][field] = value
        else:
            fields[field] = value
    result = CONS(mutation(change))
    assert result["decision_state"] == "CONSUMER_RELATION_INTEGRITY_REJECTED"
    assert result["separation_class"] is None
    assert result["downstream_value_produced"] is False


@pytest.mark.parametrize("case", ["denominator_mismatch", "support_exceeds_risk",
                                  "positive_zero_state", "zero_positive_state",
                                  "duplicate_target", "foreign_role"])
def test_conservation_and_cell_shape(case):
    def change(fields):
        rows = fields["conditional_count_profile"]
        if case == "denominator_mismatch":
            rows[0]["condition_denominator_support"] += 1
        elif case == "support_exceeds_risk":
            fields["eligible_joint_risk_total"] = 1
        elif case == "positive_zero_state":
            cell(fields)["joint_cell_state"] = "ZERO_SUPPORT"
        elif case == "zero_positive_state":
            cell(fields, 0, 1)["joint_cell_state"] = "OBSERVED_POSITIVE"
        elif case == "duplicate_target":
            cell(fields, 0, 1)["target_state"] = cell(fields, 0, 0)["target_state"]
        else:
            rows[0]["source_native_conditioner"] = "invented-native-role"
    result = CONS(mutation(change))
    assert result["decision_state"] == "CONSUMER_RELATION_INTEGRITY_REJECTED"
    assert not result["downstream_value_produced"]


@pytest.mark.parametrize("state,classification", [
    ("MISSING_TARGET_STATE", None), ("UNRESOLVED_TARGET_STATE", None),
    ("NONRESPONSE", None), ("ZERO_SUPPORT", "UNDETERMINED_ZERO_SUPPORT_RISK"),
])
def test_blocking_typed_state_never_valid_empty(state, classification):
    def change(fields):
        fields["typed_state"] = state
        fields["producer_state_blocking"] = True
        fields["conditional_count_profile"] = ()
    result = CONS(mutation(change))
    assert result["decision_state"] == "CONSUMER_PRODUCER_TYPED_STATE_BLOCKING"
    assert result["producer_typed_state"] == state
    assert result["separation_class"] == classification
    assert result["downstream_value_produced"] is False


def test_no_eligible_vs_eligible_zero_supported_are_distinct():
    no_risk = gf1g._rebuild(counts={}, eligible=0)
    zero_support = gf1g._rebuild(counts={}, eligible=2,
                                 zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    a, b = CONS(no_risk), CONS(zero_support)
    assert a["separation_class"] == "UNDETERMINED_NO_ELIGIBLE_RISK"
    assert b["separation_class"] == "UNDETERMINED_ZERO_SUPPORT_RISK"
    assert a["result_hash"] != b["result_hash"]


def test_blocked_relation_cannot_hide_invalid_risk_count():
    def change(fields):
        fields["typed_state"] = "NONRESPONSE"
        fields["producer_state_blocking"] = True
        fields["conditional_count_profile"] = ()
        fields["eligible_joint_risk_total"] = True
    result = CONS(mutation(change))
    assert result["decision_state"] == "CONSUMER_RELATION_INTEGRITY_REJECTED"
    assert result["separation_class"] is None


def test_reverse_role_requires_separate_grant_and_is_noncopy():
    row = next(r for r in gf1g.ORACLE["genuine_native_relations"]["BASELINE"]
               if r["consumer_kind"] == "QUERY"
               and r["roles"]["CONDITIONER"]["source_native_variable"] == "m01-X")
    forward = gf1g.gen_for("BASELINE", row["work_key"])
    reverse = gf1g.gen_for("BASELINE", row["work_key"], reverse=True)
    item = next(i for i in gf1g.items("BASELINE") if i["work_key"] == row["work_key"])
    with pytest.raises(G.GenericNativePairError, match="REVERSE_PAIR_GRANT_REQUIRED"):
        G.produce_generic_native_pair_relation(
            joint_fact=item["fact"], joint_query=item["query"],
            conditioner_ref=item["query"].target_refs[1],
            target_ref=item["query"].target_refs[0],
            producer_permission_ceiling=("SOURCE_FREE_DEV",))
    result = CONS(forward)
    reverse_result = CONS(reverse)
    assert result["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert "separation_signature" not in forward.semantic_projection()
    assert result["read_relation_content_hash"] == forward.content_hash
    assert reverse_result["read_relation_content_hash"] == reverse.content_hash
    assert forward.content_hash != reverse.content_hash
    assert result["operation_role_order"] == "FORWARD_NATIVE_ORDER"
    assert reverse_result["operation_role_order"] == "REVERSE_GRANTED"
    assert result["production_owner_commit"] is False


def test_self_rehashed_forged_source_stays_test_only():
    forged = mutation(lambda fields: fields.update(producer_provenance_refs=()))
    result = CONS(forged)
    assert result["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert result["generic_native_semantics_hold"] == "RETAINED"
    assert result["production_owner_commit"] is False
