"""Full LATIN source-configuration construction (all lawful items, exact exclusions).

This supersedes the earlier bounded canary slice. It binds every item whose
source evidence supports a native response or coordinate representation, and
records an exact native-field/evidence limitation for the remainder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TOOLS))

import latin_lane as L  # noqa: E402
from rawlsing_next.source_configuration import evidence as E  # noqa: E402

DATA_ROOT = ROOT / "rawlsing_next/source_configuration/data"
VAL_ROOT = ROOT / "source_pre553_validation"
SOURCE_IDS = ("SRC24", "SRC25", "SRC26")
FIXTURE_ROWS = 8


def phys_maps(sid: str):
    phys = list(E.iter_physical_slots(sid))
    return phys, {p["name"]: p for p in phys}


def has_substantive_labels(p: Mapping[str, Any]) -> bool:
    return any(L.response_state_for_label(str(label)) == "SUBSTANTIVE_RESPONSE"
               for label in (p.get("value_labels") or {}).values())


def coordinate_mode(p: Mapping[str, Any]) -> str:
    return "values" if has_substantive_labels(p) else "raw"


def is_binary_slot(p: Mapping[str, Any]) -> bool:
    labels = p.get("value_labels") or {}
    codes = set()
    for key in labels:
        try:
            codes.add(int(float(key)))
        except (TypeError, ValueError):
            pass
    substantive = {x for x in codes if x >= 0}
    return bool(substantive) and substantive <= {0, 1}


def classify(source_id: str, ctx: Mapping[str, Any]) -> dict[str, Any]:
    items = ctx["items"]
    crosswalk = ctx["crosswalk"]
    cbmap = {e["codebook_var_name"]: e["physical_names"] for e in crosswalk["codebook_entries"]}
    phys, phys_by_name = phys_maps(source_id)
    responses: list[dict[str, Any]] = []
    coordinates: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    weight_items: list[dict[str, Any]] = []

    for x in items:
        code = x["source_variable_code"]
        names = list(cbmap.get(code, []))
        relation = x.get("relation") or {}
        topology = relation.get("manual_response_topology")
        disposition = x["h48"]["disposition"]
        binding = x["p2"].get("response_binding_status")
        exact = x.get("relation_join_status") == "EXACT"
        has_values = bool(names) and all((phys_by_name[n].get("value_labels") or {}) for n in names)

        if disposition == "admin" or topology == "administrative":
            if code.casefold() == "wt" or (names and all(n.upper() == "WT" for n in names)):
                weight_items.append({"item": x, "slots": names, "reason": "WEIGHT_AUTHORITY_NOT_ESTABLISHED"})
                excluded.append({
                    "item_code": code, "slots": names,
                    "reason": "WEIGHT_AUTHORITY_NOT_ESTABLISHED",
                    "native_field": "weight_slots[].design_authority_ref / estimand_authority_ref",
                    "evidence": "The physical source carries a weight slot, but current evidence has no exact weight design, estimand or effective scope authority.",
                    "dependent_operation": "weighted/population estimation",
                })
                continue
            for name in names:
                p = phys_by_name[name]
                coordinates.append({
                    "slot": name, "item_code": code,
                    "mode": coordinate_mode(p),
                    "unit": "SOURCE_NATIVE_ADMIN_CONTEXT",
                    "note": "Source-native administrative/context field bound as a coordinate; not a measurement target.",
                })
            continue

        if topology == "scalar_coordinate":
            for name in names:
                p = phys_by_name[name]
                coordinates.append({
                    "slot": name, "item_code": code,
                    "mode": coordinate_mode(p),
                    "unit": "SOURCE_NATIVE_POSITION_COORDINATE",
                    "note": "Source item is a scalar coordinate; represented as a coordinate, not a finite response target.",
                })
            continue

        if topology in {"open_or_continuous", "open_continuous_context"}:
            if disposition in {"position_context", "structural_context", "admin"}:
                for name in names:
                    p = phys_by_name[name]
                    coordinates.append({
                        "slot": name, "item_code": code,
                        "mode": coordinate_mode(p),
                        "unit": "SOURCE_NATIVE_OPEN_CONTEXT_COORDINATE",
                        "note": "Open/continuous source context represented as raw coordinate; no finite categorical domain is invented.",
                    })
            else:
                excluded.append({
                    "item_code": code, "slots": names,
                    "reason": "OPEN_CONTINUOUS_RESPONSE_NO_FINITE_NATIVE_DOMAIN",
                    "native_field": "response_slots[].values (ResponseValueRule.physical_key)",
                    "evidence": "P2/manual topology=open_or_continuous; no finite declared value-label domain in physical evidence.",
                    "dependent_operation": "finite categorical native response construction",
                })
            continue

        if exact and binding == "bound" and topology and names and has_values:
            n = len(names)
            binary = all(is_binary_slot(phys_by_name[s]) for s in names)
            if n == 1:
                if topology == "binary_contrast":
                    layout = "binary"
                elif topology in {"multiselect_indicator", "ranking_or_multiselect"}:
                    layout = "multiselect"
                elif topology in {"nominal_choice", "nominal_position", "response_status"}:
                    layout = "single"
                else:
                    layout = "scalar"
            elif binary:
                layout = "multiselect"
            elif topology == "ranking_or_multiselect":
                layout = "ranked"
            else:
                layout = "multiselect"
            responses.append({
                "question_id": code, "item_code": code, "slots": names,
                "topology": topology, "layout": layout,
                "note": f"Source-native {topology} binding.",
            })
            continue

        reason = "OTHER_EVIDENCE_GAP"
        native_field = "items.relation / response_slots"
        evidence = "See H48/P2 evidence refs."
        dependent = "source-native response construction"
        if not exact:
            reason = "RELATION_ID_UNMATCHED"
            native_field = "items.relation.governed_row_payload_hash"
            evidence = "H48/P2 exact implementation identity exists, but the exact full-relation row is unmatched; no substitution is permitted."
            dependent = "relation-scoped semantic response use"
        elif binding != "bound":
            reason = "RESPONSE_BINDING_BLOCKED"
            native_field = "response_slots[].values / response binding"
            evidence = f"P2 response_binding_status={binding!r}; prior authority gap blocks a native response binding."
            dependent = "source-native response construction"
        elif not topology:
            reason = "TOPOLOGY_UNRESOLVED"
            native_field = "response_slots[].occurrences / multiplicity_order_rank_fields"
            evidence = "No exact manual/P2 response topology is recorded for this item."
            dependent = "native response topology construction"
        elif not names:
            reason = "NO_EXACT_PHYSICAL_COUNTERPART"
            native_field = "physical_slots[].name / response_slots[].slot"
            evidence = "No exact source physical slot corresponds to this implementation identity."
            dependent = "physical-to-native response construction"
        elif not has_values:
            reason = "NO_DECLARED_FINITE_VALUE_DOMAIN"
            native_field = "response_slots[].values (ResponseValueRule.physical_key)"
            evidence = "The mapped physical slot has no declared value labels; original respondent values were not read, so no finite non-invented response domain exists."
            dependent = "finite categorical native response construction"
        excluded.append({
            "item_code": code, "slots": names, "reason": reason,
            "native_field": native_field, "evidence": evidence,
            "dependent_operation": dependent,
        })

    used_slots = set()
    for r in responses:
        used_slots.update(r["slots"])
    for c in coordinates:
        used_slots.add(c["slot"])
    for e in excluded:
        used_slots.update(e["slots"])
    for w in weight_items:
        used_slots.update(w["slots"])
    extra_slot_reasons = {
        "P14ST.F": "Physical-only judiciary trust field; no current codebook row or implementation item; measurement identity not established.",
        "P52N": "Physical-only item with no current codebook row or implementation item; measurement identity not established.",
        "WT": "Source weight slot; design/estimand authority is not established.",
    }
    for p in phys:
        name = p["name"]
        if name in used_slots:
            continue
        if name in extra_slot_reasons:
            excluded.append({
                "item_code": None, "slots": [name],
                "reason": "PHYSICAL_ONLY_NO_ITEM_IDENTITY" if name != "WT" else "WEIGHT_AUTHORITY_NOT_ESTABLISHED",
                "native_field": "physical_slots[].codebook_mapping / items",
                "evidence": extra_slot_reasons[name],
                "dependent_operation": ("weighted estimation" if name == "WT"
                                        else "codebook-linked measurement response construction"),
            })
            continue
        coordinates.append({
            "slot": name, "item_code": None,
            "mode": coordinate_mode(p),
            "unit": "SOURCE_NATIVE_ADMIN_CONTEXT",
            "note": "Physical-only administrative/context slot bound as a raw coordinate; no item identity is invented.",
        })
        used_slots.add(name)

    included_slots = set()
    for r in responses:
        included_slots.update(r["slots"])
    for c in coordinates:
        included_slots.add(c["slot"])
    excluded_slots = set()
    for e in excluded:
        excluded_slots.update(e["slots"])
    if included_slots & excluded_slots:
        raise RuntimeError(f"{source_id}: slot both included and excluded: {included_slots & excluded_slots}")
    if included_slots | excluded_slots != {p["name"] for p in phys}:
        missing = sorted({p["name"] for p in phys} - (included_slots | excluded_slots))
        raise RuntimeError(f"{source_id}: physical slot partition is incomplete; missing={missing}")
    included_items = {r["item_code"] for r in responses} | {c["item_code"] for c in coordinates if c["item_code"]}
    excluded_items = {e["item_code"] for e in excluded if e["item_code"]}
    if included_items & excluded_items:
        raise RuntimeError(f"{source_id}: item both included and excluded")
    if included_items | excluded_items != {x["source_variable_code"] for x in items}:
        raise RuntimeError(f"{source_id}: item partition is incomplete")
    return {
        "responses": responses, "coordinates": coordinates, "excluded": excluded,
        "weight_items": weight_items,
        "included_slots": included_slots, "excluded_slots": excluded_slots,
        "included_items": included_items, "excluded_items": excluded_items,
    }


def coordinate_values(slot: Mapping[str, Any]) -> list[dict[str, Any]]:
    out = []
    for key, label in (slot.get("value_labels") or {}).items():
        try:
            code = int(float(key))
        except (TypeError, ValueError):
            continue
        state = L.response_state_for_label(str(label))
        coordinate_state = ("OBSERVED_COORDINATE" if state == "SUBSTANTIVE_RESPONSE"
                            else "MISSING" if state == "MISSING" else "UNKNOWN")
        out.append({
            "raw_value": float(code), "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None, "coordinate_state": coordinate_state,
            "canonical_value": None, "extra_authority_refs": [],
        })
    out.append({
        "raw_value": None, "missing_state": "SYSTEM_MISSING",
        "source_missing_declaration": None, "coordinate_state": "MISSING",
        "canonical_value": None, "extra_authority_refs": [],
    })
    return out


def response_occurrence(slot: Mapping[str, Any], plan: Mapping[str, Any], index: int, mode: str):
    layout = plan["layout"]
    if layout == "ranked":
        rank = index + 1
        component = L.exact_ref(
            "COMPONENT_SUBITEM",
            f"urn:rawlsing:r157:{mode}:{slot['source_id']}:{slot['name']}",
            L.sha_material({"source": slot["source_id"], "slot": slot["name"], "rank": rank}),
        )
        return f"rank_{rank}", rank, component, "RANKED_RESPONSE"
    if layout == "multiselect":
        component = None
        if len(plan["slots"]) > 1:
            component = L.exact_ref(
                "COMPONENT_SUBITEM",
                f"urn:rawlsing:r157:{mode}:{slot['source_id']}:{slot['name']}",
                L.sha_material({"source": slot["source_id"], "slot": slot["name"], "index": index}),
            )
        return f"component_{index + 1}", None, component, "UNORDERED_MULTISELECT_SET"
    if layout == "binary":
        return "0", None, None, "BINARY_CONTRAST"
    if layout == "single":
        kind = {
            "nominal_choice": "NOMINAL_CHOICE",
            "nominal_position": "NOMINAL_POSITION",
            "response_status": "RESPONSE_STATUS",
        }.get(plan["topology"], "SCALAR")
        return "0", None, None, kind
    return "0", None, None, "SCALAR"


def build_config(source_id: str, ctx: Mapping[str, Any], plan: Mapping[str, Any], *,
                 mode: str, fixture_meta: Mapping[str, Any] | None, crosswalk_sha: str) -> dict[str, Any]:
    roster = ctx["roster"]
    phys, phys_by_name = phys_maps(source_id)
    items = ctx["items"]
    item_by_code = {x["source_variable_code"]: x for x in items}
    crosswalk_by_physical = ctx["crosswalk_by_physical"]
    source_sha = roster["source_sha256"]
    wave = str(roster["wave"])
    fixture_id = fixture_meta["fixture_id"] if fixture_meta else None
    auths = L.build_authorities(source_id, source_sha, fixture_id=fixture_id, wave=wave)
    aref = {k: L.authority_ref(v) for k, v in auths.items()}
    universe_payload, universe_ref = L.make_universe(source_id, roster, auths, fixture_id=fixture_id, wave=wave)

    identity_class = "ORIGINAL_SOURCE" if mode == "original" else "NONRESPONDENT_FIXTURE"
    binding_sha = source_sha if mode == "original" else fixture_meta["fixture_source_sha256"]
    binding_rows = roster["rows"] if mode == "original" else fixture_meta["row_count"]

    physical_docs = []
    for p in phys:
        name = p["name"]
        entry = crosswalk_by_physical[name]
        cvar = entry["codebook_var_names"][0] if entry["codebook_var_names"] else None
        if name in plan["included_slots"]:
            if any(name in r["slots"] for r in plan["responses"]):
                disp, reason = "SUPPORTED_RESPONSE", "Exact source-native response binding."
            else:
                disp, reason = "SUPPORTED_COORDINATE", "Source-native coordinate/context binding."
        else:
            exc = next(e for e in plan["excluded"] if name in e["slots"])
            disp, reason = "HELD_EXACT_SOURCE_LIMITATION", exc["evidence"]
        physical_docs.append(L.physical_slot_doc(p, disp, reason, cvar))
    if mode == "fixture":
        physical_docs = [d for d in physical_docs if d["name"] in plan["included_slots"]]

    item_docs = []
    for x in items:
        code = x["source_variable_code"]
        if code in plan["excluded_items"]:
            if mode == "fixture":
                continue
            exc = next(e for e in plan["excluded"] if e.get("item_code") == code)
            doc = L.item_doc(x)
            doc["disposition"] = f"HELD_{exc['reason']}"
            doc["limits"] = list(doc["limits"]) + [exc["evidence"]]
            item_docs.append(doc)
            continue
        doc = L.item_doc(x)
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
            "question_id": r["question_id"],
            "empirical_universe_ref": universe_ref,
            "native_question_ref": L.exact_ref(
                "NATIVE_QUESTION",
                f"urn:rawlsing:r157:{mode}:{source_id}:item:{x['implementation_id']}",
                x["exact_identity_sha256"]),
            "instrument_question_version": wave,
            "canonical_question_ref_or_typed_absence": {
                "typed_absence_state": "NOT_AUTHORIZED",
                "detail": "No canonical adoption or directional certification is issued by this source preparation.",
            },
            "component_subitem_ref_or_typed_absence": {
                "typed_absence_state": "NOT_APPLICABLE", "detail": None},
            "semantic_authority_ref": aref["R157_PREPARE_SOURCE_ITEM_SEMANTICS"],
            "topology_authority_ref": aref["R157_PREPARE_SOURCE_TOPOLOGY"],
            "item_evidence": {
                "implementation_id": x["implementation_id"],
                "exact_identity_sha256": x["exact_identity_sha256"],
                "relation_join_status": x.get("relation_join_status"),
            },
        })

    response_slots = []
    for r in plan["responses"]:
        for index, slot_name in enumerate(r["slots"]):
            p = phys_by_name[slot_name]
            key, rank, component, topology_kind = response_occurrence(p, r, index, mode)
            response_slots.append({
                "slot": {"ordinal": p["ordinal"], "name": p["name"]},
                "question_id": r["question_id"],
                "values": L.slot_values(
                    p, topology=topology_kind, occurrence_prefix=key,
                    rank=rank, component_ref=component,
                    mapping_authority=aref["R157_MAP_SOURCE_CODE_TOKEN_IDENTITY"]),
            })

    coordinate_slots = []
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        mode_values = c["mode"] == "values" and bool(p.get("value_labels"))
        coordinate_slots.append({
            "slot": {"ordinal": p["ordinal"], "name": p["name"]},
            "native_coordinate_ref": L.exact_ref(
                "COORDINATE_NATIVE",
                f"urn:rawlsing:r157:{mode}:{source_id}:{p['name']}",
                L.sha_material({"source": source_id, "slot": p["name"], "mode": mode})),
            "unit_taxonomy_ref": L.exact_ref(
                "UNIT_TAXONOMY", f"urn:rawlsing:r157:{c['unit']}",
                L.sha_material({"unit": c["unit"]})),
            "effective_time": wave,
            "source_semantic_authority_ref": aref["R157_OBSERVE_SOURCE_NATIVE_COORDINATE_RAW"],
            "canonical_coordinate_ref": None, "normalization_ref": None,
            "values": coordinate_values(p) if mode_values else [],
            "copy_observed_raw": not mode_values,
        })

    routing = []
    for r in plan["responses"]:
        qid = r["question_id"]
        selector: Any = "ALL"
        routing.append({
            "question_id": qid, "row_selector": selector, "typed_state": "ROUTING_UNKNOWN",
            "risk_set_ref": L.exact_ref(
                "RISK_SET", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                L.sha_material({"source": source_id, "q": qid, "mode": mode, "r": "risk"})),
            "routing_rule_ref": L.exact_ref(
                "ROUTING_RULE", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                L.sha_material({"source": source_id, "q": qid, "mode": mode, "r": "rule"})),
            "member_set_replay_ref": L.exact_ref(
                "MEMBER_SET_REPLAY", f"urn:rawlsing:r157:{mode}:{source_id}:{qid}:unresolved",
                L.sha_material({"source": source_id, "q": qid, "mode": mode, "r": "member"})),
            "authority_ref": aref["R157_RECORD_UNRESOLVED_SOURCE_ROUTING"],
            "parent_predicate_refs": [], "dependency_refs": [],
        })

    included_ordinals = sorted(phys_by_name[n]["ordinal"] for n in plan["included_slots"])
    if mode == "original":
        excluded_slots = []
        for name in sorted(plan["excluded_slots"], key=lambda n: phys_by_name[n]["ordinal"]):
            exc = next(e for e in plan["excluded"] if name in e["slots"])
            excluded_slots.append({"ordinal": phys_by_name[name]["ordinal"], "name": name,
                                   "reason": exc["evidence"]})
        excluded_items = []
        for code in sorted(plan["excluded_items"]):
            exc = next(e for e in plan["excluded"] if e.get("item_code") == code)
            excluded_items.append({"implementation_id": item_by_code[code]["implementation_id"],
                                   "reason": exc["evidence"]})
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
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
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "partial_scope_reason": "Nonrespondent fixture slice covering every declared supported response and coordinate slot.",
            "not_a_lane_config": True,
        }

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
                "All inclusive items are source-native response or coordinate bindings; exclusions are exact limitations, not unselected canaries.",
                "Positive native C11 release is exercised by the separately identified nonrespondent fixture config.",
                "Routing remains SOURCE_ROUTING_UNRESOLVED; the portable recipe uses row_selector=ALL with ROUTING_UNKNOWN and is not physically expanded for original validation.",
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
    metadata_ref = L.exact_ref(
        "R154_PHYSICAL_METADATA",
        f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
        roster["metadata_witness"]["sha256"])
    field_evidence = [
        {"field": "identity.expected_source_sha256", "refs": [
            L.exact_ref("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha)]},
        {"field": "identity.metadata_witness_ref", "refs": [metadata_ref]},
        {"field": "correspondence", "refs": [
            L.exact_ref("SOURCE_CORRESPONDENCE",
                        f"rawlsing_next/source_configuration/data/{source_id}/crosswalk.json",
                        crosswalk_sha)]},
    ]
    for code in sorted(plan["included_items"]):
        x = item_by_code[code]
        refs = [
            L.exact_ref("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{x['implementation_id']}", x["exact_identity_sha256"]),
            L.exact_ref("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{x['implementation_id']}", x["exact_identity_sha256"]),
        ]
        if x.get("relation"):
            refs.append(L.exact_ref("FULL_RELATION_ROW",
                                    f"urn:rawlsing:r157:relation:{x['relation']['question_id']}",
                                    x["relation"]["governed_row_payload_hash"]))
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
        "limits": [
            "Prior H48/P2/full-relation evidence is reused with its original grades and limits.",
            "No original respondent rows, response values or source bytes were read.",
            "Fixture authority is not original-source authority.",
        ],
    }

    authority_section = {
        "snapshots": [auths[k] for k in sorted(auths)],
        "required_refs": [aref[k] for k in sorted(aref)],
        "projection_authority_ref": aref["R157_PREPARE_SOURCE_PROJECTION"],
        "replay_authority_ref": aref["R157_LOCAL_DETERMINISTIC_REPLAY"],
        "projection_identity_ref": L.exact_ref(
            "C11_SEMANTIC_PROJECTION",
            f"urn:rawlsing:r157:{mode}:{source_id}:projection",
            L.sha_material({"source": source_id, "sha": source_sha, "mode": mode, "questions": qids})),
        "tie_order_ref": L.exact_ref("ORDER_RULE", "urn:rawlsing:r157:canonical-ref-sort",
                                     L.sha_material({"rule": "canonical_ref_sort"})),
        "replay_protocol_version": "1.0.0",
    }

    identity = {
        "source_id": source_id, "family": roster["family"], "wave": wave,
        "source_family_id": roster["family"], "study_product_id": f"{roster['family']}:{wave}",
        "release_id": f"{source_id}_{L.WAVE_INSTRUMENT_PREFIX}_{wave}_PREPARATION",
        "instrument_release_id": f"{source_id}_INSTRUMENT_{L.WAVE_INSTRUMENT_PREFIX}_{wave}",
        "source_artifact_id": roster["source_artifact_id"],
        "expected_source_sha256": source_sha, "source_format": roster["format"],
        "source_row_count": roster["rows"], "source_column_count": roster["physical_columns"],
        "source_bytes": roster["bytes"], "codebook_rows": roster["codebook_rows"],
        "original_item_count": roster["original_items"],
        "source_snapshot_retention_ref": L.exact_ref(
            "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
        "metadata_witness_ref": metadata_ref,
        "locator": {"root": "EXTERNAL_LOCATOR_ID",
                    "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
        "reader": {
            "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
            "configuration_ref": L.exact_ref(
                "READER_CONFIGURATION", f"urn:rawlsing:r157:{source_id}:default_sav",
                L.sha_material({"source": source_id, "sha": source_sha, "reader": "default_sav"})),
            "encoding": None,
        },
    }

    if mode == "original":
        binding = {
            "identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
            "source_snapshot_ref": L.exact_ref(
                "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", source_sha),
        }
        respondents = {
            "subject_unit": "SOURCE_INTERVIEW_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:rows",
            "respondent_key_pattern": f"{source_id}-ROW-{{row_ordinal:05d}}",
            "source_native_key_slot": None, "identity_map_authority_ref": None,
            "row_identity_grade": "SOURCE_PHYSICAL_ROW_ORDINAL_ONLY",
        }
        config_id = f"R157-LATIN-{source_id}-FULL-SOURCE-PREPARATION"
        purpose = "SOURCE_PREPARATION"
    else:
        binding = {
            "identity_class": identity_class, "source_sha256": binding_sha, "row_count": binding_rows,
            "source_snapshot_ref": L.exact_ref(
                "FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:fixture:{fixture_meta['fixture_id']}", binding_sha),
            "fixture_provenance": {
                "fixture_id": fixture_meta["fixture_id"], "provenance": fixture_meta["provenance"],
                "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                "original_source_id": source_id, "original_source_sha256": source_sha,
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
            "source_native_key_slot": None, "identity_map_authority_ref": None,
            "row_identity_grade": "NONRESPONDENT_FIXTURE_ONLY",
        }
        config_id = f"R157-LATIN-{source_id}-NONRESPONDENT-FIXTURE-FULL"
        purpose = "NONRESPONDENT_FIXTURE"

    return {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id, "config_revision": 2, "config_purpose": purpose,
        "identity": identity, "binding": binding, "authority": authority_section,
        "universe": {"universes": [universe_payload]}, "respondents": respondents,
        "questions": questions, "physical_slots": physical_docs, "items": item_docs,
        "response_slots": response_slots, "coordinate_slots": coordinate_slots,
        "weight_slots": [], "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
            "comparator": {"typed_absence_state": "DEFERRED", "detail": None},
            "discovery": {"typed_absence_state": "DEFERRED", "detail": None},
            "structural": {"typed_absence_state": "NOT_APPLICABLE", "detail": None},
        },
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


def build_residuals(source_id: str, plan: Mapping[str, Any], mode: str) -> list[dict[str, str]]:
    residuals: list[dict[str, str]] = []
    if mode == "original":
        residuals.extend([
            {
                "residual_id": f"{source_id}-ROUTING-UNRESOLVED",
                "scope": source_id,
                "field": "routing.typed_state",
                "status": "UNKNOWN",
                "reason": f"SOURCE_ROUTING_UNRESOLVED for {len(plan['responses'])} response items. The portable recipe declares row_selector=ALL with typed_state ROUTING_UNKNOWN for every produced routing fact; it does not invent eligibility, forms, populations or permissions. The original source rows were not physically expanded for validation.",
                "dependent_operation": "eligibility/form-conditioned native query",
                "unaffected_scope": "unconditional source-native response incidence and coordinate binding",
                "owner": "LATIN lane / P3 integration owner",
                "next_step": "Recover exact indexed routing/form expressions before claiming eligibility-conditioned scope.",
            },
            {
                "residual_id": f"{source_id}-ROW-NATIVE-KEY",
                "scope": source_id,
                "field": "respondents.source_native_key_slot",
                "status": "UNKNOWN",
                "reason": "No exact decoded source-native respondent key witness exists in preparation; physical row ordinal is the only established key.",
                "dependent_operation": "respondent-key linkage or deduplication beyond row ordinal",
                "unaffected_scope": "row-ordinal-scoped source-native response and coordinate construction",
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
                "reason": "The source carries a weight slot, but no exact design/estimand authority or weighted scope is present in current evidence.",
                "dependent_operation": "population or weighted estimation",
                "unaffected_scope": "raw-sample source-native response incidence",
                "owner": "LATIN lane / P3 integration owner",
                "next_step": "Establish exact weight basis, design, estimand and effective scope before declaring a weighted slice.",
            },
            {
                "residual_id": f"{source_id}-DIRECTION",
                "scope": source_id,
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
        ])
        for exc in plan["excluded"]:
            code = exc.get("item_code")
            slot = exc["slots"][0] if exc["slots"] else "SOURCE_LEVEL"
            label = code or slot
            residuals.append({
                "residual_id": f"{source_id}-EXCLUDED-{label}",
                "scope": f"{source_id}/{label}",
                "field": exc["native_field"],
                "status": exc["reason"],
                "reason": exc["evidence"],
                "dependent_operation": exc["dependent_operation"],
                "unaffected_scope": "all other included source-native response and coordinate bindings",
                "owner": "LATIN lane / P3 integration owner",
                "next_step": "Preserve the exact limitation; acquire the named missing source/native fact before binding this item/slot.",
            })
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
    return residuals


def build_fixture(ctx: Mapping[str, Any], plan: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_id = ctx["source_id"]
    phys, phys_by_name = phys_maps(source_id)
    rows = FIXTURE_ROWS
    cells = []
    oracle_slots: dict[str, dict[str, list[Any]]] = {}
    for r in plan["responses"]:
        for slot_name in r["slots"]:
            p = phys_by_name[slot_name]
            labels = p.get("value_labels") or {}
            codes = []
            for key, label in labels.items():
                try:
                    codes.append(int(float(key)))
                except (TypeError, ValueError):
                    pass
            codes.sort()
            substantive = [c for c in codes if L.response_state_for_label(str(labels.get(str(float(c)), ""))) == "SUBSTANTIVE_RESPONSE"]
            specials = [c for c in codes if c not in substantive]
            sequence = substantive + specials + [None]
            oracle_slots[slot_name] = {"states": [], "raw_values": [], "canonical_values": []}
            for row in range(1, rows + 1):
                code = sequence[(row - 1) % len(sequence)]
                label = None
                if code is not None:
                    label = labels.get(str(float(code)), labels.get(str(code)))
                state = "MISSING" if code is None else L.response_state_for_label(label)
                canonical = L.canonical_token(code) if state == "SUBSTANTIVE_RESPONSE" else None
                cells.append({
                    "row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                    "raw_value": None if code is None else float(code),
                    "missing_state": "SYSTEM_MISSING" if code is None else "OBSERVED_STORAGE_VALUE",
                    "source_missing_declaration": None,
                })
                oracle_slots[slot_name]["states"].append(state)
                oracle_slots[slot_name]["raw_values"].append(None if code is None else float(code))
                oracle_slots[slot_name]["canonical_values"].append(canonical)
    for c in plan["coordinates"]:
        p = phys_by_name[c["slot"]]
        labels = p.get("value_labels") or {}
        substantive = []
        for key, label in labels.items():
            try:
                code = int(float(key))
            except (TypeError, ValueError):
                continue
            if L.response_state_for_label(str(label)) == "SUBSTANTIVE_RESPONSE":
                substantive.append(code)
        substantive.sort()
        for row in range(1, rows + 1):
            if c["mode"] == "values" and substantive:
                code = substantive[(row - 1) % len(substantive)]
                raw = float(code)
            else:
                raw = 1.0
            cells.append({
                "row_ordinal": row, "variable_ordinal": p["ordinal"], "variable_name": p["name"],
                "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
            })
    fixture_id = ctx["spec"]["fixture_id"]
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
    for data in oracle_slots.values():
        for state in data["states"]:
            state_counts[state] = state_counts.get(state, 0) + 1
    response_slot_count = sum(len(r["slots"]) for r in plan["responses"])
    oracle = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_ORACLE@1.0.0",
        "fixture_id": fixture_id,
        "fixture_source_sha256": fixture_sha,
        "row_count": rows,
        "expected": {
            "response_event_count": rows * response_slot_count,
            "coordinate_fact_count": rows * len(plan["coordinates"]),
            "routing_fact_count": rows * len(plan["responses"]),
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


def main() -> int:
    from rawlsing_next.source_configuration.schema import canonical_config_hash, validate_source_config
    for source_id in SOURCE_IDS:
        ctx = L.load_context(source_id)
        plan = classify(source_id, ctx)
        for entry in ctx["crosswalk"]["entries"]:
            entry["selected_for_supported_slice"] = entry["physical_name"] in plan["included_slots"]
        ctx["crosswalk"]["counts"]["selected_for_supported_slice"] = sum(
            1 for e in ctx["crosswalk"]["entries"] if e["selected_for_supported_slice"])
        data_dir = DATA_ROOT / source_id
        val_dir = VAL_ROOT / source_id
        data_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        crosswalk_sha, crosswalk_bytes = L.write_json(data_dir / "crosswalk.json", ctx["crosswalk"])
        ctx["crosswalk_sha256"] = crosswalk_sha
        original = build_config(source_id, ctx, plan, mode="original", fixture_meta=None,
                                crosswalk_sha=crosswalk_sha)
        validate_source_config(original)
        fixture_doc, oracle = build_fixture(ctx, plan)
        fixture_meta = {
            "fixture_id": ctx["spec"]["fixture_id"],
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "row_count": fixture_doc["row_count"],
            "provenance": "Repository-generated nonrespondent fixture for the R157 LATIN lane; no original respondents represented.",
            "fixture_study_product_id": f"R157_FIXTURE/{source_id}",
            "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
            "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
        }
        fixture_config = build_config(source_id, ctx, plan, mode="fixture", fixture_meta=fixture_meta,
                                      crosswalk_sha=crosswalk_sha)
        validate_source_config(fixture_config)
        field_evidence = L.build_field_evidence(ctx, original)
        artifacts = [("rawlsing_next/source_configuration/data/" + source_id + "/crosswalk.json",
                      crosswalk_sha, crosswalk_bytes)]
        for rel, value in (
            (f"rawlsing_next/source_configuration/data/{source_id}/source.config.json", original),
            (f"rawlsing_next/source_configuration/data/{source_id}/field_evidence.json", field_evidence),
            (f"source_pre553_validation/{source_id}/fixture.json", fixture_doc),
            (f"source_pre553_validation/{source_id}/fixture.config.json", fixture_config),
            (f"source_pre553_validation/{source_id}/fixture_oracle.json", oracle),
        ):
            digest, size = L.write_json(ROOT / rel, value)
            artifacts.append((rel, digest, size))
        manifest = {
            "schema": "PYAT_R157_LATIN_SOURCE_MANIFEST@1.0.0",
            "source_id": source_id, "family": ctx["roster"]["family"],
            "wave": str(ctx["roster"]["wave"]), "source_sha256": ctx["roster"]["source_sha256"],
            "config_sha256": canonical_config_hash(original),
            "fixture_config_sha256": canonical_config_hash(fixture_config),
            "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
            "counts": {
                "physical_slots": ctx["roster"]["physical_columns"],
                "original_items": ctx["roster"]["original_items"],
                "included_slots": len(original["coverage"]["physical_slots_included"]),
                "included_items": len(original["coverage"]["items_included"]),
                "excluded_slots": len(original["coverage"]["physical_slots_excluded"]),
                "excluded_items": len(original["coverage"]["items_excluded"]),
                "response_questions": len(plan["responses"]),
                "response_slots": len(original["response_slots"]),
                "coordinate_slots": len(original["coordinate_slots"]),
                "crosswalk_physical_entries": ctx["crosswalk"]["counts"]["physical_entries"],
                "crosswalk_codebook_entries": ctx["crosswalk"]["counts"]["codebook_entries"],
            },
            "artifacts": [{"path": p, "sha256": h, "bytes": b} for p, h, b in artifacts],
        }
        L.write_json(val_dir / "manifest.json", manifest)
        print(f"{source_id}: config={canonical_config_hash(original)} fixture={fixture_doc['fixture_source_sha256']} "
              f"included_slots={len(original['coverage']['physical_slots_included'])} "
              f"included_items={len(original['coverage']['items_included'])} "
              f"excluded_items={len(original['coverage']['items_excluded'])} "
              f"questions={len(plan['responses'])} response_slots={len(original['response_slots'])} "
              f"coords={len(original['coordinate_slots'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
