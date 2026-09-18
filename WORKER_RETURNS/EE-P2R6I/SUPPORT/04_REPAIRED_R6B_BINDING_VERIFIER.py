#!/usr/bin/env python3
"""Verify an EE-P2R6B concrete ReleaseRealizationBinding candidate fail-closed."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ISSUER_PATH = HERE / "03_REPAIRED_R6B_BINDING_ISSUER.py"
EXPECTED_ISSUER_GIT_BLOB_SHA1 = "8fd59bc69cd549c39b81bef7d44bb96c1bc0b7c6"

class VerificationError(ValueError):
    pass

def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)

def load_exact_issuer():
    require(ISSUER_PATH.is_file(), "issuer artifact missing")
    require(git_blob_sha1(ISSUER_PATH) == EXPECTED_ISSUER_GIT_BLOB_SHA1,
            "issuer Git blob identity mismatch")
    spec = importlib.util.spec_from_file_location("ee_p2r6b_exact_issuer", ISSUER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load exact issuer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def inspect_active_inventory(authority: Mapping[str, Any], candidate: Mapping[str, Any], issuer) -> None:
    inventory = authority.get("active_binding_inventory", {})
    bindings = inventory.get("active_positive_bindings", [])
    if not isinstance(bindings, list):
        raise VerificationError("active binding inventory list missing")
    if len(bindings) > 1:
        raise VerificationError("multiple active positive bindings for one scope/source/authority epoch")
    if len(bindings) == 1:
        existing = bindings[0]
        if not isinstance(existing, Mapping):
            raise VerificationError("active binding inventory member malformed")
        target = candidate.get("identity_material", {}).get("runtime_i02_release_ref")
        existing_target = existing.get("runtime_i02_release_ref")
        same_key = (
            existing.get("frozen_scope_anchor_hash") == issuer.FROZEN_SCOPE_HASH
            and existing.get("source_sha256") == issuer.SOURCE_SHA256
            and existing.get("authority_epoch_id") == issuer.AUTHORITY_EPOCH_ID
        )
        if same_key and existing_target != target:
            raise VerificationError("same anchor/source/authority epoch already bound to different active runtime release")
        raise VerificationError("pre-existing active positive binding exists; verifier requires zero before candidate issuance")

def verify_candidate(
    *,
    candidate_path: Path,
    receipt_path: Path,
    replay_path: Path,
    m01_m18_path: Path,
    extension_scan_path: Path,
    authority_path: Path,
) -> dict[str, Any]:
    issuer = load_exact_issuer()
    candidate = load_json(candidate_path)
    authority = load_json(authority_path)

    require(candidate.get("schema") == "EE_P2R6B_RELEASE_REALIZATION_BINDING_CANDIDATE@1.0.0",
            "candidate schema mismatch/non-production fixture")
    require(candidate.get("status") == "CANDIDATE__HQ_ADOPTION_REQUIRED__NOT_ACTIVE_UNTIL_ADOPTED",
            "candidate status must remain non-active pending HQ adoption")
    require(candidate.get("activation") == "HQ_ADOPTION_REQUIRED__ISSUER_OUTPUT_ALONE_IS_NOT_ACTIVE_AUTHORITY",
            "candidate incorrectly self-activates")
    inspect_active_inventory(authority, candidate, issuer)

    try:
        expected = issuer.issue_binding_candidate(
            receipt_path, replay_path, m01_m18_path, extension_scan_path, authority_path
        )
    except issuer.IssuerError as exc:
        raise VerificationError(f"issuer proof closure fails: {exc}") from exc
    require(canonical_json(candidate) == canonical_json(expected),
            "candidate differs from deterministic exact reconstruction")

    material = candidate.get("identity_material")
    require(isinstance(material, Mapping), "identity_material missing")
    binding_ref = candidate.get("binding_ref")
    issuer.require_exact_ref(binding_ref, "binding_ref", kind="ReleaseRealizationBindingCandidate@1.0.0")
    require(binding_ref["content_hash"] == issuer.sha256_obj(material), "binding candidate content address mismatch")
    require(material.get("relation_authority_ref") == issuer.RELATION_AUTHORITY_REF, "wrong R5A relation authority identity")
    require(material.get("binding_schema_ref") == issuer.BINDING_SCHEMA_REF, "wrong R5A binding schema identity")
    require(material.get("r4a_successor_clause_ref") == issuer.R4A_SUCCESSOR_CLAUSE_REF,
            "wrong R4A successor-clause identity")
    require(material.get("r5a_aggregate_ref") == issuer.R5A_AGGREGATE_REF, "wrong R5A aggregate identity")
    require(material.get("r4a_authority_closure_hash") == issuer.R4A_AGGREGATE_HASH,
            "wrong R4A authority closure")
    require(material.get("authority_epoch_id") == issuer.AUTHORITY_EPOCH_ID, "wrong authority epoch")
    require(material.get("source_sha256") == issuer.SOURCE_SHA256, "cross-source realization forbidden")
    require(material.get("frozen_scope_anchor_ref") == issuer.FROZEN_SCOPE_REF, "frozen scope anchor changed")
    require(material.get("accepted_base_i02_release_ref") == issuer.BASE_RELEASE_REF, "accepted base lineage changed")
    runtime_ref = issuer.require_exact_ref(material.get("runtime_i02_release_ref"),
                                           "runtime_i02_release_ref", kind="C11LogicalRelease")
    require(runtime_ref["content_hash"] != issuer.FROZEN_SCOPE_HASH,
            "runtime release equals frozen F02 scope anchor")
    require(material.get("direction") == "FROZEN_F02_SCOPE_ANCHOR_TO_ACCEPTED_PUBLIC_I02_RUNTIME_RELEASE",
            "binding direction changed")
    require(material.get("relation_semantics") ==
            "REALIZATION__NOT_IDENTITY_EQUALITY_ALIAS_OR_BIDIRECTIONAL_SUCCESSION",
            "binding semantics imply equality/aliasing")

    repo = material.get("repository_resolution_evidence", {})
    require(repo.get("operation") == "C11Repository.resolve_release_exact", "repository resolution operation mismatch")
    require(repo.get("resolution_mode") == "EXACT", "repository release must resolve exactly")
    require(repo.get("result") == "PASS", "repository exact resolution not PASS")
    require(repo.get("runtime_release_ref") == runtime_ref, "repository exact resolution points to different release")
    resolution_text = canonical_json(repo).lower()
    require(not any(word in resolution_text for word in issuer.FORBIDDEN_RESOLUTION_WORDS),
            "latest/default/fuzzy/nearest repository resolution forbidden")

    boundary = candidate.get("semantic_boundary", {})
    require(boundary == {
        "directional_realization_only": True,
        "identity_equality_claimed": False,
        "alias_claimed": False,
        "reverse_inference_authorized": False,
        "selector_ast_mutated": False,
        "selector_truth_conditions_mutated": False,
        "post_outcome_mutation": False,
    }, "semantic boundary/post-outcome mutation violation")

    proof = candidate.get("proof_closure", {})
    require(proof.get("r5b_verifier_git_blob_sha1") == issuer.R5B_VERIFIER_GIT_BLOB_SHA1,
            "wrong R5B verifier identity")
    require(proof.get("r5b_verifier_pass") is True, "R5B verifier proof missing")
    require(proof.get("source_sha256") == issuer.SOURCE_SHA256, "proof closure source mismatch")
    require(proof.get("r4a_authority_hashes") == issuer.R4A_AUTHORITY_HASHES, "R4A proof closure mismatch")
    require(proof.get("active_binding_inventory_material_hash") ==
            authority["active_binding_inventory"]["inventory_material_hash"],
            "uniqueness inventory proof not bound")
    require(material.get("authority_epoch_status") == "PRE_BINDING__ZERO_ACTIVE_POSITIVE_BINDINGS_VERIFIED",
            "candidate did not prove zero active binding before issuance")

    extension = candidate.get("extension_identity_set", {})
    require(extension.get("selector_hashes") == issuer.EXPECTED_SELECTORS,
            "required six F02 selector identities changed/missing")
    issuer.normalized_q_members(extension.get("f02_extension_refs"), "candidate.extension_identity_set.f02_extension_refs")
    issuer.normalized_f02_authorities(extension.get("f02_authority_refs"),
                                      "candidate.extension_identity_set.f02_authority_refs")
    require(material.get("extension_member_identity_set_hash") == issuer.sha256_obj(extension),
            "extension-member identity-set hash mismatch")

    return {
        "status": "PASS",
        "binding_ref": binding_ref,
        "runtime_i02_release_ref": runtime_ref,
        "authority_epoch_id": issuer.AUTHORITY_EPOCH_ID,
        "zero_preexisting_active_binding_verified": True,
        "candidate_active": False,
        "hq_adoption_required": True,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--replay-manifest", required=True, type=Path)
    parser.add_argument("--m01-m18", required=True, type=Path)
    parser.add_argument("--extension-scan", required=True, type=Path)
    parser.add_argument("--authority-material", required=True, type=Path)
    args = parser.parse_args()
    result = verify_candidate(
        candidate_path=args.candidate,
        receipt_path=args.receipt,
        replay_path=args.replay_manifest,
        m01_m18_path=args.m01_m18,
        extension_scan_path=args.extension_scan,
        authority_path=args.authority_material,
    )
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
