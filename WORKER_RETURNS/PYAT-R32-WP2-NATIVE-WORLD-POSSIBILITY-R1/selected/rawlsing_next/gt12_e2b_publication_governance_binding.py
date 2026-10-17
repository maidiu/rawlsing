"""Exact adopted current GT12 E2B V554/V557 publication-governance binding.

This module is a fixed repo-native current selection.  It creates no semantic
authority: every material and hash below is copied from the HQ adoption at
E2B_R3_PUBLICATION_GOVERNANCE_ADOPTION_R1/01_ADOPTION.json and revalidated
under the repository canonical semantic-hash law before use.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    V557DecisionState,
)

BUNDLE_ID = "GT12_E2B_R3_CURRENT_V554_V557_PUBLICATION_GOVERNANCE_BINDING"
BUNDLE_VERSION = "1.0.0"
BUNDLE_CONTENT_HASH = "f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14"
ADOPTION_CONTENT_HASH = "ff3c0db1ee346b176f240523f36048d88beb6216722988ea087040b4840cd492"

V554_RULE_HASH = "da431544e57ed4b418cd746be3f0a9aa486cd3c2fb2007a022005821b25e194b"
PUBLICATION_AUTHORITY_HASH = "1b2c1238139287e30acaa418e28967585a34a7fae9c937a9322b7c9e9a76322a"
V557_BINDING_HASH = "b071d9b34825b2c73fefa47cdef0ba23003d79cf5a2fa78cab802e02ee0cd6f4"

GOVERNED_USE_ID = "GT12_GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_F1_CONTEXT_PUBLICATION@1"
V554_RULE_ID = "GT12_V554_SIG004_ADMITTED_RELATION_CONTEXT_PUBLICATION_RULE"
V554_RULE_VERSION = "1.0.0"
PUBLICATION_AUTHORITY_ID = "GT12_RELATION_V554_TO_V557_F1_CONTEXT_PUBLICATION_AUTHORITY"
PUBLICATION_AUTHORITY_VERSION = "1.0.0"
V557_AUTHORITY_ID = "GT12_CAN003_V557_F1_CONTEXT_ONLY_CURRENT_BINDING"
V557_AUTHORITY_VERSION = "1.0.0"

RELATION_M1_CONTRACT = "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
RELATION_BASIS_KIND = "ADMITTED_FIELD_FORGE_RELATION"
SIG_004 = "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT"
TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"
FOCAL_PROPOSITION = "GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_COUNT_PROFILE_WITHIN_SCOPE"
DIRECT_ROUTE = "V554_TO_V557_DIRECT"
PUBLICATION_FAMILIES = ("F1",)
V557_STATE = V557DecisionState.ALLOW_CONTEXT_ONLY
V557_ALLOWED_USES = ("CONTEXT",)

_PERMISSION_TRANSLATION_REF = {
    "authority_id": "GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY",
    "authority_version": "1.0.0",
    "authority_hash": "d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c",
}

_V554_RULE_MATERIAL = {
    "schema": "GT12_E2B_R3_V554_SIG004_RULE@1.0.0",
    "rule_id": V554_RULE_ID,
    "rule_version": V554_RULE_VERSION,
    "jurisdiction": {
        "relation_m1_contract": RELATION_M1_CONTRACT,
        "basis_kind": RELATION_BASIS_KIND,
        "signature_id": SIG_004,
        "target_use": TARGET_USE,
        "focal_structural_proposition_ref": FOCAL_PROPOSITION,
        "conditions_exact": [],
        "direct_route": DIRECT_ROUTE,
        "publication_object_families_exact": ["F1"],
    },
    "semantic_derivation": {
        "creates_new_relation_semantics": False,
        "creates_new_empirical_semantics": False,
        "binds_existing_sig004_contract": True,
    },
    "forbidden": [
        "V553", "V555", "V556", "F2", "B1", "REVIEW", "ACTIVE_CAUSAL",
        "ACTOR_INFERENCE", "POSITIVE_V3_TRANSITION", "V2_AUTHORITY",
    ],
}

_V554_RULE_REF = {
    "id": V554_RULE_ID,
    "version": V554_RULE_VERSION,
    "hash": V554_RULE_HASH,
}

_PUBLICATION_AUTHORITY_MATERIAL = {
    "schema": "GT12_E2B_R3_V554_TO_V557_PUBLICATION_AUTHORITY@1.0.0",
    "authority_id": PUBLICATION_AUTHORITY_ID,
    "authority_version": PUBLICATION_AUTHORITY_VERSION,
    "producer": "V554",
    "publisher": "V557",
    "governed_use_id": GOVERNED_USE_ID,
    "rule_ref": dict(_V554_RULE_REF),
    "decision": "AUTHORIZED",
    "allowed_object_families": ["F1"],
    "jurisdiction": {
        "relation_m1_contract": RELATION_M1_CONTRACT,
        "basis_kind": RELATION_BASIS_KIND,
        "signature_id": SIG_004,
        "target_use": TARGET_USE,
        "focal_structural_proposition_ref": FOCAL_PROPOSITION,
        "conditions_exact": [],
        "direct_route": DIRECT_ROUTE,
        "inherited_downstream_use_exact": ["CONTEXT"],
    },
    "authority_exclusions": [
        "EMPIRICAL_MEANING", "FIELD_FORGE_PRODUCTION", "PREV3_ADMISSION",
        "NEW_PERMISSION_ATOMS", "REVIEW", "ACTIVE_CAUSAL", "V553", "V555",
        "V556", "F2_PUBLICATION", "B1_PUBLICATION", "ACTOR_INFERENCE",
        "POSITIVE_V3_TRANSITION", "V2_AUTHORITY",
    ],
}

_V557_BINDING_MATERIAL = {
    "schema": "GT12_E2B_R3_CAN003_V557_CURRENT_BINDING@1.0.0",
    "authority_id": V557_AUTHORITY_ID,
    "authority_version": V557_AUTHORITY_VERSION,
    "semantic_source": {
        "authority_id": "CAN-003",
        "authority_version": "CAN-003.v1",
        "contract_id": "CAN_003_V557_RUNTIME_USE",
        "accepted_artifact_path": (
            "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/"
            "schematics/release/W0_AUTHORITY_FOUNDATION/"
            "CAN_003_V557_RUNTIME_USE/AUTHORITY.json"
        ),
        "accepted_git_blob": "64fb18f01a1caa69fd3553dc62b056c0efe1ff47",
        "classification": "CANONICALIZED_EXISTING_AUTHORITY",
    },
    "narrowed_jurisdiction": {
        "producer_family": "V554",
        "semantic_class": "F1",
        "source_stage": "M1_RELATION_V554_TO_V557",
        "governed_use_id": GOVERNED_USE_ID,
        "decision_state": "ALLOW_CONTEXT_ONLY",
        "v557_allowed_uses_exact": ["CONTEXT"],
        "exception_state": "NO_EXCEPTION_STATE",
    },
    "inheritance_law": {
        "creates_new_v557_semantics": False,
        "only_current_selects_and_narrows_can003": True,
        "producer_permission_created_here": False,
    },
    "forbidden": [
        "REVIEW", "ACTIVE_CAUSAL", "V553", "V555", "V556",
        "ACTOR_INFERENCE", "POSITIVE_V3_TRANSITION", "V2_AUTHORITY",
        "FUZZY_CURRENT_SELECTION",
    ],
}

_BUNDLE_PUBLICATION_AUTHORITY = {
    **_PUBLICATION_AUTHORITY_MATERIAL,
    "authority_hash": PUBLICATION_AUTHORITY_HASH,
}

_BUNDLE_MATERIAL = {
    "schema": "GT12_E2B_R3_MINIMAL_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0",
    "bundle_id": BUNDLE_ID,
    "bundle_version": BUNDLE_VERSION,
    "jurisdiction": {
        "program": "GT1_GT2_WAVE1_FROZEN_CANARY",
        "relation_m1_contract": RELATION_M1_CONTRACT,
        "basis_kind": RELATION_BASIS_KIND,
        "signature_id": SIG_004,
        "target_use": TARGET_USE,
        "focal_structural_proposition_ref": FOCAL_PROPOSITION,
        "producer_family": "V554",
        "publication_target": "V557",
        "conditions_exact": [],
        "publication_object_families_exact": ["F1"],
        "required_v557_state": "ALLOW_CONTEXT_ONLY",
        "required_v557_uses_exact": ["CONTEXT"],
    },
    "publication_authority": _BUNDLE_PUBLICATION_AUTHORITY,
    "v557_authority_ref": {
        "authority_id": V557_AUTHORITY_ID,
        "authority_version": V557_AUTHORITY_VERSION,
        "authority_hash": V557_BINDING_HASH,
    },
    "external_prerequisites": {
        "permission_translation_authority": dict(_PERMISSION_TRANSLATION_REF),
        "producer_allowed_uses_exact": ["CONTEXT"],
        "v557_allowed_uses_exact": ["CONTEXT"],
        "v558_requested_uses_exact": ["CONTEXT"],
    },
    "derived_api_projection": {
        "governed_use_id": "publication_authority.governed_use_id",
        "v554_rule_ref": "publication_authority.rule_ref",
        "publication_authority": "publication_authority",
        "v557_authority_ref": "v557_authority_ref",
    },
    "current_selection": {
        "caller_selectable": False,
        "fuzzy_selection_forbidden": True,
    },
}

_ADOPTION_MATERIAL = {
    "schema": "GT12_E2B_R3_PUBLICATION_GOVERNANCE_ADOPTION@1.0.0",
    "decision": "ADOPTED_CURRENT",
    "accepted_central_parent": "734a7af889ceec822f049652a706ed15dc373c3b",
    "bundle_ref": {
        "id": BUNDLE_ID,
        "version": BUNDLE_VERSION,
        "content_hash": BUNDLE_CONTENT_HASH,
    },
    "evidence": {
        "h1_terminal_sha": "fa03c40f827a4e9636f9360e2ec5791c71a5d433",
        "h1_terminal": "PASS__GT12_E2B_R3_NO_EXISTING_COMPETENT_PUBLICATION_AUTHORITY_BUNDLE__EXACT_GAP_PROVED",
        "h2_terminal_sha": "e5ff4d7669d12c5c58c57258b0045e27ba1c8eb3",
        "h2_terminal": "PASS__GT12_E2B_R3_MINIMAL_PUBLICATION_AUTHORITY_BUNDLE_CONTRACT_DEFINED__NO_ADOPTION",
    },
    "authority_ceiling": {
        "publication_object_families_exact": ["F1"],
        "v557_state": "ALLOW_CONTEXT_ONLY",
        "v557_uses_exact": ["CONTEXT"],
        "v558_requested_uses_exact": ["CONTEXT"],
        "v3_positive_authority": False,
        "actor_authority": False,
        "v2_authority": False,
    },
}


class GT12E2BBindingError(ValueError):
    """The adopted current publication/governance binding failed closed."""


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(_deep_freeze(v) for v in value)
    return value


def _require_hash(label: str, material: Mapping[str, Any], expected: str) -> None:
    actual = semantic_hash(material)
    if actual != expected:
        raise GT12E2BBindingError(
            f"{label} semantic hash drift: expected {expected}, got {actual}"
        )


def _validate_materials(
    *,
    v554_rule_material: Mapping[str, Any] = _V554_RULE_MATERIAL,
    publication_authority_material: Mapping[str, Any] = _PUBLICATION_AUTHORITY_MATERIAL,
    v557_binding_material: Mapping[str, Any] = _V557_BINDING_MATERIAL,
    bundle_material: Mapping[str, Any] = _BUNDLE_MATERIAL,
    adoption_material: Mapping[str, Any] = _ADOPTION_MATERIAL,
) -> None:
    _require_hash("V554 rule", v554_rule_material, V554_RULE_HASH)
    _require_hash(
        "publication authority",
        publication_authority_material,
        PUBLICATION_AUTHORITY_HASH,
    )
    _require_hash("V557 current binding", v557_binding_material, V557_BINDING_HASH)
    _require_hash("immutable bundle", bundle_material, BUNDLE_CONTENT_HASH)
    _require_hash("adoption", adoption_material, ADOPTION_CONTENT_HASH)

    publication = bundle_material.get("publication_authority")
    if not isinstance(publication, Mapping):
        raise GT12E2BBindingError("bundle publication authority missing")
    if publication.get("authority_hash") != PUBLICATION_AUTHORITY_HASH:
        raise GT12E2BBindingError("publication authority hash projection drift")
    if publication.get("governed_use_id") != GOVERNED_USE_ID:
        raise GT12E2BBindingError("governed use drift")
    if publication.get("rule_ref") != _V554_RULE_REF:
        raise GT12E2BBindingError("V554 rule ref projection drift")
    if publication.get("producer") != "V554" or publication.get("publisher") != "V557":
        raise GT12E2BBindingError("publication route drift")
    if publication.get("decision") != "AUTHORIZED":
        raise GT12E2BBindingError("publication decision drift")
    if tuple(publication.get("allowed_object_families", ())) != PUBLICATION_FAMILIES:
        raise GT12E2BBindingError("publication families must remain exact F1 singleton")

    rule_jurisdiction = v554_rule_material.get("jurisdiction")
    if not isinstance(rule_jurisdiction, Mapping):
        raise GT12E2BBindingError("V554 rule jurisdiction missing")
    if tuple(rule_jurisdiction.get("conditions_exact", ())) != ():
        raise GT12E2BBindingError("adopted publication binding requires empty conditions")
    if tuple(rule_jurisdiction.get("publication_object_families_exact", ())) != PUBLICATION_FAMILIES:
        raise GT12E2BBindingError("V554 rule publication family drift")
    if (
        rule_jurisdiction.get("relation_m1_contract") != RELATION_M1_CONTRACT
        or rule_jurisdiction.get("basis_kind") != RELATION_BASIS_KIND
        or rule_jurisdiction.get("signature_id") != SIG_004
        or rule_jurisdiction.get("target_use") != TARGET_USE
        or rule_jurisdiction.get("focal_structural_proposition_ref") != FOCAL_PROPOSITION
        or rule_jurisdiction.get("direct_route") != DIRECT_ROUTE
    ):
        raise GT12E2BBindingError("V554 rule jurisdiction drift")

    v557 = v557_binding_material.get("narrowed_jurisdiction")
    if not isinstance(v557, Mapping):
        raise GT12E2BBindingError("V557 narrowed jurisdiction missing")
    if (
        v557.get("producer_family") != "V554"
        or v557.get("semantic_class") != "F1"
        or v557.get("source_stage") != "M1_RELATION_V554_TO_V557"
        or v557.get("governed_use_id") != GOVERNED_USE_ID
        or v557.get("decision_state") != "ALLOW_CONTEXT_ONLY"
        or tuple(v557.get("v557_allowed_uses_exact", ())) != V557_ALLOWED_USES
        or v557.get("exception_state") != "NO_EXCEPTION_STATE"
    ):
        raise GT12E2BBindingError("V557 current binding jurisdiction drift")

    forbidden = {"REVIEW", "ACTIVE_CAUSAL", "V553", "V555", "V556"}
    if forbidden & set(V557_ALLOWED_USES):
        raise GT12E2BBindingError("forbidden permission/lane entered V557 current uses")


@dataclass(frozen=True)
class CurrentPublicationGovernanceBinding:
    bundle_id: str
    bundle_version: str
    bundle_content_hash: str
    adoption_content_hash: str
    publication_authority: Mapping[str, Any]
    v557_authority_ref: M4AuthorityRef

    @property
    def governed_use_id(self) -> str:
        return str(self.publication_authority["governed_use_id"])

    @property
    def v554_rule_ref(self) -> Mapping[str, Any]:
        rule = self.publication_authority["rule_ref"]
        if not isinstance(rule, Mapping):
            raise GT12E2BBindingError("current publication rule projection malformed")
        return rule


def load_current_gt12_e2b_publication_governance_binding() -> CurrentPublicationGovernanceBinding:
    """Return the one adopted current bundle.  No caller-selectable inputs."""
    _validate_materials()
    return CurrentPublicationGovernanceBinding(
        bundle_id=BUNDLE_ID,
        bundle_version=BUNDLE_VERSION,
        bundle_content_hash=BUNDLE_CONTENT_HASH,
        adoption_content_hash=ADOPTION_CONTENT_HASH,
        publication_authority=_deep_freeze(_BUNDLE_PUBLICATION_AUTHORITY),
        v557_authority_ref=M4AuthorityRef(
            V557_AUTHORITY_ID,
            V557_AUTHORITY_VERSION,
            V557_BINDING_HASH,
        ),
    )


__all__ = [
    "BUNDLE_ID",
    "BUNDLE_VERSION",
    "BUNDLE_CONTENT_HASH",
    "ADOPTION_CONTENT_HASH",
    "V554_RULE_HASH",
    "PUBLICATION_AUTHORITY_HASH",
    "V557_BINDING_HASH",
    "PUBLICATION_FAMILIES",
    "V557_STATE",
    "V557_ALLOWED_USES",
    "GT12E2BBindingError",
    "CurrentPublicationGovernanceBinding",
    "load_current_gt12_e2b_publication_governance_binding",
]
