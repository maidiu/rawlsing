"""Build the committed R157 P0 nonrespondent example from the evidence package."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import AuthorityRef, AuthoritySnapshot, EmpiricalUniverse, ExactRef, semantic_hash
from rawlsing_next.source_configuration.evidence import (
    EVIDENCE_DIR,
    iter_codebook_rows,
    iter_item_evidence,
    iter_physical_slots,
    source_roster_entry,
)
from rawlsing_next.source_configuration.fixture import fixture_document_sha256

ROOT = Path(__file__).resolve().parents[3]
OUT_CONFIG = ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
OUT_FIXTURE = ROOT / "source_pre553_validation/foundation/fixtures/SRC09_q101_nonrespondent.json"
ORIGINAL_SHA = "4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200"
SOURCE_ID = "SRC09"


def h(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ref(kind: str, tag: str, seed: str | None = None) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:r157:p0:{tag}", h(seed or tag))


def auth_ref(tag: str) -> AuthorityRef:
    return AuthorityRef(f"R157-P0-FIXTURE-{tag}", "1.0.0", h(f"authority:{tag}"))


def snapshot(tag: str, aid: AuthorityRef, kind: str, families: tuple[str, ...],
             source_sha: str, fixture_id: str) -> dict[str, Any]:
    replay = ref("REPLAY_ROOT", f"authority:{tag}")
    return {
        "typed_state": "ALLOW",
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": replay.as_dict(),
        "authority_id": aid.authority_id,
        "authority_version": aid.authority_version,
        "authority_content_hash": aid.authority_content_hash,
        "authority_kind": kind,
        "decision_state": "ALLOW",
        "governed_operations": [f"R157-P0-FIXTURE-OP-{tag}"],
        "governed_object_families": list(families),
        "scope_envelope": {
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "fixture_id": fixture_id,
            "source_id": SOURCE_ID,
            "source_sha256": source_sha,
            "original_source_sha256": ORIGINAL_SHA,
        },
        "effective_time_or_interval": "R157_P0_FIXTURE",
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": h(f"semantics:{tag}"),
        "replay_protocol_ref": ref("REPLAY_PROTOCOL", f"authority:{tag}").as_dict(),
    }


def main() -> int:
    roster = source_roster_entry(SOURCE_ID)
    if roster["source_sha256"] != ORIGINAL_SHA:
        raise SystemExit("SRC09 source identity drifted")
    physical = {row["ordinal"]: row for row in iter_physical_slots(SOURCE_ID)}
    codebook = {row["var_name"]: row for row in iter_codebook_rows(SOURCE_ID)}
    item = next(row for row in iter_item_evidence(SOURCE_ID)
                if row["source_variable_code"] == "q101")
    relation = item["relation"]
    if relation is None:
        raise SystemExit("SRC09 q101 lacks the exact full-relation row")
    q101_slot = physical[124]
    country_slot = physical[1]
    if q101_slot["name"] != "q101" or country_slot["name"] != "country":
        raise SystemExit("SRC09 slot ordinals drifted")

    fixture_id = "R157-P0-SRC09-Q101-NONRESPONDENT"
    cells = []
    for row, (q101_value, country_value) in enumerate(
            zip((1.0, 2.0, 3.0, 4.0, -1.0, 7.0, 8.0, 9.0, None),
                (1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0)), 1):
        cells.append({
            "row_ordinal": row,
            "variable_ordinal": 124,
            "variable_name": "q101",
            "raw_value": q101_value,
            "missing_state": "SYSTEM_MISSING" if q101_value is None else "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
        })
        cells.append({
            "row_ordinal": row,
            "variable_ordinal": 1,
            "variable_name": "country",
            "raw_value": country_value,
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
        })
    fixture = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
        "fixture_id": fixture_id,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "row_count": 9,
        "cells": cells,
        "expected_results": {
            "fixture_only": True,
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "response_event_count": 9,
            "coordinate_fact_count": 9,
            "routing_fact_count": 9,
            "response_states": [
                "SUBSTANTIVE_RESPONSE", "SUBSTANTIVE_RESPONSE", "SUBSTANTIVE_RESPONSE",
                "SUBSTANTIVE_RESPONSE", "MISSING", "DK", "SOURCE_SPECIFIC_SPECIAL",
                "REFUSAL", "MISSING",
            ],
            "canonical_values": ["1", "2", "3", "4", None, None, None, None, None],
            "weight_section": "NOT_APPLICABLE",
            "source_relation_section": "DISTINCT_BY_DEFAULT",
        },
    }
    fixture_sha = fixture_document_sha256(fixture)
    fixture["fixture_source_sha256"] = fixture_sha
    OUT_FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FIXTURE.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    source_auth = auth_ref("SOURCE")
    mapping_auth = auth_ref("MAPPING")
    topology_auth = auth_ref("TOPOLOGY")
    coord_auth = auth_ref("COORD")
    routing_auth = auth_ref("ROUTING")
    replay_auth = auth_ref("REPLAY")
    projection_auth = auth_ref("PROJECTION")
    snapshots = [
        snapshot("source", source_auth, "SOURCE_SEMANTICS_TOPOLOGY",
                 ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"), ORIGINAL_SHA, fixture_id),
        snapshot("mapping", mapping_auth, "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                 ("RespondentEvent@1.0.0",), ORIGINAL_SHA, fixture_id),
        snapshot("topology", topology_auth, "SOURCE_SEMANTICS_TOPOLOGY",
                 ("RespondentEvent@1.0.0",), ORIGINAL_SHA, fixture_id),
        snapshot("coord", coord_auth, "COORDINATE_SEMANTICS",
                 ("EmpiricalCoordinateFact@1.0.0",), ORIGINAL_SHA, fixture_id),
        snapshot("routing", routing_auth, "ROUTING_RISK_SET",
                 ("RoutingEligibilityFact@1.0.0",), ORIGINAL_SHA, fixture_id),
        snapshot("replay", replay_auth, "REPLAY_PROTOCOL",
                 ("ReplayReceipt@1.0.0",), ORIGINAL_SHA, fixture_id),
        snapshot("projection", projection_auth, "SOURCE_SEMANTICS_TOPOLOGY",
                 ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"), ORIGINAL_SHA, fixture_id),
    ]

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ref("REPLAY_ROOT", "universe"),
        raw_source_identity=f"R157-NONRESPONDENT-FIXTURE:{SOURCE_ID}",
        source_family=roster["family"],
        study_product_release="R157_P0_FIXTURE/SRC09",
        instrument_release="R157_P0_FIXTURE_INSTRUMENT/SRC09",
        country_geography="FIXTURE_MULTI_COUNTRY",
        sampling_geography="FIXTURE_NONPROBABILITY",
        raw_wave=roster["wave"],
        canonical_wave_if_governed=None,
        field_or_reference_time="R157_P0_FIXTURE",
        target_population_and_sample_frame="NONRESPONDENT_FIXTURE_ROWS",
        sampling_design_regime="NONRESPONDENT_FIXTURE_ONLY",
        respondent_namespace="urn:rawlsing:r157:p0:fixture:SRC09",
        source_artifact_import_lineage="R157_P0_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    universe_payload = {
        "typed_state": universe.typed_state,
        "authority_snapshot_refs": [source_auth.as_dict()],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": ref("REPLAY_ROOT", "universe").as_dict(),
        "raw_source_identity": universe.raw_source_identity,
        "source_family": universe.source_family,
        "study_product_release": universe.study_product_release,
        "instrument_release": universe.instrument_release,
        "country_geography": universe.country_geography,
        "sampling_geography": universe.sampling_geography,
        "raw_wave": universe.raw_wave,
        "canonical_wave_if_governed": None,
        "field_or_reference_time": universe.field_or_reference_time,
        "target_population_and_sample_frame": universe.target_population_and_sample_frame,
        "sampling_design_regime": universe.sampling_design_regime,
        "respondent_namespace": universe.respondent_namespace,
        "source_artifact_import_lineage": universe.source_artifact_import_lineage,
        "harmonization_authority_ref": None,
        "source_relation_refs": [],
    }
    native_question = ref("NATIVE_QUESTION", "SRC09:q101", semantic_hash({
        "source_variable_code": "q101", "question_text": item["p2"]["question_text"],
        "fixture_only": True,
    }))
    topology = ref("RESPONSE_TOPOLOGY", "SRC09:q101:SCALAR_SINGULAR", semantic_hash({
        "source_variable_code": "q101", "topology": "scalar", "fixture_only": True,
    }))
    question = {
        "question_id": "q101",
        "empirical_universe_ref": universe.ref.as_dict(),
        "native_question_ref": native_question.as_dict(),
        "instrument_question_version": roster["wave"],
        "canonical_question_ref_or_typed_absence": TypedAbsence("NOT_AUTHORIZED").as_dict(),
        "component_subitem_ref_or_typed_absence": TypedAbsence("NOT_APPLICABLE").as_dict(),
        "semantic_authority_ref": source_auth.as_dict(),
        "topology_authority_ref": topology_auth.as_dict(),
        "item_evidence": {
            "implementation_id": item["implementation_id"],
            "exact_identity_sha256": item["exact_identity_sha256"],
            "relation_join_status": item["relation_join_status"],
        },
    }
    occurrence = {
        "key": "0",
        "topology_ref": topology.as_dict(),
        "multiplicity_order_rank_fields": {"kind": "SCALAR_SINGULAR", "index": 0},
    }
    value_map = [
        (1.0, "SUBSTANTIVE_RESPONSE", "1"),
        (2.0, "SUBSTANTIVE_RESPONSE", "2"),
        (3.0, "SUBSTANTIVE_RESPONSE", "3"),
        (4.0, "SUBSTANTIVE_RESPONSE", "4"),
        (-1.0, "MISSING", None),
        (7.0, "DK", None),
        (8.0, "SOURCE_SPECIFIC_SPECIAL", None),
        (9.0, "REFUSAL", None),
    ]
    values = [{
        "raw_value": raw,
        "missing_state": "OBSERVED_STORAGE_VALUE",
        "source_missing_declaration": None,
        "response_state": state,
        "occurrences": [occurrence],
        "canonical_value": canonical,
        "transform_authority_ref": mapping_auth.as_dict() if canonical is not None else None,
        "extra_authority_refs": [],
    } for raw, state, canonical in value_map]
    values.append({
        "raw_value": None,
        "missing_state": "SYSTEM_MISSING",
        "source_missing_declaration": None,
        "response_state": "MISSING",
        "occurrences": [occurrence],
        "canonical_value": None,
        "transform_authority_ref": None,
        "extra_authority_refs": [],
    })
    physical_payload = [
        {
            "ordinal": country_slot["ordinal"],
            "name": country_slot["name"],
            "label": country_slot["label"],
            "storage_type": country_slot["readstat_type"],
            "original_type": country_slot["original_type"],
            "storage_width": country_slot["storage_width"],
            "measure": country_slot["measure"],
            "value_labels": country_slot["value_labels"],
            "missing_declarations": None,
            "mr_declarations": None,
            "codebook_mapping": country_slot["codebook_mapping"],
            "disposition": "SUPPORTED_COORDINATE",
            "disposition_reason": "Source-native country coordinate; fixture rows are nonrespondent.",
        },
        {
            "ordinal": q101_slot["ordinal"],
            "name": q101_slot["name"],
            "label": q101_slot["label"],
            "storage_type": q101_slot["readstat_type"],
            "original_type": q101_slot["original_type"],
            "storage_width": q101_slot["storage_width"],
            "measure": q101_slot["measure"],
            "value_labels": q101_slot["value_labels"],
            "missing_declarations": None,
            "mr_declarations": None,
            "codebook_mapping": q101_slot["codebook_mapping"],
            "disposition": "SUPPORTED_RESPONSE",
            "disposition_reason": "Grounded scalar item with exact H48/P2/full-relation evidence.",
        },
    ]
    limits = [x for x in (relation["forbidden_inference"], relation["does_not_measure"]) if x]
    limits.append(f"relation_use_status_final={relation['relation_use_status_final']}")
    limits.append("P0 fixture authority is not original-source authority.")
    item_payload = {
        "implementation_id": item["implementation_id"],
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "question_text": item["p2"]["question_text"],
        "disposition": item["p2"]["canonical_disposition"],
        "response_classes": item["p2"]["response_classes"],
        "mapping_status": relation["mapping_status"],
        "authority_status": relation["authority_status"],
        "evidence_refs": [
            ExactRef("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{item['implementation_id']}",
                     item["exact_identity_sha256"]).as_dict(),
            ExactRef("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{item['implementation_id']}",
                     item["p2"]["exact_identity_sha256"]).as_dict(),
            ExactRef("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{relation['question_id']}",
                     relation["governed_row_payload_hash"]).as_dict(),
        ],
        "limits": limits,
        "relation": {
            "status": "EXACT",
            "question_id": relation["question_id"],
            "mapping_status": relation["mapping_status"],
            "manual_response_topology": relation["manual_response_topology"],
            "manual_response_normalization_rule": relation["manual_response_normalization_rule"],
            "manual_position_conditioning": relation["manual_position_conditioning"],
            "manual_semantic_role": relation["manual_semantic_role"],
            "manual_signed_polarity_status": relation["manual_signed_polarity_status"],
            "forbidden_inference": relation["forbidden_inference"] or "none recorded",
            "does_not_measure": relation["does_not_measure"] or "none recorded",
            "governed_row_payload_hash": relation["governed_row_payload_hash"],
            "p2_exact_identity_sha256": relation["p2_exact_identity_sha256"],
        },
    }
    response_slot = {
        "slot": {"ordinal": 124, "name": "q101"},
        "question_id": "q101",
        "values": values,
    }
    coordinate_slot = {
        "slot": {"ordinal": 1, "name": "country"},
        "native_coordinate_ref": ref("COORDINATE_NATIVE", "SRC09:country", semantic_hash({
            "source_variable_code": "country", "fixture_only": True,
        })).as_dict(),
        "unit_taxonomy_ref": ref("UNIT_TAXONOMY", "SOURCE_NATIVE_COUNTRY_CODE", semantic_hash({
            "source_variable_code": "country", "unit": "source_native_country_code",
        })).as_dict(),
        "effective_time": "R157_P0_FIXTURE",
        "source_semantic_authority_ref": coord_auth.as_dict(),
        "canonical_coordinate_ref": None,
        "normalization_ref": None,
        "values": [],
        "copy_observed_raw": True,
    }
    routing = [{
        "question_id": "q101",
        "row_selector": "ALL",
        "typed_state": "ELIGIBLE_APPLICABLE",
        "risk_set_ref": ref("RISK_SET", "SRC09:q101:fixture").as_dict(),
        "routing_rule_ref": ref("ROUTING_RULE", "SRC09:q101:fixture").as_dict(),
        "member_set_replay_ref": ref("MEMBER_SET_REPLAY", "SRC09:q101:fixture").as_dict(),
        "authority_ref": routing_auth.as_dict(),
        "parent_predicate_refs": [],
        "dependency_refs": [],
    }]
    config = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": "R157-P0-EXAMPLE-SRC09-Q101-FIXTURE",
        "config_revision": 1,
        "config_purpose": "P0_EXAMPLE_FIXTURE",
        "identity": {
            "source_id": SOURCE_ID,
            "family": roster["family"],
            "wave": roster["wave"],
            "source_family_id": roster["family"],
            "study_product_id": roster["family"],
            "release_id": "W4_P0_EXAMPLE_ONLY",
            "instrument_release_id": f"SRC09_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
            "source_artifact_id": roster["source_artifact_id"],
            "expected_source_sha256": ORIGINAL_SHA,
            "source_format": roster["format"],
            "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"],
            "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"],
            "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": ExactRef(
                "SOURCE_SNAPSHOT", "urn:rawlsing:r157:source-snapshot:SRC09", ORIGINAL_SHA).as_dict(),
            "metadata_witness_ref": ExactRef(
                "R154_PHYSICAL_METADATA",
                f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                roster["metadata_witness"]["sha256"]).as_dict(),
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": "SRC09_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
            },
            "reader": {
                "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                "configuration_ref": ref("READER_CONFIGURATION", "SRC09:default_sav", semantic_hash({
                    "decoder": "decode_sav", "encoding": None, "source_sha256": ORIGINAL_SHA,
                })).as_dict(),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "NONRESPONDENT_FIXTURE",
            "source_sha256": fixture_sha,
            "row_count": 9,
            "source_snapshot_ref": ExactRef(
                "FIXTURE_SNAPSHOT",
                f"urn:rawlsing:r157:fixture:{fixture_id}",
                fixture_sha).as_dict(),
            "fixture_provenance": {
                "fixture_id": fixture_id,
                "provenance": "Repository-generated nonrespondent fixture for R157 P0; no original respondents represented.",
                "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                "original_source_id": SOURCE_ID,
                "original_source_sha256": ORIGINAL_SHA,
                "no_original_respondents": True,
                "fixture_study_product_id": "R157_P0_FIXTURE/SRC09",
                "fixture_release_id": "R157_P0_FIXTURE_RELEASE/SRC09",
                "fixture_instrument_release_id": "R157_P0_FIXTURE_INSTRUMENT/SRC09",
            },
        },
        "authority": {
            "snapshots": snapshots,
            "required_refs": [x.as_dict() for x in (
                source_auth, mapping_auth, topology_auth, coord_auth,
                routing_auth, replay_auth, projection_auth)],
            "projection_authority_ref": projection_auth.as_dict(),
            "replay_authority_ref": replay_auth.as_dict(),
            "projection_identity_ref": ref(
                "C11_SEMANTIC_PROJECTION", "SRC09:q101:p0-fixture", semantic_hash({
                    "config_id": "R157-P0-EXAMPLE-SRC09-Q101-FIXTURE",
                    "fixture_source_sha256": fixture_sha,
                })).as_dict(),
            "tie_order_ref": ref("ORDER_RULE", "R157-P0-FIXTURE-CANONICAL-REF-SORT").as_dict(),
            "replay_protocol_version": "1.0.0",
        },
        "universe": {"universes": [universe_payload]},
        "respondents": {
            "subject_unit": "FIXTURE_ROW",
            "respondent_namespace": "urn:rawlsing:r157:p0:fixture:SRC09",
            "respondent_key_pattern": "FIXTURE-ROW-{row_ordinal:04d}",
            "source_native_key_slot": None,
            "identity_map_authority_ref": None,
            "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY",
        },
        "questions": [question],
        "physical_slots": physical_payload,
        "items": [item_payload],
        "response_slots": [response_slot],
        "coordinate_slots": [coordinate_slot],
        "weight_slots": [],
        "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
            "comparator": TypedAbsence("DEFERRED").as_dict(),
            "discovery": TypedAbsence("DEFERRED").as_dict(),
            "structural": TypedAbsence("NOT_APPLICABLE").as_dict(),
        },
        "supported_scope": {
            "scope_id": "SRC09-Q101-P0-EXAMPLE",
            "purpose": "P0_EXAMPLE_ONLY",
            "declared_supported": True,
            "supported_question_ids": ["q101"],
            "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS",
            "supported_form_slice": "SCALAR_Q101",
            "notes": [
                "Fixture authority is explicitly nonrespondent and does not establish original-source authority.",
                "Original SRC09 source execution is not performed or claimed by this example.",
            ],
        },
        "coverage": {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": [1, 124],
            "physical_slots_excluded": [],
            "items_included": [item["implementation_id"]],
            "items_excluded": [],
            "partial_scope_reason": "P0 example slice; complete SRC09 coverage belongs to the ASIAN lane.",
            "not_a_lane_config": True,
        },
        "residuals": [{
            "residual_id": "SRC09-Q101-ORIGINAL-AUTHORITY",
            "scope": "SRC09/q101",
            "field": "authority.snapshots",
            "status": "FIXTURE_ONLY",
            "reason": "The P0 example proves the real constructor with authorized nonrespondent fixture authority; original source authority remains lane work.",
            "dependent_operation": "original-source construction/validation",
            "unaffected_scope": "nonrespondent fixture construction and native C11 validation",
            "owner": "LANE_ASIAN",
            "next_step": "Consume source-grounded authority and routing evidence for SRC09 and replace fixture-only snapshots in the original config.",
        }],
        "evidence": {
            "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
            "pinned_inputs": [
                {"kind": "R157_PLAN_SEAL", "commit": "4c0c619eac747afee1d8e65e1418bf2d472da4c3"},
                {"kind": "R154_METADATA_SNAPSHOT", "commit": "a02adc896264e1b46afd143cba9426182ec14802",
                 "path": "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite",
                 "sha256": "7d6421e6e50f7d249cf09e7ecf964757d6afa4a7926d7a31eb1aad3407a12a16"},
                {"kind": "H48_ITEM_INDEX", "commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
                 "path": "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz",
                 "sha256": "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5"},
                {"kind": "P2_PHASE0", "sha256": "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"},
                {"kind": "FULL_RELATION_AUTHORITY", "commit": "9561723cfe0932869e781f2be27e9c80b050ad7a",
                 "path": "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
                 "sha256": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"},
            ],
            "field_evidence": [
                {"field": "items[0].implementation_id",
                 "refs": [
                     ExactRef("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{item['implementation_id']}",
                              item["exact_identity_sha256"]).as_dict(),
                     ExactRef("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{item['implementation_id']}",
                              item["p2"]["exact_identity_sha256"]).as_dict(),
                 ]},
                {"field": "items[0].relation",
                 "refs": [ExactRef("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{relation['question_id']}",
                                   relation["governed_row_payload_hash"]).as_dict()]},
            ],
            "limits": [
                "Prior authority evidence is reused with its original grade and limits.",
                "Fixture authority is not original-source authority.",
                "No original respondent rows or original source file bytes were read.",
            ],
        },
        "runtime": {
            "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
            "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
            "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
            "reader_encoding_transport": "P3_PENDING_QUALIFIED_CONFIG_WIRING",
        },
    }
    OUT_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    OUT_CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"config": str(OUT_CONFIG), "fixture": str(OUT_FIXTURE),
                      "fixture_sha256": fixture_sha}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
