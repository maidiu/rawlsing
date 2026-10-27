"""Build the R157 LATIN lane source configurations and nonrespondent fixtures.

Writes only the LATIN lane-owned paths:
  rawlsing_next/source_configuration/data/SRC24..26/
  source_pre553_validation/SRC24..26/

The original configs keep the original source identity and DEFER source-execution
authority.  Fixture configs use a distinct fixture byte identity, fixture-only
ALLOW authority and are the only configs exercised through the native C11
validator.  No original respondent rows are read or represented here.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse  # noqa: E402
from rawlsing_next.source_configuration import evidence as E  # noqa: E402

DATA_ROOT = ROOT / "rawlsing_next/source_configuration/data"
VAL_ROOT = ROOT / "source_pre553_validation"

SOURCE_IDS = ("SRC24", "SRC25", "SRC26")
WAVE_INSTRUMENT_PREFIX = "LATINOBAROMETRO"

# Response layouts selected for the declared supported slice.  Every entry is
# a real source item with exact H48/P2/relation evidence; the physical slot set
# is the explicit crosswalk target, never a casefold/prefix guess.
SPECS: dict[str, dict[str, Any]] = {
    "SRC24": {
        "family": "Latinobarómetro 1995",
        "responses": [
            {
                "question_id": "p66c",
                "item_code": "p66c",
                "slots": ["p66c"],
                "topology": "BINARY_CONTRAST",
                "layout": "scalar_binary",
                "note": "Binary source-native response with exact relation.",
            },
            {
                "question_id": "p44b",
                "item_code": "p44b",
                "slots": ["p44b"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Five-category source-native ordered response.",
            },
            {
                "question_id": "p5",
                "item_code": "p5",
                "slots": ["p5"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Three-category source-native ordered response.",
            },
            {
                "question_id": "p23",
                "item_code": "p23",
                "slots": ["p23"],
                "topology": "BINARY_CONTRAST",
                "layout": "scalar_binary",
                "note": "Binary source-native response with exact relation.",
            },
        ],
        "coordinate": {
            "slot": "pais",
            "unit": "SOURCE_NATIVE_COUNTRY_CODE",
            "note": "Source-native country code; raw observation only.",
        },
        "crosswalk_mode": "EXACT_NAMES",
        "held_reason": "Accounted but outside the declared bounded LATIN native slice.",
        "fixture_rows_min": 11,
        "fixture_id": "R157-LATIN-SRC24-NONRESPONDENT",
    },
    "SRC25": {
        "family": "Latinobarómetro 2011",
        "responses": [
            {
                "question_id": "P1ST",
                "item_code": "P1ST",
                "slots": ["P1ST"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Four-category satisfaction response.",
            },
            {
                "question_id": "P3ST_A",
                "item_code": "P3ST_A",
                "slots": ["P3ST.A"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Five-category country economic situation response.",
            },
            {
                "question_id": "P29NEA",
                "item_code": "P29NEA",
                "slots": ["P29NEA"],
                "topology": "UNORDERED_MULTISELECT_SET",
                "layout": "multiselect_indicator",
                "note": "Source-native multiselect indicator (0/1).",
            },
            {
                "question_id": "P62NG",
                "item_code": "P62NG",
                "slots": ["P62NG"],
                "topology": "UNORDERED_MULTISELECT_SET",
                "layout": "multiselect_indicator",
                "note": "Source-native multiselect indicator (0/1).",
            },
        ],
        "coordinate": {
            "slot": "IDENPA",
            "unit": "SOURCE_NATIVE_COUNTRY_CODE",
            "note": "Source-native country code; raw observation only.",
        },
        "crosswalk_mode": "ORDERED_FORMAT_VARIANT",
        "held_reason": "Accounted but outside the declared bounded LATIN native slice.",
        "fixture_rows_min": 9,
        "fixture_id": "R157-LATIN-SRC25-NONRESPONDENT",
    },
    "SRC26": {
        "family": "Latinobarómetro 2024",
        "responses": [
            {
                "question_id": "Q1ST",
                "item_code": "Q1ST",
                "slots": ["P1ST"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Four-category life-satisfaction response.",
            },
            {
                "question_id": "Q29STB",
                "item_code": "Q29STB",
                "slots": ["P29ST.B"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Four-category favorability response.",
            },
            {
                "question_id": "Q14STGBSCA",
                "item_code": "Q14STGBSCA",
                "slots": ["P14STGBS.A"],
                "topology": "SCALAR",
                "layout": "scalar_ordinal",
                "note": "Four-category trust response.",
            },
            {
                "question_id": "Q23STM",
                "item_code": "Q23STM",
                "slots": ["P23STM.1", "P23STM.2", "P23STM.3"],
                "topology": "RANKED_RESPONSE",
                "layout": "ranked_three_mentions",
                "note": "Three ordered mentions of one source item; repeated observation topology preserved.",
            },
            {
                "question_id": "Q56N1",
                "item_code": "Q56N1",
                "slots": ["P56N.1"],
                "topology": "SCALAR",
                "layout": "scalar_0_10",
                "note": "Zero-to-ten leader evaluation with source-specific special codes.",
            },
        ],
        "coordinate": {
            "slot": "IDENPA",
            "unit": "SOURCE_NATIVE_COUNTRY_CODE",
            "note": "Source-native country code; raw observation only.",
        },
        "crosswalk_mode": "EXPLICIT_PQ_AND_GROUP_CROSSWALK",
        "held_reason": "Accounted but outside the declared bounded LATIN native slice.",
        "fixture_rows_min": 14,
        "fixture_id": "R157-LATIN-SRC26-NONRESPONDENT",
    },
}


def sha_material(material: Any) -> str:
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def exact_ref(kind: str, object_id: str, content_hash: str) -> dict[str, str]:
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def authority_ref(a: Mapping[str, Any]) -> dict[str, str]:
    return {
        "authority_id": a["authority_id"],
        "authority_version": a["authority_version"],
        "authority_content_hash": a["authority_content_hash"],
    }


def authority(
    source_id: str,
    source_sha: str,
    kind: str,
    state: str,
    operation: str,
    grade: str,
    *,
    families: Iterable[str],
    scope_extra: Mapping[str, Any] | None = None,
    fixture_id: str | None = None,
) -> dict[str, Any]:
    prefix = "R157"
    authority_id = f"{prefix}-{source_id}-{operation}"
    scope: dict[str, Any] = {
        "fixture_only": fixture_id is not None,
        "grade": grade,
        "source_id": source_id,
        "source_sha256": source_sha,
    }
    if fixture_id is not None:
        scope["fixture_id"] = fixture_id
        scope["original_source_sha256"] = source_sha
    else:
        scope["execution_grant"] = "NOT_ISSUED_UNDER_R157_PREPARATION"
    if scope_extra:
        scope.update(scope_extra)
    material = {
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_kind": kind,
        "decision_state": state,
        "scope_envelope": scope,
        "governed_operations": [operation],
        "governed_object_families": list(families),
    }
    content_hash = sha_material(material)
    root = exact_ref(
        "REPLAY_ROOT",
        f"urn:rawlsing:r157:authority:{source_id}:{operation}",
        sha_material({"root": material}),
    )
    return {
        "typed_state": state,
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": root,
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": content_hash,
        "authority_kind": kind,
        "decision_state": state,
        "governed_operations": [operation],
        "governed_object_families": list(families),
        "scope_envelope": scope,
        "effective_time_or_interval": "R157_NONRESPONDENT_FIXTURE" if fixture_id else "R157_PREPARATION",
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": sha_material({"scope": scope, "operation": operation}),
        "replay_protocol_ref": exact_ref(
            "REPLAY_PROTOCOL",
            f"urn:rawlsing:r157:replay:{source_id}",
            sha_material({"operation": operation, "source_id": source_id, "fixture": fixture_id}),
        ),
    }


def build_authorities(source_id: str, source_sha: str, *, fixture_id: str | None, wave: str) -> dict[str, dict[str, Any]]:
    fixture_state = "ALLOW" if fixture_id else "DEFER"
    fixture_grade = "NONRESPONDENT_FIXTURE_ONLY" if fixture_id else "SOURCE_NATIVE_REPRESENTATION_PREPARATION"
    common = {"wave": wave}
    specs = [
        ("SOURCE_SEMANTICS_TOPOLOGY", fixture_state, "R157_PREPARE_SOURCE_ITEM_SEMANTICS", fixture_grade,
         ("RespondentEvent@1.0.0",), {"semantic_scope": "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY",
                                      "direction_status": "NOT_CERTIFIED_BY_THIS_AUTHORITY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", fixture_state, "R157_PREPARE_SOURCE_TOPOLOGY", fixture_grade,
         ("RespondentEvent@1.0.0",), {"topology_scope": "EXACT_SOURCE_VALUE_LABELS_AND_H48_TOPOLOGY_ONLY", **common}),
        ("NATIVE_CANONICAL_MAPPING_HARMONIZATION", fixture_state, "R157_MAP_SOURCE_CODE_TOKEN_IDENTITY", fixture_grade,
         ("RespondentEvent@1.0.0",), {"mapping_scope": "EXACT_SOURCE_NATIVE_CODE_TOKEN_IDENTITY_ONLY_NO_SIGNED_DIRECTION", **common}),
        ("COORDINATE_SEMANTICS", fixture_state, "R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW", fixture_grade,
         ("EmpiricalCoordinateFact@1.0.0",), {"coordinate_scope": "COPY_OBSERVED_RAW_NO_CANONICAL_CROSSWALK", **common}),
        ("ROUTING_RISK_SET", fixture_state, "R157_RECORD_UNRESOLVED_SOURCE_ROUTING", fixture_grade,
         ("RoutingEligibilityFact@1.0.0",), {"routing_scope": "SOURCE_ROUTING_UNRESOLVED_NO_ELIGIBILITY_CLAIM", **common}),
        ("REPLAY_PROTOCOL", "ALLOW", "R157_LOCAL_DETERMINISTIC_REPLAY",
         "R157_DETERMINISTIC_REPLAY_PROTOCOL" if not fixture_id else "NONRESPONDENT_FIXTURE_ONLY",
         ("ReplayReceipt@1.0.0",), {"replay_scope": "R157_LOCAL_ENGINEERING_ONLY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", fixture_state, "R157_PREPARE_SOURCE_PROJECTION", fixture_grade,
         ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
          "RoutingEligibilityFact@1.0.0"), {"projection_scope": "SUPPORTED_SLICE_ONLY", **common}),
    ]
    out: dict[str, dict[str, Any]] = {}
    for kind, state, operation, grade, families, extra in specs:
        built = authority(source_id, source_sha, kind, state, operation, grade,
                          families=families, scope_extra=extra, fixture_id=fixture_id)
        out[operation] = built
    return out


def missing_declaration(slot: Mapping[str, Any]) -> Mapping[str, Any] | None:
    out: dict[str, Any] = {}
    if slot.get("missing_ranges") is not None:
        out["ranges"] = slot["missing_ranges"]
    if slot.get("missing_user_values") is not None:
        out["user_values"] = slot["missing_user_values"]
    return out or None


def normalized_name(value: str) -> str:
    return re.sub(r"[^0-9a-z]", "", value.casefold())


def stem_name(value: str) -> str:
    normalized = normalized_name(value)
    return normalized[1:] if normalized[:1] in {"p", "q"} else normalized


def response_state_for_label(label: str | None) -> str:
    text = (label or "").casefold().strip()
    for mark in ("´", "`", "’", "‘"):
        text = text.replace(mark, "'")
    if "not asked" in text:
        return "NOT_ASKED"
    if "not applicable" in text or text in {"iap", "inapplicable"}:
        return "INAPPLICABLE"
    combined_dk = any(token in text for token in ("don't know", "dont know", "does not know", "doesn´t know", "no sabe", "ns/nr"))
    combined_na = any(token in text for token in ("no answer", "does not answer", "no responde", "refus", "not answer"))
    if combined_dk and combined_na:
        return "SOURCE_SPECIFIC_SPECIAL"
    if combined_na:
        return "REFUSAL"
    if combined_dk:
        return "DK"
    if "missing" in text or "unknown" in text:
        return "MISSING"
    if text in {"none", "ninguno", "ninguna"}:
        return "SOURCE_SPECIFIC_SPECIAL"
    return "SUBSTANTIVE_RESPONSE"


def canonical_token(code: int) -> str:
    return str(int(code))


def value_rule(
    slot: Mapping[str, Any],
    code: int | None,
    label: str | None,
    *,
    topology: str,
    occurrence_key: str,
    rank: int | None,
    component_ref: Mapping[str, str] | None,
    mapping_authority: Mapping[str, str] | None,
) -> dict[str, Any]:
    if code is None:
        missing_state = "SYSTEM_MISSING"
        response_state = "MISSING"
        raw_value = None
        canonical = None
    else:
        missing_state = "OBSERVED_STORAGE_VALUE"
        response_state = response_state_for_label(label)
        raw_value = float(code)
        canonical = canonical_token(code) if response_state == "SUBSTANTIVE_RESPONSE" else None
    multiplicity: dict[str, Any]
    if topology == "RANKED_RESPONSE":
        multiplicity = {"kind": "RANKED_RESPONSE", "rank": rank, "order": rank, "max_occurrences": 3}
    elif topology == "UNORDERED_MULTISELECT_SET":
        multiplicity = {"kind": "UNORDERED_MULTISELECT_SET", "index": 0}
    elif topology == "BINARY_CONTRAST":
        multiplicity = {"kind": "BINARY_CONTRAST", "index": 0}
    else:
        multiplicity = {"kind": "SCALAR", "index": 0}
    occurrence: dict[str, Any] = {
        "key": occurrence_key,
        "topology_ref": exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:topology:{slot['source_id']}:{slot['name']}:{topology}",
            sha_material({"source": slot["source_id"], "slot": slot["name"], "topology": topology}),
        ),
        "multiplicity_order_rank_fields": multiplicity,
    }
    if component_ref is not None:
        occurrence["component_ref"] = component_ref
    return {
        "raw_value": raw_value,
        "missing_state": missing_state,
        "source_missing_declaration": None,
        "response_state": response_state,
        "occurrences": [occurrence],
        "canonical_value": canonical,
        "transform_authority_ref": mapping_authority if canonical is not None else None,
        "extra_authority_refs": [],
    }


def slot_values(
    slot: Mapping[str, Any],
    *,
    topology: str,
    occurrence_prefix: str,
    rank: int | None,
    component_ref: Mapping[str, str] | None,
    mapping_authority: Mapping[str, str] | None,
) -> list[dict[str, Any]]:
    labels = slot.get("value_labels") or {}
    codes: list[tuple[int, str]] = []
    for key, label in labels.items():
        try:
            code = int(float(key))
        except (TypeError, ValueError):
            continue
        codes.append((code, str(label)))
    codes.sort(key=lambda item: item[0])
    out = []
    for code, label in codes:
        if topology == "RANKED_RESPONSE":
            occurrence_key = f"mention_{rank}"
        else:
            occurrence_key = occurrence_prefix
        out.append(value_rule(slot, code, label, topology=topology, occurrence_key=occurrence_key,
                              rank=rank, component_ref=component_ref, mapping_authority=mapping_authority))
    if topology == "RANKED_RESPONSE":
        occurrence_key = f"mention_{rank}"
    else:
        occurrence_key = "system_missing"
    out.append(value_rule(slot, None, None, topology=topology, occurrence_key=occurrence_key,
                          rank=rank, component_ref=component_ref, mapping_authority=mapping_authority))
    return out


def physical_slot_doc(p: Mapping[str, Any], disposition: str, reason: str, crosswalk_var: str | None) -> dict[str, Any]:
    cbm = p["codebook_mapping"]
    var_name = crosswalk_var if crosswalk_var else p["name"]
    status = cbm["status"]
    if crosswalk_var and status == "PHYSICAL_ONLY":
        status = "EXPLICIT_CROSSWALK"
    return {
        "ordinal": p["ordinal"],
        "name": p["name"],
        "label": p["label"],
        "storage_type": p["readstat_type"],
        "original_type": p["original_type"],
        "storage_width": p["storage_width"],
        "measure": p["measure"],
        "value_labels": p["value_labels"],
        "missing_declarations": missing_declaration(p),
        "mr_declarations": None,
        "codebook_mapping": {
            "var_name": var_name,
            "row_hash": cbm["row_hash"],
            "status": status,
        },
        "disposition": disposition,
        "disposition_reason": reason,
    }


def item_doc(x: Mapping[str, Any]) -> dict[str, Any]:
    relation = x.get("relation") or {}
    if relation:
        rel = {
            "status": "EXACT",
            "question_id": relation["question_id"],
            "mapping_status": relation["mapping_status"] or "governed_qsmv2_relation",
            "manual_response_topology": relation["manual_response_topology"],
            "manual_response_normalization_rule": relation["manual_response_normalization_rule"],
            "manual_position_conditioning": relation["manual_position_conditioning"],
            "manual_semantic_role": relation["manual_semantic_role"],
            "manual_signed_polarity_status": relation["manual_signed_polarity_status"],
            "forbidden_inference": relation["forbidden_inference"] or "none recorded",
            "does_not_measure": relation["does_not_measure"] or "none recorded",
            "governed_row_payload_hash": relation["governed_row_payload_hash"],
            "p2_exact_identity_sha256": relation["p2_exact_identity_sha256"],
        }
        mapping_status = rel["mapping_status"]
        authority_status = relation["authority_status"]
        refs = [
            exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
            exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
            exact_ref("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{relation['question_id']}",
                      relation["governed_row_payload_hash"]),
        ]
        limits = [
            f"relation_use_status_final={relation.get('relation_use_status_final') or 'NOT_RECORDED'}",
            f"mapping_status={mapping_status}",
            f"manual_signed_polarity_status={relation['manual_signed_polarity_status']}",
            f"forbidden_inference={relation['forbidden_inference'] or 'none recorded'}",
            f"does_not_measure={relation['does_not_measure'] or 'none recorded'}",
        ]
    else:
        rel = None
        mapping_status = "UNMATCHED_EXPLICIT_ID"
        authority_status = "RELATION_ID_UNMATCHED_NOT_ADOPTED"
        refs = [
            exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
            exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
        ]
        limits = ["exact full-relation identity unmatched; preserved, not promoted"]
    doc = {
        "implementation_id": x["implementation_id"],
        "source_variable_code": x["source_variable_code"],
        "exact_identity_sha256": x["exact_identity_sha256"],
        "question_text": x["p2"]["question_text"],
        "disposition": x["h48"]["disposition"],
        "response_classes": x["p2"]["response_classes"],
        "mapping_status": mapping_status,
        "authority_status": authority_status,
        "evidence_refs": refs,
        "limits": limits,
    }
    if rel is not None:
        doc["relation"] = rel
    return doc


def make_universe(
    source_id: str,
    roster: Mapping[str, Any],
    authorities: Mapping[str, Mapping[str, Any]],
    *,
    fixture_id: str | None,
    wave: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    semantic = authority_ref(authorities["R157_PREPARE_SOURCE_ITEM_SEMANTICS"])
    if fixture_id:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED",
            "authority_snapshot_refs": [semantic],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": exact_ref(
                "REPLAY_ROOT", f"urn:rawlsing:r157:universe:{source_id}:fixture",
                sha_material({"source": source_id, "fixture": fixture_id})),
            "raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:{source_id}",
            "source_family": roster["family"],
            "study_product_release": f"R157_FIXTURE/{source_id}",
            "instrument_release": f"R157_FIXTURE_INSTRUMENT/{source_id}",
            "country_geography": "FIXTURE_MULTI_COUNTRY",
            "sampling_geography": "FIXTURE_NONPROBABILITY",
            "raw_wave": str(roster["wave"]),
            "canonical_wave_if_governed": None,
            "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
            "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
            "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
            "respondent_namespace": f"urn:rawlsing:r157:fixture:{source_id}",
            "source_artifact_import_lineage": "R157_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE",
            "harmonization_authority_ref": None,
            "source_relation_refs": [],
        }
    else:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED",
            "authority_snapshot_refs": [semantic],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": exact_ref(
                "REPLAY_ROOT", f"urn:rawlsing:r157:universe:{source_id}",
                sha_material({"source": source_id, "sha": roster["source_sha256"]})),
            "raw_source_identity": f"{roster['family']} {roster['wave']} / {source_id}",
            "source_family": roster["family"],
            "study_product_release": f"{roster['family']}:{roster['wave']}",
            "instrument_release": f"{source_id}_INSTRUMENT_{WAVE_INSTRUMENT_PREFIX}_{roster['wave']}",
            "country_geography": "SOURCE_OBSERVED_COUNTRY_CODES",
            "sampling_geography": "UNKNOWN_SOURCE_SAMPLING_GEOGRAPHY_R157_PREPARATION",
            "raw_wave": str(roster["wave"]),
            "canonical_wave_if_governed": None,
            "field_or_reference_time": str(roster["wave"]),
            "target_population_and_sample_frame": "UNKNOWN_SOURCE_SAMPLE_FRAME_R157_PREPARATION",
            "sampling_design_regime": "UNKNOWN_SOURCE_DESIGN_R157_PREPARATION",
            "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
            "source_artifact_import_lineage": f"R154_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
            "harmonization_authority_ref": None,
            "source_relation_refs": [],
        }
    universe = EmpiricalUniverse(**payload)
    return payload, universe.ref.as_dict()


def _label_key(value: Any) -> str:
    text = str(value or "").casefold().strip()
    for mark in ("´", "`", "’", "‘"):
        text = text.replace(mark, "'")
    return re.sub(r"\s+", " ", text)


def _options(text: Any) -> dict[int, str]:
    out: dict[int, str] = {}
    for part in str(text or "").split("|"):
        match = re.match(r"^\s*(-?\d+)\s*=\s*(.*)$", part.strip())
        if match:
            out[int(match.group(1))] = _label_key(match.group(2))
    return out


def entry_verification(p: Mapping[str, Any], c: Mapping[str, Any] | None, match_basis: str) -> dict[str, Any]:
    physical_values: dict[int, str] = {}
    for key, label in (p.get("value_labels") or {}).items():
        try:
            code = int(float(key))
        except (TypeError, ValueError):
            continue
        physical_values[code] = _label_key(label)
    codebook_values = _options(c.get("response_options_all")) if c else {}
    exact = sum(1 for code, label in physical_values.items() if codebook_values.get(code) == label)
    return {
        "physical_label": p.get("label"),
        "codebook_question_text": c.get("question_text") if c else None,
        "physical_labeled_codes": len(physical_values),
        "codebook_option_codes": len(codebook_values),
        "exact_code_label_matches": exact,
        "match_basis": match_basis,
    }


def build_crosswalk(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                    cb: list[Mapping[str, Any]], mode: str) -> dict[str, Any]:
    physical_entries: list[dict[str, Any]] = []
    codebook_entries: list[dict[str, Any]] = []
    if source_id == "SRC24":
        cb_by_name = {c["var_name"]: c for c in cb}
        for p in phys:
            c = cb_by_name[p["name"]]
            physical_entries.append({
                "physical_ordinal": p["ordinal"],
                "physical_name": p["name"],
                "physical_label": p["label"],
                "codebook_var_names": [c["var_name"]],
                "codebook_row_index": c["row_index"],
                "codebook_row_hash": c["row_hash"],
                "codebook_question_text": c["question_text"],
                "relation_kind": "ONE_TO_ONE",
                "match_basis": "EXACT_SOURCE_NAME_AND_ORDINAL",
                "verification": entry_verification(p, c, "EXACT_SOURCE_NAME_AND_ORDINAL"),
            })
            codebook_entries.append({
                "codebook_var_name": c["var_name"],
                "codebook_row_index": c["row_index"],
                "codebook_row_hash": c["row_hash"],
                "codebook_question_text": c["question_text"],
                "physical_names": [p["name"]],
                "relation_kind": "ONE_TO_ONE",
            })
    elif source_id == "SRC25":
        for p, c in zip(phys, cb):
            if p["ordinal"] != c["row_index"]:
                raise RuntimeError(f"SRC25 ordinal/row_index mismatch at {p['name']}")
            if normalized_name(p["name"]) != normalized_name(c["var_name"]):
                raise RuntimeError(f"SRC25 normalized name mismatch at {p['name']}")
            match = "EXACT_SOURCE_NAME" if p["name"] == c["var_name"] else "ORDERED_NAME_FORMAT_VARIANT"
            physical_entries.append({
                "physical_ordinal": p["ordinal"],
                "physical_name": p["name"],
                "physical_label": p["label"],
                "codebook_var_names": [c["var_name"]],
                "codebook_row_index": c["row_index"],
                "codebook_row_hash": c["row_hash"],
                "codebook_question_text": c["question_text"],
                "relation_kind": "ONE_TO_ONE",
                "match_basis": match,
                "verification": {
                    **entry_verification(p, c, match),
                    "ordinal_equals_codebook_row_index": True,
                    "normalized_name_equal": True,
                },
            })
            codebook_entries.append({
                "codebook_var_name": c["var_name"],
                "codebook_row_index": c["row_index"],
                "codebook_row_hash": c["row_hash"],
                "codebook_question_text": c["question_text"],
                "physical_names": [p["name"]],
                "relation_kind": "ONE_TO_ONE",
                "match_basis": match,
            })
    elif source_id == "SRC26":
        # Explicit, evidence-curated map.  The P/Q prefix and group layouts are
        # NOT inferred by the loader; every relation below is serialized here.
        overrides: dict[str, list[str]] = {
            # Physical order carries a base F28ST plus suffixes A-D; the
            # codebook names the five fields F28STA..E.  Labels bind the shift.
            "Q28STA": ["P28ST"],
            "Q28STB": ["P28ST.A"],
            "Q28STC": ["P28ST.B"],
            "Q28STD": ["P28ST.C"],
            "Q28STE": ["P28ST.D"],
            # Fourteen physical trust fields include the judiciary field F,
            # which has no current codebook row; thirteen codebook rows remain.
            "Q14STGBSCA": ["P14STGBS.A"],
            "Q14STGBSCB": ["P14STGBS.B"],
            "Q14STGBSCC": ["P14ST.C"],
            "Q14STGBSCD": ["P14ST.D"],
            "Q14STGBSCE": ["P14ST.E"],
            "Q14STGBSCG": ["P14ST.G"],
            "Q14STGBSCH": ["P14ST.H"],
            "Q14STGBSCI": ["P14ST.I"],
            "Q14STGBSCJ": ["P14ST.J"],
            "Q14STGBSCK": ["P14ST.K"],
            "Q14STGBSCL": ["P14ST.L"],
            "Q14STGBSCM": ["P14ST.M"],
            "Q14STGBSCN": ["P14ST.N"],
            # Repeated / multiple-response / component layouts.
            "Q23STM": ["P23STM.1", "P23STM.2", "P23STM.3"],
            "Q2NCV": [f"P2NCV.{i}" for i in range(1, 13)],
            "Q4NCV": [f"P4NCV.{i}" for i in range(1, 10)],
            "Q5NCV": [f"P5NCV.{i}" for i in range(1, 7)],
            "Q6NCV": [f"P6NCV.{i}" for i in range(1, 9)],
            "Q9NCV": [f"P9NCV.{i}" for i in range(1, 9)],
            "Q48ST": [f"P48ST.{i}" for i in range(1, 12)],
            "Q2NOIJ": [f"P2NOIJ.{i}" for i in range(1, 13)],
            "Q3NOIJ": [f"P3NOIJ.{i}" for i in range(1, 10)],
            "Q4NOIJ": [f"P4NOIJ.{i}" for i in range(1, 6)],
            "Q4NINT": [f"P4NINT.{i}" for i in range(1, 11)],
            "S13-Q1STINT": [f"S13P1STINT.{i}" for i in range(1, 7)],
            "S14M": [f"S14M.{i}" for i in range(1, 12)],
            # Source-edition spelling difference; labels bind the identity.
            "P6NIOJ": ["P6NOIJ"],
            "Q56N12": ["P56ST.12"],
        }
        mapping: dict[str, list[str]] = {}
        used_physical: set[str] = set()
        for codebook_name, physical_names in overrides.items():
            for name in physical_names:
                if name in used_physical:
                    raise RuntimeError(f"SRC26 physical slot assigned twice: {name}")
                used_physical.add(name)
            mapping[codebook_name] = list(physical_names)
        cb_by_name = {c["var_name"]: c for c in cb}
        physical_by_name = {p["name"]: p for p in phys}
        # Admin/context block before the first substantive physical variable.
        admin_physical = {p["name"] for p in phys if p["ordinal"] <= 28}
        # Verify every override target exists and every override codebook row exists.
        for codebook_name, physical_names in mapping.items():
            if codebook_name not in cb_by_name:
                raise RuntimeError(f"SRC26 override names absent codebook row {codebook_name}")
            for name in physical_names:
                if name not in physical_by_name:
                    raise RuntimeError(f"SRC26 override names absent physical slot {name}")
        for c in cb:
            if c["var_name"] in mapping:
                continue
            candidates = [p["name"] for p in phys
                          if p["name"] not in used_physical
                          and p["name"] not in admin_physical
                          and stem_name(p["name"]) == stem_name(c["var_name"])]
            if len(candidates) != 1:
                raise RuntimeError(
                    f"SRC26 no unique explicit correspondence for {c['var_name']}: {candidates}")
            mapping[c["var_name"]] = candidates
            used_physical.add(candidates[0])
        # All codebook rows must be mapped.
        unmapped_cb = [c["var_name"] for c in cb if c["var_name"] not in mapping]
        if unmapped_cb:
            raise RuntimeError(f"SRC26 codebook rows without physical correspondence: {unmapped_cb}")
        # Physical slots not used by a codebook row are explicitly held extras.
        extra_reasons = {
            "P14ST.F": "Physical-only judiciary trust field; no current codebook row.",
            "P52N": "Physical-only item; current codebook has no Q52N row.",
            "S17.A": "Physical date-of-birth component; codebook has only summary S17.",
            "S17.B": "Physical date-of-birth component; codebook has only summary S17.",
            "S17.C": "Physical date-of-birth component; codebook has only summary S17.",
            "REEDUC.1": "Administrative education-code component with no codebook row.",
            "REEDUC.2": "Administrative education-code component with no codebook row.",
            "REEDUC.3": "Administrative education-code component with no codebook row.",
            "REEDAD": "Administrative education age field with no codebook row.",
            "PERPART": "Administrative questionnaire participation field with no codebook row.",
            "FAMPART": "Administrative family participation field with no codebook row.",
            "WT": "Source weight slot; design/estimand authority is not established in current evidence.",
        }
        for p in phys:
            if p["ordinal"] <= 28:
                extra_reasons[p["name"]] = "Administrative/context slot; current codebook begins with substantive Q1ST."
        # Build inverse.
        inverse: dict[str, list[str]] = {name: [] for name in physical_by_name}
        for codebook_name, names in mapping.items():
            for name in names:
                inverse[name].append(codebook_name)
        for p in phys:
            names = inverse[p["name"]]
            if not names:
                reason = extra_reasons.get(p["name"], "No exact codebook counterpart in current evidence.")
                physical_entries.append({
                    "physical_ordinal": p["ordinal"],
                    "physical_name": p["name"],
                    "physical_label": p["label"],
                    "codebook_var_names": [],
                    "codebook_row_index": None,
                    "codebook_row_hash": None,
                    "codebook_question_text": None,
                    "relation_kind": "PHYSICAL_ONLY_EXTRA",
                    "match_basis": "NO_EXACT_CODEBOOK_COUNTERPART",
                    "verification": entry_verification(p, None, "NO_EXACT_CODEBOOK_COUNTERPART"),
                    "held_reason": reason,
                })
                continue
            if len(names) == 1:
                codebook_name = names[0]
                c = cb_by_name[codebook_name]
                names_for_p = mapping[codebook_name]
                if len(names_for_p) == 1:
                    relation_kind = "ONE_TO_ONE"
                elif codebook_name == "Q23STM":
                    relation_kind = "ONE_TO_MANY_RANKED_MENTIONS"
                elif codebook_name in {"S13-Q1STINT", "S14M", "Q4NINT"}:
                    relation_kind = "ONE_TO_MANY_COMPONENT"
                else:
                    relation_kind = "ONE_TO_MANY_MULTISELECT"
                match_basis = _src26_match_basis(p, c, codebook_name)
                physical_entries.append({
                    "physical_ordinal": p["ordinal"],
                    "physical_name": p["name"],
                    "physical_label": p["label"],
                    "codebook_var_names": [codebook_name],
                    "codebook_row_index": c["row_index"],
                    "codebook_row_hash": c["row_hash"],
                    "codebook_question_text": c["question_text"],
                    "relation_kind": relation_kind,
                    "match_basis": match_basis,
                    "group_physical_names": list(names_for_p),
                    "verification": entry_verification(p, c, match_basis),
                    "evidence_note": "Explicit serialized crosswalk; no dynamic normalization or P/Q alias inference.",
                })
            else:
                raise RuntimeError(f"SRC26 physical slot has multiple codebook rows: {p['name']} {names}")
        for c in cb:
            names = mapping[c["var_name"]]
            if len(names) == 1:
                relation_kind = "ONE_TO_ONE"
            elif c["var_name"] == "Q23STM":
                relation_kind = "ONE_TO_MANY_RANKED_MENTIONS"
            elif c["var_name"] in {"S13-Q1STINT", "S14M", "Q4NINT"}:
                relation_kind = "ONE_TO_MANY_COMPONENT"
            else:
                relation_kind = "ONE_TO_MANY_MULTISELECT"
            codebook_entries.append({
                "codebook_var_name": c["var_name"],
                "codebook_row_index": c["row_index"],
                "codebook_row_hash": c["row_hash"],
                "codebook_question_text": c["question_text"],
                "physical_names": list(names),
                "relation_kind": relation_kind,
            })
    else:
        raise ValueError(source_id)

    counts = {
        "physical_entries": len(physical_entries),
        "codebook_entries": len(codebook_entries),
        "one_to_one": sum(1 for e in physical_entries if e["relation_kind"] == "ONE_TO_ONE"),
        "one_to_many": sum(1 for e in physical_entries if e["relation_kind"].startswith("ONE_TO_MANY")),
        "physical_only_extra": sum(1 for e in physical_entries if e["relation_kind"] == "PHYSICAL_ONLY_EXTRA"),
        "codebook_only_unmapped": sum(1 for e in codebook_entries if not e["physical_names"]),
    }
    if counts["physical_entries"] != len(phys) or counts["codebook_entries"] != len(cb):
        raise RuntimeError("crosswalk count mismatch")
    if counts["codebook_only_unmapped"]:
        raise RuntimeError("SRC26 codebook-only entries remain unmapped")
    return {
        "schema": "PYAT_R157_SOURCE_CORRESPONDENCE@1.0.0",
        "source_id": source_id,
        "source_sha256": roster["source_sha256"],
        "physical_columns": roster["physical_columns"],
        "codebook_rows": roster["codebook_rows"],
        "method": mode,
        "entries": physical_entries,
        "codebook_entries": codebook_entries,
        "counts": counts,
        "limits": [
            "Each relation is explicit and serialized; the loader performs no casefold, punctuation, prefix or nearest-label substitution.",
            "Physical-only extras are held with exact reasons and never aliased to a codebook row.",
            "A one-to-many relation preserves repeated/multiple-response layout; it does not collapse observations.",
        ],
    }


def _src26_match_basis(p: Mapping[str, Any], c: Mapping[str, Any], codebook_name: str) -> str:
    if normalized_name(p["name"]) == normalized_name(c["var_name"]):
        return "EXACT_NAME_MODULO_SOURCE_EDITION_PREFIX_CASE_AND_PUNCTUATION"
    if codebook_name == "Q23STM":
        return "EXACT_QUESTION_TEXT_AND_EIGHT_VALUE_LABELS_WITH_THREE_RANKED_MENTIONS"
    if codebook_name in {"Q2NCV", "Q4NCV", "Q5NCV", "Q6NCV", "Q9NCV", "Q48ST", "Q2NOIJ",
                         "Q3NOIJ", "Q4NOIJ", "Q4NINT", "S13-Q1STINT", "S14M"}:
        return "EXACT_QUESTION_STEM_AND_GROUP_LAYOUT_WITH_VALUE_LABEL_CORROBORATION"
    if codebook_name in {"Q14STGBSCA", "Q14STGBSCB", "Q14STGBSCC", "Q14STGBSCD", "Q14STGBSCE",
                         "Q14STGBSCG", "Q14STGBSCH", "Q14STGBSCI", "Q14STGBSCJ", "Q14STGBSCK",
                         "Q14STGBSCL", "Q14STGBSCM", "Q14STGBSCN"}:
        return "EXACT_TRUST_GROUP_ORDER_AND_SOURCE_LABEL_CORROBORATION"
    if codebook_name.startswith("Q28ST"):
        return "EXACT_FUTURE_GROUP_ORDER_AND_SOURCE_LABEL_CORROBORATION"
    if codebook_name == "Q56N12":
        return "EXACT_PERSON_LABEL_AND_SCALE_ENDPOINTS"
    if codebook_name == "P6NIOJ":
        return "EXACT_QUESTION_TEXT_AND_SOURCE_EDITION_SPELLING_VARIANT"
    return "EXACT_QUESTION_TEXT_AND_SOURCE_LABEL_CORROBORATION"


def load_context(source_id: str) -> dict[str, Any]:
    roster = E.source_roster_entry(source_id)
    phys = list(E.iter_physical_slots(source_id))
    cb = list(E.iter_codebook_rows(source_id))
    items = list(E.iter_item_evidence(source_id))
    spec = SPECS[source_id]
    crosswalk = build_crosswalk(source_id, roster, phys, cb, spec["crosswalk_mode"])
    crosswalk_by_physical = {e["physical_name"]: e for e in crosswalk["entries"]}
    item_by_code = {x["source_variable_code"]: x for x in items}
    phys_by_name = {p["name"]: p for p in phys}
    supported_slots = {s for r in spec["responses"] for s in r["slots"]} | {spec["coordinate"]["slot"]}
    supported_items = {r["item_code"] for r in spec["responses"]}
    for name in supported_slots:
        if name not in phys_by_name:
            raise RuntimeError(f"{source_id}: supported slot absent from physical evidence: {name}")
    for code in supported_items:
        if code not in item_by_code:
            raise RuntimeError(f"{source_id}: supported item absent from item evidence: {code}")
        x = item_by_code[code]
        if not x.get("relation") or x.get("relation_join_status") != "EXACT":
            raise RuntimeError(f"{source_id}: supported item lacks exact relation: {code}")
        if x["p2"].get("response_binding_status") != "bound":
            raise RuntimeError(f"{source_id}: supported item response binding not bound: {code}")
    for entry in crosswalk["entries"]:
        entry["selected_for_supported_slice"] = entry["physical_name"] in supported_slots
    crosswalk["counts"]["selected_for_supported_slice"] = sum(
        1 for entry in crosswalk["entries"] if entry["selected_for_supported_slice"])
    return {
        "source_id": source_id,
        "roster": roster,
        "phys": phys,
        "cb": cb,
        "items": items,
        "spec": spec,
        "crosswalk": crosswalk,
        "crosswalk_by_physical": crosswalk_by_physical,
        "item_by_code": item_by_code,
        "phys_by_name": phys_by_name,
        "supported_slots": supported_slots,
        "supported_items": supported_items,
    }


def build_config(ctx: Mapping[str, Any], *, mode: str, fixture_meta: Mapping[str, Any] | None,
                 crosswalk_sha: str) -> dict[str, Any]:
    source_id = ctx["source_id"]
    roster = ctx["roster"]
    spec = ctx["spec"]
    phys = ctx["phys"]
    items = ctx["items"]
    crosswalk = ctx["crosswalk"]
    crosswalk_by_physical = ctx["crosswalk_by_physical"]
    item_by_code = ctx["item_by_code"]
    phys_by_name = ctx["phys_by_name"]
    supported_slots = ctx["supported_slots"]
    supported_items = ctx["supported_items"]
    source_sha = roster["source_sha256"]
    wave = str(roster["wave"])
    fixture_id = fixture_meta["fixture_id"] if fixture_meta else None
    auths = build_authorities(source_id, source_sha, fixture_id=fixture_id, wave=wave)
    aref = {name: authority_ref(a) for name, a in auths.items()}
    universe_payload, universe_ref = make_universe(
        source_id, roster, auths, fixture_id=fixture_id, wave=wave)

    if mode == "original":
        identity_class = "ORIGINAL_SOURCE"
        binding_sha = source_sha
        binding_rows = roster["rows"]
    else:
        assert fixture_meta is not None
        identity_class = "NONRESPONDENT_FIXTURE"
        binding_sha = fixture_meta["fixture_source_sha256"]
        binding_rows = fixture_meta["row_count"]

    # Supported physical slots: response slots + coordinate.
    supported_physical_docs = []
    for name in sorted(supported_slots, key=lambda n: phys_by_name[n]["ordinal"]):
        p = phys_by_name[name]
        if name == spec["coordinate"]["slot"]:
            disposition = "SUPPORTED_COORDINATE"
            reason = spec["coordinate"]["note"]
        else:
            response_spec = next(r for r in spec["responses"] if name in r["slots"])
            disposition = "SUPPORTED_RESPONSE"
            reason = response_spec["note"]
        entry = crosswalk_by_physical[name]
        crosswalk_var = entry["codebook_var_names"][0] if entry["codebook_var_names"] else None
        supported_physical_docs.append(physical_slot_doc(p, disposition, reason, crosswalk_var))

    if mode == "original":
        physical_docs = []
        for p in phys:
            if p["name"] in supported_slots:
                continue
            entry = crosswalk_by_physical[p["name"]]
            if entry["relation_kind"] == "PHYSICAL_ONLY_EXTRA":
                disposition = "HELD_PHYSICAL_ONLY_EXTRA"
                reason = entry.get("held_reason") or "Physical-only slot with no exact codebook counterpart."
            else:
                disposition = "EXCLUDED_PREPARATION_SLICE"
                reason = spec["held_reason"]
            crosswalk_var = entry["codebook_var_names"][0] if entry["codebook_var_names"] else None
            physical_docs.append(physical_slot_doc(p, disposition, reason, crosswalk_var))
        physical_docs.extend(supported_physical_docs)
        physical_docs.sort(key=lambda d: d["ordinal"])
    else:
        physical_docs = supported_physical_docs

    # Items.
    supported_item_docs = []
    for code in sorted(supported_items):
        x = item_by_code[code]
        doc = item_doc(x)
        response_spec = next(r for r in spec["responses"] if r["item_code"] == code)
        doc["disposition"] = f"SUPPORTED_{response_spec['layout'].upper()}"
        doc["limits"] = list(doc["limits"]) + [response_spec["note"]]
        supported_item_docs.append(doc)
    if mode == "original":
        item_docs = []
        supported_ids = {d["implementation_id"] for d in supported_item_docs}
        for x in items:
            if x["implementation_id"] in supported_ids:
                continue
            doc = item_doc(x)
            if doc["mapping_status"] == "UNMATCHED_EXPLICIT_ID":
                doc["disposition"] = "HELD_UNMATCHED_RELATION"
                doc["limits"] = list(doc["limits"]) + ["Held; exact relation identity is unmatched."]
            elif x["p2"].get("response_binding_status") != "bound":
                doc["disposition"] = "HELD_RESPONSE_AUTHORITY_GAP"
                doc["limits"] = list(doc["limits"]) + ["Held; prior response binding is blocked."]
            elif x["h48"].get("disposition") in {"admin", "position_context", "structural_context"}:
                doc["disposition"] = "EXCLUDED_CONTEXT_OR_ADMIN"
                doc["limits"] = list(doc["limits"]) + ["Accounted context/admin item outside the declared response slice."]
            else:
                doc["disposition"] = "EXCLUDED_PREPARATION_SLICE"
                doc["limits"] = list(doc["limits"]) + [spec["held_reason"]]
            item_docs.append(doc)
        item_docs.extend(supported_item_docs)
        item_docs.sort(key=lambda d: d["implementation_id"])
    else:
        item_docs = supported_item_docs

    # Questions.
    questions = []
    for response_spec in spec["responses"]:
        x = item_by_code[response_spec["item_code"]]
        questions.append({
            "question_id": response_spec["question_id"],
            "empirical_universe_ref": universe_ref,
            "native_question_ref": exact_ref(
                "NATIVE_QUESTION",
                f"urn:rawlsing:r157:{mode}:{source_id}:item:{x['implementation_id']}",
                x["exact_identity_sha256"]),
            "instrument_question_version": wave,
            "canonical_question_ref_or_typed_absence": {
                "typed_absence_state": "NOT_AUTHORIZED",
                "detail": "No canonical adoption or directional certification is issued by this source preparation.",
            },
            "component_subitem_ref_or_typed_absence": {
                "typed_absence_state": "NOT_APPLICABLE",
                "detail": None,
            },
            "semantic_authority_ref": aref["R157_PREPARE_SOURCE_ITEM_SEMANTICS"],
            "topology_authority_ref": aref["R157_PREPARE_SOURCE_TOPOLOGY"],
            "item_evidence": {
                "implementation_id": x["implementation_id"],
                "exact_identity_sha256": x["exact_identity_sha256"],
                "relation_join_status": x.get("relation_join_status"),
            },
        })

    # Response slots.
    response_slots = []
    for response_spec in spec["responses"]:
        slots = response_spec["slots"]
        for index, slot_name in enumerate(slots):
            p = phys_by_name[slot_name]
            rank = index + 1 if response_spec["layout"] == "ranked_three_mentions" else None
            if response_spec["layout"] == "ranked_three_mentions":
                component_ref = exact_ref(
                    "COMPONENT_SUBITEM",
                    f"urn:rawlsing:r157:{mode}:{source_id}:{slot_name}",
                    sha_material({"source": source_id, "slot": slot_name, "rank": rank}),
                )
                occurrence_prefix = f"mention_{rank}"
            else:
                component_ref = None
                occurrence_prefix = "indicator" if response_spec["layout"] == "multiselect_indicator" else "0"
            response_slots.append({
                "slot": {"ordinal": p["ordinal"], "name": p["name"]},
                "question_id": response_spec["question_id"],
                "values": slot_values(
                    p,
                    topology=response_spec["topology"],
                    occurrence_prefix=occurrence_prefix,
                    rank=rank if rank is not None else None,
                    component_ref=component_ref,
                    mapping_authority=aref["R157_MAP_SOURCE_CODE_TOKEN_IDENTITY"],
                ),
            })

    # Coordinate slot.
    coord_spec = spec["coordinate"]
    coord_p = phys_by_name[coord_spec["slot"]]
    coordinate_slots = [{
        "slot": {"ordinal": coord_p["ordinal"], "name": coord_p["name"]},
        "native_coordinate_ref": exact_ref(
            "COORDINATE_NATIVE",
            f"urn:rawlsing:r157:{mode}:{source_id}:{coord_p['name']}",
            sha_material({"source": source_id, "slot": coord_p["name"], "mode": mode})),
        "unit_taxonomy_ref": exact_ref(
            "UNIT_TAXONOMY",
            f"urn:rawlsing:r157:{coord_spec['unit']}",
            sha_material({"unit": coord_spec["unit"]})),
        "effective_time": wave,
        "source_semantic_authority_ref": aref["R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW"],
        "canonical_coordinate_ref": None,
        "normalization_ref": None,
        "values": [],
        "copy_observed_raw": True,
    }]

    # Routing: source evidence is unresolved for every supported item; represent
    # that exact state rather than inventing administration or eligibility.
    routing = []
    for response_spec in spec["responses"]:
        qid = response_spec["question_id"]
        routing.append({
            "question_id": qid,
            "row_selector": "ALL",
            "typed_state": "ROUTING_UNKNOWN",
            "risk_set_ref": exact_ref(
                "RISK_SET", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                sha_material({"source": source_id, "q": qid, "mode": mode, "r": "risk"})),
            "routing_rule_ref": exact_ref(
                "ROUTING_RULE", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                sha_material({"source": source_id, "q": qid, "mode": mode, "r": "rule"})),
            "member_set_replay_ref": exact_ref(
                "MEMBER_SET_REPLAY", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                sha_material({"source": source_id, "q": qid, "mode": mode, "r": "member"})),
            "authority_ref": aref["R157_RECORD_UNRESOLVED_SOURCE_ROUTING"],
            "parent_predicate_refs": [],
            "dependency_refs": [],
        })

    # Coverage.
    supported_ordinals = sorted(d["ordinal"] for d in supported_physical_docs)
    if mode == "original":
        included_set = set(supported_ordinals)
        excluded_slots = [
            {"ordinal": p["ordinal"], "name": p["name"], "reason": spec["held_reason"]}
            for p in phys if p["ordinal"] not in included_set
        ]
        included_ids = {d["implementation_id"] for d in supported_item_docs}
        item_reasons = {}
        for d in item_docs:
            if d["implementation_id"] in included_ids:
                continue
            if d["disposition"] == "HELD_UNMATCHED_RELATION":
                item_reasons[d["implementation_id"]] = "Exact full-relation identity unmatched; held not promoted."
            elif d["disposition"] == "HELD_RESPONSE_AUTHORITY_GAP":
                item_reasons[d["implementation_id"]] = "Prior response binding blocked; held."
            elif d["disposition"] == "EXCLUDED_CONTEXT_OR_ADMIN":
                item_reasons[d["implementation_id"]] = "Context/admin item accounted outside the response slice."
            else:
                item_reasons[d["implementation_id"]] = spec["held_reason"]
        excluded_items = [
            {"implementation_id": i["implementation_id"], "reason": item_reasons[i["implementation_id"]]}
            for i in items if i["implementation_id"] not in included_ids
        ]
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": supported_ordinals,
            "physical_slots_excluded": excluded_slots,
            "items_included": [d["implementation_id"] for d in supported_item_docs],
            "items_excluded": excluded_items,
            "partial_scope_reason": (
                "Bounded LATIN lane native slice. All remaining physical slots and original items are "
                "individually accounted as excluded/held; no alias or invented semantics is used."),
        }
    else:
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "partial_scope_reason": (
                "Nonrespondent fixture slice only; original source coverage is declared in the "
                "separate ORIGINAL_SOURCE preparation config."),
            "not_a_lane_config": True,
        }

    # Supported scope.
    supported_question_ids = [r["question_id"] for r in spec["responses"]]
    if mode == "original":
        supported_scope = {
            "scope_id": f"{source_id}-R157-SOURCE-NATIVE-SLICE",
            "purpose": "SOURCE_PREPARATION",
            "declared_supported": True,
            "supported_question_ids": supported_question_ids,
            "native_validation_expectation": "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "SOURCE_INTERVIEW_ROW",
            "supported_form_slice": "SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE",
            "notes": [
                "This is a portable source-grounded recipe. Original-source execution was not performed.",
                "Positive native C11 construction is separately exercised by the nonrespondent fixture config.",
                "Source routing remains SOURCE_ROUTING_UNRESOLVED and is represented as ROUTING_UNKNOWN.",
            ],
        }
    else:
        supported_scope = {
            "scope_id": f"{source_id}-R157-NONRESPONDENT-FIXTURE-SLICE",
            "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
            "declared_supported": True,
            "supported_question_ids": supported_question_ids,
            "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS",
            "supported_form_slice": "NONRESPONDENT_FIXTURE_SLICE",
            "notes": [
                "Fixture-only authority; never original-source authority.",
                "The fixture bytes are a distinct identity and do not reuse the original source SHA.",
            ],
        }

    # Residuals.
    if mode == "original":
        residuals = build_original_residuals(ctx, supported_question_ids)
    else:
        residuals = [{
            "residual_id": f"{source_id}-FIXTURE-ONLY-AUTHORITY",
            "scope": source_id,
            "field": "authority.snapshots",
            "status": "FIXTURE_ONLY",
            "reason": "The fixture proves native construction but does not establish original-source authority.",
            "dependent_operation": "original-source execution and scientific interpretation",
            "unaffected_scope": "nonrespondent fixture native C11 validation",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Keep fixture authority separate from the ORIGINAL_SOURCE config and any future issued workload.",
        }]

    metadata_ref = exact_ref(
        "R154_PHYSICAL_METADATA",
        f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
        roster["metadata_witness"]["sha256"])
    supported_item_refs = []
    for response_spec in spec["responses"]:
        x = item_by_code[response_spec["item_code"]]
        supported_item_refs.append(exact_ref(
            "H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]))
        supported_item_refs.append(exact_ref(
            "P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]))
        if x.get("relation"):
            supported_item_refs.append(exact_ref(
                "FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{x['relation']['question_id']}",
                x["relation"]["governed_row_payload_hash"]))
    field_evidence = [
        {"field": "identity.expected_source_sha256", "refs": [
            exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)]},
        {"field": "identity.metadata_witness_ref", "refs": [metadata_ref]},
        {"field": "physical_slots", "refs": [metadata_ref]},
        {"field": "correspondence", "refs": [exact_ref(
            "SOURCE_CORRESPONDENCE", f"rawlsing_next/source_configuration/data/{source_id}/crosswalk.json",
            crosswalk_sha)]},
        {"field": "items.supported", "refs": supported_item_refs},
    ]
    evidence = {
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
        "field_evidence": field_evidence,
        "limits": [
            "Prior H48/P2/full-relation evidence is reused with its original grades and limits.",
            "No original respondent rows, original response values or original source bytes were read.",
            "Fixture authority is not original-source authority.",
        ],
    }

    authority_section = {
        "snapshots": [auths[k] for k in sorted(auths)],
        "required_refs": [aref[k] for k in sorted(aref)],
        "projection_authority_ref": aref["R157_PREPARE_SOURCE_PROJECTION"],
        "replay_authority_ref": aref["R157_LOCAL_DETERMINISTIC_REPLAY"],
        "projection_identity_ref": exact_ref(
            "C11_SEMANTIC_PROJECTION",
            f"urn:rawlsing:r157:{mode}:{source_id}:projection",
            sha_material({"source": source_id, "sha": source_sha, "mode": mode,
                          "questions": supported_question_ids})),
        "tie_order_ref": exact_ref(
            "ORDER_RULE", "urn:rawlsing:r157:canonical-ref-sort",
            sha_material({"rule": "canonical_ref_sort"})),
        "replay_protocol_version": "1.0.0",
    }

    identity = {
        "source_id": source_id,
        "family": roster["family"],
        "wave": wave,
        "source_family_id": roster["family"],
        "study_product_id": f"{roster['family']}:{wave}",
        "release_id": f"{source_id}_{WAVE_INSTRUMENT_PREFIX}_{wave}_PREPARATION",
        "instrument_release_id": f"{source_id}_INSTRUMENT_{WAVE_INSTRUMENT_PREFIX}_{wave}",
        "source_artifact_id": roster["source_artifact_id"],
        "expected_source_sha256": source_sha,
        "source_format": roster["format"],
        "source_row_count": roster["rows"],
        "source_column_count": roster["physical_columns"],
        "source_bytes": roster["bytes"],
        "codebook_rows": roster["codebook_rows"],
        "original_item_count": roster["original_items"],
        "source_snapshot_retention_ref": exact_ref(
            "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
        "metadata_witness_ref": metadata_ref,
        "locator": {"root": "EXTERNAL_LOCATOR_ID",
                    "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
        "reader": {
            "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
            "configuration_ref": exact_ref(
                "READER_CONFIGURATION", f"urn:rawlsing:r157:{source_id}:default_sav",
                sha_material({"source": source_id, "sha": source_sha, "reader": "default_sav"})),
            "encoding": None,
        },
    }

    if mode == "original":
        binding = {
            "identity_class": identity_class,
            "source_sha256": binding_sha,
            "row_count": binding_rows,
            "source_snapshot_ref": exact_ref(
                "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
        }
        respondents = {
            "subject_unit": "SOURCE_INTERVIEW_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
            "respondent_key_pattern": f"{source_id}-ROW-{{row_ordinal:05d}}",
            "source_native_key_slot": None,
            "identity_map_authority_ref": None,
            "row_identity_grade": "SOURCE_PHYSICAL_ROW_ORDINAL_ONLY",
        }
        config_id = f"R157-LATIN-{source_id}-SOURCE-PREPARATION"
        purpose = "SOURCE_PREPARATION"
    else:
        assert fixture_meta is not None
        binding = {
            "identity_class": identity_class,
            "source_sha256": binding_sha,
            "row_count": binding_rows,
            "source_snapshot_ref": exact_ref(
                "FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:fixture:{fixture_meta['fixture_id']}", binding_sha),
            "fixture_provenance": {
                "fixture_id": fixture_meta["fixture_id"],
                "provenance": fixture_meta["provenance"],
                "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                "original_source_id": source_id,
                "original_source_sha256": source_sha,
                "no_original_respondents": True,
                "fixture_study_product_id": fixture_meta["fixture_study_product_id"],
                "fixture_release_id": fixture_meta["fixture_release_id"],
                "fixture_instrument_release_id": fixture_meta["fixture_instrument_release_id"],
            },
        }
        respondents = {
            "subject_unit": "NONRESPONDENT_FIXTURE_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:fixture:{source_id}",
            "respondent_key_pattern": f"FIXTURE-{source_id}-ROW-{{row_ordinal:03d}}",
            "source_native_key_slot": None,
            "identity_map_authority_ref": None,
            "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY",
        }
        config_id = f"R157-LATIN-{source_id}-NONRESPONDENT-FIXTURE"
        purpose = "NONRESPONDENT_FIXTURE"

    return {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id,
        "config_revision": 1,
        "config_purpose": purpose,
        "identity": identity,
        "binding": binding,
        "authority": authority_section,
        "universe": {"universes": [universe_payload]},
        "respondents": respondents,
        "questions": questions,
        "physical_slots": physical_docs,
        "items": item_docs,
        "response_slots": response_slots,
        "coordinate_slots": coordinate_slots,
        "weight_slots": [],
        "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
            "comparator": {"typed_absence_state": "DEFERRED", "detail": None},
            "discovery": {"typed_absence_state": "DEFERRED", "detail": None},
            "structural": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
        },
        "supported_scope": supported_scope,
        "coverage": coverage,
        "residuals": residuals,
        "evidence": evidence,
        "runtime": {
            "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
            "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
            "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
            "reader_encoding_transport": "P3_INTEGRATION_OWNER_QUALIFIED_READER_TRANSPORT",
        },
    }


def build_original_residuals(ctx: Mapping[str, Any], supported_question_ids: list[str]) -> list[dict[str, str]]:
    source_id = ctx["source_id"]
    spec = ctx["spec"]
    items = ctx["items"]
    crosswalk = ctx["crosswalk"]
    unmatched = [x["implementation_id"] for x in items
                 if x.get("relation_join_status") == "UNMATCHED_EXPLICIT_ID"]
    extras = [e for e in crosswalk["entries"] if e["relation_kind"] == "PHYSICAL_ONLY_EXTRA"]
    residuals: list[dict[str, str]] = [
        {
            "residual_id": f"{source_id}-ROUTING-UNRESOLVED",
            "scope": f"{source_id}/{','.join(supported_question_ids)}",
            "field": "routing.typed_state",
            "status": "UNKNOWN",
            "reason": "Prior H48/P2 evidence records SOURCE_ROUTING_UNRESOLVED for these items; no form or risk-set expression is present in current evidence.",
            "dependent_operation": "eligibility-conditioned or form-conditioned native query",
            "unaffected_scope": "raw source-native response incidence for the declared slice",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Recover the exact indexed source routing/form expression before widening the supported scope.",
        },
        {
            "residual_id": f"{source_id}-ROW-NATIVE-KEY",
            "scope": source_id,
            "field": "respondents.source_native_key_slot",
            "status": "UNKNOWN",
            "reason": "No exact decoded source-native respondent key witness exists in preparation; row ordinal is the only established key.",
            "dependent_operation": "respondent-key linkage or deduplication beyond physical row ordinal",
            "unaffected_scope": "row-ordinal-scoped source-native response construction",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Supply exact row_native_keys only after a separately permitted decode; the corrected P0 factory refuses otherwise.",
        },
        {
            "residual_id": f"{source_id}-FORM-ADMIN",
            "scope": source_id,
            "field": "supported_scope.supported_form_slice",
            "status": "UNKNOWN",
            "reason": "Current physical/codebook evidence contains no form, ballot or administration variable; single-file SAV shape is all that is established.",
            "dependent_operation": "form-conditioned or administration-conditioned native query",
            "unaffected_scope": "source-native response incidence without form conditioning",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Acquire exact source form/administration evidence before claiming a form-conditioned slice.",
        },
        {
            "residual_id": f"{source_id}-WEIGHT-AUTHORITY",
            "scope": source_id,
            "field": "weight_slots",
            "status": "NOT_DECLARED",
            "reason": "The source file carries a weight slot, but no exact design/estimand authority or weighted scope is present in current evidence.",
            "dependent_operation": "population or weighted estimation",
            "unaffected_scope": "raw-sample source-native response incidence",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Establish exact weight basis, design, estimand and effective scope before declaring a weighted slice.",
        },
        {
            "residual_id": f"{source_id}-DIRECTION",
            "scope": f"{source_id}/{','.join(supported_question_ids)}",
            "field": "items.relation.manual_signed_polarity_status",
            "status": "NOT_CERTIFIED_BY_THIS_PREPARATION",
            "reason": "Response states and exact source code tokens are bound, but this preparation does not issue a new signed-direction or canonical semantic certification.",
            "dependent_operation": "signed-direction empirical or structural analysis",
            "unaffected_scope": "source-native nominal/ordinal response incidence and exact value accounting",
            "owner": "LATIN lane / later scientific authority owner",
            "next_step": "Use the original relation certification only at its exact evidenced scope; do not infer direction from this config.",
        },
        {
            "residual_id": f"{source_id}-ORIGINAL-EXECUTION",
            "scope": source_id,
            "field": "supported_scope.original_source_execution",
            "status": "NOT_PERFORMED",
            "reason": "Original respondent execution and original workload issuance are a separate permission boundary.",
            "dependent_operation": "original empirical execution",
            "unaffected_scope": "portable configuration and nonrespondent fixture native validation",
            "owner": "user-authorized execution owner",
            "next_step": "Issue a separate exact original-source execution grant and qualified reader binding.",
        },
    ]
    if unmatched:
        residuals.append({
            "residual_id": f"{source_id}-UNMATCHED-RELATION-IDS",
            "scope": source_id,
            "field": "items.relation",
            "status": "HELD",
            "reason": f"{len(unmatched)} exact implementation IDs have no full-relation row: {', '.join(unmatched)}.",
            "dependent_operation": "relation-scoped semantic use of the unmatched items",
            "unaffected_scope": "matched items and the declared supported slice",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Preserve the exact unmatched IDs; do not substitute a last row, casefold alias or nearest relation.",
        })
    if extras:
        residuals.append({
            "residual_id": f"{source_id}-PHYSICAL-ONLY-EXTRA",
            "scope": source_id,
            "field": "physical_slots.codebook_mapping",
            "status": "HELD_UNMAPPED",
            "reason": f"{len(extras)} physical-only slots have no exact current codebook counterpart: {', '.join(e['physical_name'] for e in extras)}.",
            "dependent_operation": "codebook-linked semantic use of those physical slots",
            "unaffected_scope": "the explicit crosswalk and the declared supported slice",
            "owner": "LATIN lane / P3 integration owner",
            "next_step": "Preserve these slots as physical-only; acquire exact edition evidence before any alias.",
        })
    return residuals


def fixture_sequences(ctx: Mapping[str, Any]) -> dict[str, list[int | None]]:
    source_id = ctx["source_id"]
    spec = ctx["spec"]
    phys_by_name = ctx["phys_by_name"]
    sequences: dict[str, list[int | None]] = {}
    for response_spec in spec["responses"]:
        for index, slot_name in enumerate(response_spec["slots"]):
            p = phys_by_name[slot_name]
            labels = p.get("value_labels") or {}
            codes: list[tuple[int, str]] = []
            for key, label in labels.items():
                try:
                    code = int(float(key))
                except (TypeError, ValueError):
                    continue
                codes.append((code, str(label)))
            codes.sort()
            substantive = [code for code, label in codes
                           if response_state_for_label(label) == "SUBSTANTIVE_RESPONSE"]
            specials = [code for code, label in codes
                        if response_state_for_label(label) != "SUBSTANTIVE_RESPONSE"]
            sequence: list[int | None] = substantive + specials + [None]
            if response_spec["layout"] == "ranked_three_mentions":
                shift = index % max(len(sequence), 1)
                sequence = sequence[shift:] + sequence[:shift]
            sequences[slot_name] = sequence
    return sequences


def build_fixture(ctx: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_id = ctx["source_id"]
    spec = ctx["spec"]
    phys_by_name = ctx["phys_by_name"]
    sequences = fixture_sequences(ctx)
    rows = max([spec["fixture_rows_min"]] + [len(s) for s in sequences.values()])
    coord_name = spec["coordinate"]["slot"]
    coord_slot = phys_by_name[coord_name]
    country_codes = []
    for key, label in (coord_slot.get("value_labels") or {}).items():
        try:
            code = int(float(key))
        except (TypeError, ValueError):
            continue
        if code > 0:
            country_codes.append(code)
    country_codes.sort()
    if not country_codes:
        raise RuntimeError(f"{source_id}: no positive country codes")
    cells = []
    oracle_slots: dict[str, dict[str, list[Any]]] = {}
    for response_spec in spec["responses"]:
        for slot_name in response_spec["slots"]:
            oracle_slots[slot_name] = {"states": [], "raw_values": [], "canonical_values": []}
    for row in range(1, rows + 1):
        for response_spec in spec["responses"]:
            for slot_name in response_spec["slots"]:
                p = phys_by_name[slot_name]
                sequence = sequences[slot_name]
                code = sequence[(row - 1) % len(sequence)]
                label = None
                if code is not None:
                    label = (p.get("value_labels") or {}).get(str(float(code)))
                    if label is None:
                        # fall back to string key from integer code
                        label = (p.get("value_labels") or {}).get(str(code))
                state = "MISSING" if code is None else response_state_for_label(label)
                canonical = canonical_token(code) if state == "SUBSTANTIVE_RESPONSE" else None
                cells.append({
                    "row_ordinal": row,
                    "variable_ordinal": p["ordinal"],
                    "variable_name": p["name"],
                    "raw_value": None if code is None else float(code),
                    "missing_state": "SYSTEM_MISSING" if code is None else "OBSERVED_STORAGE_VALUE",
                    "source_missing_declaration": None,
                })
                oracle_slots[slot_name]["states"].append(state)
                oracle_slots[slot_name]["raw_values"].append(None if code is None else float(code))
                oracle_slots[slot_name]["canonical_values"].append(canonical)
        code = country_codes[(row - 1) % len(country_codes)]
        cells.append({
            "row_ordinal": row,
            "variable_ordinal": coord_slot["ordinal"],
            "variable_name": coord_slot["name"],
            "raw_value": float(code),
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
        })
    fixture_id = spec["fixture_id"]
    document = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
        "fixture_id": fixture_id,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "row_count": rows,
        "cells": cells,
    }
    from rawlsing_next.source_configuration.fixture import fixture_document_sha256
    fixture_sha = fixture_document_sha256(document)
    document["fixture_source_sha256"] = fixture_sha
    state_counts: dict[str, int] = {}
    for slot_data in oracle_slots.values():
        for state in slot_data["states"]:
            state_counts[state] = state_counts.get(state, 0) + 1
    oracle = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_ORACLE@1.0.0",
        "fixture_id": fixture_id,
        "fixture_source_sha256": fixture_sha,
        "row_count": rows,
        "expected": {
            "response_event_count": rows * sum(len(r["slots"]) for r in spec["responses"]),
            "coordinate_fact_count": rows,
            "routing_fact_count": rows * len(spec["responses"]),
            "response_states_by_slot": {k: v["states"] for k, v in oracle_slots.items()},
            "raw_values_by_slot": {k: v["raw_values"] for k, v in oracle_slots.items()},
            "canonical_values_by_slot": {k: v["canonical_values"] for k, v in oracle_slots.items()},
            "response_state_counts": state_counts,
            "weight_section": "NOT_APPLICABLE",
            "source_relation_section": "DISTINCT_BY_DEFAULT",
        },
        "oracle_basis": (
            "Declared from the fixture cells and the serialized source-native value rules "
            "before the factory/native-validator call; not copied from the native result."),
    }
    return document, oracle


def write_json(path: Path, value: Any) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest(), len(raw)


def build_field_evidence(ctx: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    source_id = ctx["source_id"]
    roster = ctx["roster"]
    crosswalk = ctx["crosswalk"]
    metadata_ref = exact_ref(
        "R154_PHYSICAL_METADATA",
        f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
        roster["metadata_witness"]["sha256"])
    included_slots = set(config["coverage"].get("physical_slots_included", []))
    included_items = set(config["coverage"].get("items_included", []))
    entries = []
    for p in ctx["phys"]:
        ce = ctx["crosswalk_by_physical"][p["name"]]
        refs = [metadata_ref]
        if ce["codebook_row_hash"]:
            refs.append(exact_ref(
                "CODEBOOK_ROW", f"urn:rawlsing:r157:codebook:{source_id}:{ce['codebook_var_names'][0]}",
                ce["codebook_row_hash"]))
        entries.append({
            "field": f"physical_slots[{p['ordinal']}]",
            "physical_name": p["name"],
            "codebook_var_names": ce["codebook_var_names"],
            "included": p["ordinal"] in included_slots,
            "refs": refs,
        })
    for x in ctx["items"]:
        refs = [
            exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
            exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
        ]
        if x.get("relation"):
            refs.append(exact_ref(
                "FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{x['relation']['question_id']}",
                x["relation"]["governed_row_payload_hash"]))
        entries.append({
            "field": f"items[{x['implementation_id']}]",
            "source_variable_code": x["source_variable_code"],
            "included": x["implementation_id"] in included_items,
            "relation_join_status": x.get("relation_join_status"),
            "refs": refs,
        })
    return {
        "schema": "PYAT_R157_SOURCE_FIELD_EVIDENCE@1.0.0",
        "source_id": source_id,
        "config_id": config["config_id"],
        "physical_slot_entries": len(ctx["phys"]),
        "item_entries": len(ctx["items"]),
        "included_slots": sorted(included_slots),
        "included_items": sorted(included_items),
        "entries": entries,
        "crosswalk_sha256": ctx["crosswalk_sha256"],
        "limits": [
            "Every physical slot and original item is represented once.",
            "Included/excluded status is the config's declared preparation slice, not a deletion.",
        ],
    }


def main() -> int:
    from rawlsing_next.source_configuration.schema import (
        canonical_config_hash,
        validate_source_config,
    )
    written = []
    for source_id in SOURCE_IDS:
        ctx = load_context(source_id)
        data_dir = DATA_ROOT / source_id
        val_dir = VAL_ROOT / source_id
        data_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        crosswalk_sha, crosswalk_bytes = write_json(data_dir / "crosswalk.json", ctx["crosswalk"])
        ctx["crosswalk_sha256"] = crosswalk_sha
        original = build_config(ctx, mode="original", fixture_meta=None, crosswalk_sha=crosswalk_sha)
        validate_source_config(original)
        fixture_doc, oracle = build_fixture(ctx)
        fixture_meta = {
            "fixture_id": spec_id(ctx),
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "row_count": fixture_doc["row_count"],
            "provenance": (
                "Repository-generated nonrespondent fixture for the R157 LATIN lane; "
                "no original respondents are represented."),
            "fixture_study_product_id": f"R157_FIXTURE/{source_id}",
            "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
            "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
        }
        fixture_config = build_config(ctx, mode="fixture", fixture_meta=fixture_meta,
                                      crosswalk_sha=crosswalk_sha)
        validate_source_config(fixture_config)
        field_evidence = build_field_evidence(ctx, original)
        artifacts = []
        artifacts.append(("rawlsing_next/source_configuration/data/"
                          f"{source_id}/crosswalk.json", crosswalk_sha, crosswalk_bytes))
        for rel, value in (
            (f"rawlsing_next/source_configuration/data/{source_id}/source.config.json", original),
            (f"rawlsing_next/source_configuration/data/{source_id}/field_evidence.json", field_evidence),
            (f"source_pre553_validation/{source_id}/fixture.json", fixture_doc),
            (f"source_pre553_validation/{source_id}/fixture.config.json", fixture_config),
            (f"source_pre553_validation/{source_id}/fixture_oracle.json", oracle),
        ):
            digest, size = write_json(ROOT / rel, value)
            artifacts.append((rel, digest, size))
        manifest = {
            "schema": "PYAT_R157_LATIN_SOURCE_MANIFEST@1.0.0",
            "source_id": source_id,
            "family": ctx["roster"]["family"],
            "wave": str(ctx["roster"]["wave"]),
            "source_sha256": ctx["roster"]["source_sha256"],
            "config_sha256": canonical_config_hash(original),
            "fixture_config_sha256": canonical_config_hash(fixture_config),
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "counts": {
                "physical_slots": ctx["roster"]["physical_columns"],
                "original_items": ctx["roster"]["original_items"],
                "included_slots": len(original["coverage"]["physical_slots_included"]),
                "included_items": len(original["coverage"]["items_included"]),
                "crosswalk_physical_entries": ctx["crosswalk"]["counts"]["physical_entries"],
                "crosswalk_codebook_entries": ctx["crosswalk"]["counts"]["codebook_entries"],
            },
            "artifacts": [
                {"path": path, "sha256": digest, "bytes": size} for path, digest, size in artifacts
            ],
        }
        digest, size = write_json(val_dir / "manifest.json", manifest)
        written.append((source_id, canonical_config_hash(original), fixture_doc["fixture_source_sha256"],
                        len(original["coverage"]["physical_slots_included"]),
                        len(original["coverage"]["items_included"])))
        print(f"{source_id}: config={canonical_config_hash(original)} fixture={fixture_doc['fixture_source_sha256']} "
              f"included_slots={len(original['coverage']['physical_slots_included'])} "
              f"included_items={len(original['coverage']['items_included'])}")
    return 0


def spec_id(ctx: Mapping[str, Any]) -> str:
    return ctx["spec"]["fixture_id"]


if __name__ == "__main__":
    raise SystemExit(main())
