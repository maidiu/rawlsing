"""PYAT R2 T8F -- Tests for temporal integrity repair.

Covers the three T8R REDs and preserves original T8C test expectations.
"""

import sys
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

from t8f_temporal_integrity import (
    WaveFact, WaveFactRegistry, WaveFactRef,
    compare, consume, fixtures, Refusal, digest, canonical,
)


# --- Three T8R integrity repairs ---

def test_reject_tampered_delta_with_stale_digest():
    a, b = fixtures()
    p = compare(a, b)
    changed = deepcopy(p)
    changed["delta_later_minus_earlier"] = F(999)
    with pytest.raises(Refusal, match="PRODUCT_DIGEST_MISMATCH"):
        consume(changed)


def test_reject_tampered_native_category_with_stale_digest():
    a, b = fixtures()
    p = compare(a, b)
    changed = deepcopy(p)
    changed["later"]["categories"]["0"] = F(999)
    with pytest.raises(Refusal):
        consume(changed)


def test_typed_refusal_on_invalid_asof():
    a, b = fixtures()
    with pytest.raises(Refusal, match="INVALID_ASOF_DATE"):
        compare(a, b, asof="not-a-date")


# --- Original 19 T8C tests preserved ---

def test_valid_fixture_passes():
    a, b = fixtures()
    a.validate()
    b.validate()


def test_compare_produces_delta():
    a, b = fixtures()
    p = compare(a, b)
    assert p["delta_later_minus_earlier"] is not None
    assert p["product_digest"] != ""


def test_delta_arithmetic_correct():
    a, b = fixtures()
    p = compare(a, b)
    den_a = sum(a.category_weights)
    den_b = sum(b.category_weights)
    share_a = (a.category_weights[3] + a.category_weights[4]) / den_a
    share_b = (b.category_weights[3] + b.category_weights[4]) / den_b
    assert p["delta_later_minus_earlier"] == share_b - share_a


def test_ghana_native_category_zero_preserved():
    a, b = fixtures()
    assert a.native_category_codes == (0, 1, 2, 3, 4)
    assert b.native_category_codes == (0, 1, 2, 3, 4)
    assert a.category_weights[0] > 0
    assert b.category_weights[0] > 0


def test_independently_sampled_waves():
    a, b = fixtures()
    assert a.sample_identity == "INDEPENDENT_CROSS_SECTION_TEST_ONLY"
    assert b.sample_identity == "INDEPENDENT_CROSS_SECTION_TEST_ONLY"


def test_missing_refusal_distinctions():
    a, b = fixtures()
    assert a.refusal_code == 998
    assert b.refusal_code == 8
    assert len(a.special_weights) == 4
    assert len(b.special_weights) == 4


def test_unknown_2017_gap():
    a, b = fixtures()
    p = compare(a, b, historical_year=2017)
    assert p["historical_intervening"] == "UNKNOWN_UNOBSERVED_GAP"


def test_consume_returns_values():
    a, b = fixtures()
    p = compare(a, b)
    c = consume(p)
    assert c["selected_numeric_temporal_value"] == p["delta_later_minus_earlier"]
    assert c["values_read_digest"] != ""


def test_product_digest_verifies():
    a, b = fixtures()
    p = compare(a, b)
    c = consume(p)
    assert c["values_read_digest"] != p["product_digest"]


def test_no_same_person_inference():
    a, b = fixtures()
    p = compare(a, b)
    with pytest.raises(Refusal, match="FALSE_SAME_PERSON_INFERENCE"):
        consume(p, claim_same_person=True)


def test_no_n8s_laundering():
    a, b = fixtures()
    p = compare(a, b)
    with pytest.raises(Refusal, match="N8S_OR_CAUSAL_LAUNDERING"):
        consume(p, selected_context="OBJECTIVE_INSTITUTION")


def test_unissued_ee12_rejected():
    a, b = fixtures()
    with pytest.raises(Refusal, match="UNISSUED_EE12"):
        compare(a, b, ee12="REAL_EE12")


def test_temporal_inversion_rejected():
    a, b = fixtures()
    with pytest.raises(Refusal, match="TEMPORAL_INVERSION"):
        compare(b, a)


def test_population_mismatch_rejected():
    a, b = fixtures()
    bad_a = replace(a, population="DIFFERENT")
    with pytest.raises(Refusal):
        compare(bad_a, b)


def test_historical_time_unauthorized():
    a, b = fixtures()
    with pytest.raises(Refusal, match="HISTORICAL_TIME_UNAUTHORIZED"):
        compare(a, b, historical_year=2025)


def test_mixed_asof_rejected():
    a, b = fixtures()
    p = compare(a, b, asof="2025-06-01")
    with pytest.raises(Refusal, match="MIXED_ASOF_POLICY"):
        consume(p, asof="2025-01-01")


def test_zero_valid_support_rejected():
    a, b = fixtures()
    bad_a = replace(a, category_weights=(F(0), F(0), F(0), F(0), F(0)))
    with pytest.raises(Refusal):
        bad_a.validate()


def test_ghana_r5_r9_question_match():
    a, b = fixtures()
    assert a.question == "Q43"
    assert b.question == "Q31"
    assert a.version == "GHA_R5_2012_INSTRUMENT_TEST"
    assert b.version == "GHA_R9_2022_INSTRUMENT_TEST"


# --- Content-addressed registry tests ---

def test_registry_register_and_retrieve():
    reg = WaveFactRegistry()
    a, b = fixtures()
    ref_a = reg.register(a)
    ref_b = reg.register(b)
    assert ref_a.content_hash != ref_b.content_hash
    fact = reg.retrieve(ref_a)
    assert fact.year == 2012
    assert fact.content_hash() == ref_a.content_hash


def test_registry_rejects_tampered_ref():
    reg = WaveFactRegistry()
    a, _ = fixtures()
    ref = reg.register(a)
    bad_ref = WaveFactRef(ref_id=ref.ref_id, content_hash="0" * 64, year=ref.year)
    with pytest.raises(Refusal, match="FACT_HASH_MISMATCH"):
        reg.retrieve(bad_ref)


def test_registry_revalidate():
    reg = WaveFactRegistry()
    a, _ = fixtures()
    ref = reg.register(a)
    assert reg.revalidate(ref) is True


# --- Numerical change propagation ---

def test_numerical_change_propagates_to_consumer():
    a, b = fixtures()
    p1 = compare(a, b)
    c1 = consume(p1)
    b_changed = replace(b, category_weights=(F(3), F(15), F(30), F(35), F(27)))
    p2 = compare(a, b_changed)
    c2 = consume(p2)
    assert c1["selected_numeric_temporal_value"] != c2["selected_numeric_temporal_value"]
    assert c1["values_read_digest"] != c2["values_read_digest"]


def test_unrelated_input_stable():
    a, b = fixtures()
    p1 = compare(a, b)
    c1 = consume(p1)
    a_changed = replace(a, variance=F(1, 3000))
    p2 = compare(a_changed, b)
    c2 = consume(p2)
    assert c1["selected_numeric_temporal_value"] == c2["selected_numeric_temporal_value"]


def test_no_invented_ghana_trend():
    a, b = fixtures()
    p = compare(a, b)
    assert p["measured_original_data"] is False
    assert p["issued_EE12"] is False
    assert p["N8S"] == "NOT_APPLICABLE_SUBJECTIVE_REPORTS"


def test_wave_one_only_change():
    a, b = fixtures()
    p1 = compare(a, b)
    c1 = consume(p1)
    a_changed = replace(a, category_weights=(F(12), F(20), F(25), F(28), F(15)))
    p2 = compare(a_changed, b)
    c2 = consume(p2)
    assert c1["selected_numeric_temporal_value"] != c2["selected_numeric_temporal_value"]


def test_version_downgrade_rejected():
    a, b = fixtures()
    bad_b = replace(b, version="OLD_VERSION")
    with pytest.raises(Refusal):
        compare(a, bad_b)
