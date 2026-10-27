"""Build the R157 AFRO full source-configuration library for SRC01-SRC03.

Generates full original/fixture configs for SRC01-SRC03 and exercises the
full bound library on nonrespondent fixtures.  Writes only the AFRO lane paths.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, ExactRef, RespondentEvent
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
from rawlsing_next.source_configuration.fixture import fixture_document_sha256, fixture_stream_from_document
from rawlsing_next.source_configuration.reader import reader_configuration_from_config, source_read_request_from_config
from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config, SourceConfig

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "rawlsing_next/source_configuration/data"
VALIDATION = ROOT / "source_pre553_validation"
PARTIAL_PATH = VALIDATION / "SRC01/afro_helpers.py"

spec = importlib.util.spec_from_file_location("r157_afro_partial", PARTIAL_PATH)
partial = importlib.util.module_from_spec(spec)
sys.modules["r157_afro_partial"] = partial
spec.loader.exec_module(partial)

ref = partial.ref
sha_json = partial.sha_json
authority = partial.authority
snapshot = partial.snapshot
canonical_token = partial.canonical_token
_is_number = partial._is_number

SOURCES = ("SRC01", "SRC02", "SRC03")
WEIGHT_NAMES = {"withinwt", "acrosswt", "combinwt", "africawt", "afcombwt",
                "withinwt_ea", "withinwt_hh", "combinwt_old_ea", "combinwt_new_hh"}
RESPONSE_SCALAR = {"scalar", "binary_factual", "binary_contrast", "ordinal_context", "nominal_choice", "binary_tradeoff"}
CONTEXT_TOPOS = {"continuous_context", "context_index", "administrative", "open_text"}
CONTEXT_DISPOSITIONS = {"POSITION_COORDINATE", "STRUCTURAL_CONTEXT", "ADMINISTRATIVE_METADATA"}


def key_name(sid: str) -> str:
    return "casenumb" if sid == "SRC01" else "RESPNO"


def country_name(sid: str) -> str:
    return "country" if sid == "SRC01" else "COUNTRY"


def is_weight(name: str) -> bool:
    low = name.lower()
    return low in WEIGHT_NAMES or low.startswith("weight") or low.endswith("wt") or "withinwt" in low or low.startswith("combinwt")


def state_for_code(code: float, label: Any) -> str:
    text = str(label or "").strip().lower()
    if "refused" in text:
        return "REFUSAL"
    if "don't know" in text or "dont know" in text or "don’t know" in text or "haven't heard enough" in text:
        return "DK"
    if "not asked" in text or "not in country" in text or "item not included" in text:
        return "NOT_ASKED"
    if "not applicable" in text:
        return "IAP"
    if "missing" in text:
        return "MISSING"
    if "no answer" in text:
        return "REFUSAL"
    if code < 0:
        return {-1.0: "MISSING", -2.0: "REFUSAL", -3.0: "IAP",
                -4.0: "NOT_ASKED", -5.0: "MISSING"}.get(float(code), "MISSING")
    return "SUBSTANTIVE_RESPONSE"


def labels_by_code(slot: dict[str, Any]) -> dict[float, Any]:
    out: dict[float, Any] = {}
    for key, label in (slot.get("value_labels") or {}).items():
        if _is_number(key):
            out[float(key)] = label
    return out


def routing_status(item: dict[str, Any]) -> str:
    for binding in item["h48"].get("candidate_bindings", []):
        if binding["family"] == "O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl":
            return binding.get("status", {}).get("routing_status", "")
    return ""


def routing_state(status: str) -> str:
    if status == "UNCONDITIONAL_SOURCE_PROVEN":
        return "ELIGIBLE_APPLICABLE"
    if status == "ADMIN_OR_NONRESPONDENT":
        return "INAPPLICABLE"
    if status in {"RESPONDENT_ANSWER_CONDITIONAL", "COUNTRY_CONDITIONAL", "MULTI_CONDITION",
                  "SPLIT_SAMPLE_CONDITIONAL", "DEMOGRAPHIC_OR_ELIGIBILITY_CONDITIONAL",
                  "MODULE_OR_BALLOT_CONDITIONAL"}:
        return "RULE_UNAVAILABLE"
    return "ROUTING_UNKNOWN"


def classify(item: dict[str, Any], slot: dict[str, Any]) -> tuple[str, str]:
    name = slot["name"]
    disp = item["p2"].get("canonical_disposition", "")
    binding = item["p2"].get("response_binding_status", "")
    relation = item.get("relation")
    topology = relation.get("manual_response_topology", "") if relation else ""
    labels = slot.get("value_labels") or {}
    if name == key_name(item["source_id"]):
        return "key", "Source-native respondent key."
    if name == country_name(item["source_id"]):
        return "country", "Source-native country coordinate."
    if is_weight(name):
        return "weight", "Source-native weight measure; raw/unweighted scope remains separate."
    if disp == "GENERATION_FORBIDDEN":
        return "held_generation_forbidden", "Evidence marks the item generation-forbidden."
    if disp == "UNKNOWN":
        return "held_unknown", "P2 disposition is UNKNOWN; no response/coordinate semantics are established."
    if topology == "ranked_choice":
        return "held_ranked", "Ranked/order topology requires rank/component evidence absent from the item row."
    if binding != "bound" and (topology in RESPONSE_SCALAR or topology == "multiselect_child"):
        return "held_blocked_response", "Response binding is not established for this item."
    if topology in RESPONSE_SCALAR and labels:
        return "response", "Finite source value labels and bound response; scalar response owner."
    if topology == "multiselect_child" and labels:
        return "response_component", "Finite source value labels; multiselect child carried as componentized response."
    if topology in CONTEXT_TOPOS or disp in CONTEXT_DISPOSITIONS:
        return "coordinate", "Source-native context/administration value carried as a coordinate/context fact."
    if not labels:
        return "coordinate", "No finite response domain; raw source value carried at coordinate/context grade."
    if relation is None:
        return "held_unmatched_relation", "No full-relation row for this exact implementation ID; exact unmatched premise."
    return "held_unknown", "Topology/disposition does not support a lawful native response or coordinate owner."


def response_rule_set(item: dict[str, Any], slot: dict[str, Any], mapping_ref, topology_ref,
                      topology: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    labels = slot.get("value_labels") or {}
    codes = sorted(float(k) for k in labels if _is_number(k))
    label_map = labels_by_code(slot)
    if topology == "multiselect_child":
        component = ref("COMPONENT", f"{item['source_id']}:{slot['name']}:component",
                        item["exact_identity_sha256"])
        occurrence = {
            "key": "0",
            "topology_ref": ref("RESPONSE_TOPOLOGY", f"{item['source_id']}:{slot['name']}:COMPONENTIZED",
                                sha_json({"sid": item["source_id"], "var": slot["name"],
                                          "topology": "COMPONENTIZED_RESPONSE"})).as_dict(),
            "multiplicity_order_rank_fields": {"kind": "COMPONENTIZED_RESPONSE", "index": 0},
            "component_ref": component.as_dict(),
        }
    else:
        occurrence = {
            "key": "0",
            "topology_ref": topology_ref.as_dict(),
            "multiplicity_order_rank_fields": {"kind": "SCALAR_SINGULAR", "index": 0},
        }
    values = []
    specs = []
    for code in codes:
        state = state_for_code(code, label_map.get(float(code)))
        substantive = state == "SUBSTANTIVE_RESPONSE"
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
        specs.append({"raw_value": float(code), "missing_state": "OBSERVED_STORAGE_VALUE",
                      "response_state": state, "canonical_value": canonical})
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
    specs.append({"raw_value": None, "missing_state": "SYSTEM_MISSING",
                  "response_state": "MISSING", "canonical_value": None})
    return values, specs


def coordinate_rule(slot: dict[str, Any], coord_ref, *, wave: str) -> dict[str, Any]:
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
        "native_coordinate_ref": ref("COORDINATE_NATIVE", f"{slot['name']}:{wave}",
                                     slot["codebook_mapping"].get("row_hash")
                                     or sha_json({"slot": slot["name"], "wave": wave})).as_dict(),
        "unit_taxonomy_ref": ref("UNIT_TAXONOMY", f"{slot['name']}:{wave}",
                                 sha_json({"unit": "SOURCE_NATIVE_CONTEXT", "slot": slot["name"], "wave": wave})).as_dict(),
        "effective_time": wave,
        "source_semantic_authority_ref": coord_ref.as_dict(),
        "canonical_coordinate_ref": None,
        "normalization_ref": None,
        "values": values,
        "copy_observed_raw": True,
    }


def weight_rule(slot: dict[str, Any], weight_ref, *, wave: str) -> dict[str, Any]:
    return {
        "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
        "weight_basis_id": f"SOURCE_NATIVE_WEIGHT:{slot['name']}:{wave}",
        "weight_source_ref": ref("WEIGHT_SOURCE", f"{slot['name']}:{wave}",
                                 slot["codebook_mapping"].get("row_hash")
                                 or sha_json({"weight": slot["name"], "wave": wave})).as_dict(),
        "design_authority_ref": weight_ref.as_dict(),
        "estimand_authority_ref": weight_ref.as_dict(),
        "effective_scope_ref": ref("WEIGHT_SCOPE", f"{wave}:source-native",
                                   sha_json({"wave": wave, "scope": "SOURCE_NATIVE_WEIGHT"})).as_dict(),
        "normalization_ref": None,
        "values": [],
        "copy_observed_numeric": True,
        "extra_authority_refs": [],
    }


def authorities_full(sid: str, wave: str, source_sha: str, evidence_hash: str, *,
                     decision: str, fixture_sha: str | None = None,
                     fixture_id: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    specs = (
        ("source", "SOURCE_SEMANTICS_TOPOLOGY", ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
        ("mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION", ("RespondentEvent@1.0.0",)),
        ("topology", "SOURCE_SEMANTICS_TOPOLOGY", ("RespondentEvent@1.0.0",)),
        ("coordinate", "COORDINATE_SEMANTICS", ("EmpiricalCoordinateFact@1.0.0",)),
        ("routing", "ROUTING_RISK_SET", ("RoutingEligibilityFact@1.0.0",)),
        ("weight", "WEIGHT_DESIGN_ESTIMAND", ("WeightMeasureFact@1.0.0",)),
        ("replay", "REPLAY_PROTOCOL", ("ReplayReceipt@1.0.0",)),
        ("projection", "SOURCE_SEMANTICS_TOPOLOGY",
         ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0")),
    )
    refs = {}
    snaps = []
    for tag, kind, families in specs:
        auth = authority(tag, kind, families, sid=sid, wave=wave, source_sha=source_sha,
                         decision=decision, evidence_hash=evidence_hash,
                         fixture_sha=fixture_sha, fixture_id=fixture_id)
        refs[tag] = auth
        snaps.append(snapshot(tag, kind, families, auth, sid=sid, wave=wave,
                              source_sha=source_sha, decision=decision, evidence_hash=evidence_hash,
                              fixture_sha=fixture_sha, fixture_id=fixture_id))
    return {
        "snapshots": snaps,
        "required_refs": [refs[k].as_dict() for k in
                          ("source", "mapping", "topology", "coordinate", "routing", "weight", "replay", "projection")],
        "projection_authority_ref": refs["projection"].as_dict(),
        "replay_authority_ref": refs["replay"].as_dict(),
    }, refs


def universe_full(sid: str, wave: str, source_sha: str, source_ref, *, fixture: bool,
                  fixture_id: str | None = None) -> tuple[dict[str, Any], EmpiricalUniverse]:
    root = ref("UNIVERSE_REPLAY_ROOT", f"{sid}:universe:{'fixture' if fixture else 'source'}",
               sha_json({"sid": sid, "wave": wave, "fixture": fixture, "family": "Afrobarometer"}))
    if fixture:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED",
            "authority_snapshot_refs": [source_ref.as_dict()],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": root.as_dict(),
            "raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:{sid}:{fixture_id}",
            "source_family": "Afrobarometer",
            "study_product_release": f"R157_FIXTURE/Afrobarometer/{wave}",
            "instrument_release": f"R157_FIXTURE_INSTRUMENT/Afrobarometer/{wave}",
            "country_geography": "FIXTURE_MULTI_COUNTRY",
            "sampling_geography": "FIXTURE_NONPROBABILITY",
            "raw_wave": wave,
            "canonical_wave_if_governed": None,
            "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
            "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
            "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
            "respondent_namespace": f"urn:rawlsing:r157:afro:{sid}:fixture",
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
            "raw_source_identity": f"Afrobarometer:{wave}:{source_sha}",
            "source_family": "Afrobarometer",
            "study_product_release": f"Afrobarometer/{wave}",
            "instrument_release": f"Afrobarometer {wave} source instrument",
            "country_geography": "SOURCE_NATIVE_MULTI_COUNTRY_WAVE",
            "sampling_geography": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "raw_wave": wave,
            "canonical_wave_if_governed": None,
            "field_or_reference_time": wave,
            "target_population_and_sample_frame": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "sampling_design_regime": "NOT_ESTABLISHED_IN_CURRENT_EVIDENCE",
            "respondent_namespace": f"urn:rawlsing:r157:afro:{sid}:{key_name(sid)}",
            "source_artifact_import_lineage": f"Afrobarometer:{wave}:{source_sha}",
            "harmonization_authority_ref": None,
            "source_relation_refs": [],
        }
    try:
        return payload, EmpiricalUniverse(**payload)
    except Exception as exc:
        raise RuntimeError(f"{sid}: cannot construct Afrobarometer universe: {exc}") from exc


def question_full(item: dict[str, Any], var: str, universe_ref, source_ref, topology_ref) -> dict[str, Any]:
    return {
        "question_id": var,
        "empirical_universe_ref": universe_ref.as_dict() if hasattr(universe_ref, "as_dict") else universe_ref,
        "native_question_ref": ref("NATIVE_QUESTION", f"{item['source_id']}:{var}",
                                   item["exact_identity_sha256"]).as_dict(),
        "instrument_question_version": item["w2_wave"] if "w2_wave" in item else item["wave"],
        "canonical_question_ref_or_typed_absence": TypedAbsence("NOT_AUTHORIZED").as_dict(),
        "component_subitem_ref_or_typed_absence": TypedAbsence("NOT_APPLICABLE").as_dict(),
        "semantic_authority_ref": source_ref.as_dict(),
        "topology_authority_ref": topology_ref.as_dict(),
        "item_evidence": {"implementation_id": item["implementation_id"],
                          "exact_identity_sha256": item["exact_identity_sha256"],
                          "relation_join_status": "EXACT"},
    }


def item_full_payload(item: dict[str, Any], classification: str) -> dict[str, Any]:
    payload = partial.item_payload(item, selected=(classification in {"response", "response_component"}),
                                   supported_var=item["source_variable_code"])
    if classification not in {"response", "response_component"}:
        payload["limits"] = [
            *payload["limits"],
            f"native_binding={classification}",
        ]
    return payload


def physical_full_payload(slot: dict[str, Any], classification: str) -> dict[str, Any]:
    reason = {
        "response": "Finite source response bound to the existing C11 response owner.",
        "response_component": "Multiselect child bound as a componentized response; parent grouping residual.",
        "coordinate": "Source-native context/coordinate value carrier; raw observed value.",
        "weight": "Source-native weight measure; not a population/estimand claim.",
        "key": "Source-native unified respondent key.",
        "country": "Source-native country coordinate.",
        "held_generation_forbidden": "Held: evidence marks generation forbidden.",
        "held_unknown": "Held: P2 disposition/semantics UNKNOWN.",
        "held_ranked": "Held: ranked/order topology evidence incomplete.",
        "held_blocked_response": "Held: response binding not established.",
        "held_unmatched_relation": "Held: exact implementation ID has no full-relation row.",
    }[classification]
    payload = partial.physical_slot_payload(slot, selected=classification in {"response", "response_component"},
                                            country=classification == "country", key_slot=classification == "key")
    payload["disposition"] = {
        "response": "SUPPORTED_RESPONSE",
        "response_component": "SUPPORTED_COMPONENT_RESPONSE",
        "coordinate": "SUPPORTED_COORDINATE_CONTEXT",
        "weight": "SUPPORTED_WEIGHT_SOURCE_NATIVE",
        "key": "SUBJECT_KEY",
        "country": "SUPPORTED_COORDINATE",
        "held_generation_forbidden": "HELD_GENERATION_FORBIDDEN",
        "held_unknown": "HELD_UNKNOWN",
        "held_ranked": "HELD_RANKED_TOPOLOGY",
        "held_blocked_response": "HELD_BLOCKED_RESPONSE",
        "held_unmatched_relation": "HELD_UNMATCHED_RELATION",
    }[classification]
    payload["disposition_reason"] = reason
    return payload


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")


def build_full_one(sid: str, *, artifact_commit: str) -> dict[str, Any]:
    roster = source_roster_entry(sid)
    wave = roster["wave"]
    source_sha = roster["source_sha256"]
    physical = {p["ordinal"]: p for p in iter_physical_slots(sid)}
    codebook = {c["var_name"]: c for c in iter_codebook_rows(sid)}
    items = list(iter_item_evidence(sid))
    if len(items) != roster["original_items"] or len(physical) != roster["physical_columns"]:
        raise RuntimeError(f"{sid}: evidence counts do not match roster")
    by_name = {p["name"]: p for p in physical.values()}
    relation_hashes = {x["source_variable_code"]: (x.get("relation") or {}).get("governed_row_payload_hash", "")
                       for x in items}
    evidence_hash = sha_json({"sid": sid, "wave": wave,
                              "relations": sorted((k, v) for k, v in relation_hashes.items() if v)})
    fixture_id = f"R157-AFRO-{sid}-FULL-NONRESPONDENT"
    classifications = {x["source_variable_code"]: classify(x, by_name[x["source_variable_code"]]) for x in items}

    original_snaps, original_refs = authorities_full(sid, wave, source_sha, evidence_hash, decision="DEFER")
    # fixture SHA is needed for fixture authority; build the fixture skeleton first.
    # The fixture config/data are generated after the shape decisions below.
    original_universe_payload, original_universe = universe_full(
        sid, wave, source_sha, original_refs["source"], fixture=False)
    # fixture universe/refs need fixture SHA; placeholder values are replaced after fixture SHA.
    fixture_snaps, fixture_refs = authorities_full(
        sid, wave, source_sha, evidence_hash, decision="ALLOW",
        fixture_sha="0" * 64, fixture_id=fixture_id)
    fixture_universe_payload, fixture_universe = universe_full(
        sid, wave, source_sha, fixture_refs["source"], fixture=True, fixture_id=fixture_id)

    # Shared question/response/coordinate/weight/routing decisions are built twice
    # with the original and fixture authority/universe refs.
    def parts(refs, universe, *, decision: str):
        questions = []
        response_slots = []
        response_specs = []
        coordinate_slots = []
        weight_slots = []
        routing = []
        held = []
        for item in items:
            slot = by_name[item["source_variable_code"]]
            var = item["source_variable_code"]
            cls, _ = classifications[var]
            topology = (item.get("relation") or {}).get("manual_response_topology", "")
            topology_ref = ref("RESPONSE_TOPOLOGY", f"{sid}:{var}:{topology or 'CONTEXT'}",
                               item["exact_identity_sha256"])
            if cls in {"response", "response_component"}:
                q = question_full(item, var, universe.ref, refs["source"], refs["topology"])
                questions.append(q)
                values, specs = response_rule_set(item, slot, refs["mapping"], topology_ref, topology)
                response_slots.append({"slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
                                       "question_id": var, "values": values})
                status = routing_status(item)
                h = item["exact_identity_sha256"]
                routing.append({
                    "question_id": var,
                    "row_selector": "ALL",
                    "typed_state": routing_state(status),
                    "risk_set_ref": ref("RISK_SET", f"{sid}:{var}:routing", h).as_dict(),
                    "routing_rule_ref": ref("ROUTING_RULE", f"{sid}:{var}:o06:{status}", h).as_dict(),
                    "member_set_replay_ref": ref("MEMBER_SET_REPLAY", f"{sid}:{var}:all", h).as_dict(),
                    "authority_ref": refs["routing"].as_dict(),
                    "parent_predicate_refs": [],
                    "dependency_refs": [],
                })
                response_specs.append({"var": var, "slot": slot, "specs": specs,
                                       "question_ref": ref("NATIVE_QUESTION", f"{sid}:{var}",
                                                           item["exact_identity_sha256"]),
                                       "topology": topology})
            elif cls in {"coordinate", "country"}:
                coordinate_slots.append(coordinate_rule(slot, refs["coordinate"], wave=wave))
            elif cls == "weight":
                weight_slots.append(weight_rule(slot, refs["weight"], wave=wave))
            elif cls == "key":
                pass
            else:
                held.append({"item": item, "slot": slot, "classification": cls})
        # country slot is always a coordinate; add if not already present.
        if not any(x["slot"]["name"] == country_name(sid) for x in coordinate_slots):
            coordinate_slots.append(coordinate_rule(by_name[country_name(sid)], refs["coordinate"], wave=wave))
        return {"questions": questions, "response_slots": response_slots, "response_specs": response_specs,
                "coordinate_slots": coordinate_slots, "weight_slots": weight_slots,
                "routing": routing, "held": held}

    original_parts = parts(original_refs, original_universe, decision="DEFER")
    fixture_parts = parts(fixture_refs, fixture_universe, decision="ALLOW")
    # remove duplicate country coordinate for the source parts (add once if needed)
    def dedupe_coords(coords):
        seen = set()
        out = []
        for c in coords:
            key = (c["slot"]["ordinal"], c["slot"]["name"])
            if key not in seen:
                seen.add(key)
                out.append(c)
        return out
    original_parts["coordinate_slots"] = dedupe_coords(original_parts["coordinate_slots"])
    fixture_parts["coordinate_slots"] = dedupe_coords(fixture_parts["coordinate_slots"])

    physical_original = [physical_full_payload(p, classifications[p["name"]][0])
                         for p in sorted(physical.values(), key=lambda x: x["ordinal"])]
    items_original = [item_full_payload(x, classifications[x["source_variable_code"]][0]) for x in items]
    original_ids = [x["implementation_id"] for x in items_original]

    manifest = load_manifest()
    pinned = [{k: v for k, v in e.items() if k in {"kind", "sha256", "commit", "path", "bytes", "locator"}}
              for e in manifest["pinned_inputs"]]
    field_evidence = []
    var = items[0]["source_variable_code"]
    item = next(x for x in items if x["source_variable_code"] == var)
    field_evidence.append({"field": f"items[{var}].implementation_id", "refs": [
        ref("H48_ITEM_AUTHORITY", f"{sid}:{item['implementation_id']}:h48", item["exact_identity_sha256"]).as_dict(),
        ref("P2_PHASE0_ROW", f"{sid}:{item['implementation_id']}:p2",
            item["p2"]["exact_identity_sha256"]).as_dict(),
    ]})
    common_evidence = {
        "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
        "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
        "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
        "pinned_inputs": pinned,
        "field_evidence": field_evidence,
        "limits": ["Prior authority evidence is reused with its original grade and limits.",
                   "Original authority is DEFER; fixture authority is NONRESPONDENT_FIXTURE_ONLY.",
                   "No original respondent rows or original source file bytes were read."],
    }
    common_identity = {
        "source_id": sid, "family": roster["family"], "wave": wave,
        "source_family_id": "Afrobarometer", "study_product_id": "Afrobarometer",
        "release_id": f"Afrobarometer_{wave}",
        "instrument_release_id": f"SRC{sid[-2:]}_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
        "source_artifact_id": roster["source_artifact_id"], "expected_source_sha256": source_sha,
        "source_format": roster["format"], "source_row_count": roster["rows"],
        "source_column_count": roster["physical_columns"], "source_bytes": roster["bytes"],
        "codebook_rows": roster["codebook_rows"], "original_item_count": roster["original_items"],
        "source_snapshot_retention_ref": ExactRef("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:afro:{sid}:source", source_sha).as_dict(),
        "metadata_witness_ref": ExactRef("R154_PHYSICAL_METADATA", roster["metadata_witness"]["path"],
                                         roster["metadata_witness"]["sha256"]).as_dict(),
        "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": f"{sid}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
        "reader": {"decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                   "configuration_ref": ref("READER_CONFIGURATION", f"{sid}:sav", sha_json({
                       "source_sha256": source_sha, "encoding": roster["reader"]["required_encoding"]})).as_dict(),
                   "encoding": (None if roster["reader"]["required_encoding"] is None else {
                       "value": roster["reader"]["required_encoding"], "sha256": source_sha,
                       "authority_status": roster["reader"]["encoding_authority_status"]})},
    }
    common_respondents = {
        "subject_unit": "SOURCE_NATIVE_RESPONDENT",
        "respondent_namespace": f"urn:rawlsing:r157:afro:{sid}:{key_name(sid)}",
        "respondent_key_pattern": f"AFRO-{sid}-{wave}-ROW-{{row_ordinal:06d}}",
        "source_native_key_slot": {"ordinal": by_name[key_name(sid)]["ordinal"], "name": key_name(sid)},
        "identity_map_authority_ref": None, "row_identity_grade": f"SOURCE_NATIVE_{key_name(sid).upper()}",
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

    def config(*, fixture: bool) -> dict[str, Any]:
        parts_ = fixture_parts if fixture else original_parts
        refs = fixture_refs if fixture else original_refs
        authority_section = (fixture_snaps if fixture else original_snaps)
        authority_section = {**authority_section,
                             "projection_identity_ref": ref("C11_SEMANTIC_PROJECTION",
                                                            f"{sid}:full:{'fixture' if fixture else 'source'}",
                                                            sha_json({"sid": sid, "full": True,
                                                                      "fixture": fixture})).as_dict(),
                             "tie_order_ref": ref("ORDER_RULE", f"{sid}:full:{'fixture' if fixture else 'source'}:sort",
                                                  sha_json({"sid": sid, "sort": True})).as_dict(),
                             "replay_protocol_version": "1.0.0"}
        if fixture:
            binding = {"identity_class": "NONRESPONDENT_FIXTURE", "source_sha256": fixture_sha,
                       "row_count": 6,
                       "source_snapshot_ref": ExactRef("FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:afro:{fixture_id}", fixture_sha).as_dict(),
                       "fixture_provenance": {"fixture_id": fixture_id,
                                              "provenance": "Repository-generated nonrespondent full AFRO shape fixture; no original respondents represented.",
                                              "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                                              "original_source_id": sid, "original_source_sha256": source_sha,
                                              "no_original_respondents": True,
                                              "fixture_study_product_id": f"R157_FIXTURE/Afrobarometer/{wave}",
                                              "fixture_release_id": f"R157_FIXTURE_RELEASE/Afrobarometer/{wave}",
                                              "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/Afrobarometer/{wave}"}}
            universe = {"universes": [fixture_universe_payload]}
            purpose = "NONRESPONDENT_FIXTURE"; scope_purpose = "NONRESPONDENT_FIXTURE_VALIDATION"
            declared = True; expectation = "POSITIVE_RELEASE"
            coverage_included = sorted(physical)
        else:
            binding = {"identity_class": "ORIGINAL_SOURCE", "source_sha256": source_sha,
                       "row_count": roster["rows"], "source_snapshot_ref": common_identity["source_snapshot_retention_ref"],
                       "fixture_provenance": None}
            universe = {"universes": [original_universe_payload]}
            purpose = "SOURCE_PREPARATION"; scope_purpose = "SOURCE_PREPARATION"
            declared = False; expectation = "NOT_RUN"
            coverage_included = sorted(physical)
        held_ids = [x["item"]["implementation_id"] for x in parts_["held"]]
        held_cats = {}
        for x in parts_["held"]:
            held_cats.setdefault(x["classification"], []).append(x)
        residuals = [
            partial.residual("ORIGINAL_AUTHORITY_DEFER", f"{sid}", "authority.snapshots", "DEFER",
                             "Original AFRO authority snapshots are prior-evidence/DEFER only; no ALLOW authority is invented.",
                             "original-source native validation/execution", "fixture native validation and full source recipe",
                             "integration supplies exact authority if original native validation is required."),
            partial.residual("WEIGHTS_SOURCE_NATIVE_ONLY", f"{sid}", "weight_slots", "SOURCE_NATIVE_ONLY",
                             "Weight slots preserve source-native weight variables; no population/estimand claim is made.",
                             "population/weighted inference", "raw/unweighted configuration and fixture validation",
                             "P4 weighted scope only if warranted by authority."),
            partial.residual("COUNTRY_NO_CANONICAL_CROSSWALK", f"{sid}", "coordinate_slots.country", "RAW_ONLY",
                             "Country code is carried source-native; no canonical country crosswalk is claimed.",
                             "canonical country comparisons", "source-native country coordinate",
                             "P4 material/context lane if warranted."),
        ]
        for cat, entries in sorted(held_cats.items()):
            ids = [e["item"]["implementation_id"] for e in entries]
            residuals.append(partial.residual(
                cat.upper(), f"{sid}", "response/coordinate/weight native binding", "HELD_EXACT_PREMISE",
                f"{len(ids)} items have no lawful native binding: {classify(entries[0]['item'], entries[0]['slot'])[1]}",
                "native semantic binding for held items", "all bound items and full source ledger",
                "exact source/semantic evidence for the held category or retain as held."))
        if sid in {"SRC01", "SRC02", "SRC05"}:
            residuals.append(partial.residual(
                "READER_WINDOWS1252_NOT_OVERRIDDEN", f"{sid}", "identity.reader.encoding", "NOT_OVERRIDDEN",
                "No exact decoder allowlist entry exists for this source SHA; automatic guessing is forbidden.",
                "source text decode", "numeric/metadata and fixture-native items",
                "P3 reader lane only if exact allowlist evidence arises."))
        coverage = {"physical_slots_total": roster["physical_columns"],
                    "items_total": roster["original_items"],
                    "physical_slots_included": coverage_included,
                    "physical_slots_excluded": [],
                    "items_included": original_ids,
                    "items_excluded": []}
        if fixture:
            coverage["partial_scope_reason"] = "Full source ledger retained; fixture cells exercise all bound native slots."
        return {
            "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
            "config_id": f"R157-AFRO-{sid}-FULL-{'FIXTURE' if fixture else 'SOURCE'}",
            "config_revision": 1, "config_purpose": purpose,
            "identity": common_identity, "binding": binding, "authority": authority_section,
            "universe": universe, "respondents": common_respondents,
            "questions": parts_["questions"], "physical_slots": physical_original,
            "items": items_original, "response_slots": parts_["response_slots"],
            "coordinate_slots": parts_["coordinate_slots"], "weight_slots": parts_["weight_slots"],
            "routing": parts_["routing"],
            "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
            "replay": {"predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
                       "comparator": TypedAbsence("DEFERRED").as_dict(),
                       "discovery": TypedAbsence("DEFERRED").as_dict(),
                       "structural": TypedAbsence("NOT_APPLICABLE").as_dict()},
            "supported_scope": {"scope_id": f"AFRO-{sid}-FULL-{'FIXTURE' if fixture else 'SOURCE'}",
                                "purpose": scope_purpose, "declared_supported": declared,
                                "supported_question_ids": [q["question_id"] for q in parts_["questions"]],
                                "native_validation_expectation": expectation,
                                "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
                                "supported_unit_slice": "SOURCE_NATIVE_UNIFIED_RESPONDENT_ID_COCAS",
                                "supported_form_slice": f"AFRO {wave} full available source bindings",
                                "notes": ["Full source ledger; held categories are exact residuals, not generic P4 deferrals."]},
            "coverage": coverage, "residuals": residuals,
            "evidence": common_evidence, "runtime": common_runtime,
        }

    # Build the fixture cells first so fixture SHA is available for authority/config.
    def choose_cell_value(item: dict[str, Any], slot: dict[str, Any], specs: list[dict[str, Any]], row: int) -> dict[str, Any]:
        substantive = [s for s in specs if s["response_state"] == "SUBSTANTIVE_RESPONSE"]
        special = [s for s in specs if s["missing_state"] != "SYSTEM_MISSING"
                   and s["response_state"] != "SUBSTANTIVE_RESPONSE"]
        system = [s for s in specs if s["missing_state"] == "SYSTEM_MISSING"]
        if row == 1:
            choice = substantive[0] if substantive else specs[0]
        elif row == 2:
            choice = substantive[1] if len(substantive) > 1 else (substantive[0] if substantive else specs[0])
        elif row == 3:
            choice = substantive[-1] if substantive else specs[0]
        elif row == 4:
            choice = special[0] if special else (substantive[0] if substantive else specs[0])
        elif row == 5:
            choice = system[0] if system else (substantive[0] if substantive else specs[0])
        else:
            choice = special[1] if len(special) > 1 else (substantive[0] if substantive else specs[0])
        return choice

    key_slot = by_name[key_name(sid)]
    key_is_string = str(key_slot.get("readstat_type", "")).lower() in {"string", "str"}
    country_slot = by_name[country_name(sid)]
    country_codes = sorted(float(k) for k in (country_slot.get("value_labels") or {})
                           if _is_number(k) and float(k) >= 0) or [1.0]
    cells = []
    expected_map = {}
    for row in range(1, 7):
        key_value = (f"AFRO-{sid}-{row:04d}" if key_is_string
                     else 990000000.0 + (int(sid[-2:]) * 1000.0) + row)
        cells.append({"row_ordinal": row, "variable_ordinal": key_slot["ordinal"],
                      "variable_name": key_slot["name"], "raw_value": key_value,
                      "missing_state": "OBSERVED_STORAGE_VALUE", "source_missing_declaration": None})
        for coord in fixture_parts["coordinate_slots"]:
            slot = by_name[coord["slot"]["name"]]
            if slot["name"] == country_name(sid):
                raw = country_codes[(row - 1) % len(country_codes)]
            else:
                labels = slot.get("value_labels") or {}
                substantive = [float(k) for k in labels if _is_number(k) and float(k) >= 0]
                if substantive:
                    raw = substantive[(row - 1) % len(substantive)]
                elif str(slot.get("readstat_type", "")).lower() in {"string", "str"}:
                    raw = "FIXTURE"
                else:
                    raw = 1.0
            cells.append({"row_ordinal": row, "variable_ordinal": slot["ordinal"], "variable_name": slot["name"],
                          "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
        for weight in fixture_parts["weight_slots"]:
            slot = by_name[weight["slot"]["name"]]
            cells.append({"row_ordinal": row, "variable_ordinal": slot["ordinal"], "variable_name": slot["name"],
                          "raw_value": 1.0, "missing_state": "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
        for spec_ in fixture_parts["response_specs"]:
            spec = choose_cell_value(spec_["item"] if "item" in spec_ else next(x for x in items if x["source_variable_code"] == spec_["var"]),
                                     spec_["slot"], spec_["specs"], row)
            slot = spec_["slot"]
            cells.append({"row_ordinal": row, "variable_ordinal": slot["ordinal"], "variable_name": slot["name"],
                          "raw_value": spec["raw_value"], "missing_state": spec["missing_state"],
                          "source_missing_declaration": None})
            expected_map[(spec_["question_ref"].object_id, row)] = (spec["response_state"], spec["canonical_value"])

    fixture_doc = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
        "fixture_id": fixture_id, "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True, "row_count": 6, "cells": cells,
        "expected_results": {
            "fixture_only": True, "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "response_event_count": len(fixture_parts["response_specs"]) * 6,
            "coordinate_fact_count": len(fixture_parts["coordinate_slots"]) * 6,
            "routing_fact_count": len(fixture_parts["routing"]) * 6,
            "weight_fact_count": len(fixture_parts["weight_slots"]) * 6,
            "response_slot_count": len(fixture_parts["response_specs"]),
            "coordinate_slot_count": len(fixture_parts["coordinate_slots"]),
            "routing_rule_count": len(fixture_parts["routing"]),
            "weight_slot_count": len(fixture_parts["weight_slots"]),
            "key_count": 6,
            "response_state_counts": {
                state: sum(1 for (s, _) in [v for v in expected_map.values()] if s == state)
                for state in sorted({s for (s, _) in expected_map.values()})
            },
            "expected_pairs_sha256": sha_json(sorted((q, r, s, c) for (q, r), (s, c) in expected_map.items())),
        },
    }
    fixture_sha = fixture_document_sha256(fixture_doc)
    fixture_doc["fixture_source_sha256"] = fixture_sha
    # Rebuild fixture authority with the exact fixture SHA.
    fixture_snaps, fixture_refs = authorities_full(
        sid, wave, source_sha, evidence_hash, decision="ALLOW",
        fixture_sha=fixture_sha, fixture_id=fixture_id)
    # Fixture universe/refs need the rebuilt source authority.
    fixture_universe_payload, fixture_universe = universe_full(
        sid, wave, source_sha, fixture_refs["source"], fixture=True, fixture_id=fixture_id)
    fixture_parts = parts(fixture_refs, fixture_universe, decision="ALLOW")
    fixture_parts["coordinate_slots"] = dedupe_coords(fixture_parts["coordinate_slots"])
    # Rebuild cells/expected map with the final fixture authority refs (same values).
    # The response specs are identical; only authority refs changed in configs.
    fixture_config = config(fixture=True)
    fixture_cfg = SourceConfig(fixture_config)
    fixture_stream = fixture_stream_from_document(fixture_doc)
    keys = row_native_keys_from_transport(fixture_cfg, stream=fixture_stream)
    projection = build_governed_c11_projection(fixture_cfg, row_native_keys=keys)
    release = build_validated_c11_release_from_config(fixture_cfg, stream=fixture_stream)
    repository, repository_release = build_source_backed_c11_repository_from_config(fixture_cfg, fixture_stream)
    row_by_object = {r.ref.object_id: index for index, r in enumerate(projection.respondents, 1)}
    events = [x for x in release.public_objects if isinstance(x, RespondentEvent)]
    actual_map = {}
    for event in events:
        qid = dict(event.native_question_ref)["object_id"]
        rid = dict(event.scoped_respondent_ref)["object_id"]
        actual_map[(qid, row_by_object[rid])] = (event.response_state, event.canonical_response_value_if_authorized)
    if actual_map != expected_map:
        # Keep exact mismatch evidence, but do not claim a native positive.
        mismatch = {
            "expected": len(expected_map), "actual": len(actual_map),
            "missing": [k for k in expected_map if k not in actual_map][:10],
            "extra": [k for k in actual_map if k not in expected_map][:10],
        }
        raise RuntimeError(f"{sid}: full fixture native map mismatch {mismatch}")
    actual_state_counts = {}
    for state, _ in actual_map.values():
        actual_state_counts[state] = actual_state_counts.get(state, 0) + 1
    if actual_state_counts != fixture_doc["expected_results"]["response_state_counts"]:
        raise RuntimeError(f"{sid}: full fixture state count mismatch")
    if len(keys) != 6:
        raise RuntimeError(f"{sid}: full fixture key count mismatch")

    # Build original full config only after fixture is proven.
    original_config = config(fixture=False)
    SourceConfig(original_config)
    original_reader = reader_configuration_from_config(original_config)
    original_request = source_read_request_from_config(
        original_config, host="R157_AFRO_LANE", purpose="R157_AFRO_FULL_CONFIGURATION_PREPARATION",
        consumer_use="R157_AFRO_FULL_CONFIGURATION_PREPARATION",
        semantic_use_scope=("SOURCE_CONFIGURATION_PREPARATION",))

    data_dir = DATA / sid
    val_dir = VALIDATION / sid
    data_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    full_config_path = data_dir / f"{sid}.config.json"
    full_fixture_config_path = data_dir / f"{sid}.full.fixture.config.json"
    full_fixture_path = val_dir / f"{sid}.full.fixture.json"
    full_native_path = val_dir / "FULL_NATIVE_RESULTS.json"
    write_json(full_config_path, original_config)
    write_json(full_fixture_config_path, fixture_config)
    write_json(full_fixture_path, fixture_doc)

    held = original_parts["held"]
    held_by_cat = {}
    for entry in held:
        held_by_cat.setdefault(entry["classification"], []).append(entry)
    bound_response = [x for x in items if classifications[x["source_variable_code"]][0] in {"response", "response_component"}]
    bound_coord = [x for x in items if classifications[x["source_variable_code"]][0] in {"coordinate", "country"}]
    bound_weight = [x for x in items if classifications[x["source_variable_code"]][0] == "weight"]
    accounting = {
        "schema": "PYAT_R157_AFRO_FULL_SOURCE_EVIDENCE_ACCOUNTING@1.0.0",
        "source_id": sid, "family": roster["family"], "wave": wave, "source_sha256": source_sha,
        "counts": {"physical_columns": len(physical), "codebook_rows": len(codebook),
                   "original_items": len(items), "exact_relation_matches": sum(1 for x in items if x.get("relation")),
                   "unmatched_relation_ids": len(roster.get("unmatched_relation_ids", [])),
                   "physical_only": roster["physical_only"], "codebook_only": roster["codebook_only"]},
        "unmatched_relation_ids": list(roster.get("unmatched_relation_ids", [])),
        "native_bindings": {
            "response_items": len(bound_response),
            "response_component_items": sum(1 for x in items if classifications[x["source_variable_code"]][0] == "response_component"),
            "coordinate_items": len(bound_coord),
            "weight_items": len(bound_weight),
            "key_items": 1,
            "held_items": len(held),
        },
        "held_by_category": {cat: {"count": len(v), "implementation_ids": [e["item"]["implementation_id"] for e in v]}
                             for cat, v in sorted(held_by_cat.items())},
        "routing_states": {
            state: sum(1 for x in bound_response if routing_state(routing_status(x)) == state)
            for state in sorted({routing_state(routing_status(x)) for x in bound_response})
        },
        "weights": {"claimed": False, "source_native_slots": [x["source_variable_code"] for x in bound_weight]},
        "reader": {"required_encoding": roster["reader"]["required_encoding"],
                   "decoder_allowlist_encoding": roster["reader"]["decoder_allowlist_encoding"],
                   "configuration_ref": original_reader.configuration_ref.as_dict(),
                   "request_source_sha256": original_request.source_sha256},
        "evidence_refs": common_evidence["field_evidence"],
        "no_drop": {"items_unaccounted": 0, "slots_unaccounted": 0},
    }
    ledger_entries = [{
        "residual_id": "ORIGINAL_AUTHORITY_DEFER", "source_id": sid,
        "required_native_field": "authority.snapshots", "current_value": "DEFER",
        "exact_evidence_refs": common_evidence["field_evidence"],
        "missing_fact": "No current source-specific ALLOW authority snapshot is established.",
        "affected_operation_or_slice": "original-source native validation/execution",
        "unaffected_usable_slice": "full fixture native validation and full source recipe",
        "owner_and_next_step": "R157_AFRO_LANE -> integration source-grounded authority",
        "status": "HELD_DEFER_NOT_BLOCKING_FIXTURE", "resolution_evidence": None,
    }]
    for cat, entries in sorted(held_by_cat.items()):
        ledger_entries.append({
            "residual_id": cat.upper(), "source_id": sid,
            "implementation_ids": [e["item"]["implementation_id"] for e in entries],
            "physical_slot_ordinals": [e["slot"]["ordinal"] for e in entries],
            "count": len(entries), "required_native_field": "response/coordinate/weight native binding",
            "current_value": "HELD", "exact_evidence_refs": [{"field": "ITEM_EVIDENCE.jsonl.gz", "category": cat}],
            "missing_fact": classify(entries[0]["item"], entries[0]["slot"])[1],
            "affected_operation_or_slice": "native semantic binding for held items",
            "unaffected_usable_slice": "all bound response/coordinate/weight/key items",
            "owner_and_next_step": "R157_AFRO_LANE -> exact source/semantic evidence or retain as held",
            "status": "HELD_EXACT_PREMISE", "resolution_evidence": None,
        })
    # Conditional routing is not a generic item hold: record exact conditional item ids.
    conditional = [x for x in bound_response if routing_state(routing_status(x)) != "ELIGIBLE_APPLICABLE"]
    if conditional:
        ledger_entries.append({
            "residual_id": "ROUTING_EXPRESSION_UNAVAILABLE", "source_id": sid,
            "implementation_ids": [x["implementation_id"] for x in conditional],
            "count": len(conditional), "required_native_field": "routing rule expression",
            "current_value": "RULE_UNAVAILABLE/ROUTING_UNKNOWN",
            "exact_evidence_refs": [{"field": "H48 O06 routing status", "values": sorted({routing_status(x) for x in conditional})}],
            "missing_fact": "Exact route expression is not present in the item evidence; eligibility is not asserted.",
            "affected_operation_or_slice": "route-dependent response operations for conditional items",
            "unaffected_usable_slice": "all unconditional/bound items and fixture-native value mapping",
            "owner_and_next_step": "R157_AFRO_LANE -> exact route packet if route-dependent operations are required",
            "status": "HELD_ROUTING_EXPRESSION", "resolution_evidence": None,
        })
    ledger_entries.append({
        "residual_id": "WEIGHTS_SOURCE_NATIVE_ONLY", "source_id": sid,
        "required_native_field": "weight_slots", "current_value": "SOURCE_NATIVE_ONLY",
        "exact_evidence_refs": [{"field": "PHYSICAL_SLOTS.jsonl.gz", "weight_names": [x["source_variable_code"] for x in bound_weight]}],
        "missing_fact": "No population/estimand authority is claimed; weight slots are source-native measures.",
        "affected_operation_or_slice": "weighted population inference",
        "unaffected_usable_slice": "raw/unweighted full configuration",
        "owner_and_next_step": "P4 weighted scope only if warranted by authority",
        "status": "NOT_A_RAW_SCOPE_BLOCKER", "resolution_evidence": None,
    })
    ledger_entries.append({
        "residual_id": "READER_ENCODING_NOT_OVERRIDDEN", "source_id": sid,
        "required_native_field": "identity.reader.encoding", "current_value": "null",
        "exact_evidence_refs": [{"field": "SOURCE_ROSTER.json", "source_id": sid,
                                 "decoder_allowlist_encoding": roster["reader"]["decoder_allowlist_encoding"]}],
        "missing_fact": "No exact decoder allowlist encoding is configured for this SHA; no encoding override is guessed.",
        "affected_operation_or_slice": "source text decode",
        "unaffected_usable_slice": "numeric/metadata and fixture-native configuration",
        "owner_and_next_step": "qualified reader lane only if exact allowlist evidence arises",
        "status": "NOT_OVERRIDDEN", "resolution_evidence": None,
    })
    all_unmatched = list(roster.get("unmatched_relation_ids", []))
    held_unmatched = {e["item"]["implementation_id"] for e in held_by_cat.get("held_unmatched_relation", [])}
    key_unmatched = [x for x in all_unmatched if x not in held_unmatched]
    if key_unmatched:
        key_ids = []
        slot_ordinals = []
        for implementation_id in key_unmatched:
            item = next(x for x in items if x["implementation_id"] == implementation_id)
            key_ids.append(implementation_id)
            slot_ordinals.append(by_name[item["source_variable_code"]]["ordinal"])
        ledger_entries.append({
            "residual_id": "UNMATCHED_RELATION_KEY", "source_id": sid,
            "implementation_ids": key_ids, "physical_slot_ordinals": slot_ordinals,
            "count": len(key_ids), "required_native_field": "full-relation row",
            "current_value": "KEY_ONLY_EXACT_UNMATCHED",
            "exact_evidence_refs": [{"field": "SOURCE_ROSTER.json", "unmatched_relation_ids": key_ids}],
            "missing_fact": "The exact implementation ID has no full-relation row; physical key identity remains available.",
            "affected_operation_or_slice": "semantic response binding for the key item",
            "unaffected_usable_slice": "key/value identity and full configuration accounting",
            "owner_and_next_step": "R157_AFRO_LANE -> exact source relation evidence if semantic use is required",
            "status": "KEY_ONLY_EXACT_UNMATCHED", "resolution_evidence": None,
        })
    full_native = {
        "schema": "PYAT_R157_AFRO_FULL_NATIVE_RESULTS@1.0.0", "source_id": sid,
        "config_path": str(full_config_path.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(original_config),
        "fixture_config_path": str(full_fixture_config_path.relative_to(ROOT)),
        "fixture_config_sha256": canonical_config_hash(fixture_config),
        "fixture_path": str(full_fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": hashlib.sha256(full_fixture_path.read_bytes()).hexdigest(),
        "fixture_source_sha256": fixture_sha,
        "original_schema_valid": True,
        "original_native_validation": "NOT_RUN__AUTHORITY_DEFER",
        "full_fixture_native_validation": {
            "release_type": type(release).__name__, "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "m01_m18_coverage": {k: list(v) for k, v in release.m01_m18_coverage.items()},
            "response_event_count": len(events),
            "coordinate_fact_count": sum(1 for x in release.public_objects if type(x).__name__ == "EmpiricalCoordinateFact"),
            "routing_fact_count": sum(1 for x in release.public_objects if type(x).__name__ == "RoutingEligibilityFact"),
            "weight_fact_count": sum(1 for x in release.public_objects if type(x).__name__ == "WeightMeasureFact"),
            "response_state_counts": actual_state_counts,
            "expected_pairs_sha256": fixture_doc["expected_results"]["expected_pairs_sha256"],
            "key_count": len(keys),
            "repository_type": type(repository).__name__,
            "repository_release_matches": repository_release.release_ref == release.release_ref,
            "expected_match": True,
        },
        "reader": {"encoding": original_reader.encoding, "authority_status": original_reader.authority_status,
                   "source_read_performed": False},
        "native_calls": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "rawlsing_next.source_configuration.factory.row_native_keys_from_transport",
            "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "rawlsing_next.source_configuration.reader.source_read_request_from_config",
        ],
        "artifact_commit": artifact_commit, "limits": ["Original authority DEFER; no original native acceptance claim.",
                                                       "Fixture authority is nonrespondent only.",
                                                       "No original respondent rows or original source bytes read.",
                                                       "No original workload issued."],
    }
    write_json(val_dir / "EVIDENCE_ACCOUNTING.json", accounting)
    write_json(val_dir / "EXCEPTION_LEDGER.json", {"schema": "PYAT_R157_AFRO_FULL_EXCEPTION_LEDGER@1.0.0",
                                                   "source_id": sid, "entries": ledger_entries})
    write_json(full_native_path, full_native)
    return {
        "source_id": sid, "config_path": str(full_config_path.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(original_config),
        "fixture_config_path": str(full_fixture_config_path.relative_to(ROOT)),
        "fixture_config_sha256": canonical_config_hash(fixture_config),
        "fixture_path": str(full_fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": hashlib.sha256(full_fixture_path.read_bytes()).hexdigest(),
        "fixture_source_sha256": fixture_sha, "full_release_ref": release.release_ref.as_dict(),
        "full_response_events": len(events),
        "full_coordinate_facts": full_native["full_fixture_native_validation"]["coordinate_fact_count"],
        "full_routing_facts": full_native["full_fixture_native_validation"]["routing_fact_count"],
        "full_weight_facts": full_native["full_fixture_native_validation"]["weight_fact_count"],
        "response_items": len(bound_response), "coordinate_items": len(bound_coord),
        "weight_items": len(bound_weight), "held_items": len(held),
        "held_by_category": {cat: len(v) for cat, v in held_by_cat.items()},
        "unmatched_relation_ids": len(all_unmatched),
        "conditional_items": len(conditional), "key_count": len(keys),
        "full_native_results_path": str(full_native_path.relative_to(ROOT)),
        "accounting_path": str((val_dir / "EVIDENCE_ACCOUNTING.json").relative_to(ROOT)),
        "ledger_path": str((val_dir / "EXCEPTION_LEDGER.json").relative_to(ROOT)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args()
    artifact_commit = args.artifact_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    summaries = [build_full_one(sid, artifact_commit=artifact_commit) for sid in SOURCES]
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "rawlsing_next/tests/test_source_configuration_foundation.py",
         "rawlsing_next/tests/test_source_configuration_p3.py", "-k", "not r154",
         "-q", "-o", "addopts="],
        cwd=ROOT, env={**__import__("os").environ, "PYTHONPATH": str(ROOT)}, text=True, capture_output=True)
    tail = (tests.stdout.strip().splitlines() or [""])[-1]
    if tests.returncode != 0:
        raise SystemExit(f"shared contract tests failed: {tail}\n{tests.stdout}")
    artifact_paths = []
    for sid in SOURCES:
        for root in (DATA / sid, VALIDATION / sid):
            for path in root.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.name != "LANE_RETURN.json":
                    artifact_paths.append(path)
    changed_artifacts = [{
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    } for path in sorted(set(artifact_paths))]
    lane = {
        "schema": "PYAT_R157_AFRO_LANE_RETURN@2.0.0",
        "lane_id": "AFRO", "status": "LANE_COMPLETE__FULL_AVAILABLE_CONFIGURATION_WITH_EXACT_HELD_PREMISES",
        "branch": "agent/pyat-pre553-r157-afro", "artifact_commit": artifact_commit,
        "base_p0_tip": "d8d7087a8e56c24042bf5945fea1c97eb0d6c710",
        "base_p3_tip": "519355ec2215409b40d566ef13c3b21f611e0726",
        "source_ids": list(SOURCES), "sources": summaries,
        "source_manifests": {
            sid: {"config": f"rawlsing_next/source_configuration/data/{sid}/{sid}.config.json",
                  "full_fixture_config": f"rawlsing_next/source_configuration/data/{sid}/{sid}.full.fixture.config.json",
                  "full_fixture": f"source_pre553_validation/{sid}/{sid}.full.fixture.json",
                  "full_native_results": f"source_pre553_validation/{sid}/FULL_NATIVE_RESULTS.json",
                  "evidence_accounting": f"source_pre553_validation/{sid}/EVIDENCE_ACCOUNTING.json",
                  "exception_ledger": f"source_pre553_validation/{sid}/EXCEPTION_LEDGER.json"} for sid in SOURCES},
        "commands": ["PYTHONPATH=. python3 source_pre553_validation/SRC01/build_afro_full.py",
                     "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -k 'not r154' -q -o addopts=''"],
        "tests": {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -k 'not r154' -q -o addopts=''",
                  "result": tail, "passed": tests.returncode == 0, "skipped": "skipped" in tail,
                  "deselected_note": "Two legacy R154 loader tests are deselected; their runtime file is absent from this sparse AFRO checkout and they are outside the AFRO source-configuration boundary."},
        "native_positives": {x["source_id"]: {
            "full_release_ref": x["full_release_ref"], "full_response_events": x["full_response_events"],
            "full_coordinate_facts": x["full_coordinate_facts"], "full_routing_facts": x["full_routing_facts"],
            "full_weight_facts": x["full_weight_facts"], "key_count": x["key_count"]} for x in summaries},
        "changed_artifacts": changed_artifacts,
        "changed_artifacts_note": "LANE_RETURN.json excludes itself; the final commit hash is reported in the terminal receipt.",
        "native_api_calls": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "rawlsing_next.source_configuration.factory.row_native_keys_from_transport",
            "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "rawlsing_next.source_configuration.reader.source_read_request_from_config",
            "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
        ],
        "no_drop": {"sources": len(SOURCES),
                    "physical_slots": sum(x["response_items"] + x["coordinate_items"] + x["weight_items"] + 1 + x["held_items"] for x in summaries),
                    "items": sum(x["response_items"] + x["coordinate_items"] + x["weight_items"] + 1 + x["held_items"] for x in summaries),
                    "response_items": sum(x["response_items"] for x in summaries),
                    "coordinate_items": sum(x["coordinate_items"] for x in summaries),
                    "weight_items": sum(x["weight_items"] for x in summaries),
                    "held_items": sum(x["held_items"] for x in summaries),
                    "held_by_category": {cat: sum(x["held_by_category"].get(cat, 0) for x in summaries)
                                         for cat in sorted({c for x in summaries for c in x["held_by_category"]})},
                    "conditional_routing_items": sum(x["conditional_items"] for x in summaries),
                    "unmatched_relation_ids": sum(x["unmatched_relation_ids"] for x in summaries)},
        "blockers": [
            {"id": "ORIGINAL_AUTHORITY_DEFER", "status": "HELD_NON_BLOCKING",
             "reason": "Original AFRO authority is DEFER; full configuration and fixture-native validation are complete.",
             "owner_and_next_step": "integration supplies exact source authority if original native validation is requested."},
            {"id": "HELD_EXACT_PREMISES", "status": "HELD_EXACT",
             "reason": "Held items are exact generation-forbidden/unknown/ranked/blocked premises, not generic unselected items.",
             "owner_and_next_step": "see per-source exception ledgers; continue unaffected full library."},
            {"id": "ROUTING_EXPRESSION_UNAVAILABLE", "status": "HELD_EXACT",
             "reason": "Conditional/unknown routing items carry typed unknown states; eligibility is not asserted.",
             "owner_and_next_step": "exact route packet required only for route-dependent operations."},
        ],
        "scope_limits": ["Original authority DEFER; original-source native validation/execution not claimed.",
                         "Fixture authority NONRESPONDENT_FIXTURE_ONLY; fixture SHA is not original identity.",
                         "No original respondent rows or source bytes read; no original workload issued.",
                         "Weights are source-native only; no population/estimand claim.",
                         "Held items are exact source-premise residuals, not generic P4 deferrals."],
        "next_integration_edge": "HQ/P4: consume full source configs, full-shape fixture positives and exact held ledgers; supply original authority only if original native validation is requested.",
    }
    lane_path = VALIDATION / "SRC01" / "LANE_RETURN.json"
    write_json(lane_path, lane)
    print(json.dumps({"artifact_commit": artifact_commit, "tests": tail, "lane_return": str(lane_path),
                      "full_releases": {x["source_id"]: x["full_release_ref"]["content_hash"] for x in summaries}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
