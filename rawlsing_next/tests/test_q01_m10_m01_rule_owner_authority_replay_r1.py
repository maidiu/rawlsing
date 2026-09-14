"""Replay court for the bounded Q01 M10-M01 RULE_OWNER authority artifact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ARTIFACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "Q01_M10_M01_RULE_OWNER_AUTHORITY_R1.json"
)

EXPECTED = {
    "owner": "a75a1f35da0775343d1098d34268861b991cfccd63922fbf7161cbf73a8ce0cd",
    "scope": "b6f0bb622158e797aaf4a90b609497ae94c089986e93356532241a64732f4e12",
    "selection": "4d62f67ede66fe0b3b60d46b16934c90024048716d7cc460095807762f14f9b5",
    "authority": "80fd8e9a59b76e36392872c13536cdebf7de6273e5233d6bd285c1d0027a7289",
    "binding": "8b98c6095cc401d58b054b458d4b6b5cfc69176c82b98b62d6bd0735b3f51040",
}


def _semantic_hash(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def test_q01_m10_m01_rule_owner_authority_replays_exactly() -> None:
    artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    assert artifact["artifact_id"] == "SDTF_M10_M01_RULE_OWNER_AUTHORITY_R1@1.0.0"
    assert artifact["candidate"] == {
        "candidate_id": "M10-M01",
        "candidate_name": "PROPERTY SEPARATION / WAGE DEPENDENCY",
        "mechanism_class_ceiling": "P1 MATERIAL_ACCESS_DEPENDENCY",
    }

    assert _semantic_hash(artifact["semantic_owner_material"]) == EXPECTED["owner"]
    assert artifact["semantic_owner_ref"]["content_hash"] == EXPECTED["owner"]

    assert _semantic_hash(artifact["scope_material"]) == EXPECTED["scope"]
    assert artifact["scope_ref"]["content_hash"] == EXPECTED["scope"]

    assert (
        _semantic_hash(artifact["current_selection_evidence_material"])
        == EXPECTED["selection"]
    )
    assert (
        artifact["current_selection_evidence_ref"]["content_hash"]
        == EXPECTED["selection"]
    )

    assert _semantic_hash(artifact["authority_material"]) == EXPECTED["authority"]
    assert (
        artifact["authority_ref"]["authority_content_hash"]
        == EXPECTED["authority"]
    )

    assert (
        _semantic_hash(artifact["rule_owner_binding_material"])
        == EXPECTED["binding"]
    )
    assert artifact["rule_owner_binding_ref"]["content_hash"] == EXPECTED["binding"]

    owner = artifact["rule_owner_binding_material"]["rule_owner"]
    assert owner["role"] == "RULE_OWNER"
    assert owner["disposition"] == "BOUND"
    assert owner["scope_or_na_ref"] == artifact["scope_ref"]
    assert owner["authority_ref"] == artifact["authority_ref"]
    assert owner["current_selection_evidence_refs"] == [
        artifact["current_selection_evidence_ref"]
    ]

    authority = artifact["authority_material"]
    assert authority["authority_role"] == "RULE_OWNER"
    assert authority["scope_ref"] == artifact["scope_ref"]
    assert authority["semantic_owner_ref"] == artifact["semantic_owner_ref"]
    assert authority["current_selection_evidence_refs"] == [
        artifact["current_selection_evidence_ref"]
    ]
    assert "causal_use_authority" not in authority
    assert "rule_currentness" not in authority

    provenance = authority["provenance"]
    assert provenance["hq_fanin_commit"] == "4c2a0e9b0423be77a51284b34e87a3f8ae59a321"
    assert provenance["q01_commission_commit"] == "8a5bac3c88353f84cadfc1642e5d1ead0051c3e8"
    assert provenance["p03_return_commit"] == "903079c179abca4eabd163c99b19efdef1855ce9"
    assert provenance["source_worker_commit"] == "0ebca9ff111bea63838f9b68c8e5c3cb93d9d128"
    assert provenance["source_ledger_blob_sha1"] == "606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7"
    assert (
        provenance["binding_contract_id"]
        == "SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0"
    )
    assert provenance["binding_contract_blob_sha1"] == "c94997f5c7f2bbee9cd99c570554fd48c0f47556"
    assert provenance["mechanism_class_ceiling"] == "P1 MATERIAL_ACCESS_DEPENDENCY"

    selection = artifact["current_selection_evidence_material"]
    assert (
        selection["selected_authority_id"]
        == artifact["authority_ref"]["authority_id"]
    )
    assert (
        selection["selected_authority_version"]
        == artifact["authority_ref"]["authority_version"]
    )

    ceilings = set(authority["negative_ceilings"])
    assert "NO_CAUSAL_USE_AUTHORITY" in ceilings
    assert "NO_CONCRETE_MECHANISM_RULE" in ceilings
    assert "NO_RULE_CURRENT_ACCEPTED" in ceilings
    assert "SOURCE_CITATION_DOES_NOT_SELF_ISSUE_RULE_OWNER_AUTHORITY" in ceilings
    assert "P1_CLASS_MEMBERSHIP_DOES_NOT_SELF_ISSUE_RULE_OWNER_AUTHORITY" in ceilings
    assert (
        "HQ_DESIRE_WITHOUT_EXACT_COMMITTED_DELEGATION_DOES_NOT_SELF_ISSUE_RULE_OWNER_AUTHORITY"
        in ceilings
    )
