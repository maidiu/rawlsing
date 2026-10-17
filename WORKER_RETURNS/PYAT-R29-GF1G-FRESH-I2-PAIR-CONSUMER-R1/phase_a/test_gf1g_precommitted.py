"""GF1G Phase A PRECOMMITTED tests — frozen BEFORE GF1E inspection.

Runs against whichever court is staged at $GF1G_COURT (an R17 return directory
extracted from the verified commit). It imports the producer and the consumer
from that court; it does not import the GF1G reference consumer.

These tests are deliberately semantic: they pin the frozen classes, counts,
denominators, role identity, relation identity hashes and typed-refusal
behaviour, and they allow implementation-specific container shapes for
support_vectors as long as the semantic content is recoverable.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

COURT = Path(os.environ["GF1G_COURT"]).resolve()
ORACLE = json.loads(Path(os.environ["GF1G_ORACLE"]).read_text())
REPRO = COURT / "court" / "repro"
RT = COURT / "court" / "runtime_root"
os.chdir(REPRO)
sys.path[:0] = [str(REPRO), str(RT)]

import gf1_bootstrap as GB                                        # noqa: E402
import gf1_native as N                                            # noqa: E402
import generic_native_pair_relation as G                          # noqa: E402
from gf1_pair_support_consumer import compute_pair_support_signature as CONS  # noqa: E402

EXACT = "EXACT_PAIR_SEPARATION"
NO = "NO_PAIR_SEPARATION"
NO_RISK = "UNDETERMINED_NO_ELIGIBLE_RISK"
ZERO = "UNDETERMINED_ZERO_SUPPORT_RISK"

_BUNDLES: dict = {}
_ITEMS: dict = {}


def bundle(profile):
    if profile not in _BUNDLES:
        _BUNDLES[profile] = N.run_native(profile=profile,
                                         root=GB.RT / f"gf1g_pc_{profile.lower()}")
    return _BUNDLES[profile]


def items(profile):
    if profile not in _ITEMS:
        _ITEMS[profile] = N.collect_link_material(bundle(profile))[0]
    return _ITEMS[profile]


def gen_for(profile, work_key, reverse=False):
    it = next(i for i in items(profile) if i["work_key"] == work_key)
    if reverse:
        return G.produce_generic_native_pair_relation(
            joint_fact=it["fact"], joint_query=it["query"],
            conditioner_ref=it["query"].target_refs[1],
            target_ref=it["query"].target_refs[0],
            producer_permission_ceiling=("SOURCE_FREE_DEV",),
            reverse_pair_grant=G.REVERSE_PAIR_GRANT_ID)
    return G.produce_generic_native_pair_relation(
        joint_fact=it["fact"], joint_query=it["query"],
        conditioner_ref=it["query"].target_refs[0],
        target_ref=it["query"].target_refs[1],
        producer_permission_ceiling=("SOURCE_FREE_DEV",))


def cells(relation):
    out = {}
    for row in relation.conditional_count_profile:
        for t in row["target_counts"]:
            out[f"{row['condition_state']}{t['target_state']}"] = t["joint_support_count"]
    return out


def oracle_row(profile, work_key):
    return next(r for r in ORACLE["genuine_native_relations"][profile]
                if r["work_key"] == work_key)


def profile_rows(relation):
    return [(str(r["condition_state"]), int(r["condition_denominator_support"]),
             {str(t["target_state"]): int(t["joint_support_count"])
              for t in r["target_counts"]}) for r in relation.conditional_count_profile]


# ---------------------------------------------------------------- identity freeze
def test_g01_reference_reattest_74():
    assert GB.REATTESTED == 74


@pytest.mark.parametrize("profile", ["BASELINE", "R2_Y1", "R1_Y0"])
def test_g02_genuine_relation_identity_and_cells_exact(profile):
    for row in ORACLE["genuine_native_relations"][profile]:
        rel = gen_for(profile, row["work_key"])
        assert rel.content_hash == row["relation_content_hash"], (profile, row["work_key"])
        assert rel.object_id == row["relation_object_id"], (profile, row["work_key"])
        assert cells(rel) == row["cells_00_01_10_11"]
        assert profile_rows(rel) == [
            (r["condition_state"], r["condition_denominator_support"],
             {k: int(v) for k, v in r["targets"].items()})
            for r in row["conditional_profile"]]
        assert rel.eligible_joint_risk_total == row["eligible_joint_risk_total"]
        assert list(rel.relation_permission_ceiling) == ["SOURCE_FREE_DEV"]


def test_g03_reverse_identity_roles_and_grant():
    rev_row = ORACLE["reverse_x_given_y"]
    fwd_work_key = next(r["work_key"] for r in
                        ORACLE["genuine_native_relations"]["BASELINE"]
                        if r["relation_object_id"] == rev_row["forward_object_id"])
    fwd = gen_for("BASELINE", fwd_work_key)
    rev = gen_for("BASELINE", fwd_work_key, reverse=True)
    assert rev.content_hash == rev_row["relation_content_hash"]
    assert rev.operation_role_order == "REVERSE_GRANTED"
    assert rev.object_id != fwd.object_id
    assert rev.conditioner_source_native_variable == \
        fwd.target_source_native_variable
    assert rev.target_source_native_variable == \
        fwd.conditioner_source_native_variable
    assert cells(rev) == cells(fwd)


def test_g04_forward_relation_identity_binds_native_query():
    row = next(r for r in ORACLE["genuine_native_relations"]["BASELINE"]
               if r["consumer_kind"] == "QUERY"
               and r["roles"]["CONDITIONER"]["source_native_variable"] == "m01-X")
    rel = gen_for("BASELINE", row["work_key"])
    assert rel.conditioner_source_native_variable == "m01-X"
    assert rel.target_source_native_variable == "m01-Y"
    assert rel.operation_role_order == "FORWARD_NATIVE_ORDER"
    assert rel.content_hash == row["relation_content_hash"]


# ---------------------------------------------------------------- consumer classes
def test_g05_baseline_exact_separation_and_counts():
    row = next(r for r in ORACLE["genuine_native_relations"]["BASELINE"]
               if r["consumer_kind"] == "QUERY"
               and r["roles"]["CONDITIONER"]["source_native_variable"] == "m01-X")
    rel = gen_for("BASELINE", row["work_key"])
    res = CONS(rel)
    assert res["separation_class"] == EXACT
    assert res["joint_support_total"] == 2
    assert sorted(map(str, res["condition_states_with_positive_denominator"])) == ["0", "1"]
    assert res["read_relation_object_id"] == rel.object_id
    assert res["read_relation_content_hash"] == rel.content_hash
    assert res["generic_native_semantics_hold"] == "RETAINED"
    assert res["downstream_value_produced"] is True
    zs = res["zero_cell_semantics"]
    flat = json.dumps(zs)
    assert "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET" in flat
    assert "ZERO_SUPPORT" not in flat
    assert res["production_owner_commit"] is False
    assert res["is_population_evidence_not_actor_fact"] is True
    assert res["makes_no_causal_or_psychological_claim"] is True


def test_g06_interventions_match_frozen_classes_by_orientation():
    for profile in ("R2_Y1", "R1_Y0"):
        for row in ORACLE["genuine_native_relations"][profile]:
            if row["consumer_kind"] != "QUERY":
                continue
            rel = gen_for(profile, row["work_key"])
            res = CONS(rel)
            assert res["separation_class"] == row["consumer"]["separation_class"], \
                (profile, row["work_key"], res["separation_class"])
            assert res["joint_support_total"] == row["joint_support_total"]


def test_g07_discovery_is_distinct_risk_and_not_baseline():
    base_cells = next(r["cells_00_01_10_11"]
                      for r in ORACLE["genuine_native_relations"]["BASELINE"]
                      if r["consumer_kind"] == "QUERY")
    for row in ORACLE["genuine_native_relations"]["BASELINE"]:
        if row["consumer_kind"] != "DISCOVERY":
            continue
        rel = gen_for("BASELINE", row["work_key"])
        assert rel.eligible_joint_risk_total == 1
        assert cells(rel) != base_cells
        assert CONS(rel)["separation_class"] == row["consumer"]["separation_class"]


def test_g08_four_classes_present_in_oracle_semantics():
    classes = set()
    for rows in ORACLE["genuine_native_relations"].values():
        classes |= {r["consumer"]["separation_class"] for r in rows}
    for r in ORACLE["rehashed_test_only_relations"].values():
        classes.add(r["consumer"]["separation_class"])
    classes.discard(None)
    assert {EXACT, NO, NO_RISK, ZERO} <= classes


# ---------------------------------------------------------------- rehashed cases
TEMPLATE = None


def _template():
    global TEMPLATE
    if TEMPLATE is None:
        row = next(r for r in ORACLE["genuine_native_relations"]["BASELINE"]
                   if r["consumer_kind"] == "QUERY"
                   and r["roles"]["CONDITIONER"]["source_native_variable"] == "m01-X")
        TEMPLATE = gen_for("BASELINE", row["work_key"])
    return TEMPLATE


def _rebuild(*, counts, denoms=None, typed="SUPPORTED", eligible=2,
             zero_state="ZERO_SUPPORT"):
    t = _template()
    f = dict(t.__dict__)
    f.pop("content_hash")
    f.pop("object_id")
    if typed != "SUPPORTED":
        f["conditional_count_profile"] = ()
        f["typed_state"] = typed
        f["producer_state_blocking"] = True
        f["eligible_joint_risk_total"] = eligible
        d = G.semantic_hash(G._projection(f))
        return G.GenericNativePairRelation(
            **f, content_hash=d,
            object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")
    cdom = [str(c) for c in t.conditioner_domain]
    tdom = [str(x) for x in t.target_domain]
    rows = []
    for c in cdom:
        tcs = []
        for state in tdom:
            n = counts.get(f"{c}{state}", 0)
            tcs.append({
                "target_state": state,
                "source_native_target": t.target_source_native_variable,
                "joint_support_count": n,
                "joint_cell_state": "OBSERVED_POSITIVE" if n else zero_state,
            })
        rows.append({
            "condition_state": c,
            "source_native_conditioner": t.conditioner_source_native_variable,
            "condition_denominator_support": (denoms or {}).get(
                f"{c}", sum(x["joint_support_count"] for x in tcs)),
            "target_counts": tuple(tcs),
        })
    f["conditional_count_profile"] = tuple(rows)
    f["typed_state"] = typed
    f["producer_state_blocking"] = typed != "SUPPORTED"
    f["eligible_joint_risk_total"] = eligible
    d = G.semantic_hash(G._projection(f))
    return G.GenericNativePairRelation(
        **f, content_hash=d,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")


@pytest.mark.parametrize("name,expected", [
    ("collapsed_same_point_mass", NO),
    ("nontrivial_partial", NO),
    ("nontrivial_exact", EXACT),
    ("all_zero_observed_zero", ZERO),
    ("no_eligible_risk", NO_RISK),
])
def test_g09_synthetic_classes(name, expected):
    row = ORACLE["rehashed_test_only_relations"][name]
    assert row["consumer"]["separation_class"] == expected
    spec = {
        "collapsed_same_point_mass": dict(counts={"00": 1, "10": 1}),
        "nontrivial_partial": dict(counts={"00": 2, "01": 1, "10": 1, "11": 2},
                                   eligible=6),
        "nontrivial_exact": dict(counts={"00": 2, "11": 2}, eligible=4),
        "all_zero_observed_zero": dict(counts={}, eligible=2,
                                       zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"),
        "no_eligible_risk": dict(counts={}, eligible=0),
    }[name]
    rel = _rebuild(**spec)
    assert rel.content_hash == row["relation_content_hash"]
    assert CONS(rel)["separation_class"] == expected


@pytest.mark.parametrize("name", ["missing_target_state", "unresolved_target_state",
                                  "nonresponse"])
def test_g10_missing_unresolved_nonresponse_hold(name):
    row = ORACLE["rehashed_test_only_relations"][name]
    rel = _rebuild(counts={}, typed=row["typed_state"], eligible=0)
    res = CONS(rel)
    assert res["separation_class"] is None, res
    assert res["downstream_value_produced"] is False
    assert res["generic_native_semantics_hold"] == "RETAINED"


def test_g11_zero_support_typed_and_observed_zero():
    row = ORACLE["rehashed_test_only_relations"]["zero_support_typed"]
    rel = _rebuild(counts={}, typed="ZERO_SUPPORT", eligible=2)
    res = CONS(rel)
    assert res["separation_class"] == ZERO
    assert res["downstream_value_produced"] is False
    row2 = ORACLE["rehashed_test_only_relations"]["all_zero_observed_zero"]
    rel2 = _rebuild(counts={}, eligible=2,
                    zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    assert CONS(rel2)["separation_class"] == ZERO
    assert rel.content_hash == row["relation_content_hash"]
    assert rel2.content_hash == row2["relation_content_hash"]


@pytest.mark.parametrize("name", ["inconsistent_denominator", "support_exceeds_risk"])
def test_g12_inconsistent_denominator_and_risk_bound_typed_reject(name):
    row = ORACLE["rehashed_test_only_relations"][name]
    if name == "inconsistent_denominator":
        rel = _rebuild(counts={"00": 1, "11": 1}, denoms={"0": 2, "1": 1})
    else:
        rel = _rebuild(counts={"00": 1, "11": 1}, eligible=1)
    assert rel.content_hash == row["relation_content_hash"]
    res = CONS(rel)
    assert res["separation_class"] is None, res
    assert res["downstream_value_produced"] is False
    assert res["generic_native_semantics_hold"] == "RETAINED"


def test_g13_invalid_input_exact_contract_state():
    res = CONS({"nope": 1})
    assert res["decision_state"] == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"
    assert res["separation_class"] is None
    assert res["downstream_value_produced"] is False


def test_g14_empty_profile_contract_state():
    t = _template()
    f = dict(t.__dict__)
    f.pop("content_hash")
    f.pop("object_id")
    f["conditional_count_profile"] = ()
    d = G.semantic_hash(G._projection(f))
    empty = G.GenericNativePairRelation(
        **f, content_hash=d,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")
    res = CONS(empty)
    assert res["decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    assert res["downstream_value_produced"] is False


# ---------------------------------------------------------------- F2 / forgery
def test_g15_f2_no_copied_consumer_fields():
    row = next(r for r in ORACLE["genuine_native_relations"]["BASELINE"]
               if r["consumer_kind"] == "QUERY")
    rel = gen_for("BASELINE", row["work_key"])
    material = rel.as_dict()
    for k in ("separation_class", "separation_signature", "support_vectors",
              "zero_cell_semantics", "joint_support_total",
              "condition_states_with_positive_denominator", "result_hash"):
        assert k not in material
    res = CONS(rel)
    assert res["read_relation_object_id"] == material["object_id"]
    assert res["read_relation_content_hash"] == material["content_hash"]


def test_g16_result_hash_deterministic_and_semantically_sensitive():
    row = next(r for r in ORACLE["genuine_native_relations"]["BASELINE"]
               if r["consumer_kind"] == "QUERY")
    rel = gen_for("BASELINE", row["work_key"])
    a = CONS(rel)
    b = CONS(rel)
    assert a["result_hash"] == b["result_hash"]
    assert isinstance(a["result_hash"], str) and len(a["result_hash"]) == 64
    int(a["result_hash"], 16)
    other = _rebuild(counts={"00": 1, "10": 1})
    assert CONS(other)["result_hash"] != a["result_hash"]


def test_g17_fully_rehashed_self_authenticated_is_not_issuer_authenticated():
    """A consistent forged relation is indistinguishable structurally: the consumer
    MUST still refuse to grant real-source/production privilege."""
    base = _rebuild(counts={"00": 1, "11": 1}, eligible=2)
    f = dict(base.__dict__)
    f.pop("content_hash")
    f.pop("object_id")
    from rawlsing_next._pre553_query_common import ExactRef
    f["producer_provenance_refs"] = (
        ExactRef("GF1G_FORGED_PROVENANCE", "urn:gf1g:forged:provenance", "0" * 64),)
    f["producer_authority_refs"] = (
        ExactRef("GF1G_FORGED_AUTHORITY", "urn:gf1g:forged:authority", "0" * 64),)
    d = G.semantic_hash(G._projection(f))
    forged = G.GenericNativePairRelation(
        **f, content_hash=d,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")
    assert forged.content_hash == ORACLE["fully_rehashed_unauthenticated"]["relation_content_hash"]
    res = CONS(forged)
    assert res["separation_class"] == EXACT
    assert res["production_owner_commit"] is False
    assert res["generic_native_semantics_hold"] == "RETAINED"
    material = forged.as_dict()
    signature_fields = [k for k in material
                        if "signature" in k.lower() or "issuer" in k.lower()]
    assert signature_fields == [], \
        "no external issuer/signature field exists in the relation schema"
