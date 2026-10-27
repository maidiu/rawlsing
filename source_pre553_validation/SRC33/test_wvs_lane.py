"""Focused checks for the R157 WVS source-configuration lane."""
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
SOURCES = ("SRC33", "SRC34", "SRC35")


def _paths(source_id: str) -> dict[str, Path]:
    return {
        "source": DATA_ROOT / source_id / f"{source_id}.source.config.json",
        "accounting": DATA_ROOT / source_id / f"{source_id}.evidence-accounting.json",
        "fixture_config": VALIDATION_ROOT / source_id / f"{source_id}.fixture.config.json",
        "fixture": VALIDATION_ROOT / source_id / f"{source_id}.fixture.json",
        "results": VALIDATION_ROOT / source_id / f"{source_id}.validation-results.json",
        "manifest": VALIDATION_ROOT / source_id / f"{source_id}.manifest.json",
        "exceptions": VALIDATION_ROOT / source_id / f"{source_id}.exceptions.json",
    }


@pytest.mark.parametrize("source_id", SOURCES)
def test_original_full_accounting_and_scoped_residuals(source_id: str) -> None:
    paths = _paths(source_id)
    config = load_source_config(paths["source"])
    doc = config.document
    roster = source_roster_entry(source_id)
    assert doc["config_purpose"] == "SOURCE_PREPARATION"
    assert doc["binding"]["identity_class"] == "ORIGINAL_SOURCE"
    assert doc["binding"]["source_sha256"] == roster["source_sha256"]
    assert len(doc["physical_slots"]) == roster["physical_columns"]
    assert len(doc["items"]) == roster["original_items"]
    assert len(doc["questions"]) == roster["original_items"]
    assert len(doc["coverage"]["physical_slots_included"]) == roster["physical_columns"]
    assert len(doc["coverage"]["items_included"]) == roster["original_items"]
    assert len(doc["response_slots"]) > 100
    assert doc["respondents"]["source_native_key_slot"] is not None
    assert doc["weight_slots"] == []
    assert all(item["implementation_id"] for item in doc["items"])
    assert any(r["residual_id"].endswith("-NATIVE-ROW-KEY") for r in doc["residuals"])
    assert any(r["residual_id"].endswith("-ROUTING-UNKNOWN") for r in doc["residuals"])
    assert any(r["residual_id"].endswith("-WEIGHT-HELD") for r in doc["residuals"])
    assert any(r["residual_id"].endswith("-MULTISELECT-AGGREGATION") for r in doc["residuals"])


@pytest.mark.parametrize("source_id", SOURCES)
def test_fixture_identity_and_authority_are_separate(source_id: str) -> None:
    paths = _paths(source_id)
    original = load_source_config(paths["source"]).document
    fixture = load_source_config(paths["fixture_config"]).document
    assert fixture["config_purpose"] == "NONRESPONDENT_FIXTURE"
    assert fixture["binding"]["identity_class"] == "NONRESPONDENT_FIXTURE"
    assert fixture["binding"]["source_sha256"] != original["binding"]["source_sha256"]
    assert fixture["binding"]["source_sha256"] != fixture["identity"]["expected_source_sha256"]
    assert all(s["scope_envelope"].get("fixture_only") is True and s["scope_envelope"].get("grade") == "NONRESPONDENT_FIXTURE_ONLY"
               for s in fixture["authority"]["snapshots"])
    assert all(s["scope_envelope"].get("fixture_only") is not True for s in original["authority"]["snapshots"])
    assert fixture["binding"]["fixture_provenance"]["original_source_sha256"] == original["identity"]["expected_source_sha256"]


@pytest.mark.parametrize("source_id", SOURCES)
def test_native_release_and_p3_key_extraction(source_id: str) -> None:
    paths = _paths(source_id)
    stored = json.loads(paths["results"].read_text(encoding="utf-8"))
    fixture_cfg = load_source_config(paths["fixture_config"])
    stream = load_fixture_stream(paths["fixture"])
    fixture_doc = json.loads(paths["fixture"].read_text(encoding="utf-8"))
    keys = row_native_keys_from_transport(fixture_cfg, stream=stream)
    assert keys is not None and len(keys) == 6
    assert all(value.kind == "R157_NONRESPONDENT_FIXTURE_KEY" for value in keys.values())
    projection = build_governed_c11_projection(fixture_cfg, row_native_keys=keys)
    release = build_validated_c11_release_from_config(fixture_cfg, stream=stream)
    assert release.release_ref.as_dict() == stored["native_validation"]["release"]["release_ref"]
    assert projection.projection_identity_ref.as_dict() == stored["native_validation"]["projection"]["projection_identity_ref"]
    assert sum(isinstance(obj, AuthoritySnapshot) for obj in release.public_objects) == 7
    assert stored["native_validation"]["expected_match"] is True
    assert fixture_doc["expected_results"]["response_event_count"] == len(fixture_doc["expected_results"]["canonical_values"])
    assert release.release_ref.as_dict() == stored["native_validation"]["release"]["release_ref"]


@pytest.mark.parametrize("source_id", SOURCES)
def test_original_refuses_without_decoded_keys(source_id: str) -> None:
    paths = _paths(source_id)
    original = load_source_config(paths["source"])
    fixture_stream = load_fixture_stream(paths["fixture"])
    with pytest.raises(Exception, match="row_native_keys|source_native_key_slot"):
        build_governed_c11_projection(original)
    with pytest.raises(Exception, match="SHA|binding|key|row"):
        build_validated_c11_release_from_config(original, stream=fixture_stream)


@pytest.mark.parametrize("source_id", SOURCES)
def test_reader_transport_is_metadata_only(source_id: str) -> None:
    paths = _paths(source_id)
    config = load_source_config(paths["source"])
    reader = reader_configuration_from_config(config)
    assert reader.source_sha256 == config.original_source_sha256
    assert reader.encoding is None
    request = source_read_request_from_config(
        config, host="R157_PREPARATION_HOST", purpose="SOURCE_CONFIGURATION_PREPARATION",
        consumer_use="R157_WVS_LANE_CONFIGURATION",
        semantic_use_scope=("response_rule_configuration", "coordinate_configuration"))
    assert request.source_sha256 == config.original_source_sha256
    assert request.source_format == "SAV"
    assert request.custody_locator_binding == config.document["identity"]["locator"]["locator_id"]


def test_manifests_and_lane_return_exist() -> None:
    for source_id in SOURCES:
        paths = _paths(source_id)
        for key in ("source", "accounting", "fixture_config", "fixture", "results", "manifest", "exceptions"):
            assert paths[key].is_file(), (source_id, key)
        manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
        assert manifest["no_drop"] is True
        assert manifest["native_release_ref"]["kind"] == "C11LogicalRelease"
    lane = json.loads((VALIDATION_ROOT / "SRC33/LANE_RETURN.json").read_text(encoding="utf-8"))
    assert lane["sources"] and len(lane["sources"]) == 3
    assert lane["aggregate"]["no_drop_all_sources"] is True
    assert lane["aggregate"]["fixture_native_releases"] == 3
