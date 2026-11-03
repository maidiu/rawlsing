"""Extend the isolated SRC04 code-99 overlay to the 28 certified entries.

The input allowlists are per-item authority joins, not a universal code rule.
The script validates the corrected source configuration with the normal schema
owner and replays retained aggregate counts; it never opens the SRC04 SAV.
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def same_number(left: Any, right: str) -> bool:
    try:
        return float(left) == float(right)
    except (TypeError, ValueError):
        return False


def find_slot(doc: Mapping[str, Any], qid: str) -> Mapping[str, Any]:
    return next(slot for slot in doc["response_slots"] if slot["question_id"] == qid)


def find_value(slot: Mapping[str, Any], code: str) -> Mapping[str, Any]:
    return next(value for value in slot["values"] if same_number(value.get("raw_value"), code))


def native_code_count(field: Mapping[str, Any], code: str) -> int:
    return next(
        int(row["count"]) for row in field.get("native_value_counts", ())
        if same_number(row.get("native_value"), code))


def state_totals(field: Mapping[str, Any], code: str) -> dict[str, int]:
    states = dict(field.get("state_counts") or {})
    code_count = native_code_count(field, code)
    valid = int(states.get("SUBSTANTIVE_RESPONSE", 0))
    explicit = sum(int(states.get(key, 0)) for key in (
        "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL"))
    missing = int(states.get("MISSING", 0))
    total = int(field["source_record_denominator"])
    return {
        "valid_answer": valid,
        "explicit_nonresponse": explicit,
        "refusal": code_count,
        "missing_or_unobserved": missing,
        "source_record_denominator": total,
        "observed_response": valid + explicit,
        "corrected_valid": valid - code_count,
        "corrected_explicit": explicit + code_count,
        "corrected_observed": valid - code_count + explicit + code_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--allowlist", required=True)
    parser.add_argument("--typed-unknown", required=True)
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
    allow = read_csv(Path(args.allowlist))
    held = read_csv(Path(args.typed_unknown))
    tally = read_json(Path(args.tally_product))
    routing = read_json(Path(args.routing_receipt))
    tally_fields = {row["question_id"]: row for row in tally["fields"]}
    selected_ids = list(tally_fields)
    if len(selected_ids) != 42 or len(allow) != 28 or len(held) != 14:
        raise ValueError("expected 42 selected fields, 28 certified and 14 held")
    if set(selected_ids) != {row["question_id"] for row in allow + held}:
        raise ValueError("allowlists do not partition the selected fields")

    option_rows = read_csv(Path(args.option_authority))
    option_by_key = {}
    for row in option_rows:
        key = (row.get("question_id", ""), row.get("var_name", ""), row.get("value_code_numeric", ""))
        option_by_key[key] = row
        option_by_key[(row.get("question_id", ""), row.get("var_name", ""), str(float(row["value_code_numeric"])))] = row

    overlay_entries = []
    certified_stats = []
    for row in allow:
        qid = row["question_id"]
        qcode = row["authority_code_numeric"]
        if row["correction_status"] != "certified_correction_allowlist":
            raise ValueError(f"uncertified row in allowlist: {qid}")
        slot = find_slot(corrected, qid)
        value = find_value(slot, qcode)
        if value["response_state"] != row["source_config_response_state"]:
            raise ValueError(f"source state changed for {qid}")
        if str(value.get("canonical_value")) != row["source_config_canonical_value"]:
            raise ValueError(f"source canonical changed for {qid}")
        auth_key = (row["authority_question_id"], qid, qcode)
        authority = option_by_key.get(auth_key) or option_by_key.get(
            (row["authority_question_id"], qid, str(float(qcode))))
        if authority is None:
            raise ValueError(f"exact option authority missing for {qid}")
        for left, right in (
            ("option_group", "authority_option_group"),
            ("is_substantive", "authority_is_substantive"),
            ("is_refusal", "authority_is_refusal"),
            ("is_missing", "authority_is_missing"),
            ("response_kind", "authority_response_kind"),
        ):
            if authority[left] != row[right]:
                raise ValueError(f"authority flag mismatch for {qid}:{left}")
        value["response_state"] = "REFUSAL"
        value["canonical_value"] = None
        value["transform_authority_ref"] = None
        field = tally_fields[qid]
        stat = state_totals(field, qcode)
        if stat["source_record_denominator"] != 7337:
            raise ValueError(f"non-7337 denominator for {qid}")
        if stat["refusal"] != int(row["retained_code99_count"]):
            raise ValueError(f"retained code count mismatch for {qid}")
        overlay_entries.append({
            "question_id": qid,
            "authority_question_id": row["authority_question_id"],
            "native_value": float(qcode),
            "from_response_state": row["source_config_response_state"],
            "to_response_state": "REFUSAL",
            "from_canonical_value": row["source_config_canonical_value"],
            "to_canonical_value": None,
            "authority": {
                "option_group": authority["option_group"],
                "is_substantive": authority["is_substantive"],
                "is_refusal": authority["is_refusal"],
                "is_missing": authority["is_missing"],
                "response_kind": authority["response_kind"],
                "response_semantics_status": authority["response_semantics_status"],
            },
        })
        certified_stats.append({
            "question_id": qid,
            "native_code": qcode,
            "old_valid": stat["valid_answer"],
            "old_explicit": stat["explicit_nonresponse"],
            "code_count": stat["refusal"],
            "corrected_valid": stat["corrected_valid"],
            "corrected_explicit": stat["corrected_explicit"],
            "missing": stat["missing_or_unobserved"],
            "observed": stat["corrected_observed"],
            "total": stat["source_record_denominator"],
        })

    # The 14 held entries are not modified; record exact counts and reason.
    held_stats = []
    for row in held:
        qid = row["question_id"]
        qcode = row["authority_code_numeric"]
        field = tally_fields[qid]
        stat = state_totals(field, qcode)
        if stat["refusal"] != int(row["retained_code99_count"]):
            raise ValueError(f"held code count mismatch for {qid}")
        value = find_value(find_slot(corrected, qid), qcode)
        held_stats.append({
            "question_id": qid,
            "native_code": qcode,
            "code_count": stat["refusal"],
            "current_state": value["response_state"],
            "status": "HELD_UNCERTIFIED",
            "reason": row["typed_unknown_reason"],
        })

    validate_source_config(corrected)
    overlay = {
        "schema": "PYAT_SRC04_CERTIFIED_REFUSAL_OVERLAY@1.0.0",
        "source_id": "SRC04",
        "overlay_scope": "accepted 42 selected fields; 28 certified entries only",
        "entries": overlay_entries,
        "held_uncertified": [
            {"question_id": row["question_id"], "native_code": row["native_code"],
             "status": row["status"]} for row in held_stats
        ],
        "production_config_adopted": False,
        "authority_join": "per-item allowlist + exact option authority row",
        "universal_code_rule": False,
    }

    def totals(rows: list[Mapping[str, Any]], corrected_side: bool) -> dict[str, int]:
        valid_key = "corrected_valid" if corrected_side else "old_valid"
        explicit_key = "corrected_explicit" if corrected_side else "old_explicit"
        return {
            "valid_answer": sum(int(r[valid_key]) for r in rows),
            "explicit_nonresponse": sum(int(r[explicit_key]) for r in rows),
            "missing_or_unobserved": sum(int(r["missing"]) for r in rows),
            "observed_response": sum(int(r["observed"]) for r in rows),
            "source_record_denominator": sum(int(r["total"]) for r in rows),
        }

    old_totals = totals(certified_stats, False)
    held_valid = sum(int(state_totals(tally_fields[r["question_id"]], r["native_code"])["valid_answer"]) for r in held_stats)
    held_explicit = sum(int(state_totals(tally_fields[r["question_id"]], r["native_code"])["explicit_nonresponse"]) for r in held_stats)
    held_missing = sum(int(state_totals(tally_fields[r["question_id"]], r["native_code"])["missing_or_unobserved"]) for r in held_stats)
    overall_old = {
        "valid_answer": old_totals["valid_answer"] + held_valid,
        "explicit_nonresponse": old_totals["explicit_nonresponse"] + held_explicit,
        "missing_or_unobserved": old_totals["missing_or_unobserved"] + held_missing,
        "observed_response": old_totals["observed_response"] + held_valid + held_explicit,
        "source_record_denominator": old_totals["source_record_denominator"] + sum(
            int(state_totals(tally_fields[r["question_id"]], r["native_code"])["source_record_denominator"])
            for r in held_stats),
    }
    corrected_totals = totals(certified_stats, True)
    overall_corrected = {
        "valid_answer": corrected_totals["valid_answer"] + held_valid,
        "explicit_nonresponse": corrected_totals["explicit_nonresponse"] + held_explicit,
        "refusal": sum(int(r["code_count"]) for r in certified_stats),
        "missing_or_unobserved": corrected_totals["missing_or_unobserved"] + held_missing,
        "observed_response": corrected_totals["observed_response"] + held_valid + held_explicit,
        "source_record_denominator": corrected_totals["source_record_denominator"] + sum(
            int(state_totals(tally_fields[r["question_id"]], r["native_code"])["source_record_denominator"])
            for r in held_stats),
    }
    if overall_corrected["valid_answer"] + overall_corrected["explicit_nonresponse"] + overall_corrected["missing_or_unobserved"] != overall_corrected["source_record_denominator"]:
        raise ValueError("overall corrected totals do not conserve")
    if overall_corrected["source_record_denominator"] != 42 * 7337:
        raise ValueError("overall source-record denominator mismatch")

    result = {
        "schema": "PYAT_SRC04_CERTIFIED_REFUSAL_RECEIPT@1.0.0",
        "mode": "TEST_ONLY_SOURCEFREE_CERTIFIED_AGGREGATE_REPLAY",
        "source": {
            "source_id": source.source_id,
            "source_config_sha256": sha(Path(args.source_config)),
            "config_canonical_sha256": canonical_config_hash(source),
            "allowlist_sha256": sha(Path(args.allowlist)),
            "typed_unknown_sha256": sha(Path(args.typed_unknown)),
            "option_authority_sha256": sha(Path(args.option_authority)),
            "tally_product_sha256": sha(Path(args.tally_product)),
            "routing_receipt_sha256": sha(Path(args.routing_receipt)),
        },
        "overlay": overlay,
        "validation": {
            "schema_valid": True,
            "certified_entries": len(overlay_entries),
            "held_entries": len(held_stats),
            "selected_fields": len(selected_ids),
            "only_certified_entries_changed": True,
            "held_entries_changed": False,
        },
        "certified": certified_stats,
        "held": held_stats,
        "aggregate": {
            "old": overall_old,
            "corrected": overall_corrected,
            "delta": {
                "valid_answer": overall_corrected["valid_answer"] - overall_old["valid_answer"],
                "explicit_nonresponse": overall_corrected["explicit_nonresponse"] - overall_old["explicit_nonresponse"],
                "missing_or_unobserved": 0,
            },
            "conserved": (
                overall_corrected["valid_answer"]
                + overall_corrected["explicit_nonresponse"]
                + overall_corrected["missing_or_unobserved"]
                == overall_corrected["source_record_denominator"]
            ),
            "refusal_vs_substantive_distinction": True,
        },
        "q101": next(row for row in certified_stats if row["question_id"] == "q101"),
        "routing": {
            "state": "ROUTING_UNKNOWN",
            "selected_routing_unknown": routing["routing_authority"]["selected_routing_unknown"],
            "selected_risk_set_unresolved": routing["routing_authority"]["selected_risk_set_unresolved"],
            "accepted_routing_binding": routing["routing_authority"]["accepted_routing_binding"],
            "eligibility_denominator_binding": routing["routing_authority"]["eligibility_denominator_binding"],
            "preserved": True,
        },
        "historical": {
            "accepted_tally_product": "d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0",
            "q101_prior_correction": "preserved",
            "superseded_scope": "28 certified entries in the isolated overlay; 14 held entries unchanged",
        },
        "limits": {
            "original_source_read": False,
            "respondent_rows_read": False,
            "original_workload_issued": False,
            "production_config_adopted": False,
            "routing_inferred_from_counts": False,
            "policy_fabricated": False,
            "merge": False,
            "ci": False,
        },
        "result": "CERTIFIED_REFUSAL_OVERLAY_VALIDATED__28_CORRECTED__14_HELD__ROUTING_UNKNOWN",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    Path(args.overlay).write_text(json.dumps(overlay, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "overlay": result["validation"],
        "aggregate": result["aggregate"],
        "q101": result["q101"],
        "held": result["held"],
        "routing": result["routing"],
        "result": result["result"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
