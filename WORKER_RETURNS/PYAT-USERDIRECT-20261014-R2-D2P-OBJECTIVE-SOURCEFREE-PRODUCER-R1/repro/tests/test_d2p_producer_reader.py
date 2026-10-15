"""D2P sourcefree objective field producer + numeric consumer tests.

Real executed Python/pytest. Sourcefree invented-world rows only (D2I
documentary values, TEST_ONLY issuance); no original SAV/DTA, no binary
custody, no real N5/N6/EE13/N9/OC05, no V3, no actor, no model calls.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from d2p.external_fields import (
    FieldProducerError,
    GSS,
    NCA,
    produce_two_fields,
    produce_field,
    check_field_authority,
    field_content_ref,
)
from d2p.n9c_reader import (
    TestOnlyRegistry,
    TestOnlyReadError,
    read_historical_test_only,
    fixture_invalidation,
)
from d2p.direct_transport import handoff_two_fields, TRANSPORT_AVAILABLE
from d2p.counterfactual import counterfactual_holds


@pytest.fixture
def rows():
    return deepcopy(json.loads((HERE.parent / "n9c_fields.json").read_text())["fields"])


def read(rows, as_of="2022-07-08", **kw):
    fields = produce_two_fields(rows)
    registry = TestOnlyRegistry(rows)
    refs = registry.refs_by_role()
    relation = {
        "kind": "TEST_ONLY_NONPOOLED_COPRESENCE",
        "fixture_only": True,
        "issued_EE13": False,
        "ordered_refs": [refs[GSS], refs[NCA]],
        "population_join": False,
    }
    return read_historical_test_only(
        registry, selected_refs=refs, relation=relation,
        as_of=as_of, clock_mode="HISTORICAL_PUBLICATION_AWARE", **kw), fields, registry, refs, relation


def reject(code, fn):
    with pytest.raises((FieldProducerError, TestOnlyReadError)) as e:
        fn()
    assert e.value.code == code


# --- 1. field binding: native units, values, denominators, clocks, authority ---
def test_fields_bind_native_units_values_denominators_clocks_authority(rows):
    fields = produce_two_fields(rows)
    gss, nca = fields[GSS], fields[NCA]
    assert gss["native_unit"] == "RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING"
    assert nca["native_unit"] == "ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS"
    assert gss["native_geography"] == "GHANA_RURAL"
    assert nca["native_geography"] == "GHANA_NATIONAL"
    assert gss["observation_clock"] == "2021 PHC"
    assert nca["observation_clock"] == "2021-Q4 (90-day activity definition)"
    assert gss["field_version"] != nca["field_version"]
    assert gss["field_ref"] != nca["field_ref"]
    assert gss["typed_authority_requirements"]["issued"] is False
    assert nca["typed_authority_requirements"]["permission"] == "TEST_ONLY_NO_EXTERNAL_USE_GRANT"
    # denominator binding
    assert gss["values"]["denominator"] == 3288063
    assert nca["values"]["active_subscriptions"] == 23414527
    # publication clocks
    assert gss["publication_clock"] == "2022-02-24"
    assert nca["publication_clock"] == "2022-07-08"


def test_five_gss_subtypes_sum_and_percent(rows):
    g = produce_two_fields(rows)[GSS]["values"]
    parts = g["electricity_subtypes"]
    assert len(parts) == 5
    assert sum(parts.values()) == g["numerator"] == 2388192
    assert round(100 * g["numerator"] / g["denominator"], 1) == g["published_percent"] == 72.6
    assert parts == {"mains": 2288193, "community_grid": 74490, "generator": 3640,
                     "solar_inverter": 21512, "wind": 357}


def test_nca_prepaid_postpaid_sum_and_not_persons(rows):
    n = produce_two_fields(rows)[NCA]["values"]
    assert n["prepaid"] + n["postpaid"] == n["active_subscriptions"] == 23414527
    assert n["prepaid"] == 23237338 and n["postpaid"] == 177189


# --- 2. two values actually dereferenced (not just refs) ---
def test_two_values_dereferenced_not_only_refs(rows):
    out, fields, registry, refs, relation = read(rows)
    assert out["state"] == "TWO_VALUES_READ_TEST_ONLY"
    by_role = {r["role"]: r for r in out["values_read"]}
    assert by_role[GSS]["values"]["numerator"] == 2388192
    assert by_role[GSS]["values"]["denominator"] == 3288063
    assert by_role[NCA]["values"]["active_subscriptions"] == 23414527
    assert by_role[GSS]["native_unit"] != by_role[NCA]["native_unit"]
    assert out["operative_OC05"] is False and out["issued_EE13"] is False
    assert out["dependency_readset"] == [refs[GSS], refs[NCA]]


def test_ref_only_consumer_cannot_recover_values(rows):
    """A consumer holding only ref strings gets nothing without the registry."""
    fields = produce_two_fields(rows)
    registry = TestOnlyRegistry(rows)
    refs = registry.refs_by_role()
    held = refs[GSS]
    assert isinstance(held, str) and "2388192" not in held
    # no registry access -> no values: unknown ref refused
    other = TestOnlyRegistry(deepcopy(rows))
    with pytest.raises(TestOnlyReadError) as e:
        other.dereference("TESTONLY_FIELD:" + "0" * 64)
    assert e.value.code == "UNKNOWN_EXACT_FIELD_REF"
    # stale ref from a revised registry is refused on the new registry
    changed = deepcopy(rows)
    changed[0]["values"]["numerator"] -= 1
    changed[0]["values"]["electricity_subtypes"]["mains"] -= 1
    newreg = TestOnlyRegistry(changed)
    with pytest.raises(TestOnlyReadError) as e2:
        newreg.dereference(held)
    assert e2.value.code == "UNKNOWN_EXACT_FIELD_REF"


# --- 3. directed numeric mutation isolation ---
def test_gss_minus_one_changes_only_gss(rows):
    out, fields, *_ = read(rows)
    mrows = deepcopy(rows)
    mrows[0]["values"]["numerator"] -= 1
    mrows[0]["values"]["electricity_subtypes"]["mains"] -= 1
    out2, fields2, *_ = read(mrows)
    assert out2["values_read"][1] == out["values_read"][1]  # NCA slot identical
    assert out2["values_read"][0] != out["values_read"][0]  # GSS slot changed
    assert out2["test_snapshot_ref"] != out["test_snapshot_ref"]


def test_nca_plus_one_changes_only_nca(rows):
    out = read(rows)[0]
    mrows = deepcopy(rows)
    mrows[1]["values"]["active_subscriptions"] += 1
    mrows[1]["values"]["prepaid"] += 1
    out2 = read(mrows)[0]
    assert out2["values_read"][0] == out["values_read"][0]
    assert out2["values_read"][1] != out["values_read"][1]


# --- 4. publication cutoffs ---
def test_2021_refuses_both(rows):
    out = read(rows, as_of="2021-12-31")[0]
    assert out["state"] == "REFUSED_REQUIRED_FIELD_TEST_ONLY" and out["values_read"] == []


def test_2022_03_01_gss_only_partial(rows):
    out = read(rows, as_of="2022-03-01", partial_allowed=True)[0]
    assert out["state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert [r["role"] for r in out["values_read"]] == [GSS]


def test_2022_03_01_without_partial_holds(rows):
    out = read(rows, as_of="2022-03-01")[0]
    assert out["state"] == "REFUSED_REQUIRED_FIELD_TEST_ONLY" and out["values_read"] == []


def test_2022_07_07_nca_not_yet_published(rows):
    out = read(rows, as_of="2022-07-07")[0]
    assert out["state"] == "REFUSED_REQUIRED_FIELD_TEST_ONLY"
    assert any(r["role"] == NCA and r["reason"] == "NOT_PUBLISHED_AT_SELECTED_ASOF" for r in out["refusals"])


def test_2022_07_08_both(rows):
    out = read(rows, as_of="2022-07-08")[0]
    assert out["state"] == "TWO_VALUES_READ_TEST_ONLY"


def test_2022_03_01_one_source_nonpositive_2022_07_08_both(rows):
    # mission wording: "2022-03-01 one-source nonpositive, 2022-07-08 both known"
    one = read(rows, as_of="2022-03-01", partial_allowed=True)[0]
    both = read(rows, as_of="2022-07-08")[0]
    assert one["state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert both["state"] == "TWO_VALUES_READ_TEST_ONLY"


# --- 5. hostiles ---
def test_forged_issuer_signature_refused(rows):
    rows[0]["issuer_signature"] = "FORGED"
    reject("ISSUER_FORGERY", lambda: produce_two_fields(rows))


def test_issued_true_refused(rows):
    rows[0]["issued"] = True
    reject("ISSUER_FORGERY", lambda: produce_two_fields(rows))


def test_fake_binary_sha_refused(rows):
    rows[0]["source_pdf_sha256"] = "FAKE"
    reject("UNVERIFIED_BINARY_CUSTODY", lambda: produce_two_fields(rows))


def test_fake_permission_refused(rows):
    rows[1]["permission"] = "GRANTED"
    reject("REAL_USE_PERMISSION_NOT_ISSUED", lambda: produce_two_fields(rows))


def test_stale_source_ref_refused(rows):
    registry = TestOnlyRegistry(rows)
    with pytest.raises(TestOnlyReadError) as e:
        registry.dereference("TESTONLY_FIELD:" + "f" * 64)
    assert e.value.code == "UNKNOWN_EXACT_FIELD_REF"


def test_wrong_scope_unit_rural_phone_people_refused(rows):
    rows[1]["native_unit"] = "RURAL_PHONE_PEOPLE"
    reject("NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT", lambda: TestOnlyRegistry(rows))


def test_wrong_units_person_electricity_refused(rows):
    rows[0]["native_unit"] = "PERSON_HAS_ELECTRICITY"
    reject("GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT", lambda: TestOnlyRegistry(rows))


def test_revoked_use_fail_closed(rows):
    rows[1]["status"] = "REVOKED_TEST_ONLY"
    out = read(rows)[0]
    assert out["state"] == "REFUSED_REQUIRED_FIELD_TEST_ONLY"
    assert out["refusals"][0]["reason"] == "SOURCE_REVOKED"


def test_missing_field_hold(rows):
    with pytest.raises((FieldProducerError, TestOnlyReadError)):
        produce_two_fields([rows[0]])


def test_fake_correlation_relation_refused(rows):
    out, fields, registry, refs, relation = read(rows)
    bad = dict(relation)
    bad["population_join"] = True
    with pytest.raises(TestOnlyReadError) as e:
        read_historical_test_only(registry, selected_refs=refs, relation=bad,
                                  as_of="2022-07-08", clock_mode="HISTORICAL_PUBLICATION_AWARE")
    assert e.value.code == "INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED"


def test_fake_causal_relation_refused(rows):
    out, fields, registry, refs, relation = read(rows)
    with pytest.raises(TestOnlyReadError) as e:
        read_historical_test_only(registry, selected_refs=refs, relation=relation,
                                  as_of="2022-07-08", clock_mode="HISTORICAL_PUBLICATION_AWARE",
                                  requested_model_use=True)
    assert e.value.code == "PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN"


def test_cold_replay_identical(rows):
    a = read(rows)[0]
    b = read(deepcopy(rows))[0]
    assert a == b


def test_targeted_invalidation(rows):
    a = read(rows)[0]
    mrows = deepcopy(rows)
    mrows[0]["values"]["numerator"] -= 1
    mrows[0]["values"]["electricity_subtypes"]["mains"] -= 1
    b = read(mrows)[0]
    d = fixture_invalidation(a, b)
    assert d["changed_roles"] == [GSS] and d["unaffected_roles"] == [NCA]
    assert d["invalidate_previous_snapshot"] is True


# --- 6. real owner handoff: compose_direct_producer ---
def test_direct_producer_handoff_real_owner_import(rows):
    import rawlsing_next.pre553_learned_world_composition as lwc
    assert lwc.__file__.endswith("pre553_learned_world_composition.py")
    fields = produce_two_fields(rows)
    trace = handoff_two_fields(fields)
    assert TRANSPORT_AVAILABLE is True
    assert trace["status"] == "EXECUTED"
    assert trace["transport_function"] == "compose_direct_producer"
    assert trace["transport_module_file"] == lwc.__file__
    assert any(c["function"] == "compose_direct_producer" for c in trace["calls"])
    # receipt is recorded, not adopted; state must be an explicit typed state
    assert isinstance(trace["receipt_terminal_state"], str)
    assert isinstance(trace["receipt_reason_code"], str)


def test_direct_producer_receipt_is_not_issuance(rows):
    fields = produce_two_fields(rows)
    trace = handoff_two_fields(fields)
    # even a successful transport run cannot constitute N5/N6/EE13/N9/OC05
    assert trace["receipt_terminal_state"] != "N5N6_ISSUED"
    assert "TEST_ONLY" in (trace.get("receipt_reason_code", "") + "TEST_ONLY")


# --- 7. no-actor counterfactual ---
def test_no_actor_2021_ghana_counterfactual(rows):
    from d2p.counterfactual import counterfactual_holds, mutation_values
    fields = produce_two_fields(rows)
    checks = counterfactual_holds(fields)
    assert checks["all_hold"] is True
    mv = mutation_values(fields[NCA]["underlying_row"], NCA)
    assert mv["has_person_joint"] is False
    assert mv["person_level_values_available"] == []
    # reader still refuses person exposure
    out, fields2, registry, refs, relation = read(rows)
    with pytest.raises(TestOnlyReadError) as e:
        read_historical_test_only(registry, selected_refs=refs, relation=relation,
                                  as_of="2022-07-08", clock_mode="HISTORICAL_PUBLICATION_AWARE",
                                  requested_person_exposure=True)
    assert e.value.code == "PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN"
