"""Build the explicit TEST_ONLY technical fixture used by the preflight tests."""
from __future__ import annotations

import copy
from typing import Any

from native_input_preflight import (
    NATIVE_GRADE,
    PRACTICE_OBJECT,
    SCHEMA,
    SELF_KNOWLEDGE,
    TEST_ONLY_GRADE,
    digest,
)

A = "TEST_ONLY_ACTOR_A"
B = "TEST_ONLY_ACTOR_B"


def _artifact(content: dict[str, Any], owner: str) -> dict[str, Any]:
    return {
        "content": copy.deepcopy(content),
        "content_hash": digest(content),
        "grade": TEST_ONLY_GRADE,
        "owner_ref": owner,
    }


def build_bundle(*, mode: str = "TEST_ONLY_TECHNICAL", grade: str = TEST_ONLY_GRADE) -> dict[str, Any]:
    """Return one structurally complete technical-only A/B pathway."""
    source_grant = {
        "kind": "SOURCE_GRANT",
        "grade": grade,
        "source_id": "TEST_ONLY_SOURCE_ALPHA",
        "edition": "TEST_ONLY_EDITION_1",
        "source_content_hash": digest({"source": "TEST_ONLY_SOURCE_ALPHA", "edition": 1}),
        "owner_ref": "TEST_ONLY_SOURCE_OWNER",
        "host_ref": "TEST_ONLY_SOURCE_HOST",
        "purpose_ref": "TEST_ONLY_SOURCE_PURPOSE",
        "permission_ref": "TEST_ONLY_SOURCE_PERMISSION",
        "effective_from": 10,
        "expires_at": 1200,
        "revoked": False,
    }
    a_ep1 = {
        "kind": "ACTOR_ENACTED",
        "subject": A,
        "operation": PRACTICE_OBJECT,
        "occurred": True,
        "time": 100,
        "owner_ref": "TEST_ONLY_OBSERVER_1",
        "independent": True,
    }
    a_ep2 = {
        "kind": "ACTOR_ENACTED",
        "subject": A,
        "operation": PRACTICE_OBJECT,
        "occurred": True,
        "time": 200,
        "owner_ref": "TEST_ONLY_OBSERVER_2",
        "independent": True,
    }
    a_contrary = {
        "kind": "CONTRARY_ACTION",
        "subject": A,
        "operation": "solo_material_inspection",
        "occurred": True,
        "time": 250,
        "owner_ref": "TEST_ONLY_OBSERVER_3",
        "independent": True,
    }
    a_nonperformance = {
        "kind": "ACTOR_NONPERFORMANCE",
        "subject": A,
        "operation": PRACTICE_OBJECT,
        "occurred": False,
        "time": 300,
        "owner_ref": "TEST_ONLY_OBSERVER_3",
        "independent": True,
        "matched_opportunity_ref": "TEST_ONLY_ADP010_OPPORTUNITY",
    }
    b_offer = {
        "kind": "OTHER_OFFER",
        "subject": B,
        "operation": PRACTICE_OBJECT,
        "occurred": True,
        "time": 350,
        "owner_ref": "TEST_ONLY_OBSERVER_4",
        "independent": True,
    }
    b_refusal = {
        "kind": "OTHER_REFUSAL",
        "subject": B,
        "operation": "extra_voluntary_task",
        "occurred": True,
        "time": 360,
        "owner_ref": "TEST_ONLY_OBSERVER_4",
        "independent": True,
    }
    opportunity = {
        "kind": "ADP010_OPPORTUNITY",
        "subject": A,
        "state": "OPPORTUNITY",
        "parent": "AVAILABLE",
        "time": 400,
        "owner_ref": "TEST_ONLY_ADP010_OWNER",
        "world_ref": "TEST_ONLY_WORLD",
    }
    contact = {
        "kind": "CONTACT_OCCURRENCE",
        "participants": [A, B],
        "time": 500,
        "owner_ref": "TEST_ONLY_CONTACT_OWNER",
        "co_location_only": False,
    }
    encounter = {
        "kind": "ADP010_ENCOUNTER",
        "subject": A,
        "state": "ENCOUNTER",
        "parent_ref": "TEST_ONLY_ADP010_OPPORTUNITY",
        "contact_ref": "TEST_ONLY_ADP010_CONTACT",
        "time": 500,
        "owner_ref": "TEST_ONLY_ADP010_OWNER",
    }
    e1 = {
        "kind": "ADP019_ADMISSION",
        "admission_status": "ADMIT",
        "receipt_id": "TEST_ONLY_ADP019_RECEIPT",
        "event_id": "TEST_ONLY_E1_EVENT",
        "event_hash": digest({"event": "TEST_ONLY_E1_EVENT", "actor": A, "other": B}),
        "subject": A,
        "parent_ref": "TEST_ONLY_ADP010_ENCOUNTER",
        "time": 600,
        "source_owner_ref": "TEST_ONLY_ADP019_OWNER",
        "c8_ref": "TEST_ONLY_C8_PROTECTED",
    }
    c8 = {
        "kind": "C8_PROTECTED_WRITER",
        "writer_ref": "TEST_ONLY_C8_WRITER",
        "key_custody": "TEST_ONLY_EXTERNAL_KEY_FILE",
        "protected_writer": True,
        "anchor_ref": "TEST_ONLY_C8_ANCHOR",
        "monotonic_anchor": True,
        "proof_verified": True,
    }
    rule_a = {
        "kind": "CAN008_RULE_A",
        "authority_id": "CAN008_R2",
        "rule_id": "TEST_ONLY_CAN008_RULE_A",
        "version": "1",
        "semantic_object": PRACTICE_OBJECT,
        "subject_refs": [A],
        "readset_classes": ["ACTOR_HISTORY", "ADP010_ENCOUNTER", "ADP019_E1"],
        "issuer_ref": "TEST_ONLY_CAN008_ISSUER",
        "source_owner_ref": "TEST_ONLY_CAN008_OWNER",
        "effective_from": 550,
        "expires_at": 1200,
        "revoked": False,
        "rule_body": {"responses": ["undertake", "decline", "valid_empty"]},
    }
    rule_t = {
        "kind": "CAN011_RULE_T",
        "authority_id": "CAN011",
        "rule_id": "TEST_ONLY_CAN011_RULE_T",
        "version": "1",
        "target_kind": "V3MS_PRACTICE",
        "semantic_object": PRACTICE_OBJECT,
        "response_rule_ref": "TEST_ONLY_CAN008_RULE_A",
        "issuer_ref": "TEST_ONLY_CAN011_ISSUER",
        "source_owner_ref": "TEST_ONLY_CAN011_OWNER",
        "effective_from": 600,
        "expires_at": 1200,
        "revoked": False,
        "rule_body": {"op": "CREATE", "target": PRACTICE_OBJECT},
    }
    grant = {
        "kind": "CAN011_GRANT",
        "grant_id": "TEST_ONLY_CAN011_GRANT",
        "issuer_ref": "TEST_ONLY_CAN011_GRANT_ISSUER",
        "source_owner_ref": "TEST_ONLY_CAN011_GRANT_OWNER",
        "actor_id": A,
        "rule_a_ref": "TEST_ONLY_CAN008_RULE_A",
        "rule_t_ref": "TEST_ONLY_CAN011_RULE_T",
        "response_ref": "TEST_ONLY_CAN008_RULE_A",
        "before_state_hash": digest({"before": "TEST_ONLY_PRACTICE_ABSENT"}),
        "decision": "CREATE",
        "effective_from": 600,
        "expires_at": 1200,
        "revoked": False,
        "readset_refs": ["TEST_ONLY_CAN008_RULE_A", "TEST_ONLY_CAN011_RULE_T"],
    }
    target_state_hash = digest(
        {
            "target_id": "TEST_ONLY_TARGET",
            "e1_ref": "TEST_ONLY_ADP019_E1",
            "rule_a_ref": "TEST_ONLY_CAN008_RULE_A",
            "rule_t_ref": "TEST_ONLY_CAN011_RULE_T",
            "grant_ref": "TEST_ONLY_CAN011_GRANT",
            "commit_time": 700,
        }
    )
    target = {
        "kind": "TARGET_COMMIT",
        "target_id": "TEST_ONLY_TARGET",
        "state_hash": target_state_hash,
        "commit_time": 700,
        "committed": True,
        "e1_ref": "TEST_ONLY_ADP019_E1",
        "rule_a_ref": "TEST_ONLY_CAN008_RULE_A",
        "rule_t_ref": "TEST_ONLY_CAN011_RULE_T",
        "grant_ref": "TEST_ONLY_CAN011_GRANT",
        "readset_refs": [
            "TEST_ONLY_ADP019_E1",
            "TEST_ONLY_CAN008_RULE_A",
            "TEST_ONLY_CAN011_RULE_T",
            "TEST_ONLY_CAN011_GRANT",
        ],
    }
    e2 = {
        "kind": "E2_PERFORMED",
        "receipt_id": "TEST_ONLY_E2_RECEIPT",
        "actor_id": A,
        "act": "inspect_with_tool",
        "performed": True,
        "actuator_ref": "TEST_ONLY_TOOL",
        "occurrence_ref": "TEST_ONLY_E2_OCCURRENCE",
        "action_time": 800,
        "consumed_state_hash": target_state_hash,
        "source_owner_ref": "TEST_ONLY_E2_OWNER",
    }

    artifacts = {
        "TEST_ONLY_SOURCE_GRANT": _artifact(source_grant, "TEST_ONLY_SOURCE_OWNER"),
        "TEST_ONLY_A_EP1": _artifact(a_ep1, "TEST_ONLY_OBSERVER_1"),
        "TEST_ONLY_A_EP2": _artifact(a_ep2, "TEST_ONLY_OBSERVER_2"),
        "TEST_ONLY_A_CONTRARY": _artifact(a_contrary, "TEST_ONLY_OBSERVER_3"),
        "TEST_ONLY_A_NONPERFORMANCE": _artifact(a_nonperformance, "TEST_ONLY_OBSERVER_3"),
        "TEST_ONLY_B_OFFER": _artifact(b_offer, "TEST_ONLY_OBSERVER_4"),
        "TEST_ONLY_B_REFUSAL": _artifact(b_refusal, "TEST_ONLY_OBSERVER_4"),
        "TEST_ONLY_ADP010_OPPORTUNITY": _artifact(opportunity, "TEST_ONLY_ADP010_OWNER"),
        "TEST_ONLY_ADP010_CONTACT": _artifact(contact, "TEST_ONLY_CONTACT_OWNER"),
        "TEST_ONLY_ADP010_ENCOUNTER": _artifact(encounter, "TEST_ONLY_ADP010_OWNER"),
        "TEST_ONLY_ADP019_E1": _artifact(e1, "TEST_ONLY_ADP019_OWNER"),
        "TEST_ONLY_C8_PROTECTED": _artifact(c8, "TEST_ONLY_C8_OWNER"),
        "TEST_ONLY_CAN008_RULE_A": _artifact(rule_a, "TEST_ONLY_CAN008_OWNER"),
        "TEST_ONLY_CAN011_RULE_T": _artifact(rule_t, "TEST_ONLY_CAN011_OWNER"),
        "TEST_ONLY_CAN011_GRANT": _artifact(grant, "TEST_ONLY_CAN011_GRANT_OWNER"),
        "TEST_ONLY_TARGET": _artifact(target, "TEST_ONLY_TARGET_OWNER"),
        "TEST_ONLY_E2": _artifact(e2, "TEST_ONLY_E2_OWNER"),
    }
    declared = sorted(artifacts)
    return {
        "schema": SCHEMA,
        "claim_id": "TEST_ONLY_R27S_COORDINATED_MATERIAL_INSPECTION",
        "mode": mode,
        "grade": grade,
        "as_of": 1000,
        "production": {
            "native_issued": False,
            "grant_written": False,
            "production_registry_entries": 0,
        },
        "source_grant_ref": "TEST_ONLY_SOURCE_GRANT",
        "actor_a": {
            "actor_id": A,
            "self_knowledge": SELF_KNOWLEDGE,
            "demographic_or_role_derived": [],
            "history_refs": ["TEST_ONLY_A_EP1", "TEST_ONLY_A_EP2"],
            "contrary_refs": ["TEST_ONLY_A_CONTRARY"],
            "nonperformance_refs": ["TEST_ONLY_A_NONPERFORMANCE"],
        },
        "actor_b": {
            "actor_id": B,
            "performed_refs": ["TEST_ONLY_B_OFFER", "TEST_ONLY_B_REFUSAL"],
        },
        "encounter": {
            "opportunity_ref": "TEST_ONLY_ADP010_OPPORTUNITY",
            "contact_ref": "TEST_ONLY_ADP010_CONTACT",
            "encounter_ref": "TEST_ONLY_ADP010_ENCOUNTER",
        },
        "e1_ref": "TEST_ONLY_ADP019_E1",
        "c8_ref": "TEST_ONLY_C8_PROTECTED",
        "rule_a_ref": "TEST_ONLY_CAN008_RULE_A",
        "rule_t_ref": "TEST_ONLY_CAN011_RULE_T",
        "grant_ref": "TEST_ONLY_CAN011_GRANT",
        "target_ref": "TEST_ONLY_TARGET",
        "e2_ref": "TEST_ONLY_E2",
        "source_artifacts": artifacts,
        "readset": {
            "declared_refs": declared,
            "content_hashes": {
                ref: wrapper["content_hash"] for ref, wrapper in artifacts.items()
            },
        },
    }


def native_grade_fixture() -> dict[str, Any]:
    """Return the same bundle relabelled native without real signatures."""
    bundle = build_bundle(mode="NATIVE_CANDIDATE", grade=NATIVE_GRADE)
    for wrapper in bundle["source_artifacts"].values():
        wrapper["grade"] = NATIVE_GRADE
    for content in (wrapper["content"] for wrapper in bundle["source_artifacts"].values()):
        if "grade" in content:
            content["grade"] = NATIVE_GRADE
        if "key_custody" in content:
            content["key_custody"] = "TEST_ONLY_EXTERNAL_KEY_FILE"
    for wrapper in bundle["source_artifacts"].values():
        wrapper["content_hash"] = digest(wrapper["content"])
    bundle["readset"]["content_hashes"] = {
        ref: wrapper["content_hash"] for ref, wrapper in bundle["source_artifacts"].items()
    }
    return bundle
