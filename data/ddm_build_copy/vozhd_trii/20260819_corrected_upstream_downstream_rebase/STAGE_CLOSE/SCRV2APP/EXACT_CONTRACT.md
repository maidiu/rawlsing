# SCRV2APP EXACT CONTRACT

**Contract ID:** `SCRV2APP_EXPRESSION_FIREWALL@1.0.0`  
**Scope:** V2/application actor-safe expression receiver, prompt/render firewall, noncausal session boundary, and V2→V3 external-event prerequisite boundary.  
**Final positive sender seam:** externally owned by SCRV3 and intentionally not fabricated here.

## 1. Type classes

### 1.1 Actor-safe positive semantic input

`ACTOR_SAFE_V3_ENTRY` means an entry emitted by the final accepted SCRV3 actor-safe handoff and carrying exact V3 actor-accessibility/claim permission. Until M6, the final schema/type identity and hash are an unresolved external parameter.

Current accepted ADP-017 `ActorAccessibleRenderEnvelope@1.0.0` is the binding semantic precedent: actor, causal-time/state binding, actor-safe claim entries, explicit denials, opaque provenance, integrity, exact accessibility, component scope, and first-person permission.

### 1.2 Forbidden behavioral upstream classes

`FORBIDDEN_UPSTREAM_BEHAVIORAL_SOURCE` is any of:

`PSEPF | ActorComparatorReceipt | SourceDisagreementOrEmpiricalNegativeAsSuch | V3EmpiricalPossibilityInput | ResolvedStructuralContext | StructuralPriorRepository | V557/V558 object/locator/index/SelectionRecord | raw V553/V554/V555/V556 structural object | ReplayReceipt | opaque upstream audit/provenance object/ref`.

These classes may be reachable for separately authorized audit/replay, but are never V2/application expression authority.

### 1.3 V2-owned noncausal inputs

Separately governed V2 inputs may include final actor-safe semantic entries, current-turn stimulus, caller current-situation authority, interaction-mode authority, V2 session/presentation state, and accepted V2 expression-policy outputs. Their presence does not relax the upstream-prior firewall.

## 2. Ingress predicate

For any candidate semantic input `x` to V2/application behavioral computation:

```text
ALLOW_BEHAVIORAL_SEMANTIC_INPUT(x) :=
    IS_CURRENT_ACTOR_SAFE_V3_ENTRY(x)
    OR IS_SEPARATELY_GOVERNED_V2_NONCAUSAL_INPUT(x)
```

subject to role-specific constraints below.

```text
IF IS_FORBIDDEN_UPSTREAM_BEHAVIORAL_SOURCE(x)
THEN behavioral_use(x) = DENY
```

No wrapper, alias, hash, locator, serialization, summary, embedding, retrieval result, tool result, cache key, feature vector, model-visible prose, or copied field changes that classification.

## 3. Direct and indirect nonconsumption

For every forbidden upstream source `u`, the following operations are forbidden if their result can influence any behavioral or semantic V2/application decision:

```text
read_payload(u)
dereference(u)
parse(u)
join(u, *)
summarize(u)
rank_or_score(u)
embed(u)
semantic_search(u)
retrieve_augmented_content(u)
classify(u)
feature_extract(u)
branch_on_value_or_metadata(u)
insert_into_prompt(u)
select_expression_operation(u)
select_salience(u)
select_register_or_voice(u)
select_response_move(u)
infer_relationship(u)
infer_epistemic_state(u)
infer_confidence_or_uncertainty(u)
use_as_behavior_affecting_cache_or_partition_key(u)
```

Audit-only integrity checking is not behavioral use when its only outcomes are audit success/failure, integrity block, or provenance recording and no semantic payload/value/metadata flows back into expression computation.

## 4. Opaque provenance exact law

Every upstream provenance member crossing the actor-safe membrane must be typed as:

`AUDIT_ONLY_REF`

with semantic role:

`AUDIT_ONLY__NON_RENDER__NON_PERSONA__NON_BEHAVIORAL__NON_DEREFERENCEABLE`

Allowed operations:

1. carry immutable ref/id/hash;
2. compare exact expected ID/hash for integrity;
3. omit;
4. forward unchanged to an explicitly audit-only sink.

Forbidden operations:

1. model/prompt visibility;
2. behavioral dereference;
3. lookup-based augmentation;
4. embeddings/similarity/ranking;
5. parsing filenames, labels, paths, IDs, source names, lengths, ordering, presence patterns, or hash prefixes for expression features;
6. use in persona/voice/register/salience/response/relationship/epistemic selection;
7. use in a cache/routing/partition decision that changes behavioral output;
8. conversion of successful provenance verification into actor knowledge or claim permission.

Unknown role, missing provenance-role authority, unexpected provenance class, or integrity mismatch => fail closed.

## 5. Actor-safe V3 receiver predicate

The final SCRV3 handoff is acceptable to SCRV2APP only if all of these are machine-provable:

1. exact handoff schema/type identity, version, authority/hash, and integrity binding are immutable and verifiable;
2. exact actor identity and V3 state/effective-time/currentness binding are present;
3. every renderable claim/view is explicitly actor-accessible under a V3-owned rule;
4. every entry identifies exact permitted claim/components and exact first-person/epistemic permission;
5. denied/withheld/analyst-only content cannot be recovered through the V2-facing semantic lane;
6. relationship expression receives actor-perceived/actor-accessible views, not hidden objective relationship truth;
7. provenance exposed across the seam is audit-only and behaviorally opaque;
8. raw PSEPF, comparator receipts, source disagreement, V3 empirical input, structural context/repository objects, and upstream priors are absent from the model-visible/behavioral semantic projection;
9. stale or integrity-failed handoff is explicitly detectable and fails closed;
10. downstream V2 narrowing can be proven against the exact source handoff snapshot.

The exact sender field names/type/hash are SCRV3-owned and remain the sole final-seam dependency.

## 6. V2 monotone permission transform

Let `A` be the set of actor-safe V3 entries for one exact handoff snapshot and `O` the semantic units V2 proposes to render.

V2 must prove:

```text
claims(O) ⊆ claims(A)
components(O,c) ⊆ permitted_components(A,c)
temporal_scope(O,c) ⊆ temporal_scope(A,c)
subject_scope(O,c) ⊆ subject_scope(A,c)
relationship_view_scope(O,c) ⊆ actor_permitted_view_scope(A,c)
referent_scope(O,c) ⊆ referent_scope(A,c)
permission_class(O,c) = permission_class(A,c)
```

where equality on permission class means V2 may not transform `BELIEF` into `KNOWLEDGE`, `UNCERTAINTY` into `BELIEF`, system unknown into actor `NONKNOWLEDGE`, or any other stance/first-person class substitution. V2 narrows through omission, exact component selection, exact scope restriction, and separately authorized wording/expression choices—not by re-authoring actor epistemics.

Forbidden:

```text
infer_hidden_claim_from_join(A[i], A[j])
restore_removed_or_inaccessible_claim_from_session()
use_objective_truth_to_upgrade_permission()
use_upstream_provenance_to_upgrade_permission()
use_current_user_turn_to_create_preexisting_actor_truth()
```

## 7. Prompt/render visibility classes

Every prompt input must be assigned exactly one class:

- `MODEL_VISIBLE_AUTHORITATIVE_SEMANTIC` — exact V2 renderable unit descended from current actor-safe V3 entry and separately governed V2 semantic decision;
- `MODEL_VISIBLE_STIMULUS_ONLY_NONAUTHORITATIVE` — exact current-turn stimulus where accepted V2 authority permits it;
- `AUDIT_ONLY_NEVER_MODEL_VISIBLE` — provenance, authority manifests, opaque refs, denied/withheld material, replay data, structural/empirical upstream refs;
- `OMITTED_DENIED` — forbidden or unavailable material.

Unknown visibility class => block render admission.

The renderer/model may vary wording only within the admitted semantic plan. Model output cannot add semantic authority. Post-render validation must reject/repair any unlisted claim, permission escalation, hidden analyst truth, provenance leakage, relationship-truth widening, or invented biography/persona.

## 8. Noninterference oracle

With actor-safe handoff semantics, V2-owned lawful inputs, user-turn stimulus, interaction-mode inputs, and render policy/RNG receipts held fixed:

```text
change(forbidden_upstream_prior_or_opaque_provenance)
=> no change in behavioral/semantic V2 or application output
```

Permitted difference: audit-only records and integrity outcomes that block output.

A provenance change that changes tone, register, salience, response move, claim set, prompt-visible content, relationship expression, interaction mode, or causal packaging eligibility is a contract failure.

## 9. Session/application law

`V2_SESSION_STATE`, transcript, summary, render receipt, application metadata, and presentation state are noncausal.

They may support presentation continuity only under their accepted V2 authorities. They are not generated actor memory, knowledge, belief, relationship history, biography, or causal occurrence.

A stale/missing V3 actor-safe handoff cannot be repaired from session state, prior rendered text, user reminder, keyword retrieval, or opaque provenance.

## 10. Interaction-mode and causal-feedback law

Default posture is `PRESENTATION_NONCAUSAL` unless exact accepted interaction-mode authority establishes `IN_WORLD_CAUSAL`.

### Presentation noncausal

Rendered artifact may display/persist noncausally. It is not a V3 event and has no causal mutation.

### In-world causal

The exact outbound artifact is initially:

`CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`

It may be packaged only under the exact accepted V2→V3 packaging contract. The package is a prerequisite proposal, not an occurrence or effect.

Only ADP-019 decides:

`ADMIT | REJECT | DEFER | INVALID`.

Truth table:

| ADP-019 result | V3 occurrence | V3 state mutation by V2/package | event cursor | causal-session cursor | downstream actor effects |
|---|---|---|---|---|---|
| `ADMIT` | exactly one admitted external occurrence | none by V2/package; ADP-019 appends occurrence | advance exactly as ADP-019 owns | advance exactly as ADP-019 owns when applicable | none implied; separate V3 owners required |
| `REJECT` | none | zero | zero | zero | zero |
| `DEFER` | none | zero | zero | zero | zero |
| `INVALID` | none | zero | zero | zero | zero |

Terminal rejected artifact cannot be re-proposed under a new proposal ID to evade rejection. A rerender is a distinct candidate and receives no inherited admission. A deferred immutable proposal may be reevaluated only after its named blocker changes.

## 11. Failure states

Minimum local fail-closed classes:

- `DENIED_FORBIDDEN_UPSTREAM_BEHAVIORAL_SOURCE`
- `DENIED_OPAQUE_PROVENANCE_DEREFERENCE`
- `DENIED_MODEL_VISIBILITY_AUDIT_ONLY`
- `BLOCKED_MISSING_ACTOR_SAFE_HANDOFF`
- `BLOCKED_STALE_ACTOR_SAFE_HANDOFF`
- `BLOCKED_HANDOFF_INTEGRITY_FAILURE`
- `BLOCKED_PERMISSION_SCOPE_WIDENING`
- `BLOCKED_PERMISSION_CLASS_SUBSTITUTION`
- `BLOCKED_HIDDEN_CLAIM_JOIN`
- `BLOCKED_RELATIONSHIP_VIEW_WIDENING`
- `BLOCKED_SESSION_REHYDRATION`
- `BLOCKED_PROMPT_ALLOWLIST_VIOLATION`
- `BLOCKED_RENDER_SEMANTIC_LEAK`
- `NONCAUSAL_PRESENTATION_ONLY`
- `CAUSAL_CANDIDATE_PENDING_V3_ADMISSION`
- `ZERO_MUTATION_REJECTED`
- `ZERO_MUTATION_DEFERRED`
- `ZERO_MUTATION_INVALID`

Names are SCRV2APP test-oracle vocabulary; they do not re-own the upstream authorities' canonical decision-state names.

## 12. Final seam rule

The local contract is frozen. Final M6 acceptance remains blocked only on:

`SCRV3_EXACT_ACTOR_SAFE_HANDOFF`

No fallback schema, guessed hash, broad raw V3 state, `GeneratedPersonRecord`, upstream prior, or current implementation structure may substitute for that exact sibling return.

Current cell token:

`SCRV2APP_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`
