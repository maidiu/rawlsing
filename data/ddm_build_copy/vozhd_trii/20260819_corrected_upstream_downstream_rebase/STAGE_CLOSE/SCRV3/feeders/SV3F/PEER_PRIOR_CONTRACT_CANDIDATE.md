# V3 STRUCTURAL / EMPIRICAL PEER-PRIOR INTEGRATION — CANDIDATE CONTRACT

**Status:** `NON_DISPOSITIVE_CANDIDATE_FOR_SCRV3_AND_M5`  
**Candidate name:** `V3_STRUCTURAL_EMPIRICAL_PEER_PRIOR_INTEGRATION`  
**Broad topology:** unchanged  
**Core law:** `ResolvedStructuralContext != V3EmpiricalPossibilityInput != ActorCausalState`

## 1. Scope

This candidate defines only the V3-side coordination boundary for two already-frozen peer inputs. It creates no upstream semantic transformation and no new broad producer.

It does not own:
- structural producer semantics;
- V557/V558 publication/repository/resolver semantics;
- PSEPF geometry or comparator semantics;
- metabolism algorithm;
- actor-state domain semantics;
- V2 expression.

## 2. Three nonidentical semantic classes

### `STRUCTURAL_PEER`

Carrier: M4-final accepted `ResolvedStructuralContext`.

Meaning: exact resolver-derived structural context selected from immutable producer-preserving structural repository material under producer/V557/resolver permission narrowing.

Not meaning: actor fact, event, experience, memory, knowledge, belief, relationship, action, personality, voice, or PSEPF.

### `EMPIRICAL_POSSIBILITY_PEER`

Carrier: final SCRV3 `V3EmpiricalPossibilityInput`.

Meaning: actor/decision/effective-time/use/metabolism/lifecycle binding over exact immutable source-indexed PSEPF refs, preserving upstream typed states.

Not meaning: structural context, generated position, actor state, belief probability, response probability, memory, knowledge, persona, or voice.

### `ACTOR_CAUSAL_STATE`

Carrier: exact V3 stored/generated state/history under named actor-development authorities.

Meaning: generated actor-specific causal truth/state as of exact causal time.

Not meaning: upstream prior. It is a transition precondition/input and potential committed output under the owning V3 rule.

## 3. Candidate coordination envelope

A V3 transition that may consult either peer SHOULD bind a nonsemantic coordination record with fields equivalent to:

```text
peer_consultation_id/hash
actor_id
transition_owner_authority_id/version/hash
transition_class
owner_rule_id/version/hash
decision_context_id
use_class
effective_time
pre_actor_state_ref/hash
peer_requirement_mode
structural_peer_ref/hash OR NOT_REQUESTED
structural_peer_signature_ref
structural_permission_state/allowed_uses
structural_currentness_state
structural_resolution_receipt_ref
structural_refresh_metadata_ref
empirical_peer_ref/hash OR NOT_REQUESTED
empirical_metabolism_authority_ref/hash
empirical_read_permission_row_ref
empirical_currentness_state
empirical_upstream_typed_state_refs
empirical_operation_class
consultation_result
causal_parent_refs
rng_receipt_refs
committed_transition_ref OR NO_TRANSITION
post_actor_state_ref/hash OR UNCHANGED
receipt_hash
```

This record is replay/audit/causal-parent evidence. It is not a semantic third prior and may not carry copied structural or PSEPF geometry.

## 4. Peer requirement modes

Every owner invocation must explicitly declare one mode:

- `NEITHER_PEER_USED`
- `STRUCTURAL_ONLY_REQUIRED`
- `EMPIRICAL_ONLY_REQUIRED`
- `BOTH_PEERS_REQUIRED`
- `STRUCTURAL_REQUIRED_EMPIRICAL_OPTIONAL_BY_EXACT_RULE`
- `EMPIRICAL_REQUIRED_STRUCTURAL_OPTIONAL_BY_EXACT_RULE`
- `EITHER_PEER_BY_EXACT_DISJOINT_OWNER_RULE`

There is no default mode.

`EITHER_PEER_BY_EXACT_DISJOINT_OWNER_RULE` requires deterministic disjoint owner predicates selecting a legal branch. It may not choose whichever peer is available, newer, higher-scoring, majority-supported, or easier to resolve.

## 5. Structural peer gate

A structural peer is consultable only when all required checks pass:

1. exact M4-final `ResolvedStructuralContext` signature is bound;
2. context ID/hash, repository/query/policy, resolution receipt and required SelectionRecord refs resolve exactly;
3. the exact structural entry is within its resolver allowed-use set;
4. `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses` verifies item-wise;
5. producer negative/deferred/noncomparable/valid-empty states are preserved;
6. the named V3 transition owner independently authorizes use of that structural semantic class.

`ACTIVE_CAUSAL` at the resolver is therefore necessary only when that exact structural item is to be used causally. It is never sufficient to mutate V3.

Structural consultation results SHOULD distinguish semantic equivalents of:

```text
STRUCTURAL_NOT_REQUESTED
STRUCTURAL_ADMITTED
STRUCTURAL_USE_DENIED
STRUCTURAL_CONTEXT_DEFERRED
STRUCTURAL_CONTEXT_NEGATIVE_PRESERVED
STRUCTURAL_REFRESH_REQUIRED
STRUCTURAL_REFRESH_AUTHORITY_UNBOUND
STRUCTURAL_INTEGRITY_FAILURE
STRUCTURAL_M4_SIGNATURE_UNBOUND
```

## 6. Empirical peer gate

The empirical peer gate is inherited from final SCRV3 adjudication of accepted SV3M evidence:

1. exact `V3EmpiricalPossibilityInput` is current/admissible for actor/use/effective time;
2. exact metabolism authority ID/version/hash is bound;
3. exact transition/use/operation permission exists;
4. exact PSEPF/source components dereference by immutable ID/hash;
5. upstream negative/source-comparison state permits the exact operation;
6. owner has an independent lawful candidate/transition basis;
7. any transform is separately owner-versioned/hash-bound;
8. actual consultation is receipted.

Missing gate => `NO_PSEPF_TRANSITION_EFFECT`.

## 7. Cross-peer law

`CROSS_PEER_COMPOSITION_AUTHORITY = NONE_BY_DEFAULT`.

A transition owner may consult both peers only as separately governed inputs to its already-existing semantic rule. The owner must name the exact operation performed on each input and the output must remain in the owner's lawful semantic domain.

The following are forbidden generic operations:

```text
merge(structural_peer, empirical_peer) -> shared_prior
scalarize(structural_peer, empirical_peer) -> profile_score
embed(structural_peer, empirical_peer) -> persona_vector
argmax(empirical_peer) + structural_label -> identity
source_majority(empirical_peer) + structural_pressure -> belief
```

No cross-peer deduplication exists. Equal label, time, geography, source name, content bytes, hash fragment, or semantic-looking text does not establish identity/equivalence.

## 8. Currentness / refresh independence

### Structural currentness

Structural identity/currentness is a function of exact repository bundle, ContextQuery, resolver policy, generated bindings, resolution receipt and producer temporal/refresh authority. SCR5578 refresh metadata carries exact bound next-change information or a typed unbound state; it does not invent a trigger.

Structural re-resolution is noncausal by itself.

### Empirical currentness

Empirical currentness is a distinct function of actor objective-fact snapshot, comparator/source/query/field authority, field refs, decision/effective time, use class and metabolism binding.

Upstream-requery and V3-rebind remain distinct.

### Actor-state changes

A committed V3 transition may change an objective fact or generated binding. That change may then separately trigger:
- structural re-resolution if it changes an accepted structural query binding; and/or
- empirical comparator/field requery if it changes an eligible comparator snapshot.

Neither trigger is inferred solely because the other fired.

### Partial currentness

One peer stale/denied/unbound does not semantically poison the other. The owner requirement mode decides whether the invocation blocks, proceeds on an explicitly authorized one-peer path, or becomes a typed no-op.

## 9. Causal nonassignment theorem

For any peer input `P`:

```text
P is available
AND P is permitted for consultation
DOES NOT IMPLY
actor mutation is authorized
```

A committed actor mutation requires:

```text
named V3 owner authority
+ exact owner rule
+ required causal witnesses / lawful candidate basis
+ all requested peer gates
+ effective-time legality
+ any required ADP-020 decision receipt
+ committed transition receipt
```

Therefore these remain forbidden:

- structural availability -> encounter/exposure;
- structural pressure -> memory/belief/relationship/action;
- PSEPF mass/modal cell -> response/belief/action;
- PSEPF coordinate -> generated position;
- source disagreement -> actor contradiction;
- repository permission -> owner transition permission.

## 10. Legitimate indirect paths that do not collapse the peers

The contract does not prohibit lawful causal sequences such as:

```text
ResolvedStructuralContext
-> named V3 transition under its own rule
-> generated objective actor fact
-> later ActorComparabilityService snapshot
-> new PSEPF
```

The upstream field is produced from the later objective actor fact through the comparator/query/field chain, not synthesized from structural context.

Likewise a permitted empirical consultation may affect an owner decision, but it cannot directly mint ADP-009 generated structural position, memory, knowledge, relationship, or action without those owners' own authority.

## 11. Replay and divergence

The peer coordination receipt must bind exact peer identities actually consulted, owner rule identity, pre-state hash, causal parents and ADP-020 receipts where any.

Required laws:

- same exact peer refs + same pre-state + same causal history + same exact RNG receipts + same owner authorities => deterministic replay of the same transition result;
- same peer refs do not force same future life when subsequent lawful events/relationships/exposures/actions/RNG histories differ;
- different structural refresh history or empirical requery/rebind history changes replay identity and may lawfully change later decisions without rewriting old history.

## 12. M4 symbolic dependency

The local SCR5578 contract is observed at:

`06eefed7bb8e7db7fd2465aa262653ed95461e84`

with local machine contract hash:

`7522e3066ec7cd03de36faf065e089925e42356b4a6833d7420d00f6a139f88c`.

Its local schema name `SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0` may be referenced as a candidate semantic family, but its exact M4-final accepted signature/fingerprint is intentionally unbound here. `FINAL_M4_BINDING_SLOTS.json` is normative for the placeholders this feeder leaves unresolved.
