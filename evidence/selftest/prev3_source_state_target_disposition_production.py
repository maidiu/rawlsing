#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
CORE = ROOT / "rawlsing_next" / "source_state_target_disposition_contract.py"
ADAPTER = ROOT / "rawlsing_next" / "pre553_source_state_target_disposition.py"

spec = importlib.util.spec_from_file_location("contract", CORE)
contract = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = contract
spec.loader.exec_module(contract)


def ref(kind, tag):
    import hashlib
    h = hashlib.sha256(f"{kind}:{tag}".encode()).hexdigest()
    return {"kind": kind, "object_id": f"urn:synthetic:{kind.lower()}:{tag}", "content_hash": h}


def aref(tag):
    import hashlib
    h = hashlib.sha256(f"authority:{tag}".encode()).hexdigest()
    return {"authority_id": f"SYNTHETIC-AUTH-{tag}", "authority_version": "1.0.0", "authority_content_hash": h}


u1 = ref("EmpiricalUniverse@1.0.0", "u1")
u2 = ref("EmpiricalUniverse@1.0.0", "u2")
target = ref("QUESTION_NATIVE", "target")
domain = ref("TARGET_DOMAIN", "domain")
risk = ref("RISK_SET", "risk")


def auth_binding(universe, tag):
    return {
        "empirical_universe_ref": universe,
        "source_semantic_authority_ref": aref(f"source-{tag}"),
        "source_semantic_operation": "SYNTHETIC_SOURCE_SEMANTICS",
        "target_use_authority_ref": aref(f"target-{tag}"),
        "target_use_operation": "SYNTHETIC_TARGET_USE",
        "risk_set_authority_ref": aref(f"risk-{tag}"),
        "risk_set_operation": "SYNTHETIC_PREQUERY_RISK",
        "replay_authority_ref": aref(f"replay-{tag}"),
        "replay_operation": "SYNTHETIC_REPLAY",
    }


raw_contract = {
    "contract_id": contract.CONTRACT_ID,
    "world_scope": "OBJECTIVE",
    "authority_phase": "FROZEN_PRE_OUTCOME",
    "risk_set_ref": risk,
    "components": [{
        "target_ref": target,
        "target_domain_ref": domain,
        "authority_bindings": [auth_binding(u1, "u1"), auth_binding(u2, "u2")],
        "state_bindings": [
            {
                "empirical_universe_ref": u1,
                "response_state": "SUBSTANTIVE_RESPONSE",
                "canonical_response_value": "SYNTHETIC_ALPHA",
                "state_class": "SOURCE_SUBSTANTIVE",
                "product_target_disposition": "TARGET_MEMBER",
            },
            {
                "empirical_universe_ref": u2,
                "response_state": "SUBSTANTIVE_RESPONSE",
                "canonical_response_value": "SYNTHETIC_BETA",
                "state_class": "SOURCE_SUBSTANTIVE",
                "product_target_disposition": "RESOLVED_NON_TARGET",
            },
            {
                "empirical_universe_ref": u1,
                "response_state": "DK",
                "canonical_response_value": None,
                "state_class": "TYPED_MISSING_NONRESPONSE",
                "product_target_disposition": "UNRESOLVED",
            },
        ],
    }],
}
normalized = contract.normalize_contract(raw_contract)
component = contract.component_for_target(normalized, target)
checks = []


def ok(name, condition, detail):
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    checks.append({"check": name, "status": "PASS", "detail": detail})


# Same opaque native material may occur in different sources without acquiring a universal meaning.
raw_hash_u1 = contract.semantic_hash({"raw_response_value": 7})
raw_hash_u2 = contract.semantic_hash({"raw_response_value": 7})
a1 = contract.audit_observation(
    component=component,
    record_id="SYNTHETIC_RECORD_U1",
    universe_ref=u1,
    event_ref=ref("RespondentEvent@1.0.0", "e1"),
    opaque_raw_state_hash=raw_hash_u1,
    response_state="SUBSTANTIVE_RESPONSE",
    canonical_response_value="SYNTHETIC_ALPHA",
    source_semantic_authority_ref=aref("source-u1"),
)
a2 = contract.audit_observation(
    component=component,
    record_id="SYNTHETIC_RECORD_U2",
    universe_ref=u2,
    event_ref=ref("RespondentEvent@1.0.0", "e2"),
    opaque_raw_state_hash=raw_hash_u2,
    response_state="SUBSTANTIVE_RESPONSE",
    canonical_response_value="SYNTHETIC_BETA",
    source_semantic_authority_ref=aref("source-u2"),
)
ok(
    "same_native_material_no_universal_meaning",
    raw_hash_u1 == raw_hash_u2
    and a1["audit_trail"][2]["value"] == contract.TARGET_MEMBER
    and a2["audit_trail"][2]["value"] == contract.RESOLVED_NON_TARGET,
    "identical opaque raw material is not the lookup key; governed source-local states resolve differently",
)

# Unmapped and typed nonresponse states remain unresolved unless target-specific binding says otherwise.
unmapped = contract.audit_observation(
    component=component,
    record_id="SYNTHETIC_RECORD_UNMAPPED",
    universe_ref=u1,
    event_ref=ref("RespondentEvent@1.0.0", "e3"),
    opaque_raw_state_hash=contract.semantic_hash({"raw_response_value": 99}),
    response_state="SOURCE_SPECIFIC_SPECIAL",
    canonical_response_value=None,
    source_semantic_authority_ref=aref("source-u1"),
)
dk = contract.audit_observation(
    component=component,
    record_id="SYNTHETIC_RECORD_DK",
    universe_ref=u1,
    event_ref=ref("RespondentEvent@1.0.0", "e4"),
    opaque_raw_state_hash=contract.semantic_hash({"raw_response_value": "opaque"}),
    response_state="DK",
    canonical_response_value=None,
    source_semantic_authority_ref=aref("source-u1"),
)
ok(
    "unmapped_and_nonresponse_fail_closed",
    unmapped["audit_trail"][2]["value"] == contract.UNRESOLVED
    and dk["audit_trail"][2]["value"] == contract.UNRESOLVED,
    "unmapped source specials and explicit DK do not receive a generic target meaning",
)

# Denominator cannot be shrunk by target outcome; unresolved remains in expected record ids and blocks result.
r1 = contract.build_record_audit("SYNTHETIC_RECORD_U1", [a1])
r_bad = contract.build_record_audit("SYNTHETIC_RECORD_DK", [dk])
gate_bad = contract.denominator_resolution_check(
    contract=normalized,
    scope_identity={"scope": "SYNTHETIC_SCOPE"},
    expected_record_ids=["SYNTHETIC_RECORD_U1", "SYNTHETIC_RECORD_DK"],
    record_audits=[r1, r_bad],
)
ok(
    "unresolved_denominator_member_retained",
    gate_bad["raw_denominator_support"] == 2
    and gate_bad["raw_resolved_target_support"] == 1
    and gate_bad["passed"] is False
    and gate_bad["unresolved_record_ids"] == ["SYNTHETIC_RECORD_DK"],
    "unresolved target state remains in the frozen denominator and blocks the gate",
)
blocked = False
try:
    contract.empirical_result_receipt(
        contract=normalized,
        denominator_checks=[gate_bad],
        query_ref=ref("EmpiricalQuerySpec@1.0.0", "q"),
        release_refs=[ref("C11_RELEASE", "r")],
        fact_rows=[],
    )
except contract.SourceStateDispositionContractError:
    blocked = True
ok("result_emission_after_gate_only", blocked, "EMPIRICAL_RESULT is unavailable while gate is unresolved")

# Exact accounting: missing/duplicate record ids are contract failures.
missing_blocked = duplicate_blocked = False
try:
    contract.denominator_resolution_check(
        contract=normalized,
        scope_identity={"scope": "SYNTHETIC_SCOPE"},
        expected_record_ids=["A", "B"],
        record_audits=[contract.build_record_audit("A", [dict(a1, record_id="A")])],
    )
except contract.SourceStateDispositionContractError:
    missing_blocked = True
try:
    contract.denominator_resolution_check(
        contract=normalized,
        scope_identity={"scope": "SYNTHETIC_SCOPE"},
        expected_record_ids=["A", "A"],
        record_audits=[],
    )
except contract.SourceStateDispositionContractError:
    duplicate_blocked = True
ok("exact_record_accounting", missing_blocked and duplicate_blocked, "missing or duplicate expected ids fail closed")

# Post-outcome denominator deletion is not even an accepted target disposition token.
post_outcome_blocked = False
mutated = json.loads(json.dumps(raw_contract))
mutated["components"][0]["state_bindings"][0]["product_target_disposition"] = "AUTHORIZED_PREQUERY_EXCLUSION"
try:
    contract.normalize_contract(mutated)
except contract.SourceStateDispositionContractError:
    post_outcome_blocked = True
ok(
    "no_post_outcome_denominator_deletion",
    post_outcome_blocked,
    "target-state binding cannot express denominator exclusion; exclusion belongs to frozen risk-set authority",
)

# Risk-set and target-use authorities must remain distinct.
not_distinct_blocked = False
mutated = json.loads(json.dumps(raw_contract))
mutated["components"][0]["authority_bindings"][0]["risk_set_authority_ref"] = (
    mutated["components"][0]["authority_bindings"][0]["target_use_authority_ref"]
)
try:
    contract.normalize_contract(mutated)
except contract.SourceStateDispositionContractError:
    not_distinct_blocked = True
ok("risk_target_authority_distinct", not_distinct_blocked, "risk-set authority cannot collapse into target-use authority")

# Pre-outcome phase is fixed; no data-dependent phase can be supplied.
phase_blocked = False
mutated = json.loads(json.dumps(raw_contract))
mutated["authority_phase"] = "POST_OUTCOME"
try:
    contract.normalize_contract(mutated)
except contract.SourceStateDispositionContractError:
    phase_blocked = True
ok("risk_authority_preoutcome_frozen", phase_blocked, "only FROZEN_PRE_OUTCOME authority phase is accepted")

# Generic schema rejects native/raw/source-family fields, making native-code tables structurally inexpressible.
native_field_blocked = False
mutated = json.loads(json.dumps(raw_contract))
mutated["components"][0]["state_bindings"][0]["native_code"] = 7
try:
    contract.normalize_contract(mutated)
except contract.SourceStateDispositionContractError:
    native_field_blocked = True
ok("native_code_table_inexpressible", native_field_blocked, "state-binding schema has no native/raw/source-family key")

# Substantive state cannot resolve without governed canonical response value.
raw_fallback_blocked = False
mutated = json.loads(json.dumps(raw_contract))
mutated["components"][0]["state_bindings"][0]["canonical_response_value"] = None
try:
    contract.normalize_contract(mutated)
except contract.SourceStateDispositionContractError:
    raw_fallback_blocked = True
ok("raw_value_fallback_forbidden", raw_fallback_blocked, "substantive resolution requires authorized canonical value")

# Fully resolved denominator emits result and replay identity is order invariant/deterministic.
r2 = contract.build_record_audit("SYNTHETIC_RECORD_U2", [a2])
gate1 = contract.denominator_resolution_check(
    contract=normalized,
    scope_identity={"scope": "SYNTHETIC_SCOPE"},
    expected_record_ids=["SYNTHETIC_RECORD_U1", "SYNTHETIC_RECORD_U2"],
    record_audits=[r1, r2],
)
gate2 = contract.denominator_resolution_check(
    contract=normalized,
    scope_identity={"scope": "SYNTHETIC_SCOPE"},
    expected_record_ids=["SYNTHETIC_RECORD_U2", "SYNTHETIC_RECORD_U1"],
    record_audits=[r2, r1],
)
ok(
    "resolved_support_equals_denominator",
    gate1["passed"] is True
    and gate1["raw_resolved_target_support"] == gate1["raw_denominator_support"] == 2,
    "resolved gate requires exact support equality",
)
fact = {
    "fact_ref": ref("EmpiricalFact@1.0.0", "fact"),
    "typed_state": "SUPPORTED",
    "raw_denominator_support": 2,
    "raw_resolved_target_support": 2,
}
result1 = contract.empirical_result_receipt(
    contract=normalized,
    denominator_checks=[gate1],
    query_ref=ref("EmpiricalQuerySpec@1.0.0", "q"),
    release_refs=[ref("C11_RELEASE", "r")],
    fact_rows=[fact],
)
result2 = contract.empirical_result_receipt(
    contract=normalized,
    denominator_checks=[gate2],
    query_ref=ref("EmpiricalQuerySpec@1.0.0", "q"),
    release_refs=[ref("C11_RELEASE", "r")],
    fact_rows=[fact],
)
replay1 = contract.replay_identity(contract=normalized, denominator_checks=[gate1], empirical_result=result1)
replay2 = contract.replay_identity(contract=normalized, denominator_checks=[gate2], empirical_result=result2)
ok(
    "deterministic_replay_identity",
    gate1["check_hash"] == gate2["check_hash"] and result1["result_hash"] == result2["result_hash"] and replay1 == replay2,
    "record ordering does not alter gate/result/replay identity",
)

# A supported fact with mismatched resolved-vs-denominator support is rejected.
support_mismatch_blocked = False
bad_fact = dict(fact)
bad_fact["raw_resolved_target_support"] = 1
try:
    contract.empirical_result_receipt(
        contract=normalized,
        denominator_checks=[gate1],
        query_ref=ref("EmpiricalQuerySpec@1.0.0", "q"),
        release_refs=[ref("C11_RELEASE", "r")],
        fact_rows=[bad_fact],
    )
except contract.SourceStateDispositionContractError:
    support_mismatch_blocked = True
ok("supported_fact_support_equality_enforced", support_mismatch_blocked, "resolved result support equality is mandatory")

# Static adapter ceiling: no source-specific identifiers or literal native-code mapping appears.
adapter_text = ADAPTER.read_text(encoding="utf-8")
forbidden_source_tokens = ["q301", "lits", "wvs", "native_code_table", "native_code_map"]
ok(
    "adapter_source_agnostic",
    all(token not in adapter_text.lower() for token in forbidden_source_tokens),
    "production adapter contains no survey-specific/native-code table identifiers",
)
forbidden_legacy = ["dri" + "ver", "person" + "-terminal"]
ok(
    "quarantined_legacy_vocabulary_absent",
    all(token not in (CORE.read_text(encoding="utf-8") + adapter_text).lower() for token in forbidden_legacy),
    "new production artifacts do not revive quarantined legacy vocabulary",
)

print(json.dumps({
    "contract_id": contract.CONTRACT_ID,
    "adapter_id": "PRE553_SOURCE_STATE_TARGET_DISPOSITION_ADAPTER@1.0.0",
    "status": "PASS",
    "contract_hash": contract.contract_hash(normalized),
    "resolved_gate_hash": gate1["check_hash"],
    "resolved_result_hash": result1["result_hash"],
    "resolved_replay_identity": replay1,
    "checks": checks,
}, indent=2, sort_keys=True))
