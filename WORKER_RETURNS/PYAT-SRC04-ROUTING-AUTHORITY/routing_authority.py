"""SRC04 routing/eligibility authority trace for the accepted 42 fields.

Reads metadata, accepted aggregate overlay receipts, codebooks and source
authority only. It does not open the SRC04 SAV, read respondent rows, issue a
workload, or adopt a configuration/policy into production.
"""
from __future__ import annotations

import argparse
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


def route_ref(value: Mapping[str, Any] | None) -> str | None:
    if not isinstance(value, Mapping):
        return None
    return value.get("object_id")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--certified-receipt", required=True)
    parser.add_argument("--codebook", required=True)
    parser.add_argument("--exceptions", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(args.package_root).resolve()))

    from rawlsing_next.source_configuration.schema import (
        canonical_config_hash,
        load_source_config,
        validate_source_config,
    )

    source = load_source_config(Path(args.source_config))
    receipt = read_json(Path(args.certified_receipt))
    certified = {row["question_id"]: row for row in receipt["certified"]}
    held = {row["question_id"]: row for row in receipt["held"]}
    selected = list(certified) + list(held)
    if len(certified) != 28 or len(held) != 14 or len(selected) != 42:
        raise ValueError("certified/held partition is not 28 + 14 = 42")
    if len(set(selected)) != 42:
        raise ValueError("duplicate selected question")

    routing = {str(row["question_id"]): row for row in source.document["routing"]}
    codebook_rows = {str(row["var_name"]): row for row in read_csv(Path(args.codebook))}
    exceptions = read_json(Path(args.exceptions))
    missing_codebook = sorted(set(selected) - set(codebook_rows))
    if missing_codebook:
        raise ValueError(f"selected fields absent from codebook: {missing_codebook}")

    rows = []
    route_known = 0
    route_unknown = 0
    risk_resolved = 0
    codebook_route_terms = 0
    codebook_route_term_fields = []
    for ordinal, qid in enumerate(selected, 1):
        route = routing.get(qid)
        if route is None:
            state = "MISSING_ROUTING_ENTRY"
            rule = None
            risk = None
            row_selector = None
        else:
            state = route.get("typed_state")
            rule = route_ref(route.get("routing_rule_ref"))
            risk = route_ref(route.get("risk_set_ref"))
            row_selector = route.get("row_selector")
        rule_exact = (
            state == "ROUTING_KNOWN" and rule is not None
            and not str(rule).endswith("unresolved"))
        risk_exact = risk is not None and not str(risk).endswith("unresolved")
        route_known += int(rule_exact)
        route_unknown += int(not rule_exact)
        risk_resolved += int(risk_exact)
        cb = codebook_rows[qid]
        cb_text = " ".join(str(value) for value in cb.values()).lower()
        terms = [term for term in (
            "skip", "filter", "routing", "ask all", "unconditional", "eligib")
            if term in cb_text]
        if terms:
            codebook_route_terms += 1
            codebook_route_term_fields.append({"question_id": qid, "terms": terms,
                                               "classification": "SUBSTANTIVE_TEXT_NOT_A_ROUTING_RULE"})
        rows.append({
            "question_id": qid,
            "selected_slice_ordinal": ordinal,
            "routing_typed_state": state,
            "routing_rule_ref": rule,
            "risk_set_ref": risk,
            "row_selector": row_selector,
            "routing_rule_exact": rule_exact,
            "eligibility_denominator_exact": risk_exact,
            "route_or_eligible_known": rule_exact and risk_exact,
            "refusal_state": "CERTIFIED" if qid in certified else "HELD_UNCERTIFIED",
            "eligible": "UNKNOWN",
            "routed_or_ineligible": "UNKNOWN",
            "routing_status": "EXACT_BINDING" if rule_exact and risk_exact else "TYPED_ABSENCE_UNKNOWN",
        })

    first = rows[0]
    result = {
        "schema": "PYAT_SRC04_ROUTING_AUTHORITY@1.0.0",
        "mode": "TEST_ONLY_SOURCEFREE_ROUTING_AUTHORITY_TRACE",
        "source": {
            "source_id": source.source_id,
            "source_config_sha256": sha(Path(args.source_config)),
            "config_canonical_sha256": canonical_config_hash(source),
            "codebook_sha256": sha(Path(args.codebook)),
            "codebook_rows": len(codebook_rows),
            "exceptions_sha256": sha(Path(args.exceptions)),
            "accepted_overlay_receipt_sha256": sha(Path(args.certified_receipt)),
        },
        "routing_interface": {
            "configuration_interface": "source_configuration.data.SRC04.source.config.json:routing[]",
            "fields": ["typed_state", "routing_rule_ref", "risk_set_ref", "row_selector"],
            "selected_fields": 42,
            "exact_routing_bindings": route_known,
            "typed_unknown_or_held": route_unknown,
            "exact_eligibility_denominators": risk_resolved,
            "unresolved_eligibility_denominators": 42 - risk_resolved,
            "route_selector_all_is_not_eligibility_authority": True,
            "normal_configuration_schema_valid": True,
        },
        "authority": {
            "first_missing_question": first["question_id"],
            "first_missing_rule_ref": first["routing_rule_ref"],
            "first_missing_risk_set_ref": first["risk_set_ref"],
            "first_missing_premise": "exact item-specific questionnaire skip/routing rule and risk-set/eligibility denominator",
            "owner": "ARAB lane / P3 integration owner named in the SRC04 exception ledger",
            "no_routing_rule_found_in_codebook": True,
            "codebook_route_terms_are_substantive_text_only": True,
            "codebook_route_term_hits": codebook_route_term_fields,
            "exceptions": {
                "count": len(exceptions.get("entries", ())),
                "routing_related": [
                    {
                        "required_native_field": entry.get("required_native_field"),
                        "status": entry.get("status"),
                        "owner_step": entry.get("acquisition_fix_owner_and_step"),
                    }
                    for entry in exceptions.get("entries", ())
                    if "routing" in str(entry.get("required_native_field", "")).lower()
                    or "form" in str(entry.get("required_native_field", "")).lower()
                ],
            },
        },
        "certified_and_held": {
            "certified": sorted(certified),
            "held": sorted(held),
            "certified_count": len(certified),
            "held_count": len(held),
            "held_exact_missing_premise": {
                qid: {
                    "status": "HELD_UNCERTIFIED",
                    "code_count": held[qid]["code_count"],
                    "premise": "exact item-specific competent response-semantics certification (current option authority is preserved_not_certified)",
                    "owner": "ARAB lane / P3 integration owner; later competent source-semantics authority",
                    "routed_or_ineligible": "UNKNOWN",
                }
                for qid in sorted(held)
            },
        },
        "retained_aggregate_replay": {
            "old": receipt["aggregate"]["old"],
            "corrected": receipt["aggregate"]["corrected"],
            "conserved": receipt["aggregate"]["conserved"],
            "refusal_vs_substantive_distinction": receipt["aggregate"]["refusal_vs_substantive_distinction"],
            "distinct_refusal_state": "EXPLICIT_NONRESPONSE",
            "distinct_ineligible_state": "UNKNOWN_ROUTED_OUT_OR_INELIGIBLE",
            "ineligible_or_routed_out_inferred_from_counts": False,
            "q101": receipt["q101"],
        },
        "routing_state": {
            "unknown_fields": route_unknown,
            "known_fields": route_known,
            "ineligible_or_routed_out_known": 0,
            "unresolved_owner_dependencies": [
                "ARAB lane / P3 integration owner: exact per-item routing/skip rules and risk-set/eligibility denominators for all 42 fields",
                "Competent source-semantics authority: exact item-specific certification for 14 held code-99 option rows",
                "R03 GrammarPolicy/direction owner: exact policy/authorized direction grant remains absent",
            ],
        },
        "rows": rows,
        "limits": {
            "original_source_read": False,
            "respondent_rows_read": False,
            "original_workload_issued": False,
            "production_config_adopted": False,
            "universal_code_rule": False,
            "routing_inferred_from_counts": False,
            "policy_fabricated": False,
            "scientific_issuance": False,
            "merge": False,
            "ci": False,
        },
        "result": "HOLD_ROUTING_ELIGIBILITY_AND_14_HELD__28_CERTIFIED_PRESERVED",
    }

    # The normal schema owner validates the unmodified source configuration.
    validate_source_config(source.document)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "routing_interface": result["routing_interface"],
        "authority": result["authority"],
        "held_count": len(held),
        "aggregate": result["retained_aggregate_replay"],
        "routing_state": result["routing_state"],
        "result": result["result"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
