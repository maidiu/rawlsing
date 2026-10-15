"""HQ300 — typed shapes derived EXACTLY from adopted authority (candidate use only).

PROVISIONAL CANDIDATE — NOT AN ADOPTED RULE — NOT A PRODUCTION OWNER.

Every constant/enum below is transcribed from an adopted authority file at its
exact pinned Git blob. The pin is recorded on each family so an independent
reviewer can re-derive the transcription.

Adopted sources (git blob SHA-1, NUL-header identity):
  CAN008_R2  b80dd6925066510ecbbfec7b427bf9f688475663  (adopted via HQ pointer a6bc1555...)
  CAN008_V1  976c59086b938992114f68621f149687670e306d / 7bd28360ec6a74975bb7eb809f6ad397529491b3
  ADP016     0b7bbe29f6509e31ac7d842962a2bf3d636daa2c / c6619a286e115d060ab4830889e7fc23762167a5
  ADP017     6b4162df27003bec413074178c46fea6360d71a0 / eece4f3f2f3f9288ab9bbc645dc81e20a99e1280
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

PINS = {
    "CAN008_R2": "b80dd6925066510ecbbfec7b427bf9f688475663",
    "CAN008_V1_MD": "976c59086b938992114f68621f149687670e306d",
    "CAN008_V1_JSON": "7bd28360ec6a74975bb7eb809f6ad397529491b3",
    "ADP016_MD": "0b7bbe29f6509e31ac7d842962a2bf3d636daa2c",
    "ADP016_JSON": "c6619a286e115d060ab4830889e7fc23762167a5",
    "ADP017_MD": "6b4162df27003bec413074178c46fea6360d71a0",
    "ADP017_JSON": "eece4f3f2f3f9288ab9bbc645dc81e20a99e1280",
}
CAN008_R2_CONTRACT = "V3_ACTOR_RESPONSE_PRESSURE_FLOW_TRANSACTION_RULESET@2.0.0-CANDIDATE.R1"

# --- CAN-008 R2 §11 effect grammar (adopted; R2 adds no new kind) -------------
EFFECT_GRAMMAR: Tuple[str, ...] = (
    "BUFFER", "AMPLIFY", "DEFLECT", "REROUTE", "TRANSFORM", "BLOCK",
)

# --- CAN-008 R2 §6 occurrence-gate / §14 nonpositive decision states ----------
OCCURRENCE_GATE_STATES: Tuple[str, ...] = (
    "ADMITTED_OCCURRENCE",
    "BLOCK_UNADMITTED_EVENT",
    "BLOCK_NON_OCCURRENCE_KIND",
    "BLOCK_DUPLICATE_EVENT_IDENTITY",
)
# §14: distinct nonpositive states must remain distinct
NONPOSITIVE_DECISION_STATES: Tuple[str, ...] = (
    "RESPONSE_COUPLING_RULE_MISSING",
    "RESPONSE_CONDITIONING_BINDING_INVALID",
    "RESPONSE_CONDITIONING_OWNER_UNBOUND",
    "RESPONSE_MODALITY_EVIDENCE_UNBOUND",
    "RESPONSE_EVENT_RECEIVABILITY_UNRESOLVED",
    "RESPONSE_COUPLING_AMBIGUOUS",
    "BLOCKED_CONDITIONING_STATE_AS_EVENT",
    "BLOCKED_MACHINE_INTERPRETATION_AS_ACTOR_UPTAKE",
    "BLOCKED_UNOCCURRED_ARTIFACT_FEEDBACK",
    "BLOCKED_DURABLE_OWNER_CAPTURE",
    "COUPLING_VALID_EMPTY",
    "UPTAKE_VALID_EMPTY",
    "RECRUITMENT_VALID_EMPTY",
    "LOW_SIGNIFICANCE_COUPLING",
    "RESPONSE_INPUTS_VALID_EMPTY",
    "RESPONSE_EFFECTS_VALID_EMPTY",
    "CURRENT_RESPONSE_CONSEQUENCES_VALID_EMPTY",
)
# R2 noncollapse laws (adoption record "Adopted noncollapse laws")
NONCOLLAPSE_LAWS: Tuple[str, ...] = (
    "interpretation/expectation/striving != present-effect occurrence",
    "scar/need activation/attractor state != current causal evidence",
    "PFF receivability/matching/facilitation != occurrence or causal evidence",
    "machine reading != actor uptake",
    "uptake != durable belief",
    "recruitment != actor access",
    "actor access != focality or self-explanation",
    "precheck failure or negative simulation forces causal neutrality",
    "transient causal_trace is overwrite-only and is not durable memory",
    "current CAN-008 response authority does not seize durable source-owner jurisdictions",
    "DRAFT_RESPONSE -> NO_SELF_FEEDBACK",
    "REJECTED_RENDER -> NO_SELF_FEEDBACK",
    "UNEMITTED_CANDIDATE -> NO_SELF_FEEDBACK",
)

# --- ADP-016 (blob c6619a28...) ------------------------------------------------
ADP016_REPRESENTATION_KIND: Tuple[str, ...] = (
    "EVENT_REFERENTIAL_MEMORY", "CAUSAL_TRACE_MEMORY")
ADP016_SOURCE_FEATURE_STATE: Tuple[str, ...] = (
    "AVAILABLE_SOURCE_BOUND", "AVAILABLE_UNCERTAIN", "UNAVAILABLE")
ADP016_RETENTION_STATE: Tuple[str, ...] = (
    "RETAINED", "DEGRADED", "CONTENT_UNAVAILABLE", "RETENTION_UNKNOWN")
ADP016_ACCESSIBILITY_STATE: Tuple[str, ...] = (
    "ACCESSIBLE", "PARTIALLY_ACCESSIBLE", "INACCESSIBLE",
    "ACCESS_UNKNOWN", "NOT_APPLICABLE_CAUSAL_TRACE")
ADP016_TRANSITION_KIND: Tuple[str, ...] = (
    "FORMATION", "DEGRADE", "MARK_FEATURE_UNCERTAIN", "MARK_FEATURE_UNAVAILABLE",
    "ACCESS_DECREASE", "ACCESS_INCREASE", "RECALL", "REACTIVATE",
    "UNCERTAINTY_INCREASE", "UNCERTAINTY_DECREASE")
ADP016_FORBIDDEN_TRANSITION_KIND: Tuple[str, ...] = ("DELETE_MEMORY",)
ADP016_REQUIRED_MEMORY_FIELDS: Tuple[str, ...] = (
    "memory_id", "actor_id", "representation_kind", "formation_transition_id",
    "objective_source_event_refs", "source_feature_bindings", "retention_state",
    "memory_accessibility_state", "uncertainty_state", "last_transition_id",
    "last_transition_effective_time", "current_state_hash", "integrity_state")
ADP016_REQUIRED_TRANSITION_FIELDS: Tuple[str, ...] = (
    "memory_transition_id", "memory_id", "actor_id", "transition_kind",
    "effective_causal_time", "authority_id", "authority_version",
    "authority_or_rule_hash", "memory_rule_id", "memory_rule_version",
    "memory_rule_hash", "objective_source_event_refs", "causal_parent_event_refs",
    "cue_or_trigger_refs", "pre_state_hash", "post_state_hash",
    "feature_state_before_hash", "feature_state_after_hash",
    "decision_state", "integrity_state")
ADP016_FAIL_CLOSED_STATES: Tuple[str, ...] = (
    "INELIGIBLE_NONCAUSAL_SOURCE", "DEFERRED_MISSING_MEMORY_BASIS",
    "MISSING_PARENT_EVENT", "PARENT_EVENT_HASH_MISMATCH", "UNKNOWN_MEMORY_ID",
    "MEMORY_ID_COLLISION", "PRE_STATE_HASH_MISMATCH", "UNAUTHORIZED_TRANSITION",
    "UNAUTHORIZED_RECALL_CUE", "UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION",
    "UNAUTHORIZED_V2_SESSION_PROMOTION", "UNSUPPORTED_CONFABULATION",
    "MISSING_RULE_VERSION", "MISSING_RNG_AUTHORITY", "RETENTION_UNKNOWN",
    "ACCESS_UNKNOWN", "INTEGRITY_FAILURE")
ADP016_INELIGIBLE_DIRECT_SOURCES: Tuple[str, ...] = (
    "raw source evidence", "V553-V558 structural objects", "ResolvedStructuralContext",
    "SelectionRecord or temporal proxy metadata",
    "structural availability/applicability/opportunity without generated experience",
    "untraversed V555 route", "checkpoint/derived/readiness/integrity/analyst annotation",
    "V2 transcript/session state", "transcript summary", "rendered dialogue/narrative",
    "persona sheet/backstory prose", "memory-distillation prose", "keyword/phrase hook",
    "pending/rejected external proposal", "placeholder/default childhood experience")
ADP016_EXPORTS_TO_ADP017: Tuple[str, ...] = (
    "memory identity", "representation kind", "source-bound feature states",
    "retention state", "memory accessibility state", "uncertainty state",
    "provenance/integrity", "analyst-only causal-trace designation")
ADP016_MUST_NOT_OUTPUT: Tuple[str, ...] = (
    "actor_knows", "actor_believes", "may_claim_first_person", "V2_may_render_as_fact")

# --- ADP-017 (blob eece4f3f...) ------------------------------------------------
ADP017_STANCE_KIND: Tuple[str, ...] = (
    "KNOWLEDGE", "BELIEF", "UNCERTAINTY", "NONKNOWLEDGE")
ADP017_STANCE_OPERATION: Tuple[str, ...] = (
    "ADD", "WITHDRAW", "SUPERSEDE_EXACT_RECORD", "NO_CHANGE")
ADP017_EFFECT_DECISION_STATES: Tuple[str, ...] = (
    "APPLIED_EPISTEMIC_TRANSITION", "NO_EPISTEMIC_TRANSITION",
    "DEFERRED_MISSING_EPISTEMIC_BASIS", "DENIED_NON_ACTOR_SOURCE",
    "DENIED_UNAUTHORIZED_PROMOTION", "BLOCKED_INTEGRITY_FAILURE")
ADP017_FIRST_PERSON_PERMISSIONS: Tuple[str, ...] = (
    "PERMIT_FIRST_PERSON_KNOWLEDGE", "PERMIT_FIRST_PERSON_BELIEF",
    "PERMIT_FIRST_PERSON_UNCERTAINTY", "PERMIT_FIRST_PERSON_NONKNOWLEDGE",
    "DENY_FIRST_PERSON_CLAIM", "DEFER_MISSING_AUTHORITY")
ADP017_REQUIRED_EFFECT_FIELDS: Tuple[str, ...] = (
    "effect_id", "actor_id", "claim_ref", "stance_kind", "stance_operation",
    "causal_parent_refs", "actor_facing_basis_refs", "memory_basis_refs",
    "owning_rule_id", "owning_rule_version", "owning_rule_hash",
    "effective_causal_time")
ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN: Tuple[str, ...] = (
    "OBJECTIVE_SUPPORTED -> KNOWLEDGE",
    "MEMORY_ACCESSIBLE -> KNOWLEDGE",
    "KNOWLEDGE -> implicit BELIEF record",
    "BELIEF -> KNOWLEDGE",
    "OBJECTIVE_CONTRADICTED -> actor recognizes error",
    "EPISTEMIC_STATE_UNKNOWN -> NONKNOWLEDGE",
    "STRUCTURAL_CAUSATION -> actor explanation",
    "INACCESSIBLE -> objective fact forgotten/deleted")
ADP017_MEMORY_NONCOLLAPSE: Tuple[str, ...] = (
    "MEMORY_EXISTS != CLAIM_EXISTS",
    "CLAIM_EXISTS != ACTOR_KNOWS",
    "ACTOR_KNOWS != ACTOR_BELIEVES",
    "ACTOR_BELIEVES != ACTOR_MAY_CLAIM")
ADP017_ANALYST_ONLY_CLASSES: Tuple[str, ...] = (
    "ANALYST_ONLY_OBJECTIVE_TRUTH", "ANALYST_ONLY_CAUSAL_PROVENANCE",
    "ANALYST_ONLY_MISRECOGNITION_RELATION", "ANALYST_ONLY_CAUSAL_TRACE",
    "SYSTEM_EPISTEMIC_UNKNOWN")
ADP017_KNOWLEDGE_GATE_ALL_REQUIRED: Tuple[str, ...] = (
    "exact canonical claim verifies",
    "claim is OBJECTIVE_SUPPORTED in same temporal/subject scope",
    "exact generated/admitted actor-facing acquisition or recognition basis exists",
    "owning V3 rule explicitly emits KNOWLEDGE ActorEpistemicEffect for exact claim",
    "actor role under owning rule is sufficient",
    "causal parent and pre-state integrity verifies",
    "all required authority exists")
ADP017_OBJECTIVE_TRUTH_NECESSARY = True
ADP017_OBJECTIVE_TRUTH_SUFFICIENT = False
ADP017_ACCESSIBLE_MEMORY_AUTO_CREATES_STANCE = False
ADP017_CAUSAL_TRACE_FIRST_PERSON_BASIS = False

# --- CAN-008 R2 §16 concrete rule obligation item names (23) -------------------
R2_RULE_OBLIGATION_ITEMS: Tuple[str, ...] = (
    "rule_id_version_content_hash",
    "eligible_precipitating_event_authority_signatures_and_roles",
    "exact_actor_and_temporal_scope",
    "receivability_semantics",
    "eligible_conditioning_owner_signatures",
    "conditioning_causal_use_roles",
    "counterpart_relationship_scoping",
    "permitted_modality_evidence_authorities_and_roles",
    "actor_uptake_appraisal_relation_semantics",
    "situated_recruitment_relation_semantics",
    "multiplicity_contradiction_handling",
    "permitted_co_determination_and_deterministic_closure",
    "prior_response_history_predicates_if_used",
    "current_condition_effort_role_if_used",
    "effect_graph_and_existing_can008_effect_kinds",
    "target_authority_kind_and_target_validation",
    "pff_current_consequence_projection_if_emitted",
    "valid_empty_behavior",
    "missing_deferred_ambiguous_failure_behavior",
    "quantitative_contract_if_numeric",
    "adp020_binding_if_stochastic",
    "atomic_validation_commit_behavior",
    "provenance_replay_requirements",
)


@dataclass(frozen=True)
class AdmittedEvent:
    event_id: str
    event_hash: str
    issuer_authority_id: str
    issuer_authority_version: str
    event_kind: str
    effective_causal_time: str
    actor_scope: str
    world_ref: str
    world_as_of: str
    admission_state: str
    public_features: Tuple[str, ...] = ()
    causal_parent_event_ids: Tuple[str, ...] = ()
    derived_from_future_partition: bool = False
    reverse_chronology_flag: bool = False


@dataclass(frozen=True)
class GeneratedMemoryState:
    memory_id: str
    actor_id: str
    representation_kind: str
    formation_transition_id: str
    objective_source_event_refs: Tuple[str, ...]
    source_feature_bindings: Tuple[str, ...]
    retention_state: str
    memory_accessibility_state: str
    uncertainty_state: str
    last_transition_id: str
    last_transition_effective_time: str
    current_state_hash: str
    integrity_state: str


@dataclass(frozen=True)
class ActorEpistemicEffect:
    effect_id: str
    actor_id: str
    claim_ref: str
    stance_kind: str
    stance_operation: str
    causal_parent_refs: Tuple[str, ...]
    actor_facing_basis_refs: Tuple[str, ...]
    memory_basis_refs: Tuple[str, ...]
    owning_rule_id: str
    owning_rule_version: str
    owning_rule_hash: str
    effective_causal_time: str


def validate_memory_state(m: GeneratedMemoryState) -> Optional[str]:
    missing = [f for f in ADP016_REQUIRED_MEMORY_FIELDS if not hasattr(m, f)]
    if missing:
        return "INTEGRITY_FAILURE:missing_fields:" + ",".join(missing)
    if m.representation_kind not in ADP016_REPRESENTATION_KIND:
        return "INTEGRITY_FAILURE:bad_representation_kind"
    if m.retention_state not in ADP016_RETENTION_STATE:
        return "INTEGRITY_FAILURE:bad_retention_state"
    if m.memory_accessibility_state not in ADP016_ACCESSIBILITY_STATE:
        return "INTEGRITY_FAILURE:bad_accessibility_state"
    return None


def validate_epistemic_effect(e: ActorEpistemicEffect) -> Optional[str]:
    missing = [f for f in ADP017_REQUIRED_EFFECT_FIELDS if not hasattr(e, f)]
    if missing:
        return "BLOCKED_INTEGRITY_FAILURE:missing_fields:" + ",".join(missing)
    if e.stance_kind not in ADP017_STANCE_KIND:
        return "BLOCKED_INTEGRITY_FAILURE:bad_stance_kind"
    if e.stance_operation not in ADP017_STANCE_OPERATION:
        return "BLOCKED_INTEGRITY_FAILURE:bad_stance_operation"
    return None


def first_person_permission(stance_kind: Optional[str],
                            claim_accessibility: str) -> str:
    """ADP-017 first_person_permission.mapping, transcribed exactly."""
    if claim_accessibility == "CLAIM_ACCESS_UNKNOWN":
        return "DEFER_MISSING_AUTHORITY"
    if claim_accessibility != "CLAIM_ACCESSIBLE":
        return "DENY_FIRST_PERSON_CLAIM"
    if stance_kind is None:
        return "DENY_FIRST_PERSON_CLAIM"
    return {
        "KNOWLEDGE": "PERMIT_FIRST_PERSON_KNOWLEDGE",
        "BELIEF": "PERMIT_FIRST_PERSON_BELIEF",
        "UNCERTAINTY": "PERMIT_FIRST_PERSON_UNCERTAINTY",
        "NONKNOWLEDGE": "PERMIT_FIRST_PERSON_NONKNOWLEDGE",
    }[stance_kind]


def knowledge_gate_check(claim_objective_relation: str,
                         actor_facing_basis_exists: bool,
                         owning_rule_emits_knowledge: bool,
                         actor_role_sufficient: bool,
                         integrity_ok: bool,
                         authority_complete: bool) -> Tuple[bool, List[str]]:
    """ADP-017 knowledge_gate: ALL required; objective truth necessary, not sufficient."""
    reasons: List[str] = []
    if claim_objective_relation != "OBJECTIVE_SUPPORTED":
        reasons.append("claim not OBJECTIVE_SUPPORTED in scope")
    if not actor_facing_basis_exists:
        reasons.append("no exact generated/admitted actor-facing acquisition basis")
    if not owning_rule_emits_knowledge:
        reasons.append("owning rule does not explicitly emit KNOWLEDGE effect")
    if not actor_role_sufficient:
        reasons.append("actor role under owning rule insufficient")
    if not integrity_ok:
        reasons.append("causal parent or pre-state integrity failed")
    if not authority_complete:
        reasons.append("required authority missing")
    return (not reasons, reasons)
