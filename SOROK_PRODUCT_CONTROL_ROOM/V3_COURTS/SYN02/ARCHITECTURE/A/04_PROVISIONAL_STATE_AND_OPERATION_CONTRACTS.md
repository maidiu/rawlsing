# SYN02-A / 04 — Provisional typed state, operations, temporal and authority contracts

**Status:** FULL PROVISIONAL INTERFACE DESIGN ONLY. Types and algorithms here are candidate interface specifications, not existing imported functions, owner-issued developmental science or permission to mutate production. **Sources:** SYN01 R2 eight-court closeout at bad30f2d06830fdc6646b2657978ff1adcd203f4, CAN008 R2 generic semantics blob b80dd6925066510ecbbfec7b427bf9f688475663, CAN011 middle-state blob 1ed04e62a363493bc7032a99139454a3126e6ea0, ADP016 memory blob 0b7bbe29f6509e31ac7d842962a2bf3d636daa2c, ADP017 epistemic blob 6b4162df27003bec413074178c46fea6360d71a0, settled recursion blob 1a888b6a0eaa3d74e0a8afed715b4cd20785a5b2. No direct original Mac read; no native tests.

## 1. State and owner-qualified identity

The state is one actor-specific **event-sourced, versioned projection** of independently owned facts, not a self-sufficient psychic copy of the world. The following schema is architecture-only:

~~~text
EntityRef {
  namespace; entity_id; kind; origin_owner; immutable_source_hash;
  identity_epoch?; branch_id?
}
EffectiveStamp {
  clock_domain; logical_event_time; sequence_position;
  temporal_resolution; observed_time?; validity_status
}
AuthorityRef {
  owner_id; authority_id; version; content_hash;
  qualified_rule_id?; rule_version?; rule_content_hash?;
  permitted_source_scope; original_issuer_receipt?
}
SourceRef {
  source_id; source_kind; source_owner; source_hash;
  time_scope; event_or_state_parent_hash; actor_permissions;
  data_grade; independently_verified_grade
}
ActorStateSnapshot {
  actor_id; branch_id; history_head; previous_state_hash;
  effective_time; sources_and_rule_manifest;
  embodied_state_refs[]; need_object_relation_refs[];
  expectation_refs[]; committed_V3MS_record_refs[];
  approved_operation_instance_refs[]; contextual_relation_refs[];
  actor_known_claim_refs[]; causal_memory_refs[];
  authorized_motive_or_project_refs[];
  valid_empty_kind_set[]; state_hash
}
WorldContextView {
  world_ref; true_time; material_opportunities[];
  positions[]; resource_constraints[]; institutional_rules[];
  independent_actors[]; owner_receipts[]; UNKNOWN_gaps[]
}
~~~

**Invariants:** one actor and branch across actual later event reads; immutable objective history; monotonic effective time; unknown never becomes null-as-zero/midpoint; no age/type/class/religion-to-psyche bootstrapping; no module presence implying developed mind; no duplicated V2/PFF psyche; all numeric semantics separately authorized. A snapshot **references**, rather than takes ownership of, source-specific world, relationship, material, memory and epistemic records. A derived view computes from those records without hidden persistent writes (historical M26 failure must be repaired before reuse).

## 2. Functional operations, acquisition and sparse relations

An operation's registered definition, actor's acquired ability to use it, its current recruitment and history-conditioned interaction with another operation are distinct objects. An optional relation overlay must be *representable under current original CAN011/other owner jurisdiction* before being committed. The current registered CAN011 kinds remain exactly **V3MS_MEDIATOR, V3MS_TENSION, V3MS_PRACTICE**, not a fourth newly declared relation kind.

~~~text
RegisteredOperationSpec {
  operation_id; definition_owner; spec_hash; semantic_kind;
  input_contract_refs[]; output_effect_contract_refs[];
  qualified_preconditions[]; target_owner_id;
  failure_and_nochange_semantics; allowed_context_scope_schema;
  admission_rule_ref; evaluator_ref
}
ActorOperationInstance {
  actor_id; operation_id; instance_id; registered_spec_hash;
  formation_or_initialization_receipt; acquired_at;
  governed_scope; lifecycle: ACTIVE|DORMANT|ENDED;
  evidence_of_actual_use_refs[]; current_record_hash
}
ContextPredicate {
  predicate_id; semantic_domain; input_paths[];
  owner_ref; ruleset_ref; result: TRUE|FALSE|UNKNOWN|DENIED
}
FunctionalRelationCandidate {
  relation_id; holder_actor_id; source_operation_or_state_ref;
  destination_operation_or_state_ref; proposed_relation_semantics;
  context_predicate_refs[]; proposed_qualifying_history_refs[];
  proposed_operation: CREATE|RESTRICT|ENABLE|INHIBIT|TRANSFORM|END|NO_CHANGE;
  requested_semantic_effect_contract;
  authorized_registry_kind_or_EXTENSION_HOLD;
  qualified_creation_rule_ref?; proposed_effective_time;
  parent_state_hash; proposal_hash
}
CommittedFunctionalRelation {
  holder_actor_id; relation_id; exact_owner_rule_ref;
  authorized_persistent_carrier_ref; source_ref; target_ref;
  relation_semantics; context_scope; evidence_parent_refs[];
  formed_at; lifecycle; prior_relation_hash?; versioned_relation_hash
}
~~~

Candidate semantics include context conditioning, facilitation, inhibition, support dependency, composition and scoped recruitment. These are **research distinctions, not a validated universal ontology or automatic graph edge types**. Without a sufficient existing carrier/owner-approved state-kind extension, return **EXTENSION_HOLD**, do not create a shadow psyche. A real external tool or helper may be an affordance relation **outside the person**, not evidence of internally acquired competence. A different value under an old fixed relation is not a newly formed relation. A later signal can sometimes yield actual insight without repetition, but only if a competent rule warrants that exact acquisition.

## 3. Objective event, actor reception, actual response and durable transition

~~~text
ProposedEncounter {
  proposal_id; N_batch_ref; provisional_time_window;
  possible_world_conditions[]; contingent_coactor_ids[];
  candidate_feature_contacts[]; objective_truth_issued=false
}
ObjectiveOccurrence {
  event_id; world_and_coactor_sources[];
  actual_attempts[]; independently_realized_actions[];
  material_outcomes[]; exact_time; owner_admission_ref;
  immutable_event_hash
}
ActorReception {
  actor_id; occurrence_ref; receivable_feature_refs[];
  not_received_feature_refs[]; unknown_reception_features[];
  modality_refs[]; CAN008_domain_Rule_A_ref?;
  event_side_uptake_ref?; immediate_response_ref?
}
CurrentResponse {
  actor_id; E_ref; prior_actor_state_hash;
  coactive_conditioning_refs[]; current_streams_and_conflicts[];
  actual_action_intention_refs[]; actual_performance_receipts[];
  downstream_owner_effect_proposals[]; current_effect_hash;
  CAN008_evaluator_receipt
}
DurableChangeProposal {
  actor_id; E_or_governed_activity_parents[];
  previous_state_hash; update_kind; requested_target_kind;
  contextual_scope; evidence_for_change_and_against[];
  domain_Rule_T_ref?; transition_proposal_hash
}
~~~

Objective occurrence does not imply child exposure. Encounter receipt is not necessarily an explicit self-conscious concept. An actual attempted action and achieved material outcome differ; actual caregiver kindness and the child's felt repair differ. CAN008 R2 provides **generic** coupled actor/event input semantics; concrete Rule A remains specific and unissued here. CAN011 persistent target operation or genuine NO_CHANGE requires a valid concrete Rule T. Other domains (CAN010 needs, CAN012 rupture, ADP016 memory, ADP017 claims, CAN009 material) have independent ownership.

## 4. Memory and actor-safe retrospective view

Do **not** create a third memory store. Reuse ADP016's source-bound EVENT_REFERENTIAL_MEMORY and CAUSAL_TRACE_MEMORY and ADP017's governed CanonicalClaimRef and qualified actor stance/claim access. A nondeclarative trace may modify causal response without first-person recollection. A late false explanatory belief can be source-qualified ADP017 BELIEF while the original objective event remains true; this is not license to invent positive remembered infant event detail.

~~~text
ActorSafeBatchEnvelope {
  actor_id; effective_now; visible_event_feature_refs[];
  actually_accessible_memory_feature_bindings[];
  accessible_claim_ref_and_stance_pairs[];
  permitted_registers[]; uncertainty_and_omission_markers[];
  read_only_projection_hash; ADP016_017_permissions;
  NEVER_MODEL_VISIBLE: analyst_history_ref, inaccessible_event_id,
    inaccessible_event_count_or_order, raw_structural_classification,
    protected_causal_trace_detail, server_internal_batch_ref
}
RetrospectiveCandidate {
  narrator_output_ref; safe_envelope_hash;
  recounted_accessible_features[]; uncertain_recollections[];
  proposed_current_interpretations[]; proposed_internal_acts[];
  state_mutation_receipt=NONE
}
InternalActAdmission {
  actor_id; candidate_ref; actual_current_reflexive_activity?;
  exact_SCI05_owner_rule_ref?; source_qualification;
  before_actor_hash; decision: ACCEPT|DENY|HELD;
  after_actor_hash?; causal_transition_receipt?
}
~~~

**Side-channel rule:** suppress revealing event IDs, sequence gaps, counts, missing position placeholders, hashes or analyst interpretations in model-visible envelopes. Internal server refs stay server-side. Textual injunctions to the narrator are insufficient. V2 renders available data and never writes back a psychic state. The historical M19/M30 NarrationSupport path, which conditionally uses rendered words to mutate later person state, must not survive uncontrolled.

## 5. Typed evaluation and atomic, domain-owned effects

**Proposed function:** evaluate_current_encounter(objective_event, actor_pre, actor_access, world_read, exact_authorities) -> RuleEvaluationResult<CurrentResponse>.

Semantically it must: (i) verify source/actor/time/permission; (ii) build a bounded local, context-qualified readset of existing operations and relation candidates **actually accepted as current state**; (iii) jointly evaluate concurrent CAN008 effects under concrete Rule A (no imposed single winner); (iv) distinguish each actor's response from independently realized external action; (v) prepare target-owner proposed effects, never write arbitrary cross-domain deltas; (vi) request CAN010/011/012/ADP016/017/CAN009 specific admission separately; (vii) commit qualified, correctly ordered effects and receipts only via C9/C12-owned transaction; (viii) ensure future E2 dereferences **semantic content**, not merely a different state hash.

**Cycle policy:** evaluate a dependency subgraph restricted by approved actor/context/type; acyclic owner dependencies can be ordered by governing scheduler. When same-time dependency cycles arise, demand a separately issued termination/fixed-point/precedence rule; no invented numerical relaxation coefficient. Missing such law means **HELD_AMBIGUOUS_CYCLE**, no unbounded recursion, no silent max/average. Conflict or complexity refusal must be explicit. Historic V3 working-copy route alone is not full atomicity: RX02 found pre-route writes that may survive a fault.

~~~text
RuleEvaluationResult<T> =
  ADMITTED_EFFECT { result:T; source_readset[]; rule_receipt; pre/post_hashes }
  | EVALUATED_NO_CHANGE { exact_rule; passing_predicates; code }
  | VALID_EMPTY { target_kind; exact_registry; owner }
  | NOT_ENCOUNTERED { qualified_world_basis }
  | HELD_MISSING_RULE { missing_rule_owner; required_semantics }
  | HELD_SOURCE_OR_PERMISSION { denied_source; missing_owner }
  | HELD_INSUFFICIENT_EVIDENCE { missing_features[]; rivals[] }
  | HELD_AMBIGUOUS_OR_NONTERMINATING { conflict_or_cycle; owner }
  | REJECTED_OUT_OF_SCOPE { reason; authority }
  | INTEGRITY_FAILURE { mismatched_hash/clock/branch; receipt }
~~~

**Four separations:** VALID_EMPTY is a lawful state with zero records; EVALUATED_NO_CHANGE requires an actual qualified original-domain evaluator; HELD_MISSING_RULE says nothing about whether a person would change; NOT_ENCOUNTERED is not equivalent to an encountered zero-effect event. System unknown is not actor's positive self-report 'I do not know'.

## 6. Complete N11 batch and temporal transaction

~~~text
PersonWorldBatchInput {
  branch_id; actor_id; C12_lineage_head; pre_batch_actor_hash;
  pre_batch_world_hash; clock; source_owner_refs; authority_manifest;
  prior_batch_trajectory_ref_server_only?
}
ProspectiveBatch {
  call_id; proposal_phase=SECOND_HALF_N;
  proposed_events[3..5]: ProposedEncounter[];
  origin_person_hash; conditional_dependencies[];
  unissued_psych_effects=NONE
}
RealizedEventRecord {
  proposal_ref; world_event_receipt?; independent_coactor_actions[];
  actor_reception_and_response?; admitted_target_owner_changes[];
  actual_time; previous_actor_world_hash; post_actor_world_hash;
  realized|rejected|held|not_encountered; exact_authority_receipts
}
IntervalRecord {
  start/end; actual_household/work/school/care_actions[];
  material_change_refs[]; independent_other_actions[];
  actor_activity_and_no_encounter_receipts[];
  unknown_coverage[]; next_actor_world_hash
}
CompletedBatch {
  ordered_event_records[]; interstitial_intervals[];
  committed_prefix_count; held_suffix[]; error_class;
  actor_world_initial/final_hashes; memory_parent_refs[];
  checkpoint; server_only_batch_ref
}
CallNPlusOne {
  first_half: actor_safe_retrospection_from_completed_prefix;
  second_half: next_conditional_batch[3..5];
  postcall_SCI05_decision; dependent_proposal_invalidation;
  source_owner_candidate_validation
}
~~~

**Order:** call N second half proposes 3–5; Rawlsing realizes independently eligible actual events in increasing clock order, with intervening lived activity; event k+1 sees state after event k and its interval; call N+1 first half actor-safely retrospects actual realized prefix; same call N+1 second half proposes next 3–5. No ordinary model call within batch. First call has no synthetic prior memory batch; terminal can have retrospective-only call.

**SCI05 same-call constraint:** a first-half self-account may linguistically condition second-half prose, but cannot *natively commit* as actor state mid-uninterrupted generation without proven interleaving. After call the qualified SCI05 owner admits, denies or holds a new reflective act; second-half prospective candidates contingent on refused change are invalidated/held, independent candidates may be separately validated. No retroactive infant belief or implicit narrator psyche mutation.

**Partial batch:** C12/C6/ADP021 owner must decide accepted-prefix+held-suffix vs whole-batch abort. Either must forbid running E3 from an uncommitted E2, fabricating E2 memories, hidden test-only material assumptions, source-free independent B, and corrupt cold replay. Render failure must not falsely undo a genuinely realized world event nor leave unacknowledged psychic mutations. Preserve actual clocks, rule/source hashes, ADP020 stochastic receipts and actor-limited projection.

## 7. Discriminating tests, all SPECIFICATION_ONLY / NOT_RUN

| Test | Controlled intervention | Required semantic result |
|---|---|---|
| **P1 acquired practical composite** | Actual participated training E1, previously absent competence, later independent E2 with identical task/tool/B | Actual C9 reads formed operation semantic value and changes action; changed tool alone does not count |
| **P2 new relation vs recruitment** | Two prior operations exist; novel qualified history allegedly creates cross-operation applicability | E2 only newly uses relation when Rule T admitted; if old relation always existed but new context recruited it, label context activation, not acquisition |
| **N1 lawful continuity** | Qualified event, actual Rule A/T outputs NO_CHANGE, same E2 world/B | No fabricated change. If Rule T missing -> HOLD, not NO_CHANGE |
| **N2 coherent actor** | History demonstrates consistent conduct and no opposed learned disposition | VALID_EMPTY tension remains lawful; no default contradictions or cracks |
| **F1 sever formation→E2 edge** | Keep world/B/time and all unrelated fields fixed, remove only qualified formed relation/value-read | Later difference disappears or precisely holds; altered hash/prompt alone not proof |
| **F2 inaccessible memory** | Objective E1 unchanged; ADP016 feature unavailable / ADP017 claim inaccessible | N+1 first person reveals no direct/indirect detail; independently earned nondeclarative trace may still condition future action |
| **F3 denied B E2** | B source not owner-admitted after E1 | E2 held and E3+ not realized as facts; truthful prefix and cold/replay |
| **F4 rejected reflection** | N+1 proposes self-interpretation; SCI05 denies it | No psych write; dependent proposed future events held; unrelated ones can be validated |
| **F5 narrator-only words** | Vary rendered warm/coercive text with objective events and actor initial state fixed | Subsequent V3 state invariant absent separately admitted new internal activity |
| **F6 derived writes** | Compute derived twice/cold reopen with unchanged stored source state | No persistent register/metabolic change; historic M26 would fail |
| **F7 unissued Rule T** | Source and event admitted, domain Rule T absent | HELD_MISSING_RULE, never clean NO_CHANGE or native-person success |

No generated example has been actually run or empirically validated by SYN02-A.

## 8. Build/reuse versus scientific grant — actual downstream owners

| Proposed function (NOT verified current symbol) | Input / accountable owner | Emitted result → first consumer | Disposition |
|---|---|---|---|
| world.resolve_occurrence | C0/C4/C8/ADP019 actual world/B owner and clock | ObjectiveOccurrence → CAN008/C9 | Native source-owned producer/permission held; reuse actual qualified C8 |
| actor.qualify_reception | CAN008 generic R2 + domain Rule A + actor sources | ActorReception/CurrentResponse → C9/CAN011 | Existing generic contract; concrete science and current effective import held |
| person.evaluate_historical_transition | CAN010/011/012 exact event/action parents | Owned target transition or nochange/hold → later C9 E2 | Generic registry exists; domain Rule T/new relation semantics unissued |
| relation.evaluate_contextual_recruitment | Existing actor-owned state, event and scopes | Concurrent bounded streams/readset → CAN008 | Inherited V3/PFF adapter candidate; no separate psyche |
| life.compute_interval | C6/SDTF/C8 work/care/source-qualified activity | IntervalRecord → later event C9 | Historical scheduler can be adapted; native interval producer/wiring held |
| memory.compile_actor_safe_retrospection | ADP016/017, actually retained accessible features | ActorSafeBatchEnvelope → N+1 first half | Existing memory semantics; materialized safe packager/sidechannel verification held |
| sci05.review_self_account | Actual actor current new activity, SCI05 original issuer | Later admitted internal event or HOLD → next eligible actor reaction | Explicit native source/scientific admission held |
| batch.resolve_sequence | C6/C8/C9/C12, conditional 3–5, world/time/rules | CompletedBatch → C12 and next-call handoff | S48 one-candidate transport only; real batch engineering not integrated |
| c12.commit_and_expose | All governed actor/world state, C11 native weld | Same continuing person and actor-safe A0–A5 | Current assembled import, native source and human evaluation held |

**Minimal new engineering candidates:** owner-linked operation/relation adapter (not new psyche store); canonical event/interval transaction coordinator; indexed later C9 semantic readsets; ADP016/017-safe retrospective compactor; N11 batch proposal validation and SCI05-dependent invalidation. Recover actual current symbols and avoid duplicating existing engines first. No unissued rule or actor/source permission is created by this specification.
