from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from typing import Any


TOPOLOGY_CONTRACT_VERSION = "P3_COMPONENT_TOPOLOGY_CONTRACT_V1"
PAIR_PROJECTION_SEMANTIC_VERSION = "P3_PAIR_PROJECTION_SEMANTIC_FINGERPRINT_V1"
COMPONENT_SEMANTIC_VERSION = "P3_COMPONENT_SEMANTIC_FINGERPRINT_V1"
FAMILY_SEMANTIC_VERSION = "P3_FAMILY_SEMANTIC_ORIGIN_V1_RELEASE_NEUTRAL"
CANDIDATE_EVIDENCE_VERSION = "P3_CANDIDATE_COMPLETE_EVIDENCE_V1"


def _normalize(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value, "f").rstrip("0").rstrip(".") or "0"
    if isinstance(value, float):
        return f"{value:.12g}"
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    return value


def canonical_text(value: Any) -> str:
    return json.dumps(_normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()


def projection_semantic_payload(pair_fact_id: str, left_subject_id: str, right_subject_id: str, projection_basis: str) -> dict:
    return {
        "serialization": PAIR_PROJECTION_SEMANTIC_VERSION,
        "pair_fact_id": pair_fact_id,
        "left_subject_id": left_subject_id,
        "right_subject_id": right_subject_id,
        "projection_basis": projection_basis,
    }


def component_semantic_payload(component_type: str, subject_ids: list[str], projection_semantic_fingerprints: list[str]) -> dict:
    return {
        "serialization": COMPONENT_SEMANTIC_VERSION,
        "component_type": component_type,
        "subjects": sorted(subject_ids),
        "projection_semantic_fingerprints": sorted(projection_semantic_fingerprints),
        "topology_contract_version": TOPOLOGY_CONTRACT_VERSION,
    }


def family_semantic_payload(origin: str, subject_ids: list[str], component_semantic_fingerprints: list[str], attachment_projection_semantic_fingerprints: list[str]) -> dict:
    return {
        "serialization": FAMILY_SEMANTIC_VERSION,
        "origin": origin,
        "members": sorted(subject_ids),
        "component_semantic_fingerprints": sorted(component_semantic_fingerprints),
        "attachment_projection_semantic_fingerprints": sorted(attachment_projection_semantic_fingerprints),
    }


def packet_evidence_surface(packet: dict) -> dict:
    c = packet["candidate_family"]
    return {
        "serialization_contract": CANDIDATE_EVIDENCE_VERSION,
        "candidate_family": {k: c[k] for k in sorted(c) if k not in {"evidence_bundle_hash", "ranking"}},
        "ranking": c.get("ranking", {}),
        "origin_components": packet.get("origin_components", []),
        "members_by_source": packet.get("members_by_source", {}),
        "proposition_signature_matrix": packet.get("proposition_signature_matrix", []),
        "response_contract_matrix": packet.get("response_contract_matrix", []),
        "pair_projections": packet.get("pair_projections", []),
        "internal_pair_matrix": packet.get("internal_pair_matrix", []),
        "hard_collisions": packet.get("hard_collisions", []),
        "typed_collisions": packet.get("typed_collisions", []),
        "typed_unresolved_boundaries": packet.get("typed_unresolved_boundaries", []),
        "typed_redirect_boundaries": packet.get("typed_redirect_boundaries", []),
        "typed_coordinate_constraints": packet.get("typed_coordinate_constraints", []),
        "unresolved_pairs": packet.get("unresolved_pairs", []),
        "unruled_pairs": packet.get("unruled_pairs", []),
        "closure_obligations": packet.get("closure_obligations", []),
        "explicit_exclusions": packet.get("explicit_exclusions", []),
        "exact_evidence_links": packet.get("exact_evidence_links", []),
        "schema_version": "candidate_packet.schema.json",
        "identity_contract_version": FAMILY_SEMANTIC_VERSION,
        "topology_contract_version": TOPOLOGY_CONTRACT_VERSION,
    }


def packet_evidence_hash(packet: dict) -> str:
    return canonical_hash(packet_evidence_surface(packet))
