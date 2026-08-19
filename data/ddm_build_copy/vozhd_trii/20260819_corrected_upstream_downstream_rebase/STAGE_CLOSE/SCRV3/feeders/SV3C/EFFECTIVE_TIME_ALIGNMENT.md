# SV3C — EFFECTIVE-TIME ALIGNMENT CANDIDATE

**Status:** `NON_DISPOSITIVE_CANDIDATE_FOR_SCRV3`  
**Role:** `SV3C EFFECTIVE-TIME / SOURCE-STATE / NEGATIVE-ADMISSION FEEDER`  
**Production implementation:** `NOT AUTHORIZED`  
**Broad topology amendment:** `NONE`

## 1. Constitutional time separation

SV3C freezes the following noncollapse as the hostile candidate for SCRV3:

```text
ACTOR_FACT_SNAPSHOT_TIME
!= PSEPF_SOURCE_OR_HISTORICAL_TIME
!= V3_DECISION_OR_EFFECTIVE_TIME
!= ADP_021_SCHEDULER_TIME
```

These clocks may sometimes carry equal values. Equality of values never merges their semantic ownership.

### 1.1 Actor-fact snapshot time

This is the effective/currentness time of the exact objective actor facts used by `ActorComparabilityService`. It is comparator-input provenance. A later V3 decision may not silently pretend that an older snapshot still describes the actor after a query-relevant generated fact has changed.

### 1.2 PSEPF source/historical time

This is source-owned empirical time: source universe, historical scope, field period, survey/wave scope, target observability and per-source applicability. It remains attached to each immutable source-indexed PSEPF component. V3 may not rewrite this time to make a component convenient for a decision.

### 1.3 V3 decision/effective time

This is the time at which an exact V3 owner asks whether an already-produced immutable PSEPF may be consulted for one actor, use class and decision context. The V3 intake boundary owns the decision-bound admissibility result, not the upstream empirical meaning.

### 1.4 ADP-021 scheduler time

`V3_HYBRID_CAUSAL_SCHEDULER_POLICY` owns trigger coordination and monotone causal-time advancement. Scheduler time does not own empirical source time, comparator snapshot currentness, or PSEPF admissibility semantics. A trigger at time `T` may invoke a V3 decision at `T`; it may not convert `T` into evidence time or choose a newer/nearer field.

## 2. No implicit temporal coercion

The following implications are forbidden:

```text
nearest source time => admissible
latest source time => admissible
same calendar year => comparable
source timestamp <= decision time => sufficient
scheduler current_effective_time => PSEPF effective time
field immutability => perpetual V3 admissibility
old field exists => old field remains current
newer field exists => newer field replaces replayed historical field
```

An exact use-class-specific time/applicability rule must positively establish admissibility. Unknown alignment fails closed.

## 3. Candidate V3-side alignment predicate

Let:

- `S` = exact objective actor-fact snapshot ref/hash + its effective/currentness metadata;
- `C[i]` = one immutable source-indexed PSEPF component;
- `F` = the immutable PSEPF set/field identity;
- `D` = exact V3 decision/use binding with `decision_effective_time`;
- `M` = exact metabolism-authority binding;
- `Q` = exact upstream comparator/query/source applicability lineage;
- `A_time` = exact authority/rule proving the requested relation between `S`, `C[i]`, and `D` for this use class.

Candidate evaluation order:

```text
1. Verify immutable IDs/hashes/authority refs for S, F, C[i], D and M bindings.
   failure -> INTEGRITY_FAILURE

2. Preserve comparator-owned failures.
   NO_COMPARATOR or AMBIGUOUS_COMPARATOR -> no PSEPF read, no fallback

3. Ask whether the exact empirical request must be recomputed upstream.
   actor comparator facts changed materially,
   comparator/source/query applicability changed,
   source universe/target scope changed,
   or the requested field no longer answers the empirical question
   -> UPSTREAM_REQUERY_REQUIRED

4. Else ask whether only the V3 binding is no longer valid.
   same immutable field remains empirically valid,
   but actor/use class/decision context/effective-time/metabolism binding changed
   -> STALE_OR_REBIND_REQUIRED

5. Evaluate exact time/source applicability for each source component.
   missing or negative relation authority -> preserve SOURCE_COMPONENT_NONCOMPARABLE
   field-level decision-time relation unproved -> EFFECTIVE_TIME_NONCOMPARABLE

6. Hard reject backdating future evidence.
   if a source component contains evidence unavailable after D's decision cutoff
   and no explicit prospective-use authority governs that use,
   -> EFFECTIVE_TIME_NONCOMPARABLE; no retroactive insertion

7. Preserve source/field support states exactly.
   TARGET_UNAVAILABLE, ZERO_SUPPORT, LOW_SUPPORT, OBSERVED_ZERO,
   SOURCE_CONFLICT and SOURCE_COMPONENT_NONCOMPARABLE retain source scope.

8. Require exact metabolism authority/read permission.
   missing M -> MISSING_METABOLISM_AUTHORITY -> NO_PSEPF_TRANSITION_EFFECT

9. If all required conditions are positive for the exact requested operation,
   -> READ_ADMITTED for the exact component set and exact decision/use binding.
```

## 4. Requery versus rebind

This distinction is mandatory.

### `UPSTREAM_REQUERY_REQUIRED`

Use when the existing immutable PSEPF no longer answers the empirical question because an upstream-owned condition changed, including:

- the objective actor-fact snapshot used for comparator resolution is no longer the required snapshot;
- comparator authority or resolved conditioner predicate changes;
- source applicability changes;
- requested source universe changes;
- target/query/risk-set identity changes;
- the source/historical scope required by the use is different enough that a new field must be produced.

V3 does not mutate the old field. The old field remains valid historical/replay material.

### `STALE_OR_REBIND_REQUIRED`

Use when the existing immutable field remains empirically valid but the V3 decision binding is stale or different, including:

- a new V3 use class;
- a new decision context;
- a new decision/effective-time binding under an allowed relation to the same field;
- a changed metabolism-authority applicability binding;
- a changed actor/decision receipt that does not itself require a new comparator/query/field.

Rebinding never proves upstream empirical recomputation is necessary.

## 5. Future evidence / historical replay law

A decision at `D.t` may not consume source evidence whose availability/effective scope is in the future relative to `D.t` merely because that field is present now.

```text
CURRENT_REPOSITORY_AVAILABILITY != HISTORICAL_DECISION_AVAILABILITY
```

Historical replay binds the exact historical actor snapshot, PSEPF source components, authority versions and decision time. A newer field must not substitute for the historical field during replay.

## 6. Source plurality and temporal admission

Each PSEPF source component keeps its own source/historical scope and state. Generic admission may not silently discard an inconvenient component and then relabel the remainder as the original multi-source field.

For a multi-source operation:

- `SOURCE_COMPONENT_NONCOMPARABLE` remains attached to the exact component;
- `SOURCE_CONFLICT` remains a field comparison state;
- majority count, support rank, recency or locality does not select a winner;
- a source-scoped owner rule may read one exact component only when its own use contract explicitly requests that source/component and does not pretend to have composed or adjudicated the others;
- cross-source composition requires separate operation-specific authority.

## 7. Support-state time law

`LOW_SUPPORT` and `ZERO_SUPPORT` are empirical states, not time-alignment shortcuts.

- `LOW_SUPPORT` remains supported but weak/uncertain. A V3 owner may only use it under an exact read permission and owner rule that explicitly accepts low-support evidence. It never becomes certainty.
- `ZERO_SUPPORT` means there is no empirical conditional basis in that exact source/risk-set. It does not mean actor impossibility, zero belief, zero response probability, or metaphysical impossibility.
- `OBSERVED_ZERO` is a source/risk-set observation state and remains distinct from `ZERO_SUPPORT`.
- null/not-asked/inapplicable is never coerced into any zero state.

## 8. Scheduler nonownership fixture rule

If ADP-021 invokes a decision at scheduler time `T_sched`, the decision must carry its own exact `decision_effective_time` and field/snapshot refs. The scheduler may coordinate the invocation and receipt order; it may not:

- pick `latest` PSEPF;
- nearest-match a source wave;
- change actor snapshot time;
- backdate source evidence;
- convert a missing field into a scheduler-time default;
- advance empirical validity solely because causal time advanced.

## 9. Candidate receipt obligations

A V3 intake/read receipt should preserve, at minimum, exact refs/hashes for:

- actor or generated-person identity;
- objective actor-fact snapshot;
- comparator receipt/provenance chain;
- source-indexed PSEPF field/component set;
- source universe and historical scope per consulted component;
- V3 decision/use class and decision effective time;
- applicable time-alignment rule/authority ID/version/hash once SCRV3 freezes it;
- metabolism authority ID/version/hash;
- per-source typed states and field comparison state;
- V3 intake state (`ADMITTED`, `STALE_OR_REBIND_REQUIRED`, etc.);
- exact components/cells actually read when a metabolism-permitted owner consultation occurs;
- causal parent/replay refs where consultation affected an owner decision.

## 10. Unknown preserved for parent adjudication

SV3C does not mint the final accepted machine identity for the time-alignment rule. SCRV3 must decide whether this rule is canonically housed in the final `V3EmpiricalPossibilityInput` contract, the accepted metabolism authority dependency set, or another already-authorized SCRV3-local machine artifact.

What is frozen by this feeder candidate is the semantic ceiling:

```text
NO NEAREST/LATEST/BACKDATE/SCHEDULER-TIME SUBSTITUTION
AND
UPSTREAM REQUERY != V3 REBIND
AND
PER-SOURCE TIME/NEGATIVE STATE IS PRESERVED
AND
UNKNOWN ALIGNMENT => NO PSEPF TRANSITION EFFECT
```
