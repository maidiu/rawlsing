#!/usr/bin/env python3
"""Materialize the actual q217-only successor config v3 from exact repaired-v2.

No source body is opened. No live producer selection is changed. This is an
additive, selectable artifact under this owned mapping return.
"""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_r157_projection_adapter import (
    canonical_config_hash, load_source_config,
)

V2 = ROOT / "WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json"
V2_FILE = "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5"
V2_CANON = "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d"
V3 = HERE / "source.config.repaired.v3.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if sha(V2) != V2_FILE:
        raise SystemExit("V2_FILE_DRIFT")
    old = load_source_config(V2)
    if canonical_config_hash(old) != V2_CANON:
        raise SystemExit("V2_CANONICAL_DRIFT")
    doc = copy.deepcopy(old.document)
    # q217 only: add source-questionnaire label 7=Other; add typed special rule;
    # correct 99=Decline to Answer to REFUSAL. All other fields are preserved.
    slot = next(x for x in doc["physical_slots"] if x.get("name") == "q217")
    labels = dict(slot.get("value_labels") or {})
    labels["7.0"] = "Other"
    slot["value_labels"] = labels
    rslot = next(x for x in doc["response_slots"] if x.get("question_id") == "q217")
    values = rslot["values"]
    if any(float(v["raw_value"]) == 7.0 for v in values if v.get("raw_value") is not None):
        raise SystemExit("CODE_7_ALREADY_PRESENT")
    template = copy.deepcopy(next(v for v in values if float(v["raw_value"]) == 10.0))
    template.update({
        "raw_value": 7.0, "missing_state": "OBSERVED_STORAGE_VALUE",
        "source_missing_declaration": None,
        "response_state": "SOURCE_SPECIFIC_SPECIAL",
        "canonical_value": None, "transform_authority_ref": None,
        "extra_authority_refs": [],
    })
    values.append(template)
    rslot["values"] = sorted(
        values,
        key=lambda v: (v.get("raw_value") is None,
                       float(v["raw_value"]) if v.get("raw_value") is not None else 0.0),
    )
    code99 = next(v for v in rslot["values"] if float(v["raw_value"]) == 99.0)
    code99["response_state"] = "REFUSAL"
    code99["canonical_value"] = None
    code99["transform_authority_ref"] = None
    V3.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    new = load_source_config(V3)
    # Field-level diff: every physical/response/other semantic field except q217
    # must be identical.
    old_doc = old.document; new_doc = new.document
    old_phys = [x for x in old_doc["physical_slots"] if x.get("name") != "q217"]
    new_phys = [x for x in new_doc["physical_slots"] if x.get("name") != "q217"]
    old_resp = [x for x in old_doc["response_slots"] if x.get("question_id") != "q217"]
    new_resp = [x for x in new_doc["response_slots"] if x.get("question_id") != "q217"]
    stable = {
        "physical_slots_stable": old_phys == new_phys,
        "response_slots_stable": old_resp == new_resp,
        "questions_stable": old_doc["questions"] == new_doc["questions"],
        "coordinates_stable": old_doc["coordinate_slots"] == new_doc["coordinate_slots"],
        "weights_stable": old_doc["weight_slots"] == new_doc["weight_slots"],
        "routing_stable": old_doc["routing"] == new_doc["routing"],
        "identity_stable": old_doc["identity"] == new_doc["identity"],
        "binding_stable": old_doc["binding"] == new_doc["binding"],
    }
    if not all(stable.values()):
        raise SystemExit(f"NON_Q217_DRIFT:{json.dumps(stable)}")
    payload = {
        "schema": "ANVIL_SRC04_Q217_CONFIG_V3@1",
        "status": "SELECTABLE_SUCCESSOR_NOT_LIVE_SELECTED",
        "scope": "Q217_ONLY__180_PHYSICAL_SLOTS_AND_ALL_NON_Q217_SEMANTICS_UNCHANGED__SOURCE_BODY_NOT_READ",
        "base_v2": {"path": str(V2.relative_to(ROOT)), "file_sha256": V2_FILE, "canonical_sha256": V2_CANON},
        "v3": {"path": str(V3.relative_to(ROOT)), "file_sha256": sha(V3), "canonical_sha256": canonical_config_hash(new)},
        "q217": {
            "labels_added": {"7.0": "Other"},
            "label_source": "PRIMARY_SOURCE_QUESTIONNAIRE_SCAN_PAGE_5__Q217__7_OTHER",
            "code_7_state": "SOURCE_SPECIFIC_SPECIAL",
            "code_7_canonical": None,
            "code_99_state": "REFUSAL",
            "code_97_98_state": "DK",
            "system_missing_state": "MISSING",
            "substantive_known_codes": ["1.0","2.0","3.0","4.0","5.0","6.0","10.0"],
        },
        "field_diff": stable,
        "physical_slots_total": len(new_doc["physical_slots"]),
        "physical_slots_unchanged": len(old_phys),
        "response_slots_total": len(new_doc["response_slots"]),
        "response_slots_unchanged": len(old_resp),
        "live_selection_changed": False,
        "accepted_config_replaced": False,
        "original_source_file_touched": False,
    }
    (HERE / "evidence/q217_v3_validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (HERE / "successor_reference.json").write_text(json.dumps({
        "schema": "ANVIL_SRC04_Q217_SELECTABLE_SUCCESSOR_REF@1",
        "status": "SELECTABLE_NOT_LIVE_SELECTED",
        "source_id": "SRC04", "wave": "I",
        "config": payload["v3"],
        "base_v2": payload["base_v2"],
        "scope": payload["scope"],
        "selection": "DO_NOT_REPLACE_LIVE_SHARED_CONFIG_SELECTION_BEFORE_RECEIVING",
        "original_source_file": "UNTOUCHED",
        "q217_only": True,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"], "v3": payload["v3"], "field_diff": stable, "q217": payload["q217"]}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
