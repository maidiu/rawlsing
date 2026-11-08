"""Build full supported-scope nonrespondent fixtures for the R157 LITS lane.

Every declared supported question/response slot and every declared coordinate
shape in the original source configuration receives a permitted nonrespondent
cell for a small fixed row count.  The source-native value/state/topology rules
are reused unchanged; only fixture identity, fixture universe, fixture authority
and fixture bytes are replaced.  No original respondent bytes are read.

The prior representative fixtures and validation results are copied to
``representative_*`` files before the full-scope files are written.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "rawlsing_next" / "source_configuration" / "data" / "SRC27"))

import lits_lane_build as base  # noqa: E402
from rawlsing_next.source_configuration.fixture import fixture_document_sha256  # noqa: E402
from rawlsing_next.source_configuration.schema import (  # noqa: E402
    canonical_config_hash,
    load_source_config,
)

SOURCES = ("SRC27", "SRC28", "SRC29", "SRC30")
FIXTURE_SCHEMA = "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0"
ROWS = 5


def _raw_sort(value: Any) -> float:
    return float(value)


def _response_codes(slot: Mapping[str, Any]) -> list[tuple[Any, str, str]]:
    result = []
    for raw, label, canonical in base._ordered_codes(slot):
        state = base._classify_label(label)
        result.append((raw, state, canonical))
    result.sort(key=lambda item: _raw_sort(item[0]))
    return result


def _slot_readstat(slot: Mapping[str, Any]) -> str:
    return str(slot.get("readstat_type") or slot.get("storage_type") or "float")


def _response_fixture_values(slot: Mapping[str, Any]) -> list[Any]:
    slot = dict(slot)
    slot["readstat_type"] = _slot_readstat(slot)
    codes = _response_codes(slot)
    substantive = [raw for raw, state, _ in codes if state == "SUBSTANTIVE_RESPONSE"]
    # A few source slots have only special/continuous labels.  Keep them in the
    # declared supported scope and exercise their actual declared codes; do not
    # invent a substantive category or drop the slot.
    row1 = substantive[0] if substantive else codes[0][0]
    row2 = substantive[-1] if substantive else codes[-1][0]
    fallback = substantive[0] if substantive else codes[0][0]
    dk = next((raw for raw, state, _ in codes if state == "DK"), None)
    refusal = next((raw for raw, state, _ in codes if state == "REFUSAL"), None)
    inapplicable = next((raw for raw, state, _ in codes if state == "INAPPLICABLE"), None)
    missing = next((raw for raw, state, _ in codes if state == "MISSING"), None)
    special = next((raw for raw, state, _ in codes if state == "SOURCE_SPECIFIC_SPECIAL"), None)
    row4 = refusal if refusal is not None else (
        inapplicable if inapplicable is not None else (
            special if special is not None else (
                missing if missing is not None else fallback
            )
        )
    )
    row3 = dk if dk is not None else fallback
    values = [row1, row2, row3, row4, None]
    return values


def _coordinate_fixture_values(source_id: str, slot: Mapping[str, Any]) -> list[Any]:
    readstat = _slot_readstat(slot)
    if readstat == "string":
        return [f"R157_FIXTURE_{source_id}_{slot['name']}_ROW_{row}" for row in range(1, ROWS + 1)]
    if readstat.startswith("int"):
        return [row for row in range(1, ROWS + 1)]
    return [float(row) for row in range(1, ROWS + 1)]


def _cell(
    *,
    row: int,
    slot: Mapping[str, Any],
    raw_value: Any,
    missing_state: str = "OBSERVED_STORAGE_VALUE",
) -> dict[str, Any]:
    return {
        "row_ordinal": row,
        "variable_ordinal": slot["ordinal"],
        "variable_name": slot["name"],
        "raw_value": raw_value,
        "missing_state": missing_state,
        "source_missing_declaration": None,
    }


def _preserve_representative(source_id: str) -> dict[str, str | None]:
    validation_dir = ROOT / "source_pre553_validation" / source_id
    mapping = {
        "fixture.json": "representative_fixture.json",
        "fixture.config.json": "representative_fixture.config.json",
        "expected_results.json": "representative_expected_results.json",
        "validation_results.json": "representative_validation_results.json",
    }
    preserved = {}
    for source_name, target_name in mapping.items():
        source = validation_dir / source_name
        target = validation_dir / target_name
        if source.is_file() and not target.exists():
            shutil.copyfile(source, target)
        preserved[target_name] = str(target.relative_to(ROOT)) if target.is_file() else None
    return preserved


def _build_fixture_document(
    source_id: str,
    original: Mapping[str, Any],
    supported_questions: Sequence[Mapping[str, Any]],
    response_slots: Sequence[Mapping[str, Any]],
    coordinate_slots: Sequence[Mapping[str, Any]],
    physical_by_key: Mapping[tuple[int, str], Mapping[str, Any]],
    key_slot: Mapping[str, Any],
    key_values: Sequence[Any],
) -> tuple[dict[str, Any], dict[tuple[int, str], list[Any]]]:
    fixture_id = f"R157-LITS-{source_id}-FULL-SUPPORTED-NONRESPONDENT"
    cells = []
    response_values: dict[tuple[int, str], list[Any]] = {}
    for row in range(1, ROWS + 1):
        cells.append(
            _cell(row=row, slot=key_slot, raw_value=key_values[row - 1])
        )
        for section in response_slots:
            slot = physical_by_key[(section["slot"]["ordinal"], section["slot"]["name"])]
            values = response_values.setdefault((slot["ordinal"], slot["name"]), _response_fixture_values(slot))
            raw = values[row - 1]
            missing_state = "SYSTEM_MISSING" if raw is None else "OBSERVED_STORAGE_VALUE"
            cells.append(_cell(row=row, slot=slot, raw_value=raw, missing_state=missing_state))
        for section in coordinate_slots:
            slot = physical_by_key[(section["slot"]["ordinal"], section["slot"]["name"])]
            values = _coordinate_fixture_values(source_id, slot)
            cells.append(_cell(row=row, slot=slot, raw_value=values[row - 1]))
    document = {
        "schema": FIXTURE_SCHEMA,
        "fixture_id": fixture_id,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "original_source_id": source_id,
        "original_source_sha256": original["identity"]["expected_source_sha256"],
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "row_count": ROWS,
        "cells": cells,
        "shape_coverage": [
            (
                f"Full declared supported nonrespondent scope: "
                f"{len(supported_questions)} supported questions/response slots, "
                f"{len(coordinate_slots)} coordinate slots, {len(supported_questions)} routing rules"
            ),
            (
                "Five fixed nonrespondent rows; every supported response slot and every "
                "declared coordinate slot has a cell in every row."
            ),
            (
                "Per-slot state pattern: first substantive code, last substantive code, "
                "DK where declared, refusal/inapplicable/special where declared, and a "
                "system-missing final row."
            ),
            (
                "The P3 fixture-scoped exact row-key path is exercised with one explicitly "
                "nonrespondent key witness per row."
            ),
        ],
        "oracle_basis": (
            "Expected state/canonical values are computed from these explicit fixture cells "
            "and the source config's serialized value rules before the native call."
        ),
        "limits": [
            "Repository-generated nonrespondent input; not original respondent data.",
            "Fixture authority is NONRESPONDENT_FIXTURE_ONLY and cannot be promoted.",
            "Full supported fixture validation does not establish original-source scientific results or execution permission.",
        ],
    }
    document["fixture_source_sha256"] = fixture_document_sha256(document)
    return document, response_values


def _fixture_config(
    *,
    source_id: str,
    original: Mapping[str, Any],
    supported_questions: Sequence[Mapping[str, Any]],
    response_sections: Sequence[Mapping[str, Any]],
    coordinate_sections: Sequence[Mapping[str, Any]],
    routing_sections: Sequence[Mapping[str, Any]],
    fixture_doc: Mapping[str, Any],
    fixture_sha: str,
    recipe: Mapping[str, Any],
    roster: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    fixture_authority = base._authority_set(
        source_id=source_id,
        source_sha=fixture_sha,
        original_source_sha=original["identity"]["expected_source_sha256"],
        wave=original["identity"]["wave"],
        fixture=True,
        fixture_id=fixture_doc["fixture_id"],
        fixture_sha=fixture_sha,
        selected_vars=sorted(
            {
                section["slot"]["name"] for section in response_sections
            }
            | {
                section["slot"]["name"] for section in coordinate_sections
            }
        ),
    )
    fixture_universe_payload, fixture_universe = base._universe_payload(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        authority=fixture_authority,
        fixture=True,
        fixture_sha=fixture_sha,
    )
    config = copy.deepcopy(dict(original))
    config["config_id"] = f"R157-LITS-{source_id}-FULL-SUPPORTED-NONRESPONDENT-FIXTURE"
    config["config_purpose"] = "NONRESPONDENT_FIXTURE"
    config["binding"] = {
        "identity_class": "NONRESPONDENT_FIXTURE",
        "source_sha256": fixture_sha,
        "row_count": ROWS,
        "source_snapshot_ref": {
            "kind": "FIXTURE_SNAPSHOT",
            "object_id": f"urn:rawlsing:r157:fixture:{fixture_doc['fixture_id']}",
            "content_hash": fixture_sha,
        },
        "fixture_provenance": {
            "fixture_id": fixture_doc["fixture_id"],
            "provenance": (
                "Repository-generated full-supported-scope nonrespondent fixture for the R157 "
                "LITS lane; values are declared source codes or explicit fixture-only strings; "
                "no original respondents represented."
            ),
            "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
            "original_source_id": source_id,
            "original_source_sha256": original["identity"]["expected_source_sha256"],
            "no_original_respondents": True,
            "fixture_study_product_id": f"R157_FIXTURE/LiTS/{source_id}",
            "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}/FULL_SUPPORTED",
            "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
        },
    }
    config["authority"] = {
        "snapshots": fixture_authority["snapshots"],
        "required_refs": fixture_authority["required_refs"],
        "projection_authority_ref": fixture_authority["projection_authority_ref"],
        "replay_authority_ref": fixture_authority["replay_authority_ref"],
        "projection_identity_ref": base._exact_ref(
            "PROJECTION_IDENTITY",
            f"urn:rawlsing:r157:projection:{source_id}:full-supported-fixture",
            {
                "source_id": source_id,
                "fixture_id": fixture_doc["fixture_id"],
                "fixture_sha": fixture_sha,
                "supported_questions": sorted(
                    q["question_id"] for q in supported_questions
                ),
            },
        ),
        "tie_order_ref": base._exact_ref(
            "DETERMINISTIC_TIE_ORDER",
            f"urn:rawlsing:r157:tie-order:{source_id}:full-supported-fixture",
            {"source_id": source_id, "fixture": True, "order": "exact_ref_key"},
        ),
        "replay_protocol_version": "R157_SOURCE_CONFIGURATION@1.0.0",
    }
    config["universe"] = {"universes": [fixture_universe_payload]}
    config["respondents"] = base._respondents_section(
        source_id=source_id,
        recipe=recipe,
        slots=slots,
        universe_payload=fixture_universe_payload,
        fixture=True,
        key_slot_name=recipe["key_slot"],
    )
    config["questions"] = copy.deepcopy(list(supported_questions))
    config["response_slots"] = copy.deepcopy(list(response_sections))
    config["coordinate_slots"] = copy.deepcopy(list(coordinate_sections))
    config["routing"] = copy.deepcopy(list(routing_sections))
    semantic = base._authority_ref(fixture_authority["by_tag"]["SEMANTIC"])
    topology = base._authority_ref(fixture_authority["by_tag"]["TOPOLOGY"])
    mapping = base._authority_ref(fixture_authority["by_tag"]["MAPPING"])
    coordinate = base._authority_ref(fixture_authority["by_tag"]["COORDINATE"])
    routing_auth = base._authority_ref(fixture_authority["by_tag"]["ROUTING"])
    for question in config["questions"]:
        question["empirical_universe_ref"] = fixture_universe.ref.as_dict()
        question["semantic_authority_ref"] = semantic
        question["topology_authority_ref"] = topology
        question["item_evidence"]["fixture_identity_class"] = "NONRESPONDENT_FIXTURE"
    for section in config["response_slots"]:
        for value in section["values"]:
            if value.get("transform_authority_ref") is not None:
                value["transform_authority_ref"] = mapping
    for section in config["coordinate_slots"]:
        section["source_semantic_authority_ref"] = coordinate
    for rule in config["routing"]:
        rule["authority_ref"] = routing_auth
    for slot in config["physical_slots"]:
        if slot["name"] == recipe["key_slot"]:
            slot["disposition"] = "INCLUDED_FIXTURE_KEY_SLOT"
            slot.pop("disposition_reason", None)
    for item in config["items"]:
        if item["source_variable_code"] == recipe["key_slot"]:
            item["disposition"] = "INCLUDED_FIXTURE_KEY_SLOT"
    supported_qids = sorted(q["question_id"] for q in supported_questions)
    config["supported_scope"] = {
        "scope_id": f"{source_id}_FULL_SUPPORTED_NONRESPONDENT_SCOPE",
        "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
        "declared_supported": True,
        "supported_question_ids": supported_qids,
        "native_validation_expectation": "POSITIVE_RELEASE",
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "supported_unit_slice": "NONRESPONDENT_FIXTURE_HOUSEHOLD_ROW",
        "supported_form_slice": "NONRESPONDENT_FIXTURE_DECLARED_CELLS",
        "notes": [
            (
                f"This fixture covers every declared supported question ({len(supported_qids)}) "
                f"and every declared coordinate slot ({len(coordinate_sections)}) in the "
                "original source config, with five fixed nonrespondent rows."
            ),
            (
                "Prepared routing-unknown and response-authority-gap items are not in the "
                "declared supported scope and are not represented as fixture positives; their "
                "exact premises remain in the original config/exception ledger."
            ),
        ],
    }
    config["coverage"] = {
        "physical_slots_total": original["identity"]["source_column_count"],
        "items_total": original["identity"]["original_item_count"],
        "partial_scope_reason": (
            "Full declared supported nonrespondent scope: every supported question/response slot "
            "and every declared coordinate shape is fixture-exercised. Prepared routing-unknown "
            "and response-authority-gap bindings remain outside supported scope with exact "
            "residuals; they are not represented as fixture positives."
        ),
        "not_a_lane_config": True,
    }
    config["residuals"] = [
        {
            "residual_id": f"{source_id}-FIXTURE-ONLY-IDENTITY",
            "scope": f"{source_id}:{fixture_doc['fixture_id']}",
            "field": "identity_class_and_authority",
            "status": "FIXTURE_ONLY",
            "reason": (
                "This config deliberately binds a distinct nonrespondent fixture SHA and "
                "fixture-only authority; it is not an original-source config and cannot be "
                "promoted to original identity."
            ),
            "dependent_operation": "original-source execution or original authority claims",
            "unaffected_scope": "the full supported nonrespondent fixture native-validation scope",
            "owner": "R157 LITS lane author",
            "next_step": (
                "Use the separate ORIGINAL_SOURCE config for preparation; original execution "
                "remains a separate permission/issuance boundary."
            ),
        },
        {
            "residual_id": f"{source_id}-FIXTURE-FULL-SUPPORTED-SCOPE",
            "scope": f"{source_id}: {len(supported_qids)} supported questions and all declared coordinates",
            "field": "native_validation.scope",
            "status": "FULL_SUPPORTED_FIXTURE",
            "reason": (
                "Every declared supported question/response slot and every declared coordinate "
                "shape is present in this nonrespondent fixture. This closes the former "
                "representative-only validation gap for the declared supported scope."
            ),
            "dependent_operation": "original-source execution",
            "unaffected_scope": "full declared supported nonrespondent native input compatibility",
            "owner": "R157 integration owner / final review",
            "next_step": (
                "Keep original execution separate. Do not promote fixture authority, fixture "
                "universe or fixture SHA into original source meaning."
            ),
        },
        {
            "residual_id": f"{source_id}-FIXTURE-UNSUPPORTED-PREPARED-ITEMS",
            "scope": f"{source_id}: prepared routing-unknown/response-gap items outside declared supported scope",
            "field": "native_validation.scope",
            "status": "NOT_FIXTURE_EXERCISED",
            "reason": (
                "These prepared items are not in the original config's declared supported set: "
                "routing-unknown items lack the exact O06 clause and response-gap items lack P2 "
                "response authority. They are not claimed as fixture-validated and are not a "
                "generic representative remainder."
            ),
            "dependent_operation": "adding those items to supported scope",
            "unaffected_scope": "the full declared supported nonrespondent scope",
            "owner": "R157 LITS lane author / source-evidence owners",
            "next_step": (
                "Resolve the exact routing or response-authority premise in the original config, "
                "then extend the supported set and fixture explicitly."
            ),
        },
    ]
    config["evidence"] = base._evidence_section(
        source_id=source_id,
        roster=roster,
        fixture=True,
        fixture_doc=fixture_doc,
        fixture_sha=fixture_sha,
    )
    config["notes"] = [
        "NONRESPONDENT_FIXTURE config for the full declared supported scope.",
        "Every supported question/response slot and every declared coordinate shape is covered.",
        "Prepared routing-unknown/response-gap items are outside supported scope with exact residuals.",
        "Original source execution and original workload issuance are not performed.",
    ]
    return config


def _expected_results(
    *,
    source_id: str,
    original: Mapping[str, Any],
    fixture_config: Mapping[str, Any],
    fixture_doc: Mapping[str, Any],
    fixture_sha: str,
    response_values: Mapping[tuple[int, str], list[Any]],
) -> dict[str, Any]:
    cells_by_slot: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for cell in fixture_doc["cells"]:
        cells_by_slot.setdefault(
            (cell["variable_ordinal"], cell["variable_name"]), []
        ).append(cell)
    states_by_question: dict[str, list[str]] = {}
    canonical_by_question: dict[str, list[Any]] = {}
    occurrence_counts: dict[str, int] = {}
    for section in fixture_config["response_slots"]:
        key = (section["slot"]["ordinal"], section["slot"]["name"])
        qid = section["question_id"]
        rules = {
            (
                None if value["raw_value"] is None else (
                    int(value["raw_value"])
                    if isinstance(value["raw_value"], float) and value["raw_value"].is_integer()
                    else value["raw_value"]
                ),
                value["missing_state"],
            ): value
            for value in section["values"]
        }
        states = []
        canonical = []
        for cell in sorted(cells_by_slot[key], key=lambda item: item["row_ordinal"]):
            raw = cell["raw_value"]
            if isinstance(raw, float) and raw.is_integer():
                raw_key = int(raw)
            else:
                raw_key = raw
            rule = rules[(raw_key, cell["missing_state"])]
            states.append(rule["response_state"])
            canonical.append(rule["canonical_value"])
            kind = rule["occurrences"][0]["multiplicity_order_rank_fields"].get("kind", "unknown")
            occurrence_counts[kind] = occurrence_counts.get(kind, 0) + 1
        states_by_question[qid] = states
        canonical_by_question[qid] = canonical
    routing_states: dict[str, str] = {}
    for rule in fixture_config["routing"]:
        routing_states.setdefault(rule["question_id"], rule["typed_state"])
    coordinate_states = {
        section["slot"]["name"]: ["OBSERVED_COORDINATE"] * ROWS
        for section in fixture_config["coordinate_slots"]
    }
    return {
        "schema": "PYAT_R157_LITS_FULL_SUPPORTED_NONRESPONDENT_ORACLE@1.0.0",
        "source_id": source_id,
        "fixture_id": fixture_doc["fixture_id"],
        "fixture_path": f"source_pre553_validation/{source_id}/fixture.json",
        "fixture_sha256": fixture_sha,
        "fixture_config_path": f"source_pre553_validation/{source_id}/fixture.config.json",
        "fixture_config_canonical_hash": canonical_config_hash(fixture_config),
        "original_config_path": f"rawlsing_next/source_configuration/data/{source_id}/{source_id.lower()}.config.json",
        "original_source_id": source_id,
        "original_source_sha256": fixture_doc["original_source_sha256"],
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "fixture_only": True,
        "row_count": ROWS,
        "question_count": len(fixture_config["questions"]),
        "response_slot_count": len(fixture_config["response_slots"]),
        "coordinate_slot_count": len(fixture_config["coordinate_slots"]),
        "routing_question_count": len(fixture_config["routing"]),
        "authority_snapshot_count": len(fixture_config["authority"]["snapshots"]),
        "respondent_count": ROWS,
        "key_slot": fixture_config["respondents"].get("source_native_key_slot"),
        "key_witness_count": ROWS,
        "response_event_count": ROWS * len(fixture_config["response_slots"]),
        "coordinate_fact_count": ROWS * len(fixture_config["coordinate_slots"]),
        "routing_fact_count": ROWS * len(fixture_config["routing"]),
        "occurrence_counts": dict(sorted(occurrence_counts.items())),
        "response_states_by_question": states_by_question,
        "canonical_values_by_question": canonical_by_question,
        "routing_states_by_question": routing_states,
        "coordinate_states_by_slot": coordinate_states,
        "weight_section": "NOT_APPLICABLE",
        "source_relation_section": "DISTINCT_BY_DEFAULT",
        "oracle_basis": (
            "Computed from the explicit full-supported fixture cells and the original config's "
            "serialized value/state/topology rules before the native call."
        ),
        "limits": [
            "Full supported nonrespondent fixture validation does not establish original-source scientific results.",
            "Prepared routing-unknown/response-gap items remain outside supported scope with exact residuals.",
            "Original source execution is not performed or claimed.",
        ],
    }


def main() -> int:
    manifest_sources = []
    for source_id in SOURCES:
        recipe = base.RECIPES[source_id]
        roster, slots, items, codebook, _ = base._source_data(source_id)
        original = load_source_config(
            ROOT / "rawlsing_next" / "source_configuration" / "data" / source_id / f"{source_id.lower()}.config.json"
        ).document
        supported_qids = set(original["supported_scope"]["supported_question_ids"])
        supported_questions = [
            q for q in original["questions"] if q["question_id"] in supported_qids
        ]
        response_sections = [
            section for section in original["response_slots"]
            if section["question_id"] in supported_qids
        ]
        coordinate_sections = list(original["coordinate_slots"])
        routing_sections = [
            rule for rule in original["routing"] if rule["question_id"] in supported_qids
        ]
        if len(supported_questions) != len(supported_qids):
            raise ValueError(f"{source_id}: supported question count mismatch")
        if len(response_sections) != len(supported_questions):
            raise ValueError(f"{source_id}: supported response-slot count mismatch")
        physical_by_key = {
            (slot["ordinal"], slot["name"]): slot
            for slot in original["physical_slots"]
        }
        key_slot = next(
            slot for slot in original["physical_slots"] if slot["name"] == recipe["key_slot"]
        )
        key_values = recipe["key_values"]
        if len(key_values) != ROWS:
            raise ValueError(f"{source_id}: key values must match fixed row count")
        fixture_doc, response_values = _build_fixture_document(
            source_id=source_id,
            original=original,
            supported_questions=supported_questions,
            response_slots=response_sections,
            coordinate_slots=coordinate_sections,
            physical_by_key=physical_by_key,
            key_slot=key_slot,
            key_values=key_values,
        )
        fixture_sha = fixture_doc["fixture_source_sha256"]
        fixture_config = _fixture_config(
            source_id=source_id,
            original=original,
            supported_questions=supported_questions,
            response_sections=response_sections,
            coordinate_sections=coordinate_sections,
            routing_sections=routing_sections,
            fixture_doc=fixture_doc,
            fixture_sha=fixture_sha,
            recipe=recipe,
            roster=roster,
            slots=slots,
        )
        expected = _expected_results(
            source_id=source_id,
            original=original,
            fixture_config=fixture_config,
            fixture_doc=fixture_doc,
            fixture_sha=fixture_sha,
            response_values=response_values,
        )
        validation_dir = ROOT / "source_pre553_validation" / source_id
        preserved = _preserve_representative(source_id)
        fixture_path = validation_dir / "fixture.json"
        fixture_config_path = validation_dir / "fixture.config.json"
        expected_path = validation_dir / "expected_results.json"
        fixture_path.write_text(
            json.dumps(fixture_doc, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        fixture_config_path.write_text(
            json.dumps(fixture_config, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        expected_path.write_text(
            json.dumps(expected, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        manifest_sources.append(
            {
                "source_id": source_id,
                "fixture_path": str(fixture_path.relative_to(ROOT)),
                "fixture_sha256": base._file_sha(fixture_path),
                "fixture_source_sha256": fixture_sha,
                "fixture_config_path": str(fixture_config_path.relative_to(ROOT)),
                "fixture_config_sha256": base._file_sha(fixture_config_path),
                "fixture_config_canonical_hash": canonical_config_hash(fixture_config),
                "expected_results_path": str(expected_path.relative_to(ROOT)),
                "expected_results_sha256": base._file_sha(expected_path),
                "supported_question_count": len(supported_questions),
                "response_slot_count": len(response_sections),
                "coordinate_slot_count": len(coordinate_sections),
                "routing_question_count": len(routing_sections),
                "row_count": ROWS,
                "response_event_count": expected["response_event_count"],
                "coordinate_fact_count": expected["coordinate_fact_count"],
                "routing_fact_count": expected["routing_fact_count"],
                "occurrence_counts": expected["occurrence_counts"],
                "preserved_representative": preserved,
            }
        )
        print(
            source_id,
            "full supported",
            len(supported_questions),
            "questions",
            len(coordinate_sections),
            "coords",
            "events",
            expected["response_event_count"],
            "fixture",
            fixture_sha[:16],
        )
    manifest = {
        "schema": "PYAT_R157_LITS_FULL_SCOPE_FIXTURE_MANIFEST@1.0.0",
        "lane_id": "LITS",
        "row_count": ROWS,
        "plan_seal": base.PLAN_SEAL,
        "p0_dependency_commit": base.P0_DEPENDENCY_COMMIT,
        "p3_dependency_commit": "519355ec2215409b40d566ef13c3b21f611e0726",
        "generated_by": "source_pre553_validation/SRC27/build_full_scope_fixtures.py",
        "sources": manifest_sources,
    }
    manifest_path = ROOT / "source_pre553_validation" / "SRC27" / "full_scope_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print("manifest", manifest_path.relative_to(ROOT), base._file_sha(manifest_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
