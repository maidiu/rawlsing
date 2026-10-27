"""Focused R157 P0 source-configuration foundation tests."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import fields
import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pandas as pd
import pytest

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    RespondentEvent,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    GovernedC11Projection,
    PhysicalSlot,
)
from rawlsing_next.source_configuration.errors import (
    SourceConfigurationBindingError,
    SourceConfigurationSchemaError,
)
from rawlsing_next.source_configuration.evidence import lane_inputs, load_manifest, load_source_roster
from rawlsing_next.source_configuration.factory import (
    _respondents,
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import (
    canonical_config_hash,
    config_file_sha256,
    load_source_config,
    validate_source_config,
)

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
FIXTURE = ROOT / "source_pre553_validation/foundation/fixtures/SRC09_q101_nonrespondent.json"
JSON_SCHEMA = ROOT / "rawlsing_next/source_configuration/schema/source_configuration.schema.json"
OWNER_MAPPING = ROOT / "rawlsing_next/source_configuration/schema/OWNER_API_MAPPING.json"


def _config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _row_order(events, projection: GovernedC11Projection):
    row_by_object = {r.ref.object_id: index for index, r in enumerate(projection.respondents, 1)}
    return sorted(events, key=lambda event: row_by_object[dict(event.scoped_respondent_ref)["object_id"]])


def test_importable_schema_and_committed_example_validate():
    document = _config()
    validate_source_config(document)
    cfg = load_source_config(CONFIG)
    assert cfg.source_id == "SRC09"
    assert cfg.identity_class == "NONRESPONDENT_FIXTURE"
    assert cfg.active_row_count == 9
    assert canonical_config_hash(cfg) == canonical_config_hash(document)
    import hashlib
    assert config_file_sha256(CONFIG) == hashlib.sha256(CONFIG.read_bytes()).hexdigest()
    jsonschema.validate(document, json.loads(JSON_SCHEMA.read_text(encoding="utf-8")))


def test_fixture_builds_actual_governed_projection_and_native_release():
    cfg = load_source_config(CONFIG)
    stream = load_fixture_stream(FIXTURE)
    projection = build_governed_c11_projection(cfg)
    assert isinstance(projection, GovernedC11Projection)
    assert projection.projection_identity_ref.kind == "C11_SEMANTIC_PROJECTION"
    assert projection.expected_source_sha256 == cfg.active_source_sha256
    assert len(projection.respondents) == 9
    assert len(projection.response_slots) == 1
    assert projection.response_slots[0].slot == PhysicalSlot(124, "q101")
    assert len(projection.coordinate_slots) == 1
    assert len(projection.routing) == 9
    assert projection.source_relations.state == "DISTINCT_BY_DEFAULT"
    release = build_validated_c11_release_from_config(cfg, stream=stream)
    assert isinstance(release, C11LogicalRelease)
    assert release.source_artifact_ref.content_hash == cfg.active_source_sha256
    assert set(release.m01_m18_coverage) == {f"M{i:02d}" for i in range(1, 19)}


def test_fixture_expected_results_match_native_release_by_row():
    cfg = load_source_config(CONFIG)
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected_results"]
    projection = build_governed_c11_projection(cfg)
    release = build_validated_c11_release_from_config(cfg, stream=load_fixture_stream(FIXTURE))
    events = _row_order([x for x in release.public_objects if isinstance(x, RespondentEvent)], projection)
    coords = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    routing = [x for x in release.public_objects if isinstance(x, RoutingEligibilityFact)]
    assert len(events) == expected["response_event_count"]
    assert len(coords) == expected["coordinate_fact_count"]
    assert len(routing) == expected["routing_fact_count"]
    assert [x.response_state for x in events] == expected["response_states"]
    assert [x.canonical_response_value_if_authorized for x in events] == expected["canonical_values"]
    assert {x.response_state for x in events} == {
        "SUBSTANTIVE_RESPONSE", "MISSING", "DK", "SOURCE_SPECIFIC_SPECIAL", "REFUSAL",
    }
    assert release.m01_m18_coverage["M09"] == ("WeightMeasureFact|TypedAbsence",)
    assert release.m01_m18_coverage["M11"] == ("SourceUniverseRelation|DISTINCT_BY_DEFAULT",)


def test_fixture_stream_and_permitted_physical_incidence_agree():
    cfg = load_source_config(CONFIG)
    variables = (
        PhysicalVariable(1, "country", "double", "Country code", {}, (), {}, {}),
        PhysicalVariable(124, "q101", "double", "q101", {}, (), {}, {}),
    )
    frame = pd.DataFrame({
        "country": [1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0],
        "q101": [1.0, 2.0, 3.0, 4.0, -1.0, 7.0, 8.0, 9.0, None],
    })
    incidence = PhysicalSourceIncidence(
        source_sha256=cfg.active_source_sha256,
        source_format="SAV",
        row_count=9,
        variables=variables,
        reader_configuration={"fixture": "R157_P0_NONRESPONDENT"},
        file_metadata={"fixture": "R157_P0_NONRESPONDENT"},
        _frame=frame,
    )
    from_stream = build_validated_c11_release_from_config(cfg, stream=load_fixture_stream(FIXTURE))
    from_incidence = build_validated_c11_release_from_config(cfg, incidence=incidence)
    assert from_incidence.release_ref == from_stream.release_ref
    assert from_incidence.semantic_release_hash == from_stream.semantic_release_hash


def test_configured_native_key_slot_requires_exact_row_keys():
    universe = SimpleNamespace(ref=ExactRef(
        "UNIVERSE", "urn:test:r157:key-slot", semantic_hash({"key_slot": True})))
    doc = {
        "binding": {},
        "respondents": {
            "respondent_key_pattern": "ROW-{row_ordinal}",
            "identity_map_authority_ref": None,
            "source_native_key_slot": {"ordinal": 1, "name": "native_id"},
        },
    }
    with pytest.raises(SourceConfigurationBindingError, match="row_native_keys"):
        _respondents(doc, active_rows=2, universes=(universe,))
    observed = ExactRef(
        "SOURCE_NATIVE_RESPONDENT_KEY", "urn:test:r157:key:1",
        semantic_hash({"native_key": "one"}))
    respondents = _respondents(
        doc, active_rows=2, universes=(universe,),
        row_native_keys={1: observed, 2: TypedAbsence("UNKNOWN")},
    )
    assert respondents[0].source_native_respondent_key_ref_or_typed_absence == observed
    assert isinstance(respondents[1].source_native_respondent_key_ref_or_typed_absence, TypedAbsence)


def test_wrong_source_sha_and_row_count_are_refused():
    cfg = load_source_config(CONFIG)
    cells = tuple(load_fixture_stream(FIXTURE).iter_cells())
    wrong_sha = ExactPhysicalCellStream("f" * 64, 9, lambda: cells)
    with pytest.raises(Exception, match="SHA|binding|mismatch"):
        build_validated_c11_release_from_config(cfg, stream=wrong_sha)
    wrong_rows = ExactPhysicalCellStream(cfg.active_source_sha256, 8, lambda: cells)
    with pytest.raises(Exception, match="row count|binding|cardinality"):
        build_validated_c11_release_from_config(cfg, stream=wrong_rows)


def test_original_binding_cannot_reuse_fixture_identity_or_authority():
    document = deepcopy(_config())
    document["config_purpose"] = "SOURCE_PREPARATION"
    document["supported_scope"]["purpose"] = "SOURCE_PREPARATION"
    document["binding"]["identity_class"] = "ORIGINAL_SOURCE"
    document["binding"]["source_sha256"] = document["identity"]["expected_source_sha256"]
    document["binding"]["row_count"] = document["identity"]["source_row_count"]
    document["binding"]["source_snapshot_ref"] = document["identity"]["source_snapshot_retention_ref"]
    document["binding"].pop("fixture_provenance")
    with pytest.raises(SourceConfigurationSchemaError, match="fixture/test-only authority"):
        validate_source_config(document)


def test_synthetic_original_universe_is_refused():
    document = deepcopy(_config())
    document["config_purpose"] = "SOURCE_PREPARATION"
    document["supported_scope"]["purpose"] = "SOURCE_PREPARATION"
    document["binding"]["identity_class"] = "ORIGINAL_SOURCE"
    document["binding"]["source_sha256"] = document["identity"]["expected_source_sha256"]
    document["binding"]["row_count"] = document["identity"]["source_row_count"]
    document["binding"]["source_snapshot_ref"] = document["identity"]["source_snapshot_retention_ref"]
    document["binding"].pop("fixture_provenance")
    for snapshot in document["authority"]["snapshots"]:
        snapshot["scope_envelope"].pop("fixture_only", None)
        snapshot["scope_envelope"].pop("grade", None)
    document["universe"]["universes"][0]["sampling_design_regime"] = "TEST_ONLY"
    with pytest.raises(SourceConfigurationSchemaError, match="synthetic/default universe"):
        validate_source_config(document)


def test_private_absolute_path_is_refused():
    document = deepcopy(_config())
    document["evidence"]["limits"].append("/Users/someone/private/source.sav")
    with pytest.raises(SourceConfigurationSchemaError, match="private/absolute"):
        validate_source_config(document)


def test_owner_api_mapping_matches_actual_projection_fields():
    mapping = json.loads(OWNER_MAPPING.read_text(encoding="utf-8"))
    actual = {field.name for field in fields(GovernedC11Projection)}
    assert set(mapping["projection_field_mapping"]) == actual
    assert mapping["native_owner"]["class"] == "GovernedC11Projection"
    assert mapping["native_owner"]["sha256"] == __import__("hashlib").sha256(
        (ROOT / "rawlsing_next/pre553_source_backed_c11_facade.py").read_bytes()).hexdigest()
    assert mapping["native_validators"][0]["callable"] == "build_validated_source_backed_c11_release_from_stream"


def test_evidence_package_is_portable_and_complete():
    manifest = load_manifest()
    roster = load_source_roster()
    assert manifest["counts"]["sources"] == 35
    assert manifest["counts"]["physical_columns"] == 18_413
    assert manifest["counts"]["codebook_rows"] == 18_276
    assert manifest["counts"]["original_items"] == 18_276
    assert manifest["counts"]["exact_relation_joins"] == 18_250
    assert manifest["counts"]["unmatched_explicit_ids"] == 26
    assert roster["counts"]["sources"] == 35
    assert len(roster["sources"]) == 35
    assert sum(x["physical_columns"] for x in roster["sources"]) == 18_413
    assert sum(x["codebook_rows"] for x in roster["sources"]) == 18_276
    assert sum(x["original_items"] for x in roster["sources"]) == 18_276
    assert sum(x["exact_relation_matches"] for x in roster["sources"]) == 18_250
    assert all(not str(x).startswith("/Users/") for x in json.dumps(manifest).split('"'))


def test_every_lane_has_frozen_inputs_and_disjoint_source_coverage():
    lanes = json.loads((ROOT / "SOURCE_PRE553_PLAN/LANES.json").read_text(encoding="utf-8"))["lanes"]
    seen: list[str] = []
    for lane in lanes:
        frozen = lane_inputs(lane["lane_id"])
        assert frozen["branch"] == lane["branch"]
        assert frozen["source_ids"] == lane["source_ids"]
        assert frozen["config_contract"]["validator"] == "rawlsing_next.source_configuration.schema.validate_source_config"
        assert frozen["config_contract"]["factory"] == "rawlsing_next.source_configuration.factory.build_governed_c11_projection"
        seen.extend(frozen["source_ids"])
    assert len(seen) == 35 and len(set(seen)) == 35
