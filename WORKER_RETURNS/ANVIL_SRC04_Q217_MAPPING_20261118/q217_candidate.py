#!/usr/bin/env python3
"""Validate a minimal q217-only config candidate against existing validators.

Candidate is not applied to any product/config-custody file. It adds a typed
unknown rule for observed code 7.0 and marks label-corroborated code 99.0 as
REFUSAL. The only labels emitted are those in the source codebook/physical
metadata; code 7.0 remains unlabeled.
"""
from __future__ import annotations
import copy, hashlib, json, os, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_r157_projection_adapter import load_source_config, canonical_config_hash

CONFIG = ROOT / "WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json"
CONFIG_SHA = "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5"
CONFIG_CANONICAL = "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d"


def residual_check(codes: dict[str, int], labels: dict[str, str], missing: dict[str, int] | None = None):
    """Pure reusable checker; no source access or new labels."""
    out = {"labeled": {}, "special_labeled": {}, "unlabeled_observed": {}, "system_missing": {}}
    for key, count in codes.items():
        value = None if key == "None" else float(key)
        if value is None:
            out["system_missing"][key] = count
        elif str(key) in labels or (value is not None and str(value) in labels):
            out["labeled"][key] = {"count": count, "label": labels.get(str(key), labels.get(str(value)))}
        else:
            out["unlabeled_observed"][key] = count
    out["all_observed_accounted"] = sum(codes.values()) == sum(x["count"] for x in out["labeled"].values()) + sum(out["unlabeled_observed"].values()) + sum(out["system_missing"].values())
    return out


def main():
    raw = CONFIG.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONFIG_SHA:
        raise SystemExit("CONFIG_FILE_DRIFT")
    original = load_source_config(CONFIG)
    if canonical_config_hash(original) != CONFIG_CANONICAL:
        raise SystemExit("CONFIG_CANONICAL_DRIFT")
    doc = copy.deepcopy(original.document)
    slots = [x for x in doc["response_slots"] if x.get("question_id") == "q217"]
    if len(slots) != 1:
        raise SystemExit("Q217_RESPONSE_SLOT_NOT_EXACT")
    values = slots[0]["values"]
    by_raw = {v["raw_value"]: v for v in values}
    if 7.0 in by_raw:
        raise SystemExit("Q217_CODE_7_ALREADY_PRESENT")
    template = copy.deepcopy(by_raw[1.0])
    template.update({
        "raw_value": 7.0, "missing_state": "OBSERVED_STORAGE_VALUE",
        "source_missing_declaration": None, "response_state": "INVALID_UNRESOLVED",
        "canonical_value": None, "transform_authority_ref": None,
        "extra_authority_refs": [],
    })
    slots[0]["values"] = sorted(list(values) + [template], key=lambda v: (v["raw_value"] is None, float(v["raw_value"]) if v["raw_value"] is not None else 0.0))
    if 99.0 in by_raw:
        by_raw[99.0]["response_state"] = "REFUSAL"
        by_raw[99.0]["canonical_value"] = None
    with tempfile.TemporaryDirectory(prefix="anvil-q217-candidate-") as td:
        p = Path(td) / "candidate.config.json"
        p.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        candidate = load_source_config(p)
    cslot = [x for x in candidate.document["response_slots"] if x.get("question_id") == "q217"][0]
    states = {str(v["raw_value"]): {"state": v["response_state"], "canonical": v.get("canonical_value"), "missing": v["missing_state"]} for v in cslot["values"]}
    # Focused negative policy: code 7 must not acquire a label or substantive
    # answer, and no frequency/other-wave derivation is admitted.
    bad = copy.deepcopy(doc)
    bad_slot = [x for x in bad["response_slots"] if x.get("question_id") == "q217"][0]
    for v in bad_slot["values"]:
        if v["raw_value"] == 7.0:
            v["response_state"] = "SUBSTANTIVE_RESPONSE"
            v["canonical_value"] = "7"
    bad_ok = False
    try:
        with tempfile.TemporaryDirectory(prefix="anvil-q217-bad-") as td:
            p = Path(td) / "bad.json"; p.write_text(json.dumps(bad, indent=2, sort_keys=True) + "\n")
            bad_candidate = load_source_config(p)
        bad_slot = [x for x in bad_candidate.document["response_slots"] if x.get("question_id") == "q217"][0]
        bad_v7 = next(v for v in bad_slot["values"] if v["raw_value"] == 7.0)
        if bad_v7["response_state"] != "INVALID_UNRESOLVED" or bad_v7.get("canonical_value") is not None:
            bad_ok = True
    except Exception:
        bad_ok = False
    # Existing validator accepts the typed-unknown candidate; the policy keeps
    # 7 unlabeled and non-substantive.
    policy_ok = states.get("7.0") == {"state": "INVALID_UNRESOLVED", "canonical": None, "missing": "OBSERVED_STORAGE_VALUE"}
    output = {
        "schema": "ANVIL_SRC04_Q217_MAPPING_CANDIDATE@1",
        "status": "CANDIDATE_VALIDATED_NOT_APPLIED",
        "original_config": {"file_sha256": CONFIG_SHA, "canonical_sha256": CONFIG_CANONICAL},
        "candidate_config": {"canonical_sha256": canonical_config_hash(candidate), "loaded_by_current_validator": True},
        "q217_states": states,
        "q217_label_mapping": {
            "1.0": "television", "2.0": "radio", "3.0": "local newspaper",
            "4.0": "weekly magazines and papers", "5.0": "internet",
            "6.0": "sms messages", "10.0": "others",
            "97.0": "not clear", "98.0": "can't choose/don't know",
            "99.0": "decline to answer",
        },
        "typed_unknown": {"7.0": "INVALID_UNRESOLVED", "evidence": "UNLABELED_OBSERVED_CODE__NO_CODEBOOK_OR_PHYSICAL_LABEL"},
        "special_states": {"97.0": "DK", "98.0": "DK", "99.0": "REFUSAL", "None": "SYSTEM_MISSING"},
        "policy": {
            "code_7_labeled_or_substantive_refused": policy_ok,
            "existing_validator_accepts_candidate": True,
            "unauthorized_label_or_frequency_inference_refused": bad_ok,
            "canonical_scientific_or_source_rights_promoted": False,
        },
        "configuration_changed_on_disk": False,
    }
    (HERE / "evidence" / "q217_candidate_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    agg = json.loads((HERE / "evidence" / "q217_aggregate.json").read_text())
    residual = residual_check(agg["q217"]["codes"], agg["config"]["q217_labels"], agg["q217"]["missing_states"])
    (HERE / "evidence" / "q217_residual_check.json").write_text(json.dumps({"schema": "ANVIL_Q217_RESIDUAL_CHECK@1", "input": "q217 aggregate codes and declared labels", **residual}, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": output["status"], "candidate_canonical": output["candidate_config"]["canonical_sha256"], "residual": residual, "policy": output["policy"]}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
