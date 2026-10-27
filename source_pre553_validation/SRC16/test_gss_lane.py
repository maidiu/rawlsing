"""Focused checks for the R157 GSS source-configuration lane.

Run from the repository root:

    PYTHONPATH=. python3 -m pytest source_pre553_validation/SRC16/test_gss_lane.py -q -o addopts=''
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
from rawlsing_next.source_configuration.evidence import source_roster_entry
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.reader import (
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import load_source_config

ROOT = Path(__file__).resolve().parents[2]
VALIDATION_ROOT = ROOT / "source_pre553_validation"
DATA_ROOT = ROOT / "rawlsing_next/source_configuration/data"
SOURCES = tuple(f"SRC{i:02d}" for i in range(16, 24))


def _paths(source_id: str) -> dict[str, Path]:
    return {
        "source": DATA_ROOT / source_id / f"{source_id}.source.config.json",
        "fixture_config": VALIDATION_ROOT / source_id / f"{source_id}.fixture.config.json",
        "fixture": VALIDATION_ROOT / source_id / f"{source_id}.fixture.json",
        "results": VALIDATION_ROOT / source_id / f"{source_id}.validation-results.json",
        "manifest": VALIDATION_ROOT / source_id / f"{source_id}.manifest.json",
        "exceptions": VALIDATION_ROOT / source_id / f"{source_id}.exceptions.json",
        "accounting": DATA_ROOT / source_id / f"{source_id}.evidence-accounting.json",
    }


@pytest.mark.parametrize("source_id", SOURCES)
def test_original_config_schema_and_no_drop(source_id: str) -> None:
    paths = _paths(source_id)
    config = load_source_config(paths["source"])
    document = config.document
    roster = source_roster_entry(source_id)
    assert document["config_purpose"] == "SOURCE_PREPARATION"
    assert document["binding"]["identity_class"] == "ORIGINAL_SOURCE"
    assert document["binding"]["source_sha256"] == roster["source_sha256"]
    assert document["identity"]["expected_source_sha256"] == roster["source_sha256"]
    assert len(document["physical_slots"]) == roster["physical_columns"]
    assert len(document["items"]) == roster["original_items"]
    assert document["coverage"]["physical_slots_total"] == roster["physical_columns"]
    assert document["coverage"]["items_total"] == roster["original_items"]
    assert len(document["coverage"]["physical_slots_included"]) + len(
        document["coverage"]["physical_slots_excluded"]) == roster["physical_columns"]
    assert len(document["coverage"]["items_included"]) + len(
        document["coverage"]["items_excluded"]) == roster["original_items"]
    assert document["supported_scope"]["native_validation_expectation"] == "NOT_RUN"
    assert document["supported_scope"]["original_source_execution"] == (
        "NOT_PERFORMED_UNDER_R157_PREPARATION")
    assert document["respondents"]["source_native_key_slot"]["name"] == "id"
    assert document["weight_slots"] == []
    assert any(item["field"] == "weight_slots" for item in document["residuals"]) is False
    assert any("weight" in item["field"].lower() for item in document["residuals"])


@pytest.mark.parametrize("source_id", SOURCES)
def test_fixture_identity_is_separate_and_fixture_only(source_id: str) -> None:
    paths = _paths(source_id)
    original = load_source_config(paths["source"]).document
    fixture = load_source_config(paths["fixture_config"]).document
    assert fixture["config_purpose"] == "NONRESPONDENT_FIXTURE"
    assert fixture["supported_scope"]["purpose"] == "NONRESPONDENT_FIXTURE_VALIDATION"
    assert fixture["binding"]["identity_class"] == "NONRESPONDENT_FIXTURE"
    assert fixture["binding"]["source_sha256"] != original["binding"]["source_sha256"]
    assert fixture["binding"]["source_sha256"] != fixture["identity"]["expected_source_sha256"]
    assert all(
        item["scope_envelope"].get("fixture_only") is True
        and item["scope_envelope"].get("grade") == "NONRESPONDENT_FIXTURE_ONLY"
        for item in fixture["authority"]["snapshots"]
    )
    assert all(
        item["scope_envelope"].get("fixture_only") is not True
        for item in original["authority"]["snapshots"]
    )
    assert fixture["respondents"]["source_native_key_slot"]["name"] == "id"
    assert fixture["binding"]["fixture_provenance"]["original_source_sha256"] == (
        original["identity"]["expected_source_sha256"])


@pytest.mark.parametrize("source_id", SOURCES)
def test_native_fixture_release_and_p3_key_extraction(source_id: str) -> None:
    paths = _paths(source_id)
    stored = json.loads(paths["results"].read_text(encoding="utf-8"))
    fixture_cfg = load_source_config(paths["fixture_config"])
    stream = load_fixture_stream(paths["fixture"])
    fixture_doc = json.loads(paths["fixture"].read_text(encoding="utf-8"))
    keys = row_native_keys_from_transport(fixture_cfg, stream=stream)
    assert keys is not None
    assert len(keys) == 6
    assert all(value.kind == "R157_NONRESPONDENT_FIXTURE_KEY" for value in keys.values())
    projection = build_governed_c11_projection(fixture_cfg, row_native_keys=keys)
    release = build_validated_c11_release_from_config(fixture_cfg, stream=stream)
    assert release.release_ref.as_dict() == stored["native_validation"]["release"]["release_ref"]
    assert release.semantic_release_hash == stored["native_validation"]["release"]["semantic_release_hash"]
    assert projection.projection_identity_ref.as_dict() == stored["native_validation"]["projection"]["projection_identity_ref"]
    assert sum(isinstance(obj, AuthoritySnapshot) for obj in release.public_objects) == 7
    assert stored["native_validation"]["expected_match"] is True
    assert fixture_doc["expected_results"]["response_state_counts"] == (
        stored["native_validation"]["actual"]["response_state_counts"])
    assert stored["coverage"]["no_drop"] is True


@pytest.mark.parametrize("source_id", SOURCES)
def test_original_refuses_without_decoded_keys_and_fixture_stream(source_id: str) -> None:
    paths = _paths(source_id)
    original_cfg = load_source_config(paths["source"])
    fixture_stream = load_fixture_stream(paths["fixture"])
    with pytest.raises(Exception, match="row_native_keys|source_native_key_slot"):
        build_governed_c11_projection(original_cfg)
    with pytest.raises(Exception, match="SHA|binding|key|row"):
        build_validated_c11_release_from_config(original_cfg, stream=fixture_stream)


@pytest.mark.parametrize("source_id", SOURCES)
def test_p3_reader_transport_is_metadata_only(source_id: str) -> None:
    paths = _paths(source_id)
    config = load_source_config(paths["source"])
    reader = reader_configuration_from_config(config)
    assert reader.source_sha256 == config.original_source_sha256
    assert reader.encoding is None
    assert reader.authority_status is None
    request = source_read_request_from_config(
        config,
        host="R157_PREPARATION_HOST",
        purpose="SOURCE_CONFIGURATION_PREPARATION",
        consumer_use="R157_GSS_LANE_CONFIGURATION",
        semantic_use_scope=("response_rule_configuration", "coordinate_configuration"),
    )
    assert request.source_sha256 == config.original_source_sha256
    assert request.source_format == "SAV"
    assert request.read_operation == "SOURCE_RESPONSE_DECODE"
    assert request.custody_locator_binding == config.document["identity"]["locator"]["locator_id"]
    assert "source_bytes_read" not in request.__dict__


def test_lane_manifests_and_exception_ledgers_exist() -> None:
    for source_id in SOURCES:
        paths = _paths(source_id)
        for key in ("manifest", "exceptions", "accounting", "fixture", "fixture_config", "source", "results"):
            assert paths[key].is_file(), (source_id, key)
        manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
        assert manifest["no_drop"] is True
        assert manifest["native_release_ref"]["kind"] == "C11LogicalRelease"
        exceptions = json.loads(paths["exceptions"].read_text(encoding="utf-8"))
        assert exceptions["residual_count"] == len(exceptions["residuals"])
        assert exceptions["blocking_original_execution"] is True
