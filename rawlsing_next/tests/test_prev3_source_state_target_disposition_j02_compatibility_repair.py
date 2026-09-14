from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path
import sys

import pytest

CORE_PATH = Path(__file__).resolve().parents[1] / "source_state_target_disposition_contract.py"

spec = importlib.util.spec_from_file_location("m02_j02_compat_contract", CORE_PATH)
contract = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = contract
spec.loader.exec_module(contract)

J02_ACCEPTED_SCHEMA_BLOB = "a4d916a553b6c5039c57ea8607a15c5ac2df5c47"
J02_SOURCE_CLASSES = frozenset({
    "SOURCE_SUBSTANTIVE",
    "TYPED_MISSING_NONRESPONSE",
    "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE",
    "SOURCE_SPECIFIC_SPECIAL",
    "SOURCE_UNKNOWN",
})
J02_RESPONSE_BOUND_PRODUCT_DISPOSITIONS = frozenset({
    "TARGET_MEMBER",
    "RESOLVED_NON_TARGET",
    "TYPED_MISSING_NONRESPONSE",
    "NOT_APPLICABLE_OR_INELIGIBLE",
    "UNRESOLVED",
})


def ref(kind: str, tag: str) -> dict[str, str]:
    digest = hashlib.sha256(f"{kind}:{tag}".encode()).hexdigest()
    return {
        "kind": kind,
        "object_id": f"urn:synthetic:{kind.lower()}:{tag}",
        "content_hash": digest,
    }


def aref(tag: str) -> dict[str, str]:
    digest = hashlib.sha256(f"authority:{tag}".encode()).hexdigest()
    return {
        "authority_id": f"SYNTHETIC-AUTH-{tag}",
        "authority_version": "1.0.0",
        "authority_content_hash": digest,
    }


U = ref("EmpiricalUniverse@1.0.0", "u")
TARGET = ref("QUESTION_NATIVE", "target")
DOMAIN = ref("TARGET_DOMAIN", "domain")
RISK = ref("RISK_SET", "risk")


def authority_binding() -> dict:
    return {
        "empirical_universe_ref": U,
        "source_semantic_authority_ref": aref("source"),
        "source_semantic_operation": "SYNTHETIC_SOURCE_SEMANTICS",
        "target_use_authority_ref": aref("target"),
        "target_use_operation": "SYNTHETIC_TARGET_USE",
        "risk_set_authority_ref": aref("risk"),
        "risk_set_operation": "SYNTHETIC_PREQUERY_RISK",
        "replay_authority_ref": aref("replay"),
        "replay_operation": "SYNTHETIC_REPLAY",
    }


def base_contract() -> dict:
    return {
        "contract_id": contract.CONTRACT_ID,
        "world_scope": "OBJECTIVE",
        "authority_phase": "FROZEN_PRE_OUTCOME",
        "risk_set_ref": RISK,
        "components": [{
            "target_ref": TARGET,
            "target_domain_ref": DOMAIN,
            "authority_bindings": [authority_binding()],
            "state_bindings": [
                {
                    "empirical_universe_ref": U,
                    "response_state": "SUBSTANTIVE_RESPONSE",
                    "canonical_response_value": "YES",
                    "state_class": "SOURCE_SUBSTANTIVE",
                    "product_target_disposition": "TARGET_MEMBER",
                },
                {
                    "empirical_universe_ref": U,
                    "response_state": "DK",
                    "canonical_response_value": None,
                    "state_class": "TYPED_MISSING_NONRESPONSE",
                    "product_target_disposition": "TYPED_MISSING_NONRESPONSE",
                },
                {
                    "empirical_universe_ref": U,
                    "response_state": "NOT_APPLICABLE",
                    "canonical_response_value": None,
                    "state_class": "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE",
                    "product_target_disposition": "NOT_APPLICABLE_OR_INELIGIBLE",
                },
            ],
        }],
    }


def observe(component, record_id: str, response_state: str):
    return contract.audit_observation(
        component=component,
        record_id=record_id,
        universe_ref=U,
        event_ref=ref("RespondentEvent@1.0.0", record_id),
        opaque_raw_state_hash=contract.semantic_hash({"opaque": record_id}),
        response_state=response_state,
        canonical_response_value="YES" if response_state == "SUBSTANTIVE_RESPONSE" else None,
        source_semantic_authority_ref=aref("source"),
    )


def test_exact_j02_vocabulary_surface_is_restored():
    assert J02_ACCEPTED_SCHEMA_BLOB == "a4d916a553b6c5039c57ea8607a15c5ac2df5c47"
    assert contract.STATE_CLASSES == J02_SOURCE_CLASSES
    assert contract.DISPOSITIONS == J02_RESPONSE_BOUND_PRODUCT_DISPOSITIONS
    normalized = contract.normalize_contract(base_contract())
    rows = normalized["components"][0]["state_bindings"]
    assert {row["state_class"] for row in rows} >= {
        "TYPED_MISSING_NONRESPONSE",
        "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE",
    }
    assert {row["product_target_disposition"] for row in rows} >= {
        "TYPED_MISSING_NONRESPONSE",
        "NOT_APPLICABLE_OR_INELIGIBLE",
    }


def test_unauthorized_k02_source_class_substitution_is_rejected():
    raw = base_contract()
    raw["components"][0]["state_bindings"][2]["state_class"] = "NOT_APPLICABLE_OR_INELIGIBLE"
    with pytest.raises(contract.SourceStateDispositionContractError, match="unknown source-local state_class"):
        contract.normalize_contract(raw)


def test_typed_missing_is_typed_but_does_not_self_delete_denominator_member():
    normalized = contract.normalize_contract(base_contract())
    component = contract.component_for_target(normalized, TARGET)
    observation = observe(component, "R_TYPED", "DK")
    assert observation["audit_trail"][2]["value"] == contract.TYPED_MISSING_NONRESPONSE
    audit = contract.build_record_audit("R_TYPED", [observation])
    gate = contract.denominator_resolution_check(
        contract=normalized,
        scope_identity={"scope": "M02"},
        expected_record_ids=["R_TYPED"],
        record_audits=[audit],
    )
    assert audit["resolved"] is False
    assert gate["raw_denominator_support"] == 1
    assert gate["raw_resolved_target_support"] == 0
    assert gate["unresolved_record_ids"] == ["R_TYPED"]
    assert gate["passed"] is False


def test_not_applicable_is_typed_but_does_not_self_delete_denominator_member():
    normalized = contract.normalize_contract(base_contract())
    component = contract.component_for_target(normalized, TARGET)
    observation = observe(component, "R_NA", "NOT_APPLICABLE")
    assert observation["audit_trail"][2]["value"] == contract.NOT_APPLICABLE_OR_INELIGIBLE
    audit = contract.build_record_audit("R_NA", [observation])
    gate = contract.denominator_resolution_check(
        contract=normalized,
        scope_identity={"scope": "M02"},
        expected_record_ids=["R_NA"],
        record_audits=[audit],
    )
    assert audit["resolved"] is False
    assert gate["raw_denominator_support"] == 1
    assert gate["raw_resolved_target_support"] == 0
    assert gate["unresolved_record_ids"] == ["R_NA"]
    assert gate["passed"] is False


def test_absent_competent_binding_still_fails_closed_to_unresolved():
    normalized = contract.normalize_contract(base_contract())
    component = contract.component_for_target(normalized, TARGET)
    observation = observe(component, "R_SPECIAL", "SOURCE_SPECIFIC_SPECIAL")
    assert observation["audit_trail"][2]["value"] == contract.UNRESOLVED
    assert observation["audit_trail"][1]["value"]["binding_state"] == "NO_TARGET_SPECIFIC_BINDING"


def test_prequery_exclusion_cannot_be_smuggled_into_target_state_binding():
    raw = copy.deepcopy(base_contract())
    raw["components"][0]["state_bindings"][0]["product_target_disposition"] = "AUTHORIZED_PREQUERY_EXCLUSION"
    with pytest.raises(contract.SourceStateDispositionContractError, match="unknown product_target_disposition"):
        contract.normalize_contract(raw)


def test_generic_runtime_remains_source_agnostic_and_raw_value_opaque():
    text = CORE_PATH.read_text(encoding="utf-8").lower()
    assert "q301" not in text
    assert "lits" not in text
    assert "native_code_table" not in text
    raw = copy.deepcopy(base_contract())
    raw["components"][0]["state_bindings"][0]["native_code"] = 7
    with pytest.raises(contract.SourceStateDispositionContractError):
        contract.normalize_contract(raw)
