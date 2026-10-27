"""Build R157 EVS source configs, nonrespondent fixtures and native receipts.

Run with PYTHONPATH=. from the checkout root.  Writes only the EVS lane paths.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.source_configuration.evidence import (
    iter_codebook_rows,
    iter_item_evidence,
    iter_physical_slots,
    load_manifest,
    source_roster_entry,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import (
    fixture_document_sha256,
    fixture_stream_from_document,
)
from rawlsing_next.source_configuration.reader import (
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import (
    canonical_config_hash,
    load_source_config,
)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "rawlsing_next/source_configuration/data"
VALIDATION = ROOT / "source_pre553_validation"
CHOSEN = {
    "SRC11": "v545",
    "SRC12": "q650",
    "SRC13": "o6",
    "SRC14": "v277",
    "SRC15": "v221",
}
COUNTRY_FIXTURE_VALUES = [276.0, 250.0, 208.0, 528.0, 372.0, 380.0, 276.0, 250.0, 208.0, 528.0, 372.0, 380.0, 276.0]


def sha_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def ref(kind: str, tag: str, content_hash: str) -> ExactRef:
    if len(content_hash) != 64:
        content_hash = sha_json({"kind": kind, "tag": tag, "hash": content_hash})
    return ExactRef(kind, f"urn:rawlsing:r157:evs:{tag}", content_hash)


def authority(tag: str, kind: str, families: tuple[str, ...], *, sid: str, wave: str,
              source_sha: str, decision: str, evidence_hash: str, fixture_sha: str | None = None,
              fixture_id: str | None = None) -> AuthorityRef:
    material = {
        "schema": "R157_EVS_EVIDENCE_AUTHORITY_IDENTITY@1.0.0",
        "source_id": sid, "wave": wave, "kind": kind, "tag": tag,
        "source_sha256": source_sha, "evidence_hash": evidence_hash,
        "decision": decision, "fixture_sha256": fixture_sha, "fixture_id": fixture_id,
    }
    digest = sha_json(material)
    return AuthorityRef(f"R157-EVS-{sid}-{tag.upper()}-{decision}", "1.0.0", digest)


def snapshot(tag: str, kind: str, families: tuple[str, ...], auth: AuthorityRef, *,
             sid: str, wave: str, source_sha: str, decision: str, evidence_hash: str,
             fixture_sha: str | None = None, fixture_id: str | None = None) -> dict[str, Any]:
    replay = ref("REPLAY_PROTOCOL", f"{sid}:{tag}:replay", sha_json({"sid": sid, "tag": tag, "replay": True}))
    producer = ref("REPLAY_ROOT", f"{sid}:{tag}:producer", sha_json({"sid": sid, "tag": tag, "producer": True}))
    scope = {
        "source_id": sid,
        "wave": wave,
        "source_sha256": source_sha,
        "evidence_hash": evidence_hash,
        "grade": ("NONRESPONDENT_FIXTURE_ONLY" if decision == "ALLOW"
                  else "PRIOR_EVIDENCE_ONLY__NOT_CURRENT_SOURCE_AUTHORITY"),
    }
    if decision == "ALLOW":
        scope.update({
            "fixture_only": True,
            "fixture_source_sha256": fixture_sha,
            "fixture_id": fixture_id,
        })
    return {
        "typed_state": decision,
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": producer.as_dict(),
        "authority_id": auth.authority_id,
        "authority_version": auth.authority_version,
        "authority_content_hash": auth.authority_content_hash,
        "authority_kind": kind,
        "decision_state": decision,
        "governed_operations": [("R157_EVS_FIXTURE_VALIDATION" if decision == "ALLOW"
                                 else "R157_EVS_PRIOR_EVIDENCE_ONLY")],
        "governed_object_families": list(families),
        "scope_envelope": scope,
        "effective_time_or_interval": ("R157_NONRESPONDENT_FIXTURE" if decision == "ALLOW" else "PRIOR_EVIDENCE"),
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": sha_json({"sid": sid, "tag": tag, "decision": decision}),
        "replay_protocol_ref": replay.as_dict(),
    }


def build_authorities(sid: str, wave: str, source_sha: str, evidence_hash: str, *,
                      fixture_sha: str | None = None, fixture_id: str | None = None,
                      decision: str) -> tuple[dict[str, Any], dict[str, AuthorityRef]]:
    specs = (
        ("source", "SOURCE_SEMANTICS_TOPOLOGY", ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
        ("mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION", ("RespondentEvent@1.0.0",)),
        ("topology", "SOURCE_SEMANTICS_TOPOLOGY", ("RespondentEvent@1.0.0",)),
        ("coordinate", "COORDINATE_SEMANTICS", ("EmpiricalCoordinateFact@1.0.0",)),
        ("routing", "ROUTING_RISK_SET", ("RoutingEligibilityFact@1.0.0",)),
        ("replay", "REPLAY_PROTOCOL", ("ReplayReceipt@1.0.0",)),
        ("projection", "SOURCE_SEMANTICS_TOPOLOGY",
         ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0")),
    )
    refs: dict[str, AuthorityRef] = {}
    snaps = []
    for tag, kind, families in specs:
        auth = authority(tag, kind, families, sid=sid, wave=wave, source_sha=source_sha,
                         decision=decision, evidence_hash=evidence_hash,
                         fixture_sha=fixture_sha, fixture_id=fixture_id)
        refs[tag] = auth
        snaps.append(snapshot(tag, kind, families, auth, sid=sid, wave=wave,
                              source_sha=source_sha, decision=decision,
                              evidence_hash=evidence_hash,
                              fixture_sha=fixture_sha, fixture_id=fixture_id))
    return {
        "snapshots": snaps,
        "required_refs": [refs[k].as_dict() for k in ("source", "mapping", "topology", "coordinate", "routing", "replay", "projection")],
        "projection_authority_ref": refs["projection"].as_dict(),
        "replay_authority_ref": refs["replay"].as_dict(),
    }, refs


def universe_payload(sid: str, wave: str, source_sha: str, source_ref: AuthorityRef, *,
                     fixture: bool, fixture_id: str | None = None) -> tuple[dict[str, Any], EmpiricalUniverse]:
    root = ref("UNIVERSE_REPLAY_ROOT", f"{sid}:universe:{'fixture' if fixture else 'source'}",
               sha_json({"sid": sid, "wave": wave, "fixture": fixture}))
    if fixture:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED",
            "authority_snapshot_refs": [source_ref.as_dict()],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": root.as_dict(),
            "raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:{sid}:{fixture_id}",
            "source_family": "EVS",
            "study_product_release": f"R157_FIXTURE/EVS/{wave}",
            "instrument_release": f"R157_FIXTURE_INSTRUMENT/EVS/{wave}",
            "country_geography": "FIXTURE_MULTI_COUNTRY",
            "sampling_geography": "FIXTURE_NONPROBABILITY",
            "raw_wave": wave,
            "canonical_wave_if_governed": None,
            "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
            "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
            "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
            "respondent_namespace": f"urn:rawlsing:r157:evs:{sid}:fixture",
            "source_artifact_import_lineage": "R157_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE",
            "harmonization_authority_ref": None,
            "source_relation_refs": [],
        }
    else:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED",
            "authority_snapshot_refs": [source_ref.as_dict()],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": root.as_dict(),
            "raw_source_identity": f"EVS:{wave}:{source_sha}",
            "source_family": "EVS",
            "study_product_release": f"EVS/{wave}",
            "instrument_release": f"EVS {wave} source instrument",
            "country_geography": "SOURCE_NATIVE_MULTI_COUNTRY_WAVE",
            "sampling_geography": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "raw_wave": wave,
            "canonical_wave_if_governed": None,
            "field_or_reference_time": wave,
            "target_population_and_sample_frame": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "sampling_design_regime": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "respondent_namespace": f"urn:rawlsing:r157:evs:{sid}:id_cocas",
            "source_artifact_import_lineage": f"EVS:{wave}:{source_sha}",
            "harmonization_authority_ref": None,
            "source_relation_refs": [],
        }
    try:
        return payload, EmpiricalUniverse(**payload)
    except Exception as exc:
        raise RuntimeError(f"{sid}: cannot construct source universe: {exc}") from exc


def response_state(code: float, special_map: dict[float, str]) -> str:
    if code >= 1:
        return "SUBSTANTIVE_RESPONSE"
    return special_map.get(code, "SOURCE_SPECIFIC_SPECIAL")


def canonical_token(code: float) -> str:
    return str(int(code)) if float(code).is_integer() else str(code)


def response_values(item: dict[str, Any], slot: dict[str, Any], mapping_ref: AuthorityRef,
                    topology_ref: ExactRef, special_map: dict[float, str]) -> tuple[list[dict[str, Any]], dict[int, tuple[str, Any]]]:
    labels = slot.get("value_labels") or {}
    codes = sorted(float(key) for key in labels if _is_number(key) and float(key) >= 1)
    all_negative = sorted(float(key) for key in labels if _is_number(key) and float(key) < 0)
    occurrence = {
        "key": "0",
        "topology_ref": topology_ref.as_dict(),
        "multiplicity_order_rank_fields": {"kind": "SCALAR_SINGULAR", "index": 0},
    }
    values = []
    expected: dict[int, tuple[str, Any]] = {}
    row = 1
    for code in [*codes, *all_negative]:
        state = response_state(code, special_map)
        substantive = code >= 1
        canonical = canonical_token(code) if substantive else None
        values.append({
            "raw_value": float(code),
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
            "response_state": state,
            "occurrences": [occurrence],
            "canonical_value": canonical,
            "transform_authority_ref": mapping_ref.as_dict() if substantive else None,
            "extra_authority_refs": [],
        })
        expected[row] = (state, canonical)
        row += 1
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
    expected[row] = ("MISSING", None)
    return values, expected


def _is_number(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def coordinate_payload(slot: dict[str, Any], coord_ref: AuthorityRef, *,
                       wave: str, topology_ref: ExactRef) -> dict[str, Any]:
    labels = slot.get("value_labels") or {}
    values = []
    for key in labels:
        if not _is_number(key) or float(key) >= 0:
            continue
        code = float(key)
        state = {-1.0: "UNKNOWN", -2.0: "MISSING", -3.0: "NOT_LAWFULLY_CONDITIONABLE",
                 -4.0: "UNKNOWN", -5.0: "MISSING"}.get(code, "UNKNOWN")
        values.append({
            "raw_value": code,
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
            "coordinate_state": state,
            "canonical_value": None,
            "extra_authority_refs": [],
        })
    return {
        "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
        "native_coordinate_ref": ref(
            "COORDINATE_NATIVE", f"country:{wave}:{slot['name']}",
            slot["codebook_mapping"].get("row_hash") or sha_json({"slot": slot["name"], "wave": wave})).as_dict(),
        "unit_taxonomy_ref": ref("UNIT_TAXONOMY", f"country-code:{wave}",
                                 sha_json({"unit": "SOURCE_NATIVE_COUNTRY_CODE", "wave": wave})).as_dict(),
        "effective_time": wave,
        "source_semantic_authority_ref": coord_ref.as_dict(),
        "canonical_coordinate_ref": None,
        "normalization_ref": None,
        "values": values,
        "copy_observed_raw": True,
    }


def routing_rule(item: dict[str, Any], var: str, routing_ref: AuthorityRef,
                 topology_ref: ExactRef, wave: str) -> dict[str, Any]:
    status = ""
    for binding in item["h48"].get("candidate_bindings", []):
        if binding["family"] == "O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl":
            status = binding.get("status", {}).get("routing_status", "")
    if status != "UNCONDITIONAL_SOURCE_PROVEN":
        raise RuntimeError(f"{item['source_id']}: selected item is not unconditional: {status}")
    h = item["exact_identity_sha256"]
    return {
        "question_id": var,
        "row_selector": "ALL",
        "typed_state": "ELIGIBLE_APPLICABLE",
        "risk_set_ref": ref("RISK_SET", f"{item['source_id']}:{var}:unconditional", h).as_dict(),
        "routing_rule_ref": ref("ROUTING_RULE", f"{item['source_id']}:{var}:o06", h).as_dict(),
        "member_set_replay_ref": ref("MEMBER_SET_REPLAY", f"{item['source_id']}:{var}:all", h).as_dict(),
        "authority_ref": routing_ref.as_dict(),
        "parent_predicate_refs": [],
        "dependency_refs": [],
    }


def physical_slot_payload(slot: dict[str, Any], *, selected: bool, country: bool,
                          key_slot: bool) -> dict[str, Any]:
    reason = {
        "SUPPORTED_RESPONSE": "Selected P3 EVS scalar item with exact H48/P2/full-relation evidence.",
        "SUPPORTED_COORDINATE": "Source-native country coordinate; no canonical crosswalk claimed.",
        "SUBJECT_KEY": "Source-native unified respondent identifier (id_cocas).",
        "WEIGHT_NOT_CLAIMED": "Weight slot retained but not claimed in this raw/unweighted slice.",
        "ADMINISTRATIVE_CONTEXT": "Administrative/context slot retained in the source ledger.",
        "ACCOUNTED_UNSUPPORTED": "Slot retained and accounted; not bound in the P3 EVS supported slice.",
    }
    if selected:
        disposition = "SUPPORTED_RESPONSE"
    elif country:
        disposition = "SUPPORTED_COORDINATE"
    elif key_slot:
        disposition = "SUBJECT_KEY"
    elif slot["name"].lower().startswith("weight") or slot["name"].lower() in {"gweight", "dweight", "pweight", "gweight_no_edu"}:
        disposition = "WEIGHT_NOT_CLAIMED"
    elif slot["name"].lower() in {"studyno", "studynoc", "version", "versionc", "doi", "id_cocas", "c_abrv", "c_abrv1"}:
        disposition = "ADMINISTRATIVE_CONTEXT"
    else:
        disposition = "ACCOUNTED_UNSUPPORTED"
    missing = None
    if slot.get("missing_ranges") is not None or slot.get("missing_user_values") is not None:
        missing = {
            "ranges": slot.get("missing_ranges"),
            "user_values": slot.get("missing_user_values"),
        }
    return {
        "ordinal": slot["ordinal"],
        "name": slot["name"],
        "label": slot.get("label"),
        "storage_type": slot.get("readstat_type"),
        "original_type": slot.get("original_type"),
        "storage_width": slot.get("storage_width"),
        "measure": slot.get("measure"),
        "value_labels": slot.get("value_labels"),
        "missing_declarations": missing,
        "mr_declarations": None,
        "codebook_mapping": slot.get("codebook_mapping"),
        "disposition": disposition,
        "disposition_reason": reason[disposition],
    }


def item_payload(item: dict[str, Any], *, selected: bool, supported_var: str) -> dict[str, Any]:
    relation = item.get("relation")
    p2 = item["p2"]
    h48 = item["h48"]
    refs = [
        ref("H48_ITEM_AUTHORITY", f"{item['source_id']}:{item['implementation_id']}:h48",
            item["exact_identity_sha256"]).as_dict(),
        ref("P2_PHASE0_ROW", f"{item['source_id']}:{item['implementation_id']}:p2",
            p2["exact_identity_sha256"]).as_dict(),
    ]
    if relation and relation.get("governed_row_payload_hash"):
        refs.append(ref("FULL_RELATION_ROW", f"{item['source_id']}:{relation['question_id']}:relation",
                        relation["governed_row_payload_hash"]).as_dict())
    limits = []
    if relation:
        for field in ("forbidden_inference", "does_not_measure", "manual_conditional_strata_weights"):
            if relation.get(field):
                limits.append(f"{field}={relation[field]}")
        limits.append(f"relation_use_status_final={relation.get('relation_use_status_final', '')}")
        limits.append(f"directional_certification_status={relation.get('manual_directional_certification_status', '')}")
    limits.append("source-native response codes preserved; no directional scale normalization applied")
    limits.append("P3 EVS supported scalar slice" if selected else "not bound in the P3 EVS supported slice")
    payload = {
        "implementation_id": item["implementation_id"],
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "question_text": p2.get("question_text") or relation.get("manual_question_text") or supported_var,
        "disposition": p2.get("canonical_disposition") or relation.get("p2_canonical_disposition") or "UNKNOWN",
        "response_classes": p2.get("response_classes") or "UNKNOWN",
        "mapping_status": (relation or {}).get("mapping_status") or p2.get("mapping_status") or "UNKNOWN",
        "authority_status": (relation or {}).get("authority_status") or p2.get("authority_status") or "UNKNOWN",
        "evidence_refs": refs,
        "limits": limits,
    }
    if relation:
        payload["relation"] = {
            "status": "EXACT",
            "question_id": relation["question_id"],
            "mapping_status": relation["mapping_status"],
            "manual_response_topology": relation["manual_response_topology"],
            "manual_response_normalization_rule": relation["manual_response_normalization_rule"],
            "manual_position_conditioning": relation["manual_position_conditioning"],
            "manual_semantic_role": relation["manual_semantic_role"],
            "manual_signed_polarity_status": relation["manual_signed_polarity_status"],
            "forbidden_inference": relation.get("forbidden_inference") or "none recorded",
            "does_not_measure": relation.get("does_not_measure") or "none recorded",
            "governed_row_payload_hash": relation["governed_row_payload_hash"],
            "p2_exact_identity_sha256": relation.get("p2_exact_identity_sha256") or p2["exact_identity_sha256"],
        }
    return payload


def residual(residual_id: str, scope: str, field: str, status: str, reason: str,
             dependent: str, unaffected: str, next_step: str) -> dict[str, str]:
    return {
        "residual_id": residual_id,
        "scope": scope,
        "field": field,
        "status": status,
        "reason": reason,
        "dependent_operation": dependent,
        "unaffected_scope": unaffected,
        "owner": "R157_EVS_LANE",
        "next_step": next_step,
    }


def build_one(sid: str, *, artifact_commit: str) -> dict[str, Any]:
    roster = source_roster_entry(sid)
    var = CHOSEN[sid]
    wave = roster["wave"]
    source_sha = roster["source_sha256"]
    physical = {p["ordinal"]: p for p in iter_physical_slots(sid)}
    codebook = {c["var_name"]: c for c in iter_codebook_rows(sid)}
    items = list(iter_item_evidence(sid))
    if len(items) != roster["original_items"] or len(physical) != roster["physical_columns"]:
        raise RuntimeError(f"{sid}: evidence counts do not match roster")
    selected = next(x for x in items if x["source_variable_code"] == var)
    item_slot = next(p for p in physical.values() if p["name"] == var)
    country_slot = next(p for p in physical.values() if p["name"] == "country")
    key_slot = next(p for p in physical.values() if p["name"] == "id_cocas")
    relation = selected.get("relation")
    if relation is None:
        raise RuntimeError(f"{sid}: selected item lacks exact relation")
    evidence_hash = relation["governed_row_payload_hash"]
    fixture_id = f"R157-EVS-{sid}-{var}-NONRESPONDENT"
    special_map = {
        -1.0: "DK", -2.0: "REFUSAL", -3.0: "IAP", -4.0: "NOT_ASKED",
        -5.0: "MISSING", -8.0: "SOURCE_SPECIFIC_SPECIAL", -9.0: "SOURCE_SPECIFIC_SPECIAL",
        -10.0: "SOURCE_SPECIFIC_SPECIAL",
    }

    # Fixture rows cover all substantive codes, all source special codes, and
    # one system-missing cell for each selected item.
    labels = item_slot.get("value_labels") or {}
    substantive = sorted(float(k) for k in labels if _is_number(k) and float(k) >= 1)
    specials = sorted(float(k) for k in labels if _is_number(k) and float(k) < 0)
    item_values = [*substantive, *specials, None]
    rows = []
    for index, value in enumerate(item_values):
        row = index + 1
        key = 900000000.0 + (int(sid[-2:]) * 1000.0) + row
        country = COUNTRY_FIXTURE_VALUES[index % len(COUNTRY_FIXTURE_VALUES)]
        rows.extend([
            {"row_ordinal": row, "variable_ordinal": item_slot["ordinal"], "variable_name": item_slot["name"],
             "raw_value": value, "missing_state": ("SYSTEM_MISSING" if value is None else "OBSERVED_STORAGE_VALUE"),
             "source_missing_declaration": None},
            {"row_ordinal": row, "variable_ordinal": country_slot["ordinal"], "variable_name": country_slot["name"],
             "raw_value": country, "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None},
            {"row_ordinal": row, "variable_ordinal": key_slot["ordinal"], "variable_name": key_slot["name"],
             "raw_value": key, "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None},
        ])
    # Temporary values for expected states; rebuilt after authority refs exist.
    expected_states = []
    expected_canonical = []
    for value in item_values:
        if value is None:
            expected_states.append("MISSING"); expected_canonical.append(None)
        else:
            expected_states.append(response_state(float(value), special_map))
            expected_canonical.append(canonical_token(float(value)) if float(value) >= 1 else None)
    fixture_doc = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
        "fixture_id": fixture_id,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "row_count": len(item_values),
        "cells": rows,
        "expected_results": {
            "fixture_only": True,
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "response_event_count": len(item_values),
            "coordinate_fact_count": len(item_values),
            "routing_fact_count": len(item_values),
            "response_states": expected_states,
            "canonical_values": expected_canonical,
            "weight_section": "NOT_APPLICABLE",
            "source_relation_section": "DISTINCT_BY_DEFAULT",
        },
    }
    fixture_sha = fixture_document_sha256(fixture_doc)
    fixture_doc["fixture_source_sha256"] = fixture_sha

    original_snaps, original_refs = build_authorities(
        sid, wave, source_sha, evidence_hash, decision="DEFER")
    fixture_snaps, fixture_refs = build_authorities(
        sid, wave, source_sha, evidence_hash, decision="ALLOW",
        fixture_sha=fixture_sha, fixture_id=fixture_id)
    original_universe_payload, original_universe = universe_payload(
        sid, wave, source_sha, original_refs["source"], fixture=False)
    fixture_universe_payload, fixture_universe = universe_payload(
        sid, wave, source_sha, fixture_refs["source"], fixture=True, fixture_id=fixture_id)
    topology_ref = ref("RESPONSE_TOPOLOGY", f"{sid}:{var}:SCALAR_SINGULAR",
                       sha_json({"sid": sid, "var": var, "topology": "scalar"}))
    original_question = {
        "question_id": var,
        "empirical_universe_ref": original_universe.ref.as_dict(),
        "native_question_ref": ref("NATIVE_QUESTION", f"{sid}:{var}", selected["exact_identity_sha256"]).as_dict(),
        "instrument_question_version": wave,
        "canonical_question_ref_or_typed_absence": TypedAbsence("NOT_AUTHORIZED").as_dict(),
        "component_subitem_ref_or_typed_absence": TypedAbsence("NOT_APPLICABLE").as_dict(),
        "semantic_authority_ref": original_refs["source"].as_dict(),
        "topology_authority_ref": original_refs["topology"].as_dict(),
        "item_evidence": {"implementation_id": selected["implementation_id"],
                          "exact_identity_sha256": selected["exact_identity_sha256"],
                          "relation_join_status": "EXACT"},
    }
    fixture_question = deepcopy(original_question)
    fixture_question["empirical_universe_ref"] = fixture_universe.ref.as_dict()
    fixture_question["semantic_authority_ref"] = fixture_refs["source"].as_dict()
    fixture_question["topology_authority_ref"] = fixture_refs["topology"].as_dict()

    original_values, _ = response_values(selected, item_slot, original_refs["mapping"], topology_ref, special_map)
    fixture_values, _ = response_values(selected, item_slot, fixture_refs["mapping"], topology_ref, special_map)
    original_coord = coordinate_payload(country_slot, original_refs["coordinate"], wave=wave, topology_ref=topology_ref)
    fixture_coord = coordinate_payload(country_slot, fixture_refs["coordinate"], wave=wave, topology_ref=topology_ref)
    original_routing = routing_rule(selected, var, original_refs["routing"], topology_ref, wave)
    fixture_routing = routing_rule(selected, var, fixture_refs["routing"], topology_ref, wave)

    original_physical = [physical_slot_payload(p, selected=p["name"] == var,
                                               country=p["name"] == "country",
                                               key_slot=p["name"] == "id_cocas")
                         for p in sorted(physical.values(), key=lambda x: x["ordinal"])]
    fixture_physical = [physical_slot_payload(p, selected=p["name"] == var,
                                              country=p["name"] == "country",
                                              key_slot=p["name"] == "id_cocas")
                        for p in sorted((item_slot, country_slot, key_slot), key=lambda x: x["ordinal"])]
    original_items = [item_payload(item, selected=item["source_variable_code"] == var, supported_var=var)
                      for item in items]
    fixture_items = [item_payload(selected, selected=True, supported_var=var)]
    original_required = tuple(original_refs[k] for k in ("source", "mapping", "topology", "coordinate", "routing", "replay", "projection"))
    fixture_required = tuple(fixture_refs[k] for k in ("source", "mapping", "topology", "coordinate", "routing", "replay", "projection"))
    original_ids = [x["implementation_id"] for x in original_items]
    unsupported_ids = [x for x in original_ids if x != selected["implementation_id"]]
    unbound_ordinals = [p["ordinal"] for p in original_physical
                        if p["name"] not in {var, "country", "id_cocas"}]

    common_identity = {
        "source_id": sid,
        "family": roster["family"],
        "wave": wave,
        "source_family_id": "EVS",
        "study_product_id": "EVS",
        "release_id": f"EVS_{wave}",
        "instrument_release_id": f"SRC{sid[-2:]}_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
        "source_artifact_id": roster["source_artifact_id"],
        "expected_source_sha256": source_sha,
        "source_format": roster["format"],
        "source_row_count": roster["rows"],
        "source_column_count": roster["physical_columns"],
        "source_bytes": roster["bytes"],
        "codebook_rows": roster["codebook_rows"],
        "original_item_count": roster["original_items"],
        "source_snapshot_retention_ref": ExactRef("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:evs:{sid}:source", source_sha).as_dict(),
        "metadata_witness_ref": ExactRef("R154_PHYSICAL_METADATA", roster["metadata_witness"]["path"],
                                         roster["metadata_witness"]["sha256"]).as_dict(),
        "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": f"{sid}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
        "reader": {
            "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
            "configuration_ref": ref("READER_CONFIGURATION", f"{sid}:sav", sha_json({
                "source_sha256": source_sha, "encoding": roster["reader"]["required_encoding"],
            })).as_dict(),
            "encoding": (None if roster["reader"]["required_encoding"] is None else {
                "value": roster["reader"]["required_encoding"],
                "sha256": source_sha,
                "authority_status": roster["reader"]["encoding_authority_status"],
            }),
        },
    }
    common_respondents = {
        "subject_unit": "SOURCE_NATIVE_UNIFIED_RESPONDENT",
        "respondent_namespace": f"urn:rawlsing:r157:evs:{sid}:id_cocas",
        "respondent_key_pattern": f"EVS-{wave}-ROW-{{row_ordinal:06d}}",
        "source_native_key_slot": {"ordinal": key_slot["ordinal"], "name": key_slot["name"]},
        "identity_map_authority_ref": None,
        "row_identity_grade": "SOURCE_NATIVE_ID_COCAS",
    }
    common_runtime = {
        "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
        "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
        "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
        "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
        "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
        "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
        "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
        "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
        "reader_encoding_transport": "R157_P3_QUALIFIED_CONFIG_TRANSPORT",
    }
    manifest = load_manifest()
    pinned = [
        {key: value for key, value in entry.items()
         if key in {"kind", "sha256", "commit", "path", "bytes", "locator"}}
        for entry in manifest["pinned_inputs"]
    ]
    common_evidence = {
        "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
        "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
        "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
        "pinned_inputs": pinned,
        "field_evidence": [
            {"field": "items[0].implementation_id", "refs": [
                ref("H48_ITEM_AUTHORITY", f"{sid}:{selected['implementation_id']}:h48", selected["exact_identity_sha256"]).as_dict(),
                ref("P2_PHASE0_ROW", f"{sid}:{selected['implementation_id']}:p2", selected["p2"]["exact_identity_sha256"]).as_dict(),
            ]},
            {"field": "items[0].relation", "refs": [
                ref("FULL_RELATION_ROW", f"{sid}:{relation['question_id']}:relation", evidence_hash).as_dict(),
            ]},
            {"field": "physical_slots.item", "refs": [
                ref("CODEBOOK_ROW", f"{sid}:{var}", item_slot["codebook_mapping"]["row_hash"]).as_dict(),
            ]},
        ],
        "limits": [
            "Prior authority evidence is reused with its original grade and limits.",
            "Original authority is DEFER; fixture authority is NONRESPONDENT_FIXTURE_ONLY.",
            "No original respondent rows or original source file bytes were read.",
        ],
    }
    def make_config(*, fixture: bool) -> dict[str, Any]:
        if fixture:
            binding = {
                "identity_class": "NONRESPONDENT_FIXTURE",
                "source_sha256": fixture_sha,
                "row_count": len(item_values),
                "source_snapshot_ref": ExactRef("FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:evs:{fixture_id}", fixture_sha).as_dict(),
                "fixture_provenance": {
                    "fixture_id": fixture_id,
                    "provenance": "Repository-generated nonrespondent EVS fixture; no original respondents represented.",
                    "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                    "original_source_id": sid,
                    "original_source_sha256": source_sha,
                    "no_original_respondents": True,
                    "fixture_study_product_id": f"R157_FIXTURE/EVS/{wave}",
                    "fixture_release_id": f"R157_FIXTURE_RELEASE/EVS/{wave}",
                    "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/EVS/{wave}",
                },
            }
            authority_section = {
                **fixture_snaps,
                "projection_identity_ref": ref("C11_SEMANTIC_PROJECTION", f"{sid}:{var}:fixture",
                                               sha_json({"sid": sid, "var": var, "fixture_sha": fixture_sha})).as_dict(),
                "tie_order_ref": ref("ORDER_RULE", f"{sid}:fixture:canonical-ref-sort",
                                     sha_json({"sid": sid, "fixture": fixture_sha})).as_dict(),
                "replay_protocol_version": "1.0.0",
            }
            universe = {"universes": [fixture_universe_payload]}
            question = fixture_question
            response_slot = {"slot": {"ordinal": item_slot["ordinal"], "name": item_slot["name"]},
                             "question_id": var, "values": fixture_values}
            coordinate = fixture_coord
            routing = [fixture_routing]
            physical_slots = fixture_physical
            items_payload = fixture_items
            coverage = {
                "physical_slots_total": roster["physical_columns"],
                "items_total": roster["original_items"],
                "physical_slots_included": sorted({item_slot["ordinal"], country_slot["ordinal"], key_slot["ordinal"]}),
                "physical_slots_excluded": [],
                "items_included": [selected["implementation_id"]],
                "items_excluded": [],
                "partial_scope_reason": "P3 EVS nonrespondent fixture binds only the selected scalar item, country coordinate and id_cocas key.",
            }
            supported_scope = {
                "scope_id": f"EVS-{sid}-{var}-P3-FIXTURE",
                "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
                "declared_supported": True,
                "supported_question_ids": [var],
                "native_validation_expectation": "POSITIVE_RELEASE",
                "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
                "supported_unit_slice": "SOURCE_NATIVE_UNIFIED_RESPONDENT_ID_COCAS",
                "supported_form_slice": f"EVS {wave} scalar item",
                "notes": ["Fixture authority is explicitly nonrespondent and does not establish original-source authority."],
            }
            residuals = [
                residual("ORIGINAL_AUTHORITY_DEFER", f"{sid}/{var}", "authority.snapshots", "FIXTURE_ONLY",
                         "The fixture proves the constructor; original EVS authority remains DEFER.",
                         "original-source native validation", "fixture native validation", "P4/integration supplies source-grounded original authority."),
                residual("UNSUPPORTED_ITEM_SLICE", f"{sid}", "items", "HELD_UNSUPPORTED_SLICE",
                         f"{len(unsupported_ids)} EVS items are accounted but not bound in this fixture slice.",
                         "response-slot construction for unselected items", "selected scalar item and full source ledger", "P4 lane expansion."),
                residual("WEIGHTS_NOT_CLAIMED", f"{sid}", "weight_slots", "NOT_CLAIMED",
                         "No weight design/estimand authority is claimed for this slice.",
                         "weighted estimates", "raw/unweighted fixture validation", "P4 weighted lane if warranted."),
            ]
            return {
                "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
                "config_id": f"R157-EVS-{sid}-{var}-FIXTURE",
                "config_revision": 1,
                "config_purpose": "NONRESPONDENT_FIXTURE",
                "identity": common_identity,
                "binding": binding,
                "authority": authority_section,
                "universe": universe,
                "respondents": common_respondents,
                "questions": [question],
                "physical_slots": physical_slots,
                "items": items_payload,
                "response_slots": [response_slot],
                "coordinate_slots": [coordinate],
                "weight_slots": [],
                "routing": routing,
                "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
                "replay": {
                    "predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
                    "comparator": TypedAbsence("DEFERRED").as_dict(),
                    "discovery": TypedAbsence("DEFERRED").as_dict(),
                    "structural": TypedAbsence("NOT_APPLICABLE").as_dict(),
                },
                "supported_scope": supported_scope,
                "coverage": coverage,
                "residuals": residuals,
                "evidence": common_evidence,
                "runtime": common_runtime,
            }
        authority_section = {
            **original_snaps,
            "projection_identity_ref": ref("C11_SEMANTIC_PROJECTION", f"{sid}:{var}:source",
                                           sha_json({"sid": sid, "var": var, "source_sha": source_sha})).as_dict(),
            "tie_order_ref": ref("ORDER_RULE", f"{sid}:source:canonical-ref-sort",
                                 sha_json({"sid": sid, "source": source_sha})).as_dict(),
            "replay_protocol_version": "1.0.0",
        }
        residuals = [
            residual("ORIGINAL_AUTHORITY_DEFER", f"{sid}/{var}", "authority.snapshots", "DEFER",
                     "Original source authority is retained as prior evidence only; no ALLOW authority is invented.",
                     "original-source native validation/execution", "fixture native validation and source ledger", "P4/integration supplies source-grounded authority."),
            residual("UNSUPPORTED_ITEM_SLICE", f"{sid}", "items", "HELD_UNSUPPORTED_SLICE",
                     f"{len(unsupported_ids)} EVS items are accounted but not bound in the P3 supported slice.",
                     "response-slot construction for unselected items", "selected scalar item and full source ledger", "P4 lane expansion."),
            residual("UNBOUND_PHYSICAL_SLOT_SLICE", f"{sid}", "physical_slots", "HELD_UNSUPPORTED_SLICE",
                     f"{len(unbound_ordinals)} physical slots are accounted but not bound in the P3 supported slice.",
                     "native slot construction for unselected slots", "selected item/country/id_cocas slots", "P4 lane expansion."),
            residual("WEIGHTS_NOT_CLAIMED", f"{sid}", "weight_slots", "NOT_CLAIMED",
                     "No weight design/estimand authority is claimed for this slice.",
                     "weighted estimates", "raw/unweighted fixture validation", "P4 weighted lane if warranted."),
            residual("COUNTRY_NO_CANONICAL_CROSSWALK", f"{sid}", "coordinate_slots.country", "RAW_ONLY",
                     "Country code is carried as a source-native coordinate; no canonical country crosswalk is claimed.",
                     "canonical country comparisons", "source-native country coordinate", "P4 material/context lane if warranted."),
        ]
        if sid in {"SRC11", "SRC12", "SRC15"}:
            residuals.append(residual(
                "READER_WINDOWS1252_NOT_OVERRIDDEN", f"{sid}", "identity.reader.encoding", "NOT_OVERRIDDEN",
                "No exact decoder allowlist entry exists for this source SHA; automatic encoding guessing is forbidden.",
                "source text decode", "measured numeric item and metadata facts", "P3 reader lane only if exact allowlist evidence arises."))
        return {
            "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
            "config_id": f"R157-EVS-{sid}-{var}-SOURCE",
            "config_revision": 1,
            "config_purpose": "SOURCE_PREPARATION",
            "identity": common_identity,
            "binding": {
                "identity_class": "ORIGINAL_SOURCE",
                "source_sha256": source_sha,
                "row_count": roster["rows"],
                "source_snapshot_ref": common_identity["source_snapshot_retention_ref"],
                "fixture_provenance": None,
            },
            "authority": authority_section,
            "universe": {"universes": [original_universe_payload]},
            "respondents": common_respondents,
            "questions": [original_question],
            "physical_slots": original_physical,
            "items": original_items,
            "response_slots": [{"slot": {"ordinal": item_slot["ordinal"], "name": item_slot["name"]},
                                "question_id": var, "values": original_values}],
            "coordinate_slots": [original_coord],
            "weight_slots": [],
            "routing": [original_routing],
            "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
            "replay": {
                "predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
                "comparator": TypedAbsence("DEFERRED").as_dict(),
                "discovery": TypedAbsence("DEFERRED").as_dict(),
                "structural": TypedAbsence("NOT_APPLICABLE").as_dict(),
            },
            "supported_scope": {
                "scope_id": f"EVS-{sid}-{var}-P3-SOURCE",
                "purpose": "SOURCE_PREPARATION",
                "declared_supported": False,
                "supported_question_ids": [var],
                "native_validation_expectation": "NOT_RUN",
                "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
                "supported_unit_slice": "SOURCE_NATIVE_UNIFIED_RESPONDENT_ID_COCAS",
                "supported_form_slice": f"EVS {wave} scalar item",
                "notes": ["Source recipe is fixture-proven; original authority remains DEFER and is not a current native acceptance claim."],
            },
            "coverage": {
                "physical_slots_total": roster["physical_columns"],
                "items_total": roster["original_items"],
                "physical_slots_included": sorted(physical),
                "physical_slots_excluded": [],
                "items_included": original_ids,
                "items_excluded": [],
            },
            "residuals": residuals,
            "evidence": common_evidence,
            "runtime": common_runtime,
        }

    original_config = make_config(fixture=False)
    fixture_config = make_config(fixture=True)
    # Validate both configs through the frozen schema before writing.
    from rawlsing_next.source_configuration.schema import SourceConfig
    SourceConfig(original_config)
    fixture_cfg = SourceConfig(fixture_config)
    fixture_stream = fixture_stream_from_document(fixture_doc)
    keys = row_native_keys_from_transport(fixture_cfg, stream=fixture_stream)
    fixture_release = build_validated_c11_release_from_config(fixture_cfg, stream=fixture_stream)
    repository, repository_release = build_source_backed_c11_repository_from_config(fixture_cfg, fixture_stream)
    projection = build_governed_c11_projection(fixture_cfg, row_native_keys=keys)
    events = [x for x in fixture_release.public_objects if isinstance(x, RespondentEvent)]
    row_by_object = {r.ref.object_id: index for index, r in enumerate(projection.respondents, 1)}
    events.sort(key=lambda event: row_by_object[dict(event.scoped_respondent_ref)["object_id"]])
    actual_states = [x.response_state for x in events]
    actual_canonical = [x.canonical_response_value_if_authorized for x in events]
    expected = fixture_doc["expected_results"]
    if actual_states != expected["response_states"] or actual_canonical != expected["canonical_values"]:
        raise RuntimeError(f"{sid}: fixture expected/native mismatch")
    keys = row_native_keys_from_transport(fixture_cfg, stream=fixture_stream)
    if keys is None or len(keys) != fixture_stream.row_count:
        raise RuntimeError(f"{sid}: key extraction failed")
    reader = reader_configuration_from_config(original_config)
    request = source_read_request_from_config(
        original_config, host="R157_EVS_LANE", purpose="R157_EVS_CONFIGURATION_PREPARATION",
        consumer_use="R157_EVS_CONFIGURATION_PREPARATION", semantic_use_scope=("SOURCE_CONFIGURATION_PREPARATION",))
    data_dir = DATA / sid
    val_dir = VALIDATION / sid
    data_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    original_path = data_dir / f"{sid}.config.json"
    fixture_config_path = data_dir / f"{sid}.fixture.config.json"
    fixture_path = val_dir / f"{sid}.fixture.json"
    original_path.write_text(json.dumps(original_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fixture_config_path.write_text(json.dumps(fixture_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fixture_path.write_text(json.dumps(fixture_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    accounting = {
        "schema": "PYAT_R157_EVS_SOURCE_EVIDENCE_ACCOUNTING@1.0.0",
        "source_id": sid,
        "family": roster["family"],
        "wave": wave,
        "source_sha256": source_sha,
        "counts": {
            "physical_columns": len(physical),
            "codebook_rows": len(codebook),
            "original_items": len(items),
            "exact_relation_matches": sum(1 for x in items if x.get("relation")),
            "unmatched_relation_ids": 0,
            "physical_only": roster["physical_only"],
            "codebook_only": roster["codebook_only"],
        },
        "selected_item": {
            "implementation_id": selected["implementation_id"],
            "source_variable_code": var,
            "exact_identity_sha256": selected["exact_identity_sha256"],
            "p2_exact_identity_sha256": selected["p2"]["exact_identity_sha256"],
            "relation_governed_payload_hash": evidence_hash,
            "question_text": selected["p2"]["question_text"],
            "response_classes": selected["p2"]["response_classes"],
            "routing_status": "UNCONDITIONAL_SOURCE_PROVEN",
            "response_binding_status": selected["p2"]["response_binding_status"],
            "manual_response_topology": relation["manual_response_topology"],
            "manual_position_conditioning": relation["manual_position_conditioning"],
            "manual_semantic_role": relation["manual_semantic_role"],
            "manual_signed_polarity_status": relation["manual_signed_polarity_status"],
            "directional_certification_status": relation.get("manual_directional_certification_status"),
        },
        "slots": {
            "country": {"ordinal": country_slot["ordinal"], "name": country_slot["name"]},
            "id_cocas": {"ordinal": key_slot["ordinal"], "name": key_slot["name"]},
            "item": {"ordinal": item_slot["ordinal"], "name": item_slot["name"]},
        },
        "weights": {"claimed": False, "reason": "No weight design/estimand authority is claimed."},
        "reader": {
            "required_encoding": roster["reader"]["required_encoding"],
            "decoder_allowlist_encoding": roster["reader"]["decoder_allowlist_encoding"],
            "configuration_ref": reader.configuration_ref.as_dict(),
            "request_source_sha256": request.source_sha256,
        },
        "evidence_refs": common_evidence["field_evidence"],
        "no_drop": {"items_unaccounted": 0, "slots_unaccounted": 0},
    }
    ledger = {
        "schema": "PYAT_R157_EVS_EXCEPTION_LEDGER@1.0.0",
        "source_id": sid,
        "entries": [
            {
                "residual_id": "ORIGINAL_AUTHORITY_DEFER",
                "source_id": sid,
                "implementation_id": selected["implementation_id"],
                "required_native_field": "authority.snapshots",
                "current_value": "DEFER",
                "exact_evidence_refs": common_evidence["field_evidence"],
                "missing_fact": "No current source-specific ALLOW authority snapshot is established.",
                "affected_operation_or_slice": "original-source native validation/execution",
                "unaffected_usable_slice": "fixture native validation; selected source recipe",
                "owner_and_next_step": "R157_EVS_LANE -> P4/integration source-grounded authority",
                "status": "HELD_DEFER_NOT_BLOCKING_FIXTURE",
                "resolution_evidence": None,
            },
            {
                "residual_id": "UNSUPPORTED_ITEM_SLICE",
                "source_id": sid,
                "implementation_ids": unsupported_ids,
                "count": len(unsupported_ids),
                "required_native_field": "response_slots",
                "current_value": "ACCOUNTED_UNSUPPORTED",
                "exact_evidence_refs": [{"field": "ITEM_EVIDENCE.jsonl.gz", "all_implementation_ids": original_ids}],
                "missing_fact": "Items are accounted but not bound in the P3 EVS supported scalar slice.",
                "affected_operation_or_slice": "response-slot construction for unselected items",
                "unaffected_usable_slice": "selected scalar item, country coordinate and key slot",
                "owner_and_next_step": "R157_EVS_LANE -> P4 lane expansion",
                "status": "HELD_UNSUPPORTED_SLICE",
                "resolution_evidence": None,
            },
            {
                "residual_id": "UNBOUND_PHYSICAL_SLOT_SLICE",
                "source_id": sid,
                "physical_slot_ordinals": unbound_ordinals,
                "count": len(unbound_ordinals),
                "required_native_field": "physical_slots native binding",
                "current_value": "ACCOUNTED_UNSUPPORTED",
                "exact_evidence_refs": [{"field": "PHYSICAL_SLOTS.jsonl.gz", "source_id": sid}],
                "missing_fact": "Slots are retained but not bound in the P3 supported slice.",
                "affected_operation_or_slice": "native slot construction for unselected slots",
                "unaffected_usable_slice": "selected item/country/id_cocas slots",
                "owner_and_next_step": "R157_EVS_LANE -> P4 lane expansion",
                "status": "HELD_UNSUPPORTED_SLICE",
                "resolution_evidence": None,
            },
            {
                "residual_id": "WEIGHTS_NOT_CLAIMED",
                "source_id": sid,
                "required_native_field": "weight_slots",
                "current_value": "NOT_CLAIMED",
                "exact_evidence_refs": [{"field": "SOURCE_ROSTER.json", "source_id": sid}],
                "missing_fact": "No weight design/estimand authority is claimed.",
                "affected_operation_or_slice": "weighted estimates",
                "unaffected_usable_slice": "raw/unweighted fixture validation",
                "owner_and_next_step": "R157_EVS_LANE -> P4 weighted lane if warranted",
                "status": "NOT_CLAIMED",
                "resolution_evidence": None,
            },
        ],
    }
    if sid in {"SRC11", "SRC12", "SRC15"}:
        ledger["entries"].append({
            "residual_id": "READER_WINDOWS1252_NOT_OVERRIDDEN",
            "source_id": sid,
            "required_native_field": "identity.reader.encoding",
            "current_value": "null",
            "exact_evidence_refs": [{"field": "SOURCE_ROSTER.json", "source_id": sid,
                                     "decoder_allowlist_encoding": None}],
            "missing_fact": "No exact decoder allowlist entry exists for this SHA; automatic guessing is forbidden.",
            "affected_operation_or_slice": "source text decode",
            "unaffected_usable_slice": "numeric selected item and metadata facts",
            "owner_and_next_step": "P3 reader lane only if exact allowlist evidence arises",
            "status": "NOT_OVERRIDDEN",
            "resolution_evidence": None,
        })
    native = {
        "schema": "PYAT_R157_EVS_NATIVE_RESULTS@1.0.0",
        "source_id": sid,
        "config_path": str(original_path.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(original_config),
        "fixture_config_path": str(fixture_config_path.relative_to(ROOT)),
        "fixture_config_sha256": canonical_config_hash(fixture_config),
        "fixture_path": str(fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        "fixture_source_sha256": fixture_sha,
        "original_schema_valid": True,
        "original_native_validation": "NOT_RUN__AUTHORITY_DEFER",
        "original_projection_construction": "NOT_RUN__RECIPE_ONLY",
        "fixture_native_validation": {
            "projection_type": type(projection).__name__,
            "release_type": type(fixture_release).__name__,
            "release_ref": fixture_release.release_ref.as_dict(),
            "semantic_release_hash": fixture_release.semantic_release_hash,
            "replay_manifest_ref": fixture_release.replay_manifest.ref.as_dict(),
            "m01_m18_coverage": {k: list(v) for k, v in fixture_release.m01_m18_coverage.items()},
            "response_event_count": len(events),
            "coordinate_fact_count": sum(1 for x in fixture_release.public_objects if type(x).__name__ == "EmpiricalCoordinateFact"),
            "routing_fact_count": sum(1 for x in fixture_release.public_objects if type(x).__name__ == "RoutingEligibilityFact"),
            "response_states": actual_states,
            "canonical_values": actual_canonical,
            "key_count": len(keys),
            "repository_type": type(repository).__name__,
            "repository_release_matches": repository_release.release_ref == fixture_release.release_ref,
            "expected_match": True,
        },
        "reader": {
            "encoding": reader.encoding,
            "authority_status": reader.authority_status,
            "request_source_sha256": request.source_sha256,
            "source_read_performed": False,
        },
        "native_calls": [
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.row_native_keys_from_transport",
            "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "rawlsing_next.source_configuration.reader.source_read_request_from_config",
        ],
        "commands": [
            "PYTHONPATH=. python3 source_pre553_validation/SRC11/build_evs_lane.py",
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts=''",
        ],
        "artifact_commit": artifact_commit,
        "limits": [
            "Original authority is DEFER; no original-source native acceptance is claimed.",
            "Fixture authority is NONRESPONDENT_FIXTURE_ONLY; fixture SHA is not original source identity.",
            "No original respondent rows or original source file bytes were read.",
            "No original empirical workload is issued.",
        ],
    }
    accounting_path = val_dir / "EVIDENCE_ACCOUNTING.json"
    ledger_path = val_dir / "EXCEPTION_LEDGER.json"
    native_path = val_dir / "NATIVE_RESULTS.json"
    accounting_path.write_text(json.dumps(accounting, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    native_path.write_text(json.dumps(native, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "source_id": sid,
        "selected_item": var,
        "config_path": str(original_path.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(original_config),
        "fixture_config_path": str(fixture_config_path.relative_to(ROOT)),
        "fixture_config_sha256": canonical_config_hash(fixture_config),
        "fixture_path": str(fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        "fixture_source_sha256": fixture_sha,
        "release_ref": fixture_release.release_ref.as_dict(),
        "release_hash": fixture_release.semantic_release_hash,
        "key_count": len(keys),
        "counts": accounting["counts"],
        "unsupported_item_count": len(unsupported_ids),
        "unbound_slot_count": len(unbound_ordinals),
        "reader_encoding": reader.encoding,
        "native_results_path": str(native_path.relative_to(ROOT)),
        "evidence_accounting_path": str(accounting_path.relative_to(ROOT)),
        "exception_ledger_path": str(ledger_path.relative_to(ROOT)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args()
    artifact_commit = args.artifact_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    summaries = [build_one(sid, artifact_commit=artifact_commit) for sid in CHOSEN]
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "rawlsing_next/tests/test_source_configuration_foundation.py",
         "rawlsing_next/tests/test_source_configuration_p3.py", "-k", "not r154",
         "-q", "-o", "addopts="],
        cwd=ROOT, env={**__import__("os").environ, "PYTHONPATH": str(ROOT)},
        text=True, capture_output=True)
    test_tail = (tests.stdout.strip().splitlines() or [""])[-1]
    if tests.returncode != 0:
        raise SystemExit(f"shared contract tests failed: {test_tail}\n{tests.stdout}")
    lane = {
        "schema": "PYAT_R157_EVS_LANE_RETURN@1.0.0",
        "lane_id": "EVS",
        "status": "LANE_COMPLETE__SOURCE_CONFIGS_AND_FIXTURE_POSITIVES",
        "branch": "agent/pyat-pre553-r157-evs",
        "artifact_commit": artifact_commit,
        "base_p0_tip": "d8d7087a8e56c24042bf5945fea1c97eb0d6c710",
        "base_p3_tip": "519355ec2215409b40d566ef13c3b21f611e0726",
        "source_ids": list(CHOSEN),
        "sources": summaries,
        "source_manifests": {
            sid: {
                "config": f"rawlsing_next/source_configuration/data/{sid}/{sid}.config.json",
                "fixture_config": f"rawlsing_next/source_configuration/data/{sid}/{sid}.fixture.config.json",
                "fixture": f"source_pre553_validation/{sid}/{sid}.fixture.json",
                "native_results": f"source_pre553_validation/{sid}/NATIVE_RESULTS.json",
                "evidence_accounting": f"source_pre553_validation/{sid}/EVIDENCE_ACCOUNTING.json",
                "exception_ledger": f"source_pre553_validation/{sid}/EXCEPTION_LEDGER.json",
            } for sid in CHOSEN
        },
        "commands": [
            "PYTHONPATH=. python3 source_pre553_validation/SRC11/build_evs_lane.py",
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -k 'not r154' -q -o addopts=''",
        ],
        "tests": {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -k 'not r154' -q -o addopts=''",
                  "result": test_tail, "passed": tests.returncode == 0, "skipped": "skipped" in test_tail,
                  "deselected_note": "Two legacy R154 loader tests are deselected; their runtime file is absent from this sparse EVS checkout and they are outside the EVS source-configuration boundary."},
        "native_positives": {x["source_id"]: {"release_ref": x["release_ref"], "release_hash": x["release_hash"], "key_count": x["key_count"]} for x in summaries},
        "native_api_calls": [
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.row_native_keys_from_transport",
            "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "rawlsing_next.source_configuration.reader.source_read_request_from_config",
            "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
        ],
        "blockers": [
            {
                "id": "ORIGINAL_AUTHORITY_DEFER",
                "scope": "SRC11-SRC15 original configs",
                "status": "HELD_NON_BLOCKING",
                "reason": "Original EVS authority snapshots are DEFER/prior-evidence only; fixture-native positives do not become original ALLOW authority.",
                "owner_and_next_step": "P4/integration supplies exact source-grounded authority if original native validation is required.",
            },
            {
                "id": "UNSUPPORTED_EVS_SLICE",
                "scope": "SRC11-SRC15",
                "status": "HELD_NON_BLOCKING",
                "reason": f"{sum(x['unsupported_item_count'] for x in summaries)} items and {sum(x['unbound_slot_count'] for x in summaries)} slots are accounted but outside the five supported scalar slices.",
                "owner_and_next_step": "P4 lane expansion, preserving exact item/slot evidence and source-specific topology.",
            },
            {
                "id": "WEIGHTS_NOT_CLAIMED",
                "scope": "SRC11-SRC15",
                "status": "NOT_CLAIMED",
                "reason": "No weight design/estimand authority is claimed; fixture validation is raw/unweighted.",
                "owner_and_next_step": "P4 weighted lane only if the prepared scope claims weights.",
            },
        ],
        "no_drop": {
            "sources": 5,
            "physical_slots": sum(x["counts"]["physical_columns"] for x in summaries),
            "items": sum(x["counts"]["original_items"] for x in summaries),
            "exact_relation_matches": sum(x["counts"]["exact_relation_matches"] for x in summaries),
            "unmatched_relation_ids": 0,
            "unsupported_items_accounted": sum(x["unsupported_item_count"] for x in summaries),
            "unbound_slots_accounted": sum(x["unbound_slot_count"] for x in summaries),
        },
        "supported_scope": {
            "kind": "ONE_SCALAR_SOURCE_ITEM_PER_WAVE_PLUS_COUNTRY_AND_ID_COCAS",
            "items": {sid: var for sid, var in CHOSEN.items()},
            "all_slots_and_items_retained_in_source_configs": True,
            "fixture_positives": 5,
        },
        "scope_limits": [
            "Original authority is DEFER; original-source native validation/execution is not claimed.",
            "Fixture authority is NONRESPONDENT_FIXTURE_ONLY; fixture SHA is not original source identity.",
            "No original respondent rows or original source file bytes were read.",
            "No original empirical workload is issued.",
            "All other EVS items/slots are accounted in source configs and exact exception ledgers; P4 lane expansion remains.",
            "No shared runtime/schema/factory/native-validator changes, no other source directories touched.",
        ],
        "next_integration_edge": "HQ/P4: consume the five source configs, fixture configs, NATIVE_RESULTS and exception ledgers; expand unsupported EVS items/slots per lane and supply source-grounded original authority if required.",
    }
    lane_path = VALIDATION / "SRC11" / "LANE_RETURN.json"
    lane_path.write_text(json.dumps(lane, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact_commit": artifact_commit, "tests": test_tail, "lane_return": str(lane_path),
                      "sources": {x["source_id"]: x["release_ref"]["content_hash"] for x in summaries}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
