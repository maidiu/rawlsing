"""Additive SRC04 lane-B field repair builder.

Loads the accepted SRC04 config read-only, applies only source-grounded value
binding/missing-coordinate amendments, validates the result, and writes a
portable repaired config plus an all-181-slot ledger.  No original source bytes
or respondent rows are read.
"""
from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rawlsing_next.source_configuration.schema import canonical_config_hash, validate_source_config  # noqa: E402
from rawlsing_next.source_configuration import evidence as E  # noqa: E402

ACCEPTED = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
REPAIRED = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.json"
LEDGER = ROOT / "campaign_src04_completion/bindings/FIELD_REPAIR_LEDGER.json"
REPORT = ROOT / "campaign_src04_completion/bindings/FIELD_REPAIR_REPORT.json"
SLICE = ROOT / "campaign_a_src04/evidence/SLICE_SELECTION.json"
METADATA = ROOT / "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/SRC04_PHYSICAL_METADATA.json"

SCALE_FIELDS = [f"q{n}" for n in range(235, 245)]
DECILE_FIELDS = ["q715incomedeciles", "q716incomedeciles"]
CONTINUOUS_FIELDS = ["q715withoutmorocco", "q716withoutmorocco"]
UNRESOLVED_FIELDS = ["q217", *CONTINUOUS_FIELDS]
AGE_FIELD = "q701"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _value_template(config: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    slot = next(s for s in config["response_slots"] if s["slot"]["name"] == field)
    return slot["values"][0]


def _add_numeric_values(config: dict[str, Any], field: str, codes: list[int]) -> int:
    slot = next(s for s in config["response_slots"] if s["slot"]["name"] == field)
    existing = {float(v["raw_value"]) for v in slot["values"] if v.get("raw_value") is not None}
    template = deepcopy(slot["values"][0])
    added = 0
    for code in codes:
        if float(code) in existing:
            continue
        value = deepcopy(template)
        value["raw_value"] = float(code)
        value["missing_state"] = "OBSERVED_STORAGE_VALUE"
        value["source_missing_declaration"] = None
        value["response_state"] = "SUBSTANTIVE_RESPONSE"
        value["canonical_value"] = str(code)
        # Preserve the template's exact occurrence/transform authorities.
        slot["values"].append(value)
        added += 1
    return added


def _add_system_missing_coordinate(config: dict[str, Any], field: str) -> None:
    slot = next(s for s in config["coordinate_slots"] if s["slot"]["name"] == field)
    if any(v.get("raw_value") is None and v.get("missing_state") == "SYSTEM_MISSING"
           for v in slot.get("values") or []):
        return
    slot.setdefault("values", []).append({
        "raw_value": None,
        "missing_state": "SYSTEM_MISSING",
        "source_missing_declaration": None,
        "coordinate_state": "MISSING",
        "canonical_value": None,
        "extra_authority_refs": [],
    })


def build() -> dict[str, Any]:
    old = json.loads(ACCEPTED.read_text(encoding="utf-8"))
    config = deepcopy(old)
    config["config_id"] = f"{old['config_id']}-FIELD-REPAIR-B"
    config["config_revision"] = int(old["config_revision"]) + 1
    repairs: dict[str, Any] = {}

    for field in SCALE_FIELDS:
        added = _add_numeric_values(config, field, list(range(2, 10)))
        repairs[field] = {"kind": "ADD_EXACT_SCALE_CODES", "added": added,
                          "codes": list(range(2, 10))}
    for field in DECILE_FIELDS:
        added = _add_numeric_values(config, field, list(range(2, 10)))
        repairs[field] = {"kind": "ADD_DECILE_CODES", "added": added, "codes": list(range(2, 10))}
    _add_system_missing_coordinate(config, AGE_FIELD)
    repairs[AGE_FIELD] = {"kind": "ADD_SYSTEM_MISSING_COORDINATE_RULE", "added": 1}

    residuals = [r for r in config["residuals"] if not r["residual_id"].startswith("SRC04-FIELD-REPAIR-")]
    residuals.extend([
        {
            "residual_id": "SRC04-FIELD-REPAIR-q217",
            "scope": "SRC04/q217",
            "field": "response_slots[q217].values (ResponseValueRule.physical_key)",
            "status": "UNRESOLVED_EXACT_VALUE_LABELS_MISSING",
            "reason": "Campaign A records 38 observed q217 cells with no exact configured value rule. The retained codebook and physical value labels declare only 1,2,3,4,5,6,10,97,98,99; they do not provide exact labels for the observed residual codes, and a fresh source read is not authorized.",
            "dependent_operation": "native response binding for q217",
            "unaffected_scope": "all other SRC04 response/coordinate bindings",
            "owner": "SRC04 lane B / full-source grant owner",
            "next_step": "With the authenticated full SRC04 grant, inspect the exact residual value set and bind only declared source options.",
        },
        {
            "residual_id": "SRC04-FIELD-REPAIR-q715withoutmorocco",
            "scope": "SRC04/q715withoutmorocco",
            "field": "response_slots[q715withoutmorocco].values (ResponseValueRule.physical_key)",
            "status": "UNRESOLVED_FINITE_NATIVE_DOMAIN",
            "reason": "Continuous individual monthly income has only special labels (9999993..9999999) and 3529 Campaign A unbound observed cells. A finite ResponseValueRule set cannot represent unbounded source-currency income values without fabricating a categorical domain.",
            "dependent_operation": "native response binding for q715withoutmorocco",
            "unaffected_scope": "q715incomedeciles and all other SRC04 bindings",
            "owner": "SRC04 lane B / full-source grant owner",
            "next_step": "With the full grant, qualify a continuous/numeric owner representation or an exact observed-domain binding; do not invent income categories.",
        },
        {
            "residual_id": "SRC04-FIELD-REPAIR-q716withoutmorocco",
            "scope": "SRC04/q716withoutmorocco",
            "field": "response_slots[q716withoutmorocco].values (ResponseValueRule.physical_key)",
            "status": "UNRESOLVED_FINITE_NATIVE_DOMAIN",
            "reason": "Continuous family monthly income has only special labels (9999993..9999999) and 4547 Campaign A unbound observed cells. A finite ResponseValueRule set cannot represent unbounded source-currency income values without fabricating a categorical domain.",
            "dependent_operation": "native response binding for q716withoutmorocco",
            "unaffected_scope": "q716incomedeciles and all other SRC04 bindings",
            "owner": "SRC04 lane B / full-source grant owner",
            "next_step": "With the full grant, qualify a continuous/numeric owner representation or an exact observed-domain binding; do not invent income categories.",
        },
    ])
    config["residuals"] = residuals
    config.setdefault("notes", []).extend([
        "Lane B additive repair preserves the accepted source.config.json; it adds exact codebook scale/decile codes and a system-missing age coordinate rule.",
        "q217 and continuous q715withoutmorocco/q716withoutmorocco remain exact residuals requiring the pending full-source grant.",
    ])
    validate_source_config(config)
    return {"old": old, "config": config, "repairs": repairs}


def ledger(old: Mapping[str, Any], config: Mapping[str, Any], repairs: Mapping[str, Any]) -> dict[str, Any]:
    slice_data = json.loads(SLICE.read_text(encoding="utf-8"))
    unbound = {s["name"]: s for s in slice_data["response_slots"] if s.get("status") != "INCLUDED_IN_FIRST_ELIGIBLE_SLICE"}
    coords = {s["name"]: s for s in slice_data["coordinate_slots"]}
    old_items = {i["source_variable_code"]: i for i in old["items"]}
    new_items = {i["source_variable_code"]: i for i in config["items"]}
    old_resp = {s["slot"]["name"] for s in old["response_slots"]}
    new_resp = {s["slot"]["name"] for s in config["response_slots"]}
    old_coord = {s["slot"]["name"] for s in old["coordinate_slots"]}
    new_coord = {s["slot"]["name"] for s in config["coordinate_slots"]}
    entries = []
    for p in old["physical_slots"]:
        name = p["name"]
        if name in repairs:
            status = "REPAIRED" if name not in UNRESOLVED_FIELDS else "UNRESOLVED_EXACT"
        elif name in UNRESOLVED_FIELDS:
            status = "UNRESOLVED_EXACT"
        else:
            status = "PRESERVED"
        old_rule_count = 0
        new_rule_count = 0
        for section in ("response_slots", "coordinate_slots"):
            for s in old[section]:
                if s["slot"]["name"] == name:
                    old_rule_count = len(s.get("values") or [])
            for s in config[section]:
                if s["slot"]["name"] == name:
                    new_rule_count = len(s.get("values") or [])
        entries.append({
            "ordinal": p["ordinal"],
            "name": name,
            "kind": "RESPONSE" if name in new_resp else "COORDINATE" if name in new_coord else "UNBOUND",
            "old_kind": "RESPONSE" if name in old_resp else "COORDINATE" if name in old_coord else "UNBOUND",
            "status": status,
            "repair": repairs.get(name),
            "old_value_rule_count": old_rule_count,
            "new_value_rule_count": new_rule_count,
            "campaign_a_unbound_cells": unbound.get(name, {}).get("unbound_cells", 0),
            "campaign_a_nonobserved_cells": (unbound.get(name) or coords.get(name, {})).get("nonobserved_cells", 0),
            "codebook_row_hash": p.get("codebook_mapping", {}).get("row_hash"),
            "item_implementation_id": old_items.get(name, {}).get("implementation_id"),
            "evidence_refs": old_items.get(name, {}).get("evidence_refs", []),
            "remaining_premise": (
                "exact observed residual value labels unavailable without full source grant" if name in UNRESOLVED_FIELDS
                else None
            ),
        })
    return {
        "schema": "PYAT_SRC04_FIELD_REPAIR_LEDGER@1.0.0",
        "source_id": "SRC04",
        "source_sha256": old["identity"]["expected_source_sha256"],
        "old_config_canonical_sha256": canonical_config_hash(old),
        "new_config_canonical_sha256": canonical_config_hash(config),
        "old_config_file_sha256": sha(ACCEPTED),
        "counts": {
            "physical_slots": len(old["physical_slots"]),
            "old_responses": len(old_resp),
            "new_responses": len(new_resp),
            "old_coordinates": len(old_coord),
            "new_coordinates": len(new_coord),
            "repaired_fields": len(repairs),
            "unresolved_fields": len(UNRESOLVED_FIELDS),
        },
        "entries": entries,
        "limits": [
            "No original SAV stat/hash/open/decode occurred in this lane; Campaign A retained metadata/selection evidence was used.",
            "No respondent rows or raw unbound cells are present in this ledger.",
            "Schema validation is not native original-source qualification; the full-source grant remains pending.",
        ],
    }


def evidence_record(old: Mapping[str, Any], config: Mapping[str, Any], repairs: Mapping[str, Any]) -> dict[str, Any]:
    slice_data = json.loads(SLICE.read_text(encoding="utf-8"))
    cb = {c["var_name"]: c for c in E.iter_codebook_rows("SRC04")}
    phys = {p["name"]: p for p in old["physical_slots"]}
    resp_unbound = {s["name"]: s for s in slice_data["response_slots"]}
    coord_unbound = {s["name"]: s for s in slice_data["coordinate_slots"]}
    fields = list(repairs) + UNRESOLVED_FIELDS
    entries = []
    for field in fields:
        p = phys[field]
        c = cb[field]
        campaign = resp_unbound.get(field) or coord_unbound.get(field) or {}
        decision = repairs.get(field)
        if field in UNRESOLVED_FIELDS:
            basis = "declared codebook/physical labels do not cover the observed residual finite domain"
        elif field == AGE_FIELD:
            basis = "age is a continuous coordinate; a system-missing coordinate rule is source-supported while raw observed ages remain copy-through"
        elif field in DECILE_FIELDS:
            basis = "codebook declares approximated income deciles with first/tenth endpoint labels; intermediate integer deciles 2-9 are admitted by the decile construct"
        else:
            basis = "codebook explicitly lists integer scale options 2-9; the physical slot labels only endpoints/specials"
        entries.append({
            "field": field,
            "physical": {"ordinal": p["ordinal"], "label": p["label"], "storage_type": p["storage_type"],
                         "original_type": p["original_type"], "value_labels": p["value_labels"],
                         "missing_declarations": p["missing_declarations"]},
            "codebook": {"row_hash": c["row_hash"], "question_text": c["question_text"],
                         "response_options_all": c["response_options_all"]},
            "campaign_a": {"unbound_cells": campaign.get("unbound_cells"),
                           "nonobserved_cells": campaign.get("nonobserved_cells"),
                           "status": campaign.get("status")},
            "repair_decision": decision,
            "unresolved": field in UNRESOLVED_FIELDS,
            "evidence_basis": basis,
            "evidence_refs": [{"kind": "ACCEPTED_SRC04_CONFIG", "sha256": sha(ACCEPTED)},
                              {"kind": "CAMPAIGN_A_SLICE_SELECTION", "sha256": sha(SLICE)},
                              {"kind": "R154_PHYSICAL_METADATA",
                               "sha256": hashlib.sha256(METADATA.read_bytes()).hexdigest()}],
        })
    return {"schema": "PYAT_SRC04_FIELD_REPAIR_EVIDENCE@1.0.0", "source_id": "SRC04",
            "source_sha256": old["identity"]["expected_source_sha256"],
            "entries": entries,
            "limits": ["Nonidentifying declared labels/counts only; no respondent cells.",
                       "Campaign A counts are retained evidence, not re-derived source reads."]}


def main() -> int:
    built = build()
    old, config, repairs = built["old"], built["config"], built["repairs"]
    REPAIRED.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    led = ledger(old, config, repairs)
    LEDGER.write_text(json.dumps(led, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = {
        "schema": "PYAT_SRC04_FIELD_REPAIR_REPORT@1.0.0",
        "source_id": "SRC04",
        "status": "CONFIG_REPAIRED_AWAITING_FULL_SOURCE_GRANT",
        "old_config_path": str(ACCEPTED.relative_to(ROOT)),
        "old_config_canonical_sha256": canonical_config_hash(old),
        "old_config_file_sha256": sha(ACCEPTED),
        "repaired_config_path": str(REPAIRED.relative_to(ROOT)),
        "repaired_config_canonical_sha256": canonical_config_hash(config),
        "repaired_config_file_sha256": sha(REPAIRED),
        "ledger_path": str(LEDGER.relative_to(ROOT)),
        "ledger_sha256": sha(LEDGER),
        "repairs": repairs,
        "unresolved_fields": UNRESOLVED_FIELDS,
        "counts": led["counts"],
        "validation": {"schema_validation": "PASSED", "native_original_qualification": "NOT_RUN_NO_FULL_SOURCE_GRANT"},
        "commands": [
            "PYTHONPATH=. python3 campaign_src04_completion/bindings/source_config_repair.py",
            "PYTHONPATH=. python3 -m pytest campaign_src04_completion/bindings/test_source_config_repair.py -q -o addopts=''",
        ],
        "limits": led["limits"],
    }
    ev = evidence_record(old, config, repairs)
    EVIDENCE = ROOT / "campaign_src04_completion/bindings/FIELD_REPAIR_EVIDENCE.json"
    EVIDENCE.write_text(json.dumps(ev, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["evidence_path"] = str(EVIDENCE.relative_to(ROOT))
    report["evidence_sha256"] = sha(EVIDENCE)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"old={report['old_config_canonical_sha256']}")
    print(f"new={report['repaired_config_canonical_sha256']}")
    print(f"ledger={report['ledger_sha256']}")
    print(f"counts={led['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
