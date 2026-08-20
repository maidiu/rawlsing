# IG-M5 ACCEPTANCE ORACLE

**Purpose:** freeze the semantic acceptance boundary for a future runtime implementation of the accepted M5 structural-peer seam.  
**This file is test specification, not executable test code.**  
**Frozen semantic head:** `M5_FINAL@54f163b38fb0589327ea7b50fd98b537d7d91831`  
**Frozen reclosure:** `c4a3524f54af368a67ca50ccc85f5d5dca3d803b`

## 1. Constitutional invariants

All future IG-M5 runtime tests MUST preserve:

`ResolvedStructuralContext != V3EmpiricalPossibilityInput != ActorCausalState`

and:

`RSC_ELIGIBILITY != V3_MUTATION_AUTHORITY`

and:

`M4_SIGNATURE_VALIDITY != RSC_IDENTITY != PERMISSION != CURRENTNESS`

The following constructions are acceptance failures even if deterministic and replayable:

- `persona = f(RSC, EPI)`;
- `belief = f(RSC)`;
- `memory = f(RSC)`;
- `response = f(RSC, PSEPF)` without a separately accepted owner rule;
- a generic merged prior bag;
- a hidden scalar/persona vector derived from both peer priors.

## 2. Positive acceptance path

A positive structural-peer validation result may occur only when all of these facts are present and exact:

1. an actual runtime object with schema exactly `SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0`;
2. exact runtime `context_id` and `context_content_hash`;
3. exact repository bundle ID/hash;
4. exact ContextQuery ID/hash;
5. exact resolver policy ID/version/hash;
6. exact resolution receipt ID/hash;
7. exact resolved-entry-set digest;
8. exact preserved-negative-entry-set digest;
9. exact deferred/unresolved-entry-set digest;
10. exact SelectionRecord-set digest;
11. exact coverage/fidelity profile ID/hash;
12. exact refresh/currentness metadata ID/hash and M4-owned currentness evidence;
13. exact provenance-root digest;
14. exact producer-binding digest;
15. exact item-wise permission-subset-proof digest;
16. exact positive+negative reference-closure digest;
17. an exact transported `M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0` value;
18. recomputation of that signature from the actual runtime material with exact equality;
19. a declared V3 structural-peer use whose required use is within `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`;
20. no forbidden structural reference class or provenance-as-composition violation.

Success establishes **structural-peer eligibility only**. It does not commit an actor transition.

## 3. Exact deterministic-resolution oracle

The future implementation test suite must prove deterministic exact V558 resolution at the M4→M5 boundary by freezing one complete M4 input universe and repeating resolution/validation at least twice.

For identical exact repository bundle, query, policy, producer objects, permissions, negative/deferred state, refresh/currentness facts and authority hashes:

- RSC schema must be identical;
- `context_id` must be identical;
- `context_content_hash` must be identical;
- all bound set digests must be identical;
- the transported/recomputed M4 signature must be identical;
- M5 validation disposition must be identical.

Any dependence on mutable latest, insertion order, database row order, filesystem order, wall clock outside declared currentness authority, nearest/fuzzy match, random choice, network repair, LLM/embedding judgment or default interpolation is an acceptance failure.

M5 must not independently recreate V558 resolution semantics. The concrete M4 resolver entry point remains `UNBOUND_UNTIL_ACCEPTED_M4_RUNTIME`.

## 4. Fail-closed oracle

The accepted M5 runtime failure vocabulary already includes:

- `M5_RSC_RUNTIME_INSTANCE_MISSING`;
- `M5_RSC_SCHEMA_MISMATCH`;
- `M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH`;
- `M5_RSC_SIGNATURE_MISMATCH`;
- `M5_RSC_PRODUCER_BINDING_MISMATCH`;
- `M5_RSC_PERMISSION_PROOF_INVALID`;
- `M5_RSC_REFERENCE_CLOSURE_INVALID`;
- `M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT`;
- `M5_RSC_PROVENANCE_AUTHORITY_VIOLATION`.

Where the frozen semantic contract does not assign a more specific M5 error token (for example stale currentness or an M4-level ambiguous/missing resolver state), the test oracle requires the bounded behavior rather than inventing a new semantic enum:

`FAIL_CLOSED + ZERO_STRUCTURAL_PEER_EFFECT + NO_FALLBACK + NO_RSC_FABRICATION`

The concrete runtime error/exception spelling is `UNBOUND_UNTIL_ACCEPTED_M4_RUNTIME` unless already frozen above.

## 5. Stale/currentness oracle

An RSC is not accepted merely because it is immutable and hash-valid.

Future tests must cover:

- current RSC under exact M4-owned currentness evidence → may proceed to structural-peer eligibility validation;
- stale RSC with otherwise valid hashes → fail closed for current structural-peer consumption;
- refreshed successor RSC → may be validated prospectively as a new identity/receipt chain;
- historical receipt referencing stale predecessor → remains historically intact and replayable;
- mutation/relabeling of the old receipt to point at the refreshed RSC → acceptance failure;
- structural refresh causing empirical requery by implication → acceptance failure;
- empirical requery/rebind causing structural refresh by implication → acceptance failure.

No hidden `latest` substitution is permitted.

## 6. Missing / ambiguous / closure oracle

Future tests must attack each of the following independently:

- missing actual RSC instance;
- missing required resolved root;
- missing interpretation-critical dependency;
- missing preserved negative/limit dependency;
- missing SelectionRecord;
- missing producer object/hash binding;
- ambiguous exact reference resolution;
- duplicate candidate with no exact accepted disambiguation authority;
- corrupt dependency bytes/content;
- producer content-hash mismatch;
- repository/query/policy receipt mismatch;
- participant role/cardinality/multiplicity/order corruption;
- required deferred/unresolved state silently dropped.

Required disposition in every case: no positive structural-peer effect and no heuristic repair.

## 7. Infrastructure nonsemanticity oracle

The following facts are deliberately insufficient for positive M5 validation by themselves:

- repository row exists;
- repository bundle exists;
- persistence roundtrip succeeds;
- index contains a key;
- locator resolves an address;
- cache/snapshot contains an object;
- object is newest by timestamp;
- collection is marked ready;
- root object has permission;
- dependency is reachable;
- checksum template is known.

Tests must show these do not create producer identity, semantic ownership, permission, currentness, dependency permission, actor-state authority or a fabricated RSC.

Persistence and snapshots are required to preserve exact semantic identity/hash/closure; they may never replace them.

## 8. Permission oracle

For every selected root and interpretation-critical dependency:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`

Tests must reject:

- root permission inherited by dependencies;
- repository presence widening permission;
- collection readiness widening permission;
- a valid M4 signature widening permission;
- `ACTIVE_CAUSAL` being interpreted as actor mutation authority;
- a structural peer satisfying or substituting for empirical metabolism/read permission.

## 9. Peer-separation oracle

Future M5 integration tests must prove:

- no PSEPF or EPI inside structural repository/RSC semantics;
- no RSC embedded into EPI;
- no RSC→PSEPF synthesis;
- no PSEPF/comparator→generated structural position;
- no source disagreement→actor contradiction;
- no RSC/EPI direct creation of memory, belief, knowledge, relationship, action, response, persona or voice;
- a V3 transition can consume a structural peer only under its separately accepted owner declaration and causal-parent rules.

The current frozen SCRV3 M5 input has zero positive PSEPF actor-transition rows. Future owner amendments, if any, require their own accepted authority and are outside this preflight.

## 10. Replay oracle

A committed V3 peer-consumption receipt must preserve the exact historical:

- RSC identity/hash;
- M4 signature value;
- peer requirement declaration;
- decision effective time;
- EPI identity/hash if present;
- empirical read receipts if present;
- ordered lawful causal parents;
- RNG receipts;
- pre/post actor-state hashes;
- integrity/result state.

Same exact peer inputs + exact authority + exact causal history + exact RNG receipts must replay identically.

Same priors may lawfully diverge when later lawful causal history or separately recorded RNG decisions differ. Tests that force same-prior same-life collapse fail.

## 11. M4 runtime symbol binding rule

This preflight freezes only **facts and observable acceptance behavior**.

The following remain deliberately unbound until an accepted M4 runtime return exists:

- module path;
- resolver class/type name;
- repository adapter class/type name;
- persistence adapter class/type name;
- runtime RSC class/type name beyond the semantic schema ID;
- resolver function/method name;
- validation function/method name;
- refresh function/method name;
- concrete exception classes;
- concrete currentness receipt class/type name;
- call signature and dependency injection shape.

All are `UNBOUND_UNTIL_ACCEPTED_M4_RUNTIME`.

## 12. Acceptance rule

A future IG-M5 runtime implementation passes only if every fixture in `M5_HOSTILE_FIXTURES.json` and every invariant above is demonstrated without semantic widening, API fabrication, hidden fallback, or historical receipt rewriting.
