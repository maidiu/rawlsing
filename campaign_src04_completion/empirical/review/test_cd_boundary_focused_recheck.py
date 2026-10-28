"""Focused successor review: repaired D observed-response provenance.

This is review-owned.  It reuses the frozen prior review fixture builder
read-only, does not alter the historical RED test or receipt, reads only the
labelled SRC04 nonrespondent fixture, and writes nothing outside review/**.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace

import pytest

import campaign_src04_completion.consumers.consumer as consumer_module
from campaign_src04_completion.consumers.consumer import (
    ConsumerRefusal,
    OBSERVED_RESPONSE_STATUS,
    _observed_response_projection,
    _plain,
    consume_native_producer,
)
from campaign_src04_completion.empirical.review import test_cd_boundary_review as prior
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_observed_response import validate_contract_authority


@pytest.fixture(scope="module")
def context():
    return prior._FixtureContext()


def _joined(context):
    return context.consume_joined()


def _fact_with_topology(topology):
    return SimpleNamespace(target_topology=topology)


def _primary_and_discovery_facts(joined):
    bundle = joined["bundle"]
    result = execute_exact_bounded_discovery(
        repository=bundle.repository,
        discovery_authority=bundle.discovery.authority,
        authority_registry=bundle.authority_registry,
        release_refs=(bundle.contract.release_ref,),
        predicate_catalog=bundle.discovery.predicate_catalog,
        query_template_catalog=bundle.discovery.query_template_catalog,
    )
    return {fact.ref.key: fact for fact in result.empirical_facts}


def test_primary_projection_equals_exact_c_projection(context):
    joined = _joined(context)
    product = joined["product"]
    fact = joined["fact"]
    query = joined["bundle"].query
    expected = _plain(fact.target_topology["observed_response"])
    actual = product["observed_response"]
    assert actual == expected
    assert actual["status"] == OBSERVED_RESPONSE_STATUS
    assert actual["not_eligible_population_estimate"] is True
    assert actual["contract_ref"] == query.requested_output_grain[
        "observed_response_contract_ref"
    ]
    assert actual["contract_ref"] == expected["contract_ref"]
    assert actual["ledger"] == expected["ledger"]
    assert actual["ledger"]["target_observed"] == 7
    assert actual["ledger"]["target_unobserved"] == 1
    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"


def test_each_discovery_fact_retains_its_own_exact_projection(context):
    joined = _joined(context)
    product = joined["product"]
    facts_by_key = _primary_and_discovery_facts(joined)
    items = product["downstream_discovery"]["empirical_facts"]
    assert len(items) == len(facts_by_key)
    assert items
    for item in items:
        fact = facts_by_key[exact_ref(item["fact_ref"]).key]
        expected = _plain(fact.target_topology["observed_response"])
        actual = item["observed_response"]
        assert actual == expected
        assert actual["status"] == OBSERVED_RESPONSE_STATUS
        assert actual["not_eligible_population_estimate"] is True
        assert actual["ledger"] == expected["ledger"]
        expected_query_ref = exact_ref(fact.empirical_query_spec_ref)
        assert actual["contract_ref"] == product["observed_response"]["contract_ref"]
        assert expected_query_ref.kind == "EmpiricalQuerySpec@1.0.0"


def test_wrong_projections_refuse_with_exact_codes(context):
    joined = _joined(context)
    query = joined["bundle"].query
    good = _plain(joined["fact"].target_topology["observed_response"])

    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(_fact_with_topology({}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_PROJECTION_MISSING"

    wrong_status = deepcopy(good)
    wrong_status["status"] = "ELIGIBLE_POPULATION_ESTIMATE"
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": wrong_status}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_STATUS_INVALID"

    population_claim = deepcopy(good)
    population_claim["not_eligible_population_estimate"] = False
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": population_claim}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_POPULATION_CLAIM_REFUSED"

    wrong_contract = deepcopy(good)
    wrong_contract["contract_ref"]["content_hash"] = "0" * 64
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": wrong_contract}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_CONTRACT_REF_MISMATCH"

    no_ledger = deepcopy(good)
    del no_ledger["ledger"]
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": no_ledger}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_MISSING"

    incomplete_ledger = deepcopy(good)
    del incomplete_ledger["ledger"]["target_unobserved"]
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": incomplete_ledger}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_INCOMPLETE"

    wrong_ledger_ref = deepcopy(good)
    wrong_ledger_ref["ledger"]["contract_ref"]["content_hash"] = "1" * 64
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": wrong_ledger_ref}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_CONTRACT_REF_MISMATCH"

    bad_ledger_population = deepcopy(good)
    bad_ledger_population["ledger"]["not_eligible_population_estimate"] = False
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": bad_ledger_population}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_POPULATION_CLAIM_REFUSED"

    no_grain = SimpleNamespace(requested_output_grain={})
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _fact_with_topology({"observed_response": good}), no_grain)
    assert exc.value.code == "OBSERVED_RESPONSE_PROJECTION_WITHOUT_QUERY_GRAIN"


def test_actual_consumer_refuses_mutated_primary_projection(context, monkeypatch):
    joined = _joined(context)
    bundle = joined["bundle"]
    real_fact = joined["fact"]
    bad = deepcopy(_plain(real_fact.target_topology["observed_response"]))
    bad["status"] = "ELIGIBLE_POPULATION_ESTIMATE"
    fake = SimpleNamespace(
        ref=real_fact.ref,
        typed_state=real_fact.typed_state,
        raw_denominator_support=real_fact.raw_denominator_support,
        raw_numerator_support=real_fact.raw_numerator_support,
        empirical_query_spec_ref=real_fact.empirical_query_spec_ref,
        condition_predicate_ref=real_fact.condition_predicate_ref,
        source_empirical_provenance_refs=real_fact.source_empirical_provenance_refs,
        authority_snapshot_refs=real_fact.authority_snapshot_refs,
        target_topology={
            **dict(real_fact.target_topology),
            "observed_response": bad,
        },
    )
    monkeypatch.setattr(
        consumer_module,
        "execute_empirical_query",
        lambda **kwargs: SimpleNamespace(facts=(fake,)),
    )
    with pytest.raises(ConsumerRefusal) as exc:
        consumer_module.consume_native_producer(
            bundle,
            expected_source_id="SRC04",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        )
    assert exc.value.code == "OBSERVED_RESPONSE_STATUS_INVALID"


def test_nonobserved_b0_path_keeps_prior_shape():
    from campaign_src04_completion.consumers.b0_native_fixture import load_b0_native_bundle

    product = consume_native_producer(
        load_b0_native_bundle(),
        expected_source_id="SRC09",
        requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
        use_scope="SUPPORTED_COMPONENT_ONLY",
        allow_fixture_engineering=True,
    )
    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert "observed_response" not in product
    assert all(
        "observed_response" not in item
        for item in product["downstream_discovery"]["empirical_facts"]
    )


def test_native_value_change_restoration_and_firewall(context):
    original = _joined(context)["product"]
    mutated = prior._mutated_fixture_context().consume_joined()["product"]
    restored = _joined(context)["product"]
    assert mutated["source_sha256"] != original["source_sha256"]
    assert mutated["fact_ref"] != original["fact_ref"]
    assert (
        mutated["downstream_discovery"]["empirical_fact_refs"]
        != original["downstream_discovery"]["empirical_fact_refs"]
    )
    assert restored["source_sha256"] == original["source_sha256"]
    assert restored["fact_ref"] == original["fact_ref"]
    assert (
        restored["downstream_discovery"]["empirical_fact_refs"]
        == original["downstream_discovery"]["empirical_fact_refs"]
    )
    assert restored["observed_response"] == original["observed_response"]

    bundle = _joined(context)["bundle"]
    common = {
        "expected_source_id": "SRC04",
        "requested_claim_ceiling": "SUPPORTED_COMPONENT_ONLY",
        "use_scope": "SUPPORTED_COMPONENT_ONLY",
        "allow_fixture_engineering": True,
    }
    cases = [
        ("NATIVE_SOURCE_IDENTITY_MISMATCH", replace(
            bundle.contract, source_sha256="0" * 64)),
        ("WRONG_RELEASE_IDENTITY", replace(
            bundle.contract,
            release_ref=exact_ref(
                {"kind": "C11LogicalRelease", "object_id": "urn:test:wrong-release",
                 "content_hash": "1" * 64},
                "wrong_release",
            ),
        )),
        ("FACT_SET_MISMATCH", replace(
            bundle.contract,
            fact_ref=exact_ref(
                {"kind": "EmpiricalFact@1.0.0", "object_id": "urn:test:wrong-fact",
                 "content_hash": "2" * 64},
                "wrong_fact",
            ),
        )),
        ("MISSING_AUTHORITY", replace(
            bundle.contract,
            native_authority_refs=(),
            policy_authority_refs=(),
        )),
    ]
    for expected_code, contract in cases:
        with pytest.raises(ConsumerRefusal) as exc:
            consume_native_producer(
                replace(bundle, contract=contract),
                **common,
            )
        assert exc.value.code == expected_code
    with pytest.raises(Pre553AuthorityError, match="fixture-only"):
        validate_contract_authority(
            replace(context.contract, authority_grade="ORIGINAL_SCIENTIFIC"),
            context.registry,
        )
