"""Build full R157 SOUTH_ASIA source configurations and nonrespondent fixtures."""
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
SOURCE_IDS = ("SRC31", "SRC32")
FIXTURE_ROWS = 8


def sha_material(material: Any) -> str:
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


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
    na = any(x in text for x in ("no answer", "does not answer", "no responde", "refus", "declined"))
    if dk and na:
        return "SOURCE_SPECIFIC_SPECIAL"
    if na:
        return "REFUSAL"
    if dk:
        return "DK"
    if "missing" in text or "unknown" in text or "not provided" in text:
        return "MISSING"
    if text in {"none", "ninguno", "ninguna"}:
        return "SOURCE_SPECIFIC_SPECIAL"
    return "SUBSTANTIVE_RESPONSE"


def code_labels(slot: Mapping[str, Any]) -> list[tuple[int, str]]:
    out = []
    for key, label in (slot.get("value_labels") or {}).items():
        try:
            out.append((int(float(key)), str(label)))
        except (TypeError, ValueError):
            pass
    return sorted(out)


def topology_kind(topology: str) -> str:
    return {
        "scalar": "SCALAR",
        "nominal_context": "NOMINAL_CONTEXT",
        "ordinal_context": "ORDINAL_CONTEXT",
        "nominal_choice": "NOMINAL_CHOICE",
        "binary_contrast": "BINARY_CONTRAST",
        "binary_tradeoff": "BINARY_TRADEOFF",
        "routed_followup": "ROUTED_FOLLOWUP",
        "ranked_choice": "RANKED_CHOICE",
    }.get(topology, "SCALAR")


def value_rule(slot: Mapping[str, Any], code: int | None, label: str | None, kind: str,
               mapping_authority: Mapping[str, str]) -> dict[str, Any]:
    if code is None:
        missing_state, state, raw, canonical = "SYSTEM_MISSING", "MISSING", None, None
    else:
        missing_state = "OBSERVED_STORAGE_VALUE"
        state = response_state(label)
        raw = float(code)
        canonical = str(int(code)) if state == "SUBSTANTIVE_RESPONSE" else None
    return {
        "raw_value": raw, "missing_state": missing_state, "source_missing_declaration": None,
        "response_state": state,
        "occurrences": [{
            "key": "0",
            "topology_ref": exact_ref(
                "RESPONSE_TOPOLOGY", f"urn:rawlsing:r157:topology:{slot['source_id']}:{slot['name']}:{kind}",
                sha_material({"source": slot["source_id"], "slot": slot["name"], "kind": kind})),
            "multiplicity_order_rank_fields": {"kind": kind, "index": 0},
        }],
        "canonical_value": canonical,
        "transform_authority_ref": mapping_authority if canonical is not None else None,
        "extra_authority_refs": [],
    }


def slot_values(slot: Mapping[str, Any], kind: str, mapping_authority: Mapping[str, str]) -> list[dict[str, Any]]:
    vals = [value_rule(slot, code, label, kind, mapping_authority) for code, label in code_labels(slot)]
    vals.append(value_rule(slot, None, None, kind, mapping_authority))
    return vals


def missing_declaration(slot: Mapping[str, Any]) -> Mapping[str, Any] | None:
    out = {}
    if slot.get("missing_ranges") is not None:
        out["ranges"] = slot["missing_ranges"]
    if slot.get("missing_user_values") is not None:
        out["user_values"] = slot["missing_user_values"]
    return out or None


def physical_slot_doc(p: Mapping[str, Any], disposition: str, reason: str) -> dict[str, Any]:
    cbm = p["codebook_mapping"]
    return {"ordinal": p["ordinal"], "name": p["name"], "label": p["label"],
            "storage_type": p["readstat_type"], "original_type": p["original_type"],
            "storage_width": p["storage_width"], "measure": p["measure"],
            "value_labels": p["value_labels"], "missing_declarations": missing_declaration(p),
            "mr_declarations": None,
            "codebook_mapping": {"var_name": cbm["var_name"], "row_hash": cbm["row_hash"], "status": cbm["status"]},
            "disposition": disposition, "disposition_reason": reason}


def item_doc(x: Mapping[str, Any]) -> dict[str, Any]:
    r = x["relation"]
    rel = {"status": "EXACT", "question_id": r["question_id"],
           "mapping_status": r["mapping_status"] or "governed_qsmv2_relation",
           "manual_response_topology": r["manual_response_topology"],
           "manual_response_normalization_rule": r["manual_response_normalization_rule"],
           "manual_position_conditioning": r["manual_position_conditioning"],
           "manual_semantic_role": r["manual_semantic_role"],
           "manual_signed_polarity_status": r["manual_signed_polarity_status"],
           "forbidden_inference": r["forbidden_inference"] or "none recorded",
           "does_not_measure": r["does_not_measure"] or "none recorded",
           "governed_row_payload_hash": r["governed_row_payload_hash"],
           "p2_exact_identity_sha256": r["p2_exact_identity_sha256"]}
    return {"implementation_id": x["implementation_id"], "source_variable_code": x["source_variable_code"],
            "exact_identity_sha256": x["exact_identity_sha256"], "question_text": x["p2"]["question_text"],
            "disposition": x["h48"]["disposition"], "response_classes": x["p2"]["response_classes"],
            "mapping_status": rel["mapping_status"], "authority_status": r["authority_status"],
            "evidence_refs": [
                exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
                exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
                exact_ref("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{r['question_id']}", r["governed_row_payload_hash"])],
            "limits": [f"relation_use_status_final={r.get('relation_use_status_final') or 'NOT_RECORDED'}",
                       f"mapping_status={rel['mapping_status']}",
                       f"manual_signed_polarity_status={r['manual_signed_polarity_status']}",
                       f"forbidden_inference={r['forbidden_inference'] or 'none recorded'}",
                       f"does_not_measure={r['does_not_measure'] or 'none recorded'}"],
            "relation": rel}


def authority(source_id: str, source_sha: str, kind: str, state: str, operation: str,
              grade: str, families: list[str], extra: Mapping[str, Any],
              fixture_id: str | None) -> dict[str, Any]:
    scope = {"fixture_only": fixture_id is not None, "grade": grade, "source_id": source_id,
             "source_sha256": source_sha, **extra}
    if fixture_id:
        scope["fixture_id"] = fixture_id
        scope["original_source_sha256"] = source_sha
    else:
        scope["execution_grant"] = "NOT_ISSUED_UNDER_R157_PREPARATION"
    material = {"authority_id": f"R157-{source_id}-{operation}", "authority_version": "1.0.0",
                "authority_kind": kind, "decision_state": state, "scope_envelope": scope,
                "governed_operations": [operation], "governed_object_families": families}
    ch = sha_material(material)
    return {"typed_state": state, "authority_snapshot_refs": [], "dependency_refs": [],
            "producer_replay_locator_or_reference_root": exact_ref(
                "REPLAY_ROOT", f"urn:rawlsing:r157:authority:{source_id}:{operation}", sha_material({"root": material})),
            "authority_id": material["authority_id"], "authority_version": "1.0.0",
            "authority_content_hash": ch, "authority_kind": kind, "decision_state": state,
            "governed_operations": [operation], "governed_object_families": families,
            "scope_envelope": scope,
            "effective_time_or_interval": "R157_NONRESPONDENT_FIXTURE" if fixture_id else "R157_PREPARATION",
            "parent_authority_refs": [], "negative_limit_refs": [], "supersession_refs": [],
            "interpretation_semantics_fingerprint": sha_material({"scope": scope, "operation": operation}),
            "replay_protocol_ref": exact_ref("REPLAY_PROTOCOL", f"urn:rawlsing:r157:replay:{source_id}",
                                             sha_material({"operation": operation, "source": source_id, "fixture": fixture_id}))}


def build_authorities(source_id: str, source_sha: str, fixture_id: str | None, wave: str):
    state = "ALLOW" if fixture_id else "DEFER"
    grade = "NONRESPONDENT_FIXTURE_ONLY" if fixture_id else "SOURCE_NATIVE_REPRESENTATION_PREPARATION"
    common = {"wave": wave}
    specs = [
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_ITEM_SEMANTICS", grade,
         ["RespondentEvent@1.0.0"],
         {"semantic_scope": "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY",
          "direction_status": "NOT_CERTIFIED_BY_THIS_AUTHORITY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_TOPOLOGY", grade,
         ["RespondentEvent@1.0.0"], {"topology_scope": "EXACT_SOURCE_VALUE_LABELS_AND_H48_TOPOLOGY_ONLY", **common}),
        ("NATIVE_CANONICAL_MAPPING_HARMONIZATION", state, "R157_MAP_SOURCE_CODE_TOKEN_IDENTITY", grade,
         ["RespondentEvent@1.0.0"], {"mapping_scope": "EXACT_SOURCE_NATIVE_CODE_TOKEN_IDENTITY_ONLY_NO_SIGNED_DIRECTION", **common}),
        ("COORDINATE_SEMANTICS", state, "R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW", grade,
         ["EmpiricalCoordinateFact@1.0.0"], {"coordinate_scope": "COPY_OBSERVED_RAW_NO_CANONICAL_CROSSWALK", **common}),
        ("ROUTING_RISK_SET", state, "R157_RECORD_UNRESOLVED_SOURCE_ROUTING", grade,
         ["RoutingEligibilityFact@1.0.0"], {"routing_scope": "SOURCE_ROUTING_UNRESOLVED_NO_ELIGIBILITY_CLAIM", **common}),
        ("REPLAY_PROTOCOL", "ALLOW", "R157_LOCAL_DETERMINISTIC_REPLAY",
         "NONRESPONDENT_FIXTURE_ONLY" if fixture_id else "R157_DETERMINISTIC_REPLAY_PROTOCOL",
         ["ReplayReceipt@1.0.0"], {"replay_scope": "R157_LOCAL_ENGINEERING_ONLY", **common}),
        ("SOURCE_SEMANTICS_TOPOLOGY", state, "R157_PREPARE_SOURCE_PROJECTION", grade,
         ["EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
          "RoutingEligibilityFact@1.0.0"], {"projection_scope": "FULL_DECLARED_SOURCE_SLICE", **common}),
    ]
    return {op: authority(source_id, source_sha, kind, st, op, gr, fams, extra, fixture_id)
            for kind, st, op, gr, fams, extra in specs}


def make_universe(source_id: str, roster: Mapping[str, Any], auths: Mapping[str, Mapping[str, Any]],
                  fixture_id: str | None, wave: str):
    from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse
    semantic = authority_ref(auths["R157_PREPARE_SOURCE_ITEM_SEMANTICS"])
    if fixture_id:
        payload = {"typed_state": "UNIVERSE_IDENTIFIED", "authority_snapshot_refs": [semantic],
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
                   "harmonization_authority_ref": None, "source_relation_refs": []}
    else:
        payload = {"typed_state": "UNIVERSE_IDENTIFIED", "authority_snapshot_refs": [semantic],
                   "dependency_refs": [],
                   "producer_replay_locator_or_reference_root": exact_ref(
                       "REPLAY_ROOT", f"urn:rawlsing:r157:universe:{source_id}",
                       sha_material({"source": source_id, "sha": roster["source_sha256"]})),
                   "raw_source_identity": f"{roster['family']} {roster['wave']} / {source_id}",
                   "source_family": roster["family"], "study_product_release": f"{roster['family']}:{roster['wave']}",
                   "instrument_release": f"{source_id}_INSTRUMENT_SOUTH_ASIA_{roster['wave']}",
                   "country_geography": "SOURCE_OBSERVED_COUNTRY_CODES",
                   "sampling_geography": "UNKNOWN_SOURCE_SAMPLING_GEOGRAPHY_R157_PREPARATION",
                   "raw_wave": wave, "canonical_wave_if_governed": None, "field_or_reference_time": wave,
                   "target_population_and_sample_frame": "UNKNOWN_SOURCE_SAMPLE_FRAME_R157_PREPARATION",
                   "sampling_design_regime": "UNKNOWN_SOURCE_DESIGN_R157_PREPARATION",
                   "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
                   "source_artifact_import_lineage": f"R154_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}",
                   "harmonization_authority_ref": None, "source_relation_refs": []}
    return payload, EmpiricalUniverse(**payload).ref.as_dict()


def classify(source_id: str, items: list[Mapping[str, Any]], phys_by_name: Mapping[str, Mapping[str, Any]]):
    responses, coordinates, excluded = [], [], []
    for x in items:
        code = x["source_variable_code"]
        p = phys_by_name[code]
        r = x["relation"]
        topology = r["manual_response_topology"]
        disposition = x["h48"]["disposition"]
        binding = x["p2"].get("response_binding_status")
        labels = p.get("value_labels") or {}
        if disposition == "ADMINISTRATIVE_METADATA" or topology == "administrative_context":
            coordinates.append({"item_code": code, "slot": p["name"],
                                "mode": "values" if any(response_state(l) == "SUBSTANTIVE_RESPONSE" for l in labels.values()) else "raw",
                                "unit": "SOURCE_NATIVE_ADMIN_CONTEXT",
                                "note": "Source-native administrative/context field bound as a coordinate."})
            continue
        if topology == "continuous_context":
            coordinates.append({"item_code": code, "slot": p["name"], "mode": "raw",
                                "unit": "SOURCE_NATIVE_CONTINUOUS_CONTEXT",
                                "note": "Continuous source-native context bound as a raw coordinate; no categorical default."})
            continue
        if not labels:
            excluded.append({"item_code": code, "slot": p["name"], "reason": "NO_DECLARED_FINITE_VALUE_DOMAIN",
                             "native_field": "response_slots[].values (ResponseValueRule.physical_key)",
                             "evidence": "No declared value labels for this response item.",
                             "dependent_operation": "finite categorical native response construction"})
            continue
        if binding != "bound":
            excluded.append({"item_code": code, "slot": p["name"], "reason": "RESPONSE_BINDING_BLOCKED",
                             "native_field": "response_slots[].values / response binding",
                             "evidence": f"P2 response_binding_status={binding!r}.",
                             "dependent_operation": "source-native response construction"})
            continue
        responses.append({"question_id": code, "item_code": code, "slot": p["name"],
                          "topology": topology, "kind": topology_kind(topology)})
    incl_slots = {r["slot"] for r in responses} | {c["slot"] for c in coordinates}
    excl_slots = {e["slot"] for e in excluded}
    if incl_slots & excl_slots or incl_slots | excl_slots != set(phys_by_name):
        raise RuntimeError(f"{source_id}: physical partition incomplete")
    incl_items = {r["item_code"] for r in responses} | {c["item_code"] for c in coordinates}
    excl_items = {e["item_code"] for e in excluded}
    if incl_items & excl_items or incl_items | excl_items != {x["source_variable_code"] for x in items}:
        raise RuntimeError(f"{source_id}: item partition incomplete")
    return {"responses": responses, "coordinates": coordinates, "excluded": excluded,
            "included_slots": incl_slots, "excluded_slots": excl_slots,
            "included_items": incl_items, "excluded_items": excl_items}


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


def build_residuals(source_id: str, plan: Mapping[str, Any], mode: str):
    if mode == "fixture":
        return [{"residual_id": f"{source_id}-FIXTURE-ONLY-AUTHORITY", "scope": source_id,
                 "field": "authority.snapshots", "status": "FIXTURE_ONLY",
                 "reason": "Fixture proves native construction but does not establish original-source authority.",
                 "dependent_operation": "original-source execution and scientific interpretation",
                 "unaffected_scope": "nonrespondent fixture native C11 validation",
                 "owner": "SOUTH_ASIA lane / P3 integration owner",
                 "next_step": "Keep fixture authority separate from the ORIGINAL_SOURCE config."}]
    out = [
        {"residual_id": f"{source_id}-ROUTING-UNRESOLVED", "scope": source_id,
         "field": "routing.typed_state", "status": "UNKNOWN",
         "reason": f"SOURCE_ROUTING_UNRESOLVED for {len(plan['responses'])} response items. The portable recipe declares row_selector=ALL with typed_state ROUTING_UNKNOWN for every produced routing fact; it does not invent eligibility, forms, populations or permissions. Original rows were not physically expanded for validation.",
         "dependent_operation": "eligibility/form-conditioned native query",
         "unaffected_scope": "unconditional source-native response incidence and coordinate binding",
         "owner": "SOUTH_ASIA lane / P3 integration owner",
         "next_step": "Recover exact indexed routing/form expressions before claiming eligibility-conditioned scope."},
        {"residual_id": f"{source_id}-ROW-NATIVE-KEY", "scope": source_id,
         "field": "respondents.source_native_key_slot", "status": "UNKNOWN",
         "reason": "No exact decoded source-native respondent key witness exists in preparation; physical row ordinal is the only established key.",
         "dependent_operation": "respondent-key linkage beyond row ordinal",
         "unaffected_scope": "row-ordinal-scoped source-native construction",
         "owner": "SOUTH_ASIA lane / P3 integration owner",
         "next_step": "Supply exact row_native_keys only after a separately permitted decode."},
        {"residual_id": f"{source_id}-FORM-ADMIN", "scope": source_id,
         "field": "supported_scope.supported_form_slice", "status": "UNKNOWN",
         "reason": "Current physical/codebook evidence contains no form, ballot or administration variable; single-file SAV shape is established.",
         "dependent_operation": "form-conditioned or administration-conditioned native query",
         "unaffected_scope": "source-native response incidence without form conditioning",
         "owner": "SOUTH_ASIA lane / P3 integration owner",
         "next_step": "Acquire exact source form/administration evidence before claiming a form-conditioned slice."},
        {"residual_id": f"{source_id}-WEIGHT-AUTHORITY", "scope": source_id,
         "field": "weight_slots", "status": "NOT_DECLARED",
         "reason": "No source weight item/slot is present in current physical/codebook evidence; no weighted scope is declared.",
         "dependent_operation": "population or weighted estimation",
         "unaffected_scope": "raw-sample source-native response incidence",
         "owner": "SOUTH_ASIA lane / P3 integration owner",
         "next_step": "Bind exact weight basis, design, estimand and scope only if such a source slot is established."},
        {"residual_id": f"{source_id}-DIRECTION", "scope": source_id,
         "field": "items.relation.manual_signed_polarity_status", "status": "NOT_CERTIFIED_BY_THIS_PREPARATION",
         "reason": "Response states and exact source code tokens are bound, but this preparation does not issue a new signed-direction or canonical semantic certification.",
         "dependent_operation": "signed-direction empirical or structural analysis",
         "unaffected_scope": "source-native nominal/ordinal response incidence and exact value accounting",
         "owner": "SOUTH_ASIA lane / later scientific authority owner",
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
        out.append({"residual_id": f"{source_id}-EXCLUDED-{exc['item_code']}",
                    "scope": f"{source_id}/{exc['item_code']}", "field": exc["native_field"],
                    "status": exc["reason"], "reason": exc["evidence"],
                    "dependent_operation": exc["dependent_operation"],
                    "unaffected_scope": "all other included source-native response/coordinate bindings",
                    "owner": "SOUTH_ASIA lane / P3 integration owner",
                    "next_step": "Preserve the exact limitation; acquire the missing source/native fact before binding."})
    return out


def build_config(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                 items: list[Mapping[str, Any]], plan: Mapping[str, Any], *, mode: str,
                 fixture_meta: Mapping[str, Any] | None, crosswalk_sha: str) -> dict[str, Any]:
    phys_by_name = {p["name"]: p for p in phys}
    item_by_code = {x["source_variable_code"]: x for x in items}
    source_sha, wave = roster["source_sha256"], str(roster["wave"])
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
        doc["disposition"] = ("SUPPORTED_SOURCE_NATIVE_RESPONSE"
                              if any(code == r["item_code"] for r in plan["responses"])
                              else "SUPPORTED_SOURCE_NATIVE_COORDINATE")
        doc["limits"] = list(doc["limits"]) + ["Included at its exact source-native representation scope."]
        item_docs.append(doc)

    questions = []
    for r in plan["responses"]:
        x = item_by_code[r["item_code"]]
        questions.append({"question_id": r["question_id"], "empirical_universe_ref": universe_ref,
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
                                            "relation_join_status": x.get("relation_join_status")}})

    response_slots = [{"slot": {"ordinal": phys_by_name[r["slot"]]["ordinal"], "name": r["slot"]},
                       "question_id": r["question_id"],
                       "values": slot_values(phys_by_name[r["slot"]], r["kind"],
                                             aref["R157_MAP_SOURCE_CODE_TOKEN_IDENTITY"])}
                      for r in plan["responses"]]

    coordinate_slots = []
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        mode_values = c["mode"] == "values" and any(
            response_state(l) == "SUBSTANTIVE_RESPONSE" for l in (p.get("value_labels") or {}).values())
        coordinate_slots.append({"slot": {"ordinal": p["ordinal"], "name": p["name"]},
                                 "native_coordinate_ref": exact_ref(
                                     "COORDINATE_NATIVE", f"urn:rawlsing:r157:{mode}:{source_id}:{p['name']}",
                                     sha_material({"source": source_id, "slot": p["name"], "mode": mode})),
                                 "unit_taxonomy_ref": exact_ref(
                                     "UNIT_TAXONOMY", f"urn:rawlsing:r157:{c['unit']}", sha_material({"unit": c["unit"]})),
                                 "effective_time": wave,
                                 "source_semantic_authority_ref": aref["R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW"],
                                 "canonical_coordinate_ref": None, "normalization_ref": None,
                                 "values": coordinate_values(p) if mode_values else [],
                                 "copy_observed_raw": not mode_values})

    routing = [{"question_id": r["question_id"], "row_selector": "ALL", "typed_state": "ROUTING_UNKNOWN",
                "risk_set_ref": exact_ref("RISK_SET", f"urn:rawlsing:r157:{mode}:{source_id}:{r['question_id']}:unresolved",
                                          sha_material({"s": source_id, "q": r["question_id"], "m": mode, "r": "risk"})),
                "routing_rule_ref": exact_ref("ROUTING_RULE", f"urn:rawlsing:r157:{mode}:{source_id}:{r['question_id']}:unresolved",
                                              sha_material({"s": source_id, "q": r["question_id"], "m": mode, "r": "rule"})),
                "member_set_replay_ref": exact_ref("MEMBER_SET_REPLAY", f"urn:rawlsing:r157:{mode}:{source_id}:{r['question_id']}:unresolved",
                                                   sha_material({"s": source_id, "q": r["question_id"], "m": mode, "r": "member"})),
                "authority_ref": aref["R157_RECORD_UNRESOLVED_SOURCE_ROUTING"],
                "parent_predicate_refs": [], "dependency_refs": []}
               for r in plan["responses"]]

    included_ordinals = sorted(phys_by_name[n]["ordinal"] for n in plan["included_slots"])
    if mode == "original":
        coverage = {"physical_slots_total": roster["physical_columns"], "items_total": roster["original_items"],
                    "physical_slots_included": included_ordinals,
                    "physical_slots_excluded": [{"ordinal": phys_by_name[n]["ordinal"], "name": n,
                                                  "reason": next(e for e in plan["excluded"] if e["slot"] == n)["evidence"]}
                                                 for n in sorted(plan["excluded_slots"], key=lambda n: phys_by_name[n]["ordinal"])],
                    "items_included": sorted(item_by_code[c]["implementation_id"] for c in plan["included_items"]),
                    "items_excluded": [{"implementation_id": item_by_code[c]["implementation_id"],
                                        "reason": next(e for e in plan["excluded"] if e["item_code"] == c)["evidence"]}
                                       for c in sorted(plan["excluded_items"])],
                    "partial_scope_reason": "Every physical slot and original item is accounted; included items have a lawful source-native response or coordinate binding and exclusions carry exact native-field/evidence limitations."}
    else:
        coverage = {"physical_slots_total": roster["physical_columns"], "items_total": roster["original_items"],
                    "partial_scope_reason": "Nonrespondent fixture slice covering every declared supported response and coordinate slot.",
                    "not_a_lane_config": True}

    qids = [r["question_id"] for r in plan["responses"]]
    supported_scope = {
        "scope_id": f"{source_id}-R157-FULL-SOURCE-NATIVE-CONFIGURATION" if mode == "original" else f"{source_id}-R157-NONRESPONDENT-FIXTURE-FULL-SLICE",
        "purpose": "SOURCE_PREPARATION" if mode == "original" else "NONRESPONDENT_FIXTURE_VALIDATION",
        "declared_supported": True, "supported_question_ids": qids,
        "native_validation_expectation": "NOT_RUN" if mode == "original" else "POSITIVE_RELEASE",
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "supported_unit_slice": "SOURCE_INTERVIEW_ROW" if mode == "original" else "NONRESPONDENT_FIXTURE_ROWS",
        "supported_form_slice": "SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE" if mode == "original" else "NONRESPONDENT_FIXTURE_ALL_SUPPORTED_SLOTS",
        "notes": ["All inclusive items are source-native response or coordinate bindings; exclusions are exact limitations.",
                  "Positive native C11 release is exercised by the separately identified nonrespondent fixture config.",
                  "Routing uses row_selector=ALL with ROUTING_UNKNOWN and is not physically expanded for original validation."] if mode == "original" else ["Fixture-only authority; never original-source authority."]}
    residuals = build_residuals(source_id, plan, mode)
    metadata_ref = exact_ref("R154_PHYSICAL_METADATA",
                             f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                             roster["metadata_witness"]["sha256"])
    field_evidence = [{"field": "identity.expected_source_sha256",
                       "refs": [exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)]},
                      {"field": "identity.metadata_witness_ref", "refs": [metadata_ref]},
                      {"field": "correspondence",
                       "refs": [exact_ref("SOURCE_CORRESPONDENCE",
                                          f"rawlsing_next/source_configuration/data/{source_id}/crosswalk.json", crosswalk_sha)]}]
    for code in sorted(plan["included_items"]):
        x = item_by_code[code]
        field_evidence.append({"field": f"items[{x['implementation_id']}]",
                               "refs": [exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
                                        exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
                                        exact_ref("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{x['relation']['question_id']}", x["relation"]["governed_row_payload_hash"])]})
    evidence = {"source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
                "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
                "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
                "pinned_inputs": [{"kind": "R157_PLAN_SEAL", "commit": "4c0c619eac747afee1d8e65e1418bf2d472da4c3"},
                                  {"kind": "R154_METADATA_SNAPSHOT", "commit": "a02adc896264e1b46afd143cba9426182ec14802",
                                   "path": "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite",
                                   "sha256": "7d6421e6e50f7d249cf09e7ecf964757d6afa4a7926d7a31eb1aad3407a12a16"},
                                  {"kind": "H48_ITEM_INDEX", "commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
                                   "path": "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz",
                                   "sha256": "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5"},
                                  {"kind": "P2_PHASE0", "sha256": "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"},
                                  {"kind": "FULL_RELATION_AUTHORITY", "commit": "9561723cfe0932869e781f2be27e9c80b050ad7a",
                                   "path": "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
                                   "sha256": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"}],
                "field_evidence": field_evidence,
                "limits": ["Prior H48/P2/full-relation evidence is reused with original grades and limits.",
                           "No original respondent rows, response values or source bytes were read.",
                           "Fixture authority is not original-source authority."]}
    authority_section = {"snapshots": [auths[k] for k in sorted(auths)],
                         "required_refs": [aref[k] for k in sorted(aref)],
                         "projection_authority_ref": aref["R157_PREPARE_SOURCE_PROJECTION"],
                         "replay_authority_ref": aref["R157_LOCAL_DETERMINISTIC_REPLAY"],
                         "projection_identity_ref": exact_ref(
                             "C11_SEMANTIC_PROJECTION", f"urn:rawlsing:r157:{mode}:{source_id}:projection",
                             sha_material({"source": source_id, "sha": source_sha, "mode": mode, "questions": qids})),
                         "tie_order_ref": exact_ref("ORDER_RULE", "urn:rawlsing:r157:canonical-ref-sort",
                                                    sha_material({"rule": "canonical_ref_sort"})),
                         "replay_protocol_version": "1.0.0"}
    identity = {"source_id": source_id, "family": roster["family"], "wave": wave,
                "source_family_id": roster["family"], "study_product_id": f"{roster['family']}:{wave}",
                "release_id": f"{source_id}_SOUTH_ASIA_{wave}_PREPARATION",
                "instrument_release_id": f"{source_id}_INSTRUMENT_SOUTH_ASIA_{wave}",
                "source_artifact_id": roster["source_artifact_id"], "expected_source_sha256": source_sha,
                "source_format": roster["format"], "source_row_count": roster["rows"],
                "source_column_count": roster["physical_columns"], "source_bytes": roster["bytes"],
                "codebook_rows": roster["codebook_rows"], "original_item_count": roster["original_items"],
                "source_snapshot_retention_ref": exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
                "metadata_witness_ref": metadata_ref,
                "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
                "reader": {"decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                           "configuration_ref": exact_ref("READER_CONFIGURATION", f"urn:rawlsing:r157:{source_id}:default_sav",
                                                          sha_material({"source": source_id, "sha": source_sha, "reader": "default_sav"})),
                           "encoding": None}}
    if mode == "original":
        binding = {"identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
                   "source_snapshot_ref": exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)}
        respondents = {"subject_unit": "SOURCE_INTERVIEW_ROW", "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
                       "respondent_key_pattern": f"{source_id}-ROW-{{row_ordinal:05d}}",
                       "source_native_key_slot": None, "identity_map_authority_ref": None,
                       "row_identity_grade": "SOURCE_PHYSICAL_ROW_ORDINAL_ONLY"}
        config_id, purpose = f"R157-SOUTH-ASIA-{source_id}-FULL-SOURCE-PREPARATION", "SOURCE_PREPARATION"
    else:
        binding = {"identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
                   "source_snapshot_ref": exact_ref("FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:fixture:{fixture_meta['fixture_id']}", binding_sha),
                   "fixture_provenance": {"fixture_id": fixture_meta["fixture_id"], "provenance": fixture_meta["provenance"],
                                          "authority_grade": "NONRESPONDENT_FIXTURE_ONLY", "original_source_id": source_id,
                                          "original_source_sha256": source_sha, "no_original_respondents": True,
                                          "fixture_study_product_id": fixture_meta["fixture_study_product_id"],
                                          "fixture_release_id": fixture_meta["fixture_release_id"],
                                          "fixture_instrument_release_id": fixture_meta["fixture_instrument_release_id"]}}
        respondents = {"subject_unit": "NONRESPONDENT_FIXTURE_ROW", "respondent_namespace": f"urn:rawlsing:r157:fixture:{source_id}",
                       "respondent_key_pattern": f"FIXTURE-{source_id}-ROW-{{row_ordinal:03d}}",
                       "source_native_key_slot": None, "identity_map_authority_ref": None,
                       "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY"}
        config_id, purpose = f"R157-SOUTH-ASIA-{source_id}-NONRESPONDENT-FIXTURE", "NONRESPONDENT_FIXTURE"
    return {"schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0", "config_id": config_id,
            "config_revision": 1, "config_purpose": purpose, "identity": identity, "binding": binding,
            "authority": authority_section, "universe": {"universes": [universe_payload]},
            "respondents": respondents, "questions": questions, "physical_slots": physical_docs,
            "items": item_docs, "response_slots": response_slots, "coordinate_slots": coordinate_slots,
            "weight_slots": [], "routing": routing,
            "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
            "replay": {"predicate": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
                       "comparator": {"typed_absence_state": "DEFERRED", "detail": None},
                       "discovery": {"typed_absence_state": "DEFERRED", "detail": None},
                       "structural": {"typed_absence_state": "NOT_APPLICABLE", "detail": None}},
            "supported_scope": supported_scope, "coverage": coverage, "residuals": residuals,
            "evidence": evidence,
            "runtime": {"projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
                        "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
                        "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
                        "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
                        "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
                        "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
                        "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
                        "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
                        "reader_encoding_transport": "P3_INTEGRATION_OWNER_QUALIFIED_READER_TRANSPORT"}}


def build_fixture(source_id: str, phys_by_name: Mapping[str, Mapping[str, Any]], plan: Mapping[str, Any]):
    rows = FIXTURE_ROWS
    cells, oracle_slots = [], {}
    for r in plan["responses"]:
        p = phys_by_name[r["slot"]]
        codes = code_labels(p)
        substantive = [c for c, l in codes if response_state(l) == "SUBSTANTIVE_RESPONSE"]
        specials = [c for c, l in codes if response_state(l) != "SUBSTANTIVE_RESPONSE"]
        seq = substantive + specials + [None]
        oracle_slots[r["slot"]] = {"states": [], "raw_values": [], "canonical_values": []}
        for row in range(1, rows + 1):
            code = seq[(row - 1) % len(seq)]
            label = dict(codes).get(code) if code is not None else None
            state = "MISSING" if code is None else response_state(label)
            canonical = str(int(code)) if state == "SUBSTANTIVE_RESPONSE" else None
            cells.append({"row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                          "raw_value": None if code is None else float(code),
                          "missing_state": "SYSTEM_MISSING" if code is None else "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
            oracle_slots[r["slot"]]["states"].append(state)
            oracle_slots[r["slot"]]["raw_values"].append(None if code is None else float(code))
            oracle_slots[r["slot"]]["canonical_values"].append(canonical)
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        substantive = [code for code, label in code_labels(p) if response_state(label) == "SUBSTANTIVE_RESPONSE"]
        for row in range(1, rows + 1):
            raw = float(substantive[(row - 1) % len(substantive)]) if c["mode"] == "values" and substantive else 1.0
            cells.append({"row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                          "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
                          "source_missing_declaration": None})
    fixture_id = f"R157-SOUTH-ASIA-{source_id}-NONRESPONDENT"
    document = {"schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0", "fixture_id": fixture_id,
                "identity_class": "NONRESPONDENT_FIXTURE", "nonrespondent": True,
                "row_count": rows, "cells": cells}
    from rawlsing_next.source_configuration.fixture import fixture_document_sha256
    fixture_sha = fixture_document_sha256(document)
    document["fixture_source_sha256"] = fixture_sha
    state_counts = {}
    for data in oracle_slots.values():
        for state in data["states"]:
            state_counts[state] = state_counts.get(state, 0) + 1
    oracle = {"schema": "PYAT_R157_NONRESPONDENT_FIXTURE_ORACLE@1.0.0", "fixture_id": fixture_id,
              "fixture_source_sha256": fixture_sha, "row_count": rows,
              "expected": {"response_event_count": rows * len(plan["responses"]),
                           "coordinate_fact_count": rows * len(plan["coordinates"]),
                           "routing_fact_count": rows * len(plan["responses"]),
                           "response_states_by_slot": {k: v["states"] for k, v in oracle_slots.items()},
                           "raw_values_by_slot": {k: v["raw_values"] for k, v in oracle_slots.items()},
                           "canonical_values_by_slot": {k: v["canonical_values"] for k, v in oracle_slots.items()},
                           "response_state_counts": state_counts,
                           "weight_section": "NOT_APPLICABLE",
                           "source_relation_section": "DISTINCT_BY_DEFAULT"},
              "oracle_basis": "Declared from fixture cells and serialized source-native value rules before the native call."}
    return document, oracle


def build_crosswalk(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                    cb: list[Mapping[str, Any]]):
    cb_by_name = {c["var_name"]: c for c in cb}
    entries = [{"physical_ordinal": p["ordinal"], "physical_name": p["name"], "physical_label": p["label"],
                "codebook_var_names": [p["name"]], "codebook_row_index": cb_by_name[p["name"]]["row_index"],
                "codebook_row_hash": cb_by_name[p["name"]]["row_hash"],
                "codebook_question_text": cb_by_name[p["name"]]["question_text"],
                "relation_kind": "ONE_TO_ONE", "match_basis": "EXACT_SOURCE_NAME_AND_ORDINAL"} for p in phys]
    c_entries = [{"codebook_var_name": c["var_name"], "codebook_row_index": c["row_index"],
                  "codebook_row_hash": c["row_hash"], "codebook_question_text": c["question_text"],
                  "physical_names": [c["var_name"]], "relation_kind": "ONE_TO_ONE"} for c in cb]
    return {"schema": "PYAT_R157_SOURCE_CORRESPONDENCE@1.0.0", "source_id": source_id,
            "source_sha256": roster["source_sha256"], "physical_columns": roster["physical_columns"],
            "codebook_rows": roster["codebook_rows"], "method": "EXACT_NAMES",
            "entries": entries, "codebook_entries": c_entries,
            "counts": {"physical_entries": len(entries), "codebook_entries": len(c_entries),
                       "one_to_one": len(entries), "one_to_many": 0,
                       "physical_only_extra": 0, "codebook_only_unmapped": 0},
            "limits": ["Exact source names and ordinals; no alias or normalization is inferred."]}


def build_field_evidence(source_id: str, roster: Mapping[str, Any], phys: list[Mapping[str, Any]],
                         items: list[Mapping[str, Any]], plan: Mapping[str, Any],
                         config: Mapping[str, Any], crosswalk_sha: str):
    metadata_ref = exact_ref("R154_PHYSICAL_METADATA",
                             f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                             roster["metadata_witness"]["sha256"])
    entries = [{"field": f"physical_slots[{p['ordinal']}]", "physical_name": p["name"],
                "included": p["ordinal"] in config["coverage"]["physical_slots_included"],
                "refs": [metadata_ref, exact_ref("CODEBOOK_ROW", f"urn:rawlsing:r157:codebook:{source_id}:{p['name']}",
                                                 p["codebook_mapping"]["row_hash"])]} for p in phys]
    for x in items:
        entries.append({"field": f"items[{x['implementation_id']}]",
                        "source_variable_code": x["source_variable_code"],
                        "included": x["source_variable_code"] in plan["included_items"],
                        "refs": [exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
                                 exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"])]})
    return {"schema": "PYAT_R157_SOURCE_FIELD_EVIDENCE@1.0.0", "source_id": source_id,
            "config_id": config["config_id"], "physical_slot_entries": len(phys),
            "item_entries": len(items), "included_slots": config["coverage"]["physical_slots_included"],
            "included_items": config["coverage"]["items_included"], "entries": entries,
            "crosswalk_sha256": crosswalk_sha,
            "limits": ["Every physical slot and original item is represented once.",
                       "Included/excluded status is the declared preparation slice, not deletion."]}


def write_json(path: Path, value: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest(), len(raw)


def main() -> int:
    from rawlsing_next.source_configuration.schema import canonical_config_hash, validate_source_config
    for source_id in SOURCE_IDS:
        roster = E.source_roster_entry(source_id)
        phys, cb, items = list(E.iter_physical_slots(source_id)), list(E.iter_codebook_rows(source_id)), list(E.iter_item_evidence(source_id))
        phys_by_name = {p["name"]: p for p in phys}
        plan = classify(source_id, items, phys_by_name)
        crosswalk = build_crosswalk(source_id, roster, phys, cb)
        crosswalk["counts"]["selected_for_supported_slice"] = len(plan["included_slots"])
        data, val = DATA_ROOT / source_id, VAL_ROOT / source_id
        data.mkdir(parents=True, exist_ok=True); val.mkdir(parents=True, exist_ok=True)
        crosswalk_sha, crosswalk_bytes = write_json(data / "crosswalk.json", crosswalk)
        original = build_config(source_id, roster, phys, items, plan, mode="original", fixture_meta=None,
                                crosswalk_sha=crosswalk_sha)
        validate_source_config(original)
        fixture_doc, oracle = build_fixture(source_id, phys_by_name, plan)
        meta = {"fixture_id": fixture_doc["fixture_id"], "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
                "row_count": fixture_doc["row_count"],
                "provenance": "Repository-generated nonrespondent fixture for the R157 SOUTH_ASIA lane; no original respondents represented.",
                "fixture_study_product_id": f"R157_FIXTURE/{source_id}",
                "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
                "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}"}
        fixture_config = build_config(source_id, roster, phys, items, plan, mode="fixture", fixture_meta=meta,
                                      crosswalk_sha=crosswalk_sha)
        validate_source_config(fixture_config)
        field_evidence = build_field_evidence(source_id, roster, phys, items, plan, original, crosswalk_sha)
        artifacts = [("rawlsing_next/source_configuration/data/" + source_id + "/crosswalk.json", crosswalk_sha, crosswalk_bytes)]
        for rel, value in ((f"rawlsing_next/source_configuration/data/{source_id}/source.config.json", original),
                           (f"rawlsing_next/source_configuration/data/{source_id}/field_evidence.json", field_evidence),
                           (f"source_pre553_validation/{source_id}/fixture.json", fixture_doc),
                           (f"source_pre553_validation/{source_id}/fixture.config.json", fixture_config),
                           (f"source_pre553_validation/{source_id}/fixture_oracle.json", oracle)):
            digest, size = write_json(ROOT / rel, value)
            artifacts.append((rel, digest, size))
        manifest = {"schema": "PYAT_R157_SOUTH_ASIA_SOURCE_MANIFEST@1.0.0", "source_id": source_id,
                    "family": roster["family"], "wave": str(roster["wave"]), "source_sha256": roster["source_sha256"],
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
                    "artifacts": [{"path": p, "sha256": h, "bytes": b} for p, h, b in artifacts]}
        write_json(val / "manifest.json", manifest)
        print(f"{source_id}: config={canonical_config_hash(original)} fixture={fixture_doc['fixture_source_sha256']} "
              f"included_slots={len(original['coverage']['physical_slots_included'])} "
              f"included_items={len(original['coverage']['items_included'])} "
              f"excluded_items={len(original['coverage']['items_excluded'])} "
              f"questions={len(plan['responses'])} coords={len(original['coordinate_slots'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
