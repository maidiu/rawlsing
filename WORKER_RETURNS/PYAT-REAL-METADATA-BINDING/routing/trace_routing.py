"""Trace SRC04 routing/denominator metadata for the accepted 42-slot slice.

Reads only metadata and accepted aggregate receipts. It never opens the SRC04
SAV, reads respondent rows, issues a workload, or manufactures a routing rule or
policy. The executable input contract is entirely path-driven.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def route_ref(value: Mapping[str, Any] | None) -> str | None:
    if not isinstance(value, Mapping):
        return None
    return value.get("object_id")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--slice-selection", required=True)
    parser.add_argument("--release-receipt", required=True)
    parser.add_argument("--tally-product", required=True)
    parser.add_argument("--focused-recheck", required=True)
    parser.add_argument("--option-authority", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(args.package_root).resolve()))

    from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config
    from rawlsing_next.source_configuration.factory import build_governed_c11_projection
    from rawlsing_next.universal_grammar.types import OccurrenceKey

    config = load_source_config(Path(args.source_config))
    selection = read_json(Path(args.slice_selection))
    release_receipt = read_json(Path(args.release_receipt))
    tally = read_json(Path(args.tally_product))
    focused = read_json(Path(args.focused_recheck))

    # Existing C11 metadata owner; no source read.
    projection = build_governed_c11_projection(config)
    routing = {
        str(row["question_id"]): row for row in config.document["routing"]
    }
    selected_ids = [str(q) for q in release_receipt["selected_question_ids"]]
    selection_slots = {
        str(row["question_id"]): row
        for row in selection["response_slots"]
        if row.get("status") == "INCLUDED_IN_FIRST_ELIGIBLE_SLICE"
    }
    tally_fields = {str(row["question_id"]): row for row in tally["fields"]}
    if len(selected_ids) != 42 or len(selection_slots) != 42 or len(tally_fields) != 42:
        raise ValueError("accepted SRC04 slice is not the declared 42-field slice")
    if set(selected_ids) != set(selection_slots) or set(selected_ids) != set(tally_fields):
        raise ValueError("accepted slice, selection and tally question sets differ")

    option_rows: Counter[str] = Counter()
    option_total = 0
    option_selected_total = 0
    selected_set = set(selected_ids)
    with Path(args.option_authority).open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            option_total += 1
            qid = ""
            for field in ("var_name", "var_code", "question_id", "item_id"):
                value = str(row.get(field) or "")
                if value in selected_set:
                    qid = value
                    break
                if value.rsplit(":", 1)[-1] in selected_set:
                    qid = value.rsplit(":", 1)[-1]
                    break
            if qid in selected_set:
                option_rows[qid] += 1
                option_selected_total += 1

    rows = []
    route_unknown = 0
    risk_unresolved = 0
    exact_skip_rules = 0
    for qid in selected_ids:
        route = routing.get(qid)
        tally_field = tally_fields[qid]
        state_counts = dict(tally_field.get("state_counts") or {})
        substantive = int(state_counts.get("SUBSTANTIVE_RESPONSE", 0))
        nonresponse = sum(int(state_counts.get(key, 0)) for key in (
            "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL"))
        missing = int(state_counts.get("MISSING", 0))
        observed = substantive + nonresponse
        route_state = None if route is None else route.get("typed_state")
        rule_ref = None if route is None else route_ref(route.get("routing_rule_ref"))
        risk_ref = None if route is None else route_ref(route.get("risk_set_ref"))
        state_unknown = route_state != "ROUTING_KNOWN"
        rule_unresolved = (route is None or rule_ref is None
                           or str(rule_ref).endswith("unresolved"))
        risk_unresolved_here = (route is None or risk_ref is None
                                or str(risk_ref).endswith("unresolved"))
        if state_unknown:
            route_unknown += 1
        if risk_unresolved_here:
            risk_unresolved += 1
        if not (state_unknown or rule_unresolved):
            exact_skip_rules += 1
        occurrence = OccurrenceKey(item_id=qid, form_id=None, repeat_id=None)
        rows.append({
            "question_id": qid,
            "response_slot_ordinal": tally_field.get("response_slot_ordinal"),
            "routing_typed_state": route_state,
            "routing_rule_ref": rule_ref,
            "risk_set_ref": risk_ref,
            "routing_rule_exact": not (state_unknown or rule_unresolved),
            "risk_set_exact": not risk_unresolved_here,
            "form_id": None,
            "repeat_id": None,
            "occurrence_candidate": occurrence.material(),
            "accepted_slice": True,
            "response_option_authority_rows": option_rows.get(qid, 0),
            "source_record_denominator": int(tally_field["source_record_denominator"]),
            "event_presence_count": int(tally_field["event_presence_count"]),
            "state_counts": state_counts,
            "classification": {
                "valid_answer": substantive,
                "explicit_nonresponse": nonresponse,
                "observed_response": observed,
                "missing_or_unobserved": missing,
                "eligible": None,
                "routed_out": None,
                "eligible_or_routed_out_known": False,
            },
            "consumer_rule_status": "ROUTING_UNKNOWN_NO_EXACT_RULE",
            "consequence": (
                "source-record/event denominator only; eligibility and routed-out "
                "are not distinguishable; no route-conditioned denominator or policy"
            ),
        })

    focused_identity = focused.get("product_identity", {})
    tally_ref = tally.get("product_ref") or focused_identity.get("tally_ref")
    replay_ref = tally.get("replay_ref") or focused_identity.get("replay_ref")
    first = rows[0]
    result = {
        "schema": "PYAT_SRC04_ROUTING_BINDING_TRACE@1.0.0",
        "mode": "TEST_ONLY_SOURCEFREE_METADATA_ROUTING_TRACE",
        "source": {
            "source_id": config.source_id,
            "config_id": config.config_id,
            "source_sha256": config.active_source_sha256,
            "source_rows": config.active_row_count,
            "source_columns": config.document["identity"]["source_column_count"],
            "source_config_sha256": sha(Path(args.source_config)),
            "config_canonical_sha256": canonical_config_hash(config),
            "policy_fabricated": False,
        },
        "accepted_slice": {
            "release_ref": release_receipt.get("release_ref") or release_receipt.get("release", {}).get("release_ref"),
            "release_receipt_sha256": sha(Path(args.release_receipt)),
            "slice_selection_sha256": sha(Path(args.slice_selection)),
            "selected_response_slots": len(selected_ids),
            "selected_coordinate_slots": len(release_receipt.get("selected_coordinate_slots", ())),
            "selected_question_ids": selected_ids,
            "single_interview_row": True,
            "form_id": None,
            "repeat_id": None,
            "form_repeat_identifiers_fabricated": False,
            "form_repeat_scope": "accepted single-SAV/source-interview-row bounded slice",
        },
        "option_authority": {
            "rows_total": option_total,
            "rows_selected_42": option_selected_total,
            "sha256": sha(Path(args.option_authority)),
        },
        "prior_tally_consumer": {
            "tally_product_sha256": sha(Path(args.tally_product)),
            "tally_ref": tally_ref,
            "replay_ref": replay_ref,
            "consumer_api": tally.get("consumer_api"),
            "focused_recheck_sha256": sha(Path(args.focused_recheck)),
            "focused_recheck_verdict": focused.get("verdict"),
            "focused_recheck_acceptance": focused.get("acceptance", {}).get("bounded_grade"),
            "routing_state": tally.get("routing_state"),
            "population_or_eligibility_claims": tally.get("population_or_eligibility_claims"),
            "event_presence_count": tally.get("event_presence_count", focused_identity.get("event_presence_count")),
            "observed_response_denominator_total": tally.get("observed_response_denominator_total", focused_identity.get("observed_response_denominator_total")),
            "answered_substantive_denominator_total": tally.get("answered_substantive_denominator_total", focused_identity.get("answered_substantive_denominator_total")),
            "missing_or_unobserved_total": tally.get("missing_or_unobserved_total", focused_identity.get("missing_or_unobserved_total")),
        },
        "routing_authority": {
            "config_routing_entries": len(routing),
            "selected_routing_entries": len(rows),
            "selected_routing_unknown": route_unknown,
            "selected_risk_set_unresolved": risk_unresolved,
            "selected_exact_skip_rules": exact_skip_rules,
            "accepted_routing_binding": False,
            "source_record_denominator_binding": True,
            "eligibility_denominator_binding": False,
            "accepted_denominator_binding": False,
            "routing_inferred_from_observed_counts": False,
            "policy_fabricated": False,
        },
        "consumer_probe": {
            "c11_caller": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "c11_respondents": len(projection.respondents),
            "c11_questions": len(projection.questions),
            "c11_response_slots": len(projection.response_slots),
            "r03_occurrence_entrypoint": "rawlsing_next.universal_grammar.types.OccurrenceKey",
            "accepted_tally_consumer_api": tally.get("consumer_api"),
            "question_id": first["question_id"],
            "source_record_denominator": first["source_record_denominator"],
            "valid_answer": first["classification"]["valid_answer"],
            "explicit_nonresponse": first["classification"]["explicit_nonresponse"],
            "missing_or_unobserved": first["classification"]["missing_or_unobserved"],
            "eligible": None,
            "routed_out": None,
            "routing_rule_exact": first["routing_rule_exact"],
            "consequence": first["consequence"],
        },
        "first_missing": {
            "artifact": "exact questionnaire routing/skip rule and risk-set/eligibility denominator for the accepted SRC04 42-slot slice",
            "question_id": first["question_id"],
            "missing_rule_ref": first["routing_rule_ref"],
            "missing_risk_set_ref": first["risk_set_ref"],
            "current_typed_state": first["routing_typed_state"],
            "fields": [
                "routing[].typed_state",
                "routing[].routing_rule_ref",
                "routing[].risk_set_ref",
                "risk_set_refs",
            ],
            "owner": "ARAB lane / P3 integration owner named in the SRC04 exception ledger",
            "consequence": first["consequence"],
            "downstream_missing": {
                "artifact": "exact R03 GrammarPolicy/authorized direction grant",
                "owner": "R03 GrammarPolicy/direction owner",
            },
        },
        "rows": rows,
        "limits": {
            "original_source_read": False,
            "respondent_rows_read": False,
            "original_workload_issued": False,
            "production_edit": False,
            "merge": False,
            "ci": False,
            "policy_fabricated": False,
            "routing_inferred_from_observed_counts": False,
        },
        "result": "HOLD_ROUTING_AND_DENOMINATOR_NOT_ACCEPTED",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "result": result["result"],
        "accepted_slice": result["accepted_slice"]["selected_response_slots"],
        "routing": result["routing_authority"],
        "first_missing": result["first_missing"],
        "consumer_probe": result["consumer_probe"],
        "rows": len(rows),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
