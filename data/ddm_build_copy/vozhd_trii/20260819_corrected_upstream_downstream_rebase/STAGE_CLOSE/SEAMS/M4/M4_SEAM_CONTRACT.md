# M4 final seam contract

Contract: `M4_SCR5578_MIXED_PRODUCER_FINAL_SEAM@1.0.0`

Authority: `DISPOSITIVE_M4_FINAL_SEAM_ONLY`

This contract binds accepted producer authority into the already-frozen SCR5578 contract. It is not a producer semantic contract and may not override any V553/V554/V555/V556 identity, state, reference, rule, permission, or replay law.

## 1. Accepted producer seal model

M4 recognizes four producer families.

### V553

Acceptance seal is the exact SCR553 producer head `b261ff885b2b7fd2cd065917b862eb541e24c4a2`, token `SCR553_EXACT_CONTRACT_CLOSED`, and exact contract blob `072c0995fe3dc7915dca50193e6ee44b8164e546`.

### V554

Acceptance seal is the exact SCR554 producer head `b5d745ac70c833324c8be0addf6c08ad72372263`, token `SCR554_EXACT_CONTRACT_CLOSED`, and exact contract blob `4bce143b087d5e38dbb4829a979a3f43abf9ab90`.

### V555

Acceptance seal is composite, not synthetic:

`SCR555 local exact contract head 49a9ce7cd830eb670cf1f9d381d4d33e56ddf682`

plus

`M2 semantic package head 92128619122886d0ced877a29b42fdb453765246 / M2_ACCEPTED__SCR555_EXACT_CONTRACT_CLOSED`.

M4 must not invent a new V555 producer head or replace canonical route identity with an M2/M4 identifier.

### V556

Acceptance seal is composite, not synthetic:

`SCR556 local exact contract head 9cfefc722f51cfab64952f004afef67fe65eb4a5`

plus

`M3 accepted result blob c5c2f85bade35a1b1cda9a26ce946f76d39ec953 / M3_ACCEPTED__SCR556_EXACT_CONTRACT_CLOSED`.

M4 must not invent a new V556 producer head or replace V556 identity with an M3/M4 identifier.

## 2. Registry admission

A producer object may enter a V557 publication bundle only when all are true:

1. its producer family is V553, V554, V555, or V556;
2. its canonical producer ID and content hash verify under the exact accepted producer contract;
3. its producer typed state is exactly preserved;
4. all producer-required interpretation-critical references are exact and closure-capable;
5. its producer permission for the proposed use is exact and positive;
6. V557 independently admits the exact item/use and does not widen producer permission.

V557 governance IDs and V558 locator/index/bundle IDs are nonsemantic with respect to producer identity.

## 3. V555 identity checksum

The semantic route identity is the exact ordered tuple:

`[EXACT_V554_F1_REF, route_rule_id@route_rule_version, route_shape_id@route_shape_version, channel_structural_role_id, EXACT_STRUCTURAL_CHANNEL_REF, receiving_constraint_kind, EXACT_TARGET_RECEIVING_POSITION_REF]`

M2 binds field 1 to the accepted canonical SCR554 `F1_id`.

The matching exact B1 proves `allowed_v555_structural_use=true` for the same F1/invocation. B1 is not a route tuple field. Inherited V554 F2 is exact-reference-only and remains V554-owned.

Any route locator must reverse to and verify this exact tuple. Hash equality without tuple equality is insufficient.

## 4. V556 participant checksum

Every V556 participant occurrence binds exactly:

`[v555_route_identity_ref, role, ordinal_or_null, multiplicity_index]`

The exact V556 rule authority owns participant roles, order policy, cardinality, multiplicity, same-route reuse, source-composition policy, allowed typed states, and producer allowed uses.

Positive V556 meaning requires at least two exact canonical V555 route participants and every additional rule-declared participant. A partial n-ary object cannot be downgraded into a lawful smaller positive object.

Same-route reuse is forbidden unless the exact V556 rule positively authorizes it and every occurrence is separately bound. V556 may not reconstruct, alias, normalize, or mint replacement V555 route identity.

## 5. Permission checksum

For every root and every dependency:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`

The check is item-wise. A missing or ambiguous producer permission fails closed.

No permission follows from:

- repository presence;
- collection readiness;
- locator/index presence;
- provenance reachability;
- root permission;
- dependency relation;
- co-resolution.

V557 may narrow, never widen. ContextResolver may narrow again, never widen.

## 6. Standalone closure

Raw V553/V554/V555/V556 directories are not runtime dependencies when closure is complete.

For each published root, recursively follow only exact producer/reference-contract-declared interpretation-critical references. Preserve positive and negative dependencies alike.

A leaf is satisfied only by:

- immutable packaged content verified by exact hash; or
- an exact immutable hash-bound locator/resolution binding whose identity/version/hash is itself bound and whose deterministic resolution verifies the authoritative content.

The following never satisfy a required leaf: ID-only reference, display label, prose provenance, raw-stage path, mutable latest, bare hash with no deterministic immutable resolution contract, fuzzy/nearest substitute, or network lookup.

Missing, ambiguous, corrupt, hash/version mismatched, role-corrupt, order-corrupt, cardinality-corrupt, multiplicity-corrupt, or partially packaged required closure is `INTEGRITY_FAILURE`.

## 7. Graph law

Every reference edge preserves:

- source locator ref;
- target locator ref;
- exact reference-contract ID/version/hash;
- edge role;
- requiredness;
- participant role;
- declared cardinality;
- multiplicity key;
- order-significant bit;
- semantic ordinal.

Producer role/order/cardinality/multiplicity semantics cannot be inferred or normalized from storage order, resolver order, prose, labels, or adjacency.

## 8. Typed state separation

Producer semantic outcomes remain producer outcomes.

Examples include V553 typed temporal limits, V554 nonpositive/unknown/valid-empty results, V555 positive/negative/missing/deferred/valid-empty states, and V556 `SUPPORTED`, `VALID_EMPTY`, `DENIED`, `NONCOMPARABLE`, `UNKNOWN_AUTHORITY`, `CONFLICTING_AUTHORITY`, `INVALID_PARTICIPANT_SET`, and `UNRESOLVABLE_PARTICIPANT`.

Repository or resolver integrity failure is not any of those. Physical absence of a required dependency is an integrity failure, not semantic missing authority. Empty/incomplete index is not producer valid-empty. Hash mismatch is not semantic unknown.

## 9. Source and provenance law

Source universes remain distinct by default.

Provenance proves origin/audit reachability only. It does not grant:

- source equivalence;
- source pooling/composition;
- respondent linkage;
- estimand compatibility;
- measure/weight compatibility;
- V556 interaction/topology authority.

Cross-source composition remains `NONE_BY_DEFAULT` unless the exact governing producer operation has exact positive composition authority covering the precise source universes and participant bindings.

## 10. Reference-class firewall

StructuralPriorRepository semantic roots/edges must reject:

- PSEPF / PositionedSubjectEmpiricalPossibilityField;
- V3EmpiricalPossibilityInput;
- ActorComparatorReceipt;
- rendered persona/expression semantics.

DiscoveryResultReceipt and ReplayReceipt are audit-only. Other upstream objects may be reference-only only when the producer contract declares them interpretation-critical.

## 11. Resolver and replay law

The resolver is pure over exact immutable inputs:

- repository bundle ID/hash;
- index manifest ID/hash;
- ContextQuery ID/hash;
- `V558_CONTEXT_RESOLVER_POLICY@1.0.0` with hash `4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f`;
- exact accepted generated binding refs/hashes.

Forbidden nondeterminism/repair includes wall clock, mutable latest, filesystem/database/process order, raw-stage/network lookup, LLM/embedding inference, randomness, unrecorded cache state, labels, or default policy.

Every considered candidate emits one SelectionRecord. Equal-rank singular ambiguity remains ambiguity unless exact authority permits multiplicity. Co-resolved V555 participants do not create V556 meaning.

Replay under the same exact publication/repository hashes, producer identities/contracts/reference closure, V557 governance, index/query/policy/generated bindings, and producer authorities must reproduce the same semantic selection, typed states, SelectionRecords, receipt, fidelity/refresh metadata, and ResolvedStructuralContext.

## 12. M5 RSC signature

The M4->M5 signature is `M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0` and is defined in `M5_RSC_HANDOFF.json`.

It is a canonical verification signature over the exact SCR5578 RSC bindings. It does not replace `context_id`, `context_content_hash`, any producer identity, or any permission record. M4 does not fabricate a runtime RSC instance.

## 13. Acceptance condition

M4 is accepted only if all producer seals verify, the frozen SCR5578 contract remains unchanged, all closure/identity/permission/graph/firewall/replay hostile checks pass, and the M5 RSC signature can be stated without adding semantics.

These conditions pass under the exact authorities pinned by assignment `E02-W10-M4-FINAL-001`.

Final disposition: `M4_ACCEPTED__SCR5578_EXACT_CONTRACT_CLOSED`.
