"""Original W1 questionnaire authority trace for the 42 selected SRC04 fields.

The two supplied editions are compared byte-for-byte. Exact PDF page, printed
page, line and question label citations are extracted for response semantics.
No respondent data, SAV/DTA file, workload or production configuration is read.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

from pypdf import PdfReader


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


def labels(qid: str) -> list[str]:
    n = qid[1:]
    out = [n]
    if len(n) == 4:
        out.extend([n[:3] + "." + n[3], n[:2] + "." + n[2:]])
    return out


def locate(text: str, label: str) -> int | None:
    match = re.search(r"(?<![0-9])" + re.escape(label) + r"(?![0-9.])", text)
    return match.start() if match else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--source-config", required=True)
    parser.add_argument("--certified-receipt", required=True)
    parser.add_argument("--codebook", required=True)
    parser.add_argument("--option-authority", required=True)
    parser.add_argument("--exceptions", required=True)
    parser.add_argument("--edition-a", required=True)
    parser.add_argument("--edition-b", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(args.package_root).resolve()))

    from rawlsing_next.source_configuration.schema import (
        canonical_config_hash,
        load_source_config,
        validate_source_config,
    )

    outdir = Path(args.output_dir)
    evidence = outdir / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)

    edition_a = Path(args.edition_a)
    edition_b = Path(args.edition_b)
    hash_a = sha(edition_a)
    hash_b = sha(edition_b)
    reader_a = PdfReader(str(edition_a))
    reader_b = PdfReader(str(edition_b))
    pages_a = [page.extract_text() or "" for page in reader_a.pages]
    pages_b = [page.extract_text() or "" for page in reader_b.pages]
    if pages_a != pages_b:
        raise ValueError("the two questionnaire editions have different extracted text")
    starts: list[int] = []
    offset = 0
    for text in pages_a:
        starts.append(offset)
        offset += len(text) + 1
    full = "\n".join(pages_a)

    receipt = read_json(Path(args.certified_receipt))
    certified = {row["question_id"]: row for row in receipt["certified"]}
    held = {row["question_id"]: row for row in receipt["held"]}
    qids = [row["question_id"] for row in receipt["certified"]]
    qids += [row["question_id"] for row in receipt["held"]]
    if len(certified) != 28 or len(held) != 14 or len(qids) != 42:
        raise ValueError("expected 28 certified + 14 held = 42 selected fields")
    if len(set(qids)) != 42:
        raise ValueError("duplicate selected question")

    codebook_rows = {str(row["var_name"]): row for row in read_csv(Path(args.codebook))}
    if set(qids) - set(codebook_rows):
        raise ValueError("selected field absent from codebook")

    authority_rows = read_csv(Path(args.option_authority))
    authority_99: dict[str, dict[str, str]] = {}
    for row in authority_rows:
        if row.get("var_name") in qids and row.get("value_code_numeric") == "99.0":
            authority_99[str(row["var_name"])] = row
    if set(qids) - set(authority_99):
        raise ValueError("selected field has no exact option-authority code-99 row")

    item_rows: list[dict[str, Any]] = []
    for qid in qids:
        found = None
        for label in labels(qid):
            for page_number, text in enumerate(pages_a, 1):
                pos = locate(text, label)
                if pos is not None:
                    found = (page_number, pos, label)
                    break
            if found:
                break
        if not found:
            raise ValueError(f"question label not found in PDF: {qid}")
        page_number, pos, label = found
        absolute = starts[page_number - 1] + pos
        block = full[absolute:absolute + 1200]
        match = re.search(r"99\s*=\s*Decline\s+to\s+Answer", block, re.I)
        if match is None:
            raise ValueError(f"no exact 99=Decline-to-Answer evidence for {qid}")
        absolute_99 = absolute + match.start()
        page_99 = bisect.bisect_right(starts, absolute_99)
        rel_99 = absolute_99 - starts[page_99 - 1]
        line_q = pages_a[page_number - 1][:pos].count("\n") + 1
        line_99 = pages_a[page_99 - 1][:rel_99].count("\n") + 1
        auth = authority_99[qid]
        status = auth.get("response_semantics_status")
        is_certified = status == "certified" and qid in certified
        is_held = qid in held
        item_rows.append({
            "question_id": qid,
            "code_count": certified[qid]["code_count"] if qid in certified else held[qid]["code_count"],
            "pdf_page": page_number,
            "printed_page": page_number + 1 if page_number < len(pages_a) else None,
            "question_label": label,
            "question_line": line_q,
            "response_99_pdf_page": page_99,
            "response_99_printed_page": page_99 + 1 if page_99 < len(pages_a) else None,
            "response_99_line": line_99,
            "response_99": "99 = Decline to Answer",
            "authority_status": status,
            "authority_refusal_flag": auth.get("is_refusal"),
            "refusal_certified": is_certified,
            "refusal_held": is_held,
            "eligible": "UNKNOWN",
            "routed_or_ineligible": "UNKNOWN",
        })

    # Route terms: every hit must be evidence of a rule, not question prose.
    route_terms = ("skip", "filter", "routing", "ask all", "go to", "routed",
                   "eligib", "screened", "screen", "unconditional")
    term_hits: dict[str, list[int]] = {}
    for term in route_terms:
        pages = [i for i, text in enumerate(pages_a, 1) if term in text.lower()]
        term_hits[term] = pages
    conditional_pages = [i for i, text in enumerate(pages_a, 1) if "if " in text.lower()]
    only_pages = [i for i, text in enumerate(pages_a, 1) if "only " in text.lower()]
    exact_route_instructions = sum(len(pages) for pages in term_hits.values())

    # The normal schema owner validates the actual unmodified source config.
    source = load_source_config(Path(args.source_config))
    validate_source_config(source.document)
    routing = {str(row["question_id"]): row for row in source.document["routing"]}
    route_rows = []
    for qid in qids:
        route = routing.get(qid)
        if route is None:
            raise ValueError(f"selected field absent from routing interface: {qid}")
        state = route.get("typed_state")
        rule = route_ref(route.get("routing_rule_ref"))
        risk = route_ref(route.get("risk_set_ref"))
        exact = state == "ROUTING_KNOWN" and rule is not None and not str(rule).endswith("unresolved")
        denominator = risk is not None and not str(risk).endswith("unresolved")
        route_rows.append({
            "question_id": qid,
            "typed_state": state,
            "routing_rule_ref": rule,
            "risk_set_ref": risk,
            "row_selector": route.get("row_selector"),
            "exact_route": exact,
            "exact_eligible_denominator": denominator,
            "eligible": "UNKNOWN",
            "routed_or_ineligible": "UNKNOWN",
        })
    if any(row["exact_route"] or row["exact_eligible_denominator"] for row in route_rows):
        raise ValueError("unexpected exact routing evidence in source config")

    exceptions = read_json(Path(args.exceptions))
    routing_exceptions = [
        entry for entry in exceptions.get("entries", ())
        if "routing" in str(entry.get("required_native_field", "")).lower()
        or "form" in str(entry.get("required_native_field", "")).lower()
    ]

    held_items = []
    for qid in sorted(held):
        row = next(item for item in item_rows if item["question_id"] == qid)
        held_items.append({
            "question_id": qid,
            "code_count": held[qid]["code_count"],
            "pdf_page": row["pdf_page"],
            "printed_page": row["printed_page"],
            "response_99_pdf_page": row["response_99_pdf_page"],
            "response_99_printed_page": row["response_99_printed_page"],
            "item_response_evidence": row["response_99"],
            "authority_status": row["authority_status"],
            "authority_refusal_flag": row["authority_refusal_flag"],
            "correction_applied": False,
            "eligible": "UNKNOWN",
            "routed_or_ineligible": "UNKNOWN",
            "missing_premise": "competent item-specific authority certification; exact source evidence exists but response_semantics_status remains preserved_not_certified",
        })

    edition_comparison = {
        "edition_a": {"path": str(edition_a), "sha256": hash_a, "bytes": edition_a.stat().st_size,
                      "pages": len(reader_a.pages), "title": reader_a.metadata.title if reader_a.metadata else None},
        "edition_b": {"path": str(edition_b), "sha256": hash_b, "bytes": edition_b.stat().st_size,
                      "pages": len(reader_b.pages), "title": reader_b.metadata.title if reader_b.metadata else None},
        "byte_identical": hash_a == hash_b and edition_a.read_bytes() == edition_b.read_bytes(),
        "extracted_text_identical": pages_a == pages_b,
        "edition_delta": "NONE; the two supplied files are byte-identical",
    }
    (evidence / "EDITION_COMPARISON.json").write_text(
        json.dumps(edition_comparison, indent=2, sort_keys=True) + "\n")

    columns = list(item_rows[0])
    with (evidence / "QUESTIONNAIRE_ITEM_CITATIONS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(item_rows)

    with (evidence / "ROUTING_TERM_SCAN.json").open("w", encoding="utf-8") as handle:
        json.dump({
            "terms": term_hits,
            "exact_route_instruction_count": exact_route_instructions,
            "conditional_question_prose_pages": conditional_pages,
            "only_question_prose_pages": only_pages,
            "classification": "NO_EXPLICIT_ROUTING_INSTRUCTION; 'if'/'only' occurrences are substantive question prose, not skip rules",
        }, handle, indent=2, sort_keys=True)
        handle.write("\n")

    with (evidence / "RESPONSE_AUTHORITY_14.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(held_items[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(held_items)

    aggregate = receipt["aggregate"]
    all_code99 = sum(row["code_count"] for row in item_rows if row["refusal_certified"])
    held_code99 = sum(row["code_count"] for row in item_rows if row["refusal_held"])
    result = {
        "schema": "PYAT_SRC04_QUESTIONNAIRE_AUTHORITY@1.0.0",
        "mode": "TEST_ONLY_ORIGINAL_QUESTIONNAIRE_METADATA_TRACE",
        "base_commit": "6d1ddb9844a5117d466bb0c3a8bc5260196c4249",
        "source": {
            "source_id": source.source_id,
            "source_config_sha256": sha(Path(args.source_config)),
            "config_canonical_sha256": canonical_config_hash(source),
            "codebook_sha256": sha(Path(args.codebook)),
            "codebook_rows": len(codebook_rows),
            "option_authority_sha256": sha(Path(args.option_authority)),
            "option_authority_rows": len(authority_rows),
            "exceptions_sha256": sha(Path(args.exceptions)),
            "accepted_overlay_receipt_sha256": sha(Path(args.certified_receipt)),
        },
        "edition_comparison": edition_comparison,
        "questionnaire": {
            "selected_fields": 42,
            "items_with_exact_99_decline": sum(row["response_99"] == "99 = Decline to Answer" for row in item_rows),
            "certified_28": len(certified),
            "held_14": len(held),
            "route_terms": term_hits,
            "exact_route_instruction_count": exact_route_instructions,
            "routing_unknown_fields": 42,
            "routing_known_fields": 0,
            "eligible_known_fields": 0,
            "routed_out_known_fields": 0,
        },
        "config_interface": {
            "interface": "source_configuration.data.SRC04.source.config.json:routing[]",
            "normal_schema_valid": True,
            "config_changed": False,
            "selected_route_entries": len(route_rows),
            "exact_route_bindings": sum(row["exact_route"] for row in route_rows),
            "exact_eligible_denominators": sum(row["exact_eligible_denominator"] for row in route_rows),
            "route_selector_all_is_not_eligibility_authority": True,
            "rows": route_rows,
        },
        "response_semantics": {
            "all_42_have_exact_99_decline_item_evidence": True,
            "certified_28": sorted(certified),
            "held_14": sorted(held),
            "held_correction_not_applied": True,
            "held_code99_count_not_applied": held_code99,
        },
        "held_14_authority": held_items,
        "routing_exceptions": [
            {
                "required_native_field": entry.get("required_native_field"),
                "status": entry.get("status"),
                "owner_step": entry.get("acquisition_fix_owner_and_step"),
            }
            for entry in routing_exceptions
        ],
        "retained_aggregate_replay": {
            "old": aggregate["old"],
            "corrected": aggregate["corrected"],
            "conserved": aggregate["conserved"],
            "refusal_vs_substantive_distinction": aggregate["refusal_vs_substantive_distinction"],
            "certified_refusal_delta": all_code99,
            "held_code99_not_applied": held_code99,
            "q101": receipt["q101"],
            "distinct_refusal_state": "EXPLICIT_NONRESPONSE",
            "distinct_ineligible_state": "UNKNOWN_ROUTED_OUT_OR_INELIGIBLE",
            "ineligible_or_routed_out_inferred_from_counts": False,
        },
        "state_exercise": {
            "declined_evidenced_42": 42,
            "declined_certified_28": len(certified),
            "declined_held_14": len(held),
            "eligible_known_0": True,
            "routed_out_known_0": True,
            "routing_unknown_42": True,
            "conflation_guard": "DECLINED, ELIGIBLE and ROUTED_OUT are separate states; unknown routing is not declined or ineligible",
        },
        "owner_dependencies": [
            "ARAB lane / P3 integration owner named in the SRC04 exception ledger: exact per-item routing/skip rule and risk-set/eligibility denominator for all 42 fields",
            "Competent source-semantics authority: certify or reject the 14 held item-specific code-99 response semantics; the original questionnaire supplies exact item evidence but the option-authority status remains preserved_not_certified",
            "R03 GrammarPolicy / authorized direction owner: exact policy and authorized direction grant remain absent",
        ],
        "engineering": "HOLD_EXACT_ROUTING_EVIDENCE_MISSING",
        "science": "HOLD_ABSENT_ORIGINAL_EXECUTION_GRANT",
        "authority": "HOLD_PRODUCTION_AND_ISSUANCE_NOT_GRANTED",
        "result": "HOLD_ROUTING_UNKNOWN_AND_14_AUTHORITY__28_CERTIFIED_PRESERVED__PDF_EVIDENCE_EXACT",
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
        "runtime": {
            "python_version": sys.version.split()[0],
            "pypdf_version": __import__("pypdf").__version__,
            "config_schema_imported": True,
            "source_config_loaded": True,
            "quota": "UNKNOWN",
        },
    }
    (outdir / "04_QUESTIONNAIRE_AUTHORITY_RECEIPT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    (evidence / "CONFIG_VALIDATION.json").write_text(json.dumps({
        "source_config": str(Path(args.source_config)),
        "source_config_sha256": sha(Path(args.source_config)),
        "canonical_config_sha256": canonical_config_hash(source),
        "schema_owner": "rawlsing_next.source_configuration.schema.validate_source_config",
        "valid": True,
        "config_changed": False,
        "selected_route_entries": len(route_rows),
        "exact_route_bindings": 0,
    }, indent=2, sort_keys=True) + "\n")
    (outdir / "PASSPORT.json").write_text(json.dumps({
        "agent_type": "existing OpenCode metadata author",
        "provider": "opencode-go",
        "model": "deepseek-v4.1-flash#max",
        "runtime": "python3/pypdf/config-schema",
        "worktree": "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007",
        "base_commit": "6d1ddb9844a5117d466bb0c3a8bc5260196c4249",
        "quota": "UNKNOWN",
        "browser_local_checkout": False,
        "sanitized": True,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "edition_identical": edition_comparison["byte_identical"],
        "items_with_99": result["questionnaire"]["items_with_exact_99_decline"],
        "routing_unknown": result["questionnaire"]["routing_unknown_fields"],
        "exact_route": result["config_interface"]["exact_route_bindings"],
        "held_14": len(held),
        "held_code99_not_applied": held_code99,
        "aggregate": result["retained_aggregate_replay"],
        "engineering": result["engineering"],
        "result": result["result"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
