# SYN02-D / 03 — state, source, transaction and dynamic functional-organization interfaces

**Status:** `ARCHITECTURE_CONTRACT / SPECIFICATION_ONLY / NO IMPLEMENTATION / NO NATIVE RULE`.
**Purpose:** define durable/transient state, source rights, atomic event/batch semantics and a sparse evolving functional-organization representation without selecting a scientific learning law, graph engine or neural simulator.
**Sealed startup:** `cd1f4fd8158c2771d7c565b06ee397a7a60dc779`.

---

## 0. Non-negotiable separation

The runtime must keep these jurisdictions distinct:

| Record | What it is | Who may write | What it cannot be |
|---|---|---|---|
| `CanonicalWorldEvent` | objective occurrence with owner/source/clock/parents | C8/world owner | actor feeling, motive or memory |
| `ActorAccessRecord` | actor-local ability to receive/recall an occurrence | ADP017/access owner | objective occurrence or narrator knowledge |
| `ActorImpression` | actor-relative immediate relevance/response | C9/CAN008 | durable belief or story |
| `C9Response` | immediate response/NO_CHANGE/HELD record | C9/CAN008 rule | CAN011 durability |
| `DurableDecision` | CAN011 target/operation/relation/NO_CHANGE | CAN011 owner | renderer text |
| `ActorMemoryTrace/Episode` | fallible actor-owned memory | ADP016/ADP017 | objective event copy or analyst history |
| `ReflectiveAct` | SCI05-admitted internal act | SCI05/CAN owner | unadmitted `self_account` text |
| `FunctionalRelation` | condition-scoped causal/functional organization | CAN/ADP/science owner | free graph edge or automatic Hebbian update |
| `RenderedSurface` | expression/projection only | V2/renderer | causal state or memory |
| `DerivedView` | recomputable view | architecture | stored causal truth |

No renderer may write a durable state, access record, memory or relation.

---

## 1. Actor and world state

### 1.1 `ActorStateVersion`

```text
ActorStateVersion {
  actor_id: ActorId;
  version: uint64;
  parent_version: StateVersionRef | ROOT;
  branch_id: BranchId;
  clock: LogicalClock;
  world_version: WorldVersionRef;
  event_prefix_hash: ContentHash;
  memory_version: MemoryVersionRef;
  functional_org_version: FunctionalOrgVersionRef;
  derived_view_version: DerivedViewVersionRef;
  state_hash: ContentHash;        // excludes rendered surface
  provenance: StateProvenance;
  status: ACTIVE | SUPERSEDED | HELD | RETIRED;
}
```

The **event prefix hash** is the ordered identity of canonical events that actually changed this actor state. A state version without a committed event/readset is invalid. `rendered_output` is not part of `state_hash`.

### 1.2 State layers

```text
PersonState {
  identity: ActorIdentityRef;
  material: MaterialState;            // actual resources/time/housing/health function
  needs: NeedState;                   // owned, source-qualified
  practices: PracticeState;           // actual acquired operations
  expectations: ExpectationState;     // scoped, evidence-bearing
  relations: RelationState;           // external actors/ties, not labels
  functional_organization: FunctionalOrganizationVersion;
  memory: MemoryState;                // ADP016 traces/episodes
  access: ActorAccessState;           // ADP017
  claims: SelfClaimState;             // ADP017/SCI05, not objective history
  metadata: {
    source_refs; rule_versions; uncertainty; unknown_fields;
    state_schema_version; migration_ref;
  };
}
```

`unknown_fields` is explicit. Unknown is **not** 0/50/100 and not an absent relation.

### 1.3 World state version

```text
WorldVersion {
  world_id: WorldId;
  version: uint64;
  clock: LogicalClock;
  event_prefix_hash: ContentHash;
  objective_facts_ref: ContentHash;
  source_authority_refs: AuthorityRef[];
  status: ACTIVE | SUPERSEDED | HELD;
}
```

A world event updates a world version and creates an event record. It does not directly update a person. The actor path goes through access, C9 and CAN011.

---

## 2. Canonical event and provenance records

### 2.1 World event

```text
CanonicalWorldEvent {
  event_id: CanonicalEventId;       // deterministic, not model-local
  world_id: WorldId;
  clock: LogicalClock;
  event_kind: EventKindRef;
  participants: ActorRef[];
  owner: SourceOwnerRef;
  source_ref: SourceRef;
  source_hash: ContentHash;
  location_ref?: LocationRef;
  payload: TypedPayload;            // no private psyche
  parents: CanonicalEventId[];
  admission_grade: SOURCE_QUALIFIED | TEST_ONLY | HELD;
  rule_or_permission_refs: RuleRef[];
  content_hash: ContentHash;
}
```

### 2.2 Actor access / impression / response

```text
ActorAccessRecord {
  access_id; actor_id; event_id; clock;
  status: ACCESSIBLE | PARTIAL | NOT_WITNESSED | DISTORTED | REVOKED;
  scene_ref; channel; source_refs[]; evidence_hash;
}

ActorImpression {
  impression_id; actor_id; event_id; access_id;
  immediate_relevance_ref; response_ref;
  source_rule_ref; access_scope; created_clock;
}

C9Response {
  response_id; actor_id; event_id; impression_id;
  status: RESPONSE_COMMITTED | NO_CHANGE | HELD_MISSING_RULE | DENIED;
  response_kind; target_proposals[];
  rule_id/version/hash; evidence_refs[];
  no_ghost: bool;
}
```

A world event with `NOT_WITNESSED` access may persist objectively; the actor has no impression, response or durable change. A model may not reconstruct the missing access.

### 2.3 Durable decision

```text
DurableDecision {
  decision_id; actor_id; event_id; response_id;
  rule_id/version/hash; owner_ref;
  branch: CREATE | TRANSFORM | MAINTAIN | SUSPEND | NO_CHANGE | HELD;
  target_ref?: OperationRef | PracticeRef | RelationRef | MemoryRef;
  before_state_hash; after_state_hash;
  parents: CanonicalEventId[];
  permission_ref?;
  no_change_reason?;
  content_hash;
}
```

`NO_CHANGE` is a positive typed decision. `HELD_MISSING_RULE` is not a no-change. `SUSPEND` and `MAINTAIN` are distinct from `NO_CHANGE`; the owner must issue their semantics.

### 2.4 Canonical ledger

One append-only ledger holds all of:

- world events;
- actor access/response/durable decisions;
- intervals/activity receipts;
- memory admission;
- reflective acts;
- batch receipts.

Actor-specific views are projections, not duplicate ledgers. The old C12 `episode`/`world_event`/`perception` tables can be reused as storage primitives, but a new `ActorStateVersion`, `FunctionalOrganizationVersion`, `Batch`, `Memory` and `Transaction` layer is required.

---

## 3. Atomic transaction model

### 3.1 Unit of work per event

A single event transaction uses a **working copy** of the affected state views:

```text
BEGIN
  read stable ActorStateVersion/WorldVersion
  validate source owner and event identity
  validate actor access
  evaluate immediate C9 rule
  evaluate durable CAN011/no-change/held
  evaluate interval after event
  stage:
    canonical event
    access/impression/response/durable
    actor state delta + new state version
    memory/access records
    batch/local receipt
    ledger entry/outbox
  verify no-ghost/hash/dependencies
COMMIT
```

No external provider call occurs inside the transaction. No renderer runs inside it. No partial row is visible after failure.

### 3.2 Failure matrix

| Failure | World event | Actor access | Actor state | Durable decision | Render | Consumer outcome |
|---|---|---|---|---|---|---|
| precondition unmet | none | none | unchanged | none | none | `PRECONDITION_UNMET` |
| source/coactor denied | none | none | unchanged | none | none | `SOURCE_HELD`/`COACTOR_HELD` |
| source event exists but access absent | may persist | `NOT_WITNESSED` | unchanged | none | none | `ACCESS_NOT_RECEIVED` |
| CAN008 rule absent | persists if admitted | persists | unchanged | `HELD_MISSING_RULE` | surface may render no scene | `RULE_HELD` |
| CAN011 rule absent | persists | persists | unchanged | `HELD_MISSING_RULE` | no causal write | `RULE_HELD` |
| CAN011 lawful no-change | persists | persists | new version with no-change record | `NO_CHANGE` | surface only | `NO_CHANGE` |
| interval missing | persists | persists | prefix version | prior decision | none | `INTERVAL_HELD`; suffix held |
| transaction failure | rolled back | rolled back | rolled back | rolled back | none | typed rollback |
| render failure after commit | committed | committed | committed | committed | `RENDER_FAILED` | not “applied clean”; no state rewrite |
| batch suffix failure | prefix committed | prefix | prefix | prefix | prefix surface | `PREFIX_COMMITTED` |

The render is deliberately **out-of-band** after state commit. A failed render must not be reported as an applied-and-clean event; it also must not uncommit a real world/actor event. This corrects the old Pass2 failure/no-rollback ambiguity.

### 3.3 Batch transaction policies

- **`PREFIX_CONTIGUOUS`**: commit each realized event atomically; first unresolved stops the suffix. This is the recommended external-world policy.
- **`INDEPENDENT_SUFFIX`**: only with explicit owner gap semantics; commit independent realized events after a gap.
- **`WHOLE_BATCH_ATOMIC`**: stage all events and commit together. Only for a contained world where no external B action has already occurred; an external action is not rollbackable and cannot be represented as if it were.

The batch policy is a C9/C12 owner decision, not a SYN02-D self-issued rule.

### 3.4 Replay, idempotency and randomness

- Every event/turn has deterministic identity from actor, branch, source hash, clock, parent state, rule version and action ordinal.
- Replaying the same identity must return the same event/state/response; duplicate different content is refused.
- Any randomness is an explicit `RngReceipt` with algorithm, seed/source, stream, scope and draw coordinates; unseeded `random` is forbidden in durable formation.
- S44's `ADP-020@1.0.0` RNG is a candidate reuse for root sampling, not a license for developmental randomness.
- A transport retry is not a new semantic call; dispatch identity and `PENDING_UNKNOWN` semantics must be preserved.
- Derived views carry `source_state_hash` and recompute on load; stale cache is a typed condition, never a hidden truth.

### 3.5 Batch receipt

```text
BatchReceipt {
  batch_id; policy;
  committed_prefix: CanonicalEventId[];
  unresolved_suffix: {
    proposal_id; status; fault_code; reason;
  }[];
  actor_state_before; actor_state_after;
  world_version_before; world_version_after;
  transaction_ids: ContentHash[];
  render_status: COMPLETE | RENDER_FAILED | NOT_REQUESTED;
  no_ghost: bool;
  commit_hash;
}
```

The receipt is the authority for what happened, what did not happen and what remains unresolved. The retrospective packet is built from `committed_prefix` plus access records, not from the proposal text.

---

## 4. Dynamic functional organization

### 4.1 What is being represented

Not a permanent all-to-all graph and not a synapse simulator. The representable claim is:

> A particular actor history may change which operations recruit, inhibit, cooperate with or recontextualize which other operations under a bounded scope, or may change only a state value, or may leave a lawful no-change.

The architecture must support the **candidate** that such functional connections are acquired, without adopting a numeric Hebbian law.

### 4.2 `FunctionalOrganizationVersion`

```text
FunctionalOrganizationVersion {
  actor_id: ActorId;
  version: uint64;
  parent_version: FunctionalOrgVersionRef | ROOT;
  state_version: StateVersionRef;
  relations: FunctionalRelation[];    // canonical immutable records
  status: ACTIVE | SUPERSEDED;
  source_refs[]; rule_versions[]; content_hash;
}
```

A sparse store is canonical; a materialized adjacency view is optional. No dense `N_operations × N_operations` matrix is required.

### 4.3 `FunctionalRelation`

```text
FunctionalRelation {
  relation_id: RelationId;
  actor_id: ActorId;
  version: uint64;
  source_operation: OperationRef;
  target_operation: OperationRef;
  relation_mode: RECRUITS | INHIBITS | COOPERATES | RECONTEXTUALIZES
               | ENABLES | BLOCKS;
  scope: {
    domain_refs[]; object_refs[]; relation_refs[]; activity_refs[];
    context_predicate: ConditionExpr;   // source-qualified
    audience_or_access?: AccessScope;
  };
  activation: {
    mode: CONDITIONAL | CONSTITUTIVE;
    required_evidence_refs[];
    support_dependence: SUPPORTED | INDEPENDENT | UNKNOWN;
    inhibition_sources[];
  };
  origin: {
    event_refs: CanonicalEventId[];
    practice_refs[]; relation_history_refs[]; memory_refs[];
    formation_rule_ref?: RuleRef;
    coactivation_evidence_refs[];
  };
  evidence: {
    source_grade; positive_refs[]; contrary_refs[]; uncertainty;
  };
  status: CANDIDATE | ADMITTED | CONTESTED | SUSPENDED | RETIRED;
  valid_from: LogicalClock;
  valid_until?: LogicalClock;
  supersedes?: RelationId;
  owner: SourceOwnerRef | ScienceOwnerRef;
  content_hash: ContentHash;
}
```

No free numeric weight is required or authorized. If a specific science owner later issues a quantitative relation, it must be a versioned value with source and scope; the architecture must not smuggle a default coefficient.

### 4.4 Operation and activation records

```text
Operation {
  operation_id: OperationId;
  kind: OperationKind;
  input_refs[]; output_ref;
  preconditions: ConditionExpr[];
  value_semantics_ref;
  owner; rule_version;
}
```

```text
FunctionalActivationTrace {
  trace_id;
  actor_id; state_version; event_id; access_id;
  query_scope: ConditionExpr;
  candidate_relations: RelationId[];
  matched_relations: RelationId[];
  recruitment_paths: RecruitmentPath[];
  inhibited_relations: RelationId[];
  proposed_operations: OperationId[];
  outcome: RECRUITED | NO_ACTIVATION | CONFLICT | HELD;
  source_refs[]; content_hash;
}
```

An activation trace is **transient**. It does not create a relation merely because two operations co-occurred. A durable relation requires a `RelationFormationDecision` from the competent owner.

### 4.5 Formation decision

```text
RelationFormationDecision {
  decision_id;
  actor_id; state_version;
  relation_candidate: FunctionalRelation;
  operation: CREATE | CHANGE | SUSPEND | RETIRE | NO_CHANGE | HELD;
  basis: {
    realized_event_refs[]; actual_activity_refs[];
    coactivation_evidence_refs[];
    support_change_refs?; contrary_evidence_refs[];
  };
  rule_ref; owner; permission_ref?;
  before_org_version; after_org_version?;
  no_change_reason?;
  content_hash;
}
```

`CoActivationEvidence` is only candidate evidence:

```text
CoActivationEvidence {
  evidence_id; actor_id; source_op; target_op;
  observed_event_refs[]; contexts[]; repetition_count_bucket;
  contrary_refs[]; source_grade; uncertainty;
}
```

No architecture-level threshold or automatic update. Co-occurrence is not formation; correlation, shared context, external support and selection are rival explanations.

### 4.6 Distinctions the store must preserve

| Claim | Stored as | Not |
|---|---|---|
| state value changed | `ActorStateVersion` delta | new relation |
| temporary coactivation | `FunctionalActivationTrace` | durable relation |
| new operation/skill | `PracticeState`/`Operation` with evidence | edge weight |
| new functional relation | `FunctionalRelation` + decision | scalar update only |
| external support changed | world/B/resource record | actor learning |
| increased capacity to learn | meta-capability record under owner | automatic edge |
| no effect | `NO_CHANGE` decision | missing row |

### 4.7 Recruitment interface

```text
query_active_relations(
  actor_id, state_version, event_id, access_scope, context_expr
) -> FunctionalRelation[];

activate_functional_organization(
  actor_id, state_version, event_id, access_id, candidate_operations
) -> FunctionalActivationTrace;

decide_relation_formation(
  actor_id, candidate, basis, rule, owner, permission
) -> RelationFormationDecision;
```

`query_active_relations` returns semantic relation records by value, not just edge IDs/hashes. The C9 consumer must read the relation’s mode/scope/evidence, not merely observe that a state hash changed.

### 4.8 Sparse storage and stage cost

Canonical storage: one row/record per relation version, not an all-to-all matrix.

Indexes:

```text
(actor_id, status, valid_from/until)
(actor_id, source_operation, scope_domain)
(actor_id, target_operation, scope_domain)
(actor_id, origin.event_ref)
```

Query plan: filter by actor + current version + scope before retrieving relations; per event evaluate `m` scope-local relations, not all `E` historical relations.

Budget:

- relation record ≈ 0.5–2 KB serialized;
- active relations per actor/scope capped by an owner-set `max_active_relations`;
- inactive/retired relations archived; snapshots at meaningful boundaries (stage/year/batch) and delta journals between;
- expected operational complexity `O(log E + m)` for indexed retrieval plus small `m` activation evaluation; never `O(E_all²)`;
- no GPU or neural simulation requirement;
- if active relations grow beyond a measured budget, split by domain/scope and snapshot; do not silently truncate without a `HELD`/`BUDGET` record.

At different life stages, stage/domain scopes change; the store supports a wider adult scope without preallocating adult density in infancy. Empty/unknown is represented as no active relation plus `unknown_fields`, not as a fabricated edge.

---

## 5. Source, permission and owner binding

Every durable write carries:

```text
SourceBinding {
  source_owner: SourceOwnerRef;
  source_ref: SourceRef;
  source_hash: ContentHash;
  authority_refs: AuthorityRef[];
  rule_ref: RuleRef;
  permission_ref?: PermissionRef;
  effective_clock: LogicalClock;
  admission_grade: SOURCE_QUALIFIED | TEST_ONLY | HELD;
}
```

Rules:

- C0/Pyat world/possibility facts cannot become actor state without C8/C9/ADP/CAN processing.
- C11 source permission and Pyat N11/N12 are separate from C12 runtime readiness.
- A source owner cannot be synthesized from a generic world callback, model premise or caller boolean.
- Test-only sources are labeled and cannot be promoted by a green test.
- A missing source/rule/access is recorded as `HELD`/`PERMISSION_REQUIRED`; it is not zero, no-change, or a default relation.

---

## 6. Interface boundaries: existing and new

### 6.1 Reuse as-is (no production edit in SYN02-D)

| Existing API | Use | Limit |
|---|---|---|
| `candidate.pipeline.run_candidate_path` | C9 ingress/conditioning/response/target transaction/later E2 | production Rule A/T registries empty |
| `CandidateStore` | atomic occurrence/response/target SQLite transaction | local test store; not actor-state ledger |
| `S37TargetlessProduct` / `QualifiedC12Store` | C12 episode/world/perception/checkpoint substrate | targetless; no native |
| `S42Session.admit_event` | sequential single-event seam | one event; no batch/retrospective |
| `S46Session.produce_interval` | actual interval/activity receipt | workshop-scoped |
| `S47Session._extra_conditioning_sources` | material conditioner readset | no learned relation |
| `S48Session.run_turn` | one-call transport/dispatch/cache | one prospective; no SCI05 admission |
| `S49Session.produce_b_turn` | B owner adapter | root B source empty; controlled only |
| `S44Session.generate_root` | sampled antecedent root | synthetic/TEST_ONLY |
| `S45Session` | user SAY/DO/HELP/ATTEND | test-only |
| `pre553_*` / possibility modules | C0/C11 services | no C12 consumer |

### 6.2 New modules to create

| Proposed module/API | Input → output | First actual consumer |
|---|---|---|
| `ActorRuntimeStore` | actor state version + delta → durable version/read | C9/C12, batch |
| `CanonicalEventLedger` | world/access/response/durable/interval records → ordered ledger | batch, replay, retrospective |
| `FunctionalOrganizationStore` | relation versions + scope index → active relations | C9 activation |
| `BatchOrchestrator` | `ProspectiveBatch` + sources → `BatchRealization`/receipt | C12 turn |
| `RetrospectivePackager` | realized prefix + access records → model-visible packet | N+1 call |
| `SCI05DependencyValidator` | output self-account + proposals → admissions/invalidations | batch admission |
| `SourceRegistry` | branch/source/owner refs → resolved source handles | all runtime |
| `ProductTransport` | prompt/envelope → one call/replay | S48-style transport |
| `ActorMemoryStore` | ADP016/017 records → traces/episodes | retrospective |
| `C11WorldAdapter` | C0/C11 query/result → world/possibility source records | C4/C8 |
| `RenderAttemptStore` | state version + render result → render status | V2 surface |

These are design names, not implemented code. No production source was edited.

---

## 7. Invariants and falsifiers

1. **No ghost state.** A failed transaction leaves no event, access, response, durable, batch or state row.
2. **No state without source.** Every durable actor/world/relation state has a source/resolution/rule/permission chain.
3. **No access = no impression.** An objective event can exist without actor state.
4. **No rule = held, not no-change.**
5. **No text = no hidden state.** `self_account`, retrospective text and rendered prose are not durable state.
6. **No renderer causality.** Render failure is `RENDER_FAILED`, not applied-clean; renderer cannot write actor state.
7. **No all-to-all relation soup.** Sparse indexed relation records; no universal coactivation update.
8. **No auto-Hebbian.** Coactivation is candidate evidence; a competent owner must issue formation.
9. **No default B.** Missing B source -> `SOURCE_OWNER_HOLD`; controlled `PRIOR_B_REFUSAL` remains labeled.
10. **No unrevealed suffix leakage.** Retrospective packet includes only actor-accessible prefix.
11. **No unseeded durable randomness.** RNG receipts and replay identity are mandatory.
12. **No stale derived truth.** Derived views recompute or fail closed.

A source-edge fault must change the named downstream assertion: remove the actor access record, the later C9 semantic read must change or fail; remove the formed relation, the later operation/response must change or hold; remove the B source, the event must not become a default refusal; remove the render output, state must not change.

---

## 8. Migration and scope

The existing S37/C12 store can be migrated by additive tables/views, not by overwriting historical rows:

- preserve `episode`, `world_event`, `perception`, `checkpoint` and hashes;
- add `actor_state_version`, `access_record`, `impression`, `c9_response`, `durable_decision`, `memory_*`, `functional_relation`, `activation_trace`, `batch`, `transaction`, `render_attempt`;
- map existing test-only episodes to `TEST_ONLY` source grade;
- never infer native state from test-only rows;
- keep old C12 verifier and add new actor/ledger verifiers; do not make the old verifier the new truth.

A production migration is not authorized by SYN02-D. It is a design and owner-review target.
