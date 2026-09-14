from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from rawlsing_next import source_state_target_disposition_contract as production


ROOT = Path(__file__).resolve().parents[2]
J02_SCHEMA = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/HQ_SEVENTH_WAVE_PARTIAL_FANIN_AND_EIGHTH_WAVE_DISPATCH_R1/WORKER_COMMISSIONS/J02/01_CONTRACT_SCHEMA.json"
K02_CORE = ROOT / "rawlsing_next/source_state_target_disposition_contract.py"
K02_ADAPTER = ROOT / "rawlsing_next/pre553_source_state_target_disposition.py"
K02_SELFTEST = ROOT / "evidence/selftest/prev3_source_state_target_disposition_production.py"

K02_CANDIDATE_SHA = "639aec0e6b8310f07283922faf0afdc7e3dc7c48"
K02_CONTENT_SHA256 = {
    K02_CORE: "8c75d41d846363329147ad30187bd30cbfd6dc2e1105f2304e3d94db4150f1d4",
    K02_ADAPTER: "918f0a7e7c8622cc07b9234740e260ac2e4e7560a5aab3ddf534db9b3c36aa6e",
    K02_SELFTEST: "663f3ec3ea0d1d838b8a75b1ee75759a6d971b4ef2cbae9a37d1cb09545ee220",
}
J02_SCHEMA_GIT_BLOB_SHA1 = "a4d916a553b6c5039c57ea8607a15c5ac2df5c47"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def _ref(kind: str, tag: str) -> dict[str, str]:
    digest = hashlib.sha256(f"{kind}:{tag}".encode("utf-8")).hexdigest()
    return {
        "kind": kind,
        "object_id": f"urn:l02:{kind.lower()}:{tag}",
        "content_hash": digest,
    }


def _authority(tag: str) -> dict[str, str]:
    digest = hashlib.sha256(f"authority:{tag}".encode("utf-8")).hexdigest()
    return {
        "authority_id": f"L02-AUTH-{tag}",
        "authority_version": "1.0.0",
        "authority_content_hash": digest,
    }


def _base_contract() -> dict:
    universe = _ref("EmpiricalUniverse@1.0.0", "u")
    target = _ref("QUESTION_NATIVE", "target")
    domain = _ref("TARGET_DOMAIN", "domain")
    risk = _ref("RISK_SET", "risk")
    return {
        "contract_id": production.CONTRACT_ID,
        "world_scope": "OBJECTIVE",
        "authority_phase": "FROZEN_PRE_OUTCOME",
        "risk_set_ref": risk,
        "components": [
            {
                "target_ref": target,
                "target_domain_ref": domain,
                "authority_bindings": [
                    {
                        "empirical_universe_ref": universe,
                        "source_semantic_authority_ref": _authority("source"),
                        "source_semantic_operation": "L02_SOURCE_SEMANTICS",
                        "target_use_authority_ref": _authority("target"),
                        "target_use_operation": "L02_TARGET_USE",
                        "risk_set_authority_ref": _authority("risk"),
                        "risk_set_operation": "L02_PREQUERY_RISK",
                        "replay_authority_ref": _authority("replay"),
                        "replay_operation": "L02_REPLAY",
                    }
                ],
                "state_bindings": [
                    {
                        "empirical_universe_ref": universe,
                        "response_state": "SUBSTANTIVE_RESPONSE",
                        "canonical_response_value": "L02_ALPHA",
                        "state_class": "SOURCE_SUBSTANTIVE",
                        "product_target_disposition": "TARGET_MEMBER",
                    }
                ],
            }
        ],
    }


def _j02_enums() -> tuple[set[str], set[str]]:
    schema = json.loads(J02_SCHEMA.read_text(encoding="utf-8"))
    record = schema["properties"]["records"]["items"]["properties"]
    source_classes = set(
        record["source_local_governed_state"]["properties"]["state_class"]["enum"]
    )
    dispositions = set(
        record["product_target_disposition"]["properties"]["disposition"]["enum"]
    )
    return source_classes, dispositions


def test_exact_k02_candidate_and_j02_authority_are_frozen() -> None:
    assert K02_CANDIDATE_SHA == "639aec0e6b8310f07283922faf0afdc7e3dc7c48"
    for path, expected in K02_CONTENT_SHA256.items():
        assert _sha256(path) == expected, f"K02 candidate content drifted: {path}"
    assert _git_blob_sha1(J02_SCHEMA) == J02_SCHEMA_GIT_BLOB_SHA1


def test_k02_rejects_j02_lawful_source_not_applicable_class() -> None:
    source_classes, _ = _j02_enums()
    token = "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE"
    assert token in source_classes

    hostile = _base_contract()
    binding = hostile["components"][0]["state_bindings"][0]
    binding["response_state"] = "NOT_APPLICABLE"
    binding["canonical_response_value"] = None
    binding["state_class"] = token
    binding["product_target_disposition"] = "UNRESOLVED"

    with pytest.raises(
        production.SourceStateDispositionContractError,
        match="unknown source-local state_class",
    ):
        production.normalize_contract(hostile)

    assert token not in production.STATE_CLASSES


def test_k02_rejects_j02_lawful_typed_missing_product_disposition() -> None:
    _, dispositions = _j02_enums()
    token = "TYPED_MISSING_NONRESPONSE"
    assert token in dispositions

    hostile = _base_contract()
    binding = hostile["components"][0]["state_bindings"][0]
    binding["response_state"] = "DK"
    binding["canonical_response_value"] = None
    binding["state_class"] = "TYPED_MISSING_NONRESPONSE"
    binding["product_target_disposition"] = token

    with pytest.raises(
        production.SourceStateDispositionContractError,
        match="unknown product_target_disposition",
    ):
        production.normalize_contract(hostile)

    assert token not in production.DISPOSITIONS


def test_k02_rejects_j02_lawful_not_applicable_product_disposition() -> None:
    _, dispositions = _j02_enums()
    token = "NOT_APPLICABLE_OR_INELIGIBLE"
    assert token in dispositions

    hostile = _base_contract()
    binding = hostile["components"][0]["state_bindings"][0]
    binding["response_state"] = "NOT_APPLICABLE"
    binding["canonical_response_value"] = None
    binding["state_class"] = "NOT_APPLICABLE_OR_INELIGIBLE"
    binding["product_target_disposition"] = token

    with pytest.raises(
        production.SourceStateDispositionContractError,
        match="unknown product_target_disposition",
    ):
        production.normalize_contract(hostile)

    assert token not in production.DISPOSITIONS


def test_blocker_is_schema_drift_not_denominator_self_deletion() -> None:
    # Control: K02 can represent the same typed-missing observation only by
    # coercing the accepted J02 product-disposition vocabulary to UNRESOLVED.
    # That remains fail-closed, so the blocker is contract incompatibility,
    # not a claim that K02 silently deletes typed-missing denominator members.
    control = _base_contract()
    binding = control["components"][0]["state_bindings"][0]
    binding["response_state"] = "DK"
    binding["canonical_response_value"] = None
    binding["state_class"] = "TYPED_MISSING_NONRESPONSE"
    binding["product_target_disposition"] = "UNRESOLVED"
    normalized = production.normalize_contract(copy.deepcopy(control))
    assert normalized["components"][0]["state_bindings"][0]["product_target_disposition"] == "UNRESOLVED"
