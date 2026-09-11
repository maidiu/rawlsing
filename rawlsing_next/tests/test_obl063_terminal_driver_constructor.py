from decimal import Decimal
import hashlib
import pytest

from rawlsing_next.bounded_empirical_runtime import EvidenceTier, ExactRef
from rawlsing_next.obl063_terminal_driver_constructor import (
    ACTIVE_DRIVER_ORDER, BINDINGS, CONCEPTUAL_REGISTRY_ORDER, CONSTRUCTOR_ID,
    DIRECT_TRANSFORM, EXPLICIT_EMPTY_ACTIVE_DRIVERS, INVERSE_TRANSFORM,
    MATRIX_GIT_BLOB_SHA1, NORMALIZATION_ID, OWNER_LAW_GIT_BLOB_SHA1,
    PENDING_DRIVER_ORDER, POLICY_SEMANTIC_HASH, SELECTED_CHANNEL_IDS,
    SOFTMAX_TEMPERATURE, TYPE_IDS, TerminalChannelObservation,
    TerminalConstructorError, _load_and_validate_matrix, _load_and_validate_owner_law,
    _softmax, _transform_raw, build_driver_policies, construct_terminal_driver_vector,
    policy_manifest,
)


def h(tag): return hashlib.sha256(tag.encode()).hexdigest()
def ref(kind, tag): return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))

def obs(channel, value, tier=EvidenceTier.SOURCE_LOCAL_CERTIFIED):
    return TerminalChannelObservation(
        channel, value, tier,
        ref("SOURCE", channel) if tier is not EvidenceTier.UNAVAILABLE else None,
        ref("POP_AUTH", channel) if tier is EvidenceTier.POPULATION_CERTIFIED else None,
        False, False,
    )

def full_observations():
    return {
        "hofstede.Individualism": obs("hofstede.Individualism", "30"),
        "hofstede.PowerDistance": obs("hofstede.PowerDistance", "60"),
        "hofstede.UncertaintyAvoidance": obs("hofstede.UncertaintyAvoidance", "40"),
        "urban_pop_percent": obs("urban_pop_percent", "80"),
        "hofstede.LongTermOrientation": obs("hofstede.LongTermOrientation", "50"),
    }

def slot(result, driver): return next(x for x in result.driver_slots if x["driver_id"] == driver)


def test_01_exact_owner_and_matrix_content_pins_and_shape():
    owner, ore = _load_and_validate_owner_law()
    matrix, mre = _load_and_validate_matrix()
    assert ore["owner_law_git_blob_sha1"] == OWNER_LAW_GIT_BLOB_SHA1
    assert mre["matrix_git_blob_sha1"] == MATRIX_GIT_BLOB_SHA1
    assert owner["accepted_boundary"] == "EMPIRICAL_TO_DRIVER_VECTOR_PRE_V3"
    assert tuple(matrix) == ACTIVE_DRIVER_ORDER
    assert all(tuple(matrix[d]) == TYPE_IDS for d in ACTIVE_DRIVER_ORDER)


def test_02_exact_40_22_18_registry_topology():
    assert (len(CONCEPTUAL_REGISTRY_ORDER), len(ACTIVE_DRIVER_ORDER), len(PENDING_DRIVER_ORDER)) == (40, 22, 18)
    assert len(set(CONCEPTUAL_REGISTRY_ORDER)) == 40
    assert set(ACTIVE_DRIVER_ORDER).isdisjoint(PENDING_DRIVER_ORDER)
    assert CONCEPTUAL_REGISTRY_ORDER == ACTIVE_DRIVER_ORDER + PENDING_DRIVER_ORDER


def test_03_six_mapping_policy_uses_generic_obl063_optional_source_local_no_fallback():
    policies = build_driver_policies()
    assert tuple(policies) == tuple(BINDINGS)
    assert len(policies) == 6 and len(SELECTED_CHANNEL_IDS) == 5
    assert len(EXPLICIT_EMPTY_ACTIVE_DRIVERS) == 16
    for driver, (channel_id, _) in BINDINGS.items():
        p = policies[driver]
        assert p.allow_typed_no_numeric_driver is True and len(p.channels) == 1
        ch = p.channels[0]
        assert ch.channel_id == channel_id and ch.coefficient == Decimal("1.0")
        assert ch.required_for_runtime is False and ch.fallback is None
        assert ch.claim_ceiling.value == "SOURCE_LOCAL_STATISTIC"


def test_04_transform_contract_closed_domain_direct_inverse_no_clipping():
    assert _transform_raw("0", DIRECT_TRANSFORM) == (Decimal("0"), "TRANSFORM_ACCEPTED")
    assert _transform_raw("100", DIRECT_TRANSFORM) == (Decimal("1"), "TRANSFORM_ACCEPTED")
    assert _transform_raw("30", INVERSE_TRANSFORM) == (Decimal("0.7"), "TRANSFORM_ACCEPTED")
    assert _transform_raw("100", INVERSE_TRANSFORM) == (Decimal("0"), "TRANSFORM_ACCEPTED")
    for bad in ("-0.01", "100.01", "wat", True, None):
        assert _transform_raw(bad, DIRECT_TRANSFORM)[0] is None


def test_05_five_source_channels_yield_six_numeric_fixed_slots_and_sixteen_typed_missing():
    r = construct_terminal_driver_vector(full_observations())
    assert len(r.driver_slots) == 22
    assert tuple(x["driver_id"] for x in r.driver_slots) == ACTIVE_DRIVER_ORDER
    assert (r.driver_coverage_receipt["numeric_count"], r.driver_coverage_receipt["typed_no_numeric_count"]) == (6, 16)
    assert slot(r, "collectivism")["value"] == Decimal("0.7")
    assert slot(r, "hierarchy")["value"] == slot(r, "authorityStyle")["value"] == Decimal("0.6")
    assert slot(r, "tightness")["value"] == Decimal("0.4")
    assert slot(r, "urbanization")["value"] == Decimal("0.8")
    assert slot(r, "temporalOrientation")["value"] == Decimal("0.5")
    assert slot(r, "materialSecurity")["state"] == "TYPED_NO_NUMERIC" and slot(r, "materialSecurity")["value"] is None


def test_06_type_score_uses_exact_weights_without_missing_weight_renormalization():
    r = construct_terminal_driver_vector(full_observations())
    assert r.type_scores["t1"] == Decimal("1.47")
    assert r.driver_coverage_receipt["driver_weights_renormalized"] is False
    assert r.driver_coverage_receipt["coefficient_reallocated"] is False


def test_07_weaker_authority_is_not_promoted():
    r = construct_terminal_driver_vector({"hofstede.Individualism": obs("hofstede.Individualism", "25", EvidenceTier.PARTIAL_AUTHORITY)})
    c = slot(r, "collectivism")
    assert c["state"] == "TYPED_NO_NUMERIC" and c["value"] is None
    assert c["input_disposition"] == "INSUFFICIENT_SOURCE_LOCAL_AUTHORITY"
    assert r.terminal_status == "BLOCKED_ALL_ACTIVE_DRIVERS_NO_NUMERIC" and r.type_distribution is None


def test_08_population_certified_may_satisfy_source_local_use_and_source_ref_survives():
    r = construct_terminal_driver_vector({"hofstede.PowerDistance": obs("hofstede.PowerDistance", "55", EvidenceTier.POPULATION_CERTIFIED)})
    x = slot(r, "hierarchy")
    assert x["state"] == "NUMERIC"
    env = x["generic_runtime_envelope"]
    assert env["channel_decisions"][0]["evidence_tier"] == "POPULATION_CERTIFIED"
    assert env["effective_contributions"][0]["source_ref"]["content_hash"] == h("SOURCE:hofstede.PowerDistance")


def test_09_out_of_domain_is_typed_missing_not_numeric_zero():
    r = construct_terminal_driver_vector({"urban_pop_percent": obs("urban_pop_percent", "101")})
    u = slot(r, "urbanization")
    assert u["state"] == "TYPED_NO_NUMERIC" and u["value"] is None
    assert u["input_disposition"] == "OUT_OF_DOMAIN_0_100"
    encoded = next(x for x in r.as_dict()["driver_slots"] if x["driver_id"] == "urbanization")
    assert encoded["value"] is None and r.type_distribution is None


def test_10_all_missing_guard_emits_no_scores_or_distribution():
    r = construct_terminal_driver_vector({})
    assert r.driver_coverage_receipt["numeric_count"] == 0
    assert r.terminal_status == "BLOCKED_ALL_ACTIVE_DRIVERS_NO_NUMERIC"
    assert r.type_scores is None and r.type_distribution is None
    assert all(x["value"] is None for x in r.driver_slots)


def test_11_nonselected_channels_are_rejected_not_consumed():
    with pytest.raises(TerminalConstructorError, match="nonselected R1 terminal channels"):
        construct_terminal_driver_vector({"wvs7.V66": obs("wvs7.V66", "55")})


def test_12_softmax_fixed_temperature_one_never_legacy_minmax():
    assert NORMALIZATION_ID == "SOFTMAX" and SOFTMAX_TEMPERATURE == Decimal("1.0")
    p = _softmax({t: Decimal(i) for i, t in enumerate(TYPE_IDS)})
    assert all(x > 0 for x in p.values())
    assert abs(sum(p.values()) - Decimal("1")) < Decimal("1e-48")


def test_13_replay_byte_stable_across_observation_order():
    first = full_observations(); second = dict(reversed(list(first.items())))
    a = construct_terminal_driver_vector(first); b = construct_terminal_driver_vector(second)
    assert a.result_hash == b.result_hash and a.canonical_bytes() == b.canonical_bytes()


def test_14_constructor_policy_identity_is_versioned_content_addressed_and_no_renorm():
    m = policy_manifest()
    assert CONSTRUCTOR_ID == "RAWLSING_EMPIRICAL_TO_DRIVER_VECTOR_PRE_V3_R1@1.0.0"
    assert m["driver_weight_renormalization_on_missing"] is False
    assert m["coefficient_reallocation"] is False
    assert len(POLICY_SEMANTIC_HASH) == 64
    int(POLICY_SEMANTIC_HASH, 16)
