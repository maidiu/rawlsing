#!/usr/bin/env python3
"""EE-P2R6J deterministic R5A/R6A-compatible binding preimage issuer.

This module issues only an inactive structural candidate plus the proposed
ACTIVE_POSITIVE record used for qualification.  It does not activate authority.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

REQUIRED_FIELDS = (
    "relation_authority_ref",
    "frozen_scope_anchor_ref",
    "source_artifact_sha256",
    "accepted_base_i02_release_ref",
    "accepted_base_replay_manifest_hash",
    "runtime_i02_release_ref",
    "runtime_candidate_projection_hash",
    "runtime_replay_manifest_ref",
    "runtime_m01_m18_coverage",
    "c11_repository_exact_resolution_receipt",
    "f02_extension_refs",
    "f02_authority_refs",
    "adopted_r4a_authority_refs",
    "selector_refs",
    "selector_truth_semantics",
    "respondent_binding_semantics",
    "f02_member_law",
)
CURRENT_SNAPSHOT_HASH = "209cca7eb759c8fc2df265a0673d180f699381b164e80b88acfa5199438e2b56"
QUARANTINED_R6I_HASH = "fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0"
R6L_RETURN_HEAD = "1e0a22b6e8b4d25e1b40a0b915bb497369d72b6c"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_corrected_identity_material(
    *,
    binding_schema: Mapping[str, Any],
    relation_authority: Mapping[str, Any],
    r6l_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    required = copy.deepcopy(binding_schema["future_binding_required_fields"])
    _require(tuple(required.keys()) == REQUIRED_FIELDS, "R5A future-binding field order/surface mismatch")
    successor = r6l_receipt["accepted_i02_successor"]
    required["relation_authority_ref"] = copy.deepcopy(relation_authority["authority_ref"])
    required["runtime_i02_release_ref"] = copy.deepcopy(successor["release_ref"])
    required["runtime_candidate_projection_hash"] = successor["candidate_projection_hash"]
    required["runtime_replay_manifest_ref"] = copy.deepcopy(successor["replay_manifest_ref"])
    required["runtime_m01_m18_coverage"] = copy.deepcopy(successor["m01_m18_coverage"])
    required["c11_repository_exact_resolution_receipt"] = copy.deepcopy(successor["release_ref"])
    _require(tuple(required.keys()) == REQUIRED_FIELDS, "corrected identity material is not exactly 17 fields")
    _require(len(required) == 17, "corrected identity material must contain exactly 17 top-level fields")
    return required


def issue(
    *,
    binding_schema: Mapping[str, Any],
    relation_authority: Mapping[str, Any],
    r6l_receipt: Mapping[str, Any],
    binding_registry_snapshot: Mapping[str, Any],
    quarantined_r6i_candidate: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    snapshot_ref = binding_registry_snapshot["snapshot_ref"]
    _require(snapshot_ref["content_hash"] == CURRENT_SNAPSHOT_HASH, "current binding snapshot hash mismatch")
    _require(semantic_hash(binding_registry_snapshot["identity_material"]) == CURRENT_SNAPSHOT_HASH,
             "current binding snapshot identity mismatch")
    sim = binding_registry_snapshot["identity_material"]
    _require(sim["active_positive_binding_count"] == 0 and sim["active_positive_bindings"] == [],
             "corrected issuance requires zero active positive bindings")
    old_ref = quarantined_r6i_candidate["binding_ref"]
    _require(old_ref["content_hash"] == QUARANTINED_R6I_HASH, "quarantined predecessor mismatch")

    material = build_corrected_identity_material(
        binding_schema=binding_schema,
        relation_authority=relation_authority,
        r6l_receipt=r6l_receipt,
    )
    digest = semantic_hash(material)
    _require(digest != QUARANTINED_R6I_HASH, "corrected identity must not reuse quarantined R6I hash")
    binding_ref = {
        "kind": "ReleaseRealizationBinding@1.0.0",
        "object_id": f"urn:rawlsing:prev3:p2r6j:release-realization-binding:sha256:{digest}",
        "content_hash": digest,
    }
    candidate = {
        "schema": "EE_P2R6J_CORRECTED_RUNTIME_BINDING_CANDIDATE@1.0.0",
        "status": "STRUCTURALLY_R5A_R6A_ALIGNED__INACTIVE__PRODUCTION_RUNTIME_POSITIVE_PROOF_REQUIRED",
        "activation": "FORBIDDEN_UNTIL_HQ_ADOPTION_AFTER_EXACT_R6A_PRODUCTION_RUNTIME_POSITIVE_PROOF",
        "candidate_ref": {
            "kind": "ReleaseRealizationBindingCandidate@1.0.0",
            "object_id": f"urn:rawlsing:prev3:p2r6j:release-realization-binding-candidate:sha256:{digest}",
            "content_hash": digest,
        },
        "binding_ref": copy.deepcopy(binding_ref),
        "identity_law": "SHA256_CANONICAL(identity_material)",
        "identity_material": material,
        "proof_envelope": {
            "current_zero_binding_snapshot_ref": copy.deepcopy(snapshot_ref),
            "quarantined_predecessor_candidate_ref": copy.deepcopy(old_ref),
            "adopted_r6l_return_head": R6L_RETURN_HEAD,
            "production_runtime_positive_proof": "REQUIRED_BEFORE_HQ_ADOPTION",
        },
    }
    active_record = {
        "schema": "RELEASE_REALIZATION_BINDING@1.0.0",
        "typed_state": "ACTIVE_POSITIVE",
        "binding_ref": copy.deepcopy(binding_ref),
        "identity_material": copy.deepcopy(material),
    }
    return candidate, active_record
