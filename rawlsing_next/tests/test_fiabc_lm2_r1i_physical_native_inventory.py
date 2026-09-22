from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

from rawlsing_next.fiabc_lm2_r1e_browser_prep import validate_frozen_response_carrier
from rawlsing_next.fiabc_lm2_r1e_common_c11 import _materializer, _read_json, _structural_material
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, classify_physical_value
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_json
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key

ROOT = Path(__file__).resolve().parents[2]
CARRIER = ROOT / "WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json"
QUESTIONS = ("Q291G5", "Q291P5")
CODEC = R5TypedValueCodec()

def _j(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def _inventory():
    validate_frozen_response_carrier(CARRIER)
    doc = json.loads(CARRIER.read_text(encoding="ascii"))
    module = _materializer()
    structural_doc, variables, _country = _structural_material(module)
    qvars = {v.name: v for v in variables if v.name in QUESTIONS}
    out = {}
    for q in QUESTIONS:
        by = {}
        variable = qvars[q]
        for row in doc["rows"]:
            cell = row[q]
            witness = cell["raw_physical_value_witness"]["$raw_physical_value"]
            token = witness["token"]
            raw = CODEC.decode(token)
            state, decl = classify_physical_value(raw, variable.missing_declarations)
            assert cell["physical_missing_state"] == state.value
            packed_decl = None if decl is None else module._pack_missing_declaration(decl)
            assert cell["source_missing_declaration"] == packed_decl
            key = physical_value_binding_key(raw, state, decl)
            identity = (_j(token), state.value, _j(decl), key)
            rec = by.get(identity)
            if rec is None:
                rec = {
                    "typed_raw_token": token,
                    "python_type_after_codec_decode": type(raw).__name__,
                    "physical_missing_state": state.value,
                    "source_missing_declaration": decl,
                    "carrier_packed_source_missing_declaration": cell["source_missing_declaration"],
                    "physical_value_binding_key": key,
                    "occurrence_count": 0,
                    "first_row_ordinal": row["row_ordinal"],
                    "last_row_ordinal": row["row_ordinal"],
                }
                by[identity] = rec
            rec["occurrence_count"] += 1
            rec["last_row_ordinal"] = row["row_ordinal"]
        out[q] = sorted(by.values(), key=lambda x: (_j(x["typed_raw_token"]), x["physical_missing_state"], x["physical_value_binding_key"]))
    return out

def _rule_inventory():
    module = _materializer()
    structural_doc, variables, country = _structural_material(module)
    projection = module.materialize_from_structural_input(structural_doc)
    qvars = {v.name: v for v in variables if v.name in QUESTIONS}
    slots = {s.slot.name: s for s in projection.response_slots}
    out = {}
    for q in QUESTIONS:
        variable = qvars[q]
        constructions = {}
        for code in module.SUBSTANTIVE_CODES:
            state, decl = classify_physical_value(code, variable.missing_declarations)
            key = physical_value_binding_key(code, state, decl)
            constructions[key] = {
                "construction_class": "SUBSTANTIVE_CODE",
                "python_source_type": type(code).__name__,
                "python_source_repr": repr(code),
                "codec_token": CODEC.encode(code),
                "physical_missing_state": state.value,
                "source_missing_declaration": decl,
            }
        for code, semantic_state in module.SPECIAL_RESPONSE_STATES.items():
            state, decl = classify_physical_value(code, variable.missing_declarations)
            key = physical_value_binding_key(code, state, decl)
            constructions[key] = {
                "construction_class": "SPECIAL_SOURCE_CODE",
                "python_source_type": type(code).__name__,
                "python_source_repr": repr(code),
                "codec_token": CODEC.encode(code),
                "physical_missing_state": state.value,
                "source_missing_declaration": decl,
                "declared_response_state": semantic_state,
            }
        skey = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
        constructions[skey] = {
            "construction_class": "SYSTEM_MISSING",
            "python_source_type": "NoneType",
            "python_source_repr": "None",
            "codec_token": CODEC.encode(None),
            "physical_missing_state": PhysicalMissingState.SYSTEM_MISSING.value,
            "source_missing_declaration": None,
        }
        records = []
        for rule in slots[q].values:
            c = constructions.get(rule.physical_key, {"construction_class":"UNRECONSTRUCTED_FROM_CURRENT_MATERIALIZER_CONSTANTS"})
            records.append({
                "physical_value_binding_key": rule.physical_key,
                "construction_preimage": c,
                "response_state": rule.response_state,
                "canonical_value": rule.canonical_value,
                "transform_authority": None if rule.transform_authority_ref is None else rule.transform_authority_ref.as_dict(),
                "extra_authorities": [x.as_dict() for x in rule.extra_authority_refs],
            })
        out[q] = sorted(records, key=lambda x: x["physical_value_binding_key"])
    return out

def test_r1i_exact_keyspace_inventory_and_difference(capsys):
    physical = _inventory()
    rules = _rule_inventory()
    diff = {}
    for q in QUESTIONS:
        p = {x["physical_value_binding_key"]: x for x in physical[q]}
        r = {x["physical_value_binding_key"]: x for x in rules[q]}
        p_minus = [p[k] for k in sorted(set(p)-set(r))]
        r_minus = [r[k] for k in sorted(set(r)-set(p))]
        both = sorted(set(p)&set(r))
        diff[q] = {
            "physical_key_count": len(p),
            "rule_key_count": len(r),
            "intersection_count": len(both),
            "physical_minus_rule": p_minus,
            "rule_minus_physical": r_minus,
            "intersection_keys": both,
        }
    assert physical_value_binding_key(1, PhysicalMissingState.OBSERVED_STORAGE_VALUE) != physical_value_binding_key(1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    module = _materializer()
    structural_doc, variables, _country = _structural_material(module)
    metadata = {
        v.name: {
            "ordinal": v.ordinal,
            "storage_type": v.storage_type,
            "missing_declarations": v.missing_declarations,
        }
        for v in variables if v.name in QUESTIONS
    }
    summary = {
        q: {
            "physical_key_count": diff[q]["physical_key_count"],
            "rule_key_count": diff[q]["rule_key_count"],
            "intersection_count": diff[q]["intersection_count"],
            "physical_minus_rule_count": len(diff[q]["physical_minus_rule"]),
            "rule_minus_physical_count": len(diff[q]["rule_minus_physical"]),
            "physical_token_types": sorted({x["typed_raw_token"]["t"] for x in physical[q]}),
            "physical_python_types": sorted({x["python_type_after_codec_decode"] for x in physical[q]}),
            "realized_system_missing": any(x["physical_missing_state"] == "SYSTEM_MISSING" for x in physical[q]),
        }
        for q in QUESTIONS
    }
    with capsys.disabled():
        print("FIABC_LM2_R1I_PHYSICAL_INVENTORY="+_j(physical))
        print("FIABC_LM2_R1I_RULE_INVENTORY="+_j(rules))
        print("FIABC_LM2_R1I_KEYSPACE_DIFF="+_j(diff))
        print("FIABC_LM2_R1I_STRUCTURAL_METADATA="+_j(metadata))
        print("FIABC_LM2_R1I_DIFF_SUMMARY="+_j(summary))
