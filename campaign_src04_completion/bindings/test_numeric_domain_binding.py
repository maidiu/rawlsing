import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState  # noqa: E402
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream, physical_value_binding_key  # noqa: E402
from campaign_src04_completion.bindings import numeric_domain_binding as N  # noqa: E402

BASE = json.loads((ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json").read_text())


def _slot(config, name):
    return next(s for s in config["response_slots"] if s["slot"]["name"] == name)


def _cells():
    q715 = _slot(BASE, "q715withoutmorocco")["slot"]
    q716 = _slot(BASE, "q716withoutmorocco")["slot"]
    return (
        PhysicalCell(1, q715["ordinal"], q715["name"], 1234.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, q716["ordinal"], q716["name"], 2000.25, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, q715["ordinal"], q715["name"], 0.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, q716["ordinal"], q716["name"], 1500.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(3, q715["ordinal"], q715["name"], 9999998.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(3, q716["ordinal"], q716["name"], 9999999.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
    )


def test_apply_preserves_literal_values_and_existing_special_states():
    applied = N.apply_observed_domain(BASE, _cells())
    cfg = applied["config"]
    for name, values in (("q715withoutmorocco", {1234.5, 0.0}), ("q716withoutmorocco", {2000.25, 1500.0})):
        slot = _slot(cfg, name)
        raws = {v["raw_value"] for v in slot["values"] if v.get("response_state") == "SUBSTANTIVE_RESPONSE"}
        assert values.issubset(raws)
        assert all(v["canonical_value"] is None for v in slot["values"] if v["raw_value"] in values)
    # Stored special codes retain their existing exact rules, not new substantive ones.
    q715 = _slot(cfg, "q715withoutmorocco")
    special = next(v for v in q715["values"] if v["raw_value"] == 9999998.0)
    assert special["response_state"] == "DK"
    special = next(v for v in q715["values"] if v["raw_value"] == 9999993.0)
    assert special["response_state"] == "MISSING"
    special = next(v for v in q715["values"] if v["raw_value"] == 9999994.0)
    assert special["response_state"] == "SOURCE_SPECIFIC_SPECIAL"
    q716 = _slot(cfg, "q716withoutmorocco")
    special = next(v for v in q716["values"] if v["raw_value"] == 9999999.0)
    assert special["response_state"] == "REFUSAL"


def test_added_literal_values_have_distinct_physical_keys():
    applied = N.apply_observed_domain(BASE, _cells())
    for name in N.TARGET_SLOTS:
        slot = _slot(applied["config"], name)
        keys = [physical_value_binding_key(v["raw_value"], PhysicalMissingState(v["missing_state"]),
                                           v.get("source_missing_declaration")) for v in slot["values"]]
        assert len(keys) == len(set(keys))


def test_new_runtime_config_is_schema_valid_and_has_no_values_from_unrelated_slots():
    applied = N.apply_observed_domain(BASE, _cells())
    out = applied["config"]
    N.validate_source_config(out)
    assert len(out["response_slots"]) == len(BASE["response_slots"])
    assert len(out["coordinate_slots"]) == len(BASE["coordinate_slots"])


def test_wrong_source_and_wrong_config_refuse_before_cell_iteration():
    fake = ExactPhysicalCellStream(source_sha256="f" * 64, row_count=BASE["binding"]["row_count"],
                                   cell_iter_factory=lambda: ())
    try:
        N.build_numeric_domain_runtime_config(BASE, fake)
    except N.NumericDomainBindingError as exc:
        assert "transport source SHA" in str(exc)
    else:
        raise AssertionError("wrong source accepted")
    try:
        N.build_numeric_domain_runtime_config(BASE, fake, expected_config_canonical_sha256="e" * 64)
    except N.NumericDomainBindingError as exc:
        assert "config hash" in str(exc)
    else:
        raise AssertionError("wrong config accepted")


def test_unadmitted_object_refuses():
    try:
        N.build_numeric_domain_runtime_config(BASE, ["not-a-transport"])
    except N.NumericDomainBindingError as exc:
        assert "admitted" in str(exc)
    else:
        raise AssertionError("unadmitted object accepted")


def test_foreign_or_mutated_config_refuses():
    mutated = json.loads(json.dumps(BASE))
    mutated["config_id"] = mutated["config_id"] + "-FOREIGN"
    try:
        N.build_numeric_domain_runtime_config(mutated, ExactPhysicalCellStream(
            source_sha256=N.SOURCE_SHA256, row_count=BASE["binding"]["row_count"], cell_iter_factory=lambda: ()))
    except N.NumericDomainBindingError as exc:
        assert "foreign/mutated config" in str(exc)
    else:
        raise AssertionError("mutated config accepted")


def _fixture_base(fixture_sha: str, rows: int):
    import copy
    from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, semantic_hash
    from rawlsing_next.source_configuration.schema import canonical_config_hash, validate_source_config

    cfg = copy.deepcopy(BASE)
    fixture_id = "R157-SRC04-NUMERIC-DOMAIN-NONRESPONDENT"
    new_auths = []
    ref_map = {}
    for old in cfg["authority"]["snapshots"]:
        new = copy.deepcopy(old)
        scope = copy.deepcopy(new["scope_envelope"])
        scope.update({"fixture_only": True, "grade": "NONRESPONDENT_FIXTURE_ONLY",
                      "fixture_id": fixture_id, "source_id": "SRC04",
                      "source_sha256": N.SOURCE_SHA256, "original_source_sha256": N.SOURCE_SHA256})
        new["scope_envelope"] = scope
        new["typed_state"] = "ALLOW"
        new["decision_state"] = "ALLOW"
        new["authority_content_hash"] = semantic_hash({
            "authority_id": new["authority_id"], "authority_version": new["authority_version"],
            "authority_kind": new["authority_kind"], "decision_state": "ALLOW",
            "governed_operations": new["governed_operations"],
            "governed_object_families": new["governed_object_families"],
            "scope_envelope": scope,
        })
        ref_map[old["authority_id"]] = {"authority_id": new["authority_id"],
                                        "authority_version": new["authority_version"],
                                        "authority_content_hash": new["authority_content_hash"]}
        new_auths.append(new)

    def remap(v):
        if isinstance(v, dict):
            if set(v) == {"authority_id", "authority_version", "authority_content_hash"}:
                return ref_map.get(v["authority_id"], v)
            return {k: remap(x) for k, x in v.items()}
        if isinstance(v, list):
            return [remap(x) for x in v]
        return v

    cfg = remap(cfg)
    cfg["authority"]["snapshots"] = new_auths
    cfg["authority"]["required_refs"] = [ref_map[a["authority_id"]] for a in new_auths]
    cfg["authority"]["projection_authority_ref"] = ref_map[cfg["authority"]["projection_authority_ref"]["authority_id"]]
    cfg["authority"]["replay_authority_ref"] = ref_map[cfg["authority"]["replay_authority_ref"]["authority_id"]]

    uni = copy.deepcopy(cfg["universe"]["universes"][0])
    uni["authority_snapshot_refs"] = [ref_map[a["authority_id"]] for a in new_auths if a["authority_kind"] == "SOURCE_SEMANTICS_TOPOLOGY"][:1]
    uni.update({"raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:SRC04",
                "study_product_release": "R157_FIXTURE/SRC04",
                "instrument_release": "R157_FIXTURE_INSTRUMENT/SRC04",
                "country_geography": "FIXTURE_MULTI_COUNTRY",
                "sampling_geography": "FIXTURE_NONPROBABILITY",
                "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
                "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
                "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
                "respondent_namespace": "urn:rawlsing:r157:fixture:SRC04",
                "source_artifact_import_lineage": "R157_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE"})
    cfg["universe"] = {"universes": [uni]}
    fixture_universe_ref = EmpiricalUniverse(**uni).ref.as_dict()
    for q in cfg["questions"]:
        q["empirical_universe_ref"] = fixture_universe_ref

    cfg["binding"] = {
        "identity_class": "NONRESPONDENT_FIXTURE", "source_sha256": fixture_sha, "row_count": rows,
        "source_snapshot_ref": {"kind": "FIXTURE_SNAPSHOT", "object_id": f"urn:rawlsing:r157:fixture:{fixture_id}",
                                "content_hash": fixture_sha},
        "fixture_provenance": {
            "fixture_id": fixture_id,
            "provenance": "Repository-generated nonrespondent numeric-domain fixture; no original respondents represented.",
            "authority_grade": "NONRESPONDENT_FIXTURE_ONLY", "original_source_id": "SRC04",
            "original_source_sha256": N.SOURCE_SHA256, "no_original_respondents": True,
            "fixture_study_product_id": "R157_FIXTURE/SRC04",
            "fixture_release_id": "R157_FIXTURE_RELEASE/SRC04",
            "fixture_instrument_release_id": "R157_FIXTURE_INSTRUMENT/SRC04",
        },
    }
    cfg["respondents"] = {
        "subject_unit": "NONRESPONDENT_FIXTURE_ROW", "respondent_namespace": "urn:rawlsing:r157:fixture:SRC04",
        "respondent_key_pattern": "FIXTURE-SRC04-ROW-{row_ordinal:03d}",
        "source_native_key_slot": None, "identity_map_authority_ref": None,
        "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY",
    }
    cfg["config_id"] = "R157-SRC04-NUMERIC-DOMAIN-NONRESPONDENT"
    cfg["config_purpose"] = "NONRESPONDENT_FIXTURE"
    cfg["config_revision"] = 1
    keep_slots = {"q715withoutmorocco", "q716withoutmorocco", "country"}
    cfg["physical_slots"] = [p for p in cfg["physical_slots"] if p["name"] in keep_slots]
    cfg["items"] = [i for i in cfg["items"] if i["source_variable_code"] in keep_slots]
    cfg["questions"] = [q for q in cfg["questions"] if q["question_id"] in N.TARGET_SLOTS]
    cfg["response_slots"] = [s for s in cfg["response_slots"] if s["slot"]["name"] in N.TARGET_SLOTS]
    cfg["coordinate_slots"] = [s for s in cfg["coordinate_slots"] if s["slot"]["name"] == "country"]
    cfg["routing"] = [r for r in cfg["routing"] if r["question_id"] in N.TARGET_SLOTS]
    cfg["coverage"] = {"physical_slots_total": 181, "items_total": 181,
                       "partial_scope_reason": "Nonrespondent numeric-domain fixture for q715/q716 and country.",
                       "not_a_lane_config": True}
    cfg["supported_scope"] = {
        "scope_id": "SRC04-NUMERIC-DOMAIN-FIXTURE", "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
        "declared_supported": True, "supported_question_ids": list(N.TARGET_SLOTS),
        "native_validation_expectation": "POSITIVE_RELEASE",
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS",
        "supported_form_slice": "NONRESPONDENT_NUMERIC_DOMAIN_FIXTURE",
        "notes": ["Fixture-only identity/authority; not original-source qualification."],
    }
    cfg["residuals"] = [{"residual_id": "SRC04-NUMERIC-FIXTURE-ONLY", "scope": "SRC04", "field": "authority.snapshots",
                         "status": "FIXTURE_ONLY", "reason": "Fixture authority is not original-source authority.",
                         "dependent_operation": "original-source execution", "unaffected_scope": "fixture native validation",
                         "owner": "SRC04 lane B", "next_step": "Keep separate from original config."}]
    validate_source_config(cfg)
    return cfg


def test_nonrespondent_numeric_domain_fixture_native_validation():
    from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
    from rawlsing_next.source_configuration.fixture import fixture_document_sha256
    from rawlsing_next.pre553_c11_integrity import RespondentEvent
    from rawlsing_next.pre553_empirical_objects import EmpiricalCoordinateFact

    q715 = _slot(BASE, "q715withoutmorocco")["slot"]
    q716 = _slot(BASE, "q716withoutmorocco")["slot"]
    country = next(p for p in BASE["physical_slots"] if p["name"] == "country")
    rows = 3
    cells = []
    values = [(1234.5, 2000.25), (9999998.0, 9999999.0), (0.0, 1500.0)]
    country_values = [1.0, 2.0, 3.0]
    for row, ((v715, v716), cv) in enumerate(zip(values, country_values), 1):
        cells.append({"row_ordinal": row, "variable_ordinal": q715["ordinal"], "variable_name": q715["name"],
                      "raw_value": v715, "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None})
        cells.append({"row_ordinal": row, "variable_ordinal": q716["ordinal"], "variable_name": q716["name"],
                      "raw_value": v716, "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None})
        cells.append({"row_ordinal": row, "variable_ordinal": country["ordinal"], "variable_name": country["name"],
                      "raw_value": cv, "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None})
    doc = {"schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
           "fixture_id": "R157-SRC04-NUMERIC-DOMAIN-NONRESPONDENT",
           "identity_class": "NONRESPONDENT_FIXTURE", "nonrespondent": True,
           "row_count": rows, "cells": cells}
    fixture_sha = fixture_document_sha256(doc)
    doc["fixture_source_sha256"] = fixture_sha
    cfg = _fixture_base(fixture_sha, rows)
    stream = ExactPhysicalCellStream(source_sha256=fixture_sha, row_count=rows, cell_iter_factory=lambda: tuple(
        PhysicalCell(c["row_ordinal"], c["variable_ordinal"], c["variable_name"], c["raw_value"],
                     PhysicalMissingState(c["missing_state"]), c["source_missing_declaration"]) for c in cells))
    from rawlsing_next.source_configuration.schema import canonical_config_hash
    runtime = N.build_numeric_domain_runtime_config(
        cfg, stream, expected_source_sha256=fixture_sha,
        expected_config_canonical_sha256=canonical_config_hash(cfg))
    release = build_validated_c11_release_from_config(runtime["config"], stream=stream)
    events = [o for o in release.public_objects if isinstance(o, RespondentEvent)]
    coords = [o for o in release.public_objects if isinstance(o, EmpiricalCoordinateFact)]
    assert len(events) == 6 and len(coords) == 3
    states = {(e.response_state) for e in events}
    assert "DK" in states and "REFUSAL" in states
    raws = {e.raw_response_value["$raw_physical_value"]["token"].get("bits") for e in events}
    assert len([e for e in events if e.response_state == "SUBSTANTIVE_RESPONSE"]) == 4
    assert runtime["added_rule_counts"]["q715withoutmorocco"] >= 2
