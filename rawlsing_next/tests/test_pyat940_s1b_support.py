"""Sourcefree synthetic fixtures for the recovered S1-B R157 seam.

All fixture bytes are generated under a private temporary proof root.  No
original35 respondent row, source byte, SAV/DTA original file, or source-read
right is used.  These helpers build the smallest closed R157 configuration and
write real SAV/DTA files so the actual decoder and facade are exercised.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, ExactRef, exact_ref
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(kind: str, object_id: str) -> dict[str, str]:
    return {
        "kind": kind,
        "object_id": object_id,
        "content_hash": sha256_text(f"{kind}:{object_id}"),
    }


def authority_ref(authority_id: str) -> dict[str, str]:
    return {
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": sha256_text(f"authority:{authority_id}"),
    }


def _authority_snapshot(authority_id: str, families: Sequence[str], *, fixture_id: str, kind: str = "SOURCE_SEMANTICS_TOPOLOGY", fixture_only: bool = True) -> dict[str, Any]:
    return {
        "typed_state": "ALLOW",
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": ref(
            "REPLAY_ROOT", f"urn:rawlsing:s1b:{authority_id}:root"),
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": sha256_text(f"authority:{authority_id}"),
        "authority_kind": kind,
        "decision_state": "ALLOW",
        "governed_operations": [f"{authority_id}-OP"],
        "governed_object_families": list(families),
        "scope_envelope": (
            {
                "fixture_only": True,
                "grade": "NONRESPONDENT_FIXTURE_ONLY",
                "fixture_id": fixture_id,
            }
            if fixture_only
            else {
                "fixture_only": False,
                "grade": "SOURCE_PREPARATION_ALLOW",
                "source_id": "SRC09",
            }
        ),
        "effective_time_or_interval": "S1B_SYNTHETIC_FIXTURE",
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": sha256_text(f"fp:{authority_id}"),
        "replay_protocol_ref": ref(
            "REPLAY_PROTOCOL", f"urn:rawlsing:s1b:{authority_id}:replay"),
    }


def _typed_absence(state: str) -> dict[str, Any]:
    return {"typed_absence_state": state, "detail": None}


def _physical_slot(ordinal: int, name: str, *, disposition: str) -> dict[str, Any]:
    return {
        "ordinal": ordinal,
        "name": name,
        "label": f"Synthetic {name}",
        "storage_type": "double",
        "original_type": "F8.0",
        "storage_width": "8",
        "measure": "scale" if name == "q101" else "nominal",
        "value_labels": {"1.0": "one", "7.0": "DK"} if name == "q101" else {},
        "missing_declarations": None,
        "mr_declarations": None,
        "codebook_mapping": {
            "var_name": name,
            "row_hash": sha256_text(f"codebook:{name}"),
            "status": "EXACT",
        },
        "disposition": disposition,
        "disposition_reason": "S1-B nonrespondent synthetic binding.",
    }


def make_config(
    *,
    source_format: str,
    active_source_sha256: str,
    row_count: int,
    keyed: bool = True,
    values: Sequence[Any] = (1.0, 2.0, 0.0, 7.0, 8.0, -1.0, None),
    user_missing_range: bool = False,
    extended_missing: bool = False,
    response_state_overrides: Mapping[Any, str] | None = None,
    occurrences: int = 1,
    routing_state: str = "ELIGIBLE_APPLICABLE",
    duplicate_slot_owner: bool = False,
    include_slot_owner_set: bool = True,
    fixture_instrument_release_id: str = "S1B_FIXTURE_INSTRUMENT_R1",
    purpose: str = "NONRESPONDENT_FIXTURE",
    original: bool = False,
) -> dict[str, Any]:
    """Build one closed R157 configuration bound to a synthetic source SHA."""
    fixture_id = "S1B_NONRESPONDENT_FIXTURE"
    original_source_sha = (
        active_source_sha256
        if original
        else sha256_text("S1B_ORIGINAL_SOURCE_IDENTITY_NOT_READ")
    )
    if not original:
        assert active_source_sha256 != original_source_sha
    source_format = source_format.upper()
    if source_format not in {"SAV", "DTA"}:
        raise ValueError("source_format must be SAV or DTA")
    decoder_owner = (
        "rawlsing_next.pre553_physical_decoder.decode_sav"
        if source_format == "SAV"
        else "rawlsing_next.pre553_physical_decoder.decode_dta"
    )
    fixture_study = "S1B_FIXTURE_STUDY"
    fixture_release = "S1B_FIXTURE_RELEASE"
    source_auth = authority_ref("S1B-SOURCE-AUTH")
    mapping_auth = authority_ref("S1B-MAPPING-AUTH")
    topology_auth = authority_ref("S1B-TOPOLOGY-AUTH")
    coord_auth = authority_ref("S1B-COORD-AUTH")
    routing_auth = authority_ref("S1B-ROUTING-AUTH")
    replay_auth = authority_ref("S1B-REPLAY-AUTH")
    projection_auth = authority_ref("S1B-PROJECTION-AUTH")
    snapshots = [
        _authority_snapshot("S1B-SOURCE-AUTH", ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"), fixture_id=fixture_id, fixture_only=not original),
        _authority_snapshot("S1B-MAPPING-AUTH", ("RespondentEvent@1.0.0",), fixture_id=fixture_id, kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION", fixture_only=not original),
        _authority_snapshot("S1B-TOPOLOGY-AUTH", ("RespondentEvent@1.0.0",), fixture_id=fixture_id, fixture_only=not original),
        _authority_snapshot("S1B-COORD-AUTH", ("EmpiricalCoordinateFact@1.0.0",), fixture_id=fixture_id, fixture_only=not original),
        _authority_snapshot("S1B-ROUTING-AUTH", ("RoutingEligibilityFact@1.0.0",), fixture_id=fixture_id, fixture_only=not original),
        _authority_snapshot("S1B-REPLAY-AUTH", ("ReplayReceipt@1.0.0",), fixture_id=fixture_id, kind="REPLAY_PROTOCOL", fixture_only=not original),
        _authority_snapshot(
            "S1B-PROJECTION-AUTH",
            ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"),
            fixture_id=fixture_id,
            fixture_only=not original,
        ),
    ]
    universe_payload = {
        "typed_state": "UNIVERSE_IDENTIFIED",
        "authority_snapshot_refs": [source_auth],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": ref(
            "REPLAY_ROOT", "urn:rawlsing:s1b:universe:root"),
        "raw_source_identity": "S1B_SYNTHETIC_NONRESPONDENT",
        "source_family": "S1B_SYNTHETIC_NONRESPONDENT",
        "study_product_release": "S1B_FIXTURE_STUDY/S1B_FIXTURE_RELEASE",
        "instrument_release": fixture_instrument_release_id,
        "country_geography": "US" if original else "NONRESPONDENT_FIXTURE",
        "sampling_geography": "US-NATIONAL" if original else "NONRESPONDENT_FIXTURE",
        "raw_wave": "S1B",
        "canonical_wave_if_governed": None,
        "field_or_reference_time": "S1B_SYNTHETIC",
        "target_population_and_sample_frame": "ADULTS" if original else "NONRESPONDENT_FIXTURE",
        "sampling_design_regime": "S1B_EXACT_DESIGN" if original else "NONRESPONDENT_FIXTURE",
        "respondent_namespace": "urn:rawlsing:s1b:fixture",
        "source_artifact_import_lineage": "S1B_SYNTHETIC_FIXTURE",
        "harmonization_authority_ref": None,
        "source_relation_refs": [],
    }
    universe_ref = EmpiricalUniverse(**universe_payload).ref.as_dict()
    question_ref = ref("QUESTION_NATIVE", "urn:rawlsing:s1b:question:q101")
    coordinate_ref = ref("COORDINATE_NATIVE", "urn:rawlsing:s1b:coordinate:country")
    unit_ref = ref("UNIT_TAXONOMY", "urn:rawlsing:s1b:unit:country")
    topology_ref = ref("RESPONSE_TOPOLOGY", "urn:rawlsing:s1b:topology:q101")
    scalar_topology = ref("RESPONSE_TOPOLOGY", "urn:rawlsing:s1b:topology:q101:scalar")
    risk_ref = ref("RISK_SET", "urn:rawlsing:s1b:risk:q101")
    routing_rule_ref = ref("ROUTING_RULE", "urn:rawlsing:s1b:routing:q101")
    member_ref = ref("MEMBER_SET_REPLAY", "urn:rawlsing:s1b:member:q101")

    overrides = {str(k): v for k, v in (response_state_overrides or {}).items()}

    def physical_classification(value: Any) -> tuple[str, Mapping[str, Any] | None, str]:
        if value is None:
            return "SYSTEM_MISSING", None, "MISSING"
        if user_missing_range and value == 7.0:
            return (
                "FORMAT_USER_MISSING_VALUE",
                {"kind": "discrete", "value": 7.0},
                "DK",
            )
        if extended_missing and value == "a":
            return (
                "FORMAT_EXTENDED_MISSING",
                {"kind": "extended", "reader_token": "a", "stata_token": ".a"},
                "DK",
            )
        if value == 7.0:
            return "OBSERVED_STORAGE_VALUE", None, "DK"
        if value == 8.0:
            return "OBSERVED_STORAGE_VALUE", None, "REFUSAL"
        if value == -1.0:
            return "OBSERVED_STORAGE_VALUE", None, "MISSING"
        return "OBSERVED_STORAGE_VALUE", None, "SUBSTANTIVE_RESPONSE"

    response_values = []
    seen_raw_values = set()
    for raw in values:
        raw_token = ("none", None) if raw is None else (type(raw).__name__, raw)
        if raw_token in seen_raw_values:
            continue
        seen_raw_values.add(raw_token)
        missing_state, declaration, default_state = physical_classification(raw)
        state = overrides.get(str(raw), default_state)
        occurrence_rules = []
        for index in range(occurrences):
            occurrence_rules.append({
                "key": str(index),
                "topology_ref": topology_ref if occurrences > 1 else scalar_topology,
                "multiplicity_order_rank_fields": {
                    "kind": "MULTISELECT" if occurrences > 1 else "SCALAR_SINGULAR",
                    "index": index,
                },
            })
        response_values.append({
            "raw_value": raw,
            "missing_state": missing_state,
            "source_missing_declaration": declaration,
            "response_state": state,
            "occurrences": occurrence_rules,
            "canonical_value": None if state != "SUBSTANTIVE_RESPONSE" else str(raw),
            "transform_authority_ref": None if state != "SUBSTANTIVE_RESPONSE" else mapping_auth,
            "extra_authority_refs": [],
        })

    questions = [{
        "question_id": "q101",
        "empirical_universe_ref": universe_ref,
        "native_question_ref": question_ref,
        "instrument_question_version": "S1B-R1",
        "canonical_question_ref_or_typed_absence": _typed_absence("NOT_AUTHORIZED"),
        "component_subitem_ref_or_typed_absence": _typed_absence("NOT_APPLICABLE"),
        "semantic_authority_ref": mapping_auth,
        "topology_authority_ref": topology_auth,
    }]
    respondents = {
        "subject_unit": "FIXTURE_ROW",
        "respondent_namespace": "urn:rawlsing:s1b:fixture",
        "respondent_key_pattern": "S1B-ROW-{row_ordinal:04d}",
    }
    if keyed:
        respondents["source_native_key_slot"] = {"ordinal": 2, "name": "country"}
        respondents["row_identity_grade"] = "NONRESPONDENT_FIXTURE_KEY_WITNESS"
    physical_slots = [
        _physical_slot(1, "q101", disposition="SUPPORTED_RESPONSE"),
        _physical_slot(2, "country", disposition="SUPPORTED_COORDINATE"),
    ]
    coordinate_slots = [{
        "slot": {"ordinal": 2, "name": "country"},
        "native_coordinate_ref": coordinate_ref,
        "unit_taxonomy_ref": unit_ref,
        "effective_time": "S1B_SYNTHETIC",
        "source_semantic_authority_ref": coord_auth,
        "canonical_coordinate_ref": None,
        "normalization_ref": None,
        "values": [],
        "copy_observed_raw": True,
    }]
    response_slots = [{
        "slot": {"ordinal": 1, "name": "q101"},
        "question_id": "q101",
        "values": response_values,
    }]
    slot_owner_sets = []
    if duplicate_slot_owner:
        # q101 is deliberately emitted by both response and coordinate owners.
        coordinate_slots.append({
            "slot": {"ordinal": 1, "name": "q101"},
            "native_coordinate_ref": coordinate_ref,
            "unit_taxonomy_ref": unit_ref,
            "effective_time": "S1B_SYNTHETIC",
            "source_semantic_authority_ref": coord_auth,
            "canonical_coordinate_ref": None,
            "normalization_ref": None,
            "values": [],
            "copy_observed_raw": True,
        })
        if include_slot_owner_set:
            slot_owner_sets.append({
                "slot": {"ordinal": 1, "name": "q101"},
                "owners": [
                    {
                        "owner_family": "RespondentEvent@1.0.0",
                        "authority_refs": [mapping_auth, projection_auth],
                    },
                    {
                        "owner_family": "EmpiricalCoordinateFact@1.0.0",
                        "authority_refs": [coord_auth, projection_auth],
                    },
                ],
            })
    doc = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": f"S1B-{source_format}-{'KEYED' if keyed else 'ROW'}",
        "config_revision": 1,
        "config_purpose": "SOURCE_PREPARATION" if original else purpose,
        "identity": {
            "source_id": "SRC09",
            "family": "S1B_SYNTHETIC_NONRESPONDENT",
            "wave": "S1B",
            "source_family_id": "S1B_SYNTHETIC_NONRESPONDENT",
            "study_product_id": "S1B_ORIGINAL_STUDY_NOT_READ",
            "release_id": "S1B_ORIGINAL_RELEASE_NOT_READ",
            "instrument_release_id": "S1B_ORIGINAL_INSTRUMENT_NOT_READ",
            "source_artifact_id": "S1B_SYNTHETIC_FIXTURE_FILE",
            "expected_source_sha256": original_source_sha,
            "source_format": source_format,
            "source_row_count": row_count if original else max(1, row_count),
            "source_column_count": 2,
            "source_bytes": 1024,
            "codebook_rows": 2,
            "original_item_count": 1,
            "source_snapshot_retention_ref": {
                "kind": "SOURCE_SNAPSHOT",
                "object_id": "urn:rawlsing:s1b:original-snapshot",
                "content_hash": original_source_sha,
            },
            "metadata_witness_ref": ref("R154_PHYSICAL_METADATA", "urn:rawlsing:s1b:metadata-witness"),
            "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": "S1B_EXTERNAL_LOCATOR_ID"},
            "reader": {
                "decoder_owner": decoder_owner,
                "configuration_ref": ref("READER_CONFIGURATION", "urn:rawlsing:s1b:reader"),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "ORIGINAL_SOURCE" if original else "NONRESPONDENT_FIXTURE",
            "source_sha256": active_source_sha256,
            "row_count": row_count,
            "source_snapshot_ref": {
                "kind": "SOURCE_SNAPSHOT" if original else "FIXTURE_SNAPSHOT",
                "object_id": (
                    "urn:rawlsing:s1b:original-snapshot"
                    if original
                    else f"urn:rawlsing:s1b:fixture:{fixture_id}"
                ),
                "content_hash": active_source_sha256,
            },
            **({} if original else {
                "fixture_provenance": {
                    "fixture_id": fixture_id,
                    "provenance": "Repository-generated nonrespondent S1-B proof fixture.",
                    "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                    "original_source_id": "SRC09",
                    "original_source_sha256": original_source_sha,
                    "no_original_respondents": True,
                    "fixture_study_product_id": fixture_study,
                    "fixture_release_id": fixture_release,
                    "fixture_instrument_release_id": fixture_instrument_release_id,
                }
            }),
        },
        "authority": {
            "snapshots": snapshots,
            "required_refs": [
                source_auth, mapping_auth, topology_auth, coord_auth,
                routing_auth, replay_auth, projection_auth,
            ],
            "projection_authority_ref": projection_auth,
            "replay_authority_ref": replay_auth,
            "projection_identity_ref": ref("C11_PROJECTION", "urn:rawlsing:s1b:projection"),
            "tie_order_ref": ref("TIE_ORDER", "urn:rawlsing:s1b:tie-order"),
            "replay_protocol_version": "S1B_REPLAY@1",
        },
        "universe": {"universes": [universe_payload]},
        "respondents": respondents,
        "questions": questions,
        "physical_slots": physical_slots,
        "items": [{
            "implementation_id": "question_impl.s1b.q101",
            "source_variable_code": "q101",
            "exact_identity_sha256": sha256_text("item:q101"),
            "question_text": "S1-B synthetic nonrespondent item.",
            "disposition": "SUPPORTED_RESPONSE",
            "response_classes": "SCALAR",
            "mapping_status": "SYNTHETIC_EXACT",
            "authority_status": "NONRESPONDENT_FIXTURE_ONLY",
            "evidence_refs": [ref("S1B_EVIDENCE", "urn:rawlsing:s1b:item:q101")],
            "limits": ["No original respondent or original35 source right."],
        }],
        "response_slots": response_slots,
        "coordinate_slots": coordinate_slots,
        "weight_slots": [],
        "routing": [{
            "question_id": "q101",
            "row_selector": "ALL",
            "typed_state": routing_state,
            "risk_set_ref": risk_ref,
            "routing_rule_ref": routing_rule_ref,
            "member_set_replay_ref": member_ref,
            "authority_ref": routing_auth,
            "parent_predicate_refs": [],
            "dependency_refs": [],
        }],
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": _typed_absence("NOT_APPLICABLE"),
            "comparator": _typed_absence("DEFERRED"),
            "discovery": _typed_absence("DEFERRED"),
            "structural": _typed_absence("NOT_APPLICABLE"),
        },
        "supported_scope": {
            "scope_id": "S1B-SYNTHETIC-FIXTURE",
            "purpose": (
                "SOURCE_PREPARATION" if (purpose == "SOURCE_PREPARATION" or original)
                else "P0_EXAMPLE_ONLY" if purpose == "P0_EXAMPLE_FIXTURE"
                else "NONRESPONDENT_FIXTURE_VALIDATION"
            ),
            "declared_supported": True,
            "supported_question_ids": ["q101"],
            "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        },
        "coverage": (
            {
                "physical_slots_total": 2,
                "items_total": 1,
                "physical_slots_included": [1, 2],
                "physical_slots_excluded": [],
                "items_included": ["question_impl.s1b.q101"],
                "items_excluded": [],
            }
            if original
            else {
                "physical_slots_total": 2,
                "items_total": 1,
                "partial_scope_reason": "S1-B nonrespondent synthetic proof slice.",
                "not_a_lane_config": True,
            }
        ),
        "residuals": [],
        "evidence": {
            "source_roster_path": "S1B_SYNTHETIC_EVIDENCE/SOURCE_ROSTER.json",
            "item_index_path": "S1B_SYNTHETIC_EVIDENCE/ITEM_INDEX.jsonl",
            "evidence_manifest_path": "S1B_SYNTHETIC_EVIDENCE/MANIFEST.json",
            "pinned_inputs": [],
            "field_evidence": [],
            "limits": ["Synthetic nonrespondent fixture only."],
        },
        "runtime": {
            "projection_builder": "rawlsing_next.pre553_r157_projection_adapter.build_governed_c11_projection",
            "release_builder": "rawlsing_next.pre553_r157_projection_adapter.build_validated_c11_release_from_config",
            "repository_builder": "rawlsing_next.pre553_r157_projection_adapter.build_source_backed_c11_repository_from_config",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
            "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
            "source_read_owner": "rawlsing_next.pre553_r157_projection_adapter.decode_with_source_read_permission",
            "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
            "reader_encoding_transport": "R157_P3_QUALIFIED_CONFIG_TRANSPORT",
        },
    }
    if slot_owner_sets:
        doc["slot_owner_sets"] = slot_owner_sets
    return doc


def write_fixture(
    directory: Path,
    *,
    source_format: str,
    values: Sequence[Any],
    countries: Sequence[float] | None = None,
    missing_range: bool = False,
    extended_missing: bool = False,
) -> tuple[Path, str, int]:
    """Write a real SAV or DTA nonrespondent fixture and return path/SHA/rows."""
    directory.mkdir(parents=True, exist_ok=True)
    source_format = source_format.upper()
    rows = len(values)
    if countries is None:
        countries = [float((index % 9) + 1) for index in range(rows)]
    if len(countries) != rows:
        raise ValueError("country fixture length must match values")
    frame = pd.DataFrame({"q101": list(values), "country": list(countries)})
    if source_format == "SAV":
        path = directory / "s1b_fixture.sav"
        kwargs: dict[str, Any] = {
            "variable_value_labels": {"q101": {1.0: "one", 7.0: "DK"}},
        }
        if missing_range:
            kwargs["missing_ranges"] = {"q101": [7.0]}
        pyreadstat.write_sav(frame, str(path), **kwargs)
    elif source_format == "DTA":
        path = directory / "s1b_fixture.dta"
        kwargs = {
            "variable_value_labels": {"q101": {1.0: "one", 7.0: "DK"}},
        }
        if extended_missing:
            kwargs["missing_user_values"] = {"q101": ["a"]}
        pyreadstat.write_dta(frame, str(path), **kwargs)
    else:
        raise ValueError("source_format must be SAV or DTA")
    return path, sha256_file(path), rows


def load_fixture_document(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "sha256_text", "sha256_file", "ref", "authority_ref", "make_config",
    "write_fixture", "load_fixture_document", "deepcopy", "exact_ref", "ExactRef",
    "PhysicalMissingState",
]


def build_scenario(
    directory: Path,
    *,
    source_format: str,
    values: Sequence[Any] = (1.0, 2.0, 0.0, 7.0, 8.0, -1.0, None),
    config_kwargs: Mapping[str, Any] | None = None,
):
    """Build a full sourcefree SAV/DTA scenario through the real owners."""
    from rawlsing_next.pre553_r157_projection_adapter import (
        SourceConfig,
        build_governed_c11_projection,
        decode_fixture_config,
        project_c11_candidate_from_config,
        row_native_keys_from_transport,
    )
    from rawlsing_next.pre553_c11_ingest import validate_c11_source_release

    config_kwargs = dict(config_kwargs or {})
    write_missing_range = bool(config_kwargs.pop("missing_range", False))
    write_extended_missing = bool(config_kwargs.pop("extended_missing", False))
    config_user_missing_range = bool(
        config_kwargs.pop("user_missing_range", write_missing_range)
    )
    config_extended_missing = bool(
        config_kwargs.pop("extended_missing_config", write_extended_missing)
    )
    path, source_sha, rows = write_fixture(
        directory,
        source_format=source_format,
        values=values,
        missing_range=write_missing_range,
        extended_missing=write_extended_missing,
    )
    document = make_config(
        source_format=source_format,
        active_source_sha256=source_sha,
        row_count=rows,
        values=values,
        user_missing_range=config_user_missing_range,
        extended_missing=config_extended_missing,
        **config_kwargs,
    )
    config = SourceConfig(document)
    incidence = decode_fixture_config(config, path)
    keys = None
    if "source_native_key_slot" in document["respondents"]:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=4)
    projection = build_governed_c11_projection(config, row_native_keys=keys)
    cells = tuple(incidence.iter_cells(4))
    candidate = project_c11_candidate_from_config(
        config,
        projection,
        cells=cells,
        row_native_keys=keys,
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
    )
    release = validate_c11_source_release(candidate)
    return {
        "path": path,
        "source_sha": source_sha,
        "rows": rows,
        "values": tuple(values),
        "document": document,
        "config": config,
        "incidence": incidence,
        "keys": keys,
        "projection": projection,
        "cells": cells,
        "candidate": candidate,
        "release": release,
    }
