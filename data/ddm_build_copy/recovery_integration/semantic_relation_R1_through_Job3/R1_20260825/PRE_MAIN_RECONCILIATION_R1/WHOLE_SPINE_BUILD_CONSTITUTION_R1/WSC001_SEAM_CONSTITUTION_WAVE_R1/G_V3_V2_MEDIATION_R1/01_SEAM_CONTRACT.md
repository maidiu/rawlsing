# WSC001G — V3 -> V2 MEDIATION / EXPRESSION / RETURN SEAM CONTRACT R1

## 0. Contract scope

This contract defines the smallest lawful seam from generated V3 life into V2 mediation/expression and the only admissible route by which a V2 output may later be proposed back to V3 causality.

It is a semantic/interface contract, not a renderer implementation, V2 application implementation, V3 causal-effect implementation, physical persistence choice, or project-current authority promotion.

Working ancestry:

`d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`

Instruction/evidence ref:

`e1b9ae0bbfeea000efee65a22622196cce40aa3e`

## 1. Constitutional noncollapse

The seam SHALL preserve:

```text
OBJECTIVE_GENERATED_TRUTH
!= CAUSAL_MEMORY
!= CURRENT_ACCESSIBILITY_OR_RECALL
!= FIRST_PERSON_CLAIM_PERMISSION
!= PHENOMENOLOGICAL_PROJECTION
!= EXPRESSIVE_AFFORDANCE_OR_PLAN
!= RENDERED_EXPRESSION
!= V2_SESSION_OR_TRANSCRIPT_STATE
!= V3_CAUSAL_OCCURRENCE
!= V3_DOWNSTREAM_CAUSAL_EFFECT
```

No downstream vividness, fluency, storage, repetition, model confidence, or session continuity may widen upstream authority.

## 2. Semantic producer / owner matrix

| Layer | Semantic producer / owner | Consumer | Ownership law |
|---|---|---|---|
| objective generated facts/history | V3 generated-life causal owner | V3 replay; actor-access authority; analyst/audit | system truth does not imply actor knowledge |
| causal memory / memory transitions | V3 memory owner | V3 epistemic/access machinery | memory may causally persist without being recallable or claimable |
| actor stance / accessibility / first-person permission | V3 actor epistemic/access owner | M6 actor-safe publisher | only exact generated actor-side authority may grant first-person use |
| actor-safe publication | V3->V2 seam publisher | V2 mediation | publication is an allowlist, not a full objective record |
| phenomenological projection | separately named V2 mediation authority when present | V2 expression planning | M6 does not own positive situated phenomenology |
| expression/semantic plan | separately named admitted V2 semantic-plan authority | bounded renderer | renderer may realize but not invent semantics |
| rendered artifact | V2 render boundary | application/session; optional return-packaging lane | rendered text has no semantic or causal authority by default |
| V2 session/transcript continuity | V2 application/session owner | V2 application/audit | persistence does not create V3 memory or history |
| interaction-mode decision | separately bound V2/application mode authority | packaging eligibility | causal eligibility is not occurrence |
| return package | V2/application packaging boundary | V3 external admission court | packaging is noncausal transport only |
| external-event admission | V3 external admission owner | V3 event ledger | only ADMIT may create one occurrence |
| downstream event effects | separately governed V3 causal owners | V3 runtime | admission alone grants no memory/belief/relationship/attractor effect |

## 3. Minimum V3 -> actor-safe publication input identity

A positive actor-safe publication SHALL bind at least:

- exact `actor_id`;
- exact `as_of_causal_time`;
- exact generated-person-record state hash;
- exact actor-state hash;
- exact memory-state hash;
- exact epistemic-state hash;
- exact current actor-access authority ID/version/hash;
- exact canonical claim identity/content hash;
- exact stance-record identity;
- exact accessibility state;
- exact first-person permission class;
- exact memory refs used by the actor-side state;
- exact actor-perceived-view refs where relation/household/genealogy information is actor-facing;
- exact source transition refs;
- exact denial/defer refs for known nonrenderable claims;
- exact replay closure binding all semantic inputs and relevant causal-parent sequence;
- exact integrity/currentness result.

The reusable current implementation form is `ActorAccessibleRenderEnvelope@1.0.0` plus `ReplayClosure`.

## 4. Minimum actor-safe publication output identity

A positive output SHALL be one exact actor-safe allowlist envelope containing zero or more `ActorSafeClaimEntry@1.0.0` values.

A positive claim entry SHALL preserve:

```text
claim_ref
stance_record_ref
accessibility_state
permitted_component_refs
first_person_permission
memory_refs
actor_perceived_view_refs
source_transition_refs
entry_hash
```

The envelope SHALL preserve actor/time/source-state hashes, authority binding, exact denial refs, replay-root provenance, envelope hash, and integrity state.

Opaque audit/provenance refs MAY be carried only as opaque audit locators. They SHALL NOT become persona, belief, memory, relationship, voice, or hidden-claim authority.

## 5. Allowed first-person permission classes

The current M6 baseline recognizes positive classes equivalent to:

- `PERMIT_FIRST_PERSON_KNOWLEDGE`
- `PERMIT_FIRST_PERSON_BELIEF`
- `PERMIT_FIRST_PERSON_UNCERTAINTY`
- `PERMIT_FIRST_PERSON_NONKNOWLEDGE`

and control classes equivalent to:

- `DENY_FIRST_PERSON_CLAIM`
- `DEFER_MISSING_AUTHORITY`

No consumer may substitute a stronger class.

In particular:

```text
BELIEF -> KNOWLEDGE                 FORBIDDEN
SYSTEM_UNKNOWN -> NONKNOWLEDGE      FORBIDDEN
OBJECTIVE_TRUE -> ACTOR_KNOWS       FORBIDDEN
MEMORY_EXISTS -> CURRENT_RECALL     FORBIDDEN
CAUSAL_TRACE -> FIRST_PERSON_CLAIM  FORBIDDEN
```

## 6. Actor-safe receiver/currentness order

Before any positive V2 semantic projection:

1. validate envelope type/schema/hash/ID;
2. validate exact actor and actor-bound refs;
3. validate replay closure and its exact source-state/authority bindings;
4. compare current receiver actor/state/memory/epistemic hashes to the bound envelope snapshot;
5. fail closed on integrity mismatch;
6. fail closed on stale state;
7. honor explicit DEFER before positive entry;
8. honor explicit DENY before positive entry;
9. select at most one exact matching allowlisted claim entry;
10. if no entries exist, return valid empty;
11. if requested claim is absent from a nonempty allowlist, return no-renderable-entry.

Session/transcript claim refs are inert in this ordering and may not restore withdrawn or missing access.

## 7. Typed actor-safe ingress results

The seam SHALL preserve at least the distinctions equivalent to:

- `BLOCKED_HANDOFF_INTEGRITY_FAILURE`
- `BLOCKED_STALE_ACTOR_SAFE_HANDOFF`
- `DEFERRED_MISSING_AUTHORITY`
- `DENIED_EXPLICIT_FIRST_PERSON_CLAIM`
- `READY_PARTIAL_COMPONENT_SCOPE`
- `READY_FULL_CLAIM_SCOPE`
- `NO_RENDERABLE_ENTRY_FOR_REQUEST`
- `VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS`

These are not interchangeable.

`DENIED` does not mean false.  
`DEFERRED` does not mean actor ignorance.  
`VALID_EMPTY` does not authorize an invented generic persona response.

## 8. Mediation projection contract

The minimum semantic projection into the V2 side is an exact one-entry monotone projection equivalent to the current `ExpressionProjection`.

It SHALL bind:

- exact claim ref;
- exact permitted component refs;
- exact actor-perceived-view refs;
- exact temporal scope refs;
- exact subject scope refs;
- exact referent scope refs;
- unchanged first-person permission class;
- source actor-safe entry hash;
- deterministic projection fingerprint.

### 8.1 Monotone-narrowing permissions

V2 MAY:

- select one permitted claim entry;
- select a proper subset of permitted partial components;
- select a proper subset of permitted actor-perceived views;
- narrow temporal/subject/referent scope within the supplied ceiling;
- omit a renderable claim entirely.

V2 SHALL NOT:

- add/substitute a claim;
- join two allowed claims to infer an unlisted third claim;
- widen a partial claim to the whole;
- raise permission class;
- add an objective relationship view not present in the actor-safe entry;
- dereference opaque audit refs for behavior/persona semantics;
- infer access from transcript/session/history/keyword recurrence;
- consume PRE-V3 structural/empirical evidence as positive persona/expression authority.

## 9. Phenomenological projection / expressive-affordance boundary

M6 is only the actor-safe semantic ceiling. It does not own positive situated phenomenology or expression psychology.

Absent a separately accepted named authority, the following positive semantic classes remain:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`

- situated phenomenology;
- disclosure willingness/planning;
- salience/foreground selection;
- inhibition/suppression psychology;
- affective foregrounding;
- interlocutor-specific openness;
- psychological register/voice selection;
- response-move semantics where they would add semantic content rather than choose among already authorized variants.

A future named authority MAY consume an exact `ExpressionProjection` and emit a narrower `PhenomenologicalProjection` or `ExpressionPlan`, but it SHALL preserve the source projection fingerprint and SHALL NOT mint actor truth.

## 10. Bounded rendering contract

The reusable current renderer may produce a positive rendered artifact only when all of the following exist:

- exact current actor-safe envelope and replay closure;
- positive one-entry `ExpressionProjection`;
- exact admitted semantic render plan;
- exact accepted plan-authority binding;
- exact render-execution binding;
- one or more preauthorized wording variants bound to the exact projection;
- deterministic identity/provenance for plan, execution and selected candidate.

If any required positive plan/execution authority is absent, rendering SHALL return a typed blocked result and SHALL NOT call a model.

The bounded renderer SHALL treat model output as realization only. A renderer candidate:

- must select an admitted variant;
- must not alter claim identity;
- must not alter component/view/scope identity;
- must not raise first-person permission;
- must not invent a semantically equivalent sentence and self-certify equivalence.

A successful `RenderedExpressionArtifact` SHALL preserve:

```text
artifact_id
artifact_hash
text
variant_id
variant_hash
plan_id
plan_hash
projection_fingerprint
execution_binding_hash
semantic_authority = false
causal_occurrence = false
```

## 11. V2 session/transcript contract

V2 may own noncausal session continuity, transcript retention, render receipts, and application-local cursoring.

The following remain forbidden:

```text
TRANSCRIPT_RETENTION -> V3_MEMORY
TRANSCRIPT_DELETION -> V3_FORGETTING
SESSION_SUMMARY -> GENERATED_FACT
SESSION_SUMMARY -> RELATIONSHIP_TRUTH
PRIOR_RENDERED_TEXT -> CURRENT_CLAIM_PERMISSION
PRIOR_RENDERED_TEXT -> CAUSAL_OCCURRENCE
V2_CURSOR -> V3_EVENT_CURSOR
```

A formal V2 session close may close V2 cursor lineage only. It does not create biography, relationship truth, memory, or V3 causal advancement.

## 12. V2 -> V3 return contract

### 12.1 Constitutional default

Every successful rendered artifact is noncausal by default.

If no exact positive interaction-mode authority is supplied for the turn:

`PRESENTATION_NONCAUSAL`

is the only lawful posture.

No V3 submission occurs.

### 12.2 Causal eligibility

An explicit causal-mode receipt may make one exact rendered artifact eligible for packaging, but SHALL only establish:

`CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`

It SHALL NOT establish occurrence.

### 12.3 Minimum return-package identity

A causal candidate package SHALL bind at least:

- package schema/version/authority identity;
- immutable package ID/hash;
- exact proposal ID/hash;
- exact producer identity;
- exact subject actor ID;
- exact participant bindings;
- exact V2 session/turn/cursor provenance;
- exact interaction-mode receipt ref/hash proving causal eligibility;
- exact candidate artifact ID/hash;
- exact rendered-content hash;
- exact render receipt ref/hash;
- exact source expression-plan ref/hash;
- observable epistemic class equivalent to `V2_RENDERED_ACTOR_CANDIDATE`;
- immutable payload ref/hash resolving to the exact candidate artifact;
- exact proposed event-kind ID and exact accepted event-kind authority binding;
- exact expected V3 event cursor/history hash;
- exact causal-session ID/cursor where session-bound;
- exact provenance manifest.

The package SHALL NOT contain authoritative causal instructions such as admit/reject, state delta, memory delta, belief delta, relationship delta, attractor delta, or authoritative post-cursor.

### 12.4 Admission

Only a V3-owned external-event admission court may return:

- `ADMIT`
- `REJECT`
- `DEFER`
- `INVALID`

For the minimum return law:

```text
ADMIT:
  admitted_occurrence_count = 1
  v3_event_cursor_advance = 1
  causal_session_cursor_advance = 1 where applicable
  automatic_actor_effect = false

REJECT | DEFER | INVALID:
  admitted_occurrence_count = 0
  v3_causal_mutation_count = 0
  v3_event_cursor_advance = 0
  causal_session_cursor_advance = 0
  automatic_actor_effect = false
```

An admitted outbound expression establishes, at most, the exact external-runtime occurrence authorized by the V3 event-kind court. It does not automatically establish that the actor believed the statement before speaking, still believes it after speaking, remembered it, changed a relationship, changed position, or changed attractor state.

## 13. Replay / provenance burden

A conforming V3->V2 replay SHALL pin enough immutable material to reproduce:

- actor/time/source state;
- generated-fact refs relevant to the actor-access decision;
- exact memory objects/transitions;
- exact claim registry/content hashes;
- exact epistemic effects/transitions;
- exact permission records;
- exact owning rule IDs/versions/hashes;
- actor-state checkpoints;
- exact causal-parent sequence;
- actor-perceived-view refs;
- actor-safe entry/decision hashes;
- envelope ID/hash;
- projection fingerprint;
- exact semantic-plan ID/hash if positive rendering occurs;
- exact render-execution binding and candidate/artifact hash if rendering occurs;
- interaction-mode receipt if return eligibility occurs;
- package/proposal identity if submitted;
- V3 admission receipt and admitted event identity if `ADMIT`.

Replay SHALL NOT depend on:

- hidden wall clock;
- filesystem/list order;
- mutable `latest`/default pointers;
- unrecorded network lookup;
- transcript retention or summary as actor truth;
- prompt wording not bound to an accepted plan;
- unrecorded renderer/model randomness;
- keyword hooks as access authority;
- analyst free text.

## 14. Exact forbidden inferences

A conforming implementation SHALL reject all of the following:

```text
OBJECTIVE_GENERATED_FACT -> FIRST_PERSON_KNOWLEDGE
STRUCTURAL_OR_EMPIRICAL_PRIOR -> PERSONA_OR_VOICE
CAUSAL_PROVENANCE -> ACTOR_EXPLANATION
MEMORY_OBJECT -> ACCESSIBLE_RECALL
SYSTEM_UNKNOWN -> ACTOR_NONKNOWLEDGE
ACCESSIBLE_MEMORY -> KNOWLEDGE_WITHOUT_STANCE_AUTHORITY
ANALYST_MISRECOGNITION -> ACTOR_META_KNOWLEDGE
TWO_PERMITTED_CLAIMS -> UNLISTED_JOINED_CLAIM
OPAQUE_PROVENANCE -> EXTRA_PERSONA_FACT
STALE_ENVELOPE -> CURRENT_RENDER_PERMISSION
TRANSCRIPT_TEXT -> CURRENT_ACCESS
RENDERED_TEXT -> PREEXISTING_BELIEF
RENDERED_TEXT -> V3_EVENT
CAUSAL_MODE -> ADMISSION
PACKAGING -> OCCURRENCE
ADMISSION -> ACTOR_EFFECT
RERENDER_TEXT_EQUALITY -> PRIOR_ADMISSION
```

## 15. Existing reusable implementation/tests

Primary direct reuse:

- `rawlsing_next/m6_actor_safe_expression.py`
- `rawlsing_next/tests/test_m6_actor_safe_expression.py`
- `rawlsing_next/render_bounded_expression.py`
- `rawlsing_next/tests/test_render_bounded_expression.py`

Important current/recovered exact contract precedents:

- `.../schematics/boundaries/S07_V3_TO_V2.md`
- `.../W0_AUTHORITY_FOUNDATION/ADP_017_V3_ACTOR_ACCESS/AUTHORITY.md`
- `.../W0_AUTHORITY_FOUNDATION/ADP_019_V3_EXTERNAL_ADMISSION/AUTHORITY.md`
- `.../W0_AUTHORITY_FOUNDATION/ADP_024_V2_TRANSCRIPT_POLICY/AUTHORITY.md`
- `.../W0_AUTHORITY_FOUNDATION/ADP_025_V2_RENDER_POLICY/AUTHORITY.md`
- `.../W2_AUTHORITY_CONTRACT_COMPLETION/CAN_024_V2_INTERACTION_MODE/AUTHORITY.md`
- `.../W2_AUTHORITY_CONTRACT_COMPLETION/CAN_025_V2_TO_V3_EXTERNAL_EVENT_PACKAGING/AUTHORITY.md`

Presence of a historical/recovered authority file is not by itself a P2 current-selection ruling. Where the current PRE-MAIN authority index does not select the object, central integration must bind the exact authority before positive use.

## 16. Exact open gates

The seam is constitutionally complete but positive execution remains gated where repository authority is intentionally absent or not current-selected:

1. **GATE-G01 — positive situated phenomenology / semantic expression-plan owner**  
   Current behavior: `BLOCKED_NAMED_AUTHORITY_REQUIRED`.

2. **GATE-G02 — exact governed render-execution binding**  
   The renderer requires exact policy/renderer/variability identity; mutable/default model selection is forbidden.

3. **GATE-G03 — exact current interaction-mode authority binding for causal eligibility**  
   Otherwise default presentation/noncausal.

4. **GATE-G04 — exact current V2->V3 packaging binding / implementation**  
   No prose-to-package inference.

5. **GATE-G05 — exact current V3 external-admission binding / physical wiring**  
   Presence of a recovered authority document is not equivalent to installed current execution.

6. **GATE-G06 — exact proposed event-kind authority when causal return is requested**  
   No generic conversation-event fallback.

7. **GATE-G07 — separately governed downstream V3 effect authority after ADMIT**  
   Admission does not supply memory/belief/relationship/attractor effects.

8. **GATE-G08 — per-request currentness/replay integrity**  
   Stale/missing/mismatched actor-safe state blocks positive semantics.

## 17. Minimal GT0-compatible path

A lawful GT0 instance may use the blocked/empty path:

```text
V3 exact actor snapshot
-> replay-closed actor-safe envelope
-> exact requested claim
-> positive one-entry projection OR valid-empty/deny/defer
-> no named positive V2 semantic-plan authority
-> BLOCKED_NAMED_AUTHORITY_REQUIRED
-> no model call
-> no rendered semantic output
-> no V3 mutation
```

This proves semantic conservation and the V3/V2 jurisdiction boundary.

A later positive GT0 continuation is valid only after the named open gates are positively bound and may then follow:

```text
positive projection
-> admitted plan
-> bounded noncausal render
-> presentation-only stop
OR
-> explicit causal-mode receipt
-> exact candidate package
-> V3 admission
-> one occurrence on ADMIT
-> separately governed effects only
```

## 18. Required acceptance invariants

At minimum, future implementation/integration tests SHALL prove:

1. objective fact without actor epistemic authority does not render as first-person knowledge;
2. structural/PSEPF/comparator/provenance sources are rejected as persona/expression authority;
3. stale actor-safe envelope blocks;
4. session transcript cannot restore withdrawn access;
5. valid empty produces no model call;
6. DENY and DEFER produce no model call;
7. partial access cannot widen to whole claim;
8. actor-perceived relationship scope cannot widen to objective relationship truth;
9. permission class cannot be upgraded;
10. two allowed claims cannot be joined into a third;
11. positive rendering blocks without exact named semantic-plan authority;
12. a successful render artifact remains nonsemantic and noncausal;
13. presentation mode never submits to V3;
14. causal mode creates eligibility only;
15. REJECT/DEFER/INVALID produce zero V3 mutation;
16. ADMIT creates exactly one occurrence and no automatic actor effect;
17. rerender/new artifact identity requires a new admission decision;
18. transcript/session persistence remains disjoint from V3 memory/history.

Terminal readiness:

`PASS__WSC001G_V3_V2_MEDIATION_CONTRACT_CONSTITUTED__READY_FOR_CENTRAL_FANIN`
