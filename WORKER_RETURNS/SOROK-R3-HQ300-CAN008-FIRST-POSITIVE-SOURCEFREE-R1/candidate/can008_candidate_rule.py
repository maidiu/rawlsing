"""HQ300 — candidate CAN-008 R2 coupling/response rule module.

PROVISIONAL CANDIDATE — NOT AN ADOPTED RULE — NOT A PRODUCTION OWNER.

Implements the smallest concrete rule body permitted by the ADOPTED CAN-008 R2
semantics (blob b80dd6925066510ecbbfec7b427bf9f688475663):
  * §6 occurrence gate (committed causal response requires exact admitted occurrence)
  * §7-10 receivability -> actor uptake/appraisal -> situated recruitment,
    with all noncollapse laws enforced (machine reading != uptake; recruitment
    != access; uptake != durable belief)
  * §11 handoff: coupling -> registered response rule -> working-view effects ->
    target-owner validation -> atomic commit OR rollback
  * §11 effect grammar unchanged (BUFFER/AMPLIFY/DEFLECT/REROUTE/TRANSFORM/BLOCK)
  * §14 distinct nonpositive/valid-empty states
  * §16 the 23 rule-obligation bindings (a rule omitting a required binding FAILS CLOSED)
  * §17 V3ResponseEvaluationReceipt content requirements

Rule identity: CAND_R_CAN008_COUPLING_RESPONSE@1.0.0-candidate — registered only
in the WORKER CANDIDATE REGISTRY FIXTURE, never in the production registry.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .adopted_contract import (
    EFFECT_GRAMMAR, NONPOSITIVE_DECISION_STATES, NONCOLLAPSE_LAWS,
    R2_RULE_OBLIGATION_ITEMS, PINS, CAN008_R2_CONTRACT,
    AdmittedEvent,
)
from .candidate_registry_fixture import CANDIDATE_REGISTRY, CandidateRuleRegistration

RULE_ID = "CAND_R_CAN008_COUPLING_RESPONSE"
RULE_VERSION = "1.0.0-candidate"
RULE_GRAIN = "SOURCEFREE_CANDIDATE_RULE__NOT_ADOPTED__NOT_PRODUCTION"


def _sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class CouplingRuleBinding:
    """§16 23-item binding. Every item must be present; omission fails closed."""
    rule_id: str
    rule_version: str
    rule_content_hash: str
    eligible_event_authority_signatures: Tuple[str, ...]
    eligible_event_roles: Tuple[str, ...]
    actor_scope: str
    temporal_scope: str
    receivability_semantics: str
    eligible_conditioning_owner_signatures: Tuple[str, ...]
    conditioning_causal_use_roles: Tuple[str, ...]
    counterpart_scoping: str
    modality_evidence_authorities: Tuple[str, ...]
    uptake_appraisal_semantics: str
    recruitment_semantics: str
    multiplicity_handling: str
    co_determination_closure: str
    prior_response_history_predicates: str
    current_condition_effort_role: str
    effect_kinds: Tuple[str, ...]
    target_authority_kind: str
    target_validation: str
    pff_current_consequence_projection: str
    valid_empty_behavior: str
    missing_deferred_ambiguous_behavior: str
    quantitative_contract: str
    adp020_binding: str
    atomic_commit_behavior: str
    provenance_replay_requirements: str
    obligation_coverage: Tuple[str, ...] = R2_RULE_OBLIGATION_ITEMS

    def validate_complete(self) -> Optional[str]:
        vals = {
            "rule_id_version_content_hash": (self.rule_id, self.rule_version, self.rule_content_hash),
            "eligible_precipitating_event_authority_signatures_and_roles":
                (self.eligible_event_authority_signatures, self.eligible_event_roles),
            "exact_actor_and_temporal_scope": (self.actor_scope, self.temporal_scope),
            "receivability_semantics": (self.receivability_semantics,),
            "eligible_conditioning_owner_signatures": (self.eligible_conditioning_owner_signatures,),
            "conditioning_causal_use_roles": (self.conditioning_causal_use_roles,),
            "counterpart_relationship_scoping": (self.counterpart_scoping,),
            "permitted_modality_evidence_authorities_and_roles": (self.modality_evidence_authorities,),
            "actor_uptake_appraisal_relation_semantics": (self.uptake_appraisal_semantics,),
            "situated_recruitment_relation_semantics": (self.recruitment_semantics,),
            "multiplicity_contradiction_handling": (self.multiplicity_handling,),
            "permitted_co_determination_and_deterministic_closure": (self.co_determination_closure,),
            "prior_response_history_predicates_if_used": (self.prior_response_history_predicates,),
            "current_condition_effort_role_if_used": (self.current_condition_effort_role,),
            "effect_graph_and_existing_can008_effect_kinds": (self.effect_kinds,),
            "target_authority_kind_and_target_validation": (self.target_authority_kind, self.target_validation),
            "pff_current_consequence_projection_if_emitted": (self.pff_current_consequence_projection,),
            "valid_empty_behavior": (self.valid_empty_behavior,),
            "missing_deferred_ambiguous_failure_behavior": (self.missing_deferred_ambiguous_behavior,),
            "quantitative_contract_if_numeric": (self.quantitative_contract,),
            "adp020_binding_if_stochastic": (self.adp020_binding,),
            "atomic_validation_commit_behavior": (self.atomic_commit_behavior,),
            "provenance_replay_requirements": (self.provenance_replay_requirements,),
        }
        for item in R2_RULE_OBLIGATION_ITEMS:
            v = vals.get(item)
            if v is None or any(x is None or x == "" or x == () for x in v):
                return f"RESPONSE_COUPLING_RULE_MISSING:{item}"
        if not set(self.effect_kinds) <= set(EFFECT_GRAMMAR):
            return "RESPONSE_COUPLING_RULE_MISSING:effect_kind_outside_adopted_grammar"
        return None


def build_default_binding(actor_scope: str = "ACTOR_SYNTH_1",
                          temporal_scope: str = "T_1998_2000") -> CouplingRuleBinding:
    content = {
        "semantics": "coupling-response candidate over adopted R2 law",
        "effect_kinds": list(EFFECT_GRAMMAR),
        "target": "CAN008_CURRENT_AND_REQUESTED_OWNER_EFFECTS",
    }
    return CouplingRuleBinding(
        rule_id=RULE_ID,
        rule_version=RULE_VERSION,
        rule_content_hash=_sha(_canon(content), PINS["CAN008_R2"]),
        eligible_event_authority_signatures=("ISSUER_AUTH_WORLD_SCHED", "ISSUER_AUTH_INSTITUTION"),
        eligible_event_roles=("PRECIPITATING_EVENT_STREAM",),
        actor_scope=actor_scope,
        temporal_scope=temporal_scope,
        receivability_semantics="event public features receivable to actor scope",
        eligible_conditioning_owner_signatures=("CAN010", "CAN011", "ADP015", "ADP016", "ADP017"),
        conditioning_causal_use_roles=("RECRUITMENT_ONLY",),
        counterpart_scoping="none-required",
        modality_evidence_authorities=("NONE_USED:rule-uses-no-modality-evidence",),
        uptake_appraisal_semantics="appraisal projection; NOT durable belief",
        recruitment_semantics="situated recruitment refs; recruitment != actor access",
        multiplicity_handling="all paths preserved; no winner-take-all",
        co_determination_closure="deterministic single-pass closure",
        prior_response_history_predicates="none",
        current_condition_effort_role="none",
        effect_kinds=EFFECT_GRAMMAR,
        target_authority_kind="CAN008_CURRENT_PLUS_SEPARATE_OWNER_REQUEST",
        target_validation="atomic precheck then commit or rollback",
        pff_current_consequence_projection="not-emitted",
        valid_empty_behavior="RESPONSE_EFFECTS_VALID_EMPTY lawful and distinct",
        missing_deferred_ambiguous_behavior="typed nonpositive state; never silent conversion",
        quantitative_contract="none",
        adp020_binding="none (deterministic)",
        atomic_commit_behavior="validate-all-then-commit; rollback on any failure",
        provenance_replay_requirements="§17 receipt content bound and replay-exact",
    )


@dataclass
class OwnerPrestate:
    actor_id: str
    can010_expectations: Tuple[str, ...] = ()
    can010_strivings: Tuple[str, ...] = ()
    can011_practices: Tuple[str, ...] = ()
    can011_tensions: Tuple[str, ...] = ()
    adp016_memory_refs: Tuple[str, ...] = ()
    adp017_claim_refs: Tuple[str, ...] = ()
    prior_can008_response_count: int = 0
    world_ref: str = ""
    world_as_of: str = ""


def occurrence_gate(event: AdmittedEvent, registry) -> Dict[str, Any]:
    """§6: no committed causal response without exact admitted occurrence."""
    if event.admission_state != "ADMITTED":
        return {"status": "REFUSED", "code": "BLOCK_UNADMITTED_EVENT",
                "event_id": event.event_id}
    if event.event_kind in ("DRAFT_RESPONSE", "REJECTED_RENDER", "UNEMITTED_CANDIDATE",
                            "V2_RENDER_CANDIDATE", "STATIC_STATE_RECORD"):
        return {"status": "REFUSED", "code": "BLOCK_NON_OCCURRENCE_KIND",
                "event_kind": event.event_kind}
    if event.derived_from_future_partition:
        return {"status": "REFUSED", "code": "BLOCK_HIDDEN_FUTURE_LEAK",
                "event_id": event.event_id}
    ident = registry.admit_event_identity(event.event_id, event.event_hash,
                                          event.issuer_authority_id)
    if ident.get("status") == "REFUSED":
        return ident
    return {"status": "ADMITTED_OCCURRENCE", "event_id": event.event_id,
            "event_hash": event.event_hash}


def coupline_evaluate(event: AdmittedEvent, prestate: OwnerPrestate,
                      binding: CouplingRuleBinding,
                      registry) -> Dict[str, Any]:
    """Coupling evaluation: receivability -> uptake projection -> recruitment."""
    gate = occurrence_gate(event, registry)
    if gate["status"] != "ADMITTED_OCCURRENCE":
        return {"decision_state": gate.get("code", "BLOCK_UNADMITTED_EVENT"),
                "gate": gate, "committed": False}

    # issuer / authority signature check (§16 item 2)
    if event.issuer_authority_id not in binding.eligible_event_authority_signatures:
        return {"decision_state": "BLOCK_FORGED_OR_MISMATCHED_ISSUER",
                "code": "BLOCK_FORGED_OR_MISMATCHED_ISSUER",
                "issuer": event.issuer_authority_id, "committed": False}

    # actor + temporal scope (§16 item 3)
    if event.actor_scope != binding.actor_scope:
        return {"decision_state": "BLOCK_WRONG_ACTOR_SCOPE",
                "code": "BLOCK_WRONG_ACTOR_SCOPE",
                "actor_scope": event.actor_scope, "committed": False}

    # stale / as-of world (exact world/ctx binding)
    if event.world_ref != prestate.world_ref or event.world_as_of != prestate.world_as_of:
        return {"decision_state": "BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF",
                "code": "BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF",
                "event_world": (event.world_ref, event.world_as_of),
                "prestate_world": (prestate.world_ref, prestate.world_as_of),
                "committed": False}

    # reverse chronology guard (causal parents strictly earlier)
    # (parent event times are validated by the chain ledger; flag carried here)
    if event.causal_parent_event_ids and event.reverse_chronology_flag:
        return {"decision_state": "BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT",
                "code": "BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT", "committed": False}

    # receivability
    receivable = bool(event.public_features)
    receivability = "RECEIVABLE" if receivable else "RESPONSE_EVENT_RECEIVABILITY_UNRESOLVED"

    # uptake projection (machine reading != uptake; uptake != durable belief)
    uptake = {
        "projection": "appraisal_projection_under_" + binding.uptake_appraisal_semantics,
        "is_durable_belief": False,
        "is_machine_reading": False,
        "basis": "event public features + conditioning recruitment",
    }

    # recruitment (recruitment != access)
    recruited: List[str] = []
    for m in prestate.adp016_memory_refs:
        recruited.append(f"ADP016:{m}:RECRUITMENT_ONLY_NOT_ACCESS")
    for p in prestate.can011_practices:
        recruited.append(f"CAN011:PRACTICE:{p}")
    for t in prestate.can010_strivings:
        recruited.append(f"CAN010:STRIVING:{t}")

    return {
        "decision_state": "COUPLING_EVALUATED",
        "gate": gate,
        "receivability": receivability,
        "uptake_appraisal_projection": uptake,
        "situated_recruitment": recruited,
        "recruitment_is_not_access": True,
        "committed": False,
    }


def response_rule_apply(coupling: Dict[str, Any], prestate: OwnerPrestate,
                        binding: CouplingRuleBinding,
                        requested_effect: str) -> Dict[str, Any]:
    """§11 handoff into CAN-008 response: effect grammar + target-owner request."""
    if coupling.get("decision_state") != "COUPLING_EVALUATED":
        return {"decision_state": coupling.get("decision_state", "RESPONSE_INPUTS_VALID_EMPTY"),
                "committed": False}
    if requested_effect not in binding.effect_kinds:
        return {"decision_state": "RESPONSE_COUPLING_RULE_MISSING",
                "detail": "effect kind outside registered rule effect graph",
                "committed": False}
    current_response = {
        "effect_kind": requested_effect,
        "durability": "NON_DURABLE_CURRENT_CONSEQUENCE",
    }
    target_owner_effects = [
        {"target_owner_kind": binding.target_authority_kind, "validated": False,
         "committed": False, "request_kind": "SEPARATELY_OWNED_EFFECT_REQUEST"},
    ]
    return {
        "decision_state": "RESPONSE_EFFECTS_PRODUCED",
        "current_response_consequence": current_response,
        "target_owner_effect_requests": target_owner_effects,
        "committed": False,
    }


def build_response_receipt(event: AdmittedEvent, prestate: OwnerPrestate,
                           binding: CouplingRuleBinding,
                           coupling: Dict[str, Any],
                           response: Dict[str, Any]) -> Dict[str, Any]:
    """§17 V3ResponseEvaluationReceipt content (audit/replay evidence; NOT a
    durable actor uptake/memory/belief state)."""
    receipt = {
        "receipt_kind": "V3ResponseEvaluationReceipt",
        "contract": CAN008_R2_CONTRACT,
        "rule_id": binding.rule_id,
        "rule_version": binding.rule_version,
        "rule_content_hash": binding.rule_content_hash,
        "precipitating_event": {
            "event_id": event.event_id, "event_hash": event.event_hash,
            "issuer_authority_id": event.issuer_authority_id,
            "effective_causal_time": event.effective_causal_time,
            "role": "PRECIPITATING_EVENT_STREAM",
        },
        "conditioning_owner_refs": list(binding.eligible_conditioning_owner_signatures),
        "conditioning_causal_use_roles": list(binding.conditioning_causal_use_roles),
        "receivability": coupling.get("receivability"),
        "uptake_appraisal_projection": coupling.get("uptake_appraisal_projection"),
        "situated_recruitment": coupling.get("situated_recruitment"),
        "effect_kind": response.get("current_response_consequence", {}).get("effect_kind"),
        "current_response_consequence": response.get("current_response_consequence"),
        "target_owner_effects": response.get("target_owner_effect_requests"),
        "decision_state": response.get("decision_state"),
        "noncollapse_laws_bound": list(NONCOLLAPSE_LAWS),
        "is_durable_actor_state": False,
    }
    receipt["receipt_hash"] = _sha(_canon(receipt))
    return receipt


def register_default_rule(registry=None) -> Dict[str, Any]:
    """Register the candidate rule in the WORKER CANDIDATE REGISTRY FIXTURE only."""
    reg = registry if registry is not None else CANDIDATE_REGISTRY
    binding = build_default_binding()
    err = binding.validate_complete()
    if err:
        return {"status": "REFUSED", "code": err}
    return reg.register(CandidateRuleRegistration(
        rule_id=binding.rule_id,
        rule_version=binding.rule_version,
        rule_content_hash=binding.rule_content_hash,
        issuer_authority_id="ISSUER_AUTH_CANDIDATE_FIXTURE",
        issuer_authority_version="1",
        actor_scope=binding.actor_scope,
        temporal_scope=binding.temporal_scope,
        effect_kinds=binding.effect_kinds,
        target_owner_kind="CAN008_CURRENT",
        admission_state="CANDIDATE_ADMITTED_IN_FIXTURE",
    ))


def _with_reverse_flag(event: AdmittedEvent) -> AdmittedEvent:
    """Hostile-case helper: mark a causal-parent chronology inversion on a copy."""
    return AdmittedEvent(**{**event.__dict__, "reverse_chronology_flag": True})
