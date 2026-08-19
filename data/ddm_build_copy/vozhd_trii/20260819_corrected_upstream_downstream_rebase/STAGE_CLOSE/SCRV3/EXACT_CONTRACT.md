# SCRV3 — Exact Contract

**Input:** `V3EmpiricalPossibilityInput@1.1.0`  
**Metabolism authority:** `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.1.0` / `e0cd3c8a4443c59b7e97cc151a7db9298310f7a7e766b593fb90968546d66939`  
**Read matrix:** `SCRV3_READ_PERMISSION_MATRIX@2.0.0` / `6a4227bb3df913b8564ba0d994ce5c2be81bf0f6e8d8b5a164ba546db59fa2d1`

## Noncollapse

```text
ResolvedStructuralContext
!= V3EmpiricalPossibilityInput
!= ActorCausalState
```

PSEPF is population empirical possibility, not actor fact/history/state. `ActorComparatorReceipt` is provenance-only. `ReplayReceipt` is audit-only.

## Thin input

The machine contract is `EXACT_CONTRACT.json`. It binds:

- deterministic input/actor/run identity;
- exact already-lawful objective actor-fact snapshot refs/hashes/owner/effective time;
- comparator state and exact comparator authority/provenance;
- exact source-indexed PSEPF refs/hashes;
- earliest-owner source-state records and source-relation refs;
- V3 decision surface, requested operation, exact permission row and owner serialization binding;
- metabolism authority and effective-time receipt;
- lifecycle/requery-vs-rebind state;
- exact already-lawful causal-parent receipt;
- audit replay ref and provenance closure.

It does not embed `ResolvedStructuralContext`, masses/joint tables, configuration rows, support arrays, respondent incidence, query ASTs, comparator rules, universe payloads, uncertainty geometry, J-way/minority/multimodal payloads, modal/top-k/marginal/pairwise summaries or latent scalars.

Exact full geometry remains producer-owned and dereferenceable by immutable `source_key + psepf_ref + psepf_content_hash`.

## Comparator seam

Survey coordinates never create objective actor facts. Comparator states are:

`COMPARATOR_APPLIED | ACTOR_PROPERTY_MISSING | NO_COMPARATOR | AMBIGUOUS_COMPARATOR | COMPARATOR_TEMPORAL_NONCOMPARABLE | COMPARATOR_INTEGRITY_FAILURE`.

A comparator-relevant actor-fact change requires upstream requery. V3 cannot silently retarget the historical field.

## Typed source admission

Per-source states are:

`PRESENT | ABSENT_IN_CATALOG | DECLARED_NONE | UNSPECIFIED | NO_FIELD | SOURCE_NOT_APPLICABLE | TEMPORAL_NONCOMPARABLE | TARGET_UNAVAILABLE | OBSERVED_ZERO | ZERO_SUPPORT | LOW_SUPPORT | UNCERTAINTY_UNQUANTIFIED`.

`OBSERVED_ZERO != ZERO_SUPPORT`; `UNSPECIFIED != DECLARED_NONE`; `SOURCE_NOT_APPLICABLE != NO_FIELD`; temporal noncomparability is not an actor negative state.

Cross-source composition defaults to none. Provenance reachability does not authorize pooling, majority, strongest-source selection or averaging.

## Effective time / lifecycle

`SCRV3_EFFECTIVE_TIME_ALIGNMENT_V2@2.0.0` hash `2f9f2319975d8f7a45a31722b11436c21922866cc12ba5faccb7de96794fb8c4` binds actor-fact snapshot time, every source interval, V3 decision time and owner transition causal time. Hidden latest, unowned interpolation and future-proxy backdating are forbidden.

`V3_REBIND`: same exact field and comparator snapshot remain upstream-valid; only V3 invocation/use/causal-parent intake binding changes.

`UPSTREAM_REQUERY`: comparator-relevant facts, source applicability/time, target/source set, authority or exact dereference validity changed.

Refresh is prospective. Past fields, receipts and actor history are immutable.

## Read permission

Current positive actor-transition rows: **none**.

Only `SCRV3-RP-V3M002-V2` admits noncausal `EXACT_GEOMETRY_DEREFERENCE`. All transition use is zero-effect unless the named semantic owner separately accepts a canonical rule/registry serialization explicitly binding PSEPF/EPI use.

The operation vocabulary—constraint test, annotation, filter, weight—is a future ceiling, not a grant. A filter cannot create candidates. A weight requires an exact owner transform and cannot itself assign actor state. Stochastic selection remains ADP-020-owned.

## Causal receipt / replay

PSEPF, RSC, comparator receipts and replay receipts are never promoted to causal parents. `V3EmpiricalPossibilityReadReceipt@1.0.0` records exact source/PSEPF hashes and component paths read, owner serialization/rule/transform, causal parent receipt, time receipt, candidate sets, RNG receipts and pre/post state hashes.

Denied/unbound reads produce `NO_PSEPF_TRANSITION_EFFECT`.

Same prior may diverge by later lawful history or recorded RNG. Same exact authority/history/RNG must replay exactly. Deterministic prior-to-persona collapse is forbidden.

## Peer seam / actor-safe handoff

SCR5578 local head `06eefed7bb8e7db7fd2465aa262653ed95461e84` permits bounded preparation only. Final exact RSC integration waits on accepted M4.

M6 positive type is already frozen by ADP-017: `ActorAccessibleRenderEnvelope`. V2 may narrow/render allowed claims but may not add/widen claims, infer hidden claims, dereference opaque upstream provenance for persona semantics, convert PSEPF/RSC/objective refs into actor knowledge, or mutate V3.
