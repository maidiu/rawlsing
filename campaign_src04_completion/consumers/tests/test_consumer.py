from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef

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
    assert exc.value.code == "NATIVE_SOURCE_IDENTITY_MISMATCH"


def test_committed_consumer_evidence_has_no_respondent_cells():
    for path in EV.glob("*.json"):
        raw = path.read_text(encoding="utf-8")
        assert '"raw_response_value"' not in raw
        assert '"raw_coordinate_value"' not in raw
