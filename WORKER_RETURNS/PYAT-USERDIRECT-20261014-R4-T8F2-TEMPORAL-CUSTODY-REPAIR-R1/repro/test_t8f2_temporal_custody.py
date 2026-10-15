"""T8F2 tests: all 16 T8I frozen hostiles + required extras against repaired custody."""
import sys
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

import t8f2_temporal_custody as m


def resign(p):
    p = dict(p)
    p["product_digest"] = None
    p["product_digest"] = m.digest(p)
    return p


def reg_pair():
    reg = m.WaveFactRegistry()
    a, b = m.fixtures()
    ra = reg.register(a)
    rb = reg.register(b)
    return reg, ra, rb


def product():
    reg, ra, rb = reg_pair()
    return reg, m.compare_registered(reg, ra, rb)


def must_refuse(fn, expected=None):
    with pytest.raises(m.Refusal) as exc:
        fn()
    if expected:
        assert exc.value.code == expected


def test_control_original_valid_product_consumes():
    reg, p = product()
    c = m.consume_registered(reg, p)
    assert c["selected_numeric_temporal_value"] == p["delta_later_minus_earlier"]
    assert c["historical_intervening"] == "NATIVE_ANCHOR_ONLY"


def test_control_stale_delta_digest_refused():
    reg, p = product()
    p["delta_later_minus_earlier"] = F(999)
    must_refuse(lambda: m.consume_registered(reg, p), "PRODUCT_DIGEST_MISMATCH")


def test_control_stale_native_category_digest_refused():
    reg, p = product()
    p["later"]["categories"]["3"] += F(5)
    must_refuse(lambda: m.consume_registered(reg, p), "PRODUCT_DIGEST_MISMATCH")


def test_control_rehashed_native_category_unbalanced_share_refused():
    reg, p = product()
    p["later"]["categories"]["3"] += F(5)
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "NATIVE_CATEGORY_VALUE_MISMATCH")


def test_control_malformed_asof_typed():
    reg, ra, rb = reg_pair()
    must_refuse(lambda: m.compare_registered(reg, ra, rb, asof="not-a-date"), "INVALID_ASOF_DATE")
    reg2, p = product()
    must_refuse(lambda: m.consume_registered(reg2, p, asof="not-a-date"), "MIXED_ASOF_POLICY")
    p["query_asof"] = "not-a-date"
    must_refuse(lambda: m.consume_registered(reg2, resign(p), asof="not-a-date"), "INVALID_ASOF_DATE")


def test_control_native_category_zero_and_nonresponse_and_gap():
    reg, ra, rb = reg_pair()
    p = m.compare_registered(reg, ra, rb, historical_year=2017)
    assert sorted(p["earlier"]["categories"]) == ["0", "1", "2", "3", "4"]
    assert sorted(p["earlier"]["specials"]) == ["DK", "MISSING", "NOT_ASKED", "REFUSED"]
    assert p["earlier"]["refusal_native_code"] == 998 and p["later"]["refusal_native_code"] == 8
    assert p["earlier"]["eligible_weight"] == p["earlier"]["asked_weight"] + p["earlier"]["specials"]["NOT_ASKED"]
    assert p["later"]["eligible_weight"] == p["later"]["asked_weight"] + p["later"]["specials"]["NOT_ASKED"]
    assert m.consume_registered(reg, p)["historical_intervening"] == "UNKNOWN_UNOBSERVED_GAP"
    must_refuse(lambda: m.compare_registered(reg, ra, rb, asof="2024-09-30"), "HISTORICAL_ASOF_BEFORE_RELEASE")
    must_refuse(lambda: m.compare_registered(reg, ra, rb, ee12="ACTUAL_ISSUED"), "UNISSUED_EE12")
    must_refuse(lambda: m.consume_registered(reg, p, claim_same_person=True), "FALSE_SAME_PERSON_INFERENCE")


def test_red_registry_distinct_valid_variance_no_identity_collision():
    a, _ = m.fixtures()
    altered = replace(a, variance=F(1, 1250))
    assert a.variance != altered.variance
    assert a.content_hash() != altered.content_hash()


def test_red_registry_old_ref_retains_original_fact():
    a, _ = m.fixtures()
    reg = m.WaveFactRegistry()
    old = reg.register(a)
    newer = reg.register(replace(a, variance=F(1, 1250)))
    assert old != newer
    assert reg.retrieve(old).variance == a.variance


def test_red_wave_ref_year_bound_to_fact():
    reg, ra, rb = reg_pair()
    forged = replace(ra, year=2022)
    must_refuse(lambda: reg.retrieve(forged), "FACT_YEAR_MISMATCH")


def test_red_mutable_category_list_defensively_copied_on_registration():
    a, _ = m.fixtures()
    aliased = list(a.category_weights)
    mutable = replace(a, category_weights=aliased)
    reg = m.WaveFactRegistry()
    ref = reg.register(mutable)
    aliased[0] += F(1)
    assert reg.retrieve(ref).category_weights[0] == a.category_weights[0]


def test_red_self_resigned_forged_delta_refused():
    reg, p = product()
    p["delta_later_minus_earlier"] = F(999)
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "TEMPORAL_DELTA_ARITHMETIC_MISMATCH")


def test_red_self_resigned_forged_variance_delta_refused():
    reg, p = product()
    p["variance_delta_independent"] = F(999)
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "VARIANCE_DELTA_ARITHMETIC_MISMATCH")


def test_red_consistent_numerical_source_rewrite_refused_without_verified_refs():
    reg, p = product()
    q = p["later"]
    q["categories"]["3"] += F(5)
    q["valid_weight"] += F(5)
    q["asked_weight"] += F(5)
    q["eligible_weight"] += F(5)
    q["satisfied_share"] = (q["categories"]["3"] + q["categories"]["4"]) / sum(q["categories"].values())
    p["delta_later_minus_earlier"] = q["satisfied_share"] - p["earlier"]["satisfied_share"]
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "NATIVE_CATEGORY_VALUE_MISMATCH")


def test_red_rewritten_historical_publication_and_asof_refused():
    reg, p = product()
    p["later"]["publication"] = "2000-01-01"
    p["query_asof"] = "2001-01-01"
    must_refuse(lambda: m.consume_registered(reg, resign(p), asof="2001-01-01"), "SOURCE_PUBLICATION_CLOCK_MISMATCH")


def test_red_rewritten_eligible_risk_refused():
    reg, p = product()
    p["later"]["eligible_weight"] += F(30)
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "ELIGIBLE_RISK_DENOMINATOR_MISMATCH")


def test_red_forged_semantics_native_code_omission_refused():
    reg, p = product()
    del p["earlier"]["categories"]["0"]
    p["earlier"]["satisfied_share"] = (p["earlier"]["categories"]["3"] + p["earlier"]["categories"]["4"]) / sum(
        p["earlier"]["categories"].values())
    p["delta_later_minus_earlier"] = p["later"]["satisfied_share"] - p["earlier"]["satisfied_share"]
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "NATIVE_CATEGORY_ZERO_MISSING")


def test_extra_revoked_permission_refused_at_read():
    reg, ra, rb = reg_pair()
    p = m.compare_registered(reg, ra, rb)
    reg.revoke(rb)
    must_refuse(lambda: m.consume_registered(reg, p), "FACT_REVOKED")


def test_extra_version_downgrade_rejected():
    a, b = m.fixtures()
    reg = m.WaveFactRegistry()
    ra = reg.register(a)
    with pytest.raises(m.Refusal):
        reg.register(replace(b, version="OLD_VERSION"))


def test_extra_variance_change_targeted_invalidation():
    reg, ra, rb = reg_pair()
    p1 = m.compare_registered(reg, ra, rb)
    c1 = m.consume_registered(reg, p1)
    a, b = m.fixtures()
    reg2 = m.WaveFactRegistry()
    ra2 = reg2.register(replace(a, variance=F(1, 1250)))
    rb2 = reg2.register(b)
    p2 = m.compare_registered(reg2, ra2, rb2)
    c2 = m.consume_registered(reg2, p2)
    assert c1["values_read"]["variance_delta"] != c2["values_read"]["variance_delta"]
    assert c1["selected_numeric_temporal_value"] == c2["selected_numeric_temporal_value"]


def test_extra_self_declared_authority_rejected():
    reg, p = product()
    p["registry_authority"] = "SELF_DECLARED_AUTHORITY"
    must_refuse(lambda: m.consume_registered(reg, resign(p)), "UNVERIFIED_SOURCE_VALUE_OR_REF")


def test_extra_unrelated_input_stable():
    reg, ra, rb = reg_pair()
    p1 = m.compare_registered(reg, ra, rb)
    c1 = m.consume_registered(reg, p1)
    a, b = m.fixtures()
    reg2 = m.WaveFactRegistry()
    ra2 = reg2.register(replace(a, variance=F(1, 1250)))
    rb2 = reg2.register(b)
    p2 = m.compare_registered(reg2, ra2, rb2)
    assert p2["delta_later_minus_earlier"] == p1["delta_later_minus_earlier"]
