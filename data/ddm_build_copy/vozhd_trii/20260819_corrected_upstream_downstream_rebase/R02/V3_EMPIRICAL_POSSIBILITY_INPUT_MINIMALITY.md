# DR-R02 — V3 EMPIRICAL POSSIBILITY INPUT MINIMALITY

## 1. Question

Does `V3EmpiricalPossibilityInput` create enough V3-specific meaning to justify a boundary object, or is it merely a renamed copy of `PositionedSubjectEmpiricalPossibilityField`?

R02 ruling:

`KEEP_AS_MINIMAL_V3_BOUNDARY_OBJECT__DO_NOT_COPY_FIELD_GEOMETRY`

The wrapper is justified only because it owns V3-specific intake applicability, effective-time/lifecycle, refresh/staleness and metabolism-authority binding that PSEPF itself must not own.

## 2. Why PSEPF cannot absorb the V3 lifecycle contract

`PositionedSubjectEmpiricalPossibilityField` is population empirical possibility geometry produced by the empirical domain.

It must remain independent of:

- one specific V3 causal decision;
- whether a particular actor-development step is allowed to consult it;
- V3 developmental phase;
- V3 refresh/staleness policy;
- V3 metabolism rule version;
- V3 causal-history parentage.

Putting those concerns inside PSEPF would make an empirical object own actor-runtime policy.

Therefore the V3 boundary needs a distinct, narrow object.

## 3. Minimum semantic content

The wrapper should bind references, not duplicate empirical geometry.

Minimum content:

1. `v3_empirical_possibility_input_id`;
2. actor/generated-person identity;
3. objective actor-fact snapshot/reference set or immutable snapshot hash used for this field request;
4. one or more exact source-indexed PSEPF object IDs/content hashes;
5. effective V3 decision time / developmental context identity;
6. V3 use class or decision-context kind for which the field is admitted;
7. `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY` ID/version/hash;
8. lifecycle state: current / stale / refresh-required / invalidated / unavailable;
9. refresh trigger or next-required-requery condition where governed;
10. typed negative/availability state;
11. exact replay/intake receipt identity;
12. provenance pointer to field/comparator/query/source authorities.

The wrapper need not copy:

- joint probability/mass tables;
- configuration rows;
- raw or weighted supports;
- query AST;
- comparator rule text;
- source universe manifests;
- empirical uncertainty payload;
- respondent incidence.

Those stay inside or behind immutable PSEPF references.

## 4. Geometry access

When V3 needs the actual field geometry, it dereferences the exact immutable PSEPF object pinned by the wrapper.

The wrapper may expose a typed read interface or content locator, but the empirical geometry remains producer-owned.

Thus:

```text
V3EmpiricalPossibilityInput
!= copy(PositionedSubjectEmpiricalPossibilityField)
```

It is closer to:

```text
V3EmpiricalPossibilityInput {
  actor_context_ref,
  field_refs,
  effective_time,
  v3_use_class,
  metabolism_authority_ref,
  lifecycle_state,
  negative_state,
  replay_ref
}
```

## 5. Effective time

Field source time and V3 decision time are distinct.

The input boundary must bind:

- actor objective-fact effective time used by comparator service;
- source/historical time represented by each PSEPF component;
- V3 decision/effective time at which the field is being made available;
- any authorized temporal alignment rule.

No hidden `latest` rule is allowed.

A field does not remain valid forever merely because its object is immutable.

## 6. Refresh and staleness

The wrapper owns the V3-side question:

> Is this exact already-produced empirical field still an admissible upstream constraint for this actor and this developmental decision context?

Potential refresh triggers include, only when governed:

- objective actor fact used by a comparator changed;
- actor entered a new age/time band relevant to comparator law;
- source-applicability period changed;
- PSEPF target/request changed;
- metabolism authority version/use class changed;
- an external authority explicitly invalidated the intake.

The wrapper does not decide empirical recomputation semantics itself. `refresh-required` sends the request back to the upstream comparator/query/field producer.

## 7. Typed negative states

At minimum the V3 boundary must preserve or expose distinctions equivalent to:

- `NO_FIELD`;
- `ACTOR_PROPERTY_MISSING`;
- `NO_COMPARATOR`;
- `AMBIGUOUS_COMPARATOR`;
- `SOURCE_NOT_APPLICABLE`;
- `TEMPORAL_NONCOMPARABLE`;
- `TARGET_UNAVAILABLE`;
- `ZERO_SUPPORT`;
- `LOW_SUPPORT`;
- `UNCERTAINTY_UNQUANTIFIED`;
- `FIELD_STALE_REFRESH_REQUIRED`;
- `METABOLISM_AUTHORITY_MISSING`;
- `INPUT_USE_DENIED`.

These states are not belief priors and do not authorize fallback invention.

## 8. ActorComparatorReceipt minimality

`ActorComparatorReceipt` has no independent V3 runtime semantic role.

Its direct semantic consumer is `PossibilityFieldService`.

After field creation, V3 needs only exact provenance reachability to the comparator receipt so replay can establish why the actor facts lawfully mapped to the empirical conditioner.

Ruling:

`TRANSITIVELY_REFERENCED__PROVENANCE_ONLY_IN_V3`

Do not create a V3 comparator-prior collection.

## 9. ReplayReceipt minimality

`ReplayReceipt` likewise has no independent developmental meaning.

It proves immutable semantic/authority/input binding for historical replay and migration.

Ruling:

`AUDIT_REPLAY_ONLY`

A V3 causal step may reference the intake replay identity, but the receipt itself does not constrain actor development.

## 10. Relationship to ResolvedStructuralContext

The two inputs remain constitutionally distinct:

```text
ResolvedStructuralContext
!=
V3EmpiricalPossibilityInput
```

`ResolvedStructuralContext` is actor-independent structural context resolved from the structural repository.

`V3EmpiricalPossibilityInput` is a V3-specific admissibility wrapper over source-indexed population possibility geometry.

They may be simultaneously available to one V3 decision but must not be merged into one generic prior container.

## 11. No direct actor assignment

The wrapper's existence does not authorize a metabolism algorithm.

R02 freezes only the negative boundary:

- no `belief_probability = field.mass`;
- no direct response selection from modal cell;
- no identity/persona assignment;
- no memory or knowledge creation;
- no bypass of actual V3 history, encounter, exposure, mediation, relationships or path dependence;
- no same-field -> same-life determinism.

The later V3 close-read must specify the lawful metabolism contract without violating these prohibitions.

## 12. Persistence

The wrapper is a boundary/causal-history object, not necessarily a global durable table.

Persist it when required for:

- causal parentage;
- historical replay;
- field refresh decisions;
- audit of a developmental choice that actually consulted the field.

Otherwise it may be transient while the underlying PSEPF remains canonical/reconstructible.

## 13. Final ruling

The smallest lawful V3 boundary is a **reference-and-lifecycle envelope** over immutable PSEPF objects.

It survives minimality because it creates V3-specific meaning that PSEPF must not own:

`THIS FIELD VERSION IS LAWFULLY AVAILABLE TO THIS ACTOR DEVELOPMENTAL DECISION AT THIS EFFECTIVE TIME UNDER THIS METABOLISM AUTHORITY`.

Everything else remains producer-owned by the empirical field service.
