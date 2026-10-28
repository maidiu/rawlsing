from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

import pytest

from campaign_src04_completion.consumers.consumer import (
    ConsumerRefusal,
    OBSERVED_RESPONSE_STATUS,
    _observed_response_projection,
    _plain,
    consume_native_producer,
)
from campaign_src04_completion.empirical.review import test_cd_boundary_review as review_fixture
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import exact_ref


@pytest.fixture(scope="module")
def observed_context():
    # Reuse the review-owned fixture builder read-only.  The review test file is
    # not imported into this test module's namespace and is never edited here.
    return review_fixture._FixtureContext()


def _joined(observed_context):
    return observed_context.consume_joined()


def _observed_fact(topology):
    return SimpleNamespace(target_topology=topology)


def test_actual_joined_c_observed_projection_is_preserved(observed_context):
    joined = _joined(observed_context)
    product = joined["product"]
    fact = joined["fact"]
    c_projection = fact.target_topology["observed_response"]
    d_projection = product["observed_response"]

    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    assert d_projection == _plain(c_projection)
    assert d_projection["status"] == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
    assert d_projection["not_eligible_population_estimate"] is True
    assert d_projection["contract_ref"] == c_projection["contract_ref"]
    assert d_projection["ledger"] == _plain(c_projection["ledger"])
    assert d_projection["ledger"]["target_observed"] == 7
    assert d_projection["ledger"]["target_unobserved"] == 1

    bundle = joined["bundle"]
    discovery = execute_exact_bounded_discovery(
        repository=bundle.repository,
        discovery_authority=bundle.discovery.authority,
        authority_registry=bundle.authority_registry,
        release_refs=(bundle.contract.release_ref,),
        predicate_catalog=bundle.discovery.predicate_catalog,
        query_template_catalog=bundle.discovery.query_template_catalog,
    )
    facts_by_key = {item.ref.key: item for item in discovery.empirical_facts}
    discovery_items = product["downstream_discovery"]["empirical_facts"]
    assert discovery_items
    for item in discovery_items:
        exact_fact = facts_by_key[exact_ref(item["fact_ref"]).key]
        expected = exact_fact.target_topology["observed_response"]
        assert item["observed_response"] == _plain(expected)
        assert item["observed_response"]["status"] == OBSERVED_RESPONSE_STATUS
        assert item["observed_response"]["not_eligible_population_estimate"] is True
        assert item["observed_response"]["contract_ref"] == c_projection["contract_ref"]
        assert set(item["observed_response"]["ledger"]) == set(c_projection["ledger"])


def test_missing_or_wrong_observed_projection_is_refused(observed_context):
    joined = _joined(observed_context)
    query = joined["bundle"].query
    good = _plain(joined["fact"].target_topology["observed_response"])

    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(_observed_fact({}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_PROJECTION_MISSING"

    wrong_status = deepcopy(good)
    wrong_status["status"] = "ELIGIBLE_POPULATION_ESTIMATE"
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(_observed_fact({"observed_response": wrong_status}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_STATUS_INVALID"

    wrong_ref = deepcopy(good)
    wrong_ref["contract_ref"]["content_hash"] = "0" * 64
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(_observed_fact({"observed_response": wrong_ref}), query)
    assert exc.value.code == "OBSERVED_RESPONSE_CONTRACT_REF_MISMATCH"

    incomplete_ledger = deepcopy(good)
    del incomplete_ledger["ledger"]["target_unobserved"]
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _observed_fact({"observed_response": incomplete_ledger}), query
        )
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_INCOMPLETE"

    wrong_ledger_ref = deepcopy(good)
    wrong_ledger_ref["ledger"]["contract_ref"]["content_hash"] = "1" * 64
    with pytest.raises(ConsumerRefusal) as exc:
        _observed_response_projection(
            _observed_fact({"observed_response": wrong_ledger_ref}), query
        )
    assert exc.value.code == "OBSERVED_RESPONSE_LEDGER_CONTRACT_REF_MISMATCH"


def test_nonobserved_b0_fixture_path_keeps_prior_shape():
    from campaign_src04_completion.consumers.b0_native_fixture import load_b0_native_bundle

    product = consume_native_producer(
        load_b0_native_bundle(),
        expected_source_id="SRC09",
        requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
        use_scope="SUPPORTED_COMPONENT_ONLY",
        allow_fixture_engineering=True,
    )
    assert "observed_response" not in product
    assert all(
        "observed_response" not in item
        for item in product["downstream_discovery"]["empirical_facts"]
    )
