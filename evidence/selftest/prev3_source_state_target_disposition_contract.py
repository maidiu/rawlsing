#!/usr/bin/env python3
"""Hostile source-agnostic checks for the J02 disposition contract."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
HELPER = ROOT / "tools" / "prev3_source_state_target_disposition.py"
FIXTURE = ROOT / "evidence" / "fixtures" / "prev3_source_state_target_disposition_fixture.json"

spec = importlib.util.spec_from_file_location("prev3_source_state_contract", HELPER)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
checks = []


def check(check_id, condition, detail):
    if not condition:
        raise AssertionError(f"{check_id}: {detail}")
    checks.append({"check_id": check_id, "status": "PASS", "detail": detail})


def must_fail(check_id, fn, detail):
    try:
        fn()
    except module.ContractError:
        checks.append({"check_id": check_id, "status": "PASS", "detail": detail})
        return
    raise AssertionError(f"{check_id}: expected ContractError")


auth = fixture["authorities"]
refs = fixture["refs"]
row_by_id = {row[0]: row for row in fixture["records"]}


def exact_ref(ch, kind, object_id):
    return {"kind": kind, "object_id": object_id, "content_hash": ch * 64}


def materialize_record(row):
    rid, source_id, native, source_key, semantic, state_class, eligibility, disposition, resolution_basis, basis_ch = row
    return {
        "record_id": rid,
        "raw_source_state": {"source_id": source_id, "native_state": native},
        "source_local_governed_state": {"semantic_state": semantic, "state_class": state_class, "authority_ref": deepcopy(auth[source_key])},
        "prequery_eligibility": {"decision": eligibility, "phase": "PRE_QUERY", "authority_ref": deepcopy(auth["risk"]), "risk_set_ref": deepcopy(refs["risk_set"]), "basis_ref": exact_ref(basis_ch, "SyntheticRoutingBasis", "BASIS_" + rid)},
        "product_target_disposition": {"disposition": disposition, "resolution_basis": resolution_basis, "authority_ref": deepcopy(auth["target"]), "target_domain_ref": deepcopy(refs["target_domain"])},
    }


def make_case(case_name):
    ids = fixture["case_record_ids"][case_name]
    return {
        "query_envelope": {
            "query_id": "SYNTHETIC_QUERY_ALPHA",
            "target_id": "SYNTHETIC_OBJECTIVE_TARGET_ALPHA",
            "world_scope": "OBJECTIVE",
            "authority_phase": "FROZEN_PRE_OUTCOME",
            "expected_record_ids": list(ids),
            "source_semantic_authority_refs": [deepcopy(auth["source_alpha"]), deepcopy(auth["source_beta"])],
            "target_authority_ref": deepcopy(auth["target"]),
            "risk_set_authority_ref": deepcopy(auth["risk"]),
            "replay_authority_ref": deepcopy(auth["replay"]),
            "target_domain_ref": deepcopy(refs["target_domain"]),
            "risk_set_ref": deepcopy(refs["risk_set"]),
        },
        "records": [materialize_record(row_by_id[rid]) for rid in ids],
    }


resolved = make_case("resolved_case")
result = module.emit_empirical_result(resolved)
check("resolved_target_and_complement_accounting", result["numerator"] == 1 and result["denominator"] == 2 and len(result["ledger"]["authorized_prequery_exclusion_ids"]) == 1 and result["ledger"]["raw_resolved_target_support"] == result["denominator"], "target members and authority-resolved non-target members exhaust the denominator; pre-query exclusion stays outside it")
a, b = result["audited_records"][:2]
check("same_native_code_has_no_universal_semantics", a["audit_trail"][0]["value"]["native_state"] == b["audit_trail"][0]["value"]["native_state"] == 7 and a["audit_trail"][1]["value"]["semantic_state"] != b["audit_trail"][1]["value"]["semantic_state"] and a["audit_trail"][2]["value"]["disposition"] != b["audit_trail"][2]["value"]["disposition"], "identical raw numeric tokens remain opaque and diverge only under exact source-local and target authority")

for case_name, check_id in (("unknown_case", "source_specific_special_fails_closed"), ("missing_case", "typed_missing_member_does_not_self_delete_or_resolve"), ("not_applicable_member_case", "not_applicable_response_does_not_self_delete_denominator")):
    case = make_case(case_name)
    gate = module.denominator_resolution_check(case)
    check(check_id, gate["passed"] is False and gate["ledger"]["raw_denominator_support"] == 1 and gate["ledger"]["raw_resolved_target_support"] == 0 and len(gate["ledger"]["unresolved_record_ids"]) == 1, "typed source/product state remains a denominator member but cannot become an empirical result without a competent resolved target disposition")
    must_fail(check_id + "_result_blocked", lambda case=case: module.emit_empirical_result(case), "EMPIRICAL_RESULT is fail-closed while any denominator member is unresolved")

excluded_result = module.emit_empirical_result(make_case("prequery_exclusion_case"))
check("prequery_authorized_exclusion_is_the_only_denominator_deletion_path", excluded_result["denominator"] == 0 and excluded_result["ledger"]["authorized_prequery_exclusion_ids"] == ["SYNTHETIC_RECORD_G"] and excluded_result["ledger"]["unresolved_record_ids"] == [], "an exact PRE_QUERY ROUTING_RISK_SET decision can exclude a record before denominator construction")

post_data_delete = deepcopy(resolved)
post_data_delete["records"][0]["product_target_disposition"].update(disposition="AUTHORIZED_PREQUERY_EXCLUSION", resolution_basis="PREQUERY_ELIGIBILITY_EXCLUSION_BINDING")
must_fail("post_data_denominator_deletion_forbidden", lambda: module.denominator_resolution_check(post_data_delete), "a target/product disposition cannot convert a PRE_QUERY denominator member into an exclusion")

target_expansion = deepcopy(resolved)
target_expansion["records"][1]["product_target_disposition"]["target_domain_ref"]["content_hash"] = "9" * 64
must_fail("post_data_target_domain_substitution_forbidden", lambda: module.denominator_resolution_check(target_expansion), "every product binding must match the exact target-domain identity frozen in the query envelope")

missing_record = deepcopy(resolved)
missing_record["records"].pop()
must_fail("complete_expected_record_accounting_required", lambda: module.denominator_resolution_check(missing_record), "the observed record set must exactly equal the pre-frozen expected record-id set")

unknown_positive = make_case("unknown_case")
unknown_positive["records"][0]["product_target_disposition"].update(disposition="TARGET_MEMBER", resolution_basis="TARGET_DOMAIN_MEMBER")
must_fail("unmapped_source_special_cannot_be_promoted_by_universal_layer", lambda: module.denominator_resolution_check(unknown_positive), "SOURCE_SPECIFIC_SPECIAL/UNKNOWN states cannot receive a positive universal disposition")

wrong_source_authority = deepcopy(resolved)
wrong_source_authority["records"][0]["source_local_governed_state"]["authority_ref"]["authority_content_hash"] = "8" * 64
must_fail("source_semantic_authority_must_be_frozen_and_exact", lambda: module.denominator_resolution_check(wrong_source_authority), "source-local semantic authority must be one of the content-addressed refs frozen in the query envelope")

wrong_risk_authority = deepcopy(resolved)
wrong_risk_authority["records"][2]["prequery_eligibility"]["authority_ref"]["authority_content_hash"] = "7" * 64
must_fail("exclusion_requires_exact_prequery_risk_authority", lambda: module.denominator_resolution_check(wrong_risk_authority), "denominator exclusion fails if its exact ROUTING_RISK_SET authority differs from the frozen query authority")

reordered = deepcopy(resolved)
reordered["records"] = list(reversed(reordered["records"]))
reordered_result = module.emit_empirical_result(reordered)
check("deterministic_replay_identity", reordered_result["result_hash"] == result["result_hash"] and reordered_result["gate_hash"] == result["gate_hash"], "canonical record ordering and exact authority identities produce stable gate/result hashes")

helper_text = HELPER.read_text(encoding="utf-8")
check("production_helper_has_no_native_code_table", "native_state ==" not in helper_text and "native_state in" not in helper_text and "q301" not in helper_text.lower() and "lits" not in helper_text.lower(), "production helper is source-agnostic and never assigns meaning from a raw code literal")

output = {"contract_id": module.CONTRACT_ID, "status": "PASS", "check_count": len(checks), "checks": checks}
json.dump(output, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
