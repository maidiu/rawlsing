"""Build full R157 ARAB source configurations and nonrespondent fixtures.

All 33-name-set sources here have exact one-to-one physical/codebook/item names.
The builder binds every finite categorical item as a source-native response,
admin/continuous context as coordinates, and records exact native-field
limitations for weight and continuous list-experiment items.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from rawlsing_next.source_configuration import evidence as E  # noqa: E402

DATA_ROOT = ROOT / "rawlsing_next/source_configuration/data"
VAL_ROOT = ROOT / "source_pre553_validation"
SOURCE_IDS = ("SRC04", "SRC05", "SRC06", "SRC07")
FIXTURE_ROWS = 8


def sha_material(material: Any) -> str:
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def exact_ref(kind: str, object_id: str, content_hash: str) -> dict[str, str]:
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def authority_ref(a: Mapping[str, Any]) -> dict[str, str]:
    return {"authority_id": a["authority_id"], "authority_version": a["authority_version"],
            "authority_content_hash": a["authority_content_hash"]}


def label_key(value: Any) -> str:
    text = str(value or "").casefold().strip()
    for mark in ("´", "`", "’", "‘"):
        text = text.replace(mark, "'")
    return re.sub(r"\s+", " ", text)


def response_state(label: Any) -> str:
    text = label_key(label)
    if "not asked" in text:
        return "NOT_ASKED"
    if "not applicable" in text or text in {"iap", "inapplicable"}:
        return "INAPPLICABLE"
    dk = any(x in text for x in ("don't know", "dont know", "does not know", "no sabe", "not clear"))
    na = any(x in text for x in ("no answer", "does not answer", "no responde", "refus", "declined", "not answer"))
    if dk and na:
        return "SOURCE_SPECIFIC_SPECIAL"
    if na:
        return "REFUSAL"
    if dk:
        return "DK"
    if "missing" in text or "unknown" in text or "not provided" in text or "not usable" in text:
        return "MISSING"
    if text in {"none", "ninguno", "ninguna"}:
        return "SOURCE_SPECIFIC_SPECIAL"
    return "SUBSTANTIVE_RESPONSE"


def canonical_token(code: int) -> str:
    return str(int(code))


def code_labels(slot: Mapping[str, Any]) -> list[tuple[int, str]]:
    out = []
    for key, label in (slot.get("value_labels") or {}).items():
        try:
            out.append((int(float(key)), str(label)))
        except (TypeError, ValueError):
            pass
    return sorted(out)


def is_binary_codes(slot: Mapping[str, Any]) -> bool:
    codes = {c for c, label in code_labels(slot) if response_state(label) == "SUBSTANTIVE_RESPONSE"}
    return bool(codes) and codes <= {0, 1}


def topology_kind(topology: str, slot: Mapping[str, Any]) -> str:
    if topology == "multiselect":
        return "MULTISELECT_INDICATOR" if is_binary_codes(slot) else "MULTISELECT_SINGLE_COLUMN"
    return {
        "scalar": "SCALAR",
        "binary_factual": "BINARY_FACTUAL",
        "binary_contrast": "BINARY_CONTRAST",
        "ordinal_context": "ORDINAL_CONTEXT",
        "nominal_choice": "NOMINAL_CHOICE",
        "ranked_choice": "RANKED_CHOICE",
    }.get(topology, "SCALAR")


def value_rule(slot: Mapping[str, Any], code: int | None, label: str | None, kind: str,
               mapping_authority: Mapping[str, str]) -> dict[str, Any]:
    if code is None:
        missing_state = "SYSTEM_MISSING"
        state = "MISSING"
        raw_value = None
        canonical = None
    else:
        missing_state = "OBSERVED_STORAGE_VALUE"
        state = response_state(label)
        raw_value = float(code)
        canonical = canonical_token(code) if state == "SUBSTANTIVE_RESPONSE" else None
    occurrence = {
        "key": "0",
        "topology_ref": exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:topology:{slot['source_id']}:{slot['name']}:{kind}",
            sha_material({"source": slot["source_id"], "slot": slot["name"], "kind": kind})),
        "multiplicity_order_rank_fields": {"kind": kind, "index": 0},
    }
    return {
        "raw_value": raw_value,
        "missing_state": missing_state,
        "source_missing_declaration": None,
        "response_state": state,
        "occurrences": [occurrence],
        "canonical_value": canonical,
        "transform_authority_ref": mapping_authority if canonical is not None else None,
        "extra_authority_refs": [],
    }


def slot_values(slot: Mapping[str, Any], kind: str, mapping_authority: Mapping[str, str]) -> list[dict[str, Any]]:
    values = [value_rule(slot, code, label, kind, mapping_authority) for code, label in code_labels(slot)]
    values.append(value_rule(slot, None, None, kind, mapping_authority))
    return values


def missing_declaration(slot: Mapping[str, Any]) -> Mapping[str, Any] | None:
    out = {}
    if slot.get("missing_ranges") is not None:
        out["ranges"] = slot["missing_ranges"]
    if slot.get("missing_user_values") is not None:
        out["user_values"] = slot["missing_user_values"]
    return out or None


def physical_slot_doc(p: Mapping[str, Any], disposition: str, reason: str) -> dict[str, Any]:
    cbm = p["codebook_mapping"]
    return {
        "ordinal": p["ordinal"], "name": p["name"], "label": p["label"],
        "storage_type": p["readstat_type"], "original_type": p["original_type"],
        "storage_width": p["storage_width"], "measure": p["measure"],
        "value_labels": p["value_labels"], "missing_declarations": missing_declaration(p),
        "mr_declarations": None,
        "codebook_mapping": {"var_name": cbm["var_name"], "row_hash": cbm["row_hash"], "status": cbm["status"]},
        "disposition": disposition, "disposition_reason": reason,
    }


def item_doc(x: Mapping[str, Any]) -> dict[str, Any]:
    relation = x.get("relation") or {}
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
    refs = [
        exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
        exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
        exact_ref("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{relation['question_id']}",
                  relation["governed_row_payload_hash"]),
    ]
    return {
        "implementation_id": x["implementation_id"],
        "source_variable_code": x["source_variable_code"],
        "exact_identity_sha256": x["exact_identity_sha256"],
        "question_text": x["p2"]["question_text"],
        "disposition": x["h48"]["disposition"],
        "response_classes": x["p2"]["response_classes"],
        "mapping_status": rel["mapping_status"],
        "authority_status": relation["authority_status"],
        "evidence_refs": refs,
        "limits": [
            f"relation_use_status_final={relation.get('relation_use_status_final') or 'NOT_RECORDED'}",
            f"mapping_status={rel['mapping_status']}",
            f"manual_signed_polarity_status={relation['manual_signed_polarity_status']}",
            f"forbidden_inference={relation['forbidden_inference'] or 'none recorded'}",
            f"does_not_measure={relation['does_not_measure'] or 'none recorded'}",
        ],
        "relation": rel,
    }


def authority(source_id: str, source_sha: str, kind: str, state: str, operation: str,
              grade: str, families: list[str], scope_extra: Mapping[str, Any],
              fixture_id: str | None) -> dict[str, Any]:
    scope: dict[str, Any] = {
        "fixture_only": fixture_id is not None,
        "grade": grade,
        "source_id": source_id,
        "source_sha256": source_sha,
        **scope_extra,
    }
    if fixture_id:
        scope["fixture_id"] = fixture_id
        scope["original_source_sha256"] = source_sha
    else:
        scope["execution_grant"] = "NOT_ISSUED_UNDER_R157_PREPARATION"
    material = {
        "authority_id": f"R157-{source_id}-{operation}",
        "authority_version": "1.0.0",
        "authority_kind": kind,
        "decision_state": state,
        "scope_envelope": scope,
        "governed_operations": [operation],
        "governed_object_families": families,
    }
    ch = sha_material(material)
    return {
        "typed_state": state, "authority_snapshot_refs": [], "dependency_refs": [],
        "producer_replay_locator_or_reference_root": exact_ref(
            "REPLAY_ROOT", f"urn:rawlsing:r157:authority:{source_id}:{operation}", sha_material({"root": material})),
        "authority_id": material["authority_id"], "authority_version": "1.0.0",
        "authority_content_hash": ch, "authority_kind": kind, "decision_state": state,
        "governed_operations": [operation], "governed_object_families": families,
        "scope_envelope": scope,
        "effective_time_or_interval": "R157_NONRESPONDENT_FIXTURE" if fixture_id else "R157_PREPARATION",
        "parent_authority_refs": [], "negative_limit_refs": [], "supersession_refs": [],
        "interpretation_semantics_fingerprint": sha_material({"scope": scope, "operation": operation}),
        "replay_protocol_ref": exact_ref(
            "REPLAY_PROTOCOL", f"urn:rawlsing:r157:replay:{source_id}",
            sha_material({"operation": operation, "source": source_id, "fixture": fixture_id})),
    }


def build_authorities(source_id: str, source_sha: str, fixture_id: str | None, wave: str) -> dict[str, dict[str, Any]]:
    state = "ALLOW" if fixture_id else "DEFER"
    grade = "NONRESPONDENT_FIXTURE_ONLY" if fixture_id else "SOURCE_NATIVE_REPRESENTATION_PREPARATION"
    common = {"wave": wave}
    specs = [
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_ITEM_SEMANTICS", grade,
         ["RespondentEvent@1.0.0"],
         {"semantic_scope": "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY",
          "direction_status": "NOT_CERTIFIED_BY_THIS_AUTHORITY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_TOPOLOGY", grade,
         ["RespondentEvent@1.0.0"],
         {"topology_scope": "EXACT_SOURCE_VALUE_LABELS_AND_H48_TOPOLOGY_ONLY", **common}),
        ("NATIVE_CANONICAL_MAPPING_HARMONIZATION", state, "R157_MAP_SOURCE_CODE_TOKEN_IDENTITY", grade,
         ["RespondentEvent@1.0.0"],
         {"mapping_scope": "EXACT_SOURCE_NATIVE_CODE_TOKEN_IDENTITY_ONLY_NO_SIGNED_DIRECTION", **common}),
        ("COORDINATE_SEMANTICS", state, "R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW", grade,
         ["EmpiricalCoordinateFact@1.0.0"],
         {"coordinate_scope": "COPY_OBSERVED_RAW_NO_CANONICAL_CROSSWALK", **common}),
        ("ROUTING_RISK_SET", state, "R157_RECORD_UNRESOLVED_SOURCE_ROUTING", grade,
         ["RoutingEligibilityFact@1.0.0"],
         {"routing_scope": "SOURCE_ROUTING_UNRESOLVED_NO_ELIGIBILITY_CLAIM", **common}),
        ("REPLAY_PROTOCOL", "ALLOW", "R157_LOCAL_DETERMINISTIC_REPLAY",
         "NONRESPONDENT_FIXTURE_ONLY" if fixture_id else "R157_DETERMINISTIC_REPLAY_PROTOCOL",
         ["ReplayReceipt@1.0.0"], {"replay_scope": "R157_LOCAL_ENGINEERING_ONLY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_PROJECTION", grade,
         ["EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
          "RoutingEligibilityFact@1.0.0"],
         {"projection_scope": "FULL_DECLARED_SOURCE_SLICE", **common}),
    ]
    out = {}
    for kind, st, op, gr, fams, extra in specs:
        out[op] = authority(source_id, source_sha, kind, st, op, gr, fams, extra, fixture_id)
    return out


def make_universe(source_id: str, roster: Mapping[str, Any], auths: Mapping[str, Mapping[str, Any]],
                  fixture_id: str | None, wave: str) -> tuple[dict[str, Any], dict[str, str]]:
    from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse
    semantic = authority_ref(auths["R157_PREPARE_SOURCE_ITEM_SEMANTICS"])
    if fixture_id:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED", "authority_snapshot_refs": [semantic],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": exact_ref(
                "REPLAY_ROOT", f"urn:rawlsing:r157:universe:{source_id}:fixture",
                sha_material({"source": source_id, "fixture": fixture_id})),
            "raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:{source_id}",
            "source_family": roster["family"], "study_product_release": f"R157_FIXTURE/{source_id}",
            "instrument_release": f"R157_FIXTURE_INSTRUMENT/{source_id}",
            "country_geography": "FIXTURE_MULTI_COUNTRY", "sampling_geography": "FIXTURE_NONPROBABILITY",
            "raw_wave": wave, "canonical_wave_if_governed": None,
            "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
            "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
            "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
            "respondent_namespace": f"urn:rawlsing:r157:fixture:{source_id}",
            "source_artifact_import_lineage": "R157_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE",
            "harmonization_authority_ref": None, "source_relation_refs": [],
        }
    else:
        payload = {
            "typed_state": "UNIVERSE_IDENTIFIED", "authority_snapshot_refs": [semantic],
            "dependency_refs": [],
            "producer_replay_locator_or_reference_root": exact_ref(
                "REPLAY_ROOT", f"urn:rawlsing:r157:universe:{source_id}",
                sha_material({"source": source_id, "sha": roster["source_sha256"]})),
            "raw_source_identity": f"{roster['family']} {roster['wave']} / {source_id}",
            "source_family": roster["family"], "study_product_release": f"{roster['family']}:{roster['wave']}",
            "instrument_release": f"{source_id}_INSTRUMENT_ARAB_BAROMETER_{roster['wave']}",
            "country_geography": "SOURCE_OBSERVED_COUNTRY_CODES",
            "sampling_geography": "UNKNOWN_SOURCE_SAMPLING_GEOGRAPHY_R157_PREPARATION",
            "raw_wave": wave, "canonical_wave_if_governed": None,
            "field_or_reference_time": wave,
            "target_population_and_sample_frame": "UNKNOWN_SOURCE_SAMPLE_FRAME_R157_PREPARATION",
            "sampling_design_regime": "UNKNOWN_SOURCE_DESIGN_R157_PREPARATION",
            "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
            "source_artifact_import_lineage": f"R154_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
            "harmonization_authority_ref": None, "source_relation_refs": [],
        }
    return payload, EmpiricalUniverse(**payload).ref.as_dict()


def classify(source_id: str, items: list[Mapping[str, Any]], phys_by_name: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    responses: list[dict[str, Any]] = []
    coordinates: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for x in items:
        code = x["source_variable_code"]
        p = phys_by_name[code]
        relation = x.get("relation") or {}
        topology = relation.get("manual_response_topology")
        disposition = x["h48"]["disposition"]
        binding = x["p2"].get("response_binding_status")
        labels = p.get("value_labels") or {}
        is_weight = code.casefold() == "wt" or "weight" in (p.get("label") or "").casefold()
        if is_weight:
            excluded.append({
                "item_code": code, "slot": p["name"], "reason": "WEIGHT_AUTHORITY_NOT_ESTABLISHED",
                "native_field": "weight_slots[].design_authority_ref / estimand_authority_ref",
                "evidence": "The source carries a weight slot, but current evidence has no exact weight design, estimand or effective-scope authority.",
                "dependent_operation": "weighted/population estimation",
            })
            continue
        if disposition == "admin" or topology == "administrative":
            coordinates.append({"item_code": code, "slot": p["name"],
                                "mode": "values" if any(response_state(l) == "SUBSTANTIVE_RESPONSE" for l in labels.values()) else "raw",
                                "unit": "SOURCE_NATIVE_ADMIN_CONTEXT",
                                "note": "Source-native administrative/context field bound as a coordinate."})
            continue
        if topology == "continuous_numeric":
            if disposition in {"demographic_material_or_behavioral_context", "behavioral_or_demographic_context",
                               "behavior_exposure_context", "admin"}:
                coordinates.append({"item_code": code, "slot": p["name"], "mode": "raw",
                                    "unit": "SOURCE_NATIVE_CONTINUOUS_CONTEXT",
                                    "note": "Continuous source-native context bound as a raw coordinate; no categorical default."})
            else:
                excluded.append({
                    "item_code": code, "slot": p["name"],
                    "reason": "CONTINUOUS_MEASUREMENT_NO_FINITE_NATIVE_DOMAIN",
                    "native_field": "response_slots[].values (ResponseValueRule.physical_key)",
                    "evidence": "Continuous/list-experiment count field has no declared finite value-label domain; original values were not read, so no non-invented finite response rules exist.",
                    "dependent_operation": "finite categorical native response construction",
                })
            continue
        if not labels:
            excluded.append({
                "item_code": code, "slot": p["name"], "reason": "NO_DECLARED_FINITE_VALUE_DOMAIN",
                "native_field": "response_slots[].values (ResponseValueRule.physical_key)",
                "evidence": "The mapped physical slot has no declared value labels.",
                "dependent_operation": "finite categorical native response construction",
            })
            continue
        if binding != "bound":
            excluded.append({
                "item_code": code, "slot": p["name"], "reason": "RESPONSE_BINDING_BLOCKED",
                "native_field": "response_slots[].values / response binding",
                "evidence": f"P2 response_binding_status={binding!r}; prior authority gap blocks a native response binding.",
                "dependent_operation": "source-native response construction",
            })
            continue
        if topology is None:
            excluded.append({
                "item_code": code, "slot": p["name"], "reason": "TOPOLOGY_UNRESOLVED",
                "native_field": "response_slots[].occurrences / multiplicity_order_rank_fields",
                "evidence": "No exact manual/P2 response topology is recorded.",
                "dependent_operation": "native response topology construction",
            })
            continue
        responses.append({"question_id": code, "item_code": code, "slot": p["name"],
                          "topology": topology, "kind": topology_kind(topology, p)})
    included_slots = {r["slot"] for r in responses} | {c["slot"] for c in coordinates}
    excluded_slots = {e["slot"] for e in excluded}
    if included_slots & excluded_slots:
        raise RuntimeError(f"{source_id}: slot both included/excluded")
    if included_slots | excluded_slots != set(phys_by_name):
        raise RuntimeError(f"{source_id}: physical partition incomplete")
    included_items = {r["item_code"] for r in responses} | {c["item_code"] for c in coordinates}
    excluded_items = {e["item_code"] for e in excluded}
    if included_items & excluded_items:
        raise RuntimeError(f"{source_id}: item both included/excluded")
    if included_items | excluded_items != {x["source_variable_code"] for x in items}:
        raise RuntimeError(f"{source_id}: item partition incomplete")
    return {"responses": responses, "coordinates": coordinates, "excluded": excluded,
            "included_slots": included_slots, "excluded_slots": excluded_slots,
            "included_items": included_items, "excluded_items": excluded_items}


def coordinate_values(slot: Mapping[str, Any]) -> list[dict[str, Any]]:
    out = []
    for code, label in code_labels(slot):
        state = response_state(label)
        cstate = ("OBSERVED_COORDINATE" if state == "SUBSTANTIVE_RESPONSE"
                  else "MISSING" if state == "MISSING" else "UNKNOWN")
        out.append({"raw_value": float(code), "missing_state": "OBSERVED_STORAGE_VALUE",
                    "source_missing_declaration": None, "coordinate_state": cstate,
                    "canonical_value": None, "extra_authority_refs": []})
    out.append({"raw_value": None, "missing_state": "SYSTEM_MISSING",
                "source_missing_declaration": None, "coordinate_state": "MISSING",
                "canonical_value": None, "extra_authority_refs": []})
    return out


def build_residuals(source_id: str, plan: Mapping[str, Any], mode: str) -> list[dict[str, str]]:
    if mode == "fixture":
        return [{"residual_id": f"{source_id}-FIXTURE-ONLY-AUTHORITY", "scope": source_id,
                 "field": "authority.snapshots", "status": "FIXTURE_ONLY",
                 "reason": "Fixture proves native construction but does not establish original-source authority.",
                 "dependent_operation": "original-source execution and scientific interpretation",
                 "unaffected_scope": "nonrespondent fixture native C11 validation",
                 "owner": "ARAB lane / P3 integration owner",
                 "next_step": "Keep fixture authority separate from the ORIGINAL_SOURCE config."}]
    out = [
        {"residual_id": f"{source_id}-ROUTING-UNRESOLVED", "scope": source_id,
         "field": "routing.typed_state", "status": "UNKNOWN",
         "reason": f"SOURCE_ROUTING_UNRESOLVED for {len(plan['responses'])} response items. The portable recipe declares row_selector=ALL with typed_state ROUTING_UNKNOWN for every produced routing fact; it does not invent eligibility, forms, populations or permissions. Original rows were not physically expanded for validation.",
         "dependent_operation": "eligibility/form-conditioned native query",
         "unaffected_scope": "unconditional source-native response incidence and coordinate binding",
         "owner": "ARAB lane / P3 integration owner",
         "next_step": "Recover exact indexed routing/form expressions before claiming eligibility-conditioned scope."},
        {"residual_id": f"{source_id}-ROW-NATIVE-KEY", "scope": source_id,
         "field": "respondents.source_native_key_slot", "status": "UNKNOWN",
         "reason": "No exact decoded source-native respondent key witness exists in preparation; physical row ordinal is the only established key.",
         "dependent_operation": "respondent-key linkage beyond row ordinal",
         "unaffected_scope": "row-ordinal-scoped source-native construction",
         "owner": "ARAB lane / P3 integration owner",
         "next_step": "Supply exact row_native_keys only after a separately permitted decode."},
        {"residual_id": f"{source_id}-FORM-ADMIN", "scope": source_id,
         "field": "supported_scope.supported_form_slice", "status": "UNKNOWN",
         "reason": "Current physical/codebook evidence contains no form, ballot or administration variable; single-file SAV shape is established.",
         "dependent_operation": "form-conditioned or administration-conditioned native query",
         "unaffected_scope": "source-native response incidence without form conditioning",
         "owner": "ARAB lane / P3 integration owner",
         "next_step": "Acquire exact source form/administration evidence before claiming a form-conditioned slice."},
        {"residual_id": f"{source_id}-WEIGHT-AUTHORITY", "scope": source_id,
         "field": "weight_slots", "status": "NOT_DECLARED",
         "reason": "The source carries a weight slot, but no exact design/estimand authority or weighted scope is present in current evidence.",
         "dependent_operation": "population or weighted estimation",
         "unaffected_scope": "raw-sample source-native response incidence",
         "owner": "ARAB lane / P3 integration owner",
         "next_step": "Establish exact weight basis, design, estimand and effective scope before declaring a weighted slice."},
        {"residual_id": f"{source_id}-DIRECTION", "scope": source_id,
         "field": "items.relation.manual_signed_polarity_status", "status": "NOT_CERTIFIED_BY_THIS_PREPARATION",
         "reason": "Response states and exact source code tokens are bound, but this preparation does not issue a new signed-direction or canonical semantic certification.",
         "dependent_operation": "signed-direction empirical or structural analysis",
         "unaffected_scope": "source-native nominal/ordinal response incidence and exact value accounting",
         "owner": "ARAB lane / later scientific authority owner",
         "next_step": "Use the original relation certification only at its exact evidenced scope."},
        {"residual_id": f"{source_id}-ORIGINAL-EXECUTION", "scope": source_id,
         "field": "supported_scope.original_source_execution", "status": "NOT_PERFORMED",
         "reason": "Original respondent execution and original workload issuance are a separate permission boundary.",
         "dependent_operation": "original empirical execution",
         "unaffected_scope": "portable configuration and nonrespondent fixture native validation",
         "owner": "user-authorized execution owner",
         "next_step": "Issue a separate exact original-source execution grant and qualified reader binding."},
    ]
    for exc in plan["excluded"]:
        out.append({
            "residual_id": f"{source_id}-EXCLUDED-{exc['item_code']}",
            "scope": f"{source_id}/{exc['item_code']}",
            "field": exc["native_field"], "status": exc["reason"],
            "reason": exc["evidence"], "dependent_operation": exc["dependent_operation"],
            "unaffected_scope": "all other included source-native response/coordinate bindings",
            "owner": "ARAB lane / P3 integration owner",
            "next_step": "Preserve the exact limitation; acquire the named missing source/native fact before binding.",
        })
    return out


def build_config(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                 items: list[Mapping[str, Any]], plan: Mapping[str, Any], *,
                 mode: str, fixture_meta: Mapping[str, Any] | None, crosswalk_sha: str) -> dict[str, Any]:
    phys_by_name = {p["name"]: p for p in phys}
    item_by_code = {x["source_variable_code"]: x for x in items}
    source_sha = roster["source_sha256"]
    wave = str(roster["wave"])
    fixture_id = fixture_meta["fixture_id"] if fixture_meta else None
    auths = build_authorities(source_id, source_sha, fixture_id, wave)
    aref = {k: authority_ref(v) for k, v in auths.items()}
    universe_payload, universe_ref = make_universe(source_id, roster, auths, fixture_id, wave)
    identity_class = "ORIGINAL_SOURCE" if mode == "original" else "NONRESPONDENT_FIXTURE"
    binding_sha = source_sha if mode == "original" else fixture_meta["fixture_source_sha256"]
    binding_rows = roster["rows"] if mode == "original" else fixture_meta["row_count"]

    physical_docs = []
    for p in phys:
        if p["name"] in plan["included_slots"]:
            if any(r["slot"] == p["name"] for r in plan["responses"]):
                disp, reason = "SUPPORTED_RESPONSE", "Exact source-native response binding."
            else:
                disp, reason = "SUPPORTED_COORDINATE", "Source-native coordinate/context binding."
        else:
            exc = next(e for e in plan["excluded"] if e["slot"] == p["name"])
            disp, reason = "HELD_EXACT_SOURCE_LIMITATION", exc["evidence"]
        physical_docs.append(physical_slot_doc(p, disp, reason))
    if mode == "fixture":
        physical_docs = [d for d in physical_docs if d["name"] in plan["included_slots"]]

    item_docs = []
    for x in items:
        code = x["source_variable_code"]
        if code in plan["excluded_items"]:
            if mode == "fixture":
                continue
            exc = next(e for e in plan["excluded"] if e["item_code"] == code)
            doc = item_doc(x)
            doc["disposition"] = f"HELD_{exc['reason']}"
            doc["limits"] = list(doc["limits"]) + [exc["evidence"]]
            item_docs.append(doc)
            continue
        doc = item_doc(x)
        if any(code == r["item_code"] for r in plan["responses"]):
            doc["disposition"] = "SUPPORTED_SOURCE_NATIVE_RESPONSE"
        else:
            doc["disposition"] = "SUPPORTED_SOURCE_NATIVE_COORDINATE"
        doc["limits"] = list(doc["limits"]) + ["Included at its exact source-native representation scope."]
        item_docs.append(doc)

    questions = []
    for r in plan["responses"]:
        x = item_by_code[r["item_code"]]
        questions.append({
            "question_id": r["question_id"], "empirical_universe_ref": universe_ref,
            "native_question_ref": exact_ref(
                "NATIVE_QUESTION", f"urn:rawlsing:r157:{mode}:{source_id}:item:{x['implementation_id']}",
                x["exact_identity_sha256"]),
            "instrument_question_version": wave,
            "canonical_question_ref_or_typed_absence": {
                "typed_absence_state": "NOT_AUTHORIZED",
                "detail": "No canonical adoption or directional certification is issued by this source preparation."},
            "component_subitem_ref_or_typed_absence": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
            "semantic_authority_ref": aref["R157_PREPARE_SOURCE_ITEM_SEMANTICS"],
            "topology_authority_ref": aref["R157_PREPARE_SOURCE_TOPOLOGY"],
            "item_evidence": {"implementation_id": x["implementation_id"],
                              "exact_identity_sha256": x["exact_identity_sha256"],
                              "relation_join_status": x.get("relation_join_status")},
        })

    response_slots = []
    for r in plan["responses"]:
        p = phys_by_name[r["slot"]]
        response_slots.append({
            "slot": {"ordinal": p["ordinal"], "name": p["name"]},
            "question_id": r["question_id"],
            "values": slot_values(p, r["kind"], aref["R157_MAP_SOURCE_CODE_TOKEN_IDENTITY"]),
        })

    coordinate_slots = []
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        mode_values = c["mode"] == "values" and any(
            response_state(l) == "SUBSTANTIVE_RESPONSE" for l in (p.get("value_labels") or {}).values())
        coordinate_slots.append({
            "slot": {"ordinal": p["ordinal"], "name": p["name"]},
            "native_coordinate_ref": exact_ref(
                "COORDINATE_NATIVE", f"urn:rawlsing:r157:{mode}:{source_id}:{p['name']}",
                sha_material({"source": source_id, "slot": p["name"], "mode": mode})),
            "unit_taxonomy_ref": exact_ref(
                "UNIT_TAXONOMY", f"urn:rawlsing:r157:{c['unit']}", sha_material({"unit": c["unit"]})),
            "effective_time": wave,
            "source_semantic_authority_ref": aref["R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW"],
            "canonical_coordinate_ref": None, "normalization_ref": None,
            "values": coordinate_values(p) if mode_values else [],
            "copy_observed_raw": not mode_values,
        })

    routing = []
    for r in plan["responses"]:
        qid = r["question_id"]
        routing.append({
            "question_id": qid, "row_selector": "ALL", "typed_state": "ROUTING_UNKNOWN",
            "risk_set_ref": exact_ref("RISK_SET", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                                      sha_material({"s": source_id, "q": qid, "m": mode, "r": "risk"})),
            "routing_rule_ref": exact_ref("ROUTING_RULE", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                                          sha_material({"s": source_id, "q": qid, "m": mode, "r": "rule"})),
            "member_set_replay_ref": exact_ref("MEMBER_SET_REPLAY", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                                               sha_material({"s": source_id, "q": qid, "m": mode, "r": "member"})),
            "authority_ref": aref["R157_RECORD_UNRESOLVED_SOURCE_ROUTING"],
            "parent_predicate_refs": [], "dependency_refs": [],
        })

    included_ordinals = sorted(phys_by_name[n]["ordinal"] for n in plan["included_slots"])
    if mode == "original":
        excluded_slots = [
            {"ordinal": phys_by_name[n]["ordinal"], "name": n,
             "reason": next(e for e in plan["excluded"] if e["slot"] == n)["evidence"]}
            for n in sorted(plan["excluded_slots"], key=lambda n: phys_by_name[n]["ordinal"])]
        excluded_items = [
            {"implementation_id": item_by_code[c]["implementation_id"],
             "reason": next(e for e in plan["excluded"] if e["item_code"] == c)["evidence"]}
            for c in sorted(plan["excluded_items"])]
        coverage = {
            "physical_slots_total": roster["physical_columns"], "items_total": roster["original_items"],
            "physical_slots_included": included_ordinals,
            "physical_slots_excluded": excluded_slots,
            "items_included": sorted(item_by_code[c]["implementation_id"] for c in plan["included_items"]),
            "items_excluded": excluded_items,
            "partial_scope_reason": (
                "Every physical slot and original item is accounted. Included items have a lawful "
                "source-native response or coordinate binding; excluded items carry exact native-field "
                "and source-evidence limitations in residuals/EXCEPTIONS."),
        }
    else:
        coverage = {"physical_slots_total": roster["physical_columns"], "items_total": roster["original_items"],
                    "partial_scope_reason": "Nonrespondent fixture slice covering every declared supported response and coordinate slot.",
                    "not_a_lane_config": True}

    qids = [r["question_id"] for r in plan["responses"]]
    if mode == "original":
        supported_scope = {
            "scope_id": f"{source_id}-R157-FULL-SOURCE-NATIVE-CONFIGURATION",
            "purpose": "SOURCE_PREPARATION", "declared_supported": True,
            "supported_question_ids": qids, "native_validation_expectation": "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "SOURCE_INTERVIEW_ROW",
            "supported_form_slice": "SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE",
            "notes": [
                "All inclusive items are source-native response or coordinate bindings; exclusions are exact limitations.",
                "Positive native C11 release is exercised by the separately identified nonrespondent fixture config.",
                "Routing uses row_selector=ALL with ROUTING_UNKNOWN and is not physically expanded for original validation.",
            ],
        }
    else:
        supported_scope = {
            "scope_id": f"{source_id}-R157-NONRESPONDENT-FIXTURE-FULL-SLICE",
            "purpose": "NONRESPONDENT_FIXTURE_VALIDATION", "declared_supported": True,
            "supported_question_ids": qids, "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS",
            "supported_form_slice": "NONRESPONDENT_FIXTURE_ALL_SUPPORTED_SLOTS",
            "notes": ["Fixture-only authority; never original-source authority."],
        }

    residuals = build_residuals(source_id, plan, mode)
    metadata_ref = exact_ref("R154_PHYSICAL_METADATA",
                             f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                             roster["metadata_witness"]["sha256"])
    field_evidence = [
        {"field": "identity.expected_source_sha256",
         "refs": [exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)]},
        {"field": "identity.metadata_witness_ref", "refs": [metadata_ref]},
        {"field": "correspondence",
         "refs": [exact_ref("SOURCE_CORRESPONDENCE",
                            f"rawlsing_next/source_configuration/data/{source_id}/crosswalk.json", crosswalk_sha)]},
    ]
    for code in sorted(plan["included_items"]):
        x = item_by_code[code]
        refs = [exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
                exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
                exact_ref("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{x['relation']['question_id']}",
                          x["relation"]["governed_row_payload_hash"])]
        field_evidence.append({"field": f"items[{x['implementation_id']}]", "refs": refs})

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
        "limits": ["Prior H48/P2/full-relation evidence is reused with original grades and limits.",
                   "No original respondent rows, response values or source bytes were read.",
                   "Fixture authority is not original-source authority."],
    }

    authority_section = {
        "snapshots": [auths[k] for k in sorted(auths)],
        "required_refs": [aref[k] for k in sorted(aref)],
        "projection_authority_ref": aref["R157_PREPARE_SOURCE_PROJECTION"],
        "replay_authority_ref": aref["R157_LOCAL_DETERMINISTIC_REPLAY"],
        "projection_identity_ref": exact_ref(
            "C11_SEMANTIC_PROJECTION", f"urn:rawlsing:r157:{mode}:{source_id}:projection",
            sha_material({"source": source_id, "sha": source_sha, "mode": mode, "questions": qids})),
        "tie_order_ref": exact_ref("ORDER_RULE", "urn:rawlsing:r157:canonical-ref-sort",
                                   sha_material({"rule": "canonical_ref_sort"})),
        "replay_protocol_version": "1.0.0",
    }

    identity = {
        "source_id": source_id, "family": roster["family"], "wave": wave,
        "source_family_id": roster["family"], "study_product_id": f"{roster['family']}:{wave}",
        "release_id": f"{source_id}_ARAB_BAROMETER_{wave}_PREPARATION",
        "instrument_release_id": f"{source_id}_INSTRUMENT_ARAB_BAROMETER_{wave}",
        "source_artifact_id": roster["source_artifact_id"], "expected_source_sha256": source_sha,
        "source_format": roster["format"], "source_row_count": roster["rows"],
        "source_column_count": roster["physical_columns"], "source_bytes": roster["bytes"],
        "codebook_rows": roster["codebook_rows"], "original_item_count": roster["original_items"],
        "source_snapshot_retention_ref": exact_ref(
            "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
        "metadata_witness_ref": metadata_ref,
        "locator": {"root": "EXTERNAL_LOCATOR_ID",
                    "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
        "reader": {"decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                   "configuration_ref": exact_ref(
                       "READER_CONFIGURATION", f"urn:rawlsing:r157:{source_id}:default_sav",
                       sha_material({"source": source_id, "sha": source_sha, "reader": "default_sav"})),
                   "encoding": None},
    }

    if mode == "original":
        binding = {"identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
                   "source_snapshot_ref": exact_ref("SOURCE_SNAPSHOT",
                                                    f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)}
        respondents = {"subject_unit": "SOURCE_INTERVIEW_ROW",
                       "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
                       "respondent_key_pattern": f"{source_id}-ROW-{{row_ordinal:05d}}",
                       "source_native_key_slot": None, "identity_map_authority_ref": None,
                       "row_identity_grade": "SOURCE_PHYSICAL_ROW_ORDINAL_ONLY"}
        config_id = f"R157-ARAB-{source_id}-FULL-SOURCE-PREPARATION"
        purpose = "SOURCE_PREPARATION"
    else:
        binding = {"identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
                   "source_snapshot_ref": exact_ref("FIXTURE_SNAPSHOT",
                                                    f"urn:rawlsing:r157:fixture:{fixture_meta['fixture_id']}", binding_sha),
                   "fixture_provenance": {
                       "fixture_id": fixture_meta["fixture_id"], "provenance": fixture_meta["provenance"],
                       "authority_grade": "NONRESPONDENT_FIXTURE_ONLY", "original_source_id": source_id,
                       "original_source_sha256": source_sha, "no_original_respondents": True,
                       "fixture_study_product_id": fixture_meta["fixture_study_product_id"],
                       "fixture_release_id": fixture_meta["fixture_release_id"],
                       "fixture_instrument_release_id": fixture_meta["fixture_instrument_release_id"]}}
        respondents = {"subject_unit": "NONRESPONDENT_FIXTURE_ROW",
                       "respondent_namespace": f"urn:rawlsing:r157:fixture:{source_id}",
                       "respondent_key_pattern": f"FIXTURE-{source_id}-ROW-{{row_ordinal:03d}}",
                       "source_native_key_slot": None, "identity_map_authority_ref": None,
                       "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY"}
        config_id = f"R157-ARAB-{source_id}-NONRESPONDENT-FIXTURE"
        purpose = "NONRESPONDENT_FIXTURE"

    return {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id, "config_revision": 1, "config_purpose": purpose,
        "identity": identity, "binding": binding, "authority": authority_section,
        "universe": {"universes": [universe_payload]}, "respondents": respondents,
        "questions": questions, "physical_slots": physical_docs, "items": item_docs,
        "response_slots": response_slots, "coordinate_slots": coordinate_slots,
        "weight_slots": [], "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {"predicate": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
                   "comparator": {"typed_absence_state": "DEFERRED", "detail": None},
                   "discovery": {"typed_absence_state": "DEFERRED", "detail": None},
                   "structural": {"typed_absence_state": "NOT_APPLICABLE", "detail": None}},
        "supported_scope": supported_scope, "coverage": coverage, "residuals": residuals,
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


def build_fixture(source_id: str, phys_by_name: Mapping[str, Mapping[str, Any]],
                  plan: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = FIXTURE_ROWS
    cells = []
    oracle_slots: dict[str, dict[str, list[Any]]] = {}
    for r in plan["responses"]:
        p = phys_by_name[r["slot"]]
        codes = code_labels(p)
        substantive = [c for c, l in codes if response_state(l) == "SUBSTANTIVE_RESPONSE"]
        specials = [c for c, l in codes if response_state(l) != "SUBSTANTIVE_RESPONSE"]
        sequence = substantive + specials + [None]
        oracle_slots[r["slot"]] = {"states": [], "raw_values": [], "canonical_values": []}
        for row in range(1, rows + 1):
            code = sequence[(row - 1) % len(sequence)]
            label = dict(codes).get(code) if code is not None else None
            state = "MISSING" if code is None else response_state(label)
            canonical = canonical_token(code) if state == "SUBSTANTIVE_RESPONSE" else None
            cells.append({"row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                          "raw_value": None if code is None else float(code),
                          "missing_state": "SYSTEM_MISSING" if code is None else "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
            oracle_slots[r["slot"]]["states"].append(state)
            oracle_slots[r["slot"]]["raw_values"].append(None if code is None else float(code))
            oracle_slots[r["slot"]]["canonical_values"].append(canonical)
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        codes = code_labels(p)
        substantive = [code for code, label in codes if response_state(label) == "SUBSTANTIVE_RESPONSE"]
        for row in range(1, rows + 1):
            if c["mode"] == "values" and substantive:
                raw = float(substantive[(row - 1) % len(substantive)])
            else:
                raw = 1.0
            cells.append({"row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                          "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
    fixture_id = f"R157-ARAB-{source_id}-NONRESPONDENT"
    document = {"schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0", "fixture_id": fixture_id,
                "identity_class": "NONRESPONDENT_FIXTURE", "nonrespondent": True,
                "row_count": rows, "cells": cells}
    from rawlsing_next.source_configuration.fixture import fixture_document_sha256
    fixture_sha = fixture_document_sha256(document)
    document["fixture_source_sha256"] = fixture_sha
    state_counts: dict[str, int] = {}
    for data in oracle_slots.values():
        for state in data["states"]:
            state_counts[state] = state_counts.get(state, 0) + 1
    oracle = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_ORACLE@1.0.0",
        "fixture_id": fixture_id, "fixture_source_sha256": fixture_sha, "row_count": rows,
        "expected": {
            "response_event_count": rows * len(plan["responses"]),
            "coordinate_fact_count": rows * len(plan["coordinates"]),
            "routing_fact_count": rows * len(plan["responses"]),
            "response_states_by_slot": {k: v["states"] for k, v in oracle_slots.items()},
            "raw_values_by_slot": {k: v["raw_values"] for k, v in oracle_slots.items()},
            "canonical_values_by_slot": {k: v["canonical_values"] for k, v in oracle_slots.items()},
            "response_state_counts": state_counts,
            "weight_section": "NOT_APPLICABLE",
            "source_relation_section": "DISTINCT_BY_DEFAULT",
        },
        "oracle_basis": "Declared from fixture cells and serialized source-native value rules before the native call.",
    }
    return document, oracle


def build_crosswalk(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                    cb: list[Mapping[str, Any]]) -> dict[str, Any]:
    cb_by_name = {c["var_name"]: c for c in cb}
    entries = []
    c_entries = []
    for p in phys:
        c = cb_by_name[p["name"]]
        entries.append({"physical_ordinal": p["ordinal"], "physical_name": p["name"],
                        "physical_label": p["label"], "codebook_var_names": [c["var_name"]],
                        "codebook_row_index": c["row_index"], "codebook_row_hash": c["row_hash"],
                        "codebook_question_text": c["question_text"], "relation_kind": "ONE_TO_ONE",
                        "match_basis": "EXACT_SOURCE_NAME_AND_ORDINAL"})
        c_entries.append({"codebook_var_name": c["var_name"], "codebook_row_index": c["row_index"],
                          "codebook_row_hash": c["row_hash"], "codebook_question_text": c["question_text"],
                          "physical_names": [p["name"]], "relation_kind": "ONE_TO_ONE"})
    return {"schema": "PYAT_R157_SOURCE_CORRESPONDENCE@1.0.0", "source_id": source_id,
            "source_sha256": roster["source_sha256"], "physical_columns": roster["physical_columns"],
            "codebook_rows": roster["codebook_rows"], "method": "EXACT_NAMES",
            "entries": entries, "codebook_entries": c_entries,
            "counts": {"physical_entries": len(entries), "codebook_entries": len(c_entries),
                       "one_to_one": len(entries), "one_to_many": 0, "physical_only_extra": 0,
                       "codebook_only_unmapped": 0},
            "limits": ["Exact source names and ordinals; no alias or normalization is inferred."]}


def main() -> int:
    from rawlsing_next.source_configuration.schema import canonical_config_hash, validate_source_config
    for source_id in SOURCE_IDS:
        roster = E.source_roster_entry(source_id)
        phys = list(E.iter_physical_slots(source_id))
        cb = list(E.iter_codebook_rows(source_id))
        items = list(E.iter_item_evidence(source_id))
        phys_by_name = {p["name"]: p for p in phys}
        crosswalk = build_crosswalk(source_id, roster, phys, cb)
        plan = classify(source_id, items, phys_by_name)
        crosswalk["counts"]["selected_for_supported_slice"] = len(plan["included_slots"])
        data_dir = DATA_ROOT / source_id
        val_dir = VAL_ROOT / source_id
        data_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        crosswalk_sha, crosswalk_bytes = write_json(data_dir / "crosswalk.json", crosswalk)
        original = build_config(source_id, roster, phys, items, plan, mode="original", fixture_meta=None,
                                crosswalk_sha=crosswalk_sha)
        validate_source_config(original)
        fixture_doc, oracle = build_fixture(source_id, phys_by_name, plan)
        fixture_meta = {
            "fixture_id": fixture_doc["fixture_id"],
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "row_count": fixture_doc["row_count"],
            "provenance": "Repository-generated nonrespondent fixture for the R157 ARAB lane; no original respondents represented.",
            "fixture_study_product_id": f"R157_FIXTURE/{source_id}",
            "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
            "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
        }
        fixture_config = build_config(source_id, roster, phys, items, plan, mode="fixture",
                                      fixture_meta=fixture_meta, crosswalk_sha=crosswalk_sha)
        validate_source_config(fixture_config)
        field_evidence = build_field_evidence(source_id, roster, phys, items, plan, original, crosswalk_sha)
        artifacts = [("rawlsing_next/source_configuration/data/" + source_id + "/crosswalk.json",
                      crosswalk_sha, crosswalk_bytes)]
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
            "schema": "PYAT_R157_ARAB_SOURCE_MANIFEST@1.0.0", "source_id": source_id,
            "family": roster["family"], "wave": str(roster["wave"]),
            "source_sha256": roster["source_sha256"],
            "config_sha256": canonical_config_hash(original),
            "fixture_config_sha256": canonical_config_hash(fixture_config),
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "counts": {"physical_slots": roster["physical_columns"], "original_items": roster["original_items"],
                       "included_slots": len(original["coverage"]["physical_slots_included"]),
                       "included_items": len(original["coverage"]["items_included"]),
                       "excluded_slots": len(original["coverage"]["physical_slots_excluded"]),
                       "excluded_items": len(original["coverage"]["items_excluded"]),
                       "response_questions": len(plan["responses"]),
                       "response_slots": len(original["response_slots"]),
                       "coordinate_slots": len(original["coordinate_slots"]),
                       "crosswalk_entries": len(crosswalk["entries"])},
            "artifacts": [{"path": p, "sha256": h, "bytes": b} for p, h, b in artifacts],
        }
        write_json(val_dir / "manifest.json", manifest)
        print(f"{source_id}: config={canonical_config_hash(original)} fixture={fixture_doc['fixture_source_sha256']} "
              f"included_slots={len(original['coverage']['physical_slots_included'])} "
              f"included_items={len(original['coverage']['items_included'])} "
              f"excluded_items={len(original['coverage']['items_excluded'])} "
              f"questions={len(plan['responses'])} coords={len(original['coordinate_slots'])}")
    return 0


def build_field_evidence(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                         items: list[Mapping[str, Any]], plan: Mapping[str, Any],
                         config: Mapping[str, Any], crosswalk_sha: str) -> dict[str, Any]:
    metadata_ref = exact_ref("R154_PHYSICAL_METADATA",
                             f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                             roster["metadata_witness"]["sha256"])
    included_items = set(plan["included_items"])
    entries = []
    for p in phys:
        entries.append({"field": f"physical_slots[{p['ordinal']}]", "physical_name": p["name"],
                        "included": p["ordinal"] in config["coverage"]["physical_slots_included"],
                        "refs": [metadata_ref, exact_ref("CODEBOOK_ROW",
                                                        f"urn:rawlsing:r157:codebook:{source_id}:{p['name']}",
                                                        p["codebook_mapping"]["row_hash"])]})
    for x in items:
        entries.append({"field": f"items[{x['implementation_id']}]",
                        "source_variable_code": x["source_variable_code"],
                        "included": x["source_variable_code"] in included_items,
                        "refs": [exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}",
                                          x["exact_identity_sha256"]),
                                 exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}",
                                           x["exact_identity_sha256"])]})
    return {"schema": "PYAT_R157_SOURCE_FIELD_EVIDENCE@1.0.0", "source_id": source_id,
            "config_id": config["config_id"], "physical_slot_entries": len(phys),
            "item_entries": len(items), "included_slots": config["coverage"]["physical_slots_included"],
            "included_items": config["coverage"]["items_included"], "entries": entries,
            "crosswalk_sha256": crosswalk_sha,
            "limits": ["Every physical slot and original item is represented once.",
                       "Included/excluded status is the declared preparation slice, not deletion."]}


def write_json(path: Path, value: Any) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest(), len(raw)


if __name__ == "__main__":
    raise SystemExit(main())
