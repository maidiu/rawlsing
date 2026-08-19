# DR-R02 — V553 TEMPORALIZATION BOUNDARY

**Court:** DR-R02 Direct-DAG Ownership & Minimality Sweep  
**Base:** `ade9bbe51ca2766bcde8ec58af6c659f0ca21f25`  
**Scope:** broad ownership/minimality only; no implementation or final V553 close-read

## 1. Dispositive boundary

V553 is not the mandatory first consumer of every `StructuralEmpiricalAdmission`.

V553 is mandatory exactly when a downstream lawful structural use requires a temporal/comparability semantic transformation that the admission itself does not already contain and that V553 uniquely owns.

The finite rule is:

```text
V553_REQUIRED_IF(
    downstream_use_requires_any_of(
        NEW_TEMPORAL_OBSERVATION_IDENTITY,
        CROSS_WAVE_OR_CROSS_TIME_COMPARABILITY_DECISION,
        TEMPORAL_HARMONIZATION_ACROSS_GOVERNED_REPRESENTATIONS,
        NEW_TEMPORAL_RELATION_OR_DELTA,
        NEW_TEMPORAL_LIMIT_OR_NONCOMPARABILITY,
        DERIVED_EFFECTIVE_PERIOD_OR_INTERVAL,
        DERIVED_RELATION_TIMING_OR_SEQUENCE,
        GOVERNED_PERSISTENCE_DRIFT_CHANGE_REVERSAL_RUPTURE_SEMANTIC
    )
    AND admission_does_not_already_lawfully_supply_that_semantic
)
```

and:

```text
V553_NOT_REQUIRED_IF(
    admission_is_already_structurally_admitted
    AND temporal_scope/effective_time_is_exact_for_the_target_use
    AND no_new_cross_time_comparison_or_harmonization_is_needed
    AND no_new_temporal_relation/delta/limit/interval/timing_semantic_is_needed
    AND the earliest downstream owner can perform its own unique transformation directly
)
```

The present earliest direct structural owner for the non-temporal affordance-eligible class is V554, subject to the V554 rule registry.

## 2. Why source time alone does not force V553

Every historical empirical fact has some source/time identity. That alone does not create V553 work.

A point-in-time admitted structural proposition may already be complete for a downstream bounded use. Sending it through V553 merely to restate the same timestamp would be transit, not semantic transformation.

Therefore:

```text
HAS_TIME_METADATA != REQUIRES_V553
```

The question is whether V553 must create new temporal structural meaning.

## 3. Mandatory classes

### 3.1 Cross-wave or cross-time comparison

When a downstream use depends on comparing two or more observations across waves/times, V553 is mandatory because comparability and relation identity are not implied by shared labels, source family or chronological order.

### 3.2 New temporal relation or delta

Persistence, drift, change, reversal, increase/decrease or another delta/relation that is not already a governed admitted proposition must be created by V553 under exact authority.

The sign of a V553 temporal delta remains distinct from producer-owned structural source→target direction.

### 3.3 Temporal harmonization

When two governed temporal representations require harmonization before downstream structural use, V553 owns the harmonization/comparability transformation. String equality and common canonical labels are insufficient.

### 3.4 Temporal limit / negative authority

Gap, noncomparability, no-lawful-relation, missing endpoint or another V553-owned temporal limit must be produced/preserved as typed negative authority. A direct V554 path may not bypass the negative result.

### 3.5 Derived effective period / historical interval

If the target structural use needs an interval that must be derived from observation timing rather than already supplied by admission authority, V553 is required.

A point observation does not silently become an interval.

### 3.6 Relation timing / sequence

If before/after/sequence/temporal ordering is part of the structural proposition and is not already governed by the admission, V553 creates that temporal relation.

### 3.7 Persistence / drift / rupture

These words are not automatic semantics.

They require V553 only where an explicit governed rule actually authorizes such a temporal semantic. The accepted V553 ruling keeps qualitative rupture/persistence-style annotations disabled when no deterministic governed rule exists.

Thus:

```text
NO_GOVERNED_TEMPORAL_RULE
-> MISSING_AUTHORITY / VALID_EMPTY
not
-> DIRECT_V554_GUESS
```

## 4. Nonmandatory classes

V553 is not required when the admission itself is already complete for the target use, including:

- one exact point-in-time structural proposition;
- one exact static/timeless structural proposition;
- one exact historical interval already established by admission authority;
- one source/time structural basis requiring no cross-wave comparison;
- any other admission whose target V554 rule needs no V553-created temporal relation, limit, harmonization or interval.

For such classes, the lawful path is:

```text
StructuralEmpiricalAdmission
-> V554
```

provided the V554 rule registry explicitly admits that structural basis class.

## 5. Effective-time hostile cases

### Case A — admission has exact `effective_time = 1985`, V554 rule asks only whether this basis is eligible for a bounded mediation affordance at 1985

No new V553 meaning exists.

**Ruling:** direct V554.

### Case B — admission has one 1985 observation and V554 rule asks whether the structural basis persisted into 1995

The use requires a temporal relation/comparability decision.

**Ruling:** V553 required.

### Case C — admission already contains a governed exact interval `[1985,1995]` as part of the admitted proposition and V554 rule consumes that interval without deriving any temporal relation

V553 would only restate the interval.

**Ruling:** direct V554.

### Case D — two source universes have observations in the same year but comparability is unresolved

Same year is not source-time comparability authority.

**Ruling:** V553 required if the structural use needs a cross-source/time temporal relation; otherwise preserve the admissions separately.

### Case E — an admission is non-temporal but no V554 rule exists for it

Bypassing V553 does not create V554 authority.

**Ruling:** no positive runtime route; `MISSING_AUTHORITY` / no downstream runtime consumer.

## 6. Precedence and duplicate prevention

The same structural proposition may not instantiate the same V554 use twice merely because both a direct admission and a V553 derivative are physically available.

V554 rule signatures must declare the eligible basis class:

- `DIRECT_ADMISSION_BASIS`; or
- `V553_TEMPORAL_BASIS`.

For a fixed structural proposition/use/rule version:

1. if the rule requires V553 semantics, the V553 object is the semantic input and the underlying admission is provenance only;
2. if the rule accepts an already-complete admission and requires no V553 semantics, the direct admission is the semantic input and any V553 restatement is ineligible as a duplicate;
3. both may coexist only when they represent genuinely distinct structural propositions or downstream use classes, each with its own identity.

No `latest wins`, score precedence or artifact-presence rule is lawful.

## 7. V553 output minimality

When V553 is required, its output must contain only the V553-owned semantics needed downstream plus exact producer reference closure.

It need not copy C11 incidence, full `EmpiricalFact`, query AST, weights or discovery receipts into every temporal row. Those may remain transitively dereferenceable through:

```text
V553 temporal object
-> StructuralEmpiricalAdmission
-> EmpiricalFact / EmpiricalQuerySpec / EmpiricalUniverse / authority / replay
```

Fields that V553 itself needs to interpret or validate must remain directly addressable, but addressability does not require semantic duplication.

## 8. Close-read questions left intentionally open

The later V553 close-read must freeze:

- exact corrected intake schema/locator vocabulary;
- which V553 canonical families each admitted temporal class may create;
- temporal relation/limit rule registries;
- legacy V552/V552J compatibility parity;
- exact duplicate/error behavior when admission and historical compatibility inputs identify the same basis.

Those are bounded details beneath this ownership rule.

## 9. Court ruling

```text
V553_REQUIRED_IF_NEW_V553_OWNED_TEMPORAL_OR_COMPARABILITY_MEANING_IS_NEEDED

V553_NOT_REQUIRED_IF_ADMISSION_IS_TEMPORALLY_COMPLETE_FOR_THE_TARGET_USE_AND_NO_NEW_V553_MEANING_IS_CREATED
```

This is a semantic boundary, not an optimization heuristic.
