"""Focused B0 checks over committed metadata and the SRC04 nonrespondent fixture."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from campaign_b0_src04 import adapter


def test_original_request_plan_is_exact_and_remains_blocked():
    plan = adapter.prepare_original_request_plan()
    assert plan["status"] == "BLOCKED_MISSING_EXACT_CONSUMER_AUTHORITY"
    assert plan["query_constructed"] is False
    assert plan["request_count"] == 42
    assert len(plan["request_set"]) == 42
    assert plan["source_release_ref"]["content_hash"] == adapter.EXPECTED_RELEASE_HASH
    assert plan["source_sha256"] == adapter.EXPECTED_SOURCE_SHA256
    assert plan["source_read_performed_by_b0"] is False
    assert plan["local_original_release_read_by_b0"] is False
    assert plan["canonicalization"] == "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW"
    assert plan["canonical_response_values"] == 0
    assert plan["weight_slots"] == 0
    assert {x["routing_state"] for x in plan["request_set"]} == {"ROUTING_UNKNOWN"}
    assert all(x["query_spec"] is None for x in plan["request_set"])
    roles = {x["role"] for x in plan["missing_authority"]}
    assert "predicate_grammar_and_operation" in roles
    assert "runtime_object_catalog_and_historical_parent" in roles
    assert "routing_risk_set" in roles
    assert plan["minimal_remaining_authority"]["not_fabricated"] is True


def test_original_plan_does_not_open_source_or_local_release(monkeypatch):
    receipt = json.loads(adapter.A_RECEIPT_PATH.read_text(encoding="utf-8"))
    source_path = str(Path(receipt["source_path"]))
    local_marker = "Library/Application Support/Rawlsing/campaign-a-src04/releases"
    original_open = Path.open
    opened: list[str] = []

    def guarded_open(self, *args, **kwargs):
        text = str(self)
        if text == source_path or local_marker in text:
            opened.append(text)
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    plan = adapter.prepare_original_request_plan()
    assert plan["request_count"] == 42
    assert opened == []


def test_original_release_identity_mismatch_refuses():
    result = adapter.original_release_mismatch_negative()
    assert result["status"] == "REFUSED"
    assert result["actual_code"] == "RELEASE_HASH_MISMATCH"
    assert result["source_read_performed"] is False


def test_fixture_positive_constructs_real_catalog_and_query():
    result = adapter.build_fixture_positive()
    assert result["scope"] == "NONRESPONDENT_FIXTURE_ONLY_NOT_ORIGINAL"
    assert result["fixture_source_sha256"] == adapter.EXPECTED_FIXTURE_SOURCE_SHA256
    assert result["fixture_release_ref"]["content_hash"] == adapter.EXPECTED_FIXTURE_RELEASE_HASH
    assert result["query_ref"]["kind"] == "EmpiricalQuerySpec@1.0.0"
    assert result["predicate_ref"]["kind"] == "EmpiricalPredicate@1.0.0"
    assert result["catalog_identity"]
    assert result["test_only_query_authority_used"] is True
    assert result["original_source_or_release_read"] is False
    assert result["execution"]["status"] in {"EXECUTED", "REFUSED_OR_TYPED_UNAVAILABLE"}


def test_fixture_target_mismatch_refuses():
    result = adapter.fixture_target_mismatch()
    assert result["status"] == "REFUSED"
    assert result["actual_code"] == "FIXTURE_TARGET_NOT_ADMINISTERED"
    assert result["original_source_or_release_read"] is False
