from __future__ import annotations

from dataclasses import asdict
import json
import warnings

from rawlsing_next.gt12_e2b_publication_governance_binding import (
    BUNDLE_CONTENT_HASH,
    V557_BINDING_HASH,
    load_current_gt12_e2b_publication_governance_binding,
)
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_PRODUCER_ALLOWED_USES,
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import (
    ContextQueryItem,
    V557DecisionState,
    make_context_query,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact
from rawlsing_next.tests import gt12_e2b_actual_object_consumer_harness as harness
from rawlsing_next.v3_psepf_zero_positive_guard import GuardOutcome


def _m1_evidence(result):
    evaluation = result.m1_evaluation
    material = {
        "contract_id": evaluation.contract_id,
        "decision_state": evaluation.decision_state.value,
        "reason": evaluation.reason,
        "governed_use_id": evaluation.governed_use_id,
        "required_basis_kind": evaluation.required_basis_kind,
        "support_count": evaluation.support_count,
        "canonical_basis_semantic_id": evaluation.canonical_basis_semantic_id,
        "f1": evaluation.f1,
        "f2": evaluation.f2,
        "b1": evaluation.b1,
        "direct_v557_handoff": evaluation.direct_v557_handoff,
        "rejected_or_reference_only_basis_refs": evaluation.rejected_or_reference_only_basis_refs,
    }
    return material, semantic_hash(material)


def _v3_evidence(decision):
    pre = asdict(decision.pre_state_fingerprint) if decision.pre_state_fingerprint else None
    post = asdict(decision.post_guard_state_fingerprint) if decision.post_guard_state_fingerprint else None
    material = {
        "guard_id": decision.guard_id,
        "guard_version": decision.guard_version,
        "outcome": decision.outcome.value,
        "reason": decision.reason.value,
        "actor_id": decision.actor_id,
        "source_class": decision.source_class,
        "transition_surface_id": decision.transition_surface_id,
        "operation_class": decision.operation_class,
        "delegated_owner_rule_id": decision.delegated_owner_rule_id,
        "actor_state_effect": decision.actor_state_effect,
        "causal_ledger_appends": decision.causal_ledger_appends,
        "causal_cursor_delta": decision.causal_cursor_delta,
        "rng_mutations": decision.rng_mutations,
        "scheduler_mutations": decision.scheduler_mutations,
        "pre_state_fingerprint": pre,
        "post_guard_state_fingerprint": post,
    }
    return material, semantic_hash(material)


def test_execute_real_current_e2b_once_and_emit_identity_bearing_evidence():
    query, fact = load_current_gt2_query_fact()
    harness.require_current_r1c_actual_objects(query, fact)
    binding = load_current_gt12_e2b_publication_governance_binding()

    result = harness.run_current_r1c_e2b_actual_objects(query, fact)

    assert result.relation.typed_state == "SUPPORTED"
    assert result.relation.producer_state_blocking is False
    assert result.relation.producer_fact_ref == fact.ref
    assert result.relation.producer_query_ref == query.ref
    assert result.relation.producer_replay_ref == exact_ref(fact.replay_ref, "fact.replay_ref")
    assert result.relation.producer_permission_ceiling == ("STRUCTURAL_MEDIATION_INPUT",)
    assert result.relation.relation_permission_ceiling == ("STRUCTURAL_MEDIATION_INPUT",)

    assert result.admission.decision.value == "ADMITTED"
    assert result.admission.target_use_permissions == ("STRUCTURAL_MEDIATION_INPUT",)

    assert result.m1_evaluation.decision_state.value == "ELIGIBLE"
    assert result.m1_evaluation.required_basis_kind == "ADMITTED_FIELD_FORGE_RELATION"
    assert result.m1_evaluation.f1 is not None
    assert result.m1_evaluation.f2 == ()
    assert result.m1_evaluation.b1 is not None
    assert result.m1_evaluation.direct_v557_handoff["route"] == "V554_TO_V557_DIRECT"
    assert tuple(
        item["family"] for item in result.m1_evaluation.direct_v557_handoff["object_refs"]
    ) == ("F1",)

    terminal = result.v558_terminal
    assert len(terminal.publication.entries) == 1
    assert len(terminal.repository.entries) == 1
    publication_entry = terminal.publication.entries[0]
    repository_entry = terminal.repository.entries[0]
    assert publication_entry.obj.semantic_class == "F1"
    assert publication_entry.obj.producer_family == "V554"
    assert publication_entry.obj.producer_allowed_uses == ADOPTED_PRODUCER_ALLOWED_USES
    assert repository_entry.obj.ref == publication_entry.obj.ref
    assert repository_entry.governance.ref == publication_entry.governance.ref
    assert publication_entry.governance.decision_state is V557DecisionState.ALLOW_CONTEXT_ONLY
    assert publication_entry.governance.v557_allowed_uses == ADOPTED_V557_ALLOWED_USES
    assert publication_entry.governance.authority_ref == binding.v557_authority_ref
    assert publication_entry.governance.authority_ref.authority_hash == V557_BINDING_HASH

    v558_query = make_context_query(
        tuple(
            ContextQueryItem(key, ADOPTED_V558_REQUESTED_USES)
            for key in terminal.resolution_keys
        )
    )
    assert terminal.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert terminal.resolution.receipt.unresolved_keys == ()
    assert len(terminal.resolution.resolved_entries) == 1
    resolved = terminal.resolution.resolved_entries[0]
    assert resolved.canonical_producer_family == "V554"
    assert resolved.producer_object_ref == publication_entry.obj.ref
    assert resolved.resolver_allowed_uses == ADOPTED_V558_REQUESTED_USES

    decision = result.v3_decision
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.zero_effect is True
    assert decision.actor_state_effect == "ZERO"
    assert decision.causal_ledger_appends == 0
    assert decision.causal_cursor_delta == 0
    assert decision.rng_mutations == 0
    assert decision.scheduler_mutations == 0
    assert decision.pre_state_fingerprint == decision.post_guard_state_fingerprint

    m1_material, m1_hash = _m1_evidence(result)
    v3_material, v3_hash = _v3_evidence(decision)

    evidence = {
        "schema": "GT12_E2B_R3_REAL_RUNTIME_EVIDENCE@1.0.0",
        "actual_input": {
            "predicate": exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref").content_hash,
            "query": query.content_hash,
            "fact": fact.content_hash,
            "replay": exact_ref(fact.replay_ref, "fact.replay_ref").content_hash,
            "state": fact.typed_state,
            "denominator": fact.raw_denominator_support,
            "target_order": [
                exact_ref(ref, "query.target_refs").object_id for ref in query.target_refs
            ],
        },
        "adopted_publication_governance_bundle_hash": BUNDLE_CONTENT_HASH,
        "field_forge_relation_ref": result.relation.ref.as_dict(),
        "prev3_admission_ref": result.admission.ref.as_dict(),
        "prev3_admission_decision": result.admission.decision.value,
        "prev3_target_use_permissions": list(result.admission.target_use_permissions),
        "m1_evaluation": {
            "evidence_hash": m1_hash,
            "contract_id": m1_material["contract_id"],
            "decision_state": m1_material["decision_state"],
            "governed_use_id": m1_material["governed_use_id"],
            "required_basis_kind": m1_material["required_basis_kind"],
            "canonical_basis_semantic_id": m1_material["canonical_basis_semantic_id"],
            "direct_v557_handoff": m1_material["direct_v557_handoff"],
        },
        "f1_publication_roots": [
            entry.obj.ref.as_dict() for entry in terminal.publication.entries
        ],
        "v557_governance_records": [
            {
                "ref": entry.governance.ref.as_dict(),
                "authority_ref": entry.governance.authority_ref.as_dict(),
                "decision_state": entry.governance.decision_state.value,
                "producer_allowed_uses": list(entry.governance.producer_allowed_uses),
                "v557_allowed_uses": list(entry.governance.v557_allowed_uses),
            }
            for entry in terminal.publication.entries
        ],
        "v557_publication_bundle_ref": terminal.publication.ref.as_dict(),
        "v558_repository_ref": terminal.repository.ref.as_dict(),
        "v558_query": {
            "kind": "V558_CONTEXT_QUERY",
            "object_id": v558_query.query_id,
            "content_hash": v558_query.query_hash,
            "requested_uses": [
                list(item.requested_uses) for item in v558_query.items
            ],
        },
        "v558_resolution_receipt_ref": terminal.resolution.receipt.ref.as_dict(),
        "v558_resolution_state": terminal.resolution.receipt.result_state,
        "v558_resolved_entries": [
            {
                "producer_family": item.canonical_producer_family,
                "producer_object_ref": item.producer_object_ref.as_dict(),
                "resolver_allowed_uses": list(item.resolver_allowed_uses),
                "decision_state": item.decision_state,
            }
            for item in terminal.resolution.resolved_entries
        ],
        "permission_binding": dict(terminal.permission_binding),
        "v3_decision": {
            "evidence_hash": v3_hash,
            **v3_material,
            "zero_effect": decision.zero_effect,
        },
    }
    warnings.warn(
        "GT12_E2B_R3_REAL_RUNTIME_EVIDENCE=" + json.dumps(
            evidence, sort_keys=True, separators=(",", ":")
        ),
        RuntimeWarning,
    )
