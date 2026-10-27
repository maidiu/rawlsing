"""Focused D1 checks over the committed aggregate product and negatives."""
from __future__ import annotations

import json
from pathlib import Path

from campaign_d1_src04_tally import adapter


def _product():
    path = adapter.EVIDENCE / "TALLY_PRODUCT.json"
    assert path.is_file(), "run primary before focused checks"
    return json.loads(path.read_text(encoding="utf-8"))


def test_product_partitions_every_accepted_field():
    product = _product()
    assert product["field_count"] == 42
    assert product["held_fields"] == []
    assert len(product["fields"]) == 42
    assert product["source_record_denominator"] == 7337
    assert product["event_presence_count"] == 308154
    assert product["tally_ref"]["content_hash"]
    assert product["replay_ref"]["content_hash"]
    for field in product["fields"]:
        assert field["status"] == "COUNTED"
        assert field["event_presence_count"] == 7337
        assert sum(field["state_counts"].values()) == 7337
        assert sum(item["count"] for item in field["native_value_counts"]) == 7337
        assert (field["observed_response_denominator"] + field["missing_or_unobserved_count"]) == 7337
        assert field["answered_substantive_denominator"] <= field["observed_response_denominator"]
        assert field["component_presence"] == ["none"]


def test_product_preserves_release_and_unknown_routing():
    product = _product()
    assert product["source_sha256"] == adapter.EXPECTED_SOURCE_SHA256
    assert product["release_ref"]["content_hash"] == adapter.EXPECTED_RELEASE_HASH
    assert product["routing_state"] == "ROUTING_UNKNOWN"
    assert product["canonicalization"] == "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW"
    assert product["canonical_values_emitted"] == 0
    assert product["weight_facts"] == 0
    assert product["local_bundle"]["public_objects_sha256"] == adapter.EXPECTED_PUBLIC_SHA256


def test_source_value_control_is_discriminating():
    product = _product()
    values = {item["native_value"]: item["count"] for item in product["control"]["values"]}
    assert set(values) == {1.0, 2.0}
    assert values[1.0] != values[2.0]
    assert product["control"]["source_release_unchanged"] is True


def test_wrong_release_refuses_without_consuming_bundle():
    result = adapter.wrong_release_negative()
    assert result["status"] == "REFUSED"
    assert result["actual_code"] == "RELEASE_IDENTITY_MISMATCH"
    assert result["local_bundle_consumed"] is False


def test_unknown_state_is_held_refusal():
    result = adapter.unknown_state_negative()
    assert result["status"] == "REFUSED"
    assert result["actual_code"] == "UNKNOWN_RESPONSE_STATE"

def test_portable_grant_and_program_evidence_are_committed():
    assert adapter.D1_GRANT_PATH.is_file()
    assert adapter.D1_PROGRAM_PATH.is_file()
    assert __import__("hashlib").sha256(adapter.D1_GRANT_PATH.read_bytes()).hexdigest() == adapter.EXPECTED_D1_GRANT_SHA256
    assert __import__("hashlib").sha256(adapter.D1_PROGRAM_PATH.read_bytes()).hexdigest() == adapter.EXPECTED_PROGRAM_SHA256


def test_wrong_source_negative_refuses_before_bundle():
    result = adapter.wrong_source_negative()
    assert result["status"] == "REFUSED"
    assert result["actual_code"] == "SOURCE_IDENTITY_MISMATCH"
    assert result["local_bundle_consumed"] is False


def test_existing_defer_authority_negative_and_same_release():
    result = adapter.held_authority_negative()
    assert result["status"] == "REFUSED"
    assert result["decision_state"] == "DEFER"
    assert result["same_release_ref"]["content_hash"] == adapter.EXPECTED_RELEASE_HASH
    assert result["issued_i03_or_i05"] is False


def test_portable_primary_builder_recreates_exact_refs():
    product = adapter.build_tally()
    assert product["tally_ref"]["content_hash"] == "87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022"
    assert product["replay_ref"]["content_hash"] == "8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f"
    assert product["held_fields"] == []
