from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef

from campaign_src04_completion.consumers.b0_native_fixture import load_b0_native_bundle
from campaign_src04_completion.consumers.consumer import (
    ConsumerRefusal,
    ProducerBundle,
    b0_fixture_contract,
    consume_native_producer,
    consume_retained_b0_fixture,
    consume_retained_receipt,
    refuse_d1_tally,
    validate_contract,
)

ROOT = Path(__file__).resolve().parents[3]
EV = ROOT / "campaign_src04_completion/consumers/evidence"
B0 = EV / "B0_FIXTURE_POSITIVE.json"
D1 = EV / "D1_TALLY_REF.json"


def _receipt():
    return json.loads(B0.read_text(encoding="utf-8"))


def test_b0_fixture_consumer_positive_is_explicitly_fixture_only():
    product = consume_retained_b0_fixture(B0)
    assert product["status"] == "FIXTURE_ONLY_ENGINEERING_POSITIVE__NOT_SOURCE_LOCAL_PROOF"
    assert product["source_id"] == "SRC09"
    assert product["fixture_only"] is True
    assert product["source_value_sensitive"] is False
    assert product["source_local_claim"] is False
    assert product["oc01_receipt"]["state"] == "SUPPORTED_OBJECTIVE_RESULT"
    assert product["oc01_receipt"]["requested_claim_ceiling"] == "SUPPORTED_COMPONENT_ONLY"
    assert product["oc01_receipt"]["positive_completion"] is True
    assert product["fact_ref"]["kind"] == "EmpiricalFact@1.0.0"
    assert product["raw_numerator_support"] == 1
    assert product["raw_denominator_support"] == 1


def test_b0_fixture_cannot_be_promoted_to_source_local():
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_b0_fixture(B0, requested_claim_ceiling="SOURCE_LOCAL_STATISTIC")
    assert exc.value.code == "CLAIM_CEILING_NOT_AUTHORIZED"


def test_wrong_source_use_and_claim_are_refused():
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_b0_fixture(B0, expected_source_id="SRC04")
    assert exc.value.code == "WRONG_SOURCE_ID"
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_b0_fixture(B0, use_scope="SOURCE_LOCAL_STATISTIC")
    assert exc.value.code == "WRONG_USE_SCOPE"


def test_wrong_release_fact_and_missing_authority_are_refused():
    receipt = _receipt()
    contract = b0_fixture_contract(receipt)
    wrong_release = replace(contract, release_ref=ExactRef("C11LogicalRelease", contract.release_ref.object_id, "0" * 64))
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_receipt(receipt, wrong_release)
    assert exc.value.code == "RETAINED_RELEASE_REF_MISMATCH"
    wrong_fact = replace(contract, fact_ref=ExactRef("EmpiricalFact@1.0.0", contract.fact_ref.object_id, "1" * 64))
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_receipt(receipt, wrong_fact)
    assert exc.value.code == "RETAINED_FACT_REF_MISMATCH"
    no_auth = replace(contract, policy_authority_refs=())
    with pytest.raises(ConsumerRefusal) as exc:
        consume_retained_receipt(receipt, no_auth)
    assert exc.value.code == "MISSING_AUTHORITY"


def test_fixture_contract_cannot_become_source_local_without_native_authority():
    contract = b0_fixture_contract(_receipt())
    promoted = replace(
        contract,
        fixture_only=False,
        evidence_tier="SOURCE_LOCAL_CERTIFIED",
        claim_ceiling="SOURCE_LOCAL_STATISTIC",
        use_scopes=("SOURCE_LOCAL_STATISTIC",),
    )
    with pytest.raises(ConsumerRefusal) as exc:
        validate_contract(
            promoted,
            expected_source_id="SRC09",
            requested_claim_ceiling="SOURCE_LOCAL_STATISTIC",
            use_scope="SOURCE_LOCAL_STATISTIC",
        )
    assert exc.value.code == "NATIVE_AUTHORITY_REFS_REQUIRED"


def test_d1_tally_is_refused_not_converted():
    result = refuse_d1_tally(D1)
    assert result["status"] == "REFUSED"
    assert result["error_code"] == "PRODUCER_FAMILY_REFUSED__D1_TALLY_NOT_EMPIRICAL_FACT"
    assert result["consumer_invoked"] is False
    assert result["d1_field_count"] == 42


def test_native_path_refuses_fixture_contract():
    contract = b0_fixture_contract(_receipt())
    bundle = ProducerBundle(
        release=None,
        query=None,
        predicate=None,
        repository=None,
        authority_registry=None,
        contract=contract,
    )
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(
            bundle,
            expected_source_id="SRC09",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
        )
    assert exc.value.code == "FIXTURE_NATIVE_PATH_REQUIRES_ENGINEERING_LABEL"


def _native_fixture_product(*, mutate=False, evidence=None, case=None):
    return consume_native_producer(
        load_b0_native_bundle(mutate_q101_2_to_1=mutate),
        expected_source_id="SRC09",
        requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
        use_scope="SUPPORTED_COMPONENT_ONLY",
        allow_fixture_engineering=True,
        value_sensitivity_evidence=evidence,
        value_sensitivity_case=case,
    )


def _sensitivity_result(product):
    discovery = product["downstream_discovery"]
    return {
        "fact_ref": product["fact_ref"],
        "raw_numerator_support": product["raw_numerator_support"],
        "raw_denominator_support": product["raw_denominator_support"],
        "downstream_value_effect": product["downstream_value_effect"],
        "discovery_supported_candidate_count": discovery["supported_candidate_count"],
        "discovery_empirical_fact_refs": [
            ref["content_hash"] for ref in discovery["empirical_fact_refs"]
        ],
    }


def test_native_fixture_executes_real_value_consuming_path():
    product = _native_fixture_product()
    assert product["schema"] == "PYAT_SRC04_LANE_D_CONSUMER_PRODUCT@1.1.0"
    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert product["native_execution"] is True
    assert product["fixture_only"] is True
    assert product["source_local_claim"] is False
    assert product["fact_ref"]["content_hash"] == "a377bc42e15134ca8774fe5940ab537789cb5797bf3c2e72e8db981b4869cecc"
    assert product["raw_numerator_support"] == 1
    assert product["raw_denominator_support"] == 1
    assert product["oc01_receipt"]["state"] == "SUPPORTED_OBJECTIVE_RESULT"
    assert product["oc01_receipt"]["positive_completion"] is True
    assert product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    assert product["downstream_value_consumer"].endswith("execute_exact_bounded_discovery")
    assert product["downstream_discovery"]["supported_candidate_count"] == 1
    assert product["downstream_discovery"]["receipts"][0]["typed_state"] == "DISCOVERED_RESULT_SUPPORTED"
    assert len(product["downstream_discovery"]["empirical_fact_refs"]) == 2
    assert product["effective_n_product"]["typed_state"] == "NOT_APPLICABLE"
    assert product["source_value_sensitive"] is False
    assert product["fixture_value_sensitive"] is False
    assert product["value_sensitivity"]["status"] == "NOT_DEMONSTRATED"


def test_native_fixture_mutation_changes_values_and_restore():
    original = _native_fixture_product()
    mutated = _native_fixture_product(mutate=True)
    restored = _native_fixture_product()
    original_result = _sensitivity_result(original)
    mutated_result = _sensitivity_result(mutated)
    restored_result = _sensitivity_result(restored)
    assert original_result["fact_ref"] != mutated_result["fact_ref"]
    assert (original_result["raw_numerator_support"], original_result["raw_denominator_support"]) == (1, 1)
    assert (mutated_result["raw_numerator_support"], mutated_result["raw_denominator_support"]) == (2, 2)
    assert original_result["discovery_empirical_fact_refs"] != mutated_result["discovery_empirical_fact_refs"]
    assert restored_result == original_result
    evidence = {
        "schema": "PYAT_SRC04_LANE_D_VALUE_SENSITIVITY@1.0.0",
        "status": "MEASURED_FIXTURE_ONLY",
        "scope": "NONRESPONDENT_FIXTURE_ONLY",
        "measured": True,
        "changed": True,
        "restored": True,
        "upstream_change": "q101 row-2 2.0 -> 1.0",
        "original": original_result,
        "mutated": mutated_result,
        "restored_result": restored_result,
    }
    final_original = _native_fixture_product(evidence=evidence, case="original")
    final_mutated = _native_fixture_product(mutate=True, evidence=evidence, case="mutated")
    final_restored = _native_fixture_product(evidence=evidence, case="restored")
    assert final_original["fixture_value_sensitive"] is True
    assert final_mutated["fixture_value_sensitive"] is True
    assert final_restored["fixture_value_sensitive"] is True
    assert final_original["source_value_sensitive"] is False
    assert final_original["value_sensitivity"]["status"] == "MEASURED_FIXTURE_ONLY"
    assert final_original["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"


def test_native_fixture_cannot_be_promoted_to_source_local():
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(
            load_b0_native_bundle(),
            expected_source_id="SRC09",
            requested_claim_ceiling="SOURCE_LOCAL_STATISTIC",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        )
    assert exc.value.code == "CLAIM_CEILING_NOT_AUTHORIZED"


def test_native_fixture_requires_actual_downstream_value_consumer():
    bundle = replace(load_b0_native_bundle(), discovery=None)
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(
            bundle,
            expected_source_id="SRC09",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        )
    assert exc.value.code == "DOWNSTREAM_VALUE_CONSUMER_REQUIRED"


def test_committed_consumer_evidence_has_no_respondent_cells():
    for path in EV.glob("*.json"):
        raw = path.read_text(encoding="utf-8")
        assert '"raw_response_value"' not in raw
        assert '"raw_coordinate_value"' not in raw
