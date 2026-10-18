"""GF1K exact native-category identity hostiles against the REAL 74-module producer.

Reproduces GF1J's two REDs (condition_state / target_state integer 0 where the
native declared domain is the STRING "0") on the authoritative frozen
``GenericNativePairRelation``, then asserts GF1K's typed rejection and the
preservation of genuine string and integer domains without recoding.
"""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import os
from pathlib import Path

import pytest

COURT = Path(os.environ["GF1K_COURT"]).resolve()
GF1G = Path(os.environ["GF1K_GF1G"]).resolve()
os.environ["GF1G_COURT"] = str(COURT)
os.environ["GF1G_ORACLE"] = str(GF1G / "01_FROZEN_ORACLE.json")
spec = importlib.util.spec_from_file_location(
    "gf1g_fixture", GF1G / "phase_a/test_gf1g_precommitted.py")
gf1g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf1g)
G = gf1g.G
CONS = gf1g.CONS

INTEGRITY = "CONSUMER_RELATION_INTEGRITY_REJECTED"
IDENTITY = "CONSUMER_RELATION_IDENTITY_MISMATCH"


def rehash(fields):
    digest = G.semantic_hash(G._projection(fields))
    return G.GenericNativePairRelation(
        **fields, content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")


def clone(rel):
    fields = dict(rel.__dict__)
    fields.pop("content_hash")
    fields.pop("object_id")
    fields["conditional_count_profile"] = deepcopy(
        list(rel.conditional_count_profile))
    return fields


def assert_integrity(result):
    assert result["decision_state"] == INTEGRITY, result
    assert result["separation_class"] is None, result
    assert result["downstream_value_produced"] is False, result


# ------------------------------------------------------------ the two GF1J REDs
def test_gf1j_red1_conditioner_integer_spoofed():
    """GF1J RED1: condition_state = 0 (int) against declared string domain."""
    fields = clone(gf1g._template())
    fields["conditional_count_profile"][0]["condition_state"] = 0
    assert_integrity(CONS(rehash(fields)))


def test_gf1j_red2_target_integer_spoofed():
    """GF1J RED2: target_counts[0].target_state = 0 (int) against string domain."""
    fields = clone(gf1g._template())
    fields["conditional_count_profile"][0]["target_counts"][0]["target_state"] = 0
    assert_integrity(CONS(rehash(fields)))


# ------------------------------------------------------------ bool / int folding
@pytest.mark.parametrize("spoof", [False, 0.0, None, 1])
def test_bool_float_none_spoofed_conditioner(spoof):
    fields = clone(gf1g._template())
    fields["conditional_count_profile"][0]["condition_state"] = spoof
    assert_integrity(CONS(rehash(fields)))


def test_bool_is_not_integer_in_integer_domain():
    """A valid integer-native domain must reject bool keys, not fold bool==0."""
    fields = clone(gf1g._template())
    fields["conditioner_domain"] = (0, 1)
    fields["target_domain"] = (0, 1)
    rows = []
    for c in (0, 1):
        rows.append({
            "condition_state": c,
            "source_native_conditioner": fields["conditioner_source_native_variable"],
            "condition_denominator_support": 1,
            "target_counts": tuple(
                {"target_state": t,
                 "source_native_target": fields["target_source_native_variable"],
                 "joint_support_count": 1 if t == c else 0,
                 "joint_cell_state": "OBSERVED_POSITIVE" if t == c
                                      else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"}
                for t in (0, 1)),
        })
    fields["conditional_count_profile"] = rows
    ok = rehash(fields)
    assert CONS(ok)["separation_class"] == "EXACT_PAIR_SEPARATION"
    bad = deepcopy(rows)
    bad[0]["condition_state"] = False
    fields["conditional_count_profile"] = bad
    assert_integrity(CONS(rehash(fields)))


# ------------------------------------------------------------ order / swap
def test_swapped_condition_row_state_rejected():
    fields = clone(gf1g._template())
    fields["conditional_count_profile"][0]["condition_state"] = "1"
    assert_integrity(CONS(rehash(fields)))


def test_target_domain_ordering_rejected():
    fields = clone(gf1g._template())
    row = fields["conditional_count_profile"][0]
    row["target_counts"] = (row["target_counts"][1], row["target_counts"][0])
    assert_integrity(CONS(rehash(fields)))


# ------------------------------------------------------------ genuine integer domain
def test_valid_native_integer_domain_computed_without_recoding():
    """Genuine integer-native domains and row/target keys must be accepted."""
    fields = clone(gf1g._template())
    fields["conditioner_domain"] = (0, 1)
    fields["target_domain"] = (0, 1)
    rows = []
    for c in (0, 1):
        rows.append({
            "condition_state": c,
            "source_native_conditioner": fields["conditioner_source_native_variable"],
            "condition_denominator_support": 1,
            "target_counts": tuple(
                {"target_state": t,
                 "source_native_target": fields["target_source_native_variable"],
                 "joint_support_count": 1 if t == c else 0,
                 "joint_cell_state": "OBSERVED_POSITIVE" if t == c
                                      else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"}
                for t in (0, 1)),
        })
    fields["conditional_count_profile"] = rows
    result = CONS(rehash(fields))
    assert result["separation_class"] == "EXACT_PAIR_SEPARATION", result
    assert result["joint_support_total"] == 2
    assert set(map(int, result["condition_states_with_positive_denominator"])) == {0, 1}


# ------------------------------------------------------------ identity / regression
def test_spoofed_relations_are_legitimate_self_rehashed_instances():
    """The two REDs are valid self-rehashed relations, not hash collisions."""
    for mutate in ("conditioner", "target"):
        fields = clone(gf1g._template())
        if mutate == "conditioner":
            fields["conditional_count_profile"][0]["condition_state"] = 0
        else:
            fields["conditional_count_profile"][0]["target_counts"][0]["target_state"] = 0
        rel = rehash(fields)
        assert rel.content_hash == G.semantic_hash(rel.semantic_projection())
        assert rel.object_id == f"urn:rawlsing:gf1:generic-pair-relation:sha256:{rel.content_hash}"
        result = CONS(rel)
        assert result["decision_state"] == INTEGRITY, result


def test_genuine_baseline_still_computes_exact():
    result = CONS(gf1g._template())
    assert result["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert result["separation_class"] == "EXACT_PAIR_SEPARATION"
