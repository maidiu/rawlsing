"""Isolated q101 code-99 correction and aggregate retained-tally replay.

Reads only metadata, an accepted aggregate tally, and response-option authority.
It does not open the SRC04 SAV, read respondent rows, issue a workload, or adopt
the corrected configuration into production.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--option-authority", required=True)
    parser.add_argument("--tally-product", required=True)
    parser.add_argument("--routing-receipt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--overlay", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(args.package_root).resolve()))

    from rawlsing_next.source_configuration.schema import (
        canonical_config_hash,
        load_source_config,
        validate_source_config,
    )

    source = load_source_config(Path(args.source_config))
    original = copy.deepcopy(dict(source.document))
    corrected = copy.deepcopy(original)
    tally = read_json(Path(args.tally_product))
    routing = read_json(Path(args.routing_receipt))

    q101_slot = next(
        slot for slot in corrected["response_slots"] if slot["question_id"] == "q101")
    code99 = next(
        value for value in q101_slot["values"]
        if value.get("raw_value") in (99, 99.0, "99", "99.0"))
    old_state = code99["response_state"]
    old_canonical = code99.get("canonical_value")
    assert old_state == "SUBSTANTIVE_RESPONSE", old_state
    code99["response_state"] = "REFUSAL"
    code99["canonical_value"] = None
    code99["transform_authority_ref"] = None
    validate_source_config(corrected)

    # Exact response-option authority row for q101 / 99.
    option_row = None
    option_hash = sha(Path(args.option_authority))
    with Path(args.option_authority).open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            qid = str(row.get("question_id") or "")
            var = str(row.get("var_name") or "")
            code = str(row.get("value_code_numeric") or "")
            if (qid.endswith("q101") or var == "q101") and code in ("99", "99.0"):
                option_row = row
                break
    if option_row is None:
        raise ValueError("exact q101 code-99 option authority row absent")
    expected = {
        "option_group": "special",
        "is_substantive": "False",
        "is_refusal": "True",
        "is_missing": "True",
        "response_kind": "special_missing",
    }
    for key, value in expected.items():
        if str(option_row.get(key)) != value:
            raise ValueError(f"unexpected option authority {key}: {option_row.get(key)}")

    field = next(row for row in tally["fields"] if row["question_id"] == "q101")
    old_states = dict(field.get("state_counts") or {})
    count_99 = next(
        int(row["count"]) for row in field.get("native_value_counts", ())
        if row.get("native_value") in (99, 99.0))
    old_valid = int(old_states.get("SUBSTANTIVE_RESPONSE", 0))
    old_explicit = sum(int(old_states.get(k, 0)) for k in (
        "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL"))
    old_missing = int(old_states.get("MISSING", 0))
    total = old_valid + old_explicit + old_missing
    corrected_valid = old_valid - count_99
    corrected_explicit = old_explicit + count_99
    corrected_observed = corrected_valid + corrected_explicit
    assert total == 7337
    assert (corrected_valid, corrected_explicit, old_missing) == (7129, 204, 4)
    assert corrected_valid + corrected_explicit + old_missing == total

    # Same code-99 mapping check over all selected metadata; no correction is
    # applied outside q101.
    selected_ids = [str(row["question_id"]) for row in tally["fields"]]
    same_defect = []
    for qid in selected_ids:
        slot = next(row for row in original["response_slots"] if row["question_id"] == qid)
        value = next(
            row for row in slot["values"]
            if row.get("raw_value") in (99, 99.0, "99", "99.0"))
        if value.get("response_state") == "SUBSTANTIVE_RESPONSE":
            same_defect.append(qid)
    if len(selected_ids) != 42:
        raise ValueError("selected tally is not the accepted 42 fields")

    # The corrected config is validated by the existing schema owner. We do
    # not rebuild the 1.3M-fact projection twice; counts are read from the
    # frozen config and retained aggregate tally.
    overlay_counts = {
        "questions": len(corrected["questions"]),
        "response_slots": len(corrected["response_slots"]),
        "coordinate_slots": len(corrected["coordinate_slots"]),
        "routing_entries": len(corrected["routing"]),
    }
    overlay = {
        "schema": "PYAT_SRC04_Q101_CODE99_OVERLAY@1.0.0",
        "source_id": "SRC04",
        "question_id": "q101",
        "native_value": 99.0,
        "from_response_state": old_state,
        "to_response_state": "REFUSAL",
        "from_canonical_value": old_canonical,
        "to_canonical_value": None,
        "authority": {
            "path": "response_option_authority",
            "sha256": option_hash,
            "option_group": option_row["option_group"],
            "is_substantive": option_row["is_substantive"],
            "is_refusal": option_row["is_refusal"],
            "is_missing": option_row["is_missing"],
            "response_kind": option_row["response_kind"],
        },
        "only_change": "q101 response value 99 state/canonical classification",
        "production_config_adopted": False,
    }

    result = {
        "schema": "PYAT_SRC04_Q101_CODE99_CORRECTION@1.0.0",
        "mode": "TEST_ONLY_SOURCEFREE_AGGREGATE_TALLY_CORRECTION",
        "source": {
            "source_id": "SRC04",
            "source_config_sha256": sha(Path(args.source_config)),
            "config_canonical_sha256": canonical_config_hash(source),
            "option_authority_sha256": option_hash,
            "tally_product_sha256": sha(Path(args.tally_product)),
            "routing_receipt_sha256": sha(Path(args.routing_receipt)),
        },
        "old_classification": {
            "question_id": "q101",
            "code_99_state": old_state,
            "valid_answer": old_valid,
            "explicit_nonresponse": old_explicit,
            "missing_or_unobserved": old_missing,
            "observed_response": old_valid + old_explicit,
            "source_record_denominator": total,
            "failure": "code 99 Decline to Answer counted as SUBSTANTIVE_RESPONSE",
            "misclassified_count": count_99,
        },
        "corrected_tally": {
            "question_id": "q101",
            "valid_answer": corrected_valid,
            "explicit_nonresponse": corrected_explicit,
            "dk": int(old_states.get("DK", 0)),
            "refusal": count_99,
            "missing_or_unobserved": old_missing,
            "observed_response": corrected_observed,
            "source_record_denominator": total,
            "identity": {
                "valid_plus_explicit_plus_missing": corrected_valid + corrected_explicit + old_missing,
                "equals_source_record_denominator": True,
            },
        },
        "delta": {
            "valid_answer": corrected_valid - old_valid,
            "explicit_nonresponse": corrected_explicit - old_explicit,
            "missing_or_unobserved": 0,
        },
        "overlay": overlay,
        "overlay_validation": {
            "schema_valid": True,
            "only_q101_code99_changed": True,
            "questions": overlay_counts["questions"],
            "response_slots": overlay_counts["response_slots"],
            "coordinate_slots": overlay_counts["coordinate_slots"],
            "routing_entries": overlay_counts["routing_entries"],
        },
        "classification_owner": {
            "authority": "exact q101 response-option authority row",
            "dedicated_state_classifier_present_in_current_owners": False,
            "fields_used": ["option_group", "is_substantive", "is_refusal", "is_missing", "response_kind"],
            "no_new_policy": True,
        },
        "same_mapping_defect_in_selected_metadata": {
            "selected_fields": len(selected_ids),
            "fields_mapped_code99_to_substantive": len(same_defect),
            "question_ids": same_defect,
            "correction_applied": ["q101"],
            "remaining_uncorrected": len(same_defect) - 1,
            "other_fields_changed": False,
            "scope": "exact selected-metadata evidence; no speculative corrections",
        },
        "historical_supersession": {
            "accepted_tally_product": "d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0",
            "superseded_at": ["q101"],
            "preserved_other_fields": True,
            "old_q101": {
                "valid_answer": old_valid,
                "explicit_nonresponse": old_explicit,
                "missing_or_unobserved": old_missing,
            },
            "corrected_q101": {
                "valid_answer": corrected_valid,
                "explicit_nonresponse": corrected_explicit,
                "missing_or_unobserved": old_missing,
            },
        },
        "routing": {
            "state": "ROUTING_UNKNOWN",
            "selected_routing_unknown": routing.get("routing_authority", {}).get("selected_routing_unknown"),
            "selected_risk_set_unresolved": routing.get("routing_authority", {}).get("selected_risk_set_unresolved"),
            "accepted_routing_binding": routing.get("routing_authority", {}).get("accepted_routing_binding"),
            "eligibility_denominator_binding": routing.get("routing_authority", {}).get("eligibility_denominator_binding"),
            "status": "ROUTING_UNKNOWN_HOLD",
            "affirmative_evidence": False,
        },
        "limits": {
            "original_source_read": False,
            "respondent_rows_read": False,
            "original_workload_issued": False,
            "production_config_adopted": False,
            "policy_fabricated": False,
            "routing_inferred_from_counts": False,
            "merge": False,
            "ci": False,
        },
        "result": "Q101_CODE99_CORRECTED_AGGREGATE_REPLAY__ROUTING_HOLD",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    overlay_path = Path(args.overlay)
    overlay_path.write_text(json.dumps(overlay, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "old": result["old_classification"],
        "corrected": result["corrected_tally"],
        "delta": result["delta"],
        "overlay_validation": result["overlay_validation"],
        "same_mapping_defect": result["same_mapping_defect_in_selected_metadata"],
        "routing": result["routing"],
        "result": result["result"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
