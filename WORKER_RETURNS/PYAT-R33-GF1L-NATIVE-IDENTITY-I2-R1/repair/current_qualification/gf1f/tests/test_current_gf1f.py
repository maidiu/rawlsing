"""Current GF1F successor: user-authorized reconciliation, not frozen original.
Original source at 3dcc7d7 remains untouched. Four assertion/fixture successors
are explained in the six-failure crosswalk. All other checks are inherited.
"""
import json
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

import gf1_pair_support_consumer as C
import generic_native_pair_relation as R
from independent_relation import build_relation, cells_of

RET = Path(__file__).resolve().parents[1]
ORACLE = json.loads((RET / "01_CURRENT_PAIR_ORACLE.json").read_text())
COLD = RET / "repro" / "cold_child.py"

F2_FIELDS = ORACLE["f2_non_copy_fields"]


# ---------------------------------------------------------------- universe
@pytest.mark.parametrize("row", ORACLE["universe"],
                         ids=lambda r: "%d%d%d%d" % (r["cells"]["00"], r["cells"]["01"],
                                                     r["cells"]["10"], r["cells"]["11"]))
def test_universe_class_and_derived_fields(row):
    cells = row["cells"]
    rel = build_relation(cells, eligible=row["eligible"])
    out = C.compute_pair_support_signature(rel)
    assert out["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert out["separation_class"] == row["expected_class"]
    assert out["support_vectors"] == row["expected_support_vectors"]
    assert out["joint_support_total"] == row["expected_joint_support_total"]
    assert out["condition_states_with_positive_denominator"] == row["expected_positive_denominator"]
    # result_hash deterministic and content-bound
    assert out["result_hash"] == C.compute_pair_support_signature(rel)["result_hash"]
    assert len(out["result_hash"]) == 64


@pytest.mark.parametrize("name", sorted(ORACLE["named_cases"]))
def test_named_cases(name):
    case = ORACLE["named_cases"][name]
    cells = {k: case[k] for k in ("00", "01", "10", "11")}
    rel = build_relation(cells, eligible=case["eligible"])
    out = C.compute_pair_support_signature(rel)
    assert out["separation_class"] == case["expected_class"]


# ---------------------------------------------------------------- F2 non-copy
def test_f2_consumer_fields_are_not_copied_relation_fields():
    rel = build_relation(cells_of(1, 0, 0, 1))
    material = rel.as_dict()
    for field in F2_FIELDS:
        assert field not in material, field
    out = C.compute_pair_support_signature(rel)
    for field in F2_FIELDS:
        assert field in out, field


# ---------------------------------------------------------------- mutations
def _assert_constructor_rejects(**changes):
    base = build_relation(cells_of(1, 0, 0, 1))
    fields = dict(base.__dict__)
    fields.update(changes)
    with pytest.raises(R.GenericNativePairError):
        R.GenericNativePairRelation(**fields)


def test_mutation_object_id_without_recompute_rejected():
    _assert_constructor_rejects(object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + "0" * 64)


def test_mutation_content_hash_without_recompute_rejected():
    _assert_constructor_rejects(content_hash="0" * 64)


def test_mutation_one_cell_without_recompute_rejected():
    base = build_relation(cells_of(1, 0, 0, 1))
    profile = json.loads(json.dumps(list(base.conditional_count_profile)))
    profile[0]["target_counts"][0]["joint_support_count"] = 5
    _assert_constructor_rejects(conditional_count_profile=tuple(profile))


def test_mutation_risk_denominator_without_recompute_rejected():
    _assert_constructor_rejects(eligible_joint_risk_total=99)


def test_mutation_role_order_without_recompute_rejected():
    _assert_constructor_rejects(operation_role_order="REVERSE_GRANTED")


def test_bypass_frozen_mutation_is_identity_refused_by_consumer():
    rel = build_relation(cells_of(1, 0, 0, 1))
    object.__setattr__(rel, "eligible_joint_risk_total", 99)
    out = C.compute_pair_support_signature(rel)
    assert out["decision_state"] == "CONSUMER_RELATION_IDENTITY_MISMATCH"
    assert out["downstream_value_produced"] is False


def test_non_relation_input_refused():
    assert C.compute_pair_support_signature({"nope": 1})["decision_state"] == \
        "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"


def test_missing_suppressed_relation_remains_typed_blocking():
    rel = build_relation(cells_of(0, 0, 0, 0), typed_state="MISSING_TARGET_STATE")
    out = C.compute_pair_support_signature(rel)
    assert out["decision_state"] == "CONSUMER_PRODUCER_TYPED_STATE_BLOCKING"
    assert out["producer_typed_state"] == "MISSING_TARGET_STATE"
    assert out["separation_class"] is None
    assert out["downstream_value_produced"] is False


# ---------------------------------------------------------------- role direction
def test_reverse_xy_relation_is_a_distinct_operation():
    """The reverse is produced by the real producer under its own grant, and the
    consumer computes from the ordered profile of whichever relation it receives."""
    import gf1_bootstrap as GB
    import gf1_native as N
    from generic_native_pair_relation import (
        produce_generic_native_pair_relation as PRODUCE, REVERSE_PAIR_GRANT_ID)

    bundle = N.run_native(profile="BASELINE", root=GB.RT / "gf1f_reverse")
    items, _ = N.collect_link_material(bundle)
    item = [it for it in items if it["kind"] == "QUERY"][0]
    fwd = PRODUCE(joint_fact=item["fact"], joint_query=item["query"],
                  conditioner_ref=item["query"].target_refs[0],
                  target_ref=item["query"].target_refs[1],
                  producer_permission_ceiling=("SOURCE_FREE_DEV",))
    rev = PRODUCE(joint_fact=item["fact"], joint_query=item["query"],
                  conditioner_ref=item["query"].target_refs[1],
                  target_ref=item["query"].target_refs[0],
                  producer_permission_ceiling=("SOURCE_FREE_DEV",),
                  reverse_pair_grant=REVERSE_PAIR_GRANT_ID)
    assert rev.operation_role_order == "REVERSE_GRANTED"
    assert fwd.operation_role_order == "FORWARD_NATIVE_ORDER"
    of, orv = C.compute_pair_support_signature(fwd), C.compute_pair_support_signature(rev)
    # both are computed from their own ordered profile; neither is a fixture echo
    assert of["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert orv["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert of["separation_signature"] != orv["separation_signature"]
    assert of["result_hash"] != orv["result_hash"]


# ---------------------------------------------------------------- cold replay
def test_cold_process_consumer_replay_bit_identical():
    outs = []
    for i in range(2):
        dest = RET / "observations" / ("gf1f_cold_%d.json" % i)
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(COLD), str(dest)], check=True,
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        outs.append(json.loads(dest.read_text()))
    assert len({o["pid"] for o in outs}) == 2
    assert json.dumps(outs[0]["results"], sort_keys=True) == \
        json.dumps(outs[1]["results"], sort_keys=True)
    assert outs[0]["consumer_file"].endswith("gf1_pair_support_consumer.py")
    # every universe class is exercised in the cold process
    assert set(outs[0]["class_counts"]) == set(ORACLE["cold_class_counts"])

    assert outs[0]["class_counts"] == ORACLE["cold_class_counts"]
    expected = {"%d%d%d%d" % tuple(row["cells"][key] for key in ("00","01","10","11")): row["expected_class"] for row in ORACLE["universe"]}
    expected.update({row["case_id"]: row["expected_class"] for row in ORACLE["cold_extra_cases"]})
    assert outs[0]["results"] == expected
    assert outs[0]["consumer_sha256"] == os.environ["GF1_CURRENT_EXPECTED_CONSUMER_SHA256"]
    assert outs[1]["consumer_sha256"] == outs[0]["consumer_sha256"]


def test_true_supported_empty_profile_remains_valid_empty():
    base = build_relation(cells_of(0,0,0,0), eligible=0)
    fields = dict(base.__dict__)
    fields.pop("content_hash"); fields.pop("object_id")
    fields["conditional_count_profile"] = ()
    digest = R.semantic_hash(R._projection(fields))
    rel = R.GenericNativePairRelation(**fields,content_hash=digest,object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:"+digest)
    out = C.compute_pair_support_signature(rel)
    assert out["decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    assert out["separation_class"] is None
    assert out["downstream_value_produced"] is False


def test_no_risk_and_positive_risk_without_support_are_distinct():
    zero = cells_of(0,0,0,0)
    a = C.compute_pair_support_signature(build_relation(zero,eligible=0))
    b = C.compute_pair_support_signature(build_relation(zero,eligible=2))
    assert a["separation_class"] == "UNDETERMINED_NO_ELIGIBLE_RISK"
    assert b["separation_class"] == "UNDETERMINED_ZERO_SUPPORT_RISK"
    assert a["result_hash"] != b["result_hash"]
